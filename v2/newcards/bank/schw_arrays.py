import json,re,os
os.chdir('/Users/watermountain/Workspace/stock-widgets-preview')
T='SCHW'
root=open(f'{T}_full_widget.html',encoding='utf-8').read(); p=f'v2/{T}_full_widget.html'; h=open(p,encoding='utf-8').read()
def span(s, name):
    a=s.index(f'const {T}_{name} '); st=s.index('[',a); d=0; ins=None
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
for n in ['DAILY','MA5','MA20','MA60','MA120','BACKTEST']:
    rs,re_=span(root,n); hs,he=span(h,n)
    seg=root[rs:re_].replace("'", '"')   # DELL 루트는 작은따옴표 날짜
    h=h[:hs]+seg+h[he:]
dec=json.JSONDecoder()
D=dec.raw_decode(h,h.index('[',h.index(f'const {T}_DAILY')))[0]
for n,k in [('MA5',5),('MA20',20),('MA60',60),('MA120',120)]:
    m=dec.raw_decode(h,h.index('[',h.index(f'const {T}_{n}')))[0]
    last=[x for x in m if x is not None][-1] if m else None
    print(n,len(m),len(D), m[-1], round(sum(r[4] for r in D[-k:])/k,2))
last,prev=D[-1],D[-2]; c=(last[4]/prev[4]-1)*100; up=c>=0
new=f'<div class="price-main"><span class="price-change" style="color:var(--{"green" if up else "red"});">{"▲ +" if up else "▼ −"}{abs(c):.2f}%</span> ${last[4]:.2f}</div>'
h=re.sub(r'<div class="price-main">.*?</div>',lambda m:new,h,count=1)
h=re.sub(r'현재가 \(\d{4}\.\d\d\.\d\d\)',f'현재가 ({last[0].replace("-",".")})',h,count=1)
open(p,'w',encoding='utf-8').write(h); print('arrays', len(D), D[0][0], last, prev[4])
