# CMI(커민스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 151(시총 149위). 디젤·천연가스 엔진, 부품, 유통, 발전기(데이터센터 비상 전원), Accelera(수소·전동화).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-04), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 동부 오전 7~8시대 접수 = 장 전), StockAnalysis.
# 엔진 입력(2026-10-22): 차입금 $7,695M = 단기 은행 차입 459 + CP 348 + 1년 안 151 + 장기 6,737(DEBT_TOTAL_TAG — 단기 은행 차입이 빠져 $7,236M이었다; 장기 태그가 금융리스 포함이라 리스에서 금융리스를 또 빼지 않음).
# 현금 $3,179M · 시장성 증권 $745M · 비지배지분 $1,059M = 원문. 지분법 투자(합작사, $2,265M)는 그 이익이 영업이익 위 "Equity, royalty and interest income"에 들어 있어 따로 더하지 않는다.
# 최근 4분기 영업이익에 Accelera 수소 사업 정리 비용이 들어 있다(Q3 2025 $240M·Q4 $218M 전해조, Q1 2026 저압 연료전지 매각 등 $199M — 보도자료 금액, 영업비용에 들어 있다; Codex r1).
BUILD = {}
NI_TAGS = ['NetIncomeLossAvailableToCommonStockholdersBasic', 'NetIncomeLoss']   # Cummins 귀속 순이익 — NetIncomeLoss 태그가 2024 분기에 비어 fill이 멈췄다(2026-10-22)
CIK = '0000026172'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Cummins'
S_ = 'https://www.sec.gov/Archives/edgar/data/26172/'
SEC = S_
TENQ = S_ + '000002617226000029/cmi-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000002617226000026/cmi2026q28-kex99.htm', 'q1': S_ + '000002617226000013/cmi2026q18-kex99.htm',
      'q4': S_ + '000002617226000004/cmi2025q48-kex99.htm', 'q3': S_ + '000002617225000036/cmi2025q38-kex99.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="cmiFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 최근 4분기 EPS에는 Accelera 정리 비용이 들어 있다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). Accelera 정리 비용, 트럭 경기, 데이터센터 발전기.
MODEL_NOTE = ('최근 4분기 영업이익에는 Accelera의 전해조 사업 축소와 저압 연료전지 사업 매각에 따른 일회성 비용이 들어 있어 최근 이익률이 낮게 나온다. '   # Codex r1
              '엔진·부품 매출은 북미 트럭 경기를, 발전기 매출은 데이터센터 비상 전원 수요를 따라 움직인다. 합작사 지분 이익은 영업이익 안에 있어 지분법 투자는 따로 더하지 않았다.')
PH = ['CAT', 'PCAR', 'DE', 'ETN', 'GEV', 'PH']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '기계·전력 장비 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(CMI 제외)와 배수 순위를 매긴 값이다.',
            '항공우주·운송·서비스·건설이 섞여 있다. 차트에는 기계·전력 장비 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문 외부 매출) — 유통 3,320 + 부품 2,431 + 엔진 2,349 + 발전 1,217 + Accelera 140 = 9,457 = 연결 매출. 1년 전 3,034/2,295/2,162/1,054/98 → 8,643.
SEG = [('유통(Distribution)', 3320.0, '#d71920'), ('부품(Components)', 2431.0, '#e86a6f'), ('엔진(Engine)', 2349.0, '#8f1015'),
       ('발전(Power Systems)', 1217.0, '#f2a7aa'), ('Accelera(수소·전동화)', 140.0, '#4caf50')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별 외부 매출'
# 손 뉴스: 최신 실적(Q2 2026, 8/4)도 손으로 — 배당 인상($2.00→$2.20)을 적으려고(Fable 2026-10-22 필수). 가이던스·조정 EPS·EBITDA는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 2025-11-06T12:37Z = 07:37(장 전) → 11/6, 2026-02-05T12:54Z → 2/5, 05-05T11:40Z → 5/5.
# 넣지 않은 8-K: 주총(5/14).
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 4일 — Q2 2026 실적 · 배당 인상', '2026-08-04',
     '매출 $9.5B(+9.4%) · 희석 EPS $6.73(1년 전 $6.43) · 분기 배당 $2.00 → $2.20(+10%, 17년 연속 인상) · 데이터센터 비상 전원 수요로 2분기 기준 최대 실적', 'q2', 'Cummins 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 5일 — Q1 2026 실적', '2026-05-05',
     '매출 $8.4B(+3%) · 희석 EPS $4.71(1년 전 $5.96) — 저압 연료전지 사업 매각·약정 취소·고객 청구 정리 순비용 $199M(주당 $1.44, 회사가 순 $175M 지급) 포함 · 발전 부문 분기 최대', 'q1', 'Cummins 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 5일 — Q4 2025 실적', '2026-02-05',
     '매출 $8.5B(+1%) · 희석 EPS $4.27(1년 전 $3.02) — 전해조 사업 비용 $218M 포함 · 전해조는 신규 영업을 중단할 계획(현지 협의 전제, 기존 고객 약정은 이행 — 2/10 10-K) · 2025년 매출 $33.7B(−1%)·EPS $20.50', 'q4', 'Cummins 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 6일 — Q3 2025 실적', '2025-11-06',
     '매출 $8.3B(−2%) · 희석 EPS $3.86(1년 전 $5.86) — 전해조 사업 비현금 비용 $240M(주당 $1.73) 포함·전략 검토 시작', 'q3', 'Cummins 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 22, 'nt': 15, 'mean': 716.67, 'median': 741, 'low': 557, 'high': 845, 'sb': 11, 'b': 4, 'h': 7, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(부문 5개, 외부 매출). 원문 대조: Q2 2026 3,320/2,431/2,349/1,217/140, 1년 전 3,034/2,295/2,162/1,054/98(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "cmi:DistributionMember": [
   "유통(Distribution)",
   "#d71920"
  ],
  "cmi:ComponentsMember": [
   "부품(Components)",
   "#e86a6f"
  ],
  "cmi:EngineMember": [
   "엔진(Engine)",
   "#8f1015"
  ],
  "cmi:PowerSystemsMember": [
   "발전(Power Systems)",
   "#f2a7aa"
  ],
  "cmi:AcceleraMember": [
   "Accelera(수소·전동화)",
   "#4caf50"
  ]
 },
 "ignore": []
}
