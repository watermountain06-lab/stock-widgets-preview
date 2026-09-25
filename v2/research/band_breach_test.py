#!/usr/bin/env python3
"""밴드 연속 이탈 신호 검증 — v2/research/band_breach_prereg.md의 사전 등록을 그대로 구현한다.

    python3 v2/research/band_breach_test.py            # 결과 요약 출력 + band_breach_result.json
"""
import json
import math
import os
import sys
from datetime import date, timedelta

import numpy as np
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = "/Users/watermountain/Workspace/stock-widgets-redesign/data"
PRICE_DIR, EPS_DIR = os.path.join(DATA, "sp500_5y"), os.path.join(DATA, "sp500_eps")
EXCLUDE = {"MRNA", "ECHO", "GL", "APP"}
TRAIL_DAYS, HALFLIFE, LO, HI, MIN_SAMPLE = 730, 180.0, 10, 90, 100
F_BREACH = 1 / 3
H_MAIN, H_EXPL = 63, 126
MIN_MONTH_N = 20


def wpct(pairs, pct):
    pairs = sorted(pairs)
    tot = sum(w for _, w in pairs)
    tgt, cum = pct / 100 * tot, 0.0
    for v, w in pairs:
        cum += w
        if cum >= tgt:
            return v
    return pairs[-1][0]


def ttm_asof(eps, dates):
    e = sorted(eps, key=lambda x: x["available_date"])
    out, p = [], -1
    for d in dates:
        while p + 1 < len(e) and e[p + 1]["available_date"] <= d:
            p += 1
        out.append(e[p]["ttm_eps"] if p >= 0 else None)
    return out


def ticker_rows(t):
    bars = sorted(json.load(open(os.path.join(PRICE_DIR, t + ".json")))["daily"], key=lambda b: b["date"])
    dates = [b["date"] for b in bars]
    closes = np.array([b["c"] for b in bars], float)
    if len(dates) < 700:
        return [], dates, closes
    eps = json.load(open(os.path.join(EPS_DIR, t + ".json")))
    ttm = ttm_asof(eps, dates)
    per = np.array([closes[i] / ttm[i] if (ttm[i] and ttm[i] > 0) else np.nan for i in range(len(dates))])
    idx = {d: i for i, d in enumerate(dates)}
    start = date.fromisoformat(dates[0])
    # 체크포인트(실적 공시일)와 밴드
    cps = []
    for e in sorted(eps, key=lambda x: x["available_date"]):
        d = e["available_date"]
        if d < dates[0] or d > dates[-1] or e["ttm_eps"] <= 0:
            continue
        td = date.fromisoformat(d)
        ws = td - timedelta(days=TRAIL_DAYS)
        if ws < start:
            continue
        i0 = next(i for i, x in enumerate(dates) if x >= d)
        sample = [(per[j], 0.5 ** ((td - date.fromisoformat(dates[j])).days / HALFLIFE))
                  for j in range(i0) if dates[j] >= ws.isoformat() and not np.isnan(per[j])]
        if len(sample) < MIN_SAMPLE:
            continue
        cps.append({"d": d, "i": i0, "lo": wpct(sample, LO), "hi": wpct(sample, HI)})
    # 끝난 박스
    boxes = []
    for a, b in zip(cps, cps[1:]):
        seg = [per[j] for j in range(a["i"], b["i"]) if not np.isnan(per[j])]
        if len(seg) < 20:
            continue
        seg = np.array(seg)
        fb, ft = float(np.mean(seg < a["lo"])), float(np.mean(seg > a["hi"]))
        br = 0
        if fb >= F_BREACH and fb >= ft:
            br = 1
        elif ft >= F_BREACH:
            br = -1
        w = math.log(a["hi"] / a["lo"]) if a["hi"] > a["lo"] > 0 else None
        e = (float(np.mean(np.maximum(0, np.log(a["lo"]) - np.log(seg)) - np.maximum(0, np.log(seg) - np.log(a["hi"])))) / w
             if w else 0.0)
        dp = math.log(closes[b["i"] - 1] / closes[a["i"]])
        te0, te1 = closes[a["i"]] / per[a["i"]] if not np.isnan(per[a["i"]]) else None, \
            closes[b["i"] - 1] / per[b["i"] - 1] if not np.isnan(per[b["i"] - 1]) else None
        de = math.log(te1 / te0) if (te0 and te1 and te0 > 0 and te1 > 0) else None
        boxes.append({"end": b["d"], "end_i": b["i"], "br": br, "e": e, "dp": dp, "de": de})
    rows = []
    for k in range(3, len(boxes)):
        last4 = boxes[k - 3:k + 1]
        s1 = sum(x["br"] for x in last4)
        cur = boxes[k]["br"]
        s2 = 0
        if cur != 0:
            n = 0
            for x in reversed(boxes[:k + 1]):
                if x["br"] == cur:
                    n += 1
                else:
                    break
            s2 = cur * min(n, 4)
        i = boxes[k]["end_i"]
        if i < 252:
            continue
        hist = per[:i + 1]
        hist = hist[~np.isnan(hist)]
        if len(hist) < 500 or np.isnan(per[i]):
            continue
        rows.append({"t": t, "d": dates[i], "i": i, "S1": s1, "S2": s2, "S3": boxes[k]["e"],
                     "pct": float(np.mean(hist < per[i])), "mom": float(closes[i - 21] / closes[i - 252] - 1),
                     "dp": boxes[k]["dp"], "de": boxes[k]["de"]})
    return rows, dates, closes


def nw_t(x, lag=3):
    x = np.asarray(x, float)
    n = len(x)
    if n < 3:
        return float("nan")
    m = x.mean()
    u = x - m
    s = u @ u / n
    for L in range(1, lag + 1):
        s += 2 * (1 - L / (lag + 1)) * (u[L:] @ u[:-L]) / n
    return float(m / math.sqrt(s / n)) if s > 0 else float("nan")


def main():
    tickers = sorted(f[:-5] for f in os.listdir(EPS_DIR)
                     if f.endswith(".json") and os.path.exists(os.path.join(PRICE_DIR, f)) and f[:-5] not in EXCLUDE)
    allrows, series = [], {}
    for t in tickers:
        try:
            r, d, c = ticker_rows(t)
        except Exception as ex:
            print("skip", t, ex, file=sys.stderr)
            continue
        allrows += r
        series[t] = (d, c)
    # 같은 날 유니버스 평균 수익률
    def fwd(t, d, h):
        ds, cs = series[t]
        try:
            i = ds.index(d)
        except ValueError:
            return None
        return cs[i + h] / cs[i] - 1 if i + h < len(cs) else None
    date_mean = {}
    def uni_mean(d, h):
        k = (d, h)
        if k not in date_mean:
            v = [x for x in (fwd(t, d, h) for t in series) if x is not None]
            date_mean[k] = float(np.mean(v)) if len(v) > 50 else None
        return date_mean[k]
    for r in allrows:
        for h in (H_MAIN, H_EXPL):
            f, m = fwd(r["t"], r["d"], h), uni_mean(r["d"], h)
            r[f"x{h}"] = (f - m) if (f is not None and m is not None) else None
    out = {"n_tickers": len(series), "n_rows": len(allrows), "tests": {}, "diagnostics": {}}
    for h, tag in ((H_MAIN, "main"), (H_EXPL, "explore")):
        rows = [r for r in allrows if r.get(f"x{h}") is not None]
        months = sorted({r["d"][:7] for r in rows})
        res = {}
        for s in ("S1", "S2", "S3"):
            ics, raw = [], []
            for mth in months:
                g = [r for r in rows if r["d"][:7] == mth]
                if len(g) < MIN_MONTH_N:
                    continue
                y = np.array([r[f"x{h}"] for r in g]); x = np.array([r[s] for r in g], float)
                X = np.column_stack([np.ones(len(g)), [r["pct"] for r in g], [r["mom"] for r in g]])
                beta, *_ = np.linalg.lstsq(X, x, rcond=None)
                resid = x - X @ beta
                if np.std(resid) == 0 or np.std(x) == 0:
                    continue
                ics.append((mth, spearmanr(resid, y).correlation)); raw.append(spearmanr(x, y).correlation)
            vals = [v for _, v in ics]
            half = len(vals) // 2
            res[s] = {"months": len(vals), "resid_ic": float(np.mean(vals)) if vals else None,
                      "nw_t": nw_t(vals) if vals else None, "raw_ic": float(np.mean(raw)) if raw else None,
                      "first_half": float(np.mean(vals[:half])) if half else None,
                      "second_half": float(np.mean(vals[half:])) if vals else None,
                      "window": [ics[0][0], ics[-1][0]] if ics else None}
            v = res[s]
            if tag == "main" and v["resid_ic"] is not None:
                if v["resid_ic"] >= 0.02 and v["nw_t"] >= 2.4 and v["first_half"] > 0 and v["second_half"] > 0:
                    v["verdict"] = "통과"
                elif v["resid_ic"] <= -0.02 and v["nw_t"] <= -2.4:
                    v["verdict"] = "반대 방향(추세 정보)"
                else:
                    v["verdict"] = "미확인"
        out["tests" if tag == "main" else "diagnostics"][f"h{h}"] = res
        # 진단: 상단·하단 분리, 원인 분해
        grp = lambda cond: [r[f"x{h}"] for r in rows if cond(r)]
        diag = {}
        for name, cond in (("S1>=+2(하단 연속)", lambda r: r["S1"] >= 2), ("S1<=-2(상단 연속)", lambda r: r["S1"] <= -2),
                           ("그 밖", lambda r: -2 < r["S1"] < 2),
                           ("최근 박스 하단·가격 주도", lambda r: r["S2"] > 0 and r["de"] is not None and abs(r["dp"]) >= abs(r["de"])),
                           ("최근 박스 하단·EPS 주도", lambda r: r["S2"] > 0 and r["de"] is not None and abs(r["dp"]) < abs(r["de"])),
                           ("최근 박스 상단·가격 주도", lambda r: r["S2"] < 0 and r["de"] is not None and abs(r["dp"]) >= abs(r["de"])),
                           ("최근 박스 상단·EPS 주도", lambda r: r["S2"] < 0 and r["de"] is not None and abs(r["dp"]) < abs(r["de"]))):
            v = grp(cond)
            diag[name] = {"n": len(v), "mean_excess": float(np.mean(v)) if v else None,
                          "tickers": len({r["t"] for r in rows if cond(r)})}
        out["diagnostics"][f"groups_h{h}"] = diag
    json.dump(out, open(os.path.join(HERE, "band_breach_result.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
