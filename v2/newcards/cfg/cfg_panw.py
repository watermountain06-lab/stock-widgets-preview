# PANW(팔로알토 네트웍스) v2 카드 설정 — fill.py PANW. 회계연도 7월 31일(Q4 FY26 = 2026-05~07). 시총 루트 카드 있음.
# 틀 시절 카드(루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G4).
# 출처: SEC XBRL, FY2026 10-K(2026-09-10), 실적 보도자료(Q1~Q4 FY2026), 8-K(Chronosphere 1/29, CyberArk 2/11, 자사주 3/10), StockAnalysis(2026-10-01).
# 본업 기준 종목(core_earnings.json, 2026-10-01) — 분기 차트·YoY/QoQ 순이익도 본업 기준으로 나온다(생성기 공통 규칙, 옛 카드는 GAAP 순이익이었다).
# 재현 모드: python3 v2/newcards/build.py PANW --from-card (일봉·이동평균·백테스트는 지금 카드에서).
BUILD = {}
CIK = '0001327567'
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
RELEASE = {'rev': 3410, 'op': 172, 'ni': -282}   # Q4 FY26 손익(백만 달러) — 보도자료 GAAP 순손실 $282M, 옛 카드 YoY 막대 $3.41B·$0.17B와 같다
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Palo Alto Networks'
S_ = 'https://www.sec.gov/Archives/edgar/data/1327567/'
SEC = S_
PR = {'q4': S_ + '000132756726000019/', 'q3': S_ + '000132756726000012/', 'q2': S_ + '000132756726000003/', 'q1': S_ + '000132756725000032/'}
PR_CUR = 'q4'
TENQ = S_ + '000132756726000023/panw-20260731.htm'; TENQ_NAME = 'FY2026 10-K'
LINKS = {'buyback': S_ + '000132756726000009/panw-20260310.htm', 'cyberark': S_ + '000119312526045600/d40626d8k.htm',
         'chrono': S_ + '000119312526029489/d884183d8k.htm'}
FAIRBAND_TITLE = ('id="panwFairBand" title="최근 1년 본업 PER 25~75% 구간({FB[\'per_p25\']:.0f}~{FB[\'per_p75\']:.0f}배) × 최근 4분기 본업 이익((영업이익 + 순이자) × (1 − 세율), A8 2026-10-04). '
                  '인수 뒤 GAAP 이익이 작아 PER 구간이 넓고 흔들린다. PER만으로 낸 범위라 판정과 따로 읽는다."')
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(DCF[\'marginNow\'])})</span>'
OPM_RANGE, Y2 = (-10, 25), (-10, 25)
FCF_SUB = '영업현금흐름 − 설비투자 · 회사 조정 FCF $1.3B'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('R&amp;D (Q4 FY26)', '$0.78B', '매출의 23%')
NEXT = ('11월 중순 예상', '일정 · Q1 FY27 (회사 미확정)'); NEXT_OP = ('11월 중순', 'Q1 FY27 예상')
FY_ENDS, FY_LABEL = ('2026-07-31', '2025-07-31'), 'FY2026'
HEALTH_NOTE = ('유동비율 {FR[\'currentRatio\']:.1f}%는 유동부채 $9.9B 중 이연매출(선수 구독료)이 $7.7B라서다. 차입금은 CyberArk에서 승계한 전환사채 $1.8B뿐이고 현금·단기투자 $3.1B, 장기투자 $4.8B가 있다. '
               '이자보상배율은 이자비용이 0으로 잡혀 만점 처리됐다(규칙). 활동성은 5년 비교 이력이 부족해 판정하지 않는다.')
ACT_REASON = ''
YOY_EXTRA = '1년 전엔 인수 전이라 매출 증가에 CyberArk·Chronosphere가 들어 있다 · '
QOQ_EXTRA = 'Q3 FY26은 인수 뒤 첫 분기라 영업손실이었다 · '
SEG = [('구독·지원', 2672, '#f97316'), ('제품(방화벽 장비 등)', 738, '#94a3b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 매출 종류별'
SEG_NOTE = ('1년 전보다 구독·지원 +36%, 제품 +29% · 차세대 보안 연간 반복 매출(NGS ARR) $9.10B(+63%), 남은 계약 잔고(RPO) $21.2B(+34%) · '
            '출처: <a href="{PR[\'q4\']}" target="_blank" rel="noopener">Q4 FY2026 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (FY2026, 2월 약 680만 주 · 평균 $147.69)', '$1.0B'),
           ('잔여 바이백 승인 한도 (2026.07.31 기준, 3월 $1.0B 추가 승인)', '$1.0B'),
           ('배당 · 인수 (FY2026)', '배당 없음 · 인수 현금 지출', '$4.7B')]
CHECK_WHEN = '2026년 11월 중순 (예상) · Q1 FY27'
CHECK = ['회사 전망 — Q1 FY27 매출 $3.300~3.310B, NGS ARR $9.54~9.56B, 비GAAP EPS $0.96~0.98',
         'FY2027 전망(매출 $14.10~14.20B, 비GAAP 영업이익률 29.5%, 조정 FCF 마진 38%)과 GAAP 이익의 간격',
         'CyberArk 통합 — 인수 뒤 두 분기 GAAP 순손실이 언제 흑자로 돌아오는지',
         '주식 수 증가(8월 31일 발행주식 8.18억 주, Q1 FY27 전망의 희석 주식 8.37~8.44억 주)와 자사주 매입 여력($1.0B)']
NONOP_WHAT = '장기투자'
PH = ['MSFT', 'ORCL', 'CRM', 'IBM', 'CRWD', 'PLTR']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소프트웨어·보안 PER 비교 (PANW는 본업 기준이라 순위에서 뺌)', 'pbr': '소프트웨어·보안 PBR 비교', 'psr': '소프트웨어·보안 PSR 비교',
                'pcr': '소프트웨어·보안 PCR(FCF) 비교', 'evebitda': '소프트웨어·보안 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 28종목 대비 배수 순위(PER은 본업 기준이라 제외)'
FUND_ASOF_NOTE = 'FY2026 10-K (2026-09-10 공시)'
PREMISE = ('주가가 1년 새 {ch:.0f}% 올라 PSR {SM[\'PSR\'][\'current\']:.1f}배·PCR {SM[\'PCR\'][\'current\']:.0f}배가 5년 중 가장 비싼 쪽이다. '
           'PBR만 싸 보이는데({SM[\'PBR\'][\'current\']:.1f}배), 인수 대가로 주식을 발행해 자본이 $7.8B → $27.5B로 커져서다. '
           '자기 이력 {selfsc:.1f}점, S&P500 카드 IT 종목 안에서 {peersc:.1f}점이다. <strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가의 {DCF[\'base\'] / px * 100:.1f}%</strong>다.')
RISK = ('이 숫자들은 규칙대로 GAAP 이익으로 계산했다(2026-10-01 결정). CyberArk 인수 뒤 무형자산 상각·인수 비용·주식보상으로 최근 4분기 GAAP 영업이익률이 {pct(HIST[\'margin_now\'])}뿐이라 '
        '본업 PER {SM[\'PER\'][\'current\']:.0f}배(순이자 $374M 포함), 내재가치 기본 ${DCF[\'base\']:.2f}가 나온다. 회사 비GAAP 영업이익률은 약 30%, 조정 FCF 마진은 38%다. '
        '어떤 영업이익률·성장률로도 현재가에 닿지 않는다는 계산이다.')
FUND_TIP = ('유동비율 {FPT[\'currentRatio\']}점은 이연매출(선수 구독료)이 커서이고, 순이익률(본업 기준 3.5%)·영업이익률({FR[\'opMargin\']:.1f}%)이 2점씩인 것은 인수 뒤 GAAP 이익이 작아서다. '
            '차입금은 전환사채 $1.8B뿐이다.')
SELF_TIP = ('PER은 규칙상 본업 기준이다(최근 4분기 세전이익이 영업이익보다 23% 작다). 적자였던 2022년 무렵이 빠져 PER 이력은 {SM[\'PER\'][\'days\'] / 252:.1f}년이다. '
            'PBR {SM[\'PBR\'][\'current\']:.1f}배가 싸게 나오는 것은 인수로 자본이 커져서다.')
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '반도체·하드웨어가 많고 소프트웨어는 일부다. PSR·EV/EBITDA는 IT 안에서도 가장 비싼 쪽이다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(연 {pct(HIST[\'growth_3y\'])})에서 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다. 낮은 마진으로 빨리 클수록 재투자가 이익을 넘어 값이 음수가 된다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.11 ~ 2026.09'
NEWS = [
    ('', '2026년 9월 1일 장 마감 후 — Q4 FY2026 실적', '2026-09-02',
     '매출 $3.41B(+34%)·NGS ARR $9.10B(+63%) · GAAP 순손실 $282M(비GAAP EPS $1.02) · FY27 매출 $14.10~14.20B 전망', 'q4', 'Palo Alto Networks 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 6월 2일 장 마감 후 — Q3 FY2026 실적', '2026-06-03',
     '매출 $3.0B(+31%, 인수분 $388M 포함) · GAAP 영업손실 $183M · 비GAAP 영업이익 $814M', 'q3', 'Palo Alto Networks 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 11일 장 마감 후 — 자사주 $1.0B 추가 승인(이사회 3월 10일)', '2026-03-12',
     '2월 20~24일 약 680만 주를 $1.0B에 매입(평균 $147.69)한 뒤 한도 $1.0B 추가', 'buyback', 'Palo Alto Networks 공시 (SEC 8-K)'),
    ('', '2026년 2월 17일 장 마감 후 — Q2 FY2026 실적', '2026-02-18',
     '매출 $2.6B(+15%)·EPS $0.61(비GAAP $1.03) · 인수 마무리 직후 발표', 'q2', 'Palo Alto Networks 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 11일 — CyberArk 인수 완료', '2026-02-11',
     '인수 대가 $21.1B(10-K) · CyberArk 전환사채(2030년 만기)를 승계', 'cyberark', 'Palo Alto Networks 공시 (SEC 8-K)'),
    ('neutral', '2026년 1월 29일 장 마감 후 — Chronosphere 인수 완료', '2026-01-30',
     '관측성(observability) 플랫폼 인수 · 대가 약 $3.0B(10-K)', 'chrono', 'Palo Alto Networks 공시 (SEC 8-K)'),
    ('', '2025년 11월 19일 장 마감 후 — Q1 FY2026 실적', '2025-11-20',
     '매출 $2.5B(+16%)·EPS $0.47(비GAAP $0.93) · Chronosphere 인수 발표', 'q1', 'Palo Alto Networks 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('CyberArk·Chronosphere 인수로 매출이 30%대로 뛰었고 GAAP 이익은 적자로, 주가는 1년 새 {ch:.0f}% 올랐다', '인수 통합·고평가',
           ['Q4 FY26 매출 $3.41B(+34%), NGS ARR $9.10B(+63%)로 인수 효과가 반영됐다.',
            'GAAP으로는 두 분기 연속 순손실(Q3 −$177M, Q4 −$282M)이고, 회사 비GAAP 영업이익률은 30% 안팎이다.',
            'FY2027 매출 $14.10~14.20B(+23~24%), 조정 FCF 마진 38%를 전망했다. 주가는 종가 기준 2월 저점 $141.67에서 8월 $396까지 올랐다.'],
           '규칙대로 GAAP 이익으로 보면 인수로 자본이 커진 PBR을 뺀 배수가 모두 5년 중 비싼 쪽이고, 현금흐름 모델은 현재가를 설명하지 못한다(해 없음).',
           'Q1 FY27 실적(11월 중순 예상)의 매출 $3.30B·NGS ARR 전망 달성과 GAAP 흑자 전환 시점.')
BULL = [('성장', 'Q4 FY26 매출 +34%, NGS ARR +63%, RPO $21.2B.'),
        ('현금', 'FY2026 조정 FCF 마진 38.4%, 차입금은 전환사채 $1.8B뿐.'),
        ('전망', 'FY2027 매출 +23~24%, 비GAAP 영업이익률 29.5%.')]
BEAR = [('밸류', 'PSR {SM[\'PSR\'][\'current\']:.1f}배·PCR {SM[\'PCR\'][\'current\']:.0f}배가 5년 중 가장 비싼 쪽.'),
        ('이익', '인수 뒤 GAAP 순손실 두 분기, 영업권 $22.0B.'),
        ('희석', '인수 대가로 주식을 발행해 발행주식이 8월 31일 8.18억 주다(Q2 FY26 희석 평균 7.11억 주).')]
ANALYST = {'rating': 'Buy', 'n': 55, 'nt': 42, 'mean': 402.17, 'median': 415, 'low': 290, 'high': 475, 'sb': 32, 'b': 10, 'h': 11, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-06'
REV_FOOTNOTE = ('회계연도는 7월 31일에 끝난다(Q4 FY26 = 2026년 5~7월). 2026년 1월 Chronosphere, 2월 11일 CyberArk(인수 대가 $21.1B) 인수를 마쳐 Q3 FY26부터 매출이 뛰고, '
                '인수 비용·무형자산 상각·주식보상으로 GAAP 영업이익이 줄었다. 회사 비GAAP 영업이익은 Q4 FY26 $1.0B다.')

# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
PRE = [r'''
FR = {r_['metric']: r_['value'] for ax_ in FUND['axes'].values() for r_ in ax_.get('rows', [])}   # 기본적 분석 지표 값(E26)
FPT = {r_['metric']: r_['points'] for ax_ in FUND['axes'].values() for r_ in ax_.get('rows', [])}
''']
POST = [r'''
# 보도자료 링크 글자: 옛 카드는 회계연도 네 자리(Q4 FY2026)
h = h.replace(f"{C.CO} {QL} 실적 보도자료 (SEC 8-K) →", f"{C.CO} Q4 FY2026 실적 보도자료 (SEC 8-K) →")
# 분기 차트 아래 설명(회계연도·인수)
one(f'<canvas id="{t}RevChart"></canvas>\n    </div>\n', f'<canvas id="{t}RevChart"></canvas>\n    </div>\n'
    f'    <div class="yoy-footnote" style="margin-top:8px;">{C.REV_FOOTNOTE}</div>\n')
# QoQ 각주(옛 카드)
h = re.sub(r"(vs " + re.escape(C.QO.replace('-', '.')) + r"\(" + re.escape(C.QQL) + r"\) · GAAP 기준[^\n']*?FCF는 영업현금흐름 − 설비투자 · )(<a)", lambda m: m.group(1) + C.QOQ_EXTRA + m.group(2), h, count=1)
# 동종업 팁: PER을 뺀 이유(옛 카드 문장)
one("뒤집어 점수로 썼고 PER를 뺀 4개를 평균했다.", "뒤집어 점수로 썼고 네 개를 평균했다(PER은 PANW만 본업 기준이라 제외).")
# 총자산증가율 메모: 인수 영업권(옛 카드)
one("(전년 $23.6B) · 연간 지표</span>", "(전년 $23.6B) · CyberArk·Chronosphere 인수로 영업권 $4.6B → $22.0B</span>")
# 자본배분 제목: 연간 숫자라 FY2026(옛 카드)
one(f'<div class="card-title">자본배분 · 주주환원 ({QL} · ', '<div class="card-title">자본배분 · 주주환원 (FY2026 · ')
# 본업 각주의 음수 공시 순이익: "$-0.28B" 대신 "−$0.28B"(생성기 공통 후보)
if ni_gaap[cur] < 0:
    _o = f'(공시 순이익 {QL} ${r1(ni_gaap[cur])}B)'; assert h.count(_o) == 2, h.count(_o)
    h = h.replace(_o, f'(공시 순이익 {QL} −${-r1(ni_gaap[cur])}B)')
''']
