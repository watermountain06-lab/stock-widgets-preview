#!/usr/bin/env python3
"""카드의 부문 표(cfg SEG — 사람이 옮겨 적은 값)와 같은 값을 그 분기 보고서 원문에서 찾아 SEG_MAP을 제안한다(설계 D, 2026-10-10).

자동 카드로 바꿀 때 카드마다 부문 지도를 손으로 만들면 오래 걸린다. 지금 cfg에는 그 분기 부문 숫자가 있으니,
원문 인라인 XBRL에서 그 분기 말에 끝나는 매출 값 가운데 숫자가 정확히(±1백만 달러) 맞는 멤버를 찾는다.
축 하나 + 함께 붙은 차원 조합이 cfg 부문 전부를 덮으면 그 조합을 지도로 낸다. 못 덮으면 "수동"으로 표시한다.

    python3 v2/newcards/seg_map_propose.py PEP COST AAPL
    python3 v2/newcards/seg_map_propose.py --all
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import quarter_auto as qa  # noqa: E402
import seg_xbrl as sx  # noqa: E402

REV_HINT = ("Revenue", "Sales")


def propose(T):
    C = qa.cfg(T)
    if not getattr(C, "SEG", None) or not getattr(C, "TENQ", None) or "sec.gov" not in C.TENQ:
        return None, "SEG 또는 10-Q 링크 없음"
    is_k = C.TENQ_NAME.endswith("10-K") if getattr(C, "TENQ_NAME", "") else False
    fs = sx.facts(C.TENQ)
    if is_k:   # 4분기: 연간 − 3분기 누계로 비교 값 만들기
        form, q3 = qa.filing(C.CIK, C.QO, None)
        q3fs = sx.facts(q3) if q3 else []
    want = {n: v for n, v, _ in C.SEG}
    groups = collections.defaultdict(dict)   # (concept, axis, extra) -> {member: 값(백만)}
    for name, s, e, dims, v in fs:
        if e != C.CUR or not s or not dims or not any(h in name for h in REV_HINT):
            continue
        n = sx._days(s, e)
        if not (70 <= n <= 125 or (is_k and 350 <= n <= 380)):
            continue
        for ax, mem in dims:
            extra = tuple((d_, m) for d_, m in dims if d_ != ax)
            key = (name, ax, extra, "fy" if n > 300 else "q")
            groups[key][mem] = v / 1e6
    best = None
    for (concept, ax, extra, kind), mems in groups.items():
        vals = mems
        if kind == "fy":
            M = {"concepts": [concept], "axis": ax, "extra": dict(extra), "members": {m: (m, "") for m in mems}}
            try:
                vals = {m: v / 1e6 for m, v in sx.quarter_values(M, "10-K", C.TENQ, C.CUR, q3_url=q3, q3_end=C.QO).items()}
            except Exception:
                continue
        match = {}
        for nm, v in want.items():
            hit = [m for m, x in vals.items() if abs(x - v) <= 1.0 and m not in match.values()]
            if len(hit) == 1:
                match[nm] = hit[0]
        score = len(match)
        if score and (not best or score > best[0]):
            best = (score, concept, ax, extra, match, vals)
    if not best:
        return None, "맞는 값 없음"
    score, concept, ax, extra, match, vals = best
    colors = {n: c for n, _, c in C.SEG}
    others = [m for m in vals if m not in match.values()]
    M = {"concepts": [concept], "axis": ax, "extra": dict(extra),
         "members": {m: (n, colors[n]) for n, m in match.items()}}
    note = "전부 맞음" if score == len(want) else f"{score}/{len(want)}만 맞음 — 수동 확인"
    if others:
        M["ignore_candidates"] = others
    return M, note


def main():
    tickers = [a.upper() for a in sys.argv[1:] if not a.startswith("--")]
    if "--all" in sys.argv:
        tickers = sorted(f[4:-3].upper() for f in os.listdir(os.path.join(HERE, "cfg")) if f.startswith("cfg_"))
    out, summary = {}, collections.Counter()
    for T in tickers:
        if T in ("ASML", "TSM", "SKHY", "COF"):
            continue
        try:
            M, note = propose(T)
        except Exception as e:
            M, note = None, f"오류 {type(e).__name__}: {str(e)[:80]}"
        summary["전부 맞음" if note == "전부 맞음" else "수동"] += 1
        print(f"{T}: {note}" + (f" — {M['axis']} {len(M['members'])}개" + (f" · 다른 멤버 {len(M.get('ignore_candidates', []))}" if M.get('ignore_candidates') else "") if M else ""))
        if M:
            out[T] = M
    json.dump(out, open(os.path.join(HERE, "seg_map_proposals.json"), "w"), ensure_ascii=False, indent=1)
    print(dict(summary))


if __name__ == "__main__":
    main()
