import sys, os, json, builtins, io, time
which = sys.argv[1]
R = "/Users/watermountain/Workspace/stock-widgets-preview/v2/research"
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, R); os.chdir(R)
reads = set(); _open = builtins.open
def lopen(f, mode="r", *a, **k):
    if isinstance(f, (str, bytes, os.PathLike)) and not any(c in mode for c in "wax+"):
        reads.add(os.path.realpath(f))
    return _open(f, mode, *a, **k)
builtins.open = lopen; io.open = lopen
import verdict_replay as vr
if which == "test":
    vr.START_MONTH, vr.END_MONTH, vr.BAR_START, vr.DCF_WINDOW, vr.HASH_LEN = "2021-10", "2024-03", "2016-01-01", "rolling", 64
t0 = time.time()
meta, rows = vr.build(os.path.join(OUT, f"{which}_panel.json"))
json.dump(sorted(reads), _open(os.path.join(OUT, f"{which}_reads.json"), "w"), indent=0)
ref = json.load(_open(f"/Users/watermountain/Workspace/stock-widgets-preview/.regress_20261010/panels/f4_{which}.json"))["rows"]
print(which, "rows", len(rows), "f4", len(ref), "identical", rows == ref, "sec", round(time.time() - t0), flush=True)
if rows != ref:
    d = [(a["t"], a["m"]) for a, b in zip(rows, ref) if a != b]; print("diff", len(d), d[:20])
