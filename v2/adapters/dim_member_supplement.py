#!/usr/bin/env python3
"""차원 하나가 붙어 companyfacts에서 빠진 대차대조표 값을 원문 인라인 XBRL에서 보충한다(2026-10-01, TMUS).

TMUS는 2026년 10-Q부터 장기차입금(us-gaap:LongTermDebtNoncurrent)을 특수관계자 차원
(RelatedPartyTransactionsByRelatedPartyAxis = NonrelatedPartyMember)을 붙여서만 냈고, 분기 차입금 총계는 늘 차원 태그였다. companyfacts는 차원 있는
사실을 싣지 않아 장기차입금이 2025-12-31에서 멈췄고, 엔진 차입금이 단기차입금 $6.1B뿐이었다(실제 $84.6B).
이 스크립트는 지정한 태그·차원·멤버 **하나만** 붙은 시점 값을 차원 없는 행으로 `.sec_cache/overlay/{cik}.json`에 더한다.
companyfacts에 같은 (end, filed) 행이 있으면 건너뛴다.

    python3 v2/adapters/dim_member_supplement.py 0001283699 us-gaap:LongTermDebt \
        us-gaap:DebtInstrumentAxis tmus:TotalDebtMember 2021-01-01

TMUS는 장기차입금 줄 대신 10-Q 차입금 주석의 "Total debt"(TotalDebtMember, 단기 + 장기 + 특수관계자, 금융리스 제외)를 쓴다 —
분기마다 차원 하나로 나오고 2021년까지 거슬러 같은 정의다(2026-10-01).
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


def contexts(h, dim, member):
    out = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        b = m.group(2)
        mems = re.findall(r'<xbrldi:explicitMember dimension="([^"]+)">([^<]+)<', b)
        if mems != [(dim, member)] or "<xbrldi:typedMember" in b:
            continue
        i = re.search(r"<xbrli:instant>([^<]+)<", b)
        if i:
            out[m.group(1)] = i.group(1)
    return out


def main(cik, name, dim, member, since):
    cik = cik.zfill(10)
    tax, tag = name.split(":")
    facts = json.load(open(os.path.join(CACHE, f"{cik}_facts.json")))
    have = {(r["end"], r["filed"]) for rows in facts["facts"].get(tax, {}).get(tag, {}).get("units", {}).values() for r in rows}
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik}.json"))["filings"]["recent"]
    op = os.path.join(CACHE, "overlay", f"{cik}.json")
    data = json.load(open(op)) if os.path.exists(op) else {}
    rows = data.setdefault(tax, {}).setdefault(tag, [])
    raw = os.path.join(CACHE, f"ix_{cik}")
    os.makedirs(raw, exist_ok=True)
    added = 0
    for form, acc, filed, doc in zip(sub["form"], sub["accessionNumber"], sub["filingDate"], sub["primaryDocument"]):
        if form not in ("10-Q", "10-K") or filed < since:
            continue
        h = get(f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}", os.path.join(raw, doc))
        ctx = contexts(h, dim, member)
        for m in re.finditer(r'<ix:nonFraction([^>]*)>(.*?)</ix:nonFraction>', h, re.S):
            a = m.group(1)
            if f'name="{name}"' not in a:
                continue
            end = ctx.get(re.search(r'contextRef="([^"]+)"', a).group(1))
            txt = re.sub(r"<[^>]+>", "", m.group(2)).strip()
            if not end or not re.match(r"^[\d,.]+$", txt) or (end, filed) in have:
                continue
            sc = re.search(r'scale="(-?\d+)"', a)
            v = float(txt.replace(",", "")) * 10 ** (int(sc.group(1)) if sc else 0)
            if any(r["end"] == end and r["filed"] == filed for r in rows):
                continue
            unit = "shares" if re.search(r'unitRef="[^"]*shares', a, re.I) else "USD"   # 주식 수(SCHW 발행 보통주, 2026-10-01)
            rows.append({"end": end, "val": v, "accn": acc, "fp": "FY" if form == "10-K" else "Q", "form": form,
                         "filed": filed, "unit": unit, "src": f"ixbrl:{dim}={member}"})
            added += 1
            print(f"{form} {filed}: {tag} {end} = {v / 1e6:,.1f}M {unit}")
    os.makedirs(os.path.dirname(op), exist_ok=True)
    json.dump(data, open(op, "w"), indent=1)
    print(f"저장: {op} (+{added}행)")


if __name__ == "__main__":
    main(*sys.argv[1:6])
