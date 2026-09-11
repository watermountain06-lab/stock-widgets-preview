#!/usr/bin/env python3
"""Offline tests for the daily pipeline: completeness and anomaly rules on
synthetic charts, then the fetch scripts run end to end against a temporary
copy of stocks.json with --fixtures, including forced failures (missing
fixture, halted ticker, low-volume bar, absent macro sources), and the card
updater on copies of real cards. No network.

Usage: python3 pipeline/test_pipeline.py
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, time as dtime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fetch_macro as fm           # noqa: E402
import fetch_prices as fp          # noqa: E402
import validate_site_data as vsd   # noqa: E402
from fetch_prices import ET        # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PASSED = []


def check(name, cond, detail=""):
    if not cond:
        raise AssertionError(f"FAIL: {name} {detail}")
    PASSED.append(name)


def weekdays_back(end, n):
    days, d = [], date.fromisoformat(end)
    while len(days) < n:
        if d.weekday() < 5:
            days.append(d)
        d -= timedelta(days=1)
    return sorted(days)


def chart(days, closes, volumes=None, splits=(), open_time=dtime(9, 30)):
    ts = [int(datetime.combine(d, open_time, ET).timestamp()) for d in days]
    r = {"meta": {}, "timestamp": ts,
         "indicators": {"quote": [{"close": list(closes), "volume": list(volumes or [1_000_000] * len(days))}]}}
    if splits:
        r["events"] = {"splits": {str(ts[i]): {"date": ts[i], "numerator": 2, "denominator": 1} for i in splits}}
    return {"chart": {"result": [r], "error": None}}


AFTER = datetime(2026, 9, 10, 18, 0, tzinfo=ET)
DURING = datetime(2026, 9, 10, 12, 0, tzinfo=ET)
DAYS = weekdays_back("2026-09-10", 22)
CLOSES = [100.0 + i for i in range(22)]


def test_price_rules():
    r = fp.resolve_price(chart(DAYS, CLOSES), AFTER)
    check("completed last bar is used", (r["session"], r["prevSession"], r["status"]) == ("2026-09-10", "2026-09-09", "fresh"), r)
    check("prevClose is the prior bar, not the range start", r["prevClose"] == CLOSES[-2], r)
    r = fp.resolve_price(chart(DAYS, CLOSES), DURING)
    check("in-progress bar is dropped", r["session"] == "2026-09-09", r)
    r = fp.resolve_price(chart(DAYS, CLOSES[:-1] + [None]), AFTER)
    check("trailing null close is skipped", r["session"] == "2026-09-09", r)
    r = fp.resolve_price(chart(DAYS, CLOSES, [1_000_000] * 21 + [50_000]), AFTER)
    check("low-volume bar is suspicious", (r["status"], r.get("statusReason")) == ("suspicious", "volume-anomaly"), r)
    r = fp.resolve_price(chart(DAYS, CLOSES, splits=[10]), AFTER)
    check("split in window is suspicious", r["status"] == "suspicious" and r["statusReason"].startswith("split-in-window"), r)
    r = fp.resolve_price(chart(DAYS + [DAYS[-1]], CLOSES + [999.0]), AFTER)
    check("duplicated date keeps its last bar", (r["close"], r["prevClose"]) == (999.0, CLOSES[-2]), r)
    for name, c in (("single bar", chart(DAYS[:1], CLOSES[:1])),
                    ("chart error", {"chart": {"result": None, "error": {"code": "Not Found"}}})):
        try:
            fp.resolve_price(c, AFTER)
            check(f"{name} raises", False)
        except ValueError:
            check(f"{name} raises", True)


def test_macro_rules():
    hours = [datetime.combine(date.fromisoformat(d), dtime(h, 0), ET)
             for d in ("2026-09-09", "2026-09-10") for h in range(24)]
    closes = [1300 + (x.day - 9) * 10 + x.hour / 100 for x in hours]
    hourly = {"chart": {"result": [{"meta": {}, "timestamp": [int(x.timestamp()) for x in hours],
                                    "indicators": {"quote": [{"close": closes, "volume": [0] * len(hours)}]}}]}}
    check("FX uses the bar ending at the 16:00 ET close", abs(fm.fx_at_us_close(hourly, "2026-09-10") - 1310.15) < 1e-9)
    series = [(f"2025-{m:02d}-01", 300.0) for m in range(1, 13)] + [(f"2026-{m:02d}-01", 309.0) for m in range(1, 8)]
    check("CPI YoY vs the same month a year earlier", fm.cpi_yoy(series) == (3.0, "2026-07-01"), fm.cpi_yoy(series))
    check("target range pairs bounds on their latest common date",
          fm.target_range([("2026-09-09", 3.5), ("2026-09-10", 3.5)],
                          [("2026-09-10", 3.75), ("2026-09-11", 3.75)]) == (3.5, 3.75, "2026-09-10"))
    try:
        fm.target_range([("2026-09-09", 3.5)], [("2026-09-10", 3.75)])
        check("target range with no common date raises", False)
    except ValueError:
        check("target range with no common date raises", True)
    check("next FOMC after 09-11", fm.next_fomc(date(2026, 9, 11)) == {"start": "2026-09-15", "end": "2026-09-16"})
    check("meeting's last day still counts", fm.next_fomc(date(2026, 9, 16)) == {"start": "2026-09-15", "end": "2026-09-16"})
    check("exhausted schedule gives None", fm.next_fomc(date(2027, 12, 9)) is None)


def run(script, *args):
    return subprocess.run([sys.executable, str(ROOT / "pipeline" / script), *args], capture_output=True, text=True)


def test_end_to_end_with_failures():
    tmp = Path(tempfile.mkdtemp())
    original = json.loads((ROOT / "site_data" / "stocks.json").read_text(encoding="utf-8"))
    stocks = tmp / "stocks.json"
    stocks.write_text(json.dumps(original, ensure_ascii=False), encoding="utf-8")
    fx = tmp / "fixtures"
    fx.mkdir()
    (fx / "NVDA.json").write_text(json.dumps(chart(DAYS, CLOSES)))
    (fx / "AAPL.json").write_text(json.dumps(chart(DAYS[:-2], CLOSES[:-2])))  # halted: last bar 09-08
    (fx / "AMZN.json").write_text(json.dumps(chart(DAYS, CLOSES, [1_000_000] * 21 + [10_000])))
    # MSFT has no fixture -> fetch failure

    out = run("fetch_prices.py", "--data", str(stocks), "--fixtures", str(fx), "--now", AFTER.isoformat(),
              "--tickers", "NVDA,AAPL,MSFT,AMZN", "--write")
    check("price run exits 0", out.returncode == 0, out.stdout + out.stderr)
    data = json.loads(stocks.read_text(encoding="utf-8"))
    got = {t["ticker"]: t["price"] for t in data["tickers"]}
    before = {t["ticker"]: t["price"] for t in original["tickers"]}
    check("priceSession is the latest completed session", data["priceSession"] == "2026-09-10", data["priceSession"])
    check("normal ticker is fresh", got["NVDA"]["status"] == "fresh", got["NVDA"])
    check("halted ticker is stale with its bar date", got["AAPL"]["status"] == "stale" and "2026-09-08" in got["AAPL"]["statusReason"], got["AAPL"])
    check("fetch failure keeps the previous close, stale",
          got["MSFT"]["status"] == "stale" and got["MSFT"]["close"] == before["MSFT"]["close"]
          and got["MSFT"]["statusReason"].startswith("fetch-failed"), got["MSFT"])
    check("low-volume bar is suspicious end to end", got["AMZN"]["status"] == "suspicious", got["AMZN"])
    check("ticker outside the run is untouched", got["TSLA"] == before["TSLA"])
    r = vsd.Report()
    for t in data["tickers"]:
        vsd.check_ticker(t, data, r)
    check("every resulting price block passes the validator", not r.errors, r.errors[:3])

    # refreshing only the halted ticker must not roll priceSession back
    out = run("fetch_prices.py", "--data", str(stocks), "--fixtures", str(fx), "--now", AFTER.isoformat(),
              "--tickers", "AAPL", "--write")
    d2 = json.loads(stocks.read_text(encoding="utf-8"))
    p2 = {t["ticker"]: t["price"] for t in d2["tickers"]}
    check("subset refresh keeps the newer priceSession", d2["priceSession"] == "2026-09-10", d2["priceSession"])
    check("subset refresh leaves other fresh tickers fresh", p2["NVDA"]["status"] == "fresh", p2["NVDA"])
    check("halted ticker stays stale against the global session", p2["AAPL"]["status"] == "stale", p2["AAPL"])

    # a failed fetch with no usable previous close stays unavailable (a stale record needs a close)
    for t in d2["tickers"]:
        if t["ticker"] == "GOOGL":
            t["price"] = {"close": None, "status": "unavailable", "statusReason": "test-no-history"}
    stocks.write_text(json.dumps(d2, ensure_ascii=False), encoding="utf-8")
    out = run("fetch_prices.py", "--data", str(stocks), "--fixtures", str(fx), "--now", AFTER.isoformat(),
              "--tickers", "GOOGL,NVDA", "--write")
    d3 = json.loads(stocks.read_text(encoding="utf-8"))
    g = next(t["price"] for t in d3["tickers"] if t["ticker"] == "GOOGL")
    check("failed fetch without a prior close stays unavailable",
          g["status"] == "unavailable" and g["close"] is None and g["statusReason"].startswith("fetch-failed"), g)
    r = vsd.Report()
    for t in d3["tickers"]:
        vsd.check_ticker(t, d3, r)
    check("records still pass the validator after partial runs", not r.errors, r.errors[:3])

    out = run("fetch_prices.py", "--data", str(stocks), "--fixtures", str(fx), "--tickers", "NOPE")
    check("unknown ticker exits non-zero", out.returncode != 0)

    (fx / "^GSPC_1d.json").write_text(json.dumps(chart(DAYS, [6000.0 + i for i in range(22)])))
    macro = tmp / "macro.json"
    out = run("fetch_macro.py", "--stocks", str(stocks), "--out", str(macro), "--fixtures", str(fx),
              "--now", AFTER.isoformat(), "--write")
    check("macro run exits 0 with most sources missing", out.returncode == 0, out.stdout + out.stderr)
    m = json.loads(macro.read_text(encoding="utf-8"))
    ind = m["indicators"]
    check("sp500 fresh on the price session", (ind["sp500"]["status"], ind["sp500"]["asOf"]) == ("fresh", "2026-09-10"), ind["sp500"])
    check("missing sources are unavailable with a reason, not substituted",
          all(ind[k]["status"] == "unavailable" and ind[k]["statusReason"] for k in ("vix", "usdkrw", "fedTarget", "unemployment", "cpiYoy")),
          {k: ind[k]["status"] for k in ind})
    r = vsd.Report()
    vsd.check_macro(macro, data["priceSession"], r)
    check("macro.json passes the validator", not r.errors, r.errors)

    (fx / "^GSPC_1d.json").unlink()  # second run: sp500 source gone -> previous value kept, stale
    out = run("fetch_macro.py", "--stocks", str(stocks), "--out", str(macro), "--fixtures", str(fx),
              "--now", AFTER.isoformat(), "--write")
    m2 = json.loads(macro.read_text(encoding="utf-8"))["indicators"]["sp500"]
    check("failed source keeps its previous value as stale", m2["status"] == "stale" and m2["value"] == ind["sp500"]["value"], m2)


def test_no_change_and_health():
    tmp = Path(tempfile.mkdtemp())
    stocks = tmp / "stocks.json"
    stocks.write_text((ROOT / "site_data" / "stocks.json").read_text(encoding="utf-8"), encoding="utf-8")
    fx = tmp / "fixtures"
    fx.mkdir()
    (fx / "NVDA.json").write_text(json.dumps(chart(DAYS, CLOSES)))
    (fx / "^GSPC_1d.json").write_text(json.dumps(chart(DAYS, [6000.0 + i for i in range(22)])))

    price_args = ["--data", str(stocks), "--fixtures", str(fx), "--now", AFTER.isoformat(), "--tickers", "NVDA", "--write"]
    run("fetch_prices.py", *price_args)
    first = stocks.read_text(encoding="utf-8")
    out = run("fetch_prices.py", *price_args)
    check("repeat price run with nothing new leaves stocks.json untouched",
          stocks.read_text(encoding="utf-8") == first and "No change" in out.stdout, out.stdout + out.stderr)

    macro = tmp / "macro.json"
    macro_args = ["--stocks", str(stocks), "--out", str(macro), "--fixtures", str(fx), "--now", AFTER.isoformat(), "--write"]
    run("fetch_macro.py", *macro_args)
    first = macro.read_text(encoding="utf-8")
    out = run("fetch_macro.py", *macro_args)
    check("repeat macro run with nothing new leaves macro.json untouched",
          macro.read_text(encoding="utf-8") == first and "No change" in out.stdout, out.stdout + out.stderr)

    out = run("health_check.py", "--stocks", str(stocks), "--macro", str(macro))
    check("health check fails when a market series is not fresh", out.returncode == 1, out.stdout)

    healthy = tmp / "healthy_macro.json"
    healthy.write_text(json.dumps({"indicators": {k: {"status": "fresh"} for k in ("sp500", "vix", "usdkrw")},
                                   "nextFomc": {"start": "2026-09-15", "end": "2026-09-16"}}))
    out = run("health_check.py", "--stocks", str(stocks), "--macro", str(healthy))
    check("health check passes on fresh data", out.returncode == 0, out.stdout)

    d = json.loads(stocks.read_text(encoding="utf-8"))
    for t in d["tickers"][:6]:
        t["price"] = dict(t["price"], status="stale", statusReason="test")
    stocks.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    out = run("health_check.py", "--stocks", str(stocks), "--macro", str(healthy))
    check("health check fails at 6 non-fresh tickers", out.returncode == 1, out.stdout)


def test_retries_and_breakers():
    """Network behaviour with urlopen and sleep patched - no real requests, no waiting."""
    import urllib.error

    class Resp:
        def __init__(self, body):
            self.body = body

        def read(self):
            return self.body

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    calls = []

    def scripted(*outcomes):
        seq = list(outcomes)

        def urlopen(req, timeout=None):
            calls.append(req.full_url)
            outcome = seq.pop(0) if len(seq) > 1 else seq[0]  # the last outcome repeats
            if isinstance(outcome, BaseException):
                raise outcome
            return Resp(outcome)
        return urlopen

    real_urlopen, real_sleep, real_argv = fp.urllib.request.urlopen, fp.time.sleep, sys.argv
    fp.time.sleep = lambda seconds: None
    try:
        calls.clear()
        fp.urllib.request.urlopen = scripted(TimeoutError("t"), TimeoutError("t"), b"ok")
        check("timeouts are retried until success", fp.http_get("http://x") == b"ok" and len(calls) == 3, calls)

        calls.clear()
        fp.urllib.request.urlopen = scripted(TimeoutError("t"))
        try:
            fp.http_get("http://x")
            check("gives up after 3 attempts", False)
        except TimeoutError:
            check("gives up after 3 attempts", len(calls) == 3, calls)

        calls.clear()
        fp.urllib.request.urlopen = scripted(urllib.error.HTTPError("http://x", 404, "nf", {}, None))
        try:
            fp.http_get("http://x")
            check("404 is not retried", False)
        except urllib.error.HTTPError:
            check("404 is not retried", len(calls) == 1, calls)

        calls.clear()
        fp.urllib.request.urlopen = scripted(urllib.error.HTTPError("http://x", 503, "busy", {}, None), b"ok")
        check("503 is retried", fp.http_get("http://x") == b"ok" and len(calls) == 2, calls)

        tmp = Path(tempfile.mkdtemp())
        stocks = tmp / "stocks.json"
        stocks.write_text((ROOT / "site_data" / "stocks.json").read_text(encoding="utf-8"), encoding="utf-8")
        before = stocks.read_text(encoding="utf-8")

        # the price provider is down: only 3 tickers are tried, then the rest are skipped
        calls.clear()
        fp.urllib.request.urlopen = scripted(TimeoutError("t"))
        sys.argv = ["fetch_prices.py", "--data", str(stocks), "--now", AFTER.isoformat(), "--write"]
        try:
            fp.main()
        except SystemExit:
            pass
        check("price breaker stops after 3 unreachable tickers", len(calls) == 9, len(calls))
        check("nothing written when no ticker produced a session", stocks.read_text(encoding="utf-8") == before)

        # FRED is down: one series uses its 3 attempts, the others are skipped
        calls.clear()
        fm._fred_down = None
        macro = tmp / "macro.json"
        sys.argv = ["fetch_macro.py", "--stocks", str(stocks), "--out", str(macro), "--now", AFTER.isoformat(), "--write"]
        fm.main()
        fred_calls = [u for u in calls if "stlouisfed" in u]
        check("FRED breaker: one series tried, the rest skipped", len(fred_calls) == 3, len(fred_calls))
        ind = json.loads(macro.read_text(encoding="utf-8"))["indicators"]
        check("skipped FRED series are unavailable with a reason",
              all(ind[k]["status"] == "unavailable" and "skipped" in ind[k]["statusReason"]
                  for k in ("unemployment", "cpiYoy")), {k: ind[k] for k in ("unemployment", "cpiYoy")})
    finally:
        fp.urllib.request.urlopen, fp.time.sleep, sys.argv = real_urlopen, real_sleep, real_argv
        fm._fred_down = None


def test_fred_api_mode():
    """Source selection by FRED_API_KEY, JSON parsing, and no reason churn - no real requests."""
    import os
    real_get, real_key = fm.http_get, os.environ.get("FRED_API_KEY")
    seen = []
    api_body = json.dumps({"observations": [{"date": "2026-09-09", "value": "3.50"},
                                            {"date": "2026-09-10", "value": "."},
                                            {"date": "2026-09-11", "value": "3.75"}]}).encode()
    try:
        fm._fred_down = None
        fm.http_get = lambda url, timeout=30: (seen.append(url), api_body)[1]
        os.environ["FRED_API_KEY"] = "testkey123"
        series = fm.fred("DFEDTARU", None)
        check("official API used when FRED_API_KEY is set",
              "api.stlouisfed.org" in seen[0] and "api_key=testkey123" in seen[0], seen)
        check("API JSON parsed with '.' observations dropped", series == [("2026-09-09", 3.5), ("2026-09-11", 3.75)], series)

        seen.clear()
        del os.environ["FRED_API_KEY"]
        fm.http_get = lambda url, timeout=30: (seen.append(url), b"observation_date,DFEDTARU\n2026-09-10,3.75\n")[1]
        series = fm.fred("DFEDTARU", None)
        check("public CSV used without a key", series == [("2026-09-10", 3.75)] and "fredgraph.csv" in seen[0], seen)
    finally:
        fm.http_get = real_get
        fm._fred_down = None
        if real_key is None:
            os.environ.pop("FRED_API_KEY", None)
        else:
            os.environ["FRED_API_KEY"] = real_key

    prev = {"indicators": {
        "cpiYoy": {"value": 3.3, "asOf": "2026-07", "status": "stale", "statusReason": "fetch-failed: first"},
        "vix": {"status": "unavailable", "statusReason": "fetch-failed: first"},
        "sp500": {"value": 7591.7, "asOf": "2026-09-10", "status": "fresh"}}}
    check("already-stale value keeps its first reason",
          fm.keep_previous(prev, "cpiYoy", "fetch-failed: second")["statusReason"] == "fetch-failed: first")
    check("already-unavailable value keeps its first reason",
          fm.keep_previous(prev, "vix", "fetch-failed: second")["statusReason"] == "fetch-failed: first")
    kept = fm.keep_previous(prev, "sp500", "fetch-failed: now")
    check("fresh value that fails becomes stale with the new reason",
          (kept["status"], kept["statusReason"], kept["value"]) == ("stale", "fetch-failed: now", 7591.7), kept)


def card_chart(bars, splits=()):
    """Yahoo chart JSON for [date, o, h, l, c, v] bars (session-open timestamps)."""
    stamp = lambda d: int(datetime.combine(date.fromisoformat(d), dtime(9, 30), ET).timestamp())
    quote = {k: [b[i + 1] for b in bars] for i, k in enumerate(("open", "high", "low", "close", "volume"))}
    events = {str(stamp(s)): {"date": stamp(s), "numerator": 2, "denominator": 1} for s in splits}
    return {"chart": {"result": [{"timestamp": [stamp(b[0]) for b in bars], "indicators": {"quote": [quote]},
                                  "events": {"splits": events}}], "error": None}}


def test_card_updater():
    """update_cards.py on copies of real cards: append, re-sync, hold, failure, idempotency."""
    import update_cards as uc
    tmp = Path(tempfile.mkdtemp())
    cards, fx, state = tmp / "cards", tmp / "fixtures", tmp / "state"
    for p in (cards, fx, state):
        p.mkdir()
    data = json.loads((ROOT / "site_data" / "stocks.json").read_text(encoding="utf-8"))
    # ANET normal, NVDA mid-session bar, AAPL split, MSFT no fixture, BAC second
    # statement after its MA120 array, KO Yahoo lagging, V stale on the homepage
    data["tickers"] = [t for t in data["tickers"] if t["ticker"] in ("ANET", "NVDA", "AAPL", "MSFT", "BAC", "KO", "V")]
    new_close, card_last = {}, {}
    for t in data["tickers"]:
        tk = t["ticker"]
        html = (ROOT / t["href"]).read_text(encoding="utf-8")
        (cards / t["href"]).write_text(html, encoding="utf-8")
        if (ROOT / "site_data" / "tech_state" / f"{tk}.json").exists():
            shutil.copy(ROOT / "site_data" / "tech_state" / f"{tk}.json", state / f"{tk}.json")
        _, arrays = uc.parse_card_arrays(html)
        bars = [list(uc.bar_values(x)) for x in arrays["DAILY"]["tokens"][-30:]]
        nxt = date.fromisoformat(bars[-1][0]) + timedelta(days=1)
        while nxt.weekday() >= 5:
            nxt += timedelta(days=1)
        c = round(bars[-1][4] * 1.01, 2)
        bars.append([nxt.isoformat(), c, round(c * 1.01, 2), round(c * 0.99, 2), c, 5_000_000])
        if tk == "NVDA":
            bars[-2][5] += 1000  # the card's last bar was captured mid-session
        new_close[tk] = (nxt.isoformat(), c)
        card_last[tk] = (bars[-2][0], bars[-2][4])
        t["price"] = {"close": c, "prevClose": bars[-2][4], "session": nxt.isoformat(),
                      "prevSession": bars[-2][0], "status": "fresh"}
        if tk == "V":  # the homepage kept V's previous close - the card must not run ahead of it
            t["price"] = {"close": bars[-2][4], "prevClose": bars[-3][4], "session": bars[-2][0],
                          "prevSession": bars[-3][0], "status": "stale", "statusReason": "fetch-failed: test"}
        if tk != "MSFT":  # MSFT: no fixture -> fetch failure
            splits = [bars[-5][0]] if tk == "AAPL" else ()
            served = bars[:-1] if tk == "KO" else bars  # KO: Yahoo hasn't published the session yet
            (fx / f"{t.get('yahooSymbol', tk)}.json").write_text(json.dumps(card_chart(served, splits)), encoding="utf-8")
    data["priceSession"] = max(s for s, _ in new_close.values())
    stocks = tmp / "stocks.json"
    stocks.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    status = tmp / "card_status.json"
    now = datetime.combine(date.fromisoformat(data["priceSession"]), dtime(18, 0), ET).isoformat()
    args = ("--data", str(stocks), "--cards-dir", str(cards), "--state-dir", str(state),
            "--status", str(status), "--fixtures", str(fx), "--now", now)
    snapshot = lambda: {p.name: p.read_bytes() for p in cards.iterdir()}
    before = snapshot()

    out = run("update_cards.py", *args)
    check("card dry run exits 0", out.returncode == 0, out.stdout + out.stderr)
    check("card dry run writes nothing", snapshot() == before and not status.exists())

    out = run("update_cards.py", *args, "--write")
    check("card write run exits 0", out.returncode == 0, out.stdout + out.stderr)
    st = json.loads(status.read_text(encoding="utf-8"))["cards"]
    check("normal card is updated", st["ANET"]["status"] == "updated", st["ANET"])
    check("card's mid-session bar is re-synced",
          st["NVDA"]["status"] == "updated" and any(r.startswith("re-synced") for r in st["NVDA"]["reasons"]), st["NVDA"])
    check("split in the window holds the card untouched",
          st["AAPL"]["status"] == "held" and snapshot()["AAPL_full_widget.html"] == before["AAPL_full_widget.html"], st["AAPL"])
    check("fetch failure leaves the card untouched",
          st["MSFT"]["status"] == "failed" and snapshot()["MSFT_full_widget.html"] == before["MSFT_full_widget.html"], st["MSFT"])
    for tk, q in (("ANET", "'"), ("NVDA", '"')):
        html = (cards / f"{tk}_full_widget.html").read_text(encoding="utf-8")
        _, arrays = uc.parse_card_arrays(html)
        d, c = new_close[tk]
        lens = {len(a["tokens"]) for a in arrays.values()}
        check(f"{tk}: DAILY and MA arrays stay equal length, capped", len(lens) == 1 and max(lens) <= uc.MAX_BARS, lens)
        check(f"{tk}: new bar written in the card's own quote style",
              arrays["DAILY"]["tokens"][-1].startswith(f"[{q}{d}{q}"), arrays["DAILY"]["tokens"][-1])
        check(f"{tk}: header shows the new close", f'<div class="price-main">{uc.money(c)}</div>' in html)
        check(f"{tk}: as-of label inserted once", html.count('class="asof-line"') == 1)
        check(f"{tk}: key-levels title carries the analysis date once",
              html.count('class="levels-asof"') == 1 and "분석 기준)</span></div>" in html)
        check(f"{tk}: tech state saved for the new session",
              json.loads((state / f"{tk}.json").read_text(encoding="utf-8"))["asOf"] == d)

    check("Yahoo missing the session holds the card", st["KO"]["status"] == "held"
          and snapshot()["KO_full_widget.html"] == before["KO_full_widget.html"], st["KO"])
    _, v_arrays = uc.parse_card_arrays((cards / "V_full_widget.html").read_text(encoding="utf-8"))
    check("stale homepage price caps the card at its own session",
          uc.bar_values(v_arrays["DAILY"]["tokens"][-1])[0] == card_last["V"][0] and st["V"]["status"] != "failed", st["V"])
    old_bac = [l for l in before["BAC_full_widget.html"].decode("utf-8").split("\n") if l.startswith("const BAC_MA120")][0]
    new_bac = [l for l in (cards / "BAC_full_widget.html").read_text(encoding="utf-8").split("\n")
               if l.startswith("const BAC_MA120")][0]
    check("statement after BAC's MA120 array is kept verbatim",
          st["BAC"]["status"] == "updated" and new_bac.split("];", 1)[1] == old_bac.split("];", 1)[1], st["BAC"])
    for tk in ("ANET", "NVDA", "BAC"):
        html = (cards / f"{tk}_full_widget.html").read_text(encoding="utf-8")
        s, e = uc.tech_segment(html)
        g = re.search(r'<div class="scorecard-grade (grade-[a-z]+)">([^<]+)</div>', html[s:e])
        check(f"{tk}: grade colour and text come from the same grade",
              any(uc.GRADE_CLASS[k] == g.group(1) and uc.GRADE_TEXT[k] == g.group(2) for k in uc.GRADE_CLASS), g.groups())

    after = snapshot()
    out = run("update_cards.py", *args, "--write")
    st = json.loads(status.read_text(encoding="utf-8"))["cards"]
    check("second card run changes nothing", snapshot() == after and st["ANET"]["status"] == "unchanged", st["ANET"])
    status_after = status.read_bytes()
    (state / "ANET.json").unlink()
    run("update_cards.py", *args, "--write")
    check("a lost tech state file comes back while the card stays as is",
          (state / "ANET.json").exists() and snapshot() == after)
    check("a run with no change leaves the status file alone", status.read_bytes() == status_after)

    macro = tmp / "macro.json"
    macro.write_text(json.dumps({"indicators": {k: {"status": "fresh"} for k in ("sp500", "vix", "usdkrw")},
                                 "nextFomc": {"start": "2026-09-15", "end": "2026-09-16"}}), encoding="utf-8")
    hc = run("health_check.py", "--stocks", str(stocks), "--macro", str(macro), "--cards", str(status))
    failed_part = hc.stdout.split("HEALTH CHECK FAILED")[-1]
    check("health check fails on a failed card and a split hold, not on a late-Yahoo hold",
          hc.returncode == 1 and "card MSFT failed" in failed_part and "card AAPL held" in failed_part
          and "card KO" not in failed_part, hc.stdout)
    only_ko = json.loads(status.read_text(encoding="utf-8"))
    only_ko["cards"] = {"KO": only_ko["cards"]["KO"]}
    ko_status = tmp / "card_status_ko.json"
    ko_status.write_text(json.dumps(only_ko), encoding="utf-8")
    hc = run("health_check.py", "--stocks", str(stocks), "--macro", str(macro), "--cards", str(ko_status))
    check("a hold that clears by itself doesn't fail the health check", hc.returncode == 0, hc.stdout)


def test_card_units():
    """Pieces of update_cards.py that fixtures can't easily reach."""
    import update_cards as uc
    card = ("const X_DAILY = [['2026-09-01',10.0,11.0,9.0,10.5,100],['2026-09-02',10.5,11.5,10.0,11.0,100],"
            "['2026-09-03',11.0,12.0,10.5,11.5,100]];\nconst X_MA5 = [null,null,null]; const OTHER = [1];")
    _, arrays = uc.parse_card_arrays(card)
    check("array line keeps a trailing statement as its tail", arrays["MA5"]["tail"] == "; const OTHER = [1];")
    def held_by_sync(card_dates, yahoo_dates):
        toks = ",".join(f"['{d}',10.0,11.0,9.0,10.5,100]" for d in card_dates)
        _, a = uc.parse_card_arrays(f"const X_DAILY = [{toks}];")
        try:  # update_card turns the returned card-only sessions into a hold
            return bool(uc.sync_bars(a, [(d, 10.0, 11.0, 9.0, 10.5, 100) for d in yahoo_dates], [], [])[3])
        except uc.Hold:
            return True
    days = ["2026-09-01", "2026-09-02", "2026-09-03"]
    check("card-only session holds the card", held_by_sync(days, [days[0], days[2]]))
    check("session missing inside the card holds it", held_by_sync([days[0], days[2]], days))
    check("matching sessions don't hold", not held_by_sync(days, days))
    check("every display grade has both a colour and a label", set(uc.GRADE_CLASS) == set(uc.GRADE_TEXT))

    flags = '<div class="scorecard-flags">\n      <span class="risk-flag" data-tooltip="x">⚠️ 단기추세이탈</span>\n    </div>'
    out = uc.render_flags(flags, [], [])
    check("cleared flag shows the no-flags span", "단기추세이탈" not in out and uc.NO_FLAG_SPAN in out)
    check("unchanged flag set leaves the block alone", uc.render_flags(flags, ["단기추세이탈"], []) == flags)
    noflags = '<div class="scorecard-noflags">✅ 감지된 리스크 플래그 없음 — 손으로 쓴 문장</div>'
    check("hand-written no-flags line stays while there are none", uc.render_flags(noflags, [], []) == noflags)
    out = uc.render_flags(noflags, ["고점대비큰조정"], [])
    check("first flag replaces the no-flags line",
          "scorecard-noflags" not in out and '<div class="scorecard-flags">' in out and "⚠️ 고점대비큰조정" in out)
    bare = ('<div class="detail-toggle other">\n<div class="subscores-note">n</div>\n\n    <div class="detail-toggle collapsed">'
            '\n<div class="detail-toggle later">')  # WMT: other toggles before and after in the same block
    out = uc.render_flags(bare, ["장기추세이탈"], [])
    check("first flag on a card without a flag line goes before the scorecard's own toggle",
          out.index('<div class="subscores-note">') < out.index('<div class="scorecard-flags">')
          < out.index('<div class="detail-toggle collapsed">'))
    check("div balance holds when a flag block is added", out.count("<div") - out.count("</div>") == bare.count("<div") - bare.count("</div>"))


def test_valuation_base_units():
    """build_valuation_base.py's pure pieces (no git history needed - Actions checks out depth 1)."""
    import build_valuation_base as vb
    from decimal import Decimal as D
    check("stage: an exact edge stays in the lower stage",
          [vb.stage_of(D(x)) for x in ("0", "20", "20.1", "40", "60", "80", "80.1", "100")] == [1, 1, 2, 2, 3, 4, 5, 5])
    check("width is rounded half-up and clamped",
          (vb.width_of(D("37.3"), D(8), D(48)), vb.width_of(D(50), D(8), D(48)), vb.width_of(D(1), D(8), D(48)))
          == (D("73.3"), D(100), D(0)))
    check("width rounding keeps a near-edge value in its stage", vb.stage_of(vb.width_of(D("2.18"), D("1.8"), D("3.7"))) == 1)
    band = {"intervals": [["95.1", "136.3"], ["136.3", "193.4"], ["193.4", "253.6"]], "segments": ["26", "36", "38"]}
    check("marker: piecewise over the band's intervals", abs(vb.marker_left(band, D("192.93")) - D("61.7")) < D("0.1"))
    check("marker: outside the band gives None", vb.marker_left(band, D(300)) is None)
    gap = {"intervals": [["10", "20"], ["20", "25"], ["25", "40"]], "segments": ["30", "10", "60"]}
    check("marker: a gap interval has its own segment", vb.marker_left(gap, D("22.5")) == D(35))
    body = "anchor: { value: '54.2x', formula: '평균(CSCO 32.86x, CIEN 75.45x) = 54.16x — …', cross: null },\n    verdict: 'X 60.86x는 앵커 대비 +12.4% — …',"
    check("anchor candidates: formula first, then displayed", vb.anchors_of(body) == [("formula", D("54.16")), ("display", D("54.2"))])
    check("verdict premium keeps its sign and shown decimals", vb.verdict_premium(body) == (D("12.4"), 1))
    check("negative premium with a unicode minus", vb.verdict_premium("verdict: 'Y는 앵커 대비 −16% — 저평가'")[0] == D(-16))
    check("the verdict's own comparison value is a candidate too",
          vb.verdict_reference("verdict: 'AMAT PCR 44.69x는 앵커(LRCX 68.45x·KLAC 59.60x 평균 64.0x) 대비 -30.2%'")
          == [("verdict", D("64.0"))])
    ev_cases = {
        "EV/EBITDA = EV($406.2B, 시총 $379.0B+총차입금 $43.54B−현금 $16.37B) ÷ EBITDA($15.89B) = 25.56x": (406.2, 379.0),
        "EV/EBITDA = EV($253,546M = 시총 $258,308M − 현금 $4,762M) ÷ EBITDA($12,538M) = 20.2x": (253.546, 258.308),
        "EV/EBITDA = EV($1,201.8B, ADR가 기준 시총 $1,207.8B+총차입금 $13.4B−현금 $19.4B) ÷ EBITDA(…)": (1201.8, 1207.8),
        "EV/EBITDA = (시가총액 $418.9B - 현금+투자자산 $9.41B, 무차입) ÷ TTM EBITDA($2.66B) = 153.8x": (409.49, 418.9),
    }
    for calc, (ev, mc) in ev_cases.items():
        e0, m0, _ = vb.ev_parts(calc, {})
        check(f"EV parts ({calc[:24]}…)", e0 is not None and abs(e0 - ev) < 0.01 and abs(m0 - mc) < 0.01, (e0, m0))
    e0, m0, how = vb.ev_parts("EV/EBITDA = EV($4.79T) ÷ EBITDA($168.0B) = 28.5x", {}, header_cap=4760.0)
    check("EV-only calcLine uses the header cap in trillions -> billions", (e0, m0) == (4790.0, 4760.0) and "header" in how)
    check("EV-only calcLine without a cap stays unresolved", vb.ev_parts("EV/EBITDA = EV($4.79T) ÷ EBITDA($168.0B)", {})[0] is None)
    rec = {"method": "ev-delta", "value0": "20", "ev0": 100.0, "mcap0": 80.0}
    check("EV/EBITDA moves by the equity share of EV only", vb.value_at(rec, D("1.5")) == D(28))
    rec = {"method": "price-ratio", "value0": "60.86"}
    check("price-ratio multiples scale with price", vb.value_at(rec, D(2)) == D("121.72"))
    row = ('<div class="val-item" data-metric="pbr" onclick="x"><div class="val-header"><span class="val-name">PBR '
           '<span style="color:var(--text3);">(가중치 0.5)</span></span><div style="display:flex;align-items:center;gap:8px;">'
           '<span class="val-number">19.29x</span><span class="stage-badge stage-5">5단계 매우높음</span></div></div>\n'
           '<div class="val-track"><div class="val-fill" style="width:89.1%;background:x;"></div></div>\n'
           '<div class="val-labels"><span class="val-low">저 6.7x</span><span class="val-mid">적정 6.7x</span>'
           '<span class="val-high">고 20.8x</span></div>')
    m = vb.ROW.search(row)
    check("a val-name with a nested span (CAT, PANW) still parses", m is not None and "가중치 0.5" in m.group("name"))
    ebitda = {"EV/EBITDA = EV($406.2B, 시총 $379.0B) ÷ EBITDA($15.89B, 영업이익 $14.85B+D&A $1.03B) = 25.56x": 15.89,
              "EV/EBITDA = EV($374.7B = 시가총액 $375.2B) ÷ EBITDA TTM($9.67B = 영업이익 $9.14B) = 38.76x": 9.67,
              "EV/EBITDA = EV($229.99B) ÷ TTM EBITDA($4.640B = 영업이익 $4.547B) = 49.57x": 4.64,
              "EV/EBITDA = EV($357.3B) ÷ EBITDA 추정치(TTM $12.53B = 세전이익 $10.37B) = 28.52x": 12.53,
              "EV/EBITDA(조정) = EV($244.13B) ÷ TTM 조정 EBITDA($4.12B = …) = 59.33x": 4.12,
              "EV/EBITDA = EV($253,546M = 시총 $258,308M) ÷ EBITDA($12,538M = 영업이익 $12,389M) = 20.2x": 12.538}
    for calc, want in ebitda.items():
        got = vb.ebitda_of(calc)
        check(f"EBITDA divisor, not the metric's own name ({calc[:30]}…)", got is not None and abs(got - want) < 1e-6, got)


if __name__ == "__main__":
    test_valuation_base_units()
    test_price_rules()
    test_macro_rules()
    test_end_to_end_with_failures()
    test_no_change_and_health()
    test_retries_and_breakers()
    test_fred_api_mode()
    test_card_units()
    test_card_updater()
    print(f"OK - {len(PASSED)} checks passed")
