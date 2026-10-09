# 수익률 없는 점검 요약 — 패널 행(평가일 값)만 쓴다. 가격 파일·add_returns를 부르지 않는다.
import sys, os, json, math, collections, statistics as st
R="/Users/watermountain/Workspace/stock-widgets-preview/v2/research"
sys.path.insert(0,R); os.chdir(R)
import verdict_replay as vr, gate_membership as gm
def load(p): return json.load(open(p))["rows"]
T=load("gate_test_panel.json"); L=load("verdict_replay_panel.json")
L=[r for r in L if "2024-10"<=r["m"]<="2026-03"]          # 학습 구간
mem=json.load(open("gate_membership.json"))["tickers"]
for r in T: r["mem"]=gm.member_at(mem.get(r["t"]), r["d"])
for rows in (T,L):
    vr.peer_scores(rows); vr.assign(rows)
o=[]; P=lambda *a: o.append(" ".join(map(str,a)))
def q(xs,ps=(0.05,0.25,0.5,0.75,0.95)):
    xs=sorted(x for x in xs if x is not None and math.isfinite(x)); n=len(xs)
    return [round(xs[min(n-1,int(p*n))],2) for p in ps] if xs else []
def pct(a,b): return f"{100*a/b:.1f}%" if b else "-"
P("# 수익률 없는 점검 요약 (시험 2021-10~2024-03 / 학습 2024-10~2026-03)\n")
P("## 행·구성종목"); P("시험 행",len(T),"구성종목 True",sum(r['mem'] is True for r in T),"False",sum(r['mem'] is False for r in T),"None",sum(r['mem'] is None for r in T),"| 학습 행",len(L))
TM=[r for r in T if r["mem"] is True]
P("\n## 월별 (시험, 구성종목만): 월 행 dcf_ok self앉음 peer앉음 판정있음(V0) dq있음")
for m in sorted({r['m'] for r in TM}):
    g=[r for r in TM if r['m']==m]; n=len(g)
    P(m,n,pct(sum(r['dcf_ok'] for r in g),n),pct(sum(r['self_vote'] is not None for r in g),n),pct(sum(r['peer_vote'] is not None for r in g),n),pct(sum(r['g_V0'] is not None for r in g),n),pct(sum(bool(r['dq']) for r in g),n))
P("\n## 월별 (학습)")
for m in sorted({r['m'] for r in L}):
    g=[r for r in L if r['m']==m]; n=len(g)
    P(m,n,pct(sum(r['dcf_ok'] for r in g),n),pct(sum(r['self_vote'] is not None for r in g),n),pct(sum(r['peer_vote'] is not None for r in g),n),pct(sum(r['g_V0'] is not None for r in g),n),pct(sum(bool(r['dq']) for r in g),n))
for name,rows in (("시험(구성종목)",TM),("학습",L)):
    n=len(rows)
    P(f"\n## 칸별 분포 — {name}")
    P("self_score 5/25/50/75/95%",q([r['self_score'] for r in rows]))
    P("peer_score 5/25/50/75/95%",q([r.get('peer_score') for r in rows]))
    P("D=-ln(px/base) 5/25/50/75/95% (base>0)",q([r['D'] for r in rows if r['D'] is not None]))
    P("self_vote",dict(collections.Counter(r['self_vote'] for r in rows)))
    P("peer_vote",dict(collections.Counter(r['peer_vote'] for r in rows)))
    P("lv_V0",{k:pct(v,n) for k,v in collections.Counter(r['lv_V0'] for r in rows).items()})
    P("g_V0",{k:pct(v,n) for k,v in collections.Counter(r['g_V0'] for r in rows).items()})
    P("dcf_why",dict(collections.Counter(r.get('dcf_why') for r in rows if not r['dcf_ok']).most_common(8)))
    P("dq 종류",dict(collections.Counter(str(x).split(':')[0].split('(')[0] for r in rows for x in r['dq']).most_common(10)))
    P("섹터별 dcf_ok",{s:pct(sum(r['dcf_ok'] for r in rows if r['sec']==s),sum(r['sec']==s for r in rows)) for s in sorted({r['sec'] for r in rows})})
P("\n## 이상값 (시험, 구성종목)")
for lab in vr.METRICS:
    xs=[(r['peer'].get(lab),r['t'],r['m']) for r in TM if isinstance(r['peer'].get(lab),(int,float))]
    xs.sort(); P(lab,"n",len(xs),"최저",[(round(a,2),t,m) for a,t,m in xs[:3]],"최고",[(round(a,1),t,m) for a,t,m in xs[-5:]])
bt=collections.defaultdict(list)
for r in TM: bt[r['t']].append(r)
jumps=[]; pxj=[]
for t,g in bt.items():
    g.sort(key=lambda r:r['m'])
    for a,b in zip(g,g[1:]):
        if a['base'] and b['base'] and a['base']>0 and b['base']>0 and max(a['base']/b['base'],b['base']/a['base'])>3: jumps.append((t,a['m'],b['m'],round(a['base'],1),round(b['base'],1)))
        if max(a['px']/b['px'],b['px']/a['px'])>2: pxj.append((t,a['m'],b['m'],round(a['px'],2),round(b['px'],2)))
P("기본 내재가치 한 달에 3배 넘게 변한 경우",len(jumps),jumps[:25])
P("평가일 종가 한 달에 2배 넘게 변한 경우(분할 처리 점검)",len(pxj),pxj[:25])
ext=sorted([r for r in TM if r['base'] is not None and r['base']!=0],key=lambda r:r['base'])
P("기본 내재가치 최저 5",[(r['t'],r['m'],round(r['base'])) for r in ext[:5]],"최고 5",[(r['t'],r['m'],round(r['base']),round(r['px'])) for r in ext[-5:]])
P("\n## 시험 구간에만 dcf_ok 0인 종목(학습은 계산됨)")
lt={r['t'] for r in L if r['dcf_ok']}; z=[t for t,g in bt.items() if not any(r['dcf_ok'] for r in g)]
P("시험 전부 결측",len(z),"그중 학습 계산됨",sorted(t for t in z if t in lt))
P("\n## 태그 전환 리츠 행(UDR·AMT·CCI·ESS·EXR·CPT) — 계산된 행 수",{t:sum(r['dcf_ok'] for r in bt.get(t,[])) for t in ("UDR","AMT","CCI","ESS","EXR","CPT")})
open("/private/tmp/claude-501/-Users-watermountain-Workspace-second-brain/bbfd380b-94a7-4972-94ba-641e4f0c0be6/scratchpad/rfv/summary.md","w").write("\n".join(o)+"\n")
print("\n".join(o))
