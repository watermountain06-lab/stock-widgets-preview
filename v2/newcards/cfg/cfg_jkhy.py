# JKHY(잭 헨리) v2 카드 설정 — 자동 카드(AUTO). 회계연도 6월 말(Q4 FY26 = 2026-04~06). 지역 은행·신협용 코어 뱅킹·결제 처리 — 부문 Core·Payments·Complementary·Corporate Services.
# 출처: SEC XBRL, FY2026 10-K(2026-08-28 장 마감 뒤 → 첫 세션 08-31), 실적 보도자료(Q1 FY26~Q1 FY27, 8-K 2.02항 — 모두 16시대 장 마감 뒤 → 다음 거래일). 사전 조사 scratchpad pre/JKHY.md.
# Q1 FY27 10-Q는 아직 없다(실적은 11-03 발표) — 카드는 FY2026 10-K 기준이고 새 10-Q는 매일 실행 auto_approve가 반영한다(2026-11-05 사용자 결정).
# 엔진 입력(2026-11-05): 현금은 10-K가 제한 현금 포함 합계 태그로만 내서(제한 현금 0) EV_TAGS 튜플로 잇는다. 감가상각 = Depreciation + AdjustmentForAmortization(DDA_PARTS, 합산 태그 없음),
# 이자비용 InterestExpenseOperating(CONCEPTS_BY_CIK — 2023-12 뒤). 설비투자는 PP&E $67.1M만(엔진 공통 정의) — 자본화 소프트웨어 $184.2M·구입 소프트웨어 $4.1M은 빠져 PCR이 낮게 나온다.
# 일회성 시험(scratchpad jkhy_e54/, 최근 4분기만 깎은 제한 시험): 디컨버전 영업이익 $30M + 항공기 매각 이익 $6.8M을 빼면(EPS 6.98 → 6.62) 자기 80.8·동종업 54.3·현금흐름 −2.
# 디컨버전을 과거 이력에서도 빼면 자기 81.7, 자본화 소프트웨어를 설비투자에 넣어도 현금흐름 기본 $95.35(−2) — 표 불변(Fable r1).
CIK = '0000779152'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
FY_ENDS, FY_LABEL = ('2026-06-30', '2025-06-30'), 'FY2026'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Jack Henry'
S_ = 'https://www.sec.gov/Archives/edgar/data/779152/'
SEC = S_
TENQ = S_ + '000077915226000067/jkhy-20260630.htm'; TENQ_NAME = 'FY2026 10-K'
PR = {'q4': S_ + '000077915226000057/jkhy-20260630xex99pressrel.htm', 'q3': S_ + '000077915226000021/jkhy-20260331xex99pressrel.htm',
      'q2': S_ + '000077915226000007/jkhy-20251231xex99pressrel.htm', 'q1': S_ + '000077915225000090/jkhy-20250930xex99pressrel.htm'}
LINKS = {'fy27q1': S_ + '000077915226000095/jkhy-20260930xex99pressrel.htm'}
FAIRBAND_TITLE = 'id="jkhyFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (15, 35)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('카드 재무는 FY2026 10-K(6월 말) 기준이다. 11월 3일 발표한 Q1 FY27 실적(매출 +8.8%, 희석 EPS $2.28)과 올린 연간 전망은 10-Q가 접수되면 자동으로 반영된다. '
              '매출에는 고객이 다른 시스템으로 옮길 때 받는 디컨버전 수수료가 분기마다 들쭉날쭉 들어 있다(FY26 $42.8M) — 회사는 조정 매출에서 뺀다. '
              '설비투자에 자본화 소프트웨어(FY26 $184M)가 들어 있지 않아(엔진 공통 정의) 잉여현금흐름과 PCR은 실제보다 좋게 나온다 — 소프트웨어까지 빼면 FY26 잉여현금흐름은 약 $507M이다.')
PH = ['FISV', 'FIS', 'GPN', 'PYPL', 'V', 'MA']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '결제 처리 6곳 PER 비교 (점수는 S&P500 결제·거래소·금융 데이터 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 결제·거래소·금융 데이터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 결제·거래소·금융 데이터 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('S&P500 결제 처리·거래소·금융 데이터 18곳 중 JKHY를 뺀 17곳과 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 처리·거래소·신용평가가 섞여 있어 성장·마진 구조가 다르다. 차트에는 결제 처리 6곳만 보인다.')
# 부문(FY2026 10-K 연간 − Q3 FY26 10-Q 9개월) — Core 191.6 + Payments 240.4 + Complementary 188.8 + Corporate Services 23.2 = 644.0.
SEG = [('코어 뱅킹', 191.6, '#00205b'), ('결제', 240.4, '#0096d6'), ('보완 솔루션', 188.8, '#9fd3f0'), ('기타(Corporate Services)', 23.2, '#8a96a3')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q4 FY26)'
# 손 뉴스: Q1 FY27 실적(11-03 장 마감 뒤 → 11-04 반응)이 카드 날짜 안이라 손 항목으로 쓰고, 그래서 자동 항목(Q4 FY26)이 빠지므로 Q4도 손으로 쓴다.
NEWS_RANGE = '2025.11 ~ 2026.11'
NEWS = [
    ('green', '2026년 11월 3일 장 마감 뒤 — Q1 FY27 실적·전망 상향', '2026-11-04',
     '매출 $701.5M(+8.8%) · 희석 EPS $2.28(1년 전 $1.97) · FY27 GAAP EPS 전망 $7.33~7.38 → $7.47~7.51 — 다음 날 주가 +10.8%', 'fy27q1', 'Jack Henry 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 8월 18일 장 마감 뒤 — Q4 FY26 실적', '2026-08-19',
     '매출 $644.0M(+4.7%) · 희석 EPS $1.57(1년 전 $1.75) — 다음 날 주가 +6.5%', 'q4', 'Jack Henry 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 5일 장 마감 뒤 — Q3 FY26 실적', '2026-05-06',
     '희석 EPS $1.71 — 다음 날 주가 −4.3%', 'q3', 'Jack Henry 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 3일 장 마감 뒤 — Q2 FY26 실적', '2026-02-04',
     '희석 EPS $1.72 — 다음 날 주가 +4.6%', 'q2', 'Jack Henry 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 17, 'mean': 193.47, 'median': 195, 'low': 165, 'high': 215, 'sb': 11, 'b': 4, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-05'


POST = [r"""
import re as _rej
h = _rej.sub(r'(<span class="diag-label">이자보상배율)(</span><span class="diag-value">[\d.,]+x)', r'\1(최근 4분기)\2', h, count=1)   # 연간 값이라 기간 표시(Codex r2 2026-11-05)
"""]


# ── 자동 카드 — 부문 지도 1판(손 표와 일치, FQ2 FY26까지 CorporateAndOtherMember 이름 → 별칭, 2026-11-05) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "jkhy:CoreSegmentMember": [
   "코어 뱅킹",
   "#00205b"
  ],
  "jkhy:PaymentsMember": [
   "결제",
   "#0096d6"
  ],
  "jkhy:ComplementaryMember": [
   "보완 솔루션",
   "#9fd3f0"
  ],
  "jkhy:CorporateServicesMember": [
   "기타(Corporate Services)",
   "#8a96a3"
  ]
 },
 "ignore": [],
 "alias": {
  "jkhy:CorporateAndOtherMember": "jkhy:CorporateServicesMember"
 }
}
