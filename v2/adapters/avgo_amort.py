#!/usr/bin/env python3
"""AVGO 무형자산 상각 보충 — companyfacts에 빠진 2020~2025 값을 공시 원문(인라인 XBRL)에서 뽑는다.

AVGO는 2025-12 이전 공시에서 무형자산 상각을 회사 자체 태그 두 줄로 냈다
(avgo:Amortizationofacquisitionrelatedintangibleassetscostofproductssold + …operatingexpenses).
companyfacts는 표준 태그만 모으므로 그 기간 us-gaap:AmortizationOfIntangibleAssets가 비고,
감가상각이 분기 $0.15B만 잡혀 EBITDA가 분기 약 $2B 작게, EV/EBITDA 이력이 부풀어 나왔다(2026-09-25).

두 줄의 합(차원 없는 맥락)을 us-gaap:AmortizationOfIntangibleAssets 행 모양으로
`v2/.sec_cache/overlay/0001730168.json`에 쓴다. `build_multiple_history._facts`가 불러올 때
같은 (start, end)가 이미 있으면 덮지 않고 빈 기간만 채운다.

    python3 v2/adapters/avgo_amort.py
"""
import json
import os
import re
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
CIK = "0001730168"
UA = "kim research gptjhss@gmail.com"
RAW = os.path.join(V2, ".sec_cache", "avgo_filings")
OUT = os.path.join(V2, ".sec_cache", "overlay", f"{CIK}.json")
PARTS = ("avgo:Amortizationofacquisitionrelatedintangibleassetscostofproductssold",
         "avgo:Amortizationofacquisitionrelatedintangibleassetsoperatingexpenses")


def get(url, path=None):
    if path and os.path.exists(path):
        return open(path, encoding="utf-8", errors="ignore").read()
    txt = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, text=True).stdout
    time.sleep(0.2)
    if path:
        open(path, "w").write(txt)
    return txt


def contexts(h):
    out = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        body = m.group(2)
        if "xbrldi:" in body:          # 차원(부문·항목 분해)이 붙은 맥락은 뺀다
            continue
        s = re.search(r"<xbrli:startDate>([^<]+)<", body)
        e = re.search(r"<xbrli:endDate>([^<]+)<", body)
        if s and e:
            out[m.group(1)] = (s.group(1), e.group(1))
    return out


def facts_in(h, ctx):
    got = {}
    for m in re.finditer(r'<ix:nonFraction([^>]*)>(.*?)</ix:nonFraction>', h, re.S):
        attrs, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        name = re.search(r'name="([^"]+)"', attrs).group(1)
        if name not in PARTS:
            continue
        c = re.search(r'contextRef="([^"]+)"', attrs).group(1)
        if c not in ctx:
            continue
        scale = int(re.search(r'scale="(-?\d+)"', attrs).group(1)) if 'scale="' in attrs else 0
        val = float(txt.replace(",", "") or 0) * 10 ** scale
        if 'sign="-"' in attrs:
            val = -val
        got.setdefault(ctx[c], {})[name] = val
    return got


def main():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{CIK}.json"))["filings"]["recent"]
    rows = []
    for form, acc, filed, doc in zip(sub["form"], sub["accessionNumber"], sub["filingDate"], sub["primaryDocument"]):
        if form not in ("10-Q", "10-K") or filed < "2020-01-01":
            continue
        url = f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{acc.replace('-', '')}/{doc}"
        h = get(url, os.path.join(RAW, doc))
        got = facts_in(h, contexts(h))
        for (s, e), parts in sorted(got.items()):
            if len(parts) != 2:
                print(f"  ⚠ {doc} {s}~{e}: 두 줄 중 {len(parts)}개만 — 버림")
                continue
            rows.append({"start": s, "end": e, "val": sum(parts.values()), "accn": acc,
                         "form": form, "filed": filed, "src": doc})
        print(f"{form} {filed} {doc}: {len(got)}개 기간")
    json.dump({"us-gaap": {"AmortizationOfIntangibleAssets": rows}}, open(OUT, "w"), indent=1)
    print(f"저장: {OUT} ({len(rows)}행)")


if __name__ == "__main__":
    main()
