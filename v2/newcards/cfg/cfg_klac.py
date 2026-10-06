# KLAC(KLA) v2 카드 설정 — fill.py KLAC. 회계연도 6월 30일(Q4 FY26 = 2026-04-01~06-30, 최신 공시는 FY2026 10-K). 2026-06-12 10:1 분할.
# 틀 시절 카드(2026-09 루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G2).
# 출처: SEC XBRL, FY2026 10-K(2026-08-06), 실적 보도자료(Q1~Q4 FY26), 8-K(배당·자사주 3/12, 분할 5/7), StockAnalysis(2026-10-01).
# 엔진: 손익계산서에 영업이익 줄이 없어 DERIVED_OPINC(세전이익 + 이자비용 − 기타수익 + 채무 상환 손익), 단기투자 STI 태그 — build_multiple_history.
# 재현 모드: python3 v2/newcards/build.py KLAC --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-30).
CIK = '0000319201'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
RELEASE = {'rev': 3657.6, 'op': 1553.9, 'ni': 1363.1}   # Q4 FY26 실적 보도자료(백만 달러, 순이익 1,363,059천, 영업이익은 세전 1,549.4 + 이자 73.3 − 기타수익 68.7)
RELEASE_TOL = 1
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'KLA'
S_ = 'https://www.sec.gov/Archives/edgar/data/319201/'
SEC = S_
PR = {'q4': S_ + '000031920126000024/exhibit991earningsrelease7.htm', 'q3': S_ + '000031920126000014/exhibit991earningsrelease3.htm',
      'q2': S_ + '000031920126000006/exhibit991earningsrelease1.htm', 'q1': S_ + '000031920125000031/exhibit991earningsrelease0.htm'}
PR_CUR = 'q4'
TENQ = S_ + '000031920126000027/klac-20260630.htm'; TENQ_NAME = 'FY2026 10-K'
LINKS = {'split': S_ + '000119312526212093/d116682d8k.htm', 'div': S_ + '000119312526102999/d105235d8k.htm'}
FAIRBAND_TITLE = 'id="klacFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (마진 100%로도 불가)</span>'
OPM_RANGE, Y2 = (30, 50), (30, 50)
FCF_SUB = '영업현금흐름 − 설비투자 · FY2026 합계 $3.77B'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('R&amp;D (Q4 FY26)', '$0.40B', '연구개발 · 매출의 10.9%')
NEXT = ('10월 하순 예상', '일정 · Q1 FY27 (회사 미확정)'); NEXT_OP = ('10월 하순', 'Q1 FY27 예상')
FY_ENDS, FY_LABEL = ('2026-06-30', '2025-06-30'), 'FY2026'
HEALTH_NOTE = ('차입금은 회사채 원금 $5.95B(장부가 $5.89B, 만기 2029~2062년)이고 현금 $1.65B·시장성 증권 $3.25B(채권 $3.21B + 상장 지분 $0.05B)가 있다. '
               '이자보상배율·영업이익률·순이익률은 4분기가 10-K로 나와 FY2026 연간 값이다(이자비용 $284M). 활동성은 매출채권·재고·매입채무로 계산한다.')
ACT_REASON = ''
YOY_EXTRA = ''
SEG = [('반도체 공정 제어', 3256.8, '#0f6eb4'), ('특수 반도체 공정', 159.7, '#c8102e'), ('PCB·부품 검사', 241.1, '#94a3b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별 매출'
SEG_NOTE = ('1년 전보다 반도체 공정 제어 +13.2%, PCB·부품 검사 +56.5% · FY2026 지역별로 중국 29.8%·대만 26.8%·한국 13.5%(10-K) · 출처: '
            '<a href="{PR[\'q4\']}" target="_blank" rel="noopener">Q4 FY26 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (Q4 FY26)', '$0.57B'),
           ('잔여 바이백 승인 한도 (2026.06.30 기준)', '$9.74B'),
           ('배당 (Q4 FY26 지급)', '3월 21% 인상 → 분할 후 분기 $0.23', '$0.31B')]
CHECK_WHEN = '2026년 10월 하순 (예상) · Q1 FY27'
CHECK = ['1분기 전망 — 매출 $4.0B ± $0.2B, GAAP EPS $1.14 ± $0.10',
         '회사가 말한 2026년 하반기~2027년 수요 가속(AI 인프라·첨단 패키징)이 수주로 이어지는지',
         '중국 매출 비중(FY2026 29.8%, 2년 전 42.8%)과 미국 수출 규제',
         '자사주 매입($9.74B 한도)과 분할 후 배당']
NONOP_WHAT = '지분·장기투자'
PH = ['LRCX', 'AMAT', 'ASML', 'NVDA', 'MU', 'TXN']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {'per': ' (점수는 IT 카드 유니버스 기준)'}
CHART_TITLES = {'per': '반도체 장비·반도체 6곳 PER 비교', 'pbr': '반도체 장비 PBR 비교', 'psr': '반도체 장비 PSR 비교',
                'pcr': '반도체 장비 PCR(FCF) 비교', 'evebitda': '반도체 장비 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
FUND_ASOF_NOTE = 'FY2026 10-K (2026-08-06 공시)'
PREMISE = ('주가가 1년 새 {ch:+.0f}% 올라 PER {SM[\'PER\'][\'current\']:.1f}배·PSR·PBR·PCR이 5년 중, EV/EBITDA가 {SM[\'EV/EBITDA\'][\'days\'] / 252:.1f}년 중 상위 {max(100 - SM[k][\'percentile\'] for k in (\'PER\', \'PSR\', \'PBR\', \'PCR\', \'EV/EBITDA\')):.0f}% 안이라 자기 이력 {selfsc:.1f}점이다. '
           '카드 유니버스 IT 안에서도 PBR·PSR·PCR이 비싼 쪽이라 {peersc:.1f}점이다. <strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {sgn(VOTES[0])}·{sgn(VOTES[1])}·{sgn(VOTES[2])}{jo_ro(VOTES[2])} 합계 {TOTAL_TXT} “{VERDICT}”다. 영업이익률을 100%로 올려도 현재가에 닿지 않고, '
        '성장으로만 맞추려면 5년 내내 연 {pct(DCF[\'requiredGrowth\'])}가 필요하다(지난 5년 {pct(HIST[\'growth_5y\'])}, 3년 {pct(HIST[\'growth_3y\'])}). '
        '낙관 시나리오(${DCF[\'high\']:.0f})가 기본(${DCF[\'base\']:.0f})보다 낮은 것은 3년 성장률이 5년보다 낮아서다.')
FUND_TIP = '부채비율 2점은 자사주 매입으로 자본($6.3B)이 작아서다. 영업이익은 손익계산서에 줄이 없어 세전이익 + 이자 − 기타수익으로 계산했다.'
SELF_TIP = ('PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)를 비롯해 다섯 배수가 모두 5년 중 비싼 쪽이다. '
            'EV/EBITDA 이력은 {SM[\'EV/EBITDA\'][\'days\'] / 252:.1f}년이다.')
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(연 {pct(HIST[\'growth_3y\'])})에서 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ''   # 옛 카드는 별도 줄(비영업 줄 뒤) — POST
DCF_NOTE2 = ('낙관 시나리오(${DCF[\'high\']:.0f})가 기본(${DCF[\'base\']:.0f})보다 낮다. 낙관은 3년 성장률(연 {pct(HIST[\'growth_3y\'])}), '
             '기본은 5년 성장률(연 {pct(HIST[\'growth_5y\'])})을 쓰는데 3년이 더 낮기 때문이다.')
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('', '2026년 7월 28일 장 마감 후 — Q4 FY26 실적', '2026-07-29',
     '매출 $3.66B(+15%)·EPS $1.04 · 1분기 매출 전망 $4.0B ± $0.2B', 'q4', 'KLA 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 7일 장 마감 후 — 10:1 주식 분할 발표', '2026-05-08',
     '주식을 10:1로 나눈다(6월 11일 장 마감 뒤 효력)', 'split', 'KLA 공시 (SEC 8-K)'),
    ('', '2026년 4월 29일 장 마감 후 — Q3 FY26 실적', '2026-04-30',
     '매출 $3.42B(+11%)·EPS $0.91(분할 반영, 발표 당시 $9.12)', 'q3', 'KLA 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 12일 개장 전 공시 — 배당 21% 인상·자사주 $7B 추가(3월 11일 이사회)', '2026-03-12',
     '분기 배당 $1.90 → $2.30(분할 후 $0.23), 자사주 매입 한도 $7B 추가 · 투자자의 날', 'div', 'KLA 공시 (SEC 8-K)'),
    ('', '2026년 1월 29일 장 마감 후 — Q2 FY26 실적', '2026-01-30',
     '매출 $3.30B(+7%)·EPS $0.87(분할 반영, 발표 당시 $8.68)', 'q2', 'KLA 실적 보도자료 (SEC 8-K)'),
    ('', '2025년 10월 29일 장 마감 후 — Q1 FY26 실적', '2025-10-30',
     '매출 $3.21B(+13%)·EPS $0.85(분할 반영, 발표 당시 $8.47)', 'q1', 'KLA 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('AI 반도체 투자로 공정 제어 장비 수요가 늘어 FY2026 매출 $13.6B(+12%), 주가는 1년 새 {ch:+.0f}%', '우량 장비주·5년 상위 배수',
           ['4분기 매출 $3.66B(+15%), 순이익 $1.36B, 영업이익률 42%였다.',
            '회사는 2026년 하반기부터 2027년까지 수요가 가속된다고 보고 1분기 매출을 $4.0B로 전망했다.',
            '3월 배당을 21% 올리고 자사주 한도 $7B를 더했으며, 6월 주식을 10:1로 나눴다.'],
           '실적은 꾸준하지만 다섯 배수 모두 이력 상위 {max(100 - SM[k][\'percentile\'] for k in (\'PER\', \'PSR\', \'PBR\', \'PCR\', \'EV/EBITDA\')):.0f}% 안이고, 현금흐름 모델로는 현재가의 {DCF[\'base\'] / px * 100:.0f}%만 설명된다.',
           'Q1 FY27 실적(10월 하순 예상)의 매출 $4.0B 전망 달성과 수요 가속 여부.')
BULL = [('수익성', '4분기 영업이익률 42%, 순이익률 37%(FY2026 연간 42%·36%).'),
        ('전망', '1분기 매출 $4.0B 전망(4분기보다 +9%).'),
        ('환원', 'FY2026 주주환원 $3.35B, 자사주 한도 $9.74B.')]
BEAR = [('밸류', 'PER {SM[\'PER\'][\'current\']:.0f}배 — 5년 중앙값 {SM[\'PER\'][\'median\']:.0f}배, 현금흐름 기본 ${DCF[\'base\']:.0f}.'),
        ('중국', 'FY2026 매출의 29.8%가 중국 — 미국 수출 규제 영향.'),
        ('주기', '반도체 설비투자 경기에 따라 장비 수요가 흔들린다.')]
ANALYST = {'rating': 'Buy', 'n': 29, 'nt': 21, 'mean': 236.95, 'median': 245, 'low': 180, 'high': 325, 'sb': 14, 'b': 5, 'h': 10, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-05'

# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
POST = [r'''
# 분기 차트 아래 설명(회계연도·영업이익 계산·Q2 FY25 손상)
one('<canvas id="klacRevChart"></canvas>\n    </div>\n', '<canvas id="klacRevChart"></canvas>\n    </div>\n'
    '    <div class="yoy-footnote" style="margin-top:8px;">회계연도는 6월 30일에 끝난다(Q4 FY26 = 2026년 4~6월). 손익계산서에 영업이익 줄이 없어 영업이익은 세전이익 + 이자비용 − 기타수익으로 계산했다(매출 − 비용과 같다). Q2 FY25 영업이익률이 낮은 것은 영업권·무형자산 손상 $239M 때문이다.</div>\n')
# YoY·QoQ 각주: 영업이익 계산법(옛 카드)
assert h.count("· GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · ") == 2
h = h.replace("· GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · ", "· GAAP 기준(영업이익은 세전 + 이자 − 기타수익) · FCF는 영업현금흐름 − 설비투자 · ")
# 내재가치 표 아래 낙관 < 기본 설명(옛 카드: 비영업 줄 다음 별도 줄)
one('<div class="note" data-dcf-nonop hidden></div>', '<div class="note" data-dcf-nonop hidden></div>\n    <div class="note">' + F(C.DCF_NOTE2) + '</div>')
''']
