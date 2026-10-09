# 회귀 후보 종목의 Revenues/Excl 연간 값, CPT 태그 구성, HAL 10-K EPS 행과 pit.eps_ttm 창 간격. 가격·수익률 안 씀.
import sys, os, json
from datetime import date
sys.path.insert(0, "/Users/watermountain/Workspace/stock-widgets-preview/v2/research")
import pit
R = "/Users/watermountain/Workspace/stock-widgets-preview/v2/research"
SP = "/Users/watermountain/Workspace/stock-widgets-redesign/scripts/sp500.json"
uni = {r["ticker"]: r["cik"].zfill(10) for r in json.load(open(SP))}
TAGS = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet"]
SH = {"Revenues": "Rev", "RevenueFromContractWithCustomerExcludingAssessedTax": "Excl", "RevenueFromContractWithCustomerIncludingAssessedTax": "Incl", "SalesRevenueNet": "SRN"}
def days(e):
    return (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days if "start" in e else -1
def load(t):
    return json.load(open(os.path.join(R, ".facts_20261002", f"{uni[t]}_facts.json")))
def first_annual(fx, tag):
    b = {}
    for e in fx.get(tag, {}).get("units", {}).get("USD", []):
        if "start" in e and days(e) > 350:
            if e["end"] not in b or e["filed"] < b[e["end"]]["filed"]: b[e["end"]] = e
    return b
for t in ("CVX", "BLK", "GIS", "NTAP", "EQT", "WMB", "DVN", "XOM", "UNP", "VST"):
    fx = load(t)["facts"]["us-gaap"]
    rev, exc = first_annual(fx, "Revenues"), first_annual(fx, TAGS[1])
    ks = sorted(set(rev) | set(exc))
    print(t, [(k[:7], round(rev[k]["val"] / 1e9, 1) if k in rev else None, round(exc[k]["val"] / 1e9, 1) if k in exc else None) for k in ks if k >= "2017"])
print("\nCPT tags with 'Revenue' in name (annual first-filed, 2018+):")
fx = load("CPT")["facts"]["us-gaap"]
for tag in sorted(fx):
    if "Revenue" in tag or "LeaseIncome" in tag:
        b = first_annual(fx, tag)
        if b: print("  ", tag, [(k[:7], round(v["val"] / 1e6)) for k, v in sorted(b.items()) if k >= "2018"])
print("\nHAL EPS rows days>350 (first filed):")
data = load("HAL"); fx = data["facts"]["us-gaap"]
b = {}
for e in fx["EarningsPerShareDiluted"]["units"]["USD/shares"]:
    if "start" in e and days(e) > 350:
        k = (e["start"], e["end"])
        if k not in b or e["filed"] < b[k]["filed"]: b[k] = e
print("  ", [(k, v["val"], v["filed"], v.get("form")) for k, v in sorted(b.items()) if k[1] >= "2020"])
pj = json.load(open(os.path.join(R, ".prices10y", "HAL.json")))
out = pit.eps_ttm(pit.filtered(data, "2024-03-31"), pj.get("splits") or [])
print("  pit.eps_ttm HAL (asof 2024-03-31) last 10:", [(e["quarter_end"], e["val"], e["available"]) for e in out[-10:]])
# span check across universe: how many eps_ttm windows span > 310 days (quarter gap) at full data
import collections
bad = collections.Counter(); tot = 0
for t, cik in sorted(uni.items()):
    p = os.path.join(R, ".facts_20261002", f"{cik}_facts.json"); pp = os.path.join(R, ".prices10y", f"{t}.json")
    if not os.path.exists(p) or not os.path.exists(pp): continue
    d = json.load(open(p))
    rows = d.get("facts", {}).get("us-gaap", {}).get("EarningsPerShareDiluted", {}).get("units", {}).get("USD/shares", [])
    if not rows: continue
    try:
        o = pit.eps_ttm(d, json.load(open(pp)).get("splits") or [])
    except Exception as ex:
        continue
    # reconstruct spans: eps_ttm doesn't expose; approximate by consecutive quarter_end gaps in output
    ends = sorted(e["quarter_end"] for e in o)
    for a, bq in zip(ends, ends[1:]):
        tot += 1
        if (date.fromisoformat(bq) - date.fromisoformat(a)).days > 100 and bq >= "2016":
            bad[t] += 1
print("\nTTM EPS consecutive quarter_end gaps > 100 days (2016+): tickers", len(bad), "windows", sum(bad.values()), "of", tot)
print("  top:", bad.most_common(25))
