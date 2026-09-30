#!/usr/bin/env python3
"""GE 손익 영업외 항목 — 회사 고유 태그 두 개를 공시 원문(인라인 XBRL)에서 뽑는다.

GE 손익계산서에는 영업이익 줄이 없다. 영업이익 = 세전이익 − 기타수익(NonoperatingIncomeExpense)
+ 이자·기타 금융비용 + 영업외 연금비용(수익이면 음수)으로 합성한다(build_multiple_history.DERIVED_OPINC).
뒤 두 항목은 `ge:InterestAndOtherFinancialCharges`·`ge:BenefitCostIncomeNonoperating`(2021년까지 `ge:BenefitCostsNonoperating`)이라 companyfacts에 없다.
차원이 없는 기간(duration) 맥락의 값만 GE 전용 이름으로 `v2/.sec_cache/overlay/0000040545.json`에 쓴다.
Q2 2026 대조: 세전 2,801 − 기타수익 313 + 이자 215 + 연금 (−177) = 2,526 = 매출 13,349 − (원가·판관·분리·R&D·보험 비용) 10,823.

    python3 v2/adapters/ge_income_items.py
"""
import html
import json
import os
import re
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
CIK = "0000040545"
UA = "kim research gptjhss@gmail.com"
RAW = os.path.join(V2, ".sec_cache", "ge_filings")
OUT = os.path.join(V2, ".sec_cache", "overlay", f"{CIK}.json")
TAGS = {"ge:InterestAndOtherFinancialCharges": "GeInterestAndOtherFinancialCharges",
        "ge:BenefitCostIncomeNonoperating": "GeBenefitCostIncomeNonoperating",
        "ge:BenefitCostsNonoperating": "GeBenefitCostIncomeNonoperating"}   # 2021년까지의 이름(같은 줄, 비용이 양수)


def get(url, path=None):
    if path and os.path.exists(path):
        return open(path, encoding="utf-8", errors="ignore").read()
    txt = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, text=True).stdout
    time.sleep(0.2)
    if path:
        open(path, "w").write(txt)
    return txt


def contexts(h):
    """차원 없는 기간 맥락 → (시작, 끝)."""
    out = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        body = m.group(2)
        if "xbrldi:" in body:
            continue
        s, e = re.search(r"<xbrli:startDate>([^<]+)<", body), re.search(r"<xbrli:endDate>([^<]+)<", body)
        if s and e:
            out[m.group(1)] = (s.group(1), e.group(1))
    return out


def facts_in(h, ctx):
    got = {}
    for m in re.finditer(r'<ix:nonFraction([^>]*)>(.*?)</ix:nonFraction>', h, re.S):
        attrs, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        name = re.search(r'name="([^"]+)"', attrs).group(1)
        if name not in TAGS:
            continue
        c = re.search(r'contextRef="([^"]+)"', attrs).group(1)
        if c not in ctx:
            continue
        scale = int(re.search(r'scale="(-?\d+)"', attrs).group(1)) if 'scale="' in attrs else 0
        txt = html.unescape(txt).replace(",", "").strip()
        val = 0.0 if (not txt or not re.search(r"\d", txt)) else float(txt) * 10 ** scale
        if 'sign="-"' in attrs:
            val = -val
        got.setdefault(TAGS[name], {})[ctx[c]] = val
    return got


def main():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{CIK}.json"))["filings"]["recent"]
    rows = {}
    for form, acc, filed, doc in zip(sub["form"], sub["accessionNumber"], sub["filingDate"], sub["primaryDocument"]):
        if form not in ("10-Q", "10-K") or filed < "2019-01-01":
            continue
        url = f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{acc.replace('-', '')}/{doc}"
        h = get(url, os.path.join(RAW, doc))
        got = facts_in(h, contexts(h))
        for tag, by_per in got.items():
            for (start, end), val in by_per.items():
                rows.setdefault(tag, []).append({"start": start, "end": end, "val": val, "accn": acc, "form": form,
                                                 "filed": filed, "src": doc})
        print(f"{form} {filed} {doc}: " + ", ".join(f"{t[2:]} {len(v)}" for t, v in sorted(got.items())))
    overlay = json.load(open(OUT)) if os.path.exists(OUT) else {}
    overlay.setdefault("us-gaap", {}).update(rows)
    json.dump(overlay, open(OUT, "w"), indent=1)
    print(f"저장: {OUT} ({sum(len(v) for v in rows.values())}행)")


if __name__ == "__main__":
    main()
