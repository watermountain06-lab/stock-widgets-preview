# VMC(벌컨 머티리얼스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 미국 최대 골재(쇄석·모래·자갈) 생산 — 골재, 아스팔트, 레미콘.
# 출처: SEC XBRL + 인라인 XBRL 보충(BUILD overlay — companyfacts에 7/29 Q2 10-Q가 없다), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 07:05 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/VMC.md.
# 엔진 입력(2026-10-28): 차입금 $4,364M(1년 안 $400M 포함), 현금 $194M(제한 현금 $94.5M 별도), 비지배지분 $24M. EPS는 계속사업 희석 EPS 우선(헤드라인 — 2005년 매각한 화학 사업 잔여 손익이 분기마다 ±0.01).
# 일회성: 최근 4분기 순 주당 −0.06 + 세금 +0.07 ≈ 0(사업·부동산 매각 이익, CEO 교체 비용, 매각 손실 — 절대값 약 5%).
BUILD = {'overlay': True, 'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}
CIK = '0001396009'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Vulcan Materials'
S_ = 'https://www.sec.gov/Archives/edgar/data/1396009/'
SEC = S_
TENQ = S_ + '000162828026050486/vmc-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': 'https://www.sec.gov/Archives/edgar/data/1396009/000114036126029958/ef20078928_ex99-1.htm', 'q1': 'https://www.sec.gov/Archives/edgar/data/1396009/000114036126017638/ef20071724_ex99-1.htm',
      'q4': 'https://www.sec.gov/Archives/edgar/data/1396009/000114036126005605/ef20065685_ex99-1.htm', 'q3': 'https://www.sec.gov/Archives/edgar/data/1396009/000114036125039792/ef20057945_ex99-1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="vmcFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 계속사업 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('골재는 운반비 때문에 지역 독점에 가까워 가격이 매년 오르지만, 건설 경기와 날씨에 따라 분기 물량이 크게 흔들린다(1분기가 가장 약하다). '
              '2026년 2분기 캘리포니아 레미콘·버진아일랜드 사업을 팔아 레미콘 부문이 줄었다 — 1년 전과의 부문 비교가 달라진다. 5년 매출 성장률에는 2021년 8월 U.S. Concrete 인수(2022년 매출 +32%)가 들어 있어 기본 시나리오가 보수·낙관보다 높게 나온다(최근 3년 성장은 연 2%대). 동종업 점수는 문턱(30)에서 3.5점 위라 동종 종목 배수가 조금만 바뀌어도 표가 바뀔 수 있다.')
PH = ['MLM', 'NUE', 'STLD', 'CF', 'PPG', 'LIN']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소재 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(VMC 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·건자재·포장재가 섞여 있다. 차트에는 건자재·철강·화학 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 부문 간 제거 후) — 골재 1,639.0 + 아스팔트 330.0 + 레미콘 186.8 = 2,155.8.
SEG = [('골재', 1639.0, '#004b8d'), ('아스팔트', 330.0, '#6d9cc9'), ('레미콘', 186.8, '#8c8c8c')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 계속사업 희석). 반응일: 장 전 07:05 발표 → 같은 날. 넣지 않은 8-K: CEO 교체·임원, 주총, 사업 매각(10-Q 본문).
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 29일 장 전 — Q2 2026 실적', '2026-07-29',
     '매출 $2.16B(+2.5%) · 순이익 $323M · 계속사업 희석 EPS $2.47(1년 전 $2.43) · 2026년 조정 EBITDA 전망 $2.5B', 'q2', 'Vulcan Materials 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 29일 장 전 — Q1 2026 실적', '2026-04-29',
     '매출 $1.76B · 순이익 $165M · 계속사업 희석 EPS $1.27(1년 전 $0.98)', 'q1', 'Vulcan Materials 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 17일 장 전 — Q4 2025 실적', '2026-02-17',
     '매출 $1.91B · 순이익 $252M · 계속사업 희석 EPS $1.91(1년 전 $2.23) · 2025년 $8.15 — 당일 주가 −7.8%', 'q4', 'Vulcan Materials 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 30일 장 전 — Q3 2025 실적', '2025-10-30',
     '매출 $2.29B · 순이익 $375M · 계속사업 희석 EPS $2.83(1년 전 $1.57)', 'q3', 'Vulcan Materials 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 16, 'mean': 311.63, 'median': 320, 'low': 249, 'high': 350, 'sb': 14, 'b': 2, 'h': 7, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-28'


# ── 자동 카드 — 부문 3개(다른 차원 없는 값 — 부문 간 제거 후). 원문 대조: Q2 2026 1,639.0/330.0/186.8(2026-10-28) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"vmc:AggregatesMember": ["골재", "#004b8d"], "vmc:AsphaltMember": ["아스팔트", "#6d9cc9"], "vmc:ConcreteMember": ["레미콘", "#8c8c8c"]},
 "ignore": ["vmc:FormerCementMember"]
}
