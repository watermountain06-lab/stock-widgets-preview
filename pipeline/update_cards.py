#!/usr/bin/env python3
"""Stage 2A: keep each card's market data in step with the daily pipeline.

For every ticker card ({T}_full_widget.html in the preview repo root) this:
  1. fetches completed daily bars from Yahoo (fetch_prices.py's rule: the bar
     for ET date D counts only after D 16:20 ET) up to the homepage's
     priceSession, and treats them as authoritative for their dates - a bar
     the card already has is replaced when it differs (12 cards were built on
     an in-progress last bar), newer bars are appended;
  2. extends the precomputed MA arrays APPEND-ONLY: stored values keep their
     exact text (they differ from a fresh SMA only by half a unit in the last
     place, so recomputing them would rewrite hundreds of values per card);
     only new or re-synced indices get an exact decimal SMA of the DAILY
     closes, rounded half-up to that array's own decimals;
  3. keeps DAILY at most MAX_BARS bars, dropping from the front together with
     the matching MA values so the chart's index pairing holds;
  4. recomputes the technical score and breakout badge with the frozen v1
     scripts, taking the previous displayGrade from site_data/tech_state/
     rather than from the HTML;
  5. rewrites fixed-format numbers in place: header price, change, 52-week
     line and market cap (SEC usEquivalent x close); the chart's static title
     and range summary (the same text its JS computes for the 1Y view); the
     scorecard's score, bar, grade, subscores and date, plus the model risk
     flags and breakout badge only when their state changes; and a one-line
     as-of label that separates the price/technical date from the date the
     analysis prose and valuation were written.
Analysis prose, the valuation tab and the target band (stage 2B) are never
touched.

Every replacement must match exactly once. A card is written only if all
checks pass (strictly increasing dates, sane OHLC on new bars, DAILY/MA
lengths equal, header price == last close, <div> balance, `node --check` on
the inline scripts); otherwise it is left as is and reported. A run with
nothing new changes nothing.

Usage: python3 pipeline/update_cards.py [--tickers A,B] [--write]
          [--cards-dir DIR] [--data PATH] [--state-dir DIR] [--status PATH]
          [--fixtures DIR] [--now ISO]
  --fixtures DIR   read {SYMBOL}.json chart responses from DIR (tests)
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
from datetime import date, datetime, timezone
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "scripts"))
import fetch_prices as fp  # noqa: E402
from compute_breakout_signal import compute_active_breakout  # noqa: E402
from compute_technical_score import compute_signal  # noqa: E402

MAX_BARS = 1255
CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={range}&interval=1d&events=split"
TECH_CONFIG = ROOT / "scripts" / "tech_score_config_v1.json"
BREAKOUT_CONFIG = ROOT / "scripts" / "breakout_config_v1.json"

ARRAY_START = re.compile(r"^const (\w+?)_(DAILY|MA5|MA20|MA60|MA120)\s*=")
# [^;] stops the array at its own "];" - BAC's MA120 line carries a second
# statement (backtest data) after it, which is kept verbatim as the tail
ARRAY_LINE = re.compile(r"^(const (\w+?)_(DAILY|MA5|MA20|MA60|MA120)\s*=\s*)(\[[^;]*\])(\s*;.*)$")
# Cards were built by different scripts: 41 quote dates with ", 8 with ', and
# SKHY puts a space after each comma. New bars are written in the card's own
# style, with numbers as Python float repr (22.0, 197.1) like the builders did.
BAR_TOKEN = re.compile(r"\[([\"'])(\d{4}-\d{2}-\d{2})\1(,\s*)([^\]]*)\]")

GRADE_CLASS = {"강한": "grade-strong", "긍정적": "grade-positive", "혼조": "grade-mixed", "약한": "grade-weak"}
# the cards' labels sit on the same cuts as the grades (85 / 60), so 혼조 and 약한 share one
GRADE_TEXT = {"강한": "기술적 분석 우수", "긍정적": "기술적 분석 적격", "혼조": "기술적 분석 부적격", "약한": "기술적 분석 부적격"}
MODEL_FLAGS = ("장기추세이탈", "고점대비큰조정", "변동성급증(자체이력대비)", "단기추세이탈")
# Generic tooltips for newly raised flags. The cards' existing tooltips quote
# prices from the day they were written, so a new flag gets a number-free one.
GENERIC_TIPS = {
    "장기추세이탈": "현재가가 MA150·MA200 아래에 있고 MA200 자체도 21거래일 전보다 낮아, 중장기 추세가 하락 쪽으로 기울어 있음을 의미합니다.",
    "고점대비큰조정": "52주 고점 대비 하락폭이 25%를 넘어, 고점에서 상당히 깊게 조정받은 상태임을 의미합니다.",
    "변동성급증(자체이력대비)": "ATR(14일 평균 실제 변동폭)이 이 종목 자신의 최근 1년 이력 중 상위 10% 수준에 들어, 하루 변동폭이 평소보다 크게 높아진 상태임을 의미합니다.",
    "단기추세이탈": "종가가 MA50(50일 이동평균)보다 낮다는 뜻입니다. 중장기 추세와 별개로 최근 1~2개월의 단기 흐름이 약해졌다는 신호입니다.",
}
NO_FLAG_SPAN = ('<span class="risk-flag" style="opacity:0.75;" data-tooltip="모델이 점검하는 추세이탈·과열 플래그 중 '
                '현재 발생한 항목이 없다는 뜻입니다. 리스크가 없다는 의미가 아니라, 가격·거래량 기준의 경고 조건에 '
                '걸리지 않았다는 뜻입니다.">✅ 발생한 리스크 플래그 없음</span>')
# sits between .header and .box-key, both max-width:1100px centred; the 16px
# side padding lines the text up with .box-key's own
ASOF_STYLE = ("max-width:1100px;margin:10px auto 12px;padding:0 16px;box-sizing:border-box;"
              "font-size:11px;color:var(--text3);line-height:1.5;")


class EditError(Exception):
    """A replacement didn't match exactly once - the card is left untouched."""


class Hold(Exception):
    """The card needs a human (split, a gap inside its history, too far behind)."""


# ---------- small formatting helpers ----------

def money(x):
    return f"${x:,.2f}"


def dot(iso):
    return iso.replace("-", ".")


def ym(iso):
    return iso[:7].replace("-", ".")


def fmt_price(x):
    """Python float repr of the 2dp value: 22.0, 197.1, 192.93 (the cards' array style)."""
    return repr(round(float(x), 2))


def fmt_dp(value, dp):
    """Exact Decimal SMA rounded half-up to `dp`, written as float repr like the stored values."""
    return repr(float(value.quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP)))


def pct_width(score, mx):
    w = score / mx * 100 if mx else 0
    return f"{w:.0f}" if abs(w - round(w)) < 1e-9 else f"{w:.1f}"


def sub1(html, pattern, repl, label, flags=0):
    new, n = re.subn(pattern, repl, html, flags=flags)
    if n != 1:
        raise EditError(f"{label}: expected 1 match, found {n}")
    return new


# ---------- card arrays ----------

def parse_card_arrays(html):
    """{kind: dict(line_no, prefix, head, tail, tokens)} for DAILY and MA lines."""
    lines = html.split("\n")
    found = {}
    for i, line in enumerate(lines):
        m = ARRAY_LINE.match(line)
        if not m:
            start = ARRAY_START.match(line)
            if start:  # skipping it would leave that array out of step with DAILY
                raise EditError(f"line {i + 1}: {start.group(2)} is not a plain one-line array")
            continue
        head, prefix, kind, body, tail = m.groups()
        if kind in found:
            raise EditError(f"duplicate {kind} array")
        style = None
        if kind == "DAILY":
            matches = list(BAR_TOKEN.finditer(body))
            tokens = [t.group(0) for t in matches]
            if not tokens or "[" + ",".join(tokens) + "]" != body:
                raise EditError("DAILY array is not in the expected [date,o,h,l,c,v] format")
            style = (matches[-1].group(1), matches[-1].group(3))  # (quote, separator)
        else:
            tokens = body[1:-1].split(",") if body != "[]" else []
        found[kind] = {"line": i, "prefix": prefix, "head": head, "tail": tail, "tokens": tokens, "style": style}
    if "DAILY" not in found:
        raise EditError("no DAILY array")
    if len({a["prefix"] for a in found.values()}) != 1:
        raise EditError(f"arrays with different prefixes: {sorted({a['prefix'] for a in found.values()})}")
    return lines, found


def bar_values(token):
    m = BAR_TOKEN.fullmatch(token)
    parts = m.group(4).split(",")
    return (m.group(2), float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), int(float(parts[4])))


def bar_token(style, d, o, h, l, c, v):
    q, sep = style
    return f"[{q}{d}{q}{sep}" + sep.join([fmt_price(o), fmt_price(h), fmt_price(l), fmt_price(c), str(v)]) + "]"


def close_decimal(token):
    return Decimal(BAR_TOKEN.fullmatch(token).group(4).split(",")[3].strip())


def array_dp(tokens):
    decs = [len(t.split(".")[1]) for t in tokens if t != "null" and "." in t]
    return max(decs) if decs else None


# ---------- bars from Yahoo ----------

def fetch_bars(symbol, rng, fixtures, now_et, max_date):
    if fixtures:
        chart = json.loads((Path(fixtures) / f"{symbol}.json").read_text(encoding="utf-8"))
    else:
        chart = json.loads(fp.http_get(CHART_URL.format(symbol=urllib.parse.quote(symbol, safe=""), range=rng)))
        time.sleep(0.2)
    body = chart.get("chart") or {}
    if not body.get("result"):
        raise ValueError(f"no chart result ({body.get('error')})")
    r = body["result"][0]
    q = r["indicators"]["quote"][0]
    bars = {}
    for i, ts in enumerate(r.get("timestamp") or []):
        o, h, l, c, v = (q[k][i] for k in ("open", "high", "low", "close", "volume"))
        if None in (o, h, l, c):
            continue
        d = datetime.fromtimestamp(ts, fp.ET).date()
        if now_et < datetime.combine(d, fp.SETTLE, fp.ET) or d.isoformat() > max_date:
            continue  # not a completed session yet, or past the homepage's session
        bars[d.isoformat()] = (round(o, 2), round(h, 2), round(l, 2), round(c, 2), int(v or 0))
    splits = sorted(datetime.fromtimestamp(int(s.get("date", k)), fp.ET).date().isoformat()
                    for k, s in ((r.get("events") or {}).get("splits") or {}).items())
    return [(d,) + bars[d] for d in sorted(bars)], splits


def fetch_range(last_card_date, max_date):
    gap = (date.fromisoformat(max_date) - date.fromisoformat(last_card_date)).days
    if gap <= 25:
        return "1mo"
    if gap <= 80:
        return "3mo"
    if gap <= 360:
        return "1y"
    raise Hold(f"card is {gap} days behind - rebuild its price history")


# ---------- the update for one card ----------

def sync_bars(arrays, fetched, splits, notes):
    """Replace differing bars / append new ones. Returns (first changed index or None, replaced, appended)."""
    tokens = arrays["DAILY"]["tokens"]
    dates = [bar_values(t)[0] for t in tokens]
    first_card_date = dates[0]
    if any(s >= first_card_date for s in splits):
        raise Hold(f"split in the fetched window ({', '.join(splits)}) - price history needs a rebuild")
    index = {d: i for i, d in enumerate(dates)}
    fetched_dates = {b[0] for b in fetched}
    missing_in_card = [b[0] for b in fetched if b[0] not in index and b[0] < dates[-1]]
    if missing_in_card:
        raise Hold(f"trading day(s) missing inside the card's history: {', '.join(missing_in_card[:5])}")
    changed, replaced, appended = None, 0, 0
    for d, o, h, l, c, v in fetched:
        new = bar_token(arrays["DAILY"]["style"], d, o, h, l, c, v)
        if d in index:
            i = index[d]
            old = bar_values(tokens[i])
            if (abs(old[1] - o) > 0.005 or abs(old[2] - h) > 0.005 or abs(old[3] - l) > 0.005
                    or abs(old[4] - c) > 0.005 or old[5] != v):
                tokens[i] = new
                replaced += 1
                notes.append(f"re-synced {d}: close {old[4]} -> {c}, volume {old[5]:,} -> {v:,}")
                changed = i if changed is None else min(changed, i)
        elif d > dates[-1]:
            tokens.append(new)
            dates.append(d)
            appended += 1
            changed = len(tokens) - 1 if changed is None else changed
    extra = [d for d in dates if d >= fetched[0][0] and d not in fetched_dates] if fetched else []
    return changed, replaced, appended, extra


def extend_mas(arrays, changed):
    """Append-only MA update from index `changed` to the end. Returns number of values computed."""
    daily = arrays["DAILY"]["tokens"]
    closes = [close_decimal(t) for t in daily]
    fallback_dp = next((array_dp(arrays[k]["tokens"]) for k in ("MA20", "MA5", "MA60", "MA120")
                        if k in arrays and array_dp(arrays[k]["tokens"]) is not None), 4)
    computed = 0
    for kind in ("MA5", "MA20", "MA60", "MA120"):
        if kind not in arrays:
            continue
        n = int(kind[2:])
        toks = arrays[kind]["tokens"]
        dp = array_dp(toks) or fallback_dp
        start = changed if changed is not None else len(toks)
        toks[:] = toks[:start]  # anything from `changed` on is recomputed
        for i in range(start, len(daily)):
            if i + 1 < n:
                toks.append("null")
            else:
                toks.append(fmt_dp(sum(closes[i - n + 1:i + 1]) / n, dp))
            computed += 1
    return computed


def trim_front(arrays):
    extra = len(arrays["DAILY"]["tokens"]) - MAX_BARS
    if extra <= 0:
        return 0
    for kind in arrays:
        arrays[kind]["tokens"] = arrays[kind]["tokens"][extra:]
    return extra


def price_data(ticker, tokens):
    bars = [bar_values(t) for t in tokens]
    return {"ticker": ticker, "asOf": bars[-1][0], "current": bars[-1][4],
            "daily": [{"date": d, "o": o, "h": h, "l": l, "c": c, "v": v} for d, o, h, l, c, v in bars]}


def window_stats(bars, n=252):
    """What the chart's JS shows for the 1Y view: range low/high (first occurrence) and return."""
    data = bars[-n:]
    start = len(bars) - len(data)
    base = bars[start - 1][4] if start > 0 else data[0][4]
    last = data[-1][4]
    lows, highs = [b[3] for b in data], [b[2] for b in data]
    lo, hi = min(lows), max(highs)
    return {"from": data[0][0], "to": data[-1][0], "ret": (last / base - 1) * 100, "last": last,
            "lo": lo, "lo_date": data[lows.index(lo)][0], "hi": hi, "hi_date": data[highs.index(hi)][0]}


def scorecard_blocks(html):
    """(start, end) of each <div class="scorecard"> block, each running to the next one."""
    starts = [m.start() for m in re.finditer(r'<div class="scorecard">', html)]
    return [(s, starts[i + 1] if i + 1 < len(starts) else len(html)) for i, s in enumerate(starts)]


def tech_segment(html):
    """(start, end) of the one scorecard block that holds the technical score."""
    hits = [(s, e) for s, e in scorecard_blocks(html) if "가격·거래량 기반 기술 상태 점수" in html[s:e]]
    if len(hits) != 1:
        raise EditError(f"technical scorecard: expected 1 block, found {len(hits)}")
    return hits[0]


def flag_spans(names):
    unknown = [f for f in names if f not in GENERIC_TIPS]
    if unknown:
        raise EditError(f"no tooltip for risk flag(s) {unknown}")
    return [f'<span class="risk-flag" data-tooltip="{GENERIC_TIPS[f]}">⚠️ {f}</span>' for f in names]


def render_flags(html, wanted, notes):
    """Risk flags in the technical scorecard, which comes in three forms: a
    .scorecard-flags block of spans (27 cards), a hand-written .scorecard-noflags
    line (15), or no flag line at all (6, plus the two young listings). Only a
    change in the model's flag set touches it; a first flag replaces the
    no-flags line or goes in just before the detail toggle."""
    n_flags, n_noflags = html.count('<div class="scorecard-flags">'), html.count('<div class="scorecard-noflags">')
    if n_flags + n_noflags > 1:
        raise EditError(f"risk flags: {n_flags} flag and {n_noflags} no-flag containers")
    name_of = lambda s: re.sub(r"^[^\w가-힣]+", "", re.sub(r"<[^>]+>", "", s)).strip()
    if n_flags:
        m = re.search(r'(<div class="scorecard-flags">)(.*?)(</div>)', html, re.S)
        spans = re.findall(r'<span class="risk-flag"[^>]*>[^<]*</span>', m.group(2))
        current = [name_of(s) for s in spans if name_of(s) in MODEL_FLAGS]
        if set(current) == set(wanted):
            return html
        keep = [s for s in spans if name_of(s) not in MODEL_FLAGS and "발생한 리스크 플래그 없음" not in s]
        new = flag_spans(wanted) + keep
        inner = "\n      " + ("\n      ".join(new) if new else NO_FLAG_SPAN) + "\n    "
        notes.append(f"risk flags {current or '없음'} -> {wanted or '없음'}")
        return html[:m.start(2)] + inner + html[m.end(2):]
    if not wanted:
        return html  # the card's own no-flags line (or no line) still holds
    block = '<div class="scorecard-flags">\n      ' + "\n      ".join(flag_spans(wanted)) + "\n    </div>"
    if n_noflags:
        m = re.search(r'<div class="scorecard-noflags">[^<]*</div>', html)
        if not m:
            raise EditError("scorecard-noflags line has markup inside")
        html = html[:m.start()] + block + html[m.end():]
    else:
        # the scorecard's own toggle is the first one after its subscores note
        # (a card's last scorecard block runs to the end of the file, other toggles included)
        note = html.find('class="subscores-note"')
        i = html.find('<div class="detail-toggle', note) if note >= 0 else -1
        if i < 0:
            raise EditError("no detail toggle after the subscores note to put the new risk flags before")
        html = html[:i] + block + "\n\n    " + html[i:]
    notes.append(f"risk flags 없음 -> {wanted}")
    return html


def render(html, ticker, tokens, tech, breakout, shares, card_asof, notes, ma_last):
    bars = [bar_values(t) for t in tokens]
    last, prev = bars[-1], bars[-2]
    close = last[4]
    w = window_stats(bars)

    # --- header ---
    html = sub1(html, r'<div class="price-main">\$[\d,]+\.\d+</div>',
                lambda m: f'<div class="price-main">{money(close)}</div>', "price-main")

    def change(m):
        decimals = len(m.group(3).split(".")[1]) if "." in m.group(3) else 0
        chg = (close / prev[4] - 1) * 100
        up = chg >= 0
        return (f'<div class="price-change" style="color:var(--{"green" if up else "red"});">'
                f'{"▲" if up else "▼"} {"+" if up else "-"}{abs(chg):.{decimals}f}% ({dot(last[0])} {m.group(4) or ""}기준)</div>')
    html = sub1(html, r'<div class="price-change" style="color:var\(--(red|green)\);">([▲▼]) [+\-]([\d.]+)% '
                      r'\(\d{4}\.\d{2}\.\d{2} (종가 )?기준\)</div>', change, "price-change")

    # 48 cards say "52주 최저 …"; the two young listings (SKHY, SPCX) say "상장 이후 최저 …"
    # and cover every bar since listing
    y52 = re.compile(r'(<div style="font-size:11px;color:var\(--text3\);margin-top:2px;">(52주|상장 이후) 최저 )'
                     r'\$[\d,]+\.\d+ \(\d{4}\.\d{2}\.\d{2}\) · 최고 \$[\d,]+\.\d+ \(\d{4}\.\d{2}\.\d{2}\)(</div>)')
    if y52.search(html):
        def hi_lo(m):
            s = w if m.group(2) == "52주" else window_stats(bars, len(bars))
            return (f"{m.group(1)}{money(s['lo'])} ({dot(s['lo_date'])}) · "
                    f"최고 {money(s['hi'])} ({dot(s['hi_date'])}){m.group(3)}")
        html = sub1(html, y52, hi_lo, "header high/low line")
    else:
        raise EditError("header high/low line: expected 1 match, found 0")

    if shares:
        cap = shares * close
        cap_txt = f"${cap / 1e12:.2f}T" if cap >= 1e12 else f"${cap / 1e9:.1f}B"
        html = sub1(html, r'(meta-label">시가총액</span><span class="meta-value[^"]*">)(약 )?\$[\d,.]+[TB](<)',
                    lambda m: f"{m.group(1)}{m.group(2) or ''}{cap_txt}{m.group(3)}", "market cap")

    # --- chart static texts (the JS overwrites them with the same values) ---
    title = re.compile(r'(id="techHeaderTitle">기술적 분석 — 일봉 캔들스틱 \()\d{4}\.\d{2} ~ \d{4}\.\d{2}'
                       r'(\) · 1년 수익률 <span id="techHeaderReturn">)[^<]*(</span>)')
    title_text = re.search(r'id="techHeaderTitle">([^<]*)', html)
    if not title_text:
        raise EditError("no techHeaderTitle")
    if "상장" not in title_text.group(1):  # SKHY/SPCX: since-listing wording, left to the page JS
        sign = "+" if w["ret"] >= 0 else ""
        html = sub1(html, title, lambda m: f"{m.group(1)}{ym(w['from'])} ~ {ym(w['to'])}{m.group(2)}"
                                           f"{sign}{w['ret']:.1f}%{m.group(3)}", "tech title")
    summary = re.search(r'id="techRangeSummary">([^<]*)<', html)
    if not summary:
        raise EditError("no techRangeSummary")
    if "상장" not in summary.group(1):
        text = (f"1년 최저 ${w['lo']:.2f} ({ym(w['lo_date'])}) → 1년 최고 ${w['hi']:.2f} ({ym(w['hi_date'])}) "
                f"→ 현재 ${w['last']:.2f}")
        html = sub1(html, r'(id="techRangeSummary">)[^<]*(<)', lambda m: f"{m.group(1)}{text}{m.group(2)}", "range summary")

    # --- MA box: each row's latest value and whether the close is above it ---
    ma_row = re.compile(r'(<div class="ma-row"><span class="ma-name"><span class="ma-dot" style="background:var\(--ma(\d+)\)">'
                        r'</span>[^<]+</span><div style="display:flex;align-items:center;gap:10px;"><span class="ma-val">)'
                        r'\$[\d,.]+(</span><span class="ma-status )status-(?:above|below)">([^<]+)(</span>)')

    def ma_repl(m):
        v = ma_last.get("MA" + m.group(2))
        if v is None:
            raise EditError(f"MA box shows MA{m.group(2)}, which the card has no array for")
        above = close >= v
        text = m.group(4).replace("하회", "상회") if above else m.group(4).replace("상회", "하회")
        return f"{m.group(1)}{money(v)}{m.group(3)}{'status-above' if above else 'status-below'}\">{text}{m.group(5)}"
    html, n = ma_row.subn(ma_repl, html)
    if n != html.count('<div class="ma-row">'):
        raise EditError(f"MA box: {html.count('<div class=\"ma-row\">')} rows, {n} in the expected format")

    # --- scorecard ---
    if tech and not tech.get("insufficientHistory") and '<div class="scorecard-score">' in html:
        # some cards also carry a fundamental scorecard with the same classes;
        # edit only the technical one
        full = html
        seg_start, seg_end = tech_segment(full)
        html = full[seg_start:seg_end]
        raw = tech["rawScore"]
        html = sub1(html, r'(<div class="scorecard-score"><span class="num">)\d+(</span>)',
                    lambda m: f"{m.group(1)}{raw}{m.group(2)}", "score")
        # text and colour both follow displayGrade, so hysteresis can't split them
        grade = tech.get("displayGrade")
        if grade not in GRADE_CLASS:
            raise EditError(f"unknown displayGrade {grade!r}")
        cls, tier = GRADE_CLASS[grade], GRADE_TEXT[grade]
        html = sub1(html, r'<div class="scorecard-grade grade-[a-z]+">[^<]+</div>',
                    lambda m: f'<div class="scorecard-grade {cls}">{tier}</div>', "grade")
        html = sub1(html, r'(<div class="scorecard-bar-fill" style="width:)[\d.]+(%;")',
                    lambda m: f"{m.group(1)}{raw}{m.group(2)}", "score bar")
        html = sub1(html, r'(가격·거래량 기반 기술 상태 점수 \(모델 v1\.0\.0 · )\d{4}-\d{2}-\d{2}( 기준\))',
                    lambda m: f"{m.group(1)}{tech['asOf']}{m.group(2)}", "scorecard date")
        if re.search(r"<span>기준일 \d{4}-\d{2}-\d{2}</span>", html):
            html = sub1(html, r"(<span>기준일 )\d{4}-\d{2}-\d{2}(</span>)",
                        lambda m: f"{m.group(1)}{tech['asOf']}{m.group(2)}", "scorecard footer date")

        ts, mo, p52 = tech["trendStructure"], tech["momentum"], tech["position52w"]
        met = sum(bool(v) for v in ts["conditions"].values())
        total = len(ts["conditions"])
        ts_desc = (f"MA50/150/200 배열 조건 {total}개 전부 충족" if met == total else
                   f"MA50/150/200 배열 조건 {total}개 전부 미충족" if met == 0 else
                   f"MA50/150/200 배열 조건 {total}개 중 {met}개 충족")
        roc = mo.get("weightedRocPct")
        mo_desc = "모멘텀 계산 불가(이력 부족)" if roc is None else f"최근 3개월~1년 가중 수익률 {'+' if roc >= 0 else ''}{roc:.2f}%"
        p_desc = f"저점 대비 +{p52['riseFromLowPct']:.2f}%, 고점 대비 -{p52['drawdownFromHighPct']:.2f}%"
        for label, part, desc in (("추세구조", ts, ts_desc), ("절대모멘텀", mo, mo_desc), ("52주위치", p52, p_desc)):
            pat = (rf'(<div class="subscore-label"><span>{label}</span><span class="subscore-max">)\d+/\d+'
                   r'(</span></div>\s*<div class="subscore-val">)\d+'
                   r'(</div>\s*<div class="subscore-bar"><div class="subscore-bar-fill" style="width:)[\d.]+'
                   r'(%;"></div></div>\s*<div class="subscore-desc">)[^<]*(</div>)')
            html = sub1(html, pat, lambda m, p=part, d=desc: (f"{m.group(1)}{p['score']}/{p['max']}{m.group(2)}"
                                                             f"{p['score']}{m.group(3)}{pct_width(p['score'], p['max'])}"
                                                             f"{m.group(4)}{d}{m.group(5)}"), f"subscore {label}")

        html = render_flags(html, list(tech.get("riskFlagsShown") or []), notes)

        badge = re.search(r'(<div class="scorecard-noOpp-inline">)([^<]+)(</div>)', html)
        if not badge:
            raise EditError("no breakout badge in the technical scorecard")
        if badge:
            ab = (breakout or {}).get("activeBreakout")
            text = badge.group(2)
            if ab:
                text = f"🎯 돌파 신호 발생 ({dot(ab['eventDate'])} · 거래량 {ab['volumeRatio']:.1f}배)"
            elif "없음" not in text:
                text = "🎯 돌파 신호 없음"
            if text != badge.group(2):
                html = html[:badge.start(2)] + text + html[badge.end(2):]
                notes.append(f"breakout badge -> {text}")
        html = full[:seg_start] + html + full[seg_end:]

        # 11 cards' fundamental scorecard quotes "기술 N · 평균 X", X = (fundamental + N) / 2.
        # Follow the new N only where the card's current X fits that formula.
        mentions = list(re.finditer(r"기술 (\d+) · 평균 (\d+(?:\.\d+)?)", html))
        if len(mentions) > 1:
            raise EditError(f"fundamental scorecard: {len(mentions)} '기술 N · 평균' mentions")
        if len(mentions) == 1:
            m = mentions[0]
            block = next((html[s:e] for s, e in scorecard_blocks(html) if s <= m.start() < e), "")
            fm = re.search(r'scorecard-score"><span class="num">([\d.]+)<', block)
            half = lambda x: Decimal(x).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
            if fm and half((Decimal(fm.group(1)) + int(m.group(1))) / 2) == Decimal(m.group(2)):
                html = html[:m.start()] + f"기술 {raw} · 평균 {half((Decimal(fm.group(1)) + raw) / 2)}" + html[m.end():]
            else:
                raise EditError("fundamental scorecard's '기술 N · 평균 X' doesn't fit (fundamental+N)/2")

    # --- as-of label ---
    if 'class="asof-line"' in html:
        html = sub1(html, r'(<div class="asof-line"[^>]*>가격·기술지표: )\d{4}\.\d{2}\.\d{2}',
                    lambda m: f"{m.group(1)}{dot(last[0])}", "as-of label")
    else:
        cap_part = " · 시가총액: SEC 공시 주식수 기준" if shares else ""
        label = (f'<div class="asof-line" style="{ASOF_STYLE}">가격·기술지표: {dot(last[0])} 종가 기준 갱신 · '
                 f'분석 문장·밸류에이션: {dot(card_asof)} 기준{cap_part}</div>\n')
        html = sub1(html, r'(?=<div class="box-key">)', lambda m: label, "as-of label anchor")
    return html


def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.chmod(tmp, 0o644)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def commit(card_path, html, state_path, tech):
    """State file first, then the card, each replaced atomically. The state is
    rewritten whenever it differs, so one lost after a failed run comes back
    even when the card itself is already current."""
    if tech is not None:
        text = json.dumps(tech, ensure_ascii=False, indent=2) + "\n"
        if not state_path.exists() or state_path.read_text(encoding="utf-8") != text:
            atomic_write(state_path, text)
    if html is not None:
        atomic_write(card_path, html)


def node_check(html):
    node = shutil.which("node")
    if not node:
        return None
    for i, js in enumerate(re.findall(r"<script>(.*?)</script>", html, re.S)):
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(js)
            path = f.name
        r = subprocess.run([node, "--check", path], capture_output=True, text=True)
        os.unlink(path)
        if r.returncode != 0:
            return f"inline script {i}: {r.stderr.strip()[-200:]}"
    return ""


def update_card(path, entry, session, fixtures, now_et, state_dir, tech_config, breakout_config):
    ticker = entry["ticker"]
    old_html = path.read_text(encoding="utf-8")
    lines, arrays = parse_card_arrays(old_html)
    notes = []
    for kind in arrays:
        if len(arrays[kind]["tokens"]) != len(arrays["DAILY"]["tokens"]):
            raise EditError(f"{kind} length {len(arrays[kind]['tokens'])} != DAILY {len(arrays['DAILY']['tokens'])}")

    last_card_date = bar_values(arrays["DAILY"]["tokens"][-1])[0]
    # the card follows the homepage: stop at this ticker's own recorded session
    # (a stale ticker keeps its last good session; nothing to follow otherwise)
    p = entry["price"]
    if p.get("status") in ("unavailable", "suspicious") or not p.get("session") or p.get("close") is None:
        raise Hold(f"homepage price is {p.get('status')} ({p.get('statusReason', 'no session')}) - card left as is")
    target = p["session"]
    rng = fetch_range(last_card_date, target)
    fetched, splits = fetch_bars(entry.get("yahooSymbol", ticker), rng, fixtures, now_et, target)
    if not fetched:
        raise ValueError("no completed bars fetched")
    changed, replaced, appended, extra = sync_bars(arrays, fetched, splits, notes)
    if extra:  # it would sit inside every later MA window
        raise Hold(f"card has session(s) Yahoo doesn't: {', '.join(extra[:5])}")
    computed = extend_mas(arrays, changed)
    trimmed = trim_front(arrays)

    tokens = arrays["DAILY"]["tokens"]
    bars = [bar_values(t) for t in tokens]
    for a, b in zip(bars, bars[1:]):
        if b[0] <= a[0]:
            raise EditError(f"dates not strictly increasing at {b[0]}")
    if bars[-1][0] != target:
        raise Hold(f"no completed Yahoo bar for {target} yet (card ends {bars[-1][0]})")
    if abs(p["close"] - bars[-1][4]) > 0.005:
        raise EditError(f"last close {bars[-1][4]} != homepage close {p['close']} for {target}")
    check_from = max(0, (changed if changed is not None else len(bars)) - trimmed)
    for d, o, h, l, c, v in bars[check_from:]:  # every bar this run wrote
        if min(o, h, l, c) <= 0 or v < 0 or h + 0.011 < max(o, c) or l - 0.011 > min(o, c):
            raise EditError(f"implausible bar {d}: o{o} h{h} l{l} c{c} v{v}")

    pdata = price_data(ticker, tokens)
    state_path = state_dir / f"{ticker}.json"
    prev_state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else None
    tech = compute_signal(ticker, pdata, tech_config, prev_state)
    breakout = compute_active_breakout(ticker, pdata, breakout_config)

    for kind, a in arrays.items():
        lines[a["line"]] = a["head"] + "[" + ",".join(a["tokens"]) + "]" + a["tail"]
    html = "\n".join(lines)
    shares = entry["shares"].get("usEquivalent")
    if entry.get("listing", {}).get("type") == "adr":
        # ADR cards quote the ordinary-share market cap (SKHY: KRX basis, and its
        # prose is built on the ADR premium), so an ADR-price cap would contradict it
        shares = None
        notes.append("ADR card: header market cap is on the ordinary-share basis - left as is")
    elif not shares:
        notes.append("no SEC share count - market cap left as is")
    ma_last = {k: float(a["tokens"][-1]) for k, a in arrays.items() if k != "DAILY" and a["tokens"][-1] != "null"}
    html = render(html, ticker, tokens, tech, breakout, shares, entry["cardAsOf"], notes, ma_last)

    if html == old_html:  # tech is still returned so a missing state file gets repaired
        return "unchanged", bars[-1][0], {"replaced": 0, "appended": 0}, notes, None, tech
    if f'<div class="price-main">{money(bars[-1][4])}</div>' not in html:
        raise EditError("header price != last close after rendering")
    div_delta = (html.count("<div") - html.count("</div>")) - (old_html.count("<div") - old_html.count("</div>"))
    if div_delta != 0:
        raise EditError(f"<div> balance changed by {div_delta}")
    err = node_check(html)
    if err:
        raise EditError(f"node --check failed: {err}")
    if err is None:
        raise EditError("node not found - can't check the inline scripts")
    counts = {"replaced": replaced, "appended": appended, "trimmed": trimmed, "maComputed": computed,
              "score": tech.get("rawScore")}
    return "updated", bars[-1][0], counts, notes, html, tech


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", default=None, help="comma-separated subset (pilot)")
    ap.add_argument("--cards-dir", default=str(ROOT))
    ap.add_argument("--data", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--state-dir", default=str(ROOT / "site_data" / "tech_state"))
    ap.add_argument("--status", default=str(ROOT / "site_data" / "card_status.json"))
    ap.add_argument("--fixtures", default=None)
    ap.add_argument("--now", default=None)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--out-dir", default=None, help="also save updated cards here (for review diffs)")
    args = ap.parse_args()

    now_et = datetime.fromisoformat(args.now).astimezone(fp.ET) if args.now else datetime.now(fp.ET)
    data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    session = data.get("priceSession")
    if not session:
        sys.exit("stocks.json has no priceSession - run fetch_prices.py first")
    wanted = {t.strip().upper() for t in args.tickers.split(",")} if args.tickers else None
    if wanted:
        unknown = wanted - {t["ticker"] for t in data["tickers"]}
        if unknown:
            sys.exit(f"unknown ticker(s) in --tickers: {', '.join(sorted(unknown))} - nothing written")
    cards_dir, state_dir, status_path = Path(args.cards_dir), Path(args.state_dir), Path(args.status)
    tech_config = json.loads(TECH_CONFIG.read_text(encoding="utf-8"))
    breakout_config = json.loads(BREAKOUT_CONFIG.read_text(encoding="utf-8"))
    status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.exists() else {"cards": {}}
    status_before = json.dumps(status, sort_keys=True)

    print(f"target session {session} (now {now_et:%Y-%m-%d %H:%M} ET)")
    results, net_failures = {}, 0
    for entry in data["tickers"]:
        t = entry["ticker"]
        if wanted and t not in wanted:
            continue
        path = cards_dir / entry["href"]
        if net_failures >= fp.MAX_NET_FAILURES:  # Yahoo is down - don't spend the job's time limit retrying
            st, last, counts, notes, html, tech = ("failed", None, {}, [f"skipped after {fp.MAX_NET_FAILURES} "
                                                   "consecutive network failures"], None, None)
        else:
            try:
                st, last, counts, notes, html, tech = update_card(path, entry, session, args.fixtures, now_et,
                                                                  state_dir, tech_config, breakout_config)
                net_failures = 0
                if args.write:
                    commit(path, html if st == "updated" else None, state_dir / f"{t}.json", tech)
            except Hold as e:
                st, last, counts, notes, html, tech = "held", None, {}, [str(e)], None, None
                net_failures = 0
            except Exception as e:  # one card's problem must not stop the rest
                st, last, counts, notes, html, tech = "failed", None, {}, [f"{type(e).__name__}: {e}"], None, None
                net_failures = net_failures + 1 if fp.is_network_error(e) else 0
        results[t] = (st, last, counts, notes)
        print(f"{t:5} {st:9} last={last} {counts}" + ("".join(f"\n        - {n}" for n in notes)))
        if args.out_dir and st == "updated":  # pilot review: save the result elsewhere, touch nothing
            Path(args.out_dir).mkdir(parents=True, exist_ok=True)
            (Path(args.out_dir) / path.name).write_text(html, encoding="utf-8")
        prev = status["cards"].get(t, {})
        status["cards"][t] = {
            "status": st, "reasons": notes,
            "lastBar": last or prev.get("lastBar"),
            "lastUpdated": (datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                            if st == "updated" and args.write else prev.get("lastUpdated")),
        }

    summary = {s: sum(1 for r in results.values() if r[0] == s) for s in ("updated", "unchanged", "held", "failed")}
    print(f"summary: {summary}")
    if not args.write:
        print("Dry run - pass --write to update the cards")
        return
    status["priceSession"] = session
    # rewrite only on a real change, so a quiet day (holiday) leaves nothing to commit
    if json.dumps(status, sort_keys=True) != status_before:
        status["generatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        atomic_write(status_path, json.dumps(status, ensure_ascii=False, indent=2) + "\n")
        print(f"Wrote {status_path}")


if __name__ == "__main__":
    main()
