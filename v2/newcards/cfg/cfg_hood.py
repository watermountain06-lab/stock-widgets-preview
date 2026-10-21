# HOOD(로빈후드) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 143(시총 141위). 온라인 증권·옵션·가상자산·예측시장 거래.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30 접수), 실적 자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 마감 뒤 접수), 8-K(인력 감축 6/16, 전환사채 6/23), StockAnalysis.
# 경로: 증권사(은행 지주회사 아님)라 일반 경로 + 결제·거래소 비교군(peer_universe/brokers_fees.json) — 사용자 결정 2026-10-21.
# 짧은 상장(2021-07-29, 일봉 1,313개) — BUILD short_listing(사용자 승인 2026-10-21), SELF_SPAN·GROWTH_SPAN.
# 차입금에 넣지 않은 것: 연결 신용카드 자금 신탁 차입 $959M(10-Q 주석 11, 기타 유동부채 안 — 신용카드 채권과 맞물린 비소구 조달이라 운전자본 쪽에 남긴다, Codex r1).
# 엔진 입력(2026-10-21): 영업이익 줄이 없어 합성(세전이익 − 기타 수익 = 순매출 − 영업비용, Q2 574 — build_multiple_history.DERIVED_OPINC), 설비투자 PaymentsToAcquireOtherProductiveAssets
# (기본 태그는 2023-09에 멈춤), 차입금 = 전환사채 $2,170M(2026-06 발행), 다중 클래스(A·B)라 주식 수는 표지 값(cover_shares).
# PCR은 뺀다 — 증권사 영업현금흐름은 고객 자금·증권 대차 잔액 변동이 대부분이라 FCF 배수가 뜻이 없다(403배로 나왔다). 4분기 EPS 2024·2025 보도자료 값.
BUILD = {'short_listing': True, 'cover_shares': True, 'drop_multiples': ['pcr']}
CIK = '0001783879'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, None, -2), '적정~고평가'
CO = 'Robinhood'
S_ = 'https://www.sec.gov/Archives/edgar/data/1783879/'
SEC = S_
TENQ = S_ + '000178387926000114/hood-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000178387926000113/q22026robinhoodexhibit991.htm', 'q1': S_ + '000178387926000061/q12026robinhoodexhibit991.htm',
      'q4': S_ + '000178387926000013/q42025robinhoodexhibit991.htm', 'q3': S_ + '000178387925000309/q32025robinhoodexhibit991.htm'}
LINKS = {'tenq': TENQ, 'bb': 'https://www.sec.gov/Archives/edgar/data/1783879/000178387926000045/robinhoodboardofdirector.htm', 'rif': 'https://www.sec.gov/Archives/edgar/data/1783879/000178387926000071/hood-20260616.htm', 'cvt': 'https://www.sec.gov/Archives/edgar/data/1783879/000178387926000074/hood-20260622.htm'}
FAIRBAND_TITLE = 'id="hoodFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 연 {pct(HIST[\'growth_5y\'])} — 상장 뒤)</span>'
Y2 = (-20, 60)
GROWTH_SPAN = '상장 뒤 이력(2021년 하반기 이후)'
SELF_SPAN = '상장 뒤, 2021-10 이후'
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-27', 'src': '10/1 회사 공지 — 장 마감 뒤 발표, 콜 오후 5시(동부)'}   # 엔진 추정은 작년 10/31 주문 처리 보고(2.02항)를 실적으로 오인했다(Codex r1 필수)
ACT_REASON = '증권사라 재고·매출채권 회전으로 보는 활동성이 맞지 않는다'
HEALTH_EXTRA = '증권사라 유동자산·부채의 대부분은 고객 융자·고객 예탁금·증권 대차처럼 서로 맞물린 잔액이다 — 유동비율과 운전자본은 일반 기업처럼 읽지 않는다.'
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 거래량·가상자산·금리에 민감한 매출, 짧은 이력과 저점 출발 성장률, 증권사 대차대조표.
MODEL_NOTE = ('매출은 주식·옵션·가상자산·예측시장 거래량과 금리에 크게 좌우돼 분기마다 많이 흔들린다. 상장 뒤 이력만 써서 짧고, 그 사이 거래가 몰린 해와 적던 해를 모두 지나 성장률이 구간에 따라 크게 다르다. '
              '이익률 가정은 적자였던 상장 초기까지 포함한 이력에서 뽑아, 시나리오 사이 차이가 매우 크다 — 가장 낮은 값은 가치 하한이 아니라 적자 시절 이익률로 돌아가는 가정이다. '
              '운전자본에는 고객 융자·예탁금·담보 같은 증권업 잔액이 섞여 재투자 계산을 흔든다. 고객 자금이 영업현금흐름을 크게 움직여 PCR은 쓰지 않는다.')   # Codex r1 필수
PH = ['COIN', 'SCHW', 'IBKR', 'ICE', 'CME', 'NDAQ']
PEER_FILE = 'peer_universe/brokers_fees.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '증권·거래소 PER 비교 (점수는 결제·거래소·중개 비교군 기준)', 'pbr': '증권·거래소 PBR 비교', 'psr': '증권·거래소 PSR 비교',
                'pcr': '증권·거래소 PCR(FCF) 비교', 'evebitda': '증권·거래소 EV/EBITDA 비교'}
PEER_NAME_TITLE = '결제·거래소·보험 중개 비교군보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '결제·거래소·중개 비교군 대비 배수 순위 (v2/peer_universe/brokers_fees.json)'
PEER_TIP = ('결제·거래소·금융 데이터·보험 중개 회사(HOOD 제외)와 배수 순위를 매긴 값이다.',
            '증권사는 S&P500에 몇 곳뿐이라 수수료형 금융 회사와 함께 비교한다. 차트에는 증권·거래소 회사만 보인다.')
# 매출(Q2 2026 10-Q) — 거래 수익 776 + 기타 143 = 919, 순이자 수익 389를 더해 1,308. 1년 전 539/93, 순이자 357 → 989. 단일 부문 회사.
SEG = [('거래 수익', 776, '#00c805'), ('기타(구독 등)', 143, '#8ee58f')]
SEG_ADJ = 389
SEG_TITLE = '매출 구성 — 수수료형 수익(순이자 수익은 따로)'
SEG_ADJ_LABEL = '순이자 수익'
# 손 뉴스: 최신 실적(Q2 2026)도 손으로 — 하는 김에 같은 형식. 가이던스·조정 EBITDA는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부, 날짜도 UTC 값): 실적 8-K 2025-11-06T02:05Z(11/5 21:05)→11/6, 2026-02-11T02:05Z→2/11, 04-29T00:05Z→4/29, 07-30T00:05Z→7/30.
# 인력 감축 2026-06-16T14:00Z → 6/16. 전환사채는 회사 보도자료 6/22(시작·가격 결정 발표), 8-K 접수 6/23T14:04Z — 최초 공개일 6/22로(Codex r1).
# 넣지 않은 8-K: 주문 처리 보고(2.02항 10/31·1/30), 신용 약정(3/25), CTO 퇴임(5/9), 주총(6/4), 회계 책임자(6/27), CFO 교체는 실적 8-K 안(11/5 예고·2/6 선임).
NEWS_RANGE = '2025.11 ~ 2026.07'
NEWS = [
    ('green', '2026년 7월 29일 장 마감 뒤 — Q2 2026 실적', '2026-07-30',
     '매출 $1.31B(+32%) · 희석 EPS $0.62(1년 전 $0.42 — 이번 분기에 RVI 비연결 이익 주당 $0.14 포함) · 주식·옵션·예측시장 거래량 사상 최대 · 6월 Susquehanna와의 합작 예측시장 거래소·청산소 Rothera 출범', 'q2', 'Robinhood 실적 자료 (SEC 8-K)'),
    ('neutral', '2026년 6월 22일 — 전환사채 발행 발표', '2026-06-22',
     '사모 전환사채 원금 $2.20B(분기 말 장부가 $2.17B) — 회사 첫 장기 차입(8-K는 6/23 접수)', 'cvt', 'Robinhood 공시 (SEC 8-K)'),
    ('neutral', '2026년 6월 16일 — 정규직 약 10% 감원', '2026-06-16',
     '회사는 6월 들어 주식·옵션·예측시장 하루 평균 거래량이 사상 최대인 가운데 조직을 줄인다고 밝혔다', 'rif', 'Robinhood 공시 (SEC 8-K)'),
    ('neutral', '2026년 6월 1일 — WonderFi 인수 완료', '2026-06-01',
     '캐나다 가상자산 거래 회사 인수 완료(10-Q 주석 — 8-K 없음)', 'tenq', 'Robinhood Q2 2026 10-Q'),
    ('red', '2026년 4월 28일 장 마감 뒤 — Q1 2026 실적', '2026-04-29',
     '매출 $1.07B(+15%, 직전 분기보다 −17%) · 희석 EPS $0.38(1년 전 $0.37)', 'q1', 'Robinhood 실적 자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 24일 장 마감 뒤 — 자사주 매입 한도 $1.5B', '2026-03-25',
     '이사회가 A주 자사주 매입 $1.5B를 승인(이전 한도 잔여분 포함)', 'bb', 'Robinhood 공시 (SEC 8-K)'),
    ('neutral', '2026년 2월 10일 장 마감 뒤 — Q4 2025 실적 · CFO 교체', '2026-02-11',
     '매출 $1.28B(+27%) · 희석 EPS $0.66(1년 전 $1.01 — 그 분기엔 법인세 환입) · 2월 6일 Shiv Verma CFO 선임 · 1월 20일 Susquehanna와의 합작사 Rothera가 예측시장 거래소 MIAXdx 90% 인수', 'q4', 'Robinhood 실적 자료 (SEC 8-K)'),
    ('green', '2025년 11월 5일 장 마감 뒤 — Q3 2025 실적', '2025-11-06',
     '매출 $1.27B(+100%) · 희석 EPS $0.61(1년 전 $0.17) · Jason Warnick CFO 은퇴 예고', 'q3', 'Robinhood 실적 자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 31, 'nt': 26, 'mean': 137.34, 'median': 136, 'low': 107, 'high': 170, 'sb': 19, 'b': 6, 'h': 4, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-21'

# ── 자동 카드 — 부문 지도: 손으로(수익 종류 축). 원문 대조: Q2 2026 776/143(순이자 389), 1년 전 539/93(순이자 357)(2026-10-21) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {
  "hood:TransactionBasedRevenuesMember": ["거래 수익", "#00c805"],
  "us-gaap:FinancialServiceOtherMember": ["기타(구독 등)", "#8ee58f"]
 },
 "ignore": []
}
