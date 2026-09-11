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
    html = section_title(html, p1, session)
    html = summary_asof(html, asof)
    return asof_wording(html)


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


ANCHOR_DATE = re.compile(r"(?:, |\(앵커 )\d{4}\.\d{2}\.\d{2} 기준\)")


def add_anchor_date(vt, asof):
    """Say once that the anchor is an analysis-date snapshot - inside the parenthesis that holds the
    comparison value ("앵커(… 평균 54.2x, 2026.09.09 기준) 대비 +10.1%"), else right after the premium."""
    i = vt.find("대비")
    head = vt[:i]
    j = head.rfind(")")
    k = head.rfind("(", 0, j) if j > 0 else -1
    if j > 0 and k >= 0 and re.search(r"[\d.]+x", head[k:j]):
        return vt[:j] + f", {asof} 기준" + vt[j:]
    pos = vt.find("%", i) + 1
    return vt[:pos] + f" (앵커 {asof} 기준)" + vt[pos:]


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
