BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # 2023-04 뒤 희석 EPS는 계속사업 태그에만 있다(EarningsPerShareDiluted는 2022-12에 멈춤)
# VRSN(베리사인) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. .com·.net 도메인 레지스트리(독점 운영 계약), 인터넷 루트 서버 운영. 단일 사업 — 매출 구성은 지역별.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-22 16:33 장 마감 뒤 접수), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 마감 직후 16시 발표 → 다음 날 반응), StockAnalysis. 사전 조사 scratchpad pre/VRSN.md.
# 엔진 입력(2026-10-29): 희석 EPS는 2023-04부터 계속사업 태그(BUILD eps_tag — EarningsPerShareDiluted는 2022-12에 멈춤), 비지배지분 없음(EV_TAGS_BY_CIK nci 빈 목록 — 2010년 값이 낡은 값으로 DCF를 막았다).
# 차입금 = 선순위 채권 $1,786M(7/20 상환 뒤, DEBT_TOTAL_TAG SeniorNotesCurrent + SeniorLongTermNotes — 기본은 0이었다), 현금 $207M + 단기투자 $269M. 자기자본 −$2,285M(자사주 매입). 일회성: 최근 4분기 GAAP 9.30 중 Q3 매각예정 자산 평가손실 0.06(0.6%)뿐.
CIK = '0001014473'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'VeriSign'
S_ = 'https://www.sec.gov/Archives/edgar/data/1014473/'
SEC = S_
TENQ = S_ + '000101447326000039/vrsn-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000101447326000038/q32026earningsrelease.htm', 'q2': S_ + '000101447326000026/q22026earningsrelease.htm', 'q1': S_ + '000101447326000019/q12026earningsrelease.htm', 'q4': S_ + '000101447326000005/q42025earningsrelease.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="vrsnFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('자사주 매입과 배당으로 이익보다 많이 돌려줘서(9개월 $620M + $221M = $841M, 순이익 $644M) 자기자본이 음수(−$2.3B)라 PBR은 뜻이 없다. 지역 매출은 등록 대행사(레지스트라) 청구지 기준이다. '
              '.com 가격은 ICANN 협약으로 인상 상한이 있고, 2026-09 가격 독점을 문제 삼은 집단소송(Kessler)이 제기됐다(손실 추정 불가). 동종업 점수는 카드 유니버스 IT(반도체·소프트웨어·하드웨어) 기준이다.')
PH = ['MSFT', 'ORCL', 'CRM', 'PANW', 'CRWD', 'CSCO']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소프트웨어·인터넷 기반 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(VRSN 제외)과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 섞여 있다. 차트에는 소프트웨어·인터넷 기반 6곳만 보인다.')
# 매출(Q3 2026 10-Q 지역) — 미국 295.1 + EMEA 78.0 + 아시아태평양 46.8 + 기타 23.1 = 443.0.
SEG = [('미국', 295.1, '#0e4c92'), ('유럽·중동·아프리카', 78.0, '#5a8fd0'), ('아시아태평양', 46.8, '#f7a800'), ('기타', 23.1, '#9aa5b1')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 직후 발표(16:0x 동부) → 다음 날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 22일 장 마감 뒤 — Q3 2026 실적', '2026-10-23',
     '매출 $443M(+5.7%) · 순이익 $213M · 희석 EPS $2.35(1년 전 $2.27) — 매각예정 자산 평가손실 $7.5M 포함 · 다음 날 주가 −1.4%', 'q3', 'VeriSign 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 23일 장 마감 뒤 — Q2 2026 실적', '2026-07-24',
     '매출 $435M · 순이익 $217M · 희석 EPS $2.38(1년 전 $2.21) · 연간 전망 상향 — 다음 날 주가 +7.0%', 'q2', 'VeriSign 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 23일 장 마감 뒤 — Q1 2026 실적', '2026-04-24',
     '매출 $429M · 순이익 $215M · 희석 EPS $2.34(1년 전 $2.10) — 다음 날 주가 −2.8%', 'q1', 'VeriSign 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 5일 장 마감 뒤 — Q4 2025 실적', '2026-02-06',
     '매출 $425M · 순이익 $206M · 희석 EPS $2.23(1년 전 $2.00) · 2025년 EPS $8.81 · 분기 배당 $0.81로 인상 — 다음 날 주가 −7.6%', 'q4', 'VeriSign 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 5, 'nt': 4, 'mean': 352, 'median': 367, 'low': 316, 'high': 380, 'sb': 3, 'b': 0, 'h': 1, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 295.1/78.0/46.8/23.1(2026-10-29) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "srt:StatementGeographicalAxis",
 "extra": {},
 "members": {"country:US": ["미국", "#0e4c92"], "us-gaap:EMEAMember": ["유럽·중동·아프리카", "#5a8fd0"], "srt:AsiaPacificMember": ["아시아태평양", "#f7a800"], "vrsn:OtherMember": ["기타", "#9aa5b1"]},
 "ignore": []
}
