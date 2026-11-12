# CDW(CDW) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 기업·정부·교육 기관에 IT 하드웨어(노트북·서버·저장장치)·소프트웨어·클라우드·서비스를 공급하는 유통·통합 회사.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/CDW.md.
# 엔진 입력(2026-10-25): 기본 경로 — 차입금 = 1년 안 $1,008.9M + 장기 $4,808.1M, 현금 $361.8M. 2026년 9월 발행 사채 $1.5B는 6월 말 재무상태표 뒤라 빠진다(사용처 미공시).
# 일회성 거의 없음. 2026년 부문 재편(상업·정부·교육·기타) — 1년 전 값은 회사가 새 부문으로 다시 낸 값.
CIK = '0001402057'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'CDW'
S_ = 'https://www.sec.gov/Archives/edgar/data/1402057/'
SEC = S_
TENQ = S_ + '000140205726000065/cdw-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000140205726000062/cdw-2026630earningsrelease.htm', 'q1': S_ + '000140205726000023/cdw-2026331earningsrelease.htm',
      'q4': S_ + '000140205726000001/cdw-20251231earningsrelease.htm', 'q3': S_ + '000140205725000191/cdw-2025930earningsrelease.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="cdwFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 10)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('다른 회사 제품을 파는 유통 사업이라 매출은 크고 영업이익률은 한 자릿수로 낮다 — PSR보다 PER·EV/EBITDA가 비교에 맞다. '
              '2026년 9월 사채 $1.5B를 새로 발행했는데 6월 말 재무상태표 뒤라 카드의 차입금에는 아직 없다. 2026년 부문을 새로 나눴다.')
PH = ['DELL', 'IBM', 'CSCO', 'ANET', 'STX', 'APH']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': 'IT 하드웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(CDW 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 IT 하드웨어 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 2026년 재편) — 상업 3,965.4 + 교육 933.1 + 정부 848.0 + 기타 825.7 = 6,572.2.
SEG = [('상업(기업)', 3965.4, '#cc0000'), ('교육', 933.1, '#e86666'), ('정부', 848.0, '#333333'), ('기타(영국·캐나다 등)', 825.7, '#a0a0a0')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 고객 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07:03~07:08 동부 접수) → 같은 날. 넣지 않은 8-K: 임원·이사 교체, 신용 한도(12/23), 자사주 한도 $1B 증액, 사채 발행(9월), 부문 재편 자료(5/1).
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('red', '2026년 8월 5일 — Q2 2026 실적', '2026-08-05',
     '순매출 $6.57B(+10%) · 순이익 $274M · 희석 EPS $2.15(1년 전 $2.05) · CFO 2027년 은퇴 예정 — 발표 당일 주가 −9%', 'q2', 'CDW 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 6일 — Q1 2026 실적', '2026-05-06',
     '순매출 $5.68B · 순이익 $235M · 희석 EPS $1.82(1년 전 $1.69) — 발표 당일 주가 −20%', 'q1', 'CDW 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 4일 — Q4 2025 실적', '2026-02-04',
     '순매출 $5.51B · 순이익 $280M · 희석 EPS $2.14(1년 전 $1.97) · 2025년 EPS $8.08 — 발표 당일 주가 +9%', 'q4', 'CDW 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 4일 — Q3 2025 실적', '2025-11-04',
     '순매출 $5.74B · 순이익 $291M · 희석 EPS $2.21(1년 전 $2.34) — 발표 당일 주가 −9%', 'q3', 'CDW 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 10, 'nt': 6, 'mean': 181, 'median': 193, 'low': 148, 'high': 195, 'sb': 5, 'b': 2, 'h': 3, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 4개(수동 지도, 2026년 재편). 원문 대조: Q2 2026 3,965.4/933.1/848.0/825.7(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"cdw:CommercialSegmentMember": ["상업(기업)", "#cc0000"], "cdw:EducationSegmentMember": ["교육", "#e86666"],
             "cdw:GovernmentSegmentMember": ["정부", "#333333"], "us-gaap:AllOtherSegmentsMember": ["기타(영국·캐나다 등)", "#a0a0a0"]},
 "ignore": []
}
