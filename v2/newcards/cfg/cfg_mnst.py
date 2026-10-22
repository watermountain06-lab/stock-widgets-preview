# MNST(몬스터 베버리지) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 163(시총 162위). 에너지 음료(Monster·Reign·Bang·Burn 등), 주류(크래프트 맥주·FMB).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-07), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 마감 뒤 접수), 8-K(분할 7/8, 임원 9/25), StockAnalysis.
# 2-for-1 분할 두 번(2023-03-28, 2026-08-11 — 두 번째는 기준 10-Q 접수 8/7 뒤). KNOWN_SPLITS로 EPS·주식 수를 분할 뒤 기준으로 맞춘다(주식 1,959M = 10-Q 979.5M × 2).
# EPS 태그는 계속사업 희석 EPS(BUILD eps_tag — EarningsPerShareDiluted가 2011년에 멈췄다). 엔진 입력(2026-10-22): 차입금 0 — 2025년 상반기에 자사주 공개매수 차입을 다 갚았다
# (EV_ZERO_FROM_BY_CIK debt 2025-06-30부터 0, 그 전 마지막 값 $199M이 이어지지 않게). 운용리스 태그도 2025-03에 멈췄다(10-Q 계약 의무 표 미할인 $87.8M, 금융리스 $5.1M — 무시할 크기, 카드의 금융리스 $8M는 2025-03 마지막 태그값).
NI_TAGS = ['ProfitLoss']   # NetIncomeLoss 태그가 없다(비지배지분 없음 — ProfitLoss = 순이익)
BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}
CIK = '0000865752'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Monster'
S_ = 'https://www.sec.gov/Archives/edgar/data/865752/'
SEC = S_
TENQ = S_ + '000110465926092193/mnst-20260630x10q.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000110465926092046/tm2622396d1_ex99-1.htm', 'q1': S_ + '000110465926057188/tm2613885d1_ex99-1.htm',
      'q4': S_ + '000110465926020525/tm267393d1_ex99-1.htm', 'q3': S_ + '000110465925107778/tm2530426d1_ex99-1.htm'}
LINKS = {'buyback': S_ + '000110465926062567/tm2614725d1_ex99-1.htm', 'split': S_ + '000110465926081842/tm2619964d1_ex99-1.htm', 'exec': S_ + '000110465926110965/tm2626151d1_8k.htm'}
FAIRBAND_TITLE = 'id="mnstFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(분할 반영). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '장기 투자'
# 고정 문장(숫자 없음). 코카콜라 지분·유통, 분할.
MODEL_NOTE = 'EPS·주가와 주식 수는 모두 2026년 8월 2-for-1 분할 뒤 기준으로 맞췄다 — 분기 EPS는 보도자료·10-Q 본표의 분할 전 값을 2로 나눈 값이다(10-Q 주석의 분할 반영 추정 EPS는 반올림이 달라 조금 다를 수 있다).'   # Codex r1 권장
HEALTH_EXTRA = '차입금이 없고 현금·투자 자산이 많아 재무 안정성 지표가 매우 좋게 나온다.'
PH = ['KO', 'PEP', 'KDP', 'CELH', 'PG', 'MDLZ']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '음료·식품 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(MNST 제외)와 배수 순위를 매긴 값이다.',
            '음료·식품·생활용품·유통이 섞여 있다. 차트에는 음료·식품 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, Reign은 Monster 에너지 음료 부문 — Codex r1) — Monster 에너지 음료 2,356.1 + 전략 브랜드 143.7 + 주류 32.2 + 기타 5.4 = 2,537.5. 1년 전 1,937.3·129.9·38.0·6.4 → 2,111.6.
SEG = [('Monster 에너지 음료', 2356.1, '#4a8c1c'), ('전략 브랜드(Burn·Predator·Fury 등)', 143.7, '#95d15a'), ('주류', 32.2, '#2a5a0c'), ('기타', 5.4, '#c9e6ae')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 분할 반영 값 — 보도자료는 분할 전 $0.59 등), 분할, 임원. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K 2025-11-07T02:27Z·2026-02-27T02:24Z·05-08T00:26Z·08-07T00:23Z = 전날 장 마감 뒤 → 다음 세션.
# 분할 발표 8-K 2026-07-09T01:09Z(7/8 동부 21:09) → 7/9. 미주 CEO 사임 8-K 2026-09-26T00:05Z(9/25 금 동부 20:05) → 9/28(월).
# 자사주 8-K 2026-05-16T00:16Z(5/15 금 동부 20:16) → 5/18(Fable r1 권장 — 주총 8-K에 함께 실린 8.01항).
# 넣지 않은 8-K: 투자자 행사(12/2), 주총 결과(5/15 5.07항), 이사 사임 예고(6/4), 회계 책임자(9/4).
NEWS_RANGE = '2025.11 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 25일 — 미주 CEO 코카콜라로 이동', '2026-09-28',
     'Monster Energy 미주 CEO Rob Gehring이 11월 30일 사임하고 코카콜라로 돌아간다고 통보', 'exec', 'Monster 공시 (SEC 8-K)'),
    ('neutral', '2026년 8월 6일 — Q2 2026 실적', '2026-08-07',
     '매출 $2.54B(+20.2%) · 희석 EPS $0.295(분할 반영, 보도자료 $0.59, 1년 전 $0.25)', 'q2', 'Monster 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 8일 — 2-for-1 주식 분할 발표', '2026-07-09',
     '7월 24일 기준 주주에게 1주당 1주 배당 — 8월 11일부터 분할 가격으로 거래', 'split', 'Monster 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 15일 — 자사주 매입 $500M 추가 승인 발표', '2026-05-18',
     '새 매입 프로그램 최대 $500M(기존 잔여 약 $400M)', 'buyback', 'Monster 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 7일 — Q1 2026 실적', '2026-05-08',
     '매출 $2.35B(+26.9%) · 희석 EPS $0.29(분할 반영, 보도자료 $0.58, 1년 전 $0.225)', 'q1', 'Monster 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 26일 — Q4 2025 실적', '2026-02-27',
     '매출 $2.13B(+17.6%) · 희석 EPS $0.23(분할 반영, 보도자료 $0.46, 1년 전 $0.14)', 'q4', 'Monster 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 6일 — Q3 2025 실적', '2025-11-07',
     '매출 $2.20B(+16.8%) · 희석 EPS $0.265(분할 반영, 보도자료 $0.53, 1년 전 $0.19)', 'q3', 'Monster 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 25, 'nt': 18, 'mean': 50.36, 'median': 50, 'low': 40, 'high': 57, 'sb': 11, 'b': 3, 'h': 10, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-22'

# ── 자동 카드 — 부문 4개. 원문 대조: Q2 2026 2,356.1/143.7/32.2/5.4, 1년 전 1,937.3/129.9/38.0/6.4(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"mnst:MonsterEnergyDrinksSegmentMember": ["Monster 에너지 음료", "#4a8c1c"], "mnst:StrategicBrandsSegmentMember": ["전략 브랜드(Burn·Predator·Fury 등)", "#95d15a"],
             "mnst:AlcoholBrandsSegmentMember": ["주류", "#2a5a0c"], "us-gaap:AllOtherSegmentsMember": ["기타", "#c9e6ae"]},
 "ignore": []
}
