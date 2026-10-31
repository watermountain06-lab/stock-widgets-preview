# PYPL(페이팔) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 온라인 결제 — PayPal·Venmo·Braintree(가맹점 결제 처리), 후불결제(BNPL)·소액 대출.
# 출처: SEC XBRL(10/27 Q3 2026 10-Q까지 요약 자료에 있음), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 07시 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/PYPL_q3.md.
# 엔진 입력(2026-10-28): 회사 현금 $7,160M + 단기투자 $3,120M(고객 자금 $38.4B와 대응 부채 $40.9B는 회사 현금·차입금이 아니다), 차입금 $13,472M(1년 안 $2,533M 포함), 세전이익 태그가 IncomeLossAttributableToParent(PRETAX_TAG_BY_CIK).
# 일회성: 최근 4분기 GAAP 5.24 대 조정 5.40 — 4분기 세금 이익(주당 약 0.24)과 3분기 구조조정 $178M(인력 감축)이 엇갈려 순 3%(절대값 14.5%).
CIK = '0001633917'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, 1), '저평가'
CO = 'PayPal'
S_ = 'https://www.sec.gov/Archives/edgar/data/1633917/'
SEC = S_
TENQ = S_ + '000163391726000088/pypl-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000163391726000086/pypl3q-26earningsrelease.htm', 'q2': S_ + '000163391726000080/pypl2q-26earningsrelease.htm',
      'q1': S_ + '000163391726000065/pypl1q-26earningsrelease.htm', 'q4': S_ + '000163391726000021/pypl4q-25earningsrelease.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="pyplFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '결제 회사라 재고 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('대차대조표에 고객 자금(현금·채권 $38.4B)과 고객 부채($40.9B)가 함께 있다 — 카드 순현금은 회사 자기 현금·투자만 쓰지만, 부채비율·유동비율에는 고객 부채가 들어가 높게 나온다. 장기투자 $4.8B에는 전략 투자(비상장 지분 $1.7B)가 들어 있다. '
              '자사주를 크게 사서 희석 주식 수가 1년 새 960M에서 858M으로 줄었다. 3분기에 조직 개편 인력 감축 비용($152M)이 영업이익을 눌렀다.')
PH = ['V', 'MA', 'FIS', 'FISV', 'CPAY', 'JKHY']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '결제 6곳 PER 비교 (점수는 결제·거래소 비교군 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '결제·거래소 비교군 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '결제·거래소 비교군 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('결제·거래소 비교군(PYPL 제외)과 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 처리·금융 데이터·거래소가 섞여 있다. 차트에는 결제·결제 처리 6곳만 보인다.')
# 매출(Q3 2026 10-Q, 단일 부문 — 매출 유형) — 거래 수익 7,711 + 기타 부가서비스 873 = 8,584.
SEG = [('거래 수익', 7711, '#003087'), ('기타 부가서비스', 873, '#009cde')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 유형별(단일 부문)'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 27일 장 전 — Q3 2026 실적', '2026-10-27',
     '매출 $8.58B(+2.0%) · 순이익 $1.07B · 희석 EPS $1.25(1년 전 $1.30) — 구조조정 $178M 포함 · 2026년 GAAP EPS 전망 약 $5.07', 'q3', 'PayPal 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 28일 장 전 — Q2 2026 실적', '2026-07-28',
     '매출 $8.68B · 순이익 $1.10B · 희석 EPS $1.25(1년 전 $1.29)', 'q2', 'PayPal 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 5일 장 전 — Q1 2026 실적', '2026-05-05',
     '매출 $8.35B · 순이익 $1.11B · 희석 EPS $1.21(1년 전 $1.29) — 당일 주가 −7.7%', 'q1', 'PayPal 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 3일 장 전 — Q4 2025 실적', '2026-02-03',
     '매출 $8.68B · 순이익 $1.44B · 희석 EPS $1.53(1년 전 $1.11) — 비반복 세금 이익 $223M 포함 · CEO 교체 발표 — 당일 주가 −20.3%', 'q4', 'PayPal 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 43, 'nt': 27, 'mean': 57.67, 'median': 58, 'low': 45, 'high': 70, 'sb': 4, 'b': 3, 'h': 31, 's': 2, 'ss': 3}
ANALYST_ASOF = '2026-10-31'


# ── 자동 카드 — 매출 유형 2개(단일 보고 부문). 원문 대조: Q3 2026 7,711/873(2026-10-28) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"pypl:TransactionRevenuesMember": ["거래 수익", "#003087"], "pypl:RevenuesFromOtherValueAddedServicesMember": ["기타 부가서비스", "#009cde"]},
 "ignore": []
}
