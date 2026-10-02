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
         "0000753308": {"Revenues": "RegulatedAndUnregulatedOperatingRevenue"},
         # BA: 재고를 InventoryNetOfAllowancesCustomerAdvancesAndProgressBillings로만 내 당좌비율이 유동비율과 같게 나왔다(Codex·Fable 2026-10-02).
         "0000012927": {"InventoryNet": "InventoryNetOfAllowancesCustomerAdvancesAndProgressBillings"},
         # ACN: 장기차입금을 LongTermDebtAndCapitalLeaseObligations로만 내 차입금의존도가 유동 차입금만으로 0.2%가 나왔다(Codex 2026-10-02, 10-Q 7.5%).
         "0001467373": {"LongTermDebt": "LongTermDebtAndCapitalLeaseObligations"},
         # PGR: 차입금을 DebtLongtermAndShorttermCombinedAmount로 낸다 — 목록의 LongTermDebt는 2016-06($2.66B)에 멈춰 차입금의존도가 2.1%로 나왔다(10-Q 6.7%, 2026-10-02).
         "0000080661": {"LongTermDebt": "DebtLongtermAndShorttermCombinedAmount"},
         # MPC: 장기차입금 목록 이름이 2012-03에 멈춰 차입금의존도가 5.8%로 나왔다(10-Q 34.8%, 2026-10-02).
         "0001510295": {"LongTermDebtNoncurrent": "LongTermDebtAndCapitalLeaseObligations"}}
# 총계 태그 없이 구성 줄만 낸 항목을 같은 제출·같은 날짜의 구성 줄 합으로 싣는다.
# ACN: 총부채 태그가 없어 부채비율이 자산 − 지배기업 자본(비지배지분·상환가능 비지배지분 포함)으로 115.8%가 나왔다 —
# 유동 21,609.1 + 비유동 13,689.7 = 10-Q 총부채 35,298.8(백만 달러, 2026-05-31; Codex 2026-10-02).
SUM = {"0001467373": {"Liabilities": ("LiabilitiesCurrent", "LiabilitiesNoncurrent")},
       # NEM: 당좌비율의 재고 = 재고 1,478 + 유동 광석 비축분 1,321(둘 다 회사 고유 태그, cfg_nem company_tags; Codex 2026-10-02).
       # InventoryNet은 2015년에 멈춘 옛 행이 있어 덮어쓴다(REPLACE).
       "0001164727": {"InventoryNet": ("InventoryNet", "InventoryOreStockpilesCurrentNem")}}
REPLACE = {"0001164727": {"InventoryNet"}}
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
    for dst, parts in SUM.get(cik, {}).items():
        if (dst in g and dst not in REPLACE.get(cik, ())) or not all(p in g for p in parts):
            continue
        rows = {}
        for unit, es in g[parts[0]]["units"].items():
            for e in es:
                if "start" in e:
                    continue
                vals = []
                for p in parts[1:]:
                    m = [x for x in g[p]["units"].get(unit, []) if x.get("end") == e["end"] and x.get("accn") == e.get("accn") and "start" not in x]
                    if not m:
                        break
                    vals.append(m[0]["val"])
                else:
                    rows.setdefault(unit, []).append(dict(e, val=e["val"] + sum(vals)))
        g[dst] = {"units": rows}
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
