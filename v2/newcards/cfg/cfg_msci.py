# MSCI v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 190. 지수(ETF·파생상품 사용료), 분석, 지속가능성·기후 데이터, 사모 자산 데이터.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-20T21:54Z 장 마감 뒤 접수), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 발표, 11시 콜), StockAnalysis. 사전 조사 자료표 scratchpad pre/MSCI.md.
# 엔진 입력(2026-10-23): D&A = 감가상각 + 무형자산 상각(DDA_PARTS_BY_CIK + EXCLUDE_TAGS — 합계 태그는 감가상각만, TTM $198M), 설비투자 = 유형자산 + 자본화 소프트웨어(SUM_TAGS_BY_CIK, TTM $39.6M + $120.5M = $160M — 안건 E30①의 다른 카드 기본(소프트웨어 제외)과 다르다. D&A에 소프트웨어 상각이 들어가 맞춘 것),
# 차입금 $6,717M(사채 + 리볼버 $810M), 일회성 세금 두 건은 tax_oneoff.json, 자본 −$3.0B(자사주 매입으로 자본잠식 — PBR 계산 불가), 4분기 EPS 2023·2024 보도자료 값.
CIK = '0001408198'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, None, -2), '적정~고평가'
CO = 'MSCI'
S_ = 'https://www.sec.gov/Archives/edgar/data/1408198/'
SEC = S_
TENQ = S_ + '000140819826000056/msci-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000140819826000054/exhibit991earningsrelease-.htm', 'q2': S_ + '000140819826000044/exhibit991earningsrelease-.htm',
      'q1': S_ + '000140819826000032/earningsrelease-20260331xe.htm', 'q4': S_ + '000140819826000005/exhibit991earningsrelease-.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="msciFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (40, 70)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('자사주를 많이 사 들여 자본이 마이너스라 PBR은 계산하지 않는다. 주식 수가 해마다 줄어 주당순이익이 순이익보다 빠르게 늘어난다. '
              '자기 이력 점수는 5년 내내 높은 PER을 받아 온 이 종목 안에서 지금 배수가 낮은 편이라는 뜻이고, 현금흐름 모델은 그 높은 배수 자체를 인정하지 않는다 — 5년 뒤에는 낮은 장기 성장률과 적용 할인율로 잔존가치를 잡아, 지금 시장이 매기는 배수보다 훨씬 낮은 배수가 된다. 그래서 과거보다 싸면서도 현금흐름 기준으로는 비쌀 수 있고, 두 판정은 같은 질문이 아니다. '
              '법인 구조 재편에 따른 일회성 세금 비용(Q4 2025)과 혜택(Q1 2026)은 PER의 최근 4분기 EPS와 내재가치 세율에서 뺐다. '
              '지수 사용료의 상당 부분이 ETF 운용 자산에 비례해 주식 시장 흐름에 따라 움직인다.')
PH = ['SPGI', 'MCO', 'ICE', 'NDAQ', 'CME', 'CBOE']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '거래소·금융 데이터 6곳 PER 비교', 'pbr': '거래소·금융 데이터 PBR 비교', 'psr': '거래소·금융 데이터 PSR 비교',
                'pcr': '거래소·금융 데이터 PCR(FCF) 비교', 'evebitda': '거래소·금융 데이터 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 결제·거래소 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 결제·거래소 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('S&P500 결제·거래소·금융 데이터(MSCI 제외)와 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 처리·거래소·신용평가·지수 회사가 섞여 있다. 비교할 값이 있는 회사가 적은 배수는 빠지는데, MSCI는 PER 하나만 남아 동종업 점수는 참고값이고 판정에서는 기권이다. 차트에는 거래소·금융 데이터 6곳만 보인다.')
# 매출(Q3 2026 10-Q 주석 11 부문) — 지수 532.6 + 분석 191.0 + 지속가능성·기후 93.7 + 사모 자산(기타) 74.7 = 892.0. 1년 전 451.1·182.2·90.1·70.0.
SEG = [('지수', 532.6, '#1a2b6b'), ('분석', 191.0, '#6b7fc4'), ('지속가능성·기후', 93.7, '#0f1a45'), ('사모 자산(기타)', 74.7, '#a9b4de')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다). 반응일: 보도자료 장 전(11시 콜), 8-K 장중 접수 → 같은 날.
# 넣지 않은 8-K: BlackRock 지수 사용 계약 2035년까지 연장(1/28, 매출의 약 12%), 사채(2025-11), 임원·주총. 소규모 인수(First Street 등)는 8-K 없음.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 20일 — Q3 2026 실적', '2026-10-20',
     '매출 $892M(1년 전 $793M) · 순이익 $351M · 희석 EPS $4.86(1년 전 $4.25)', 'q3', 'MSCI 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 21일 — Q2 2026 실적', '2026-07-21',
     '매출 $867M · 순이익 $342M · 희석 EPS $4.69(1년 전 $3.92) — 발표 날 주가 −10%', 'q2', 'MSCI 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 21일 — Q1 2026 실적', '2026-04-21',
     '매출 $851M · 순이익 $406M · 희석 EPS $5.53(1년 전 $3.71) — 법인 구조 재편 세금 혜택 $88M(EPS $1.20) 포함', 'q1', 'MSCI 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 28일 — Q4 2025 실적', '2026-01-28',
     '매출 $823M · 순이익 $285M · 희석 EPS $3.81(1년 전 $3.90) — 법인 구조 재편 세금 비용 $38M(EPS $0.51) 포함', 'q4', 'MSCI 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 18, 'nt': 14, 'mean': 699.29, 'median': 710, 'low': 618, 'high': 760, 'sb': 12, 'b': 4, 'h': 1, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 부문 4개(수동 지도). 원문 대조: Q3 2026 532.6/191.0/93.7/74.7(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"msci:IndexSegmentMember": ["지수", "#1a2b6b"], "msci:AnalyticsSegmentMember": ["분석", "#6b7fc4"],
             "msci:SustainabilityAndClimateSegmentMember": ["지속가능성·기후", "#0f1a45"], "us-gaap:AllOtherSegmentsMember": ["사모 자산(기타)", "#a9b4de"]},
 "ignore": []
}
