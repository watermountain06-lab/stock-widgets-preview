BUILD = {'short_listing': True}   # 2023-10-02 Danaher에서 분사 상장 — 일봉 1,375개 미만 짧은 상장, 사용자 승인(2026-10-30) short_listing(CEG·GEHC 방식)
# VLTO(베랄토) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일(1~3분기는 금요일 끝 — Q3 2026 = 2026-07-04~10-02). 수질(하크·트로전 등 분석·처리)과 제품 품질·혁신(비디오젯 마킹·X-Rite 색 관리 등) 두 부문.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-29 18:34 장 마감 뒤 접수 — 첫 세션 10/30), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 마감 뒤 16:3x 동부 → 다음 날 반응), StockAnalysis. 사전 조사 scratchpad pre/VLTO.md.
# 2023-10-02 Danaher에서 분사 상장 — 짧은 상장(BUILD short_listing, 사용자 승인 2026-10-30, CEG·GEHC 방식): 자기 이력은 상장 뒤만. 분사 전 분기 EPS는 캐브아웃 값.
# 엔진 입력(2026-10-30): 차입금 = 총차입 LongTermDebt $2,920M(CP $249M 포함, DEBT_TOTAL_TAG — 기본은 장기 $2,671M만), 현금 $1,785M. Q4 2025 EPS는 보도자료 1.01(Q4_EPS_OVERRIDE).
# 일회성: 최근 4분기 GAAP 4.04 대 회사 조정 4.40 — 세후 무형 상각(약 0.18)을 빼면 순 약 0.18(4%대); 구조조정·세금보상자산 감소와 이산 세 혜택이 상쇄, 관세 환급(약 +0.07)은 조정 밖. 자기 이력은 2024-10-24부터(HISTORY_START — 분사 전 캐브아웃 EPS 제외), D&A는 감가상각 + 무형 상각, 리스는 최신 OperatingLeaseLiability.
CIK = '0001967680'
CUR, YO, QO = '2026-10-02', '2025-10-03', '2026-07-03'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Veralto'
S_ = 'https://www.sec.gov/Archives/edgar/data/1967680/'
SEC = S_
TENQ = S_ + '000196768026000048/vlto-20261002.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000196768026000047/vlto-20261029xex991.htm', 'q2': S_ + '000196768026000043/vlto-20260728xex991.htm', 'q1': S_ + '000196768026000023/vlto-20260428xex991.htm', 'q4': S_ + '000196768026000003/vlto-202625xex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="vltoFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('2023년 Danaher에서 분사해 상장했다 — 자기 이력은 분사 전 캐브아웃 실적이 최근 4분기 합에서 빠진 2024-10-24부터(약 2년) 비교했다. '
              '3분기 영업이익에 Danaher 분사 관련 세금보상자산 감소 $39M과 구조조정 $22M이 들어 있어 영업이익률이 낮게 나왔다 — 세금보상자산 감소 $39M은 같은 금액의 세금 부채 감소(세금 이익)로 순이익에서 상쇄됐고, 구조조정은 상쇄되지 않았다. 10/5 Cleanwater1을 $465M에 인수했다(9월 말 CP $249M 포함 현금·CP로 지급). '
              '동종업 점수는 S&P500 산업재 기준이다.')
PH = ['XYL', 'PNR', 'DOV', 'AME', 'IEX', 'FTV']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '수처리·계측 산업재 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(VLTO 제외)와 배수 순위를 매긴 값이다.',
            '기계·항공·운송·건설이 섞여 있다. 차트에는 수처리·계측 산업재 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 수질 939 + 제품 품질·혁신 570 = 1,509.
SEG = [('수질', 939, '#004b87'), ('제품 품질·혁신', 570, '#7ab800')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:3x 동부) → 다음 날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 29일 장 마감 뒤 — Q3 2026 실적', '2026-10-30',
     '매출 $1.51B(+7.5%) · 순이익 $253M · 희석 EPS $1.03(1년 전 $0.95) · 조정 EPS $1.18 · 연간 조정 EPS 전망 4.49~4.52로 상향 — 다음 날 주가 +6.8%', 'q3', 'Veralto 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 28일 장 마감 뒤 — Q2 2026 실적', '2026-07-29',
     '매출 $1.47B(+7.5%) · 순이익 $241M · 희석 EPS $0.98(1년 전 $0.89) — 다음 날 주가 +0.4%', 'q2', 'Veralto 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 28일 장 마감 뒤 — Q1 2026 실적', '2026-04-29',
     '매출 $1.42B(+6.8%) · 순이익 $254M · 희석 EPS $1.02(1년 전 $0.90) · In-Situ 인수 — 다음 날 주가 +4.5%', 'q1', 'Veralto 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 3일 장 마감 뒤 — Q4 2025 실적', '2026-02-04',
     '매출 $1.40B(+3.8%) · 순이익 $254M · 희석 EPS $1.01(1년 전 $0.91) · 2025년 EPS $3.76 — 다음 날 주가 −6.2%', 'q4', 'Veralto 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 17, 'nt': 13, 'mean': 111.92, 'median': 111, 'low': 100, 'high': 125, 'sb': 9, 'b': 2, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-30'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 939/570(2026-10-30) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"vlto:WaterQualitySegmentMember": ["수질", "#004b87"], "vlto:ProductQualityAndInnovationMember": ["제품 품질·혁신", "#7ab800"]},
 "ignore": []
}
