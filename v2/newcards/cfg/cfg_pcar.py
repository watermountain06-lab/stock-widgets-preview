# PCAR(팩카) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 177. 대형 트럭(Kenworth·Peterbilt·DAF), 부품(PACCAR Parts), 금융 서비스(PACCAR Financial).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-29 장 마감 뒤 접수), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 전), StockAnalysis.
# 엔진 입력(2026-10-23): 재무상태표가 트럭·부품·기타와 금융 서비스로 나뉜다(부문 차원으로만 태그).
# 영업이익 줄이 없어 세전이익 − 투자수익으로 합성(DERIVED_OPINC, Q2 2026 981.5 − 86.0 = 895.5 — 금융 서비스 이자비용은 영업).
# 차입금은 트럭·부품·기타 부문만(CAT·DE·GM 규칙) = 0(EV_ZERO_FROM_BY_CIK — 금융 서비스 CP·은행 차입 $4,789M·채권 $9,908M 제외).
# 현금 = 연결 $5,574.7M(현금흐름표 태그), 단기투자 = 트럭 부문 시장성 증권 $3,259.6M(BUILD dim_facts). 2023-02 1.5:1 주식 배당(분할).
BUILD = {'dim_facts': [('us-gaap:MarketableSecuritiesCurrent', 'us-gaap:StatementBusinessSegmentsAxis', 'pcar:TruckPartsAndOtherMember', 'MarketableSecuritiesCurrentTruckPcar')]}
CIK = '0000075362'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -1), '적정'
CO = 'PACCAR'
S_ = 'https://www.sec.gov/Archives/edgar/data/75362/'
SEC = S_
TENQ = S_ + '000119312526323642/pcar-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000119312526318918/pcar-ex99_1.htm', 'q1': S_ + '000119312526183626/pcar-ex99_1.htm',
      'q4': S_ + '000119312526023374/pcar-ex99_1.htm', 'q3': S_ + '000119312525244291/pcar-ex99_1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="pcarFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 금융 자회사 처리, 트럭 경기 순환.
MODEL_NOTE = ('트럭 수요는 운송 경기에 따라 크게 오르내리는 순환 업종이라, 이익이 낮은 해에는 PER이 높게 보인다 — 2025년 1분기 유럽 소송 비용은 이미 최근 4분기 밖이라 지금 PER과는 무관하다. 주가는 8월부터 10월까지 큰 하루 하락 없이 꾸준히 내려왔다(회사 공시로 확인한 원인 없음). '
              '금융 자회사(PACCAR Financial)의 차입금은 대출·리스 자산을 위한 것이라 순차입금·EV에서 뺐다(CAT·DE와 같은 처리) — 금융 서비스 이익(이자비용 차감 뒤)은 영업이익에 들어 있다. '
              '다만 FCF의 설비투자에는 금융 부문의 리스 장비 취득이 빠져 있어, 일반 제조업처럼 FCF를 배당 여력으로 그대로 읽으면 후하다. 영업이익은 세전이익에서 투자수익을 뺀 값이다.')
HEALTH_EXTRA = '재무상태표가 트럭·부품·기타와 금융 서비스로 나뉘어 연결 유동자산·유동부채가 없어 유동비율·당좌비율과 활동성은 계산하지 않는다 — 차입금은 트럭·부품·기타 부문(차입금 없음)만 넣고 금융 서비스 차입금은 뺐으며, 현금은 연결 값이다. 회사 전체가 무차입이라는 뜻이 아니고, 부채비율에는 금융 서비스 차입금이 들어 있다. 금융리스 $1M 안팎은 2025년 말 값이다.'   # 고정 문장
PH = ['CAT', 'DE', 'CMI', 'ITW', 'ETN', 'PH']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '기계·장비 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(PCAR 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·건설이 섞여 있다. 차트에는 기계·장비 6곳만 보인다.')
# 매출(Q2 2026 10-Q) — 트럭 5,253.1 + 부품 1,746.9 + 기타 −3.0 = 트럭·부품·기타 6,997.0, 금융 서비스 549.7 → 총 7,546.7.
SEG = [('트럭', 5253.1, '#0b3d91'), ('부품', 1746.9, '#5b7fc4'), ('금융 서비스', 549.7, '#06275e')]
SEG_ADJ = -3.0
SEG_TITLE = '매출 구성 — 사업별'
SEG_ADJ_LABEL = '기타·상계'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS는 쓰지 않는다). 반응일: 실적 8-K 12:05Z(1월은 13:05Z) — 모두 장 전 → 같은 날.
# DCF 이력 반영일: 10-Q 7/29 20:06Z(장 마감 뒤)인데 7/29부터 — 장 마감 뒤 접수를 같은 날로 보는 전 카드 공통 문제(안건 E45).
# 넣지 않은 8-K: 임원(12/12·1/16·5/1), 주총(5/1). 8~10월 주가 하락(약 −20%, 하루 −5% 넘는 날 없음)은 회사 1차 자료 없음 — 뉴스 대신 MODEL_NOTE에 둔다.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('green', '2026년 7월 28일 — Q2 2026 실적', '2026-07-28',
     '매출 $7.55B · 순이익 $752M · 희석 EPS $1.43(1년 전 $1.37) · 트럭 인도 38,700대 · 부품 매출 최대 $1.75B', 'q2', 'PACCAR 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 28일 — Q1 2026 실적', '2026-04-28',
     '매출 $6.78B(1년 전 $7.44B) · 순이익 $605M · 희석 EPS $1.15(1년 전 $0.96은 유럽 민사 소송 비용 세후 $264.5M을 포함한 값)', 'q1', 'PACCAR 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 27일 — Q4 2025 실적', '2026-01-27',
     '매출 $6.82B(1년 전 $7.91B) · 희석 EPS $1.06(1년 전 $1.66) · 2025년 희석 EPS $4.51(유럽 소송 비용 포함) · 2025년 배당 주당 $2.72(연말 특별배당 $1.40 포함) · 미국 중대형 트럭 수입 관세(Section 232)에 북미 공장 입지가 유리하다고 언급', 'q4', 'PACCAR 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 21일 — Q3 2025 실적', '2025-10-21',
     '매출 $6.67B · 순이익 $590M · 희석 EPS $1.12(1년 전 $1.85) · 트럭 인도 31,900대', 'q3', 'PACCAR 실적 보도자료 (SEC 8-K)'),
]
# 체크포인트 ③ 보정(Fable r1): 반기 지급 배당을 두 배로 연 환산하면 1월 7일 지급한 연말 특별배당 $1.40을 두 번 센다 — 2025년 선언 총액으로(분기 갱신 때 다시 볼 것)
POST = [r'''
assert h.count('배당 지급(연 환산 약 $2.2B)') == 1
h = h.replace('배당 지급(연 환산 약 $2.2B)', '배당(2025년 선언 주당 $2.72, 약 $1.4B — 연말 특별배당 $1.40 포함)')
h = h.replace('연말 특별배당 $1.40 포함)을 넘는지', '연말 특별배당 $1.40 포함)을 넘는지 — FCF에 금융 부문 리스 장비 취득이 빠져 있어 단순 비교로 배당 여력을 확정하지는 못한다', 1)
assert h.count('현금·단기투자가 차입금·리스보다') == 1
h = h.replace('현금·단기투자가 차입금·리스보다', '(금융 서비스 차입금 제외 기준) 현금·단기투자가 차입금·리스보다')
''']
ANALYST = {'rating': 'Buy', 'n': 19, 'nt': 9, 'mean': 132.11, 'median': 125, 'low': 115, 'high': 150, 'sb': 6, 'b': 3, 'h': 10, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 트럭·부품(하위 부문 축) + 금융 서비스(제품 축). 원문 대조: Q2 2026 5,253.1/1,746.9/549.7(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "parts": [
  {"concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], "axis": "us-gaap:SubsegmentsAxis",
   "extra": {"us-gaap:StatementBusinessSegmentsAxis": "pcar:TruckPartsAndOtherMember"},
   "members": {"pcar:TruckSubsegmentMember": ["트럭", "#0b3d91"], "pcar:PartsSubsegmentMember": ["부품", "#5b7fc4"]}},
  {"concepts": ["us-gaap:Revenues"], "axis": "srt:ProductOrServiceAxis", "extra": {},
   "members": {"pcar:FinancialServicesMember": ["금융 서비스", "#06275e"]}}
 ],
 "ignore": []
}
