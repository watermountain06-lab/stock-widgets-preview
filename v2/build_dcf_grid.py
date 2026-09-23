#!/usr/bin/env python3
"""내재가치 탭의 "직접 바꿔보기"가 쓰는 격자를 만든다.

시나리오 3 × 할인율 × 영구성장률의 주당 내재가치를 `build_dcf.scenarios()`로
미리 전부 계산해 카드에 박는다. 카드 안의 JS는 이 표에서 값을 **찾기만** 한다.

JS로 DCF를 다시 짜지 않는 이유는 계산이 두 벌이 되기 때문이다. 한쪽만 고쳐지면
슬라이더의 $315와 요약 격자의 $315가 어느 날 조용히 갈라진다.

사용법
------
    python3 v2/build_dcf_grid.py NVDA            # 카드의 DCF_GRID 블록을 교체
    python3 v2/build_dcf_grid.py NVDA --dry-run  # 기본값 칸만 찍고 끝낸다
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_dcf as d  # noqa: E402

WACCS = [0.08, 0.09, 0.10, 0.11, 0.12]
TERMS = [0.015, 0.020, 0.025, 0.030, 0.035]
DEFAULT = (0.100, 0.025)   # 요약 격자·헤더의 $315가 쓰는 가정
NAMES = ["보수", "기본", "낙관"]

BEGIN, END = "/* DCF_GRID:BEGIN */", "/* DCF_GRID:END */"


def build(ticker):
    base = d.base_inputs(ticker)
    hist = d.history(ticker)
    values = {n: [] for n in NAMES}          # values[시나리오][영구성장 i][할인율 j]
    for g in TERMS:
        rows = {n: [] for n in NAMES}
        for w in WACCS:
            for s in d.scenarios(base, hist, w, g):
                rows[s["name"]].append(round(s["per_share"], 2))
        for n in NAMES:
            values[n].append(rows[n])
    return {"waccs": WACCS, "terms": TERMS, "default": list(DEFAULT), "values": values}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    t = args.ticker.upper()

    grid = build(t)
    gi, wi = TERMS.index(DEFAULT[1]), WACCS.index(DEFAULT[0])
    for n in NAMES:
        print(f"  {n} @ 할인율 {DEFAULT[0]:.1%} · 영구 {DEFAULT[1]:.1%}  ${grid['values'][n][gi][wi]:.2f}")
    if args.dry_run:
        return

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{t}_full_widget.html")
    html = open(path, encoding="utf-8").read()

    # 격자의 기본값 칸은 요약 격자·헤더가 읽는 NVDA_DCF와 같아야 한다.
    m = re.search(rf"const {t}_DCF = \{{low: ([\d.]+), base: ([\d.]+), high: ([\d.]+)", html)
    if not m:
        sys.exit(f"{path}: {t}_DCF 상수를 못 찾았다")
    for n, card in zip(NAMES, map(float, m.groups())):
        mine = grid["values"][n][gi][wi]
        if abs(mine - card) > 0.005:
            sys.exit(f"{n}: 격자 ${mine:.2f} ≠ {t}_DCF ${card:.2f} — build_dcf.py로 {t}_DCF부터 갱신할 것")

    block = f"{BEGIN}\nconst {t}_DCF_GRID = {json.dumps(grid, ensure_ascii=False)};\n{END}"
    pat = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    if len(pat.findall(html)) != 1:
        sys.exit(f"{path}: DCF_GRID 마커가 정확히 한 쌍이 아니다")
    html = pat.sub(lambda _: block, html)
    open(path, "w", encoding="utf-8").write(html)
    print("교체:", path)


if __name__ == "__main__":
    main()
