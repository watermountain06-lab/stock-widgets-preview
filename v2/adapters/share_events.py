#!/usr/bin/env python3
"""분기 뒤 주식 발행 이벤트를 "주식 + 받은 현금" 한 묶음으로 오버레이에 넣는다(v2.1 D-1, 2026-10-05).

공모·전환·워런트 행사로 주식이 늘면, 주식 수만 늘리면 현금이 빠진 채 시가총액만 커지고 주당 가치가 줄어든다.
`v2/share_events.json`에 공시 원문으로 확인한 이벤트를 적고, 이 스크립트가 `.sec_cache/overlay/{cik}.json`에
그날 기준 표지 주식 수(dei:EntityCommonStockSharesOutstanding)와 현금(직전 분기말 현금 + 순수입금)을 한 행씩 넣는다.
자본(StockholdersEquity·연결 자본)에도 같은 순수입금을 더한다 — 현금만 늘리면 투하자본(자본 + 차입금 − 현금)이 줄고 PBR이
새 주식 수와 옛 자본을 섞는다(Codex). 공개일 = 이벤트를 밝힌 8-K·증권신고서 공시일. 이벤트 행은 날짜가 붙어 있어 지우지 않는다 —
그 뒤 결산의 10-Q/10-K가 들어오면 더 새 결산일이라 지금 값은 그 공시가 덮고, 그 사이 날짜의 과거 계산(자기 이력·DCF 추적)은
이벤트를 계속 쓴다(Codex). 조건부 주식·행사 전 워런트는 넣지 않는다(카드 문장에만).

    python3 v2/adapters/share_events.py INTC      # 오버레이 갱신(예전에 넣은 이벤트 행을 지우고 다시 쓴다)
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
    """엔진과 같은 경로로 받는다(캐시가 없으면 SEC에서 받아 둔다)."""
    sys.path.insert(0, V2)
    import build_multiple_history as bmh
    cwd = os.getcwd(); os.chdir(V2)
    try:
        return bmh._facts(cik)["facts"]
    finally:
        os.chdir(cwd)


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
    eq_rows = {tg: [r for r in f["us-gaap"].get(tg, {}).get("units", {}).get("USD", []) if r.get("form") in ("10-Q", "10-K")]
               for tg in ("StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest")}
    for e in spec["events"]:
        if any(r["end"] >= e["date"] for r in periodic):
            print(f"{T} {e['date']}: 그 뒤 결산 정기 공시가 있다 — 지금 값은 그 공시가 덮고, 이벤트 행은 과거 날짜 계산을 위해 남긴다")
        cash0 = latest(periodic, e["date"])
        if cash0 is None:
            sys.exit(f"{T}: 이벤트 전 분기말 현금이 없다")
        row = {"end": e["date"], "filed": e["filed"], "form": "8-K", "accn": e["accn"], "src": f"{SRC}: {e['src']}"}
        ov.setdefault("dei", {}).setdefault("EntityCommonStockSharesOutstanding", []).append(
            {**row, "val": e["shares_after"], "unit": "shares"})
        ov.setdefault("us-gaap", {}).setdefault("CashAndCashEquivalentsAtCarryingValue", []).append(
            {**row, "val": cash0["val"] + e["net_proceeds"], "unit": "USD"})
        for tg, rows in eq_rows.items():   # 자본에도 순수입금(현금과 짝)
            eq0 = latest(rows, e["date"])
            if eq0:
                ov["us-gaap"].setdefault(tg, []).append({**row, "val": eq0["val"] + e["net_proceeds"], "unit": "USD"})
        live.append(e)
        print(f"{T} {e['date']}: 주식 {e['shares_after']:,} · 현금 {cash0['val'] / 1e9:.2f}B({cash0['end']}) + {e['net_proceeds'] / 1e9:.2f}B")
    os.makedirs(os.path.dirname(op), exist_ok=True)
    json.dump(ov, open(op, "w"), indent=1)
    print(f"저장: {op} · 살아 있는 이벤트 {len(live)}개")


if __name__ == "__main__":
    main(sys.argv[1].upper())
