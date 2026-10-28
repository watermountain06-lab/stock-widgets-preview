# GEHC(GE 헬스케어) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 2023-01 GE에서 분사 — 영상 장비(CT·MRI·초음파), 의약품 진단(조영제·방사성의약품), 환자 모니터링.
# 출처: SEC XBRL(10/28 Q3 2026 10-Q까지 요약 자료에 있음), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 06:25 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/GEHC_q3.md.
# 엔진 입력(2026-10-28): 차입금 $9,973M, 현금 $2,826M, 비지배지분 = 자본 안 $17M + 상환가능 $234M(EV_TAGS_BY_CIK), 연금 부채 $5.1B(차입금에 넣지 않는다), 감가상각 = 감가상각 + 무형 상각(합산 태그 없음).
# 일회성: 최근 4분기 GAAP 4.74 대 조정 4.90(3.4% — 인수 무형 상각·구조조정·연금 비영업 수익·2분기 관세 환급). 2026-03 Intelerad 인수 $2.3B.
# 2023-01-04 GE에서 분사 상장 — 일봉 1,375개 미만 짧은 상장, 사용자 결정(2026-10-28) short_listing(CEG 방식).
BUILD = {'short_listing': True}
CIK = '0001932393'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'GE HealthCare'
S_ = 'https://www.sec.gov/Archives/edgar/data/1932393/'
SEC = S_
TENQ = S_ + '000193239326000059/gehc-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000193239326000058/release3q26earnings.htm', 'q2': S_ + '000193239326000045/release2q26earnings.htm',
      'q1': S_ + '000193239326000030/release1q26earnings.htm', 'q4': S_ + '000193239326000006/release4q25earnings.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="gehcFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('2023년 1월 GE에서 분사해 상장 이력이 4년이 안 된다 — 자기 이력은 그 기간만으로 비교한다. 연금 부채 $5.1B는 차입금에 넣지 않았다. '
              '2026년 3월 Intelerad(의료 영상 소프트웨어)를 $2.3B에 인수했다. 2분기 이익에는 2025년분 관세 환급(주당 약 0.25)이 들어 있다 — 빼도 자기 이력·동종업 표는 그대로다. 배당은 분기 $0.035 → $0.04(1년 전 3분기에는 선언이 두 번 들어가 $0.07로 보인다).')
PH = ['TMO', 'DHR', 'ABT', 'BSX', 'SYK', 'MDT']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '의료기기·진단 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(GEHC 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·유통·서비스가 섞여 있다. 차트에는 의료기기·진단 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 영상 장비(AIS) 3,873 + 의약품 진단(PDx) 846 + 환자 모니터링(PCS) 793 = 5,512, 본사 2·반올림 −1 → 5,513.
SEG = [('영상 장비(AIS)', 3873, '#5a2d82'), ('의약품 진단(PDx)', 846, '#9c7cc4'), ('환자 모니터링(PCS)', 793, '#00a3ad')]
SEG_ADJ = 1
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 28일 장 전 — Q3 2026 실적', '2026-10-28',
     '매출 $5.51B(+7.2%) · 순이익 $615M · 희석 EPS $1.36(1년 전 $0.98) · 연간 조정 EPS 전망 $4.95~5.05로 올림 — 당일 주가 +6.8%', 'q3', 'GE HealthCare 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 29일 장 전 — Q2 2026 실적', '2026-07-29',
     '매출 $5.30B · 순이익 $561M · 희석 EPS $1.24(1년 전 $1.06) — 2025년분 관세 환급 포함 — 당일 주가 +12.2%', 'q2', 'GE HealthCare 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 29일 장 전 — Q1 2026 실적', '2026-04-29',
     '매출 $5.13B · 순이익 $389M · 희석 EPS $0.85(1년 전 $1.23) — 당일 주가 −13.2%', 'q1', 'GE HealthCare 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 4일 장 전 — Q4 2025 실적', '2026-02-04',
     '매출 $5.70B · 순이익 $589M · 희석 EPS $1.29(1년 전 $1.57) · 2025년 EPS $4.55', 'q4', 'GE HealthCare 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 22, 'nt': 16, 'mean': 79.81, 'median': 80, 'low': 70, 'high': 93, 'sb': 10, 'b': 6, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-28'


# ── 자동 카드 — 부문 3개(영업 부문 차원). 원문 대조: Q3 2026 3,873/846/793(2026-10-28) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"gehc:AISSegmentMember": ["영상 장비(AIS)", "#5a2d82"], "gehc:PDxSegmentMember": ["의약품 진단(PDx)", "#9c7cc4"], "gehc:PCSSegmentMember": ["환자 모니터링(PCS)", "#00a3ad"]},
 "ignore": []
}
