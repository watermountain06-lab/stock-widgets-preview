import json,re,os
os.chdir('/Users/watermountain/Workspace/stock-widgets-preview')
T='APH'
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
# APH: 루트 카드가 9/3 분할 안전장치에 걸려 9/11에서 멈춤(card_status "held") → Yahoo 분할 반영 일봉으로 9/30까지 다시 만든다.
# 겹치는 날 종가는 루트와 모두 같음(2026-10-01 대조). 이동평균은 루트와 같은 방식(창 안에서만, 앞 k−1개 null).
_rows=[r for r in json.load(open('/tmp/aph_rows.json')) if r[0]<='2026-09-30'][-1255:]
_c=[r[4] for r in _rows]
_ma=lambda k:[None if i<k-1 else round(sum(_c[i-k+1:i+1])/k,6) for i in range(len(_c))]
_gen={'DAILY':_rows,'MA5':_ma(5),'MA20':_ma(20),'MA60':_ma(60),'MA120':_ma(120)}
for n in ['DAILY','MA5','MA20','MA60','MA120','BACKTEST']:
    hs,he=span(h,n)
    if n in _gen: seg=json.dumps(_gen[n])
    else:
        rs,re_=span(root,n); seg=root[rs:re_].replace("'", '"')
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
