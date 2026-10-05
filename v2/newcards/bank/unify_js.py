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
def hard_rule(r):
    return (["roeend"] if r["roe_2y_median"] < 0.10 else []) + (["b0"] if r["b"] == 0 else []) + (["nosol"] if r.get("required_roe") is None else [])
dec=json.JSONDecoder()
for T in BANKS:
    p=os.path.join(ROOT,"v2",f"{T}_full_widget.html"); h=open(p,encoding="utf-8").read()
    h,c=patch(h,T)
    k=f"const {T}_DCF = "; i=h.index(k)+len(k); D,e=dec.raw_decode(h,i)
    r=json.load(open(os.path.join(ROOT,"v2",f"{T}_bank.json")))["rim"]
    old=D.get("hard"); D["hard"]=hard_rule(r); D["roeTarget"]=r["roe_2y_median"]
    h=h[:i]+json.dumps(D,ensure_ascii=False)+h[e:]
    open(p,"w",encoding="utf-8").write(h); print(T,dict(c),"hard",old,"->",D["hard"])
