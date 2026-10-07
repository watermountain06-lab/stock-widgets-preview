# TJX(TJX 컴퍼니스) v2 카드 설정 — fill.py TJX. 회계연도는 1월 말 전후 토요일 마감(FY27 = 2026-02 ~ 2027-01). 시총 86위(S&P500 현재 시총 순, 2026-10-02 StockAnalysis 기준, 루트 카드 없음).
# 출처: SEC XBRL, Q2 FY27 10-Q(2026-08-28), 실적 보도자료(Q3 FY26~Q2 FY27, SEC 접수 모두 오전 9시 9~12분 = 장 시작 전), 8-K(이사 선임 9/16), StockAnalysis.
# 엔진 수정(2026-10-02): 손익계산서에 영업이익 줄이 없어 DERIVED_OPINC = 세전이익 − 순이자수익(InterestRevenueExpenseNet).
# 비교군은 HD·MCD와 같은 S&P500 경기소비재(build_peer_score TICKER_UNIVERSE).
BUILD = {}
CIK = '0000109198'
CUR, YO, QO = '2026-08-01', '2025-08-02', '2026-05-02'
QLABEL, YL, QQL = 'Q2 FY27', 'Q2 FY26', 'Q1 FY27'
L8 = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27', 'Q2 FY27']
RELEASE = {'rev': 15180, 'op': 1987, 'ni': 1520, 'ocf': 2226, 'cap': 497}   # 영업이익 = 세전 2,018 − 순이자수익 31, 현금흐름은 상반기 − 1분기
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'TJX'
S_ = 'https://www.sec.gov/Archives/edgar/data/109198/'
SEC = S_
PR = {'q2': S_ + '000010919826000045/tjxq2fy27earningspressrele.htm', 'q1': S_ + '000010919826000023/tjxq1fy27earningspressrele.htm',
      'q4': S_ + '000010919826000004/tjxq4fy26earningspressrele.htm', 'q3': S_ + '000010919825000058/tjxq3fy26earningspressrele.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000010919826000048/tjx-20260801.htm'; TENQ_NAME = 'Q2 FY27 10-Q'
LINKS = {}
FAIRBAND_TITLE = 'id="tjxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 최근 4분기 EPS에는 관세 환급(2분기)·카드 수수료 소송 합의(4분기) 이익이 들어 있다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {HIST[\'growth_5y\'] * 100:+.1f}%)</span>'
OPM_RANGE, Y2 = (5, 20), (0, 20)
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '점포·물류 설비 취득(현금흐름표 “Property additions”)'
STAT3 = ('기존점 매출 (Q2 FY27)', '+4%', '회사 계획 상회 · 조정 EPS $1.22(+11%)')
NEXT = ('11월 중순 예상', '일정 · Q3 FY27 (회사 미확정)'); NEXT_OP = ('11월 중순', 'Q3 FY27 예상')
FY_ENDS, FY_LABEL = ('2026-01-31', '2025-02-01'), 'FY26'
HEALTH_NOTE = ('차입금은 $2.9B(1년 안 만기 $1.0B + 장기 $1.9B)이고 현금은 $6.0B다. 운용리스 부채가 $11.4B(1년 안 $1.7B + 장기 $9.7B)로 차입금보다 훨씬 크다. '
               '순이자는 수익(2분기 $31M)이라 이자보상배율은 계산하지 않는다.')
ACT_REASON = ''
YOY_EXTRA = '기존점 매출 +4% · 관세 환급으로 세전이익 순증 $219M(제외 시 EPS $1.22) · '
SEG = [('Marmaxx (미국)', 9109, '#c8102e'), ('HomeGoods (미국)', 2507, '#f59e0b'), ('TJX International', 2094, '#0072c6'), ('TJX Canada', 1470, '#22c55e')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 사업부별 매출'
SEG_NOTE = ('기존점 매출은 Marmaxx +1%, HomeGoods +7%, TJX Canada +6%, TJX International +7% · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Q2 FY27 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (상반기, 890만 주)', '$1.4B'),
           ('FY27 자사주 매입 계획', '$2.75~3.0B'),
           ('분기 배당 (FY27부터)', '$0.425 → $0.48', '+13%')]
CHECK_WHEN = '2026년 11월 중순 (예상) · Q3 FY27'
CHECK = ['3분기 전망 기존점 매출 +2~3%, 세전이익률 12.8~12.9%(관세 환급 제외 12.3~12.4%)',
         '추가 관세 환급(회사는 금액·시기·가능성이 불확실하다고 밝힘)',
         'Marmaxx 기존점 매출(2분기 +1%)',
         'FY28부터 점포 증가율 4%, 장기 목표 7,500개']
NONOP_WHAT = '장기 투자'
PH = ['ROST', 'HD', 'LOW', 'TSCO', 'BBY', 'ULTA']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소매 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': '소매 PBR 비교', 'psr': '소매 PSR 비교',
                'pcr': '소매 PCR(FCF) 비교', 'evebitda': '소매 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
FUND_ASOF_NOTE = 'Q2 FY27 10-Q (2026-08-28 공시)'
PREMISE = ('주가가 1년 새 {CH_TXT} 내려 PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PBR·PCR·EV/EBITDA가 5년 중 싼 쪽이라 자기 이력 {selfsc:.1f}점(싸다)이다. PSR만 중앙값보다 조금 비싸다. '
           'S&P500 경기소비재 안에서는 다섯 배수가 모두 중간~비싼 쪽이라 {peersc:.1f}점(중간)이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”다. 현재가를 정당화하려면 5년 매출 성장이 연 {pct(DCF[\'requiredGrowth\'])}여야 한다(실제 5년 연 {pct(HIST[\'growth_5y\'])}). '
        '배수는 5년 이력보다 낮아졌지만, 영업이익률 11~13%의 소매업 현금흐름으로는 현재가의 절반 정도가 나온다.')
FUND_TIP = '부채비율 {FR[\'debtToEquity\'][\'value\']:.0f}%는 운용리스 부채($11.4B)가 부채에 들어가서다. 당좌비율이 낮은 것은 재고($7.9B)가 유동자산의 절반이라서다. 순이자가 수익이라 이자보상배율은 매기지 않는다. 활동성은 영업순환주기 기준이다.'
SELF_TIP = 'PER {SM[\'PER\'][\'current\']:.1f}배는 5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배보다 낮다. 최근 4분기 EPS에는 관세 환급(2분기 세전이익 순증 $219M)과 카드 수수료 소송 합의 이익(4분기 주당 $0.15)이 들어 있다.'
PEER_TIP = ('S&P500 경기소비재(TJX 제외)와 배수 순위를 매긴 값이다.',
            '자동차·온라인·외식·여행이 섞여 있다. 차트에는 소매 6곳만 보인다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})으로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})로 시작해 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('세 시나리오가 현재가의 {min(DCF[k_] for k_ in (\'low\', \'base\', \'high\')) / px * 100:.0f}~{max(DCF[k_] for k_ in (\'low\', \'base\', \'high\')) / px * 100:.0f}%다. 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}에는 관세 환급·소송 합의 이익이 들어 있다. '
            '운용리스 부채 $11.4B(주당 약 $10)는 영업이익에 임차료가 이미 비용으로 들어 있어 내재가치에서 빼지 않는다(2026-10-03 수정 — 전에는 빼서 기본이 $64.34였고 판정은 같다).')
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('red', '2026년 8월 19일 장 시작 전 — Q2 FY27 실적', '2026-08-19',
     '매출 $15.2B(+5%) · 기존점 +4% · EPS $1.36(관세 환급 제외 $1.22) · 연간 세전이익률·EPS 전망 상향 · 당일 주가 −4.2%', 'q2', 'TJX 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 20일 장 시작 전 — Q1 FY27 실적', '2026-05-20',
     '매출 $14.3B(+9%) · 기존점 +6% · EPS $1.19(+29%) · 연간 기존점·세전이익률·EPS·자사주 전망 상향 · 당일 주가 +5.7%', 'q1', 'TJX 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 25일 장 시작 전 — Q4 FY26 실적', '2026-02-25',
     '기존점 +5% · EPS $1.58(소송 합의 제외 $1.43) · 배당 13% 인상·FY27 자사주 $2.50~2.75B 예정 · 당일 주가 −1.2%', 'q4', 'TJX 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 19일 장 시작 전 — Q3 FY26 실적', '2025-11-19',
     '매출 $15.1B(+7%) · 기존점 +5% · EPS $1.28(+12%) · 연간 전망 상향 · 당일 주가 +0.2%', 'q3', 'TJX 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('네 분기 연속 계획을 웃돌았지만 주가는 1년 새 {CH_TXT}', '실적 상회·주가 하락',
           ['2분기 기존점 매출이 +4%로 회사 계획을 웃돌았고, 관세 환급을 뺀 조정 EPS가 $1.22(+11%)였다.',
            '2분기에 IEEPA 관세 환급 $331M을 받아 세전이익이 순 $219M 늘었고, 3분기에도 추가 환급을 예상한다(금액·시기는 불확실하다고 밝힘).',
            '상반기에 자사주 $1.4B·배당 $1.0B를 돌려줬고, FY28부터 점포 증가율을 4%로 높인다.'],
           '배수는 5년 이력보다 낮아졌지만 현금흐름 모델 기본값은 주당 ${DCF[\'base\']:.2f}로 현재가의 절반 정도다.',
           'Q3 FY27 실적(11월 중순 예상)의 기존점 매출(전망 +2~3%)과 관세 환급.')
BULL = [('꾸준한 성장', '네 분기 모두 기존점 +4~6%, 회사 계획 상회.'),
        ('주주환원', 'FY27 자사주 $2.75~3.0B, 배당 +13%.'),
        ('점포 확대', 'FY28부터 점포 4% 증가, 장기 7,500개.')]
BEAR = [('일회성 이익', '2분기 EPS의 $0.14가 관세 환급.'),
        ('주력 둔화', 'Marmaxx 기존점 +1%(1년 전 +3%).'),
        ('밸류에이션', '현금흐름 기본값이 현재가의 절반 정도.')]
ANALYST = {'rating': 'Buy', 'n': 22, 'nt': 16, 'mean': 170.75, 'median': 175, 'low': 140, 'high': 198, 'sb': 13, 'b': 5, 'h': 4, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-06'

PRE = ["FR = {r_['metric']: r_ for ax_ in FUND['axes'].values() for r_ in ax_['rows']}"]   # 기본적 분석 지표 행(값·점수)
