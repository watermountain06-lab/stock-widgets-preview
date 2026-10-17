#!/usr/bin/env python3
"""Fail if preview-only screen code has leaked into the live repo (2026-10-17, dr consensus).

Screen code is authored in preview and copied to live by hand when the user asks
(pipeline/site_ui/UI_DIFF.md). Features listed as preview-only there must not reach live:
neither visible nor as code. Run this on the live working tree after copying and before
committing.

It scans every *.html, *.css and *.js at the live repo root and under dist/ - the whole set
each time, not a fixed list, so a newly added screen file is covered too. cards/ is not
scanned: cards come from preview v2/ through sync_cards.py and never carry homepage code.

Limits: it only finds the markers and identifiers below. Preview-only code copied without
its marker, or a card path left unconverted, is not caught - the browser check and the
live diff in UI_DIFF.md step 4 are the final check.

Usage: python3 pipeline/site_ui/check_live_leak.py ~/Workspace/stock-widgets-redesign
"""
import sys
from pathlib import Path

# Extend together with UI_DIFF.md section 1 when a preview-only feature is added.
NEEDLES = [
    "preview-only",        # line markers and the preview-only.js / .css file names
    "PreviewOnly",         # window.PreviewOnly (range toggle)
    "range-bar",           # range toggle markup and CSS
    "STOCKS_DATA_START",   # preview's source data block (stays in preview)
]


def scan(live):
    files = []
    for base in (live, live / "dist"):
        if base.is_dir():
            files += [p for p in sorted(base.iterdir()) if p.is_file() and p.suffix in (".html", ".css", ".js")]
    hits = []
    for p in files:
        for n, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for needle in NEEDLES:
                if needle in line:
                    hits.append(f"{p.relative_to(live)}:{n}: {needle}")
    return files, hits


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__.strip().splitlines()[-1])
    live = Path(sys.argv[1]).expanduser().resolve()
    if not (live / "index.html").is_file():
        sys.exit(f"check_live_leak: no index.html in {live}")
    files, hits = scan(live)
    if hits:
        print(f"LEAK - preview-only code found in {live}:")
        print("\n".join(hits))
        sys.exit(1)
    print(f"OK - no preview-only code in {len(files)} screen files under {live}")


if __name__ == "__main__":
    main()
