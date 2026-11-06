BUILD = {}
# TSCO(트랙터 서플라이) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 마지막 토요일(52/53주). 농촌 생활용품 소매, 단일 보고 부문(Petsense 포함).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-06), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 07시 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/TSCO.md.
# 품목 매출은 금액 없이 정수 비중(%)으로만 공시(농·축산 32·계절·레저 26·반려동물 21·트럭·공구 14·의류·선물 7, Q2 2026) — 매출 구성은 '매출 전체' 한 줄(2026-11-03 사용자 결정: 판정이 가능하면 낸다).
# Q3 2026은 보도자료뿐(10-Q 11월 초 예상) — 2026-10-30 사용자 결정대로 Q2 10-Q 기준. 2024-12 5:1 분할(KNOWN_SPLITS). Q4 2025 EPS 보도자료 값. 우선주 태그 2024-09 멈춤 → 비움.
# 일회성: Q2 2026 Petsense 손상·VIP Petcare 인수 비용 세전 $81.2M(조정 EPS 0.81 대 GAAP 0.69).
CIK = '0000916365'
CUR, YO, QO = '2026-06-27', '2025-06-28', '2026-03-28'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-27', '2024-12-28'), 'FY2025'
VOTES, VERDICT = (1, 0, -1), '적정'
CO = 'Tractor Supply'
S_ = 'https://www.sec.gov/Archives/edgar/data/916365/'
SEC = S_
TENQ = S_ + '000091636526000059/tsco-20260627.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q3': S_ + '000091636526000069/ex991-q32026earningsrelease.htm', 'q2': S_ + '000091636526000052/ex991-q22026earningsrelease.htm', 'q1': S_ + '000091636526000020/ex991-q12026earningsrelease.htm', 'q4': S_ + '000091636526000005/ex991-q42025earningsrelease.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="tscoFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('품목별 매출을 금액 없이 비중(%)으로만 공시한다(농·축산 32%·계절·레저 26%·반려동물 21%·트럭·공구 14%·의류·선물 7%, Q2 2026). '
              '그래서 매출 구성은 전체 한 줄로만 보인다. 2026년 2분기 이익에 Petsense 손상·구조조정과 VIP Petcare 인수 비용(세전 $81M)이 들어 있다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['HD', 'LOW', 'TJX', 'ROST', 'BBY', 'WSM']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소매 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(TSCO 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 소매 6곳만 보인다.')
# 매출(Q2 2026 10-Q) — 단일 부문 4,541.3.
SEG = [('매출 전체(단일 부문)', 4541.3, '#c8102e')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 단일 부문(Q2 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07시 동부) → 같은 날.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 22일 장 전 — Q3 2026 실적', '2026-10-22',
     '매출 $3.91B(+5.1%) · 순이익 $225M · 희석 EPS $0.43(1년 전 $0.49) · 동일점 +0.4% — 당일 주가 +6.2%', 'q3', 'Tractor Supply 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 23일 장 전 — Q2 2026 실적', '2026-07-23',
     '매출 $4.54B(+2.3%) · 순이익 $361M · 희석 EPS $0.69(1년 전 $0.81, Petsense 손상 포함) · 조정 EPS $0.81 · 연간 전망 하향 — 당일 주가 +3.3%', 'q2', 'Tractor Supply 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 21일 장 전 — Q1 2026 실적', '2026-04-21',
     '매출 $3.59B(+3.6%) · 순이익 $165M · 희석 EPS $0.31(1년 전 $0.34) — 당일 주가 −11.7%', 'q1', 'Tractor Supply 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 29일 장 전 — Q4 2025 실적', '2026-01-29',
     '매출 $3.90B(+3.3%) · 순이익 $227M · 희석 EPS $0.43(1년 전 $0.44) — 당일 주가 −7.6%', 'q4', 'Tractor Supply 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 30, 'nt': 21, 'mean': 38.24, 'median': 38, 'low': 31, 'high': 51, 'sb': 12, 'b': 3, 'h': 15, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-04'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q2 2026 연결 매출 4,541.3 한 줄(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {"us-gaap:Revenues": ["매출 전체(단일 부문)", "#c8102e"]},
 "ignore": []
}
