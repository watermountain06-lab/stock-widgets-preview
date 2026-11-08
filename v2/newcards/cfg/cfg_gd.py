# GD(제너럴 다이내믹스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일(1~3분기는 일요일 끝 — Q2 2026 = 4/6~7/5). 방산·항공 — Gulfstream 비즈니스 제트기, 잠수함·함정(Electric Boat·NASSCO), 전차·탄약, 국방 IT.
# 출처: SEC XBRL + 인라인 XBRL 보충(BUILD overlay — companyfacts에 7/29 Q2 10-Q가 없다), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/GD.md.
# 엔진 입력(2026-10-25): 차입금 = 1년 안 $1,256M + 장기 $6,260M(DEBT_TOTAL_TAG), 리스 태그는 운용 + 금융 합계(FL_IN_DEBT — 금융리스 $392M을 따로 더하지 않는다), 현금 $4,333M(고객 선수금 $11.0B 때문에 분기마다 크게 움직인다), 비지배지분·우선주 없음.
# EPS 태그는 계속사업 희석 EPS뿐(EarningsPerShareDiluted 없음). 일회성: 회사가 조정 EPS를 내지 않는다 — 최근 4분기 일회성 없음(계약 추정 변경 효과는 상시 항목).
BUILD = {'overlay': True, 'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}
CIK = '0000040533'
CUR, YO, QO = '2026-07-05', '2025-06-29', '2026-04-05'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'General Dynamics'
S_ = 'https://www.sec.gov/Archives/edgar/data/40533/'
SEC = S_
TENQ = S_ + '000004053326000032/gd-20260705.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000004053326000029/gd-20260705exhibit991.htm', 'q1': S_ + '000004053326000010/gd-20260405exhibit991.htm',
      'q4': S_ + '000004053326000003/gd-20251231exhibit991.htm', 'q3': S_ + '000004053325000043/gd-20250928exhibit9911.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="gdFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('정부 계약은 고객 선수금이 커서(약 $11B) 분기 현금흐름과 현금 잔액이 크게 흔들린다. 1~3분기는 일요일에 끝나 분기 길이가 달력 분기와 조금 다르다. '
              '감가상각은 감가상각 + 무형자산 상각으로 이어 붙여 금융리스 상각이 빠진다 — 회사 합계보다 7~11% 작아 EV/EBITDA가 1% 남짓 높게 나온다. '
              'SEC 요약 자료에 최신 10-Q가 아직 없어 원문 인라인 XBRL로 채웠다.')
PH = ['LMT', 'NOC', 'RTX', 'HII', 'LDOS', 'TDG']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '방산 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(GD 제외)와 배수 순위를 매긴 값이다.',
            '방산·항공·기계·운송·건설 서비스가 섞여 있다. 차트에는 방산 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 해양 4,660 + 기술 3,619 + 항공 3,525 + 전투 2,290 = 14,094.
SEG = [('해양 시스템', 4660, '#002f6c'), ('기술(국방 IT)', 3619, '#5b87c5'), ('항공(Gulfstream)', 3525, '#9aa5b1'), ('전투 시스템', 2290, '#c8a24a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 회사는 조정 EPS를 내지 않는다). 반응일: 장 전 발표(07:50~08:01 동부) → 같은 날. 넣지 않은 8-K: 임원(차기 CEO 2027-01), 401(k) 주식 청약 철회권, 주총.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 29일 장 전 — Q2 2026 실적', '2026-07-29',
     '매출 $14.09B(+8.1%) · 순이익 $1.16B · 희석 EPS $4.24(1년 전 $3.74)', 'q2', 'General Dynamics 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 29일 장 전 — Q1 2026 실적', '2026-04-29',
     '매출 $13.48B(+10.3%) · 순이익 $1.13B · 희석 EPS $4.10(1년 전 $3.66) — 당일 주가 +8%', 'q1', 'General Dynamics 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 28일 장 전 — Q4 2025 실적', '2026-01-28',
     '매출 $14.38B · 순이익 $1.14B · 희석 EPS $4.17(1년 전 $4.15) · 2025년 EPS $15.45', 'q4', 'General Dynamics 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 24일 장 전 — Q3 2025 실적', '2025-10-24',
     '매출 $12.91B · 순이익 $1.06B · 희석 EPS $3.88(1년 전 $3.35)', 'q3', 'General Dynamics 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 15, 'mean': 413.8, 'median': 415, 'low': 309, 'high': 480, 'sb': 10, 'b': 4, 'h': 9, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 4개(축 하나만 붙은 값). 원문 대조: Q2 2026 4,660/3,619/3,525/2,290(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"gd:MarineSystemsMember": ["해양 시스템", "#002f6c"], "gd:TechnologiesMember": ["기술(국방 IT)", "#5b87c5"],
             "gd:AerospaceMember": ["항공(Gulfstream)", "#9aa5b1"], "gd:CombatSystemsMember": ["전투 시스템", "#c8a24a"]},
 "ignore": []
}
