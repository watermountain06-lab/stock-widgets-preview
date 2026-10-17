# PSX(필립스 66) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 106.
# 출처: SEC XBRL(+ 설비투자 회사 고유 태그), Q2 2026 10-Q(2026-08-05), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항), 8-K(WRB 지분 인수 발표 2025-09-09,
# 364일 대출 $2.25B 2026-03-18), StockAnalysis.
# 엔진 입력(2026-10-13): 영업이익 줄이 없어 세전 + 이자·차입 비용(COP·XOM 규칙, DERIVED_OPINC — 지분법 이익·처분 손익·기타 수익은 영업),
# 세전이익은 회사 태그 IncomeLossIncludingPortionAttributableToNoncontrollingInterest(build_dcf PRETAX_TAG_BY_CIK), 차입금 = 단기 + 장기(DebtCurrent + LongTermDebtAndCapitalLeaseObligations), 분기 이자비용(interest_extra),
# 4분기 EPS 보도자료 값(2025 $7.17·2024 $0.01). 설비투자는 "Capital expenditures and investments"(지분법 투자 포함, COP와 같은 처리).
# 2025년 4분기 이익에 독일·오스트리아 소매 사업 일부 처분 이익(M&S 특별 항목 세전 $2.0B)이 들어 최근 4분기 영업이익·EV/EBITDA에 반영된다.
BUILD = {'company_tags': [('psx:CapitalExpendituresAndInvestments', 'PaymentsToAcquireProductiveAssets')]}
CIK = '0001534701'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Phillips 66'
S_ = 'https://www.sec.gov/Archives/edgar/data/1534701/'
SEC = S_
TENQ = S_ + '000153470126000032/psx-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q1': S_ + '000153470126000020/psx-2026331_ex991.htm', 'q4': S_ + '000153470126000003/psx-20251231_ex991.htm',
      'q3': S_ + '000153470125000153/psx-20250930_ex991.htm'}
LINKS = {'prelim': S_ + '000153470126000015/psx-2026_q1prexrelease.htm', 'notes': S_ + '000119312525207435/d25054d8k.htm', 'wrb': S_ + '000153470126000032/psx-20260630.htm', 'loan': S_ + '000119312526114070/d20718d8k.htm'}
FAIRBAND_TITLE = 'id="psxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 최근 4분기 EPS에는 4분기 $7.17(소매 사업 처분 이익 포함)과 2분기 $9.55가 들어 있다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
CAPEX_LABEL = '설비투자·투자'   # psx:CapitalExpendituresAndInvestments = 설비투자 + 지분법 투자(상반기 $1,308M)
ACT_REASON = ''
NONOP_WHAT = '투자'
PH = ['VLO', 'MPC', 'XOM', 'CVX', 'COP', 'OXY']
PEER_FILE = 'peer_universe/energy.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '정유·석유 6곳 PER 비교 (점수는 S&P500 에너지 기준)', 'pbr': '정유·석유 PBR 비교', 'psr': '정유·석유 PSR 비교',
                'pcr': '정유·석유 PCR(FCF) 비교', 'evebitda': '정유·석유 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 에너지 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 에너지 대비 배수 순위 (v2/peer_universe/energy.json)'
PEER_TIP = ('S&P500 에너지(PSX 제외)와 배수 순위를 매긴 값이다.',
            '통합 석유사·탐사생산·정유·장비·가스관 회사가 섞여 있다. 정유사는 매출이 커 PSR이 낮게 나온다. 차트에는 정유·석유 6곳만 보인다.')
# 부문(Q2 2026 10-Q 부문 표, 외부 고객 매출) — 미드스트림 5,231 + 정유 13,618 + 판매·특수 31,297 + 재생 연료 849 + 본사 9 = 51,004.
# 화학(CPChem 지분법)은 매출이 없다. 본사·기타($9M)는 뺀다.
SEG = [('판매·특수제품', 31297, '#e2241b'), ('정유', 13618, '#5a5a5a'), ('미드스트림', 5231, '#1f6fb2'), ('재생 연료', 849, '#6aa84f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(외부 고객, 본사 $9M 제외)'
# 손 뉴스: Q2 2026 실적(8/5)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤 손 항목(8/20 매출채권 유동화 변경, 9/29 정유 부문장 은퇴 통보)은 넣지 않았다(README).
NEWS_RANGE = '2025.09 ~ 2026.08'
NEWS = [
    ('green', '2026년 4월 29일 — Q1 2026 실적', '2026-04-29',
     '순이익 $207M · 희석 EPS $0.51(1년 전 $1.18)', 'q1', 'Phillips 66 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 6일 — 1분기 예비 실적 공시', '2026-04-06',
     '헤지 파생상품 세전 평가손실 약 $900M · 파생상품 현금 담보 순유출 약 $3B, 약정 신용한도 인출', 'prelim', 'Phillips 66 공시 (SEC 8-K)'),
    ('neutral', '2026년 3월 18일 — 364일 대출 $2.25B 약정', None,
     'Mizuho 등 대주단, Phillips 66 보증', 'loan', 'Phillips 66 공시 (SEC 8-K)'),
    ('green', '2026년 2월 4일 — Q4 2025 실적', '2026-02-04',
     '순이익 $2.9B · 희석 EPS $7.17(1년 전 $0.01) — 특별 항목 세전 $2.1B(독일·오스트리아 소매 사업 일부 처분 이익 $2.0B 포함) 포함 · 2025년 주주환원 $3.1B', 'q4', 'Phillips 66 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 29일 — Q3 2025 실적', '2025-10-29',
     '순이익 $133M · 희석 EPS $0.32(1년 전 $0.82) — 정유 부문 특별 항목 세전 −$948M 포함', 'q3', 'Phillips 66 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 1일 — WRB Refining 나머지 지분 50% 인수 완료', '2025-10-01',
     'Cenovus로부터 현금 $1.3B(9월 9일 계약 발표) · 이날부터 WRB(Wood River·Borger 정유) 100% 연결 — Q2 2026 10-Q 인수 주석', 'wrb', 'Phillips 66 10-Q (SEC)'),
    ('neutral', '2025년 9월 16일 — 후순위채 $2.0B 발행 계약', None,
     '2056년 만기 A종 $1.0B(연 5.875%)·B종 $1.0B(연 6.200%)', 'notes', 'Phillips 66 공시 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 18, 'mean': 273.83, 'median': 284, 'low': 151, 'high': 345, 'sb': 8, 'b': 3, 'h': 7, 's': 0, 'ss': 2}
ANALYST_ASOF = '2026-10-17'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-Q 부문 표 외부 고객 매출 Q2 2026 31,297/13,618/5,231/849, 본사 9, 화학 0(CPChem 지분법) — 화학은 ignore(2026-10-13) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "psx:MarketingSpecialitySegmentMember": [
   "판매·특수제품",
   "#e2241b"
  ],
  "psx:RefiningSegmentMember": [
   "정유",
   "#5a5a5a"
  ],
  "psx:MidstreamSegmentMember": [
   "미드스트림",
   "#1f6fb2"
  ],
  "psx:RenewableFuelsMember": [
   "재생 연료",
   "#6aa84f"
  ]
 },
 "ignore": [
  "psx:ChemicalsSegmentMember"
 ]
}
