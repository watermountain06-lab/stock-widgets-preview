#!/usr/bin/env python3
"""Stage 3: say when the prose measured the analyst upside it quotes.

Runs inside update_cards.py's per-card transaction, after the valuation tab, so anything
that fails here leaves the card untouched.

Why this exists. Since stage 2B-3 the band marker, its stat-box and the header pill
recompute the upside from today's close every night. The sentences around them do not:
they quote the number as it stood at the card's analysis date. 82 of the 84 audited
occurrences now disagree with the stat-box on their own card - CRWD's prose said
"+12.6%" while its own box read "-3.6%", the stock having passed its consensus target.

Why it stamps rather than recomputes. The percentage is one term in a Korean sentence
whose verb, marker and surrounding clause carry the claim ("+5.7%에 불과해 여력이 제한적",
a green bull bullet, "이미 소폭 넘어선 상태"). Moving only the number leaves the claim
behind, and a sign change can make the sentence assert the opposite of what it shows.
Two anchors whose direction actually flipped are rewritten as past-tense observations
with their marker neutralised; the rest are dated where they stand.

Anchors are audited, never rediscovered. site_data/prose_anchors.json pins each
occurrence by its exact original text and a hash of it. Offsets are deliberately not
recorded: 2A/2B-2/2B-3/2C rewrite these same files nightly, so any offset would be stale
by morning. The manifest was built from the pre-2B-3 snapshot by the selection that
produced the original 84 - a percentage regex cannot reproduce it, and must not be used
to try: several numbers that look identical to an upside are band positions.

Rendering is tri-state and fails closed:
  preimage present exactly once   -> apply it, count it
  postimage present exactly once  -> already applied, accept
  anything else                   -> RenderError, and the card is not written
A preimage matching more than once fails as well: the manifest promises exactly one, and
a second match means the sentence is no longer the one that was audited.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANCHORS = ROOT / "site_data" / "prose_anchors.json"

# The pilot. ANET (two bare stamps), ABBV (a stamp inside a parenthesis that already holds
# its source), AAPL (a caption whose stale 현재가 becomes a dated 종가), CRWD and CVX (the
# two whose direction flipped, each carrying a marker edit in the same anchor) cover all
# five shapes in the manifest. Set to None to render every card.
PROSE_TICKERS = {"ANET", "ABBV", "AAPL", "CRWD", "CVX"}

_cache = {}


class RenderError(Exception):
    """An anchor did not match as audited - the whole card is left untouched."""


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def load(path=ANCHORS):
    """The manifest, verified against its own hashes so a corrupted file cannot edit a card."""
    path = Path(path)
    key = str(path)
    if key in _cache:
        return _cache[key]
    if not path.exists():
        raise RenderError(f"anchor manifest missing: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("entries")
    if not entries:
        raise RenderError(f"anchor manifest lists no entries ({path})")
    for e in entries:
        if sha(e["preimage"]) != e["preSha"]:
            raise RenderError(f"{e['ticker']}: preimage hash does not match the manifest")
        if sha(e["postimage"]) != e["postSha"]:
            raise RenderError(f"{e['ticker']}: postimage hash does not match the manifest")
        if e["preimage"] == e["postimage"]:
            raise RenderError(f"{e['ticker']}: anchor would change nothing")
    by_ticker = {}
    for e in entries:
        by_ticker.setdefault(e["ticker"], []).append(e)
    _cache[key] = by_ticker
    return by_ticker


def render(html, ticker, notes, path=ANCHORS, tickers=None):
    """Apply every anchor recorded for this ticker. Returns (html, counts).

    counts["applied"] is what this run inserted and counts["already"] what a previous run
    did. Both are reported rather than only the first: a rerun that inserts nothing is the
    expected steady state, and observing zero insertions is not on its own evidence that
    the card is correct - each already-applied anchor is verified against its recorded
    postimage, not merely against the presence of a date.
    """
    gate = PROSE_TICKERS if tickers is None else tickers
    if gate is not None and ticker not in gate:
        return html, {"applied": 0, "already": 0, "gated": True}
    entries = load(path).get(ticker, [])
    if not entries:
        return html, {"applied": 0, "already": 0, "gated": False}

    applied = already = 0
    for e in entries:
        pre, post = e["preimage"], e["postimage"]
        n_pre, n_post = html.count(pre), html.count(post)
        if n_pre == 1 and n_post == 0:
            html = html.replace(pre, post, 1)
            applied += 1
        elif n_post == 1 and n_pre == 0:
            already += 1
        else:
            raise RenderError(
                f"{ticker} {e['disposition']}/{e.get('form')}: preimage x{n_pre}, postimage x{n_post} "
                f"(expected exactly one of them once) - {pre[:60]!r}")

    # Post-render assertion. Re-read the written card rather than trusting the edits above:
    # an exact-once replacement can still put the right text in the wrong card state.
    for e in entries:
        if html.count(e["postimage"]) != 1:
            raise RenderError(f"{ticker}: after rendering, postimage appears "
                              f"{html.count(e['postimage'])}x - {e['postimage'][:60]!r}")
        if html.count(e["preimage"]) != 0:
            raise RenderError(f"{ticker}: after rendering, the preimage is still present - "
                              f"{e['preimage'][:60]!r}")
    if applied:
        notes.append(f"prose: {applied} anchor(s) dated" + (f", {already} already" if already else ""))
    return html, {"applied": applied, "already": already, "gated": False}


def expected_counts(path=ANCHORS, tickers=None):
    """What a full run should touch, by disposition - for the fleet-level assertion."""
    gate = PROSE_TICKERS if tickers is None else tickers
    out = {}
    for t, entries in load(path).items():
        if gate is not None and t not in gate:
            continue
        for e in entries:
            out[e["disposition"]] = out.get(e["disposition"], 0) + 1
    return out
