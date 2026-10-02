#!/usr/bin/env python3
"""회사 고유 태그를 공시 원문(인라인 XBRL)에서 뽑아 표준 태그 이름으로 overlay에 싣는다(2026-10-02, COP).

SEC companyfacts에는 us-gaap·dei 태그만 있다. 설비투자·이자비용 같은 핵심 줄을 회사 고유 태그로만 내는 회사는
엔진이 그 값을 못 본다(COP 설비투자 cop:PaymentToAcquireProductiveAssetsAndInvestments, NEE 설비투자·이자비용).
since 이후의 10-Q·10-K 원문에서 **차원 없는** 그 태그 값을 모두 꺼내 `.sec_cache/overlay/{cik}.json`의 표준 태그 이름 아래
`src: company:{원래 태그}`로 더한다(같은 기간·공시일 행은 다시 쓰지 않는다). 원문은 `.sec_cache/ix_{cik}/`에 캐시한다.

    python3 v2/adapters/company_tag_feed.py 0001163165 cop:PaymentToAcquireProductiveAssetsAndInvestments PaymentsToAcquireProductiveAssets --since 2020-01-01
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cover_shares import get  # noqa: E402
from ixbrl_supplement import CACHE, parse  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cik"); ap.add_argument("company_tag"); ap.add_argument("std_tag")
    ap.add_argument("--since", default="2020-01-01")
    a = ap.parse_args()
    cik = a.cik.zfill(10); prefix = a.company_tag.split(":")[0] + ":"
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik}.json"))["filings"]["recent"]
    op = os.path.join(CACHE, "overlay", f"{cik}.json")
    data = json.load(open(op)) if os.path.exists(op) else {}
    rows = data.setdefault("us-gaap", {}).setdefault(a.std_tag, [])
    raw = os.path.join(CACHE, f"ix_{cik}"); os.makedirs(raw, exist_ok=True)
    added = 0
    for form, acc, filed, doc in zip(sub["form"], sub["accessionNumber"], sub["filingDate"], sub["primaryDocument"]):
        if form not in ("10-Q", "10-K") or filed < a.since or not doc.endswith(".htm"):
            continue
        h = get(f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}", os.path.join(raw, doc))
        seen = set(); n = 0
        for name, s, e, v, u in parse(h, prefixes=(prefix,)):
            if name != a.company_tag or (s, e) in seen:
                continue
            seen.add((s, e))
            if any(r.get("start") == s and r["end"] == e and r["filed"] == filed for r in rows):
                continue
            row = {"end": e, "val": v, "accn": acc, "fp": "FY" if form == "10-K" else "Q", "form": form, "filed": filed,
                   "unit": u, "src": f"company:{a.company_tag}"}
            if s:
                row["start"] = s
            rows.append(row); added += 1; n += 1
        print(f"{form} {filed}: {n}행")
    json.dump(data, open(op, "w"), indent=1)
    print(f"저장: {op} ({a.std_tag} +{added}행)")


if __name__ == "__main__":
    main()
