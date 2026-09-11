#!/usr/bin/env python3
"""Offline tests for the daily pipeline: completeness and anomaly rules on
synthetic charts, then the fetch scripts run end to end against a temporary
copy of stocks.json with --fixtures, including forced failures (missing
fixture, halted ticker, low-volume bar, absent macro sources). No network.

Usage: python3 pipeline/test_pipeline.py
"""
import json
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


if __name__ == "__main__":
    test_price_rules()
    test_macro_rules()
    test_end_to_end_with_failures()
    test_no_change_and_health()
    test_retries_and_breakers()
    print(f"OK - {len(PASSED)} checks passed")
