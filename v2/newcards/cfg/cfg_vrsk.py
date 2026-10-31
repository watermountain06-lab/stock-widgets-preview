BUILD = {'overlay': True, 'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # SEC 요약 자료에 Q2 2026 10-Q가 없다(마지막 2026-04-29) — 원문 인라인 XBRL 보충(ixbrl_supplement, CNP 방식)
# VRSK(베리스크) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 보험 데이터·분석(언더라이팅 — 위험 평가·보험료 산정, 보상 — 손해 사정·사기 탐지). 보고 부문 하나(Insurance) — 매출 구성은 언더라이팅·보상.
# 출처: SEC XBRL(Q2 2026 10-Q는 SEC 요약 자료에 없어 원문 인라인 XBRL 보충 — BUILD overlay, CNP 방식), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 07:1x 동부 → 당일 반응), AccuLynx 8-K(10/29), StockAnalysis. 사전 조사 scratchpad pre/VRSK.md.
# 엔진 입력(2026-10-30): 차입금 = 1년 안 $257.7M + 장기 $4,215.8M = $4,473.5M(금융리스 포함, DEBT_TOTAL_TAG). 에너지(Wood Mackenzie, 2023-02 매각) 재작성 — RESTATED_LATEST, 자기 이력 2023-02-28부터(HISTORY_START), 현금흐름 성장 이력 2022-12 최근 4분기 합부터(HISTORY_WINDOW), 희석 EPS는 계속사업 우선·Q4 2021~2025 보도자료 값, EBITDA 상각 합산(DDA_SPLIT_BY_CIK).
# 자기자본 −$1,189M(2026 상반기 자사주 $1.57B·ASR $1.5B)이라 PBR 없음. 일회성: 최근 4분기 GAAP 6.51 중 약 0.49(7.5%, 채무 조기상환 손실·인수 관련 비용 등).
CIK = '0001442145'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Verisk'
S_ = 'https://www.sec.gov/Archives/edgar/data/1442145/'
SEC = S_
TENQ = S_ + '000143774926024749/vrsk20260630_10q.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'ax': S_ + '000095010326016441/dp255815_8k.htm', 'q2': S_ + '000143774926024748/ex_968691.htm', 'q1': S_ + '000143774926013728/ex_926417.htm', 'q4': S_ + '000143774926004451/ex_895228.htm', 'q3': S_ + '000143774925032072/ex_856088.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="vrskFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('2025-12 AccuLynx 인수($2.35B 현금) 계약을 해지했는데 상대가 소송을 냈고, 10/23 델라웨어 대법원이 1심 판결을 유지했다 — 인수를 마쳐야 할 수 있다(FTC 검토 등 조건 남음, 판결 내용 미공시). 인수하면 차입이 늘고 카드 숫자에는 없다. '
              '자사주를 크게 사서(2026 상반기 $1.57B) 자기자본이 음수(−$1.2B)라 PBR은 뜻이 없다. '
              '동종업 점수는 S&P500 산업재 기준이다.')
PH = ['EFX', 'BR', 'ADP', 'PAYX', 'CTAS', 'CPRT']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '데이터·업무 서비스 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(VRSK 제외)와 배수 순위를 매긴 값이다.',
            '기계·항공·운송·건설이 섞여 있다. 차트에는 데이터·업무 서비스 6곳만 보인다.')
# 매출(Q2 2026 10-Q 제품 축, 부문 Insurance) — 언더라이팅 569.1 + 보상 237.2 = 806.3.
SEG = [('언더라이팅', 569.1, '#0a2240'), ('보상(손해 사정)', 237.2, '#e8a33d')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 언더라이팅·보상'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건 + AccuLynx 판결(EPS는 GAAP 희석). 반응일: 장 전 발표(07:1x 동부) → 당일.
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 23일 — AccuLynx 소송 대법원 판결', '2026-10-23',
     '델라웨어 대법원이 AccuLynx 인수 소송 1심 판결을 유지(회사 발표 10/23, SEC 8-K 10/29) — 인수 완료 의무 가능성 — 당일 주가 −3.7%', 'ax', 'Verisk 공시 (SEC 8-K)'),
    ('neutral', '2026년 7월 29일 장 전 — Q2 2026 실적', '2026-07-29',
     '매출 $806M(+4.4%) · 순이익 $229M · 희석 EPS $1.75(1년 전 $1.81) · 조정 EPS $1.98 — 당일 주가 +0.4%', 'q2', 'Verisk 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 29일 장 전 — Q1 2026 실적', '2026-04-29',
     '매출 $783M(+4.0%) · 순이익 $234M · 희석 EPS $1.73(1년 전 $1.65) · $1.5B 가속 자사주 매입 — 당일 주가 +6.5%', 'q1', 'Verisk 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 18일 장 전 — Q4 2025 실적', '2026-02-18',
     '매출 $779M(+5.8%) · 순이익 $197M · 희석 EPS $1.42(1년 전 계속사업 $1.44) — 채무 조기상환 손실 등 주당 $0.31 포함 — 당일 주가 +3.8%', 'q4', 'Verisk 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 29일 장 전 — Q3 2025 실적', '2025-10-29',
     '매출 $768M(+5.9%) · 순이익 $226M · 희석 EPS $1.61(1년 전 $1.54) — 당일 주가 −10.4%', 'q3', 'Verisk 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 19, 'nt': 15, 'mean': 229.33, 'median': 230, 'low': 185, 'high': 260, 'sb': 7, 'b': 4, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-31'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q2 2026 569.1/237.2(2026-10-30) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {"us-gaap:StatementBusinessSegmentsAxis": "vrsk:InsuranceMember"},
 "members": {"vrsk:UnderwritingMember": ["언더라이팅", "#0a2240"], "vrsk:ClaimsMember": ["보상(손해 사정)", "#e8a33d"]},
 "ignore": []
}
