#!/usr/bin/env python3
"""Post-publish health check for the daily workflow.

Exits 1 - so the run is marked failed and GitHub emails the owner - when the
data just committed is degraded. The data itself is still published with
honest status labels; this step only makes sure a person hears about it.

Fails when:
  - MAX_NOT_FRESH or more tickers are not fresh (stale/suspicious/unavailable)
  - any market series in macro.json (sp500, vix, usdkrw) is not fresh
  - macro.json is missing, or its FOMC schedule has run out
  - with --cards: the card updater didn't reach the price session, or a card
    failed, or was held for something a person has to fix (a split, missing
    sessions - see NEEDS_PERSON). Holds that clear by themselves (a ticker's
    price not fresh, Yahoo late with the session) are only listed.
On a market holiday the previous session simply carries over as fresh, so a
holiday is not reported as a failure.

Usage: python3 pipeline/health_check.py [--stocks PATH] [--macro PATH] [--cards PATH]
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_NOT_FRESH = 6
MARKET_KEYS = ("sp500", "vix", "usdkrw")
# update_cards.py hold reasons that won't clear without rebuilding the card's history
NEEDS_PERSON = ("rebuild", "missing inside", "Yahoo doesn't")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stocks", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--macro", default=str(ROOT / "site_data" / "macro.json"))
    ap.add_argument("--cards", default=None, help="card_status.json written by update_cards.py")
    args = ap.parse_args()

    stocks = json.loads(Path(args.stocks).read_text(encoding="utf-8"))
    problems = []

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
    if problems:
        print("HEALTH CHECK FAILED:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("Health check OK")


if __name__ == "__main__":
    main()
