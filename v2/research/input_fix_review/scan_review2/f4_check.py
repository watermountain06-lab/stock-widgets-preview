# F4 2판 규칙을 비금융 전 종목(손 목록 경로 포함)에 적용: 트리거(엔진 없음 또는 < 0.5×LongTermDebt) → ① 총계 태그 ② LTD+STB/CP
# (STB_INCLUDES: LTDNoncurrent(없으면 LTD−LTDCurrent)+STB, DEBT_NONCURRENT_ONLY: +DebtCurrent). 가격·수익률 안 씀.
import sys, os, json, io, contextlib, glob, collections
sys.path.insert(0, "/private/tmp/claude-501/-Users-watermountain-Workspace-second-brain/bbfd380b-94a7-4972-94ba-641e4f0c0be6/scratchpad/rfv/fable")
import helper as H
bmh, vr = H.bmh, H.vr
STB_INC = vr.d.STB_INCLUDES_CURRENT_LTD
cards = {os.path.basename(p).replace("_full_widget.html", "") for p in glob.glob("/Users/watermountain/Workspace/stock-widgets-preview/v2/*_full_widget.html")}
sec = {r["ticker"]: r.get("sector") for r in json.load(open(vr.v.SP500))}
EXCL = {"CAT", "DE", "BX", "VRTX"}
def inst(data, tag):
    b = {}
    for e in data["facts"].get("us-gaap", {}).get(tag, {}).get("units", {}).get("USD", []):
        if "start" in e: continue
        if e["end"] not in b or e["filed"] < b[e["end"]]["filed"]: b[e["end"]] = e
    return b
res = collections.defaultdict(list); dc_unused = collections.Counter()
for t in sorted(H.UNI):
    if sec.get(t) == "Financials" or t in EXCL: continue
    try:
        cik, data, pj = H.setup(t)
    except Exception:
        continue
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            ser = bmh.ev_component(cik, "debt", bmh.EV_COMPONENTS["debt"])
        except Exception:
            continue
    eng = {}
    for e in ser:
        if e["end"] not in eng or e["available"] < eng[e["end"]]["available"]: eng[e["end"]] = e
    ltd = inst(data, "LongTermDebt"); comb = inst(data, "DebtLongtermAndShorttermCombinedAmount")
    stb = inst(data, "ShortTermBorrowings"); cp = inst(data, "CommercialPaper"); nc = inst(data, "LongTermDebtNoncurrent")
    ltdc = inst(data, "LongTermDebtCurrent"); dcur = inst(data, "DebtCurrent")
    for end, te in sorted(ltd.items()):
        if end < "2017-01-01" or te["val"] <= 0: continue
        ev = eng.get(end)
        if ev is not None and ev["val"] >= 0.5 * te["val"]: continue
        short = stb.get(end, cp.get(end)); sv = short["val"] if short else 0.0
        if end in comb:
            how, val = "①comb", comb[end]["val"]
        elif cik in STB_INC:
            base = nc[end]["val"] if end in nc else te["val"] - (ltdc[end]["val"] if end in ltdc else 0.0)
            how, val = "②stbinc", base + sv
        elif cik in bmh.DEBT_NONCURRENT_ONLY:
            how, val = "②nconly", te["val"] + sv + (dcur[end]["val"] if end in dcur else 0.0)
        else:
            how, val = "②ltd+stb", te["val"] + sv
        if how == "②ltd+stb" and end in dcur and not short and dcur[end]["val"] > 0.05 * te["val"]:
            dc_unused[t] += 1
        res[t].append((end, round((ev["val"] if ev else 0) / 1e9, 3), round(te["val"] / 1e9, 3), how, round(val / 1e9, 3),
                       "DC=%.2f" % (dcur[end]["val"] / 1e9) if end in dcur else ""))
print("# non-financial tickers triggered:", len(res), "rows:", sum(len(v) for v in res.values()))
print("# by path:", collections.Counter(r[3] for v in res.values() for r in v))
print("# cards triggered:", sorted(t for t in res if t in cards))
print("# DebtCurrent present (>5% LTD) but rule ② ignores it (no STB/CP):", dict(dc_unused))
for t in ["LIN", "KLAC", "RMD", "TRMB", "TTWO", "OMC", "VTR", "EQIX", "PTC", "A", "DRI", "ADI", "LITE", "HWM", "KVUE", "AME", "CHRW", "INTU", "CPAY"]:
    v = res.get(t)
    if not v: print(t, "not triggered"); continue
    print(t, sec.get(t), "CARD" if t in cards else "", f"n={len(v)}", v[:3], "..." if len(v) > 3 else "", v[-1] if len(v) > 3 else "")
print("\n# all triggered tickers:", {t: len(v) for t, v in res.items()})
