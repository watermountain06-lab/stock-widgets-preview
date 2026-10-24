# SHW(셔윈윌리엄스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 147(시총 145위). 건축용 도료·코팅(직영 도료 매장, 소비자 브랜드, 산업용 코팅).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-28), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장중 접수, 보도자료는 장 전), 8-K(CFO 은퇴 2025-11-03), StockAnalysis.
# Q3 2026 실적은 10/27 장 전(10/1 회사 공지) — 이 카드는 Q2 기준, 다음 분기는 자동 갱신.
# 엔진 입력(2026-10-22): 영업이익 줄이 없다(OperatingIncomeLoss는 2024-09에 멈춤 — 그대로 두면 현금흐름 모델이 2024-09 최근 4분기 $4,410M을 썼다) →
# build_multiple_history.DERIVED_OPINC(세전 + 이자비용 − 이자수익 − 기타 영업외 수익 = 매출총이익 − 판관비 − 기타 일반비용, Q2 1,230.9). 최근 4분기 $3,992M.
# 차입금 $12,072M(단기 $2,246 + 1년 안 만기 $1,498 + 장기 $8,327) · 현금 $293.5M = 원문. 인수 대금 최근 4분기 $1,155M(2025-10-01 완료한 브라질 Suvinil — 2025-02-15 계약). 본사 매각후리스 금융부채 $816.3M은 nonop_extra 음수(Codex r1).
# 3-for-1 분할 2021-04-01(KNOWN_SPLITS). 4분기 EPS 2025 보도자료 값. 자본이 작아 PBR이 높다(자사주 누적).
BUILD = {}
CIK = '0000089800'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, -1, -2), '적정~고평가'
CO = 'Sherwin-Williams'
S_ = 'https://www.sec.gov/Archives/edgar/data/89800/'
SEC = S_
TENQ = S_ + '000008980026000049/shw-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000008980026000046/shwearningsrelease2q2026.htm', 'q1': S_ + '000008980026000036/shwearningsrelease1q2026.htm',
      'q4': S_ + '000008980026000003/shw2025yeearningsrelease.htm', 'q3': S_ + '000008980025000124/shwearningsrelease3q2025.htm'}
LINKS = {'suvinil': S_ + '000008980025000120/shw-20250925.htm', 'cfo': S_ + '000008980025000128/shw991pressreleasenovember.htm'}
FAIRBAND_TITLE = 'id="shwFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
BB_TAGS = ['PaymentsForRepurchaseOfEquity']   # 현금흐름표 "Treasury stock purchased"(상반기 $1,837.0M) — 기본 태그로 안 낸다(Codex r1 필수)
NONOP_WHAT = '투자'
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-27', 'src': '10/1 회사 공지 — 장 시작 전 발표, 콜 오전 10시(동부)'}
# 고정 문장(숫자 없음). 주택·건설 경기 민감, 합성 영업이익, 계절성, 자사주로 작은 자본.
MODEL_NOTE = ('매출은 주택 도장·리모델링과 건설 경기에 민감하고 봄·여름 분기가 크다. 손익계산서에 영업이익 줄이 없어 세전이익에 이자·기타 영업외 손익을 되돌려 합성했다. '
              '본사 등을 팔고 다시 빌린 거래에서 생긴 금융부채는 차입금 줄에 없어 내재가치에서 따로 뺐다. 자사주 매입으로 자본이 작아 PBR과 부채비율이 높게 나온다.')   # Codex r2
PH = ['LIN', 'APD', 'ECL', 'PPG', 'DD', 'NUE']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '화학·소재 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(SHW 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·포장·건자재가 섞여 있다. 차트에는 화학·코팅·소재 회사 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 도료 매장 3,890.0 + 산업용 코팅 1,913.8 + 소비자 브랜드 983.5 = 6,787.3, 본사 2.0을 더해 6,789.3. 1년 전 3,702.2/1,801.1/809.4, 본사 1.8 → 6,314.5.
SEG = [('도료 매장(Paint Stores)', 3890.0, '#e4002b'), ('산업용 코팅', 1913.8, '#f25c74'), ('소비자 브랜드', 983.5, '#f9b4c0')]
SEG_ADJ = 2.0
SEG_TITLE = '매출 구성 — 사업 부문별'
SEG_ADJ_LABEL = '본사'
# 손 뉴스: 최신 실적(Q2 2026, 7/28)은 news_auto — 뒤 손 항목 없음(9/24 단기 대출 약정은 넣지 않음). 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부, 날짜도 UTC 값): 실적 8-K 2025-10-28T15:05Z·2026-01-29T17:08Z·04-28T15:05Z = 장중 접수(보도자료 장 전) → 같은 날.
# CFO 은퇴 8-K 2025-11-04T02:30Z = 11/3 21:30 → 11/4.
# Suvinil 인수 완료 8-K(2.03·8.01, 접수 2025-10-02T00:25Z = 10/1 20:25 → 10/2)는 뉴스로 — 처음엔 신용 약정으로 잘못 분류(Fable 2026-10-22 필수).
# 넣지 않은 8-K: 신용·대출 약정(2025-11-05·11-17·2026-02-09·06-09·09-29), 주총(4/24).
HEALTH_EXTRA = '이자보상배율은 최근 분기 기준이라 봄·여름 분기 이익이 큰 이 회사는 그 분기에 높게 나온다.'   # 고정 문장(Fable 권장)
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('green', '2026년 4월 28일 — Q1 2026 실적', '2026-04-28',
     '매출 $5.67B(+6.8%) · 희석 EPS $2.15(1년 전 $2.00) · 기존 도료 매장 매출 +2.4%', 'q1', 'Sherwin-Williams 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 29일 — Q4 2025 실적', '2026-01-29',
     '매출 $5.60B(+5.6%) · 희석 EPS $1.92(1년 전 $1.90) · 10월 1일 완료한 브라질 Suvinil 인수가 이 분기부터 반영 · 2025년 매출 $23.57B(+2.1%)·EPS $10.26', 'q4', 'Sherwin-Williams 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 3일 장 마감 뒤 — CFO 은퇴 예고', '2025-11-04',
     'Allen Mistysyn CFO가 2025년 말 물러나고 Benjamin Meisenzahl 재무 담당 부사장이 2026년 1월 1일 CFO를 맡는다', 'cfo', 'Sherwin-Williams 공시 (SEC 8-K)'),
    ('neutral', '2025년 10월 1일 장 마감 뒤 — 브라질 Suvinil 인수 완료', '2025-10-02',
     'BASF의 브라질 건축용 도료 사업(Suvinil·Glasu! 상표)을 $1.15B에 인수 완료(2025년 2월 계약) — 인수 대금은 단기 대출 인출로 마련', 'suvinil', 'Sherwin-Williams 공시 (SEC 8-K)'),
    ('green', '2025년 10월 28일 — Q3 2025 실적', '2025-10-28',
     '매출 $6.36B(+3.2%) · 희석 EPS $3.35(1년 전 $3.18) · 기존 도료 매장 매출 +3.6%', 'q3', 'Sherwin-Williams 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 29, 'nt': 17, 'mean': 385.53, 'median': 395, 'low': 340, 'high': 420, 'sb': 12, 'b': 3, 'h': 14, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(부문 3개, 본사는 SEG_ADJ). 원문 대조: Q2 2026 3,890.0/1,913.8/983.5(본사 2.0), 1년 전 3,702.2/1,801.1/809.4(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "shw:PaintStoresGroupMember": [
   "도료 매장(Paint Stores)",
   "#e4002b"
  ],
  "shw:PerformanceCoatingsGroupMember": [
   "산업용 코팅",
   "#f25c74"
  ],
  "shw:ConsumerBrandsGroupMember": [
   "소비자 브랜드",
   "#f9b4c0"
  ]
 },
 "ignore": []
}
