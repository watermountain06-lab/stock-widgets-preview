# F3 (b) 2판 규칙(WA<1e7이면 {1,1e3,1e6} 중 표지에 가장 가까운 배율, 표지 없으면 지금 규칙) + (a) 0.5~2배 대조를
# 전 종목 분기 WA(2016+)에 적용해 결과를 나열한다. 가격·수익률 안 씀.
import json, os, glob, math
from datetime import date
R = "/Users/watermountain/Workspace/stock-widgets-preview/v2/research"
SP = "/Users/watermountain/Workspace/stock-widgets-redesign/scripts/sp500.json"
cards = {os.path.basename(p).replace("_full_widget.html", "") for p in glob.glob("/Users/watermountain/Workspace/stock-widgets-preview/v2/*_full_widget.html")}
uni = {r["ticker"]: r["cik"].zfill(10) for r in json.load(open(SP))}
days = lambda e: (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days if "start" in e else -1
def wa_q(fx):
    b = {}
    for e in fx.get("us-gaap", {}).get("WeightedAverageNumberOfDilutedSharesOutstanding", {}).get("units", {}).get("shares", []):
        if "start" in e and 80 <= days(e) <= 100 and (e["end"] not in b or e["filed"] < b[e["end"]]["filed"]): b[e["end"]] = e
    return b
def cover(fx):
    b = {}
    for e in fx.get("dei", {}).get("EntityCommonStockSharesOutstanding", {}).get("units", {}).get("shares", []):
        if "start" not in e and (e["end"] not in b or e["filed"] < b[e["end"]]["filed"]): b[e["end"]] = e
    return b
rows = []
for t, cik in sorted(uni.items()):
    p = os.path.join(R, ".facts_20261002", f"{cik}_facts.json")
    if not os.path.exists(p): continue
    fx = json.load(open(p))["facts"]; w = wa_q(fx); c = sorted(cover(fx).items())
    for k, v in sorted(w.items()):
        if k < "2016": continue
        wa = v["val"]
        cv = next((x for x in c if x[0] >= k and (date.fromisoformat(x[0]) - date.fromisoformat(k)).days <= 120), None)
        cov = cv[1]["val"] if cv else None
        # (b)
        if wa < 1e7:
            if cov:
                cands = [(abs(math.log((wa * m) / cov)) if wa > 0 else 9e9, m) for m in (1, 1e3, 1e6)]
                best = min(cands); m = best[1]
                tie = sorted(x[0] for x in cands)
                note = "TIE" if abs(tie[0] - tie[1]) < 1e-6 else ""
            else:
                m = 1e6 if wa < 1e6 else 1; note = "nocover"
            wa2 = wa * m
        else:
            m = 1; wa2 = wa; note = ""
        # (a)
        if cov and wa2 > 0:
            ratio = cov / wa2
            if 0.5 <= ratio <= 2.0: used = "cover"; final = cov
            else: used = "WA"; final = wa2
        elif not cov or cov < 1e7:
            used = "missing"; final = None; ratio = None
        else:
            used = "cover"; final = cov; ratio = None
        if wa < 1e7 or (cov and not (0.5 <= cov / wa <= 2.0)):
            rows.append((t, "CARD" if t in cards else "", k, wa, cov, m, used, final, round(ratio, 3) if ratio else None, note))
print("# rows where (b) or (a) acts (WA<1e7, or cover/WA outside 0.5~2):", len(rows))
flag = [r for r in rows if r[9] in ("TIE",) or r[6] == "missing" or (r[6] == "WA" and r[3] < 1e7) or (r[7] is not None and r[7] < 1e7)]
print("# FLAGGED (tie / missing / WA<1e7 ends up used / final < 1e7):", len(flag))
for r in flag: print("   ", r)
print("\n# all acting rows:")
for r in rows: print("   ", r)
