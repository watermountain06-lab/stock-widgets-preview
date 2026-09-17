#!/usr/bin/env python3
"""Stage 2B-2: move each card's valuation tab with the price, from its recorded baseline.

Called by update_cards.py inside the same per-card transaction as the price layer
(stage 2A) - if anything here fails, the card isn't written at all. Everything is
computed from site_data/valuation_base/{T}.json (build_valuation_base.py) and
today's close P1, never from yesterday's rounded HTML:
  - each automatic multiple: its value, gauge width and badge (stage from the
    width rule; the badge's label and colour change only when the stage does)
  - its MULTIPLE_DATA entry: the ticker's value, the verdict's own multiple and
    "대비 ±x%" (an anchor-date marker is added once - the anchor is a snapshot
    of the analysis date), and the calcLine's price / market cap / EV / result
    when the recorded form allows; a calcLine that can't follow the price is
    labelled "(분석일 … 기준 계산)" instead
  - the valuation section title's price and date, and the as-of label's wording
Frozen metrics (build_valuation_base.py records why) are left exactly as they are.
"""
import re
from decimal import ROUND_HALF_UP, Decimal

import build_valuation_base as vb

LABEL = {1: "매우낮음", 2: "낮음", 3: "적정", 4: "높음", 5: "매우높음"}
GRAD = {1: "linear-gradient(90deg,#27ae60,#2ecc71)", 2: "linear-gradient(90deg,#27ae60,#8bc34a)",
        3: "linear-gradient(90deg,#f0c040,#e67e22)", 4: "linear-gradient(90deg,#e67e22,#e74c3c)",
        5: "linear-gradient(90deg,#e74c3c,#c0392b)"}
MD_RE = re.compile(r"const MULTIPLE_DATA = \{(.*?)\n\};", re.S)


class RenderError(Exception):
    """A valuation edit didn't match as recorded - the whole card is left untouched."""


def q(x, places):
    return x.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP)


def num(x, places, commas=False):
    return f"{q(x, places):,.{places}f}" if commas else f"{q(x, places):.{places}f}"


def width_text(w):
    s = f"{w:.1f}"
    return s[:-2] if s.endswith(".0") else s


def money(value_b, tok):
    """A dollar amount in the token's own unit, decimals and comma style ("$379.0B", "$253,546M")."""
    v = Decimal(str(value_b)) / Decimal(str(vb.UNIT[tok["unit"]]))
    return "$" + num(v, tok["decimals"], tok["commas"]) + (tok["unit"] if tok.get("shownUnit", True) else "")


def dot(iso):
    return iso.replace("-", ".")


def sub_one(pattern, text, repl, label):
    ms = list(re.finditer(pattern, text))
    if len(ms) != 1:
        raise RenderError(f"{label}: expected 1 match, found {len(ms)}")
    m = ms[0]
    return text[:m.start()] + repl(m) + text[m.end():]


def render(html, base, p1, session, notes):
    r = p1 / Decimal(base["p0"])
    asof = dot(base["cardAsOf"])
    for rec in base["metrics"]:
        if rec["frozen"]:
            continue
        v1 = vb.value_at(rec, r)
        html = val_item(html, rec, v1, base.get("gradients") or {}, notes)
        html = multiple_data(html, rec, v1, r, p1, asof)
    html = target_band(html, base, p1, notes)
    html = section_title(html, p1, session)
    html = summary_asof(html, asof)
    return asof_wording(html)


# ---------- stage 2B-3: the target band ----------

NEUTRAL = "var(--text3)"
FAMILY_COLOUR = {"green": "var(--green)", "gold": "var(--gold)", "red": "var(--red)", "gap": NEUTRAL}
# Anchored on each element's own markup, not on "the old left% appears twice": the marker
# and target ticks can hold the same left%, and then replacing by value would move both.
# top/height verified identical on all 66 cards; only the properties that change are rewritten,
# so any per-card styling the audit did not cover survives.
MARK_TICK = re.compile(r'(top:10px;left:)([\d.]+)(%;width:2px;height:28px;background:)(var\(--[a-z0-9]+\))(;border-radius:1px;)(display:none;)?')
MARK_LABEL = re.compile(r'(top:-6px;left:)([\d.]+)(%;transform:translateX\(-50%\);[^"]*?color:)(var\(--[a-z0-9]+\))([^"]*">현재 \$)([\d,.]+)([^<]*)(</div>)')
TGT_TICK = re.compile(r'top:22px;left:([\d.]+)%;width:2px;height:24px')
TGT_LABEL = re.compile(r'(">)([▲▼▶])( 목표 \$)([\d,.]+)( ?\()([+\-−][\d.]+)(%\)</div>)')
# The stat-box is addressed by the target price it shows, and the pill by its wording, because
# neither may be found by the percentage this stage rewrites - after one render it is gone.
STAT_BOX = re.compile(r'(class="stat-value[^"]*"[^>]*>\$)([\d,.]+)(</div>\s*<div class="stat-sub">[^<%]*?)([+\-−]\d+(?:\.\d+)?)%')
PILL = re.compile(r'(<span style="[^"]*border-radius:999px;[^"]*">)([^<]*)(</span>)')
PILL_UPSIDE = re.compile(r"컨센서스\s*(?:목표가|여력)")


def band_families(band):
    """green / gold / red for the Bear, Base and Bull ranges, "gap" for the grey strips between
    them. Derived from the baseline so the colour never depends on what the card renders today."""
    fams, i = [], 0
    for pair in band["intervals"]:
        if pair in band["ranges"]:
            fams.append(["green", "gold", "red"][i])
            i += 1
        else:
            fams.append("gap")
    return fams


def band_position(band, price):
    """(left%, colour family) for a price, or (None, direction) when it is outside the band.
    Intervals own [low, high); the last one closes on its upper bound."""
    lo0, hi0 = Decimal(band["intervals"][0][0]), Decimal(band["intervals"][-1][1])
    if price < lo0:
        return None, "below"
    if price > hi0:
        return None, "above"
    cum = Decimal(0)
    last = len(band["intervals"]) - 1
    for i, ((lo, hi), w, fam) in enumerate(zip(band["intervals"], band["segments"], band_families(band))):
        lo, hi, w = Decimal(lo), Decimal(hi), Decimal(w)
        if lo <= price < hi or (i == last and price == hi):
            return q(cum + w * (price - lo) / (hi - lo), 1), fam
        cum += w
    return None, "above"  # unreachable while the segments cover the range


def upside_text(target, p1):
    """Signed 1dp percentage plus the arrow that is true of it. At the target neither arrow is,
    so the marker is neutral and a -0.0% is normalised away."""
    pct = q((target / p1 - 1) * 100, 1)
    if pct == 0:
        return "▶", "+0.0"
    return ("▲" if pct > 0 else "▼"), f"{'+' if pct > 0 else ''}{pct}"


# Stage 2B-3. The pilot - ASML, AVGO, INTC and DE, which carry a spaced target label, a
# price in a grey gap, a compound stat-sub and a header pill between them - moved with the
# 2026-09-16 session, and rendering the other 62 offline produced no failure, so the gate
# is open. Put a set of tickers here to hold a change to those cards again.
BAND_TICKERS = None


def target_band(html, base, p1, notes):
    band = base.get("targetBand") or {}
    if band.get("frozen") or not band.get("target"):
        return html
    if BAND_TICKERS is not None and base.get("ticker") not in BAND_TICKERS:
        return html
    open_m = list(re.finditer(r'<div style="position:relative;[^"]*">', html))
    marks = [m for m in MARK_LABEL.finditer(html)]
    if len(marks) != 1:
        raise RenderError(f"target band marker label: expected 1, found {len(marks)}")
    starts = [m.start() for m in open_m if m.start() < marks[0].start()]
    if not starts:
        raise RenderError("target band container not found before the marker")
    blk_start = starts[-1]
    cap = html.find("justify-content:space-between", marks[0].end())
    if cap < 0 or cap - blk_start > 3000:
        raise RenderError("target band caption row not found after the marker")
    blk = html[blk_start:cap]

    left, fam = band_position(band, p1)
    colour = FAMILY_COLOUR[fam] if left is not None else NEUTRAL
    # width_text drops a trailing ".0", so the edges are written the same way an in-band
    # position of 0 or 100 would be - otherwise the same spot reads differently depending
    # on whether the price is just inside the band or just outside it.
    edge, suffix = ("0", " · 밴드 아래") if fam == "below" else ("100", " · 밴드 위")
    pos = width_text(left) if left is not None else edge
    hide = "" if left is not None else "display:none;"

    blk = sub_one(MARK_TICK, blk, lambda x: f"{x.group(1)}{pos}{x.group(3)}{colour}{x.group(5)}{hide}", "band marker tick")
    blk = sub_one(MARK_LABEL, blk,
                  lambda x: (f"{x.group(1)}{pos}{x.group(3)}{colour}{x.group(5)}{num(p1, 2, True)}"
                             f"{'' if left is not None else suffix}{x.group(8)}"), "band marker label")
    arrow, pct = upside_text(Decimal(band["target"]), p1)
    blk = sub_one(TGT_LABEL, blk, lambda x: f"{x.group(1)}{arrow}{x.group(3)}{x.group(4)}{x.group(5)}{pct}{x.group(7)}",
                  "band target label")

    tgt = TGT_TICK.search(blk)
    want, _ = band_position(band, Decimal(band["target"]))
    if tgt and want is not None and abs(Decimal(tgt.group(1)) - want) > Decimal("0.3"):
        raise RenderError(f"band target tick at {tgt.group(1)}% but the baseline puts {band['target']} at {want}%")
    if left is None:
        notes.append(f"price ${num(p1, 2, True)} is {fam} the target band "
                     f"(${band['intervals'][0][0]}~${band['intervals'][-1][1]}) - marker hidden")
    html = html[:blk_start] + blk + html[cap:]
    html = band_stat_box(html, band, pct)
    return band_pill(html, pct)


def band_stat_box(html, band, pct):
    """The stat-box beside the band restates the same upside. It is found by the target price it
    shows - a value this stage never rewrites - and not by yesterday's percentage, which would be
    unfindable after the first render. Only the leading percentage token is replaced: 11 cards
    carry extra context after it, and LRCX and QCOM carry a SECOND percentage that means
    something else. CRM puts words before its percentage ("현재가 대비 +10.4% · 56명 · Buy"), so the
    leading token is the first percentage inside the row rather than the row's first character.
    All 66 in-scope cards carry this box, so finding none is a failure and never a quiet skip."""
    target = Decimal(band["target"])
    hits = []
    for m in STAT_BOX.finditer(html):
        try:
            shown = Decimal(m.group(2).replace(",", ""))
        except ArithmeticError:
            continue
        if abs(shown - target) <= Decimal("0.5"):
            hits.append(m)
    if len(hits) != 1:
        raise RenderError(f"band stat-box: expected 1 for target {band['target']}, found {len(hits)}")
    m = hits[0]
    return html[:m.start(4)] + pct + html[m.end(4):]


def band_pill(html, pct):
    """DE, TMUS and VZ repeat the upside in a header pill, each with its own wording. The pill is
    anchored on its wording rather than on the number, for the same reason as the stat-box - but
    on 컨센서스 목표가/여력 specifically, not on 컨센서스 alone: CSCO's pill reads
    "FY27 가이던스 컨센서스 대폭 상회" and its one percentage is revenue growth, which the looser
    anchor would have overwritten with the target upside."""
    hits = [m for m in PILL.finditer(html) if PILL_UPSIDE.search(m.group(2))]
    if not hits:
        return html
    if len(hits) != 1:
        raise RenderError(f"band header pill: expected 1, found {len(hits)}")
    m = hits[0]
    pcts = list(re.finditer(r"[+\-−]\d+(?:\.\d+)?%", m.group(2)))
    if len(pcts) != 1:
        raise RenderError(f"band header pill: expected 1 percentage, found {len(pcts)}")
    start = m.start(2) + pcts[0].start()
    return html[:start] + pct + "%" + html[start + pcts[0].end() - pcts[0].start():]


SUMMARY_ASOF_STYLE = "font-size:11px;font-weight:400;color:var(--text3);"


def summary_asof(html, asof):
    """The "종합 판단" paragraph quotes the analysis-date multiples and premiums while the gauges above
    it move - say so in its heading (user decision 2026-09-11). Cards without the heading are skipped."""
    pat = r'(<div class="verdict-summary-head">종합 판단 )(?:<span class="summary-asof"[^>]*>[^<]*</span> )?'
    if not re.search(pat, html):
        return html
    return sub_one(pat, html, lambda x: f'{x.group(1)}<span class="summary-asof" style="{SUMMARY_ASOF_STYLE}">'
                                        f'({asof} 분석 기준)</span> ', "종합 판단 heading")


def badge_suffix(badge):
    """What follows the stage wording - "(가중치 0.5)", " · 평가보류" - kept when the stage changes.
    The wording itself may be several words ("4단계 다소 높음"), so only a parenthesis or " ·" starts a suffix."""
    m = re.search(r"(\(.*|\s·.*)$", badge)
    return m.group(1) if m else ""


def val_item(html, rec, v1, gradients, notes):
    """Badge label and colour come from the baseline, never from yesterday's HTML, so the result
    depends on P1 alone: the row's own label and colour at its original stage, otherwise the
    standard label (with the original suffix) and the card's own colour for that stage."""
    ms = [m for m in vb.ROW.finditer(html) if m.group("metric") == rec["metric"]]
    if len(ms) != 1:
        raise RenderError(f"{rec['metric']} row: expected 1, found {len(ms)}")
    m = ms[0]
    blk = m.group(0)
    prefix = re.match(r"[^\d]*", m.group("num").strip()).group(0)  # e.g. "~"
    w = vb.width_of(v1, Decimal(rec["low"]), Decimal(rec["high"]))
    stage = vb.stage_of(w)
    blk = sub_one(r'(<span class="val-number">)[^<]*(</span>)', blk,
                  lambda x: f"{x.group(1)}{prefix}{num(v1, rec['decimals'])}x{x.group(2)}", f"{rec['metric']} value")
    blk = sub_one(r'(<div class="val-fill" style="width:)[\d.]+(%)', blk,
                  lambda x: f"{x.group(1)}{width_text(w)}{x.group(2)}", f"{rec['metric']} width")
    old = int(m.group("stage"))
    if stage == rec["stage0"]:
        label, grad = rec["badge"], rec.get("gradient0") or GRAD[stage]
    else:
        suffix = badge_suffix(rec["badge"])
        label, grad = f"{stage}단계 {LABEL[stage]}{suffix}", gradients.get(str(stage), GRAD[stage])
    blk = sub_one(r"(<span class=\"stage-badge) stage-\d", blk, lambda x: f"{x.group(1)} stage-{stage}", f"{rec['metric']} badge class")
    blk = sub_one(r'(<span class="stage-badge[^"]*"(?: style="[^"]*")?>)[^<]*(</span>)', blk,
                  lambda x: f"{x.group(1)}{label}{x.group(2)}", f"{rec['metric']} badge text")
    blk = sub_one(r'(<div class="val-fill" style="width:[\d.]+%;background:)[^;"]*', blk,
                  lambda x: x.group(1) + grad, f"{rec['metric']} gradient")
    if stage != old:
        notes.append(f"{rec['metric']} badge {old}단계 -> {stage}단계")
    return html[:m.start()] + blk + html[m.end():]


def multiple_data(html, rec, v1, r, p1, asof):
    md = [m for m in MD_RE.finditer(html)]
    if len(md) != 1:
        raise RenderError(f"MULTIPLE_DATA: expected 1, found {len(md)}")
    region = md[0].group(1)
    bm = [m for m in re.finditer(rf"\n  {rec['metric']}: \{{(.*?)\n  \}}", region, re.S)]
    if len(bm) != 1:
        raise RenderError(f"MULTIPLE_DATA.{rec['metric']}: expected 1, found {len(bm)}")
    body = bm[0].group(1)
    if rec.get("valueKey"):
        body = sub_one(rf"({rec['valueKey']}: )[\d.]+(,)", body,
                       lambda x: f"{x.group(1)}{num(v1, rec['decimals'])}{x.group(2)}", f"{rec['metric']} {rec['valueKey']}")
    body = verdict(body, rec, v1, asof)
    body = calc_line(body, rec, v1, r, p1, asof)
    region = region[:bm[0].start(1)] + body + region[bm[0].end(1):]
    s, e = md[0].span(1)
    return html[:s] + region + html[e:]


def verdict(body, rec, v1, asof):
    vm = re.search(r"(verdict: ')([^']*)(')", body)
    if not vm:
        return body
    vt = vm.group(2)
    if rec.get("verdictFirstIsValue"):
        vt = sub_one(r"~?[\d.]+x", vt[:re.search(r"~?[\d.]+x", vt).end()], lambda x: f"{num(v1, rec['decimals'])}x",
                     "verdict value") + vt[re.search(r"~?[\d.]+x", vt).end():]
    pm = re.search(r"대비 ([+\-−])([\d.]+)%", vt)
    if pm and rec.get("anchor") and rec.get("verdictPremium0") is not None:
        p = q((v1 / Decimal(rec["anchor"]) - 1) * 100, rec["premiumDecimals"])
        neg = pm.group(1) if pm.group(1) in "-−" else "-"
        sign = "+" if p >= 0 else neg
        vt = vt[:pm.start()] + f"대비 {sign}{abs(p):.{rec['premiumDecimals']}f}%" + vt[pm.end():]
        if not ANCHOR_DATE.search(vt):
            vt = add_anchor_date(vt, asof)
    elif pm and not re.search(r"\(분석일 \d{4}\.\d{2}\.\d{2} 기준\)", vt):  # a premium the model can't follow stays, labelled
        vt = vt[:pm.end()] + f" (분석일 {asof} 기준)" + vt[pm.end():]
    return body[:vm.start(2)] + vt + body[vm.end(2):]


ANCHOR_DATE = re.compile(r"(?:, |\(앵커 )\d{4}\.\d{2}\.\d{2}(?: 분석 시점 고정| 기준)\)")
# Any as-of already written inside the anchor parenthesis, whatever separator
# introduces it. The narrow ANCHOR_DATE above only recognises ", " and "(앵커 ",
# so a card that wrote "평균 27.23x· 2026.09.11 기준" got a second date appended
# and rendered "…, 2026.09.11 기준, 2026.09.11 기준)". Three shipped cards did
# (CRM, LIN, CRWD). The date is NOT overwritten: it states when the peer
# multiples were measured, which is not always the analysis date - CRWD's peers
# really are 2026.09.09 against a 2026.09.11 analysis.
# The qualifier between the date and 기준 is not fixed - cards write "2026.09.11 기준",
# "2026.09.11 종가 기준", "2026.09.11 분석 기준". Matching only the bare form let VZ
# collect "(앵커 … 기준) (앵커 … 종가 기준)" on all five metrics.
INNER_DATE = re.compile(r"\d{4}\.\d{2}\.\d{2}(?:\s*분석 시점 고정|(?:\s*[^()\s]{1,4})?\s*기준)")


# What this stamp may claim. It says the anchor is FROZEN at the analysis - it does not
# move with price the way the card's own multiple does. It must not be read as "the peer
# multiples were measured on this date", because that is something the pipeline has no way
# to know: KLAC's peers are AMAT 09.08 / LRCX 09.04 and IBM's are ORCL 09.04 / CSCO 09.06,
# both stated on the cards themselves, and the old wording ", 2026.09.11 기준" contradicted
# those statements outright. "분석 시점 고정" is true on every card whatever the peers' own
# as-of, so no per-card detection is needed. (Decided with the user 2026-09-13.)
FROZEN_AT = "분석 시점 고정"


def add_anchor_date(vt, asof):
    """Say once that the anchor is frozen at the analysis date - inside the parenthesis that holds the
    comparison value ("앵커(… 평균 54.2x, 2026.09.09 분석 시점 고정) 대비 +10.1%"), else right after
    the premium. See FROZEN_AT above for what this may and may not be read as claiming."""
    i = vt.find("대비")
    head = vt[:i]
    j = head.rfind(")")
    k = head.rfind("(", 0, j) if j > 0 else -1
    if j > 0 and k >= 0 and re.search(r"[\d.]+x", head[k:j]):
        if INNER_DATE.search(head[k:j]):   # the card already states one - leave it alone
            return vt
        return vt[:j] + f", {asof} {FROZEN_AT}" + vt[j:]
    pos = vt.find("%", i) + 1
    # Same guard as the branch above, which this one lacked: a self-history verdict
    # ("자기 5년 중앙값 대비 +17.0%") has no anchor parenthesis holding an "x" value, so it
    # falls through to here - and VZ, whose card already said "(앵커 2026.09.11 종가 기준)",
    # got a second one appended on all five metrics.
    if INNER_DATE.search(vt[pos:pos + 60]):
        return vt
    return vt[:pos] + f" (앵커 {asof} {FROZEN_AT})" + vt[pos:]


def calc_line(body, rec, v1, r, p1, asof):
    cm = re.search(r"(calcLine: ')([^']*)(')", body)
    if not cm:
        return body
    c, info = cm.group(2), rec.get("calc") or {"form": "fixed"}
    if info["form"] == "fixed":
        if not re.search(r"\(분석일 \d{4}\.\d{2}\.\d{2} 기준 계산\)", c):
            c = f"(분석일 {asof} 기준 계산) " + c
    else:
        res = info["result"]
        c = sub_one(vb.RESULT_RE, c, lambda x: x.group(1) + num(Decimal(res["value"]) * v1 / Decimal(rec["value0"]),
                                                                res["decimals"]) + x.group(3), "calcLine result")
        if info["form"] == "price":
            c = sub_one(vb.PRICE_RE, c, lambda x: f"{x.group(1)}${num(p1, 2, True)}{x.group(3)}", "calcLine price")
        if info.get("mcap"):
            mc0 = vb.billions(info["mcap"]["value"], info["mcap"]["unit"])
            c = sub_one(vb.MC_RE, c, lambda x: x.group(1) + money(Decimal(str(mc0)) * r, info["mcap"]), "calcLine market cap")
        if info["form"] == "ev":
            ev1 = Decimal(str(rec["ev0"])) + Decimal(str(rec["mcap0"])) * (r - 1)
            c = sub_one(vb.EV_RE, c, lambda x: x.group(1) + money(ev1, info["ev"]), "calcLine EV")
        if info.get("priceContext"):
            ctx = info["priceContext"]
            c = sub_one(re.escape(ctx) + r"\$[\d,.]+", c, lambda x: f"{ctx}${num(p1, 2, True)}", "calcLine quoted price")
    return body[:cm.start(2)] + c + body[cm.end(2):]


def section_title(html, p1, session):
    m = re.search(r'section-title">밸류에이션[^<]*', html)
    if not m or "현재가 $" not in m.group(0):
        return html
    seg = sub_one(r"(현재가 )\$[\d,.]+", m.group(0), lambda x: f"{x.group(1)}${num(p1, 2, True)}", "valuation title price")
    seg = re.sub(r"\(\d{4}\.\d{2}\.\d{2} 종가\)", f"({dot(session)} 종가)", seg, count=1)
    return html[:m.start()] + seg + html[m.end():]


def asof_wording(html):
    """The as-of label now has to say the multiples follow the price too."""
    html = re.sub(r'(<div class="asof-line"[^>]*>)가격·기술지표: ', r"\1가격·기술지표·배수: ", html, count=1)
    return html.replace(" · 분석 문장·밸류에이션: ", " · 분석 문장·재무·앵커: ", 1)
