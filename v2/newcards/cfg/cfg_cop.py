# COP(코노코필립스) v2 카드 설정 — fill.py COP. 회계연도 12월 31일. 시총 83위(S&P500 현재 시총 순, 2026-10-02 StockAnalysis 기준, 루트 카드 없음).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-06), 실적 보도자료(Q3 2025~Q2 2026), 8-K(법무책임자 은퇴 6/23, CEO 교체 8/11), StockAnalysis.
# 엔진 수정(2026-10-02): 영업이익 줄이 없어 DERIVED_OPINC(세전이익 + 이자비용, XOM·CVX 방식), 매출은 손익계산서 매출 Revenues 우선(PREFER_TAGS),
# 차입금 = DebtCurrent + LongTermDebtAndCapitalLeaseObligations, 설비투자는 회사 고유 태그(cop:PaymentToAcquireProductiveAssetsAndInvestments)를
# adapters/company_tag_feed.py로 overlay에 실었다. 2022년 분기 세전이익은 SEC 요약 데이터에 없어 그 기간 영업이익·EV/EBITDA 이력이 빈다.
BUILD = {'company_tags': [('cop:PaymentToAcquireProductiveAssetsAndInvestments', 'PaymentsToAcquireProductiveAssets')]}
CIK = '0001163165'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 19161, 'op': 6264, 'ni': 3931, 'ocf': 7434, 'cap': 3024}
VOTES, VERDICT = (0, 0, 0), '적정'
CO = 'ConocoPhillips'
S_ = 'https://www.sec.gov/Archives/edgar/data/1163165/'
SEC = S_
PR = {'q2': S_ + '000116316526000030/cop-20260806x8kexx991.htm', 'q1': S_ + '000116316526000016/cop-20260430x8kexx991.htm',
      'q4': S_ + '000116316526000005/cop-20260205x8kexx991.htm', 'q3': S_ + '000116316525000056/cop-20251106x8kexx991.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000116316526000032/cop-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'ceo': S_ + '000110465926094062/tm2622739d1_ex99-1.htm'}
FAIRBAND_TITLE = 'id="copFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 2분기 유가 상승으로 EPS가 크게 늘기 전의 PER을 곱해 범위가 넓다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
OPM_RANGE, Y2 = (10, 40), (0, 50)
FCF_SUB = '영업현금흐름 − 설비투자·투자(회사 기준 “Capital expenditures and investments”)'
CAPEX_SUB = '설비투자·투자(현금흐름표) · 2026년 계획 $12.0~12.5B'
STAT3 = ('실현 가격 (Q2 2026)', '$62.33/BOE', '+36% · 생산량 2,248 MBOED(−4%, 인수·매각 조정)')
NEXT = ('11월 초 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('11월 초', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('차입금은 $23.3B(1년 안 만기 $0.5B + 장기 $22.8B)이고 현금·단기투자는 $7.7B(제한 현금 제외, 회사 발표 기준 $8.1B)다. '
               '자산 매각 목표 $5B를 앞당겨 채웠고, 이라크 키르쿠크 지역 합작사 지분 42% 인수(연말 완료 예상)에 합의했다.')
ACT_REASON = ''
YOY_EXTRA = '실현 가격 +36% · 생산량 −4%(인수·매각 조정) · 순이익 약 2배 · '
SEG = [('미국 본토(Lower 48)', 13028, '#c8102e'), ('유럽·중동·북아프리카', 2276, '#f59e0b'), ('알래스카', 1873, '#5aa9e6'), ('캐나다', 1304, '#a78bfa'), ('아시아·태평양', 674, '#22c55e')]
SEG_ADJ = 6
SEG_TITLE = '매출 구성 — 지역별 매출'
SEG_NOTE = ('부문 간 거래를 뺀 매출 · 미국 본토가 68%(델라웨어 분지 생산 720 MBOED) · 본사·기타 $6M · '
            '출처: <a href="{TENQ}" target="_blank" rel="noopener">Q2 2026 10-Q (SEC) →</a>')
CAPITAL = [('자사주 매입 (상반기, 2분기 두 배로)', '$3.0B'),
           ('배당 지급 (상반기)', '$2.1B'),
           ('분기 배당 (2025년 4분기부터)', '$0.78 → $0.84', '+8%')]
CHECK_WHEN = '2026년 11월 초 (예상) · Q3 2026'
CHECK = ['유가·실현 가격(2분기 $62.33/BOE)과 회사 기준 CFO(운전자본 변동 제외)의 45% 주주환원 목표',
         '새 CEO(Andy O’Brien, 9월 1일 취임) 아래 전략',
         '생산량(2분기 −4%, 인수·매각 조정)과 2026년 설비투자 $12.0~12.5B',
         '이라크 키르쿠크 합작사 인수 완료와 LNG 구매 계약 12 MTPA']
NONOP_WHAT = '장기 투자'
PH = ['XOM', 'CVX', 'EOG', 'OXY', 'FANG', 'DVN']
PEER_FILE = 'peer_universe/energy.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '석유·가스 6곳 PER 비교 (점수는 S&P500 에너지 기준)', 'pbr': '석유·가스 PBR 비교', 'psr': '석유·가스 PSR 비교',
                'pcr': '석유·가스 PCR(FCF) 비교', 'evebitda': '석유·가스 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 에너지 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 에너지 대비 배수 순위 (v2/peer_universe/energy.json)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-08-06 공시)'
PREMISE = ('주가가 1년 새 {CH_TXT} 올라 PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PSR·PCR이 중앙값보다 비싸고 PBR·EV/EBITDA는 조금 싸 자기 이력 {selfsc:.1f}점(중간)이다. '
           'S&P500 에너지 안에서는 EV/EBITDA·PCR이 싼 쪽, PER·PSR·PBR은 중간이라 {peersc:.1f}점(중간)이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”이다. 현재가를 정당화하는 5년 매출 성장은 연 {pct(DCF[\'requiredGrowth\'])}로, 5년 성장률(연 {pct(HIST[\'growth_5y\'])})보다 낮다. '
        '다만 최근 4분기 이익에는 2분기 유가 급등이 들어 있다. 유가가 내려가면 이익률과 현금흐름 가치가 함께 줄어든다.')
FUND_TIP = '매출·영업이익 성장률이 음수인 것은 2022년(유가 고점)과 2025년 연간 수치를 비교하는 3년 성장률이라서다. 활동성은 영업순환주기 기준이다.'
SELF_TIP = 'PER {SM[\'PER\'][\'current\']:.1f}배는 5년 중앙값보다 비싸다. EV/EBITDA는 2022년 분기 세전이익이 SEC 요약 데이터에 없어 이력이 짧다({SM[\'EV/EBITDA\'][\'days\']}일).'
PEER_TIP = ('S&P500 에너지(COP 제외)와 배수 순위를 매긴 값이다.',
            '통합 석유사·탐사생산·정유·장비·가스관 회사가 섞여 있다. 차트에는 석유·가스 6곳만 보인다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})으로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})이 2.5%보다 낮아 5년 내내 2.5%로 두고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('“낙관”이 “기본”보다 낮다. 3년 성장률(2022년 유가 고점 뒤라 음수)이 2.5%보다 낮아 “낙관”은 5년 내내 2.5%로 크는 반면, “기본”은 5년 성장률(연 {pct(HIST[\'growth_5y\'])})로 시작한다. '
            '설비투자는 회사 기준 “설비투자·투자”(회사 고유 태그)를 썼다. 유가에 따라 이익률이 크게 움직이는 업종이라 현재 이익률을 이어 가는 가정에 민감하다.')
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 8월 6일 — CEO 교체 발표', None,
     'Ryan Lance가 사장·CEO에서 물러나 전환기 이사회 의장(executive chair)으로 남고, CFO Andy O’Brien이 9월 1일 CEO에 취임', 'ceo', 'ConocoPhillips 공시 (SEC 8-K)'),
    ('green', '2026년 8월 6일 장 시작 전 — Q2 2026 실적', '2026-08-06',
     '매출 $19.2B(+37%) · EPS $3.23(조정 $3.24) · 실현 가격 +36% · 자사주 매입 두 배 · 당일 주가 +1.5%', 'q2', 'ConocoPhillips 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 30일 장 시작 전 — Q1 2026 실적', '2026-04-30',
     '매출 $15.8B(−5%) · EPS $1.78(조정 $1.89) · 연간 생산·설비투자 전망 조정 · 당일 주가 −1.9%', 'q1', 'ConocoPhillips 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 5일 장 시작 전 — Q4 2025 실적', '2026-02-05',
     'EPS $1.17(조정 $1.02) · 2026년 설비투자 약 $12B · 당일 주가 −2.4%', 'q4', 'ConocoPhillips 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 6일 장 시작 전 — Q3 2025 실적', '2025-11-06',
     'EPS $1.38(조정 $1.61) · 분기 배당 8% 인상($0.84) · 당일 주가 −2.3%', 'q3', 'ConocoPhillips 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('실현 가격이 크게 올라 2분기 이익이 두 배가 됐고 주가는 1년 새 {CH_TXT}', '유가 상승·주주환원',
           ['2분기 실현 가격이 $62.33/BOE(+36%)로 올라 순이익이 $3.9B(1년 전 $2.0B)였다. 생산량은 인수·매각 조정 기준 −4%였다.',
            '2분기 자사주 매입을 두 배로 늘려 주주환원이 $3.0B였고, 올해 회사 기준 CFO(운전자본 변동 제외)의 45%를 돌려줄 계획이다.',
            '9월 1일 CEO가 Andy O’Brien으로 바뀌었고, 이라크 키르쿠크 합작사 지분 인수에 합의했다.'],
           '배수는 5년·업종 안에서 대체로 중간이고, 현금흐름 모델 기본값은 주당 ${DCF[\'base\']:.2f}로 현재가와 비슷하다.',
           'Q3 2026 실적(11월 초 예상)의 실현 가격과 주주환원.')
BULL = [('유가', '2분기 실현 가격 +36%, 순이익 약 2배.'),
        ('주주환원', 'CFO의 45% 환원 목표, 자사주 2분기 두 배.'),
        ('재무', '차입금 $23.3B, 현금·단기투자 $7.7B.')]
BEAR = [('유가 의존', '이익이 유가에 따라 크게 움직임.'),
        ('생산 감소', '생산량 −4%(인수·매각 조정), 중동 분쟁으로 카타르 생산 영향.'),
        ('경영 교체', '9월 1일 CEO 교체, 법무책임자 은퇴(후임 미정).')]
ANALYST = {'rating': 'Buy', 'n': 27, 'nt': 23, 'mean': 145.09, 'median': 146, 'low': 121, 'high': 189, 'sb': 15, 'b': 4, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-05'
