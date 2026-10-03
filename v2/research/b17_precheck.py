#!/usr/bin/env python3
"""B17 사전 점검 — research/b17_prereg.md를 그대로 구현한다(엔진 파일은 고치지 않고 메모리에서 변형 계산).

주의(2026-10-03): **B17 이전 엔진(커밋 79e85e3)에서만 유효하다.** V1이 엔진(build_dcf.current_debt)에 들어간 뒤에는
base["nwc"]가 이미 고쳐져 있어 nwc_v1이 운전자본을 두 번 고치고, V0도 새 엔진을 부른다(Codex). 다시 돌리려면 그 커밋을 체크아웃한다.

    python3 v2/research/b17_precheck.py universe   # S&P500 비금융, 분기 말 6개 평가일 → b17_precheck_universe.json
    python3 v2/research/b17_precheck.py cards       # 현금흐름 카드(영향 보고용)        → b17_precheck_cards.json
"""
import contextlib
import functools
import io
import json
import math
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, V2)
import numpy as np  # noqa: E402
import valuation_judges_test as v  # noqa: E402
import build_multiple_history as bmh  # noqa: E402
import splits as _splits  # noqa: E402

d = v.d
FACTS = os.path.join(HERE, ".facts_20261002")
PRICES = os.path.join(HERE, ".prices10y")
MONTHS = ["2025-06", "2025-09", "2025-12", "2026-03", "2026-06", "2026-09"]
VARIANTS = ["V0", "V1", "V2", "V3", "V4"]


FRESH_DAYS = 200


def at_end(cik, tag, asof, end):
    """그 결산일(end)의 값, 없으면 결산일 이전 200일 안의 마지막 값 — asof까지 공시된 것만(2026-10-03 구현 수정).

    처음 구현은 결산일 값만 써서 분기 보고서에 단기 차입 태그가 없는 회사(MCD — 연말에만 공시)는 새 단기 차입이 0이 되고,
    엔진의 옛 값(latest)과 기준이 달라 운전자본이 거꾸로 움직였다(Fable). 엔진의 신선도 기준(200일)과 맞춘다.
    """
    rows = [e for e in bmh.component_sum(cik, [tag]) if e.get("available", e["end"]) <= asof and e["end"] <= end
            and (date.fromisoformat(end) - date.fromisoformat(e["end"])).days <= FRESH_DAYS]
    if not rows:
        return None
    same = [e for e in rows if e["end"] == end]
    return (same or sorted(rows, key=lambda e: (e["end"], e.get("available", "")))) [-1]["val"]


def bs_end(cik, asof):
    rows = [e for e in bmh.component_sum(cik, ["AssetsCurrent"]) if e.get("available", e["end"]) <= asof]
    return rows[-1]["end"] if rows else None


def nwc_v1(base, cik, asof):
    """V1 운전자본 = 지금 운전자본 + (새 단기 차입 − 옛 단기 차입). 옛 단기 차입은 엔진과 같이 latest(LongTermDebtCurrent)."""
    if base.get("nwc") is None:
        return None
    end = bs_end(cik, asof)
    if not end:
        return None
    st_old = d.latest(bmh.component_sum(cik, ["LongTermDebtCurrent"]), asof) or 0
    a = at_end(cik, "DebtCurrent", asof, end) or 0
    comb = at_end(cik, "LongTermDebtAndCapitalLeaseObligationsCurrent", asof, end)
    ltc = comb if comb is not None else (at_end(cik, "LongTermDebtCurrent", asof, end) or 0)
    stb = at_end(cik, "ShortTermBorrowings", asof, end)
    if stb is None:
        stb = at_end(cik, "CommercialPaper", asof, end) or 0
    comp = ltc + stb
    st_new = max(a, comp)
    # DebtCurrent는 유동 금융리스를 이미 담는다(TSLA "current portion of debt and finance leases", Fable) — 구성요소 합을 쓸 때만 더한다
    if comb is None and comp >= a:
        st_new += at_end(cik, "FinanceLeaseLiabilityCurrent", asof, end) or 0
    return base["nwc"] + (st_new - st_old)


def lagged(t, cik, base, asof, k):
    """k년 전 같은 분기가 공시된 날의 base(없으면 None)."""
    _, rrows = bmh.pick_tag(cik, bmh.FLOW_TAGS["revenue"])
    rev = bmh.ttm_series(bmh.quarterly_flow(rrows, t)) if rrows else []
    seen = [e for e in rev if e["available"] <= asof]
    if not seen:
        return None
    end_now = date.fromisoformat(seen[-1]["end"])
    prior = [e for e in rev if abs((end_now - date.fromisoformat(e["end"])).days - 365 * k) <= 10 + 5 * (k - 1)
             and e["available"] <= asof]
    if not prior:
        return None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return d.base_inputs(t, prior[-1]["available"])
    except Exception:
        return None


def marginals(t, cik, base, asof):
    """변형별 한계 매출/자본과 평균 비율."""
    with contextlib.redirect_stdout(io.StringIO()):
        avg = d.run_dcf(base, [0.0] * 5, 0.10, 0.025, 0.0)["s2c_path"][0]
        m0 = d.marginal_s2c(base)
    bs = [base] + [lagged(t, cik, base, asof, k) for k in (1, 2, 3)]
    nw = [nwc_v1(b, cik, b["asof"]) if b else None for b in bs]

    def cum(k):
        if any(b is None for b in bs[:k + 1]):
            return None
        if any(b.get("capex") is None or b.get("dda") is None for b in bs[:k]) or not bs[k].get("revenue"):
            return None
        d_rev = base["revenue"] - bs[k]["revenue"]
        dnwc = (nw[0] - nw[k]) if (nw[0] is not None and nw[k] is not None) else 0.0   # 한쪽이 없으면 변화 0
        inv = sum(b["capex"] - b["dda"] + (b.get("acquisitions") or 0) for b in bs[:k]) + dnwc
        if d_rev <= 0 or inv <= 0:
            return None
        return min(d_rev / inv, d.S2C_MAX)

    m1 = cum(1)
    out = {"avg": avg, "V0": m0, "V1": m1, "V2": cum(2), "V3": cum(3),
           "V4": (min(max(m1, 0.5 * avg), 2 * avg) if m1 is not None else None)}
    out["cap"] = {k: (out[k] is not None and (out[k] >= d.S2C_MAX - 1e-9 or (k == "V4" and m1 is not None and m1 >= 2 * avg)))
                  for k in VARIANTS}
    return out


def scen_with(base, hist, m):
    """한계 비율을 m으로 바꿔 세 시나리오 주당 가치."""
    b = dict(base)
    b["_s2c_marginal"] = m
    with contextlib.redirect_stdout(io.StringIO()):
        s = d.scenarios(b, hist, 0.10, 0.025)
    return [x["per_share"] for x in s]


def universe():
    uni = [r for r in json.load(open(v.SP500)) if r.get("sector") != "Financials"]
    rows = []
    for k, r in enumerate(uni):
        t, cik = r["ticker"], r["cik"].zfill(10)
        if t in v.EXCLUDE or not os.path.exists(os.path.join(v.EPS_DIR, t.replace(".", "-") + ".json")):
            continue
        pf5 = v.price_file(t)
        fp, pf = os.path.join(FACTS, f"{cik}_facts.json"), os.path.join(PRICES, f"{t}.json")
        if not pf5 or not os.path.exists(fp) or not os.path.exists(pf) or len(json.load(open(pf5))["daily"]) < 700:
            continue
        data = json.load(open(fp))
        pj = json.load(open(pf))
        _splits.OVERRIDE[t] = [(s["date"], s["ratio"]) for s in (pj.get("splits") or [])]
        d.feh.CIKS[t] = cik
        bmh._facts = functools.lru_cache(maxsize=2)(lambda c, _data=data: _data if c == cik else {})
        if hasattr(bmh.concept, "cache_clear"):
            bmh.concept.cache_clear()
        ends = {}
        for b_ in pj["daily"]:
            ends[b_["date"][:7]] = (b_["date"], b_["c"])
        for mth in MONTHS:
            if mth not in ends:
                continue
            day, px = ends[mth]
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    base = d.base_inputs(t, day)
                    hist = d.history(t, day)
                if not (hist and base.get("revenue") and base.get("shares") and base.get("opinc") is not None):
                    continue
                mm = marginals(t, cik, base, day)
                row = {"t": t, "m": mth, **{x: mm[x] for x in ["avg"] + VARIANTS}, "cap": mm["cap"]}
                if mth == MONTHS[-1]:
                    row["scen"] = {x: (scen_with(base, hist, mm[x]) if x != "V0" else scen_with(base, hist, mm["V0"]))
                                   for x in VARIANTS}
                rows.append(row)
            except Exception as e:
                rows.append({"t": t, "m": mth, "err": str(e)[:80]})
        if k % 25 == 0:
            print(k, t, len(rows), flush=True)
    json.dump(rows, open(os.path.join(HERE, "b17_precheck_universe.json"), "w"))
    summarize(rows)


def summarize(rows):
    ok = [r for r in rows if "err" not in r]
    res = {"n_obs": len(ok), "n_tickers": len({r["t"] for r in ok})}
    by = {}
    for r in ok:
        by.setdefault(r["t"], {})[r["m"]] = r
    for x in VARIANTS:
        jumps, jumps4, err = [], [], []
        for t, ms in by.items():
            for m_a, m_b in zip(MONTHS, MONTHS[1:]):          # 연속 분기끼리만(Codex)
                a, b = (ms.get(m_a) or {}).get(x), (ms.get(m_b) or {}).get(x)
                if a and b:
                    jumps.append(abs(math.log(b / a)))
            for m_a, m_b in zip(MONTHS, MONTHS[4:]):          # 보조: 4분기 간격(겹침 적음)
                a, b = (ms.get(m_a) or {}).get(x), (ms.get(m_b) or {}).get(x)
                if a and b:
                    jumps4.append(abs(math.log(b / a)))
                real = (ms.get(m_b) or {}).get("V1")           # 보조: 다음 해 실제 1년 한계(V1)를 맞히는가
                if a and real:
                    err.append(abs(math.log(a / real)))
        none = sum(1 for r in ok if r[x] is None) / len(ok)
        cap = sum(1 for r in ok if r["cap"][x]) / len(ok)
        last = [r for r in ok if r["m"] == MONTHS[-1] and r.get("scen")]
        inv = [r for r in last if all(v_ is not None for v_ in r["scen"][x]) and r["scen"][x][1] > r["scen"][x][2]]
        res[x] = {"instability_median": float(np.median(jumps)) if jumps else None, "pairs": len(jumps),
                  "none_rate": none, "cap_rate": cap,
                  "supp_instability_4q": float(np.median(jumps4)) if jumps4 else None, "supp_pairs_4q": len(jumps4),
                  "supp_pred_err_next_year": float(np.median(err)) if err else None, "supp_pred_n": len(err),
                  "base_gt_high_rate": round(len(inv) / len(last), 4) if last else None}
    # 보조: 평균 비율로 다음 해 실제 1년 한계를 맞힐 때
    err = []
    for t, ms in by.items():
        for m_a, m_b in zip(MONTHS, MONTHS[4:]):
            a, real = (ms.get(m_a) or {}).get("avg"), (ms.get(m_b) or {}).get("V1")
            if a and real:
                err.append(abs(math.log(a / real)))
    res["supp_pred_err_avg"] = float(np.median(err)) if err else None
    # 판정 규칙(사전 등록 2·3)
    v1 = res["V1"]
    cands = [x for x in ("V2", "V3", "V4")
             if res[x]["instability_median"] is not None and v1["instability_median"]
             and res[x]["instability_median"] <= 0.9 * v1["instability_median"]
             and res[x]["none_rate"] <= v1["none_rate"] + 0.05 and res[x]["cap_rate"] <= v1["cap_rate"]]
    if cands:
        best = min(cands, key=lambda x: res[x]["instability_median"])
        simple = [x for x in ("V4", "V2", "V3") if x in cands and res[x]["instability_median"] <= res[best]["instability_median"] * 1.1]
        pick = simple[0] if simple else best
    else:
        pick = "V1"
    res["candidates"], res["pick"] = cands, pick
    json.dump(res, open(os.path.join(HERE, "b17_precheck_result.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


def cards():
    import build_dcf_block as blk
    import subprocess
    cj = json.loads(subprocess.run(["node", os.path.join(HERE, "extract_card_verdicts.js")], capture_output=True, text=True).stdout)
    out = {}
    for T, c in sorted(cj.items()):
        if c["judges"][2][0] != "현금흐름" or c.get("base") is None:
            continue
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                daily = bmh.load_daily(T)
                asof, px = daily[-1][0], daily[-1][4]
                r = bmh.fx.rate(T, asof)
                base = d.base_inputs(T, asof)
                hist = d.history(T, asof)
            mm = marginals(T, d.feh.CIKS[T], base, asof)
            out[T] = {"price": px, "card_base": c["base"], "verdict": c["verdict"], "judges": c["judges"],
                      **{x: mm[x] for x in ["avg"] + VARIANTS},
                      "scen": {x: [s_ / r if s_ is not None else None for s_ in scen_with(base, hist, mm[x])] for x in VARIANTS}}
            print(T, {x: round(out[T]["scen"][x][1], 2) for x in VARIANTS}, flush=True)
        except Exception as e:
            out[T] = {"err": str(e)[:100]}
            print("ERR", T, e, flush=True)
    json.dump(out, open(os.path.join(HERE, "b17_precheck_cards.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    {"universe": universe, "cards": cards, "summary": lambda: summarize(json.load(open(os.path.join(HERE, "b17_precheck_universe.json"))))}[sys.argv[1]]()
