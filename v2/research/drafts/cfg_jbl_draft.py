# JBL(재빌) v2 카드 설정 — 자동 카드(AUTO). 회계연도 8월 31일(FY2026 = 2025-09~2026-08). 전자 제조 서비스(EMS) — AI 데이터센터·통신 인프라, 의료·자동차·에너지(규제 산업), 소비자 기기·리테일.
# 출처: SEC XBRL(10/23 FY2026 10-K까지 요약 자료에 있음 — 4분기는 연간 − 9개월), 실적 보도자료(Q4 FY25~Q4 FY26, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/JBL.md.
# 엔진 입력(2026-10-27): 차입금 $3,379M(1년 안 $499M 포함), 금융리스 $319M, 현금 $1,739M, 최근 4분기 인수 $852M, 주주 자본 $1.6B(자산 $27.4B — 자사주 매입).
# 일회성: 구조조정·손상 FY26 $97M(Q1 $76M) — 주당 약 0.8(GAAP EPS 9.75의 약 8%). 회사 core EPS 13.09는 주식 보상·상각까지 빼서 쓰지 않는다.
CIK = '0000898293'
CUR, YO, QO = '2026-08-31', '2025-08-31', '2026-05-31'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
FY_ENDS, FY_LABEL = ('2026-08-31', '2025-08-31'), 'FY2026'
VOTES, VERDICT = (-1, 1, -2), '적정~고평가'
CO = 'Jabil'
S_ = 'https://www.sec.gov/Archives/edgar/data/898293/'
SEC = S_
TENQ = S_ + '000162828026067038/jbl-20260831.htm'; TENQ_NAME = 'FY2026 10-K'
PR = {'q4': S_ + '000162828026063890/jbl-20260930ex991.htm', 'q3': S_ + '000162828026043719/jbl-20260617ex991.htm',
      'q2': S_ + '000162828026019043/jbl-20260318ex991.htm', 'q1': S_ + '000162828025057488/jbl-20251217ex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="jblFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('AI 데이터센터 장비 수요로 FY2026 매출이 +20.6%, 4분기만 +29% 늘었다. 2024년 모바일 사업 매각 이익(2분기 EPS 7.31)이 5년 이력에 섞여 있다. '
              '자사주를 많이 사서 주주 자본이 자산의 6%뿐이라 PBR·부채비율은 크게 나온다. 회사가 내세우는 core EPS(13.09)는 주식 보상·상각까지 빼서 카드에는 쓰지 않는다.')
HEALTH_EXTRA = '자사주 매입으로 주주 자본이 작아 자본 기준 비율(부채비율 등)이 크게 나온다.'
PH = ['DELL', 'APH', 'ANET', 'CSCO', 'IBM', 'STX']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '전자 부품·하드웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(JBL 제외)과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 섞여 있다. 차트에는 전자 부품·하드웨어 6곳만 보인다.')
# 매출(Q4 FY26 = 연간 − 9개월, 10-K 부문) — 지능형 인프라 5,822 + 규제 산업 3,414 + 커넥티드 리빙·디지털 커머스 1,380 = 10,616.
SEG = [('지능형 인프라(AI·통신)', 5822, '#004b87'), ('규제 산업(의료·자동차·에너지)', 3414, '#5b8fc7'), ('커넥티드 리빙·디지털 커머스', 1380, '#f2a900')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q4 FY26)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07:31~07:32 동부) → 같은 날. 넣지 않은 8-K: 사채 발행, 이사 선임·과반 미달, 주총, 임원.
NEWS_RANGE = '2025.12 ~ 2026.09'
NEWS = [
    ('red', '2026년 9월 30일 장 전 — Q4 FY26 실적', '2026-09-30',
     '매출 $10.62B(+28.6%) · 순이익 $398M · 희석 EPS $3.76(1년 전 $1.99) · FY2026 EPS $9.75 — 당일 주가 −10.0%', 'q4', 'Jabil 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 6월 17일 장 전 — Q3 FY26 실적', '2026-06-17',
     '매출 $8.75B · 순이익 $275M · 희석 EPS $2.59(1년 전 $2.03)', 'q3', 'Jabil 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 18일 장 전 — Q2 FY26 실적', '2026-03-18',
     '매출 $8.28B · 순이익 $223M · 희석 EPS $2.08(1년 전 $1.06)', 'q2', 'Jabil 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 17일 장 전 — Q1 FY26 실적', '2025-12-17',
     '매출 $8.31B · 순이익 $146M · 희석 EPS $1.35(1년 전 $0.88) — 구조조정 비용 $76M 포함', 'q1', 'Jabil 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 10, 'nt': 9, 'mean': 437.22, 'median': 440, 'low': 378, 'high': 475, 'sb': 7, 'b': 2, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-27'


# ── 자동 카드 — 부문 3개. 원문 대조: FY2026 17,872/12,694/5,388, Q4 FY26(연간 − 9개월) 5,822/3,414/1,380(2026-10-27) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"jbl:IntelligentInfrastructureMember": ["지능형 인프라(AI·통신)", "#004b87"], "jbl:RegulatedIndustriesMember": ["규제 산업(의료·자동차·에너지)", "#5b8fc7"],
             "jbl:ConnectedLivingAndDigitalCommerceMember": ["커넥티드 리빙·디지털 커머스", "#f2a900"]},
 "ignore": []
}
