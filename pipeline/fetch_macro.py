#!/usr/bin/env python3
"""Refresh site_data/macro.json - the six indicators above the stock list.

Every value carries its own asOf and status, and the market series are tied
to the same US session as the stock prices (stocks.json priceSession):
  - sp500 (^GSPC), vix (^VIX): the completed daily bar dated priceSession,
    using fetch_prices.py's completeness rule;
  - usdkrw (KRW=X): FX trades around the clock and its daily bar is still
    open at the US close, so the value is the hourly bar ending 16:00 ET on
    priceSession - the rate at the US close, not a mixed-session daily bar
    (the old fetch_macro.py took the latest non-null bar, which could be an
    in-progress one);
  - fedTarget: FRED DFEDTARL/DFEDTARU, the announced target range (the
    homepage used to show FEDFUNDS, a monthly average effective rate);
  - unemployment (UNRATE) and cpiYoy (CPIAUCSL, YoY computed here): monthly,
    asOf is the observation month;
  - nextFomc: from the Fed's published schedule below; fomcScheduleThrough
    says how far it reaches, and an exhausted schedule is reported.
A failed source keeps its previous value marked stale (unavailable if there
was none) - never a substituted value from another date.

Network: requests are retried like fetch_prices.py. FRED gets 60s per
attempt (it timed out at 30s from GitHub's runners on the first workflow
run, 2026-09-11), and once one FRED series fails on the network the other
FRED series are skipped instead of each waiting out its own retries.

Usage: python3 pipeline/fetch_macro.py [--write] [--stocks PATH] [--out PATH]
                                       [--fixtures DIR] [--now ISO]
  --fixtures DIR   read {SYMBOL}_{interval}.json and {SERIES}.csv from DIR (tests)
"""
import argparse
import csv
import io
import json
import sys
import time
import urllib.parse
from datetime import date, datetime, time as dtime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_prices import ET, completed_bars, http_get, is_network_error  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=1mo&interval={interval}"
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
FRED_TIMEOUT = 60

# federalreserve.gov/monetarypolicy/fomccalendars.htm, checked 2026-09-11
FOMC = [
    ("2026-01-27", "2026-01-28"), ("2026-03-17", "2026-03-18"), ("2026-04-28", "2026-04-29"),
    ("2026-06-16", "2026-06-17"), ("2026-07-28", "2026-07-29"), ("2026-09-15", "2026-09-16"),
    ("2026-10-27", "2026-10-28"), ("2026-12-08", "2026-12-09"),
    ("2027-01-26", "2027-01-27"), ("2027-03-16", "2027-03-17"), ("2027-04-27", "2027-04-28"),
    ("2027-06-08", "2027-06-09"), ("2027-07-27", "2027-07-28"), ("2027-09-14", "2027-09-15"),
    ("2027-10-26", "2027-10-27"), ("2027-12-07", "2027-12-08"),
]
FOMC_THROUGH = "2027-12"

# set to the network error once FRED fails, so the remaining series skip it
_fred_down = None


def _get(url, fixture, fixtures, timeout=30):
    if fixtures:
        path = Path(fixtures) / fixture
        if not path.exists():
            raise FileNotFoundError(f"no fixture {fixture}")
        return path.read_text(encoding="utf-8")
    text = http_get(url, timeout).decode("utf-8")
    time.sleep(0.2)
    return text


def yahoo(symbol, interval, fixtures):
    url = YAHOO.format(symbol=urllib.parse.quote(symbol, safe=""), interval=interval)
    return json.loads(_get(url, f"{symbol}_{interval}.json", fixtures))


def fred(sid, fixtures):
    """[(date, value)] oldest first; FRED marks missing observations with '.'."""
    global _fred_down
    if _fred_down is not None:
        raise RuntimeError(f"skipped: FRED unreachable earlier in this run ({_fred_down})")
    try:
        text = _get(FRED.format(sid=sid), f"{sid}.csv", fixtures, timeout=FRED_TIMEOUT)
    except Exception as e:
        if is_network_error(e):
            _fred_down = e
        raise
    rows = list(csv.reader(io.StringIO(text)))
    series = [(r[0], float(r[1])) for r in rows[1:] if len(r) == 2 and r[1] not in ("", ".")]
    if not series:
        raise ValueError(f"FRED {sid}: no observations")
    return series


def daily_on_session(chart, session, now_et):
    """(close, change % vs the prior completed bar, prior bar's date) for the bar dated session."""
    bars, _ = completed_bars(chart, now_et)
    idx = next((i for i, b in enumerate(bars) if b[0] == session), None)
    if idx is None:
        raise ValueError(f"no completed bar dated {session}")
    if idx == 0:
        raise ValueError(f"no bar before {session} for the change")
    close, prev = bars[idx][1], bars[idx - 1][1]
    return round(close, 2), round((close / prev - 1) * 100, 2), bars[idx - 1][0]


def fx_at_us_close(chart, session):
    """Close of the hourly bar that starts 15:00 ET (so ends at the 16:00 ET close) on session."""
    r = chart["chart"]["result"][0]
    start = datetime.combine(date.fromisoformat(session), dtime(15, 0), ET)
    for ts, close in zip(r["timestamp"], r["indicators"]["quote"][0]["close"]):
        if close is not None and datetime.fromtimestamp(ts, ET) == start:
            return close
    raise ValueError(f"no hourly bar starting 15:00 ET on {session}")


def cpi_yoy(series):
    """(YoY % rounded to 0.1, latest observation date) against the same month a year earlier."""
    latest_date, latest = series[-1]
    y, m = int(latest_date[:4]), latest_date[5:7]
    year_ago = next((v for d, v in series if d.startswith(f"{y - 1}-{m}")), None)
    if year_ago is None:
        raise ValueError(f"no CPI observation for {y - 1}-{m}")
    return round((latest / year_ago - 1) * 100, 1), latest_date


def target_range(lower, upper):
    """(lower, upper, date) on the latest date BOTH bounds have an observation.
    FRED can post one bound's newest day before the other's (2026-09-11:
    DFEDTARU had 09-11, DFEDTARL only 09-10), so pairing each series' own
    latest value would mix dates."""
    lo, hi = dict(lower), dict(upper)
    common = sorted(set(lo) & set(hi))
    if not common:
        raise ValueError("target range bounds share no observation date")
    day = common[-1]
    return lo[day], hi[day], day


def next_fomc(today):
    for start, end in FOMC:
        if date.fromisoformat(end) >= today:
            return {"start": start, "end": end}
    return None


def keep_previous(prev, key, reason):
    old = ((prev or {}).get("indicators") or {}).get(key)
    if old and (old.get("value") is not None or old.get("upper") is not None):
        return dict(old, status="stale", statusReason=reason)
    return {"status": "unavailable", "statusReason": reason}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stocks", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--out", default=str(ROOT / "site_data" / "macro.json"))
    ap.add_argument("--fixtures", default=None)
    ap.add_argument("--now", default=None)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    now_et = datetime.fromisoformat(args.now).astimezone(ET) if args.now else datetime.now(ET)
    session = json.loads(Path(args.stocks).read_text(encoding="utf-8")).get("priceSession")
    if not session:
        sys.exit("stocks.json has no priceSession - run fetch_prices.py first")
    out = Path(args.out)
    prev = json.loads(out.read_text(encoding="utf-8")) if out.exists() else None
    fx = args.fixtures
    ind, prev_session = {}, None

    for key, symbol in (("sp500", "^GSPC"), ("vix", "^VIX")):
        try:
            value, change, before = daily_on_session(yahoo(symbol, "1d", fx), session, now_et)
            ind[key] = {"value": value, "changePct": change, "asOf": session, "status": "fresh",
                        "source": f"Yahoo {symbol} daily close"}
            prev_session = prev_session or before
        except Exception as e:
            ind[key] = keep_previous(prev, key, f"fetch-failed: {str(e)[:160]}")

    try:
        if not prev_session:
            raise ValueError("previous session unknown (index fetches failed)")
        hourly = yahoo("KRW=X", "60m", fx)
        rate, before = fx_at_us_close(hourly, session), fx_at_us_close(hourly, prev_session)
        ind["usdkrw"] = {"value": round(rate, 2), "changePct": round((rate / before - 1) * 100, 2),
                         "asOf": session, "status": "fresh", "source": "Yahoo KRW=X hourly bar ending 16:00 ET"}
    except Exception as e:
        ind["usdkrw"] = keep_previous(prev, "usdkrw", f"fetch-failed: {str(e)[:160]}")

    try:
        lower, upper, day = target_range(fred("DFEDTARL", fx), fred("DFEDTARU", fx))
        ind["fedTarget"] = {"lower": lower, "upper": upper, "asOf": day,
                            "status": "fresh", "source": "FRED DFEDTARL/DFEDTARU"}
    except Exception as e:
        ind["fedTarget"] = keep_previous(prev, "fedTarget", f"fetch-failed: {str(e)[:160]}")

    try:
        u = fred("UNRATE", fx)
        ind["unemployment"] = {"value": u[-1][1], "asOf": u[-1][0][:7], "status": "fresh", "source": "FRED UNRATE"}
    except Exception as e:
        ind["unemployment"] = keep_previous(prev, "unemployment", f"fetch-failed: {str(e)[:160]}")

    try:
        value, when = cpi_yoy(fred("CPIAUCSL", fx))
        ind["cpiYoy"] = {"value": value, "asOf": when[:7], "status": "fresh", "source": "FRED CPIAUCSL, YoY computed"}
    except Exception as e:
        ind["cpiYoy"] = keep_previous(prev, "cpiYoy", f"fetch-failed: {str(e)[:160]}")

    fomc = next_fomc(now_et.date())
    macro = {"generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "priceSession": session, "indicators": ind,
             "nextFomc": fomc, "fomcScheduleThrough": FOMC_THROUGH}

    for key, v in ind.items():
        shown = v.get("value", f"{v.get('lower')}-{v.get('upper')}" if "upper" in v else None)
        print(f"{key:13} {v['status']:11} {str(shown):>12}  {v.get('asOf', '')}  {v.get('statusReason', '')}")
    print(f"next FOMC {fomc}" if fomc else f"WARNING: FOMC schedule exhausted (through {FOMC_THROUGH}) - add next year's dates")
    if args.write:
        # same as fetch_prices.py: no rewrite when only generatedAt would change
        if prev is not None and ({k: v for k, v in prev.items() if k != "generatedAt"}
                                 == {k: v for k, v in macro.items() if k != "generatedAt"}):
            print(f"No change - {out.name} left as is")
            return
        out.write_text(json.dumps(macro, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {out}")
    else:
        print("Dry run - pass --write to update macro.json")


if __name__ == "__main__":
    main()
