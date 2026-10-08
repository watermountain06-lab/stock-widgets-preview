# SKHY(SK하이닉스 ADR) v2 카드 설정 — fill.py SKHY. 회계연도 12월 31일. ADR 1주 = 보통주 0.1주, ADR 상장 2026-07-10.
# 재무는 K-IFRS 연결재무제표(KIND 원문) — 어댑터(v2/adapters/skhy_ifrs.py)가 원화 그대로 companyfacts 모양 캐시를 만든다.
# 자기 이력은 원주(KRX 000660) 가격 분포(build_multiple_history.LOCAL_HISTORY), 순이익은 본업 기준(core_earnings.json).
# 빌드: build.py의 EPS·재무 단계를 skhy_feed.py로 바꿔 끼우고 활동성에 --facts 캐시를 준 래퍼로 돌렸다(2026-10-05 G3, TSM과 같은 공통 후보).
# 카드 표시: 분기 차트·YoY/QoQ 금액·FCF는 분기 평균 환율(연준 H.10)로 달러 환산, 증감률은 원화 기준(옛 카드 규칙) — PRE·POST.
# 틀 시절 카드를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G3).
# 출처: KIND(잠정실적 1/28·4/23, 반기보고서 8/14, 투자 8/7, 자사주 8/19), SEC 6-K(Q2 잠정 7/29)·424B4(ADR 7/10), StockAnalysis(2026-09-27).
# 재현 모드: python3 build_ifrs.py <clone> SKHY --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-25).
BUILD = {'feed': True}   # IFRS·원화 — adapters/skhy_feed.py
CIK = '0002120882'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 79318746, 'op': 60542608, 'ni': 93820236}   # 2026 반기보고서 2분기(백만 원)
VOTES, VERDICT = (-1, 1, 1), '적정~저평가'
CO = 'SK hynix'
KIND = 'https://kind.krx.co.kr/common/disclsviewer.do?method=search&acptno='
S_ = 'https://www.sec.gov/Archives/edgar/data/2120882/'
SEC = S_
PR = {'q2': S_ + '000119312526321989/d115239d6k.htm', 'q1': KIND + '20260423000001', 'q4': KIND + '20260128000709', 'h1': KIND + '20260814002925'}
PR_CUR = 'q2'
TENQ = KIND + '20260814002925'; TENQ_NAME = '2026 반기보고서'
LINKS = {'buyback': KIND + '20260819000318', 'fab': KIND + '20260807000613', 'adr': S_ + '000119312526299963/d32785d424b4.htm'}
FAIRBAND_TITLE = 'id="skhyFairBand" title="원주 최근 1년 PER(본업 기준) 25~75% 구간 × 현재 본업 EPS. 원주 가격 분포라 ADR 프리미엄이 없다 — 원주 환산가는 $134."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +{HIST[\'growth_3y\'] * 100:.0f}%)</span>'
OPM_RANGE, Y2 = (30, 80), (30, 80)
FCF_SUB = '현금창출력'
CAPEX_SUB = '미래 재투자'
STAT3 = ('R&amp;D (Q2 2026)', '$2.3B', '기술 경쟁력 투자')
NEXT = ('10월 말 예상', '일정 · Q3 2026 잠정실적'); NEXT_OP = ('10월 말', 'Q3 2026 잠정실적 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('현금·단기금융상품·단기투자 ₩88.0조가 차입금 ₩18.6조보다 ₩69.4조 많다. 이자보상배율은 손익계산서에 이자비용 줄이 없어 현금흐름표의 분기 이자 지급액으로 계산했다'
               '(2분기 약 {FR[\'interestCoverage\']:.0f}배). 장기투자자산(Kioxia 투자 법인 지분 포함)은 여기서 빼고 셌다.')
ACT_REASON = ''
YOY_EXTRA = ''
SEG = [('미국', 50565618, '#e11d48'), ('중국', 19681698, '#f97316'), ('아시아(중국 제외)', 6913940, '#3498db'), ('유럽', 1675649, '#2ecc71'), ('국내', 481841, '#8a8fa8')]   # 백만 원
SEG_ADJ = 0   # PRE에서 원화 도넛과 달러 환산 매출의 차이로 — 매출 대조는 원화로 따로 한다
SEG_TITLE = '매출 구성 — 지역별'
SEG_NOTE = ('회사는 반도체 단일 부문이라 제품(D램·낸드)별 매출을 정기보고서에 따로 싣지 않는다. 지역은 고객 소재지 기준 · '
            '출처: <a href="{TENQ}" target="_blank" rel="noopener">SK하이닉스 2026 반기보고서 연결재무제표 주석 (KIND) →</a>')
CAPITAL = [('설비투자 (상반기, 유형자산 취득)', '₩18.3조'),
           ('자사주 매입·소각 결정 (8/20~11/19, 최대 2,407만 주)', '₩40.0조'),
           ('배당 지급 (상반기)', '', '₩1.6조')]
CHECK_WHEN = '2026년 10월 말 (예상) · Q3 2026 잠정실적'
CHECK = ['분기 매출(2분기 ₩79.3조)과 영업이익률(76.3%)이 더 오르는지, 꺾이는지',
         '₩40조 자사주 매입(11/19 종료)이 얼마나 진행됐는지 — 소각 뒤 주식 수가 최대 3.3% 줄어든다',
         'Kioxia 투자 법인 평가손익이 다시 영업외 이익을 크게 흔드는지 (상반기 평가이익 ₩59.3조)',
         'ADR과 원주의 가격 차이(9월 +40%대)가 좁혀지는지']
NONOP_WHAT = '지분·장기투자'
PH = ['MU', 'SNDK', 'NVDA', 'TSM', 'AVGO']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '메모리·반도체 PER 비교', 'pbr': '메모리·반도체 PBR 비교', 'psr': '메모리·반도체 PSR 비교',
                'pcr': '메모리·반도체 PCR(FCF) 비교', 'evebitda': '메모리·반도체 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터(카드 유니버스 28종목)보다 배수가 얼마나 낮은가. 높을수록 싸다. ADR 가격 기준.'
PEER_COMMENT = 'GICS Information Technology 대비 배수 순위 (ADR 가격 × 그날 환율 ÷ 원화 재무)'
FUND_ASOF_NOTE = '2026 반기보고서 (2026-08-14 공시)'
PREMISE = ('IT 28종목 안에서는 싼 쪽(동종업 {peersc:.1f}점)이지만, 원주의 5년 배수 분포에 ADR 가격을 대 보면 다섯 배수 모두 비싼 쪽(자기 이력 {selfsc:.1f}점)이다. '
           '<strong>ADR이 원주보다 약 43% 비싸서 그 차이가 그대로 얹힌다.</strong> 동종업 점수는 PER을 빼고(본업 기준이라) 네 배수로 셌고, PCR·EV/EBITDA는 정점 이익이 분모라 낮게 나온다. '
           '현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%로, 영업이익률이 최근 4분기 {HIST[\'margin_now\'] * 100:.0f}%에서 '
           '최근 2년 중앙값 {HIST[\'margin_2y\'] * 100:.0f}%로 내려온다고 본 값이다.')
RISK = ('메모리는 가격이 크게 오르내린다. 2023년 영업손실이 ₩7.7조였고, 지금 마진(2분기 76.3%)은 5년 중앙값(연 {HIST[\'margin_5y\'] * 100:.0f}%)의 두 배를 넘는다. '
        '현재가가 정당하려면 5년간 매출이 매년 <strong data-vs="req">{pct(DCF[\'requiredGrowth\'])}</strong>씩 커야 한다(최근 3년 실제 연 {HIST[\'growth_3y\'] * 100:.0f}%).')
FUND_TIP = ('K-IFRS 연결재무제표(KIND 원문)를 원화 그대로 계산했다(v2/adapters/skhy_ifrs.py). 순이익률은 본업 기준(영업이익 × (1 − 실효세율))이다. '
            '이자보상배율은 손익계산서에 이자비용 줄이 없어 현금흐름표의 분기 이자 지급액으로 계산했다. 감가상각은 비용의 성격별 분류 주석 값이라 재고에 남은 몫이 빠져 EBITDA가 약간 작다.')
SELF_TIP = ('5년 분포는 원주(KRX 000660) 가격으로, 현재 값은 ADR 가격으로 계산했다. ADR 상장이 2026년 7월이라 ADR만으로는 이력이 없다. '
            '그래서 현재 위치에 ADR 프리미엄(약 43%)이 그대로 들어간다. PER은 본업 이익 기준이다.')
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다(ADR 가격 기준, 원화 재무는 그날 환율로 환산).',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['5년 성장률의 절반(연 {HIST[\'growth_5y\'] / 2 * 100:.0f}%)에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 내려간다.',
           '5년 성장률(연 {HIST[\'growth_5y\'] * 100:.0f}%)에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 내려간다. 5년 뒤 매출 약 ₩479조.',
           '3년 성장률(연 {HIST[\'growth_3y\'] * 100:.0f}%)에서 출발하고 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다. 5년 뒤 매출 약 ₩1,006조.']
DCF_NOTE = ''
NEWS_RANGE = '2026.01 ~ 2026.09'
NEWS = [
    ('green', '2026년 8월 19일 15:41(한국) — ₩40조 자사주 매입·소각', '2026-08-19',
     '11월 19일까지 최대 2,407만 주를 사서 전량 소각 · 2025~2027년 누적 잉여현금흐름의 50% 이상 환원 방침', 'buyback', 'SK하이닉스 공시 (KIND)'),
    ('neutral', '2026년 8월 14일 — 반기보고서', '2026-08-14',
     '상반기 금융상품 평가이익 ₩63.2조 · Kioxia 투자 법인(BCPE Pangea Cayman2) 평가 ₩6.7조 → ₩66.1조 · 교환사채 파생손실 ₩4.0조', 'h1', 'SK하이닉스 반기보고서 (KIND)'),
    ('neutral', '2026년 8월 7일 — 용인·청주 신규 팹 ₩54.3조 투자', '2026-08-07',
     '용인 클러스터 2기 팹 ₩35.2조(~2031.10) · 청주 M17 ₩19.1조(~2031.04) · 분기 배당 주당 ₩375', 'fab', 'SK하이닉스 공시 (KIND)'),
    ('', '2026년 7월 29일 07:43(한국) — Q2 2026 잠정실적', '2026-07-29',
     '매출 ₩79.3조(+257%) · 영업이익 ₩60.5조(영업이익률 76.3%) · 순이익 ₩93.8조(금융상품평가이익 ₩53.2조·배당금수익 ₩10.0조 등 금융수익 ₩65.9조 포함)', 'q2', 'SK hynix 잠정실적 (SEC 6-K)'),
    ('neutral', '2026년 7월 10일 — 나스닥 ADR 상장', None,
     'ADR 1억 7,790만 주(보통주 1,779만 주 신주)를 $149에 공모 · 7/14 납입 ₩39.9조 · 원주 KRX 상장은 1996년', 'adr', 'SK hynix 투자설명서 (SEC 424B4)'),
    ('', '2026년 4월 23일 07:34(한국) — Q1 2026 잠정실적', None,
     '매출 ₩52.6조 · 영업이익 ₩37.6조(영업이익률 71.5%) · ADR 상장 전', 'q1', 'SK하이닉스 공시 (KIND)'),
    ('', '2026년 1월 28일 16:36(한국) — Q4 2025 잠정실적', None,
     '2025년 매출 ₩97.1조 · 영업이익 ₩47.2조 · 같은 날 자사주 1,530만 주 소각 결정 · ADR 상장 전', 'q4', 'SK하이닉스 공시 (KIND)'),
]
SUMMARY = ('AI 메모리 호황으로 이익이 폭증했고, 증설과 주주환원을 함께 키운다', '초호황·ADR 웃돈',
           ['분기 매출이 ₩24.4조(Q3 2025) → ₩32.8조 → ₩52.6조 → ₩79.3조로 세 분기 만에 3배가 됐고, 영업이익률은 46.6%에서 76.3%로 올랐다.',
            '2분기 공시 순이익 ₩93.8조에는 금융수익 ₩65.9조(금융상품평가이익 ₩53.2조·배당금수익 ₩10.0조)가 섞여 있다. 평가이익의 대부분은 Kioxia 투자 법인 몫이다(상반기 ₩59.3조). 그래서 이 카드의 PER은 본업 이익 기준이다.',
            '7월 ADR 상장으로 ₩39.9조를 조달했고, 8월에 ₩40조 자사주 매입·소각과 용인·청주 신규 팹 ₩54.3조 투자를 결정했다.'],
           'ADR이 원주보다 약 43% 비싸게 거래된다. 메모리 가격이 꺾이면 마진이 빠르게 줄어든다(2023년 영업손실 ₩7.7조).',
           'Q3 2026 잠정실적(10월 말 예상)의 매출·마진 추세, 자사주 매입 진행(11/19 종료), ADR과 원주의 가격 차이.')
BULL = [('수요', '2분기 매출 ₩79.3조(+257%), 영업이익률 76.3%로 네 분기 연속 올랐다.'),
        ('주주환원', '₩40조 자사주 매입·소각을 결정했고, 3년 누적 잉여현금흐름의 50% 이상을 돌려준다.'),
        ('재무', '현금·단기금융 ₩88.0조가 차입금 ₩18.6조의 네 배를 넘는다.')]
BEAR = [('ADR 웃돈', 'ADR이 원주보다 약 43% 비싸다. 같은 회사를 원주로는 그만큼 싸게 산다.'),
        ('사이클', '2023년 영업손실 ₩7.7조였다. 메모리 가격이 꺾이면 마진이 빠르게 줄어든다.'),
        ('설비투자', '8월에만 신규 팹 ₩54.3조 투자를 결정했고, 상반기 설비투자가 ₩18.3조였다.')]
ANALYST = {'rating': 'Buy', 'n': 15, 'nt': 10, 'mean': 254.7, 'median': 250, 'low': 200, 'high': 320, 'sb': 9, 'b': 5, 'h': 0, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-06'
PRE = [r'''
FR = {r_['metric']: r_['value'] for ax_ in FUND['axes'].values() for r_ in ax_.get('rows', [])}   # 기본적 분석 지표 값
# 원화 매출 대조(도넛)와 증감률(원화 기준)용 사본
assert abs(sum(v_ for _, v_, _ in C.SEG) - rev[cur] / 1e6) <= 1.5
_LOC = {'rev': dict(rev), 'op': dict(op), 'ni': dict(ni_chart), 'fcf': dict(fcf)}
# 분기 흐름을 분기 평균 환율(연준 H.10)로 달러 환산 — 원화 재무(어댑터)를 옛 카드처럼 달러로 보인다
import fx as _fx, datetime as _dt
_, _rr = bmh.pick_tag(CIK, bmh.FLOW_TAGS['revenue'])
_st = {e_['end']: e_.get('start') for e_ in bmh.quarterly_flow(_rr, T)}
_fds, _fvs = _fx._load(_fx.CURRENCY[T])
def _qavg(k):
    s_ = _st.get(k) or (_dt.date.fromisoformat(k) - _dt.timedelta(days=91)).isoformat()
    x_ = [v_ for d_, v_ in zip(_fds, _fvs) if s_ <= d_ <= k]
    return sum(x_) / len(x_)
_seen = set()
for _dd in (rev, op, ni, ni_chart, ni_gaap, ocf, cap, fcf):
    if id(_dd) in _seen:
        continue
    _seen.add(id(_dd))
    for _k in list(_dd):
        _dd[_k] = _dd[_k] / _qavg(_k)
C.SEG_ADJ = rev[cur] / 1e6 - sum(v_ for _, v_, _ in C.SEG)   # 원화 도넛 — 위에서 원화로 대조했다
''']
# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
POST = [r'''
# 분기 차트 제목·설명(본업 순이익, 달러 환산)
one('분기 매출 / 순이익(본업 기준) / 영업이익률 (Q3 2024~Q2 2026)', '분기 매출 / 본업 순이익 / 영업이익률 (Q3 2024~Q2 2026 · 달러 환산)')
one('<canvas id="skhyRevChart"></canvas>\n    </div>\n', '<canvas id="skhyRevChart"></canvas>\n    </div>\n'
    '    <div class="yoy-footnote" style="margin-top:8px;">K-IFRS 원화 실적을 분기 평균 환율(연준 H.10)로 달러 환산했다. 순이익은 본업 기준(영업이익 × (1 − 그 분기 실효세율))이다 — 2분기 공시 순이익 ₩93.8조에는 금융수익 ₩65.9조(금융상품평가이익 ₩53.2조·배당금수익 ₩10.0조)가 들어 있다.</div>\n')
# YoY·QoQ: 증감률은 원화 기준, 각주는 K-IFRS·달러 환산·반기보고서(옛 카드)
_fd = lambda a, b_: '%+.1f%%' % ((a / b_ - 1) * 100)
for _cmp, _ql in ((yo, C.YL), (qo, C.QQL)):
    _dl = [_fd(_LOC[k_][cur], _LOC[k_][_cmp]) for k_ in ('rev', 'op', 'ni', 'fcf')]
    sub(r"(cmpLabel: '" + re.escape(_ql) + r"',\n    titleSuffix: '[^']*',\n    chart: \{ cur: \[[^\]]*\], cmp: \[[^\]]*\] \},\n    deltas: )\[[^\]]*\]",
        lambda m: m.group(1) + '[' + ', '.join("'" + x_ + "'" for x_ in _dl) + ']')
_old = re.findall(r"footnote: '기준일: [^']*'", h)
assert len(_old) == 2, len(_old)
for _o, _a in zip(_old, (f'{C.YO.replace("-", ".")}({C.YL})', f'{C.QO.replace("-", ".")}({C.QQL})')):
    h = h.replace(_o, f"footnote: '기준일: {C.CUR.replace('-', '.')}({QL}) vs {_a} · K-IFRS 연결재무제표 · 금액은 분기 평균 환율로 달러 환산, 증감률은 원화 기준 · 순이익은 본업 기준(영업이익 × (1 − 실효세율)) · FCF는 영업현금흐름 − 유형자산 취득 · <a href=\"{C.TENQ}\" target=\"_blank\" rel=\"noopener\">SK하이닉스 2026 반기보고서 (KIND) →</a>'", 1)
# 총자산증가율 메모: 원화 그대로(옛 카드)
sub(r'(<span class="diag-label">총자산증가율</span><span class="diag-value">[^<]*</span><span class="diag-note">)[^<]*(</span>)',
    lambda m: m.group(1) + f'FY25 ₩{a1 / 1e6:.1f}조(전기 ₩{a0 / 1e6:.1f}조) · 원화 기준 연간 지표, FY26 마감 전까지 동일' + m.group(2))
# 매출 구성 범례: 원화 조 단위(옛 카드)
_tot = sum(v_ for _, v_, _ in C.SEG)
for n_, v_, c_ in C.SEG:
    sub(r'(</span>' + re.escape(n_) + r' <strong style="color:var\(--text\);">)[^<]*(</strong>)', lambda m: m.group(1) + f'₩{v_ / 1e6:.1f}조 · {v_ / _tot * 100:.1f}%' + m.group(2))
# 자본배분: 제목 기준일, 배당 줄 태그 없음, 네 번째 줄(ADR 신주)과 아래 환원 방침 각주(옛 카드)
one('<div class="card-title">자본배분 · 주주환원 (Q2 2026 · 2026.06.30 기준)</div>', '<div class="card-title">자본배분 · 주주환원 (2026년 · 2026.08.21 기준)</div>')
one('<span class="zone-tag" style="background:rgba(240,192,64,0.18);color:var(--gold);"></span>\n            ', '')
sub(r'(<span class="zone-val">₩1\.6조</span>\n          </div>\n        </div>\n)',
    lambda m: m.group(1) + '        <div class="zone-item">\n          <span class="zone-label">ADR 신주 발행 (7/14 납입, 1,779만 주)</span>\n          <span class="zone-val">₩39.9조</span>\n        </div>\n')
sub(r'(<span class="zone-val">₩39\.9조</span>\n        </div>\n      </div>\n)',
    lambda m: m.group(1) + '      <div class="yoy-footnote" style="margin-top:14px;">회사는 2025~2027년 누적 잉여현금흐름의 50% 이상을 자사주 매입·소각과 배당으로 돌려주겠다고 밝혔다(8/19 공정공시) · 2월에 기존 자사주 1,530만 주를 소각했다 · 출처: <a href="' + LINKS['buyback'] + '" target="_blank" rel="noopener">자기주식 취득 결정 (KIND) →</a></div>\n')
# 헤더 부제: ADR 첫 거래·비율·원주 대비 웃돈(옛 카드, 숫자는 원주 9/23 종가·환율 9/18 기준)
sub(r'NASDAQ ADR\([^<]*', 'NASDAQ ADR(2026.07.10 첫 거래 · 1 ADR = 보통주 0.1주) · 원주 KRX:000660 · ADR이 원주보다 +43% 비싸다(원주 09/23 종가·환율 09/18 기준)')
# 주가 차트 머리: 상장 뒤 일봉이 기간보다 짧으면 "상장 이후"(옛 카드, 공통 후보 — 짧은 이력 종목)
one("    const base = prevClose != null ? prevClose : data[0][4];\n", "    const base = prevClose != null ? prevClose : data[0][4];\n"
    "    const FULL = {'1M':21,'6M':126,'1Y':252,'3Y':756,'5Y':1260};\n"
    "    const LBL = (prevClose == null && data.length < FULL[rangeKey] * 0.9) ? '상장 이후' : RANGE_LABELS[rangeKey];\n")
one("일봉 캔들스틱 (${dateFrom} ~ ${dateTo}) · ${RANGE_LABELS[rangeKey]} 수익률 `;", "일봉 캔들스틱 (${dateFrom} ~ ${dateTo}) · ${LBL} 수익률 `;")
one("rangeSummary.textContent = `${RANGE_LABELS[rangeKey]} 최저 $${periodLow.toFixed(2)} (${lowDate}) → ${RANGE_LABELS[rangeKey]} 최고", "rangeSummary.textContent = `${LBL} 최저 $${periodLow.toFixed(2)} (${lowDate}) → ${LBL} 최고")
# 재무 건전성 출처 링크: 반기보고서는 KIND(fill.py는 "(SEC)"로 적는다)
one('>2026 반기보고서 (SEC) →</a>', '>2026 반기보고서 (KIND) →</a>')
# 기본적 분석 툴팁: 분기 자료는 반기보고서(10-Q 아님)
one("분기(Q2 2026, 10-Q), 성장률은", "분기(Q2 2026, 반기보고서), 성장률은")
# 역산 문장: 성장 모드 — 틀의 칸 있는 문장(MU·TSM과 같은 공통 후보)
assert DCF['reqMode'] == 'growth'
one('<div class="reverse">—</div>', F('<div class="reverse">지금 가격(<span data-dcf-price>${px:.2f}</span>)이 정당하려면 5년간 매출이 매년 <b data-dcf-req>{pct(DCF[\'requiredGrowth\'])}</b>씩 커야 한다. '
    '기본 시나리오(<span data-dcf-basev>${DCF[\'base\']:.0f}</span>)를 같은 방식으로 환산하면 연 <span data-dcf-baseeq>{pct(DCF[\'baseEquivGrowth\'])}</span>다.</div>'))
''']
