"""SCHW 일봉·이동평균·백테스트 배열을 v2 카드로 옮긴다(jpm_arrays.py와 같은 방식). clone_card.py SCHW --force 뒤에 실행.
원본은 기본으로 루트 카드(SCHW_full_widget.html). 2026-10-05 기반을 지금 NVDA 틀로 다시 만들 때는 그때 v2 카드의 배열(마지막 봉 2026-09-30)을
그대로 쓰려고 원본 경로를 인자로 줬다: python3 v2/newcards/bank/schw_arrays.py <카드 사본 경로>"""
import json,re,os,sys
os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))   # 저장소 루트(스크립트 위치 기준 — Actions에서도, 2026-10-06)
T='SCHW'
src=sys.argv[1] if len(sys.argv)>1 else f'{T}_full_widget.html'
root=open(src,encoding='utf-8').read(); p=f'v2/{T}_full_widget.html'; h=open(p,encoding='utf-8').read()
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
