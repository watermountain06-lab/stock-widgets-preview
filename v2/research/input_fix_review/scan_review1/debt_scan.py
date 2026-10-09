# F4: 엔진 차입금(기본 경로) < 0.5 × 같은 종료일 LongTermDebt 인 종목·날짜, 그 날짜의 세부 태그 구성, LongTermDebt가 총액인지 비유동만인지.
import sys, os, json, io, contextlib, glob
sys.path.insert(0, "/private/tmp/claude-501/-Users-watermountain-Workspace-second-brain/bbfd380b-94a7-4972-94ba-641e4f0c0be6/scratchpad/rfv/fable")
import helper as H
bmh = H.bmh
cards = {os.path.basename(p).replace("_full_widget.html", "") for p in glob.glob("/Users/watermountain/Workspace/stock-widgets-preview/v2/*_full_widget.html")}
TAGS = ["LongTermDebt", "LongTermDebtCurrent", "LongTermDebtNoncurrent", "ShortTermBorrowings", "CommercialPaper", "DebtCurrent",
        "LongTermDebtAndCapitalLeaseObligations", "LongTermDebtAndCapitalLeaseObligationsCurrent", "OtherShortTermBorrowings", "DebtLongtermAndShorttermCombinedAmount"]
def inst(data, tag):
    b = {}
    for e in data["facts"].get("us-gaap", {}).get(tag, {}).get("units", {}).get("USD", []):
        if "start" in e: continue
        if e["end"] not in b or e["filed"] < b[e["end"]]["filed"]: b[e["end"]] = e
    return b
hits = []
targets = ["LIN", "A", "ADI", "DRI", "EQIX", "KLAC", "OMC", "PTC", "RMD", "TRMB", "TTWO", "VTR"]
for t in sorted(H.UNI):
    try:
        cik, data, pj = H.setup(t)
    except Exception as e:
        continue
    if cik in bmh.DEBT_TOTAL_TAG or cik in bmh.EV_TAGS_BY_CIK and "debt" in bmh.EV_TAGS_BY_CIK[cik]:
        if t in targets: print("NOTE target in hand list:", t)
        continue
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            ser = bmh.ev_component(cik, "debt", bmh.EV_COMPONENTS["debt"])
        except Exception as e:
            continue
    eng = {}
    for e in ser:
        if e["end"] not in eng or e["available"] < eng[e["end"]]["available"]: eng[e["end"]] = e
    tot = inst(data, "LongTermDebt")
    m = {tag: inst(data, tag) for tag in TAGS[1:]}
    for end, te in sorted(tot.items()):
        if end < "2017-01-01" or te["val"] <= 0: continue
        ev = eng.get(end)
        if ev is None or ev["val"] < 0.5 * te["val"]:
            parts = {k[:14]: round(m[k][end]["val"] / 1e9, 2) for k in TAGS[1:] if end in m[k]}
            nc = m["LongTermDebtNoncurrent"].get(end)
            kind = ("=NC" if nc and abs(nc["val"] - te["val"]) <= 0.01 * te["val"] else ("TOT>NC" if nc else "?"))
            hits.append((t, "CARD" if t in cards else "", end, round((ev["val"] if ev else 0) / 1e9, 2), round(te["val"] / 1e9, 2), kind, parts))
print("# engine debt < 0.5×LongTermDebt (same end), 2017+ :", len(hits), "rows,", len({h[0] for h in hits}), "tickers")
import collections
by = collections.defaultdict(list)
for h in hits: by[h[0]].append(h)
for t in sorted(by, key=lambda x: (x not in targets, x)):
    hs = by[t]
    print(f"{t} {hs[0][1]} n={len(hs)} ends {hs[0][2]}..{hs[-1][2]} kinds={collections.Counter(h[5] for h in hs)}")
    for h in hs[:3]: print("    ", h[2], "engine", h[3], "LTD", h[4], h[5], h[6])
print("\n# tickers hit:", sorted(by))
print("# cards hit:", sorted(t for t in by if t in cards))
# LIN detail
cik, data, pj = H.setup("LIN")
for end in ("2022-06-30", "2022-09-30", "2022-12-31", "2023-03-31"):
    print("LIN", end, {k: round(inst(data, k)[end]["val"] / 1e9, 3) for k in TAGS if end in inst(data, k)})
