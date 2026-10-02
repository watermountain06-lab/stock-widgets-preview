#!/usr/bin/env python3
"""루트 카드가 없는 새 종목(71위부터, 2026-10-01)의 v2 카드 배열 — 일봉·이동평균·예상밴드 백테스트.

루트 카드 70장은 배열(DAILY·MA5/20/60/120·BACKTEST)을 루트에서 잘라 붙였다. 새 종목은 루트가 없어 직접 만든다.
- DAILY: Yahoo 차트(분할 조정 OHLCV)에서 기준일까지 마지막 1,255거래일([날짜, 시, 고, 저, 종, 거래량], 가격 소수 둘째 자리).
- MA: 같은 종가의 단순 이동평균(소수 셋째 자리). 루트 카드는 앞쪽 12거래일만 더 받아 앞부분이 비었지만(null),
  여기서는 이력을 넉넉히 받아 빈칸 없이 계산한다.
- BACKTEST: scripts/compute_earnings_backtest_band.py 기본 설정(직전 2년 PER 분포, 10~90 백분위, 반감기 180일) —
  루트 카드와 같은 설정이다(DE로 재현 확인: 체크포인트 12개·첫 밴드 10.94~19.28배 일치).

    python3 v2/new_ticker_arrays.py ADI --yahoo /path/adi_yahoo.json --asof 2026-09-30
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
N_DAYS = 1255


def bars_from_yahoo(path, asof):
    r = json.load(open(path))["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    off = r.get("meta", {}).get("gmtoffset", 0)
    out = []
    for i, ts in enumerate(r["timestamp"]):
        day = time.strftime("%Y-%m-%d", time.gmtime(ts + off))
        o, h, l, c, v = (q[k][i] for k in ("open", "high", "low", "close", "volume"))
        if day > asof or None in (o, h, l, c):
            continue
        out.append([day, round(o, 2), round(h, 2), round(l, 2), round(c, 2), int(v or 0)])
    return out


def sma(closes, n):
    out, s = [], 0.0
    for i, c in enumerate(closes):
        s += c
        if i >= n:
            s -= closes[i - n]
        out.append(round(s / n, 3) if i >= n - 1 else None)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--yahoo", required=True)
    ap.add_argument("--asof", required=True)
    a = ap.parse_args()
    t = a.ticker.upper()
    allbars = bars_from_yahoo(a.yahoo, a.asof)
    assert allbars and allbars[-1][0] == a.asof, ("기준일 봉이 없다", allbars[-1][0] if allbars else None)
    assert len(allbars) >= N_DAYS + 120, ("이력이 짧다 — 이동평균 앞부분을 채울 수 없다", len(allbars))
    closes = [b[4] for b in allbars]
    ma = {n: sma(closes, n)[-N_DAYS:] for n in (5, 20, 60, 120)}
    daily = allbars[-N_DAYS:]
    assert all(x is not None for n in ma for x in ma[n])

    tmp = f"/tmp/{t}_daily_for_backtest.json"
    json.dump({"daily": daily}, open(tmp, "w"))
    eps = os.path.join(REPO, "scripts", f"{t}_eps_history.json")
    out = f"/tmp/{t}_backtest.json"
    r = subprocess.run([sys.executable, os.path.join(REPO, "scripts", "compute_earnings_backtest_band.py"), t,
                        "--eps", eps, "--daily-json", tmp, "--out", out], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip()[-500:])
    bt = json.load(open(out))["checkpoints"]

    p = os.path.join(HERE, f"{t}_full_widget.html")
    h = open(p, encoding="utf-8").read()

    def put(name, value):
        nonlocal h
        m = re.search(rf"const {t}_{name}\s*=\s*\[", h)
        assert m, name
        st = m.end() - 1
        d, ins = 0, None
        for i in range(st, len(h)):
            ch = h[i]
            if ins:
                if ch == ins and h[i - 1] != "\\":
                    ins = None
                continue
            if ch in "\"'":
                ins = ch
            elif ch == "[":
                d += 1
            elif ch == "]":
                d -= 1
                if d == 0:
                    h = h[:st] + json.dumps(value, ensure_ascii=False, separators=(", ", ": ")) + h[i + 1:]
                    return
        raise AssertionError(name)

    put("DAILY", daily)
    for n in (5, 20, 60, 120):
        put(f"MA{n}", ma[n])
    put("BACKTEST", bt)
    # 헤더 현재가·등락률·기준일 — 루트 카드 배열 스크립트가 하던 일(빠뜨려 ADI 헤더에 NVDA 틀 값 $228.87이 남았다, Codex 2026-10-01)
    last, prev = daily[-1], daily[-2]
    c = (last[4] / prev[4] - 1) * 100
    up = c >= 0
    new = (f'<div class="price-main"><span class="price-change" style="color:var(--{"green" if up else "red"});">'
           f'{"▲ +" if up else "▼ −"}{abs(c):.2f}%</span> ${last[4]:.2f}</div>')
    h, k1 = re.subn(r'<div class="price-main">.*?</div>', lambda m: new, h, count=1)
    h, k2 = re.subn(r"현재가 \(\d{4}\.\d\d\.\d\d\)", f'현재가 ({last[0].replace("-", ".")})', h, count=1)
    assert k1 == 1 and k2 == 1, (k1, k2)
    open(p, "w", encoding="utf-8").write(h)
    print("arrays", len(daily), daily[0][0], daily[-1], "MA120", ma[120][-1], "backtest", len(bt))


if __name__ == "__main__":
    main()
