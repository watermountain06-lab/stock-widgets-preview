#!/usr/bin/env python3
"""Stage 2B-1: record each card's valuation baseline once, and audit it.

Stage 2B will move the valuation tab (the five multiples, their gauges and
badges, the MULTIPLE_DATA detail numbers) and the target-band marker with the
daily price. To avoid re-scaling yesterday's rounded HTML (which drifts), the
update is always computed from a fixed baseline taken here from the card as it
was written:

  P0      the price the card's analysis used = the header price before stage
          2A started rewriting it (git commit PRE_2A); the calcLine "주가($X)"
          agrees with it in all 48 cards that quote one
  metric  value0 (the displayed multiple), its band edges (저/고 labels), the
          weight suffix on its badge, and how it moves with price:
            price-ratio  PER, PBR, PSR, PCR - denominators are fixed until the
                         next earnings, so value = value0 * P1/P0 exactly
            ev-delta     EV/EBITDA - EV1 = EV0 + mcap0*(P1/P0 - 1), so the
                         multiple moves by the equity share of EV only
          anything that can't be reproduced is recorded as frozen, with why
  anchor  the peer anchor from MULTIPLE_DATA (a snapshot at the analysis date)
  band    the target band's price ranges, bar segment widths and target price

Every recorded item has to pass a baseline test - plugging P1 = P0 back in must
reproduce what the card shows now (value text, gauge width, badge stage, the
verdict's "대비 ±x%", the marker's left%). Items that fail are frozen, so the
daily updater never publishes a number its model can't reproduce.

Usage: python3 pipeline/build_valuation_base.py [--tickers A,B] [--write]
       [--out DIR] [--report PATH]
Dry run by default; --write saves site_data/valuation_base/{T}.json.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRE_2A = "e68eda0"  # last commit before stage 2A rewrote card headers
SCHEMA = 1

ROW = re.compile(
    r'<div class="val-item" data-metric="(?P<metric>\w+)"[^>]*>\s*<div class="val-header">\s*'
    r'<span class="val-name">(?P<name>(?:[^<]|<span[^>]*>[^<]*</span>)+)</span>\s*<div style="display:flex;align-items:center;gap:8px;">\s*'
    r'<span class="val-number">(?P<num>[^<]*)</span>\s*'
    r'<span class="stage-badge(?: stage-(?P<stage>\d))?"(?: style="[^"]*")?>(?P<badge>[^<]*)</span>\s*</div>\s*</div>\s*'
    r'<div class="val-track"><div class="val-fill" style="width:(?P<width>[\d.]+)%;[^"]*"></div></div>\s*'
    r'<div class="val-labels">\s*<span class="val-low">(?P<low>[^<]*)</span>\s*<span class="val-mid">[^<]*</span>\s*'
    r'<span class="val-high">(?P<high>[^<]*)</span>', re.S)
# the cards' deliberate full bars for 0-weight metrics (not a width error)
DELIBERATE = {("BRKB", "psr"), ("BRKB", "pcr"), ("BRKB", "evebitda"), ("GE", "evebitda"),
              ("RTX", "pbr"), ("SNDK", "per"), ("SNDK", "pcr")}
PRICE_RATIO = {"per", "pbr", "psr", "pcr"}
UNIT = {"": 1, "M": 1e-3, "B": 1, "T": 1e3}  # to billions


def dec(s):
    return Decimal(s)


def stage_of(w):
    """Width rule shared by every badge (an exact edge stays in the lower stage)."""
    return 1 if w <= 20 else 2 if w <= 40 else 3 if w <= 60 else 4 if w <= 80 else 5


def width_of(v, lo, hi):
    w = (v - lo) / (hi - lo) * 100
    return min(max(w, Decimal(0)), Decimal(100)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def number(text):
    m = re.search(r"-?[\d,]*\.?\d+", text.replace(",", ""))
    return dec(m.group(0)) if m else None


def decimals(text):
    m = re.search(r"\d+\.(\d+)", text)
    return len(m.group(1)) if m else 0


def billions(num, unit):
    return float(num.replace(",", "")) * UNIT.get(unit or "", 1)


# ---------- MULTIPLE_DATA ----------

def multiple_data(html):
    m = re.search(r"const MULTIPLE_DATA = \{(.*?)\n\};", html, re.S)
    if not m:
        return {}
    return {k: body for k, body in re.findall(r"\n  (\w+): \{(.*?)\n  \}", m.group(1), re.S)}


def anchors_of(body):
    """Anchor candidates: the formula's precise value ("= 54.16x") and the displayed one ("54.2x").
    Cards computed the verdict's premium against one or the other, so both are tried."""
    a = re.search(r"anchor: \{ value: '([^']*)'(?:, formula: '([^']*)')?", body)
    out = []
    if a and a.group(2):
        f = re.search(r"=\s*([\d.]+)x", a.group(2))
        if f:
            out.append(("formula", dec(f.group(1))))
    if a:
        v = re.search(r"([\d.]+)x", a.group(1))
        if v:
            out.append(("display", dec(v.group(1))))
    return out


def verdict_reference(body):
    """The comparison value the verdict states itself - the last "N.Nx" before "대비". Some cards
    compare against another peer set or an adjusted average than MULTIPLE_DATA's anchor."""
    v = re.search(r"verdict: '([^']*?)대비", body)
    nums = re.findall(r"([\d.]+)x", v.group(1)) if v else []
    return [("verdict", dec(nums[-1]))] if nums else []


def verdict_premium(body):
    """The verdict's "대비 ±x%" as (value, decimals shown)."""
    v = re.search(r"verdict: '[^']*?대비 ([+\-−])([\d.]+)%", body)
    if not v:
        return None
    return (-1 if v.group(1) in "-−" else 1) * dec(v.group(2)), decimals(v.group(2))


def ebitda_of(calc):
    """The divisor after "÷" ("÷ EBITDA($15.89B", "÷ TTM 조정 EBITDA($4.12B", "÷ EBITDA 추정치(TTM $12.53B"),
    in billions - never the "EBITDA" of the metric's own name."""
    m = re.search(r"÷\s*[^$(÷]{0,12}?EBITDA[^$(]{0,14}\(\s*(?:TTM\s*)?\$([\d,.]+)([MBT])?", calc)
    return billions(m.group(1), m.group(2)) if m else None


def ev_parts(calc, mds, header_cap=None):
    """(EV0, mcap0) in billions from the EV/EBITDA calcLine; the market cap falls back to the
    PSR/PCR calcLine's, then to the card header's at P0 (non-ADR cards only)."""
    m = re.search(r"EV\(\$([\d,.]+)([MBT])?\s*[,=]\s*(?:ADR가 기준 )?(?:시총|시가총액)\s*\$([\d,.]+)([MBT])?", calc)
    if m:
        return billions(m.group(1), m.group(2)), billions(m.group(3), m.group(4)), "calcLine EV and market cap"
    ev = re.search(r"EV\(\$([\d,.]+)([MBT])?", calc)
    for k in ("psr", "pcr"):
        mc = re.search(r"시가총액\(\$([\d,.]+)([MBT])?\)", re.search(r"calcLine: '([^']*)'", mds.get(k, "")).group(1)
                       if re.search(r"calcLine: '([^']*)'", mds.get(k, "")) else "")
        if ev and mc:
            return billions(ev.group(1), ev.group(2)), billions(mc.group(1), mc.group(2)), f"calcLine EV, market cap from {k}"
    pl = re.search(r"\(시가총액 \$([\d,.]+)([MBT])? - [^$]*\$([\d,.]+)([MBT])?, 무차입\)", calc)  # PLTR: EV = mcap - cash
    if pl:
        mc = billions(pl.group(1), pl.group(2))
        return mc - billions(pl.group(3), pl.group(4)), mc, "market cap minus net cash"
    if ev and header_cap:  # early cards state EV alone; the header cap at P0 gives the equity share
        return billions(ev.group(1), ev.group(2)), header_cap, "calcLine EV, market cap from the card header at P0"
    return None, None, None


# ---------- target band ----------

def target_band(html):
    lab = re.findall(r'<span[^>]*>(Bear|Base|Bull) \$([\d,.]+)~([\d,.]+)', html)
    seg = re.search(r'overflow:hidden;display:flex;">(.*?)</div>\s*</div>', html, re.S)
    marker = re.search(r'left:([\d.]+)%;transform:translateX\(-50%\);[^"]*">현재 \$([\d,.]+)</div>', html)
    target = re.search(r'">[▲▼] 목표 \$([\d,.]+) ?\(([+\-−][\d.]+)%\)</div>', html)
    if len(lab) != 3 or not seg or not marker:
        return None, "no standard Bear/Base/Bull band"
    ranges = [(dec(a.replace(",", "")), dec(b.replace(",", ""))) for _, a, b in lab]
    segs = [dec(w) for w in re.findall(r"width:([\d.]+)%", seg.group(1))]
    # price intervals: each range, plus a gap wherever the next range starts above this one's end
    intervals = []
    for i, (lo, hi) in enumerate(ranges):
        intervals.append((lo, hi))
        if i + 1 < len(ranges) and ranges[i + 1][0] > hi:
            intervals.append((hi, ranges[i + 1][0]))
    if len(intervals) != len(segs):
        return None, f"{len(segs)} bar segments for {len(intervals)} price intervals"
    return {"ranges": [[str(a), str(b)] for a, b in ranges], "intervals": [[str(a), str(b)] for a, b in intervals],
            "segments": [str(s) for s in segs], "marker0": marker.group(1),
            "target": target.group(1).replace(",", "") if target else None,
            "upside0": target.group(2).replace("−", "-") if target else None}, None


def marker_left(band, price):
    cum = Decimal(0)
    for (lo, hi), w in zip(band["intervals"], band["segments"]):
        lo, hi, w = dec(lo), dec(hi), dec(w)
        if lo <= price <= hi:
            return cum + w * (price - lo) / (hi - lo)
        cum += w
    return None  # outside the band


# ---------- per card ----------

def pre2a_header(href):
    """(price, market cap in billions) from the card's header before stage 2A rewrote it."""
    old = subprocess.run(["git", "-C", str(ROOT), "show", f"{PRE_2A}:{href}"], capture_output=True, text=True).stdout
    m = re.search(r'<div class="price-main">\$([\d,]+\.\d+)</div>', old)
    c = re.search(r'meta-label">시가총액</span><span class="meta-value[^"]*">(?:약 )?\$([\d,.]+)([TB])', old)
    return (dec(m.group(1).replace(",", "")) if m else None), (billions(c.group(1), c.group(2)) if c else None)


def build(entry, html):
    t = entry["ticker"]
    p0, cap0 = pre2a_header(entry["href"])
    # an ADR card's header cap may be on the ordinary-share basis, unlike its EV - don't mix them
    header_cap = cap0 if entry.get("listing", {}).get("type") != "adr" else None
    base = {"schema": SCHEMA, "ticker": t, "cardAsOf": entry["cardAsOf"], "p0": str(p0) if p0 else None,
            "p0Source": f"header price at git {PRE_2A} (before stage 2A)", "metrics": [], "targetBand": None,
            "builtAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    mds = multiple_data(html)
    calc_prices = {dec(x.replace(",", "")) for x in re.findall(r"calcLine: '[^']*주가\(\$([\d,.]+)\)", html)}
    if p0 and calc_prices and any(abs(c - p0) > Decimal("0.005") for c in calc_prices):
        base["p0Warning"] = f"calcLine price(s) {sorted(map(str, calc_prices))} differ from P0"

    for m in ROW.finditer(html):
        g = m.groupdict()
        rec = {"metric": g["metric"], "name": re.sub(r"<[^>]+>", "", g["name"]).strip(), "valueText": g["num"].strip(), "badge": g["badge"],
               "stage0": int(g["stage"]) if g["stage"] else None, "width0": g["width"],
               "low": str(number(g["low"])) if number(g["low"]) is not None else None,
               "high": str(number(g["high"])) if number(g["high"]) is not None else None,
               "weight": float(wt.group(1)) if (wt := re.search(r"가중치\s*([\d.]+)", g["badge"] + g["name"])) else 1.0,
               "frozen": False}
        body = mds.get(g["metric"], "")
        vkey = re.search(r"(\w+Value):", body)
        rec["valueKey"] = vkey.group(1) if vkey else None
        v0 = number(g["num"]) if re.fullmatch(r"~?\$?-?[\d,.]+x", g["num"].strip()) else None

        def freeze(why):
            rec.update(frozen=True, frozenReason=why)

        if not p0:
            freeze("no analysis-date price")
        elif v0 is None or v0 <= 0:
            freeze(f"not a positive multiple ({g['num'].strip()})")
        elif not g["stage"] or "평가보류" in g["badge"]:
            freeze("badge withheld (평가보류/no stage)")
        elif (t, g["metric"]) in DELIBERATE:
            freeze("deliberate full bar for a 0-weight metric")
        elif rec["low"] is None or rec["high"] is None or dec(rec["high"]) <= dec(rec["low"]):
            freeze("band edges not numeric")
        else:
            rec.update(value0=str(v0), decimals=decimals(g["num"]))
            if g["metric"] in PRICE_RATIO:
                rec["method"] = "price-ratio"
            elif g["metric"] in ("evebitda", "evsales"):
                calc = re.search(r"calcLine: '([^']*)'", body)
                ev0, mc0, how = ev_parts(calc.group(1) if calc else "", mds, header_cap)
                if ev0 and mc0 and ev0 > 0:
                    rec.update(method="ev-delta", ev0=round(ev0, 4), mcap0=round(mc0, 4), evSource=how)
                    # cross-checks the P1 = P0 test can't make: EV0 / EBITDA must give the shown
                    # multiple, and a calcLine market cap must agree with the header's at P0
                    eb = ebitda_of(calc.group(1) if calc else "")
                    implied = ev0 / eb if eb else None
                    rec["evChecked"] = implied is not None
                    if implied is not None and abs(implied / float(v0) - 1) > 0.01:
                        freeze(f"EV0/EBITDA gives {implied:.2f}x, card shows {v0}x")
                    elif header_cap and "header" not in how and abs(mc0 / header_cap - 1) > 0.03:
                        freeze(f"calcLine market cap {mc0:.1f}B is off the header's {header_cap:.1f}B")
                else:
                    freeze("EV/market cap not stated in a parseable form")
            else:
                freeze(f"unknown metric {g['metric']}")
        if not rec["frozen"]:
            # the verdict's premium is only moved later if it can be reproduced exactly here,
            # at the precision the card shows, from one of the anchor candidates
            rec["anchor"] = rec["verdictPremium0"] = None
            prem = verdict_premium(body)
            if prem is not None:
                shown, places = prem
                q = Decimal(1).scaleb(-places)
                hits = [(b, a) for b, a in anchors_of(body) + verdict_reference(body)
                        if ((dec(rec["value0"]) / a - 1) * 100).quantize(q, rounding=ROUND_HALF_UP) == shown]
                if any(b == "verdict" for b, _ in hits):  # the value the sentence itself compares against wins
                    hits = [(b, a) for b, a in hits if b == "verdict"]
                if len({a for _, a in hits}) > 1:  # both reproduce at this precision - use the one the verdict quotes
                    vtext = re.search(r"verdict: '([^']*)'", body).group(1)
                    hits = [(b, a) for b, a in hits
                            if re.search(rf"(?<![\d.]){re.escape(format(a.normalize(), 'f'))}x", vtext)]
                if len({a for _, a in hits}) == 1:
                    basis, anc = hits[0]
                    rec.update(anchor=str(anc), anchorBasis=basis, verdictPremium0=str(shown), premiumDecimals=places)
                elif hits:
                    rec["verdictPremiumNote"] = f"verdict {shown}% fits more than one anchor - left as is"
                else:
                    rec["verdictPremiumNote"] = f"verdict {shown}% not reproducible from the anchor - left as is"
            problems = baseline_test(rec)
            if problems:
                freeze("baseline test: " + "; ".join(problems))
        base["metrics"].append(rec)

    # a row the pattern couldn't read must still be on record, so the updater knows to leave it alone
    parsed = {m["metric"] for m in base["metrics"]}
    for metric in re.findall(r'<div class="val-item" data-metric="(\w+)"', html):
        if metric not in parsed:
            base["metrics"].append({"metric": metric, "frozen": True, "frozenReason": "row markup not parsed"})

    band, why = target_band(html)
    if band and p0:
        left = marker_left(band, p0)
        if left is None or abs(left - dec(band["marker0"])) > Decimal("0.3"):
            band.update(frozen=True, frozenReason=f"marker at P0 gives {left and round(left, 1)} vs card {band['marker0']}")
        else:
            band["frozen"] = False
        base["targetBand"] = band
    else:
        base["targetBand"] = {"frozen": True, "frozenReason": why or "no P0"}
    return base


def value_at(rec, ratio):
    v0 = dec(rec["value0"])
    if rec["method"] == "price-ratio":
        return v0 * ratio
    share = Decimal(str(rec["mcap0"])) / Decimal(str(rec["ev0"]))
    return v0 * (1 + share * (ratio - 1))


def baseline_test(rec):
    """P1 = P0 must reproduce the card: value text, width, badge stage, verdict premium."""
    out = []
    v = value_at(rec, Decimal(1))
    shown = v.quantize(Decimal(1).scaleb(-rec["decimals"]), rounding=ROUND_HALF_UP)
    if shown != number(rec["valueText"]):
        out.append(f"value {shown} vs {rec['valueText']}")
    w = width_of(v, dec(rec["low"]), dec(rec["high"]))
    if abs(w - dec(rec["width0"])) > Decimal("0.6"):
        out.append(f"width {w} vs {rec['width0']}")
    if stage_of(w) != rec["stage0"]:
        out.append(f"stage {stage_of(w)} vs {rec['stage0']}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default=None)
    ap.add_argument("--data", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--out", default=str(ROOT / "site_data" / "valuation_base"))
    ap.add_argument("--report", default=None, help="also write the audit table (markdown) here")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    wanted = {t.strip().upper() for t in args.tickers.split(",")} if args.tickers else None
    lines = ["| 종목 | P0 | 자동 지표 | 동결 지표(사유) | verdict % | 목표가 밴드 |", "|---|---|---|---|---|---|"]
    totals = {"auto": 0, "frozen": 0, "premium": 0, "band": 0, "cards": 0}
    out_dir = Path(args.out)
    for entry in data["tickers"]:
        t = entry["ticker"]
        if wanted and t not in wanted:
            continue
        html = (ROOT / entry["href"]).read_text(encoding="utf-8")
        base = build(entry, html)
        auto = [m["metric"] for m in base["metrics"] if not m["frozen"]]
        frozen = [f"{m['metric']}({m['frozenReason']})" for m in base["metrics"] if m["frozen"]]
        prem = sum(1 for m in base["metrics"] if not m["frozen"] and m.get("verdictPremium0"))
        band = base["targetBand"]
        totals["cards"] += 1
        totals["auto"] += len(auto); totals["frozen"] += len(frozen); totals["premium"] += prem
        totals["band"] += 0 if band.get("frozen") else 1
        lines.append(f"| {t} | {base['p0']} | {', '.join(auto) or '-'} | {'; '.join(frozen) or '-'} | {prem} | "
                     f"{'자동' if not band.get('frozen') else '동결: ' + band.get('frozenReason', '')} |")
        if base.get("p0Warning"):
            lines[-1] += f" ⚠️ {base['p0Warning']}"
        if args.write:
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / f"{t}.json").write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    summary = (f"{totals['cards']} cards: {totals['auto']} metrics automatic, {totals['frozen']} frozen, "
               f"{totals['premium']} verdict premiums reproducible, {totals['band']} target bands automatic")
    print("\n".join(lines)); print("\n" + summary)
    if args.report:
        Path(args.report).write_text("\n".join(lines) + "\n\n" + summary + "\n", encoding="utf-8")
    print(f"Wrote {out_dir}" if args.write else "Dry run - pass --write to save the baselines")


if __name__ == "__main__":
    main()
