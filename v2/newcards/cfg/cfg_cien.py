# CIEN(시에나) v2 카드 설정 — 자동 카드(AUTO). 회계연도 10월 말 무렵 토요일(52·53주). 카드 순위 186. 광통신 네트워크 장비(Networking Platforms)·소프트웨어·서비스.
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-09-03 장 마감 뒤 접수, 분기 끝 8/1), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 보도자료는 장 전, 8:30 콜), 8-K(전환사채 2026-06), StockAnalysis. 사전 조사 자료표 scratchpad pre/CIEN.md.
# 엔진 입력(2026-10-23): D&A = 감가상각 + 현금흐름표 무형자산 상각(회사 고유 태그 → company_tags·DDA_PARTS_BY_CIK), 차입금 = 장기 $3,229.8M(2031 만기 0% 전환사채 장부 $2,832M(원금 $2.875B) + 2030 4% 사채 $398M — 6월 발행 대금으로 텀론 상환), 인수 $231.1M(build_dcf ACQ_FIXED, Nubis), 4분기 EPS FY2024 보도자료 값(Q4_EPS_OVERRIDE — 14주 분기).
BUILD = {'company_tags': [('cien:AmortizationOfIntangibleAssetsExcludingAmortizationIncludedInPropertyPlantAndEquipment', 'AmortizationOfIntangibleAssetsCashFlowCien')]}
CIK = '0000936395'
CUR, YO, QO = '2026-08-01', '2025-08-02', '2026-05-02'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-11-01', '2024-11-02'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Ciena'
S_ = 'https://www.sec.gov/Archives/edgar/data/936395/'
SEC = S_
TENQ = S_ + '000162828026060361/cien-20260801.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000162828026060245/ex9912026q3earningspressre.htm', 'q2': S_ + '000162828026040614/ex9912026q2earningspressre.htm',
      'q1': S_ + '000162828026015006/ex9912026q1earningspressre.htm', 'q4': S_ + '000162828025056425/ex9912025q4earningspressre.htm'}
LINKS = {'cv': S_ + '000119312526267607/d118604d8k.htm'}
FAIRBAND_TITLE = 'id="cienFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 80)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('AI 데이터센터 연결 수요로 2026 회계연도 들어 매출·이익이 급증해, 이익이 적던 시기와 많은 시기의 배수가 한 이력에 섞여 있다 — 주가가 실적 발표 때마다 크게 움직였다. '
              '과거 PER 적용 참고범위는 이익이 적던 시기의 매우 높은 PER을 급증한 최근 EPS에 곱한 값이라 참고용일 뿐이다. 현금흐름 내재가치가 낮은 주된 이유는 보수·기본 시나리오의 이익률이 급증 전 시기 값(2년·5년 중앙값)이기 때문이다. '
              '6월 발행 무이자 전환사채는 원금을 현금으로 갚고, 헤지·워런트로 실질 희석은 주가가 약 $1,000을 넘을 때부터다. 2025 회계연도 4분기 이익에는 인수한 연구개발 자산의 개발 포기에 따른 일회성 손상과 세금 혜택이 들어 있다.')
PH = ['ANET', 'CSCO', 'APH', 'DELL', 'QCOM']   # 비교 자료(카드 유니버스 IT)에 값이 있는 종목만
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '네트워크·부품·하드웨어 5곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(CIEN 제외)과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 섞여 있다. 차트에는 네트워크·부품·하드웨어 5곳만 보인다.')
# 매출(Q3 FY26 10-Q 부문) — Networking Platforms 1,355.7 + Platform Software and Services 98.7 + Blue Planet 23.2 + Global Services 193.6 = 1,671.1(= 총매출).
SEG = [('네트워킹 플랫폼', 1355.675, '#d81e05'), ('글로벌 서비스', 193.592, '#e86a5a'), ('플랫폼 소프트웨어·서비스', 98.657, '#900f00'), ('Blue Planet 자동화', 23.205, '#f2b3aa')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다), 전환사채.
# 반응일: 보도자료는 장 전(8:30 콜) — 8-K 2025-12-11T17:07Z·2026-03-05T17:49Z·06-04T15:05Z·09-03T15:07Z(장중) → 같은 날. 전환사채 발표 8-K 2026-06-08T15:08Z(장중) → 6/8(확정 8-K 6/12T00:21Z).
# 넣지 않은 8-K: Nubis 인수 합의·완료(2025-09·10 — 범위 앞), 임원 계약(12/3), 주총(3/31), 전환사채 발행 계획(6/8).
NEWS_RANGE = '2025.12 ~ 2026.09'
NEWS = [
    ('red', '2026년 9월 3일 — Q3 FY26 실적', '2026-09-03',
     '매출 $1.67B(1년 전 $1.22B) · GAAP 순이익 $266M · 희석 EPS $1.83(1년 전 $0.35)', 'q3', 'Ciena 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 6월 8일 — 무이자 전환사채 발행 발표', '2026-06-08',
     '2031년 만기 0% 전환사채 발행 계획 발표(장중) — 6/11 원금 $2.875B(추가 옵션 포함, 전환가 약 $747)로 확정, 대금 약 $1.14B로 텀론 상환·자사주 약 $140M 매입, 헤지·워런트로 실질 희석은 약 $1,000부터', 'cv', 'Ciena 공시 (SEC 8-K)'),
    ('red', '2026년 6월 4일 — Q2 FY26 실적', '2026-06-04',
     '매출 $1.57B · GAAP 순이익 $218M · 희석 EPS $1.49(1년 전 $0.06)', 'q2', 'Ciena 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 5일 — Q1 FY26 실적', '2026-03-05',
     '매출 $1.43B · GAAP 순이익 $150M · 희석 EPS $1.03(1년 전 $0.31)', 'q1', 'Ciena 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 11일 — Q4 FY25 실적', '2025-12-11',
     '매출 $1.35B · GAAP 순이익 $19.5M · 희석 EPS $0.13(1년 전 $0.25) — 인수 연구개발 자산 개발 포기 손상 $89M 등 손상·구조조정 $107M과 세금 혜택 포함', 'q4', 'Ciena 실적 보도자료 (SEC 8-K)'),
]
# 머리 '적정주가 (배수 기준)' 이름 보정(Codex·Fable r1) — 이익 급증기라 과거 PER을 곱한 참고 범위
POST = [r'''
h = h.replace('<span class="meta-label">적정주가 (배수 기준)</span>', '<span class="meta-label">과거 PER 적용 참고범위</span>', 1)
''']
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 17, 'mean': 512.82, 'median': 548, 'low': 347, 'high': 658, 'sb': 11, 'b': 5, 'h': 5, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 부문 4개(수동 지도). 원문 대조: Q3 FY26 1,355.7/193.6/98.7/23.2(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"cien:NetworkingPlatformsSegmentMember": ["네트워킹 플랫폼", "#d81e05"], "cien:GlobalServicesMember": ["글로벌 서비스", "#e86a5a"],
             "cien:PlatformSoftwareandServicesSegmentMember": ["플랫폼 소프트웨어·서비스", "#900f00"], "cien:BluePlanetAutomationSoftwareandServicesSegmentMember": ["Blue Planet 자동화", "#f2b3aa"]},
 "ignore": []
}
