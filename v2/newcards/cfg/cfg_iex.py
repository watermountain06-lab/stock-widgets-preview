# IEX(IDEX) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 정밀 유체·측정 기술 — 생명과학·광학 부품(HST), 펌프·유량계(FMT), 소방·안전 장비(FSDP).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-29), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/IEX.md.
# 엔진 입력(2026-10-25): 기본 경로 — 차입금 1년 안 $0.4M + 장기 $1,858.5M, 현금 $621.3M. D&A = 감가상각 + 무형자산 상각(DDA_PARTS_BY_CIK — 합산 태그 2024-09 멈춤, FY20~23 연간 합 일치).
# 일회성 작음(최근 4분기 구조조정 세전 약 $13M, Q2 2026 관세 환급).
CIK = '0000832101'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'IDEX'
S_ = 'https://www.sec.gov/Archives/edgar/data/832101/'
SEC = S_
TENQ = S_ + '000083210126000022/iex-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000083210126000019/iex-20260630xex991.htm', 'q1': S_ + '000083210126000007/iex-20260331xex991.htm',
      'q4': S_ + '000162828026005268/iex-20251231xex991.htm', 'q3': S_ + '000162828025046909/iex-20250930xex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="iexFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('작은 회사를 자주 인수해(2024 Mott, 2025 Micro-LAM) 무형자산 상각이 늘어 GAAP 이익이 회사 조정 이익보다 낮다. '
              '생명과학·반도체 장비용 광학·유체 부품(HST) 비중이 커지고 있다. '
              '현금흐름 모델 값이 낮은 것은 인수로 쌓인 영업권·무형자산이 투하자본의 대부분이라(매출/자본 약 0.68배) 투하자본 이익률이 할인율과 비슷해 성장이 가치를 거의 더하지 못하기 때문이다.')
PH = ['DOV', 'IR', 'XYL', 'ITW', 'PH', 'AME']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '산업 기계 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(IEX 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 산업 기계 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 보건·과학 414.0 + 유체·계량 316.7 + 소방·안전 189.9 = 920.6.
SEG = [('보건·과학 기술', 414.0, '#004b87'), ('유체·계량 기술', 316.7, '#4d86b8'), ('소방·안전·특수 제품', 189.9, '#e57200')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07:00~07:08 동부 접수) → 같은 날. 넣지 않은 8-K: 자사주 승인(2025-09), CFO 선임, 신용 계약, 주총·이사.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 29일 — Q2 2026 실적', '2026-07-29',
     '매출 $921M(+6.4%) · 순이익 $143M · 희석 EPS $1.93(1년 전 $1.74) — 관세 환급 포함', 'q2', 'IDEX 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 29일 — Q1 2026 실적', '2026-04-29',
     '매출 $887M · 순이익 $120M · 희석 EPS $1.61(1년 전 $1.26) — 발표 당일 주가 +6%', 'q1', 'IDEX 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 4일 — Q4 2025 실적', '2026-02-04',
     '매출 $899M · 순이익 $128M · 희석 EPS $1.71(1년 전 $1.62) · 2025년 EPS $6.41 — 발표 당일 주가 +5%', 'q4', 'IDEX 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 29일 — Q3 2025 실적', '2025-10-29',
     '매출 $879M · 순이익 $128M · 희석 EPS $1.70(1년 전 $1.57)', 'q3', 'IDEX 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 15, 'nt': 12, 'mean': 268.08, 'median': 272, 'low': 245, 'high': 283, 'sb': 9, 'b': 1, 'h': 5, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 3개(수동 지도, 영업 부문 차원). 원문 대조: Q2 2026 414.0/316.7/189.9(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"iex:HealthAndScienceTechnologiesMember": ["보건·과학 기술", "#004b87"], "iex:FluidAndMeteringTechnologiesMember": ["유체·계량 기술", "#4d86b8"],
             "iex:FireAndSafetyDiversifiedProductsMember": ["소방·안전·특수 제품", "#e57200"]},
 "ignore": []
}
