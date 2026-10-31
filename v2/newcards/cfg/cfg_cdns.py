# CDNS(케이던스 디자인 시스템즈) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 반도체 설계 소프트웨어(EDA) — 핵심 EDA 68%, 설계 IP 15%, 시스템 설계·해석 17%(Q2 2026 매출 비중).
# 출처: SEC XBRL + 인라인 XBRL 보충(BUILD overlay — companyfacts에 7/28 Q2 10-Q가 없다), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/CDNS.md.
# 엔진 입력(2026-10-25): 차입금 = 무담보 사채 $2,482M(DEBT_TOTAL_TAG UnsecuredLongTermDebt), 현금 $1,440M(2/23 Hexagon 설계·엔지니어링 사업 인수로 $3.0B에서 줄었다), 최근 4분기 인수 $2.41B.
# 일회성: 회사 조정에서 주식 보상·상각을 뺀 일회성 성격(인수·통합 +0.59, 구조조정 +0.11, 투자 이익 −0.49 등)은 최근 4분기 순합 주당 약 +0.4(GAAP EPS 5.03의 약 8%) — 방향이 반대라 대부분 상쇄.
BUILD = {'overlay': True}
CIK = '0000813672'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, -1, -2), '적정~고평가'
CO = 'Cadence'
S_ = 'https://www.sec.gov/Archives/edgar/data/813672/'
SEC = S_
TENQ = S_ + '000081367226000092/cdns-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000081367226000089/cdns07272026ex9901.htm', 'q1': S_ + '000081367226000044/cdns04272026ex9901.htm',
      'q4': S_ + '000081367226000013/cdns02172026ex9901.htm', 'q3': S_ + '000081367225000144/cdns10272025ex9901.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="cdnsFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = '소프트웨어·IP 라이선스 회사라 재고 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('2026년 2월 Hexagon 설계·엔지니어링 사업($3.0B — 현금 $2.1B + 주식 $0.9B)을 인수해 1분기부터 매출과 무형자산 상각이 커졌다 — 1년 전과의 비교에 인수 효과가 섞여 있다(인수 사업을 1년 전에도 포함한 회사 추정 기준 2분기 성장률 약 +17.5%). 현금흐름 모델의 최근 4분기 재투자에 인수 현금 $2.1B가 통째로 들어가고 매출은 4개월분뿐이라 기본 시나리오 값이 낮게 나온다(인수를 빼면 약 $69). '
              '1년 전 2분기에는 미국 수출 규제 위반 합의 손실($128.5M)이 있어 2분기 EPS 증가율이 부풀어 보인다. SEC 요약 자료에 최신 10-Q가 아직 없어 원문 인라인 XBRL로 채웠다.')
PH = ['MSFT', 'ORCL', 'CRM', 'PLTR', 'ASML', 'KLAC']   # 비교 자료(카드 유니버스 IT)에 값이 있는 종목만 — SNPS·ADSK·ADBE·INTU·NOW는 값 없음
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소프트웨어·반도체 장비 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(CDNS 제외)과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 섞여 있다. 차트에는 소프트웨어·반도체 장비 6곳만 보인다.')
# 매출(Q2 2026 10-Q 매출 유형) — 제품·유지보수 1,430.7 + 서비스 153.8 = 1,584.5(단일 보고 부문).
SEG = [('제품·유지보수', 1430.7, '#d71920'), ('서비스', 153.8, '#f07a7f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 유형별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:02~16:03 동부) → 다음 거래일. 넣지 않은 8-K: 인수 종결(2/23, 3.02항 주식 발행), 이사 선임, 주총.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 27일 장 마감 뒤 — Q2 2026 실적', '2026-07-28',
     '매출 $1.58B(+24.2%, 인수 포함) · 순이익 $367M · 희석 EPS $1.33(1년 전 $0.59 — 규제 합의 손실) · 연간 GAAP EPS 전망 $4.76~4.86', 'q2', 'Cadence 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 27일 장 마감 뒤 — Q1 2026 실적', '2026-04-28',
     '매출 $1.47B(+18.7%) · 순이익 $336M · 희석 EPS $1.23(1년 전 $1.00)', 'q1', 'Cadence 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 17일 장 마감 뒤 — Q4 2025 실적', '2026-02-18',
     '매출 $1.44B · 순이익 $388M · 희석 EPS $1.42(1년 전 $1.24) · 2025년 EPS $4.06 — 다음 날 주가 +7.6%', 'q4', 'Cadence 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 27일 장 마감 뒤 — Q3 2025 실적', '2025-10-28',
     '매출 $1.34B · 순이익 $287M · 희석 EPS $1.05(1년 전 $0.87)', 'q3', 'Cadence 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 24, 'nt': 17, 'mean': 414.18, 'median': 425, 'low': 300, 'high': 470, 'sb': 18, 'b': 4, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-31'


# ── 자동 카드 — 매출 유형 2개(단일 보고 부문). 원문 대조: Q2 2026 1,430.7/153.8(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"cdns:ProductandmaintenanceMember": ["제품·유지보수", "#d71920"], "us-gaap:TechnologyServiceMember": ["서비스", "#f07a7f"]},
 "ignore": []
}
