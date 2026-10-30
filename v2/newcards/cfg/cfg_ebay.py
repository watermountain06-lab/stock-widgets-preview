BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # 중단사업 잔여 손익이 매 분기 있다(Q3 2026 계속사업 1.11 대 총 1.10, Q3 2025 1.27 대 1.34) — 회사 헤드라인인 계속사업을 쓴다
# EBAY(이베이) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 온라인 마켓플레이스(수집품·자동차 부품·중고·명품 등), 2026-07 Depop 인수. 보고 부문 하나 — 매출 구성은 거래 수수료·광고.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-29 16:08 장 마감 뒤 접수 — 첫 세션 10/30), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 마감 뒤 16:07 동부 → 다음 날 반응), 구조조정 8-K(10/22), StockAnalysis. 사전 조사 scratchpad pre/EBAY.md.
# 엔진 입력(2026-10-30): 차입금 = 1년 안 $1,599M(CP $750M 포함) + 장기 $5,134M = $6,733M(DEBT_TOTAL_TAG — 기본 $5,989M). 희석 EPS는 계속사업 우선(중단사업 잔여 손익이 매 분기 있다).
# 단기투자 $809M은 EV_TAGS_BY_CIK sti(매도가능 채권 만기 1년 안 태그), 장기투자 $2,171M은 회사 고유 태그라 빠짐(더하면 주당 약 $4.9 — 판정 불변). 2026-01 ASU 2025-06 소급 적용으로 2025 분기가 약간 재작성됐다(Q3 2025 1.28 → 1.27).
# 일회성: 최근 4분기 GAAP(계속사업) 4.58 중 구조조정·거래 관련 비용 세후 약 0.29(6.3%), 지분투자·워런트 손익 약 1%.
CIK = '0001065088'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'eBay'
S_ = 'https://www.sec.gov/Archives/edgar/data/1065088/'
SEC = S_
TENQ = S_ + '000106508826000212/ebay-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000106508826000209/exhibit991erebayq32026.htm', 'rs': S_ + '000106508826000205/ebay-20261020.htm', 'q2': S_ + '000106508826000174/exhibit991erebayq22026.htm', 'q1': S_ + '000106508826000092/exhibit991erebayq12026.htm', 'q4': S_ + '000106508826000017/exhibit991erebayq42025.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ebayFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('단기투자 $0.8B는 내재가치에 더했고, 장기투자 $2.2B(매도가능 채권 $1.4B + 지분 $0.8B, Aurelia(옛 Adevinta) $473M 포함)는 회사 고유 태그라 더하지 않았다 — 더하면 주당 약 $4.9다. '
              '자사주를 많이 사(3분기 $689M) 자본이 작아 PBR이 높다. 4분기에 인력 약 9% 감축 구조조정 비용 $130~150M(세전)이 잡힐 예정이다. '
              '가격은 10/30 장중 값이다(Q3 10-Q가 10/29 장 마감 뒤 접수). 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['AMZN', 'ABNB', 'BKNG', 'EXPE', 'DASH', 'CVNA']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '인터넷 상거래·플랫폼 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(EBAY 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 인터넷 상거래·플랫폼 6곳만 보인다.')
# 매출(Q3 2026 10-Q 매출 유형) — 마켓플레이스 2,599 + 광고 607 = 3,206.
SEG = [('마켓플레이스 수수료', 2599, '#0064d2'), ('광고', 607, '#f5af02')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 유형별(Q3 2026)'
# 손 뉴스: 실적 4건 + 구조조정(EPS는 GAAP 희석, 계속사업). 반응일: 장 마감 뒤 발표(16:07 동부) → 다음 날, 구조조정은 장 전 → 당일.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 28일 장 마감 뒤 — Q3 2026 실적', '2026-10-29',
     '매출 $3.21B(+14%) · 순이익 $497M · 계속사업 희석 EPS $1.11(1년 전 $1.27, 세금 이익 포함) · 거래액(GMV) +15% — 다음 날 주가 +2.7%', 'q3', 'eBay 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 10월 20일 — 구조조정 발표', '2026-10-20',
     '인력 약 9% 감축, 세전 비용 $130~150M(대부분 4분기) · 3분기 실적이 이전 전망을 넘을 것이라고 예고(8-K는 10/22 접수) — 당일 주가 +0.6%', 'rs', 'eBay 공시 (SEC 8-K)'),
    ('neutral', '2026년 8월 5일 장 마감 뒤 — Q2 2026 실적', '2026-08-06',
     '매출 $3.13B(+15%) · 순이익 $550M · 희석 EPS $1.21(1년 전 $0.78) · Depop 인수 완료(7/30) — 다음 날 주가 −0.9%', 'q2', 'eBay 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 29일 장 마감 뒤 — Q1 2026 실적', '2026-04-30',
     '매출 $3.09B(+19%) · 순이익 $512M · 희석 EPS $1.12(1년 전 $1.05) — 구조조정·임원 비용 $104M 포함 — 다음 날 주가 −0.3%', 'q1', 'eBay 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 18일 장 마감 뒤 — Q4 2025 실적', '2026-02-19',
     '매출 $2.97B(+15%) · 순이익 $528M · 계속사업 희석 EPS $1.14(1년 전 $1.40) · Depop 인수 발표 — 다음 날 주가 +3.1%', 'q4', 'eBay 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 32, 'nt': 23, 'mean': 127.26, 'median': 133, 'low': 75, 'high': 153, 'sb': 8, 'b': 4, 'h': 18, 's': 0, 'ss': 2}
ANALYST_ASOF = '2026-10-30'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 2,599/607(2026-10-30) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"ebay:MarketplaceRevenuesMember": ["마켓플레이스 수수료", "#0064d2"], "ebay:AdvertisingRevenuesMember": ["광고", "#f5af02"]},
 "ignore": []
}
