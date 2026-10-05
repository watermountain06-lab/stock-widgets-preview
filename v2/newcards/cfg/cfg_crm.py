# CRM(세일즈포스) v2 카드 설정 — _core_fill.py CRM. 회계연도 1월 31일(Q2 FY27 = 2026-05~07).
# 출처: SEC XBRL, Q2 FY27 10-Q(2026-08-27), 실적 보도자료(Q3 FY26~Q2 FY27), 8-K(Informatica 11/18, 회사채 3/13, ASR 3/16, 사장 8/5), StockAnalysis.
# 엔진 수정(2026-10-01): 본업 기준 PER(core_earnings.json — 전략 투자 평가이익), 이자비용 손입력(interest_extra.json, 태그가 2025-10에 멈춤).
CIK = '0001108524'
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q2 FY27', 'Q2 FY26', 'Q1 FY27'
L8 = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27', 'Q2 FY27']
RELEASE = {'rev': 11345, 'op': 2331, 'ni': 3526}
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'Salesforce'
S_ = 'https://www.sec.gov/Archives/edgar/data/1108524/'
SEC = S_
PR = {'q2': S_ + '000110852426000187/crm-q2fy27xexhibit991.htm', 'q1': S_ + '000110852426000125/crm-q1fy27xexhibit991.htm',
      'q4': S_ + '000110852426000056/crm-q4fy26xexhibit991.htm', 'q3': S_ + '000110852425000234/crm-q3fy26xexhibit991.htm'}
TENQ = S_ + '000110852426000190/crm-20260731.htm'; TENQ_NAME = 'Q2 FY27 10-Q'
LINKS = {'infa': S_ + '000110852425000207/ex991-infaclosingpressrele.htm', 'asr': S_ + '000119312526107403/d887663dex991.htm',
         'pres': S_ + '000110852426000160/crm-20260805.htm'}
FAIRBAND_TITLE = 'id="crmFairBand" title="최근 1년 본업 PER 25~75% 구간({float(Decimal(str(FB[\'per_p25\'])).quantize(Decimal(\'0.1\'), ROUND_HALF_UP)):.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 본업 EPS ${eps_ttm}(10달러 단위 반올림). 본업 이익은 (영업이익 + 순이자) × (1 − 실효세율)이라 전략 투자 평가이익이 빠지고 이자비용은 들어간다(A8 2026-10-04). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (10, 30), (0, 35)
FCF_SUB = '영업현금흐름 − 설비투자 · 회사 FCF $1.1B(+81%)'
CAPEX_SUB = '설비투자(현금흐름표)'
STAT3 = ('cRPO (Q2 FY27)', '$33.5B', '1년 안 계약 잔고 +14% · Agentforce·Data 360 ARR 약 $3.9B')
NEXT = ('12월 초 예상', '일정 · Q3 FY27 (회사 미확정)'); NEXT_OP = ('12월 초', 'Q3 FY27 예상')
FY_ENDS, FY_LABEL = ('2026-01-31', '2025-01-31'), 'FY2026'
HEALTH_NOTE = ('차입금은 $39.3B로 연초 $14.4B(1년 안 $4.0B + 장기 $10.4B)에서 늘었다. 3월에 만기 2028~2066년 회사채를 냈고, 같은 달 $25B 가속 자사주 매입(ASR)으로 약 1억300만 주를 먼저 받았다(10월 정산 예정). '
               '그 사이 자기자본은 $59.1B에서 $38.4B로 줄었다. 현금·유가증권은 $11.4B다. 이자보상배율은 2분기 영업이익 ÷ 10-Q 이자비용 $473M(손입력)이다. '
               '매입채무가 2019년 뒤 미지급비용과 한 줄로만 공시돼 활동성 5년 비교를 하지 않는다.')
ACT_REASON = '매입채무 표준 태그가 2019년에 멈춤'
YOY_EXTRA = '매출 +11%에 Informatica $456M 포함 · 공시 순이익에는 전략 투자 평가이익 $2,613M이 들어 있다 · '
SEG = [('구독·지원', 10820, '#00a1e0'), ('전문 서비스·기타', 525, '#94a3b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 구독 대 서비스'
SEG_NOTE = ('1년 전보다 구독·지원 +12%(Informatica $440M 포함), 전문 서비스 −4% · Agentforce ARR $1.5B 넘음(+240% 넘게) · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Q2 FY27 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('가속 자사주 매입 (3월 ASR, 10월 정산 예정)', '$25B'),
           ('인수 (Informatica 2025년 11월 종결 · Contentful·Fin 합의)', '진행 중'),
           ('배당 (Q2 FY27 지급)', '분기 배당', '$0.36B')]
CHECK_WHEN = '2026년 12월 초 (예상) · Q3 FY27'
CHECK = ['3분기 가이던스 매출 $11.42~11.50B(+11~12%)와 cRPO 성장 약 14%',
         '연간 매출 가이던스 $46.1~46.4B·GAAP 영업이익률 20.1%·비GAAP 34.3%',
         'Agentforce·Data 360 ARR(2분기 약 $3.9B)과 하반기 유기적 매출 재가속',
         '10월 ASR 정산 뒤 주식 수와 늘어난 차입금($39.3B)의 이자(2분기 $473M)']
NONOP_WHAT = '전략 투자 등'
PH = ['MSFT', 'ORCL', 'PLTR', 'PANW', 'CRWD', 'IBM']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {'per': 200, 'pcr': 150, 'evebitda': 120}, {'per': ' · CRM은 본업 기준'}
CHART_TITLES = {'per': '소프트웨어 6곳 PER 비교 (점수는 IT 카드 유니버스 전체)', 'pbr': '소프트웨어 PBR 비교', 'psr': '소프트웨어 PSR 비교',
                'pcr': '소프트웨어 PCR(FCF) 비교', 'evebitda': '소프트웨어 EV/EBITDA 비교'}
MISS_WHY = {('CRWD', 'evebitda'): ' 값 없음'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다. 본인 PER은 본업 기준이라 동종업 비교에서 뺀다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위(PER은 본업 기준이라 제외)'
FUND_ASOF_NOTE = 'Q2 FY27 10-Q (2026-08-27 공시)'
PREMISE = ('본업 PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PSR·PCR·EV/EBITDA가 5년 중 싼 쪽이고 PBR만 비싼 쪽인데, 3월 $25B 자사주 매입으로 자기자본이 $59.1B에서 $38.4B로 줄어서다. 그래서 자기 이력은 {selfsc:.1f}점(싸다)이다(PBR을 빼도 결과는 같다). '
           '카드 유니버스 IT(반도체·하드웨어 포함 23~27종목) 안에서도 PBR·PSR·PCR이 가장 싼 쪽, EV/EBITDA가 중간이라 {peersc:.1f}점(싸다)이다(PER은 본업 기준이라 비교에서 뺐다). '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”이다. 배수 두 칸이 싸다고 보지만 현금흐름 모델이 −2라 상쇄된다. 현재가를 설명하려면 영업이익률이 {pct(DCF[\'requiredMargin\'])}여야 한다(최근 4분기 {pct(HIST[\'margin_now\'])}, 회사 비GAAP 2분기 34.1%). '
        '잔존가치가 내재가치의 {DCF[\'tvShare\'] * 100:.0f}%라 영구성장률·할인율 가정에 크게 기댄다. 최근 4분기 PER은 전략 투자 평가이익을 빼려고 본업 이익((영업이익 + 순이자) × (1 − 세율))으로 낸다 — ASR 차입 뒤 늘어난 이자비용(2분기 $473M)도 뺀다. '
        '애널리스트 목표가($272)는 비GAAP 이익 기준이고, 이 카드는 주식보상·상각을 비용으로 본 GAAP 영업이익에서 출발해 차이가 크다. 예상밴드와 밴드 적중률은 GAAP EPS(전략 투자 이익 포함) 기준이라 적정주가와 기준이 다르다.')
FUND_TIP = '순이익률은 본업 기준((영업이익 + 순이자) × (1 − 세율), 전략 투자 평가이익 제외)이다. 매출 3년 CAGR 9.8%는 연간 FY2023→FY2026, 영업이익 CAGR 100.7%는 FY2023 영업이익($1.03B)이 작았던 기저효과다(FY2026 $8.33B). 이자보상배율은 10-Q 2분기 이자비용 $473M을 손입력해 계산했다(기본적 분석이 읽는 이자비용 태그가 2025-10에 멈췄고, 회사는 그 뒤 다른 태그로 낸다 — 본업 PER은 그 태그를 이어 읽는다).'
SELF_TIP = '본업 PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PSR·PCR·EV/EBITDA는 5년 중 싼 쪽, PBR은 비싼 쪽이다. 5년 PER 중앙값이 높은 것은 2021~2023년 영업이익이 작았던 구간 때문이다.'
PEER_TIP = ('카드 유니버스 IT 종목과 배수 순위를 매긴 값이다. CRM의 PER은 본업 기준이라 동종업(공시 EPS 기준) 비교에서 뺐다.',
            '소프트웨어 외에 반도체·하드웨어가 섞여 있다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})에서 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('성장을 더 낮게 잡은 낙관(3년 연 {pct(HIST[\'growth_3y\'])})이 기본(${DCF[\'base\']:.0f})보다 조금 높은(${DCF[\'high\']:.0f}) 것은 투하자본 수익률(약 12%)이 할인율 10%에 가까워 매출 성장에 드는 재투자가 이익을 거의 상쇄하기 때문이다. 비영업 자산(전략 투자 등) 주당 ${DCF[\'nonopPerShare\']:.2f}가 기본에 들어 있다. '
            'GAAP 영업이익에는 주식보상·인수 무형자산 상각이 들어 있어 회사 비GAAP 영업이익률(34%)보다 낮다.')
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('', '2026년 8월 26일 장 마감 후 — Q2 FY27 실적', '2026-08-27',
     '매출 $11.3B(+11%) · cRPO $33.5B(+14%) · GAAP EPS $4.29(전략 투자 이익 포함)·비GAAP $5.90 · 연간 매출 가이던스 $46.1~46.4B로 상향', 'q2', 'Salesforce 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 5일 장 마감 후 — 사장 퇴임', '2026-08-06',
     '스리니 탈라프라가다 사장 겸 최고엔지니어링·고객성공책임자가 8월 6일 물러나 CEO 특별고문으로', 'pres', 'Salesforce 공시 (SEC 8-K)'),
    ('', '2026년 5월 27일 장 마감 후 — Q1 FY27 실적', '2026-05-28',
     '매출 $11.1B(+13%) · cRPO $33.6B(+14%) · GAAP EPS $2.42(+52%)·비GAAP $3.88(+50%)', 'q1', 'Salesforce 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 16일 개장 전 — $25B 자사주 매입 선급', '2026-03-16',
     '3월 11일 맺은 $25B 가속 자사주 매입(ASR) 대금을 먼저 내고 약 1억300만 주를 우선 받았다(10월 정산 예정)', 'asr', 'Salesforce 공시 (SEC 8-K)'),
    ('', '2026년 2월 25일 장 마감 후 — Q4 FY26 실적', '2026-02-26',
     'RPO $72.4B(+14%) · cRPO $35.1B(+16%, Informatica 4%p 포함) · 4분기 구독·지원 매출 $10.7B(+13%)', 'q4', 'Salesforce 실적 보도자료 (SEC 8-K)'),
    ('', '2025년 12월 3일 장 마감 후 — Q3 FY26 실적', '2025-12-04',
     '매출 $10.3B(+9%) · cRPO $29.4B(+11%) · GAAP 영업이익률 21.3%', 'q3', 'Salesforce 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 18일 장 마감 후 — Informatica 인수 종결', '2025-11-19',
     'Informatica 인수를 마치고 대금 일부를 대출 $6B(364일 $4B + 3년 $2B)로 마련', 'infa', 'Salesforce 공시 (SEC 8-K)'),
]
SUMMARY = ('AI 제품(Agentforce·Data 360) 계약이 빠르게 늘고 $25B 자사주 매입을 진행하며, 주가는 1년 새 {CH_TXT}', '배수 싸짐·자사주',
           ['2분기 매출 $11.3B(+11%), cRPO $33.5B(+14%)였고, 연간 매출 가이던스를 $46.1~46.4B로 $200M 올렸다(유기적 $100M, 인수 예정 Contentful·Fin $200M, 환율 −$100M).',
            'Agentforce·Data 360 ARR이 약 $3.9B로 커졌다(Informatica Cloud ARR 포함).',
            '3월 $25B 가속 자사주 매입으로 약 1억300만 주를 먼저 받았고, 차입금은 $39.3B로 늘었다.'],
           '배수는 자기 이력과 IT 카드 유니버스 모두에서 싼 쪽이지만, 현금흐름 모델은 현재가의 {DCF[\'base\'] / px * 100:.0f}%만 설명해 합계가 “적정”이다.',
           'Q3 FY27 실적(12월 초 예상)의 cRPO 성장 약 14%와 ASR 정산.')
BULL = [('계약', 'cRPO $33.5B(+14%, Informatica 기여 포함), RPO $66.3B(+11%).'),
        ('AI', 'Agentforce·Data 360 ARR 약 $3.9B(1분기 $3.4B 중 $1.1B는 Informatica Cloud), Agentforce ARR은 2분기부터 Slackbot 등을 넣어 $1.5B.'),
        ('배수', '본업 PER {SM[\'PER\'][\'current\']:.1f}배(이자비용을 뺀 이익 기준 — 3월 사채 발행으로 분기 이자비용이 $473M), PCR {SM[\'PCR\'][\'current\']:.1f}배로 5년 중 싼 쪽.')]
BEAR = [('부채', '차입금이 연초 $14.4B에서 $39.3B로 늘었고 2분기 이자비용은 $473M이다.'),
        ('성장', '매출 +11% 가운데 Informatica($456M)가 약 4.5%p라 유기적 성장은 약 6%다.'),
        ('일회성', '2분기 GAAP EPS $4.29에 전략 투자 평가이익 $2.6B가 들어 있다.')]
ANALYST = {'rating': 'Buy', 'n': 55, 'mean': 271.69, 'median': 275, 'low': 160, 'high': 400, 'sb': 32, 'b': 6, 'h': 15, 's': 2, 'ss': 0}

POST = [r'''
h = h.replace('기본 시나리오 $${Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base)} = 사업 가치 $${Math.round(D.base) - Math.round(n)} + 비영업 자산 $${Math.round(n)}', '기본 시나리오 $${D.base.toFixed(2)} = 사업 가치 $${(D.base - n).toFixed(2)} + 비영업 자산 $${n.toFixed(2)}', 1)
''']
