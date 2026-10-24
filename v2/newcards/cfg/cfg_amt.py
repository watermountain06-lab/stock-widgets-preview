# AMT(아메리칸 타워) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 135(시총 133위). 통신탑 리츠(미국·중남미·유럽·아프리카), 데이터센터(CoreSite).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-28), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항), 8-K(DISH 불이행 2026-01-28·계약 해지 2026-06-04, 배당 2025-12-04·2026-03-05), StockAnalysis.
# 사업 매각(중단사업 재작성) 경로 — 2024-09-12 인도 사업(ATC TIPL) 매각 완료. EMR 방식(README "사업 매각"): RESTATED_LATEST(재작성 값), 자기 이력 창 2025-02-25부터
# (계속사업 분기·연간 재작성 값이 처음 함께 나온 FY2024 10-K — HISTORY_START), 현금흐름 성장 이력은 2023년 말 최근 4분기 합부터(HISTORY_WINDOW), EPS는 계속사업 EPS(없으면 희석).
# 엔진 입력(2026-10-21): 차입금 $37,190M(1년 안 $5,226.5 + 장기 $31,963.1 — 금융리스 포함) = 원문. 단기투자(2019년)·우선주(2014년) 태그는 멈춘 값이라 뺌, 리스는 운용리스
# ($7,790M; 금융리스 $14.4M은 차입금 표 안이라 build_dcf.FL_IN_DEBT로 한 번만). 비지배지분 $6,533M(Stonepeak 등)은 엔진 기본. 4분기 EPS: 2025는 보도자료 $1.75.
BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # 계속사업 EPS, 2026년 분기는 중단사업이 없어 희석만 태깅(EMR과 같다)
CIK = '0001053507'
NI_TAGS = ['NetIncomeLossFromContinuingOperationsAvailableToCommonShareholdersBasic', 'NetIncomeLossAvailableToCommonStockholdersBasic']   # 분기 순이익: 계속사업 귀속(2024~2025, 인도 중단사업 제외), 2026년부터는 중단사업이 없어 보통주 귀속만 — NetIncomeLoss 태그 없음
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'American Tower'
S_ = 'https://www.sec.gov/Archives/edgar/data/1053507/'
SEC = S_
TENQ = S_ + '000105350726000133/amt-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q1': S_ + '000105350726000094/pressreleaseq12026.htm', 'q4': S_ + '000105350726000032/pressreleaseq42025.htm',
      'q3': S_ + '000105350725000147/pressreleaseq32025.htm'}
LINKS = {'dish_term': S_ + '000105350726000127/amt-20260602.htm', 'dish_def': S_ + '000105350726000026/amt-20260128.htm',
         'div': S_ + '000105350726000041/amt-20260305.htm'}
FAIRBAND_TITLE = 'id="amtFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 60)
# 다음 실적일: 2026-09-29 Business Wire 공지 — 10/27 오전 7시(동부) 발표, 8시 30분 콜(Codex r1)
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-27', 'src': '9/29 회사 공지 — 장 시작 전(오전 7시)'}
ACT_REASON = '매출원가 합계 표준 태그가 없음(리츠 — 부동산 운영비를 따로 공시)'
NONOP_WHAT = '장기 투자'
SELF_SPAN = '인도 사업을 뺀 재작성 값이 갖춰진 2025-02부터'   # 자기 이력 창 — 길이(년)는 쓰지 않는다
GROWTH_SPAN = '인도 사업을 뺀 계속사업 재작성 이력(2023-12 이후)'   # 역산 설명의 '지난 5년' 자리
# 고정 문장(숫자 없음). 리츠에 일반 기업 모델(EQIX·PLD·WELL 선례).
MODEL_NOTE = ('리츠에 일반 기업용 모델을 그대로 쓴 참고 값이다 — 현금흐름 내재가치는 영업이익·재투자 모델이라 리츠의 FFO·AFFO 기반 평가가 아니고, '
              '차입금과 비지배지분(데이터센터·유럽 사업의 외부 지분)을 빼면 주주 몫이 작게 남는다.')
PH = ['CCI', 'SBAC', 'EQIX', 'DLR', 'PLD', 'WELL']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '통신탑·데이터센터·리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '통신탑·리츠 PBR 비교', 'psr': '통신탑·리츠 PSR 비교',
                'pcr': '통신탑·리츠 PCR(FCF) 비교', 'evebitda': '통신탑·리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(AMT 제외)과 배수 순위를 매긴 값이다.',
            '통신탑·데이터센터·물류·주거·의료 리츠와 부동산 서비스가 섞여 있다. 차트에는 통신탑·데이터센터·리츠 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문 주석 — 부문 매출) — 미국·캐나다 부동산 1,274.4 + 아프리카·아태 415.3 + 유럽 259.4 + 중남미 441.6 + 데이터센터 297.1 + 서비스 61.3 = 2,749.1(연결).
# 1년 전 1,307.1/336.3/232.7/389.4/261.9/99.5 → 2,626.9.
SEG = [('미국·캐나다 통신탑', 1274.4, '#0f4c81'), ('중남미', 441.6, '#4a90c8'), ('아프리카·아태', 415.3, '#7fb3de'), ('데이터센터(CoreSite)', 297.1, '#f2a33a'),
       ('유럽', 259.4, '#a9c9e8'), ('서비스(미국)', 61.3, '#9ca3af')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 사업 부문별'
# 손 뉴스: 최신 실적(Q2 2026, 7/28)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤 손 항목 없음(9월 회사채·이사 선임은 넣지 않음). 가이던스·조정 이익·AFFO는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K는 모두 장중 접수(보도자료는 장 전) — Q1 4/28 15:04 → 4/28, Q4 2/24 17:05 → 2/24, Q3 10/28 15:04 → 10/28.
# DISH 해지 8-K 6/5 00:39(=6/4 20:39) → 6/5, DISH 불이행 1/29 02:22(=1/28 21:22) → 1/29, 배당 3/6 02:22(=3/5 21:22) → 3/6.
# 넣지 않은 8-K: 회사채 발행·상환(2025-12·2026-05·06·09), 신용 약정 개정(5/7), 임원·이사(11/7·1/29·2/27·3/10·9/18), 주총(5/21).
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 6월 4일 장 마감 뒤 — DISH와의 장기 임대 계약 해지', '2026-06-05',
     'DISH Wireless와 2021년 맺은 전략적 공동 사용 계약(SCA)을 6월 2일부로 해지 통보 · 2026년 1월부터 DISH 매출 전액을 이미 이탈(churn)로 반영해 이번 해지로 실적 전망은 바뀌지 않는다고 밝힘 · 10-Q: 6월 15일 손해배상 청구에 모회사 EchoStar 추가, 6월 30일 DISH 파산보호(챕터 11) 신청 · 계약상 임대료 인상분을 넘는 이탈로 2분기 매출 $24.6M 순감소(주로 DISH) · DISH는 2025년 전체 부동산 매출의 약 2%, 미국·캐나다의 약 4%', 'dish_term', 'American Tower 공시 (SEC 8-K)·Q2 2026 10-Q'),
    ('green', '2026년 4월 28일 — Q1 2026 실적', '2026-04-28',
     '매출 $2.74B(+7%) · 희석 EPS $1.84(1년 전 계속사업 $1.04)', 'q1', 'American Tower 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 5일 장 마감 뒤 — 분기 배당 $1.79', '2026-03-06',
     '직전 분기 $1.70에서 5.3% 인상 · 4월 28일 지급', 'div', 'American Tower 공시 (SEC 8-K)'),
    ('neutral', '2026년 2월 24일 — Q4 2025 실적', '2026-02-24',
     '매출 $2.74B(+7%) · 계속사업 희석 EPS $1.75(1년 전 $2.62) · 2025년 매출 $10.64B·계속사업 EPS $5.40', 'q4', 'American Tower 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 28일 장 마감 뒤 — DISH 지급 불이행', '2026-01-29',
     'DISH Wireless가 전략적 공동 사용 계약(SCA)의 지급 의무를 지키지 않아 계약 불이행 상태 · 2025년 실적에는 영향 없다고 밝힘', 'dish_def', 'American Tower 공시 (SEC 8-K)'),
    ('green', '2025년 10월 28일 — Q3 2025 실적', '2025-10-28',
     '매출 $2.72B(+8%) · 계속사업 희석 EPS $1.82(1년 전 $0.89)', 'q3', 'American Tower 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 25, 'nt': 17, 'mean': 214.82, 'median': 210, 'low': 188, 'high': 248, 'sb': 15, 'b': 7, 'h': 3, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-21'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(보고 부문 축 6개, 부문 매출). 부동산 소계(PropertyMember)는 ignore.
# 원문 대조: Q2 2026 1,274.4/441.6/415.3/297.1/259.4/61.3, 1년 전 1,307.1/389.4/336.3/261.9/232.7/99.5, Q1 2026·Q4 2025도 같은 지도로 값이 나옴(2026-10-21) ──
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
  "amt:PropertyUSAndCanadaMember": [
   "미국·캐나다 통신탑",
   "#0f4c81"
  ],
  "amt:PropertyLatinAmericaMember": [
   "중남미",
   "#4a90c8"
  ],
  "amt:PropertyAfricaAPACMember": [
   "아프리카·아태",
   "#7fb3de"
  ],
  "amt:PropertyDataCentersMember": [
   "데이터센터(CoreSite)",
   "#f2a33a"
  ],
  "amt:PropertyEuropeMember": [
   "유럽",
   "#a9c9e8"
  ],
  "amt:ServicesSegmentMember": [
   "서비스(미국)",
   "#9ca3af"
  ]
 },
 "ignore": [
  "amt:PropertyMember"
 ]
}
