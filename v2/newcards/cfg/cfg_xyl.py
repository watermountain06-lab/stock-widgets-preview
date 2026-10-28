# XYL(자일럼) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 물 펌프·처리 설비(Water Infrastructure), 건물·산업용 펌프(Applied Water), 스마트 계량기·계측(MCS), 수처리 서비스(WSS, 2023 Evoqua 인수).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-28), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/XYL.md.
# 엔진 입력(2026-10-25): 차입금 = 단기·1년 안 $531M + 장기 $2,395M(DEBT_TOTAL_TAG), 현금 $1,276M, 비지배지분 = 상환가능 $242M + $3M(EV_TAGS nci).
# D&A = 감가상각 + 무형자산 상각(DDA_PARTS_BY_CIK — 합산 태그가 2024-09에 멈춤, FY20~25 연간 합 일치).
# 진행 중 거래: Indicor의 Cornell·Roper 펌프 인수 약 $1.46B 현금(2026-08 서명, 4분기 종결 예정) — 9월 사채 $1.5B 발행. 둘 다 6월 말 재무상태표 뒤라 카드에 없다(문장 공개).
CIK = '0001524472'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Xylem'
S_ = 'https://www.sec.gov/Archives/edgar/data/1524472/'
SEC = S_
TENQ = S_ + '000152447226000110/xyl-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000152447226000108/xyl07282026ex991.htm', 'q1': S_ + '000152447226000065/xyl04282026ex991.htm',
      'q4': S_ + '000152447226000008/xyl02102026ex991.htm', 'q3': S_ + '000152447225000043/xyl10282025ex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="xylFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 25)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('2023년 Evoqua 주식 인수로 매출·주식 수·무형자산 상각이 한꺼번에 커져 5년 이력이 그 전후로 다르다 — GAAP 이익은 인수 상각만큼 회사 조정 이익보다 낮다. '
              'Cornell·Roper 펌프 인수(약 $1.46B, 4분기 종결 예정)와 9월 사채 $1.5B는 6월 말 재무상태표 뒤라 차입금·현금에 아직 없다. '
              '현금흐름 모델 값이 낮은 것은 Evoqua 영업권으로 투하자본이 커서(매출/자본 약 0.75배) 인수 포함 성장률을 따라가는 재투자가 세후 영업이익보다 크게 잡히기 때문이다. '
              '10-Q는 리스 부채를 1년 안 분만 태깅해 순차입금의 리스가 실제(2025년 말 운용 $408M·금융 $125M)보다 작다.')
PH = ['DOV', 'IR', 'IEX', 'ITW', 'PH', 'EMR']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '산업 기계 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(XYL 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 산업 기계 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 수처리 인프라 683 + 수처리 서비스 644 + 계측·제어 508 + 응용 펌프 501 = 2,336.
SEG = [('수처리 인프라', 683, '#0076c0'), ('수처리 서비스', 644, '#00a19a'), ('계측·제어(스마트 미터)', 508, '#5aa9dc'), ('응용 펌프(건물·산업)', 501, '#9cc9e8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q2 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07:02~07:06 동부 접수) → 같은 날. 넣지 않은 8-K: 자사주 $1.5B 승인, 사채 발행(5월·9월), 신용 한도, 이사·CFO 교체(9/1).
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 28일 — Q2 2026 실적', '2026-07-28',
     '매출 $2.34B(+1.5%) · 순이익 $263M · 희석 EPS $1.11(1년 전 $0.93)', 'q2', 'Xylem 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 — Q1 2026 실적', '2026-04-28',
     '매출 $2.13B · 순이익 $193M · 희석 EPS $0.79(1년 전 $0.69)', 'q1', 'Xylem 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 10일 — Q4 2025 실적', '2026-02-10',
     '매출 $2.40B · 순이익 $335M · 희석 EPS $1.37(1년 전 $1.34) · 2025년 EPS $3.92 — 발표 당일 주가 −8%', 'q4', 'Xylem 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 28일 — Q3 2025 실적', '2025-10-28',
     '매출 $2.27B · 순이익 $227M · 희석 EPS $0.93(1년 전 $0.89)', 'q3', 'Xylem 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 12, 'mean': 138.58, 'median': 141, 'low': 110, 'high': 165, 'sb': 10, 'b': 4, 'h': 7, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 4개(수동 지도, 영업 부문 차원). 원문 대조: Q2 2026 683/644/508/501(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax", "us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"xyl:WaterInfrastructureSegmentMember": ["수처리 인프라", "#0076c0"], "xyl:WaterSolutionsServicesSegmentMember": ["수처리 서비스", "#00a19a"],
             "xyl:MeasurementAndControlSolutionsSegmentMember": ["계측·제어(스마트 미터)", "#5aa9dc"], "xyl:AppliedWaterSegmentMember": ["응용 펌프(건물·산업)", "#9cc9e8"]},
 # 2026 Q3 10-Q부터 회사가 두 부문의 태그 이름을 바꿨다(사업부는 그대로) — 옛 이름을 그대로 쓰는 지난 분기와 맞추려고 되돌려 읽는다(2026-10-28)
 "alias": {"xyl:AppliedWaterMember": "xyl:AppliedWaterSegmentMember",
           "xyl:MeasurementandControlSolutionsMember": "xyl:MeasurementAndControlSolutionsSegmentMember"},
 "ignore": []
}
