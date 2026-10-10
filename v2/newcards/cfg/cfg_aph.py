# APH(앰페놀) v2 카드 설정 — _core_fill.py APH. 회계연도 12월 31일. 2026-09-03부터 2:1 분할 기준 거래(보도자료 주당 수치는 분할 전).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-31), 실적 보도자료(Q3 2025~Q2 2026), 8-K(CommScope CCS 종결 1/12, 의장 2/5, 분할 8/6·9/4), StockAnalysis.
# 엔진 수정(2026-10-01): KNOWN_SPLITS 세 번째 2:1(2026-09-03), 차입금 DEBT_TOTAL_TAG(1년 안 만기 $1,634M 누락 → $18,811M).
# 배열: 루트 카드가 분할 안전장치에 걸려 9/11에서 멈춰(card_status "held") Yahoo 분할 반영 일봉으로 9/30까지 다시 만들었다(aph_arrays.py).
PBR_GAP_NEG_EQUITY = False   # 자본은 늘 양수 — PBR 이력 공백에 '자본 음수' 문구를 안 쓴다
CIK = '0000820313'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 8758.1, 'op': 2584.6, 'ni': 1769.2, 'ocf': 1557.2, 'cap': 355.5}
RELEASE_TOL = 0.2
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Amphenol'
S_ = 'https://www.sec.gov/Archives/edgar/data/820313/'
SEC = S_
PR = {'q2': S_ + '000110465926087904/aph-20260729xex99d1.htm', 'q1': S_ + '000110465926050984/aph-20260429xex99d1.htm',
      'q4': S_ + '000110465926007259/aph-20260128xex99d1.htm', 'q3': S_ + '000110465925101429/aph-20251022xex99d1.htm'}
TENQ = S_ + '000110465926089194/aph-20260630x10q.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'ccs': S_ + '000110465926002737/tm262701d1_8k.htm', 'chair': S_ + '000110465926010676/tm265098d1_8k.htm',
         'split': S_ + '000110465926091969/tm2622441d1_8k.htm'}
FAIRBAND_TITLE = 'id="aphFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(분할 반영, 10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 지난 5년 연 {pct(HIST[\'growth_5y_raw\'])})</span>'
OPM_RANGE, Y2 = (15, 35), (10, 40)
FCF_SUB = '영업현금흐름 − 설비투자 · 회사 FCF $1.2B'
CAPEX_SUB = '설비투자(현금흐름표)'
STAT3 = ('수주 (Q2 2026)', '$10.7B', '수주/매출 1.23배')
NEXT = ('10월 하순 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('10월 하순', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('차입금은 $18.8B(1년 안 만기 $1.6B + 장기 $17.2B)다. 1월 CommScope 연결·케이블 사업 인수(약 $10.5B 현금) 자금은 회사채, 지연인출 기간대출(3년·364일), 보유 현금으로 마련했다. '
               '현금·단기투자는 $5.42B로 연초 $11.43B에서 줄었다. 9월 2일 2:1 분할 주식이 배분됐으므로 주당 수치는 분할 후 기준으로 맞췄다(보도자료 수치는 분할 전). '
               '활동성은 분기 평균 잔액이라 인수로 늘어난 매출채권($4.72B → $6.79B, +44%)·재고($3.42B → $4.55B, +33%)를 아직 다 반영하지 않는다. “5년 중 짧은 편”은 그만큼 낮춰 읽어야 한다.')
YOY_EXTRA = '매출 +55% 가운데 유기적 성장 +30%(나머지는 인수·환율) · 영업이익에는 IEEPA 관세 환급 순효과 $80M · '
SEG = [('통신 솔루션', 5383.6, '#0067b1'), ('극한 환경 솔루션', 1856.8, '#5aa9e6'), ('연결·센서 시스템', 1517.7, '#94a3b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별 외부 매출'
SEG_NOTE = ('1년 전보다 통신 솔루션 +85%(CommScope 연결·케이블 사업 포함), 극한 환경 +28%, 연결·센서 +17% · 부문 영업이익률 통신 33.3%, 극한 환경 29.5%, 연결·센서 20.6%(부문 간 매출 포함 기준) · '
            '출처: <a href="{TENQ}" target="_blank" rel="noopener">Q2 2026 10-Q 부문 표 (SEC) →</a>')
CAPITAL = [('자사주 매입 (Q2 2026, 150만 주 · 분할 전)', '$0.21B'),
           ('인수 (상반기 3건, CommScope 연결·케이블 사업 등)', '$10.7B'),
           ('배당 (Q2 2026 지급)', '분기 배당', '$0.31B')]
CHECK_WHEN = '2026년 10월 하순 (예상) · Q3 2026'
CHECK = ['3분기 가이던스 매출 $9.3~9.4B(+50~52%), 조정 EPS 분할 반영 $0.70~0.71(분할 전 $1.40~1.42)를 넘는지',
         '수주/매출 비율(2분기 1.23)과 유기적 성장(2분기 +30%)이 이어지는지',
         'CommScope 통합 진행과 차입금($18.8B, 기간대출 포함) 상환·차환 계획이 나오는지',
         '2:1 분할 뒤 첫 실적의 주당 수치(분할 반영 기준)']
NONOP_WHAT = '지분 투자'
PH = ['ANET', 'CSCO', 'DELL', 'TXN', 'AVGO', 'KLAC']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '네트워크·하드웨어·반도체 6곳 PER 비교 (점수는 IT 카드 유니버스 기준)', 'pbr': '네트워크·하드웨어·반도체 PBR 비교', 'psr': '네트워크·하드웨어·반도체 PSR 비교',
                'pcr': '네트워크·하드웨어·반도체 PCR(FCF) 비교', 'evebitda': '네트워크·하드웨어·반도체 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-31 공시)'
PREMISE = ('PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PSR·PBR·PCR이 5년 중 비싼 쪽이고 EV/EBITDA만 중간이라 자기 이력 {selfsc:.1f}점(비싸다)이다. '
           '카드 유니버스 IT 안에서는 PSR이 싼 쪽, 나머지가 중간이라 {peersc:.1f}점(중간)이다. 머리글 적정주가 ${FB[\'low\']}~${FB[\'high\']}는 최근 1년 PER 범위(5년 이력의 위쪽)에 최근 4분기 EPS를 곱한 값이라 판정과 별개다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”다. 현재가를 설명하려면 5년 내내 매출이 연 {pct(DCF[\'requiredGrowth\'])}씩 커야 한다(영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 내려가는 기본 경로 기준). '
        '격차의 대부분은 출구 배수에서 온다. 모델은 5년 뒤를 할인율 10%·영구성장 2.5%로 접어 그해 현금흐름의 약 13배로 보지만, 시장은 지금 FCF의 {SM[\'PCR\'][\'current\']:.0f}배를 준다. 할인율 8%·영구성장 3.5%까지 풀어도 기본 ${GMAX:.0f}, 낙관 ${GMAXH:.0f}이다.')
FUND_TIP = '매출 3년 CAGR(연간 FY2022→FY2025) {FR[\'revenueCagr\']:.1f}%에는 인수 매출이 들어 있다(내재가치 탭 {pct(HIST[\'growth_5y\'])}는 최근 4분기 합 기준 5년 성장률). 부채비율 {FPT[\'debtToEquity\']}점은 CommScope 사업 인수 차입금 때문이다.'
SELF_TIP = 'PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PSR·PBR·PCR은 5년 중 비싼 쪽, EV/EBITDA는 중간이다. 9월 2:1 분할 전 주가·EPS는 분할 기준으로 맞췄다.'
PEER_TIP = ('카드 유니버스 IT 종목과 배수 순위를 매긴 값이다.',
            '카드 유니버스에 커넥터·수동부품 제조사가 없어 반도체·네트워크·소프트웨어와 비교한다. 점수는 IT 카드 28종목 안의 위치다. 직접 경쟁사가 없는 비교라 동종업 표({sgn(VOTES[1])})는 참고로 읽는다(비교군 설계는 v2.1에서 따로).')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})에서 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = '5년 성장률 {pct(HIST[\'growth_5y\'])}에는 인수 매출이 섞여 있다. 다만 최근 네 분기 유기적 성장(+41% → +37% → +33% → +30%)은 이보다 높아, 쟁점은 이 속도가 얼마나 오래 가느냐다. 낙관(3년 연 {pct(HIST[\'growth_3y\'])}가 식는 경로)도 주당 ${DCF[\'high\']:.2f}로 현재가에 못 미친다.'
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 6일 장 마감 후 — 2:1 주식 분할 발표', '2026-08-07',
     '8월 17일 기준 주주에게 9월 2일 1주당 1주를 더 주는 주식 배당 방식(9월 3일부터 분할 기준 거래)', 'split', 'Amphenol 공시 (SEC 8-K)'),
    ('', '2026년 7월 29일 개장 전 — Q2 2026 실적', '2026-07-29',
     '매출 $8.8B(+55%, 유기적 +30%) · 수주 $10.7B · EPS 분할 반영 $0.69(분할 전 $1.37, +59%) · 3분기 매출 가이던스 $9.3~9.4B', 'q2', 'Amphenol 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 4월 29일 개장 전 — Q1 2026 실적', '2026-04-29',
     '매출 $7.6B(+58%, 유기적 +33%) · EPS 분할 반영 $0.36(분할 전 $0.72)·조정 $0.53(분할 전 $1.06)', 'q1', 'Amphenol 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 5일 개장 전 — 의장 교체 예정', '2026-02-05',
     '마틴 뢰플러 의장이 5월 주주총회 때 이사회를 떠나고 R. 애덤 노르윗 CEO가 의장을 겸한다', 'chair', 'Amphenol 공시 (SEC 8-K)'),
    ('', '2026년 1월 28일 개장 전 — Q4 2025 실적', '2026-01-28',
     '매출 $6.4B(+49%, 유기적 +37%) · EPS 분할 반영 $0.46(분할 전 $0.93)', 'q4', 'Amphenol 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 12일 개장 전 — CommScope 사업 인수 종결', '2026-01-12',
     'CommScope의 연결·케이블 솔루션 사업을 약 $10.5B 현금에 인수 완료(1월 9일)', 'ccs', 'Amphenol 공시 (SEC 8-K)'),
    ('', '2025년 10월 22일 개장 전 — Q3 2025 실적', '2025-10-22',
     '매출 $6.2B(+53%, 유기적 +41%) · EPS 분할 반영 $0.49(분할 전 $0.97)', 'q3', 'Amphenol 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('IT 데이터컴 시장의 큰 유기적 성장과 CommScope 사업 인수로 매출이 55% 늘고, 주가는 1년 새 {CH_TXT}', '고성장·높은 배수',
           ['2분기 매출 $8.8B(+55%, 유기적 +30%), 수주 $10.7B(수주/매출 1.23)였다.',
            'GAAP EPS 분할 반영 $0.69(+59%), GAAP 영업이익률 29.5%였다(관세 환급 $80M 포함).',
            '1월 CommScope 연결·케이블 사업을 약 $10.5B에 인수했고 9월에 2:1 분할을 했다.'],
           '배수가 5년 중 비싼 쪽이고, 지난 5년 성장(연 {pct(HIST[\'growth_5y_raw\'])})으로도 현금흐름 모델은 현재가의 {DCF[\'base\'] / px * 100:.0f}%만 설명한다.',
           'Q3 2026 실적(10월 하순 예상)이 매출 가이던스 $9.3~9.4B를 넘는지.')
BULL = [('성장', '매출 +55%, 유기적 +30%, 수주/매출 1.23.'),
        ('수익성', '2분기 GAAP 영업이익률 29.5%(조정 29.8%).'),
        ('현금', '2분기 영업현금 $1.6B, 회사 FCF $1.2B.')]
BEAR = [('밸류', 'PER {SM[\'PER\'][\'current\']:.0f}배·PBR {SM[\'PBR\'][\'current\']:.1f}배로 5년 중 비싼 쪽이다.'),
        ('부채', 'CommScope 사업 인수 뒤 차입금 $18.8B, 현금·단기투자 $5.4B.'),
        ('일회성', '2분기 이익에 IEEPA 관세 환급 순효과 $80M(분할 전 주당 $0.04)이 들어 있다.')]
ANALYST = {'rating': 'Strong Buy', 'n': 19, 'nt': 12, 'mean': 100.83, 'median': 100, 'low': 88.5, 'high': 116, 'sb': 13, 'b': 4, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-06'
MISS_WHY = {('DELL', 'pbr'): ' 자본 음수'}
PRE = [r'''
_G = json.loads(re.search(r'^const APH_DCF_GRID = (\{.*?\});', h, re.M).group(1))
GMAX = max(v for row in _G['values']['기본'] for v in row if v is not None); GMAXH = max(v for row in _G['values']['낙관'] for v in row if v is not None)
FR = {r_['metric']: r_['value'] for ax_ in FUND['axes'].values() for r_ in ax_.get('rows', [])}   # 기본적 분석 지표 값·점수(E26)
FPT = {r_['metric']: r_['points'] for ax_ in FUND['axes'].values() for r_ in ax_.get('rows', [])}
''']


# ── 자동 카드(설계 D, 2026-10-10) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose.py 제안(손 표와 숫자 일치) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "aph:CommunicationsSolutionsSegmentMember": [
   "통신 솔루션",
   "#0067b1"
  ],
  "aph:HarshEnvironmentSolutionsSegmentMember": [
   "극한 환경 솔루션",
   "#5aa9e6"
  ],
  "aph:InterconnectAndSensorSystemsMember": [
   "연결·센서 시스템",
   "#94a3b8"
  ]
 },
 "ignore": []
}
