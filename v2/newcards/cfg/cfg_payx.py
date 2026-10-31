# PAYX(페이첵스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 5월 31일(FY2027 = 2026-06~2027-05). 카드 순위 196. 중소기업 급여·인사 아웃소싱, PEO·보험.
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-09-25T00:06Z), 실적 보도자료(Q2 FY26~Q1 FY27, 8-K 2.02항 — 장 전 발표, 9:30 콜, 8-K 장중 접수), StockAnalysis. 사전 조사 자료표 scratchpad pre/PAYX.md.
# 엔진 입력(2026-10-24): 매출 = Revenues(고객 자금 이자 포함, Q1 FY27 $1,630.5M), 차입금 $4,558M(사채 — 2025-04 Paycor 인수 자금), 현금 $601M + 회사 투자 $333M. 고객 자금(funds held for clients)과 고객 자금 채무는 현금·차입금에서 뺀다(엔진 기본 태그에 안 잡힘).
# 4분기 EPS FY2025 보도자료 값(0.82 — Paycor 인수 비용으로 낮음). companyfacts에 DEF 14A 순이익 중복(FY2024 1,690달러)이 있으나 엔진은 10-K·10-Q만 쓴다.
CIK = '0000723531'
CUR, YO, QO = '2026-08-31', '2025-08-31', '2026-05-31'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-05-31', '2025-05-31'), 'FY2026'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Paychex'
S_ = 'https://www.sec.gov/Archives/edgar/data/723531/'
SEC = S_
TENQ = S_ + '000072353126000006/payx-20260831.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000072353126000004/payx-ex99_1.htm', 'q4': S_ + '000119312526280314/payx-ex99_1.htm', 'q3': S_ + '000119312526122887/payx-ex99_1.htm',
      'q2': S_ + '000119312525325838/payx-ex99_1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="payxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (20, 45)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('2025년 4월 Paycor를 인수해 매출이 한 단계 커졌고, 인수 무형자산 상각과 통합 비용 때문에 GAAP 이익이 회사가 발표하는 조정 이익보다 작다. 인수 자금으로 사채를 크게 발행해 차입금이 늘었다. '
              '매출에는 고객에게서 받아 둔 급여 자금의 이자 수익이 들어 있어 금리에 따라 움직인다. 그 고객 자금과 관련 지급 의무는 회사 현금·차입금으로 보지 않는다(재무건전성의 유동비율에는 고객 자금과 관련 지급 의무가, 부채비율에는 관련 지급 의무가 들어 있다). 회계연도 3분기(12~2월)가 계절적으로 가장 크다. '
              '자기 이력 점수는 5년 동안 높은 배수를 받아 온 이 종목 안에서 지금 배수가 낮은 편이라는 뜻이고, 현금흐름 모델은 그 높은 배수 자체를 인정하지 않는다 — 5년 뒤에는 낮은 장기 성장률과 적용 할인율로 잔존가치를 잡아 지금 시장 배수보다 훨씬 낮은 배수가 된다. 그래서 두 판정은 같은 질문이 아니다. 기본값이 낮은 또 다른 이유는 Paycor 영업권이 든 투하자본 대비 매출이 낮아, 성장에 필요한 재투자가 크게 잡히기 때문이다.')
PH = ['ADP', 'CTAS', 'GWW', 'FAST', 'WM', 'RSG']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '산업 서비스 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(PAYX 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·건설·사업 서비스가 섞여 있다. 차트에는 산업 서비스 6곳만 보인다.')
# 매출(Q1 FY27 10-Q) — 관리 솔루션 1,213.1 + PEO·보험 367.6 = 1,580.7, 고객 자금 이자 49.8 → 1,630.5. 단일 부문.
SEG = [('관리 솔루션(급여·인사)', 1213.1, '#0055a5'), ('PEO·보험', 367.6, '#5fa0dc')]
SEG_ADJ = 49.8
SEG_ADJ_LABEL = '고객 자금 이자'
SEG_TITLE = '매출 구성 — 서비스별'
# 손 뉴스: 4건(최신 Q1 FY27도 손으로 — news_auto에 PAYX 항목이 없었다, Codex·Fable r1 필수)(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다). 반응일: 보도자료 장 전(9:30 콜) → 같은 날.
# 넣지 않은 8-K: 이사·임원, 주총.
NEWS_RANGE = '2025.12 ~ 2026.09'
NEWS = [
    ('red', '2026년 9월 23일 — Q1 FY27 실적', '2026-09-23',
     '매출 $1.63B(+6%) · 순이익 $430M · 희석 EPS $1.21(1년 전 $1.06) · 분기 FCF는 운전자본 시점 차로 1년 전보다 줄었다 — 발표 날 주가 −9%', 'q1', 'Paychex 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 6월 24일 — Q4 FY26 실적', '2026-06-24',
     '매출 $1.61B · 순이익 $421M · 희석 EPS $1.17(1년 전 $0.82 — Paycor 인수 비용) · 2026 회계연도 희석 EPS $4.89', 'q4', 'Paychex 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 25일 — Q3 FY26 실적', '2026-03-25',
     '매출 $1.81B · 순이익 $560M · 희석 EPS $1.56(1년 전 $1.43)', 'q3', 'Paychex 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 19일 — Q2 FY26 실적', '2025-12-19',
     '매출 $1.56B · 순이익 $395M · 희석 EPS $1.10(1년 전 $1.14)', 'q2', 'Paychex 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 19, 'nt': 13, 'mean': 116.38, 'median': 112, 'low': 96, 'high': 150, 'sb': 2, 'b': 0, 'h': 15, 's': 0, 'ss': 2}
ANALYST_ASOF = '2026-10-31'


# ── 자동 카드 — 서비스 2개(수동 지도, 제품·서비스 축), 고객 자금 이자는 SEG_ADJ. 원문 대조: Q1 FY27 1,213.1/367.6/49.8(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"payx:ManagementSolutionsMember": ["관리 솔루션(급여·인사)", "#0055a5"], "payx:PeoAndInsuranceSolutionsMember": ["PEO·보험", "#5fa0dc"]},
 "ignore": []
}
