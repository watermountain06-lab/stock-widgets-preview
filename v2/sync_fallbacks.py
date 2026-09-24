#!/usr/bin/env python3
"""v2 카드의 HTML 대체값을 JS가 실제로 그린 값으로 맞춘다.

카드의 숫자는 대부분 JS가 상수({T}_DCF, {T}_FUNDAMENTAL, {T}_VALUATION …)에서 그린다.
HTML에 적힌 값은 스크립트가 꺼지거나 중간에 죽었을 때만 보이는 대체값인데, 손으로
맞추다 보면 빠진다. AAPL 첫 변환 때 요약 격자 $315/$160/$602, 밸류 탭 "싸다" 같은 NVDA
대체값이 헤더의 "고평가"와 반대로 남아 있었다(Codex 지적, 2026-09-24).

방법
----
1. 헤드리스 Chrome으로 카드를 띄우고(로컬 http 서버 필요), 렌더가 끝난 뒤 아래 SELECTORS에
   걸리는 요소의 innerHTML·class·style을 DOM 순서대로 뽑는다.
2. 원본 HTML의 본문(첫 <script> 전까지)에서 같은 표지(id·data 속성·클래스)를 가진 요소를
   같은 순서로 찾아 안쪽과 class·style을 바꾼다. JS가 만든 요소(차트, 버튼)는 대상이 아니다.
3. 표지 개수가 DOM과 원본에서 다르면 그 표지는 건드리지 않고 알린다.

한계: 탭을 열 때만 JS가 채우는 칸(기본적 분석 탭의 `fundPeriodTitle`처럼 selectFundPeriod가
처음 불릴 때 쓰는 값)은 첫 화면에 없으므로 여기서 못 맞춘다. 그런 칸은 손으로 확인한다.

사용법
------
    python3 -m http.server 8765            # 저장소 루트에서, 따로 띄워 둔다
    python3 v2/sync_fallbacks.py AAPL      # 바뀐 요소 수와 목록을 출력하고 파일을 고친다
    python3 v2/sync_fallbacks.py AAPL --dry-run
"""
import argparse
import html as htmlmod
import json
import os
import re
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# (표지 이름, 원본에서 찾을 정규식 조각, DOM 선택자). {lo}는 소문자 종목 코드.
SELECTORS = [
    ("id", r'id="{lo}DcfReq"', "#{lo}DcfReq"),
    ("id", r'id="{lo}ConfidenceLabel"', "#{lo}ConfidenceLabel"),
    ("id", r'id="{lo}Confidence"', "#{lo}Confidence"),
    ("id", r'id="{lo}DcfVerdict"', "#{lo}DcfVerdict"),
    ("id", r'id="{lo}DcfBox"', "#{lo}DcfBox"),
    ("id", r'id="{lo}FundBox"', "#{lo}FundBox"),
    ("id", r'id="{lo}FundVerdict"', "#{lo}FundVerdict"),
    ("id", r'id="{lo}FundScore"', "#{lo}FundScore"),
    ("id", r'id="{lo}PeerBox"', "#{lo}PeerBox"),
    ("id", r'id="{lo}PeerVerdict"', "#{lo}PeerVerdict"),
    ("id", r'id="{lo}PeerScore"', "#{lo}PeerScore"),
    ("id", r'id="{lo}SelfBox"', "#{lo}SelfBox"),
    ("id", r'id="{lo}SelfVerdict"', "#{lo}SelfVerdict"),
    ("id", r'id="{lo}SelfScore"', "#{lo}SelfScore"),
    ("id", r'id="techHeaderTitle"', "#techHeaderTitle"),
    ("id", r'id="techRangeSummary"', "#techRangeSummary"),
    ("id", r'id="fundCompTotal"', "#fundCompTotal"),
    ("id", r'id="fundHealthAxis"', "#fundHealthAxis"),
    ("id", r'id="fundHealthSummary"', "#fundHealthSummary"),
    ("id", r'id="fundNetCashPs"', "#fundNetCashPs"),
    ("id", r'id="fundNetCashNote"', "#fundNetCashNote"),
    ("id", r'id="fundPeriodTitle"', "#fundPeriodTitle"),
    ("id", r'id="actPeriod"', "#actPeriod"),
    ("id", r'id="actSummary"', "#actSummary"),
    ("id", r'id="actCccExplain"', "#actCccExplain"),
    ("id", r'id="actBar"', "#actBar"),
    ("id", r'id="dcfPickValue"', "#dcfPickValue"),
    ("id", r'id="dcfPickUpside"', "#dcfPickUpside"),
    ("id", r'id="multipleCompareTitle"', "#multipleCompareTitle"),
    ("data", r'data-axis="[a-zA-Z]+"', "[data-axis]"),
    ("data", r'data-act-turn="[a-z]+"', "[data-act-turn]"),
    ("data", r'data-act-days="[a-z]+"', "[data-act-days]"),
    ("data", r'data-act-sub="[a-z]+"', "[data-act-sub]"),
    ("data", r'data-fund-metric="[a-zA-Z]+"', "[data-fund-metric]"),
    ("data", r'class="val-item"', "#valuation .val-item"),
    ("data", r'id="valComp"', "#valComp"),
    ("data", r'data-vs="[a-z]+"', "[data-vs]"),
    ("data", r'data-dcf-value="[a-z]+"', "[data-dcf-value]"),
    ("data", r'data-dcf-upside="[a-z]+"', "[data-dcf-upside]"),
    ("data", r'data-dcf-(?:price|req|basev|baseeq)(?=[\s>])', "[data-dcf-price],[data-dcf-req],[data-dcf-basev],[data-dcf-baseeq]"),
    ("data", r'data-react="[0-9-]+"', "[data-react]"),
    ("data", r'data-an="[a-z]+"', "[data-an]"),
    ("data", r'data-an-bar="[a-z]+"', "[data-an-bar]"),
]

VOID = {"br", "img", "input", "meta", "link", "hr", "source", "wbr"}


def dom_dump(url, selectors):
    """헤드리스 Chrome에 카드를 띄워 선택자마다 [innerHTML, class, style] 목록을 받는다."""
    probe = ("<script>setTimeout(function(){var out={};"
             + "".join(f"out[{json.dumps(s)}]=[].map.call(document.querySelectorAll({json.dumps(s)}),"
                       "function(e){return [e.innerHTML,e.getAttribute('class'),e.getAttribute('style')];});"
                       for s in selectors)
             + "var p=document.createElement('pre');p.id='__sync';"
             "p.textContent=JSON.stringify(out);document.body.appendChild(p);},1500);</script>")
    return probe


def tag_end(src, start):
    """src[start]의 '<'부터 따옴표 밖의 첫 '>' 다음 위치. 속성값 안의 '>'는 건너뛴다."""
    q = None
    for i in range(start + 1, len(src)):
        c = src[i]
        if q:
            if c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c == ">":
            return i + 1
    raise ValueError(f"여는 태그가 닫히지 않음 (위치 {start})")


def element_span(src, start):
    """src[start]이 여는 태그의 '<'일 때 (여는 태그 끝, 닫는 태그 시작, 닫는 태그 끝).
    안쪽에 주석이 있으면 경계를 믿을 수 없으므로 None을 돌려 건너뛰게 한다."""
    m = re.match(r"<([a-zA-Z0-9]+)", src[start:])
    tag = m.group(1).lower()
    open_end = tag_end(src, start)
    if tag in VOID or src[open_end - 2] == "/":
        return open_end, open_end, open_end
    depth, i = 1, open_end
    pat = re.compile(rf"<(/?){tag}(?=[\s>/])|<!--", re.I)
    while True:
        m = pat.search(src, i)
        if not m:
            raise ValueError(f"닫는 </{tag}>를 못 찾음 (위치 {start})")
        if m.group(0) == "<!--":
            return None
        if m.group(1):
            depth -= 1
            if depth == 0:
                return open_end, m.start(), tag_end(src, m.start())
            i = m.end()
        else:
            depth += 1
            i = tag_end(src, m.start())


ATTR = re.compile(r"""\s+([^\s=/>"']+)(?:\s*=\s*("[^"]*"|'[^']*'|[^\s"'>]+))?""")


def set_attrs(open_tag, updates):
    """여는 태그를 속성 단위로 읽어 updates의 값으로 바꾼다(None이면 뺀다).
    속성값 안의 'class="…"' 같은 글자는 속성으로 보지 않는다."""
    m = re.match(r"<([a-zA-Z0-9]+)", open_tag)
    pos, attrs = m.end(), []
    while True:
        a = ATTR.match(open_tag, pos)
        if not a:
            break
        attrs.append([a.group(1), a.group(2)])
        pos = a.end()
    tail = open_tag[pos:]
    if tail.strip() not in (">", "/>"):
        raise ValueError(f"여는 태그를 속성으로 다 읽지 못함: {open_tag[:80]}")
    names = [n.lower() for n, _ in attrs]
    for name, value in updates.items():
        v = None if value is None else '"' + htmlmod.escape(value, quote=True) + '"'
        if name in names:
            k = names.index(name)
            if v is None:
                attrs.pop(k); names.pop(k)
            else:
                attrs[k][1] = v
        elif v is not None:
            attrs.append([name, v]); names.append(name)
    return "<" + m.group(1) + "".join(f" {n}={v}" if v is not None else f" {n}" for n, v in attrs) + tail.strip()


def render_text(url):
    """렌더된 화면의 글자만(스크립트·차트 제외). 적용 전후 비교용."""
    out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--window-size=1440,900",
                          "--virtual-time-budget=6000", "--dump-dom", url],
                         capture_output=True, text=True, timeout=90).stdout
    out = re.sub(r"<script.*?</script>|<canvas[^>]*>.*?</canvas>|<svg.*?</svg>", "", out, flags=re.S)
    out = htmlmod.unescape(re.sub(r"<[^>]+>", "\n", out))
    return [l.strip() for l in out.split("\n") if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--base", default="http://localhost:8765")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    t = args.ticker.upper()
    lo = t.lower()
    path = os.path.join(HERE, f"{t}_full_widget.html")
    src = open(path, encoding="utf-8").read()

    sels = [(kind, pat.format(lo=lo), sel.format(lo=lo)) for kind, pat, sel in SELECTORS]
    tmp_name = f"_sync_{t}_{int(time.time())}.html"
    tmp_path = os.path.join(HERE, tmp_name)
    open(tmp_path, "w", encoding="utf-8").write(
        src.replace("</body>", dom_dump(None, [s for _, _, s in sels]) + "</body>", 1))
    try:
        out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--window-size=1440,900",
                              "--virtual-time-budget=6000", "--dump-dom",
                              f"{args.base}/v2/{tmp_name}"], capture_output=True, text=True, timeout=90).stdout
    finally:
        os.remove(tmp_path)
    m = re.search(r'<pre id="__sync">(.*?)</pre>', out, re.S)
    if not m:
        sys.exit("렌더 결과를 못 받았다 — http 서버가 저장소 루트에서 떠 있는지 확인")
    dom = json.loads(htmlmod.unescape(m.group(1)))

    body_start = src.index("<body")
    body_end = src.index("<script", body_start)
    edits, skipped = [], []
    for kind, pat, sel in sels:
        found = [mm.start() for mm in re.finditer(pat, src[body_start:body_end])]
        starts = [src.rindex("<", 0, body_start + f) for f in found]
        vals = dom.get(sel, [])
        if len(starts) != len(vals):
            skipped.append(f"{sel}: 원본 {len(starts)}개 · DOM {len(vals)}개")
            continue
        for st, (inner, cls, style) in zip(starts, vals):
            span = element_span(src, st)
            if span is None:
                skipped.append(f"{sel}: 안쪽에 주석이 있어 건너뜀 (위치 {st})")
                continue
            open_end, close_start, _ = span
            edits.append((st, open_end, close_start, inner, cls, style))

    # 바깥 요소가 안쪽 요소를 이미 포함하면(예: #valComp 안의 data-vs) 바깥만 쓴다.
    edits.sort()
    kept, last_close = [], -1
    for e in edits:
        if e[0] < last_close:
            continue
        kept.append(e)
        last_close = e[2]
    changed = 0
    for st, open_end, close_start, inner, cls, style in sorted(kept, reverse=True):
        open_tag = src[st:open_end]
        new_open = open_tag if (cls, style) == (None, None) and 'class=' not in open_tag and 'style=' not in open_tag \
            else set_attrs(open_tag, {"class": cls, "style": style})
        if new_open != open_tag and set_attrs(open_tag, {}) == set_attrs(new_open, {}):
            new_open = open_tag
        if new_open == open_tag and src[open_end:close_start] == inner:
            continue
        src = src[:st] + new_open + inner + src[close_start:]
        changed += 1

    print(f"{t}: 대체값 {changed}곳 갱신 (검사 {len(kept)}곳)")
    for s in skipped:
        print("  건너뜀 —", s)
    if args.dry_run or not changed:
        return
    # 적용 전후 렌더 글자가 같아야 한다. 대체값만 바꿨으니 JS가 그린 화면은 그대로여야 한다.
    original = open(path, encoding="utf-8").read()
    url = f"{args.base}/v2/{t}_full_widget.html?sync="
    before = render_text(url + f"a{time.time()}")
    open(path, "w", encoding="utf-8").write(src)
    after = render_text(url + f"b{time.time()}")
    if before != after:
        open(path, "w", encoding="utf-8").write(original)
        import difflib
        print("\n".join(list(difflib.unified_diff(before, after, lineterm=""))[:40]))
        sys.exit("렌더 글자가 달라져 되돌렸다")
    print(f"  렌더 글자 {len(after)}줄 전후 동일 — 저장")


if __name__ == "__main__":
    main()
