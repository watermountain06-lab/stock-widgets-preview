# ADP(오토매틱 데이터 프로세싱) v2 카드 설정 — 자동 카드(AUTO). 회계연도 6월 말(Q4 FY26 = 2026-04~06). 카드 순위 110.
# 출처: SEC XBRL, FY2026 10-K(2026-08-05), 실적 보도자료(Q1~Q4 FY26, 8-K 2.02항 — 모두 장 시작 전 접수), 8-K(회사채 2026-05-07, 신용 약정 2026-06-26), StockAnalysis.
# 엔진 입력(2026-10-16): 손익계산서에 영업이익 줄이 없어 합성 — 세전 − "Other (income)/expense, net" + 이자비용 = 매출 − 원가 − 판관비(FY26 $5,779M,
# build_multiple_history DERIVED_OPINC, 세전 태그가 FY2021까지 달라 목록으로 잇는다). 설비투자는 PaymentsToAcquireOtherPropertyPlantAndEquipment(EXTRA_TAGS) —
# 자본화 소프트웨어("Additions to intangibles" $468.5M)는 넣지 않는다(공통 안건, MCK와 같은 정의). 고객 자금($44.0B)과 고객 지급 의무($44.4B)는 맞물린 통과 잔액이라
# 현금·차입금·비영업 자산에 넣지 않는다(엔진 기본 태그가 이미 뺀다). 고객 자금 이자($1,355M)는 매출 안이라 영업.
# 환매조건부 차입(회사 고유 태그)을 차입금에 — build_multiple_history DEBT_TOTAL_TAG(Codex 2026-10-16)
BUILD = {'company_tags': [('adp:ObligationsUnderReverseRepurchaseAgreements', 'SecuritiesSoldUnderAgreementsToRepurchase')]}
CIK = '0000008670'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
FY_ENDS, FY_LABEL = ('2026-06-30', '2025-06-30'), 'FY2026'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'ADP'
S_ = 'https://www.sec.gov/Archives/edgar/data/8670/'
SEC = S_
TENQ = S_ + '000000867026000030/adp-20260630.htm'; TENQ_NAME = 'FY2026 10-K'
PR = {'q4': S_ + '000000867026000025/q4fy26exhibit99.htm', 'q3': S_ + '000000867026000016/q3fy26exhibit99.htm',
      'q2': S_ + '000000867026000006/q2fy26exhibit99.htm', 'q1': S_ + '000000867025000042/q1fy26exhibit99.htm'}
LINKS = {'notes': S_ + '000119312526212131/d932558d8k.htm', 'credit': S_ + '000095014226001884/eh260799361_8k.htm'}
FAIRBAND_TITLE = 'id="adpFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (15, 40)
ACT_REASON = ''
NONOP_WHAT = '장기 시장성 증권'
PH = ['PAYX', 'BR', 'VRSK', 'EFX', 'CTAS', 'LDOS']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '업무 서비스 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '업무 서비스 PBR 비교', 'psr': '업무 서비스 PSR 비교',
                'pcr': '업무 서비스 PCR(FCF) 비교', 'evebitda': '업무 서비스 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(ADP 제외)와 배수 순위를 매긴 값이다.',
            '기계·항공·운송·건설·업무 서비스 회사가 섞여 있다. 급여 대행처럼 자산이 가벼운 회사는 PBR이 높게 나온다. 차트에는 업무 서비스 6곳만 보인다.')
# 부문(FY2026 10-K 부문 주석 연간 − Q3 FY26 10-Q 9개월 누계, 부문 매출 = 외부 고객 + 고객 자금 이자 + 사내 거래) —
# 고용주 서비스 14,831.4 − 11,134.6 = 3,696.8, PEO 7,128.1 − 5,348.7 = 1,779.4, 합 5,476.2 − 사내 거래 2.4 = 연결 매출 5,473.8.
SEG = [('고용주 서비스', 3696.8, '#d0271d'), ('PEO(전문 고용주)', 1779.4, '#5a5a5a')]
SEG_ADJ = -2.4
SEG_TITLE = '매출 구성 — 부문별(고객 자금 이자 포함, 사내 거래 상계 전)'
# 손 뉴스: Q4 FY26 실적(7/29)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤 손 항목은 없다. 가이던스는 손 뉴스에도 쓰지 않는다(CVS 2026-10-15).
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 6월 26일 — 신용 약정 교체', None,
     '364일 약정 $5.7B(이전 $4.55B)·5년 약정 $3.5B, 이전 두 약정은 같은 날 종료', 'credit', 'ADP 공시 (SEC 8-K)'),
    ('neutral', '2026년 5월 7일 — 회사채 $1.0B 발행', None,
     '연 5.000%, 2036년 만기', 'notes', 'ADP 공시 (SEC 8-K)'),
    ('green', '2026년 4월 29일 — Q3 FY26 실적', '2026-04-29',
     '매출 $5.94B(+7%) · 희석 EPS $3.38(1년 전 $3.06)', 'q3', 'ADP 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 28일 — Q2 FY26 실적', '2026-01-28',
     '매출 $5.36B(+6%) · 희석 EPS $2.62(1년 전 $2.35)', 'q2', 'ADP 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 29일 — Q1 FY26 실적', '2025-10-29',
     '매출 $5.18B(+7%) · 희석 EPS $2.49(1년 전 $2.34)', 'q1', 'ADP 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Hold', 'n': 18, 'nt': 16, 'mean': 283.5, 'median': 287, 'low': 225, 'high': 322, 'sb': 4, 'b': 0, 'h': 12, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-17'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-K 부문 주석 Total segment revenues FY26 14,831.4/7,128.1, FY25 13,883.1/6,690.4,
# 4분기 = 연간 − Q3 10-Q 9개월(3,696.8/1,779.4). 사내 거래 상계 −2.4(SEG_ADJ)(2026-10-16) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "adp:EmployerServicesSegmentMember": [
   "고용주 서비스",
   "#d0271d"
  ],
  "adp:ProfessionalEmployeeOrganizationServicesSegmentMember": [
   "PEO(전문 고용주)",
   "#5a5a5a"
  ]
 },
 "ignore": []
}
