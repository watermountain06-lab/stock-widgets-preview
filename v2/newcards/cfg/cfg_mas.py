# MAS(마스코) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 수전·욕실 제품(Delta·Hansgrohe)과 건축용 도료(Behr).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-28), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/MAS.md.
# 엔진 입력(2026-10-29): 기본 경로 — 차입금 단기 $2M + 장기 $3,245M(기한부 대출 $300M 포함), 현금 $610M, 비지배지분 $256M(Hansgrohe 소수지분). 자기자본 −$448M(자사주 매입).
# 일회성: 최근 4분기 GAAP 4.62 대 조정 4.69(1.5%). 회사가 빼지 않는 관세(IEEPA) 환급 — 9개월 영업이익 약 $90M(주당 약 0.34, 추정)은 GAAP·조정 모두에 들어 있다.
CIK = '0000062996'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 1, -2), '적정~고평가'
CO = 'Masco'
S_ = 'https://www.sec.gov/Archives/edgar/data/62996/'
SEC = S_
TENQ = S_ + '000006299626000033/mas-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000006299626000032/a930268-kex99.htm', 'q2': S_ + '000006299626000026/a630268-kex99.htm', 'q1': S_ + '000006299626000013/a331268-kex99.htm', 'q4': S_ + '000006299626000004/a1231258-kex99.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="masFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('자사주를 많이 사서 자기자본이 음수(−$448M)라 PBR은 뜻이 없다. 2026년 영업이익에는 관세(IEEPA) 환급 약 $90M(9개월, 주로 수전 부문)이 들어 있어 이번 최근 4분기 이익이 반복 수준보다 높게 잡혔을 수 있다 — 환급을 빼도 판정은 같다(현금흐름 비율 약 1.45, 동종업 점수 약 83). '
              '2026년 1분기에 부문 정의가 바뀌어(Liberty를 Delta로 통합, 과거 비교 기간 재작성) 예전 보고서의 부문 값과는 직접 비교하지 않는다.')
PH = ['AOS', 'ALLE', 'LII', 'CARR', 'BLDR', 'TT']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '건물 설비 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(MAS 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 건물 설비 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 수전·욕실 1,338 + 건축용 도료 628 = 1,966.
SEG = [('수전·욕실(Plumbing)', 1338, '#00447c'), ('건축용 도료(Decorative)', 628, '#f39200')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07:01 동부) → 같은 날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 28일 — Q3 2026 실적', '2026-10-28',
     '매출 $1.97B(+2.6%) · 순이익 $230M · 희석 EPS $1.17(1년 전 $0.90) — Bristan 매각 이익 $13M 포함', 'q3', 'Masco 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 29일 — Q2 2026 실적', '2026-07-29',
     '매출 $1.99B · 순이익 $318M · 희석 EPS $1.60(1년 전 $1.28) — 당일 주가 −11.1%', 'q2', 'Masco 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 22일 — Q1 2026 실적', '2026-04-22',
     '매출 $1.92B · 순이익 $213M · 희석 EPS $1.05(1년 전 $0.87) — 당일 주가 +10.8%', 'q1', 'Masco 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 10일 — Q4 2025 실적', '2026-02-10',
     '매출 $1.79B · 순이익 $165M · 희석 EPS $0.80(1년 전 $0.85) · 2025년 EPS $3.86 — 당일 주가 +8.7%', 'q4', 'Masco 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 22, 'nt': 15, 'mean': 82.47, 'median': 82, 'low': 70, 'high': 98, 'sb': 6, 'b': 0, 'h': 15, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-31'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 1,338/628(2026-10-29) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"mas:PlumbingProductsMember": ["수전·욕실(Plumbing)", "#00447c"], "mas:DecorativeArchitecturalProductsMember": ["건축용 도료(Decorative)", "#f39200"]},
 "ignore": []
}
