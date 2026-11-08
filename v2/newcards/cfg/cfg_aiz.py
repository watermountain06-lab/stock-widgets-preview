BUILD = {'overlay': True, 'no_dcf': '보험사라 현금흐름 모델을 쓰지 않는다'}   # CB·PGR과 같은 방식(2026-10-02 사용자 결정)
# AIZ(어슈어런트) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 특종 보험·보증 서비스 — Global Lifestyle(휴대폰 보호·연장 보증·자동차 보증)·Global Housing(대출자 지정 주택보험·세입자 보험) 2부문.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-05 17:15 동부 장 마감 뒤 → 첫 세션 11-06 — 카드는 11-06 장중 가격으로 만들고 매일 실행이 종가로 고친다), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항).
# 엔진 입력(2026-11-06): 차입 = 무담보채 UnsecuredDebt $2,208.7M(DEBT_TOTAL_TAG — 기본 LongTermDebt는 2020-03에 멈춤), 우선주 0(2021 의무전환 우선주 전환 뒤), 비지배지분 0. 단기투자 $300.8M은 보험 운용자산이라 뺌(EV_TAGS_BY_CIK sti — 기본 태그는 2019 멈춤). 운용리스 $73.9M은 연간(10-K)만 있어 낡은 값으로 0.
# 일회성(E54 범주, Fable r1): 창(2021-11~) 안 2022 구조조정 $41.8M(Q4 2022, 세후 약 $0.6/주)이 문턱을 넘을 수 있으나 판정 보류 카드라 입력하지 않았다 — 빼면 2023년 PER 최고 31.2 → 약 27, 현재 백분위 영향 작음. 재해 손실은 매년 반복이라 대상 아님.
# D&A는 부문 조정표에만 있고(Q3 감가상각 $44.3M·인수 무형자산 상각 $17.9M) 요약 자료의 표준 태그로 이어지지 않아 EV/EBITDA는 계산 불가.
NO_DCF_SKEW = True   # 금융 카드 — 현금흐름 칸 쏠림 메모(A0) 없음
CIK = '0001267238'
OP_DISPLAY = (['IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest'], [(['InterestExpenseDebt', 'InterestExpense'], 1)])   # 카드 표시용 영업이익 = 세전이익 + 이자비용(CB와 같다) — 이자 태그는 2024-04부터 InterestExpenseDebt
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Assurant'
S_ = 'https://www.sec.gov/Archives/edgar/data/1267238/'
SEC = S_
TENQ = S_ + '000126723826000046/aiz-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000126723826000043/aiz-20260930exx991pressrel.htm', 'q2': S_ + '000126723826000039/aiz-20260630exx991pressrel.htm',
      'q1': S_ + '000126723826000024/aiz-20260331exx991pressrel.htm', 'q4': S_ + '000126723826000006/aiz-20251231exx991pressrel.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="aizFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (현금흐름 미적용)</span>'
Y2 = (0, 20)
ACT_REASON = '보험사라 재고·매출채권 회전으로 보는 활동성이 맞지 않는다'
NONOP_WHAT = '투자'
PH = ['ALL', 'HIG', 'TRV', 'CINF', 'AIG', 'GL']
PEER_FILE = 'peer_universe/insurers.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '보험 6곳 PER 비교 (점수는 S&P500 보험사 기준)', 'pbr': '보험 PBR 비교', 'psr': '보험 PSR 비교',
                'pcr': '보험 PCR(FCF) 비교', 'evebitda': '보험 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 보험사(손해·종합·생명)보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 보험사 대비 배수 순위 (v2/peer_universe/insurers.json)'
PEER_TIP = ('S&P500 손해·종합·생명보험 16곳 중 AIZ를 뺀 15곳과 배수 순위를 매긴 값이다.', 'AIZ는 보증·기기 보호 수수료 매출이 커서 전통 손해보험사와 매출·자본 구조가 다르다. 차트에는 6곳만 보인다.')
MODEL_NOTE = ('보험사라 현금흐름 내재가치는 계산하지 않아 판정 보류다(자기 이력·동종업 점수는 참고). 주요 사업은 휴대폰 보호·연장 보증·자동차 보증(Global Lifestyle, 3분기 매출의 약 4분의 3)과 '
              '대출자 지정 주택보험·세입자 보험(Global Housing)이다. 3분기 보고 대상 재해 손실은 조정 EBITDA 기준 약 $20M이다. 차입금은 무담보채 $2.2B다. 3분기 채권 평가손실(기타포괄손익 −$302M)로 자본이 줄어 PBR이 5년 중 가장 높은 쪽으로 보인다 — 9월 말 기타포괄손익 누계 −$902M을 빼고 보면 그만큼 낮아진다.')
# 매출(Q3 2026 10-Q 부문 주석) — Connected Living 1,583.5 + Global Automotive 1,077.6 + Homeowners 600.0 + Renters and Other 144.9 = 3,406.0,
# 나머지 123.5(순투자수익 147.2 − 실현손실 25.3 + 기타 1.6)는 SEG_ADJ — 합 3,529.5.
SEG = [('기기 보호(Connected Living)', 1583.5, '#003b71'), ('자동차 보증', 1077.6, '#4f8fcc'), ('주택보험', 600.0, '#b0cde8'), ('세입자·기타', 144.9, '#8a96a3')]
SEG_ADJ = 123.5
SEG_TITLE = '매출 구성 — 상품군별(Q3 2026)'
# 손 뉴스: 실적 3건(GAAP 순이익, 희석 EPS, 조정 EPS). 최신 Q3 2026(11-03 장 마감 뒤)은 news_auto가 붙인다.
# 반응일: Q2·Q4는 16시대 접수 → 다음 거래일. Q1 8-K는 2026-05-05 14:01 동부 접수 → 같은 날.
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('green', '2026년 8월 4일 장 마감 뒤 — Q2 2026 실적·연간 전망 상향', '2026-08-05',
     '매출 $3.45B(+9.4%) · 순이익 $298.6M · 희석 EPS $5.95(1년 전 $4.56) · 조정 EPS $6.41 — 다음 날 주가 +7.2%', 'q2', 'Assurant 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 5일 — Q1 2026 실적·연간 전망 상향', '2026-05-05',
     '매출 $3.42B(+11.3%) · 순이익 $274.1M · 희석 EPS $5.41(1년 전 $2.83) · 조정 EPS $5.95 — 당일 주가 +3.5%', 'q1', 'Assurant 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 10일 장 마감 뒤 — Q4 2025 실적', '2026-02-11',
     '매출 $3.35B(+7.9%) · 순이익 $225.2M · 희석 EPS $4.41(1년 전 $3.87) · 조정 EPS $5.61 — 다음 날 주가 −8.6%', 'q4', 'Assurant 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 7, 'nt': 6, 'mean': 330, 'median': 331, 'low': 300, 'high': 355, 'sb': 4, 'b': 3, 'h': 0, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


POST = [r"""
h = h.replace('</span> 종가 기준</span>', '</span> 장중 기준</span>', 1)   # 10-Q가 11-05 장 마감 뒤라 11-06 장중 가격으로 만들었다 — 매일 실행이 종가로 고친다
h = h.replace('부문 간 거래·조정 +$', '순투자수익·기타 +$')   # 상품군 합 밖의 나머지는 순투자수익(실현손실 차감)이다
import re as _re5
h = _re5.sub(r'(차입금 \$[\d.,]+[BM], )현금·단기투자 ', r'\1현금(보험 운용 단기투자 제외) ', h)   # 단기투자는 보험 운용자산이라 뺐다(Codex r1 2026-11-06)
h = h.replace("+ `현금·단기투자 ${B(N.cash + N.sti)}`", "+ `현금(보험 운용 단기투자 제외) ${B(N.cash + N.sti)}`")
"""]


# ── 자동 카드 — 부문 지도(손 작성: 상품군 매출은 회사 고유 개념 aiz:NetEarnedPremiumsFeesandOtherIncome × SubsegmentsAxis, 부문 축은 free_axes.
#    원문 대조: Q3 2026 10-Q 부문 주석 1,583.5/1,077.6/600.0/144.9, 1년 전 1,357.2/1,049.0/553.9/149.0, 2026-11-06) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "aiz:NetEarnedPremiumsFeesandOtherIncome"
 ],
 "axis": "us-gaap:SubsegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "free_axes": ["us-gaap:StatementBusinessSegmentsAxis"],
 "members": {
  "aiz:ConnectedLivingMember": ["기기 보호(Connected Living)", "#003b71"],
  "aiz:GlobalAutomotiveMember": ["자동차 보증", "#4f8fcc"],
  "aiz:HomeownersMember": ["주택보험", "#b0cde8"],
  "aiz:RentersAndOtherMember": ["세입자·기타", "#8a96a3"]
 },
 "ignore": []
}
