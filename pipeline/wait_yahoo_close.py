#!/usr/bin/env python3
"""Wait out Yahoo's evening blank-close window before fetching prices.

Yahoo blanks the day's close on individual stocks' daily bars for a while in the evening
(2026-10-19 probe: bar present, close null, 20:16-21:16 ET; fine at 19:56 and 21:36). Since
2026-09-11 the evening refresh read the previous session on 14 of 24 runs, every ticker at
once; GitHub starts it 2-5 h late, into that window. How many of those 14 were this pattern
rather than no bar at all (09-14, 09-16, 09-21 per daily_refresh.yml) the old logs can't say -
only 10-19 was observed. This polls a
few large stocks; while any of them shows the expected session's bar with a null close, it
sleeps and looks again, up to --tries times. Then fetch_prices.py runs as usual, and if the
close is still blank it falls back to meta (fetch_prices.fill_from_meta).

Waits only on the blank-close pattern: no bar for the expected session (a holiday, or the
provider simply late) does not wait - the next scheduled pass handles that, as before. Never
fails the job: a network error or anything unexpected ends the wait and lets the fetch run.

Usage: python3 pipeline/wait_yahoo_close.py [--tries 6] [--gap 1200] [--now ISO]
"""
import argparse
import json
import sys
import time
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fetch_prices as fp  # noqa: E402

SYMBOLS = ("AAPL", "MSFT", "NVDA")
URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=5d&interval=1d"


def expected_session(now_et):
    """The latest weekday whose close has settled by now_et (holidays not known here)."""
    d = now_et.date()
    while d.weekday() >= 5 or now_et < datetime.combine(d, fp.SETTLE, fp.ET):
        d -= timedelta(days=1)
    return d.isoformat()


def blank_close(chart, session):
    """True when the chart's last bar is `session` and its close is null."""
    r = ((chart.get("chart") or {}).get("result") or [None])[0]
    if not r:
        return False
    ts = r.get("timestamp") or []
    closes = r["indicators"]["quote"][0].get("close") or []
    if not ts or len(closes) != len(ts):
        return False
    return (datetime.fromtimestamp(ts[-1], fp.ET).date().isoformat() == session
            and closes[-1] is None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tries", type=int, default=6)
    ap.add_argument("--gap", type=int, default=1200)
    ap.add_argument("--now", default=None)
    a = ap.parse_args()
    for i in range(a.tries + 1):
        now = datetime.fromisoformat(a.now).astimezone(fp.ET) if a.now else datetime.now(fp.ET)
        session = expected_session(now)
        try:
            blank = [s for s in SYMBOLS
                     if blank_close(json.loads(fp.http_get(URL.format(symbol=urllib.parse.quote(s)))), session)]
        except Exception as e:  # never block the refresh on this check
            print(f"wait check failed ({type(e).__name__}: {e}) - fetching now")
            return
        if not blank:
            print(f"{now:%H:%M} ET: no blank {session} close - fetching now")
            return
        if i == a.tries:
            print(f"{now:%H:%M} ET: {session} close still blank on {', '.join(blank)} after "
                  f"{a.tries} waits - fetching; fetch_prices falls back to meta")
            return
        print(f"{now:%H:%M} ET: {session} close blank on {', '.join(blank)} - "
              f"waiting {a.gap // 60} min ({i + 1}/{a.tries})", flush=True)
        time.sleep(a.gap)


if __name__ == "__main__":
    main()
