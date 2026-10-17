# NKE(나이키) v2 카드 설정 — 자동 카드(AUTO). 회계연도 5월 31일. 카드 순위 117(사용자 요청으로 시총 순서 밖에서 먼저 — 2026-10-17 시총 247위).
# 출처: SEC XBRL(+ 표지 주식 수 클래스 합산), Q1 FY27 10-Q(2026-10-02), 실적 보도자료(Q2 FY26~Q1 FY27, 8-K 2.02항 — 모두 장 마감 뒤 접수),
# 8-K(경영진 개편 2025-12-02, 구조조정 2026-03-05, CFO 교체 2026-06-23, 이사 선임 2026-09-16, Pace 프로그램 2026-10-01), StockAnalysis.
# 엔진 입력(2026-10-17): 영업이익 줄이 없다 — 세전이익 − 순이자수익 − 기타 영업외 수익(DERIVED_OPINC, 세전 태그 두 개). 표지 주식 수는 A·B 클래스별로만 내
# companyfacts에 2015년 값만 남았다 → BUILD cover_shares(META 방식, 14.85억 주). 단기투자는 매도가능 채무증권 유동 태그 두 개(EV_TAGS_BY_CIK).
# 감가상각은 Depreciation(~2025-02) + DepreciationDepletionAndAmortization(2023-05~)을 한 줄로(DDA_PARTS_BY_CIK 튜플, 합산 태그는 EXCLUDE_TAGS).
# 4분기 EPS 보도자료 값(FY2026 $0.72·FY2022 $0.90). FY2026 4분기 EPS에 IEEPA 관세 환급 예상 이익 $0.52 포함(일회성 — 판정 계산 규칙이라 손대지 않음).
# 이자비용 태그가 없다(순이자수익 회사) — 이자보상배율 계산 안 함. 10-Q 본문의 이자비용(투자 이자수익 $71M − 순이자수익 $14M = 약 $57M)으로 합성하는 것은 공통 안건.
BUILD = {'cover_shares': True}
CIK = '0000320187'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-08-31', '2025-08-31', '2026-05-31'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-05-31', '2025-05-31'), 'FY2026'
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'Nike'
S_ = 'https://www.sec.gov/Archives/edgar/data/320187/'
SEC = S_
TENQ = S_ + '000032018726000193/nke-20260831.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000032018726000184/q1fy27exhibit991er.htm', 'q4': S_ + '000032018726000076/q4fy26exhibit991er.htm',
      'q3': S_ + '000032018726000026/q3fy26exhibit991er.htm', 'q2': S_ + '000032018725000138/q2fy26exhibit991er.htm'}
LINKS = {'pace': S_ + '000032018726000184/nke-20261001.htm', 'board': S_ + '000032018726000170/a091626pressrelease.htm',
         'cfo': S_ + '000032018726000070/pressrelease062326.htm', 'restr': S_ + '000032018726000017/nke-20260227.htm',
         'slt': S_ + '000032018725000115/sltannouncement.htm'}
FAIRBAND_TITLE = 'id="nkeFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '장기투자'
PH = ['LULU', 'DECK', 'TPR', 'RL', 'TJX', 'ROST']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '의류·신발 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': '의류·신발 PBR 비교', 'psr': '의류·신발 PSR 비교',
                'pcr': '의류·신발 PCR(FCF) 비교', 'evebitda': '의류·신발 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(NKE 제외)와 배수 순위를 매긴 값이다.',
            '유통·자동차·여행·외식·의류 회사가 섞여 있다. PBR은 자사주로 자본이 작거나 음수인 회사가 많아 흔들린다. 차트에는 의류·신발·의류 소매 6곳만 보인다.')
# 매출(Q1 FY27 10-Q 매출 세분 표) — 북미 5,127 + EMEA 3,176 + 중화권 1,180 + 아시아·태평양·중남미 1,463 + Converse 263 = 11,209,
# Converse 263 + 글로벌 브랜드(라이선스 등) 6 + 본사 −2 = 267은 SEG_ADJ(Converse는 XBRL에서 다른 축이라 지도에 못 넣는다). 합 11,213 = 연결 매출.
SEG = [('북미', 5127, '#111111'), ('유럽·중동·아프리카', 3176, '#e85d1f'), ('중화권', 1180, '#b74513'), ('아시아·태평양·중남미', 1463, '#f19972')]
SEG_ADJ = 267
SEG_SUM_LABEL, SEG_ADJ_LABEL = '나이키 브랜드 지역 합', 'Converse·라이선스·본사 매출'
SEG_TITLE = '매출 구성 — 나이키 브랜드 지역 부문(Converse 제외)'
# 손 뉴스: Q1 FY27 실적(10/1)은 같은 8-K의 Pace 프로그램을 함께 보이려고 손으로 쓴다(README). 가이던스·절감 목표는 쓰지 않는다.
# 반응일: 실적 8-K는 모두 동부 20~21시 접수(보도자료 오후 2시 PT 발표) → 다음 거래일. 6/23 8-K 20:24 접수(보도 시각 미표기) → 6/24.
# 3/5 구조조정 8-K 21:32 → 3/6. 9/16 이사 선임 8-K 20:21 → 9/17. 12/2 경영진 개편 8-K 12/2 21:18 → 12/3.
NEWS_RANGE = '2025.12 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 1일 장 마감 뒤 — Q1 FY27 실적·Pace 프로그램', '2026-10-02',
     '매출 $11.21B(−4.3%) · 희석 EPS $0.48(1년 전 $0.49) · 다년 비용 구조 개편 Pace — 세전 비용 약 $1.0B 추가(대부분 퇴직 관련)', 'q1', 'Nike 실적 보도자료·공시 (SEC 8-K)'),
    ('green', '2026년 9월 16일 장 마감 뒤 — Alexandre Arnault 이사 선임', '2026-09-17',
     'LVMH 이사·Moët Hennessy 부CEO · 이사회 12명으로', 'board', 'Nike 공시 (SEC 8-K)'),
    ('green', '2026년 6월 30일 장 마감 뒤 — Q4 FY26 실적', '2026-07-01',
     '매출 $10.97B(−1.1%) · 희석 EPS $0.72(IEEPA 관세 환급 예상 이익 $0.52 포함, 1년 전 $0.14) · FY2026 EPS $2.10', 'q4', 'Nike 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 6월 23일 — CFO 교체 발표', '2026-06-24',
     'Dave Denton(Pfizer CFO)이 8월 중순 CFO 취임 · Matthew Friend 퇴임', 'cfo', 'Nike 공시 (SEC 8-K)'),
    ('red', '2026년 3월 31일 장 마감 뒤 — Q3 FY26 실적', '2026-04-01',
     '매출 $11.28B(+0.1%) · 희석 EPS $0.35(1년 전 $0.54)', 'q3', 'Nike 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 5일 장 마감 뒤 — 조직 개편 비용 공시', '2026-03-06',
     '2월 27일 승인 · 9개월(~2/28) 세전 비용 약 $300M, 대부분 퇴직 관련', 'restr', 'Nike 공시 (SEC 8-K)'),
    ('red', '2025년 12월 18일 장 마감 뒤 — Q2 FY26 실적', '2025-12-19',
     '매출 $12.43B(+0.6%) · 희석 EPS $0.53(1년 전 $0.78)', 'q2', 'Nike 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 2일 장 마감 뒤 — 경영진 개편', '2025-12-03',
     'COO 신설(Venkatesh Alagirisamy) · CTO·최고상업책임자 자리 폐지 · 4개 지역 책임자가 CEO 직속으로', 'slt', 'Nike 공시 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Hold', 'n': 42, 'nt': 27, 'mean': 36.65, 'median': 33, 'low': 19, 'high': 62, 'sb': 9, 'b': 1, 'h': 25, 's': 3, 'ss': 4}
ANALYST_ASOF = '2026-10-17'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(나이키 브랜드 지역 4개, 손 표와 일치). 원문 대조: 10-Q 매출 세분 표 Q1 FY27 5,127/3,176/1,180/1,463,
# 1년 전 5,020/3,331/1,512/1,490. Converse 263(1년 전 366)·라이선스·본사는 SEG_ADJ(2026-10-17) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:SubsegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember",
  "us-gaap:StatementBusinessSegmentsAxis": "nke:NIKEBrandMember"
 },
 "members": {
  "nke:NorthAmericaSegmentMember": [
   "북미",
   "#111111"
  ],
  "nke:EuropeMiddleEastAndAfricaSegmentMember": [
   "유럽·중동·아프리카",
   "#e85d1f"
  ],
  "nke:GreaterChinaSegmentMember": [
   "중화권",
   "#b74513"
  ],
  "nke:AsiaPacificAndLatinAmericaSegmentMember": [
   "아시아·태평양·중남미",
   "#f19972"
  ]
 },
 "ignore": []
}
