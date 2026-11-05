BUILD = {'overlay': True, 'no_dcf': '손해보험사라 현금흐름 모델을 쓰지 않는다'}   # CB·PGR과 같은 방식(2026-10-02 사용자 결정)
# CINF(신시내티 파이낸셜) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 손해보험(상업·개인·E&S)·생명보험·투자 — 독립 대리점 판매.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-26 16:10 동부 장 마감 뒤 → 첫 세션 10-27), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 모두 16시대 장 마감 뒤 → 다음 거래일). 사전 조사 scratchpad pre/CINF.md.
# 엔진 입력(2026-11-05): 차입 = 어음 $17M + 장기 $791M = $808M(DEBT_TOTAL_TAG), 단기투자 $141M은 보험 운용자산이라 뺌. 순이익에 보유 주식 평가손익이 들어 있다(최근 4분기 주당 약 7.29 — 2분기만 세후 $1,031M).
NO_DCF_SKEW = True   # 금융 카드 — 현금흐름 칸 쏠림 메모(A0) 없음
CIK = '0000020286'
OP_DISPLAY = (['IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest'], [(['InterestExpense'], 1)])   # 카드 표시용 영업이익 = 세전이익 + 이자비용(CB와 같음)
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, 0), '판정 보류'
CO = 'Cincinnati Financial'
S_ = 'https://www.sec.gov/Archives/edgar/data/20286/'
SEC = S_
TENQ = S_ + '000002028626000060/cinf-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000002028626000059/exhibit9913q26.htm', 'q2': S_ + '000002028626000043/exhibit9912q26.htm', 'q1': S_ + '000002028626000025/exhibit9911q26.htm', 'q4': S_ + '000002028626000005/exhibit991q425.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="cinfFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (현금흐름 미적용)</span>'
Y2 = (0, 40)
ACT_REASON = '보험사라 재고·매출채권 회전으로 보는 활동성이 맞지 않는다'
NONOP_WHAT = '투자'
PH = ['CB', 'TRV', 'ALL', 'HIG', 'WRB', 'PGR']
PEER_FILE = 'peer_universe/insurers.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '보험 6곳 PER 비교 (점수는 S&P500 보험사 기준)', 'pbr': '보험 PBR 비교', 'psr': '보험 PSR 비교',
                'pcr': '보험 PCR(FCF) 비교', 'evebitda': '보험 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 보험사(손해·종합·생명)보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 보험사 대비 배수 순위 (v2/peer_universe/insurers.json)'
PEER_TIP = ('S&P500 손해·종합·생명보험 15곳(CINF 제외)과 배수 순위를 매긴 값이다.', '생명보험사는 장부가·매출 구조가 달라 PBR·PSR 비교가 거칠다. 차트에는 손해보험 6곳만 보인다.')
MODEL_NOTE = ('보험사라 현금흐름 내재가치는 계산하지 않아 판정 보류다(자기 이력·동종업 점수는 참고). 순이익에 보유 주식의 평가손익이 그대로 들어가 분기 EPS가 크게 흔들린다 — 최근 4분기 희석 EPS 17.05 가운데 약 7.29가 투자 이익이다. 3분기 합산비율은 90.9%다. 영업 EPS로 PER을 매기면 S&P500 보험사 가운데 가장 비싼 쪽이 돼 동종업 칸은 ‘비싸다’로 바뀐다(카드는 다른 보험사와 같이 GAAP EPS를 쓴다). '
              '회사의 영업 EPS(최근 4분기 9.76)로 보면 PER은 약 19.5배로, 카드의 GAAP 기준 PER보다 훨씬 높다. 매출에도 투자 손익이 들어 있어 PSR과 매출 성장률이 부풀 수 있다. 차입금 $808M에는 금융·운용 리스(약 $67M)가 빠져 있다. 영업현금흐름이 큰 것은 보험료를 먼저 받고 보험금을 나중에 내는 시차 때문이기도 하다.')
SEG = [('상업 손해보험', 1272, '#c8102e'), ('개인 손해보험', 889, '#e9a0aa'), ('E&S(초과·잉여)', 188, '#7a0019'), ('생명보험', 87, '#1d1d1d'), ('투자', 345, '#8a96a3')]
SEG_ADJ = 266   # 기타 보험료 $260M(Cincinnati Re·Cincinnati Global) + 기타 수익 $6M
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: Q3 2026 실적 8-K를 news_auto가 실적으로 분류하지 않아(results False) 손 항목으로 쓴다. 반응일은 발표 시각 기준.
NEWS_RANGE = '2026.01 ~ 2026.11'
NEWS = [
    ('red', '2026년 10월 26일 장 마감 뒤 — Q3 2026 실적', '2026-10-27',
     '순이익 $459M · 희석 EPS $2.96(1년 전 $7.11, 주식 평가이익 차이) · 영업 EPS $2.86 — 다음 날 주가 +2.3%', 'q3', 'Cincinnati Financial 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 27일 장 마감 뒤 — Q2 2026 실적', '2026-07-28',
     '순이익 $1,255M · 희석 EPS $8.05(1년 전 $4.34, 주식 평가이익 포함) · 영업 EPS $1.43 — 다음 날 주가 −0.9%', 'q2', 'Cincinnati Financial 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 27일 장 마감 뒤 — Q1 2026 실적', '2026-04-28',
     '순이익 $274M · 희석 EPS $1.75(1년 전 −$0.57) · 영업 EPS $2.10 — 다음 날 주가 −0.4%', 'q1', 'Cincinnati Financial 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 9일 장 마감 뒤 — Q4 2025 실적', '2026-02-10',
     '순이익 $676M · 희석 EPS $4.29(1년 전 $2.56) · 영업 EPS $3.37 — 다음 날 주가 −3.3%', 'q4', 'Cincinnati Financial 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 8, 'nt': 4, 'mean': 193, 'median': 200, 'low': 171, 'high': 204, 'sb': 2, 'b': 0, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-05'


POST = [r"""
h = h.replace('차입금·리스 $', '차입금(리스 제외) $').replace('차입금·리스 ${B(', '차입금(리스 제외) ${B(').replace('차입금·리스보다 $', '차입금(리스 제외)보다 $')
h = h.replace('부문 간 거래·조정 +$', '기타 보험료·수익(Cincinnati Re·Global 등) +$')   # Codex r2 2026-11-05
"""]


# ── 자동 카드 — 부문 지도(손 표와 일치, 2026-11-05) ──
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
  "cinf:CommercialLinesInsuranceMember": [
   "상업 손해보험",
   "#c8102e"
  ],
  "cinf:PersonalLinesInsuranceMember": [
   "개인 손해보험",
   "#e9a0aa"
  ],
  "cinf:ExcessandSurplusLinesInsuranceMember": [
   "E&S(초과·잉여)",
   "#7a0019"
  ],
  "cinf:LifeInsuranceMember": [
   "생명보험",
   "#1d1d1d"
  ],
  "cinf:InvestmentSegmentOfCINFMember": [
   "투자",
   "#8a96a3"
  ]
 },
 "ignore": []
}
