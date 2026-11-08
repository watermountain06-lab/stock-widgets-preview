# NTAP(넷앱) v2 카드 설정 — 자동 카드(AUTO). 회계연도 4월 마지막 금요일. 데이터 스토리지(올플래시·하이브리드 플래시, ONTAP)·퍼블릭 클라우드 서비스.
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-09-02), 실적 보도자료(Q2 FY26~Q1 FY27, 8-K 2.02항 — 장 마감 뒤 발표, 2:30 PT 콜 → 다음 거래일 반응), StockAnalysis. 사전 조사 자료표 scratchpad pre/NTAP.md.
# 엔진 입력(2026-10-24): companyfacts의 Q3 FY22 매출 중복 행($796M)은 v2/fact_fixes.json(안건 E55)이 뺀다. 차입금 $2,488M(사채), 현금 $1,573M + 단기투자 $2,003M.
# FY2027은 53주 — Q1 FY27이 14주라(1년 전 13주) 전년 대비 성장률이 약 1/13 부풀어 있다(MODEL_NOTE).
CIK = '0001002047'
CUR, YO, QO = '2026-07-31', '2025-07-25', '2026-04-24'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-04-24', '2025-04-25'), 'FY2026'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'NetApp'
S_ = 'https://www.sec.gov/Archives/edgar/data/1002047/'
SEC = S_
TENQ = S_ + '000119312526380207/ntap-20260731.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000100204726000003/ntap-ex99_1.htm', 'q4': S_ + '000119312526245196/ntap-ex99_1.htm',
      'q3': S_ + '000119312526076545/ntap-ex99_1.htm', 'q2': S_ + '000119312525297164/ntap-ex99_1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ntapFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 35)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장.
MODEL_NOTE = ('FY2027은 53주 회계연도라 Q1 FY27이 14주다(1년 전 13주) — 전년 대비 매출·이익 성장률이 한 주만큼 부풀어 있고(주당으로 맞추면 매출 성장은 약 21%), 최근 4분기 합은 53주치다. '
              'Q1 FY27 GAAP 이익에는 새 구조조정(인력 감축) 비용이 들어 있다. 자사주 매입이 커서 장부 자본이 작아 PBR·ROE는 의미가 약하다. '
              '매출의 대부분은 기업용 하이브리드 클라우드(올플래시 비중이 커지는 중)이고, 퍼블릭 클라우드 서비스는 작다.')
HEALTH_EXTRA = '장부 자본이 자사주 매입으로 작아 부채비율이 높게 보이지만, 현금·단기투자가 차입금보다 많다.'
# 14주 표시(Fable r1 권장) — EPS 칸의 전년 대비는 14주 대 13주
POST = [r'''
h = h.replace('<div class="stat-sub">GAAP · 1년 전 $1.15 (+63%)</div>', '<div class="stat-sub">GAAP · 1년 전 $1.15 (+63%, 14주 대 13주)</div>', 1)
''']
PH = ['STX', 'DELL', 'CSCO', 'ANET', 'IBM', 'MU']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '저장장치·하드웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(NTAP 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 저장장치·하드웨어 6곳만 보인다.')
# 매출(Q1 FY27 10-Q 부문) — 하이브리드 클라우드 1,819(올플래시 1,309 포함) + 퍼블릭 클라우드 206 = 2,025.
SEG = [('하이브리드 클라우드', 1819.0, '#0067c5'), ('퍼블릭 클라우드', 206.0, '#5aa3e8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다. 주 수도 적지 않는다 — auto_card가 분기 길이가 다르면 각주에 써 주고(14주 대 13주), 제목에 적으면 13주 분기에서 틀린 말이 된다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 비GAAP·가이던스는 쓰지 않는다). 반응일: 장 마감 뒤 발표 → 다음 거래일.
# 넣지 않은 8-K: 이사 선임(2026-01-12), 주총(2025-09·2026-09). DataPelago 인수($193M, 8-K 없음)는 작아서 뺐다.
NEWS_RANGE = '2025.11 ~ 2026.09'
NEWS = [
    ('green', '2026년 9월 2일 — Q1 FY27 실적(14주 분기)', '2026-09-03',
     '매출 $2.03B(1년 전 13주 $1.56B) · 순이익 $375M · 희석 EPS $1.88(1년 전 $1.15) — 구조조정 비용 $56M 포함', 'q1', 'NetApp 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 28일 — Q4 FY26 실적', '2026-05-29',
     '매출 $1.95B(1년 전 $1.73B) · 순이익 $404M · 희석 EPS $2.03(1년 전 $1.65) · 자사주 $1.0B 추가 승인 — 발표 다음 날 주가 +22%', 'q4', 'NetApp 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 26일 — Q3 FY26 실적', '2026-02-27',
     '매출 $1.71B · 순이익 $334M · 희석 EPS $1.67(1년 전 $1.44)', 'q3', 'NetApp 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 25일 — Q2 FY26 실적', '2025-11-26',
     '매출 $1.71B · 순이익 $305M · 희석 EPS $1.51(1년 전 $1.42) — 구조조정 비용 $23M 포함', 'q2', 'NetApp 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 15, 'mean': 213.53, 'median': 195, 'low': 170, 'high': 300, 'sb': 7, 'b': 1, 'h': 13, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 2개(수동 지도). 원문 대조: Q1 FY27 1,819/206(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax", "us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"ntap:HybridCloudSegmentMember": ["하이브리드 클라우드", "#0067c5"], "ntap:PublicCloudSegmentMember": ["퍼블릭 클라우드", "#5aa3e8"]},
 "ignore": []
}
