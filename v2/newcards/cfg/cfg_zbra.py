# ZBRA(지브라 테크놀로지스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일(분기는 토요일 마감). 바코드 스캐너·라벨 프린터·현장용 모바일 컴퓨터(Connected Frontline), RFID·머신 비전(Asset Visibility & Automation).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-04, 분기말 7/4), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/ZBRA.md.
# 엔진 입력(2026-10-25): 기본 경로 — 차입금 1년 안 $2,275M + 장기 $493M, 현금 $157M. 인수 = 최근 4분기 $1,303M(Elo Touch 2025-09-30 약 $1.3B).
# 일회성: Q4 2025 철수·구조조정 세전 $76M(로봇 $55M + 생산성 $21M), Q2 2026 관세 환급 이익 세전 $73M — 거의 상쇄(Codex r1).
CIK = '0000877212'
CUR, YO, QO = '2026-07-04', '2025-06-28', '2026-04-04'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'Zebra'
S_ = 'https://www.sec.gov/Archives/edgar/data/877212/'
SEC = S_
TENQ = S_ + '000162828026052550/zbra-20260704.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000162828026052158/zbraex99120260704.htm', 'q1': S_ + '000162828026033877/zbraex99120260404.htm',
      'q4': S_ + '000087721226000003/zbraex991123125.htm', 'q3': S_ + '000162828025046567/zbraex99120250927.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="zbraFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 25)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('유통·물류 기업의 설비투자 주기에 따라 매출이 크게 오르내린다 — 2023년 수요 급감으로 이익이 줄었다가 회복 중이라 5년 이력에 그 저점이 섞여 있다. '
              'Elo Touch 인수(약 $1.3B, 2025-09-30)로 매출·상각이 늘었고, 인수 대금이 현금흐름 모델의 최근 투자에 잡혀 기본 가치를 약 15% 낮춘다(빼면 약 $112, 판정은 같다). 최근 4분기 이익에는 Q4 2025 철수·구조조정 비용(세전 $76M — 로봇 사업 철수 $55M + 생산성 개선 $21M)과 Q2 2026 관세 환급 이익(세전 $73M, 영업이익 안)이 함께 들어 있어 서로 거의 상쇄된다 — 각각 빼도 세 표는 같다. '
              '차입금의 대부분($2.3B)이 1년 안 만기다.')
PH = ['ANET', 'CSCO', 'DELL', 'APH', 'STX', 'IBM']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': 'IT 하드웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(ZBRA 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 IT 하드웨어 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — Connected Frontline 903 + Asset Visibility & Automation 654 = 1,557.
SEG = [('현장용 모바일·스캐너(CF)', 903, '#000000'), ('RFID·프린터·머신 비전(AVA)', 654, '#8a8a8a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07:27~07:53 동부 접수) → 같은 날. 넣지 않은 8-K: Elo 인수 완료 보도(10/1 7.01 — Q3 실적 항목에 적음), 로봇 사업 철수(12/15 2.05 — Q4 실적 항목), 임원·정관·주총.
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 4일 — Q2 2026 실적', '2026-08-04',
     '매출 $1.56B(+20%) · 순이익 $233M · 희석 EPS $4.85(1년 전 $2.19) — 관세 환급 이익 세전 $73M 포함, 발표 당일 주가 +26%', 'q2', 'Zebra 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 12일 — Q1 2026 실적', '2026-05-12',
     '매출 $1.50B · 순이익 $135M · 희석 EPS $2.72(1년 전 $2.62) — 발표 당일 주가 +11%', 'q1', 'Zebra 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 12일 — Q4 2025 실적', '2026-02-12',
     '매출 $1.48B · 순이익 $70M · 희석 EPS $1.39(1년 전 $3.14) — 철수·구조조정 비용 세전 $76M(로봇 사업 $55M 포함) 포함, 발표 당일 주가 +9%', 'q4', 'Zebra 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 28일 — Q3 2025 실적', '2025-10-28',
     '매출 $1.32B · 순이익 $101M · 희석 EPS $1.97(1년 전 $2.64) · Elo Touch 인수 완료(9/30) — 발표 당일 주가 −12%', 'q3', 'Zebra 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 16, 'nt': 11, 'mean': 409.55, 'median': 430, 'low': 317, 'high': 450, 'sb': 7, 'b': 3, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 2개(수동 지도). 원문 대조: Q2 2026 903/654(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"zbra:ConnectedFrontlineSegmentMember": ["현장용 모바일·스캐너(CF)", "#000000"], "zbra:AssetVisibilityAndAutomationSegmentMember": ["RFID·프린터·머신 비전(AVA)", "#8a8a8a"]},
 "ignore": []
}
