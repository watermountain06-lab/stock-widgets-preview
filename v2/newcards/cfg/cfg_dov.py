# DOV(도버) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 산업 기계 5개 부문(엔지니어드 제품, 청정에너지·연료, 마킹·식별, 펌프·공정, 냉장·기후 기술).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-22 장 전), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/DOV.md.
# 엔진 입력(2026-10-25): 차입금 = LongTermDebt $3,264.6M(1년 안 포함, DEBT_TOTAL_TAG — 단기차입 태그가 같은 금액이라 기본 합산이 두 번 셌다), 현금 $1,693M(제한 현금 포함 줄).
# EPS는 계속사업 EPS(BUILD eps_tag, EMR 방식) — 2024년 4분기 ESG 매각 중단사업 이익(주당 $8.66)이 희석 EPS에 들어 그해 PER이 크게 낮게 나왔다.
# 2024년 1분기 De-Sta-Co 매각 이익(세전 $529.9M)은 계속사업 안이라 남는다. 최근 4분기 구조조정 비용은 계속사업 EPS의 약 7%.
BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}
CIK = '0000029905'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Dover'
S_ = 'https://www.sec.gov/Archives/edgar/data/29905/'
SEC = S_
TENQ = S_ + '000002990526000033/dov-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000002990526000032/a202610228-kexhibit991pr.htm', 'q2': S_ + '000002990526000026/a202607238-kexhibit991pr.htm',
      'q1': S_ + '000002990526000014/a202604238-kexhibit991pr.htm', 'q4': S_ + '000002990526000004/a202601298-kexhibit991pr.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="dovFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 계속사업 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('EPS는 계속사업 기준이다 — 2024년 ESG 사업 매각 이익(중단사업)을 빼야 그해 PER이 다른 해와 비교된다. 2024년 1분기 De-Sta-Co 매각 이익은 계속사업 안이라 그 시기 PER은 낮게 보인다 — 빼고 계산해도 자기 이력 점수는 약 69로 70에 못 미친다. '
              '현금흐름 시나리오 순서가 뒤집힌 것은 낙관 시나리오가 처음부터 낮은 매출/자본 비율을 써서 성장에 드는 재투자가 이익 증가를 상쇄하기 때문이다. '
              '사업 매각과 인수를 자주 해 매출 성장률에 그 영향이 섞인다.')
PH = ['ITW', 'PH', 'IR', 'XYL', 'IEX', 'EMR']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '산업 기계 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(DOV 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 산업 기계 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문, 내부거래 제거 전) — 청정에너지 606.0 + 펌프 568.5 + 냉장·기후 481.5 + 마킹 304.7 + 엔지니어드 274.9 = 2,235.5(제거 −1.7 → 2,233.8).
SEG = [('청정에너지·연료', 606.0, '#1a5aa6'), ('펌프·공정', 568.5, '#6f9fd8'), ('냉장·기후 기술', 481.5, '#0d2f5c'), ('마킹·식별', 304.7, '#a9c6ea'), ('엔지니어드 제품', 274.9, '#3d7cc4')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 계속사업 희석). 반응일: 장 전 발표 → 같은 날. 넣지 않은 8-K: $500M 자사주 일괄 매입(2025-11), 유로 사채, 신용 한도, 주총.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 22일 — Q3 2026 실적', '2026-10-22',
     '매출 $2.23B(+7.5%) · 순이익 $333M · 계속사업 희석 EPS $2.50(1년 전 $2.20)', 'q3', 'Dover 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 23일 — Q2 2026 실적', '2026-07-23',
     '매출 $2.19B · 순이익 $312M · 계속사업 희석 EPS $2.31(1년 전 $2.03) — 발표 당일 주가 −8%', 'q2', 'Dover 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 23일 — Q1 2026 실적', '2026-04-23',
     '매출 $2.05B · 순이익 $238M · 계속사업 희석 EPS $1.76(1년 전 $1.73) — 발표 당일 주가 +6%', 'q1', 'Dover 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 29일 — Q4 2025 실적', '2026-01-29',
     '매출 $2.10B · 순이익 $282M · 계속사업 희석 EPS $2.01 · 2025년 계속사업 EPS $7.97', 'q4', 'Dover 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 19, 'nt': 13, 'mean': 245.85, 'median': 245, 'low': 215, 'high': 274, 'sb': 14, 'b': 0, 'h': 4, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 5개(수동 지도, 내부거래 제거 전). 원문 대조: Q3 2026 606.0/568.5/481.5/304.7/274.9(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"dov:CleanEnergyFuelingSegmentMember": ["청정에너지·연료", "#1a5aa6"], "dov:PumpsProcessSolutionsSegmentMember": ["펌프·공정", "#6f9fd8"],
             "dov:ClimateSustainabilityTechnologiesSegmentMember": ["냉장·기후 기술", "#0d2f5c"], "dov:ImagingIdentificationSegmentMember": ["마킹·식별", "#a9c6ea"],
             "dov:EngineeredProductsSegmentMember": ["엔지니어드 제품", "#3d7cc4"]},
 "ignore": []
}
