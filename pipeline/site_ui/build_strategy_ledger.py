#!/usr/bin/env python3
"""Write the day's fixed record for the Portfolio tab's strategy comparison (2026-10-19, preview only).

Design: pipeline/portfolio/STRATEGY_DESIGN.md section 2. The browser replays each strategy from these
records, so a record is written once per session and never rewritten (the workflow fails if an existing
file changes). Only public market data goes in - the universe is fixed and independent of anyone's
holdings: every ticker that was a card on any earlier record or is a card today, plus FIXED_ETFS.

When it writes session X (site_data/strategy_ledger/X.json):
  - stocks.json priceSession == v2/daily_status.json session == X, and daily_status has `finished`.
    Before v2 cards finish X's verdicts nothing is written (the next run tries again).
  - X.json doesn't exist yet. An existing record is never touched.
  - a failed run writes nothing ("no file" means "no data" for that session).
  - none of X's closes is a stand-in from Yahoo's meta (closeSource "yahoo-meta", 2026-10-20): such a
    session waits for served closes, usually from the morning refresh (not guaranteed - if none comes
    before the next session, X has no record).

Each record:
  session, generatedAt (file creation time - NOT the public time), prevPublishedAt (when the previous
  record first reached the public repo, from GitHub's push activity; the engine uses this as that
  record's public time), ruleVersion, cards {T: tier, tierStatus, close, verdictAsOf, priceStale},
  prices {T: close} for dropped cards and FIXED_ETFS, splits [{id, ticker, effectiveDate, ratio}] not on
  any earlier record with effectiveDate <= session, missing [T].

Card closes come from stocks.json (the site's own close for X). Dropped cards and ETFs come from
Yahoo's daily chart, which is also where every split comes from. Yahoo rewrites past closes after a split,
which is why a session's close has to be frozen on its own record.

Usage: python3 pipeline/site_ui/build_strategy_ledger.py [--fixtures DIR] [--now ISO] [--no-publish-lookup]
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "pipeline"))
import fetch_prices  # noqa: E402  (same Yahoo chart request, retries and completed-bar rule as the price job)

LEDGER = REPO / "site_data" / "strategy_ledger"
FIXED_ETFS = ["SPY", "RSP", "QQQ"]   # benchmarks; never extended from anyone's holdings
USABLE_TIER = {"valid", "normalized"}
OWNER_REPO = "watermountain06-lab/stock-widgets-preview"


def rule_version():
    src = (REPO / "pipeline" / "sync_v2_home.py").read_text(encoding="utf-8")
    return re.search(r'^RULE = "([^"]+)"', src, re.M).group(1)


def earlier_records():
    if not LEDGER.is_dir():
        return []
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(LEDGER.glob("[0-9]*.json"))]


def splits_from_chart(chart, ticker, session, seen):
    r = (chart.get("chart") or {}).get("result") or []
    out = []
    for k, s in ((r[0].get("events") or {}).get("splits") or {}).items() if r else []:
        day = datetime.fromtimestamp(int(s.get("date", k)), fetch_prices.ET).date().isoformat()
        sid = f"{ticker}:{day}"
        if day <= session and sid not in seen and s.get("denominator"):
            out.append({"id": sid, "ticker": ticker, "effectiveDate": day,
                        "ratio": round(s["numerator"] / s["denominator"], 6)})
    return out


class MetaClose(Exception):
    """The session's close came from Yahoo's meta, not a served bar (fetch_prices.fill_from_meta)."""


def close_on(chart, session, now_et):
    bars, r = fetch_prices.completed_bars(chart, now_et)
    if r.get("_metaFilled") == session:
        raise MetaClose(session)
    hit = [c for d, c, _v in bars if d == session]
    return round(hit[0], 4) if hit else None


def published_at(path, run=subprocess.run):
    """When the commit that added `path` first reached origin/main: the earliest push whose `after`
    contains it and whose `before` doesn't. None if it can't be told (the engine then treats that
    record as not yet public)."""
    rel = str(path.relative_to(REPO))
    added = run(["git", "log", "--diff-filter=A", "--format=%H", "--", rel], cwd=REPO,
                capture_output=True, text=True).stdout.split()
    if not added:
        return None
    sha = added[-1]
    res = run(["gh", "api", "--paginate", f"repos/{OWNER_REPO}/activity?activity_type=push&ref=main&per_page=100",
               "--jq", '.[] | [.timestamp, .before, .after] | @tsv'], capture_output=True, text=True)
    if res.returncode:
        return None
    pushes = [dict(zip(("timestamp", "before", "after"), line.split("\t")))
              for line in res.stdout.splitlines() if line.count("\t") == 2]

    def contains(tip):
        return run(["git", "merge-base", "--is-ancestor", sha, tip], cwd=REPO, capture_output=True).returncode == 0

    hits = [p["timestamp"] for p in pushes
            if contains(p["after"]) and not (p["before"].strip("0") and contains(p["before"]))]
    return min(hits) if hits else None


def build(now_et, fixtures=None, lookup_publish=True):
    stocks = json.loads((REPO / "site_data" / "stocks.json").read_text(encoding="utf-8"))
    status = json.loads((REPO / "v2" / "daily_status.json").read_text(encoding="utf-8"))
    session = stocks.get("priceSession")
    if status.get("session") != session or not status.get("finished"):
        return None, f"skip: verdicts for {session} not finished (daily_status {status.get('session')})"
    out = LEDGER / f"{session}.json"
    if out.exists():
        return None, f"skip: {out.name} already written"
    # A record is never rewritten, so it must not freeze a stand-in close: when Yahoo blanked the
    # day's bar and fetch_prices took meta's price instead (2026-10-20), wait for a later run to
    # bring the served close (usually the morning refresh, which triggers this workflow again).
    meta = [t["ticker"] for t in stocks["tickers"]
            if t["price"].get("session") == session and t["price"].get("closeSource") == "yahoo-meta"]
    if meta:
        return None, f"skip: {session} closes for {len(meta)} cards are meta-filled ({', '.join(meta[:5])}) - waiting for served closes"

    prior = earlier_records()
    seen_splits = {s["id"] for rec in prior for s in rec.get("splits", [])}
    ever_cards = {t for rec in prior for t in rec.get("cards", {})}
    symbol = {t: c["yahooSymbol"] for rec in prior for t, c in rec.get("cards", {}).items() if c.get("yahooSymbol")}
    failed_cards = {t for t, c in (status.get("cards") or {}).items() if c.get("status") != "ok"}

    cards, missing = {}, []
    for t in stocks["tickers"]:
        p, tier = t["price"], t["tier"]
        ok_price = p.get("session") == session and p.get("close") is not None
        cards[t["ticker"]] = {
            "tier": tier.get("value") if tier.get("status") in USABLE_TIER else None,
            "tierStatus": tier.get("status"),
            "close": p["close"] if ok_price else None,
            "verdictAsOf": t.get("cardAsOf"),
            "priceStale": (not ok_price) or p.get("status") != "fresh" or t["ticker"] in failed_cards,
        }
        if t.get("yahooSymbol"):   # e.g. BRKB -> BRK-B; kept so a dropped card can still be fetched
            cards[t["ticker"]]["yahooSymbol"] = symbol[t["ticker"]] = t["yahooSymbol"]
        if not ok_price:
            missing.append(t["ticker"])

    extra = sorted((ever_cards - set(cards)) | set(FIXED_ETFS))
    prices, splits = {}, []
    for t in sorted(set(cards) | set(extra)):
        try:
            chart = fetch_prices.fetch_chart(symbol.get(t, t), fixtures)
        except Exception as e:  # noqa: BLE001 - a ticker we can't fetch is recorded as missing
            if t in extra:
                missing.append(t)
            print(f"  {t}: chart failed ({e})", file=sys.stderr)
            continue
        splits += splits_from_chart(chart, t, session, seen_splits)
        if t in extra:
            try:
                c = close_on(chart, session, now_et)
            except MetaClose:
                return None, f"skip: {t} {session} close is meta-filled - waiting for a served close"
            if c is None:
                missing.append(t)
            else:
                prices[t] = c

    prev = sorted(LEDGER.glob("[0-9]*.json"))[-1] if prior else None
    rec = {
        "session": session,
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prevSession": prev.stem if prev else None,
        "prevPublishedAt": (published_at(prev) if lookup_publish else None) if prev else None,
        "ruleVersion": rule_version(),
        "scoreVersion": stocks.get("scoreVersion"),
        "pipelineFull": bool(status.get("full")) and not status.get("failed"),
        "cards": cards,
        "prices": prices,
        "splits": sorted(splits, key=lambda s: s["id"]),
        "missing": sorted(set(missing)),
    }
    LEDGER.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    index = sorted(p.stem for p in LEDGER.glob("[0-9]*.json"))
    (LEDGER / "index.json").write_text(json.dumps({"sessions": index}) + "\n", encoding="utf-8")
    return out, f"wrote {out.name}: {len(cards)} cards, {len(prices)} other prices, {len(rec['splits'])} splits, {len(rec['missing'])} missing"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", default=None)
    ap.add_argument("--now", default=None)
    ap.add_argument("--no-publish-lookup", action="store_true")
    a = ap.parse_args()
    now = datetime.fromisoformat(a.now) if a.now else datetime.now(fetch_prices.ET)
    _, msg = build(now.astimezone(fetch_prices.ET), a.fixtures, not a.no_publish_lookup)
    print(msg)


if __name__ == "__main__":
    main()
