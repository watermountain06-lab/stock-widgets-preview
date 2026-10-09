"""밴드 적중률 색 기준 5년 재측정 (2026-10-09, `c14_hit_recalib_5y.md`).
C14(`c14_band_halflife.py`)의 one()과 같은 밴드(H180·트레일링 2년·10~90 백분위·최소 240일)에 가격만 `.prices10y`(2016-10~)를 써서
2021년 체크포인트도 2년 표본을 갖게 한다. 구간마다 날짜별 밴드 안/밖을 남기고, 종목별 일수 가중 적중률의 10·90 분위를 낸다.
    python3 v2/research/c14_hit_recalib_5y.py            # 구간 계산(약 3분) + 표
    python3 v2/research/c14_hit_recalib_5y.py --reuse    # 저장한 구간 파일로 표만
"""
import bisect, json, math, os, sys
from datetime import date, timedelta
REPO = os.path.expanduser("~/Workspace/stock-widgets-preview"); V2 = os.path.join(REPO, "v2")
sys.path.insert(0, V2); sys.path.insert(0, os.path.join(REPO, "scripts")); sys.path.insert(0, os.path.join(V2, "research"))
import c14_band_halflife as c14
cb, bmh, rb = c14.cb, c14.bmh, c14.rb
DATA = c14.DATA; P10 = os.path.join(V2, "research", ".prices10y")
TAXONEOFF = {k for k in json.load(open(os.path.join(V2, "tax_oneoff.json"))) if not k.startswith("_")}

def one(t):
    pp, ep = os.path.join(P10, f"{t}.json"), os.path.join(DATA, "sp500_eps", f"{t}.json")
    if not (os.path.exists(pp) and os.path.exists(ep)): return None
    pr = json.load(open(pp)); daily = [(d["date"], d["c"]) for d in pr["daily"] if d.get("c")]
    if len(daily) < 700: return None
    splits = [(s["date"], s["ratio"]) for s in pr.get("splits") or [] if s.get("ratio")]
    raw_rows = [e for e in json.load(open(ep)) if e.get("ttm_eps") is not None and e.get("available_date")]
    raw_rows.sort(key=lambda e: e["available_date"])
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
    dates = [d for d, _ in daily]
    boxes = []
    for k, t0 in enumerate(fdates):
        if t0 < dates[0] or t0 >= dates[-1]: continue
        x0 = ttm(t0)
        if not x0 or x0 <= 0: continue
        nxt = fdates[k + 1] if k + 1 < len(fdates) else None
        if not nxt or nxt > dates[-1]: continue
        ws = (date.fromisoformat(t0) - timedelta(days=730)).isoformat()
        if ws < dates[0]: continue
        samp = [(d, p) for d, p in per.items() if ws <= d < t0 and not inramp(d)]
        if len(samp) < c14.MIN_SAMPLE: continue
        pairs = [(p, cb.recency_weight(d, t0, 180)) for d, p in samp]
        lo, hi = c14.wpct(pairs, 10), c14.wpct(pairs, 90)
        if lo <= 0: continue
        days = [(d, lo <= per[d] <= hi) for d in dates if t0 < d < nxt and d in per]
        if days: boxes.append({"start": t0, "end": nxt, "ramp": inramp(t0), "days": days})
    return boxes

BOXES = os.path.join(V2, ".sec_cache", "_work", "c14_hit_recalib_boxes.json")   # 18MB — 커밋하지 않고 다시 만든다


def q(v, p):
    """선형 보간 분위."""
    v = sorted(v); x = (len(v) - 1) * p; i = int(x); f = x - i
    return v[i] + (v[min(i + 1, len(v) - 1)] - v[i]) * f


def per_stock(B, lo, hi, clip, weighted=True, min_boxes=4):
    """카드 헤더와 같은 집계 — 흑자 초기(램프) 구간 제외, 끝난 구간만, 체크포인트 당일 제외(구간 계산에서), 일수 가중.
    clip=True면 창에 걸친 구간은 창 안 날만 센다(카드 DAILY 첫날 기준, refresh_backtest의 clipped_from과 같음)."""
    out = {}
    for t, bs in B.items():
        covs, ins, tot = [], 0, 0
        for b in bs:
            if b.get("ramp"): continue
            if clip:
                if b["end"] <= lo or b["end"] > hi: continue
                days = [x for x in b["days"] if lo <= x[0] <= hi]
            else:
                if not (b["start"] >= lo and b["end"] <= hi): continue
                days = b["days"]
            if not days: continue
            k = sum(1 for _, h in days if h); covs.append(k / len(days)); ins += k; tot += len(days)
        if len(covs) >= min_boxes:
            out[t] = ins / tot if weighted else sum(covs) / len(covs)
    return out


if __name__ == "__main__":
    if "--reuse" not in sys.argv:
        tick = sorted(f[:-5] for f in os.listdir(os.path.join(DATA, "sp500_5y")) if f.endswith(".json") and f[:-5] not in c14.EXCLUDE)
        out = {}
        for t in tick:
            try:
                b = one(t)
            except Exception as e:
                print("skip", t, str(e)[:60]); continue
            if b: out[t] = b
        os.makedirs(os.path.dirname(BOXES), exist_ok=True)
        json.dump(out, open(BOXES, "w"))
    B = json.load(open(BOXES))
    print("종목", len(B), "구간", sum(len(v) for v in B.values()))
    for name, lo, hi, clip in (("옛 창(10-04 기준 재현)", "2023-09-13", "2026-09-11", False), ("5년 창", "2021-10-07", "2026-10-01", True)):
        for w in (True, False):
            for mn in (1, 4):
                v = list(per_stock(B, lo, hi, clip, w, mn).values())
                print(f"{name} {'일수 가중' if w else '단순 평균'} 최소 {mn}구간: 종목 {len(v)} · 10/50/90 분위 "
                      f"{q(v,.1):.3f} {q(v,.5):.3f} {q(v,.9):.3f} · 평균 {sum(v)/len(v):.3f}")
