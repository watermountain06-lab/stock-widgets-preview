# ETN(이튼) v2 카드 설정 — _core_fill.py ETN. 회계연도 12월 31일. 시총 74위(S&P500 현재 시총 순, 루트 카드 없음).
# 배열은 v2/new_ticker_arrays.py(Yahoo 일봉). 출처: SEC XBRL, Q2 2026 10-Q(2026-07-31), 실적 보도자료(Q3 2025~Q2 2026),
# 8-K(CFO 교체 11/20·3/2, Mobility 분사 발표 1/26, 기간대출·신용한도 2/6, 회사채 3/10, Dana RMT 합의 6/11), StockAnalysis.
# 엔진 수정(2026-10-01): 손익계산서에 영업이익 줄이 없어(OperatingIncomeLoss 태그 없음) DERIVED_OPINC = 세전이익 + 순이자비용
# − 기타 영업외손익 − 사업 매각 이익. 순이자 태그가 공시마다 바뀌어 태그별 부호((태그, 배수))를 지원하도록 _derived_opinc를 넓혔다.
CIK = '0001551182'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 8531, 'op': 1392, 'ni': 821, 'ocf': 1127, 'cap': 253}   # 보도자료 손익(영업이익 = 매출 − 매출원가 − 판관비 − R&D), FCF $874M
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Eaton'
S_ = 'https://www.sec.gov/Archives/edgar/data/1551182/'
SEC = S_
PR = {'q2': S_ + '000155118226000027/etn06302026exhibit99.htm', 'q1': S_ + '000155118226000010/etn03312026exhibit99.htm',
      'q4': S_ + '000155118226000002/etn12312025exhibit99.htm', 'q3': S_ + '000155118225000033/etn09302025exhibit99.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000155118226000030/etn-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'dana': S_ + '000095014226001733/eh260792115_ex9901.htm', 'spin': S_ + '000114036126002286/ef20063889_ex99-1.htm',
         'term': S_ + '000114036126004227/ef20064951_8k.htm', 'notes': S_ + '000114036126008836/ef20067414_8k.htm',
         'cfo': S_ + '000114036126007206/ef20066779_ex99-1.htm', 'cfo_leave': S_ + '000114036125042797/ef20059654_8k.htm'}
FAIRBAND_TITLE = 'id="etnFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 올해 인수 관련 비용으로 GAAP EPS가 줄었는데 주가는 올라 지금 PER({SM[\'PER\'][\'current\']:.1f}배)이 이 구간 위에 있다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (10, 25), (-40, 60)
FCF_SUB = '영업현금흐름 − 설비투자 · 보도자료 FCF $874M(+22%)'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('부문 이익률 (Q2 2026)', '23.1%', '회사 기준 · 1년 전 23.9% · GAAP 영업이익률 16.3%')
NEXT = ('11월 초 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('11월 초', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('차입금은 $20.6B(단기 $2.1B + 장기 $18.5B)로 연초 $9.9B에서 두 배가 됐고 현금·단기투자는 $0.7B다. 3월 Boyd Thermal 인수($9.55B)와 1월 Ultra PCS 인수($1.53B)를 회사채(미국 순조달 약 $8.4B·유로 €1.2B)로 치렀다. '
               '영업권 $20.2B·무형자산 $12.6B로 연초 $20.8B에서 $32.8B가 됐다. Mobility 사업을 Dana와 합치는 거래(2027년 1분기 완료 예상)로 현금 약 $1.1B를 받는다.')
ACT_REASON = ''
YOY_EXTRA = '유기적 성장 +14%, 인수 +7% · Electrical Global +44%(Boyd Thermal 포함) · 순이익은 인수 관련 비용(주당 $0.49)과 이자비용 증가($71M → $201M)로 −16% · '
SEG = [('Electrical Americas', 3951, '#0050a0'), ('Electrical Global', 2517, '#3d86d6'), ('Aerospace', 1222, '#a78bfa'), ('Mobility', 841, '#94a3b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별 매출'
SEG_NOTE = ('1년 전보다 Electrical Americas +18%, Electrical Global +44%(Boyd Thermal 기여 25%p), Aerospace +13%, Mobility 0% · 부문 이익률은 각각 27.5%·19.8%·22.8%·13.0% · Mobility는 Dana와 합칠 예정 · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Q2 2026 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (상반기, 1년 전 $1.3B)', '없음'),
           ('배당 지급 (상반기)', '$0.86B'),
           ('분기 배당 (2026년 1분기부터)', '$1.04 → $1.10', '+6%')]
CHECK_WHEN = '2026년 11월 초 (예상) · Q3 2026'
CHECK = ['3분기 가이던스 GAAP EPS $2.77~2.87·유기적 성장 13.5~15.5%·부문 이익률 24.6~25.0%',
         '연간 GAAP EPS 가이던스 $10.36~10.56(2월 $11.57~12.07에서 두 번 낮춤, 조정 EPS는 $13.40~13.60로 올림)',
         'Electrical 수주(12개월 평균 Americas +41%)와 데이터센터 수요',
         'Dana와의 Mobility 거래 진행과 인수 뒤 차입금 $20.6B 상환']
NONOP_WHAT = '투자'
PH = ['GEV', 'EMR', 'HUBB', 'ROK', 'AME', 'VRT']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {'evebitda': 60}, {}, {}
CHART_TITLES = {'per': '전력·전기장비 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '전력·전기장비 PBR 비교', 'psr': '전력·전기장비 PSR 비교',
                'pcr': '전력·전기장비 PCR(FCF) 비교', 'evebitda': '전력·전기장비 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-31 공시)'
PREMISE = ('주가가 1년 새 {CH_TXT} 오르는 동안 GAAP EPS는 인수 관련 비용으로 줄어 PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PBR·EV/EBITDA가 5년 중 가장 비싼 쪽이고 PSR·PCR도 비싼 쪽이라 자기 이력 {selfsc:.1f}점(비싸다)이다. '
           'S&P500 산업재 81종목 안에서도 다섯 배수 모두 비싼 쪽이라 {peersc:.1f}점(비싸다)이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”다. 현재가를 정당화하려면 GAAP 영업이익률이 {pct(DCF[\'requiredMargin\'])}까지 올라야 한다(최근 4분기 {pct(HIST[\'margin_now\'])}, 5년 중앙값 {pct(HIST[\'margin_5y\'])}, 회사 부문 이익률 23.1%). '
        '현금흐름 −2는 최근 4분기 인수 대금 $11.1B(Boyd Thermal·Ultra PCS)가 재투자로 잡혀 매출 1달러를 늘리는 데 드는 자본이 크게 계산된 영향도 크다. 그 가정이 이어지면 성장해도 현금이 거의 남지 않는다.')
FUND_TIP = '이자보상배율은 인수 차입으로 이자비용이 늘어(분기 $71M → $201M) 낮아졌다. 활동성은 영업순환주기(163일)가 5년 중 긴 편이라 30점이다.'
SELF_TIP = 'PER {SM[\'PER\'][\'current\']:.1f}배는 5년 최고({SM[\'PER\'][\'max\']:.1f}배) 근처다. 조정 EPS(연간 가이던스 $13.40~13.60) 기준이면 약 32배이지만 사이트는 GAAP 희석 EPS를 쓴다.'
PEER_TIP = ('S&P500 산업재(ETN 제외 80종목)와 배수 순위를 매긴 값이다.',
            '항공·기계·운송·서비스가 섞여 있다. 차트에는 전력·전기장비 6곳만 보인다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})으로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '매출이 3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})로 시작해 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('세 값 모두 현재가보다 크게 낮다. 매출/자본을 최근 4분기 증분 값(약 0.35)에서 잡는데, 이 기간 인수 대금 $11.1B가 투하자본에 들어가 매출 1달러를 늘리려면 약 $2.8를 재투자해야 하는 것으로 계산됐다. '
            '“보수”는 그 값이 5년 내내 이어져 거의 0이고, “기본”은 이력 평균(약 0.73) 쪽으로 회복한다. 인수를 빼고 다시 계산하는 것은 사이트 규칙상 하지 않는다. 잔존가치 비중이 {DCF[\'tvShare\'] * 100:.0f}%라 할인율·영구성장 가정에 민감하다.')
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('green', '2026년 7월 31일 장 시작 전 — Q2 2026 실적', '2026-07-31',
     '매출 $8.5B(+21%, 유기적 +14%) · EPS $2.11(−16%, 조정 $3.15) · 연간 유기적 성장 가이던스 11~13%로 상향 · 당일 주가 +7.3%', 'q2', 'Eaton 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 6월 10일 — 모빌리티 사업을 다나(Dana)와 합치기로', None,
     'Mobility 사업(약 $5.1B 평가)을 Dana와 합치는 RMT 거래 — 이튼은 현금 약 $1.1B, 주주는 합친 회사 지분 50.1% 이상 · 2027년 1분기 완료 예상', 'dana', 'Eaton 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 5일 장 시작 전 — Q1 2026 실적', '2026-05-05',
     '매출 $7.5B(+17%) · EPS $2.22(−9%, 조정 $2.81) · 연간 GAAP EPS 가이던스 하향, 유기적 성장 상향 · 당일 주가 −2.7%', 'q1', 'Eaton 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 10일 — 회사채 발행', None,
     '미국 회사채(순조달 약 $8.4B)와 유로 회사채 €1.2B — Boyd Thermal 인수($9.55B, 3월 12일 완료) 자금', 'notes', 'Eaton 공시 (SEC 8-K)'),
    ('neutral', '2026년 2월 6일 — $8B 기간대출 약정', None,
     '인수 자금용 최대 $8.0B 기간대출(2026년 12월 만기)과 신용한도 증액', 'term', 'Eaton 공시 (SEC 8-K)'),
    ('green', '2026년 2월 3일 장 시작 전 — Q4 2025 실적', '2026-02-03',
     '매출 $7.1B(+13%) · EPS $2.91(+19%) · 2026년 가이던스 발표 · 당일 주가 +0.9%', 'q4', 'Eaton 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 26일 — 모빌리티 사업 분사 계획 발표', None,
     '자동차·상용차 부품 사업(Mobility)을 떼어 내겠다고 발표 — 6월에 Dana와의 합병으로 구체화', 'spin', 'Eaton 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 4일 장 시작 전 — Q3 2025 실적', '2025-11-04',
     '매출 $7.0B(+10%) · EPS $2.59(+2%, 조정 $3.07) · 당일 주가 −2.3%', 'q3', 'Eaton 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('데이터센터 수요와 Boyd Thermal 등 인수로 매출이 20% 안팎 늘고 주가는 1년 새 {CH_TXT}', '데이터센터·인수',
           ['2분기 매출 $8.5B(+21%) 가운데 유기적 성장이 14%이고 Electrical Americas 12개월 평균 수주가 +41%였다.',
            'Boyd Thermal($9.55B)·Ultra PCS($1.53B) 인수로 차입금이 $20.6B로 늘고, 인수 관련 비용으로 2분기 GAAP EPS가 $2.11(−16%)였다.',
            'Mobility 사업을 Dana와 합치기로 해(2027년 1분기 완료 예상) 전기·항공 사업 중심으로 바뀐다.'],
           'PER·PBR·EV/EBITDA가 5년 중 가장 비싼 쪽이고, 인수 대금이 재투자로 잡힌 현금흐름 모델은 기본 주당 ${DCF[\'base\']:.2f}이다.',
           'Q3 2026 실적(11월 초 예상)의 유기적 성장 13.5~15.5% 달성 여부와 부문 이익률 회복.')
BULL = [('수주', 'Electrical Americas 12개월 평균 수주 +41%, Electrical 수주잔고 +43%.'),
        ('데이터센터', 'Boyd Thermal(냉각)로 데이터센터 제품군 확대.'),
        ('사업 재편', 'Mobility를 Dana와 합쳐 고성장·고마진 사업에 집중.')]
BEAR = [('GAAP 이익', '인수 비용으로 2분기 EPS −16%, 연간 GAAP 가이던스 두 번 하향.'),
        ('부채', '차입금 $20.6B(연초 $9.9B), 이자비용 분기 $201M.'),
        ('밸류에이션', 'PER {SM[\'PER\'][\'current\']:.1f}배로 5년 중 가장 비싼 쪽.')]
ANALYST = {'rating': 'Buy', 'n': 28, 'mean': 490.42, 'median': 502, 'low': 392, 'high': 534, 'sb': 19, 'b': 5, 'h': 3, 's': 1, 'ss': 0}
