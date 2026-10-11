import sys, os, json
R = "/Users/watermountain/Workspace/stock-widgets-preview/v2/research"
sys.path.insert(0, R); os.chdir(R)
import verdict_replay as vr
KEEP = set(sys.argv[1].split(",")); DAYS = sys.argv[2].split(",")
vr.START_MONTH, vr.END_MONTH, vr.BAR_START, vr.DCF_WINDOW, vr.HASH_LEN = "2022-10", "2022-10", "2016-01-01", "rolling", 64
vr.provenance = lambda: {}
allt = {r["ticker"] for r in json.load(open(vr.v.SP500))}
vr.v.EXCLUDE = set(vr.v.EXCLUDE) | (allt - KEEP)
d = vr.d; orig = d.scenarios; out = sys.__stdout__
def spy(b, h, *a, **k):
    sc = orig(b, h, *a, **k)
    keys = ["ticker", "revenue", "opinc", "capex", "da", "sbc", "nwc", "acquisitions", "net_debt", "debt", "cash", "shares", "tax_rate", "leases", "reinvest", "s2c"]
    print("BASE", {kk: b.get(kk) for kk in b if not isinstance(b.get(kk), (list, dict))}, file=out)
    print("HIST", {kk: h.get(kk) for kk in h if not isinstance(h.get(kk), (list, dict))}, file=out)
    s = sc[1]; print("SC", {kk: s.get(kk) for kk in s if not isinstance(s.get(kk), (list,))}, file=out)
    return sc
d.scenarios = spy
vr.build(os.devnull)
