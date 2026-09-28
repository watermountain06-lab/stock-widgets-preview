#!/usr/bin/env python3
"""ASML 어댑터 — 분기 실적 6-K의 US GAAP 첨부("Quarterly Summary", 최근 5개 분기)를 SEC companyfacts 모양으로 바꾼다.

왜 필요한가 (2026-09-28)
------------------------
ASML은 20-F(US GAAP)를 내지만 **분기 보고서(10-Q)를 내지 않아** companyfacts에는 연간 유로 값만 있다.
v2 스크립트는 분기 행(TTM)과 USD·shares·USD/shares 단위 키를 읽으므로, TSM·SKHY 어댑터와 같은 방식으로
분기마다 6-K에 붙는 US GAAP 요약 재무제표(EX-99, "financialstatementsusgaap")에서 숫자를 꺼내 같은 모양으로 쓴다.

- 원문: `asml_reports.py` → `.sec_cache/asml_reports/`, 목록 `asml_manifest.json` (2020-01 ~ )
- 추출: `asml_extract.py` (백만 유로, 주당 값 유로, 주식 수 백만 주)
- 값은 **유로 그대로**(단위 키는 스크립트 호환용 "USD"). 가격(나스닥, 달러)과 만나는 곳에서 v2/fx.py가
  그날 환율(ECB 기준환율 1유로당 달러의 역수, fx.py)을 곱한다 — TSM·SKHY와 같은 규칙. FRED DEXUSEU(연준 H.10)가
  2026-09-28 응답하지 않아 ECB를 썼다 — 고시 시각이 달라(14:15 CET 대 정오 NY) 보통 0.5% 안 차이. 되돌릴 때 INVERT는 유지(둘 다 1유로당 달러).
- 나스닥 주식은 뉴욕 등록 보통주(ADR 아님, 1주 = 보통주 1주)라 주식 수·EPS를 바꾸지 않는다.
- 요약표는 분기마다 **3개월 값**을 준다(4분기도 3개월). 분기마다 그 분기가 처음 실린 보고서(맨 오른쪽 열)의
  값을 쓴다 — 나중 보고서의 재작성 값으로 과거를 덮지 않는다(시점 규칙). 손익은 3개월 행과 누적 행을(누적 EPS는 본문의 누적 열),
  현금흐름·감가상각은 US 10-Q처럼 누적 행만 싣는다.
- 회계연도 = 달력연도(12-31 결산). 분기말은 13주 달력(예: 2021-04-04)이라 원문 날짜 그대로 쓴다.
- filed = 6-K 접수일 **당일**. 접수 시각이 UTC 10시 전후(미국 동부 06시)로 나스닥 개장 전이다.
- 주식 수: 분기 요약에 기말 주식 수가 없어 **기본 가중평균 주식 수**를 CommonStockSharesOutstanding로 싣는다
  (2026-06-28: 384.5M. 20-F 표지의 2025-12-31 기말 385.4M과 0.3% 차이).
- 부채: 요약 재무상태표는 유동부채를 한 줄로만 준다. 유동 차입금(단기차입금·유동성 장기부채)은 반기 법정보고서와
  20-F에만 있어 `asml_semiannual.json`(6월·12월)에서 LongTermDebtCurrent로 싣는다 — 1·3분기는 직전 값이 이어진다.
  리스부채는 분기·반기 모두 따로 없어 뺀다(2025-12-31 사용권자산 €341M 수준).
- 이자비용: 손익계산서는 "Interest and other, net"(순액)뿐이라 InterestExpense를 싣지 않는다.
- 2019년은 4분기만 있어(첫 보고서가 2020-01) 재무상태표(2019-12-31)만 싣는다(분기가 모자라면 TTM이 엉뚱하게 묶인다, TSM 교훈).

    python3 v2/adapters/asml_reports.py     # 새 보고서 받기
    python3 v2/adapters/asml_ifrs.py        # → v2/.sec_cache/0000937966_facts.json
"""
import json
import os
import sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from asml_extract import extract, get, ytd_eps  # noqa: E402

V2 = os.path.dirname(HERE)
CACHE = os.path.join(V2, ".sec_cache")
REPORTS = os.path.join(CACHE, "asml_reports")
MANIFEST = os.path.join(HERE, "asml_manifest.json")
OUT = os.path.join(CACHE, "0000937966_facts.json")
CIK = "0000937966"
MIL = 1_000_000

# (태그, 원문 라벨, 부호) — 부호 −1은 원문이 비용을 음수로 적은 줄
IS = [("RevenueFromContractWithCustomerExcludingAssessedTax", "Total net sales", 1),
      ("Revenues", "Total net sales", 1),
      ("CostOfRevenue", "Total cost of sales", -1),
      ("GrossProfit", "Gross profit", 1),
      ("ResearchAndDevelopmentExpense", "Research and development costs", -1),
      ("SellingGeneralAndAdministrativeExpense", "Selling, general and administrative costs", -1),
      ("OperatingIncomeLoss", "Income from operations", 1),
      ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
       "Income before income taxes", 1),
      ("IncomeTaxExpenseBenefit", "Benefit from (provision for) income taxes", -1),
      ("NetIncomeLoss", "Net income", 1)]
EPS = [("EarningsPerShareDiluted", "Diluted net income per ordinary share"),
       ("EarningsPerShareBasic", "Basic net income per ordinary share")]
# 현금흐름: 라벨 후보(연도마다 이름이 바뀐 줄), 부호
CF = [("NetCashProvidedByUsedInOperatingActivities", ["Net cash provided by (used in) operating activities"], 1),
      ("PaymentsToAcquirePropertyPlantAndEquipment", ["Purchase of property, plant and equipment"], -1),
      ("PaymentsToAcquireIntangibleAssets", ["Purchase of intangible assets"], -1),
      ("DepreciationDepletionAndAmortization", ["Depreciation and amortization"], 1),
      ("ShareBasedCompensation", ["Share-based compensation expense", "Share-based payments"], 1),
      ("PaymentsOfDividendsCommonStock", ["Dividend paid"], -1),
      ("PaymentsForRepurchaseOfCommonStock", ["Purchase of treasury shares", "Purchase of shares"], -1)]
BS = [("CashAndCashEquivalentsAtCarryingValue", "Cash and cash equivalents"),
      ("ShortTermInvestments", "Short-term investments"),
      ("AccountsReceivableNetCurrent", "Accounts receivable, net"),
      ("InventoryNet", "Inventories, net"),
      ("AssetsCurrent", "Total current assets"),
      ("Assets", "Total assets"),
      ("LiabilitiesCurrent", "Total current liabilities"),
      ("Liabilities", "Total liabilities"),
      ("LongTermDebtNoncurrent", "Long-term debt"),
      ("StockholdersEquity", "Total shareholders’ equity"),
      ("EquityMethodInvestments", "Equity method investments"),
      ("Goodwill", "Goodwill")]
# 없던 줄이 새로 생긴 항목 — 있는 분기만 싣는다. "Equity investments"는 2025년 3분기 Mistral AI 지분(€1.3B 투자)부터
# 재무상태표에 따로 나온다. 장기투자로 실어 build_dcf가 비영업 자산으로 더한다.
BS_OPTIONAL = [("LongTermInvestments", "Equity investments")]


def build():
    man = json.load(open(MANIFEST))
    q = {}      # 분기말 → (행, 보고서) — 그 분기가 맨 오른쪽 열로 처음 실린 보고서
    for m in sorted(man, key=lambda x: x["filed"]):
        r = extract(os.path.join(REPORTS, m["file"]))
        last = max(r)
        if last not in q:
            q[last] = (r[last], m)
    ends = sorted(q)
    facts = {}

    def add(tag, unit, row):
        facts.setdefault(tag, {"units": {}})["units"].setdefault(unit, []).append(row)

    def need(rows, label, e):
        v = get(rows, label)
        if v is None:
            raise SystemExit(f"{e}: '{label}' 없음")
        return v

    by_year = {}
    for e in ends:
        by_year.setdefault(int(e[:4]), []).append(e)
    for y, es in sorted(by_year.items()):
        es = sorted(es)
        full = len(es) == 4 or (len(es) < 4 and es[0][5:7] in ("03", "04") and y == int(ends[-1][:4]))
        prev_end = None
        ytd = {}
        for n, e in enumerate(es, 1):
            rows, m = q[e]
            start = f"{y}-01-01" if n == 1 else (date.fromisoformat(prev_end) + timedelta(days=1)).isoformat()
            fp, form = ("FY", "10-K") if e.endswith("12-31") else (f"Q{n}", "10-Q")
            meta = {"end": e, "accn": m["accn"], "fy": y, "fp": fp, "form": form, "filed": m["filed"]}
            if full:
                for tag, label, sign in IS:
                    v = need(rows, label, e) * sign * MIL
                    ytd[tag] = ytd.get(tag, 0.0) + v
                    add(tag, "USD", {**meta, "start": start, "val": v})
                    if n >= 2:
                        add(tag, "USD", {**meta, "start": f"{y}-01-01", "val": ytd[tag]})
                cum = ytd_eps(os.path.join(REPORTS, m["file"])) if n >= 2 else None
                if n >= 2 and not cum:
                    raise SystemExit(f"{e}: 본문 누적 EPS 없음")
                for tag, label in EPS:
                    v = need(rows, label, e)
                    add(tag, "USD/shares", {**meta, "start": start, "val": v})
                    # 누적 EPS는 본문 손익계산서의 누적 열(분기 합과 1~3센트 다르다, Codex)
                    if n >= 2:
                        add(tag, "USD/shares", {**meta, "start": f"{y}-01-01",
                                                "val": cum["diluted" if tag.endswith("Diluted") else "basic"]})
                for tag, labels, sign in CF:
                    v = next((get(rows, lb) for lb in labels if get(rows, lb) is not None), 0.0)
                    ytd[tag] = ytd.get(tag, 0.0) + v * sign * MIL
                    add(tag, "USD", {**meta, "start": f"{y}-01-01", "val": ytd[tag]})
                add("WeightedAverageNumberOfDilutedSharesOutstanding", "shares",
                    {**meta, "start": start, "val": need(rows, "Diluted", e) * MIL})
            for tag, label in BS:
                add(tag, "USD", {**meta, "val": need(rows, label, e) * MIL})
            for tag, label in BS_OPTIONAL:
                v = rows.get(label)      # 끝부분 맞추기(get)를 쓰면 "Equity method investments"와 헷갈리지 않게 정확히
                if v is not None:
                    add(tag, "USD", {**meta, "val": v * MIL})
            add("CommonStockSharesOutstanding", "shares", {**meta, "val": need(rows, "Basic", e) * MIL})
            prev_end = e
    semi = json.load(open(os.path.join(HERE, "asml_semiannual.json")))
    for r in semi["LongTermDebtCurrent"]:
        e = r["end"]
        add("LongTermDebtCurrent", "USD", {"end": e, "accn": "semiannual", "fy": int(e[:4]),
                                           "fp": "FY" if e.endswith("12-31") else "Q2",
                                           "form": "10-K" if e.endswith("12-31") else "10-Q",
                                           "filed": r["filed"], "val": r["val_meur"] * MIL})
    shares = facts.pop("CommonStockSharesOutstanding")
    out = {"cik": int(CIK), "entityName": "ASML Holding N.V. (v2 adapter)",
           "facts": {"us-gaap": {**facts, "CommonStockSharesOutstanding": shares},
                     "dei": {"EntityCommonStockSharesOutstanding": shares}},
           "_adapter": {"source": "ASML quarterly 6-K US GAAP summary financial statements (Quarterly Summary, 5 quarters)",
                        "valuesCurrency": "EUR", "fx": "ECB euro reference rate (USD per EUR, 14:15 CET), inverted — FRED DEXUSEU unreachable 2026-09-28",
                        "reports": len(man), "quarters": ends, "built": date.today().isoformat()}}
    json.dump(out, open(OUT, "w"))
    print(f"저장: {OUT} — 보고서 {len(man)}건, 분기 {len(ends)}개({ends[0]} ~ {ends[-1]}), 태그 {len(facts) + 1}개")
    return out


if __name__ == "__main__":
    build()
