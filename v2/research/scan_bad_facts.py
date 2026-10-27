#!/usr/bin/env python3
"""companyfacts의 잘못된 개별 사실 후보를 찾는다(E55, 읽기 전용 — 고치지 않는다. 사람이 원문을 보고 v2/fact_fixes.json에 넣는다).

고침 적용 **전** 자료로 본다(FACT_FIXES=off). 흐름 태그(매출·영업이익·세전이익·영업현금흐름·설비투자)만.
  (a) 같은 accn·같은 end에 start가 0~3일 다른 행이 둘 이상이고 값이 다르다(NTAP형)
  (b) 분기 기간(80~100일) 행이 같은 태그·같은 accn의 앞 2·3분기 누계와 ±2%로 같다(누계를 분기로 태그),
      또는 10-K의 분기 기간 행이 같은 해 9개월 누계보다 크다(LHX형 — 같은 accn·기간의 다른 태그도 함께 적는다)
  (c) 엔진 분기 값이 앞뒤 분기 중앙값의 0.4~0.6·1.7~2.3·3.5~4.5배(참고 — 2020 코로나·인수 급증 거짓 양성이 많다)

    python3 v2/research/scan_bad_facts.py                 # 카드 종목
    python3 v2/research/scan_bad_facts.py --sp500         # S&P500 전체(캐시가 있는 종목)
    python3 v2/research/scan_bad_facts.py --tickers NTAP,LHX
"""
import argparse
import contextlib
import glob
import io
import json
import os
import statistics
import sys
from datetime import date

os.environ["FACT_FIXES"] = "off"
HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, V2)
import build_multiple_history as bmh  # noqa: E402

SP500 = "/Users/watermountain/Workspace/stock-widgets-redesign/scripts/sp500.json"
SERIES = {"revenue": bmh.FLOW_TAGS["revenue"], "opinc": bmh.EBITDA_TAGS["opinc"], "ocf": bmh.FLOW_TAGS["ocf"],
          "capex": bmh.FLOW_TAGS["capex"],
          "pretax": ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"]}
BANDS = [(0.4, 0.6), (1.7, 2.3), (3.5, 4.5)]


def days(r):
    return (date.fromisoformat(r["end"]) - date.fromisoformat(r["start"])).days


def scan(t, cik):
    out = []
    data = bmh._facts(cik).get("facts", {})
    for name, tags in SERIES.items():
        for tag in tags:
            rows = [r for r in data.get("us-gaap", {}).get(tag, {}).get("units", {}).get("USD", []) if r.get("start")]
            by = {}
            for r in rows:
                by.setdefault((r.get("accn"), r["end"]), []).append(r)
            for (accn, end), rs in by.items():
                for i, a in enumerate(rs):
                    for b in rs[i + 1:]:
                        gap = abs((date.fromisoformat(a["start"]) - date.fromisoformat(b["start"])).days)
                        if gap <= 3 and a["val"] != b["val"] and 80 <= days(a) <= 100 and 80 <= days(b) <= 100:
                            out.append(("a", t, name, tag, f"{accn} end {end}: start {a['start']} {a['val']/1e6:,.0f} 대 {b['start']} {b['val']/1e6:,.0f}"))
                qs = [r for r in rs if 80 <= days(r) <= 100]
                ytd = [r for r in rows if r.get("accn") == accn and r["end"] == end and 170 <= days(r) <= 290]
                for qr in qs:
                    for y in ytd:
                        if y["val"] and abs(qr["val"] / y["val"] - 1) <= 0.02:
                            out.append(("b", t, name, tag, f"{accn} end {end}: 분기 {qr['val']/1e6:,.0f} ≈ 누계({days(y)}일) {y['val']/1e6:,.0f}"))
                    if str(qr.get("form", "")).startswith("10-K"):
                        nine = [r for r in rows if r["end"] < end and 260 <= days(r) <= 290
                                and (date.fromisoformat(end) - date.fromisoformat(r["end"])).days < 110]
                        if nine and qr["val"] > max(r["val"] for r in nine) > 0:
                            ctx = sorted({tg for tg, v in data.get("us-gaap", {}).items() for u in v.get("units", {}).values()
                                          for r in u if r.get("accn") == accn and r.get("start") == qr["start"] and r["end"] == end})
                            out.append(("b", t, name, tag, f"{accn} 10-K 분기 기간 {qr['start']}~{end} {qr['val']/1e6:,.0f} > 9개월 {max(r['val'] for r in nine)/1e6:,.0f} — 같은 기간 태그 {len(ctx)}개"))
        with contextlib.redirect_stdout(io.StringIO()):
            u, rr = bmh.pick_tag(cik, tags)
            q = bmh.quarterly_flow(rr, t) if rr else []
        vals = [e["val"] for e in q]
        for i in range(2, len(q) - 2):
            nb = vals[i - 2:i] + vals[i + 1:i + 3]
            med = statistics.median(nb)
            if med > 0 and vals[i] > 0:
                k = vals[i] / med
                if any(lo <= k <= hi for lo, hi in BANDS):
                    out.append(("c", t, name, u, f"{q[i]['end']}: {vals[i]/1e6:,.0f} = 앞뒤 중앙값 {med/1e6:,.0f}의 {k:.2f}배"))
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--sp500", action="store_true"); ap.add_argument("--tickers")
    a = ap.parse_args()
    sp = {r["ticker"]: r["cik"].zfill(10) for r in json.load(open(SP500))}
    if a.tickers:
        tick = a.tickers.split(",")
    elif a.sp500:
        tick = sorted(t for t, c in sp.items() if os.path.exists(os.path.join(bmh.CACHE_DIR, f"{c}_facts.json")))
    else:
        tick = sorted(os.path.basename(p)[:-len("_full_widget.html")] for p in glob.glob(os.path.join(V2, "*_full_widget.html")))
    res = []
    for t in tick:
        cik = sp.get(t) or bmh.feh.CIKS.get(t)
        if not cik or not os.path.exists(os.path.join(bmh.CACHE_DIR, f"{str(cik).zfill(10)}_facts.json")):
            continue
        res += scan(t, str(cik).zfill(10))
    order = {"a": 0, "b": 1, "c": 2}
    for kind, t, name, tag, msg in sorted(res, key=lambda x: (order[x[0]], x[1])):
        print(f"({kind}) {t:6} {name:8} {msg}")
    print(f"\n후보 {len(res)}건 — (a) {sum(r[0]=='a' for r in res)}, (b) {sum(r[0]=='b' for r in res)}, (c) {sum(r[0]=='c' for r in res)}")


if __name__ == "__main__":
    main()
