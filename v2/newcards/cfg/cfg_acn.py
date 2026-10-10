# ACN(액센츄어) v2 카드 설정 — fill.py ACN. 회계연도 8월 31일(FY26 = 2025-09 ~ 2026-08). 시총 98위(S&P500 현재 시총 순, 2026-10-02 StockAnalysis 기준, 루트 카드 없음).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-06-18), 실적 보도자료(Q4 FY25~Q3 FY26, SEC 접수 모두 오전 6시 40분대 = 장 시작 전, Q4 FY26은 10/1 — 카드 기준일 9/30 뒤),
# 8-K(신용 약정 4/24, 자사주 확대 6/23, 회사채 7/10), StockAnalysis.
# 엔진 수정(2026-10-02): 표지 주식 수가 클래스별(dei 2010년에 멈춤)이고 Class A에 회사 보유 자기주식(5,557만 주)이 들어 있어,
# 표지 합산(adapters/cover_shares.py) 뒤 오버레이 값을 분기 희석 가중평균으로 바꿨다(Q3 FY26 2026-05-31 종료 3개월 희석 가중평균 615,593,409주; 행의 end는 표지 기준일 2026-06-04 그대로 둬 날짜만 표지를 따른다. 회사 발표 유통 약 6.12억 주).
BUILD = {'overlay': True}   # 총부채 합산·장기차입금 별칭(adapters/overlay_feed.py SUM·ALIAS)을 재무에 먹인다
CIK = '0001467373'
CUR, YO, QO = '2026-05-31', '2025-05-31', '2026-02-28'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
RELEASE = {'rev': 18718, 'op': 3175, 'ni': 2339, 'ocf': 3786, 'cap': 186}   # 10-Q, 현금흐름은 9개월 차분
VOTES, VERDICT = (1, 1, 0), '적정~저평가'
CO = 'Accenture'
S_ = 'https://www.sec.gov/Archives/edgar/data/1467373/'
SEC = S_
PR = {'q2': S_ + '000146737326000031/q3fy26earnings8-kexhibit.htm', 'q1': S_ + '000146737326000013/q2fy26earnings8-kexhibit.htm',
      'q4': S_ + '000146737325000221/q1fy26earnings8-kexhibit.htm', 'q3': S_ + '000146737325000213/q4fy25earnings8-kexhibit.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000146737326000032/acn-20260531.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
LINKS = {'q4fy26': S_ + '000146737326000037/q4fy26earnings8-kexhibit.htm', 'buyback': S_ + '000146737326000035/acn062320268-kexhibit.htm', 'notes': S_ + '000119312526300813/d181172d8k.htm'}
FAIRBAND_TITLE = 'id="acnFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y_raw\'])})</span>'
OPM_RANGE, Y2 = (5, 25), (0, 25)
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('신규 수주 (Q3 FY26)', '$19.3B', '1년 전 $19.7B · 1억 달러 이상 수주 104건(FY26 누적, 전년 같은 기간 대비 +13%)')
NEXT = ('10월 1일 발표', '일정 · Q4 FY26 (카드 기준일 뒤)'); NEXT_OP = ('10월 1일', 'Q4 FY26 발표됨')
FY_ENDS, FY_LABEL = ('2025-08-31', '2024-08-31'), 'FY25'
HEALTH_NOTE = ('5월 말 차입금은 $5.1B, 현금은 $10.2B다. 7월에 회사채 $5.0B를 냈다. 리스 부채가 약 $3.2B 있다. '
               '회사 발표 유통 주식은 약 6.12억 주다.')
ACT_REASON = ''
YOY_EXTRA = '매출 +6%(현지 통화 +3%) · 영업이익률 17.0%(+0.2%p) · 신규 수주 −2% · '
SEG = [('컨설팅', 9328.5, '#a100ff'), ('매니지드 서비스', 9389.7, '#c466ff')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 서비스 종류별'
SEG_NOTE = ('1년 전보다 컨설팅 +3.6%, 매니지드 서비스 +7.7% · 출처: <a href="{TENQ}" target="_blank" rel="noopener">Q3 FY26 10-Q (SEC) →</a>')
CAPITAL = [('주주환원 (FY26 9개월, 자사주+배당)', '$8.2B'),
           ('FY26 자사주 매입 계획 (6월 $2B 확대)', '$7.5B'),
           ('분기 배당 (FY26)', '$1.63', '+10%')]
CHECK_WHEN = '2026년 10월 1일 발표 · Q4 FY26(카드 기준일 뒤, 반영 안 함)'
CHECK = ['10월 1일 Q4 FY26: 매출 $18.7B(현지 통화 +7%), GAAP EPS $3.29, FY26 GAAP EPS $13.56(카드 수치에는 아직 없음)',
         '신규 수주 흐름(3분기 $19.3B, 4분기 $22.2B)',
         '미국 연방 정부 사업 영향(연간 성장 약 1%p)',
         'Dragos 등 보안 인수와 7월 회사채 $5.0B']
NONOP_WHAT = '투자'
PH = ['IBM', 'CRM', 'ORCL', 'CSCO', 'MSFT', 'DELL']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소프트웨어·하드웨어·IT 서비스 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': '소프트웨어·IT 서비스 PBR 비교', 'psr': '소프트웨어·IT 서비스 PSR 비교',
                'pcr': '소프트웨어·IT 서비스 PCR(FCF) 비교', 'evebitda': '소프트웨어·IT 서비스 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
FUND_ASOF_NOTE = 'Q3 FY26 10-Q (2026-06-18 공시)'
PREMISE = ('주가가 1년 새 {CH_TXT} 내려 다섯 배수가 모두 5년 중 가장 싼 쪽(PER {SM[\'PER\'][\'current\']:.1f}배 대 5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)이라 자기 이력 {selfsc:.1f}점(싸다)이다. '
           '카드 유니버스 IT 안에서는 다섯 배수 모두 가장 낮아 {peersc:.1f}점(싸다)이다. 다만 이 비교군은 반도체·소프트웨어·하드웨어가 대부분이라 같은 업종끼리 잰 순위는 아니다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가와 비슷하다</strong>.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”다. 현재가를 정당화하려면 5년 매출 성장이 연 {pct(DCF[\'requiredGrowth\'])}면 된다(실제 5년 연 {pct(HIST[\'growth_5y_raw\'])}). '
        '동종업 +1은 반도체·소프트웨어가 많은 비교군 안의 순위라 IT 서비스끼리 잰 값으로 읽지 않는다.')
FUND_TIP = '차입금이 총자산의 {FR[\'debtDependency\'][\'value\']:.1f}%로 적고 이익률이 안정적이다. 매출 성장은 최근 4분기 기준 3년 연 {pct(HIST[\'growth_3y\'])}(점수 칸의 연간 결산 기준은 {FR[\'revenueCagr\'][\'value\']:.1f}%)로 5년(연 {pct(HIST[\'growth_5y\'])})보다 느려졌다. 활동성은 영업순환주기 기준이다.'
SELF_TIP = 'PER {SM[\'PER\'][\'current\']:.1f}배는 5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배의 절반 수준이다. 최근 4분기 EPS는 사업 최적화 비용만큼(주당 $1.18) 낮아져 있어 이를 되돌리면 PER은 약 13.4배다. 주식 수는 표지가 아니라 분기 희석 가중평균을 썼다.'
PEER_TIP = ('카드 유니버스 IT 종목과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 대부분이라 IT 서비스끼리 잰 순위는 아니다. 차트에는 소프트웨어·하드웨어·IT 서비스 6곳만 보인다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})로 시작해 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('세 시나리오가 현재가의 {min(DCF[k_] for k_ in (\'low\', \'base\', \'high\')) / px * 100:.0f}~{max(DCF[k_] for k_ in (\'low\', \'base\', \'high\')) / px * 100:.0f}%로 좁게 모여 있다. 5년 성장률(연 {pct(HIST[\'growth_5y\'])})로 시작하는 “기본”이 가장 높다. “낙관”은 3년 성장률(연 {pct(HIST[\'growth_3y\'])})이 5년보다 낮은 데다 최근 4분기 이익률 {pct(HIST[\'margin_now\'])}를 그대로 이어 가, 이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 돌아가는 “보수”보다도 낮다. 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}에는 사업 최적화 비용 $0.92B(Q4 FY25 $615M, Q1 FY26 $308M)가 들어 있어 이를 빼면 약 1.3%p 높다. '
            '10월 1일 발표된 Q4 FY26 실적은 들어 있지 않다.')
NEWS_RANGE = '2025.09 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 7월 10일 — 회사채 $5.0B 발행', None,
     '2029~2036년 만기 사채 5종(변동금리 포함)', 'notes', 'Accenture 공시 (SEC 8-K)'),
    ('neutral', '2026년 6월 23일 — 자사주 매입 $2B 확대', None,
     'FY26 자사주 매입 예정액을 $7.5B로 늘림', 'buyback', 'Accenture 공시 (SEC 8-K)'),
    ('red', '2026년 6월 18일 장 시작 전 — Q3 FY26 실적', '2026-06-18',
     '매출 $18.7B(현지 통화 +3%) · EPS $3.80(+9%) · 신규 수주 $19.3B(1년 전 $19.7B) · 연간 매출 전망 상단을 5%에서 4%로 낮춤(현지 통화 3~4%) · 당일 주가 −18.0%', 'q2', 'Accenture 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 19일 장 시작 전 — Q2 FY26 실적', '2026-03-19',
     '매출 $18.0B(현지 통화 +4%) · EPS $2.93 · 신규 수주 사상 최대 $22.1B · 당일 주가 +4.3%', 'q1', 'Accenture 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 12월 18일 장 시작 전 — Q1 FY26 실적', '2025-12-18',
     '매출 $18.7B(현지 통화 +5%) · EPS $3.54(조정 $3.94) · 신규 수주 $20.9B · 당일 주가 −1.4%', 'q4', 'Accenture 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 9월 25일 장 시작 전 — Q4 FY25 실적', '2025-09-25',
     'FY25 매출 $69.7B(+7%) · 4분기 EPS $2.25(조정 $3.03) · FY26 매출 전망 현지 통화 +2~5% · 당일 주가 −2.7%', 'q3', 'Accenture 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('3분기 신규 수주가 줄고 실적 날 주가가 −18.0%였으며, 1년 새 {CH_TXT}', '수주 둔화·주가 하락',
           ['3분기 매출 $18.7B(현지 통화 +3%), EPS $3.80(+9%)였지만 신규 수주는 $19.3B로 1년 전($19.7B)보다 적었다.',
            '연간 매출 전망 상단을 5%에서 4%로 낮췄고(현지 통화 3~4%), 실적 날 주가는 −18.0%였다.',
            'FY26 자사주 매입을 $7.5B로 늘렸고, 7월에 회사채 $5.0B를 냈다.'],
           '배수는 5년 이력과 IT 비교군 모두에서 가장 싼 쪽이고, 현금흐름 모델 기본값은 주당 ${DCF[\'base\']:.2f}로 현재가와 비슷하다.',
           '10월 1일 발표된 Q4 FY26 실적(카드 기준일 뒤 — 다음 갱신 때 반영).')
BULL = [('배수', 'PER {SM[\'PER\'][\'current\']:.1f}배, 5년 중앙값의 절반 수준.'),
        ('주주환원', 'FY26 자사주 $7.5B, 배당 +10%.'),
        ('수주', '1억 달러 이상 수주가 FY26 누적 104건(전년 같은 기간 대비 +13%).')]
BEAR = [('성장 둔화', '현지 통화 성장 3%, 3분기 수주 감소.'),
        ('주가 급락', '3분기 실적 날 −18.0%.'),
        ('미국 연방', '미국 연방 정부 사업이 연간 성장을 약 1%p 깎음(회사 전망).')]
ANALYST = {'rating': 'Buy', 'n': 27, 'nt': 19, 'mean': 222.84, 'median': 220, 'low': 175, 'high': 275, 'sb': 9, 'b': 2, 'h': 16, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-10'

PRE = ["FR = {r_['metric']: r_ for ax_ in FUND['axes'].values() for r_ in ax_['rows']}"]   # 기본적 분석 지표 행(값·점수)


# ── 자동 카드(설계 D, 2026-10-10) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose.py 제안(손 표와 숫자 일치) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:Revenues"
 ],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {
  "acn:ConsultingRevenueMember": [
   "컨설팅",
   "#a100ff"
  ],
  "acn:ManagedServicesRevenueMember": [
   "매니지드 서비스",
   "#c466ff"
  ]
 },
 "ignore": []
}
