#!/usr/bin/env python3
"""v2 시안: 배수의 5년 이력을 재구성해 백분위 기준선을 만든다.

왜 필요한가
-----------
카드의 5단계 평가 테이블은 배수마다 저/적정/고 세 기준선을 갖는데, 적정만
"자체 10년 중앙값"이라는 근거가 있고 저·고는 손으로 놓은 값이다. NVDA의 PER
저 기준선 15x는 5년 동안 한 번도 관측된 적이 없는 값이라(최저 26.5x) 점수를
중간으로 눌러버린다. 기준선 위치에 점수가 크게 흔들리므로, 70장을 한 줄로
세우면 기준선을 후하게 잡은 종목이 위로 간다.

그래서 기준선을 없애고 **그 종목 자신의 5년 배수 분포 안에서의 백분위**를
점수로 쓴다. 정의가 하나뿐이고, 잘리는 구간이 없고, 종목마다 눈금 폭이
달라지는 문제도 생기지 않는다.

미래 정보를 쓰지 않는다
-----------------------
각 거래일의 배수는 그날까지 **공시로 공개돼 있던** 재무제표만으로 계산한다.
SEC XBRL 항목의 `filed` 날짜를 그대로 쓰고, 그보다 나중에 제출된 수치는
그 날짜 이전 구간에 절대 반영하지 않는다.

분할 처리
---------
Yahoo 일봉은 분할이 소급 반영돼 있고 XBRL의 주식수는 당시 보고치라 서로
기준이 다르다. `fetch_eps_history.py`의 분할 표와 같은 규칙으로, 그 공시
이후에 일어난 분할 배수만큼 **주식수를 곱해** 오늘 기준으로 환산한다
(EPS는 같은 이유로 나눈다).

사용법
------
    EPS_HISTORY=scripts/NVDA_eps_history.json python3 v2/build_multiple_history.py NVDA
    EPS_HISTORY=scripts/NVDA_eps_history.json python3 v2/build_multiple_history.py NVDA --json out.json

EPS 이력이 없으면 PER만 빠진 채 계산된다. 만들려면:
    python3 scripts/fetch_eps_history.py NVDA --cik 0001045810 --out scripts/NVDA_eps_history.json
"""
import argparse
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import fetch_eps_history as feh  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fx  # noqa: E402  재무 통화가 달러가 아닌 종목(TSM)의 환율

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# 배수별로 필요한 XBRL 태그. 앞의 것부터 시도해 데이터가 있는 것을 쓴다.
FLOW_TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
                "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet"],
    "ocf": ["NetCashProvidedByUsedInOperatingActivities",
            "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment",
              "PaymentsToAcquireProductiveAssets"],
}
INSTANT_TAGS = {
    "equity": ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
    "shares": ["CommonStockSharesOutstanding", "EntityCommonStockSharesOutstanding"],
}

# EV/EBITDA
# ---------
# 기업가치의 구성은 친구에게 받은 기관용 모델(Canalyst 형식, BILL·JFrog·NYT)의
# Balance Sheet Summary 블록을 그대로 따른다.
#   Cash      = 현금성자산 + 단기투자
#   Debt      = 차입금 전부(단기·장기·신용공여·전환사채)
#   Net Debt  = Debt + 운용리스부채 - Cash      ← 리스를 부채로 본다
#   EV        = Net Debt + 시가총액 + 비지배지분 + 우선주 + 기타
# 같은 구성요소를 여러 태그가 나눠 담으므로 이쪽은 **합산**한다. 기간 항목처럼
# 중복을 걸러내면 안 된다(그러면 구성요소 하나만 남는다).
EV_COMPONENTS = {
    "cash": ["CashAndCashEquivalentsAtCarryingValue"],
    "sti": ["MarketableSecuritiesCurrent", "DebtSecuritiesCurrent", "ShortTermInvestments",
            "AvailableForSaleSecuritiesDebtSecuritiesCurrent"],
    "debt": ["LongTermDebtCurrent", "LongTermDebtNoncurrent", "ShortTermBorrowings",
             "CommercialPaper", "OtherShortTermBorrowings", "ConvertibleNotesPayableCurrent",
             "ConvertibleNotesPayableNoncurrent"],
    "lease": ["OperatingLeaseLiabilityCurrent", "OperatingLeaseLiabilityNoncurrent"],
    "nci": ["MinorityInterest"],
    # 전환우선주를 다른 태그로 내는 회사가 있다 — GOOGL 6.25% 의무전환 우선주 $18.0B
    # (2026, ConvertiblePreferredStock…). 이 태그를 안 보면 EV와 주당 내재가치에서 빠진다.
    "preferred": ["PreferredStockValue", "ConvertiblePreferredStockNonredeemableOrRedeemableIssuerOptionValue"],
}
# 감가상각은 회사마다 보고 구조가 다르다. NVDA는 합산 태그 하나로 내지만
# MSFT는 Depreciation과 AmortizationOfIntangibleAssets를 따로 낸다. 합산 태그가
# 있으면 그것을 쓰고(구성요소를 또 더하면 이중계상), 없을 때만 구성요소를 더한다.
DDA_COMBINED = ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization",
                "DepreciationAmortizationAndAccretionNet", "DepreciationAmortizationAndOther"]
DDA_PARTS = ["Depreciation", "AmortizationOfIntangibleAssets",
             "FinanceLeaseRightOfUseAssetAmortization"]
# 구성요소 목록을 종목별로 바꿔야 하는 회사(CIK). MRK: 무형자산 상각을 분기엔 현금흐름표 "Amortization"
# (AdjustmentForAmortization, 2026 상반기 $1,915M)으로만 내고 AmortizationOfIntangibleAssets는 10-K 연간뿐이라,
# 분기 EBITDA에서 상각이 빠져 EV/EBITDA가 43배로 부풀었다(Fable, 2026-09-30). 연간 태그는 빼야 두 번 세지 않는다.
DDA_PARTS_BY_CIK = {"0000310158": ["Depreciation", "AdjustmentForAmortization"]}
# 태그 의미가 도중에 바뀐 회사의 합산 감가상각(CIK). AMD의 OtherDepreciationAndAmortization(현금흐름표
# "Depreciation and amortization")은 FY2024 10-K(2025-02-05) 전까지 인수 무형자산 상각을 **포함한** 합계였고,
# 그 뒤로는 상각을 AmortizationOfIntangibleAssets 줄로 떼어 낸다(Fable, 2026-09-27). 분할 뒤 공시의 행에만
# 같은 (start, end, accn)의 상각을 더해 한 줄기 합산 시리즈로 만든다. Depreciation 태그는 10-K 연간(설비만)뿐이다.
# (처음엔 두 태그를 구성요소로 더했다가 2023~24년이 이중 계상되고 2024 Q4가 음수가 됐다.)
DDA_SPLIT_BY_CIK = {"0000002488": {"total": "OtherDepreciationAndAmortization", "add": "AmortizationOfIntangibleAssets",
                                   "split_from": "2025-02-05"}}


def split_era_dda(cik):
    cfg = DDA_SPLIT_BY_CIK[cik]
    add = {(r.get("start"), r["end"], r.get("accn")): r["val"] for r in concept(cik, cfg["add"])}
    out = []
    for r in concept(cik, cfg["total"]):
        if r.get("filed", "") >= cfg["split_from"]:
            k = (r.get("start"), r["end"], r.get("accn"))
            if k not in add:
                continue
            r = dict(r, val=r["val"] + add[k])
        out.append(r)
    return out

EBITDA_TAGS = {
    "opinc": ["OperatingIncomeLoss"],
    # NVDA는 2021-11 이전을 DepreciationAndAmortization으로만 보고했다. 이 태그를
    # 빼면 EV/EBITDA만 5년이 아니라 4년치가 된다(1016일 vs 1255일).
    "dda": ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization",
            "DepreciationAmortizationAndAccretionNet"],
}
# 본업 기준 PER에 쓰는 세율 = 최근 4분기 법인세 ÷ 세전이익 (build_dcf와 같은 정의)
CORE_TAX_TAGS = {
    "tax": ["IncomeTaxExpenseBenefit"],
    "pretax": ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
               "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
}
CORE_EARNINGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "core_earnings.json")


def core_tickers():
    """본업 이익으로 PER을 계산할 종목(v2/core_earnings.json)."""
    if not os.path.exists(CORE_EARNINGS):
        return {}
    return {k: v for k, v in json.load(open(CORE_EARNINGS)).items() if not k.startswith("_")}


TAX_ONEOFF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tax_oneoff.json")


def oneoff_in_ttm(ticker, ttm_end, field, asof=None):
    """결산일 ttm_end로 끝나는 최근 4분기에 든 일회성 법인세 항목(v2/tax_oneoff.json)의 합.

    META 2025 Q3 −$15.93B(비현금 세금)·2026 Q1 +$8.03B(환입)처럼 회사가 금액을 밝힌 것만
    넣는다(2026-09-25 사용자 결정). asof가 있으면 그때 공시된 항목만 센다.
    """
    if not ttm_end or not os.path.exists(TAX_ONEOFF):
        return 0.0
    end = date.fromisoformat(ttm_end)
    total = 0.0
    for it in json.load(open(TAX_ONEOFF)).get(ticker, []):
        lag = (end - date.fromisoformat(it["quarter_end"])).days
        if 0 <= lag < 330 and (asof is None or it["filed"] <= asof):
            total += it[field]
    return total


# 두 시리즈를 짝지을 때 허용하는 뒤처짐. 한 분기 늦은 보고(약 91일)는 받고,
# 두 분기 이상 비면 버린다.
MAX_PAIR_LAG_DAYS = 200


CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".sec_cache")


def _facts(cik):
    """회사의 XBRL 전체(companyfacts)를 **한 번만** 받아 캐시한다.

    태그마다 companyconcept를 부르면 한 종목에 15~20번을 호출하게 되고, 70장을
    돌리면 SEC가 요청 제한을 건다(검증 중 실제로 429에 막혔다). companyfacts는
    같은 내용을 한 번에 주므로 호출이 1/15로 줄고, 캐시가 있으면 0이 된다.
    새로 받으려면 이 디렉터리의 파일을 지운다.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{cik}_facts.json")
    if os.path.exists(path):
        try:
            return _overlay(cik, json.load(open(path)))
        except Exception:
            pass
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    try:
        data = feh.curl_json(url)
    except Exception:
        return {}
    if "facts" in data:
        json.dump(data, open(path, "w"))
    return _overlay(cik, data)


def _overlay(cik, data):
    """companyfacts에 없는 기간을 `.sec_cache/overlay/{cik}.json`으로 채운다.

    회사가 한동안 자체 태그로만 낸 항목(AVGO 무형자산 상각 2020~2025, `adapters/avgo_amort.py`)은
    companyfacts에 빠진다. 같은 (start, end, 공시일)이 이미 있으면 SEC 값을 그대로 둔다. 공시일까지
    보는 이유는 AVGO가 2026년 공시에서 2025년 분기를 비교 수치로 표준 태그에 다시 실었기 때문이다 —
    기간만으로 겹침을 보면 제때(2025) 공시된 보충 행이 빠지고, 시점 규칙이 그 분기를 1년 늦게
    알려진 값으로 보고 버린다.
    """
    op = os.path.join(CACHE_DIR, "overlay", f"{cik}.json")
    if not os.path.exists(op) or "facts" not in data:
        return data
    for tax, tags in json.load(open(op)).items():
        for tag, rows in tags.items():
            units = data["facts"].setdefault(tax, {}).setdefault(tag, {"units": {}})["units"]
            # 행마다 단위를 적을 수 있다(주식 수는 "shares" — META 표지 합산, `adapters/cover_shares.py`)
            for unit in sorted({r.get("unit", "USD") for r in rows}):
                have = units.setdefault(unit, [])
                keys = {(r.get("start"), r["end"], r.get("filed")) for r in have}
                have.extend(r for r in rows if r.get("unit", "USD") == unit
                            and (r.get("start"), r["end"], r["filed"]) not in keys)
    return data


def concept(cik, tag, taxonomy="us-gaap"):
    """companyfacts 캐시에서 한 태그의 항목들을 꺼낸다."""
    facts = _facts(cik).get("facts", {}).get(taxonomy, {})
    units = facts.get(tag, {}).get("units", {})
    for key in ("USD", "shares", "USD/shares"):
        if units.get(key):
            return units[key]
    return []


# 회사 전용 태그 보강(CIK별). 표준 태그 대신 같은 항목을 다른 표준 태그로만 내는 회사.
# LLY: 설비투자 = PaymentsToAcquireOtherPropertyPlantAndEquipment(10-Q "Purchases of property and equipment"),
#      인수 = OtherPaymentsToAcquireBusinesses("Cash paid for acquisitions, net of cash acquired", 2022년 이후).
EXTRA_TAGS = {
    # VZ: 설비투자가 2019-09 뒤 PaymentsToAcquireOtherProductiveAssets(분기 약 $4B, "Capital expenditures (including capitalized
    # software)")로 옮겨 가 기본 목록이 2019년 값에 멈췄다 — PCR 계산 불가(2026-10-01).
    "0000732712": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsToAcquireOtherProductiveAssets"]},
    # WELL(리츠): 설비투자 표준 태그가 없다 — 기존 자산 개량 지출(PaymentsForCapitalImprovements, 상반기 2026 $589M)을 쓴다. 부동산 인수
    # ($6.3B)·개발 공사($167M)는 넣지 않는다(리츠 평가법 미정, 안건). 순이익은 보통주 귀속 태그만 낸다(2026-10-02).
    # NEE: 손익계산서 총매출은 RegulatedAndUnregulatedOperatingRevenue(Q2 2026 $7,534M)다. RevenueFromContractWithCustomerIncludingAssessedTax는
    # 주석의 고객 계약 매출(0.1B 단위 반올림, $6.7B)이라 뺀다(EXCLUDE_TAGS). 설비투자·이자비용은 회사 고유 태그라 표준 데이터에 없다(2026-10-02).
    "0000753308": {"Revenues": ["RegulatedAndUnregulatedOperatingRevenue"]},
    # GLW: 설비투자("Capital expenditures", 상반기 2026 $754M)를 2020년부터 PaymentsForCapitalImprovements로만 낸다 — 기본 목록은
    # 2020-09에 멈춘 PaymentsToAcquireProductiveAssets를 잡아 PCR 계산 불가였다(2026-10-02).
    "0000024741": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsForCapitalImprovements"]},
    "0000766704": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsForCapitalImprovements"],
                   "NetIncomeLoss": ["NetIncomeLossAvailableToCommonStockholdersBasic"]},
    # COST: 세전이익을 FY2023부터 IncomeLossAttributableToParent로 낸다(FY2023 연간 8,487 = 손익계산서 세전이익,
    # Q3 FY26 2,938 = 10-Q "INCOME BEFORE INCOME TAXES"). 표준 태그는 10-Q 기준 2024-05에서 끊겨 DCF 세율이
    # FY2024 연간 세전으로 계산됐다(29.9% → 24.8%, Fable 2026-09-29).
    "0000909832": {"IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest":
                   ["IncomeLossAttributableToParent"]},
    "0000059478": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsToAcquireOtherPropertyPlantAndEquipment"],
                   "PaymentsToAcquireBusinessesNetOfCashAcquired": ["OtherPaymentsToAcquireBusinesses"]},
}
# 영업이익 줄이 없는 손익계산서(LLY). 영업이익 = 세전이익 − 영업외손익("Other income (expense)")으로 합성한다.
# LLY Q2 2026: 매출 22,974 − 매출원가 3,268 − R&D 3,819 − 판관비 3,430 − 인수 IPR&D 2,776 − 손상·구조조정 703
# = 8,978 = 세전 9,247 − 영업외 269(10-Q 대조, 2026-09-27). 같은 공시(accn)·같은 기간끼리만 뺀다.
# JNJ도 영업이익 줄이 없다(OperatingIncomeLoss는 2015년까지). 영업외 = 이자수익 − 이자비용(2024년부터
# InterestExpenseNonoperating) + "Other (income) expense, net"(탈크 소송·인수 비용·연금·증권 손익 포함 — 2025 Q1 탈크
# 충당금 환입 $7.2B가 여기 있다). Q2 2026: 세전 6,747 − (219 − 281 − 331) = 7,140 = 매출 25,310 − 매출원가 8,051
# − 판관비 6,432 − R&D 3,653 − 구조조정 34(10-Q 대조, 2026-09-28). 구조조정·IPR&D 손상은 영업으로 둔다.
DERIVED_OPINC = {# TJX: 손익계산서에 영업이익 줄이 없다. 영업이익 = 세전이익 − "Interest (income) expense, net"(InterestRevenueExpenseNet, 순이자수익이면 양수).
                 # Q2 FY27: 2,018 − 31 = 1,987 = 매출 15,180 − 원가 10,108 − 판관비 3,085(10-Q 대조, 2026-10-02).
                 "0000109198": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["InterestRevenueExpenseNet"], 1)]),
                 # BX: 영업이익 줄이 없다. 영업이익 = 세전이익 − "Total Other Income"(펀드 투자 순이익) + 이자비용(총비용 안에 있다 — Codex).
                 # Q2 2026: 2,808 − 140 + 145 = 2,813 = 총매출 5,044 − (총비용 2,376 − 이자 145)(10-Q 대조, 2026-10-02).
                 "0001393818": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["OtherNonoperatingIncomeExpense"], 1), (["InterestExpense"], -1)]),
                 # BMY: MRK와 같은 구조(영업이익 줄 없음). 영업이익 = 세전이익 − "Other (income)/expense, net"(이자비용·투자수익·구조조정·지분 평가 포함,
                 # 수익이면 양수). Q2 2026: 4,086 − 61 = 4,025 = 매출 12,973 − (총비용 8,887 + 61)(10-Q 대조, 2026-10-02).
                 "0000014272": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                "OtherNonoperatingIncomeExpense"),
                 # NEM: LLY와 같은 구조(영업이익 줄 없음). 영업이익 = 세전이익 − 영업외손익 합계(NonoperatingIncomeExpense).
                 # Q2 2026: 2,999 − (−97) = 3,096 = 매출 6,118 − 총비용 3,022(10-Q 대조, 2026-10-02).
                 "0001164727": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                "NonoperatingIncomeExpense"),
                 "0000059478": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                "NonoperatingIncomeExpense"),
                 "0000200406": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["InvestmentIncomeInterest"], 1), (["InterestExpenseNonoperating", "InterestExpense"], -1),
                                 (["OtherNonoperatingIncomeExpense"], 1)]),
                 # XOM: 손익계산서에 영업이익 줄이 없다. 영업이익 = 세전이익 + 이자비용(2026-09-29 사용자 결정) — 지분법 이익
                 # (카타르 LNG 등 합작 생산)·기타수익은 영업으로 본다(지분법 투자는 비영업 자산에 더하지 않는다). Q2 2026:
                 # 세전 19,424 + 이자 227 = 19,651(10-Q 대조).
                 "0000034088": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["InterestExpense"], -1)]),
                 # CVX: XOM과 같은 구조(영업이익 줄 없음) → 같은 규칙. 영업이익 = 세전이익 + 이자비용("Interest and debt
                 # expense", InterestExpenseDebt). 지분법 이익(TCO 등)·기타수익은 영업. Q2 2026: 세전 16,684 + 352 = 17,036.
                 "0000093410": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
                                [(["InterestExpenseDebt"], -1)]),
                 # MRK: 손익계산서에 영업이익 줄이 없다(LLY·JNJ와 같은 구조). 영업이익 = 세전이익 − "Other (income) expense, net"
                 # (OtherNonoperatingIncomeExpense — 이자비용 포함, 비용이면 음수). Q2 2026: −683 − (−99) = −584(10-Q 대조).
                 # 인수 IPR&D(1분기 $8.54B·2분기 $5.27B)는 R&D 안이라 영업이익에 남는다(ABBV 선례, 안건 B2).
                 "0000310158": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                "OtherNonoperatingIncomeExpense"),
                 # GE: 손익계산서에 영업이익 줄이 없다. 영업이익 = 세전이익 − 기타수익("Other income (loss)", 지분 매각·평가 손익)
                 # + 이자·기타 금융비용 + 영업외 연금비용(수익이면 음수). 뒤 두 줄은 회사 고유 태그라 인라인 XBRL 어댑터
                 # (adapters/ge_income_items.py)가 overlay에 싣는다. 보험(런오프) 수익·비용은 영업으로 둔다. Q2 2026: 2,801 − 313
                 # + 215 − 177 = 2,526 = 매출 13,349 − 영업비용 10,823(10-Q 대조).
                 "0000040545": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["NonoperatingIncomeExpense"], 1), (["GeInterestAndOtherFinancialCharges"], -1),
                                 (["GeBenefitCostIncomeNonoperating"], -1)]),
                 # KLAC: 손익계산서에 영업이익 줄이 없다(OperatingIncomeLoss는 2015년까지 — 그 값이 계속 쓰였다). 영업이익 = 세전이익
                 # + 이자비용 − "Other expense (income), net"(기타수익, 양수). Q4 FY26: 1,549.4 + 73.3 − 68.7 = 1,553.9 = 매출 3,657.6
                 # − 매출원가 1,413.1 − R&D 399.0 − 판관비 291.5(실적 보도자료 대조, 2026-10-01).
                 # DE: 손익계산서에 영업이익 줄이 없다(금융 부문 이자·대손이 비용 안). CAT 결정(금융 부문 빚 제외·그 이자는 영업)과 같게
                 # 영업이익 = 세전이익("Income of Consolidated Group before Income Taxes") — 장비 부문 대외 이자(분기 약 $50M,
                 # 연결 이자 $710M − 금융 부문 $661M, Q3 FY26)까지 영업 비용에 남아 영업이익이 약 3% 낮다(태그가 없어 더하지 못함, 2026-10-01).
                 # DIS: OperatingIncomeLoss 태그가 회사 비GAAP "부문 영업이익 합계"(Q3 FY26 $5,555M — 본사 비용·인수 무형자산 상각·
                 # 구조조정 제외)다. GAAP 손익계산서로 영업이익 = 세전이익 − 순이자(InterestIncomeExpenseNonoperatingNet, 비용이면 음수) − 기타 영업외손익.
                 # 지분법 이익·구조조정·손상은 영업에 둔다(XOM·ABBV 선례). Q3 FY26: 3,645 + 298 = 3,943 = 매출 25,248 − 비용 20,488
                 # − 구조조정·손상 900 + 지분법 83(10-Q 대조, 2026-10-01).
                 "0001744489": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["InterestIncomeExpenseNonoperatingNet", "InterestIncomeExpenseNet"], 1),
                                 # "Other income (expense), net"(DraftKings 평가손 등, 분기에 따라 없음 → 선택 항목). FY2022 −$667M,
                                 # Q3 FY24 −$65M을 영업이익에서 뺀다(Codex, 2026-10-01).
                                 (["OtherNonoperatingIncomeExpense", "NonoperatingIncomeExpense"], 1, True)]),
                 "0000315189": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", []),
                 "0000319201": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["InterestExpenseNonoperating", "InterestExpense"], -1), (["OtherNonoperatingIncomeExpense"], 1),
                                 # 채무 상환 손실(손익계산서 별도 줄, 손실은 음수) — Q1 FY23 $13.3M(Codex). 없는 분기는 0.
                                 (["GainsLossesOnExtinguishmentOfDebt"], 1, True)]),
                 # IBM: 손익계산서에 영업이익 줄이 없고 "지식재산·주문 개발 수익"과 "기타 (수익)·비용"은 회사 고유 태그라 SEC 요약 데이터에
                 # 없다. 영업이익 = 매출총이익 − 판관비 − R&D(표준 태그만). 지식재산 수익(Q2 2026 $166M)은 빠져 조금 보수적이다.
                 # Q2 2026: 9,907 − 4,981 − 2,311 = 2,615(10-Q 대조, 2026-10-01).
                 "0000051143": ("GrossProfit", [(["SellingGeneralAndAdministrativeExpense"], 1), (["ResearchAndDevelopmentExpense"], 1)]),
                 # ETN: 손익계산서에 영업이익 줄이 없다(OperatingIncomeLoss 태그 없음). 영업이익 = 세전이익 + 순이자비용("Interest expense - net")
                 # − "Other expense (income) - net"(OtherNonoperatingIncomeExpense, 비용이면 음수). 순이자비용 태그가 공시마다 바뀌었다 —
                 # 2024-09부터 InterestExpenseNonoperating(양수), 일부 재작성 공시는 InterestExpenseOperating(양수), 그 전은
                 # InterestIncomeExpenseNet(비용이면 음수, 부호를 뒤집는다). 같은 공시에 둘이 있으면 앞 태그를 쓴다.
                 # Q2 2026: 1,144 + 201 + 47 = 1,392 = 매출 8,531 − 매출원가 5,676 − 판관비 1,236 − R&D 227(10-Q 대조, 2026-10-01).
                 "0001551182": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["InterestExpenseNonoperating", "InterestExpenseOperating", ("InterestIncomeExpenseNet", -1)], -1),
                                 # 기타 영업외손익도 공시마다 태그가 다르다 — 수익인 분기는 OtherNonoperatingIncome(양수, Q1 2026 $41M), 비용만이면
                                 # OtherNonoperatingExpense(양수, 부호를 뒤집는다). 빠뜨리면 그 분기가 0으로 잡혔다(Codex: Q1 2026 1,213 → 1,172).
                                 (["OtherNonoperatingIncomeExpense", "OtherNonoperatingIncome", ("OtherNonoperatingExpense", -1)], 1, True),
                                 # 사업 매각 이익(손익계산서 별도 줄 "Gain on sale of business") — Q3 2021 유압 사업 $617M, Q1 2022 $24M.
                                 # 없는 분기는 0. 빼지 않으면 Q3 2021 영업이익률이 24.7%로 튄다(다른 분기 12~14%).
                                 (["GainLossOnSaleOfBusiness"], 1, True)]),
                 # WELL(리츠): 손익계산서에 영업이익 줄이 없고 비용 합계(CostsAndExpenses)에 이자비용이 들어 있다. 영업이익 = 총매출 − 비용 합계
                 # + 이자비용(2022-12부터 InterestExpenseBorrowings, 그 전 InterestExpenseDebt). 비용 합계 밖인 부동산 매각 이익은 영업에서 빠지고, 자산 손상은 비용 합계 안이라 영업에 남는다.
                 # Q2 2026: 3,544.6 − 3,224.2 + 181.9 = 502.3(10-Q 대조, 2026-10-02).
                 "0000766704": ("Revenues", [(["CostsAndExpenses"], 1), (["InterestExpenseBorrowings", "InterestExpenseDebt"], -1)]),
                 # PFE: 손익계산서에 영업이익 줄이 없다(MRK·LLY와 같은 구조). 영업이익 = 세전이익 − "Other (income)/deductions—net"
                 # (OtherNonoperatingIncomeExpense, 비용이면 음수 — 이자비용·무형자산 손상·지분 평가손익 포함, MRK 선례대로 영업 밖).
                 # Q2 2026: −653 − (−3,716) = 3,063(10-Q 대조, 2026-10-02).
                 "0000078003": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                "OtherNonoperatingIncomeExpense"),
                 # COP: XOM·CVX와 같은 구조(영업이익 줄 없음) → 같은 규칙. 영업이익 = 세전이익 + 이자비용("Interest and debt expense",
                 # InterestAndDebtExpense). 지분법 이익·기타 수익은 영업. Q2 2026: 6,082 + 182 = 6,264(10-Q 대조, 2026-10-02).
                 "0001163165": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["InterestAndDebtExpense"], -1)])}


def _derived_opinc(cik, taxonomy):
    """영업이익 = 세전이익 − 영업외 손익. 영업외는 태그 하나(LLY) 또는 [(대체 태그들, 부호), …](JNJ)이고,
    같은 (start, end, accn)에 모든 항목이 있을 때만 만든다."""
    pre_tag, non_spec = DERIVED_OPINC[cik]
    items = [([non_spec], 1)] if isinstance(non_spec, str) else non_spec
    maps = []
    for it in items:
        tags, sign = it[0], it[1]
        optional = len(it) > 2 and it[2]        # 선택 항목: 그 공시에 없으면 0(KLAC 채무 상환 손익 — 일부 분기만)
        m = {}
        for t in tags:                          # 앞 태그 우선(이름이 바뀐 태그는 뒤에)
            t, mult = t if isinstance(t, tuple) else (t, 1)   # (태그, 배수): 같은 줄을 부호가 반대인 태그로 낸 공시(ETN 이자)
            for r in concept(cik, t, taxonomy):
                m.setdefault((r.get("start"), r["end"], r.get("accn")), mult * r["val"])
        maps.append((m, sign, optional))
    out = []
    for r in concept(cik, pre_tag, taxonomy):
        k = (r.get("start"), r["end"], r.get("accn"))
        if all(k in m or opt for m, _, opt in maps):
            out.append({**r, "val": r["val"] - sum(sign * m.get(k, 0) for m, sign, _ in maps)})
    return out


# 종목별로 후보에서 빼는 태그(CIK). MA는 2018~2022년 RevenueFromContractWithCustomerExcludingAssessedTax에
# 리베이트·인센티브 차감 전 **총매출**(2022 Q3 $9.17B)을, Revenues에 순매출($5.76B)을 실었다. 합치면 앞 태그가
# 이겨 2021~2022 매출이 부풀고 2022 Q4가 −$3.7B가 됐다(5년 성장 4.9% — 실제 순매출 기준 약 14%, 2026-09-29).
# GE: RevenueFromContractWithCustomerExcludingAssessedTax는 보험 매출을 뺀 값이라(2023 Q2 $7,907M 대 총매출 $8,755M) 총매출
# Revenues와 섞이면 분기마다 기준이 달라진다(Codex, 2026-09-30). 손익계산서 "Total revenue"인 Revenues만 쓴다.
EXCLUDE_TAGS = {"0001141391": ("RevenueFromContractWithCustomerExcludingAssessedTax",),
                "0000040545": ("RevenueFromContractWithCustomerExcludingAssessedTax",),
                # AMGN: DepreciationAndAmortization(분기 약 $220M)이 현금흐름표 "Depreciation, amortization and other"
                # (DepreciationDepletionAndAmortization, 분기 약 $1.1B)와 같은 기간에 함께 있어 먼저 공시된 작은 값이 섞였다 — EBITDA가 낮아
                # EV/EBITDA가 높게 나왔다(Fable, 2026-10-01).
                "0000318154": ("DepreciationAndAmortization",),
                # MCD: DepreciationDepletionAndAmortization(분기 $111M)는 현금흐름표 D&A(DepreciationAndAmortization, 분기 $565M)의 일부라
                # 앞 태그가 이겨 EBITDA·DCF 감가상각이 낮았다(최근 4분기 $0.47B 대 약 $2.2B, 2026-10-02).
                "0000063908": ("DepreciationDepletionAndAmortization",),
                # WELL: RevenueFromContractWithCustomerExcludingAssessedTax는 시니어 주택 운영 매출만(Q2 2026 $2,985M)이고 임대 수익·이자
                # 수익을 뺀 값이다 — 손익계산서 총매출 Revenues($3,545M)만 쓴다(2026-10-02).
                "0000766704": ("RevenueFromContractWithCustomerExcludingAssessedTax",),
                "0000753308": ("RevenueFromContractWithCustomerIncludingAssessedTax",)}


# PFE: 2024년 10-K부터 RevenueFromContractWithCustomerExcludingAssessedTax를 제품 매출만(FY2023 $50.9B)으로 다시 정의했다 —
# 총매출 Revenues(FY2023 $58.5B)와 같은 날 공시돼 앞 태그가 이겨 2023년 4분기가 $6.7B(실제 $14.2B)로 나왔다. 2021년 분기는
# Revenues가 없어 옛 태그를 쓴다(그때는 총매출과 같은 값, 2026-10-02).
PREFER_TAGS = {"0000078003": ("Revenues",),
               # COP: 손익계산서 "Sales and other operating revenues"는 Revenues(Q2 2026 $19,161M)이고 RevenueFromContract…는 그중 고객 계약분
               # ($18,088M, 파생 계약 매출 제외)이다(10-Q 매출 주석, 2026-10-02).
               "0001163165": ("Revenues",)}


def pick_tag(cik, names, taxonomy="us-gaap"):
    """후보 태그를 **전부 합친다**.

    회사는 같은 항목을 도중에 다른 태그로 옮긴다. NVDA는 매출을
    RevenueFromContractWithCustomerExcludingAssessedTax(2020년까지) →
    Revenues로, 설비투자를 PaymentsToAcquirePropertyPlantAndEquipment(2020년까지)
    → PaymentsToAcquireProductiveAssets로 옮겼다. 첫 번째로 값이 있는 태그만
    쓰면 시리즈가 2020년에 멈춘 채 조용히 낡은 값을 계속 내놓는다
    (그 상태로 PSR이 17.8x 대신 490x로 나왔다).

    같은 기간을 두 태그가 함께 보고하면 먼저 제출된 쪽을 쓴다
    (dedup_earliest_filed와 같은 규칙).
    """
    extra = EXTRA_TAGS.get(cik, {})
    names = list(names) + [x for n in names for x in extra.get(n, []) if x not in names]
    names = [n for n in names if n not in EXCLUDE_TAGS.get(cik, ())]
    # 같은 기간·같은 공시일이면 앞 태그가 이긴다 — 종목별로 앞세울 태그(PREFER_TAGS)를 맨 앞으로.
    names = [n for n in PREFER_TAGS.get(cik, ()) if n in names] + [n for n in names if n not in PREFER_TAGS.get(cik, ())]
    merged, used = [], []
    for name in names:
        rows = concept(cik, name, taxonomy)
        if rows and name == "NetCashProvidedByUsedInOperatingActivities":
            # 총액에는 중단영업 현금이 섞인다. 같은 (start, end, accn)에 중단영업 영업현금흐름이 있으면 뺀다 —
            # AMD 2025년 ZT Systems 제조 부문(분기 $0.3~0.5B, TTM 약 7%, Fable 2026-09-27).
            disc = {(r.get("start"), r["end"], r.get("accn")): r["val"]
                    for r in concept(cik, "CashProvidedByUsedInOperatingActivitiesDiscontinuedOperations", taxonomy)}
            if disc:
                rows = [dict(r, val=r["val"] - disc[(r.get("start"), r["end"], r.get("accn"))])
                        if (r.get("start"), r["end"], r.get("accn")) in disc else r for r in rows]
        if rows:
            used.append(f"{name}({len(rows)})")
            merged.extend(rows)
    # 합성 대상 회사는 영업이익 태그가 옛날에만 있어도(JNJ는 2015년까지) 합성값만 쓴다
    if "OperatingIncomeLoss" in names and cik in DERIVED_OPINC and taxonomy == "us-gaap":
        merged = _derived_opinc(cik, taxonomy)
        if merged:
            used.append(f"세전−영업외(합성 {len(merged)})")
    return ("+".join(used) if used else None), merged


# 4분기가 16주(나머지 12주)인 52·53주 회계 종목. quarterly_flow가 4분기를 연간에서 뺄 때 3분기 끝을 112일 전까지 찾는다.
LONG_Q4_TICKERS = {"COST", "PEP"}   # PEP: 12·12·12·16주(2026-10-01)


def quarterly_flow(entries, ticker):
    """기간 항목(매출·영업현금흐름·설비투자)을 분기 단위로 환원한다.

    XBRL은 분기(약 90일)와 연간(약 365일)을 섞어 담고 있고, 4분기는 따로
    제출되지 않는 경우가 많아 연간에서 앞 세 분기를 빼서 만든다.
    """
    rows = [e for e in entries if "start" in e and "end" in e and "filed" in e]
    rows = feh.dedup_for(rows, ticker)   # 분사 재작성 종목(GE)은 나중 공시 값
    # 약 90일 항목인데 값이 같은 결산일의 연간 값과 똑같고 9개월 누계가 있으면 태깅 오류다 — ORCL FY2021·FY2022 10-K가 연간 매출
    # $40,479M·$42,440M을 3/1~5/31 기간으로도 태깅해 4분기 자리에 연간 값이 들어갔다(2026-10-01). 이런 항목은 버리고
    # 4분기는 아래에서 연간 − 1~3분기로 만든다.
    # 다만 4분기에 처음 생긴 항목(예: 4분기 인수)은 분기 = 연간이 정상이라, 같은 회계연도 9개월 누계가 0보다 클 때만
    # 모순(앞 세 분기 합이 0이 아님)으로 보고 버린다(Codex 2026-10-01).
    _ann = {e["end"]: e for e in rows if feh.days_between(e) > 350}
    def _bad_q(e):
        a = _ann.get(e["end"])
        if not a or a["val"] != e["val"]:
            return False
        return any(r["start"] == a["start"] and r["val"] > 0 and 250 <= feh.days_between(r) <= 290 for r in rows)
    q = {e["end"]: e for e in rows if 80 <= feh.days_between(e) <= 100 and not _bad_q(e)}

    # 현금흐름표는 분기가 아니라 회계연도 누계로 보고된다(2분기 10-Q에 6개월
    # 누계가 실린다). 그래서 같은 시작일을 공유하는 누계들을 끝나는 날짜 순으로
    # 세워 앞의 것을 빼면 그 분기 값이 나온다. 이 처리를 빼면 최근 분기가
    # 통째로 사라져 TTM이 한 분기 낡은 채로 계산된다(PCR이 42.5x 대신 58x).
    # 누계끼리만 묶으면 짝이 안 맞는다. 같은 회계연도 시작일을 공유하는 항목을
    # 길이와 무관하게 전부 모아야 3개월 → 6개월 → 9개월로 이어지는 사다리가 생긴다.
    by_start = {}
    for e in rows:
        by_start.setdefault(e["start"], []).append(e)
    for start, group in by_start.items():
        group.sort(key=lambda e: e["end"])
        for prev, cur in zip(group, group[1:]):
            gap = (date.fromisoformat(cur["end"]) - date.fromisoformat(prev["end"])).days
            if 80 <= gap <= 100 and cur["end"] not in q:
                q[cur["end"]] = {
                    "end": cur["end"],
                    "val": cur["val"] - prev["val"],
                    "filed": cur["filed"],
                    "start": prev["end"],
                }

    ann = [e for e in rows if feh.days_between(e) > 350]
    for a in ann:
        end = date.fromisoformat(a["end"])
        parts, cur = [], end
        ok = True
        for i in range(3):  # 직전 세 분기를 거슬러 찾는다
            prev = None
            # 4분기가 16주인 회계(COST 12·12·12·16주)는 연간 결산일과 3분기 끝이 112일(53주 해는 119일) 떨어진다.
            # 80~100일만 찾으면 4분기가 통째로 빠져 TTM이 하나도 안 만들어졌다(2026-09-29).
            hi = 120 if (i == 0 and ticker in LONG_Q4_TICKERS) else 100
            for e in q.values():
                d = (cur - date.fromisoformat(e["end"])).days
                if 80 <= d <= hi:
                    prev = e
                    break
            if prev is None:
                ok = False
                break
            parts.append(prev)
            cur = date.fromisoformat(prev["end"])
        if ok and a["end"] not in q:
            nine = [e for e in rows if e["start"] == a["start"] and e["end"] == parts[0]["end"]
                    and 260 <= feh.days_between(e) <= 285] if ticker in feh.RESTATED_LATEST else []
            q[a["end"]] = {
                "end": a["end"],
                "val": a["val"] - (nine[0]["val"] if nine else sum(p["val"] for p in parts)),   # 재작성 종목은 연간 − 9개월 누계
                "filed": a["filed"],
                "start": a["start"],
            }
    return sorted(q.values(), key=lambda e: e["end"])


def ttm_series(quarters, max_span_days=310):
    """분기 값 네 개를 더해 TTM을 만들고, 그 값이 공개된 날짜를 함께 남긴다.

    분기가 빠져 있으면 "네 개"가 1년이 아니라 2년에 걸칠 수 있다. NVDA의
    설비투자가 그랬다 — 표준 태그에 공백이 있어 546일짜리 TTM이 만들어졌고,
    그 앞에서는 27개월 동안 같은 값(1,176M)이 그대로 쓰였다. 창이 1년을 크게
    벗어나면 버린다.

    창은 **첫 분기와 마지막 분기의 결산일 사이**로 잰다. 붙어 있는 4분기는
    그 간격이 3분기, 즉 약 273일이다(분기 길이 84~98일 × 3 = 252~294일).
    문턱이 400일이던 동안에는 한 분기가 통째로 빠져 간격이 약 365일이 돼도
    그대로 통과했다(2026-09-22 Codex 발견 — NVDA capex의 2021-08-01 창이
    2020-07-26·2020-10-25·2021-05-02·2021-08-01로 만들어져 2021년 PCR 이력에
    분기 하나가 빠진 분모가 들어갔다). 310일이면 정상 창은 다 통과하고
    한 분기 누락은 걸린다.

    분기의 `start`로 재면 더 직접적일 것 같지만 그럴 수 없다. 연간에서 앞
    세 분기를 빼 만든 파생 분기는 `start`가 **연간 기간의 시작일**이라 1년
    길이로 잡힌다(그렇게 재면 정상 창까지 30개가 버려졌다).
    """
    out, dropped = [], 0
    for i in range(3, len(quarters)):
        window = quarters[i - 3:i + 1]
        span = (date.fromisoformat(window[-1]["end"]) - date.fromisoformat(window[0]["end"])).days
        if span > max_span_days:
            dropped += 1
            continue
        out.append({
            "end": window[-1]["end"],
            "val": sum(w["val"] for w in window),
            "available": max(w["filed"] for w in window),
        })
    if dropped:
        print(f"    ⚠ 1년을 넘는 TTM 창 {dropped}개 버림 (분기 공백)")
    return sorted(out, key=lambda e: e["available"])


SHARE_ADJUST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "share_adjust.json")


def share_adjustments(ticker):
    if not os.path.exists(SHARE_ADJUST):
        return []
    return json.load(open(SHARE_ADJUST)).get(ticker, [])


def instant_series(entries, ticker, is_share_count):
    rows = [e for e in entries if "end" in e and "filed" in e and "start" not in e]
    rows = feh.dedup_earliest_filed_instant(rows) if hasattr(feh, "dedup_earliest_filed_instant") else rows
    best = {}
    for e in rows:
        key = e["end"]
        if key not in best or e["filed"] < best[key]["filed"]:
            best[key] = e
    # 주식 수를 정정 공시(10-Q/A·10-K/A)로 고친 경우 정정 값을 **정정 공시일부터** 따로 넣는다. 표지 주식 수 오타다 —
    # SNDK 첫 10-Q(2025-03-07) 114,863,251주를 10-Q/A(2025-03-17)에서 144,863,251주로 고쳤는데, 처음 값이 다음 10-Q까지
    # 쓰여 2025-03~05 배수가 21% 낮게 나왔다(2026-10-01). 처음 공시일로 당기면 미래 정보가 섞인다(Codex) — 그사이는 처음 값.
    amended = []
    if is_share_count:
        # 같은 기간의 정정은 공시 순서대로 바로 앞 값과 비교한다 — 두 번째 정정이 처음 값으로 되돌려도 남는다(Codex 2차).
        last = {k: v["val"] for k, v in best.items()}
        for e in sorted(rows, key=lambda r: r["filed"]):
            b0 = best[e["end"]]
            if str(e.get("form", "")).endswith("/A") and e["filed"] > b0["filed"] and e["val"] != last[e["end"]] \
                    and not any(x["end"] > e["end"] and x["filed"] <= e["filed"] for x in best.values()):
                amended.append(e); last[e["end"]] = e["val"]
    out = []
    # 손 목록(KNOWN_SPLITS)이 없으면 Yahoo 분할 기록으로 보정한다(v2/splits.py, 2026-09-25).
    # 전에는 목록에 없는 종목의 분할 전 주식 수가 그대로 들어가 주당 가치가 부풀었다(BKNG·KLAC·CRWD).
    import splits as _splits
    splits = _splits.for_ticker(ticker)
    adjust = share_adjustments(ticker) if is_share_count else []
    for e in list(best.values()) + amended:
        val = e["val"]
        if is_share_count and splits:
            # 이 공시 이후에 일어난 분할만큼 주식수를 오늘 기준으로 늘린다
            val = val * feh.split_ratio(e["filed"], splits)
        # 획득 전 성과 조건부 제한주는 뺀다(v2/share_adjust.json, TSLA 423.7M주)
        val -= sum(a["shares"] for a in adjust
                   if e["end"] >= a["from"] and (a.get("until") is None or e["end"] < a["until"]))
        out.append({"end": e["end"], "val": val, "available": e["filed"]})
    return sorted(out, key=lambda e: e["available"])


def live_combined(cik):
    """합산 감가상각 태그. 오래전에 멈췄으면(AVGO는 2018-05 두 건뿐, 이후 구성요소로만
    보고) 없는 것으로 보고 구성요소로 넘긴다 — 멈춘 합산 태그가 잡히면 구성요소 경로에
    가지 못해 EV/EBITDA가 통째로 빠진다(2026-09-25)."""
    if cik in DDA_SPLIT_BY_CIK:
        return f"{DDA_SPLIT_BY_CIK[cik]['total']}(+분할 뒤 {DDA_SPLIT_BY_CIK[cik]['add']})", split_era_dda(cik)
    tag, rows = pick_tag(cik, DDA_COMBINED)
    stale = date.fromordinal(date.today().toordinal() - 730).isoformat()
    if rows and max(r["end"] for r in rows) < stale:
        return None, []
    return tag, rows


def dda_quarters(cik, ticker):
    """감가상각 분기 시리즈. 합산 태그 우선, 없으면 구성요소를 더한다."""
    tag, rows = live_combined(cik)
    if rows:
        return tag, quarterly_flow(rows, ticker)
    # 구성요소마다 그 분기가 **처음 공시된 때**가 다르다. 작은 항목이 1년 뒤 비교
    # 수치로 처음 나오면(GOOGL 무형자산 상각 $0.12B·금융리스 상각 $0.1B), 예전에는
    # 분기 공개일을 가장 늦은 항목 날짜로 잡아 과거 분기 전체가 1년 늦게 "공개"된
    # 셈이 됐고 EV/EBITDA 이력이 44일만 남았다(2026-09-24). 결산 후 LATE_PART_DAYS
    # 안에 공시된 항목만 그 분기에 더한다 — 그때 알 수 없던 값은 빼는 것이 시점 규칙이다.
    LATE_PART_DAYS = 120
    per_end = {}
    used = []
    for name in DDA_PARTS_BY_CIK.get(cik, DDA_PARTS):
        part = concept(cik, name)
        if not part:
            continue
        used.append(name)
        # 판정은 그 분기가 **처음 알려진 날**로 한다 — 같은 결산일로 끝나는 행(3개월이든
        # 누계든) 가운데 가장 이른 공시일. quarterly_flow가 고른 행의 공시일로 판정하면,
        # 제때 누계 차이로 계산됐던 분기가 1년 뒤 비교 수치(직접값)로 다시 실릴 때 지워진다
        # (Codex 지적, 2026-09-24).
        first_known = {}
        for r in part:
            if "filed" in r and "end" in r:
                first_known[r["end"]] = min(first_known.get(r["end"], r["filed"]), r["filed"])
        for e in quarterly_flow(part, ticker):
            known = first_known.get(e["end"], e["filed"])
            if (date.fromisoformat(known) - date.fromisoformat(e["end"])).days > LATE_PART_DAYS:
                continue
            slot = per_end.setdefault(e["end"], {"val": 0.0, "filed": e["filed"]})
            slot["val"] += e["val"]
            slot["filed"] = max(slot["filed"], e["filed"])
    out = [{"end": k, "val": v["val"], "filed": v["filed"], "start": k}
           for k, v in per_end.items()]
    return ("+".join(used) if used else None), sorted(out, key=lambda e: e["end"])


def annual_points(cik, tags, mode="sum"):
    """연 1회만 보고되는 항목을 TTM 시점값으로 만든다.

    MSFT는 2024년 이전 감가상각을 10-K에만 실었다(FY2019 $9.7B 등). 분기가 없어
    `quarterly_flow`가 아무것도 만들지 못하고, 그 결과 감가상각이 무형자산
    상각 $2B만으로 계산돼 EBITDA 마진 이력이 통째로 낮아졌다(매출의 1.5%).
    연간값 자체가 그 시점의 TTM이므로 그대로 쓴다.

    `mode`가 태그 여러 개를 어떻게 합칠지 정한다. 이 구분을 놓치면 조용히
    이중계상된다(2026-09-22에 `dda_ttm`에서 실제로 그랬다).

    - `"sum"` — **구성요소**다. 같은 결산일의 값들을 더한다(감가상각 + 무형자산
      상각처럼 한 줄이 여러 태그로 쪼개진 경우).
    - `"pick"` — **대체 태그**다. 회사가 같은 항목의 이름만 바꾼 것이라 더하면
      안 된다. 같은 결산일을 두 태그가 함께 내면 먼저 제출된 쪽을 쓴다
      (`pick_tag`·`dedup_earliest_filed`와 같은 규칙).
    """
    out = {}
    for tag in tags:
        for e in concept(cik, tag):
            if "start" not in e or "filed" not in e:
                continue
            if not (350 <= days_between_safe(e) <= 380):
                continue
            key = (tag, e["end"])
            if key not in out or e["filed"] < out[key]["filed"]:
                out[key] = e
    merged = {}
    for (tag, end), e in sorted(out.items(), key=lambda kv: kv[1]["filed"]):
        slot = merged.get(end)
        if slot is None:
            merged[end] = {"val": e["val"], "filed": e["filed"]}
        elif mode == "sum":
            slot["val"] += e["val"]
            slot["filed"] = max(slot["filed"], e["filed"])
        # mode == "pick": 먼저 제출된 쪽이 이미 들어가 있다(filed 순 정렬)
    return sorted(({"end": k, "val": v["val"], "available": v["filed"]}
                   for k, v in merged.items()), key=lambda e: e["available"])


def days_between_safe(e):
    try:
        return (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days
    except Exception:
        return -1


def component_sum(cik, tags):
    """구성요소 태그들을 **더해서** 하나의 시점 시리즈로 만든다.

    현금·차입금·리스처럼 한 줄이 여러 태그로 쪼개져 보고되는 항목용이다.
    같은 날짜에 어떤 태그가 없으면 그 항목은 0으로 본다(그 분기에 없었다는 뜻).
    공개 시점은 그 날짜를 구성한 태그들의 제출일 중 가장 늦은 것으로 잡는다.
    """
    per_date = {}
    seen_by_date = {}
    per_tag = {}
    for tag in tags:
        rows = [e for e in concept(cik, tag) if "end" in e and "filed" in e and "start" not in e]
        best = {}
        for e in rows:
            if e["end"] not in best or e["filed"] < best[e["end"]]["filed"]:
                best[e["end"]] = e
        for end, e in best.items():
            slot = per_date.setdefault(end, {"val": 0.0, "filed": e["filed"]})
            slot["val"] += e["val"]
            slot["filed"] = max(slot["filed"], e["filed"])
            seen_by_date.setdefault(end, []).append(tag)
            per_tag.setdefault(tag, {})[end] = e["val"]
    # 총계 태그와 그 세부내역 태그를 함께 보고하는 회사가 있다. 그런 날짜를
    # 그냥 더하면 부채가 두 번 들어간다. 여기서는 고치지 않고 드러내기만 한다 —
    # 어느 쪽이 총계인지는 회사마다 달라 자동 판정이 위험하기 때문이다.
    # 여러 태그가 같은 날짜를 보고하는 것 자체는 정상이다(유동+비유동을 더하는
    # 경우가 그렇다). 위험한 건 **한 태그가 나머지의 합과 같은 경우**다 —
    # 총계와 세부내역을 함께 태깅한 회사이고, 그대로 더하면 두 배가 된다.
    suspicious = []
    for d, tag_list in seen_by_date.items():
        if len(tag_list) < 3:
            continue
        parts = [per_tag[tg][d] for tg in tag_list if d in per_tag.get(tg, {})]
        if len(parts) < 3:
            continue
        biggest = max(parts)
        if abs(biggest - (sum(parts) - biggest)) < 0.01 * max(abs(biggest), 1):
            suspicious.append(d)
    if suspicious:
        print(f"    ⚠ 총계와 세부내역을 함께 보고한 날짜 {len(suspicious)}건"
              f" (예: {sorted(suspicious)[-1]}) — 이중계상 가능")
    return sorted(({"end": k, "val": v["val"], "available": v["filed"]}
                   for k, v in per_date.items()), key=lambda e: e["available"])


# 같은 항목의 **대체 태그**라 더하면 안 되는 EV 구성요소. 날짜마다 앞 태그 우선으로 하나만 쓴다.
# 우선주 총계(PreferredStockValue)와 전환우선주(ConvertiblePreferredStock…)를 함께 내는 회사는
# component_sum으로 더하면 두 배가 된다(Codex 지적, 2026-09-24).
PICK_COMPONENTS = {"preferred"}


def pick_instant(cik, tags):
    """시점값을 태그 목록 순서대로 골라 하나의 시리즈로 — 날짜마다 앞 태그가 우선."""
    per_date = {}
    for tag in tags:
        for e in concept(cik, tag):
            if "end" not in e or "filed" not in e or "start" in e:
                continue
            cur = per_date.get(e["end"])
            if cur is None or (cur["tag"] == tag and e["filed"] < cur["filed"]):
                if cur is None or cur["tag"] == tag:
                    per_date[e["end"]] = {"val": e["val"], "filed": e["filed"], "tag": tag}
    return sorted(({"end": k, "val": v["val"], "available": v["filed"]} for k, v in per_date.items()),
                  key=lambda e: e["available"])


# LongTermDebt를 비유동분으로만 태깅한다고 10-Q로 확인한 회사(CIK). TSLA 2026-06 LongTermDebt $7,721M =
# 10-Q 장기분, 유동분 $1,340M은 DebtCurrent(총차입금 $9,061M).
DEBT_NONCURRENT_ONLY = {"0001318605"}
# 비유동 차입금 태그를 시기마다 바꿔 내는 회사(유동분 DebtCurrent만 꾸준함)는 10-Q "총차입금"과 같은 한 태그로 고정한다.
# MU는 2025-11까지 LongTermDebt(사채만, 금융리스 제외)·그 뒤 LongTermDebtAndCapitalLeaseObligations(비유동+금융리스)라
# 정의가 섞였다. DebtAndCapitalLeaseObligations = 유동+비유동+금융리스 = 10-Q 주석 9 총계(2026-05 $5,722M), 2019년부터 30개.
# LLY는 유동분을 DebtCurrent("Short-term borrowings and current maturities", 2026-06 $7,050M)로만 내서 세부 태그 목록에 안 잡혔다
# (비유동 $47,858M만 잡힘). 두 태그가 2020년부터 같은 26개 날짜에 있어 합으로 고정 — 10-Q 총 $54,908M.
# XOM: 유동 "Notes and loans payable"은 DebtCurrent, 장기차입금은 LongTermDebtAndCapitalLeaseObligations(금융리스 포함)로만 낸다.
# 기본 목록으로는 2017년에 멈춘 LongTermDebtNoncurrent가 섞이고 유동분이 빠졌다(2026-06-30 $32.2B → 10-Q 합계 $42.4B).
# CRWD: SEC 요약 데이터(companyfacts)에 기말 주식 수가 2025-05부터만 있다(그 전 표지 주식 수는 A·B 종류별 보고라 빠짐).
# 그 전 구간은 분기 가중평균 기본 주식 수로 채운다 — 기말 수와 1~2% 다를 수 있다(2026-10-01).
SHARES_WA_FALLBACK = {"0001535527"}
DEBT_TOTAL_TAG = {"0000723125": "DebtAndCapitalLeaseObligations",
                  # ETN: 1년 안 만기 장기차입금을 LongTermDebtAndCapitalLeaseObligationsCurrent로 내 기본 목록에서 빠졌다(FY2025 말 $1,136M —
                  # 엔진 $8,759M 대 재무상태표 $9,895M, Codex 2026-10-01). 금융리스 포함 태그라 금융리스를 따로 더하지 않는다.
                  "0001551182": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # T: 1년 안 만기 차입금을 DebtCurrent($9.3B, 2026-06-30)로만 내 기본 목록에서 빠졌다(엔진 $134.6B 대 재무상태표 $144.0B, 2026-10-02).
                  # 장기는 금융리스 포함 LongTermDebtAndCapitalLeaseObligations(GE와 같은 조합).
                  "0000732717": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # UNP: 1년 안 만기 차입금을 LongTermDebtAndCapitalLeaseObligationsCurrent($1,288M, 2026-06-30)로만 내 기본 목록에서 빠졌다(2026-10-02).
                  "0000100885": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # COP: 1년 안 만기 차입금 DebtCurrent($462M, 2026-06-30)가 빠지고 금융리스($0.8B)는 장기 태그 안인데 따로 더해졌다(2026-10-02).
                  "0001163165": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # DHR: 1년 안 만기 차입금을 DebtCurrent($1,411M, 2026-06-26)로 낸다 — 기본 목록(LongTermDebtCurrent는 2011년에 멈춤)에서 빠졌다(2026-10-02).
                  "0000313616": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # GLW: 장기차입금 태그만 잡혀 1년 안 만기·단기차입 $668M이 빠졌다(재무상태표 Total debt $8,424M, 2026-10-02).
                  "0000024741": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # ACN: 유동 차입금 중 기업어음만 잡혀 기타(금융리스) $13.4M이 빠졌다 — 유동 112.8 + 장기 5,029.4 = 5,142.3(백만 달러, 2026-05-31 10-Q 주석 9; Codex 2026-10-02).
                  "0001467373": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # NEM: 회사 순차입금 기준(차입금 + 리스·기타 금융채무). 리스·기타 금융채무는 회사 고유 태그라 cfg_nem의 company_tags가
                  # FinanceLeaseLiabilityCurrent·Noncurrent 이름으로 싣는다 — 2026-06-30 차입금 5,083 + 132 + 383 = 5,598(10-Q 총부채 설명과 같음).
                  "0001164727": ["LongTermDebtCurrent", "LongTermDebtNoncurrent", "FinanceLeaseLiabilityCurrent", "FinanceLeaseLiabilityNoncurrent"],
                  # PGR: 재무상태표 차입금 한 줄을 DebtLongtermAndShorttermCombinedAmount로 낸다(2026-06-30 $8,387M) — 기본 목록은 연말 주석 값(2025-12)만 잡혔다(2026-10-02).
                  "0000080661": ["DebtLongtermAndShorttermCombinedAmount"],
                  # MPC: 기본 목록(LongTermDebtCurrent·Noncurrent)이 2012-03에 멈춰 옛 $3.3B가 EV·순차입금에 쓰였다 —
                  # 유동 2,120 + 장기 30,696 = 32,816(2026-06-30 10-Q, MPLX 포함 연결, 2026-10-02).
                  "0001510295": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # NOW: 단기차입(기업어음, ShortTermBorrowings $2,082M)과 장기 사채(LongTermDebt $5,435M) — 엔진 조합은 $4,182M였다(2026-10-02).
                  "0001373715": ["ShortTermBorrowings", "LongTermDebt"],
                  # BMY: ShortTermBorrowings($1,027M = 재무상태표 "Short-term debt obligations")에 1년 안 만기 사채 $768M가 이미 들어 있어 기본 조합이 두 번 셌다($43.9B 대 $43.1B, 2026-10-02).
                  "0000014272": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # VRTX: 차입금이 없다 — LongTermDebt가 2011-09($105M)에 멈춘 값이라 쓰지 않는다(금융리스는 따로 잡힌다, 2026-10-02).
                  "0000875320": ["LongTermDebtNoncurrent"],
                  # PH: 1년 안 만기·기업어음($1,754M = "Notes payable and long-term debt payable within one year")이 기본 조합에서 일부 빠져 $7.8B였다(10-K $8,520M, 2026-10-02).
                  "0000076334": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # CB: 단기 $663M + 장기 $17,452M + 하이브리드 $427M(OtherBorrowings) — 기본 조합은 단기만 잡혀 순현금이 양수로 나왔다(Fable 2026-10-02). 환매조건부 차입은 투자 운용이라 뺀다.
                  "0000896159": ["ShortTermBorrowings", "LongTermDebt", "OtherBorrowings"],
                  # BX: LongTermDebt에 연결 펀드 차입 $124M이 더 들어 있다 — 재무상태표 Loans Payable($13,195M)만(Codex 2026-10-02).
                  "0001393818": "LoansPayable",
                  # BA: LongTermDebt는 장기차입금 유동분까지만 담아 단기차입금이 빠진다($45,596M 대 재무상태표 $45,900M, 2026-10-02).
                  "0000012927": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"], "0000059478": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  "0000034088": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # INTC: 10-Q는 1년 안 만기 차입금을 DebtCurrent로만 낸다(LongTermDebtCurrent는 10-K에만) — 기본 목록으론
                  # 2026-06-27 단기 $1,988M이 빠져 $48,549M이었다(10-Q 합계 $50,537M, 2026-09-29).
                  "0000050863": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # ABBV: 1년 안 만기분을 LongTermDebtAndCapitalLeaseObligationsCurrent로 내 기본 목록에서 빠졌다
                  # (2026-06-30 $62,481M만 → 10-Q 합계 $70,822M, 2026-09-29). 단기차입금은 있는 날짜만.
                  "0001551152": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent",
                                 "LongTermDebtAndCapitalLeaseObligations"],
                  # CVX: 대차대조표는 단기차입금 + 장기차입금(금융리스 포함) 두 줄. 장기 줄을 분기마다 …IncludingCurrentMaturities로
                  # 내고(10-K는 태그가 둘 다 같은 값) — 2026-06-30 $401M + $36,674M = $37.1B(10-Q "total debt" 대조).
                  "0000093410": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities"],
                  # KO: 단기 차입 NotesAndLoansPayable(기업어음 포함 — CommercialPaper는 그 일부라 넣지 않는다) + 유동·비유동 장기차입금.
                  # 장기차입금 태그가 2024년에 LongTermDebt(Non)Current → LongTermDebtAndCapitalLeaseObligations(Current)로 바뀌어
                  # 괄호 묶음(튜플)은 날짜마다 앞 태그를 우선하고 없으면 뒤 태그를 쓴다 — 두 태그가 같은 값을 낸 2023-12-31에
                  # 유동분 $1,960M이 두 번 잡히지 않게(Codex·Fable, 2026-09-30). 2026-07-03 $48 + $6,494 + $37,001 = $43,543M(10-Q).
                  # CAT: 기계·동력·에너지 부문 빚만(2026-09-30 사용자 결정). 금융 부문(Cat Financial) 차입금은 할부·리스 채권과 묶인
                  # 영업 부채이고 이자비용이 영업이익 안에 있다. 부문 값은 차원 태그라 `adapters/cat_segment_debt.py`가 오버레이에 쓴다.
                  # 2026-06-30 $35M + $10,655M = $10,690M(10-Q; 연결 합계 $45,146M 중 금융 부문 $34,456M 제외).
                  "0000018230": ["CatMETShortTermBorrowings", "CatMETLongTermDebtCurrent", "CatMETLongTermDebtNoncurrent"],
                  # DE: 장비 부문 빚만(CAT과 같은 규칙). 부문 차입금은 10-Q·10-K 보충 표에 태그 없이 있어 `adapters/de_equipment_debt.py`가
                  # 원문 장비 열을 오버레이에 싣는다(장비 + 금융 + 제거 = 연결 대조). 2026-08-02 $417 + $1 + $8,907 = $9,325M(연결 $63,836M).
                  "0000315189": ["DeEquipShortTermBorrowings", "DeEquipSecuritizationBorrowings", "DeEquipLongTermBorrowings"],
                  # MRK: 유동 차입을 DebtCurrent("Loans payable and current portion of long-term debt")로만 낸다(분기마다).
                  # 기본 목록으론 2026-06-30 $2,825M이 빠져 $51,081M이었다(10-Q 합계 $53,906M, 2026-09-30, INTC와 같은 경우).
                  "0000310158": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # AMAT: 재무상태표 "Short-term debt"(ShortTermBorrowings)가 1년 안 만기 장기차입금 + 기업어음 합계인데
                  # 유동 장기차입금을 LongTermDebtCurrent로도 따로 태그해 기본 목록이 두 번 더했다(2026-07-26 $1,199M,
                  # 2024-10~2025-07 $700M). 2026-07-26 $1,299 + $5,245 = $6,544M(10-Q, 2026-09-30).
                  "0000006951": ["ShortTermBorrowings", "LongTermDebtNoncurrent"],
                  # UNH: 유동 차입을 DebtCurrent("Short-term borrowings and current maturities")로만 낸다 — 기본 목록으론
                  # 2026-06-30 $3,827M이 빠졌다(10-Q 합계 $73,328M, 2026-09-30, MRK와 같은 경우).
                  "0000731766": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # GE: 1년 안 만기·단기 차입 DebtCurrent($2,000M) + 장기 LongTermDebtAndCapitalLeaseObligations($17,157M) = 10-Q 합계.
                  "0000040545": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # DELL: 단기 DebtCurrent($8,481M) + 장기 LongTermDebtNoncurrent($25,985M) = $34,466M(10-Q). DFS 빚($9.6B)은 이자가
                  # 영업이익 밖(interest and other, net)이라 차입금에 넣는다(2026-10-01 사용자 결정, CAT과 반대).
                  "0001571996": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # HD: 기업어음 CommercialPaper($4,248M) + 1년 안 만기 장기 LongTermDebtAndCapitalLeaseObligationsCurrent($4,697M) +
                  # 장기 LongTermDebtAndCapitalLeaseObligations($43,951M) = $52,896M(10-Q). 금융리스는 이 태그 안에 있어 리스에 다시 더하지 않는다.
                  "0000354950": [("ShortTermBorrowings", "CommercialPaper"), "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # 단기는 정확한 합계 태그 우선(기업어음은 반올림값, Codex)
                  # RTX: ShortTermBorrowings($229M) + LongTermDebtAndCapitalLeaseObligationsCurrent($5,296M) + LongTermDebtAndCapitalLeaseObligations($31,858M)
                  # = $37,383M(2026-06-30 10-Q "Total debt"). 기본 조합은 1년 안 만기 $5.3B를 빠뜨렸다(HD·PM과 같은 모양).
                  "0000101829": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # LIN: 기본 목록은 OtherShortTermBorrowings($330M, 단기차입금의 일부) 등이 겹쳐 2026-06-30 $32,874M였다.
                  # 10-Q 합계 $28,013M = 단기 $4,861M + 1년 안 만기 $2,474M + 장기 $20,678M(2026-10-01).
                  "0001707925": ["ShortTermBorrowings", "LongTermDebtCurrent", "LongTermDebtNoncurrent"],
                  # APH: 기본 목록이 장기분만 잡아 1년 안 만기 $1,634M가 빠졌다(10-Q 합계 $18,811M, 2026-10-01).
                  "0000820313": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # VZ: 장기 줄이 금융리스를 포함하는데 리스로 금융리스를 또 더했다(Fable, 2026-10-01). 1년 안 + 장기 = $165,231M(10-Q).
                  "0000732712": ["LongTermDebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # GEV: 10-Q 주석 14 차입금 합계 $2,849M(회사채 $2.6B + 금융리스 등, 1년 안 만기 $55M 포함). 장기 태그만 잡혀 $2,794M였다(2026-10-01).
                  "0001996810": ["LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities"],
                  # TMO: LongTermDebt($42,284M)는 단기 차입 일부·금융리스가 빠진다. 재무상태표 = 단기·1년 안 만기 $3,368M + 장기 $39,181M
                  # = $42,549M(2026-06-27 10-Q, 2026-10-01).
                  "0000097745": ["DebtCurrent", ("LongTermDebtAndCapitalLeaseObligations", "LongTermDebtNoncurrent")],   # 앞 태그가 2021-10부터라 그 전은 장기 태그(Codex)
                  # IBM: 차입금 $61,987M = 단기 $5,775M + 장기(금융리스 포함) $56,212M(10-Q). 합계 태그 없이 기본 목록이면 금융리스 $1.15B가
                  # 리스에 다시 더해졌다(Codex, 2026-10-01).
                  "0000051143": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligations"],
                  # TMUS: 2026 10-Q부터 장기차입금을 특수관계자 차원으로만 내 companyfacts가 2025-12에서 멈췄다(단기 $6.1B만 남음).
                  # 10-Q 차입금 주석 "Total debt"(LongTermDebt, DebtInstrumentAxis=TotalDebtMember, 금융리스 제외)를
                  # `adapters/dim_member_supplement.py`가 오버레이에 싣는다(2021년부터). 2026-06-30 $84,621M(단기 $6,117 + 장기 $78,504, 2026-10-01).
                  # 금융리스는 이 합계 밖이고 기본 리스(운용)에도 없어 EV에서 빠졌다 → 유동 + 비유동 금융리스 태그를 더한다
                  # ($1,178 + $1,121, Codex). build_dcf는 "FinanceLease"가 든 목록이면 리스에 다시 더하지 않는다.
                  "0001283699": ["LongTermDebt", "FinanceLeaseLiabilityCurrent", "FinanceLeaseLiabilityNoncurrent"],
                  # QCOM: LongTermDebt가 분기마다 비유동 장기차입금만(LongTermDebtNoncurrent는 10-K만)이고 유동분은 DebtCurrent.
                  # 기본 목록이 2026-06-28 유동 $2,489M를 빠뜨렸다. $2,489 + $12,781 = $15,270M(10-Q, 2026-10-01).
                  "0000804328": ["DebtCurrent", "LongTermDebt"],
                  # PEP: 재무상태표 "Short-term debt obligations"(ShortTermBorrowings $10,602M)가 기업어음 $6,100M·1년 안 만기 $1,600M를
                  # 이미 담는데 기본 목록이 둘을 또 더해 $7.7B가 두 번 잡혔다. 장기 줄은 분기마다 LongTermDebtAndCapitalLeaseObligations
                  # (LongTermDebtNoncurrent는 10-K만). 2026-06-13 $10,602 + $42,612 = $53,214M(10-Q, 2026-10-01).
                  "0000077476": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligations"],
                  # ADI: 10-K 결산일마다 기업어음이 ShortTermBorrowings와 CommercialPaper 두 태그로 같은 값($446.6M, 2025-11-01)이라 기본 목록이
                  # 두 번 더했다. 기업어음(없으면 단기차입금) + 1년 안 만기 + 장기. 2026-08-01 $1,005 + $1,345 + $6,772 = $9,122M(10-Q, 2026-10-01).
                  # 목록에 넣으면 기본적 분석 차입금의존도도 같은 차입금을 쓴다(fetch_financials 값은 기업어음을 뺐다 — 16.8% 대 18.8%, Codex).
                  "0000006281": [("CommercialPaper", "ShortTermBorrowings"), "LongTermDebtCurrent", "LongTermDebtNoncurrent"],
                  # CSCO: DebtCurrent($10,161M — 기업어음 + 1년 안 만기 장기) + LongTermDebtNoncurrent($19,372M) = $29,533M(FY2026 10-K "Total debt").
                  # 기본 조합은 LongTermDebtCurrent + Noncurrent($22,872M)라 기업어음 $6.7B가 빠졌다.
                  "0000858877": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # ORCL: 유동 NotesPayableCurrent($7,625M) + 비유동 LongTermNotesAndLoans($117,712M) = $125,337M(2026-08-31 10-Q).
                  # 기본 태그가 하나도 없어 차입금 0으로 계산됐다(이자비용 $5.1B와 모순, debt_suspect). 연간 전용 태그는 뒤 순위로 둔다.
                  "0001341439": [("NotesPayableCurrent", "DebtCurrent"), ("LongTermNotesAndLoans", "LongTermNotesPayable")],
                  # PANW: 차입금은 전환사채뿐이다. 기본 태그(ConvertibleNotesPayable*)는 2023-07-31 $1,992M에서 멈춰 그 뒤 날짜에
                  # 옛 값이 그대로 쓰였다(2025-07-31 실제 0, 2026-07-31 CyberArk 승계분 $1,774M — FY2026 10-K). 0을 명시한 태그를 우선한다.
                  "0001327567": [("ConvertibleDebtCurrent", "ConvertibleNotesPayableCurrent"), ("ConvertibleDebtNoncurrent", "ConvertibleNotesPayableNoncurrent")],
                  # PM: 단기 ShortTermBorrowings($3,341M) + 1년 안 만기 장기 LongTermDebtAndCapitalLeaseObligationsCurrent($3,406M) +
                  # 장기 LongTermDebtAndCapitalLeaseObligations($42,366M) = $49,113M(2026-06-30 10-Q). 기본 태그로는 유동분이 빠졌다.
                  "0001413329": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  "0000021344": ["NotesAndLoansPayable",
                                 ("LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtCurrent"),
                                 ("LongTermDebtAndCapitalLeaseObligations", "LongTermDebtNoncurrent")]}


# EV 구성요소의 종목별 태그(CIK). V: 유동 투자증권을 2020년까지 AvailableForSaleSecuritiesDebtSecuritiesCurrent로,
# 그 뒤로는 Investments(2018~ 이어짐, Q3 FY26 $1,433M)로 낸다. 기본 목록을 합치면 2020년 값($3.6B)이 계속 남아
# 순현금·EV·DCF가 틀렸다(Codex, 2026-09-27). 겹치는 2018~2020년도 한 태그만 쓴다.
# 우선주·비지배지분은 V에선 빈 목록(0)이다 — 우선주는 PreferredStockValue가 2019년($5,462M)에 멈췄고, 분기말 환산
# 주식 수(v:SharesOutstandingAsConvertedBasis)가 이미 우선주 환산분을 포함해 EV에 또 더하면 이중 계산이다.
# 비지배지분은 2011년 값($2M)뿐이다(Fable, 2026-09-27).
EV_TAGS_BY_CIK = {"0001403161": {"sti": ["Investments"], "preferred": [], "nci": []},
                  # GLW: 우선주(삼성디스플레이 보유 $2.3B)는 2021년 보통주로 바뀌어 태그가 2021-03에 멈췄다 — 옛 값이 EV에 더해졌다(2026-10-02).
                  "0000024741": {"preferred": []},
                  # FTNT: 단기투자를 2021-06 뒤 OtherShortTermInvestments로만 낸다(2026-06-30 $1,134.7M) — 멈춘 ShortTermInvestments(2021-06 $1,233.9M)가 쓰였다(2026-10-02).
                  "0001262039": {"sti": ["OtherShortTermInvestments"]},
                  # NEM: 운용리스 유동·비유동 태그는 2021-09, 우선주 태그는 2012-09에 멈춰 옛 값이 EV에 더해졌다 — 운용리스는 연말 합계
                  # OperatingLeaseLiability(2025-12 $109M)로, 우선주는 없음으로. 리스·기타 금융채무($515M)는 차입금 쪽(DEBT_TOTAL_TAG)에 넣는다(2026-10-02).
                  "0001164727": {"lease": ["OperatingLeaseLiability"], "preferred": []},
                  # PGR: 비지배지분 태그가 2016-06에 멈췄다(현재 비지배지분 없음 — 10-Q 자본 항목에 없다, 2026-10-02).
                  # 현금은 Cash 태그로만 낸다(2026-06-30 $178M) — 기본 태그가 없어 0으로 잡혔다(Fable 2026-10-02).
                  "0000080661": {"nci": [], "cash": ["Cash"]},
                  # CB: 현금 태그가 2023-06, 단기투자 태그가 2019-09에 멈춰 옛 값($2.29B·$2.84B)이 쓰였다 — 제한 현금 포함 현금 $2,753M, 기타 단기투자 $5,458M(Codex 2026-10-02).
                  "0000896159": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"], "sti": ["OtherShortTermInvestments"]},
                  # BLK: 리스부채를 유동·비유동으로 나누지 않고 총액(OperatingLeaseLiability, 2026-06-30 $2,224M)만 낸다 — 기본 목록으론 0이었다(2026-10-01).
                  "0002012383": {"lease": ["OperatingLeaseLiability"]},
                  # ETN: 분기 재무상태표에는 비유동 운용리스 부채만 있고 유동분은 10-K에만 있다 → JNJ처럼 10-K 총액(FY2025 $789M)을 쓴다(Codex 2026-10-01).
                  "0001551182": {"lease": ["OperatingLeaseLiability"]},
                  # T: 단기투자 태그가 2014-12 $1.89B에서 멈춰 그 값이 계속 순현금에 더해졌다. 리스는 분기엔 비유동분만 있어 10-K 총액(Codex 2026-10-02).
                  "0000732717": {"sti": [], "lease": ["OperatingLeaseLiability"]},
                  # MCD: 단기투자 줄이 없다(ShortTermInvestments가 2014-09에 멈춤, 2026-10-02).
                  "0000063908": {"sti": []},
                  # DHR: 현금 태그 CashAndCashEquivalentsAtCarryingValue가 2020-10에 멈춰 그 값($5.7B)이 계속 쓰였다 → 제한 현금 포함 총계
                  # (2026-06-26 $4,348M, 재무상태표 현금과 대조할 것). 리스는 분기마다 총액만(OperatingLeaseLiability), 우선주는 2023년 전환으로 없음(2026-10-02).
                  "0000313616": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"], "lease": ["OperatingLeaseLiability"], "preferred": []},
                  # UNP: 단기투자를 만기보유 증권(HeldToMaturitySecuritiesCurrent, $500M)으로 낸다 — 기본 목록으론 비었다(2026-10-02).
                  "0000100885": {"sti": ["HeldToMaturitySecuritiesCurrent"]},
                  # PFE: 재무상태표 단기투자 총액은 OtherShortTermInvestments($10,723M, 2026-06-28 = 매도가능 $7,281M + 만기보유 $1,811M + 지분 $1,630M).
                  # ShortTermInvestments는 2021-10에 멈췄고 기본 목록은 매도가능 증권만 잡았다(2026-10-02).
                  "0000078003": {"sti": ["OtherShortTermInvestments"]},   # 두 태그를 같이 두면 2021년에 합산돼 두 배가 됐다(Codex) — 총액 태그만
                  # VZ: 단기투자 줄이 없다(ShortTermInvestments가 2015-12 $350M에 멈춰 그 값이 계속 쓰였다, Codex 2026-10-01).
                  "0000732712": {"sti": []},
                  # STX: 단기투자 태그 AvailableForSaleSecuritiesDebtSecuritiesCurrent가 2012-06-29 $411M에서 멈췄는데 2026년 순현금에 더해졌다
                  # (Codex, 2026-10-01). FY2026 10-K는 현금 $1,704M뿐이다.
                  "0001137789": {"sti": []},
                  # JNJ: 비유동 리스 태그는 2019년에 멈췄고 총 리스부채(OperatingLeaseLiability, 10-K 연간)만 이어진다.
                  "0000200406": {"lease": ["OperatingLeaseLiability"]},
                  # XOM: 단기투자 줄이 없다(ShortTermInvestments 태그가 2011-06에 멈춰 그 값이 계속 쓰였다). 리스는 10-K 연간 총액.
                  "0000034088": {"sti": [], "lease": ["OperatingLeaseLiability"]},
                  # MA: 유동 투자증권은 V처럼 Investments($318M, 2026-06-30)로 낸다 — 기본 목록으론 0이었다(Codex, 2026-09-29).
                  "0001141391": {"sti": ["Investments"]},
                  # CVX: 재무상태표 현금을 2024-09부터 회사 고유 태그(cvx:CashAndCashEquivalentsExcludingTimeDeposits)로 내
                  # companyfacts에 없다 — 표준 태그는 2024-06-30 $4,008M에서 멈춰 그 값이 계속 쓰였다(2026-06-30 실제 $8,527M).
                  # 공정가치 주석 태그(0.1B 단위 반올림)는 2021년부터 매 분기 이어진다(2026-06-30 $8.5B, 2026-09-29).
                  "0000093410": {"cash": ["CashAndCashEquivalentsFairValueDisclosure"]},
                  # LRCX: ShortTermInvestments가 2015-06-28 $2,575M에서 멈춰 그 값이 계속 순현금·EV에 더해졌다(2026-09-30).
                  # 이후 투자 잔액은 Investments 태그(2021-09 $569M → 2024-03-31 $0)로 냈고, FY2026 10-K 재무상태표에는
                  # 단기투자 줄이 없다. Investments가 0으로 끝나 옛 값이 이어지지 않는다(Fable).
                  "0000707549": {"sti": ["Investments"]},
                  # KO: 단기투자 = OtherShortTermInvestments + MarketableSecurities(10-Q "Short-term investments" 622 +
                  # "Marketable securities" 2,842, 2026-07-03). 기본 목록의 MarketableSecuritiesCurrent는 2020-12($2,348M)에 멈췄다.
                  "0000021344": {"sti": ["OtherShortTermInvestments", "MarketableSecurities"]},
                  # CAT: 재무상태표에 단기투자 줄이 없다(2026-06-30 10-Q). ShortTermInvestments가 2014-09-30 $378M에서 멈춰 그 값이 쓰였다.
                  "0000018230": {"sti": []},
                  "0000315189": {"sti": [], "lease": ["OperatingLeaseLiability"]},
                  # GILD: CashAndCashEquivalentsAtCarryingValue가 2022-12 $5,412M에 멈춰 2026년 순현금에 쓰였다(실제 2026-06-30 $3,179M) —
                  # 현금은 제한 현금 포함 총계 태그(재무상태표 현금과 같은 값, 2026-10-01)
                  "0000882095": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]},   # DE: 유가증권 $1.35B 중 $1.20B가 금융 부문(보험) 몫 — CAT처럼 단기투자를 더하지 않는다
                  # KLAC: AvailableForSaleSecuritiesDebtSecuritiesCurrent가 2021-03-31 $990.6M에서 멈춰 그 값이 쓰였다. 재무상태표
                  # "Marketable securities" $3,252.6M(2026-06-30) = 매도가능 채권 합계 $3,205.8M + 상장 지분증권 약 $46.8M(2026-10-01).
                  "0000319201": {"sti": ["AvailableForSaleSecuritiesDebtSecurities"]},
                  # IBM: 단기투자 태그가 2021-03-31 $600M에서 멈춰 쓰였다. 10-Q "Marketable securities" $960M(2026-06-30)은
                  # DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent(Codex, 2026-10-01).
                  "0000051143": {"sti": ["DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent"]},
                  # RTX: MarketableSecuritiesCurrent $711M(2026-06-30)은 비적격 퇴직급여 지급용 신탁 증권이다(10-Q 주석 10·13).
                  # 회사가 쓸 수 있는 단기투자가 아니라 순현금에서 뺀다(Codex, 2026-10-01).
                  "0000101829": {"sti": []},
                  # MRK: 우선주가 없다. PreferredStockValue가 2009-09-30 $2,500M(셰링-플라우 합병 때)에서 멈춰 EV에 계속 더해졌다(2026-09-30).
                  "0000310158": {"preferred": []},
                  # UNH: 리스는 10-K 연간 총액(OperatingLeaseLiability)만 — 기본 유동·비유동 태그는 2019년 값에 멈췄다.
                  "0000731766": {"lease": ["OperatingLeaseLiability"]},
                  # GE: CashAndCashEquivalentsAtCarryingValue가 2017년($43.3B)에 멈췄다. 재무상태표 첫 줄은 제한 현금 포함 합계뿐.
                  "0000040545": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]},
                  # PG: CashAndCashEquivalentsAtCarryingValue가 2019-09($9.3B)에 멈췄다. 재무상태표 현금 $9,942M(2026-06-30)은 합계 태그로만 낸다.
                  "0000080424": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]},
                  # GEV: 재무상태표 첫 줄이 "Cash, cash equivalents, and restricted cash" $13,120M 합계뿐이라 현금이 비어 있었다(2026-10-01, GE·PG 선례).
                  "0001996810": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]}}
# 이 결산일부터 0인 구성요소(CIK) — 잔액이 사라졌는데 태그가 멈춰 마지막 값이 계속 쓰이는 경우. JNJ 비지배지분은
# 2023-07-02(Kenvue 분리 중) $1,260M이 마지막이고 8월 교환 공개매수로 사라졌다 → 2023-10-01 분기(10-Q 2023-10-27)부터 0.
# 전 기간 0으로 두면 실제 잔액이 있던 2023년 EV까지 빠진다(Codex, 2026-09-28).
EV_ZERO_FROM_BY_CIK = {"0000200406": {"nci": ("2023-10-01", "2023-10-27")}}
# 차입금 합계의 가용일을 10-K 원문 날짜로 바로잡는 회사(CIK → {분기말: 가용일}). 합계 가용일은 구성요소 중 가장 늦은 접수일인데,
# 한 구성요소(0)가 나중 공시의 비교 열에서만 태깅되면 그 분기 값이 1년 가까이 늦게 열린다.
# PANW: 2025-07-31 전환사채 0(유동 0은 FY2025 10-K 2025-08-29, 비유동 0은 2026-06-03 10-Q 비교 열에서만 태깅) — FY2025 10-K 재무상태표에
# 전환사채 줄이 "—"이고 옛 사채는 2025-06-01까지 전환·상환(FY2026 10-K Note 12, Codex). 그래서 2025-08-29부터 0이다.
DEBT_AVAILABLE_FIX = {"0001327567": {"2025-07-31": "2025-08-29"}}


def ev_component(cik, name, tags):
    tags = EV_TAGS_BY_CIK.get(cik, {}).get(name, tags)
    zf = EV_ZERO_FROM_BY_CIK.get(cik, {}).get(name)
    if zf:
        rows = [e for e in component_sum(cik, tags) if e["end"] < zf[0]]
        return rows + [{"end": zf[0], "val": 0.0, "available": zf[1]}]
    if name == "debt" and cik in DEBT_TOTAL_TAG:
        tags = DEBT_TOTAL_TAG[cik]
        tags = tags if isinstance(tags, list) else [tags]
        if not any(isinstance(t, tuple) for t in tags):
            return component_sum(cik, tags)
        # 튜플 항목은 날짜마다 앞 태그 우선(pick_instant), 문자열 항목은 그대로 더한다(KO).
        by_end = {}
        for t in tags:
            for e in (pick_instant(cik, list(t)) if isinstance(t, tuple) else component_sum(cik, [t])):
                slot = by_end.setdefault(e["end"], {"end": e["end"], "val": 0.0, "available": e["available"]})
                slot["val"] += e["val"]
                slot["available"] = max(slot["available"], e["available"])
        for end, av in DEBT_AVAILABLE_FIX.get(cik, {}).items():
            if end in by_end:
                by_end[end]["available"] = av
        return sorted(by_end.values(), key=lambda e: e["available"])
    out = pick_instant(cik, tags) if name in PICK_COMPONENTS else component_sum(cik, tags)
    # 차입금을 유동·비유동으로 나누지 않고 총계(LongTermDebt)로만 내는 회사가 있다 — SPCX $38.3B가
    # 통째로 빠져 순현금이 $98.6B로 부풀었다(Fable, 2026-09-25). 세부 태그가 **하나도 없을 때만** 쓴다
    # (둘 다 내는 회사에서 더하면 이중 계산).
    fell_back = name == "debt" and not out
    total_dates = set()
    if fell_back:
        out = component_sum(cik, ["LongTermDebt"])
    elif name == "debt" and out:
        # 세부 태그가 옛날에만 있고 이후 총계만 내는 회사(TSLA는 세부가 2018-12에 끝나고 2019년부터
        # LongTermDebt 총계만)는 세부가 **없는 날짜**를 총계로 채운다. 세부가 있는 날짜는 그대로(이중 계산 방지).
        # 총계로 채운 날짜에는 아래 LTD&CLO 보충을 더하지 않는다(총계에 이미 들어 있다).
        have = {e["end"] for e in out}
        filled = [e for e in component_sum(cik, ["LongTermDebt"]) if e["end"] not in have
                  and e["end"] > max(have)]
        if filled:
            # 이런 회사는 LongTermDebt를 비유동분으로만 태깅한다(TSLA 2026-06 $7.72B = 10-Q 장기분,
            # 유동분 $1.34B는 DebtCurrent). 같은 날짜의 DebtCurrent를 더한다 — 총계 $9.06B와 일치.
            # us-gaap 정의상 LongTermDebt는 유동분 포함 총액이라, 비유동분만 태깅한다고 10-Q로 확인한
            # 회사(DEBT_NONCURRENT_ONLY)에서만 DebtCurrent를 더한다(Fable: 일반화하면 유동분 이중 계산 위험).
            cur = {e["end"]: e for e in component_sum(cik, ["DebtCurrent"])} if cik in DEBT_NONCURRENT_ONLY else {}
            if cik not in DEBT_NONCURRENT_ONLY:
                print(f"    ⚠ 차입금: 세부 태그 이후를 LongTermDebt로 채움({len(filled)}개 날짜) — 유동분 포함 여부를 10-Q로 확인할 것")
            for e in filled:
                c = cur.get(e["end"])
                if c:
                    e["val"] += c["val"]
                    e["available"] = max(e["available"], c["available"])
            out = sorted(out + filled, key=lambda e: e["available"])
            total_dates = {e["end"] for e in filled}
        else:
            total_dates = set()
    # 비유동 차입금을 LongTermDebtAndCapitalLeaseObligations(비유동, 리스 포함)로 낸 기간이 있다.
    # AVGO는 2025-08까지 이 태그로만 내서 VMware 인수 차입금 약 $60B이 EV·투하자본에서 빠졌다
    # (2026-09-25). LongTermDebtNoncurrent가 **없는 날짜에만** 더한다(둘 다 있는 날짜는 같은 값).
    # 총계(LongTermDebt) 폴백으로 채운 회사에는 더하지 않는다 — 총계에 이미 들어 있다
    # (SPCX 2026-06 $38.3B + $36.8B = $75.1B로 두 번 잡혔다, Fable).
    if name == "debt" and out and not fell_back:
        nonc = {e["end"] for e in component_sum(cik, ["LongTermDebtNoncurrent"])}
        by_end = {e["end"]: e for e in out}
        for e in component_sum(cik, ["LongTermDebtAndCapitalLeaseObligations"]):
            if e["end"] in nonc or e["end"] in total_dates:
                continue
            if e["end"] in by_end:
                slot = by_end[e["end"]]
                slot["val"] += e["val"]
                slot["available"] = max(slot["available"], e["available"])
            else:
                by_end[e["end"]] = dict(e)
        out = sorted(by_end.values(), key=lambda e: e["available"])
    return out


def dda_ttm(cik, ticker):
    """감가상각 TTM 시리즈. 태그 구조가 두 갈래라 다루는 법이 다르다.

    - **대체 태그**(`DDA_COMBINED`): 같은 항목의 이름을 회사가 도중에 바꾼 것이다.
      NVDA는 2021-08까지 `DepreciationAndAmortization`으로, 그 뒤로는
      `DepreciationDepletionAndAmortization`으로 낸다. 이것들은 더하는 게 아니라
      **이어붙여야** 한다. `pick_tag`가 이미 한 줄기로 병합하므로 그 결과에서
      TTM을 하나 만든다.
    - **구성요소**(`DDA_PARTS`): 합산 태그가 아예 없는 회사다. MSFT는 무형자산
      상각은 분기로, 감가상각은 2024년까지 연 1회로 보고했다. 한 덩어리로 묶으면
      분기가 있는 쪽만 잡히고 연간만 있는 쪽이 통째로 빠진다(감가상각이 매출의
      1.5%로 나왔던 이유). 각 항목의 시리즈를 따로 만들고 평가 시점마다 더한다.

    2026-09-22 이전에는 이 둘을 구분하지 않고 `DDA_COMBINED`도 전부 더했다.
    NVDA에서 2021-08에 멈춘 옛 태그의 마지막 값 $1.154B이 영구히 더해져 최신
    D&A가 $3.687B 대신 $4.383B로 **18.9% 부풀어 있었다**(Codex 발견). 같은 값이
    EBITDA 마진 → 시나리오 내재가치 → 요구 성장률까지 흘러갔다.
    """
    def with_annuals(series, tags, mode):
        have = {e["end"] for e in series}
        for e in annual_points(cik, tags, mode=mode):
            if e["end"] not in have:
                series.append(e)
        return sorted(series, key=lambda e: (e["available"], e["end"]))

    combined, rows = live_combined(cik)
    if rows:
        q = quarterly_flow(rows, ticker)
        series = with_annuals(ttm_series(q) if q else [], DDA_COMBINED, "pick")
        return combined, series

    per_tag = {}
    for tag in DDA_PARTS_BY_CIK.get(cik, DDA_PARTS):
        part = concept(cik, tag)
        if not part:
            continue
        q = quarterly_flow(part, ticker)
        series = with_annuals(ttm_series(q) if q else [], [tag], "sum")
        # 멈춘 구성요소(AVGO 금융리스 상각은 FY2024 10-K가 마지막)는 마지막 값이 영원히 더해진다.
        # 연 1회만 내는 항목(MSFT 감가상각)도 다음 10-K는 결산 뒤 약 425일 안에 나오므로,
        # 마지막 결산일에서 450일이 지난 평가 시점에는 넣지 않는다.
        if series:
            stale_after = date.fromordinal(date.fromisoformat(series[-1]["end"]).toordinal() + 450).isoformat()
            per_tag[tag] = (series, stale_after)
    if not per_tag:
        return None, []

    # 평가 시점은 **공시일**이다. 예전에는 `available`에 결산일을 적어두고
    # 결산일로 조회해, 각 구성요소가 한 분기씩 밀린 값으로 더해졌다.
    out = []
    for day in sorted({e["available"] for s, _ in per_tag.values() for e in s}):
        parts = []
        for s, stale_after in per_tag.values():
            if day > stale_after:
                continue
            newest = None
            for e in s:
                if e["available"] <= day:
                    newest = e
                else:
                    break
            if newest is not None:
                parts.append(newest)
        if parts:
            out.append({"end": max(e["end"] for e in parts),
                        "val": sum(e["val"] for e in parts),
                        "available": day})
    return "+".join(per_tag), out


def check_fresh(series, last_day, max_lag_days=200):
    """시리즈가 최근 분기까지 닿는지 본다.

    태그 교체를 놓치면 옛 값이 조용히 계속 쓰이므로, 마지막 일봉보다 크게
    뒤처지면 눈에 띄게 표시한다.
    """
    if not series:
        return "  ← 비어 있음"
    lag = (date.fromisoformat(last_day) - date.fromisoformat(series[-1]["end"])).days
    return f"  ← ⚠ {lag}일 뒤처짐" if lag > max_lag_days else ""


def as_of(series, day):
    """그날까지 공개돼 있던 가장 최근 값."""
    val = None
    for e in series:
        if e["available"] <= day:
            val = e["val"]
        else:
            break
    return val


def load_daily(ticker):
    path = os.path.join(REPO, "v2", f"{ticker}_full_widget.html")
    if not os.path.exists(path):
        path = os.path.join(REPO, f"{ticker}_full_widget.html")
    html = open(path).read()
    m = re.search(rf"const {ticker}_DAILY\s*=\s*(\[.*?\]);", html, re.S)
    return json.loads(m.group(1).replace("'", '"'))


# 자기 이력 분포를 ADR 가격이 아닌 원주 가격으로 만드는 종목(2026-09-27 사용자 결정, SKHY: ADR 상장 2026-07-10).
# 분포는 원주(KRX) 종가를 ADR 1주 상당 달러(÷ ADR당 주식 수 역수 ÷ 그날 환율)로 바꿔 5년치를 쓰고,
# **마지막 날(현재)은 ADR 가격**을 쓴다 — 현재 위치에 ADR 프리미엄이 그대로 들어간다.
LOCAL_HISTORY = {"SKHY": {"loader": "skhy_krx", "ads_per_share": 10}}


# 자기 이력 창의 시작일을 늦추는 종목. GE: 버노바 분사(2024-04-02) 뒤 첫 재무상태표(2024-06-30)가 나온 2024-07-23
# (2분기 10-Q)부터 — 그 전 배수는 분사 조정된 주가와 복합기업 재무가 섞여 싸게 나온다(2026-09-30 사용자 결정). 2024-03-31
# 재무상태표는 버노바를 포함해 자본 $29.9B(분사 뒤 $18.6B)였고, 1분기 현금흐름(2023 Q1)이 재작성되지 않아 2분기 누계 차감이 섞였다(Fable).
HISTORY_START = {"GE": "2024-07-23",
                 # DELL: VMware 분사(2021-11-01) 뒤 첫 재무상태표(FY2022 말 2022-01-28)가 나온 10-K 공시일(2026-10-01 사용자 결정).
                 "DELL": "2022-03-24",
                 # IBM: Kyndryl 분사(2021-11-03) 뒤 첫 재무상태표(2021-12-31)가 나온 FY2021 10-K 공시일(2026-10-01, GE·DELL 방식).
                 "IBM": "2022-02-22",
                 # WDC: SanDisk 분사(2025-02-21 완료). 첫 분사 후 재무상태표는 Q3 FY25 10-Q(2025-05-02)지만, 계속사업 기준으로 재작성한
                 # 분기 매출·이익이 처음 나온 것은 FY25 10-K(2025-08-14)다. 그 전 날짜는 재작성 전 최근 4분기(분사 전 원공시와 섞임,
                 # 2023-06 분기 음수)를 써 PSR이 29.8배로 튀었다 → 10-K 공시일부터(2026-10-02, GE 방식 변형).
                 "WDC": "2025-08-14",
                 # T: WarnerMedia 분사(2022-04-08). 첫 분사 후 재무상태표는 2022-06-30이지만, 최근 4분기 합이 모두 분사 뒤 분기인 첫
                 # 시점은 2023-03-31(1분기 10-Q 2023-05-01)이다 — 그 전 합은 분사 전 분기(WarnerMedia 포함)와 섞인다(WDC 교훈, 2026-10-02).
                 "T": "2023-05-01",
                 # DHR: Veralto 분사(2023-09-30) 뒤 첫 재무상태표(2023-09-29)가 나온 3분기 10-Q 공시일(2026-10-02, GE 방식). 재작성 값이
                 # 2022년 분기부터 있어 그 날 최근 4분기 합은 모두 계속사업 기준이다.
                 "DHR": "2023-10-24"}


def history_daily(ticker, daily):
    if ticker in HISTORY_START:
        daily = [r for r in daily if r[0] >= HISTORY_START[ticker]]
    cfg = LOCAL_HISTORY.get(ticker)
    if not cfg:
        return daily
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "adapters"))
    mod = __import__(cfg["loader"])
    last = daily[-1]
    y, m, d = map(int, last[0].split("-"))
    start = date(y - 5, m, min(d, 28)).isoformat()
    k = cfg["ads_per_share"]
    bars = [[b[0]] + [v / k / fx.rate(ticker, b[0]) for v in b[1:5]]
            for b in mod.load() if start <= b[0] < last[0]]
    return bars + [last]


def percentile_rank(values, current):
    below = sum(1 for v in values if v < current)
    return below / len(values) * 100


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--json", help="결과를 저장할 경로")
    args = ap.parse_args()
    t = args.ticker.upper()
    cik = feh.CIKS.get(t)
    if not cik:
        sys.exit(f"{t}: CIK를 모른다. fetch_eps_history.py의 CIKS에 추가할 것")

    daily = history_daily(t, load_daily(t))
    print(f"{t}: 일봉 {len(daily)}개 ({daily[0][0]} ~ {daily[-1][0]})"
          + (" — 원주 가격 이력 + 마지막 날 ADR 가격" if t in LOCAL_HISTORY else ""))

    # EPS는 기존 스크립트가 이미 만든 형식을 그대로 쓴다
    eps_path = os.environ.get("EPS_HISTORY", "")
    eps = []
    if eps_path and os.path.exists(eps_path):
        # 일회성 세금을 뺀 EPS — 항목은 그 분기 실적과 같은 공시에서 밝혀지므로 같은 시점에 반영한다
        eps = [{"available": e["available_date"],
                "val": e["ttm_eps"] + oneoff_in_ttm(t, e.get("quarter_end"), "eps")}
               for e in json.load(open(eps_path)) if e.get("ttm_eps")]
        eps.sort(key=lambda e: e["available"])

    series = {}
    for name, tags in FLOW_TAGS.items():
        tag, rows = pick_tag(cik, tags)
        if not rows:
            print(f"  {name}: 태그 없음")
            continue
        q = quarterly_flow(rows, t)
        series[name] = ttm_series(q)
        stale = check_fresh(series[name], daily[-1][0])
        print(f"  {name}: {tag} — 분기 {len(q)}개 → TTM {len(series[name])}개"
              f" · 최신 {series[name][-1]['end'] if series[name] else '없음'}{stale}")
    for name, tags in INSTANT_TAGS.items():
        if name == "shares":
            # CommonStockSharesOutstanding은 us-gaap, EntityCommonStockSharesOutstanding은
            # dei에 산다. 둘 다 dei로 조회하면 앞의 것은 영영 안 잡힌다(Codex 지적).
            # 반대로 us-gaap만 쓰면 연 1회 10-K에만 실려 8개월씩 낡는다. 둘은 같은
            # 수량을 다른 곳에서 보고하는 것이므로 **합산이 아니라 병합**한다.
            t1, r1 = pick_tag(cik, ["CommonStockSharesOutstanding"], "us-gaap")
            t2, r2 = pick_tag(cik, ["EntityCommonStockSharesOutstanding"], "dei")
            tag = "+".join(x for x in (t1, t2) if x)
            rows = r1 + r2
            if cik in SHARES_WA_FALLBACK:
                # 기말 주식 수가 시작되기 전 구간만 분기(약 3개월) 가중평균 기본 주식 수로 채운다(종목 예외)
                from datetime import date as _d
                _, rw = pick_tag(cik, ["WeightedAverageNumberOfSharesOutstandingBasic"], "us-gaap")
                first = min((r["end"] for r in r2 if "start" not in r), default="9999-12-31")   # 표지(dei) 주식 수가 시작되기 전
                extra = [{k: v for k, v in r.items() if k != "start"} for r in rw if "start" in r and r["end"] < first
                         and 80 <= (_d.fromisoformat(r["end"]) - _d.fromisoformat(r["start"])).days <= 100]
                rows = rows + extra
                tag += f"+분기 가중평균 기본 {len(extra)}개({first} 전)"
        else:
            tag, rows = pick_tag(cik, tags, "us-gaap")
        if not rows:
            print(f"  {name}: 태그 없음")
            continue
        series[name] = instant_series(rows, t, is_share_count=(name == "shares"))
        stale = check_fresh(series[name], daily[-1][0])
        print(f"  {name}: {tag} — 시점 {len(series[name])}개"
              f" · 최신 {series[name][-1]['end'] if series[name] else '없음'}{stale}")

    # EV 구성요소(시점)와 EBITDA(기간)
    for name, tags in EV_COMPONENTS.items():
        series[name] = ev_component(cik, name, tags)
        if series[name]:
            print(f"  {name}: {len(series[name])}개 · 최신 {series[name][-1]['end']}"
                  f"{check_fresh(series[name], daily[-1][0])}")
        else:
            print(f"  {name}: 없음 (0으로 본다)")
    for name, tags in EBITDA_TAGS.items():
        if name == "dda":
            tag, q = dda_quarters(cik, t)
            if not q:
                print("  dda: 태그 없음")
                series[name] = []
                continue
        else:
            tag, rows = pick_tag(cik, tags)
            if not rows:
                print(f"  {name}: 태그 없음")
                series[name] = []
                continue
            q = quarterly_flow(rows, t)
        series[name] = ttm_series(q)
        print(f"  {name}: {tag} — 분기 {len(q)}개 → TTM {len(series[name])}개"
              f" · 최신 {series[name][-1]['end'] if series[name] else '없음'}"
              f"{check_fresh(series[name], daily[-1][0])}")

    core = t in core_tickers()
    if core:
        # 공시 순이익에 투자 평가이익이 크게 섞인 종목은 PER을 본업 이익으로 낸다.
        # GOOGL 2026 Q2: 영업이익 $40.8B, 영업외이익 $98.0B, 희석 EPS $9.11(본업만 약 $2.7).
        for name, tags in CORE_TAX_TAGS.items():
            tag, rows = pick_tag(cik, tags)
            series[name] = ttm_series(quarterly_flow(rows, t)) if rows else []
            if name == "pretax" and not series[name]:
                # 세전이익을 연간에만 태그한 회사(MRVL)는 분기 세전 = 순이익 + 법인세로 만든다 — build_dcf.base_inputs와 같은 대체(2026-10-01)
                _, nr = pick_tag(cik, ["NetIncomeLoss"]); _, tr = pick_tag(cik, CORE_TAX_TAGS["tax"])
                nq = {e["end"]: e for e in quarterly_flow(nr, t)}; tq = {e["end"]: e for e in quarterly_flow(tr, t)}
                merged = [dict(nq[k], val=nq[k]["val"] + tq[k]["val"], filed=max(nq[k]["filed"], tq[k]["filed"])) for k in sorted(nq) if k in tq]
                series[name] = ttm_series(merged)
                tag = "NetIncomeLoss + 법인세(분기 세전 태그 없음)"
            print(f"  {name}: {tag} — TTM {len(series[name])}개 (본업 기준 PER용)")

    def core_earnings(d):
        """그날 공개돼 있던 최근 4분기 본업 이익 = 영업이익 × (1 − 법인세/세전이익), 같은 분기끼리."""
        parts = {n: [e for e in series.get(n, []) if e["available"] <= d] for n in ("opinc", "tax", "pretax")}
        if not all(parts.values()):
            return None
        common = set.intersection(*({e["end"] for e in v} for v in parts.values()))
        if not common:
            return None
        end = max(common)
        lead = max(v[-1]["end"] for v in parts.values())
        if (date.fromisoformat(lead) - date.fromisoformat(end)).days > MAX_PAIR_LAG_DAYS:
            return None
        o, tx, pt = ([e for e in parts[n] if e["end"] == end][-1]["val"] for n in ("opinc", "tax", "pretax"))
        if pt <= 0 or o <= 0:
            return None
        r = tx / pt
        # 종목 예외(core_earnings.json "statutory_fallback"): 세율이 0~40% 밖이면 법정 21%. GEV는 세금 평가충당금 환입
        # $2.9B로 최근 4분기 세율이 −20.8%라 본업 이익이 영업이익보다 컸다(Codex·Fable, 2026-10-01). 전 종목 적용은
        # ABBV·PANW 점수를 바꿔 100장 뒤 안건으로 미룬다.
        if core_tickers().get(t, {}).get("statutory_fallback") and not 0.0 <= r <= 0.40:
            r = 0.21
        return o * (1 - r)

    out = {"ticker": t, "window": [daily[0][0], daily[-1][0]], "multiples": {},
           "perBasis": "core" if core else "diluted"}
    defs = {
        "PER": (lambda d, px: (mcap(d, px) / core_earnings(d)) if mcap(d, px) and core_earnings(d) else None) if core
        else (lambda d, px: px * fx.rate(t, d) / as_of(eps, d) if eps and as_of(eps, d) and as_of(eps, d) > 0 else None),
        "PSR": lambda d, px: mcap(d, px) / as_of(series.get("revenue", []), d)
        if mcap(d, px) and as_of(series.get("revenue", []), d) else None,
        "PBR": lambda d, px: mcap(d, px) / as_of(series.get("equity", []), d)
        if mcap(d, px) and as_of(series.get("equity", []), d) else None,
        "PCR": lambda d, px: (mcap(d, px) / fcf(d)) if mcap(d, px) and fcf(d) and fcf(d) > 0 else None,
        "EV/EBITDA": lambda d, px: (ev(d, px) / ebitda(d))
        if ev(d, px) and ebitda(d) and ebitda(d) > 0 else None,
    }

    def mcap(d, px):
        # 재무가 현지 통화(TSM 대만달러)면 달러 가격을 그날 환율로 바꿔 같은 통화끼리 나눈다(v2/fx.py).
        sh = as_of(series.get("shares", []), d)
        return px * fx.rate(t, d) * sh if sh else None

    def ev(d, px):
        m = mcap(d, px)
        if not m:
            return None
        cash = (as_of(series.get("cash", []), d) or 0) + (as_of(series.get("sti", []), d) or 0)
        debt = (as_of(series.get("debt", []), d) or 0) + (as_of(series.get("lease", []), d) or 0)
        extra = (as_of(series.get("nci", []), d) or 0) + (as_of(series.get("preferred", []), d) or 0)
        return m + debt - cash + extra

    def ebitda(d):
        o, a = paired("opinc", "dda", d)
        return (o + a) if (o is not None and a is not None) else None

    def paired(name_a, name_b, d):
        """두 시리즈에서 **같은 분기**의 값만 짝지어 돌려준다.

        영업현금흐름은 2분기까지 반영됐는데 설비투자는 1분기에 멈춰 있으면
        그대로 빼도 숫자는 나오지만 서로 다른 기간을 섞은 값이다(Codex 지적).
        """
        ea = [e for e in series.get(name_a, []) if e["available"] <= d]
        eb = [e for e in series.get(name_b, []) if e["available"] <= d]
        if not ea or not eb:
            return None, None
        if ea[-1]["end"] != eb[-1]["end"]:
            # 한쪽이 앞서 있으면 둘 다 가진 가장 최근 분기로 맞춘다
            common = {x["end"] for x in ea} & {x["end"] for x in eb}
            if not common:
                return None, None
            end = max(common)
            # 그 분기가 앞선 쪽의 최신 분기보다 한참 뒤처지면 쓰지 않는다.
            # NVDA는 2021~2023년 10-Q에서 설비투자를 회사 전용 태그(nvda:)로
            # 보고했고 companyfacts는 그 태그를 주지 않는다. 그 동안 짝이 맞는
            # "가장 최근" 분기를 찾다가 2012-10-28까지 거슬러 가서, 10년 전
            # FCF $0.6B를 2021~2024년 주가의 분모로 썼다(PCR 910배, 5년 중앙값
            # 64.97 → 381, 2026-09-23 발견). 그런 날은 값을 내지 않는다.
            lead = max(ea[-1]["end"], eb[-1]["end"])
            if (date.fromisoformat(lead) - date.fromisoformat(end)).days > MAX_PAIR_LAG_DAYS:
                return None, None
            ea = [x for x in ea if x["end"] == end]
            eb = [x for x in eb if x["end"] == end]
        return ea[-1]["val"], eb[-1]["val"]

    def fcf(d):
        o, c = paired("ocf", "capex", d)
        return (o - c) if (o is not None and c is not None) else None

    # 오늘 배수가 없을 때 적자(분모 0 이하)인지 가르는 분모. 본업 PER은 core_earnings가
    # 적자면 None을 돌려 가를 수 없어 넣지 않는다.
    DENOMS = {"PCR": fcf, "EV/EBITDA": ebitda,
              "PSR": lambda d: as_of(series.get("revenue", []), d),
              "PBR": lambda d: as_of(series.get("equity", []), d)}
    if not core:
        DENOMS["PER"] = lambda d: as_of(eps, d) if eps else None

    for label, fn in defs.items():
        pts = []
        for b in daily:
            try:
                v = fn(b[0], b[4])
            except Exception:
                v = None
            if v and v > 0:
                pts.append((b[0], v))
        if not pts:
            print(f"  {label}: 계산 불가")
            continue
        vals = [v for _, v in pts]
        cur = pts[-1][1]
        srt = sorted(vals)
        # 오늘 값이 없으면 마지막 양수 날의 값을 "현재"로 쓰면 안 된다(Codex 지적, 2026-09-24 AMZN:
        # TTM FCF −$11.6B인데 과거 양수일의 PCR 367x가 현재로 실렸다). 오늘 분모가 0 이하면
        # 가장 비싼 것과 같게 0점(사용자 결정, 동종업도 적자를 꼴찌로 센다), 분모 자체를 못 구하면
        # 점수를 내지 않아 평균에서 빠진다.
        stale_note = None
        if pts[-1][0] != daily[-1][0]:
            dfn = DENOMS.get(label)
            dv = dfn(daily[-1][0]) if dfn else None
            stale_note = "negative" if (dv is not None and dv <= 0) else "missing"

        def q(p):
            i = (len(srt) - 1) * p
            lo = int(i)
            hi = min(lo + 1, len(srt) - 1)
            return srt[lo] + (srt[hi] - srt[lo]) * (i - lo)

        pr = percentile_rank(vals, cur)
        if stale_note:
            cur, pr = None, 100.0
        out["multiples"][label] = {
            "days": len(pts), "current": round(cur, 2) if cur is not None else None,
            "min": round(srt[0], 2), "p10": round(q(.10), 2), "median": round(q(.50), 2),
            "p90": round(q(.90), 2), "max": round(srt[-1], 2),
            # 평균도 같이 낸다. 기본적 분석 점수의 밸류에이션 축이 "현재값이 5년
            # 평균에서 몇 % 떨어졌나"로 단계를 매기기 때문이다(build_fundamental_score).
            # 중앙값이 아니라 평균인 것은 그 산식이 그렇게 정의돼 있어서다.
            "mean": round(sum(vals) / len(vals), 2),
            "percentile": round(pr, 1),
            "score": None if stale_note == "missing" else round(100 - pr, 1),
        }
        if stale_note:
            out["multiples"][label]["currentNote"] = stale_note
        if label == "PER" and not stale_note:
            # 적정주가 밴드 — 최근 252거래일 PER의 p25~p75 × 현재 EPS, $10 반올림.
            # EPS_now = P_now / PER_now이므로 현재가 × (분위 PER ÷ 현재 PER)로 같다.
            # (2026-09-24 손값에서 스크립트로. NVDA $260~$370·AAPL $300~$330 재현)
            # 창은 **최근 252거래일**(일봉 날짜 기준)이다. 계산에 성공한 마지막 252개로 잡으면
            # 결측 구간이 있을 때 창이 과거로 늘어난다. 오늘 PER이 없으면 밴드를 내지 않는다(Codex).
            start_day = daily[-252][0] if len(daily) >= 252 else daily[0][0]
            yr = sorted(v for dd, v in pts if dd >= start_day)
            def yq(p):
                i = (len(yr) - 1) * p; lo = int(i); hi = min(lo + 1, len(yr) - 1)
                return yr[lo] + (yr[hi] - yr[lo]) * (i - lo)
            px_now = daily[-1][4]
            lo_px, hi_px = px_now * yq(.25) / cur, px_now * yq(.75) / cur
            out["fairBand"] = {"per_p25": round(yq(.25), 2), "per_p75": round(yq(.75), 2),
                               "low": int(round(lo_px / 10) * 10), "high": int(round(hi_px / 10) * 10),
                               "asOf": daily[-1][0], "basis": out["perBasis"]}
            print(f"  적정주가 밴드: PER {yq(.25):.1f}~{yq(.75):.1f}x → ${out['fairBand']['low']}~${out['fairBand']['high']}"
                  f" ({out['perBasis']})")
        m = out["multiples"][label]
        if stale_note:
            print(f"  {label}: 오늘 값 없음 ({'분모 0 이하 → 0점' if stale_note == 'negative' else '분모를 못 구함 → 평균에서 뺌'})")
            continue
        print(f"  {label}: 현재 {m['current']}  (최저 {m['min']} · 중앙 {m['median']} · 최고 {m['max']})"
              f"  하위 {m['percentile']}%  → 점수 {m['score']}  [{m['days']}일]")

    if args.json:
        json.dump(out, open(args.json, "w"), ensure_ascii=False, indent=1)
        print("저장:", args.json)


if __name__ == "__main__":
    main()
