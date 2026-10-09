# F3: HAL EPS 행, PKG·TER·DLR·CCL 가중평균/표지 값, 전 종목 가중평균 단위·비율 구간 점검. 가격·수익률 안 씀.
import json, os, glob, sys
from datetime import date
R = "/Users/watermountain/Workspace/stock-widgets-preview/v2/research"
SP = "/Users/watermountain/Workspace/stock-widgets-redesign/scripts/sp500.json"
cards = {os.path.basename(p).replace("_full_widget.html", "") for p in glob.glob("/Users/watermountain/Workspace/stock-widgets-preview/v2/*_full_widget.html")}
uni = {r["ticker"]: r["cik"].zfill(10) for r in json.load(open(SP))}
def days(e):
    return (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days if "start" in e else -1
def load(t):
    return json.load(open(os.path.join(R, ".facts_20261002", f"{uni[t]}_facts.json")))["facts"]

print("=== HAL EarningsPerShareDiluted (first filed per period) 2021-12..2024-12 ===")
fx = load("HAL")["us-gaap"]
b = {}
for e in fx["EarningsPerShareDiluted"]["units"]["USD/shares"]:
    if "start" not in e: continue
    k = (e["start"], e["end"])
    if k not in b or e["filed"] < b[k]["filed"]: b[k] = e
for k, e in sorted(b.items(), key=lambda x: x[0][1]):
    if "2021-12" <= k[1] <= "2024-12": print("  ", k, days(e), e["val"], e["filed"], e.get("form"))
print("  all filings for Q3 2023 (2023-07-01..2023-09-30):", [(e["val"], e["filed"], e.get("form")) for e in fx["EarningsPerShareDiluted"]["units"]["USD/shares"] if e.get("start") == "2023-07-01" and e["end"] == "2023-09-30"])
for tag in ("NetIncomeLoss", "WeightedAverageNumberOfDilutedSharesOutstanding"):
    rows = [e for e in fx.get(tag, {}).get("units", {}).get(list(fx.get(tag, {}).get("units", {"USD": []}).keys())[0], []) if "start" in e and 80 <= days(e) <= 100 and "2022-01" <= e["end"] <= "2024-12"]
    b2 = {}
    for e in rows:
        if e["end"] not in b2 or e["filed"] < b2[e["end"]]["filed"]: b2[e["end"]] = e
    print("  ", tag, [(k, v["val"], v["filed"]) for k, v in sorted(b2.items())][:12])

print("\n=== cover vs weighted diluted (quarterly) — target tickers ===")
def wa_q(fx):
    rows = [e for e in fx.get("us-gaap", {}).get("WeightedAverageNumberOfDilutedSharesOutstanding", {}).get("units", {}).get("shares", []) if "start" in e and 80 <= days(e) <= 100]
    b = {}
    for e in rows:
        if e["end"] not in b or e["filed"] < b[e["end"]]["filed"]: b[e["end"]] = e
    return b
def cover(fx):
    rows = fx.get("dei", {}).get("EntityCommonStockSharesOutstanding", {}).get("units", {}).get("shares", [])
    b = {}
    for e in rows:
        if "start" in e: continue
        if e["end"] not in b or e["filed"] < b[e["end"]]["filed"]: b[e["end"]] = e
    return b
for t, lo, hi in (("PKG", "2022-12", "2023-09"), ("TER", "2023-06", "2024-03"), ("DLR", "2022-01", "2023-09"), ("CCL", "2022-06", "2023-03"), ("CMG", "2022-01", "2022-09"), ("FOX", "2019-01", "2019-12"), ("SPG", "2012-06", "2013-06")):
    fx = load(t); w = wa_q(fx); c = cover(fx)
    print(t, "wa:", [(k, v["val"], v["filed"]) for k, v in sorted(w.items()) if lo <= k <= hi])
    print("   cover:", [(k, v["val"], v["filed"]) for k, v in sorted(c.items()) if lo <= k <= hi])

print("\n=== scan: quarterly weighted diluted < 1e7 (unit suspects) and cover/wa ratio bands on wa >= 1e7 ===")
small = []; band = []
for t, cik in sorted(uni.items()):
    p = os.path.join(R, ".facts_20261002", f"{cik}_facts.json")
    if not os.path.exists(p): continue
    fx = json.load(open(p))["facts"]; w = wa_q(fx); c = cover(fx)
    cov = sorted(c.items())
    for k, v in sorted(w.items()):
        if k < "2016": continue
        # nearest cover at/after quarter end within 120 days
        cv = next((x for x in cov if x[0] >= k and (date.fromisoformat(x[0]) - date.fromisoformat(k)).days <= 120), None)
        ratio = (cv[1]["val"] / v["val"]) if (cv and v["val"]) else None
        if v["val"] < 1e7:
            small.append((t, "CARD" if t in cards else "", k, v["val"], cv[1]["val"] if cv else None, round(ratio, 1) if ratio else None))
        elif ratio and (500 <= ratio <= 2000 or 5e5 <= ratio <= 2e6):
            band.append((t, "CARD" if t in cards else "", k, v["val"], cv[1]["val"], round(ratio, 1)))
print("wa < 1e7:", len(small))
for s in small: print("  ", s)
print("wa >= 1e7 but cover/wa in draft bands (draft (b) would scale wa up — PKG-type):", len(band))
for s in band: print("  ", s)
