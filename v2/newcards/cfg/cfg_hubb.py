# HUBB(허벨) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 전력망 부품(송배전 연결·보호·자동화)과 전기 배선·산업용 제품.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-28), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/HUBB.md.
# 엔진 입력(2026-10-29): 차입금 1년 안 $613.8M(CP $313M + 유동 채권 $300M) + 장기 $4,506.4M = $5,120.2M(엔진 DEBT_TOTAL_TAG 줄), 현금 $334.5M + 단기투자 $20M. 인수 = 최근 4분기 $3.8B(NSI Industries $3.0B, 2026-06).
# 일회성: 최근 4분기 거래·통합 비용 주당 0.61(Q2 집중), Q3 매출원가의 관세(IEEPA) 환급 약 $31M(주당 약 0.44, 조정에서도 안 뺌) — 서로 상쇄, 순 약 1%.
CIK = '0000048898'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Hubbell'
S_ = 'https://www.sec.gov/Archives/edgar/data/48898/'
SEC = S_
TENQ = S_ + '000162828026067729/hubb-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000162828026067421/exhibit991_10272026.htm', 'q2': S_ + '000162828026049934/exhibit991_07282026.htm', 'q1': S_ + '000162828026028600/exhibit991_04302026.htm', 'q4': S_ + '000162828026004800/exhibit991_02032026.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="hubbFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('NSI Industries 인수($3.0B 현금, 2026-06)가 최근 4분기 투자에 들어 있어 투자 효율이 낮게 잡힌다. 인수로 무형자산 상각이 늘어(Q3 주당 0.89) GAAP EPS와 회사 조정 EPS 차이가 커졌다. '
              '3분기 매출원가에는 관세(IEEPA) 환급 약 $31M이 들어 있다.')
PH = ['ETN', 'AME', 'ROK', 'EMR', 'GEV', 'VRT']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '전력·전기 설비 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(HUBB 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 전력·전기 설비 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 유틸리티 솔루션 1,027.8 + 전기 솔루션 844.7 = 1,872.5.
SEG = [('유틸리티 솔루션(전력망)', 1027.8, '#c8102e'), ('전기 솔루션', 844.7, '#4d4d4d')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(08:0x 동부) → 같은 날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 27일 — Q3 2026 실적', '2026-10-27',
     '매출 $1.87B(+24.6%, NSI 인수 포함) · 순이익 $263M · 희석 EPS $4.94(1년 전 $4.77) — 당일 주가 −5.5%', 'q3', 'Hubbell 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 28일 — Q2 2026 실적', '2026-07-28',
     '매출 $1.71B · 순이익 $240M · 희석 EPS $4.52(1년 전 $4.56) — NSI 인수 비용 포함', 'q2', 'Hubbell 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 30일 — Q1 2026 실적', '2026-04-30',
     '매출 $1.52B · 순이익 $182M · 희석 EPS $3.41(1년 전 $3.03) — 당일 주가 −6.9%', 'q1', 'Hubbell 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 3일 — Q4 2025 실적', '2026-02-03',
     '매출 $1.49B · 순이익 $224M · 희석 EPS $4.19(1년 전 $3.66) · 2025년 EPS $16.54', 'q4', 'Hubbell 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 15, 'nt': 9, 'mean': 557.22, 'median': 580, 'low': 486, 'high': 600, 'sb': 7, 'b': 1, 'h': 7, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-29'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 1,027.8/844.7(2026-10-29) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"hubb:UtilitySolutionsSegmentMember": ["유틸리티 솔루션(전력망)", "#c8102e"], "hubb:ElectricalSegmentMember": ["전기 솔루션", "#4d4d4d"]},
 "ignore": []
}
