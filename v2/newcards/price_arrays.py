#!/usr/bin/env python3
"""v2 카드의 일봉·이동평균 배열에 새 종가를 붙인다 — 매일 가격 재빌드(build.py --price)의 첫 단계(2026-10-06 사용자 결정).

받는 규칙·검사는 루트 카드용 매일 갱신(pipeline/update_cards.py)과 같은 함수를 그대로 쓴다:
Yahoo 일봉(동부 16:20 뒤에만 확정), 카드에 이미 있는 봉이 다르면 바꾸고 새 봉은 붙이고, 이동평균은 바뀐 자리부터
다시 계산하고, 앞쪽은 1,255봉에서 자른다. 기준 세션은 홈페이지 가격 파일(site_data/stocks.json)의 그 종목 세션,
홈페이지에 아직 없는 종목은 파일 전체의 priceSession이다.

    python3 v2/newcards/price_arrays.py KO                 # v2/KO_full_widget.html 을 고친다
    python3 v2/newcards/price_arrays.py KO --card X.html   # 다른 파일(사본)을 고친다
    python3 v2/newcards/price_arrays.py KO --dry
종료 코드 0 = 고쳤거나 이미 최신, 1 = 멈춤(카드는 그대로 — 이유를 찍는다).
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
sys.path.insert(0, os.path.join(REPO, "pipeline"))
import update_cards as uc   # noqa: E402
import fetch_prices as fp   # noqa: E402

SYMBOL = {"BRKB": "BRK-B"}   # 홈페이지에 없는 종목의 Yahoo 기호(있는 종목은 stocks.json의 yahooSymbol)


def fix_header(html, T):
    """헤더 현재가·등락·기준일을 카드 일봉 마지막 봉으로(root_arrays.py와 같은 규칙). 은행 기반·손 카드는 헤더를 다시 쓰는
    단계가 없어 일봉만 10/6이고 헤더는 10/5로 남았다(2026-10-07 JPM·NVDA)."""
    D = json.loads(re.search(rf"const {T}_DAILY\s*=\s*(\[.*?\]);", html, re.S).group(1).replace("'", '"'))
    lastb, prevb = D[-1], D[-2]
    c = (lastb[4] / prevb[4] - 1) * 100
    up = c >= 0
    newp = (f'<div class="price-main"><span class="price-change" style="color:var(--{"green" if up else "red"});">'
            f'{"▲ +" if up else "▼ −"}{abs(c):.2f}%</span> ${lastb[4]:.2f}</div>')
    html, k = re.subn(r'<div class="price-main">.*?</div>', lambda _: newp, html, count=1, flags=re.S)   # 여러 줄이어도(Codex)
    if k != 1:
        raise SystemExit(f"{T}: 헤더 현재가 자리를 못 찾았다")
    return re.sub(r'현재가 \(\d{4}\.\d\d\.\d\d\)', f'현재가 ({lastb[0].replace("-", ".")})', html, count=1)


def compact(html, T):
    """생성기가 json.dumps 기본값(쉼표 뒤 공백)으로 쓴 배열 줄을 루트 카드 꼴(공백 없음)로 바꾼다 — 읽는 규칙이 그 꼴만 받는다."""
    out = []
    for line in html.split("\n"):
        m = uc.ARRAY_LINE.match(line)
        if m and ", " in m.group(4):
            line = m.group(1) + json.dumps(json.loads(m.group(4)), separators=(",", ":")) + m.group(5)
        out.append(line)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--card", default=None)
    ap.add_argument("--session", default=None, help="기준 세션(기본: stocks.json)")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--fixtures", default=None)
    a = ap.parse_args()
    T = a.ticker.upper()
    path = Path(a.card or os.path.join(V2, f"{T}_full_widget.html"))
    data = json.load(open(os.path.join(REPO, "site_data", "stocks.json"), encoding="utf-8"))
    entry = next((e for e in data["tickers"] if e["ticker"] == T), None)
    lost = set()
    if a.session:
        session = a.session
    elif entry:
        p = entry["price"]
        if p.get("status") in ("unavailable", "suspicious") or not p.get("session"):
            print(f"{T}: 멈춤 — 홈페이지 가격이 {p.get('status')}"); sys.exit(1)
        session, lost = p["session"], set(p.get("providerGaps") or [])
    else:
        session = data["priceSession"]
    symbol = (entry or {}).get("yahooSymbol") or SYMBOL.get(T, T)

    html = compact(path.read_text(encoding="utf-8"), T)
    try:
        lines, arrays = uc.parse_card_arrays(html)
        empty = [k for k in arrays if k != "DAILY" and not arrays[k]["tokens"]]   # 상장이 짧아 비워 둔 이동평균(SPCX MA120)
        for k in empty:
            arrays[k]["tokens"] = ["null"] * len(arrays["DAILY"]["tokens"])
        n0 = len(arrays["DAILY"]["tokens"])
        for kind in arrays:
            if len(arrays[kind]["tokens"]) != n0:
                raise uc.EditError(f"{kind} 길이 {len(arrays[kind]['tokens'])} ≠ DAILY {n0}")
        last = uc.bar_values(arrays["DAILY"]["tokens"][-1])[0]
        if last >= session:
            fixed = fix_header(html, T)
            if fixed != html and not a.dry:
                path.write_text(fixed, encoding="utf-8")
            print(f"{T}: 이미 최신({last})" + (" · 헤더 현재가를 일봉에 맞춤" if fixed != html else "")); return
        now_et = datetime.now(fp.ET)
        fetched, splits = uc.fetch_bars(symbol, uc.fetch_range(last, session), a.fixtures, now_et, session)
        if not fetched:
            raise uc.Hold("받은 확정 봉이 없다")
        notes = []
        changed, replaced, appended, inserted, extra = uc.sync_bars(arrays, fetched, splits, notes, lost)
        if [d for d in extra if d not in lost]:
            raise uc.Hold(f"카드에만 있는 세션: {extra[:5]}")
        uc.extend_mas(arrays, changed)
        trimmed = uc.trim_front(arrays)
        for kind in arrays:
            if len(arrays[kind]["tokens"]) != len(arrays["DAILY"]["tokens"]):
                raise uc.EditError(f"맞춘 뒤 {kind} 길이가 DAILY와 다르다")
        # 루트 카드 매일 갱신과 같은 검사(Codex 2026-10-06): 날짜 순서, 목표 세션 도달, 홈 종가 일치, 새 봉 OHLC
        bars = [uc.bar_values(t) for t in arrays["DAILY"]["tokens"]]
        for x, y in zip(bars, bars[1:]):
            if y[0] <= x[0]:
                raise uc.EditError(f"날짜가 늘지 않는다: {y[0]}")
        if bars[-1][0] != session:
            raise uc.Hold(f"{session} 확정 봉이 아직 없다(카드 끝 {bars[-1][0]})")
        if entry and entry["price"].get("session") == session and entry["price"].get("close") is not None \
                and not uc.close_matches(entry["price"]["close"], arrays["DAILY"]["tokens"][-1]):
            raise uc.EditError(f"종가 {bars[-1][4]} ≠ 홈 종가 {entry['price']['close']}")
        start = max(0, (changed if changed is not None else len(bars)) - trimmed)
        for d, o, h, l, c, v in bars[start:]:
            if min(o, h, l, c) <= 0 or v < 0 or h + 0.011 < max(o, c) or l - 0.011 > min(o, c):
                raise uc.Hold(f"{d} 봉이 앞뒤가 안 맞는다: o{o} h{h} l{l} c{c} v{v}")
    except (uc.EditError, uc.Hold, ValueError) as e:
        print(f"{T}: 멈춤 — {e}"); sys.exit(1)
    for kind, arr in arrays.items():
        if kind in empty and all(t == "null" for t in arr["tokens"]):
            arr["tokens"] = []   # 아직 다 비어 있으면 원래대로 빈 배열
        body = "[" + ",".join(arr["tokens"]) + "]"
        lines[arr["line"]] = arr["head"] + body + arr["tail"]
    new_last = uc.bar_values(arrays["DAILY"]["tokens"][-1])
    print(f"{T}: {last} → {new_last[0]} 종가 {new_last[4]} · 새 봉 {appended} · 바뀐 봉 {replaced} · 앞 자름 {trimmed}"
          + (f" · {'; '.join(notes)}" if notes else ""))
    out = "\n".join(lines)
    out = fix_header(out, T)
    if not a.dry:
        path.write_text(out, encoding="utf-8")


if __name__ == "__main__":
    main()
