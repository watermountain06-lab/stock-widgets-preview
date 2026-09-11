#!/usr/bin/env python3
"""Validate site_data/*.json against schema v1 and check index.html is in
sync with it. Exits 1 on any error; warnings (e.g. provisional legacy-seeded
share counts) are printed but don't fail the run.

With --baseline PATH (an index.html from before the pipeline existed, e.g.
`git show d958f8d:index.html > base.html`) it also runs the migration
regression: every legacy row must be reproduced by the generated DATA -
same order/rank/ticker/name/sector/href, identical price and change strings,
market cap equal within the legacy string's own precision.

Usage: python3 pipeline/validate_site_data.py [--baseline PATH]
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_index      # noqa: E402
import seed_from_index  # noqa: E402

TIERS = ["초저평가", "저평가", "적정~저평가", "적정", "고평가~적정", "고평가", "초고평가"]
LISTING_TYPES = {"common", "multi-class", "adr", "ny-registry"}
PRICE_STATUS = {"fresh", "stale", "suspicious", "unavailable"}
SHARES_METHOD = {"sec-dei", "sec-cover", "sec-note", "sec-annual-report", "prospectus", "manual"}
# legacy-implied is transitional: only the one-time seed writes it, and the
# share-seeding step must replace every occurrence (reported as a warning)
SHARES_BASIS = {"single", "sum-of-classes", "class-b-equivalent", "as-converted",
                "adr-equivalent", "ny-registry", "legacy-implied"}
SHARES_STATUS = {"ok", "stale", "unverified"}
TIER_STATUS = {"valid", "normalized", "missing", "conflict"}
SCORE_STATUS = {"available", "missing", "excluded"}
HISTORY_DECISIONS = {"seeded", "changed", "held-hysteresis", "held-divergence"}
MARKET_MACRO_KEYS = {"sp500", "vix", "usdkrw"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)


def fmt_price(x):
    return f"${x:,.2f}"


def fmt_cap(x):
    return f"${x / 1e12:.2f}T" if x >= 1e12 else f"${x / 1e9:.1f}B"


def is_date(v):
    return isinstance(v, str) and bool(DATE_RE.match(v))


def check_ticker(t, top, r):
    tk = t.get("ticker", "?")
    for key in ("ticker", "name", "sector", "href"):
        v = t.get(key)
        if not isinstance(v, str) or not v:
            r.err(f"{tk}: {key} missing")
        elif any(c in v for c in "<>&"):
            r.err(f"{tk}: {key} contains an HTML-special character: {v!r}")
    if t.get("href") != f"{tk}_full_widget.html":
        r.err(f"{tk}: href {t.get('href')!r} != {tk}_full_widget.html")
    if not is_date(t.get("cardAsOf")):
        r.err(f"{tk}: cardAsOf not an ISO date")

    lst = t.get("listing", {})
    if lst.get("type") not in LISTING_TYPES:
        r.err(f"{tk}: listing.type {lst.get('type')!r}")
    if lst.get("type") in ("adr", "ny-registry") and not (lst.get("adrRatio") or 0) > 0:
        r.err(f"{tk}: {lst.get('type')} needs a positive adrRatio")

    p = t.get("price", {})
    st = p.get("status")
    if st not in PRICE_STATUS:
        r.err(f"{tk}: price.status {st!r}")
    if st != "fresh" and not p.get("statusReason"):
        r.err(f"{tk}: price.status {st} needs a statusReason")
    if st == "unavailable":
        if p.get("close") is not None:
            r.err(f"{tk}: unavailable price must have close null")
    elif not (isinstance(p.get("close"), (int, float)) and p["close"] > 0):
        r.err(f"{tk}: price.close must be positive")
    if st == "fresh":
        if not (isinstance(p.get("prevClose"), (int, float)) and p["prevClose"] > 0):
            r.err(f"{tk}: fresh price needs a positive prevClose")
        if not (is_date(p.get("session")) and is_date(p.get("prevSession"))
                and p["prevSession"] < p["session"]):
            r.err(f"{tk}: fresh price needs prevSession < session")
        if p.get("session") != top.get("priceSession"):
            r.err(f"{tk}: fresh price session {p.get('session')} != priceSession {top.get('priceSession')}")
    elif not is_date(p.get("session")) and st != "unavailable":
        r.err(f"{tk}: price.session not an ISO date")

    s = t.get("shares", {})
    if not (isinstance(s.get("usEquivalent"), int) and s["usEquivalent"] > 0):
        r.err(f"{tk}: shares.usEquivalent must be a positive integer")
    if s.get("method") not in SHARES_METHOD:
        r.err(f"{tk}: shares.method {s.get('method')!r}")
    if s.get("basis") not in SHARES_BASIS:
        r.err(f"{tk}: shares.basis {s.get('basis')!r}")
    if s.get("basis") == "adr-equivalent" and lst.get("type") != "adr":
        r.err(f"{tk}: adr-equivalent shares on a non-ADR listing")
    if s.get("status") not in SHARES_STATUS:
        r.err(f"{tk}: shares.status {s.get('status')!r}")
    if s.get("basis") == "legacy-implied" or s.get("status") == "unverified":
        r.warn(f"{tk}: provisional share count ({s.get('basis')}, {s.get('status')})")
    elif s.get("status") == "stale":
        r.warn(f"{tk}: stale share count as of {s.get('asOf')} ({s.get('note', 'no note')})")
    if not is_date(s.get("asOf")):
        r.err(f"{tk}: shares.asOf not an ISO date")
    if s.get("filedAt") is not None and not is_date(s["filedAt"]):
        r.err(f"{tk}: shares.filedAt not an ISO date")
    if "classes" in s:
        cls = s["classes"]
        well_formed = isinstance(cls, list) and cls and all(
            isinstance(c, dict) and isinstance(c.get("class"), str) and c["class"].strip()
            and isinstance(c.get("shares"), int)
            and isinstance(c.get("factor"), (int, float)) for c in cls)
        if not well_formed:
            r.err(f"{tk}: shares.classes must be a non-empty list of {{class, shares:int, factor:number}}")
        else:
            total = sum(c["shares"] * c["factor"] for c in cls)
            if total != s.get("usEquivalent"):
                r.err(f"{tk}: shares.classes sum {total:,} != usEquivalent {s.get('usEquivalent')}")

    tier = t.get("tier", {})
    ts = tier.get("status")
    if ts not in TIER_STATUS:
        r.err(f"{tk}: tier.status {ts!r}")
    elif ts == "missing":
        if tier.get("value") is not None:
            r.err(f"{tk}: missing tier must have value null")
    elif tier.get("value") not in TIERS:
        r.err(f"{tk}: tier.value {tier.get('value')!r} not in the 7-tier enum")

    sc = t.get("score", {})
    ss = sc.get("status")
    if ss not in SCORE_STATUS:
        r.err(f"{tk}: score.status {ss!r}")
    elif ss == "available":
        if not isinstance(sc.get("total"), (int, float)):
            r.err(f"{tk}: available score needs a numeric total")
        for k in ("financialsAsOf", "valuationAsOf"):
            if not is_date(sc.get(k)):
                r.err(f"{tk}: available score needs {k}")
    elif not sc.get("reason"):
        r.err(f"{tk}: {ss} score needs a reason")
    if "scoreVersion" in sc and sc["scoreVersion"] != top.get("scoreVersion"):
        r.err(f"{tk}: score.scoreVersion {sc['scoreVersion']} != top-level {top.get('scoreVersion')}")


def check_stocks(data, r):
    if data.get("schemaVersion") != 1:
        r.err(f"schemaVersion {data.get('schemaVersion')!r} != 1")
    if data.get("priceSession") is not None and not is_date(data["priceSession"]):
        r.err("priceSession not an ISO date")
    tickers = data.get("tickers", [])
    for t in tickers:
        check_ticker(t, data, r)

    for key in ("ticker", "cardRank", "href"):
        vals = [t.get(key) for t in tickers]
        dups = {v for v in vals if vals.count(v) > 1}
        if dups:
            r.err(f"duplicate {key}: {sorted(map(str, dups))}")
    ranks = sorted(t.get("cardRank") for t in tickers if isinstance(t.get("cardRank"), int))
    if ranks != list(range(1, len(tickers) + 1)):
        r.err("cardRank must run 1..N with no gaps")

    cards = {p.name for p in ROOT.glob("*_full_widget.html")}
    hrefs = {t.get("href") for t in tickers}
    if cards != hrefs:
        r.err(f"card files vs tickers mismatch: only cards {sorted(cards - hrefs)}, "
              f"only data {sorted(hrefs - cards)}")


def check_tier_history(path, r):
    if not path.exists():
        return
    entries = json.loads(path.read_text(encoding="utf-8"))
    seen = set()
    for e in entries:
        key = (e.get("ticker"), e.get("evaluatedAt"), e.get("ruleVersion"))
        if key in seen:
            r.err(f"tier_history: duplicate entry {key}")
        seen.add(key)
        if e.get("decision") not in HISTORY_DECISIONS:
            r.err(f"tier_history: {key} decision {e.get('decision')!r}")
        if e.get("publishedTier") is not None and e["publishedTier"] not in TIERS:
            r.err(f"tier_history: {key} publishedTier {e['publishedTier']!r}")


def check_macro(path, price_session, r):
    if not path.exists():
        return
    macro = json.loads(path.read_text(encoding="utf-8"))
    for key, ind in macro.get("indicators", {}).items():
        st = ind.get("status")
        if st not in PRICE_STATUS:
            r.err(f"macro.{key}: status {st!r}")
        if st != "fresh" and not ind.get("statusReason"):
            r.err(f"macro.{key}: status {st} needs a statusReason")
        # a market series must come from the same session as the stock prices -
        # never a substituted previous bar or an in-progress intraday bar
        if st == "fresh" and key in MARKET_MACRO_KEYS and ind.get("asOf") != price_session:
            r.err(f"macro.{key}: fresh asOf {ind.get('asOf')} != priceSession {price_session}")


def check_index_sync(data, index_html, r):
    for marker in (build_index.START, build_index.END):
        n = index_html.count(marker)
        if n != 1:
            r.err(f"index.html has {n} {marker} markers (need exactly 1)")
            return
    if build_index.splice(index_html, build_index.render_block(data)) != index_html:
        r.err("index.html is stale - run pipeline/build_index.py")


def check_regression(baseline_html, index_html, r):
    legacy = seed_from_index.parse_legacy_rows(baseline_html)
    rows = build_index.parse_inline_rows(index_html)
    if len(legacy) != len(rows):
        r.err(f"regression: {len(legacy)} legacy rows vs {len(rows)} generated")
        return
    normalized = []
    for old, new in zip(legacy, rows):
        rank, ticker, name, sector, price, change, cap_num, cap_unit, href = old
        tk = new["ticker"]
        if (int(rank), ticker, href) != (new["rank"], tk, new["href"]):
            r.err(f"regression: row order/identity changed at legacy rank {rank} ({ticker} -> {tk})")
            continue
        if html.unescape(name) != new["name"] or html.unescape(sector) != new["sector"]:
            r.err(f"regression: {tk} name/sector text changed")
        if fmt_price(new["price"]) != f"${price}":
            r.err(f"regression: {tk} price ${price} -> {fmt_price(new['price'])}")
        if f"{new['change']:.2f}" != f"{float(change):.2f}":
            r.err(f"regression: {tk} change {change} -> {new['change']}")
        unit = 1e12 if cap_unit == "T" else 1e9
        decimals = len(cap_num.split(".")[1]) if "." in cap_num else 0
        legacy_cap = float(cap_num) * unit
        if abs(new["marketCap"] - legacy_cap) > 0.5 * 10 ** -decimals * unit:
            r.err(f"regression: {tk} market cap ${cap_num}{cap_unit} -> {fmt_cap(new['marketCap'])}")
        elif fmt_cap(new["marketCap"]) != f"${cap_num}{cap_unit}":
            normalized.append(f"{tk} ${cap_num}{cap_unit} -> {fmt_cap(new['marketCap'])}")
    if normalized:
        print("regression: market-cap strings normalized (same value, uniform decimals): "
              + "; ".join(normalized))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", default=None, help="pre-pipeline index.html for the migration regression")
    args = ap.parse_args()

    r = Report()
    data = json.loads((ROOT / "site_data" / "stocks.json").read_text(encoding="utf-8"))
    index_html = (ROOT / "index.html").read_text(encoding="utf-8")

    check_stocks(data, r)
    check_tier_history(ROOT / "site_data" / "tier_history.json", r)
    check_macro(ROOT / "site_data" / "macro.json", data.get("priceSession"), r)
    check_index_sync(data, index_html, r)
    if args.baseline:
        check_regression(Path(args.baseline).read_text(encoding="utf-8"), index_html, r)

    if r.warnings:
        print(f"{len(r.warnings)} warning(s):")
        for w in r.warnings[:10]:
            print(f"  - {w}")
        if len(r.warnings) > 10:
            print(f"  ... and {len(r.warnings) - 10} more")
    if r.errors:
        print(f"{len(r.errors)} error(s):")
        for e in r.errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"OK - {len(data['tickers'])} tickers valid")


if __name__ == "__main__":
    main()
