# IR(잉거솔 랜드) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 압축기·진공 펌프·블로어(산업 기술·서비스)와 정밀 펌프·유체 기술(정밀·과학 기술).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-31), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/IR.md.
# 엔진 입력(2026-10-25): 차입금 = 1년 안 $699.8M + 장기 $4,068.7M(DEBT_TOTAL_TAG — LongTermDebtAndCapitalLeaseObligations는 이름과 달리 비유동만), 현금 $1,173.5M, 비지배지분 $65.7M.
# D&A = 무형자산 상각 + 매출원가 감가상각(DDA_PARTS_BY_CIK — 합산 태그는 분기 행이 2024년부터라 EV/EBITDA 이력이 짧았다; FY21~25 연간 합 일치).
# EPS는 계속사업 EPS(BUILD eps_tag, EMR 방식) — 2021년 중단사업(고압 솔루션 매각) 이익을 뺀다. 계속사업 태그가 FY2024에 멈춘 뒤로는 희석 EPS(중단사업 없음).
# 일회성: Q2 2025 영업권·무형자산 손상 $265.8M + 지분법 손실 $120.9M(주당 약 $1.0) — 최근 4분기 밖이지만 5년 PER 이력 안. 최근 4분기 구조조정은 EPS의 약 4%.
BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}
CIK = '0001699150'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Ingersoll Rand'
S_ = 'https://www.sec.gov/Archives/edgar/data/1699150/'
SEC = S_
TENQ = S_ + '000162828026051415/iri-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000162828026051068/ir2026q2ex991.htm', 'q1': S_ + '000162828026027949/ir2026q1ex991.htm',
      'q4': S_ + '000162828026007710/ir2025q4ex991.htm', 'q3': S_ + '000162828025047573/ir2025q3ex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="irFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 25)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('작은 인수를 꾸준히 해서 무형자산 상각이 커 GAAP 이익이 조정 이익보다 낮게 나온다. '
              'Q2 2025 손상·지분법 손실(세전 주당 약 $0.97)로 2025년 하반기~2026년 상반기의 최근 4분기 EPS가 낮아 그 기간 PER이 높게 보인다 — 5년 PER 이력에 그 구간이 들어 있다 — 빼고 계산해도 자기 이력 점수는 약 89로 같다. '
              '현금흐름 시나리오 순서가 뒤집힌 것은 낙관 시나리오가 처음부터 낮은 매출/자본 비율을 써서 성장에 드는 재투자가 이익 증가를 상쇄하기 때문이다.')
PH = ['DOV', 'XYL', 'ITW', 'PH', 'IEX', 'GWW']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '산업 기계 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(IR 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 산업 기계 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 산업 기술·서비스 1,622.1 + 정밀·과학 기술 426.7 = 2,048.8.
SEG = [('산업 기술·서비스', 1622.1, '#c8102e'), ('정밀·과학 기술', 426.7, '#e8707f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:16~16:42 동부 접수) → 다음 거래일. 넣지 않은 8-K: 이사 선임, 주식보상 계획, 주총.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 30일 장 마감 뒤 — Q2 2026 실적', '2026-07-31',
     '매출 $2.05B(+8.5%) · 순이익 $257M · 희석 EPS $0.66(1년 전 −$0.29 — 손상·지분법 손실)', 'q2', 'Ingersoll Rand 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 장 마감 뒤 — Q1 2026 실적', '2026-04-29',
     '매출 $1.85B · 순이익 $192M · 희석 EPS $0.49(1년 전 $0.46)', 'q1', 'Ingersoll Rand 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 12일 장 마감 뒤 — Q4 2025 실적', '2026-02-13',
     '매출 $2.09B · 순이익 $266M · 희석 EPS $0.67(1년 전 $0.57) · 2025년 EPS $1.45(손상 포함)', 'q4', 'Ingersoll Rand 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 30일 장 마감 뒤 — Q3 2025 실적', '2025-10-31',
     '매출 $1.96B · 순이익 $244M · 희석 EPS $0.61(1년 전 $0.54)', 'q3', 'Ingersoll Rand 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 14, 'nt': 6, 'mean': 95, 'median': 95, 'low': 84, 'high': 109, 'sb': 7, 'b': 0, 'h': 7, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 2개(수동 지도). 원문 대조: Q2 2026 1,622.1/426.7(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"iri:IndustrialTechnologiesAndServicesSegmentMember": ["산업 기술·서비스", "#c8102e"], "iri:PrecisionAndScienceTechnologiesSegmentMember": ["정밀·과학 기술", "#e8707f"]},
 "ignore": []
}
