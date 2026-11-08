# GRMN(가민) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 마지막 토요일(52/53주, Q3 2026 = 6/28~9/26). GPS·웨어러블 — 피트니스, 아웃도어, 항공, 해양, 자동차 OEM.
# 출처: SEC XBRL(10/28 Q3 2026 10-Q까지 요약 자료에 있음), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 07:00 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/GRMN_q3.md.
# 엔진 입력(2026-10-28): 차입금 없음, 현금 $2,040M + 시장성 증권(유동 $300M·비유동 $1,727M), 감가상각 = 감가상각 + 상각(합산 태그 없음).
# 일회성: 회사 pro forma는 환차손익만 뺀다 — 최근 4분기 순 0.2%. 2026 2·3분기 관세(IEEPA) 환급 약 $54M(주당 약 0.23, 회사 조정 안 함)이 매출원가를 낮췄다.
CIK = '0001121788'
CUR, YO, QO = '2026-09-26', '2025-09-27', '2026-06-27'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-27', '2024-12-28'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Garmin'
S_ = 'https://www.sec.gov/Archives/edgar/data/1121788/'
SEC = S_
TENQ = S_ + '000119312526435070/grmn-20260926.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000119312526435066/grmn-ex99_1.htm', 'q2': S_ + '000119312526322113/grmn-ex99_1.htm',
      'q1': S_ + '000119312526188907/grmn-ex99_1.htm', 'q4': S_ + '000119312526056025/grmn-ex99_1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="grmnFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('차입금이 없고 현금·시장성 증권이 약 $4.1B다. 2026년 2·3분기에 미국 관세(IEEPA) 환급 약 $54M이 매출원가를 낮춰 이익률을 끌어올렸다(회사는 조정하지 않는다) — 빼도 자기 이력 표는 그대로(−1)다. '
              '회계연도가 52/53주라 분기 끝이 토요일이고, 2022년 4분기는 14주였다.')
PH = ['DECK', 'LULU', 'NKE', 'HAS', 'BBY', 'TSLA']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소비재 브랜드·전자 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(GRMN 제외)와 배수 순위를 매긴 값이다.',
            '자동차·소매·외식·여행·소비재가 섞여 있다. 차트에는 소비재 브랜드·전자 소매 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 피트니스 694.3 + 아웃도어 597.3 + 해양 309.9 + 항공 252.7 + 자동차 OEM 131.9 = 1,986.1.
SEG = [('피트니스', 694.3, '#007cc3'), ('아웃도어', 597.3, '#4aa564'), ('해양', 309.9, '#00a6a6'), ('항공', 252.7, '#6d6e71'), ('자동차 OEM', 131.9, '#b5b5b5')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 07:00 발표 → 같은 날. 넣지 않은 8-K: 배당(주총 승인), 임원.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 28일 장 전 — Q3 2026 실적', '2026-10-28',
     '매출 $1.99B(+12.2%) · 순이익 $542M · 희석 EPS $2.80(1년 전 $2.08) · 2026년 pro forma EPS 전망 $10.80으로 올림(이전 $10.00) — 당일 주가 −6.0%', 'q3', 'Garmin 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 29일 장 전 — Q2 2026 실적', '2026-07-29',
     '매출 $2.02B · 순이익 $542M · 희석 EPS $2.80(1년 전 $2.07) — 당일 주가 +16.2%', 'q2', 'Garmin 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 29일 장 전 — Q1 2026 실적', '2026-04-29',
     '매출 $1.75B · 순이익 $405M · 희석 EPS $2.09(1년 전 $1.72)', 'q1', 'Garmin 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 18일 장 전 — Q4 2025 실적', '2026-02-18',
     '매출 $2.13B · 순이익 $529M · 희석 EPS $2.73(1년 전 $2.25) — 당일 주가 +9.4%', 'q4', 'Garmin 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 9, 'nt': 6, 'mean': 302.83, 'median': 310, 'low': 230, 'high': 370, 'sb': 3, 'b': 0, 'h': 5, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 5개. 원문 대조: Q3 2026 694.3/597.3/309.9/252.7/131.9(2026-10-28) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"grmn:FitnessSegmentMember": ["피트니스", "#007cc3"], "grmn:OutdoorSegmentMember": ["아웃도어", "#4aa564"], "grmn:MarineSegmentMember": ["해양", "#00a6a6"],
             "grmn:AviationSegmentMember": ["항공", "#6d6e71"], "grmn:AutoOemSegmentMember": ["자동차 OEM", "#b5b5b5"]},
 "ignore": []
}
