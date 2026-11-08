BUILD = {'overlay': True, 'no_dcf': '손해보험사라 현금흐름 모델을 쓰지 않는다', 'company_tags': [('wrb:SeniorNotesAndOtherDebt', 'SeniorNotesWrb'), ('us-gaap:OtherLiabilities', 'SubDebtWrb', '2025-04-01')]}   # CB·PGR과 같은 방식(2026-10-02 사용자 결정)
# WRB(W. R. 버클리) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 전문 손해보험(보험·재보험·특종).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-02 16:15 동부 장 마감 뒤 → 첫 세션 11-03), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 모두 16시대 장 마감 뒤 → 다음 거래일). 사전 조사 scratchpad pre/WRB.md.
# 엔진 입력(2026-11-05): 차입 = 선순위채 $1,827.9M(회사 고유 태그 wrb:SeniorNotesAndOtherDebt, company_tags → SeniorNotesWrb). 후순위채 $1,011.1M은 2025-03부터 OtherLiabilities로 잘못 붙어(기타부채와 태그가 뒤바뀜)
# DEBT_TOTAL_TAG 튜플로 날짜를 가른다(company_tags 시작일 2025-04-01 → SubDebtWrb) — 차입 $2,838.9M. 2025-12-31(10-K) 한 시점은 $3,554M으로 남는다(이력 값, 이 카드의 EV/EBITDA는 계산 불가라 영향 없음). 설비투자 태그는 2019에 멈춤(회사 고유 순액 태그), 감가상각 줄 없음 → PCR·EV/EBITDA 계산 불가.
# 주식 수 두 기준: 유통 371.5M(PBR·시총) vs EPS 391.3M(그랜터 트러스트 17.4M 포함).
NO_DCF_SKEW = True   # 금융 카드 — 현금흐름 칸 쏠림 메모(A0) 없음
CIK = '0000011544'
OP_DISPLAY = (['IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest'], [(['InterestExpense'], 1)])   # 카드 표시용 영업이익 = 세전이익 + 이자비용(CB와 같음)
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, 0), '판정 보류'
CO = 'W. R. Berkley'
S_ = 'https://www.sec.gov/Archives/edgar/data/11544/'
SEC = S_
TENQ = S_ + '000001154426000048/wrb-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000001154426000046/wrb93020268-kex991.htm', 'q2': S_ + '000001154426000033/wrb63020268-kex991.htm', 'q1': S_ + '000001154426000008/wrb33120268-kex991.htm', 'q4': S_ + '000001154426000003/wrb123120258-kex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="wrbFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (현금흐름 미적용)</span>'
Y2 = (0, 40)
ACT_REASON = '보험사라 재고·매출채권 회전으로 보는 활동성이 맞지 않는다'
NONOP_WHAT = '투자'
PH = ['CB', 'TRV', 'ACGL', 'CINF', 'HIG', 'ALL']
PEER_FILE = 'peer_universe/insurers.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '보험 6곳 PER 비교 (점수는 S&P500 보험사 기준)', 'pbr': '보험 PBR 비교', 'psr': '보험 PSR 비교',
                'pcr': '보험 PCR(FCF) 비교', 'evebitda': '보험 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 보험사(손해·종합·생명)보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 보험사 대비 배수 순위 (v2/peer_universe/insurers.json)'
PEER_TIP = ('S&P500 손해·종합·생명보험 15곳(WRB 제외)과 배수 순위를 매긴 값이다.', '생명보험사는 장부가·매출 구조가 달라 PBR·PSR 비교가 거칠다. 차트에는 손해보험 6곳만 보인다.')
MODEL_NOTE = ('보험사라 현금흐름 내재가치는 계산하지 않아 판정 보류다(자기 이력·동종업 점수는 참고). 차입금 $2.8B은 선순위채 $1.8B와 후순위채 $1.0B다. 3분기 합산비율은 90.8%다.'
              'PER은 EPS(분기 가중평균, 그랜터 트러스트 주식 포함 391M주) 기준이고 PBR·시총은 분기말 유통 주식 372M주 기준이다. 2026년 6월 창업자 William R. Berkley가 별세했고 미쓰이스미토모가 지분 12.5% 넘게 사들였다.')
SEG = [('순보험료 수익', 3213.6, '#00205b'), ('투자 수익', 383.5, '#6d8fbf')]
SEG_ADJ = 141.67   # 비보험 사업 매출·투자 손익
SEG_TITLE = '매출 구성 — 수익 종류별(Q3 2026)'
# 손 뉴스: Q3 2026 실적 8-K를 news_auto가 실적으로 알아보지 못해(빈 목록) 손 항목으로 쓴다. 반응일은 발표 시각 기준.
NEWS_RANGE = '2026.01 ~ 2026.11'
NEWS = [
    ('red', '2026년 10월 19일 장 마감 뒤 — Q3 2026 실적', '2026-10-20',
     '순이익 $446M · 희석 EPS $1.14(1년 전 $1.28) · 영업 EPS $1.17 · 합산비율 90.8% — 다음 날 주가 −1.3%', 'q3', 'W. R. Berkley 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 20일 장 마감 뒤 — Q2 2026 실적', '2026-07-21',
     '순이익 $452M · 희석 EPS $1.15(1년 전 $1.00) · 영업 EPS $1.27 — 다음 날 주가 −0.8%', 'q2', 'W. R. Berkley 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 21일 장 마감 뒤 — Q1 2026 실적', '2026-04-22',
     '순이익 $515M · 희석 EPS $1.31(1년 전 $1.04) · 영업 EPS $1.30 — 다음 날 주가 +3.2%', 'q1', 'W. R. Berkley 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 26일 장 마감 뒤 — Q4 2025 실적', '2026-01-27',
     '순이익 $450M · 희석 EPS $1.13(1년 전 $1.44) · 영업 EPS $1.13 — 다음 날 주가 +0.5%', 'q4', 'W. R. Berkley 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 18, 'nt': 13, 'mean': 70.15, 'median': 69, 'low': 51, 'high': 83, 'sb': 2, 'b': 0, 'h': 9, 's': 3, 'ss': 4}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 지도(손 표와 일치, 2026-11-05) ──
AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {
  "us-gaap:PremiumsEarnedNet": [
   "순보험료 수익",
   "#00205b"
  ],
  "us-gaap:NetInvestmentIncome": [
   "투자 수익",
   "#6d8fbf"
  ]
 },
 "ignore": []
}
