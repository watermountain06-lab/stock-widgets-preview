# INTU(인튜이트) v2 카드 설정 — 자동 카드(AUTO). 회계연도 7월 31일. 카드 순위 129(시총 127위). 세무(TurboTax·Credit Karma)·소상공인 회계(QuickBooks·Mailchimp) 소프트웨어.
# 출처: SEC XBRL, FY2026 10-K(2026-09-09), 실적 보도자료(Q1~Q4 FY26, 8-K 2.02항 — 모두 장 마감 뒤 접수), 8-K(이사 선임 2025-11-18, 내부자 매도 계획 종료·자사주 가속 2026-03-16,
# 소상공인 부문장 사임 2026-04-28, 구조조정 2026-05-20, 선순위채 2026-06-11), StockAnalysis.
# 엔진 입력(2026-10-18): 단기투자 AvailableForSaleSecuritiesDebtSecuritiesCurrent 2023-01 멈춤($524M) → 재무상태표 "Investments"($2,495M) 태그(EV_TAGS_BY_CIK).
# 감가상각 = Depreciation + AdjustmentForAmortization(인수 무형자산 상각 전체 $659M — 기본 선택은 기타 무형자산 $485M뿐이라 인수 기술 $174M이 빠졌다, DDA_PARTS_BY_CIK).
# 고객 자금(Funds receivable and amounts held for customers $5,038M = 같은 금액의 부채)은 현금·차입금에서 빠진다(엔진 기본, ADP와 같다). 대출 채권(QuickBooks Capital·
# Credit Karma, 보유 $1,468M + 매각 예정 $179M)은 운전자본 안(영업 자산). 4분기 EPS: FY21~FY26 모두 보도자료 값(역산과 $0.02~0.07 차이, Q4_EPS_OVERRIDE).
# FY26 영업현금흐름 $8.8B에는 OBBBA(연구개발비 즉시 비용처리 부활)로 줄어든 법인세 현금 납부 효과가 들어 있다(10-K) — PCR이 낮게 나온다(CHART_NOTE).
CIK = '0000896878'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
FY_ENDS, FY_LABEL = ('2026-07-31', '2025-07-31'), 'FY2026'
VOTES, VERDICT = (1, 1, -1), '적정~저평가'
CO = 'Intuit'
S_ = 'https://www.sec.gov/Archives/edgar/data/896878/'
SEC = S_
TENQ = S_ + '000089687826000037/intu-20260731.htm'; TENQ_NAME = 'FY2026 10-K'
PR = {'q4': S_ + '000089687826000029/fy26q4earningspressrelease.htm', 'q3': S_ + '000089687826000024/fy26q3earningspressrelease.htm',
      'q2': S_ + '000089687826000012/fy26q2earningspressrelease.htm', 'q1': S_ + '000089687825000046/fy26q1earningspressrelease.htm'}
LINKS = {'notes': S_ + '000119312526267866/d159651d8k.htm', 'restructure': S_ + '000089687826000024/intu-20260520.htm',
         'sbg': S_ + '000089687826000020/intu-20260428.htm', 'buyback': S_ + '000089687826000017/intu-20260316.htm'}
FAIRBAND_TITLE = 'id="intuFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 60)
ACT_REASON = ''
NONOP_WHAT = '장기투자'
# 고정 문장(숫자 없음 — 분기마다 고치지 않는다). 성장률·FCF가 일회성으로 부푼 점(Fable 필수 2026-10-18).
MODEL_NOTE = ('5년 매출 성장률에는 Mailchimp 인수(2021년 11월) 첫해 매출이 들어 있어, 기본 시나리오의 출발 성장률이 유기 성장보다 높다 — 최초 연결 편입 효과가 없는 3년 성장률을 쓰는 '
              '낙관 시나리오가 기본보다 낮게 나오는 이유다. 최근 회계연도 영업현금흐름·FCF에는 연구개발비 즉시 비용처리 부활(OBBBA)로 줄어든 법인세 현금 납부 효과가 들어 있다.')
HEALTH_EXTRA = '유동비율에는 고객 자금(결제 처리·급여 대행 — 자산과 부채에 같은 금액)이 들어 있어 실제 지급능력보다 낮게 나온다.'   # 고정 문장
PH = ['CRM', 'MSFT', 'ORCL', 'PANW', 'IBM', 'CRWD']   # ADBE·NOW는 카드 유니버스 배수 값이 없어 차트에서 뺌(fill.py가 멈춘다)
PEER_FILE = None
CHART_CAP, SELF_CAP = {}, {}
CHART_NOTE = {'pcr': ' (INTU FY2026 영업현금흐름에는 연구개발비 즉시 비용처리 부활로 줄어든 법인세 현금 납부 효과가 들어 있다 — 10-K)'}
CHART_TITLES = {'per': '소프트웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': '소프트웨어 PBR 비교', 'psr': '소프트웨어 PSR 비교',
                'pcr': '소프트웨어 PCR(FCF) 비교', 'evebitda': '소프트웨어 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(INTU 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 소프트웨어 6곳만 보인다.')
# 매출(FY2026 10-K 주석 부문 표 연간 − Q3 FY26 10-Q 9개월 = 4분기) — 글로벌 비즈니스 솔루션 12,864 − 9,440 = 3,424, 소비자 8,584 − 7,654 = 930,
# 합 4,354 = 연결 4분기 매출(21,448 − 17,094). 1년 전 4분기 3,013·818. 세금 시즌(2~4월) 뒤라 4분기 소비자 매출이 작다.
SEG = [('글로벌 비즈니스 솔루션(QuickBooks·Mailchimp)', 3424, '#236cff'), ('소비자(TurboTax·Credit Karma)', 930, '#00b9a9')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 보고 부문별(4분기)'
# 손 뉴스: 최신 실적(Q4 FY26, 8/25)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤(같은 날 포함) 손 항목은 없다. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K는 모두 20~21시 접수(장 마감 뒤) → 다음 거래일. 선순위채 8-K 6/11 21:07 → 6/12, 구조조정(Q3 실적 8-K 2.05항) 5/20 20:05 → 5/21,
# 부문장 8-K 4/28 20:08 → 4/29, 자사주 8-K 3/16 20:23 → 3/17, 이사 선임(Q1 실적 8-K 5.02항) 11/20 21:01 → 11/21. 신용 계약 8-K(1/9·1/30)는 넣지 않는다.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 6월 11일 장 마감 뒤 — 선순위채 $1.75B 발행', '2026-06-12',
     '2031년 만기 $750M(연 4.950%) + 2036년 만기 $1.0B(연 5.500%) · 순조달 약 $1.74B · 일반 목적(2026년 만기채 $750M·2027년 만기채 $500M 차환에 쓸 수 있다)', 'notes', 'Intuit 공시 (SEC 8-K)'),
    ('neutral', '2026년 5월 20일 장 마감 뒤 — 구조조정: 정규직 약 17% 감축', '2026-05-21',
     '조직 단순화 · 일부 사업장 폐쇄 검토 · 비용 약 $300M~$340M 예상 · 실제 4분기(5~7월)에 $293M 반영(세전 비용의 주당 환산 $1.08, Q4 보도자료 — 4분기 영업이익률·EPS를 누름) · 같은 날 Q3 실적 발표', 'restructure', 'Intuit 공시 (SEC 8-K)'),
    ('green', '2026년 5월 20일 장 마감 뒤 — Q3 FY26 실적', '2026-05-21',
     '매출 $8.56B(+10%) · 희석 EPS $11.09(1년 전 $10.02)', 'q3', 'Intuit 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 장 마감 뒤 — 소상공인 부문장 사임', '2026-04-29',
     'Marianna Tessel 수석부사장(소상공인 그룹) 5월 31일 사임 · Ashley Still(중견기업 그룹)이 두 그룹을 함께 맡음', 'sbg', 'Intuit 공시 (SEC 8-K)'),
    ('green', '2026년 3월 16일 장 마감 뒤 — 내부자 매도 계획 종료 · 자사주 매입 가속', '2026-03-17',
     '창업자·경영진이 사전 매도 계획(10b5-1)을 모두 종료 · 1월 말 남은 한도 최대 $3.5B까지 매입을 크게 앞당기겠다고 밝힘 · 상반기 매입 $1.8B(+40%)', 'buyback', 'Intuit 공시 (SEC 8-K)'),
    ('green', '2026년 2월 26일 장 마감 뒤 — Q2 FY26 실적', '2026-02-27',
     '매출 $4.65B(+17%) · 희석 EPS $2.48(1년 전 $1.67)', 'q2', 'Intuit 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 20일 장 마감 뒤 — Q1 FY26 실적', '2025-11-21',
     '매출 $3.89B(+18%) · 희석 EPS $1.59(1년 전 $0.70) · 같은 8-K에 Adena Friedman·Bill McDermott 이사 선임(2026년 8월 1일부터)', 'q1', 'Intuit 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 34, 'nt': 24, 'mean': 384.88, 'median': 400, 'low': 290, 'high': 550, 'sb': 15, 'b': 5, 'h': 12, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-18'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(보고 부문 축 2개, 10-K 연간 − Q3 9개월). 원문 대조: 4분기 3,424/930(합 4,354 = 연결), 1년 전 3,013/818(2026-10-18) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "intu:GlobalBusinessSolutionsSegmentMember": [
   "글로벌 비즈니스 솔루션(QuickBooks·Mailchimp)",
   "#236cff"
  ],
  "intu:ConsumerSegmentMember": [
   "소비자(TurboTax·Credit Karma)",
   "#00b9a9"
  ]
 },
 "ignore": []
}
