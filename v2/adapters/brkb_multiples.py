#!/usr/bin/env python3
"""BRKB 금융 카드 배수 — research/brkb_two_pillar_prereg.md §2(금융 카드 배수 규칙) 구현.

    python3 v2/adapters/brkb_multiples.py --json v2/BRKB_multiples.json

배수 두 개만 만든다(PSR·PCR·EV/EBITDA는 보험지주에 뜻이 없다).
- PBR = 종가 × B주 환산 주식 수 ÷ 지배주주 자본
- 정상화 PER = 종가 × B주 환산 주식 수 ÷ 최근 4분기 정상화 영업이익(brkb_pillars.pillars()["op_norm"])
분모는 공시일마다 바뀌는 계단이다(그날까지 공시된 10-Q/10-K만). 핵심 항목을 못 찾은 공시 구간은
배수를 비워 둔다(0으로 채우지 않는다 — 2025-11-03 10-Q는 B주 환산 주식 수 태그가 없다).
출력 형식은 build_multiple_history.py --json과 같다(multiples·fairBand). 밴드는 정상화 PER 기준.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, V2)
import brkb_pillars as B  # noqa: E402
from build_multiple_history import load_daily, percentile_rank  # noqa: E402


def steps():
    """공시일 → (정상화 영업이익, 지배주주 자본, B주 환산 주식 수, 기준 분기). 기권이면 None 값."""
    out = []
    for d in sorted({f["filed"] for f in B.FACTS}):
        s = B.pillars(d)
        sh = s.get("sharesA") * 1500 if s.get("sharesA") else None
        out.append({"filed": d, "L": s.get("L"), "op": s.get("op_norm"), "eq": s.get("equity"), "sh": sh,
                    "abstain": s.get("abstain")})
    return out


def as_of(st, day):
    cur = None
    for s in st:
        if s["filed"] <= day:
            cur = s
    return cur


def main():
    daily = load_daily("BRKB")
    st = steps()
    start = daily[0][0]
    defs = {"PER": lambda s: s["op"], "PBR": lambda s: s["eq"]}
    out = {"ticker": "BRKB", "window": [start, daily[-1][0]], "perBasis": "normalized_operating",
           "rule": "financial", "multiples": {}, "steps": [
               {k: s[k] for k in ("filed", "L", "op", "eq", "sh", "abstain")} for s in st if s["filed"] >= "2020-01-01"]}
    for label, den in defs.items():
        pts = []
        for b in daily:
            s = as_of(st, b[0])
            if not s or not s["sh"] or not den(s) or den(s) <= 0:
                continue
            pts.append((b[0], b[4] * s["sh"] / den(s)))
        vals = [v for _, v in pts]
        srt = sorted(vals)

        def q(p, a=srt):
            i = (len(a) - 1) * p
            lo = int(i)
            hi = min(lo + 1, len(a) - 1)
            return a[lo] + (a[hi] - a[lo]) * (i - lo)

        today = pts and pts[-1][0] == daily[-1][0]
        cur = pts[-1][1] if today else None
        pr = percentile_rank(vals, cur) if today else None
        out["multiples"][label] = {
            "days": len(pts), "current": round(cur, 2) if cur else None,
            "min": round(srt[0], 2), "p10": round(q(.10), 2), "median": round(q(.50), 2),
            "p90": round(q(.90), 2), "max": round(srt[-1], 2), "mean": round(sum(vals) / len(vals), 2),
            "percentile": round(pr, 1) if pr is not None else None,
            "score": round(100 - pr, 1) if pr is not None else None,
            # 창 안에서 핵심 항목 기권으로 빈 거래일 수(카드가 "최근 N년 이력" 대신 빈 구간을 적는다)
            "gapDays": sum(1 for d in daily if as_of(st, d[0]) and not (as_of(st, d[0])["sh"] and den(as_of(st, d[0])) and den(as_of(st, d[0])) > 0))}
        if not today:
            out["multiples"][label]["currentNote"] = "missing"
        if label == "PER" and today:
            start_day = daily[-252][0]
            yr = sorted(v for dd, v in pts if dd >= start_day)
            px = daily[-1][4]
            lo_px, hi_px = px * q(.25, yr) / cur, px * q(.75, yr) / cur
            out["fairBand"] = {"per_p25": round(q(.25, yr), 2), "per_p75": round(q(.75, yr), 2),
                               # 바깥쪽으로 $10 맞춤 — 1년 PER 사분위 폭이 좁아(0.65배) 반올림하면 현재 PER이 p25와
                               # 같은데도 하한이 현재가 위로 올라갔다(Fable, 2026-09-26). 다른 카드는 반올림.
                               "low": int(math.floor(lo_px / 10) * 10), "high": int(math.ceil(hi_px / 10) * 10),
                               "asOf": daily[-1][0], "basis": out["perBasis"], "days": len(yr)}
        m = out["multiples"][label]
        print(f"  {label}: 현재 {m['current']} (최저 {m['min']} · 중앙 {m['median']} · 최고 {m['max']}) "
              f"하위 {m['percentile']}% → 점수 {m['score']} [{m['days']}일]")
    if "fairBand" in out:
        fb = out["fairBand"]
        print(f"  적정주가 밴드: 정상화 PER {fb['per_p25']}~{fb['per_p75']}x → ${fb['low']}~${fb['high']} ({fb['days']}일)")
    gaps = [s for s in out["steps"] if not s["sh"] or not s["op"] or not s["eq"]]
    for g in gaps:
        print(f"  ⚠ 공시 {g['filed']}(분기 {g['L']}) 구간 배수 없음: {g['abstain']}")
    if "--json" in sys.argv:
        p = sys.argv[sys.argv.index("--json") + 1]
        json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
        print("저장:", p)


if __name__ == "__main__":
    main()
