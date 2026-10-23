# TEL(TE 커넥티비티) v2 카드 설정 — 자동 카드(AUTO). 회계연도 9월 마지막 금요일(FY26 = 2025-09-27 ~ 2026-09-25). 카드 순위 173. 커넥터·센서(운송·산업 — 데이터센터 포함), 아일랜드 법인.
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-06-26 분기, 7/24 장중 접수), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 보도자료 장 전, 8-K 장중), StockAnalysis.
# 엔진 입력(2026-10-23): 차입금 = 단기 102 + 장기 5,530 = $5,632M(DEBT_TOTAL_TAG), 비지배지분 = 상환 가능 $147M(EV_TAGS_BY_CIK). EPS는 계속사업 희석(BUILD eps_tag — 4분기 역산이 중단사업과 섞이지 않게).
BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}
# 안건 E48: 자본 = 비지배지분 포함 자본 − nci라 상환 가능 비지배지분 $147M이 두 번 빠진다(DCF 영향 몇십 센트, Codex r2) — 엔진 공통이라 100장 뒤.
CIK = '0001385157'
CUR, YO, QO = '2026-06-26', '2025-06-27', '2026-03-27'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-09-26', '2024-09-27'), 'FY25'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'TE Connectivity'
S_ = 'https://www.sec.gov/Archives/edgar/data/1385157/'
SEC = S_
TENQ = S_ + '000110465926086509/tel-20260626x10q.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000110465926085589/tel-20260722xex99d1.htm', 'q2': S_ + '000110465926046285/tel-20260422xex99d1.htm',
      'q1': S_ + '000110465926005219/tel-20260121xex99d1.htm', 'q4': S_ + '000110465925103388/tel-20251029xex99d1.htm'}
LINKS = {'iday': S_ + '000110465925114450/tm2531643d1_ex99-1.htm'}
FAIRBAND_TITLE = 'id="telFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
YOY_NOTE = {'2026-06-26': '최근 4분기 EPS에는 Q2 FY26 과거 세금 문제 정산에 따른 세금 혜택 주당 약 $0.39가 들어 있다 — 빼면 최근 4분기 EPS 약 $9.82, PER 약 21배'}   # Fable r1 필수
# 고정 문장(숫자 없음). 운송(자동차) 경기 민감, 데이터센터·에너지 수요.
MODEL_NOTE = ('매출의 절반은 자동차 등 운송, 절반은 데이터센터·에너지·자동화 같은 산업 쪽이다. 운송 쪽은 자동차 생산 경기에, 산업 쪽은 데이터센터 투자에 따라 성장 속도가 갈린다. '
              'EPS는 계속사업 기준이다. 7월에 합의한 Astrodyne TDI 인수(현금)는 아직 숫자에 없다.')
PH = ['APH', 'ANET', 'DELL', 'CSCO', 'TXN', 'QCOM']   # 비교 자료(카드 유니버스 IT)에 값이 있는 종목만
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '전자 부품·하드웨어·반도체 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(TEL 제외)과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 섞여 있어 성장률이 높은 종목이 많다 — 부품 회사는 배수가 낮게 나와 점수가 높아진다. 차트에는 전자 부품·하드웨어·반도체 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 부문) — 운송 2,580 + 산업 2,580 = 5,160. 1년 전 2,418·2,116.
SEG = [('운송 솔루션', 2580.0, '#f28d00'), ('산업 솔루션(데이터센터·에너지 등)', 2580.0, '#f7b866')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 계속사업 희석 — 조정 EPS·가이던스는 쓰지 않는다).
# 반응일: 실적 보도자료 장 전 배포, 8-K 접수 UTC 2025-10-29T14:10Z·2026-01-21T16:17Z·04-22T14:09Z·07-22T14:40Z = 장중 → 같은 날.
# 넣지 않은 8-K: 회사채(2/9), 신용 약정(2/17), 주총(3/11), 이사 은퇴(10/7).
NEWS_RANGE = '2025.10 ~ 2026.07'
# 투자자 행사 8-K 2025-11-20T19:16Z(장중) → 11/20. 다음 실적: 10/7 회사 공지 — 10/28 장 전, 오전 8시 30분(동부) 콜.
NEXT_CONFIRMED = {'quarter_end': '2026-09-25', 'date': '2026-10-28', 'src': '10/7 회사 공지 — 장 시작 전 발표, 콜 오전 8시 30분(동부)'}
NEWS = [
    ('red', '2026년 7월 22일 — Q3 FY26 실적 · Astrodyne TDI 인수 합의', '2026-07-22',
     '매출 $5.16B(+14%, 유기 +12%) · 계속사업 희석 EPS $2.55(+19%) · 전력 부품 회사 Astrodyne TDI를 현금 약 $1.4B에 인수 합의(산업 부문, 연매출 $250M 이상, 미완료)', 'q3', 'TE Connectivity 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 22일 — Q2 FY26 실적', '2026-04-22',
     '매출 $4.74B(+15%, 유기 +7%) · 계속사업 희석 EPS $2.90(과거 세금 정산 혜택 주당 약 $0.39 포함, 1년 전 $0.04 — 세금 비용 분기) · 영업이익률 20%', 'q2', 'TE Connectivity 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 21일 — Q1 FY26 실적', '2026-01-21',
     '매출 $4.7B(+22%, 유기 +15%) · 계속사업 희석 EPS $2.53(+45%)', 'q1', 'TE Connectivity 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 20일 — 투자자 행사(사업 계획)', '2025-11-20',
     '두 부문 사업 계획과 중기 목표 발표(8-K 7.01, 장중 접수)', 'iday', 'TE Connectivity 발표 자료 (SEC 8-K)'),
    ('green', '2025년 10월 29일 — Q4 FY25 실적', '2025-10-29',
     '매출 $4.75B(+17%, 유기 +11%) · 계속사업 희석 EPS $2.23(+148%)', 'q4', 'TE Connectivity 실적 보도자료 (SEC 8-K)'),
]
# 템플릿 보정(Codex·Fable r1): 1년 전 분기 배당은 지급 기준 $0.71(선언 태그가 없어 '없음'으로 나왔다)
POST = [r'''
h = h.replace('1년 전 배당 없음', '1년 전 $0.71(지급 기준)')
''']
ANALYST = {'rating': 'Buy', 'n': 19, 'nt': 11, 'mean': 247.09, 'median': 235, 'low': 215, 'high': 290, 'sb': 12, 'b': 1, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-23'

# ── 자동 카드 — 부문 2개(손으로 — seg_map_propose가 두 부문 값이 같아 판정 못 함). 원문 대조: Q3 FY26 2,580/2,580, 1년 전 2,418/2,116(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "tel:TransportationSolutionsMember": [
   "운송 솔루션",
   "#f28d00"
  ],
  "tel:IndustrialSolutionsMember": [
   "산업 솔루션(데이터센터·에너지 등)",
   "#f7b866"
  ]
 },
 "ignore": []
}
