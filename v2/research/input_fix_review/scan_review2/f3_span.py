# F3 (d) 400일 창 검사: pit.eps_ttm과 같은 방식으로 분기(10-Q 3개월 + 10-K에서 유도한 4분기)를 만들고,
# 네 분기 창의 "첫 start ~ 끝 end" 일수와 "첫 end ~ 끝 end" 일수를 잰다. 가격·수익률 안 씀.
import json, os, collections
from datetime import date
R = "/Users/watermountain/Workspace/stock-widgets-preview/v2/research"
SP = "/Users/watermountain/Workspace/stock-widgets-redesign/scripts/sp500.json"
uni = {r["ticker"]: r["cik"].zfill(10) for r in json.load(open(SP))}
D = date.fromisoformat
def quarters_like_pit(rows):
    pdays = lambda e: (D(e["end"]) - D(e["start"])).days if "start" in e else -1
    def first(sel):
        b = {}
        for e in sel:
            k = (e["start"], e["end"])
            if k not in b or e["filed"] < b[k]["filed"]: b[k] = e
        return sorted(b.values(), key=lambda e: e["end"])
    qs = first([e for e in rows if e.get("form") == "10-Q" and 80 <= pdays(e) <= 100])
    fy = first([e for e in rows if e.get("form") == "10-K" and pdays(e) > 350])
    quarters = list(qs)
    for f in fy:
        fe = D(f["end"])
        mem = [q for q in qs if D(q["end"]) <= fe and (fe - D(q["start"])).days <= 380 and (fe - D(q["end"])).days <= 280]
        if len(mem) == 3 and not any(q["end"] == f["end"] for q in qs):
            quarters.append({"end": f["end"], "start": max(mem, key=lambda m: m["end"])["end"], "val": 0, "filed": f["filed"], "derived": True})
    quarters.sort(key=lambda e: e["end"])
    return quarters
over400 = collections.Counter(); gap_but_under = []; normal_max = 0; normal_over371 = []; n = 0; by_span = collections.Counter()
for t, cik in sorted(uni.items()):
    p = os.path.join(R, ".facts_20261002", f"{cik}_facts.json")
    if not os.path.exists(p): continue
    rows = json.load(open(p)).get("facts", {}).get("us-gaap", {}).get("EarningsPerShareDiluted", {}).get("units", {}).get("USD/shares", [])
    if not rows: continue
    qs = quarters_like_pit(rows)
    for i in range(3, len(qs)):
        w = qs[i - 3:i + 1]
        if w[-1]["end"] < "2016": continue
        n += 1
        span = (D(w[-1]["end"]) - D(w[0]["start"])).days
        e2e = (D(w[-1]["end"]) - D(w[0]["end"])).days
        maxgap = max((D(b["end"]) - D(a["end"])).days for a, b in zip(w, w[1:]))
        by_span[span // 10 * 10] += 1
        if span > 400: over400[t] += 1
        if maxgap > 100 and span <= 400: gap_but_under.append((t, w[0]["start"], w[-1]["end"], span, maxgap))
        if maxgap <= 100:
            normal_max = max(normal_max, span)
            if span > 371: normal_over371.append((t, w[0]["start"], w[-1]["end"], span, maxgap))
print("windows 2016+:", n, "| span>400:", sum(over400.values()), "tickers", len(over400))
print("top >400:", over400.most_common(20))
print("max span among windows with all gaps<=100:", normal_max, "| >371:", len(normal_over371), normal_over371[:15])
print("windows with a gap>100 but span<=400 (would slip through):", len(gap_but_under), gap_but_under[:20])
print("span histogram (10-day bins, 340..460):", sorted((k, v) for k, v in by_span.items() if 340 <= k <= 460))
