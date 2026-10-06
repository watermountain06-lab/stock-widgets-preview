#!/usr/bin/env python3
"""분기 뒤 주식 발행 이벤트를 "주식 + 받은 현금" 한 묶음으로 오버레이에 넣는다(v2.1 D-1, 2026-10-05).

공모·전환·워런트 행사로 주식이 늘면, 주식 수만 늘리면 현금이 빠진 채 시가총액만 커지고 주당 가치가 줄어든다.
`v2/share_events.json`에 공시 원문으로 확인한 이벤트를 적고, 이 스크립트가 `.sec_cache/overlay/{cik}.json`에
그날 기준 표지 주식 수(dei:EntityCommonStockSharesOutstanding)와 현금(직전 분기말 현금 + 순수입금)을 한 행씩 넣는다.
공개일 = 이벤트를 밝힌 8-K·증권신고서 공시일. **그 날짜 뒤 결산의 10-Q/10-K가 companyfacts에 들어오면 이벤트를 끈다**
(그 공시가 주식·현금을 이미 담는다). 조건부 주식·행사 전 워런트는 넣지 않는다(카드 문장에만).

    python3 v2/adapters/share_events.py INTC      # 오버레이 갱신(이벤트가 꺼졌으면 넣었던 행을 지운다)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
EVENTS = os.path.join(V2, "share_events.json")
CACHE = os.path.join(V2, ".sec_cache")
SRC = "share-event"


def facts(cik):
    return json.load(open(os.path.join(CACHE, f"{cik}_facts.json")))["facts"]


def latest(rows, before):
    ok = [r for r in rows if r["end"] <= before]
    return max(ok, key=lambda r: (r["end"], r["filed"])) if ok else None


def main(T):
    ev_all = json.load(open(EVENTS))
    spec = ev_all.get(T)
    if not spec:
        sys.exit(f"{T}: share_events.json에 이벤트가 없다")
    cik = spec["cik"]
    f = facts(cik)
    # 이벤트 뒤 결산의 정기 공시가 있으면 끈다
    periodic = [r for r in f["us-gaap"].get("CashAndCashEquivalentsAtCarryingValue", {}).get("units", {}).get("USD", [])
                if r.get("form") in ("10-Q", "10-K")]
    op = os.path.join(CACHE, "overlay", f"{cik}.json")
    ov = json.load(open(op)) if os.path.exists(op) else {}
    # 예전에 넣은 이벤트 행은 지우고 다시 쓴다
    for tax in ov.values():
        for tag in list(tax):
            tax[tag] = [r for r in tax[tag] if not str(r.get("src", "")).startswith(SRC)]
            if not tax[tag]:
                del tax[tag]
    live = []
    for e in spec["events"]:
        if any(r["end"] >= e["date"] for r in periodic):
            print(f"{T} {e['date']}: 이후 결산 정기 공시가 있어 끈다 — {e['src'][:60]}")
            continue
        cash0 = latest(periodic, e["date"])
        if cash0 is None:
            sys.exit(f"{T}: 이벤트 전 분기말 현금이 없다")
        row = {"end": e["date"], "filed": e["filed"], "form": "8-K", "accn": e["accn"], "src": f"{SRC}: {e['src']}"}
        ov.setdefault("dei", {}).setdefault("EntityCommonStockSharesOutstanding", []).append(
            {**row, "val": e["shares_after"], "unit": "shares"})
        ov.setdefault("us-gaap", {}).setdefault("CashAndCashEquivalentsAtCarryingValue", []).append(
            {**row, "val": cash0["val"] + e["net_proceeds"], "unit": "USD"})
        live.append(e)
        print(f"{T} {e['date']}: 주식 {e['shares_after']:,} · 현금 {cash0['val'] / 1e9:.2f}B({cash0['end']}) + {e['net_proceeds'] / 1e9:.2f}B")
    os.makedirs(os.path.dirname(op), exist_ok=True)
    json.dump(ov, open(op, "w"), indent=1)
    print(f"저장: {op} · 살아 있는 이벤트 {len(live)}개")


if __name__ == "__main__":
    main(sys.argv[1].upper())
