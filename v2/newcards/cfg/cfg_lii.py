# LII(레녹스 인터내셔널) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 가정용(Home Comfort)·상업용(Building Climate) 냉난방(HVAC) 장비.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-28), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/LII.md.
# 엔진 입력(2026-10-29): 차입금 CP $455.1M + 1년 안 $319.2M + 장기 $847.1M = $1,621.4M(금융리스 포함, 엔진 DEBT_TOTAL_TAG 줄), 현금 $43.3M + 단기투자 $2.2M. 인수 = Heat Controller $210M(2026-07).
# 일회성: 최근 4분기 GAAP 21.55 대 조정 22.36(3.8% — 인수 비용·구조조정·소송, 매각 이익 반대 방향).
CIK = '0001069202'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, -1), '적정~저평가'
CO = 'Lennox'
S_ = 'https://www.sec.gov/Archives/edgar/data/1069202/'
SEC = S_
TENQ = S_ + '000106920226000096/lii-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000106920226000094/lii-20260930xexx991pressre.htm', 'q2': S_ + '000106920226000085/lii-20260630xexx991pressre.htm', 'q1': S_ + '000106920226000052/lii-20260331xexx991pressre.htm', 'q4': S_ + '000106920226000005/lii-20251231xexx991pressre.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="liiFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('2025년 4분기에 재고 회계를 LIFO에서 FIFO로 바꿔 그 이전 분기 EPS가 다시 계산됐다(Q3 2025 원 발표 6.98 → 7.38). '
              '가정용 수요 부진으로 2026년 조정 EPS 전망을 7월(23.00~24.00)과 10월(21.00~21.50) 두 번 낮췄다.')
PH = ['CARR', 'TT', 'JCI', 'AOS', 'ALLE', 'MAS']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '건물 설비 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(LII 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 건물 설비 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 가정용 937.2 + 상업용 635.3 = 1,572.5.
SEG = [('가정용 냉난방(Home Comfort)', 937.2, '#cf2030'), ('상업용 냉난방(Building Climate)', 635.3, '#2b2b2b')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:5x 동부) → 같은 날.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 28일 — Q3 2026 실적', '2026-10-28',
     '매출 $1.57B(+10.2%) · 순이익 $221M · 희석 EPS $6.41(1년 전 $7.38) · 연간 조정 EPS 전망 21.00~21.50으로 하향 — 당일 주가 −10.6%', 'q3', 'Lennox 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 29일 — Q2 2026 실적', '2026-07-29',
     '매출 $1.55B · 순이익 $269M · 희석 EPS $7.72(1년 전 $7.71) · 연간 전망 하향 — 당일 주가 −21.0%', 'q2', 'Lennox 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 29일 — Q1 2026 실적', '2026-04-29',
     '매출 $1.14B · 순이익 $117M · 희석 EPS $3.35(1년 전 $3.63)', 'q1', 'Lennox 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 28일 — Q4 2025 실적', '2026-01-28',
     '매출 $1.20B · 순이익 $143M · 희석 EPS $4.07(1년 전 $5.64, FIFO 재작성) · 2025년 EPS $22.79', 'q4', 'Lennox 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 18, 'nt': 9, 'mean': 381.78, 'median': 357, 'low': 350, 'high': 490, 'sb': 1, 'b': 1, 'h': 15, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 937.2/635.3(2026-10-29) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"lii:ResidentialHeatingAndCoolingMember": ["가정용 냉난방(Home Comfort)", "#cf2030"], "lii:CommercialHeatingAndCoolingMember": ["상업용 냉난방(Building Climate)", "#2b2b2b"]},
 "ignore": []
}
