# NDAQ(나스닥) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 188. 거래소·시장 서비스, 금융 기술(Verafin·Adenza), 자본 접근 플랫폼(데이터·지수·상장).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-22 장 마감 뒤 접수 → 기준일 10/23), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 8-K는 장중 접수(11:18~12:29 ET) — 반응일 = 발표일), StockAnalysis. 사전 조사 자료표 scratchpad pre/NDAQ.md.
# 엔진 입력(2026-10-23): D&A = 현금흐름표 줄(EXCLUDE_TAGS로 10-K 한 해짜리 DDA 태그를 뺌, TTM $657M — 인수 무형자산 상각 포함), 차입금 = 단기(CP) 269 + 장기 8,471 = $8,740M(엔진 값 = 원문), 4분기 EPS 2022·2023·2024 보도자료 값(Q4_EPS_OVERRIDE), 2022-08 3:1 분할.
# 매출은 GAAP 총매출(거래 기반 비용 차감 전) — 회사가 앞세우는 순매출(Q3 2026 $1,481M)보다 크다(ICE 카드와 같은 처리).
CIK = '0001120193'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, None, -2), '적정~고평가'
CO = 'Nasdaq'
S_ = 'https://www.sec.gov/Archives/edgar/data/1120193/'
SEC = S_
TENQ = S_ + '000112019326000020/ndaq-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000112019326000017/earningsrelease3q26ex-991.htm', 'q2': S_ + '000112019326000011/earningsrelease2q26ex-991.htm',
      'q1': S_ + '000119312526171829/d148002dex991.htm', 'q4': S_ + '000119312526028185/d103698dex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ndaqFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 50)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('매출은 GAAP 총매출(거래 기반 비용 차감 전)이라 거래량·리베이트에 따라 크게 움직이는 통과 항목이 들어 있다 — 순매출 기준보다 영업이익률·PSR이 낮게 보이고(Q3 2026 영업이익률 총매출 기준 약 31%, 순매출 기준 약 49%), 성장률도 다르다(Q3 순매출 +13%). '
              '1년 전 분기 매출은 처음 보고한 값이라 회사가 나중에 재분류한 값과 조금 다르다. '
              '현금흐름 내재가치가 낮은 주된 이유는 투하자본 대부분이 인수 영업권·무형자산(약 $20B)이라 매출 1달러를 늘리는 데 2달러 넘는 자본이 든다고 계산되고, 자본수익률이 할인율과 비슷해 성장이 가치를 거의 더하지 못하기 때문이다 — 이익률 문제가 아니다. '
              '시장 서비스 부문 총매출 증가는 거래 기반 비용을 뺀 순매출로 보면 작다(Q3 2026 $309M, 1년 전 $303M). '
              '2023년 Adenza 인수로 금융 기술 사업이 커졌고, 최근 분기 GAAP 이익에는 사업 매각 이익·소송 합의 같은 일회성 항목이 섞여 있다.')
HEALTH_EXTRA = '부채비율에는 청산 회원 담보금(Q3 2026 약 $2.5B, 같은 금액이 자산에도 있다)이 부채로 들어 있어, 빼면 약 107%다.'   # 고정 문장(Fable r1 2026-10-23)
PH = ['ICE', 'CME', 'CBOE', 'SPGI', 'MCO', 'MSCI']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '거래소·금융 데이터 6곳 PER 비교', 'pbr': '거래소·금융 데이터 PBR 비교', 'psr': '거래소·금융 데이터 PSR 비교',
                'pcr': '거래소·금융 데이터 PCR(FCF) 비교', 'evebitda': '거래소·금융 데이터 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 결제·거래소 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 결제·거래소 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('S&P500 결제·거래소·금융 데이터(NDAQ 제외)와 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 처리·거래소·신용평가·지수 회사가 섞여 있다. 차트에는 거래소·금융 데이터 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문, 총매출) — 시장 서비스 1,221 + 자본 접근 641 + 금융 기술 529 = 2,391, 본사(정리·매각 사업) 2 → 2,393. 시장 서비스 순매출은 309.
SEG = [('시장 서비스(총매출)', 1221.0, '#0090ba'), ('자본 접근 플랫폼', 641.0, '#5bb8d6'), ('금융 기술', 529.0, '#005f7a')]
SEG_ADJ = 2.0
SEG_TITLE = '매출 구성 — 부문별(총매출)'
SEG_ADJ_LABEL = '본사(정리·매각 사업)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다). 반응일: 보도자료 발표일(장 전 추정 — 8-K 오전 접수) → 같은 날.
# 넣지 않은 8-K: 채권 공개매수(12/1·12/15), 정관(1/16), 주총(6/16), 신용약정(7/1). 다음 실적: 회사 공지 없음(1월 말 추정).
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 22일 — Q3 2026 실적', '2026-10-22',
     '순매출 $1.48B(총매출 $2.39B) · 순이익 $540M · 희석 EPS $0.96(1년 전 $0.73) — 소송 합의 이익 $16M 포함', 'q3', 'Nasdaq 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 23일 — Q2 2026 실적', '2026-07-23',
     '순매출 $1.50B(총매출 $2.53B) · 순이익 $507M · 희석 EPS $0.89(1년 전 $0.78)', 'q2', 'Nasdaq 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 23일 — Q1 2026 실적', '2026-04-23',
     '순매출 $1.41B · 순이익 $519M · 희석 EPS $0.91(1년 전 $0.68) — 북유럽 전력 선물 사업 이전 이익 $89M 포함', 'q1', 'Nasdaq 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 29일 — Q4 2025 실적', '2026-01-29',
     '순매출 $1.39B · 순이익 $519M · 희석 EPS $0.90(1년 전 $0.61) — 사업 매각 이익 $49M 등 포함', 'q4', 'Nasdaq 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 18, 'nt': 15, 'mean': 116.6, 'median': 118, 'low': 107, 'high': 133, 'sb': 8, 'b': 6, 'h': 3, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 부문 3개(수동 지도, 총매출). 원문 대조: Q3 2026 1,221/641/529(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"ndaq:MarketServicesMember": ["시장 서비스(총매출)", "#0090ba"], "ndaq:CapitalAccessPlatformsMember": ["자본 접근 플랫폼", "#5bb8d6"], "ndaq:FinancialTechnologyMember": ["금융 기술", "#005f7a"]},
 "ignore": []
}
