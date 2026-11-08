# EXPD(익스피디터스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 국제 화물 운송 주선(항공·해상 — 자산을 거의 갖지 않음)과 통관·물류 서비스.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표, 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/EXPD.md.
# 엔진 입력(2026-10-25): 이자부 차입금 없음, 현금 $1,031M, 운용리스 $0.57B. 일회성: Q2 2026 기술 조직 구조조정 세전 $25M(최근 4분기 EPS의 약 2%).
CIK = '0000746515'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Expeditors'
S_ = 'https://www.sec.gov/Archives/edgar/data/746515/'
SEC = S_
TENQ = S_ + '000119312526334457/expd-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000119312526332198/expd-ex99_1.htm', 'q1': S_ + '000119312526205511/expd-ex99_1.htm',
      'q4': S_ + '000119312526066101/expd-ex99_1.htm', 'q3': S_ + '000119312525264045/expd-ex99_1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="expdFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 15)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('운임과 물동량에 따라 매출·이익이 크게 오르내린다 — 2021~2022년 코로나 물류 대란 때 이익이 최고였고 2023년에 절반 가까이 줄었다. 5년 이력 배수와 성장률에 그 고점이 섞여 있다. '
              'Q2 2026 매출은 항공 화물 운임(+44%)과 물동량(+14%)이 함께 늘어 1년 전보다 30% 넘게 늘었다 — 운임 급등이 계속될지는 알 수 없다. 같은 분기 이익에는 구조조정 비용(−$25M)과 부동산 매각 이익(+$16M)이 함께 들어 있다. '
              '현금흐름 모델은 운용리스를 차입금으로 빼지 않는다(순현금 칸은 리스 포함, EV/EBITDA는 운용리스를 빚으로 보지 않는다).')
PH = ['CHRW', 'UPS', 'FDX', 'JBHT', 'ODFL', 'UNP']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '운송·물류 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(EXPD 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 운송·물류 6곳만 보인다.')
# 매출(Q2 2026 10-Q 서비스별) — 항공 1,494.8 + 통관·기타 1,296.6 + 해상 710.9 = 3,502.3.
SEG = [('항공 화물', 1494.8, '#0b3d91'), ('통관·기타 서비스', 1296.6, '#5b84c8'), ('해상 화물', 710.9, '#e0a526')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 서비스별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 보도자료 오전 8:30(동부) 장 전 발표 → 같은 날(8-K 접수는 장중). 넣지 않은 8-K: 배당, 자사주 $3B 승인(2/24 실적과 함께), 공시 정책 자료, 임원.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 4일 — Q2 2026 실적', '2026-08-04',
     '매출 $3.50B(+32%) · 순이익 $266M · 희석 EPS $2.03(1년 전 $1.34) — 구조조정 비용 $25M·부동산 매각 이익 $16M(모두 세전) 포함, 발표 당일 주가 +6%', 'q2', 'Expeditors 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 5일 — Q1 2026 실적', '2026-05-05',
     '매출 $2.78B · 순이익 $230M · 희석 EPS $1.71(1년 전 $1.47) — 발표 당일 주가 +10%', 'q1', 'Expeditors 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 24일 — Q4 2025 실적', '2026-02-24',
     '순이익 $201M · 희석 EPS $1.49(1년 전 $1.68) · 2025년 매출 $11.07B·EPS $5.95 · 자사주 매입 $3B 승인 — 발표 당일 주가 −7%', 'q4', 'Expeditors 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 4일 — Q3 2025 실적', '2025-11-04',
     '매출 $2.89B · 순이익 $222M · 희석 EPS $1.64(1년 전 $1.63) — 발표 당일 주가 +11%', 'q3', 'Expeditors 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 18, 'nt': 13, 'mean': 195, 'median': 200, 'low': 100, 'high': 245, 'sb': 3, 'b': 0, 'h': 10, 's': 2, 'ss': 3}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 서비스 3개(수동 지도). 원문 대조: Q2 2026 1,494.8/1,296.6/710.9(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"expd:AirfreightServicesMember": ["항공 화물", "#0b3d91"], "expd:CustomsBrokerageAndOtherServicesMember": ["통관·기타 서비스", "#5b84c8"],
             "expd:OceanFreightAndOceanServicesMember": ["해상 화물", "#e0a526"]},
 "ignore": []
}
