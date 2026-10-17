# SBUX(스타벅스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 9월 말(52/53주, Q3 FY26 = 2026-03-30~06-28). 카드 순위 113.
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-07-29), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항), 8-K(중국 합작사 계약 2025-11-03·완료 2026-04-02,
# 구조조정 2026-05-13·09-22), StockAnalysis.
# 엔진 입력(2026-10-16): 현금은 CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents(EV_TAGS_BY_CIK — 기본 태그가 2022-07-03 $3,178M에 멈춰 4년 넘게 옛 값이 쓰였다).
# 장기투자 $313.2M이 두 태그(OtherLongTermInvestments·AvailableForSale 비유동)로 두 번 더해지던 것을 build_dcf에서 한 번만(공통 규칙, 기존 카드 해당 0장).
# 4분기 EPS: FY2025 보도자료 $0.12(역산 $0.11). Q1·Q2 FY26 일회성 법인세 $266M·$8M(주당 $0.23·$0.01)은 v2/tax_oneoff.json — PER용 EPS·내재가치 세율에서만 뺀다(Fable). 자본 음수(−$7.7B) — PBR 해당 없음.
# 중국 소매 사업은 2026-03-30 Boyu와의 합작사(Starbucks 40%)로 넘겨 연결에서 빠졌다 — 분사·중단사업이 아니라 재작성 없음. 매각 이익 $536M은 영업이익 아래(영업외).
# 합작사 지분(약 $1.2B, 지분법 투자 전체 $1.7B 안)은 그 이익이 영업이익 안("Income from equity investees")이라 비영업 자산에 더하지 않는다.
CIK = '0000829224'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-28', '2025-06-29', '2026-03-29'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-09-28', '2024-09-29'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Starbucks'
S_ = 'https://www.sec.gov/Archives/edgar/data/829224/'
SEC = S_
TENQ = S_ + '000082922426000130/sbux-20260628.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000082922426000129/sbux-06282026xearningsrele.htm', 'q2': S_ + '000082922426000078/sbux-03292026xearningsrele.htm',
      'q1': S_ + '000082922426000010/sbux-12282025xearningsrele.htm', 'q4': S_ + '000082922425000074/sbux-09282025xexhibit991.htm'}
LINKS = {'close': S_ + '000082922426000145/sbux-20260922.htm', 'china': S_ + '000082922426000064/sbux-04022026xexhibit991.htm',
         'chinadeal': S_ + '000082922425000079/a20251103-form8xkxex991.htm', 'restr': S_ + '000082922426000088/sbux-20260513.htm'}
FAIRBAND_TITLE = 'id="sbuxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
BB_NONE = {'2026-06-28': '없음 · 10-Q 주석'}   # 현금흐름표 매입 줄·태그 없음 — Q3 FY26 10-Q "we made no share repurchases"(세 분기 누계). 새 10-Q마다 주석 확인
NONOP_WHAT = '장기투자'
PH = ['MCD', 'CMG', 'YUM', 'DRI', 'DPZ', 'TJX']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '외식·소매 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': '외식·소매 PBR 비교', 'psr': '외식·소매 PSR 비교',
                'pcr': '외식·소매 PCR(FCF) 비교', 'evebitda': '외식·소매 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(SBUX 제외)와 배수 순위를 매긴 값이다.',
            '유통·자동차·여행·외식·의류 회사가 섞여 있다. PBR은 자사주로 자본이 작거나 음수인 회사가 많아 흔들린다. 차트에는 외식·소매 6곳만 보인다.')
# 부문(Q3 FY26 10-Q 부문 주석) — 북미 7,395.1 + 해외 1,322.6 + 채널 개발 587.9 + 본사·기타 17.1 = 9,322.7(연결 매출). 본사·기타는 뺀다.
# 해외는 3/30부터 중국 소매가 빠져 1년 전 2,010.7보다 작다.
SEG = [('북미', 7395.1, '#00704a'), ('해외', 1322.6, '#d4a017'), ('채널 개발', 587.9, '#7a5c3e')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(본사·기타 제외 · 해외는 3월 30일부터 중국 소매 연결 제외)'
# 손 뉴스: Q3 FY26 실적(7/29)도 손으로 쓴다 — 그 뒤 9/22 매장 정리 결정을 넣으면 자동 실적 항목이 빠지기 때문(README). 가이던스는 손 뉴스에 쓰지 않는다.
# 반응일: 실적 8-K 7/29·4/28·10/29는 동부 20시 접수 → 다음 거래일, 1/28은 12:46(장중) → 당일. 중국 완료 8-K 4/2 20:55 → 4/3 성금요일 휴장이라 4/6.
# 9/22 8-K는 9/24 10:55 접수(장중) → 9/24. 5/13 구조조정 8-K는 5/15 13:00(동부, 장중) → 5/15. 합작사 계약 8-K는 11/3 22:00 접수 → 11/4.
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('red', '2026년 9월 24일 — 북미 매장 약 1% 폐점 결정', '2026-09-24',
     '9월 22일 이사회 승인 · 구조조정 비용 약 $300M(현금 약 $200M) · 폐점은 대부분 FY2026 안', 'close', 'Starbucks 공시 (SEC 8-K)'),
    ('green', '2026년 7월 29일 장 마감 뒤 — Q3 FY26 실적', '2026-07-30',
     '매출 $9.32B(−1.4%, 중국 소매 연결 제외 반영) · 희석 EPS $0.91(중국 매각 이익 세전 $536M 포함, 1년 전 $0.49) · 기존점 매출 +7.9%', 'q3', 'Starbucks 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 15일 — 구조조정 계획 승인 공시', '2026-05-15',
     '5월 13일 이사회 승인 · 지원 조직·비소매 시설 축소, Reserve·Roastery 운영 단순화 · 구조조정 비용 약 $400M(비현금 손상 약 $280M)', 'restr', 'Starbucks 공시 (SEC 8-K)'),
    ('green', '2026년 4월 28일 장 마감 뒤 — Q2 FY26 실적', '2026-04-29',
     '매출 $9.53B(+8.8%) · 희석 EPS $0.45(1년 전 $0.34) · 기존점 매출 +6.2%', 'q2', 'Starbucks 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 2일 장 마감 뒤 — 중국 소매 합작사 거래 완료', '2026-04-06',
     'Boyu Capital 펀드 60%·Starbucks 40% · 3월 30일 종결', 'china', 'Starbucks 공시 (SEC 8-K)'),
    ('red', '2026년 1월 28일 — Q1 FY26 실적', '2026-01-28',
     '매출 $9.92B(+5.5%) · 희석 EPS $0.26(1년 전 $0.69) · 기존점 매출 +4%', 'q1', 'Starbucks 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 3일 장 마감 뒤 — 중국 소매 합작사 계약', '2025-11-04',
     'Boyu Capital이 최대 60%, Starbucks 40% 보유 · 브랜드·지식재산은 Starbucks가 계속 소유하고 라이선스', 'chinadeal', 'Starbucks 공시 (SEC 8-K)'),
    ('red', '2025년 10월 29일 장 마감 뒤 — Q4 FY25 실적', '2025-10-30',
     '매출 $9.57B(+5.5%) · 희석 EPS $0.12(1년 전 $0.80) · 기존점 매출 +1%', 'q4', 'Starbucks 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 35, 'nt': 19, 'mean': 116.47, 'median': 115, 'low': 97, 'high': 143, 'sb': 12, 'b': 2, 'h': 19, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-16'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-Q 부문 주석 Q3 FY26 7,395.1/1,322.6/587.9 + 본사 17.1,
# 1년 전 6,927.0/2,010.7/483.8 + 34.5 — 본사·기타 ignore(2026-10-16) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:Revenues"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "sbux:NorthAmericaSegmentMember": [
   "북미",
   "#00704a"
  ],
  "sbux:InternationalSegmentMember": [
   "해외",
   "#d4a017"
  ],
  "sbux:ChannelDevelopmentMember": [
   "채널 개발",
   "#7a5c3e"
  ]
 },
 "ignore": [
  "us-gaap:CorporateAndOtherMember"
 ]
}
