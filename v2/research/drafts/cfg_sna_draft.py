# SNA(스냅온) v2 카드 설정 — 자동 카드(AUTO). 52/53주 회계연도(12월 31일에 가까운 토요일 — FY2025는 2026-01-03에 끝난 53주, 4분기 14주). 정비 공구(트럭 판매망)·진단·산업용 공구와 공구 할부 금융.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-22), 실적 보도자료(Q3 2025~Q3 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/SNA.md.
# 엔진 입력(2026-10-25): 차입금 = LongTermDebt $1,205.1M(1년 안 만기·어음 포함 합계, DEBT_TOTAL_TAG), 현금 $1,670M, 비지배지분 $25M.
# 설비투자 = PaymentsForCapitalImprovements, D&A = 감가상각만(EV_TAGS 대체·EXCLUDE — 합산 태그는 연간만이라 4분기에 상각이 몰렸다. 무형자산 상각 연 약 $22M은 2026년 분기에 표준 태그가 없어 빠진다).
# 매출은 금융 서비스 수익 포함 총매출(Revenues). 금융 자회사 할부채권(약 $2.5B)은 영업 자산으로 둔다.
CIK = '0000091440'
CUR, YO, QO = '2026-10-03', '2025-09-27', '2026-07-04'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2026-01-03', '2024-12-28'), 'FY2025'
VOTES, VERDICT = (-1, 1, -1), '적정~고평가'
CO = 'Snap-on'
S_ = 'https://www.sec.gov/Archives/edgar/data/91440/'
SEC = S_
TENQ = S_ + '000009144026000172/sna-20261003.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000009144026000169/q32026pressreleaseforpress.htm', 'q2': S_ + '000009144026000141/q22026pressreleaseforpress.htm',
      'q1': S_ + '000009144026000106/q12026pressreleaseforpress.htm', 'q4': S_ + '000009144026000008/q42025pressreleaseforpress.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="snaFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('매출에는 공구 할부 금융 수익(분기 약 $0.1B)이 들어 있고, 금융 자회사의 할부채권은 영업 자산으로 본다. '
              'FY2025 4분기는 14주라 그 분기와 최근 4분기 이익이 1주만큼(약 2%) 크다. D&A는 감가상각만이라 EBITDA가 무형자산 상각(연 약 $22M)만큼 작다.')
PH = ['ITW', 'DOV', 'GWW', 'FAST', 'PH', 'IR']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '산업 기계·공구 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(SNA 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 산업 기계·공구 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문, 부문 간 거래 제거 전) — 공구 471.5 + 정비 시스템·정보 454.7 + 상업·산업 404.3 + 금융 98.6 = 1,429.1, 제거 −146.8 → 1,282.3.
SEG = [('공구(Tools)', 471.5, '#e31837'), ('정비 시스템·정보', 454.7, '#f07a8a'), ('상업·산업', 404.3, '#1a1a1a'), ('금융 서비스', 98.6, '#9a9a9a')]
SEG_ADJ = -146.8
SEG_TITLE = '매출 구성 — 부문별(Q3 2026, 부문 간 거래 제거 전)'
# 손 뉴스: 실적 5건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:30 동부 접수) → 같은 날. 넣지 않은 8-K: 주총.
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 22일 — Q3 2026 실적', '2026-10-22',
     '순매출 $1.18B(−0.6%) · 순이익 $243M · 희석 EPS $4.64(1년 전 $5.02 — 소송 합의 이익 $0.31 포함)', 'q3', 'Snap-on 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 23일 — Q2 2026 실적', '2026-07-23',
     '순매출 $1.24B · 순이익 $261M · 희석 EPS $4.96(1년 전 $4.72)', 'q2', 'Snap-on 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 23일 — Q1 2026 실적', '2026-04-23',
     '순매출 $1.21B · 순이익 $247M · 희석 EPS $4.69(1년 전 $4.51)', 'q1', 'Snap-on 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 5일 — Q4 2025 실적(14주)', '2026-02-05',
     '순매출 $1.23B · 순이익 $261M · 희석 EPS $4.94(1년 전 $4.82) · 2025년 EPS $19.19', 'q4', 'Snap-on 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 11, 'nt': 6, 'mean': 415.5, 'median': 433, 'low': 340, 'high': 485, 'sb': 2, 'b': 3, 'h': 5, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 4개(수동 지도, 영업 부문 차원). 원문 대조: Q3 2026 471.5/454.7/404.3/98.6, 제거 −146.8(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"sna:ToolsGroupMember": ["공구(Tools)", "#e31837"], "sna:RepairSystemsAndInformationGroupMember": ["정비 시스템·정보", "#f07a8a"],
             "sna:CommercialAndIndustrialGroupMember": ["상업·산업", "#1a1a1a"], "sna:FinancialServicesMember": ["금융 서비스", "#9a9a9a"]},
 "ignore": []
}
