# CTSH(코그니전트) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. IT 서비스·컨설팅 — 금융·헬스케어·제조·통신 고객, 인도 중심 인력.
# 출처: SEC XBRL(10/29 Q3 2026 10-Q까지 요약 자료에 있음), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 06:3x 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/CTSH_q3.md.
# 엔진 입력(2026-10-29): 차입금 $1,552M(회전 $1,000M + 텀론 $553M), 현금 $1,515M + 단기투자 $37M, 최근 4분기 인수 $1.31B(3Cloud·Astreya).
# 일회성: 최근 4분기 GAAP 5.48 대 조정 5.61(2.3% — Project Leap 구조조정·환율). 1년 전 3분기 세법(OBBBA) 일회성 세금(주당 0.80)은 이번 창에서 빠졌다.
CIK = '0001058290'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, 1), '저평가'
CO = 'Cognizant'
S_ = 'https://www.sec.gov/Archives/edgar/data/1058290/'
SEC = S_
TENQ = S_ + '000105829026000041/ctsh-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000105829026000039/exhibit9919302026.htm', 'q2': S_ + '000105829026000030/exhibit9916302026.htm',
      'q1': S_ + '000105829026000015/exhibit9913312026.htm', 'q4': S_ + '000105829026000003/exhibit99112312025.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ctshFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = 'IT 서비스 회사라 재고 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('2025년 3분기에는 미국 세법(OBBBA) 변경에 따른 일회성 세금(주당 0.80)이 있어 그 분기 EPS가 $0.56으로 낮았다 — 이번 최근 4분기 창에서는 빠졌다. '
              '현금흐름 비율(현재가 ÷ 기본 내재가치)이 0.90 문턱 바로 아래라 주가가 약 $62.80을 넘으면 현금흐름 표가 +1에서 0으로 바뀐다. 동종업 점수는 반도체·소프트웨어·하드웨어가 섞인 카드 유니버스 IT 25곳과 비교한 값(배수 5개 모두 가장 쌈)이다. '
              '자사주를 크게 사서 희석 주식 수가 1년 새 487M에서 450M으로 줄었다. 2026년 Project Leap 구조조정(연 $140~160M)이 진행 중이다.')
PH = ['IBM', 'MSFT', 'ORCL', 'CRM', 'CSCO', 'DELL']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': 'IT 서비스·소프트웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(CTSH 제외)과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 섞여 있다. 차트에는 IT 서비스·소프트웨어·하드웨어 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 금융 서비스 1,767 + 헬스 사이언스 1,587 + 제조·유통·에너지 1,371 + 통신·미디어·기술 939 = 5,664.
SEG = [('금융 서비스', 1767, '#0033a1'), ('헬스 사이언스', 1587, '#26a8e0'), ('제조·유통·에너지', 1371, '#7fb2e5'), ('통신·미디어·기술', 939, '#000048')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 산업 부문별(Q3 2026)'
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 29일 장 전 — Q3 2026 실적', '2026-10-29',
     '매출 $5.66B(+4.6%) · 순이익 $627M · 희석 EPS $1.39(1년 전 $0.56 — 세법 일회성 세금) · 연간 매출 전망 범위를 좁힘 — 당일 주가 −5.8%(장중)', 'q3', 'Cognizant 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 29일 장 전 — Q2 2026 실적', '2026-07-29',
     '매출 $5.48B · 순이익 $636M · 희석 EPS $1.36 — 당일 주가 +11.3%', 'q2', 'Cognizant 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 29일 장 전 — Q1 2026 실적', '2026-04-29',
     '매출 $5.41B · 순이익 $662M · 희석 EPS $1.39', 'q1', 'Cognizant 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 4일 장 전 — Q4 2025 실적', '2026-02-04',
     '매출 $5.33B · 순이익 $648M · 희석 EPS $1.34(1년 전 $1.10)', 'q4', 'Cognizant 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 29, 'nt': 17, 'mean': 67.29, 'median': 68, 'low': 47, 'high': 82, 'sb': 10, 'b': 3, 'h': 16, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-29'


# ── 자동 카드 — 산업 부문 4개(축 하나만 붙은 값). 원문 대조: Q3 2026 1,767/1,587/1,371/939(2026-10-29) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"ctsh:FinancialServicesMember": ["금융 서비스", "#0033a1"], "ctsh:HealthSciencesMember": ["헬스 사이언스", "#26a8e0"],
             "ctsh:ProductsandResourcesMember": ["제조·유통·에너지", "#7fb2e5"], "ctsh:CommunicationsMediaAndTechnologyMember": ["통신·미디어·기술", "#000048"]},
 "ignore": []
}
