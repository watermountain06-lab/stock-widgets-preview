# FICO(페어 아이작) v2 카드 설정 — 자동 카드(AUTO). 회계연도 9월 30일(FY2026 = 2025-10~2026-09). FICO 신용점수(B2B·B2C)와 의사결정 분석 소프트웨어(FICO Platform).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-07-29), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/FICO.md.
# 엔진 입력(2026-10-25): 기본 경로 — 차입금 LongTermDebt $5,582.4M(1년 안 $300M 포함), 현금 $248.4M. 자본 −$4,097M(자사주 매입 누적 — 자본 잠식이라 PBR 제외).
# 일회성 작음(최근 4분기 안). 10/6 인력 15% 감축 공시 — 퇴직금 약 $27M은 Q4 FY26(9월 분기)에 들어갈 예정(카드 밖).
CIK = '0000814547'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-09-30', '2024-09-30'), 'FY2025'
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'FICO'
S_ = 'https://www.sec.gov/Archives/edgar/data/814547/'
SEC = S_
TENQ = S_ + '000081454726000030/fico-20260630.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000081454726000031/exhibit991erq32026.htm', 'q2': S_ + '000081454726000020/exhibit991erq22026.htm',
      'q1': S_ + '000081454726000010/exhibit991erq12026.htm', 'q4': S_ + '000081454725000026/exhibit991erq42025.htm'}
LINKS = {'rif': 'https://www.sec.gov/Archives/edgar/data/814547/000119312526415732/d127042d8k.htm'}
FAIRBAND_TITLE = 'id="ficoFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 60)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('신용점수는 거의 독점이라 가격 인상으로 매출이 크게 늘었다(Q3 FY26 점수 매출 +41%). 영업이익률이 50% 안팎으로 매우 높다. '
              '자사주를 빚으로 사들여 자본이 음수다 — PBR·ROE는 해석할 수 없다. 주가는 1년 새 크게 내렸다(점수 가격 정책·규제 우려). '
              '10월 인력 15% 감축(퇴직금 약 $27M)은 Q4 FY26에 들어갈 예정이다. '
              '설비투자는 유형자산만이고 자본화한 소프트웨어 개발비(최근 4분기 약 $35M)는 빠진다(전 카드 공통 — 넣어도 현금흐름 기본값은 거의 같다). 주식 수는 7/17 표지 기준이라 ASR 최종 인도분은 아직 빠져 있다.')
PH = ['MSFT', 'ORCL', 'CRM', 'PANW', 'CRWD', 'PLTR']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소프트웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(FICO 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 소프트웨어 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 부문) — 점수 458.9 + 소프트웨어 215.3 = 674.2.
SEG = [('신용점수(Scores)', 458.9, '#0e3a5f'), ('소프트웨어', 215.3, '#3e7cb1')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건 + 인력 감축(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:15~16:19 동부 접수) → 다음 거래일. 인력 감축 8-K는 10/6 16:58 접수 → 10/7. 넣지 않은 8-K: 주총, 사채 $1B(3월), 신용 계약·자사주 $2B·ASR $1.5B(6/8).
NEWS_RANGE = '2025.11 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 6일 장 마감 뒤 — 인력 약 15% 감축 계획', '2026-10-07',
     '퇴직금 약 $27M(세전)을 Q4 FY26에 반영, FY27 3분기까지 완료(8-K 2.05)', 'rif', 'FICO 공시 (SEC 8-K)'),
    ('red', '2026년 7월 29일 장 마감 뒤 — Q3 FY26 실적', '2026-07-30',
     '매출 $674M(+26%) · 순이익 $237M · 희석 EPS $10.45(1년 전 $7.40) — 다음 날 주가 −17%', 'q3', 'FICO 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 장 마감 뒤 — Q2 FY26 실적', '2026-04-29',
     '매출 $692M(+39%) · 순이익 $265M · 희석 EPS $11.14(1년 전 $6.59)', 'q2', 'FICO 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 28일 장 마감 뒤 — Q1 FY26 실적', '2026-01-29',
     '매출 $512M · 순이익 $158M · 희석 EPS $6.61(1년 전 $6.14)', 'q1', 'FICO 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 5일 장 마감 뒤 — Q4 FY25 실적', '2025-11-06',
     '매출 $516M · 순이익 $155M · 희석 EPS $6.42(1년 전 $5.44) · FY2025 EPS $26.54', 'q4', 'FICO 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 16, 'mean': 1186.56, 'median': 1129, 'low': 700, 'high': 1675, 'sb': 7, 'b': 4, 'h': 8, 's': 0, 'ss': 2}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 2개(수동 지도). 원문 대조: Q3 FY26 458.9/215.3(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"fico:ScoresMember": ["신용점수(Scores)", "#0e3a5f"], "fico:SoftwareMember": ["소프트웨어", "#3e7cb1"]},
 "ignore": []
}
