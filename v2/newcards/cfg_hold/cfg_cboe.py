# CBOE(Cboe 글로벌 마켓) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 198. 옵션 거래소(SPX·VIX 독점), 미국·유럽 주식·선물·외환 거래소.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-31T16:15Z), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표, 8:30 콜, 8-K 장중 접수), 8-K(구조조정 2.05 5/1, S&P 라이선스 9/29), StockAnalysis. 사전 조사 자료표 scratchpad pre/CBOE.md.
# 영업현금흐름은 청산소 담보금 유출입을 뺀 값(안건 E57 OCF_NETTING — 회사 고유 태그를 BUILD company_tags로 overlay에 싣는다). 운전자본에 매각 예정 자산·부채가 섞이는 것(E46)은 그대로 — MODEL_NOTE.
# 엔진 입력(2026-10-24): 설비투자 = PaymentsToAcquireProductiveAssets(2026 2분기부터, EXTRA_TAGS — EQIX와 같은 경우), 4분기 EPS 2021·2022·2024 보도자료 값.
# 매출은 총매출(유동성 리베이트·Section 31 통과 수수료 포함) — 순매출(Q2 2026 $731.6M)이 회사 기준. 청산 담보금·디폴트 펀드 $2.5B는 자산·부채 양쪽에 있어 현금·차입금에서 뺀다. 호주·캐나다 사업은 TMX에 약 $300M 매각 예정(중단사업 아님).
BUILD = {'company_tags': [('cboe:IncreaseDecreaseInRestrictedCashClearingFund', 'IncreaseDecreaseInRestrictedCashClearingFundCboe')]}
CIK = '0001374310'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, None, -2), '고평가'
CO = 'Cboe'
S_ = 'https://www.sec.gov/Archives/edgar/data/1374310/'
SEC = S_
TENQ = S_ + '000162828026051239/cboe-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000162828026051217/cboe-20260731xex991.htm', 'q1': S_ + '000162828026029103/cboe-20260501xex991.htm',
      'q4': S_ + '000162828026005944/cboe-20260206xex991.htm', 'q3': S_ + '000162828025047668/cboe-20251031xex991.htm'}
LINKS = {'sp': S_ + '000110465926111989/tm2626203d1_8k.htm'}
FAIRBAND_TITLE = 'id="cboeFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (20, 45)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('매출은 총매출(유동성 리베이트·통과 수수료 포함)이라 회사가 앞세우는 순매출 기준보다 영업이익률·PSR이 낮게 보인다. '
              '옵션 거래량, 특히 S&P500 지수 옵션(SPX)과 VIX가 이익의 중심이고, S&P와의 독점 사용 계약이 2051년까지 연장됐다(새 사용료는 2027년부터). '
              '호주·캐나다 사업 매각과 일본 철수, 인력 감축 같은 구조 재편이 진행 중이라 분기마다 구조조정·손상 비용이 섞인다. 최근 4분기는 GAAP EPS와 회사 조정 EPS의 차이가 작다. '
              '영업현금흐름·FCF·PCR은 청산소(Cboe Clear Europe) 회원 담보금·디폴트 펀드 유출입을 뺀 값이다. '
              '매각 예정인 호주·캐나다 사업의 자산·부채(현금·영업권 포함)가 유동 항목으로 옮겨져 현금흐름 모델의 운전자본에 섞여 있다 — 값을 조금 낮추는 쪽이다(순액만 빼 본 민감도 계산으로 기본 값이 약 4% 높아지는 정도 — 확정 보정값은 아니다).')
HEALTH_EXTRA = '청산 회원 담보금·디폴트 펀드는 같은 금액이 자산과 부채에 함께 있어 유동비율을 100% 쪽으로 끌어당기고 부채비율을 키운다 — 회사 현금·차입금으로 보지 않는다.'   # 고정 문장(NDAQ와 같은 처리, 2026-10-24)
# 표시 보정(Fable·Codex r2 권장) — FCF의 영업현금흐름은 담보금 흐름을 뺀 값, 분기 차트 매출은 총매출
POST = [r'''
h = h.replace('<div class="stat-sub">영업현금흐름 − 설비투자</div>', '<div class="stat-sub">영업현금흐름(청산 담보금 흐름 제외) − 설비투자</div>')
h = h.replace('FCF는 영업현금흐름 − 설비투자 ·', 'FCF는 영업현금흐름(청산 담보금 흐름 제외) − 설비투자 · 매출은 총매출 ·')
h = h.replace('<div class="card-title">분기 매출 / 순이익 / 영업이익률 (Q3 2024~Q2 2026)</div>', '<div class="card-title">분기 총매출 / 순이익 / 영업이익률 (Q3 2024~Q2 2026)</div>', 1)
''']
PH = ['ICE', 'CME', 'NDAQ', 'SPGI', 'MCO', 'MSCI']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '거래소·금융 데이터 6곳 PER 비교', 'pbr': '거래소·금융 데이터 PBR 비교', 'psr': '거래소·금융 데이터 PSR 비교',
                'pcr': '거래소·금융 데이터 PCR(FCF) 비교', 'evebitda': '거래소·금융 데이터 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 결제·거래소 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 결제·거래소 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('S&P500 결제·거래소·금융 데이터(CBOE 제외)와 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 처리·거래소·신용평가·지수 회사가 섞여 있다. 비교할 값이 있는 회사가 적은 배수는 빠진다. 차트에는 거래소·금융 데이터 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 총매출) — 옵션 743.1 + 북미 주식 520.0 + 유럽·아시아태평양 117.8 + 선물 33.4 + 외환 28.5 = 1,442.8(= 총매출). 순매출 473.9·114.7·84.8·30.6·27.6.
SEG = [('옵션', 743.1, '#00a3e0'), ('북미 주식', 520.0, '#7fd0ef'), ('유럽·아시아태평양', 117.8, '#00628a'), ('선물', 33.4, '#9bb7c4'), ('외환', 28.5, '#c9dbe3')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(총매출)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다) + S&P 라이선스. 반응일: 보도자료 장 전 → 같은 날, S&P 라이선스는 9/29 오전 8시 15분(동부) 회사 발표(8-K는 그날 밤 접수) → 9/29(Codex r1).
# 넣지 않은 8-K: 신용 한도(6/26·7/28), COO 은퇴(1/26), 주총(5/18). 구조조정 2단계(5/1 2.05)는 Q1 실적 항목에.
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('green', '2026년 9월 29일 — S&P와 지수 옵션 독점 사용 계약 2051년까지 연장', '2026-09-29',
     'SPX 옵션·VIX 관련 지수 독점 사용 — 새 계약당 사용료는 2027년부터(매출원가 변화)', 'sp', 'Cboe 공시 (SEC 8-K)'),
    ('green', '2026년 7월 31일 — Q2 2026 실적', '2026-07-31',
     '총매출 $1.44B(순매출 $732M) · 순이익 $352M · 희석 EPS $3.35(1년 전 $2.23) — 구조조정(인력 감축) 비용 $23.7M 포함', 'q2', 'Cboe 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 1일 — Q1 2026 실적 · 구조 재편 2단계', '2026-05-01',
     '총매출 $1.27B(순매출 $729M) · 순이익 $384M · 희석 EPS $3.66(1년 전 $2.37) · 2~4분기 구조조정 비용 $36~46M 예상(8-K 2.05)', 'q1', 'Cboe 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 6일 — Q4 2025 실적', '2026-02-06',
     '총매출 $1.20B(순매출 $671M) · 순이익 $312M · 희석 EPS $2.97(1년 전 $1.86) — 손상 $25.1M 포함', 'q4', 'Cboe 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 31일 — Q3 2025 실적 · 호주·캐나다 매각 추진', '2025-10-31',
     '총매출 $1.14B(순매출 $606M) · 순이익 $299M · 희석 EPS $2.85(1년 전 $2.07) — 투자 평가이익 $52.7M 포함', 'q3', 'Cboe 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 18, 'nt': 13, 'mean': 326.85, 'median': 320, 'low': 288, 'high': 380, 'sb': 2, 'b': 3, 'h': 12, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-24'


# ── 자동 카드 — 부문 5개(수동 지도, 총매출). 원문 대조: Q2 2026 743.1/520.0/117.8/33.4/28.5(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax", "us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"cboe:OptionsMember": ["옵션", "#00a3e0"], "cboe:NorthAmericanEquitiesMember": ["북미 주식", "#7fd0ef"], "cboe:EuropeAndAsiaPacificMember": ["유럽·아시아태평양", "#00628a"],
             "cboe:FuturesMember": ["선물", "#9bb7c4"], "cboe:GlobalFXMember": ["외환", "#c9dbe3"]},
 "ignore": []
}
