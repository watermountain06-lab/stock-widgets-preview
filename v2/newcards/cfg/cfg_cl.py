# CL(콜게이트-팜올리브) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 153(시총 151위). 치약·칫솔(구강), 개인·가정용품, 반려동물 사료(Hill's).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-31), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 동부 오전 7~8시대 접수 = 장 전), 8-K(부문 재편 3/17, 구조조정 2.05항), StockAnalysis.
# 엔진 입력(2026-10-22): 차입금 $7,857M = 1년 안 34 + 장기 7,823(DEBT_TOTAL_TAG — "Debt payable within one-year"가 ShortTermBankLoansAndNotesPayable이라 빠졌다).
# 현금 $1,370M = 원문. 단기 증권 $107M(10-Q 공정가치 주석 6/30 $83M — 차이 $24M)·운용리스 $566M(10-Q에 없음)은 2025-12 10-K 값. 자본이 $236M뿐(자사주 누적)이라 PBR이 수백 배로 나온다.
# 최근 4분기 영업이익에 스킨케어(Filorga 등) 영업권·무형자산 손상 $919M(Q4 2025)이 들어 있다 — 최근 4분기 이익률이 그만큼 낮다. 4분기 EPS 2023~2025 보도자료 값.
BUILD = {}
CIK = '0000021665'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Colgate-Palmolive'
S_ = 'https://www.sec.gov/Archives/edgar/data/21665/'
SEC = S_
TENQ = S_ + '000002166526000042/cl-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000002166526000041/q22026pressreleasetables.htm', 'q1': S_ + '000002166526000022/q12026pressreleasetables.htm',
      'q4': S_ + '000002166526000003/a4q2025pressreleasetables.htm', 'q3': S_ + '000002166525000052/q32025pressreleasetables.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="clFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 최근 4분기 EPS에는 스킨케어 손상차손이 들어 있다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 손상차손, 작은 자본, 구조조정.
MODEL_NOTE = ('최근 4분기 영업이익에는 스킨케어 사업의 영업권·무형자산 손상차손(현금 지출 없음)과 구조조정·소송 관련 비용이 들어 있어, 최근 이익률이 평소 수준보다 낮게 나오고 이 이익률에서 출발하는 시나리오도 그만큼 낮다. '   # Fable r1 필수
              '자사주 매입을 오래 해 장부상 자본이 매우 작아 PBR과 부채비율은 회사 비교에 쓰기 어렵다. 단기 증권과 운용리스는 직전 연차 보고서(2025년 말) 값을 쓴다(운용리스는 분기 보고서에 없다).')   # Codex r1 필수
PH = ['PG', 'KO', 'PEP', 'MDLZ', 'KMB', 'CHD']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '생활용품·식음료 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(CL 제외)와 배수 순위를 매긴 값이다.',
            '유통·담배·식품·음료가 섞여 있다. 차트에는 생활용품·식음료 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 2026년부터 유럽·아프리카/유라시아를 EMEA로 합침) — 생활용품 지역별 중남미 1,372 + EMEA 1,121 + 북미 891 + 아태 782 + Hill's 1,195 = 5,361. 1년 전 1,207/1,083/919/746/1,157 → 5,112.
SEG = [('중남미(생활용품)', 1372.0, '#d7282f'), ('Hill\'s 반려동물 사료', 1195.0, '#1f5aa6'), ('유럽·중동·아프리카(생활용품)', 1121.0, '#e87075'),
       ('북미(생활용품)', 891.0, '#8c1a1f'), ('아시아·태평양(생활용품)', 782.0, '#f2b3b6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문·지역별'
# 손 뉴스: 최신 실적(Q2 2026, 7/31)은 news_auto. 가이던스·Base Business(조정) EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 2025-10-31T11:57Z·2026-01-30T12:57Z·05-01T11:31Z = 장 전 → 같은 날.
# 넣지 않은 8-K: 사채(2025-11-10), 이사 선임(3/12), 법무 책임자(4/9), 주총(5/13), 부문 재편(3/17 — SEG 주석에 반영), 구조조정 확대(5/1 2.05 — Q1 항목에).
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('green', '2026년 5월 1일 — Q1 2026 실적 · 구조조정 확대', '2026-05-01',
     '매출 +8.4%(인수·환율 포함, 유기적 +2.9%) · 희석 EPS $0.80(−6%) · 3년 생산성 프로그램(2025년 7월 시작)의 예상 누적 세전 비용을 $200~300M에서 $350~550M으로 확대', 'q1', 'Colgate-Palmolive 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 30일 — Q4 2025 실적 · 스킨케어 손상차손', '2026-01-30',
     '매출 $5.23B(+5.8%) · 희석 EPS −$0.05(1년 전 $0.90) — 스킨케어 사업 영업권·무형자산 손상 $919M · 2025년 EPS $2.63(−25%)', 'q4', 'Colgate-Palmolive 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 31일 — Q3 2025 실적', '2025-10-31',
     '매출 +2.0%(유기적 +0.4%, 자체 상표 사료 철수 영향) · 희석 EPS $0.91(+1%)', 'q3', 'Colgate-Palmolive 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 17, 'mean': 98.41, 'median': 100, 'low': 87, 'high': 110, 'sb': 7, 'b': 6, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 손으로(두 축: 생활용품의 지역 축 + Hill's 부문). 원문 대조: Q2 2026 1,372/1,121/891/782/1,195, 1년 전 1,207/1,083/919/746/1,157(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "parts": [
  {"concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], "axis": "srt:StatementGeographicalAxis",
   "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember", "us-gaap:StatementBusinessSegmentsAxis": "cl:OralPersonalAndHomeCareMember"},
   "members": {"srt:LatinAmericaMember": ["중남미(생활용품)", "#d7282f"], "us-gaap:EMEAMember": ["유럽·중동·아프리카(생활용품)", "#e87075"],
               "srt:NorthAmericaMember": ["북미(생활용품)", "#8c1a1f"], "srt:AsiaPacificMember": ["아시아·태평양(생활용품)", "#f2b3b6"]}},
  {"concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], "axis": "us-gaap:StatementBusinessSegmentsAxis",
   "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
   "members": {"cl:HillsPetNutritionMember": ["Hill's 반려동물 사료", "#1f5aa6"]}}
 ]
}

# Bear 문구에 왜곡 요인을 붙인다(Codex r1 필수) — 마진에는 Q4 2025 손상차손 $919M(이 분기가 최근 4분기에 있는 동안만), 부채비율은 작은 자본. Q4 2025가 최근 4분기에서 빠지면(2026-12 분기) 첫 줄을 지울 것.
POST = [r'''
sub(r"(최근 4분기 영업이익률 [\d.]+%\(5년 중앙값 [\d.]+%\))\.", lambda m: m.group(1) + ' — 2025년 4분기 스킨케어 손상차손 $919M(현금 지출 없음)이 들어 있다.')
sub(r"(부채비율\(총부채 ÷ 자본\) [\d,]+%, 자본 \$[\d.]+[MB])\.", lambda m: m.group(1) + ' — 오랜 자사주 매입으로 자본이 작아 비율이 크게 나온다.')
''']
