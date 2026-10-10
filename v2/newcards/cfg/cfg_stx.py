# STX(씨게이트) v2 카드 설정 — _core_fill.py STX. 회계연도는 6월 말~7월 초 금요일(FY2026은 53주, 2026-07-03 종료).
# 출처: SEC XBRL, FY2026 10-K(2026-08-04), 실적 보도자료(Q1~Q4 FY26), 8-K(교환사채 교환 11/13·2/19·5/28, 상환 6/12·9/9), StockAnalysis.
# 엔진 수정 없음. 최신 공시가 10-K라 기본적 분석은 FY2026 연간 기준.
CIK = '0001137789'
CUR, YO, QO = '2026-07-03', '2025-06-27', '2026-04-03'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
RELEASE = {'rev': 3629, 'op': 1559, 'ni': 1294, 'ocf': 1305}   # 보도자료(영업이익률 43.0%)·10-K 현금흐름(연간 3,674 − 앞 세 분기)
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Seagate'
S_ = 'https://www.sec.gov/Archives/edgar/data/1137789/'
SEC = S_
PR = {'q4': S_ + '000113778926000153/stxq42026pressreleasefinan.htm', 'q3': S_ + '000113778926000084/stxq32026pressreleasefinan.htm',
      'q2': S_ + '000113778926000016/stxq22026pressreleasefinan.htm', 'q1': S_ + '000113778925000283/stxq12026pressreleasefinan.htm'}
TENQ = S_ + '000113778926000159/stx-20260703.htm'; TENQ_NAME = 'FY2026 10-K'
PR_CUR = 'q4'   # 최신 분기 보도자료 키
LINKS = {'ex_nov': S_ + '000119312525279125/d76399d8k.htm', 'ex_feb': S_ + '000119312526059681/d112160d8k.htm',
         'ex_may': S_ + '000119312526243110/d106085d8k.htm', 'redeem': S_ + '000119312526268170/d24300d8k.htm',
         'redeem_done': S_ + '000119312526385961/d109585d8k.htm', 'tenk': S_ + '000113778926000159/stx-20260703.htm'}
FAIRBAND_TITLE = 'id="stxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 최근 1년 사이 PER이 38~70배로 넓게 움직여(주가 약 4배) 범위가 넓다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (0, 50), (0, 200)
FCF_SUB = '영업현금흐름 − 설비투자 · 회사 FCF $1.1B'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('니어라인 출하 용량 (FY2026)', '695EB', '+40% · 전체 789EB(1년 전 595EB)')
NEXT = ('10월 하순 예상', '일정 · Q1 FY27 (회사 미확정)'); NEXT_OP = ('10월 하순', 'Q1 FY27 예상')
FY_ENDS, FY_LABEL = ('2026-07-03', '2025-06-27'), 'FY2026'
HEALTH_NOTE = ('차입금은 $3.6B(1년 안 만기 $0.2B + 장기 $3.4B)로 FY2026에 $1.4B 줄었다. 2028년 만기 교환사채를 현금 약 $1.3B와 주식 약 1,260만 주로 교환하고 일부 사채를 사들였다. 결산 뒤 7월 15일에 선순위 사채 $1B를 더 갚았고, 9월에 남은 교환사채도 정리했다(주식 165만 주 추가). '
               '현금은 $1.7B다. 자본이 1년 전 −$0.45B에서 $2.17B로 막 플러스가 돼 부채비율({FR[\'debtToEquity\'][\'value\']:.0f}%)이 높고 PBR이 {SM[\'PBR\'][\'current\']:.0f}배로 크다.')
ACT_REASON = ''
YOY_EXTRA = '데이터센터용 니어라인 하드디스크 수요 · 매출총이익률 52.3%(1년 전 37.4%) · FY2026은 53주(1분기 14주)라 연간·최근 4분기 합이 약 2% 크다(4분기 비교는 13주끼리) · '
SEG = [('하드디스크·스토리지 (단일 부문)', 3629, '#6ebe49')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 단일 부문'
SEG_NOTE = ('씨게이트는 부문이 하나이고, 시장별 비중은 10-Q·10-K에 비율로만 나온다(Q4 분기 비중은 10-K에 없음) · FY2026 연간으로는 데이터센터 80%(1년 전 75%), Edge IoT 20% · 판매 경로는 OEM 81% · '
            '출처: <a href="{TENQ}" target="_blank" rel="noopener">FY2026 10-K 매출 표 (SEC) →</a>')
CAPITAL = [('자사주 매입 (FY2026)', '$0.18B'),
           ('자사주 매입 승인 잔여 (2025년 5월 $5.0B 승인)', '$4.8B'),
           ('배당 (FY2026 지급, 분기 주당 $0.74)', '2025년 10월 약 3% 인상', '$0.63B')]
CHECK_WHEN = '2026년 10월 하순 (예상) · Q1 FY27'
CHECK = ['1분기 가이던스 매출 $4.1B(±$0.1B)·비GAAP EPS $7.30(±$0.20)을 넘는지',
         '매출총이익률(4분기 52.3%)이 더 오르는지, 니어라인 출하 용량',
         'HAMR 기반 Mozaic 제품 비중 확대',
         '교환사채 정리 뒤 주식 수(희석)와 차입금(6월 말 $3.6B, 7월 $1B 상환 뒤 약 $2.6B)']
NONOP_WHAT = '지분 투자'
PH = ['MU', 'SNDK', 'SKHY', 'DELL', 'ANET', 'CSCO']   # WDC·NTAP·HPE는 카드 유니버스에 없음
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {'pbr': 150}, {}
CHART_TITLES = {'per': '스토리지·메모리·하드웨어 PER 비교', 'pbr': '스토리지·메모리·하드웨어 PBR 비교', 'psr': '스토리지·메모리·하드웨어 PSR 비교',
                'pcr': '스토리지·메모리·하드웨어 PCR(FCF) 비교', 'evebitda': '스토리지·메모리·하드웨어 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
FUND_ASOF_NOTE = 'FY2026 10-K (2026-08-04 공시)'
PREMISE = ('주가가 1년 새 약 {ch / 100 + 1:.1f}배가 돼 PER {SM[\'PER\'][\'current\']:.1f}배(흑자였던 {SM[\'PER\'][\'days\']}일 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PSR {SM[\'PSR\'][\'current\']:.1f}배·PCR {SM[\'PCR\'][\'current\']:.0f}배·EV/EBITDA {SM[\'EV/EBITDA\'][\'current\']:.0f}배가 이력 중 가장 비싼 쪽이라 자기 이력 {selfsc:.1f}점(비싸다)이다. PBR만 중간인데 자본이 막 플러스가 된 {SM[\'PBR\'][\'days\']}일 이력이라 뜻이 작다. '
           '카드 유니버스 IT 안에서도 PSR만 중간이고 나머지가 비싼 쪽이라 {peersc:.1f}점(비싸다)이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”다. 영업이익률을 100%로 올려도 현재가에 닿지 않는다(성장으로는 5년간 연 {pct(DCF[\'requiredGrowth\'])}가 필요). '
        '내재가치 기본값이 낮은 것은 5년 매출 성장률이 연 {pct(HIST[\'growth_5y\'])}에 그치고(FY2023 침체 포함) 최근 2년 영업이익률 중앙값이 {pct(HIST[\'margin_2y\'])}로 지금({pct(HIST[\'margin_now\'])})보다 훨씬 낮아서다. 하드디스크는 업황을 크게 타는 사업이라 지금 이익률이 이어질지가 핵심이다.')
FUND_TIP = '최신 공시가 10-K라 FY2026 연간 기준이다. 부채비율 {FR[\'debtToEquity\'][\'points\']}점은 자본이 막 플러스로 돌아서($2.17B) 생긴 값이다. 매출 3년 CAGR {FR[\'revenueCagr\'][\'value\']:.1f}%는 FY2023 침체 바닥에서 잰 값이다. 영업이익 CAGR은 FY2023 적자에서 흑자로 바뀌어 비율을 내지 않는다.'
SELF_TIP = 'PER은 흑자였던 {SM[\'PER\'][\'days\']}일, PBR은 자본이 플러스였던 {SM[\'PBR\'][\'days\']}일만 이력이 있다. PSR {SM[\'PSR\'][\'current\']:.1f}배는 5년 중앙값 {SM[\'PSR\'][\'median\']:.1f}배의 약 {SM[\'PSR\'][\'current\'] / SM[\'PSR\'][\'median\']:.0f}배다.'
PEER_TIP = ('카드 유니버스 IT 종목과 배수 순위를 매긴 값이다.',
            'PBR은 자본이 막 플러스가 된 씨게이트가 비교군 전체에서 가장 높다({SM[\'PBR\'][\'current\']:.0f}배). PSR만 비교군 중간이다.')
STORIES = ['매출이 5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})이 영구성장률 2.5%보다 낮아 5년 내내 2.5%로 두고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '매출이 5년 성장률(연 {pct(HIST[\'growth_5y\'])})로 시작해 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '매출이 3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})로 시작해 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('보수·기본은 이익률을 과거 중앙값(4분기 합산 기준)으로 돌린다. 5년 중앙값 {pct(HIST[\'margin_5y\'])}에는 FY2023 적자가, 2년 중앙값 {pct(HIST[\'margin_2y\'])}에는 FY2024 회복기(영업이익률 6.9%)가 들어 있어 지금 {pct(HIST[\'margin_now\'])}보다 크게 낮다. '
            '“낙관”은 지금 이익률에 3년 성장률(연 {pct(HIST[\'growth_3y\'])}, FY2023 바닥에서 잰 값이라 오히려 높은 쪽)을 쓰는데도 ${DCF[\'high\']:.2f}로 현재가의 {DCF[\'high\'] / px * 100:.0f}%다. 시가총액이 FY2026 FCF $3.1B의 약 {SM[\'PCR\'][\'current\']:.0f}배라 할인율 10%·영구성장 2.5%의 5년 모델로는 닿기 어렵다.')
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 8일 — 교환사채 상환 마무리', None,
     '6월에 상환을 통지한 2028년 만기 교환사채 잔액 약 $150.7M을 정리(교환분은 원금 현금 + 주식 164.8만 주)', 'redeem_done', 'Seagate 공시 (SEC 8-K)'),
    ('neutral', '2026년 7월 28일 장 마감 후 — Q4 FY26 실적', '2026-07-29',
     '매출 $3.63B(+48%) · EPS $5.58·조정 $5.71 · 영업이익률 43.0% · 1분기 가이던스 매출 $4.1B · 다음 날 주가 +2.3%', 'q4', 'Seagate 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 15일 — 선순위 사채 $1B 상환', None,
     '6월 말 결산 뒤 선순위 사채 원금 $1B를 상환(FY2026 10-K 후속 사건)', 'tenk', 'Seagate FY2026 10-K (SEC)'),
    ('neutral', '2026년 5월 28일 — 교환사채 교환', None,
     '2028년 만기 교환사채 $185.9M을 현금 $185.9M과 주식 202만 주로 교환', 'ex_may', 'Seagate 공시 (SEC 8-K)'),
    ('green', '2026년 4월 28일 장 마감 후 — Q3 FY26 실적', '2026-04-29',
     '매출 $3.11B(+44%) · EPS $3.27·조정 $4.10 · FCF $953M · 다음 날 주가 +11.1%', 'q3', 'Seagate 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 19일 — 교환사채 교환', None,
     '2028년 만기 교환사채 $600M을 현금 약 $599M과 주식 595만 주로 교환', 'ex_feb', 'Seagate 공시 (SEC 8-K)'),
    ('green', '2026년 1월 27일 장 마감 후 — Q2 FY26 실적', '2026-01-28',
     '매출 $2.83B(+22%) · EPS $2.60·조정 $3.11 · 매출총이익률·영업이익률 사상 최고 · 다음 날 주가 +19.1%', 'q2', 'Seagate 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 13일 — 교환사채 교환', None,
     '2028년 만기 교환사채 $500M을 현금 약 $503M과 주식 431만 주로 교환', 'ex_nov', 'Seagate 공시 (SEC 8-K)'),
    ('green', '2025년 10월 28일 장 마감 후 — Q1 FY26 실적', '2025-10-29',
     '매출 $2.63B(+21%) · EPS $2.43·조정 $2.61 · 분기 배당 $0.74로 약 3% 인상 · 다음 날 주가 +19.1%', 'q1', 'Seagate 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('AI 데이터센터의 대용량 하드디스크 수요로 매출이 48% 늘고 이익률이 사상 최고를 이어 가, 주가는 1년 새 {CH_TXT}', '초고성장·초고배수',
           ['4분기 매출 $3.63B(+48%), 영업이익률 43.0%(1년 전 23.2%)로 FY2026(53주) 매출이 $12.2B(+34%)였다.',
            'FY2026 FCF $3.1B로 차입금 $1.4B를 갚고 교환사채를 정리했으며 자본이 플러스로 돌아섰다.',
            '1분기 가이던스 매출 $4.1B로 성장이 이어질 전망이다.'],
           '배수는 자기 이력과 IT 비교군 모두에서 비싼 쪽이고, 현금흐름 모델은 지금 이익률을 그대로 이어 가도 현재가의 일부에 그친다.',
           'Q1 FY27 실적(10월 하순 예상)의 매출 $4.1B 달성과 매출총이익률.')
BULL = [('수요', '니어라인 출하 용량 +40%(FY2026 695EB), 매출의 80%가 데이터센터.'),
        ('이익', '4분기 매출총이익률 52.3%, 영업이익률 43.0%로 사상 최고.'),
        ('재무', 'FY2026 FCF $3.1B, 차입금 $1.4B 상환.')]
BEAR = [('밸류', 'PSR {SM[\'PSR\'][\'current\']:.0f}배(5년 중앙값 {SM[\'PSR\'][\'median\']:.1f}배), PER {SM[\'PER\'][\'current\']:.0f}배.'),
        ('업황', 'FY2023 적자를 낸 업황 산업, 이익률 중앙값은 5년 {pct(HIST[\'margin_5y\'])}.'),
        ('희석', '교환사채 정리로 주식 약 1,420만 주 발행(FY2026 약 1,260만 + 9월 165만).')]
ANALYST = {'rating': 'Strong Buy', 'n': 25, 'nt': 19, 'mean': 1124.84, 'median': 1090, 'low': 860, 'high': 1600, 'sb': 18, 'b': 4, 'h': 2, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-10'

PRE = ["FR = {r_['metric']: r_ for ax_ in FUND['axes'].values() for r_ in ax_['rows']}"]   # 기본적 분석 지표 행(값·점수)


# ── 자동 카드(설계 D, 2026-10-11) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose2·3 제안(손 표와 숫자 일치 — 여러 축·나머지 줄) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:ContractWithCustomerSalesChannelAxis",
 "extra": {},
 "members": {
  "stx:OEMsMember": [
   "하드디스크·스토리지 (단일 부문)",
   "#6ebe49"
  ],
  "stx:DistributorsMember": [
   "하드디스크·스토리지 (단일 부문)",
   "#6ebe49"
  ],
  "us-gaap:RetailMember": [
   "하드디스크·스토리지 (단일 부문)",
   "#6ebe49"
  ]
 },
 "ignore": []
}
