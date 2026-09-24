#!/usr/bin/env python3
"""Daily bars a person recorded because the provider cannot supply them.

Why this exists. On 2026-09-22 Yahoo served UNH, GS and DIS with a high below their own
open, so update_cards held those three cards - an impossible bar is a provider glitch, not
a card problem. Overnight Yahoo nulled that session for 41 tickers and had not restored it
three days later, so the cards advanced from 09-21 to 09-23 with a hole in the middle and
their moving averages spanned it. Every other ticker kept the bar it had already written.

Why a manifest rather than a fetch. The bar is still recoverable - Yahoo's own 1h and 5m
endpoints serve that session, and an independent vendor lists it - but reading it at run
time would mean the pipeline deciding, unattended, which vendor to believe about a close
and a volume that differ between them. A recorded bar is auditable instead: each entry
names where every field came from and why the ones that disagreed were resolved the way
they were. Nothing here is computed, inferred or averaged.

How it is used. update_cards.py folds these bars into what the fetch returned, so a bar the
card is missing is inserted at its place in the history rather than holding the card for
ever. The bar is then subject to every check a fetched bar is subject to: strictly
increasing dates, sane OHLC, DAILY/MA lengths equal, and the moving averages from the
insertion point on are recomputed rather than patched.

The manifest is a floor, not a licence: a session missing from BOTH the card and the fetch
and absent from here still holds the card, which is what should happen when nobody has
checked what the right numbers are.
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "site_data" / "backfill_bars.json"

# the same tolerance update_cards.py allows a fetched bar, so a bar cannot pass here and
# then fail the card's own check
TOL = 0.011

_cache = {}


class BackfillError(Exception):
    """The manifest does not describe a usable bar - nothing is inserted anywhere."""


def load(path=MANIFEST):
    """{ticker: {session: (o, h, l, c, v)}}, or {} when there is nothing recorded."""
    path = Path(path)
    key = str(path)
    if key in _cache:
        return _cache[key]
    if not path.exists():
        _cache[key] = {}
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for e in data.get("bars") or []:
        tk, session = e.get("ticker"), e.get("session")
        if not tk or not session:
            raise BackfillError("a bar with no ticker or no session")
        where = f"{tk} {session}"
        try:
            d = date.fromisoformat(session)
        except ValueError as exc:
            raise BackfillError(f"{where}: session is not an ISO date") from exc
        if d.weekday() >= 5:
            raise BackfillError(f"{where}: that is a weekend, not a trading session")
        if not (e.get("source") or "").strip():
            raise BackfillError(f"{where}: no source - a recorded bar has to say where it came from")
        try:
            o, h, l, c = (float(e[k]) for k in ("open", "high", "low", "close"))
            v = int(e["volume"])
        except (KeyError, TypeError, ValueError) as exc:
            raise BackfillError(f"{where}: open/high/low/close/volume missing or not a number") from exc
        # exactly the check update_cards.py runs on every bar it writes
        if min(o, h, l, c) <= 0 or v < 0 or h + TOL < max(o, c) or l - TOL > min(o, c) or h + TOL < l:
            raise BackfillError(f"{where}: not a consistent bar - o{o} h{h} l{l} c{c} v{v}")
        if session in out.get(tk, {}):
            raise BackfillError(f"{where}: recorded twice")
        out.setdefault(tk, {})[session] = (session, o, h, l, c, v)
    _cache[key] = out
    return out


def sessions(ticker, path=MANIFEST):
    """The sessions recorded for this ticker - what update_cards may insert rather than hold on."""
    return set(load(path).get(ticker, {}))


def merge(fetched, ticker, notes, path=MANIFEST):
    """`fetched` with any recorded bar the provider did not return folded in, oldest first.

    Only within the fetched window: a bar older than the window has nothing to do with this
    run, and one newer than the window would let the manifest push the card past the session
    the homepage published. A bar the provider DID return is left alone - the provider is the
    source of truth whenever it has an answer, and this file only fills silence.
    """
    recorded = load(path).get(ticker, {})
    if not recorded or not fetched:
        return fetched, []
    have = {b[0] for b in fetched}
    lo, hi = fetched[0][0], fetched[-1][0]
    added = [b for s, b in sorted(recorded.items()) if s not in have and lo <= s <= hi]
    if not added:
        return fetched, []
    out = sorted(fetched + added, key=lambda b: b[0])
    notes.append(f"recorded bar(s) the provider cannot supply: {', '.join(b[0] for b in added)}")
    return out, [b[0] for b in added]
