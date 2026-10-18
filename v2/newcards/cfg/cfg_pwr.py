# PWR(콴타 서비스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 121(시총 118위).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 시작 전 접수), 8-K(선순위채 발행 2026-08-03 가격 결정·08-06 발행), StockAnalysis.
# 엔진 입력(2026-10-17): 4분기 EPS 보도자료 값(2021 $0.71). 공통 수정 — 실적 8-K에 붙은 XBRL이 전년 4분기 3개월 값을 처음 직접 실어
# 2023-12~2024-12 영업이익 TTM 공개일이 전부 2025-02-20으로 밀렸던 것을 고쳤다(build_multiple_history.quarterly_flow, EV/EBITDA 1,117일 → 1,255일).
# 비영업 자산: 장기투자 $433.9M 중 통합 지분법 투자 $283.3M(이익이 영업이익 안)은 영업 자산 — 합계를 버리고(build_dcf.NONOP_FROM_EXTRA) 비통합 지분법(원문 차원 값,
# BUILD dim_facts → adapters/dim_fact_feed.py, 최신 공시에 없으면 빌드 멈춤) + 비시장성 지분증권(표준 태그)만 더한다 — 분기마다 손입력 없음(2026-10-17 dr). 비통합분은 2022-08 10-Q부터 공시(2021-12 비교 수치 포함) — 그 전 시점은 미공시라 0(주당 약 $0.2 과소).
# 인수가 잦다 — 2025년 Dynamic Systems 포함 8건, 2026년 상반기 3건(현금 $930M), 6/30 뒤 1건. 매출 증가율에 인수분이 섞여 있다.
BUILD = {'dim_facts': [('us-gaap:EquityMethodInvestments', 'srt:ScheduleOfEquityMethodInvestmentEquityMethodInvesteeNameAxis',
                        'pwr:NonIntegralUnconsolidatedAffiliatesMember', 'EquityMethodInvestmentsNonIntegralPwr')]}   # 비영업 자산 — 원문 차원 값(nonop_extra tag)
CIK = '0001050915'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Quanta Services'
S_ = 'https://www.sec.gov/Archives/edgar/data/1050915/'
SEC = S_
TENQ = S_ + '000105091526000025/pwr-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000119312526324855/d56853dex991.htm', 'q1': S_ + '000119312526193918/d107542dex991.htm',
      'q4': S_ + '000119312526058069/d101511dex991.htm', 'q3': S_ + '000119312525257378/d851878dex991.htm'}
LINKS = {'notes': S_ + '000119312526331400/d114917dex991.htm'}
FAIRBAND_TITLE = 'id="pwrFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 12)
ACT_REASON = '매입채무 단독 태그가 2020년 말부터라(그 전엔 미지급 비용과 합산) 5년 비교 분기가 2개 모자람'   # build_activity_score 21행 요건(Fable 2026-10-17)
NONOP_WHAT = '비통합 지분법 투자·비시장성 지분'
PH = ['EME', 'J', 'ETN', 'GEV', 'VRT', 'URI']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '시공·전력 설비 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '시공·전력 설비 PBR 비교', 'psr': '시공·전력 설비 PSR 비교',
                'pcr': '시공·전력 설비 PCR(FCF) 비교', 'evebitda': '시공·전력 설비 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(PWR 제외)와 배수 순위를 매긴 값이다.',
            '기계·항공·운송·건설·업무 서비스 회사가 섞여 있다. 차트에는 시공·전력 설비 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문 표) — 전력 7,837.8 + 지하·인프라 1,719.2 = 9,557.0(연결 매출).
SEG = [('전력', 7837.8, '#e87722'), ('지하·인프라', 1719.2, '#5a6b7a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 8/3 선순위채 가격 결정을 넣으므로 Q2 실적(7/30)도 손으로 쓴다(README). 가이던스·조정 EPS는 쓰지 않는다.
# 반응일: 실적 8-K는 모두 동부 06~07시 접수(장 시작 전) → 같은 날. 선순위채 보도자료는 8/3 자(시각 미표기, 8-K는 8/4 06:04 접수) — 8/3로 두고 제목에 밝힌다(Codex).
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 3일 — 선순위채 $2.0B 발행 가격 결정(보도 시각 미표기 · 등락은 8/3 종가)', '2026-08-03',
     '2029·2033·2036년 만기 3종(연 4.85~5.55%) · 8월 6일 발행 · 자금은 기업어음·신용 약정 차입금 상환 등 — 순증 규모는 미정, 카드의 차입금(6/30 기준 $6.1B)에는 아직 없다', 'notes', 'Quanta Services 공시 (SEC 8-K)'),
    ('green', '2026년 7월 30일 — Q2 2026 실적', '2026-07-30',
     '매출 $9.56B(+41.1%, 인수분 포함) · 희석 EPS $2.96(1년 전 $1.52)', 'q2', 'Quanta Services 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 30일 — Q1 2026 실적', '2026-04-30',
     '매출 $7.87B(+26.3%) · 희석 EPS $1.45(1년 전 $0.96)', 'q1', 'Quanta Services 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 19일 — Q4 2025 실적', '2026-02-19',
     '매출 $7.84B(+19.7%) · 희석 EPS $2.08(1년 전 $2.03) · 2025년 매출 $28.48B', 'q4', 'Quanta Services 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 30일 — Q3 2025 실적', '2025-10-30',
     '매출 $7.63B(+17.5%) · 희석 EPS $2.24(1년 전 $1.95)', 'q3', 'Quanta Services 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Strong Buy', 'n': 31, 'nt': 23, 'mean': 799.35, 'median': 800, 'low': 684, 'high': 945, 'sb': 24, 'b': 1, 'h': 5, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-17'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-Q 부문 표 Q2 2026 7,837.8/1,719.2, 1년 전 5,458.1/1,314.9 = 연결 매출(2026-10-17) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "pwr:ElectricMember": [
   "전력",
   "#e87722"
  ],
  "pwr:UndergroundAndInfrastructureMember": [
   "지하·인프라",
   "#5a6b7a"
  ]
 },
 "ignore": []
}
