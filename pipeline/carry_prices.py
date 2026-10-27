#!/usr/bin/env python3
"""Carry this run's prices onto a newer main after the refresh's push was rejected.

The refresh commits, then pushes. If a person pushed in between (2026-10-21: a new MSI card at
21:34 ET while the refresh sat out Yahoo's blank close), the two commits edit different lines of
the same files and the rebase conflicts. The workflow then resets to the new main and rebuilds on
top of it. It does not fetch again: a second fetch can land in the blank-close window or see a
withdrawn bar, and a session already read cleanly would be thrown away (Codex, review 2026-10-21).

carry: each ticker this run priced gets this run's price block back, unless the other commit
changed that ticker's price block or yahooSymbol against the commit this run started from: those
are fetched again rather than overwritten with what this run read for the old row (Opus review
2026-10-21), and the person's block stays only if that fetch brings nothing for this session.
They, and tickers the other commit added, are printed for the caller to fetch into a scratch copy. Fails, writing nothing, if the newer main
already carries a later session than this run read.

merge: takes the fetched blocks for those tickers back from the scratch copy, only when they are
for this run's session. A ticker that fetched another session, or nothing, keeps main's block, so
one new ticker can neither stop the session from landing nor move it (Codex/Opus round 2).

Usage: python3 pipeline/carry_prices.py carry SAVED BASE [--data site_data/stocks.json]
       python3 pipeline/carry_prices.py merge FETCHED TICKERS [--data site_data/stocks.json]
carry prints the tickers to fetch, comma-separated (empty line when none).
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def carry(saved, base, data):
    """Copy saved price blocks into data in place; return the tickers to fetch instead."""
    if (data.get("priceSession") or "") > saved["priceSession"]:
        raise SystemExit(f"main already holds session {data['priceSession']}, this run read "
                         f"{saved['priceSession']} - nothing written")
    ours = {t["ticker"]: t["price"] for t in saved["tickers"]}
    before = {t["ticker"]: t for t in base["tickers"]}
    fetch = []
    for t in data["tickers"]:
        b = before.get(t["ticker"])
        if (t["ticker"] in ours and b is not None and t["price"] == b["price"]
                and t.get("yahooSymbol") == b.get("yahooSymbol")):
            t["price"] = ours[t["ticker"]]
        else:
            fetch.append(t["ticker"])
    data["priceSession"] = saved["priceSession"]
    data["generatedAt"] = saved.get("generatedAt", data.get("generatedAt"))
    return fetch


def merge(fetched, tickers, data):
    """Take fetched blocks for `tickers` that are for data's session; return the ones left out."""
    got = {t["ticker"]: t["price"] for t in fetched["tickers"]}
    left = []
    for t in data["tickers"]:
        if t["ticker"] not in tickers:
            continue
        p = got.get(t["ticker"])
        if p and p.get("session") == data["priceSession"] and p.get("close") is not None:
            if p.get("status") == "stale" and str(p.get("statusReason", "")).startswith("latest completed bar"):
                # stale only because another fetched ticker ran ahead to a later target (Codex round 3)
                p = {k: v for k, v in p.items() if k != "statusReason"} | {"status": "fresh"}
            t["price"] = p
        else:
            left.append(t["ticker"])
            if t["price"].get("status") == "fresh" and t["price"].get("session") != data["priceSession"]:
                # as fetch_prices does for a ticker it could not refresh (validate: fresh == priceSession)
                t["price"] = dict(t["price"], status="stale", statusReason="not refreshed after the push retry")
    return left


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["carry", "merge"])
    ap.add_argument("first")
    ap.add_argument("second")
    ap.add_argument("--data", default=str(ROOT / "site_data" / "stocks.json"))
    a = ap.parse_args()
    path = Path(a.data)
    data = json.loads(path.read_text(encoding="utf-8"))
    first = json.loads(Path(a.first).read_text(encoding="utf-8"))
    if a.mode == "carry":
        fetch = carry(first, json.loads(Path(a.second).read_text(encoding="utf-8")), data)
        print(f"carried {len(data['tickers']) - len(fetch)} price blocks; to fetch: "
              f"{', '.join(fetch) or 'none'}", file=sys.stderr)
        print(",".join(fetch))
    else:
        tickers = {s for s in a.second.split(",") if s}
        left = merge(first, tickers, data)
        if left:
            print(f"::warning::no {data['priceSession']} price for {', '.join(left)} - main's block kept")
        print(f"merged {len(tickers) - len(left)} fetched price blocks", file=sys.stderr)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
