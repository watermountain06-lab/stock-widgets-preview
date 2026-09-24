#!/usr/bin/env python3
"""Offline tests for the daily pipeline: completeness and anomaly rules on
synthetic charts, then the fetch scripts run end to end against a temporary
copy of stocks.json with --fixtures, including forced failures (missing
fixture, halted ticker, low-volume bar, absent macro sources), and the card
updater on copies of real cards. No network.

Usage: python3 pipeline/test_pipeline.py
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, time as dtime, timedelta
from decimal import Decimal
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
    # An INTERIOR null is the dangerous one: the bar vanishes from the series, so prevClose
    # silently comes from the session before it and a two-day move reads as a one-day change.
    r = fp.resolve_price(chart(DAYS, CLOSES[:-2] + [None] + CLOSES[-1:]), AFTER)
    check("an interior null close makes prevSession skip a session",
          (r["session"], r["prevSession"], r["prevClose"]) == ("2026-09-10", "2026-09-08", CLOSES[-3]), r)
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


def run(script, *args, env=None):
    """env overrides the child's environment; a None value removes a variable. Pin the
    variables the script under test actually reads - health_check.py formats its warnings
    differently when GITHUB_ACTIONS is set, so a test that reads them passes locally and
    fails on the runner."""
    child = None
    if env is not None:
        child = dict(os.environ)
        for k, v in env.items():
            if v is None:
                child.pop(k, None)
            else:
                child[k] = v
    return subprocess.run([sys.executable, str(ROOT / "pipeline" / script), *args],
                          capture_output=True, text=True, env=child)


def seed_stocks(path):
    """A copy of the site's stocks.json moved back to the fixtures' session, so these tests don't drift
    as the real site advances: the top-level session and every priced ticker read as that day's close.
    Prices themselves are kept (a fetch failure still falls back to one), and records without a close
    are left alone - "unavailable" must keep a null close to pass the validator."""
    data = json.loads((ROOT / "site_data" / "stocks.json").read_text(encoding="utf-8"))
    session, prev = DAYS[-1].isoformat(), DAYS[-2].isoformat()
    data["priceSession"] = session
    for t in data["tickers"]:
        p = t["price"]
        if isinstance(p.get("close"), (int, float)) and p["close"] > 0:
            t["price"] = {"close": p["close"], "prevClose": p.get("prevClose") or p["close"],
                          "session": session, "prevSession": prev, "status": "fresh"}
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


def test_end_to_end_with_failures():
    tmp = Path(tempfile.mkdtemp())
    stocks = tmp / "stocks.json"
    original = seed_stocks(stocks)
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

    # A provider going BACKWARDS is not the same as a halt, and the difference decides whether a
    # real close survives. On 2026-09-22 Yahoo served a complete session that evening; by the 23rd
    # its close and volume were null for all 70 tickers, so the fetch read the previous day as the
    # latest completed bar and wrote it - AAPL went to $338.98 on the homepage while its own card
    # still held the real $339.75, and the commit step runs before the health check, so the
    # regression was public before anything failed. A withdrawal must keep the recorded close; a
    # genuine halt, where the record already sits at the provider's last bar, must still go stale.
    back = tmp / "back.json"
    seed_stocks(back)                                     # every ticker recorded at 09-10
    run("fetch_prices.py", "--data", str(back), "--fixtures", str(fx), "--now", AFTER.isoformat(),
        "--tickers", "AAPL", "--write")                   # AAPL's fixture stops at 09-08
    w = {t["ticker"]: t["price"] for t in json.loads(back.read_text(encoding="utf-8"))["tickers"]}["AAPL"]
    check("a withdrawn session keeps the recorded close, not the older one",
          w["close"] == before["AAPL"]["close"] and w["session"] == "2026-09-10", w)
    check("and the reason says the provider withdrew it",
          w["status"] == "stale" and "withdrew" in (w.get("statusReason") or ""), w)

    halt = json.loads(back.read_text(encoding="utf-8"))    # record already at the provider's last bar
    for t in halt["tickers"]:
        if t["ticker"] == "AAPL":
            t["price"] = {"close": CLOSES[-3], "prevClose": CLOSES[-4],
                          "session": DAYS[-3].isoformat(), "prevSession": DAYS[-4].isoformat(),
                          "status": "fresh"}
    (tmp / "halt.json").write_text(json.dumps(halt, ensure_ascii=False), encoding="utf-8")
    run("fetch_prices.py", "--data", str(tmp / "halt.json"), "--fixtures", str(fx),
        "--now", AFTER.isoformat(), "--tickers", "AAPL", "--write")
    h = {t["ticker"]: t["price"] for t in json.loads((tmp / "halt.json").read_text(encoding="utf-8"))["tickers"]}["AAPL"]
    check("a halted ticker whose record matches the provider is still written stale",
          h["status"] == "stale" and "target session" in (h.get("statusReason") or ""), h)
    check("halted ticker stays stale against the global session", p2["AAPL"]["status"] == "stale", p2["AAPL"])

    # The provider skipping a session we already hold, rather than retreating from it. Yahoo nulled
    # the 2026-09-22 close for 41 of 70 tickers on the 23rd while serving a complete 09-23 bar, and
    # the date it published was the right one - only prevClose was two sessions old. Left alone that
    # would have shown STX +5.30% against a real +0.44% and reversed the sign on twelve tickers,
    # all labelled fresh with a session lag of zero, so the health check could not have seen it.
    gap = tmp / "gap.json"
    seed_stocks(gap)
    g = json.loads(gap.read_text(encoding="utf-8"))
    for t in g["tickers"]:                                 # hold AAPL at the session about to be nulled
        if t["ticker"] == "AAPL":
            t["price"] = {"close": CLOSES[-2], "prevClose": CLOSES[-3],
                          "session": DAYS[-2].isoformat(), "prevSession": DAYS[-3].isoformat(),
                          "status": "fresh"}
    gap.write_text(json.dumps(g, ensure_ascii=False), encoding="utf-8")
    (fx / "AAPL.json").write_text(json.dumps(chart(DAYS, CLOSES[:-2] + [None] + CLOSES[-1:])))
    run("fetch_prices.py", "--data", str(gap), "--fixtures", str(fx), "--now", AFTER.isoformat(),
        "--tickers", "AAPL", "--write")
    gp = {t["ticker"]: t["price"] for t in json.loads(gap.read_text(encoding="utf-8"))["tickers"]}["AAPL"]
    # Yahoo never restored 2026-09-22, so the site advances rather than waiting for good, and the
    # one figure the hole corrupts is taken from our own record instead of the bar before it.
    check("a session the provider lost does not stop the site advancing",
          gp["session"] == DAYS[-1].isoformat() and gp["close"] == CLOSES[-1]
          and gp["status"] == "fresh", gp)
    check("and prevClose is repaired from our record, not read off the bar before the hole",
          gp["prevSession"] == DAYS[-2].isoformat() and gp["prevClose"] == CLOSES[-2], gp)
    check("the lost session is recorded so the card layer can tell it from a stray bar",
          gp.get("providerGaps") == [DAYS[-2].isoformat()], gp)

    # providerGaps has to outlive the run that wrote it: every branch rebuilds the price block.
    (fx / "AAPL.json").write_text(json.dumps(chart(DAYS, CLOSES)))    # the provider is whole again
    run("fetch_prices.py", "--data", str(gap), "--fixtures", str(fx), "--now", AFTER.isoformat(),
        "--tickers", "AAPL", "--write")
    gk = {t["ticker"]: t["price"] for t in json.loads(gap.read_text(encoding="utf-8"))["tickers"]}["AAPL"]
    check("the record of a lost session survives a later ordinary run",
          gk["status"] == "fresh" and gk.get("providerGaps") == [DAYS[-2].isoformat()], gk)

    # Reading the same incomplete response a second time must not undo the repair. This pipeline
    # runs three times a day, so the second read is the normal case: by then we have advanced past
    # the hole, so the detection above no longer fires, and the provider's own prevClose - which
    # still spans the hole - would be copied straight back in. (Codex found this, and then found
    # that the first version of this very check re-read a COMPLETE fixture left behind by the test
    # above, so it passed with the repair-preservation deleted. The fixture is set here on purpose.)
    (fx / "AAPL.json").write_text(json.dumps(chart(DAYS, CLOSES[:-2] + [None] + CLOSES[-1:])))
    run("fetch_prices.py", "--data", str(gap), "--fixtures", str(fx), "--now", AFTER.isoformat(),
        "--tickers", "AAPL", "--write")
    g2 = {t["ticker"]: t["price"] for t in json.loads(gap.read_text(encoding="utf-8"))["tickers"]}["AAPL"]
    check("a second read of the same incomplete response keeps the repaired previous close",
          g2["prevSession"] == DAYS[-2].isoformat() and g2["prevClose"] == CLOSES[-2]
          and g2["session"] == DAYS[-1].isoformat(), g2)

    # Crossing the hole does not make a lagging ticker fresh. The repaired record is still subject to
    # the target session, or validate_site_data rejects the whole file before anything commits.
    lag = tmp / "lag.json"
    seed_stocks(lag)
    l = json.loads(lag.read_text(encoding="utf-8"))
    l["priceSession"] = "2026-09-11"                       # the fleet is a session ahead of AAPL
    for t in l["tickers"]:
        if t["ticker"] == "AAPL":
            t["price"] = {"close": CLOSES[-2], "prevClose": CLOSES[-3],
                          "session": DAYS[-2].isoformat(), "prevSession": DAYS[-3].isoformat(),
                          "status": "fresh"}
    lag.write_text(json.dumps(l, ensure_ascii=False), encoding="utf-8")
    (fx / "AAPL.json").write_text(json.dumps(chart(DAYS, CLOSES[:-2] + [None] + CLOSES[-1:])))
    run("fetch_prices.py", "--data", str(lag), "--fixtures", str(fx), "--now", AFTER.isoformat(),
        "--tickers", "AAPL", "--write")
    ld = json.loads(lag.read_text(encoding="utf-8"))
    lp = {t["ticker"]: t["price"] for t in ld["tickers"]}["AAPL"]
    check("a ticker that crosses the hole behind the fleet is stale, not fresh",
          lp["status"] == "stale" and "target session" in (lp.get("statusReason") or "")
          and lp.get("providerGaps") == [DAYS[-2].isoformat()], lp)
    rl = vsd.Report()
    for t in ld["tickers"]:
        vsd.check_ticker(t, ld, rl)
    check("and the file still passes the validator", not rl.errors, rl.errors[:3])

    run("fetch_prices.py", "--data", str(lag), "--fixtures", str(fx), "--now", AFTER.isoformat(),
        "--tickers", "AAPL", "--write")
    l2 = {t["ticker"]: t["price"] for t in json.loads(lag.read_text(encoding="utf-8"))["tickers"]}["AAPL"]
    check("a lagging ticker keeps its repaired previous close on a rerun as well",
          l2["prevSession"] == DAYS[-2].isoformat() and l2["prevClose"] == CLOSES[-2], l2)

    # Marking the session lag must not overwrite a flag on the NEW bar either: a volume-anomalous bar
    # that crosses the hole would become "stale", which update_cards accepts and suspicious it does not.
    (fx / "AAPL.json").write_text(json.dumps(
        chart(DAYS, CLOSES[:-2] + [None] + CLOSES[-1:], [1_000_000] * 21 + [10_000])))
    for t in l["tickers"]:
        if t["ticker"] == "AAPL":
            t["price"] = {"close": CLOSES[-2], "prevClose": CLOSES[-3],
                          "session": DAYS[-2].isoformat(), "prevSession": DAYS[-3].isoformat(),
                          "status": "fresh"}
    lag.write_text(json.dumps(l, ensure_ascii=False), encoding="utf-8")
    run("fetch_prices.py", "--data", str(lag), "--fixtures", str(fx), "--now", AFTER.isoformat(),
        "--tickers", "AAPL", "--write")
    l3 = {t["ticker"]: t["price"] for t in json.loads(lag.read_text(encoding="utf-8"))["tickers"]}["AAPL"]
    check("a suspicious new bar crossing the hole keeps its anomaly, not a plain stale label",
          l3["status"] == "suspicious" and l3["statusReason"] == "volume-anomaly", l3)

    # The same hole once the provider has served a session past it. This is the state the real
    # incident was actually in: the first response to the 09-22 loss was to stop advancing, so by
    # the time it was diagnosed 09-23 had arrived and the hole was no longer adjacent to the top.
    # An adjacency test would have missed it, and prevClose must NOT be overwritten here - it now
    # comes from a real bar, and our older record would be the wrong number.
    far = tmp / "far.json"
    seed_stocks(far)
    f = json.loads(far.read_text(encoding="utf-8"))
    for t in f["tickers"]:                                 # held two sessions behind the provider
        if t["ticker"] == "AAPL":
            t["price"] = {"close": CLOSES[-3], "prevClose": CLOSES[-4],
                          "session": DAYS[-3].isoformat(), "prevSession": DAYS[-4].isoformat(),
                          "status": "fresh"}
    far.write_text(json.dumps(f, ensure_ascii=False), encoding="utf-8")
    (fx / "AAPL.json").write_text(json.dumps(chart(DAYS, CLOSES[:-3] + [None] + CLOSES[-2:])))
    run("fetch_prices.py", "--data", str(far), "--fixtures", str(fx), "--now", AFTER.isoformat(),
        "--tickers", "AAPL", "--write")
    fp = {t["ticker"]: t["price"] for t in json.loads(far.read_text(encoding="utf-8"))["tickers"]}["AAPL"]
    check("a lost session is still caught once the provider has moved past it",
          fp["session"] == DAYS[-1].isoformat() and fp.get("providerGaps") == [DAYS[-3].isoformat()], fp)
    check("and prevClose is left on the real bar, not overwritten with the older record",
          fp["prevSession"] == DAYS[-2].isoformat() and fp["prevClose"] == CLOSES[-2], fp)

    # A record that was already suspect must not advance: the gap branch would drop its flag, and
    # update_cards holds a card on suspicious while letting fresh through, so the card would follow
    # a price the card layer had refused. APH carried a split-in-window flag through this exact day.
    for t in g["tickers"]:
        if t["ticker"] == "AAPL":
            t["price"] = {"close": CLOSES[-2], "prevClose": CLOSES[-3],
                          "session": DAYS[-2].isoformat(), "prevSession": DAYS[-3].isoformat(),
                          "status": "suspicious", "statusReason": "split-in-window 2026-09-03"}
    gap.write_text(json.dumps(g, ensure_ascii=False), encoding="utf-8")
    (fx / "AAPL.json").write_text(json.dumps(chart(DAYS, CLOSES[:-2] + [None] + CLOSES[-1:])))
    run("fetch_prices.py", "--data", str(gap), "--fixtures", str(fx), "--now", AFTER.isoformat(),
        "--tickers", "AAPL", "--write")
    gs = {t["ticker"]: t["price"] for t in json.loads(gap.read_text(encoding="utf-8"))["tickers"]}["AAPL"]
    check("a suspect record does not advance across the hole, and keeps its flag",
          gs["status"] == "suspicious" and gs["session"] == DAYS[-2].isoformat()
          and "already suspicious" in (gs.get("statusReason") or ""), gs)
    (fx / "AAPL.json").write_text(json.dumps(chart(DAYS[:-2], CLOSES[:-2])))   # restore the halt fixture

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
    seed_stocks(stocks)
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

    out = run("health_check.py", "--stocks", str(stocks), "--macro", str(macro), "--now", AFTER.isoformat())
    check("health check fails when a market series is not fresh", out.returncode == 1, out.stdout)

    healthy = tmp / "healthy_macro.json"
    healthy.write_text(json.dumps({"indicators": {k: {"status": "fresh"} for k in ("sp500", "vix", "usdkrw")},
                                   "nextFomc": {"start": "2026-09-15", "end": "2026-09-16"}}))
    out = run("health_check.py", "--stocks", str(stocks), "--macro", str(healthy), "--now", AFTER.isoformat())
    check("health check passes on fresh data", out.returncode == 0, out.stdout)

    # 2026-09-14: the provider answered with a clean chart whose newest bar was days old,
    # so everything read "fresh" on a session the market had moved past. stocks is on
    # Thursday 2026-09-10; run the check as if it were later without new data arriving.
    hc_args = ["--stocks", str(stocks), "--macro", str(healthy), "--now"]
    out = run("health_check.py", *hc_args, datetime(2026, 9, 11, 18, 0, tzinfo=ET).isoformat())
    check("one weekday behind warns but passes - a market holiday looks the same",
          out.returncode == 0 and "is 1 weekday(s) behind 2026-09-11" in out.stdout, out.stdout)
    out = run("health_check.py", *hc_args, datetime(2026, 9, 14, 18, 0, tzinfo=ET).isoformat())
    check("two weekdays behind fails, so a stale provider can't pass as a quiet day",
          out.returncode == 1 and "is 2 weekday(s) behind 2026-09-14" in out.stdout, out.stdout)
    out = run("health_check.py", *hc_args, datetime(2026, 9, 11, 12, 0, tzinfo=ET).isoformat())
    check("before the settle cutoff the day's own session isn't expected yet",
          out.returncode == 0 and "weekday(s) behind" not in out.stdout, out.stdout)
    out = run("health_check.py", *hc_args, datetime(2026, 9, 13, 12, 0, tzinfo=ET).isoformat())
    check("a weekend run measures against Friday, not the weekend day",
          out.returncode == 0 and "is 1 weekday(s) behind 2026-09-11" in out.stdout, out.stdout)

    d = json.loads(stocks.read_text(encoding="utf-8"))
    for t in d["tickers"][:6]:
        t["price"] = dict(t["price"], status="stale", statusReason="test")
    stocks.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    out = run("health_check.py", "--stocks", str(stocks), "--macro", str(healthy), "--now", AFTER.isoformat())
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
        seed_stocks(stocks)
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
    # statement after its MA120 array, KO Yahoo lagging, V stale on the homepage,
    # PEP a session the provider lost and fetch_prices recorded, XOM the same hole unrecorded
    data["tickers"] = [t for t in data["tickers"]
                       if t["ticker"] in ("ANET", "NVDA", "AAPL", "MSFT", "BAC", "KO", "V", "CVX",
                                          "PEP", "XOM", "TSM")]
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
        if tk == "CVX":  # the provider sent low above open (really happened 2026-09-11) - hold, don't fail
            bars[-1][3] = round(bars[-1][1] * 1.01, 2)
        if tk == "PEP":  # fetch_prices saw the provider lose this session and wrote it down
            t["price"]["providerGaps"] = [bars[-2][0]]
        if tk == "TSM":  # the homepage repaired its previous close; the card's own bar disagrees
            t["price"]["prevClose"] = bars[-3][4]
        if tk == "V":  # the homepage kept V's previous close - the card must not run ahead of it
            t["price"] = {"close": bars[-2][4], "prevClose": bars[-3][4], "session": bars[-2][0],
                          "prevSession": bars[-3][0], "status": "stale", "statusReason": "fetch-failed: test"}
        if tk != "MSFT":  # MSFT: no fixture -> fetch failure
            splits = [bars[-5][0]] if tk == "AAPL" else ()
            served = bars[:-1] if tk == "KO" else bars  # KO: Yahoo hasn't published the session yet
            if tk in ("PEP", "XOM"):  # the provider dropped the bar the card currently ends on
                served = bars[:-2] + bars[-1:]
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
        # The title says which day the levels are from: the analysis date while the box is left
        # alone, today's close once its rows are recomputed. Read through the box's own container,
        # never a character window - zone-item and ladder-item also appear in other lists below.
        ki = html.find("핵심 가격대")
        opener = re.search(r'<div class="(zone-list|price-ladder)">', html[ki:ki + 2000])
        box = html[ki + opener.start():uc.close_div(html, ki + opener.start())]
        named = [l for l in re.findall(r'(?:zone-label|ladder-label)">([^<]*)</span>', box)]
        refreshed = bool(named) and all(uc.level_kind(l) not in ("ambiguous", "other") for l in named)
        want = "종가 기준)</span></div>" if refreshed else "분석 기준)</span></div>"
        check(f"{tk}: key-levels title says which day its levels are from",
              html.count('class="levels-asof"') == 1 and want in html,
              (refreshed, html[html.find('class="levels-asof"'):][:120]))
        check(f"{tk}: tech state saved for the new session",
              json.loads((state / f"{tk}.json").read_text(encoding="utf-8"))["asOf"] == d)

    check("an inconsistent bar holds the card instead of failing it",
          st["CVX"]["status"] == "held" and any("inconsistent bar" in r for r in st["CVX"]["reasons"])
          and snapshot()["CVX_full_widget.html"] == before["CVX_full_widget.html"], st["CVX"])
    check("Yahoo missing the session holds the card", st["KO"]["status"] == "held"
          and snapshot()["KO_full_widget.html"] == before["KO_full_widget.html"], st["KO"])
    # Yahoo lost 2026-09-22 for 41 tickers and never restored it. A bar the card holds and the fetch
    # no longer returns is normally a card problem, but when fetch_prices recorded the loss the bar
    # is one this pipeline wrote from a complete, OHLC-checked session - keeping it is what lets the
    # card follow the price again instead of freezing on the provider's hole for good.
    # The day's change has to come from the pair the homepage published. These agree on any ordinary
    # day and part company exactly when a session is missing from one side - UNH refused its
    # 2026-09-22 bar as impossible, Yahoo then lost that session for good, and the card would have
    # printed -1.66% beside the homepage's -0.45% for the same ticker on the same day.
    tsm_html = (cards / "TSM_full_widget.html").read_text(encoding="utf-8")
    _, tsm_arrays = uc.parse_card_arrays(tsm_html)
    tsm_bars = [uc.bar_values(x) for x in tsm_arrays["DAILY"]["tokens"]]
    tsm_home = [t["price"] for t in data["tickers"] if t["ticker"] == "TSM"][0]
    want = (tsm_bars[-1][4] / tsm_home["prevClose"] - 1) * 100
    shown = re.search(r'class="price-change"[^>]*>[▲▼] ([+\-][\d.]+)%', tsm_html)
    check("the card's day change follows the homepage's pair, not its own previous bar",
          shown and abs(float(shown.group(1)) - want) < 0.011
          and abs(float(shown.group(1)) - (tsm_bars[-1][4] / tsm_bars[-2][4] - 1) * 100) > 0.011,
          (shown.group(1) if shown else None, round(want, 2)))

    _, pep_arrays = uc.parse_card_arrays((cards / "PEP_full_widget.html").read_text(encoding="utf-8"))
    pep_dates = [uc.bar_values(x)[0] for x in pep_arrays["DAILY"]["tokens"]]
    check("a recorded lost session is kept and the card advances past it",
          st["PEP"]["status"] == "updated" and pep_dates[-1] == new_close["PEP"][0]
          and card_last["PEP"][0] in pep_dates
          and any("provider lost" in r for r in st["PEP"]["reasons"]), (st["PEP"], pep_dates[-3:]))
    check("the same hole with nothing recorded still holds the card",
          st["XOM"]["status"] == "held" and any("Yahoo doesn't" in r for r in st["XOM"]["reasons"])
          and snapshot()["XOM_full_widget.html"] == before["XOM_full_widget.html"], st["XOM"])
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
    hc = run("health_check.py", "--stocks", str(stocks), "--macro", str(macro), "--cards", str(status),
             "--now", now)
    failed_part = hc.stdout.split("HEALTH CHECK FAILED")[-1]
    check("health check fails on a failed card and a split hold, not on a late-Yahoo hold",
          hc.returncode == 1 and "card MSFT failed" in failed_part and "card AAPL held" in failed_part
          and "card KO" not in failed_part, hc.stdout)
    only_ko = json.loads(status.read_text(encoding="utf-8"))
    only_ko["cards"] = {"KO": only_ko["cards"]["KO"]}
    ko_status = tmp / "card_status_ko.json"
    ko_status.write_text(json.dumps(only_ko), encoding="utf-8")
    hc = run("health_check.py", "--stocks", str(stocks), "--macro", str(macro), "--cards", str(ko_status),
             "--now", now)
    check("a hold that clears by itself doesn't fail the health check", hc.returncode == 0, hc.stdout)

    # A newly added ticker's card updates before build_valuation_base.py has run for it.
    # The valuation tab is skipped, which must leave a trace instead of passing silently.
    for name, blob in before.items():
        (cards / name).write_bytes(blob)
    no_base = tmp / "no_valuation_base"
    no_base.mkdir()
    run("update_cards.py", *args, "--valuation-dir", str(no_base), "--write")
    st = json.loads(status.read_text(encoding="utf-8"))["cards"]
    why = "; ".join(st["ANET"]["reasons"])
    check("a missing valuation baseline is recorded on the card, not skipped silently",
          st["ANET"]["status"] == "updated" and "no valuation baseline" in why, st["ANET"])
    check("the note names the command that fixes it", "build_valuation_base.py --tickers ANET" in why, why)
    hc = run("health_check.py", "--stocks", str(stocks), "--macro", str(macro), "--cards", str(status),
             "--now", now, env={"GITHUB_ACTIONS": None})
    failed_part = hc.stdout.split("HEALTH CHECK FAILED")[-1]
    check("a missing baseline warns and never fails the run",
          "WARNING: card ANET" in hc.stdout and "no valuation baseline" in hc.stdout
          and "card ANET" not in failed_part, hc.stdout)
    hc = run("health_check.py", "--stocks", str(stocks), "--macro", str(macro), "--cards", str(status),
             "--now", now, env={"GITHUB_ACTIONS": "true"})
    check("on Actions that warning becomes an annotation instead",
          "::warning::card ANET" in hc.stdout and "WARNING: card ANET" not in hc.stdout, hc.stdout)

    # A 가중평균 disagreement is a standing condition on several cards, so repeating every one of
    # them nightly would be tuned out: only a card that changed class is worth a line.
    wa = json.loads(status.read_text(encoding="utf-8"))
    wa["cards"]["ANET"]["weightedAverage"] = {"class": "legacy", "stated": 4.6, "now": 3.8,
                                              "atBaseline": 4.2, "changed": True}
    wa["cards"]["KO"]["weightedAverage"] = {"class": "legacy", "stated": 2.4, "now": 2.33,
                                            "atBaseline": 2.33, "changed": False}
    wa["cards"]["BAC"]["weightedAverage"] = {"class": "weight-disagreement", "stated": 3.0, "changed": True}
    wa_status = tmp / "card_status_wavg.json"
    wa_status.write_text(json.dumps(wa, ensure_ascii=False), encoding="utf-8")
    hc = run("health_check.py", "--stocks", str(stocks), "--macro", str(macro), "--cards", str(wa_status),
             "--now", now, env={"GITHUB_ACTIONS": None})
    failed_part = hc.stdout.split("HEALTH CHECK FAILED")[-1]
    check("가중평균: only a card that changed class is reported",
          "WARNING: card ANET: 가중평균 legacy" in hc.stdout and "card KO: 가중평균" not in hc.stdout, hc.stdout)
    check("가중평균: a weight disagreement says so instead of quoting an average",
          "card BAC: 가중평균 weight-disagreement" in hc.stdout
          and "badge weights disagree" in hc.stdout, hc.stdout)
    check("가중평균: the standing set is counted, not listed",
          "가중평균 disagreeing with their own badges: 3 (legacy 2, weight-disagreement 1)" in hc.stdout, hc.stdout)
    check("가중평균: a disagreement never fails the run", "가중평균" not in failed_part, hc.stdout)


def test_card_units():
    """Pieces of update_cards.py that fixtures can't easily reach."""
    import update_cards as uc
    card = ("const X_DAILY = [['2026-09-01',10.0,11.0,9.0,10.5,100],['2026-09-02',10.5,11.5,10.0,11.0,100],"
            "['2026-09-03',11.0,12.0,10.5,11.5,100]];\nconst X_MA5 = [null,null,null]; const OTHER = [1];")
    _, arrays = uc.parse_card_arrays(card)
    check("array line keeps a trailing statement as its tail", arrays["MA5"]["tail"] == "; const OTHER = [1];")

    # SNDK 2026-09-15: one raw close, rounded to 4dp for stocks.json and 2dp for the card,
    # is exactly half a cent apart. The float form of that tie is 0.005000000000109139,
    # which failed a "> 0.005" test and left the card unwritten.
    tok = lambda c: f"['2026-09-15',10.0,11.0,9.0,{c},100]"
    check("a half-cent rounding tie still counts as a match", uc.close_matches(1530.895, tok(1530.9)))
    check("the tie matches in the other direction too", uc.close_matches(1530.895, tok(1530.89)))
    check("an exact match still matches", uc.close_matches(192.93, tok(192.93)))
    check("a real mismatch is still caught", not uc.close_matches(1530.895, tok(1531.02)))
    check("exactly at the tolerance is a match", uc.close_matches(100.005, tok(100.0)))
    check("a hair past the tolerance is caught", not uc.close_matches(100.0051, tok(100.0)))
    def held_by_sync(card_dates, yahoo_dates):
        toks = ",".join(f"['{d}',10.0,11.0,9.0,10.5,100]" for d in card_dates)
        _, a = uc.parse_card_arrays(f"const X_DAILY = [{toks}];")
        try:  # update_card turns the returned card-only sessions into a hold
            return bool(uc.sync_bars(a, [(d, 10.0, 11.0, 9.0, 10.5, 100) for d in yahoo_dates], [], [])[4])
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
    # a ticker added after stage 2A isn't in the pre-2A commit at all (skipped on a shallow clone)
    if subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", f"{vb.PRE_2A}^{{commit}}"], capture_output=True).returncode == 0:
        price, cap, src = vb.pre2a_header("NOT_A_CARD_full_widget.html", '<div class="price-main">$12.34</div>')
        check("a card added after stage 2A takes P0 from its own header",
              (price, cap) == (D("12.34"), None) and "added after stage 2A" in src, (price, cap, src))
    ebitda = {"EV/EBITDA = EV($406.2B, 시총 $379.0B) ÷ EBITDA($15.89B, 영업이익 $14.85B+D&A $1.03B) = 25.56x": 15.89,
              "EV/EBITDA = EV($374.7B = 시가총액 $375.2B) ÷ EBITDA TTM($9.67B = 영업이익 $9.14B) = 38.76x": 9.67,
              "EV/EBITDA = EV($229.99B) ÷ TTM EBITDA($4.640B = 영업이익 $4.547B) = 49.57x": 4.64,
              "EV/EBITDA = EV($357.3B) ÷ EBITDA 추정치(TTM $12.53B = 세전이익 $10.37B) = 28.52x": 12.53,
              "EV/EBITDA(조정) = EV($244.13B) ÷ TTM 조정 EBITDA($4.12B = …) = 59.33x": 4.12,
              "EV/EBITDA = EV($253,546M = 시총 $258,308M) ÷ EBITDA($12,538M = 영업이익 $12,389M) = 20.2x": 12.538}
    for calc, want in ebitda.items():
        got = vb.ebitda_of(calc)
        check(f"EBITDA divisor, not the metric's own name ({calc[:30]}…)", got is not None and abs(got - want) < 1e-6, got)


def test_valuation_render():
    """valuation.py on a synthetic card: numbers, badge change, verdict, calcLine, title, label;
    re-running is a no-op and the result depends on P1 only, not on the path taken."""
    import valuation as va
    from decimal import Decimal as D
    html = ('<div class="section-title">밸류에이션 (Valuation Multiples) — 현재가 $100.00 (2026.09.09 종가) · 피어</div>\n'
            '<div class="asof-line" style="x">가격·기술지표: 2026.09.10 종가 기준 갱신 · 분석 문장·밸류에이션: 2026.09.09 기준</div>\n'
            '<div class="val-item" data-metric="per" onclick="x">\n<div class="val-header"><span class="val-name">PER</span>'
            '<div style="display:flex;align-items:center;gap:8px;"><span class="val-number">50.00x</span>'
            '<span class="stage-badge stage-3">3단계 적정(가중치 0.5)</span></div></div>\n'
            '<div class="val-track"><div class="val-fill" style="width:57.1%;background:linear-gradient(90deg,#f0c040,#e67e22);"></div></div>\n'
            '<div class="val-labels"><span class="val-low">저 10x</span><span class="val-mid">적정 40x</span><span class="val-high">고 80x</span></div>\n'
            "<script>\nconst MULTIPLE_DATA = {\n  per: {\n    unit: 'PER', max: 80, tValue: 50.00,\n"
            "    calcLine: 'PER = 주가($100.00) ÷ EPS($2.00) = 50.00x',\n"
            "    verdict: 'T PER 50.00x는 앵커(평균 40.0x) 대비 +25.0% — 설명',\n  }\n};\n</script>")
    base = {"p0": "100.00", "cardAsOf": "2026-09-09", "metrics": [
        {"metric": "per", "frozen": False, "method": "price-ratio", "value0": "50.00", "decimals": 2, "low": "10", "high": "80",
         "stage0": 3, "badge": "3단계 적정(가중치 0.5)", "gradient0": "linear-gradient(90deg,#f0c040,#e67e22)",
         "valueKey": "tValue", "anchor": "40.0", "verdictPremium0": "25.0", "premiumDecimals": 1, "verdictFirstIsValue": True,
         "calc": {"form": "price", "result": {"value": "50.00", "decimals": 2}}}]}
    out = va.render(html, base, D("130"), "2026-09-11", [])
    check("valuation: multiple, width and badge follow the price",
          ">65.00x<" in out and "width:78.6%" in out and "stage-badge stage-4\">4단계 높음(가중치 0.5)<" in out)
    check("valuation: verdict value, premium and anchor date",
          "T PER 65.00x는 앵커(평균 40.0x, 2026.09.09 분석 시점 고정) 대비 +62.5% — 설명" in out)
    # the stamp says the anchor is frozen at the analysis, NOT that the peers were priced
    # then - two cards state peer dates of their own that differ from it (KLAC, IBM)
    stamped = va.render(out, base, D("130"), "2026-09-11", [])
    check("valuation: the anchor stamp is added once and never claims a measurement date",
          stamped.count("2026.09.09 분석 시점 고정") == 1 and "2026.09.09 기준) 대비" not in stamped)
    own = html.replace("앵커(평균 40.0x)", "앵커(평균 40.0x, 2026.09.04 종가 기준)")
    check("valuation: a card that states its own anchor as-of keeps it and gets no second stamp",
          "2026.09.04 종가 기준" in va.render(own, base, D("130"), "2026-09-11", [])
          and "분석 시점 고정" not in va.render(own, base, D("130"), "2026-09-11", []))
    check("valuation: calcLine price and result", "PER = 주가($130.00) ÷ EPS($2.00) = 65.00x" in out and "tValue: 65.00," in out)
    check("valuation: section title and as-of wording",
          "현재가 $130.00 (2026.09.11 종가)" in out and "가격·기술지표·배수: " in out and "분석 문장·재무·앵커: " in out)
    check("valuation: re-running with the same price changes nothing", va.render(out, base, D("130"), "2026-09-11", []) == out)

    # stage 2B-3: the target band. Today every card sits inside its band, so the branches that
    # matter most - outside it, in a grey gap, exactly on a boundary, exactly at the target -
    # are only reachable with synthetic prices.
    band_html = (
        '<div style="position:relative;height:70px;margin:28px 6px 6px;">\n'
        '<div style="position:absolute;top:28px;left:0;right:0;height:10px;border-radius:5px;overflow:hidden;display:flex;">'
        '<div style="width:20.0%;height:100%;background:rgba(46,204,113,0.45);"></div>'
        '<div style="width:10.0%;height:100%;background:var(--bg3);"></div>'
        '<div style="width:30.0%;height:100%;background:rgba(240,192,64,0.5);"></div>'
        '<div style="width:10.0%;height:100%;background:var(--bg3);"></div>'
        '<div style="width:30.0%;height:100%;background:rgba(231,76,60,0.45);"></div></div>\n'
        '<div style="position:absolute;top:10px;left:25.0%;width:2px;height:28px;background:var(--gold);border-radius:1px;"></div>\n'
        '<div style="position:absolute;top:-6px;left:25.0%;transform:translateX(-50%);font-size:11px;font-weight:800;'
        'color:var(--gold);white-space:nowrap;">현재 $25.00</div>\n'
        '<div style="position:absolute;top:22px;left:85.0%;width:2px;height:24px;background:var(--red);border-radius:1px;"></div>\n'
        '<div style="position:absolute;top:48px;left:85.0%;transform:translateX(-50%);font-size:10px;font-weight:700;'
        'color:var(--red);white-space:nowrap;">▲ 목표 $55.00 (+120.0%)</div>\n</div>\n'
        '<div style="display:flex;justify-content:space-between;font-size:10.5px;"><span>Bear $10~20</span></div>\n'
        '<div class="stat-box"><div class="stat-label">평균 목표주가</div>'
        '<div class="stat-value gold" style="font-size:19px;">$55.00</div><div class="stat-sub">+120.0%</div></div>')
    band_base = {"p0": "25.00", "cardAsOf": "2026-09-09", "metrics": [], "ticker": "ASML", "targetBand": {
        "ranges": [["10", "20"], ["30", "40"], ["50", "60"]],
        "intervals": [["10", "20"], ["20", "30"], ["30", "40"], ["40", "50"], ["50", "60"]],
        "segments": ["20.0", "10.0", "30.0", "10.0", "30.0"],
        "marker0": "25.0", "target": "55.00", "upside0": "+120.0", "frozen": False}}

    def band(price):
        return va.target_band(band_html, band_base, D(price), [])

    b = band("35")
    check("band: a price inside a range takes that range's colour and position",
          "top:10px;left:45%;width:2px;height:28px;background:var(--gold)" in b and "현재 $35.00</div>" in b, b[-400:])
    check("band: the target percentage follows the price, the target price does not",
          "▲ 목표 $55.00 (+57.1%)" in b and "<div class=\"stat-sub\">+57.1%</div>" in b)
    check("band: a price in a grey gap gets the neutral colour, not a valuation colour",
          "background:var(--text3)" in band("25") and "left:25%" in band("25"))
    check("band: an interval owns [low, high) so a boundary belongs to the segment above",
          "left:20%;width:2px;height:28px;background:var(--text3)" in band("20"))
    check("band: the last interval closes on its upper bound", "left:100%" in band("60"))
    below, above = band("5"), band("65")
    check("band: below the band hides the tick and says so at the left edge",
          "left:0%" in below and "display:none;" in below and "· 밴드 아래" in below, below[-500:])
    check("band: an edge reads the same whether the price is just inside or just outside",
          "left:100%" in above and "display:none;" in above and "· 밴드 위" in above)
    check("band: at the target neither arrow is true, so the marker is neutral",
          "▶ 목표 $55.00 (+0.0%)" in band("55"))
    check("band: a price above the target flips the arrow down", "▼ 목표 $55.00 (-8.3%)" in band("60"))
    check("band: re-rendering at the same price changes nothing", va.target_band(b, band_base, D("35"), []) == b)
    check("band: the result depends on today's price alone, not on the path",
          va.target_band(b, band_base, D("52"), []) == band("52"))
    check("band: a frozen band is left exactly as it was",
          va.target_band(band_html, dict(band_base, targetBand=dict(band_base["targetBand"], frozen=True)),
                         D("35"), []) == band_html)

    # The 가중평균 detector. The badges feeding that sentence move daily and the sentence does
    # not, so the card can contradict itself; this only reports, and must tell a stale sentence
    # (legacy) apart from one the daily update walked away from (drift).
    import update_cards as uc
    wd = Path(tempfile.mkdtemp())

    def wbase(stage0, weight):
        p = wd / f"W{stage0}{weight}.json"
        p.write_text(json.dumps({"ticker": "W", "metrics": [
            {"metric": "per", "stage0": stage0, "weight": weight}]}), encoding="utf-8")
        return p

    def wcard(stated, stage=3):
        return (html.replace("stage-badge stage-3\">3단계 적정(가중치 0.5)",
                             f"stage-badge stage-{stage}\">{stage}단계 적정(가중치 0.5)")
                + f'<div class="box-key">다섯 지표 가중평균 {stated}/5단계가 나왔다</div>')

    check("가중평균: a card its badges still support says nothing",
          uc.wavg_report(wcard("3.00"), wbase(3, 0.5)) is None)
    r = uc.wavg_report(wcard("2.50"), wbase(3, 0.5))
    check("가중평균: a sentence its badges never supported is legacy",
          r and r["class"] == "legacy" and r["now"] == 3.0 and r["atBaseline"] == 3.0, r)
    r = uc.wavg_report(wcard("3.00", stage=5), wbase(3, 0.5))
    check("가중평균: matched at the baseline and left behind by a badge move is drift",
          r and r["class"] == "drift" and r["now"] == 5.0 and r["atBaseline"] == 3.0, r)
    r = uc.wavg_report(wcard("3.00"), wbase(3, 1.0))
    check("가중평균: a badge weight the baseline disagrees with reports that, and no average",
          r and r["class"] == "weight-disagreement" and "now" not in r, r)
    check("가중평균: a card stating no average is not reported",
          uc.wavg_report(html, wbase(3, 0.5)) is None)
    check("가중평균: a ticker with no baseline yet is not reported",
          uc.wavg_report(wcard("2.50"), wd / "absent.json") is None)
    check("가중평균: the comparison uses the precision the sentence itself claims",
          uc.wavg_report(wcard("3"), wbase(3, 0.5)) is None
          and uc.wavg_report(wcard("3.0"), wbase(3, 0.5)) is None)

    # The scoring config behind the page's comparability flags. build_index used to read it from
    # a sibling repo by absolute home path and fall back to an empty set on OSError; the runner
    # checks out this repo alone, so six tickers were published unflagged from the day the feature
    # shipped and nothing noticed. Every bad state must raise rather than render a guess.
    import build_index as bi
    cfgdir = Path(tempfile.mkdtemp())
    good = {"comparability_flags": {"flags": ["valuation_target_only", "stale_financials"]}}
    (cfgdir / "good.json").write_text(json.dumps(good), encoding="utf-8")
    (cfgdir / "bad.json").write_text("{oops", encoding="utf-8")
    (cfgdir / "nokey.json").write_text(json.dumps({"version": "1"}), encoding="utf-8")
    (cfgdir / "empty.json").write_text(json.dumps({"comparability_flags": {"flags": []}}), encoding="utf-8")

    def cfg_raises(name):
        try:
            bi.comparability_flags(cfgdir / name)
            return False
        except bi.ConfigError:
            return True

    check("score config: a good one loads", bi.comparability_flags(cfgdir / "good.json")
          == {"valuation_target_only", "stale_financials"})
    check("score config: a missing file raises instead of publishing a guess", cfg_raises("nope.json"))
    check("score config: malformed JSON raises", cfg_raises("bad.json"))
    check("score config: a missing comparability_flags.flags raises", cfg_raises("nokey.json"))
    check("score config: an empty flag list raises - it reads the same as no card being flagged",
          cfg_raises("empty.json"))
    check("score config: this repo's own copy still declares the two comparability flags",
          bi.comparability_flags() == {"valuation_target_only", "stale_financials"},
          sorted(bi.comparability_flags()))

    scored = {"ticker": "AA", "cardRank": 1, "name": "A", "sector": "s", "href": "AA_full_widget.html",
              "price": {"close": 10.0, "prevClose": 10.0, "status": "fresh"},
              "shares": {"usEquivalent": 100}, "cardAsOf": "2026-09-01",
              "tier": {"value": "적정", "status": "ok"},
              "score": {"status": "available", "total": 50.0, "valuationAsOf": "2026-08-18",
                        "qualityFlags": ["valuation_target_only", "negative_equity"]}}
    check("score config: only comparability flags reach the page, not every quality flag",
          bi.ui_row(scored, {"valuation_target_only"})["scoreFlags"] == ["valuation_target_only"])
    check("score config: a card carrying no comparability flag shows an empty list",
          bi.ui_row(scored, {"stale_financials"})["scoreFlags"] == [])
    check("valuation: result depends on today's price only, not on the path",
          va.render(out, base, D("90"), "2026-09-12", []) == va.render(html, base, D("90"), "2026-09-12", []))
    # a card whose own label/colour for a stage isn't the standard one must get them back, whatever the path
    odd = html.replace("3단계 적정(가중치 0.5)", "3단계 보통(가중치 0.5)").replace("#f0c040,#e67e22", "#c8a84b,#f0c040")
    odd_base = {"p0": "100.00", "cardAsOf": "2026-09-09", "gradients": {"3": "linear-gradient(90deg,#c8a84b,#f0c040)"},
                "metrics": [dict(base["metrics"][0], stage0=3, badge="3단계 보통(가중치 0.5)",
                                 gradient0="linear-gradient(90deg,#c8a84b,#f0c040)")]}
    via = va.render(va.render(odd, odd_base, D("130"), "2026-09-11", []), odd_base, D("100"), "2026-09-11", [])
    check("valuation: back at the original stage, the card's own label and colour return",
          via == va.render(odd, odd_base, D("100"), "2026-09-11", []) and "3단계 보통(가중치 0.5)" in via and "#c8a84b,#f0c040" in via)
    head = '<div class="verdict-summary-head">종합 판단 <span class="tag mixed">적정</span></div>'
    once = va.summary_asof(head, "2026.09.09")
    check("valuation: 종합 판단 heading gets the analysis date once",
          '종합 판단 <span class="summary-asof"' in once and "(2026.09.09 분석 기준)</span> <span class=\"tag mixed\">" in once
          and va.summary_asof(once, "2026.09.09") == once)
    check("valuation: a card without the heading is left alone", va.summary_asof("<div>x</div>", "2026.09.09") == "<div>x</div>")
    check("valuation: a multi-word stage wording isn't mistaken for a suffix",
          [va.badge_suffix(b) for b in ("4단계 다소 높음", "4단계 높음(가중치 0.5)", "1단계 매우낮음 · 평가보류", "5단계 매우높음")]
          == ["", "(가중치 0.5)", " · 평가보류", ""])
    base["metrics"][0].update(stage0=3, badge="3단계 적정(가중치 0.5)", gradient0="linear-gradient(90deg,#f0c040,#e67e22)")
    frozen = {"p0": "100.00", "cardAsOf": "2026-09-09", "metrics": [dict(base["metrics"][0], frozen=True)]}
    kept = va.render(html, frozen, D("130"), "2026-09-11", [])
    check("valuation: a frozen metric is left exactly as it was", ">50.00x<" in kept and "대비 +25.0% — 설명" in kept)


def test_prose_stamp():
    """Stage 3's tri-state on a synthetic card, then the manifest this repo actually ships."""
    import prose_stamp as ps

    tmp = Path(tempfile.mkdtemp())
    pre = "평균 목표가 $100.00는 현재가 대비 +10.0%다."
    post = "평균 목표가 $100.00는 2026.09.09 종가 기준 현재가 대비 +10.0%다."
    seq = [0]

    def manifest(entries):
        seq[0] += 1
        p = tmp / f"m{seq[0]}.json"
        p.write_text(json.dumps({"version": "t", "entries": entries}, ensure_ascii=False), encoding="utf-8")
        ps._cache.clear()
        return p

    def entry(**over):
        e = {"ticker": "AA", "disposition": "stamp", "form": "bare", "asOf": "2026-09-09",
             "token": "+10.0%", "preimage": pre, "preSha": ps.sha(pre),
             "postimage": post, "postSha": ps.sha(post)}
        e.update(over)
        return e

    def fails(html, mp):
        try:
            ps.render(html, "AA", [], path=mp, tickers={"AA"})
            return False
        except ps.RenderError:
            return True

    m = manifest([entry()])
    out, c = ps.render(f"<div>{pre}</div>", "AA", [], path=m, tickers={"AA"})
    check("prose: the audited sentence is dated exactly once",
          out == f"<div>{post}</div>" and c["applied"] == 1, c)
    again, c2 = ps.render(out, "AA", [], path=m, tickers={"AA"})
    check("prose: a rerun writes nothing and is verified against the recorded postimage",
          again == out and c2 == {"applied": 0, "already": 1, "gated": False}, c2)
    _, cg = ps.render(f"<div>{pre}</div>", "AA", [], path=m, tickers={"BB"})
    check("prose: a card outside the gate is untouched", cg["gated"] is True)
    check("prose: a sentence that is neither preimage nor postimage fails the card",
          fails("<div>평균 목표가 $100.00는 현재가 대비 +9.9%다.</div>", m))
    check("prose: a preimage appearing twice fails rather than picking one",
          fails(f"<div>{pre}</div><div>{pre}</div>", m))
    check("prose: a manifest whose hash does not match its text is refused",
          fails(f"<div>{pre}</div>", manifest([entry(preSha="0" * 16)])))
    check("prose: an anchor that would change nothing is refused",
          fails(f"<div>{pre}</div>", manifest([entry(postimage=pre, postSha=ps.sha(pre))])))
    half = f"<div>{pre}</div><div>{post}</div>"
    check("prose: a card holding both states at once fails", fails(half, m))

    # A stamp that only PREFIXES its sentence leaves the preimage inside the postimage.
    # DE, TXN and VZ are shaped that way ("컨센서스 여력 +1.0%:"), and a bare zero-count
    # failed all three on the first fleet run - and would have failed every rerun after,
    # because the already-applied branch could never match either.
    lab = "컨센서스 여력 +1.0%:"
    lab_post = "2026.09.14 종가 기준 " + lab
    lm = manifest([entry(preimage=lab, preSha=ps.sha(lab),
                         postimage=lab_post, postSha=ps.sha(lab_post))])
    out2, c3 = ps.render(f"<div>{lab}</div>", "AA", [], path=lm, tickers={"AA"})
    check("prose: a prefix-only stamp applies though the postimage contains the preimage",
          out2 == f"<div>{lab_post}</div>" and c3["applied"] == 1, c3)
    out3, c4 = ps.render(out2, "AA", [], path=lm, tickers={"AA"})
    check("prose: and its rerun reads as already applied, not as a failure",
          out3 == out2 and c4 == {"applied": 0, "already": 1, "gated": False}, c4)
    check("prose: a prefix-form preimage left twice in the card still fails",
          fails(f"<div>{lab}</div><div>{lab}</div>", lm))

    ps._cache.clear()
    real = ps.load()
    total = sum(len(v) for v in real.values())
    check("prose: the shipped manifest is the audited set - 72 anchors across 47 cards",
          total == 72 and len(real) == 47, (total, len(real)))
    # Counting states, not occurrences: a correctly stamped prefix-form anchor leaves its
    # preimage inside the postimage, so "pre + post == 1" calls a healthy card broken.
    unresolved = []
    for t, entries in real.items():
        card = (ROOT / f"{t}_full_widget.html").read_text(encoding="utf-8")
        for e in entries:
            pre_i, post_i = e["preimage"], e["postimage"]
            npre, npost = card.count(pre_i), card.count(post_i)
            stamped = npost == 1 and npre == post_i.count(pre_i)
            awaiting = npost == 0 and npre == 1
            if not (stamped or awaiting):
                unresolved.append((t, pre_i[:40], npre, npost))
    check("prose: every anchor resolves to exactly one state on its live card",
          not unresolved, unresolved[:3])
    check("prose: the manifest carries all five anchor shapes",
          {e["form"] for es in real.values() for e in es}
          == {"bare", "paren", "price-label", "bb-item", "green-span"})
    check("prose: no anchor is recorded against a card that lost its 종가 기준 wording",
          all("종가 기준" in e["postimage"] or "종가 $" in e["postimage"]
              for es in real.values() for e in es))


def test_backfill():
    """A recorded bar fills a hole the provider cannot, and every moving average from the
    insertion point on is recomputed rather than shifted onto the wrong bar."""
    import update_cards as uc
    import backfill as bf
    tmp = Path(tempfile.mkdtemp())

    def manifest(bars, name="m.json"):
        pth = tmp / name
        pth.write_text(json.dumps({"bars": bars}, ensure_ascii=False), encoding="utf-8")
        bf._cache.clear()
        return pth

    good = {"ticker": "X", "session": "2026-09-22", "open": 10.0, "high": 11.0,
            "low": 9.0, "close": 10.5, "volume": 100, "source": "recorded by hand for this test"}
    check("a recorded bar loads", bf.load(manifest([good]))["X"]["2026-09-22"][4] == 10.5)
    check("no manifest at all is not an error", bf.load(tmp / "absent.json") == {})
    # The manifest is the only place a bar can come from that the provider did not serve, so it is
    # checked harder than a fetched bar, not less: the same OHLC rule, plus a weekday, plus stated
    # provenance. A bar that cannot pass here must not reach a card.
    for bad, why, word in (
        ({**good, "session": "2026-09-20"}, "a weekend date", "weekend"),
        ({**good, "source": "   "}, "no stated source", "source"),
        ({**good, "high": 9.5}, "a high under its own close", "consistent"),
        ({**good, "low": 10.4}, "a low over its own open", "consistent"),
        ({**good, "volume": -1}, "negative volume", "consistent"),
        ({**good, "close": 0}, "a zero close", "consistent"),
        ({**good, "close": "x"}, "a close that is not a number", "not a number"),
    ):
        try:
            bf.load(manifest([bad]))
            check(f"a bar with {why} is refused", False, bad)
        except bf.BackfillError as e:
            check(f"a bar with {why} is refused", word in str(e), str(e))
    try:
        bf.load(manifest([good, dict(good)]))
        check("the same session recorded twice is refused", False)
    except bf.BackfillError as e:
        check("the same session recorded twice is refused", "twice" in str(e), str(e))

    m = manifest([good])
    fetched = [("2026-09-21", 1.0, 1.0, 1.0, 1.0, 1), ("2026-09-23", 2.0, 2.0, 2.0, 2.0, 2)]
    out, added = bf.merge(fetched, "X", [], m)
    check("a recorded bar the provider skipped is folded in, in date order",
          [b[0] for b in out] == ["2026-09-21", "2026-09-22", "2026-09-23"]
          and added == ["2026-09-22"], out)
    check("and is not folded in twice", bf.merge(out, "X", [], m)[1] == [])
    check("a recorded bar outside the fetched window is left alone",
          bf.merge([("2026-09-23", 2.0, 2.0, 2.0, 2.0, 2)], "X", [], m)[1] == [])
    check("a ticker with nothing recorded is untouched", bf.merge(fetched, "Y", [], m) == (fetched, []))

    # The array mechanics. A bar dropped into the middle shifts every index after it, which is the
    # one place a silent off-by-one would put every moving average on the wrong bar.
    days = ["2026-09-10", "2026-09-11", "2026-09-14", "2026-09-15", "2026-09-16",
            "2026-09-17", "2026-09-18", "2026-09-21", "2026-09-23"]
    cl = {d: 100.0 + i for i, d in enumerate(days)}
    daily = ",".join(f"['{d}',{cl[d]},{cl[d] + 1},{cl[d] - 1},{cl[d]},1000]" for d in days)
    card = f"const X_DAILY = [{daily}];\nconst X_MA5 = [{','.join(['null'] * len(days))}];"
    _, a = uc.parse_card_arrays(card)
    uc.extend_mas(a, 0)                                   # a consistent starting point
    served = [(d, cl[d], cl[d] + 1, cl[d] - 1, cl[d], 1000) for d in days]
    served.append(("2026-09-22", 108.5, 109.5, 107.5, 108.5, 1000))
    served.sort(key=lambda b: b[0])
    changed, replaced, appended, inserted, extra = uc.sync_bars(a, served, [], [], {"2026-09-22"})
    check("the missing session is inserted, not appended to the end",
          (inserted, appended, replaced, changed) == (1, 0, 0, 8), (inserted, appended, replaced, changed))
    uc.extend_mas(a, changed)
    got = [uc.bar_values(t)[0] for t in a["DAILY"]["tokens"]]
    check("the series comes back in order with the hole filled",
          got == sorted(got) and "2026-09-22" in got and len(got) == len(days) + 1, got[-4:])
    check("DAILY and MA5 stay the same length", len(a["MA5"]["tokens"]) == len(got))
    closes = [Decimal(str(uc.bar_values(t)[4])) for t in a["DAILY"]["tokens"]]
    i = got.index("2026-09-22")
    for at, label in ((i, "at the inserted bar"), (len(got) - 1, "at the end")):
        want = sum(closes[at - 4:at + 1]) / 5
        check(f"MA5 {label} matches a direct average of the filled series",
              abs(Decimal(a["MA5"]["tokens"][at]) - want) < Decimal("0.00005"),
              (a["MA5"]["tokens"][at], str(want)))
    check("the bar before the hole is untouched by the insertion",
          uc.bar_values(a["DAILY"]["tokens"][i - 1])[0] == "2026-09-21")

    # Running again changes nothing: the card now has the bar, so it goes through the ordinary
    # replace path and the values match.
    again = uc.sync_bars(a, served, [], [], {"2026-09-22"})
    check("a second run neither inserts nor replaces anything",
          (again[1], again[2], again[3]) == (0, 0, 0), again[:4])

    # And the floor: a hole nobody has recorded a bar for still holds the card.
    _, a2 = uc.parse_card_arrays(card)
    uc.extend_mas(a2, 0)
    try:
        uc.sync_bars(a2, served, [], [], set())
        check("a hole nobody recorded still holds the card", False)
    except uc.Hold as e:
        check("a hole nobody recorded still holds the card", "missing inside" in str(e), str(e))


if __name__ == "__main__":
    test_prose_stamp()
    test_valuation_render()
    test_valuation_base_units()
    test_price_rules()
    test_macro_rules()
    test_end_to_end_with_failures()
    test_no_change_and_health()
    test_retries_and_breakers()
    test_fred_api_mode()
    test_card_units()
    test_card_updater()
    test_backfill()
    print(f"OK - {len(PASSED)} checks passed")
