#!/usr/bin/env python3
"""Post-publish health check for the daily workflow.

Exits 1 - so the run is marked failed and GitHub emails the owner - when the
data just committed is degraded. The data itself is still published with
honest status labels; this step only makes sure a person hears about it.

Fails when:
  - MAX_NOT_FRESH or more tickers are not fresh (stale/suspicious/unavailable),
    not counting a new ticker still waiting for its first home price (see below)
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

Warns without failing when a card reports no valuation baseline. That is the
expected state while a new ticker is being onboarded, so it must not fail the
run - but it must not pass with no trace either.

The same goes for a new ticker's empty home price: add_v2_ticker.py writes
"unavailable: 새 종목 ..." until a price run fills it, so the row is not fresh
while cardAsOf is still ahead of priceSession. Counting those as failures hit
2026-10-30: eight cards added in one evening put 8 rows in that state, the
not-fresh limit failed this check, and because test_pipeline.py runs it on a
copy of the live stocks.json, the refresh job that would have filled the prices
stopped before fetching them - the cards stayed empty and every later run broke
the same way. Once priceSession reaches cardAsOf an empty price is a real
problem again, so the exemption ends there.

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
from collections import Counter
from datetime import date, datetime, time as dtime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
MAX_NOT_FRESH = 6
MARKET_KEYS = ("sp500", "vix", "usdkrw")
# update_cards.py hold reasons that won't clear without rebuilding the card's history
NEEDS_PERSON = ("rebuild", "missing inside", "Yahoo doesn't")
# update_cards.py's note for a card with no valuation baseline yet - warn, never fail
NO_BASELINE = "no valuation baseline"
# add_v2_ticker.py's statusReason prefix for a new ticker's empty home price - warn while
# the price session hasn't reached the card's session yet (2026-10-30)
ONBOARDING_PRICE = "새 종목"
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


def iso_day(value):
    """YYYY-MM-DD면 그대로, 아니면 빈 문자열 — 날짜로 읽히지 않는 값이 비교를 통과하지 못하게 한다(Codex 2026-10-30)."""
    try:
        return date.fromisoformat(str(value)).isoformat()
    except (TypeError, ValueError):
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stocks", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--macro", default=str(ROOT / "site_data" / "macro.json"))
    ap.add_argument("--cards", default=None, help="card_status.json written by update_cards.py")
    ap.add_argument("--now", default=None, help="ISO timestamp standing in for the clock (tests)")
    args = ap.parse_args()

    now_et = datetime.fromisoformat(args.now).astimezone(ET) if args.now else datetime.now(ET)
    stocks = json.loads(Path(args.stocks).read_text(encoding="utf-8"))
    problems, warnings, wavg_standing = [], [], []

    stale, warn = session_age(stocks.get("priceSession"), now_et)
    if stale:
        problems.append(stale)
    if warn:
        warnings.append(warn)

    session = stocks.get("priceSession") or ""
    session_day = iso_day(session)   # 세션이 날짜로 읽히지 않으면 면제하지 않는다 — 그 경우는 session_age가 따로 잡는다(Codex r2)
    not_fresh, onboarding = [], []
    for t in stocks["tickers"]:
        price = t["price"]
        if price["status"] == "fresh":
            continue
        line = f"{t['ticker']} ({price['status']}: {price.get('statusReason', '')})"
        # 새 종목의 빈 홈 가격은 가격 실행이 카드 세션을 따라올 때까지의 정상 상태다. 따라온 뒤에도 비어 있으면 진짜 문제라
        # 그때부터 다시 센다 — 면제를 무기한 두면 못 채우는 종목이 조용히 묻힌다.
        if (price["status"] == "unavailable" and str(price.get("statusReason", "")).startswith(ONBOARDING_PRICE)
                and session_day and iso_day(t.get("cardAsOf")) > session_day):
            onboarding.append(line)
        else:
            not_fresh.append(line)
    if len(not_fresh) >= MAX_NOT_FRESH:
        problems.append(f"{len(not_fresh)} tickers not fresh (limit {MAX_NOT_FRESH - 1})")
    if onboarding:
        warnings.append(f"{len(onboarding)} new tickers waiting for their first home price")

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
                why = "; ".join(c.get("reasons", []))
                if NO_BASELINE in why:  # also on a card that updated cleanly otherwise
                    warnings.append(f"card {tk}: {why}")
                wa = c.get("weightedAverage")
                if wa:
                    # The standing set is counted below, not listed: nine cards repeating the same
                    # line every night is noise that gets tuned out. Only a card that changed class
                    # - started disagreeing, or changed why - is worth reading.
                    wavg_standing.append(f"{tk} {wa['class']}")
                    if wa.get("changed"):
                        detail = (f"states {wa['stated']}, its badges give {wa['now']}"
                                  if wa.get("now") is not None else "badge weights disagree with the baseline")
                        warnings.append(f"card {tk}: 가중평균 {wa['class']} - {detail}")
                if c["status"] == "v2":
                    # v2 카드는 이 실행 뒤 v2 재빌드가 갱신한다 — 지금은 하루 늦은 게 정상이다. 두 세션 넘게 늦으면
                    # v2 재빌드가 돌지 않았거나 그 카드가 계속 실패하는 것이다(Codex 2026-10-07).
                    own = next((t for t in stocks["tickers"] if t["ticker"] == tk), {}).get("price", {})
                    if c.get("lastBar") and own.get("prevSession") and c["lastBar"] < own["prevSession"]:
                        problems.append(f"card {tk}: v2 카드가 {c['lastBar']}에 멈춰 있다(가격 {own.get('session')}) — v2 재빌드 확인")
                    continue
                if c["status"] not in ("failed", "held"):
                    continue
                card_lines.append(f"{tk} {c['status']}: {why}")
                if c["status"] == "failed" or any(k in why for k in NEEDS_PERSON):
                    problems.append(f"card {tk} {c['status']}: {why}")

    print(f"priceSession {stocks.get('priceSession')}: "
          f"{len(stocks['tickers']) - len(not_fresh) - len(onboarding)} fresh, {len(not_fresh)} not fresh"
          + (f", {len(onboarding)} onboarding" if onboarding else ""))
    for line in not_fresh:
        print(f"  - {line}")
    for line in onboarding:
        print(f"  - (onboarding) {line}")
    if args.cards:
        print(f"cards: {len(card_lines)} held or failed")
        for line in card_lines:
            print(f"  - {line}")
        if wavg_standing:
            kinds = Counter(s.split()[-1] for s in wavg_standing)
            print(f"가중평균 disagreeing with their own badges: {len(wavg_standing)} "
                  f"({', '.join(f'{k} {n}' for k, n in sorted(kinds.items()))})")
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
