# BALL(볼) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 알루미늄 음료캔(북·중미, EMEA, 남미). 항공우주 사업은 2024-02 매각.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-04), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/BALL.md.
# 엔진 입력(2026-10-25): 영업이익 = 세전이익 + 부채 이자비용(DERIVED_OPINC — OperatingIncomeLoss 태그가 2024-03에 멈춤), 차입금 = 1년 안 $692M + 장기 $6,528M(DEBT_TOTAL_TAG),
# 순이익 = ProfitLoss(EV_TAGS 대체), 현금 $491M, 비지배지분 $20M. 일회성: Q3 2025 사우디 합작 지분 매각 이익 세전 $86M — 반대로 사업 통합 비용도 있어 GAAP 최근 4분기 EPS 3.52가 회사 비교 가능 3.90보다 약 10% 낮다.
BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # 계속사업 EPS — 2024-02 항공우주 매각 이익(중단사업)이 희석 EPS에 들어 PER이 3.5배까지 내려갔다(EMR 방식)
CIK = '0000009389'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Ball'
S_ = 'https://www.sec.gov/Archives/edgar/data/9389/'
SEC = S_
TENQ = S_ + '000110465926090226/ball-20260630x10q.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000110465926090074/ball-20260804xex99d1.htm', 'q1': S_ + '000000938926000107/ball-20260505xex99.htm',
      'q4': S_ + '000000938926000039/ball-20260203xex99.htm', 'q3': S_ + '000000938925000048/ball-20251104xex99.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ballFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 15)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('손익계산서에 영업이익 줄이 따로 태깅되지 않아 세전이익에 이자비용을 더해 영업이익으로 쓴다 — 그래서 Q3 2025 사우디 지분 매각 이익($86M)도 그 분기 영업이익에 들어 있다. '
              '2024년 항공우주 사업 매각 전후로 사업 범위가 달라 5년 이력이 끊긴다. 알루미늄 가격을 고객에게 넘기는 구조라 매출은 알루미늄 값에 따라 오르내린다.')
PH = ['AMCR', 'PKG', 'AVY', 'IP', 'SW', 'CRH']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '포장재 등 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(BALL 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·건자재·포장재가 섞여 있다. 차트에는 포장재 등 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 북·중미 2,006 + EMEA 1,242 + 남미 591 = 3,839, 본사·기타 158 → 3,997.
SEG = [('음료캔 — 북·중미', 2006, '#003f87'), ('음료캔 — EMEA', 1242, '#5b8ac4'), ('음료캔 — 남미', 591, '#a7a9ac'), ('기타(본사·부문 외)', 158, '#d9d9d9')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q2 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07:43~08:13 동부 접수) → 같은 날. 넣지 않은 8-K: 사채·신용 계약.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 4일 — Q2 2026 실적', '2026-08-04',
     '매출 $4.00B(+20%) · 순이익 $221M · 희석 EPS $0.83(1년 전 $0.76)', 'q2', 'Ball 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 5일 — Q1 2026 실적', '2026-05-05',
     '매출 $3.60B · 순이익 $205M · 희석 EPS $0.77(1년 전 $0.63) — 발표 당일 주가 −6%', 'q1', 'Ball 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 3일 — Q4 2025 실적', '2026-02-03',
     '매출 $3.35B · 순이익 $200M · 희석 EPS $0.75(1년 전 −$0.11) · 2025년 EPS $3.30 — 발표 당일 주가 +9%', 'q4', 'Ball 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 4일 — Q3 2025 실적', '2025-11-04',
     '매출 $3.38B · 순이익 $321M · 희석 EPS $1.18(1년 전 $0.65) — 사우디 합작 지분 매각 이익 세전 $86M 포함', 'q3', 'Ball 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 14, 'nt': 9, 'mean': 70.67, 'median': 72, 'low': 63, 'high': 78, 'sb': 8, 'b': 3, 'h': 3, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 3개 + 나머지(본사·기타, 수동 지도). 원문 대조: Q2 2026 2,006/1,242/591, 나머지 158(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"ball:MetalBeveragePackagingNorthAndCentralAmericaMember": ["음료캔 — 북·중미", "#003f87"], "ball:MetalBeveragePackagingEuropeMember": ["음료캔 — EMEA", "#5b8ac4"],
             "ball:MetalBeveragePackagingSouthAmericaMember": ["음료캔 — 남미", "#a7a9ac"]},
 "ignore": [],
 "remainder": ["기타(본사·부문 외)", "#d9d9d9", 0.04]
}
