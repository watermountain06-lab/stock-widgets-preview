# CHD(처치 앤 드와이트) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 생활용품 — Arm & Hammer(베이킹소다·세제·고양이 모래), OxiClean, TheraBreath, Batiste, Hero, Touchland 등.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-31), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/CHD.md.
# 엔진 입력(2026-10-25): 차입금 = 기업어음 $49.9M + 장기 $2,206.3M(DEBT_TOTAL_TAG — 기본 합산이 같은 금액의 CommercialPaper를 또 더했다), 현금 $254.8M.
# D&A = 감가상각 + 상각(DDA_PARTS_BY_CIK — 합산 태그가 2026-03에 멈춤, FY2025 연간 합 일치).
# 일회성: Q4 2025 비타민 사업 매각 손실 세전 $58.5M(세후 $45.6M, 주당 $0.18 — 영업외) — 최근 4분기 GAAP EPS 3.11이 회사 조정 3.51보다 약 11% 낮다(매각 손실 몫은 약 6%, 나머지는 Touchland 주식보상·조건부 대가 등). 빼도 표 유지(Fable r1).
CIK = '0000313927'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Church & Dwight'
S_ = 'https://www.sec.gov/Archives/edgar/data/313927/'
SEC = S_
TENQ = S_ + '000119312526327567/chd-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000119312526326749/chd-ex99_1.htm', 'q1': S_ + '000119312526199066/chd-ex99_1.htm',
      'q4': S_ + '000119312526030474/chd-ex99_1.htm', 'q3': S_ + '000119312525259387/chd-ex99_1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="chdFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 GAAP 이익에는 Q4 2025 비타민 사업 매각 손실(주당 $0.18)과 인수 관련 주식보상 등이 들어 있어 회사 조정 이익보다 약 11% 낮다 — PER이 그만큼 높게 나온다(회사 조정 이익으로 계산해도 세 표는 같다). '
              '브랜드 인수를 자주 해 무형자산 상각이 크고, 과거에도 손상(2022년 Flawless, 2024년 비타민 상표)이 있어 5년 PER 이력에 튀는 구간이 있다. 사업 매각 때문에 매출 성장률이 실제 기존 사업 성장보다 낮게 보인다. '
              '현금흐름 모델 값이 낮은 것은 인수로 쌓인 영업권 때문에 투하자본 대비 이익률이 할인율과 비슷하게 나와 성장이 가치를 거의 더하지 못하기 때문이다.')
PH = ['CL', 'CLX', 'KMB', 'PG', 'KVUE', 'SJM']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '생활용품 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(CHD 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·담배·생활용품 제조사와 소매가 섞여 있다. 차트에는 생활용품 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 국내 소비재 1,155.8 + 해외 소비재 297.5 + 특수 제품 76.7 = 1,530.0.
SEG = [('미국 소비재', 1155.8, '#0055a5'), ('해외 소비재', 297.5, '#5d9bd5'), ('특수 제품(동물 영양 등)', 76.7, '#f2a900')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07:04~07:08 동부 접수) → 같은 날. 넣지 않은 8-K: 지배구조 지침, 주총. 비타민 사업 매각 합의(12/9)는 Q4 실적 항목에 적는다.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 31일 — Q2 2026 실적', '2026-07-31',
     '순매출 $1.53B(+1.6%) · 순이익 $203M · 희석 EPS $0.85(1년 전 $0.78 — 사업 철수 손상 포함)', 'q2', 'Church & Dwight 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 1일 — Q1 2026 실적', '2026-05-01',
     '순매출 $1.47B · 순이익 $216M · 희석 EPS $0.91(1년 전 $0.89)', 'q1', 'Church & Dwight 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 30일 — Q4 2025 실적', '2026-01-30',
     '순매출 $1.64B · 순이익 $144M · 희석 EPS $0.60(1년 전 $0.76) — 비타민 사업 매각 손실 세전 $58.5M 포함 · 2025년 EPS $3.02', 'q4', 'Church & Dwight 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 31일 — Q3 2025 실적', '2025-10-31',
     '순매출 $1.59B · 순이익 $182M · 희석 EPS $0.75(1년 전 −$0.31 — 비타민 상표 손상)', 'q3', 'Church & Dwight 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 12, 'mean': 112.42, 'median': 115, 'low': 89, 'high': 120, 'sb': 8, 'b': 2, 'h': 8, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 3개(수동 지도, 영업 부문 차원). 원문 대조: Q2 2026 1,155.8/297.5/76.7(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"chd:ConsumerDomesticMember": ["미국 소비재", "#0055a5"], "chd:ConsumerInternationalMember": ["해외 소비재", "#5d9bd5"],
             "chd:SpecialtyProductsDivisionMember": ["특수 제품(동물 영양 등)", "#f2a900"]},
 "ignore": []
}
