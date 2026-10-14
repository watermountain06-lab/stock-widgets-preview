# LMT(록히드 마틴) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일, 분기는 마지막 일요일에 끝난다(Q2 2026 = 2026-06-28). 카드 순위 107.
# 출처: SEC XBRL(+ 감가상각 회사 고유 태그), Q2 2026 10-Q(2026-07-23), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항),
# 8-K(연금 단체연금 전환 2025-12-16), StockAnalysis.
# 엔진 입력(2026-10-14): 감가상각 표준 태그(DepreciationAndAmortization)가 분기 값 없이 연간만 있고, 2025년 3분기 누계는
# 회사 고유 태그 lmt:DepreciationAndAmortizationIncludingDiscontinuedOperations(9개월 $1,224M)로만 나와 최근 4분기 합이 끊겼다 →
# company_tags로 DepreciationAmortizationAndAccretionNet 이름에 싣는다. 4분기 EPS 2024년 보도자료 값 $2.22(역산 $2.27).
# 단기투자(2011년 $3M)·비지배지분(2021년 0) 태그는 멈췄지만 마지막 값이 0 근처이고 재무상태표에 줄이 없어 그대로 둔다.
BUILD = {'company_tags': [('lmt:DepreciationAndAmortizationIncludingDiscontinuedOperations', 'DepreciationAmortizationAndAccretionNet')]}
CIK = '0000936468'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-28', '2025-06-29', '2026-03-29'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'Lockheed Martin'
S_ = 'https://www.sec.gov/Archives/edgar/data/936468/'
SEC = S_
TENQ = S_ + '000162828026049411/lmt-20260628.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q1': S_ + '000162828026026683/ex991q12026.htm', 'q4': S_ + '000162828026003970/ex991q42025.htm',
      'q3': S_ + '000162828025045582/ex991q32025.htm'}
LINKS = {'ultra': S_ + '000162828026049411/lmt-20260628.htm', 'pension': S_ + '000093646825000057/lmt-20251218.htm'}
FAIRBAND_TITLE = 'id="lmtFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
PH = ['RTX', 'GD', 'NOC', 'LHX', 'BA', 'GE']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '항공우주·방위 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '항공우주·방위 PBR 비교', 'psr': '항공우주·방위 PSR 비교',
                'pcr': '항공우주·방위 PCR(FCF) 비교', 'evebitda': '항공우주·방위 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(LMT 제외)와 배수 순위를 매긴 값이다.',
            '방위·항공·기계·운송·건설 회사가 섞여 있다. 차트에는 항공우주·방위 6곳만 보인다.')
# 부문(Q2 2026 10-Q 부문 표) — 항공 8,112 + 미사일·화력 4,101 + 회전익·임무 4,354 + 우주 3,496 = 20,063 = 연결 매출(1년 전 7,420/3,433/3,995/3,307 = 18,155)
SEG = [('항공', 8112, '#000080'), ('회전익·임무 체계', 4354, '#4a6fa5'), ('미사일·화력', 4101, '#b22222'), ('우주', 3496, '#6a6a6a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: Q2 2026 실적(7/23)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤 손 항목(8/24 364일 신용 약정)은 넣지 않았다(README).
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 6일 — Ultra Maritime Solutions $3.45B 인수 계약', None,
     '수중전·대잠 체계 회사, 보유 현금과 추가 자금 조달로 지급, 2026년 4분기 종결 예상(규제 승인 조건) — Q2 2026 10-Q', 'ultra', 'Lockheed Martin 10-Q (SEC)'),
    ('red', '2026년 4월 23일 장 시작 전 — Q1 2026 실적', '2026-04-23',
     '매출 $18.0B(1년 전 $18.0B) · 순이익 $1.5B · 희석 EPS $6.44(1년 전 $7.28)', 'q1', 'Lockheed Martin 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 29일 장 시작 전 — Q4 2025 실적', '2026-01-29',
     '4분기 매출 $20.3B · 희석 EPS $5.80(1년 전 $2.22) · 2025년 EPS $21.49(연금 정산 비용 주당 $1.63 포함) · 수주 잔고 $194B', 'q4', 'Lockheed Martin 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 16일 — 연금 의무 약 $900M 보험사로 이전', None,
     '기존 단체연금 계약을 매수 전환 — 추가 현금 부담·출연 없음, 4분기에 비현금 영업외 정산손실 $479M 인식', 'pension', 'Lockheed Martin 공시 (SEC 8-K)'),
    ('red', '2025년 10월 21일 장 시작 전 — Q3 2025 실적', '2025-10-21',
     '매출 $18.6B(1년 전 $17.1B) · 희석 EPS $6.95(1년 전 $6.80) · 수주 잔고 $179B', 'q3', 'Lockheed Martin 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 16, 'mean': 617.06, 'median': 600, 'low': 486, 'high': 700, 'sb': 7, 'b': 2, 'h': 13, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-14'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-Q 부문 표 Q2 2026 8,112/4,101/4,354/3,496, 1년 전 7,420/3,433/3,995/3,307, 합 = 연결 매출(20,063·18,155)이라 조정 없음(2026-10-14) ──
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
  "lmt:AeronauticsMember": [
   "항공",
   "#000080"
  ],
  "lmt:RotaryAndMissionSystemsMember": [
   "회전익·임무 체계",
   "#4a6fa5"
  ],
  "lmt:MissilesAndFireControlMember": [
   "미사일·화력",
   "#b22222"
  ],
  "lmt:SpaceMember": [
   "우주",
   "#6a6a6a"
  ]
 },
 "ignore": []
}
