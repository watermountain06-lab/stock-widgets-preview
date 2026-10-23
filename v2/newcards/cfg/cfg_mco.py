# MCO(무디스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 172. 신용평가(MIS), 데이터·분석·소프트웨어(MA).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-21 장 마감 뒤 접수 → 첫 세션 10/22), 실적 보도자료(Q3 2025~Q3 2026, 8-K 2.02항 — 보도자료 장 전, 8-K 장중), 8-K(MA CEO 4/15), StockAnalysis.
# 엔진 입력(2026-10-23): 차입금 = 1년 안 568 + 장기 6,343 = $6,911M(원문), 현금 $1,513M·단기투자 $108M. 4분기 EPS 2024·2025 보도자료 값.
# 매각 이익: MA 규제 솔루션 Q2 세전 $179M(세후 주당 $0.72) + Q3 추가 $115M(세후 $0.47) = 누적 세전 $294M(10-Q 주석 11). Q4 2025 교육 솔루션 $23M.
# 이자비용은 순이자(InterestIncomeExpenseNonoperatingNet, CONCEPTS_BY_CIK).
CIK = '0001059556'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, None, -2), '적정~고평가'
CO = 'Moody’s'
S_ = 'https://www.sec.gov/Archives/edgar/data/1059556/'
SEC = S_
TENQ = S_ + '000162828026066731/mco-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000162828026066594/a3q26earningsrelease.htm', 'q2': S_ + '000162828026049104/a2q26earningsrelease.htm',
      'q1': S_ + '000162828026026383/a1q26earningsrelease.htm', 'q4': S_ + '000162828026008788/a4q25earningsrelease.htm',
      'q3_25': S_ + '000162828025045770/a3q25earningsrelease.htm'}
LINKS = {'ma_ceo': S_ + '000105955626000028/pressreleaseapril2026.htm'}
FAIRBAND_TITLE = 'id="mcoFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 60)
ACT_REASON = ''
NONOP_WHAT = '투자'
YOY_NOTE = {'2026-09-30': '최근 4분기 순이익에는 MA 규제 솔루션 사업 매각 이익이 들어 있다 — Q2 2026 세전 $179M(그 분기 사업 매각 이익 세후 주당 $0.72), Q3 2026 추가분 세전 $115M(세후 주당 $0.47). Q3 희석 EPS $4.24에서 이 몫을 빼면 약 $3.77로 1년 전 $3.60보다 약 5% 높다'}   # Codex·Fable r1 필수
# 고정 문장(숫자 없음). 자사주로 자본이 작아 PBR이 높음, 신용평가는 채권 발행 경기에 민감, 매각 이익.
MODEL_NOTE = ('꾸준한 자사주 매입으로 장부상 자본이 작아 PBR이 매우 높게 나온다 — 자본 대비 지표보다 이익·현금흐름 배수로 보는 편이 맞다. '
              '신용평가 매출은 회사채 발행 경기에 따라 분기마다 크게 흔들린다. 최근 4분기 이익에는 사업 매각 이익이 섞여 있다.')
PH = ['SPGI', 'MSCI', 'ICE', 'CME', 'FDS', 'VRSK']
PEER_FILE = 'peer_universe/brokers_fees.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '금융 데이터·거래소 6곳 PER 비교 (점수는 중개사 + 결제·거래소·데이터 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 보험 중개사와 결제·거래소·금융 데이터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 보험 중개 + 결제·거래소·금융 데이터 대비 배수 순위 (v2/peer_universe/brokers_fees.json)'
PEER_TIP = ('S&P500 결제·거래소·금융 데이터 회사와 보험 중개사(MCO 제외)와 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 처리·보험 중개가 섞여 있어 성장·마진 구조가 다르다. 차트에는 금융 데이터·거래소 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 외부 매출) — 신용평가(MIS) 1,087 + 분석(MA) 936 = 2,023. 1년 전 1,098·909.
SEG = [('신용평가(MIS)', 1087.0, '#002b5c'), ('데이터·분석(MA)', 936.0, '#5b84b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(외부 매출)'
# 손 뉴스: 실적 5건(EPS는 GAAP 희석 — 조정 EPS·가이던스 수치는 쓰지 않는다), MA CEO.
# 반응일: 실적 보도자료 장 전 배포, 8-K 접수 UTC 2025-10-22T14:56Z·2026-02-18T16:58Z·04-22T14:59Z·07-22T14:59Z·10-21T14:57Z = 장중 → 같은 날.
# MA CEO 8-K 2026-04-15T16:14Z → 4/15. 넣지 않은 8-K: 정관(2025-10-17), 보상 계획(12/19), 이사 선임(1/12·8/12), 주총(4/16).
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 21일 — Q3 2026 실적', '2026-10-21',
     '매출 $2.0B(+1%) · 희석 EPS $4.24(1년 전 $3.60, +18% — 규제 솔루션 매각 추가 이익 세후 주당 $0.47 포함) · 영업이익률 44.8%', 'q3', 'Moody’s 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 22일 — Q2 2026 실적', '2026-07-22',
     '매출 $2.2B(+15%) · 희석 EPS $5.03(+57%, 사업 매각 이익 세후 주당 $0.72 포함 — 5월 완료한 MA 규제 솔루션 세전 $179M 등) · 영업이익률 47.9%', 'q2', 'Moody’s 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 22일 — Q1 2026 실적', '2026-04-22',
     '매출 $2.1B(+8%) · 희석 EPS $3.73(+8%) · 영업이익률 44.3%', 'q1', 'Moody’s 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 15일 — Moody’s Analytics 새 CEO', '2026-04-15',
     'Christina Kosmowski가 6월부터 Moody’s Analytics CEO', 'ma_ceo', 'Moody’s 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 18일 — Q4 2025 실적', '2026-02-18',
     '희석 EPS $3.41(1년 전 $2.17, +57%) · 2025년 매출 $7.7B·희석 EPS 21% 증가', 'q4', 'Moody’s 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 22일 — Q3 2025 실적', '2025-10-22',
     '매출 $2.0B(+11%) · 희석 EPS $3.60(+23%)', 'q3_25', 'Moody’s 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 17, 'mean': 556.06, 'median': 572, 'low': 480, 'high': 610, 'sb': 13, 'b': 5, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-23'

# ── 자동 카드 — 부문 2개(외부 매출). 원문 대조: Q3 2026 1,087/936, 1년 전 1,098/909(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "mco:MoodysInvestorsServiceMember": [
   "신용평가(MIS)",
   "#002b5c"
  ],
  "mco:MoodysAnalyticsMember": [
   "데이터·분석(MA)",
   "#5b84b8"
  ]
 },
 "ignore": []
}
