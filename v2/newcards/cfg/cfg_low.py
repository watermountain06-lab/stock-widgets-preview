# LOW(로우스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 1월 말(52/53주, Q2 FY2026 = 2026-05-02~07-31). 카드 순위 112.
# 출처: SEC XBRL, Q2 FY2026 10-Q(2026-08-27), 실적 보도자료(Q3 FY2025~Q2 FY2026, 8-K 2.02항 — 모두 장 시작 전 접수), 8-K(FBM 인수 완료 2025-10-09), StockAnalysis.
# 엔진 입력(2026-10-16): 차입금 = 단기차입 + 리스 포함 장기차입금 유동·비유동(build_multiple_history DEBT_TOTAL_TAG — 1년 안 만기 $2,352M이 빠졌었다).
# 이자비용은 손익계산서 "Interest – net"(vendor/fetch_financials CONCEPTS_BY_CIK — InterestExpenseOther는 순이자 표의 "Other" 한 줄이라 0이 나왔다).
# 4분기 EPS: FY2024 보도자료 $1.99(역산 $2.01). 자본 음수(−$7.4B) — PBR 해당 없음. 2025-10-09 FBM 인수($8.8B 현금)로 무형자산·영업권이 늘었다.
CIK = '0000060667'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-07-31', '2025-08-01', '2026-05-01'
QLABEL, YL, QQL = 'Q2 FY26', 'Q2 FY25', 'Q1 FY26'
L8 = ['Q3 FY24', 'Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26']
FY_ENDS, FY_LABEL = ('2026-01-30', '2025-01-31'), 'FY2025'
VOTES, VERDICT = (1, 1, -1), '적정~저평가'
CO = "Lowe’s"
S_ = 'https://www.sec.gov/Archives/edgar/data/60667/'
SEC = S_
TENQ = S_ + '000006066726000117/low-20260731.htm'; TENQ_NAME = 'Q2 FY2026 10-Q'
PR = {'q2': S_ + '000006066726000113/exhibit991-07312026.htm', 'q1': S_ + '000006066726000062/exhibit991-05012026.htm',
      'q4': S_ + '000006066726000020/exhibit991-01302026.htm', 'q3': S_ + '000006066725000203/exhibit991-10312025.htm'}
LINKS = {'fbm': S_ + '000006066725000199/low-20251009.htm'}
FAIRBAND_TITLE = 'id="lowFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '장기투자'
PH = ['HD', 'TSCO', 'TJX', 'WSM', 'BBY', 'ORLY']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소매 유통 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': '소매 유통 PBR 비교', 'psr': '소매 유통 PSR 비교',
                'pcr': '소매 유통 PCR(FCF) 비교', 'evebitda': '소매 유통 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(LOW 제외)와 배수 순위를 매긴 값이다.',
            '유통·자동차·여행·외식·의류 회사가 섞여 있다. PBR은 자사주로 자본이 작거나 음수인 회사가 많아 흔들린다. 차트에는 소매 유통 6곳만 보인다.')
# 매출(Q2 FY2026 10-Q 매출 세분 표) — 소매 주택 개량 부문 상품군 하드라인 7,952 + 홈 데코 7,817 + 건축 자재 7,554 + 기타 692, 기타 부문 1,941 = 25,956(연결 매출).
# 표는 소매 주택 개량 부문의 상품군만 — 기타 부문(인수한 Pro 유통 등, 1,941)은 다른 축이라 SEG_ADJ로 합계 대조에만 넣는다.
SEG = [('하드라인', 7952, '#012169'), ('홈 데코', 7817, '#2f6fd0'), ('건축 자재', 7554, '#7fa7e8'), ('기타 상품', 692, '#9a9a9a')]
SEG_ADJ = 1941
SEG_SUM_LABEL, SEG_ADJ_LABEL = '소매 부문 상품군 합', '기타 부문 매출'   # 조정은 부문 간 거래가 아니라 기타 부문(FBM 등) 매출(Codex)
SEG_TITLE = '매출 구성 — 소매 주택 개량 부문 상품군(기타 부문 제외)'
# 손 뉴스: Q2 FY2026 실적(8/19)도 손으로 쓴다 — 매출 +8.3%의 대부분이 FBM 인수분이라 기존점 매출(+0.2%)을 함께 보여 주려고(Fable). 8/28 임원 선임은 넣지 않았다. 가이던스는 손 뉴스에 쓰지 않는다.
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 19일 — Q2 FY2026 실적', '2026-08-19',
     '매출 $26.0B(1년 전 $24.0B) · 희석 EPS $4.27(1년 전 $4.27) · 기존점 매출 +0.2%', 'q2', "Lowe’s 실적 보도자료 (SEC 8-K)"),
    ('green', '2026년 5월 20일 — Q1 FY2026 실적', '2026-05-20',
     '매출 $23.1B(1년 전 $20.9B) · 희석 EPS $2.90(1년 전 $2.92) · 기존점 매출 +0.6%', 'q1', "Lowe’s 실적 보도자료 (SEC 8-K)"),
    ('red', '2026년 2월 25일 — Q4 FY2025 실적', '2026-02-25',
     '매출 $20.6B(1년 전 $18.6B) · 희석 EPS $1.78(1년 전 $1.99) · 기존점 매출 +1.3%', 'q4', "Lowe’s 실적 보도자료 (SEC 8-K)"),
    ('green', '2025년 11월 19일 — Q3 FY2025 실적', '2025-11-19',
     '매출 $20.8B(1년 전 $20.2B) · 희석 EPS $2.88(1년 전 $2.99) · 기존점 매출 +0.4%', 'q3', "Lowe’s 실적 보도자료 (SEC 8-K)"),
    ('red', '2025년 10월 9일 — FBM(Foundation Building Materials) 인수 완료', '2025-10-09',
     '현금 $8.8B · 3년 만기 기간대출 $2.0B 전액 인출로 일부 조달', 'fbm', "Lowe’s 공시 (SEC 8-K)"),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 35, 'nt': 22, 'mean': 252, 'median': 258, 'low': 190, 'high': 275, 'sb': 20, 'b': 5, 'h': 9, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-16'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(소매 부문 상품군 4개, 손 표와 일치). 원문 대조: 10-Q 매출 세분 표 Q2 FY2026 7,952/7,817/7,554/692,
# 1년 전 8,006/7,782/7,472/561(재분류 반영). 기타 부문 1,941(1년 전 138)은 SEG_ADJ(2026-10-16) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "low:HardlinesMember": [
   "하드라인",
   "#012169"
  ],
  "low:HomeDecorMember": [
   "홈 데코",
   "#2f6fd0"
  ],
  "low:BuildingProductsMember": [
   "건축 자재",
   "#7fa7e8"
  ],
  "low:OtherSalesMember": [
   "기타 상품",
   "#9a9a9a"
  ]
 },
 "ignore": []
}
