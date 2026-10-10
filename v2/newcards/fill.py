"""공통 v2 카드 채우기(비은행) — LIN 스크립트(lin_fill.py)를 일반화. 종목별 내용은 설정 모듈(cfg_{t}.py)에 둔다.
사용: python3 v2/newcards/fill.py VZ   (clone + 배열 + 데이터 블록 뒤 — 보통 build.py가 부른다)
설정 문자열 안의 {…}는 이 스크립트의 변수(SM·selfsc·peersc·DCF·HIST·px·FB·pct·b·eps_ttm·ch·FUND 등)로 f-string처럼 채운다."""
import importlib.util, json, math, os, re, sys
T = sys.argv[1]; t = T.lower()
HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('cfg', os.path.join(HERE, 'cfg', f'cfg_{t}.py')); C = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(C)
os.chdir(os.path.dirname(HERE))   # v2/
sys.path.insert(0, '.')
import build_multiple_history as bmh
import build_dcf as bd
AUTO = getattr(C, 'AUTO', False)   # 자동 카드(설계 D, 2026-10-10) — 분기마다 고치던 칸을 SEC 자료·규칙 문장으로(auto_card.py)
if AUTO:
    import auto_card as _ac
    _ac.apply(C, T)

CIK = C.CIK
p = f'{T}_full_widget.html'; h = open(p, encoding='utf-8').read()


def one(o, n):
    global h
    c = h.count(o); assert c == 1, (c, o[:100]); h = h.replace(o, n)


def one_done(o, n):
    """틀(NVDA)에 이미 같은 수정이 들어가 있으면 건너뛴다 — 2026-10-05 틀 시절 카드 47장(NVDA 포함)에 이 음수 표시 규칙을 넣었다(E25)."""
    if n in h:
        return
    one(o, n)


def sub(pat, new, flags=re.S):
    global h
    m = list(re.finditer(pat, h, flags)); assert len(m) == 1, (len(m), pat[:90])
    h = h[:m[0].start()] + (new(m[0]) if callable(new) else new) + h[m[0].end():]


_SPEC = re.compile(r"^[<>^=]?[+\- ]?,?(\.\d+)?[a-z%]?$")


def F(s):
    """설정 문자열의 {표현식} · {표현식:형식}을 이 스크립트 변수로 채운다(따옴표가 섞여도 되게 f-string 대신 직접 계산)."""
    def rep(m):
        body = m.group(1); expr, spec = body, ''
        if ':' in body:
            e_, s_ = body.rsplit(':', 1)
            if _SPEC.match(s_):
                expr, spec = e_, s_
        return format(eval(expr, globals()), spec)
    return re.sub(r'\{([^{}]+)\}', rep, s)


def q(tags):
    _, rows = bmh.pick_tag(CIK, tags)
    return {e['end']: e['val'] for e in bmh.quarterly_flow(rows, T)}


pct = lambda v: f'{v * 100:.1f}%'
rev = q(bmh.FLOW_TAGS['revenue']); op = q(['OperatingIncomeLoss']); ni = q(getattr(C, 'NI_TAGS', ['NetIncomeLoss']))
ocf = q(bmh.FLOW_TAGS['ocf']); cap = q(bmh.FLOW_TAGS['capex'])   # 엔진과 같은 태그 목록 — T는 2026년부터 계속사업 영업현금흐름 태그로만 냈다(2026-10-02)
if getattr(C, 'OP_DISPLAY', None):   # 영업이익 줄이 없는 종목의 카드 표시용 영업이익(엔진 배수에는 안 씀) — CB 보험사: 세전이익 + 이자비용(2026-10-02)
    _pt_tags, _adds = C.OP_DISPLAY
    _pt = q(_pt_tags)
    _add = [(q(_t), _sg) for _t, _sg in _adds]
    op = {k: _pt[k] + sum(_sg * _a.get(k, 0) for _a, _sg in _add) for k in _pt}
for _e, _o, _n in getattr(C, 'OVERRIDE_OP_NI', []):   # 회사가 수정값·보도자료 값을 낸 분기(백만 달러)
    op[_e], ni[_e] = _o * 1e6, _n * 1e6
fcf = {k: ocf[k] - cap[k] for k in ocf if k in cap}
# 본업 기준 종목(core_earnings.json)은 분기 차트·YoY/QoQ 순이익도 본업 순이익((영업이익 + 순이자) × (1 − 그 분기 실효세율, 범위 밖이면 21%))으로(2026-09-24 사용자 결정, GEV 방식)
CORE = T in json.load(open('core_earnings.json'))
ni_gaap = dict(ni)
if CORE:
    _tax = q(['IncomeTaxExpenseBenefit'])
    _pt = q(['IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest', 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments'])
    for _k in ni_gaap:
        if _k not in _pt and _k in _tax:
            _pt[_k] = ni_gaap[_k] + _tax[_k]   # 분기 세전 태그가 없는 회사(MRVL)
    # 세율 분모에 반복적 비공제 항목(tax_rate_addback.json)을 되돌려 더한다 — 본업 PER·현금흐름과 같은 세율 규칙(ABBV 조건부 대가, 2026-10-05).
    # 일회성 세금(tax_oneoff.json)은 분기 차트에서 빼지 않는다(GEV·WDC 카드가 "분기 차트는 그 분기 세율 그대로"라고 밝힌 기존 규칙, Codex)
    _ptr = {k: _pt[k] + bmh.rate_addback(T, CIK, k, quarter=True) for k in _pt}
    _txr = dict(_tax)
    _rate = lambda k: _txr[k] / _ptr[k] if _ptr.get(k) and _ptr[k] > 0 and k in _txr and 0 <= _txr[k] / _ptr[k] <= 0.40 else 0.21
    # A8(2026-10-04 사용자 결정): 본업 순이익 = (영업이익 + 순이자) × (1 − 세율). 순이자 결측 분기는 영업이익만.
    _nis = bmh.net_interest_series(CIK, T)
    ni_chart = {k: (op[k] + (bmh.net_interest_at(_nis, k, quarter=True) or 0.0)) * (1 - _rate(k)) for k in op}
else:
    ni_chart = ni
ks = sorted(k for k in rev if k <= C.CUR)[-8:]
cur, yo, qo = ks[-1], ks[-5], ks[-2]
assert (cur, yo, qo) == (C.CUR, C.YO, C.QO), ks
for _k, _v in C.RELEASE.items():   # 보도자료·10-Q 대조(백만 달러, 반올림)
    _s = {'rev': rev, 'op': op, 'ni': ni_gaap, 'ocf': ocf, 'cap': cap}[_k]
    assert abs(_s[cur] / 1e6 - _v) <= getattr(C, 'RELEASE_TOL', 1), (_k, _s[cur], _v)
from decimal import Decimal, ROUND_HALF_UP
r1 = lambda v: float(Decimal(str(v / 1e9)).quantize(Decimal('0.01'), ROUND_HALF_UP))
L8 = C.L8
D = json.loads(re.search(rf'const {T}_DAILY\s*=\s*(\[.*?\]);', h, re.S).group(1)); days = {r[0] for r in D}
MUL = json.load(open(f'{T}_multiples.json')); FB = MUL.get('fairBand'); SM = MUL['multiples']   # 최근 4분기 EPS ≤ 0이면 밴드 없음(GILD, 2026-10-01)
HIST = bd.history(T) or {}   # 현금흐름 미적용 종목(CB)은 이력이 없을 수 있다
DCF = json.loads(re.search(rf'^const {T}_DCF = (\{{.*?\}});', h, re.M).group(1))
FUND = json.loads(re.search(rf'^const {T}_FUNDAMENTAL = (\{{.*?\}});', h, re.M).group(1))
VAL = json.loads(re.search(rf'^const {T}_VALUATION = (\{{.*?\}});', h, re.M).group(1))
selfsc, peersc = VAL['self']['score'], VAL['peer']['score']
px = D[-1][4]
b = bd.base_inputs(T)
eps_ttm = round(px / SM['PER']['current'], 2) if SM.get('PER') and SM['PER'].get('current') else None
ratio = px / DCF['base'] if DCF.get('base') else None
_vote = lambda s: 1 if s >= 70 else -1 if s < 30 else 0
_dv = (1 if ratio <= 0.9 else 0 if ratio <= 1.1 else -1 if ratio <= 1.5 else -2) if ratio and DCF['base'] > 0 else -2
if DCF.get('unavailable'):   # 현금흐름 미적용(보험사, 2026-10-02 사용자 결정) — 판정은 자기 이력·동종업 두 칸
    _dv = 0
VOTES = (_vote(selfsc), _vote(peersc), _dv); TOTAL = sum(VOTES)
VERDICT = '저평가' if TOTAL >= 3 else '적정~저평가' if TOTAL >= 1 else '적정' if TOTAL > -1 else '적정~고평가' if TOTAL > -3 else '고평가'
if DCF.get('unavailable'):   # 현금흐름이 기권하면 카드 JS가 '판정 보류'로 덮어쓴다(BRKB 선례, Fable 2026-10-02)
    VERDICT = '판정 보류'
_refresh = None
if (VOTES, VERDICT) != (C.VOTES, C.VERDICT) and os.environ.get('REFRESH') == '1':
    # 갱신 모드(새 가격·자료로 다시 만들 때, 2026-10-06): 멈추지 않고 cfg의 표·판정을 고치고 기록한다 — 판정이 바뀐 카드는 목록으로 사람이 본다.
    # cfg·기록은 카드를 다 쓴 뒤(맨 끝)에 쓴다 — 중간 확인에서 멈추면 아무것도 바꾸지 않는다(Codex 2026-10-06)
    _refresh = {'ticker': T, 'old': [list(C.VOTES), C.VERDICT], 'new': [list(VOTES), VERDICT], 'self': selfsc, 'peer': peersc, 'ratio': ratio}
    print(f'표·판정 변경 {C.VOTES} {C.VERDICT} → {VOTES} {VERDICT}')
else:
    assert (VOTES, VERDICT) == (C.VOTES, C.VERDICT), (VOTES, VERDICT, selfsc, peersc, ratio)
sgn = lambda v: f'{v:+d}'.replace('-', '−') if v else '0'
# 점수 → 판정 단어(70 이상 싸다 · 30 미만 비싸다) — cfg 문장에 '(중간)' 같은 단어를 손으로 적으면 갱신 때 틀린다(2026-10-06 GILD·META·PFE·PLD·TMO·VRTX)
score_word = lambda sc: '싸다' if sc >= 70 else '비싸다' if sc < 30 else '중간'
# 부호 붙은 정수 뒤 조사(받침 기준 — 0 영·1 일·3 삼·6 육·7 칠·8 팔은 받침, ㄹ 받침(1·7·8)은 '로'): 표가 바뀌면 '−1는'·'0로'가 되던 것(Fable, 2026-10-05)
jo = lambda v, a_, b_: a_ if abs(v) % 10 in (0, 1, 3, 6, 7, 8) else b_
jo_ro = lambda v: '으로' if abs(v) % 10 in (0, 3, 6) else '로'
VOTES_TXT = f'자기 이력 {sgn(VOTES[0])} · 동종업 {sgn(VOTES[1])} · 현금흐름 ' + ('미적용' if DCF.get('unavailable') else sgn(VOTES[2])); TOTAL_TXT = sgn(TOTAL)
SEC = C.SEC; PR = C.PR; TENQ = C.TENQ; LINKS = getattr(C, 'LINKS', {})
ch = (px / D[max(-253, -len(D))][4] - 1) * 100   # 일봉이 1년보다 짧으면 첫날부터(SKHY ADR, 2026-10-05)
CH_TXT = ('제자리(' + format(ch, '+.1f') + '%)') if abs(ch) < 1 else format(ch, '+.0f') + '%'
if AUTO:
    _ac.texts(C, globals())
for _code in getattr(C, 'PRE', []):
    exec(_code, globals())

# ── 1. 헤더 ──
if FB:
    h = re.sub(rf'(id="{t}FairBand"[^>]*>)[^<]*(</span>)', lambda m: m.group(1) + f'${FB["low"]:,} ~ ${FB["high"]:,}' + m.group(2), h, count=1)
    one(f'id="{t}FairBand" style=', F(C.FAIRBAND_TITLE) + ' style=')
else:   # 같은 자리에 '해당 없음'(틀 구조 유지, CRWD 카드 한정 처리를 공통으로)
    sub(rf'id="{t}FairBand" style="[^"]*">[^<]*<', F(C.FAIRBAND_TITLE) + ' style="font-size:22px;color:var(--text3);">해당 없음<')
one('<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +110%)</span>', F(C.HEADER_REQ_LABEL))

# 루트 카드의 마지막 종목(DE)은 '다음'이 막혀 있다 — 새 종목 meta의 '이전'이 이 종목을 가리키면 그 종목으로 잇는다(ADI 추가 때 카드에 직접 고친 것, 2026-10-05)
_nb = '<span class="back-bar-nav disabled">다음 ▶</span>'
if _nb in h:
    for _mf in sorted(os.listdir(os.path.join(HERE, 'meta'))):
        if f'href="{T}_full_widget.html"' in json.load(open(os.path.join(HERE, 'meta', _mf), encoding='utf-8')).get('prev', ''):
            _nt = _mf[:-5].upper()
            one(_nb, f'<a class="back-bar-nav" href="{_nt}_full_widget.html">다음 {_nt} ▶</a>')
            break

# ── 2. 기본적 분석 ──
if L8[0] != 'Q3 FY25':
    one('분기 매출 / 순이익 / 영업이익률 (Q3 FY25~Q2 FY27)', f'분기 매출 / 순이익 / 영업이익률 ({L8[0]}~{L8[-1]})')
sub(r'const revenue=\[[^\]]*\];', 'const revenue=' + json.dumps([r1(rev[k]) for k in ks]).replace(' ', '') + ';')
sub(r'const netIncome=\[[^\]]*\];', 'const netIncome=' + json.dumps([r1(ni_chart[k]) for k in ks]).replace(' ', '') + ';')
if CORE:
    h = h.replace('분기 매출 / 순이익 / 영업이익률', '분기 매출 / 순이익(본업 기준) / 영업이익률', 1)
opm = [round(op[k] / rev[k] * 100, 1) for k in ks]
assert C.OPM_RANGE[0] < min(opm) and max(opm) < C.OPM_RANGE[1], opm
sub(r'const opm=\[[^\]]*\];', 'const opm=' + json.dumps(opm).replace(' ', '') + ';')
one('const y2min=40, y2max=75;', f'const y2min={C.Y2[0]}, y2max={C.Y2[1]};')
if L8[0] != 'Q3 FY25':
    one("labels:['Q3 FY25','Q4 FY25','Q1 FY26','Q2 FY26','Q3 FY26','Q4 FY26','Q1 FY27','Q2 FY27'],", 'labels:' + json.dumps(L8).replace('"', "'").replace(', ', ',') + ',')
QL = C.QLABEL   # 예: 'Q2 2026'
# 설비투자 태그가 없는 회사(NEE — 회사 고유 태그)는 FCF·Capex 칸을 같은 자리에 "해당 없음"으로(2026-10-02)
for lab, val, subt in [('FCF', f'${r1(fcf[cur])}B' if cur in fcf else '해당 없음', F(C.FCF_SUB)), ('Capex', f'${r1(cap[cur])}B' if cur in cap else '해당 없음', F(C.CAPEX_SUB))]:
    sub(rf'<div class="stat-label">{lab} \(Q2 FY27\)</div>\n      <div class="stat-value">[^<]*</div>\n      <div class="stat-sub">[^<]*</div>',
        f'<div class="stat-label">{lab} ({QL})</div>\n      <div class="stat-value">{val}</div>\n      <div class="stat-sub">{subt}</div>')
_s3 = C.STAT3
sub(r'<div class="stat-label">R&amp;D \(Q2 FY27\)</div>\n      <div class="stat-value">[^<]*</div>\n      <div class="stat-sub">[^<]*</div>',
    f'<div class="stat-label">{F(_s3[0])}</div>\n      <div class="stat-value">{F(_s3[1])}</div>\n      <div class="stat-sub">{F(_s3[2])}</div>')
sub(r'<div class="stat-value">11월 중순 예상</div>\n      <div class="stat-sub">일정 · Q3 FY27</div>',
    f'<div class="stat-value">{C.NEXT[0]}</div>\n      <div class="stat-sub">{C.NEXT[1]}</div>')
one('재무 건전성 — 안정성·활동성 (Q2 FY27 · 2026.07.26 기준)', f'재무 건전성 — 안정성·활동성 ({QL} · {C.CUR.replace("-", ".")} 기준)')
_, arows = bmh.pick_tag(CIK, ['Assets'])
AS = {r['end']: r['val'] / 1e6 for r in sorted(arows, key=lambda r: r['filed']) if r.get('form') == '10-K'}
a1, a0 = AS[C.FY_ENDS[0]], AS[C.FY_ENDS[1]]
sub(r'<span class="diag-label">총자산증가율</span><span class="diag-value">[^<]*</span><span class="diag-note">[^<]*</span>',
    f'<span class="diag-label">총자산증가율</span><span class="diag-value">{(a1 / a0 - 1) * 100:+.1f}%</span><span class="diag-note">{C.FY_LABEL} 말 ${a1 / 1000:.1f}B(전년 ${a0 / 1000:.1f}B) · 연간 지표</span>')
sub(r'<div style="margin-top:14px;font-size:11\.5px;color:var\(--text2\);line-height:1\.6;">유동비율·당좌비율.*?</div>',
    '<div style="margin-top:14px;font-size:11.5px;color:var(--text2);line-height:1.6;">' + F(C.HEALTH_NOTE)
    + f' <a href="{TENQ}" target="_blank" rel="noopener">{C.TENQ_NAME} (SEC) →</a></div>')
class _JsNull:
    def __repr__(self):
        return 'null'
vec = lambda e: [r1(rev[e]), r1(op[e]), r1(ni_chart[e]), (r1(fcf[e]) if e in fcf else _JsNull())]
f = lambda a, b_: '—' if a is None or b_ is None else ('흑자 전환' if a > 0 else '적자 지속') if b_ <= 0 else ('적자 전환' if a <= 0 else ('약 %.0f배' % (a / b_) if a / b_ >= 10 else ('0.0%' if abs(a / b_ - 1) < 0.0005 else '%+.1f%%' % ((a / b_ - 1) * 100))))
yd = [f(rev[cur], rev[yo]), f(op[cur], op[yo]), f(ni_chart[cur], ni_chart[yo]), f(fcf.get(cur), fcf.get(yo))]
qd = [f(rev[cur], rev[qo]), f(op[cur], op[qo]), f(ni_chart[cur], ni_chart[qo]), f(fcf.get(cur), fcf.get(qo))]
tq = lambda a: ', '.join(f"'{x}'" for x in a)
sub(r"curLabel: 'Q2 FY27', cmpLabel: 'Q2 FY26',\n    titleSuffix: '[^']*',\n    chart: \{ cur: \[[^\]]*\], cmp: \[[^\]]*\] \},\n    deltas: \[[^\]]*\],",
    f"curLabel: '{QL}', cmpLabel: '{C.YL}',\n    titleSuffix: 'YoY ({QL} vs {C.YL})',\n    chart: {{ cur: {vec(cur)}, cmp: {vec(yo)} }},\n    deltas: [{tq(yd)}],")
sub(r"curLabel: 'Q2 FY27', cmpLabel: 'Q1 FY27',\n    titleSuffix: '[^']*',\n    chart: \{ cur: \[[^\]]*\], cmp: \[[^\]]*\] \},\n    deltas: \[[^\]]*\],",
    f"curLabel: '{QL}', cmpLabel: '{C.QQL}',\n    titleSuffix: 'QoQ ({QL} vs {C.QQL})',\n    chart: {{ cur: {vec(cur)}, cmp: {vec(qo)} }},\n    deltas: [{tq(qd)}],")
fn = lambda a, extra='': (f"footnote: '기준일: {C.CUR.replace('-', '.')}({QL}) vs {a} · GAAP 기준{(', 순이익은 본업 기준(공시 순이익 ' + QL + ' $' + str(r1(ni_gaap[cur])) + 'B)') if CORE else ''} · FCF는 영업현금흐름 − 설비투자 · {extra}"
                          f"<a href=\"{PR[getattr(C, 'PR_CUR', 'q2')]}\" target=\"_blank\" rel=\"noopener\">{C.CO} {QL} 실적 보도자료 (SEC 8-K) →</a>'")
sub(r"footnote: '기준일: 2026\.07\.26\(Q2 FY27\) vs 2025\.07\.27\(Q2 FY26\)[^\n]*'", fn(f'{C.YO.replace("-", ".")}({C.YL})', F(C.YOY_EXTRA)))
sub(r"footnote: '기준일: 2026\.07\.26\(Q2 FY27\) vs 2026\.04\.26\(Q1 FY27\)[^\n]*'", fn(f'{C.QO.replace("-", ".")}({C.QQL})'))
if QL != 'Q2 FY27':
    one('<span id="fundPeriodTitle">YoY (Q2 FY27 vs Q2 FY26)</span>', f'<span id="fundPeriodTitle">YoY ({QL} vs {C.YL})</span>')
SEG = C.SEG
tot = sum(v for _, v, _ in SEG)
assert abs(tot + C.SEG_ADJ - rev[cur] / 1e6) <= 1.5, (tot, C.SEG_ADJ, rev[cur])
leg = ''.join(f'\n          <div style="display:flex;align-items:center;gap:7px;font-size:11px;color:var(--text2);white-space:nowrap;"><span style="width:8px;height:8px;border-radius:50%;background:{c};display:inline-block;flex-shrink:0;"></span>{n} <strong style="color:var(--text);">${v / 1000:.2f}B · {v / tot * 100:.1f}%</strong></div>' for n, v, c in SEG)
sub(r'<div class="card-title">매출 구성 — Market Platform.*?</div>\n\n      <div style="display:flex;align-items:center;justify-content:center;gap:20px;">.*?\n      </div>\n\n      <div class="yoy-footnote" style="margin-top:14px;">.*?</div>',
    f'<div class="card-title">{C.SEG_TITLE} ({QL} · {C.CUR.replace("-", ".")} 기준)</div>\n\n      <div style="display:flex;align-items:center;justify-content:center;gap:20px;">\n        <div class="chart-wrap" style="height:170px;width:170px;flex-shrink:0;">\n          <canvas id="segmentPieChart"></canvas>\n        </div>\n        <div style="display:flex;flex-direction:column;gap:9px;">' + leg +
    '\n        </div>\n      </div>\n\n      <div class="yoy-footnote" style="margin-top:14px;">' + F(C.SEG_NOTE) + '</div>')
sub(r'// ─── 매출 구성 도넛 차트 \([^)]*\) ───', f'// ─── 매출 구성 도넛 차트 ({QL}, 백만 달러) ───')
one('const total = 96221;', f'const total = {tot};')
one("labels:['Hyperscale','AI Clouds·Industrial·Enterprise','Edge Computing'],", 'labels:' + json.dumps([n for n, _, _ in SEG], ensure_ascii=False) + ',')
one('data:[48710, 40313, 7198],', 'data:[' + ', '.join(str(v) for _, v, _ in SEG) + '],')
sub(r"backgroundColor:\['#[0-9a-fA-F]{6}','#4d7a00','#3498db'\],", 'backgroundColor:' + json.dumps([c for _, _, c in SEG]) + ',')
one('<div class="card-title">자본배분 · 주주환원 (Q2 FY27 · 2026.07.26 기준)</div>', f'<div class="card-title">자본배분 · 주주환원 ({QL} · {C.CUR.replace("-", ".")} 기준)</div>')
(z1l, z1v), (z2l, z2v), (z3l, z3t, z3v) = C.CAPITAL
one('<span class="zone-label">자사주 매입 (Q2 FY27)</span>\n          <div style="display:flex;align-items:center;gap:8px;">\n            <span class="zone-val">$19.7B</span>',
    f'<span class="zone-label">{z1l}</span>\n          <div style="display:flex;align-items:center;gap:8px;">\n            <span class="zone-val">{z1v}</span>')
one('<span class="zone-label">잔여 바이백 승인 한도 (2026.07.26 기준)</span>\n          <span class="zone-val">$99.3B</span>',
    f'<span class="zone-label">{z2l}</span>\n          <span class="zone-val">{z2v}</span>')
sub(r'<span class="zone-label">배당 \(Q2 FY27\)</span>\n          <div style="display:flex;align-items:center;gap:8px;">\n            <span class="zone-tag" style="background:rgba\(240,192,64,0\.18\);color:var\(--gold\);">[^<]*</span>\n            <span class="zone-val">\$6\.0B</span>',
    f'<span class="zone-label">{z3l}</span>\n          <div style="display:flex;align-items:center;gap:8px;">\n            <span class="zone-tag" style="background:rgba(240,192,64,0.18);color:var(--gold);">{z3t}</span>\n            <span class="zone-val">{z3v}</span>')
CHECK = (f'<div class="card-title">다음 실적 체크포인트 <span style="color:var(--gold);font-weight:600;">{C.CHECK_WHEN}</span></div>\n    <div style="font-size:12px;color:var(--text2);line-height:1.8;">\n'
         + '\n'.join(f'      <div{" style=\"margin-bottom:8px;\"" if i < 3 else ""}><strong style="color:var(--accent2);">{"①②③④"[i]}</strong> {F(x)}</div>' for i, x in enumerate(C.CHECK)) + '\n    </div>')
sub(r'<div class="card-title">다음 실적 체크포인트 <span[^>]*>[^<]*</span></div>\n    <div style="font-size:12px;color:var\(--text2\);line-height:1\.8;">.*?\n    </div>', CHECK)
_usd = lambda v: ('−$' if v < 0 else '$') + f'{abs(v):.2f}'   # 음수 기본값(BA) — "$-63.51" 대신 "−$63.51"
if DCF.get('nonopPerShare', 0) >= 0.5 and not (AUTO and DCF.get('base') is not None and DCF['base'] <= 0):   # 자동 카드: 음수 기본값은 이 줄에서도 드러내지 않는다(BA, Fable)
    one('<div class="note" data-dcf-nonop>기본 시나리오 $314 = 사업 가치 $310 + 비영업 자산 $4(주당, 지분·장기투자)</div>', f'<div class="note" data-dcf-nonop>기본 시나리오 {_usd(DCF["base"])} = 사업 가치 {_usd(DCF["base"] - DCF["nonopPerShare"])} + 비영업 자산 ${DCF["nonopPerShare"]:.2f}(주당, {C.NONOP_WHAT})</div>')
else:
    one('<div class="note" data-dcf-nonop>기본 시나리오 $314 = 사업 가치 $310 + 비영업 자산 $4(주당, 지분·장기투자)</div>', '<div class="note" data-dcf-nonop hidden></div>')

# ── 3. 밸류에이션 ──
PH = C.PH
if C.PEER_FILE:
    U = json.load(open(C.PEER_FILE))['tickers']
    _isnum = lambda tk, k: isinstance(U.get(tk, {}).get(k), (int, float))
    peers = {k: [(tk, round(U[tk][k], 1)) for tk in PH if _isnum(tk, k) and not (k in C.CHART_CAP and U[tk][k] > C.CHART_CAP[k])] for k in ('per', 'pbr', 'psr', 'pcr', 'evebitda')}
    miss = {k: [tk for tk in PH if not _isnum(tk, k)] for k in peers}
    # C9(2026-10-04)로 순이익률 2% 미만·적자 종목의 PER이 perNA로 옮겨져 'negative' 표시가 사라졌다 — 카드가 '적자'로 적은 것은 cfg MISS_WHY로(NEM·BMY·VRTX)
    _why = lambda tk, k: getattr(C, 'MISS_WHY', {}).get((tk, k)) or (' 적자' if U.get(tk, {}).get(k) == 'negative' else ' 값 없음')
    _ua = json.load(open(C.PEER_FILE))['asOf']
    _ld = D[-1][0]   # 카드 막대 날짜 = 카드 마지막 종가(재현 모드에서는 옛 카드 날짜, 2026-10-05 — 예전엔 9/30 고정)
    DT = f'{int(_ua[5:7])}/{int(_ua[8:10])} 종가' + ('' if _ua == _ld else f'({T} 막대는 {int(_ld[5:7])}/{int(_ld[8:10])})')
else:
    import build_peer_score as bps
    PR_ = bps.load_prices()
    now = {tk: bps.multiples_now(tk, PR_) for tk in PH}
    peers = {k: [(tk, round(now[tk][0][k], 1)) for tk in PH if k in now[tk][0] and not (k in C.CHART_CAP and now[tk][0][k] > C.CHART_CAP[k])] for k in ('per', 'pbr', 'psr', 'pcr', 'evebitda')}
    miss = {k: [tk for tk in PH if k not in now[tk][0]] for k in peers}
    _why = lambda tk, k: getattr(C, 'MISS_WHY', {}).get((tk, k), ' 값 없음')
    DT = f'{min(v[1] for v in now.values())[5:].replace("-", "/")}~{max(v[1] for v in now.values())[5:].replace("-", "/")} 카드 기준({T} 막대는 {int(D[-1][0][5:7])}/{int(D[-1][0][8:10])})'
_m = lambda k: f' ({"·".join(tk + _why(tk, k) for tk in miss[k])})' if miss[k] else ''
_cur = lambda k: (SM.get({'per': 'PER', 'pbr': 'PBR', 'psr': 'PSR', 'pcr': 'PCR', 'evebitda': 'EV/EBITDA'}[k]) or {}).get('current') or 0
_mx = lambda k: int(math.ceil(max([v for _, v in peers[k]] + [min(_cur(k), C.SELF_CAP.get(k, 1e9))] + [1]) * 1.15 / 5) * 5)
meta = {k: (C.CHART_TITLES[k] + _m(k) + C.CHART_NOTE.get(k, ''), {'per': 'PER', 'pbr': 'PBR', 'psr': 'PSR(TTM)', 'pcr': 'PCR(FCF)', 'evebitda': 'EV/EBITDA'}[k], _mx(k)) for k in peers}
one('<div class="vs-name" title="같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.">동종업 대비</div>',
    f'<div class="vs-name" title="{C.PEER_NAME_TITLE}">동종업 대비</div>')
md = 'const MULTIPLE_DATA = {\n' + ',\n'.join(
    f"  {k}: {{\n    title: '{meta[k][0]} · {DT}',\n    unit: '{meta[k][1]}', max: {meta[k][2]}, {t}Value: null,\n    peers: [\n" +
    ',\n'.join(f"      {{ name:'{n}', value:{v}, status:'reference' }}" for n, v in peers[k]) + "\n    ]\n  }" for k in peers) + '\n};'
sub(r'const MULTIPLE_DATA = \{.*?\n\};', md)
one('<div class="card-title"><span id="multipleCompareTitle">글로벌 AI 반도체 PER 비교</span></div>',
    f'<div class="card-title"><span id="multipleCompareTitle">{meta["per"][0]} · {DT}</span></div>')
sub(r'<div class="vs-premise">.*?</div>\n    <div class="verdict-summary-risk">.*?</div>',
    '<div class="vs-premise">' + F(C.PREMISE) + '</div>\n    <div class="verdict-summary-risk">⚠️ ' + F(C.RISK) + '</div>')
SCORES = f"""const {T}_SCORES = {{
  fundamental: {FUND["score"]},   // 재무건전성 + 성장·수익성 (밸류에이션 축 제외)
  peer: {peersc},          // {C.PEER_COMMENT}
  selfHistory: {selfsc},   // 자기 5년 배수 분포 백분위 ({D[0][0]} ~ {D[-1][0]})
  asOf: "{D[-1][0]}",
  fundamentalAsOf: "{C.CUR}",   // {C.FUND_ASOF_NOTE}
}};"""
sub(rf'const {T}_SCORES = \{{.*?\n\}};', SCORES)
sub(r'// 기본적 분석이 98\.1이 아니라 96\.1인 이유\..*?// `--basis annual`로 돌리면 98\.1이 그대로 나온다 — 배점을 안 건드렸다는 확인이다\.\n', '')
one("+ `\\n대차대조표와 마진은 ${S.fundamentalAsOf} 분기(확인 필요), 성장률은 연간 시계열을 쓴다.`",
    ("+ `\\n대차대조표는 ${S.fundamentalAsOf} 시점, 마진·이자보상배율은 " + C.FY_LABEL + " 연간(10-K), 성장률은 연간 시계열(" + C.FY_LABEL + "까지)을 쓴다.`"
     if FUND.get('periodSource') == '10-K' else   # 최신 공시가 10-K면 분기가 아니라 연간 값이다(STX, Codex 2026-10-01)
     "+ `\\n대차대조표와 마진은 ${S.fundamentalAsOf} 분기(" + QL + ", 10-Q), 성장률은 연간 시계열(" + C.FY_LABEL + "까지)을 쓴다.`"))
one("+ `\\n(확인 필요 — NVDA 문장 자리)`);", "+ `\\n" + F(C.FUND_TIP) + "`);")
one("+ `\\n(확인 필요 — NVDA 문장 자리)`\n", "+ `\\n" + F(C.SELF_TIP) + "`\n")
if '`이 종목 자신의 5년 배수 분포에서 현재값이 하위 몇 %인지를 점수로 쓴 값이다.`' in h:   # 틀(NVDA)은 2026-10-05에 고쳐졌다(E13)
    one('`이 종목 자신의 5년 배수 분포에서 현재값이 하위 몇 %인지를 점수로 쓴 값이다.`', '`이 종목 자신의 5년 배수 분포에서 지금과 배수가 같거나 높았던 날의 비율을 점수로 쓴 값이다.`')
if getattr(C, 'GROWTH_SPAN', None):   # 현금흐름 이력이 5년보다 짧은 종목(분사) — 역산 설명의 "지난 5년"을 실제 이력으로(2026-10-02, DHR Codex 2차)
    for _o in ('매출이 지난 5년 속도', '필요해 지난 5년의 3배', '필요해 지난 5년 실제의 3배'):
        assert h.count(_o) >= 1, _o; h = h.replace(_o, _o.replace('지난 5년', C.GROWTH_SPAN))
if getattr(C, 'SELF_SPAN', None):   # 자기 이력이 5년보다 짧은 종목(분사·흑자 전환) — "5년" 표기를 실제 이력으로(2026-10-02, DHR Codex)
    one('<div class="card-title">배수별 자기 5년 위치</div>', f'<div class="card-title">배수별 자기 이력 위치 ({C.SELF_SPAN})</div>')
    one(f'title="지난 5년 {T} 자신의 배수보다', f'title="{T} 자신의 배수 이력({C.SELF_SPAN})보다')
    # 틀 문구가 E13(2026-10-05)에서 '지금과 배수가 같거나 높았던 날의 비율'로 바뀌어 옛 앵커('지금보다')가 없어졌다 — 둘 다 받는다
    _sa = '`이 종목 자신의 5년 배수 분포에서 지금보다' if '`이 종목 자신의 5년 배수 분포에서 지금보다' in h else '`이 종목 자신의 5년 배수 분포에서 지금과'
    one(_sa, _sa.replace('5년 배수 분포에서', f'배수 이력({C.SELF_SPAN})에서'))
one("`같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.`", "`" + F(C.PEER_TIP[0]) + "`")
one("+ `\\n회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.`);", "+ `\\n" + F(C.PEER_TIP[1]) + "`);")

# ── 4. 내재가치 ──
new = [F(x) for x in C.STORIES]
olds = re.findall(r'<td class="story">(지난 5년 성장 속도의 절반.*?|지난 5년의 성장 속도로.*?|최근 3년의 성장 속도로.*?)</td>', h)
assert len(olds) == 3, len(olds)
for o, n in zip(olds, new):
    assert h.count(o) == 1
    h = h.replace(o, n)
if DCF.get('unavailable'):   # 현금흐름 미적용 — 계산했다는 문구를 빼고 사유만(CB)
    one('<div class="lede">회사가 앞으로 벌어들일 현금만으로 계산한 주당 가치다.</div>', '<div class="lede">이 종목은 현금흐름 내재가치를 계산하지 않는다.</div>')
    one('<div class="note">세 값은 확률이 아니라, 과거 실적에서 서로 다른 가정을 뽑아 계산한 결과다.</div>', '<div class="note">' + F(C.DCF_NOTE) + '</div>')
else:
 one('<div class="note">세 값은 확률이 아니라, 과거 실적에서 서로 다른 가정을 뽑아 계산한 결과다.</div>',
    '<div class="note">세 값은 확률이 아니라, 과거 실적에서 서로 다른 가정을 뽑아 계산한 결과다.' + (' ' + F(C.DCF_NOTE) if getattr(C, 'DCF_NOTE', '') else '') + '</div>')
# 음수·$10 미만 시나리오, 이력 기간 표기(카드 한정 패치 모음 — PANW·TMO·LIN·CRWD에서 쓴 것과 같다)
one_done("    el.textContent = '$' + D[el.dataset.dcfValue].toFixed(2);", "    const v0 = D[el.dataset.dcfValue]; el.textContent = v0 > 0 ? '$' + v0.toFixed(2) : '계산 불가(음수)';   // 카드 한정")
one_done("    const v = D[el.dataset.dcfUpside];\n    el.textContent = pct(v); el.style.color = tone(v);",
    "    const v = D[el.dataset.dcfUpside];\n    if (!(v > 0)) { el.textContent = '—'; return; }   // 음수 시나리오(카드 한정)\n    el.textContent = pct(v); el.style.color = tone(v);")
one_done("    + ' · 높은 성장 $' + Math.round(d.high) + '</span>';", "    + ' · 낙관 ' + (d.high > 0 ? '$' + (d.high < 10 ? d.high.toFixed(2) : Math.round(d.high)) : '계산 불가') + '</span>';")
one_done("    + '<span class=\"logic-denom\"> · 낮은 성장 $' + Math.round(d.low)", "    + '<span class=\"logic-denom\"> · 보수 ' + (d.low > 0 ? '$' + (d.low < 10 ? d.low.toFixed(2) : Math.round(d.low)) : '계산 불가')")
one("m.percentile >= 50 ? `5년 중 상위 ${Math.round(100 - m.percentile)}%` : `5년 중 하위 ${Math.round(m.percentile)}%`;",
    "m.percentile >= 50 ? `${m.days < 1200 ? (m.days / 252).toFixed(1) + '년' : '5년'} 중 상위 ${Math.round(100 - m.percentile)}%` : `${m.days < 1200 ? (m.days / 252).toFixed(1) + '년' : '5년'} 중 하위 ${Math.round(m.percentile)}%`;   // 이력이 짧은 배수는 실제 기간(카드 한정)")
one_done("  const every = SCN.flatMap(s => G.values[s[0]].flat()).concat(price != null ? [price] : []);",
    "  const every = SCN.flatMap(s => G.values[s[0]].flat()).filter(v => v != null && v > 0).concat(price != null ? [price] : []);   // 음수 칸 제외(카드 한정)")
one_done("    pv.textContent = '주당 $' + Math.round(pick); pv.style.color = col;",
    "    pv.textContent = pick > 0 ? '주당 $' + (pick < 10 ? pick.toFixed(2) : Math.round(pick)) : '계산 불가(음수)'; pv.style.color = col;")
one_done("    if (price != null) { pu.textContent = '현재가 대비 ' + pct(pick); pu.style.color = tone(pick); }",
    "    if (price != null) { pu.textContent = pick > 0 ? '현재가 대비 ' + pct(pick) : '—'; pu.style.color = pick > 0 ? tone(pick) : ''; }")
one_done("      + SCN.map((s, i) => `<div class=\"ruler-pt${i === st.scn ? ' on' : ''}\" style=\"left:${x(vals[i])};color:${s[2]}\">`\n        + `<div class=\"ruler-lab\">${s[0]}<br>$${Math.round(vals[i])}</div><div class=\"ruler-dot\" style=\"background:${s[2]}\"></div></div>`).join('');",
    "      + SCN.map((s, i) => !(vals[i] > 0) ? '' : `<div class=\"ruler-pt${i === st.scn ? ' on' : ''}\" style=\"left:${x(vals[i])};color:${s[2]}\">`\n        + `<div class=\"ruler-lab\">${s[0]}<br>$${vals[i] < 10 ? vals[i].toFixed(2) : Math.round(vals[i])}</div><div class=\"ruler-dot\" style=\"background:${s[2]}\"></div></div>`).join('');")
h = h.replace("'$' + Math.round(d.base)", "'$' + (Math.abs(d.base) < 10 ? d.base.toFixed(2) : Math.round(d.base))")
h = h.replace("'$' + Math.round(D.base)", "'$' + (Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base))")
h = h.replace("${Math.round(d.base)}", "${Math.abs(d.base) < 10 ? d.base.toFixed(2) : Math.round(d.base)}").replace("${Math.round(D.base)}", "${Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base)}")
sub(r'<div class="reverse">.*?</div>', '<div class="reverse">—</div>')   # JS가 문장으로 채운다(틀 NVDA 숫자 제거)
# 기본 내재가치가 0 이하면 헤더·밸류에이션 칸을 "0 이하"·"—"로 — 시나리오 표의 "계산 불가(음수)"와 맞춘다(T·WELL, Fable 2026-10-02)
one_done("put('dcf', '$' + (Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base)));", "put('dcf', D.base > 0 ? '$' + (Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base)) : '0 이하');")
one_done("    if (D && D.base != null) { const u = (D.base / last[4] - 1) * 100;", "    if (D && D.base != null && D.base > 0) { const u = (D.base / last[4] - 1) * 100;")
one_done("  if (box)  box.innerHTML = '$' + (Math.abs(d.base) < 10 ? d.base.toFixed(2) : Math.round(d.base))", "  if (box)  box.innerHTML = (d.base > 0 ? '$' + (Math.abs(d.base) < 10 ? d.base.toFixed(2) : Math.round(d.base)) : '0 이하')")
one_done("put('low', '$' + Math.round(D.low));", "put('low', D.low > 0 ? '$' + (D.low < 10 ? D.low.toFixed(2) : Math.round(D.low)) : '계산 불가');")
# 시나리오 범위·갈림은 세 값 최소·최대(이름 순서가 뒤집힌 카드가 많다 — AXP·CRWD·LIN)
one_done("  const split = D.low > 0 && D.high > 0 && D.low < price && price < D.high;\n  const range = (D.low > 0 && D.high > 0)\n    ? `시나리오 범위: 낙관 기준 ${(price / D.high).toFixed(2)} ~ 보수 기준 ${(price / D.low).toFixed(2)}` : '';",
    "  const _mn = Math.min(D.low, D.base, D.high), _mx = Math.max(D.low, D.base, D.high);   // 세 시나리오 최소·최대(카드 한정)\n  const split = _mn > 0 && _mn < price && price < _mx;\n  const range = _mn > 0\n    ? `시나리오 범위: ${(price / _mx).toFixed(2)} ~ ${(price / _mn).toFixed(2)}(세 시나리오 최대·최소 기준)` : '';")
# 내재가치 추적선 음수 값(카드 한정, LIN)
one_done("      : dcfVisible.flatMap(t => [clipDcf(t.low), clipDcf(t.high)]);", "      : dcfVisible.flatMap(t => [t.low, t.base, t.high].filter(v => v > 0).map(clipDcf));   // 음수는 빼고 기본도 축에 넣는다(카드 한정, Codex)")
one_done("          const yTop = overlapOnly ? py(clipDcf(e.v.base)) - 6 : py(clipDcf(e.v.high));\n          const yBot = overlapOnly ? py(clipDcf(e.v.base)) + 6 : py(clipDcf(e.v.low));",
    "          const _vmx = Math.max(e.v.low, e.v.base, e.v.high), _vmn = Math.max(Math.min(e.v.low, e.v.base, e.v.high), 0);   // 순서가 뒤집힌 시나리오도 잡히게(카드 한정, Codex)\n          const yTop = overlapOnly ? py(clipDcf(e.v.base)) - 6 : py(clipDcf(_vmx));\n          const yBot = overlapOnly ? py(clipDcf(e.v.base)) + 6 : py(clipDcf(_vmn));")
one_done("          const usd = x => (x < 0 ? '−$' : '$') + Math.abs(x).toFixed(0);", "          const usd = x => x < 0 ? '계산 불가(음수)' : '$' + x.toFixed(0);   // 카드 한정")
# 재고 없는 회사의 회전율·현금순환 문장(카드 한정, CRWD)
# 틀(NVDA)에 2026-10-05 '재고 없음' 가드가 들어갔다(META Infinity회) — 그 줄이면 옛 줄로 되돌린 뒤 아래 교체를 그대로 적용한다
_TPL_TURN = "  document.querySelectorAll('[data-act-turn]').forEach(el => { el.textContent = A.now[el.dataset.actTurn] > 0 ? (365 / A.now[el.dataset.actTurn]).toFixed(2) + '회' : (el.dataset.actTurn === 'dio' ? '재고 없음' : '해당 없음'); });   // 회전기간 0(재고 없음)이면 Infinity회가 찍혔다(META, 2026-10-05)"
if _TPL_TURN in h:
    h = h.replace(_TPL_TURN, "  document.querySelectorAll('[data-act-turn]').forEach(el => { el.textContent = (365 / A.now[el.dataset.actTurn]).toFixed(2) + '회'; });")
one("  document.querySelectorAll('[data-act-turn]').forEach(el => { el.textContent = (365 / A.now[el.dataset.actTurn]).toFixed(2) + '회'; });",
    "  document.querySelectorAll('[data-act-turn]').forEach(el => { const dd = A.now[el.dataset.actTurn]; el.textContent = dd > 0 ? (365 / dd).toFixed(2) + '회' : '해당 없음'; });   // 카드 한정")
h = h.replace("`재고를 사서 판매 대금을 회수하기까지 ${d1(A.now.op)}일이 걸리는데", "`${A.now.dio > 0 ? '재고를 사서 ' : ''}판매 대금을 회수하기까지 ${d1(A.now.op)}일이 걸리는데")
# 계산 어려움 메모 끝 구분점(카드 한정, CRWD)
h = h.replace("D.hard.map(k => (TXT[k] ? TXT[k]() : k).split(' — ')[0]).join(' · ') + ' · ' : '') + tv;", "D.hard.map(k => (TXT[k] ? TXT[k]() : k).split(' — ')[0]).join(' · ') + (tv ? ' · ' : '') : '') + tv;", 1)
# 이 카드에 없는 배수는 같은 자리에 '계산 불가'(카드 한정, CRWD)
_have = {m['metric'] for m in VAL['self']['metrics']}
if len(_have) < 5:
    one(f"  ['peer', 'self'].forEach(k => {{",
        f"""  const haveM = new Set({T}_VALUATION.self.metrics.map(m => m.metric));   // 없는 배수 칸(카드 한정)
  document.querySelectorAll('#valuation .val-item[data-metric]').forEach(item => {{
    if (haveM.has(item.dataset.metric)) return;
    const f = sel => item.querySelector(`[data-hist="${{sel}}"]`);
    if (f('cur')) f('cur').textContent = '—';
    if (f('badge')) {{ f('badge').className = 'hist-badge mid'; f('badge').textContent = '계산 불가'; }}
    if (f('note')) f('note').textContent = {json.dumps(getattr(C, 'MISSING_NOTE', '데이터 없음'), ensure_ascii=False)};
    if (f('fill')) {{ f('fill').className = 'val-fill hist-fill mid'; f('fill').style.width = '0%'; }}
    ['min', 'median', 'max'].forEach(k => {{ if (f(k)) f(k).textContent = '—'; }});
  }});
  ['peer', 'self'].forEach(k => {{""")

# 공통 문구(카드 한정): 요구 영업이익률 라벨 기간, 역산 문장 대시, 비영업 자산 표기, 차트의 시나리오 이름
h = h.replace("`현재가 요구 영업이익률 (현재 ${f1(d.marginNow)})`", "`현재가 요구 영업이익률 (최근 4분기 ${f1(d.marginNow)})`")
h = h.replace("`\\n성장만으로는 설명되지 않는다 — ` + (d.requiredGrowth != null", "`\\n성장만으로는 설명되지 않는다. ` + (d.requiredGrowth != null")
h = h.replace("` 성장만으로는 설명되지 않는다 — ` + (D.requiredGrowth != null", "` 성장만으로는 설명되지 않는다. ` + (D.requiredGrowth != null")
h = h.replace("(주당, 지분·장기투자)`", f"(주당, {C.NONOP_WHAT})`")
# 비영업 자산 줄: 부호 처리식 하나로(양수면 출력이 예전과 같고, 음수 기본값은 '−$59.75' — BA·INTC, 18cf363·Fable 2026-10-05)
h = h.replace('기본 시나리오 $${Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base)} = 사업 가치 $${Math.round(D.base) - Math.round(n)} + 비영업 자산 $${Math.round(n)}', "기본 시나리오 ${(D.base < 0 ? '−$' : '$') + Math.abs(D.base).toFixed(2)} = 사업 가치 ${(D.base - n < 0 ? '−$' : '$') + Math.abs(D.base - n).toFixed(2)} + 비영업 자산 $${n.toFixed(2)}", 1)
h = h.replace("공시 기준 — 낮은 성장 ${usd(e.v.low)}`", "공시 기준 · 보수 ${usd(e.v.low)}`").replace("` · 기본 ${usd(e.v.base)} · 높은 성장 ${usd(e.v.high)}`", "` · 기본 ${usd(e.v.base)} · 낙관 ${usd(e.v.high)}`")
h = h.replace("' · 높은 성장은 화면 밖이라 잘라서 표시'", "' · 낙관은 화면 밖이라 잘라서 표시'").replace("'\\n⚠ 이 시점엔 높은 성장이 가장 낮다 — ", "'\\n⚠ 이 시점엔 낙관이 가장 낮다. ")
h = h.replace("' 낮은·기본·높은 세 가정의 범위.'", "' 보수·기본·낙관 세 가정의 범위.'")

# ── 5. 뉴스 ──
def item(dot, date, react, title, href, src):
    cls = f'tl-dot {dot}'.strip()
    rx_ = f'<span class="tl-reaction flat" data-react="{react}">0.0%</span>' if react else ''
    return (f'      <div class="tl-item">\n        <div class="{cls}"></div>\n        <div class="tl-date">{date}{rx_}</div>\n'
            f'        <div class="tl-title">{title}</div>\n        <a class="tl-source" href="{href}" target="_blank" rel="noopener">{src} →</a>\n      </div>')


items = [(d_, dt, rx, ti, (PR.get(hr) or LINKS.get(hr) or hr), src) for d_, dt, rx, ti, hr, src in C.NEWS]
# 자동 뉴스(news_auto.py, 2026-10-08): 손 뉴스보다 뒤에 나온 실적 발표 8-K — 날짜·제목·보도자료 링크만, 숫자는 분기 반영 때 사람이 쓴다.
# 카드 마지막 종가 날짜까지 접수된 것만(시점 규칙). 손 뉴스에 같은 발표(앞 1일~뒤 3일)가 있으면 넣지 않는다.
_auto_p = os.path.join(os.path.dirname(HERE), "news_auto.json")
_auto = [e for e in (json.load(open(_auto_p)).get(T, []) if os.path.exists(_auto_p) else []) if e.get("results")]
if _auto:
    import datetime as _dt
    import news_auto as _na
    _hand, _last = _na.hand_dates(C), max(days)
    _new = []
    for e in _auto:
        d = _dt.date.fromisoformat(e["date"])
        if e["filed"] > _last or (_hand and d <= max(_hand)) or any(d - _dt.timedelta(days=1) <= x <= d + _dt.timedelta(days=3) for x in _hand):
            continue
        # 주가 반응일: 미국 동부 16시 이후 접수면 다음 거래일 — 카드 일봉에 있는 첫날
        r0 = (d + _dt.timedelta(days=1)).isoformat() if e["after_close"] else e["date"]
        rx = min((x for x in days if x >= r0), default=None)
        # 날짜는 주가가 반응한 거래일로, 장 마감 뒤 접수면 괄호로 밝힌다 — PEP 8-K가 10/7 저녁 접수, 보도·반응은 10/8(Fable 2026-10-10)
        _shown = _dt.date.fromisoformat(rx) if rx else d
        _when = f'{_shown.year}년 {_shown.month}월 {_shown.day}일' + (f' (공시 접수 {d.month}/{d.day} 장 마감 뒤)' if e["after_close"] and rx and rx != e["date"] else '')
        _body = '실적 보도자료 공시(8-K 2.02항) — 매출·이익 숫자는 분기 보고서를 확인한 뒤 이 카드에 반영한다'
        if AUTO and 0 < (d - _dt.date.fromisoformat(C.CUR)).days <= 80 and C.CUR in rev:   # 자동 카드: 이번 분기 실적이면 SEC 숫자로
            _eps = _ac.json.load(open(os.path.join(os.path.dirname(os.path.dirname(HERE)), 'scripts', f'{T}_eps_history.json')))
            _e = {x['quarter_end']: x['quarter_eps'] for x in _eps}
            _rc = _ac.chg(rev[C.CUR], rev.get(C.YO))
            _body = (f'{C.QLABEL} 매출 {_ac.B(rev[C.CUR])}' + (f'({_rc})' if _rc else '') + ', GAAP 영업이익 ' + _ac.B(op[C.CUR])
                     + (f', GAAP 희석 EPS {_ac.money(_e[C.CUR])}(1년 전 {_ac.money(_e[C.YO])})' if C.CUR in _e and C.YO in _e else '')
                     + (' · SEC 10-K 기준' if C.TENQ_NAME.endswith('10-K') else ' · SEC 10-Q 기준'))   # 실제 문서만(Fable)
        _new.append(('neutral', f'{_when} — 실적 발표', rx, _body, e["url"], f'{C.CO} 실적 보도자료 (SEC 8-K)'))
    items = _new + items
    if _new:
        _end = max(e["date"] for e in _auto if e["filed"] <= _last)[:7].replace("-", ".")   # 반응일이 아직 없어도(마지막 날 장 마감 후) 발표 달로
        if _end and _end > C.NEWS_RANGE.split("~")[-1].strip():
            C.NEWS_RANGE = C.NEWS_RANGE.split("~")[0].strip() + " ~ " + _end
for it in items:
    assert it[2] is None or it[2] in days, it[2]
tl = '    <div class="timeline" id="newsTimeline">\n' + '\n'.join(item(*i) for i in items) + '\n    </div>'
sub(r'    <div class="timeline" id="newsTimeline">\n.*?\n    </div>\n    <div class="tl-pager"', tl + '\n    <div class="tl-pager"')
sub(r'<div class="section-title">시계열 주요 뉴스 \([^)]*\)</div>', f'<div class="section-title">시계열 주요 뉴스 ({C.NEWS_RANGE})</div>')
# 숫자 목록이 비면 목록 칸을 통째로 뺀다 — 자동 카드는 목록 없이 머리말·위험·다음 확인만(2026-10-10 사용자 결정)
SUMMARY = (f'<div class="verdict-summary-head">지배적 내러티브 · {F(C.SUMMARY[0])}<span class="tag">{C.SUMMARY[1]}</span></div>\n'
           + (('    <ol class="news-list">\n' + '\n'.join(f'      <li>{F(x)}</li>' for x in C.SUMMARY[2]) + '\n    </ol>\n') if C.SUMMARY[2] else '')
           + f'    <div class="verdict-summary-counter">⚠️ {F(C.SUMMARY[3])}</div>\n    <div class="verdict-summary-next">🔍 다음 확인 포인트 · {F(C.SUMMARY[4])}</div>')
sub(r'<div class="verdict-summary-head">지배적 내러티브.*?<div class="verdict-summary-next">.*?</div>', SUMMARY)
row = lambda k, head, tx: f'<div class="bb-row {k}"><span class="bb-icon">{"▲" if k == "bull" else "▼"}</span><span class="bb-head">{head}</span><span class="bb-text">{tx}</span></div>'
bull = [(a, F(x)) for a, x in C.BULL]; bear = [(a, F(x)) for a, x in C.BEAR]
m = re.search(r'(<div class="bb-title bb-bull">🐂 Bull 요인</div>\n)(.*?)(\n    </div>\n    <div class="bb-box">\n      <div class="bb-title bb-bear">🐻 Bear 요인</div>\n)(.*?)(\n    </div>\n  </div>)', h, re.S)
h = h[:m.start()] + m.group(1) + '\n'.join('      ' + row('bull', *b_) for b_ in bull) + m.group(3) + '\n'.join('      ' + row('bear', *b_) for b_ in bear) + m.group(5) + h[m.end():]
A_ = C.ANALYST
# 애널리스트 인원: 의견 인원 · 목표가 인원(통계 표본)을 나눠 적는다(D48, 2026-10-05) — 주석은 줄 밖에(같은 줄 뒤 문장이 있다)
h = h.replace("put('n', A.n);", "put('n', A.n + (A.nTargets != null && A.nTargets !== A.n ? `명 · 목표가 ${A.nTargets}` : ''));", 1)   # 틀(NVDA) 표시 줄
sub(rf"const {T}_ANALYST = \{{[^}}]*\}};", f"const {T}_ANALYST = {{ asOf: '{getattr(C, 'ANALYST_ASOF', '2026-10-01')}', source: 'StockAnalysis (의견 집계 · 개별 목표가)', rating: '{A_['rating']}', n: {A_['n']}, nTargets: {A_.get('nt', 'null')}, mean: {A_['mean']}, median: {A_['median']},\n  low: {A_['low']}, high: {A_['high']}, strongBuy: {A_['sb']}, buy: {A_['b']}, hold: {A_['h']}, sell: {A_['s']}, strongSell: {A_['ss']} }};")
assert A_['n'] == A_['sb'] + A_['b'] + A_['h'] + A_['s'] + A_['ss']
sub(r'<span class="op-val">11월 중순 <span class="op-sub">Q3 FY27 예상</span></span>', f'<span class="op-val">{C.NEXT_OP[0]} <span class="op-sub">{C.NEXT_OP[1]}</span></span>')
_vc = {'저평가': 'var(--green)', '적정~저평가': 'var(--green)', '적정': 'var(--gold)', '적정~고평가': 'var(--gold)', '고평가': 'var(--red)', '판정 보류': 'var(--gold)'}[VERDICT]
h = h.replace('data-verdict style="font-size:22px;color:var(--gold);">적정~저평가</span>', f'data-verdict style="font-size:22px;color:{_vc};">{VERDICT}</span>', 1)
one('<span class="vs-verdict" data-verdict>적정~저평가</span>', f'<span class="vs-verdict" data-verdict>{VERDICT}</span>')
if getattr(C, 'ACT_REASON', None):   # 활동성 미판정 사유(카드 한정)
    h = h.replace('"status": "N/A", "reason": "5년 비교 이력 부족"}', f'"status": "N/A", "reason": "{C.ACT_REASON}"}}', 1)
    h = h.replace('종합 진단: 판정하지 않음 — 5년 비교 이력 부족', f'종합 진단: 판정하지 않음 — {C.ACT_REASON}', 1)
# 상세 토글 색: 진단 요약 색을 따른다(사용자 요청 2026-10-01)
one("  .detail-toggle.collapsed .chevron { transform: rotate(-90deg); }\n",
    "  .detail-toggle.collapsed .chevron { transform: rotate(-90deg); }\n"
    "  .diag-summary + .detail-toggle .toggle-hint { background: rgba(46,204,113,0.12); border-color: rgba(46,204,113,0.35); }\n"
    "  .diag-summary + .detail-toggle:hover .toggle-hint { background: rgba(46,204,113,0.22); border-color: rgba(46,204,113,0.5); }\n"
    "  .diag-summary + .detail-toggle .toggle-hint-text, .diag-summary + .detail-toggle .chevron { color: var(--green); }\n"
    "  .diag-summary.watch + .detail-toggle .toggle-hint { background: rgba(240,192,64,0.12); border-color: rgba(240,192,64,0.35); }\n"
    "  .diag-summary.watch + .detail-toggle:hover .toggle-hint { background: rgba(240,192,64,0.22); border-color: rgba(240,192,64,0.5); }\n"
    "  .diag-summary.watch + .detail-toggle .toggle-hint-text, .diag-summary.watch + .detail-toggle .chevron { color: var(--gold); }\n"
    "  .diag-summary.alert + .detail-toggle .toggle-hint { background: rgba(231,76,60,0.12); border-color: rgba(231,76,60,0.35); }\n"
    "  .diag-summary.alert + .detail-toggle:hover .toggle-hint { background: rgba(231,76,60,0.22); border-color: rgba(231,76,60,0.5); }\n"
    "  .diag-summary.alert + .detail-toggle .toggle-hint-text, .diag-summary.alert + .detail-toggle .chevron { color: var(--red); }\n"
    "  .diag-summary.none + .detail-toggle .toggle-hint { background: var(--bg3); border-color: var(--border); }\n"
    "  .diag-summary.none + .detail-toggle .toggle-hint-text, .diag-summary.none + .detail-toggle .chevron { color: var(--text2); }\n")
# 성장·마진 모두 해 없음(요구 영업이익률 100%로도 불가) — CRWD에서 쓴 카드 한정 패치를 공통으로(MRVL Fable)
# 해가 있든 없든 margin 모드면 바꾼다 — 아래 문구는 화면에서 해 유무를 다시 가르므로 해가 있는 카드의 표시는 같다.
# 주가에 따라 해가 생겼다 없어졌다 하면 카드 설정(INTC)이 기대하는 문구가 사라져 재빌드가 멈췄다(2026-10-08 종가, Actions)
if DCF.get('reqMode') == 'margin':
    one("                           : mMode ? (d.requiredMargin != null ? f1(d.requiredMargin) : '—')",
        "                           : mMode ? (d.requiredMargin != null ? f1(d.requiredMargin) : '100%로도 불가')   // 해 없음(카드 한정)")
    one("    if (lb) lb.textContent = noSol ? '현재가 요구 성장 (마진 100%로도 불가)' : `현재가 요구 영업이익률 (최근 4분기 ${f1(d.marginNow)})`;",
        "    if (lb) lb.textContent = noSol ? '현재가 요구 성장 (마진 100%로도 불가)' : d.requiredMargin == null ? '현재가 요구 영업이익률' : `현재가 요구 영업이익률 (최근 4분기 ${f1(d.marginNow)})`;")
    one("          + ` 영업이익률이 ${d.requiredMargin != null ? f1(d.requiredMargin) : '(범위 밖)'}여야 한다(현재 ${f1(d.marginNow)}).`",
        "          + (d.requiredMargin != null ? ` 영업이익률이 ${f1(d.requiredMargin)}여야 한다(현재 ${f1(d.marginNow)}).` : ` 영업이익률을 100%로 올려도 모자란다(현재 ${f1(d.marginNow)}).`)")
    one("      + ` 영업이익률이 <b>${D.requiredMargin != null ? pc(D.requiredMargin) : '범위 밖'}</b>여야 한다(지금 ${pc(D.marginNow)}).`",
        "      + (D.requiredMargin != null ? ` 영업이익률이 <b>${pc(D.requiredMargin)}</b>여야 한다(지금 ${pc(D.marginNow)}).` : ` 영업이익률을 <b>100%</b>로 올려도 모자란다(지금 ${pc(D.marginNow)}).`)")
# 동종업 배수 개수(PER·EV/EBITDA가 빠진 카드)
_np = len(VAL['peer']['metrics'])
if _np < 5:
    _miss = [x for x in ('PER', 'PBR', 'PSR', 'PCR', 'EV/EBITDA') if x.lower().replace('/', '') not in {m['metric'] for m in VAL['peer']['metrics']}]
    h = h.replace('뒤집어 점수로 썼고 다섯 개를 평균했다.', f'뒤집어 점수로 썼고 {"·".join(_miss)}를 뺀 {_np}개를 평균했다.', 1)
# 배수 이력 배지: "최근 N년 이력"은 이력이 끊긴 경우(적자·자본 음수 구간 제외, STX PER·PBR)에 틀린다 → "유효 이력"(Fable, 2026-10-01)
h = h.replace("`최근 ${(m.days / 252).toFixed(1)}년 이력`", "`유효 이력 ${(m.days / 252).toFixed(1)}년(적자·결측 구간 제외)`")
# 분모 음수 배지: PBR의 분모는 자본이라 "적자"가 아니라 "자본 음수"(BKNG 흑자·자본 −$10.8B, Codex 2026-10-02)
h = h.replace("f('badge').textContent = neg ? '적자 · 0점'", "f('badge').textContent = neg ? (m.metric === 'pbr' ? '자본 음수 · 0점' : '적자 · 0점')")
_pbr_gap = '자본 음수·결측' if getattr(C, 'PBR_GAP_NEG_EQUITY', True) else '결측'   # 자본이 음수였던 적이 없는 종목(SEC 자본 확인 — APH·DHR·MRVL·T·WDC)은 PBR 공백이 결측뿐(Fable 2026-10-05)
h = h.replace("`유효 이력 ${(m.days / 252).toFixed(1)}년(적자·결측 구간 제외)`", "`유효 이력 ${(m.days / 252).toFixed(1)}년(${m.metric === 'pbr' ? '" + _pbr_gap + "' : '적자·결측'} 구간 제외)`")
# 활동성 — 분기 매입채무가 없는 카드(DPO·CCC null): ABBV 카드 한정 패치를 공통으로(PEP에서 null.toFixed로 스크립트 전체가 멈췄다, Codex·Fable 2026-10-01)
_ACT = re.search(rf'^const {T}_ACTIVITY = (\{{.*?\}});', h, re.M)
if _ACT and (json.loads(_ACT.group(1)).get('now') or {}).get('dpo', 0) is None:
    one("  const d1 = v => v.toFixed(1);\n  const cmp = k => {", "  const d1 = v => v == null ? '—' : v.toFixed(1);   // 분기 매입채무 미공시면 dpo·ccc가 null\n  const cmp = k => {")
    one("document.querySelectorAll('[data-act-days]').forEach(el => { el.textContent = d1(A.now[el.dataset.actDays]) + '일'; });",
        "document.querySelectorAll('[data-act-days]').forEach(el => { const v = A.now[el.dataset.actDays]; el.textContent = v == null ? '해당 없음' : d1(v) + '일'; });")
    one("const k = el.dataset.actSub; el.textContent = LEAD[k](d1(A.now[k])) + ' · ' + cmp(k);",
        "const k = el.dataset.actSub;\n    // 분기 매입채무를 따로 공시하지 않는 회사는 지급기간을 계산하지 않는다.\n    el.textContent = A.now[k] == null ? '분기 매입채무를 따로 공시하지 않아 계산하지 않는다' : LEAD[k](d1(A.now[k])) + ' · ' + cmp(k);")
    one("const ex = $('actCccExplain'), cccDiff = A.now.ccc - A.prev.ccc;",
        "const ex = $('actCccExplain'), cccDiff = A.now.ccc - A.prev.ccc;\n  const noAp = A.now.dpo == null;")
    one("  if (ex) ex.innerHTML = lead\n",
        "  if (ex && noAp) {\n    const opDiff = A.now.op - A.prev.op;\n    ex.innerHTML = `재고를 사서 판매 대금을 회수하기까지 ${d1(A.now.op)}일이 걸린다(재고 ${d1(A.now.dio)}일 + 매출채권 ${d1(A.now.dso)}일). `\n      + `분기 매입채무를 따로 공시하지 않아 외상으로 버티는 기간과 현금창출주기는 계산하지 않았다. `\n      + (Math.abs(opDiff) < 0.05 ? '직전 분기와 같다.' : `직전 분기 ${d1(A.prev.op)}일보다 ${d1(Math.abs(opDiff))}일 ${opDiff > 0 ? '길어졌다' : '짧아졌다'}.`);\n  } else if (ex) ex.innerHTML = lead\n")
    one("    const span = Math.max(A.now.op, A.now.dpo);",
        "    const span = noAp ? A.now.op : Math.max(A.now.op, A.now.dpo);\n    if (noAp) bar.querySelectorAll('.tl-marker, .tl-marker-label, .tl-ccc-span').forEach(el => { el.style.display = 'none'; });")
    one("    bar.querySelectorAll('.tl-marker, .tl-marker-label').forEach(el => { el.style.left = pct(A.now.dpo); });",
        "    if (!noAp) bar.querySelectorAll('.tl-marker, .tl-marker-label').forEach(el => { el.style.left = pct(A.now.dpo); });")
    one("    ml.textContent = `매입채무 지급 ${d1(A.now.dpo)}일`;", "    if (!noAp) ml.textContent = `매입채무 지급 ${d1(A.now.dpo)}일`;")
    one("    cs.style.left = pct(Math.min(A.now.dpo, A.now.op)); cs.style.width = pct(Math.abs(A.now.ccc));",
        "    if (!noAp) { cs.style.left = pct(Math.min(A.now.dpo, A.now.op)); cs.style.width = pct(Math.abs(A.now.ccc)); }")
    one("    if (A.now.ccc < 0) {", "    if (!noAp && A.now.ccc < 0) {")
    one("    } else if (fl) { fl.remove(); cs.style.display = ''; }", "    } else if (fl) { fl.remove(); if (!noAp) cs.style.display = ''; }")
# DCF 추적 툴팁: "낙관이 가장 낮다"는 낙관이 보수·기본 모두보다 낮을 때만(QCOM 2024-11·2025-02는 기본이 최저, Codex 2026-10-01)
h = h.replace("+ (e.v.high < e.v.low ? '\\n⚠ 이 시점엔 낙관이 가장 낮다.", "+ (e.v.high < e.v.low && e.v.high < e.v.base ? '\\n⚠ 이 시점엔 낙관이 가장 낮다.")
# DCF 추적 툴팁: 낙관이 가장 낮은 이유를 "빨리 클수록 가치가 준다"(AVGO, ROIC < 할인율)로 단정하던 템플릿 문구를 중립으로 —
# QCOM은 ROIC 26%라 그 설명이 틀렸다(Fable, 2026-10-01). 투하자본 수익률이 할인율보다 낮을 때만 뒷부분을 붙인다.
_tt_old = '현재 영업이익률이 과거보다 낮아, 그 마진으로 빨리 클수록 재투자가 이익을 넘어 가치가 줄어든다.'
if _tt_old in h:
    _roic = (DCF.get('hardDetail') or {}).get('roic')
    h = h.replace(_tt_old, '현재 영업이익률이 과거보다 낮아, 그 마진을 이어 가는 낙관이 작게 나온다.' + (' 투하자본 수익률이 할인율보다 낮아 빨리 클수록 가치가 더 줄어든다.' if _roic is not None and _roic < 0.10 else ''))
# 요구 성장률 배수: 틀은 "3배를 넘는다"로 고정 — 틀 시절 카드(KO·ABBV·CAT·COST·JNJ·MRK·XOM)는 실제 배수를 적었다(cfg REQ_MULT_EXACT, 2026-10-05)
if getattr(C, 'REQ_MULT_EXACT', False):
    one("가 필요해 지난 5년의 3배를 넘는다.`", "가 필요해 지난 5년의 ${Math.round(d.requiredGrowth / d.growth5y)}배다.`")
    one("가 필요해 지난 5년 실제의 3배를 넘는다.`", "가 필요해 지난 5년 실제의 ${Math.round(D.requiredGrowth / D.growth5y)}배다.`")
# 현금흐름 칸 쏠림 메모(A0, 86af3f2)는 비금융 카드에만 — 근거 패널에 금융이 없다. GICS Financials면 뺀다(cfg NO_DCF_SKEW는 예전 표시, 남겨 둬도 같음)
_SECT = json.load(open('sectors.json')).get(T)   # GICS 섹터(v2/sectors.json)
if getattr(C, 'NO_DCF_SKEW', False) or 'Financ' in json.dumps(_SECT or ''):   # 금융 섹터는 섹터로 정한다(v2.1 B-3, 2026-10-05 — MA·V에 남아 있었다)
    sub(r'// 이 칸이 대부분 종목에서 "매우 비싸다"라는 사실을 툴팁으로 알린다\.[^\n]*\n// 금융 카드에는 넣지 않는다[^\n]*\nconst DCF_SKEW_NOTE = [^\n]*\n', '')
    one("      + (lv.ratio != null ? '\\n' + DCF_SKEW_NOTE : '')\n", '')
# 해 없음 카드 모델 범위 툴팁(v2.1 B-4, 2026-10-05) — 라벨 줄 뒤에, 해 없음일 때만 실행
_LB = "    if (lb) lb.textContent = noSol ? '현재가 요구 성장 (마진 100%로도 불가)' : d.requiredMargin == null ? '현재가 요구 영업이익률' : `현재가 요구 영업이익률 (최근 4분기 ${f1(d.marginNow)})`;"
if _LB in h and 'v2.1 B-4' not in h:
    h = h.replace(_LB, _LB + "\n    if (d.requiredMargin == null) {   // 해 없음: 모델 범위를 툴팁에(v2.1 B-4, 2026-10-05)\n"
        + f"      const _ps = {json.dumps((SM.get('PSR') or {}).get('current'))};   // 생성 때 PSR(이 줄 위에서 {T}_VALUATION을 부르면 선언 전 접근으로 스크립트가 멈춘다)\n"
        + "      req.title = '영업이익률을 100%로 올려도 이 모델(할인율 10%·영구성장 2.5%, 지난 성장 경로에서 식는 5년)로는 현재가에 닿지 않는다'\n"
        + "        + (_ps ? (_ps > 10 ? ` — 현재가는 매출의 ${_ps.toFixed(1)}배(PSR)로, 모델 상한(세후 이익률 100% ÷ (할인율 − 영구성장) ≈ 매출의 10배)을 넘는 성장·마진 기대가 들어 있다.` : ` — 현재가는 매출의 ${_ps.toFixed(1)}배(PSR)로 모델 상한(≈ 매출의 10배)보다 낮다. 해가 없는 것은 순부채·재투자 가정이 사업 가치를 깎기 때문이다.`) : '.');\n    }", 1)
if AUTO:   # 자동 카드의 종목별 패치는 표기 고침뿐이다 — 찾는 글이 없으면(데이터·분기에 따라 문구가 바뀌면) 건너뛰고 기록만, 카드를 멈추지 않는다(2026-10-10)
    _one_hard, _sub_hard = one, sub
    def one(o, n):
        if h.count(o) == 1:
            _one_hard(o, n)
        else:
            print(f'  POST 건너뜀(글 {h.count(o)}곳): {o[:60]!r}')
    def sub(pat, new, flags=re.S):
        if len(re.findall(pat, h, flags)) == 1:
            _sub_hard(pat, new, flags)
        else:
            print(f'  POST 건너뜀(패턴): {pat[:60]!r}')
try:
    for _code in getattr(C, 'POST', []):   # 종목별 추가 패치
        try:
            exec(_code, globals())
        except Exception as _e:   # 자동 카드: 표기 고침 덩어리의 어떤 오류든(MA requiredGrowth 없음 → pct(None)) 그 덩어리만 건너뛴다(Codex)
            if not AUTO:
                raise
            print(f'  POST 덩어리 건너뜀: {type(_e).__name__} {str(_e)[:80]}')
finally:
    if AUTO:
        one, sub = _one_hard, _sub_hard
# 숨긴 '추세 구조' 칸: 틀(NVDA)·옛 카드의 52주 저·고점 숫자가 정적 글자로 남지 않게 중립 문장으로(안건 E7·D55, 2026-10-05) — POST의 옛 문장 복원보다 뒤에
h = re.sub(r'(<div class="card" hidden>\n    <div class="card-title">추세 구조</div>\n    <div style="font-size:12\.5px;color:var\(--text2\);line-height:1\.7;">)(.*?)(\n    </div>\n  </div>)',
           lambda m: m.group(1) + '\n      기술적 분석(추세 상태)은 이 사이트의 판단(내재가치 대비)에서 뺐다. 이 칸은 화면에 보이지 않는다.' + m.group(3), h, count=1, flags=re.S)
# 성장 모드 역산 문장: 위에서 .reverse를 '—'로 비우는데 카드 JS는 마진 모드일 때만 문장을 다시 쓴다 — 성장 모드 카드는 '—'만 남았다
# (ACN·APH·BKNG 등, 틀 통일 변환에서 발견, 2026-10-05). cfg REVERSE가 있으면 그 문장, 없으면 틀 시절 카드의 표준 문장(칸은 JS가 갱신).
if '<div class="reverse">—</div>' in h and DCF.get('reqMode') == 'growth' and DCF.get('requiredGrowth') is not None:
    _rev = F(C.REVERSE) if getattr(C, 'REVERSE', None) else (f'지금 가격(<span data-dcf-price>${px:.2f}</span>)이 정당하려면 5년간 매출이 매년 <b data-dcf-req>{pct(DCF["requiredGrowth"])}</b>씩 커야 한다. '
        + f'기본 시나리오(<span data-dcf-basev>${(f'{DCF["base"]:.2f}' if abs(DCF["base"]) < 10 else f'{DCF["base"]:.0f}')}</span>)를 같은 방식으로 환산하면 연 <span data-dcf-baseeq>{pct(DCF["baseEquivGrowth"])}</span>다.')
    one('<div class="reverse">—</div>', '<div class="reverse">' + _rev + '</div>')
open(p, 'w', encoding='utf-8').write(h)
if _refresh:
    _cp = os.path.join(HERE, 'cfg', f'cfg_{t}.py'); _cs = open(_cp, encoding='utf-8').read()
    _cs, _k = re.subn(r'^VOTES, VERDICT = .*$', f'VOTES, VERDICT = {VOTES}, {VERDICT!r}', _cs, count=1, flags=re.M)
    assert _k == 1, 'cfg에 VOTES, VERDICT 한 줄이 없다'
    open(_cp, 'w', encoding='utf-8').write(_cs)
    with open(os.path.join(HERE, 'refresh_changes.jsonl'), 'a', encoding='utf-8') as _f:
        _f.write(json.dumps(_refresh, ensure_ascii=False) + '\n')
print('ok', T, VERDICT, VOTES, 'self', selfsc, 'peer', peersc, 'ratio', round(ratio, 2) if ratio else None, 'YoY', vec(cur), yd, 'QoQ', qd, 'opm', opm, 'ch', round(ch, 1))
print('peers', {k: v for k, v in peers.items()}, 'miss', miss)
