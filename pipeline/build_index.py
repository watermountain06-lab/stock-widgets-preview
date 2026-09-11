#!/usr/bin/env python3
"""Render site_data/stocks.json into index.html's inline DATA block.

Data stays inline (no fetch) so the page also works from file:// and the HTML
can never be served out of sync with its data. Only the text between the
/*STOCKS_DATA_START*/ and /*STOCKS_DATA_END*/ markers is rewritten, and only
when each marker appears exactly once. Derived values (change %, estimated
market cap) are computed here rather than stored in stocks.json.

Usage: python3 pipeline/build_index.py [--data PATH] [--index PATH] [--check]
  --check   write nothing; exit 1 if index.html is not up to date
"""
import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
START = "/*STOCKS_DATA_START*/"
END = "/*STOCKS_DATA_END*/"


def ui_row(t):
    """The slim per-ticker record the page's JS actually uses."""
    p = t["price"]
    close, prev = p.get("close"), p.get("prevClose")
    change = round((close / prev - 1) * 100, 2) if close and prev else None
    shares = t["shares"].get("usEquivalent")
    cap = round(close * shares) if close and shares else None
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
    }


def render_block(data):
    rows = sorted((ui_row(t) for t in data["tickers"]), key=lambda r: r["rank"])
    # "</" inside a <script> block would end it early; "<\/" is the same JSON string
    lines = [json.dumps(r, ensure_ascii=False, separators=(", ", ": ")).replace("</", "<\\/")
             for r in rows]
    return f"{START}\n  var DATA = [\n    " + ",\n    ".join(lines) + f"\n  ];\n  {END}"


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
    a = index_html.index(START)
    b = index_html.index(END)
    block = index_html[a:b]
    return json.loads(block[block.index("["): block.rindex("]") + 1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--index", default=str(ROOT / "index.html"))
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    index = Path(args.index)
    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    old = index.read_text(encoding="utf-8")
    new = splice(old, render_block(data))

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
