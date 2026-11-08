BUILD = {}
# DPZ(도미노피자) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일에 가까운 일요일(52/53주) — 분기 12·12·12·16주(FY2026 53주라 Q4 17주, LONG_Q4_TICKERS).
# 출처: SEC XBRL, Q3 2026 10-Q, 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 06:05 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/DPZ.md.
# 엔진 입력(2026-11-03): 차입금 = 증권화 채권 비유동 $3,559M + 1년 안 $1,327M = $4,886M(금융리스 $127M 포함, DEBT_TOTAL_TAG). 자본 −$3,955M(PBR 해당 없음). 운용리스 $236M. 우선주 태그 비움.
# Q4 2021~2023 EPS 보도자료 값. 일회성: DPC Dash 공정가 손실·항공기 매각 이익·리프랜차이징 손익 순 약 −0.39/주(2%, 회사 미공시 계산값).
CIK = '0001286681'
CUR, YO, QO = '2026-09-06', '2025-09-07', '2026-06-14'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-28', '2024-12-29'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Domino’s Pizza'
S_ = 'https://www.sec.gov/Archives/edgar/data/1286681/'
SEC = S_
TENQ = S_ + '000128668126000040/dpz-20260906.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000128668126000039/dpz-ex99_1.htm', 'q2': S_ + '000128668126000034/dpz-ex99_1.htm', 'q1': S_ + '000128668126000024/dpz-ex99_1.htm', 'q4': S_ + '000119312526062313/dpz-ex99_1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="dpzFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('매출 분기가 12·12·12·16주라 분기 값을 4배 하면 틀리고, 2026년은 53주 해라 4분기가 17주다. 매출의 63%는 원가에 연동된 공급망 매출이라 마진이 낮아 보인다. '
              '자사주·배당을 증권화 채권으로 해 와서 자본이 마이너스라 PBR은 쓰지 않는다. 2027년 7월 예상 상환일(법적 만기 2047·2048년) 채권 $1.3B가 1년 안 부채로 옮겨왔다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['MCD', 'YUM', 'SBUX', 'CMG', 'DRI', 'HLT']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '외식·호텔 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(DPZ 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 외식·호텔 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문, 12주) — 746.2 + 355.7 + 83.7 = 1,185.6.
SEG = [('공급망', 746.2, '#7a8b99'), ('미국 매장', 355.7, '#006491'), ('해외 프랜차이즈', 83.7, '#e31837')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q3 2026, 12주)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:05 동부) → 같은 날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 13일 장 전 — Q3 2026 실적', '2026-10-13',
     '매출 $1.19B(+3.4%) · 순이익 $152M · 희석 EPS $4.60(1년 전 $4.08) — 당일 주가 −4.8%', 'q3', 'Domino’s 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 20일 장 전 — Q2 2026 실적', '2026-07-20',
     '매출 $1.19B(+4.3%) · 순이익 $136M · 희석 EPS $4.07(1년 전 $3.81) · 직영점 77곳 매각 — 당일 주가 +2.1%', 'q2', 'Domino’s 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 27일 장 전 — Q1 2026 실적', '2026-04-27',
     '매출 $1.15B(+3.5%) · 순이익 $140M · 희석 EPS $4.13(1년 전 $4.33) — 당일 주가 −8.8%', 'q1', 'Domino’s 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 23일 장 전 — Q4 2025 실적', '2026-02-23',
     '매출 $1.54B(16주, +6.4%) · 순이익 $182M · 희석 EPS $5.35(1년 전 $4.89) · FY2025 EPS $17.57 — 당일 주가 +4.1%', 'q4', 'Domino’s 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 30, 'nt': 20, 'mean': 362.8, 'median': 353, 'low': 308, 'high': 455, 'sb': 12, 'b': 2, 'h': 15, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 746.2/355.7/83.7(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"dpz:SupplyChainMember": ["공급망", "#7a8b99"], "dpz:USStoresMember": ["미국 매장", "#006491"], "dpz:InternationalFranchiseMember": ["해외 프랜차이즈", "#e31837"]},
 "ignore": []
}
