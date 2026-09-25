#!/usr/bin/env python3
"""카드의 `{T}_DCF` 블록을 `build_dcf`에서 만들어 교체한다.

예전에는 세 시나리오 값·요구 성장률·환산 성장률을 손으로 옮겨 적었다. 그러다
AMZN의 baseEquivGrowth가 기본값($65.36)이 아닌 다른 입력의 값(6.74%, 맞는 값 4.01%)으로
남아 있었다(2026-09-24). 한 스크립트가 같은 입력으로 전부 계산해 넣는다.

블록에 들어가는 값
------------------
    low · base · high        세 시나리오 주당 가치 (할인율 10% · 영구 2.5%)
    requiredGrowth           현재가를 정당화하는 5년 일정 매출 성장률 (기본 시나리오 마진·매출/자본)
    baseEquivGrowth          기본 시나리오 가치를 같은 방식으로 환산한 성장률
    reqMode                  "growth" | "margin" — 요구 성장률이 최근 5년 실제 성장의
                             REQ_GROWTH_MULTIPLE배를 넘거나 해가 없으면 "margin"(2026-09-24 사용자 결정)
    requiredMargin           reqMode가 margin일 때: 기본 시나리오 성장 경로에서 현재가가 요구하는 영업이익률
    marginNow · growth5y     비교 기준 (최근 4분기 영업이익률, 최근 5년 연평균 매출 성장)
    nonopPerShare            주주가치에 더한 비영업 자산(주당) — 카드에 분리 표기(사용자 결정)
    asOf                     카드 일봉 마지막 날

사용법
------
    python3 v2/build_dcf_block.py AMZN            # 카드 블록 교체
    python3 v2/build_dcf_block.py AMZN --dry-run  # 값만 찍는다
"""
import argparse
import contextlib
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_dcf as d  # noqa: E402
import fx  # noqa: E402

WACC, TERM = 0.10, 0.025


def compute(t):
    with contextlib.redirect_stdout(io.StringIO()):
        daily = d.bmh.load_daily(t)
        price, asof = daily[-1][4], daily[-1][0]
        # 재무가 현지 통화(TSM)면 역산은 현지 통화 가격으로 하고, 주당 가치는 그날 환율로 달러로 되돌린다.
        r = fx.rate(t, asof)
        price_local = price * r
        # 기준일은 카드 일봉의 마지막 날 — 그 뒤 공시가 캐시에 있어도 쓰지 않는다(Codex).
        base = d.base_inputs(t, asof)
        hist = d.history(t, asof)
        s = d.scenarios(base, hist, WACC, TERM)
        mp = d.margin_path_for(hist, "기본")
        sp = d.s2c_path_for(base, "기본")[0]
        req = d.implied_growth(base, price_local, WACC, TERM, margin_path=mp, s2c=sp)
        beq = d.implied_growth(base, s[1]["per_share"], WACC, TERM, margin_path=mp, s2c=sp)
        g5 = hist["growth_5y"]
        mode = "growth"
        # 5년 성장이 0 이하면 3배 문턱도 0 이하라, 양의 요구 성장은 전부 마진 모드가 된다.
        if req is None or (g5 is not None and req > d.REQ_GROWTH_MULTIPLE * g5):
            mode = "margin"
        g0 = max(g5 or TERM, TERM)
        path = [g0 + (TERM - g0) * i / 4 for i in range(5)]
        rm = d.implied_margin(base, price_local, WACC, TERM, path, s2c=sp) if mode == "margin" else None
    return {
        "low": round(s[0]["per_share"] / r, 2), "base": round(s[1]["per_share"] / r, 2),
        "high": round(s[2]["per_share"] / r, 2),
        "requiredGrowth": round(req, 4) if req is not None else None,
        "baseEquivGrowth": round(beq, 4) if beq is not None else None,
        "reqMode": mode,
        "requiredMargin": round(rm, 4) if rm is not None else None,
        "marginNow": round(hist["margin_now"], 4), "growth5y": round(g5, 4) if g5 else None,
        "nonopPerShare": round(s[1]["nonop_per_share"] / r, 2),
        "s2cFallback": any(x["s2c_fallback"] for x in s),
        "asOf": asof,
    }, price


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    t = args.ticker.upper()
    blk, price = compute(t)
    print(t, f"${price}", json.dumps(blk, ensure_ascii=False))
    if blk["s2cFallback"]:
        print("  ⚠ 최근 1년 매출/자본을 못 구해 평균으로 떨어진 시나리오가 있다")
    if args.dry_run:
        return
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{t}_full_widget.html")
    html = open(path, encoding="utf-8").read()
    pat = re.compile(rf"const {t}_DCF = \{{.*?\}};[^\n]*", re.S)
    if len(pat.findall(html)) != 1:
        sys.exit(f"{path}: const {t}_DCF 블록이 정확히 하나가 아니다")
    js = f"const {t}_DCF = {json.dumps(blk, ensure_ascii=False)};   // build_dcf_block.py"
    open(path, "w", encoding="utf-8").write(pat.sub(lambda _: js, html))
    print("교체:", path)


if __name__ == "__main__":
    main()
