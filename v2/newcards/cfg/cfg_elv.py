# ELV(엘리번스 헬스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 122(시총 120위). 관리의료 건강보험(옛 Anthem).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-15), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 동부 장중 접수), 8-K(경영진 개편 2026-02-26,
# CMS 제재 예고 2026-03-02), StockAnalysis.
# 엔진 입력(2026-10-17, 아래 현금흐름 설명은 RIM 전환 전 기록 — 배수·재무 칸은 그대로 쓴다): 투자수익이 'Total revenues' 안(Net investment income, Q2 $704M) — UNH·CVS와 같은 유형. OperatingIncomeLoss 태그는 투자수익·이자·
# 무형자산 상각을 뺀 값이라(Q2 $1,763M) 영업이익 = 세전이익 + 이자비용으로 합성(DERIVED_OPINC, Q2 $2,301M), 투자자산은 영업 자산(INVESTMENTS_OPERATING).
# 감가상각은 현금흐름표 DepreciationAmortizationAndAccretionNet만(DepreciationDepletionAndAmortization 8행은 다른 항목 값이라 EXCLUDE_TAGS).
# 4분기 EPS 보도자료 값(자사주로 주식 수가 줄어 역산이 어긋남 — 2021~2025). 리스는 연간값만(10-K).
# Q1 2026 영업비용에 CMS 통지 관련 충당금 $935M(일회성 — 판정 계산 규칙이라 손대지 않음, 5/27 $342M 지급).
# 보험 RIM(2026-10-17 사용자 결정·research/insurer_rim_prereg.md 1판): 세 번째 심판을 현금흐름 대신 초과이익모형으로(adapters/insurer_rim.py),
# 자기 이력·동종업에서 EV/EBITDA·PCR을 뺀다(보험 플로트 왜곡 — 배수 파일에서 빠지고 점수는 PER·PBR·PSR 셋).
BUILD = {'rim': True, 'drop_multiples': ['pcr', 'evebitda']}
NO_DCF_SKEW = True   # 쏠림 메모는 현금흐름 칸 통계라 RIM 칸에는 넣지 않는다
CIK = '0001156039'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'Elevance Health'
S_ = 'https://www.sec.gov/Archives/edgar/data/1156039/'
SEC = S_
TENQ = S_ + '000115603926000060/elv-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000115603926000058/a2q2026elvearningsrelease.htm', 'q1': S_ + '000115603926000039/a1q2026elvearningsrelease.htm',
      'q4': S_ + '000115603926000006/a4q2025elvearningsrelease.htm', 'q3': S_ + '000119312525244191/d270615dex991.htm'}
LINKS = {'cms': S_ + '000115603926000022/elv-20260302.htm', 'mgmt': S_ + '000115603926000019/elevancehealthpressrelease.htm'}
FAIRBAND_TITLE = 'id="elvFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 ROE (5년 일정 · 최근 4분기 {pct(DCF[\'roe0\']) if DCF.get(\'roe0\') is not None else \'—\'})</span>'
Y2 = (0, 8)
ACT_REASON = ''
NONOP_WHAT = '장기투자'
PH = ['UNH', 'CVS', 'CI', 'HUM', 'CNC', 'HCA']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '건강보험·의료 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': '건강보험·의료 PBR 비교', 'psr': '건강보험·의료 PSR 비교',
                'pcr': '건강보험·의료 PCR(FCF) 비교', 'evebitda': '건강보험·의료 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(ELV 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·의료 서비스 회사가 섞여 있다. 보험사는 매출이 커 PSR이 낮게 나온다. 차트에는 건강보험·의료 서비스 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문 표, 영업 매출) — 건강보험 42,720 + CarelonRx 11,250 + Carelon Services 7,975 = 61,945,
# 본사·기타 6 + 부문 간 제거 −12,125 + 투자수익 704 + 금융상품 손익 −56 = −11,471은 SEG_ADJ. 합 50,474 = 연결 매출(Total revenues).
SEG = [('건강보험', 42720, '#1355e9'), ('CarelonRx(약제)', 11250, '#6d95f2'), ('Carelon Services', 7975, '#0d3ca6')]
SEG_ADJ = -11471
SEG_SUM_LABEL, SEG_ADJ_LABEL = '부문 합', '부문 간 제거·투자수익 등'
SEG_TITLE = '매출 구성 — 보고 부문별(부문 간 거래 제거 전)'
# 손 뉴스: Q2 실적(7/15)은 같은 10-Q의 CMS 종결(7/13 통지)을 함께 적으려고 손으로 쓴다. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일: 실적 8-K는 모두 동부 10~11시 접수(장중) → 같은 날. CMS 8-K 3/2 11:03 → 3/2. 경영진 개편 8-K 2/26 19:59 → 2/27.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('red', '2026년 7월 15일 — Q2 2026 실적', '2026-07-15',
     '매출 $50.47B(+1.4%) · 희석 EPS $6.71(1년 전 $7.72) · CMS가 7월 13일 제재 없이 절차 종결 통지(10-Q) — 충당금 $935M 중 $342M 지급, 잔여 $593M은 부채로 남음', 'q2', 'Elevance Health 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 22일 — Q1 2026 실적', '2026-04-22',
     '매출 $50.18B(+2.6%) · 희석 EPS $8.00(1년 전 $9.61) · 영업비용에 CMS 통지 관련 충당금 $935M', 'q1', 'Elevance Health 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 2일 — CMS 메디케어 어드밴티지 제재 예고', '2026-03-02',
     '2023년 4월 3일 이전 진료분의 위험 조정 자료 제출 관련 — 3월 31일부터 MA-PD 신규 가입 정지 예고(기존 가입자 혜택은 그대로)', 'cms', 'Elevance Health 공시 (SEC 8-K)'),
    ('red', '2026년 2월 26일 장 마감 뒤 — 경영진 개편', '2026-02-27',
     'Carelon 사장 Peter Haytaian 5월 4일 퇴임 · CFO Mark Kaye가 Carelon까지 맡고 Felicia Norwood가 통합 건강보험 조직을 이끈다', 'mgmt', 'Elevance Health 공시 (SEC 8-K)'),
    ('green', '2026년 1월 28일 — Q4 2025 실적', '2026-01-28',
     '매출 $49.75B(+9.5%) · 희석 EPS $2.47(1년 전 $1.81) · 2025년 EPS $25.21', 'q4', 'Elevance Health 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 21일 — Q3 2025 실적', '2025-10-21',
     '매출 $50.71B(+12.4%) · 희석 EPS $5.32(1년 전 $4.36)', 'q3', 'Elevance Health 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 22, 'nt': 18, 'mean': 451.39, 'median': 465, 'low': 393, 'high': 498, 'sb': 12, 'b': 2, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-17'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-Q 부문 표 영업 매출 Q2 2026 42,720/11,250/7,975, 1년 전 41,582/10,643/7,441.
# Carelon 합계·본사는 ignore, 부문 간 제거·투자수익은 SEG_ADJ(2026-10-17) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "elv:OperatingRevenue"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "elv:HealthBenefitsSegmentMember": [
   "건강보험",
   "#1355e9"
  ],
  "elv:CarelonRxSegmentMember": [
   "CarelonRx(약제)",
   "#6d95f2"
  ],
  "elv:CarelonServicesSegmentMember": [
   "Carelon Services",
   "#0d3ca6"
  ]
 },
 "ignore": [
  "elv:TotalCarelonMember",
  "us-gaap:CorporateAndOtherMember"
 ]
}
