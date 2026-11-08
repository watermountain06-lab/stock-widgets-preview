# CASY(케이시스 제너럴 스토어) v2 카드 설정 — 자동 카드(AUTO). 회계연도 4월 30일(FY2027 = 2026-05~2027-04). 미국 중서부 편의점(조리 피자·식품)과 주유소, 약 2,900곳.
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-09-08), 실적 보도자료(Q2 FY26~Q1 FY27, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/CASY.md.
# 엔진 입력(2026-10-25): 영업이익 = 세전이익 + 순이자비용("Interest, net" — InterestExpense 태그, DERIVED_OPINC — 손익계산서에 영업이익 줄이 없다. 10-K 연간 세전이익은 IncomeLossAttributableToParent 태그로만 실린다),
# 차입금 = 1년 안 $104.3M + 장기 $2,326.2M(DEBT_TOTAL_TAG), 현금 $524M. RestrictedCashNoncurrent 태그($430.7M)는 사용권자산 줄에 잘못 붙은 것이라 쓰지 않는다(엔진 기본 현금 경로는 이 태그를 안 씀).
CIK = '0000726958'
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-04-30', '2025-04-30'), 'FY2026'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Casey’s'
S_ = 'https://www.sec.gov/Archives/edgar/data/726958/'
SEC = S_
TENQ = S_ + '000072695826000085/casy-20260731.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000072695826000084/q1fy2027earningspressrelea.htm', 'q4': S_ + '000072695826000033/ex991q42026pressrelease.htm',
      'q3': S_ + '000072695826000012/q3fy2026earningspressrelea.htm', 'q2': S_ + '000072695825000116/q2fy2026earningspressrelea.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="casyFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 10)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('매출의 대부분이 연료라 유가에 따라 매출이 크게 오르내리고 영업이익률은 낮게 보인다 — 이익은 갤런당 연료 마진과 매장 안 식품·잡화 마진에서 나온다. '
              '여름(회계 1분기)에 이익이 가장 크고 겨울(3분기)이 가장 작다. 손익계산서에 영업이익 줄이 없어 세전이익에 순이자비용을 더해 영업이익으로 쓴다. '
              '매출 구성은 단일 보고 부문이라 한 조각이다 — 연료·식품·잡화별 매출은 SEC 자료에 태깅되지 않는다.')
PH = ['WMT', 'COST', 'KR', 'DG', 'DLTR', 'TGT']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소매 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(CASY 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·담배·생활용품 제조사와 소매가 섞여 있다. 차트에는 소매 6곳만 보인다.')
SEG = [('편의점·주유소(단일 부문)', 5678.3, '#c8102e')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 단일 보고 부문'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:29~16:36 동부 접수) → 다음 거래일. 넣지 않은 8-K: 주총, 이사 선임, 자사주 한도 $1B, Investor Day(6/24).
NEWS_RANGE = '2025.12 ~ 2026.09'
NEWS = [
    ('red', '2026년 9월 8일 장 마감 뒤 — Q1 FY27 실적', '2026-09-09',
     '매출 $5.68B(+24%) · 순이익 $274M · 희석 EPS $7.37(1년 전 $5.77) — 다음 날 주가 −14%', 'q1', 'Casey’s 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 6월 9일 장 마감 뒤 — Q4 FY26·연간 실적', '2026-06-10',
     '매출 $4.57B · 순이익 $163M · 희석 EPS $4.37(1년 전 $2.63) · FY2026 EPS $19.16 — 다음 날 주가 +20%', 'q4', 'Casey’s 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 9일 장 마감 뒤 — Q3 FY26 실적', '2026-03-10',
     '매출 $3.92B · 순이익 $130M · 희석 EPS $3.49(1년 전 $2.33)', 'q3', 'Casey’s 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 12월 9일 장 마감 뒤 — Q2 FY26 실적', '2025-12-10',
     '매출 $4.51B · 순이익 $206M · 희석 EPS $5.53(1년 전 $4.85) — 다음 날 주가 −5%', 'q2', 'Casey’s 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 15, 'mean': 806.73, 'median': 780, 'low': 687, 'high': 950, 'sb': 12, 'b': 4, 'h': 4, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 단일 보고 부문(매출 = 부문 매출). 원문 대조: Q1 FY27 5,678.3(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"casy:ReportableSegmentMember": ["편의점·주유소(단일 부문)", "#c8102e"]},
 "ignore": []
}
