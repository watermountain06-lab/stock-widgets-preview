#!/usr/bin/env python3
"""오버레이를 합친 companyfacts로 redesign의 fetch_financials를 돌린다(2026-09-27, V).

fetch_financials는 SEC API를 직접 부른다. companyfacts가 최신 10-Q를 아직 싣지 않은 종목(V: 2026-07-29 10-Q)은
`ixbrl_supplement.py`가 오버레이에 보충한 값을 build_multiple_history._facts(캐시 + 오버레이)로 먹인다.

    python3 v2/adapters/overlay_feed.py V 0001403161
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
sys.path.insert(0, V2)
import build_multiple_history as bmh  # noqa: E402


# fetch_financials 태그 목록에 없는 이름으로 낸 항목을 목록 안 이름으로 옮겨 싣는다(목록 이름이 멈췄을 때만 의미가 있다).
# WELL: 이자비용이 2022-12부터 InterestExpenseBorrowings — 목록의 InterestExpenseDebt는 2024-09에 멈춰 이자보상배율이 비었다(Codex 2026-10-02).
ALIAS = {"0000766704": {"InterestExpense": "InterestExpenseBorrowings"},
         # NEE: 총매출 RegulatedAndUnregulatedOperatingRevenue를 fetch_financials가 아는 이름으로(엔진 EXTRA_TAGS와 같은 기준, Codex 2026-10-02).
         # 이자비용은 회사 고유 태그라 대신할 표준 태그가 없다(현금 이자 지급액은 다른 항목이라 쓰지 않는다 — Codex).
         "0000753308": {"Revenues": "RegulatedAndUnregulatedOperatingRevenue"}}
# 함께 지울 태그(엔진 EXCLUDE_TAGS와 같은 기준) — NEE 주석의 고객 계약 매출(0.1B 반올림)
DROP = {"0000753308": ("RevenueFromContractWithCustomerIncludingAssessedTax",)}


def _facts_with_alias(cik):
    data = bmh._facts(cik)
    g = data["facts"]["us-gaap"]
    for t in DROP.get(cik, ()):
        g.pop(t, None)
    for dst, src in ALIAS.get(cik, {}).items():
        if src in g:   # 목록 이름이 옛 기간에만 있어도(NEE Revenues는 2013년에 멈춤) 덮어쓴다
            g[dst] = g[src]
    return data


def main(ticker, cik):
    sys.path.insert(0, os.path.join(os.path.dirname(REPO), "stock-widgets-redesign", "scripts"))
    import fetch_financials as ff
    ff.fetch_json = lambda url, ua: _facts_with_alias(cik)
    sys.argv = ["fetch_financials.py", ticker, "--cik", cik, "--years", "5",
                "--out", os.path.join(V2, "fundamental_data", f"{ticker}_financials.json")]
    ff.main()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2].zfill(10))
