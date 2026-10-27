#!/usr/bin/env python3
"""연구 SEC 스냅샷에 지금 엔진 태그를 채운다 — .facts_20261002 → .facts_20261002_t1026 (2026-10-26).

10-02 스냅샷은 그때 엔진 소스에 적힌 태그만 남겼다. 그 뒤 카드 세션·엔진 수정이 쓰기 시작한 태그 47개
(제한현금·건설 중 설비투자·상환가능 비지배지분·회사별 차입금 등)가 없어 패널이 카드와 다른 값을 냈다
(ED 설비투자 None, UAL 차입금 2014 값으로 보류 등 — five_year_gate_prereg.md 2026-10-26 재봉인).

- 옛 파일의 태그는 한 줄도 바꾸지 않는다. 옛 파일에 **없는** 엔진 태그만 새로 받은 companyfacts에서 넣는다.
- 넣는 행도 공시일(filed)이 CUTOFF 이하인 것만 — 결과는 "10-02 시점 자료를 지금 태그 목록으로 받은 것"이다.
- 재개 가능 — 이미 만든 종목은 건너뛴다. 받은 원본은 남기지 않는다.

    python3 v2/research/refresh_facts_tags.py
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_universe_facts as fuf  # noqa: E402

OLD = os.path.join(HERE, ".facts_20261002")
NEW = os.path.join(HERE, ".facts_20261002_t1026")
CUTOFF = "2026-10-02"
UA = "stock-widgets research gptjhss@gmail.com"


def main():
    os.makedirs(NEW, exist_ok=True)
    keep = fuf.wanted_tags()
    log = {"cutoff": CUTOFF, "tags": sorted(keep), "added": {}, "errors": []}
    files = sorted(f for f in os.listdir(OLD) if f.endswith("_facts.json"))
    for k, fn in enumerate(files):
        dst = os.path.join(NEW, fn)
        if os.path.exists(dst):
            continue
        old = json.load(open(os.path.join(OLD, fn)))
        cik = fn.split("_")[0]
        r = subprocess.run(["curl", "-s", "-A", UA, f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"], capture_output=True)
        try:
            facts = json.loads(r.stdout).get("facts", {})
        except Exception as e:
            log["errors"].append([cik, str(e)[:80]]); time.sleep(1); continue
        added = []
        for ns in ("us-gaap", "dei"):
            have = old["facts"].setdefault(ns, {})
            for tag, v in facts.get(ns, {}).items():
                if tag not in keep or tag in have:
                    continue
                units = {u: [x for x in rows if x.get("filed", "9999") <= CUTOFF] for u, rows in v.get("units", {}).items()}
                units = {u: rows for u, rows in units.items() if rows}
                if units:
                    have[tag] = {**{a: b for a, b in v.items() if a != "units"}, "units": units}
                    added.append(tag)
        json.dump(old, open(dst, "w"))
        if added:
            log["added"][cik] = sorted(added)
        if k % 50 == 0:
            print(k, cik, len(added), flush=True)
        time.sleep(0.15)
    lp = os.path.join(NEW, "_refresh_log.json")
    if os.path.exists(lp):   # 재개했으면 앞 기록과 합친다
        prev = json.load(open(lp)); prev["added"].update(log["added"]); prev["errors"] += log["errors"]; log = prev
    json.dump(log, open(lp, "w"), indent=1)
    print("완료 — 태그를 더한 종목", len(log["added"]), "오류", len(log["errors"]))


if __name__ == "__main__":
    main()
