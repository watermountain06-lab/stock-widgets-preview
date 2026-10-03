#!/usr/bin/env python3
"""종합 판정 시점 재현(verdict_replay_prereg.md)용 자료 받기 — 라이브 데이터는 건드리지 않는다.

- 가격: Yahoo 10년 일봉 + 분할 기록 → research/.prices10y/ (sp500_5y는 2021-09부터라 2024-10 평가일의
  "과거 5년" 자기 이력과 2026-03 평가월의 126거래일 수익률이 모자란다). CUTOFF 이후 봉은 버린다(장중 미완성 봉).
- SEC companyfacts: **지금 엔진 코드**가 쓰는 태그만 남겨 research/.facts_20261002/ (09-25 캐시는 그때 태그 목록).
재개 가능 — 이미 받은 종목은 건너뛴다.

    python3 v2/research/fetch_replay_data.py
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_universe_facts as fuf  # noqa: E402

PRICES = os.path.join(HERE, ".prices10y")
FACTS = os.path.join(HERE, ".facts_20261002")
EPS = os.path.join(HERE, ".eps_20261002")
CUTOFF = "2026-10-01"


def fetch_prices(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t.replace('.', '-')}?range=10y&interval=1d&events=split"
    raw = subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", url], capture_output=True, text=True, timeout=60).stdout
    r = json.loads(raw)["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    day = lambda ts: datetime.fromtimestamp(ts, tz=timezone.utc).astimezone().strftime("%Y-%m-%d")
    bars = [{"date": day(ts), "c": round(q["close"][i], 4)} for i, ts in enumerate(r["timestamp"])
            if q["close"][i] is not None and day(ts) <= CUTOFF]
    splits = sorted(({"date": day(s["date"]), "ratio": s["numerator"] / s["denominator"]}
                     for s in ((r.get("events") or {}).get("splits") or {}).values()), key=lambda s: s["date"])
    return {"daily": bars, "splits": splits}


def main():
    os.makedirs(PRICES, exist_ok=True)
    os.makedirs(FACTS, exist_ok=True)
    keep = fuf.wanted_tags()
    uni = json.load(open(fuf.SP500))
    errs = []
    for k, row in enumerate(uni):
        t, cik = row["ticker"], row["cik"].zfill(10)
        pp = os.path.join(PRICES, f"{t}.json")
        if not os.path.exists(pp):
            try:
                json.dump(fetch_prices(t), open(pp, "w"))
            except Exception as e:
                errs.append((t, "price", str(e)[:60]))
            time.sleep(0.3)
        fp = os.path.join(FACTS, f"{cik}_facts.json")
        if not os.path.exists(fp):
            r = subprocess.run(["curl", "-s", "-A", fuf.UA, f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"],
                               capture_output=True)
            try:
                data = json.loads(r.stdout)
                facts = data.get("facts", {})
                slim = {ns: {tg: v for tg, v in tags.items() if tg in keep} for ns, tags in facts.items() if ns in ("us-gaap", "dei")}
                json.dump({"cik": data.get("cik"), "entityName": data.get("entityName"), "facts": slim}, open(fp, "w"))
            except Exception as e:
                errs.append((t, "facts", str(e)[:60]))
            time.sleep(0.15)
        if k % 50 == 0:
            print(k, t, flush=True)
    print("완료, 오류", len(errs))
    for e in errs:
        print(" ", *e)


def main_eps():
    """희석 EPS(TTM) — 통제 유니버스와 같은 함수(fetch_control_universe.fetch_eps), 분할은 10년 가격 파일 기록으로."""
    sys.path.insert(0, "/Users/watermountain/Workspace/stock-widgets-redesign/scripts")
    import fetch_control_universe as fcu
    os.makedirs(EPS, exist_ok=True)
    errs = []
    for k, row in enumerate(json.load(open(fuf.SP500))):
        t, cik = row["ticker"], row["cik"].zfill(10)
        out, pp = os.path.join(EPS, f"{t}.json"), os.path.join(PRICES, f"{t}.json")
        if os.path.exists(out) or not os.path.exists(pp):
            continue
        try:
            json.dump(fcu.fetch_eps(t, cik, json.load(open(pp))["splits"]), open(out, "w"))
        except Exception as e:
            errs.append((t, str(e)[:60]))
        time.sleep(0.15)
        if k % 50 == 0:
            print("eps", k, t, flush=True)
    print("EPS 완료, 오류", len(errs), errs)


if __name__ == "__main__":
    main_eps() if "--eps" in sys.argv else main()
