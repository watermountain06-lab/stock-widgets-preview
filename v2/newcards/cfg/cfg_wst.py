# WST(웨스트 파마슈티컬 서비스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 주사제 포장 부품(고무 마개·주사기 부품, Proprietary)과 위탁 생산(West Vantage).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-23), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), 8-K(사이버 사고 1.05 2026-05-11), StockAnalysis. 사전 조사 scratchpad pre/WST.md.
# 엔진 입력(2026-10-25): 차입금 $202.9M(LongTermDebt), 현금 $435.8M. 일회성 작음(최근 4분기 GAAP 7.81 대 회사 조정 8.50 — 상각 등 반복 차이).
CIK = '0000105770'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'West'
S_ = 'https://www.sec.gov/Archives/edgar/data/105770/'
SEC = S_
TENQ = S_ + '000010577026000099/wst-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000010577026000097/exh991q22026earningsrelease.htm', 'q1': S_ + '000010577026000047/exh991q12026earningsrelease.htm',
      'q4': S_ + '000010577026000005/exh991q42025earningsrelease.htm', 'q3': S_ + '000010577025000090/exh991q32025earningsrelease.htm'}
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-29', 'src': '회사 공지 — 장 시작 전 발표, 콜 오전 8시(동부)'}
LINKS = {'cyber': S_ + '000010577026000068/wst-20260507.htm'}
FAIRBAND_TITLE = 'id="wstFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('코로나 백신 특수(2021~2022)로 이익이 크게 늘었다가 줄어든 뒤 다시 회복하는 중이라, 5년 이력의 이익률·성장률에 그 고점이 섞여 있다. '
              '고부가 부품(GLP-1 주사제용 등) 비중이 커지며 매출이 늘고 있다. 5월 사이버 사고는 회사가 실적 영향이 크지 않다고 밝혔다. CEO가 6월에 바뀌었다.')
PH = ['TMO', 'DHR', 'A', 'MTD', 'BDX', 'STE']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '생명과학 도구·의료 소모품 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(WST 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·유통·생명과학 도구가 섞여 있다. 차트에는 생명과학 도구·의료 소모품 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 자체 제품 722.6 + 위탁 생산 149.7 = 872.3.
SEG = [('자체 제품(Proprietary)', 722.6, '#00539b'), ('위탁 생산(West Vantage)', 149.7, '#5c94cc')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q2 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석) + 사이버 사고. 반응일: 장 전 발표 → 같은 날, 사이버 8-K 5/11 17:06(동부, 장 마감 뒤) → 5/12. 넣지 않은 8-K: CEO 교체(3/9 은퇴 예정·6/1 선임), Daikyo 계약(7/14), 주총.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 23일 — Q2 2026 실적', '2026-07-23',
     '매출 $872M(+13.8%) · 순이익 $154M · 희석 EPS $2.15(1년 전 $1.82)', 'q2', 'West 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 11일 장 마감 뒤 — 사이버 사고 공시', '2026-05-12',
     '5/4 침입 탐지 — 데이터 유출·시스템 암호화로 운영 차질(Q2 매출 약 $7M 감소 — 10-Q), 5/20 정상화 후속 공시', 'cyber', 'West 공시 (SEC 8-K)'),
    ('green', '2026년 4월 23일 — Q1 2026 실적', '2026-04-23',
     '매출 $845M · 순이익 $139M · 희석 EPS $1.92(1년 전 $1.23) — 발표 당일 주가 +13%', 'q1', 'West 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 12일 — Q4 2025 실적', '2026-02-12',
     '매출 $805M · 순이익 $132M · 희석 EPS $1.82(1년 전 $1.78) · 2025년 희석 EPS $6.79', 'q4', 'West 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 23일 — Q3 2025 실적', '2025-10-23',
     '매출 $805M · 순이익 $140M · 희석 EPS $1.92(1년 전 $1.85) — 발표 당일 주가 +11%', 'q3', 'West 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 16, 'nt': 10, 'mean': 413.4, 'median': 415, 'low': 375, 'high': 447, 'sb': 12, 'b': 3, 'h': 0, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 2개(수동 지도). 원문 대조: Q2 2026 722.6/149.7(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"wst:ProprietaryProductsMember": ["자체 제품(Proprietary)", "#00539b"], "wst:WestVantageSegmentMember": ["위탁 생산(West Vantage)", "#5c94cc"]},
 "ignore": []
}
