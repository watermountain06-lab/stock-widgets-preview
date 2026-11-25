#!/usr/bin/env python3
"""Daily stock bars from Polygon (Massive), kept as a committed per-session cache.

Why (2026-11-25): Yahoo served the evening's bar before it had settled - 27 card failures in
11-17..20 were bars whose open or close lay outside their own high-low range (AVY 11-19: o186.28
h185.77), all from runs 30-55 min after the close (daily/2026-11-24), and it never served SNDK's
bars after its 8:1 split on 11-20. Polygon's grouped daily gives every US ticker for one session
in one call and had no such bar across 2,020 bars (404 tickers x 11-18..24); its close matched the
homepage for all 403 comparable tickers.

The free plan allows 5 calls a minute and refuses a session until it has ended ("Attempted to
request today's data before end of day" - NotYet). So one grouped call per session is cached here
as site_data/polygon_daily/{DATE}.json, holding only this site's tickers:
    {"session", "status", "fetchedAt", "updatedAt", "count", "rebased": {SYMBOL: DATE},
     "nullChecked": [SYMBOL], "bars": {SYMBOL: [o, h, l, c, v] | null}}
A null means Polygon had no bar for that ticker that session (a halt; every ticker on a holiday -
Polygon answers a holiday with status OK and no results, measured on 2026-09-07). A ticker MISSING
from a file was not in the universe when the file was fetched; its history is filled with one
per-ticker call (backfill_ticker). A file whose status is not "OK" (the latest session is still
"DELAYED" the next night, and its ticker count grew 12,630 -> 12,650 meanwhile) is fetched again on
later runs until it is OK. Only sync() fetches; chart() reads the cache and raises on a gap, so
every reader that runs without a key (the v2 card workflow) or after sync sees what was committed.

Split basis. adjusted=true prices are split-adjusted as of when they are fetched (measured: SNDK's
11-18 bar fetched on 11-25 was on the post-11-20 basis; UNVERIFIED: whether a fetch on the
execution date itself, before the open, is already re-based). Each file therefore carries, per
ticker, the date its bars are on: rebased[SYMBOL] if a later call rewrote them, else the ET date of
fetchedAt. A listed split after that date and not after the newest cached session leaves those
bars one ratio off; sync() re-fetches the ticker's history in one call, checks that Polygon's close
for the newest such session moved by the combined ratio, and only then rewrites and stamps
rebased. The state lives in the files themselves, so merging two copies of the cache cannot
separate a "done" mark from the bars it describes.

The splits list (_splits.json, all US tickers since 2015) is refreshed each run. chart() reports a
split between the window's first bar and the next day as Yahoo's events.splits did (a day early,
because of the unverified point above), so fetch_prices marks the price suspicious and the card
updater holds the card until a person looks. A split a person has confirmed the card was rebuilt
for goes in pipeline/split_acks.json (fetch_prices.split_acks, update_cards.split_reflected - the
existing acknowledgement, 2026-11-20); chart() still reports it, and those callers skip it.

chart() returns the same shape as Yahoo's v8 chart response (timestamp = the session's 09:30 ET
open, indicators.quote[0] o/h/l/c/v, events.splits), so fetch_prices.completed_bars,
update_cards.fetch_bars and their tests read it unchanged. There is no meta, so
fetch_prices.fill_from_meta never fills anything from Polygon.

Key: POLYGON_API_KEY from the environment (GitHub secret) or ~/.config/second-brain/api_keys.env.
Without a key sync does nothing; chart() never fetches either way.

Usage: python3 pipeline/polygon_bars.py sync [--days 31] [--now ISO]    # what fetch_prices runs first
       python3 pipeline/polygon_bars.py splits-init                       # one-time full splits pull
       python3 pipeline/polygon_bars.py merge DIR                         # workflow push retry
"""
import argparse
import json
import math
import os
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, time as dtime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ET = ZoneInfo("America/New_York")
CACHE = Path(os.environ.get("POLYGON_CACHE") or ROOT / "site_data" / "polygon_daily")
BASE = "https://api.polygon.io"
GAP = 13                 # seconds between calls: 5 a minute
MIN_RESULTS = 11000      # a real session had 12,457-12,875 tickers (2026-08-17..11-24); fewer is partial
SETTLE = dtime(16, 20)   # = fetch_prices.SETTLE (test_pipeline checks they agree)
RANGE_DAYS = {"1mo": 31, "3mo": 92, "1y": 366}
REFETCH_MAX = 5          # non-OK files fetched again per run
HOLES_MAX = 20           # missing weekdays older than the window fetched per run
NULL_CHECK_MAX = 10      # suspicious nulls re-checked per run (one per-ticker call each)
DEADLINE = 45 * 60       # seconds; sync stops starting new calls after this
SPLITS_FROM = "2015-01-01"
HISTORY_DAYS = 729       # the free plan's two years
_last_call = [0.0]
_deadline = [None]       # time.monotonic() after which get() refuses to start a request (set by sync)


class NotYet(Exception):
    """Polygon has not released this session yet (free plan: not before the end of the day)."""


class ProviderDown(RuntimeError):
    """Network errors, 5xx or 429 through every retry: the rest of a sync is not attempted."""


def psym(symbol):
    """Yahoo-style class shares (BRK-B) are BRK.B on Polygon."""
    return symbol.replace("-", ".")


def api_key():
    if os.environ.get("POLYGON_API_KEY"):
        return os.environ["POLYGON_API_KEY"].strip()
    try:
        for line in open(os.path.expanduser("~/.config/second-brain/api_keys.env"), encoding="utf-8"):
            if line.startswith("POLYGON_API_KEY="):
                return line.split("=", 1)[1].strip()
    except OSError:
        pass
    return ""


def _network(e):
    if isinstance(e, urllib.error.HTTPError):
        return e.code >= 500
    return isinstance(e, (urllib.error.URLError, TimeoutError, ConnectionError))


def get(url):
    """GET a Polygon URL (path or full next_url), spaced GAP seconds apart. 429 waits 20/40/60/80 s
    and retries; a 403 that says the session has not ended raises NotYet; network errors and 5xx
    are retried twice (5 s, 15 s). Exhausted retries raise ProviderDown."""
    key = api_key()
    if not key:
        raise RuntimeError("no POLYGON_API_KEY")
    if not url.startswith("http"):
        url = BASE + url
    net_tries, rate_tries = 0, 0
    while True:
        if _deadline[0] is not None and time.monotonic() > _deadline[0]:
            # every attempt and every page counts against sync's deadline, not just each step
            raise ProviderDown("sync deadline reached")
        wait = _last_call[0] + GAP - time.monotonic()
        if wait > 0:
            time.sleep(wait)
        _last_call[0] = time.monotonic()
        try:
            req = urllib.request.Request(url, headers={"Authorization": "Bearer " + key,
                                                       "User-Agent": "stock-widgets-pipeline"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read()[:300].decode("utf-8", "replace")
            if e.code == 429:
                if rate_tries >= 4:
                    raise ProviderDown("polygon HTTP 429 after 5 attempts") from None
                rate_tries += 1
                time.sleep(20 * rate_tries)
                continue
            if e.code == 403 and "before end of day" in body:
                raise NotYet(body) from None
            if not _network(e):
                raise RuntimeError(f"polygon HTTP {e.code}: {body[:160]}") from None
            if net_tries >= 2:
                raise ProviderDown(f"polygon HTTP {e.code} after 3 attempts") from None
        except Exception as e:
            if not _network(e):
                raise
            if net_tries >= 2:
                raise ProviderDown(f"polygon unreachable after 3 attempts: {e}") from None
        time.sleep((5, 15)[net_tries])
        net_tries += 1


def _ok_status(j, what):
    st = j.get("status")
    if st not in ("OK", "DELAYED"):
        raise ValueError(f"{what}: status {st} - not cached")
    return st


# ---------- the per-session cache ----------

def day_path(d):
    return CACHE / f"{d}.json"


def load_day(d):
    p = day_path(d)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def _now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def et_date(stamp):
    """The ET date of a ...Z timestamp (fetchedAt) - split execution dates are ET dates."""
    return datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone(ET).date().isoformat()


def basis(rec, sym):
    """The date sym's bars in this file are split-adjusted as of."""
    return max(et_date(rec["fetchedAt"]), (rec.get("rebased") or {}).get(sym, ""))


def _write(path, text):
    # the temporary file sits outside the committed directory, so a crash leaves nothing to commit
    fd, tmp = tempfile.mkstemp(prefix=".polygon_", suffix=".tmp", dir=path.parent.parent)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def save_day(rec):
    CACHE.mkdir(parents=True, exist_ok=True)
    rec["updatedAt"] = _now_utc()
    bars = rec["bars"]
    # one ticker per line keeps the daily commit's diff readable
    body = ",\n".join(f'    {json.dumps(k)}: {json.dumps(bars[k])}' for k in sorted(bars))
    head = {k: rec[k] for k in ("session", "status", "fetchedAt", "updatedAt", "count")}
    for k in ("rebased", "nullChecked"):
        if rec.get(k):
            head[k] = dict(sorted(rec[k].items())) if isinstance(rec[k], dict) else sorted(rec[k])
    _write(day_path(rec["session"]), json.dumps(head)[:-1] + ', "bars": {\n' + body + "\n  }}\n")


def cached_days():
    return sorted(p.stem for p in CACHE.glob("????-??-??.json")) if CACHE.exists() else []


def _bar(x):
    return [x["o"], x["h"], x["l"], x["c"], x.get("v") or 0]


def fetch_day(d, universe, now_et):
    """Fetch session d (grouped daily) and cache it for `universe`. Returns the record, or raises
    NotYet / ProviderDown / ValueError. Never cached: a status other than OK/DELAYED, a partial
    answer (under MIN_RESULTS tickers), and an empty answer unless it is a holiday - no file with
    bars for that session yet, and asked after noon ET the next day (before that it could be a
    session not yet published; Polygon answered 2026-09-07 with OK and no results). A file whose bars and status would not change is not
    rewritten, so a quiet day commits nothing."""
    j = get(f"/v2/aggs/grouped/locale/us/market/stocks/{d}?adjusted=true")
    status = _ok_status(j, f"grouped daily {d}")
    res = j.get("results") or []
    old = load_day(d)
    if not res:
        if old and any(old["bars"].values()):
            raise ValueError(f"grouped daily {d}: empty answer over a cached session - not cached")
        if now_et < datetime.combine(date.fromisoformat(d) + timedelta(days=1), dtime(12, 0), ET):
            raise ValueError(f"grouped daily {d}: empty answer, status {status} - not cached yet")
        # a holiday; sync asks again for a week (and until OK), and a real session that turns up
        # replaces the all-null file (nothing to protect in it)
    elif len(res) < MIN_RESULTS:
        raise ValueError(f"grouped daily {d}: only {len(res)} tickers, status {status} - not cached")
    by = {x["T"]: x for x in res}
    syms = set(universe) | set((old or {"bars": {}})["bars"])
    bars = {s: (_bar(by[s]) if s in by else None) for s in syms}
    if old and old["bars"] == bars and old["status"] == status:
        return old
    # a fresh grouped answer is on today's basis for every ticker, so per-ticker stamps are moot
    rec = {"session": d, "status": status, "count": len(res), "fetchedAt": _now_utc(), "bars": bars}
    save_day(rec)
    return rec


def history(sym):
    """{session: bar} for sym over the cache's span (at most two years back from the newest file),
    from one per-ticker call. Raises on a bad status or an empty answer."""
    days = cached_days()
    first = max(days[0], (date.fromisoformat(days[-1]) - timedelta(days=HISTORY_DAYS)).isoformat())
    j = get(f"/v2/aggs/ticker/{urllib.parse.quote(sym, safe='.')}/range/1/day/{first}/{days[-1]}"
            "?adjusted=true&sort=asc&limit=50000")
    status = _ok_status(j, f"{sym} history")
    got = {datetime.fromtimestamp(x["t"] / 1000, ET).date().isoformat(): _bar(x) for x in j.get("results") or []}
    if not got:
        raise ValueError(f"{sym} history: empty answer - nothing written")
    return first, got, status


def backfill_ticker(sym, today):
    """A ticker new to the universe: fill sym into every file (within two years) that lacks it, from
    one call; a session the answer has no bar for becomes null. The bars are on today's basis and are
    stamped so. An empty answer writes nothing. Returns the number of files written."""
    if not cached_days():
        return 0
    first, got = history(sym)[:2]
    n = 0
    for d in cached_days():
        rec = load_day(d)
        if d < first or sym in rec["bars"]:
            continue
        rec["bars"][sym] = got.get(d)
        rec.setdefault("rebased", {})[sym] = today
        save_day(rec)
        n += 1
    return n


def _ratio_tol(ratio):
    """How far a close may be from old_close / ratio and still count as re-based: 2%, but never so
    wide that a ratio near 1 (a 5% stock dividend) would pass un-rebased."""
    return min(0.02, abs(math.log(ratio)) / 3) if ratio > 0 else 0


def readjust(sym, pending, today):
    """Rewrite sym's bars that are on an older basis than the listed splits `pending`
    [(ex, ratio)] (all <= the newest cached session). One per-ticker call; nothing is written unless
    the answer covers every such session and its close for the newest one equals the cached close
    divided by the combined ratio of the splits after that file's basis (several splits in a gap
    combine). The check uses the newest stale file whose basis is not an execution date; a file
    fetched ON an execution date (the unverified case in the module docstring) may be on either
    basis, so if only such files are stale, the answer must also show no split-sized step across
    the split before an unmoved close is taken as already re-based. Either way the stale files are
    rewritten from the answer and stamped.
    Returns the number of files rewritten."""
    recs = {d: load_day(d) for d in cached_days()}
    last_ex = max(ex for ex, _ in pending)
    # basis == ex counts as stale: a fetch on the execution date itself may be on either basis
    stale = [d for d, r in sorted(recs.items()) if r["bars"].get(sym) and basis(r, sym) <= last_ex and d < last_ex]
    if not stale:
        return 0
    first, got = history(sym)[:2]
    stale = [d for d in stale if d >= first]
    if not stale:
        return 0
    lost = [d for d in stale if d not in got]
    if lost:
        raise ValueError(f"{sym} history lacks {len(lost)} cached session(s) ({lost[0]}..) - nothing written")
    exs = {ex for ex, _ in pending}

    def moved(d, w):
        old, new = recs[d]["bars"][sym][3], got[d][3]
        return bool(new) and abs(old / new / w - 1) <= (_ratio_tol(w) if w != 1 else 0.002)

    # Proof that the answer is on the new basis comes from a file whose basis is not an execution
    # date: for it exactly one ratio is right and "unmoved" never passes. A file fetched ON an
    # execution date could be on either basis, so it proves nothing (Codex/Fable r4).
    sure = [d for d in stale if basis(recs[d], sym) not in exs]
    if sure:
        d0 = sure[-1]
        want = math.prod(r for ex, r in pending if ex > basis(recs[d0], sym))
        if not moved(d0, want):
            raise ValueError(f"{sym} {d0}: close {recs[d0]['bars'][sym][3]} -> {got[d0][3]}, "
                             f"not the {want:g} split(s) yet - nothing written")
    else:
        # only execution-date files: the answer is on the new basis if it shows no split-sized step
        # from the last stale session to the first session on or after the split
        # Only the splits d0 can still miss count: executed after d0's own session and not before its
        # basis date (that date itself is the ambiguous one). An unmoved close is taken as re-based
        # only if the answer shows no step at ANY of them: across each split, between the last
        # answered session before it and the first one on or after it, the close moves by less than
        # half that split's own ratio (Codex r5/r6: one combined threshold let a single split's step
        # through, and anchoring on the earliest split compared d0 with itself).
        d0 = stale[-1]
        b0 = basis(recs[d0], sym)
        relevant = [(ex, r) for ex, r in pending if ex > d0 and ex >= b0]
        want = math.prod(r for _, r in relevant)

        def no_step(ex, r):
            prev = max((d for d in got if d < ex), default=None)
            nxt = min((d for d in got if d >= ex), default=None)
            return (prev is not None and nxt is not None and got[prev][3] and got[nxt][3]
                    and abs(math.log(got[nxt][3] / got[prev][3])) < abs(math.log(r)) / 2)

        step_ok = bool(relevant) and all(no_step(ex, r) for ex, r in relevant)
        if not relevant or not ((moved(d0, want)) or (moved(d0, 1) and step_ok)):
            raise ValueError(f"{sym} {d0}: close {recs[d0]['bars'][sym][3]} -> {got[d0][3]}, "
                             f"not shown to be on the new basis - nothing written")
    n = 0
    for d in stale:
        rec = recs[d]
        rec["bars"][sym] = got[d]
        rec.setdefault("rebased", {})[sym] = today
        save_day(rec)
        n += 1
    return n


def recheck_nulls(sym, sessions, today):
    """A ticker null in a session while it traded on both neighbours may be a partial answer that
    passed MIN_RESULTS. One per-ticker call fills what Polygon has; the rest stay null and are marked
    checked so they are not asked about again - only when the answer's status is OK; a DELAYED
    answer may still lack the bar, so the session is asked about again on a later run."""
    first, got, status = history(sym)
    n = 0
    for d in sessions:
        rec = load_day(d)
        if d < first or rec["bars"].get(sym) is not None:
            continue
        if got.get(d):
            rec["bars"][sym] = got[d]
            rec.setdefault("rebased", {})[sym] = today
            n += 1
        elif status != "OK":
            continue
        if status == "OK":
            rec["nullChecked"] = sorted(set(rec.get("nullChecked") or []) | {sym})
        save_day(rec)
    return n


def merge_from(src):
    """Fold another copy of the cache (the workflow's own, after a push retry reset the checkout)
    into CACHE: per session the better file wins - status OK over not, then the later updatedAt
    (the split stamps travel inside the file); the splits list with the later updatedAt wins."""
    src = Path(src)
    rank = lambda r: (r["status"] == "OK", r.get("updatedAt") or r["fetchedAt"])
    n = 0
    for p in sorted(src.glob("????-??-??.json")):
        theirs = json.loads(p.read_text(encoding="utf-8"))
        ours = load_day(p.stem)
        if ours is None or rank(theirs) > rank(ours):
            CACHE.mkdir(parents=True, exist_ok=True)
            _write(day_path(p.stem), p.read_text(encoding="utf-8"))
            n += 1
    sp = src / "_splits.json"
    if sp.exists():
        theirs, ours = json.loads(sp.read_text(encoding="utf-8")), load_splits()
        if (theirs.get("updatedAt") or "") > (ours.get("updatedAt") or ""):
            CACHE.mkdir(parents=True, exist_ok=True)
            _write(splits_path(), sp.read_text(encoding="utf-8"))
    return n


# ---------- splits ----------

def splits_path():
    return CACHE / "_splits.json"


def load_splits():
    p = splits_path()
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"checked": None, "updatedAt": None, "splits": {}}


def save_splits(s):
    CACHE.mkdir(parents=True, exist_ok=True)
    s["updatedAt"] = _now_utc()
    body = ",\n".join(f'    {json.dumps(k)}: {json.dumps(s["splits"][k])}' for k in sorted(s["splits"]))
    _write(splits_path(), f'{{"checked": {json.dumps(s["checked"])}, "updatedAt": {json.dumps(s["updatedAt"])},'
                          f' "splits": {{\n{body}\n  }}}}\n')


def pull_splits(since):
    """All US splits with execution_date >= since: {ticker: [[date, split_from, split_to], ...]}.
    Every page must carry status OK."""
    url = f"/v3/reference/splits?execution_date.gte={since}&limit=1000&order=asc&sort=execution_date"
    out = {}
    while url:
        j = get(url)
        if j.get("status") != "OK" or not isinstance(j.get("results", []), list):
            raise ValueError(f"splits list: status {j.get('status')} - not used")
        for x in j.get("results") or []:
            out.setdefault(x["ticker"], []).append([x["execution_date"], x["split_from"], x["split_to"]])
        url = j.get("next_url")
    return out


def update_splits(today):
    """Replace every split dated on or after `since` (the last check minus 10 days) with what Polygon
    lists now, so a split announced late lands and one cancelled or corrected leaves. An empty answer
    over a period that had splits is refused (the list is never emptied by a glitch). The file is
    rewritten only when the list changed or its check is a week old, so a quiet day commits nothing."""
    s = load_splits()
    if s["checked"] == today:
        return s
    since = SPLITS_FROM if not s["checked"] else (date.fromisoformat(s["checked"]) - timedelta(days=10)).isoformat()
    fresh = pull_splits(since)
    held = sum(1 for rows in s["splits"].values() for r in rows if r[0] >= since)
    if held and not fresh:
        raise ValueError(f"splits list: empty answer over {held} cached split(s) since {since} - not used")
    new = {}
    for t in set(s["splits"]) | set(fresh):
        rows = sorted([r for r in s["splits"].get(t, []) if r[0] < since] + [list(r) for r in fresh.get(t, [])])
        if rows:
            new[t] = rows
    changed = new != s["splits"]
    week_old = not s["checked"] or date.fromisoformat(s["checked"]) <= date.fromisoformat(today) - timedelta(days=7)
    s["splits"] = new
    if changed or week_old:
        s["checked"] = today
        save_splits(s)
    return s


def splits_for(sym, upto=None):
    """[(execution_date, ratio)] for sym from the cached list, ratio = split_to / split_from
    (>1 = more shares). Entries after `upto` (default: today in ET) are left out - announced, not
    yet effective."""
    upto = upto or datetime.now(ET).date().isoformat()
    return [(d, b / a) for d, a, b in load_splits()["splits"].get(sym, []) if d <= upto and a and b]


# ---------- sync and read ----------

SPLITS_FRESH = [False]   # set by sync: the splits list was refreshed in this process


def last_settled(now_et):
    d = now_et.date()
    if now_et < datetime.combine(d, SETTLE, ET):
        d -= timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


def weekdays(start, end):
    d, out = start, []
    while d <= end:
        if d.weekday() < 5:
            out.append(d.isoformat())
        d += timedelta(days=1)
    return out


def sync(universe, now_et, days=31, log=print, deadline=DEADLINE):
    """Bring the cache up to date for `universe` (Polygon symbols). The only place that fetches:
    chart() reads the cache and nothing else, so a provider outage costs one call's three attempts
    and then the whole sync stops (ProviderDown); a slow provider stops it at `deadline` seconds.
    Returns warnings; never raises for a provider problem, so the caller runs on what is cached.

    In order: weekdays of the last `days` calendar days without a file; up to HOLES_MAX older
    weekdays without one (back to the first cached file); up to REFETCH_MAX files whose status is
    not OK, newest first; empty (holiday) files of the last 7 days; tickers missing from any file (one call each); the splits list; tickers
    whose cached bars are on a basis older than a listed split; up to NULL_CHECK_MAX tickers null in
    a recent session while they traded on both neighbours."""
    SPLITS_FRESH[0] = False
    if not api_key():
        return ["no POLYGON_API_KEY - prices are read from the cache as it is"]
    warn, t0 = [], time.monotonic()
    _deadline[0] = t0 + deadline
    today = now_et.date().isoformat()
    end = last_settled(now_et)
    window = weekdays(end - timedelta(days=days), end)
    have = cached_days()
    todo = [d for d in window if d not in have]
    if have:
        todo += [d for d in weekdays(date.fromisoformat(have[0]), end - timedelta(days=days))
                 if d not in set(have)][-HOLES_MAX:]
    todo += sorted((d for d in have if load_day(d)["status"] != "OK"), reverse=True)[:REFETCH_MAX]
    # an empty answer taken for a holiday is asked again for a week: a real session answered empty
    # once would otherwise be lost for good (Codex r4); a real holiday answers the same and nothing
    # is rewritten
    todo += [d for d in have if d >= (end - timedelta(days=7)).isoformat() and load_day(d)["count"] == 0]

    pg_notyet = [False]

    def step(label, fn):
        """Run one network step: (ok, value). ProviderDown or the deadline stop the sync."""
        if time.monotonic() - t0 > deadline:
            raise StopIteration(f"polygon sync: {deadline // 60} min deadline reached before {label}")
        try:
            return True, fn()
        except NotYet:
            pg_notyet[0] = True
            log(f"polygon {label}: not released yet")
        except ProviderDown as e:
            raise StopIteration(f"polygon {label}: {str(e)[:160]} - sync stopped, prices read from the cache as it is")
        except Exception as e:
            warn.append(f"polygon {label}: {str(e)[:160]}")
        return False, None

    try:
        gap = None
        for d in sorted(set(todo)):
            if gap and d in window and d not in have:
                # never cache a session past an uncached one inside the window: chart() would then
                # fail every ticker on the hole instead of serving the last complete session
                warn.append(f"polygon {d}: not fetched - {gap} is not cached yet")
                continue
            ok, rec = step(d, lambda: fetch_day(d, universe, now_et))
            if ok:
                log(f"polygon {d}: {rec['count']} tickers, status {rec['status']}")
            elif d in window and d not in have and not pg_notyet[0]:
                gap = d
            pg_notyet[0] = False
        days_now = cached_days()
        if days_now:
            floor = (date.fromisoformat(days_now[-1]) - timedelta(days=HISTORY_DAYS)).isoformat()
            recs = {d: load_day(d) for d in days_now if d >= floor}
            for s in sorted({s for s in universe for r in recs.values() if s not in r["bars"]}):
                ok, n = step(f"backfill {s}", lambda: backfill_ticker(s, today))
                if ok:
                    log(f"polygon backfill {s}: {n} sessions")
        ok, sp = step("splits", lambda: update_splits(today))
        SPLITS_FRESH[0] = ok
        sp = sp if ok else load_splits()
        recs = {d: load_day(d) for d in cached_days()}
        newest = max(recs) if recs else ""
        for s in universe:
            listed = [(ex, b / a) for ex, a, b in sp["splits"].get(s, []) if a and b and ex <= newest]
            older = [r for d, r in recs.items() if r["bars"].get(s)]
            pending = [(ex, r) for ex, r in listed if any(basis(x, s) <= ex and x["session"] < ex for x in older)]
            if pending:
                ok, n = step(f"re-adjust {s}", lambda: readjust(s, pending, today))
                if ok:
                    log(f"polygon re-adjust {s} for {', '.join(ex for ex, _ in pending)}: {n} sessions")
                    recs = {d: load_day(d) for d in cached_days()}
        recent = [d for d in sorted(recs) if recs[d]["count"]][-days:]   # holidays (count 0) are all null by nature
        asked = 0
        for s in universe:
            if asked >= NULL_CHECK_MAX:
                break
            gaps = [d for i, d in enumerate(recent[1:-1], 1)
                     if recs[d]["bars"].get(s, 0) is None and s not in (recs[d].get("nullChecked") or [])
                     and recs[recent[i - 1]]["bars"].get(s) and recs[recent[i + 1]]["bars"].get(s)]
            if gaps:
                asked += 1
                ok, n = step(f"null re-check {s}", lambda: recheck_nulls(s, gaps, today))
                if ok:
                    log(f"polygon null re-check {s} {gaps}: {n} filled")
    except StopIteration as e:
        warn.append(str(e))
    finally:
        _deadline[0] = None
    return warn


def chart(symbol, days, today=None):
    """A Yahoo-v8-shaped daily chart for symbol over the last `days` calendar days of the cache.
    Reads the cache only (sync is the one fetcher).

    The window ends at the newest cached session; every weekday inside it must have a file
    (holidays have one, all null) and the file must list the symbol, otherwise ValueError - an
    unseen gap would read as a session the provider lost. A split is reported (events.splits) when
    it falls between the window's first bar and the day after `today` (ET; default now), even if its
    own session is not cached yet. Acknowledged splits (pipeline/split_acks.json) are reported too;
    fetch_prices and update_cards decide what an acknowledgement lifts."""
    sym = psym(symbol)
    all_days = cached_days()
    if not all_days:
        raise ValueError("price cache is empty - run pipeline/polygon_bars.py sync")
    end = date.fromisoformat(all_days[-1])
    rows = []
    for d in weekdays(end - timedelta(days=days), end):
        rec = load_day(d)
        if rec is None:
            raise ValueError(f"price cache has no file for {d}")
        if sym not in rec["bars"]:
            raise ValueError(f"price cache has no {sym} entry for {d}")
        b = rec["bars"].get(sym)
        if b:
            rows.append((d, b))
    if not rows:
        return {"chart": {"result": None, "error": f"no polygon bars for {sym}"}}
    ts = [int(datetime.combine(date.fromisoformat(d), dtime(9, 30), ET).timestamp()) for d, _ in rows]
    q = {k: [b[i] for _, b in rows] for i, k in enumerate(("open", "high", "low", "close", "volume"))}
    r = {"meta": {"symbol": symbol, "source": "polygon"}, "timestamp": ts, "indicators": {"quote": [q]}}
    upto = (date.fromisoformat(today or datetime.now(ET).date().isoformat()) + timedelta(days=1)).isoformat()
    ev = {}
    for ex, a, b in load_splits()["splits"].get(sym, []):
        if rows[0][0] <= ex <= upto and a and b:
            t = int(datetime.combine(date.fromisoformat(ex), dtime(9, 30), ET).timestamp())
            ev[str(t)] = {"date": t, "numerator": b, "denominator": a, "splitRatio": f"{b:g}:{a:g}"}
    if ev:
        r["events"] = {"splits": ev}
    return {"chart": {"result": [r], "error": None}}


def universe_from(stocks):
    return [psym(t.get("yahooSymbol", t["ticker"])) for t in stocks["tickers"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sync", "splits-init", "merge"])
    ap.add_argument("src", nargs="?", help="merge: the other cache directory")
    ap.add_argument("--data", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--days", type=int, default=31)
    ap.add_argument("--now", default=None)
    a = ap.parse_args()
    now_et = datetime.fromisoformat(a.now).astimezone(ET) if a.now else datetime.now(ET)
    if a.cmd == "merge":
        print(f"polygon cache: {merge_from(a.src)} session file(s) taken from {a.src}")
        return
    if a.cmd == "splits-init":
        s = load_splits()
        s["checked"] = None
        save_splits(s)
        s = update_splits(now_et.date().isoformat())
        print(f"splits: {len(s['splits'])} tickers")
        return
    uni = universe_from(json.loads(Path(a.data).read_text(encoding="utf-8")))
    for w in sync(uni, now_et, a.days):
        print(f"::warning::{w}")


if __name__ == "__main__":
    main()
