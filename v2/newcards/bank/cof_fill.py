"""COF(캐피털 원) v2 카드 채우기 — SCHW 스크립트(schw_fill.py)에서 옮김. 은행 세트 여덟 번째, 루트 카드 없는 첫 은행.
기반: 지금 NVDA 틀을 clone_card.py COF --force --meta v2/newcards/meta/cof.json으로 복제하고 cof_arrays.py <카드 사본>으로 배열을 넣은 것(2026-10-05 다시 만듦,
JPM 방식 — 그 전 기반은 10-02 build.py COF --data). 데이터: v2/COF_bank.json(adapters/bank_card.py). 사용자 결정(2026-10-02): COF는 은행 RIM 경로(AXP·JPM·BAC 방식).
관문(2026-10-05 사전 등록 9 개정 뒤): G1~G5 모두 통과 — 회사가 BVPS·순환원율을 공시하지 않는 것은 "확인 불가"로 보고 남은 독립 점검(보통주 자본 금액 + TBVPS,
SEC 자본 총계 − 우선주)으로 판정한다. P/TBV 1.84가 생겨 두 배수 심판이 앉고 초과이익모형도 표를 준다 → 자기 이력 0 · 동종업 0 · 초과이익 −2 → 적정~고평가.
기반이 지금 틀이라 은행 카드가 받지 않은 틀 변경(A3 PER 해당 없음·쏠림 안내·음수 시나리오 표기)은 6절에서 되돌린다(jpm_fill.py 6절과 같다).
엔진 보강(2026-10-02): 우선주 장부가 0(청산가 태그 없음)이라 보도자료 보통주 자본·유형자본(research/bank_equity_override.json, WFC·BAC 선례, Claude 추천),
특별 항목은 보도자료 항목별 세후 EPS(bank_items.json — 반복되는 인수 상각·통합 비용 제외)."""
import json, os, re, sys
os.chdir('/Users/watermountain/Workspace/stock-widgets-preview/v2')
sys.path.insert(0, '.'); sys.path.insert(0, 'adapters')
import build_multiple_history as bmh
import bank_rim as br

T, CIK = 'COF', '0000927628'
p = 'COF_full_widget.html'; h = open(p, encoding='utf-8').read()


def one(o, n):
    global h
    c = h.count(o); assert c == 1, (c, o[:100]); h = h.replace(o, n)


def sub(pat, new, flags=re.S):
    global h
    m = list(re.finditer(pat, h, flags)); assert len(m) == 1, (len(m), pat[:90])
    h = h[:m[0].start()] + (new(m[0]) if callable(new) else new) + h[m[0].end():]


J = json.load(open('COF_bank.json'))
R = J['rim']; SH = J['self']; PEER = J['peer']; FB = SH['fairBand']
assert J['gates'] == {'G1': True, 'G2': True, 'G5': True, 'G3': True, 'G4': True}, J['gates']; assert not R['reference_only'] and SH['ptbv'] is not None and PEER['ptbv']['score'] is not None
D = json.loads(re.search(r'const COF_DAILY\s*=\s*(\[.*?\]);', h, re.S).group(1)); days = {r[0] for r in D}
px, asof = D[-1][4], D[-1][0]
assert abs(px - J['price']) < 1e-6 and asof == J['asOf']
bank = br.Bank(T, CIK, overrides=True)
S_, CE = R['shares'], R['ce']


def q(tags):
    _, rows = bmh.pick_tag(CIK, tags)
    return {e['end']: e['val'] for e in bmh.quarterly_flow(rows, T)}


# 분기 값은 보도자료(각 분기 재무 보충자료 Table 1)에서 손입력 — 순수익(Total net revenue), 순이익은 보통주 귀속
L8E = ['2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30', '2025-12-31', '2026-03-31', '2026-06-30']
rev = dict(zip(L8E, [x * 1e6 for x in [10014, 10190, 10000, 12492, 15359, 15583, 15231, 15850]]))
ni = dict(zip(L8E, [x * 1e6 for x in [1692, 1022, 1325, -4340, 3086, 2057, 2081, 2935]]))
pt = {'2026-06-30': 3818e6, '2026-03-31': 2699e6, '2025-06-30': -5929e6}      # 계속사업 세전이익(대손비용 차감 후)
nii = {'2026-06-30': 12374e6, '2026-03-31': 12145e6, '2025-06-30': 9995e6}    # 순이자수익(Net interest income)
_xq = q(['Revenues']); _nq = q(['NetIncomeLossAvailableToCommonStockholdersBasic'])
for _k in L8E:   # SEC 분기 값과 손입력이 맞는지(순이익은 참여주식 배분·4분기 차분 차이 ±$20M 안 — G5와 같은 폭)
    assert abs(_xq[_k] - rev[_k]) < 1.5e6 and abs(_nq[_k] - ni[_k]) < 25e6, (_k, _xq.get(_k), _nq.get(_k))
ks = sorted(k for k in rev if k <= '2026-06-30')[-8:]
cur, yo, qo = ks[-1], ks[-5], ks[-2]
assert (cur, yo, qo) == ('2026-06-30', '2025-06-30', '2026-03-31'), ks
r1 = lambda v: round(v / 1e9, 1)
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
roe_q = [round(bank.roe(k)[0] * 100, 1) for k in ks]
SEC = 'https://www.sec.gov/Archives/edgar/data/927628/'
PR = {'q2': SEC + '000092762826000083/ex991q22026earningsrelease.htm', 'q1': SEC + '000092762826000039/ex991q12026earningsrelease.htm',
      'q4': SEC + '000119312526019444/d45426dex991.htm', 'q3': SEC + '000092762825000267/ex991q32025earningsrelease.htm'}
SUPP = SEC + '000092762826000083/ex992q22026earningsrelease.htm'
BREX0, BREX1 = SEC + '000119312526019543/d97758d8k.htm', SEC + '000119312526145764/d85207d8k.htm'
NOTES0, NOTES1 = SEC + '000119312526033632/d66948d8k.htm', SEC + '000119312526391921/d458116d8k.htm'
PREFM = SEC + '000119312526358268/d825041d8k.htm'
TENQ = SEC + '000092762826000089/cof-20260630.htm'
f1 = lambda v: f'{v * 100:.1f}%'

# ── 1. 헤더 ──
one('<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +110%)</span>',
    f'<span class="meta-label">현재가 요구 ROE (5년 · 최근 4분기 {f1(R["roe0"])})</span>')
_NA_WHY = f'최근 1년 PER 구간(25~75% {FB["per_p25"]:.0f}~{FB["per_p75"]:.0f}배)은 2025년 2분기 Discover 인수 초기 충당금(주당 −$13.04)이 든 당시의 최근 4분기 EPS로 잰 값이라 부풀어, 지금 EPS에 곱해도 이익 수준의 범위로 읽을 수 없다(BA와 같은 규칙).'
sub(r'id="cofFairBand" style="[^"]*">[^<]*<', f'id="cofFairBand" title="PER 25~75% 구간 × 최근 4분기 EPS로 내는 범위다. {_NA_WHY}" style="font-size:22px;color:var(--text3);">해당 없음<')
h = re.sub(r'const COF_BACKTEST = \[.*?\];', 'const COF_BACKTEST = [];', h, count=1, flags=re.S)
one("if (label) { label.textContent = '밴드 적중률'; label.title = '백테스트 없음'; }", "if (label) { label.textContent = '밴드 적중률'; label.title = '" + _NA_WHY + "'; }")
one('<button class="ma-toggle-btn ma-off" data-ma="dcf" style="color:#38bdf8;border-color:#38bdf8;">◆ DCF 시나리오</button>',
    '<button class="ma-toggle-btn ma-off" data-ma="dcf" style="color:#38bdf8;border-color:#38bdf8;" hidden>◆ DCF 시나리오</button>')

# ── 2. 내재가치(RIM) 상수·격자·문장 ──
dcf = {"low": round(R['보수'], 2), "base": round(R['기본'], 2), "high": round(R['낙관'], 2), "requiredGrowth": R['required_roe'],
       "baseEquivGrowth": None, "reqMode": "roe", "requiredMargin": None, "marginNow": None, "roeNow": R['roe0'],
       "growth5y": None, "nonopPerShare": 0, "s2cFallback": False, "asOf": asof, "hard": (["roeend"] if R["roe_2y_median"] < 0.10 else []) + (["b0"] if R["b"] == 0 else []), "hardDetail": {}, "tvShare": None,
       "model": "rim", "retention": R['b'], "bvps": R['bvps'], "referenceOnly": R['reference_only']}
sub(r'^const COF_DCF = \{.*$', 'const COF_DCF = ' + json.dumps(dcf, ensure_ascii=False) + ';   // 초과이익모형 — adapters/bank_card.py, research/bank_rim_prereg.md', re.M)
ends = {'보수': R['roe_5y_median'], '기본': R['roe_2y_median'], '낙관': R['roe0']}
waccs, lams = [0.08, 0.09, 0.10, 0.11, 0.12], [0.0, 0.5, 1.0]
vals = {n: [[round(br.rim_value(CE, R['roe0'], e, R['b'], r, lam) / S_, 2) if br.rim_value(CE, R['roe0'], e, R['b'], r, lam) else None
             for r in waccs] for lam in lams] for n, e in ends.items()}
grid = {"waccs": waccs, "terms": lams, "default": [0.10, 0.5], "values": vals, "kind": "rim"}
sub(r'^const COF_DCF_GRID = .*$', 'const COF_DCF_GRID = ' + json.dumps(grid, ensure_ascii=False) + ';   // 자기자본비용 × 잔존 수렴 비율(λ)', re.M)
sub(r'const COF_DCF_TRACK = \[.*?\];', 'const COF_DCF_TRACK = [];')
one('<div class="section-title">내재가치 (DCF) — 현금흐름이 말하는 가격</div>\n  <div class="lede">회사가 앞으로 벌어들일 현금만으로 계산한 주당 가치다.</div>',
    '<div class="section-title">내재가치 (초과이익모형) — 자본이 버는 초과이익이 말하는 가격</div>\n  <div class="lede">은행은 현금흐름 모델 대신 장부가치에 자기자본비용(10%)을 넘는 이익의 현재가치를 더해 계산한다.</div>')
_dir = lambda e: '내려간다' if e < R['roe0'] else '올라간다'
new = [f'ROE가 최근 4분기 {f1(R["roe0"])}에서 5년 중앙값 {f1(R["roe_5y_median"])}로 {_dir(R["roe_5y_median"])}.',
       f'ROE가 최근 4분기 {f1(R["roe0"])}에서 최근 2년 중앙값 {f1(R["roe_2y_median"])}로 {_dir(R["roe_2y_median"])}.',
       f'ROE {f1(R["roe0"])}가 5년 동안 이어진다.']
olds = re.findall(r'<td class="story">(지난 5년 성장 속도의 절반.*?|지난 5년의 성장 속도로.*?|최근 3년의 성장 속도로.*?)</td>', h)
assert len(olds) == 3
for o, n in zip(olds, new):
    assert h.count(o) == 1; h = h.replace(o, n)
one('<div class="note">세 값은 확률이 아니라, 과거 실적에서 서로 다른 가정을 뽑아 계산한 결과다.</div>',
    f'<div class="note">세 값은 확률이 아니라, 과거 ROE에서 서로 다른 가정을 뽑아 계산한 결과다. 5년 뒤 ROE가 자기자본비용(10%)보다 높으면 그쪽으로 절반 수렴한다고 보는데, COF는 세 시나리오의 끝 ROE({f1(R["roe_5y_median"])}·{f1(R["roe_2y_median"])}·{f1(R["roe0"])})가 모두 10%보다 낮아 수렴 가정이 값을 바꾸지 않는다(자기자본비용 10% 기준으로 수렴 없음·완전 수렴 모두 기본 ${vals["기본"][0][2]:.0f}; 직접 바꿔보기에서 자기자본비용을 8~9%로 낮추면 끝 ROE가 그보다 높은 보수·낙관에서는 수렴이 작동한다). 유보율은 0%(최근 4분기 배당·자사주 환원이 순이익보다 많다)라 장부가가 자라지 않는다고 보고, 기타포괄손익은 반영하지 않는다. 5년 중앙값 ROE가 가장 높아 “보수”(${R["보수"]:.0f})가 “낙관”(${R["낙관"]:.0f})·“기본”(${R["기본"]:.0f})보다 높게 나온다(이름과 순서가 뒤집힘). 기본의 2년 중앙값이 낮은 것은 2025년 2분기 Discover 인수 초기 충당금으로 적자였던 기간이 들어 있어서다.</div>')
one("    ['현금흐름', lv.label in DV ? DV[lv.label] : null, lv.label, 2],",
    "    ['초과이익', lv.label in DV && !D.referenceOnly ? DV[lv.label] : null, D.referenceOnly ? '참고용' : lv.label, 2],   // 데이터 점검(G1·G2·G4) 미통과 → 참고용·기권(사전 등록 7-7)")
one("    dv.textContent = lv.label + (lv.split ? ' · 갈림' : '');",
    "    dv.textContent = d.referenceOnly ? '참고용 · 기권' : lv.label + (lv.split ? ' · 갈림' : '');   // 데이터 점검 미통과(사전 등록 7-7)")
one("    pill('dcf', lv.cls, lv.label + (lv.split ? ' · 갈림' : ''));", "    pill('dcf', D.referenceOnly ? 'mid' : lv.cls, D.referenceOnly ? '참고용 · 기권' : lv.label + (lv.split ? ' · 갈림' : ''));   // 데이터 점검 미통과(카드 한정)")
one('<div class="note" data-dcf-nonop>기본 시나리오 $314 = 사업 가치 $310 + 비영업 자산 $4(주당, 지분·장기투자)</div>', '<div class="note" data-dcf-nonop hidden></div>')
sub(r'<div class="reverse">.*?</div>\n  </div>', f'<div class="reverse" data-rim-reverse>지금 가격이 정당하려면 5년 동안 ROE가 매년 <b data-dcf-req>—</b>여야 하고, 그 뒤에도 절반만 수렴한 약 {f1(0.10 + 0.5 * (R["required_roe"] - 0.10))}가 이어져야 한다.</div>\n  </div>')
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
    """    if (cell) cell.title = roeMode ? `현재가 $${price.toFixed(2)} 가 정당화되려면 5년 동안 ROE가 ${d.requiredGrowth != null ? f1(d.requiredGrowth) + '이고 그 뒤 절반 수렴한 ' + f1(0.10 + 0.5 * (d.requiredGrowth - 0.10)) + '가 이어져야' : '(범위 밖)여야'} 한다(최근 4분기 ${f1(d.roeNow)}).`
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
selfscore = round((SH['ptbv']['score'] + SH['per']['score']) / 2, 1)   # 표시 점수는 두 배수 평균, 표는 두 배수가 같은 방향일 때만(2026-10-05 관문 개정 뒤 P/TBV 생김)
peerscore = round((PEER['ptbv']['score'] + PEER['per']['score']) / 2, 1)
sub(r'const COF_SCORES = \{.*?\n\};', f'''const COF_SCORES = {{
  fundamental: null,   // 은행 — 일반 재무비율 산식이 맞지 않아 매기지 않는다
  peer: {peerscore},          // S&P500 은행 대비 P/TBV·PER 순위 평균(표시용). 표는 두 배수가 같은 방향일 때만
  selfHistory: {selfscore},   // 자기 5년 P/TBV·PER 평균(표시용). 표는 두 배수가 같은 방향일 때만
  asOf: "{asof}",
  fundamentalAsOf: "2026-06-30",   // Q2 2026 10-Q (2026-07-28 공시)
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
fund = {"ticker": T, "basis": "quarter", "asOf": "2026-06-30", "filedAt": "2026-07-28", "score": None, "grade": None, "qualityFlags": ["financial"],
        "axes": {"health": {"rows": [frow("currentRatio", "유동비율", "%", note=NA), frow("quickRatio", "당좌비율", "%", note=NA),
                                     frow("debtDependency", "차입금의존도", "%", note=NA), frow("interestCoverage", "이자보상배율", "x", note=NA),
                                     frow("debtToEquity", "부채비율", "%", LI['2026-06-30'] / SE['2026-06-30'] * 100)], "points": None, "max": 33},
                 "growthProfit": {"rows": [frow("revenueCagr", "매출 CAGR", "%", CAGR_REV, "순수익 · 2025년 5월 Discover 인수로 규모가 커졌다"), frow("opIncomeCagr", "순이익 CAGR", "%", CAGR_NI, "은행은 영업이익 대신 보통주 귀속 순이익 · 2025년은 Discover 인수 초기 충당금(세전 $8.8B)으로 낮다"),
                                           frow("opMargin", "영업이익률(OPM)", "%", note=NA), frow("netMargin", "순이익률", "%", NM_TTM)], "points": None, "max": 34}},
        "note": "은행 지주회사(신용카드·소비자 금융) — 예금이 부채라 유동·차입 비율이 뜻이 없고 v1 모델도 은행을 채점하지 않는다", "netCash": None}
sub(r'^const COF_FUNDAMENTAL = \{.*$', 'const COF_FUNDAMENTAL = ' + json.dumps(fund, ensure_ascii=False) + ';', re.M)
act = {"ticker": T, "status": "na", "reason": "은행 지주회사(예금으로 신용카드·자동차·기업 대출)라 매출채권·재고 회전으로 운영 효율을 판정하지 않는다"}
sub(r'^const COF_ACTIVITY = \{.*$', 'const COF_ACTIVITY = ' + json.dumps(act, ensure_ascii=False) + ';', re.M)
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
one('const y2min=40, y2max=75;', 'const y2min=-10, y2max=40;')   # 순이익률 −0.6% 분기(Discover 인수 초기)가 축 밖으로 나가지 않게(D39, 2026-10-05)
one("labels:['Q3 FY25','Q4 FY25','Q1 FY26','Q2 FY26','Q3 FY26','Q4 FY26','Q1 FY27','Q2 FY27'],", 'labels:[' + ','.join(f"'{x}'" for x in L8) + '],')
one("{type:'line',label:'OPM(%)',", "{type:'line',label:'ROE(최근 4분기, 기초자본 기준, GAAP, %)',")
one("{type:'bar',label:'매출($B)',", "{type:'bar',label:'순영업수익($B)',")
one("{type:'bar',label:'순이익($B)',", "{type:'bar',label:'순이익($B, 보통주 귀속)',")
for lab, nl, val, subt in [('FCF', 'CET1 비율 (Q2 2026)', '13.7%', '1분기 14.4% · 바젤 III 표준법'),
                           ('Capex', '대출 잔액 (Q2 2026 말)', '$457.2B', '+2%(분기) · 신용카드 $275.4B'),
                           ('R&amp;D', '순이자수익 (Q2 2026)', f'${nii[cur] / 1e9:.1f}B', f'전년 대비 {(nii[cur] / nii[yo] - 1) * 100:+.0f}% · 순이자마진 8.01%')]:
    sub(rf'<div class="stat-label">{lab} \(Q2 FY27\)</div>\n      <div class="stat-value">[^<]*</div>\n      <div class="stat-sub">[^<]*</div>',
        f'<div class="stat-label">{nl}</div>\n      <div class="stat-value">{val}</div>\n      <div class="stat-sub">{subt}</div>')
sub(r'<div class="stat-value">11월 중순 예상</div>\n      <div class="stat-sub">일정 · Q3 FY27</div>',
    '<div class="stat-value">10월 하순 예상</div>\n      <div class="stat-sub">일정 · Q3 2026 (회사 미확정)</div>')
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
extra = (xrow('CET1 비율 (연결)', '13.7%', 'CET1 자본 $70.8B · 6월 말 기준(잠정), 1분기 14.4%')
         + xrow('Tier 1 레버리지 · TCE 비율', '11.8% · 10.2%', '6월 말 기준 · 1년 전 14.2% · 10.3%')
         + xrow('유형 장부가치(TBVPS)', '$105.21', '회사 공시값과 카드 계산이 맞는다(G1 통과). 주당 장부가치(BVPS)는 공시하지 않아 보통주 자본 금액과 TBVPS로 대신 확인한다(사전 등록 9-1)'))
sub(r'(<span class="diag-note" id="fundNetCashNote">[^<]*</span></div>\n        <div class="diag-badge info">ℹ️ 참고</div>\n      </div>\n)', lambda m: m.group(1) + extra)
sub(r'<div style="margin-top:14px;font-size:11\.5px;color:var\(--text2\);line-height:1\.6;">유동비율·당좌비율.*?</div>',
    f'<div style="margin-top:14px;font-size:11.5px;color:var(--text2);line-height:1.6;">COF는 신용카드 중심 은행 지주회사라 예금($484.3B)이 부채의 대부분이어서 유동·당좌·차입 비율과 이자보상배율을 해당 없음으로 두고, 규제자본 비율을 대신 싣는다. 부채비율 {LI['2026-06-30'] / SE['2026-06-30'] * 100:,.0f}%는 예금과 차입($45.4B)을 포함한 값이다. CET1 비율은 1분기 14.4%에서 13.7%로 내려왔다(4월 Brex 인수와 2분기 자사주 매입 $2.7B가 든 분기).</div>')
vec = lambda e: [r1(rev[e]), r1(pt[e]), r1(ni[e]), r1(nii[e])]
f = lambda a, b: '%+.1f%%' % ((a / b - 1) * 100)
fs = lambda a, b: '흑자 전환' if b < 0 < a else f(a, b)   # 1년 전 분기 적자(Discover 초기 충당금)
yd = [f(rev[cur], rev[yo]), fs(pt[cur], pt[yo]), fs(ni[cur], ni[yo]), f(nii[cur], nii[yo])]
qd = [f(rev[cur], rev[qo]), f(pt[cur], pt[qo]), f(ni[cur], ni[qo]), f(nii[cur], nii[qo])]
tq = lambda a: ', '.join(f"'{x}'" for x in a)
sub(r"curLabel: 'Q2 FY27', cmpLabel: 'Q2 FY26',\n    titleSuffix: '[^']*',\n    chart: \{ cur: \[[^\]]*\], cmp: \[[^\]]*\] \},\n    deltas: \[[^\]]*\],",
    f"curLabel: 'Q2 2026', cmpLabel: 'Q2 2025',\n    titleSuffix: 'YoY (Q2 2026 vs Q2 2025)',\n    chart: {{ cur: {vec(cur)}, cmp: {vec(yo)} }},\n    deltas: [{tq(yd)}],")
sub(r"curLabel: 'Q2 FY27', cmpLabel: 'Q1 FY27',\n    titleSuffix: '[^']*',\n    chart: \{ cur: \[[^\]]*\], cmp: \[[^\]]*\] \},\n    deltas: \[[^\]]*\],",
    f"curLabel: 'Q2 2026', cmpLabel: 'Q1 2026',\n    titleSuffix: 'QoQ (Q2 2026 vs Q1 2026)',\n    chart: {{ cur: {vec(cur)}, cmp: {vec(qo)} }},\n    deltas: [{tq(qd)}],")
fn = lambda a, extra='': (f"footnote: '기준일: 2026.06.30(Q2 2026) vs {a} · GAAP · 세전 이익은 대손비용을 뺀 계속사업 세전이익 · 순이익은 보통주 귀속 · 1년 전 분기는 Discover 인수 초기 충당금 $8.8B로 적자 · {extra}"
                f"<a href=\"{PR['q2']}\" target=\"_blank\" rel=\"noopener\">Capital One Q2 2026 실적 보도자료 (SEC 8-K) →</a>'")
sub(r"footnote: '기준일: 2026\.07\.26\(Q2 FY27\) vs 2025\.07\.27\(Q2 FY26\)[^\n]*'", fn('2025.06.30(Q2 2025)'))
sub(r"footnote: '기준일: 2026\.07\.26\(Q2 FY27\) vs 2026\.04\.26\(Q1 FY27\)[^\n]*'", fn('2026.03.31(Q1 2026)'))
one('<span id="fundPeriodTitle">YoY (Q2 FY27 vs Q2 FY26)</span>', '<span id="fundPeriodTitle">YoY (Q2 2026 vs Q2 2025)</span>')
one("        labels: ['매출', '영업이익', '순이익', 'FCF'],", "        labels: ['순수익', '세전 이익', '순이익', '순이자수익'],")
one('// FCF = 영업현금흐름 − PaymentsToAcquireProductiveAssets, 분기값은 누적값의 차이.',
    '// 은행 지주회사: 순수익 · 세전 이익(대손비용 차감 후) · 보통주 귀속 순이익 · 순이자수익, 분기값은 보도자료 손입력.')
SEG = [('신용카드', 11765, '#004977'), ('소비자 금융', 3209, '#d03027'), ('기업 금융', 850, '#6b8fb3'), ('기타', 26, '#b0b8c0')]
tot = sum(v for _, v, _ in SEG); assert tot == round(rev[cur] / 1e6), tot
leg = ''.join(f'\n          <div style="display:flex;align-items:center;gap:7px;font-size:11px;color:var(--text2);white-space:nowrap;"><span style="width:8px;height:8px;border-radius:50%;background:{c};display:inline-block;flex-shrink:0;"></span>{n} <strong style="color:var(--text);">${v / 1000:.1f}B · {v / tot * 100:.1f}%</strong></div>' for n, v, c in SEG)
sub(r'<div class="card-title">매출 구성 — Market Platform.*?</div>\n\n      <div style="display:flex;align-items:center;justify-content:center;gap:20px;">.*?\n      </div>\n\n      <div class="yoy-footnote" style="margin-top:14px;">.*?</div>',
    '<div class="card-title">순수익 구성 — 부문별 (Q2 2026 · 2026.06.30 기준)</div>\n\n      <div style="display:flex;align-items:center;justify-content:center;gap:20px;">\n        <div class="chart-wrap" style="height:170px;width:170px;flex-shrink:0;">\n          <canvas id="segmentPieChart"></canvas>\n        </div>\n        <div style="display:flex;flex-direction:column;gap:9px;">' + leg +
    f'\n        </div>\n      </div>\n\n      <div class="yoy-footnote" style="margin-top:14px;">1년 전보다 신용카드 +29.4%, 소비자 금융 +25.5%, 기업 금융 −9.3%(1년 전 분기에는 Discover가 5월 18일부터만 들어 있다) · 출처: <a href="{SUPP}" target="_blank" rel="noopener">Q2 2026 재무 보충자료 부문 표 (SEC) →</a></div>')
sub(r'// ─── 매출 구성 도넛 차트 \([^)]*\) ───', '// ─── 순수익 구성 도넛 차트 (부문 4개, 백만 달러) ───')
one('const total = 96221;', f'const total = {tot};')
one("labels:['Hyperscale','AI Clouds·Industrial·Enterprise','Edge Computing'],", 'labels:' + json.dumps([n for n, _, _ in SEG], ensure_ascii=False) + ',')
one('data:[48710, 40313, 7198],', 'data:[' + ', '.join(str(v) for _, v, _ in SEG) + '],')
sub(r"backgroundColor:\['#[0-9a-fA-F]{6}','#4d7a00','#3498db'\],", 'backgroundColor:' + json.dumps([c for _, _, c in SEG]) + ',')
R_payout = bank.payout_ttm(cur)[0] / bank.ni_ttm(cur)[0]
assert abs(min(max(1 - R_payout, 0.0), 1.0) - R['b']) < 1e-6, (R_payout, R['b'])   # 환원 > 순이익이면 b = 0(사전 등록 1-7)
_sh0 = bank.shares('2025-06-30'); _sh1 = bank.shares(cur)
CAPA = f"""<div class="card-title">자본배분 · 주주환원 (Q2 2026 · 2026.06.30 기준)</div>
      <div class="zone-list">
        <div class="zone-item">
          <span class="zone-label">자사주 매입 (Q2 2026)</span>
          <span class="zone-val">$2.7B</span>
        </div>
        <div class="zone-item">
          <span class="zone-label">자사주 매입 (2026 상반기)</span>
          <span class="zone-val">$5.2B</span>
        </div>
        <div class="zone-item">
          <span class="zone-label">분기 배당 인상 (2025년 4분기부터)</span>
          <div style="display:flex;align-items:center;gap:8px;">
            <span class="zone-tag" style="background:rgba(240,192,64,0.18);color:var(--gold);">$0.60 → $0.80</span>
            <span class="zone-val">+33%</span>
          </div>
        </div>
        <div class="zone-item">
          <span class="zone-label">최근 4분기 환원율 (SEC 배당 + 자사주 − 주식 발행, ÷ 보통주 순이익)</span>
          <span class="zone-val">{R_payout * 100:.0f}%</span>
        </div>
      </div>
      <div class="yoy-footnote" style="margin-top:14px;">환원이 순이익보다 많아 유보율이 {f1(R['b'])}이다(초과이익모형 입력 b, 장부가가 자라지 않는다) · 기말 주식 수는 1년 새 {(_sh0[0] - _sh1[0]) / 1e4:,.0f}만 주 줄었다({_sh0[0] / 1e8:.2f}억 → {_sh1[0] / 1e8:.2f}억, 4월 Brex 인수 대가 주식 발행 포함) · 9월 1일 우선주 시리즈 M $1.0B를 상환했다(카드 기준 분기 뒤) · 출처: <a href="{TENQ}" target="_blank" rel="noopener">Q2 2026 10-Q →</a> · <a href="{SUPP}" target="_blank" rel="noopener">재무 보충자료</a> · <a href="{PREFM}" target="_blank" rel="noopener">우선주 상환 (SEC 8-K)</a></div>
    </div>"""
sub(r'<div class="card-title">자본배분 · 주주환원 \(Q2 FY27 · 2026\.07\.26 기준\)</div>\n      <div class="zone-list">.*?\n      </div>\n    </div>', CAPA)
CHK = """<div class="card-title">다음 실적 체크포인트 <span style="color:var(--gold);font-weight:600;">2026년 10월 하순 (예상) · Q3 2026</span></div>
    <div style="font-size:12px;color:var(--text2);line-height:1.8;">
      <div style="margin-bottom:8px;"><strong style="color:var(--accent2);">①</strong> 순상각률(2분기 3.23%)과 30일 이상 연체율(3.13%) — 월간 신용 지표(7·8월)도 함께</div>
      <div style="margin-bottom:8px;"><strong style="color:var(--accent2);">②</strong> Discover 통합 비용(2분기 세전 $298M)과 인수 상각(세전 $494M)</div>
      <div style="margin-bottom:8px;"><strong style="color:var(--accent2);">③</strong> 4월 인수한 Brex 통합 비용(2분기 세전 $96M)</div>
      <div><strong style="color:var(--accent2);">④</strong> CET1 13.7%에서 자사주 매입 속도(2분기 $2.7B)와 9월 유로 사채 €1.5B 발행</div>
    </div>"""
sub(r'<div class="card-title">다음 실적 체크포인트 <span[^>]*>[^<]*</span></div>\n    <div style="font-size:12px;color:var\(--text2\);line-height:1\.8;">.*?\n    </div>', CHK)

# ── 4. 밸류에이션 ──
one('<div class="vc-head">PBR</div>', '<div class="vc-head">P/TBV</div>')
one('<div class="vs-name" title="지난 5년 COF 자신의 배수보다 지금이 얼마나 낮은가. 높을수록 싸다.">자기 이력 대비</div>',
    '<div class="vs-name" title="지난 5년 COF 자신의 배수보다 지금이 얼마나 낮은가. 높을수록 싸다. 은행 규칙은 P/TBV·PER 두 배수가 모두 70 이상이면 +1, 모두 30 미만이면 −1, 그 밖은 0이다. 표시 점수는 두 배수 평균이다.">자기 이력 대비</div>')
one('<div class="vs-name" title="회사가 앞으로 벌어들일 현금만으로 계산한 주당 가치(기본 시나리오).">현금흐름 (내재가치)</div>',
    '<div class="vs-name" title="은행은 초과이익모형(장부가치 + 자기자본비용 10%를 넘는 이익의 현재가치)으로 계산한다. 기본 시나리오.">초과이익 (내재가치)</div>')
one('<span class="logic-tag">내재가치 <span class="logic-denom">현금흐름</span></span>', '<span class="logic-tag">내재가치 <span class="logic-denom">초과이익</span></span>')
one('<div class="vs-name" title="같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.">동종업 대비</div>',
    '<div class="vs-name" title="S&P500 은행(대형·지역 13곳) 대비 P/TBV·PER 순위. 높을수록 싸다. 두 배수가 같은 방향일 때만 표를 준다. 표시 점수는 두 배수 평균이다.">동종업 대비</div>')
sub(r'<div class="vs-note">현재가 <span data-vs="price">[^<]*</span> 대비 <strong data-vs="upside">[^<]*</strong> · 기본 시나리오</div>',
    '<div class="vs-note">현재가 <span data-vs="price">—</span> 대비 <strong data-vs="upside">—</strong> · 초과이익모형 기본</div>')
one('<span class="val-name">PBR <span class="hist-note" data-hist="note"></span></span>', '<span class="val-name">P/TBV (유형 장부) <span class="hist-note" data-hist="note"></span></span>')
a_ = h.index('    </div>\n\n    <div class="card" style="display:flex;flex-direction:column;">')
h = h[:a_] + ('      <div style="font-size:11px;color:var(--text3);line-height:1.6;margin-top:6px;">은행은 매출·현금흐름·EBITDA 배수가 뜻이 없어 P/TBV·PER 두 배수만 본다. '
              'COF는 회사가 유형 장부가치(TBVPS $105.21)를 공시해 카드 계산과 맞고(G1), 주당 장부가치(BVPS)는 공시하지 않아 보통주 자본 금액과 TBVPS로 대신 확인한다(G2, 사전 등록 9-1). 보통주 자본은 우선주가 장부상 0(청산가 태그 없음)이라 보도자료의 보통주 자본($108.4B)·유형 보통주 자본($64.5B)을 쓴다(WFC·BAC 선례).</div>\n') + h[a_:]
wm = lambda k, m: {"metric": k, "score": round(m['score'], 1), "percentile": round(m['percentile'], 1), "current": round(m['current'], 2),
                   "min": round(m['min'], 2), "median": round(m['median'], 2), "max": round(m['max'], 2), "days": m['days'], "gapDays": m['gapDays']}
pm = lambda k, m: {"metric": k, "score": m['score'], "rank": m['rank'], "peers": m['peers']}
V = {"peer": {"score": peerscore, "rule": "both", "need": 2, "sector": "Financials (S&P500 은행)", "asOf": [asof, asof],
              "metrics": [pm('per', PEER['per']), pm('pbr', PEER['ptbv'])]},
     "self": {"score": selfscore, "rule": "both", "need": 2, "naNote": "은행", "window": [D[0][0], asof],
              "metrics": [wm('per', SH['per']), wm('pbr', SH['ptbv'])]}}   # 두 배수 규칙(사전 등록 §0) — 2026-10-05 관문 개정 뒤 P/TBV 생김
sub(r'^const COF_VALUATION = \{.*$', 'const COF_VALUATION = ' + json.dumps(V, ensure_ascii=False) + ';', re.M)
U = {k: v for k, v in json.load(open('peer_universe/banks.json'))['tickers'].items() if k != T}   # 본인 제외
PB = ['JPM', 'USB', 'FITB', 'RF', 'MTB', 'HBAN']
mk = lambda k, key, title, unit, mx: {"title": title, "unit": unit, "max": mx, "msValue": None,
                                     "peers": [{"name": t, "value": round(U[t][key], 2), "status": "reference"} for t in PB if isinstance(U.get(t, {}).get(key), (int, float))]}
_mdy = (lambda d: f'{int(d[5:7])}/{int(d[8:])} 종가')(json.load(open('peer_universe/banks.json'))['asOf'])   # 차트 제목 날짜 = 비교군 기준일(2026-10-06, 손으로 적은 날짜가 갱신 뒤 남았다 — Fable)
MD = {"per": mk('per', 'per', f'S&P500 은행 PER 비교 · {_mdy} (13곳 중 6곳 표시)', 'PER(TTM)', 25),
      "pbr": mk('pbr', 'ptbv', f'S&P500 은행 P/TBV 비교 · {_mdy} ({PEER["ptbv"]["peers"]}곳 중 6곳 표시)', 'P/TBV', 4)}
assert len(MD['per']['peers']) == len(MD['pbr']['peers']) == 6, (len(MD['per']['peers']), len(MD['pbr']['peers']))
for k, nm, why in (('psr', 'PSR', '은행 매출에는 이자수익이 들어 있다'), ('pcr', 'PCR', '은행 현금흐름은 예금·대출 증감이 좌우한다'), ('evebitda', 'EV/EBITDA', '예금·차입이 영업 자금이라 기업가치가 뜻이 없다')):
    MD[k] = {"title": f'{nm} — 은행에 해당 없음 ({why})', "unit": nm, "max": 1, "msValue": None, "peers": []}
sub(r'const MULTIPLE_DATA = \{.*?\n\};\n', '// 은행 동종업(peer_universe/banks.json, 은행 사전 등록 §3) 중 6곳. 값이 없는 은행은 뺀다.\nconst MULTIPLE_DATA = ' + json.dumps(MD, ensure_ascii=False, indent=2) + ';\n')
one('<div class="card-title"><span id="multipleCompareTitle">글로벌 AI 반도체 PER 비교</span></div>', f'<div class="card-title"><span id="multipleCompareTitle">{MD["per"]["title"]}</span></div>')
lvl = px / R['기본']
_pe = [U[t]['per'] for t in U if isinstance(U[t].get('per'), (int, float))]
n_pe = sum(v > SH['per']['current'] for v in _pe)
assert len(_pe) == PEER['per']['peers'] == 13 and n_pe == 13 - PEER['per']['rank'] + 1, (len(_pe), n_pe)   # COF보다 PER이 높은 은행 수 = 13 − (싼 쪽 순위 − 1)
RK = PEER['per']['rank']
_tb = sorted(t for t in U if isinstance(U[t].get('ptbv'), (int, float)))
_tb_hi = [t for t in _tb if U[t]['ptbv'] > SH['ptbv']['current']]   # COF보다 P/TBV가 높은 은행
assert len(_tb) == PEER['ptbv']['peers'] == 11 and len(_tb_hi) == PEER['ptbv']['peers'] - PEER['ptbv']['rank'] + 1, (len(_tb), _tb_hi)
sub(r'<div class="vs-premise">.*?</div>\n    <div class="verdict-summary-risk">.*?</div>',
    f'<div class="vs-premise">COF는 신용카드 중심 은행 지주회사라 은행 사전 등록의 고정 비교군인 S&P500 대형·지역 은행 {len(_pe)}곳과 비교한다. PER {SH["per"]["current"]:.1f}배(최근 4분기 EPS는 회사 발표 분기 EPS의 합)는 {len(_pe)}곳 중 싼 쪽에서 {RK}번째로 중간이고(중앙값 {PEER["per"]["median"]:.1f}배), 자기 이력에서도 중간(하위 {SH["per"]["percentile"]:.0f}%)이다. '
    f'P/TBV {SH["ptbv"]["current"]:.2f}배는 유형자본을 계산할 수 있는 은행 {len(_tb)}곳 중 {len(_tb_hi)}곳({"·".join(_tb_hi)})이 COF보다 비싸 중간이고, 자기 이력에서는 위쪽(상위 {100 - SH["ptbv"]["percentile"]:.0f}%)이다. 두 배수가 같은 방향일 때만 표를 주는 은행 규칙에 따라 자기 이력·동종업 모두 “중간”이다. '
    f'<strong>초과이익모형 기본 가치(${R["기본"]:.0f})는 현재가의 {1 / lvl * 100:.0f}%라 −2(매우 비싸다)다</strong>. 합계 −2로 “적정~고평가”다. 회사가 주당 장부가치(BVPS)와 순환원율을 공시하지 않는다. 보통주 자본은 보도자료 값을 그대로 쓰므로 그 자체는 대조가 아니지만, SEC 자본 총계와의 차이가 우선주($4.8~5.4B)와 맞고 유형 장부가치(TBVPS)가 회사 공시와 맞아(주식 수까지 확인) 데이터 점검을 통과시킨다(공시 없는 항목은 확인 불가, 사전 등록 9-1, 2026-10-05).</div>\n'
    f'    <div class="verdict-summary-risk">⚠️ 현재가가 초과이익모형 기본 가치의 {lvl:.2f}배라 −2다. 지금 가격은 ROE {f1(R["required_roe"])}가 5년 이어진다는 값이다(최근 4분기 특별 항목 제외 {f1(R["roe0"])}). 기본 가정의 최근 2년 중앙값 ROE({f1(R["roe_2y_median"])})에는 2025년 2분기 Discover 인수 초기 충당금(세전 $8.8B)으로 적자였던 기간이 들어 있어 낮다(5년 중앙값 {f1(R["roe_5y_median"])}로 가는 보수는 ${R["보수"]:.0f}). 최근 4분기 환원이 순이익보다 많아 유보율이 0이라 장부가가 자라지 않는다고 둔다.</div>')

# 판정 JS — 금융 규칙(두 배수가 같은 방향일 때만 표), 자기 이력·동종업 모두
# 자기 이력 툴팁 첫 줄(E13 '같거나 높았던 날')은 지금 틀에 이미 들어 있다
one("""  const valid = side => side && side.score != null
    && (side.metrics || []).filter(m => m.score != null).length >= 3;
  const vote = s => s >= 70 ? 1 : s < 30 ? -1 : 0;""",
    """  // 금융 카드(rule 'both', research/brkb_two_pillar_prereg.md §2 · bank_rim_prereg.md §0)는 두 배수로 성립하고,
  // 두 점수가 모두 70 이상이면 +1, 모두 30 미만이면 −1이다(P/TBV = PER × ROTCE라 독립 증거가 아니다).
  const valid = side => side && side.score != null
    && (side.metrics || []).filter(m => m.score != null).length >= (side.rule === 'both' ? Math.max(2, side.need || 0, side.metrics.length) : 3);
  const vote = s => s >= 70 ? 1 : s < 30 ? -1 : 0;
  const sideVote = side => side.rule === 'both'
    ? (side.metrics.every(m => m.score >= 70) ? 1 : side.metrics.every(m => m.score < 30) ? -1 : 0) : vote(side.score);""")
one("['자기 이력', valid(V.self) ? vote(V.self.score) : null, V.self && V.self.score, 1],",
    "['자기 이력', valid(V.self) ? sideVote(V.self) : null, V.self && V.self.score, 1],")
one("['동종업', valid(V.peer) ? vote(V.peer.score) : null, V.peer && V.peer.score, 1],",
    "['동종업', valid(V.peer) ? sideVote(V.peer) : null, V.peer && V.peer.score, 1],")
one("  if (verdictOf(judges) === COF_VERDICT) judges.slice(0, 2).forEach((j, i) => {",
    "  // 금융 카드는 심판 표가 sideVote(규칙별 — 두 배수가 같은 쪽일 때만 표)라 한 칸 바꾸기 계산이 맞지 않아 건너뛴다(Codex)\n  if (false) judges.slice(0, 2).forEach((j, i) => {")
one("pill('self', ...byScore(V.self.score)); pill('peer', ...(V.peer.score == null ? ['mid', '표본 부족'] : byScore(V.peer.score)));",
    """const bothPill = s => (s.metrics.some(m => m.score == null) || s.metrics.length < (s.need || 0)) ? ['mid', '기권'] : s.metrics.every(m => m.score >= 70) ? ['', '싸다'] : s.metrics.every(m => m.score < 30) ? ['high', '비싸다'] : ['mid', '중간'];
  pill('self', ...(V.self.rule === 'both' ? bothPill(V.self) : byScore(V.self.score)));
  pill('peer', ...(V.peer.score == null ? ['mid', '표본 부족'] : V.peer.rule === 'both' ? bothPill(V.peer) : byScore(V.peer.score)));""")
one("""    const f = sel => item.querySelector(`[data-hist="${sel}"]`), x = v => v.toFixed(1) + 'x';""",
    """    const f = sel => item.querySelector(`[data-hist="${sel}"]`), x = v => v.toFixed(m.metric === 'pbr' ? 2 : 1) + 'x';""")
# 빈 구간 안내(gapDays)는 6절의 PER 해당 없음 되돌리기와 같은 줄이라 거기서 넣는다
one("""  ['peer', 'self'].forEach(k => {""",
    """  // 이 카드가 쓰지 않는 배수(금융 카드의 PSR·PCR·EV/EBITDA)는 같은 자리에 '해당 없음'
  const haveM = new Set(V.self.metrics.map(m => m.metric));
  if (V.self.metrics.length) document.querySelectorAll('#valuation .val-item[data-metric]').forEach(item => {
    if (haveM.has(item.dataset.metric)) return;
    const f = sel => item.querySelector(`[data-hist="${sel}"]`);
    if (f('cur')) f('cur').textContent = '—';
    if (f('badge')) { f('badge').className = 'hist-badge mid'; f('badge').textContent = '해당 없음'; }
    if (f('note')) f('note').textContent = (V.self.naNotes || {})[item.dataset.metric] || V.self.naNote || '';
    if (f('fill')) { f('fill').className = 'val-fill hist-fill mid'; f('fill').style.width = '0%'; }
    ['min', 'median', 'max'].forEach(k => { if (f(k)) f(k).textContent = '—'; });
  });
  ['peer', 'self'].forEach(k => {""")
one("""  // 두 밸류에이션 점수가 크게 갈리면 그 사실 자체가 정보다.""",
    """  [['self', 'cofSelfBox', 'cofSelfVerdict'], ['peer', 'cofPeerBox', 'cofPeerVerdict']].forEach(([k, bid, vid]) => {
    const side = COF_VALUATION[k];   // 금융 규칙: 단어·색은 두 배수가 같은 방향일 때만 싼 편·비싼 편
    if (!side || side.rule !== 'both' || !side.metrics.length) return;
    const ms = side.metrics, sb = $(bid), sv = $(vid);
    const w = (ms.some(m => m.score == null) || ms.length < (side.need || 0)) ? ['logic-neutral', '기권'] : ms.every(m => m.score >= 70) ? ['logic-positive', '싼 편'] : ms.every(m => m.score < 30) ? ['logic-negative', '비싼 편'] : ['logic-neutral', '중간'];
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
    f"""      `S&P500 은행(대형 7·지역 6) 13곳 안에서 PER 순위를 매긴 값이다. COF 자신이 13곳에 없어 본인을 빼지 않고 13곳 모두와 비교한다.`
      + `\\nPER {SH['per']['current']:.1f}배는 {PEER['per']['peers']}곳 중 싼 쪽에서 {RK}번째라 {PEER['per']['score']}점이다(중앙값 {PEER['per']['median']:.1f}배).`
      + `\\n은행 규칙은 P/TBV·PER 두 배수가 같은 방향일 때만 표를 준다(COF는 둘 다 중간이라 0).`);""")
one("""      + `\\n(확인 필요 — NVDA 문장 자리)`
      + ``);""",
    f"""      + `\\nPER {SH['per']['current']:.1f}배(5년 중 하위 {SH['per']['percentile']:.0f}%, 중앙값 {SH['per']['median']:.1f}배). P/TBV {SH['ptbv']['current']:.2f}배(5년 중 상위 {100 - SH['ptbv']['percentile']:.0f}%).`
      + ``);""")

# 격자 계산 불가 칸(null) 보호(사전 등록 7-10 "—", Codex) — 지금 틀의 음수 시나리오 표기를 6절에서 이 형태로 되돌린다

# 은행 "계산 어려움" 신호(사전 등록: ① 기본 ROE_end < r ② b = 0 ③ 요구 ROE 해 없음) — 이 카드는 b = 0(카드 한정 JS, Codex 2026-10-01)
one("        nosol: () => '어떤 일정 성장률로도 현재가에 닿지 않는다',", "        nosol: () => '어떤 일정 성장률로도 현재가에 닿지 않는다',\n        b0: () => '유보율 0 — 이익보다 많이 돌려줘 장부가가 자라지 않는다(초과이익모형 신호, 사전 등록)',\n        roeend: () => '기본 시나리오 끝 ROE " + f'{R["roe_2y_median"] * 100:.1f}' + "% < 자기자본비용 10% — 장부가 위에 초과이익이 생기지 않는다(초과이익모형 신호, 사전 등록)',")
one('b.textContent = `⚠ 계산 어려움 ${D.hard.length}/5`;', "b.textContent = D.model === 'rim' ? `⚠ 모형 신호 ${D.hard.length}/3` : `⚠ 계산 어려움 ${D.hard.length}/5`;   // 은행 초과이익모형 신호는 3개(사전 등록)")

# 참고용(기권)인데 툴팁이 판정 단어만 보이던 것(카드 한정, Fable 2026-10-01)
one('→ ${lv.label} (${DCF_RULE_TEXT})` : (mMode', "→ ${lv.label}${d.referenceOnly ? ' — 참고용(데이터 점검 미통과로 기권)' : ''} (${DCF_RULE_TEXT})` : (mMode")
one("+ (lv.range ? '\\n' + lv.range : '') + (note ? '\\n' + note : '');", "+ (lv.range ? '\\n' + lv.range : '') + (note ? '\\n' + note : '') + (d.referenceOnly ? '\\n참고용 — 데이터 점검 미통과로 판정에 쓰지 않는다' : '');")

# 내재가치 탭 경고 분모·알약 툴팁도 은행 기준으로(Codex 2차)
one('note.textContent = (D.hard.length ? `⚠ 계산 어려움 ${D.hard.length}/5 — `', "note.textContent = (D.hard.length ? (D.model === 'rim' ? `⚠ 모형 신호 ${D.hard.length}/3 — ` : `⚠ 계산 어려움 ${D.hard.length}/5 — `)")
one("      + (lv.split ? '\\n보수~낙관 시나리오가 현재가를 사이에 둬, 가정에 따라 판정이 갈린다.' : '');", "      + (lv.split ? '\\n보수~낙관 시나리오가 현재가를 사이에 둬, 가정에 따라 판정이 갈린다.' : '')\n      + (D.referenceOnly ? '\\n참고용 — 데이터 점검 미통과로 판정에 쓰지 않는다' : '');   // 카드 한정")

# ── 5. 뉴스 ──
def item(dot, date, react, title, href, src):
    cls = f'tl-dot {dot}'.strip()
    rx = f'<span class="tl-reaction flat" data-react="{react}">0.0%</span>' if react else ''
    return (f'      <div class="tl-item">\n        <div class="{cls}"></div>\n        <div class="tl-date">{date}{rx}</div>\n'
            f'        <div class="tl-title">{title}</div>\n        <a class="tl-source" href="{href}" target="_blank" rel="noopener">{src} →</a>\n      </div>')


items = [
    ('neutral', '2026년 9월 15일 — 유로 사채 €1.5B 발행', None,
     '2032·2037년 만기 고정→변동 금리 선순위 채권 각 €750M', NOTES1, 'Capital One 공시 (SEC 8-K)'),
    ('neutral', '2026년 8월 20일 — 우선주 시리즈 M 상환 발표', None,
     '9월 1일 시리즈 M 우선주 $1.0B 전액 상환(주당 $1,000)', PREFM, 'Capital One 공시 (SEC 8-K)'),
    ('red', '2026년 7월 21일 장 마감 후 — Q2 2026 실적', '2026-07-22',
     'EPS $4.73·조정 $5.81 · 순수익 $15.9B(+27%) · 순이자마진 8.01% · 순상각률 3.23% · CET1 13.7% · 다음 날 주가 −2.4%', PR['q2'], 'Capital One 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 21일 장 마감 후 — Q1 2026 실적', '2026-04-22',
     'EPS $3.34·조정 $4.42 · 순수익 $15.2B · 대손비용 $4.1B · 다음 날 주가 −1.5%', PR['q1'], 'Capital One 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 7일 — Brex 인수 종결', None,
     '법인카드·지출관리 회사 Brex 인수를 마쳤다(종결 기준 현금 약 $2.56B + 보통주 1,064.6만 주, 1월 합의 $5.15B)', BREX1, 'Capital One 공시 (SEC 8-K)'),
    ('red', '2026년 1월 22일 장 마감 후 — Q4 2025 실적·Brex 인수 합의', '2026-01-23',
     'EPS $3.26·조정 $3.86 · 2025년 보통주 순이익 $2.2B · Brex 인수 합의($5.15B) · 다음 날 주가 −7.6%', PR['q4'], 'Capital One 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 21일 장 마감 후 — Q3 2025 실적', '2025-10-22',
     'EPS $4.83·조정 $5.95 · 순수익 $15.4B(+53%, Discover 포함) · 다음 날 주가 +1.5%', PR['q3'], 'Capital One 실적 보도자료 (SEC 8-K)'),
]
for it in items:
    assert it[2] is None or it[2] in days, it[2]
tl = '    <div class="timeline" id="newsTimeline">\n' + '\n'.join(item(*i) for i in items) + '\n    </div>'
sub(r'    <div class="timeline" id="newsTimeline">\n.*?\n    </div>\n    <div class="tl-pager"', tl + '\n    <div class="tl-pager"')
sub(r'<div class="section-title">시계열 주요 뉴스 \([^)]*\)</div>', '<div class="section-title">시계열 주요 뉴스 (2025.10 ~ 2026.09)</div>')
SUM = f"""<div class="verdict-summary-head">지배적 내러티브 · Discover 인수 1년, 분기 순수익이 $15B대로 커졌지만 주가는 1년 새 {(px / D[-253][4] - 1) * 100:+.0f}%<span class="tag">통합 진행·적정~고평가</span></div>
    <ol class="news-list">
      <li>2분기 순수익 $15.9B(+27%), 보통주 순이익 $2.9B, EPS $4.73·조정 $5.81였다. 1년 전 분기는 Discover 인수 초기 충당금으로 적자였다.</li>
      <li>순상각률이 3.23%로 1분기(3.45%)보다 낮아졌고, 대손충당금을 $662M 환입했다.</li>
      <li>상반기 자사주 $5.2B를 샀고(최근 4분기 환원율 {R_payout * 100:.0f}%), 4월에 Brex 인수를 마쳤다.</li>
    </ol>
    <div class="verdict-summary-counter">⚠️ 배수는 자기 이력·동종업 모두 중간이고, 현재가가 초과이익모형 기본 가치의 {lvl:.2f}배라 그 칸이 −2다 — 합계 −2 “적정~고평가”. {lvl:.2f}배는 −2 문턱(1.5)에 {(lvl / 1.5 - 1) * 100:.0f}% 붙어 있다 — 기본 가정의 2년 중앙값 ROE({f1(R["roe_2y_median"])})에 Discover 인수 초기 적자 분기가 8개 중 4개 창에 들어 있어서이고, 그 분기를 뺀 창만 쓰면 1.3배 안팎(−1)이다.</div>
    <div class="verdict-summary-next">🔍 다음 확인 포인트 · Q3 2026 실적(10월 하순 예상)의 순상각률과 Discover·Brex 통합 비용.</div>"""
sub(r'<div class="verdict-summary-head">지배적 내러티브.*?<div class="verdict-summary-next">.*?</div>', SUM)
row = lambda k, head, t: f'<div class="bb-row {k}"><span class="bb-icon">{"▲" if k == "bull" else "▼"}</span><span class="bb-head">{head}</span><span class="bb-text">{t}</span></div>'
bull = [('규모', '순수익 분기 $15.9B(+27%), 대출 $457.2B, 순이자마진 8.01%.'),
        ('신용', '순상각률 3.23%(1분기 3.45%), 2분기 충당금 $662M 환입.'),
        ('주주환원', '상반기 자사주 $5.2B, 분기 배당 $0.80(+33%).')]
bear = [('통합', 'Discover·Brex 통합 비용이 분기 세전 약 $0.4B 이어진다.'),
        ('주가', '실적 다음 날 네 번 중 세 번 하락(1월 −7.6%).'),
        ('신용카드 비중', '신용카드 대출이 전체 대출의 60%($275.4B)다.')]
m = re.search(r'(<div class="bb-title bb-bull">🐂 Bull 요인</div>\n)(.*?)(\n    </div>\n    <div class="bb-box">\n      <div class="bb-title bb-bear">🐻 Bear 요인</div>\n)(.*?)(\n    </div>\n  </div>)', h, re.S)
h = h[:m.start()] + m.group(1) + '\n'.join('      ' + row('bull', *b) for b in bull) + m.group(3) + '\n'.join('      ' + row('bear', *b) for b in bear) + m.group(5) + h[m.end():]
sub(r"const COF_ANALYST = \{[^}]*\};", "const COF_ANALYST = { asOf: '2026-10-05', source: 'StockAnalysis (의견 집계 · 개별 목표가)', rating: 'Buy', n: 23, nTargets: 18, mean: 258.44, median: 260,\n  low: 220, high: 300, strongBuy: 14, buy: 5, hold: 4, sell: 0, strongSell: 0 };")
sub(r'<span class="op-val">11월 중순 <span class="op-sub">Q3 FY27 예상</span></span>', '<span class="op-val">10월 하순 <span class="op-sub">Q3 2026 예상</span></span>')
# 세 시나리오 최소·최대 범위(이름 순서가 뒤집힌 카드, Codex)는 지금 틀에 들어 있다 — 주석만 이 카드 것으로
one("  const _mn = Math.min(D.low, D.base, D.high), _mx = Math.max(D.low, D.base, D.high);   // 세 시나리오 최소·최대(카드 한정)",
    "  const _mn = Math.min(D.low, D.base, D.high), _mx = Math.max(D.low, D.base, D.high);   // 세 시나리오 최소·최대(이름 순서가 뒤집힌 카드, Codex)")
one("    req.style.color = lv.color;   // 5단계와 같은 신호: 싸다 파랑 · 적정 노랑 · 비싸다 빨강",
    "    req.style.color = d.referenceOnly ? 'var(--gold)' : lv.color;   // 참고용(기권)이면 판정 색을 쓰지 않는다(카드 한정, Fable)")
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
# 음수 시나리오 표기(E2/E17/E25, 비금융 카드 일괄) 이전 형태 — 초과이익모형 격자는 null만 있다(사전 등록 7-10 "—")
one("  const every = SCN.flatMap(s => G.values[s[0]].flat()).filter(v => v != null && v > 0).concat(price != null ? [price] : []);   // 음수 칸 제외(카드 한정)",
    "  const every = SCN.flatMap(s => G.values[s[0]].flat()).filter(v => v != null).concat(price != null ? [price] : []);")
one("    pv.textContent = pick > 0 ? '주당 $' + (pick < 10 ? pick.toFixed(2) : Math.round(pick)) : '계산 불가(음수)'; pv.style.color = col;",
    "    pv.textContent = pick == null ? '계산 불가' : '주당 $' + Math.round(pick); pv.style.color = col;")
one("    if (price != null) { pu.textContent = pick > 0 ? '현재가 대비 ' + pct(pick) : '—'; pu.style.color = pick > 0 ? tone(pick) : ''; }",
    "    if (price != null) { pu.textContent = pick == null ? '—' : '현재가 대비 ' + pct(pick); pu.style.color = pick == null ? '' : tone(pick); }")

# ── 7. 판정 확인 · 헤더 단어 ──
_sv = lambda m: 1 if all(x['score'] >= 70 for x in m.values()) else -1 if all(x['score'] < 30 for x in m.values()) else 0
_d = 1 if lvl <= 0.7 else 1 if lvl <= 0.9 else 0 if lvl <= 1.1 else -1 if lvl <= 1.5 else -2   # "매우 싸다"도 +1만
_sum = _sv({'a': SH['ptbv'], 'b': SH['per']}) + _sv({'a': PEER['ptbv'], 'b': PEER['per']}) + _d   # 카드 식: 합 × 4 ÷ 무게(1+1+2) = 합
VERD = '저평가' if _sum >= 3 else '적정~저평가' if _sum >= 1 else '적정' if _sum > -1 else '적정~고평가' if _sum > -3 else '고평가'
assert (_sum, VERD) == (-2, '적정~고평가') and _d == -2, (_sum, _d)   # 자기 이력 0(PER 45·P/TBV 20) · 동종업 0(46·55) · 초과이익 1.54배 −2 → −2(문턱 1.5에 3% 붙음, 요약 문장)
h = h.replace('data-verdict style="font-size:22px;color:var(--gold);">적정~저평가</span>', f'data-verdict style="font-size:22px;color:var(--red);">{VERD}</span>', 1)   # 대체 색은 고평가 쪽 빨강(BAC·WFC와 같게, 2026-10-05)
one('<span class="vs-verdict" data-verdict>적정~저평가</span>', f'<span class="vs-verdict" data-verdict>{VERD}</span>')
open(p, 'w', encoding='utf-8').write(h)
print('votes sum', _sum, VERD)
print('ok base', R['기본'], 'ratio', round(lvl, 3), 'self', selfscore, 'peer', peerscore, 'req', R['required_roe'], 'band', FB['low'], FB['high'])
print('YoY', vec(cur), yd); print('QoQ', vec(qo), qd); print('roe_q', roe_q)
