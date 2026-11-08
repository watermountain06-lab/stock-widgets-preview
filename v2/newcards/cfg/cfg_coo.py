CIK = '0000711404'
# COO(쿠퍼 컴퍼니즈) v2 카드 설정 — 자동 카드(AUTO). 회계연도 10월 31일. 콘택트렌즈(CooperVision) + 여성 건강·불임 치료(CooperSurgical).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-09-09 16:48 동부 장 마감 뒤 → 첫 세션 09-10, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 16:2x~16:4x 동부 → 다음 날),
#        전략 검토 시작(2025-12-04)·Browning West 협력 합의(2025-12-23)·전략 검토 종료(2026-09-09)·CEO 퇴임(2026-10-27 16:36 동부 → 10-28).
# 보류 목록 D군(안건 E54) — 2026-11-07 사용자 결정: 서로 상쇄되는 일회성은 순액으로 30%를 본다 → 정식 판정(GAAP + 문장).
# 엔진 입력(2026-11-07): 이자비용 InterestExpenseNonoperating(InterestExpense는 2024-04에 멈춤), 4분기 EPS는 보도자료 GAAP 희석 EPS(Q4_EPS_OVERRIDE 2021·2024·2025 — 2021은 4:1 분할 반영 값).
# 일회성: 최근 4분기 GAAP 희석 EPS 2.93(0.43 + 0.66 − 0.40 + 2.24) 대 조정 4.61(1.15 + 1.10 + 1.21 + 1.15). 차이 대부분은 매 분기 반복되는 인수 무형자산 상각 등이고,
#   일회성은 Q2 FY26 배아 배양액 리콜 소송 충당 순 $271.6M(세전 — 부채 $324.1M − 보험 회수 예상 $52.5M, 10-Q 누계 $272.0M·세금 효과 $40.9M)과 Q3 FY26 영국 세무조사 종결 세금 이익 $307.2M — 세후 순 약 $76.1M, 주당 약 $0.39(약 13%, Codex r1).
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-10-31', '2024-10-31'), 'FY2025'
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'The Cooper Companies'
S_ = 'https://www.sec.gov/Archives/edgar/data/711404/'
SEC = S_
TENQ = S_ + '000162828026061160/coo-20260731.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000162828026061155/cooperq32026pressrelease.htm', 'q2': S_ + '000162828026040823/cooperq22026pressrelease.htm',
      'q1': S_ + '000162828026015231/cooperq12026pressrelease.htm', 'q4': S_ + '000162828025055405/cooperq42025pressrelease.htm',
      'review': S_ + '000162828026061155/cooperq32026pressreleaseex.htm', 'ceo': S_ + '000119312526434317/d141889dex991.htm',
      'bw': S_ + '000119312525331117/d96045dex991.htm', 'review0': S_ + '000162828025055405/cooperq42025pressreleaseex.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="cooFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-10, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 GAAP 이익에는 서로 반대 방향의 큰 일회성 두 개가 들어 있다 — 2026 회계연도 2분기에 CooperSurgical 배아 배양액 리콜(2023년 12월) 소송을 끝내려고 잡은 충당금 순 $271.6M(세전, 보험 회수 예상 $52.5M 차감)과, '
              '3분기에 영국 세무조사가 유리하게 끝나 생긴 세금 이익 $307.2M이다(별도로 2014년 Sauflon 인수 관련 영국 급여세 분쟁은 2026년 3월 1심 판정이 대체로 영국 국세청 쪽이었고 회사가 항소 중이며, 추정 손실(최대 약 £72M과 이자)은 장부에 잡지 않았다). 소송 비용의 세금 효과($40.9M)까지 넣어 세후로 합치면 이익 쪽으로 약 $76M, 주당 약 $0.39(최근 4분기 GAAP EPS의 약 13%)라 GAAP 그대로 쓴다. 회사 조정 EPS(최근 4분기 약 $4.61)와의 나머지 차이에는 인수 무형자산 상각(최근 4분기 약 $192M, 주당 약 $1)과 사업 재편·철수 비용, 회사 내 자산 이전에 따른 반복 세금 조정이 섞여 있다. '
              '소송 충당금은 영업비용이라 현금흐름 모델의 출발점인 최근 4분기 영업이익률을 약 6%p 낮추고, 기본 시나리오는 그 뒤 2년 중앙값 이익률로 회복한다고 봐 영향이 줄어든다(실효세율이 음수라 모델은 세율 21%를 대신 쓴다). 현금흐름 칸이 낮은 것은 인수로 쌓인 영업권·무형자산이 커서 투하자본 대비 수익률이 낮게 잡히기 때문이기도 하다. 2025년 12월 시작한 전략 검토에서 CooperSurgical 매각을 검토했지만 2026년 9월 보유하기로 결론 내고 자사주 매입 한도를 $2B에서 $3B로 늘렸다. 10월 27일 CEO가 물러나 이사 Walt Rosebrough가 집행 의장으로 선임됐고 후임 CEO를 찾는 중이다(회사는 연간 전망 유지). '
              '동종업 점수는 S&P500 헬스케어 기준이다.')
PH = ['ALGN', 'BAX', 'BDX', 'MDT', 'STE', 'ZBH']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '의료기기 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(COO 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·보험이 섞여 있다. 차트에는 의료기기 6곳만 보인다.')
# 매출(Q3 FY26 보도자료 부문): CooperVision 717.0 + CooperSurgical 349.2 = 1,066.2.
SEG = [('CooperVision(콘택트렌즈)', 717.0, '#00205b'), ('CooperSurgical(여성 건강·불임)', 349.2, '#00a3ad')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(Q3는 전략 검토 종료와 같은 날 — 손 항목으로 합침) + CEO 퇴임 + 전략 검토 시작·협력 합의. 반응일: 장 마감 뒤 → 다음 날.
NEWS_RANGE = '2025.12 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 27일 장 마감 뒤 — CEO 퇴임', '2026-10-28',
     'Al White CEO 퇴임, 이사 Walt Rosebrough 집행 의장 · 후임 CEO 탐색 · 이사회 개편 · 2026 회계연도 전망 유지 — 다음 날 주가 −0.8%', 'ceo', 'CooperCompanies 보도자료 (SEC 8-K)'),
    ('red', '2026년 9월 9일 장 마감 뒤 — Q3 FY26 실적·전략 검토 종료', '2026-09-10',
     '매출 $1.07B(+1%) · GAAP 희석 EPS $2.24(영국 세금 이익 $307.2M 포함) · 조정 EPS $1.15(+4%) · 연간 조정 EPS 전망 $4.58~4.66 → $4.51~4.55, 매출 전망 $4.23~4.25B로 하향 · 미국 유통 재고 축소로 CooperVision 정체 · CooperSurgical 매각 대신 보유(비호르몬 IUD 경쟁 제품 등장·소송 합의로 가치가 낮게 평가됨), 자사주 한도 $3B로 확대 — 다음 날 주가 −14.7%', 'q3', 'CooperCompanies 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 6월 4일 장 마감 뒤 — Q2 FY26 실적', '2026-06-05',
     '매출 $1.08B(+8%) · GAAP 희석 EPS −$0.40(배아 배양액 리콜 소송 충당 순 $271.6M) · 조정 EPS $1.21(+26%) · 연간 매출 전망 소폭 하향, 조정 EPS 전망 유지 — 다음 날 주가 +8.6%', 'q2', 'CooperCompanies 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 5일 장 마감 뒤 — Q1 FY26 실적', '2026-03-06',
     '매출 $1.02B(+6%) · GAAP 희석 EPS $0.66 · 조정 EPS $1.10(+20%) · 연간 이익·현금흐름 전망 상향 — 다음 날 주가 −4.6%', 'q1', 'CooperCompanies 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 23일 장 마감 뒤 — 투자사 Browning West와 협력 합의', '2025-12-24',
     'Walt Rosebrough를 2026년 1월 3일부터 이사로 영입(2026년 말까지 의장 선임을 검토하기로) — 다음 날 주가 −0.4%', 'bw', 'CooperCompanies 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 4일 장 마감 뒤 — Q4 FY25 실적·전략 검토 시작', '2025-12-05',
     '매출 $1.07B(+5%) · GAAP 희석 EPS $0.43 · 조정 EPS $1.15(+11%) · 새 이사회 의장(Colleen Jay, 2026년 1월 2일부터)·공식 전략 검토 시작 — 다음 날 주가 +5.7%', 'q4', 'CooperCompanies 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 17, 'nt': 13, 'mean': 64.54, 'median': 61, 'low': 58, 'high': 75, 'sb': 3, 'b': 3, 'h': 11, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 지도(손 작성 — 10-Q에 같은 부문 멤버가 대소문자 두 표기로 있고 매출은 소문자 표기(Coopervision·Coopersurgical)에 붙는다).
#    원문 대조: Q3 FY26 보도자료 717.0 + 349.2 = 1,066.2(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"coo:CoopervisionSegmentMember": ["CooperVision(콘택트렌즈)", "#00205b"], "coo:CoopersurgicalSegmentMember": ["CooperSurgical(여성 건강·불임)", "#00a3ad"]},
 "ignore": []
}
