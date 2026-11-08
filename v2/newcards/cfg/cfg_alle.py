# ALLE(알레기온) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 아일랜드 법인. 자물쇠·출입 통제·도어 하드웨어(Schlage, LCN, Von Duprin, Interflex 등).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-22 장 전), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/ALLE.md.
# 엔진 입력(2026-10-25): 차입금 LongTermDebt $2,032.0M(1년 안 포함 합계), 현금 = 제한 현금 포함 줄 $388.1M(EV_TAGS cash — 기본 현금 태그는 10-K만), 비지배지분 없음.
# D&A = DepreciationAmortizationAndAccretionNet만(EXCLUDE — 합산 태그는 연간만이라 4분기가 섞였다). 인수 = ACQ_FIXED $72.9M(인수 대금을 다른 태그로만 낸다).
# 일회성 작음(GAAP이 조정 EPS보다 약 8% 낮은 것은 상각·구조조정·인수 비용 등 반복 항목).
CIK = '0001579241'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Allegion'
S_ = 'https://www.sec.gov/Archives/edgar/data/1579241/'
SEC = S_
TENQ = S_ + '000157924126000034/alle-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000157924126000032/exhibit991-pressreleasedat.htm', 'q2': S_ + '000157924126000026/exhibit991-pressreleasedat.htm',
      'q1': S_ + '000157924126000013/exhibit991-pressreleasedat.htm', 'q4': S_ + '000157924126000006/exhibit991-pressreleasedat.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="alleFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('작은 회사를 자주 인수해(2025 ELATEC 약 $387M 등, 2026-10 Overly Door $88.7M) 무형자산 상각이 늘고 있다. '
              '미국 상업용·주거용 건축 경기에 따라 수요가 움직인다. 매출의 약 80%가 미주 부문이다. '
              '10월 2일 Overly Door 인수 대금($88.7M, 현금 + 리볼버)은 9월 말 재무상태표 뒤라 현금·차입금에 아직 없다.')
PH = ['CARR', 'JCI', 'TT', 'LII', 'MAS', 'AOS']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '건물 설비·자재 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(ALLE 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 건물 설비·자재 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 미주 942.4 + 해외 230.2 = 1,172.6.
SEG = [('미주', 942.4, '#ff6900'), ('해외', 230.2, '#333f48')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:01~06:14 동부 접수) → 같은 날. 넣지 않은 8-K: 신용 계약, 자사주 한도 $500M, 주총, 임원 은퇴.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 22일 — Q3 2026 실적', '2026-10-22',
     '매출 $1.17B(+9.6%) · 순이익 $221M · 희석 EPS $2.59(1년 전 $2.18) — 발표 당일 주가 +11%', 'q3', 'Allegion 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 23일 — Q2 2026 실적', '2026-07-23',
     '매출 $1.15B · 순이익 $185M · 희석 EPS $2.15(1년 전 $1.85) — 발표 당일 주가 +10%', 'q2', 'Allegion 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 28일 — Q1 2026 실적', '2026-04-28',
     '매출 $1.03B · 순이익 $138M · 희석 EPS $1.59(1년 전 $1.71) — 발표 당일 주가 −7%', 'q1', 'Allegion 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 17일 — Q4 2025 실적', '2026-02-17',
     '매출 $1.03B · 순이익 $148M · 희석 EPS $1.70(1년 전 $1.65) · 2025년 EPS $7.44 — 발표 당일 주가 −9%', 'q4', 'Allegion 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 11, 'nt': 9, 'mean': 182.89, 'median': 181, 'low': 155, 'high': 206, 'sb': 6, 'b': 0, 'h': 5, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 2개(수동 지도, 영업 부문 차원). 원문 대조: Q3 2026 942.4/230.2(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax", "us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"alle:AllegionAmericasMember": ["미주", "#ff6900"], "alle:AllegionInternationalMember": ["해외", "#333f48"]},
 "ignore": []
}
