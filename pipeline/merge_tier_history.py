#!/usr/bin/env python3
"""git merge driver for site_data/tier_history.json, used by the v2 rebuild's push retry.

The file is an append-only list. When a person adds a card while the rebuild runs, both sides
append an entry at the end and git's line merge conflicts (2026-10-23: TRGP/TDG pushed during the
10-22 rebuild, all three retries failed, the session's cards were lost). Entries are keyed the way
validate_site_data.py keys them (ticker, evaluatedAt, ruleVersion) and merged three-way per key:
a key changed on only one side takes that side, the same change on both is taken once, and a key
both sides changed differently is a real conflict - the driver exits 1 and git reports it as before.

Order: ours (%A) as it is, then the entries only theirs (%B) added, in their order.

Usage (git config merge.tierhistory.driver "python3 pipeline/merge_tier_history.py %O %A %B"):
    python3 pipeline/merge_tier_history.py BASE OURS THEIRS   # writes the result into OURS
"""
import json
import sys
from pathlib import Path


def key(e):
    return (e.get("ticker"), e.get("evaluatedAt"), e.get("ruleVersion"))


def keyed(entries, name):
    if not isinstance(entries, list) or not all(isinstance(e, dict) for e in entries):
        raise ValueError(f"{name}: not a list of entries")
    out = {}
    for e in entries:
        if key(e) in out:
            raise ValueError(f"{name}: duplicate entry {key(e)}")
        out[key(e)] = e
    return out


def merge(base, ours, theirs):
    """Return the merged list, or raise ValueError on a key both sides changed differently."""
    o, a, b = keyed(base, "base"), keyed(ours, "ours"), keyed(theirs, "theirs")
    pick = {}
    for k in {**o, **a, **b}:
        vo, va, vb = o.get(k), a.get(k), b.get(k)
        if va == vb or vb == vo:
            pick[k] = va
        elif va == vo:
            pick[k] = vb
        else:
            raise ValueError(f"both sides changed {k} differently")
    out = [pick[key(e)] for e in ours if pick[key(e)] is not None]
    out += [pick[key(e)] for e in theirs if key(e) not in a and pick[key(e)] is not None]
    return out


def main():
    base_p, ours_p, theirs_p = (Path(p) for p in sys.argv[1:4])
    load = lambda p: json.loads(p.read_text(encoding="utf-8"))
    try:
        # git passes an empty %O when the file did not exist in the common ancestor; an empty side is a
        # truncated file, not a deletion of the history, and stops the merge (Codex review 2026-10-23)
        base = json.loads(base_p.read_text(encoding="utf-8") or "[]")
        out = merge(base, load(ours_p), load(theirs_p))
    except (ValueError, TypeError, AttributeError) as e:   # also invalid JSON, or not a list of objects
        print(f"tier_history merge: {e}", file=sys.stderr)
        return 1
    ours_p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"tier_history merge: {len(out)} entries", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
