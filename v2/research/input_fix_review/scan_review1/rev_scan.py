# F2 (a) 회귀 범위: 전체 자료(시점 필터 없음)에서 같은 (start,end)에 Revenues와 ExclAssessedTax가 함께 있는 종목의 비율·공시일 관계.
import json, os, glob, collections, sys
from datetime import date
R = "/Users/watermountain/Workspace/stock-widgets-preview/v2/research"
SP = "/Users/watermountain/Workspace/stock-widgets-redesign/scripts/sp500.json"
cards = {os.path.basename(p).replace("_full_widget.html", "") for p in glob.glob("/Users/watermountain/Workspace/stock-widgets-preview/v2/*_full_widget.html")}
uni = {r["ticker"]: r["cik"].zfill(10) for r in json.load(open(SP))}
TAGS = ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet"]
SH = {"Revenues": "Rev", "RevenueFromContractWithCustomerExcludingAssessedTax": "Excl", "RevenueFromContractWithCustomerIncludingAssessedTax": "Incl", "SalesRevenueNet": "SRN"}
def days(e):
    return (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days if "start" in e else -1
def first_by_period(rows):
    b = {}
    for e in rows:
        if "start" not in e: continue
        d = days(e)
        if not (80 <= d <= 100 or d > 350): continue
        k = (e["start"], e["end"])
        if k not in b or e["filed"] < b[k]["filed"]: b[k] = e
    return b
out = []
for t, cik in sorted(uni.items()):
    p = os.path.join(R, ".facts_20261002", f"{cik}_facts.json")
    if not os.path.exists(p): continue
    fx = json.load(open(p)).get("facts", {}).get("us-gaap", {})
    per = {}
    for tag in TAGS:
        rows = fx.get(tag, {}).get("units", {}).get("USD", [])
        per[tag] = first_by_period(rows)
    rev, exc = per["Revenues"], per[TAGS[1]]
    common = set(rev) & set(exc)
    if common:
        ratios = []
        for k in sorted(common):
            a, b = rev[k]["val"], exc[k]["val"]
            if b:
                ratios.append((k[1], a / b, rev[k]["filed"], exc[k]["filed"]))
        if ratios:
            lo = min(r[1] for r in ratios); hi = max(r[1] for r in ratios)
            n_diff = sum(1 for r in ratios if abs(r[1] - 1) > 0.02)
            n_samefile = sum(1 for r in ratios if abs(r[1] - 1) > 0.02 and r[2] == r[3])
            n_rev_later = sum(1 for r in ratios if abs(r[1] - 1) > 0.02 and r[2] > r[3])
            n_rev_earlier = sum(1 for r in ratios if abs(r[1] - 1) > 0.02 and r[2] < r[3])
            if n_diff:
                ex = [r for r in ratios if abs(r[1] - 1) > 0.02]
                out.append((t, "CARD" if t in cards else "", len(ratios), n_diff, round(lo, 3), round(hi, 3), n_samefile, n_rev_later, n_rev_earlier,
                            ex[0][0], ex[-1][0]))
    # Excl vs Incl/SRN overlap with different value (rank would prefer Excl over them regardless of filing order)
    for other in TAGS[2:]:
        oth = per[other]
        c2 = set(exc) & set(oth)
        dif = [(k[1], round(exc[k]["val"] / oth[k]["val"], 3), exc[k]["filed"], oth[k]["filed"]) for k in sorted(c2) if oth[k]["val"] and abs(exc[k]["val"] / oth[k]["val"] - 1) > 0.02]
        if dif:
            print(f"Excl vs {SH[other]} differ: {t} {'CARD' if t in cards else ''} n={len(dif)} first={dif[0]} last={dif[-1]} excl_filed_later={sum(1 for x in dif if x[2] > x[3])}")
        # Rev vs Incl/SRN
        c3 = set(rev) & set(oth)
        dif = [(k[1], round(rev[k]["val"] / oth[k]["val"], 3), rev[k]["filed"], oth[k]["filed"]) for k in sorted(c3) if oth[k]["val"] and abs(rev[k]["val"] / oth[k]["val"] - 1) > 0.02]
        if dif:
            print(f"Rev vs {SH[other]} differ: {t} {'CARD' if t in cards else ''} n={len(dif)} first={dif[0]} last={dif[-1]} rev_filed_later={sum(1 for x in dif if x[2] > x[3])}")
print("\n# Rev vs Excl differ >2% (ticker, card, n_common, n_diff, min ratio Rev/Excl, max, n_samefiled, n_rev_filed_later, n_rev_filed_earlier, first_end, last_end)")
for o in sorted(out, key=lambda x: x[4]):
    print(o)
print("\n# Rev < 0.98*Excl somewhere (rank rule would pick the SMALLER Revenues):", [o[0] for o in out if o[4] < 0.98])
print("# Rev > 1.02*Excl somewhere:", [o[0] for o in out if o[5] > 1.02])
print("# n_rev_filed_later>0 (Revenues row for that period comes from a later filing → availability shifts):", [(o[0], o[7]) for o in out if o[7]])
