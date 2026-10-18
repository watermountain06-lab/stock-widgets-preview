# ICE(인터컨티넨탈 익스체인지) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 124(시총 122위). 거래소(NYSE·ICE 선물)·청산, 채권·데이터, 모기지 기술.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 시작 전 접수), 8-K(Polymarket 투자 2025-10-07,
# MarketAxess 인수 계약 2026-07-29, 선순위채 발행 2026-08-20), StockAnalysis.
# 엔진 입력(2026-10-18): 차입금 = ShortTermBorrowings + LongTermDebtNoncurrent — 재무상태표 "Short-term debt" 한 줄을 세 태그(LongTermDebtCurrent·CommercialPaper 포함)로
# 내 기본 합이 $1,218M을 세 번 더했다($22,282M 대 $19,846M, DEBT_TOTAL_TAG). 단기투자 태그는 2017년에 멈춰 뺐다(EV_TAGS_BY_CIK sti []).
# 비영업 자산: 비시장성 지분 $2,386M(Polymarket 우선주 약 $2.0B 등, 엔진 기본) + 지분법 투자 $499M(OCC 40% 등 — 이익이 영업외, nonop_extra.json 태그).
# 청산 증거금·보증기금($114.6B)은 자산·부채에 같은 금액으로 맞물린 통과 잔액이라 현금·차입금에 넣지 않는다(엔진 기본 — CME와 같다).
# 매출은 GAAP 총매출(Total revenues) — 회사가 앞세우는 "거래 관련 비용 차감 매출"(Section 31 수수료·유동성 지급분을 뺀 값, Q2 $2,666M)보다 크다.
# 4분기 EPS: 2023년만 보도자료 값($0.65, 역산 $0.64).
CIK = '0001571949'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, None, -2), '적정~고평가'
CO = 'Intercontinental Exchange'
S_ = 'https://www.sec.gov/Archives/edgar/data/1571949/'
SEC = S_
TENQ = S_ + '000157194926000011/ice-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000110465926088462/tm2621213d1_ex99-1.htm', 'q1': S_ + '000110465926052145/tm2612824d1_ex99-1.htm',
      'q4': S_ + '000110465926010646/tm264989d1_ex99-1.htm', 'q3': S_ + '000110465925104017/tm2529550d1_ex99-1.htm'}
LINKS = {'mktx': S_ + '000119312526324909/d116245dex991.htm', 'notes': S_ + '000119312526359229/d124897d8k.htm',
         'poly': S_ + '000094787125000890/ss5432176_8k.htm'}
FAIRBAND_TITLE = 'id="iceFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (20, 60)
ACT_REASON = ''
NONOP_WHAT = '비상장 지분·지분법 투자'
# 고정 문장(숫자 없음 — 분기마다 고치지 않는다). 현금흐름 모델이 이 회사에 맞지 않는 점과 매출 정의(Fable 필수 2026-10-18).
MODEL_NOTE = ('투하자본의 대부분이 과거 인수에서 생긴 영업권·무형자산이라 이 모델은 매출 1달러를 늘리는 데 큰 재투자가 든다고 본다. 감가상각의 큰 몫이 인수 무형자산 상각이라 '
              '최근 1년 순투자가 음수여서 한계 효율을 정의하지 못하고 평균 비율을 쓴다 — 실제 FCF보다 훨씬 작은 현금흐름을 가정한 값이다. '
              '매출은 GAAP 총매출(거래 관련 비용 차감 전)이라 SEC 요율에 따라 0이 되기도 하는 통과 항목 Section 31 수수료가 들어 있어, 성장률·영업이익률·PSR이 회사가 앞세우는 순매출 기준과 다르다.')
HEALTH_EXTRA = '유동비율·부채비율·총자산증가율에는 청산 증거금·보증기금(회원 예치금 — 자산과 부채에 같은 금액)이 들어 있어, 실제 지급능력보다 나쁘게 나오거나 크게 흔들린다.'
PH = ['CME', 'NDAQ', 'CBOE', 'SPGI', 'MCO', 'MSCI']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '거래소·금융 데이터 6곳 PER 비교', 'pbr': '거래소·금융 데이터 PBR 비교', 'psr': '거래소·금융 데이터 PSR 비교',
                'pcr': '거래소·금융 데이터 PCR(FCF) 비교', 'evebitda': '거래소·금융 데이터 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 결제·거래소 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 결제·거래소 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('S&P500 결제·거래소·금융 데이터(ICE 제외)와 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 처리·거래소·신용평가·지수 회사가 섞여 있다. 비교할 값이 있는 회사가 적은 배수는 점수에서 빠진다. 차트에는 거래소·금융 데이터 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문 표, 총매출) — 거래소 2,409 + 채권·데이터 645 + 모기지 기술 557 = 3,611(연결 총매출). 거래 관련 비용 945는 거래소 부문 몫.
SEG = [('거래소', 2409, '#1b3d6d'), ('채권·데이터', 645, '#4f7fb8'), ('모기지 기술', 557, '#8fb3dc')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 보고 부문별(총매출)'
# 손 뉴스: 8/20 선순위채 발행(MarketAxess 인수 자금)을 넣으므로 Q2 실적(7/30)도 손으로 쓴다(README). 가이던스·조정 EPS는 쓰지 않는다.
# 반응일: 실적 8-K는 모두 동부 07:30 무렵 접수(장 시작 전) → 같은 날. MarketAxess 8-K 7/30 07:32 → 7/30. 선순위채 8-K 8/20 16:22 → 8/21.
# Polymarket 8-K 2025-10-07 17:05 → 10/8.
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 20일 장 마감 뒤 — 선순위채 $3.75B 발행', '2026-08-21',
     '2029·2031·2033·2036년 만기 4종(연 4.70~5.40%) · 순수입 약 $3.71B는 MarketAxess 인수 대금 등에 · 카드의 차입금(6/30 기준 $19.8B)에는 아직 없다', 'notes', 'Intercontinental Exchange 공시 (SEC 8-K)'),
    ('neutral', '2026년 7월 30일 — MarketAxess 인수 계약', '2026-07-30',
     '주당 현금 $167(7/29 종가 대비 33% 할증) · 지분 가치 약 $6.0B, 기업가치 약 $5.7B · 2027년 상반기 완료 예정(MarketAxess 주주·규제 승인 조건) · 최대 $6.25B 브리지 대출 약정', 'mktx', 'Intercontinental Exchange 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 30일 — Q2 2026 실적', '2026-07-30',
     '매출 $3.61B(+10.7%) · 희석 EPS $1.69(1년 전 $1.48)', 'q2', 'Intercontinental Exchange 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 30일 — Q1 2026 실적', '2026-04-30',
     '매출 $3.67B(+13.5%) · 희석 EPS $2.48(1년 전 $1.38) · 영업외 기타 수익 $411M(비상장 지분 평가이익 포함)', 'q1', 'Intercontinental Exchange 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 5일 — Q4 2025 실적', '2026-02-05',
     '매출 $3.14B(+3.7%) · 희석 EPS $1.49(1년 전 $1.21) · 2025년 매출 $12.64B·EPS $5.77', 'q4', 'Intercontinental Exchange 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 30일 — Q3 2025 실적', '2025-10-30',
     '매출 $3.01B(−0.9%) · 희석 EPS $1.42(1년 전 $1.14)', 'q3', 'Intercontinental Exchange 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 7일 장 마감 뒤 — Polymarket 투자 계약', '2025-10-08',
     '예측 시장 Polymarket에 최대 $2B 투자 · ICE가 Polymarket 데이터를 전 세계에 배포', 'poly', 'Intercontinental Exchange 공시 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 16, 'nt': 15, 'mean': 185.4, 'median': 180, 'low': 160, 'high': 243, 'sb': 8, 'b': 5, 'h': 2, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-18'


# ── 자동 카드 — 부문 지도: seg_map_propose 1판은 매출 종류 축(ProductOrServiceAxis — 채권·데이터가 us-gaap:TechnologyServiceMember)을 골랐지만,
# 같은 값이 보고 부문 축에도 있어 그쪽으로 연결. 원문 대조: 10-Q 부문 표 Q2 2026 2,409/645/557, 1년 전 2,134/597/531 = 연결 총매출(2026-10-18) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "ice:ExchangesSegmentMember": [
   "거래소",
   "#1b3d6d"
  ],
  "ice:FixedIncomeAndDataServicesSegmentMember": [
   "채권·데이터",
   "#4f7fb8"
  ],
  "ice:MortgageTechnologySegmentMember": [
   "모기지 기술",
   "#8fb3dc"
  ]
 },
 "ignore": []
}
