BUILD = {'cover_shares': True, 'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # FY2025 10-K부터 Foxtel이 중단사업 — 희석 EPS 총액(2.07)이 아니라 계속사업(0.84)을 쓴다(2023-06 전은 총액 = 계속사업)
# NWSA(뉴스코프 Class A) v2 카드 설정 — 자동 카드(AUTO). 회계연도 6월 30일. 다우존스(WSJ·배런스·팩티바), 디지털 부동산(REA Group 62%·Move/Realtor.com 80%), 출판(하퍼콜린스), 뉴스 미디어(더 타임스·뉴욕포스트 등).
# 출처: SEC XBRL, FY2026 10-K(2026-08-07 07:02 장 전 접수), 실적 보도자료(Q1~Q4 FY26, 8-K 2.02항 — 장 마감 뒤 16:1x 동부 발표 → 다음 날 반응), StockAnalysis. 사전 조사 scratchpad pre/NWSA.md.
# 엔진 입력(2026-10-30): 다중 클래스(A·B) — 표지 주식 수가 클래스별뿐이라 BUILD cover_shares(541.05M, 2026-07-31). 희석 EPS는 계속사업 태그(FY2025 총액 2.07에 Foxtel 매각 이익 주당 1.22).
# 영업이익 태그 없음 → DERIVED_OPINC(세전 − 순이자 − 기타 영업외, DIS 방식, FY2026 1,021). Foxtel 매각(DAZN, 2025-04-02) 재작성 — RESTATED_LATEST, 자기 이력 창 2025-08-06부터(HISTORY_START), 현금흐름 성장 이력 2024-06 최근 4분기 합부터(HISTORY_WINDOW).
# 차입금 $1,989M(장기만), 현금 $2,095M(REA 보유 $255M 포함), 비지배지분 장부 $710M(REA 38% — 시장가는 훨씬 크다). 일회성: 최근 4분기 GAAP 1.03 중 구조조정·손상 등 순 0.15(14.6%).
CIK = '0001564708'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
FY_ENDS, FY_LABEL = ('2026-06-30', '2025-06-30'), 'FY2026'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'News Corp'
S_ = 'https://www.sec.gov/Archives/edgar/data/1564708/'
SEC = S_
TENQ = S_ + '000156470826000175/nws-20260630.htm'; TENQ_NAME = 'FY2026 10-K'
PR = {'q4': S_ + '000156470826000171/release-q4fy2026.htm', 'q3': S_ + '000156470826000101/release-q3fy2026.htm', 'q2': S_ + '000156470826000027/release-q2fy2026.htm', 'q1': S_ + '000156470825000571/release-q1fy2026.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="nwsaFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('REA Group(호주 상장)의 지분 38%를 다른 주주가 갖고 있는데 내재가치와 EV/EBITDA는 비지배지분을 장부가 $0.7B로만 셈한다. 시장가로 셈하면 내재가치는 더 낮고 EV/EBITDA는 더 높다. '
              '시가총액은 Class A·B 합계 주식 수(541M)에 NWSA 가격을 곱한 값이다(의결권 있는 Class B NWS는 약 10% 비싸게 거래돼, 반영하면 시총이 약 3% 커진다). '
              '2025년 4월 Foxtel 매각으로 과거 실적이 재작성돼, 자기 이력은 재작성 값이 처음 나온 2025-08-06부터 비교한다. 동종업 점수는 S&P500 커뮤니케이션 기준이다.')
PH = ['FOXA', 'DIS', 'CMCSA', 'OMC', 'NFLX', 'GOOGL']
PEER_FILE = 'peer_universe/communication_services.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '미디어·플랫폼 6곳 PER 비교 (점수는 S&P500 커뮤니케이션 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 커뮤니케이션 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 커뮤니케이션 대비 배수 순위 (v2/peer_universe/communication_services.json)'
PEER_TIP = ('S&P500 커뮤니케이션(NWSA 제외, 클래스 중복 GOOG·FOX·NWS 포함)과 배수 순위를 매긴 값이다.',
            '미디어 외에 통신·인터넷 플랫폼이 섞여 있다. 차트에는 미디어·플랫폼 6곳만 보인다.')
# 매출(FY2026 10-K 부문, 4분기 = 연간 − 9개월) — 다우존스 644 + 디지털 부동산 553 + 출판 566 + 뉴스 미디어 574 = 2,337.
SEG = [('다우존스', 644, '#1a1a1a'), ('디지털 부동산', 553, '#c8102e'), ('출판', 566, '#2f6db5'), ('뉴스 미디어', 574, '#9aa5b1')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q4 FY26)'
YOY_NOTE = {'2026-06-30': '1년 전 순이익 $743M에는 Foxtel 매각 등 중단사업 이익 $690M이 들어 있다(계속사업 지배 순이익은 $53M, 회사 조정표)'}
# 손 뉴스: 실적 4건(EPS는 GAAP 희석, 1년 전은 계속사업). 반응일: 장 마감 뒤 발표(16:1x 동부) → 다음 날.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 5일 장 마감 뒤 — Q4 FY26 실적', '2026-08-06',
     '매출 $2.34B(+11%) · 순이익 $179M · 희석 EPS $0.33(1년 전 계속사업 $0.09) · FY2026 매출 $9.03B · EPS $1.03 — 다음 날 주가 +2.1%', 'q4', 'News Corp 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 7일 장 마감 뒤 — Q3 FY26 실적', '2026-05-08',
     '매출 $2.19B(+9%) · 순이익 $89M · 희석 EPS $0.16(1년 전 계속사업 $0.14) — 다음 날 주가 −0.1%', 'q3', 'News Corp 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 5일 장 마감 뒤 — Q2 FY26 실적', '2026-02-06',
     '매출 $2.36B(+6%) · 순이익 $193M · 희석 EPS $0.34(1년 전 계속사업 $0.40) — 다음 날 주가 −7.1%', 'q2', 'News Corp 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 6일 장 마감 뒤 — Q1 FY26 실적', '2025-11-07',
     '매출 $2.14B(+2%) · 순이익 $112M · 희석 EPS $0.20(1년 전 계속사업 $0.21) — 다음 날 주가 +6.5%', 'q1', 'News Corp 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 9, 'nt': 5, 'mean': 32.83, 'median': 35, 'low': 26.73, 'high': 38, 'sb': 5, 'b': 3, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-30'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q4 FY26 644/553/566/574(2026-10-30) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"nws:DowJonesSegmentMember": ["다우존스", "#1a1a1a"], "nws:DigitalRealEstateServicesSegmentMember": ["디지털 부동산", "#c8102e"], "nws:BookPublishingSegmentMember": ["출판", "#2f6db5"], "nws:NewsAndInformationServicesSegmentMember": ["뉴스 미디어", "#9aa5b1"]},
 "ignore": []
}
