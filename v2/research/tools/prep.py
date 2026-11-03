#!/usr/bin/env python3
"""카드 준비 한 번에: python3 prep.py TICKER CIK SECTOR "Name" "accent1,accent2,accent3" "sub line" [--register] [--data ASOF]
- 공시 목록(10-Q/10-K·8-K), companyfacts 핵심 태그 최신값
- --register: fetch_eps_history CIKS/KNOWN_SPLITS(분할은 Yahoo에서), activity CIKS, sectors, sec_approved(최근 10-Q/10-K filingDate), meta, cfg 뼈대
- --data ASOF: build.py --data, base_inputs, 낡은 태그, EPS 이력
- 8-K 원문(2025-10 이후) 텍스트를 SP/<t>/k8_*.txt로
"""
import json, os, re, subprocess, sys, time, html, datetime as dt

UA = "stock-widgets research gptjhss@gmail.com"
SP = os.environ.get("CARD_WORK", "/tmp/card_work"); os.makedirs(SP, exist_ok=True)
REPO = os.path.expanduser("~/Workspace/stock-widgets-preview")


def get(url):
    return subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True).stdout


def main():
    T, C, SECTOR, NAME, ACC, SUB = sys.argv[1:7]
    C = C.zfill(10); t = T.lower(); d = os.path.join(SP, t); os.makedirs(d, exist_ok=True)
    flags = sys.argv[7:]
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{C}.json")); open(f"{d}/sub.json", "w").write(json.dumps(sub))
    cf = json.loads(get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{C}.json")); open(f"{d}/cf.json", "w").write(json.dumps(cf))
    r = sub["filings"]["recent"]
    print(sub["name"], "FYE", sub["fiscalYearEnd"])
    last_q = None
    for i in range(len(r["form"])):
        f = r["form"][i]
        if f in ("10-Q", "10-K", "10-Q/A", "10-K/A") and r["filingDate"][i] >= "2025-07":
            print(f, r["filingDate"][i], r["acceptanceDateTime"][i], r["accessionNumber"][i], r["primaryDocument"][i], r["reportDate"][i])
            if last_q is None and not f.endswith("/A"):
                last_q = (r["filingDate"][i], r["accessionNumber"][i], r["primaryDocument"][i], r["reportDate"][i])
        elif f == "8-K" and r["filingDate"][i] >= "2025-09-15":
            print(f, r["filingDate"][i], r["acceptanceDateTime"][i], r["items"][i], r["accessionNumber"][i], r["primaryDocument"][i])
    u = cf["facts"].get("us-gaap", {})
    for tag in ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "OperatingIncomeLoss", "EarningsPerShareDiluted", "NetIncomeLoss",
                "PaymentsToAcquirePropertyPlantAndEquipment", "DepreciationDepletionAndAmortization", "DepreciationAndAmortization", "Depreciation",
                "AmortizationOfIntangibleAssets", "PaymentsForRepurchaseOfCommonStock", "PaymentsOfDividendsCommonStock", "InterestExpense"]:
        if tag in u:
            for un, v in u[tag]["units"].items():
                ends = sorted(set(x["end"] for x in v)); print("  tag", tag, len(ends), ends[-1])
    print("LAST", last_q)
    # Yahoo
    yp = f"{REPO}/v2/newcards/yahoo/{t}.json"
    open(yp, "wb").write(subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", f"https://query1.finance.yahoo.com/v8/finance/chart/{T}?period1=1577836800&period2={int(time.time())}&interval=1d&events=div%2Csplits"], capture_output=True).stdout)
    yd = json.load(open(yp))["chart"]["result"][0]
    splits = sorted((dt.datetime.fromtimestamp(int(k), dt.UTC).date().isoformat(), v["numerator"] / v["denominator"]) for k, v in yd.get("events", {}).get("splits", {}).items())
    print("yahoo", len(yd["timestamp"]), yd["indicators"]["quote"][0]["close"][-3:], "splits", splits)
    if "--register" in flags:
        os.chdir(REPO)
        def ins(p, anchor_re, new):
            s = open(p).read()
            if new.strip() in s:
                return
            m = list(re.finditer(anchor_re, s))
            assert m, (p, anchor_re)
            k = m[-1].end(); s = s[:k] + new + s[k:]; open(p, "w").write(s)
        p = "scripts/fetch_eps_history.py"; s = open(p).read()
        if f'"{T}": "{C}"' not in s:
            s = s.replace('CIKS = {\n', f'CIKS = {{\n    "{T}": "{C}",\n', 1) if 'CIKS = {\n' in s else s
            open(p, "w").write(s)
        s = open(p).read()
        if f'    "{T}": [' not in s:
            spl = ", ".join(f'("{a}", {b})' for a, b in splits if a >= "2010-01-01")
            note = "Yahoo 분할 이벤트와 같음" if spl else "데이터 창(2020~) 안 분할 없음, Yahoo 분할 이벤트 없음"
            s = s.replace("KNOWN_SPLITS = {\n", f'KNOWN_SPLITS = {{\n    "{T}": [{spl}],   # {NAME}: {note}(2026-10-23).\n', 1); open(p, "w").write(s)
        p = "v2/build_activity_score.py"; s = open(p).read()
        if f'"{T}": "{C}"' not in s:
            s2 = re.sub(r'("[A-Z.]+": "\d{10}")\}', lambda m: m.group(1) + f', "{T}": "{C}"}}', s, count=1)
            assert s2 != s; open(p, "w").write(s2)
        p = "v2/sectors.json"; dj = json.load(open(p))
        if T not in dj:
            s = open(p).read().rstrip(); assert s.endswith("}"); s = s[:-1].rstrip() + f',\n  "{T}": "{SECTOR}"\n}}\n'; open(p, "w").write(s)
        p = "v2/sec_approved.json"; dj = json.load(open(p))
        if C not in dj:
            s = open(p).read().rstrip(); assert s.endswith("}"); s = s[:-1].rstrip() + f',\n "{C}": "{last_q[0]}"\n}}\n'; open(p, "w").write(s)
        a = ACC.split(",")
        m = {"accent": a, "sub": SUB, "name": NAME, "current": f"{T} · 시총 순", "prev": "", "next": "<span class=\"back-bar-nav disabled\">다음 ▶</span>"}
        mp = f"v2/newcards/meta/{t}.json"
        if not os.path.exists(mp):
            open(mp, "w").write(json.dumps(m, ensure_ascii=False))
        cp = f"v2/newcards/cfg/cfg_{t}.py"
        if not os.path.exists(cp):
            open(cp, "w").write(f"CIK = '{C}'\n")
    if "--data" in flags:
        asof = flags[flags.index("--data") + 1]
        os.chdir(REPO)
        env = dict(os.environ, REFRESH="1", SYNC_BASE="http://localhost:8777")
        out = subprocess.run(["python3", "v2/newcards/build.py", T, "--data", "--asof", asof], capture_output=True, text=True, env=env)
        open(f"{SP}/{t}_data.log", "w").write(out.stdout + out.stderr)
        for ln in (out.stdout + out.stderr).splitlines():
            if re.search(r"⚠|: 현재|동종업 대비 =|자기 이력 대비 =|Traceback|해당 없음|Error|계산 불가", ln) and "주식 수 대조" not in ln:
                print("  ", ln[:220])
        code = f"""
import sys,json;sys.path.insert(0,'v2')
import build_dcf as b, build_multiple_history as m
x=b.base_inputs('{T}');print(json.dumps({{k:v for k,v in x.items() if not isinstance(v,(list,dict))}},default=str))
for nm,tags in [('rev',m.FLOW_TAGS['revenue']),('op',m.EBITDA_TAGS['opinc'])]:
  u,r=m.pick_tag('{C}',tags); q=m.quarterly_flow(r,'{T}'); print(nm,u,[(z['end'],round(z['val']/1e6)) for z in q][-8:])
d=json.load(open('v2/fundamental_data/{T}_financials.json'))
for k,v in d.items():
  if isinstance(v,dict) and v.get('latestQuarter') and v['latestQuarter']['end']<'{last_q[3]}' and k!='sharesOutstanding': print('stale',k,v['tag'],v['latestQuarter']['end'])
for e in json.load(open('scripts/{T}_eps_history.json'))[-9:]: print(e['quarter_end'],e['fp'],e['quarter_eps'])
"""
        o2 = subprocess.run(["python3", "-c", code], capture_output=True, text=True)
        print("\n".join(l for l in (o2.stdout + o2.stderr).splitlines() if "⚠" not in l))
    if "--k8" in flags:
        cik_n = str(int(C))
        for i in range(len(r["form"])):
            if r["form"][i] != "8-K" or r["filingDate"][i] < "2025-09-15":
                continue
            acc = r["accessionNumber"][i].replace("-", "")
            try:
                idx = json.loads(get(f"https://www.sec.gov/Archives/edgar/data/{cik_n}/{acc}/index.json"))
            except Exception:
                continue
            names = [it["name"] for it in idx["directory"]["item"] if it["name"].endswith(".htm") and not it["name"].startswith("R")]
            for n in names[:3]:
                tx = get(f"https://www.sec.gov/Archives/edgar/data/{cik_n}/{acc}/{n}").decode("utf-8", "ignore")
                tx = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " | ", tx))); tx = re.sub(r"(\|\s*)+", "| ", tx).replace("​", "")
                open(f"{d}/k8_{r['filingDate'][i]}_{acc[-6:]}_{n}.txt", "w").write(tx); time.sleep(0.12)
        # 10-Q 원문
        if last_q:
            tx = get(f"https://www.sec.gov/Archives/edgar/data/{cik_n}/{last_q[1].replace('-', '')}/{last_q[2]}").decode("utf-8", "ignore")
            tx = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " | ", tx))); tx = re.sub(r"(\|\s*)+", "| ", tx).replace("​", "")
            open(f"{d}/10q.txt", "w").write(tx)
            i = tx.find("Total current liabilities"); print("BS>>", tx[max(0, i - 900):i + 900])


if __name__ == "__main__":
    main()
