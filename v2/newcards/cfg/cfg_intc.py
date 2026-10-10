# INTC(인텔) v2 카드 설정 — fill.py INTC. 회계연도 12월 마지막 토요일(Q2 2026 = 2026-06-27). 루트 카드 있음.
# 틀 시절 카드(2026-09 루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일).
# 최근 4분기 GAAP 적자 — 적정주가 밴드 없음(PER 해당 없음), 현금흐름 기본값 음수(카드 JS의 음수 처리는 fill.py 공통 패치).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-24), 실적 보도자료(Q3 2025~Q2 2026), 8-K(NVIDIA 지분 12/26, Fab 34 4/8, 회사채 4/30, 공모 8/10), StockAnalysis(2026-09-29).
# 엔진: 차입금 DEBT_TOTAL_TAG(10-Q는 1년 안 만기를 DebtCurrent로만 낸다) — build_multiple_history. 동종업은 카드 유니버스 IT(PEER_FILE 없음).
# 재현 모드: python3 v2/newcards/build.py INTC --from-card (마지막 종가 2026-09-28).
BUILD = {'share_events': True}   # 8월 공모를 주식 + 순수입금으로(v2.1 D-1, v2/share_events.json)
CIK = '0000050863'
CUR, YO, QO = '2026-06-27', '2025-06-28', '2026-03-28'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 16128, 'op': 1796, 'ni': -11033}   # Q2 2026 보도자료(백만 달러, 순이익은 인텔 귀속)
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Intel'
S_ = 'https://www.sec.gov/Archives/edgar/data/50863/'
SEC = S_
PR = {'q2': S_ + '000005086326000155/q226earningsrelease.htm', 'q1': S_ + '000005086326000077/q126earningsrelease.htm',
      'q4': S_ + '000005086326000009/q425earningsrelease.htm', 'q3': S_ + '000005086325000169/q325earningsrelease.htm'}
PR_CUR = 'q2'
TENQ = PR['q2']; TENQ_NAME = 'Q2 2026 실적 보도자료'   # 옛 카드는 재무 메모에 10-Q 대신 보도자료를 걸었다
LINKS = {'offering': S_ + '000119312526346806/d117670dex992.htm', 'notes': S_ + '000119312526197845/d143782d8k.htm',
         'fab34': S_ + '000005086326000072/intc-20260408.htm', 'nvda': S_ + '000005086325000204/intc-20251226.htm'}
FAIRBAND_TITLE = 'id="intcFairBand" title="최근 4분기 GAAP 순이익이 적자라 PER 기준 적정주가 밴드를 만들 수 없다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {mp(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (-80, 30), (-80, 30)
FCF_SUB = '영업현금흐름 − 유형자산 취득'
CAPEX_SUB = '투자활동 유형자산 취득(회사 기준 총액 $2.65B)'
STAT3 = ('R&amp;D (Q2 2026)', '$3.4B', '매출의 20.9%')
NEXT = ('10월 말 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('10월 말', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-27', '2024-12-28'), '2025년'
HEALTH_NOTE = ('현금·단기투자 $29.7B, 차입금 ${b[\'debt\'] / 1e9:.1f}B(단기 $2.0B 포함, 4월 회사채 $6.5B 발행). '
               '4월 아일랜드 Fab 34 합작 지분 49%를 Apollo에서 $14.2B에 되사며 파트너 분배금 $14.3B가 나가 자본이 줄었다(인텔 귀속 자본 $114.3B → $87.5B, 상반기 순손실 포함 — 8월 공모 순수입금 약 $22.6B를 더하면 약 $110.2B로, PBR은 이 값을 쓴다). '
               '8월 보통주 공모(2억 4,210만 주 × $95, 순수입금 약 $22.6B)는 3분기 재무상태표 전이라 주식 수·현금·자본에 공모일(8/12) 기준으로 함께 넣었다(v2.1 D-1).')
ACT_REASON = ''
YOY_EXTRA = ''   # 두 각주 모두 같은 꼬리 — POST에서 넣는다
SEG = [('클라이언트·피지컬 AI (CCPG)', 8877, '#0071c5'), ('데이터센터·AI (DCAI)', 6262, '#00c7fd'),
       ('파운드리 외부·기타(Mobileye 등, 내부 거래 제거 후)', 989, '#8a8fa8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
SEG_NOTE = ('전년 대비 CCPG +13%, DCAI +59%, 파운드리(내부 포함) +31% · 부문 영업이익 CCPG $2.34B, DCAI $2.47B, 파운드리 −$2.09B · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Intel Q2 2026 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (Q2 2026)', '없음'),
           ('자본 조달 (4월 회사채 $6.5B · 8월 보통주 $23.0B)', '$29.5B'),
           ('배당 (Q2 2026)', '2025년부터 지급 없음', '$0')]
CHECK_WHEN = '2026년 10월 말 (예상) · Q3 2026'
CHECK = ['3분기 가이던스 매출 $15.8~16.8B·GAAP 매출총이익률 41.0%·GAAP EPS $0.31 달성',
         '에스크로 주식 평가손익이 다시 GAAP 이익을 흔드는지(2분기 −$12.5B)',
         '파운드리 영업손실(2분기 −$2.09B)이 줄어드는지와 18A 양산 확대',
         '8월 증자 $23.0B 뒤 설비투자 증액 규모와 주식 수(2억 4,210만 주 추가)']
NONOP_WHAT = '지분·장기투자'
PH = ['AMD', 'NVDA', 'TSM', 'QCOM', 'TXN', 'MU']
PEER_FILE = None   # 카드 유니버스 IT(GICS Information Technology)
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '반도체 대형주 PER 비교', 'pbr': '반도체 대형주 PBR 비교', 'psr': '반도체 대형주 PSR 비교',
                'pcr': '반도체 대형주 PCR(FCF) 비교', 'evebitda': '반도체 대형주 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'GICS Information Technology 대비 배수 순위'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-24 공시)'
PRE = [r'''
mp = lambda v: pct(v).replace('-', '−')   # 음수 퍼센트는 유니코드 마이너스(옛 카드 표기)
BASE_TXT = f"{DCF['base']:.1f}".replace('-', '−')
TOP3 = math.ceil(round(100 - min(SM[k_]['percentile'] for k_ in ('PSR', 'PBR', 'PCR')), 1))   # PSR·PBR·PCR 중 가장 낮은 백분위의 '상위 N% 안'(올림)
''']
PREMISE = ('최근 4분기 GAAP가 적자라 PER은 점수에서 빼고(PER 해당 없음, 순이익률 2% 미만 규칙), PSR·PBR·PCR이 자기 5년 이력의 상위 {TOP3}% 안이라 {selfsc:.1f}점이다. '
           'IT 28종목 안에서는 PBR·PSR이 싼 쪽이지만 PCR·EV/EBITDA가 비싼 쪽이라 {peersc:.1f}점이다. '
           '<strong>현금흐름 내재가치는 기본 {BASE_TXT}달러로 음수</strong>다 — 최근 4분기 영업이익률이 {mp(HIST[\'margin_now\'])}라 지금 수익성으로는 투자가 가치를 만들지 못한다.')
RISK = ('이 모델로는 영업이익률을 100%로 잡아도 현재가에 닿지 않는다. 현재가는 매출의 {SM[\'PSR\'][\'current\']:.1f}배인데, '
        '할인율 10%·영구성장 2.5%·세율 21%에서는 영업이익률이 100%여도 사업 가치가 매출의 약 10배에 그치고 여기서 순부채·비지배지분(주당 약 ${(b[\'debt\'] + b[\'lease\'] - b[\'op_lease\'] + (b.get(\'nci\') or 0) - b[\'cash\'] - b[\'sti\'] - (b.get(\'lt_marketable\') or 0)) / b[\'shares\']:.0f}, 8월 공모 현금 반영)을 뺀다. '
        '일회성 비용을 뺀 2분기 비GAAP 영업이익률 17.2%를 5년 유지해도 주당 약 $14다(공모 뒤 주식 수·현금 기준, 사업 가치는 그대로). 현재가는 과거 실적이 아니라 파운드리·18A 전환과 AI 수요에 대한 기대를 반영한다.')
FUND_TIP = '순이익률이 크게 음수인 것은 2분기 에스크로 주식 평가손(−$12.5B) 때문이다. 매출 3년 증가율이 음수인 것은 2022년 대비이고 2025년 9월 Altera 매각으로 매출이 빠진 영향도 있다.'
SELF_TIP = ('최근 4분기 GAAP 순이익이 적자라 PER은 해당 없음(점수에서 뺌)이다. PSR·PBR·PCR은 5년 상위 {TOP3}% 안이다. 주식 수는 8월 공모 뒤 52.85억 주(증권신고서 기준 공모 전 50.43억 주 + 공모 2억 4,211만 주, 순수입금 약 $22.6B는 현금·자본에 함께 — v2.1 D-1)다. '
            '미국 정부 몫 에스크로 미방출 1억 4,300만 주(파생부채 $15.6B, 순부채에 넣지 않음)는 조건부라 넣지 않았다(넣으면 약 2.7% 늘어난다).')
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다. 적자 배수는 가장 비싼 쪽으로 센다(INTC의 PER은 해당 없음이라 비교에서 뺀다).')
STORIES = ['매출이 영구성장률 2.5%(지난 5년 실제 연 {mp(HIST[\'growth_5y\'])})로 크고, 영업이익률이 5년 중앙값 {mp(HIST[\'margin_5y\'])}로 간다.',
           '매출이 영구성장률 2.5%로 크고, 영업이익률이 최근 2년 중앙값 {mp(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(연 {mp(HIST[\'growth_3y\'])})이 영구성장률보다 낮아 2.5%로 두고, 영업이익률 {mp(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('', '2026년 8월 10일 장 전 — 보통주 $23.0B 공모', '2026-08-10',
     '$15B에서 $20B로 늘려 주당 $95에 2억 1,053만 주 · 초과배정 3,158만 주까지 전량 행사(총 2억 4,210만 주) · 8월 12일 완료 예정', 'offering', 'Intel 발표 (SEC 8-K)'),
    ('', '2026년 7월 23일 장 마감 후 · 7월 24일 반응 — Q2 2026 실적', '2026-07-24',
     '매출 $16.1B(+25%, 15년여 만의 최고 증가율) · GAAP EPS −$2.16(에스크로 주식 평가손), 비GAAP $0.42 · 3분기 매출 $15.8~16.8B 전망', 'q2', 'Intel 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 30일 — 회사채 $6.5B 발행', None,
     '2031~2066년 만기 5개 트랜치, 순수입 약 $6.47B · 4월 8일에는 Fab 34 재매입에 쓴 브리지론 $6.5B를 차환할 계획이라고 밝혔다', 'notes', 'Intel 공시 (SEC 8-K)'),
    ('', '2026년 4월 23일 장 마감 후 · 4월 24일 반응 — Q1 2026 실적', '2026-04-24',
     '매출 $13.6B(+7%) · GAAP EPS −$0.73(Mobileye 영업권 손상), 비GAAP $0.29 · 2분기 매출 $13.8~14.8B 전망', 'q1', 'Intel 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 4월 8일 장 마감 후 · 4월 9일 반응 — Fab 34 합작 지분 재매입', '2026-04-09',
     '아일랜드 Fab 34 합작의 Apollo 지분 49%를 $14.2B에 되사 100% 소유 · 현금과 브리지론 $6.5B로 조달', 'fab34', 'Intel 공시 (SEC 8-K)'),
    ('', '2026년 1월 22일 장 마감 후 · 1월 23일 반응 — Q4 2025 실적', '2026-01-23',
     '4분기 매출 $13.7B(−4%) · 2025년 매출 $52.9B(전년 수준) · 1분기 매출 $11.7~12.7B·GAAP EPS −$0.21 전망', 'q4', 'Intel 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 26일 — NVIDIA 지분 투자 완료', None,
     'NVIDIA에 보통주 2억 1,478만 주를 주당 $23.28, 총 $5.0B에 발행(9월 계약)', 'nvda', 'Intel 공시 (SEC 8-K)'),
    ('', '2025년 10월 23일 장 마감 후 · 10월 24일 반응 — Q3 2025 실적', '2025-10-24',
     '매출 $13.7B(+3%) · GAAP EPS $0.90, 비GAAP $0.23 · 미국 정부·NVIDIA·SoftBank 투자로 재무 보강', 'q3', 'Intel 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('AI 수요로 매출이 다시 늘고, 증자·지분 투자로 파운드리 투자 자금을 모은다', '회복 기대·적자 지속',
           ['2분기 매출이 ${rev[cur] / 1e9:.1f}B로 {(rev[cur] / rev[yo] - 1) * 100:.0f}% 늘었다. 데이터센터·AI가 59%, 클라이언트가 13% 늘었고, 비GAAP 영업이익률은 17.2%였다.',
            'NVIDIA $5.0B(12월), 회사채 $6.5B(4월), 보통주 $23.0B(8월)를 조달했고, 4월에 Fab 34 합작 지분을 $14.2B에 되샀다.',
            'GAAP로는 적자가 이어진다 — 1분기 Mobileye 영업권 손상, 2분기 에스크로 주식 평가손 −$12.5B.'],
           '파운드리 부문은 2분기에도 영업손실 −$2.09B였다. 8월 증자로 주식이 약 4.8% 늘었다.',
           'Q3 2026 실적(10월 말 예상)의 매출 $15.8~16.8B 가이던스, 파운드리 손실 축소, 에스크로 주식 평가손익.')
BULL = [('성장', '2분기 매출이 25% 늘어 회사가 15년여 만의 최고 증가율이라고 밝혔고, 3분기도 $15.8~16.8B를 전망했다.'),
        ('수익성', '2분기 매출총이익률이 40.4%로 1년 전(27.5%)보다 12.9%p 높아졌다.'),
        ('자금', '증자·회사채·NVIDIA 투자로 1년 사이 $34.5B를 조달했다.')]
BEAR = [('밸류', 'PSR·PBR·PCR이 자기 5년 이력의 상위 {TOP3}% 안이고, 현금흐름 내재가치는 음수다.'),
        ('적자', '최근 4분기 GAAP 순이익이 적자이고, 파운드리 부문은 분기 −$2.09B 손실이다.'),
        ('희석', 'NVIDIA 2.1억 주, 8월 공모 2.4억 주를 발행했고, 정부 에스크로 1.4억 주와 조건부 워런트 2.4억 주($20)가 남아 있다.')]
ANALYST = {'rating': 'Buy', 'n': 49, 'nt': 35, 'mean': 115.66, 'median': 114, 'low': 65, 'high': 200, 'sb': 14, 'b': 1, 'h': 32, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-10'

# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
POST = [r'''
# YoY·QoQ 각주: 순이익 귀속·에스크로 평가손, FCF 정의와 회사 조정 FCF(옛 카드는 두 각주 모두)
_fx = " · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · <a"
assert h.count(_fx) == 2, h.count(_fx)
h = h.replace(_fx, " · GAAP 기준 · 순이익은 인텔 귀속(2분기 에스크로 주식 평가손 −$12.5B 포함, 비GAAP EPS $0.42) · FCF는 영업현금흐름 − 투자활동 유형자산 취득(회사 조정 FCF −$8.4B는 Fab 34 지분 재매입 등 파트너 분배금 −$12.2B 반영) · <a")
# 총자산증가율 메모 꼬리(연간 지표라 올해 마감 전까지 같은 값)
sub(r"\(전년 \$[0-9.]+B\) · 연간 지표</span>", lambda m_: m_.group(0).replace("연간 지표</span>", "연간 지표, 2026년 마감 전까지 동일</span>"))
# 재무 메모 링크 이름: 보도자료(SEC 8-K)
one(f'>{C.TENQ_NAME} (SEC) →</a></div>', f'>{C.TENQ_NAME} (SEC 8-K) →</a></div>')
# 분기 차트 아래 설명(에스크로 평가손·Mobileye 손상·Altera 매각)
one('<canvas id="intcRevChart"></canvas>\n    </div>\n', '<canvas id="intcRevChart"></canvas>\n    </div>\n'
    '    <div class="yoy-footnote" style="margin-top:8px;">순이익은 인텔 귀속 GAAP. 2분기 순손실 −$11.0B는 영업이 아니라 미국 정부 거래의 에스크로 주식 파생부채 평가손 −$12.5B(영업외 “이자·기타” 합계 −$12.6B에 포함, 주가 상승 때문)이다. 1분기 영업손실은 Mobileye 영업권 손상 등 구조조정·기타 비용 $4.1B 때문이다. 2025년 9월 Altera 지분 51% 매각으로 그 뒤 매출에서 Altera가 빠졌다.</div>\n')
# INTC: 5년 성장이 음수라 모델은 영구성장률(2.5%)을 하한으로 쓰고, 요구 마진 해가 없다(nosol) — 옛 카드의 카드 한정 문장(헤더 툴팁·역산 문장)
one("? `현재가 $${price.toFixed(2)} 가 정당화되려면 매출이 지난 5년 속도(연 ${f1(d.growth5y)})로 크다가 식는 동안`\n"
    "          + (d.requiredMargin != null ? ` 영업이익률이 ${f1(d.requiredMargin)}여야 한다(현재 ${f1(d.marginNow)}).` : ` 영업이익률을 100%로 올려도 모자란다(현재 ${f1(d.marginNow)}).`)",
    "? `현재가 $${price.toFixed(2)} 가 정당화되려면 매출이 연 2.5%(지난 5년 실제 연 ${f1(d.growth5y)}, 영구성장률 하한)로 크는 동안`\n"
    "          + (d.requiredMargin != null ? ` 영업이익률이 ${f1(d.requiredMargin)}여야 한다(현재 ${f1(d.marginNow)}).` : ` 영업이익률을 100%로 잡아도 닿지 않는다(현재 ${f1(d.marginNow)}, 탐색 범위 −50~100%).`)")
one("이 정당하려면, 매출이 지난 5년 속도(연 ${pc(D.growth5y)})로 크다가 식는 동안`\n"
    "      + (D.requiredMargin != null ? ` 영업이익률이 <b>${pc(D.requiredMargin)}</b>여야 한다(지금 ${pc(D.marginNow)}).` : ` 영업이익률을 <b>100%</b>로 올려도 모자란다(지금 ${pc(D.marginNow)}).`)",
    "이 정당하려면, 매출이 연 2.5%(지난 5년 실제 연 ${pc(D.growth5y)}, 영구성장률을 하한으로 둔다)로 크는 동안`\n"
    "      + (D.requiredMargin != null ? ` 영업이익률이 <b>${pc(D.requiredMargin)}</b>여야 한다(지금 ${pc(D.marginNow)}).` : ` 영업이익률을 <b>100%로 잡아도</b> 닿지 않는다(지금 ${pc(D.marginNow)}).`)")
# 동종업 툴팁: PER이 빠진 이유(해당 없음, 순이익률 2% 미만)
one('뒤집어 점수로 썼고 PER를 뺀 4개를 평균했다.', '뒤집어 점수로 썼고, PER은 해당 없음(순이익률 2% 미만)이라 빼고 나머지 네 개를 평균했다.')
# 음수 표기 정리(카드 한정, 틀 과제 — 공통 후보) — 틀 JS가 음수 금액·비율을 "$-12", "-6.5%"로 찍는다. 텍스트 노드만 바꾸고 날짜는 건드리지 않는다.
_NEG = """<script>
// 음수 표기 정리(카드 한정, 틀 과제) — 틀 JS가 음수 금액·비율을 "$-12", "-6.5%"로 찍는다. 텍스트 노드만 바꾸고 날짜(2026-06-27)는 건드리지 않는다.
(function(){
  const RX1 = /\\$-(\\d)/g, RX2 = /(^|[\\s(~·])-(\\d)/g;
  const fix = root => {
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    let n;
    while ((n = w.nextNode())) {
      const p = n.parentElement && n.parentElement.tagName;
      if (p === 'SCRIPT' || p === 'STYLE') continue;
      const t = n.textContent;
      if (t.indexOf('-') < 0) continue;
      const u = t.replace(RX1, '−$$$1').replace(RX2, '$1−$2');
      if (u !== t) n.textContent = u;
    }
  };
  const run = () => fix(document.body);
  run();
  new MutationObserver(run).observe(document.body, {childList: true, subtree: true, characterData: true});
})();
</script>
"""
assert h.count('</body>') == 1
h = h.replace('</body>', _NEG + '</body>')
''']


# ── 자동 카드(설계 D, 2026-10-11) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose2·3 제안(손 표와 숫자 일치 — 여러 축·나머지 줄) ──
AUTO = True
SEG_MAP = {
 "parts": [
  {
   "concepts": [
    "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
   ],
   "axis": "srt:ConsolidationItemsAxis",
   "extra": {
    "us-gaap:StatementBusinessSegmentsAxis": "intc:DatacenterAndAIMember"
   },
   "members": {
    "us-gaap:OperatingSegmentsMember": [
     "데이터센터·AI (DCAI)",
     "#00c7fd"
    ]
   }
  },
  {
   "concepts": [
    "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
   ],
   "axis": "us-gaap:StatementBusinessSegmentsAxis",
   "extra": {
    "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
   },
   "members": {
    "intc:ClientComputingAndPhysicalAIGroupMember": [
     "클라이언트·피지컬 AI (CCPG)",
     "#0071c5"
    ]
   }
  }
 ],
 "remainder": [
  "파운드리 외부·기타(Mobileye 등, 내부 거래 제거 후)",
  "#8a8fa8",
  0.0613
 ]
}
# 손 문구 블록 정리: 화면 구조 고침만 남기고 분기 문장·날짜 박힌 치환·손 데이터 블록은 뺐다(자동 카드는 못 찾으면 건너뜀)
POST = ["# 동종업 툴팁: PER이 빠진 이유(해당 없음, 순이익률 2% 미만)\none('뒤집어 점수로 썼고 PER를 뺀 4개를 평균했다.', '뒤집어 점수로 썼고, PER은 해당 없음(순이익률 2% 미만)이라 빼고 나머지 네 개를 평균했다.')", '# 음수 표기 정리(카드 한정, 틀 과제 — 공통 후보) — 틀 JS가 음수 금액·비율을 "$-12", "-6.5%"로 찍는다. 텍스트 노드만 바꾸고 날짜는 건드리지 않는다.\n_NEG = """<script>\n// 음수 표기 정리(카드 한정, 틀 과제) — 틀 JS가 음수 금액·비율을 "$-12", "-6.5%"로 찍는다. 텍스트 노드만 바꾸고 날짜(2026-06-27)는 건드리지 않는다.\n(function(){\n  const RX1 = /\\\\$-(\\\\d)/g, RX2 = /(^|[\\\\s(~·])-(\\\\d)/g;\n  const fix = root => {\n    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);\n    let n;\n    while ((n = w.nextNode())) {\n      const p = n.parentElement && n.parentElement.tagName;\n      if (p === \'SCRIPT\' || p === \'STYLE\') continue;\n      const t = n.textContent;\n      if (t.indexOf(\'-\') < 0) continue;\n      const u = t.replace(RX1, \'−$$$1\').replace(RX2, \'$1−$2\');\n      if (u !== t) n.textContent = u;\n    }\n  };\n  const run = () => fix(document.body);\n  run();\n  new MutationObserver(run).observe(document.body, {childList: true, subtree: true, characterData: true});\n})();\n</script>\n"""\nassert h.count(\'</body>\') == 1\nh = h.replace(\'</body>\', _NEG + \'</body>\')']
