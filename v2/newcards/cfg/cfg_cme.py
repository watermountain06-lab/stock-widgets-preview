# CME(CME 그룹) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 114.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-24), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 시작 전 접수), 8-K(CEO 승계 2026-06-17), StockAnalysis.
# 엔진 입력(2026-10-16): 차입금은 UnsecuredLongTermDebt($3,424.2M — 기본 목록이 단기차입 0만 잡아 0이었다, DEBT_TOTAL_TAG). 감가상각은 손익계산서
# "Depreciation and amortization"(10-Q Depreciation·10-K DepreciationAndAmortization을 한 구성요소로) + "Amortization of purchased intangibles"(DDA_PARTS_BY_CIK —
# 분기 TTM이 2019년에 멈춰 EV/EBITDA 계산 불가였다). 이자비용은 InterestAndDebtExpense(vendor/fetch_financials CONCEPTS_BY_CIK). 비지배지분 태그는 2021년에 멈춰 nci = [].
# 청산 증거금·보증기금($158.1B)은 자산·부채에 같은 금액으로 맞물린 통과 잔액이라 현금·차입금에 넣지 않는다(엔진 기본 태그가 이미 뺀다).
# 증거금 운용 투자수익과 회원 지급분은 영업이익 아래(영업외)라 현금흐름 가치에 들어가지 않는다. S&P Dow Jones Indices 지분 장부가 $1.4B(FY2025 10-K)는
# 지분법 이익이 영업이익 아래라 비영업 자산(v2/nonop_extra.json, 연간 갱신).
NI_TAGS = ['ProfitLoss', 'NetIncomeLoss']   # 분기 순이익을 2025년 2분기 전까지 ProfitLoss(손익계산서 'Net Income', 비지배지분 없음)로만 냈다
CIK = '0001156375'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, None, -2), '고평가'
CO = 'CME Group'
S_ = 'https://www.sec.gov/Archives/edgar/data/1156375/'
SEC = S_
TENQ = S_ + '000115637526000047/cme-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000115637526000042/exhibit9916302026.htm', 'q1': S_ + '000115637526000016/exhibit9913312026.htm',
      'q4': S_ + '000115637526000006/exhibit991123125.htm', 'q3': S_ + '000115637525000204/exhibit9919302025.htm'}
LINKS = {'ceo': S_ + '000119312526273442/d129556d8k.htm'}
FAIRBAND_TITLE = 'id="cmeFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (40, 80)
ACT_REASON = ''
BB_TAGS = ['StockRepurchasedDuringPeriodValue']   # 현금흐름표 'Repurchase of Class A common stock'($1,236.9M 상반기)를 PaymentsForProceedsFromDerivativeInstrumentFinancingActivities로 잘못 태깅 — 자본변동표 값이 같다
NONOP_WHAT = 'S&P 다우존스 지수 지분'
PH = ['ICE', 'NDAQ', 'CBOE', 'SPGI', 'MCO', 'MSCI']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '거래소·금융 데이터 6곳 PER 비교', 'pbr': '거래소·금융 데이터 PBR 비교', 'psr': '거래소·금융 데이터 PSR 비교',
                'pcr': '거래소·금융 데이터 PCR(FCF) 비교', 'evebitda': '거래소·금융 데이터 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 결제·거래소 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 결제·거래소 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('S&P500 결제·거래소·금융 데이터(CME 제외)와 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 처리·거래소·신용평가·지수 회사가 섞여 있다. 비교할 값이 있는 회사가 적은 배수는 점수에서 빠진다. 차트에는 거래소·금융 데이터 6곳만 보인다.')
# 매출(Q2 2026 10-Q 손익계산서) — 청산·거래 수수료 1,352.5 + 시장 데이터 238.1 + 기타 115.6 = 1,706.2(연결 매출, 단일 부문).
SEG = [('청산·거래 수수료', 1352.5, '#1a6fb0'), ('시장 데이터', 238.1, '#439ee3'), ('기타', 115.6, '#9a9a9a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 매출 종류별(단일 부문)'
# 손 뉴스: Q2 2026 실적(7/22)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤 손 항목(9/9 재무·법무 임원 선임)은 넣지 않았다(README). 가이던스는 쓰지 않는다.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('red', '2026년 6월 17일 — CEO 승계 결정', '2026-06-17',
     'Terrence Duffy(의장·CEO)는 상근 의장으로, Lynne Fitzpatrick(사장·CFO)이 CEO — 2027년 3월 1일과 2026년 10-K 제출일 중 늦은 날부터', 'ceo', 'CME Group 공시 (SEC 8-K)'),
    ('green', '2026년 4월 22일 — Q1 2026 실적', '2026-04-22',
     '매출 $1.88B(+14%) · 희석 EPS $3.18(1년 전 $2.62)', 'q1', 'CME Group 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 4일 — Q4 2025 실적', '2026-02-04',
     '매출 $1.65B(+8%) · 희석 EPS $3.24(1년 전 $2.40) · 2025년 매출 $6.5B(+6%)·EPS $11.16', 'q4', 'CME Group 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 22일 — Q3 2025 실적', '2025-10-22',
     '매출 $1.54B(−3%) · 희석 EPS $2.49(1년 전 $2.50)', 'q3', 'CME Group 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Hold', 'n': 17, 'nt': 13, 'mean': 283.77, 'median': 285, 'low': 218, 'high': 337, 'sb': 4, 'b': 4, 'h': 6, 's': 2, 'ss': 1}
ANALYST_ASOF = '2026-10-16'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-Q 손익계산서 Q2 2026 1,352.5/238.1/115.6, 1년 전 1,388.0/198.1/105.9 = 연결 매출.
# 같은 축의 증거금 이자(InterestFromPerformanceBonds, 1,388.8)는 영업외 투자수익이라 ignore(2026-10-16) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:Revenues"
 ],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {
  "cme:ClearingandtransactionfeesMember": [
   "청산·거래 수수료",
   "#1a6fb0"
  ],
  "cme:MarketDataMember": [
   "시장 데이터",
   "#439ee3"
  ],
  "cme:OtherRevenueMember": [
   "기타",
   "#9a9a9a"
  ]
 },
 "ignore": [
  "cme:InterestFromPerformanceBondsMember"
 ]
}
