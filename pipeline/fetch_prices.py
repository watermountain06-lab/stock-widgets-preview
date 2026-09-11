#!/usr/bin/env python3
"""Daily price refresh: update every ticker's price block in
site_data/stocks.json from Yahoo's daily chart and set priceSession.

Rules (from the 2026-09-11 spike):
  - Yahoo's daily-bar timestamp is the session OPEN, so completeness is
    judged by the clock: the bar for ET date D counts only once it's past
    D 16:20 ET (the close plus a settling buffer). An in-progress bar is
    dropped. Half-day sessions (13:00 close) are deliberately not
    special-cased: the fixed cutoff only delays picking up a half-day close
    until 16:20 ET - a run before that keeps the previous session for every
    ticker alike, so nothing is mislabeled - and the scheduled run is after
    16:20 ET year-round. (An exchange calendar was suggested in review and
    declined 2026-09-11: hand-kept holiday dates for no correctness gain.)
  - meta.chartPreviousClose is the close before the requested RANGE, not the
    previous session, so prevClose is the prior completed bar's close.
  - Raw close, not adjclose (they differ by dividend adjustment).
  - Trailing null closes (holidays, gaps) are skipped; a duplicated date
    keeps its last bar.
Kept but marked suspicious (excluded from the ±5% counts):
  - volume under 15% of the prior 20-bar mean (an intraday-looking bar);
  - a split inside the fetched window (prevClose, shares and market cap all
    need a human look before the change % means anything).
priceSession is the latest completed session found this run. A ticker whose
latest completed bar is older (halt, missing bar), whose fetch failed (its
previous block is kept), or that wasn't refreshed this run is "stale".

Usage: python3 pipeline/fetch_prices.py [--tickers A,B] [--write]
                                        [--data PATH] [--fixtures DIR] [--now ISO]
  --fixtures DIR   read {SYMBOL}.json chart responses from DIR (tests)
  --now ISO        pretend it is this time (tests), e.g. 2026-09-10T18:00:00-04:00
"""
import argparse
import json
import statistics
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, time as dtime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ET = ZoneInfo("America/New_York")
CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1mo&interval=1d&events=split"
SETTLE = dtime(16, 20)
VOLUME_FLOOR = 0.15
BIG_MOVE = 0.15  # reported for a news check, not treated as an error


def fetch_chart(symbol, fixtures=None):
    if fixtures:
        path = Path(fixtures) / f"{symbol}.json"
        if not path.exists():
            raise FileNotFoundError(f"no fixture for {symbol}")
        return json.loads(path.read_text(encoding="utf-8"))
    url = CHART_URL.format(symbol=urllib.parse.quote(symbol, safe=""))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    time.sleep(0.2)
    return data


def completed_bars(chart, now_et):
    """([(date, close, volume)] of completed sessions oldest first, result dict)."""
    body = chart.get("chart") or {}
    if not body.get("result"):
        raise ValueError(f"no chart result ({body.get('error')})")
    r = body["result"][0]
    q = r["indicators"]["quote"][0]
    by_date = {}
    for ts, close, vol in zip(r.get("timestamp") or [], q["close"], q["volume"]):
        if close is None:
            continue
        d = datetime.fromtimestamp(ts, ET).date()
        if now_et < datetime.combine(d, SETTLE, ET):
            continue  # that session hasn't closed (plus buffer) yet
        by_date[d.isoformat()] = (d.isoformat(), close, vol or 0)
    return [by_date[k] for k in sorted(by_date)], r


def resolve_price(chart, now_et):
    """A schema-v1 price block from one daily chart response."""
    bars, r = completed_bars(chart, now_et)
    if len(bars) < 2:
        raise ValueError(f"only {len(bars)} completed bar(s)")
    (day, close, vol), (prev_day, prev_close, _) = bars[-1], bars[-2]
    rec = {"close": round(close, 4), "prevClose": round(prev_close, 4),
           "session": day, "prevSession": prev_day, "status": "fresh"}
    prior = [b[2] for b in bars[-21:-1] if b[2]]
    if prior and vol < VOLUME_FLOOR * statistics.mean(prior):
        rec.update(status="suspicious", statusReason="volume-anomaly")
    splits = (r.get("events") or {}).get("splits") or {}
    if splits:
        days = sorted(datetime.fromtimestamp(int(s.get("date", k)), ET).date().isoformat()
                      for k, s in splits.items())
        rec.update(status="suspicious", statusReason="split-in-window " + ",".join(days))
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--tickers", default=None, help="comma-separated subset")
    ap.add_argument("--fixtures", default=None)
    ap.add_argument("--now", default=None)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    now_et = datetime.fromisoformat(args.now).astimezone(ET) if args.now else datetime.now(ET)
    path = Path(args.data)
    data = json.loads(path.read_text(encoding="utf-8"))
    wanted = {s.strip().upper() for s in args.tickers.split(",")} if args.tickers else None
    if wanted:
        unknown = wanted - {t["ticker"] for t in data["tickers"]}
        if unknown:
            sys.exit(f"unknown ticker(s) in --tickers: {', '.join(sorted(unknown))} - nothing written")

    results = {}
    for t in data["tickers"]:
        tk = t["ticker"]
        if wanted and tk not in wanted:
            continue
        try:
            results[tk] = resolve_price(fetch_chart(t.get("yahooSymbol", tk), args.fixtures), now_et)
        except Exception as e:  # one ticker's failure must not stop the rest
            results[tk] = e

    sessions = sorted({r["session"] for r in results.values() if isinstance(r, dict)})
    if not sessions:
        sys.exit("no ticker produced a completed session - nothing written")
    # a --tickers subset must never roll the published session back (e.g.
    # refreshing only a halted ticker whose latest completed bar is older)
    target = max(sessions[-1], data.get("priceSession") or sessions[-1])

    counts, notes, big = Counter(), [], []
    for t in data["tickers"]:
        tk, r = t["ticker"], results.get(t["ticker"])
        if isinstance(r, Exception):
            reason = f"fetch-failed: {str(r)[:160]}"
            if t["price"].get("close"):
                new = dict(t["price"], status="stale", statusReason=reason)
            else:  # nothing usable to fall back on - a stale record needs a close
                new = {"close": None, "status": "unavailable", "statusReason": reason}
        elif isinstance(r, dict):
            new = r if r["session"] == target else dict(
                r, status="stale", statusReason=f"latest completed bar {r['session']}, target session {target}")
        else:
            new = t["price"]
            if new["status"] == "fresh" and new.get("session") != target:
                new = dict(new, status="stale", statusReason="not refreshed in this run")
        if new["status"] == "fresh" and abs(new["close"] / new["prevClose"] - 1) >= BIG_MOVE:
            big.append(f"{tk} {new['close'] / new['prevClose'] - 1:+.1%}")
        if new["status"] != "fresh" and tk in results:
            notes.append(f"{tk}: {new['status']} - {new.get('statusReason')}")
        t["price"] = new
        counts[new["status"]] += 1

    print(f"target session {target} (now {now_et:%Y-%m-%d %H:%M} ET) - {dict(counts)}")
    for n in notes:
        print(f"  {n}")
    if big:
        print(f"  big moves (check the news before trusting): {', '.join(big)}")
    if args.write:
        data["priceSession"] = target
        # a holiday repeats the same session: don't rewrite (and so don't
        # commit) a file whose only change would be its generatedAt stamp
        old = json.loads(path.read_text(encoding="utf-8"))
        if {k: v for k, v in old.items() if k != "generatedAt"} == {k: v for k, v in data.items() if k != "generatedAt"}:
            print(f"No change - {path.name} left as is")
            return
        data["generatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {path}")
    else:
        print("Dry run - pass --write to update stocks.json")


if __name__ == "__main__":
    main()
