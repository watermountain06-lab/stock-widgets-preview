BUILD = {'overlay': True, 'no_dcf': '손해보험사라 현금흐름 모델을 쓰지 않는다', 'company_tags': [('eg:InterestFeeAndBondIssueCostAmortizationExpense', 'InterestExpense')]}   # CB·PGR과 같은 방식(2026-10-02 사용자 결정)
# EG(에베레스트 그룹) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 재보험(트리티)·글로벌 도매·특종 보험, 버뮤다 법인.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-30 16:21 동부 장 마감 뒤 → 첫 세션 11-02), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 모두 수요일 16시대 장 마감 뒤 → 다음 거래일). 사전 조사 scratchpad pre/EG.md.
# 엔진 입력(2026-11-05): 현금 Cash $987M(기본 태그는 2018 멈춤), 단기투자 $3,055M은 보험 운용자산이라 뺌(TRV·ALL 선례), 차입 = 선순위채 2,353 + 후순위채 218 + FHLB 1,019 = $3,590M(DEBT_TOTAL_TAG — 기본은 2011년 $40M),
# 이자비용은 회사 고유 태그(eg:InterestFeeAndBondIssueCostAmortizationExpense, company_tags → InterestExpense — us-gaap 태그는 2020 멈춤). 현금흐름표에 설비투자·감가상각 줄이 없어 PCR·EV/EBITDA는 계산 불가(정상).
NO_DCF_SKEW = True   # 금융 카드 — 현금흐름 칸 쏠림 메모(A0) 없음
CIK = '0001095073'
OP_DISPLAY = (['IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest'], [(['InterestExpense'], 1)])   # 카드 표시용 영업이익 = 세전이익 + 이자비용(CB와 같음)
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, 0), '판정 보류'
CO = 'Everest'
S_ = 'https://www.sec.gov/Archives/edgar/data/1095073/'
SEC = S_
TENQ = S_ + '000109507326000043/eg-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000109507326000041/everest3q26earningsrelease.htm', 'q2': S_ + '000109507326000029/everest2q26earningsrelease.htm', 'q1': S_ + '000109507326000019/everest1q26earningsrelease.htm', 'q4': S_ + '000109507326000003/everest4q25earningsrelease.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="egFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (현금흐름 미적용)</span>'
Y2 = (0, 40)
ACT_REASON = '보험사라 재고·매출채권 회전으로 보는 활동성이 맞지 않는다'
NONOP_WHAT = '투자'
PH = ['ACGL', 'CB', 'TRV', 'WRB', 'AIG', 'HIG']
PEER_FILE = 'peer_universe/insurers.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '보험 6곳 PER 비교 (점수는 S&P500 보험사 기준)', 'pbr': '보험 PBR 비교', 'psr': '보험 PSR 비교',
                'pcr': '보험 PCR(FCF) 비교', 'evebitda': '보험 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 보험사(손해·종합·생명)보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 보험사 대비 배수 순위 (v2/peer_universe/insurers.json)'
PEER_TIP = ('S&P500 손해·종합·생명보험 16곳(EG 제외)과 배수 순위를 매긴 값이다.', '생명보험사는 장부가·매출 구조가 달라 PBR·PSR 비교가 거칠다. 차트에는 손해보험 6곳만 보인다.')
MODEL_NOTE = ('보험사라 현금흐름 내재가치는 계산하지 않아 판정 보류다(자기 이력·동종업 점수는 참고). 2025년 말 소매 상업보험 갱신권을 팔았고 4개국 소매 법인을 팔고 있어(캐나다는 10월 1일 완료, 콜롬비아·멕시코·칠레는 진행 중) 보험료가 줄고 있다(3분기 원수보험료 −14.5%) — 과거 매출 성장률은 앞으로와 다르다. 3분기 합산비율은 107.1%로 보험 영업은 적자였고 순투자수익이 이익을 받쳤다.'
              '2025년 4분기 매출에는 갱신권 매각 이익($259M)이 들어 있다. 회사의 순영업이익 정의가 2026년 3분기에 바뀌어 그 전 분기 영업 EPS와 바로 비교되지 않는다. 3분기에 재보험 캐주얼티 준비금을 보강했다(전기 손해 불리한 변동 $268M).')
SEG = [('순보험료 수익', 3156, '#002f6c'), ('투자 수익', 634, '#5b8cc2')]
SEG_ADJ = -77   # 투자 손실 −68 등
SEG_TITLE = '매출 구성 — 수익 종류별(Q3 2026)'
# 손 뉴스: Q3 2026 실적 8-K를 news_auto가 실적으로 알아보지 못해(빈 목록) 손 항목으로 쓴다. 반응일은 발표 시각 기준.
NEWS_RANGE = '2026.01 ~ 2026.11'
NEWS = [
    ('green', '2026년 10월 28일 장 마감 뒤 — Q3 2026 실적', '2026-10-29',
     '순이익 $233M · 희석 EPS $6.12(1년 전 $6.09) · 영업 EPS $7.62(새 정의) · 재보험 캐주얼티 준비금 보강 — 다음 날 주가 +3.5%', 'q3', 'Everest 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 29일 장 마감 뒤 — Q2 2026 실적', '2026-07-30',
     '순이익 $559M · 희석 EPS $14.22(1년 전 $16.10) · 영업 EPS $14.85 — 다음 날 주가 −4.7%', 'q2', 'Everest 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 29일 장 마감 뒤 — Q1 2026 실적', '2026-04-30',
     '순이익 $653M · 희석 EPS $16.21(1년 전 $4.90) · 영업 EPS $16.08 — 다음 날 주가 +3.7%', 'q1', 'Everest 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 4일 장 마감 뒤 — Q4 2025 실적', '2026-02-05',
     '순이익 $446M · 희석 EPS $10.77(1년 전 −$13.96) · 영업 EPS $13.26 — 다음 날 주가 −2.3%', 'q4', 'Everest 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 17, 'nt': 12, 'mean': 421.33, 'median': 428, 'low': 376, 'high': 475, 'sb': 3, 'b': 4, 'h': 10, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-05'


# ── 자동 카드 — 부문 지도(손 표와 일치, 2026-11-05) ──
AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {
  "us-gaap:PremiumsEarnedNet": [
   "순보험료 수익",
   "#002f6c"
  ],
  "us-gaap:NetInvestmentIncome": [
   "투자 수익",
   "#5b8cc2"
  ]
 },
 "ignore": []
}
