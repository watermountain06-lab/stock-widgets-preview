BUILD = {'company_tags': [('bro:MarkToMarketOfEscrowLiability', 'MarkToMarketOfEscrowLiabilityBro')]}   # 빌린 이름 — DERIVED_OPINC가 영업이익에서 뺀다(2026-11-05)
# BRO(브라운 앤 브라운) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일(submissions fiscalYearEnd "0119"는 오기). 보험 중개 — 리테일·전문 유통(Programs + Wholesale, 2025 Q3 재편) 2개 부문.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-26 17:05 동부 장 마감 뒤 → 첫 세션 10-27), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 모두 월요일 17시 무렵 장 마감 뒤 → 다음 거래일 반응). 사전 조사 scratchpad pre/BRO.md.
# 엔진 입력(2026-11-05): 손익계산서에 영업이익 줄이 없어 합성 — 세전이익 + 이자비용(DERIVED_OPINC, HCA 규칙, 이자 태그 2024-06에 InterestExpense → InterestExpenseNonoperating).
# 감가상각 = Depreciation + AdjustmentForAmortization(DDA_PARTS_BY_CIK). 단기투자 태그는 2024-12 뒤 없음(EV_TAGS sti []). 수탁 현금 $2,442M·수탁 채권 $1,234M = 수탁 부채 $3,676M(회사 고유 태그)은 엔진 현금 밖.
# Accession Risk Management 인수(2025-08-01 종결, 대가 $9,608M — 2025-06 주식 공모 43.1백만 주·채권 $4.2B): 1년 전 대비 매출·이익 증가 대부분이 인수 몫(Q3 2026 유기 성장 1.2%).
# 희석 EPS는 에스크로 주식 평가이익(비과세·비현금, 최근 4분기 +$145M)을 빼고 에스크로 주식을 더한 값이라 순이익 ÷ 주식 수보다 낮다(Q3 0.67 대 0.73).
# 일회성 시험(E54, 2026-11-05 scratchpad bro_e54/): 에스크로 평가손익을 영업 밖으로 뺀 정의(사용자 결정 — DERIVED_OPINC + company_tags)로 (+1, +1, −2) 적정 —
# 11-05 종가 $74.38 기준 자기 87.8·동종업 73.0·현금흐름 기본 $47.99(1.55배). 인수·통합 비용(Q4 2025 27·Q1 26·Q2 31·Q3 36)·earn-out(7·5·−40·27)은 E54 장치 범주 밖이라
# 빼지 않는다(2026-11-05 사용자 결정 — 일회성 시험을 장치 규칙(6종·반복 제외)으로 통일). 장치 범주인 처분 손익(1·−1·1·0)은 문턱 아래. 처음엔 11-04 종가($73.90)에서 통합 비용을 빼면 1.483배로 표가 바뀌어 보류했었다.
# 이력 창 안 2023 Q4 사업 매각이익 $135M(세후 EPS 약 0.38, 당시 TTM의 12% — Codex r1)은 처분 줄이 8분기 중 7개에 있어 장치 반복 규칙(r16)으로 빠지지 않는다(Fable r1). 뺐더라도 자기 점수가 오르는 쪽이라 표 불변. 가격은 11-05 종가 $74.38(첫 빌드는 장중 $75.81이었다, Codex r1).
# 주식 수: 엔진은 표지 331,691,829주(10-23)를 쓴다. 재무상태표 327M주는 에스크로 주식(약 4.43M주)을 뺀 수 — 시총 1.4% 차이, 표 영향 없음(Fable r1).
CIK = '0000079282'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, -1), '적정~저평가'
CO = 'Brown & Brown'
S_ = 'https://www.sec.gov/Archives/edgar/data/79282/'
SEC = S_
TENQ = S_ + '000119312526432146/bro-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000119312526432142/bro-ex99_1.htm', 'q2': S_ + '000119312526318245/bro-ex99_1.htm',
      'q1': S_ + '000119312526182375/bro-ex99_1.htm', 'q4': S_ + '000119312526022760/bro-ex99_1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="broFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (15, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('손익계산서에 영업이익 줄이 없어 세전이익 + 이자비용으로 영업이익을 만들고, Accession 인수 에스크로 주식 평가손익(자기 주가에 연동된 부채의 재측정, 비현금·비과세)은 영업 밖으로 뺀다. '
              '인수·통합 비용(최근 4분기 $120M)과 earn-out 변동은 일회성 조정 범주(손상·매각·소송·계약 해지·IPR&D·구조조정) 밖이라 이익에 그대로 두었다 — 빼면 현금흐름 기본 가치가 약 4% 올라간다. '
              '2025년 8월 Accession 인수로 1년 전 대비 매출·이익 증가의 대부분은 인수 몫이다(2026년 3분기 유기 성장 1.2%). '
              '희석 EPS는 에스크로 평가이익을 빼고 에스크로 주식을 더한 값이라 순이익 ÷ 주식 수보다 낮다. 비교 종목은 S&P500 보험 중개사 4곳과 결제·거래소·금융 데이터 회사다.')
HEALTH_EXTRA = '유동비율·부채비율에는 고객 수탁 자산과 수탁 부채(같은 금액)가 들어 있어 실제 지급능력보다 나쁘게 나온다.'
PH = ['AJG', 'AON', 'MRSH', 'WTW', 'SPGI', 'MCO']
PEER_FILE = 'peer_universe/brokers_fees.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '보험 중개·금융 데이터 6곳 PER 비교 (점수는 중개사 + 결제·거래소·데이터 기준)', 'pbr': '보험 중개·금융 데이터 PBR 비교', 'psr': '보험 중개·금융 데이터 PSR 비교',
                'pcr': '보험 중개·금융 데이터 PCR(FCF) 비교', 'evebitda': '보험 중개·금융 데이터 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 보험 중개사와 결제·거래소·금융 데이터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 보험 중개 + 결제·거래소·금융 데이터 대비 배수 순위 (v2/peer_universe/brokers_fees.json)'
PEER_TIP = ('S&P500 보험 중개사(BRO 제외 4곳)와 결제·거래소·금융 데이터 회사(수수료로 버는 자산 경량 서비스)와 배수 순위를 매긴 값이다 — 중개사만으로는 비교 표본(8곳)이 모자란다.',
            '결제 처리·카드 네트워크·거래소가 섞여 있어 성장·마진 구조가 다르다. 차트에는 보험 중개·금융 데이터 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 표, Revenues) — 리테일 978 + 전문 유통 739 = 1,717, 본사 기타 8은 SEG_ADJ — 합 1,725.
SEG = [('리테일', 978, '#003a70'), ('전문 유통(프로그램·도매)', 739, '#5b8db8')]
SEG_ADJ = 8
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: Q3 2026 실적(10/26)은 news_auto가 SEC 숫자로 붙인다. 반응일: 장 마감 뒤 발표 → 다음 거래일.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('green', '2026년 7월 27일 장 마감 뒤 — Q2 2026 실적', '2026-07-28',
     '매출 $1.68B(+30.4%, 인수 포함) · 희석 EPS $0.84(1년 전 $0.78) · 조정 EPS $1.07 — 다음 날 주가 +5.7%', 'q2', 'Brown & Brown 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 27일 장 마감 뒤 — Q1 2026 실적', '2026-04-28',
     '매출 $1.90B(+35.4%, 인수 포함) · 희석 EPS $1.06(1년 전 $1.15) · 조정 EPS $1.39 — 다음 날 주가 −4.5%', 'q1', 'Brown & Brown 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 26일 장 마감 뒤 — Q4 2025 실적', '2026-01-27',
     '매출 $1.61B(+35.7%, 인수 포함) · 희석 EPS $0.59(1년 전 $0.73) · 조정 EPS $0.93 — 다음 날 주가 −6.9%', 'q4', 'Brown & Brown 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 21, 'nt': 16, 'mean': 74.06, 'median': 75, 'low': 55, 'high': 85, 'sb': 4, 'b': 3, 'h': 13, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(영업 부문 Revenues, 손 표와 일치, 2026-11-05) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:Revenues"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "bro:RetailSegmentMember": [
   "리테일",
   "#003a70"
  ],
  "bro:SpecialtyDistributionMember": [
   "전문 유통(프로그램·도매)",
   "#5b8db8"
  ]
 },
 "ignore": []
}
