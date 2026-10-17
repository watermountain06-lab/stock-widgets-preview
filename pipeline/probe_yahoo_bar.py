#!/usr/bin/env python3
"""Temporary probe (2026-10-17): when does Yahoo's daily chart first show the
day's bar after the close, and does the URL form matter?

The evening refresh missed the same-day close on 14 of 24 runs since
2026-09-11, with every ticker and index missing together and no clock-time
pattern (19:48 ET hit, 21:14 ET missed). Suspect: a cached response for the
fixed `range=1mo` URL. This polls a few symbols with the production URL and
with variants that change the URL each time, and prints one line per fetch.
Reviewed by Codex and Fable 2026-10-17 (raw last bar, per-request time,
backend-cluster headers, runner region).
Writes nothing to the site. Delete with its workflow once answered.
"""
import json
import sys
import urllib.parse
import time
import urllib.request
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
SYMBOLS = ["SPY", "^GSPC", "AAPL", "NVDA"]
BASE = "https://{host}/v8/finance/chart/{sym}"


def variants(sym, now):
    s = urllib.parse.quote(sym, safe="")
    p2 = int(now.timestamp())
    p1 = int((now - timedelta(days=40)).timestamp())
    q1 = BASE.format(host="query1.finance.yahoo.com", sym=s)
    return {
        "prod": q1 + "?range=1mo&interval=1d&events=split",
        "q2": BASE.format(host="query2.finance.yahoo.com", sym=s) + "?range=1mo&interval=1d&events=split",
        "period": q1 + f"?period1={p1}&period2={p2}&interval=1d&events=split",
        "bust": q1 + f"?range=1mo&interval=1d&events=split&_={p2}",
        "5d": q1 + "?range=5d&interval=1d",
        "5m": q1 + "?range=1d&interval=5m",
    }


def et(ts):
    return datetime.fromtimestamp(ts, ET).strftime("%m-%d %H:%M") if ts else "-"


def last_bar(url):
    """One fetch, summarized. Keeps the raw last bar even when its close is null, so a
    missing bar and a null-close bar (the 2026-09-22 case) read differently."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        hdr = {k.lower(): v for k, v in resp.headers.items()}
        data = json.loads(resp.read())
    r = data["chart"]["result"][0]
    m, q = r["meta"], r["indicators"]["quote"][0]
    ts = r.get("timestamp") or []
    tail = " ".join(f"{et(t)}:{c}/{v}" for t, c, v in list(zip(ts, q["close"], q["volume"]))[-3:])
    reg = (m.get("currentTradingPeriod") or {}).get("regular") or {}
    head = " ".join(f"{k}={hdr[k]}" for k in
                    ("date", "age", "etag", "expires", "y-rid", "x-envoy-decorator-operation",
                     "x-envoy-upstream-service-time") if k in hdr)
    return (f"n={len(ts)} tail=[{tail}] rmt={et(m.get('regularMarketTime'))} "
            f"rmp={m.get('regularMarketPrice')} range={m.get('range')!r} "
            f"regular={et(reg.get('start'))}-{et(reg.get('end'))} | {head}")


def runner_info():
    for name, url, h in (("ip", "https://api.ipify.org", {}),
                         ("region", "http://169.254.169.254/metadata/instance/compute/location"
                                    "?api-version=2021-02-01&format=text", {"Metadata": "true"})):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=5) as resp:
                print(f"runner {name}: {resp.read().decode()[:60]}", flush=True)
        except Exception as e:
            print(f"runner {name}: unavailable ({type(e).__name__})", flush=True)
    print(f"runner clock: {datetime.now(ET):%Y-%m-%d %H:%M:%S %Z}", flush=True)


def main():
    rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    gap = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    runner_info()
    for i in range(rounds):
        began = time.monotonic()
        for sym in SYMBOLS:
            for name, url in variants(sym, datetime.now(ET)).items():
                t0 = time.monotonic()
                stamp = datetime.now(ET)
                try:
                    out = last_bar(url)
                except Exception as e:
                    out = f"error {type(e).__name__}: {e}"
                print(f"{stamp:%m-%d %H:%M:%S} ET {time.monotonic() - t0:5.1f}s  {sym:6} {name:6} {out}",
                      flush=True)
                time.sleep(0.3)
        if i < rounds - 1:
            time.sleep(max(0, gap - (time.monotonic() - began)))  # fixed cadence, not gap + round time


if __name__ == "__main__":
    main()
