#!/usr/bin/env python3
"""fetch_financials가 태그 하나로만 읽는 항목을 여러 태그의 합으로 다시 채운다(2026-09-29, XOM).

redesign의 fetch_financials는 재고를 `InventoryNet` 하나로 읽는다. XOM은 재고를 "원유·제품·상품"
(EnergyRelatedInventory)과 "자재"(InventoryPartsAndComponentsNetOfReserves) 두 줄로만 내고 InventoryNet은
2012년에 멈췄다 — 그래서 당좌비율이 유동비율과 같게(재고 0) 나왔다. 여기서는 캐시+오버레이 companyfacts
(build_multiple_history._facts)에서 같은 결산일·같은 공시의 두 값을 더해 `{T}_financials.json`의 그 항목을
바꾼다(연간 = 10-K 시점값, 최신 분기 = 가장 늦은 결산일). 한 태그라도 빠진 날짜는 싣지 않는다.

    python3 v2/adapters/financials_sum_tags.py XOM
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, V2)
import build_multiple_history as bmh  # noqa: E402

SUMS = {"XOM": {"cik": "0000034088",
                "inventory": ["EnergyRelatedInventory", "InventoryPartsAndComponentsNetOfReserves"]}}


def rows_by_key(g, tag):
    out = {}
    for r in g.get(tag, {}).get("units", {}).get("USD", []):
        if "start" in r:
            continue
        out[(r["end"], r["accn"])] = r
    return out


def main(t):
    spec = SUMS[t]
    g = bmh._facts(spec["cik"])["facts"]["us-gaap"]
    path = os.path.join(V2, "fundamental_data", f"{t}_financials.json")
    fin = json.load(open(path))
    for key, tags in spec.items():
        if key == "cik":
            continue
        maps = [rows_by_key(g, tag) for tag in tags]
        common = set(maps[0]).intersection(*maps[1:])
        rows = [{**maps[0][k], "val": sum(m[k]["val"] for m in maps)} for k in common]
        annual = {}
        for r in sorted(rows, key=lambda r: r["filed"]):          # 같은 결산일은 늦은 공시(정정)가 이긴다
            if r.get("form") == "10-K":
                annual[r["end"]] = r
        latest = max(rows, key=lambda r: (r["end"], r["filed"]))
        fin[key] = {"tag": "+".join(tags), "annual": [annual[e] for e in sorted(annual)], "latestQuarter": latest}
        print(f"{t} {key}: 연간 {len(annual)}개, 최신 {latest['end']} = {latest['val'] / 1e9:.2f}B")
    json.dump(fin, open(path, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1].upper())
