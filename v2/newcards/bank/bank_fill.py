"""은행 카드 공통 채우기 — 사전 등록 7판(research/bank_rim_prereg.md 11절, 2026-10-11). 분기마다 손으로 고치는 값이 없다.

은행 9장은 종목별 채우기 스크립트({t}_fill.py)로 만들었고, 보도자료에서 옮긴 숫자(사업부 순이익·자본비율·대손 내역·자본배분·뉴스)와
문장이 분기마다 손으로 들어갔다. 이 스크립트는 SEC 자료(companyfacts + 원문 인라인 XBRL, adapters/bank_sec_values.py)와 규칙 문장만 쓴다.
  - 분기: v2/{T}_bank.json(adapters/bank_card.py, 7판)의 RIM 기준 분기 — 관문을 통과한 최신 분기
  - 분기 차트·YoY/QoQ: 순영업수익 · 충당금 전 이익(순영업수익 − 비이자비용) · 보통주 귀속 순이익 · 순이자이익(9곳 모두 태그가 있다 — 대손비용은 4곳이 없어 뺐다)
  - 매출 구성 도넛: 순이자이익 · 그 밖의 순영업수익(사업부 순이익은 보도자료에만 있다)
  - 자본 칸: CET1 비율은 원문 태그가 있을 때만, BVPS·TBVPS는 우리 정의(11-7)
  - 자본배분·체크포인트·종합 해석·강세/약세·위험 문장: 규칙(원인은 쓰지 않는다 — 일반 자동 카드와 같은 원칙)
  - 뉴스: 실적 보도자료 8-K(news_auto.json) — 날짜·제목·링크, 이번 분기면 SEC 숫자
기반 HTML(base/{t}_base.html — 틀 복제 + 배열) 뒤에 실행. 은행 공통 화면 규칙은 이어서 unify_js.py가 넣는다.

    python3 v2/newcards/bank/bank_fill.py JPM
"""
import datetime as dt
import importlib.util
import json
import os
import re
import statistics
import sys

V2 = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(V2)
sys.path.insert(0, '.'); sys.path.insert(0, 'adapters'); sys.path.insert(0, 'newcards')
import build_multiple_history as bmh  # noqa: E402
import bank_rim as br  # noqa: E402
import auto_card as ac  # noqa: E402
import news_auto as na  # noqa: E402

T = sys.argv[1].upper(); t = T.lower()
_sp = importlib.util.spec_from_file_location('bcfg', os.path.join(V2, 'newcards', 'bank', 'cfg', f'cfg_{t}.py'))
K = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(K)
CIK = K.CIK
p = f'{T}_full_widget.html'; h = open(p, encoding='utf-8').read()


def one(o, n):
    global h
    c = h.count(o); assert c == 1, (c, o[:100]); h = h.replace(o, n)


def sub(pat, new, flags=re.S):
    global h
    m = list(re.finditer(pat, h, flags)); assert len(m) == 1, (len(m), pat[:90])
    h = h[:m[0].start()] + (new(m[0]) if callable(new) else new) + h[m[0].end():]


J = json.load(open(f'{T}_bank.json'))
assert J.get('edition', 6) >= 7, f'{T}_bank.json은 7판이 아니다 — BANK_EDITION=7로 bank_card.py를 돌릴 것'
R = J['rim']; SH = J['self']; PEER = J['peer']; FB = SH.get('fairBand') or {}
D = json.loads(re.search(rf'const {T}_DAILY\s*=\s*(\[.*?\]);', h, re.S).group(1)); days = {r[0] for r in D}
px, asof = D[-1][4], D[-1][0]
assert abs(px - J['price']) < 1e-6 and asof == J['asOf'], (px, J['price'], asof, J['asOf'])
cut = (R.get('frozen') or {}).get('asof_cut')
bank = br.Bank(T, CIK, cut or asof, edition=7)   # 카드 판정 JSON과 같은 7판(Fable — 기본값이 6이던 때 4장이 섞였다)
L = R.get('L') or max(e for e in bank.se if bank.se[e][1] <= (cut or asof))   # 재무 기준 분기(관문을 통과한 최신 분기)
S_, CE = (R.get('shares'), R.get('ce')) if R.get('L') else ((bank.shares(L) or (None,))[0], (bank.ce(L) or (None,))[0])
f1 = lambda v: f'{v * 100:.1f}%'
B = lambda v: ('−' if v < 0 else '') + (f'${abs(v) / 1e9:.1f}B' if abs(v) >= 1e9 else f'${abs(v) / 1e6:,.0f}M')
r1 = lambda v: round(v / 1e9, 1)
qd_ = lambda e: f'{e[:4]}.{e[5:7]}.{e[8:]}'


def q(tags):
    _, rows = bmh.pick_tag(CIK, tags)
    rows = [x for x in rows if x['filed'] <= (cut or asof)]
    # 표시용 흐름은 같은 기간의 가장 나중 공시 값(재표시 기준)으로 — 1년 전 분기를 처음 공시 값으로 두면 BAC 증감률이 기준이 섞였다(Fable)
    _lat = {}
    for x in rows:
        k_ = (x.get('start'), x['end'])
        if k_ not in _lat or x['filed'] > _lat[k_]['filed']:
            _lat[k_] = x
    rows = sorted(_lat.values(), key=lambda x: (x['end'], x['filed']))
    return {e['end']: e['val'] for e in bmh.quarterly_flow(rows, T)}


# REV_TAG가 튜플이면 구성 태그의 합 — 총수익을 한 태그로 분기 공시하지 않는 은행(BNY: 비이자수익 + 순이자수익, 2026-10-17)
_sum_q = lambda tags: (lambda ds: {k: sum(d_[k] for d_ in ds) for k in set.intersection(*(set(d_) for d_ in ds))})([q([t_]) for t_ in tags])
rev = _sum_q(K.REV_TAG) if isinstance(K.REV_TAG, tuple) else q([K.REV_TAG]); ni = q(['NetIncomeLossAvailableToCommonStockholdersBasic'])
nie = q(['NoninterestExpense']); nii = q(['InterestIncomeExpenseNet'])
ks = sorted(k for k in rev if k <= L and k in ni and k in nie and k in nii)[-8:]
assert ks[-1] == L, (ks[-1], L)
cur, qo = ks[-1], ks[-2]
yo = [k for k in ks if 350 <= (dt.date.fromisoformat(cur) - dt.date.fromisoformat(k)).days <= 380][-1]
qlab = lambda e: f'Q{(int(e[5:7]) - 1) // 3 + 1} {e[:4]}'
L8 = [qlab(k) for k in ks]; QL, YL, QQL = qlab(cur), qlab(yo), qlab(qo)
roe_q = [round(bank.roe(k)[0] * 100, 1) if bank.roe(k) else None for k in ks]
filed = bank.se[L][1]
secv = br.SEC_VALUES.get(T, {}).get(L, {})
chg = lambda a, b_: None if b_ is None or a is None or b_ <= 0 else (a / b_ - 1)
pc = lambda x: f'{x * 100:+.1f}%'.replace('-', '−') if x is not None else '—'

# 실적 보도자료(8-K 2.02)와 다음 실적일 — 일반 자동 카드와 같은 규칙(작년 같은 분기 보도자료 + 364일, "예상")
_sub = ac._submissions(CIK)
_rel = [(_sub['filingDate'][i], _sub['accessionNumber'][i], _sub['primaryDocument'][i]) for i, f_ in enumerate(_sub['form'])
        if f_ == '8-K' and '2.02' in _sub['items'][i].split(',')]


def _is_res(x):
    pth = os.path.join(ac.SUBS, f'exhibit_{x[1]}.json')
    if os.path.exists(pth) and 'head' in json.load(open(pth)):
        _hd = json.load(open(pth))['head']
        return bool(na.RESULTS.search(_hd[:400]) or na.BANK_RESULTS.search(_hd[:600]))
    try:
        u, hd = na.exhibit(CIK, x[1], x[2])
    except Exception:
        return True
    json.dump({'url': u, 'head': hd[:400]}, open(pth, 'w'))
    return bool(na.RESULTS.search(hd[:400]) or na.BANK_RESULTS.search(hd[:600]))


def first_rel(after, within=80):
    c_ = sorted(x for x in _rel if 0 < (dt.date.fromisoformat(x[0]) - dt.date.fromisoformat(after)).days <= within)
    # 실적으로 읽히는 첫 2.02항, 없으면 첫 2.02항 — 은행 2.02항은 거의 실적 발표다(AXP 2025-10-17 첫머리가 실적 낱말 없이 시작)
    return next((x for x in c_ if _is_res(x)), c_[0] if c_ else None)


def rel_url(x):
    pth = os.path.join(ac.SUBS, f'exhibit_{x[1]}.json')
    if os.path.exists(pth) and json.load(open(pth)).get('url'):
        return json.load(open(pth))['url']
    u, hd = na.exhibit(CIK, x[1], x[2])
    json.dump({'url': u, 'head': hd[:400]}, open(pth, 'w'))
    return u


_cr = first_rel(cur)
PRU = rel_url(_cr) if _cr else f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={CIK}&type=10-Q'
_ya_next = [k for k in sorted(rev) if 250 <= (dt.date.fromisoformat(cur) - dt.date.fromisoformat(k)).days <= 300]   # 1년 전 같은 분기의 다음 분기(그 실적 발표 + 364일)
_ago = first_rel(_ya_next[0]) if _ya_next else None
_nl = qlab((dt.date.fromisoformat(cur) + dt.timedelta(days=91)).isoformat()[:8] + '28')
if _ago:
    _est = dt.date.fromisoformat(_ago[0]) + dt.timedelta(days=364); _a = dt.date.fromisoformat(_ago[0])
    NEXT = (f'{_est.month}월 {_est.day}일 무렵 예상', f'일정 · {_nl} (작년 {_a.month}/{_a.day} 공시, 같은 요일로 추정)')
    NEXT_OP = (f'{_est.month}월 {_est.day}일 무렵', f'{_nl} 예상'); CHECK_WHEN = f'{_est.year}년 {_est.month}월 {_est.day}일 무렵 (예상) · {_nl}'
elif _cr:   # 작년 보도자료가 SEC 최근 공시 목록 밖이면(JPM·GS·MS — 구조화 채권 공시가 많아 목록이 몇 달치) 이번 분기 보도자료 + 91일(같은 요일)
    _est = dt.date.fromisoformat(_cr[0]) + dt.timedelta(days=91); _a = dt.date.fromisoformat(_cr[0])
    NEXT = (f'{_est.month}월 {_est.day}일 무렵 예상', f'일정 · {_nl} ({QL} 발표 {_a.month}/{_a.day} + 13주로 추정)')
    NEXT_OP = (f'{_est.month}월 {_est.day}일 무렵', f'{_nl} 예상'); CHECK_WHEN = f'{_est.year}년 {_est.month}월 {_est.day}일 무렵 (예상) · {_nl}'
else:
    NEXT, NEXT_OP, CHECK_WHEN = ('미정', f'일정 · {_nl}'), ('미정', _nl), _nl
CHECK_TAIL = ' 실적 공시.'
# 다음 분기 실적 보도자료가 카드 날짜까지 이미 나왔으면(은행은 10-Q보다 2~3주 먼저) '예상'이 아니라 '발표됨'으로 — 재무·RIM은 아직 이번 10-Q 기준(BNY 10/15, Codex 2026-10-17)
_ny, _nm = int(cur[:4]) + (int(cur[5:7]) + 3 > 12), (int(cur[5:7]) + 3 - 1) % 12 + 1
_nq_end = f'{_ny}-{_nm:02d}-{ {3: 31, 6: 30, 9: 30, 12: 31}[_nm] }'
_nr = first_rel(_nq_end)
if _nr and _nr[0] <= asof:
    _d = dt.date.fromisoformat(_nr[0])
    _rq, _rn = ('10-K' if cur.endswith('12-31') else '10-Q'), ('10-K' if _nq_end.endswith('12-31') else '10-Q')   # 4분기는 10-K(Codex 2차)
    NEXT = (f'{_d.month}월 {_d.day}일 발표됨', f'{_nl} 실적 · 재무·내재가치는 {QL} {_rq} 기준({_nl} {_rn} 반영 전)')
    NEXT_OP = (f'{_d.month}월 {_d.day}일 발표됨', f'{_nl} {_rn} 반영 전')
    CHECK_WHEN = f'{_nl} {_rn}(실적은 {_d.month}월 {_d.day}일 발표됨)'
    CHECK_TAIL = ' 반영.'

# ── 1. 헤더 ──
sub(r'<span class="meta-label">현재가 요구 성장 \(5년 · 실제 3년 [^)]*\)</span>',
    f'<span class="meta-label">현재가 요구 ROE (5년 · 최근 4분기 {f1(R["roe0"]) if R.get("roe0") is not None else "—"})</span>')
if FB:
    h = re.sub(rf'(id="{t}FairBand"[^>]*>)[^<]*(</span>)', lambda m: m.group(1) + f'${FB["low"]} ~ ${FB["high"]}' + m.group(2), h, count=1)
one('<button class="ma-toggle-btn ma-off" data-ma="dcf" style="color:#38bdf8;border-color:#38bdf8;">◆ DCF 시나리오</button>',
    '<button class="ma-toggle-btn ma-off" data-ma="dcf" style="color:#38bdf8;border-color:#38bdf8;" hidden>◆ DCF 시나리오</button>')

# ── 2. 내재가치(RIM) ──
RIM_OK = not R.get('abstain') and R.get('기본') is not None
dcf = {"low": round(R['보수'], 2) if RIM_OK and R.get('보수') else None, "base": round(R['기본'], 2) if RIM_OK else None,
       "high": round(R['낙관'], 2) if RIM_OK and R.get('낙관') else None, "requiredGrowth": R.get('required_roe'),
       "baseEquivGrowth": None, "reqMode": "roe", "requiredMargin": None, "marginNow": None, "roeNow": R.get('roe0'),
       "growth5y": None, "nonopPerShare": 0, "s2cFallback": False, "asOf": asof, "hard": [], "hardDetail": {}, "tvShare": None,
       "model": "rim", "retention": R.get('b'), "bvps": R.get('bvps'), "roeTarget": R.get('roe_2y_median'), "referenceOnly": False}
if not RIM_OK:
    dcf["unavailable"] = R.get('abstain') or '초과이익모형 입력 없음'
sub(rf'^const {T}_DCF = \{{.*$', f'const {T}_DCF = ' + json.dumps(dcf, ensure_ascii=False) + ';   // 초과이익모형 — adapters/bank_card.py, research/bank_rim_prereg.md 7판', re.M)
ends = {'보수': R.get('roe_5y_median'), '기본': R.get('roe_2y_median'), '낙관': R.get('roe0')}
waccs, lams = [0.08, 0.09, 0.10, 0.11, 0.12], [0.0, 0.5, 1.0]
_rv = lambda e, r, lam: (br.rim_value(CE, R['roe0'], e, R['b'], r, lam) / S_) if RIM_OK and e is not None and br.rim_value(CE, R['roe0'], e, R['b'], r, lam) else None
vals = {n: [[round(_rv(e, r, lam), 2) if _rv(e, r, lam) else None for r in waccs] for lam in lams] for n, e in ends.items()}
grid = {"waccs": waccs, "terms": lams, "default": [0.10, 0.5], "values": vals, "kind": "rim"}
sub(rf'^const {T}_DCF_GRID = (?:\{{.*|null;)$', f'const {T}_DCF_GRID = ' + json.dumps(grid, ensure_ascii=False) + ';   // 자기자본비용 × 잔존 수렴 비율(λ)', re.M)
sub(rf'const {T}_DCF_TRACK = \[.*?\];', f'const {T}_DCF_TRACK = [];')
one('<div class="section-title">내재가치 (DCF) — 현금흐름이 말하는 가격</div>\n  <div class="lede">회사가 앞으로 벌어들일 현금만으로 계산한 주당 가치다.</div>',
    '<div class="section-title">내재가치 (초과이익모형) — 자본이 버는 초과이익이 말하는 가격</div>\n  <div class="lede">은행은 현금흐름 모델 대신 장부가치에 자기자본비용(10%)을 넘는 이익의 현재가치를 더해 계산한다.</div>')
if RIM_OK:
    new = [f'ROE가 최근 4분기 {f1(R["roe0"])}에서 5년 중앙값 {f1(R["roe_5y_median"])}로 간다.' if R.get('roe_5y_median') is not None else '5년 ROE 이력이 모자라 계산하지 않는다.',
           f'ROE가 최근 4분기 {f1(R["roe0"])}에서 최근 2년 중앙값 {f1(R["roe_2y_median"])}로 간다.',
           f'ROE {f1(R["roe0"])}(GAAP, 특별 항목 미조정)가 5년 동안 이어진다.']
else:
    new = ['계산하지 않음', '계산하지 않음', '계산하지 않음']
olds = re.findall(r'<td class="story">(지난 5년 성장 속도의 절반.*?|지난 5년의 성장 속도로.*?|최근 3년의 성장 속도로.*?)</td>', h)
assert len(olds) == 3
for o, n in zip(olds, new):
    assert h.count(o) == 1; h = h.replace(o, n)
S4 = R.get('signal4')
_same = RIM_OK and vals['기본'][0][2] and vals['기본'][2][2] and round(vals['기본'][0][2]) == round(vals['기본'][2][2])
_note = ('세 값은 확률이 아니라, 과거 ROE에서 서로 다른 가정을 뽑아 계산한 결과다. 5년 뒤 ROE는 자기자본비용 쪽으로 절반 수렴한다고 본다'
         + ('. 이 카드는 기본 시나리오 끝 ROE가 자기자본비용 10% 이하라 수렴 가정이 값을 바꾸지 않는다' if _same else ' — 이 가정이 값에 가장 크게 작용한다')
         + ((f'(수렴 없음이면 기본 ${vals["기본"][0][2]:.0f}, 완전 수렴이면 ${vals["기본"][2][2]:.0f})' if round(vals["기본"][0][2]) != round(vals["기본"][2][2])
             else '') if RIM_OK and vals['기본'][0][2] and vals['기본'][2][2] else '')
         + ((f'. 유보율 {f1(R["b"])}(최근 4분기 배당·자사주 환원 뒤 남는 몫)로 장부가가 자라고' if R['b'] > 0 else '. 유보율 0%(최근 4분기에 이익보다 많이 돌려줬다)라 장부가가 자라지 않는다고 보고')
            + ', 기타포괄손익은 반영하지 않는다. 순이익은 GAAP이고 특별 항목을 조정하지 않는다.' if RIM_OK else '.')
         + (f' ⚠ 출발 ROE: {", ".join(qlab(e) for e in S4["quarters"])} 순이익이 최근 8분기 중앙값에서 40% 넘게 벗어났다 — 일회성일 수도, 실적 수준 변화일 수도 있다. 그 분기를 중앙값으로 바꾸면 ROE {f1(S4["roe_at_median"])}다.' if S4 and S4.get('roe_at_median') else '')
         + (f' 5년 중앙값 ROE({f1(R["roe_5y_median"])})가 2년 중앙값({f1(R["roe_2y_median"])})보다 높아 보수가 기본보다 높게 나온다(이름과 순서가 뒤집힘).' if RIM_OK and R.get('보수') and R['보수'] > R['기본'] else '')
         + (f' 계산하지 않음 — {dcf["unavailable"]}.' if not RIM_OK else ''))
one('<div class="note">세 값은 확률이 아니라, 과거 실적에서 서로 다른 가정을 뽑아 계산한 결과다.</div>', f'<div class="note">{_note}</div>')
sub(r'<div class="note" data-dcf-nonop>[^<]*</div>', '<div class="note" data-dcf-nonop hidden></div>')
sub(r'<div class="reverse">.*?</div>\n  </div>', ('<div class="reverse" data-rim-reverse>지금 가격이 정당하려면 5년 동안 ROE가 매년 <b data-dcf-req>—</b>여야 한다.</div>\n  </div>' if R.get('required_roe') is not None
    else '<div class="reverse" data-rim-reverse>지금 가격은 5년 ROE 0~60% 범위의 어떤 값으로도 맞출 수 없다(초과이익모형 — <b data-dcf-req>해 없음</b>).</div>\n  </div>'))
one('<div class="knob"><span class="knob-l">영구성장 <span class="knob-d" data-knob-default="term">(2.5%)</span></span>',
    '<div class="knob"><span class="knob-l">잔존 수렴 <span class="knob-d" data-knob-default="term">(절반)</span></span>')
one('<div class="knob"><span class="knob-l">할인율 <span class="knob-d" data-knob-default="wacc">(10%)</span></span>',
    '<div class="knob"><span class="knob-l">자기자본비용 <span class="knob-d" data-knob-default="wacc">(10%)</span></span>')
one("""  // 마진 모드인데 영업이익률 100%로도 닿지 않으면(해 없음) 요구 성장률을 대신 보인다(2026-09-30 사용자 결정, LRCX·PLTR).
  const noSol = mMode && d.requiredMargin == null && d.requiredGrowth != null;
  if (req) req.textContent = noSol ? '연 ' + f1(d.requiredGrowth)
""",
    """  const roeMode = d.reqMode === 'roe';   // 은행 초과이익모형 — 요구 ROE(research/bank_rim_prereg.md)
  if (req) req.textContent = roeMode ? (d.requiredGrowth != null ? 'ROE ' + f1(d.requiredGrowth) : '해 없음')
""")
one("""    if (lb) lb.textContent = noSol ? '현재가 요구 성장 (마진 100%로도 불가)' : `현재가 요구 영업이익률 (현재 ${f1(d.marginNow)})`;""",
    """    if (lb) lb.textContent = `현재가 요구 영업이익률 (현재 ${f1(d.marginNow)})`;""")
one("""    if (cell) cell.title = (mMode""",
    """    if (cell) cell.title = roeMode ? `현재가 $${price.toFixed(2)} 가 정당화되려면 5년 동안 ROE가 ${d.requiredGrowth != null ? f1(d.requiredGrowth) : '(범위 밖)'}여야 한다(최근 4분기 ${d.roeNow != null ? f1(d.roeNow) : '—'}, GAAP).`
      + `\\n현재가 ÷ 내재가치 $${Math.round(d.base)} = ${lv.ratio != null ? lv.ratio.toFixed(2) : '—'} → ${lv.label} (${DCF_RULE_TEXT})` : (mMode""")
one("""  if (box)  box.innerHTML = (d.base > 0 ? '$' + (Math.abs(d.base) < 10 ? d.base.toFixed(2) : Math.round(d.base)) : '0 이하')
    + '<span class="logic-denom"> · 보수 ' + (d.low > 0 ? '$' + (d.low < 10 ? d.low.toFixed(2) : Math.round(d.low)) : '계산 불가')
    + ' · 낙관 ' + (d.high > 0 ? '$' + (d.high < 10 ? d.high.toFixed(2) : Math.round(d.high)) : '계산 불가') + '</span>';""",
    """  const lowW = roeMode ? '보수' : '낮은 성장', highW = roeMode ? '낙관' : '높은 성장';
  if (box)  box.innerHTML = (d.base > 0 ? '$' + (Math.abs(d.base) < 10 ? d.base.toFixed(2) : Math.round(d.base)) : '0 이하')
    + '<span class="logic-denom"> · ' + lowW + ' ' + (d.low != null ? '$' + Math.round(d.low) : '—')
    + ' · ' + highW + ' ' + (d.high != null ? '$' + Math.round(d.high) : '—') + '</span>';""")
one("""  fill('[data-dcf-req]', (D.requiredGrowth * 100).toFixed(1) + '%');""",
    """  fill('[data-dcf-req]', D.requiredGrowth != null ? (D.requiredGrowth * 100).toFixed(1) + '%' : '해 없음');""")
one("""    term: G.terms.map(t => +(t * 100).toFixed(1) + '%'),""",
    """    term: G.kind === 'rim' ? G.terms.map(t => ({0: '수렴 없음', 0.5: '절반', 1: '완전'})[t]) : G.terms.map(t => +(t * 100).toFixed(1) + '%'),""")
one("""    el.textContent = '(' + +(v * 100).toFixed(1) + '%)';""",
    """    el.textContent = G.kind === 'rim' && el.dataset.knobDefault === 'term' ? '(절반)' : '(' + +(v * 100).toFixed(1) + '%)';""")

# ── 3. 점수 상수 · 기본적 분석 · 활동성 ──
_both = lambda d: round((d['ptbv']['score'] + d['per']['score']) / 2, 1) if d.get('ptbv') and d.get('per') and d['ptbv'].get('score') is not None and d['per'].get('score') is not None else None
selfscore, peerscore = _both(SH), _both(PEER)
sub(rf'const {T}_SCORES = \{{.*?\n\}};', f'''const {T}_SCORES = {{
  fundamental: null,   // 은행 — 일반 재무비율 산식이 맞지 않아 매기지 않는다
  peer: {json.dumps(peerscore)},          // S&P500 은행 대비 P/TBV·PER 순위 평균(표시용). 표는 두 배수가 같은 방향일 때만
  selfHistory: {json.dumps(selfscore)},   // P/TBV·PER 자기 5년 백분위 평균(표시용)
  asOf: "{asof}",
  fundamentalAsOf: "{L}",   // {QL} {"10-K" if L.endswith("12-31") else "10-Q"} ({filed} 공시)
}};''')
sub(r'// 기본적 분석이 98\.1이 아니라 96\.1인 이유\..*?// `--basis annual`로 돌리면 98\.1이 그대로 나온다 — 배점을 안 건드렸다는 확인이다\.\n', '')
F_ = bmh._facts(CIK)['facts']['us-gaap']


def _ann(tag):
    out = {}
    for x in F_.get(tag, {}).get('units', {}).get('USD', []):
        if x.get('form') == '10-K' and 'start' in x and x['end'].endswith('12-31') and x['filed'] <= (cut or asof) and 350 <= (dt.date.fromisoformat(x['end']) - dt.date.fromisoformat(x['start'])).days <= 380:
            if x['end'] not in out or x['filed'] < out[x['end']][1]:
                out[x['end']] = (x['val'], x['filed'])
    return {k: v[0] for k, v in out.items()}


_ra = ((lambda ds: {k: sum(d_[k] for d_ in ds) for k in set.intersection(*(set(d_) for d_ in ds))})([_ann(t_) for t_ in K.REV_TAG])
       if isinstance(K.REV_TAG, tuple) else _ann(K.REV_TAG))
_na = _ann('NetIncomeLossAvailableToCommonStockholdersBasic')
FY1 = max(k for k in _ra if k in _na); FY0 = f'{int(FY1[:4]) - 5}-12-31'
cagr = lambda d_: ((d_[FY1] / d_[FY0]) ** (1 / 5) - 1) * 100 if FY0 in d_ and d_[FY0] > 0 and d_[FY1] > 0 else None
CAGR_REV, CAGR_NI = cagr(_ra), cagr(_na)
NM_TTM = sum(ni[k] for k in ks[-4:]) / sum(rev[k] for k in ks[-4:]) * 100
_inst = lambda tag: {x['end']: x['val'] for x in F_.get(tag, {}).get('units', {}).get('USD', []) if x['filed'] <= (cut or asof)}
LI, SE, A_ = _inst('Liabilities'), _inst('StockholdersEquity'), _inst('Assets')
DTE = LI[L] / SE[L] * 100 if L in LI and L in SE else None
NA = '해당 없음'
frow = lambda m, lab, unit, v=None, note=None: {"metric": m, "label": lab, "unit": unit, "value": v, "points": None, "note": note}
fund = {"ticker": T, "basis": "quarter", "asOf": L, "filedAt": filed, "score": None, "grade": None, "qualityFlags": ["financial"],
        "axes": {"health": {"rows": [frow("currentRatio", "유동비율", "%", note=NA), frow("quickRatio", "당좌비율", "%", note=NA),
                                     frow("debtDependency", "차입금의존도", "%", note=NA), frow("interestCoverage", "이자보상배율", "x", note=NA),
                                     frow("debtToEquity", "부채비율", "%", DTE)], "points": None, "max": 33},
                 "growthProfit": {"rows": [frow("revenueCagr", "매출 CAGR", "%", CAGR_REV), frow("opIncomeCagr", "순이익 CAGR", "%", CAGR_NI, "은행은 영업이익 대신 보통주 귀속 순이익"),
                                           frow("opMargin", "영업이익률(OPM)", "%", note=NA), frow("netMargin", "순이익률", "%", NM_TTM)], "points": None, "max": 34}},
        "note": "은행 — 예금이 부채라 유동·차입 비율이 뜻이 없고 v1 모델도 은행을 채점하지 않는다", "netCash": None}
sub(rf'^const {T}_FUNDAMENTAL = \{{.*$', f'const {T}_FUNDAMENTAL = ' + json.dumps(fund, ensure_ascii=False) + ';', re.M)
act = {"ticker": T, "status": "na", "reason": "은행이라 매출채권·재고 회전으로 운영 효율을 판정하지 않는다"}
sub(rf'^const {T}_ACTIVITY = \{{.*$', f'const {T}_ACTIVITY = ' + json.dumps(act, ensure_ascii=False) + ';', re.M)
one("""    if (title) title.textContent = '종합 진단: 판정하지 않음 — ' + ((A && A.reason) || '활동성 데이터 없음');""",
    """    if (title) title.textContent = '종합 진단: 판정하지 않음 — ' + ((A && A.reason) || '활동성 데이터 없음');
    if (A && A.status === 'na') {   // 해당 없는 업종(은행·보험) — 틀 구조는 두고 칸마다 '해당 없음'
      document.querySelectorAll('#fund [data-act-turn], #fund [data-act-days]').forEach(el => { el.textContent = '해당 없음'; });
      document.querySelectorAll('#fund [data-act-sub]').forEach(el => { el.textContent = '—'; });
      const ex = $('actCccExplain'); if (ex) ex.textContent = A.reason + '.';
      const bar = $('actBar'); if (bar) bar.hidden = true;
      const per0 = $('actPeriod'); if (per0) per0.textContent = '해당 없음';
      return;
    }""")
sub(r'분기 매출 / 순이익 / 영업이익률 \([^)]*\)', f'분기 순영업수익 / 순이익 / ROE ({L8[0]}~{L8[-1]})')
sub(r'const revenue=\[[^\]]*\];', 'const revenue=' + json.dumps([r1(rev[k]) for k in ks]).replace(' ', '') + ';')
sub(r'const netIncome=\[[^\]]*\];', 'const netIncome=' + json.dumps([r1(ni[k]) for k in ks]).replace(' ', '') + ';')
sub(r'const opm=\[[^\]]*\];', 'const opm=' + json.dumps(roe_q).replace(' ', '') + ';')
_rq = [x for x in roe_q if x is not None]
sub(r'const y2min=[\d.]+, y2max=[\d.]+;', f'const y2min={max(0, int(min(_rq) // 5 * 5 - 5)) if _rq else 0}, y2max={int(max(_rq) // 5 * 5 + 10) if _rq else 25};')
sub(r"labels:\['Q\d FY\d\d'(,'Q\d FY\d\d'){7}\],", 'labels:[' + ','.join(f"'{x}'" for x in L8) + '],')
one("{type:'line',label:'OPM(%)',", "{type:'line',label:'ROE(최근 4분기, %)',")
one("{type:'bar',label:'매출($B)',", "{type:'bar',label:'순영업수익($B)',")
one("{type:'bar',label:'순이익($B)',", "{type:'bar',label:'순이익($B, 보통주 귀속)',")
CET1 = secv.get('cet1') if secv.get('accn') or secv else None
_roe_now = bank.roe(L)
_tiles = [('FCF', (f'CET1 비율 ({QL})', f'{CET1 * 100:.1f}%', '원문 공시(표준방식)') if CET1 else
                  (f'ROE ({QL}, 최근 4분기)', f1(_roe_now[0]) if _roe_now else '—', '보통주 귀속 순이익 ÷ 1년 전 보통주 자본')),
          ('Capex', (f'순이자이익 ({QL})', B(nii[cur]), f'1년 전 대비 {pc(chg(nii[cur], nii.get(yo)))}')),
          ('R&amp;D', (f'효율성 비율 ({QL})', f'{nie[cur] / rev[cur] * 100:.1f}%', f'비이자비용 ÷ 순영업수익 · 1년 전 {nie[yo] / rev[yo] * 100:.1f}%'))]
for lab, (nl, val, subt) in _tiles:
    sub(rf'<div class="stat-label">{lab} \([^)]*\)</div>\n      <div class="stat-value">[^<]*</div>\n      <div class="stat-sub">[^<]*</div>',
        f'<div class="stat-label">{nl}</div>\n      <div class="stat-value">{val}</div>\n      <div class="stat-sub">{subt}</div>')
sub(r'<div class="stat-value">[^<]*</div>\n      <div class="stat-sub">일정 · [^<]*</div>',
    f'<div class="stat-value">{NEXT[0]}</div>\n      <div class="stat-sub">{NEXT[1]}</div>')
sub(r'재무 건전성 — 안정성·활동성 \([^)]*\)', f'재무 건전성 — 안정성·활동성 ({QL} · {qd_(L)} 기준)')
sub(r'<span id="fundHealthAxis">[^<]*</span>', '<span id="fundHealthAxis">점수 없음</span>')
sub(r'<div class="title" id="fundHealthTitle">[^<]*</div>', '<div class="title" id="fundHealthTitle">종합 진단: 판정하지 않음 — 은행이라 점수를 매기지 않는다</div>')
one('<div class="diag-summary" id="fundHealthSummary">', '<div class="diag-summary watch" id="fundHealthSummary">')
one('<span>안정성 상세 — 개별 비율 7개</span>', '<span>안정성 상세 — 개별 비율 7개 · 은행 자본 지표</span>')
_fya = sorted(k for k in A_ if k.endswith('12-31') and k <= L)
a1, a0 = A_[_fya[-1]], A_[_fya[-2]]
sub(r'<span class="diag-label">총자산증가율</span><span class="diag-value">[^<]*</span><span class="diag-note">[^<]*</span>',
    f'<span class="diag-label">총자산증가율</span><span class="diag-value">{(a1 / a0 - 1) * 100:+.1f}%</span><span class="diag-note">FY{_fya[-1][2:4]} ${a1 / 1e12:.2f}T(전기 ${a0 / 1e12:.2f}T) · 연간 지표, 다음 10-K 전까지 동일</span>'.replace('+-', '−'))
sub(r'<span class="diag-value" id="fundNetCashPs">[^<]*</span><span class="diag-note" id="fundNetCashNote">[^<]*</span>',
    '<span class="diag-value" id="fundNetCashPs">해당 없음</span><span class="diag-note" id="fundNetCashNote">은행은 예금·차입이 영업 자금이라 순현금을 따지지 않는다</span>')
xrow = lambda lab, val, note: (f'      <div class="diag-row">\n        <div class="diag-left"><span class="diag-label">{lab}</span><span class="diag-value">{val}</span>'
                               f'<span class="diag-note">{note}</span></div>\n        <div class="diag-badge info">ℹ️ 참고</div>\n      </div>\n')
_bv = lambda e: (bank.ce(e)[0] / bank.shares(e)[0]) if bank.ce(e) and bank.shares(e) else None
_tbv = lambda e: (bank.tce(e)[0] / bank.shares(e)[0]) if bank.tce(e) and bank.shares(e) else None
BVPS, TBVPS = _bv(L), _tbv(L)
extra = ((xrow('CET1 비율 (표준방식)', f'{CET1 * 100:.1f}%', f'{qd_(L)} 원문 공시') if CET1 else '')
         + (xrow('주당 장부가치 (BVPS)', f'${BVPS:.2f}', f'1년 전 대비 {pc(chg(BVPS, _bv(yo)))} · 보통주 자본 ÷ 분기말 주식 수(SEC 10-Q)' + (f' · {K.BV_NOTE}' if K.BV_NOTE and 'BVPS' in K.BV_NOTE + 'GS' and T == 'GS' else '')) if BVPS else '')
         + (xrow('주당 유형 장부가치 (TBVPS)', f'${TBVPS:.2f}', f'1년 전 대비 {pc(chg(TBVPS, _tbv(yo)))} · 영업권·무형자산을 뺀 값, 이연법인세 미가산(카드의 P/TBV 분모)' + (f' · {K.BV_NOTE}' if K.BV_NOTE and T != 'GS' else '')) if TBVPS else ''))   # BV_NOTE: GS는 BVPS 줄, 나머지는 TBVPS 줄(2026-10-17 COF 하드코딩 → BNY도)
sub(r'(<span class="diag-note" id="fundNetCashNote">[^<]*</span></div>\n        <div class="diag-badge info">ℹ️ 참고</div>\n      </div>\n)', lambda m: m.group(1) + extra)
sub(r'<div style="margin-top:14px;font-size:11\.5px;color:var\(--text2\);line-height:1\.6;">유동비율·당좌비율.*?</div>',
    '<div style="margin-top:14px;font-size:11.5px;color:var(--text2);line-height:1.6;">은행은 예금이 부채라 유동·당좌·차입 비율과 이자보상배율이 뜻이 없어 해당 없음으로 두고, '
    + ('규제자본 비율과 ' if CET1 else '') + '장부가치를 대신 싣는다.' + (f' 부채비율 {DTE:,.0f}%는 예금을 포함한 값이다.' if DTE else '') + ' 값은 모두 SEC 10-Q·10-K에서 계산했다(회사 발표값과 정의가 다를 수 있다).</div>')
vec = lambda e: [r1(rev[e]), r1(rev[e] - nie[e]), r1(ni[e]), r1(nii[e])]
fpc = lambda a, b_: '%+.1f%%' % ((a / b_ - 1) * 100) if b_ and b_ > 0 and a > 0 else ('흑자 전환' if a > 0 else '적자 지속' if b_ and b_ <= 0 else '적자 전환')
yd = [fpc(rev[cur], rev[yo]), fpc(rev[cur] - nie[cur], rev[yo] - nie[yo]), fpc(ni[cur], ni[yo]), fpc(nii[cur], nii[yo])]
qdl = [fpc(rev[cur], rev[qo]), fpc(rev[cur] - nie[cur], rev[qo] - nie[qo]), fpc(ni[cur], ni[qo]), fpc(nii[cur], nii[qo])]
tq = lambda a: ', '.join(f"'{x}'" for x in a)
for kind, cmp, cl in (('YoY', yo, YL), ('QoQ', qo, QQL)):
    sub(rf"curLabel: '[^']*', cmpLabel: '[^']*',\n    titleSuffix: '{kind} [^']*',\n    chart: \{{ cur: \[[^\]]*\], cmp: \[[^\]]*\] \}},\n    deltas: \[[^\]]*\],",
        f"curLabel: '{QL}', cmpLabel: '{cl}',\n    titleSuffix: '{kind} ({QL} vs {cl})',\n    chart: {{ cur: {vec(cur)}, cmp: {vec(cmp)} }},\n    deltas: [{tq(yd if kind == 'YoY' else qdl)}],")
_fns = list(re.finditer(r"footnote: '기준일: [^\n]*'", h))
assert len(_fns) == 2, len(_fns)   # 틀 순서: YoY, QoQ
for _m, (cmp, cl) in sorted(zip(_fns, ((yo, YL), (qo, QQL))), key=lambda z: -z[0].start()):
    h = h[:_m.start()] + (f"footnote: '기준일: {qd_(cur)}({QL}) vs {qd_(cmp)}({cl}) · GAAP · 충당금 전 이익 = 순영업수익 − 비이자비용 · 순이익은 보통주 귀속 · "
                          f"<a href=\"{PRU}\" target=\"_blank\" rel=\"noopener\">{K.CO} {QL} 실적 보도자료 (SEC 8-K) →</a>'") + h[_m.end():]
sub(r'<span id="fundPeriodTitle">YoY \([^)]*\)</span>', f'<span id="fundPeriodTitle">YoY ({QL} vs {YL})</span>')
one("        labels: ['매출', '영업이익', '순이익', 'FCF'],", "        labels: ['순영업수익', '충당금 전 이익', '순이익', '순이자이익'],")
one('// FCF = 영업현금흐름 − PaymentsToAcquireProductiveAssets, 분기값은 누적값의 차이.',
    '// 은행: 순영업수익 · 충당금 전 이익(순영업수익 − 비이자비용) · 보통주 귀속 순이익 · 순이자이익, 분기값은 누적값의 차이(SEC 10-Q·10-K).')
# 매출 구성: 순이자이익 · 그 밖의 순영업수익(사업부 순이익은 보도자료에만 있다 — 7판 11-7)
oth = rev[cur] - nii[cur]
SEG = [('순이자이익', round(nii[cur] / 1e6), K.COLOR), ('그 밖의 순영업수익 (비이자 수익)', round(oth / 1e6), '#94a3b8')]
tot = sum(v for _, v, _ in SEG)
leg = ''.join(f'\n          <div style="display:flex;align-items:center;gap:7px;font-size:11px;color:var(--text2);white-space:nowrap;"><span style="width:8px;height:8px;border-radius:50%;background:{c};display:inline-block;flex-shrink:0;"></span>{n} <strong style="color:var(--text);">${v / 1000:.1f}B · {v / tot * 100:.1f}%</strong></div>' for n, v, c in SEG)
_oth_yo = rev[yo] - nii[yo]
sub(r'<div class="card-title">매출 구성 — .*?</div>\n\n      <div style="display:flex;align-items:center;justify-content:center;gap:20px;">.*?\n      </div>\n\n      <div class="yoy-footnote" style="margin-top:14px;">.*?</div>',
    f'<div class="card-title">순영업수익 구성 — 순이자이익 · 그 밖의 수익 ({QL} · {qd_(cur)} 기준)</div>\n\n      <div style="display:flex;align-items:center;justify-content:center;gap:20px;">\n        <div class="chart-wrap" style="height:170px;width:170px;flex-shrink:0;">\n          <canvas id="segmentPieChart"></canvas>\n        </div>\n        <div style="display:flex;flex-direction:column;gap:9px;">' + leg +
    f'\n        </div>\n      </div>\n\n      <div class="yoy-footnote" style="margin-top:14px;">1년 전 같은 분기보다 순이자이익 {pc(chg(nii[cur], nii[yo]))}, 그 밖의 순영업수익 {pc(chg(oth, _oth_yo))} · 그 밖의 수익 = 순영업수익 − 순이자이익 · 출처: <a href="{PRU}" target="_blank" rel="noopener">{K.CO} {QL} (SEC) →</a></div>')
sub(r'// ─── 매출 구성 도넛 차트 \([^)]*\) ───', '// ─── 순영업수익 구성 도넛 차트 (순이자이익 · 그 밖의 수익, 백만 달러) ───')
sub(r'const total = \d+;', f'const total = {tot};')
_m = re.search(r"labels:(\[[^\]]*\]),\s*\n?\s*datasets:\s*\[\s*\{\s*data:\s*(\[[^\]]*\]),", h)
assert _m, '도넛 labels·data를 못 찾았다'
h = h[:_m.start(1)] + json.dumps([n for n, _, _ in SEG], ensure_ascii=False) + h[_m.end(1):_m.start(2)] + '[' + ', '.join(str(v) for _, v, _ in SEG) + ']' + h[_m.end(2):]
sub(r"(segmentPieChart[\s\S]{0,1500}?backgroundColor:)\[[^\]]*\]", lambda m: m.group(1) + json.dumps([c for _, _, c in SEG]))
# 자본배분 — SEC 현금흐름표·주당 배당(선언) 태그
_buy, _div = bank.buy.get(cur), (bank.div_com.get(cur) or ((bank.div_all[cur][0] - bank.div_pref.get(cur, (0,))[0], '') if bank.div_all.get(cur) else None))
_dps, _dps_yo, _dlab, _dend = ac.latest_dps(CIK, cur)
_pay, _nit = bank.payout_ttm(cur), bank.ni_ttm(cur)
PAY = _pay[0] / _nit[0] if _pay and _nit and _nit[0] > 0 else None
zone = lambda lab, val, tag=None: (f'        <div class="zone-item">\n          <span class="zone-label">{lab}</span>\n'
                                   + (f'          <div style="display:flex;align-items:center;gap:8px;">\n            <span class="zone-tag" style="background:rgba(240,192,64,0.18);color:var(--gold);">{tag}</span>\n            <span class="zone-val">{val}</span>\n          </div>\n'
                                      if tag else f'          <span class="zone-val">{val}</span>\n') + '        </div>\n')
CAPA = (f'<div class="card-title">자본배분 · 주주환원 ({QL} · {qd_(cur)} 기준)</div>\n      <div class="zone-list">\n'
        + zone(f'자사주 매입 ({QL})', B(_buy[0]) if _buy else '공시 없음')
        + zone(f'보통주 배당 ({QL})', B(_div[0]) if _div else '공시 없음')
        + (zone(f'최근 분기 주당 배당 ({_dlab}, {_dend[5:7].lstrip("0")}/{_dend[8:].lstrip("0")} 분기)', f'${_dps:.2f}', (f'1년 전 ${_dps_yo:.2f} · {pc(chg(_dps, _dps_yo))}' if _dps_yo else None)) if _dps else '')
        + zone('최근 4분기 순환원율 (배당 + 매입 − 발행 ÷ 순이익)', f'{PAY * 100:.0f}%' if PAY is not None else '—')
        + f'      </div>\n      <div class="yoy-footnote" style="margin-top:14px;">현금흐름표 기준(SEC {"10-K" if cur.endswith("12-31") else "10-Q"}) · <a href="{PRU}" target="_blank" rel="noopener">{K.CO} {QL} 실적 보도자료 (SEC 8-K) →</a></div>\n    </div>')
sub(r'<div class="card-title">자본배분 · 주주환원 \([^)]*\)</div>\n      <div class="zone-list">.*?\n      </div>\n    </div>', CAPA)
# 체크포인트 — 규칙(숫자는 SEC, 원인은 쓰지 않는다)
_roe_yo = bank.roe(yo)
_eff, _eff_yo = nie[cur] / rev[cur] * 100, nie[yo] / rev[yo] * 100
CHKS = [f'최근 4분기 ROE({f1(_roe_now[0]) if _roe_now else "—"})가 1년 전({f1(_roe_yo[0]) if _roe_yo else "—"})보다 높은 수준을 지키는지',
        f'순이자이익이 1년 전 같은 분기보다 늘어나는지({QL} {pc(chg(nii[cur], nii[yo]))})',
        f'효율성 비율(비이자비용 ÷ 순영업수익, {QL} {_eff:.1f}%, 1년 전 {_eff_yo:.1f}%)이 낮아지는지',
        (f'최근 4분기 순환원율 {PAY * 100:.0f}%가 이익 안에서 유지되는지' if PAY is not None and PAY <= 1 else
         f'최근 4분기 순환원율 {PAY * 100:.0f}%로 이익보다 많이 돌려주는 흐름이 이어지는지' if PAY is not None else '자사주 매입·배당 공시')]
CHK = (f'<div class="card-title">다음 실적 체크포인트 <span style="color:var(--gold);font-weight:600;">{CHECK_WHEN}</span></div>\n    <div style="font-size:12px;color:var(--text2);line-height:1.8;">\n'
       + '\n'.join(f'      <div{" style=\"margin-bottom:8px;\"" if i < 3 else ""}><strong style="color:var(--accent2);">{"①②③④"[i]}</strong> {c}</div>' for i, c in enumerate(CHKS))
       + '\n    </div>')
sub(r'<div class="card-title">다음 실적 체크포인트 <span[^>]*>[^<]*</span></div>\n    <div style="font-size:12px;color:var\(--text2\);line-height:1\.8;">.*?\n    </div>', CHK)

# ── 4. 밸류에이션 ──
one('<div class="vc-head">PBR</div>', '<div class="vc-head">P/TBV</div>')
sub(r'<div class="vs-name" title="지난 5년 [A-Z]+ 자신의 배수보다 지금이 얼마나 낮은가\. 높을수록 싸다\.">자기 이력 대비</div>',
    f'<div class="vs-name" title="지난 5년 {T} 자신의 배수보다 지금이 얼마나 낮은가. 높을수록 싸다. 은행 규칙에 따라 P/TBV·PER 두 배수가 모두 70 이상이면 +1, 모두 30 미만이면 −1이다.">자기 이력 대비</div>')
one('<div class="vs-name" title="회사가 앞으로 벌어들일 현금만으로 계산한 주당 가치(기본 시나리오).">현금흐름 (내재가치)</div>',
    '<div class="vs-name" title="은행은 초과이익모형(장부가치 + 자기자본비용 10%를 넘는 이익의 현재가치)으로 계산한다. 기본 시나리오.">초과이익 (내재가치)</div>')
one('<span class="logic-tag">내재가치 <span class="logic-denom">현금흐름</span></span>', '<span class="logic-tag">내재가치 <span class="logic-denom">초과이익</span></span>')
one('<div class="vs-name" title="같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.">동종업 대비</div>',
    '<div class="vs-name" title="S&amp;P500 은행(대형·지역) 대비 P/TBV·PER 순위. 높을수록 싸다. 두 배수가 같은 방향일 때만 표를 준다.">동종업 대비</div>')
sub(r'<div class="vs-note">현재가 <span data-vs="price">[^<]*</span> 대비 <strong data-vs="upside">[^<]*</strong> · 기본 시나리오</div>',
    '<div class="vs-note">현재가 <span data-vs="price">—</span> 대비 <strong data-vs="upside">—</strong> · 초과이익모형 기본</div>')
one('<span class="val-name">PBR <span class="hist-note" data-hist="note"></span></span>', '<span class="val-name">P/TBV (유형 장부) <span class="hist-note" data-hist="note"></span></span>')
TB0 = (SH.get('ptbv') or {}).get('firstDay')
_ptd = (SH.get('ptbv') or {}).get('days')
a_ = h.index('    </div>\n\n    <div class="card" style="display:flex;flex-direction:column;">')
h = h[:a_] + ('      <div style="font-size:11px;color:var(--text3);line-height:1.6;margin-top:6px;">은행은 매출·현금흐름·EBITDA 배수가 뜻이 없어 P/TBV·PER 두 배수만 본다. P/TBV는 보통주 자본에서 영업권·무형자산을 뺀 유형 장부가치 기준(이연법인세를 더하지 않아 회사 발표 TBVPS보다 작다). '
              + (f'P/TBV 이력은 {_ptd}거래일({_ptd / 252:.1f}년)이라 "5년 중" 위치는 그 안의 위치다.' if _ptd and _ptd < 1200 else '') + '</div>\n') + h[a_:]
wm = lambda k, m: {"metric": k, "score": round(m['score'], 1), "percentile": round(m['percentile'], 1), "current": round(m['current'], 2) if isinstance(m.get('current'), (int, float)) else None,
                   "min": round(m['min'], 2), "median": round(m['median'], 2), "max": round(m['max'], 2), "days": m['days'], "gapDays": m['gapDays']} if m else {"metric": k, "score": None}
pm = lambda k, m: {"metric": k, "score": m.get('score'), "rank": m.get('rank'), "peers": m.get('peers')}
V = {"peer": {"score": peerscore, "rule": "both", "sector": "Financials (S&P500 은행)", "asOf": [asof, asof],
              "metrics": [pm('per', PEER['per']), pm('pbr', PEER['ptbv'])]},
     "self": {"score": selfscore, "rule": "both", "naNote": "은행에 해당 없음", "window": [D[0][0], asof],
              "metrics": [wm('per', SH.get('per')), wm('pbr', SH.get('ptbv'))]}}
sub(rf'^const {T}_VALUATION = \{{.*$', f'const {T}_VALUATION = ' + json.dumps(V, ensure_ascii=False) + ';', re.M)
UB = json.load(open('peer_universe/banks.json'))
U = {k: v for k, v in UB['tickers'].items() if k != T}
NOTB = sorted(k for k in U if not isinstance(U[k].get('ptbv'), (int, float)))
mdy = f'{int(UB["asOf"][5:7])}/{int(UB["asOf"][8:])} 종가'
mk = lambda key, title, unit, mx: {"title": title, "unit": unit, "max": mx, f"{t}Value": None,
                                   "peers": [{"name": x, "value": round(U[x][key], 2), "status": "reference"} for x in K.PB if isinstance(U.get(x, {}).get(key), (int, float))]}
MD = {"per": mk('per', f'S&P500 은행 PER 비교 · {mdy}', 'PER(TTM)', 25),
      "pbr": mk('ptbv', f'S&P500 은행 P/TBV 비교 · {mdy}' + (f' ({"·".join(NOTB)}는 유형자본을 만들 수 없음)' if NOTB else ''), 'P/TBV', 4)}
for k, nm, why in (('psr', 'PSR', '은행 매출에는 이자수익이 들어 있다'), ('pcr', 'PCR', '은행 현금흐름은 예금·대출 증감이 좌우한다'), ('evebitda', 'EV/EBITDA', '예금·차입이 영업 자금이라 기업가치가 뜻이 없다')):
    MD[k] = {"title": f'{nm} — 은행에 해당 없음 ({why})', "unit": nm, "max": 1, f"{t}Value": None, "peers": []}
sub(r'(// [^\n]*\n)?const MULTIPLE_DATA = \{.*?\n\};\n', '// 은행 동종업(peer_universe/banks.json, 은행 사전 등록 §3)에서 고른 6곳. 값이 없는 은행은 뺀다.\nconst MULTIPLE_DATA = ' + json.dumps(MD, ensure_ascii=False, indent=2) + ';\n')
sub(r'<div class="card-title"><span id="multipleCompareTitle">[^<]*</span></div>', f'<div class="card-title"><span id="multipleCompareTitle">{MD["per"]["title"].replace("&", "&amp;")}</span></div>')
lvl = px / R['기본'] if RIM_OK and R['기본'] > 0 else None
_sv = lambda d: None if not (d.get('ptbv') and d.get('per')) or d['ptbv'].get('score') is None or d['per'].get('score') is None else \
    (1 if d['ptbv']['score'] >= 70 and d['per']['score'] >= 70 else -1 if d['ptbv']['score'] < 30 and d['per']['score'] < 30 else 0)
v_self, v_peer = _sv(SH), _sv(PEER)
_d = None if not RIM_OK else (-2 if R['기본'] <= 0 else 1 if lvl <= 0.9 else 0 if lvl <= 1.1 else -1 if lvl <= 1.5 else -2)
VOTES = (v_self, v_peer, _d)
if None in VOTES:
    VERD = '판정 보류'
else:
    _sum = sum(VOTES)
    VERD = '저평가' if _sum >= 3 else '적정~저평가' if _sum >= 1 else '적정' if _sum > -1 else '적정~고평가' if _sum > -3 else '고평가'
sgn = lambda v: '기권' if v is None else (f'{v:+d}'.replace('-', '−') if v else '0')
_lvlw = (None if lvl is None else '매우 싸다' if lvl <= 0.7 else '싸다' if lvl <= 0.9 else '적정' if lvl <= 1.1 else '비싸다' if lvl <= 1.5 else '매우 비싸다')
_near = (lvl is not None and any(abs(lvl - x) < 0.05 for x in (0.7, 0.9, 1.1, 1.5)))
RISK_TXT = ((f'⚠️ 현재가 ÷ 기본 가치가 {lvl:.2f}로 "{_lvlw}"다' + (' — 경계 가까이라 작은 주가 움직임으로 칸이 바뀔 수 있다' if _near else '') + '. ' if lvl is not None else '⚠️ 초과이익모형을 계산하지 않아 세 번째 칸이 기권이다. ')
            + f'세 칸이 자기 이력 {sgn(v_self)} · 동종업 {sgn(v_peer)} · 초과이익 {sgn(_d)}로 종합 평가는 {VERD}다.'
            + (f' 재무는 관문을 통과한 {QL}에 머물러 있다({", ".join((R.get("frozen") or {}).get("stop", []))} 미통과 분기 반영 보류).' if R.get('frozen') else ''))
_ptbv_now = (SH.get('ptbv') or {}).get('current')
_rank = (PEER.get('ptbv') or {}).get('rank'), (PEER.get('ptbv') or {}).get('peers')
_hy = f'{_ptd / 252:.1f}년' if _ptd and _ptd < 1200 else '5년'
PREM = (f'P/TBV {_ptbv_now:.2f}배는 자기 {_hy} 이력의 {"위쪽" if (SH["ptbv"]["percentile"] >= 50) else "아래쪽"}(상위 {100 - SH["ptbv"]["percentile"]:.0f}%)' if isinstance(_ptbv_now, (int, float)) else 'P/TBV 이력이 없다')
_ntot = (_rank[1] or 0) + 1
_inu = T in json.load(open(os.path.join(V2, 'peer_universe', 'banks.json')))['tickers']   # 비교군(S&P500 대형·지역 은행) 밖 은행 — BNY 수탁은행(2026-10-17)
_grp = f'S&P500 은행 {_ntot}곳(본인 포함)' if _inu else f'비교군 S&P500 대형·지역 은행 {_ntot - 1}곳' + (f'({K.PEER_NOTE})' if getattr(K, 'PEER_NOTE', '') else '') + '과 견주면'
PREM += ((f'이고 {_grp} 중 가장 비싸다. ' if _rank[0] == _ntot else f'이고 {_grp} 중 가장 싸다. ' if _rank[0] == 1
          else f'이고 {_grp} 중 비싼 쪽부터 {_ntot - _rank[0] + 1}번째다. ') if _rank[0] else '. ')
if not _inu:
    PREM = PREM.replace(f'{_grp} 중 가장 비싸다', f'{_grp} 가장 비싸다').replace(f'{_grp} 중 가장 싸다', f'{_grp} 가장 싸다').replace(f'{_grp} 중 비싼 쪽부터', f'{_grp} 비싼 쪽부터')
PREM += (f'<strong>초과이익모형 기본 가치 ${R["기본"]:.0f}은 현재가의 {1 / lvl * 100:.0f}%</strong>로, 지금 가격은 ROE {f1(R["required_roe"])}가 5년 이어진다는 값이다(최근 4분기 {f1(R["roe0"])}, GAAP).'
         if lvl is not None and R.get('required_roe') is not None else '')
sub(r'<div class="vs-premise">.*?</div>\n    <div class="verdict-summary-risk">.*?</div>',
    f'<div class="vs-premise">{PREM}</div>\n    <div class="verdict-summary-risk">{RISK_TXT}</div>')
one("""  const valid = side => side && side.score != null
    && (side.metrics || []).filter(m => m.score != null).length >= 3;
  const vote = s => s >= 70 ? 1 : s < 30 ? -1 : 0;""",
    """  // 금융 카드(rule 'both', research/brkb_two_pillar_prereg.md §2 · bank_rim_prereg.md §0)는 두 배수로 성립하고,
  // 두 점수가 모두 70 이상이면 +1, 모두 30 미만이면 −1이다(P/TBV = PER × ROTCE라 독립 증거가 아니다).
  const valid = side => side && side.score != null
    && (side.metrics || []).filter(m => m.score != null).length >= (side.rule === 'both' ? Math.max(2, side.metrics.length) : 3);
  const vote = s => s >= 70 ? 1 : s < 30 ? -1 : 0;
  const sideVote = side => side.rule === 'both'
    ? (side.metrics.every(m => m.score >= 70) ? 1 : side.metrics.every(m => m.score < 30) ? -1 : 0) : vote(side.score);""")
one("['자기 이력', valid(V.self) ? vote(V.self.score) : null, V.self && V.self.score, 1],",
    "['자기 이력', valid(V.self) ? sideVote(V.self) : null, V.self && V.self.score, 1],")
one("['동종업', valid(V.peer) ? vote(V.peer.score) : null, V.peer && V.peer.score, 1],",
    "['동종업', valid(V.peer) ? sideVote(V.peer) : null, V.peer && V.peer.score, 1],")
one(f"  if (verdictOf(judges) === {T}_VERDICT) judges.slice(0, 2).forEach((j, i) => {{",
    "  // 금융 카드는 심판 표가 sideVote(규칙별 — 두 배수가 같은 쪽일 때만 표)라 한 칸 바꾸기 계산이 맞지 않아 건너뛴다(Codex)\n  if (false) judges.slice(0, 2).forEach((j, i) => {")
one("pill('self', ...byScore(V.self.score)); pill('peer', ...(V.peer.score == null ? ['mid', '표본 부족'] : byScore(V.peer.score)));",
    """const bothPill = s => s.metrics.some(m => m.score == null) ? ['mid', '기권'] : s.metrics.every(m => m.score >= 70) ? ['', '싸다'] : s.metrics.every(m => m.score < 30) ? ['high', '비싸다'] : ['mid', '중간'];
  pill('self', ...(V.self.rule === 'both' ? bothPill(V.self) : byScore(V.self.score)));
  pill('peer', ...(V.peer.score == null ? ['mid', '표본 부족'] : V.peer.rule === 'both' ? bothPill(V.peer) : byScore(V.peer.score)));""")
one("""    const f = sel => item.querySelector(`[data-hist="${sel}"]`), x = v => v.toFixed(1) + 'x';""",
    """    const f = sel => item.querySelector(`[data-hist="${sel}"]`), x = v => v.toFixed(m.metric === 'pbr' ? 2 : 1) + 'x';""")
one("""  ['peer', 'self'].forEach(k => {""",
    """  // 이 카드가 쓰지 않는 배수(금융 카드의 PSR·PCR·EV/EBITDA)는 같은 자리에 '해당 없음'
  const haveM = new Set(V.self.metrics.map(m => m.metric));
  if (V.self.metrics.length) document.querySelectorAll('#valuation .val-item[data-metric]').forEach(item => {
    if (haveM.has(item.dataset.metric)) return;
    const f = sel => item.querySelector(`[data-hist="${sel}"]`);
    if (f('cur')) f('cur').textContent = '—';
    if (f('badge')) { f('badge').className = 'hist-badge mid'; f('badge').textContent = '해당 없음'; }
    if (f('note')) f('note').textContent = V.self.naNote || '';
    if (f('fill')) { f('fill').className = 'val-fill hist-fill mid'; f('fill').style.width = '0%'; }
    ['min', 'median', 'max'].forEach(k => { if (f(k)) f(k).textContent = '—'; });
  });
  ['peer', 'self'].forEach(k => {""")
one("""  // 두 밸류에이션 점수가 크게 갈리면 그 사실 자체가 정보다.""",
    f"""  [['self', '{t}SelfBox', '{t}SelfVerdict'], ['peer', '{t}PeerBox', '{t}PeerVerdict']].forEach(([k, bid, vid]) => {{
    const side = {T}_VALUATION[k];   // 금융 규칙: 단어·색은 두 배수가 같은 방향일 때만 싼 편·비싼 편
    if (!side || side.rule !== 'both' || !side.metrics.length) return;
    const ms = side.metrics, sb = $(bid), sv = $(vid);
    const w = ms.some(m => m.score == null) ? ['logic-neutral', '기권'] : ms.every(m => m.score >= 70) ? ['logic-positive', '싼 편'] : ms.every(m => m.score < 30) ? ['logic-negative', '비싼 편'] : ['logic-neutral', '중간'];
    if (sb) {{ sb.classList.remove('logic-positive', 'logic-neutral', 'logic-negative'); sb.classList.add(w[0]); }}
    if (sv) sv.textContent = w[1];
  }});
  // 두 밸류에이션 점수가 크게 갈리면 그 사실 자체가 정보다.""")
one("const selfRaw = selfNA ? null : _vs ? +_vs.current.toFixed(1) : d[selfKey];",
    "const selfRaw = selfNA ? null : _vs ? +_vs.current.toFixed(_vs.current < 10 ? 2 : 1) : d[selfKey];")
one("""      + `\\n대차대조표와 마진은 ${S.fundamentalAsOf} 분기(확인 필요), 성장률은 연간 시계열을 쓴다.`
      + `\\n(확인 필요 — NVDA 문장 자리)`);""",
    f"""      + `\\n은행이라 점수를 매기지 않는다 — 예금이 부채라 유동·차입 비율이 뜻이 없고 영업이익 개념도 없다.`
      + `\\n기본적 분석 탭에 ${{S.fundamentalAsOf}} 분기({QL}) 자본비율·장부가치를 싣는다(SEC 10-Q·10-K 계산).`);""")
one("""    const WHY = { negative_equity:""", """    const WHY = { financial: '은행·보험이라 일반 재무비율 산식이 맞지 않는다', negative_equity:""")
one("if (vd) vd.textContent = F.qualityFlags.length ? '해석 제한' : (F.grade || '—');",
    "if (vd) vd.textContent = F.qualityFlags.includes('financial') ? '판정 안 함' : F.qualityFlags.length ? '해석 제한' : (F.grade || '—');")
_why = {k: (UB.get('skipped', {}).get(k + ':ptbv') or '값 없음') for k in NOTB}
one("""      `같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.`
      + `\\n배수마다 "나보다 싼 종목이 몇 %인가"를 뒤집어 점수로 썼고 다섯 개를 평균했다.`
      + `\\n회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.`);""",
    f"""      `S&P500 은행(대형 7·지역 6) 안에서 P/TBV·PER 순위를 매긴 값이다(표시 점수는 두 배수 평균).`
      + `\\nP/TBV는 유형자본을 만들 수 있는 {PEER['ptbv'].get('peers')}곳, PER은 {PEER['per'].get('peers')}곳과 비교했다.`
      + `{('\\n' + '·'.join(NOTB) + '는 P/TBV에서 빠졌다(' + '; '.join(f'{k}: {_why[k]}' for k in NOTB) + ').') if NOTB else ''}`);""")
_sp_ = SH.get('ptbv') or {}
one("""      + `\\n(확인 필요 — NVDA 문장 자리)`
      + ``);""",
    f"""      + `\\n{(f"P/TBV {_sp_['current']:.2f}배(5년 중 상위 {100 - _sp_['percentile']:.0f}%)" if isinstance(_sp_.get('current'), (int, float)) else 'P/TBV 없음')}·PER {SH['per']['current']:.1f}배(상위 {100 - SH['per']['percentile']:.0f}%).{(f" P/TBV 이력은 {TB0}부터 {_ptd}거래일이다." if TB0 and _ptd and _ptd < 1200 else '')}`
      + ``);""")

# ── 5. 뉴스 · 종합 해석 · 강세/약세 · 애널리스트 ──
def item(dot, date, react, title, href, src):
    cls = f'tl-dot {dot}'.strip()
    rx = f'<span class="tl-reaction flat" data-react="{react}">0.0%</span>' if react else ''
    return (f'      <div class="tl-item">\n        <div class="{cls}"></div>\n        <div class="tl-date">{date}{rx}</div>\n'
            f'        <div class="tl-title">{title}</div>\n        <a class="tl-source" href="{href}" target="_blank" rel="noopener">{src} →</a>\n      </div>')


_na = [e for e in (json.load(open('news_auto.json')).get(T, []) if os.path.exists('news_auto.json') else []) if e.get('results') and e['filed'] <= asof]
items = []
for e in sorted(_na, key=lambda e: e['accepted'], reverse=True)[:6]:
    d0 = dt.date.fromisoformat(e['date'])
    r0 = (d0 + dt.timedelta(days=1)).isoformat() if e.get('after_close') else e['date']
    rx = min((x for x in days if x >= r0), default=None)
    if rx is None:   # 마지막 종가 뒤(장 마감 후)에 나온 발표 — 다음 종가가 생기면 넣는다(Codex)
        continue
    sh_ = dt.date.fromisoformat(rx)
    body = '실적 보도자료 공시(8-K 2.02항)'
    _qe = [k for k in ks if 0 < (d0 - dt.date.fromisoformat(k)).days <= 80]
    if _qe:
        k = _qe[-1]; ky = [x for x in sorted(ni) if 350 <= (dt.date.fromisoformat(k) - dt.date.fromisoformat(x)).days <= 380]
        body = f'{qlab(k)} 순영업수익 {B(rev[k])}, 보통주 귀속 순이익 {B(ni[k])}' + (f'(1년 전 {B(ni[ky[-1]])})' if ky else '') + ' · SEC 10-Q·10-K 기준'
    items.append(('neutral', f'{sh_.year}년 {sh_.month}월 {sh_.day}일 — 실적 발표', rx, body, e['url'], f'{K.CO} 실적 보도자료 (SEC 8-K)'))
if not items:
    items.append(('neutral', f'{qd_(filed)} — {QL} 보고서', None, f'{QL} {"10-K" if L.endswith("12-31") else "10-Q"} 공시', PRU, f'{K.CO} (SEC)'))
for it in items:
    assert it[2] is None or it[2] in days, it[2]
tl = '    <div class="timeline" id="newsTimeline">\n' + '\n'.join(item(*i) for i in items) + '\n    </div>'
sub(r'    <div class="timeline" id="newsTimeline">\n.*?\n    </div>\n    <div class="tl-pager"', tl + '\n    <div class="tl-pager"')
_nr = sorted(e['date'] for e in _na)
sub(r'<div class="section-title">시계열 주요 뉴스 \([^)]*\)</div>',
    f'<div class="section-title">시계열 주요 뉴스 ({(_nr[0][:7].replace("-", ".") + " ~ " + _nr[-1][:7].replace("-", ".")) if _nr else QL})</div>')
_ch = (px / D[max(-253, -len(D))][4] - 1) * 100
_ni_c = chg(ni[cur], ni[yo])
HEAD = (f'{QL} 순이익(보통주 귀속) {B(ni[cur])}' + (f'({pc(_ni_c)})' if _ni_c is not None and abs(_ni_c) <= 0.5 else '') + f', 최근 4분기 ROE {f1(_roe_now[0]) if _roe_now else "—"}. 주가는 1년 새 {_ch:+.0f}%'.replace('+-', '−'))
_tag = ('수익성 ' + ('높음' if _roe_now and _roe_now[0] >= 0.15 else '자본비용 위' if _roe_now and _roe_now[0] >= 0.10 else '자본비용 아래')) + ' · ' + {'저평가': '저평가', '적정~저평가': '적정~저평가', '적정': '적정', '적정~고평가': '밸류 부담', '고평가': '고평가', '판정 보류': '판정 보류'}[VERD]
SUM = (f'<div class="verdict-summary-head">지배적 내러티브 · {HEAD}<span class="tag">{_tag}</span></div>\n'
       f'    <div class="verdict-summary-counter">⚠️ 세 칸이 자기 이력 {sgn(v_self)} · 동종업 {sgn(v_peer)} · 초과이익 {sgn(_d)}, 종합 "{VERD}"이다.'
       + (f' 초과이익모형 기본 가치(${R["기본"]:.0f})는 현재가의 {1 / lvl * 100:.0f}%다.' if lvl else '') + '</div>\n'
       f'    <div class="verdict-summary-next">🔍 다음 확인 포인트 · {CHECK_WHEN}{CHECK_TAIL}</div>')
sub(r'<div class="verdict-summary-head">지배적 내러티브.*?<div class="verdict-summary-next">.*?</div>', SUM)
row = lambda k, head, t_: f'<div class="bb-row {k}"><span class="bb-icon">{"▲" if k == "bull" else "▼"}</span><span class="bb-head">{head}</span><span class="bb-text">{t_}</span></div>'
cand = []
if _roe_now:
    cand.append(('수익성', 1 if _roe_now[0] >= 0.12 else -1 if _roe_now[0] < 0.10 else 0, f'최근 4분기 ROE {f1(_roe_now[0])}' + (f'(1년 전 {f1(_roe_yo[0])})' if _roe_yo else '')
                 + (' — 자기자본비용 10%를 넘는다.' if _roe_now[0] >= 0.12 else ' — 자기자본비용 10%에 못 미친다.' if _roe_now[0] < 0.10 else ' — 자기자본비용 10% 근처다.')))
_nc = chg(nii[cur], nii[yo])
if _nc is not None:
    cand.append(('순이자이익', 1 if _nc > 0.03 else -1 if _nc < -0.03 else 0, f'{QL} 순이자이익 {B(nii[cur])}, 1년 전보다 {pc(_nc)}.'))
cand.append(('효율', 1 if _eff < _eff_yo - 1 else -1 if _eff > _eff_yo + 1 else 0, f'효율성 비율 {_eff:.1f}%(1년 전 {_eff_yo:.1f}%) — 낮을수록 비용이 적다.'))
if PAY is not None:
    cand.append(('환원', 1 if 0.5 <= PAY <= 1.0 else -1 if PAY > 1.2 else 0, f'최근 4분기 순이익의 {PAY * 100:.0f}%를 배당·자사주로 돌려줬다.'))
if isinstance(_ptbv_now, (int, float)):
    cand.append(('밸류', -1 if SH['ptbv']['percentile'] >= 70 else 1 if SH['ptbv']['percentile'] <= 30 else 0,
                 f'P/TBV {_ptbv_now:.2f}배, 자기 5년 이력의 상위 {100 - SH["ptbv"]["percentile"]:.0f}%.'))
if lvl is not None:
    cand.append(('내재가치', 1 if lvl <= 0.9 else -1 if lvl > 1.1 else 0, f'초과이익모형 기본 가치 ${R["기본"]:.0f}, 현재가 ÷ 기본 {lvl:.2f}.'))
bull = [(a, c) for a, s, c in cand if s > 0][:3] or [(a, c) for a, s, c in cand if s == 0][:1]
bear = [(a, c) for a, s, c in cand if s < 0][:3] or [(a, c) for a, s, c in cand if s == 0][-1:]
m = re.search(r'(<div class="bb-title bb-bull">🐂 Bull 요인</div>\n)(.*?)(\n    </div>\n    <div class="bb-box">\n      <div class="bb-title bb-bear">🐻 Bear 요인</div>\n)(.*?)(\n    </div>\n  </div>)', h, re.S)
h = h[:m.start()] + m.group(1) + '\n'.join('      ' + row('bull', *b_) for b_ in bull) + m.group(3) + '\n'.join('      ' + row('bear', *b_) for b_ in bear) + m.group(5) + h[m.end():]
A = K.ANALYST
sub(rf"const {T}_ANALYST = \{{[^}}]*\}};", f"const {T}_ANALYST = {{ asOf: '{K.ANALYST_ASOF}', source: 'StockAnalysis (의견 집계 · 개별 목표가)', rating: '{A['rating']}', n: {A['n']}, nTargets: {A['nt']}, mean: {A['mean']}, median: {json.dumps(A['median'])},\n  low: {A['low']}, high: {A['high']}, strongBuy: {A['sb']}, buy: {A['b']}, hold: {A['h']}, sell: {A['s']}, strongSell: {A['ss']} }};")
one("  const usd = v => '$' + (Number.isInteger(v) ? v : v.toFixed(2));",
    "  const usd = v => v == null ? '—' : '$' + (Number.isInteger(v) ? v.toLocaleString('en-US') : v.toFixed(2));")
sub(r'<span class="op-val">[^<]*<span class="op-sub">[^<]*</span></span>', f'<span class="op-val">{NEXT_OP[0]} <span class="op-sub">{NEXT_OP[1]}</span></span>')

# ── 6. 은행 카드가 받지 않은 틀 변경 되돌리기(jpm_fill.py 6절과 같다) ──
one("""// 쏠림 안내(2026-10-02 사용자 결정, A0 — research/verdict_replay_prereg.md 결과): 사전 규칙상 문턱 변형이 모두 탈락해 V0를 유지하고,
// 이 칸이 대부분 종목에서 "매우 비싸다"라는 사실을 툴팁으로 알린다. 숫자는 현금흐름이 계산되는 S&P500 비금융 종목의 월별 비중(dq 필터 적용).
// 금융 카드에는 넣지 않는다(검증 패널에 금융이 없다).
const DCF_SKEW_NOTE = "이 칸은 보수적으로 잡혀 있다(할인율 10%, 5년 뒤 영구성장 2.5%). S&P500 비금융 종목의 83~91%가 매달 '매우 비싸다'에 들어간다(2024-10~2026-09). 다른 종목과 견주려면 위 비율 숫자를 함께 볼 것.";
""", '')
one("""      + (lv.ratio != null ? '\\n' + DCF_SKEW_NOTE : '')
""", '')
one("""    // per_na = PER 해당 없음(A3 — 최근 4분기 GAAP 순이익률 2% 미만): 값은 보이되 점수·평균에서 뺀다.
    const perNA = m.currentNote === 'per_na';
    // pbr_na = PBR 해당 없음(C11 — 자본 음수): 비싸다는 뜻이 아니라 잴 수 없다. 점수·평균에서 뺀다.
    const pbrNA = m.currentNote === 'pbr_na';
    const na = m.current == null, neg = na && m.currentNote !== 'missing' && !perNA && !pbrNA;   // missing = 분모를 못 구함(점수 없음)""",
    """    const na = m.current == null, neg = na && m.currentNote !== 'missing' && m.currentNote !== 'pbr_na';   // missing = 분모를 못 구함(점수 없음)""")
one("""    f('badge').textContent = perNA ? '해당 없음 · 평균 제외(순이익률 2% 미만)' : pbrNA ? '해당 없음 · 평균 제외(자본 음수)' : neg ? '적자 · 0점' : na ? '데이터 없음 · 평균 제외' : m.percentile >= 50 ? `5년 중 상위 ${Math.round(100 - m.percentile)}%` : `5년 중 하위 ${Math.round(m.percentile)}%`;
    // 이력이 5년에 못 미치면(회사 전용 태그 구간을 버린 경우 등) 이름 옆에 적는다.
    const nt = f('note'); if (nt) nt.textContent = m.days < 1200 ? `최근 ${(m.days / 252).toFixed(1)}년 이력` : '';""",
    """    f('badge').textContent = neg ? '적자 · 0점' : na ? '데이터 없음 · 평균 제외' : m.percentile >= 50 ? `5년 중 상위 ${Math.round(100 - m.percentile)}%` : `5년 중 하위 ${Math.round(m.percentile)}%`;
    // PBR 해당 없음(C11, 2026-10-04 — 자본 음수): 비싸다는 뜻이 아니라 잴 수 없어 점수·평균에서 뺀다
    if (m.currentNote === 'pbr_na') { f('badge').textContent = '해당 없음 · 평균 제외(자본 음수)'; }
    // 이력이 5년에 못 미치면(회사 전용 태그 구간을 버린 경우 등) 이름 옆에 적는다.
    const nt = f('note'); if (nt) nt.textContent = m.gapDays ? `5년 중 ${m.gapDays}거래일 빈 구간` : m.days < 1200 ? `최근 ${(m.days / 252).toFixed(1)}년 이력` : '';""")
one("""    f('fill').style.width = (m.score == null || perNA || pbrNA ? 0 : Math.max(m.percentile, 2)) + '%';""",
    """    f('fill').style.width = (m.score == null ? 0 : Math.max(m.percentile, 2)) + '%';""")
sub(r"  // PER 해당 없음\(A3\): PER 구간 × EPS로 만든 밴드라.*?\n    return;\n  \}\n", '')
one("  const every = SCN.flatMap(s => G.values[s[0]].flat()).filter(v => v != null && v > 0).concat(price != null ? [price] : []);   // 음수 칸 제외(카드 한정)",
    "  const every = SCN.flatMap(s => G.values[s[0]].flat()).filter(v => v != null).concat(price != null ? [price] : []);")
one("    pv.textContent = pick > 0 ? '주당 $' + (pick < 10 ? pick.toFixed(2) : Math.round(pick)) : '계산 불가(음수)'; pv.style.color = col;",
    "    pv.textContent = pick == null ? '계산 불가' : '주당 $' + Math.round(pick); pv.style.color = col;")
one("    if (price != null) { pu.textContent = pick > 0 ? '현재가 대비 ' + pct(pick) : '—'; pu.style.color = pick > 0 ? tone(pick) : ''; }",
    "    if (price != null) { pu.textContent = pick == null ? '—' : '현재가 대비 ' + pct(pick); pu.style.color = pick == null ? '' : tone(pick); }")

# ── 7. 헤더 판정 단어 ──
h = re.sub(r'(data-verdict style="font-size:22px;color:var\(--gold\);">)[^<]*(</span>)', lambda m_: m_.group(1) + VERD + m_.group(2), h, count=1)
sub(r'<span class="vs-verdict" data-verdict>[^<]*</span>', f'<span class="vs-verdict" data-verdict>{VERD}</span>')
open(p, 'w', encoding='utf-8').write(h)
print('ok', T, QL, 'votes', VOTES, VERD, 'base', R.get('기본'), 'lvl', lvl and round(lvl, 3), 'self', selfscore, 'peer', peerscore, 'next', NEXT[0], 'frozen', bool(R.get('frozen')))
