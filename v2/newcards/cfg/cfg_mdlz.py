# MDLZ(몬델리즈) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 과자·초콜릿·껌(Oreo, Cadbury, Milka, Toblerone) — 북미·유럽·중남미·아시아중동아프리카.
# 출처: SEC XBRL + 인라인 XBRL 보충(BUILD overlay — companyfacts에 7/28 Q2 10-Q가 없다, 시험 3장 중 2), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/MDLZ.md.
# 엔진 입력(2026-10-25): 차입금 = 단기 $2,327M + 1년 안 $2,663M + 장기 $16,460M(DEBT_TOTAL_TAG), 현금 = 제한 현금 포함 줄 $1,759M(EV_TAGS cash — 기본 태그 없음), 비지배지분 $53M.
# 일회성: 원자재 헤지 파생상품 평가손익(MTM)이 영업이익 안 — Q2 2026 이익 세전 $827M(주당 0.51), 앞 세 분기 손실. 최근 4분기 순효과는 주당 +0.02(약 1%)지만 분기마다 크게 흔들린다.
BUILD = {'overlay': True}
CIK = '0001103982'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Mondelez'
S_ = 'https://www.sec.gov/Archives/edgar/data/1103982/'
SEC = S_
TENQ = S_ + '000162828026050179/mdlz-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000162828026050157/mdlzearningsreleasecontent.htm', 'q1': S_ + '000162828026027915/mdlzearningsreleasecontent.htm',
      'q4': S_ + '000162828026005016/mdlzearningsreleasecontent.htm', 'q3': S_ + '000162828025046750/mdlzearningsreleasecontent.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="mdlzFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('코코아·밀·설탕 등 원자재 헤지 파생상품의 평가손익이 영업이익에 그대로 들어가 분기 이익이 크게 흔들린다 — Q2 2026은 평가이익(세전 $827M)으로 EPS가 $1.20, Q1은 평가손실로 $0.44. '
              '최근 4분기를 합치면 평가손익이 거의 상쇄되지만 5년 PER 이력에는 분기마다 튀는 구간이 섞여 있다. 2024~2025년 코코아 가격 급등으로 이익률이 눌렸다. '
              'SEC 요약 자료에 최신 10-Q가 아직 없어 원문 인라인 XBRL로 채웠다.')
HEALTH_EXTRA = ('Q2 2026 분기 값에는 헤지 평가이익(세전 $827M)이 들어 있다 — 빼면 영업이익률 약 12.0%, 순이익률 약 9.5%, 이자보상배율 약 7.8배로 낮아진다. '
                '현금흐름 모델 값이 낮은 것은 투하자본의 약 94%가 영업권·무형자산(Cadbury 등 인수)이라 자본 수익률이 할인율보다 낮게 계산되기 때문이다.')
PH = ['PEP', 'KO', 'HSY', 'GIS', 'KHC', 'PG']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '식품·음료 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(MDLZ 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·담배·생활용품 제조사와 소매가 섞여 있다. 차트에는 식품·음료 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 유럽 3,377 + 북미 2,633 + 아시아·중동·아프리카 1,971 + 중남미 1,374 = 9,355.
SEG = [('유럽', 3377, '#4f2170'), ('북미', 2633, '#9a72b8'), ('아시아·중동·아프리카', 1971, '#e5a823'), ('중남미', 1374, '#c9b6dd')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:07~16:17 동부 접수) → 다음 거래일. 넣지 않은 8-K: 신용 한도, 임원(COO·CFO), 주총.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 28일 장 마감 뒤 — Q2 2026 실적', '2026-07-29',
     '매출 $9.36B(+4.1%) · 순이익 $1.55B · 희석 EPS $1.20(1년 전 $0.49) — 헤지 평가이익 세전 $827M 포함(회사 조정 EPS $0.73)', 'q2', 'Mondelez 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 장 마감 뒤 — Q1 2026 실적', '2026-04-29',
     '매출 $10.08B · 순이익 $560M · 희석 EPS $0.44(1년 전 $0.31) — 헤지 평가손실 세전 $273M 포함', 'q1', 'Mondelez 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 3일 장 마감 뒤 — Q4 2025 실적', '2026-02-04',
     '매출 $10.50B · 순이익 $665M · 희석 EPS $0.51(1년 전 $1.30) · 2025년 EPS $1.89 — 헤지 평가손실 포함', 'q4', 'Mondelez 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 28일 장 마감 뒤 — Q3 2025 실적', '2025-10-29',
     '매출 $9.74B · 순이익 $743M · 희석 EPS $0.57(1년 전 $0.63)', 'q3', 'Mondelez 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 17, 'mean': 71.12, 'median': 72, 'low': 66, 'high': 75, 'sb': 10, 'b': 5, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-31'


# ── 자동 카드 — 지역 부문 4개(수동 지도, 영업 부문 차원). 원문 대조: Q2 2026 3,377/2,633/1,971/1,374(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"mdlz:EuropeSegmentMember": ["유럽", "#4f2170"], "mdlz:NorthAmericaSegmentMember": ["북미", "#9a72b8"],
             "mdlz:AsiaMiddleEastAndAfricaSegmentMember": ["아시아·중동·아프리카", "#e5a823"], "mdlz:LatinAmericaSegmentMember": ["중남미", "#c9b6dd"]},
 "ignore": []
}
