# LITE(루멘텀) v2 카드 설정 — 자동 카드(AUTO). 회계연도 6월 말 무렵 토요일(FY26 = 2025-06-29 ~ 2026-06-27). 카드 순위 149(시총 147위). 광통신 부품·모듈·레이저.
# 출처: SEC XBRL, FY2026 10-K(2026-08-17), 실적 보도자료(Q1~Q4 FY26, 8-K 2.02항 — 모두 장 마감 뒤 접수), 8-K(NVIDIA 우선주 2026-03-02, 전환사채 교환 4/8·6/1), StockAnalysis.
# 엔진 입력(2026-10-22):
#  · 차입금 = 단기 $1,596.9M + 장기 $40.5M = $1,637.4M(DEBT_TOTAL_TAG — 같은 1년 안 만기 전환사채를 ShortTermBorrowings·LongTermDebtCurrent 두 태그로 실어 기본 합이 $3,234M이었다).
#  · 주식 수 = 표지 89.7M + NVIDIA Series A 전환우선주 2,876,415주(build_dcf.SHARES_ADD — 배당 없이 전환 기준 참여, 회사가 기본 EPS에도 넣는다). 배수의 시가총액은 표지 주식 수 그대로.
#  · 전환사채(원금 $1,554M — 2032 $1,265M 전환가 $187.77 등)는 원금 현금·초과분 주식 결제라 원금만 차입금이다. 주가가 전환가를 크게 넘어 초과분 희석(대략 수백만 주)은 반영하지 않는다(안건).
#  · 4분기 EPS 다섯 해 보도자료 값(Q4_EPS_OVERRIDE). FY26 4분기 순손실 $7.2B는 전환사채 주식화에 따른 비현금 상환 손실 $7.8B — PER은 A3로 빠진다.
#  · 부문: FY26부터 단일 사업. 10-K XBRL은 제품군 태그(Components·Systems)가 본문 비율과 뒤바뀌어 있어(10-K Systems $2,005.6M, 본문 Components 66.5%) 지역별로 쓴다.
BUILD = {}
CIK = '0001633978'
CUR, YO, QO = '2026-06-27', '2025-06-28', '2026-03-28'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
FY_ENDS, FY_LABEL = ('2026-06-27', '2025-06-28'), 'FY26'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Lumentum'
S_ = 'https://www.sec.gov/Archives/edgar/data/1633978/'
SEC = S_
TENQ = S_ + '000162828026057358/lite-20260627.htm'; TENQ_NAME = 'FY2026 10-K'
PR = {'q4': S_ + '000162828026055726/lite_ex991xq4fy26.htm', 'q3': S_ + '000162828026030530/lite_ex991xq3fy26.htm',
      'q2': S_ + '000162828026005005/lite_ex991xq2fy26.htm', 'q1': S_ + '000162828025048860/lite_ex991xq1fy26.htm'}
LINKS = {'nvda': S_ + '000119312526085412/d41019dex991.htm',
         'sp500': 'https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-to-Join-the-SP-500-Index/default.aspx'}
FAIRBAND_TITLE = 'id="liteFairBand" title="최근 1년 PER 25~75% 구간 × 최근 4분기 희석 EPS. 최근 4분기 EPS가 상환 손실로 음수라 이 범위는 참고용이다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-20, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 이 분기만의 각주(auto_card YOY_NOTE — 분기가 바뀌면 빠진다). Codex r1 필수: 재무 영역만 읽어도 손실 원인이 보이게.
YOY_NOTE = {'2026-06-27': '4분기 순손실·EPS·순이익률에는 전환사채를 주식으로 바꾸며 생긴 일회성 비현금 상환 손실 $7.76B가 들어 있다(영업이익은 흑자)'}
NEXT_CONFIRMED = {'quarter_end': '2026-09-26', 'date': '2026-11-05', 'src': '10/5 회사 공지 — 장 마감 뒤 발표, 콜 오후 5시(동부)'}
# 고정 문장(숫자 없음). 상환 손실, 전환사채 희석, 우선주, 급성장으로 이력 이익률이 낮음.
MODEL_NOTE = ('최근 4분기 순이익은 전환사채를 주식으로 바꾸며 생긴 비현금 상환 손실 때문에 크게 음수라 PER은 빠진다. 영업이익률은 최근에야 흑자로 올라서 '
              '과거 이익률에서 출발하는 시나리오는 가치를 작게 계산한다. NVIDIA가 산 전환우선주는 내재가치의 주식 수에만 더했고(배수의 시가총액은 보통주 기준), 전환가를 크게 넘은 전환사채의 초과분 희석은 반영하지 않았다.')   # Codex r1 권장
PH = ['NVDA', 'AVGO', 'ANET', 'CSCO', 'APH', 'MU']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': 'AI 네트워크·반도체 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(LITE 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 AI 데이터센터 네트워크·반도체 6곳만 보인다.')
# 매출(Q4 FY26 = FY2026 10-K 연간 − Q3 10-Q 9개월, 지역별·고객 소재지 기준) — 아태 589.5 + 미주 368.7 + EMEA 48.1 = 1,006.3. 1년 전 287.1/143.8/49.8 → 480.7.
SEG = [('아시아·태평양', 589.5, '#0a6ebd'), ('미주', 368.7, '#4fa3e0'), ('유럽·중동·아프리카', 48.1, '#9cc9ee')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역별(고객 소재지 기준)'
# 손 뉴스: 최신 실적(Q4 FY26, 8/11)도 손으로 — 상환 손실을 적으려고. 가이던스·비GAAP 이익은 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부, 날짜도 UTC 값): 실적 8-K 2025-11-05T02:16Z·2026-02-04T02:12Z·05-06T00:11Z·08-12T00:24Z = 장 마감 뒤 → 다음 날.
# NVIDIA 투자: 8-K 접수 2026-03-03T02:10Z이지만 공동 보도자료는 3/2자이고 3/2 주가 +11.75%(전날 대비) — 최초 공개일 3/2.
# S&P 500 편입: 지수 발표 3/6(금) 장 마감 뒤 → 3/9 +14.73%(Codex r1 권장; 회사 보도자료 3/10, 편입 3/23 장 전).
# 넣지 않은 8-K: 이사 선임(12/15), 회계책임자 은퇴(1/5), 신용 약정(12/22), 주총(11/24), 품질 담당 은퇴(7/30), 전환사채 교환(4/8·6/1 — 4분기 손실 항목에 묶음).
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('red', '2026년 8월 11일 장 마감 뒤 — Q4 FY26 실적 · 상환 손실', '2026-08-12',
     '매출 $1.01B(1년 전 $481M) · GAAP 순손실 $7.2B, 희석 EPS −$84.65 — 전환사채 일부를 주식으로 바꾸며 비현금 상환 손실 $7.8B', 'q4', 'Lumentum 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 5일 장 마감 뒤 — Q3 FY26 실적', '2026-05-06',
     '매출 $808M(1년 전 $425M) · 희석 EPS $1.50(1년 전 −$0.64)', 'q3', 'Lumentum 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 6일 장 마감 뒤 — S&P 500 편입 결정', '2026-03-09',
     'S&P 미드캡 400에서 S&P 500으로 옮겨 3월 23일 장 시작 전부터 편입(회사 공지 3/10)', 'sp500', 'Lumentum 보도자료'),
    ('green', '2026년 3월 2일 — NVIDIA $2B 투자·전략 제휴', '2026-03-02',
     'NVIDIA가 전환우선주 $2.0B(주당 $695.31, 2.88M주)를 사고 다년 구매 약정·레이저 생산능력 확보 계약 — 미국 신규 공장 투자에 쓴다', 'nvda', 'NVIDIA·Lumentum 공동 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 3일 장 마감 뒤 — Q2 FY26 실적', '2026-02-04',
     '매출 $666M(1년 전 $402M) · 희석 EPS $0.89(1년 전 −$0.88)', 'q2', 'Lumentum 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 4일 장 마감 뒤 — Q1 FY26 실적', '2025-11-05',
     '매출 $534M(1년 전 $337M) · 희석 EPS $0.05(1년 전 −$1.21)', 'q1', 'Lumentum 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 26, 'nt': 24, 'mean': 1123.42, 'median': 1140, 'low': 820, 'high': 1400, 'sb': 17, 'b': 5, 'h': 4, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 손으로(지역 축 3개, 나라별 소계는 ignore). 10-K는 ExcludingAssessedTax, 10-Q는 IncludingAssessedTax로 실어 둘 다 둔다.
# 원문 대조: Q4 FY26 589.5/368.7/48.1, 1년 전 287.1/143.8/49.8(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax", "us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
 "axis": "srt:StatementGeographicalAxis",
 "extra": {},
 "members": {
  "srt:AsiaPacificMember": ["아시아·태평양", "#0a6ebd"],
  "srt:AmericasMember": ["미주", "#4fa3e0"],
  "us-gaap:EMEAMember": ["유럽·중동·아프리카", "#9cc9ee"]
 },
 "ignore": ["country:US", "country:MX", "country:TH", "country:HK", "country:CN", "country:JP",
            "lite:AmericasExcludingUnitedStatesAndMexicoMember", "lite:OtherAsiaPacificNotIndividuallyIdentifiedMember"]
}

# 계산 어려움(roic) 설명: 예측 끝 자본수익률은 기본 시나리오의 가정 이익률(2년 중앙값)에서 나온 값이지 지금 실적이 아니다(Fable 2026-10-22 필수 — SNDK와 같은 치환).
POST = [r'''
one("    if (el && Array.isArray(D.hard)) {", "    const HM = " + repr(HIST['margin_2y']) + ";\n    if (el && Array.isArray(D.hard)) {")
sub(r"roic: \(\) => `자본수익률 \$\{pct\(H\.roic\)\} < 할인율 10% — [^`]*`", "roic: () => `예측 끝 자본수익률 ${pct(H.roic)} < 할인율 10% — 기본 시나리오의 가정 이익률(2년 중앙값 ${(HM * 100).toFixed(1)}%)에서 나온 값이고 지금 실적이 아니다`")
''']
