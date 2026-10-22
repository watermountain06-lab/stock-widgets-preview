# ECL(에코랩) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 154(시총 152위). 위생·세척, 수처리, 해충 방제, 생명과학 공정 솔루션.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-06), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 동부 오전 8시대 접수 = 장 전), 8-K(CoolIT 인수 3/20, 대출 4/15, 사채 5/29), StockAnalysis.
# 엔진 입력(2026-10-22): 차입금 $13,176.2M = 단기 1,271.1 + 장기 11,905.1(DEBT_TOTAL_TAG). 운용리스 $761.0M = 2025-12 10-K 합계(EV_TAGS_BY_CIK — 분기에는 유동분만 태그돼 $165.9M이었다).
# 이자비용 최신 분기 = InterestExpenseNonoperating(vendor LATEST_Q_BY_CIK — InterestExpense는 2026-03에 멈춤).
# 분기 말 현금 $5,135M에는 5월 사채 $5.0B가 들어 있고, 그 돈으로 7월 2일 CoolIT($4.75B)를 인수했다 — 6/30 기준 순차입금은 일관되지만 CoolIT 실적은 Q3부터.
# 4분기 EPS 2024 보도자료 값(2025는 역산과 같음).
BUILD = {}
CIK = '0000031462'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Ecolab'
S_ = 'https://www.sec.gov/Archives/edgar/data/31462/'
SEC = S_
TENQ = S_ + '000162828026053886/ecl-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000162828026049933/ecl_ex99x1.htm', 'q1': S_ + '000110465926049822/ecl-20260428xex99d1.htm',
      'q4': S_ + '000110465926012358/ecl-20260210xex99d1.htm', 'q3': S_ + '000110465925102859/ecl-20251028xex99d1.htm'}
LINKS = {'tenq': S_ + '000162828026053886/ecl-20260630.htm', 'coolit': S_ + '000110465926032446/tm269446d1_ex99-1.htm'}
FAIRBAND_TITLE = 'id="eclFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 25)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 이 분기만의 각주·체크포인트(auto_card YOY_NOTE·CHECK_DEBT — 분기가 바뀌면 빠진다). Fable r1.
YOY_NOTE = {'2026-06-30': '첫 막대(2024년 3분기) 영업이익·순이익에는 수술 사업 매각 차익이 들어 있다'}
CHECK_DEBT = {'2026-06-30': '7월 2일 CoolIT 인수 대금 지급 뒤 순차입금(분기 말 차입금 {debt}에서 현금이 빠진다)이 줄어드는지'}
# 고정 문장(숫자 없음). CoolIT 인수 시점.
MODEL_NOTE = ('분기 말 현금에는 분기 직후 마친 CoolIT(데이터센터 액체 냉각) 인수 대금으로 쓸 사채 자금이 들어 있어, 이 카드는 인수 전 재무로 본 평가이고 CoolIT 실적은 다음 분기부터 들어온다. '
              '2024년 3분기 영업이익에는 수술 사업 매각 차익이 들어 있어 그 분기 이익률과 과거 이익률 이력이 높게 나오고, 이 이력에서 고른 기본 시나리오 이익률과 내재가치도 그만큼 높다.')   # Codex r1 권장·Fable r1 필수
PH = ['LIN', 'APD', 'SHW', 'PPG', 'DD', 'IFF']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '화학·소재 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(ECL 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·포장·건자재가 섞여 있다. 차트에는 화학·소재 6곳만 보인다.')
# 매출(Q2 2026 10-Q 매출 분해 — 부문별 제품·장비 + 서비스·리스, 보고 환율) — 물 2,223.4 + 기관·특수 1,620.8 + 해충 방제 351.1 + 생명과학 220.1 = 4,415.4. 1년 전 1,977.3/1,544.6/317.4/185.9 → 4,025.2.
SEG = [('물(Global Water)', 2223.4, '#0074c1'), ('기관·특수(Institutional & Specialty)', 1620.8, '#5aa6dd'), ('해충 방제', 351.1, '#2e7d32'), ('생명과학', 220.1, '#9c27b0')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 최신 실적(Q2 2026, 7/28)도 손으로 — 7/2 CoolIT 인수 완료를 적으려고. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K 2025-10-28T12:10Z·2026-02-10T13:04Z·04-28T12:06Z·07-28T12:01Z, CoolIT 8-K 03-20T12:05Z = 장 전 → 같은 날.
# 넣지 않은 8-K: 사채 $5.0B(5/29 — CoolIT 항목에), 대출 약정(4/15), 이사 불출마(2/23), 공동 COO(2/25), 주총(5/11), 부문 재작성(3/27).
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('green', '2026년 7월 28일 — Q2 2026 실적', '2026-07-28',
     '매출 $4.42B(+9.7%) · 희석 EPS $1.90(+3%) · 7월 2일 CoolIT 인수 완료(10-Q)', 'q2', 'Ecolab 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 — Q1 2026 실적', '2026-04-28',
     '매출 $4.07B(+10.0%) · 희석 EPS $1.52(+8%)', 'q1', 'Ecolab 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 20일 — CoolIT Systems 인수 계약', '2026-03-20',
     '데이터센터 액체 냉각 회사 CoolIT를 $4.75B에 인수(KKR 펀드로부터) — 향후 12개월 매출 약 $550M 예상 · 5월 사채 $5.0B 발행으로 자금 마련', 'coolit', 'Ecolab 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 10일 — Q4 2025 실적', '2026-02-10',
     '매출 $4.20B(+4.8%) · 희석 EPS $1.98(1년 전 $1.66, +19%) · 구조조정(One Ecolab) 확대 — 2027년 말까지 세전 비용 약 $425M, 2027년 연간 절감 약 $325M 목표', 'q4', 'Ecolab 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 16일 — Ovivo Electronics 인수 완료', '2025-12-16',
     '반도체 공장용 초순수 물 처리 사업을 현금 $1.60B(취득 현금 제외)에 인수 — Global Water에 편입', 'tenq', 'Ecolab Q2 2026 10-Q (인수 주석)'),
    ('red', '2025년 10월 28일 — Q3 2025 실적', '2025-10-28',
     '매출 $4.17B(+4.2%) · 희석 EPS $2.05(1년 전 $2.58 — 수술 사업 매각 차익 포함, −21%)', 'q3', 'Ecolab 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 16, 'mean': 324.5, 'median': 330, 'low': 295, 'high': 360, 'sb': 15, 'b': 5, 'h': 4, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 손으로(부문 축 × 제품·서비스 두 묶음을 같은 이름으로 합친다). 원문 대조: Q2 2026 2,223.4/1,620.8/351.1/220.1, 1년 전 1,977.3/1,544.6/317.4/185.9(2026-10-22) ──
AUTO = True
_M = {"ecl:WaterServicesMember": ["물(Global Water)", "#0074c1"], "ecl:GlobalInstitutionalMember": ["기관·특수(Institutional & Specialty)", "#5aa6dd"],
      "ecl:GlobalPestEliminationMember": ["해충 방제", "#2e7d32"], "ecl:GlobalHealthcareAndLifeSciencesMember": ["생명과학", "#9c27b0"]}
SEG_MAP = {"parts": [
    {"concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], "axis": "us-gaap:StatementBusinessSegmentsAxis",
     "extra": {"srt:ProductOrServiceAxis": "ecl:ProductAndEquipmentMember"}, "members": _M},
    {"concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], "axis": "us-gaap:StatementBusinessSegmentsAxis",
     "extra": {"srt:ProductOrServiceAxis": "ecl:ServiceAndLeaseMember"}, "members": _M}]}
