#!/usr/bin/env python3
"""One-time migration of index.html's hand-written DATA array into
site_data/stocks.json (schema v1).

The legacy array only carried display strings, so everything it did not
carry is seeded as explicitly provisional instead of guessed:
  - shares.usEquivalent is back-solved as legacy marketCap / price
    (basis "legacy-implied", status "unverified") and gets replaced from SEC
    filings in the share-seeding step;
  - price.prevClose is back-solved from the legacy change % so the migrated
    build reproduces the old screen exactly;
  - price.session is the card's own header date (the legacy prices were
    copied from each card), with status "stale" / statusReason "legacy-seed";
  - tier and score stay "missing" until the tier/score extraction step.

Refuses to overwrite an existing stocks.json unless --force.

Usage: python3 pipeline/seed_from_index.py [--index PATH] [--out PATH] [--force]
"""
import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# the legacy rows are hand-aligned with varying runs of spaces after commas
LEGACY_ROW_RE = re.compile(
    r"\{rank:(\d+),\s*ticker:'([^']+)',\s*name:'([^']+)',\s*sector:'([^']+)',\s*"
    r"price:'\$([\d,]+\.\d\d)',\s*change:(-?\d+(?:\.\d+)?),\s*"
    r"marketCap:'\$(\d+(?:\.\d+)?)([TB])',\s*href:'([^']+)'\}"
)
DATE_RE = re.compile(r"(20\d\d)[.-](\d\d)[.-](\d\d)")

LISTING = {
    "TSM": {"type": "adr", "adrRatio": 5},     # 1 ADR = 5 ordinary shares (20-F)
    "SKHY": {"type": "adr", "adrRatio": 0.1},  # 1 ADS = 1/10 common share (424B4, 2026-07-10)
    "ASML": {"type": "ny-registry", "adrRatio": 1},
}
MULTI_CLASS = {"BRKB", "MA", "V", "GOOGL", "META", "PLTR", "DELL", "SPCX"}
YAHOO_OVERRIDE = {"BRKB": "BRK-B"}


def parse_legacy_rows(index_html):
    """[(rank, ticker, name, sector, price, change, capNum, capUnit, href), ...]
    from the hand-written `var DATA = [...]` array. Exits rather than return
    a partial list if any row fails to parse."""
    m = re.search(r"var DATA = \[(.*?)\n\s*\];", index_html, re.S)
    if not m:
        sys.exit("legacy DATA array not found (already migrated?)")
    body = m.group(1)
    rows = LEGACY_ROW_RE.findall(body)
    n_objects = body.count("{rank:")
    if len(rows) != n_objects:
        sys.exit(f"parsed {len(rows)} of {n_objects} legacy rows - refusing a partial migration")
    return rows


def card_header_date(card_path):
    """The date printed next to the card's header price (price-main), i.e.
    the session the legacy index price was copied from."""
    s = card_path.read_text(encoding="utf-8")
    i = s.find('class="price-main"')
    if i < 0:
        sys.exit(f"{card_path.name}: no price-main header")
    m = DATE_RE.search(s, i, i + 2000)
    if not m:
        sys.exit(f"{card_path.name}: no date near the header price")
    return "-".join(m.groups())


def listing_for(ticker):
    if ticker in LISTING:
        return dict(LISTING[ticker])
    return {"type": "multi-class" if ticker in MULTI_CLASS else "common"}


def build_record(row):
    rank, ticker, name, sector, price, change, cap_num, cap_unit, href = row
    close = float(price.replace(",", ""))
    change = float(change)
    cap = float(cap_num) * (1e12 if cap_unit == "T" else 1e9)
    card_date = card_header_date(ROOT / href)

    rec = {"ticker": ticker}
    if ticker in YAHOO_OVERRIDE:
        rec["yahooSymbol"] = YAHOO_OVERRIDE[ticker]
    rec.update({
        "name": html.unescape(name),
        "sector": html.unescape(sector),
        "href": href,
        "cardRank": int(rank),
        "cardAsOf": card_date,
        "listing": listing_for(ticker),
        "price": {
            "close": close,
            "prevClose": round(close / (1 + change / 100), 6),
            "session": card_date,
            "status": "stale",
            "statusReason": "legacy-seed",
        },
        "shares": {
            "usEquivalent": round(cap / close),
            "method": "manual",
            "basis": "legacy-implied",
            "asOf": card_date,
            "filing": "legacy index.html marketCap / price",
            "approximate": True,
            "status": "unverified",
        },
        "tier": {"value": None, "raw": None, "status": "missing"},
        "score": {"status": "missing", "reason": "not-yet-extracted"},
    })
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", default=str(ROOT / "index.html"))
    ap.add_argument("--out", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    out = Path(args.out)
    if out.exists() and not args.force:
        sys.exit(f"{out} already exists - the seed is one-time; pass --force to redo it")

    rows = parse_legacy_rows(Path(args.index).read_text(encoding="utf-8"))
    data = {
        "schemaVersion": 1,
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "priceSession": None,
        "scoreVersion": "1.0.0",
        "tickers": [build_record(r) for r in rows],
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(rows)} tickers)")


if __name__ == "__main__":
    main()
