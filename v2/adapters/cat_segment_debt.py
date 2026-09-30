#!/usr/bin/env python3
"""CAT 기계·동력 부문 차입금 — 금융 부문(Cat Financial) 빚을 뺀 차입금 시리즈를 공시 원문(인라인 XBRL)에서 뽑는다.

2026-09-30 사용자 결정: 캐터필러 EV·내재가치의 차입금은 기계·동력·에너지(ME&T/MP&E) 부문 빚만 쓴다. 금융 부문
차입금($34.5B, 2026-06-30)은 할부·리스 채권($25.2B)과 묶인 영업 부채이고 그 이자비용은 이미 영업이익 안
("Interest expense of Financial Products")에서 빠지기 때문이다.

재무상태표의 부문별 차입금은 `cat:MachineryPowerEnergyMember`(옛 이름 Machinery·Energy·Transportation) 차원이 붙은 값이라
companyfacts에 없다. 차원이 그 부문 하나뿐인 시점 맥락의 세 태그를 CAT 전용 이름으로 `v2/.sec_cache/overlay/0000018230.json`에 쓴다.

    python3 v2/adapters/cat_segment_debt.py
"""
import html
import json
import os
import re
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
CIK = "0000018230"
UA = "kim research gptjhss@gmail.com"
RAW = os.path.join(V2, ".sec_cache", "cat_filings")
OUT = os.path.join(V2, ".sec_cache", "overlay", f"{CIK}.json")
# 표준 태그 → CAT 전용 이름(부문 차입금). 옛 공시의 유동·비유동 태그도 같은 줄로 받는다.
TAGS = {"us-gaap:ShortTermBorrowings": "CatMETShortTermBorrowings",
        "us-gaap:LongTermDebtAndCapitalLeaseObligationsCurrent": "CatMETLongTermDebtCurrent",
        "us-gaap:LongTermDebtCurrent": "CatMETLongTermDebtCurrent",
        "us-gaap:LongTermDebtAndCapitalLeaseObligations": "CatMETLongTermDebtNoncurrent",
        "us-gaap:LongTermDebtNoncurrent": "CatMETLongTermDebtNoncurrent"}
MEMBER = re.compile(r"cat:Machinery\w*Member")


def get(url, path=None):
    if path and os.path.exists(path):
        return open(path, encoding="utf-8", errors="ignore").read()
    txt = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, text=True).stdout
    time.sleep(0.2)
    if path:
        open(path, "w").write(txt)
    return txt


def contexts(h):
    """차원이 기계·동력 부문 하나뿐인 시점(instant) 맥락 → 결산일."""
    out = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        body = m.group(2)
        dims = re.findall(r"<xbrldi:explicitMember[^>]*>([^<]+)<", body)
        if len(dims) != 1 or not MEMBER.fullmatch(dims[0].strip()):
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
        val = 0.0 if (not txt or "fixed-zero" in attrs or not re.search(r"\d", txt)) else float(txt) * 10 ** scale   # "—"는 0
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
        if form not in ("10-Q", "10-K") or filed < "2020-01-01":
            continue
        url = f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{acc.replace('-', '')}/{doc}"
        h = get(url, os.path.join(RAW, doc))
        got = facts_in(h, contexts(h))
        for tag, by_end in got.items():
            for end, val in by_end.items():
                rows.setdefault(tag, []).append({"end": end, "val": val, "accn": acc, "form": form, "filed": filed, "src": doc})
        print(f"{form} {filed} {doc}: " + ", ".join(f"{t[6:]} {len(v)}" for t, v in sorted(got.items())))
    overlay = json.load(open(OUT)) if os.path.exists(OUT) else {}
    overlay.setdefault("us-gaap", {}).update(rows)
    json.dump(overlay, open(OUT, "w"), indent=1)
    print(f"저장: {OUT} ({sum(len(v) for v in rows.values())}행)")


if __name__ == "__main__":
    main()
