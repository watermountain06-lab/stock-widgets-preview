#!/usr/bin/env python3
"""prep.py --register 되돌리기: python3 unreg.py TICKER CIK"""
import json, os, re, glob, sys
REPO = os.path.expanduser("~/Workspace/stock-widgets-preview")
T, C = sys.argv[1], sys.argv[2].zfill(10); t = T.lower()
os.chdir(REPO)
p = "scripts/fetch_eps_history.py"; s = open(p).read()
s = s.replace(f'    "{T}": "{C}",\n', "")
s = re.sub(rf'    "{re.escape(T)}": \[[^\n]*\n', "", s, count=1)
open(p, "w").write(s)
p = "v2/build_activity_score.py"; s = open(p).read(); s = s.replace(f', "{T}": "{C}"', ""); open(p, "w").write(s)
p = "v2/sectors.json"; s = open(p).read(); s = re.sub(rf',\n  "{re.escape(T)}": "[^"]*"', "", s); open(p, "w").write(s)
p = "v2/sec_approved.json"; s = open(p).read(); s = re.sub(rf',\n "{C}": "[^"]*"', "", s); open(p, "w").write(s)
for f in [f"v2/newcards/cfg/cfg_{t}.py", f"v2/newcards/meta/{t}.json", f"v2/newcards/yahoo/{t}.json", f"scripts/{T}_eps_history.json",
          f"v2/fundamental_data/{T}_financials.json", f"v2/backtest_pre/{T}.json", f"{T}_full_widget.html"] + glob.glob(f"v2/{T}_*"):
    if os.path.exists(f):
        os.remove(f)
for x in ["v2/sectors.json", "v2/sec_approved.json"]:
    json.load(open(x))
print("unregistered", T)
