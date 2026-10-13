# MO(알트리아) v2 카드 설정 — 처음부터 자동 카드(AUTO, VLO 다음 두 번째). 회계연도 12월 31일. 카드 순위 105.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항), 8-K(CEO·CFO 교체 2025-12-11), StockAnalysis.
# 엔진 입력(2026-10-13): 4분기 EPS 보도자료 값(fetch_eps_history Q4_EPS_OVERRIDE 2025 $0.66·2024 $1.79), 분기 순이자비용(interest_extra — PM 전례),
# 비영업 자산 ABI·Cronos 지분법 장부가 $8.9B(nonop_extra 'Investments'). 10-K/A(2026-05-27)는 ABI 재무제표 첨부(Rule 3-09)뿐이라 재무 변경 없음.
# 매출은 손익계산서 "Net revenues"(소비세 포함 — 보도자료의 소비세 차감 매출이 아니다). 자본이 음수라 PBR 해당 없음.
CIK = '0000764180'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -1), '적정~고평가'
CO = 'Altria'
S_ = 'https://www.sec.gov/Archives/edgar/data/764180/'
SEC = S_
TENQ = S_ + '000076418026000094/mo-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q1': S_ + '000076418026000056/exhibit991erq12026.htm', 'q4': S_ + '000076418026000007/exhibit991erq42025.htm',
      'q3': S_ + '000076418025000128/exhibit991erq32025.htm'}
LINKS = {'ceo': S_ + '000076418025000133/mo-20251208.htm'}
FAIRBAND_TITLE = 'id="moFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 70)
ACT_REASON = ''
NONOP_WHAT = 'ABI·Cronos 지분'
PH = ['PM', 'KO', 'PEP', 'MDLZ', 'CL', 'KMB']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '담배·필수소비재 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': '필수소비재 PBR 비교', 'psr': '필수소비재 PSR 비교',
                'pcr': '필수소비재 PCR(FCF) 비교', 'evebitda': '필수소비재 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(MO 제외)와 배수 순위를 매긴 값이다.',
            '담배·음료·식품·생활용품·유통 회사가 섞여 있다. 담배 회사는 이익률이 높아 PSR이 높게 나온다. 차트에는 6곳만 보인다.')
# 부문(Q2 2026 10-Q 부문 주석) — 흡연 5,392 + 구강 713 + 기타 6 = 연결 매출 6,111. '기타'(전자담배 등)는 $6M이고 1년 전 −$8M(음수)이라 뺀다
SEG = [('흡연 제품', 5392, '#033787'), ('구강 담배', 713, '#68b820')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(기타 $6M 제외)'
# 손 뉴스: Q2 2026 실적(7/30)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤 손 항목(8/27 이사 선임, 10/7 신용 약정 연장)은 넣지 않았다(README).
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('green', '2026년 4월 30일 — Q1 2026 실적', '2026-04-30',
     '희석 EPS $1.30(1년 전 $0.63 — 전자담배 영업권 손상 $873M 포함) · 1분기 자사주 매입 $280M', 'q1', 'Altria 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 29일 — Q4 2025 실적', '2026-01-29',
     '4분기 희석 EPS $0.66(전자담배 부문 영업권·무형자산 손상 세전 $1.3B, 주당 $0.61 포함) · 1년 전 $1.79(법인세 항목 $928M, 주당 $0.55 포함) · 2025년 EPS $4.12', 'q4', 'Altria 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 10일 — CEO·CFO 교체 결정', None,
     'Salvatore Mancuso(CFO) CEO, Heather Newman CFO — 2026년 5월 14일 주총 뒤부터, Billy Gifford CEO 은퇴', 'ceo', 'Altria 공시 (SEC 8-K)'),
    ('red', '2025년 10월 30일 — Q3 2025 실적', '2025-10-30',
     '순매출 $6.1B(−3.0%) · 희석 EPS $1.41(1년 전 $1.34)', 'q3', 'Altria 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Hold', 'n': 14, 'nt': 9, 'mean': 71, 'median': 71, 'low': 58, 'high': 82, 'sb': 4, 'b': 0, 'h': 8, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-13'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판. 원문 대조: 10-Q 부문 주석 Q2 2026 5,392/713/6, 1년 전 5,357/753/−8, 합 = 연결 매출(6,111·6,102). 'All other'는 작고 음수가 나와 ignore(매출의 0.1%)(2026-10-13) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "mo:SmokeableProductsSegmentMember": [
   "흡연 제품",
   "#033787"
  ],
  "mo:OralTobaccoSegmentMember": [
   "구강 담배",
   "#68b820"
  ]
 },
 "ignore": [
  "us-gaap:AllOtherSegmentsMember"
 ]
}
