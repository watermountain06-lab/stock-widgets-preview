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
import time
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import fetch_eps_history as feh  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fx  # noqa: E402  재무 통화가 달러가 아닌 종목(TSM)의 환율
import eps_oneoff as _eo  # noqa: E402  일회성 손익 장치(안건 E54) — 함수 안에서만 이 모듈을 되부른다
import common_equity  # noqa: E402  보통주 자본(안건 E44)
import share_claims as _sc  # noqa: E402  카드별 전환·교환 증권 표(안건 E44 §3)

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
DDA_PARTS_BY_CIK = {"0000310158": ["Depreciation", "AdjustmentForAmortization"],
                    "0000922224": ["Depreciation", "AdjustmentForAmortization"],   # PPL: 손익계산서 감가상각 + 현금흐름표 상각(규제자산·무형, 상반기 $65M) — 감가상각만 읽으면 EBITDA에서 상각이 빠진다(2026-10-30)
                    # GRMN: 합산 태그 없음 — 감가상각 + 상각(AdjustmentForAmortization, 분기 약 $10M; AmortizationOfIntangibleAssets는 연간만, Fable·Codex r1 2026-10-28)
                    "0001121788": ["Depreciation", "AdjustmentForAmortization"],
                    # AEP: 분기 감가상각은 손익계산서·현금흐름표가 함께 쓰는 유틸리티 비용 태그뿐 — 합산 태그 분기 행이 2011년에 멈춰 TTM이 2025 연간값에 묶였다(2026-10-28)
                    "0000004904": ["UtilitiesOperatingExpenseDepreciationAndAmortization"],
                    # GD: 합산 태그 DepreciationAndAmortization이 2019~2023 분기에 없어 EV/EBITDA 이력이 251일뿐이었다 — 감가상각 + 무형자산 상각. 금융리스 사용권 상각은 연간 태그뿐이라 빠져 회사 합계보다 7~11% 작다(FY21~25, Fable r1 2026-10-25)
                    "0000040533": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # HII: 합산 태그는 분기 행이 2024년부터 — 감가상각 + 무형자산 상각(FY20~25 연간 합 일치, 2026-10-25)
                    "0001501585": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # AVY: 합산 태그는 분기 행이 2024년부터라 EV/EBITDA 이력이 249일뿐이었다 — 감가상각 + 무형자산 상각(5년 전 구간). 소프트웨어 상각(연 약 $30M, 합산의 약 9%)은 표준 태그가 없어 빠진다(2026-10-25)
                    "0000008818": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # NDSN: 10-K가 합산 태그에 무형자산 상각만 싣는 해가 있다(FY25 79.3 = 상각, 9개월 누계 112.5보다 작음 → 4분기 −33.2) — 감가상각 + 상각(FY21~24 합 일치, 2026-10-25) [엔진수정대기]
                    "0000072331": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # IEX: 합산 태그가 2024-09에 멈춤 — 감가상각 + 무형자산 상각(FY20~23 연간 합 일치, 2026-10-25)
                    "0000832101": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # XYL: 합산 태그가 2024-09에 멈춤(연간만 2025) — 감가상각 + 무형자산 상각(FY20~25 연간 합 일치, 2026-10-25)
                    "0001524472": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # CHD: 합산 태그가 2026-03에 멈춤(누계는 2025-09) — 감가상각 + 상각(FY2025 89.7 + 157.7 = 247.4, 2026-10-25)
                    "0000313927": ["Depreciation", "AdjustmentForAmortization"],
                    # IR: 합산 태그는 분기 행이 2024년부터 — 무형자산 상각 + 매출원가 감가상각(FY21~25 연간 합이 합산 태그와 정확히 같다, 2026-10-25)
                    "0001699150": ["AmortizationOfIntangibleAssets", "CostOfGoodsAndServicesSoldDepreciation"],
                    # WST: 합산 태그는 분기 행이 2024년부터라 EV/EBITDA 이력이 252일뿐이었다 — 감가상각 + 상각(2021~, Codex r1 2026-10-25)
                    "0000105770": ["Depreciation", "AdjustmentForAmortization"],
                    # MTD: 현금흐름표 D&A = 감가상각 + "Amortization"(AmortizationOfDeferredCharges — 무형자산·소프트웨어 포함, FY25 $74.5M). 무형자산 상각 태그는 그 안의 일부(Fable r1 2026-10-25)
                    "0001037646": ["Depreciation", "AmortizationOfDeferredCharges"],
                    # TTWO: DepreciationDepletionAndAmortization(Q1 FY27 $48.2M)는 유형자산분만 — 현금흐름표 "무형자산 상각·손상"(회사 고유 태그 →
                    # BUILD company_tags → AmortizationAndImpairmentOfIntangibleAssetsTtwo, Q1 FY27 $168.5M)을 더한다. 표준 AmortizationOfIntangibleAssets는 10-K 연간뿐(2026-10-24)
                    "0000946581": ["DepreciationDepletionAndAmortization", "AmortizationAndImpairmentOfIntangibleAssetsTtwo"],
                    # FIX: DepreciationAndAmortization는 FY2025 10-K 한 해($62.4M, 감가상각만)뿐 — 감가상각 + 무형자산 상각(Q3 2026 21.9 + 25.7)으로(2026-10-24)
                    "0001035983": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # MSCI: DepreciationDepletionAndAmortization는 유형자산 감가상각만($23M/년) — 손익계산서 '무형자산 상각'(인수 무형자산 + 자본화 소프트웨어, Q3 2026 $45M)을 더한다(2026-10-23)
                    "0001408198": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # CIEN: 현금흐름표 무형자산 상각($35.4M, FY26 9개월)은 회사 고유 태그(BUILD company_tags → AmortizationOfIntangibleAssetsCashFlowCien)뿐이고
                    # 표준 AmortizationOfIntangibleAssets는 영업비용 몫($12.2M)만이다 — 감가상각 + 현금흐름표 상각(TTM 129.8 + 45.2 = 175.1, Codex r1, 2026-10-23)
                    "0000936395": ["Depreciation", "AmortizationOfIntangibleAssetsCashFlowCien"],
                    # TER: 합산 태그 DepreciationDepletionAndAmortization는 분기 행이 2024-03부터만이라 EV/EBITDA 이력이 246일뿐이었다 —
                    # 구성요소 Depreciation + AmortizationOfIntangibleAssets(2008~; 2026 상반기 58.9 + 7.2 = 66.1 ≈ 합산 66.3, Fable r1, 2026-10-23)
                    "0000097210": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # VRT: 합산 태그 DepreciationDepletionAndAmortization는 분기 행이 듬성듬성해(2021-12부터 13개) EV/EBITDA 이력이 250일뿐이었다 —
                    # 현금흐름표 구성요소 Depreciation + AmortizationOfIntangibleAssets(2021~ 22개; 2026 상반기 66.9 + 156.6 = 223.5 = 합산 태그, 2026-10-21).
                    "0001674101": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # PKG: 합산 태그 DepreciationDepletionAndAmortization가 2015~2023년에 없어(분기 33개) EV/EBITDA 이력이 252일뿐이었다 —
                    # 현금흐름표 구성요소 Depreciation + AmortizationOfIntangibleAssets(2013~ 55개; 2026-09 분기 162.4 + 18.4 = 180.8 ≈ 합산 181.3, 2026-11-07).
                    "0000075677": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # CTAS: 합산 태그 DepreciationDepletionAndAmortization는 분기 행이 듬성듬성해(24개) EV/EBITDA 이력이 138일뿐이었다 —
                    # 현금흐름표 Depreciation + "Amortization"(AdjustmentForAmortization — 계약 비용 상각 포함; AmortizationOfIntangibleAssets는 Q1 FY27에 무형자산만 14.9로 좁아짐) = 78.9 + 48.4 = 127.3 = 합산 태그(2026-10-22).
                    "0000723254": ["Depreciation", "AdjustmentForAmortization"],
                    # COR: 합산 태그 DepreciationDepletionAndAmortization는 22개뿐이라 EV/EBITDA 이력이 55일이었다 — 손익계산서 "Depreciation"(DepreciationNonproduction)
                    # + "Amortization"(AmortizationOfIntangibleAssets) = 9개월 FY26 417.4 + 361.8 = 779.2 = 합산 태그(2026-10-22). Depreciation(432.0)은 다른 범위라 쓰지 않는다.
                    "0001140859": ["DepreciationNonproduction", "AmortizationOfIntangibleAssets"],
                    # AON: 무형자산 상각을 2022-12부터 회사 고유 태그 aon:AmortizationAndImpairmentOfIntangibleAssets(손상 포함)로만 낸다 — BUILD company_tags가
                    # AmortizationOfIntangibleAssets 이름으로 overlay에 싣는다. 기본 D&A는 감가상각 $190M뿐이었다. 상반기 2026: 95 + 326 = 421(2026-10-22).
                    "0000315293": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # TDG: 합산 태그 DepreciationDepletionAndAmortization는 30개뿐이라 EV/EBITDA 이력이 56일이었다 — 현금흐름표 Depreciation + AmortizationOfIntangibleAssets
                    # (9개월 FY26 137 + 185 = 322, 합산 태그 324 — 제품 인증 비용 상각 2 차이, 2026-10-22).
                    "0001260221": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # FAST: 합산 D&A 태그는 10-K 4개뿐이라 EV/EBITDA를 아예 못 냈다 — 현금흐름표 Depreciation + AmortizationOfIntangibleAssets(9개월 2026 126.9 + 8.2, 2026-10-22).
                    "0000815556": ["Depreciation", "AmortizationOfIntangibleAssets"],
                    # CME: 손익계산서 "Depreciation and amortization" 줄을 10-Q는 Depreciation, 10-K 연간은 DepreciationAndAmortization으로 낸다 —
                    # 둘을 한 구성요소로 합쳐야 4분기가 생긴다(없으면 4분기 감가상각이 빠져 TTM이 $233M, 2026-10-16). 무형자산 상각은 따로.
                    "0001156375": [("Depreciation", "DepreciationAndAmortization"), "AmortizationOfIntangibleAssets"],
                    # NKE: 현금흐름표 "Depreciation" 줄 태그가 Depreciation(~2025-02) → DepreciationDepletionAndAmortization(2023-05~)으로 바뀌었다 — 겹치는 기간 값 같음.
                    # 기본 선택은 새 태그 9분기만 잡아 EV/EBITDA 이력이 138일뿐이었다(2026-10-17).
                    "0000320187": [("Depreciation", "DepreciationDepletionAndAmortization")],
                    # CSX: 손익계산서 "Depreciation and Amortization" 줄을 2022년 10-Q까지 Depreciation, 그 뒤(2021 비교부터) DepreciationDepletionAndAmortization으로.
                    # 새 태그만 쓰면 2021년 분기 공개일이 1년 뒤 비교 수치로 밀려 EV/EBITDA 이력이 921일이었다. 분기 값은 겹치는 기간 같다. 새 태그를 앞에 —
                    # Depreciation의 FY2022 연간 80은 다른 줄 값이라 같은 날(2023-02-15) 공시된 새 태그 1,500이 이겨야 한다(2026-10-18).
                    "0000277948": [("DepreciationDepletionAndAmortization", "Depreciation")],
                    # MRSH: 현금흐름표 "Depreciation and amortization of fixed assets and capitalized software"를 2023년까지 Depreciation, 2024년부터
                    # DepreciationDepletionAndAmortization으로(분기 약 $90M). 2021~2023 10-K의 DepreciationDepletionAndAmortization 연간에는 무형자산 상각을
                    # 합친 값(2021 747 = 382 + 365)이 섞여 있어 Depreciation을 앞에. "Amortization of intangible assets"(분기 약 $140M)는 따로 —
                    # 합산 태그만 쓰면 무형자산 상각이 빠지고 분기가 2024년부터라 EV/EBITDA가 252일이었다(2026-10-18).
                    "0000062709": [("Depreciation", "DepreciationDepletionAndAmortization"), "AmortizationOfIntangibleAssets"],
                    # CEG: 기본 선택(현금흐름표 DepreciationAmortizationAndAccretionNet, 2026 상반기 $2,368M)에는 Calpine 인수 파생계약 상각($423M — 매출 차감)·
                    # ARO 부채 증가분($338M)·인수 에너지 계약(UEC) 상각($240M)이 섞여 있다. 손익계산서 "Depreciation and amortization" 줄($886M = 고정자산 $870M +
                    # 무형자산 $16M) + 핵연료 상각(AmortizationOfNuclearFuelLease $496M, 연료비 안 — 핵연료 구입은 설비투자 줄에 있다, 10-Q 보충 현금흐름 표, 2026-10-18).
                    "0001868275": ["CostOfGoodsAndServicesSoldDepreciationAndAmortization", "AmortizationOfNuclearFuelLease"],
                    # INTU: 기본 선택 AmortizationOfIntangibleAssets는 "기타 인수 무형자산 상각"($485M)뿐 — 매출원가 안 "인수 기술 상각"($174M)이 빠졌다.
                    # 현금흐름표 "Amortization of acquired intangible assets"(AdjustmentForAmortization, FY26 $659M = 174 + 485)로(MRK와 같은 구성, 2026-10-18).
                    "0000896878": ["Depreciation", "AdjustmentForAmortization"],
                    # BRO: 감가상각 + 무형자산 상각(현금흐름표 두 줄, Q3 2026 18 + 110) — 합산 태그 없음(2026-11-05)
                    "0000079282": ["Depreciation", "AdjustmentForAmortization"],
                    # JKHY: 감가상각 42.1 + 상각 171.1(소프트웨어·고객관계) = FY26 213.2 — 합산 태그 없음(2026-11-05)
                    "0000779152": ["Depreciation", "AdjustmentForAmortization"]}
# 태그 의미가 도중에 바뀐 회사의 합산 감가상각(CIK). AMD의 OtherDepreciationAndAmortization(현금흐름표
# "Depreciation and amortization")은 FY2024 10-K(2025-02-05) 전까지 인수 무형자산 상각을 **포함한** 합계였고,
# 그 뒤로는 상각을 AmortizationOfIntangibleAssets 줄로 떼어 낸다(Fable, 2026-09-27). 분할 뒤 공시의 행에만
# 같은 (start, end, accn)의 상각을 더해 한 줄기 합산 시리즈로 만든다. Depreciation 태그는 10-K 연간(설비만)뿐이다.
# (처음엔 두 태그를 구성요소로 더했다가 2023~24년이 이중 계상되고 2024 Q4가 음수가 됐다.)
DDA_SPLIT_BY_CIK = {"0000002488": {"total": "OtherDepreciationAndAmortization", "add": "AmortizationOfIntangibleAssets",
                                   "split_from": "2025-02-05"},
                    # VRSK: DepreciationAndAmortization은 고정자산 감가상각뿐이고 무형자산 상각(TTM $64.1M)은 AmortizationOfIntangibleAssets로 따로 낸다 —
                    # 합계 태그로 오인해 EBITDA에서 상각이 빠졌다(EV/EBITDA 17.64 → 16.98배, Codex r1 2026-10-30). 전 기간 같은 구조라 처음부터 더한다.
                    "0001442145": {"total": "DepreciationAndAmortization", "add": "AmortizationOfIntangibleAssets", "split_from": "2000-01-01"},
                    # VLTO: DepreciationDepletionAndAmortization은 부문표 분기 값뿐이라 EV/EBITDA 이력이 253일만 잡혔다 — 감가상각 + 무형 상각(Codex r1, 2026-10-30)
                    "0001967680": {"total": "Depreciation", "add": "AmortizationOfIntangibleAssets", "split_from": "2000-01-01"},
                    # BEN: DepreciationDepletionAndAmortization(현금흐름표 "Depreciation and other amortization", FY25 $125.3M)은 무형자산 상각($406.5M)을 뺀 값 — 2018년부터 늘 따로 낸다(Codex r1, 2026-11-04)
                    "0000038777": {"total": "DepreciationDepletionAndAmortization", "add": "AmortizationOfIntangibleAssets", "split_from": "2000-01-01"},
                    # GNRC: 합산 태그 DepreciationDepletionAndAmortization에 2026년 1분기 행이 없어(반기·9개월 누계와 2분기만) 최근 4분기 EV/EBITDA가 비었다 — 감가상각 + 무형자산 상각(Q1 2026 25.6 + 30.4 = 반기 − 2분기 56.0, 2026-11-08)
                    "0001474735": {"total": "Depreciation", "add": "AmortizationOfIntangibleAssets", "split_from": "2000-01-01"}}


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


DISC_EPS_TAGS = ["IncomeLossFromDiscontinuedOperationsNetOfTaxPerDilutedShare",
                 "DiscontinuedOperationIncomeLossFromDiscontinuedOperationNetOfTaxPerDilutedShare",
                 "IncomeLossFromDiscontinuedOperationsNetOfTaxPerBasicAndDilutedShare"]
CONT_EPS_TAGS = ["IncomeLossFromContinuingOperationsPerDilutedShare", "IncomeLossFromContinuingOperationsPerBasicAndDilutedShare"]
TOTAL_EPS_TAGS = ["EarningsPerShareDiluted", "EarningsPerShareBasicAndDiluted"]
_PS_CACHE = {}


def _ps_facts(ticker, tags):
    """그 종목 주당 값 기간 사실 — (start, end, val(오늘 주식 기준, 분할 보정), filed). 같은 기간은 먼저 공시된 것(같은 날이면 앞 태그)."""
    key = (ticker, tuple(tags))
    if key not in _PS_CACHE:
        cik = feh.CIKS.get(ticker)
        import splits as _splits
        sp = _splits.for_ticker(ticker)
        seen = {}
        if cik:
            got = [e for tg in tags for e in concept(cik, tg) if "start" in e and "filed" in e]
            for e in sorted(got, key=lambda e: e["filed"]):   # 정렬은 안정적 — 같은 공시일이면 태그 목록 순서
                seen.setdefault((e["start"], e["end"]), e)
        # 주당 값이 1,000달러를 넘는 사실은 단위 오태깅(DELL 2020~2022 ×1e6) — 버린다(Fable E62 r1)
        _PS_CACHE[key] = [(e["start"], e["end"], e["val"] / (feh.split_ratio(e["filed"], sp) if sp else 1), e["filed"]) for e in seen.values()
                          if abs(e["val"]) <= 1000]
    return _PS_CACHE[key]


def _disc_facts(ticker):
    return _ps_facts(ticker, DISC_EPS_TAGS)


def ps_quarter(ticker, tags, q_end, upto):
    """결산일 q_end 분기의 주당 값(upto까지 공시된 사실만) — 3개월 값, 없으면 회계연도 누계 − 직전 누계(4분기 = 연간 − 9개월 — 기간별 가중평균
    주식 수가 달라 근사, Codex E62 r1: MPC 2021 4분기 중단영업 0.20 대 회사 분기표 0). 없으면 None."""
    facts = _ps_facts(ticker, tags)
    rows = [r for r in facts if r[1] == q_end and r[3] <= upto]
    days = lambda r: (date.fromisoformat(r[1]) - date.fromisoformat(r[0])).days
    q = [r for r in rows if 80 <= days(r) <= 100]
    if q:
        return min(q, key=lambda r: r[3])[2]
    for y in sorted((r for r in rows if days(r) > 100), key=days):
        prev = [r for r in facts if r[0] == y[0] and r[3] <= upto and 80 <= (date.fromisoformat(y[1]) - date.fromisoformat(r[1])).days <= 100]
        if prev:
            return y[2] - min(prev, key=lambda r: r[3])[2]
    return None


def disc_eps_quarter(ticker, q_end, upto):
    v = ps_quarter(ticker, DISC_EPS_TAGS, q_end, upto)
    return v or 0.0


# E62: 4분기를 보도자료 값으로 손 보정한 행(fetch_eps_history.Q4_EPS_OVERRIDE) 가운데 그 해 중단영업이 큰(|연간| ≥ 0.10) 것의 기준 —
# 'continuing'(보정 값이 계속사업 EPS — 수집기 주석 "계속사업 희석 EPS") 또는 'total'(총 EPS). 없으면 4분기 총·계속영업 역산 중 가까운 쪽.
# 'total'은 보도자료 4분기 중단영업 희석 EPS를 함께 적는다(연간 − 9개월 역산은 주식 수가 급변한 해에 틀림).
# COF 2025: 3.26은 총 EPS, 4분기 중단영업 0.60·계속영업 2.66(8-K 2026-01-22 ex99.2 'Income (loss) from discontinued operations 0.60';
# 역산은 0.70, Discover 합병 주식 수 급변)
Q4_OVERRIDE_BASIS = {
    ("PPL", "2021-12-31"): "continuing", ("VRSK", "2021-12-31"): "continuing", ("VRSK", "2022-12-31"): "continuing",
    ("VRSK", "2023-12-31"): "continuing", ("EBAY", "2021-12-31"): "continuing", ("DVA", "2022-12-31"): "continuing",
    ("DVA", "2025-12-31"): "continuing", ("VMC", "2022-12-31"): "continuing", ("EXC", "2022-12-31"): "continuing",
    ("PPG", "2024-12-31"): "continuing", ("IR", "2021-12-31"): "continuing", ("SNPS", "2024-10-31"): "continuing",
    ("EMR", "2024-09-30"): "continuing", ("COF", "2025-12-31"): ("total", 0.60),
    # D: 2025 4분기 보도자료 EPS 0.65는 총 EPS — 중단영업 −0.01(보도자료 손익계산서, 계속영업 0.66). 자동 역산은 −0.02였다(Codex r1, 2026-11-07)
    ("D", "2025-12-31"): ("total", -0.01),
    # BAX: Q4 2025 덮어쓴 값 −2.01은 계속사업 희석 EPS(보도자료) — 중단사업을 다시 빼지 않는다(2026-11-07)
    ("BAX", "2025-12-31"): "continuing",
    # CARR: Q4 2025 덮어쓴 값은 보도자료 계속사업 희석 EPS 0.03(2026-11-07)
    ("CARR", "2025-12-31"): "continuing",
    # D 2024: 4분기 중단영업 직접값 0(10-K 2025-02-27 CY2024Q4) — 자동 역산은 연간 0.24 − 9개월 당시값 0.22 = 0.02(Codex r2, 2026-11-07)
    ("D", "2024-12-31"): ("total", 0.0),
    # WTW: 중단영업 없음 — 10-K가 연간 총 EPS를 IncomeLossFromDiscontinuedOperationsNetOfTaxPerDilutedShare에도 붙였다(2023 9.95·2024 −0.96·2025 16.26, 2026-11-05)
    ("WTW", "2023-12-31"): "continuing", ("WTW", "2024-12-31"): "continuing", ("WTW", "2025-12-31"): "continuing",
}


def _annual_ps(ticker, tags, fy_end, upto):
    rows = [r for r in _ps_facts(ticker, tags) if r[1] == fy_end and r[3] <= upto
            and 350 <= (date.fromisoformat(r[1]) - date.fromisoformat(r[0])).days <= 380]
    return min(rows, key=lambda r: r[3])[2] if rows else None


def disc_q4_status(ticker, file_rows, upto):
    """4분기 역산 행(fp Q4-derived — 파일 4분기 = 연간 − 앞 세 분기, 또는 보도자료 4분기 값): 분기 비교 대신 **연간**으로 판정한다 —
    파일 네 분기 합(= 그 해 연간)이 연간 총 EPS면 뺄 값 = 연간 중단영업 − 앞 세 분기 중단영업(연말 TTM이 연간 계속영업 EPS와 정확히
    맞는다 — ALL 2021 4.96 + 12.02 = 16.98, MPC 2021 15.24 − 13.22 = 2.02, Fable E62 r1), 연간 계속영업 EPS면 'already'.
    file_rows = 그 회계연도 네 분기 행(마지막이 4분기)."""
    q4 = file_rows[-1]
    fy_end = q4["quarter_end"]
    a_disc = _annual_ps(ticker, DISC_EPS_TAGS, fy_end, upto)
    three = lambda: sum(ps_quarter(ticker, DISC_EPS_TAGS, r["quarter_end"], upto) or 0.0 for r in file_rows[:-1])
    # 연간 0이어도 앞 세 분기에 중단영업이 있으면(분기 간 상쇄 — 1분기 +1·4분기 −1) 4분기에 되돌려야 연말 TTM이 맞다(Codex E62 r2)
    if a_disc is None or (abs(a_disc) < 0.005 and abs(three()) < 0.005):
        return 0.0, "none"
    if fy_end in feh.Q4_EPS_OVERRIDE.get(ticker, {}):
        basis = Q4_OVERRIDE_BASIS.get((ticker, fy_end))
        if basis == "continuing":
            return 0.0, "already"
        if isinstance(basis, tuple) and basis[0] == "total":
            return -basis[1], "removed"
        # 4분기를 보도자료 값으로 손 보정한 행(COF 2025 총 EPS 3.26, SNPS FY24 계속영업 1.79) — 파일 네 분기 합이 연간과 안 맞을 수 있어
        # (합병으로 주식 수 급변 — COF 2.96 대 연간 4.03) 4분기 값을 4분기 총·계속영업 역산과 비교해 가까운 쪽(Fable E62 r1)
        q_tot = ps_quarter(ticker, TOTAL_EPS_TAGS, fy_end, upto)
        q_cont = ps_quarter(ticker, CONT_EPS_TAGS, fy_end, upto)
        if q_tot is not None and q_cont is not None:
            if abs(q4["quarter_eps"] - q_cont) < abs(q4["quarter_eps"] - q_tot):
                return 0.0, "already"
            return -(a_disc - three()), "removed"
        return 0.0, "unknown"
    total = sum(r.get("quarter_eps") or 0 for r in file_rows)
    a_tot = _annual_ps(ticker, TOTAL_EPS_TAGS, fy_end, upto)
    a_cont = _annual_ps(ticker, CONT_EPS_TAGS, fy_end, upto)
    d_tot = abs(total - a_tot) if a_tot is not None else None
    d_cont = abs(total - a_cont) if a_cont is not None else None
    if d_cont is not None and d_cont <= 0.03 and (d_tot is None or d_cont < d_tot):
        return 0.0, "already"
    if d_tot is not None and d_tot <= 0.03:
        return -(a_disc - three()), "removed"
    return 0.0, "unknown"


def disc_quarter_status(ticker, file_q, q_end, upto):
    """(뺄 값, 판정) — EPS 파일의 그 분기 값(file_q)이 총 EPS인지 계속영업 EPS인지 **분기마다** 확인한다(Codex E62 r1 — SNPS는 재작성 목록
    밖인데 FY24 4분기를 계속영업 1.79로 손 보정해 둬서 종목 단위 판정이면 5.35를 두 번 뺐다). 판정: 'none'(중단영업 없음),
    'already'(파일이 이미 계속영업 값), 'removed'(파일이 총 EPS — 중단영업을 뺀다), 'unknown'(가를 수 없음 — 빼지 않음)."""
    disc = ps_quarter(ticker, DISC_EPS_TAGS, q_end, upto)
    if not disc or abs(disc) < 0.005 or file_q is None:
        return 0.0, "none"
    cont = ps_quarter(ticker, CONT_EPS_TAGS, q_end, upto)
    tot = ps_quarter(ticker, TOTAL_EPS_TAGS, q_end, upto)
    d_cont = abs(file_q - cont) if cont is not None else None
    d_tot = abs(file_q - tot) if tot is not None else (abs(file_q - cont - disc) if cont is not None else None)
    if d_cont is not None and d_cont <= 0.011 and (d_tot is None or d_cont < d_tot):   # 가까운 쪽(1센트 안 동률 — Fable)
        return 0.0, "already"
    if d_tot is not None and d_tot <= (0.011 if tot is not None else 0.02):
        return -disc, "removed"
    return 0.0, "unknown"


def _restated_even_split(ticker, rows, q_end, upto):
    """E72(2026-11-07): 재작성 종목(RESTATED_LATEST)에서 그 회계연도 앞 세 분기의 중단영업 주당 사실이 **하나도 없고**(0이 아니라 없음 —
    나중 분사로 과거를 다시 쓰며 연간 값만 냈다) 4분기 판정이 'removed'(연간 전액을 4분기에서 뺌)이면, 그 금액을 네 분기에 고르게 나눈 값.
    MMM 2022(Solventum 분사 2024 재작성): 연간 3.11을 4분기 행 하나에 몰아 2023-03·06·09 TTM에서 주당 약 2.3을 더 뺐다(Fable E54 MMM).
    연중 매각으로 4분기에 몰린 경우(WTW 2021 등)는 재작성 종목이 아니라 해당 없음. 4분기 3개월 중단영업 사실이 따로 있거나 4분기를 손 보정한
    해(Q4_EPS_OVERRIDE)는 실제 4분기 몫을 아니까 나누지 않는다(Codex E72 r1). 나눈 분기는 'removed'로 두어 E54 중단영업 항목이 같은 금액을
    한 번 더 빼지 않게 한다(추정 배분과 E54 항목 금액이 다를 수 있지만 이중 차감이 더 나쁘다). 해당 없으면 None."""
    q4s = {}
    for x in sorted(rows, key=lambda x: x.get("available_date", "")):   # 같은 결산일 4분기 행이 여럿이면 공개일이 가장 늦은 행(Codex E72 r1)
        if str(x.get("fp", "")).startswith("Q4") and x.get("quarter_end") and x.get("available_date", "") <= upto:
            q4s[x["quarter_end"]] = x
    for r4 in q4s.values():
        if not 0 <= (date.fromisoformat(r4["quarter_end"]) - date.fromisoformat(q_end)).days <= 300:
            continue
        if r4["quarter_end"] in feh.Q4_EPS_OVERRIDE.get(ticker, {}):
            return None
        if any(f[1] == r4["quarter_end"] and f[3] <= upto and 80 <= (date.fromisoformat(f[1]) - date.fromisoformat(f[0])).days <= 100
               for f in _ps_facts(ticker, DISC_EPS_TAGS)):
            return None
        prev = sorted({x["quarter_end"] for x in rows if x.get("quarter_end") and x["quarter_end"] < r4["quarter_end"]
                       and x.get("available_date", "") <= upto})[-3:]
        if len(prev) < 3 or (q_end not in prev and q_end != r4["quarter_end"]):
            continue
        if (date.fromisoformat(r4["quarter_end"]) - date.fromisoformat(prev[0])).days > 310:
            return None
        if any(ps_quarter(ticker, DISC_EPS_TAGS, q, upto) is not None for q in prev):
            return None
        by = {}
        for x in sorted(rows, key=lambda x: x.get("available_date", "")):
            if x.get("quarter_end") in prev and x.get("available_date", "") <= upto:
                by[x["quarter_end"]] = x
        if len(by) < 3:
            return None
        v, st = disc_q4_status(ticker, [by[q] for q in prev] + [r4], upto)
        return v / 4 if st == "removed" else None
    return None


def _quarter_status(ticker, rows, r, upto):
    """EPS 파일 행 r(그 분기)의 E62 판정 — 4분기 역산 행은 그 회계연도 네 분기로 연간 판정(disc_q4_status).
    재작성 종목의 '앞 세 분기 사실 없음' 해는 연간 제거액을 네 분기에 고르게(E72, _restated_even_split)."""
    if ticker in feh.RESTATED_LATEST and r.get("quarter_end"):
        v = _restated_even_split(ticker, rows, r["quarter_end"], upto)
        if v is not None:
            return v, "removed"
    if str(r.get("fp", "")).startswith("Q4"):
        prev = sorted({x["quarter_end"] for x in rows if x.get("quarter_end") and x["quarter_end"] < r["quarter_end"]
                       and x.get("available_date", "") <= upto})[-3:]
        if len(prev) == 3 and (date.fromisoformat(r["quarter_end"]) - date.fromisoformat(prev[0])).days <= 310:
            by = {}
            for x in sorted(rows, key=lambda x: x.get("available_date", "")):
                if x.get("quarter_end") in prev and x.get("available_date", "") <= upto:
                    by[x["quarter_end"]] = x
            if len(by) == 3:
                return disc_q4_status(ticker, [by[q] for q in prev] + [r], upto)
    return disc_quarter_status(ticker, r.get("quarter_eps"), r["quarter_end"], upto)


def _disc_upto(ticker, upto):
    """재작성 종목(RESTATED_LATEST)은 EPS 파일 값이 이미 나중 공시 기준이라 판정도 같은 기준(시점 제한 없음) — 아니면 분사 재작성 뒤에야 나온
    중단영업 사실이 시점 필터에 걸려 DHR·MMM·T(파일 = 총 EPS)에서 아무것도 못 뺐다(Fable E62 r1)."""
    return "9999-12-31" if ticker in feh.RESTATED_LATEST else upto


def _ttm_quarter_rows(rows, ttm_end, upto):
    """그 TTM의 구성 4분기(EPS 파일, 공개일 ≤ upto인 행 중 결산일마다 마지막) — 마지막이 ttm_end이고 이웃 간격 120일 안일 때만."""
    by_q = {}
    for r in sorted((r for r in rows if r.get("quarter_end") and r["quarter_end"] <= ttm_end
                     and r.get("available_date", "") <= upto), key=lambda r: r.get("available_date", "")):
        by_q[r["quarter_end"]] = r
    qs = sorted(by_q)[-4:]
    if len(qs) < 4 or qs[-1] != ttm_end:
        return None
    if any((date.fromisoformat(b) - date.fromisoformat(a)).days > 120 for a, b in zip(qs, qs[1:])):
        return None
    return [by_q[q] for q in qs]


def disc_in_ttm(ticker, rows, ttm_end, upto):
    """E62: 카드 PER EPS에서 뺄 중단영업 주당 손익(그 TTM 구성 4분기 중 '총 EPS'로 확인된 분기의 합의 음수) — 엔진 EPS
    (EarningsPerShareDiluted)는 중단영업 손익을 담는다(CARR 2024 Access·Industrial Fire 매각 차익, MPC 2021 Speedway 12.55, ALL 2021
    생명보험 매각). 카드 모드에서만(연구 모드·12-01 봉인 자료는 그대로). 사실은 그 TTM 행 공개일까지 공시된 것만."""
    if ASOF_REF is not None or not _disc_facts(ticker):
        return 0.0
    qr = _ttm_quarter_rows(rows, ttm_end, upto)
    if qr is None:
        return 0.0
    u = _disc_upto(ticker, upto)
    return sum(_quarter_status(ticker, rows, r, u)[0] for r in qr)


def disc_removed(ticker, rows, q_end, upto):
    """그 분기 중단영업을 E62가 실제로 뺐는가(E54 중단영업 항목을 건너뛸지 — Codex E62 r1: 태그 존재가 아니라 그 분기 제거 확인)."""
    if ASOF_REF is not None or not _disc_facts(ticker):
        return False
    r = [x for x in rows if x.get("quarter_end") == q_end and x.get("available_date", "") <= upto]
    if not r:
        return False
    last = max(r, key=lambda x: x.get("available_date", ""))   # 파일 순서가 아니라 공개일 최댓값(GS·MS 파일은 정렬 안 됨 — Fable)
    st = _quarter_status(ticker, rows, last, _disc_upto(ticker, upto))[1]
    # 4분기를 손으로 계속영업 EPS로 보정한 행(Q4_OVERRIDE_BASIS "continuing")은 카드 EPS에 그 분기 중단영업이 없다 — E54가 다시 빼면 안 된다.
    # 예전엔 "removed"만 봐서 CARR Q4 2024(계속영업 −0.05로 보정)에 중단영업 매각 이익 $1,332M이 한 번 더 빠져 PER 최고 1,510배가 됐다.
    # 자동 판정 "already"(역산·연간 합 근사)는 그 분기 중단영업 부재를 보장하지 않아 넣지 않는다(Codex 엔진 검토, 2026-11-07 사용자 결정).
    if st == "already" and q_end in feh.Q4_EPS_OVERRIDE.get(ticker, {}) and Q4_OVERRIDE_BASIS.get((ticker, q_end)) == "continuing":
        return True
    return st == "removed"


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
            total += it.get(field, 0)   # pretax 필드는 세율 분모에서 뺄 비과세 일회성 세전 항목(GEV Prolec, 2026-10-04)
    return total


# A8(2026-10-04 사용자 결정): 본업 이익 = (영업이익 + 순이자) × (1 − 세율). 분자 시가총액이 주주 몫이라 분모도 이자를 낸 뒤의 이익이어야
# 잣대가 맞는다(현금 많은 회사의 이자수익, 빚 많은 회사의 이자비용). 대상 종목은 지금처럼 core_earnings.json 목록 — 자동 문턱은
# S&P500 시점 재현(research/a8_core_prereg.md)에서 양(+) 쪽 C+가 탈락해 보류했다. 태그 규칙은 그 재현과 같다.
NET_INTEREST_TAGS = {
    "net": ["InterestIncomeExpenseNonoperatingNet", "InterestIncomeExpenseNet"],
    "inc": ["InvestmentIncomeInterest", "InterestIncomeOther", "InvestmentIncomeInterestAndDividend", "InterestIncomeNonoperating"],
    "exp": ["InterestExpenseNonoperating", "InterestExpense", "InterestExpenseDebt", "InterestAndDebtExpense"],
}


def net_interest_series(cik, ticker, quarter=False):
    """순이자 계산 재료: 묶음(순액·수익·비용)마다 {분기 결산일: [태그 우선순위 순 분기 항목]}과 공시 행(결산일, 공시일).

    회사가 시기마다 태그를 바꾸므로(CRM 이자비용: FY26까지 InterestExpenseDebt, FY27부터 InterestExpenseNonoperating) 분기마다
    후보를 모두 남기고, 고르는 일은 기준일에 맞춰 net_interest_at이 한다 — 나중 공시의 비교 수치로 생긴 앞 태그가 그때 이미 공개돼 있던
    뒤 태그 값을 가리지 않게(Codex, 2026-10-04). quarter 인자는 호출 쪽 호환용(분기·4분기 합 모두 같은 재료를 쓴다).
    """
    if ticker in LOCAL_HISTORY:
        return None        # SKHY: 어댑터의 InterestExpense는 현금흐름표 "이자의 지급"(현금)이라 발생 기준 순이자가 아니다 — 영업이익만
    out = {}
    for name, tags in NET_INTEREST_TAGS.items():
        byq, raw = {}, []
        for tg in tags:
            _, rows = pick_tag(cik, [tg])
            if not rows:
                continue
            for e in quarterly_flow(rows, ticker):
                byq.setdefault(e["end"], []).append(e)
            raw += [(r["end"], r.get("filed", "")) for r in rows]
        out[name] = (byq, raw)
    return out


def net_interest_at(nis, end, asof="9999-12-31", quarter=False):
    """결산일 end의 순이자(이자수익 − 이자비용) — quarter면 그 분기, 아니면 end로 끝나는 4분기 합.
    순액 태그가 있으면 그것, 없으면 수익 − 비용(그 무렵 태그를 안 쓰는 쪽은 0). 태그는 쓰는데 값을 못 만들면 None(결측) —
    그 종목은 영업이익만으로 계산한다. 분기마다 asof까지 공시된 후보 가운데 우선순위가 가장 높은 태그 값을 쓴다."""
    if not nis:
        return None
    def pick(byq, q_end):
        xs = [e for e in byq.get(q_end, []) if e.get("filed", "") <= asof]
        return xs[0]["val"] if xs else None
    def comp(name):
        byq, raw = nis[name]
        if quarter:
            val = pick(byq, end)
        else:
            ends = [k for k in sorted(byq) if k <= end and any(e.get("filed", "") <= asof for e in byq[k])]
            last4 = ends[-4:]
            val = None
            if len(last4) == 4 and last4[-1] == end and \
                    (date.fromisoformat(end) - date.fromisoformat(last4[0])).days <= 310:
                vals = [pick(byq, k) for k in last4]
                val = sum(vals) if None not in vals else None
        if val is not None:
            return val
        e0 = date.fromisoformat(end)
        near = any(abs((date.fromisoformat(en) - e0).days) <= MAX_PAIR_LAG_DAYS for en, fd in raw if fd <= asof)
        return None if near else "absent"
    net = comp("net")
    if net not in (None, "absent"):
        return net
    a, b = comp("inc"), comp("exp")
    if (a == "absent" and b == "absent") or a is None or b is None:
        return None
    return (0.0 if a == "absent" else a) - (0.0 if b == "absent" else b)


TAX_RATE_ADDBACK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tax_rate_addback.json")


def rate_addback(ticker, cik, end, asof="9999-12-31", quarter=False):
    """세율 분모에 되돌려 더할 반복적 비공제 영업외 항목(v2/tax_rate_addback.json)의 end 분기 값(quarter) 또는 end로 끝나는 4분기 합.
    태그 값이 그 기간에 없으면 0(그 종목 설정이 없을 때와 같다)."""
    if not os.path.exists(TAX_RATE_ADDBACK):
        return 0.0
    cfg = json.load(open(TAX_RATE_ADDBACK)).get(ticker)
    if not cfg:
        return 0.0
    total = 0.0
    for tg in cfg["tags"]:
        _, rows = pick_tag(cik, [tg])
        rows = [r for r in rows if r.get("filed", "") <= asof]   # 원자료를 먼저 거른다 — 유도 분기는 나중 입력의 공시일을 남기지 않는다(Codex)
        q = quarterly_flow(rows, ticker) if rows else []
        if quarter:
            total += next((e["val"] for e in q if e["end"] == end), 0.0)
        else:
            ser = [e for e in ttm_series(q) if e["end"] == end]
            total += ser[-1]["val"] if ser else 0.0
    return cfg.get("sign", 1) * total


# 두 시리즈를 짝지을 때 허용하는 뒤처짐. 한 분기 늦은 보고(약 91일)는 받고,
# 두 분기 이상 비면 버린다.
MAX_PAIR_LAG_DAYS = 200
PER_NA_MARGIN = 0.02   # A3: 최근 4분기 GAAP 순이익률이 이보다 낮으면(적자 포함) PER 해당 없음


CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".sec_cache")
# 이 프로세스에서 이미 새로 받아 본 회사 — 요약 자료에 승인한 공시가 아직 없으면(SEC가 비운 종목, 2026-10-24 KO·XOM·WELL) 아래 조건이
# 늘 참이라 태그마다 다시 받고 큰 파일을 다시 써서 카드 한 장이 10분 걸렸다(build_dcf_grid KO: 191번, 515초 중 약 500초). 한 번만 받는다
_TRIED = set()


# (cik, 승인 공시일, 캐시 파일 표식, overlay 파일 표식, 갱신 실행 표식) → 합친 facts. 한 프로세스가 같은 회사를
# 수천 번 묻는다(build_dcf_track PPG 5,556번 — 승인 공시가 한 분기 더 가면 5,797번) — 그때마다 10MB 캐시를 다시 해석하고 overlay·자르기를 다시 했다.
# 키에 두 파일의 수정 시각·크기와 승인일을 넣어, 그 사이 누가 파일을 다시 쓰거나 기준표를 고치면 새로 만든다. 키의
# 표식은 **그 자료를 읽은 시점**의 것이고, 만드는 동안 파일이 바뀌면 아예 기억하지 않는다
# (서버는 카드 4장이 같은 .sec_cache를 쓴다 — dr r1·r2 Codex·Fable). CACHE_DIR은 프로세스 안에서 상수로 본다.
# 최대 두 칸만 두고 오래 쓰지 않은 것부터 버린다 — 비교 종목까지 도는 실행에서 메모리가 쌓이지 않게.
_FACTS_MEMO = {}
_FACTS_MEMO_HITS = [0, 0]   # [적중, 버림] — 시험·점검용


def _facts(cik):
    """회사의 XBRL 전체(companyfacts)를 **한 번만** 받아 캐시한다.

    태그마다 companyconcept를 부르면 한 종목에 15~20번을 호출하게 되고, 70장을
    돌리면 SEC가 요청 제한을 건다(검증 중 실제로 429에 막혔다). companyfacts는
    같은 내용을 한 번에 주므로 호출이 1/15로 줄고, 캐시가 있으면 0이 된다.
    새로 받으려면 이 디렉터리의 파일을 지운다.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{cik}_facts.json")
    appr = _approved().get(cik)   # 분기 반영을 승인한 공시 제출일(v2/sec_approved.json) — 없으면 캐시 그대로
    ovp = os.path.join(CACHE_DIR, "overlay", f"{cik}.json")
    key = (cik, appr, _stamp(path), _stamp(ovp), os.environ.get("SEC_REFRESH_UNLISTED"))
    if key in _FACTS_MEMO:   # 두 번째부터는 만들어 둔 것을 그대로 — 아래 파일 읽기·overlay·자르기를 다시 하지 않는다
        _FACTS_MEMO[key] = _FACTS_MEMO.pop(key)   # 최근 쓴 것으로(두 칸 LRU)
        _FACTS_MEMO_HITS[0] += 1
        return _FACTS_MEMO[key]
    fst = _stamp(path)   # 지금 읽는 파일의 표식 — 아래에서 받아 다시 쓰면 그때 다시 잡는다
    data = None
    if os.path.exists(path):
        try:
            data = json.load(open(path))
        except Exception:
            data = None
    # 토요일 비교군 갱신(SEC_REFRESH_UNLISTED=세션): 기준표 밖 회사(카드 아닌 비교 종목)는 그 실행에서 한 번 새로 받는다 —
    # 그날까지 나온 실적으로 견준다(2026-10-08 사용자 결정, Codex·Fable 권고). 받기 실패는 옛 캐시를 쓰고 기록만 남긴다.
    # 파일 시각은 Actions 캐시 복원에서 믿을 수 없어 실행 표식으로 센다. 캐시가 없던 회사도 같은 표식을 남긴다(Codex)
    run_id = None if appr else os.environ.get("SEC_REFRESH_UNLISTED")
    done = os.path.join(CACHE_DIR, "_work", f"refreshed_{run_id}.txt")
    stale = bool(run_id) and cik not in (open(done).read().split() if os.path.exists(done) else [])
    if (data is None or stale or (appr and _max_filed(data) < appr)) and cik not in _TRIED:   # 캐시가 없거나 이번 실행에 아직 안 받았거나 기준일보다 앞서면 새로 받는다
        _TRIED.add(cik)
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
        for _try in (1, 2):   # 한 번만 받으므로 일시 오류(429 등)에 한 번 더 — 예전에는 태그마다 다시 받아 우연히 가려졌다(Fable)
            try:
                fresh = feh.curl_json(url)
            except Exception:
                fresh = {}
            if "facts" in fresh:
                break
            time.sleep(2)
        ok = "facts" in fresh
        if ok:
            json.dump(fresh, open(path, "w"))
            data = fresh
            fst = None   # 내가 방금 쓴 경우는 이번 호출에서 기억하지 않는다 — 쓰고 표식을 재는 사이 남이 또 쓸 수 있다
            # (dr r4 Codex). 다음 호출이 파일을 읽어서 기억한다 — 받은 회사당 해석 한 번이 더 든다
        if run_id:   # 성공·실패 모두 이번 실행에는 다시 받지 않는다(태그마다 재요청하지 않게)
            os.makedirs(os.path.dirname(done), exist_ok=True)
            with open(done, "a") as f:
                f.write(cik + "\n")
            if not ok:
                with open(os.path.join(CACHE_DIR, "_refresh_failed.txt"), "a") as f:
                    f.write(f"{cik} facts\n")
    if data is None:   # 받기 실패는 기억하지 않는다 — 다른 프로세스가 캐시 파일을 만들면 이 프로세스도 다음 호출에서 집는다(dr r1 Codex)
        return {}
    ovst = _stamp(ovp)
    merged = _overlay(cik, data)
    if appr:   # 보충 자료(overlay)까지 합친 뒤에 자른다 — 앞에서 자르면 overlay의 승인 뒤 행이 다시 들어온다(Codex)
        if not any(r.get("filed") == appr and r.get("form") in ("10-Q", "10-K", "10-Q/A", "10-K/A", "20-F", "40-F")
                   for tx in merged.get("facts", {}).values() for tg in tx.values() for rows in tg.get("units", {}).values() for r in rows):
            # 승인한 공시가 자료에 없다(SEC 반영 지연·받기 실패) — 옛 분기로 계속 계산하지 않고 멈춘다(Codex). 매일 재빌드는 이 카드를 전날 상태로 둔다
            raise RuntimeError(f"{cik}: 승인한 공시({appr} 제출)가 SEC 자료에 없다 — sec_approved.json 확인")
        merged = _cap_filed(merged, appr)
    # 만드는 동안 다른 프로세스가 파일을 다시 썼으면 기억하지 않는다 — 옛 자료를 새 파일 표식으로 두면
    # 이 프로세스가 끝까지 옛 자료를 쓴다(dr r3 Codex). 기억하지 않으면 다음 호출이 새 파일로 다시 만든다.
    if fst is None or (_stamp(path), _stamp(ovp)) != (fst, ovst):
        return merged
    return _memo((cik, appr, fst, ovst, os.environ.get("SEC_REFRESH_UNLISTED")), merged)


def _stamp(path):
    """파일의 수정 시각·크기 — 같은 프로세스에서 그 파일이 바뀌면 메모를 다시 만들게 하는 표식."""
    try:
        st = os.stat(path)
    except OSError:
        return None
    return (st.st_mtime_ns, st.st_size)


def _memo(key, merged):
    """만든 facts를 프로세스 안에 둔다. 두 칸을 넘으면 오래 쓰지 않은 것부터 버린다 —
    카드 본체처럼 (내 회사, 비교 종목, 내 회사, …)로 번갈아 물을 때 내 회사가 남는다(dr r1 Fable)."""
    while len(_FACTS_MEMO) >= 2:
        _FACTS_MEMO.pop(next(iter(_FACTS_MEMO)))
        _FACTS_MEMO_HITS[1] += 1
    _FACTS_MEMO[key] = merged
    return merged


SEC_APPROVED = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sec_approved.json")


def _approved():
    """카드 공시 기준표 {cik: 'YYYY-MM-DD'} — 그 날짜까지 제출된 공시만 쓴다(2026-10-08, 분기 반영 절차; 카드 100장 기준선).
    매일·토요일 재빌드는 SEC 재무를 자동 반영하지 않는다(사용자 결정). 사람이 점검을 거쳐 승인한 공시만 이 표에 올리고,
    캐시가 그보다 오래됐으면(예: Actions 캐시) 새로 받아 그 날짜에서 자른다 — 승인한 분기가 다음 날 되돌아가지 않게."""
    # 파일이 없거나 깨졌거나 비었으면 멈춘다 — 빈 표면 모든 카드에 새 공시가 들어간다(Codex 2026-10-08).
    # 카드 회사가 표에서 빠졌는지는 매 실행 앞에서 daily_price.check_approved가 본다.
    table = {k: v for k, v in json.load(open(SEC_APPROVED)).items() if not k.startswith("_")}
    def _ok(v):
        try:
            return isinstance(v, str) and len(v) == 10 and bool(date.fromisoformat(v))
        except ValueError:
            return False
    if not table or not all(_ok(v) for v in table.values()):   # 실제 달력 날짜만(2026-99-99·null은 멈춘다, Codex)
        raise RuntimeError(f"{SEC_APPROVED}: 비었거나 날짜 형식이 틀렸다")
    return table


def _max_filed(data):
    return max((r.get("filed", "") for tx in data.get("facts", {}).values() for tg in tx.values()
                for rows in tg.get("units", {}).values() for r in rows), default="")


def _cap_filed(data, appr):
    out = {k: v for k, v in data.items() if k != "facts"}
    out["facts"] = {tx: {tag: {**body, "units": {u: [r for r in rows if r.get("filed") and r["filed"] <= appr]
                                                 for u, rows in body.get("units", {}).items()}}
                         for tag, body in tags.items()} for tx, tags in data.get("facts", {}).items()}
    return out


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
    """companyfacts 캐시에서 한 태그의 항목들을 꺼낸다. 잘못된 개별 사실 보정(v2/fact_fixes.json, E55)을 사본으로 적용한다."""
    facts = _facts(cik).get("facts", {}).get(taxonomy, {})
    units = facts.get(tag, {}).get("units", {})
    for key in ("USD", "shares", "USD/shares"):
        if units.get(key):
            return _apply_fact_fixes(cik, tag, taxonomy, key, units[key])
    return []


# E55(2026-10-24 사용자 승인, 설계 research/e55_fact_fixes_design.md): companyfacts의 잘못된 개별 사실·기간 정보를 CIK·태그·기간·값으로
# 지정해 빼거나(drop) 시작일을 고친다(set_start). concept()가 고칠 행만 새 dict로 바꾼 목록을 돌려준다 — 캐시 원본·연구의 시점별
# 자료(pit.filtered가 행 dict를 얕게 공유)는 그대로다. concept 안에서는 일치 여부를 따지지 않는다(연구 평가일이 공시 전이면 행이 없는 게
# 정상, Codex·Fable). 일치·기대값 검사는 validate_fixes()가 카드·동종업 빌드(main)에서 CIK마다 한 번 한다.
FACT_FIXES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fact_fixes.json")
_FIXES_CACHE = {}


def _fact_fixes():
    """{cik: [고침]} — 환경변수 FACT_FIXES=off면 빈 dict(고침 전 자료로 스캔·비교할 때), FACT_FIXES=경로면 그 파일."""
    path = os.environ.get("FACT_FIXES", FACT_FIXES)
    if path == "off" or not os.path.exists(path):
        return {}
    if path not in _FIXES_CACHE:
        raw = json.load(open(path))
        out, ids = {}, set()
        for cik, items in raw.items():
            if cik.startswith("_"):
                continue
            for f in items:
                if f["id"] in ids:
                    raise SystemExit(f"fact_fixes: id 중복 {f['id']}")
                ids.add(f["id"])
                if f["scope"] not in ("fact", "context") or f["action"] not in ("drop", "set_start"):
                    raise SystemExit(f"fact_fixes {f['id']}: scope·action 값")
                if f["action"] == "set_start" and not f.get("new_start"):
                    raise SystemExit(f"fact_fixes {f['id']}: new_start 없음")
                if f["scope"] == "fact" and not (f.get("tag") and f.get("unit") and "val" in f["match"]):
                    raise SystemExit(f"fact_fixes {f['id']}: fact 범위는 tag·unit·match.val 필수")
                if f["scope"] == "context" and not f.get("expect_tags"):
                    raise SystemExit(f"fact_fixes {f['id']}: context 범위는 expect_tags 필수")
                if "..." in f.get("source", "...") or not f.get("source", "").startswith("https://www.sec.gov/"):
                    raise SystemExit(f"fact_fixes {f['id']}: source는 정확한 SEC 주소")
                out.setdefault(cik.zfill(10), []).append(f)
        _FIXES_CACHE[path] = out
    return _FIXES_CACHE[path]


def _fix_hits(f, taxonomy, tag, unit, r):
    m = f["match"]
    if r.get("accn") != m["accn"] or r.get("start") != m["start"] or r.get("end") != m["end"]:
        return False
    if f["scope"] == "fact":
        return f.get("taxonomy", "us-gaap") == taxonomy and f["tag"] == tag and f["unit"] == unit and r.get("val") == m["val"]
    return True


def _apply_fact_fixes(cik, tag, taxonomy, unit, rows):
    fixes = _fact_fixes().get(str(cik).zfill(10))
    if not fixes:
        return rows
    out = []
    for r in rows:
        f = next((f for f in fixes if _fix_hits(f, taxonomy, tag, unit, r)), None)
        if f is None:
            out.append(r)
        elif f["action"] == "set_start":
            nr = {k: v for k, v in r.items() if k != "frame"}   # 분기 frame(CY2025Q4)이 연간 기간과 한 행에 남지 않게
            nr["start"] = f["new_start"]
            out.append(nr)
        # drop: 넣지 않는다
    return out


def validate_fixes(cik, ticker=None, strict=None):
    """그 CIK의 고침이 지금 자료(카드가 보는 _facts — overlay 포함·공시 승인일 절단 그대로)에 맞는지 검사하고 문제 목록을 돌려준다.

    (a) 일치 수 — 0개: 낡은 고침(SEC가 고쳤거나 승인일이 그 공시 전), 같은 값 중복: 경고 (b) context 범위는 걸린 (분류, 태그, 단위, 값)
    집합 == expect_tags (c) 고친 뒤 기간 길이 — 연간 350~380일(set_start) (d) set_start면 new_start 전날이 같은 태그 직전 연간 행의 end
    (e) expect — pick_tag → quarterly_flow 결과의 분기 값(정확히). strict(기본: 환경변수 FACT_FIXES_STRICT=1)면 문제가 있을 때 멈춘다."""
    cik = str(cik).zfill(10)
    fixes = _fact_fixes().get(cik)
    if not fixes:
        return []
    strict = os.environ.get("FACT_FIXES_STRICT") == "1" if strict is None else strict
    facts = _facts(cik).get("facts", {})
    probs = []
    for f in fixes:
        hits = []
        for tx, tags in facts.items():
            for tg, v in tags.items():
                for u, rows in v.get("units", {}).items():
                    hits += [(tx, tg, u, r) for r in rows if _fix_hits(f, tx, tg, u, r)]
        if not hits:
            probs.append(f"{f['id']}: 일치하는 행 없음(낡은 고침이거나 승인일이 그 공시 전)")
            continue
        got = {(tx, tg, u, r["val"]) for tx, tg, u, r in hits}
        if len(got) < len(hits):
            print(f"  ⚠ fact_fixes {f['id']}: 같은 값 중복 행 {len(hits) - len(got)}개 — 모두 적용")
        if f["scope"] == "context" and got != {tuple(x) for x in f["expect_tags"]}:
            probs.append(f"{f['id']}: 걸린 사실 집합이 expect_tags와 다름 — {sorted(got ^ {tuple(x) for x in f['expect_tags']})}")
        if f["action"] == "set_start":
            n = (date.fromisoformat(f["match"]["end"]) - date.fromisoformat(f["new_start"])).days
            if not 350 <= n <= 380:
                probs.append(f"{f['id']}: 고친 기간 {n}일(연간 350~380 아님)")
            prev = (date.fromisoformat(f["new_start"]) - timedelta(days=1)).isoformat()
            for tx, tg, u, _ in hits:
                ends = {r["end"] for r in facts[tx][tg]["units"][u] if r.get("start") and 350 <= feh.days_between(r) <= 380}
                if ends and prev not in ends:
                    probs.append(f"{f['id']}: {tg} 직전 연간 결산일 {prev}이 없음(new_start 오타?)")
        for x in f.get("expect", []):
            tags = {"revenue": FLOW_TAGS["revenue"], "opinc": EBITDA_TAGS["opinc"]}[x["series"]]
            q = {e["end"]: e["val"] for e in quarterly_flow(pick_tag(cik, tags)[1], ticker or cik)}
            if q.get(x["quarter_end"]) != x["val"]:
                probs.append(f"{f['id']}: {x['series']} {x['quarter_end']} = {q.get(x['quarter_end'])}, 기대 {x['val']}")
    for p in probs:
        print(f"  ⚠ fact_fixes {p}")
    if probs and strict:
        raise SystemExit(f"fact_fixes 검사 실패({len(probs)}건) — FACT_FIXES_STRICT=1")
    return probs


# E57(2026-10-24 사용자 승인, 설계 research/e57_ocf_netting_design.md): 청산소가 있는 거래소의 영업현금흐름에 섞인 회원 담보금·디폴트 펀드
# 유출입을 뺀다. CBOE만 영업활동에 이 줄이 있다(Cboe Clear Europe — "Restricted cash and cash equivalents and customer bank deposits
# (included in margin deposits, default fund, and interoperability fund)" Q1 2026 +$1,878M). NDAQ·ICE·CME는 재무·투자활동에 둔다.
# 회사 고유 태그라 company_tags 피드(adapters/company_tag_feed.py)가 overlay에 빌린 이름으로 싣는다. 영향 = sign × XBRL 값(CBOE −1,
# 10-K·10-Q 같음 — 원문 확인), 뺀 값 = OCF − 영향. 누계 행끼리 같은 (start, end, accn)로 빼므로 분기 역산이 그대로 맞는다.
# 담보금 시대(era — 태그 첫 공시 Q3 2020 10-Q, EuroCCP 인수 2020-07 뒤) 안의 행은 짝이 있어야 쓴다 — 없으면 그 행을 뺀다(태그 변경·
# 파싱 실패·피드 미실행을 담보금 포함 값으로 조용히 통과시키지 않는다, Codex·Fable). 인수 전 기간(결산일 ≤ 2020-06-30)은 공시일과 상관없이 그대로.
OCF_NETTING = {
    "0001374310": {"tag": "IncreaseDecreaseInRestrictedCashClearingFundCboe", "company_tag": "cboe:IncreaseDecreaseInRestrictedCashClearingFund",
                   "sign": -1, "era_filed": "2020-10-30", "era_accn": "0001558370-20-012101",
                   "exempt_period_end_through": "2020-06-30", "confirmed_none": []},
}


def net_ocf(cik, rows):
    """영업현금흐름 행에서 담보금 영향을 뺀 새 목록(사본). 시대 안 짝 없는 행은 빼고 경고(OCF_NETTING_STRICT=1이면 멈춤)."""
    cfg = OCF_NETTING.get(str(cik).zfill(10))
    if not cfg or not rows:
        return rows
    coll = {(r.get("start"), r["end"], r.get("accn")): r["val"] for r in concept(cik, cfg["tag"])}
    out, dropped = [], []
    for r in rows:
        if r.get("filed", "") < cfg["era_filed"] or r["end"] <= cfg["exempt_period_end_through"]:
            out.append(r)
            continue
        k = (r.get("start"), r["end"], r.get("accn"))
        if k in coll:
            out.append(dict(r, val=r["val"] - cfg["sign"] * coll[k]))
        elif r.get("accn") in cfg["confirmed_none"]:
            out.append(r)
        else:
            dropped.append(r)
    if dropped:
        msg = ", ".join(f"{r.get('start')}~{r['end']}({r.get('accn')})" for r in dropped[:4]) + (" …" if len(dropped) > 4 else "")
        print(f"  ⚠ ocf_netting {cik}: 담보금 짝 없는 영업현금흐름 {len(dropped)}행 제외 — {msg}")
        if os.environ.get("OCF_NETTING_STRICT") == "1":
            raise RuntimeError(f"ocf_netting {cik}: 짝 없는 행 {len(dropped)}개 — OCF_NETTING_STRICT=1")
    return out


def check_ocf_netting(cik):
    """빌드 시작 검사: (a) 원본 companyfacts의 시대 안 영업현금흐름에 같은 (start, end, filed)·다른 accn이 있으면 오류(짝짓기가 accn 기준이라)
    (b) 시대 안 form은 10-K·10-Q만 (c) 가장 최근 영업현금흐름 행에 담보금 짝이 있어야 한다 — 없으면 피드를 안 돌린 것이라 옛 TTM이 현재처럼
    쓰인다(PCR·FCF 계산 불가로 멈춘다). RuntimeError라 동종업 유니버스(sector_universe의 except Exception)에서는 그 종목만 빠진다."""
    cfg = OCF_NETTING.get(str(cik).zfill(10))
    if not cfg:
        return
    raw = os.path.join(CACHE_DIR, f"{str(cik).zfill(10)}_facts.json")
    rows = json.load(open(raw)).get("facts", {}).get("us-gaap", {}).get("NetCashProvidedByUsedInOperatingActivities", {}).get("units", {}).get("USD", []) \
        if os.path.exists(raw) else []
    era = [r for r in rows if r.get("filed", "") >= cfg["era_filed"] and r["end"] > cfg["exempt_period_end_through"]]
    seen = {}
    for r in era:
        k = (r.get("start"), r["end"], r.get("filed"))
        if k in seen and seen[k] != r.get("accn"):
            raise RuntimeError(f"ocf_netting {cik}: 같은 기간·공시일에 accn 둘({seen[k]}, {r.get('accn')}) — accn 짝짓기 불가")
        seen[k] = r.get("accn")
    bad_forms = sorted({r.get("form") for r in era} - {"10-K", "10-Q"})
    if bad_forms:
        raise RuntimeError(f"ocf_netting {cik}: 시대 안 영업현금흐름 form {bad_forms} — 피드가 받지 않는 양식")
    if era:
        last = max(era, key=lambda r: (r["filed"], r["end"]))
        coll = {(r.get("start"), r["end"], r.get("accn")) for r in concept(cik, cfg["tag"])}
        if (last.get("start"), last["end"], last.get("accn")) not in coll and last.get("accn") not in cfg["confirmed_none"]:
            raise RuntimeError(f"ocf_netting {cik}: 최근 영업현금흐름({last['end']}, {last.get('accn')})에 담보금 짝이 없다 — "
                               f"company_tag_feed.py {cik} {cfg['company_tag']} {cfg['tag']} 를 먼저 돌린다(PCR·FCF 계산 불가)")


# 회사 전용 태그 보강(CIK별). 표준 태그 대신 같은 항목을 다른 표준 태그로만 내는 회사.
# LLY: 설비투자 = PaymentsToAcquireOtherPropertyPlantAndEquipment(10-Q "Purchases of property and equipment"),
#      인수 = OtherPaymentsToAcquireBusinesses("Cash paid for acquisitions, net of cash acquired", 2022년 이후).
# 한 항목을 두 표준 태그로 **나눠** 내는 회사 — 같은 공시(accn)·같은 기간 값을 더해 기본 태그 자리에 쓴다(pick_tag).
# EOG: 현금흐름표 "Additions to Oil and Gas Properties"(PaymentsToAcquireOilAndGasPropertyAndEquipment, 상반기 2026 $3,129M)
#      + "Additions to Other Property, Plant and Equipment"(PaymentsToAcquireOtherPropertyPlantAndEquipment, $297M) = 설비투자 $3,426M.
#      기본 목록 태그가 없어 설비투자가 비었다(2026-10-21).
SUM_TAGS_BY_CIK = {# AEP: 설비투자는 공사 지출(PaymentsForConstructionInProcess)만 — 발전소 인수 태그는 2023-12부터라 함께 합산하면 그 전 이력이 사라졌다(Codex·Fable r1, 2026-10-28)
                   "0000004904": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsForConstructionInProcess"]},
                   # MSCI: 설비투자 = 유형자산(PaymentsToAcquirePropertyPlantAndEquipment) + 자본화 소프트웨어(PaymentsForSoftware) — D&A에 소프트웨어 상각이 들어가므로 맞춘다(TTM 약 $40M + $106M, 2026-10-23)
                   "0001408198": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsForSoftware"]},
# DAL: 설비투자 = 항공기(PaymentsForFlightEquipment) + 지상 설비·기타(PaymentsToAcquireOtherProductiveAssets) — 합계 태그는 2026년 1분기에 멈췄다(겹치는 기간 합 = 합계, FY2025 4,499, 2026-10-23)
                   "0000027904": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsForFlightEquipment", "PaymentsToAcquireOtherProductiveAssets"]},
                   "0000821189": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsToAcquireOilAndGasPropertyAndEquipment",
                                                                              "PaymentsToAcquireOtherPropertyPlantAndEquipment"]}}
EXTRA_TAGS = {
    # RL: 10-K는 현금흐름표 설비투자를 PaymentsToAcquireMachineryAndEquipment(FY26 $408.1M·FY25 $216.2M)로, 10-Q는 PaymentsToAcquireProductiveAssets로 낸다 —
    # 10-K 태그가 기본 목록에 없어 4분기가 비고 TTM이 2025-12에 멈췄다($439M, 실제 $274.2M). 겹치는 연간 값은 같다(Fable r1, 2026-11-03).
    "0001037038": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsToAcquireMachineryAndEquipment"]},
    # EQIX: 설비투자를 PaymentsToAcquireProductiveAssets로 내다가 2026년 2분기 누계부터 PaymentsToAcquireOtherPropertyPlantAndEquipment로만 낸다
    # (겹치는 기간 값 같음 — 2025년 누계 $4,311M). 없으면 설비투자가 2026-03에 멈췄다(2026-10-17). 부동산 취득($224M 상반기)은 넣지 않는다.
    "0001101239": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsToAcquireOtherPropertyPlantAndEquipment"]},
    # VZ: 설비투자가 2019-09 뒤 PaymentsToAcquireOtherProductiveAssets(분기 약 $4B, "Capital expenditures (including capitalized
    # software)")로 옮겨 가 기본 목록이 2019년 값에 멈췄다 — PCR 계산 불가(2026-10-01).
    "0000732712": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsToAcquireOtherProductiveAssets"]},
    # HOOD: 현금흐름표 "Purchases of property, software, and equipment"(상반기 2026 $21M)를 PaymentsToAcquireOtherProductiveAssets로 낸다 —
    # 기본 목록의 PaymentsToAcquireProductiveAssets는 2023-09에 멈췄다(2026-10-21). 자본화 소프트웨어(PaymentsToDevelopSoftware)는 넣지 않는다(공통 안건 E30①).
    "0001783879": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsToAcquireOtherProductiveAssets"]},
    # WELL(리츠): 설비투자 표준 태그가 없다 — 기존 자산 개량 지출(PaymentsForCapitalImprovements, 상반기 2026 $589M)을 쓴다. 부동산 인수
    # ($6.3B)·개발 공사($167M)는 넣지 않는다(리츠 평가법 미정, 안건). 순이익은 보통주 귀속 태그만 낸다(2026-10-02).
    # NEE: 손익계산서 총매출은 RegulatedAndUnregulatedOperatingRevenue(Q2 2026 $7,534M)다. RevenueFromContractWithCustomerIncludingAssessedTax는
    # 주석의 고객 계약 매출(0.1B 단위 반올림, $6.7B)이라 뺀다(EXCLUDE_TAGS). 설비투자·이자비용은 회사 고유 태그라 표준 데이터에 없다(2026-10-02).
    "0000753308": {"Revenues": ["RegulatedAndUnregulatedOperatingRevenue"]},
    # VEEV: 현금흐름표 "Long-term assets"(설비·소프트웨어 취득, 상반기 FY27 $9.8M)를 PaymentsForSoftware로, 감가상각("Depreciation and amortization" $22.5M)을
    # OtherDepreciationAndAmortization으로 낸다 — 기본 설비투자 태그는 2020-04에, D&A 태그는 2020-01에 멈췄다(2026-10-23)
    "0001393052": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsForSoftware"], "DepreciationDepletionAndAmortization": ["OtherDepreciationAndAmortization"]},
    # WDAY: 현금흐름표 "Depreciation and amortization"(FY2026 $347M — 감가상각 + 무형자산 상각)을 OtherDepreciationAndAmortization으로 낸다. 기본으로는 감가상각(Depreciation)만 잡혀 TTM $227M이었다(Codex r1, 2026-10-24)
    "0001327811": {"DepreciationDepletionAndAmortization": ["OtherDepreciationAndAmortization"]},
    # XEL: 총매출은 RegulatedAndUnregulatedOperatingRevenue(Q2 2026 $3,119M) — Revenues 태그는 2019-09에 멈췄다(NEE와 같은 경우, 2026-10-23)
    "0000072903": {"Revenues": ["RegulatedAndUnregulatedOperatingRevenue"]},
    # ED: 설비투자는 "Utility construction expenditures"(PaymentsForConstructionInProcess, Q1 2026 $1,172M) — 기본 태그는 2019년에 멈췄다(2026-10-24)
    "0001047862": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsForConstructionInProcess"]},
    # SNA: 설비투자는 PaymentsForCapitalImprovements(9개월 $69.0M), D&A는 감가상각(Depreciation)만 분기로 — 합산 태그는 연간만, 무형자산 상각(연 약 $22M)은 2026년 분기에 표준 태그가 없다(2026-10-25)
    "0000091440": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsForCapitalImprovements"], "DepreciationDepletionAndAmortization": ["Depreciation"]},
    # CBOE: 설비투자를 2026 2분기부터 PaymentsToAcquireProductiveAssets(유형자산 + 소프트웨어 개발비 합)로 낸다 — EQIX와 같은 경우(2026-10-24)
    "0001374310": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsToAcquireProductiveAssets"]},
    # DUK: 총매출은 RegulatedAndUnregulatedOperatingRevenue — Revenues 태그는 2017년에 멈췄다(XEL과 같은 경우, 2026-10-24)
    "0001326160": {"Revenues": ["RegulatedAndUnregulatedOperatingRevenue"]},
    # AWK: 총매출은 RegulatedAndUnregulatedOperatingRevenue(Q3 2026 $1,510M) — Revenues 태그는 2015-06에 멈췄다(DUK과 같은 경우, 2026-11-07)
    "0001410636": {"Revenues": ["RegulatedAndUnregulatedOperatingRevenue"]},
    # SRE: 총매출은 RegulatedAndUnregulatedOperatingRevenue(Q3 2026 $3,191M) — Revenues 태그는 2025-12에 멈췄다(AWK와 같은 경우, 2026-11-07)
    "0001032208": {"Revenues": ["RegulatedAndUnregulatedOperatingRevenue"]},
    # D: 설비투자는 PaymentsForProceedsFromProductiveAssets(2026 Q1 $3,030M) — Q3 2026 10-Q부터 회사 고유 태그(d:PaymentsToAcquirePropertyPlantAndEquipmentIncludingNuclearFuel, 9개월 $8,576M)라 BUILD company_tags가 같은 이름으로 싣는다. 기본 태그는 2020-03에 멈췄다(2026-11-07)
    "0000715957": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsForProceedsFromProductiveAssets"]},
    # INCY: 설비투자("Capital expenditures", 9개월 2026 $38.2M)를 2021-12부터 PaymentsToAcquireOtherProductiveAssets로 — 기본 태그는 2022-12에 멈춰 PCR이 빠졌다(2026-11-07)
    "0000879169": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsToAcquireOtherProductiveAssets", "PaymentsToAcquireProductiveAssets"]},
    # BAX: 설비투자를 2026년부터 PaymentsToAcquireOtherProductiveAssets로(9개월 $363M) — 기본은 2025-12에 멈춘 PaymentsToAcquireProductiveAssets(2026-11-07)
    "0000010456": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsToAcquireOtherProductiveAssets", "PaymentsToAcquireProductiveAssets"]},
    # PEG: 감가상각은 손익계산서 "Depreciation and Amortization" 줄(CostOfGoodsAndServicesSoldDepreciationAndAmortization, Q2 2026 $321M)뿐 — 기본 D&A 태그가 없어 0이었다(2026-10-24)
    "0000788784": {"DepreciationDepletionAndAmortization": ["CostOfGoodsAndServicesSoldDepreciationAndAmortization"]},
    # GLW: 설비투자("Capital expenditures", 상반기 2026 $754M)를 2020년부터 PaymentsForCapitalImprovements로만 낸다 — 기본 목록은
    # 2020-09에 멈춘 PaymentsToAcquireProductiveAssets를 잡아 PCR 계산 불가였다(2026-10-02).
    "0000024741": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsForCapitalImprovements"]},
    # AJG: 현금흐름표 "Capital expenditures"(상반기 2026 $87M)를 2015년부터 PaymentsForCapitalImprovements로 낸다 — 기본 목록은 2017년에 멈췄다(2026-10-22).
    "0000354190": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsForCapitalImprovements"]},
    # VLO: 2026년 10-Q부터 현금흐름표 설비투자·정기보수 줄을 VIE 차원으로만 태깅해 PaymentsToAcquireProductiveAssets가 2025-09에 멈췄다(PCR 계산 불가).
    # SegmentExpenditureAdditionToLongLivedAssets(차원 없음)가 겹치는 기간에 같은 값이다 — 2024년 $2,057M, 2025년 상반기 $1,066M, 2026년 상반기 $798M(2026-10-13).
    "0001035002": {"PaymentsToAcquirePropertyPlantAndEquipment": ["SegmentExpenditureAdditionToLongLivedAssets"]},
    # FCX: 2분기 10-Q는 설비투자를 부문 차원으로만 태깅해(합계 없음) PaymentsToAcquireProductiveAssets가 2026-03에 멈췄다 — 부문 설비투자 합계 태그가
    # 같은 값이다(2025 상반기 2,433 = 2,433, 2026 상반기 2,077 = 496+285+972+49+275, VLO와 같은 처리, 2026-10-17).
    "0000831259": {"PaymentsToAcquirePropertyPlantAndEquipment": ["SegmentExpenditureAdditionToLongLivedAssets"]},
    # ADP: 현금흐름표 "Capital expenditures"(FY2026 $196.6M)를 PaymentsToAcquireOtherPropertyPlantAndEquipment로 낸다 — 기본 목록 태그가 없어 PCR 계산 불가였다.
    # 자본화 소프트웨어 "Additions to intangibles"($468.5M, PaymentsToAcquireIntangibleAssets)는 넣지 않는다(공통 안건 — MCK와 같은 정의, 2026-10-16).
    "0000008670": {"PaymentsToAcquirePropertyPlantAndEquipment": ["PaymentsToAcquireOtherPropertyPlantAndEquipment"]},
    # RJF: 손익계산서 헤드라인은 순매출 "Net revenues"(RevenuesNetOfInterestExpense, Q3 FY26 $3,928M) — Revenues($4,362M)는 이자수익을 더한 총수익이라
    # 부문 순매출 합과 $194M(= 이자비용 434 − Other·제거 240) 어긋났다. 이자비용이 순매출 계산 안에서 빠지는 증권·은행 구조(2026-11-04)
    "0000720005": {"Revenues": ["RevenuesNetOfInterestExpense"]},
    # IVZ: NetIncomeLoss는 2025-03에 멈췄고 그 뒤 "Net income attributable to Invesco Ltd."(우선주 배당·재매입 비용 차감 뒤 보통주 몫, Q3 2026 $294.5M)를
    # NetIncomeLossAvailableToCommonStockholdersBasic로 낸다 — 기본 대체 ProfitLoss는 CIP 비지배·우선주 배당 차감 전이라 순이익률이 −1.15%로 나왔다(2026-11-04)
    "0000914208": {"NetIncomeLoss": ["NetIncomeLossAvailableToCommonStockholdersBasic"]},
    # CF: 순이익은 보통주 귀속 태그만 낸다(NetIncomeLoss 2012 멈춤, Q2 2026 $727M)(2026-10-25)
    "0001324404": {"NetIncomeLoss": ["NetIncomeLossAvailableToCommonStockholdersBasic"]},
    # AEP: 지배 순이익은 NetIncomeLoss가 없고 보통주 귀속 순이익뿐 — ProfitLoss는 비지배 포함(2026-10-28)
    "0000004904": {"NetIncomeLoss": ["NetIncomeLossAvailableToCommonStockholdersBasic", "NetIncomeLossAvailableToCommonStockholdersDiluted"]},
    # EXC: NetIncomeLoss 태그는 2013에 멈췄다 — 보통주 귀속 순이익(Q2 2026 $396M, 비지배 없음)으로(2026-10-28)
    "0001109357": {"NetIncomeLoss": ["NetIncomeLossAvailableToCommonStockholdersBasic"]},
    # ETR: 연결 NetIncomeLoss는 2023에 멈췄다(이후 자회사 축 값만) — 보통주 귀속 순이익(Q2 2026 $482.6M)으로(2026-10-28)
    "0000065984": {"NetIncomeLoss": ["NetIncomeLossAvailableToCommonStockholdersBasic"]},
    # ALLE: 2025-04 뒤 10-Q는 순이익을 ProfitLoss로만 낸다(비지배지분 없음, NetIncomeLoss는 10-K·Q1 2025만) — 분기 순이익 차트가 비어 build가 멈췄다(2026-10-25)
    "0001579241": {"NetIncomeLoss": ["ProfitLoss"]},
    # BALL: 순이익을 ProfitLoss로 낸다(NetIncomeLoss 없음) — 비지배지분 몫(분기 약 $2M)이 섞인다(2026-10-25)
    "0000009389": {"NetIncomeLoss": ["ProfitLoss"]},
    # PNW: 순이익은 보통주 귀속 태그만 낸다(NetIncomeLoss 없음, Q2 2026 $178.6M) — 분기 순이익 차트가 비어 build가 멈췄다(2026-10-25)
    "0000764622": {"NetIncomeLoss": ["NetIncomeLossAvailableToCommonStockholdersBasic"]},
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
DERIVED_OPINC = {# RJF: 영업이익 줄이 없다 — 손익계산서는 순매출(이자비용 차감 뒤) − 비이자비용 = 세전이익(Q3 FY26 3,928 − 3,178 = 750, 10-Q). 세전 태그는 2025-06 뒤 회사 고유 태그라 companyfacts에 없다(2026-11-04)
                 "0000720005": (["RevenuesNetOfInterestExpense"], [(["NoninterestExpense"], 1)]),
                 # HCA: 손익계산서에 영업이익 줄이 없다(이자·상각·시설 매각 손익이 비용 합계 안) — 영업이익 = 세전이익 + 이자비용(2026-10-25).
                 # PHM: 손익계산서에 영업이익 줄이 없다(주택건설 매출총이익 − 판관비 + 금융 부문 이익 + 기타). 영업이익 = 세전이익(Domestic 태그) − 이자수익 − 기타 영업외(제조 자산 매각 이익 등)
                 # − 지분법 이익. 보증금·사전취득비 상각과 무형 상각은 영업으로 둔다. 이자는 대부분 재고에 자본화돼 이자비용은 거의 0(2026-11-03).
                 # GPC: 영업이익 태그가 2016에 멈춤. 영업이익 = 세전이익 − 영업외 손익 합계(이자·연금 정산 등, 음수라 더해짐) — GrossProfit − OperatingExpenses와 80개 기간 일치(Codex r1).
                 # 처음엔 이자만 더해 Q4 2025 연금 정산 손실 $742M이 영업이익에 남았다(2026-11-03).
                 "0000040987": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"],
                                [(["NonoperatingIncomeExpense"], 1)]),
                 "0000822416": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic"],
                                [(["InterestIncomeOther"], 1, True), (["OtherNonoperatingIncomeExpense", "OtherNonoperatingIncome"], 1, True), (["IncomeLossFromEquityMethodInvestments"], 1, True)]),   # 부호 1 = 뺀다(처음에 −1로 넣어 더해졌다 — Codex·Fable r1). 10-K 연간 기타는 OtherNonoperatingIncome
                 # BRO: 손익계산서에 영업이익 줄이 없다(비용 합계 안에 이자·상각·earn-out 변동) — 영업이익 = 세전이익 + 이자비용(HCA 규칙). 이자 태그는 2024-06에 InterestExpense → InterestExpenseNonoperating(Q3 2026 320 + 100 = 420, 2026-11-05)
                 # 에스크로 주식 평가손익(bro:MarkToMarketOfEscrowLiability — 비용 줄, 이익이면 음수)은 자기 주가에 연동된 Accession 에스크로 부채의 재측정이라 영업 밖 —
                 # 회사 고유 태그라 cfg BUILD company_tags가 빌린 이름으로 싣고, 2025 Q3 전 공시엔 없어 선택 항목(0). Q3 2026: 320 + 100 − 14 = 406(2026-11-05 사용자 결정)
                 "0000079282": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"],
                                [(["InterestExpense", "InterestExpenseNonoperating"], -1), (["MarkToMarketOfEscrowLiabilityBro"], -1, True)]),
                 "0000860730": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"],
                                [(["InterestExpense"], -1)]),
                 # PPG: 손익계산서에 영업이익 줄이 없다 — OperatingIncomeLoss 태그(Q2 2026 $743M)는 4분기 행이 없고 세전이익($569M)보다 커서 부문 이익 합계로 보인다(ROK와 같은 경우).
                 # 영업이익 = 세전이익 + 이자비용(MTD 방식, 2026-10-25). 구조조정·환경 정화 등 "기타 비용"은 영업으로 둔다.
                 "0000079879": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"],
                                [(["InterestExpense", "InterestExpenseNonoperating"], -1),   # 10-K 연간 이자는 InterestExpenseNonoperating에만 있다(없으면 4분기가 빈다)
                                 (["InvestmentIncomeInterest"], 1, True)]),   # 이자수익(Q2 2026 $42M)은 빼서 금융손익 제외 — 현금을 따로 더하는 DCF와 겹치지 않게(Codex r1)
                 # AVY: OperatingIncomeLoss 태그가 한 번도 없다 — 영업이익 = 세전이익 + 이자비용(MTD 방식, 2026-10-25). 세전 태그는 2023까지 옛 이름, 이자 태그는 2024-03까지 InterestExpense.
                 "0000008818": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                 "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
                                [(["InterestExpenseNonoperating", "InterestExpense"], -1),
                                 (["OtherNonoperatingIncomeExpense"], 1, True)]),   # 기타 영업외 수익(연금 등, 최근 4분기 약 $17M)은 뺀다 — 그 분기에 없으면 0(Fable r1)
                 # BALL: OperatingIncomeLoss 태그가 2024-03에 멈췄다 — 영업이익 = 세전이익 + 부채 이자비용(InterestExpenseDebt)(MTD 방식, 2026-10-25).
                 "0000009389": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
                                [(["InterestExpenseDebt"], -1)]),
                 # CASY: 손익계산서에 영업이익 줄이 없다(OperatingIncomeLoss 태그가 한 번도 없음) — 영업이익 = 세전이익 + 이자비용(MTD 방식).
                 # Q1 FY27: 347.0 + 22.1 = 369.1(10-Q 대조, 2026-10-25). 세전 태그는 FY2022부터 …ExtraordinaryItemsNoncontrollingInterest, 그 전은 옛 태그.
                 "0000726958": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                 "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
                                 "IncomeLossAttributableToParent"],   # 10-K 연간 세전이익은 이 태그로만 실린다(FY26 $937.0M = 손익계산서 "Income before income taxes", 10-K만)
                                [(["InterestExpense"], -1)]),
                 # MTD: 손익계산서에 영업이익 줄이 없다(OperatingIncomeLoss 태그가 한 번도 없음) — "Earnings before taxes"에서 끝난다. 영업이익 = 세전이익 + 이자비용.
                 # 구조조정·기타 비용(수익)은 영업으로 둔다. Q2 2026: 289.4 + 17.2 = 306.6(10-Q 대조, 2026-10-25)
                 "0001037646": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                 "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],   # 2021-06까지 옛 세전 태그(Fable r1)
                                [(["InterestExpense", "InterestExpenseNonoperating"], -1)]),
                 # BIIB: 영업이익 줄이 없다(OperatingIncomeLoss는 2022-03에 멈춤) — "Total cost and expenses" 안에 "Other (income) expense, net"이 들어 있다
                 # (이자비용·투자수익·지분증권 손익. XBRL은 수익이면 양수 — 분기는 OtherOperatingIncomeExpenseNet, 10-K 연간은 NonoperatingIncomeExpense).
                 # 영업이익 = 세전이익 − 그 줄. 인수 IPR&D·조건부 대가 변동은 영업으로 둔다. Q1 2026: 377.7 − (−19.7) = 397.4(10-Q 대조, 2026-10-24)
                 # 세전 태그는 2025년부터 …ExtraordinaryItemsNoncontrollingInterest, 그 전은 …MinorityInterestAndIncomeLossFromEquityMethodInvestments(ROST와 같은 방식).
                 "0000875045": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                 "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
                                [(["OtherOperatingIncomeExpenseNet", "NonoperatingIncomeExpense"], 1),
                                 # 비용 안 별도 줄의 일회성 매각 이익도 뺀다(ETN 전례) — Q2 2022 Samsung Bioepis 지분 $1,505.4M, Q3 2022 건물 $503.7M(Fable r1),
                                 # Q2 2024 무형자산(우선 심사권) 매각 $88.6M — 그 이익을 10-Q 누계는 GainLossOnSaleOfPropertyPlantEquipment로도, 10-K 연간은
                                 # GainLossOnDispositionOfIntangibleAssets로만(유형자산 태그는 0) 냈다. 한 항목에 두 태그를 두고 0인 행을 건너뛰어 기간마다 한 번만 뺀다(Codex r2).
                                 (["EquityMethodInvestmentRealizedGainLossOnDisposal"], 1, True),
                                 (["GainLossOnSaleOfPropertyPlantEquipment", "GainLossOnDispositionOfIntangibleAssets"], 1, True, True)]),
                 # DHI: 손익계산서에 영업이익 줄이 없다(주택 건설사) — 영업이익 = 세전이익. 기타 영업외 손익(Q3 FY26 $71.2M)에는 임대·모기지 이자수익 같은
                 # 반복 영업 수익이 섞여 있고, 이자비용은 대부분 자본화돼 매출원가로 나가 세전이익이 사실상 이자 차감 전이다(Codex r1, 2026-10-24)
                 "0000882184": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", []),
# PCAR: 영업이익 줄이 없다 — 손익계산서는 트럭·부품·기타 세전 + 금융 서비스 세전 + 투자수익 = 세전이익. 영업이익 = 세전이익 − 투자수익(InvestmentIncomeNet,
                 # 트럭 부문 시장성 증권 수익). 금융 서비스 이자비용은 영업으로 둔다(CAT·DE 규칙). Q2 2026: 981.5 − 86.0 = 895.5(10-Q 대조, 2026-10-23)
                 "0000075362": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", [(["InvestmentIncomeNet"], 1)]),
# NUE: 영업이익 줄이 없다 — 손익계산서는 매출 − 비용(지분법 이익·자산 손상·순이자 포함) = 세전이익. 영업이익 = 세전이익 + 순이자비용(InterestRevenueExpenseNet, 음수로 실림).
                 # 지분법 이익·자산 손상은 영업으로 둔다. Q2 2026: 1,625 + 12 = 1,637(10-Q 대조, 2026-10-23)
                 "0000073309": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", [(["InterestRevenueExpenseNet"], 1)]),
# AJG(보험 중개): 영업이익 줄이 없다 — 손익계산서는 총수익 − 총비용(이자비용 포함) = 세전이익. 영업이익 = 세전이익 + 이자비용.
                 # 수탁 자금 이자수익(총수익 안)과 인수 성과보수 추정 변동(비용 안)은 영업으로 둔다. Q2 2026: 414 + 168 = 582(10-Q 대조, 2026-10-22).
                 "0000354190": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest", [(["InterestExpense"], -1)]),
# ROST: 영업이익 태그(OperatingIncomeLoss)는 2023년부터만 — 그 전엔 손익계산서에 영업이익 줄이 없어 현금흐름 이력이 비었다.
                 # 영업이익 = 세전이익 − 순이자수익(InterestIncomeExpenseNet, 순수익이면 양수). Q2 FY26: 1,134.8 − 31.1 = 1,103.6 = 영업이익 태그(2026-10-22).
                 "0000745732": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                 "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
                                [(["InterestIncomeExpenseNet"], 1)]),
                 # SHW: 영업이익 줄이 없다(OperatingIncomeLoss는 2024-09에 멈춤). 영업이익 = 세전이익 + 이자비용 − 이자수익 − 기타 영업외 수익
                 # = 매출총이익 − 판관비 − 기타 일반비용. Q2 2026: 1,112.5 + 135.9 − 5.4 − 12.1 = 1,230.9 = 3,338.0 − 2,103.7 − 3.4(10-Q 대조, 2026-10-22).
                 "0000089800": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["InterestExpenseNonoperating", "InterestExpense"], -1), (["InvestmentIncomeNet", "InvestmentIncomeInterest"], 1, True),
                                 (["OtherNonoperatingIncomeExpense"], 1)]),
                 # HOOD: 영업이익 줄이 없다. 영업이익 = 세전이익 − "Other income, net"(OtherNonoperatingIncomeExpense) = 순매출 − 영업비용.
                 # Q2 2026: 709 − 135 = 574 = 1,308 − 734(10-Q 대조, 2026-10-21).
                 "0001783879": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["OtherNonoperatingIncomeExpense"], 1)]),
                 # TJX: 손익계산서에 영업이익 줄이 없다. 영업이익 = 세전이익 − "Interest (income) expense, net"(InterestRevenueExpenseNet, 순이자수익이면 양수).
                 # Q2 FY27: 2,018 − 31 = 1,987 = 매출 15,180 − 원가 10,108 − 판관비 3,085(10-Q 대조, 2026-10-02).
                 "0000109198": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["InterestRevenueExpenseNet"], 1)]),
                 # BX: 영업이익 줄이 없다. 영업이익 = 세전이익 − "Total Other Income"(펀드 투자 순이익) + 이자비용(총비용 안에 있다 — Codex).
                 # Q2 2026: 2,808 − 140 + 145 = 2,813 = 총매출 5,044 − (총비용 2,376 − 이자 145)(10-Q 대조, 2026-10-02).
                 "0001393818": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["OtherNonoperatingIncomeExpense"], 1), (["InterestExpense"], -1)]),
                 # ADP: 영업이익 줄이 없다. 영업이익 = 세전이익 − "Other (income)/expense, net"(NonoperatingIncomeExpense, 수익이면 양수 — 회사 투자 이자 등) + 이자비용(총비용 안).
                 # FY2026: 5,730.3 − 410.6 + 459.3 = 5,779.0 = 매출 21,947.4 − 원가 11,760.2 − 판관비 4,408.2(10-K 대조, 2026-10-16). 고객 자금 이자는 매출 안이라 영업.
                 # 세전 태그가 FY2021까지 …MinorityInterestAndIncomeLossFromEquityMethodInvestments라 목록으로 잇는다(없으면 합성 이력이 2022-08 공시부터).
                 # NKE: 영업이익 줄이 없다. 영업이익 = 세전이익 − "Interest (income) expense, net"(InterestIncomeExpenseNonoperatingNet, 순이자수익이면 양수)
                 # − "Other (income) expense, net"(OtherNonoperatingIncomeExpense, 수익이면 양수). Q1 FY27: 921 − 14 − 19 = 888 = 매출총이익 4,798 − 판관비 3,910(10-Q 대조, 2026-10-17).
                 # 세전 태그가 FY2021까지 …MinorityInterestAndIncomeLossFromEquityMethodInvestments라 목록으로 잇는다(ADP 전례 — 없으면 합성 이력이 2022-10 공시부터).
                 # ELV: OperatingIncomeLoss 태그는 영업 매출 − 의료비·상품원가·영업비용(Q2 2026 $1,763M) — 'Total revenues' 안의 투자수익($704M)·금융상품 손익과
                 # 무형자산 상각이 빠진다. UNH·CVS처럼 투자수익을 영업으로 보고(INVESTMENTS_OPERATING) 영업이익 = 세전이익 + 이자비용
                 # (Q2 2026: 1,937 + 364 = 2,301). 이자 태그가 2024-07부터 InterestExpenseNonoperating, 세전 태그는 FY2021까지 다른 이름(2026-10-17).
                 "0001156039": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                 "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
                                [(["InterestExpenseNonoperating", "InterestExpense"], -1)]),
                 "0000320187": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                 "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
                                [(["InterestIncomeExpenseNonoperatingNet"], 1), (["OtherNonoperatingIncomeExpense"], 1)]),
                 "0000008670": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                 "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
                                [(["NonoperatingIncomeExpense"], 1), (["InterestExpense"], -1)]),
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
                 # + 이자·기타 금융비용 + 영업외 연금비용(수익이면 음수). 뒤 두 줄은 회사 고유 태그라 새 공시마다 cfg_ge BUILD
                 # company_tags(adapters/company_tag_feed.py)가 overlay에 싣는다(2026-10-21; 2021년까지 옛 이름은 ge_income_items.py가 한 번 넣음). 보험(런오프) 수익·비용은 영업으로 둔다. Q2 2026: 2,801 − 313
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
                 # NWSA: 손익계산서에 영업이익 줄이 없다(OperatingIncomeLoss 태그 없음) — DIS와 같은 규칙: 세전이익 − 순이자 − 기타 영업외손익.
                 # 지분법 손실·구조조정·손상은 영업에 둔다. FY2026: 1,046 − 29 − (−4) = 1,021(10-K 대조, 2026-10-30).
                 "0001564708": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["InterestIncomeExpenseNonoperatingNet"], 1),
                                 (["OtherNonoperatingIncomeExpense"], 1, True)]),
                 "0000315189": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments", []),
                 "0000319201": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["InterestExpenseNonoperating", "InterestExpense"], -1), (["OtherNonoperatingIncomeExpense"], 1),
                                 # 채무 상환 손실(손익계산서 별도 줄, 손실은 음수) — Q1 FY23 $13.3M(Codex). 없는 분기는 0.
                                 (["GainsLossesOnExtinguishmentOfDebt"], 1, True)]),
                 # IBM: 손익계산서에 영업이익 줄이 없고 "지식재산·주문 개발 수익"과 "기타 (수익)·비용"은 회사 고유 태그라 SEC 요약 데이터에
                 # 없다. 영업이익 = 매출총이익 − 판관비 − R&D(표준 태그만). 지식재산 수익(Q2 2026 $166M)은 빠져 조금 보수적이다.
                 # Q2 2026: 9,907 − 4,981 − 2,311 = 2,615(10-Q 대조, 2026-10-01).
                 "0000051143": ("GrossProfit", [(["SellingGeneralAndAdministrativeExpense"], 1), (["ResearchAndDevelopmentExpense"], 1)]),
                 # AES: 손익계산서에 영업이익 줄이 없다 — 합성 값 "Operating margin"(GrossProfit) − 일반관리비(회사 보고 지표 아님). 자산 손상·사업 매각 손익·환차손은 합성 값에서 뺀다.
                 # Q3 2026: 982 − 68 = 914(10-Q 대조, 2026-11-07)
                 "0000874761": ("GrossProfit", [(["GeneralAndAdministrativeExpense"], 1)]),
                 # SRE: 손익계산서에 영업이익 줄이 없다(비용 합계 안에 기타 수익·이자·매각 이익). 영업이익 = 세전·지분법 전 이익 + 이자비용 − 이자수익 − "Other income, net"
                 # − 매각 이익("Gain on sales", Ecogas). 규제 불인정 비용은 영업으로 둔다. 지분법 이익(Oncor·Cameron LNG)은 세전 줄 아래라 들어가지 않는다.
                 # Q3 2026: 460 + 298 − 35 − 58 − 214 = 451 = 매출 3,191 − 비용 줄 합 2,740(10-Q 대조, 2026-11-07)
                 "0001032208": (["IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
                                [(["InterestExpenseNonoperating", "InterestExpense"], -1), (["InvestmentIncomeInterest"], 1, True),
                                 (["OtherNonoperatingIncomeExpense"], 1, True), (["DisposalGroupNotDiscontinuedOperationGainLossOnDisposal"], 1, True)]),
                 # ETN: 손익계산서에 영업이익 줄이 없다(OperatingIncomeLoss 태그 없음). 영업이익 = 세전이익 + 순이자비용("Interest expense - net")
                 # − "Other expense (income) - net"(OtherNonoperatingIncomeExpense, 비용이면 음수). 순이자비용 태그가 공시마다 바뀌었다 —
                 # 2024-09부터 InterestExpenseNonoperating(양수), 일부 재작성 공시는 InterestExpenseOperating(양수), 그 전은
                 # InterestIncomeExpenseNet(비용이면 음수, 부호를 뒤집는다). 같은 공시에 둘이 있으면 앞 태그를 쓴다.
                 # Q2 2026: 1,144 + 201 + 47 = 1,392 = 매출 8,531 − 매출원가 5,676 − 판관비 1,236 − R&D 227(10-Q 대조, 2026-10-01).
                 # EMR: 손익계산서에 영업이익 줄이 없다(OperatingIncomeLoss 태그 없음). 영업이익 = 계속사업 세전이익 + 순이자비용
                 # (InterestIncomeExpenseNonoperatingNet, 비용이면 음수). "Other deductions, net"(무형자산 상각·구조조정·인수 비용·환차손)은 영업비용으로 남긴다.
                 # Q3 FY26: 916 + 85 = 1,001 = 매출 4,873 − 매출원가 2,218 − 판관비 1,343 − 기타 차감 311(10-Q 대조, 2026-10-18).
                 "0000032604": ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                                [(["InterestIncomeExpenseNonoperatingNet"], 1)]),
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
                                [(["InterestAndDebtExpense"], -1)]),
                 # PSX: COP·XOM과 같은 구조(영업이익 줄 없음) → 같은 규칙. 세전이익은 IncomeLossIncludingPortionAttributableToNoncontrollingInterest
                 # (손익계산서 "Income before income taxes" — Q2 2025 1,120 대조)로만 낸다. 영업이익 = 세전 + "Interest and debt expense".
                 # CPChem·DCP 등 지분법 이익·처분 손익·기타 수익은 영업(XOM 규칙). Q2 2026: 4,971 + 314 = 5,285(10-Q 대조, 2026-10-13).
                 "0001534701": ("IncomeLossIncludingPortionAttributableToNoncontrollingInterest",
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
        skip_zero = len(it) > 3 and it[3]       # 0인 행은 건너뛰고 뒤 태그 값을 쓴다(BIIB — 같은 이익을 기간마다 다른 태그로, 안 쓴 태그엔 0)
        m = {}
        for t in tags:                          # 앞 태그 우선(이름이 바뀐 태그는 뒤에)
            t, mult = t if isinstance(t, tuple) else (t, 1)   # (태그, 배수): 같은 줄을 부호가 반대인 태그로 낸 공시(ETN 이자)
            for r in concept(cik, t, taxonomy):
                if skip_zero and not r["val"]:
                    continue
                m.setdefault((r.get("start"), r["end"], r.get("accn")), mult * r["val"])
        maps.append((m, sign, optional))
    out = []
    # 세전 태그는 하나 또는 목록(앞 태그 우선 — 이름이 바뀐 회사: ADP는 FY2021까지 …MinorityInterestAndIncomeLossFromEquityMethodInvestments)
    pre_rows, seen_k = [], set()
    for pt in ([pre_tag] if isinstance(pre_tag, str) else pre_tag):
        for r in concept(cik, pt, taxonomy):
            k = (r.get("start"), r["end"], r.get("accn"))
            if k not in seen_k:
                seen_k.add(k)
                pre_rows.append(r)
    for r in pre_rows:
        k = (r.get("start"), r["end"], r.get("accn"))
        if all(k in m or opt for m, _, opt in maps):
            out.append({**r, "val": r["val"] - sum(sign * m.get(k, 0) for m, sign, _ in maps)})
    return out


# 종목별로 후보에서 빼는 태그(CIK). MA는 2018~2022년 RevenueFromContractWithCustomerExcludingAssessedTax에
# 리베이트·인센티브 차감 전 **총매출**(2022 Q3 $9.17B)을, Revenues에 순매출($5.76B)을 실었다. 합치면 앞 태그가
# 이겨 2021~2022 매출이 부풀고 2022 Q4가 −$3.7B가 됐다(5년 성장 4.9% — 실제 순매출 기준 약 14%, 2026-09-29).
# GE: RevenueFromContractWithCustomerExcludingAssessedTax는 보험 매출을 뺀 값이라(2023 Q2 $7,907M 대 총매출 $8,755M) 총매출
# Revenues와 섞이면 분기마다 기준이 달라진다(Codex, 2026-09-30). 손익계산서 "Total revenue"인 Revenues만 쓴다.
EXCLUDE_TAGS = {"0001140536": ("RevenueFromContractWithCustomerExcludingAssessedTax",),   # WTW: 계약 매출(이자·기타 제외)과 총매출 Revenues가 섞여 Q4 2025가 $2,744M(총 $2,936M)으로 역산됐다 — 총매출만(Codex r1 2026-11-05)
                "0000720005": ("Revenues",),   # RJF: 총수익(이자수익 포함) 대신 순매출 — EXTRA_TAGS(2026-11-04)
                "0000046080": ("Revenues",),   # HAS: Revenues는 2024-12~2026-06 내부거래 제거 전 부문 합(Q2 2026 $1,290.5M 대 순매출 $1,139.6M) — 계약 매출 태그만(2026-11-03)
                # MTD: CommonStockSharesOutstanding(21,683,802)은 자사주를 빼지 않은 낡은 값이 분기마다 반복된다 — 표지 dei 주식 수(20.04M)만 쓴다(Fable r1 2026-10-25)
                "0001037646": ("CommonStockSharesOutstanding",),
                # BE: 손익계산서 매출은 Revenues(Q3 2026 $1,235.8M) — 고객 계약 매출 태그($1,231.0M)는 전력 판매·리스 일부가 빠진다(2026-10-24)
                "0001664703": ("RevenueFromContractWithCustomerExcludingAssessedTax",),
                # NTAP: D&A는 현금흐름표 DepreciationAndAmortization(분기·연간 모두)만 — 10-K의 DepreciationDepletionAndAmortization(유형자산분 $179M)과 섞이면 Q4 FY26이 $28M으로 줄었다(Fable r1, 2026-10-24)
                "0001002047": ("DepreciationDepletionAndAmortization",),
                "0001141391": ("RevenueFromContractWithCustomerExcludingAssessedTax",),
                # ED: 손익계산서 총매출은 Revenues(Q1 2026 $5,095M) — 고객 계약 매출 태그($5,231M)는 대체 수익 조정 전이라 크다(2026-10-24)
                "0001047862": ("RevenueFromContractWithCustomerExcludingAssessedTax", "PaymentsToAcquirePropertyPlantAndEquipment"),   # 설비투자 옛 태그(10-K 연간만, 비유틸리티·철거비 포함)가 섞이면 4분기 역산이 틀어진다(Fable r1)
                # DUK: 고객 계약 매출 태그(Q1 2026 $8,995M — 대체 매출 빠짐)를 빼야 RegulatedAndUnregulatedOperatingRevenue($9,178M)가 쓰인다(2026-10-24)
                "0001326160": ("RevenueFromContractWithCustomerIncludingAssessedTax", "RevenueFromContractWithCustomerExcludingAssessedTax", "SalesRevenueNet"),
                # AWK: 고객 계약 매출 태그 두 개(Q3 2026 $1,502M, Q1 2025 $1,134M — 대체 매출 빠짐)를 빼야 RegulatedAndUnregulatedOperatingRevenue($1,510M·$1,142M)가 쓰인다.
                # IncludingAssessedTax는 2018~2025-03에 있어 Q1 2025가 $1,134M으로 섞였다(Codex r1, 2026-11-07)
                "0001410636": ("RevenueFromContractWithCustomerIncludingAssessedTax", "RevenueFromContractWithCustomerExcludingAssessedTax"),
                # SRE: 고객 계약 매출 태그는 주석 값(대체 매출 빠짐) — 빼야 RegulatedAndUnregulatedOperatingRevenue가 쓰인다(AWK와 같음, 2026-11-07)
                "0001032208": ("RevenueFromContractWithCustomerIncludingAssessedTax", "RevenueFromContractWithCustomerExcludingAssessedTax"),
                # D: 고객 계약 매출 태그(Q3 2026 $5,592M — 기타 매출 $25M 빠짐)를 빼야 손익계산서 총매출 Revenues($5,617M)가 쓰인다(2026-11-07)
                "0000715957": ("RevenueFromContractWithCustomerIncludingAssessedTax", "RevenueFromContractWithCustomerExcludingAssessedTax"),
                # FIX: 한 해짜리 DDA 합계 태그를 빼야 DDA_PARTS가 쓰인다(2026-10-24)
                "0001035983": ("DepreciationAndAmortization",),
                # MSCI: 감가상각만인 DDA 합계 태그를 빼야 DDA_PARTS(감가상각 + 무형자산 상각)가 쓰인다(2026-10-23)
                "0001408198": ("DepreciationDepletionAndAmortization",),
                # NDAQ: DepreciationDepletionAndAmortization는 10-K 한 해(2025 $145M, 유형자산 감가상각만)뿐 — 현금흐름표 D&A(DepreciationAndAmortization, 인수 무형자산 상각 포함 TTM $657M)와 섞이면 D&A가 $169M으로 줄었다(Codex r1, 2026-10-23)
                "0001120193": ("DepreciationDepletionAndAmortization",),
                # RSG: 차원 없는 Revenues(Q2 2026 $5,076M)는 부문 간 거래 상계 전 합계 — 손익계산서 매출은 RevenueFromContractWithCustomerExcludingAssessedTax $4,430M(2026-10-23)
                "0001060391": ("Revenues",),
                # PCAR: DepreciationDepletionAndAmortization는 유형자산만(6개월 210.6) — 연결 D&A(DepreciationAndAmortization, 리스 장비 포함 415.1)로 이력을 맞춘다(Codex r1, 2026-10-23)
                "0000075362": ("DepreciationDepletionAndAmortization",),
                # GWW: DepreciationDepletionAndAmortization는 부문 주석 "감가상각·상각·비현금 리스비용" 합계(6개월 165) — 현금흐름표 D&A(DepreciationAndAmortization, 128)를 쓴다(Codex·Fable r1, 2026-10-23)
                "0000277135": ("DepreciationDepletionAndAmortization",),
                # DDOG: DepreciationDepletionAndAmortization(상반기 $34.1M)는 현금흐름표 "Depreciation and amortization"(DepreciationAndAmortization, $37.4M)보다 작다 — 현금흐름표 줄만(2026-10-21).
                "0001561550": ("DepreciationDepletionAndAmortization",),
                # WMB: RevenueFromContractWithCustomerExcludingAssessedTax는 대리·트레이딩 거래를 순액으로 줄이기 전 계약 매출(Q2 2026 $3,379M — 10-Q 주석 4
                # "Other adjustments" −$904M 전)이라 손익계산서 Total revenues($3,053M)보다 크다 — 섞여 최근 4분기 매출이 $15.4B(실제 $12.2B)였다. Revenues만(2026-10-19).
                "0000107263": ("RevenueFromContractWithCustomerExcludingAssessedTax",),
                # ELV: DepreciationDepletionAndAmortization(2023-06~ 8행)은 0·659 같은 다른 항목 값 — 감가상각은 현금흐름표 DepreciationAmortizationAndAccretionNet만(2026-10-17)
                "0001156039": ("DepreciationDepletionAndAmortization",),
                # NKE: 합산 태그 DepreciationDepletionAndAmortization이 2023-05부터라 기본 선택이 그것만 잡는다 — 구성요소 튜플(DDA_PARTS_BY_CIK)로 옛 Depreciation과 잇는다.
                "0000320187": ("DepreciationDepletionAndAmortization",),
                "0000277948": ("DepreciationDepletionAndAmortization",),   # CSX — 구성요소 튜플 경로로(DDA_PARTS_BY_CIK)
                "0001699150": ("DepreciationDepletionAndAmortization",),   # IR — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-25)
                "0000091440": ("DepreciationDepletionAndAmortization",),   # SNA — 연간 합산(상각 포함)이 분기 감가상각과 섞여 4분기만 커졌다 → 감가상각만(2026-10-25) [엔진수정대기]
                "0000313927": ("DepreciationDepletionAndAmortization",),   # CHD — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-25)
                "0001524472": ("DepreciationDepletionAndAmortization",),   # XYL — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-25)
                "0000832101": ("DepreciationDepletionAndAmortization",),   # IEX — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-25)
                "0000033185": ("DepreciationDepletionAndAmortization",),   # EFX — 손익 D&A(DepreciationAndAmortization)와 현금흐름 D&A가 섞여 TTM $755M(손익 $751.4M)이 되었다 → 손익 줄만(Codex r1, 2026-10-25)
                "0000072331": ("DepreciationDepletionAndAmortization",),   # NDSN — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-25)
                "0001579241": ("DepreciationDepletionAndAmortization",),   # ALLE — 합산 태그는 연간만이라 분기 DepreciationAmortizationAndAccretionNet과 섞여 4분기가 작아졌다 → 현금흐름 줄만(2026-10-25) [엔진수정대기]
                "0001336920": ("RevenueFromContractWithCustomerExcludingAssessedTax",),   # LDOS — 총매출(Revenues, Q2 FY26 $4,558M)로 통일: 고객 계약 매출($4,548M)과 섞여 YoY·TTM 정의가 달랐다(Codex r1, 2026-10-25)
                "0000008818": ("DepreciationDepletionAndAmortization",),   # AVY — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-25)
                "0000004904": ("DepreciationDepletionAndAmortization", "DepreciationAndAmortization", "PaymentsToAcquireProductiveAssets"),   # AEP — 감가상각은 구성요소 경로, 발전소 인수는 설비투자에서 뺌(2026-10-28)   # AEP — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-28)
                "0000040533": ("DepreciationAndAmortization",),   # GD — 합산 태그가 2019~2023 분기에 없다 → 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-25)
                "0001501585": ("DepreciationDepletionAndAmortization", "PaymentsToAcquireProductiveAssets"),   # HII — 구성요소 경로로(DDA_PARTS_BY_CIK), 설비투자는 PP&E 태그만(ProductiveAssets가 Q3 2025에 섞여 TTM $429M — 원문 $432M, Codex r1, 2026-10-25)
                "0000105770": ("DepreciationDepletionAndAmortization",),   # WST — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-25)
                "0000946581": ("DepreciationDepletionAndAmortization",),   # TTWO — 구성요소 경로로(DDA_PARTS_BY_CIK, 무형자산 상각 더함, 2026-10-24)
                "0000062709": ("DepreciationDepletionAndAmortization",),   # MRSH — 구성요소 경로로(DDA_PARTS_BY_CIK)
                "0001868275": ("DepreciationAmortizationAndAccretionNet",),   # CEG — 구성요소 경로로(DDA_PARTS_BY_CIK)
                # UPS: DepreciationDepletionAndAmortization(2023-12~ 7행, 2026 상반기 $1,600M)는 유형자산 주석의 감가상각 일부 — 연결 D&A는 현금흐름표
                # DepreciationAndAmortization(상반기 $1,965M, 최근 4분기 $3,863M). 합산 태그가 우선 잡혀 $940M 적었다(Codex 2026-10-22).
                "0001090727": ("DepreciationDepletionAndAmortization",),
                # TGT: DepreciationAndAmortization(분기 약 $650M)는 손익계산서 "매출원가 안 감가상각 제외" 줄 — 현금흐름표 합계 DepreciationDepletionAndAmortization(약 $780M)와 섞여
                # 최근 4분기 D&A가 $2,916M(실제 $3,173M)이었다(Codex 2026-10-22). 손익계산서 줄을 뺀다.
                "0000027419": ("DepreciationAndAmortization",),
                "0000723254": ("DepreciationDepletionAndAmortization",),   # CTAS — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-22)
                "0001140859": ("DepreciationDepletionAndAmortization",),   # COR — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-22)
                "0000315293": ("DepreciationDepletionAndAmortization", "DepreciationAndAmortization"),   # AON — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-22)
                "0001260221": ("DepreciationDepletionAndAmortization",),   # TDG — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-22)
                "0000815556": ("DepreciationDepletionAndAmortization",),   # FAST — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-22)
                "0001674101": ("DepreciationDepletionAndAmortization",),   # VRT — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-21)
                "0000097210": ("DepreciationDepletionAndAmortization",),   # TER — 구성요소 경로로(DDA_PARTS_BY_CIK, 2026-10-23)
                "0000075677": ("DepreciationDepletionAndAmortization",),   # PKG — 구성요소 경로로(DDA_PARTS_BY_CIK, 합산 태그 2015~2023 공백, 2026-11-07)
                "0000040545": ("RevenueFromContractWithCustomerExcludingAssessedTax",),
                # AMGN: DepreciationAndAmortization(분기 약 $220M)이 현금흐름표 "Depreciation, amortization and other"
                # (DepreciationDepletionAndAmortization, 분기 약 $1.1B)와 같은 기간에 함께 있어 먼저 공시된 작은 값이 섞였다 — EBITDA가 낮아
                # EV/EBITDA가 높게 나왔다(Fable, 2026-10-01).
                "0000318154": ("DepreciationAndAmortization",),
                # VLO: DepreciationAndAmortization은 판관비 줄 D&A(분기 $12~14M)뿐이다 — 큰 몫은 매출원가 줄(CostOfGoodsAndServicesSoldDepreciationAndAmortization,
                # 분기 $723~828M)이라 EBITDA ≈ 영업이익, EV/EBITDA 최고 452배였다. 현금흐름표 D&A(DepreciationAmortizationAndAccretionNet, 2025년 $3,158M)를 쓴다(Fable 2026-10-13).
                "0001035002": ("DepreciationAndAmortization",),
                # MCK: DepreciationDepletionAndAmortization(연간 FY2026 $287M)은 현금흐름표 D&A(감가상각 $256M + 상각 $473M = DepreciationAndAmortization
                # $729M)의 일부라 앞 태그가 이겨 EBITDA·DCF 감가상각이 절반 이하였다(MCD와 같은 유형, 2026-10-13).
                "0000927653": ("DepreciationDepletionAndAmortization",),
                # SYK: DepreciationDepletionAndAmortization(Q2 2026 $404M, 부문 주석 전체 D&A — 대여 수술기구 상각 등 포함)은 분기 값이 2024년부터라 EV/EBITDA 이력이
                # 240일이었고, 대여기구 구입비가 설비투자 줄에 없어(어디에 잡히는지는 공시로 확정 못 함 — 추정) DCF 순투자와 정의가 어긋날 수 있다. 현금흐름표 "Depreciation"(Q2 $121M) + "Amortization of intangible assets"($175M)로 전 기간 같은 정의를 쓴다(구성요소 경로, 2026-10-16).
                "0000310764": ("DepreciationDepletionAndAmortization",),
                # CME: DepreciationAndAmortization은 2020년부터 연간에만 실려 분기 TTM이 2019-12에 멈췄다(EV/EBITDA 계산 불가) — 손익계산서 두 줄
                # "Depreciation and amortization"(Depreciation, Q2 2026 $28.2M) + "Amortization of purchased intangibles"($56.0M)로(구성요소 경로, 2026-10-16).
                "0001156375": ("DepreciationAndAmortization",),
                # FCX: RevenueFromContractWithCustomerExcludingAssessedTax는 잠정 가격 조정을 뺀 "고객 계약 매출"(Q2 2026 $6,917M)이라 손익계산서 Revenues($7,029M)와
                # 분기마다 다르다 — Revenues만(MA·GE와 같은 처리, 2026-10-17).
                "0000831259": ("RevenueFromContractWithCustomerExcludingAssessedTax",),
                # MCD: DepreciationDepletionAndAmortization(분기 $111M)는 현금흐름표 D&A(DepreciationAndAmortization, 분기 $565M)의 일부라
                # 앞 태그가 이겨 EBITDA·DCF 감가상각이 낮았다(최근 4분기 $0.47B 대 약 $2.2B, 2026-10-02).
                "0000063908": ("DepreciationDepletionAndAmortization",),
                # WELL: RevenueFromContractWithCustomerExcludingAssessedTax는 시니어 주택 운영 매출만(Q2 2026 $2,985M)이고 임대 수익·이자
                # 수익을 뺀 값이다 — 손익계산서 총매출 Revenues($3,545M)만 쓴다(2026-10-02).
                "0000766704": ("RevenueFromContractWithCustomerExcludingAssessedTax",),
                # CPT: 손익계산서 총매출(Revenues)을 표준 태그로 내지 않고, 계약 매출 태그는 2019년부터 임대료를 뺀 분기 $3~13M뿐이다 —
                # 매출로 쓰면 PSR이 수천 배가 된다. 규칙(F2)으로 고칠 수 없어 매출 결측으로 둔다(input_fix_prereg F2 (d), 2026-10-10).
                "0000906345": ("RevenueFromContractWithCustomerExcludingAssessedTax",),
                "0000753308": ("RevenueFromContractWithCustomerIncludingAssessedTax",)}


# PFE: 2024년 10-K부터 RevenueFromContractWithCustomerExcludingAssessedTax를 제품 매출만(FY2023 $50.9B)으로 다시 정의했다 —
# 총매출 Revenues(FY2023 $58.5B)와 같은 날 공시돼 앞 태그가 이겨 2023년 4분기가 $6.7B(실제 $14.2B)로 나왔다. 2021년 분기는
# Revenues가 없어 옛 태그를 쓴다(그때는 총매출과 같은 값, 2026-10-02).
PREFER_TAGS = {"0000922224": ("Revenues",),   # PPL: 손익계산서 총매출(Q2 2026 $2,111M) — 계약 매출이 골라져 $2.14B로 나왔다(CNP·AEP와 같음, 2026-10-30)
               "0001130310": ("Revenues",),   # CNP: 손익계산서 총매출(Q3 2026 $2,191M) — 계약 매출(2,201)이 골라져 성장률·마진이 보도자료·부문표와 어긋났다(Codex·Fable r1, 2026-10-29)
               "0000004904": ("Revenues",),   # AEP: 손익계산서 총매출(Q3 2026 $6,832M) — 계약 매출(6,793)과 섞이면 성장률·마진이 어긋났다(Codex·Fable r1, 2026-10-28)
               "0000078003": ("Revenues",),
               # COP: 손익계산서 "Sales and other operating revenues"는 Revenues(Q2 2026 $19,161M)이고 RevenueFromContract…는 그중 고객 계약분
               # ($18,088M, 파생 계약 매출 제외)이다(10-Q 매출 주석, 2026-10-02).
               "0001163165": ("Revenues",)}


REV_TOTAL, REV_CONTRACT = "Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax"


def _prefer_total_revenue(merged, total_rows, contract_rows):
    """F2 (a)(input_fix_prereg, 2026-10-10): 계약 매출은 정의상 총매출의 일부다. 같은 시작일(회계연도·분기)에 두 태그가 함께 있는
    기간 가운데 가장 긴 기간에서 `Revenues` > 1.02 × 계약 매출이면, 그 시작일의 겹치는 기간 전부에서 계약 매출 행을 뺀다(총매출을 쓴다).
    리츠(UDR·AMT·SBAC…)는 계약 매출이 임대료를 빼 총매출의 수 %였고, GD 2017은 연간만 계약 매출이 작아 4분기가 음수가 됐다 —
    기간마다 따로 판정하면 9개월 누계가 계약 매출로 남아 4분기가 여전히 틀린다(Fable). `Revenues`가 2% 안에서 같거나 작으면
    (BLK·GIS처럼 `Revenues`에 일부만 실은 회사) 지금 규칙(먼저 공시된 행) 그대로다. 각 값은 그 기간에 처음 공시된 행으로 비교한다."""
    def first(rows):
        b = {}
        for r in rows:
            if "start" not in r:
                continue
            k = (r["start"], r["end"])
            if k not in b or r.get("filed", "") < b[k].get("filed", ""):
                b[k] = r
        return {k: r["val"] for k, r in b.items()}
    tot, con = first(total_rows), first(contract_rows)
    by_start = {}
    for k in tot.keys() & con.keys():
        by_start.setdefault(k[0], []).append(k)
    drop = set()
    for ks in by_start.values():
        k = max(ks, key=lambda x: x[1])                # 같은 시작일에서 가장 긴(가장 늦게 끝나는) 기간
        if tot[k] > 1.02 * con[k]:
            # 묶음 안에서도 두 값이 2% 안에서 같은 기간은 남긴다 — 같은 값인데 `Revenues` 행의 늦은 공시일이 가용일이 되지 않게(PFE 2022·IRM 2019, Fable)
            drop.update(x for x in ks if abs(tot[x] - con[x]) > 0.02 * max(abs(tot[x]), 1.0))
    if not drop:
        return merged
    return [r for r in merged if not (r.get("_tag") == REV_CONTRACT and (r.get("start"), r.get("end")) in drop)]


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
    rev_family = REV_TOTAL in names or REV_CONTRACT in names
    per_tag = {}
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
            rows = net_ocf(cik, rows)   # E57 — 청산소 담보금 유출입(CBOE). 짝 없으면 통과가 아니라 제외(위 중단영업 방식과 다르다)
        elif rows and name in FLOW_TAGS["ocf"]:
            rows = net_ocf(cik, rows)   # E57 — 다른 영업현금흐름 후보 태그(…ContinuingOperations)도 같은 규칙(시대 안 짝 없으면 제외)
        if rows:
            used.append(f"{name}({len(rows)})")
            if rev_family:   # 매출 행에는 태그를 적어 둔다(F2 — 사본이라 concept 캐시를 건드리지 않는다)
                rows = [dict(r, _tag=name) for r in rows]
                per_tag[name] = rows
            merged.extend(rows)
    # 설비투자를 두 줄로 나눠 내는 회사(SUM_TAGS_BY_CIK)는 같은 공시·같은 기간의 두 값을 더한 행을 만든다 — 위 병합은 대체 태그용이라 더하지 않는다.
    _sum = SUM_TAGS_BY_CIK.get(cik, {})
    for _std, _parts in _sum.items():
        if _std in names and taxonomy == "us-gaap":
            _rows = {}
            for _p in _parts:
                for r in concept(cik, _p, taxonomy):
                    _rows.setdefault((r.get("start"), r["end"], r.get("accn")), []).append(r)
            merged = [dict(v[0], val=sum(x["val"] for x in v)) for v in _rows.values() if len(v) == len(_parts)]
            used.append(f"합({'+'.join(_parts)} {len(merged)})")
    if rev_family and REV_TOTAL in per_tag and REV_CONTRACT in per_tag:
        merged = _prefer_total_revenue(merged, per_tag[REV_TOTAL], per_tag[REV_CONTRACT])
    # 합성 대상 회사는 영업이익 태그가 옛날에만 있어도(JNJ는 2015년까지) 합성값만 쓴다
    if "OperatingIncomeLoss" in names and cik in DERIVED_OPINC and taxonomy == "us-gaap":
        merged = _derived_opinc(cik, taxonomy)
        if merged:
            used.append(f"세전−영업외(합성 {len(merged)})")
    return ("+".join(used) if used else None), merged


# 4분기가 16주(나머지 12주)인 52·53주 회계 종목. quarterly_flow가 4분기를 연간에서 뺄 때 3분기 끝을 112일 전까지 찾는다.
LONG_Q4_TICKERS = {"COST", "PEP", "DPZ"}   # PEP: 12·12·12·16주(2026-10-01). DPZ도 12·12·12·16주(53주 해 Q4 17주, 2026-11-03)


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
    _ann_tag = {}
    for e in entries:   # 매출(태그가 적힌 행)은 태그별 연간 값 — 같은 종료일의 처음 공시
        if e.get("_tag") and "start" in e and "filed" in e and feh.days_between(e) > 350:
            k = (e["end"], e["_tag"])
            if k not in _ann_tag or e["filed"] < _ann_tag[k]["filed"]:
                _ann_tag[k] = e
    _ytd = {}
    for r in rows:   # 같은 결산일의 반기·9개월 누계(시작일 → 값) — 아래 누계 오태깅 판정용
        if 170 <= feh.days_between(r) <= 290:
            _ytd.setdefault(r["end"], []).append(r)

    def _bad_q(e):
        # 3개월 행의 값이 같은 결산일의 반기·9개월 누계와 똑같고, 그 누계의 앞 분기분(같은 시작일, 이 분기 시작 전날까지)이 0보다 크면
        # 누계를 3개월 기간으로 잘못 태깅한 것 — MRSH 2021 2분기 무형자산 상각 189(반기 누계, 실제 분기 89 — Codex 2026-10-18).
        # 직전 누계는 이 분기 바로 앞(시작일 전날 ±5일)에서 끝나야 하고 0이 아니어야 한다 — 같은 시작일의 아무 과거 행이나 인정하면
        # Q1 100·Q2 −100처럼 상반기 합이 0인 정상 Q3를 버렸다. 매출(태그가 적힌 행)은 같은 태그끼리만(Codex 2차 2026-10-18).
        for y in _ytd.get(e["end"], []):
            if y["val"] != e["val"] or y["start"] >= e["start"] or (e.get("_tag") and y.get("_tag") != e.get("_tag")):
                continue
            # 직전 누계는 이 분기 시작 **전에** 끝나야 한다(0~6일 앞) — 시작 뒤에 끝나는 다른 달력의 누계를 인정하면 VTRS 2020 분기(셸 회사 52주 달력 0)가
            # Upjohn 달력 1분기 누계 $2,588M과 이어져 버려지고 누계 차이로 −$2,588M이 만들어졌다(Codex 2026-10-25).
            if any(r["start"] == y["start"] and r["val"] != 0 and 0 <= (date.fromisoformat(e["start"]) - date.fromisoformat(r["end"])).days <= 6
                   and (not e.get("_tag") or r.get("_tag") == e.get("_tag")) for r in rows):
                return True
        # F2 (b)(2026-10-10): 매출(태그가 적힌 행)은 **같은 태그**의 연간 값과 2% 안이면 같은 값으로 본다 — ORCL FY2018은 재작성 연간
        # $39,383M을 3개월 기간으로 실었는데 처음 연간 값은 $39,831M이라 똑같지 않아 안 걸렸다. 다른 태그의 같은 값은 버리지 않는다(Codex).
        # 다른 항목은 지금처럼 같은 종료일 연간 값과 똑같을 때만.
        if e.get("_tag"):
            a = _ann_tag.get((e["end"], e["_tag"]))
            if not a or not (a["val"] and abs(a["val"] - e["val"]) <= 0.02 * abs(a["val"])):
                return False
        else:
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
                    "filed": max(cur["filed"], prev["filed"]),   # 누계 차이의 공개일은 두 누계 중 늦은 쪽(7-2 — 앞 누계가 나중에 처음 공시됐으면 그날, Codex 2차)
                    "start": prev["end"],
                }
            elif 80 <= gap <= 100 and q[cur["end"]]["filed"] > max(cur["filed"], prev["filed"]):
                # 3개월 직접값이 1년 뒤 비교 수치로만 처음 실리면 그 늦은 행이 골라져 그 분기 공개일이 1년 밀렸다 — 그때 이미 누계 차이로
                # 같은 값(±0.5%)을 알 수 있었으면 누계 차이와 그 공개일로(아래 4분기 규칙과 같은 조건, MRSH 2021 3분기 무형자산 상각 — Codex 2026-10-18)
                _d = cur["val"] - prev["val"]
                _qv = q[cur["end"]]["val"]
                # E70(2026-11-07): 같은 값이 아니어도(±5%) 3개월 직접값이 누계 차이보다 120일 넘게 늦게 처음 실렸으면 먼저 공개된 누계 차이로 —
                # 다른 태그·정의의 비교 열이 1년 뒤에야 실린 경우(PEP 2024 감가상각 DDA 누계 738·739 대 D&A 3개월 719·722, 2.6%: 분기 공개일 1년 밀림).
                # 5%를 넘는 차이(분사·매각 재작성 FIS·GE·DHR, 태그 섞인 누계 사다리)와 재작성 종목(나중 값을 일부러 씀)은 그대로.
                _late = (date.fromisoformat(q[cur["end"]]["filed"]) - date.fromisoformat(max(cur["filed"], prev["filed"]))).days
                if abs(_d - _qv) <= 0.005 * max(abs(_qv), 1) or (_late > 120 and abs(_d - _qv) <= 0.05 * max(abs(_qv), 1) and ticker not in feh.RESTATED_LATEST):
                    q[cur["end"]] = {**q[cur["end"]], "val": _d, "filed": max(cur["filed"], prev["filed"])}

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
                # 공개일은 역산에 쓴 자료 중 가장 늦은 날 — 연간 공시일만 쓰면 앞 분기 3개월 값이 연간보다 늦게 처음 실린 경우(다음 해 10-Q 비교
                # 수치) 그날 몰랐던 값이 섞였다(PEP 2024 4분기 감가상각 2025-02-04 → 2025-10-09, CBOE 2021 4분기 순이익 — Codex A3 r2, 2026-11-06)
                "filed": max([a["filed"]] + ([nine[0]["filed"]] if nine else [p["filed"] for p in parts])),
                "start": a["start"],
            }
        elif ok and a["end"] in q and q[a["end"]]["filed"] > a["filed"]:
            # 4분기 3개월 값을 나중 공시(다음 해 실적 8-K·10-K 비교 수치)가 처음 직접 실으면 그 늦은 행이 골라져 4분기 공개일이 1년 밀렸다
            # (PWR: 2025-02-20 실적 8-K XBRL에 2023년 4분기 — 2023-12~2024-12 영업이익 TTM이 전부 2025-02-20 공개, EV/EBITDA 138일 빔, 2026-10-17).
            # 연간 − 앞 세 분기로 같은 값(±0.5%)이 그때 알려졌으면 그 역산값과 그 날로 — 나중 값을 소급하지 않고, 기존 공개일보다 빠를 때만(Codex 2026-10-17).
            _d = a["val"] - sum(p["val"] for p in parts)
            _qv = q[a["end"]]["val"]
            _cand = max([a["filed"]] + [p["filed"] for p in parts])
            if abs(_d - _qv) <= 0.005 * max(abs(_qv), 1) and _cand < q[a["end"]]["filed"]:
                q[a["end"]] = {**q[a["end"]], "val": _d, "filed": _cand}
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
    # 결산일이 공시일보다 늦은 행(오태깅)은 결산일별 처음 공시를 고르기 **전에** 버린다 — 뒤에 나온 정상 행이 살아남게(component_sum과 같은 순서, E63 Codex)
    rows = [e for e in entries if "end" in e and "filed" in e and "start" not in e and e["end"] <= e["filed"]]
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


def wa_unit(wa, cover):
    """F3 (b)(input_fix_prereg, 2026-10-10): 희석 가중평균(WA) 단위 오류를 표지 주식 수로 가른다.
    WA > 5×10^10(S&P500 최대 NVDA 약 2.4×10^10)이면 천 단위 오타로 보고 ÷1e3(WAT 2026 82.1B 대 표지 98.1M).
    WA < 1e7이면 배율 {1, 1e3, 1e6} 중 표지에 가장 가까운 것(TER 164,050 → ×1e3, MCD 711 → ×1e6, NVR 3.3M → ×1).
    표지가 없으면 예전 규칙(1e6 미만 → ×1e6). 그 밖의 WA는 믿는다(PKG처럼 표지가 틀린 경우). 돌려주는 것: (WA, 배율 표시 또는 None)."""
    import math
    tag = None
    if wa > 5e10:
        wa, tag = wa / 1e3, "/1e3"
    if 0 < wa < 1e7:
        if cover and cover > 0:
            m = min((1, 1e3, 1e6), key=lambda k: abs(math.log(wa * k / cover)))
            if m != 1:
                wa, tag = wa * m, f"x{m:.0e}"
        elif wa < 1e6:
            wa, tag = wa * 1e6, "x1e6"
    return wa, tag


def wa_quarters(cik, ticker):
    """분기(80~100일) 희석 가중평균 주식 수, 공시일 순. 표지 주식 수처럼 그 공시 뒤 분할만큼 오늘 기준으로 맞춘다."""
    import splits as _splits
    _, rows = pick_tag(cik, ["WeightedAverageNumberOfDilutedSharesOutstanding"])
    sp = _splits.for_ticker(ticker)
    out = []
    for e in rows or []:
        if "start" in e and e.get("filed") and 80 <= (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days <= 100:
            out.append({"end": e["end"], "start": e["start"], "filed": e["filed"],
                        "val": e["val"] * (feh.split_ratio(e["filed"], sp) if sp else 1)})
    return sorted(out, key=lambda e: (e["filed"], e["end"]))


def check_shares(points, cik, ticker):
    """F3 (a): 배수 시리즈의 표지 주식 수를 그 시점까지 공시된 직전 분기 WA와 대조한다 — DCF(base_inputs)와 같은 규칙.
    표지 점과 WA 공시일을 합친 날짜마다 다시 대조한다(나중에 WA만 새로 나와도 갱신 — Codex 2026-10-10).
    20배 넘게 다르면 WA(단위 보정 뒤)를 쓰고(2026-10-10 사용자 결정 — 등록은 0.5~2배였다, 변경 기록), 2~20배면 표지를 두고 shares_suspect만,
    WA가 없고 표지가 1,000만 주 미만이면 그날부터 결측(None — 앞의 정상 점이 이어지지 않게).
    FOX '1'주·SPG 8,000주·CMG 27,962주·PKG 899억 주(표지 ×1000 오타). 돌려주는 것: (점들, dq 표시 목록)."""
    wq = wa_quarters(cik, ticker)
    if not points:
        return points, []
    pts = sorted(points, key=lambda e: e["available"])
    days = sorted({p["available"] for p in pts} | {w["filed"] for w in wq if w["filed"] >= pts[0]["available"]})
    out, dq, prev = [], [], None
    for day in days:
        p = newest_row([x for x in pts if x["available"] <= day])   # as_of와 같은 규칙(결산일이 가장 늦은 행 — 같은 공시일의 분기 WA보다 표지, CRWD 2025-06, E63)
        if p is None:
            continue                     # 그날까지 공개된 행이 모두 오태깅(결산일 > 공개일)
        cand = [w for w in wq if w["filed"] <= day]
        note = None
        wa_q = None
        if not cand:
            if p["val"] < 1e7:
                val, note = None, f"series_shares_missing:{day}:{p['val']}"
            else:
                val = p["val"]
        else:
            w = max(cand, key=lambda x: (x["end"], x["filed"]))
            wa, unit = wa_unit(w["val"], p["val"])
            if unit:
                note = f"weighted_shares_unit:{day}:{w['val']}{unit}"
            val = p["val"]
            r_ = p["val"] / wa if wa > 0 else None
            if r_ is not None and not (1 / 20 <= r_ <= 20):
                # 20배 넘게 다르면 단위 오류(FOX 1주·SPG 8,000·CMG·PKG ×1000·TER 천 단위) — WA로(2026-10-10 사용자 결정)
                val = wa
                wa_q = (w["start"], w["end"])
                note = f"shares_fallback_series:{day}:{p['val']}->{wa:.0f}"
                if unit or wa < 1e5:
                    dq.append(f"shares_suspect:{day}")
            elif r_ is not None and not (0.5 <= r_ <= 2.0):
                # 2~20배는 합병·상장·자본 재편 직후 WA가 뒤처진 경우가 많다(UBER 2019·PCG·IFF·WBD·CHTR 2026, Fable) — 표지를 두고 표시만
                dq.append(f"shares_suspect:{day}")
            elif p["val"] < 1e5 and wa < 1e5:
                dq.append(f"shares_suspect:{day}")
        if note:
            dq.append(note)
        if prev is None or (p["end"], val, wa_q) != prev:
            # wa_q: 이 값이 희석 가중평균(그 분기 시작·결산일)이면 — 카드별 증권 표가 그 분기 wa_shares를 빼고 날짜 값으로 바꾼다(E44 §3.2).
            # 값이 같아도 WA 분기가 바뀌면 새 행(표가 뺄 몫이 달라진다, Codex)
            out.append({"end": p["end"], "val": val, "available": day, **({"wa_q": wa_q} if wa_q else {})})
            prev = (p["end"], val, wa_q)
    return out, dq


ASOF_REF = None   # 연구용 시점 재현의 평가일(research/pit.py). 카드는 None(오늘).


def live_combined(cik):
    """합산 감가상각 태그. 오래전에 멈췄으면(AVGO는 2018-05 두 건뿐, 이후 구성요소로만
    보고) 없는 것으로 보고 구성요소로 넘긴다 — 멈춘 합산 태그가 잡히면 구성요소 경로에
    가지 못해 EV/EBITDA가 통째로 빠진다(2026-09-25)."""
    if cik in DDA_SPLIT_BY_CIK:
        return f"{DDA_SPLIT_BY_CIK[cik]['total']}(+분할 뒤 {DDA_SPLIT_BY_CIK[cik]['add']})", split_era_dda(cik)
    tag, rows = pick_tag(cik, DDA_COMBINED)
    # 기준일: 카드는 오늘, 연구용 시점 재현은 평가일(ASOF_REF — research/pit.py가 넣는다, C8). 오늘 기준으로만 재면 과거 평가일에
    # 살아 있던 합산 태그도 지금 멈췄다는 이유로 버려진다(Codex).
    ref = date.fromisoformat(ASOF_REF) if ASOF_REF else date.today()
    stale = date.fromordinal(ref.toordinal() - 730).isoformat()
    if rows and max(r["end"] for r in rows) < stale:
        return None, []
    return tag, rows


def dda_quarters(cik, ticker):
    """감가상각 분기 시리즈. 합산 태그 우선, 없으면 구성요소를 더한다."""
    tag, rows = live_combined(cik)
    if rows:
        q = quarterly_flow(rows, ticker)
        # 연구용 시점 재현(ASOF_REF)에서는 연간만 남은 합산 태그가 "살아 있다"고 판정돼 분기가 비거나(DHR·EME) 분기가 오래돼
        # 영업이익과 짝이 안 맞으면(ACN 2020-08·IEX·FE — Fable, C8) EBITDA가 통째로 빠졌다. 그때만 구성요소로 넘어간다.
        # 카드 경로(ASOF_REF None)는 그대로.
        if not ASOF_REF:
            return tag, q
        # 기준은 실제 짝짓기다 — 합산 분기의 마지막 결산일이 영업이익 분기보다 MAX_PAIR_LAG_DAYS 넘게 뒤처지면 EBITDA가 안 나오므로
        # 구성요소로(IEX 2025-07: 평가일 시차 304일로 통과했지만 영업이익과 짝이 안 맞았다 — Fable 3차). 영업이익 분기를 모르면 평가일 시차로.
        if q:
            q_end = date.fromisoformat(max(e["end"] for e in q))
            _, orows = pick_tag(cik, EBITDA_TAGS["opinc"])   # EBITDA 짝짓기에 쓰는 영업이익 태그와 같다
            oq = quarterly_flow(orows, ticker) if orows else []
            if oq:
                if (date.fromisoformat(max(e["end"] for e in oq)) - q_end).days <= MAX_PAIR_LAG_DAYS:
                    return tag, q
            elif (date.fromisoformat(ASOF_REF) - q_end).days <= MAX_PAIR_LAG_DAYS + 120:
                return tag, q
    # 구성요소마다 그 분기가 **처음 공시된 때**가 다르다. 작은 항목이 1년 뒤 비교
    # 수치로 처음 나오면(GOOGL 무형자산 상각 $0.12B·금융리스 상각 $0.1B), 예전에는
    # 분기 공개일을 가장 늦은 항목 날짜로 잡아 과거 분기 전체가 1년 늦게 "공개"된
    # 셈이 됐고 EV/EBITDA 이력이 44일만 남았다(2026-09-24). 결산 후 LATE_PART_DAYS
    # 안에 공시된 항목만 그 분기에 더한다 — 그때 알 수 없던 값은 빼는 것이 시점 규칙이다.
    LATE_PART_DAYS = 120
    per_end = {}
    used = []
    for name in DDA_PARTS_BY_CIK.get(cik, DDA_PARTS):
        # 튜플은 **같은 줄의 두 태그 이름**(분기는 한 이름, 10-K 연간은 다른 이름 — CME) — 행을 합쳐 4분기를 연간 − 9개월로 만든다
        part = sum((concept(cik, n) for n in name), []) if isinstance(name, tuple) else concept(cik, name)
        if not part:
            continue
        used.append("|".join(name) if isinstance(name, tuple) else name)
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
            # 튜플(이름만 바뀐 같은 줄)은 새 이름이 옛 분기를 비교 수치로 다시 실어 quarterly_flow가 그 늦은 행을 고른다 — 공개일은 처음 알려진 날로
            # (NKE 2024-11·2025-02 분기가 2025-12·2026-04 공개로 잡혀 EV/EBITDA가 2025-07~2026-03 비었다, 2026-10-17)
            # 단, 처음 알려진 날 공개된 행만으로 같은 값이 나올 때만 — 나중 비교 수치가 고쳐진 값이면 소급하지 않는다(Codex 2026-10-17)
            f_, v_ = e["filed"], e["val"]
            if isinstance(name, tuple) and known < e["filed"]:
                _early = {x["end"]: x["val"] for x in quarterly_flow([r for r in part if r.get("filed", "9999") <= known], ticker)}
                if e["end"] in _early and abs(_early[e["end"]] - e["val"]) <= 0.005 * max(abs(e["val"]), 1):
                    f_, v_ = known, _early[e["end"]]   # 그때 알던 값으로(Codex PWR 검토 — 나중 값을 소급하지 않는다)
            slot = per_end.setdefault(e["end"], {"val": 0.0, "filed": f_})
            slot["val"] += v_
            slot["filed"] = max(slot["filed"], f_)
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


def _period_ends(cik):
    """그 회사 재무상태표 결산일 — 총자산·자본·부채와자본 합계 시점 행 결산일의 합집합(component_sum 날짜 가드용).
    캐시하지 않는다: 연구 재현(pit)은 한 프로세스에서 평가일마다 자료를 바꿔 끼우므로 CIK만 키로 남기면 첫 평가일 결산일로
    뒤 평가일 행을 통째로 버렸다(Fable E63 r2). concept()가 이미 자료 단위로 기억한다."""
    ends = set()
    for tag in ("Assets", "StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
                "LiabilitiesAndStockholdersEquity"):
        ends |= {date.fromisoformat(e["end"]) for e in concept(cik, tag) if "end" in e and "start" not in e}
    return sorted(ends)


def _near_period_end(cik, end, before=7, after=0):
    """end가 재무상태표 결산일 **이전 7일 ~ 당일** 안인가. 결산일 다음 날짜(ASC 842 도입일 2019-01-01 리스, 분사일 개시 재무상태표)는
    결산일보다 늦어 '결산일이 가장 늦은 행' 규칙이 고르는 꼴이라 막는다(Fable E63 r2). 52/53주 회계연도 차이는 결산일 쪽 태그가 덮는다."""
    import bisect
    ends = _period_ends(cik)
    if not ends:
        return True                      # 결산일 근거가 없으면 거르지 않는다
    d = date.fromisoformat(end)
    i = bisect.bisect_left(ends, d)                  # ends[i] ≥ d
    if i < len(ends) and (ends[i] - d).days <= before:
        return True                                  # 결산일 이전 before일 ~ 당일
    return i > 0 and (d - ends[i - 1]).days <= after


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
        # 결산일이 공시일보다 늦은 행(만기일·오태깅 — GD 2012-12-31 현금을 2012-05-01 10-Q에)은 버린다. 같은 결산일의 가장 먼저 공시된 행을
        # 고르기 전에 걸러야 뒤에 나온 정상 행(GD 10-K 3,296)이 살아남는다(Fable r3, 2026-10-25).
        rows = [e for e in concept(cik, tag) if "end" in e and "filed" in e and "start" not in e and e["end"] <= e["filed"]]
        # 재무상태표 결산일 ±7일 밖 날짜(분기 중간 거래일·분사일 단독 태그 행 — JNJ CommercialPaper 2024-05-15 $3.6B, VMC 2022-08-31)는
        # 그 항목의 총계가 아니다. 결산일이 늦다는 이유만으로 분기말 총계를 이기지 않게 버린다(안건 E63, Codex·Fable 2026-10-29).
        rows = [e for e in rows if _near_period_end(cik, e["end"])]
        best = {}
        for e in rows:
            if e["end"] not in best or e["filed"] < best[e["end"]]["filed"]:
                best[e["end"]] = e
        for end, e in best.items():
            slot = per_date.setdefault(end, {"val": 0.0, "filed": e["filed"], "parts": []})
            slot["val"] += e["val"]
            slot["filed"] = max(slot["filed"], e["filed"])
            slot["parts"].append((e["filed"], e["val"], tag))
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
    # 시점 인식 합산(안건 E65): 결산일마다 구성요소 첫 공시일 순서로 **그날까지 공개된 구성요소의 합**을 행으로 낸다. 마지막 행은
    # 예전과 같은 완전한 합·최대 공시일이다. 예전에는 슬롯 공개일 = 구성요소 공시일 최대라, 1년 뒤 비교 열로 처음 태깅된
    # 구성요소 하나가 분기말 총계 전체를 1년 "미공개"로 만들었다(META 차입 2026-01-29~04-29에 2025-09-30 $28.8B — 12-31 $58.7B는
    # 10-K 2026-01-29 공시, 54종목 5,247거래일 — Fable 2026-10-29). 결산일별로 한 줄을 기대하는 호출부({end: 행})는 마지막 행 = 예전 값을 받는다.
    # 부분 합은 그날까지 모인 태그가 **직전 4개 결산일 태그의 합집합을 모두 포함할 때만** 낸다(Fable·Codex E65 r1·r2).
    # 직전 하나만 보면 연말에만 태깅되는 구성요소(GS 단기차입 $61B는 10-K에만)·성긴 비교열(TDG 리스)을 뚫었다(r2). 큰 구성요소가 늦게 오는 회사
    # (EXC: 10-K에는 단기 + 1년 안 만기만, 장기 비유동분 $47B는 다음 10-Q 비교 열에서 처음)는 부분 합이 완전한 합의 5%라, 직전 분기
    # 완전한 합을 쓰던 예전보다 훨씬 틀렸다. 직전 결산일이 없으면 부분 합을 내지 않는다.
    out = []
    prev_tags = None
    recent = []                          # 직전 결산일들의 태그 집합(최근 4개)
    for k in sorted(per_date):
        v = per_date[k]
        acc, parts, i, seen = 0.0, sorted(v["parts"]), 0, set()
        while i < len(parts):
            f = parts[i][0]
            while i < len(parts) and parts[i][0] == f:
                acc += parts[i][1]
                seen.add(parts[i][2])
                i += 1
            if i == len(parts) or (prev_tags is not None and seen >= prev_tags):
                out.append({"end": k, "val": acc, "available": f})
        recent = (recent + [{t for _, _, t in parts}])[-4:]
        prev_tags = set().union(*recent)
    return sorted(out, key=lambda e: (e["available"], e["end"]))


# 같은 항목의 **대체 태그**라 더하면 안 되는 EV 구성요소. 날짜마다 앞 태그 우선으로 하나만 쓴다.
# 우선주 총계(PreferredStockValue)와 전환우선주(ConvertiblePreferredStock…)를 함께 내는 회사는
# component_sum으로 더하면 두 배가 된다(Codex 지적, 2026-09-24).
# 단기투자(sti) 네 태그는 기본으로 더하지 않는다 — 같은 날 같은 값을 두 태그로 낸 회사(META 2021-12-31 MarketableSecuritiesCurrent·
# AvailableForSaleSecuritiesDebtSecuritiesCurrent 둘 다 $31,397M → 합 $62,794M), 매도가능 채권(부분)과 단기투자 총계를 함께 낸 회사(PYPL
# ShortTermInvestments 6.65 ⊃ AFS 5.51, QCOM·UPS)가 있어 더하면 이중이 된다. 앞 태그(총계 쪽)가 이긴다(안건 E67, 2026-11-05 — 2021-06 이후
# 같은 날 두 태그 48건 전부 앞 태그가 총계거나 같은 값)
PICK_COMPONENTS = {"preferred", "sti"}
# IFRS 16 회사 — 임차료 대신 사용권자산 감가상각과 리스 이자를 인식하므로 리스부채를 빚으로 둔다(B16). DCF(build_dcf.IFRS_LEASE)도 이 목록을 쓴다
IFRS_LEASE = {"TSM", "SKHY"}
# 리스 태그(OperatingLeaseLiability…)가 운용 + 금융리스 합계인 회사(CIK) — 운용리스를 뺄 때 금융리스(빚)는 남긴다(B16). DCF도 이 목록을 쓴다.
# MCD: 10-K 리스 주석 표 2025-12 $694M·$14,147M이 합계(금융 약 $2.4B), GD: 리스 태그 330·1,633이 합계(금융 $392M, Fable r1 2026-10-25)
LEASE_INCLUDES_FINANCE = {"0000063908", "0000040533"}


def finance_lease_series(cik):
    """금융리스 부채 시리즈 — 합계 태그(FinanceLeaseLiability), 유동 + 비유동이 더 최근이면 그쪽(DCF base_inputs와 같은 고르기)."""
    tot = component_sum(cik, ["FinanceLeaseLiability"])
    parts = component_sum(cik, ["FinanceLeaseLiabilityCurrent", "FinanceLeaseLiabilityNoncurrent"])
    if not tot:
        return parts
    if parts and max(e["end"] for e in parts) > max(e["end"] for e in tot):
        return parts
    return tot
# 단기투자 지정 태그가 재무상태표의 서로 다른 줄이라 더해야 하는 회사 — KO: OtherShortTermInvestments(정기예금)와 MarketableSecurities.
# DXCM·INTU·NKE의 지정 목록(AFS 두 이름)은 태그 이름 변경이라 하나만(같은 결산일 같은 값 — DXCM 2024-12 $1,730M 둘, Codex E67 r1)
STI_SUM_CIKS = {"0000021344"}


def pick_instant(cik, tags):
    """시점값을 태그 목록 순서대로 골라 하나의 시리즈로 — 날짜마다 앞 태그가 우선.
    시점 규칙(E67 Codex r1): 결산일마다 **그때까지 공개된 태그 중** 가장 앞 태그를 쓴다 — 앞 태그가 나중에 처음 공개되면(태그 이름 변경:
    DXCM 새 AFS 태그 2025-07-30 대 옛 태그 2025-02-18) 그 전에는 옛 태그 행, 앞 태그가 공개된 날부터 앞 태그 행(같은 결산일·늦은 공개 →
    newest_row가 고른다). 결산일 ±7일 밖 날짜(분기 중간 단독 행)는 component_sum과 같게 버린다."""
    cands = {}
    for rank, tag in enumerate(tags):
        for e in concept(cik, tag):
            if "end" not in e or "filed" not in e or "start" in e or e["end"] > e["filed"]:   # 미래 날짜 행 — component_sum과 같게(2026-10-25)
                continue
            if not _near_period_end(cik, e["end"]):
                continue
            k = (e["end"], rank)
            if k not in cands or e["filed"] < cands[k]["filed"]:
                cands[k] = {"val": e["val"], "filed": e["filed"]}
    by_end = {}
    for (end, rank), c in cands.items():
        by_end.setdefault(end, []).append((c["filed"], rank, c["val"]))
    out = []
    for end, lst in by_end.items():
        best = None
        for filed, rank, val in sorted(lst):
            if best is None or rank < best:   # 더 앞 태그가 공개된 날부터 그 값으로
                best = rank
                out.append({"end": end, "val": val, "available": filed})
    return sorted(out, key=lambda e: (e["available"], e["end"]))


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
DEBT_TOTAL_TAG = {"0000874761": ["RecourseDebtTotalAes", ("NonRecourseDebtCurrentAes", "ShortTermBorrowingsNonrecourseAes"), ("NonRecourseDebtNonCurrentAes", "LongTermDebtNonrecourseAes")],   # AES: 재무상태표 차입금이 차원(RecourseStatusAxis)으로만 — 모회사 보증 차입 총액 $6,361M(공정가치 주석 장부가, 1년 안 몫 포함 — 2025-12 879 + 5,105 = 5,984) + 비소구 1년 안 $2,950M + 비소구 장기 $23,953M = $33,264M(Q3 2026 10-Q). BUILD dim_facts — 옛 공시는 비소구를 회사 고유 태그(aes:NonRecourseDebtCurrent·NonCurrent, BUILD company_tags)로 냈다 — 튜플은 회사 태그 먼저: 10-K는 회사 태그, 10-Q는 차원 값이라 차원을 앞에 두면 연말이 두 행(10-K·다음 10-Q)이 되고 합계 경로가 둘을 더해 두 배가 됐다. 빠지면 2021-12 등이 모회사 몫만 남았다(Codex r1). 비소구 차입에 금융리스 포함(10-K 주석 12·15)(2026-11-07)
                  "0001032208": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # SRE: 단기 $4,438M + 1년 안 장기·금융리스 $1,528M + 장기·금융리스 $31,508M = $37,474M(Q3 2026 10-Q). SI Partners 차입은 "매각 예정 부채"에 묶여 빠진다(2026-11-07)
                  "0001474735": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # GNRC: 단기 $53.1M + 1년 안 만기(금융리스 포함) $36.7M + 장기(금융리스 포함) $1,243.7M = $1,333.6M(금융리스 $91.0M 포함 — EV에 금융리스가 들어간다). 기본은 텀론 원금에 1년 안 만기를 다시 더해 $1,268.7M(Codex r1, 2026-11-08)
                  "0001000228": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # HSIC: 은행 신용한도 $1,000M + 1년 안 만기 $142M + 장기 $2,382M = $3,524M — 기본은 1년 안 만기를 빼 $3,382M(2026-11-07)
                  "0001285785": ["OtherShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # MOS: 단기 $511.6M + 1년 안 만기 $68.7M + 장기 $5,332.8M = $5,913.1M — 기본은 1년 안 만기를 빼 $5,844.4M(2026-11-07)
                  "0000010456": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # BAX: 1년 안 $844M + 장기 $7,757M(2026년부터 회사 고유 태그 — BUILD company_tags로 표준 이름에) — 없으면 차입금 0(2026-11-07)
                  "0001031296": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # FE: 1년 안 만기 포함 총차입금(기본은 1년 안을 빼 $27,896M — 사전 조사 2026-10-29)
                  "0000715957": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # D: 단기 $3,308M + 1년 안 만기 $2,399M + 장기 $48,939M(후순위채 $7,461M·증권화 채권 포함) = $54,646M(Q3 2026 10-Q). 기본 경로는 1년 안 몫을 빠뜨려 $52,247M이었다(2026-11-07)
                  "0001410636": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # AWK: CP $1,449M + 1년 안 장기부채 $898M + 장기 $13,987M = $16,334M(Q3 2026 10-Q 재무상태표, XEL과 같은 구성). 기본 LongTermDebt는 2020에 멈췄다(2026-11-07)
                  "0001267238": ["UnsecuredDebt"],   # AIZ: 무담보 선순위·후순위채 $2,208.7M(Q3 2026 10-Q 재무상태표 "Debt") — 2008~ 분기마다 이 태그. 기본은 LongTermDebt가 2020-03에 멈춰 낡은 값이 잡혔다(2026-11-06)
                  "0000783325": ["ShortTermBorrowings", "LongTermDebtCurrent", "LongTermDebtNoncurrent"],   # WEC: 단기(CP) $1,904.3M + 1년 안 장기부채 $1,134.5M + 장기 $19,717.2M = $22,756.0M(Q3 2026 10-Q MD&A "Total debt"와 같다, 전환사채·후순위채 포함, 2026-11-03)
                  "0000940944": ["ShortTermBorrowings", ("LongTermDebt", "LongTermDebtNoncurrent")],   # DRI: 단기(CP + 1년 안 채권 $500M) $979.7M + 장기 $1,636.1M = $2,615.8M(Q1 FY27 10-Q). 기본은 단기만 잡혔다. 2023-05 전 장기는 LongTermDebtNoncurrent. 2026-05 LongTermDebtCurrent $693.6M은 단기 줄과 같은 값이라 빼다(2026-11-03)
                  "0001513761": ["LongTermDebtAndCapitalLeaseObligations", "LongTermDebtAndCapitalLeaseObligationsCurrent"],   # NCLH: 대차대조표 비유동 $13,951.5M + 유동 $1,135.0M = $15,086.5M(Q3 2026 10-Q). ...IncludingCurrentMaturities $15,498M은 원금 상환표 합계라 쓰지 않는다(2026-11-04)
                  "0001286681": ["LongTermDebtAndCapitalLeaseObligations", "LongTermDebtAndCapitalLeaseObligationsCurrent"],   # DPZ: 증권화 채권 비유동 $3,559M + 1년 안 $1,327M(2027-07 ARD 재분류) = $4,886M(금융리스 포함, Q3 2026 10-Q). 기본은 비유동만(2026-11-03)
                  "0000040987": ["ShortTermBorrowings", "LongTermDebtCurrent", "LongTermDebtNoncurrent"],   # GPC: 단기 $388M(CP 포함) + 1년 안 $250M + 장기 $4,472M = $5,110M(Q3 2026 10-Q). 기본은 CP를 단기 차입과 또 더해 $5,499M(2026-11-03)
                  "0000764478": [("DebtAndCapitalLeaseObligations", "LongTermDebt")],   # BBY: 총차입(유동 포함, 금융리스 $32M 포함) $1,169M(Q2 FY27 10-Q) — FY26 10-K부터 새 태그, 그 전은 LongTermDebt(겹치는 날 값 같음). 기본은 비유동 $1,158M만(2026-11-03)
                  "0000822416": "NotesPayable",   # PHM: 주택건설 차입금 $1,808.9M(선순위채 $1,783.5M + 토지 어음 $25.4M, Q3 2026 10-Q). 기본은 LongTermDebt $43.9M(2025-12, 의미 불명). 모기지 자회사 환매 차입 $383.2M(회사 태그)은 매각 예정 대출 $433.9M로 담보된 운전자본성이라 넣지 않는다(2026-11-03)
                  "0001300514": "LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities",   # LVS: 유동 $1,566M + 비유동 $13,878M = $15,444M(금융리스 $147M 포함, Q3 2026 10-Q). 기본은 2025-12 10-K 값에 멈춰 $15,770M(2026-11-03)
                  "0001116132": ["LongTermDebt", "LongTermDebtCurrent"],   # TPR: 장기 순액(할인·발행비 차감) $2,379.0M + 1년 안 $0(FY26 10-K). 기본은 채권 액면 합 LongTermDebtNoncurrent $2,396.6M이 잡혔다(2026-11-03)
                  "0001967680": ["LongTermDebt"],   # VLTO: 총차입 $2,920M = CP $249M(DebtCurrent) + 장기 $2,671M(Q3 2026 10-Q) — 기본은 장기만 $2,671M(2026-10-30)
                  "0000922224": ["ShortTermBorrowings", "LongTermDebtCurrent", "LongTermDebtNoncurrent"],   # PPL: 단기 $65M + 1년 안 장기부채 $469M + 장기 $19,789M = $20,323M(Q2 2026 10-Q, 자회사 값은 LegalEntityAxis라 제외, 2026-10-30)
                  "0000352541": [("CommercialPaper", "ShortTermBorrowings"), "OtherShortTermBorrowings", "LongTermDebtCurrent", "LongTermDebtNoncurrent"],   # LNT: CP $708M + 기타 단기(텀론) $400M + 1년 안 장기부채 $374M + 장기 $10,636M = $12,118M(Q2 2026 10-Q MD&A "Total debt"와 같다, 2026-10-30)
                  "0001711269": [("ShortTermBankLoansAndNotesPayable", "CommercialPaper"), "TransfersAccountedForAsSecuredBorrowingsAssociatedLiabilitiesCarryingAmount", "LongTermDebtCurrent", "LongTermDebtNoncurrent"],   # EVRG: 어음·CP $2,331.0M + 매출채권 담보차입 $356.0M + 1년 안 장기부채 $1,495.3M(전환사채 포함) + 장기 $12,315.7M = $16,498.0M(Q2 2026 10-Q, 증권화 채권 $288.1M은 장기부채 안, 2026-10-30). 어음·CP 줄이 없는 분기는 CommercialPaper(튜플 — 이력 2025-12가 $13,487.9M으로 덜 잡혔다, Codex r1)
                  "0001442145": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # VRSK: 1년 안 $257.7M(364일 텀론 $249.4M + 금융리스) + 장기 $4,215.8M(선순위채 8건 + 금융리스) = $4,473.5M(Q2 2026 10-Q, 2026-10-30)
                  "0001065088": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # EBAY: 1년 안 $1,599M(CP $750M·장기 유동 $850M 포함) + 장기 $5,134M = $6,733M(Q3 2026 10-Q) — 기본은 $5,989M(2026-10-30)
                  "0000927066": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # DVA: 1년 안 $112.5M + 장기 $10,656.6M = $10,769.1M(금융리스 $151.6M 포함, Q3 2026 10-Q) — 기본은 장기만 잡고 금융리스를 또 더했다(2026-10-30)
                  "0001014473": ["SeniorNotesCurrent", "SeniorLongTermNotes"],   # VRSN: 1년 안 선순위 채권 + 장기 선순위 채권 = $1,785.9M(Q3 2026 10-Q, 7/20 상환 뒤 — 기본은 태그를 못 찾아 0, Codex r1 2026-10-29)
                  "0001130310": ["ShortTermBorrowings", "OtherLongTermDebtCurrent", "LongTermDebtNoncurrent"],   # CNP: 단기 0 + 1년 안 기타 1,106 + 장기 23,677(증권화 1,747 + 기타 21,930) = $24,783M(Q3 2026 10-Q — 기본은 장기만 $23,677M; 1년 안 증권화채 $120M은 회사 고유 태그 cnp:라 엔진이 못 읽어 빠진다, 0.5%, 2026-10-29)
                  "0000048898": ["DebtCurrent", "LongTermDebtNoncurrent"],   # HUBB: 1년 안(CP 313 + 유동 채권 300) $613.8M + 장기 $4,506.4M = $5,120.2M(Q3 2026 10-Q — 기본은 $4,821M로 CP가 빠졌다, 2026-10-29)
                  "0001069202": ["CommercialPaper", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # LII: CP $455.1M + 1년 안 $319.2M + 장기 $847.1M = 주석 총차입 $1,621.4M(금융리스 포함, Q3 2026 10-Q — 기본은 1년 안을 빼 $1,302M, 2026-10-29)
                  "0001932393": ["LongTermDebt"],   # GEHC: ShortTermBorrowings가 1년 안 장기차입을 이미 담아 기본 합산이 이중으로 셌다(2025-09 $2,005M + $2,002M) — 총계 $9,973M(Fable·Codex r1, 2026-10-28)
                  "0001633917": ["DebtCurrent", "LongTermDebtNoncurrent"],   # PYPL: 1년 안(장기채 유동분 + CP $200M) $2,533M + 장기 $10,939M = $13,472M(기본은 CP를 빠뜨렸다, 2026-10-28)
                  "0000004904": ["ShortTermBorrowings", "LongTermDebt"],   # AEP: 단기(유동화 900 + CP 등) + 장기(1년 안 포함) — 기본은 CP를 한 번 더 셌다(Q3 2026 $54,416M, 2026-10-28)
                  "0001109357": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtNoncurrent", "LongTermDebtToFinancingTrusts"],   # EXC: 단기 $1,243M + 1년 안 $727M + 장기 $50,313M + 금융신탁 $390M = $52,673M(Q2 2026 10-Q, 2026-10-28) — 금융신탁은 회사 태그 exc:LongTermDebtToFinancingTrusts라 us-gaap 이름으로는 안 잡혀 엔진 값은 $52,283M
                  "0001506307": ["DebtCurrent", "LongTermDebtNoncurrent"],   # KMI: 1년 안(CP 포함) $1,726M + 장기 $31,347M = $33,073M(Q3 2026 10-Q — 기본은 장기만, 2026-10-27)
                  # NCLH: 차입금을 금융리스 포함 장기차입 비유동(LongTermDebtAndCapitalLeaseObligations) + 1년 안(…Current)으로만 낸다(2012~, 분기마다) — 기본 태그는
                  # LongTermDebt 2020-12-31 $1,552M에서 멈춰 그 뒤 차입금이 0이 됐다(Fable r2). 2025-12-31 13,730 + 876 = 14,606 = DebtAndCapitalLeaseObligations(10-K, 2026-10-25).
                  "0001513761": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  "0000813672": ["UnsecuredLongTermDebt"],   # CDNS: 무담보 사채 $2,482M(Q2 2026 10-Q — 주석 LongTermDebt는 발행 때 순조달액이라 쓰지 않는다, 2026-10-25)
                  "0000040533": ["DebtCurrent", "LongTermDebtNoncurrent"],   # GD: 1년 안 $1,256M + 장기 $6,260M = $7,516M(Q2 2026 10-Q — 기본은 장기만, 2026-10-25)
                  "0000860730": ["DebtLongtermAndShorttermCombinedAmount"],   # HCA: 단기·CP·1년 안 포함 총차입금 $49,718M(Q2 2026 10-Q — 기본은 장기 비유동만 $43,454M, 2026-10-25)
                  "0001103982": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # MDLZ: 단기 $2,327M + 1년 안 $2,663M + 장기 $16,460M(Q2 2026 10-Q — 기본 합산은 1년 안을 빠뜨렸다, 2026-10-25)
                  "0000079879": ["DebtCurrent", "LongTermDebtNoncurrent"],   # PPG: 1년 안·단기 $691M + 장기 $6,195M(Q2 2026 10-Q — LongTermDebt $6,876M은 1년 안 포함이라 DebtCurrent와 겹침, 2026-10-25)
                  "0001145197": ["LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities"],   # PODD: 1년 안 포함 합계 $948.4M(Q2 2026 10-Q, 2026-10-25)
                  "0000008818": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # AVY: 1년 안 $500.5M + 장기 $3,177.7M(Q2 2026 10-Q — LongTermDebt는 2025-12에 끊김, 2026-10-25)
                  "0000009389": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # BALL: 1년 안 $692M(만기 649 포함) + 장기 $6,528M(Q2 2026 10-Q, 2026-10-25)
                  "0001336920": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # LDOS: 1년 안 $22M + 장기 $6,009M(Q2 FY26 10-Q, 2026-10-25)
                  "0000033185": ["DebtCurrent", "LongTermDebtNoncurrent"],   # EFX: 1년 안 $157.7M + 장기 $5,049.0M(Q3 2026 10-Q — LongTermDebt 태그는 10-K만, 2026-10-25) [엔진수정대기]
                  "0001524472": ["DebtCurrent", "LongTermDebtNoncurrent"],   # XYL: 단기·1년 안 $531M + 장기 $2,395M(Q2 2026 10-Q — 기본은 장기만, 2026-10-25)
                  "0001111711": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # NI: 단기 $692.0M + 1년 안 $1,098.4M + 장기 $15,612.6M(Q2 2026 10-Q — 기본 합산은 1년 안을 빠뜨렸다, 2026-10-25)
                  "0000313927": ["ShortTermBorrowings", "LongTermDebt"],   # CHD: 기업어음 $49.9M + 장기 $2,206.3M — 기본 합산이 CommercialPaper(같은 금액)를 또 더했다(Q2 2026 10-Q, 2026-10-25)
                  "0000091440": ["LongTermDebt"],   # SNA: LongTermDebt $1,205.1M = 1년 안 만기·어음 $317.9M 포함 합계(Q3 2026 10-Q, 2026-10-25)
                  "0001699150": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # IR: 1년 안 $699.8M + 장기(이름과 달리 비유동만) $4,068.7M(Q2 2026 10-Q, 2026-10-25)
                  "0000726958": ["LongTermDebtCurrent", "LongTermDebtNoncurrent"],   # CASY: 1년 안 $104.3M + 장기 $2,326.2M(Q1 FY27 10-Q — LongTermDebt 합계 태그는 연간만, 2026-10-25)
                  "0000029905": ["LongTermDebt"],   # DOV: LongTermDebt $3,264.6M(1년 안 $683.4M 포함) — ShortTermBorrowings가 같은 1년 안 금액이라 기본 합산이 두 번 셌다(Q3 2026 10-Q, 2026-10-25)
                  "0001781335": ["ShortTermBorrowings", "LongTermDebt"],   # OTIS: 단기 $210M + LongTermDebt(1년 안 포함) $8,226M = $8,436M(Q2 2026 10-Q, 2026-10-25)
                  "0000731802": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # ATO: 1년 안 $502.5M + 장기 $9,748.7M(Q3 FY26 10-Q, 2026-10-25)
                  "0001093557": ["ConvertibleNotesPayableCurrent", "ConvertibleLongTermNotesPayable"],   # DXCM: 전환사채 1년 안 + 장기(Q2 2026 장기 $1,242.8M — 기본 목록에 전환사채 태그가 없어 0이었다, 2026-10-25)
                  "0000029534": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # DG: 1년 안 $12.7M + 장기 $4,558.1M(Q2 FY26 10-Q, 2026-10-25)
                  "0001002910": ["ShortTermBorrowings", "LongTermDebtCurrent", "LongTermDebtNoncurrent"],   # AEE: 단기 $1,220M + 1년 안 $1,524M + 장기 $19,064M = $21,808M(Q2 2026 10-Q, 2026-10-25)
                  "0001037646": "DebtLongtermAndShorttermCombinedAmount",   # MTD: 1년 안 + 장기 합계 $2,112.0M(매 분기 있음 — DebtCurrent는 3월 분기에 없다, Fable r1 2026-10-25)
                  "0000100517": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],   # UAL: 1년 안 $1,848M + 장기 $24,550M(금융리스 포함) = $26,398M(Q3 2026 10-Q, 2026-10-25)
                  "0000723125": "DebtAndCapitalLeaseObligations",
                  # ED: 장기차입금을 분기에는 LongTermDebtFairValue(장부가와 같은 값 — 태그 오용)로, 연말에는 LongTermDebtNoncurrent로 낸다. 기본 선택은 CP $869M만 잡았다.
                  # CP + 은행 텀론(LoansPayableToBankCurrent — 2024~2025 $500~700M, Q1 2026 0) + 1년 안(날짜마다 앞 태그 우선) + 장기(날짜마다 앞 태그 우선). Q1 2026: 869 + 0 + 250 + 25,554 = 26,673(10-Q 대조, 2026-10-24)
                  "0001047862": ["NotesPayableCurrent", "LoansPayableToBankCurrent", ("OtherLongTermDebtCurrent", "LongTermDebtCurrent"), ("LongTermDebtNoncurrent", "LongTermDebtFairValue")],
                  # SO: 1년 안 만기 사채(LongTermDebtAndCapitalLeaseObligationsCurrent $5,701M)가 빠졌다 — 단기 차입 + 1년 안 + 장기(XEL과 같은 구성). Q1 2026: 1,673 + 5,701 + 67,148 = 74,522(10-Q 대조, 2026-10-24)
                  "0000092122": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # DHI: 재무상태표 차입금은 한 줄 "Notes payable"(NotesPayable, Q3 FY26 $7,112.6M — 주택 금융의 모기지 환매 약정 $1.8B 포함, 2026-10-24)
                  "0000882184": "NotesPayable",
                  # RMD: 기본 선택이 단기 차입($260M)만 잡았다 — 재무상태표 합계 DebtLongtermAndShorttermCombinedAmount(FY2026 말 260 + 399.4 = $659.4M)(2026-10-24)
                  "0000943819": "DebtLongtermAndShorttermCombinedAmount",
                  # IDXX: 기본 목록에 신용한도 차입(LinesOfCreditCurrent, 텀론 $250M 포함 — Q2 2026 $519M)이 빠졌다 — 신용한도 + 1년 안 사채 + 장기 사채. Q2 2026: 519 + 150 + 299.9 = 968.9(10-Q 대조, 2026-10-24)
                  "0000874716": ["LinesOfCreditCurrent", "LongTermDebtCurrent", "LongTermDebtNoncurrent"],
                  # RSG: 기본 장기 태그가 2018년에 멈추고 합계가 연말 값(2025-12)에 머물렀다 — 1년 안 + 장기(금융리스 포함). Q2 2026: 548 + 13,521 = 14,069(10-Q 대조, 2026-10-23)
                  "0001060391": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # A: 기본 합계가 대체값(debt_total_fallback)으로 잡혔다(값은 같다) — 단기 차입 + 장기. Q3 FY26: 304 + 3,645 = 3,949(10-Q 대조, 2026-10-23)
                  "0001090872": ["ShortTermBorrowings", "LongTermDebt"],
                  # XEL: 기본 합계가 1년 안 장기부채(LongTermDebtAndCapitalLeaseObligationsCurrent $999M)를 빠뜨렸다 — 단기 + 1년 안 장기 + 장기.
                  # Q2 2026: 2,510 + 999 + 35,948 = 39,457(10-Q 대조, Codex·Fable r1, 2026-10-23)
                  "0000072903": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # ADSK: 기본 합계가 대체값으로 떨어졌다($3,494M) — 단기 차입(CP) + 1년 안 사채 + 장기 사채. Q2 FY27: 994 + 499 + 1,985 = 3,478(10-Q 대조, 2026-10-23)
                  "0000769397": ["ShortTermBorrowings", "NotesPayableCurrent", "LongTermNotesPayable"],
                  # AME: 기본 합계가 장기만 잡았다($1,056M) — 1년 안 차입(CP 포함) + 장기. Q2 2026: 980.6 + 1,055.5 = 2,036.2(10-Q 대조, 2026-10-23)
                  "0001037868": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # NUE: 장기 비유동 태그(LongTermDebtNoncurrent)가 2019년에 멈춤 — 재무상태표 단기 차입 + 1년 안 장기·금융리스 + 1년 뒤 장기·금융리스.
                  # Q2 2026: 129 + 581 + 6,389 = 7,099(10-Q 대조, 2026-10-23)
                  "0000073309": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # LITE: 같은 1년 안 만기 전환사채($1,596.9M, 2026-06)를 ShortTermBorrowings와 LongTermDebtCurrent 두 태그로 실어 기본 합이 두 번 더했다($3,234M) —
                  # 단기 + 장기 비유동 = 10-K 재무상태표 1,596.9 + 40.5 = 1,637.4(DebtLongtermAndShorttermCombinedAmount와 같음, 그 태그는 2024-06부터만)(2026-10-22).
                  "0001633978": ["ShortTermBorrowings", "LongTermDebtNoncurrent"],
                  # CMI: 단기 은행 차입 "Loans payable" $459M(ShortTermBankLoansAndNotesPayable)이 기본 목록에 없어 빠졌다 — 459 + CP 348 + 1년 안 151 + 장기 6,737
                  # = 10-Q $7,695M(DebtInstrumentCarryingAmount와 같음). 장기 태그 이름에 CapitalLease가 있어 금융리스를 리스로 또 더하지 않는다(2026-10-22).
                  "0000026172": ["ShortTermBankLoansAndNotesPayable", "CommercialPaper", "LongTermDebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # UPS: 1년 안 만기 $634M(DebtCurrent)이 빠지고 장기만 남았다 — 634 + 장기·금융리스 23,850 = 10-Q $24,484M(DebtAndCapitalLeaseObligations와 같음, 그 태그는 2022-12부터).
                  # 두 태그 모두 금융리스 포함이라 리스에서 금융리스를 또 더하지 않는다(2026-10-22).
                  "0001090727": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # CL: 재무상태표 "Debt payable within one-year"(2025-12 $1,117M, 2026-06 $34M)는 ShortTermBankLoansAndNotesPayable — 기본 목록은
                  # 그 일부인 LongTermDebtCurrent(2025-03 뒤 끊김)만 봐 2026-06 차입금이 장기 $7,823M뿐이었다. 34 + 7,823 = $7,857M(2026-10-22).
                  "0000021665": ["ShortTermBankLoansAndNotesPayable", "LongTermDebtNoncurrent"],
                  # ECL: 재무상태표 "Short-term debt" $1,271.1M(DebtCurrent — 1년 안 만기 1,265.7 + 단기 차입 5.4) + 장기 11,905.1(LongTermDebtAndCapitalLeaseObligations) = $13,176.2M(2026-10-22).
                  "0000031462": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # ITW: 재무상태표 "Short-term debt" $3,145M(DebtCurrent — CP 2,100 + 1년 안 만기) + 장기 6,549 = $9,694M — 기본은 CP와 장기만 잡아 $8,649M였다(Codex 2026-10-22).
                  "0000049826": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # RCL: 1년 안 만기 $1,573M이 빠지고 장기만 남았다 — 1,573 + 21,263 = $22,836M(두 태그 모두 금융리스 포함이라 리스에서 또 더하지 않음, 2026-10-22).
                  "0000884887": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # DASH: 차입금은 2025년 Deliveroo 인수 자금 전환사채뿐(ConvertibleLongTermNotesPayable, 2026-06 $2,727M) — 기본 태그는 2021년에 멈춰 0이었다(2026-10-22).
                  "0001792789": ["ConvertibleLongTermNotesPayable"],
                  # TGT: 1년 안 $1,136M + 장기 $14,221M(둘 다 금융리스 포함 태그) = $15,357M — 기본은 장기만 잡고 금융리스 $2,113M을 리스로 따로 더했다(2026-10-22).
                  "0000027419": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # APD: 2023년부터 장기 차입금을 특수관계자 축(비특수 $16,585.1M + 특수 $186.2M, 2026-06)으로만 실어 요약 자료에 차원 없는 값이 없다 —
                  # BUILD dim_facts가 overlay에 LongTermDebtNonrelatedApd·LongTermDebtRelatedApd로 싣고, 그 전 날짜는 차원 없는 태그(튜플 앞 우선). 기본은 단기 $126.7M뿐이었다(2026-10-22).
                  # 날짜마다 표준 태그 먼저(원래 공시일) — 2023-03까지는 차원 없는 장기 + NotesPayableRelatedPartiesNoncurrent(2022-12 $658.4M), 그 뒤는 overlay(Codex r1: overlay를 앞에 두면 2022-09가 2023-08 공시일로 밀렸다).
                  "0000002969": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent",
                                 ("LongTermDebtAndCapitalLeaseObligations", "LongTermDebtNonrelatedApd"), ("NotesPayableRelatedPartiesNoncurrent", "LongTermDebtRelatedApd")],
                  # MMM: 단기 차입·1년 안 만기 DebtCurrent $2,439M + 장기 LongTermDebtNoncurrent $12,558M = 10-Q $14,997M(기본은 장기만, 2026-10-21).
                  "0000066740": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # TRV: 재무상태표 "Debt" $9,813M(사채 + CP $100M)은 DebtLongtermAndShorttermCombinedAmount — 기본 선택은 2025-12에 멈춘 태그였다(2026-10-21).
                  "0000086312": "DebtLongtermAndShorttermCombinedAmount",
                  # HLT: 1년 안 만기 $624M + 장기 $12,719M(둘 다 금융리스 포함 태그) = 10-Q $13,343M — 기본은 장기만이고 금융리스를 리스로 또 더했다(2026-10-21).
                  "0001585689": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # HOOD: 차입금은 2026년 발행 전환사채 $2,170M(ConvertibleDebtNoncurrent)뿐 — 기본 목록에 없어 0이었다(2026-10-21).
                  "0001783879": "ConvertibleDebtNoncurrent",
                  # HPE: "Notes payable and short-term borrowings" $2,901M(DebtCurrent) + 장기 $17,343M = $20,244M — 기본은 LongTermDebtCurrent $2,137M만 잡아 $764M이 빠졌다(2026-10-21).
                  "0001645590": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # MAR: "Current portion of long-term debt" + "Long-term debt"(…AndCapitalLeaseObligations 두 태그 — 금융리스 포함). 기본 선택은 LongTermDebt($23M, 다른 항목)를
                  # 잡아 차입금이 $0.02B였다(2026-06-30 $460M + $16,455M = $16,915M, 2026-10-21).
                  "0001048286": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # DDOG: 전환사채만 — 장기분 ConvertibleLongTermNotesPayable(2026-06-30 $985.5M, 2029년 만기) + 1년 안 ConvertibleNotesPayableCurrent(2024-06~2025-03의
                  # 2025년 만기분). 기본 목록에 장기 태그가 없어 차입금 0이었다(두 태그는 같은 날 겹치지 않음, 2026-10-21).
                  "0001561550": ["ConvertibleNotesPayableCurrent", "ConvertibleLongTermNotesPayable"],
                  # AKAM: 차입금이 전환사채뿐 — 1년 안(ConvertibleNotesPayableCurrent) + 장기(ConvertibleLongTermNotesPayable, 2026-06-30 $5,857M).
                  # 기본 목록에 장기 태그가 없어 2019년부터 장기분이 통째로 빠졌다(재봉인 dr r1 2026-10-27 전환사채 전수 점검).
                  "0001086222": ["ConvertibleNotesPayableCurrent", "ConvertibleLongTermNotesPayable"],
                  # SMCI: 신용한도·기한부 대출(DebtLongtermAndShorttermCombinedAmount — 10-Q "Lines of credit and term loans" 유동 + 비유동,
                  # 2026-03-31 $2,095M + $2,019M = $4,114M) + 전환사채(ConvertibleLongTermNotesPayable $4,659M, 재무상태표 "Convertible notes" 한 줄 — 합계 태그와
                  # 겹치지 않음, 10-Q 2026-03-31·2025-12-31 원문). 기본 목록은 전환사채가 빠졌다(2024-06~, 재봉인 dr r1 2026-10-27).
                  "0001375365": ["DebtLongtermAndShorttermCombinedAmount", "ConvertibleLongTermNotesPayable"],
                  # CIEN·AXON: 같은 사채를 분기에 따라 일반 태그(LongTermDebt…)나 전환사채 태그로 낸다 — 날짜마다 앞 태그 우선(튜플).
                  # CIEN 2019-07~2022-07, AXON 2022-12~2024-06 분기가 전환사채 장기 태그뿐이라 차입금이 0~7이었다(재봉인 dr r1 2026-10-27).
                  "0000936395": [("LongTermDebtNoncurrent", "ConvertibleLongTermNotesPayable"), ("LongTermDebtCurrent", "ConvertibleNotesPayableCurrent")],
                  "0001069183": [("LongTermDebtNoncurrent", "ConvertibleLongTermNotesPayable"), ("LongTermDebtCurrent", "ConvertibleNotesPayableCurrent")],
                  # WM: "Current portion of long-term debt"(DebtCurrent) + "Long-term debt, less current portion"(LongTermDebtAndCapitalLeaseObligations — 금융리스 포함).
                  # 기본 선택은 1년 안 만기분이 빠졌다(2026-06-30 $1,075M + $22,281M = $23,356M = DebtAndCapitalLeaseObligations, 2026-10-21).
                  "0000823768": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # WMB: 기업어음 + "Long-term debt due within one year" + "Long-term debt"(…AndCapitalLeaseObligations 두 태그). 기본 선택은 1년 안 만기분이 빠졌다
                  # (2026-06-30 $475M + $2,197M + $28,121M = $30,793M — 엔진 $28,596M, 2026-10-19).
                  "0000107263": ["CommercialPaper", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # EQIX: 기본 선택은 세부 태그가 끊긴 뒤 LongTermDebt만 잡아 금융리스 $2,280M이 빠졌다 — 선순위채·대출 원금(LongTermDebt $19,873M, 장부가 $19,709M)
                  # + 금융리스(유동 176 + 비유동 2,104). 2026-06-30 합계 $22,153M(2026-10-17).
                  "0001101239": ["LongTermDebt", "FinanceLeaseLiability"],
                  # ADBE: LongTermDebt는 비유동분만 — 1년 안 만기분은 DebtCurrent($1,597M, 2026-08-28)라 기본 선택에서 빠졌다(엔진 $4,766M 대 재무상태표 $6,363M, 2026-10-17).
                  "0000796343": ["DebtCurrent", "LongTermDebt"],
                  # EMR: 재무상태표 "Short-term borrowings and current maturities of long-term debt"(DebtCurrent) + "Long-term debt"(LongTermDebtNoncurrent).
                  # 2026-06-30 $5,587M + $7,526M = $13,113M(2026-10-18).
                  "0000032604": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # CSX: "Current Maturities of Long-term Debt" + "Long-term Debt"를 …AndCapitalLeaseObligations(Current) 두 태그로만 낸다 —
                  # 기본 선택이 2012년에 멈춘 LongTermDebt($9,832M)를 잡았다(2026-06-30 원문 $1,702M + $17,162M = $18,864M, 2026-10-18).
                  "0000277948": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # MRSH: 재무상태표 "Short-term debt"(DebtCurrent — 기업어음 + 1년 안 만기) + "Long-term debt"(LongTermDebtNoncurrent).
                  # 기본 합이 $22,133M(1년 안 만기·기업어음 겹침)으로 원문 $1,644M + $18,889M = $20,533M보다 컸다(2026-10-18).
                  "0000062709": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # ICE: 재무상태표 "Short-term debt" 한 줄을 ShortTermBorrowings·LongTermDebtCurrent·CommercialPaper(그 일부) 세 태그로 내
                  # 기본 합이 같은 $1,218M을 세 번 더했다($22,282M 대 원문 $19,846M, 2026-10-18). 2020~2026 내내 앞 둘은 같은 값.
                  "0001571949": ["ShortTermBorrowings", "LongTermDebtNoncurrent"],
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
                  # VLO: 기본 목록 태그가 없어 공정가치 주석의 금융리스 뺀 차입금(DebtLongtermAndShorttermCombinedAmount $9,101M)으로 대체됐다.
                  # 재무상태표 "debt and finance lease obligations" 유동 $927M + 장기 $10,422M = $11,349M(2026-06-30, COP와 같은 조합, 2026-10-13).
                  "0001035002": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # PSX: 1년 안 만기 차입금(DebtCurrent "Short-term debt" $1,797M, 2026-06-30)이 기본 목록에서 빠져 장기분 $18,768M만 잡혔다(MPC·VLO와 같은 조합, 2026-10-13).
                  "0001534701": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # CVS: 1년 안 만기 차입금(LongTermDebtAndCapitalLeaseObligationsCurrent $1,958M, 2026-06-30)이 빠져 장기분 $59,452M만 잡혔다.
                  # 금융리스($1,326M, 10-K 리스 주석)는 재무상태표 장기차입금 두 줄 안이다. 기업어음은 ShortTermBorrowings(2025-09-30 $1,247M, ETN과 같은 조합, 2026-10-15).
                  "0000064803": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # ADP: 기본 목록(전환사채 태그 두 개는 ADP 자료 0건이라 뺌) + 환매조건부 차입("Obligations under reverse repurchase agreements" $139.3M, 2026-06-30 — 회사 고유 태그라 cfg_adp company_tags가
                  # SecuritiesSoldUnderAgreementsToRepurchase 이름으로 싣는다). 담보인 장기 채권 $138.6M은 비영업 자산에 들어가므로 짝을 맞춘다(Codex 2026-10-16).
                  # SYK: 1년 안 만기 차입금(DebtCurrent $750M — 기업어음 $250M 포함, 2026-06-30)이 빠지고 CommercialPaper만 더해져 $500M이 모자랐다
                  # (10-Q 차입금 표 합계 $14,942M = 유동 750 + 비유동 14,192, DHR과 같은 조합, Codex 2026-10-16).
                  "0000310764": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # LOW: 1년 안 만기($2,352M, 2026-07-31)가 빠져 장기분 $35,204M만 잡혔다 — 리스 포함 태그 두 줄 + 단기차입(2026-05-01 기업어음 $380M)(ETN 조합, 2026-10-16).
                  # CME: 차입금을 UnsecuredLongTermDebt($3,424.2M, 2026-06-30)로만 내 기본 목록이 단기차입 0만 잡아 차입금이 0이었다(2026-10-16).
                  # TT: 1년 안 만기·단기차입(DebtCurrent $693.1M, 2026-06-30)이 빠져 장기분 $3,923.7M만 잡혔다(DHR 조합, 2026-10-16).
                  "0001466258": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  "0001156375": ["UnsecuredLongTermDebt", "UnsecuredDebtCurrent", "ShortTermBorrowings"],
                  "0000060667": ["ShortTermBorrowings", "LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  "0000008670": ["LongTermDebtCurrent", "LongTermDebtNoncurrent", "ShortTermBorrowings", "CommercialPaper", "OtherShortTermBorrowings",
                                 "SecuritiesSoldUnderAgreementsToRepurchase"],
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
                  # 2022~2025-09 사채($1.48~1.49B)는 ConvertibleLongTermNotesPayable로만 냈다 — 날짜마다 LongTermDebt 우선, 없으면 그 태그(튜플).
                  # 기본 경로는 LongTermDebtNoncurrent가 2021-09에 멈추고 1년 안 0만 이어져 차입금 0이었다(재봉인 dr r1 2026-10-27).
                  # 2021 분기 사채는 LongTermDebtNoncurrent로만, 1년 안 만기분(2022 전환사채)은 LongTermDebtCurrent(2022-12까지)로 냈다 — 튜플 끝과 더하는 항목.
                  # 빼면 지정 총계가 2020-06에 시작해 2021 분기가 기본 경로에서 잘리고 2021-10~2022-01이 낡은 값 보류가 됐다(재봉인 r8 점검).
                  "0001373715": ["ShortTermBorrowings", ("LongTermDebt", "ConvertibleLongTermNotesPayable", "LongTermDebtNoncurrent"), "LongTermDebtCurrent"],
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
                  # GM: 자동차 부문 빚만(CAT·DE와 같은 규칙, 2026-09-30 사용자 결정) — 재무상태표가 차입금을 gm:BusinessGroupAxis(Automotive/GM Financial)로만 싣는다.
                  # BUILD dim_facts가 overlay에 싣는다. Q3 2026: 1년 안 529 + 장기 15,270 = $15,799M(GM Financial $112,944M 제외, 2026-10-22).
                  "0001467858": ["DebtCurrentAutoGm", "LongTermDebtAutoGm"],
                  # COR: 내재가치 입력이 장기 $11,444M만 잡았다 — 단기 차입금(DebtCurrent $279M)을 더한다(배수 쪽은 LongTermDebt $11,723M로 이미 같은 값, 2026-10-22).
                  "0001140859": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # AON: 1년 안 차입금(DebtCurrent $2,020M — 기업어음·1년 안 만기)이 기본 합에서 빠져 장기 $12,947M뿐이었다(2026-10-22).
                  "0000315293": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # TDG: 매출채권 유동화 차입(ShortTermBankLoansAndNotesPayable $725M)이 빠져 1년 안 139 + 장기 32,621뿐이었다 — 합 $33,485M(2026-06, 10-Q 재무상태표).
                  # 장기 태그는 2020-09부터 LongTermDebtAndCapitalLeaseObligations(금융리스 포함), 그 전 날짜는 LongTermDebtNoncurrent(튜플 앞 우선, 2026-10-22).
                  "0001260221": ["LongTermDebtCurrent", "ShortTermBankLoansAndNotesPayable", ("LongTermDebtAndCapitalLeaseObligations", "LongTermDebtNoncurrent")],
                  # TEL: 단기 차입금(DebtCurrent $102M)이 기본 합에서 빠져 장기 $5,530M뿐이었다(2026-10-23).
                  "0001385157": ["DebtCurrent", "LongTermDebtNoncurrent"],
                  # BSX: 1년 안 차입금(DebtCurrent, 2026-06 $1,709M — 기업어음 포함)이 기본 합에서 빠져 장기 $10,915M뿐이었다(2026-10-22).
                  "0000885725": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
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
                  # FISV: "Short-term and current maturities of long-term debt"(DebtCurrent $1,254M) + "Long-term debt"(LongTermDebtAndCapitalLeaseObligations $25,809M) = $27,063M(Q3 2026 10-Q,
                  # 기업어음 $1,610M·금융리스 $2,421M 포함). 기본 경로는 유동분을 빠뜨렸다(Codex 2026-11-05).
                  "0000798354": ["DebtCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # EG: 선순위채 $2,353M + 후순위채 $218M + FHLB 차입 $1,019M = $3,590M(Q3 2026 10-Q). 기본 경로는 2011년 단기차입 $40M만 잡았다(2026-11-05)
                  "0001095073": ["SeniorNotes", "SubordinatedDebt", "AdvancesFromFederalHomeLoanBanks"],
                  # WRB: 선순위채는 회사 고유 태그(wrb:SeniorNotesAndOtherDebt $1,827.9M, cfg company_tags가 빌린 이름으로 싣는다). 후순위채 $1,011.1M은 2025-03부터 OtherLiabilities로
                  # 잘못 붙어(기타부채와 태그가 뒤바뀜) 아래 튜플로 날짜를 가른다
                  "0000011544": ["SeniorNotesWrb", ("SubDebtWrb", "JuniorSubordinatedNotes")],   # 후순위채: 2025-03 공시부터 OtherLiabilities로 붙어 cfg company_tags(시작일 2025-04-01)가 SubDebtWrb로 싣고, 그 전 날짜는 JuniorSubordinatedNotes(날짜마다 앞 태그 우선, Codex r1 2026-11-05)
                  # L: 장기 $8,417M + 유동 $521M = $8,938M(Q3 2026, CNA·Boardwalk·호텔 포함 연결). 기본 경로는 유동분을 빠뜨렸다(2026-11-05)
                  "0000060086": ["LongTermDebtAndCapitalLeaseObligationsCurrent", "LongTermDebtAndCapitalLeaseObligations"],
                  # CINF: 어음 $17M + 장기 $791M(2028·2034 만기) = $808M(2026-11-05)
                  "0000020286": ["NotesPayable", "LongTermDebt"],
                  # ACGL: 선순위채 SeniorLongTermNotes $4,286M(Q3 2026, 6월 $2,000M 발행) — 기본 차입 태그가 하나도 없다(2026-11-05)
                  "0000947484": ["SeniorLongTermNotes"],
                  # CPAY: LongTermDebt $10,623.5M = 유동 포함 총계(매출채권 유동화 $2,300M 포함). 기본 경로는 유동분 $4,525M만 잡았다(Codex r1 2026-11-05)
                  "0001175454": ["LongTermDebt"],
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
EV_TAGS_BY_CIK = {"0000010456": {"sti": []},   # BAX: 단기투자는 2016-03의 낡은 값(2026-11-07)
                  "0000879169": {"sti": ("DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent", "AvailableForSaleSecuritiesDebtSecuritiesCurrent")},   # INCY: 시장성 증권(유동, Q3 2026 $578.7M)은 2023-12부터 새 태그 — 옛 태그는 2024-09에 멈춤, 날짜마다 앞 태그 우선(2026-11-07)
                  "0000827052": {"nci": ["MinorityInterestAmountRepresentedByPreferredStock"], "sti": [], "preferred": ["PreferredStockValueOutstanding"]},   # EIX: 비지배지분 = SCE 우선주 $1,564M(이 태그뿐 — 없으면 0), EIX 우선주 Series B $83M, 단기투자는 2010년 낡은 값(사전 조사 2026-10-29, 2026-11-07)
                  "0000842023": {"sti": [], "nci": []},   # TECH: 단기투자(2025-03)·비지배지분(2022-06)은 지금 재무상태표에 없는 낡은 값(Q1 FY27 10-Q, 2026-11-07)
                  "0001097149": {"sti": []},   # ALGN: 단기투자 태그가 2024-12에 멈춤 — 2026-09 재무상태표에 단기 시장성 증권 없음(현금 $1,145M뿐, 2026-11-08)
                  "0001000228": {"nci": ["MinorityInterest", "TemporaryEquityCarryingAmountIncludingPortionAttributableToNoncontrollingInterests"], "sti": []},   # HSIC: 비지배지분 $658M + 상환 가능 $914M(임시자본, UHS·DVA와 같은 처리), 단기투자는 2010년 낡은 값(2026-11-07)
                  "0000352915": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},   # UHS: 비지배지분 $71.0M + 상환 가능 $74.2M(임시자본, DVA와 같은 처리 — Codex r1, 2026-11-07)
                  "0001032208": {"nci": ["OtherMinorityInterests", "MinorityInterestAmountRepresentedByPreferredStock", "TemporaryEquityCarryingAmountIncludingPortionAttributableToNoncontrollingInterests"],
                                 "preferred": []},   # SRE: 기타 비지배 $7,457M + 자회사 우선주($0, 2025-12 $20M) + 상환가능 비지배 $3,392M. 보통주 앞 우선주는 Q3 2026 재무상태표 "—" — 기본 태그는 2018-06에 멈춰 계산 보류로 걸렸다(Q3 2026 10-Q, 2026-11-07)
                  "0000874761": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},   # AES: 비지배 $5,071M + 상환가능 자회사 주식 $3,100M(Q3 2026 10-Q, CPAY와 같은 처리, 2026-11-07)
                  "0001174922": {"sti": ["Investments", "ShortTermInvestments"]},   # WYNN: 유동자산 "Investments"(정기예금 등) $150.2M(Q3 2026 10-Q, 2022-12~ 이 태그) — 기본 단기투자 태그는 2018 멈춤(2026-11-06)
                  "0001175454": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},   # CPAY: 비지배 $46M + 상환가능 $314M(Mastercard, 2026-11-05 Codex r1)
                  "0000779152": {"cash": ("CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents")},   # JKHY: 10-K(6월 말)는 현금을 제한 현금 포함 합계 태그로만 낸다(제한 현금 0 — 같은 값). 날짜마다 앞 태그 우선(2026-11-05)
                  "0001267238": {"sti": []},   # AIZ: 단기투자 OtherShortTermInvestments $300.8M은 보험 운용자산이고 기본 태그는 2019 멈춤(DCF 입력 보류로 순현금 칸이 비었다) — ACGL과 같게 뺀다(2026-11-06)
                  "0000947484": {"sti": []},   # ACGL: 단기투자 $3,253M은 보험 운용자산(축 값, OtherShortTermInvestments는 2021 멈춤) — 현금은 CashAndCashEquivalentsAtCarryingValue $1,152M(2026-11-05)
                  "0000060086": {"sti": []},   # L: 단기투자 $5,715M은 CNA 보험 운용자산(TRV·ALL 선례) — 현금은 Cash $505M(2026-11-05)
                  "0000020286": {"sti": []},   # CINF: 단기투자 $141M은 보험 운용자산(같은 원칙, 2026-11-05)
                  "0001095073": {"cash": ["Cash"], "sti": []},   # EG: 현금 태그가 2018에 멈춤 — Cash $987M(Q3 2026), 단기투자 $3,055M은 보험 운용자산(TRV·ALL·PGR 선례, 2026-11-05)
                  "0000079282": {"sti": []},   # BRO: ShortTermInvestments는 2024-12 $10M이 마지막 — 2025부터 기타 유동자산에 합쳤다(재표시). 수탁 현금 $2,442M은 엔진 현금 밖(2026-11-05)
                  "0000798354": {"lease": ["OperatingLeaseLiability"]},   # FISV: 금융리스($2,421M)는 차입금 두 줄 안에 있어 리스에는 운용리스만 — 10-Q에 유동분만 있어 총액은 FY2025 10-K $763M(2026-11-05, Codex r1)
                  "0000720005": {"debt": ["SeniorNotes", "OtherBorrowings"], "lease": ["OperatingLeaseLiability"]},   # RJF: 차입 = 선순위채 $3,522M + 기타 차입 $950M(FHLB·신용한도) — 기본 태그는 2022-12에 멈춤. 예금 $63B는 차입 아님. 운용리스 $568M(Q3 FY26 10-Q, 2026-11-04)
                  "0001521332": {"sti": []},   # APTV: 단기투자 태그는 2024-09($0.79B)에 멈춤 — 지금 재무상태표에 단기투자 줄 없음(Q3 2026 10-Q 현금 $670M, Codex r1 2026-11-04)
                  "0000914208": {"sti": [], "lease": ["OperatingLeaseLiability"], "nci": ["MinorityInterest", "TemporaryEquityCarryingAmountIncludingPortionAttributableToNoncontrollingInterests"]},   # IVZ: 단기투자 태그는 2018-09에 멈춤(지금 재무상태표에 없는 줄), 운용리스는 10-K 총액만(2025-12 $406.7M), 비지배 = 비상환 $701.6M + 상환가능 $297.0M(모두 CIP 몫, BEN과 같이 둘 다 — Fable r1). 차입 $1,281.3M = 회사 차입(CIP 차입 $7,919.6M은 차원 값), 현금 $965.5M = 회사 몫(Q3 2026 10-Q, 2026-11-04)
                  "0000038777": {"cash": ("CashCompanyBen", "CashAndCashEquivalentsAtCarryingValue"), "sti": [], "lease": ["OperatingLeaseLiability"],
                                 "nci": ["MinorityInterest", "TemporaryEquityMinorityInterestsBen"]},   # BEN: 현금은 회사 몫 $2,670.3M(dei:LegalEntityAxis 차원, BUILD dim_facts — 축 없는 태그는 2021-12 멈춤, 합계 태그 $3,760.9M에는 CIP 현금 $1,090.6M), 비지배 = 비상환 $1,181.7M(CIP 몫 $757.4M 포함 — 빼는 장치가 없어 TROW처럼 둔다, 주당 약 $1.49 보수적) + 상환가능 자회사 몫 $1,137.3M(차원), 운용리스 $974.6M(Q3 FY26 10-Q, 2026-11-04)
                  "0001324424": {"nci": ["NonredeemableNoncontrollingInterest", "MinorityInterest"]},   # EXPE: 비지배지분 $1,262M(trivago 소수지분)은 NonredeemableNoncontrollingInterest 태그(Q2 2026 10-Q, 2026-11-03)
                  "0000783325": {"nci": ["OtherMinorityInterests"]},   # WEC: 비지배지분 $404.3M은 OtherMinorityInterests 태그(MinorityInterest 아님, Q3 2026 10-Q, 2026-11-03)
                  "0001967680": {"lease": ["OperatingLeaseLiability"]},   # VLTO: 최신 운용리스 합계 $196M(Q3 2026) — 유동·비유동 태그는 연간(2025-12 $206M)뿐(Codex r1, 2026-10-30)
                  "0001513761": {"sti": [], "nci": []},   # NCLH: 단기투자(2022)·비지배지분(2014)은 사라진 항목(2026-11-04)
                  "0001286681": {"preferred": []},   # DPZ: 우선주 태그 2025-12 멈춤(발행 없음, 2026-11-03)
                  "0000910521": {"sti": [], "nci": []},   # DECK: 단기투자(2009)·비지배지분(2012)은 사라진 항목, 차입금 0(2026-11-03)
                  "0001397187": {"nci": []},   # LULU: 비지배지분 $0.01B(2012-07)은 사라진 항목(2026-11-03)
                  "0000046080": {"sti": ["DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent"], "lease": ["OperatingLeaseLiability"]},   # HAS: 단기 국채 $576.2M(채권 상환 적립, Q3 2026 10-Q) — 기본 목록에 없는 태그(2026-11-03)
                  "0000040987": {"lease": ["OperatingLeaseLiability"]},   # GPC: 10-Q는 비유동 운용리스($1,714M)만 태그 — 유동분 포함 총액은 10-K OperatingLeaseLiability($2,134M, 2025-12, Codex r1)
                  "0000916365": {"preferred": []},   # TSCO: 우선주 태그가 2024-09에 멈춤(발행 없음, 2026-11-03)
                  "0000764478": {"sti": [], "nci": []},   # BBY: 단기투자 $0.06B(2021-05)·비지배지분(2016-01)은 지금 재무상태표에 없는 낡은 값(2026-11-03)
                  "0000822416": {"lease": ["OperatingLeaseLiability"], "preferred": []},   # PHM: 운용리스는 합계 태그 하나($123.2M), 우선주 $0(2024-12에 멈춘 태그) — 2026-11-03
                  "0001116132": {"sti": ["ShortTermInvestments"]},   # TPR: 단기투자 $177.3M = 매도가능 채권 $149.4M + 기타 $27.9M(FY26 10-K) — 기본 목록이 합계와 구성을 함께 더해 $326.7M(2026-11-03)
                  "0000922224": {"sti": [], "preferred": [], "nci": []},   # PPL: 단기투자(2015)·우선주(2010)·비지배지분(2023)은 지금 재무상태표에 없는 낡은 값(2026-10-30)
                  "0000352541": {"sti": [], "preferred": [], "nci": []},   # LNT: 단기투자 $250M은 2025-09 한 번뿐, 우선주 $200M(2014)·비지배지분 $29M(2022)은 사라진 항목 — 낡은 값이 EV에 더해졌다(Codex r1, 2026-10-30)
                  "0001065088": {"sti": ["AvailableForSaleSecuritiesDebtMaturitiesWithinOneYearFairValue"]},   # EBAY: 단기투자 $809M(재무상태표 "Short-term investments"는 회사 고유 태그, 같은 금액이 매도가능 채권 만기 1년 안 태그에 있다) — 기본은 2025-06에 멈춘 ShortTermInvestments $26M(Fable r1, 2026-10-30)
                  "0000927066": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},   # DVA: 상환 가능 비지배지분 $1,484M(임시자본, 투석 합작 파트너 풋) + 자본 내 $233M(Q3 2026 10-Q, 2026-10-30)
                  "0001014473": {"nci": []},   # VRSN: 비지배지분 없음 — MinorityInterest 마지막 값이 2010-06($0.05B)이라 낡은 값으로 DCF가 보류됐다(Q3 2026 10-Q, 2026-10-29)
                  "0001664703": {"debt": ["LongTermDebtCurrent", "LongTermDebtNoncurrent"]},   # BE: ShortTermBorrowings를 1년 안 장기차입금과 같은 금액으로 함께 태깅 — 기본 목록이면 두 번 더해진다(2024-09 $114M, Fable 2026-10-29). LongTermDebt 총계 = 유동 + 비유동 확인
                  # VMC: CommercialPaper 태그는 잔액이 아니라 프로그램 한도 $1,600.0M("Our $1,600.0 million commercial paper program",
                  # 10-Q 2022-09-30·2025-03-31). 실제 기업어음 잔액은 차입금 표의 장기차입(2022-09 $550M → LongTermDebtNoncurrent) 또는
                  # 단기차입(2024-06 $95M·2025-06 $550M → ShortTermBorrowings)에 들어 있다 — 기본 목록이면 한도가 더해져 2025-03-31 차입금이
                  # $6,508M(실제 $4,908.4M, +33%)이 됐다. 2015~2026-09 캐시 CommercialPaper 17행 모두 한도, 장기 유동+비유동 = LongTermDebt 47분기 확인
                  # (안건 E64, Fable·Codex 2026-10-29~30)
                  "0001396009": {"debt": ["LongTermDebtCurrent", "LongTermDebtNoncurrent", "ShortTermBorrowings", "OtherShortTermBorrowings",
                                          "ConvertibleNotesPayableCurrent", "ConvertibleNotesPayableNoncurrent"]},
                  "0001130310": {"sti": []},   # CNP: 단기투자 $425M은 ZENS(교환사채) 기초 주식 — 짝인 ZENS 지수부채 파생 $468M이 차입금에 없어 한쪽만 더하면 지분가치가 부푼다, 현금성에서 뺀다(Codex·Fable r1, 2026-10-29)
                  # GEHC: 비지배지분 = 자본 안 $17M + 상환가능(메자닌) $234M(Q3 2026 10-Q, 2026-10-28)
                  "0001932393": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},
                  # DGX: 비지배지분 = 자본 안 $318M(2026 Corewell 합작으로 $36M에서 증가) + 상환가능(메자닌) $81M(Q3 2026 10-Q, 2026-10-27)
                  "0001022079": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},
                  # OTIS: 비지배지분 $188M + 상환가능 비지배지분 $106M(2026-10-25)
                  "0001781335": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},
# DXCM: 단기투자 = 유동 매도가능 채무증권(2025-06까지 AvailableForSale…Current, 그 뒤 DebtSecuritiesAvailableForSale…Current — Q2 2026 $704.8M, 2026-10-25)
                  "0001093557": {"sti": ["DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent", "AvailableForSaleSecuritiesDebtSecuritiesCurrent"]},
# XYL: 상환가능 비지배지분 $242M(메자닌) + 비지배지분 $3M(Q2 2026 10-Q, 2026-10-25)
                  "0001524472": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},
# EFX: 상환가능 비지배지분 $120.8M + 비지배지분 $20.5M(Q3 2026 10-Q, 2026-10-25)
                  "0000033185": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},
# CRH: 상환가능 비지배지분(자본 밖, Q2 2026 $435M) + 자본 안 비지배지분 $1,065M(ICE 방식, 2026-10-24)
                  "0000849395": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},
# MCHP: 7.5% 의무전환 우선주 청산가치 $1,485M(PreferredStockLiquidationPreferenceValue) — 장부 우선주 값은 0(추가납입자본 안, 2026-10-24)
                  "0000827054": {"preferred": ["PreferredStockLiquidationPreferenceValue"]},
# P(옛 PSTG): 단기투자 = 유동 매도가능 채무증권(DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent, Q2 FY27 $622.2M) — 기본 태그는 2021-05에 멈췄다(2026-10-24)
                  "0001474432": {"sti": ["DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent"]},
# ALLE: 현금 = CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents($388.1M — 2025-03부터 재무상태표 줄, 기본 현금 태그는 10-K만, 2026-10-25) [엔진수정대기]
                  "0001579241": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]},
# CF: 현금 = CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents($2,480M = 재무상태표 "Cash and cash equivalents") — 기본 현금 태그는 2019년에 멈췄다(2026-10-25)
                  "0001324404": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]},
# HII: 현금 = CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents($12M — 기본 현금 태그는 2024-03에 멈췄다, 2026-10-25)
                  "0001501585": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]},
# PODD: 현금 = CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents($534.9M — 기본 현금 태그는 2021-09에 멈췄다, 2026-10-25)
                  "0001145197": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]},
# MDLZ: 현금 = CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents($1,759M — 기본 현금 태그를 쓰지 않는다, 2026-10-25)
                  "0001103982": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]},
# DOV: 현금 = CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents($1,693.2M = 재무상태표 줄) — 기본 현금 태그를 쓰지 않는다(2026-10-25)
                  "0000029905": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]},
# BIIB: 현금 = CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents($3,382.7M = 재무상태표 "Cash and cash equivalents") — 기본 현금 태그는 2019-12에 멈췄다(2026-10-24)
                  "0000875045": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]},
# WAB: 현금 = CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents($489M, 제한 현금 포함 — 재무상태표 줄) — 기본 현금 태그는 2022-09에 멈췄다(2026-10-23)
                  "0000943452": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]},
# TER: 단기투자 = 매도가능 채무증권(AvailableForSaleSecuritiesDebtSecurities, 6월 말 $100.7M) — 기본 MarketableSecuritiesCurrent는 2014년에 멈춤. 이연보상용 뮤추얼펀드는 뺀다(Fable r1, 2026-10-23)
                  "0000097210": {"sti": ["AvailableForSaleSecuritiesDebtSecurities"]},
                  # CDNS: ShortTermInvestments는 10-K에만(2025-12 $154M) — 10-Q 시장성 채권 $80.2M(지분 $11.2M은 투자 자산 쪽, Codex·Fable r1 2026-10-25)
                  "0000813672": {"sti": ["AvailableForSaleSecuritiesDebtSecurities"]},
# PCAR: 현금 = 연결 현금(트럭 5,407.8 + 금융 166.9 = 5,574.7 — 현금흐름표 태그, 재무상태표는 부문 차원만), 단기투자 = 트럭 부문 시장성 증권 3,259.6(BUILD dim_facts)(2026-10-23)
                  "0000075362": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsIncludingDisposalGroupAndDiscontinuedOperations"], "sti": ["MarketableSecuritiesCurrentTruckPcar"]},
# OKE: 비지배지분 = 비상환 $100M + 상환 가능 $44M(2026-06, 상환 가능분은 2026년부터, 2026-10-23).
                  "0001039684": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},
# TEL: 비지배지분은 상환 가능 비지배지분 $147M(재무상태표) — 기본 태그는 2024-03에 멈춤(2026-10-23).
                  "0001385157": {"nci": ["RedeemableNoncontrollingInterestEquityCarryingAmount"]},
# TDG: 비지배지분 = 비상환 $9M + 상환 가능 $81M(2026-03부터, 2026-10-22).
                  "0001260221": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},
# AON: 비지배지분 = 비상환 $88M + 상환 가능 $24M(2023-12부터 이 두 태그, 기본 태그는 2024-03에 멈춤, 2026-10-22).
                  "0000315293": {"nci": ["NonredeemableNoncontrollingInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},
# ALL(손해보험): 현금은 재무상태표 "Cash" $840M만(TRV와 같이 단기 증권 $4,872M는 보험 운용자산이라 뺀다), 우선주 $2,001M = PreferredStockIncludingAdditionalPaidInCapital
                  # (기본 PreferredStockValue는 2010년에 멈춤 — 청산가치 $2,050M, 2026-10-22).
                  "0000899051": {"cash": ["Cash"], "sti": [], "preferred": ["PreferredStockIncludingAdditionalPaidInCapital"]},
# SPG: 비지배지분 $1,140M = 운영 파트너십 외부 파트너 $758M + 부동산 비지배 $382M. 유닛은 build_dcf SHARES_ADD로 주식에 더하므로 부동산분만(2026-10-22).
                  "0001063761": {"nci": ["OtherMinorityInterests"]},
# AJG: 재무상태표 현금 $1,386M(수탁 현금 $7,947M은 수탁 자산 안 — 고객 돈이라 빼지 않는다)은 2023-12부터 CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents,
                  # 그 전은 CashAndCashEquivalentsAtCarryingValue(2026-10-22). 2023년 표시 변경 전 제한 현금 태그에는 고객 수탁 현금이 들어 있어(2022-12 $4,964M 대 재무상태표 $342M)
                  # 튜플로 날짜마다 앞 태그 우선(pick_instant) — 리스트로 두면 최신 태그를 통째로 써서 EV 이력이 낮게 깔렸다(Fable r1 필수). 프리미엄 금융 차입금($134M)은 영업 자금이라 차입금에 넣지 않는다(기본값과 같음).
                  "0000354190": {"cash": ("CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"), "sti": [],
                                 "lease": ["OperatingLeaseLiability"]},   # 리스: 분기엔 비유동분만 태그 — 10-K 합계(2025-12 $646M, Codex r1)
# TGT: 재무상태표 현금 $5,411M은 CashCashEquivalentsAndShortTermInvestments — 기본 현금 태그는 2017년에 멈췄고, 단기투자 태그(2026-01 $4,611M)는 현금성 자산 안의 값이라 따로 더하면 두 번 센다(2026-10-22).
                  "0000027419": {"cash": ["CashCashEquivalentsAndShortTermInvestments"], "sti": [], "lease": ["OperatingLeaseLiability"]},   # 리스: 분기엔 비유동분만 태그 — 10-K 합계(2026-01 $3,834M)
                  # ECL: 운용리스 비유동분($576.7M)은 분기 태그가 없어 유동분(OperatingLeaseLiabilityCurrent $165.9M)만 잡혔다 — 합계 OperatingLeaseLiability(10-K, 2025-12 $761.0M)로(2026-10-22).
                  "0000031462": {"lease": ["OperatingLeaseLiability"]},
                  # HPE: 비지배 태그 2024-07 멈춤(10-Q 비지배 $62M은 MinorityInterest로 안 냄) → nci 없음으로, 우선주 태그는 2021년(옛 우선주) — 2024-09 발행 Series C 의무전환 우선주는 nonop_extra 음수로(2026-10-21).
                  "0001645590": {"nci": [], "preferred": []},
                  # HLT: 상환가능 비지배지분 $5M(자본 밖 별도 줄)도 비지배에 — 합계 $33M(Codex 2026-10-21, MCK·SNPS와 같은 처리)
                  "0001585689": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},
                  # TRV: 재무상태표 현금 $766M(제한 현금 $147M 포함)은 Cash 태그 — 기본 태그가 없어 현금 $0이었다(Codex 2026-10-21). 단기 증권은 보험 운용자산이라 넣지 않는다.
                  "0000086312": {"cash": ["Cash"]},
                  # VRT: 단기투자 $300M은 만기보유 채권(유동) 태그, 10-Q "Long-term lease liabilities" $316.4M은 표준 태그가 없어 총 운용리스는 10-K 값(2025-12 $314.5M, 2026-10-21).
                  "0001674101": {"sti": ["DebtSecuritiesHeldToMaturityAmortizedCostAfterAllowanceForCreditLossCurrent"], "lease": ["OperatingLeaseLiability"]},
                  # EOG: 10-Q는 1년 안 운용리스($324M)만 태그하고 비유동분은 "Other Liabilities" 안 — 총 운용리스는 10-K 값(2025-12 $1,199M)을 쓴다(Codex 2026-10-21).
                  "0000821189": {"lease": ["OperatingLeaseLiability"]},
                  # MMM: 현금 줄은 제한 현금 포함 태그($4,835M = 재무상태표 "Cash and cash equivalents"), CashAndCashEquivalentsAtCarryingValue는 2017-03에 멈췄다.
                  # 시장성 증권(유동) $310M은 매도가능 채권 태그(2026-10-21).
                  "0000066740": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"], "sti": ["DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent"],
                                 "nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},   # 상환가능 비지배지분 $971M(Bain의 Madison 합작사 49.9%, 2026-07 — Codex)
                  "0001403161": {"sti": ["Investments"], "preferred": [], "nci": []},
                  # EQIX: 우선주 태그가 2022-12(0)에 멈췄다 — 우선주 없음.
                  "0001101239": {"preferred": []},
                  # ICE: ShortTermInvestments는 2017-12에 멈췄다($16M) — 그 뒤 단기투자 줄 없음("Short-term restricted investments"는 규제 자본, 현금 아님)
                  # EMR: 현금 태그 CashAndCashEquivalentsAtCarryingValue가 2021-12에 멈춤 → 재무상태표 "Cash and equivalents"와 같은 값을 내는 합계 태그.
                  # 단기투자 태그 2016·우선주 태그 2013에 멈춤(없음).
                  # CSX: 현금 태그 CashAndCashEquivalentsAtCarryingValue가 2022-12에 멈춤($1,958M) → 합계 태그(2026-06-30 $1,007M = 원문).
                  # 차입금 태그에 금융리스가 들어 있어 리스는 운용리스만(ETN 방식).
                  # MRSH: 단기투자 줄 없음 — ShortTermInvestments는 2012년 값이 남아 있었다. 수탁 현금($12.3B)은 부채와 맞물린 통과 잔액이라 현금에 넣지 않는다(엔진 기본).
                  "0000062709": {"sti": []},
                  # INTU: 단기투자 AvailableForSaleSecuritiesDebtSecuritiesCurrent가 2023-01에 멈춤($524M) → 재무상태표 "Investments"와 같은 값의
                  # DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent(2022-07~, 2026-07-31 $2,495M). 고객 자금 증권은 "Funds receivable and amounts held for customers" 줄이라 따로(2026-10-18).
                  "0000896878": {"sti": ["DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent", "AvailableForSaleSecuritiesDebtSecuritiesCurrent"]},
                  "0000277948": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"], "lease": ["OperatingLeaseLiability"]},
                  "0000032604": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"], "sti": [], "preferred": []},
                  "0001571949": {"sti": [], "nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCarryingAmount"]},   # 상환가능 비지배지분 $32M(자본 밖 별도 줄, Codex 2026-10-18 — MCK와 같은 처리)
                  # NKE: 재무상태표 "Short-term investments"를 2022-02까지 AvailableForSaleSecuritiesDebtSecuritiesCurrent, 그 뒤로는
                  # DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent로 낸다($1,465M, 2026-08-31). 기본 목록의 ShortTermInvestments는 2014년에 멈춤.
                  "0000320187": {"sti": ["DebtSecuritiesAvailableForSaleExcludingAccruedInterestCurrent", "AvailableForSaleSecuritiesDebtSecuritiesCurrent"]},
                  # SYK: MinorityInterest가 2018-03-31($9M)에 멈춰 그 값이 EV에 더해지고 자본에서 빠졌다 — 지금 재무상태표에 비지배지분 줄이 없다(Codex 2026-10-16).
                  "0000310764": {"nci": []},
                  # SBUX: CashAndCashEquivalentsAtCarryingValue가 2022-07-03($3,178M)에 멈춰 4년 넘게 옛 현금이 쓰였다 — 그 뒤로는
                  # CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents만 낸다(2026-06-28 $3,450M = 재무상태표 현금 $3,449.8M, 2026-10-16).
                  # CME: MinorityInterest가 2021-12에 멈췄다(지금 재무상태표에 비지배지분 줄 없음, 2026-10-16).
                  "0001156375": {"nci": []},
                  # FCX: 우선주 태그가 2009-03-31($832M, 옛 의무전환 우선주)에 멈춰 EV에 더해지고 DCF에서 빠졌다 — 지금 우선주 없음(2026-10-17).
                  "0000831259": {"preferred": []},
                  # TT: 현금 기본 태그는 연말에만 실려(분기는 …IncludingDisposalGroupAndDiscontinuedOperations, 2026-06-30 $1,318.3M) 2025-12 값이 9개월 쓰였다.
                  # 리스는 유동·비유동 태그가 2020-09에 멈췄고 연간 OperatingLeaseLiability만 있다(2025-12 $824.7M — 2021~2024는 값이 없어 2020년 값이 이어진다, 2026-10-16).
                  "0001466258": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsIncludingDisposalGroupAndDiscontinuedOperations"], "lease": ["OperatingLeaseLiability"]},
                  "0000829224": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"]},
                  # WM: ShortTermInvestments는 2013-12($177M)에 멈췄다 — 지금 재무상태표에 단기투자 줄 없음. 금융리스는 차입금 태그 안이라 리스는 운용리스만(연간, 2025-12 $1,010M, 2026-10-21).
                  "0000823768": {"sti": [], "lease": ["OperatingLeaseLiability"]},
                  # AMT: 단기투자 태그 2019-03($18.4M)·우선주 태그 2014-12에 멈춤 — 지금 재무상태표에 둘 다 없음. 금융리스는 "Long-term obligations" 안이라 리스는 운용리스만
                  # (2026-06-30 $644.1M + $7,146.2M, 2026-10-21).
                  "0001053507": {"sti": [], "preferred": [], "lease": ["OperatingLeaseLiabilityCurrent", "OperatingLeaseLiabilityNoncurrent"]},
                  # MAR: MinorityInterest가 2010-09에 멈춤 — 지금 재무상태표에 비지배지분 줄 없음(2026-10-21).
                  "0001048286": {"nci": []},
                  # WMB: 현금 태그 CashAndCashEquivalentsAtCarryingValue가 2023-09에 멈춤($2,074M) → 합계 태그(2026-06-30 $203M = 재무상태표 현금).
                  # 리스는 유동·비유동 태그가 2024-12에 멈추고 연간 OperatingLeaseLiability만 있다(2025-12 $183M, TT 방식, 2026-10-19).
                  "0000107263": {"cash": ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"], "lease": ["OperatingLeaseLiability"]},
                  # MCK: 비지배지분 대부분이 상환 가능 비지배지분(재무상태표 메자닌, 2026-06-30 $2,563M — Core Ventures 30%(풋옵션)와 Apollo의
                  # 의료·수술 부문 전환우선주 약 13% $1.25B, 10-Q Note 5)이라 MinorityInterest($376M)만 잡혔다. 연결 EBITDA에 그 몫이 다 들어 있어 EV에 더한다(2026-10-13).
                  "0000927653": {"nci": ["MinorityInterest", "RedeemableNoncontrollingInterestEquityCommonCarryingAmount"]},
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
# 회사별 태그가 그 시점에 없어도 기본 태그로 돌아가지 않는 항목 — 기본 태그가 다른 범위를 잡는다(build_dcf.base_inputs).
# SPG: 기본 MinorityInterest(2021-10 $476M)에 운영 파트너십 유닛이 들어 있어 SHARES_ADD와 겹친다(r6 회귀, 2026-10-25).
EV_TAGS_NO_DEFAULT = {"0001063761": {"nci"}}
# 이 결산일부터 0인 구성요소(CIK) — 잔액이 사라졌는데 태그가 멈춰 마지막 값이 계속 쓰이는 경우. JNJ 비지배지분은
# 2023-07-02(Kenvue 분리 중) $1,260M이 마지막이고 8월 교환 공개매수로 사라졌다 → 2023-10-01 분기(10-Q 2023-10-27)부터 0.
# 전 기간 0으로 두면 실제 잔액이 있던 2023년 EV까지 빠진다(Codex, 2026-09-28).
EV_ZERO_FROM_BY_CIK = {# PCAR: 차입금은 트럭·부품·기타 부문만(CAT·DE·GM 규칙) — 그 부문엔 차입금이 없다(금융 서비스 CP·은행 차입 $4,789M·채권 $9,908M 제외, Q2 2026 10-Q).
                       # 기본 태그가 금융 서비스 차입을 잡지 않게 전 기간 0(2026-10-23)
                       "0000075362": {"debt": ("2000-01-01", "2000-01-01")},
                       "0000200406": {"nci": ("2023-10-01", "2023-10-27")},
                       # KHC: Berkshire 보유 9% 누적 우선주 $8,320M을 2016-06-07 전액 상환·소각(8-K 2016-06-07, 현금흐름표 2016-07-03 상반기 상환 $8,320M) —
                       # 그 뒤 우선주 태그가 없어 2015-06-28 값이 낡은 값으로 남았다(Codex r2, 2026-10-25). 상반기 10-Q 공시일부터 0.
                       "0001637459": {"preferred": ("2016-07-03", "2016-08-05")},
                       # MNST: 2024년 자사주 공개매수 자금 차입($750M)을 2025년 상반기에 다 갚았다 — 2025-03 $199M 뒤 차입금 태그가 없다(Q2 2025 10-Q 재무상태표에 차입금 줄 없음).
                       # 마지막 값이 계속 이어지지 않게 2025-06-30부터 0(가용일 = Q2 2025 10-Q 2025-08-08, 2026-10-22).
                       "0000865752": {"debt": ("2025-06-30", "2025-08-08")}}
# 차입금 합계의 가용일을 10-K 원문 날짜로 바로잡는 회사(CIK → {분기말: 가용일}). 합계 가용일은 구성요소 중 가장 늦은 접수일인데,
# 한 구성요소(0)가 나중 공시의 비교 열에서만 태깅되면 그 분기 값이 1년 가까이 늦게 열린다.
# PANW: 2025-07-31 전환사채 0(유동 0은 FY2025 10-K 2025-08-29, 비유동 0은 2026-06-03 10-Q 비교 열에서만 태깅) — FY2025 10-K 재무상태표에
# 전환사채 줄이 "—"이고 옛 사채는 2025-06-01까지 전환·상환(FY2026 10-K Note 12, Codex). 그래서 2025-08-29부터 0이다.
# DRI: 단기 줄이 10-K에서 0(태그 없음)이거나 LongTermDebtCurrent로 붙어, ShortTermBorrowings 값은 다음 10-Q 비교 열에서야 나온다 — 합계 반영이 몇 달 늦었다.
# 값은 10-K 재무상태표와 같으므로 10-K 접수일로 당긴다(Codex 2026-11-03).
DEBT_AVAILABLE_FIX = {"0001327567": {"2025-07-31": "2025-08-29"},
                      "0000940944": {"2022-05-29": "2022-07-22", "2023-05-28": "2023-07-21", "2026-05-31": "2026-07-24"}}


# F4(input_fix_prereg, 2026-10-10): 차입금 세부 태그가 일부만 잡히면 총계로 바꾸지 않는 회사들. 금융 섹터는 차입금 정의가 달라
# 통째로 뺀다(은행 카드는 bank_items 경로). CAT·DE는 금융 자회사 부문 차입금을 뺀 값이 사용자 결정(2026-09-30)이라 총계와 다른 게 맞다.
# BX는 LoansPayable, VRTX는 0.5배 규칙과 맞지 않는 회사별 결정.
DEBT_TOTAL_FALLBACK_SKIP = {"0000075362", "0000018230", "0000315189", "0001393818", "0000875320", "0001467858"}
_FIN_CIKS = None


def _financial_ciks():
    global _FIN_CIKS
    if _FIN_CIKS is None:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor", "sp500.json")
        _FIN_CIKS = {str(r.get("cik")).zfill(10) for r in json.load(open(p)) if r.get("sector") == "Financials"} if os.path.exists(p) else set()
    return _FIN_CIKS


def _debt_total_fallback(cik, out):
    """F4: 그 종료일의 엔진 차입금이 없거나 같은 종료일 `LongTermDebt`(총계)의 0.5배 미만이면 바꾼다 — LIN 2022-09-30은 세부 중
    단기차입 $3.18B만 태깅해 10-Q 합계 $15.34B가 빠졌다(회사별 목록 경로라 총계 대체 전에 끝났다). 순서: ① 그날의
    `DebtLongtermAndShorttermCombinedAmount` ② `LongTermDebt` + 단기 차입(`ShortTermBorrowings`, 없으면 `CommercialPaper`).
    단기 차입에 1년 안 만기 장기분이 들어 있는 회사(build_dcf.STB_INCLUDES_CURRENT_LTD)는 장기 비유동분 + 단기 차입,
    `LongTermDebt`를 비유동분으로만 내는 회사(DEBT_NONCURRENT_ONLY)는 + `DebtCurrent`. 바꾼 점에는 `_note`를 남긴다."""
    if cik in DEBT_TOTAL_FALLBACK_SKIP or cik in _financial_ciks():
        return out
    ltd = {e["end"]: e for e in component_sum(cik, ["LongTermDebt"])}
    comb = {e["end"]: e for e in component_sum(cik, ["DebtLongtermAndShorttermCombinedAmount"])}
    if not ltd and not comb:
        return out
    import build_dcf as _bd
    have = {e["end"]: e for e in sorted(out, key=lambda e: e["available"])}   # 결산일마다 마지막 행(완전한 합)으로 판정
    stb = {e["end"]: e for e in component_sum(cik, ["ShortTermBorrowings"])}
    cp = {e["end"]: e for e in component_sum(cik, ["CommercialPaper"])}
    nonc = {e["end"]: e for e in component_sum(cik, ["LongTermDebtNoncurrent"])}
    curr = {e["end"]: e for e in component_sum(cik, ["LongTermDebtCurrent"])}
    dc = {e["end"]: e for e in component_sum(cik, ["DebtCurrent"])}
    changed = False
    for end in sorted(set(ltd) | set(comb)):
        L, e = ltd.get(end), have.get(end)
        if L is None:
            if e is not None:                              # 총계(LongTermDebt)가 없으면 엔진 값이 없을 때만 합계 태그로
                continue
        elif e is not None and e["val"] >= 0.5 * L["val"]:
            continue
        # 합계 태그가 부분값인 회사가 있다(GPC 2014: 합계 태그 $500M = 비유동분, LongTermDebt $765.5M — Fable) — 총계의 절반 이상일 때만
        if end in comb and (L is None or comb[end]["val"] >= 0.5 * L["val"]):
            parts = [comb[end]]
        else:
            if cik in _bd.STB_INCLUDES_CURRENT_LTD:
                if end in nonc:
                    base_ = [nonc[end]]
                elif end in curr:
                    base_ = [L, {"val": -curr[end]["val"], "available": curr[end]["available"]}]
                else:
                    base_ = [L]
            else:
                base_ = [L]
            short = stb.get(end) or cp.get(end)
            extra = [dc[end]] if (cik in DEBT_NONCURRENT_ONLY and end in dc) else []
            parts = base_ + ([short] if short else []) + extra
        val = sum(x["val"] for x in parts)
        have[end] = {"end": end, "val": val, "available": max(x["available"] for x in parts), "_note": "debt_total_fallback"}
        changed = True
    # 결산일당 여러 행(E65)은 살린다 — 대체한 결산일은 그 결산일 행을 모두 대체 행 하나로, 나머지 결산일의 부분 행은 그날 이미 공개된
    # 총계(LongTermDebt)의 절반 미만이면 버린다(미래의 완전한 합으로만 판정하면 그 사이 부분 합이 그대로 통과 — Codex E65 r1, EXC)
    rows = []
    for e in out:
        h = have.get(e["end"])
        if h is not None and h.get("_note") == "debt_total_fallback":
            continue
        L = ltd.get(e["end"])
        if h is not None and e is not h and L is not None and L["available"] <= e["available"] and e["val"] < 0.5 * L["val"]:
            changed = True
            continue
        rows.append(e)
    rows += [h for h in have.values() if h.get("_note") == "debt_total_fallback"]
    return sorted(rows, key=lambda e: (e["available"], e["end"])) if changed else out


# 원문으로 **그 시점에 없어진 것**을 확인한 EV 구성요소 — 그 결산일에 0 관측 하나를 끼운다(공개일 = 그 공시). EV_ZERO_FROM_BY_CIK와 달리
# 그 뒤 실제 값은 지우지 않는다(ULTA는 2020-09 차입금 $800M을 다 갚고 2023-10 다시 $195M을 빌렸다). 확인 출처는 Codex r3(2026-10-25).
EV_ZERO_AT_BY_CIK = {"0000879169": {"debt": [("2020-12-31", "2021-02-09")]},    # INCY: 남은 2020 전환사채를 만기 전 주식으로 전환(10-K 2020)
                     # HOOD: 2021-02 전환사채 $3.55B(공정가치 $5.19B)가 상장 완료(2021-08-02) 때 보통주로 전환 — 10-Q 2021-09-30 자본변동표 "Conversion of
                     # convertible notes to common stock … 5,217,597"(천 달러). 신용한도는 같은 분기 전액 상환. 표지가 없어 2021-06 $5.19B가
                     # 2025-12까지 차입금으로 남았다(안건 E66, 2026-10-30)
                     "0001783879": {"debt": [("2021-09-30", "2021-10-29")]},
                     "0001001250": {"sti": [("2019-03-31", "2019-05-01")]},     # EL: 단기투자 2019-03-31 재무상태표 '—'(10-Q)
                     "0001513761": {"sti": [("2022-03-31", "2022-05-10")]},     # NCLH: 1분기 만기 회수 $240M·신규 매입 0, 재무상태표 0(10-Q)
                     "0001524472": {"sti": [("2020-12-31", "2021-02-26")]},     # XYL: 단기투자 $200M 연간 매입·회수 같고 연말 재무상태표에 없음(10-K 2020)
                     "0001403568": {"debt": [("2020-10-31", "2020-12-03")]},    # ULTA: 2020-09-02 신용한도 $800M 전액 상환, 10-Q 차입금 0
                     # MSI: 단기투자가 Q3 2017 10-Q(2017-11-03) 재무상태표에 없다 — 2017-09-30 유동자산은 현금 $653M·제한현금 $64M·매출채권·재고·기타뿐이고
                     # AvailableForSaleSecuritiesCurrent 태그도 0이다. 기본 태그 MarketableSecuritiesCurrent가 2015-10-03 $276M(총자산의 2%)에 멈춰
                     # DCF가 계속 보류됐다(MSI 카드 2026-10-26·27 실패). 지금 남은 투자 $300M은 장기(LongTermInvestments)라 EV 현금에 넣지 않는다.
                     # 0을 그 결산일에 한 칸만 끼운다 — 기본 수집 태그로 다시 공시하면 그 값이 살아난다(ZERO_FROM은 이후 값을 버린다 —
                     # dr r2에서 2027년 가짜 관측으로 확인). 2015~2017에 쓴 AvailableForSaleSecuritiesCurrent로만 다시 내면
                     # 수집 단계에서 못 읽고 0이 최신으로 남는다(1% 문턱도 못 넘어 표식 없음) — MSI 전용 태그 지정은 백로그(dr r2).
                     "0000068505": {"sti": [("2017-09-30", "2017-11-03")]}}


EV_TAGS_NO_DEFAULT_CASH_FILL = set()   # 현금 합계 대체를 쓰지 않을 회사(필요하면 원문 확인 뒤 추가)
CASH_TOTAL_TAGS = ["CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
                   "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalentsIncludingDisposalGroupAndDiscontinuedOperations"]


def _cash_total_fill(cik, out):
    """배수 엔진 현금: 기본 태그의 직전 결산일보다 200일 넘게 뒤의 결산일을 현금 + 제한현금 합계 태그(재무상태표·현금흐름표 기말 현금)
    − 같은 결산일 제한현금으로 채운다 — DCF base_inputs의 현금 대체(2026-10-25)와 같은 값. 배수 엔진에는 없어 INTC는 2021-09 현금
    $7.9B가 2023-01~2025-07 EV에 쓰였다(안건 E66, 2026-10-30). 시점 규칙: '직전' 기본 결산일은 그 합계 행 공개일까지 공개된 기본 행에서만
    고르고(뒤에 나온 기본 행이 앞 계산을 바꾸지 않게, Codex E66 r1), 같은 결산일 기본 행이 나중에 나오면 그날부터 기본 행이 이긴다(newest_row).
    배수 엔진 시리즈에서만 쓴다 — DCF는 자체 대체(제한현금·dq 표식)를 쓰므로 ev_component에 넣지 않는다(Codex E66 r1)."""
    if not out:
        return out
    rc_tot = pick_instant(cik, ["RestrictedCashAndCashEquivalents", "RestrictedCash", "RestrictedCashAndCashEquivalentsAtCarryingValue"])
    rc_cur = pick_instant(cik, ["RestrictedCashCurrent", "RestrictedCashAndCashEquivalentsCurrent"])
    rc_non = pick_instant(cik, ["RestrictedCashNoncurrent", "RestrictedCashAndCashEquivalentsNoncurrent"])

    def _rc(end, avail):
        at = lambda rows: next((r["val"] for r in rows if r["end"] == end and r["available"] <= avail), None)
        v = at(rc_tot)
        if v is None:
            c, n = at(rc_cur), at(rc_non)
            v = None if c is None and n is None else (c or 0) + (n or 0)
        return max(v or 0, 0)
    fill = []
    for e in pick_instant(cik, CASH_TOTAL_TAGS):
        known = [b for b in out if b["available"] <= e["available"]]
        if any(b["end"] == e["end"] for b in known):
            continue                     # 같은 결산일 기본 행이 이미 공개됨 — 기본 행
        prev = [b["end"] for b in known if b["end"] < e["end"]]
        if not prev:
            continue
        if (date.fromisoformat(e["end"]) - date.fromisoformat(max(prev))).days > 200:
            fill.append(dict(e, val=e["val"] - _rc(e["end"], e["available"]), _note="cash_total_tag"))
    return sorted(out + fill, key=lambda e: (e["available"], e["end"])) if fill else out


def ev_component(cik, name, tags):
    out = _ev_component(cik, name, tags)
    if name == "debt" and not EV_ZERO_FROM_BY_CIK.get(cik, {}).get(name):
        out = _debt_total_fallback(cik, out)
    # 확인된 0은 총계 대체 **뒤에** 끼운다 — 앞에 끼우면 그 날짜의 LongTermDebt 행이 0을 덮어쓸 수 있다(Fable r4)
    zat = EV_ZERO_AT_BY_CIK.get(cik, {}).get(name)
    if zat:
        have = {e["end"] for e in out}
        out = sorted(out + [{"end": e, "val": 0.0, "available": a} for e, a in zat if e not in have], key=lambda e: e["available"])
    return out


def _debt_total_tag_rows(cik):
    """DEBT_TOTAL_TAG로 지정한 차입금 총계 행 — 문자열 항목은 더하고, 튜플 항목은 날짜마다 앞 태그 우선(pick_instant)."""
    tags = DEBT_TOTAL_TAG[cik]
    tags = tags if isinstance(tags, list) else [tags]
    if not any(isinstance(t, tuple) for t in tags):
        return component_sum(cik, tags)
    # 튜플 항목은 날짜마다 앞 태그 우선(pick_instant), 문자열 항목은 그대로 더한다(KO).
    # 같은 결산일에 한 항목이 행을 둘 이상 낼 수 있다(나중 공시가 같은 날짜를 다시 싣거나 튜플의 앞 태그가 늦게 공개 — pick_instant는 공개 시점마다
    # 행을 낸다). 전에는 그 행들을 다 더해 그 날짜 차입금이 두 배였다(AES 2024-06·09, BBY·ED·KO 등 13곳의 과거 날짜 — 2026-11-07 사용자 승인,
    # AES Codex r1). 이제 공개일마다 "그날까지 공개된 항목별 가장 새 행"을 더한 합계 행을 낸다 — 모든 항목이 처음 공개된 날부터(전과 같은 시작),
    # 뒤에 고쳐 실린 날마다 새 행. 먼저 공개된 정상 값을 늦추지 않는다(Codex r2: 가장 늦은 행 하나만 쓰면 AES 2024-06이 2025-03-11로 밀렸다).
    per_end = {}
    for k, t in enumerate(tags):
        for e in (pick_instant(cik, list(t)) if isinstance(t, tuple) else component_sum(cik, [t])):
            per_end.setdefault(e["end"], {}).setdefault(k, []).append(e)
    rows = []
    for end, items in per_end.items():
        for k in items:
            items[k].sort(key=lambda e: e["available"])
        start = max(r[0]["available"] for r in items.values())
        dates = sorted({e["available"] for r in items.values() for e in r if e["available"] >= start})
        prev = None
        for d in dates:
            val = sum([e for e in r if e["available"] <= d][-1]["val"] for r in items.values())
            if prev is None or val != prev:
                rows.append({"end": end, "val": val, "available": d})
                prev = val
    fix = DEBT_AVAILABLE_FIX.get(cik, {})
    if fix:   # 공개일을 손으로 고친 결산일은 전처럼 한 행(마지막 값)으로
        keep = [r for r in rows if r["end"] not in fix]
        for end, av in fix.items():
            last = [r for r in rows if r["end"] == end]
            if last:
                keep.append({"end": end, "val": last[-1]["val"], "available": av})
        rows = keep
    return sorted(rows, key=lambda e: e["available"])


def _ev_component(cik, name, tags, _no_total=False):
    tags = EV_TAGS_BY_CIK.get(cik, {}).get(name, tags)
    zf = EV_ZERO_FROM_BY_CIK.get(cik, {}).get(name)
    if zf:
        rows = [e for e in component_sum(cik, tags) if e["end"] < zf[0]]
        return rows + [{"end": zf[0], "val": 0.0, "available": zf[1]}]
    if name == "debt" and cik in DEBT_TOTAL_TAG and not _no_total:
        des = _debt_total_tag_rows(cik)
        # 지정 총계가 시작하기 **전**은 기본 경로로 — UAL 지정 태그는 2023-12부터라 그 전이 2014년에 멈춘 LongTermDebt로
        # 보류됐다(재봉인 점검 2026-10-26). 지정 총계가 아직 하나도 없으면
        # (연구 패널은 공시일로 자르므로 지정 태그를 처음 낸 공시 전 평가일이 그렇다) 전부 기본 경로 — 오래 멈춘 값은 build_dcf가 낡음으로 거른다.
        # 기본 경로가 다른 범위를 잡는 회사(DEBT_TOTAL_FALLBACK_SKIP — CAT·DE·GM은 금융 부문 빼고, 지정 값이 부문 차원 자료라 연구
        # 스냅샷에 없다)는 돌아가지 않는다 — 돌아가면 금융 자회사 차입금까지 더해 CAT 현금흐름 칸이 '매우 비싸다'로 바뀌었다(q2 회귀).
        if cik in DEBT_TOTAL_FALLBACK_SKIP:
            return des
        # 자르는 기준은 지정 행이 처음 **공개된 날**이다(결산일이 아니라). UAL 지정 태그는 2025-02-27 10-K가 2023-12 결산까지 거슬러 처음
        # 실었다 — 결산일로 자르면 그 공시 뒤에 과거를 볼 때 2024-03·06·09 분기가 빠지고 2023-09 값이 이어졌다(재봉인 dr r1 2026-10-27).
        # 같은 결산일이 둘 다 있으면 newest()가 늦게 공개된 지정 행을 고른다.
        first = min((e["available"] for e in des), default="9999-12-31")
        old = [e for e in _ev_component(cik, name, tags, _no_total=True) if e["available"] < first]
        return sorted(old + des, key=lambda e: e["available"])
    if isinstance(tags, tuple):   # EV_TAGS_BY_CIK 값이 튜플이면 날짜마다 앞 태그 우선(AJG 현금 — 표시 변경 전 태그를 옛 날짜에, 2026-10-22 Fable)
        return pick_instant(cik, list(tags))
    # 단기투자를 회사별로 지정한 목록(EV_TAGS_BY_CIK)은 그 결정대로 더한다 — KO는 단기투자(정기예금)와 시장성 증권이 재무상태표 다른 줄(E67)
    pick = name in PICK_COMPONENTS and not (name == "sti" and cik in STI_SUM_CIKS)
    out = pick_instant(cik, tags) if pick else component_sum(cik, tags)
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
        rows_by_end = {}
        for e in out:
            rows_by_end.setdefault(e["end"], []).append(dict(e))
        for e in component_sum(cik, ["LongTermDebtAndCapitalLeaseObligations"]):
            if e["end"] in nonc or e["end"] in total_dates:
                continue
            rows = rows_by_end.get(e["end"])
            if not rows:
                rows_by_end[e["end"]] = [dict(e)]
                continue
            # 결산일당 여러 행(E65 시점 합산)을 살린다 — 보충 행이 공개된 뒤의 행에만 더하고, 보충이 마지막 행보다 늦으면 그 날짜에 새 행
            for r in rows:
                if e["available"] <= r["available"]:
                    r["val"] += e["val"]
            last = max(rows, key=lambda r: r["available"])
            if e["available"] > last["available"]:
                rows.append({"end": e["end"], "val": last["val"] + e["val"], "available": e["available"]})
        out = sorted((r for rs in rows_by_end.values() for r in rs), key=lambda e: (e["available"], e["end"]))
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
        # 튜플 = 같은 줄의 두 태그 이름(CME) — dda_quarters와 같게 행을 합친다. 연간 보충은 "pick"(대체 이름이라 더하지 않는다)
        part = sum((concept(cik, n) for n in tag), []) if isinstance(tag, tuple) else concept(cik, tag)
        if not part:
            continue
        q = quarterly_flow(part, ticker)
        series = (with_annuals(ttm_series(q) if q else [], list(tag), "pick") if isinstance(tag, tuple)
                  else with_annuals(ttm_series(q) if q else [], [tag], "sum"))
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
    return "+".join("|".join(t) if isinstance(t, tuple) else t for t in per_tag), out


def check_fresh(series, last_day, max_lag_days=200):
    """시리즈가 최근 분기까지 닿는지 본다.

    태그 교체를 놓치면 옛 값이 조용히 계속 쓰이므로, 마지막 일봉보다 크게
    뒤처지면 눈에 띄게 표시한다.
    """
    if not series:
        return "  ← 비어 있음"
    lag = (date.fromisoformat(last_day) - date.fromisoformat(series[-1]["end"])).days
    return f"  ← ⚠ {lag}일 뒤처짐" if lag > max_lag_days else ""


def newest_row(rows):
    """공개된 행들 가운데 **결산일이 가장 늦은 행**(같은 결산일이면 늦게 공개된 정정값, 그다음 목록 순서) — DCF `build_dcf.newest`와 같은 규칙.
    결산일이 공개일보다 늦은 행은 오태깅이라 고르지 않는다. 결산일이 없는 행(end 없음)은 가장 이른 결산일로 본다."""
    best = None
    for i, e in enumerate(rows):
        if e.get("end") and e["end"] > e["available"]:
            continue
        k = (e.get("end") or "", e["available"], i)
        if best is None or k > best[0]:
            best = (k, e)
    return best[1] if best else None


def as_of_entry(series, day):
    """그날까지 공개돼 있던 행 가운데 결산일이 가장 늦은 행(newest_row). 시리즈는 공개일 순서다.

    예전에는 공개일 순서의 마지막 원소를 골라, 옛 결산일이 나중 공시에서 처음 나오면(분사·신규 상장의 분사 전 비교 열,
    분기 중간 날짜 단독 태그 행) 그 옛 값이 그날의 최신 값을 덮었다 — GEHC 2023-07~2024-04 자본 2022-06-30 $17.1B가
    최신 자본을 덮어 PBR 이력이 절반으로, VMC 차입금 CommercialPaper 2022-08-31 단독 행이 분기말 총 차입금 $4.19B를
    125거래일 덮었다(안건 E63, Codex·Fable 2026-10-29). DCF는 2026-10-25에 같은 규칙으로 고쳤다."""
    i = 0
    while i < len(series) and series[i]["available"] <= day:
        i += 1
    return newest_row(series[:i])


def as_of(series, day):
    """그날까지 공개돼 있던 가장 최근 결산일의 값(as_of_entry)."""
    e = as_of_entry(series, day)
    return e["val"] if e else None


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
                 # LVS: 마카오 봉쇄 해(2020~2022) 매출·EBITDA가 바닥이라 PSR·EV/EBITDA 이력이 수십~수백 배로 튀어 오늘이 싸 보였다.
                 # 재개장 뒤 첫 최근 4분기 합(FY2023 10-K, 2024-02-07)부터 비교한다(2026-11-03).
                 "LVS": "2024-02-07",
                 "WYNN": "2024-02-23",   # WYNN: 마카오 봉쇄(2020~2022) 기저 — 자기 이력 PER 최고 1,768배·적자 구간. 재개장 뒤 첫 최근 4분기 합(FY2023 10-K, EPS 파일 공개일 2024-02-23)부터(LVS 방식, 2026-11-06)
                 "NCLH": "2024-02-28",   # NCLH: 코로나 적자(FY20~FY22) 뒤 첫 흑자 해 FY2023 10-K 공시일(2024-02-28, 실적 발표는 02-27)부터 — 그 전 PER·EV/EBITDA는 음수·수백 배(2026-11-04)
                 # EXC: Constellation 분사(2022-02-01). 최근 4분기가 모두 분사 뒤인 첫 시점(FY2022 10-K, 2023-02-14 — T 방식). 그 전은 재작성 연간 − 원공시 9개월로
                 # 2020년 4분기 매출이 −$8,262M이 되어 PSR이 8배로 튀었다(2026-10-28, Fable r1 후속).
                 "EXC": "2023-02-14",
                 # MMM: Solventum 분사(2024-04-01) 뒤 첫 재무상태표(2024-06-30)가 나온 2분기 10-Q 공시일(2026-10-21, GE 방식). 2024년 1분기는
                 # 원공시가 Solventum을 포함해 나중(10-K 2025-02-05)에 재작성됐고, RESTATED_LATEST로 재작성 값을 쓴다.
                 "MMM": "2024-07-26",
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
                 "DHR": "2023-10-24",
                 # EMR: Climate Technologies(Copeland) 지분 55% 매각 완료(2023-05-31) 뒤 첫 재무상태표(2023-06-30)가 나온 3분기 10-Q 공시일
                 # (2026-10-18 사용자 결정 "GE 방식 + 매각 뒤 창"). 재작성 분기 값이 FY22 1분기부터 있어 그날 최근 4분기 합은 모두 계속사업 기준.
                 "EMR": "2023-08-02",
                 # AMT: 인도 사업(ATC TIPL) 매각 완료 2024-09-12. 2024년 1·2분기는 인도 포함 값으로 처음 공시됐고, 계속사업 기준 분기·연간 재작성 값이
                 # 처음 함께 나온 것은 FY2024 10-K(2025-02-25)다 — 그날부터(WDC 방식, 2026-10-21). 그날 최근 4분기 합 = 2024년 계속사업 연간.
                 "AMT": "2025-02-25",
                 # VRSK: 에너지(Wood Mackenzie) 중단사업 재작성 — 계속사업 연간이 처음 나온 FY2022 10-K(2023-02-28)부터. 그 전 최근 4분기 합은 에너지 포함 원공시와 섞였다(2021 Q4 매출 $229.9M, Codex r1 2026-10-30).
                 "VRSK": "2023-02-28",
                 # EVRG: 2021년 1~3분기 장기부채가 SEC 요약 자료에 없다(차원·고유 태그) — 차입금이 $1.0~1.7B로만 잡혀 EV/EBITDA가 6.6배로 낮게 나왔다. 장기부채가 다시 잡히는 FY2021 10-K(2022-02-25)부터(Codex r1, 2026-10-30).
                 "EVRG": "2022-02-25",
                 # PPL: EPS 이력에 2021 Q1~2022 Q3 행이 없다(2021 영국 사업 중단사업) — 옛 TTM이 재사용됐다. 2022-05 로드아일랜드 인수가 최근 4분기에 온전히 들어간 Q2 2023 10-Q(2023-08-04)부터(Codex r1, 2026-10-30).
                 "PPL": "2023-08-04",
                 # VLTO: 2023-10 Danaher 분사 상장 — 분사 전 캐브아웃 EPS(이자 거의 0)가 최근 4분기 합에 섞이지 않는 첫 날(분사 뒤 네 분기, Q3 2024 10-Q 2024-10-24)부터(Codex r1, 2026-10-30).
                 "VLTO": "2024-10-24",
                 # LH: Fortrea 분사(2023-06-30). 2023 Q1 계속사업 재작성 값이 처음 나온 Q1 2024 10-Q(2024-04-30)부터 — 그날 최근 4분기 합이 모두 계속사업(WDC 방식, 2026-10-30).
                 "LH": "2024-04-30",
                 # NWSA: Foxtel 매각(DAZN, 2025-04-02 완료). 계속사업 기준 분기·연간 재작성 값이 처음 함께 나온 것은 FY2025 10-K(2025-08-06) — 그날부터(AMT 방식, 2026-10-30).
                 # 그 전 최근 4분기 합은 Foxtel 포함 원공시(FY2022 매출 $10,385M 대 재작성 FY2023 $8,012M)와 섞여 PSR이 싸게 나왔다.
                 "NWSA": "2025-08-06"}


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
    ap.add_argument("--drop", default="", help="계산하지 않을 배수(쉼표, PCR·EV/EBITDA) — 보험 RIM 카드(사전 등록 insurer_rim_prereg §1, CB처럼 파일에서 빠진다)")
    args = ap.parse_args()
    t = args.ticker.upper()
    cik = feh.CIKS.get(t)
    if not cik:
        sys.exit(f"{t}: CIK를 모른다. fetch_eps_history.py의 CIKS에 추가할 것")
    validate_fixes(cik, t)   # E55 — 카드·동종업 빌드마다 그 종목 고침이 자료와 맞는지(카드 빌드는 경고, FACT_FIXES_STRICT=1이면 멈춤)
    check_ocf_netting(cik)   # E57 — 담보금 빼기 대상(CBOE)이면 accn 충돌·양식·최신 행 짝 검사

    daily = history_daily(t, load_daily(t))
    print(f"{t}: 일봉 {len(daily)}개 ({daily[0][0]} ~ {daily[-1][0]})"
          + (" — 원주 가격 이력 + 마지막 날 ADR 가격" if t in LOCAL_HISTORY else ""))

    # EPS는 기존 스크립트가 이미 만든 형식을 그대로 쓴다
    eps_path = os.environ.get("EPS_HISTORY", "")
    eps = []
    _a3_rows = _a3_cap = None   # A3 순이익률 조정(_eo_ni)이 PER과 같은 EPS 행·cap을 쓰게(Codex A3 r1)
    if eps_path and os.path.exists(eps_path):
        # 일회성 세금을 뺀 EPS — 항목은 그 분기 실적과 같은 공시에서 밝혀지므로 같은 시점에 반영한다
        cap = _approved().get(str(cik).zfill(10))   # 카드 공시 기준표 — 그 뒤에 알려진 EPS는 쓰지 않는다(비교군으로 쓰일 때도, Codex 2026-10-08)
        # 일회성 손익(v2/eps_oneoff.json, 안건 E54)도 TTM 결산일마다 반복·문턱 판정 뒤 뺀다. 이 장치가 있는 종목은 EPS 0 행도 읽어
        # 조정 뒤 값으로 0·음수를 가른다(설계 e54_v2_design §6). 연구 모드(ASOF_REF)에서는 eps_oneoff가 빈 목록을 돌려준다.
        _rows = json.load(open(eps_path))
        _eo_on = _eo.has(t)
        _a3_rows, _a3_cap = _rows, cap
        eps = [{"available": e["available_date"], **({"end": e["quarter_end"]} if e.get("quarter_end") else {}),   # 결산일(E63 newest_row)
                "val": e["ttm_eps"] + oneoff_in_ttm(t, e.get("quarter_end"), "eps")
                       + disc_in_ttm(t, _rows, e.get("quarter_end"), e["available_date"])   # E62 계속영업 EPS
                       + (_eo.eps_adjust(t, _rows, e.get("quarter_end"), cap, row=e) if _eo_on else 0.0)}
               for e in _rows if (e.get("ttm_eps") is not None if _eo_on else e.get("ttm_eps"))
               and (not cap or e["available_date"] <= cap)]
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
        if name == "equity":
            # PBR 분모는 보통주 자본 — 자본 안 비전환 우선주를 빼고 비지배지분 포함 총계는 지배주주 자본으로 되돌린다(안건 E44, v2/common_equity.py)
            series[name] = common_equity.ce_series(cik, t, series[name])
        if name == "shares":   # F3 (a) — DCF와 같은 대조를 배수 시리즈에도
            series[name], _sdq = check_shares(series[name], cik, t)
            for x in _sdq:
                print(f"  ⚠ 주식 수 대조: {x}")
        stale = check_fresh(series[name], daily[-1][0])
        print(f"  {name}: {tag} — 시점 {len(series[name])}개"
              f" · 최신 {series[name][-1]['end'] if series[name] else '없음'}{stale}")

    # EV 구성요소(시점)와 EBITDA(기간)
    for name, tags in EV_COMPONENTS.items():
        series[name] = ev_component(cik, name, tags)
        # 현금 합계 대체(E66) — 배수 엔진에서만. 금융회사(은행 카드는 따로 정한 현금 정의)·현금 태그를 회사별로 지정한 회사는 그 결정을 따른다
        if (name == "cash" and cik not in EV_TAGS_NO_DEFAULT_CASH_FILL and cik not in _financial_ciks()
                and "cash" not in EV_TAGS_BY_CIK.get(cik, {})):
            series[name] = _cash_total_fill(cik, series[name])
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
    _eo_tag, _a8_q = None, {}
    if core:
        # 공시 순이익에 투자 평가이익이 크게 섞인 종목은 PER을 본업 이익으로 낸다.
        # GOOGL 2026 Q2: 영업이익 $40.8B, 영업외이익 $98.0B, 희석 EPS $9.11(본업만 약 $2.7).
        for name, tags in CORE_TAX_TAGS.items():
            tag, rows = pick_tag(cik, tags)
            _a8_q[name] = quarterly_flow(rows, t) if rows else []
            series[name] = ttm_series(_a8_q[name]) if rows else []
            if name == "pretax" and not series[name]:
                # 세전이익을 연간에만 태그한 회사(MRVL)는 분기 세전 = 순이익 + 법인세로 만든다 — build_dcf.base_inputs와 같은 대체(2026-10-01)
                _, nr = pick_tag(cik, ["NetIncomeLoss"]); _, tr = pick_tag(cik, CORE_TAX_TAGS["tax"])
                nq = {e["end"]: e for e in quarterly_flow(nr, t)}; tq = {e["end"]: e for e in quarterly_flow(tr, t)}
                merged = [dict(nq[k], val=nq[k]["val"] + tq[k]["val"], filed=max(nq[k]["filed"], tq[k]["filed"])) for k in sorted(nq) if k in tq]
                series[name] = ttm_series(merged)
                _a8_q[name] = merged
                tag = "NetIncomeLoss + 법인세(분기 세전 태그 없음)"
            print(f"  {name}: {tag} — TTM {len(series[name])}개 (본업 기준 PER용)")
            if name == "pretax":
                _eo_tag = "NI+TAX" if str(tag).startswith("NetIncomeLoss + ") else tag   # 일회성 장치 세전 태그 대조(E54)
        nis = net_interest_series(cik, t)
        lastni = net_interest_at(nis, series["opinc"][-1]["end"]) if series.get("opinc") else None
        print(f"  순이자(A8): 최근 {'결측 — 영업이익만' if lastni is None else f'{lastni / 1e6:,.0f}M'}")
    else:
        nis = None
    # 일회성 손익 장치(E54)의 A8 세율 조정 재료 — 판정은 카드 EPS 파일 행으로, 시점은 카드 공시 기준(cap)
    _eo_rows = _eo.eps_rows_for(t) if core and _eo.has(t) else None
    _eo_on = _eo_rows is not None
    _eo_cap = _approved().get(str(cik).zfill(10)) if _eo_on else None

    def core_earnings(d):
        """그날 공개돼 있던 최근 4분기 본업 이익 = 영업이익 × (1 − 법인세/세전이익), 같은 분기끼리."""
        parts = {n: [e for e in series.get(n, []) if e["available"] <= d] for n in ("opinc", "tax", "pretax")}
        if not all(parts.values()):
            return None
        common = set.intersection(*({e["end"] for e in v} for v in parts.values()))
        if not common:
            return None
        end = max(common)
        _nw = [newest_row(v) for v in parts.values()]
        if None in _nw:
            return None
        lead = max(x["end"] for x in _nw)
        if (date.fromisoformat(lead) - date.fromisoformat(end)).days > MAX_PAIR_LAG_DAYS:
            return None
        _at = [newest_row([e for e in parts[n] if e["end"] == end]) for n in ("opinc", "tax", "pretax")]
        if None in _at:
            return None
        o, tx, pt = (x["val"] for x in _at)
        # 일회성 손익(v2/eps_oneoff.json, 안건 E54)이 그 결산일에 적용됐으면 세율만 조정하고(영업이익은 그대로 — 설계 §12),
        # 양수 검사는 조정 뒤 세전이익으로 한다. 적용된 항목이 없으면 아래 지금 코드 그대로.
        _ea = None
        if _eo_on:
            _tq = [_eo.ttm_quarters(_a8_q.get(n, []), end) for n in ("tax", "pretax")]
            _ea = _eo.tax_adjust(t, _eo_rows, end, _eo_tag, "a8", _eo_cap,
                                 tax_quarters=set(_tq[0]) & set(_tq[1]) if None not in _tq else set())
        if _ea:
            r = _eo.a8_rate(o, pt, tx, oneoff_in_ttm(t, end, "pretax", d), oneoff_in_ttm(t, end, "tax", d),
                            rate_addback(t, cik, end, d), _ea)
            if r is None:
                return None
            if core_tickers().get(t, {}).get("statutory_fallback") and not 0.0 <= r <= 0.40:
                r = 0.21
            ni = net_interest_at(nis, end, d) if nis else None
            base = o + ni if ni is not None else o
            return base * (1 - r) if base > 0 else None
        if pt <= 0 or o <= 0:
            return None
        # 회사가 금액을 밝힌 일회성 법인세 항목(v2/tax_oneoff.json)은 현금흐름 세율(build_dcf.effective_tax)과 같게 세율에서 뺀다
        # (2026-10-04 — 같은 카드 안에서 본업 PER은 법정 21%, 현금흐름은 일회성을 뺀 16.1%로 세율이 갈렸다, GEV)
        # 회사가 금액과 비과세임을 밝힌 일회성 세전 이익(pretax 필드, GEV Prolec 재평가 $3,992M)은 분모에서도 뺀다 — 안 빼면 세금이 안 붙는
        # 이익이 분모만 키워 세율이 어느 분기에도 없는 16.1%가 됐다(Fable, 2026-10-04 사용자 결정). 본업 이익(opinc)에서는 원래 빠져 있다.
        pt_rate = pt - oneoff_in_ttm(t, end, "pretax", d) + rate_addback(t, cik, end, d)   # 반복적 비공제 항목(ABBV 조건부 대가, 2026-10-05)
        r = (tx - oneoff_in_ttm(t, end, "tax", d)) / pt_rate if pt_rate > 0 else tx / pt
        # 종목 예외(core_earnings.json "statutory_fallback"): 세율이 0~40% 밖이면 법정 21%. GEV는 세금 평가충당금 환입
        # $2.9B로 최근 4분기 세율이 −20.8%라 본업 이익이 영업이익보다 컸다(Codex·Fable, 2026-10-01). 위에서 그 환입을 빼면
        # 비과세 Prolec 이익까지 빼 범위 안(32.5%)이라 지금은 걸리지 않는다. 전 종목 적용은 ABBV·PANW 점수를 바꿔 100장 뒤 안건으로 미룬다.
        if core_tickers().get(t, {}).get("statutory_fallback") and not 0.0 <= r <= 0.40:
            r = 0.21
        # A8: 순이자를 더한다. 결측(태그는 쓰는데 그 분기 값 없음, 태그 없음)이면 영업이익만(CRM·GEV — 2026-10-04 사용자 결정)
        ni = net_interest_at(nis, end, d) if nis else None
        base = o + ni if ni is not None else o
        if base <= 0:
            return None
        return base * (1 - r)

    out = {"ticker": t, "window": [daily[0][0], daily[-1][0]], "multiples": {},
           "perBasis": "core" if core else "diluted"}
    # 카드별 전환·교환 증권 표(E44 §3) — 표에 있는 종목만, 연구 모드는 끔
    _sc_on = _sc.has(t)
    _px_by = {b[0]: b[4] for b in daily}          # 일봉 [날짜, 시가, 고가, 저가, 종가, …] — 아래 배수 계산과 같은 종가
    _px_at = lambda d: _px_by.get(d, daily[-1][4])
    defs = {
        "PER": (lambda d, px: (mcap(d, px) / core_earnings(d)) if mcap(d, px) and core_earnings(d) else None) if core
        else (lambda d, px: px * fx.rate(t, d) / as_of(eps, d) if eps and as_of(eps, d) and as_of(eps, d) > 0 else None),
        "PSR": lambda d, px: mcap(d, px) / as_of(series.get("revenue", []), d)
        if mcap(d, px) and as_of(series.get("revenue", []), d) else None,
        "PBR": lambda d, px: mcap(d, px) / equity_ce(d, px)
        if mcap(d, px) and equity_ce(d, px) else None,
        "PCR": lambda d, px: (mcap(d, px) / fcf(d)) if mcap(d, px) and fcf(d) and fcf(d) > 0 else None,
        "EV/EBITDA": lambda d, px: (ev(d, px) / ebitda(d))
        if ev(d, px) and ebitda(d) and ebitda(d) > 0 else None,
    }

    def mcap(d, px):
        # 재무가 현지 통화(TSM 대만달러)면 달러 가격을 그날 환율로 바꿔 같은 통화끼리 나눈다(v2/fx.py).
        sh = as_of(series.get("shares", []), d)
        if sh and _sc_on:
            # 카드별 전환·교환 증권 표(v2/share_claims.json, E44 §3) — 보통주로 보는 증권의 주식 수를 그날 값으로
            e = as_of_entry(series["shares"], d)
            wq = e.get("wa_q")
            sh = _sc.adjusted_shares(t, d, px, sh, e["end"], base_is_wa=bool(wq), wa_start=wq[0] if wq else None,
                                     wa_end=wq[1] if wq else None)
        return px * fx.rate(t, d) * sh if sh else None

    def _claims(d, px):
        """그날 엔진 관측 결산일에 맞춘 표의 짝 금액(E44 §3.3)."""
        obs = {}
        for k in ("equity", "nci", "preferred", "debt"):
            e = as_of_entry(series.get(k, []), d) if series.get(k) else None
            obs[k] = e["end"] if e else None
        return _sc.claims(t, d, px, obs)

    def equity_ce(d, px=None):
        """PBR 분모 — 보통주 자본(common_equity) + 표 증권의 ce_add·pref_in_p(보통주로 보는 우선주는 P에서 되돌림)."""
        e = as_of_entry(series.get("equity", []), d) if series.get("equity") else None
        v = e["val"] if e else None
        if v is None or not _sc_on:
            return v
        c = _claims(d, px if px is not None else _px_at(d))
        if c["pref_in_p"] > (e.get("pref") or 0) + 1:
            # 표가 P에서 되돌리는 금액이 그날 P에 실제로 실린 우선주보다 크면 이중 되돌림(GOOGL 두 시리즈 합 등, §3.1)
            raise _sc.ClaimHold(f"{t} {e['end']}: 표 pref_in_p {c['pref_in_p']:,.0f} > 엔진 P {e.get('pref') or 0:,.0f}")
        return v + _sc.ce_extra(c)

    _fin_lease = finance_lease_series(cik) if cik in LEASE_INCLUDES_FINANCE else []

    def ev(d, px):
        m = mcap(d, px)
        if not m:
            return None
        cash = (as_of(series.get("cash", []), d) or 0) + (as_of(series.get("sti", []), d) or 0)
        # 운용리스는 EV에 더하지 않는다 — EBITDA(영업이익)가 임차료를 이미 뺐으므로 부채로 또 더하면 이중(B16 — DCF와 같은 기준, 안건 E61
        # 2026-11-05 사용자 결정). IFRS 16 회사(TSM·SKHY)는 리스 비용이 영업이익 밖이라 리스부채를 빚으로 둔다.
        lease = as_of(series.get("lease", []), d) or 0
        if t in IFRS_LEASE:
            lease_ev = lease
        elif cik in LEASE_INCLUDES_FINANCE:
            lease_ev = min(lease, as_of(_fin_lease, d) or 0)   # 리스 태그 안 금융리스분만(빚)
        else:
            lease_ev = 0
        debt = (as_of(series.get("debt", []), d) or 0) + lease_ev
        extra = (as_of(series.get("nci", []), d) or 0) + (as_of(series.get("preferred", []), d) or 0)
        if _sc_on:
            # 보통주로 본 증권은 EV 청구권에서 뺀다(주식 수에 더했으므로 — 한 증권은 한쪽으로만, E44 §1)
            c = _claims(d, px)
            for _n, _f in (("debt", "principal_in_debt"), ("nci", "nci_remove"), ("preferred", "pref_ev")):
                if c[_f] > (as_of(series.get(_n, []), d) or 0) + 1:
                    # 표가 빼는 금액이 그날 엔진 잔액보다 크다 — 짝 금액 배분 오류(Codex r2)
                    raise _sc.ClaimHold(f"{t} {d}: 표 {_f} {c[_f]:,.0f} > 엔진 {_n} {as_of(series.get(_n, []), d) or 0:,.0f}")
            debt -= c["principal_in_debt"]
            extra -= c["nci_remove"] + c["pref_ev"]
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
        na, nb = newest_row(ea), newest_row(eb)    # 목록 마지막이 아니라 결산일이 가장 늦은 행(E63)
        if na is None or nb is None:
            return None, None
        if na["end"] != nb["end"]:
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
            lead = max(na["end"], nb["end"])
            if (date.fromisoformat(lead) - date.fromisoformat(end)).days > MAX_PAIR_LAG_DAYS:
                return None, None
            na = newest_row([x for x in ea if x["end"] == end])
            nb = newest_row([x for x in eb if x["end"] == end])
            if na is None or nb is None:
                return None, None
        return na["val"], nb["val"]

    def fcf(d):
        o, c = paired("ocf", "capex", d)
        return (o - c) if (o is not None and c is not None) else None

    # 오늘 배수가 없을 때 적자(분모 0 이하)인지 가르는 분모. 본업 PER은 core_earnings가
    # 적자면 None을 돌려 가를 수 없어 넣지 않는다.
    DENOMS = {"PCR": fcf, "EV/EBITDA": ebitda,
              "PSR": lambda d: as_of(series.get("revenue", []), d),
              "PBR": lambda d: equity_ce(d)}
    if not core:
        DENOMS["PER"] = lambda d: as_of(eps, d) if eps else None

    # A3(2026-10-01 사용자 결정, 100장 뒤 적용 — 2026-10-03): 최근 4분기 GAAP 순이익률이 2% 미만(손익분기 근처 흑자)이거나
    # 순이익 ≤ 0(적자)이면 "PER 해당 없음" 종목. PER을 자기 이력·동종업 점수에서 빼고, PER 기준 적정주가 밴드는 만들지 않는다.
    def _net_margin_now():
        """지배주주 귀속 순이익(NetIncomeLoss, 우선주 배당 전) TTM ÷ 매출 TTM. 태그가 멈췄으면(매출 TTM 결산일보다 120일 넘게 뒤처짐)
        다음 태그로 — AVGO는 NetIncomeLoss TTM이 2019에 멈춰 2019 순이익 ÷ 2026 매출이 될 뻔했다(Fable, A3)."""
        day = daily[-1][0]
        rv_s = [e for e in series.get("revenue", []) if e["available"] <= day]
        if not rv_s:
            return None
        rv = newest_row(rv_s)    # 목록 마지막이 아니라 결산일이 가장 늦은 행(E63)
        if rv is None:
            return None
        rv_end = date.fromisoformat(rv["end"])
        for tags in (["NetIncomeLoss"], ["ProfitLoss"], ["NetIncomeLossAvailableToCommonStockholdersBasic"]):   # ProfitLoss는 비지배 포함
            _, nr = pick_tag(cik, tags)
            ni_s = [e for e in (ttm_series(quarterly_flow(nr, t)) if nr else []) if e["available"] <= day]
            ni = newest_row(ni_s) if ni_s else None
            if ni and abs((rv_end - date.fromisoformat(ni["end"])).days) <= 120 and rv["val"]:
                _dq = set()   # 중단영업 금액을 뺀 분기 — 그 분기의 E54 중단영업 항목은 다시 빼지 않는다(Codex r2)
                _dc = _disc_ni(ni["end"], day, consolidated=tags == ["ProfitLoss"], used=_dq)
                _disc_ni_hit[0] = bool(_dc)
                _adj = _eo_ni(ni["end"], consolidated=tags == ["ProfitLoss"], skip_disc=_dq)
                _eo_ni_hit[0] = bool(_adj)
                return (ni["val"] + _adj + _dc) / rv["val"]
        return None

    _eo_ni_hit = [False]
    _disc_ni_hit = [False]

    def _disc_ni(end, day, consolidated=False, used=None):
        """E62 기준(계속영업)으로 맞출 중단영업 손익 금액(손실 +, 이익 −) — A3 순이익률도 PER EPS처럼 계속영업으로 본다(2026-11-05 사용자
        결정: GPN은 Issuer 매각 쪽 중단영업 손실로 GAAP 순이익률 −9.1%인데 PER은 계속영업 EPS라 기준이 갈렸다). EPS 행은 PER 경로와 같은
        목록(_a3_rows·_a3_cap, ttm_eps 있음)에서 그 결산일·기준일까지 공개된 마지막 행. 그 TTM 네 분기의 E62 판정이 모두 'removed'(총 EPS에서
        뺐다)·'already'(파일이 이미 계속영업)·'none'이고 하나라도 중단영업이 있을 때만, 순이익과 같은 기준의 금액 태그(지배 순이익이면 지배 몫
        태그, ProfitLoss면 연결 태그 — 비지배 몫 중단영업이 0이 아니면 서로 대신 쓰지 않는다) 그 결산일 TTM을 뺀다. 'unknown' 분기·태그 없음은 0 + 경고(Codex r1)."""
        if _a3_rows is None or ASOF_REF is not None or not _disc_facts(t):
            return 0.0
        r = sorted((x for x in _a3_rows if x.get("quarter_end") == end and x.get("ttm_eps") is not None
                    and x["available_date"] <= day and (not _a3_cap or x["available_date"] <= _a3_cap)), key=lambda x: x["available_date"])
        if not r:   # 순이익 결산일이 PER EPS 행(cap)보다 뒤 — COF(Fable r1)
            print(f"  ⚠ A3 계속영업: 순이익 결산일 {end}의 PER EPS 행이 없다 — 중단영업 조정 미적용")
            return 0.0
        row = r[-1]   # as_of_entry처럼 공개일 동률이면 뒤 행
        qr = _ttm_quarter_rows(_a3_rows, end, row["available_date"])
        if qr is None:
            print(f"  ⚠ A3 계속영업: {end}로 끝나는 네 분기 EPS 행이 없다 — 중단영업 조정 미적용")
            return 0.0
        u = _disc_upto(t, row["available_date"])
        st = [_quarter_status(t, _a3_rows, q, u)[1] for q in qr]
        if all(x == "none" for x in st):
            return 0.0
        def _q_at(tags_):
            """{분기 결산일: 3개월 금액} — 중단영업은 있는 분기에만 공시돼 TTM 창이 안 생기는 회사가 많아(APD·SNPS·T) 분기별로 더한다(Fable r1)."""
            _, dr = pick_tag(cik, tags_)
            out_ = {}
            for e in (quarterly_flow(dr, t) if dr else []):
                if e["filed"] <= day:
                    out_.setdefault(e["end"], e["val"])
            return out_
        tot = ["IncomeLossFromDiscontinuedOperationsNetOfTax", "DiscontinuedOperationIncomeLossFromDiscontinuedOperationNetOfTax"]
        par = ["IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToReportingEntity"]
        ends = [q["quarter_end"] for q, x in zip(qr, st) if x != "none"]   # 'none' 분기는 중단영업 0
        # 연결·지배 몫은 비지배 몫 중단영업 태그가 그 분기들에 없을 때만 서로 대신한다(APD 등은 연결 태그만 쓴다 — 11-05 전수 비교)
        # 분기로 환산되지 않는 연간·누계 공시만 있어도 그 분기를 덮는 비지배 값이 0이 아니면 대체 금지(Codex r2)
        _, nr_ = pick_tag(cik, ["IncomeLossFromDiscontinuedOperationsNetOfTaxAttributableToNoncontrollingInterest"])
        nci = any(e.get("val") and "start" in e and e.get("filed", "") <= day and e["start"] < e_ <= e["end"] for e in (nr_ or []) for e_ in ends)
        order = (tot + ([] if nci else par)) if consolidated else (par + ([] if nci else tot))
        tg, got = order[0], None
        for tg in order:
            qv = _q_at([tg])
            if all(e_ in qv for e_ in ends):
                got = sum(qv[e_] for e_ in ends)
                break
        if "unknown" in st or got is None:
            print(f"  ⚠ A3 계속영업: {end} 분기 판정 {st}, 분기 금액 태그 {'있음' if got is not None else '없음'} — 중단영업 조정 미적용")
            return 0.0
        if used is not None:
            used.update(ends)
        return -got

    def _eo_ni(end, consolidated=False, skip_disc=()):
        """일회성 손익 장치(E54)가 그 결산일 PER EPS에서 뺀 항목의 세후 지배주주 몫(손실 +, 이익 −) — A3 순이익률도 같은 기준으로
        본다(2026-11-05 사용자 결정: 손상으로 적자가 된 카드가 장치로 EPS를 고쳐도 GAAP 순이익률 때문에 PER이 빠지던 문제, FISV·IVZ).
        장치 판정(judge)이 그 결산일에 적용한 항목만, 세금은 같은 cap의 item_tax. EPS 행·cap은 PER 경로가 읽은 것(_a3_rows·_a3_cap)과
        같아야 한다 — 비교군 갱신은 EPS_HISTORY가 다른 파일이다(Codex A3 r1). 순이익이 비지배 포함(ProfitLoss)이면 항목도 연결 전액으로
        더한다(parent_share 미적용 — 지배 몫만 더하면 기준이 섞인다). EPS 파일이 없거나 연구 모드·장치 없는 종목은 0."""
        if not _eo.has(t) or _a3_rows is None:
            return 0.0
        j = _eo.judge(t, _a3_rows, end, _a3_cap)
        if not j:
            return 0.0
        cap_ = _eo._cap(t, _a3_cap)
        return sum((it["adj_pretax"] - _eo.item_tax(it, cap_)) * (1 if consolidated else it.get("parent_share", 1)) for it in j["applied"]
                   if not (it.get("discontinued") and it["quarter_end"] in skip_disc))
    per_margin = _net_margin_now()
    _eo_ni_used = _eo_ni_hit[0]
    per_na = per_margin is not None and per_margin < PER_NA_MARGIN
    out["perNA"] = {"netMargin": round(per_margin, 4), "rule": ("최근 4분기 순이익률(" + "·".join(x for x, on in (("일회성 장치 E54 항목", _eo_ni_used), ("중단영업", _disc_ni_hit[0])) if on) + "을 뺀 값) < 2% 또는 적자"
                                                          if (_eo_ni_used or _disc_ni_hit[0]) else "최근 4분기 GAAP 순이익률 < 2% 또는 적자")} if per_na else None
    if per_na:
        print(f"  PER 해당 없음: 최근 4분기 순이익률 {per_margin:.2%} (< 2%) — 자기 이력·동종업 점수에서 PER을 뺀다(A3)")
    elif per_margin is None and eps and (as_of(eps, daily[-1][0]) or 0) <= 0 and as_of(eps, daily[-1][0]) is not None:
        # 순이익률을 못 구해도 최근 4분기 EPS가 0 이하(적자)면 해당 — 양수 PER 이력이 없어 아래 반복이 PER을 건너뛰어도 적용되게
        # 배수 계산 전에 정한다(Codex 2차).
        per_na = True
        out["perNA"] = {"netMargin": None, "rule": "최근 4분기 EPS ≤ 0(적자) — 순이익률 계산 불가"}
        print("  PER 해당 없음: 순이익률은 못 구했지만 최근 4분기 EPS ≤ 0(적자) — 자기 이력·동종업 점수에서 PER을 뺀다(A3)")

    _drop = {x.strip() for x in args.drop.split(",") if x.strip()}
    for label, fn in defs.items():
        if label in _drop:
            print(f"  {label}: 사전 등록으로 제외")
            continue
        pts = []
        for b in daily:
            try:
                v = fn(b[0], b[4])
            except _sc.ClaimHold:
                raise                       # 표 짝 금액이 그 결산일에 없다 — 그 종목 카드만 보류(E44 §3.3)
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
        if label == "PER" and per_na:
            m_ = out["multiples"]["PER"]
            m_["score"], m_["currentNote"] = None, "per_na"
        if label == "PBR" and stale_note == "negative":
            # 자본 음수(자사주 매입 누적 등)면 PBR은 비싸다는 뜻이 아니라 잴 수 없다 — 해당 없음, 자기 이력·동종업 평균에서 뺀다
            # (C11, 2026-10-04 사용자 결정 H). 자본이 한 번도 양수가 아니던 종목(MCD)은 원래 "계산 불가"로 빠졌는데,
            # 한때 양수였던 종목(BKNG·ABBV)만 0점이던 어긋남을 맞춘다. PCR·EV/EBITDA의 음수는 그대로 0점.
            m_ = out["multiples"]["PBR"]
            m_["score"], m_["currentNote"] = None, "pbr_na"
        if label == "PER" and not stale_note and not per_na:
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
        if label == "PER" and per_na:
            print(f"  {label}: 해당 없음(A3 — 점수·평균에서 뺌)")
            continue
        if stale_note:
            print(f"  {label}: 오늘 값 없음 ({('자본 음수 → 해당 없음(C11)' if label == 'PBR' else '분모 0 이하 → 0점') if stale_note == 'negative' else '분모를 못 구함 → 평균에서 뺌'})")
            continue
        print(f"  {label}: 현재 {m['current']}  (최저 {m['min']} · 중앙 {m['median']} · 최고 {m['max']})"
              f"  하위 {m['percentile']}%  → 점수 {m['score']}  [{m['days']}일]")

    if args.json:
        json.dump(out, open(args.json, "w"), ensure_ascii=False, indent=1)
        print("저장:", args.json)


if __name__ == "__main__":
    main()
