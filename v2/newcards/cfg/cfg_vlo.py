# VLO(발레로 에너지) v2 카드 설정 — 처음부터 자동 카드(AUTO)로 만든 첫 장(newcards/README.md 절차 검증, 2026-10-13). 회계연도 12월 31일. 카드 순위 104.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항), 8-K(신용 약정 2025-10-16, CFO 선임 10/28, 회사채 2026-03-05,
# 자사주 매입 승인 7/16), StockAnalysis.
# 엔진 수정(2026-10-13): 설비투자 태그 대체(build_multiple_history EXTRA_TAGS — 2026년 10-Q부터 VIE 차원으로만 태깅), 차입금 태그
# (DebtCurrent + LongTermDebtAndCapitalLeaseObligations, COP와 같은 조합), 4분기 EPS 보도자료 값(fetch_eps_history Q4_EPS_OVERRIDE $3.73).
# 손 문장 키(SUMMARY·BULL·BEAR·PREMISE·RISK·STORIES 등)는 auto_card가 쓰므로 두지 않는다(README "cfg 키").
CIK = '0001035002'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Valero Energy'
S_ = 'https://www.sec.gov/Archives/edgar/data/1035002/'
SEC = S_
TENQ = S_ + '000162828026050937/vlo-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q1': S_ + '000162828026028602/a3312026exh9901earningsrel.htm', 'q4': S_ + '000162828026003974/a12312025exh9901earningsre.htm',
      'q3': S_ + '000162828025045978/a9302025exh9901earningsrel.htm'}
LINKS = {'buyback': S_ + '000162828026048495/vlo-20260716.htm', 'notes': S_ + '000119312526098770/d109706d8k.htm',
         'cfo': S_ + '000119312525254583/d34851d8k.htm', 'credit': S_ + '000119312525241519/d40220d8k.htm'}
FAIRBAND_TITLE = 'id="vloFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 최근 4분기 EPS에는 2분기 $12.62가 들어 있다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
CAPEX_LABEL = '설비투자·정기보수·촉매'   # 설비투자 태그(SegmentExpenditureAdditionToLongLivedAssets) = 설비투자 + 정기보수·촉매 지출(Q2 $226M + $124M = $350M)
ACT_REASON = ''
NONOP_WHAT = '투자'
PH = ['MPC', 'PSX', 'XOM', 'CVX', 'COP', 'OXY']
PEER_FILE = 'peer_universe/energy.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '정유·석유 6곳 PER 비교 (점수는 S&P500 에너지 기준)', 'pbr': '정유·석유 PBR 비교', 'psr': '정유·석유 PSR 비교',
                'pcr': '정유·석유 PCR(FCF) 비교', 'evebitda': '정유·석유 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 에너지 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 에너지 대비 배수 순위 (v2/peer_universe/energy.json)'
PEER_TIP = ('S&P500 에너지(VLO 제외)와 배수 순위를 매긴 값이다.',
            '통합 석유사·탐사생산·정유·장비·가스관 회사가 섞여 있다. 정유사는 매출이 커 PSR이 낮게 나온다. 차트에는 정유·석유 6곳만 보인다.')
# 부문(Q2 2026 10-Q 매출 세분 표, 외부 고객) — 합 $44,476M = 연결 매출이라 조정 0
SEG = [('정유', 42300, '#1d4f91'), ('재생 디젤', 1176, '#6aa84f'), ('에탄올', 1000, '#e0a030')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(외부 고객)'
# 손 뉴스: Q2 2026 실적(7/30)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤 손 항목이 있으면 자동 항목이 빠지므로(fill.py) 9/17 이사 선임은 넣지 않았다.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('green', '2026년 7월 16일 — 자사주 매입 $5.0B 추가 승인', '2026-07-16',
     '만기 없음, 2월 승인분 남은 $1.4B(6월 말)에 더해진다', 'buyback', 'Valero 공시 (SEC 8-K)'),
    ('green', '2026년 4월 30일 — Q1 2026 실적', '2026-04-30',
     '순이익 $1.3B · 희석 EPS $4.22(1년 전 −$1.90)', 'q1', 'Valero 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 5일 — 회사채 $850M 발행 계약', None,
     '연 5.150%, 2036년 만기', 'notes', 'Valero 공시 (SEC 8-K)'),
    ('red', '2026년 1월 29일 — Q4 2025 실적', '2026-01-29',
     '4분기 순이익 $1.1B · 희석 EPS $3.73 · 2025년 EPS $7.57', 'q4', 'Valero 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 28일 — 새 CFO 선임', None,
     'Homer Bhullar(IR·재무 부사장), 2026년 1월 1일부터 · Jason Fraser 은퇴', 'cfo', 'Valero 공시 (SEC 8-K)'),
    ('green', '2025년 10월 23일 — Q3 2025 실적', '2025-10-23',
     '순이익 $1.1B · 희석 EPS $3.53(1년 전 $1.14) · 3분기 주주환원 $1.3B', 'q3', 'Valero 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 16일 — 회전 신용 약정 연장', None,
     '만기 2027년 11월 → 2030년 10월', 'credit', 'Valero 공시 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지 — 정규식이 줄 전체를 바꾼다)
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 19, 'mean': 392.58, 'median': 434, 'low': 203, 'high': 496, 'sb': 6, 'b': 3, 'h': 9, 's': 0, 'ss': 2}
ANALYST_ASOF = '2026-10-13'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-Q 매출 세분 표(외부 고객) Q2 2026 42,300/1,176/1,000, 1년 전 28,324/565/1,000, 합 = 연결 매출(44,476·29,889)이라 상계·본사 조정 없음(2026-10-13) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "vlo:RefiningMember": [
   "정유",
   "#1d4f91"
  ],
  "vlo:RenewableDieselMember": [
   "재생 디젤",
   "#6aa84f"
  ],
  "vlo:EthanolMember": [
   "에탄올",
   "#e0a030"
  ]
 },
 "ignore": []
}
