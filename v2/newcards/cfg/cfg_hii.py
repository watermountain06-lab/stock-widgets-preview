# HII(헌팅턴 잉걸스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 미 해군 항공모함·잠수함(Newport News), 구축함·상륙함(Ingalls), 국방 기술 서비스(Mission Technologies).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/HII.md.
# 엔진 입력(2026-10-25): 차입금 = 장기 $2,702M, 현금 = 제한 현금 포함 줄 $12M(EV_TAGS cash — 기본 태그 2024-03 멈춤), D&A = 감가상각 + 무형자산 상각(DDA_PARTS — 합산 태그 분기 행 2024년부터),
# 인수 = ACQ_FIXED 0(2026 10-Q에 인수 줄이 없어 2025 상반기 인수 $132M이 최근 4분기로 잘못 잡혔다). 일회성 없음.
CIK = '0001501585'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'HII'
S_ = 'https://www.sec.gov/Archives/edgar/data/1501585/'
SEC = S_
TENQ = S_ + '000150158526000047/hii-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000150158526000045/hii2026q2earningsrelease.htm', 'q1': S_ + '000150158526000027/hii2026q1earningsrelease.htm',
      'q4': S_ + '000150158526000004/hiiq42025earningsrelease.htm', 'q3': S_ + '000150158525000109/hii2025q3earningsrelease.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="hiiFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 10)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('매출 거의 전부가 미 해군 장기 계약이라 계약 원가 추정 변경(EAC)과 노동력·공급망 문제에 따라 분기 이익률이 크게 흔들린다. 영업이익률은 한 자릿수로 낮다. '
              '2023년 4분기 EPS($6.90)에는 베네수엘라 판결 채권 매각·Hydroid 보험금 합의 등 일회성 이익이 들어 있어 2024년 PER 이력이 그만큼 낮게 보인다. Q3 2026 실적이 10월 말 나올 예정이다.')
PH = ['GD', 'NOC', 'LHX', 'LMT', 'RTX', 'LDOS']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '방산 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(HII 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 방산 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 부문 간 거래 제거 전) — Newport News 1,849 + Ingalls 845 + Mission Technologies 760 = 3,454(제거 후 3,418).
SEG = [('Newport News(항모·잠수함)', 1849, '#002f6c'), ('Ingalls(구축함·상륙함)', 845, '#5a7fb5'), ('Mission Technologies', 760, '#a7a9ac')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07:13~07:23 동부 접수) → 같은 날.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('green', '2026년 7월 30일 — Q2 2026 실적', '2026-07-30',
     '매출 $3.42B · 순이익 $208M · 희석 EPS $5.27(1년 전 $3.86) — 발표 당일 주가 +14%', 'q2', 'HII 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 5일 — Q1 2026 실적', '2026-05-05',
     '매출 $3.10B · 순이익 $149M · 희석 EPS $3.79(1년 전 $3.79) — 발표 당일 주가 −10%', 'q1', 'HII 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 5일 — Q4 2025 실적', '2026-02-05',
     '매출 $3.48B · 순이익 $159M · 희석 EPS $4.04(1년 전 $3.15) · 2025년 EPS $15.39 — 발표 당일 주가 −11%', 'q4', 'HII 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 30일 — Q3 2025 실적', '2025-10-30',
     '매출 $3.19B · 순이익 $145M · 희석 EPS $3.68(1년 전 $2.56) — 발표 당일 주가 +7%', 'q3', 'HII 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 12, 'nt': 7, 'mean': 349, 'median': 340, 'low': 304, 'high': 406, 'sb': 5, 'b': 1, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-31'


# ── 자동 카드 — 부문 3개(수동 지도, 영업 부문 차원). 원문 대조: Q2 2026 1,849/845/760(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues", "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"hii:NewportNewsShipbuildingMember": ["Newport News(항모·잠수함)", "#002f6c"], "hii:IngallsMember": ["Ingalls(구축함·상륙함)", "#5a7fb5"],
             "hii:MissionTechnologiesMember": ["Mission Technologies", "#a7a9ac"]},
 "ignore": []
}
