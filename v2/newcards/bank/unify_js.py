"""은행 카드 9장의 화면 코드를 한 규칙으로 맞춘다(은행 개선 1단계, 2026-10-05 사용자 결정). 채우기 스크립트 뒤에 돌린다 — 여러 번 돌려도 같다.

- 세 번째 칸 이름은 '초과이익', 관문 미통과(referenceOnly)면 참고용·기권(사전 등록 7-7) — C·GS·JPM·MS에 빠져 있던 조건
- 모형 신호 3개를 한 규칙으로: roeend(기본 시나리오 끝 ROE < 10%), b0(유보율 0), nosol(요구 ROE가 0~60% 밖) — 채우기 스크립트마다 달랐다
- 배지·문구 '모형 신호 n/3', 요약 칸 요구 ROE가 없으면 '해 없음'('0.0%'로 찍히던 것)

    python3 v2/newcards/bank/unify_js.py            # 9장 모두
    python3 v2/newcards/bank/unify_js.py WFC        # 한 장
"""
import glob,json,os,re,collections,sys
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BANKS=sys.argv[1:] or ["AXP","BAC","C","COF","GS","JPM","MS","SCHW","WFC"]
JUDGE_OLD=[ "['현금흐름', lv.label in DV ? DV[lv.label] : null, lv.label, 2],",
            "['초과이익', lv.label in DV ? DV[lv.label] : null, lv.label, 2],"]
JUDGE_NEW="['초과이익', lv.label in DV && !D.referenceOnly ? DV[lv.label] : null, D.referenceOnly ? '참고용' : lv.label, 2],   // 관문 미통과 → 참고용·기권(사전 등록 7-7) — 은행 9장 공통(2026-10-05)"
TEXT=[('현금흐름이 "매우 싸다"여도 +1만 준다','초과이익이 "매우 싸다"여도 +1만 준다'),
      ('→ 현금흐름 기준값이 밴드','→ 초과이익 기준값이 밴드')]
BADGE="        b.className = 'vs-hard'; b.textContent = D.model === 'rim' ? `⚠ 모형 신호 ${D.hard.length}/3` : `⚠ 계산 어려움 ${D.hard.length}/5`;   // 은행 초과이익모형 신호는 3개(사전 등록) — 9장 공통 표기(2026-10-05)"
NOTE="        note.textContent = (D.hard.length ? (D.model === 'rim' ? `⚠ 모형 신호 ${D.hard.length}/3 — ` : `⚠ 계산 어려움 ${D.hard.length}/5 — `) + D.hard.map(k => (TXT[k] ? TXT[k]() : k).split(' — ')[0]).join(' · ') + ' · ' : '') + tv;"
TXT_BANK=("        nosol: () => D.model === 'rim' ? '현재가를 맞추는 ROE가 탐색 범위(0~60%) 밖이다(초과이익모형 신호, 사전 등록)' : '어떤 일정 성장률로도 현재가에 닿지 않는다',\n"
          "        b0: () => '유보율 0 — 이익보다 많이 돌려줘 장부가가 자라지 않는다(초과이익모형 신호, 사전 등록)',\n"
          "        roeend: () => `기본 시나리오 끝 ROE ${D.roeTarget != null ? pct(D.roeTarget) : '—'} < 자기자본비용 10% — 장부가 위에 초과이익이 생기지 않는다(초과이익모형 신호, 사전 등록)`,")
REQ_OLD=": (D.requiredGrowth * 100).toFixed(1) + '%')"
REQ_NEW=": (D.requiredGrowth != null ? (D.requiredGrowth * 100).toFixed(1) + '%' : '해 없음'))"
def patch(h, tag):
    c=collections.Counter()
    for o in JUDGE_OLD:
        if h.count(o)==1: h=h.replace(o,JUDGE_NEW); c["judge"]+=1
    for a,b in TEXT:
        if h.count(a)==1: h=h.replace(a,b); c["text"]+=1
    h,n=re.subn(r"^\s*b\.className = 'vs-hard'; b\.textContent = .*$",lambda m:BADGE,h,count=1,flags=re.M); c["badge"]+=n
    h,n=re.subn(r"^\s*note\.textContent = \(D\.hard\.length \? .*$",lambda m:NOTE,h,count=1,flags=re.M); c["note"]+=n
    h=re.sub(r"^\s*(b0|roeend): \(\) => .*\n","",h,flags=re.M)
    h,n=re.subn(r"^\s*nosol: \(\) => .*$",lambda m:TXT_BANK,h,count=1,flags=re.M); c["txt"]+=n
    if h.count(REQ_OLD)==1: h=h.replace(REQ_OLD,REQ_NEW); c["req"]+=1
    return h,c
# 틀(NVDA)·생성기에 나중에 들어간 공통 수정 — 은행 기반 HTML은 그 전에 만들어져 다시 만들면 빠진다(2026-10-05)
import ast as _ast
_FILL = os.path.join(ROOT, "v2", "newcards", "fill.py")
_tree = _ast.parse(open(_FILL, encoding="utf-8").read())
NEG = sorted([( n.lineno, _ast.literal_eval(n.args[0]), _ast.literal_eval(n.args[1])) for n in _ast.walk(_tree)
              if isinstance(n, _ast.Call) and getattr(n.func, "id", None) == "one_done"])
LATER = [("이 종목 자신의 5년 배수 분포에서 현재값이 하위 몇 %인지를 점수로 쓴 값이다.", "이 종목 자신의 5년 배수 분포에서 지금과 배수가 같거나 높았던 날의 비율을 점수로 쓴 값이다."),
         ("이 종목 자신의 5년 배수 분포에서 지금보다 배수가 높았던 날의 비율을 점수로 쓴 값이다.", "이 종목 자신의 5년 배수 분포에서 지금과 배수가 같거나 높았던 날의 비율을 점수로 쓴 값이다."),
         ("const clipDcf = v => Math.min(DCF_CAP_HI, v);", "const clipDcf = v => Math.max(0, Math.min(DCF_CAP_HI, v));   // 음수 시나리오는 0에 그린다 — 실제 값은 툴팁(E17, 2026-10-05)"),
         ("? dcfVisible.map(t => clipDcf(t.base))", "? dcfVisible.map(t => t.base).filter(v => v > 0).map(clipDcf)   // 겹침 모드도 음수는 축에서 뺀다(E17)")]
_REPL_LINE = next(i for i, l in enumerate(open(_FILL, encoding="utf-8").read().split("\n"), 1) if l.startswith("h = h.replace(\"'$' + Math.round(d.base)\""))
REPL = [("'$' + Math.round(d.base)", "'$' + (Math.abs(d.base) < 10 ? d.base.toFixed(2) : Math.round(d.base))"),
        ("'$' + Math.round(D.base)", "'$' + (Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base))")]


def later_fixes(h, c):
    """음수 내재가치 표시(E2·E17·E25)·자기 이력 툴팁(E13) — 생성기 규칙을 같은 순서로(옛 문자열이 하나 있을 때만, 새 문자열이 있으면 건너뜀)."""
    def apply(pairs):
        nonlocal h
        for _, a, b in pairs:
            if b not in h and h.count(a) == 1:
                h = h.replace(a, b); c["neg"] += 1
    apply([x for x in NEG if x[0] < _REPL_LINE])           # 생성기에서 REPL보다 앞선 것
    for a, b in REPL:
        if a in h:
            h = h.replace(a, b)
    apply([x for x in NEG if x[0] > _REPL_LINE])
    for a, b in LATER:
        if b not in h and a in h:
            h = h.replace(a, b); c["later"] += 1
    return h


def hard_rule(r):
    return (["roeend"] if r["roe_2y_median"] < 0.10 else []) + (["b0"] if r["b"] == 0 else []) + (["nosol"] if r.get("required_roe") is None else [])
dec=json.JSONDecoder()
for T in BANKS:
    p=os.path.join(ROOT,"v2",f"{T}_full_widget.html"); h=open(p,encoding="utf-8").read()
    h,c=patch(h,T)
    h=later_fixes(h,c)
    k=f"const {T}_DCF = "; i=h.index(k)+len(k); D,e=dec.raw_decode(h,i)
    r=json.load(open(os.path.join(ROOT,"v2",f"{T}_bank.json")))["rim"]
    old=D.get("hard"); D["hard"]=hard_rule(r); D["roeTarget"]=r["roe_2y_median"]
    h=h[:i]+json.dumps(D,ensure_ascii=False)+h[e:]
    open(p,"w",encoding="utf-8").write(h); print(T,dict(c),"hard",old,"->",D["hard"])
