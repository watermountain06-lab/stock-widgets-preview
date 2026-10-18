# EMR(에머슨 일렉트릭) v2 카드 설정 — 자동 카드(AUTO). 회계연도 9월 30일(Q3 FY26 = 2026-04-01~06-30). 카드 순위 125(시총 123위). 자동화 제어·계측·소프트웨어.
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-08-04), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항), 8-K(CEO·COO 특별 성과 스톡옵션 2025-11-13, 보고 부문 개편 2025-11-20,
# 연금 회계 변경 2026-10-13), StockAnalysis.
# 과거 숫자(2026-10-18 사용자 결정 "GE 방식 + 매각 뒤 창"): 2023-05 Climate Technologies(Copeland) 매각으로 과거 매출·이익이 계속사업 기준으로 재작성됐다
# (FY2021 원공시 $18.2B → $12.9B). 분사가 아니라 현금 매각이라 주가는 조정되지 않았지만, 재작성 값을 쓰고(fetch_eps_history.RESTATED_LATEST) 자기 이력 창은
# 매각 뒤 첫 재무상태표가 나온 2023-08-02부터(build_multiple_history.HISTORY_START), 현금흐름 성장률 창은 2022-09-30부터(build_dcf.HISTORY_WINDOW).
# EPS는 계속사업 EPS(BUILD eps_tag — FY2023 매각 이익이 희석 EPS에 들어 PER이 3.7배까지 내려갔다). 4분기 EPS: FY24만 보도자료 값 $0.97(역산 $0.98).
# 엔진 입력: 손익계산서에 영업이익 줄이 없어 영업이익 = 계속사업 세전이익 + 순이자비용(DERIVED_OPINC — "Other deductions, net"의 무형자산 상각·구조조정은 영업비용으로 남김).
# 차입금 = DebtCurrent + LongTermDebtNoncurrent($13,113M), 현금 태그 2021 멈춤 → 합계 태그(EV_TAGS_BY_CIK), 이자비용 = 순이자(vendor CONCEPTS_BY_CIK).
# 2026-10-13 연금 회계 변경(보험계리 손익을 그해 4분기에 한 번에 반영) — FY24·FY25도 소급 재작성(FY25 4분기 세전 −$36M, EPS 1.12 → 1.07, Fable 필수). 카드의 과거 값은
# 지금 SEC 자료(재작성 전)라 FY26 10-K가 나오면 재작성 값으로 바뀐다(RESTATED_LATEST).
CIK = '0000032604'
BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # 계속사업 EPS, 없는 분기는 희석 EPS(FY26 1분기 10-Q는 중단사업이 없어 희석만 태깅 — 없으면 공개일이 2분기 10-Q로 밀렸다, Codex 2026-10-18)
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-09-30', '2024-09-30'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Emerson'
S_ = 'https://www.sec.gov/Archives/edgar/data/32604/'
SEC = S_
TENQ = S_ + '000003260426000043/emr-20260630.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000003260426000042/a2026q3release_ex991.htm', 'q2': S_ + '000003260426000034/a2026q2release_ex991.htm',
      'q1': S_ + '000003260426000006/a2026q1release_ex991.htm', 'q4': S_ + '000003260425000079/a2025q4release_ex991.htm'}
LINKS = {'pension': S_ + '000003260426000047/emr-20261013.htm', 'seg': S_ + '000003260425000094/a2025updatedsegmentrelease.htm',
         'award': S_ + '000003260425000091/emr-20251113.htm'}
FAIRBAND_TITLE = 'id="emrFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 계속사업 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 매각 뒤 실제 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 30)
ACT_REASON = ''
NONOP_WHAT = '장기투자'
SELF_SPAN = 'Copeland 매각 뒤 2023-08부터'   # 자기 이력 창 — 길이(년)는 쓰지 않는다(시간이 지나면 틀린다)
GROWTH_SPAN = '매각 뒤 계속사업 이력(2022-09 이후)'   # 역산 설명의 '지난 5년' 자리
# 고정 문장(숫자 없음 — 분기마다 고치지 않는다)
MODEL_NOTE = ('과거 숫자는 2023년 Copeland(공조 사업) 매각 뒤 계속사업 기준으로 재작성된 값이고, 자기 이력은 매각 뒤부터만 본다. '
              '투하자본의 대부분이 인수(NI·AspenTech 등)에서 생긴 영업권·무형자산이라 이 모델은 매출 1달러를 늘리는 데 큰 재투자가 든다고 본다. '
              '감가상각의 큰 몫이 인수 무형자산 상각이라 최근 1년 순투자가 음수여서 한계 효율을 정의하지 못하고 평균 비율을 쓴다 — 실제 FCF보다 훨씬 작은 현금흐름을 가정한 값이다.')
PH = ['ITW', 'ETN', 'ROK', 'AME', 'PH', 'JCI']   # HON은 비교군 파일 값(PER 9.7·PSR 1.7)이 분사 영향으로 보여 차트에서 뺌 — 점수는 S&P500 산업재 전체(공통 안건 E28)
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '자동화·산업 장비 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '자동화·산업 장비 PBR 비교', 'psr': '자동화·산업 장비 PSR 비교',
                'pcr': '자동화·산업 장비 PCR(FCF) 비교', 'evebitda': '자동화·산업 장비 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(EMR 제외)와 배수 순위를 매긴 값이다.',
            '기계·항공·운송·건설·업무 서비스 회사가 섞여 있다. 차트에는 자동화·산업 장비 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 부문 표) — 제어 시스템·소프트웨어 1,199 + 시험·계측 445 + 센서 1,091 + 최종 제어 1,586 + 안전·생산성 552 = 4,873(연결 매출).
SEG = [('제어 시스템·소프트웨어', 1199, '#004b8d'), ('시험·계측', 445, '#3d7cc0'), ('센서', 1091, '#7fa8d6'), ('최종 제어(밸브)', 1586, '#00335f'), ('안전·생산성', 552, '#9a9a9a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 보고 부문별(FY26부터 5개)'
# 손 뉴스: 10/13 연금 회계 변경 8-K가 Q3 실적(8/4) 뒤라 Q3도 손으로 쓴다(README). 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): Q3 8-K 8/4 20:05 → 8/5, Q2 5/5 20:06 → 5/6, Q1 2/3 21:05 → 2/4, Q4 FY25 11/5 11:55(장중) → 11/5,
# 부문 개편 11/20 11:55(장중) → 11/20, 특별 성과 스톡옵션(부여 11/13, 공시 11/14 21:23) → 11/17, 연금 회계 10/13 10:57(장중) → 10/13(Codex 2026-10-18 — 처음엔 접수일과 UTC 시각을 섞어 하루 앞당겼다).
NEWS_RANGE = '2025.11 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 13일 — 연금 회계 방식 변경', '2026-10-13',
     '보험계리 손익을 그해 4분기에 한 번에 손익으로 반영(시가 평가 방식) · FY24부터 소급 재작성 — FY25 4분기 세전 −$36M(계속사업 EPS $1.12 → $1.07, FY2025 $4.03 → $3.99), FY26 분기는 $2~3M · FY26 4분기 조정은 세전 $5M 미만 이익 예상', 'pension', 'Emerson 공시 (SEC 8-K)'),
    ('green', '2026년 8월 4일 장 마감 뒤 — Q3 FY26 실적', '2026-08-05',
     '매출 $4.87B(+7%) · 계속사업 희석 EPS $1.28(1년 전 $1.03) · 관세(IEEPA) 환급 $82M(주당 $0.11)이 매출원가에서 빠져 이익에 포함', 'q3', 'Emerson 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 5일 장 마감 뒤 — Q2 FY26 실적', '2026-05-06',
     '매출 $4.56B(+3%) · 계속사업 희석 EPS $1.10(1년 전 $0.86)', 'q2', 'Emerson 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 3일 장 마감 뒤 — Q1 FY26 실적', '2026-02-04',
     '매출 $4.35B(+4%) · 계속사업 희석 EPS $1.07(1년 전 $1.02)', 'q1', 'Emerson 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 20일 — 보고 부문 개편', '2025-11-20',
     'FY26부터 제어 시스템·소프트웨어, 시험·계측, 센서, 최종 제어, 안전·생산성 5개 부문으로 공시(과거 분기 재구성 자료 공개)', 'seg', 'Emerson 공시 (SEC 8-K)'),
    ('neutral', '2025년 11월 14일 장 마감 뒤 — CEO·COO 특별 성과 스톡옵션(11/13 부여)', '2025-11-17',
     'CEO Lal Karsanbhai·COO Ram Krishnan에게 장기 성과형 스톡옵션 — 80%는 행사가를 부여일 시가보다 크게 높여 주가가 많이 올라야 가치가 생긴다', 'award', 'Emerson 공시 (SEC 8-K)'),
    ('green', '2025년 11월 5일 — Q4 FY25 실적', '2025-11-05',
     '매출 $4.86B(+5%) · 계속사업 희석 EPS $1.12(1년 전 $0.97) · FY2025 매출 $18.02B·EPS $4.03', 'q4', 'Emerson 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 30, 'nt': 15, 'mean': 173.67, 'median': 175, 'low': 135, 'high': 190, 'sb': 16, 'b': 4, 'h': 8, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-18'


# ── 자동 카드 — 부문 지도: 부문마다 그룹 축(ProductOrServiceAxis — Software & Systems·Intelligent Devices, 안전·생산성은 없음)이 붙어 seg_map_propose는 2/5만 맞췄다.
# 그 축은 free_axes로 무시(seg_xbrl 2026-10-18 새 키). 원문 대조: 10-Q 부문 표 Q3 FY26 1,199/445/1,091/1,586/552, 1년 전 1,120/360/1,013/1,522/538 = 연결 매출 ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "free_axes": ["srt:ProductOrServiceAxis"],
 "members": {
  "emr:ControlSystemsAndSoftwareMember": ["제어 시스템·소프트웨어", "#004b8d"],
  "emr:TestAndMeasurementMember": ["시험·계측", "#3d7cc0"],
  "emr:SensorsMember": ["센서", "#7fa8d6"],
  "emr:FinalControlMember": ["최종 제어(밸브)", "#00335f"],
  "emr:SafetyAndProductivityMember": ["안전·생산성", "#9a9a9a"]
 },
 "ignore": []
}
