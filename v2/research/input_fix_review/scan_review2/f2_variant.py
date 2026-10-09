# F2 (a) 두 가지 판정 단위를 비교: v1 = 2판(기간(start,end)마다), v2 = 같은 start(회계연도)의 가장 긴 기간으로 판정해
# 그 start의 겹침 기간(Rev 행이 있는 것)에 적용. 2022-10-31 공시 상태. 가격·수익률 안 씀. 인자: 종목들 또는 ALL.
import sys, os, json, io, contextlib, glob
sys.path.insert(0, "/private/tmp/claude-501/-Users-watermountain-Workspace-second-brain/bbfd380b-94a7-4972-94ba-641e4f0c0be6/scratchpad/rfv/fable")
import helper as H
from datetime import date
bmh, pit, vr = H.bmh, H.pit, H.vr
ASOF = "2022-10-31"
cards = {os.path.basename(p).replace("_full_widget.html", "") for p in glob.glob("/Users/watermountain/Workspace/stock-widgets-preview/v2/*_full_widget.html")}
EXCL, REV = "RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"
days = lambda e: (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days
sec = {r["ticker"]: r.get("sector") for r in json.load(open(vr.v.SP500))}

def names_for(cik):
    names = list(bmh.FLOW_TAGS["revenue"])
    extra = bmh.EXTRA_TAGS.get(cik, {})
    names = names + [x for n in names for x in extra.get(n, []) if x not in names]
    names = [n for n in names if n not in bmh.EXCLUDE_TAGS.get(cik, ())]
    return [n for n in bmh.PREFER_TAGS.get(cik, ()) if n in names] + [n for n in names if n not in bmh.PREFER_TAGS.get(cik, ())]

def tagged_rows(cik):
    return [dict(r, _tag=n) for n in names_for(cik) for r in bmh.concept(cik, n) if "start" in r and "end" in r and "filed" in r]

def firsts(rows):
    first = {}
    for r in rows:
        k = (r["start"], r["end"], r["_tag"])
        if k not in first or r["filed"] < first[k]["filed"]: first[k] = r
    return first

def rule_v1(rows):
    first = firsts(rows); drop = set()
    for (s, e, t), r in first.items():
        x = first.get((s, e, EXCL))
        if t == REV and x and x["val"] and r["val"] / x["val"] > 1.02: drop.add((s, e))
    return [r for r in rows if not (r["_tag"] == EXCL and (r["start"], r["end"]) in drop)]

def rule_v2(rows):
    first = firsts(rows)
    both = {}
    for (s, e, t), r in first.items():
        if t == REV and (s, e, EXCL) in first: both.setdefault(s, []).append((days(r), e))
    drop = set()
    for s, lst in both.items():
        _, e = max(lst)                      # 같은 start의 가장 긴 겹침 기간으로 판정
        r, x = first[(s, e, REV)], first[(s, e, EXCL)]
        if x["val"] and r["val"] / x["val"] > 1.02:
            drop.update((s, e2) for _, e2 in lst)   # 그 start의 모든 겹침 기간에서 Excl을 버린다
    return [r for r in rows if not (r["_tag"] == EXCL and (r["start"], r["end"]) in drop)]

def rule_b(rows):
    ann = {}
    for r in rows:
        if days(r) > 350:
            k = (r["end"], r["_tag"])
            if k not in ann or r["filed"] < ann[k]["filed"]: ann[k] = r
    out = []
    for r in rows:
        if 80 <= days(r) <= 100:
            a = ann.get((r["end"], r["_tag"]))
            if a and a["val"] and abs(r["val"] / a["val"] - 1) <= 0.02 and r["val"] != a["val"] \
               and any(x["start"] == a["start"] and x["val"] > 0 and 250 <= days(x) <= 290 for x in rows):
                continue
        out.append(r)
    return out

def ttm_of(rows, t):
    with contextlib.redirect_stdout(io.StringIO()):
        q = bmh.quarterly_flow(rows, t)
        return {e["end"]: (round(e["val"] / 1e6), e["available"]) for e in bmh.ttm_series(q)}, {e["end"]: round(e["val"] / 1e6) for e in q}

args = sys.argv[1:]
tickers = sorted(H.UNI) if args == ["ALL"] else args
summary = []
for t in tickers:
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
        v1, q1 = ttm_of(rule_b(rule_v1(rows)), t)
        v2, q2 = ttm_of(rule_b(rule_v2(rows)), t)
    finally:
        pit.reset(bmh)
    ends = [e for e in sorted(set(base) | set(v1) | set(v2)) if e >= "2017-01-01"]
    d1 = [e for e in ends if (base.get(e) or (None,))[0] != (v1.get(e) or (None,))[0]]
    d2 = [e for e in ends if (base.get(e) or (None,))[0] != (v2.get(e) or (None,))[0]]
    d12 = [e for e in ends if (v1.get(e) or (None,))[0] != (v2.get(e) or (None,))[0]]
    if d1 or d2 or args != ["ALL"]:
        summary.append((t, sec.get(t), "CARD" if t in cards else "", len(d1), (d1[0], d1[-1]) if d1 else None, len(d2), (d2[0], d2[-1]) if d2 else None, len(d12), d12[:4]))
        if args != ["ALL"] or d12:
            print(t, "v1 vs v2 differ at", [(e, v1.get(e), v2.get(e)) for e in d12][:6])
            if t == "GD":
                print("  GD q v1:", [(e, v) for e, v in sorted(q1.items()) if "2017" <= e <= "2018-12"])
                print("  GD q v2:", [(e, v) for e, v in sorted(q2.items()) if "2017" <= e <= "2018-12"])
                print("  GD ttm v2:", [(e, v) for e, v in sorted(v2.items()) if "2017-06" <= e <= "2019-01"])
print("\n# ticker, sector, card, n_changed_v1, range_v1, n_changed_v2, range_v2, n_v1≠v2, first few")
for s in summary: print(s)
