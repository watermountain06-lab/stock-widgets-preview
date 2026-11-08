# ODFL(올드 도미니언 프레이트 라인) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 미국 소량화물(LTL) 트럭 운송, 단일 부문.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/ODFL.md.
# 엔진 입력(2026-10-24): 매출 = RevenueFromContractWithCustomerIncludingAssessedTax(엔진 기본), 차입금 $20.0M(1년 안 사채), 현금 $283.9M. 분할 2020(3:2)·2024(2:1)은 KNOWN_SPLITS.
# 일회성: Q2 2026 설비 처분 이익 $17.2M(최근 4분기 EPS의 약 1%)뿐. Q3 2026 실적 10/28 장 전 발표 예정(회사 공지).
CIK = '0000878927'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Old Dominion'
S_ = 'https://www.sec.gov/Archives/edgar/data/878927/'
SEC = S_
TENQ = S_ + '000087892726000023/odfl-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000087892726000021/odfl-ex99_1.htm', 'q1': S_ + '000087892726000009/odfl-ex99_1.htm',
      'q4': S_ + '000119312526036791/odfl-ex99_1.htm', 'q3': S_ + '000119312525255040/odfl-ex99_1.htm'}
LINKS = {}
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-28', 'src': '9/30 회사 공지 — 장 시작 전 발표, 콜 오전 10시(동부)'}
FAIRBAND_TITLE = 'id="odflFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (15, 35)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('2023년부터 화물 물동량이 줄어든 가운데 Q2 2026에는 물동량 감소가 완화되고 단가·수익성이 개선됐다(톤수는 아직 1년 전보다 적다) — 회복이 이어지면 최근 4분기 이익이 앞으로를 낮게 볼 수 있다. '
              '과거 5년 이익률 중앙값은 호황기(2021~2022)가 섞여 높다. 화물 경기에 따라 이익 변동이 크다. '
              '설비투자는 남는 터미널 용량을 쓰며 줄였다가 2026년 계획을 다시 늘렸다 — 이 모델은 설비투자를 그대로 빼지 않고 매출 대비 투하자본으로 재투자를 추정한다.')
PH = ['UNP', 'CSX', 'UPS', 'JBHT', 'CHRW', 'EXPD']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '운송 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '운송 PBR 비교', 'psr': '운송 PSR 비교',
                'pcr': '운송 PCR(FCF) 비교', 'evebitda': '운송 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(ODFL 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 운송 6곳만 보인다.')
# 매출(Q2 2026 10-Q, 단일 부문) — LTL 운송 1,538.9 + 기타 15.1 = 1,554.0.
SEG = [('LTL 운송', 1538.9, '#00703c'), ('기타 서비스', 15.1, '#9fd3b4')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 서비스별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표 → 같은 날. 넣지 않은 8-K: 월간 운영 지표(7.01), 배당(8.01), 이사 사임·은퇴, 주총.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('green', '2026년 7월 29일 — Q2 2026 실적', '2026-07-29',
     '매출 $1.55B(+10.4%) · 순이익 $351M · 희석 EPS $1.68(1년 전 $1.27) · 영업비율(OR) 70.1% — 설비 처분 이익 $17.2M 포함', 'q2', 'Old Dominion 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 29일 — Q1 2026 실적', '2026-04-29',
     '매출 $1.33B · 순이익 $238M · 희석 EPS $1.14(1년 전 $1.19)', 'q1', 'Old Dominion 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 4일 — Q4 2025 실적', '2026-02-04',
     '매출 $1.31B · 순이익 $230M · 희석 EPS $1.09(1년 전 $1.23) · 2025년 희석 EPS $4.84(1년 전 $5.48)', 'q4', 'Old Dominion 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 29일 — Q3 2025 실적', '2025-10-29',
     '매출 $1.41B · 순이익 $271M · 희석 EPS $1.28(1년 전 $1.43)', 'q3', 'Old Dominion 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 18, 'mean': 223.17, 'median': 223, 'low': 194, 'high': 280, 'sb': 9, 'b': 1, 'h': 13, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 서비스 2개(수동 지도). 원문 대조: Q2 2026 1,538.9/15.1(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"odfl:LTLServiceRevenueMember": ["LTL 운송", "#00703c"], "odfl:OtherServiceRevenueMember": ["기타 서비스", "#9fd3b4"]},
 "ignore": []
}
