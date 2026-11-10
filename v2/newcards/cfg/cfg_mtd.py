# MTD(메틀러 토레도) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 정밀 계측기(실험실 저울·분석 기기, 산업 계량, 식품 검사)와 서비스.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-31), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/MTD.md.
# 엔진 입력(2026-10-25): 영업이익 = 세전이익 + 이자비용(DERIVED_OPINC — 손익계산서에 영업이익 줄이 없다). 차입금 = 1년 안 $67.3M + 장기 $2,044.7M = $2,112.0M(DEBT_TOTAL_TAG).
# 주식 수는 표지 값 20.04M(cover_shares + EXCLUDE_TAGS CommonStockSharesOutstanding — 21.68M은 자사주를 빼지 않은 낡은 값, Fable r1). D&A = 감가상각 + 현금흐름표 상각(DDA_PARTS_BY_CIK). 자본이 사실상 0(자사주 $10.3B)이라 PBR·ROE는 의미 없음.
# 일회성: Q2 2026 관세 환급(+EPS 0.92)·인수 조건부 대가(−0.31) — 순 +0.61로 최근 4분기 EPS의 약 1.4%.
BUILD = {'cover_shares': True}
CIK = '0001037646'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Mettler-Toledo'
S_ = 'https://www.sec.gov/Archives/edgar/data/1037646/'
SEC = S_
TENQ = S_ + '000103764626000051/mtd-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000103764626000049/ex-991mtd8xkq22026.htm', 'q1': S_ + '000103764626000019/ex-991mtd8xkq12026.htm',
      'q4': S_ + '000103764626000008/ex-991mtd8xkq42025.htm', 'q3': S_ + '000103764625000056/ex-991mtd8xkq32025.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="mtdFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (15, 35)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('손익계산서에 영업이익 줄이 없어 세전이익에 이자비용을 더한 값을 영업이익으로 쓴다 — 구조조정과 연금·이자수익 같은 기타 손익도 들어 있어 회사의 영업이익 정의와 조금 다르다. '
              '자사주를 꾸준히 사들여 장부 자본이 사실상 0이라 PBR·ROE는 의미가 없다. '
              'Q2 2026에는 관세 환급(일회성)이 원가를 낮추고 고객 환급분이 매출을 줄였다.')
PH = ['TMO', 'A', 'DHR', 'WAT', 'IQV', 'RVTY']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '생명과학 도구 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': '생명과학 도구 PBR 비교', 'psr': '생명과학 도구 PSR 비교',
                'pcr': '생명과학 도구 PCR(FCF) 비교', 'evebitda': '생명과학 도구 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(MTD 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·유통·생명과학 도구가 섞여 있다. 차트에는 생명과학 도구 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 외부 고객) — 미국 352.5 + 스위스 56.5 + 서유럽 227.0 + 중국 187.2 + 기타 204.1 = 1,027.3.
SEG = [('미국', 352.5, '#0b4ea2'), ('서유럽', 227.0, '#3f7cc6'), ('기타 지역', 204.1, '#7fa8dc'), ('중국', 187.2, '#d24a3b'), ('스위스', 56.5, '#b9cfee')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문(지역)별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다). 반응일: 장 마감 뒤 발표 → 다음 거래일. 넣지 않은 8-K: 임원 계약·이사 선임·주총·LTI.
NEWS_RANGE = '2025.11 ~ 2026.07'
NEWS = [
    ('green', '2026년 7월 30일 — Q2 2026 실적', '2026-07-31',
     '매출 $1.03B(1년 전 $983M) · 순이익 $233M · 희석 EPS $11.55(1년 전 $9.76) — 관세 환급 +$0.92, 인수 조건부 대가 −$0.31 포함', 'q2', 'Mettler-Toledo 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 7일 — Q1 2026 실적', '2026-05-08',
     '매출 $947M · 순이익 $170M · 희석 EPS $8.33(1년 전 $7.81)', 'q1', 'Mettler-Toledo 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 5일 — Q4 2025 실적', '2026-02-06',
     '매출 $1.13B · 순이익 $286M · 희석 EPS $13.98(1년 전 $11.96) — 일회성 세금 이익(주당 $0.95) 포함', 'q4', 'Mettler-Toledo 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 6일 — Q3 2025 실적', '2025-11-07',
     '매출 $1.03B · 순이익 $218M · 희석 EPS $10.57(1년 전 $9.96)', 'q3', 'Mettler-Toledo 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 13, 'nt': 15, 'mean': 1496.93, 'median': 1515, 'low': 1180, 'high': 1930, 'sb': 4, 'b': 1, 'h': 6, 's': 0, 'ss': 2}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 5개(수동 지도). 원문 대조: Q2 2026 352.5/56.5/227.0/187.2/204.1(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"mtd:USOperationsMember": ["미국", "#0b4ea2"], "mtd:WesternEuropeanOperationsMember": ["서유럽", "#3f7cc6"], "mtd:OtherOperationsMember": ["기타 지역", "#7fa8dc"],
             "mtd:ChineseOperationsMember": ["중국", "#d24a3b"], "mtd:SwissOperationsMember": ["스위스", "#b9cfee"]},
 "ignore": []
}
