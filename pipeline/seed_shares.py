#!/usr/bin/env python3
"""Replace the provisional legacy-implied share counts in site_data/stocks.json
with counts taken from SEC filings, expressed in US-listed-share units
(shares.usEquivalent), so estimated market cap = US close x usEquivalent.

Source per ticker, in order of preference:
  1. MANUAL - counts that aren't a single machine-readable cover fact:
     TSM/ASML (20-F, annual dei only), SKHY (prospectus, no XBRL), V
     (as-converted Class A total from the 10-Q equity note - the cover lists
     five classes that convert at different, drifting rates).
  2. COVER - multi-class issuers. Their dei:EntityCommonStockSharesOutstanding
     is reported per class (dimensional), which companyfacts/companyconcept
     drop, so the cover-page sentence of the latest 10-Q/10-K is parsed and
     each class converted with a per-ticker factor (BRK: A = 1,500 B).
  3. dei via the companyconcept API - everyone else. If the submissions feed
     has a newer 10-Q/10-K than the latest dei fact (companyfacts can lag: KO's
     10-Q filed 2026-07-29 was still missing on 2026-09-11), the cover of that
     newer filing is parsed instead, and the stale dei value is only kept as a
     last resort with status "stale".

Each new count is compared with the provisional value it replaces and gaps
over 5% are flagged. That is a parse-error alarm, not verification - the
legacy value is itself unverified - so a flag needs a human look, not a revert.

Dry run by default; --write updates stocks.json (only if every ticker resolved).

Usage: python3 pipeline/seed_shares.py [--tickers A,B] [--write] [--cache DIR]
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = os.environ.get("SEC_USER_AGENT", "second-brain-stock-widgets gptjhss@gmail.com")
SEC_TICKER = {"BRKB": "BRK-B"}
FILING_FORMS = ("10-Q", "10-K")
FLAG_GAP = 0.05

DATE = r"([A-Z][a-z]+ \d{1,2}, \d{4})"
APOS = "[’']"
NUM = r"([\d,]+)"

MANUAL = {
    "TSM": {
        "usEquivalent": round(25_932_524_521 / 5), "method": "sec-annual-report", "basis": "adr-equivalent",
        "asOf": "2025-12-31", "filedAt": "2026-04-16",
        "filing": "20-F FY2025 dei 25,932,524,521 ordinary shares / 5 per ADR",
        "approximate": False, "status": "ok",
    },
    "ASML": {
        "usEquivalent": 385_417_665, "method": "sec-annual-report", "basis": "ny-registry",
        "asOf": "2025-12-31", "filedAt": "2026-02-25",
        "filing": "20-F FY2025 dei 385,417,665 shares (NY registry 1:1)",
        "approximate": False, "status": "stale",
        "note": "quarterly counts are only published in 6-K press material, not XBRL",
    },
    "SKHY": {
        "usEquivalent": 711_075_500 * 10, "method": "prospectus", "basis": "adr-equivalent",
        "asOf": "2026-07-10", "filedAt": "2026-07-10",
        "filing": "424B4 2026-07-10: 711,075,500 common shares outstanding; 1 ADS = 1/10 share",
        "approximate": False, "status": "ok",
    },
    "V": {
        "usEquivalent": 1_880_000_000, "method": "sec-note", "basis": "as-converted",
        "asOf": "2026-06-30", "filedAt": "2026-07-29",
        "filing": "10-Q Note 11 as-converted class A total 1,880M (classes B-1/B-2/B-3/C and preferred converted)",
        "approximate": True, "status": "ok",
    },
}

# ticker -> (as-of date regex, [(class, count regex, factor)], unit, basis)
COVER = {
    "BRKB": (rf"outstanding as of {DATE}",
             [("A", rf"Class A\s*[—–-]\s*{NUM}\s*shares", 1500),
              ("B", rf"Class B\s*[—–-]\s*{NUM}\s*shares", 1)], 1, "class-b-equivalent"),
    "MA": (rf"As of {DATE}, there were",
           [(c, rf"{NUM} shares outstanding of the registrant{APOS}s Class {c}", 1) for c in "AB"],
           1, "sum-of-classes"),
    "GOOGL": (rf"As of {DATE}, there were",
              [(c, rf"{NUM} million shares of Alphabet{APOS}s Class {c}", 1) for c in "ABC"],
              1_000_000, "sum-of-classes"),
    "META": (rf"shares outstanding as of {DATE}",
             [(c, rf"Class {c} Common Stock \$0\.000006 par value {NUM} shares outstanding", 1) for c in "AB"],
             1, "sum-of-classes"),
    "PLTR": (rf"As of {DATE}, there were",
             [(c, rf"{NUM} shares of the registrant{APOS}s Class {c} common stock", 1) for c in "ABF"],
             1, "sum-of-classes"),
    "DELL": (rf"As of {DATE}, there were",
             [(c, rf"{NUM} outstanding shares of Class {c} Common Stock", 1) for c in "ABC"],
             1, "sum-of-classes"),
    "SPCX": (rf"As of {DATE}, the registrant had",
             [(c, rf"{NUM} shares of Class {c} common stock", 1) for c in "AB"],
             1, "sum-of-classes"),
}

# single-class cover sentences, tried in order when dei lags the latest filing
SINGLE_COVER = [
    rf"Shares Outstanding as of (?P<date>{DATE[1:-1]})\s*\$?[\d.]+ Par Value (?P<n>[\d,]+)",
    rf"As of (?P<date>{DATE[1:-1]}),? (?:there were|the registrant had) (?P<n>[\d,]+) shares of "
    rf"(?:the registrant{APOS}s )?common stock",
    rf"(?P<n>[\d,]+) shares of (?:the registrant{APOS}s )?common stock[^.]{{0,60}}?outstanding as of "
    rf"(?P<date>{DATE[1:-1]})",
]
COVER_CHARS = 25_000  # the cover page sits before the table of contents


class Sec:
    def __init__(self, cache_dir):
        self.cache = Path(cache_dir) if cache_dir else None
        if self.cache:
            self.cache.mkdir(parents=True, exist_ok=True)
        self._ciks = None

    def get(self, url, name):
        if self.cache and (self.cache / name).exists():
            return (self.cache / name).read_bytes()
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        time.sleep(0.15)  # SEC fair-access limit is 10 req/s
        if self.cache:
            (self.cache / name).write_bytes(data)
        return data

    def cik(self, ticker):
        if self._ciks is None:
            raw = json.loads(self.get("https://www.sec.gov/files/company_tickers.json", "company_tickers.json"))
            self._ciks = {v["ticker"]: str(v["cik_str"]).zfill(10) for v in raw.values()}
        sec_ticker = SEC_TICKER.get(ticker, ticker)
        if sec_ticker not in self._ciks:
            raise LookupError(f"no SEC CIK for {sec_ticker}")
        return self._ciks[sec_ticker]

    def latest_filing(self, cik):
        sub = json.loads(self.get(f"https://data.sec.gov/submissions/CIK{cik}.json", f"sub_{cik}.json"))
        r = sub["filings"]["recent"]
        for i, form in enumerate(r["form"]):
            if form in FILING_FORMS:
                return {"form": form, "filedAt": r["filingDate"][i],
                        "accession": r["accessionNumber"][i], "doc": r["primaryDocument"][i]}
        raise LookupError(f"CIK {cik}: no recent 10-Q/10-K")

    def dei_shares(self, cik):
        url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/dei/EntityCommonStockSharesOutstanding.json"
        try:
            facts = json.loads(self.get(url, f"dei_{cik}.json"))["units"]["shares"]
        except (urllib.error.HTTPError, KeyError):
            return None
        if not facts:  # companyconcept can answer with an empty list (KO, 2026-09-11)
            return None
        return max(facts, key=lambda f: (f["end"], f["filed"]))

    def cover_text(self, cik, filing):
        acc = filing["accession"].replace("-", "")
        url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}/{filing['doc']}"
        raw = self.get(url, f"doc_{acc}.htm").decode("utf-8", errors="ignore")
        # inline-XBRL filings open with a hidden <ix:header> (contexts, units,
        # hidden dei facts) that can run tens of thousands of characters and
        # push the visible cover page past any fixed window
        raw = re.sub(r"<ix:header>.*?</ix:header>", " ", raw, flags=re.S | re.I)
        raw = re.sub(r"<(style|script)\b.*?</\1>", " ", raw, flags=re.S | re.I)
        text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
        return re.sub(r"\s+", " ", text)[:COVER_CHARS]


def iso(date_str):
    return datetime.strptime(date_str, "%B %d, %Y").date().isoformat()


def filing_label(f):
    return f"{f['form']} {f['accession']} cover"


def from_cover_classes(ticker, text, filing):
    date_re, classes, unit, basis = COVER[ticker]
    d = re.search(date_re, text)
    if not d:
        raise ValueError(f"{ticker}: cover as-of date not found")
    parsed = []
    for cls, pattern, factor in classes:
        m = re.search(pattern, text)
        if not m:
            raise ValueError(f"{ticker}: Class {cls} count not found on the cover")
        parsed.append({"class": cls, "shares": int(m.group(1).replace(",", "")) * unit, "factor": factor})
    return {
        "usEquivalent": sum(c["shares"] * c["factor"] for c in parsed),
        "method": "sec-cover", "basis": basis, "classes": parsed,
        "asOf": iso(d.group(1)), "filedAt": filing["filedAt"], "filing": filing_label(filing),
        "approximate": unit > 1, "status": "ok",
    }


def from_single_cover(text, filing):
    for pattern in SINGLE_COVER:
        m = re.search(pattern, text)
        if m:
            n = int(m.group("n").replace(",", ""))
            return {
                "usEquivalent": n, "method": "sec-cover", "basis": "single",
                "asOf": iso(m.group("date")), "filedAt": filing["filedAt"], "filing": filing_label(filing),
                "approximate": n % 1_000_000 == 0, "status": "ok",
            }
    return None


def resolve(ticker, listing_type, sec):
    """(shares record, source label) for one ticker."""
    if ticker in MANUAL:
        return dict(MANUAL[ticker]), "manual"
    cik = sec.cik(ticker)
    filing = sec.latest_filing(cik)
    if ticker in COVER:
        return from_cover_classes(ticker, sec.cover_text(cik, filing), filing), "cover-classes"
    if listing_type != "common":
        raise ValueError(f"{ticker}: {listing_type} listing has no MANUAL/COVER rule")

    fact = sec.dei_shares(cik)
    if fact and fact["filed"] >= filing["filedAt"]:
        return {
            "usEquivalent": fact["val"], "method": "sec-dei", "basis": "single",
            "asOf": fact["end"], "filedAt": fact["filed"], "filing": f"{fact['form']} {fact['accn']} dei",
            "approximate": fact["val"] % 1_000_000 == 0, "status": "ok",
        }, "dei"

    # dei is missing or older than the latest 10-Q/10-K: read that filing's cover
    rec = from_single_cover(sec.cover_text(cik, filing), filing)
    if rec:
        return rec, "cover-fallback"
    if fact:
        return {
            "usEquivalent": fact["val"], "method": "sec-dei", "basis": "single",
            "asOf": fact["end"], "filedAt": fact["filed"], "filing": f"{fact['form']} {fact['accn']} dei",
            "approximate": fact["val"] % 1_000_000 == 0, "status": "stale",
            "note": f"newer {filing['form']} filed {filing['filedAt']} but its cover could not be parsed",
        }, "dei-stale"
    raise ValueError(f"{ticker}: no dei fact and the latest cover could not be parsed")


# Shares that are legally outstanding (so they're on the cover and in dei) but
# are excluded from EPS and from economic share counts. Found via the >5%
# flag: LLY's cover says 941,357,065 while its EPS basis is ~891M.
TRUST_SHARES = {
    "LLY": (50_000_000, "10-K FY2025: employee benefit trust held 50 million shares "
                        "at 2025-12-31 and 2024-12-31 (cost basis $3.0B)"),
}


def apply_trust(ticker, rec):
    """Subtract trust-held shares, keeping both lines so the adjustment is auditable."""
    if ticker not in TRUST_SHARES:
        return rec
    held, source = TRUST_SHARES[ticker]
    rec = dict(rec)
    rec["classes"] = [{"class": "common (cover)", "shares": rec["usEquivalent"], "factor": 1},
                      {"class": "employee benefit trust", "shares": held, "factor": -1}]
    rec["usEquivalent"] -= held
    rec["basis"] = "sum-of-classes"
    rec["note"] = source
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--tickers", default=None, help="comma-separated subset")
    ap.add_argument("--cache", default=None, help="cache SEC responses in this directory")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    path = Path(args.data)
    data = json.loads(path.read_text(encoding="utf-8"))
    wanted = {t.strip().upper() for t in args.tickers.split(",")} if args.tickers else None
    if wanted:
        unknown = wanted - {t["ticker"] for t in data["tickers"]}
        if unknown:
            sys.exit(f"unknown ticker(s) in --tickers: {', '.join(sorted(unknown))} - nothing written")
    sec = Sec(args.cache)

    failures, flagged, held = [], [], []
    print(f"{'ticker':6} {'source':14} {'usEquivalent':>16} {'asOf':10} {'filed':10}  vs legacy")
    for t in data["tickers"]:
        tk = t["ticker"]
        if wanted and tk not in wanted:
            continue
        try:
            rec, source = resolve(tk, t["listing"]["type"], sec)
            rec = apply_trust(tk, rec)
        except Exception as e:  # report every ticker's problem, then refuse to write
            failures.append(f"{tk}: {e}")
            continue
        gap = rec["usEquivalent"] / t["shares"]["usEquivalent"] - 1
        # Refuse to move a count BACKWARDS in time, whatever the gap size.
        # Citigroup is the case this exists for: SEC's XBRL API has indexed
        # none of its 2026 filings, so the dei series still ends at the
        # February 10-K while stocks.json holds the Q2 10-Q's own cover
        # figure. The gap is 4.29%, under FLAG_GAP, so it printed no warning
        # and a --write would have silently replaced a verified count with a
        # seven-month-older one - enough to move the ticker's market cap past
        # its rank neighbour. A size threshold cannot catch this class; the
        # as-of date can, and it is the honest test: newer data may differ by
        # any amount, older data should never win.
        stale = rec["asOf"] < t["shares"].get("asOf", "")
        if stale:
            held.append(f"{tk} (incoming {rec['asOf']} older than held {t['shares']['asOf']})")
        flag = "  <-- OLDER, HELD" if stale else ("  <-- CHECK" if abs(gap) > FLAG_GAP else "")
        if flag and not stale:
            flagged.append(tk)
        print(f"{tk:6} {source:14} {rec['usEquivalent']:>16,} {rec['asOf']:10} {rec['filedAt']:10} "
              f"{gap:+7.2%}{flag}")
        if not stale:
            t["shares"] = rec

    if held:
        print(f"\n{len(held)} held - incoming record is OLDER than the one already stored, not written:")
        for h in held:
            print(f"  - {h}")
    if flagged:
        print(f"\n{len(flagged)} flagged (>{FLAG_GAP:.0%} from the provisional value): {', '.join(flagged)}")
    if failures:
        print(f"\n{len(failures)} failed - nothing written:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    if args.write:
        data["generatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\nWrote {path}")
    else:
        print("\nDry run - pass --write to update stocks.json")


if __name__ == "__main__":
    main()
