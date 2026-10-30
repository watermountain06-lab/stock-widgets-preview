# DXCM(덱스컴) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 연속혈당측정기(CGM — G7·Stelo), 단일 부문.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/DXCM.md.
# 엔진 입력(2026-10-25): 차입금 = 전환사채(DEBT_TOTAL_TAG — 기본 목록에 없어 0이었다, Q2 2026 $1,242.8M), 단기투자 = 유동 매도가능 채무증권 $704.8M(EV_TAGS), 현금 $1,105M.
# 2022-06 4:1 분할(KNOWN_SPLITS). 일회성: Q3 2025 지분 투자 이익 세전 $82.7M(주당 약 $0.20, 최근 4분기 EPS 2.53의 약 8%) — 다음 분기 실적이 나오면 빠진다.
CIK = '0001093557'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'DexCom'
S_ = 'https://www.sec.gov/Archives/edgar/data/1093557/'
SEC = S_
TENQ = S_ + '000109355726000143/dxcm-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000109355726000142/dxcm06302026-exhibit991.htm', 'q1': S_ + '000109355726000072/dxcm3312026-exhibit991.htm',
      'q4': S_ + '000109355726000025/dxcm12312025-exhibit991.htm', 'q3': S_ + '000109355725000278/dxcm09302025-exhibit991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="dxcmFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (5, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 GAAP 이익에는 Q3 2025 지분 투자 이익(일회성, 영업 밖)이 들어 있어 PER이 그만큼 낮게 나온다 — 다음 분기 실적이 나오면 빠진다. '
              '전환사채가 있어 희석 EPS는 전환을 가정해 계산된다. 2022년 4:1 분할 이전 주당 값은 분할을 반영해 비교한다.')
PH = ['ABT', 'MDT', 'ISRG', 'BSX', 'SYK', 'PODD']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '의료기기 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': '의료기기 PBR 비교', 'psr': '의료기기 PSR 비교',
                'pcr': '의료기기 PCR(FCF) 비교', 'evebitda': '의료기기 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(DXCM 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·유통이 섞여 있다. 차트에는 의료기기 6곳만 보인다.')
# 매출(Q2 2026 10-Q, 지역별) — 미국 933.4 + 해외 375.0 = 1,308.4.
SEG = [('미국', 933.4, '#58a618'), ('해외', 375.0, '#9fd36a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표 → 다음 거래일. 넣지 않은 8-K: 예비 매출(1/12), CEO 교체(2025-12-22 — 2026-01-01부터 Jacob Leach), 이사회·투자자의 날·COO.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('green', '2026년 7월 30일 — Q2 2026 실적', '2026-07-31',
     '매출 $1.31B(+13.1%) · 순이익 $249M · 희석 EPS $0.64(1년 전 $0.45) — 발표 다음 날 주가 +12%', 'q2', 'DexCom 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 30일 — Q1 2026 실적', '2026-05-01',
     '매출 $1.19B · 순이익 $200M · 희석 EPS $0.51(1년 전 $0.27)', 'q1', 'DexCom 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 12일 — Q4 2025 실적', '2026-02-13',
     '매출 $1.26B · 순이익 $267M · 희석 EPS $0.68(1년 전 $0.38) — 발표 다음 날 주가 +7.6%', 'q4', 'DexCom 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 30일 — Q3 2025 실적', '2025-10-31',
     '매출 $1.21B · 순이익 $284M · 희석 EPS $0.70(1년 전 $0.34) — 지분 투자 이익 세전 $82.7M 포함 · 발표 다음 날 주가 −15%', 'q3', 'DexCom 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 29, 'nt': 21, 'mean': 95.43, 'median': 95, 'low': 77, 'high': 115, 'sb': 22, 'b': 4, 'h': 3, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 지역 2개(수동 지도). 원문 대조: Q2 2026 933.4/375.0(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:StatementGeographicalAxis",
 "extra": {},
 "members": {"country:US": ["미국", "#58a618"], "us-gaap:NonUsMember": ["해외", "#9fd36a"]},
 "ignore": []
}
