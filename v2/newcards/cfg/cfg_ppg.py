# PPG(PPG 인더스트리즈) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 도료·코팅 — 건축용(Global Architectural), 자동차 보수·항공·보호 코팅(Performance), 자동차 OEM·산업·포장 코팅(Industrial).
# 출처: SEC XBRL + 인라인 XBRL 보충(BUILD overlay — companyfacts에 7/29 Q2 10-Q가 없다, 시험 3장 중 1), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/PPG.md.
# 엔진 입력(2026-10-25): 영업이익 = 세전이익 + 이자비용 − 이자수익(DERIVED_OPINC — OperatingIncomeLoss 태그는 4분기 행이 없는 부문 이익 합계로 보여 합성만 쓴다; 10-K 연간 이자는 InterestExpenseNonoperating),
# 차입금 = 1년 안·단기 $691M + 장기 $6,195M(DEBT_TOTAL_TAG — LongTermDebt $6,876M은 1년 안 포함이라 겹침), 현금 $1,520M·단기투자 $74M, 비지배지분 $147M.
# EPS는 계속사업 EPS 우선(BUILD eps_tag — 헤드라인이 계속사업 기준, 총 EPS와 0.01~0.02 차이; 2024 Q4는 중단사업 손실로 총 EPS −1.20).
# 일회성: 상각 제외 일회성(구조조정·환경 정화·세무·포트폴리오) 최근 4분기 약 5%.
BUILD = {'overlay': True, 'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}
CIK = '0000079879'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'PPG'
S_ = 'https://www.sec.gov/Archives/edgar/data/79879/'
SEC = S_
TENQ = S_ + '000007987926000252/ppg-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000007987926000246/exhibit99-2q2026earningsre.htm', 'q1': S_ + '000007987926000167/exhibit99-1q2026earningsre.htm',
      'q4': S_ + '000007987926000025/exhibit99-4q2025earningsre.htm', 'q3': S_ + '000007987925000306/exhibit99-3q2025earningsre.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ppgFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 계속사업 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('손익계산서에 영업이익 줄이 없어 세전이익에 이자비용을 더하고 이자수익을 빼서 영업이익으로 쓴다(구조조정·환경 정화 같은 기타 비용은 영업으로 둔다). '
              '2024년 미국·캐나다 건축용 도료 사업 매각 전후로 사업 범위가 달라 5년 이력이 끊긴다. SEC 요약 자료에 최신 10-Q가 아직 없어 원문 인라인 XBRL로 채웠다.')
PH = ['SHW', 'ECL', 'DD', 'AVY', 'LIN', 'APD']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '화학·코팅 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(PPG 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·건자재·포장재가 섞여 있다. 차트에는 화학·코팅 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 산업 1,778 + 퍼포먼스 1,619 + 건축 1,098 = 4,495.
SEG = [('산업 코팅', 1778, '#0078c1'), ('퍼포먼스 코팅', 1619, '#6cb4e4'), ('건축용 도료', 1098, '#4d4d4d')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건 + Q1 사전 발표(EPS는 계속사업 희석). 반응일: 장 마감 뒤 발표(16:11~16:42 동부 접수) → 다음 거래일. 넣지 않은 8-K: 사채 발행·상환, CFO 교체(7/6), 주총.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('red', '2026년 7월 28일 장 마감 뒤 — Q2 2026 실적', '2026-07-29',
     '매출 $4.50B(+7.2%) · 계속사업 순이익 $439M · 희석 EPS $1.96(1년 전 $1.98) — 환경 정화·소송 비용 포함, 다음 날 주가 −6%', 'q2', 'PPG 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 장 마감 뒤 — Q1 2026 실적', '2026-04-29',
     '매출 $3.93B · 계속사업 순이익 $382M · 희석 EPS $1.70(1년 전 $1.64)', 'q1', 'PPG 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 27일 장 마감 뒤 — Q4 2025 실적', '2026-01-28',
     '매출 $3.91B · 계속사업 순이익 $302M · 희석 EPS $1.34(1년 전 $0.01 — 구조조정 비용) · 2025년 계속사업 EPS $6.92', 'q4', 'PPG 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 28일 장 마감 뒤 — Q3 2025 실적', '2025-10-29',
     '매출 $4.08B · 계속사업 순이익 $444M · 희석 EPS $1.96(1년 전 $1.90) — 다음 날 주가 −6%', 'q3', 'PPG 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 25, 'nt': 15, 'mean': 132.07, 'median': 135, 'low': 120, 'high': 140, 'sb': 10, 'b': 2, 'h': 13, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 3개(수동 지도, 지역 차원 없는 값). 원문 대조: Q2 2026 1,778/1,619/1,098(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"ppg:IndustrialCoatingsSegmentMember": ["산업 코팅", "#0078c1"], "ppg:PerformanceCoatingsSegmentMember": ["퍼포먼스 코팅", "#6cb4e4"],
             "ppg:GlobalArchitecturalCoatingsSegmentMember": ["건축용 도료", "#4d4d4d"]},
 "ignore": []
}
