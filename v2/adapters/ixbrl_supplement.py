#!/usr/bin/env python3
"""companyfacts에 아직 안 들어온 최신 10-Q/10-K를 원문 인라인 XBRL에서 보충한다(2026-09-27, V).

SEC companyfacts는 가끔 최근 공시를 몇 달씩 싣지 않는다(JPM 카드의 C: 2026 10-Q 없음, V: 2026-07-29 10-Q 없음).
그 공시의 원문(인라인 XBRL)에서 **차원 없는** us-gaap·dei 수치만 꺼내 companyfacts 행 모양
({start?, end, val, accn, fy?, fp, form, filed})으로 `v2/.sec_cache/overlay/{cik}.json`에 더한다.
기존 오버레이의 다른 태그·행은 보존하고, 같은 (start, end, filed) 행은 다시 쓰지 않는다.

    python3 v2/adapters/ixbrl_supplement.py 0001403161
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cover_shares import get  # noqa: E402

CACHE = os.path.join(V2, ".sec_cache")


def parse(h):
    ctx = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        b = m.group(2)
        if "<xbrldi:explicitMember" in b or "<xbrldi:typedMember" in b:
            continue
        s, e, i = (re.search(rf"<xbrli:{k}>([^<]+)<", b) for k in ("startDate", "endDate", "instant"))
        ctx[m.group(1)] = (s.group(1), e.group(1)) if s and e else (None, i.group(1)) if i else None
    unit = {m.group(1): m.group(2) for m in re.finditer(r'<xbrli:unit id="([^"]+)">(.*?)</xbrli:unit>', h, re.S)}
    out = []
    for m in re.finditer(r'<ix:nonFraction([^>]*)>(.*?)</ix:nonFraction>', h, re.S):
        a = m.group(1)
        name = re.search(r'name="([^"]+)"', a).group(1)
        if not name.startswith(("us-gaap:", "dei:")):
            continue
        c = ctx.get(re.search(r'contextRef="([^"]+)"', a).group(1))
        txt = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if c and "fixed-zero" in a:
            txt = "0"                                   # ixt:fixed-zero("—")는 0이다(Codex)
        if not c or not re.match(r"^[\d,.]+$", txt):
            continue
        sc = re.search(r'scale="(-?\d+)"', a)
        v = float(txt.replace(",", "")) * 10 ** (int(sc.group(1)) if sc else 0)
        if 'sign="-"' in a:
            v = -v
        ub = unit.get((re.search(r'unitRef="([^"]+)"', a) or [None, ""])[1], "")
        u = "USD/shares" if "shares" in ub and "USD" in ub else "shares" if "shares" in ub else "USD" if "USD" in ub else "pure"
        out.append((name, c[0], c[1], v, u))
    return out


def main(cik):
    cik = cik.zfill(10)
    facts = json.load(open(os.path.join(CACHE, f"{cik}_facts.json")))
    have = {r["filed"] for t in facts["facts"].get("us-gaap", {}).values() for rows in t["units"].values() for r in rows}
    last = max(have)
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik}.json"))["filings"]["recent"]
    op = os.path.join(CACHE, "overlay", f"{cik}.json")
    data = json.load(open(op)) if os.path.exists(op) else {}
    raw = os.path.join(CACHE, f"ix_{cik}")
    os.makedirs(raw, exist_ok=True)
    added = 0
    for form, acc, filed, doc in zip(sub["form"], sub["accessionNumber"], sub["filingDate"], sub["primaryDocument"]):
        if form not in ("10-Q", "10-K") or filed <= last:
            continue
        h = get(f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}", os.path.join(raw, doc))
        fp = "FY" if form == "10-K" else "Q"
        seen = set()
        for name, s, e, v, u in parse(h):
            tax, tag = name.split(":")
            key = (tag, s, e)
            if key in seen:
                continue
            seen.add(key)
            rows = data.setdefault(tax, {}).setdefault(tag, [])
            if any(r.get("start") == s and r["end"] == e and r["filed"] == filed for r in rows):
                continue
            row = {"end": e, "val": v, "accn": acc, "fp": fp, "form": form, "filed": filed, "unit": u, "src": "ixbrl"}
            if s:
                row["start"] = s
            rows.append(row)
            added += 1
        print(f"{form} {filed} {doc}: 보충 {len(seen)}개 사실")
    os.makedirs(os.path.dirname(op), exist_ok=True)
    json.dump(data, open(op, "w"), indent=1)
    print(f"저장: {op} (+{added}행, companyfacts 마지막 공시 {last})")


if __name__ == "__main__":
    main(sys.argv[1])
