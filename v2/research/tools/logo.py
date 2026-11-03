#!/usr/bin/env python3
"""python3 logo.py T "검색어" — 위키미디어에서 로고 SVG를 찾아 PNG로 받고 정사각형(흰 배경)으로 logos/{t}.png에 저장. 찾은 파일명 출력."""
import json, subprocess, sys, os, urllib.parse
from PIL import Image
T, q = sys.argv[1], sys.argv[2]; t = T.lower()
SP = os.environ.get("CARD_WORK", "/tmp/card_work"); D = f"{SP}/logo/{t}"; os.makedirs(D, exist_ok=True)
UA = "stock-widgets research gptjhss@gmail.com"
u = "https://commons.wikimedia.org/w/api.php?action=query&list=search&srnamespace=6&format=json&srlimit=10&srsearch=" + urllib.parse.quote(q + " logo")
res = json.loads(subprocess.run(["curl", "-s", "-A", UA, u], capture_output=True).stdout)["query"]["search"]
cands = [r["title"][5:] for r in res if r["title"].lower().endswith(".svg") and "logo" in r["title"].lower()] or [r["title"][5:] for r in res if r["title"].lower().endswith((".svg", ".png"))]
for name in cands:
    out = f"{D}/ok.png"
    subprocess.run(["curl", "-sL", "-A", UA, "-o", out, f"https://commons.wikimedia.org/wiki/Special:FilePath/{urllib.parse.quote(name)}?width=512"])
    try:
        im = Image.open(out).convert("RGBA")
    except Exception:
        continue
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); im = Image.alpha_composite(bg, im).convert("RGB")
    bb = Image.eval(im.convert("L"), lambda v: 255 if v < 245 else 0).getbbox() or (0, 0) + im.size
    m = im.crop(bb); w, h = m.size; s = int(max(w, h) * 1.12)
    c = Image.new("RGB", (s, s), (255, 255, 255)); c.paste(m, ((s - w) // 2, (s - h) // 2))
    c.resize((128, 128), Image.LANCZOS).save(os.path.expanduser(f"~/Workspace/stock-widgets-preview/logos/{t}.png"))
    print(T, name); break
else:
    print(T, "못 찾음", cands)
