# FDS(팩트셋) v2 카드 설정 — 자동 카드(AUTO). 회계연도 8월 말(Q4 FY26 = 2026-06~08). 금융 데이터·분석 구독(지역 3개 부문).
# 출처: SEC XBRL, FY2026 10-K(2026-10-20 07:30 동부 장 전), 실적 보도자료(Q1~Q4 FY26, 8-K 2.02항 — 모두 장 전 07시 무렵 → 같은 날 반응), 8-K(신용 약정 2026-08-31, CFO 교체 2026-04-08). 사전 조사 scratchpad pre/FDS.md.
# 검토(Codex r1 2026-11-05): 현금흐름 −2가 평균 자본효율 0.797배 대체에 기대고 있었다 — 같은 날 엔진 규칙 변경(매출 2% 넘게 늘고 순투자 ≤ 0이면 상한 10)으로 기본 $216(1.58배), −2 그대로.
# 엔진 입력(2026-11-05): 설비투자는 PaymentsToAcquirePropertyPlantAndEquipment(2023-08까지) → PaymentsToAcquireProductiveAssets(FY24부터, 자본화 소프트웨어 포함 한 줄)를 엔진이 잇는다.
# 이자비용은 InterestExpense(2024-02까지) → InterestExpenseNonoperating(손익계산서 줄). 차입 $1,370.0M(2027 채권 $500 유동 + 2032 채권 $500 + 기한부대출 $375), 현금 $233.3M + 단기투자 $32.0M, 운용리스 $172.4M. 기말 뒤 회전신용 $90 차입(10-K 본문, 9월 말 숫자 아님).
CIK = '0001013237'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-08-31', '2025-08-31', '2026-05-31'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
FY_ENDS, FY_LABEL = ('2026-08-31', '2025-08-31'), 'FY2026'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'FactSet'
S_ = 'https://www.sec.gov/Archives/edgar/data/1013237/'
SEC = S_
TENQ = S_ + '000162828026066391/fds-20260831.htm'; TENQ_NAME = 'FY2026 10-K'
PR = {'q4': S_ + '000162828026063888/fdsq42026earningsrelease.htm', 'q3': S_ + '000162828026046338/fdsq32026earningsrelease.htm',
      'q2': S_ + '000162828026022203/fdsq22026earningsrelease.htm', 'q1': S_ + '000162828025057794/fdsq12026earningsrelease.htm'}
LINKS = {'credit': S_ + '000095015726000966/form8-k.htm', 'cfo': S_ + '000095010326005447/dp244995_8k.htm'}
FAIRBAND_TITLE = 'id="fdsFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (15, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 1년 순투자(설비투자 − 감가상각 − 운전자본 감소)가 −$123M으로 음수라, 매출을 늘리는 데 자본이 거의 들지 않은 것으로 보고 최근 자본효율을 상한(투하자본 1달러당 매출 10달러)으로 두었다. 기본 시나리오는 이 값에서 5년 평균(0.8달러)으로 돌아간다. '
              '5년 매출 성장률에는 2022년 CGS 인수가 섞여 있다(회사 유기 성장 6~7%). '
              '동종업 점수는 결제 처리·카드 네트워크까지 넣은 S&P500 결제·거래소·금융 데이터 17곳 기준이다. 차트의 금융 데이터·거래소 6곳만 보면 더 싼 쪽(약 85)이지만 비교군 최소 수(8곳)에 못 미쳐 점수로 쓰지 않는다. '
              'FY2026에는 구조조정(세전 $46M)·CEO 취임 보상($20M)·지분투자 손상(세후 $12M)이 있었다 — 빼고 계산해도 세 표는 같다(자기 이력 76.9, 동종업 64.2).')
PH = ['SPGI', 'MCO', 'MSCI', 'ICE', 'NDAQ', 'CME']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '금융 데이터·거래소 6곳 PER 비교 (점수는 S&P500 결제·거래소·금융 데이터 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 결제·거래소·금융 데이터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 결제·거래소·금융 데이터 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('S&P500 결제 처리·거래소·금융 데이터 18곳 중 FDS를 뺀 17곳과 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 처리·거래소·신용평가가 섞여 있어 성장·마진 구조가 다르다. 차트에는 금융 데이터·거래소 6곳만 보인다.')
# 부문(FY2026 10-K 부문 주석 연간 − Q3 FY26 10-Q 9개월 누계, 보도자료 표와 일치) — Americas 414.3, EMEA 154.8, Asia Pacific 65.6, 합 634.7 = 연결 매출.
SEG = [('미주', 414.3, '#00629b'), ('유럽·중동·아프리카', 154.8, '#3e8ed0'), ('아시아태평양', 65.6, '#a9cbe8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역 부문별(Q4 FY26)'
# 손 뉴스: Q4 FY26 실적(9/30)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤 손 항목은 없다. 가이던스는 쓰지 않는다. 반응일: 모두 장 전 발표 → 같은 날.
NEWS_RANGE = '2025.12 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 8월 31일 장 마감 뒤 — 신용 약정 개정', None,
     '기한부대출 $375M 만기를 2029년 8월로 연장, 회전신용 $1.0B → $1.5B(2031년 8월 만기) — 새 차입은 아니다', 'credit', 'FactSet 공시 (SEC 8-K)'),
    ('green', '2026년 7월 1일 장 전 — Q3 FY26 실적', '2026-07-01',
     '매출 $622.9M(+6.4%) · 희석 EPS $3.50(1년 전 $3.87, 구조조정 세전 $19.6M 포함)', 'q3', 'FactSet 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 8일 장 전 — CFO 교체', '2026-04-08',
     'Helen Shan 퇴임, Joshua Warren(전 Envestnet CFO)이 4월 13일 CFO로', 'cfo', 'FactSet 공시 (SEC 8-K)'),
    ('green', '2026년 3월 31일 장 전 — Q2 FY26 실적', '2026-03-31',
     '매출 $611.0M(+7.1%) · 희석 EPS $3.59(1년 전 $3.76)', 'q2', 'FactSet 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 12월 18일 장 전 — Q1 FY26 실적', '2025-12-18',
     '매출 $607.6M(+6.8%) · 희석 EPS $4.06(1년 전 $3.89)', 'q1', 'FactSet 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Hold', 'n': 18, 'nt': 13, 'mean': 274.54, 'median': 290, 'low': 212, 'high': 340, 'sb': 3, 'b': 0, 'h': 9, 's': 2, 'ss': 4}
ANALYST_ASOF = '2026-11-05'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-K 부문 주석 FY26 1,617.4/605.3/253.5, 4분기 = 연간 − Q3 10-Q 9개월(414.3/154.8/65.6)(2026-11-05) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "fds:AmericasSegmentMember": [
   "미주",
   "#00629b"
  ],
  "fds:EMEASegmentMember": [
   "유럽·중동·아프리카",
   "#3e8ed0"
  ],
  "fds:AsiaPacificSegmentMember": [
   "아시아태평양",
   "#a9cbe8"
  ]
 },
 "ignore": []
}
