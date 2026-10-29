# TDY(텔레다인 테크놀로지스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 마지막 일요일(52/53주). 적외선 열화상·디지털 영상 센서(FLIR), 계측기, 항공·방산 전자, 엔지니어드 시스템.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-23 17:19 장 마감 뒤 접수 → 첫 세션 10/26), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 07시 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/TDY.md.
# 엔진 입력(2026-10-29): 기본 경로 — 차입금 $2,028M(장기, 1년 안 0.1), 현금 $562M, 비지배 없음. Varex Imaging 인수(약 $1.1B 현금, 2026-08 계약)는 미종결.
# 일회성: 최근 4분기 GAAP 21.88 중 Q4 2025 FLIR 세금 이익 $20.8M(주당 약 0.44, 2%), Q3 2026 Varex 지분 평가이익 $10.6M(주당 약 0.2). 빼도 표 그대로(Codex r1).
CIK = '0001094285'
CUR, YO, QO = '2026-09-27', '2025-09-28', '2026-06-28'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-28', '2024-12-29'), 'FY2025'
VOTES, VERDICT = (-1, 1, -2), '적정~고평가'
CO = 'Teledyne'
S_ = 'https://www.sec.gov/Archives/edgar/data/1094285/'
SEC = S_
TENQ = S_ + '000109428526000059/tdy-20260927.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000109428526000055/q3-2026earningsrelease.htm', 'q2': S_ + '000109428526000039/q2-2026earningsrelease.htm', 'q1': S_ + '000109428526000024/q1-2026earningsrelease.htm', 'q4': S_ + '000109428526000008/q4-2025earningsrelease.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="tdyFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('S&P500 업종 분류가 정보기술(전자 장비·계측기)이라 동종업 점수는 카드 유니버스 IT(반도체·소프트웨어·하드웨어) 기준이다 — 계측·방산 전자 회사와 직접 비교한 값이 아니다. '
              'Varex Imaging 인수(약 $1.1B 현금, 2026-08 계약)는 아직 끝나지 않아 그 사업 실적과 인수 차입은 들어 있지 않다 — 먼저 사 둔 Varex 지분의 평가이익 $10.6M은 3분기 기타이익에 들어 있다. '
              '산업재 비교군(S&P500 산업재)으로 재면 동종업 점수가 약 42로 내려가 판정이 고평가가 된다.')
PH = ['APH', 'TXN', 'CSCO', 'QCOM', 'DELL', 'IBM']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '하드웨어·부품 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(TDY 제외)과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 섞여 있다. 차트에는 하드웨어·부품 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 디지털 영상 903.0 + 계측기 370.5 + 항공·방산 전자 287.4 + 엔지니어드 시스템 124.0 = 1,684.9.
SEG = [('디지털 영상(FLIR 등)', 903.0, '#003a70'), ('계측기', 370.5, '#4f86c6'), ('항공·방산 전자', 287.4, '#e4002b'), ('엔지니어드 시스템', 124.0, '#8c8c8c')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07시 동부) → 같은 날.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 21일 — Q3 2026 실적', '2026-10-21',
     '매출 $1.68B(+9.4%) · 순이익 $273M · 희석 EPS $5.82(1년 전 $4.65) · Varex Imaging 인수 계약 재확인', 'q3', 'Teledyne 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 22일 — Q2 2026 실적', '2026-07-22',
     '매출 $1.66B · 순이익 $252M · 희석 EPS $5.37(1년 전 $4.43)', 'q2', 'Teledyne 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 22일 — Q1 2026 실적', '2026-04-22',
     '매출 $1.56B · 순이익 $227M · 희석 EPS $4.85(1년 전 $3.99) — 당일 주가 +2.2%', 'q1', 'Teledyne 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 21일 — Q4 2025 실적', '2026-01-21',
     '매출 $1.61B · 순이익 $276M · 희석 EPS $5.84(1년 전 $4.20) · FLIR 세금 이익 $20.8M 포함 — 당일 주가 +9.8%', 'q4', 'Teledyne 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 12, 'nt': 10, 'mean': 766.1, 'median': 780, 'low': 646, 'high': 915, 'sb': 6, 'b': 3, 'h': 3, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-29'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 903.0/370.5/287.4/124.0(2026-10-29) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"tdy:DigitalImagingMember": ["디지털 영상(FLIR 등)", "#003a70"], "tdy:InstrumentationMember": ["계측기", "#4f86c6"], "tdy:AerospaceAndDefenseElectronicsMember": ["항공·방산 전자", "#e4002b"], "tdy:EngineeredSystemsMember": ["엔지니어드 시스템", "#8c8c8c"]},
 "ignore": []
}
