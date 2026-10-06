"""BAC(뱅크오브아메리카) v2 카드 채우기 — WFC 스크립트(wfc_fill.py)에서 옮김. 은행 세트 다섯 번째(비교군은 S&P500 은행 13곳, BAC 본인 제외).
 — clone + 배열 뒤에 실행. 데이터: v2/BAC_bank.json(adapters/bank_card.py).
Claude 추천 결정(사용자 위임, 리뷰 때 확인): 보통주·유형 보통주 자본은 보도자료 회사 값(research/bank_equity_override.json, 우선주 태그 없음), 배당 현금 태그 DIV_COM_TAGS.
G5(2025년 4분기 순이익 — 회계 방식 변경 재작성으로 XBRL 7,200 대 보도자료 7,319)는 처음(10-01) 미통과 → 참고용 → 판정 보류였으나,
2026-10-05 관문 보정(사전 등록 9-2 — 회사가 공시한 재작성 몫)으로 통과 → 초과이익모형이 표를 준다 → 적정~고평가(−1).
기반(base/bac_base.html)은 2026-10-05 지금 NVDA 틀을 `clone_card.py BAC --force`로 복제하고 `bac_arrays.py <그때 v2 카드 사본>`으로 그 카드의
배열(마지막 봉 2026-09-30)을 넣어 만들었다. 이 기반 + 그때의 BAC_bank.json·peer_universe/banks.json(e1886df)으로 채우기 → unify_js.py →
sync_fallbacks.py를 돌리면 e1886df 카드가 그대로 나온다. 은행 카드가 받지 않은 틀 변경은 6절에서 되돌린다(jpm_fill.py와 같은 방식)."""
import json, os, re, sys
os.chdir('/Users/watermountain/Workspace/stock-widgets-preview/v2')
sys.path.insert(0, '.'); sys.path.insert(0, 'adapters')
import build_multiple_history as bmh
import bank_rim as br

T, CIK = 'BAC', '0000070858'
p = 'BAC_full_widget.html'; h = open(p, encoding='utf-8').read()


def one(o, n):
    global h
    c = h.count(o); assert c == 1, (c, o[:100]); h = h.replace(o, n)


def sub(pat, new, flags=re.S):
    global h
    m = list(re.finditer(pat, h, flags)); assert len(m) == 1, (len(m), pat[:90])
    h = h[:m[0].start()] + (new(m[0]) if callable(new) else new) + h[m[0].end():]


J = json.load(open('BAC_bank.json'))
R = J['rim']; SH = J['self']; PEER = J['peer']; FB = SH['fairBand']
assert J['gates'] == {'G1': True, 'G2': True, 'G5': True, 'G3': True, 'G4': True}, J['gates']; assert not R['reference_only']   # 2026-10-05 관문 보정 뒤
D = json.loads(re.search(r'const BAC_DAILY\s*=\s*(\[.*?\]);', h, re.S).group(1)); days = {r[0] for r in D}
px, asof = D[-1][4], D[-1][0]
assert abs(px - J['price']) < 1e-6 and asof == J['asOf']
bank = br.Bank(T, CIK, overrides=True)
S_, CE = R['shares'], R['ce']


def q(tags):
    _, rows = bmh.pick_tag(CIK, tags)
    return {e['end']: e['val'] for e in bmh.quarterly_flow(rows, T)}


rev = q(['Revenues']); ni = q(['NetIncomeLossAvailableToCommonStockholdersBasic'])
nie = q(['NoninterestExpense']); prov = {'2026-06-30': 1366e6, '2026-03-31': 1337e6, '2025-06-30': 1592e6}   # 보도자료 'Provision for credit losses'(분기 표준 태그 없음, MS와 같이 손입력)
nii = q(['InterestIncomeExpenseNet']); nii = q(['InterestIncomeExpenseNet'])
# 2025-12 회계 방식 변경 재작성 — 2Q25~2Q26은 2Q26 보도자료(재작성 기준) 분기 값으로 맞춘다. SEC 데이터의 4Q25는 재작성 연간 − 원래 9개월이라
# $31.2B·$7.2B로 섞였고, 2Q25는 원공시라 전년 대비가 부풀었다(Codex·Fable). 2025년 1분기 이전은 원공시 그대로(차트 각주에 적음).
for _e, _r, _n, _x, _i in [('2025-06-30', 27443, 6879, 17183, 14670), ('2025-09-30', 29040, 7903, 17337, 15233), ('2025-12-31', 28367, 7319, 17437, 15750),
                           ('2026-03-31', 30272, 8155, 18531, 15745), ('2026-06-30', 31558, 8748, 18627, 15997)]:
    rev[_e], ni[_e], nie[_e], nii[_e] = _r * 1e6, _n * 1e6, _x * 1e6, _i * 1e6
ks = sorted(k for k in rev if k <= '2026-06-30')[-8:]
cur, yo, qo = ks[-1], ks[-5], ks[-2]
assert (cur, yo, qo) == ('2026-06-30', '2025-06-30', '2026-03-31'), ks
assert round(ni[cur] / 1e6) == 8748 and round(rev[cur] / 1e6) == 31558 and round(nie[cur] / 1e6) == 18627   # 보도자료 보통주 귀속 순이익·순수익
r1 = lambda v: round(v / 1e9, 1)
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
roe_q = [round(bank.roe(k)[0] * 100, 1) for k in ks]
SEC = 'https://www.sec.gov/Archives/edgar/data/70858/'
PR = {'q2': SEC + '000007085826000353/bac06302026ex991.htm', 'q2s': SEC + '000007085826000353/bac06302026ex992.htm',
      'q1': SEC + '000007085826000222/bac03312026ex991.htm', 'q4': SEC + '000007085826000020/bac12312025ex991.htm',
      'q3': SEC + '000007085825000390/bac093025ex991.htm'}
DIV = SEC + '000007085826000364/exhibit991.htm'
ACCT = SEC + '000007085826000011/a162026tax-relatedequityin.htm'   # 세금 관련 지분투자 회계 방식 변경 재작성
TENQ = PR['q2s']
f1 = lambda v: f'{v * 100:.1f}%'

# ── 1. 헤더 ──
one('<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +110%)</span>',
    f'<span class="meta-label">현재가 요구 ROE (5년 · 최근 4분기 {f1(R["roe0"])})</span>')
one('id="bacFairBand" style=', f'id="bacFairBand" title="최근 1년 PER 25~75% 구간({FB["per_p25"]:.1f}~{FB["per_p75"]:.1f}배) × 최근 4분기 EPS로 낸 PER만의 범위다(10달러 단위로 반올림하면 양 끝이 같아져 1달러 단위로 표시). 판정은 P/TBV·PER 두 배수와 초과이익모형을 함께 보므로 이 범위와 따로 읽는다. 지금 PER({SH["per"]["current"]:.1f}배)이 1년 구간 아래라 현재가가 범위보다 낮다." style=')
_eps = px / SH['per']['current']; _lo, _hi = FB['per_p25'] * _eps, FB['per_p75'] * _eps
h = re.sub(r'(id="bacFairBand"[^>]*>)[^<]*(</span>)', lambda m: m.group(1) + f'${_lo:.0f} ~ ${_hi:.0f}' + m.group(2), h, count=1)   # 10달러 단위면 $60 ~ $60이라 1달러 단위(카드 한정)
one('<button class="ma-toggle-btn ma-off" data-ma="dcf" style="color:#38bdf8;border-color:#38bdf8;">◆ DCF 시나리오</button>',
    '<button class="ma-toggle-btn ma-off" data-ma="dcf" style="color:#38bdf8;border-color:#38bdf8;" hidden>◆ DCF 시나리오</button>')

# ── 2. 내재가치(RIM) 상수·격자·문장 ──
dcf = {"low": round(R['보수'], 2), "base": round(R['기본'], 2), "high": round(R['낙관'], 2), "requiredGrowth": R['required_roe'],
       "baseEquivGrowth": None, "reqMode": "roe", "requiredMargin": None, "marginNow": None, "roeNow": R['roe0'],
       "growth5y": None, "nonopPerShare": 0, "s2cFallback": False, "asOf": asof, "hard": (["b0"] if R["b"] == 0 else []), "hardDetail": {}, "tvShare": None,
       "model": "rim", "retention": R['b'], "bvps": R['bvps'], "referenceOnly": R['reference_only']}   # 관문 보정(10-05) 뒤 False — 참고용 JS는 남겨 둔다
sub(r'^const BAC_DCF = \{.*$', 'const BAC_DCF = ' + json.dumps(dcf, ensure_ascii=False) + ';   // 초과이익모형 — adapters/bank_card.py, research/bank_rim_prereg.md', re.M)
ends = {'보수': R['roe_5y_median'], '기본': R['roe_2y_median'], '낙관': R['roe0']}
waccs, lams = [0.08, 0.09, 0.10, 0.11, 0.12], [0.0, 0.5, 1.0]
vals = {n: [[round(br.rim_value(CE, R['roe0'], e, R['b'], r, lam) / S_, 2) if br.rim_value(CE, R['roe0'], e, R['b'], r, lam) else None
             for r in waccs] for lam in lams] for n, e in ends.items()}
grid = {"waccs": waccs, "terms": lams, "default": [0.10, 0.5], "values": vals, "kind": "rim"}
sub(r'^const BAC_DCF_GRID = \{.*$', 'const BAC_DCF_GRID = ' + json.dumps(grid, ensure_ascii=False) + ';   // 자기자본비용 × 잔존 수렴 비율(λ)', re.M)
sub(r'const BAC_DCF_TRACK = \[.*?\];', 'const BAC_DCF_TRACK = [];')
one('<div class="section-title">내재가치 (DCF) — 현금흐름이 말하는 가격</div>\n  <div class="lede">회사가 앞으로 벌어들일 현금만으로 계산한 주당 가치다.</div>',
    '<div class="section-title">내재가치 (초과이익모형) — 자본이 버는 초과이익이 말하는 가격</div>\n  <div class="lede">은행은 현금흐름 모델 대신 장부가치에 자기자본비용(10%)을 넘는 이익의 현재가치를 더해 계산한다.</div>')
new = [f'ROE가 최근 4분기 {f1(R["roe0"])}에서 5년 중앙값 {f1(R["roe_5y_median"])}로 내려간다.',
       f'ROE가 최근 4분기 {f1(R["roe0"])}에서 최근 2년 중앙값 {f1(R["roe_2y_median"])}로 내려간다.',
       f'ROE {f1(R["roe0"])}가 5년 동안 이어진다.']
olds = re.findall(r'<td class="story">(지난 5년 성장 속도의 절반.*?|지난 5년의 성장 속도로.*?|최근 3년의 성장 속도로.*?)</td>', h)
assert len(olds) == 3
for o, n in zip(olds, new):
    assert h.count(o) == 1; h = h.replace(o, n)
one('<div class="note">세 값은 확률이 아니라, 과거 실적에서 서로 다른 가정을 뽑아 계산한 결과다.</div>',
    f'<div class="note">세 값은 확률이 아니라, 과거 ROE에서 서로 다른 가정을 뽑아 계산한 결과다. 5년 뒤 ROE는 자기자본비용 쪽으로 절반 수렴한다고 본다(수렴 없음이면 기본 ${vals["기본"][0][2]:.0f}, 완전 수렴이면 ${vals["기본"][2][2]:.0f}). 값을 더 크게 바꾸는 것은 자기자본비용이다(8%면 ${vals["기본"][1][0]:.0f}, 12%면 ${vals["기본"][1][4]:.0f}). 유보율 {f1(R["b"])}(최근 4분기 배당·자사주 환원 뒤 남는 몫)로 장부가 자라고, 기타포괄손익은 반영하지 않는다.' + (f' 5년 중앙값 ROE({f1(R["roe_5y_median"])})가 2년 중앙값({f1(R["roe_2y_median"])})보다 조금 높아 보수가 기본보다 높게 나온다(이름과 순서가 뒤집힘).' if R['보수'] > R['기본'] else '') + '</div>')
one("    ['현금흐름', lv.label in DV ? DV[lv.label] : null, lv.label, 2],",
    "    ['초과이익', lv.label in DV && !D.referenceOnly ? DV[lv.label] : null, D.referenceOnly ? '참고용' : lv.label, 2],   // G5 미통과 → 참고용·기권(사전 등록 7-7)")
one("    dv.textContent = lv.label + (lv.split ? ' · 갈림' : '');",
    "    dv.textContent = d.referenceOnly ? '참고용 · 기권' : lv.label + (lv.split ? ' · 갈림' : '');   // G5 미통과(사전 등록 7-7)")
one("    pill('dcf', lv.cls, lv.label + (lv.split ? ' · 갈림' : ''));", "    pill('dcf', D.referenceOnly ? 'mid' : lv.cls, D.referenceOnly ? '참고용 · 기권' : lv.label + (lv.split ? ' · 갈림' : ''));   // G3 미통과(카드 한정)")
one('<div class="note" data-dcf-nonop>기본 시나리오 $314 = 사업 가치 $310 + 비영업 자산 $4(주당, 지분·장기투자)</div>', '<div class="note" data-dcf-nonop hidden></div>')
sub(r'<div class="reverse">.*?</div>\n  </div>', '<div class="reverse" data-rim-reverse>지금 가격이 정당하려면 5년 동안 ROE가 매년 <b data-dcf-req>—</b>여야 한다.</div>\n  </div>')
one('<div class="knob"><span class="knob-l">영구성장 <span class="knob-d" data-knob-default="term">(2.5%)</span></span>',
    '<div class="knob"><span class="knob-l">잔존 수렴 <span class="knob-d" data-knob-default="term">(절반)</span></span>')
one('<div class="knob"><span class="knob-l">할인율 <span class="knob-d" data-knob-default="wacc">(10%)</span></span>',
    '<div class="knob"><span class="knob-l">자기자본비용 <span class="knob-d" data-knob-default="wacc">(10%)</span></span>')
# 헤더·요약·탭 JS — ROE 모드(은행). 다른 카드는 reqMode가 'roe'가 아니라 동작 불변.
one("""  if (req) req.textContent = noSol ? '연 ' + f1(d.requiredGrowth)
                           : mMode ? (d.requiredMargin != null ? f1(d.requiredMargin) : '—')
                                   : '연 ' + f1(d.requiredGrowth);""",
    """  const roeMode = d.reqMode === 'roe';   // 은행 초과이익모형 — 요구 ROE(research/bank_rim_prereg.md)
  if (req) req.textContent = roeMode ? (d.requiredGrowth != null ? 'ROE ' + f1(d.requiredGrowth) : '해 없음')
                           : noSol ? '연 ' + f1(d.requiredGrowth)
                           : mMode ? (d.requiredMargin != null ? f1(d.requiredMargin) : '—')
                                   : '연 ' + f1(d.requiredGrowth);""")
one("""    if (cell) cell.title = (mMode""",
    """    if (cell) cell.title = roeMode ? `현재가 $${price.toFixed(2)} 가 정당화되려면 5년 동안 ROE가 ${d.requiredGrowth != null ? f1(d.requiredGrowth) : '(범위 밖)'}여야 한다(최근 4분기 ${f1(d.roeNow)}).`
      + `\\n현재가 ÷ 내재가치 $${Math.round(d.base)} = ${lv.ratio != null ? lv.ratio.toFixed(2) : '—'} → ${lv.label} (${DCF_RULE_TEXT})` : (mMode""")
one("""  if (box)  box.innerHTML = (d.base > 0 ? '$' + (Math.abs(d.base) < 10 ? d.base.toFixed(2) : Math.round(d.base)) : '0 이하')
    + '<span class="logic-denom"> · 보수 ' + (d.low > 0 ? '$' + (d.low < 10 ? d.low.toFixed(2) : Math.round(d.low)) : '계산 불가')
    + ' · 낙관 ' + (d.high > 0 ? '$' + (d.high < 10 ? d.high.toFixed(2) : Math.round(d.high)) : '계산 불가') + '</span>';""",
    """  const lowW = roeMode ? '보수' : '낮은 성장', highW = roeMode ? '낙관' : '높은 성장';
  if (box)  box.innerHTML = (d.base > 0 ? '$' + (Math.abs(d.base) < 10 ? d.base.toFixed(2) : Math.round(d.base)) : '0 이하')
    + '<span class="logic-denom"> · ' + lowW + ' $' + Math.round(d.low)
    + ' · ' + highW + ' $' + Math.round(d.high) + '</span>';""")
one("""  fill('[data-dcf-req]', (D.requiredGrowth * 100).toFixed(1) + '%');""",
    """  fill('[data-dcf-req]', D.requiredGrowth != null ? (D.requiredGrowth * 100).toFixed(1) + '%' : '해 없음');""")
one("""    term: G.terms.map(t => +(t * 100).toFixed(1) + '%'),""",
    """    term: G.kind === 'rim' ? G.terms.map(t => ({0: '수렴 없음', 0.5: '절반', 1: '완전'})[t]) : G.terms.map(t => +(t * 100).toFixed(1) + '%'),""")
one("""    el.textContent = '(' + +(v * 100).toFixed(1) + '%)';""",
    """    el.textContent = G.kind === 'rim' && el.dataset.knobDefault === 'term' ? '(절반)' : '(' + +(v * 100).toFixed(1) + '%)';""")

# ── 3. 점수 상수 · 기본적 분석 · 활동성 ──
selfscore = round((SH['ptbv']['score'] + SH['per']['score']) / 2, 1)
peerscore = round((PEER['ptbv']['score'] + PEER['per']['score']) / 2, 1)
sub(r'const BAC_SCORES = \{.*?\n\};', f'''const BAC_SCORES = {{
  fundamental: null,   // 은행 — 일반 재무비율 산식이 맞지 않아 매기지 않는다
  peer: {peerscore},          // S&P500 은행 대비 P/TBV·PER 순위 평균(표시용). 표는 두 배수가 같은 방향일 때만
  selfHistory: {selfscore},   // P/TBV·PER 자기 5년 백분위 평균(표시용)
  asOf: "{asof}",
  fundamentalAsOf: "2026-06-30",   // Q2 2026 10-Q (2026-07-31 공시)
}};''')
sub(r'// 기본적 분석이 98\.1이 아니라 96\.1인 이유\..*?// `--basis annual`로 돌리면 98\.1이 그대로 나온다 — 배점을 안 건드렸다는 확인이다\.\n', '')
F_ = bmh._facts(CIK)['facts']['us-gaap']
def _ann(tag):
    from datetime import date as _d
    out = {}
    for x in F_[tag]['units']['USD']:
        if x.get('form') == '10-K' and 'start' in x and x['end'].endswith('12-31') and 350 <= (_d.fromisoformat(x['end']) - _d.fromisoformat(x['start'])).days <= 380:
            if x['end'] not in out or x['filed'] < out[x['end']][1]:
                out[x['end']] = (x['val'], x['filed'])
    return {k: v[0] for k, v in out.items()}
_rv, _ni = _ann('Revenues'), _ann('NetIncomeLossAvailableToCommonStockholdersBasic')
CAGR_REV = ((_rv['2025-12-31'] / _rv['2020-12-31']) ** (1 / 5) - 1) * 100   # FY2020 → FY2025
CAGR_NI = ((_ni['2025-12-31'] / _ni['2020-12-31']) ** (1 / 5) - 1) * 100
NM_TTM = sum(ni[k] for k in ks[-4:]) / sum(rev[k] for k in ks[-4:]) * 100
LI = {x['end']: x['val'] for x in F_['Liabilities']['units']['USD']}; SE = {x['end']: x['val'] for x in F_['StockholdersEquity']['units']['USD']}
A = {x['end']: x['val'] for x in F_['Assets']['units']['USD']}
NA = '해당 없음'
frow = lambda m, lab, unit, v=None, note=None: {"metric": m, "label": lab, "unit": unit, "value": v, "points": None, "note": note}
fund = {"ticker": T, "basis": "quarter", "asOf": "2026-06-30", "filedAt": "2026-07-31", "score": None, "grade": None, "qualityFlags": ["financial"],
        "axes": {"health": {"rows": [frow("currentRatio", "유동비율", "%", note=NA), frow("quickRatio", "당좌비율", "%", note=NA),
                                     frow("debtDependency", "차입금의존도", "%", note=NA), frow("interestCoverage", "이자보상배율", "x", note=NA),
                                     frow("debtToEquity", "부채비율", "%", LI['2026-06-30'] / SE['2026-06-30'] * 100)], "points": None, "max": 33},
                 "growthProfit": {"rows": [frow("revenueCagr", "매출 CAGR", "%", CAGR_REV), frow("opIncomeCagr", "순이익 CAGR", "%", CAGR_NI, "은행은 영업이익 대신 보통주 귀속 순이익"),
                                           frow("opMargin", "영업이익률(OPM)", "%", note=NA), frow("netMargin", "순이익률", "%", NM_TTM)], "points": None, "max": 34}},
        "note": "은행 — 예금이 부채라 유동·차입 비율이 뜻이 없고 v1 모델도 은행을 채점하지 않는다", "netCash": None}
sub(r'^const BAC_FUNDAMENTAL = \{.*$', 'const BAC_FUNDAMENTAL = ' + json.dumps(fund, ensure_ascii=False) + ';', re.M)
act = {"ticker": T, "status": "na", "reason": "은행이라 매출채권·재고 회전으로 운영 효율을 판정하지 않는다"}
sub(r'^const BAC_ACTIVITY = \{.*$', 'const BAC_ACTIVITY = ' + json.dumps(act, ensure_ascii=False) + ';', re.M)
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
one('분기 매출 / 순이익 / 영업이익률 (Q3 FY25~Q2 FY27)', '분기 순영업수익 / 순이익 / ROE (Q3 2024~Q2 2026)')
sub(r'const revenue=\[[^\]]*\];', 'const revenue=' + json.dumps([r1(rev[k]) for k in ks]).replace(' ', '') + ';')
sub(r'const netIncome=\[[^\]]*\];', 'const netIncome=' + json.dumps([r1(ni[k]) for k in ks]).replace(' ', '') + ';')
sub(r'const opm=\[[^\]]*\];', 'const opm=' + json.dumps(roe_q).replace(' ', '') + ';')
one('const y2min=40, y2max=75;', 'const y2min=0, y2max=25;')
one("labels:['Q3 FY25','Q4 FY25','Q1 FY26','Q2 FY26','Q3 FY26','Q4 FY26','Q1 FY27','Q2 FY27'],", 'labels:[' + ','.join(f"'{x}'" for x in L8) + '],')
one("{type:'line',label:'OPM(%)',", "{type:'line',label:'ROE(최근 4분기, GAAP, %)',")
one("{type:'bar',label:'매출($B)',", "{type:'bar',label:'순영업수익($B)',")
one("{type:'bar',label:'순이익($B)',", "{type:'bar',label:'순이익($B, 보통주 귀속)',")
for lab, nl, val, subt in [('FCF', 'CET1 비율 (Q2 2026)', '11.2%', '표준방식 · 1분기 11.2%'),
                           ('Capex', '대손비용 (Q2 2026)', f'${prov[cur] / 1e9:.2f}B', f'1년 전 ${prov[yo] / 1e9:.2f}B · 순상각 $1.4B'),
                           ('R&amp;D', '순이자이익 (Q2 2026)', f'${nii[cur] / 1e9:.1f}B', f'전년 대비 {(nii[cur] / nii[yo] - 1) * 100:+.0f}%')]:
    sub(rf'<div class="stat-label">{lab} \(Q2 FY27\)</div>\n      <div class="stat-value">[^<]*</div>\n      <div class="stat-sub">[^<]*</div>',
        f'<div class="stat-label">{nl}</div>\n      <div class="stat-value">{val}</div>\n      <div class="stat-sub">{subt}</div>')
sub(r'<div class="stat-value">11월 중순 예상</div>\n      <div class="stat-sub">일정 · Q3 FY27</div>',
    '<div class="stat-value">10월 중순 예상</div>\n      <div class="stat-sub">일정 · Q3 2026</div>')
one('재무 건전성 — 안정성·활동성 (Q2 FY27 · 2026.07.26 기준)', '재무 건전성 — 안정성·활동성 (Q2 2026 · 2026.06.30 기준)')
sub(r'<span id="fundHealthAxis">[^<]*</span>', '<span id="fundHealthAxis">점수 없음</span>')
sub(r'<div class="title" id="fundHealthTitle">[^<]*</div>', '<div class="title" id="fundHealthTitle">종합 진단: 판정하지 않음 — 은행이라 점수를 매기지 않는다</div>')
one('<div class="diag-summary" id="fundHealthSummary">', '<div class="diag-summary watch" id="fundHealthSummary">')
one('<span>안정성 상세 — 개별 비율 7개</span>', '<span>안정성 상세 — 개별 비율 7개 · 은행 자본 지표</span>')
a1, a0 = A['2025-12-31'], A['2024-12-31']
sub(r'<span class="diag-label">총자산증가율</span><span class="diag-value">[^<]*</span><span class="diag-note">[^<]*</span>',
    f'<span class="diag-label">총자산증가율</span><span class="diag-value">+{(a1 / a0 - 1) * 100:.1f}%</span><span class="diag-note">FY25 ${a1 / 1e12:.2f}T(전기 ${a0 / 1e12:.2f}T) · 연간 지표, FY26 마감 전까지 동일</span>')
sub(r'<span class="diag-value" id="fundNetCashPs">[^<]*</span><span class="diag-note" id="fundNetCashNote">[^<]*</span>',
    '<span class="diag-value" id="fundNetCashPs">해당 없음</span><span class="diag-note" id="fundNetCashNote">은행은 예금·차입이 영업 자금이라 순현금을 따지지 않는다</span>')
xrow = lambda lab, val, note: (f'      <div class="diag-row">\n        <div class="diag-left"><span class="diag-label">{lab}</span><span class="diag-value">{val}</span>'
                               f'<span class="diag-note">{note}</span></div>\n        <div class="diag-badge info">ℹ️ 참고</div>\n      </div>\n')
extra = (xrow('CET1 비율 (표준방식)', '11.2%', 'CET1 자본 $201.6B ÷ 위험가중자산 $1,793B · 6월 말 기준, 2026.07.14 보도자료')
         + xrow('주당 장부가치 (BVPS)', '$39.34', '1년 전 $36.92(새 회계 방식으로 재작성한 값) 대비 +6.6% · 회사 발표')
         + xrow('주당 유형 장부가치 (TBVPS)', '$29.37', '1년 전 $27.49(재작성) 대비 +6.8% · 회사 발표(카드의 P/TBV 분모와 같다)'))
sub(r'(<span class="diag-note" id="fundNetCashNote">[^<]*</span></div>\n        <div class="diag-badge info">ℹ️ 참고</div>\n      </div>\n)', lambda m: m.group(1) + extra)
sub(r'<div style="margin-top:14px;font-size:11\.5px;color:var\(--text2\);line-height:1\.6;">유동비율·당좌비율.*?</div>',
    f'<div style="margin-top:14px;font-size:11.5px;color:var(--text2);line-height:1.6;">은행은 예금이 부채라 유동·당좌·차입 비율과 이자보상배율이 뜻이 없어 해당 없음으로 두고, 규제자본 비율과 장부가치를 대신 싣는다. 부채비율 {LI['2026-06-30'] / SE['2026-06-30'] * 100:,.0f}%는 예금 약 $2.0조를 포함한 값이다. CET1 비율 11.2%는 1분기와 같고 1년 전(11.5%)보다 조금 낮다. 분기 차트는 2025년 2분기부터 재작성 기준(보도자료), 그 전은 원공시 값이다. 2025년 4분기에 세금 관련 지분투자의 회계 방식을 바꿔 과거 장부가치가 재작성됐다(2026-01-06 8-K).</div>')
vec = lambda e: [r1(rev[e]), r1(rev[e] - nie[e]), r1(ni[e]), r1(prov[e])]
f = lambda a, b: '%+.1f%%' % ((a / b - 1) * 100)
yd = [f(rev[cur], rev[yo]), f(rev[cur] - nie[cur], rev[yo] - nie[yo]), f(ni[cur], ni[yo]), f(prov[cur], prov[yo])]
qd = [f(rev[cur], rev[qo]), f(rev[cur] - nie[cur], rev[qo] - nie[qo]), f(ni[cur], ni[qo]), f(prov[cur], prov[qo])]
tq = lambda a: ', '.join(f"'{x}'" for x in a)
sub(r"curLabel: 'Q2 FY27', cmpLabel: 'Q2 FY26',\n    titleSuffix: '[^']*',\n    chart: \{ cur: \[[^\]]*\], cmp: \[[^\]]*\] \},\n    deltas: \[[^\]]*\],",
    f"curLabel: 'Q2 2026', cmpLabel: 'Q2 2025',\n    titleSuffix: 'YoY (Q2 2026 vs Q2 2025)',\n    chart: {{ cur: {vec(cur)}, cmp: {vec(yo)} }},\n    deltas: [{tq(yd)}],")
sub(r"curLabel: 'Q2 FY27', cmpLabel: 'Q1 FY27',\n    titleSuffix: '[^']*',\n    chart: \{ cur: \[[^\]]*\], cmp: \[[^\]]*\] \},\n    deltas: \[[^\]]*\],",
    f"curLabel: 'Q2 2026', cmpLabel: 'Q1 2026',\n    titleSuffix: 'QoQ (Q2 2026 vs Q1 2026)',\n    chart: {{ cur: {vec(cur)}, cmp: {vec(qo)} }},\n    deltas: [{tq(qd)}],")
fn = lambda a, extra='': (f"footnote: '기준일: 2026.06.30(Q2 2026) vs {a} · GAAP · 충당금 전 이익 = 순영업수익 − 비이자비용 · 순이익은 보통주 귀속 · 대손비용은 늘면 나쁘다 · {extra}"
                f"<a href=\"{PR['q2']}\" target=\"_blank\" rel=\"noopener\">Bank of America Q2 2026 실적 보도자료 (SEC 8-K) →</a>'")
sub(r"footnote: '기준일: 2026\.07\.26\(Q2 FY27\) vs 2025\.07\.27\(Q2 FY26\)[^\n]*'", fn('2025.06.30(Q2 2025)', '1년 전 값은 재작성 기준(2026-07-14 보도자료) · '))
sub(r"footnote: '기준일: 2026\.07\.26\(Q2 FY27\) vs 2026\.04\.26\(Q1 FY27\)[^\n]*'", fn('2026.03.31(Q1 2026)'))
one('<span id="fundPeriodTitle">YoY (Q2 FY27 vs Q2 FY26)</span>', '<span id="fundPeriodTitle">YoY (Q2 2026 vs Q2 2025)</span>')
one("        labels: ['매출', '영업이익', '순이익', 'FCF'],", "        labels: ['순영업수익', '충당금 전 이익', '순이익', '대손비용'],")
one('// FCF = 영업현금흐름 − PaymentsToAcquireProductiveAssets, 분기값은 누적값의 차이.',
    '// 은행: 순영업수익 · 충당금 전 이익(순영업수익 − 비이자비용) · 보통주 귀속 순이익 · 대손비용, 분기값은 누적값의 차이.')
SEG = [('소비자 금융', 11336, '#e31837'), ('글로벌 마켓', 8022, '#012169'), ('자산관리(GWIM)', 6871, '#5aa9e6'), ('기업금융(Global Banking)', 6236, '#94a3b8')]
tot = sum(v for _, v, _ in SEG); assert tot - 744 - 163 == round(rev[cur] / 1e6), tot   # 기타(All Other) −$744M, 과세 상당(FTE) 조정 $163M 차감 전
leg = ''.join(f'\n          <div style="display:flex;align-items:center;gap:7px;font-size:11px;color:var(--text2);white-space:nowrap;"><span style="width:8px;height:8px;border-radius:50%;background:{c};display:inline-block;flex-shrink:0;"></span>{n} <strong style="color:var(--text);">${v / 1000:.1f}B · {v / tot * 100:.1f}%</strong></div>' for n, v, c in SEG)
sub(r'<div class="card-title">매출 구성 — Market Platform.*?</div>\n\n      <div style="display:flex;align-items:center;justify-content:center;gap:20px;">.*?\n      </div>\n\n      <div class="yoy-footnote" style="margin-top:14px;">.*?</div>',
    '<div class="card-title">순수익 구성 — 사업부별 (Q2 2026 · 2026.06.30 기준)</div>\n\n      <div style="display:flex;align-items:center;justify-content:center;gap:20px;">\n        <div class="chart-wrap" style="height:170px;width:170px;flex-shrink:0;">\n          <canvas id="segmentPieChart"></canvas>\n        </div>\n        <div style="display:flex;flex-direction:column;gap:9px;">' + leg +
    f'\n        </div>\n      </div>\n\n      <div class="yoy-footnote" style="margin-top:14px;">과세 상당(FTE) 기준, 기타 부문 −$0.74B 차감 전 · 1년 전보다 소비자 금융 +5%, 글로벌 마켓 +34%, 자산관리 +16%, 기업금융 +10% · 출처: <a href="{PR["q2"]}" target="_blank" rel="noopener">Bank of America Q2 2026 실적 보도자료 (SEC 8-K) →</a></div>')
sub(r'// ─── 매출 구성 도넛 차트 \([^)]*\) ───', '// ─── 순수익 구성 도넛 차트 (부문 4개, 기타·FTE 조정 차감 전, 백만 달러) ───')
one('const total = 96221;', f'const total = {tot};')
one("labels:['Hyperscale','AI Clouds·Industrial·Enterprise','Edge Computing'],", 'labels:' + json.dumps([n for n, _, _ in SEG], ensure_ascii=False) + ',')
one('data:[48710, 40313, 7198],', 'data:[' + ', '.join(str(v) for _, v, _ in SEG) + '],')
sub(r"backgroundColor:\['#[0-9a-fA-F]{6}','#4d7a00','#3498db'\],", 'backgroundColor:' + json.dumps([c for _, _, c in SEG]) + ',')
R_payout = bank.payout_ttm(cur)[0] / bank.ni_ttm(cur)[0]
G_PAY = json.load(open('research/bank_gate_BAC.json'))['quarters']['2026-06-30']['net_payout_ltm']
CAPA = f"""<div class="card-title">자본배분 · 주주환원 (Q2 2026 · 2026.06.30 기준)</div>
      <div class="zone-list">
        <div class="zone-item">
          <span class="zone-label">자사주 매입 (Q2 2026)</span>
          <span class="zone-val">$6.0B</span>
        </div>
        <div class="zone-item">
          <span class="zone-label">보통주 배당 (Q2 2026, 분기 $0.28)</span>
          <span class="zone-val">$2.0B</span>
        </div>
        <div class="zone-item">
          <span class="zone-label">분기 배당 인상 (7월 24일 발표)</span>
          <div style="display:flex;align-items:center;gap:8px;">
            <span class="zone-tag" style="background:rgba(240,192,64,0.18);color:var(--gold);">$0.28 → $0.32</span>
            <span class="zone-val">+14%</span>
          </div>
        </div>
        <div class="zone-item">
          <span class="zone-label">최근 4분기 환원율 (보도자료 자사주 + 배당 총액 ÷ 보통주 순이익)</span>
          <span class="zone-val">{G_PAY * 100:.0f}%</span>
        </div>
      </div>
      <div class="yoy-footnote" style="margin-top:14px;">순이익과 비슷하거나 많이 돌려줘 유보율이 0이다(초과이익모형 입력 b = 0) · 기말 주식 수는 1년 새 4.2억 주 줄었다 · 출처: <a href="{PR['q2']}" target="_blank" rel="noopener">Q2 2026 보도자료 (SEC 8-K) →</a> · <a href="{DIV}" target="_blank" rel="noopener">배당 인상 (SEC 8-K)</a></div>
    </div>"""
sub(r'<div class="card-title">자본배분 · 주주환원 \(Q2 FY27 · 2026\.07\.26 기준\)</div>\n      <div class="zone-list">.*?\n      </div>\n    </div>', CAPA)
CHK = """<div class="card-title">다음 실적 체크포인트 <span style="color:var(--gold);font-weight:600;">2026년 10월 중순 (예상) · Q3 2026</span></div>
    <div style="font-size:12px;color:var(--text2);line-height:1.8;">
      <div style="margin-bottom:8px;"><strong style="color:var(--accent2);">①</strong> ROTCE가 2분기 17.0%(1분기 16.0%) 수준을 지키는지</div>
      <div style="margin-bottom:8px;"><strong style="color:var(--accent2);">②</strong> 순이자이익(2분기 $16.0B, +9%)과 대출(+8%)·예금(+2%) 증가</div>
      <div style="margin-bottom:8px;"><strong style="color:var(--accent2);">③</strong> 글로벌 마켓 순수익(2분기 +34%)이 시장 활동이 가라앉아도 버티는지</div>
      <div><strong style="color:var(--accent2);">④</strong> CET1 11.2%에서 자사주 매입 속도(2분기 $6.0B)와 3분기 배당 $0.32</div>
    </div>"""
sub(r'<div class="card-title">다음 실적 체크포인트 <span[^>]*>[^<]*</span></div>\n    <div style="font-size:12px;color:var\(--text2\);line-height:1\.8;">.*?\n    </div>', CHK)

# ── 4. 밸류에이션 ──
one('<div class="vc-head">PBR</div>', '<div class="vc-head">P/TBV</div>')
one('<div class="vs-name" title="지난 5년 BAC 자신의 배수보다 지금이 얼마나 낮은가. 높을수록 싸다.">자기 이력 대비</div>',
    '<div class="vs-name" title="지난 5년 BAC 자신의 배수보다 지금이 얼마나 낮은가. 높을수록 싸다. 은행 규칙에 따라 P/TBV·PER 두 배수가 모두 70 이상이면 +1, 모두 30 미만이면 −1이다.">자기 이력 대비</div>')
one('<div class="vs-name" title="회사가 앞으로 벌어들일 현금만으로 계산한 주당 가치(기본 시나리오).">현금흐름 (내재가치)</div>',
    '<div class="vs-name" title="은행은 초과이익모형(장부가치 + 자기자본비용 10%를 넘는 이익의 현재가치)으로 계산한다. 기본 시나리오.">초과이익 (내재가치)</div>')
one('<span class="logic-tag">내재가치 <span class="logic-denom">현금흐름</span></span>', '<span class="logic-tag">내재가치 <span class="logic-denom">초과이익</span></span>')
one('<div class="vs-name" title="같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.">동종업 대비</div>',
    '<div class="vs-name" title="S&P500 은행(대형·지역) 대비 P/TBV·PER 순위. 높을수록 싸다. 두 배수가 같은 방향일 때만 표를 준다.">동종업 대비</div>')
sub(r'<div class="vs-note">현재가 <span data-vs="price">[^<]*</span> 대비 <strong data-vs="upside">[^<]*</strong> · 기본 시나리오</div>',
    '<div class="vs-note">현재가 <span data-vs="price">—</span> 대비 <strong data-vs="upside">—</strong> · 초과이익모형 기본</div>')
one('<span class="val-name">PBR <span class="hist-note" data-hist="note"></span></span>', '<span class="val-name">P/TBV (유형 장부) <span class="hist-note" data-hist="note"></span></span>')
a_ = h.index('    </div>\n\n    <div class="card" style="display:flex;flex-direction:column;">')
h = h[:a_] + ('      <div style="font-size:11px;color:var(--text3);line-height:1.6;margin-top:6px;">은행은 매출·현금흐름·EBITDA 배수가 뜻이 없어 P/TBV·PER 두 배수만 본다. P/TBV는 보통주 자본에서 영업권·무형자산을 뺀 유형 장부가치 기준(회사 발표 TBVPS와 같다). '
              'BAC는 보통주 자본·유형 보통주 자본을 회사가 실적 보도자료에 밝힌 값으로 쓴다(SEC 표준 데이터에 우선주 잔액이 없어 회사 값을 다시 만들 수 없어서다).</div>\n') + h[a_:]
wm = lambda k, m: {"metric": k, "score": round(m['score'], 1), "percentile": round(m['percentile'], 1), "current": round(m['current'], 2),
                   "min": round(m['min'], 2), "median": round(m['median'], 2), "max": round(m['max'], 2), "days": m['days'], "gapDays": m['gapDays']}
pm = lambda k, m: {"metric": k, "score": m['score'], "rank": m['rank'], "peers": m['peers']}
V = {"peer": {"score": peerscore, "rule": "both", "sector": "Financials (S&P500 은행)", "asOf": [asof, asof],
              "metrics": [pm('per', PEER['per']), pm('pbr', PEER['ptbv'])]},
     "self": {"score": selfscore, "rule": "both", "naNote": "은행", "window": [D[0][0], asof],
              "metrics": [wm('per', SH['per']), wm('pbr', SH['ptbv'])]}}
sub(r'^const BAC_VALUATION = \{.*$', 'const BAC_VALUATION = ' + json.dumps(V, ensure_ascii=False) + ';', re.M)
U = {k: v for k, v in json.load(open('peer_universe/banks.json'))['tickers'].items() if k != T}   # 본인 제외
PB = ['JPM', 'USB', 'FITB', 'RF', 'MTB', 'HBAN']
mk = lambda k, key, title, unit, mx: {"title": title, "unit": unit, "max": mx, "msValue": None,
                                     "peers": [{"name": t, "value": round(U[t][key], 2), "status": "reference"} for t in PB if isinstance(U.get(t, {}).get(key), (int, float))]}
_mdy = (lambda d: f'{int(d[5:7])}/{int(d[8:])} 종가')(json.load(open('peer_universe/banks.json'))['asOf'])   # 차트 제목 날짜 = 비교군 기준일(2026-10-06, 손으로 적은 날짜가 갱신 뒤 남았다 — Fable)
MD = {"per": mk('per', 'per', f'S&P500 은행 PER 비교 · {_mdy} (12곳 중 6곳 표시)', 'PER(TTM)', 25),
      "pbr": mk('pbr', 'ptbv', f'S&P500 은행 P/TBV 비교 · {_mdy} (12곳 중 6곳 표시 · PNC·TFC는 유형자본 태그 결측)', 'P/TBV', 4)}
for k, nm, why in (('psr', 'PSR', '은행 매출에는 이자수익이 들어 있다'), ('pcr', 'PCR', '은행 현금흐름은 예금·대출 증감이 좌우한다'), ('evebitda', 'EV/EBITDA', '예금·차입이 영업 자금이라 기업가치가 뜻이 없다')):
    MD[k] = {"title": f'{nm} — 은행에 해당 없음 ({why})', "unit": nm, "max": 1, "msValue": None, "peers": []}
sub(r'const MULTIPLE_DATA = \{.*?\n\};\n', '// 은행 동종업(peer_universe/banks.json, 은행 사전 등록 §3) 중 6곳. 값이 없는 은행은 뺀다.\nconst MULTIPLE_DATA = ' + json.dumps(MD, ensure_ascii=False, indent=2) + ';\n')
one('<div class="card-title"><span id="multipleCompareTitle">글로벌 AI 반도체 PER 비교</span></div>', f'<div class="card-title"><span id="multipleCompareTitle">{MD["per"]["title"]}</span></div>')
lvl = px / R['기본']
_pt = [U[t]['ptbv'] for t in U if isinstance(U[t].get('ptbv'), (int, float))]; _pe = [U[t]['per'] for t in U if isinstance(U[t].get('per'), (int, float))]
n_pt, n_pe = sum(v > SH['ptbv']['current'] for v in _pt), sum(v > SH['per']['current'] for v in _pe)
assert len(_pt) == PEER['ptbv']['peers'] and len(_pe) == PEER['per']['peers'], (len(_pt), len(_pe))
_ptx = [t for t in U if isinstance(U[t].get('ptbv'), (int, float)) and U[t]['ptbv'] > SH['ptbv']['current']]
pt_txt = f'유형자본을 계산할 수 있는 은행 {len(_pt)}곳 모두보다 비싸고' if n_pt == 0 else f'유형자본을 계산할 수 있는 은행 {len(_pt)}곳 중 {n_pt}곳({"·".join(_ptx)})이 BAC보다 비싸고'
pe_txt = f'{len(_pe)}곳 중 BAC보다 비싼 곳이 {n_pe}곳이다'
sub(r'<div class="vs-premise">.*?</div>\n    <div class="verdict-summary-risk">.*?</div>',
    f'<div class="vs-premise">BAC는 S&P500 대형·지역 은행 12곳(본인 제외)과 비교한다. P/TBV {SH["ptbv"]["current"]:.2f}배는 {pt_txt}, PER {SH["per"]["current"]:.1f}배는 {pe_txt}. 자기 이력에서는 P/TBV가 위쪽(상위 {100 - SH["ptbv"]["percentile"]:.0f}%)이고 PER은 중간이라, 두 배수가 같은 방향일 때만 표를 주는 은행 규칙에 따라 “중간”이다. <strong>초과이익모형 기본 가치(${R["기본"]:.0f})는 현재가의 {1 / lvl * 100:.0f}%라 −1(비싸다)이다</strong>. 합계 −1로 “적정~고평가”다. 2025년 4분기 회계 방식 변경(세금 관련 지분투자, 1~3분기 소급 재작성)으로 그 분기 순이익이 SEC 데이터($7,200M, 재작성 연간 − 원래 9개월)와 보도자료($7,319M)에서 $119M 어긋나는데, 회사가 공시한 재작성 몫이라 데이터 점검을 통과시킨다(사전 등록 9-2, 2026-10-05).</div>\n'
    f'    <div class="verdict-summary-risk">⚠️ 현재가가 초과이익모형 기본 가치의 {lvl:.2f}배라 −1이고, 자기 이력·동종업 0과 합쳐 “적정~고평가”다. 지금 가격은 ROE {f1(R["required_roe"])}가 5년 이어진다는 값이다(최근 4분기 {f1(R["roe0"])}). 순이익만큼 돌려줘 유보율이 0이라 장부가가 거의 자라지 않는 것이 내재가치를 누른다.</div>')

# 판정 JS — 금융 규칙(두 배수가 같은 방향일 때만 표), 자기 이력·동종업 모두
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
one("  if (verdictOf(judges) === BAC_VERDICT) judges.slice(0, 2).forEach((j, i) => {",
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
    """  [['self', 'bacSelfBox', 'bacSelfVerdict'], ['peer', 'bacPeerBox', 'bacPeerVerdict']].forEach(([k, bid, vid]) => {
    const side = BAC_VALUATION[k];   // 금융 규칙: 단어·색은 두 배수가 같은 방향일 때만 싼 편·비싼 편
    if (!side || side.rule !== 'both' || !side.metrics.length) return;
    const ms = side.metrics, sb = $(bid), sv = $(vid);
    const w = ms.some(m => m.score == null) ? ['logic-neutral', '기권'] : ms.every(m => m.score >= 70) ? ['logic-positive', '싼 편'] : ms.every(m => m.score < 30) ? ['logic-negative', '비싼 편'] : ['logic-neutral', '중간'];
    if (sb) { sb.classList.remove('logic-positive', 'logic-neutral', 'logic-negative'); sb.classList.add(w[0]); }
    if (sv) sv.textContent = w[1];
  });
  // 두 밸류에이션 점수가 크게 갈리면 그 사실 자체가 정보다.""")
one("const selfRaw = selfNA ? null : _vs ? +_vs.current.toFixed(1) : d[selfKey];",
    "const selfRaw = selfNA ? null : _vs ? +_vs.current.toFixed(_vs.current < 10 ? 2 : 1) : d[selfKey];")
one("""      + `\\n대차대조표와 마진은 ${S.fundamentalAsOf} 분기(확인 필요), 성장률은 연간 시계열을 쓴다.`
      + `\\n(확인 필요 — NVDA 문장 자리)`);""",
    """      + `\\n은행이라 점수를 매기지 않는다 — 예금이 부채라 유동·차입 비율이 뜻이 없고 영업이익 개념도 없다.`
      + `\\n기본적 분석 탭에 ${S.fundamentalAsOf} 분기(Q2 2026) 자본비율·장부가치를 싣는다.`);""")
one("""    const WHY = { negative_equity:""", """    const WHY = { financial: '은행·보험이라 일반 재무비율 산식이 맞지 않는다', negative_equity:""")
one("if (vd) vd.textContent = F.qualityFlags.length ? '해석 제한' : (F.grade || '—');",
    "if (vd) vd.textContent = F.qualityFlags.includes('financial') ? '판정 안 함' : F.qualityFlags.length ? '해석 제한' : (F.grade || '—');")
one("""      `같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.`
      + `\\n배수마다 "나보다 싼 종목이 몇 %인가"를 뒤집어 점수로 썼고 다섯 개를 평균했다.`
      + `\\n회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.`);""",
    f"""      `S&P500 은행(대형 7·지역 6) 안에서 P/TBV·PER 순위를 매긴 값이다(표시 점수는 두 배수 평균). BAC 본인을 뺀 12곳과 비교한다.`
      + `\\nP/TBV는 유형자본을 만들 수 있는 {PEER['ptbv']['peers']}곳, PER은 {PEER['per']['peers']}곳과 비교했다. 두 배수 모두 중간이라 표가 없다.`
      + `\\nPNC·TFC는 유형자본 태그를 못 채워(WFC는 회사 정의 보정값으로 넣음, 2026-10-05) 빠졌다.`);""")
one("""      + `\\n(확인 필요 — NVDA 문장 자리)`
      + ``);""",
    f"""      + `\\nP/TBV {SH['ptbv']['current']:.2f}배(5년 중 상위 {100 - SH['ptbv']['percentile']:.0f}%)·PER {SH['per']['current']:.1f}배(하위 {SH['per']['percentile']:.0f}%). 보통주·유형 보통주 자본은 보도자료 회사 값이다.`
      + ``);""")

# 은행 "계산 어려움" 신호(사전 등록: ① 기본 ROE_end < r ② b = 0 ③ 요구 ROE 해 없음) — 이 카드는 b = 0(카드 한정 JS, Codex 2026-10-01)
one("        nosol: () => '어떤 일정 성장률로도 현재가에 닿지 않는다',", "        nosol: () => '어떤 일정 성장률로도 현재가에 닿지 않는다',\n        b0: () => '유보율 0 — 이익을 모두 돌려줘 장부가가 자라지 않는다(초과이익모형 신호, 사전 등록)',")
one('b.textContent = `⚠ 계산 어려움 ${D.hard.length}/5`;', "b.textContent = `⚠ 계산 어려움 ${D.hard.length}/${D.model === 'rim' ? 3 : 5}`;   // 은행 초과이익모형 신호는 3개(사전 등록)")

# 참고용(기권)인데 툴팁이 판정 단어만 보이던 것(카드 한정, Fable 2026-10-01)
one('→ ${lv.label} (${DCF_RULE_TEXT})` : (mMode', "→ ${lv.label}${d.referenceOnly ? ' — 참고용(데이터 점검 미통과로 기권)' : ''} (${DCF_RULE_TEXT})` : (mMode")
one("+ (lv.range ? '\\n' + lv.range : '') + (note ? '\\n' + note : '');", "+ (lv.range ? '\\n' + lv.range : '') + (note ? '\\n' + note : '') + (d.referenceOnly ? '\\n참고용 — 데이터 점검 미통과로 판정에 쓰지 않는다' : '');")

# 내재가치 탭 경고 분모·알약 툴팁도 은행 기준으로(Codex 2차)
one('note.textContent = (D.hard.length ? `⚠ 계산 어려움 ${D.hard.length}/5 — `', "note.textContent = (D.hard.length ? `⚠ 계산 어려움 ${D.hard.length}/${D.model === 'rim' ? 3 : 5} — `")
one("      + (lv.split ? '\\n보수~낙관 시나리오가 현재가를 사이에 둬, 가정에 따라 판정이 갈린다.' : '');", "      + (lv.split ? '\\n보수~낙관 시나리오가 현재가를 사이에 둬, 가정에 따라 판정이 갈린다.' : '')\n      + (D.referenceOnly ? '\\n참고용 — 데이터 점검 미통과로 판정에 쓰지 않는다' : '');   // 카드 한정")

# ── 5. 뉴스 ──
def item(dot, date, react, title, href, src):
    cls = f'tl-dot {dot}'.strip()
    rx = f'<span class="tl-reaction flat" data-react="{react}">0.0%</span>' if react else ''
    return (f'      <div class="tl-item">\n        <div class="{cls}"></div>\n        <div class="tl-date">{date}{rx}</div>\n'
            f'        <div class="tl-title">{title}</div>\n        <a class="tl-source" href="{href}" target="_blank" rel="noopener">{src} →</a>\n      </div>')


items = [
    ('green', '2026년 7월 24일 개장 전 — 배당 14% 인상', '2026-07-24',
     '분기 배당 $0.28 → $0.32', DIV, 'Bank of America 공시 (SEC 8-K)'),
    ('', '2026년 7월 14일 개장 전 — Q2 2026 실적', '2026-07-14',
     '순이익 $9.1B·EPS $1.21(+34%) · 매출 $31.6B(+15%) · ROTCE 17.0% · 보통주 환원 $8.0B', PR['q2'], 'Bank of America 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 4월 15일 개장 전 — Q1 2026 실적', '2026-04-15',
     '순이익 $8.6B·EPS $1.11(+25%) · 매출 $30.3B(+7%)', PR['q1'], 'Bank of America 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 1월 14일 개장 전 — Q4 2025 실적', '2026-01-14',
     'EPS $0.98 · 2025년 순이익 $30.5B·EPS $3.81(+19%)', PR['q4'], 'Bank of America 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 6일 장 마감 후 — 회계 방식 변경 재작성', '2026-01-07',
     '세금 관련 지분투자 회계 방식을 바꿔 과거 분기 실적·장부가치를 재작성(2024년 보통주 순이익 $25.5B → $25.3B)', ACCT, 'Bank of America 공시 (SEC 8-K)'),
    ('', '2025년 10월 15일 개장 전 — Q3 2025 실적', '2025-10-15',
     '순이익 $8.5B·EPS $1.06 · 매출 $28.1B(+11%) · 투자은행 수수료 $2B 넘어 +43%', PR['q3'], 'Bank of America 실적 보도자료 (SEC 8-K)'),
]
for it in items:
    assert it[2] is None or it[2] in days, it[2]
tl = '    <div class="timeline" id="newsTimeline">\n' + '\n'.join(item(*i) for i in items) + '\n    </div>'
sub(r'    <div class="timeline" id="newsTimeline">\n.*?\n    </div>\n    <div class="tl-pager"', tl + '\n    <div class="tl-pager"')
sub(r'<div class="section-title">시계열 주요 뉴스 \([^)]*\)</div>', '<div class="section-title">시계열 주요 뉴스 (2025.10 ~ 2026.09)</div>')
SUM = f"""<div class="verdict-summary-head">지배적 내러티브 · 순이자이익과 트레이딩이 함께 늘어 순이익이 분기 $9B를 넘었고, 주가는 1년 새 {(px / D[-253][4] - 1) * 100:+.0f}%<span class="tag">이익 개선·적정~고평가</span></div>
    <ol class="news-list">
      <li>2분기 순이익 $9.1B·EPS $1.21(+34%), ROE 12.7%·ROTCE 17.0%였다.</li>
      <li>매출 +15% 가운데 순이자이익 +9%, 글로벌 마켓 +34%였고 효율 비율이 59%로 좋아졌다.</li>
      <li>2분기 보통주 $8.0B를 돌려주고 7월에 배당을 $0.32로 올렸다. 최근 4분기 순이익의 약 {G_PAY * 100:.0f}%를 돌려줬다.</li>
    </ol>
    <div class="verdict-summary-counter">⚠️ 배수는 자기 이력·동종업 모두 중간이고, 현재가가 초과이익모형 기본 가치의 {lvl:.2f}배라 그 칸만 −1이다 — 합계 −1 “적정~고평가”.</div>
    <div class="verdict-summary-next">🔍 다음 확인 포인트 · Q3 2026 실적(10월 중순 예상)의 순이자이익과 ROTCE 17% 유지.</div>"""
sub(r'<div class="verdict-summary-head">지배적 내러티브.*?<div class="verdict-summary-next">.*?</div>', SUM)
row = lambda k, head, t: f'<div class="bb-row {k}"><span class="bb-icon">{"▲" if k == "bull" else "▼"}</span><span class="bb-head">{head}</span><span class="bb-text">{t}</span></div>'
bull = [('수익성', '2분기 ROTCE 17.0%, EPS +34%, 효율 비율 59%.'),
        ('성장', '순이자이익 +9%, 평균 대출 +8%, 글로벌 마켓 +34%.'),
        ('주주환원', '2분기 보통주 환원 $8.0B, 배당 $0.32(+14%).')]
bear = [('밸류', f'P/TBV {SH["ptbv"]["current"]:.2f}배는 5년 중 위쪽(상위 {100 - SH["ptbv"]["percentile"]:.0f}%)이다.'),
        ('시장 의존', '글로벌 마켓 순수익 $8.0B는 시장 활동에 따라 흔들린다.'),
        ('회계', '2025년 4분기 회계 방식 변경으로 과거 장부가치·순이익이 재작성됐다.')]
m = re.search(r'(<div class="bb-title bb-bull">🐂 Bull 요인</div>\n)(.*?)(\n    </div>\n    <div class="bb-box">\n      <div class="bb-title bb-bear">🐻 Bear 요인</div>\n)(.*?)(\n    </div>\n  </div>)', h, re.S)
h = h[:m.start()] + m.group(1) + '\n'.join('      ' + row('bull', *b) for b in bull) + m.group(3) + '\n'.join('      ' + row('bear', *b) for b in bear) + m.group(5) + h[m.end():]
sub(r"const BAC_ANALYST = \{[^}]*\};", "const BAC_ANALYST = { asOf: '2026-10-05', source: 'StockAnalysis (의견 집계 · 개별 목표가)', rating: 'Buy', n: 24, nTargets: 17, mean: 66.29, median: 66,\n  low: 59, high: 75, strongBuy: 15, buy: 6, hold: 3, sell: 0, strongSell: 0 };")
sub(r'<span class="op-val">11월 중순 <span class="op-sub">Q3 FY27 예상</span></span>', '<span class="op-val">10월 중순 <span class="op-sub">Q3 2026 예상</span></span>')
# ── 6. 은행 카드가 받지 않은 틀 변경 되돌리기 ──
# 은행 9장은 아래 틀 변경 전에 만들어졌고, 뒤의 일괄 적용(비금융 카드 대상)에서도 빠졌다. 지금 NVDA 틀로 복제한 기반에는 들어 있으므로
# 다른 은행 카드와 같은 상태로 되돌린다. 쏠림 안내는 틀 주석 그대로 금융 카드에 넣지 않는다.
one("""// 쏠림 안내(2026-10-02 사용자 결정, A0 — research/verdict_replay_prereg.md 결과): 사전 규칙상 문턱 변형이 모두 탈락해 V0를 유지하고,
// 이 칸이 대부분 종목에서 "매우 비싸다"라는 사실을 툴팁으로 알린다. 숫자는 현금흐름이 계산되는 S&P500 비금융 종목의 월별 비중(dq 필터 적용).
// 금융 카드에는 넣지 않는다(검증 패널에 금융이 없다).
const DCF_SKEW_NOTE = "이 칸은 보수적으로 잡혀 있다(할인율 10%, 5년 뒤 영구성장 2.5%). S&P500 비금융 종목의 83~91%가 매달 '매우 비싸다'에 들어간다(2024-10~2026-09). 다른 종목과 견주려면 위 비율 숫자를 함께 볼 것.";
""", '')
one("""      + (lv.ratio != null ? '\\n' + DCF_SKEW_NOTE : '')
""", '')
# A3 PER 해당 없음(순이익률 2% 미만) — 은행 카드에는 없다
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
# 음수 시나리오 표기(E2/E17/E25, 비금융 카드 일괄) 이전 형태 — 초과이익모형 격자는 null만 있다(사전 등록 7-10 "—", Codex)
one("  const every = SCN.flatMap(s => G.values[s[0]].flat()).filter(v => v != null && v > 0).concat(price != null ? [price] : []);   // 음수 칸 제외(카드 한정)",
    "  const every = SCN.flatMap(s => G.values[s[0]].flat()).filter(v => v != null).concat(price != null ? [price] : []);")
one("    pv.textContent = pick > 0 ? '주당 $' + (pick < 10 ? pick.toFixed(2) : Math.round(pick)) : '계산 불가(음수)'; pv.style.color = col;",
    "    pv.textContent = pick == null ? '계산 불가' : '주당 $' + Math.round(pick); pv.style.color = col;")
one("    if (price != null) { pu.textContent = pick > 0 ? '현재가 대비 ' + pct(pick) : '—'; pu.style.color = pick > 0 ? tone(pick) : ''; }",
    "    if (price != null) { pu.textContent = pick == null ? '—' : '현재가 대비 ' + pct(pick); pu.style.color = pick == null ? '' : tone(pick); }")

# ── 7. 판정 확인 · 헤더 단어 ──
_sv = lambda m: 1 if all(x['score'] >= 70 for x in m.values()) else -1 if all(x['score'] < 30 for x in m.values()) else 0
_d = 1 if lvl <= 0.7 else 1 if lvl <= 0.9 else 0 if lvl <= 1.1 else -1 if lvl <= 1.5 else -2
_sum = _sv({'a': SH['ptbv'], 'b': SH['per']}) + _sv({'a': PEER['ptbv'], 'b': PEER['per']}) + _d
VERD = '저평가' if _sum >= 3 else '적정~저평가' if _sum >= 1 else '적정' if _sum > -1 else '적정~고평가' if _sum > -3 else '고평가'
assert (_sum, VERD) == (-1, '적정~고평가') and _d == -1, (_sum, _d)   # 자기 이력 0 · 동종업 0 · 초과이익 "비싸다" −1 → −1 → 적정~고평가(관문 보정 10-05 뒤)
h = h.replace('data-verdict style="font-size:22px;color:var(--gold);">적정~저평가</span>', f'data-verdict style="font-size:22px;color:var(--red);">{VERD}</span>', 1)   # 대체 색은 c_fill.py와 같이 적정~고평가 = 빨강(화면에서는 JS가 다시 칠한다)
one('<span class="vs-verdict" data-verdict>적정~저평가</span>', f'<span class="vs-verdict" data-verdict>{VERD}</span>')
open(p, 'w', encoding='utf-8').write(h)
print('votes sum', _sum, VERD)
print('ok base', R['기본'], 'ratio', round(lvl, 3), 'self', selfscore, 'peer', peerscore, 'req', R['required_roe'], 'band', FB['low'], FB['high'])
print('YoY', vec(cur), yd); print('QoQ', vec(qo), qd); print('roe_q', roe_q)
