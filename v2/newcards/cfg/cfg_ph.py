# PH(파커하니핀) v2 카드 설정 — fill.py PH. 회계연도 6월 30일(FY26 = 2025-07 ~ 2026-06). 시총 94위(S&P500 현재 시총 순, 2026-10-02 StockAnalysis 기준, 루트 카드 없음).
# 출처: SEC XBRL, FY26 10-K(2026-08-21), 실적 보도자료(Q1~Q4 FY26, SEC 접수 모두 오전 8시 전 = 장 시작 전),
# 8-K(Filtration Group 인수 합의 11/12·완료 8/13, 인수 자금 대출 12/10, 회사채 9/14), StockAnalysis.
# 엔진 수정(2026-10-02): 차입금 = LongTermDebtAndCapitalLeaseObligationsCurrent + LongTermDebtAndCapitalLeaseObligations($8,520M) — 기본 조합은 $7.8B였다.
# Filtration Group 인수($9.25B, 2026-08-13 완료)와 그 차입은 6월 말 재무에 없어 배수·현금흐름에 반영되지 않았다.
BUILD = {}
NI_TAGS = ['NetIncomeLoss', 'ProfitLoss']   # 분기 순이익을 2021년 뒤 ProfitLoss로만 낸다(비지배지분 $1M 차이)
CIK = '0000076334'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
RELEASE = {'rev': 5755, 'ni': 1092}   # 매출(보도자료 $5.8B, +9.8%), 순이익(연간 − 9개월, 보도자료 $1.1B)
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Parker'
S_ = 'https://www.sec.gov/Archives/edgar/data/76334/'
SEC = S_
PR = {'q2': S_ + '000007633426000082/exhibit991q4fy26.htm', 'q1': S_ + '000007633426000070/exhibit991q3fy26.htm',
      'q4': S_ + '000007633426000005/exhibit991q2fy26.htm', 'q3': S_ + '000007633425000068/exhibit991q1fy26.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000007633426000105/ph-20260630.htm'; TENQ_NAME = 'FY26 10-K'
LINKS = {'fg': S_ + '000119312526349148/d105152d8k.htm', 'fg_deal': S_ + '000119312525275641/d205331d8k.htm', 'notes': S_ + '000119312526390561/d45003d8k.htm'}
FAIRBAND_TITLE = 'id="phFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (10, 35), (0, 35)
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('수주 증가 (Q4 FY26)', '+19%', '항공우주 수주잔고 $8.5B(사상 최대) · 회사 기준 EPS $9.27')
NEXT = ('11월 초 예상', '일정 · Q1 FY27 (회사 미확정)'); NEXT_OP = ('11월 초', 'Q1 FY27 예상')
FY_ENDS, FY_LABEL = ('2026-06-30', '2025-06-30'), 'FY26'
HEALTH_NOTE = ('6월 말 차입금은 $8.5B(1년 안 만기 $1.8B, 기업어음 $1.0B 포함 + 장기 $6.8B)이고 리스 $0.2B는 따로, 현금은 $0.5B다. 8월 13일 Filtration Group을 현금 $9.25B에 인수하며 '
               '기간 대출 $7.75B(364일 $5.25B + 3년 $2.50B)를 빌렸고, 9월에 회사채(달러 $2.4B·유로 €2.025B)를 냈다. 이 인수 차입은 6월 말 수치에 없다. CIRCOR 항공우주 사업 인수(5월 합의)는 아직 완료 전이다.')
ACT_REASON = ''
YOY_EXTRA = '매출 +9.8%(유기적 +8.0%) · 항공우주 +13.4% · 수주 +19% · '
SEG = [('산업재 — 북미', 2221, '#1f3f7a'), ('산업재 — 해외', 1634, '#5a7fbf'), ('항공우주', 1900, '#f59e0b')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별 매출'
SEG_NOTE = ('1년 전보다 북미 +7.0%, 해외 +9.5%, 항공우주 +13.4% · 부문 영업이익률 26.5%(+2.6%p) · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Q4 FY26 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('주주환원 (FY26, 자사주+배당)', '약 $2B'),
           ('Filtration Group 인수 (2026-08-13 완료)', '$9.25B'),
           ('연간 배당 인상 (70년 연속)', '+11%', 'FY26')]
CHECK_WHEN = '2026년 11월 초 (예상) · Q1 FY27'
CHECK = ['FY27 전망 매출 +5.5~8.5%, EPS $30.00~31.00(회사 기준 $34.25~35.25) — Filtration Group·CIRCOR 제외',
         'Filtration Group 통합과 인수 뒤 차입금, CIRCOR 항공우주 사업 인수(미완료) 종결 여부',
         '수주(4분기 +19%, FY27부터는 12개월 이동 기준으로 바꿔 발표)와 항공우주 수주잔고 $8.5B',
         '산업재 회복이 이어지는지(북미 유기적 +4.9%)']
NONOP_WHAT = '투자'
PH = ['ETN', 'EMR', 'ITW', 'DOV', 'ROK', 'AME']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '산업 기계·부품 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '산업 기계·부품 PBR 비교', 'psr': '산업 기계·부품 PSR 비교',
                'pcr': '산업 기계·부품 PCR(FCF) 비교', 'evebitda': '산업 기계·부품 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
FUND_ASOF_NOTE = 'FY26 10-K (2026-08-21 공시)'
PREMISE = ('주가가 1년 새 {CH_TXT} 올라 다섯 배수가 모두 5년 중 비싼 쪽(PER {SM[\'PER\'][\'current\']:.1f}배 대 5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)이라 자기 이력 {selfsc:.1f}점(비싸다)이다. '
           'S&P500 산업재 안에서도 다섯 배수가 비싼 쪽이라 {peersc:.1f}점(비싸다)이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”다. 현재가를 정당화하려면 영업이익률이 {pct(DCF[\'requiredMargin\'])}까지 올라야 한다(최근 4분기 {pct(HIST[\'margin_now\'])}). '
        '8월에 끝난 Filtration Group 인수($9.25B)는 아직 6월 말 수치에 없다. 반영되면 그 사업의 현금흐름이 더해지는 대신 인수 차입이 빠지므로, 배수와 주당 가치가 어느 쪽으로 움직일지는 정해지지 않았다.')
FUND_TIP = '유동비율이 낮은 것은 1년 안 만기 차입·기업어음이 유동부채에 있어서다. 점수의 매출 성장은 3년 연 4.1%다(5년은 연 8.1%). 활동성은 5년 비교 이력이 부족해 판정하지 않는다.'
SELF_TIP = 'PER {SM[\'PER\'][\'current\']:.1f}배는 5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배보다 높고, EV/EBITDA·PSR은 5년 중 가장 높은 쪽이다.'
PEER_TIP = ('S&P500 산업재(PH 제외)와 배수 순위를 매긴 값이다.',
            '항공우주·방산·운송·건설이 섞여 있다. 차트에는 산업 기계·부품 6곳만 보인다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})로 시작해 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('“낙관”이 “기본”보다 조금 낮다. 3년 성장률(연 {pct(HIST[\'growth_3y\'])})이 5년 성장률(연 {pct(HIST[\'growth_5y\'])})보다 낮아, 이익률을 더 높게 두는 “낙관”의 성장 출발점이 더 낮기 때문이다. '
            'Filtration Group($9.25B, 8월 완료)의 매출·이익과 인수 차입은 들어 있지 않다.')
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 14일 — 회사채 발행', None,
     '달러 사채 $2.4B·유로 사채 €2.025B 발행 완료', 'notes', 'Parker 공시 (SEC 8-K)'),
    ('neutral', '2026년 8월 13일 — Filtration Group 인수 완료', None,
     '여과 장비 회사 Filtration Group을 현금 $9.25B(운전자본 조정 전)에 인수 완료', 'fg', 'Parker 공시 (SEC 8-K)'),
    ('green', '2026년 8월 6일 장 시작 전 — Q4 FY26 실적', '2026-08-06',
     '매출 $5.8B(+9.8%) · EPS $8.54(회사 기준 $9.27) · 수주 +19% · FY27 EPS 전망 $30.00~31.00 · 당일 주가 +7.3%', 'q2', 'Parker 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 30일 장 시작 전 — Q3 FY26 실적', '2026-04-30',
     '매출 $5.5B(+11%) · EPS $7.06(1년 전 세금 이익 기저로 −4%, 회사 기준 $8.17) · 연간 전망 상향 · 당일 주가 −4.0%', 'q1', 'Parker 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 29일 장 시작 전 — Q2 FY26 실적', '2026-01-29',
     '매출 $5.2B(+9%) · EPS $6.60(1년 전 매각 이익 기저로 −9%, 회사 기준 $7.65) · 당일 주가 +3.5%', 'q4', 'Parker 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 10일 — Filtration Group 인수 합의', '2025-11-10',
     '현금 $9.25B · 당일 주가 −0.4%', 'fg_deal', 'Parker 공시 (SEC 8-K)'),
    ('green', '2025년 11월 6일 장 시작 전 — Q1 FY26 실적', '2025-11-06',
     '매출 $5.1B · EPS $6.29(+18%) · 연간 전망 상향 · 당일 주가 +7.8%', 'q3', 'Parker 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('실적과 수주가 사상 최대였고, 주가는 1년 새 {CH_TXT} 올랐다', '수주 증가·고평가',
           ['FY26 4분기 매출 $5.8B(+9.8%), 수주 +19%, 항공우주 +13.4%였고 회사 기준 EPS는 $9.27(+21%)였다.',
            '8월 13일 Filtration Group을 $9.25B에 인수했다. 기간 대출 $7.75B를 빌렸고 9월에 회사채를 냈다.',
            'FY27 EPS 전망은 $30.00~31.00(회사 기준 $34.25~35.25)이며 이 인수는 빠져 있다.'],
           '다섯 배수가 이력·업종 모두에서 비싼 쪽이고, 현금흐름 모델 기본값은 주당 ${DCF[\'base\']:.2f}로 현재가의 3분의 1 정도다.',
           'Q1 FY27 실적(11월 초 예상)의 수주와 인수 통합.')
BULL = [('수주', '4분기 수주 +19%, 항공우주 수주잔고 $8.5B.'),
        ('이익률', '부문 영업이익률 26.5%(+2.6%p).'),
        ('배당', '70년 연속 배당 인상, FY26 +11%.')]
BEAR = [('밸류에이션', '다섯 배수 모두 5년 중 비싼 쪽.'),
        ('인수 차입', 'Filtration Group $9.25B(기간 대출 $7.75B), CIRCOR 항공우주 인수 대기.'),
        ('경기', '산업재 수요 회복에 의존.')]
ANALYST = {'rating': 'Buy', 'n': 26, 'nt': 17, 'mean': 1157.06, 'median': 1200, 'low': 850, 'high': 1358, 'sb': 16, 'b': 3, 'h': 6, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-10'
