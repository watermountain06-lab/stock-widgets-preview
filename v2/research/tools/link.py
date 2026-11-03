#!/usr/bin/env python3
"""python3 link.py PREV NEW — PREV 카드의 '다음' 링크를 NEW로(메타 + v2·루트 HTML, 재빌드 없이), NEW 메타의 이전 링크를 PREV로."""
import json, os, re, sys
R = os.path.expanduser("~/Workspace/stock-widgets-preview")
P, N = sys.argv[1], sys.argv[2]
nx = f'<a class="back-bar-nav" href="{N}_full_widget.html">다음 {N} ▶</a>'
mp = f"{R}/v2/newcards/meta/{P.lower()}.json"
if os.path.exists(mp):
    m = json.load(open(mp)); m["next"] = nx; open(mp, "w").write(json.dumps(m, ensure_ascii=False))
for f in (f"{R}/v2/{P}_full_widget.html", f"{R}/{P}_full_widget.html"):
    if os.path.exists(f):
        s = open(f).read()
        s2, n = re.subn(r'<span class="back-bar-nav disabled">다음 ▶</span>|<a class="back-bar-nav" href="[A-Z.]+_full_widget\.html">다음 [A-Z.]+ ▶</a>', nx, s, count=1)
        open(f, "w").write(s2); print(f, n)
nm = f"{R}/v2/newcards/meta/{N.lower()}.json"
if os.path.exists(nm):
    m = json.load(open(nm)); m["prev"] = f'<a class="back-bar-nav" href="{P}_full_widget.html">◀ {P}</a>'; open(nm, "w").write(json.dumps(m, ensure_ascii=False))
