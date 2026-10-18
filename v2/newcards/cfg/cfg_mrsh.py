# MRSH(마시, 옛 Marsh McLennan) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 127(시총 125위). 보험·재보험 중개(Marsh Risk·Guy Carpenter), 컨설팅(Mercer·Oliver Wyman).
# 2026-01-14 브랜드를 Marsh McLennan → Marsh로 바꾸고 티커가 MMC → MRSH(법인명 Marsh & McLennan Companies는 그대로, 10-Q).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-15), 실적 보도자료(Q3 2025~Q3 2026, 8-K 2.02항 — 모두 장중 접수), 8-K(Marsh Risk CEO 승계 2026-03-10, COO·CFO 임명 2026-04-14), StockAnalysis.
# 보험사가 아니라 수수료형 중개·컨설팅이라 일반 경로(현금흐름 모델). 동종업 비교군: S&P500 중개사가 5곳뿐이라(MIN_PEERS 8 미만) 중개사 + 결제·거래소·금융 데이터
# 24곳(peer_universe/brokers_fees.json, build_peer_score.TICKER_UNIVERSE — 2026-10-18 사용자 결정).
# 엔진 입력(2026-10-18): 차입금 = DebtCurrent + LongTermDebtNoncurrent($1,644M + $18,889M — 기본 합 $22,133M은 1년 안 만기·기업어음이 겹쳤다, DEBT_TOTAL_TAG),
# 단기투자 줄 없음(2012년 값이 남아 있었다, EV_TAGS_BY_CIK sti []). 감가상각 = 고정자산·소프트웨어(Depreciation → DepreciationDepletionAndAmortization 튜플,
# 2021~2023 연간에 무형자산 상각을 합친 값이 섞여 Depreciation 앞) + 무형자산 상각(AmortizationOfIntangibleAssets) — 합산 태그만 쓰면 무형자산 상각이 빠지고
# EV/EBITDA가 252일이었다(DDA_PARTS_BY_CIK + EXCLUDE_TAGS). 수탁 현금($12.3B)은 수탁 부채와 맞물린 통과 잔액이라 현금에 넣지 않는다(엔진 기본) —
# 그 이자(분기 약 $100M)는 매출(Risk and Insurance Services) 안이라 영업이익에 있다. 4분기 EPS 역산 = 보도자료(2021~2025).
# 2026년 영업비용에 Greensill 관련 호주 소송 비용(Q1 $425M, Q3 $144M, 보험금 차감 뒤 — 6월 합의)이 있다 — 최근 4분기 이익률·낙관 시나리오를 누른다(판정 규칙상 손대지 않음, Fable).
CIK = '0000062709'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Marsh'
S_ = 'https://www.sec.gov/Archives/edgar/data/62709/'
SEC = S_
TENQ = S_ + '000006270926000258/mrsh-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000006270926000256/mmc3q2026ex991newsrelease.htm', 'q2': S_ + '000006270926000193/mmc2q2026ex991newsrelease.htm',
      'q1': S_ + '000006270926000096/mmc1q2026ex991newsrelease.htm', 'q4': S_ + '000006270926000014/mmc4q2025ex991newsrelease.htm',
      'q3_25': S_ + '000006270925000123/mmc3q2025ex991newsrelease.htm'}
LINKS = {'coo': S_ + '000095010326005674/dp245126_8k.htm', 'risk_ceo': S_ + '000006270926000071/asouthappointment03102026.htm'}
FAIRBAND_TITLE = 'id="mrshFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 30)
ACT_REASON = ''
NONOP_WHAT = '장기투자'
HEALTH_EXTRA = '유동비율·부채비율에는 고객 수탁 자금(현금과 부채에 같은 금액)이 들어 있어 실제 지급능력보다 나쁘게 나온다.'   # 고정 문장(Fable 권장)
PH = ['AON', 'AJG', 'BRO', 'WTW', 'SPGI', 'MCO']
PEER_FILE = 'peer_universe/brokers_fees.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '보험 중개·금융 데이터 6곳 PER 비교 (점수는 중개사 + 결제·거래소·데이터 기준)', 'pbr': '보험 중개·금융 데이터 PBR 비교', 'psr': '보험 중개·금융 데이터 PSR 비교',
                'pcr': '보험 중개·금융 데이터 PCR(FCF) 비교', 'evebitda': '보험 중개·금융 데이터 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 보험 중개사와 결제·거래소·금융 데이터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 보험 중개 + 결제·거래소·금융 데이터 대비 배수 순위 (v2/peer_universe/brokers_fees.json)'
PEER_TIP = ('S&P500 보험 중개사(MRSH 제외 4곳)와 결제·거래소·금융 데이터 회사(수수료로 버는 자산 경량 서비스)와 배수 순위를 매긴 값이다 — 중개사만으로는 비교 표본(8곳)이 모자란다.',
            '카드 네트워크·결제 처리·거래소·신용평가·지수 회사가 섞여 있어 성장·마진 구조가 다르다. PER이 낮은 결제 회사들이 점수를 끌어올릴 수 있어, 중개사끼리만 견주면 결과가 다를 수 있다 — 차트의 중개사 4곳과 직접 비교할 것(차트에는 중개사 4곳과 신용평가 2곳만 보인다).')
# 매출(Q3 2026 10-Q 부문 표 — 표준 매출 태그는 수탁 자금 이자를 사업에 나눠 담는다) — 보험 중개(Risk) 3,796 + 재보험 404 + 인력·투자 1,672 + 경영 컨설팅 1,013
# = 6,885(부문 합), 본사·제거 −22 = 6,863(연결 매출). 수탁 이자를 뺀 값(3,726·374)은 회사 고유 매출 태그.
SEG = [('보험 중개(Marsh Risk)', 3796, '#002c77'), ('재보험(Guy Carpenter)', 404, '#009de0'), ('인력·투자(Mercer)', 1672, '#00a3a1'), ('경영 컨설팅(Oliver Wyman)', 1013, '#6e7ab8')]
SEG_ADJ = -22
SEG_SUM_LABEL, SEG_ADJ_LABEL = '사업 합', '본사·부문 간 제거'
SEG_TITLE = '매출 구성 — 사업별'
# 손 뉴스: 최신 실적(Q3 2026, 10/15)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤 손 항목은 없다. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K는 모두 10~12시 접수(장중) → 같은 날. COO·CFO 8-K 4/14 12:22 → 4/14, Marsh Risk CEO 8-K 3/10 12:34 → 3/10.
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('green', '2026년 7월 21일 — Q2 2026 실적', '2026-07-21',
     '매출 $7.40B(+6%) · 희석 EPS $2.63(1년 전 $2.45)', 'q2', 'Marsh 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 16일 — Q1 2026 실적', '2026-04-16',
     '매출 $7.60B(+8%) · 희석 EPS $2.36(1년 전 $2.79) · 영업이익에 Greensill 관련 호주 소송 비용 $425M 포함(6월 합의, 3분기에도 $144M)', 'q1', 'Marsh 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 14일 — COO·CFO 임명', '2026-04-14',
     'Mark McGivney(CFO)가 4월 15일부터 수석부사장·COO 겸 CFO', 'coo', 'Marsh 공시 (SEC 8-K)'),
    ('neutral', '2026년 3월 10일 — Marsh Risk CEO 승계', '2026-03-10',
     'Oliver Wyman CEO Nick Studer가 4월 1일부터 Marsh Risk 사장·CEO(Martin South 후임)', 'risk_ceo', 'Marsh 공시 (SEC 8-K)'),
    ('green', '2026년 1월 29일 — Q4 2025 실적', '2026-01-29',
     '매출 $6.60B(+9%) · 희석 EPS $1.68(1년 전 $1.59) · 2025년 EPS $8.43', 'q4', 'Marsh 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 16일 — Q3 2025 실적', '2025-10-16',
     '매출 $6.35B(+11%) · 희석 EPS $1.51(1년 전 $1.51)', 'q3_25', 'Marsh McLennan 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Hold', 'n': 23, 'nt': 16, 'mean': 202.5, 'median': 201, 'low': 180, 'high': 234, 'sb': 5, 'b': 2, 'h': 15, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-18'


# ── 자동 카드 — 부문 지도: 사업(SubsegmentsAxis)마다 부문 축(StatementBusinessSegmentsAxis — 보험·재보험은 RIS, 나머지는 Consulting)이 달라 seg_map_propose는 2/4만 맞췄다.
# 부문 축은 free_axes로 무시(EMR 방식), 인력·투자 세부 3항목은 ignore. 원문 대조: 표준 매출 태그 Q3 2026 3,796/404/1,672/1,013(합 6,885), 1년 전은 아래 시험(2026-10-18) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:SubsegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "free_axes": ["us-gaap:StatementBusinessSegmentsAxis"],
 "members": {
  "mrsh:RiskMember": ["보험 중개(Marsh Risk)", "#002c77"],
  "mrsh:ReinsuranceMember": ["재보험(Guy Carpenter)", "#009de0"],
  "mrsh:PeopleAndInvestmentsMember": ["인력·투자(Mercer)", "#00a3a1"],
  "mrsh:ManagementConsultingMember": ["경영 컨설팅(Oliver Wyman)", "#6e7ab8"]
 },
 "ignore": [
  "mrsh:InvestmentsAndRetirementMember", "mrsh:HealthAndBenefitsMember", "mrsh:WorkforceAndRewardsMember", "mrsh:RiskReinsuranceMember"
 ]
}
