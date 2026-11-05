BUILD = {'dim_facts': [('us-gaap:CashAndCashEquivalentsAtCarryingValue', 'dei:LegalEntityAxis', 'ben:FranklinResourcesInc.Member', 'CashCompanyBen'),
                       ('us-gaap:TemporaryEquityCarryingAmountIncludingPortionAttributableToNoncontrollingInterests', 'us-gaap:StatementEquityComponentsAxis', 'ben:MinorityInterestsMember', 'TemporaryEquityMinorityInterestsBen')]}
# BEN(프랭클린 템플턴, 2026-08-17 Franklin Resources에서 사명 변경) v2 카드 설정 — 자동 카드(AUTO). 회계연도 9월 30일. 자산운용 — 뮤추얼펀드·ETF·대체투자(Western Asset·Putnam·Clarion), 단일 보고 부문.
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-07-31), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 장 전 08시 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/BEN.md. 비교군 asset_managers(2026-10-25 등록). FY2026 10-K·4분기 실적은 미제출(2026-11-04).
# 엔진 입력(2026-11-04): 연결 재무제표에 CIP(연결 투자상품, 자산 $16,856M·CLO 차입 $13,334M)가 섞여 회사 몫만 쓴다 — 현금 $2,670.3M(dei:LegalEntityAxis 차원, BUILD dim_facts — 축 없는 현금 태그는 2021-12 멈춤, 합계 태그 $3,760.9M에는 CIP 현금 $1,090.6M),
# 차입 $2,401.9M(축 없는 LongTermDebt = 회사 차입 전부), 운용리스 $974.6M, 비지배 = 비상환 $1,181.7M(CIP 몫 $757.4M 포함 — 빼는 장치가 없어 TROW처럼 둔다, 주당 약 $1.49 보수적) + 상환가능 자회사 몫 $1,137.3M(차원, EV_TAGS_BY_CIK).
# 감가상각 = 감가상각 + 무형자산 상각(DDA_SPLIT_BY_CIK, TTM $347.0M — 합계처럼 보이는 태그가 상각을 뺀 값, Codex r1).
# 회사 보유 투자자산(약 $2.7B, CIP 지분 $1.16B 포함)은 넣지 않았다(TROW와 같음). 설비투자는 FY2025 $154.5M — FY26 1·2분기 10-Q가 사무실 매각대금을 뺀 순액 줄만 내 태그가 없다(9개월 순 $15.0M).
# 일회성(E54 시험, Codex r1 뒤 다시 계산): 최근 4분기 무형자산 손상 세전 $235.2M(Q4 FY25 $202.2M·Q3 FY26 $33.0M)·Western Asset SEC 합의금 $100M(공제 안 됨). 2계급 몫(6.5%) 빼고 주당 반영 — 합의금만 빼면 자기 25.4, 손상까지 빼면 29.2~29.5(세율 30~21%)
# 로 30 아래 → 자기 −1 유지(PER 22.0→16.3~16.6, EV/EBITDA 15.54→12.26). 이력 안 손상까지 같이 빼면 PER 자기 점수가 거의 그대로(약 28, Fable r1). 동종업(80.3, +1)·현금흐름(−2, 기본이 $21.6를 넘어야 바뀜)도 같은 쪽 — 정식 판정.
CIK = '0000038777'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-09-30', '2024-09-30'), 'FY2025'
VOTES, VERDICT = (-1, 1, -2), '적정~고평가'
CO = 'Franklin Templeton'
S_ = 'https://www.sec.gov/Archives/edgar/data/38777/'
SEC = S_
TENQ = S_ + '000003877726000217/ben-20260630.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000003877726000215/exhibit991q3fy26.htm', 'q2': S_ + '000003877726000100/exhibit991q2fy26.htm', 'q1': S_ + '000003877726000032/exhibit991q1fy26.htm', 'q4': S_ + '000003877725000234/exhibit991q4fy25.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="benFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(손상·합의금 포함, 10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('연결 재무제표에 회사가 운용하는 펀드(CIP — 자산 $16.9B, CLO 차입 $13.3B)가 섞여 있어 현금·차입·비지배지분은 회사 몫만 썼다. 다만 비지배지분에는 CIP 외부 투자자 몫($757M, 주당 약 $1.49)이 남아 있고 회사가 직접 들고 있는 투자자산(약 $2.7B, CIP 지분 $1.16B 별도)은 넣지 않아 내재가치가 낮게 잡힌다 — 둘을 고쳐도 현금흐름 칸은 그대로다. '
              '최근 4분기 이익에 무형자산 손상(세전 $235M)과 Western Asset SEC 합의금($100M)이 들어 있다 — 둘을 빼도 자기 이력 점수가 30 아래(약 29)에 머물러 판정은 같다. 회계 4분기(7~9월) 실적과 연간 보고서는 예년대로면 11월 초에 나온다. 비교 종목은 S&P500 자산운용·수탁은행 12곳 중 BEN을 뺀 11곳이다.')
PH = ['BLK', 'TROW', 'IVZ', 'AMP', 'NTRS', 'STT']
PEER_FILE = 'peer_universe/asset_managers.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '자산운용 6곳 PER 비교 (점수는 S&P500 자산운용·수탁은행 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 자산운용·수탁은행 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 자산운용·수탁은행 대비 배수 순위 (v2/peer_universe/asset_managers.json)'
PEER_TIP = ('S&P500 자산운용·수탁은행 12곳 중 BEN을 뺀 11곳과 배수 순위를 매긴 값이다.',
            '전통 운용사·대체투자사·수탁은행이 섞여 있다. 차트에는 6곳만 보인다.')
# 매출(Q3 FY26 10-Q, srt:ProductOrServiceAxis) — 1,866.2 + 404.5 + 74.3 + 13.4 = 2,358.4.
SEG = [('운용보수(성과보수 포함)', 1866.2, '#1d4f91'), ('판매·유통 수수료', 404.5, '#5b8bd0'), ('주주 서비스', 74.3, '#a9c4ea'), ('기타', 13.4, '#8a96a3')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 항목별(Q3 FY26)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(08시 동부) → 같은 날.
NEWS_RANGE = '2025.11 ~ 2026.07'
NEWS = [
    ('green', '2026년 7월 31일 장 전 — Q3 FY26 실적·사명 변경', '2026-07-31',
     '매출 $2.36B(+14.3%) · 순이익 $172M · 희석 EPS $0.31(1년 전 $0.15, SEC 합의금 $100M·손상 $33M 포함) · 조정 EPS $0.72 · 사명 Franklin Templeton, Inc.로 변경 — 당일 주가 +2.1%', 'q3', 'Franklin Templeton 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 28일 장 전 — Q2 FY26 실적', '2026-04-28',
     '매출 $2.29B(+8.7%) · 순이익 $268M · 희석 EPS $0.49(1년 전 $0.26) · 조정 EPS $0.71 — 당일 주가 +6.9%', 'q2', 'Franklin Templeton 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 30일 장 전 — Q1 FY26 실적', '2026-01-30',
     '매출 $2.33B(+3.4%) · 순이익 $256M · 희석 EPS $0.46(1년 전 $0.29) · 조정 EPS $0.70 — 당일 주가 +2.9%', 'q1', 'Franklin Templeton 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 7일 장 전 — Q4 FY25 실적', '2025-11-07',
     '매출 $2.34B(+6.0%) · 순이익 $118M · 희석 EPS $0.21(1년 전 −$0.19, Western Asset 운용계약 손상 $200M 포함) · 조정 EPS $0.67 — 당일 주가 −4.4%', 'q4', 'Franklin Templeton 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 13, 'nt': 11, 'mean': 35.73, 'median': 35, 'low': 26, 'high': 40, 'sb': 4, 'b': 0, 'h': 7, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-11-04'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 FY26 1,866.2/404.5/74.3/13.4(2026-11-04) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"us-gaap:InvestmentAdvisoryManagementAndAdministrativeServiceMember": ["운용보수(성과보수 포함)", "#1d4f91"], "ben:SalesAndDistributionFeesMember": ["판매·유통 수수료", "#5b8bd0"], "us-gaap:ShareholderServiceMember": ["주주 서비스", "#a9c4ea"], "us-gaap:ServiceOtherMember": ["기타", "#8a96a3"]},
 "ignore": []
}
