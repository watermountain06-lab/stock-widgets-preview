#!/usr/bin/env python3
"""ASML 분기 재무(US GAAP, 유로) 원문 받기 — 매 분기 6-K에 붙는 "Financial Statements US GAAP" 첨부(EX-99.3).

ASML은 SEC에 20-F(연간)만 XBRL로 내서 companyfacts에 분기 값이 없다(단위도 EUR). 대신 분기 6-K의
US GAAP 요약 재무제표에 "Quarterly Summary"(최근 5개 분기 손익·재무상태·현금흐름)가 실린다(2026-09-28).

    python3 v2/adapters/asml_reports.py    → v2/adapters/asml_manifest.json, v2/.sec_cache/asml_reports/*.htm
"""
import json
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
OUT = os.path.join(V2, ".sec_cache", "asml_reports")
MANIFEST = os.path.join(HERE, "asml_manifest.json")
CIK = "0000937966"
UA = "kim research gptjhss@gmail.com"
SINCE = "2020-01-01"


def get(url):
    r = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, check=True).stdout
    time.sleep(0.15)
    return r


def main():
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{CIK}.json"))["filings"]
    pages = [sub["recent"]] + [json.loads(get(f"https://data.sec.gov/submissions/{f['name']}"))
                               for f in sub.get("files", []) if f.get("filingTo", "9999") >= SINCE]
    rows = sorted({x for p in pages for x in zip(p["form"], p["accessionNumber"], p["filingDate"], p["acceptanceDateTime"])}, key=lambda x: x[2])
    man = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else []
    have = {m["accn"] for m in man}
    os.makedirs(OUT, exist_ok=True)
    for form, acc, filed, acpt in rows:
        if form != "6-K" or filed < SINCE or acc in have:
            continue
        idx = None
        for _ in range(4):                      # SEC가 가끔 빈 응답(요청 제한)을 준다
            try:
                idx = json.loads(get(f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{acc.replace('-', '')}/index.json"))
                break
            except json.JSONDecodeError:
                time.sleep(3)
        if idx is None:
            print("  ⚠ 목록 실패:", filed, acc)
            continue
        names = [it["name"] for it in idx["directory"]["item"] if it["name"].lower().endswith(".htm")]
        cand = [n for n in names if "usgaa" in n.lower() or ("financialstatements" in n.lower() and "ifrs" not in n.lower())]
        if not cand:
            continue
        n = cand[0]
        path = os.path.join(OUT, f"{filed}_{n}")
        open(path, "wb").write(get(f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{acc.replace('-', '')}/{n}"))
        man.append({"filed": filed, "accepted": acpt, "accn": acc, "file": os.path.basename(path)})
        print("추가:", filed, acc, n)
        json.dump(sorted(man, key=lambda m: m["filed"]), open(MANIFEST, "w"), indent=1)
    man.sort(key=lambda m: m["filed"])
    json.dump(man, open(MANIFEST, "w"), indent=1)
    print(len(man), "건")


if __name__ == "__main__":
    main()
