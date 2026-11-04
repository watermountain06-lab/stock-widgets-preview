BUILD = {}
# LULU(룰루레몬) v2 카드 설정 — 자동 카드(AUTO). 회계연도 1월 31일에 가까운 일요일(52/53주 — FY24 53주). 운동복·애슬레저, 부문은 미주·중국 본토·기타 해외.
# 출처: SEC XBRL, Q2 FY26 10-Q(2026-09-03), 실적 보도자료(Q3 FY25~Q2 FY26, 8-K 2.02항 — 장 마감 뒤 16:0x 동부 → 다음 날 반응), StockAnalysis. 사전 조사 scratchpad pre/LULU.md.
# 엔진 입력(2026-11-03): 차입금 0, 현금은 합계 태그 $1,389.7M, 운용리스 $2,141.1M, 낡은 비지배지분(2012) 제외(EV_TAGS_BY_CIK). Q4 FY23~FY25 EPS 보도자료 값.
# 주식 수: 표지 보통주 105.59M만 쓴다 — 교환주식 5.12M(보통주와 1:1, EPS 분모에는 포함)이 빠져 시가총액이 4.6% 작다. share_adjust는 빼기만이라 못 더함(판정과 먼 거리, 백로그).
# 민감도(Codex·Fable r1): 현금흐름 +1이 뒤집히려면 5년 내내 영업이익률 ≤10.3% — Q3 반영 뒤 TTM 마진도 약 15.6%라 유지.
# 일회성: Q2 FY26 관세(IEEPA) 환급 주당 +0.86(최근 4분기 12.21의 7%, 이익 쪽) — 빼도 PER 9.4로 표 같음. Q3 FY26 가이던스 EPS 0.93~0.98(전년 2.59)로 이익 급감 중.
CIK = '0001397187'
CUR, YO, QO = '2026-08-02', '2025-08-03', '2026-05-03'
QLABEL, YL, QQL = 'Q2 FY26', 'Q2 FY25', 'Q1 FY26'
L8 = ['Q3 FY24', 'Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26']
FY_ENDS, FY_LABEL = ('2026-02-01', '2025-02-02'), 'FY2025'
VOTES, VERDICT = (1, 1, 1), '저평가'
CO = 'lululemon'
S_ = 'https://www.sec.gov/Archives/edgar/data/1397187/'
SEC = S_
TENQ = S_ + '000139718726000127/lulu-20260802.htm'; TENQ_NAME = 'Q2 FY26 10-Q'
PR = {'q2': S_ + '000139718726000126/lulu-20260802xex991.htm', 'q1': S_ + '000139718726000077/lulu-20260503xex991.htm', 'q4': S_ + '000139718726000019/lulu-20260201xex991.htm', 'q3': S_ + '000139718725000054/lulu-20251102xex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="luluFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('이익이 빠르게 줄고 있다 — 회사가 낸 3분기 EPS 전망은 $0.93~0.98로 1년 전 $2.59의 3분의 1 수준이다. 최근 4분기 이익 기준 배수와 내재가치는 이 감소를 반영하지 못해 실제보다 싸게 보일 수 있다. 내재가치는 영업이익률이 5년 내내 10% 아래로 떨어져야 현재가 근처로 내려온다(지금 17.8%, 환급 빼면 16.6%). '
              '2분기 이익에 관세 환급(주당 $0.86)이 들어 있다. 시가총액에는 교환주식(약 512만 주)이 빠져 있어 4.6% 작게 잡힌다(넣어도 동종업 점수 약 0.5점 차이). 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['NKE', 'DECK', 'RL', 'TPR', 'TJX', 'ROST']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '의류·신발 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(LULU 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 의류·신발 6곳만 보인다.')
# 매출(Q2 FY26 10-Q 부문) — 1,616.8 + 407.1 + 391.8 = 2,415.6.
SEG = [('미주', 1616.8, '#d22030'), ('중국 본토', 407.1, '#1d1d1b'), ('기타 해외', 391.8, '#8a8d8f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역 부문별(Q2 FY26)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:0x 동부) → 다음 날.
NEWS_RANGE = '2025.12 ~ 2026.09'
NEWS = [
    ('red', '2026년 9월 3일 장 마감 뒤 — Q2 FY26 실적', '2026-09-04',
     '매출 $2.42B(−4.3%) · 순이익 $329M · 희석 EPS $2.92(1년 전 $3.10, 관세 환급 $0.86 포함) · 3분기 EPS 전망 $0.93~0.98 — 다음 날 주가 −17.4%', 'q2', 'lululemon 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 6월 4일 장 마감 뒤 — Q1 FY26 실적', '2026-06-05',
     '매출 $2.47B(+4.3%) · 순이익 $195M · 희석 EPS $1.69(1년 전 $2.60) · 연간 EPS 전망 하향 — 다음 날 주가 −8.6%', 'q1', 'lululemon 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 17일 장 마감 뒤 — Q4 FY25 실적', '2026-03-18',
     '매출 $3.64B(+0.8%, 1년 전 14주) · 순이익 $587M · 희석 EPS $5.01(1년 전 $6.14) · FY25 EPS $13.26 — 다음 날 주가 +3.8%', 'q4', 'lululemon 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 11일 장 마감 뒤 — Q3 FY25 실적', '2025-12-12',
     '매출 $2.57B(+7.1%) · 순이익 $307M · 희석 EPS $2.59(1년 전 $2.87) · 자사주 $1B 추가 승인 — 다음 날 주가 +9.6%', 'q3', 'lululemon 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 1, 'nt': 1, 'mean': 0, 'median': 0, 'low': 0, 'high': 0, 'sb': 0, 'b': 0, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-03'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q2 FY26 1,616.8/407.1/391.8(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"lulu:AmericasSegmentMember": ["미주", "#d22030"], "lulu:ChinaMainlandSegmentMember": ["중국 본토", "#1d1d1b"], "lulu:OtherCountrySegmentMember": ["기타 해외", "#8a8d8f"]},
 "ignore": []
}
