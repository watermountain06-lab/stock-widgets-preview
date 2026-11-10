CIK = '0000719955'
# WSM(윌리엄스소노마) v2 카드 설정 — 자동 카드(AUTO). 회계연도 1월 말에 가까운 일요일(52/53주 — Q2 FY26 = 2026-05-04~08-02). 가정용 가구·주방용품, 브랜드 다섯(포터리반·웨스트엘름·포터리반 키즈/틴·윌리엄스소노마·기타).
# 출처: SEC XBRL, Q2 FY26 10-Q(2026-08-28), 실적 보도자료(Q3 FY25~Q2 FY26, 8-K 2.02항 — 장 전 08~09시 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/WSM.md.
# 엔진 입력(2026-11-03): 차입금 없음(회전 한도 $600M 미사용, 옛 부채 태그는 2022에 멈춤), 현금 $1,029M, 운용리스 $1,528M. 2024-07 2:1 분할(KNOWN_SPLITS), Q4 FY21~FY25 EPS는 보도자료 값(Q4_EPS_OVERRIDE — FY24 4분기는 14주).
# 2026-10-30 사용자 결정(공시 대기만으로 보류하지 않는다) — Q3 FY26 10-Q(11월 하순 예상) 전 Q2 기준.
# 일회성: 최근 4분기 GAAP 9.77 중 Q2 FY26 관세 환급 순이익 주당 0.74(7.6%, 이익 쪽) — 빼면 EPS가 줄어 배수가 더 비싸지므로 판정은 같다.
CIK = '0000719955'
CUR, YO, QO = '2026-08-02', '2025-08-03', '2026-05-03'
QLABEL, YL, QQL = 'Q2 FY26', 'Q2 FY25', 'Q1 FY26'
L8 = ['Q3 FY24', 'Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26']
FY_ENDS, FY_LABEL = ('2026-02-01', '2025-02-02'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Williams-Sonoma'
S_ = 'https://www.sec.gov/Archives/edgar/data/719955/'
SEC = S_
TENQ = S_ + '000071995526000208/wsm-20260802.htm'; TENQ_NAME = 'Q2 FY26 10-Q'
PR = {'q2': S_ + '000071995526000203/exhibit991fy2026q2earnings.htm', 'q1': S_ + '000071995526000126/exhibit991fy2026q1earnings.htm', 'q4': S_ + '000071995526000030/exhibit991fy2025q4earnings.htm', 'q3': S_ + '000071995525000043/exhibit991fy2025q3earnings.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="wsmFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('Q2 FY26 이익에 관세(IEEPA) 환급 순이익 주당 $0.74가 들어 있다 — 빼면 배수가 더 비싸져 동종업 점수가 30 아래(약 28)로 내려가지만 판정은 고평가로 같다. 3분기에 환급 약 $29M이 더 잡힐 예정이다. FY24 분기 실적은 재고 손실 정정 뒤 값이다. '
              '빚 없이 자사주를 꾸준히 사서 자본이 작아 PBR이 높다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['HD', 'LOW', 'TJX', 'ROST', 'BBY', 'TSCO']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소매 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(WSM 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 소매 6곳만 보인다.')
# 매출(Q2 FY26 10-Q 브랜드) — 770.8 + 496.3 + 297.4 + 268.8 + 126.4 = 1,959.8.
SEG = [('포터리반', 770.8, '#1f3a2e'), ('웨스트엘름', 496.3, '#a68b5b'), ('포터리반 키즈·틴', 297.4, '#6b9bc3'), ('윌리엄스소노마', 268.8, '#8c2f2f'), ('기타(리주버네이션 등)', 126.4, '#9aa5b1')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 브랜드별(Q2 FY26)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(08~09시 동부) → 같은 날.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 26일 장 전 — Q2 FY26 실적', '2026-08-26',
     '매출 $1.96B(+6.7%) · 순이익 $338M · 희석 EPS $2.84(1년 전 $2.00) · 조정 EPS $2.10(관세 환급 제외) · 연간 전망 상향 — 당일 주가 +1.1%', 'q2', 'Williams-Sonoma 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 21일 장 전 — Q1 FY26 실적', '2026-05-21',
     '매출 $1.81B(+4.4%) · 순이익 $231M · 희석 EPS $1.93(1년 전 $1.85) — 당일 주가 +6.5%', 'q1', 'Williams-Sonoma 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 18일 장 전 — Q4 FY25 실적', '2026-03-18',
     '매출 $2.36B(1년 전은 14주) · 순이익 $368M · 희석 EPS $3.04(1년 전 $3.28) · FY25 EPS $8.84 · 분기 배당 15% 인상 — 당일 주가 +1.1%', 'q4', 'Williams-Sonoma 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 19일 장 전 — Q3 FY25 실적', '2025-11-19',
     '매출 $1.88B(+4.6%) · 순이익 $242M · 희석 EPS $1.96(1년 전 $1.87) · 자사주 $1B 추가 승인 — 당일 주가 −3.4%', 'q3', 'Williams-Sonoma 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 16, 'mean': 256.31, 'median': 259, 'low': 190, 'high': 286, 'sb': 9, 'b': 2, 'h': 11, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q2 FY26 770.8/496.3/297.4/268.8/126.4(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"wsm:PotteryBarnSegmentMember": ["포터리반", "#1f3a2e"], "wsm:WestElmSegmentMember": ["웨스트엘름", "#a68b5b"], "wsm:PotteryBarnKidsAndTeenSegmentMember": ["포터리반 키즈·틴", "#6b9bc3"], "wsm:WilliamsSonomaSegmentMember": ["윌리엄스소노마", "#8c2f2f"], "us-gaap:AllOtherSegmentsMember": ["기타(리주버네이션 등)", "#9aa5b1"]},
 "ignore": ["wsm:ReportableSegmentMember"]
}
