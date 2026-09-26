#!/usr/bin/env python3
"""③ 단계 보정표 — 지금 모델과 A(10년 2단계 + 재투자 시점 수정)를 같은 패널에서 비교한다.

사전 등록: research/two_stage_prereg.md ③. S&P500 통제 유니버스(금융 제외), 월말 평가,
그때 공시된 자료만(base_inputs(asof)), 126거래일 동일가중 초과수익. 데이터 품질 표시(dq)의
차입금 누락 의심·주식 수 없음 행은 뺀다(2026-09-25 결정).

    python3 v2/research/step_calibration.py            # 패널 생성 + 분석
    python3 v2/research/step_calibration.py --analyze  # 저장된 패널로 분석만
"""
import contextlib
import functools
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import numpy as np  # noqa: E402
import valuation_judges_test as v  # noqa: E402

d = v.d
PANEL = os.path.join(HERE, "step_calibration_panel.json")
RESULT = os.path.join(HERE, "step_calibration_result.json")
CONFIGS = {"now": (False, "fade"), "A": (True, "two_stage")}
LEVELS = ["매우 싸다", "싸다", "적정", "비싸다", "매우 비싸다"]


def level(x):
    if x is None:
        return None
    return LEVELS[0] if x <= .7 else LEVELS[1] if x <= .9 else LEVELS[2] if x <= 1.1 else LEVELS[3] if x <= 1.5 else LEVELS[4]


def build():
    uni = [r for r in json.load(open(v.SP500)) if r.get("sector") != "Financials"]
    rows = []
    for k, r in enumerate(uni):
        t, cik = r["ticker"], r["cik"].zfill(10)
        if t in v.EXCLUDE or not os.path.exists(os.path.join(v.EPS_DIR, t.replace(".", "-") + ".json")):
            continue
        pf = v.price_file(t)
        data = v.load_json(cik)
        if not pf or not data.get("facts"):
            continue
        bars = sorted(json.load(open(pf))["daily"], key=lambda b: b["date"])
        dates, closes = [b["date"] for b in bars], [b["c"] for b in bars]
        if len(dates) < 700:
            continue
        import splits as _splits
        _splits.OVERRIDE[t] = [(s["date"], s["ratio"]) for s in (json.load(open(pf)).get("splits") or [])]
        d.feh.CIKS[t] = cik
        d.bmh._facts = functools.lru_cache(maxsize=2)(lambda c, _data=data: _data if c == cik else {})
        filed_all = sorted({row.get("filed") for ns in data["facts"].values() for vv in ns.values()
                            for rr in vv["units"].values() for row in rr if row.get("filed")})
        month_ends = {}
        for i, dd in enumerate(dates):
            month_ends[dd[:7]] = i
        cache = {}
        for mth, i in sorted(month_ends.items()):
            if mth < v.START_MONTH:
                continue
            day, px = dates[i], closes[i]
            state = max((f for f in filed_all if f <= day), default=None)
            if state is None:
                continue
            if state not in cache:
                res = {"dq": []}
                try:
                    with contextlib.redirect_stdout(io.StringIO()):
                        b = d.base_inputs(t, day)
                        h = d.history(t, day)
                        res["dq"] = b.get("dq") or []
                        okk = h and b.get("revenue") and b.get("shares") and b.get("opinc") is not None
                        for name, (lead, path) in CONFIGS.items():
                            d.REINVEST_LEAD = lead
                            b.pop("_s2c_marginal", None)
                            sc = d.scenarios(b, h, 0.10, 0.025, path=path) if okk else None
                            base = sc[1]["per_share"] if sc and sc[1]["per_share"] and sc[1]["per_share"] > 0 else None
                            res[name] = base
                        d.REINVEST_LEAD = False
                except Exception:
                    d.REINVEST_LEAD = False
                cache[state] = res
            res = cache[state]
            row = {"t": t, "d": day, "i": i, "px": px, "dq": res.get("dq", [])}
            for name in CONFIGS:
                base = res.get(name)
                row[f"ratio_{name}"] = (px / base) if base else None
            rows.append(row)
        if k % 25 == 0:
            print(k, t, len(rows), flush=True)
    json.dump({"rows": rows}, open(PANEL, "w"))
    return rows


def analyze(rows):
    bad = lambda r: any(str(x).startswith(("debt_suspect", "shares_missing")) for x in r["dq"])
    before = len(rows)
    rows = [r for r in rows if not bad(r)]
    v.add_returns(rows)
    res = {"rows_total": before, "rows_used": len(rows), "excluded_dq": before - len(rows),
           "tickers": len({r["t"] for r in rows}), "horizon": v.H_MAIN}
    for name in CONFIGS:
        tab = {}
        for lv in LEVELS:
            xs = [r[f"x{v.H_MAIN}"] for r in rows if level(r[f"ratio_{name}"]) == lv and r.get(f"x{v.H_MAIN}") is not None]
            tk = {r["t"] for r in rows if level(r[f"ratio_{name}"]) == lv}
            tab[lv] = {"n": len(xs), "tickers": len(tk),
                       "mean": round(float(np.mean(xs)), 4) if xs else None,
                       "median": round(float(np.median(xs)), 4) if xs else None}
        cheap = [r[f"x{v.H_MAIN}"] for r in rows if (r[f"ratio_{name}"] or 9) <= .9 and r.get(f"x{v.H_MAIN}") is not None]
        dear = [r[f"x{v.H_MAIN}"] for r in rows if (r[f"ratio_{name}"] or 0) > 1.5 and r.get(f"x{v.H_MAIN}") is not None]
        dist = {lv: sum(1 for r in rows if level(r[f"ratio_{name}"]) == lv) for lv in LEVELS}
        tot = sum(dist.values())
        res[name] = {"table": tab, "cheap_le_0.9_mean": round(float(np.mean(cheap)), 4) if cheap else None,
                     "dear_gt_1.5_mean": round(float(np.mean(dear)), 4) if dear else None,
                     "ends_order_ok": (np.mean(cheap) >= np.mean(dear)) if cheap and dear else None,
                     "dist": {k2: round(c / tot, 3) for k2, c in dist.items()} if tot else {}}
        res[name]["ends_order_ok"] = bool(res[name]["ends_order_ok"]) if res[name]["ends_order_ok"] is not None else None
    json.dump(res, open(RESULT, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return res


if __name__ == "__main__":
    rows = json.load(open(PANEL))["rows"] if "--analyze" in sys.argv else build()
    analyze(rows)
