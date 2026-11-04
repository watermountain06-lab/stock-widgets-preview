BUILD = {}
# NCLH(노르웨이전 크루즈 라인) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 크루즈 — Norwegian·Oceania·Regent Seven Seas, 단일 보고 부문(버뮤다 법인, 법인세 거의 없음).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-29 장 마감 뒤), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 06:45~07:00 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/NCLH.md.
# 엔진 입력(2026-11-04): 차입금 = 대차대조표 비유동 $13,951.5M + 유동 $1,135.0M = $15,086.5M(DEBT_TOTAL_TAG — 원금 상환표 합계 $15,498M은 안 씀). 현금 $256.5M, 운용리스 $940.3M, 낡은 단기투자·비지배지분 제외.
# 코로나 운항 중단(FY20~FY22 적자): 자기 이력은 첫 흑자 해 FY2023 10-K(2024-02-28)부터(HISTORY_START), 현금흐름 성장은 2023-12-31 합부터(HISTORY_WINDOW). Q4 2023~2025 EPS 보도자료 값(교환사채 희석). 세율은 STATUTORY_TAX 1%(버뮤다, TTM 세금 음수라 21%로 떨어졌다 — Codex r1).
# 일회성: IT 소프트웨어 상각 $95M·구조조정·자문료와 유로 차입금 환산 이익 $88M이 거의 상쇄(순 약 +0.10/주, 5%). 빼도 동종업 PER 순위 2위로 점수 69.2 그대로.
CIK = '0001513761'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Norwegian Cruise Line'
S_ = 'https://www.sec.gov/Archives/edgar/data/1513761/'
SEC = S_
TENQ = S_ + '000110465926120217/nclh-20260930x10q.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000117184326006957/exh_991.htm', 'q2': S_ + '000117184326005050/exh_991.htm', 'q1': S_ + '000117184326002957/exh_991.htm', 'q4': S_ + '000117184326001220/exh_991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="nclhFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('현금흐름 내재가치가 마이너스다 — 영업이익 $1.4B에 비해 순차입금이 $14.8B(약 10.5배)라, 10% 할인율로 사업 가치를 매기면 빚을 갚고 주주 몫이 남지 않는다(할인율 8%면 약 +$9). 새 배 건조 투자로 최근 잉여현금흐름도 적자다. 배수로는 싸 보이지만(PER 9.6배) 빚이 판정을 끌어내린다. 내재가치가 마이너스라 머리말의 요구 성장률(음수)은 투자를 회수한다는 계산상의 값일 뿐 의미가 없다. '
              '코로나로 2020~2022년 적자라 자기 이력은 2024년 2월부터 비교한다. 분기 이익은 유로 차입금 환산 손익으로 흔들린다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['RCL', 'CCL', 'BKNG', 'EXPE', 'MAR', 'HLT']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '크루즈·여행 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(NCLH 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 크루즈·여행 6곳만 보인다.')
# 매출(Q3 2026 10-Q 상품 축) — 승객 티켓 1,945.6 + 선내·기타 1,001.1 = 2,946.8(연결과 일치, 비용 태그의 같은 멤버는 개념으로 걸러짐).
SEG = [('승객 티켓', 1945.6, '#003a70'), ('선내·기타', 1001.1, '#00a0df')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 티켓·선내(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:45~07:00 동부) → 같은 날.
NEWS_RANGE = '2026.03 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 29일 장 전 — Q3 2026 실적', '2026-10-29',
     '매출 $2.95B(+0.3%) · 순이익 $492M · 희석 EPS $1.07(1년 전 $0.86, 전년 채무 소멸 손실 기저) · 영업이익 −16.7% · 조정 EPS $1.12(1년 전 $1.20) · CFO 교체 — 당일 주가 +13.4%', 'q3', 'Norwegian Cruise Line 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 30일 장 전 — Q2 2026 실적', '2026-07-30',
     '매출 $2.64B(+4.9%) · 순이익 $223M · 희석 EPS $0.48(1년 전 $0.07) — 당일 주가 −9.8%', 'q2', 'Norwegian Cruise Line 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 4일 장 전 — Q1 2026 실적', '2026-05-04',
     '매출 $2.33B(+9.6%) · 순이익 $105M · 희석 EPS $0.23(1년 전 −$0.09) — 당일 주가 −8.6%', 'q1', 'Norwegian Cruise Line 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 2일 장 전 — Q4 2025 실적', '2026-03-02',
     '매출 $2.24B(+6.4%) · 순이익 $14M · 희석 EPS $0.03(IT 상각 $95M 포함, 1년 전 $0.52) · FY2025 매출 $9.83B — 당일 주가 −10.5%', 'q4', 'Norwegian Cruise Line 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 26, 'nt': 18, 'mean': 18.78, 'median': 19, 'low': 13, 'high': 24, 'sb': 9, 'b': 1, 'h': 15, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-04'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 1,945.6/1,001.1(2026-11-04) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"us-gaap:PassengerMember": ["승객 티켓", "#003a70"], "nclh:OnboardAndOtherMember": ["선내·기타", "#00a0df"]},
 "ignore": []
}
