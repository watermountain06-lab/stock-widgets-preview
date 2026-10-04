#!/usr/bin/env python3
"""C14 ② 반감기 비교 — 사전 등록 `c14_band_prereg.md`를 그대로 따른다(돌린 뒤 문서를 고치지 않는다).
S&P500 통제 유니버스에서 구간마다 로그 PER 공간 구간 점수(α=0.2)를 내고, 반감기 변형끼리 같은 구간에서 짝지어 비교한다.
    python3 v2/research/c14_band_halflife.py --out v2/research/c14_band_result.json
"""
import argparse, bisect, json, math, os, random, sys
from datetime import date, timedelta
HERE = os.path.dirname(os.path.abspath(__file__)); V2 = os.path.dirname(HERE); REPO = os.path.dirname(V2)
sys.path.insert(0, V2); sys.path.insert(0, os.path.join(REPO, "scripts"))
import compute_earnings_backtest_band as cb
import build_multiple_history as bmh
import refresh_backtest as rb
DATA = os.path.join(os.path.dirname(REPO), "stock-widgets-redesign", "data")
EXCLUDE = {"MRNA", "ECHO", "GL", "APP"}
VARIANTS = {"H90": 90, "H180": 180, "H365": 365, "HFLAT": None}
ALPHA, MIN_SAMPLE, LEARN, HOLD = 0.2, 240, ("2023-09-01", "2025-06-30"), "2025-07-01"

def wpct(pairs, pct):
    return cb.weighted_percentile(pairs, pct)

def one(t):
    pp, ep = os.path.join(DATA, "sp500_5y", f"{t}.json"), os.path.join(DATA, "sp500_eps", f"{t}.json")
    if not (os.path.exists(pp) and os.path.exists(ep)): return None
    pr = json.load(open(pp)); daily = [(d["date"], d["c"]) for d in pr["daily"] if d.get("c")]
    if len(daily) < 700: return None
    splits = [(s["date"], s["ratio"]) for s in pr.get("splits") or [] if s.get("ratio")]
    raw_rows = [e for e in json.load(open(ep)) if e.get("ttm_eps") is not None and e.get("available_date")]
    raw_rows.sort(key=lambda e: e["available_date"])
    # 통제 유니버스 EPS 파일은 종목마다 분할 조정 여부가 다르다(NVDA·AVGO는 이미 조정 — Codex). 분할 직전·직후 공시의 분기 EPS가
    # 분할 비율만큼 뛰면 원자료로 보고 보정하고, 아니면 이미 조정된 것으로 둔다(변경 기록 2026-10-04).
    raw_splits = []
    for d, k in splits:
        bef = [e for e in raw_rows if e["available_date"] < d and e.get("quarter_eps")]
        aft = [e for e in raw_rows if e["available_date"] >= d and e.get("quarter_eps")]
        if bef and aft and aft[0]["quarter_eps"] and abs(bef[-1]["quarter_eps"] / aft[0]["quarter_eps"]) > math.sqrt(k):
            raw_splits.append((d, k))
    rows = []
    for e in raw_rows:
        r = 1.0
        for d, k in raw_splits:
            if e["available_date"] < d: r *= k
        adj = bmh.oneoff_in_ttm(t, e.get("quarter_end"), "eps") if t in TAXONEOFF else 0.0
        rows.append({**e, "ttm_eps": e["ttm_eps"] / r + adj, "quarter_eps": (e.get("quarter_eps") or 0) / r})
    rows.sort(key=lambda e: e["available_date"])
    if not rows: return None
    av = [e["available_date"] for e in rows]; tt = [e["ttm_eps"] for e in rows]
    def ttm(day):
        i = bisect.bisect_right(av, day) - 1
        return tt[i] if i >= 0 else None
    per = {}
    for d, c in daily:
        x = ttm(d)
        if x and x > 0: per[d] = c / x
    ramps = rb.ramp_windows(rows, daily[-1][0])
    inramp = lambda d: any(a <= d <= b for a, b in ramps)
    first = {}
    for e in rows:
        q = e.get("quarter_end") or e["available_date"]; first[q] = min(first.get(q, e["available_date"]), e["available_date"])
    fdates = sorted(first.values())
    dates = [d for d, _ in daily]; dpos = {d: i for i, d in enumerate(dates)}
    boxes = []
    for k, t0 in enumerate(fdates):
        if t0 < dates[0] or t0 >= dates[-1]: continue
        x0 = ttm(t0)
        if not x0 or x0 <= 0: continue
        nxt = fdates[k + 1] if k + 1 < len(fdates) else None
        if not nxt or nxt > dates[-1]: continue      # 끝난 구간만
        ws = (date.fromisoformat(t0) - timedelta(days=730)).isoformat()
        if ws < dates[0]: continue
        samp = [(d, p) for d, p in per.items() if ws <= d < t0 and not inramp(d)]
        if len(samp) < MIN_SAMPLE: continue
        path = [per[d] for d in dates if t0 < d < nxt and d in per]
        if not path: continue
        row = {"t": t, "start": t0, "end": nxt, "month": nxt[:7], "n": len(path)}
        for name, hl in VARIANTS.items():
            pairs = [(p, 1.0 if hl is None else cb.recency_weight(d, t0, hl)) for d, p in samp]
            lo, hi = wpct(pairs, 10), wpct(pairs, 90)
            if lo <= 0: break
            lL, lU = math.log(lo), math.log(hi)
            iss = [(lU - lL) + (2 / ALPHA) * (max(0, lL - math.log(p)) + max(0, math.log(p) - lU)) for p in path]
            row[name] = {"is": sum(iss) / len(iss), "cover": sum(1 for p in path if lo <= p <= hi) / len(path),
                         "width": hi / lo, "below": sum(1 for p in path if p < lo) / len(path), "above": sum(1 for p in path if p > hi) / len(path)}
        else:
            boxes.append(row)
    return boxes

def monthly_mean(rows, f):
    by = {}
    for r in rows: by.setdefault(r["month"], []).append(f(r))
    ms = sorted(by); vals = [sum(by[m]) / len(by[m]) for m in ms]; w = [len(by[m]) for m in ms]
    return ms, vals, w

def wmean(v, w): return sum(a * b for a, b in zip(v, w)) / sum(w) if w else None

def boot(vals, w, B=5000, blk=6, seed=7):
    rnd = random.Random(seed); n = len(vals); out = []
    if n == 0: return (None, None)
    for _ in range(B):
        idx = []
        while len(idx) < n:
            s = rnd.randrange(n); idx += [(s + j) % n for j in range(blk)]
        idx = idx[:n]; out.append(wmean([vals[i] for i in idx], [w[i] for i in idx]))
    out.sort(); return (out[int(0.025 * B)], out[int(0.975 * B) - 1])

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); a = ap.parse_args()
    global TAXONEOFF
    TAXONEOFF = {k for k in json.load(open(os.path.join(V2, "tax_oneoff.json"))) if not k.startswith("_")}
    tick = sorted(f[:-5] for f in os.listdir(os.path.join(DATA, "sp500_5y")) if f.endswith(".json") and f[:-5] not in EXCLUDE)
    boxes = []
    for t in tick:
        try:
            b = one(t)
        except Exception as e:
            print("skip", t, str(e)[:60]); continue
        if b: boxes += b
    res = {"boxes": len(boxes), "tickers": len({b["t"] for b in boxes}), "variants": {}}
    for split, cond in (("learn", lambda r: LEARN[0] <= r["start"] <= LEARN[1]), ("hold", lambda r: r["start"] >= HOLD)):
        rows = [r for r in boxes if cond(r)]
        part = {"boxes": len(rows)}
        for name in VARIANTS:
            ms, v, w = monthly_mean(rows, lambda r: r[name]["is"])
            cov = wmean(*monthly_mean(rows, lambda r: r[name]["cover"])[1:])
            wid = sorted(r[name]["width"] for r in rows); bel = wmean(*monthly_mean(rows, lambda r: r[name]["below"])[1:])
            abv = wmean(*monthly_mean(rows, lambda r: r[name]["above"])[1:])
            d = {"is": wmean(v, w), "cover": cov, "width_median": wid[len(wid) // 2] if wid else None, "below": bel, "above": abv}
            if name != "H180":
                ms2, dv, dw = monthly_mean(rows, lambda r: r[name]["is"] - r["H180"]["is"])
                d["dIS"] = wmean(dv, dw); d["dIS_ci"] = boot(dv, dw); d["months"] = len(ms2)
            part[name] = d
        res["variants"][split] = part
    learn = res["variants"]["learn"]; hold = res["variants"]["hold"]
    cands = [n for n in VARIANTS if n != "H180" and learn[n]["dIS"] < 0 and learn[n]["dIS_ci"][1] is not None and learn[n]["dIS_ci"][1] < 0]
    best = min(cands, key=lambda n: learn[n]["dIS"]) if cands else None
    res["rule"] = {"learn_candidates": cands, "best": best, "hold_dIS": hold[best]["dIS"] if best else None,
                   "decision": (best if best and hold[best]["dIS"] < 0 else "H180")}
    json.dump(res, open(a.out, "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
