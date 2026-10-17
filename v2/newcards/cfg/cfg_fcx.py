# FCX(프리포트-맥모란) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 116.
# 출처: SEC XBRL(+ 인라인 XBRL 보충·회사 고유 태그), Q2 2026 10-Q(2026-08-06), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 시작 전 접수),
# 8-K(Grasberg 사고 2025-10-05·재가동 계획 11-18, 인도네시아 정부 MOU 2026-02-18, 3분기 생산 현황 10-02), StockAnalysis.
# 엔진 입력(2026-10-17): EPS — 10-K 연간 EPS를 IncomeLossFromContinuingOperationsPerDilutedShare로만 내 2022년부터 4분기가 안 생겨 EPS 이력이 2022-09에 멈췄다(PER 26배 대 실제 약 34배)
# → eps_tag 두 개(DELL 전례). 4분기 EPS 보도자료 값(2025 $0.28·2024 $0.19). 우선주 태그가 2009년($832M)에 멈춰 EV_TAGS_BY_CIK preferred = [].
# 이자비용은 순이자(InterestIncomeExpenseNet, vendor/fetch_financials CONCEPTS_BY_CIK). 재고는 합계 줄이 없어 제품 + 자재 + 유동 광석 비축분(company_tags·overlay SUM·INV_SUM_BY_CIK, NEM 전례).
# 비지배지분 $12.1B(PT Freeport Indonesia — FCX 지분 48.76%·Cerro Verde 등 — 엔진이 EV에 더한다). 1분기 영업이익에 Grasberg 사고 보험금 이익 $699M 포함(일회성 — 판정 계산 규칙이라 손대지 않음).
BUILD = {'overlay': True, 'eps_tag': 'EarningsPerShareDiluted,IncomeLossFromContinuingOperationsPerDilutedShare',
         'company_tags': [('fcx:Product', 'InventoryProductFcx'),   # 빌린 이름 — overlay_feed SUM·활동성 INV_SUM_BY_CIK가 재고에 더한다
                          ('fcx:InventoryMillandStockpilesonLeachPadsCurrent', 'InventoryStockpilesCurrentFcx')]}
NI_TAGS = ['NetIncomeLossAvailableToCommonStockholdersBasic', 'NetIncomeLoss']   # 분기 순이익(주주 귀속)을 주로 보통주 귀속 태그로 낸다 — NetIncomeLoss는 일부 분기뿐, ProfitLoss는 비지배지분 몫 포함
CIK = '0000831259'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Freeport-McMoRan'
S_ = 'https://www.sec.gov/Archives/edgar/data/831259/'
SEC = S_
TENQ = S_ + '000083125926000036/fcx-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000083125926000033/a2q2026exhibit991.htm', 'q1': S_ + '000083125926000021/a1q2026exhibit991.htm',
      'q4': S_ + '000083125926000006/a4q2025exhibit991.htm', 'q3': S_ + '000083125925000048/a3q2025exhibit991.htm'}
LINKS = {'ops': S_ + '000083125926000043/fcx_261002.htm', 'mou': S_ + '000083125926000014/fcxnewrelease21826.htm',
         'restart': S_ + '000083125925000052/fcx_251118.htm', 'mud': S_ + '000083125925000046/fcx_251005.htm'}
FAIRBAND_TITLE = 'id="fcxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (15, 40)
ACT_REASON = ''
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-27', 'src': '10/2 8-K 공시 — 장 시작 전'}
NONOP_WHAT = '장기투자'
PH = ['NEM', 'NUE', 'LIN', 'APD', 'SHW', 'ECL']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소재 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': '소재 PBR 비교', 'psr': '소재 PSR 비교',
                'pcr': '소재 PCR(FCF) 비교', 'evebitda': '소재 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(FCX 제외)와 배수 순위를 매긴 값이다.',
            '광산·화학·산업용 가스·건자재·포장 회사가 섞여 있다. 차트에는 광산·철강·화학 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문 표, 외부 고객) — XBRL 보고 부문: 미국(Morenci 17 + 정련·로드 2,228) + 남미(Cerro Verde 1,159) + 인도네시아(Grasberg 1,482) + 스페인 제련(Atlantic Copper 1,024) = 5,910,
# 나머지 1,119(다른 미국·남미 광산, 몰리브덴 가공, 본사·상계 — XBRL MaterialReconcilingItems)는 SEG_ADJ. 합 7,029 = 연결 매출.
SEG = [('미국(정련·로드+Morenci)', 2245, '#b0632a'), ('인도네시아', 1482, '#7f471e'), ('남미(Cerro Verde)', 1159, '#d8925d'), ('스페인 제련', 1024, '#5a6b7a')]
SEG_ADJ = 1119
SEG_SUM_LABEL, SEG_ADJ_LABEL = '보고 부문 합', '기타 부문 외부 고객 매출'
SEG_TITLE = '매출 구성 — 보고 부문별(외부 고객, 다른 광산·본사 제외)'
# 손 뉴스: 10/2 3분기 생산 현황(8-K 2.02항이지만 실적 아님)을 넣으므로 Q2 실적(7/23)도 손으로 쓴다(README). 가이던스는 쓰지 않는다.
# 반응일: 실적 8-K는 모두 동부 08시 전후 접수 → 같은 날. 생산 현황 10/2 08:35 → 10/2. MOU 8-K는 2/23 18:03(동부) 접수지만 보도자료는 2/18이라 2/18(그날 공개).
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 2일 — 3분기 잠정 생산 현황 공시', '2026-10-02',
     '구리 생산 약 8.3억 파운드 · 금 약 23만 온스, 인도네시아 정련 금 약 6만 온스 판매가 4분기로 · PTFI 제련소 8월 말 재가동', 'ops', 'Freeport 공시 (SEC 8-K)'),
    ('red', '2026년 7월 23일 — Q2 2026 실적', '2026-07-23',
     '매출 $7.03B(−7.3%) · 희석 EPS $0.68(1년 전 $0.53)', 'q2', 'Freeport 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 23일 — Q1 2026 실적', '2026-04-23',
     '매출 $6.23B(+8.8%) · 희석 EPS $0.61(1년 전 $0.24) — Grasberg 사고 보험금 이익 포함', 'q1', 'Freeport 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 18일 — 인도네시아 정부와 운영권 연장 양해각서', '2026-02-18',
     '자원 소진 때까지 운영권 연장에 합의(인도네시아 정부의 개정 광업 허가 발급이 조건) · 2041년에 PTFI 지분 12% 이전 · 탐사·지역 지원 확대', 'mou', 'Freeport 공시 (SEC 8-K)'),
    ('red', '2026년 1월 22일 — Q4 2025 실적', '2026-01-22',
     '매출 $5.63B(−1.5%) · 희석 EPS $0.28(1년 전 $0.19) · 2025년 EPS $1.52', 'q4', 'Freeport 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 18일 — Grasberg 단계적 재가동 계획', '2025-11-18',
     '영향받지 않은 DMLZ·Big Gossan 지하 광산은 10월 말 생산 재개 · Grasberg Block Cave는 2026년 2분기부터 단계적 재가동', 'restart', 'Freeport 공시 (SEC 8-K)'),
    ('green', '2025년 10월 23일 — Q3 2025 실적', '2025-10-23',
     '매출 $6.97B(+2.7%) · 희석 EPS $0.46(1년 전 $0.36)', 'q3', 'Freeport 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 5일(일) — Grasberg 사고 실종자 수습 발표', '2025-10-06',
     '9월 8일 Grasberg Block Cave 광산 이류(mud rush) 사고로 실종된 5명이 숨진 채 발견 — 9월 20일 2명 포함 7명 사망', 'mud', 'Freeport 공시 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 15, 'mean': 80.8, 'median': 80, 'low': 72, 'high': 92, 'sb': 12, 'b': 6, 'h': 4, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-17'


# ── 자동 카드 — 부문 지도는 손으로(제안기가 남미·인도네시아 같은 금액 1,482를 엇갈려 짝지음). 원문 대조: 10-Q 부문 표 외부 고객 Q2 2026 Morenci 17·Cerro Verde 1,159·
# Grasberg 1,482·정련·로드 2,228·Atlantic 1,024, 1년 전 63·836·3,419·1,692·815, 나머지(MaterialReconcilingItems) 1,119·757(2026-10-17) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:Revenues"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember",
  "srt:MajorCustomersAxis": "fcx:UnaffiliatedCustomersMember"
 },
 "members": {
  "fcx:MorenciMember": [
   "미국(정련·로드+Morenci)",
   "#b0632a"
  ],
  "fcx:RodAndRefiningSegmentMember": [
   "미국(정련·로드+Morenci)",
   "#b0632a"
  ],
  "fcx:GrasbergSegmentMember": [
   "인도네시아",
   "#7f471e"
  ],
  "fcx:CerroVerdeMember": [
   "남미(Cerro Verde)",
   "#d8925d"
  ],
  "fcx:AtlanticCopperSmeltingAndRefiningSegmentMember": [
   "스페인 제련",
   "#5a6b7a"
  ]
 },
 "ignore": []
}
