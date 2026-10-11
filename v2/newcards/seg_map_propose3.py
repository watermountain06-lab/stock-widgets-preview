#!/usr/bin/env python3
"""seg_map_propose 3판 — 여러 축을 섞은 손 표(parts)와 "기타 = 매출 − 나머지" 줄(remainder)까지(2026-10-11).

손 표 한 줄마다: ① 어느 묶음(개념·축·차원)이든 값이 하나 맞는 멤버 ② 같은 묶음 안 2~4개 멤버의 합.
남은 줄이 하나면 나머지 줄로(그 분기 매출 − 다른 줄 합과 맞을 때만). 묶음별로 parts를 만든다.
    python3 v2/newcards/seg_map_propose3.py AMD GOOGL ...
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import seg_map_propose2 as p2  # noqa: E402
import build_multiple_history as bmh  # noqa: E402


def propose(T):
    C, r, gs = p2.groups(T)
    want = {n: v for n, v, _ in C.SEG}
    colors = {n: c for n, _, c in C.SEG}
    used = {}   # group index -> set(members)
    mapping = {}   # name -> (group index, [members])
    for nm, v in sorted(want.items(), key=lambda x: -x[1]):
        for gi, (_, _, _, vals) in enumerate(gs):
            tol = max(1.0, 0.006 * v)   # 손 표가 1억 달러 단위로 반올림된 카드(MSFT·AMZN·WMT)
            hit = [m for m, x in vals.items() if abs(x - v) <= tol and m not in used.get(gi, set())]
            if len(hit) == 1:
                mapping[nm] = (gi, hit); used.setdefault(gi, set()).add(hit[0]); break
    for nm, v in want.items():
        if nm in mapping:
            continue
        for gi, (_, _, _, vals) in enumerate(gs):
            rest = [m for m in vals if m not in used.get(gi, set()) and vals[m] > 0]
            found = next((c for k in (2, 3, 4) for c in itertools.combinations(rest, k) if abs(sum(vals[m] for m in c) - v) <= max(1.5, 0.006 * v)), None)
            if found:
                mapping[nm] = (gi, list(found)); used.setdefault(gi, set()).update(found); break
    left = [n for n in want if n not in mapping]
    # 차원 없는 손익계산서 항목(보험사 순보험료·MCD 가맹 수익 등)에서 찾는다 — 묶음 하나(axis None)로
    if left:
        import seg_xbrl as sx
        fs = sx.facts(r["TENQ"])
        nd = {}
        for name, s_, e_, dims, v_ in fs:
            if e_ == r["CUR"] and s_ and not dims and 70 <= sx._days(s_, e_) <= 125 and any(h in name for h in ("Revenue", "Premium", "Income", "Gain", "Fee", "Sales", "Interest")):
                nd[name] = v_ / 1e6
        for nm in list(left):
            v = want[nm]
            hit = [k for k, x in nd.items() if abs(x - v) <= max(1.0, 0.006 * v)]
            if len(hit) >= 1:
                gi = len(gs)
                gs.append((None, None, (), {hit[0]: nd[hit[0]]}))
                mapping[nm] = (gi, [hit[0]])
                left.remove(nm)
    cik = str(C.CIK).zfill(10)
    _, rows = bmh.pick_tag(cik, bmh.FLOW_TAGS["revenue"])
    rev = {e["end"]: e["val"] / 1e6 for e in bmh.quarterly_flow(rows, T)}.get(C.CUR)
    rem = None
    if len(left) == 1 and rev:
        others = sum(want[n] for n in mapping)
        adj = getattr(C, "SEG_ADJ", 0) or 0
        if abs(rev - others - want[left[0]]) <= max(2.0, abs(adj) + 2):
            rem = [left[0], colors[left[0]], round(want[left[0]] / rev, 4)]
            left = []
    if left:
        return None, f"{len(want) - len(left)}/{len(want)} — 남은 줄 {left}"
    parts = []
    nodim = {}
    for gi in sorted({g for g, _ in mapping.values()}):
        concept, ax, extra, vals = gs[gi]
        mem = {m: (nm, colors[nm]) for nm, (g, ms) in mapping.items() if g == gi for m in ms}
        if ax is None:
            nodim.update(mem)
            continue
        parts.append({"concepts": [concept], "axis": ax, "extra": dict(extra), "members": mem})
    if nodim:
        parts.append({"concepts": [], "axis": None, "extra": {}, "members": nodim})
    M = parts[0] if len(parts) == 1 else {"parts": parts}
    if rem:
        M["remainder"] = rem
    return M, "전부 맞음" + (f" (나머지 줄 {rem[0]})" if rem else "") + (f" (축 {len(parts)}개)" if len(parts) > 1 else "")


if __name__ == "__main__":
    out = {}
    for T in [a.upper() for a in sys.argv[1:]]:
        try:
            M, note = propose(T)
        except Exception as e:
            M, note = None, f"오류 {type(e).__name__}: {str(e)[:80]}"
        print(f"{T}: {note}")
        if M:
            out[T] = M
    p = os.path.join(HERE, "seg_map_proposals3.json")
    old = json.load(open(p)) if os.path.exists(p) else {}
    old.update(out)
    json.dump(old, open(p, "w"), ensure_ascii=False, indent=1)
