# GILD(길리어드 사이언스) v2 카드 설정 — _core_fill.py GILD. 회계연도 12월 31일. 시총 72위(S&P500 현재 시총 순, 루트 카드 없음).
# 배열은 v2/new_ticker_arrays.py(Yahoo 일봉). 출처: SEC XBRL, Q2 2026 10-Q(2026-08-06), 실적 보도자료(Q3 2025~Q2 2026),
# 8-K(Biktarvy 특허 합의 10/6, Arcellx 합의 2/23·완료 4/28, 회사채 5/20), StockAnalysis.
# 엔진 수정(2026-10-01): 현금 태그가 2022-12에 멈춰 EV_TAGS_BY_CIK cash = 제한 현금 포함 총계(재무상태표 값). 인수 IPR&D는 GAAP 유지 + 명시
# (MRK·ABBV 사용자 결정, 안건 B2) → 최근 4분기 적자로 PER·EV/EBITDA·적정주가 밴드 없음.
CIK = '0000882095'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 7803, 'op': -10394, 'ni': -10496, 'ocf': 3573}   # 보도자료 손익계산서(영업손실 = 인수 IPR&D $11.18B·IPR&D 손상 $1.75B 포함)
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Gilead'
S_ = 'https://www.sec.gov/Archives/edgar/data/882095/'
SEC = S_
PR = {'q2': S_ + '000088209526000028/exhibit991earningspressrel.htm', 'q1': S_ + '000088209526000022/exhibit991earningspressrel.htm',
      'q4': S_ + '000088209526000003/exhibit991earningspressrel.htm', 'q3': S_ + '000088209525000044/exhibit991earningspressrel.htm'}
TENQ = S_ + '000088209526000031/gild-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'bik': S_ + '000088209525000041/gild-20251006.htm', 'arcellx': S_ + '000110465926018314/tm267044d1_8k.htm',
         'arcellx_done': S_ + '000110465926049874/tm2612748d1_ex99-1.htm', 'notes': S_ + '000110465926064518/tm2615045d1_8k.htm'}
FAIRBAND_TITLE = 'id="gildFairBand" title="최근 4분기 희석 EPS가 −$2.66(2분기 인수 IPR&D·관련 세금 주당 −$9.08 포함)이라 PER 밴드를 낼 수 없다. 그 항목을 빼면 최근 4분기 EPS는 약 $6.4(PER 약 23배), IPR&D 손상 $1.75B(주당 약 $1.41)까지 빼면 약 $7.8(PER 약 19배)이다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (-140, 50), (-600, 100)
FCF_SUB = '영업현금흐름 − 설비투자 · 인수 대금(상반기 $11.3B)은 투자활동'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('HIV 제품 매출 (Q2 2026)', '$5.69B', '+12% · Biktarvy $3.8B(+7%) · Descovy +48%')
NEXT = ('10월 하순 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('10월 하순', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('차입금은 $26.2B(1년 안 만기 $2.4B + 장기 $23.8B)이고 현금·유가증권은 $3.2B로 연초 $10.6B에서 줄었다. 상반기에 인수(Arcellx 등) $11.3B, 차입금 상환 $2.8B, 배당 $2.1B, 자사주 $0.8B를 쓰고 차입(회사채 $3.0B·기간대출 $1.1B)으로 순 $4.1B를 조달했다. '
               '2분기 영업손실(−$10.4B)은 인수 IPR&D 비용 $11.18B(Arcellx $7.0B·Tubulis $3.1B·Ouro $1.9B에서 Lakefront 분담을 뺀 순 $1.0B 등)와 IPR&D 손상 $1.75B 때문이다.')
ACT_REASON = ''
YOY_EXTRA = '제품 매출(Veklury 제외) +10%, HIV +12% · 영업이익·순이익은 인수 IPR&D 비용 $11.18B와 IPR&D 손상 $1.75B로 적자 · '
SEG = [('HIV', 5693, '#c4122f'), ('간질환', 877, '#f59e0b'), ('항암(Trodelvy·세포치료)', 873, '#a78bfa'), ('기타 제품(Veklury 포함)', 184, '#94a3b8'), ('로열티·계약 수익', 176, '#5aa9e6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품군별 매출'
SEG_NOTE = ('1년 전보다 HIV +12%, 간질환 +10%, 항암 +3%(Trodelvy +26%, 세포치료 −14%), Veklury −81% · 로열티는 과거 지식재산 매각 관련 · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Q2 2026 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (상반기, 2분기 $0.36B)', '$0.77B'),
           ('배당 지급 (상반기)', '$2.1B'),
           ('분기 배당 (2026년 1분기부터)', '$0.79 → $0.82', '+4%')]
CHECK_WHEN = '2026년 10월 하순 (예상) · Q3 2026'
CHECK = ['연간 제품 매출 가이던스 $30.1~30.4B(Veklury 제외 $29.8~30.1B)와 GAAP 주당 손실 $3.40~3.75',
         'HIV 성장(2분기 +12%)과 PrEP(Descovy +48%) 확대, 주 1회 경구 PrEP 심사(목표일 2027년 2월 2일)',
         'Arcellx(anito-cel) 등 인수 자산 개발과 세포치료 매출 감소(−14%)',
         '인수 뒤 현금 $3.2B·차입금 $26.2B와 자사주 매입 속도']
NONOP_WHAT = '지분 투자'
PH = ['ABBV', 'AMGN', 'VRTX', 'BMY', 'MRK', 'REGN']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {'per': 100}, {}, {}
CHART_TITLES = {'per': '대형 바이오·제약 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': '대형 바이오·제약 PBR 비교', 'psr': '대형 바이오·제약 PSR 비교',
                'pcr': '대형 바이오·제약 PCR(FCF) 비교', 'evebitda': '대형 바이오·제약 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-08-06 공시)'
PREMISE = ('최근 4분기가 인수 IPR&D 비용으로 적자라 PER은 점수에서 빼고(PER 해당 없음, 순이익률 2% 미만 규칙) EV/EBITDA는 0점이고, 주가가 1년 새 {CH_TXT} 올라 PSR {SM[\'PSR\'][\'current\']:.1f}배·PBR {SM[\'PBR\'][\'current\']:.1f}배가 5년 중 가장 비싼 쪽이다. PCR {SM[\'PCR\'][\'current\']:.1f}배만 중간보다 조금 비싸 자기 이력 {selfsc:.1f}점({score_word(selfsc)})이다. '
           'S&P500 헬스케어 안에서도 EV/EBITDA(적자)·PBR이 가장 비싼 쪽이고 PCR만 싼 쪽이라 {peersc:.1f}점({score_word(peersc)}, PER 제외)이다. 인수 비용을 빼면 PER은 약 23배다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”다. 세 칸 모두 2분기 인수 IPR&D 비용($11.18B, GAAP 유지 규칙)의 영향을 받는다. 현금흐름 −2도 그 일회성 비용으로 음수가 된 최근 4분기 이익률을 출발점으로 삼은 결과다(5월 공시 기준 기본은 약 $57). 그 비용과 무관한 PSR도 5년 중 가장 비싼 쪽이다(PBR은 비용으로 줄어든 GAAP 자본 기준이라 높게 나온다). '
        '현재가를 정당화하려면 영업이익률이 {pct(DCF[\'requiredMargin\'])}까지 올라야 한다(5년 중앙값 {pct(HIST[\'margin_5y\'])}). 내재가치에서 빼는 것은 차입금 $26.2B이고 현금 $3.2B와 지분 투자 $2.0B를 더한다(운용리스 $0.6B는 영업이익이 임차료를 이미 뺐으므로 빼지 않는다).')
FUND_TIP = '영업이익률·순이익률·이자보상배율은 2분기 인수 IPR&D 비용으로 크게 음수다. 활동성은 영업순환주기(167일)가 5년 중 거의 가장 길어 10점이다.'
SELF_TIP = '최근 4분기 적자라 PER은 해당 없음(점수에서 뺌), EV/EBITDA는 0점이다(PER은 인수 IPR&D 제외 PER 약 23배, 5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배). PBR {SM[\'PBR\'][\'current\']:.1f}배는 인수 비용으로 자본이 줄어 5년 최고({SM[\'PBR\'][\'max\']:.1f}배) 근처다.'
PEER_TIP = ('S&P500 헬스케어(GILD 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오 외에 보험·의료기기·서비스가 섞여 있다. 적자인 EV/EBITDA는 가장 비싼 순위로 센다(GILD의 PER은 해당 없음이라 비교에서 뺀다).')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})이 영구성장률 2.5%보다 낮아 5년 내내 2.5%로 두고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})이 2.5%보다 낮아 5년 내내 2.5%로 두고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '매출이 3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})로 시작해 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}(인수 IPR&D로 음수)가 이어진다.']
DCF_NOTE = ('“낙관”과 “보수”가 음수다. “낙관”은 인수 IPR&D 비용으로 음수인 최근 4분기 영업이익률을 그대로 이어 간다. “보수”는 이익률이 2년차부터 흑자로 돌아오지만, 매출/자본을 최근 낮은 값(약 0.15, 인수로 투하자본이 커짐)으로 유지해 재투자 부담이 커서 음수다. '
            '“기본”도 이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 출발해 5년에 걸쳐 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 돌아가 1~2년차가 손실로 잡히고, 매출/자본은 이력 평균 쪽으로 회복한다. “낙관”은 성장만 낙관이고 이익률은 지금의 적자를 이어 가는 가정이라 가장 낮다. 인수 비용을 빼고 다시 계산하는 것은 사이트 규칙(GAAP 유지, 안건 B2)상 하지 않는다.')
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('red', '2026년 8월 4일 장 마감 후 — Q2 2026 실적', '2026-08-05',
     '매출 $7.8B(+10%) · 주당 손실 $8.45(인수 IPR&D·관련 세금 주당 −$9.08) · HIV +12% · 연간 제품 매출 가이던스 상향 · 다음 날 주가 −2.6%', 'q2', 'Gilead 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 20일 — 회사채 발행', None,
     '2028년 만기 등 선순위 채권 $3.0B 발행(상반기 차입 순조달은 기간대출 포함 $4.1B)', 'notes', 'Gilead 공시 (SEC 8-K)'),
    ('red', '2026년 5월 7일 장 마감 후 — Q1 2026 실적', '2026-05-08',
     '매출 $7.0B(+4%) · EPS $1.61 · Veklury 제외 제품 매출 +8% · 다음 날 주가 −2.0%', 'q1', 'Gilead 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 — Arcellx 인수 완료', None,
     '세포치료(anito-cel) 회사 Arcellx 공개매수 완료(주당 $115 현금 + 판매 연동 CVR) — 2분기에 IPR&D $7.0B 비용 처리', 'arcellx_done', 'Gilead 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 22일 — Arcellx 인수 합의', None,
     'Arcellx를 주당 $115 현금과 CVR로 인수하기로', 'arcellx', 'Gilead 공시 (SEC 8-K)'),
    ('green', '2026년 2월 10일 장 마감 후 — Q4 2025 실적', '2026-02-11',
     '매출 $7.9B(+5%) · EPS $1.74 · 분기 배당 $0.82(+4%) · 다음 날 주가 +5.8%', 'q4', 'Gilead 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 30일 장 마감 후 — Q3 2025 실적', '2025-10-31',
     '매출 $7.8B(+3%) · EPS $2.43 · Veklury 제외 제품 매출 +4% · 다음 날 주가 +1.1%', 'q3', 'Gilead 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 6일 — Biktarvy 특허 합의', None,
     '복제약 회사 세 곳과 합의 — 미국에서 해당 용량 Biktarvy 복제약은 2036년 4월 1일 전에는 나오지 않을 전망(통상적인 조기 진입 조항 있음)', 'bik', 'Gilead 공시 (SEC 8-K)'),
]
SUMMARY = ('HIV 사업이 성장하는 가운데 Arcellx 등 인수로 2분기 IPR&D 비용 $11.2B를 반영해 최근 4분기가 적자가 됐고, 주가는 1년 새 {CH_TXT}', '인수·HIV 성장',
           ['2분기 매출 $7.8B(+10%) 가운데 HIV가 $5.7B(+12%)이고 Descovy(PrEP)가 +48%였다.',
            'Arcellx($7.0B)·Tubulis($3.1B)·Ouro(순 $1.0B) 인수 IPR&D와 손상 $1.75B로 2분기 주당 손실 $8.45였다.',
            '현금·유가증권이 연초 $10.6B에서 $3.2B로 줄고 차입으로 순 $4.1B를 조달했다. Biktarvy 복제약은 특허 합의로 미국에서 2036년 4월 1일 전 진입하지 않을 전망이다(조기 진입 조항 있음).'],
           'PSR과 GAAP 기준 PBR이 5년 중 가장 비싼 쪽이고, GAAP 적자 탓에 현금흐름 모델은 “기본”만 주당 ${DCF[\'base\']:.2f}이다.',
           'Q3 2026 실적(10월 하순 예상)의 HIV 성장과 연간 제품 매출 $30.1~30.4B.')
BULL = [('HIV', 'HIV 매출 +12%, Biktarvy 복제약은 미국에서 2036년 4월 전 진입하지 않을 전망(조기 진입 조항 있음).'),
        ('파이프라인', '2분기 FDA 승인 3건·임상 3상 긍정 결과 3건.'),
        ('배당', '분기 배당 $0.82(+4%).')]
BEAR = [('적자', '2분기 주당 손실 $8.45, 연간 GAAP 주당 손실 가이던스 $3.40~3.75.'),
        ('부채', '현금·유가증권 $3.2B(연초 $10.6B), 차입금 $26.2B.'),
        ('세포치료', '세포치료 매출 −14%, Veklury −81%.')]
ANALYST = {'rating': 'Buy', 'n': 28, 'nt': 22, 'mean': 160.77, 'median': 165, 'low': 126, 'high': 180, 'sb': 16, 'b': 6, 'h': 5, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-10'
# 밴드 적중률: 8월 6일 2분기 공시로 최근 4분기 EPS가 음수(−$2.66)가 돼 그 뒤로는 PER 밴드가 뜻이 없다. 백테스트는 음수 체크포인트를 만들지 않아
# 1분기 밴드가 9/30까지 열려 있었다 → 카드 한정으로 열린 구간을 8/5에서 끊는다(Codex, 2026-10-01, 안건 C — 백테스트 공통 과제)
POST = [r'''
# A3·C9(2026-10-04) 카드 직접 수정 — 동종업 툴팁의 평균 문장
one('뒤집어 점수로 썼고 PER를 뺀 4개를 평균했다.', '뒤집어 점수로 썼고, PER은 해당 없음(순이익률 2% 미만)이라 빼고 나머지 네 개를 평균했다.')
one("    const end = cp.is_open ? lastDate : (cp.period_end_date || lastDate);",
    "    const end = cp.is_open ? (lastDate > '2026-08-05' ? '2026-08-05' : lastDate) : (cp.period_end_date || lastDate);   // 8/6부터 최근 4분기 EPS 음수 — 밴드 무의미(카드 한정, Codex)")
one("""    const cpEnd = cp => cp.is_open
      ? dataDates[dataDates.length-1]""", """    const cpEnd = cp => cp.is_open
      ? (dataDates[dataDates.length-1] > '2026-08-05' ? '2026-08-05' : dataDates[dataDates.length-1])   // 차트도 8/5에서 끊는다(카드 한정, Codex 2차)""")
one("`${cp.checkpoint_date} ~ ${cp.is_open ? '진행 중' : (cp.period_end_date || '')}`",
    "`${cp.checkpoint_date} ~ ${cp.is_open ? '2026-08-05(8/6부터 최근 4분기 EPS 음수 — 밴드 없음)' : (cp.period_end_date || '')}`")
''']
