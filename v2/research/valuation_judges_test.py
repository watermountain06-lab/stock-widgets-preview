#!/usr/bin/env python3
"""현금흐름 심판 분포 · 역-DCF 투표 · 품질 거부권 검증 — valuation_judges_prereg.md를 그대로 구현한다.

카드와 같은 코드(build_dcf.scenarios · implied_growth, build_fundamental_score.compute)를 쓰고,
입력은 매월 말 기준 **그때까지 공시된 것만**(filed ≤ 평가일) 쓴다. 재무는 fetch_universe_facts.py 캐시.

    python3 v2/research/valuation_judges_test.py            # 패널 계산 + 결과(valuation_judges_result.json)
    python3 v2/research/valuation_judges_test.py --analyze  # 저장된 패널로 분석만
"""
import argparse
import contextlib
import functools
import io
import json
import math
import os
import sys

import numpy as np
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, V2)
sys.path.insert(0, "/Users/watermountain/Workspace/stock-widgets-redesign/scripts")
import build_dcf as d  # noqa: E402
import build_fundamental_score as bfs  # noqa: E402
import fetch_financials as ff  # noqa: E402

DATA = "/Users/watermountain/Workspace/stock-widgets-redesign/data"
PRICE_DIR, EPS_DIR = os.path.join(DATA, "sp500_5y"), os.path.join(DATA, "sp500_eps")
SP500 = "/Users/watermountain/Workspace/stock-widgets-redesign/scripts/sp500.json"
FACTS = os.path.join(HERE, ".facts")
PANEL = os.path.join(HERE, "valuation_judges_panel.json")
EXCLUDE = {"MRNA", "ECHO", "GL", "APP"}
H_MAIN, H_EXPL = 126, 252
START_MONTH = "2024-06"
MIN_MONTH_N = 50


def load_json(cik):
    p = os.path.join(FACTS, f"{cik}_facts.json")
    return json.load(open(p)) if os.path.exists(p) else {}


def price_file(t):
    for name in (t, t.replace(".", "-")):
        p = os.path.join(PRICE_DIR, name + ".json")
        if os.path.exists(p):
            return p
    return None


def filtered_facts(data, day):
    out = {}
    for ns, tags in data.get("facts", {}).items():
        out[ns] = {}
        for tag, v in tags.items():
            units = {u: [r for r in rows if r.get("filed", "9999") <= day] for u, rows in v.get("units", {}).items()}
            units = {u: rows for u, rows in units.items() if rows}
            if units:
                out[ns][tag] = {"units": units}
    return out


def quality_asof(t, data, day, config):
    fx = filtered_facts(data, day)
    facts = dict(fx.get("us-gaap", {}))
    dei = fx.get("dei", {})
    if "EntityCommonStockSharesOutstanding" in dei:
        facts["EntityCommonStockSharesOutstanding"] = dei["EntityCommonStockSharesOutstanding"]
    fin = {"ticker": t, "cik": data.get("cik"), "entityName": data.get("entityName")}
    for key, tags in ff.CONCEPTS.items():
        fin[key] = ff.extract_concept(facts, tags, is_instant=key in ff.INSTANT_CONCEPTS, n_years=5)
    with contextlib.redirect_stdout(io.StringIO()):
        res = bfs.compute(t, fin, config, "quarter")
    return res.get("score"), bool(res.get("qualityFlags"))


def build_panel():
    uni = [r for r in json.load(open(SP500)) if r.get("sector") != "Financials"]
    config = json.load(open(bfs.DEFAULT_CONFIG))
    series, rows = {}, []
    for k, r in enumerate(uni):
        t, cik = r["ticker"], r["cik"].zfill(10)
        if t in EXCLUDE or not os.path.exists(os.path.join(EPS_DIR, t.replace(".", "-") + ".json")):
            continue
        pf = price_file(t)
        data = load_json(cik)
        if not pf or not data.get("facts"):
            continue
        bars = sorted(json.load(open(pf))["daily"], key=lambda b: b["date"])
        dates, closes = [b["date"] for b in bars], [b["c"] for b in bars]
        if len(dates) < 700:
            continue
        series[t] = (dates, closes)
        # 분할: 가격 파일(Yahoo)의 분할 기록으로 주식 수를 보정한다(v2/splits.py, Fable 지적 — 첫 실행은 미보정)
        import splits as _splits
        _splits.OVERRIDE[t] = [(s["date"], s["ratio"]) for s in (json.load(open(pf)).get("splits") or [])]
        # 카드 코드가 이 종목의 캐시를 읽게 한다(메모리 캐시, 종목마다 비운다)
        d.feh.CIKS[t] = cik
        d.bmh._facts = functools.lru_cache(maxsize=2)(lambda c, _data=data: _data if c == cik else {})
        filed_all = sorted({row.get("filed") for ns in data["facts"].values() for v in ns.values()
                            for rows in v["units"].values() for row in rows if row.get("filed")})
        month_ends = {}
        for i, dd in enumerate(dates):
            month_ends[dd[:7]] = i
        cache = {}
        for mth, i in sorted(month_ends.items()):
            if mth < START_MONTH:
                continue
            day, px = dates[i], closes[i]
            state = max((f for f in filed_all if f <= day), default=None)
            if state is None:
                continue
            if state not in cache:
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        b = d.base_inputs(t, day)
                        h = d.history(t, day)
                        ok = h and b.get("revenue") and b.get("shares") and b.get("opinc") is not None and b.get("tax") is not None
                        sc = d.scenarios(b, h, 0.10, 0.025) if ok else None
                except Exception:
                    ok, sc, b, h = False, None, None, None
                try:
                    q, qflag = quality_asof(t, data, day, config)
                except Exception:
                    q, qflag = None, None
                cache[state] = (b, h, sc, q, qflag)
            b, h, sc, q, qflag = cache[state]
            if not sc or sc[1]["per_share"] is None or sc[1]["per_share"] <= 0:
                base = None
            else:
                base = sc[1]["per_share"]
            req = None
            if base:
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        req = d.implied_growth(b, px, 0.10, 0.025, margin_path=d.margin_path_for(h, "기본"),
                                               s2c=d.s2c_path_for(b, "기본")[0])
                except Exception:
                    req = None
            rows.append({"t": t, "d": day, "i": i, "px": px, "base": base,
                         "ratio": (px / base) if base else None,
                         "g5": (h or {}).get("growth_5y") if h else None, "req": req,
                         "q": q, "qflag": qflag, "mcap": (b.get("shares") * px) if (b and b.get("shares")) else None})
        if k % 25 == 0:
            print(k, t, len(rows), flush=True)
    json.dump({"rows": rows}, open(PANEL, "w"))
    return rows, series


def add_returns(rows):
    series = {}
    for r in rows:
        if r["t"] not in series:
            bars = sorted(json.load(open(price_file(r["t"])))["daily"], key=lambda b: b["date"])
            series[r["t"]] = ([b["date"] for b in bars], [b["c"] for b in bars])
    means = {}
    for h in (H_MAIN, H_EXPL):
        for day in {r["d"] for r in rows}:
            v = []
            for ds, cs in series.values():
                try:
                    i = ds.index(day)
                except ValueError:
                    continue
                if i + h < len(cs):
                    v.append(cs[i + h] / cs[i] - 1)
            means[(day, h)] = float(np.mean(v)) if len(v) > 50 else None
        for r in rows:
            ds, cs = series[r["t"]]
            i = ds.index(r["d"])
            m = means.get((r["d"], h))
            r[f"x{h}"] = (cs[i + h] / cs[i] - 1 - m) if (i + h < len(cs) and m is not None) else None


def boot_weighted(vals, weights, block=6, n=5000, seed=42):
    vals, weights = np.asarray(vals, float), np.asarray(weights, float)
    k = len(vals)
    if k < block or k < 3:
        return None
    rng = np.random.default_rng(seed)
    out = np.empty(n)
    nb = -(-k // block)
    for b in range(n):
        idx = np.concatenate([np.arange(s, s + block) for s in rng.integers(0, k - block + 1, nb)])[:k]
        out[b] = np.average(vals[idx], weights=weights[idx])
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]


def analyze(rows):
    res = {"n_rows": len(rows), "n_tickers": len({r["t"] for r in rows})}
    # ① 분포
    def level(x):
        return None if x is None else ("매우 싸다" if x <= .7 else "싸다" if x <= .9 else "적정" if x <= 1.1 else "비싸다" if x <= 1.5 else "매우 비싸다")
    def dist(rs):
        c = {}
        for r in rs:
            lv = level(r["ratio"])
            if lv:
                c[lv] = c.get(lv, 0) + 1
        n = sum(c.values())
        return {k: round(v / n, 3) for k, v in c.items()} | {"n": n}
    last_m = max(r["d"][:7] for r in rows)
    last = [r for r in rows if r["d"][:7] == last_m]
    top50 = {r["t"] for r in sorted([r for r in last if r["mcap"]], key=lambda r: -r["mcap"])[:50]}
    res["dist_all"] = dist(rows)
    res["dist_last_month"] = dist(last) | {"month": last_m}
    res["dist_top50_last"] = dist([r for r in last if r["t"] in top50])
    res["dist_flag"] = any(v >= .70 for k, v in res["dist_all"].items() if k != "n")
    # ② 역-DCF vs D
    for h in (H_MAIN, H_EXPL):
        key = f"x{h}"
        months = sorted({r["d"][:7] for r in rows})
        icD, icR, dI, w = [], [], [], []
        for m in months:
            g = [r for r in rows if r["d"][:7] == m and r.get(key) is not None and r["ratio"] and r["req"] is not None and r["g5"] is not None]
            if len(g) < MIN_MONTH_N:
                continue
            y = [r[key] for r in g]
            D = [-math.log(r["ratio"]) for r in g]
            R = [r["g5"] - r["req"] for r in g]
            a, b = spearmanr(D, y).correlation, spearmanr(R, y).correlation
            icD.append(a); icR.append(b); dI.append(b - a); w.append(len(g))
        out = {"months": len(w)}
        if w:
            out.update({"IC_D": float(np.average(icD, weights=w)), "IC_D_ci": boot_weighted(icD, w),
                        "IC_R": float(np.average(icR, weights=w)), "IC_R_ci": boot_weighted(icR, w),
                        "dIC": float(np.average(dI, weights=w)), "dIC_ci": boot_weighted(dI, w)})
            if h == H_MAIN:
                ci = out["dIC_ci"]
                out["verdict_R"] = "통과(R로 교체)" if (out["dIC"] > 0 and ci and ci[0] > 0 and out["IC_R"] >= 0) else "미통과"
                cD = out["IC_D_ci"]
                out["verdict_D"] = "역방향" if (cD and cD[1] < 0) else ("양의 효과" if (cD and cD[0] > 0) else "0과 구분 안 됨")
        res[f"reverse_dcf_h{h}"] = out
    # ④ 품질 거부권
    for h in (H_MAIN, H_EXPL):
        key = f"x{h}"
        months = sorted({r["d"][:7] for r in rows})
        diffs, w, nlow = [], [], 0
        for m in months:
            g = [r for r in rows if r["d"][:7] == m and r.get(key) is not None and r["ratio"] and r["ratio"] <= .9 and r["q"] is not None]
            lo = [r[key] for r in g if r["q"] < 40]
            hi = [r[key] for r in g if r["q"] >= 40]
            nlow += len(lo)
            if lo and hi:
                diffs.append(np.mean(lo) - np.mean(hi)); w.append(min(len(lo), len(hi)))
        out = {"months": len(w), "n_low_quality_cheap": nlow}
        if w:
            out.update({"diff": float(np.average(diffs, weights=w)), "diff_ci": boot_weighted(diffs, w)})
            if h == H_MAIN:
                ci = out["diff_ci"]
                out["verdict"] = ("표본 부족" if nlow < 30 else
                                  "통과(거부권 채택)" if (out["diff"] < 0 and ci and ci[1] < 0) else "미통과")
        res[f"quality_veto_h{h}"] = out
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--analyze", action="store_true")
    a = ap.parse_args()
    if a.analyze:
        rows = json.load(open(PANEL))["rows"]
    else:
        rows, _ = build_panel()
    add_returns(rows)
    res = analyze(rows)
    json.dump(res, open(os.path.join(HERE, "valuation_judges_result.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))
