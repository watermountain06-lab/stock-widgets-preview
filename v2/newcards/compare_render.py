#!/usr/bin/env python3
"""두 카드 파일을 렌더해 보이는 글자·툴팁을 줄 단위로 비교한다(틀 통일 재현 확인, 2026-10-05).

    python3 v2/newcards/compare_render.py KO /tmp/KO_from_card.html     # 지금 v2/KO_full_widget.html 과 옛 사본
    python3 v2/newcards/compare_render.py KO OLD.html --base http://localhost:8765

저장소 루트에서 http 서버가 떠 있어야 한다(sync_fallbacks와 같다). 옛 사본은 v2/ 안에 임시 이름으로 복사해 띄우고 지운다.
출력: 보이는 글자 줄 차이, title 속성 차이(판정 칸은 research/extract_card_verdicts.js로 따로 본다). 종료 코드 0 = 같음, 1 = 다름.
"""
import argparse
import difflib
import html as hm
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, V2)
CHROME = os.environ.get("CHROME") or next((c for c in ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable", "/usr/bin/chromium") if os.path.exists(c)), "google-chrome")   # 맥·리눅스(Actions) 둘 다


def dump(url):
    out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--window-size=1440,900",
                          "--virtual-time-budget=6000", "--dump-dom", url],
                         capture_output=True, text=True, timeout=120).stdout
    out = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>|<canvas[^>]*>.*?</canvas>", "", out, flags=re.S)
    titles = [hm.unescape(x) for x in re.findall(r'title="([^"]*)"', out)]
    text = [l.strip() for l in hm.unescape(re.sub(r"<[^>]+>", "\n", out)).split("\n") if l.strip()]
    return text, titles


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("old")
    ap.add_argument("--new")
    ap.add_argument("--base", default="http://localhost:8765")
    a = ap.parse_args()
    T = a.ticker.upper()
    new = a.new or os.path.join(V2, f"{T}_full_widget.html")
    tmp_old = os.path.join(V2, f"_cmp_old_{T}_{int(time.time())}.html")
    tmp_new = os.path.join(V2, f"_cmp_new_{T}_{int(time.time())}.html")
    shutil.copy(a.old, tmp_old)
    shutil.copy(new, tmp_new)
    try:
        to, ho = dump(f"{a.base}/v2/{os.path.basename(tmp_old)}")
        tn, hn = dump(f"{a.base}/v2/{os.path.basename(tmp_new)}")
    finally:
        os.remove(tmp_old)
        os.remove(tmp_new)
    diff = [l for l in difflib.unified_diff(to, tn, "old", "new", n=0, lineterm="") if not l.startswith(("---", "+++", "@@"))]
    tdiff = [l for l in difflib.unified_diff(sorted(set(ho)), sorted(set(hn)), "old", "new", n=0, lineterm="")
             if not l.startswith(("---", "+++", "@@"))]
    print(f"{T}: 보이는 글자 {len(to)}줄 → {len(tn)}줄, 다른 줄 {len(diff)} · 툴팁 다른 것 {len(tdiff)}")
    for l in diff:
        print("  " + l[:220])
    for l in tdiff:
        print("  [title] " + l[:220])
    sys.exit(0 if not diff and not tdiff else 1)


if __name__ == "__main__":
    main()
