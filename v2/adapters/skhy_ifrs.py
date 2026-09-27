#!/usr/bin/env python3
"""SKHY 어댑터 — SK하이닉스 연결재무제표(K-IFRS, KIND 원문)를 SEC companyfacts 모양으로 바꾼다.

왜 필요한가 (2026-09-27)
------------------------
SKHY는 2026-07-10 나스닥 ADR 상장. SEC에는 F-1·424B4·6-K뿐이고 companyfacts는 사실상 비어 있다.
v2 스크립트는 전부 companyfacts의 us-gaap 태그를 읽으므로, TSM 어댑터(tsm_ifrs.py)와 같은 방식으로
한국 원문 보고서(분기·반기보고서, 연결감사보고서)에서 숫자를 꺼내 같은 모양으로 쓴다.

- 원문: `skhy_reports.py`(KIND) → `.sec_cache/skhy_reports/`, 목록은 `skhy_manifest.json`
- 추출: `skhy_extract.py`(표를 내용으로 찾음, 백만원)
- 값은 **원화 그대로**(단위 키는 스크립트 호환용 "USD"). 가격(ADR, 달러)과 만나는 곳에서 v2/fx.py가
  그날 환율(연준 H.10 DEXKOUS)을 곱한다 — TSM과 같은 규칙(2026-09-25 사용자 결정).
- 주식 수·EPS는 **ADR 1주(= 보통주 0.1주)** 기준: 주식 수 × 10, EPS ÷ 10 (424B4 "Each ADS represents
  one-tenth of a common share").
- 손익 Q1~Q3는 3개월 값, Q4 = 연간(감사보고서) − 3분기 누적. 현금흐름·감가상각은 누적의 차이.
- 2019년은 연간 감사보고서만 있어 재무상태표(2019-12-31)만 싣는다(분기가 없으면 TTM이 엉뚱하게 묶인다, TSM 교훈).
- filed = 공시일 **다음 날**. 한국 공시는 16~17시(KST)로 KRX 장 마감(15:30) 뒤라, 원주 가격 이력에서
  그날 종가에 쓰면 몇 시간 앞당겨 쓰는 셈이다. 예비 실적(잠정실적, 한 달 앞)보다 늦어 보수적이다.
- 이자비용 줄은 손익계산서에 따로 없어(금융비용에 환손실 등 섞임) **현금흐름표 "이자의 지급"**을
  InterestExpense로 싣는다.

    python3 v2/adapters/skhy_reports.py     # 새 보고서 받기
    python3 v2/adapters/skhy_ifrs.py        # → v2/.sec_cache/0002120882_facts.json
"""
import json
import os
import sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from skhy_extract import extract  # noqa: E402

V2 = os.path.dirname(HERE)
CACHE = os.path.join(V2, ".sec_cache")
REPORTS = os.path.join(CACHE, "skhy_reports")
MANIFEST = os.path.join(HERE, "skhy_manifest.json")
OUT = os.path.join(CACHE, "0002120882_facts.json")
CIK = "0002120882"
ADS_PER_SHARE = 10      # 1 ADS = 보통주 0.1주 (424B4, 2026-07-10)
MIL = 1_000_000         # 원문 단위 백만원
# 분기보고서 뒤에 알려진 주식 수(보통주, 발행 − 자기주식). 공시 원문에서 확인한 값만 적는다.
#   2026-07-10 ADR 공모 신주 17,790,000주(424B4) → 2026-08-21 자기주식처분결과보고서:
#   발행주식 730,492,365(8/19 주식 소각 결정 공시) − 자기주식 1,625,769 = 728,866,596
#   (8/20~11/19 소각 목적 자기주식 취득 최대 24,070,000주는 결과 공시 전이라 반영하지 않는다)
SHARE_EVENTS = [{"end": "2026-07-14", "filed": "2026-07-15", "shares": 728_865_500,
                 "src": "424B4 공모 후 유통주식 728,865,500주 · 신주 1,779만 주 7/14 납입(발행결과 자율공시 KIND 20260715000045)"},
                {"end": "2026-08-21", "filed": "2026-08-21", "shares": 728_866_596,
                 "src": "자기주식처분결과보고서(KIND 20260821000540) + 주식 소각 결정(20260819000340)"}]

FLOW = {"revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax"], "cogs": ["CostOfRevenue"],
        "opinc": ["OperatingIncomeLoss"],
        "pretax": ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"],
        "tax": ["IncomeTaxExpenseBenefit"], "ni": ["NetIncomeLoss"], "ni_total": ["ProfitLoss"]}
CF = {"ocf": ["NetCashProvidedByUsedInOperatingActivities"], "capex_ppe": ["PaymentsToAcquirePropertyPlantAndEquipment"],
      "capex_int": ["PaymentsToAcquireIntangibleAssets"], "da": ["DepreciationDepletionAndAmortization"],
      "div": ["PaymentsOfDividendsCommonStock"], "buyback": ["PaymentsForRepurchaseOfCommonStock"],
      "int_paid": ["InterestPaidNet"]}
BS = {"cash": ["CashAndCashEquivalentsAtCarryingValue"], "sti": ["ShortTermInvestments"],
      "ar": ["AccountsReceivableNetCurrent"], "inv": ["InventoryNet"], "assets": ["Assets"], "ca": ["AssetsCurrent"],
      "cl": ["LiabilitiesCurrent"], "liab": ["Liabilities"], "ap": ["AccountsPayableCurrent"],
      "st_debt": ["LongTermDebtCurrent", "DebtCurrent"], "lt_debt": ["LongTermDebtNoncurrent"],
      "lease_cur": ["OperatingLeaseLiabilityCurrent"], "lease_non": ["OperatingLeaseLiabilityNoncurrent"],
      "equity": ["StockholdersEquity"], "nci": ["MinorityInterest"], "lti": ["LongTermInvestments"],
      "equity_method": ["EquityMethodInvestments"]}
QEND = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}
QSTART = {1: "01-01", 2: "04-01", 3: "07-01", 4: "10-01"}
KIND2N = {"Q1": 1, "Q2": 2, "Q3": 3, "FY": 4}


def next_day(s):
    return (date.fromisoformat(s[:10]) + timedelta(days=1)).isoformat()


def build():
    man = json.load(open(MANIFEST))
    rep = {}
    for m in man:
        r = extract(os.path.join(REPORTS, m["file"]))
        if r["missing"]:
            raise SystemExit(f"{m['file']}: 항목 누락 {r['missing']}")
        # 접수번호 앞 8자리가 공시일이다(KIND 목록 시각은 정정·재게시 때 늦게 찍힌다 — 2023 1분기 5/15 접수가 5/24로 보였다, Fable)
        r["filed"], r["accn"] = next_day(m["acptno"][:4] + "-" + m["acptno"][4:6] + "-" + m["acptno"][6:8]), m["acptno"]
        rep[(int(r["end"][:4]), KIND2N[r["kind"]])] = r
    facts = {}

    def add(tag, unit, row):
        facts.setdefault(tag, {"units": {}})["units"].setdefault(unit, []).append(row)

    def meta(y, n, start):
        r = rep[(y, n)]
        form, fp = ("10-K", "FY") if n == 4 else ("10-Q", f"Q{n}")
        return {"start": start, "end": f"{y}-{QEND[n]}", "accn": r["accn"], "fy": y, "fp": fp, "form": form,
                "filed": r["filed"]}

    years = sorted({y for y, _ in rep})
    for y in years:
        have = [n for n in (1, 2, 3, 4) if (y, n) in rep]
        full = have == [1, 2, 3, 4] or (have and have == list(range(1, max(have) + 1)))
        if full:
            # ── 손익: 3개월 행(Q1~Q3, Q4 = 연간 − 3분기 누적), 누적 행(Q2·Q3), 연간 행 ──
            for key, tags in FLOW.items():
                for n in have:
                    r = rep[(y, n)]
                    if n < 4:
                        three, ytd = r["is3"][key] * MIL, r["isy"][key] * MIL
                    else:
                        three, ytd = (r["isy"][key] - rep[(y, 3)]["isy"][key]) * MIL, r["isy"][key] * MIL
                    for tg in tags:
                        add(tg, "USD", {**meta(y, n, f"{y}-{QSTART[n]}"), "val": three})
                        if n >= 2:
                            add(tg, "USD", {**meta(y, n, f"{y}-01-01"), "val": ytd})
            for key, tag in (("eps_d", "EarningsPerShareDiluted"), ("eps_b", "EarningsPerShareBasic")):
                for n in have:
                    r = rep[(y, n)]
                    three = r["is3"][key] if n < 4 else r["isy"][key] - rep[(y, 3)]["isy"][key]
                    add(tag, "USD/shares", {**meta(y, n, f"{y}-{QSTART[n]}"), "val": round(three / ADS_PER_SHARE, 4)})
                    if n >= 2:
                        add(tag, "USD/shares", {**meta(y, n, f"{y}-01-01"), "val": round(r["isy"][key] / ADS_PER_SHARE, 4)})
            # ── 현금흐름·감가상각·이자 지급: 누적 행만(US 10-Q처럼) ──
            for key, tags in CF.items():
                for n in have:
                    v = rep[(y, n)]["cfy"].get(key)
                    if v is None:
                        v = 0.0         # 배당금 지급 등 그 기간에 행이 없으면 0
                    for tg in tags:
                        add(tg, "USD", {**meta(y, n, f"{y}-01-01"), "val": v * MIL})
            # ── 이자 지급액 → InterestExpense: 3개월 행(누적의 차이) + 누적 행 ──
            # 이자보상배율은 분기 영업이익 ÷ 분기 이자비용이다. 누적 행만 두면 2분기 영업이익을 상반기
            # 누적 이자로 나눈다(Codex 지적, 123배 → 441배).
            prev = 0.0
            for n in have:
                ytd = (rep[(y, n)]["cfy"].get("int_paid") or 0.0) * MIL
                add("InterestExpense", "USD", {**meta(y, n, f"{y}-{QSTART[n]}"), "val": ytd - prev})
                if n >= 2:
                    add("InterestExpense", "USD", {**meta(y, n, f"{y}-01-01"), "val": ytd})
                prev = ytd
        # ── 재무상태표(원화 그대로), 주식 수(ADR 기준) ──
        for n in have:
            r = rep[(y, n)]
            base = {"end": f"{y}-{QEND[n]}", "accn": r["accn"], "fy": y, "fp": "FY" if n == 4 else f"Q{n}",
                    "form": "10-K" if n == 4 else "10-Q", "filed": r["filed"]}
            for key, tags in BS.items():
                for tg in tags:
                    add(tg, "USD", {**base, "val": r["bs"][key] * MIL})
            add("CommonStockSharesOutstanding", "shares", {**base, "val": r["shares"] * ADS_PER_SHARE})
    for ev in SHARE_EVENTS:
        add("CommonStockSharesOutstanding", "shares", {"end": ev["end"], "accn": "manual", "fy": int(ev["end"][:4]),
                                                        "fp": "Q3", "form": "10-Q", "filed": ev["filed"],
                                                        "val": ev["shares"] * ADS_PER_SHARE})
    shares = facts.pop("CommonStockSharesOutstanding")
    out = {"cik": int(CIK), "entityName": "SK hynix Inc. (v2 adapter)",
           "facts": {"us-gaap": {**facts, "CommonStockSharesOutstanding": shares},
                     "dei": {"EntityCommonStockSharesOutstanding": shares}},
           "_adapter": {"source": "SK hynix K-IFRS consolidated statements (KIND: quarterly/half-year reports, consolidated audit reports)",
                        "valuesCurrency": "KRW", "fx": "FRED DEXKOUS (Fed H.10)", "adsPerShare": ADS_PER_SHARE,
                        "shareEvents": SHARE_EVENTS, "reports": len(man), "built": date.today().isoformat()}}
    json.dump(out, open(OUT, "w"))
    print(f"저장: {OUT} — 보고서 {len(man)}건, 태그 {len(facts) + 1}개")
    return out


if __name__ == "__main__":
    build()
