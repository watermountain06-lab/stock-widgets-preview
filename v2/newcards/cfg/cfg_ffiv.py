CIK = '0001048695'
# FFIV(F5) v2 카드 설정 — 자동 카드(AUTO). 회계연도 9월 30일. 애플리케이션 보안·전송(BIG-IP 하드웨어·소프트웨어, NGINX, 분산 클라우드), 2025-09 CalypsoAI·2026-06 SurePath AI 인수. 보고 부문 하나 — 매출 구성은 제품·서비스.
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-08-06), 실적 보도자료(Q1~Q4 FY26, 8-K 2.02항 — 장 마감 뒤 16:0x~16:1x 동부 → 다음 날 반응), StockAnalysis. 사전 조사 scratchpad pre/FFIV.md.
# 카드 재무는 Q3 FY26(6월 분기)까지다 — Q4 FY26 실적(10/27)은 보도자료뿐이고 FY2026 10-K(11월 하순 예상)가 나오면 자동 반영된다(2026-10-30 사용자 결정 "공시 대기만으로 보류하지 않는다").
# 엔진 입력(2026-10-30): 차입금 없음(2025-01 신용한도 만료), 현금 $1,606M, 리스 $252M, 표지 주식 56.6M(8/3). 일회성: 최근 4분기 GAAP 12.53 중 인수 관련·사이버 사고(보험 환급 차감)·시설·구조조정 약 1.20(세전, 9.6%).
CIK = '0001048695'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-09-30', '2024-09-30'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'F5'
S_ = 'https://www.sec.gov/Archives/edgar/data/1048695/'
SEC = S_
TENQ = S_ + '000104869526000067/ffiv-20260630.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q4': S_ + '000104869526000074/ex991-q426earningsreleasef.htm', 'q3': S_ + '000104869526000063/ex991-q326earningsreleasef.htm', 'q2': S_ + '000104869526000042/ex991-q226earningsreleasef.htm', 'q1': S_ + '000104869526000018/ex991-q126earningsreleasef.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ffivFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('카드 재무는 6월 분기까지다. 10/27 발표한 4분기(매출 $917M, +13%, 희석 EPS $3.23)는 FY2026 10-K가 나오면 반영된다 — 발표 다음 날 주가는 −20.4%였다. '
              '2025-10 공시한 국가 배후 해킹(BIG-IP 소스코드 유출)으로 FY26 비용 $28M(보험 환급 $10M)이 들었고 증권 집단소송이 진행 중이다(충당금 없음). '
              '동종업 점수는 카드 유니버스 IT(반도체·소프트웨어·하드웨어) 기준이다.')
PH = ['CSCO', 'ANET', 'PANW', 'CRWD', 'ORCL', 'MSFT']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '네트워크·보안·소프트웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(FFIV 제외)과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 섞여 있다. 차트에는 네트워크·보안·소프트웨어 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 제품·서비스) — 제품 462.8 + 서비스 402.2 = 865.1(반올림).
SEG = [('제품(시스템·소프트웨어)', 462.8, '#e4002b'), ('서비스(유지보수 등)', 402.2, '#1a1a1a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품·서비스'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:0x 동부) → 다음 날.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 27일 장 마감 뒤 — Q4 FY26 실적', '2026-10-28',
     '매출 $917M(+13%) · 순이익 $186M · 희석 EPS $3.23(1년 전 $3.26) · FY2026 EPS $12.52 · FY27 매출 +8~9% 전망 · 자사주 $1.5B 추가 — 다음 날 주가 −20.4%', 'q4', 'F5 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 27일 장 마감 뒤 — Q3 FY26 실적', '2026-07-28',
     '매출 $865M(+11%) · 순이익 $208M · 희석 EPS $3.62(1년 전 $3.25) — 다음 날 주가 −1.1%', 'q3', 'F5 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 28일 장 마감 뒤 — Q2 FY26 실적', '2026-04-29',
     '매출 $812M(+11%) · 순이익 $148M · 희석 EPS $2.58(1년 전 $2.48) — 다음 날 주가 +8.0%', 'q2', 'F5 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 27일 장 마감 뒤 — Q1 FY26 실적', '2026-01-28',
     '매출 $822M(+7%) · 순이익 $180M · 희석 EPS $3.10(1년 전 $2.82) — 사이버 사고 비용 $17M 포함 — 다음 날 주가 +8.1%', 'q1', 'F5 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 13, 'nt': 9, 'mean': 445.78, 'median': 448, 'low': 300, 'high': 540, 'sb': 1, 'b': 3, 'h': 8, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 FY26 462.8/402.2(2026-10-30) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"us-gaap:ProductMember": ["제품(시스템·소프트웨어)", "#e4002b"], "us-gaap:ServiceMember": ["서비스(유지보수 등)", "#1a1a1a"]},
 "ignore": []
}
