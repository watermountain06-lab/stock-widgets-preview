#!/usr/bin/env python3
"""StockAnalysis 예측 페이지에서 애널리스트 의견·목표가를 한 기준으로 받아 cfg에 쓴다(안건 D48, 2026-10-05).

예전 카드는 목표가 통계(평균·중앙·최저·최고)는 개별 목표가 표본(`targets`, 예: BA 16명)에서, 인원은 의견 집계(`recommendations`
마지막 달 total, 27명)에서 가져와 두 표본이 섞였다. 이제 같은 날 한 번 받아 두 인원을 나눠 적는다:
  n  = 의견을 낸 애널리스트 수(recommendations 마지막 항목 total) — 의견 막대의 분모
  nt = 목표가를 낸 애널리스트 수(targets.count) — 평균·중앙·최저·최고의 표본
페이지 본문의 "average price target"은 다른 집계(S&P Global 컨센서스)라 쓰지 않는다 — 표본 수·중앙값이 없다.

    python3 v2/newcards/fetch_analyst.py AAPL MSFT      # cfg_{t}.py의 ANALYST·ANALYST_ASOF를 고친다
    python3 v2/newcards/fetch_analyst.py --dry AAPL     # 받은 값만 찍는다
"""
import datetime
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = {"BRKB": "brk.b"}


def fetch(T):
    url = f"https://stockanalysis.com/stocks/{SLUG.get(T, T.lower())}/forecast/"
    # 짧은 브라우저 UA는 403 — curl UA(README)
    h = subprocess.run(["curl", "-s", "-A", "curl/8.4.0", url], capture_output=True, text=True, timeout=60).stdout
    rec = re.findall(r"\{buy:(\d+),date:\"([\d-]+)\",hold:(\d+),sell:(\d+),month:\"[^\"]*\",score:[\d.]+,total:(\d+),updated:\"[\d-]+\",consensus:\"([^\"]+)\",strongBuy:(\d+),strongSell:(\d+)\}", h)
    tg = re.search(r"targets:\{low:([\d.]+),high:([\d.]+),count:(\d+),median:([\d.]+),average:([\d.]+),updated:\"([\d-]+)\"", h)
    if not rec or not tg:
        raise ValueError(f"{T}: 페이지에서 의견·목표가를 못 찾음({len(h)}자)")
    b, d, hold, s, total, cons, sb, ss = rec[-1]
    low, high, cnt, med, avg, upd = tg.groups()
    num = lambda x: int(float(x)) if float(x).is_integer() else float(x)
    out = {"rating": cons, "n": int(total), "nt": int(cnt), "mean": num(avg), "median": num(med), "low": num(low), "high": num(high),
           "sb": int(sb), "b": int(b), "h": int(hold), "s": int(s), "ss": int(ss)}
    assert out["sb"] + out["b"] + out["h"] + out["s"] + out["ss"] == out["n"], (T, out)
    return out, upd


def write(T, A, asof):
    p = os.path.join(HERE, "cfg", f"cfg_{T.lower()}.py")
    s = open(p, encoding="utf-8").read()
    line = "ANALYST = " + repr(A)
    s, n = re.subn(r"^ANALYST = \{[^\n]*\}$", lambda _: line, s, count=1, flags=re.M)
    if n != 1:
        raise ValueError(f"{T}: cfg에 ANALYST 한 줄이 없다")
    if re.search(r"^ANALYST_ASOF = ", s, re.M):
        s = re.sub(r"^ANALYST_ASOF = .*$", f"ANALYST_ASOF = '{asof}'", s, count=1, flags=re.M)
    else:
        s = s.replace(line, line + f"\nANALYST_ASOF = '{asof}'", 1)
    open(p, "w", encoding="utf-8").write(s)


def main():
    args = sys.argv[1:]
    dry = "--dry" in args
    tickers = [a.upper() for a in args if a != "--dry"]
    for T in tickers:
        try:
            A, upd = fetch(T)
        except Exception as e:
            print(f"{T}: 실패 — {e}")
            continue
        asof = datetime.date.today().isoformat()
        print(f"{T}: {A} (목표가 갱신 {upd})")
        if not dry:
            write(T, A, asof)
        time.sleep(1.0)


if __name__ == "__main__":
    main()
