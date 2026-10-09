import sys, os, json, io, contextlib
sys.path.insert(0, "/private/tmp/claude-501/-Users-watermountain-Workspace-second-brain/bbfd380b-94a7-4972-94ba-641e4f0c0be6/scratchpad/rfv/fable")
import helper as H
bmh = H.bmh
def inst(data, tag):
    b = {}
    for e in data["facts"].get("us-gaap", {}).get(tag, {}).get("units", {}).get("USD", []):
        if "start" in e: continue
        if e["end"] not in b or e["filed"] < b[e["end"]]["filed"]: b[e["end"]] = e
    return b
for t in ["ADI", "APH", "IBM", "PH", "LIN", "KLAC"]:
    cik, data, pj = H.setup(t)
    with contextlib.redirect_stdout(io.StringIO()):
        ser = bmh.ev_component(cik, "debt", bmh.EV_COMPONENTS["debt"])
    eng = {}
    for e in ser:
        if e["end"] not in eng or e["available"] < eng[e["end"]]["available"]: eng[e["end"]] = e
    ltd = inst(data, "LongTermDebt"); comb = inst(data, "DebtLongtermAndShorttermCombinedAmount"); stb = inst(data, "ShortTermBorrowings"); cp = inst(data, "CommercialPaper")
    hits = []
    for end, te in sorted(ltd.items()):
        if end < "2017-01-01" or te["val"] <= 0: continue
        ev = eng.get(end)
        if ev is not None and ev["val"] >= 0.5 * te["val"]: continue
        s = stb.get(end, cp.get(end)); sv = s["val"] if s else 0
        hits.append((end, round((ev["val"] if ev else 0)/1e9, 2), round(te["val"]/1e9, 2), "comb" if end in comb else "ltd+stb", round((comb[end]["val"] if end in comb else te["val"] + sv)/1e9, 2)))
    print(t, "hand" if cik in bmh.DEBT_TOTAL_TAG else "default", len(hits), [h for h in hits if h[0] >= "2021-06"] or hits[-2:])
