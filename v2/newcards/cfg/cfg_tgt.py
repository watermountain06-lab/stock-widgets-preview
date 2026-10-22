# TGT(타깃) v2 카드 설정 — 자동 카드(AUTO). 회계연도 1월 말 전후 토요일 마감, 이름은 시작한 해(FY2026 = 2026-02 ~ 2027-01, HD와 같은 꼴). 카드 순위 160(시총 158위). 대형 할인점.
# 출처: SEC XBRL, Q2 FY26 10-Q(2026-08-28), 실적 보도자료(Q3 FY25~Q2 FY26, 8-K 2.02항 — 모두 동부 오전 7~8시대 접수 = 장 전), 8-K(4분기 매출 예비 확인·경영진 개편 2/10, 신용 약정 8/14), StockAnalysis.
# 엔진 입력(2026-10-22): 차입금 $15,357M = 1년 안 1,136 + 장기 14,221(둘 다 금융리스 포함 — DEBT_TOTAL_TAG; 기본은 장기만 잡고 금융리스 $2,113M을 리스로 따로 더했다).
# 현금 $5,411M = CashCashEquivalentsAndShortTermInvestments(EV_TAGS_BY_CIK — 기본 현금 태그는 2017년에 멈췄고, 단기투자 태그는 현금성 자산 안의 값이라 빼서 두 번 세지 않는다). 운용리스 = 10-K 합계 OperatingLeaseLiability(2026-01 $3,834M — 분기엔 비유동분만 태그, Q2 실제 $3,733M). D&A는 현금흐름표 합계만(손익계산서 D&A 줄은 매출원가 안 감가상각 제외 — Codex r1 필수).
# Q2 FY26 EPS $4.11에 관세 환급 이익 주당 $1.65 — 최근 4분기 이익률이 그만큼 부풀어 있다(ROST와 같은 경우). 4분기 EPS는 역산과 보도자료가 같다.
BUILD = {}
CIK = '0000027419'
CUR, YO, QO = '2026-08-01', '2025-08-02', '2026-05-02'
QLABEL, YL, QQL = 'Q2 FY26', 'Q2 FY25', 'Q1 FY26'
L8 = ['Q3 FY24', 'Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26']
FY_ENDS, FY_LABEL = ('2026-01-31', '2025-02-01'), 'FY25'
FY_NAME_OFFSET = -1
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'Target'
S_ = 'https://www.sec.gov/Archives/edgar/data/27419/'
SEC = S_
TENQ = S_ + '000002741926000042/tgt-20260801.htm'; TENQ_NAME = 'Q2 FY26 10-Q'
PR = {'q2': S_ + '000002741926000034/a2026q2ex-99.htm', 'q1': S_ + '000002741926000020/a2026q1ex-99.htm',
      'q4': S_ + '000002741926000012/a2025q4ex-99.htm', 'q3': S_ + '000002741925000123/a2025q3ex-99.htm'}
LINKS = {'lead': S_ + '000002741926000009/trgtannouncesexecutivelead.htm'}
FAIRBAND_TITLE = 'id="tgtFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 최근 4분기 EPS에는 2분기 관세 환급 이익이 들어 있다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 15)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 이 분기만의 각주(YOY_NOTE). 관세 환급 $994M(매출원가 차감) = Q2 매출의 약 3.7%p(Fable r1 필수).
YOY_NOTE = {'2026-08-01': 'Q2 FY26 영업이익·순이익·FCF에는 관세 환급 $994M(매출원가 차감, 영업이익률 약 3.7%p)이 들어 있다'}
# 고정 문장(숫자 없음). 관세 환급 일회성, 운용리스.
MODEL_NOTE = ('최근 분기 이익과 현금흐름에 일회성 관세 환급이 들어 있어, 최근 4분기 이익률에서 출발하는 시나리오와 PER·PCR·이자보상배율이 그만큼 유리하게 계산된다. '   # Fable r1 필수
              '매장 임차료는 영업이익에 이미 비용으로 들어 있어 운용리스 부채는 내재가치에서 빼지 않는다. 순현금 칸의 운용리스는 직전 연차 보고서(FY25 말) 값이다.')   # Codex r2
PH = ['WMT', 'COST', 'KR', 'DG', 'DLTR', 'PG']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유통·생활용품 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(TGT 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·담배·생활용품이 섞여 있다. 차트에는 유통·생활용품 6곳만 보인다.')
# 매출(Q2 FY26 10-Q 상품군) — 식품·음료 5,991 + 생활필수품 4,617 + 의류 4,090 + 하드라인 3,894 + 홈 3,668 + 뷰티 3,639 + 광고·카드·기타 640(광고 279 + 신용카드 이익 공유 139 + 기타 174 + 기타 상품 48) = 26,539.
SEG = [('식품·음료', 5991.0, '#cc0000'), ('생활필수품', 4617.0, '#e65c5c'), ('의류·잡화', 4090.0, '#850000'), ('하드라인(전자·장난감 등)', 3894.0, '#f2a3a3'),
       ('홈 가구·장식', 3668.0, '#5a5a5a'), ('뷰티', 3639.0, '#a0a0a0'), ('광고·카드·기타', 640.0, '#d9d9d9')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 상품군별'
# 손 뉴스: 최신 실적(Q2 FY26, 8/19)도 손으로 — 관세 환급을 적으려고. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K 2025-11-19T12:58Z·2026-03-03T12:12Z·05-20T11:57Z·08-19T11:51Z = 장 전 → 같은 날. 경영진 개편 8-K 2/11 11:30Z(보도자료 2/10) → 2/10.
# 넣지 않은 8-K: 신용 약정(2025-10-09·2026-08-14), 이사 선임(1/22·7/22), CEO 보수(2/5), COO 선임(2/10 — 개편 항목에), 주총(6/12).
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 19일 — Q2 FY26 실적 · 관세 환급', '2026-08-19',
     '매출 $26.5B(+5.3%) · 기존점 +3.8% · 희석 EPS $4.11(1년 전 $2.05) — 관세 환급 이익 주당 $1.65 포함, 제외하면 +20%', 'q2', 'Target 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 20일 — Q1 FY26 실적', '2026-05-20',
     '매출 $25.4B(+6.7%) · 고객 방문 +4.4% · 희석 EPS $1.71(1년 전 $2.27 — 일회성 소송 합의 이익 포함)', 'q1', 'Target 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 3일 — Q4 FY25 실적', '2026-03-03',
     '매출 $30.5B(−1.5%) · 기존점 −2.5% · 희석 EPS $2.30(1년 전 $2.41) · FY2025 EPS $8.13', 'q4', 'Target 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 10일 — 새 CEO 아래 경영진 개편', '2026-02-10',
     '2월 1일 취임한 Michael Fiddelke CEO가 COO 등 경영진을 바꾸고, 4분기 매출·연간 EPS가 기존 전망 범위라고 확인', 'lead', 'Target 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 19일 — Q3 FY25 실적', '2025-11-19',
     '매출 $25.3B(−1.5%) · 기존점 −2.7% · 희석 EPS $1.51(1년 전 $1.85)', 'q3', 'Target 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 38, 'nt': 29, 'mean': 164.1, 'median': 161, 'low': 130, 'high': 200, 'sb': 11, 'b': 2, 'h': 21, 's': 4, 'ss': 0}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 손으로(상품 축; 상품 소계 ProductMember는 ignore, 광고·카드·기타 4개 멤버는 한 줄). 원문 대조: Q2 FY26 합 26,539, 1년 전 25,211(2026-10-22) ──
AUTO = True
SEG_MAP = {"concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], "axis": "srt:ProductOrServiceAxis", "extra": {},
           "members": {"us-gaap:FoodAndBeverageMember": ["식품·음료", "#cc0000"], "tgt:HouseholdEssentialsMember": ["생활필수품", "#e65c5c"],
                       "tgt:ApparelAndAccessoriesMember": ["의류·잡화", "#850000"], "tgt:HardlinesMember": ["하드라인(전자·장난감 등)", "#f2a3a3"],
                       "tgt:HomeFurnishingsAndDecorMember": ["홈 가구·장식", "#5a5a5a"], "tgt:BeautyMember": ["뷰티", "#a0a0a0"],
                       "tgt:OtherProductMember": ["광고·카드·기타", "#d9d9d9"], "tgt:AdvertisingRevenueMember": ["광고·카드·기타", "#d9d9d9"],
                       "tgt:CreditCardProfitSharingMember": ["광고·카드·기타", "#d9d9d9"], "tgt:OtherOtherRevenueMember": ["광고·카드·기타", "#d9d9d9"]},
           "ignore": ["us-gaap:ProductMember"]}

# 종합 해석·체크포인트의 Q2 영업이익률 9.6%에 관세 환급 표기(Fable r1 필수) — Q2 FY26이 최근 분기인 동안만. 다음 분기에 지울 것.
POST = [r'''
for _pat in [r"(영업이익률 9\.6%\(1년 전 [\d.]+%\))", r"(직전 Q2 FY26 9\.6%)"]:
    if re.search(_pat, h):
        h = re.sub(_pat, lambda m: m.group(1) + "(관세 환급 약 3.7%p 포함)", h)
''']
