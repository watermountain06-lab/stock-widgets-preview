#!/usr/bin/env python3
"""다중 클래스 종목의 표지 주식 수 이력 — 10-Q/10-K 표지의 클래스별 값을 합산한다.

META는 표지의 dei:EntityCommonStockSharesOutstanding을 Class A·B 차원으로만 낸다.
companyfacts는 차원이 붙은 값을 싣지 않으므로 META의 시점 주식 수가 통째로 빠져
시가총액 기반 배수(PSR·PBR·PCR·EV/EBITDA)가 "계산 불가"였다(2026-09-25).
사이트 파이프라인(site_data/stocks.json "sec-cover · sum-of-classes")과 같은 방식으로,
공시마다 표지 클래스 값을 더해 dei:EntityCommonStockSharesOutstanding 행 모양으로
`v2/.sec_cache/overlay/{cik}.json`에 쓴다(기존 오버레이 내용은 보존).

    python3 v2/adapters/cover_shares.py META
"""
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(V2), "scripts"))
import fetch_eps_history as feh  # noqa: E402

UA = "kim research gptjhss@gmail.com"
SINCE = "2019-01-01"


def get(url, path=None):
    if path and os.path.exists(path):
        return open(path, encoding="utf-8", errors="ignore").read()
    txt = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, text=True).stdout
    time.sleep(0.2)
    if path:
        open(path, "w").write(txt)
    return txt


def cover_classes(h):
    """표지 주식 수: 맥락 id → (시점, 클래스 멤버). 클래스 차원이 없는 단일 값도 받는다."""
    ctx = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        body = m.group(2)
        inst = re.search(r"<xbrli:instant>([^<]+)<", body)
        mem = re.search(r'dimension="us-gaap:StatementClassOfStockAxis">([^<]+)<', body)
        other = len(re.findall(r"<xbrldi:explicitMember", body)) - (1 if mem else 0)
        if inst and other == 0:
            ctx[m.group(1)] = (inst.group(1), mem.group(1) if mem else None)
    got = {}
    for m in re.finditer(r'<ix:nonFraction([^>]*name="dei:EntityCommonStockSharesOutstanding"[^>]*)>(.*?)</ix:nonFraction>', h, re.S):
        attrs, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2))
        c = re.search(r'contextRef="([^"]+)"', attrs).group(1)
        if c not in ctx:
            continue
        scale = int(re.search(r'scale="(-?\d+)"', attrs).group(1)) if 'scale="' in attrs else 0
        got[ctx[c]] = float(txt.replace(",", "") or 0) * 10 ** scale
    return got


def main(ticker):
    cik = feh.CIKS[ticker]
    raw = os.path.join(V2, ".sec_cache", f"{ticker.lower()}_filings")
    out = os.path.join(V2, ".sec_cache", "overlay", f"{cik}.json")
    os.makedirs(raw, exist_ok=True)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subj = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik}.json"))["filings"]
    # "recent"는 최근 1,000건뿐이다 — META는 임원 지분 공시(Form 4)가 많아 2024년 이전 10-Q가 빠진다
    pages = [subj["recent"]] + [json.loads(get(f"https://data.sec.gov/submissions/{f['name']}"))
                                for f in subj.get("files", []) if f.get("filingTo", "9999") >= SINCE]
    listing = [x for sub in pages for x in zip(sub["form"], sub["accessionNumber"], sub["filingDate"], sub["primaryDocument"])]
    rows = []
    for form, acc, filed, doc in sorted(set(listing), key=lambda x: x[2], reverse=True):
        if form not in ("10-Q", "10-K") or filed < SINCE:
            continue
        url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}"
        got = cover_classes(get(url, os.path.join(raw, doc)))
        by_day = {}
        for (day, cls), v in got.items():
            by_day.setdefault(day, {})[cls] = v
        if not by_day:
            print(f"  ⚠ {form} {filed} {doc}: 표지 주식 수 없음")
            continue
        day = max(by_day)
        parts = by_day[day]
        if None in parts and len(parts) > 1:      # 합계와 클래스별이 함께 있으면 합계만
            parts = {None: parts[None]}
        rows.append({"end": day, "val": sum(parts.values()), "filed": filed, "form": form, "accn": acc,
                     "unit": "shares", "classes": {str(k): v for k, v in parts.items()}})
        print(f"{form} {filed}: {day} {sum(parts.values()) / 1e9:.4f}B {sorted(str(k) for k in parts)}")
    data = json.load(open(out)) if os.path.exists(out) else {}
    data.setdefault("dei", {})["EntityCommonStockSharesOutstanding"] = rows
    json.dump(data, open(out, "w"), indent=1)
    print(f"저장: {out} ({len(rows)}행)")


if __name__ == "__main__":
    main(sys.argv[1])
