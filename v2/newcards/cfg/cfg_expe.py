BUILD = {'cover_shares': True}   # 보통주 + Class B — 표지 주식 수가 클래스별뿐(114.5M + 5.5M = 120.0M)
# EXPE(익스피디아 그룹) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 온라인 여행 — B2C(Expedia·Hotels.com·Vrbo), B2B(여행사·항공사·카드사에 예약 기술 공급), trivago(호텔 가격 비교, 상장 자회사).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05 17:35 장 마감 뒤 수락), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 마감 직후 16:00 동부 → 다음 날 반응), StockAnalysis. 사전 조사 scratchpad pre/EXPE.md.
# 엔진 입력(2026-11-03): 보통주 + Class B — 표지 주식 수가 클래스별뿐이라 BUILD cover_shares(120.02M, 2026-07-24). Q4 2024·2025 EPS는 보도자료 값(Q4_EPS_OVERRIDE). 현금흐름 성장 이력은 2022-12-31 최근 4분기 합부터(HISTORY_WINDOW — 코로나 저점 기저효과 축소).
# 현금 $6,682M(제한 현금 $2,402M 별도, 고객 선수금 $15,426M이 대응), 차입금 $5,459M, 비지배지분 $1,262M(trivago). 인수 현금은 회사 자체 태그(expe:AcquisitionsAndOtherNet)라 엔진이 읽지 못해 0.
# 2026-10-30 사용자 결정(공시 대기만으로 보류하지 않는다) — Q3 2026 실적(11월 초 예상) 전 Q2 기준. 일회성: 최근 4분기 GAAP 16.04 — 지분 평가이익 1.76 대 법적 충당·구조조정·전환옵션 2.36(헤지 등 포함 순 +0.81, 5%, 세금 효과 미반영 근사). 빼도 동종업 55~56으로 표 같음.
# GBTG 지분(2026-06 $702M)은 nonop_extra.json 고정값(Fable 2026-11-03) — 넣기 전 기본 $194.06·비율 1.54.
CIK = '0001324424'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -1), '적정~고평가'
CO = 'Expedia Group'
S_ = 'https://www.sec.gov/Archives/edgar/data/1324424/'
SEC = S_
TENQ = S_ + '000132442426000053/expe-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000132442426000051/earningsrelease-q22026.htm', 'q1': S_ + '000132442426000031/earningsrelease-q12026.htm', 'q4': S_ + '000132442426000005/earningsrelease-q42025.htm', 'q3': S_ + '000132442425000049/earningsrelease-q32025.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="expeFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 연 {pct(HIST[\'growth_5y\'])}, 2022년 말부터)</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '채권 투자·GBTG 지분'
MODEL_NOTE = ('고객이 미리 낸 여행 대금이 $15.4B라 현금 $6.7B에는 이 대금에 대응하는 운영 자금이 섞여 있을 수 있다. 내재가치는 현금을 그대로 더한다. '
              '분기 순이익에 GBTG 지분 평가이익이 크게 섞여 있다(최근 4분기 주당 $1.76). 법적 충당·구조조정·전환옵션 비용(주당 $2.36)과 대부분 상쇄된다(세금 효과 빼고 단순 합). GBTG 지분 $0.7B는 비영업 자산으로 더한다(빼면 현재가 ÷ 내재가치가 1.54로 “매우 비싸다” 쪽으로 넘어가는 경계다). '
              '현금흐름 성장 이력은 코로나 저점 기저효과를 줄이려고 2022년 말 최근 4분기 합부터 잡는다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['BKNG', 'ABNB', 'MAR', 'HLT', 'RCL', 'CCL']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '여행 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(EXPE 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 여행 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 외부 고객 — 축 하나만 붙은 값) — B2C 2,677 + B2B 1,493 + trivago 145 = 4,315(연결과 일치, 부문 간 51은 제외).
SEG = [('B2C', 2677, '#000080'), ('B2B', 1493, '#ffc72c'), ('trivago', 145, '#5b6770')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q2 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 직후 발표(16:00 동부) → 다음 날.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('red', '2026년 8월 5일 장 마감 뒤 — Q2 2026 실적', '2026-08-06',
     '매출 $4.32B(+14%) · 순이익 $878M · 희석 EPS $7.16(1년 전 $2.48, GBTG 평가이익 주당 $2.29 포함) · 조정 EPS $5.76 — 다음 날 주가 −4.1%', 'q2', 'Expedia Group 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 7일 장 마감 뒤 — Q1 2026 실적', '2026-05-08',
     '매출 $3.43B(+15%) · 순손실 $6M · 희석 EPS −$0.05(1년 전 −$1.56) · 조정 EPS $1.96 — 다음 날 주가 −9.0%', 'q1', 'Expedia Group 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 12일 장 마감 뒤 — Q4 2025 실적', '2026-02-13',
     '매출 $3.55B(+11%) · 순이익 $205M · 희석 EPS $1.60(1년 전 $2.20) · FY2025 매출 $14.73B · EPS $9.81 — 다음 날 주가 −6.4%', 'q4', 'Expedia Group 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 6일 장 마감 뒤 — Q3 2025 실적', '2025-11-07',
     '매출 $4.41B(+9%) · 순이익 $959M · 희석 EPS $7.33(1년 전 $5.04) · 조정 EPS $7.57 — 다음 날 주가 +17.5%', 'q3', 'Expedia Group 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 1, 'nt': 1, 'mean': 0, 'median': 0, 'low': 0, 'high': 0, 'sb': 0, 'b': 0, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-03'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q2 2026 2,677/1,493/145(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"expe:B2CMember": ["B2C", "#000080"], "expe:B2BMember": ["B2B", "#ffc72c"], "expe:TrivagoMember": ["trivago", "#5b6770"]},
 "ignore": []
}
