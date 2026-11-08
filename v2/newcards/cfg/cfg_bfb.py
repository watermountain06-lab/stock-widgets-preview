CIK = '0000014693'
BUILD = {'cover_shares': True}   # 표지 주식 수가 Class A·B별뿐(dei 합계 태그 없음 — CommonStockSharesOutstanding은 2025-04에 멈춤, 2026-11-07)
# BFB(브라운포맨 B주) v2 카드 설정 — 자동 카드(AUTO). 회계연도 4월 30일. 위스키(Jack Daniel's 등)·즉석 음료(RTD)·데킬라·진 등 주류.
# 티커: 사이트 표기 BFB(BRKB와 같은 방식), Yahoo BF-B(prep·price_arrays·seed 매핑), StockAnalysis bf.b. 시가총액은 A·B 두 종류 합친 주식 수 기준.
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-09-02 16:07 동부 장 마감 뒤 → 첫 세션 09-03, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 장 전 08:0x 동부 → 그날),
#        Pernod Ricard 논의 확인(2026-03-26 19:14 동부 → 03-27)·종료(04-28 16:45 → 04-29), CEO 은퇴 발표(07-13 16:40 → 07-14), CFO 선임(03-16 09:02 → 그날).
# 보류 목록 D군(안건 E54) — 일회성이 30% 미만이라 정식 판정(GAAP + 문장): Q4 FY26 브랜드 손상 $132M(Gin Mare $45M·Diplomático $87M)이 최근 4분기 GAAP EPS 1.55의 약 14%(세후 근사).
# 4분기 EPS: FY22~FY26은 보도자료와 역산이 같고(Codex r1 대조), FY21만 보도자료 $0.25로 덮는다(Q4_EPS_OVERRIDE).
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-04-30', '2025-04-30'), 'FY2026'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Brown-Forman'
S_ = 'https://www.sec.gov/Archives/edgar/data/14693/'
SEC = S_
TENQ = S_ + '000001469326000052/bfb-20260731.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000001469326000048/fy27_q1xerevergreen.htm', 'q4': S_ + '000001469326000018/fy26_q4xerevergreen.htm',
      'q3': S_ + '000001469326000005/fy26_q3xerevergreen.htm', 'pr1': S_ + '000001469326000014/brown-formanstatementonper.htm',
      'pr2': S_ + '000001469326000016/brown-formanandpernodricar.htm', 'ceo': S_ + '000001469326000033/fy27julyceoannouncesretire.htm',
      'cfo': S_ + '000001469326000012/releasebrown-formannamesji.htm', 'notes': S_ + '000119312526396679/d178040d8k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="bfbFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 GAAP 이익에는 2026 회계연도 4분기 브랜드 손상 $132M(Gin Mare $45M·Diplomático $87M, 비현금)이 들어 있다 — 4분기 실효세율(25.1%)로 세후를 근사하면 최근 4분기 EPS의 약 14%라 GAAP 그대로 쓴다. 다만 Gin Mare는 2025 회계연도에도 $47M 손상이 있어, 브랜드 손상이 한 번으로 끝난다고 보기는 어렵다. '
              '2026년 3월 프랑스 Pernod Ricard와 합병에 가까운 결합을 논의한다고 확인했다가 4월 조건이 맞지 않아 논의를 끝냈고, 7월 CEO Lawson Whiting이 후임이 정해지면 은퇴한다고 발표했다. '
              '회사는 2027 회계연도 유기 매출을 대체로 제자리, 유기 영업이익을 3~5% 감소로 내다본다 — 소비 둔화와 선진국 주류 소비 감소가 부담이고, 구조조정·미국 유통사 변경·신제품(Jack Daniel’s Tennessee Blackberry)은 도움이 된다고 봤다. 기타 브랜드 매출이 크게 준 것은 Korbel 유통 계약이 끝나고 Gin Mare 판매가 줄었기 때문이고, 캐나다 대부분 주에서 미국산 주류가 매장 진열대에서 빠진 것도 즉석 음료·선진국 매출을 깎았다. 9월에 채권 $500M을 발행해 분기 말 뒤 차입금이 늘었을 수 있다. '
              '보통주는 의결권 있는 A주(BFA)와 의결권 없는 B주(BFB)가 있고, 시가총액·주당 값은 두 종류를 합친 주식 수로 계산한다. 분기 배당은 주당 $0.2310이다(2026년 5월·7월 선언). 동종업 점수는 S&P500 필수소비재 기준이다.')
PH = ['STZ', 'TAP', 'KO', 'PEP', 'MNST', 'PM']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '음료·주류 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(BFB 제외)와 배수 순위를 매긴 값이다.',
            '식품·생활용품·유통이 섞여 있다. 차트에는 음료·주류 6곳만 보인다.')
# 매출(Q1 FY27 10-Q 주석 9 제품별): 위스키 658 + 즉석 음료 154 + 데킬라 54 + 기타 브랜드 39 + 비브랜드·벌크 6 = 911.
SEG = [('위스키(Jack Daniel’s 등)', 658.0, '#5a1f1f'), ('즉석 음료(RTD)', 154.0, '#c8a24a'), ('데킬라', 54.0, '#a46a5b'),
       ('기타 브랜드', 39.0, '#ead9d0'), ('비브랜드·벌크(중고 오크통 판매 등)', 6.0, '#c9c9c9')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품별'
# 손 뉴스: 실적 3건 + Pernod Ricard 2건 + CEO 은퇴 + CFO 선임. 최신 Q1 FY27(09-02 장 전)은 news_auto가 붙인다. 반응일: 장 마감 뒤 → 다음 날.
NEWS_RANGE = '2026.03 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 21일 장 마감 뒤 — 채권 $500M 발행', '2026-09-22',
     '2031년 만기 5.375% 채권 $500M — 일반 용도·기업어음 상환 등 — 다음 날 주가 +1.6%', 'notes', 'Brown-Forman 공시 (SEC 8-K)'),
    ('neutral', '2026년 7월 13일 장 마감 뒤 — CEO 은퇴 발표', '2026-07-14',
     'Lawson Whiting CEO가 후임이 정해지면 은퇴 · 내·외부 후보 탐색 · 2027 회계연도 전망 유지 — 다음 날 주가 −4.4%', 'ceo', 'Brown-Forman 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 6월 4일 장 전 — Q4 FY26 실적', '2026-06-04',
     '분기 매출 $912M(+2%) · 영업이익 $96M(−53%, 브랜드 손상 포함) · 희석 EPS $0.12(−62%) · 연간 EPS $1.53(−17%) · 2027 회계연도 전망 첫 제시 — 그날 주가 +2.8%', 'q4', 'Brown-Forman 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 28일 장 마감 뒤 — Pernod Ricard와 결합 논의 종료', '2026-04-29',
     '조건이 맞지 않아 논의를 끝냄 — 다음 날 주가 −10.3%', 'pr2', 'Brown-Forman 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 26일 장 마감 뒤 — Pernod Ricard와 결합 논의 확인', '2026-03-27',
     '시장 소문에 대해 합병에 가까운 결합을 논의 중이라고 확인(소문이 돈 당일 이미 +9.6%) — 다음 날 주가 +5.6%', 'pr1', 'Brown-Forman 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 16일 장 전 — 새 CFO 선임', '2026-03-16',
     'Whirlpool 출신 Jim Peters를 3월 31일부터 CFO로 — 그날 주가 −1.7%', 'cfo', 'Brown-Forman 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 4일 장 전 — Q3 FY26 실적', '2026-03-04',
     '매출 $1.1B(+2%) · 영업이익 $340M(+21%) · 희석 EPS $0.58(+1%) — 그날 주가 −6.6%', 'q3', 'Brown-Forman 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 18, 'nt': 9, 'mean': 26.67, 'median': 27, 'low': 23, 'high': 29, 'sb': 1, 'b': 0, 'h': 13, 's': 2, 'ss': 2}
ANALYST_ASOF = '2026-11-07'


# ── 자동 카드 — 제품별 매출 지도(seg_map_propose 전부 맞음). 원문 대조: Q1 FY27 10-Q 주석 9 658/154/54/39/6 = 911(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"bfb:WhiskeyMember": ["위스키(Jack Daniel’s 등)", "#5a1f1f"], "bfb:ReadyToDrinkMember": ["즉석 음료(RTD)", "#c8a24a"], "bfb:TequilaMember": ["데킬라", "#a46a5b"], "bfb:RestofportfolioMember": ["기타 브랜드", "#ead9d0"], "bfb:NonbrandedandbulkMember": ["비브랜드·벌크(중고 오크통 판매 등)", "#c9c9c9"]},
 "ignore": []
}
