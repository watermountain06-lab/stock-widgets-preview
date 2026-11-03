#!/usr/bin/env python3
"""python3 badge.py T "#rrggbb" — 로고를 못 찾을 때 티커 글자 배지(원형)를 logos/{t}.png로."""
import sys, os
from PIL import Image, ImageDraw, ImageFont
T, col = sys.argv[1], sys.argv[2]
S = 512; im = Image.new("RGB", (S, S), (255, 255, 255)); d = ImageDraw.Draw(im)
d.ellipse((16, 16, S - 16, S - 16), fill=col)
fs = 200 if len(T) <= 3 else 160
font = None
for f in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc", "/Library/Fonts/Arial.ttf"]:
    if os.path.exists(f):
        font = ImageFont.truetype(f, fs); break
font = font or ImageFont.load_default()
bb = d.textbbox((0, 0), T, font=font); w, h = bb[2] - bb[0], bb[3] - bb[1]
d.text(((S - w) / 2 - bb[0], (S - h) / 2 - bb[1]), T, fill="white", font=font)
im.resize((128, 128), Image.LANCZOS).save(os.path.expanduser(f"~/Workspace/stock-widgets-preview/logos/{T.lower()}.png"))
print("badge", T)
