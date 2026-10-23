# TRGP(타가 리소시스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 169(시총 168위). 미드스트림 — 천연가스 수집·처리(퍼미안), NGL 운송·분별·수출.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-06 장중), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 전 접수), 8-K(회사채 2025-11·2026-02), StockAnalysis.
# 엔진 입력(2026-10-22): 차입금 = 1년 안 558 + 장기 19,020 = $19,578M(엔진 값 = 원문), 현금 $132M, 비지배지분 $139M(원문). 이자비용은 손익계산서 "Interest expense, net"
# (InterestIncomeExpenseNonoperatingNet, CONCEPTS_BY_CIK — InterestExpense는 2014년에 멈춤). 설비투자(TTM $4.1B)가 영업이익보다 커 FCF가 작다 — 성장 투자 단계.
NI_TAGS = ['NetIncomeLossAvailableToCommonStockholdersBasic', 'NetIncomeLoss']
BUILD = {'company_tags': [('trgp:PaymentsOfOrdinaryDividendsCommonAndPreferredShareholders', 'PaymentsOfDividendsCommonStock')]}   # 배당 지급(상반기 $488.6M) — 우선주는 2023년에 상환해 지금은 보통주 배당뿐(Fable r1)
CIK = '0001389170'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Targa'
S_ = 'https://www.sec.gov/Archives/edgar/data/1389170/'
SEC = S_
TENQ = S_ + '000119312526337729/trgp-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000119312526336525/trgp-ex99_1.htm', 'q1': S_ + '000119312526210165/trgp-ex99_1.htm',
      'q4': S_ + '000119312526058040/trgp-ex99_1.htm', 'q3': S_ + '000119312525265621/trgp-ex99_1.htm'}
LINKS = {'xom': 'https://targaresources.gcs-web.com/news-releases/news-release-details/targa-resources-corp-announces-20-year-agreements-exxonmobil-and'}
FAIRBAND_TITLE = 'id="trgpFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 상품 가격이 매출을 흔듦(PSR 해석), 성장 투자로 FCF 작음.
MODEL_NOTE = ('매출의 대부분이 NGL·천연가스 판매라 상품 가격에 따라 매출이 크게 오르내린다 — PSR 이력은 이익보다 가격의 영향을 많이 받는다(이익은 수수료 계약과 처리 물량에 더 달려 있다). '
              '퍼미안 처리 설비·파이프라인에 큰 성장 투자를 이어 가고 있어 잉여현금흐름이 작고, 그래서 PCR이 높게 나온다. '
              '현금흐름 내재가치가 낮은 것은 이익률이 과거 수준으로 내려간다고 보는 가정, 큰 투자에 비해 낮게 잡히는 투자 효율, 할인율, 큰 순차입금을 함께 반영한 결과다. 설비투자 외에 금융리스로 들인 설비(대부분 기존 압축기 리스 연장)도 재투자로 잡힌다.')   # Codex r1 필수
PH = ['OKE', 'WMB', 'KMI', 'XOM', 'CVX', 'COP']   # 미드스트림 3곳(ET·EPD는 MLP라 자료 없음) + 대형 통합·생산
PEER_FILE = 'peer_universe/energy.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '미드스트림 3곳·대형 에너지 3곳 PER 비교 (점수는 S&P500 에너지 기준)', 'pbr': '미드스트림 PBR 비교', 'psr': '미드스트림 PSR 비교',
                'pcr': '미드스트림 PCR(FCF) 비교', 'evebitda': '미드스트림 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 에너지 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 에너지 대비 배수 순위 (v2/peer_universe/energy.json)'
PEER_TIP = ('S&P500 에너지(TRGP 제외)와 배수 순위를 매긴 값이다.',
            '석유·가스 생산, 정유, 서비스, 미드스트림이 섞여 있다. 차트에는 미드스트림 3곳과 대형 에너지 3곳만 보인다.')
# 매출(Q2 2026 10-Q 부문 외부 매출) — 물류·운송 3,460.3 + 수집·처리 876.7 + 기타(헤지 등) 103.1 = 4,440.1.
SEG = [('물류·운송(NGL)', 3460.3, '#00539b'), ('수집·처리', 876.7, '#5f95d0'), ('기타(헤지 등)', 103.1, '#b3cce8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(외부 매출)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석, 조정 EBITDA·가이던스 수치는 쓰지 않는다 — 배당은 실제 선언 값만).
# 반응일: 실적 8-K 2025-11-05T11:15Z·2026-02-19T11:15Z·05-07T10:15Z·08-06T10:15Z = 장 전 → 같은 날.
# 넣지 않은 8-K: 회사채 발행(2025-11 $1.75B·2026-02 $1.5B — 일상 조달), 매출채권 약정(7/6), 이사·임원(7/17·8/25), 주총(5/22).
NEWS_RANGE = '2025.11 ~ 2026.08'
# ExxonMobil 계약은 회사 보도자료(8/17 월 오후 4:15 동부 = 장 마감 뒤, 8-K 없음) → 다음 거래일 8/18(Codex r2 확인).
NEWS = [
    ('green', '2026년 8월 17일 — ExxonMobil 20년 계약 · 처리 설비 3기', '2026-08-18',
     'ExxonMobil과 퍼미안 수집·처리·NGL 운송·분별 20년 수수료 계약(2046년까지) — 델라웨어 처리 설비 3기(합계 약 825MMcf/d, 2028년 상반기 가동) 추가, 2026년 성장 투자 전망 약 $5B로 높임 — 장 마감 뒤 발표라 반응은 다음 거래일(8/18)', 'xom', 'Targa 보도자료'),
    ('green', '2026년 8월 6일 — Q2 2026 실적', '2026-08-06',
     '매출 $4.44B(+4.2%) · 보통주 지배기업 귀속 순이익 $765M(1년 전 $629M) · 희석 EPS $3.54(1년 전 $2.87)', 'q2', 'Targa 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 7일 — Q1 2026 실적 · 배당 25% 인상', '2026-05-07',
     '매출 $4.10B(−10%) · 지배기업 귀속 순이익 $480M(1년 전 $271M — 비지배지분 지분 인수 프리미엄을 빼면 보통주 귀속 약 $200M) · 희석 EPS $2.21(1년 전 $0.91) · 분기 배당 $1.25(25% 인상)', 'q1', 'Targa 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 19일 — Q4 2025 실적', '2026-02-19',
     '매출 $4.06B(−7.9%) · 지배기업 귀속 순이익 $545M(1년 전 $351M) · 2025년 지배기업 귀속 순이익 $1.92B(1년 전 $1.31B) · 1월 Stakeholder Midstream 인수 완료(퍼미안 수집·처리)', 'q4', 'Targa 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 5일 — Q3 2025 실적', '2025-11-05',
     '매출 $4.15B(+7.8%) · 지배기업 귀속 순이익 $478M(1년 전 $387M) · 희석 EPS $2.20(1년 전 $1.75)', 'q3', 'Targa 실적 보도자료 (SEC 8-K)'),
]
BB_TAGS = ['PaymentsForRepurchaseOfEquity']   # 자사주 매입 현금 지급 — 기본 태그가 2015년에 멈췄다(Codex r1)
# 다음 실적일: 10/13 회사 보도자료 — 11/5 장 전 발표, 오전 11시(동부) 웹캐스트(Codex r1 필수)
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-11-05', 'src': '10/13 회사 보도자료 — 장 시작 전 발표, 웹캐스트 오전 11시(동부)'}
ANALYST = {'rating': 'Strong Buy', 'n': 22, 'nt': 17, 'mean': 330.53, 'median': 328, 'low': 294, 'high': 359, 'sb': 15, 'b': 6, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'

# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(부문 3개, 외부 매출). 원문 대조: Q2 2026 3,460.3/876.7/103.1(2026-10-22) ──
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
  "trgp:LogisticsAndTransportationMember": [
   "물류·운송(NGL)",
   "#00539b"
  ],
  "trgp:GatheringAndProcessingMember": [
   "수집·처리",
   "#5f95d0"
  ],
  "us-gaap:AllOtherSegmentsMember": [
   "기타(헤지 등)",
   "#b3cce8"
  ]
 },
 "ignore": []
}
