BUILD = {}
# DECK(데커스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 3월 31일. 신발 브랜드 — HOKA·UGG·기타(Teva 등). 2024-09 6:1 분할(KNOWN_SPLITS).
# 출처: SEC XBRL, Q2 FY27 10-Q(2026-10-29), 실적 보도자료(Q3 FY26~Q2 FY27, 8-K 2.02항 — 장 마감 뒤 16:0x 동부 → 다음 날 반응), StockAnalysis. 사전 조사 scratchpad pre/DECK.md.
# 엔진 입력(2026-11-03): 세전 태그가 IncomeLossAttributableToParent(PRETAX_TAG_BY_CIK). 차입금 0, 현금 $1,209.7M, 운용리스 $539.5M, 낡은 단기투자(2009)·비지배지분(2012) 제외. Q4 FY22~FY26 EPS 보도자료 값(분할 반영).
# 일회성: Q2 FY27 관세(IEEPA) 환급 주당 +0.28(회사 명시, 최근 4분기 분기 합 7.54의 3.7%, 이익 쪽) — 빼도 표 같음. Q3에도 약 +0.24 예정. FY27 매출 전망 하향(중앙값 −2.9%).
CIK = '0000910521'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q2 FY27', 'Q2 FY26', 'Q1 FY27'
L8 = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27', 'Q2 FY27']
FY_ENDS, FY_LABEL = ('2026-03-31', '2025-03-31'), 'FY2026'
VOTES, VERDICT = (1, 1, 1), '저평가'
CO = 'Deckers'
S_ = 'https://www.sec.gov/Archives/edgar/data/910521/'
SEC = S_
TENQ = S_ + '000162828026068116/deck-20260930.htm'; TENQ_NAME = 'Q2 FY27 10-Q'
PR = {'q2': S_ + '000091052126000028/deckex991pressrelease-9302.htm', 'q1': S_ + '000091052126000015/deckex991pressrelease-6302.htm', 'q4': S_ + '000091052126000007/deckex991pressrelease-3312.htm', 'q3': S_ + '000091052126000002/deckex991pressrelease-1231.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="deckFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('2분기 이익에 관세 환급(주당 $0.28)이 들어 있고 3분기에도 비슷한 환급이 예정돼 있다. 환급을 빼면 회사의 연간 이익 전망은 사실상 낮아졌다. '
              'UGG 매출이 연말 분기(10~12월)에 몰려 분기 값만으로 연환산하면 틀린다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['NKE', 'LULU', 'RL', 'TPR', 'TJX', 'ROST']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '의류·신발 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(DECK 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 의류·신발 6곳만 보인다.')
# 매출(Q2 FY27 10-Q 브랜드 부문) — 786.4 + 677.2 + 17.0 = 1,480.6.
SEG = [('UGG', 786.4, '#c8a165'), ('HOKA', 677.2, '#00a1de'), ('기타(Teva 등)', 17.0, '#8a8d8f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 브랜드별(Q2 FY27)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:0x 동부) → 다음 날.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 22일 장 마감 뒤 — Q2 FY27 실적', '2026-10-23',
     '매출 $1.48B(+3.5%) · 순이익 $313M · 희석 EPS $2.31(1년 전 $1.82, 관세 환급 $0.28 포함) · 연간 매출 전망 하향 — 다음 날 주가 −4.9%', 'q2', 'Deckers 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 23일 장 마감 뒤 — Q1 FY27 실적', '2026-07-24',
     '매출 $1.02B(+5.7%) · 순이익 $130M · 희석 EPS $0.94(1년 전 $0.93) — 다음 날 주가 −0.2%', 'q1', 'Deckers 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 21일 장 마감 뒤 — Q4 FY26 실적', '2026-05-22',
     '매출 $1.12B(+9.6%) · 순이익 $136M · 희석 EPS $0.96(1년 전 $1.00) · FY26 EPS $7.02 · 자사주 $3.5B 추가 — 다음 날 주가 +3.9%', 'q4', 'Deckers 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 29일 장 마감 뒤 — Q3 FY26 실적', '2026-01-30',
     '매출 $1.96B(+7.1%) · 순이익 $481M · 희석 EPS $3.33(1년 전 $3.00) · 연간 전망 상향 — 다음 날 주가 +19.5%', 'q3', 'Deckers 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 27, 'nt': 19, 'mean': 104, 'median': 102, 'low': 70, 'high': 137, 'sb': 7, 'b': 5, 'h': 11, 's': 1, 'ss': 3}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q2 FY27 786.4/677.2/17.0(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"deck:UGGBrandSegmentMember": ["UGG", "#c8a165"], "deck:HokaBrandSegmentMember": ["HOKA", "#00a1de"], "deck:OtherBrandsSegmentMember": ["기타(Teva 등)", "#8a8d8f"]},
 "ignore": []
}
