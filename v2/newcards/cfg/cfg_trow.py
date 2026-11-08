BUILD = {}
# TROW(T. 로 프라이스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 자산운용 — 뮤추얼펀드·퇴직연금·OHA 대체투자, 단일 보고 부문.
# 출처: SEC XBRL, Q3 2026 10-Q, 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 07시 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/TROW.md. 비교군 asset_managers(2026-10-25 등록).
# 엔진 입력(2026-11-04): 회사 차입 0(CIP의 CLO 차입은 회사 차입 아님), 현금 $3,774M(회사 몫, CIP 현금 제외). 감가상각은 회사 자체 태그라 엔진이 못 읽어 0(넣어도 기본 $128~132로 거의 같음), 보유 투자자산(이연보상 헤지 빼고 $2.85B)도 0 — 넣으면 기본 약 $148(Codex·Fable r1). 카드 FCF에는 CIP 매매 현금흐름이 섞여 작게 나온다(회사 몫 TTM 약 $2.6B).
# 일회성: Q4 2025 구조조정 $149M(주당 0.49, 비용 쪽), 시장 연동 영업외 손익(회사 투자·CIP 포함)이 분기마다 −$48M~+$369M(Q2 2026 이익 쪽). 일회성을 빼도 자기 75.8~81.1·동종 74.6~78.8로 +1 유지 — GAAP EPS가 영업과 따로 움직인다.
CIK = '0001113169'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, None, 1), '적정~저평가'
CO = 'T. Rowe Price'
S_ = 'https://www.sec.gov/Archives/edgar/data/1113169/'
SEC = S_
TENQ = S_ + '000111316926000005/trow-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000111316926000003/earningsreleaseq32026.htm', 'q2': S_ + '000162828026051211/earningsreleaseq22026.htm', 'q1': S_ + '000162828026028572/earningsreleaseq12026.htm', 'q4': S_ + '000162828026005273/earningsreleaseq42025.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="trowFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('분기 순이익에 펀드 투자·연결 투자상품 손익이 크게 섞여 영업과 따로 움직인다(2분기 영업외 +$369M). 고객 자금은 4분기 연속 순유출(3분기 $28B)이고 매출 증가는 시장 상승 덕이다. '
              '내재가치에는 회사가 들고 있는 투자자산(약 $2.9B)이 빠져 있어 실제보다 낮게 잡힌다(넣으면 기본 약 $148). 잉여현금흐름에는 연결 투자상품의 매매 현금이 섞여 작게 나온다. 비교 종목은 S&P500 자산운용·수탁은행 12곳 중 TROW를 뺀 11곳이다.')
PH = ['BLK', 'BEN', 'IVZ', 'AMP', 'NTRS', 'STT']
PEER_FILE = 'peer_universe/asset_managers.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '자산운용 6곳 PER 비교 (점수는 S&P500 자산운용·수탁은행 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 자산운용·수탁은행 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 자산운용·수탁은행 대비 배수 순위 (v2/peer_universe/asset_managers.json)'
PEER_TIP = ('S&P500 자산운용·수탁은행 12곳 중 TROW를 뺀 11곳과 배수 순위를 매긴 값이다.',
            '전통 운용사·대체투자사·수탁은행이 섞여 있다. 차트에는 6곳만 보인다.')
# 매출(Q3 2026 10-Q) — 단일 부문 순매출 2,004.9.
SEG = [('매출 전체(단일 부문)', 2004.9, '#003b70')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 단일 부문(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07시 동부) → 같은 날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 29일 장 전 — Q3 2026 실적', '2026-10-29',
     '순매출 $2.00B(+5.9%) · 순이익 $612M · 희석 EPS $2.79(1년 전 $2.87) · 조정 EPS $2.86 · 순유출 $28.3B — 당일 주가 +2.5%', 'q3', 'T. Rowe Price 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 31일 장 전 — Q2 2026 실적', '2026-07-31',
     '순매출 $1.91B(+10.7%) · 순이익 $632M · 희석 EPS $2.88(1년 전 $2.24, 투자이익 포함) · 조정 EPS $2.57 — 당일 주가 −6.3%', 'q2', 'T. Rowe Price 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 30일 장 전 — Q1 2026 실적', '2026-04-30',
     '순매출 $1.86B(+5.3%) · 순이익 $498M · 희석 EPS $2.23(1년 전 $2.15) · 조정 EPS $2.52 — 당일 주가 +2.4%', 'q1', 'T. Rowe Price 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 4일 장 전 — Q4 2025 실적', '2026-02-04',
     '순매출 $1.93B(+6.0%) · 순이익 $445M · 희석 EPS $1.99(1년 전 $1.92, 구조조정 $149M 포함) · 조정 EPS $2.44 — 당일 주가 −5.5%', 'q4', 'T. Rowe Price 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 14, 'nt': 12, 'mean': 106, 'median': 109, 'low': 90, 'high': 124, 'sb': 0, 'b': 0, 'h': 10, 's': 3, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 순매출 2,004.9 한 줄(2026-11-04) ──
AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {"us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax": ["매출 전체(단일 부문)", "#003b70"]},
 "ignore": []
}
