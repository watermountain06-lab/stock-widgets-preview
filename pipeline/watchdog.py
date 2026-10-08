#!/usr/bin/env python3
"""예약 실행이 빠졌는지 본다 — 감시 작업(.github/workflows/watchdog.yml)이 하루 세 번 돌린다(2026-10-08).

GitHub는 바쁠 때 예약 실행을 늦추거나 그냥 건너뛰고, 건너뛴 실행은 아무 알림도 남기지 않는다(2026-09-21, 2026-10-08 가격 재시도).
health_check.py는 실행이 돌아야 돌므로 이 경우를 잡지 못한다. 여기서는 저장소에 남은 결과 파일의 날짜만 보고
무엇이 밀렸는지 한 줄씩 낸다. 다시 시작(dispatch)과 알림(실패 종료 → 메일)은 워크플로가 한다.

출력(마지막 줄 JSON): {"price": bool, "v2": bool, "weekly": bool, "notes": [...]}
    python3 pipeline/watchdog.py [--now 2026-10-08T15:30:00+00:00]
"""
import argparse
import json
import sys
from datetime import date, datetime, time as dtime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ET = ZoneInfo("America/New_York")
UTC = ZoneInfo("UTC")
# NYSE 휴장일 — 빠진 해가 오면 멈춘다(달력을 더할 것). 휴장일을 "밀림"으로 알리지 않으려고 둔다.
HOLIDAYS = {
    2026: ["2026-01-01", "2026-01-19", "2026-02-16", "2026-04-03", "2026-05-25", "2026-06-19", "2026-07-03",
           "2026-09-07", "2026-11-26", "2026-12-25"],
    2027: ["2027-01-01", "2027-01-18", "2027-02-15", "2027-03-26", "2027-05-31", "2027-06-18", "2027-07-05",
           "2027-09-06", "2027-11-25", "2027-12-24"],
}
PRICE_GRACE = dtime(10, 30)   # 장 마감 다음 날 오전 10:30 ET까지 — 저녁 실행과 아침 재시도 두 번(05:23·09:41 ET) 뒤
V2_GRACE = timedelta(hours=2)   # 가격 갱신 뒤 v2 재빌드(약 50분)를 기다리는 시간
WEEKLY_AT = (5, 15, 7)   # 토요일 15:07 UTC(v2_cards.yml)
WEEKLY_GRACE = timedelta(hours=4)


def trading_day(d):
    if d.year not in HOLIDAYS:
        sys.exit(f"watchdog: {d.year}년 휴장일이 없다 — HOLIDAYS에 더할 것")
    return d.weekday() < 5 and d.isoformat() not in HOLIDAYS[d.year]


def due_session(now_et):
    """지금쯤 사이트에 올라와 있어야 할 세션 — 다음 날 PRICE_GRACE가 지난 가장 최근 거래일."""
    d = now_et.date() - timedelta(days=1)
    while True:
        if trading_day(d) and now_et >= datetime.combine(d + timedelta(days=1), PRICE_GRACE, ET):
            return d
        d -= timedelta(days=1)


def last_weekly(now_utc):
    """가장 최근 토요일 실행 시각(UTC) — 아직 WEEKLY_GRACE가 안 지났으면 그 전 주."""
    d = now_utc.date()
    while d.weekday() != WEEKLY_AT[0]:
        d -= timedelta(days=1)
    t = datetime.combine(d, dtime(WEEKLY_AT[1], WEEKLY_AT[2]), UTC)
    return t if now_utc >= t + WEEKLY_GRACE else t - timedelta(days=7)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--now")
    a = ap.parse_args()
    now = datetime.fromisoformat(a.now).astimezone(UTC) if a.now else datetime.now(UTC)
    now_et = now.astimezone(ET)
    stocks = json.loads((ROOT / "site_data" / "stocks.json").read_text(encoding="utf-8"))
    status_p, weekly_p = ROOT / "v2" / "daily_status.json", ROOT / "v2" / "weekly_status.json"
    daily = json.loads(status_p.read_text(encoding="utf-8")) if status_p.exists() else {}
    out = {"price": False, "v2": False, "weekly": False, "notes": []}

    due, sess = due_session(now_et).isoformat(), stocks.get("priceSession", "")
    if sess < due:
        out["price"] = True
        out["notes"].append(f"가격이 {sess}에 멈춤 — {due} 세션이 올라와 있어야 한다")
    # 가격은 최신인데 v2 카드가 뒤처짐 — 가격 커밋 뒤 V2_GRACE가 지났을 때만(재빌드 중일 수 있다)
    gen = stocks.get("generatedAt") or stocks.get("asOf") or ""
    try:
        price_time = datetime.fromisoformat(gen.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        price_time = None
    if daily.get("session", "") < sess and (price_time is None or now - price_time >= V2_GRACE):
        out["v2"] = True
        out["notes"].append(f"v2 카드가 {daily.get('session')}에 멈춤 — 가격은 {sess}")
    elif daily.get("session") == sess and not (daily.get("full") and daily.get("finished")):
        # 중단된 실행, 또는 일부 종목만 다시 만든 실행 — 나머지 카드는 전 세션일 수 있다(Codex)
        out["notes"].append("v2 재빌드가 이 세션에서 전체를 끝내지 못했다(중단 또는 일부만)")
        out["v2"] = True

    lw = last_weekly(now)
    if lw >= datetime(2026, 10, 10, 15, 7, tzinfo=UTC):   # 토요일 결과 파일은 10/10 실행부터 생긴다
        w = json.loads(weekly_p.read_text(encoding="utf-8")) if weekly_p.exists() else {}
        fin = w.get("finished") or ""
        try:
            fin_t = datetime.strptime(fin, "%Y-%m-%dT%H:%M:%S%z").astimezone(UTC)
        except ValueError:
            fin_t = None
        if fin_t is None or fin_t < lw:
            out["weekly"] = True
            out["notes"].append(f"토요일 실행({lw:%m/%d %H:%M} UTC) 결과가 없다 — 마지막 {fin or '없음'}")

    for n in out["notes"]:
        print(n)
    print("밀린 것 없음" if not out["notes"] else "")
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main()
