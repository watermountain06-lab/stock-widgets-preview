"""루트 카드(70장)가 있는 종목의 배열(일봉·이동평균·백테스트)과 헤더 현재가를 루트 카드에서 옮긴다. 사용: python3 v2/newcards/root_arrays.py VZ [원본 카드 경로]
원본 경로를 주면 루트 카드 대신 그 파일(예: 지금 v2 카드의 사본)에서 옮긴다 — build.py --from-card(재현 모드, 2026-10-05)."""
import json,re,os,subprocess,sys
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
T=sys.argv[1].upper()
root=open(sys.argv[2] if len(sys.argv)>2 else f'{T}_full_widget.html',encoding='utf-8').read(); p=f'v2/{T}_full_widget.html'; h=open(p,encoding='utf-8').read()
def span(s, name, t=None):
    a=s.index(f'const {t or T}_{name} '); st=s.index('[',a); d=0; ins=None
    for i in range(st,len(s)):
        c=s[i]
        if ins:
            if c==ins and s[i-1]!='\\': ins=None
            continue
        if c in '"\'': ins=c
        elif c=='[': d+=1
        elif c==']':
            d-=1
            if d==0: return st,i+1
# 루트 카드에 없는 배열(2026-10-06): 이동평균은 일봉으로 계산하고, 백테스트는 예전 v2 카드(FALLBACK, build.py가 덮어쓰기 전에 떠 둔 사본)의 것을 쓴다 —
# INTC 루트는 적자라 BACKTEST가 없고, SKHY 루트는 이력이 짧아 MA60·MA120·BACKTEST가 없다.
FALLBACK=os.environ.get('ROOT_ARRAYS_FALLBACK')
dec=json.JSONDecoder()
# 백테스트는 루트 카드가 아니라 다시 만들기 전 카드(FALLBACK) 자신의 것을 쓴다(2026-10-08). 10/6 전체 갱신(0e72737)이 루트 카드의
# 옛 배열을 가져와 refresh_backtest.py로 다시 계산한 배열(C1 구간 표시·일회성 세금·환율 처리)을 93장에서 지웠고, 루트에 배열이 없던
# INTC·SKHY에는 틀(NVDA)의 배열이 남았다. 백테스트는 refresh_backtest.py만 바꾼다.
OWN_BT=None
if FALLBACK and os.path.exists(FALLBACK):
    fb0=open(FALLBACK,encoding='utf-8').read()
    if f'const {T}_BACKTEST ' in fb0:
        fs0,fe0=span(fb0,'BACKTEST'); OWN_BT=fb0[fs0:fe0]
for n in ['DAILY','MA5','MA20','MA60','MA120','BACKTEST']:
    hs,he=span(h,n)
    if n=='BACKTEST' and OWN_BT is not None:
        seg=OWN_BT
    elif f'const {T}_{n} ' in root:
        rs,re_=span(root,n); seg=root[rs:re_].replace("'", '"')   # DELL 루트는 작은따옴표 날짜
    elif n.startswith('MA'):
        k=int(n[2:]); D0=dec.raw_decode(h,h.index('[',h.index(f'const {T}_DAILY')))[0]
        seg=json.dumps([None if i+1<k else round(sum(r[4] for r in D0[i+1-k:i+1])/k,2) for i in range(len(D0))])
    elif FALLBACK and os.path.exists(FALLBACK):
        fb=open(FALLBACK,encoding='utf-8').read(); fs,fe=span(fb,n); seg=fb[fs:fe]
        print(f'arrays ⚠ {n}: 루트 카드에 없어 예전 v2 카드의 것을 쓴다({FALLBACK}) — 백테스트는 갱신되지 않는다')
    else:
        raise SystemExit(f'{T}: 루트 카드에 {n}가 없다(ROOT_ARRAYS_FALLBACK으로 예전 카드를 주면 그것을 쓴다)')
    h=h[:hs]+seg+h[he:]
# 틀(NVDA)의 백테스트가 그대로 남았으면 멈춘다 — 다른 종목 카드에 NVDA 밴드가 실린다(INTC·SKHY 2026-10-06)
if T!='NVDA':
    tpl=open('v2/newcards/template/NVDA_template.html',encoding='utf-8').read()
    ts,te=span(tpl,'BACKTEST','NVDA'); bs,be=span(h,'BACKTEST')
    js=lambda x: json.loads(subprocess.run(['node','-e',f'process.stdout.write(JSON.stringify({x}))'],capture_output=True,text=True,check=True).stdout)
    key=lambda arr: {(c['checkpoint_date'],c['predicted_low'],c['predicted_high']) for c in arr}
    same=key(js(h[bs:be]))&key(js(tpl[ts:te]))
    if len(same)>=3:
        raise SystemExit(f'{T}: 백테스트 체크포인트 {len(same)}개가 틀(NVDA)과 날짜·밴드까지 같다 — refresh_backtest.py로 다시 만들거나 비워야 한다')
D=dec.raw_decode(h,h.index('[',h.index(f'const {T}_DAILY')))[0]
for n,k in [('MA5',5),('MA20',20),('MA60',60),('MA120',120)]:
    m=dec.raw_decode(h,h.index('[',h.index(f'const {T}_{n}')))[0]
    last=next((x for x in reversed(m) if x is not None), None)   # 이력이 짧으면(SKHY) 전부 빈 값일 수 있다
    print(n,len(m),len(D), m[-1] if m else None, round(sum(r[4] for r in D[-k:])/k,2))
last,prev=D[-1],D[-2]; c=(last[4]/prev[4]-1)*100; up=c>=0
new=f'<div class="price-main"><span class="price-change" style="color:var(--{"green" if up else "red"});">{"▲ +" if up else "▼ −"}{abs(c):.2f}%</span> ${last[4]:.2f}</div>'
h=re.sub(r'<div class="price-main">.*?</div>',lambda m:new,h,count=1)
h=re.sub(r'현재가 \(\d{4}\.\d\d\.\d\d\)',f'현재가 ({last[0].replace("-",".")})',h,count=1)
open(p,'w',encoding='utf-8').write(h); print('arrays', len(D), D[0][0], last, prev[4])
