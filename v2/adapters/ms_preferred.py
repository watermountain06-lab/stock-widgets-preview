#!/usr/bin/env python3
"""MS 우선주 잔액 — 회사 고유 태그 `ms:PreferredStockCarryingValue`(재무상태표 "Preferred stock", 2026-06-30 $9,750M)를
공시 원문(인라인 XBRL)에서 뽑아 `PreferredStockValue` 이름으로 `v2/.sec_cache/overlay/0000895421.json`에 쓴다.
companyfacts에는 표준 우선주 태그가 2026년 분기에 없어 은행 세트의 보통주 자본(CE = 자본 − 우선주)이 비었다(2026-10-01).

    python3 v2/adapters/ms_preferred.py
"""
import html
import json
import os
import re
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
CIK = "0000895421"
UA = "kim research gptjhss@gmail.com"
RAW = os.path.join(V2, ".sec_cache", "ms_filings")
OUT = os.path.join(V2, ".sec_cache", "overlay", f"{CIK}.json")
TAGS = {"ms:PreferredStockCarryingValue": "PreferredStockValue"}


def get(url, path=None):
    if path and os.path.exists(path):
        return open(path, encoding="utf-8", errors="ignore").read()
    txt = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, text=True).stdout
    time.sleep(0.2)
    if path:
        open(path, "w").write(txt)
    return txt


def contexts(h):
    """차원 없는 시점(instant) 맥락 → 결산일."""
    out = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        body = m.group(2)
        if "xbrldi:" in body:
            continue
        e = re.search(r"<xbrli:instant>([^<]+)<", body)
        if e:
            out[m.group(1)] = e.group(1)
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
        got.setdefault(TAGS[name], {})[ctx[c]] = val
    return got


def filings():
    s = json.loads(get(f"https://data.sec.gov/submissions/CIK{CIK}.json"))
    pages = [s["filings"]["recent"]]
    for fl in s["filings"]["files"]:
        if fl["filingTo"] >= "2020-01-01":
            pages.append(json.loads(get("https://data.sec.gov/submissions/" + fl["name"])))
    for r in pages:
        for form, acc, filed, doc in zip(r["form"], r["accessionNumber"], r["filingDate"], r["primaryDocument"]):
            if form in ("10-Q", "10-K") and filed >= "2020-01-01":
                yield form, acc, filed, doc


def main():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    rows = {}
    for form, acc, filed, doc in sorted(set(filings())):
        url = f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{acc.replace('-', '')}/{doc}"
        h = get(url, os.path.join(RAW, doc))
        got = facts_in(h, contexts(h))
        for tag, by_end in got.items():
            for end, val in by_end.items():
                rows.setdefault(tag, []).append({"end": end, "val": val, "accn": acc, "form": form, "filed": filed, "src": doc})
        print(f"{form} {filed} {doc}: " + ", ".join(f"{t} {len(v)}" for t, v in sorted(got.items())))
    overlay = json.load(open(OUT)) if os.path.exists(OUT) else {}
    overlay.setdefault("us-gaap", {}).update(rows)
    json.dump(overlay, open(OUT, "w"), indent=1)
    print(f"저장: {OUT} ({sum(len(v) for v in rows.values())}행)")


if __name__ == "__main__":
    main()
