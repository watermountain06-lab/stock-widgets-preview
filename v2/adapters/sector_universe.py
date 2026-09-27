#!/usr/bin/env python3
"""표본이 모자란 섹터의 동종업 비교군을 S&P500 구성종목으로 넓힌다(2026-09-27 사용자 결정, LLY).

사이트 비교 유니버스(site_data/valuation_base, 카드 종목 약 70개)에 헬스케어는 7종목뿐이라
배수마다 동종업이 2~6곳이어서 `build_peer_score.MIN_PEERS`(8)를 못 넘었다. 여기서는
S&P500의 같은 GICS 섹터 종목(stock-widgets-redesign/scripts/sp500.json) 전체에 대해
**카드와 같은 엔진**(build_multiple_history)으로 기준일의 다섯 배수를 계산해 파일 하나로 남긴다.
build_peer_score는 SECTOR_UNIVERSE에 적힌 섹터만 이 파일을 비교군으로 쓴다(다른 섹터는 그대로).

    python3 v2/adapters/sector_universe.py "Health Care" --asof 2026-09-25

- 가격: Yahoo 일봉(1년), 기준일 종가까지. 분할 기록도 같은 요청에서 받는다.
- EPS: scripts/fetch_eps_history.py(카드와 같은 SEC 희석 EPS). 분할 손 목록이 없으므로
  기준일 전 400일 안에 분할이 있으면 그 종목의 PER은 뺀다(분할 전 EPS가 섞인다).
- 배수 정의·적자 처리(음수면 "negative" → 동종업 꼴찌)·분모 결측은 카드와 같다.
- 생존자 표본(현재 구성종목)이다. 기준일 하나의 횡단면이라 과거 백분위와는 무관하다.
- SEC 요청은 종목마다 쉬어 간다(429 방지). 이미 받은 companyfacts는 .sec_cache를 쓴다.
"""
import argparse
import contextlib
import io
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
sys.path.insert(0, V2)
sys.path.insert(0, os.path.join(REPO, "scripts"))
import build_multiple_history as bmh  # noqa: E402
import build_peer_score as ps  # noqa: E402
import fetch_eps_history as feh  # noqa: E402

SP500 = os.path.join(os.path.dirname(REPO), "stock-widgets-redesign", "scripts", "sp500.json")
OUT_DIR = os.path.join(V2, "peer_universe")
UA = "Mozilla/5.0"   # 긴 브라우저 UA는 Yahoo가 429로 막았다(2026-09-27)


def sp500_rows():
    d = json.load(open(SP500))
    rows = d if isinstance(d, list) else d.get("tickers", d)
    return list(rows.values()) if isinstance(rows, dict) else rows


def yahoo(ticker, asof):
    sym = ticker.replace(".", "-")
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1y&interval=1d&events=split"
    # urllib는 Yahoo가 429로 막는다 — curl로 받는다(reference_stock_widgets_yahoo_kr_ticker).
    raw = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, text=True, timeout=60).stdout
    r = json.loads(raw)["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    bars = []
    for i, ts in enumerate(r["timestamp"]):
        day = time.strftime("%Y-%m-%d", time.gmtime(ts + r.get("gmtoffset", 0)))
        if day > asof or q["close"][i] is None or not q["volume"][i]:
            continue
        bars.append([day, q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i]])
    splits = sorted(time.strftime("%Y-%m-%d", time.gmtime(s["date"]))
                    for s in (r.get("events", {}).get("splits") or {}).values())
    return bars, splits


def one(ticker, cik, asof, eps_dir):
    bars, splits = yahoo(ticker, asof)
    if not bars or bars[-1][0] != asof:
        return None, f"기준일 종가 없음({bars[-1][0] if bars else '—'})"
    eps_path = os.path.join(eps_dir, f"{ticker}_eps_history.json")
    if not os.path.exists(eps_path):
        subprocess.run([sys.executable, os.path.join(REPO, "scripts", "fetch_eps_history.py"), ticker,
                        "--cik", cik, "--out", eps_path], capture_output=True, text=True)
        time.sleep(0.6)
    feh.CIKS[ticker] = cik
    orig = bmh.load_daily
    bmh.load_daily = lambda t, path=None: bars
    out = os.path.join(eps_dir, f"{ticker}_multiples.json")
    old_argv, old_env = sys.argv, os.environ.get("EPS_HISTORY")
    try:
        sys.argv = ["x", ticker, "--json", out]
        os.environ["EPS_HISTORY"] = eps_path if os.path.exists(eps_path) else ""
        with contextlib.redirect_stdout(io.StringIO()):
            bmh.main()
    finally:
        bmh.load_daily, sys.argv = orig, old_argv
        if old_env is None:
            os.environ.pop("EPS_HISTORY", None)
        else:
            os.environ["EPS_HISTORY"] = old_env
    m = ps.self_multiples(out)      # 카드 본인 값과 같은 규칙(음수 → negative, 결측 → 제외)
    recent = [s for s in splits if (time.mktime(time.strptime(asof, "%Y-%m-%d")) -
                                    time.mktime(time.strptime(s, "%Y-%m-%d"))) / 86400 <= 400]
    note = None
    if recent and "per" in m:
        m.pop("per")
        note = f"최근 분할 {recent[-1]} — PER 제외"
    return m, note


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sector")
    ap.add_argument("--asof", required=True)
    a = ap.parse_args()
    rows = [r for r in sp500_rows() if r.get("sector") == a.sector]
    slug = a.sector.lower().replace(" ", "_")
    eps_dir = os.path.join(OUT_DIR, slug)
    os.makedirs(eps_dir, exist_ok=True)
    res = {"sector": a.sector, "asOf": a.asof, "source": "S&P500 현재 구성종목(sp500.json) · 카드와 같은 엔진",
           "tickers": {}, "skipped": {}}
    for r in rows:
        t = (r.get("ticker") or r.get("symbol")).replace("-", ".")
        cik = str(r.get("cik")).zfill(10)
        try:
            m, note = one(t, cik, a.asof, eps_dir)
        except Exception as e:  # 한 종목 실패가 전체를 멈추지 않게
            m, note = None, f"오류: {type(e).__name__}: {e}"
        if m is None:
            res["skipped"][t] = note
        else:
            res["tickers"][t] = m
            if note:
                res["skipped"][t] = note
        print(t, "→", m if m is not None else note, flush=True)
        time.sleep(0.4)
    path = os.path.join(OUT_DIR, f"{slug}.json")
    json.dump(res, open(path, "w"), ensure_ascii=False, indent=1)
    print("저장:", path, len(res["tickers"]), "종목")


if __name__ == "__main__":
    main()
