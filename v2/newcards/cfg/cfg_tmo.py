# TMO(써모피셔) v2 카드 설정 — fill.py TMO. 회계연도 12월 31일(분기는 토요일 마감, Q2 2026 = 2026-06-27). 루트 카드 있음.
# 틀 시절 카드(루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-31), 실적 보도자료(Q3 2025~Q2 2026), 8-K(Clario 합의 10/29·종결 3/24, 경영진 1/12), StockAnalysis(2026-10-01).
# 엔진: 매출원가 표준 태그가 없어 활동성 미판정 — build_activity_score.
# 재현 모드: python3 v2/newcards/build.py TMO --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-30).
CIK = '0000097745'
CUR, YO, QO = '2026-06-27', '2025-06-28', '2026-03-28'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 11994}   # Q2 2026 보도자료 매출(백만 달러, 부문 합 12,560 − 부문 간 거래 566)
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Thermo Fisher'
S_ = 'https://www.sec.gov/Archives/edgar/data/97745/'
SEC = S_
PR = {'q2': S_ + '000009774526000138/q22026earnings8kex99_1.htm', 'q1': S_ + '000009774526000086/q12026earnings8kex99_1.htm',
      'q4': S_ + '000009774526000012/q42025earnings8kex99_1.htm', 'q3': S_ + '000009774525000150/q32025earnings8kex99_1.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000009774526000144/tmo-20260627.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'clario_close': S_ + '000009774526000066/a03242026_thermofisherscie.htm', 'exec': S_ + '000114036126000871/ef20062683_8k.htm',
         'clario': S_ + '000009774525000156/thermofisherscientifictoac.htm'}
FAIRBAND_TITLE = 'id="tmoFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (10, 25), (10, 25)
FCF_SUB = '영업현금흐름 − 설비투자 · 회사 FCF $1.68B'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('R&amp;D (Q2 2026)', '$0.36B', '연구개발 · 매출의 3.0%')
NEXT = ('10월 하순 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('10월 하순', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('차입금은 $42.5B(단기·1년 안 만기 $3.4B + 장기 $39.2B)로, Clario 인수(약 $8.9B, 3월 종결) 자금을 회사채로 마련해 연초 $39.4B에서 늘었다. 현금은 $4.1B다. '
               '활동성은 매출원가 표준 태그가 없어(제품·서비스 원가를 따로 냄) 계산하지 않는다.')
ACT_REASON = '매출원가 표준 태그 없음'
YOY_EXTRA = '매출 +10% 중 유기적 성장 +5%(나머지는 Clario·Solventum 여과·분리 사업 인수와 환율) · '
SEG = [('실험실 제품·바이오제약 서비스', 6693, '#0f6eb4'), ('생명과학 솔루션', 2815, '#5aa9e6'), ('분석 기기', 1847, '#2e8b57'), ('특수 진단', 1205, '#f0c040')]
SEG_ADJ = -566   # 부문 간 거래(보고 매출 11,994 − 부문 합 12,560)
SEG_TITLE = '매출 구성 — 부문별 매출'
SEG_NOTE = ('부문 간 거래 −$0.57B 차감 전 · 1년 전보다 실험실 제품·바이오제약 서비스 +12%(Clario 포함), 생명과학 +13%, 분석 기기 +7%, 특수 진단 +6% · '
            '비율은 부문 간 거래 차감 전 합계 기준(회사 표는 연결 매출 기준 55.8%·23.5%·15.4%·10.0%) · 특수 진단의 미생물 사업은 약 $1.08B에 매각 합의(3분기 종결 예정) · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Q2 2026 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (Q2 2026 $1.0B, 1분기 $3.0B)', '상반기 $4.0B'),
           ('인수 (Clario, 3월 종결 · 현금)', '약 $8.9B'),
           ('배당 (Q2 2026 지급 = 상반기 $337M − 1분기 $162M)', '상반기 $0.34B(보도자료)', '$0.18B')]
CHECK_WHEN = '2026년 10월 하순 (예상) · Q3 2026'
CHECK = ['유기적 성장(2분기 +5%)이 이어지는지 — 회사는 고객 수요가 계속 좋아진다고 밝혔다',
         'Clario($8.9B) 통합과 차입금(전체 $42.5B, 연초 $39.4B)',
         '미생물 사업 매각 종결(약 $1.08B, 3분기 예정)',
         '조정 영업이익률(2분기 22.8%)과 GAAP 영업이익률({opm[-1]:.1f}%)의 차이 — 인수 무형자산 상각']
NONOP_WHAT = '지분 투자'
PH = ['DHR', 'A', 'IQV', 'ABT', 'BDX', 'RVTY']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '생명과학 도구·진단 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': '생명과학 도구 PBR 비교', 'psr': '생명과학 도구 PSR 비교',
                'pcr': '생명과학 도구 PCR(FCF) 비교', 'evebitda': '생명과학 도구 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&amp;P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-31 공시)'
PREMISE = ('PER {SM[\'PER\'][\'current\']:.1f}배·PSR·PCR이 5년 중 비싼 쪽이고 EV/EBITDA는 이력(4.3년) 최고에 가까워 자기 이력 {selfsc:.1f}점이다. '
           'S&P500 헬스케어 안에서는 {peersc:.1f}점({score_word(peersc)})이다 — 비싼 쪽 문턱 30 바로 {"아래" if peersc < 30 else "위"}라 동종 종목 자료가 갱신될 때마다 0과 −1을 오간다(2026-10-04 한때 29.6점). '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {sgn(VOTES[0])}·{sgn(VOTES[1])}·{sgn(VOTES[2])}로 합계 {sgn(TOTAL)} “{VERDICT}”다. GAAP 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}(인수 무형자산 상각 포함, 회사 조정 22.8%), '
        '5년 성장률 연 {pct(HIST[\'growth_5y\'])}·3년 {pct(HIST[\'growth_3y\'])}라, 현재가를 설명하려면 영업이익률이 {pct(DCF[\'requiredMargin\'])}여야 한다. '
        '최근 4분기 실효세율이 7.8%로 낮고(계산 어려움 신호 — 10-Q는 저세율 지역 이익 비중 등으로 설명하고 2026년 GAAP 세율을 9~11%로 예상), 보수 시나리오는 음수다(계산 불가) — '
        '보수는 한계·평균 매출/자본 중 나쁜 쪽을 쓰는데, Clario 인수로 투하자본이 커져 재투자 부담이 크게 잡힌다.')
FUND_TIP = '매출·영업이익 3년 CAGR(연간 FY2022→FY2025)이 음수(1점)인 것은 2022년 정점 뒤 2023년 매출이 줄었기 때문이다. 활동성은 매출원가 표준 태그가 없어 계산하지 않는다.'
SELF_TIP = 'PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PSR·PCR이 5년 중 비싼 쪽, EV/EBITDA는 4.3년 이력 최고에 가깝다. PBR만 중간이다.'
PEER_TIP = ('S&P500 헬스케어(59종목)와 배수 순위를 매긴 값이다.',
            '생명과학 도구 외에 제약·의료기기·보험·병원 등이 섞여 있다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})이 영구성장률 2.5%보다 낮아 5년 내내 2.5%로 두고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(연 {pct(HIST[\'growth_3y\'])})이 영구성장률 2.5%보다 낮아 5년 내내 2.5%로 두고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('', '2026년 7월 23일 개장 전 — Q2 2026 실적', '2026-07-23',
     '매출 $11.99B(+10%, 유기적 +5%)·EPS $4.68(조정 $6.03) · 미생물 사업 매각 합의·자사주 $1.0B', 'q2', 'Thermo Fisher 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 4월 23일 개장 전 — Q1 2026 실적', '2026-04-23',
     '매출 $11.01B(+6%)·EPS $4.43(조정 $5.44)', 'q1', 'Thermo Fisher 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 24일 개장 전 — Clario 인수 종결', '2026-03-24',
     '임상시험 데이터 기업 Clario 인수를 마쳤다(현금 약 $8.875B + 이연·조건부 대가)', 'clario_close', 'Thermo Fisher 공시 (SEC 8-K)'),
    ('', '2026년 1월 29일 개장 전 — Q4 2025 실적', '2026-01-29',
     '매출 $12.21B(+7%)·EPS $5.21(조정 $6.57) · 2025년 매출 $44.56B(+4%)', 'q4', 'Thermo Fisher 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 12일 개장 전 — 경영진 변경', '2026-01-12',
     '미셸 라가르드 COO(3월 말)와 프레더릭 로워리 부사장(2월 말)이 회사를 떠나고 3월 조직을 개편한다', 'exec', 'Thermo Fisher 공시 (SEC 8-K)'),
    ('', '2025년 10월 29일 개장 전 — Clario 인수 합의', '2025-10-29',
     '현금 약 $8.875B(이연 $125M·조건부 최대 $400M 별도)에 Clario 인수 합의', 'clario', 'Thermo Fisher 공시 (SEC 8-K)'),
    ('', '2025년 10월 22일 개장 전 — Q3 2025 실적', '2025-10-22',
     '매출 $11.12B(+5%)·EPS $4.27(조정 $5.79)', 'q3', 'Thermo Fisher 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('고객 수요 회복과 Clario 인수로 2분기 매출이 10% 늘고, 주가는 1년 새 {CH_TXT}', '회복기·높은 배수',
           ['2분기 매출 $11.99B(+10%, 유기적 +5%), GAAP EPS $4.68(+9%), 조정 EPS $6.03(+13%)였다.',
            '3월 임상시험 데이터 기업 Clario를 약 $8.9B에 인수했고, 4월 미생물 사업을 약 $1.08B에 팔기로 했다.',
            '인수 자금으로 회사채를 내 차입금이 $42.5B로 늘었고, 상반기에 자사주를 $4.0B 샀다.'],
           'PER·PSR·PCR이 5년 중, EV/EBITDA가 4.3년 이력 중 비싼 쪽이고, GAAP 영업이익률 {pct(HIST[\'margin_now\'])}로는 현금흐름 모델이 현재가의 {DCF[\'base\'] / px * 100:.0f}%만 설명한다.',
           'Q3 2026 실적(10월 하순 예상)의 유기적 성장과 Clario 기여.')
BULL = [('성장', '2분기 매출 +10%(유기적 +5%), 네 부문 모두 성장.'),
        ('이익', '조정 영업이익률 22.8%(1년 전 21.9%), 조정 EPS +13%.'),
        ('포트폴리오', 'Clario 인수로 임상시험 데이터 사업 추가, 비핵심 미생물 사업 매각.')]
BEAR = [('밸류', 'PER {SM[\'PER\'][\'current\']:.0f}배 — 5년 중앙값 {SM[\'PER\'][\'median\']:.0f}배, 현금흐름 기본 ${DCF[\'base\']:.0f}.'),
        ('부채', '차입금 $42.5B로 연초보다 $3B 넘게 늘었다.'),
        ('세율', '최근 4분기 실효세율 7.8% — 회사는 2026년 GAAP 세율 9~11%를 예상한다(10-Q).')]
ANALYST = {'rating': 'Strong Buy', 'n': 27, 'nt': 22, 'mean': 647.36, 'median': 639, 'low': 535, 'high': 780, 'sb': 19, 'b': 4, 'h': 3, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-10'

REQ_MULT_EXACT = False   # 옛 카드는 틀 문구("3배를 넘는다") 그대로
POST = []


# ── 자동 카드(설계 D, 2026-10-10) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose.py 제안(손 표와 숫자 일치) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "tmo:LaboratoryProductsAndBiopharmaServicesMember": [
   "실험실 제품·바이오제약 서비스",
   "#0f6eb4"
  ],
  "tmo:LifeSciencesSolutionsMember": [
   "생명과학 솔루션",
   "#5aa9e6"
  ],
  "tmo:AnalyticalInstrumentsMember": [
   "분석 기기",
   "#2e8b57"
  ],
  "tmo:SpecialtyDiagnosticsMember": [
   "특수 진단",
   "#f0c040"
  ]
 },
 "ignore": []
}
