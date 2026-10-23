# GM(제너럴 모터스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 164(시총 163위). 자동차(북미·해외), 금융 자회사 GM Financial.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-20 밤 접수 → 첫 세션 10/21), 실적 보도자료(Q3 2025~Q3 2026, 8-K 2.02항 — 보도자료는 장 전, 8-K는 장중 접수), 8-K(EV 손상 2.06항 2025-10-14, EV 비용 2026-01-08), StockAnalysis.
# 엔진 입력(2026-10-22): 차입금은 자동차 부문만(CAT·DE와 같은 규칙, 2026-09-30 사용자 결정) — 재무상태표가 gm:BusinessGroupAxis로만 실어 BUILD dim_facts
# (overlay DebtCurrentAutoGm·LongTermDebtAutoGm) + DEBT_TOTAL_TAG. Q3 2026 $15,799M(GM Financial $112,944M 제외). 현금·시장성 증권은 연결 값(CAT 선례).
# 감가상각에는 GM Financial 운용리스 차량 감가상각이 들어 있다(9개월 $3.9B) — EBITDA가 그만큼 크다(CAT·DE와 같은 처리). 이자비용은 자동차 부문 차원 값뿐이라 이자보상배율은 빠진다(안건 E36).
# 4분기 EPS 2024·2025 보도자료 값(EV 관련 비용으로 두 해 모두 적자).
BUILD = {'dim_facts': [('us-gaap:DebtCurrent', 'gm:BusinessGroupAxis', 'gm:AutomotiveMember', 'DebtCurrentAutoGm'),
                       ('us-gaap:LongTermDebtAndCapitalLeaseObligations', 'gm:BusinessGroupAxis', 'gm:AutomotiveMember', 'LongTermDebtAutoGm')]}
CIK = '0001467858'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -1), '적정'
CO = 'GM'
S_ = 'https://www.sec.gov/Archives/edgar/data/1467858/'
SEC = S_
TENQ = S_ + '000146785826000059/gm-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000146785826000056/gmq32026pressreleaseandfin.htm', 'q2': S_ + '000146785826000049/gmq22026pressreleaseandfin.htm',
      'q1': S_ + '000146785826000033/gmq12026pressreleaseandfin.htm', 'q4': S_ + '000146785826000011/gmq42025pressreleaseandfin.htm',
      'q3_25': S_ + '000146785825000141/gmq32025pressreleaseandfin.htm'}
LINKS = {'ev1': S_ + '000146785825000136/gm-20251007.htm', 'ev2': S_ + '000146785826000005/gm-20260108.htm'}
FAIRBAND_TITLE = 'id="gmFairBand" title="최근 1년 PER 25~75% 구간 × 최근 4분기 희석 EPS. 최근 4분기 EPS에 EV 관련 비용(Q4 2025)이 들어 있어 이 범위는 참고용이다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-10, 15)
ACT_REASON = ''
NONOP_WHAT = '투자'
YOY_NOTE = {'2026-09-30': '최근 4분기에는 Q4 2025 EV 생산 능력 축소 비용 약 $6.0B(그 밖에 중국 합작 구조조정 등 비EV 비용 약 $1.1B)가 들어 있다 — EV 비용만 빼도 최근 4분기 영업이익률은 2.3%가 아니라 약 5.5%다. 이 비용 때문에 보고 PER이 높아져 있다'}   # Fable r1 필수
# 고정 문장(숫자 없음). 금융 자회사, 리스 차량 감가상각, EV 비용.
MODEL_NOTE = ('차입금은 자동차 부문 빚만 넣었다 — GM Financial의 차입금은 할부·리스 채권과 짝을 이룬 영업 자금이라 뺀다(CAT·디어와 같은 규칙). '
              '감가상각에는 GM Financial이 빌려준 리스 차량의 감가상각이 들어 있어 EBITDA가 크게 나오고 EV/EBITDA는 낮게 보인다. '
              '보수 시나리오가 기본보다 높은 것은 보수가 5년 중앙 이익률을, 기본은 최근 2년 중앙값을, 낙관은 지금 이익률을 쓰는데 최근 이익률에 일회성 비용이 들어 있기 때문이다. '
              '순현금은 연결 현금·증권(GM Financial 몫 포함)에서 자동차 부문 빚만 뺀 값이라 회사 전체의 무차입 여력이 아니다. 최근 4분기 이익에는 EV 생산 능력을 줄이며 생긴 대규모 일회성 비용이 들어 있다.')   # Codex r1 필수
HEALTH_EXTRA = '이자보상배율이 빈 것은 회사가 공시하지 않아서가 아니다 — 손익계산서의 자동차 부문 이자비용이 부문 축이 붙은 태그로만 실려 엔진이 읽지 못한다.'   # 고정 문장(Codex r1 필수, 안건 E36)
PH = ['F', 'TSLA', 'APTV', 'BWA', 'LKQ', 'GPC']   # 미국 상장·10-Q 제출 회사만(TM·STLA·HMC는 20-F라 자료 없음)
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '자동차·부품 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': '자동차 PBR 비교', 'psr': '자동차 PSR 비교',
                'pcr': '자동차 PCR(FCF) 비교', 'evebitda': '자동차 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(GM 제외)와 배수 순위를 매긴 값이다.',
            '유통·외식·호텔·의류·자동차가 섞여 있어 자동차 회사는 배수가 늘 낮게 나온다 — 높은 점수가 곧 저평가를 뜻하지는 않는다. 차트에는 자동차·부품 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 북미 41,419 + 해외 4,085 + GM Financial 4,312 + 본사 201 = 50,017, 부문 간 제거 −2 → 50,015. 1년 전 40,551·3,645·4,337·60.
SEG = [('북미(GMNA)', 41419.0, '#0b4da2'), ('GM Financial', 4312.0, '#5f95dd'), ('해외(GMI)', 4085.0, '#06306a')]
SEG_ADJ = 199   # 본사 201 − 부문 간 제거 2(차트에는 세 부문만)
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 5건(EPS는 GAAP 희석, 조정 EPS·가이던스는 쓰지 않는다), EV 비용 공시 2건.
# 반응일: 실적 보도자료는 동부 오전 6~7시대 배포(장 전), 8-K 접수 2025-10-21T15:38Z·2026-01-27T17:25Z·04-28T15:25Z·07-21T15:14Z·10-20T15:30Z = 장중 → 모두 같은 날.
# EV 손상 8-K 2025-10-14T14:15Z(장중) → 10/14. EV 비용 8-K 2026-01-09T02:02Z(1/8 동부 21:02) → 1/9.
# 넣지 않은 8-K: 신용 약정(3/23·8/11 공급업체 금융 프로그램), 이사 불출마(5/26), 주총(6/4).
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 20일 — Q3 2026 실적 · 자사주 $20B 승인', '2026-10-20',
     '매출 $50.0B(+2.9%) · 희석 EPS $3.73(1년 전 $1.35 — EV 비용 $1.6B 반영 분기) · 1월 $6.0B 자사주 매입 완료, 새 $20.0B 다년 매입 승인', 'q3', 'GM 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 21일 — Q2 2026 실적', '2026-07-21',
     '매출 $48.0B(+1.9%) · 희석 EPS $1.41(1년 전 $1.91)', 'q2', 'GM 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 — Q1 2026 실적', '2026-04-28',
     '매출 $43.6B(−0.9%) · 희석 EPS $2.82(1년 전 $3.35) · 대법원 IEEPA 관세 판결로 약 $0.5B 유리한 조정', 'q1', 'GM 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 27일 — Q4 2025 실적 · 배당 인상', '2026-01-27',
     '매출 $45.3B(−5.1%) · 희석 EPS −$3.60(1년 전 −$1.64) — EV 관련 비용 반영 · 분기 배당 20% 인상($0.18), 자사주 $6.0B 승인', 'q4', 'GM 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 8일 — EV 비용 약 $6.0B 예고', '2026-01-09',
     'EV 생산 능력·투자 재검토로 Q4 2025에 약 $6.0B 비용(비현금 손상 약 $1.8B, 공급업체 정산·계약 해지 등 약 $4.2B) 계상 예정 · 중국 사업 구조조정 등 비EV 비용 약 $1.1B도', 'ev2', 'GM 공시 (SEC 8-K)'),
    ('green', '2025년 10월 21일 — Q3 2025 실적', '2025-10-21',
     '매출 $48.6B(−0.3%) · 희석 EPS $1.35(1년 전 $2.68) — EV 관련 비용 $1.6B 반영', 'q3_25', 'GM 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 14일 — EV 손상 $1.6B 공시', '2025-10-14',
     '미국 EV 세액공제 종료·규제 완화로 EV 수요 둔화 예상 — Q3 2025에 북미 EV 생산 능력 재편 비용 $1.6B', 'ev1', 'GM 공시 (SEC 8-K 2.06항)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 20, 'mean': 105.15, 'median': 105, 'low': 76, 'high': 132, 'sb': 13, 'b': 7, 'h': 4, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'

# ── 자동 카드 — 부문 3개(본사 201은 다른 축 조합이라 SEG_ADJ). 원문 대조: Q3 2026 41,419/4,312/4,085, 1년 전 40,551/4,337/3,645(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:Revenues"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "gm:GMNorthAmericaMember": [
   "북미(GMNA)",
   "#0b4da2"
  ],
  "gm:GMFinancialSegmentMember": [
   "GM Financial",
   "#5f95dd"
  ],
  "gm:GMIMember": [
   "해외(GMI)",
   "#06306a"
  ]
 },
 "ignore": []
}

# 템플릿 문구 보정(Codex r2): 이자보상배율 상세 행·순현금 문장의 범위
POST = [r'''
h = h.replace('"note": "그 분기 이자비용 미공시", "label": "이자보상배율"', '"note": "자동차 부문 이자비용 추출 미지원(부문 축 태그)", "label": "이자보상배율"')
h = h.replace('현금·단기투자가 차입금·리스보다 $10.7B 많다(순현금).', '현금·단기투자가 차입금·리스보다 $10.7B 많다(순현금 — 연결 현금에서 자동차 부문 빚만 뺀 값).')
''']

