"""One-off/occasional backfill of USD/KRW for the Portfolio tab's Korean account (2026-10-28).

Writes site_data/fx_history.json: {"version": N, "src": "yahoo-1d-prev", "rates": {"YYYY-MM-DD": rate}} for every
weekday from --since to today, using the same rule as the daily ledger (build_strategy_ledger.fx_for: the last
KRW=X daily bar completed before that date). The ledger's own fx value wins when both exist (the page reads both).
Public market data only. A new run bumps "version"; earlier values are not edited in place by anything else.
"""
import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import fetch_prices  # noqa: E402
from build_strategy_ledger import fx_for, REPO  # noqa: E402

OUT = REPO / "site_data" / "fx_history.json"


def build(since, until, chart):
    rates, d = {}, date.fromisoformat(since)
    while d <= until:
        if d.weekday() < 5:
            fx = fx_for(d.isoformat(), chart)
            if fx:
                rates[d.isoformat()] = fx["USDKRW"]
        d += timedelta(days=1)
    return rates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="2026-09-30")
    a = ap.parse_args()
    chart = fetch_prices.fetch_chart("KRW=X", None)
    old = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
    rates = build(a.since, date.today(), chart)
    OUT.write_text(json.dumps({"version": int(old.get("version", 0)) + 1, "src": "yahoo-1d-prev", "rates": rates},
                              sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name}: {len(rates)} dates")


if __name__ == "__main__":
    main()
