#!/usr/bin/env python3
"""Post-publish health check for the daily workflow.

Exits 1 - so the run is marked failed and GitHub emails the owner - when the
data just committed is degraded. The data itself is still published with
honest status labels; this step only makes sure a person hears about it.

Fails when:
  - MAX_NOT_FRESH or more tickers are not fresh (stale/suspicious/unavailable)
  - any market series in macro.json (sp500, vix, usdkrw) is not fresh
  - macro.json is missing, or its FOMC schedule has run out
  - priceSession is MAX_SESSION_LAG or more weekdays behind the session that
    should have settled by now (see below)
  - with --cards: the card updater didn't reach the price session, or a card
    failed, or was held for something a person has to fix (a split, missing
    sessions - see NEEDS_PERSON). Holds that clear by themselves (a ticker's
    price not fresh, Yahoo late with the session) are only listed.
On a market holiday the previous session simply carries over as fresh, so a
holiday is not reported as a failure.

The session-lag check exists because of 2026-09-14: Yahoo answered with a
well-formed chart whose newest bar was three days old, so every ticker stayed
"fresh" on that old session, nothing errored, and the run reported success.
Freshness only says a record matches what the source returned; this says the
source itself moved. No exchange calendar is kept (fetch_prices.py declined
one for the same reason), so one day of provider lag is indistinguishable
from a market holiday - hence one weekday behind warns, two or more fails.

Usage: python3 pipeline/health_check.py [--stocks PATH] [--macro PATH] [--cards PATH] [--now ISO]
"""
import argparse
import json
import os
import sys
from datetime import date, datetime, time as dtime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
MAX_NOT_FRESH = 6
MARKET_KEYS = ("sp500", "vix", "usdkrw")
# update_cards.py hold reasons that won't clear without rebuilding the card's history
NEEDS_PERSON = ("rebuild", "missing inside", "Yahoo doesn't")
ET = ZoneInfo("America/New_York")
SETTLE = dtime(16, 20)   # the cutoff fetch_prices.py uses to call a bar complete
MAX_SESSION_LAG = 2      # weekdays behind before a quiet provider counts as a failure


def expected_session(now_et):
    """The most recent weekday whose close has settled by now_et."""
    d = now_et.date()
    if now_et < datetime.combine(d, SETTLE, ET):
        d -= timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


def weekday_lag(session, expected):
    """Weekdays after `session` up to and including `expected`, so 0 means the
    data is current and 1 is the gap a single market holiday can account for."""
    n, d = 0, session
    while d < expected:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n += 1
    return n


def session_age(session, now_et):
    """(problem, warning) for how far behind priceSession is - at most one is set."""
    if not session:
        return "priceSession missing from stocks.json", None
    try:
        parsed = date.fromisoformat(session)
    except ValueError:
        return f"priceSession {session!r} is not a date", None
    expected = expected_session(now_et)
    if parsed > expected:
        return f"priceSession {session} is ahead of the settled session {expected}", None
    lag = weekday_lag(parsed, expected)
    note = (f"priceSession {session} is {lag} weekday(s) behind {expected} - "
            f"the provider may be serving stale data")
    if lag >= MAX_SESSION_LAG:
        return note, None
    if lag:
        return None, f"{note} (a market holiday looks the same)"
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stocks", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--macro", default=str(ROOT / "site_data" / "macro.json"))
    ap.add_argument("--cards", default=None, help="card_status.json written by update_cards.py")
    ap.add_argument("--now", default=None, help="ISO timestamp standing in for the clock (tests)")
    args = ap.parse_args()

    now_et = datetime.fromisoformat(args.now).astimezone(ET) if args.now else datetime.now(ET)
    stocks = json.loads(Path(args.stocks).read_text(encoding="utf-8"))
    problems, warnings = [], []

    stale, warn = session_age(stocks.get("priceSession"), now_et)
    if stale:
        problems.append(stale)
    if warn:
        warnings.append(warn)

    not_fresh = [f"{t['ticker']} ({t['price']['status']}: {t['price'].get('statusReason', '')})"
                 for t in stocks["tickers"] if t["price"]["status"] != "fresh"]
    if len(not_fresh) >= MAX_NOT_FRESH:
        problems.append(f"{len(not_fresh)} tickers not fresh (limit {MAX_NOT_FRESH - 1})")

    macro_path = Path(args.macro)
    if not macro_path.exists():
        problems.append("macro.json missing")
    else:
        macro = json.loads(macro_path.read_text(encoding="utf-8"))
        for key in MARKET_KEYS:
            ind = macro.get("indicators", {}).get(key, {})
            if ind.get("status") != "fresh":
                problems.append(f"macro {key} is {ind.get('status', 'missing')}: {ind.get('statusReason', '')}")
        if macro.get("nextFomc") is None:
            problems.append("FOMC schedule exhausted - add next year's dates to fetch_macro.py")

    card_lines = []
    if args.cards:
        cards_path = Path(args.cards)
        if not cards_path.exists():
            problems.append("card_status.json missing - the card updater didn't run")
        else:
            cs = json.loads(cards_path.read_text(encoding="utf-8"))
            if cs.get("priceSession") != stocks.get("priceSession"):
                problems.append(f"cards were last run for {cs.get('priceSession')}, "
                                f"prices are {stocks.get('priceSession')}")
            for tk, c in sorted(cs.get("cards", {}).items()):
                if c["status"] not in ("failed", "held"):
                    continue
                why = "; ".join(c.get("reasons", []))
                card_lines.append(f"{tk} {c['status']}: {why}")
                if c["status"] == "failed" or any(k in why for k in NEEDS_PERSON):
                    problems.append(f"card {tk} {c['status']}: {why}")

    print(f"priceSession {stocks.get('priceSession')}: {len(stocks['tickers']) - len(not_fresh)} fresh, "
          f"{len(not_fresh)} not fresh")
    for line in not_fresh:
        print(f"  - {line}")
    if args.cards:
        print(f"cards: {len(card_lines)} held or failed")
        for line in card_lines:
            print(f"  - {line}")
    for w in warnings:
        # an annotation on Actions, so a warning shows on the run page without an email
        print(f"::warning::{w}" if os.environ.get("GITHUB_ACTIONS") else f"WARNING: {w}")
    if problems:
        print("HEALTH CHECK FAILED:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("Health check OK")


if __name__ == "__main__":
    main()
