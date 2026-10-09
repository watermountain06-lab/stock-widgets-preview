"""AXP(아메리칸 익스프레스) v2 카드 채우기 — BAC 스크립트(bac_fill.py)에서 옮김. 은행 세트 여섯 번째(비교군은 S&P500 은행 13곳, AXP는 비교군 밖).
 — clone + 배열 뒤에 실행. 데이터: v2/AXP_bank.json(adapters/bank_card.py).
Claude 추천 결정(사용자 위임, 리뷰 때 확인): AXP는 은행지주회사(CET1 규제)라 은행 세트로 둔다. 우선주는 태그 잔액이 없어 주식 수 × 청산가 $1,000,000(bank_rim.PREF_PRICE)으로 뺀다.
SEC 영업권 태그가 연말에만 있어 처음(10-01)에는 유형자본을 8분기 모두 만들 수 없었다(G1 미통과 → P/TBV 없음 → 두 배수 심판 기권 → 판정 보류).
관문 개정(사전 등록 9-1, 2026-10-05)으로 회사 값이 없는 항목은 확인 불가로 두어 G2(BVPS 대조)·G4가 통과하고, 6판 10-1(2026-10-05)로 영업권을
그 결산일 이전 가장 최근 값으로 400일까지 이어 써 8분기 모두 유형자본이 생겨 G1도 통과한다(회사가 TBVPS를 공시하지 않아 8분기 모두 확인 불가 —
G1은 회사 값과 대조한 것이 아니라 우리 TCE가 8분기 모두 있는지만 본 것이다). → P/TBV가 자기 이력·동종업에 들어가 판정이 나온다:
자기 이력 0(P/TBV 50.8·PER 56.2) · 동종업 −1(P/TBV·PER 모두 0점) · 초과이익 −2(현재가 ÷ 기본 1.74) = −3 → 고평가(2026-09-30 자료).
기반(base/axp_base.html)은 2026-10-05 지금 NVDA 틀을 clone_card.py AXP --force로 복제하고 axp_arrays.py <그때 v2 카드 사본>으로 배열(마지막 봉 2026-09-30)을 넣어
다시 만들었다(jpm_fill.py와 같은 방식). 은행 카드가 받지 않은 틀 변경은 6절에서 되돌린다."""
import json, os, re, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))   # v2(스크립트 위치 기준 — Actions에서도, 2026-10-06)
sys.path.insert(0, '.'); sys.path.insert(0, 'adapters')
import build_multiple_history as bmh
import bank_rim as br

T, CIK = 'AXP', '0000004962'
p = 'AXP_full_widget.html'; h = open(p, encoding='utf-8').read()


def one(o, n):
    global h
    c = h.count(o); assert c == 1, (c, o[:100]); h = h.replace(o, n)


def sub(pat, new, flags=re.S):
    global h
    m = list(re.finditer(pat, h, flags)); assert len(m) == 1, (len(m), pat[:90])
    h = h[:m[0].start()] + (new(m[0]) if callable(new) else new) + h[m[0].end():]


J = json.load(open('AXP_bank.json'))
R = J['rim']; SH = J['self']; PEER = J['peer']; FB = SH['fairBand']
assert J['gates'] == {'G1': True, 'G2': True, 'G5': True, 'G3': True, 'G4': True}, J['gates']; assert not R['reference_only'] and SH['ptbv'] is not None and PEER['ptbv']['score'] is not None   # 6판 10-1(영업권 이어쓰기) 뒤
assert J['gateRows']['G2']['unverifiable'] == 8 and J['gateRows']['G4']['unverifiable'] == 8   # 관문 개정(사전 등록 9-1, 2026-10-05): 회사 값이 없는 분기는 확인 불가로 둔다 → G2·G4 통과
G1R = J['gateRows']['G1']['rows']   # [분기말, 우리 TBVPS, 회사 TBVPS, 차이] — 회사 값이 없어 8분기 모두 확인 불가, 우리 TCE는 8분기 모두 있다(9-1·10-1)
assert J['gateRows']['G1']['unverifiable'] == 8 and len(G1R) == 8 and all(r[1] and r[2] is None for r in G1R), G1R
TB = {r[0]: r[1] for r in G1R}
assert SH['ptbv']['gapDays'] == 96 and SH['per']['gapDays'] == 0, SH['ptbv']['gapDays']   # 2021·2022년 말 주식 수 첫 접수가 2024-02-09라 2022·2023년 2~4월이 빈다(자기 이력 툴팁)   # 카드 계산 TBVPS(SEC 자본 − 우선주 − 영업권 − 무형자산) ÷ 주식 수
D = json.loads(re.search(r'const AXP_DAILY\s*=\s*(\[.*?\]);', h, re.S).group(1)); days = {r[0] for r in D}
px, asof = D[-1][4], D[-1][0]
assert abs(px - J['price']) < 1e-6 and asof == J['asOf']
bank = br.Bank(T, CIK, overrides=True)
GW_ = (max(e for e in bank.gw if e <= '2026-06-30'), bank.gw[max(e for e in bank.gw if e <= '2026-06-30')][0])   # 6판 10-1: 2026-06-30 TCE가 이어 쓴 영업권
assert GW_[0] == '2025-12-31' and '2026-06-30' not in bank.gw, GW_   # 영업권 태그는 연말에만 있다
S_, CE = R['shares'], R['ce']


def q(tags):
    _, rows = bmh.pick_tag(CIK, tags)
    return {e['end']: e['val'] for e in bmh.quarterly_flow(rows, T)}


# 분기 값은 보도자료(Q1'25·Q2'26 실적 보도자료 통계표)에서 손입력 — 순수익은 이자비용 차감 후, 순이익은 보통주 귀속(회사 표 A행)
L8E = ['2024-09-30', '2024-12-31', '2025-03-31', '2025-06-30', '2025-09-30', '2025-12-31', '2026-03-31', '2026-06-30']
rev = dict(zip(L8E, [x * 1e6 for x in [16636, 17179, 16967, 17856, 18426, 18980, 18907, 19637]]))
ni = dict(zip(L8E, [x * 1e6 for x in [2474, 2139, 2552, 2852, 2868, 2429, 2938, 3076]]))
nie = {'2026-06-30': 14482e6, '2026-03-31': 13878e6, '2025-06-30': 12901e6}      # 총비용(Total expenses)
prov = {'2026-06-30': 1084e6, '2026-03-31': 1251e6, '2025-06-30': 1405e6}       # 대손비용(Total provisions for credit losses)
nii = {'2026-06-30': 4649e6, '2026-03-31': 4692e6, '2025-06-30': 4187e6}        # 순이자이익
_xq = q(['RevenuesNetOfInterestExpense']); _nq = q(['NetIncomeLossAvailableToCommonStockholdersBasic'])
for _k in ('2026-06-30', '2026-03-31', '2025-06-30'):   # SEC 분기 값과 손입력이 맞는지(순이익은 참여주식 배분 차이 ±$20M 안 — 데이터 점검 G5와 같은 폭)
    assert abs(_xq[_k] - rev[_k]) < 1.5e6 and abs(_nq[_k] - ni[_k]) < 25e6, (_k, _xq.get(_k), _nq.get(_k))
ks = sorted(k for k in rev if k <= '2026-06-30')[-8:]
cur, yo, qo = ks[-1], ks[-5], ks[-2]
assert (cur, yo, qo) == ('2026-06-30', '2025-06-30', '2026-03-31'), ks
r1 = lambda v: round(v / 1e9, 1)
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
roe_q = [round(bank.roe(k)[0] * 100, 1) for k in ks]
SEC = 'https://www.sec.gov/Archives/edgar/data/4962/'
PR = {'q2': SEC + '000000496226000318/q226exhibit991.htm', 'q2s': SEC + '000000496226000318/q226exhibit992.htm',
      'q1': SEC + '000000496226000188/q126exhibit991.htm', 'q4': SEC + '000000496226000037/q425exhibit991.htm',
      'q3': SEC + '000000496225000218/q325exhibit991v2.htm'}
DIV = SEC + '000000496226000112/ex-991dividendmar22026fili.htm'
PREF = SEC + '000000496226000338/'   # 우선주 시리즈 E 발행·시리즈 D 상환 예정
TENQ = SEC + '000000496226000322/axp-20260630.htm'
f1 = lambda v: f'{v * 100:.1f}%'

# ── 1. 헤더 ──
one('<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +110%)</span>',
    f'<span class="meta-label">현재가 요구 ROE (5년 · 최근 4분기 {f1(R["roe0"])})</span>')
one('id="axpFairBand" style=', f'id="axpFairBand" title="최근 1년 PER 25~75% 구간({FB["per_p25"]:.1f}~{FB["per_p75"]:.1f}배) × 최근 4분기 EPS(10달러 단위 반올림)로 낸 PER만의 범위다. 판정은 P/TBV·PER 두 배수와 초과이익모형을 함께 보므로 이 범위와 따로 읽는다. 지금 PER({SH["per"]["current"]:.1f}배)이 1년 구간 아래라 현재가가 범위보다 낮다." style=')
h = re.sub(r'(id="axpFairBand"[^>]*>)[^<]*(</span>)', lambda m: m.group(1) + f'${FB["low"]} ~ ${FB["high"]}' + m.group(2), h, count=1)
one('<button class="ma-toggle-btn ma-off" data-ma="dcf" style="color:#38bdf8;border-color:#38bdf8;">◆ DCF 시나리오</button>',
    '<button class="ma-toggle-btn ma-off" data-ma="dcf" style="color:#38bdf8;border-color:#38bdf8;" hidden>◆ DCF 시나리오</button>')

# ── 2. 내재가치(RIM) 상수·격자·문장 ──
dcf = {"low": round(R['보수'], 2), "base": round(R['기본'], 2), "high": round(R['낙관'], 2), "requiredGrowth": R['required_roe'],
       "baseEquivGrowth": None, "reqMode": "roe", "requiredMargin": None, "marginNow": None, "roeNow": R['roe0'],
       "growth5y": None, "nonopPerShare": 0, "s2cFallback": False, "asOf": asof, "hard": (["b0"] if R["b"] == 0 else []), "hardDetail": {}, "tvShare": None,
       "model": "rim", "retention": R['b'], "bvps": R['bvps'], "referenceOnly": R['reference_only']}
sub(r'^const AXP_DCF = \{.*$', 'const AXP_DCF = ' + json.dumps(dcf, ensure_ascii=False) + ';   // 초과이익모형 — adapters/bank_card.py, research/bank_rim_prereg.md', re.M)
ends = {'보수': R['roe_5y_median'], '기본': R['roe_2y_median'], '낙관': R['roe0']}
waccs, lams = [0.08, 0.09, 0.10, 0.11, 0.12], [0.0, 0.5, 1.0]
vals = {n: [[round(br.rim_value(CE, R['roe0'], e, R['b'], r, lam) / S_, 2) if br.rim_value(CE, R['roe0'], e, R['b'], r, lam) else None
             for r in waccs] for lam in lams] for n, e in ends.items()}
grid = {"waccs": waccs, "terms": lams, "default": [0.10, 0.5], "values": vals, "kind": "rim"}
sub(r'^const AXP_DCF_GRID = \{.*$', 'const AXP_DCF_GRID = ' + json.dumps(grid, ensure_ascii=False) + ';   // 자기자본비용 × 잔존 수렴 비율(λ)', re.M)
sub(r'const AXP_DCF_TRACK = \[.*?\];', 'const AXP_DCF_TRACK = [];')
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
    f'<div class="note">세 값은 확률이 아니라, 과거 ROE에서 서로 다른 가정을 뽑아 계산한 결과다. 5년 뒤 ROE는 자기자본비용 쪽으로 절반 수렴한다고 본다(수렴 없음이면 기본 ${vals["기본"][0][2]:.0f}, 완전 수렴이면 ${vals["기본"][2][2]:.0f}). {"값을 더 크게 바꾸는 것은 수렴 가정이다" if (vals["기본"][0][2] - vals["기본"][2][2]) > (vals["기본"][1][0] - vals["기본"][1][4]) else "값을 더 크게 바꾸는 것은 자기자본비용이다"}(자기자본비용 8%면 ${vals["기본"][1][0]:.0f}, 12%면 ${vals["기본"][1][4]:.0f}). 수렴은 점진이 아니라 6년차에 한 번에 일어난다(기본은 ROE {f1(R["roe_2y_median"])}에서 {f1(0.10 + 0.5 * (R["roe_2y_median"] - 0.10))}로). 유보율 {f1(R["b"])}(최근 4분기 배당·자사주 환원 뒤 남는 몫)로 장부가 자라고, 기타포괄손익은 반영하지 않는다.' + (f' 2년 중앙값 ROE({f1(R["roe_2y_median"])})가 최근 4분기({f1(R["roe0"])})보다 조금 높아 기본(${R["기본"]:.0f})이 낙관(${R["낙관"]:.0f})보다 높게 나온다(이름과 순서가 뒤집힘). 세 ROE가 36.8~37.6%로 붙어 있어 세 값의 차이는 $4 안쪽이다.' if R['낙관'] < R['기본'] else '') + '</div>')
one("    ['현금흐름', lv.label in DV ? DV[lv.label] : null, lv.label, 2],",
    "    ['초과이익', lv.label in DV && !D.referenceOnly ? DV[lv.label] : null, D.referenceOnly ? '참고용' : lv.label, 2],   // 데이터 점검(G1·G2·G4) 미통과 → 참고용·기권(사전 등록 7-7)")
one("    dv.textContent = lv.label + (lv.split ? ' · 갈림' : '');",
    "    dv.textContent = d.referenceOnly ? '참고용 · 기권' : lv.label + (lv.split ? ' · 갈림' : '');   // 데이터 점검 미통과(사전 등록 7-7)")
one("    pill('dcf', lv.cls, lv.label + (lv.split ? ' · 갈림' : ''));", "    pill('dcf', D.referenceOnly ? 'mid' : lv.cls, D.referenceOnly ? '참고용 · 기권' : lv.label + (lv.split ? ' · 갈림' : ''));   // 데이터 점검 미통과(카드 한정)")
one('<div class="note" data-dcf-nonop>기본 시나리오 $314 = 사업 가치 $310 + 비영업 자산 $4(주당, 지분·장기투자)</div>', '<div class="note" data-dcf-nonop hidden></div>')
sub(r'<div class="reverse">.*?</div>\n  </div>', f'<div class="reverse" data-rim-reverse>지금 가격이 정당하려면 5년 동안 ROE가 매년 <b data-dcf-req>—</b>여야 하고, 그 뒤에도 절반만 수렴한 약 {f1(0.10 + 0.5 * (R["required_roe"] - 0.10))}가 이어져야 한다(탐색 상한 60% 바로 아래).</div>\n  </div>'
    if R["required_roe"] is not None else
    # 주가가 올라 요구 ROE가 탐색 상한 60%를 넘으면 해가 없다(2026-10-08 종가 $308.1) — 사전 등록의 nosol 신호, 판정 규칙은 그대로
    '<div class="reverse" data-rim-reverse>지금 가격이 정당하려면 5년 동안 ROE가 매년 탐색 상한 60%보다 높아야 한다 — 이 모형의 가정으로는 닿지 않는 가격이다.</div>\n  </div>')
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
selfscore = round((SH['ptbv']['score'] + SH['per']['score']) / 2, 1)   # 표시 점수는 두 배수 평균, 표는 두 배수가 같은 방향일 때만
peerscore = round((PEER['ptbv']['score'] + PEER['per']['score']) / 2, 1)
sub(r'const AXP_SCORES = \{.*?\n\};', f'''const AXP_SCORES = {{
  fundamental: null,   // 은행 — 일반 재무비율 산식이 맞지 않아 매기지 않는다
  peer: {peerscore},          // S&P500 은행 대비 P/TBV·PER 순위 평균(표시용). 표는 두 배수가 같은 방향일 때만
  selfHistory: {selfscore},   // P/TBV·PER 자기 5년 백분위 평균(표시용)
  asOf: "{asof}",
  fundamentalAsOf: "2026-06-30",   // Q2 2026 10-Q (2026-07-24 공시)
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
_rv, _ni = _ann('RevenuesNetOfInterestExpense'), _ann('NetIncomeLossAvailableToCommonStockholdersBasic')
CAGR_REV = ((_rv['2025-12-31'] / _rv['2020-12-31']) ** (1 / 5) - 1) * 100   # FY2020 → FY2025
CAGR_NI = ((_ni['2025-12-31'] / _ni['2020-12-31']) ** (1 / 5) - 1) * 100
NM_TTM = sum(ni[k] for k in ks[-4:]) / sum(rev[k] for k in ks[-4:]) * 100
LI = {x['end']: x['val'] for x in F_['Liabilities']['units']['USD']}; SE = {x['end']: x['val'] for x in F_['StockholdersEquity']['units']['USD']}
A = {x['end']: x['val'] for x in F_['Assets']['units']['USD']}
NA = '해당 없음'
frow = lambda m, lab, unit, v=None, note=None: {"metric": m, "label": lab, "unit": unit, "value": v, "points": None, "note": note}
fund = {"ticker": T, "basis": "quarter", "asOf": "2026-06-30", "filedAt": "2026-07-24", "score": None, "grade": None, "qualityFlags": ["financial"],
        "axes": {"health": {"rows": [frow("currentRatio", "유동비율", "%", note=NA), frow("quickRatio", "당좌비율", "%", note=NA),
                                     frow("debtDependency", "차입금의존도", "%", note=NA), frow("interestCoverage", "이자보상배율", "x", note=NA),
                                     frow("debtToEquity", "부채비율", "%", LI['2026-06-30'] / SE['2026-06-30'] * 100)], "points": None, "max": 33},
                 "growthProfit": {"rows": [frow("revenueCagr", "매출 CAGR", "%", CAGR_REV, "순수익(이자비용 차감 후) · 2020년은 코로나로 낮았던 해"), frow("opIncomeCagr", "순이익 CAGR", "%", CAGR_NI, "은행은 영업이익 대신 보통주 귀속 순이익 · 2020년 기저가 낮다"),
                                           frow("opMargin", "영업이익률(OPM)", "%", note=NA), frow("netMargin", "순이익률", "%", NM_TTM)], "points": None, "max": 34}},
        "note": "은행지주회사 — 예금이 부채라 유동·차입 비율이 뜻이 없고 v1 모델도 은행을 채점하지 않는다", "netCash": None}
sub(r'^const AXP_FUNDAMENTAL = \{.*$', 'const AXP_FUNDAMENTAL = ' + json.dumps(fund, ensure_ascii=False) + ';', re.M)
act = {"ticker": T, "status": "na", "reason": "은행지주회사(카드 대출·예금)라 매출채권·재고 회전으로 운영 효율을 판정하지 않는다"}
sub(r'^const AXP_ACTIVITY = \{.*$', 'const AXP_ACTIVITY = ' + json.dumps(act, ensure_ascii=False) + ';', re.M)
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
one('const y2min=40, y2max=75;', 'const y2min=0, y2max=50;')
one("labels:['Q3 FY25','Q4 FY25','Q1 FY26','Q2 FY26','Q3 FY26','Q4 FY26','Q1 FY27','Q2 FY27'],", 'labels:[' + ','.join(f"'{x}'" for x in L8) + '],')
one("{type:'line',label:'OPM(%)',", "{type:'line',label:'ROE(최근 4분기, GAAP, %)',")
one("{type:'bar',label:'매출($B)',", "{type:'bar',label:'순영업수익($B)',")
one("{type:'bar',label:'순이익($B)',", "{type:'bar',label:'순이익($B, 보통주 귀속)',")
for lab, nl, val, subt in [('FCF', 'CET1 비율 (Q2 2026)', '10.4%', '표준방식 · 목표 10~11% · 1분기 10.5%'),
                           ('Capex', '대손비용 (Q2 2026)', f'${prov[cur] / 1e9:.2f}B', f'1년 전 ${prov[yo] / 1e9:.2f}B · 순상각률 2.0%'),
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
extra = (xrow('CET1 비율 (표준방식)', '10.4%', 'CET1 자본 $27.8B ÷ 위험가중자산 $268.3B · 6월 말 기준, 2026.07.24 10-Q')
         + xrow('주당 장부가치 (BVPS)', '$48.42', '1년 전 $44.16 대비 +9.6% · 회사 발표')
         + xrow('주당 유형 장부가치 (TBVPS)', f'${TB[cur]:.2f}', f'카드 계산(회사 미공시) · 1년 전 ${TB[yo]:.2f} 대비 {(TB[cur] / TB[yo] - 1) * 100:+.1f}% · 영업권은 연말 값(2025년 말 ${GW_[1] / 1e9:.2f}B)을 이어 썼다 · 카드의 P/TBV 분모'))
sub(r'(<span class="diag-note" id="fundNetCashNote">[^<]*</span></div>\n        <div class="diag-badge info">ℹ️ 참고</div>\n      </div>\n)', lambda m: m.group(1) + extra)
sub(r'<div style="margin-top:14px;font-size:11\.5px;color:var\(--text2\);line-height:1\.6;">유동비율·당좌비율.*?</div>',
    f'<div style="margin-top:14px;font-size:11.5px;color:var(--text2);line-height:1.6;">AXP는 카드사지만 은행지주회사라 예금이 부채에 들어 있어 유동·당좌·차입 비율과 이자보상배율을 해당 없음으로 두고, 규제자본 비율과 장부가치를 대신 싣는다. 부채비율 {LI['2026-06-30'] / SE['2026-06-30'] * 100:,.0f}%는 고객 예금 $157.0B를 포함한 값이다. CET1 비율 10.4%는 회사 목표 범위(10~11%) 안이고 1년 전(10.6%)보다 조금 낮다.</div>')
vec = lambda e: [r1(rev[e]), r1(rev[e] - nie[e]), r1(ni[e]), r1(prov[e])]
f = lambda a, b: '%+.1f%%' % ((a / b - 1) * 100)
yd = [f(rev[cur], rev[yo]), f(rev[cur] - nie[cur], rev[yo] - nie[yo]), f(ni[cur], ni[yo]), f(prov[cur], prov[yo])]
qd = [f(rev[cur], rev[qo]), f(rev[cur] - nie[cur], rev[qo] - nie[qo]), f(ni[cur], ni[qo]), f(prov[cur], prov[qo])]
tq = lambda a: ', '.join(f"'{x}'" for x in a)
sub(r"curLabel: 'Q2 FY27', cmpLabel: 'Q2 FY26',\n    titleSuffix: '[^']*',\n    chart: \{ cur: \[[^\]]*\], cmp: \[[^\]]*\] \},\n    deltas: \[[^\]]*\],",
    f"curLabel: 'Q2 2026', cmpLabel: 'Q2 2025',\n    titleSuffix: 'YoY (Q2 2026 vs Q2 2025)',\n    chart: {{ cur: {vec(cur)}, cmp: {vec(yo)} }},\n    deltas: [{tq(yd)}],")
sub(r"curLabel: 'Q2 FY27', cmpLabel: 'Q1 FY27',\n    titleSuffix: '[^']*',\n    chart: \{ cur: \[[^\]]*\], cmp: \[[^\]]*\] \},\n    deltas: \[[^\]]*\],",
    f"curLabel: 'Q2 2026', cmpLabel: 'Q1 2026',\n    titleSuffix: 'QoQ (Q2 2026 vs Q1 2026)',\n    chart: {{ cur: {vec(cur)}, cmp: {vec(qo)} }},\n    deltas: [{tq(qd)}],")
fn = lambda a, extra='': (f"footnote: '기준일: 2026.06.30(Q2 2026) vs {a} · GAAP · 순수익은 이자비용 차감 후 · 충당금 전 이익 = 순수익 − 총비용 · 순이익은 보통주 귀속 · 대손비용은 늘면 나쁘다 · {extra}"
                f"<a href=\"{PR['q2']}\" target=\"_blank\" rel=\"noopener\">American Express Q2 2026 실적 보도자료 (SEC 8-K) →</a>'")
sub(r"footnote: '기준일: 2026\.07\.26\(Q2 FY27\) vs 2025\.07\.27\(Q2 FY26\)[^\n]*'", fn('2025.06.30(Q2 2025)'))
sub(r"footnote: '기준일: 2026\.07\.26\(Q2 FY27\) vs 2026\.04\.26\(Q1 FY27\)[^\n]*'", fn('2026.03.31(Q1 2026)'))
one('<span id="fundPeriodTitle">YoY (Q2 FY27 vs Q2 FY26)</span>', '<span id="fundPeriodTitle">YoY (Q2 2026 vs Q2 2025)</span>')
one("        labels: ['매출', '영업이익', '순이익', 'FCF'],", "        labels: ['순수익', '충당금 전 이익', '순이익', '대손비용'],")
one('// FCF = 영업현금흐름 − PaymentsToAcquireProductiveAssets, 분기값은 누적값의 차이.',
    '// 은행지주회사(카드): 순수익(이자비용 차감 후) · 충당금 전 이익(순수익 − 총비용) · 보통주 귀속 순이익 · 대손비용, 분기값은 보도자료 손입력.')
SEG = [('미국 소비자(USCS)', 9524, '#006fcf'), ('기업 카드(CS)', 4503, '#00175a'), ('국제 카드(ICS)', 3619, '#5aa9e6'), ('가맹점·네트워크(GMNS)', 2096, '#94a3b8')]
tot = sum(v for _, v, _ in SEG); assert abs(tot - 104 - round(rev[cur] / 1e6)) <= 1, tot   # 기업·기타(Corporate and Other) −$104M 차감 전(반올림 $1 차이)
leg = ''.join(f'\n          <div style="display:flex;align-items:center;gap:7px;font-size:11px;color:var(--text2);white-space:nowrap;"><span style="width:8px;height:8px;border-radius:50%;background:{c};display:inline-block;flex-shrink:0;"></span>{n} <strong style="color:var(--text);">${v / 1000:.1f}B · {v / tot * 100:.1f}%</strong></div>' for n, v, c in SEG)
sub(r'<div class="card-title">매출 구성 — Market Platform.*?</div>\n\n      <div style="display:flex;align-items:center;justify-content:center;gap:20px;">.*?\n      </div>\n\n      <div class="yoy-footnote" style="margin-top:14px;">.*?</div>',
    '<div class="card-title">순수익 구성 — 사업부별 (Q2 2026 · 2026.06.30 기준)</div>\n\n      <div style="display:flex;align-items:center;justify-content:center;gap:20px;">\n        <div class="chart-wrap" style="height:170px;width:170px;flex-shrink:0;">\n          <canvas id="segmentPieChart"></canvas>\n        </div>\n        <div style="display:flex;flex-direction:column;gap:9px;">' + leg +
    f'\n        </div>\n      </div>\n\n      <div class="yoy-footnote" style="margin-top:14px;">이자비용 차감 후 순수익, 기업·기타 −$0.10B 차감 전 · 1년 전보다 미국 소비자 +11%, 기업 카드 +7%, 국제 카드 +12%, 가맹점·네트워크 +8% · 출처: <a href="{PR["q2"]}" target="_blank" rel="noopener">American Express Q2 2026 실적 보도자료 (SEC 8-K) →</a></div>')
sub(r'// ─── 매출 구성 도넛 차트 \([^)]*\) ───', '// ─── 순수익 구성 도넛 차트 (부문 4개, 기업·기타 차감 전, 백만 달러) ───')
one('const total = 96221;', f'const total = {tot};')
one("labels:['Hyperscale','AI Clouds·Industrial·Enterprise','Edge Computing'],", 'labels:' + json.dumps([n for n, _, _ in SEG], ensure_ascii=False) + ',')
one('data:[48710, 40313, 7198],', 'data:[' + ', '.join(str(v) for _, v, _ in SEG) + '],')
sub(r"backgroundColor:\['#[0-9a-fA-F]{6}','#4d7a00','#3498db'\],", 'backgroundColor:' + json.dumps([c for _, _, c in SEG]) + ',')
R_payout = bank.payout_ttm(cur)[0] / bank.ni_ttm(cur)[0]
assert abs(R_payout - (1 - R['b'])) < 1e-6, (R_payout, R['b'])
CAPA = f"""<div class="card-title">자본배분 · 주주환원 (Q2 2026 · 2026.06.30 기준)</div>
      <div class="zone-list">
        <div class="zone-item">
          <span class="zone-label">자사주 매입 (Q2 2026, 710만 주 · 평균 $315.77)</span>
          <span class="zone-val">$2.2B</span>
        </div>
        <div class="zone-item">
          <span class="zone-label">보통주 배당 (Q2 2026, 분기 $0.95)</span>
          <span class="zone-val">$0.6B</span>
        </div>
        <div class="zone-item">
          <span class="zone-label">분기 배당 인상 (3월 2일 발표)</span>
          <div style="display:flex;align-items:center;gap:8px;">
            <span class="zone-tag" style="background:rgba(240,192,64,0.18);color:var(--gold);">$0.82 → $0.95</span>
            <span class="zone-val">+16%</span>
          </div>
        </div>
        <div class="zone-item">
          <span class="zone-label">최근 4분기 환원율 (SEC 배당 + 자사주 − 주식 발행, ÷ 보통주 순이익)</span>
          <span class="zone-val">{R_payout * 100:.0f}%</span>
        </div>
      </div>
      <div class="yoy-footnote" style="margin-top:14px;">남는 몫(유보율 {f1(R['b'])})으로 장부가가 자란다(초과이익모형 입력 b) · 2분기 환원은 보통주 순이익의 약 93%(10-Q) · 기말 주식 수는 1년 새 2,100만 주 줄었다(6.96억 → 6.75억) · 8월에 우선주 시리즈 E $1.6B를 발행하고 시리즈 D는 9월 15일 상환 예정이었다(완료 공시는 카드에 없음) · 출처: <a href="{TENQ}" target="_blank" rel="noopener">Q2 2026 10-Q →</a> · <a href="{DIV}" target="_blank" rel="noopener">배당 인상 (SEC 8-K)</a> · <a href="{PREF}" target="_blank" rel="noopener">우선주 (SEC 8-K)</a></div>
    </div>"""
sub(r'<div class="card-title">자본배분 · 주주환원 \(Q2 FY27 · 2026\.07\.26 기준\)</div>\n      <div class="zone-list">.*?\n      </div>\n    </div>', CAPA)
CHK = """<div class="card-title">다음 실적 체크포인트 <span style="color:var(--gold);font-weight:600;">2026년 10월 중순 (예상) · Q3 2026</span></div>
    <div style="font-size:12px;color:var(--text2);line-height:1.8;">
      <div style="margin-bottom:8px;"><strong style="color:var(--accent2);">①</strong> 순상각률과 충당금 환입 — 월별 8-K로 미국 소비자 카드 원금 기준 순상각률이 6월 1.4%에서 7·8월 1.7%로 올랐다</div>
      <div style="margin-bottom:8px;"><strong style="color:var(--accent2);">②</strong> 카드 회원 결제액 증가(2분기 +9%)와 올려 잡은 연간 매출 성장 10%</div>
      <div style="margin-bottom:8px;"><strong style="color:var(--accent2);">③</strong> 총비용(2분기 +12%, 플래티넘 카드 개편·혜택 이용)이 매출(+10%)보다 빨리 느는지</div>
      <div><strong style="color:var(--accent2);">④</strong> CET1 10~11% 목표 안에서 자사주 매입 속도(2분기 $2.2B)와 연간 EPS $17.30~17.90 유지</div>
    </div>"""
sub(r'<div class="card-title">다음 실적 체크포인트 <span[^>]*>[^<]*</span></div>\n    <div style="font-size:12px;color:var\(--text2\);line-height:1\.8;">.*?\n    </div>', CHK)

# ── 4. 밸류에이션 ──
one('<div class="vc-head">PBR</div>', '<div class="vc-head">P/TBV</div>')
one('<div class="vs-name" title="지난 5년 AXP 자신의 배수보다 지금이 얼마나 낮은가. 높을수록 싸다.">자기 이력 대비</div>',
    '<div class="vs-name" title="지난 5년 AXP 자신의 배수보다 지금이 얼마나 낮은가. 높을수록 싸다. 은행 규칙에 따라 P/TBV·PER 두 배수가 모두 70 이상이면 +1, 모두 30 미만이면 −1이다.">자기 이력 대비</div>')
one('<div class="vs-name" title="회사가 앞으로 벌어들일 현금만으로 계산한 주당 가치(기본 시나리오).">현금흐름 (내재가치)</div>',
    '<div class="vs-name" title="은행은 초과이익모형(장부가치 + 자기자본비용 10%를 넘는 이익의 현재가치)으로 계산한다. 기본 시나리오.">초과이익 (내재가치)</div>')
one('<span class="logic-tag">내재가치 <span class="logic-denom">현금흐름</span></span>', '<span class="logic-tag">내재가치 <span class="logic-denom">초과이익</span></span>')
one('<div class="vs-name" title="같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.">동종업 대비</div>',
    '<div class="vs-name" title="S&P500 은행(대형·지역 13곳) 대비 P/TBV·PER 순위. 높을수록 싸다. 두 배수가 같은 방향일 때만 표를 준다. AXP는 수수료 중심 카드사라 대출 중심 은행보다 ROE·배수가 구조적으로 높아 두 배수 순위가 맨 끝으로 몰린다(사업 모델별 비교는 참고로만 적는다, 은행 사전 등록 10-2).">동종업 대비</div>')
sub(r'<div class="vs-note">현재가 <span data-vs="price">[^<]*</span> 대비 <strong data-vs="upside">[^<]*</strong> · 기본 시나리오</div>',
    '<div class="vs-note">현재가 <span data-vs="price">—</span> 대비 <strong data-vs="upside">—</strong> · 초과이익모형 기본</div>')
one('<span class="val-name">PBR <span class="hist-note" data-hist="note"></span></span>', '<span class="val-name">P/TBV (유형 장부) <span class="hist-note" data-hist="note"></span></span>')
a_ = h.index('    </div>\n\n    <div class="card" style="display:flex;flex-direction:column;">')
h = h[:a_] + ('      <div style="font-size:11px;color:var(--text3);line-height:1.6;margin-top:6px;">은행은 매출·현금흐름·EBITDA 배수가 뜻이 없어 P/TBV·PER 두 배수만 본다. '
              f'P/TBV는 보통주 자본에서 영업권·무형자산을 뺀 유형 장부가치 기준인데, AXP는 회사가 TBVPS를 공시하지 않아 카드가 계산한다(6월 말 ${TB[cur]:.2f}). SEC 영업권 태그는 연말에만 있어 분기에는 직전 연말 값을 400일까지 이어 쓴다(은행 사전 등록 10-1, 6월 말은 2025년 말 ${GW_[1] / 1e9:.2f}B). '
              '회사 TBVPS가 없으니 이 가정을 회사 값으로 확인하지는 못했고, 데이터 점검 G1은 8분기 모두 유형자본이 만들어지는지만 봤다(8분기 모두 확인 불가). 보통주 자본은 SEC 자본 총계에서 우선주(주식 수 × 청산가 $1,000,000)를 뺀 값이고, 회사 발표 BVPS와 8분기 모두 0.4% 안에서 맞는다(최대 차이 $0.16, 2025년 말).</div>\n') + h[a_:]
wm = lambda k, m: {"metric": k, "score": round(m['score'], 1), "percentile": round(m['percentile'], 1), "current": round(m['current'], 2),
                   "min": round(m['min'], 2), "median": round(m['median'], 2), "max": round(m['max'], 2), "days": m['days'], "gapDays": m['gapDays']}
pm = lambda k, m: {"metric": k, "score": m['score'], "rank": m['rank'], "peers": m['peers']}
V = {"peer": {"score": peerscore, "rule": "both", "need": 2, "sector": "Financials (S&P500 은행)", "asOf": [asof, asof],
              "metrics": [pm('per', PEER['per']), pm('pbr', PEER['ptbv'])]},
     "self": {"score": selfscore, "rule": "both", "need": 2, "naNote": "은행", "window": [D[0][0], asof],
              "metrics": [wm('per', SH['per']), wm('pbr', SH['ptbv'])]}}   # 6판 10-1 뒤 P/TBV가 생겨 두 배수 규칙으로 표
sub(r'^const AXP_VALUATION = \{.*$', 'const AXP_VALUATION = ' + json.dumps(V, ensure_ascii=False) + ';', re.M)
U = {k: v for k, v in json.load(open('peer_universe/banks.json'))['tickers'].items() if k != T}   # 본인 제외
PB = ['JPM', 'USB', 'FITB', 'RF', 'MTB', 'HBAN']
mk = lambda k, key, title, unit, mx: {"title": title, "unit": unit, "max": mx, "msValue": None,
                                     "peers": [{"name": t, "value": round(U[t][key], 2), "status": "reference"} for t in PB if isinstance(U.get(t, {}).get(key), (int, float))]}
_mdy = (lambda d: f'{int(d[5:7])}/{int(d[8:])} 종가')(json.load(open('peer_universe/banks.json'))['asOf'])   # 차트 제목 날짜 = 비교군 기준일(2026-10-06, 손으로 적은 날짜가 갱신 뒤 남았다 — Fable)
MD = {"per": mk('per', 'per', f'S&P500 은행 PER 비교 · {_mdy} (13곳 중 6곳 표시)', 'PER(TTM)', 25),
      "pbr": mk('pbr', 'ptbv', f'S&P500 은행 P/TBV 비교 · {_mdy} (11곳 중 6곳 표시 · PNC·TFC는 유형자본 태그 결측)', 'P/TBV', 8)}   # 축 8 — AXP 7.41배가 잘리지 않게(카드 한정)
for k, nm, why in (('psr', 'PSR', '은행 매출에는 이자수익이 들어 있다'), ('pcr', 'PCR', '은행 현금흐름은 예금·대출 증감이 좌우한다'), ('evebitda', 'EV/EBITDA', '예금·차입이 영업 자금이라 기업가치가 뜻이 없다')):
    MD[k] = {"title": f'{nm} — 은행에 해당 없음 ({why})', "unit": nm, "max": 1, "msValue": None, "peers": []}
sub(r'const MULTIPLE_DATA = \{.*?\n\};\n', '// 은행 동종업(peer_universe/banks.json, 은행 사전 등록 §3) 중 6곳. 값이 없는 은행은 뺀다.\nconst MULTIPLE_DATA = ' + json.dumps(MD, ensure_ascii=False, indent=2) + ';\n')
one('<div class="card-title"><span id="multipleCompareTitle">글로벌 AI 반도체 PER 비교</span></div>', f'<div class="card-title"><span id="multipleCompareTitle">{MD["per"]["title"]}</span></div>')
lvl = px / R['기본']
_pt = [U[t]['ptbv'] for t in U if isinstance(U[t].get('ptbv'), (int, float))]; _pe = [U[t]['per'] for t in U if isinstance(U[t].get('per'), (int, float))]
n_pt, n_pe = sum(v > SH['ptbv']['current'] for v in _pt), sum(v > SH['per']['current'] for v in _pe)
assert len(_pt) == PEER['ptbv']['peers'] == 11 and len(_pe) == PEER['per']['peers'] == 13 and n_pt == 0 and n_pe == 0, (len(_pt), len(_pe), n_pt, n_pe)
assert max(_pt) < SH['ptbv']['current'] < MD['pbr']['max'], (max(_pt), SH['ptbv']['current'])
COF_ = json.load(open('COF_bank.json'))   # 같은 카드·소비자금융 모델(사전 등록 10-2, 참고 표시만 — 판정에 쓰지 않는다)
assert COF_['asOf'] == asof, COF_['asOf']   # 매일 재빌드는 COF를 AXP보다 먼저 돈다(daily_price.py BANKS 순서)
cof_txt = f'같은 카드·소비자금융 모델인 COF는 P/TBV {COF_["self"]["ptbv"]["current"]:.2f}배·PER {COF_["self"]["per"]["current"]:.1f}배로, {int(COF_["asOf"][5:7])}/{int(COF_["asOf"][8:])} 기준 참고일 뿐 판정에 쓰지 않는다 — 사전 등록 10-2'
sub(r'<div class="vs-premise">.*?</div>\n    <div class="verdict-summary-risk">.*?</div>',
    f'<div class="vs-premise">AXP는 카드사지만 은행지주회사(CET1 규제)라 은행 사전 등록의 고정 비교군인 S&P500 대형·지역 은행 {len(_pe)}곳과 비교한다. 수수료 중심(비이자수익이 순수익의 {14988 / 19637 * 100:.0f}%)·ROE 37%인 사업 구조 차이도 이 순위에 함께 들어 있다. P/TBV {SH["ptbv"]["current"]:.2f}배는 유형자본을 계산할 수 있는 은행 {len(_pt)}곳 모두보다 비싸고(중앙값 {PEER["ptbv"]["median"]:.2f}배), PER {SH["per"]["current"]:.1f}배도 {len(_pe)}곳 모두보다 비싸 동종업은 −1(비싸다)이다. 자기 이력에서는 두 배수 모두 중간(P/TBV 하위 {SH["ptbv"]["percentile"]:.0f}%·PER 하위 {SH["per"]["percentile"]:.0f}%)이라 0이다. <strong>초과이익모형 기본 가치(${R["기본"]:.0f})는 현재가의 {1 / lvl * 100:.0f}%라 −2(매우 비싸다)다</strong>. 합계 −3으로 “고평가”다. 회사가 유형 장부가치를 밝히지 않아 P/TBV는 카드 계산 값이고, SEC 영업권 태그가 연말에만 있어 분기에는 직전 연말 영업권을 400일까지 이어 쓴다(사전 등록 10-1, 2026-10-05). 회사 TBVPS가 없으니 이 값을 회사 값과 대조하지는 못했고, 데이터 점검 G1은 8분기 모두 유형자본이 만들어지는지만 확인했다. 보통주 자본은 회사 BVPS와 8분기 모두 0.4% 안에서 맞고(G2), 최근 4분기 환원 총액은 회사가 분기마다 내지 않아 확인 불가로 둔다(G4, 6월 스트레스 테스트 보도자료의 12개월 값 하나는 카드 계산과 맞는다).</div>\n'
    f'    <div class="verdict-summary-risk">⚠️ 현재가가 초과이익모형 기본 가치의 {lvl:.2f}배라 −2이고, 동종업 −1·자기 이력 0과 합쳐 “고평가”다. {"지금 가격은 ROE " + f1(R["required_roe"]) + "가 5년 이어진다는 값이다" if R["required_roe"] is not None else "지금 가격은 ROE가 5년 동안 60%를 넘어야 나오는 값이다"}(최근 4분기 {f1(R["roe0"])}). 다만 이 모형은 5년 뒤 ROE가 자기자본비용 쪽으로 절반 수렴한다고 보므로, ROE 37%가 이어지는 사업에는 낮게 나올 수 있다(수렴 없음이면 기본 ${vals["기본"][0][2]:.0f}). 동종업 −1도 대출 중심 은행과 견준 값이라 사업 구조 차이가 함께 들어 있다({cof_txt}).</div>')

# 판정 JS — 금융 규칙(두 배수가 같은 방향일 때만 표), 자기 이력·동종업 모두
assert h.count('`이 종목 자신의 5년 배수 분포에서 지금과 배수가 같거나 높았던 날의 비율을 점수로 쓴 값이다.`') == 1   # E13 문장은 지금 틀에 이미 있다
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
one("pill('self', ...byScore(V.self.score)); pill('peer', ...(V.peer.score == null ? ['mid', '표본 부족'] : byScore(V.peer.score)));",
    """const bothPill = s => (s.metrics.some(m => m.score == null) || s.metrics.length < (s.need || 0)) ? ['mid', '기권'] : s.metrics.every(m => m.score >= 70) ? ['', '싸다'] : s.metrics.every(m => m.score < 30) ? ['high', '비싸다'] : ['mid', '중간'];
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
    if (f('note')) f('note').textContent = (V.self.naNotes || {})[item.dataset.metric] || V.self.naNote || '';
    if (f('fill')) { f('fill').className = 'val-fill hist-fill mid'; f('fill').style.width = '0%'; }
    ['min', 'median', 'max'].forEach(k => { if (f(k)) f(k).textContent = '—'; });
  });
  ['peer', 'self'].forEach(k => {""")
one("  if (verdictOf(judges) === AXP_VERDICT) judges.slice(0, 2).forEach((j, i) => {",
    "  // 금융 카드는 심판 표가 sideVote(규칙별 — 두 배수가 같은 쪽일 때만 표)라 한 칸 바꾸기 계산이 맞지 않아 건너뛴다(Codex)\n  if (false) judges.slice(0, 2).forEach((j, i) => {")
one("""  // 두 밸류에이션 점수가 크게 갈리면 그 사실 자체가 정보다.""",
    """  [['self', 'axpSelfBox', 'axpSelfVerdict'], ['peer', 'axpPeerBox', 'axpPeerVerdict']].forEach(([k, bid, vid]) => {
    const side = AXP_VALUATION[k];   // 금융 규칙: 단어·색은 두 배수가 같은 방향일 때만 싼 편·비싼 편
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
    f"""      `S&P500 은행(대형 7·지역 6) 안에서 P/TBV·PER 순위를 매긴 값이다(표시 점수는 두 배수 평균). AXP 자신이 13곳에 없어 본인을 빼지 않고 비교한다.`
      + `\\nP/TBV {SH['ptbv']['current']:.2f}배는 유형자본을 만들 수 있는 {PEER['ptbv']['peers']}곳(중앙값 {PEER['ptbv']['median']:.2f}배), PER {SH['per']['current']:.1f}배는 {PEER['per']['peers']}곳(중앙값 {PEER['per']['median']:.1f}배) 모두보다 비싸 둘 다 0점 → −1이다. PNC·TFC는 유형자본 태그를 못 채워 P/TBV에서 빠졌다.`
      + `\\n수수료 중심 카드사라 대출 중심 은행보다 ROE·배수가 구조적으로 높다. {cof_txt}.`);""")
one("""      + `\\n(확인 필요 — NVDA 문장 자리)`
      + ``);""",
    f"""      + `\\nP/TBV {SH['ptbv']['current']:.2f}배(5년 중 하위 {SH['ptbv']['percentile']:.0f}%, 중앙값 {SH['ptbv']['median']:.2f}배)·PER {SH['per']['current']:.1f}배(하위 {SH['per']['percentile']:.0f}%, 중앙값 {SH['per']['median']:.1f}배)로 둘 다 중간이라 0이다.`
      + `\\nP/TBV는 카드 계산 값이다(회사 TBVPS 미공시). SEC 영업권 태그가 연말에만 있어 분기에는 직전 연말 값을 400일까지 이어 쓴다(사전 등록 10-1). 2021·2022년 말 주식 수가 SEC 데이터에 2024년에야 들어와 그 다음 해 2~4월 {SH['ptbv']['gapDays']}거래일은 P/TBV가 빈다.`
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
    ('neutral', '2026년 9월 15일 개장 전 — 8월 신용 지표', '2026-09-15',
     '미국 소비자 카드 원금 기준 순상각률 1.7%(6월 1.4%), 30일 연체율 1.1% 유지(월별 공시)', SEC + '000000496226000353/', 'American Express 공시 (SEC 8-K)'),
    ('neutral', '2026년 8월 5일 개장 전 — 우선주 공모', '2026-08-05',
     '비누적 우선주 시리즈 E 공모 발표(8월 12일 6.450%·$1.6B로 발행), 3.550% 시리즈 D 상환 목적', SEC + '000000496226000327/axp-20260805.htm', 'American Express 공시 (SEC 8-K)'),
    ('', '2026년 7월 24일 개장 전 — Q2 2026 실적', '2026-07-24',
     'EPS $4.53(+11%) · 매출 $19.6B(+10%) · 카드 결제액 +9% · 연간 매출 성장 가이던스 10%로 상향, EPS $17.30~17.90 유지', PR['q2'], 'American Express 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 6월 25일 장 마감 후 — 스트레스 테스트', '2026-06-26',
     '자체 스트레스 테스트 결과 발표 · 스트레스 자본 완충 2.5%(최저) 2027년 9월까지 유지 · 3월까지 12개월 환원 $8.7B', SEC + '000000496226000281/', 'American Express 공시 (SEC 8-K)'),
    ('', '2026년 4월 23일 개장 전 — Q1 2026 실적', '2026-04-23',
     'EPS $4.28(+18%) · 매출 $18.9B(+11%)', PR['q1'], 'American Express 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 2일 장 마감 후 — 배당 16% 인상', '2026-03-03',
     '분기 배당 $0.82 → $0.95', DIV, 'American Express 공시 (SEC 8-K)'),
    ('', '2026년 1월 30일 개장 전 — Q4 2025 실적', '2026-01-30',
     'EPS $3.53 · 2025년 순이익 $10.8B·EPS $15.38(+10%) · 2026년 매출 성장 9~10%·EPS $17.30~17.90 제시', PR['q4'], 'American Express 실적 보도자료 (SEC 8-K)'),
    ('', '2025년 10월 17일 개장 전 — Q3 2025 실적', '2025-10-17',
     'EPS $4.14(+19%) · 매출 $18.4B(+11%) · 미국 플래티넘 카드 개편 뒤 신규 가입이 개편 전의 두 배', PR['q3'], 'American Express 실적 보도자료 (SEC 8-K)'),
]
for it in items:
    assert it[2] is None or it[2] in days, it[2]
tl = '    <div class="timeline" id="newsTimeline">\n' + '\n'.join(item(*i) for i in items) + '\n    </div>'
sub(r'    <div class="timeline" id="newsTimeline">\n.*?\n    </div>\n    <div class="tl-pager"', tl + '\n    <div class="tl-pager"')
sub(r'<div class="section-title">시계열 주요 뉴스 \([^)]*\)</div>', '<div class="section-title">시계열 주요 뉴스 (2025.10 ~ 2026.09)</div>')
SUM = f"""<div class="verdict-summary-head">지배적 내러티브 · 카드 회원 결제액이 3년 만에 가장 빠르게(+9%) 늘어 연간 매출 가이던스를 올렸고, 주가는 1년 새 {(px / D[-253][4] - 1) * 100:+.0f}%<span class="tag">성장 가속·고평가</span></div>
    <ol class="news-list">
      <li>2분기 EPS $4.53(+11%), 매출 $19.6B(+10%), 회사 발표 분기 보통주 ROE(ROCE) 37.8%였다.</li>
      <li>카드 회원 결제액이 환율 조정 +9%로 3년 만에 가장 빨랐고, 연간 매출 성장 가이던스를 10%로 올렸다(EPS $17.30~17.90 유지).</li>
      <li>2분기 보통주 $2.9B를 돌려주고 3월에 배당을 $0.95로 16% 올렸다. 최근 4분기 순이익의 약 {R_payout * 100:.0f}%를 돌려줬다.</li>
    </ol>
    <div class="verdict-summary-counter">⚠️ 배수는 자기 이력에서 중간(0)이지만 S&P500 은행 대비로는 P/TBV·PER 모두 가장 비싸고(−1), 현재가가 초과이익모형 기본 가치의 {lvl:.2f}배라(−2) 합계 −3 “고평가”다. 다만 비교 은행은 대출 중심이고 초과이익모형은 ROE가 절반 수렴한다고 보므로, ROE 37%의 수수료 사업에는 두 칸 모두 불리하게 나온다.</div>
    <div class="verdict-summary-next">🔍 다음 확인 포인트 · Q3 2026 실적(10월 중순 예상)의 비용 증가 속도와, 월별 8-K에서 7·8월 1.7%로 오른 미국 소비자 순상각률.</div>"""
sub(r'<div class="verdict-summary-head">지배적 내러티브.*?<div class="verdict-summary-next">.*?</div>', SUM)
row = lambda k, head, t: f'<div class="bb-row {k}"><span class="bb-icon">{"▲" if k == "bull" else "▼"}</span><span class="bb-head">{head}</span><span class="bb-text">{t}</span></div>'
bull = [('수익성', '2분기 회사 발표 보통주 ROE(ROCE) 37.8%, EPS +11%, 순상각률 2.0%로 1년 전과 같다.'),
        ('성장', '카드 결제액 +9%, 순이자이익 +11%, 연회비 수익 +15%.'),
        ('주주환원', '2분기 환원 $2.9B(순이익의 약 93%), 배당 $0.95(+16%).')]
bear = [('밸류', f'P/TBV {SH["ptbv"]["current"]:.2f}배·PER {SH["per"]["current"]:.1f}배는 S&P500 은행 모두보다 높고(중앙값 {PEER["ptbv"]["median"]:.2f}배·{PEER["per"]["median"]:.1f}배), 현재가가 초과이익모형 기본 가치의 {lvl:.2f}배다.'),
        ('비용', '총비용 +12%(플래티넘 카드 개편·혜택 이용)가 매출 +10%보다 빠르다.'),
        ('규제', '카드 수수료·금리 상한 같은 규제 논의가 위험 요인으로 적혀 있다.')]
m = re.search(r'(<div class="bb-title bb-bull">🐂 Bull 요인</div>\n)(.*?)(\n    </div>\n    <div class="bb-box">\n      <div class="bb-title bb-bear">🐻 Bear 요인</div>\n)(.*?)(\n    </div>\n  </div>)', h, re.S)
h = h[:m.start()] + m.group(1) + '\n'.join('      ' + row('bull', *b) for b in bull) + m.group(3) + '\n'.join('      ' + row('bear', *b) for b in bear) + m.group(5) + h[m.end():]
sub(r"const AXP_ANALYST = \{[^}]*\};", "const AXP_ANALYST = { asOf: '2026-10-05', source: 'StockAnalysis (의견 집계 · 개별 목표가)', rating: 'Buy', n: 28, nTargets: 23, mean: 367.83, median: 370,\n  low: 300, high: 425, strongBuy: 9, buy: 5, hold: 14, sell: 0, strongSell: 0 };")
sub(r'<span class="op-val">11월 중순 <span class="op-sub">Q3 FY27 예상</span></span>', '<span class="op-val">10월 중순 <span class="op-sub">Q3 2026 예상</span></span>')
one("  const _mn = Math.min(D.low, D.base, D.high), _mx = Math.max(D.low, D.base, D.high);   // 세 시나리오 최소·최대(카드 한정)",   # 지금 틀에 이미 있다 — 주석만 이 카드 것으로
    "  const _mn = Math.min(D.low, D.base, D.high), _mx = Math.max(D.low, D.base, D.high);   // 세 시나리오 최소·최대(이름 순서가 뒤집힌 카드, Codex)")
one("      const color = (delta.startsWith('-') || delta.startsWith('−') || delta.includes('적자')) ? '#e74c3c' : '#2ecc71';",
    "      const _neg = (delta.startsWith('-') || delta.startsWith('−') || delta.includes('적자'));\n      const color = (i === 3 ? delta.startsWith('+') : _neg) ? '#e74c3c' : '#2ecc71';   // 4번째 막대 대손비용은 늘면 나쁘다(카드 한정, Codex)")
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
_d = 1 if lvl <= 0.7 else 1 if lvl <= 0.9 else 0 if lvl <= 1.1 else -1 if lvl <= 1.5 else -2
_js = (_sv({'a': SH['ptbv'], 'b': SH['per']}), _sv({'a': PEER['ptbv'], 'b': PEER['per']}), _d)
_sum = sum(_js)
VERD = '저평가' if _sum >= 3 else '적정~저평가' if _sum >= 1 else '적정' if _sum > -1 else '적정~고평가' if _sum > -3 else '고평가'
assert _js == (0, -1, -2) and (_sum, VERD) == (-3, '고평가'), (_js, _sum)   # 자기 이력 0 · 동종업 −1 · 초과이익 −2 → −3 → 고평가(6판 10-1 뒤, 2026-09-30 자료)
h = h.replace('data-verdict style="font-size:22px;color:var(--gold);">적정~저평가</span>', f'data-verdict style="font-size:22px;color:var(--red);">{VERD}</span>', 1)   # 대체 색 고평가 = 빨강(화면에서는 JS가 다시 칠한다)
one('<span class="vs-verdict" data-verdict>적정~저평가</span>', f'<span class="vs-verdict" data-verdict>{VERD}</span>')
open(p, 'w', encoding='utf-8').write(h)
print('votes', _js, 'sum', _sum, VERD)
print('ok base', R['기본'], 'ratio', round(lvl, 3), 'self', selfscore, 'peer', peerscore, 'req', R['required_roe'], 'band', FB['low'], FB['high'])
print('YoY', vec(cur), yd); print('QoQ', vec(qo), qd); print('roe_q', roe_q)
