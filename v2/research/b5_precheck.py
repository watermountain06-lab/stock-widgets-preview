#!/usr/bin/env python3
"""B5 사전 점검 — research/b5_prereg.md를 그대로 구현한다(엔진 파일은 고치지 않고 메모리에서 W1 계산).

현재 엔진(B17 반영, 커밋 6cada37) 기준. W0 = build_dcf.marginal_s2c, W1 = 감가상각에서 같은 분기 무형자산 상각 TTM을 뺀 base로 같은 함수.

    python3 v2/research/b5_precheck.py universe   # → b5_precheck_universe.json, b5_precheck_result.json
    python3 v2/research/b5_precheck.py cards      # → b5_precheck_cards.json(영향 보고용)
"""
import contextlib
import functools
import io
import json
import math
import os
import subprocess
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


def amort_ttm(t, cik, asof):
    """매출 TTM과 같은 분기에 끝나는 무형자산 상각 TTM(그날까지 공시분). 없으면 None."""
    _, rrows = bmh.pick_tag(cik, bmh.FLOW_TAGS["revenue"])
    rev = [e for e in (bmh.ttm_series(bmh.quarterly_flow(rrows, t)) if rrows else []) if e["available"] <= asof]
    if not rev:
        return None
    end_now = rev[-1]["end"]
    _, arows = bmh.pick_tag(cik, ["AmortizationOfIntangibleAssets"])
    if not arows:
        return None
    am = [e for e in bmh.ttm_series(bmh.quarterly_flow(arows, t)) if e["available"] <= asof and e["end"] == end_now]
    return am[-1]["val"] if am else None


def marginals(t, cik, base):
    asof = base["asof"]
    with contextlib.redirect_stdout(io.StringIO()):
        avg = d.run_dcf(base, [0.0] * 5, 0.10, 0.025, 0.0)["s2c_path"][0]
        b0 = dict(base); b0.pop("_s2c_marginal", None)
        w0 = d.marginal_s2c(b0)
        am = amort_ttm(t, cik, asof)
        dda = base.get("dda")
        adj = am if (am and dda and 0 < am < dda) else 0.0
        b1 = dict(base); b1.pop("_s2c_marginal", None)
        if adj:
            b1["dda"] = dda - adj
        w1 = d.marginal_s2c(b1)
    return {"avg": avg, "W0": w0, "W1": w1, "amort": am, "adj": adj, "dda": dda}


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
            ends[b_["date"][:7]] = b_["date"]
        for mth in MONTHS:
            if mth not in ends:
                continue
            day = ends[mth]
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    base = d.base_inputs(t, day)
                    hist = d.history(t, day)
                if not (hist and base.get("revenue") and base.get("shares") and base.get("opinc") is not None):
                    continue
                rows.append({"t": t, "m": mth, **marginals(t, cik, base)})
            except Exception as e:
                rows.append({"t": t, "m": mth, "err": str(e)[:80]})
        if k % 25 == 0:
            print(k, t, len(rows), flush=True)
    json.dump(rows, open(os.path.join(HERE, "b5_precheck_universe.json"), "w"))
    summarize(rows)


def summarize(rows):
    ok = [r for r in rows if "err" not in r]
    res = {"n_obs": len(ok), "n_tickers": len({r["t"] for r in ok}),
           "adjusted_obs": sum(1 for r in ok if r["adj"]), "amort_missing_obs": sum(1 for r in ok if not r["amort"])}
    by = {}
    for r in ok:
        by.setdefault(r["t"], {})[r["m"]] = r
    for x in ("W0", "W1"):
        none = sum(1 for r in ok if r[x] is None) / len(ok)
        cap = sum(1 for r in ok if r[x] is not None and r[x] >= d.S2C_MAX - 1e-9) / len(ok)
        e_var, e_avg = [], []
        for t, ms in by.items():
            for m_a, m_b in zip(MONTHS, MONTHS[4:]):
                a, real, av = (ms.get(m_a) or {}).get(x), (ms.get(m_b) or {}).get(x), (ms.get(m_a) or {}).get("avg")
                if a and real and av:                      # 같은 쌍에서 둘 다 비교
                    e_var.append(abs(math.log(a / real)))
                    e_avg.append(abs(math.log(av / real)))
        res[x] = {"none_rate": none, "cap_rate": cap, "pred_pairs": len(e_var),
                  "err_variant": float(np.median(e_var)) if e_var else None,
                  "err_avg": float(np.median(e_avg)) if e_avg else None,
                  "skill": (float(np.median(e_avg)) - float(np.median(e_var))) if e_var else None}
    w0, w1 = res["W0"], res["W1"]
    cond = {"1_none_drop_10pp": w1["none_rate"] <= w0["none_rate"] - 0.10,
            "3_skill_not_worse": (w1["skill"] is not None and w0["skill"] is not None and w1["skill"] >= w0["skill"] - 0.02),
            "2_cap_within_2pp": w1["cap_rate"] <= w0["cap_rate"] + 0.02}
    res["rule"] = cond
    res["pick"] = "W1" if all(cond.values()) else "W0"
    json.dump(res, open(os.path.join(HERE, "b5_precheck_result.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


def cards():
    import build_dcf_block as blk  # noqa: F401
    import verdict_replay as vr
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
            mm = marginals(T, d.feh.CIKS[T], base)
            sc = {}
            for x in ("W0", "W1"):
                b = dict(base); b["_s2c_marginal"] = mm[x]
                with contextlib.redirect_stdout(io.StringIO()):
                    s = d.scenarios(b, hist, 0.10, 0.025)
                sc[x] = [z["per_share"] / r if z["per_share"] is not None else None for z in s]
            j = c["judges"]
            lv = [vr.ratio_level(px, sc[x][1]) for x in ("W0", "W1")]
            g = [vr.verdict([(j[0][1], 1), (j[1][1], 1), (vr.SCORE_V0[l], 2)])[0] or "판정 보류" for l in lv]
            out[T] = {"price": px, "card_base": c["base"], "W0": mm["W0"], "W1": mm["W1"], "avg": mm["avg"], "adj": mm["adj"],
                      "scen": sc, "level": lv, "verdict": g}
            print(T, round(sc["W0"][1], 2), "→", round(sc["W1"][1], 2), g, flush=True)
        except Exception as e:
            out[T] = {"err": str(e)[:100]}
    json.dump(out, open(os.path.join(HERE, "b5_precheck_cards.json"), "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    {"universe": universe, "cards": cards,
     "summary": lambda: summarize(json.load(open(os.path.join(HERE, "b5_precheck_universe.json"))))}[sys.argv[1]]()
