# ROST(로스 스토어스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 1월 말 전후 토요일 마감, 이름은 시작한 해(FY2026 = 2026-02 ~ 2027-01, HD와 같은 꼴). 카드 순위 148(시총 146위).
# 할인 의류·잡화 매장(Ross Dress for Less, dd's DISCOUNTS). 출처: SEC XBRL, Q2 FY2026 10-Q(2026-09-01), 실적 보도자료(Q3 FY25~Q2 FY26, 8-K 2.02항 — 모두 장 마감 뒤 접수), 8-K(이사회 의장 승계 2025-11-24), StockAnalysis.
# 엔진 입력(2026-10-22): 손익계산서 영업이익 줄(OperatingIncomeLoss)은 2023년부터만 → build_multiple_history.DERIVED_OPINC(세전 − 순이자수익, TJX와 같은 방식, Q2 1,103.6 = 태그).
# 그 전엔 현금흐름 이력이 비어 build_dcf_block이 멈췄다. 차입금 $1,019M · 현금 $4,288M · 운용리스 $3,721M(임차료가 영업이익에 이미 비용이라 내재가치에서 빼지 않음).
# 이자보상배율: vendor/fetch_financials CONCEPTS_BY_CIK — 장기차입 이자(기본 후보는 기타 $0.35M 한 줄만 잡아 3,153배였다, Codex r1 필수).
# Q2 FY26 영업이익에 IEEPA 관세 환급 약 $253M(EPS 약 $0.60)이 들어 있다 — 최근 4분기 이익률이 그만큼 부풀어 있다(뉴스·MODEL_NOTE).
# 데이터 창(2020~) 안 분할 없음. 4분기 EPS: FY23 $1.82·FY24 $1.79 보도자료와 일치, FY22 $1.30은 연간 − 9개월 역산(보도자료 미확인).
BUILD = {}
CIK = '0000745732'
CUR, YO, QO = '2026-08-01', '2025-08-02', '2026-05-02'
QLABEL, YL, QQL = 'Q2 FY26', 'Q2 FY25', 'Q1 FY26'
L8 = ['Q3 FY24', 'Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26']
FY_ENDS, FY_LABEL = ('2026-01-31', '2025-02-01'), 'FY25'
FY_NAME_OFFSET = -1
VOTES, VERDICT = (-1, 1, -2), '적정~고평가'
CO = 'Ross Stores'
S_ = 'https://www.sec.gov/Archives/edgar/data/745732/'
SEC = S_
TENQ = S_ + '000074573226000041/rost-20260801.htm'; TENQ_NAME = 'Q2 FY26 10-Q'
PR = {'q2': S_ + '000074573226000038/q226exhibit991.htm', 'q1': S_ + '000074573226000025/q126exhibit991.htm',
      'q4': S_ + '000074573226000003/q4fy25exhibit991.htm', 'q3': S_ + '000074573225000055/q325exhibit991.htm'}
LINKS = {'chair': S_ + '000074573225000058/balmuth-9912.htm'}
FAIRBAND_TITLE = 'id="rostFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 최근 4분기 EPS에는 2분기 관세 환급 이익이 들어 있다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 관세 환급 일회성, 합성 영업이익, 운용리스.
MODEL_NOTE = ('최근 분기 영업이익에 일회성 관세 환급이 들어 있어, 최근 4분기 이익률에서 출발하는 세 시나리오와 현금흐름이 모두 그만큼 높게 계산된다. '   # Codex r1 권장
              '예전 손익계산서에 영업이익 줄이 없어 세전이익에서 순이자수익을 빼 이력을 이었다. 매장 임차료는 영업이익에 이미 비용으로 들어 있어 운용리스 부채는 빼지 않는다.')
PH = ['TJX', 'HD', 'LOW', 'TSCO', 'ULTA', 'BBY']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소매 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': '소매 PBR 비교', 'psr': '소매 PSR 비교',
                'pcr': '소매 PCR(FCF) 비교', 'evebitda': '소매 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(ROST 제외)와 배수 순위를 매긴 값이다.',
            '자동차·온라인·외식·여행이 섞여 있다. 차트에는 소매 6곳만 보인다.')
# 매출(Q2 FY26 10-Q) — 단일 부문, 품목별은 비율로만 공시(STX와 같은 처리). 6,264.9, 1년 전 5,529.2.
SEG = [('할인 매장 매출 (단일 부문)', 6264.9, '#0047ba')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 단일 부문'
SEG_NOTE = '로스는 부문이 하나이고, 품목별 비중은 10-Q·10-K에 비율로만 나온다.'
# 손 뉴스: 최신 실적(Q2 FY26, 8/20)도 손으로 — 관세 환급을 적으려고. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부, 날짜도 UTC 값): 실적 8-K 2025-11-21T02:03Z·2026-03-04T02:03Z·05-22T00:02Z·08-21T00:11Z = 장 마감 뒤 → 다음 날.
# 의장 승계 8-K 2025-11-25T02:08Z = 11/24 21:08 → 11/25. 넣지 않은 8-K: 주총(5/27), 이사 교체(9/17).
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 20일 장 마감 뒤 — Q2 FY26 실적 · 관세 환급', '2026-08-21',
     '매출 $6.26B(+13%) · 기존점 +10% · 희석 EPS $2.66(1년 전 $1.56) — IEEPA 관세 환급 약 $253M(EPS 약 $0.60) 포함', 'q2', 'Ross Stores 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 21일 장 마감 뒤 — Q1 FY26 실적', '2026-05-22',
     '매출 $6.01B(+21%) · 기존점 +17% · 희석 EPS $2.02(1년 전 $1.47)', 'q1', 'Ross Stores 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 3일 장 마감 뒤 — Q4 FY25 실적', '2026-03-04',
     '매출 $6.64B(+12%) · 기존점 +9% · 희석 EPS $2.00(1년 전 $1.79) · FY2025 매출 $22.8B·EPS $6.61 · 2년 $2.55B 자사주 매입 승인', 'q4', 'Ross Stores 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 24일 장 마감 뒤 — 이사회 의장 승계', '2025-11-25',
     'Michael Balmuth 집행 의장이 2026년 1월 말 물러나고 Gunnar Bjorklund 선임 사외이사가 2월 1일 의장을 맡는다', 'chair', 'Ross Stores 공시 (SEC 8-K)'),
    ('green', '2025년 11월 20일 장 마감 뒤 — Q3 FY25 실적', '2025-11-21',
     '매출 $5.60B(+10%) · 기존점 +7% · 희석 EPS $1.58(1년 전 $1.48)', 'q3', 'Ross Stores 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 15, 'mean': 270.27, 'median': 272, 'low': 234, 'high': 298, 'sb': 12, 'b': 2, 'h': 5, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 손으로(단일 부문: 매출 개념 하나, 축 없음). 원문 대조: Q2 FY26 6,264.9, 1년 전 5,529.2(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax": [
   "할인 매장 매출 (단일 부문)",
   "#0047ba"
  ]
 },
 "ignore": []
}
