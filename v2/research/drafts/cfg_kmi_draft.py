# KMI(킨더 모건) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 천연가스 파이프라인(수송·저장)·석유제품 파이프라인·터미널·CO2(원유 회수).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-23), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/KMI.md.
# 엔진 입력(2026-10-24): 차입금 = 1년 안(DebtCurrent, CP 포함) $1,726M + 장기 $31,347M = $33,073M(DEBT_TOTAL_TAG — 기본 선택은 장기만). 비지배지분 $1,232M.
# 지분법 투자(이익은 영업이익 아래)는 엔진 기본 비영업 자산. 최근 4분기 GAAP 이익의 '특정 항목'(매각 이익·평가손익·충당금)은 세후 합계 −$61M으로 작다.
CIK = '0001506307'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '적정'
CO = 'Kinder Morgan'
S_ = 'https://www.sec.gov/Archives/edgar/data/1506307/'
SEC = S_
TENQ = S_ + '000150630726000132/kmi-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000150630726000130/kmi2026q38-kex991.htm', 'q2': S_ + '000150630726000063/kmi2026q28-kex991.htm',
      'q1': S_ + '000150630726000033/kmi2026q18-kex991.htm', 'q4': S_ + '000150630726000002/kmi2025q48-kex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="kmiFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 45)
ACT_REASON = ''
NONOP_WHAT = '투자자산(대부분 지분법)'
MODEL_NOTE = ('수송관 설비 투자가 크고 사업 가치의 상당 부분이 차입금으로 빠져 주당 값이 작게 나올 수 있다 — 장기 수송 계약·규제 요금 자산에도 일반 할인율을 쓴다. '
              '지분법 투자(합작 파이프라인)의 이익은 영업이익 아래에 있어 투자 장부가를 비영업 자산으로 더한다. '
              'Q3 2026 이익은 석유제품 파이프라인의 법률·환경 충당금으로 낮아졌고 소규모 매각 이익으로 일부 메워졌다.')
PH = ['WMB', 'OKE', 'TRGP', 'XOM', 'CVX', 'COP']
PEER_FILE = 'peer_universe/energy.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '가스관·석유 6곳 PER 비교 (점수는 S&P500 에너지 기준)', 'pbr': '가스관·석유 PBR 비교', 'psr': '가스관·석유 PSR 비교',
                'pcr': '가스관·석유 PCR(FCF) 비교', 'evebitda': '가스관·석유 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 에너지 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 에너지 대비 배수 순위 (v2/peer_universe/energy.json)'
PEER_TIP = ('S&P500 에너지(KMI 제외)와 배수 순위를 매긴 값이다.',
            '석유 생산·정유·서비스·가스관 회사가 섞여 있다. 차트에는 가스관 3곳과 석유 대기업 3곳만 보인다.')
# 매출(Q3 2026 10-Q 부문, 외부 매출) — 천연가스 파이프라인 2,894 + 석유제품 772 + 터미널 560 + CO2 305 = 4,531.
SEG = [('천연가스 파이프라인', 2894.0, '#1a4f8b'), ('석유제품 파이프라인', 772.0, '#6f9fd6'), ('터미널', 560.0, '#a8c6ea'), ('CO2', 305.0, '#d4a03a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q3 2026, 외부 매출)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다). 반응일: 장 마감 뒤 발표 → 다음 거래일.
# 넣지 않은 8-K: 콘퍼런스 참석 안내(7.01), COO 교체(4/22, 실적과 함께), 주총, 신용 한도 연장(5/28), 사채 발행(8/3).
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 21일 — Q3 2026 실적', '2026-10-22',
     '매출 $4.53B(1년 전 $4.15B) · 순이익 $764M · 희석 EPS $0.34(1년 전 $0.28) — 석유제품 파이프라인 법률·환경 충당금 $138M, 매각 이익 $71M 포함', 'q3', 'Kinder Morgan 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 22일 — Q2 2026 실적', '2026-07-23',
     '매출 $4.48B(1년 전 $4.04B) · 순이익 $867M · 희석 EPS $0.39(1년 전 $0.32)', 'q2', 'Kinder Morgan 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 22일 — Q1 2026 실적', '2026-04-23',
     '매출 $4.83B(1년 전 $4.24B) · 순이익 $976M · 희석 EPS $0.44(1년 전 $0.32)', 'q1', 'Kinder Morgan 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 21일 — Q4 2025 실적', '2026-01-22',
     '매출 $4.51B(1년 전 $3.99B) · 순이익 $996M · 희석 EPS $0.45(1년 전 $0.30) — 매각 이익 $123M 포함 · 2025년 희석 EPS $1.37', 'q4', 'Kinder Morgan 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 18, 'mean': 37.06, 'median': 37, 'low': 32, 'high': 43, 'sb': 11, 'b': 2, 'h': 11, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-24'


# ── 자동 카드 — 부문 4개(외부 매출, 다른 차원 없는 행). 원문 대조: Q3 2026 2,894/772/560/305(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"kmi:NaturalGasPipelinesMember": ["천연가스 파이프라인", "#1a4f8b"], "kmi:ProductsPipelinesMember": ["석유제품 파이프라인", "#6f9fd6"],
             "kmi:TerminalsMember": ["터미널", "#a8c6ea"], "kmi:Co2Member": ["CO2", "#d4a03a"]},
 "ignore": []
}
