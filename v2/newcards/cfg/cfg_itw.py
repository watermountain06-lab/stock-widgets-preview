# ITW(일리노이 툴 웍스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 157(시총 155위). 산업용 부품·장비 7개 사업(자동차 부품, 식품 장비, 계측·전자, 용접, 폴리머·유체, 건설 자재, 특수 제품).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-06), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 동부 오전 접수, 보도자료는 장 전), 8-K(사채 8/13, 신용 약정 2/23), StockAnalysis.
# 엔진 입력(2026-10-22): 세전이익 = IncomeLossIncludingPortionAttributableToNoncontrollingInterest(build_dcf PRETAX_TAG_BY_CIK·vendor CONCEPTS_BY_CIK — 표준 세전 태그는 2021-06에 멈춰 세율이 법정 21%였다).
# 무형자산 상각(손익계산서 줄)은 회사 고유 태그 itw:AmortizationandImpairmentofIntangibleAssets → BUILD company_tags로 AmortizationOfIntangibleAssets에(감가상각 $328M → $400M).
# 차입금 $9,694M = 단기 3,145(CP 2,100 포함) + 장기 6,549(DEBT_TOTAL_TAG — 기본은 $8,649M), 매출원가 = CostOfGoodsAndServicesSold(활동성 COGS_TAG_BY_CIK — CostOfRevenue는 부문 변동원가). 현금 $839M. 운용리스 $242M은 2025-12 10-K 값. 4분기 EPS 2022·2024 보도자료 값.
BUILD = {'company_tags': [('itw:AmortizationandImpairmentofIntangibleAssets', 'AmortizationOfIntangibleAssets')]}
CIK = '0000049826'
NI_TAGS = ['ProfitLoss']   # 순이익을 ProfitLoss로만 낸다(NetIncomeLoss 분기 없음 — 비지배 $1M 수준이라 같은 값, 2026-10-22)
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Illinois Tool Works'
S_ = 'https://www.sec.gov/Archives/edgar/data/49826/'
SEC = S_
TENQ = S_ + '000004982626000049/itw-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000004982626000047/a20260630-2q26ex991pressre.htm', 'q1': S_ + '000004982626000025/a20260331-1q26ex991pressre.htm',
      'q4': S_ + '000004982626000003/a20251231-4q25ex991pressre.htm', 'q3': S_ + '000004982625000050/a20250930-3q25ex991pressre.htm'}
LINKS = {'notes': S_ + '000119312526349149/d23818d8k.htm'}
FAIRBAND_TITLE = 'id="itwFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 자사주로 작은 자본, 사업 매각 차익 이력.
MODEL_NOTE = ('자사주 매입을 오래 해 장부상 자본이 작아 PBR과 부채비율이 높게 나온다. 2024년 3분기 EPS에는 사업 매각 차익이 들어 있어, 그 분기와 비교하면 EPS가 줄어든 것처럼 보인다.')   # Codex r1
PH = ['EMR', 'ETN', 'PH', 'DOV', 'GWW', 'MMM']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '산업재 다각화 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(ITW 제외)와 배수 순위를 매긴 값이다.',
            '항공우주·운송·서비스·건설이 섞여 있다. 차트에는 다각화 산업재 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 부문 간 거래 포함) — 자동차 857 + 계측·전자 769 + 식품 장비 692 + 용접 549 + 건설 494 + 폴리머·유체 476 + 특수 468 = 4,305, 부문 간 거래 −4 → 4,301. 1년 전 845/686/680/479/473/438/455.
SEG = [('자동차 부품(OEM)', 857.0, '#d81e05'), ('계측·전자', 769.0, '#ef6a5a'), ('식품 장비', 692.0, '#8e1403'), ('용접', 549.0, '#f4a582'),
       ('건설 자재', 494.0, '#92c5de'), ('폴리머·유체', 476.0, '#4393c3'), ('특수 제품', 468.0, '#2166ac')]
SEG_ADJ = -4.0
SEG_TITLE = '매출 구성 — 사업별(부문 간 거래 포함)'
SEG_ADJ_LABEL = '부문 간 거래'
# 손 뉴스: 최신 실적(Q2 2026, 7/28)도 손으로 — 8/14 사채 손 항목보다 앞선 자동 항목은 빠지므로. 사채 8-K 2026-08-13T20:05Z = 16:05(장 뒤) → 8/14(Codex r1 권장). 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K 2025-10-24T13:43Z·2026-02-03T14:48Z·04-30T13:14Z = 동부 9~10시(보도자료는 장 전) → 같은 날.
# 넣지 않은 8-K: 사채 $1.5B(8/13 — 4.65% 2029년), 신용 약정(2/23), 회계책임자 은퇴(5/22), 주총(5/12).
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 13일 장 마감 뒤 — 사채 $1.5B 발행', '2026-08-14',
     '4.65% 2029년 만기 — 기업어음(CP) 상환용이라 차입금이 그만큼 늘지는 않는다', 'notes', 'ITW 공시 (SEC 8-K)'),
    ('green', '2026년 7월 28일 — Q2 2026 실적', '2026-07-28',
     '매출 $4.30B(+6.1%, 유기적 +4.5%) · 희석 EPS $2.84(+10%) · 영업이익률 26.7%', 'q2', 'ITW 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 30일 — Q1 2026 실적', '2026-04-30',
     '매출 $4.02B(+4.6%) · 희석 EPS $2.66(+12%) · 영업이익률 25.4%', 'q1', 'ITW 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 3일 — Q4 2025 실적', '2026-02-03',
     '매출 $4.09B(+4.1%, 유기적 +1.3%) · 희석 EPS $2.72(1년 전 $2.54) · 영업이익률 26.5% · 2025년 매출 $16.0B(+0.9%)', 'q4', 'ITW 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 24일 — Q3 2025 실적', '2025-10-24',
     '매출 $4.06B(+2.3%) · 희석 EPS $2.81(1년 전 $3.91 — 사업 매각 차익 포함) · 영업이익률 27.4% 사상 최고', 'q3', 'ITW 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 16, 'nt': 9, 'mean': 282, 'median': 286, 'low': 254, 'high': 300, 'sb': 1, 'b': 0, 'h': 12, 's': 0, 'ss': 3}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(부문 7개). 원문 대조: Q2 2026 857/769/692/549/494/476/468, 1년 전 845/686/680/479/473/438/455(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "itw:AutomotiveOEMSegmentMember": [
   "자동차 부품(OEM)",
   "#d81e05"
  ],
  "itw:TestandMeasurementandElectronicsSegmentMember": [
   "계측·전자",
   "#ef6a5a"
  ],
  "itw:FoodEquipmentSegmentMember": [
   "식품 장비",
   "#8e1403"
  ],
  "itw:WeldingSegmentMember": [
   "용접",
   "#f4a582"
  ],
  "itw:ConstructionProductsSegmentMember": [
   "건설 자재",
   "#92c5de"
  ],
  "itw:PolymersAndFluidsSegmentMember": [
   "폴리머·유체",
   "#4393c3"
  ],
  "itw:SpecialtyProductsSegmentMember": [
   "특수 제품",
   "#2166ac"
  ]
 },
 "ignore": []
}
