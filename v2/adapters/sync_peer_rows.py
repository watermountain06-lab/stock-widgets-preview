#!/usr/bin/env python3
"""S&P500 비교군 파일에서 v2 카드가 있는 종목의 행을 그 카드의 엔진 값으로 바꾼다(2026-10-06).

그동안 손으로 하던 일(T·NEE·TMUS·DIS·NFLX·GE·LIN·COST·XOM·CVX·MRK·V 행을 "카드 엔진 값으로 바꿨다")을 규칙으로:
카드 자기 이력 창의 끝 날짜가 파일 기준일과 같을 때만, 카드 `{T}_VALUATION.self.metrics`의 현재값으로 행을 덮는다.
본업 기준 PER(perBasis 'core')인 카드는 공시 EPS 기준인 다른 행과 잣대가 달라 PER은 그대로 둔다. 카드에 없는 배수(적자·결측)는 파일 값을 둔다.
은행·보험·BRKB처럼 동종업을 따로 내는 카드는 대상이 아니다(이 파일들에 행이 없거나 다른 엔진).

    python3 v2/adapters/sync_peer_rows.py            # 전 파일 — 바뀐 행을 찍는다
    python3 v2/adapters/sync_peer_rows.py --dry
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
SKIP = {"banks.json"}
KEY = {"per": "per", "pbr": "pbr", "psr": "psr", "pcr": "pcr", "evebitda": "evebitda"}


def card_self(T):
    p = os.path.join(V2, f"{T}_full_widget.html")
    if not os.path.exists(p):
        return None
    h = open(p, encoding="utf-8").read()
    k = f"const {T}_VALUATION = "
    if k not in h:
        return None
    return json.JSONDecoder().raw_decode(h, h.index(k) + len(k))[0]["self"]


def main():
    dry = "--dry" in sys.argv
    for p in sorted(glob.glob(os.path.join(V2, "peer_universe", "*.json"))):
        if os.path.basename(p) in SKIP:
            continue
        d = json.load(open(p))
        asof, changed = d.get("asOf"), []
        for T, row in d["tickers"].items():
            s = card_self(T)
            if not s or not s.get("window") or s["window"][1] != asof:
                continue
            new = dict(row)
            for m in s.get("metrics", []):
                k = KEY.get(m["metric"])
                if not k or m.get("current") is None:
                    continue
                if k == "per" and s.get("perBasis") == "core":
                    continue
                if f"{T}:{k}" in d.get("skipped", {}):   # 이상값·수동 제외한 배수는 되살리지 않는다(Codex 2026-10-06)
                    continue
                new[k] = round(m["current"], 2)
            if new != row:
                changed.append((T, {k: (row.get(k), new.get(k)) for k in set(row) | set(new) if row.get(k) != new.get(k)}))
                d["tickers"][T] = new
                d.setdefault("cardRows", {})[T] = f"카드 엔진 값으로 바꿨다(같은 기준일 {asof}, sync_peer_rows.py)"
        for T, ch in changed:
            print(f"{os.path.basename(p)} {T}: {ch}")
        if changed and not dry:
            json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
