# VRTX(버텍스) v2 카드 설정 — fill.py VRTX. 회계연도 12월 31일. 시총 90위(S&P500 현재 시총 순, 2026-10-02 StockAnalysis 기준, 루트 카드 없음).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-04), 실적 보도자료(Q3 2025~Q2 2026, SEC 접수 모두 오후 4시대 = 장 마감 뒤),
# 8-K(Crinetics 인수 합의 7/7, povetacicept 신청 완료 3/31, CFO 교체 9/1), StockAnalysis.
# 엔진 수정(2026-10-02): 차입금이 없다 — LongTermDebt가 2011-09($105M)에 멈춘 값이라 쓰지 않는다(DEBT_TOTAL_TAG). 현금흐름에는 금융리스($112M)를 따로 더하지만 배수 EV에는 들어가지 않는다(영향 작음, Codex).
BUILD = {}
CIK = '0000875320'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 3334, 'op': 1247, 'ni': 1100}   # 10-Q
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Vertex'
S_ = 'https://www.sec.gov/Archives/edgar/data/875320/'
SEC = S_
PR = {'q2': S_ + '000087532026000256/ex-991_q22026.htm', 'q1': S_ + '000087532026000171/ex-991_q12026.htm',
      'q4': S_ + '000087532026000034/ex-991_q42025.htm', 'q3': S_ + '000087532025000230/ex-991_q32025.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000087532026000259/vrtx-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'cfo': S_ + '000087532026000264/vrtx-20260827.htm', 'crnx': S_ + '000119312526296710/d113650d8k.htm', 'pove': S_ + '000087532026000147/vrtx-20260331.htm'}
FAIRBAND_TITLE = 'id="vrtxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
OPM_RANGE, Y2 = (10, 50), (0, 50)
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('비CF 제품 매출 (Q2 2026)', '$126M', 'CASGEVY $76M · JOURNAVX $50M')
NEXT = ('11월 초 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('11월 초', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('6월 말(Crinetics 인수 전) 차입금이 없고 현금·시장성 증권은 $13.6B다(연초 $12.3B). Crinetics 인수(약 $10.0B, 현금)는 보유 현금과 7월에 맺은 $4.5B 기간 대출로 치를 예정이다. '
               '리스 부채가 약 $2.1B 있다.')
ACT_REASON = ''
YOY_EXTRA = '낭포성 섬유증(CF) 치료제가 매출의 96% · CASGEVY $76M(1년 전 $30M) · JOURNAVX $50M(1년 전 $12M) · '
SEG = [('낭포성 섬유증(CF) 치료제', 3207.9, '#4b2e83'), ('CASGEVY(유전자 치료)', 76.4, '#8a6fbf'), ('JOURNAVX(진통제)', 49.6, '#f59e0b')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품별 매출'
SEG_NOTE = ('CF 치료제(TRIKAFTA·ALYFTREK 등)가 96% · 미국 매출 +11%, 미국 밖 +14% · '
            '출처: <a href="{TENQ}" target="_blank" rel="noopener">Q2 2026 10-Q (SEC) →</a>')
CAPITAL = [('자사주 매입 (2분기, 110만 주)', '$0.46B'),
           ('Crinetics 인수 (3분기 완료 예정, 10월 2일 현재 완료 공시 없음)', '약 $10.0B'),
           ('배당', '없음', '자사주로만 환원')]
CHECK_WHEN = '2026년 11월 초 (예상) · Q3 2026'
CHECK = ['연간 매출 전망 $13.1~13.2B(8월 실적 때 올림)과 비CF 제품 $500M 이상',
         'povetacicept(IgA 신장병) FDA 결정일 11월 30일',
         'Crinetics 인수 완료 여부(3분기 예정이었으나 10월 2일 현재 완료 공시 없음)와 기간 대출 사용',
         'CASGEVY 투여·JOURNAVX 처방 증가']
NONOP_WHAT = '장기 시장성 증권'
PH = ['REGN', 'AMGN', 'GILD', 'BIIB', 'INCY', 'LLY']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '바이오 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': '바이오 PBR 비교', 'psr': '바이오 PSR 비교',
                'pcr': '바이오 PCR(FCF) 비교', 'evebitda': '바이오 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-08-04 공시)'
PREMISE = ('주가가 1년 새 {CH_TXT} 올라 PER {SM[\'PER\'][\'current\']:.1f}배(이력 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PCR·EV/EBITDA·PSR이 중앙값보다 비싸 자기 이력 {selfsc:.1f}점({score_word(selfsc)})이다. '
           'S&P500 헬스케어 안에서는 PSR·PCR이 비싼 쪽이라 {peersc:.1f}점({score_word(peersc)})이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”다. 현재가를 정당화하려면 5년 매출 성장이 연 {pct(DCF[\'requiredGrowth\'])}여야 한다(실제 5년 연 {pct(HIST[\'growth_5y\'])}). '
        '현금흐름 모델은 지나간 실적만 쓰고, 신약(povetacicept)·Crinetics 제품의 앞으로의 매출은 넣지 않는다.')
FUND_TIP = '차입금이 없고 영업이익률이 30%대라 기본적 분석 점수가 높다. 2025년 1분기 이익률이 낮은 것은 무형자산 손상 $379M 때문이다. 활동성은 영업순환주기 기준이다.'
SELF_TIP = 'PER 이력은 최근 4분기 EPS가 음수였던 2024년 기간을 빼 {SM[\'PER\'][\'days\']}일이다. 다섯 배수 모두 이력 중앙값보다 높다.'
PEER_TIP = ('S&P500 헬스케어(VRTX 제외)와 배수 순위를 매긴 값이다.',
            '제약·의료기기·보험·서비스가 섞여 있다. 차트에는 바이오·제약 6곳만 보인다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})로 시작해 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('세 시나리오가 현재가의 {min(DCF[k] for k in (\'low\', \'base\', \'high\')) / px * 100:.0f}~{max(DCF[k] for k in (\'low\', \'base\', \'high\')) / px * 100:.0f}%로 좁게 모여 있다. 성장률(연 {min(HIST[\'growth_5y\'] / 2, HIST[\'growth_5y\'], HIST[\'growth_3y\']) * 100:.0f}~{max(HIST[\'growth_5y\'] / 2, HIST[\'growth_5y\'], HIST[\'growth_3y\']) * 100:.0f}%)과 영업이익률({min(HIST[k] for k in (\'margin_now\', \'margin_2y\', \'margin_5y\')) * 100:.0f}~{max(HIST[k] for k in (\'margin_now\', \'margin_2y\', \'margin_5y\')) * 100:.0f}%)이 서로 엇갈려 값 차이가 작다. '
            '비영업 자산(장기 시장성 증권, 주당 약 ${DCF[\'nonopPerShare\']:.0f})이 기본값에 들어 있다. Crinetics 인수 대금(약 $10.0B)은 아직 반영되지 않았다.')
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 1일 — CFO 교체 발표', None,
     '2027년 1월 1일부터 Jonathan Poole(재무 부사장)이 CFO, Charles Wagner는 COO로 남음', 'cfo', 'Vertex 공시 (SEC 8-K)'),
    ('green', '2026년 8월 3일 장 마감 뒤 — Q2 2026 실적', '2026-08-04',
     '매출 $3.33B(+12%) · EPS $4.31 · 연간 매출 전망 $13.1~13.2B로 상향 · povetacicept FDA 결정일 11월 30일 · 다음 날 주가 +1.7%', 'q2', 'Vertex 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 6일 — Crinetics 인수 합의', '2026-07-06',
     '내분비 질환 치료제 회사 Crinetics를 주당 $85 현금(지분 가치 약 $10.0B)에 인수 · 3분기 완료 예정 · 당일 주가 +0.3%', 'crnx', 'Vertex 공시 (SEC 8-K)'),
    ('red', '2026년 5월 4일 장 마감 뒤 — Q1 2026 실적', '2026-05-05',
     '매출 $2.99B(+8%) · EPS $4.02(1년 전 $2.49, 당시 무형자산 손상 $379M) · 연간 전망 유지 · 다음 날 주가 −1.3%', 'q1', 'Vertex 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 31일 — povetacicept 허가 신청 완료', None,
     'IgA 신장병 치료제 povetacicept의 신속 승인 신청을 마쳤고, 우선 심사권을 써 6개월 심사를 예상', 'pove', 'Vertex 공시 (SEC 8-K)'),
    ('green', '2026년 2월 12일 장 마감 뒤 — Q4 2025 실적', '2026-02-13',
     '매출 $3.19B(+10%) · EPS $4.65 · 2026년 매출 전망 $12.95~13.1B · 다음 날 주가 +5.7%', 'q4', 'Vertex 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 3일 장 마감 뒤 — Q3 2025 실적', '2025-11-04',
     '매출 $3.08B(+11%) · EPS $4.20 · 연간 매출 전망 $11.9~12.0B로 좁힘 · 다음 날 주가 −1.0%', 'q3', 'Vertex 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('CF 치료제로 매출이 꾸준히 늘었고 주가는 1년 새 {CH_TXT} 올랐다', '안정 성장·고평가',
           ['2분기 매출 $3.33B(+12%) 가운데 CF 치료제가 96%였고, CASGEVY·JOURNAVX가 $126M로 늘었다.',
            '7월에 Crinetics를 약 $10.0B에 인수하기로 했고, 8월 실적 때 연간 매출 전망을 $13.1~13.2B로 올렸다.',
            'povetacicept(IgA 신장병)의 FDA 결정일이 11월 30일이다.'],
           '이력에서는 다섯 배수 모두, 업종 안에서는 PSR·PCR이 비싼 쪽이고, 현금흐름 모델 기본값은 주당 ${DCF[\'base\']:.2f}로 현재가의 절반 정도다.',
           'Q3 2026 실적(11월 초 예상)과 povetacicept FDA 결정(11월 30일).')
BULL = [('CF 독점', 'CF 치료제 매출 $3.2B, 계속 증가.'),
        ('재무', '6월 말 차입금 없음, 현금·증권 $13.6B(인수 전).'),
        ('신약', 'povetacicept FDA 결정 11월 30일, Crinetics 인수.')]
BEAR = [('밸류에이션', '다섯 배수 모두 이력 중앙값보다 비쌈.'),
        ('집중', '매출의 96%가 CF 치료제.'),
        ('인수 부담', 'Crinetics 약 $10.0B, 기간 대출 $4.5B.')]
MISS_WHY = {('GILD', 'per'): ' 적자', ('GILD', 'evebitda'): ' 적자'}   # C9 뒤 동종 파일 PER은 perNA로 옮겨졌다 — 카드 표기 그대로
ANALYST = {'rating': 'Buy', 'n': 32, 'nt': 20, 'mean': 573.3, 'median': 585, 'low': 350, 'high': 665, 'sb': 20, 'b': 6, 'h': 4, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-06'
