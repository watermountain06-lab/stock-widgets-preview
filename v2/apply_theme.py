#!/usr/bin/env python3
"""카드를 라이브 홈과 같은 밝게/어둡게 전환 테마로 바꾼다(2026-10-07 사용자 결정).

사용자 요구: "회사 느낌이 없음, 밋밋하고 흐릿함, stock-as.kro.kr 홈페이지처럼 어둡고 밝은 게 왔다갔다 하는 식".
  - 색은 라이브 홈(stock-widgets-redesign styles.css·theme.css)의 밝은/어두운 값을 그대로 쓴다.
    기기 설정을 따르고, 맨 위 막대의 스위치로 바꾼다. 저장 키는 홈과 같은 'site-theme'(같은 사이트면 홈에서 고른 값이 카드에도).
  - 회사 느낌: 헤더 회사명 옆 로고, 종목 배지와 헤더 위쪽 선에만 회사 대표색(--brand). 탭·버튼·제목 강조는 사이트 색(--accent).
  - 카드 CSS의 어두운 고정색은 CSS 변수로 바꿔 두 모드에서 함께 바뀌게 하고, 캔버스(차트)에 그리는 JS 고정색은
    두 바탕 모두에서 읽히는 중간 톤으로 바꾼다(캔버스는 CSS 변수를 못 읽는다).

카드는 매일 다시 만들어지므로 마지막 단계로 돈다(build.py·은행 rebuild·daily_price 손 카드). 두 번 돌아도 결과가 같다.

    python3 v2/apply_theme.py NVDA                  # v2/NVDA_full_widget.html 을 고친다
    python3 v2/apply_theme.py --all
    python3 v2/apply_theme.py NVDA --out X.html     # 사본으로(시안)
"""
import glob
import os
import re
import sys

V2 = os.path.dirname(os.path.abspath(__file__))
MARK = "<!-- theme: site v2 -->"
OLD_MARK = "<!-- theme: light-site v1 -->"

# 카드 CSS의 어두운 고정색 → 변수(두 모드 공통 이름)
CSS_VAR = {
    "#0f1117": "var(--bg)", "#1a1d27": "var(--bg2)", "#22263a": "var(--bg3)", "#2e3347": "var(--border)",
    "#e8eaf0": "var(--text)", "#9aa0b8": "var(--text2)", "#5c6282": "var(--text3)",
    "#2ecc71": "var(--green)", "#e74c3c": "var(--red)", "#f0c040": "var(--gold)", "#3498db": "var(--blue)",
    "#38bdf8": "var(--sky)", "#818cf8": "var(--indigo)", "#f1c40f": "var(--gold)",
}
# JS·인라인(캔버스 포함)의 고정색 → 두 바탕 모두에서 읽히는 중간 톤
MID = {
    "#0f1117": "#8a8d9e", "#1a1d27": "#8a8d9e", "#22263a": "#8a8d9e", "#2e3347": "#8a8d9e",
    "#e8eaf0": "#6f7180", "#9aa0b8": "#8a8d9e", "#5c6282": "#9a9cab",
    "#2ecc71": "#1fa463", "#e74c3c": "#e5484d", "#f0c040": "#d4a017", "#3498db": "#3b82f6",
    "#38bdf8": "#0ea5e9", "#818cf8": "#6366f1", "#f1c40f": "#d4a017",
    "#22d3ee": "#06b6d4", "#ff6b9d": "#ec4899",
}
LIGHT = ("--bg:#f8f9fc;--bg2:#ffffff;--bg3:#f1f2f7;--border:#e6e5ee;--text:#191923;--text2:#646474;--text3:#797989;"
         "--accent:#6551c9;--accent2:#191923;--accent3:#ece8fb;--green:#14804a;--red:#d92d20;--gold:#a8650c;--blue:#1d4ed8;"
         "--sky:#0369a1;--indigo:#4f46e5;--shadow:0 1px 3px rgba(25,25,35,.06)")
DARK = ("--bg:#15171d;--bg2:#20232d;--bg3:#2a2e3b;--border:#393d4d;--text:#ececf5;--text2:#bec0d0;--text3:#a5a9bd;"
        "--accent:#b3a3ff;--accent2:#ececf5;--accent3:#36304f;--green:#7cddb6;--red:#ff8799;--gold:#f2c14e;--blue:#83b8ff;"
        "--sky:#7dd3fc;--indigo:#a5b4fc;--shadow:0 4px 20px rgba(0,0,0,.35)")

THEME_JS = """<script>
(function(){   // 라이브 홈(theme.js)과 같은 규칙·같은 저장 키 — 홈에서 고른 모드가 카드에도 이어진다
  var mq = window.matchMedia ? matchMedia('(prefers-color-scheme: dark)') : null, choice = null;
  try { choice = localStorage.getItem('site-theme'); } catch (e) {}
  if (choice !== 'light' && choice !== 'dark') choice = null;
  function apply(){
    var dark = choice ? choice === 'dark' : !!(mq && mq.matches);
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    var t = document.getElementById('theme-toggle');
    if (t) { t.setAttribute('aria-checked', String(dark)); t.title = dark ? '라이트 모드로 전환' : '다크 모드로 전환'; }
  }
  apply();
  if (mq && mq.addEventListener) mq.addEventListener('change', apply);
  window.addEventListener('storage', function(e){ if (e.key === 'site-theme' || e.key === null) { choice = (e.newValue === 'light' || e.newValue === 'dark') ? e.newValue : null; apply(); } });
  document.addEventListener('DOMContentLoaded', function(){
    var t = document.getElementById('theme-toggle'); if (!t) return;
    t.onclick = function(){ choice = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('site-theme', choice); } catch (e) {} apply(); };
    apply();
  });
})();
</script>"""

TOGGLE = ('<button id="theme-toggle" type="button" role="switch" aria-label="다크 모드" aria-checked="false">'
          '<span aria-hidden="true">☀</span><span aria-hidden="true">☾</span><span class="theme-knob"></span></button>')


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def theme(h, ticker):
    if OLD_MARK in h:
        raise SystemExit(f"{ticker}: 1판(밝은 고정) 테마가 입혀진 카드다 — 테마 전 카드에서 다시 만든다")
    if MARK in h:
        return h
    m = re.search(r"--accent:\s*(#[0-9a-fA-F]{6});\s*--accent2:\s*(#[0-9a-fA-F]{6});\s*--accent3:\s*(#[0-9a-fA-F]{6});", h)
    brand = m.group(1).lower() if m else "#6551c9"
    brand2 = m.group(2).lower() if m else "#6551c9"
    brand3 = m.group(3).lower() if m else "#36304f"
    keep = {k.lower() for k in CSS_VAR} | {k.lower() for k in MID}
    brands = [b for b in (brand, brand2, brand3) if b not in keep]   # 회사색이 의미 색과 같으면 건드리지 않는다

    def css_fix(css):
        css = re.sub(r"--accent:\s*#[0-9a-fA-F]{6};\s*--accent2:\s*#[0-9a-fA-F]{6};\s*--accent3:\s*#[0-9a-fA-F]{6};", "", css)
        for a, b in CSS_VAR.items():
            css = re.sub(re.escape(a) + r"(?![0-9a-fA-F])", b, css, flags=re.I)
        for b in brands:
            r, g, bl = hex_rgb(b)
            css = re.sub(rf"rgba\(\s*{r}\s*,\s*{g}\s*,\s*{bl}\s*,\s*([\d.]+)\s*\)",
                         lambda mm: f"color-mix(in srgb, var(--accent) {round(float(mm.group(1)) * 100)}%, transparent)", css)
            css = re.sub(re.escape(b) + r"(?![0-9a-fA-F])", "var(--accent)", css, flags=re.I)
        css = re.sub(r"rgba\(\s*255\s*,\s*255\s*,\s*255\s*,\s*([\d.]+)\s*\)",
                     lambda mm: f"color-mix(in srgb, var(--text) {round(float(mm.group(1)) * 100)}%, transparent)", css)
        css = css.replace("0 4px 20px rgba(0,0,0,0.4)", "var(--shadow)")
        css = re.sub(r"(\.header\s*\{\s*background:\s*)linear-gradient\([^;]*\);", r"\1var(--bg2); border-top: 3px solid var(--brand);", css)
        css = re.sub(r"(\.header::before \{[^}]*?background: )radial-gradient\([^;]*\);", r"\1none;", css)
        css = re.sub(r"(\.back-bar \{[^}]*?background: )rgba\(\s*10\s*,\s*11\s*,\s*17\s*,\s*0\.92\s*\)",
                     r"\1color-mix(in srgb, var(--bg2) 94%, transparent)", css)
        return css.replace("font-family: 'Segoe UI', -apple-system, sans-serif;",
                           "font-family: 'Noto Sans KR', system-ui, -apple-system, sans-serif;")

    def mid_fix(s):
        # 차트 가격 이름표(SVG 사각형) — style로 주면 CSS 변수를 쓸 수 있어 모드를 따라간다
        s = s.replace("bg.setAttribute('fill','rgba(15,17,23,0.85)')", "bg.style.fill='color-mix(in srgb, var(--bg2) 90%, transparent)'")
        for b in brands:
            r, g, bl = hex_rgb(b)
            s = re.sub(rf"rgba\(\s*{r}\s*,\s*{g}\s*,\s*{bl}\s*,", "rgba(124,106,214,", s)
            s = re.sub(re.escape(b) + r"(?![0-9a-fA-F])", "#7c6ad6", s, flags=re.I)
        for a, b in MID.items():
            s = re.sub(re.escape(a) + r"(?![0-9a-fA-F])", b, s, flags=re.I)
            r, g, bl = hex_rgb(a); r2, g2, b2 = hex_rgb(b)
            s = re.sub(rf"rgba\(\s*{r}\s*,\s*{g}\s*,\s*{bl}\s*,", f"rgba({r2},{g2},{b2},", s)
        return re.sub(r"rgba\(\s*255\s*,\s*255\s*,\s*255\s*,", "rgba(128,130,145,", s)

    parts = re.split(r"(<style[^>]*>.*?</style>)", h, flags=re.S)
    h = "".join(css_fix(p) if p.startswith("<style") else mid_fix(p) for p in parts)
    # 회사 느낌 — 헤더 로고(홈 logos/; v2/ 폴더에서 볼 때는 ../logos/), 배지·헤더 위쪽 선은 회사색
    t = ticker.lower()
    h = re.sub(r'(<div class="company-name">)', '<img class="hdr-logo" src="logos/' + t + '.png" alt="" '
               'onerror="if(!this.dataset.r){this.dataset.r=1;this.src=\'../logos/' + t + '.png\'}else{this.remove()}">' + r'\1', h, count=1)
    h = h.replace('<div class="back-bar-right">', '<div class="back-bar-right">' + TOGGLE, 1)
    h = h.replace("<span>[사이트명] · 전체 종목 목록</span>", "<span>US stock 가치를 말하다 · 전체 종목 목록</span>")
    vars_css = (f"<style>/* site theme v2 */\n:root{{{LIGHT};--brand:{brand};color-scheme:light}}\n"
                f":root[data-theme=\"dark\"]{{{DARK};--brand:{brand};color-scheme:dark}}\n"
                ".ticker-badge{background:var(--brand)!important;color:#fff!important}\n"
                ".hdr-logo{width:34px;height:34px;object-fit:contain;border-radius:8px;background:#fff;padding:4px;"
                "border:1px solid var(--border);margin-right:12px;display:inline-block;vertical-align:middle}\n"
                ".hdr-logo + .company-name{display:inline-block;vertical-align:middle}\n"
                ".back-bar-logo{background:var(--accent)!important}\n"
                ".price-main{color:var(--text)!important}\n"
                "#theme-toggle{position:relative;width:54px;height:28px;padding:3px 6px;border:1px solid var(--border);border-radius:20px;"
                "background:var(--bg2);color:var(--text2);display:flex;justify-content:space-between;align-items:center;cursor:pointer;font-size:12px}\n"
                "#theme-toggle .theme-knob{position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:var(--accent);transition:transform .2s}\n"
                "#theme-toggle[aria-checked=true] .theme-knob{transform:translateX(26px)}\n</style>")
    font = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n')
    return h.replace("</head>", font + vars_css + "\n" + THEME_JS + "\n" + MARK + "\n</head>", 1)


def main():
    args = sys.argv[1:]
    out = None
    if "--out" in args:
        i = args.index("--out"); out = args[i + 1]; del args[i:i + 2]
    paths = sorted(glob.glob(os.path.join(V2, "*_full_widget.html"))) if args == ["--all"] else \
        [a if a.endswith(".html") else os.path.join(V2, f"{a.upper()}_full_widget.html") for a in args]
    for p in paths:
        T = os.path.basename(p).split("_")[0]
        h = open(p, encoding="utf-8").read()
        n = theme(h, T)
        if n != h or out:
            open(out or p, "w", encoding="utf-8").write(n)
            print("고침", os.path.basename(out or p))


if __name__ == "__main__":
    main()
