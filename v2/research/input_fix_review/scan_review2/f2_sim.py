# F2 (a)+(b) 2판 규칙을 2022-10-31 공시 상태에서 전 종목 매출 TTM에 적용해 기준(지금 규칙)과 비교한다. 가격·수익률 안 씀.
import sys, os, json, io, contextlib, glob, collections
sys.path.insert(0, "/private/tmp/claude-501/-Users-watermountain-Workspace-second-brain/bbfd380b-94a7-4972-94ba-641e4f0c0be6/scratchpad/rfv/fable")
import helper as H
from datetime import date
bmh, pit, vr = H.bmh, H.pit, H.vr
feh = vr.d.feh
ASOF = sys.argv[1] if len(sys.argv) > 1 else "2022-10-31"
cards = {os.path.basename(p).replace("_full_widget.html", "") for p in glob.glob("/Users/watermountain/Workspace/stock-widgets-preview/v2/*_full_widget.html")}
EXCL, REV = "RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"
days = lambda e: (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days

def names_for(cik):
    names = list(bmh.FLOW_TAGS["revenue"])
    extra = bmh.EXTRA_TAGS.get(cik, {})
    names = names + [x for n in names for x in extra.get(n, []) if x not in names]
    names = [n for n in names if n not in bmh.EXCLUDE_TAGS.get(cik, ())]
    names = [n for n in bmh.PREFER_TAGS.get(cik, ()) if n in names] + [n for n in names if n not in bmh.PREFER_TAGS.get(cik, ())]
    return names

def tagged_rows(cik):
    out = []
    for n in names_for(cik):
        for r in bmh.concept(cik, n):
            if "start" in r and "end" in r and "filed" in r:
                out.append(dict(r, _tag=n))
    return out

def rule_a(rows):
    """같은 (start,end)에 Rev·Excl이 함께 있고 Rev/Excl > 1.02 (= 2% 넘게 다르고 Rev ≥ 0.98×Excl)이면 Excl 행을 버린다."""
    first = {}
    for r in rows:
        k = (r["start"], r["end"], r["_tag"])
        if k not in first or r["filed"] < first[k]["filed"]:
            first[k] = r
    drop = set(); hits = []
    for (s, e, t), r in first.items():
        if t != REV: continue
        x = first.get((s, e, EXCL))
        if x and x["val"] and r["val"] / x["val"] > 1.02:
            drop.add((s, e)); hits.append((s, e, round(r["val"] / x["val"], 3)))
    return [r for r in rows if not (r["_tag"] == EXCL and (r["start"], r["end"]) in drop)], hits

def rule_b(rows):
    """매출 3개월 행이 같은 태그·같은 종료일의 첫 공시 12개월 값과 2% 안이고 같은 회계연도 9개월 누계(>0)가 있으면 버린다."""
    ann = {}
    for r in rows:
        if days(r) > 350:
            k = (r["end"], r["_tag"])
            if k not in ann or r["filed"] < ann[k]["filed"]: ann[k] = r
    out = []; hits = []
    for r in rows:
        if 80 <= days(r) <= 100:
            a = ann.get((r["end"], r["_tag"]))
            if a and a["val"] and abs(r["val"] / a["val"] - 1) <= 0.02 and r["val"] != a["val"] \
               and any(x["start"] == a["start"] and x["val"] > 0 and 250 <= days(x) <= 290 for x in rows):
                hits.append((r["start"], r["end"], r["val"], a["val"])); continue
        out.append(r)
    return out, hits

def ttm_of(rows, t):
    with contextlib.redirect_stdout(io.StringIO()):
        q = bmh.quarterly_flow(rows, t)
        return {e["end"]: (round(e["val"] / 1e6), e["available"]) for e in bmh.ttm_series(q)}, {e["end"]: round(e["val"] / 1e6) for e in q}

targets = ["UDR", "SBAC", "IRM", "AMT", "CCI", "ESS", "EXR", "URI", "DOC", "INVH", "DVN", "GD", "ORCL", "PM", "CPT", "BLK", "GIS", "MA", "ADP", "CAT", "COST", "GE", "NVDA", "CVX", "XOM"]
sec = {r["ticker"]: r.get("sector") for r in json.load(open(vr.v.SP500))}
changed = {}
for t in sorted(H.UNI):
    try:
        cik, data, pj = H.setup(t)
    except Exception:
        continue
    state = H.filed_state(data, ASOF)
    if not state: continue
    pit.install(bmh, cik, data, state, ref=ASOF)
    try:
        rows = tagged_rows(cik)
        base, _ = ttm_of(rows, t)
        ra, ha = rule_a(rows)
        rb, hb = rule_b(ra)
        new, qnew = ttm_of(rb, t)
    finally:
        pit.reset(bmh)
    ends = sorted(set(base) | set(new))
    ends = [e for e in ends if e >= "2017-01-01"]
    diff = [(e, base.get(e), new.get(e)) for e in ends if base.get(e) != new.get(e)]
    if diff or t in targets:
        changed[t] = (diff, ha, hb, base, new, qnew)
print(f"# F2 (a)+(b) at state ≤ {ASOF}: tickers with any TTM change (2017+):", len([t for t, v in changed.items() if v[0]]))
for t, (diff, ha, hb, base, new, qnew) in changed.items():
    vd = [d for d in diff if d[1] is None or d[2] is None or d[1][0] != d[2][0]]
    ad = [d for d in diff if d[1] and d[2] and d[1][0] == d[2][0] and d[1][1] != d[2][1]]
    print(f"{t} {sec.get(t)} {'CARD' if t in cards else ''}: value-changes={len(vd)} avail-only={len(ad)} ruleA-hits={len(ha)} ruleB-hits={len(hb)}")
    for d in vd[:6]: print("    val", d)
    for d in ad[:3]: print("    avail", d)
    if hb: print("    ruleB:", hb[:4])
    if t in ("GD", "ORCL", "PM", "CPT", "BLK", "GIS", "UDR", "AMT"):
        print("    TTM new:", [(e, v) for e, v in sorted(new.items()) if "2017-06" <= e <= "2019-01"])
        print("    TTM base:", [(e, v) for e, v in sorted(base.items()) if "2017-06" <= e <= "2019-01"])
        print("    q new:", [(e, v) for e, v in sorted(qnew.items()) if "2017-01" <= e <= "2018-12"])
