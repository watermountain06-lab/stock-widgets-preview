BUILD = {}
# HAS(해즈브로) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 마지막 일요일(52/53주). 부문: Wizards of the Coast·디지털 게임(Magic 등), 소비재(장난감·게임), 엔터테인먼트.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-29), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 06:3x 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/HAS.md.
# 엔진 입력(2026-11-03): 매출은 계약 매출 태그만(EXCLUDE_TAGS Revenues — 내부거래 제거 전 부문 합이 섞여 TTM $6,109M, 실제 $5,181M). 단기 국채 $576.2M(EV_TAGS_BY_CIK sti). 현금은 제한 현금 포함 합계 태그 $850.7M.
# 현금흐름 성장은 eOne 매각(2023-12-27) 뒤 첫 최근 4분기 합 2024-12-29부터(HISTORY_WINDOW, 넣기 전 5년 −3.3%). Q4 2025 EPS 보도자료 값. 자본은 비지배 포함 태그 기반 계산값 $913.6M.
# 일회성: 최근 4분기에 Q2 2026 디지털 게임 소프트웨어 손상 $56.4M과 Q3 관세 환급 $54.5M·세금 이익 $16.8M이 거의 상쇄(순 약 +0.13/주, 2%). 2025년 2분기 영업권 손상 $1,022M은 4분기 밖이지만 마진 이력(2년 중앙값)에 있다.
# 민감도(Codex r1): 소프트웨어 개발 투자(TTM $114M)를 설비투자에 넣으면 기본 $35.21, 영업권 손상까지 이력에서 빼면 $83.22·1.42(−1) — 판정 글자는 어느 쪽이든 적정~고평가. 소프트웨어 합산은 그 태그가 2026 전 연간뿐이라 PCR 이력이 250일로 줄어 넣지 않았다(백로그). 자기 이력 EV/EBITDA 175일도 감가상각 합산 태그 공백 탓(구성 태그로 이으면 782일, 점수 0표 유지).
CIK = '0000046080'
CUR, YO, QO = '2026-09-27', '2025-09-28', '2026-06-28'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-28', '2024-12-29'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Hasbro'
S_ = 'https://www.sec.gov/Archives/edgar/data/46080/'
SEC = S_
TENQ = S_ + '000004608026000065/has-20260927.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000004608026000058/exhibit991q32026.htm', 'q2': S_ + '000004608026000044/exhibit991q22026.htm', 'q1': S_ + '000004608026000029/exhibit991q12026.htm', 'q4': S_ + '000004608026000006/exhibit991q42025.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="hasFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 이익에서 소프트웨어 손상($56M)과 관세 환급($55M)이 거의 상쇄돼 순영향은 작다. 다만 2025년 2분기 영업권 손상($1.0B)이 과거 마진에 남아 내재가치 기본 시나리오를 낮춘다(손상을 빼면 기본 약 $77, 현재가 ÷ 내재가치 1.54로 여전히 “매우 비싸다”). '
              '2023년 말 eOne(영화·TV)을 팔아 현금흐름 성장 이력은 2024년 말부터 잡는다. 자사주 매입과 손상으로 자본이 작아 PBR이 높다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['NKE', 'LULU', 'DECK', 'RL', 'TPR', 'WSM']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소비재 브랜드 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(HAS 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 소비재 브랜드 6곳만(장난감 동종사는 지수에 없다) 보인다.')
# 매출(Q3 2026 10-Q 부문 외부 매출 — 회사 간 거래 축 없는 값) — 827.9 + 747.2 + 20.2 = 1,595.3.
SEG = [('소비재(장난감·게임)', 827.9, '#0057b8'), ('Wizards·디지털 게임', 747.2, '#e4002b'), ('엔터테인먼트', 20.2, '#ffb81c')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:3x 동부) → 같은 날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 20일 장 전 — Q3 2026 실적', '2026-10-20',
     '매출 $1.60B(+15.0%) · 순이익 $395M · 희석 EPS $2.77(1년 전 $1.64) · 조정 EPS $2.90 · 관세 환급 $55M 포함 — 당일 주가 +11.2%', 'q3', 'Hasbro 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 21일 장 전 — Q2 2026 실적', '2026-07-21',
     '매출 $1.14B(+16.2%) · 순이익 $161M · 희석 EPS $1.12(1년 전 −$6.10, 영업권 손상) · 디지털 게임 소프트웨어 손상 $56M 포함 — 당일 주가 +8.8%', 'q2', 'Hasbro 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 20일 장 전 — Q1 2026 실적', '2026-05-20',
     '매출 $1.00B(+12.8%) · 순이익 $198M · 희석 EPS $1.39(1년 전 $0.70) · 사이버 사고로 10-Q가 먼저 나옴(5/13) — 당일 주가 −8.8%', 'q1', 'Hasbro 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 10일 장 전 — Q4 2025 실적', '2026-02-10',
     '매출 $1.45B(+31.3%) · 순이익 $202M · 희석 EPS $1.41(1년 전 −$0.25) · FY2025 매출 $4.70B — 당일 주가 +7.5%', 'q4', 'Hasbro 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 14, 'nt': 13, 'mean': 117.23, 'median': 118, 'low': 100, 'high': 137, 'sb': 10, 'b': 2, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-03'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 827.9/747.2/20.2(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"has:ConsumerProductsSegmentMember": ["소비재(장난감·게임)", "#0057b8"], "has:WizardsOfTheCoastAndDigitalGamingSegmentMember": ["Wizards·디지털 게임", "#e4002b"], "has:EntertainmentSegmentMember": ["엔터테인먼트", "#ffb81c"]},
 "ignore": []
}
