#!/usr/bin/env python3
"""seg_map_propose의 2판 — 손 표 한 줄이 여러 공시 멤버의 합인 경우(부분합)까지 찾는다(2026-10-11).

후보 묶음(개념·축·함께 붙은 차원)마다 그 분기 값(10-K면 연간 − 3분기 누계)을 만들고,
① 손 표 값과 하나가 맞는 멤버 ② 남은 멤버 2~4개의 합이 맞는 조합을 찾는다. 손 표 전부를 덮는 묶음을 낸다.
분기 변수·보고서는 quarter_auto.resolve(지금 기준표 날짜)로 정한다(cfg의 TENQ가 비거나 보도자료인 카드).

    python3 v2/newcards/seg_map_propose2.py AMD GOOGL ...
"""
import collections
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quarter_auto as qa  # noqa: E402
import seg_xbrl as sx  # noqa: E402

REV_HINT = ("Revenue", "Sales")


def groups(T):
    C = qa.cfg(T)
    r = qa.resolve(T)
    cur, url, is_k = r["CUR"], r["TENQ"], r["TENQ_NAME"].endswith("10-K")
    fs = sx.facts(url)
    q3 = qa.filing(C.CIK, r["QO"], None)[1] if is_k else None
    keys = set()
    for name, s, e, dims, v in fs:
        if e != cur or not s or not dims or not any(h in name for h in REV_HINT):
            continue
        n = sx._days(s, e)
        if not (70 <= n <= 125 or (is_k and 350 <= n <= 380)):
            continue
        for ax, mem in dims:
            keys.add((name, ax, tuple(sorted((d_, m) for d_, m in dims if d_ != ax))))
    out = []
    for concept, ax, extra in keys:
        M = {"concepts": [concept], "axis": ax, "extra": dict(extra), "members": {}}
        try:
            vals = sx.quarter_values(M, "10-K" if is_k else "10-Q", url, cur, q3_url=q3, q3_end=r["QO"])
        except Exception:
            continue
        if vals:
            out.append((concept, ax, extra, {m: v / 1e6 for m, v in vals.items()}))
    return C, r, out


def match(want, vals):
    mapping, used = {}, set()
    for nm, v in sorted(want.items(), key=lambda x: -x[1]):
        hit = [m for m, x in vals.items() if abs(x - v) <= 1.0 and m not in used]
        if len(hit) == 1:
            mapping[nm] = [hit[0]]; used.add(hit[0])
    for nm, v in want.items():
        if nm in mapping:
            continue
        rest = [m for m in vals if m not in used and vals[m] > 0]
        found = None
        for k in (2, 3, 4):
            for combo in itertools.combinations(rest, k):
                if abs(sum(vals[m] for m in combo) - v) <= 1.5:
                    found = combo; break
            if found:
                break
        if found:
            mapping[nm] = list(found); used |= set(found)
    return mapping, used


def propose(T):
    C, r, gs = groups(T)
    want = {n: v for n, v, _ in C.SEG}
    colors = {n: c for n, _, c in C.SEG}
    best = None
    for concept, ax, extra, vals in gs:
        mp, used = match(want, vals)
        if not best or len(mp) > len(best[0]):
            best = (mp, concept, ax, extra, vals, used)
    if not best or not best[0]:
        return None, "맞는 값 없음"
    mp, concept, ax, extra, vals, used = best
    M = {"concepts": [concept], "axis": ax, "extra": dict(extra),
         "members": {m: (n, colors[n]) for n, ms in mp.items() for m in ms},
         "ignore": [m for m in vals if m not in used]}
    return M, ("전부 맞음" if len(mp) == len(want) else f"{len(mp)}/{len(want)} — 수동") + f" ({r['QLABEL']})"


if __name__ == "__main__":
    out = {}
    for T in [a.upper() for a in sys.argv[1:]]:
        try:
            M, note = propose(T)
        except Exception as e:
            M, note = None, f"오류 {type(e).__name__}: {str(e)[:80]}"
        print(f"{T}: {note}" + (f" — {M['axis']} · 멤버 {len(M['members'])} · 무시 {len(M['ignore'])}" if M else ""))
        if M:
            out[T] = M
    p = os.path.join(HERE, "seg_map_proposals2.json")
    old = json.load(open(p)) if os.path.exists(p) else {}
    old.update(out)
    json.dump(old, open(p, "w"), ensure_ascii=False, indent=1)
