#!/usr/bin/env python3
"""SPCX(스페이스X) 부분 카드용 — 최근 4분기 합산(TTM)과 현재 배수를 만든다.

상장(2026-06-12) 직후라 SEC companyfacts에는 첫 10-Q(Q2 2026, 전년 비교 포함)뿐이다. 연간 실적은
최종 투자설명서(424B4, 2026-06-12)의 요약 재무 데이터에만 있다(S-1 XBRL은 표지 3KB뿐).
TTM = FY2025(투자설명서) + 2026 상반기(10-Q) − 2025 상반기(10-Q).

- 자기 이력(5년 배수)·내재가치(과거 성장 13분기 필요)·활동성(5년)은 만들 수 없다 → 카드에서 기권.
- 순손실·잉여현금흐름 적자라 PER·PCR은 "분모 0 이하"(currentNote negative → 동종업 0점).
- 주식 수 = 10-Q 표지(2026-07-28) Class A 7,696,293,669 + Class B 5,485,486,276. 2026-05 5:1 분할은
  두 자료 모두 반영된 뒤의 숫자다.

    python3 v2/adapters/spcx_ttm.py   # → v2/SPCX_multiples.json (동종업 점수 입력)
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
FACTS = os.path.join(V2, ".sec_cache", "0001181412_facts.json")   # SEC companyfacts (없으면 받아 둘 것)
PROSPECTUS = "https://www.sec.gov/Archives/edgar/data/1181412/000162828026042639/spaceexplorationtechnologi.htm"
TENQ = "https://www.sec.gov/Archives/edgar/data/1181412/000162828026052535/spcx-20260630.htm"

# 424B4 요약 재무 데이터(백만 달러) — 2025 회계연도
FY2025 = {"revenue": 18674, "opinc": -2589, "ni": -4937, "ocf": 6785, "capex": 20737, "da": 6701}
# 10-Q 표지(2026-07-28) + 8/14 Cursor 인수 대가로 발행한 Class A(389,289,254 + RSU 1,752,426, 8-K 2026-08-14)
SHARES = 7_696_293_669 + 5_485_486_276 + 389_289_254 + 1_752_426


def h1(facts, tag, year):
    for u in facts[tag]["units"].values():
        for r in u:
            if r.get("start") == f"{year}-01-01" and r["end"] == f"{year}-06-30":
                return r["val"] / 1e6
    raise KeyError(tag, year)


def instant(facts, tag, end):
    for u in facts[tag]["units"].values():
        for r in u:
            if "start" not in r and r["end"] == end:
                return r["val"] / 1e6
    raise KeyError(tag, end)


def main(price, day):
    facts = json.load(open(FACTS))["facts"]["us-gaap"]
    tags = {"revenue": "RevenueFromContractWithCustomerExcludingAssessedTax", "opinc": "OperatingIncomeLoss",
            "ni": "NetIncomeLoss", "ocf": "NetCashProvidedByUsedInOperatingActivities",
            "capex": "PaymentsToAcquirePropertyPlantAndEquipment", "da": "DepreciationDepletionAndAmortization"}
    ttm = {k: FY2025[k] + h1(facts, t, 2026) - h1(facts, t, 2025) for k, t in tags.items()}
    eq = instant(facts, "StockholdersEquity", "2026-06-30")
    cash = instant(facts, "CashAndCashEquivalentsAtCarryingValue", "2026-06-30") + \
        instant(facts, "MarketableSecuritiesCurrent", "2026-06-30")   # 현금 + 단기 유가증권(실적 발표 '현금·유가증권 $100B')
    debt = instant(facts, "LongTermDebt", "2026-06-30")
    mcap = price * SHARES / 1e6
    ebitda = ttm["opinc"] + ttm["da"]
    fcf = ttm["ocf"] - ttm["capex"]
    ev = mcap + debt - cash
    cur = lambda v: {"current": round(v, 2), "score": None, "percentile": None, "min": None, "median": None,
                     "max": None, "days": 0, "currentNote": None}
    neg = {"current": None, "score": None, "percentile": None, "min": None, "median": None, "max": None,
           "days": 0, "currentNote": "negative"}
    out = {"ticker": "SPCX", "window": [day, day], "perBasis": "diluted",
           "multiples": {"PER": neg if ttm["ni"] <= 0 else cur(mcap / ttm["ni"]),
                         "PSR": cur(mcap / ttm["revenue"]), "PBR": cur(mcap / eq),
                         "PCR": neg if fcf <= 0 else cur(mcap / fcf),
                         "EV/EBITDA": neg if ebitda <= 0 else cur(ev / ebitda)},
           "ttm": {k: round(v, 1) for k, v in ttm.items()} | {"ebitda": round(ebitda, 1), "fcf": round(fcf, 1)},
           "balance": {"equity": eq, "cash": cash, "debt": debt, "shares": SHARES},
           "sources": {"fy2025": PROSPECTUS, "h1": TENQ}, "asOf": day, "price": price}
    json.dump(out, open(os.path.join(V2, "SPCX_multiples.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out["multiples"], ensure_ascii=False), out["ttm"])


if __name__ == "__main__":
    h = open(os.path.join(V2, "SPCX_full_widget.html"), encoding="utf-8").read()
    daily = json.loads(re.search(r"const SPCX_DAILY\s*=\s*(\[.*?\]);", h, re.S).group(1))
    main(daily[-1][4], daily[-1][0])
