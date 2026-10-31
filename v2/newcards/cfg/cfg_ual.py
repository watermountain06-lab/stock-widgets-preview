# UAL(유나이티드 항공 홀딩스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 항공(국제선·국내선), 화물, 마일리지 제휴. United Airlines, Inc.와 결합 공시.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-21), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/UAL.md.
# 엔진 입력(2026-10-25): 차입금 = 1년 안 $1,848M + 장기 $24,550M(금융리스 포함) = $26,398M(DEBT_TOTAL_TAG), 현금 $6,648M + 단기투자 $8,005M, 운용리스 별도.
# 일회성: 특별 항목(주로 항공기 판매 후 리스 이익) 최근 4분기 순 이익 $757M — GAAP 영업이익을 약 18%, GAAP EPS를 회사 조정 EPS보다 약 24% 높인다(빼는 장치는 E54 보류). 판정이 이 때문에 바뀌는지 검토에서 확인.
CIK = '0000100517'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, 1), '적정~저평가'
CO = 'United'
S_ = 'https://www.sec.gov/Archives/edgar/data/100517/'
SEC = S_
TENQ = S_ + '000010051726000186/ual-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000010051726000184/ual_erx09302026xex991.htm', 'q2': S_ + '000010051726000135/ual_erx06302026xex991.htm',
      'q1': S_ + '000010051726000089/ual_erx03312026xex991.htm', 'q4': S_ + '000010051726000014/ual_12312025erex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ualFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-20, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 GAAP 이익에는 항공기 판매 후 리스 이익 같은 영업 특별 항목(순이익 쪽)이 커서 영업이익이 약 18%, EPS가 회사 조정 EPS보다 약 24% 높다 — PER은 그만큼 싸게 보인다. 이 항목을 빼고 다시 계산해도 세 칸의 표는 같다(Codex·Fable 재계산). '
              '기본 시나리오의 5년 성장률은 코로나 뒤 회복기가 들어 있어 높게 잡힌다. '
              '5년 이력 앞부분에는 코로나 적자가 있어 자기 이력 비교의 의미가 제한된다. 연료비 급등과 운용리스·차입금이 큰 구조라 경기·유가에 이익이 크게 흔들린다.')
PH = ['DAL', 'UNP', 'CSX', 'UPS', 'GE', 'BA']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '항공·운송·항공우주 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(UAL 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 항공·운송·항공우주 6곳만 보인다.')
# 매출(Q3 2026 10-Q, 단일 부문) — 여객 16,241 + 화물 529 + 기타(마일리지 제휴 등) 1,106 = 17,876(손익계산서 17,875, 반올림).
SEG = [('여객', 16241.0, '#005daa'), ('기타(마일리지 제휴 등)', 1106.0, '#5c9ad6'), ('화물', 529.0, '#a9c8ea')]
SEG_ADJ = -1
SEG_LABEL_ADJ = '반올림'
SEG_TITLE = '매출 구성 — 종류별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다). 반응일: 장 마감 뒤 발표 → 다음 거래일.
# 넣지 않은 8-K: 사채 발행(2026-02), American 합병 접촉 발언(4/27 7.01 — 거래 없음), 주총.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 20일 — Q3 2026 실적', '2026-10-21',
     '매출 $17.9B(1년 전 $15.2B) · 순이익 $1.03B · 희석 EPS $3.14(1년 전 $2.90) — 특별 항목(순이익 쪽) 세전 $215M 포함', 'q3', 'United 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 15일 — Q2 2026 실적', '2026-07-16',
     '매출 $17.7B · 순이익 $805M · 희석 EPS $2.46(1년 전 $2.97) — 특별 항목 세전 $145M 포함 · 연료비 급등', 'q2', 'United 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 21일 — Q1 2026 실적', '2026-04-22',
     '매출 $14.6B · 순이익 $699M · 희석 EPS $2.14(1년 전 $1.16) — 판매 후 리스 이익 등 특별 항목 세전 $389M 포함(조정 EPS $1.19)', 'q1', 'United 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 20일 — Q4 2025 실적', '2026-01-21',
     '매출 $15.4B · 순이익 $1.04B · 희석 EPS $3.19(1년 전 $2.95) · 2025년 희석 EPS $10.20', 'q4', 'United 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 25, 'nt': 16, 'mean': 155.56, 'median': 152, 'low': 125, 'high': 203, 'sb': 19, 'b': 4, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 종류 3개(수동 지도). 원문 대조: Q3 2026 16,241/529/1,106(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"us-gaap:PassengerMember": ["여객", "#005daa"], "us-gaap:ProductAndServiceOtherMember": ["기타(마일리지 제휴 등)", "#5c9ad6"], "us-gaap:CargoAndFreightMember": ["화물", "#a9c8ea"]},
 "ignore": []
}
