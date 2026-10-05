# BMY(브리스톨마이어스스퀴브) v2 카드 설정 — fill.py BMY. 회계연도 12월 31일. 시총 93위(S&P500 현재 시총 순, 2026-10-02 StockAnalysis 기준, 루트 카드 없음).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30), 실적 보도자료(Q3 2025~Q2 2026, SEC 접수 모두 오전 7시대 = 장 시작 전),
# 8-K(사채 공개매수 11/3·11/18, 유로 회사채 11/10, JPM 발표 1/12), StockAnalysis.
# 엔진 수정(2026-10-02): 영업이익 줄이 없어 DERIVED_OPINC = 세전이익 − "Other (income)/expense, net"(MRK 방식). Q2: 4,086 − 61 = 4,025.
# 차입금 = DebtCurrent + LongTermDebtNoncurrent — 기본 조합은 단기차입($1,027M, 1년 안 만기 사채 $768M 포함)과 유동 사채를 두 번 셌다.
BUILD = {}
CIK = '0000014272'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 12973, 'op': 4025, 'ni': 3317}   # 10-Q, 영업이익은 합성
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'Bristol Myers Squibb'
S_ = 'https://www.sec.gov/Archives/edgar/data/14272/'
SEC = S_
PR = {'q2': S_ + '000001427226000018/a2026q2ex991-filing.htm', 'q1': S_ + '000001427226000008/a2026q1ex991.htm',
      'q4': S_ + '000001427226000002/a2025q4ex991.htm', 'q3': S_ + '000001427225000147/a2025q3ex991.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000001427226000020/bmy-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'tender': S_ + '000114036125042607/ef20059419_ex99-1.htm', 'eur': S_ + '000114036125041380/ny20057651x6_8k.htm'}
FAIRBAND_TITLE = 'id="bmyFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 1년 전 PER에는 인수 연구개발비(IPRD)로 줄어든 EPS가 들어 있다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (0, 40), (0, 40)
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '설비투자(현금흐름표 “Capital expenditures”)'
STAT3 = ('성장 제품군 매출 (Q2 2026)', '$7.56B', '+15%(환율 제외 +14%) · 회사 기준 EPS $2.04')
NEXT = ('10월 하순 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('10월 하순', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('차입금은 $43.1B(1년 안 만기 $1.0B + 장기 $42.1B)이고 현금·시장성 증권은 $11.5B다. 2025년 11월에 사채 공개매수로 일부를 사들이고 유로 회사채 €5.0B를 냈다. '
               '자기자본이 $22.3B라 부채비율이 높다.')
ACT_REASON = ''
YOY_EXTRA = '성장 제품군 +15% · Eliquis +22% · 기존 제품군 −4%(Revlimid −49%) · '
SEG = [('성장 제품군(Opdivo·Reblozyl·Camzyos 등)', 7560, '#be2bbb'), ('기존 제품군(Eliquis·Revlimid 등)', 5422, '#d97ad6')]
SEG_ADJ = -9   # 기타 매출 −$9M
SEG_TITLE = '매출 구성 — 제품군별 매출'
SEG_NOTE = ('성장 제품군 +15%(Camzyos +60%·Breyanzi +41%·Reblozyl +29%), 기존 제품군 −4%(Eliquis $4.48B +22%, Revlimid −49%) · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Q2 2026 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('배당 지급 (상반기)', '$2.57B'),
           ('남은 자사주 매입 한도 (6월 말)', '약 $5B'),
           ('2026년 회사 기준 EPS 전망', '$6.75~7.00', '7월 상향')]
CHECK_WHEN = '2026년 10월 하순 (예상) · Q3 2026'
CHECK = ['연간 전망 매출 약 $49.0~50.0B, 회사 기준 EPS $6.75~7.00(4월 $6.05~6.35에서 올림)',
         'Eliquis 연간 +20~25% 전망과 기존 제품군 −4~6%',
         '하반기 주요 임상 결과(회사는 2026년 하반기에 여러 핵심 결과를 예상)',
         '차입금 $43.1B 감축']
NONOP_WHAT = '지분증권·장기 시장성 증권'
PH = ['MRK', 'PFE', 'ABBV', 'JNJ', 'GILD', 'AMGN']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '제약 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': '제약 PBR 비교', 'psr': '제약 PSR 비교',
                'pcr': '제약 PCR(FCF) 비교', 'evebitda': '제약 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-30 공시)'
PREMISE = ('주가가 1년 새 {CH_TXT} 올랐지만 이익도 늘어 PER {SM[\'PER\'][\'current\']:.1f}배(이력 중앙값 {SM[\'PER\'][\'median\']:.1f}배)는 싼 쪽이고, PBR·PCR은 비싼 쪽, PSR·EV/EBITDA는 중간이라 자기 이력 {selfsc:.1f}점(중간)이다. '
           'S&P500 헬스케어 안에서는 PER·PCR·EV/EBITDA가 싼 쪽이라 {peersc:.1f}점(싸다)이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”다. 현재가를 정당화하려면 영업이익률이 {pct(DCF[\'requiredMargin\'])}까지 올라야 한다(최근 4분기 {pct(HIST[\'margin_now\'])}). '
        '최근 두 분기 영업이익률은 28.5~31.0%다. 현금흐름 모델은 인수 연구개발비로 낮았던 과거 이익률 쪽으로 돌아간다고 보아, 회사 전망이 가리키는 이익률 수준은 반영하지 않는다.')
FUND_TIP = '자기자본이 작아 부채비율이 높다. 분기 이익률이 크게 흔들리는 것은 인수 연구개발비(IPRD)를 그 분기 비용으로 뺐기 때문이다(2025년 4분기는 인수 연구개발비·라이선스 수익 순영향 주당 −$0.60). 매출 성장은 5년 연 1~3%다. 활동성은 영업순환주기 기준이다.'
SELF_TIP = 'PER 이력은 최근 4분기 EPS가 음수였던 2024년 기간을 빼 {SM[\'PER\'][\'days\']}일이다. EV/EBITDA도 같은 이유로 이력이 짧다.'
PEER_TIP = ('S&P500 헬스케어(BMY 제외)와 배수 순위를 매긴 값이다.',
            '의료기기·보험·서비스가 섞여 있다. 차트에는 제약 6곳만 보인다.')
STORIES = ['5년 성장률의 절반이 2.5%보다 낮아 5년 내내 2.5%로 두고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})이 2.5%보다 낮아 5년 내내 2.5%로 두고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})로 시작해 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('세 값이 ${min(DCF[\'low\'], DCF[\'base\'], DCF[\'high\']):.0f}~{max(DCF[\'low\'], DCF[\'base\'], DCF[\'high\']):.0f}로 크게 벌어진다. “보수”와 “기본”의 차이는 이익률({pct(HIST[\'margin_5y\'])} 대 {pct(HIST[\'margin_2y\'])})이 아니라 재투자 가정이다. “보수”는 최근 1년 증분 매출/자본 0.30(운전자본 증가와 인수 대금 $3.7B가 든 값)을 5년 내내 쓰고, '
            '“기본”은 0.42에서 이력 평균 0.90으로 회복한다. “기본”과 “낙관”의 차이는 영업이익률(최근 2년 중앙값 {pct(HIST[\'margin_2y\'])} 대 최근 4분기 {pct(HIST[\'margin_now\'])})이다. 중앙값에는 인수 연구개발비로 이익률이 낮았던 분기가 들어 있다.')
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('green', '2026년 7월 30일 장 시작 전 — Q2 2026 실적', '2026-07-30',
     '매출 $12.97B(+6%) · EPS $1.62(회사 기준 $2.04) · 연간 매출 전망 약 $49~50B·EPS $6.75~7.00으로 상향 · 당일 주가 +2.8%', 'q2', 'Bristol Myers Squibb 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 30일 장 시작 전 — Q1 2026 실적', '2026-04-30',
     '매출 $11.49B(+3%) · EPS $1.31(회사 기준 $1.58) · 성장 제품군 +12% · 당일 주가 +5.2%', 'q1', 'Bristol Myers Squibb 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 5일 장 시작 전 — Q4 2025 실적', '2026-02-05',
     '매출 $12.50B(+1%) · EPS $0.53(회사 기준 $1.26, 인수 연구개발비·라이선스 수익 순영향 주당 −$0.60) · 당일 주가 +3.3%', 'q4', 'Bristol Myers Squibb 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 3~18일 — 사채 공개매수·유로 회사채', None,
     '11월 3일 사채 공개매수 시작, 10일 유로 회사채 €5.0B 발행, 18일 조기 응모 결과 발표(조기 정산은 20일 예정)', 'tender', 'Bristol Myers Squibb 공시 (SEC 8-K)'),
    ('green', '2025년 10월 30일 장 시작 전 — Q3 2025 실적', '2025-10-30',
     '매출 $12.22B(+3%) · EPS $1.08(회사 기준 $1.63) · 성장 제품군 +18% · 당일 주가 +7.1%', 'q3', 'Bristol Myers Squibb 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('성장 제품군과 Eliquis 매출이 늘었다. 실적 날 주가는 네 번 모두 올랐고 1년 수익률은 {CH_TXT}', '성장 제품군·전망 상향',
           ['2분기 성장 제품군 매출이 $7.56B(+15%), Eliquis가 $4.48B(+22%)였고 Revlimid는 −49%였다.',
            '7월에 연간 매출 전망을 약 $46.0~47.5B에서 $49.0~50.0B로, 회사 기준 EPS를 $6.75~7.00으로 올렸다.',
            '실적 날 주가가 네 번 모두 올랐다(+7.1%·+3.3%·+5.2%·+2.8%).'],
           '배수는 업종 안에서 싼 쪽이지만, 현금흐름 모델 기본값은 주당 ${DCF[\'base\']:.2f}로 현재가의 3분의 1 정도다.',
           'Q3 2026 실적(10월 하순 예상)과 하반기 주요 임상 결과.')
BULL = [('전망 상향', '연간 매출 전망 약 $49~50B로 상향.'),
        ('성장 제품군', 'Camzyos +60%, Breyanzi +41%, Reblozyl +29%.'),
        ('배수', 'PER {SM[\'PER\'][\'current\']:.1f}배, 업종 안에서 싼 쪽.')]
BEAR = [('특허 만료', 'Revlimid −49%, 기존 제품군 −4%.'),
        ('부채', '차입금 $43.1B, 자기자본 $22.3B.'),
        ('의견', '애널리스트 대부분 보유(Hold) 의견.')]
MISS_WHY = {('GILD', 'per'): ' 적자', ('GILD', 'evebitda'): ' 적자'}   # C9 뒤 동종 파일 PER은 perNA로 옮겨졌다 — 카드 표기 그대로
ANALYST = {'rating': 'Buy', 'n': 28, 'mean': 67.22, 'median': 70, 'low': 40, 'high': 82, 'sb': 7, 'b': 3, 'h': 17, 's': 0, 'ss': 1}
