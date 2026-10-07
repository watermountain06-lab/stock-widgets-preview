#!/usr/bin/env python3
"""카드를 홈과 같은 밝은 테마·하나의 사이트 색으로 바꾼다(2026-10-07 사용자 결정: 대표색 통일 + 밝은 바탕).

카드는 매일 다시 만들어지므로 일회성 수정이 아니라 마지막 단계로 돈다(build.py·은행 rebuild·daily_price 손 카드).
같은 카드에 여러 번 돌려도 결과가 같다(이미 바꾼 카드는 그대로).

바꾸는 것
  1. :root 변수 — 어두운 바탕·글자·테두리 → 홈 팔레트, 회사별 --accent/2/3 → 사이트 남색 한 가지,
     초록·빨강·금색·파랑 → 밝은 바탕에서 읽히는 진한 쪽(홈의 상승·하락 색과 같은 계열).
  2. 직접 박힌 색 — 어두운 테마 고정값(#0f1117 등)과 카드의 회사색(헥스·rgba)을 같은 규칙으로.
     어두운 바탕 위 밝은 반투명(rgba(255,255,255,a))은 밝은 바탕 위 어두운 반투명으로.
  3. 헤더 그라디언트, 글꼴(홈과 같은 Noto Sans KR).

    python3 v2/apply_theme.py NVDA                  # v2/NVDA_full_widget.html 을 고친다
    python3 v2/apply_theme.py --all
    python3 v2/apply_theme.py NVDA --out X.html     # 사본으로(시안)
"""
import glob
import os
import re
import sys

V2 = os.path.dirname(os.path.abspath(__file__))
MARK = "<!-- theme: light-site v1 -->"

# 어두운 테마 고정값 → 밝은 값(홈 index.html :root와 같은 계열)
FIXED = {
    "#0f1117": "#f7f5ef",   # --bg
    "#1a1d27": "#ffffff",   # --bg2 패널
    "#22263a": "#f1eee4",   # --bg3
    "#2e3347": "#e6e2d3",   # --border
    "#e8eaf0": "#1f2420",   # --text
    "#9aa0b8": "#6b6a5e",   # --text2
    "#5c6282": "#706e62",   # --text3 — 바탕과 대비 4.7:1(홈의 #9c9a8c는 2.6:1이라 작은 글씨가 안 읽힌다, Codex 2026-10-07)
    "#2ecc71": "#1f7a4d",   # --green
    "#e74c3c": "#d92d20",   # --red
    "#f0c040": "#b7791f",   # --gold
    "#3498db": "#1a56db",   # --blue
    "#38bdf8": "#0e7490",   # 내재가치 선·시나리오(하늘색)
    "#818cf8": "#4f46e5",
    "#22d3ee": "#0e7490",   # MA120
    "#ff6b9d": "#d6336c",   # MA5
    "#9b59b6": "#7b3fa0",   # MA20
    "#f1c40f": "#b7791f",
}
ACCENT, ACCENT2, ACCENT3 = "#1c2b4a", "#1c2b4a", "#dfe5f0"   # 사이트 색(홈 --accent), 강조 글자, 옅은 바탕·테두리
RGB = {"#1c2b4a": (28, 43, 74)}


def hex_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_of(hexv):
    r, g, b = hex_rgb(hexv)
    return f"{r},{g},{b}"


def theme(h):
    # 이미 입힌 카드도 다시 돈다 — 그 뒤 손 카드에 새로 들어간 블록(어두운 색)까지 바꾸려고(Codex). 바꾸는 쪽 값은
    # 어두운 원래 값이라 두 번 돌아도 결과가 같다.
    m = re.search(r"--accent:\s*(#[0-9a-fA-F]{3,6});\s*--accent2:\s*(#[0-9a-fA-F]{3,6});\s*--accent3:\s*(#[0-9a-fA-F]{3,6});", h)
    brand = [x.lower() for x in m.groups()] if m else []
    # 회사색이 의미 색(초록·빨강 등)이나 사이트 색과 같으면 바꾸지 않는다 — 판정 색까지 남색이 되지 않게(Codex)
    keep = {k.lower() for k in FIXED} | {v.lower() for v in FIXED.values()} | {ACCENT.lower(), ACCENT3.lower()}
    brand = [b if b not in keep else None for b in brand]
    # 1. :root 변수(회사색 포함)
    h = re.sub(r"--accent:\s*#[0-9a-fA-F]{3,6};\s*--accent2:\s*#[0-9a-fA-F]{3,6};\s*--accent3:\s*#[0-9a-fA-F]{3,6};",
               f"--accent: {ACCENT}; --accent2: {ACCENT2}; --accent3: {ACCENT3};", h)
    h = h.replace("--shadow: 0 4px 20px rgba(0,0,0,0.4);", "--shadow: 0 1px 3px rgba(31,36,32,0.08);")
    # 2-a. 회사색 헥스(대소문자 무관) → 사이트 색. accent3(어두운 변형)은 옅은 바탕색으로
    for i, b in enumerate(brand):
        if not b:
            continue
        to = ACCENT3 if i == 2 else ACCENT
        h = re.sub(re.escape(b) + r"(?![0-9a-fA-F])", to, h, flags=re.I)   # 완전한 색 값만(#abc가 #abcdef를 건드리지 않게)
    # 2-b. 회사색 rgba → 사이트 색 rgba(같은 투명도)
    for b in brand:
        if not b:
            continue
        r, g, bl = hex_rgb(b)
        h = re.sub(rf"rgba\(\s*{r}\s*,\s*{g}\s*,\s*{bl}\s*,", f"rgba({rgb_of(ACCENT)},", h)
    # 2-c. 어두운 테마 고정값
    for a, b in FIXED.items():
        h = re.sub(re.escape(a) + r"(?![0-9a-fA-F])", b, h, flags=re.I)
        r, g, bl = hex_rgb(a)
        h = re.sub(rf"rgba\(\s*{r}\s*,\s*{g}\s*,\s*{bl}\s*,", f"rgba({rgb_of(b)},", h)
        h = h.replace(f"rgb({r}, {g}, {bl})", "rgb({}, {}, {})".format(*hex_rgb(b)))
    # 2-d. 어두운 바탕 위 밝은 반투명 → 밝은 바탕 위 어두운 반투명
    h = re.sub(r"rgba\(\s*255\s*,\s*255\s*,\s*255\s*,", "rgba(31,36,32,", h)
    h = re.sub(r"rgba\(\s*0\s*,\s*0\s*,\s*0\s*,\s*0\.4\s*\)", "rgba(31,36,32,0.08)", h)
    # 3. 헤더 그라디언트(카드마다 회사색 조금 섞인 어두운 그라디언트) → 흰색에서 바탕색으로
    h = re.sub(r"(\.header\s*\{\s*background:\s*)linear-gradient\([^;]*\);",
               r"\1linear-gradient(135deg, #ffffff 0%, #fbfaf6 60%, #f7f5ef 100%);", h)
    # 배지 글자(#0f1117 → 바뀐 값) 위 그라디언트는 남색이라 흰 글자로
    h = h.replace("background: linear-gradient(135deg, var(--accent3), var(--accent)); color: #f7f5ef;",
                  "background: var(--accent); color: #ffffff;")
    # 맨 위 이동 막대(어두운 반투명) → 흰 반투명, 헤더 오른쪽 위 원형 장식은 밝은 바탕에서 얼룩으로 보여 뺀다
    h = re.sub(r"(\.back-bar \{[^}]*?background: )rgba\(\s*10\s*,\s*11\s*,\s*17\s*,\s*0\.92\s*\)", r"\1rgba(247,245,239,0.94)", h)
    h = re.sub(r"(\.header::before \{[^}]*?background: )radial-gradient\([^;]*\);", r"\1none;", h)
    # 이동 막대의 사이트 이름 자리표시(처음 만들 때부터 비어 있던 것) → 홈 제목
    h = h.replace("<span>[사이트명] · 전체 종목 목록</span>", "<span>US stock 가치를 말하다 · 전체 종목 목록</span>")
    # 글꼴
    h = h.replace("font-family: 'Segoe UI', -apple-system, sans-serif;", "font-family: 'Noto Sans KR', system-ui, -apple-system, sans-serif;")
    if "fonts.googleapis.com/css2?family=Noto+Sans+KR" not in h:
        h = h.replace("</head>", '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
                      '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n</head>', 1)
    return h if MARK in h else h.replace("</head>", MARK + "\n</head>", 1)


def main():
    args = sys.argv[1:]
    out = None
    if "--out" in args:
        i = args.index("--out"); out = args[i + 1]; del args[i:i + 2]
    paths = sorted(glob.glob(os.path.join(V2, "*_full_widget.html"))) if args == ["--all"] else \
        [a if a.endswith(".html") else os.path.join(V2, f"{a.upper()}_full_widget.html") for a in args]
    for p in paths:
        h = open(p, encoding="utf-8").read()
        n = theme(h)
        if n != h:
            open(out or p, "w", encoding="utf-8").write(n)
            print("고침", os.path.basename(out or p))


if __name__ == "__main__":
    main()
