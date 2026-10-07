# ANET(아리스타 네트웍스) v2 카드 설정 — fill.py ANET. 회계연도 12월 31일.
# 틀 시절 카드(2026-09 루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G2).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05), 실적 보도자료(Q3 2025~Q2 2026), StockAnalysis(2026-10-01).
# 재현 모드: python3 v2/newcards/build.py ANET --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-30).
CIK = '0001596532'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 3035.7, 'op': 1378.0, 'ni': 1212.9}   # Q2 2026 10-Q 손익계산서(백만 달러, 제품 + 서비스 = 3,035.7)
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Arista'
S_ = 'https://www.sec.gov/Archives/edgar/data/1596532/'
SEC = S_
PR = {'q2': S_ + '000159653226000174/ex991q226-earningsrelease.htm', 'q1': S_ + '000159653226000074/ex991q126-earningsrelease.htm',
      'q4': S_ + '000159653226000010/ex991q425-earningsrelease.htm', 'q3': S_ + '000159653225000284/ex991q325-earningsrelease.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000159653226000175/anet-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {}
FAIRBAND_TITLE = 'id="anetFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 연 +{HIST[\'growth_3y\'] * 100:.1f}%)</span>'
OPM_RANGE, Y2 = (30, 55), (35, 50)
FCF_SUB = '영업현금흐름 − 설비투자 · 상반기 합계 $2.69B'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('R&amp;D (Q2 2026)', '$0.35B', '연구개발 · 매출의 11.5%')
NEXT = ('11월 초 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('11월 초', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('차입금이 없고 현금 $2.29B와 단기 투자증권 $11.05B를 갖고 있다. 이자비용이 없어 이자보상배율은 계산하지 않는다(점수에서 빠짐). '
               '부채 $8.9B의 대부분은 이연매출 $6.9B(유동 $5.1B·비유동 $1.8B)다.')
ACT_REASON = ''
YOY_EXTRA = ''
QOQ_EXTRA = '2분기 영업현금흐름은 법인세 납부와 매출채권 증가로 1분기($1.69B)보다 줄었다 · '
SEG = [('제품', 2605.2, '#0f6eb4'), ('서비스', 430.5, '#94a3b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품·서비스'
SEG_NOTE = ('회사는 단일 사업부라 부문 매출을 내지 않는다 · 1년 전보다 제품 +38.8% · 앞으로 인식할 잔여 이행의무 $8.4B(약 91%가 2년 안, '
            '<a href="{TENQ}" target="_blank" rel="noopener">10-Q</a>) · 출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Q2 2026 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (상반기 없음, 1년 전 상반기 $0.98B)', '$0'),
           ('잔여 바이백 승인 한도 (2026.06.30 기준)', '$0.82B'),
           ('배당', '지급하지 않음', '$0')]
CHECK_WHEN = '2026년 11월 초 (예상) · Q3 2026'
CHECK = ['3분기 전망 — 매출 약 $3.3B, 비GAAP 영업이익률 48~49%, 비GAAP EPS $1.06~1.08',
         '대형 고객 주문 시점 — 두 최종 고객이 2025년 매출의 26%·16%였고, 회사는 고객 집중과 매출 시점 변동이 이어질 것이라고 밝혔다',
         '이연매출($6.9B)·잔여 이행의무($8.4B)와 구매 약정 $9.7B의 흐름',
         '메모리·반도체 공급 제약과 매출총이익률']
NONOP_WHAT = '지분·장기투자'
PH = ['CSCO', 'AVGO', 'NVDA', 'DELL', 'APH', 'IBM']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {'per': ' (점수는 IT 카드 유니버스 기준)'}
CHART_TITLES = {'per': '네트워크·AI 반도체·하드웨어 6곳 PER 비교', 'pbr': '네트워크·AI 하드웨어 PBR 비교', 'psr': '네트워크·AI 하드웨어 PSR 비교',
                'pcr': '네트워크·AI 하드웨어 PCR(FCF) 비교', 'evebitda': '네트워크·AI 하드웨어 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-08-05 공시)'
PREMISE = ('주가가 1년 새 {ch:+.0f}% 올라 PER {SM[\'PER\'][\'current\']:.1f}배·PSR {SM[\'PSR\'][\'current\']:.1f}배·PBR·EV/EBITDA가 모두 5년 중 상위 {100 - min(SM[k_][\'percentile\'] for k_ in (\'PER\', \'PSR\', \'PBR\', \'EV/EBITDA\')):.0f}% 안이라 자기 이력 {selfsc:.1f}점이다. '
           '카드 유니버스 IT 안에서도 PSR·EV/EBITDA가 비싼 쪽이라 {peersc:.1f}점이다. <strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {sgn(VOTES[0])}·{sgn(VOTES[1])}·{sgn(VOTES[2])}{jo_ro(VOTES[2])} 합계 {TOTAL_TXT} “{VERDICT}”다. 현재가가 정당하려면 매출이 5년 내내 연 {pct(DCF[\'requiredGrowth\'])}씩 늘어야 한다'
        '(지난 5년 {pct(HIST[\'growth_5y\'])}, 3년 {pct(HIST[\'growth_3y\'])}). 낙관 시나리오(${DCF[\'high\']:.0f})가 기본(${DCF[\'base\']:.0f})보다 낮은 것은 3년 성장률이 5년보다 낮아서다. '
        '최근 1년 매출/자본을 못 구해 시나리오 일부는 과거 평균을 썼다.')
FUND_TIP = '이자비용이 없어 이자보상배율은 점수에서 빠진다. 부채비율 {FR[\'debtToEquity\'][\'points\']}점은 이연매출이 부채로 잡혀서다.'
SELF_TIP = 'PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PSR·PBR·EV/EBITDA가 5년 최고치에 가깝다. PCR만 중간 쪽이다.'
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(연 {pct(HIST[\'growth_3y\'])})에서 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ''   # 옛 카드는 별도 줄(비영업 줄 뒤) — POST
DCF_NOTE2 = ('낙관 시나리오(${DCF[\'high\']:.0f})가 기본(${DCF[\'base\']:.0f})보다 낮다. 낙관은 3년 성장률(연 {pct(HIST[\'growth_3y\'])}), '
             '기본은 5년 성장률(연 {pct(HIST[\'growth_5y\'])})을 쓰는데 3년이 더 낮기 때문이다.')
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('', '2026년 8월 4일 장 마감 후 — Q2 2026 실적', '2026-08-05',
     '매출 $3.04B(+37.7%)·EPS $0.95 · 첫 $3B 분기 · 3분기 매출 전망 약 $3.3B', 'q2', 'Arista 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 5월 5일 장 마감 후 — Q1 2026 실적', '2026-05-06',
     '매출 $2.71B(+35.1%)·EPS $0.80 · 2분기 매출 전망 약 $2.8B', 'q1', 'Arista 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 2월 12일 장 마감 후 — Q4 2025 실적', '2026-02-13',
     '매출 $2.49B(+28.9%)·EPS $0.75 · 2025년 매출 $9.01B(+28.6%)', 'q4', 'Arista 실적 보도자료 (SEC 8-K)'),
    ('', '2025년 11월 4일 장 마감 후 — Q3 2025 실적', '2025-11-05',
     '매출 $2.31B(+27.5%)·EPS $0.67 · 4분기 매출 전망 $2.3~2.4B', 'q3', 'Arista 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('AI 데이터센터 네트워크 수요로 2분기 매출이 38% 늘고 영업이익률 45%, 주가는 1년 새 {ch:+.0f}%', '고성장·5년 최고 배수',
           ['2분기 매출 $3.04B(+37.7%)로 처음 $3B를 넘었고, GAAP 영업이익률 45.4%·EPS $0.95(+36%)였다.',
            '3분기 매출 전망은 약 $3.3B, 비GAAP 영업이익률 48~49%다.',
            '차입금 없이 현금·투자증권 $13.3B를 갖고 있고, 올해 상반기엔 자사주를 사지 않았다.'],
           '실적은 좋지만 PER·PSR·EV/EBITDA가 5년 중 가장 높은 구간이고, 현금흐름 모델로는 현재가의 {DCF[\'base\'] / px * 100:.0f}%만 설명된다.',
           'Q3 2026 실적(11월 초 예상)의 매출 $3.3B 전망 달성과 대형 고객 투자 흐름.')
BULL = [('성장', '2분기 매출 +37.7%, 4분기 연속 전년 대비 +27% 이상.'),
        ('수익성', 'GAAP 영업이익률 45.4%, 순이익률 40%.'),
        ('재무', '차입금 0, 현금·투자증권 $13.3B.')]
BEAR = [('밸류', 'PER {SM[\'PER\'][\'current\']:.0f}배 — 5년 중 상위 {100 - SM[\'PER\'][\'percentile\']:.0f}%, 현금흐름 기본 ${DCF[\'base\']:.0f}.'),
        ('집중', '2025년 매출의 26%·16%가 두 최종 고객 — 주문 시점에 따라 분기 매출이 흔들린다(10-Q).'),
        ('환원', '상반기 자사주 매입 없음, 배당 없음, 남은 한도 $0.82B.')]
ANALYST = {'rating': 'Strong Buy', 'n': 31, 'nt': 19, 'mean': 239.53, 'median': 250, 'low': 164, 'high': 289, 'sb': 23, 'b': 7, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-06'

# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
PRE = ["FR = {r_['metric']: r_ for ax_ in FUND['axes'].values() for r_ in ax_['rows']}"]   # 기본적 분석 지표 행(값·점수)
POST = [r'''
# QoQ 각주에만 영업현금흐름 설명(옛 카드)
one(f"vs {C.QO.replace('-', '.')}({C.QQL}) · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · <a", f"vs {C.QO.replace('-', '.')}({C.QQL}) · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · " + C.QOQ_EXTRA + "<a")
# 내재가치 표 아래 낙관 < 기본 설명(옛 카드: 비영업 줄 다음 별도 줄)
one('<div class="note" data-dcf-nonop hidden></div>', '<div class="note" data-dcf-nonop hidden></div>\n    <div class="note">' + F(C.DCF_NOTE2) + '</div>')
''']
