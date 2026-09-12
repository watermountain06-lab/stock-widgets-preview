#!/usr/bin/env python3
"""One-time seed of stocks.json's tier and score blocks from existing artifacts.

Tier: each card states its 7-tier valuation verdict in three places that the
playbook requires to agree - the 핵심 투자 논리 headline, the 종합 밸류에이션
"종합 판단" tag, and the 4개 분석 종합 "⚖️ 밸류에이션" row. The headline is the
source of truth; the other two are cross-checked and any disagreement is
recorded as status "conflict" (headline value kept, never auto-resolved).
Non-standard labels are normalized only for the tickers in NORMALIZE_ALLOW;
anything else unrecognized fails the run instead of being guessed. Each tier
found is also appended to tier_history.json as a "seeded" entry (skipped if
that exact entry already exists, so re-runs don't duplicate).

Score: copied from the redesign repo's frozen v1.0.0 fundamental-score files.
Banks are "excluded" by the config's bank_exclude_tickers, which is the one
place that list lives (WFC/GS were folded in on 2026-09-12; they had been
hardcoded here, so a re-scoring run that read only the config would have
silently scored them).

Dry run by default (prints a 50-row review table); --write updates
stocks.json and tier_history.json.

Usage: python3 pipeline/extract_tiers_scores.py [--write] [--scores-dir DIR]
"""
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REDESIGN_SCORES = Path.home() / "Workspace/stock-widgets-redesign/scripts"

TIERS = ["초저평가", "저평가", "적정~저평가", "적정", "고평가~적정", "고평가", "초고평가"]
# longest first so "고평가~적정" isn't read as "고평가"; the two reversed
# orderings are recognized only so NORMALIZE_ALLOW can map them
TOKENS = ["초고평가", "초저평가", "고평가~적정", "적정~고평가", "적정~저평가", "저평가~적정",
          "고평가", "저평가", "적정"]
REVERSED = {"저평가~적정": "적정~저평가", "적정~고평가": "고평가~적정"}
NORMALIZE_ALLOW = {
    "CSCO": "reversed range order 저평가~적정",
    "SNDK": "reversed range order 적정~고평가",
    "SKHY": "trailing ADR-premium caveat after the label",
}

HEADLINE_RE = re.compile(r"핵심 투자 논리 <span[^>]*>\(([^)]*)\)</span>")
SUMMARY_RE = re.compile(r'class="verdict-summary-head">종합 판단 <span[^>]*>([^<]*)</span>')
ROW_RE = re.compile(r'<span class="zone-label">⚖️ 밸류에이션</span><span class="zone-val"[^>]*>([^<]*)</span>')

SCORE_FILE = {"BRKB": "BRK_B"}
SEED_RULE = "card-headline-v0"


def leading_token(text):
    t = (text or "").strip()
    return next((tok for tok in TOKENS if t.startswith(tok)), None)


def canonical(token):
    return REVERSED.get(token, token)


def extract_tier(ticker, html):
    """(tier record, review row) from one card's three verdict spots."""
    h = HEADLINE_RE.search(html)
    s = SUMMARY_RE.search(html)
    r = ROW_RE.search(html)
    raw = h.group(1).strip() if h else None
    head_tok = leading_token(raw)
    others = {"summary": leading_token(s.group(1)) if s else None,
              "row": leading_token(r.group(1)) if r else None}

    if head_tok is None:
        tier = {"value": None, "raw": raw, "status": "missing"}
        return tier, others
    value = canonical(head_tok)
    if raw == value:
        status = "valid"
    elif ticker in NORMALIZE_ALLOW:
        status = "normalized"
    else:
        raise ValueError(f"{ticker}: unrecognized headline label {raw!r} (not in NORMALIZE_ALLOW)")

    tier = {"value": value, "raw": raw, "status": status}
    if status == "normalized":
        tier["note"] = NORMALIZE_ALLOW[ticker]
    disagree = {spot: tok for spot, tok in others.items() if tok is not None and canonical(tok) != value}
    if disagree:
        tier["status"] = "conflict"
        tier["note"] = "headline kept; " + ", ".join(f"{k} says {v}" for k, v in disagree.items())
    # a spot with no readable label can't confirm the headline - not a
    # disagreement, but it must not pass silently either (the markup may have
    # drifted), so it is recorded on the tier and warned about
    absent = [spot for spot, tok in others.items() if tok is None]
    if absent:
        msg = "no tier label found in " + ", ".join(absent)
        tier["note"] = f"{tier['note']}; {msg}" if tier.get("note") else msg
        print(f"WARNING {ticker}: {msg} - headline unconfirmed there", file=sys.stderr)
    return tier, others


def extract_score(ticker, scores_dir, bank_list, unsupported=None):
    if ticker in bank_list:
        return {"status": "excluded", "reason": "bank (config bank_exclude_tickers)"}
    if unsupported and ticker in unsupported:
        return {"status": "unsupported", "reason": unsupported[ticker]}
    path = scores_dir / "fundamental_scores" / f"{SCORE_FILE.get(ticker, ticker)}_fundamental_score.json"
    if not path.exists():
        return {"status": "missing", "reason": "no score file (card built after the 2026-08-25 scoring run)"}
    d = json.loads(path.read_text(encoding="utf-8"))
    if d.get("totalScore") is None:
        return {"status": "missing", "reason": f"score file has no totalScore ({d.get('status', 'no status')})"}
    rec = {"status": "available", "total": d["totalScore"], "grade": d.get("grade"),
           "financialsAsOf": d["financialsAsOf"], "valuationAsOf": d.get("valuationAsOf")}
    if d.get("coverageStatus") != "full":
        rec["note"] = f"coverage {d.get('coverageStatus')}"
    # v1.0.1 - carry the diagnostics the homepage needs to stop presenting a
    # thin score as if it were comparable. qualityFlags is separate from
    # coverageStatus on purpose (see the score config's v1_0_1_note).
    flags = d.get("qualityFlags") or []
    if flags:
        rec["qualityFlags"] = flags
    if d.get("financialsAgeMonths") is not None:
        rec["financialsAgeMonths"] = d["financialsAgeMonths"]
    val = d.get("valuation") or {}
    if val.get("historicalMultipleCoverage") is not None:
        rec["valuationCoverage"] = {
            "historicalMultiples": val["historicalMultipleCoverage"],
            "targetPrice": bool(val.get("targetPriceAvailable")),
        }
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--history", default=str(ROOT / "site_data" / "tier_history.json"))
    ap.add_argument("--scores-dir", default=str(REDESIGN_SCORES))
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    data_path, hist_path, scores_dir = Path(args.data), Path(args.history), Path(args.scores_dir)
    data = json.loads(data_path.read_text(encoding="utf-8"))
    config = json.loads((scores_dir / "fundamental_score_config_v1.json").read_text(encoding="utf-8"))
    if config.get("version") != data.get("scoreVersion"):
        sys.exit(f"score config version {config.get('version')} != stocks.json scoreVersion {data.get('scoreVersion')}")
    banks = set(config["bank_exclude_tickers"])
    unsupported = config.get("unsupported_tickers", {})
    history = json.loads(hist_path.read_text(encoding="utf-8")) if hist_path.exists() else []
    seen = {(e["ticker"], e["evaluatedAt"], e["ruleVersion"]) for e in history}

    failures, added = [], 0
    print(f"{'tk':5} {'headline':30} {'summary':10} {'row':10} -> {'tier':10} {'status':10} | score")
    for t in data["tickers"]:
        tk = t["ticker"]
        try:
            tier, others = extract_tier(tk, (ROOT / t["href"]).read_text(encoding="utf-8"))
        except ValueError as e:
            failures.append(str(e))
            continue
        score = extract_score(tk, scores_dir, banks, unsupported)
        t["tier"], t["score"] = tier, score
        sc = f"{score['total']} ({score['financialsAsOf']})" if score["status"] == "available" else score["status"]
        print(f"{tk:5} {str(tier['raw'])[:30]:30} {str(others['summary']):10} {str(others['row']):10} -> "
              f"{str(tier['value']):10} {tier['status']:10} | {sc}")

        key = (tk, t["cardAsOf"], SEED_RULE)
        if tier["value"] is not None and key not in seen:
            history.append({"ticker": tk, "evaluatedAt": t["cardAsOf"], "stages": None, "weights": None,
                            "weightedAvg": None, "machineTier": None, "previousTier": None,
                            "publishedTier": tier["value"], "decision": "seeded", "ruleVersion": SEED_RULE})
            seen.add(key)
            added += 1

    counts = {}
    for t in data["tickers"]:
        counts[t["tier"]["status"]] = counts.get(t["tier"]["status"], 0) + 1
    print(f"\ntier status: {counts}")
    print("tier values:", {v: sum(1 for t in data["tickers"] if t["tier"]["value"] == v) for v in TIERS})
    if failures:
        print(f"\n{len(failures)} failed - nothing written:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    if args.write:
        data["generatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        data_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        hist_path.write_text(json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\nWrote {data_path} and {hist_path} (+{added} history entries)")
    else:
        print(f"\nDry run - would add {added} history entries; pass --write to apply")


if __name__ == "__main__":
    main()
