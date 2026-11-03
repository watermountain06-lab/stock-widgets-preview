BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # 2023-06 Fortrea 분사 — 계속사업 EPS 우선
# LH(랩코프) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 진단(미국 임상 검사) + 바이오제약 실험실 서비스(중앙 검사실·초기 개발), 부문 2개.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-30 16:11 장 마감 뒤 접수 — 첫 세션 11/2), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 06:5x 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/LH.md(Q2 기준 + Q3 보도자료).
# 2023-06-30 Fortrea(임상 개발 사업) 분사 — RESTATED_LATEST, 자기 이력 2024-04-30부터(HISTORY_START — 그날 최근 4분기 합이 모두 계속사업), 현금흐름 성장 이력 2023-06 최근 4분기 합부터(HISTORY_WINDOW), Yahoo 1.164는 분사 가격 조정이라 분할 목록 비움(KNOWN_SPLITS []).
# 희석 EPS는 계속사업 우선, Q4 2022~2024는 보도자료 값(Q4_EPS_OVERRIDE). 비지배지분 2010년 낡은 값 제외(EV_TAGS_BY_CIK). E54 시험: 일회성(구조조정 등)을 빼도 투표 불변.
# 일회성: 최근 4분기 GAAP 12.19 중 Q4 2025 Early Development 구조조정 $110.8M(세전) 등 — 회사 조정에는 매 분기 반복되는 인수 비용·LaunchPad 비용도 섞여 있다.
CIK = '0000920148'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Labcorp'
S_ = 'https://www.sec.gov/Archives/edgar/data/920148/'
SEC = S_
TENQ = S_ + '000092014826000222/lh-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000092014826000213/form8-kexhibit9913q26.htm', 'q2': S_ + '000092014826000162/form8-kexhibit9912q26.htm', 'q1': S_ + '000092014826000135/form8-kexhibit9911q26.htm', 'q4': S_ + '000092014826000098/form8-kerex991for4q25.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="lhFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('회사 조정 EPS(최근 4분기 18.09)는 GAAP(12.19)보다 훨씬 높다 — 인수 무형자산 상각과 매 분기 반복되는 인수·비용 절감(LaunchPad) 비용을 빼서다. 카드는 GAAP 기준이라 영업이익률이 낮게 나오고 현금흐름 가치도 낮다. '
              '2023년 Fortrea 분사로 과거 실적이 재작성돼 자기 이력은 2024-04-30부터 비교한다. 3분기 뒤 인수 4건(MLM Medical Labs 완료 등)과 9월 메디케어 검사 수가(PAMA) 인하 예비안이 있다. '
              '동종업 점수는 S&P500 헬스케어 기준이다.')
PH = ['DGX', 'HCA', 'UHS', 'IQV', 'CRL', 'DVA']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '검사·헬스케어 서비스 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(LH 제외)와 배수 순위를 매긴 값이다.',
            '제약·의료기기·보험이 섞여 있다. 차트에는 검사·병원·임상 서비스 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 진단 2,948.9 + 바이오제약 실험실 866.7 = 3,815.6, 부문 간 거래 −5.6 → 연결 3,810.0.
SEG = [('진단(임상 검사)', 2948.9, '#00539b'), ('바이오제약 실험실 서비스', 866.7, '#e31837')]
SEG_ADJ = -5.6
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:5x 동부) → 같은 날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 28일 장 전 — Q3 2026 실적', '2026-10-28',
     '매출 $3.81B(+6.9%) · 순이익 $263M · 희석 EPS $3.22(1년 전 $3.12) · 조정 EPS $4.78 · 연간 조정 EPS 전망 18.30~18.70으로 상향 — 당일 주가 +8.8%', 'q3', 'Labcorp 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 30일 장 전 — Q2 2026 실적', '2026-07-30',
     '매출 $3.73B(+5.8%) · 순이익 $299M · 희석 EPS $3.64(1년 전 $2.84) · 조정 EPS $4.99 — 당일 주가 +2.7%', 'q2', 'Labcorp 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 30일 장 전 — Q1 2026 실적', '2026-04-30',
     '매출 $3.54B(+5.8%) · 순이익 $278M · 희석 EPS $3.35(1년 전 $2.52) — 당일 주가 −0.1%', 'q1', 'Labcorp 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 17일 장 전 — Q4 2025 실적', '2026-02-17',
     '매출 $3.52B(+5.6%) · 순이익 $165M · 희석 EPS $1.98(1년 전 $1.70) · Early Development 구조조정 $111M 포함 · 2025년 EPS $10.46 — 당일 주가 −2.1%', 'q4', 'Labcorp 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 17, 'nt': 11, 'mean': 374, 'median': 380, 'low': 310, 'high': 420, 'sb': 10, 'b': 2, 'h': 5, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-03'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 2,948.9/866.7(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"lh:DiagnosticsMember": ["진단(임상 검사)", "#00539b"], "lh:BiopharmaLaboratoryServicesMember": ["바이오제약 실험실 서비스", "#e31837"]},
 "ignore": []
}
