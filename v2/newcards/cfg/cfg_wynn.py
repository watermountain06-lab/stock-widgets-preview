CIK = '0001174922'
# WYNN(윈 리조트) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카지노 리조트 — 마카오 2곳(Wynn Palace·Wynn Macau, Wynn Macau Ltd 지분 약 71%·홍콩 상장), 라스베이거스, 보스턴(Encore Boston Harbor). UAE Wynn Al Marjan(지분 투자, 2027-09 개장 예정).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-05 17:42 동부 장 마감 뒤 → 첫 세션 11-06 — 카드는 11-06 장중 가격으로 만들고 매일 실행이 종가로 고친다), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 모두 16:0x 동부 → 다음 거래일).
# 엔진 입력(2026-11-06): 현금 $1,642.2M + 단기 Investments $150.2M(EV_TAGS_BY_CIK sti — 기본 태그 2018 멈춤), 차입 $10,734M, 리스 $1,723M(2026-09 운용리스 비유동분 $1,621M + 2025-12 금융리스 $102M — DCF는 운용리스를 순부채에서 다시 뺀다), 비지배지분 장부 −$767.6M(Wynn Macau 누적 적자 — 음수라 내재가치에 더해진다), 자본 −$217M(PBR 해당 없음).
# 마카오 봉쇄(2020~2022) 기저: 자기 이력은 재개장 뒤 첫 최근 4분기 합 공시일 2024-02-23부터(HISTORY_START), 현금흐름 성장은 2023-12-31 합부터(HISTORY_WINDOW) — LVS 방식.
# 비지배지분은 장부가 유지(사용자 결정 2026-11-03 LVS) — 시장가(Wynn Macau 약 29%, 11-06 HKD 4.42)로 빼면 내재가치가 더 낮아진다. 현금흐름 표는 이미 −2.
# 지분법 투자 $1,199.5M(Al Marjan 등)은 nonop_extra.json(장부가, Fable r1 — PWR 방식). 넣기 전 기본 $21.95 → 넣은 뒤 약 $35.7, 비율 2.3대 — 둘 다 −2.
# −2 견고성(Fable r1): 지분법 + 세율 9.9% 고정이 가장 유리한 조합으로 기본 $49.7(−1 경계 $55.25). E54: Property charges는 8/8분기 반복, 계약 해지는 문턱 미달 — 장치 적용 0, 이력 창 소송·손상(2023~24)을 빼도 자기 PER 점수 0이어도 44.0이라 표 불변.
# 일회성: 최근 4분기 조정 항목은 파생상품 평가손익·외화 환산·자산 처분/손상(Property charges, 매 분기 반복)·개장 전 비용·차입 손실 — E54 범주(손상·매각·소송·계약 해지·IPR&D·구조조정) 중 손상류는 매 분기라 반복 기준으로 빠지지 않는다.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Wynn Resorts'
S_ = 'https://www.sec.gov/Archives/edgar/data/1174922/'
SEC = S_
TENQ = S_ + '000117492226000079/wynn-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000117492226000078/ex991wrlq32026pressrelease.htm', 'q2': S_ + '000117492226000051/ex991wrlq22026pressrelease.htm',
      'q1': S_ + '000117492226000034/ex991wrlq12026pressrelease.htm', 'q4': S_ + '000117492226000007/ex991wrlye2025pressrelease.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="wynnFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 25)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('Wynn Macau 지분의 약 29%를 다른 주주가 갖고 있는데, 그 장부가가 누적 적자로 −$0.8B라 내재가치에서 빼는 대신 오히려 더해진다. 시장가로 빼면 내재가치는 더 낮아진다. '
              'UAE Wynn Al Marjan(2027년 9월 개장 예정)은 지분 투자로, 개장 전이라 이익 없이 지분법 손실(올해 9개월 $16.5M, 개장 전 비용으로 영업이익 안)만 반영된다 — 내재가치에는 지분법 투자 장부가 $1.2B를 비영업 자산으로 더했다. 최근 4분기 EPS는 2025년 4분기를 연간 − 9개월로 역산한 값(0.96)이라 보도자료 분기 EPS 합(3.35)보다 조금 크다(분기마다 희석 주식 수가 달라 주당 값이 그대로 더해지지 않는다). 자사주 매입과 적자 누적으로 자본이 마이너스라 PBR은 쓰지 않는다. '
              '마카오 봉쇄(2020~2022) 시기를 빼려고 자기 이력은 2024-02부터, 현금흐름 성장 이력은 2023년 말부터 잡는다. 최근 4분기 이익에는 파생상품 평가손익과 외화 환산 손익이 섞여 분기마다 크게 흔들린다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['LVS', 'MGM', 'MAR', 'HLT', 'RCL', 'BKNG']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '카지노·호텔·여행 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(WYNN 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 카지노·호텔·여행 6곳만 보인다.')
# 매출(Q3 2026 실적 보도자료 리조트별) — Wynn Palace 583.8 + Wynn Macau 335.4 + 라스베이거스 575.2 + Encore Boston Harbor 194.7 = 1,689.1(연결 1,689.1).
SEG = [('윈 팰리스(마카오)', 583.8, '#8c6d3f'), ('라스베이거스', 575.2, '#2b2b2b'), ('윈 마카오', 335.4, '#cdb88f'), ('앙코르 보스턴 하버', 194.7, '#7d8a96')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 리조트별(Q3 2026)'
# 손 뉴스: 실적 3건(희석 EPS GAAP, 조정 EPS). 최신 Q3 2026(11-05 장 마감 뒤)은 news_auto가 붙인다. 반응일: 16:0x 동부 접수 → 다음 거래일.
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('green', '2026년 8월 4일 장 마감 뒤 — Q2 2026 실적', '2026-08-05',
     '매출 $1.86B(+6.9%) · 순이익 $140.1M · 희석 EPS $1.32(1년 전 $0.64) · 조정 EPS $1.24 — 다음 날 주가 +3.6%', 'q2', 'Wynn Resorts 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 7일 장 마감 뒤 — Q1 2026 실적', '2026-05-08',
     '매출 $1.86B(+9.2%) · 순이익 $120.5M · 희석 EPS $1.04(1년 전 $0.69) · 조정 EPS $1.25 — 다음 날 주가 −4.1%', 'q1', 'Wynn Resorts 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 12일 장 마감 뒤 — Q4 2025 실적', '2026-02-13',
     '매출 $1.87B(+1.5%) · 순이익 $100.0M · 희석 EPS $0.82(1년 전 $2.29) · 조정 EPS $1.17 — 다음 날 주가 +5.1%', 'q4', 'Wynn Resorts 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 21, 'nt': 16, 'mean': 121.06, 'median': 122, 'low': 93, 'high': 143, 'sb': 17, 'b': 4, 'h': 0, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-06'
POST = [r"""
h = h.replace('</span> 종가 기준</span>', '</span> 장중 기준</span>', 1)   # 10-Q가 11-05 장 마감 뒤라 11-06 장중 가격으로 만들었다 — 매일 실행이 종가로 고친다
h = re.sub(r'배당 지급 \(([^)]*)\)<', r'배당 지급 (\1 · Wynn Macau 소수주주 몫 포함)<', h)   # 9개월 지급 $163M은 본사 배당(분기 주당 $0.25)보다 커서 연결 지급액이다(Codex r1)
"""]


# ── 자동 카드 — 부문 지도(손 작성, 축 2개: 마카오 두 리조트는 법인 축(dei:LegalEntityAxis, 부문 = MacauOperations), 라스베이거스·보스턴은 부문 축.
#    원문 대조: Q3 2026 10-Q 583,771/335,428/575,154/194,700 = 연결 1,689,053, 2026-11-06) ──
AUTO = True
SEG_MAP = {
 "parts": [
  {
   "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
   "axis": "dei:LegalEntityAxis",
   "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember", "us-gaap:StatementBusinessSegmentsAxis": "wynn:MacauOperationsMember"},
   "members": {"wynn:WynnPalaceMember": ["윈 팰리스(마카오)", "#8c6d3f"], "wynn:WynnMacauMember": ["윈 마카오", "#cdb88f"]}
  },
  {
   "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
   "axis": "us-gaap:StatementBusinessSegmentsAxis",
   "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
   "members": {"wynn:LasVegasOperationsMember": ["라스베이거스", "#2b2b2b"], "wynn:EncoreBostonHarborMember": ["앙코르 보스턴 하버", "#7d8a96"]}
  }
 ],
 "ignore": []
}
