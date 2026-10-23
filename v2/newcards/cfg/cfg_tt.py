# TT(트레인 테크놀로지스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 115. 아일랜드 법인이지만 10-Q·10-K 제출(미국 발행사 경로).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항), 8-K(Stellar Energy 인수 계약 2025-12-02, COO 선임 2026-06-10), StockAnalysis.
# 엔진 입력(2026-10-16): 현금은 …IncludingDisposalGroupAndDiscontinuedOperations(기본 태그는 연말만 — 2025-12 값이 9개월 쓰였다), 차입금 = DebtCurrent + 비유동(유동 $693M이 빠졌었다),
# 리스는 연간 OperatingLeaseLiability(유동·비유동 태그가 2020년에 멈춤 — 2021~2024 EV 이력엔 2020년 값). 4분기 EPS: 2024년 보도자료 순이익 기준 $2.66(역산 $2.65).
# EPS는 순이익 기준(중단사업 포함 — 석면 관련 등 분기 −$0.04 안팎). 보도자료 헤드라인은 계속사업 EPS라 숫자가 조금 다르다.
# 2020-03-02 Yahoo "분할" 1.289:1은 Ingersoll Rand 산업 부문 분리 조정 — 5년 창 앞이라 계산에 들어가지 않는다.
CIK = '0001466258'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Trane Technologies'
S_ = 'https://www.sec.gov/Archives/edgar/data/1466258/'
SEC = S_
TENQ = S_ + '000162828026051117/tt-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000162828026050743/exhibit991-q22026earningsr.htm', 'q1': S_ + '000162828026028547/exhibit991-q12026earningsr.htm',
      'q4': S_ + '000162828026003953/exhibit991-q42025earningsr.htm', 'q3': S_ + '000162828025047261/exhibit991-q32025earningsr.htm'}
LINKS = {'coo': S_ + '000162828026042055/projectsouthernpressrelease.htm', 'stellar': S_ + '000162828025054789/projectkramerpressrelease.htm'}
FAIRBAND_TITLE = 'id="ttFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 25)
ACT_REASON = ''
NONOP_WHAT = '장기투자'
PH = ['CARR', 'JCI', 'LII', 'ETN', 'EMR', 'HON']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '공조·전기 설비 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '공조·전기 설비 PBR 비교', 'psr': '공조·전기 설비 PSR 비교',
                'pcr': '공조·전기 설비 PCR(FCF) 비교', 'evebitda': '공조·전기 설비 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(TT 제외)와 배수 순위를 매긴 값이다.',
            '기계·항공·운송·건설·업무 서비스 회사가 섞여 있다. 차트에는 공조·전기 설비 6곳만 보인다.')
# 부문(Q2 2026 10-Q 부문 주석) — 미주 5,271.3 + EMEA 697.6 + 아시아·태평양 384.6 = 6,353.5(연결 매출).
SEG = [('미주', 5271.3, '#6400ff'), ('EMEA', 697.6, '#9c5cff'), ('아시아·태평양', 384.6, '#c9b0ff')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역 부문별'
# 손 뉴스: Q2 2026 실적(7/30)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤 손 항목은 없다. 가이던스는 쓰지 않는다.
# Stellar 인수는 2026-02-17 완료(현금 제외 $553.4M, 미주 부문 — Q2 10-Q 인수 주석; 뉴스에는 8-K 원문만).
# 반응일: 실적 8-K는 동부 장중(10~11시) 접수 — 보도자료는 장 시작 전이라 같은 날. 인수 계약 8-K는 12/2 21:32 접수 → 12/3. COO 8-K는 6/10 10:16 → 6/10.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('red', '2026년 6월 10일 — COO 선임', '2026-06-10',
     'Donny Simmons(미주 그룹 사장) 7월 1일부터 COO · Dave Regnery 의장·CEO에게 보고', 'coo', 'Trane Technologies 공시 (SEC 8-K)'),
    ('green', '2026년 4월 30일 — Q1 2026 실적', '2026-04-30',
     '매출 $4.97B(+6%) · 희석 EPS $2.62(1년 전 $2.67)', 'q1', 'Trane Technologies 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 29일 — Q4 2025 실적', '2026-01-29',
     '매출 $5.14B(+6%) · 희석 EPS $2.64(1년 전 $2.66) · 2025년 EPS $12.98', 'q4', 'Trane Technologies 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 12월 2일 장 마감 뒤 — Stellar Energy 데이터센터 냉각 사업 인수 계약', '2025-12-03',
     'Stellar Energy International로부터 Stellar Energy Digital 인수 — 액체 냉각 데이터센터용 모듈형 냉각 설비', 'stellar', 'Trane Technologies 공시 (SEC 8-K)'),
    ('green', '2025년 10월 30일 — Q3 2025 실적', '2025-10-30',
     '매출 $5.74B(+6%) · 희석 EPS $3.78(1년 전 $3.39)', 'q3', 'Trane Technologies 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 26, 'nt': 14, 'mean': 540.64, 'median': 550, 'low': 485, 'high': 575, 'sb': 14, 'b': 3, 'h': 8, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-17'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 지역 축(StatementGeographicalAxis)이지만 값이 부문 주석과 같다:
# Q2 2026 5,271.3/697.6/384.6, 1년 전 4,692.3/707.9/346.2 = 연결 매출(2026-10-16) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "srt:StatementGeographicalAxis",
 "extra": {},
 "members": {
  "srt:AmericasMember": [
   "미주",
   "#6400ff"
  ],
  "us-gaap:EMEAMember": [
   "EMEA",
   "#9c5cff"
  ],
  "srt:AsiaPacificMember": [
   "아시아·태평양",
   "#c9b0ff"
  ]
 },
 "ignore": []
}
