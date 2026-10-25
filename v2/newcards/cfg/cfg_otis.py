# OTIS(오티스 월드와이드) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 엘리베이터·에스컬레이터 신규 설치(New Equipment)와 유지보수·현대화(Service).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-23), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), 8-K(CEO 은퇴 예정 2026-09-15), StockAnalysis. 사전 조사 scratchpad pre/OTIS.md.
# 엔진 입력(2026-10-25): 차입금 = 단기 $210M + LongTermDebt(1년 안 포함) $8,226M = $8,436M(DEBT_TOTAL_TAG), 비지배지분 $188M + 상환가능 $106M(EV_TAGS).
# 자본 잠식(약 −$5.7B — 2020 분사 때 부채를 안고 출발, 자사주) — PBR·ROE는 의미 없음. 일회성 작음(최근 4분기 GAAP 3.89 대 회사 조정 3.98).
CIK = '0001781335'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'Otis'
S_ = 'https://www.sec.gov/Archives/edgar/data/1781335/'
SEC = S_
TENQ = S_ + '000178133526000113/otis-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000178133526000110/a2026-06x308xkerexhibit99.htm', 'q1': S_ + '000178133526000072/a2026-03x318xkerexhibit99.htm',
      'q4': S_ + '000178133526000004/a2025-12x318xkerexhibit99.htm', 'q3': S_ + '000178133525000046/a2025-09x308xkerexhibit99.htm'}
LINKS = {'ceo': 'https://www.sec.gov/Archives/edgar/data/1781335/000114036126036566/ef20081992_ex99-1.htm'}
FAIRBAND_TITLE = 'id="otisFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('2020년 분사 때 부채를 안고 출발했고 자사주 매입을 이어 와서 장부 자본이 마이너스다 — PBR·ROE는 의미가 없다. '
              '매출의 약 3분의 2가 유지보수·현대화 서비스라 이익이 안정적인 편이고, 신규 설치는 중국 부동산 경기에 영향을 받는다. CEO가 2027년 상반기 후임 선임 뒤 물러날 예정이다. 시장성 증권(약 $0.06B)은 표준 태그가 없어 현금흐름 모델에 넣지 않았다.')
PH = ['TT', 'CARR', 'JCI', 'HON', 'ETN', 'GE']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '건물 설비·산업재 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(OTIS 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 건물 설비·산업재 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 서비스 2,580 + 신규 설치 1,279 = 3,859.
SEG = [('서비스(유지보수·현대화)', 2580.0, '#1c3f94'), ('신규 설치', 1279.0, '#6c8fd1')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q2 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석) + CEO 은퇴 예정. 반응일: 장 전 발표 → 같은 날, CEO 8-K 9/15 → 9/15. 넣지 않은 8-K: 사채 발행, COO 선임, 주총.
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('red', '2026년 9월 15일 — CEO 은퇴 예정 발표', '2026-09-15',
     'Judith Marks 회장 겸 CEO가 후임이 정해지면 물러난다(2027년 상반기 예상, 7월 말까지 재임 또는 고문)', 'ceo', 'Otis 공시 (SEC 8-K)'),
    ('red', '2026년 7월 22일 — Q2 2026 실적', '2026-07-22',
     '매출 $3.86B(+7.3%) · 순이익 $428M · 희석 EPS $1.12(1년 전 $0.99)', 'q2', 'Otis 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 22일 — Q1 2026 실적', '2026-04-22',
     '매출 $3.57B · 순이익 $340M · 희석 EPS $0.87(1년 전 $0.61)', 'q1', 'Otis 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 28일 — Q4 2025 실적', '2026-01-28',
     '매출 $3.80B · 순이익 $374M · 희석 EPS $0.95(1년 전 $0.84) · 2025년 희석 EPS $3.50', 'q4', 'Otis 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 29일 — Q3 2025 실적', '2025-10-29',
     '매출 $3.69B · 순이익 $374M · 희석 EPS $0.95(1년 전 $1.34 — 세금 이익 포함)', 'q3', 'Otis 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 15, 'nt': 9, 'mean': 88.22, 'median': 90, 'low': 75, 'high': 108, 'sb': 5, 'b': 2, 'h': 7, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 2개(수동 지도). 원문 대조: Q2 2026 2,580/1,279(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"otis:ServicesMember": ["서비스(유지보수·현대화)", "#1c3f94"], "otis:NewEquipmentMember": ["신규 설치", "#6c8fd1"]},
 "ignore": []
}
