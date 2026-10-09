# GD 2017~2018 TTM 절반의 원인, ORCL 2018-05-31 행, PM·MA·NVDA 태그 구성. 가격·수익률 안 씀.
import sys, os, json, io, contextlib
sys.path.insert(0, "/private/tmp/claude-501/-Users-watermountain-Workspace-second-brain/bbfd380b-94a7-4972-94ba-641e4f0c0be6/scratchpad/rfv/fable")
import helper as H
from datetime import date
bmh, pit = H.bmh, H.pit
TAGS = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet"]
SH = {"Revenues": "Rev", "RevenueFromContractWithCustomerExcludingAssessedTax": "Excl", "RevenueFromContractWithCustomerIncludingAssessedTax": "Incl", "SalesRevenueNet": "SRN"}
def days(e):
    return (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days if "start" in e else -1

def raw_rows(data, lo, hi, tags=TAGS):
    fx = data["facts"]["us-gaap"]
    for tag in tags:
        for e in fx.get(tag, {}).get("units", {}).get("USD", []):
            if "start" in e and lo <= e["end"] <= hi:
                yield SH.get(tag, tag), e["start"], e["end"], days(e), e["val"] / 1e6, e["filed"], e.get("form"), e.get("fp")

def engine_q(t, asof):
    cik, data, pj = H.setup(t)
    state = H.filed_state(data, asof)
    pit.install(bmh, cik, data, state, ref=asof)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            tag, rows = bmh.pick_tag(cik, bmh.FLOW_TAGS["revenue"])
            q = bmh.quarterly_flow(rows, t)
            ttm = bmh.ttm_series(q)
    finally:
        pit.reset(bmh)
    return state, tag, q, ttm, data

print("=== GD at asof 2018-07-31 ===")
state, tag, q, ttm, data = engine_q("GD", "2018-07-31")
print("state", state, "tags", tag)
for e in q:
    if "2016-06" <= e["end"] <= "2018-09": print("  q", e["end"], e.get("start"), round(e["val"] / 1e6), e["filed"])
for e in ttm:
    if "2016-12" <= e["end"] <= "2018-09": print("  ttm", e["end"], round(e["val"] / 1e6), e["available"])
print("raw GD rows 2017-01..2018-07 (filed<=2018-07-31):")
for r in sorted(raw_rows(data, "2017-01-01", "2018-07-31")):
    if r[5] <= "2018-07-31": print("  ", r)

print("\n=== ORCL rows end 2018-05-31 / 2018-02-28 ===")
cik, data, pj = H.setup("ORCL")
for r in sorted(raw_rows(data, "2018-02-01", "2018-05-31")): print("  ", r)
state, tag, q, ttm, _ = engine_q("ORCL", "2018-09-30")
print("engine q (asof 2018-09-30):", [(e["end"], round(e["val"] / 1e6)) for e in q if "2017-05" <= e["end"] <= "2018-09"])
print("engine ttm:", [(e["end"], round(e["val"] / 1e6), e["available"]) for e in ttm if "2017-05" <= e["end"] <= "2018-09"])

print("\n=== PM tag inventory (annual rows, first filed) ===")
cik, data, pj = H.setup("PM")
fx = data["facts"]["us-gaap"]
for tag in TAGS:
    rows = [e for e in fx.get(tag, {}).get("units", {}).get("USD", []) if "start" in e and days(e) > 350]
    b = {}
    for e in rows:
        k = e["end"]
        if k not in b or e["filed"] < b[k]["filed"]: b[k] = e
    print(" ", SH[tag], [(k, round(v["val"] / 1e9, 1), v["filed"]) for k, v in sorted(b.items()) if k >= "2015"])
print("PM quarterly rows 2017-04..2018-12 (all tags):")
for r in sorted(raw_rows(data, "2017-04-01", "2018-12-31")):
    if 80 <= r[3] <= 100: print("  ", r)
state, tag, q, ttm, _ = engine_q("PM", "2019-03-31")
print("engine PM ttm (asof 2019-03-31):", [(e["end"], round(e["val"] / 1e9, 1), e["available"]) for e in ttm if e["end"] >= "2017-06"])

print("\n=== MA annual rows ===")
cik, data, pj = H.setup("MA")
fx = data["facts"]["us-gaap"]
for tag in TAGS:
    rows = [e for e in fx.get(tag, {}).get("units", {}).get("USD", []) if "start" in e and days(e) > 350]
    b = {}
    for e in rows:
        k = e["end"]
        if k not in b or e["filed"] < b[k]["filed"]: b[k] = e
    print(" ", SH[tag], [(k, round(v["val"] / 1e9, 2), v["filed"]) for k, v in sorted(b.items()) if k >= "2016"])

print("\n=== NVDA: periods where both Rev and Excl exist, filed dates ===")
cik, data, pj = H.setup("NVDA")
fx = data["facts"]["us-gaap"]
def firstmap(tag):
    b = {}
    for e in fx.get(tag, {}).get("units", {}).get("USD", []):
        if "start" not in e or not (80 <= days(e) <= 100 or days(e) > 350): continue
        k = (e["start"], e["end"])
        if k not in b or e["filed"] < b[k]["filed"]: b[k] = e
    return b
rev, exc = firstmap("Revenues"), firstmap(TAGS[1])
for k in sorted(set(rev) & set(exc)):
    print("  ", k, round(rev[k]["val"] / 1e6), rev[k]["filed"], "| excl", round(exc[k]["val"] / 1e6), exc[k]["filed"])
print("  Excl periods:", min(k[1] for k in exc), "~", max(k[1] for k in exc), "| Rev periods:", min(k[1] for k in rev), "~", max(k[1] for k in rev))
