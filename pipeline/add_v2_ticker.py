#!/usr/bin/env python3
"""새 v2 카드를 홈 목록(site_data/stocks.json)에 더한다 — 2026-10-07 33장 이관과 같은 모양(2026-10-13).

    python3 pipeline/add_v2_ticker.py VLO --name "발레로 에너지"

- cardRank = 목록 끝 번호 + 1(카드 순위 — 시총 순위가 아니다. 검사기가 중복·공백을 막는다).
- sector = meta/{t}.json의 sub("NYSE · 에너지 — 정유")에서 거래소 뒤, cardAsOf = 카드 일봉 마지막 날.
- shares = v2 엔진 SEC 요약 자료의 dei EntityCommonStockSharesOutstanding 최신 값(단일 클래스만 — 클래스가 여럿이면 멈춘다, 손으로 classes를 넣는다).
- price는 "unavailable"로 두고 이어서 `python3 pipeline/fetch_prices.py --tickers T --write`, 등급·점수는 `python3 pipeline/sync_v2_home.py`가 채운다.
이미 목록에 있으면 아무것도 하지 않는다.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "v2"
sys.path.insert(0, str(V2))
sys.path.insert(0, str(ROOT / "scripts"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--name", required=True, help="홈에 보일 한국어 이름")
    a = ap.parse_args()
    T, t = a.ticker.upper(), a.ticker.lower()
    sp = ROOT / "site_data" / "stocks.json"
    data = json.loads(sp.read_text(encoding="utf-8"))
    if any(x["ticker"] == T for x in data["tickers"]):
        print(f"{T}: 이미 목록에 있다 — 그대로 둔다")
        return
    card = (V2 / f"{T}_full_widget.html").read_text(encoding="utf-8")
    daily = re.search(rf"const {T}_DAILY\s*=\s*(\[.*?\]);", card, re.S).group(1)
    as_of = re.findall(r'\["(\d{4}-\d{2}-\d{2})",', daily)[-1]
    meta = json.loads((V2 / "newcards" / "meta" / f"{t}.json").read_text(encoding="utf-8"))
    sector = meta["sub"].split("·", 1)[-1].strip()
    import build_multiple_history as bmh
    import fetch_eps_history as feh
    cik = str(feh.CIKS[T]).zfill(10)
    rows = bmh._facts(cik)["facts"].get("dei", {}).get("EntityCommonStockSharesOutstanding", {}).get("units", {}).get("shares", [])
    if not rows:
        sys.exit(f"{T}: dei 주식 수가 없다 — shares를 손으로 넣는다(method·basis·asOf·filedAt·filing·status)")
    last = max(r["end"] for r in rows)
    cur = [r for r in rows if r["end"] == last]
    if len({r["val"] for r in cur}) > 1:
        sys.exit(f"{T}: {last}에 dei 주식 수가 여러 개(클래스별) — shares.classes를 손으로 넣는다")
    r = max(cur, key=lambda x: x["filed"])
    appr = json.loads((V2 / "sec_approved.json").read_text(encoding="utf-8")).get(cik)
    if r["filed"] != appr:   # 마지막 dei 행이 카드의 기준 공시 것이 아니면 낡았거나(V는 2010년에 멈춤) 클래스별로 빠진 것이다(Codex 2026-10-13)
        sys.exit(f"{T}: dei 주식 수({last}, 접수 {r['filed']})가 기준 공시({appr})의 것이 아니다 — 표지 주식 수를 확인해 shares를 손으로 넣는다")
    rank = max(x["cardRank"] for x in data["tickers"]) + 1
    data["tickers"].append({
        "ticker": T, "name": a.name, "sector": sector, "href": f"{T}_full_widget.html",
        "cardRank": rank, "cardAsOf": as_of, "listing": {"type": "common"},
        "price": {"close": None, "status": "unavailable", "statusReason": "새 종목 — 가격 받기 전(fetch_prices.py --write)"},
        "shares": {"usEquivalent": int(r["val"]), "method": "sec-dei", "basis": "single", "asOf": r["end"], "filedAt": r["filed"],
                   "filing": f'{r.get("form")} {r.get("accn")} dei (v2 카드 엔진 facts)', "status": "ok"},
        "tier": {"value": None, "raw": None, "status": "missing", "note": "추가 직후 — sync_v2_home.py가 채운다"},
        "score": {"status": "excluded", "reason": "추가 직후 — sync_v2_home.py가 채운다"},
    })
    sp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{T}: 홈 목록 {rank}번째로 추가(cardAsOf {as_of}, 주식 수 {int(r['val']):,} {r['end']}) — 이어서 fetch_prices --write, sync_v2_home")


if __name__ == "__main__":
    main()
