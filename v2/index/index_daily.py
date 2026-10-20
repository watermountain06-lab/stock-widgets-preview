#!/usr/bin/env python3
"""S&P 500 지수 카드(preview 전용, 2026-10-20) — 가격·기간별 수익률·월별 등락률·가격 사건.

자료: Yahoo ^GSPC 일봉 종가(홈 시장 지표 macro.json과 같은 출처). FRED SP500(S&P Dow Jones Indices 제공, 최근 10년)과
겹치는 날짜를 모두 대조한다 — 날짜 집합이 같아야 하고, 최근 250세션은 소수 둘째 자리까지 같아야 하며, 그 앞은 0.2% 안이어야 한다.
계산·표시는 FRED 대조 구간(첫 FRED 날짜부터)의 종가만 쓴다 — 그래서 "사상 최고"가 아니라 "그날 이후 최고"다(2026-10-20 dr r3,
사용자 결정). FRED는 하루 늦게 올라오므로 S 하루는 "대조 전"으로 적고 쓴다. 어긋나거나, FRED에 닿지 못하거나, FRED 값이 이상하거나,
FRED가 직전 세션까지 없으면 카드를 "보류"로 쓴다.

세션: 홈 카드 세션 P와 직전 세션(site_data/stocks.json priceSession, 종목들의 prevSession)까지의 종가만 쓴다. Yahoo 마지막 두
종가 날짜가 그 둘과 다르면 보류.
가격 지수라 배당은 빠진다. 사건은 가격으로만 감지하고 원인 설명을 붙이지 않는다.

    python3 v2/index/index_daily.py [--out-root DIR] [--yahoo FILE] [--fred FILE] [--stocks FILE]
"""
import argparse
import csv
import html
import io
import json
import math
import os
import sys
import time
import traceback
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ET = timezone(timedelta(hours=-5))   # 날짜만 쓴다 — Yahoo 일봉 timestamp(개장 시각)는 서머타임과 무관하게 같은 날짜
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC?period1=0&period2={end}&interval=1d"
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SP500"
FRED_API = ("https://api.stlouisfed.org/fred/series/observations?series_id=SP500&api_key={key}"
            "&file_type=json&observation_start={start}")
UA = "Mozilla/5.0 (stock-widgets-preview index card)"
RECENT_EXACT = 250       # 최근 250세션은 소수 둘째 자리까지 같아야
OLD_TOL = 0.002          # 그 앞은 0.2% 안
BIG_MOVE = 0.03          # 하루 ±3% 이상
DRAWDOWNS = (0.10, 0.20)
PERIODS = (("1개월", 1), ("6개월", 6), ("1년", 12), ("3년", 36), ("5년", 60))
YEARS_SHOWN = 10
REASON_TEXT = {"fetch_fail": "Yahoo 시세를 받지 못함", "date_mismatch": "종가 날짜가 홈 세션과 다름",
               "cross_check": "FRED(S&P DJI) 대조 불일치", "run_fail": "스크립트 실행 실패",
               "short": "시세 기간이 모자람", "no_session": "홈 세션을 읽지 못함", "cross_unavailable": "FRED(S&P DJI) 대조 못 함"}
EPS = 1e-9               # 경계(정확히 −10%·±3%)에서 부동소수점 오차로 사건을 놓치지 않게


class Hold(Exception):
    def __init__(self, reason, detail=""):
        super().__init__(reason)
        self.reason, self.detail = reason, detail


def http_get(url, timeout=60, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8")
        except Exception as e:   # noqa: BLE001 — 재시도 뒤 호출자가 분류한다
            last = e
            time.sleep(2 * (i + 1))
    raise last


def parse_yahoo(text):
    """[(date iso, close)] 오래된 순. 빈 종가는 버린다. 같은 날짜가 두 번이면 뒤의 것."""
    body = json.loads(text).get("chart") or {}
    if not body.get("result"):
        raise ValueError("Yahoo: no chart result")
    r = body["result"][0]
    by = {}
    for ts, c in zip(r.get("timestamp") or [], r["indicators"]["quote"][0]["close"]):
        if c is None or not math.isfinite(c) or c <= 0:
            continue
        by[datetime.fromtimestamp(ts, ET).date().isoformat()] = float(c)
    return sorted(by.items())


def parse_fred(text):
    t = text.lstrip()
    if t.startswith("{"):
        obs = json.loads(t).get("observations") or []
        pairs = [(o["date"], o.get("value")) for o in obs]
    else:
        pairs = [(r[0], r[1]) for r in list(csv.reader(io.StringIO(text)))[1:] if len(r) == 2]
    out = {}
    for k, v in pairs:
        if v in (None, "", "."):
            continue            # FRED가 휴장일에 비워 두는 칸
        x = float(v)
        if not math.isfinite(x) or x <= 0:
            raise ValueError(f"FRED {k}: 값이 이상함")   # → 대조 못 함 → 보류
        out[k] = x
    return out


def fetch_fred():
    key = os.environ.get("FRED_API_KEY", "").strip()
    if key:   # 키는 URL에만 쓰고 출력하지 않는다(예외 메시지도 버린다)
        start = (date.today() - timedelta(days=11 * 366)).isoformat()
        try:
            return http_get(FRED_API.format(key=urllib.parse.quote(key, safe=""), start=start))
        except Exception:   # noqa: BLE001 — 키가 틀리거나 API가 막히면 공개 CSV로
            pass
    return http_get(FRED_CSV)


# ---------- 계산 ----------

def d(s):
    return date.fromisoformat(s)


def minus_months(day, k):
    y, m = divmod(day.year * 12 + day.month - 1 - k, 12)
    m += 1
    last = (date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)).day
    return date(y, m, min(day.day, last))


def close_on_or_before(series, day):
    """day 이하 마지막 (날짜, 종가). 없으면 None."""
    lo, hi, iso = 0, len(series), day.isoformat()
    while lo < hi:
        mid = (lo + hi) // 2
        if series[mid][0] <= iso:
            lo = mid + 1
        else:
            hi = mid
    return series[lo - 1] if lo else None


def cross_check(series, fred, S, prevP):
    """(상태, 설명). 상태: ok | mismatch | unavailable — ok만 게시한다.
    prevP = 홈 시세 파일이 적은 S 직전 세션(종목 131개의 prevSession). FRED는 적어도 prevP까지 있어야 하고, 그 구간의 날짜 집합이
    같아야 한다 — 그러면 대조 전인 값은 S 하루뿐이고, S 직전 날짜가 prevP인지는 compute가 따로 본다."""
    if not fred:
        return "unavailable", "FRED에 닿지 못함"
    ys = dict(series)
    f_days = sorted(k for k in fred if k <= S)
    if len(f_days) < RECENT_EXACT:
        return "unavailable", f"FRED 날짜가 {len(f_days)}개뿐"
    lo, hi = f_days[0], f_days[-1]
    if hi < prevP:
        return "unavailable", f"FRED가 {hi}까지만 있음 — 직전 세션 {prevP}까지 없다"
    lag = hi < S
    only_f = [k for k in f_days if k not in ys]
    only_y = [k for k, _ in series if lo <= k <= hi and k not in fred]
    if only_f or only_y:
        return "mismatch", f"날짜 불일치: Yahoo에 없는 날 {len(only_f)}일, FRED에 없는 날 {len(only_y)}일 (첫 날 {(only_f or only_y)[0]})"
    recent = f_days[-RECENT_EXACT:]
    bad_recent = [k for k in recent if abs(round(ys[k], 2) - fred[k]) > 0.0051]
    old_diffs = [(k, abs(ys[k] / fred[k] - 1)) for k in f_days[:-RECENT_EXACT]]
    bad_old = [k for k, r in old_diffs if r > OLD_TOL]
    small = sum(1 for k, r in old_diffs if abs(round(ys[k], 2) - fred[k]) > 0.0051)
    if bad_recent or bad_old:
        return "mismatch", f"최근 {RECENT_EXACT}세션 불일치 {len(bad_recent)}일, 그 앞 0.2% 초과 {len(bad_old)}일 (첫 날 {(bad_recent or bad_old)[0]})"
    worst = max((r for _, r in old_diffs), default=0.0)
    return "ok", (f"FRED SP500과 {len(f_days)}일({lo}~{hi}) 대조: 날짜 모두 같음, 최근 {RECENT_EXACT}세션 값 모두 같음, "
                  f"그 앞 {small}일이 소수 둘째 자리에서 다름(최대 {worst * 100:.2f}%)"
                  + (f" · 마지막 {S} 종가는 FRED 미게시로 대조 전(Yahoo 값)" if lag else ""))


def returns(series, S):
    sd, sc = d(S), series[-1][1]
    out = []
    for label, k in PERIODS:
        b = close_on_or_before(series, minus_months(sd, k))
        if b is None:
            raise Hold("short", f"{label} 기준 종가 없음")
        r = sc / b[1] - 1
        row = {"label": label, "months": k, "base": b[0], "baseClose": round(b[1], 2), "ret": r}
        if k >= 36:
            row["annual"] = (1 + r) ** (12 / k) - 1
        out.append(row)
    b = close_on_or_before(series, date(sd.year - 1, 12, 31))
    out.append({"label": "YTD", "months": None, "base": b[0], "baseClose": round(b[1], 2), "ret": sc / b[1] - 1})
    return out


def month_ends(series):
    """{(y, m): (마지막 날짜, 종가)}"""
    me = {}
    for k, c in series:
        me[(int(k[:4]), int(k[5:7]))] = (k, c)
    return me


def month_done(S):
    """S가 그 달 마지막 평일이면 끝난 달로 본다(월말 휴장일은 모른다 — 그날은 다음 세션 실행에서 풀린다)."""
    n = d(S) + timedelta(days=1)
    while n.weekday() >= 5:
        n += timedelta(days=1)
    return n.month != d(S).month


def monthly(series, S):
    me = month_ends(series)
    sy, sm = int(S[:4]), int(S[5:7])
    open_m = not month_done(S)
    years = list(range(sy - YEARS_SHOWN + 1, sy + 1))
    rows = []
    for y in years:
        cells = []
        for m in range(1, 13):
            prev = me.get((y - (m == 1), 12 if m == 1 else m - 1))
            cur = me.get((y, m))
            if (y, m) > (sy, sm) or not prev or not cur:
                cells.append(None)
                continue
            cells.append({"ret": cur[1] / prev[1] - 1, "partial": open_m and (y, m) == (sy, sm)})
        pe, ce = me.get((y - 1, 12)), (me.get((y, 12)) if y < sy else (S, series[-1][1]))
        annual = {"ret": ce[1] / pe[1] - 1, "partial": y == sy and (sm < 12 or open_m)} if pe and ce else None
        rows.append({"year": y, "months": cells, "annual": annual})
    stats = []
    for m in range(12):
        vals = [r["months"][m]["ret"] for r in rows if r["months"][m] and not r["months"][m]["partial"]]
        stats.append({"mean": sum(vals) / len(vals), "up": sum(v > 0 for v in vals), "n": len(vals)} if vals else None)
    last12 = []
    y, m = sy, sm
    for _ in range(12):
        prev, cur = me.get((y - (m == 1), 12 if m == 1 else m - 1)), me.get((y, m))
        last12.append({"ym": f"{y}-{m:02d}", "ret": cur[1] / prev[1] - 1, "partial": open_m and (y, m) == (sy, sm)})
        y, m = (y - 1, 12) if m == 1 else (y, m - 1)
    return {"rows": rows, "stats": stats, "last12": last12[::-1]}


def events(series, S):
    """가격 사건(최근 10년, series 첫 날 이후). 최고·고점은 series 안에서만 본다 — compute가 FRED 대조 구간만 넘긴다.
    회복은 −10% 이상 빠진 뒤 전고점 이상으로 돌아온 첫날."""
    start = minus_months(d(S), 12 * YEARS_SHOWN).isoformat()
    out, peak, peak_day, hit, trough = [], 0.0, None, set(), 0.0
    prev = None
    for k, c in series:
        show = k >= start
        ch = c / prev - 1 if prev is not None else 0.0
        if prev is not None and show and abs(ch) >= BIG_MOVE - EPS:
            out.append({"date": k, "close": round(c, 2), "chg": ch, "type": "up" if ch > 0 else "down",
                        "text": f"하루 {'상승' if ch > 0 else '하락'} {abs(ch) * 100:.2f}%"})
        if hit and c >= peak * (1 - EPS):
            if show:
                out.append({"date": k, "close": round(c, 2), "chg": ch, "type": "recover",
                            "text": f"전고점 회복 — 고점 {kdate(peak_day)}, 최대 낙폭 {pct(trough)}"})
            hit, trough = set(), 0.0
        if c > peak:
            if show and peak_day:
                out.append({"date": k, "close": round(c, 2), "chg": ch, "type": "ath", "text": f"{kdate(series[0][0])} 이후 최고 종가"})
            peak, peak_day, hit, trough = c, k, set(), 0.0
        else:
            dd = c / peak - 1
            trough = min(trough, dd)
            for t in DRAWDOWNS:
                if dd <= -t + EPS and t not in hit:
                    hit.add(t)
                    if show:
                        out.append({"date": k, "close": round(c, 2), "chg": ch, "type": "dd",
                                    "text": f"고점 대비 −{int(t * 100)}% 진입 — 고점 {kdate(peak_day)}"})
        prev = c
    return out[::-1]


def weekly(points):
    """주마다 마지막 종가."""
    by = {}
    for k, c in points:
        y, w, _ = d(k).isocalendar()
        by[(y, w)] = (k, c)
    return [by[x] for x in sorted(by)]


def chart_series(series, S):
    """기간별 수익률과 같은 기준점(목표일 이하 마지막 종가)에서 시작한다 — 캡션 등락률 = 수익률 칸."""
    sd, out = d(S), {}
    for key, k in (("1년", 12), ("5년", 60), ("10년", 120)):
        b = close_on_or_before(series, minus_months(sd, k)) or series[0]   # 10년 기준일이 대조 구간 앞이면 구간 첫 날
        pts = [p for p in series if p[0] > b[0]]
        if k > 12:
            pts = weekly(pts)
            if pts[-1][0] != S:
                pts[-1] = series[-1]
        out[key] = [b] + pts
    return out


def compute(series, fred, P, prevP):
    if not P or not prevP:
        raise Hold("no_session", "홈 시세 파일에서 세션을 읽지 못함")
    series = [p for p in series if p[0] <= P]
    if len(series) < 260 * 5:
        raise Hold("short", f"종가 {len(series)}개")
    S = series[-1][0]
    if S != P or series[-2][0] != prevP:
        raise Hold("date_mismatch", f"마지막 두 종가 {series[-2][0]}·{S}, 홈 세션 {prevP}·{P}")
    cc, cc_text = cross_check(series, fred, S, prevP)
    if cc != "ok":
        raise Hold("cross_check" if cc == "mismatch" else "cross_unavailable", cc_text)
    series = [p for p in series if p[0] >= min(fred)]   # 대조된 구간만(그 앞 Yahoo 값은 쓰지 않는다)
    close, prev = series[-1][1], series[-2][1]
    b1 = close_on_or_before(series, minus_months(d(S), 12))
    yr = [p for p in series if p[0] >= b1[0]]   # 1년 수익률·1년 그림과 같은 창(기준일 포함), 52주 아님
    hi = max(yr, key=lambda p: p[1])
    lo = min(yr, key=lambda p: p[1])
    ath = max(series, key=lambda p: p[1])
    return {"status": "ok", "S": S, "builtFor": P, "close": round(close, 2), "prevSession": series[-2][0],
            "chg": close / prev - 1, "hi1y": {"date": hi[0], "close": round(hi[1], 2), "from": close / hi[1] - 1},
            "lo1y": {"date": lo[0], "close": round(lo[1], 2), "from": close / lo[1] - 1},
            "ath": {"date": ath[0], "close": round(ath[1], 2), "from": close / ath[1] - 1}, "since": series[0][0],
            "returns": returns(series, S), "monthly": monthly(series, S), "events": events(series, S),
            "chart": {k: [[a, round(b, 2)] for a, b in v] for k, v in chart_series(series, S).items()},
            "crossCheck": {"status": cc, "text": cc_text}}


# ---------- 화면 ----------

MINUS = "−"


def pct(x, dg=1, sign=True):
    if x is None:
        return "—"
    s = f"{abs(x) * 100:.{dg}f}%"
    return (("+" if x > 0 else MINUS if x < 0 else "") if sign else "") + s


def num(x):
    return f"{x:,.2f}"


def cls(x):
    return "up" if x > 0 else "down" if x < 0 else ""


def kdate(s):
    return s.replace("-", ".")


def svg_chart(points, key):
    W, H, L, R, T, B = 800, 260, 58, 12, 12, 26
    vals = [c for _, c in points]
    lo, hi = min(vals), max(vals)
    pad = (hi - lo) * 0.06 or 1
    lo, hi = lo - pad, hi + pad
    n = len(points)
    X = lambda i: L + (W - L - R) * i / max(n - 1, 1)
    Y = lambda v: T + (H - T - B) * (1 - (v - lo) / (hi - lo))
    path = "M" + " L".join(f"{X(i):.1f},{Y(c):.1f}" for i, (_, c) in enumerate(points))
    area = path + f" L{X(n - 1):.1f},{H - B} L{L},{H - B} Z"
    g = []
    step = 10 ** math.floor(math.log10((hi - lo) / 4))
    step = min((s * step for s in (1, 2, 2.5, 5, 10)), key=lambda s: abs((hi - lo) / s - 4))
    v = math.ceil(lo / step) * step
    while v <= hi:
        g.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>'
                 f'<text class="ax" x="{L - 6}" y="{Y(v) + 4:.1f}" text-anchor="end">{v:,.0f}</text>')
        v += step
    # x축: 1년은 분기 첫 달, 5·10년은 해 바뀜
    seen = None
    for i, (k, _) in enumerate(points):
        tag = k[:4] if key != "1년" else (k[:7] if int(k[5:7]) in (1, 4, 7, 10) else None)
        if tag and tag != seen and i > 0 and (seen is not None or key == "1년"):
            label = k[:4] if key != "1년" else f"{k[2:4]}.{k[5:7]}"
            g.append(f'<line class="tick" x1="{X(i):.1f}" x2="{X(i):.1f}" y1="{T}" y2="{H - B}"/>'
                     f'<text class="ax" x="{X(i):.1f}" y="{H - 8}" text-anchor="middle">{label}</text>')
        if tag:
            seen = tag
        elif seen is None:
            seen = ""
    first, last = points[0][1], points[-1][1]
    c = cls(last - first)
    return (f'<svg viewBox="0 0 {W} {H}" class="chart {c}" role="img" aria-label="S&amp;P 500 {key} 종가 '
            f'{num(first)}에서 {num(last)}">{"".join(g)}<path class="area" d="{area}"/><path class="line" d="{path}"/>'
            f'<circle class="dot" cx="{X(n - 1):.1f}" cy="{Y(last):.1f}" r="3.5"/></svg>'
            f'<p class="small">{kdate(points[0][0])} {num(first)} → {kdate(points[-1][0])} {num(last)} '
            f'(<span class="{c}">{pct(last / first - 1)}</span>){" · 주마다 마지막 종가" if key != "1년" else " · 일별 종가"}</p>')


def heat_cell(cell):
    if cell is None:
        return '<td class="hc empty"></td>'
    r = cell["ret"]
    a = min(abs(r) / 0.08, 1)   # ±8%에서 가장 진함
    style = f' style="--a:{0.12 + 0.78 * a:.2f}"'
    mark = ' title="진행 중"' if cell["partial"] else ""
    return (f'<td class="hc {cls(r)}{" strong" if a > 0.55 else ""}{" partial" if cell["partial"] else ""}"{style}{mark}>'
            f'<span>{pct(r, 1)}</span></td>')


def render_monthly(m):
    head = "".join(f"<th>{i}월</th>" for i in range(1, 13))
    body = []
    for row in m["rows"][::-1]:
        a = row["annual"]
        body.append(f'<tr><th class="yr">{row["year"]}</th>' + "".join(heat_cell(c) for c in row["months"])
                    + (f'<td class="annual {cls(a["ret"])}">{pct(a["ret"])}{"*" if a["partial"] else ""}</td>' if a else "<td></td>")
                    + "</tr>")
    stat_mean = "".join(f'<td class="st {cls(s["mean"])}">{pct(s["mean"])}</td>' if s else "<td></td>" for s in m["stats"])
    stat_up = "".join(f'<td class="st">{s["up"]}/{s["n"]}</td>' if s else "<td></td>" for s in m["stats"])
    table = (f'<div class="scroll"><table class="heat"><thead><tr><th></th>{head}<th>연간</th></tr></thead>'
             f'<tbody>{"".join(body)}</tbody><tfoot><tr><th>평균</th>{stat_mean}<td></td></tr>'
             f'<tr><th>상승</th>{stat_up}<td></td></tr></tfoot></table></div>')
    mx = max(abs(x["ret"]) for x in m["last12"]) or 0.01
    bars = []
    for x in m["last12"]:
        h = abs(x["ret"]) / mx * 50
        bars.append(f'<div class="b12{" partial" if x["partial"] else ""}" title="{x["ym"]} {pct(x["ret"], 2)}">'
                    f'<span class="v {cls(x["ret"])}">{pct(x["ret"], 1)}</span>'
                    f'<span class="col"><i class="{cls(x["ret"])}" style="height:{h:.1f}%;'
                    f'{"bottom:50%" if x["ret"] >= 0 else "top:50%"}"></i></span>'
                    f'<span class="m">{x["ym"][2:4]}.{x["ym"][5:]}</span></div>')
    return table, "".join(bars)


def render_events(evs):
    years = sorted({e["date"][:4] for e in evs}, reverse=True)
    counts = {}
    for e in evs:
        counts.setdefault(e["date"][:4], {}).setdefault(e["type"], 0)
        counts[e["date"][:4]][e["type"]] += 1
    blocks = []
    for i, y in enumerate(years):
        rows = "".join(
            f'<tr class="ev ev-{e["type"]}"><td class="num">{kdate(e["date"][5:])}</td><td class="num">{num(e["close"])}</td>'
            f'<td class="num {cls(e["chg"])}">{pct(e["chg"], 2)}</td><td><span class="evtag t-{e["type"]}">{e["text"]}</span></td></tr>'
            for e in evs if e["date"][:4] == y)
        c = counts[y]
        sm = " · ".join(f"{lab} {c[t]}" for t, lab in (("up", "급등"), ("down", "급락"), ("dd", "낙폭"),
                                                        ("recover", "회복"), ("ath", "최고")) if c.get(t))
        has = [h for h, ts in (("move", ("up", "down")), ("dd", ("dd", "recover")), ("ath", ("ath",))) if any(c.get(t) for t in ts)]
        if "move" in has or "dd" in has:
            has.append("main")
        blocks.append(f'<details class="year {" ".join("has-" + h for h in has)}"{" open" if i < 2 else ""}><summary><b>{y}</b> <span class="small">{sm}</span></summary>'
                      f'<div class="scroll"><table><thead><tr><th>날짜</th><th>종가</th><th>하루 등락</th><th>사건</th></tr></thead>'
                      f'<tbody>{rows}</tbody></table></div></details>')
    return "".join(blocks)


FILTERS = ('<input type="radio" name="f" id="f-main" checked><label for="f-main">주요(최고 종가 빼고)</label>'
           '<input type="radio" name="f" id="f-all"><label for="f-all">전체</label>'
           '<input type="radio" name="f" id="f-move"><label for="f-move">하루 ±3%</label>'
           '<input type="radio" name="f" id="f-dd"><label for="f-dd">낙폭·회복</label>'
           '<input type="radio" name="f" id="f-ath"><label for="f-ath">구간 최고</label>')


def fill(tpl, m):
    for k, v in m.items():
        tpl = tpl.replace("{{" + k + "}}", v)
    return tpl


def render(res):
    tpl = (HERE / "template" / "index_template.html").read_text(encoding="utf-8")
    etpl = (HERE / "template" / "events_template.html").read_text(encoding="utf-8")
    common = {"S": kdate(res.get("S") or "—"), "BUILTFOR": kdate(res.get("builtFor") or "—"),
              "CHECK": html.escape((res.get("crossCheck") or {}).get("text", "")),
              "STATUS": res["status"], "STYLE": (HERE / "template" / "index_style.css").read_text(encoding="utf-8")}
    if res["status"] != "ok":
        msg = (f'<section class="held"><h2>판정 보류 · {html.escape(res["reasonText"])}</h2>'
               f'<p class="small">{html.escape(res.get("detail", ""))}</p></section>')
        m = dict(common, HEAD="", BODY=msg)
        return fill(tpl, m), fill(etpl, dict(common, COUNTS=msg.replace("<section", "<div").replace("</section>", "</div>"), EVENTS=""))
    rets = "".join(
        f'<div class="ret"><div class="k">{r["label"]}</div><div class="v num {cls(r["ret"])}">{pct(r["ret"])}</div>'
        f'<div class="sm num">{"연 " + pct(r["annual"]) if "annual" in r else "&nbsp;"}</div>'
        f'<div class="sm num base">기준 {kdate(r["base"])}</div></div>' for r in res["returns"])
    charts, radios = [], []
    for i, k in enumerate(("1년", "5년", "10년")):
        radios.append(f'<input type="radio" name="rng" id="rng{i}"{" checked" if i == 0 else ""}><label for="rng{i}">{k}</label>')
        charts.append(f'<div class="pane pane{i}">{svg_chart(res["chart"][k], k)}</div>')
    table, bars = render_monthly(res["monthly"])
    head = (f'<div class="price"><span class="lvl num">{num(res["close"])}</span>'
            f'<span class="chg num {cls(res["chg"])}">{"▲" if res["chg"] > 0 else "▼" if res["chg"] < 0 else ""} {pct(res["chg"], 2)}</span>'
            f'<span class="small">{kdate(res["S"])} 종가 · 전일 {kdate(res["prevSession"])}</span></div>'
            f'<div class="hilo">'
            f'<div><span class="k">1년 최고(종가)</span> <b class="num">{num(res["hi1y"]["close"])}</b> <span class="small">{kdate(res["hi1y"]["date"])} · 대비 <span class="{cls(res["hi1y"]["from"])}">{pct(res["hi1y"]["from"])}</span></span></div>'
            f'<div><span class="k">1년 최저(종가)</span> <b class="num">{num(res["lo1y"]["close"])}</b> <span class="small">{kdate(res["lo1y"]["date"])} · 대비 <span class="{cls(res["lo1y"]["from"])}">{pct(res["lo1y"]["from"])}</span></span></div>'
            f'<div><span class="k">{kdate(res["since"])} 이후 최고(종가)</span> <b class="num">{num(res["ath"]["close"])}</b> <span class="small">{kdate(res["ath"]["date"])} · 대비 <span class="{cls(res["ath"]["from"])}">{pct(res["ath"]["from"])}</span></span></div>'
            f'</div>')
    body = (f'<section><h2>가격 그림</h2><div class="rng">{"".join(radios)}{"".join(charts)}</div></section>'
            f'<section><h2>기간별 수익률 <span class="small">가격 지수 · 배당 제외 · 3년·5년은 연 환산 함께</span></h2>'
            f'<div class="rets">{rets}</div></section>'
            f'<section><h2>최근 12개월 월별 등락률</h2><div class="bars12">{bars}</div>'
            + (f'<p class="small">흐린 막대는 진행 중인 달({kdate(res["S"])}까지).</p>' if res["monthly"]["last12"][-1]["partial"] else "")
            + '</section>'
            f'<section><h2>월별 등락률 · {res["monthly"]["rows"][0]["year"]}~{res["monthly"]["rows"][-1]["year"]}</h2>{table}'
            f'<p class="small">달마다 마지막 종가 ÷ 전달 마지막 종가 − 1. 빨강 상승·파랑 하락, ±8%에서 가장 진함. 점선 칸·*는 진행 중. '
            f'평균·상승은 끝난 달만 센다.</p></section>')
    m = dict(common, HEAD=head, BODY=body)
    evs = res["events"]
    counts = {t: sum(e["type"] == t for e in evs) for t in ("up", "down", "dd", "recover", "ath")}
    cnt = (f'<p class="small">{kdate(minus_months(d(res["S"]), 12 * YEARS_SHOWN).isoformat())} 이후: 하루 +3% 이상 {counts["up"]}일 · −3% 이하 {counts["down"]}일 · '
           f'고점 대비 −10%/−20% 진입 {counts["dd"]}번 · 전고점 회복 {counts["recover"]}번 · 최고 종가 경신 {counts["ath"]}일</p>')
    return fill(tpl, m), fill(etpl, dict(common, COUNTS=cnt, EVENTS=FILTERS + '<div class="evs">' + render_events(evs) + "</div>"))


# ---------- 실행 ----------

def selfcheck(res, series):
    """내놓기 전 불변식 — 어긋나면 예외(→ 보류)."""
    if res["status"] != "ok":
        return
    ys = dict(series)
    assert abs(ys[res["S"]] - res["close"]) < 0.006
    for r in res["returns"]:
        assert abs(res["close"] / r["baseClose"] - 1 - r["ret"]) < 1e-3, r["label"]
        assert r["base"] < res["S"]
    ytd = next(r for r in res["returns"] if r["label"] == "YTD")
    cur = next(x for x in res["monthly"]["rows"] if x["year"] == int(res["S"][:4]))
    assert abs(cur["annual"]["ret"] - ytd["ret"]) < 1e-12
    prod = 1.0
    for c in cur["months"]:
        if c:
            prod *= 1 + c["ret"]
    assert abs(prod - 1 - ytd["ret"]) < 1e-9          # 월별 곱 = YTD
    assert res["chart"]["1년"][-1][0] == res["S"] and res["chart"]["10년"][-1][0] == res["S"]
    by = {r["label"]: r for r in res["returns"]}
    for key in ("1년", "5년"):
        first, last = res["chart"][key][0], res["chart"][key][-1]
        assert first[0] == by[key]["base"] and abs(last[1] / first[1] - 1 - by[key]["ret"]) < 1e-3, key
    assert all(e["date"] <= res["S"] for e in res["events"])


def read_sessions(path):
    """(P, P 직전 세션). 직전 세션은 홈 시세 파일 종목들의 price.prevSession — P 세션인 종목이 모두 같은 값을 적었을 때만."""
    data = json.loads(path.read_text(encoding="utf-8"))
    P = data["priceSession"]
    prev = {(t.get("price") or {}).get("prevSession") for t in data.get("tickers") or []
            if (t.get("price") or {}).get("session") == P}
    return P, (prev.pop() if len(prev) == 1 else None)


def write_all(files):
    """세 산출물을 임시 파일로 모두 쓴 뒤에야 바꿔 넣는다 — 쓰기 실패면 셋 다 어제 것으로 남는다."""
    tmps = []
    try:
        for path, text in files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_name(path.name + ".tmp")
            tmp.write_text(text, encoding="utf-8")
            tmps.append((tmp, path))
    except Exception:
        for tmp, _ in tmps:
            tmp.unlink(missing_ok=True)
        raise
    for tmp, path in tmps:
        os.replace(tmp, path)


def held_res(reason, detail, P):
    return {"status": "held", "reason": reason, "reasonText": REASON_TEXT[reason], "detail": detail,
            "builtFor": P, "S": None, "index": "SP500", "name": "S&P 500", "source": "Yahoo Finance ^GSPC 일봉 종가"}


def pages_for(res, P):
    """렌더링이 실패해도 보류 페이지를 쓴다 — 틀이 깨졌으면 틀 없는 최소 페이지."""
    try:
        return (res,) + render(res)
    except Exception as e:   # noqa: BLE001
        traceback.print_exc()
        res = dict(held_res("run_fail", f"화면 만들기 실패({type(e).__name__})", P), runAt=res.get("runAt"))
    try:
        return (res,) + render(res)
    except Exception:   # noqa: BLE001
        traceback.print_exc()
        page = ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
                '<title>S&amp;P 500 지수</title></head><body><main data-status="held" style="max-width:900px;margin:0 auto;padding:28px 16px">'
                f'<a href="index.html">← 홈</a><h1>S&amp;P 500</h1><p>판정 보류 · {REASON_TEXT["run_fail"]}. 홈 세션 {html.escape(P or "—")}.</p>'
                '</main></body></html>\n')
        return res, page, page


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-root", default=str(ROOT))
    ap.add_argument("--yahoo", help="Yahoo chart JSON 파일(시험용)")
    ap.add_argument("--fred", help="FRED CSV/JSON 파일(시험용)")
    ap.add_argument("--stocks", default=str(ROOT / "site_data" / "stocks.json"))
    a = ap.parse_args(argv)
    out = Path(a.out_root)
    P, prevP, series = None, None, []
    try:
        try:
            P, prevP = read_sessions(Path(a.stocks))
        except Exception:
            pass
        try:
            ytext = Path(a.yahoo).read_text(encoding="utf-8") if a.yahoo else http_get(YAHOO.format(end=int(time.time()) + 86400))
            series = parse_yahoo(ytext)
        except Exception as e:
            raise Hold("fetch_fail", type(e).__name__)
        try:
            fred = parse_fred(Path(a.fred).read_text(encoding="utf-8") if a.fred else fetch_fred())
            if not fred:
                fred = None
        except Exception:
            fred = None
        res = compute(series, fred, P, prevP)
        selfcheck(res, [p for p in series if p[0] <= P])
    except Hold as h:
        res = {"status": "held", "reason": h.reason, "reasonText": REASON_TEXT[h.reason], "detail": h.detail,
               "builtFor": P, "S": None}
    except Exception as e:   # noqa: BLE001 — 어떤 실패도 보류로 쓰고 종목 게시는 막지 않는다
        traceback.print_exc()
        res = {"status": "held", "reason": "run_fail", "reasonText": REASON_TEXT["run_fail"],
               "detail": type(e).__name__, "builtFor": P, "S": None}
    res["index"], res["name"] = "SP500", "S&P 500"
    res["runAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    res["source"] = "Yahoo Finance ^GSPC 일봉 종가"
    res, page, epage = pages_for(res, P)
    write_all({out / "v2" / "index" / "SP500.json": json.dumps(res, ensure_ascii=False, indent=1) + "\n",
               out / "preview-only-index-sp500.html": page, out / "preview-only-index-sp500-events.html": epage})
    line = (f"INDEX SP500: {res['status']}"
            + (f" S={res['S']} close={res['close']} cross={res['crossCheck']['status']} events={len(res['events'])}"
               if res["status"] == "ok" else f" reason={res['reason']} ({res.get('detail', '')})"))
    print(line)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
