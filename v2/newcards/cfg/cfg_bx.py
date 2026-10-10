# BX(블랙스톤) v2 카드 설정 — fill.py BX. 회계연도 12월 31일. 시총 87위(S&P500 현재 시총 순, 2026-10-02 StockAnalysis 기준, 루트 카드 없음).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-07), 실적 보도자료(Q3 2025~Q2 2026, SEC 접수 모두 오전 6시 55~57분 = 장 시작 전), 8-K(분기 중 실현 수익 추정 9/22), StockAnalysis.
# 엔진 수정(2026-10-02): 영업이익 줄이 없어 DERIVED_OPINC = 세전이익 − 펀드 투자 순이익 + 이자비용(총비용 안), 차입금은 Loans Payable.
# Up-C 구조라 현금흐름 주식 수를 경제적 전체 주식 수(보통주 + Blackstone Holdings 파트너십 지분, 2026-06-30 12.44억)로 바꿨다(build_dcf ECON_SHARES).
# 배수(PSR·PCR·EV/EBITDA)는 Class A 주식 시가총액만 써서 낮게 나온다 — 고치지 않고 문장으로 밝힌다(안건).
# 비교군은 BLK와 같은 S&P500 자산운용·수탁은행(build_peer_score TICKER_UNIVERSE).
BUILD = {}
NO_DCF_SKEW = True   # 금융 카드 — 현금흐름 칸 쏠림 메모(A0) 없음
CIK = '0001393818'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 5044, 'op': 2813, 'ni': 1229}   # 10-Q, 영업이익 = 세전 2,808 − 펀드 투자 순이익 140 + 이자 145, 순이익은 Blackstone Inc. 귀속
VOTES, VERDICT = (1, -1, -2), '적정~고평가'
CO = 'Blackstone'
S_ = 'https://www.sec.gov/Archives/edgar/data/1393818/'
SEC = S_
PR = {'q2': S_ + '000119312526313250/d153439dex991.htm', 'q1': S_ + '000119312526171788/d60443dex991.htm',
      'q4': S_ + '000119312526028145/d92648dex991.htm', 'q3': S_ + '000119312525247643/d48505dex991.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000119312526340208/d158269d10q.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'real_sep': S_ + '000119312526398100/d92415dex991.htm'}
FAIRBAND_TITLE = 'id="bxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. EPS는 Blackstone Inc. 귀속 이익(파트너십 지분 몫 제외) 기준이다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (20, 70), (0, 80)
FCF_SUB = '영업현금흐름 − 설비투자(사무 설비)'
CAPEX_SUB = '가구·장비·임차 개량 취득(현금흐름표)'
STAT3 = ('운용자산 (Q2 2026)', '$1.35T', '분기 유입 $68.3B · 수수료 운용자산 $961.6B')
NEXT = ('10월 하순 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('10월 하순', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('차입금(Loans Payable)은 $13.2B, 현금은 $2.5B다(펀드 보유 현금 별도). 유동·비유동을 나누지 않는 재무상태표라 유동비율·당좌비율은 매기지 않는다. '
               '2분기 순이익 가운데 Blackstone Holdings 파트너십 지분 몫이 $946M, Blackstone Inc. 몫이 $1,229M이다. 파트너십 몫은 법인세 전 이익에서 나눠 지분율(약 36%)보다 비중이 크다.')
ACT_REASON = ''
YOY_EXTRA = '실현 성과보수 $1.37B(1년 전 $0.83B) · 분기 유입 $68.3B · 분배가능이익 주당 $1.52 · '
SEG = [('운용·자문 수수료', 2266, '#0072c6'), ('성과보수(성과 배분)', 1952, '#22c55e'), ('자기자본 투자 이익', 520, '#f59e0b'), ('인센티브 수수료', 159, '#a78bfa'), ('이자·배당', 134, '#5aa9e6')]
SEG_ADJ = 12   # 기타 매출 $12M
SEG_TITLE = '매출 구성 — 매출 종류별(GAAP)'
SEG_NOTE = ('성과보수는 실현 $1.37B + 미실현 $0.59B, 자기자본 투자 이익은 실현 $0.11B + 미실현 $0.41B · '
            '출처: <a href="{TENQ}" target="_blank" rel="noopener">Q2 2026 10-Q (SEC) →</a>')
CAPITAL = [('배당 선언 (상반기, 주당)', '$2.65'),
           ('자사주 매입 (상반기, 40만 주)', '$48M'),
           ('분기 배당 (분배가능이익에 연동)', '$1.29', '2분기분')]
CHECK_WHEN = '2026년 10월 하순 (예상) · Q3 2026'
CHECK = ['실현 수익 — 9월 22일까지 실현 성과보수·자기자본 투자 이익 $350M 넘게 예상(회사 추정)',
         '분기 유입(2분기 $68.3B)과 수수료 운용자산',
         '분배가능이익(2분기 주당 $1.52)과 배당',
         '미실현 성과보수 잔액(순 $7.5B)']
NONOP_WHAT = '투자'
PH = ['BLK', 'KKR', 'APO', 'ARES', 'TROW', 'BEN']
PEER_FILE = 'peer_universe/asset_managers.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '자산운용 6곳 PER 비교 (점수는 S&P500 자산운용·수탁은행 기준)', 'pbr': '자산운용 PBR 비교', 'psr': '자산운용 PSR 비교',
                'pcr': '자산운용 PCR(FCF) 비교', 'evebitda': '자산운용 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 자산운용·수탁은행보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 자산운용·수탁은행 대비 배수 순위 (v2/peer_universe/asset_managers.json)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-08-07 공시)'
PREMISE = ('주가가 1년 새 {CH_TXT} 내려 PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)를 비롯한 다섯 배수가 모두 5년 중 싼 쪽이라 자기 이력 {selfsc:.1f}점(싸다)이다. '
           'S&P500 자산운용·수탁은행 안에서는 PBR이 가장 비싸고 PSR도 비싼 쪽, PER은 중간이라 {peersc:.1f}점(비싸다)이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”다. 현재가를 정당화하려면 영업이익률이 {pct(DCF[\'requiredMargin\'])}까지 올라야 한다(최근 4분기 {pct(HIST[\'margin_now\'])}). '
        'PSR·PCR은 Class A 보통주 시가총액만 써서, 경제적 전체 주식 가운데 빠진 몫(파트너십 지분·미가득 참여 주식, 약 40%)만큼 낮게 나온다. EV/EBITDA도 같은 시가총액을 써서 낮게 나온다. 자기 이력의 “싸다”는 그만큼 덜어서 읽는다.')
FUND_TIP = '유동·비유동을 나누지 않는 재무상태표라 유동비율·당좌비율은 매기지 않는다. 영업이익률이 높은 것은 매출에 성과보수·투자 이익이 들어 있어서다. 활동성은 5년 비교 이력이 부족해 판정하지 않는다.'
SELF_TIP = 'PER은 Blackstone Inc. 귀속 EPS 기준이다. PSR·PCR은 Class A 시가총액을 회사 전체 매출·현금흐름으로 나눠, EV/EBITDA는 EV에 같은 시가총액을 써서 낮게 나온다. 2021년 성과보수가 컸던 때의 높은 배수가 이력에 들어 있다.'
PEER_TIP = ('S&P500 자산운용·수탁은행(BX 제외 11곳)과 배수 순위를 매긴 값이다. PCR·EV/EBITDA는 값이 있는 곳이 적어 빼고 셋으로 매겼다.',
            '수탁은행(BNY·STT·NTRS)과 전통 운용사가 섞여 있다. 차트에는 자산운용 6곳만 보인다.')
STORIES = ['5년 성장률(연 {pct(HIST[\'growth_5y\'])}, 2021년 성과보수 고점 대비)이 2.5%보다 낮아 5년 내내 2.5%로 두고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률이 2.5%보다 낮아 5년 내내 2.5%로 두고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])}, 2023년 저점 대비)로 시작해 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('“보수”와 “기본”이 거의 같다. 5년 성장률이 2021년 성과보수 고점 대비라 음수여서 둘 다 2.5%로 두기 때문이다. “낙관”만 2023년 저점 대비 3년 성장률(연 {pct(HIST[\'growth_3y\'])})을 써서 크게 높다. '
            '영업이익 전체를 쓰므로 주식 수는 회사가 밝힌 경제적 전체 주식 수(보통주 + 파트너십 지분 12.44억)로 나눴다(Class A 7.5억 주만 쓰면 기본 약 $95). 세율은 연결 실효세율(약 15%, 과세되지 않는 펀드 이익·파트너십 몫 포함)에서 시작해 Blackstone Inc. 자체 세율(약 26%)보다 낮고, 미실현 성과보수 순 $7.5B(주당 약 $6)는 더하지 않았다. 앞의 것은 값을 높이고 뒤의 것은 낮춘다. 최근 증분 매출/자본을 구하지 못해 이력 평균(약 0.8)을 쓴다.')
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 22일 — 3분기 실현 수익 추정', None,
     '7월 1일~9월 22일 실현 성과보수·자기자본 투자 이익 $350M 넘게 예상(약 90%가 성과보수)', 'real_sep', 'Blackstone 공시 (SEC 8-K)'),
    ('green', '2026년 7월 23일 장 시작 전 — Q2 2026 실적', '2026-07-23',
     'EPS $1.54(1년 전 $0.98) · 분배가능이익 주당 $1.52 · 유입 $68.3B · 운용자산 $1.35T · 배당 $1.29 · 당일 주가 +1.4%', 'q2', 'Blackstone 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 23일 장 시작 전 — Q1 2026 실적', '2026-04-23',
     'EPS $0.83 · 분배가능이익 주당 $1.36 · 유입 $68.5B · 배당 $1.16 · 당일 주가 −5.7%', 'q1', 'Blackstone 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 29일 장 시작 전 — Q4 2025 실적', '2026-01-29',
     'EPS $1.30 · 분배가능이익 주당 $1.75 · 유입 $71.5B(3년여 만에 최대) · 배당 $1.49 · 당일 주가 −2.6%', 'q4', 'Blackstone 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 23일 장 시작 전 — Q3 2025 실적', '2025-10-23',
     'EPS $0.80(1년 전 $1.02) · 분배가능이익 주당 $1.52 · 유입 $54.2B · 배당 $1.29 · 당일 주가 −4.2%', 'q3', 'Blackstone 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('유입과 이익은 늘었지만 주가는 1년 새 {CH_TXT}', '유입 확대·주가 하락',
           ['2분기 EPS가 $1.54(1년 전 $0.98)였고 실현 성과보수가 $1.37B로 늘었다.',
            '분기 유입이 네 분기 연속 $54~72B였고 운용자산은 $1.35T가 됐다.',
            '배당은 분배가능이익에 따라 분기마다 바뀌어 $1.16~1.49였다.'],
           '배수는 5년 이력에서 싼 쪽이지만 동종업 안에서는 비싼 쪽이고, 현금흐름 모델 기본값은 주당 ${DCF[\'base\']:.2f}이다.',
           'Q3 2026 실적(10월 하순 예상)의 실현 수익과 유입.')
BULL = [('유입', '네 분기 유입 $54~72B, 최근 1년 $262.5B.'),
        ('실현', '2분기 실현 성과보수 $1.37B(1년 전 $0.83B).'),
        ('대기 자금', '투자 대기 자금 $228.1B, 미실현 성과보수 순 $7.5B.')]
BEAR = [('주가', '1년 새 −36%, 실적 날 네 번 중 세 번 하락.'),
        ('이익 변동', '성과보수·투자 이익이 시장에 따라 크게 움직임.'),
        ('구조', '경제적 지분의 약 36%가 파트너십 지분.')]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 18, 'mean': 143.33, 'median': 142, 'low': 119, 'high': 184, 'sb': 9, 'b': 4, 'h': 11, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-10'


# ── 자동 카드(설계 D, 2026-10-11) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose2·3 제안(손 표와 숫자 일치 — 여러 축·나머지 줄) ──
AUTO = True
SEG_MAP = {
 "parts": [
  {
   "concepts": [
    "bx:FeeRelatedPerformanceRevenues"
   ],
   "axis": "us-gaap:StatementBusinessSegmentsAxis",
   "extra": {
    "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
   },
   "members": {
    "bx:CreditAndInsuranceMember": [
     "인센티브 수수료",
     "#a78bfa"
    ]
   }
  },
  {
   "concepts": [
    "bx:PerformanceRevenueRealized"
   ],
   "axis": "us-gaap:StatementBusinessSegmentsAxis",
   "extra": {
    "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
   },
   "members": {
    "bx:PrivateEquitySegmentMember": [
     "자기자본 투자 이익",
     "#f59e0b"
    ],
    "bx:CreditAndInsuranceMember": [
     "자기자본 투자 이익",
     "#f59e0b"
    ],
    "bx:MultiAssetsInvestingMember": [
     "자기자본 투자 이익",
     "#f59e0b"
    ]
   }
  },
  {
   "concepts": [
    "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
   ],
   "axis": "srt:ProductOrServiceAxis",
   "extra": {},
   "members": {
    "us-gaap:InvestmentAdviceMember": [
     "운용·자문 수수료",
     "#0072c6"
    ]
   }
  },
  {
   "concepts": [],
   "axis": None,
   "extra": {},
   "members": {
    "us-gaap:InvestmentIncomeInterestAndDividend": [
     "이자·배당",
     "#5aa9e6"
    ]
   }
  }
 ],
 "remainder": [
  "성과보수(성과 배분)",
  "#22c55e",
  0.387
 ]
}
