BUILD = {'cover_shares': True}   # Class A 37,700,963 + Class B 21,881,276 = 59,582,239(2026-07-31) — 표지 주식 수가 클래스별뿐
# RL(랄프 로렌) v2 카드 설정 — 자동 카드(AUTO). 회계연도 3월 말에 가까운 토요일(52/53주 — FY27은 53주). 의류·잡화 브랜드, 부문은 북미·유럽·아시아 + 기타(라이선스).
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-08-06), 실적 보도자료(Q2 FY26~Q1 FY27, 8-K 2.02항 — 장 전 08시 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/RL.md.
# 엔진 입력(2026-11-03): Class A + Class B — 표지 주식 수가 클래스별뿐이라 BUILD cover_shares(59.58M, 2026-07-31). 설비투자는 FY26 10-K가 연간 값을 PaymentsToAcquireMachineryAndEquipment(10-K 현금흐름표 태그)로 내 EXTRA_TAGS로 보강(TTM $274.2M).
# 차입금 $1,239.4M(선순위채 두 종), 현금 $1,719.0M + 단기투자 $222.6M, 운용리스 $1,536.7M + 금융리스 $227.8M. Q4 FY22~FY24 EPS는 보도자료 값(Q4_EPS_OVERRIDE).
# 2026-10-30 사용자 결정(공시 대기만으로 보류하지 않는다) — Q2 FY27 실적(11월 초 예상) 전 Q1 기준. 일회성: 최근 4분기 GAAP 15.87 중 NGT 전환 프로젝트·구조조정 등 회사 조정 항목 주당 1.53(9.6%, 비용 쪽).
# 일회성 시험: 영업이익에 세전 $122.3M을 되돌리면 현금흐름 기본 $240.00 → $247.15(비율 1.61, −2 그대로). 빼면 이익이 커져 배수 점수는 오른다(자기 13.1·동종 40.3 — 문턱과 멀다, scratchpad rl_e54).
CIK = '0001037038'
CUR, YO, QO = '2026-06-27', '2025-06-28', '2026-03-28'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-03-28', '2025-03-29'), 'FY2026'
VOTES, VERDICT = (-1, 0, -1), '적정~고평가'
CO = 'Ralph Lauren'
S_ = 'https://www.sec.gov/Archives/edgar/data/1037038/'
SEC = S_
TENQ = S_ + '000162828026053992/rl-20260627.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000162828026053896/rl-20260627ex991xpressrele.htm', 'q4': S_ + '000162828026037053/rl-20260328xex991xpressrel.htm', 'q3': S_ + '000162828026005615/rl-20251227ex991xpressrele.htm', 'q2': S_ + '000162828025049886/rl-20250927ex991xpressrele.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="rlFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 이익에 다년 전환 프로젝트(NGT)·구조조정 등 회사 조정 비용 주당 $1.53(9.6%)이 들어 있다. 회사 조정 EPS는 $17.40이다. 되돌려도 판정은 같다. '
              '시가총액은 상장된 Class A 가격에 Class A·B 합계 주식 수(59.6M)를 곱한 값이다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['TPR', 'NKE', 'LULU', 'DECK', 'TJX', 'ROST']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '의류·잡화 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(RL 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 의류·잡화 6곳만 보인다.')
# 매출(Q1 FY27 10-Q 부문, 축 하나만 붙은 값 — 지역 축 값과 다르다) — 740.3 + 594.4 + 589.3 + 35.8 = 1,959.8.
SEG = [('북미', 740.3, '#041e42'), ('유럽', 594.4, '#a6192e'), ('아시아', 589.3, '#b9975b'), ('기타(라이선스)', 35.8, '#9aa5b1')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q1 FY27)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(08시 동부) → 같은 날.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 6일 장 전 — Q1 FY27 실적', '2026-08-06',
     '매출 $1.96B(+14.0%) · 순이익 $262M · 희석 EPS $4.28(1년 전 $3.52) · 조정 EPS $4.59 · 연간 전망 상향 — 당일 주가 +4.0%', 'q1', 'Ralph Lauren 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 21일 장 전 — Q4 FY26 실적', '2026-05-21',
     '매출 $1.98B(+16.6%) · 순이익 $152M · 희석 EPS $2.45(1년 전 $2.03) · FY26 매출 $8.11B · EPS $15.11 · 배당 10% 인상 — 당일 주가 +13.9%', 'q4', 'Ralph Lauren 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 5일 장 전 — Q3 FY26 실적', '2026-02-05',
     '매출 $2.41B(+12.2%) · 순이익 $362M · 희석 EPS $5.82(1년 전 $4.66) · 조정 EPS $6.22 — 당일 주가 −4.5%', 'q3', 'Ralph Lauren 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 6일 장 전 — Q2 FY26 실적', '2025-11-06',
     '매출 $2.01B(+16.5%) · 순이익 $208M · 희석 EPS $3.32(1년 전 $2.31) · 조정 EPS $3.79 — 당일 주가 −0.6%', 'q2', 'Ralph Lauren 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 18, 'nt': 14, 'mean': 458.36, 'median': 460, 'low': 425, 'high': 529, 'sb': 11, 'b': 5, 'h': 1, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q1 FY27 740.3/594.4/589.3/35.8(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"rl:NorthAmericaSegmentMember": ["북미", "#041e42"], "rl:EuropeSegmentMember": ["유럽", "#a6192e"], "rl:AsiaSegmentMember": ["아시아", "#b9975b"], "rl:OtherNonReportableSegmentRelatedMember": ["기타(라이선스)", "#9aa5b1"]},
 "ignore": []
}
