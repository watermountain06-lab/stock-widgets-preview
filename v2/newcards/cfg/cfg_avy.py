# AVY(에이버리 데니슨) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일(2025년부터 달력 분기말, 그 전은 토요일 마감). 라벨·포장 소재(Materials Group), RFID·의류 라벨·브랜드 솔루션(Solutions Group).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-04 장 마감 뒤), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/AVY.md.
# 엔진 입력(2026-10-25): 영업이익 = 세전이익 + 이자비용 − 기타 영업외 수익(DERIVED_OPINC — OperatingIncomeLoss 태그 없음), 차입금 = 1년 안 $500.5M + 장기 $3,177.7M(DEBT_TOTAL_TAG), 현금 $227.3M.
# 인수 = ACQ_FIXED $391.6M(Taylor Adhesives 2025-10-20 약 $390M — Wiliot 소수 지분 투자 약 $75M은 뺌). 일회성 작음(GAAP이 조정 EPS보다 약 11% 낮은 것은 구조조정·상각 등 반복 항목).
CIK = '0000008818'
CUR, YO, QO = '2026-06-30', '2025-06-28', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-28'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Avery Dennison'
S_ = 'https://www.sec.gov/Archives/edgar/data/8818/'
SEC = S_
TENQ = S_ + '000000881826000131/avy-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000000881826000127/ex9918k7-30x26.htm', 'q1': S_ + '000000881826000075/ex9918k4-28x26.htm',
      'q4': S_ + '000000881826000004/ex9918k2-4x26.htm', 'q3': S_ + '000119312525245839/d79220dex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="avyFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 15)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('손익계산서에 영업이익 줄이 태깅되지 않아 세전이익에 이자비용을 더하고 기타 영업외 수익(연금 등)을 빼서 영업이익으로 쓴다. '
              'D&A는 감가상각 + 무형자산 상각이다 — 소프트웨어 상각(연 약 $30M)은 표준 태그가 없어 빠져 EBITDA가 약 2% 작다. '
              '2025년 Taylor Adhesives 인수(약 $390M)가 최근 4분기 투자에 들어 있다. Q3 2026 실적이 10월 말 나올 예정이다.')
PH = ['BALL', 'AMCR', 'PKG', 'IP', 'SW', 'PPG']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '포장재·소재 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(AVY 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·건자재·포장재가 섞여 있다. 차트에는 포장재·소재 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 외부 매출) — 소재 1,796.1 + 솔루션 666.8 = 2,462.9.
SEG = [('라벨·포장 소재', 1796.1, '#e4002b'), ('RFID·의류 라벨 솔루션', 666.8, '#4d4d4d')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:45~09:07 동부 접수) → 같은 날. 넣지 않은 8-K: 이사회 의장 선임(8/19).
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 30일 — Q2 2026 실적', '2026-07-30',
     '매출 $2.46B(+11%) · 순이익 $204M · 희석 EPS $2.67(1년 전 $2.41)', 'q2', 'Avery Dennison 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 — Q1 2026 실적', '2026-04-28',
     '매출 $2.30B · 순이익 $168M · 희석 EPS $2.18(1년 전 $2.09)', 'q1', 'Avery Dennison 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 4일 — Q4 2025 실적', '2026-02-04',
     '순이익 $166M · 희석 EPS $2.15(1년 전 $2.17) · 2025년 EPS $8.79 · Taylor Adhesives 인수(2025-10)', 'q4', 'Avery Dennison 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 22일 — Q3 2025 실적', '2025-10-22',
     '매출 $2.22B · 순이익 $166M · 희석 EPS $2.13(1년 전 $2.25)', 'q3', 'Avery Dennison 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 11, 'nt': 9, 'mean': 198.44, 'median': 198, 'low': 175, 'high': 230, 'sb': 7, 'b': 2, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 2개(수동 지도, 영업 부문 차원). 원문 대조: Q2 2026 1,796.1/666.8(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"avy:MaterialsGroupSegmentMember": ["라벨·포장 소재", "#e4002b"], "avy:SolutionsGroupSegmentMember": ["RFID·의류 라벨 솔루션", "#4d4d4d"]},
 "ignore": []
}
