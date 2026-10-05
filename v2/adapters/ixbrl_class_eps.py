#!/usr/bin/env python3
"""주식 종류별로만 EPS를 태그하는 회사의 희석 EPS를 10-Q·10-K 원문 인라인 XBRL에서 꺼내 오버레이에 더한다(2026-10-05, D66).

HSY(보통주·Class B)·CVNA(Class A·B)는 희석 EPS를 `StatementClassOfStockAxis` 차원으로만 태그해 SEC companyfacts(차원 없는 값만 싣는다)에
EPS가 없다. 상장된 종류(HSY 보통주, CVNA Class A)의 차원 값만 골라 `v2/.sec_cache/overlay/{cik}.json`의 us-gaap:EarningsPerShareDiluted에
차원 없는 행처럼 넣는다(`src: "ixbrl-class:<member>"`). `fetch_eps_history`는 SEC 자료에 없는 (start, end)만 오버레이에서 채운다.
비교군은 최근 4분기만 쓰므로 since 이후 공시만 읽는다.

    python3 v2/adapters/ixbrl_class_eps.py 0000047111 us-gaap:CommonStockMember 2024-06-01
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
TAG = "EarningsPerShareDiluted"


def parse(h, member):
    ctx = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        b = m.group(2)
        mem = re.findall(r'<xbrldi:explicitMember dimension="([^"]+)">([^<]+)<', b)
        if mem != [("us-gaap:StatementClassOfStockAxis", member)] or "<xbrldi:typedMember" in b:
            continue                                     # 그 종류 하나만 걸린 문맥
        s, e = re.search(r"<xbrli:startDate>([^<]+)<", b), re.search(r"<xbrli:endDate>([^<]+)<", b)
        if s and e:
            ctx[m.group(1)] = (s.group(1), e.group(1))
    out = {}
    for m in re.finditer(rf'<ix:nonFraction([^>]*name="us-gaap:{TAG}"[^>]*)>(.*?)</ix:nonFraction>', h, re.S):
        c = ctx.get(re.search(r'contextRef="([^"]+)"', m.group(1)).group(1))
        txt = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if not c or not re.match(r"^[\d,.]+$", txt):
            continue
        sc = re.search(r'scale="(-?\d+)"', m.group(1))
        v = float(txt.replace(",", "")) * 10 ** (int(sc.group(1)) if sc else 0)
        if 'sign="-"' in m.group(1):
            v = -v
        out[c] = v
    return out


def main(cik, member, since):
    cik = cik.zfill(10)
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik}.json"))["filings"]["recent"]
    op = os.path.join(CACHE, "overlay", f"{cik}.json")
    data = json.load(open(op)) if os.path.exists(op) else {}
    rows = data.setdefault("us-gaap", {}).setdefault(TAG, [])
    raw = os.path.join(CACHE, f"ix_{cik}")
    os.makedirs(raw, exist_ok=True)
    added = 0
    for form, acc, filed, doc in zip(sub["form"], sub["accessionNumber"], sub["filingDate"], sub["primaryDocument"]):
        if form not in ("10-Q", "10-K") or filed < since:
            continue
        h = get(f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}", os.path.join(raw, doc))
        vals = parse(h, member)
        for (s, e), v in vals.items():
            if any(r.get("start") == s and r["end"] == e and r["filed"] == filed for r in rows):
                continue
            rows.append({"start": s, "end": e, "val": v, "accn": acc, "fp": "FY" if form == "10-K" else "Q", "form": form,
                         "filed": filed, "unit": "USD/shares", "src": f"ixbrl-class:{member}"})
            added += 1
        print(f"{form} {filed} {doc}: {member} 희석 EPS {len(vals)}개")
    os.makedirs(os.path.dirname(op), exist_ok=True)
    json.dump(data, open(op, "w"), indent=1)
    print(f"저장: {op} (+{added}행)")


if __name__ == "__main__":
    main(*sys.argv[1:4])
