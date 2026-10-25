# HAL(핼리버튼) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 유전 서비스(완결·생산 — 수압파쇄·시멘팅 등, 시추·평가).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-23), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/HAL.md.
# 엔진 입력(2026-10-25): 차입금 = 1년 안 $90M + LongTermDebt(비유동 줄) $7,072M = $7,162M(DEBT_TOTAL_TAG). FY2025 연간 EPS가 요약 자료에 없어 4분기 EPS는 보도자료 값(Q4_EPS_OVERRIDE).
# 일회성: 손상·기타 비용과 환입이 분기마다 있지만 최근 4분기 GAAP EPS 2.39는 회사 조정 EPS와 거의 같다(서로 상쇄). 1년 전 Q3 2025 손상($392M)이 전년 대비를 키운다.
CIK = '0000045012'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '적정'
CO = 'Halliburton'
S_ = 'https://www.sec.gov/Archives/edgar/data/45012/'
SEC = S_
TENQ = S_ + '000004501226000074/hal-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000004501226000070/livemastererdocument.htm', 'q2': S_ + '000004501226000057/livemastererdocument.htm',
      'q1': S_ + '000004501226000036/livemastererdocument.htm', 'q4': S_ + '000004501226000008/livemastererdocument.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="halFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 25)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('유가와 북미 시추 활동에 이익이 크게 흔들리는 업종이다 — 최근 북미 매출은 줄고 해외(중남미·유럽·중동)가 늘었다. '
              '분기마다 손상·기타 비용과 환입이 섞이지만 최근 4분기 합으로는 회사 조정 이익과 거의 같다. 1년 전 분기의 큰 손상 때문에 전년 대비 증가율이 크게 나온다.')
PH = ['SLB', 'BKR', 'XOM', 'CVX', 'COP', 'EOG']
PEER_FILE = 'peer_universe/energy.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유전 서비스·석유 6곳 PER 비교 (점수는 S&P500 에너지 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 에너지 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 에너지 대비 배수 순위 (v2/peer_universe/energy.json)'
PEER_TIP = ('S&P500 에너지(HAL 제외)와 배수 순위를 매긴 값이다.',
            '석유 생산·정유·서비스·가스관 회사가 섞여 있다. 차트에는 유전 서비스 2곳과 석유 4곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 완결·생산 3,089 + 시추·평가 2,614 = 5,703.
SEG = [('완결·생산', 3089.0, '#cc0000'), ('시추·평가', 2614.0, '#e86b6b')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS는 쓰지 않는다). 반응일: 장 전 발표 → 같은 날. 넣지 않은 8-K: 이사·임원, Voltagrid 지분(2025-10), 주총.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 20일 — Q3 2026 실적', '2026-10-20',
     '매출 $5.70B(1년 전 $5.60B) · 순이익 $417M · 희석 EPS $0.50(1년 전 $0.02 — 손상) — 손상·기타 비용 포함', 'q3', 'Halliburton 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 21일 — Q2 2026 실적', '2026-07-21',
     '매출 $5.71B · 순이익 $534M · 희석 EPS $0.64(1년 전 $0.55) — 손상 환입(세전 약 $95M) 포함', 'q2', 'Halliburton 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 21일 — Q1 2026 실적', '2026-04-21',
     '매출 $5.40B · 순이익 $461M · 희석 EPS $0.55(1년 전 $0.24)', 'q1', 'Halliburton 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 21일 — Q4 2025 실적', '2026-01-21',
     '매출 $5.66B · 순이익 $589M · 희석 EPS $0.70(1년 전 $0.70)', 'q4', 'Halliburton 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 28, 'nt': 18, 'mean': 42.56, 'median': 42, 'low': 34, 'high': 51, 'sb': 16, 'b': 6, 'h': 5, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 2개(수동 지도). 원문 대조: Q3 2026 3,089/2,614(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"hal:CompletionAndProductionMember": ["완결·생산", "#cc0000"], "hal:DrillingAndEvaluationMember": ["시추·평가", "#e86b6b"]},
 "ignore": []
}
