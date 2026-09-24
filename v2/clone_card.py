#!/usr/bin/env python3
"""v2 기준 카드(NVDA)를 복제해 새 종목의 v2 카드 틀을 만든다 — 1단계 70장 변환의 첫 단계.

하는 일은 **기계적 치환뿐**이다. 숫자·문장은 그대로 NVDA 것이 남으므로, 이 스크립트를 돌린
뒤 CARD_ITEMS.md의 순서대로 데이터 블록(스크립트)·배열(루트 카드)·판단 콘텐츠(1차 출처)를
채운다.

치환하는 것
-----------
- 이름: `NVDA_` 상수, `nvdaXxx` id, 제목·배지·aria-label·툴팁의 "NVDA", 갱신 명령 주석
- 머리: 거래소·업종 줄, 회사명, 뒤로가기 막대(시총 순위·이전·다음 링크) — 루트 카드에서 읽는다
- 색: `:root`의 --accent 셋, 그리고 **틀에 박힌 NVDA 초록 리터럴**(차트 막대·선택 버튼·CCC 막대).
  AAPL 첫 변환 때 이 리터럴이 남아 AAPL 카드에 NVDA 초록이 칠해졌다(2026-09-24).

루트 카드({T}_full_widget.html)는 읽기만 한다. 대상 파일이 이미 있으면 멈춘다.

사용법
------
    python3 v2/clone_card.py AAPL
    python3 v2/clone_card.py AAPL --force     # 이미 있는 v2 작업본을 덮어쓴다(주의)
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TEMPLATE = os.path.join(HERE, "NVDA_full_widget.html")

# 틀(NVDA)의 브랜드 색. --accent 셋과, 틀 안에 리터럴로 박힌 초록.
NVDA_ACCENT = ("#76b900", "#aeff20", "#3b5d00")
NVDA_RGB = "118,185,0"


def rgb(hexcol):
    h = hexcol.lstrip("#")
    return ",".join(str(int(h[i:i + 2], 16)) for i in (0, 2, 4))


def root_meta(t):
    """루트 카드에서 새 카드 머리에 쓸 값을 읽는다."""
    path = os.path.join(REPO, f"{t}_full_widget.html")
    h = open(path, encoding="utf-8").read()

    def need(pat, what):
        m = re.search(pat, h, re.S)
        if not m:
            sys.exit(f"루트 카드에서 {what}를 못 찾았다: {path}")
        return m

    acc = need(r"--accent:\s*(#[0-9a-fA-F]{6});\s*--accent2:\s*(#[0-9a-fA-F]{6});\s*--accent3:\s*(#[0-9a-fA-F]{6});", "--accent 셋")
    sub = need(r'<span class="ticker-badge">' + re.escape(t) + r'</span>\s*<span[^>]*>([^<]+)</span>', "거래소·업종 줄")
    name = need(r'<div class="company-name">([^<]+)</div>', "회사명")
    cur = need(r'<span class="back-bar-current">([^<]+)</span>', "뒤로가기 막대 현재 표시")
    prev = re.search(r'<(?:a|span) class="back-bar-nav[^"]*"[^>]*>◀[^<]*</(?:a|span)>', h)
    nxt = re.search(r'<(?:a|span) class="back-bar-nav[^"]*"[^>]*>[^<]*▶</(?:a|span)>', h)
    if not prev or not nxt:
        sys.exit(f"루트 카드의 이전·다음 링크를 못 찾았다: {path}")
    return {"accent": acc.groups(), "sub": sub.group(1), "name": name.group(1),
            "current": cur.group(1), "prev": prev.group(0), "next": nxt.group(0)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--force", action="store_true")
    t = ap.parse_args().ticker.upper()
    lo = t.lower()
    force = ap.parse_args().force
    dst = os.path.join(HERE, f"{t}_full_widget.html")
    if os.path.exists(dst) and not force:
        sys.exit(f"이미 있다: {dst} (덮어쓰려면 --force)")

    meta = root_meta(t)
    h = open(TEMPLATE, encoding="utf-8").read()

    def one(old, new):
        nonlocal h
        n = h.count(old)
        if n != 1:
            sys.exit(f"틀에서 정확히 한 번 나와야 한다 ({n}번): {old[:70]}")
        h = h.replace(old, new)

    # 1. 머리 — 틀의 NVDA 값을 루트 카드 값으로. 링크 치환보다 먼저 이름을 바꾸면
    #    "NVDA_full_widget.html" 이전 링크까지 바뀐다(AAPL 첫 시도에서 실제로 났다).
    h = h.replace("NVDA_", f"{t}_")
    h = re.sub(r"\bnvda(?=[A-Z])", lo, h)
    one("<title>NVDA 종합 분석 위젯", f"<title>{t} 종합 분석 위젯")
    one('<span class="ticker-badge">NVDA</span>', f'<span class="ticker-badge">{t}</span>')
    one("NASDAQ · AI 반도체", meta["sub"])
    one('<div class="company-name">NVIDIA Corporation</div>', f'<div class="company-name">{meta["name"]}</div>')
    one('<span class="back-bar-current">NVDA · 시총 1위</span>', f'<span class="back-bar-current">{meta["current"]}</span>')
    one('<span class="back-bar-nav disabled">◀ 이전</span>', meta["prev"])
    m = re.search(r'<a class="back-bar-nav" href="[A-Z]+_full_widget\.html">다음 [A-Z]+ ▶</a>', h)
    if not m:
        sys.exit("틀의 다음 링크를 못 찾았다")
    h = h[:m.start()] + meta["next"] + h[m.end():]
    h = h.replace('aria-label="NVDA ', f'aria-label="{t} ')
    one("지난 5년 NVDA 자신의 배수", f"지난 5년 {t} 자신의 배수")
    h = re.sub(r"(python3 v2/build_[a-z_]+\.py) NVDA", rf"\1 {t}", h)
    h = h.replace("stockanalysis.com/stocks/nvda/", f"stockanalysis.com/stocks/{lo}/")

    # 2. 색
    a1, a2, a3 = meta["accent"]
    h = h.replace(f"--accent: {NVDA_ACCENT[0]}; --accent2: {NVDA_ACCENT[1]}; --accent3: {NVDA_ACCENT[2]};",
                  f"--accent: {a1}; --accent2: {a2}; --accent3: {a3};")
    h = h.replace(f"rgba({NVDA_RGB},", f"rgba({rgb(a1)},").replace("#76b900", a1).replace("#9fdb2f", a2)

    # 4. NVDA 전용 툴팁 문장 — 그대로 복제되면 새 카드에 NVDA 사실이 뜬다(AAPL 첫 변환 때 Codex가 잡음).
    #    "확인 필요"로 바꿔 두고 새 종목 사실로 다시 쓴다. 상수 {T}_SCORES도 다시 채울 것.
    for old in ("장기차입금이 반년 사이 $7.5B → $32.4B로 늘어 차입금의존도가 4.1%에서 10.4%가 됐다.",
                "⚠ PER이 구조적으로 내려오는 중이라 과거 분포는 현재보다 높게 잡힌다 —"):
        if old in h:
            h = h.replace(old, "(확인 필요 — NVDA 문장 자리)")
    h = h.replace(' "자기 역사상 싸다"가 "지금 싸다"를 뜻하지 않는다.', "")
    h = h.replace("분기(Q2 FY27), 성장률은", "분기(확인 필요), 성장률은")

    open(dst, "w", encoding="utf-8").write(h)

    # 3. 남은 NVDA 흔적 — 이전 카드 링크 외에는 전부 이후 단계에서 채울 NVDA 내용이다.
    left = [(i + 1, l.strip()[:110]) for i, l in enumerate(h.split("\n"))
            if re.search(r"nvda|nvidia", l, re.I)]
    print(f"작성: {dst}")
    print(f"남은 NVDA 흔적 {len(left)}줄 (데이터 블록·산문·뉴스는 다음 단계에서 교체):")
    for n, l in left:
        print(f"  {n}: {l}")
    for lit in ("118,185,0", "#76b900", "#9fdb2f", "#aeff20", "#3b5d00"):
        if lit in h:
            print(f"⚠ NVDA 색 리터럴이 남았다: {lit}")


if __name__ == "__main__":
    main()
