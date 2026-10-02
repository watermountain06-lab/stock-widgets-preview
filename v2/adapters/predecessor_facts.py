#!/usr/bin/env python3
"""지주회사 재편·법인 이전으로 CIK가 바뀐 회사의 옛 CIK XBRL을 새 CIK 앞 기간에 이어 붙인다(2026-10-01, BLK).

BlackRock은 2024-10 GIP 인수 때 새 지주회사(CIK 0002012383)를 세워 옛 BlackRock, Inc.(CIK 0001364742, 지금 이름
BlackRock Finance, Inc.)를 자회사로 두었다. companyfacts는 CIK별이라 새 CIK에는 2024-09 이후 8분기 EPS뿐이고
5년 자기 이력·성장률이 비었다(안건 D4 — XOM·MRVL과 같은 모양).

태그마다 **재편 직전 분기말(cutoff) 이전** 옛 CIK 행을 `.sec_cache/overlay/{새 CIK}.json`에 더한다. 새 CIK가 같은 기간을 비교 수치로 1년 늦게
다시 실어도 옛 행(제때 공시일)이 함께 있어 시점 규칙이 원래 공시일을 쓴다(fetch_eps_history는 predecessor 행을 같은 기간 SEC 행보다 앞세운다).
옛 회사의 재편 뒤 공시는 자회사 기준이라 cutoff로 버린다.
taxonomy는 us-gaap와 dei. 행에 `src: predecessor:{옛 CIK}`를 적는다.

    python3 v2/adapters/predecessor_facts.py 0002012383 0001364742 2024-09-30
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
CACHE = os.path.join(V2, ".sec_cache")
UA = "Su-san Kim gptjhss@gmail.com"


def facts(cik):
    p = os.path.join(CACHE, f"{cik}_facts.json")
    if not os.path.exists(p):
        raw = subprocess.run(["curl", "-s", "-A", UA, f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"],
                             capture_output=True, text=True).stdout
        time.sleep(0.2)
        open(p, "w").write(raw)
    return json.load(open(p))


def main(new_cik, old_cik, cutoff):
    """cutoff: 옛 CIK에서 받을 마지막 결산일(재편 직전 분기말, BLK 2024-09-30). 그 뒤 옛 회사 공시는 자회사 기준이라 버린다."""
    new_cik, old_cik = new_cik.zfill(10), old_cik.zfill(10)
    new, old = facts(new_cik)["facts"], facts(old_cik)["facts"]
    op = os.path.join(CACHE, "overlay", f"{new_cik}.json")
    data = json.load(open(op)) if os.path.exists(op) else {}
    added = 0
    for tax in ("us-gaap", "dei"):
        for tag, body in old.get(tax, {}).items():
            out = [r for r in data.get(tax, {}).get(tag, []) if not str(r.get("src", "")).startswith("predecessor:")]
            for unit, rows in body.get("units", {}).items():
                for r in rows:
                    if r["end"] > cutoff:
                        continue
                    row = {k: r[k] for k in ("start", "end", "val", "accn", "fy", "fp", "form", "filed", "frame") if k in r}
                    row.update(unit=unit, src=f"predecessor:{old_cik}")
                    out.append(row)
                    added += 1
            if out:
                data.setdefault(tax, {})[tag] = out
    os.makedirs(os.path.dirname(op), exist_ok=True)
    json.dump(data, open(op, "w"))
    print(f"저장: {op} (옛 CIK 행 {added}개)")


if __name__ == "__main__":
    main(*sys.argv[1:4])
