BUILD = {'overlay': True, 'no_dcf': '손해보험사라 현금흐름 모델을 쓰지 않는다', 'company_tags': [('acgl:IncomeLossFromContinuingOperationsBeforeEarningsFromAffiliatesIncomeTaxesNoncontrollingInterest', 'PretaxBeforeAffiliatesAcgl')]}   # 10-Q 세전이익은 회사 고유 태그(관계사 손익 제외) — 표시용 영업이익에만 쓴다   # CB·PGR과 같은 방식(2026-10-02 사용자 결정)
# ACGL(아치 캐피털 그룹) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 전문 손해보험·재보험·모기지 보험 3부문, 버뮤다 법인.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-04 16:06 동부 장 마감 뒤 → 첫 세션 11-05 — 카드는 11-05 장중 가격으로 만들고 매일 실행이 종가로 고친다), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 모두 16시대 장 마감 뒤 → 다음 거래일). 사전 조사 scratchpad pre/ACGL.md.
# 엔진 입력(2026-11-05): 차입 = 선순위채 SeniorLongTermNotes $4,286M(DEBT_TOTAL_TAG — 기본 차입 태그 없음), 현금 $1,152M, 단기투자 $3,253M은 보험 운용자산이라 뺌, 우선주 $830M(비누적, Series F·G). 비지배지분 0(태그 경고는 2022 낡은 값).
# PBR은 엔진이 우선주 $830M을 뺀 보통주 자본 $22,162M으로 계산한다(Codex r1 — 처음 주석은 반대로 썼다). D&A 줄이 없어 EV/EBITDA는 계산 불가.
NO_DCF_SKEW = True   # 금융 카드 — 현금흐름 칸 쏠림 메모(A0) 없음
CIK = '0000947484'
OP_DISPLAY = (['PretaxBeforeAffiliatesAcgl'], [(['InterestExpense'], 1)])   # 카드 표시용 영업이익 = 세전이익(관계사 손익 제외, 회사 고유 태그) + 이자비용 — 10-K의 us-gaap 세전(관계사 포함)과 섞지 않는다
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Arch Capital'
S_ = 'https://www.sec.gov/Archives/edgar/data/947484/'
SEC = S_
TENQ = S_ + '000094748426000152/acgl-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000094748426000128/ex-991release93026.htm', 'q2': S_ + '000094748426000118/ex-991release63026.htm', 'q1': S_ + '000094748426000051/ex-991release33126.htm', 'q4': S_ + '000094748426000010/ex-991release123125.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="acglFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (현금흐름 미적용)</span>'
Y2 = (0, 40)
ACT_REASON = '보험사라 재고·매출채권 회전으로 보는 활동성이 맞지 않는다'
NONOP_WHAT = '투자'
PH = ['CB', 'TRV', 'WRB', 'EG', 'CINF', 'HIG']
PEER_FILE = 'peer_universe/insurers.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '보험 6곳 PER 비교 (점수는 S&P500 보험사 기준)', 'pbr': '보험 PBR 비교', 'psr': '보험 PSR 비교',
                'pcr': '보험 PCR(FCF) 비교', 'evebitda': '보험 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 보험사(손해·종합·생명)보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 보험사 대비 배수 순위 (v2/peer_universe/insurers.json)'
PEER_TIP = ('S&P500 손해·종합·생명보험 15곳(ACGL 제외)과 배수 순위를 매긴 값이다.', '생명보험사는 장부가·매출 구조가 달라 PBR·PSR 비교가 거칠다. 차트에는 손해보험 6곳만 보인다.')
MODEL_NOTE = ('보험사라 현금흐름 내재가치는 계산하지 않아 판정 보류다(자기 이력·동종업 점수는 참고). 3분기 합산비율은 82.5%(재해·전기 준비금 제외 81.2%)이고 부문별로 보험 94.4%, 재보험 78.3%, 모기지 25.5%다. '
              'PBR은 우선주 $830M을 뺀 보통주 자본 기준이다. 2026년 1분기 실효세율은 버뮤다·영국 세법 변경으로 8.6%에 그쳤다. 3분기 손해에는 이란 분쟁 관련 손실이 들어 있다.')
SEG = [('보험(순경과보험료)', 1937, '#00539b'), ('재보험', 1807, '#6c96c8'), ('모기지 보험', 270, '#b5cbe5')]
SEG_ADJ = 641   # 순투자수익 451 − 실현손실 99 + 기타 인수수익 61 + 지분법 224 + 기타 4
SEG_TITLE = '매출 구성 — 부문별 순경과보험료(Q3 2026)'
# 손 뉴스: 실적 4건(보통주 순이익, 희석 EPS, 세후 영업 EPS). 반응일: 장 마감 뒤 → 다음 거래일.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 27일 장 마감 뒤 — Q3 2026 실적', '2026-10-28',
     '보통주 순이익 $1,025M · 희석 EPS $3.00(1년 전 $3.56) · 영업 EPS $2.67 · 합산비율 82.5% — 다음 날 주가 +2.2%', 'q3', 'Arch Capital 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 28일 장 마감 뒤 — Q2 2026 실적', '2026-07-29',
     '보통주 순이익 $1,047M · 희석 EPS $3.00(1년 전 $3.23) · 영업 EPS $2.56 — 다음 날 주가 −1.8%', 'q2', 'Arch Capital 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 28일 장 마감 뒤 — Q1 2026 실적', '2026-04-29',
     '보통주 순이익 $1,037M · 희석 EPS $2.88(1년 전 $1.48) · 영업 EPS $2.50 — 다음 날 주가 −4.5%', 'q1', 'Arch Capital 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 9일 장 마감 뒤 — Q4 2025 실적', '2026-02-10',
     '보통주 순이익 $1,228M · 희석 EPS $3.35(1년 전 $2.42) · 영업 EPS $2.98 — 다음 날 주가 +1.9%', 'q4', 'Arch Capital 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 15, 'mean': 111, 'median': 110, 'low': 95, 'high': 125, 'sb': 7, 'b': 2, 'h': 10, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-05'


POST = [r"""
h = h.replace('</span> 종가 기준</span>', '</span> 장중 기준</span>', 1)   # 10-Q가 11-04 장 마감 뒤라 11-05 장중 가격으로 만들었다 — 매일 실행이 종가로 고친다(2026-11-05)
h = h.replace('보통주 배당 없음', '정기 보통주 배당 없음(9개월 현금 지급 $5M)').replace('<span class="zone-label">보통주 배당 지급</span>\n          <span class="zone-val">없음</span>', '<span class="zone-label">보통주 배당 지급</span>\n          <span class="zone-val">정기 배당 없음</span>').replace('최근 4분기 영업이익의', '최근 4분기 추정 영업이익(세전 + 이자)의')
h = h.replace('부문 간 거래·조정 +$', '순투자수익·지분법·기타 수익 +$')   # Codex r1 2026-11-05
"""]


# ── 자동 카드 — 부문 지도(손 작성: 제안기는 매출 태그만 찾는다. 원문 PremiumsEarnedNet × 부문 축 1,937/1,807/270, 2026-11-05) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:PremiumsEarnedNet"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "acgl:InsuranceSegmentMember": [
   "보험(순경과보험료)",
   "#00539b"
  ],
  "acgl:ReinsuranceSegmentMember": [
   "재보험",
   "#6c96c8"
  ],
  "acgl:MortgageSegmentMember": [
   "모기지 보험",
   "#b5cbe5"
  ]
 },
 "ignore": []
}
