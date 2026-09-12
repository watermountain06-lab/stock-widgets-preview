#!/usr/bin/env python3
"""Render site_data/stocks.json (and macro.json) into index.html's inline block.

Data stays inline (no fetch) so the page also works from file:// and the HTML
can never be served out of sync with its data. Only the text between the
/*STOCKS_DATA_START*/ and /*STOCKS_DATA_END*/ markers is rewritten, and only
when each marker appears exactly once. Derived values (change %, estimated
market cap) are computed here rather than stored in stocks.json.

The block holds three globals: DATA (one slim row per ticker, what the page's
JS renders), META (the as-of dates shown next to the list, so the page never
implies one date for values that come from different dates) and MACRO (the
macro.json indicators, or null before the first macro run).

Usage: python3 pipeline/build_index.py [--data PATH] [--macro PATH] [--index PATH] [--check]
  --check   write nothing; exit 1 if index.html is not up to date
"""
import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MACRO_PATH = ROOT / "site_data" / "macro.json"
SCORE_CONFIG = Path.home() / "Workspace/stock-widgets-redesign/scripts/fundamental_score_config_v1.json"
try:
    COMPARABILITY_FLAGS = set(json.loads(SCORE_CONFIG.read_text(encoding="utf-8"))
                              .get("comparability_flags", {}).get("flags", []))
except OSError:
    COMPARABILITY_FLAGS = set()

START = "/*STOCKS_DATA_START*/"
END = "/*STOCKS_DATA_END*/"


def ui_row(t):
    """The slim per-ticker record the page's JS actually uses."""
    p = t["price"]
    close, prev = p.get("close"), p.get("prevClose")
    change = round((close / prev - 1) * 100, 2) if close and prev else None
    shares = t["shares"].get("usEquivalent")
    cap = round(close * shares) if close and shares else None
    score = t["score"]
    return {
        "rank": t["cardRank"],
        "ticker": t["ticker"],
        "name": t["name"],
        "sector": t["sector"],
        "price": close,
        "change": change,
        "marketCap": cap,
        "href": t["href"],
        "priceStale": p["status"] != "fresh",
        "tier": t["tier"]["value"],
        "tierConflict": t["tier"]["status"] == "conflict",
        "score": score.get("total") if score["status"] == "available" else None,
        # v1.0.1 - flags that make a score non-comparable with the rest of its
        # tier group. The page groups these separately rather than listing them
        # in the same ordering: a badge alone still reads as a like-for-like
        # rank. Empty list when the score is fully comparable.
        "scoreFlags": [f for f in (score.get("qualityFlags") or []) if f in COMPARABILITY_FLAGS],
    }


def meta(data):
    """As-of dates for the page's date line - one per source, never merged."""
    card_dates = sorted(t["cardAsOf"] for t in data["tickers"])
    valuation_dates = sorted(t["score"]["valuationAsOf"] for t in data["tickers"]
                             if t["score"]["status"] == "available")
    return {
        "priceSession": data.get("priceSession"),
        # None bounds for an empty dataset - the page has its own empty state
        "cardAsOfMin": card_dates[0] if card_dates else None,
        "cardAsOfMax": card_dates[-1] if card_dates else None,
        # both bounds, so scores priced off different dates are shown as a range
        "scoreValuationAsOfMin": valuation_dates[0] if valuation_dates else None,
        "scoreValuationAsOfMax": valuation_dates[-1] if valuation_dates else None,
        "scoreVersion": data.get("scoreVersion"),
    }


def load_macro(path=MACRO_PATH):
    path = Path(path)
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def _js(obj):
    # "</" inside a <script> block would end it early; "<\/" is the same JSON string
    return json.dumps(obj, ensure_ascii=False, separators=(", ", ": ")).replace("</", "<\\/")


def render_block(data, macro=None):
    rows = sorted((ui_row(t) for t in data["tickers"]), key=lambda r: r["rank"])
    return (f"{START}\n  var DATA = [\n    " + ",\n    ".join(_js(r) for r in rows)
            + f"\n  ];\n  var META = {_js(meta(data))};\n  var MACRO = {_js(macro)};\n  {END}")


def splice(index_html, block):
    if index_html.count(START) != 1 or index_html.count(END) != 1:
        raise ValueError(f"expected exactly one {START} and one {END} in index.html")
    a = index_html.index(START)
    b = index_html.index(END) + len(END)
    if b <= a:
        raise ValueError("DATA markers are out of order")
    return index_html[:a] + block + index_html[b:]


def parse_inline_rows(index_html):
    """Inverse of render_block, for validation: the DATA rows currently inlined."""
    block = index_html[index_html.index(START): index_html.index(END)]
    s = block.index("var DATA = [") + len("var DATA = ")
    e = block.index("\n  ];", s) + len("\n  ]")
    return json.loads(block[s:e])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--macro", default=str(MACRO_PATH))
    ap.add_argument("--index", default=str(ROOT / "index.html"))
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    index = Path(args.index)
    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    old = index.read_text(encoding="utf-8")
    new = splice(old, render_block(data, load_macro(args.macro)))

    if args.check:
        if new != old:
            print("index.html is stale - run pipeline/build_index.py")
            sys.exit(1)
        print("index.html is up to date")
        return
    if new == old:
        print("index.html already up to date")
        return

    # write-then-rename so a crash can never leave a half-written index.html
    fd, tmp = tempfile.mkstemp(dir=index.parent, prefix=".index.", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(new)
    os.chmod(tmp, 0o644)
    os.replace(tmp, index)
    print(f"Wrote {index} ({len(data['tickers'])} tickers)")


if __name__ == "__main__":
    main()
