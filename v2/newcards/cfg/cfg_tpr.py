CIK = '0001116132'
# TPR(태피스트리) v2 카드 설정 — 자동 카드(AUTO). 회계연도 6월 말에 가까운 토요일(52/53주 — FY26 52주, FY27 53주). 패션 잡화 — 코치(매출 86%), 케이트 스페이드. 스튜어트 와이츠먼은 2025-08-04 매각(중단사업 아님).
# 출처: SEC XBRL, FY2026 10-K(2026-08-13 06:48 장 전), 실적 보도자료(Q1~Q4 FY26, 8-K 2.02항 — 장 전 06:45 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/TPR.md.
# D&A TTM $164.9M은 현금흐름표 $160.8M에 부문표 값이 Q2·Q3에 섞인 것(EV/EBITDA 12.93 대 12.95, 점수 차 0.1 — Codex r1, 엔진 고침 없음).
# 엔진 입력(2026-11-03): 차입금 = 장기 순액 $2,379.0M(DEBT_TOTAL_TAG — 기본은 액면 합 $2,396.6M), 단기투자 $177.3M(EV_TAGS_BY_CIK sti — 기본은 구성까지 더해 $326.7M). 현금 $974.7M, 운용리스 $1,574M.
# Q4 FY22·FY24~FY26 EPS는 보도자료 값(Q4_EPS_OVERRIDE — 자사주 매입이 커 연간 − 3분기 누계가 어긋남). 2026-10-30 사용자 결정(공시 대기만으로 보류하지 않는다) — Q1 FY27 10-Q(11-05 무렵 예상) 전 FY26 10-K 기준.
# 일회성: 최근 4분기 GAAP 7.29 중 Q4 관세(IEEPA) 환급 주당 +0.43(5.9%, 이익 쪽, 대부분 미수금) − 조직 효율·매각·유통망 비용 0.21. 환급을 EPS·영업이익에서 빼면 자기 이력 30.7 → 30.2(0표 유지, scratchpad tpr_e54).
CIK = '0001116132'
CUR, YO, QO = '2026-06-27', '2025-06-28', '2026-03-28'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
FY_ENDS, FY_LABEL = ('2026-06-27', '2025-06-28'), 'FY2026'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Tapestry'
S_ = 'https://www.sec.gov/Archives/edgar/data/1116132/'
SEC = S_
TENQ = S_ + '000111613226000018/tpr-20260627.htm'; TENQ_NAME = 'FY2026 10-K'
PR = {'q4': S_ + '000114036126032624/ef20079840_ex99-1.htm', 'q3': S_ + '000114036126019428/ef20072115_ex99-1.htm', 'q2': S_ + '000114036126003783/ef20064297_ex99-1.htm', 'q1': S_ + '000114036125040658/ef20058309_ex99-1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="tprFairBand" title="최근 1년 PER이 FY25 손상(연간 EPS $0.82) 시기의 40~90배라, PER 구간으로 낸 적정주가가 의미 없어 표시하지 않는다."'
PRE = ['FB = None']
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('Q4 FY26 이익에 관세(IEEPA) 환급 주당 $0.43이 들어 있다(대부분 아직 못 받은 미수금). 빼면 자기 이력 점수가 30.8에서 30.2로 내려가 −1 문턱(30)에 가깝지만 표는 같다. '
              '현금흐름 기본 시나리오의 영업이익률(최근 2년 중앙값 14.2%)에는 FY25 케이트 스페이드 손상($855M) 분기가 섞여 있다. 손상을 되돌리면 기본이 약 $83(현재가 ÷ 내재가치 1.45, 비싸다 −1)이 되지만 판정은 같다. '
              '자사주 매입이 커서 자본이 작아 PBR이 높다. 5년 배수 이력에는 FY25 케이트 스페이드 손상($855M)과 Capri 인수 무산 비용으로 이익이 눌린 시기가 들어 있다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['RL', 'NKE', 'LULU', 'DECK', 'TJX', 'ROST']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '의류·잡화 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(TPR 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 의류·잡화 6곳만 보인다.')
# 매출(FY2026 10-K 부문, 4분기 = 연간 − 9개월) — 코치 1,641.5 + 케이트 스페이드 235.1 = 1,876.6(스튜어트 와이츠먼 0, 매각).
SEG = [('코치', 1641.5, '#1c1c1c'), ('케이트 스페이드', 235.1, '#e4007f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 브랜드별(Q4 FY26)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:45 동부) → 같은 날.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('red', '2026년 8월 13일 장 전 — Q4 FY26 실적', '2026-08-13',
     '매출 $1.88B(+8.9%) · 순이익 $348M · 희석 EPS $1.68(1년 전 −$2.49, 손상) · 조정 EPS $1.32 · FY27 조정 EPS 전망 $7.80~7.90(53번째 주 제외) — 당일 주가 −16.5%', 'q4', 'Tapestry 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 7일 장 전 — Q3 FY26 실적', '2026-05-07',
     '매출 $1.92B(+21.2%) · 순이익 $344M · 희석 EPS $1.65(1년 전 $0.95) · 조정 EPS $1.66 — 당일 주가 −12.3%', 'q3', 'Tapestry 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 5일 장 전 — Q2 FY26 실적', '2026-02-05',
     '매출 $2.50B(+14.0%) · 순이익 $561M · 희석 EPS $2.68(1년 전 $1.38) · 조정 EPS $2.69 — 당일 주가 +10.2%', 'q2', 'Tapestry 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 6일 장 전 — Q1 FY26 실적', '2025-11-06',
     '매출 $1.70B(+13.1%) · 순이익 $275M · 희석 EPS $1.28(1년 전 $0.79) · 조정 EPS $1.38 — 당일 주가 −9.6%', 'q1', 'Tapestry 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 1, 'nt': 1, 'mean': 0, 'median': 0, 'low': 0, 'high': 0, 'sb': 0, 'b': 0, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-03'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q4 FY26 1,641.5/235.1(8-K, 2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"tpr:CoachMember": ["코치", "#1c1c1c"], "tpr:KateSpadeCompanyMember": ["케이트 스페이드", "#e4007f"], },
 "ignore": ["tpr:StuartWeitzmanSegmentMember", "tpr:StuartWeitzmanMember"]
}
