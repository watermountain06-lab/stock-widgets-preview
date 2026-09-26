#!/usr/bin/env python3
"""버크셔 해서웨이 10-Q/10-K 인라인 XBRL 사실 저장소 (research/brkb_two_pillar_prereg.md 4판).

companyfacts에는 회사 자체 태그(brka:)와 차원(보험·기타/철도·에너지 열, 보험 하위 그룹, 클래스별
주식 수)이 붙은 사실이 없어서, 공시 원문에서 직접 읽는다. 원문은 v2/.sec_cache/brk_filings/에 캐시.

    from adapters.brkb_facts import load_facts
    facts = load_facts()   # [{name, start, end, dims, val, filed, form, doc}, ...]
"""
import datetime as dt
import json
import os
import re
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
CIK = "0001067983"
UA = "kim research gptjhss@gmail.com"
RAW = os.path.join(V2, ".sec_cache", "brk_filings")
STORE = os.path.join(V2, ".sec_cache", "brk_facts.json")
# 정정·이전 발표치 사실은 버린다(4판 1-4)
BAD_MEMBERS = ("RevisionOfPriorPeriod", "ScenarioPreviouslyReported", "RestatementAdjustment", "PreviouslyReported")


def _get(url, path=None):
    if path and os.path.exists(path):
        return open(path, encoding="utf-8", errors="ignore").read()
    txt = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, text=True).stdout
    time.sleep(0.2)
    if path:
        open(path, "w").write(txt)
    return txt


def filings(since="2019-01-01"):
    sub = json.loads(_get(f"https://data.sec.gov/submissions/CIK{CIK}.json"))["filings"]
    pages = [sub["recent"]] + [json.loads(_get(f"https://data.sec.gov/submissions/{f['name']}")) for f in sub.get("files", [])]
    rows = {x for p in pages for x in zip(p["form"], p["accessionNumber"], p["filingDate"], p["primaryDocument"], p["reportDate"])
            if x[0] in ("10-Q", "10-K") and x[2] >= since}
    return sorted(rows, key=lambda x: x[2])


def _num(txt, attrs):
    t = re.sub(r"<[^>]+>", "", txt).strip().replace(",", "")
    if t in ("", "-", "—", "–"):
        return 0.0
    if 'format="ixt:fixed-zero"' in attrs or 'ixt:zerodash' in attrs:
        return 0.0
    try:
        v = float(t)
    except ValueError:
        return None
    sc = re.search(r'scale="(-?\d+)"', attrs)
    v *= 10 ** int(sc.group(1)) if sc else 1
    return -v if 'sign="-"' in attrs else v


def parse(h, meta):
    ctx = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        body = m.group(2)
        dims = tuple(sorted(v.split(":")[-1] for v in re.findall(r'dimension="[^"]+">([^<]+)<', body)))
        s = re.search(r"<xbrli:startDate>([^<]+)<", body)
        e = re.search(r"<xbrli:endDate>([^<]+)<", body)
        i = re.search(r"<xbrli:instant>([^<]+)<", body)
        ctx[m.group(1)] = (s.group(1) if s else None, (e or i).group(1) if (e or i) else None, dims)
    out = []
    for m in re.finditer(r"<ix:nonFraction([^>]*)>(.*?)</ix:nonFraction>", h, re.S):
        attrs = m.group(1)
        name = re.search(r'name="([^"]+)"', attrs).group(1).split(":")[-1]
        c = re.search(r'contextRef="([^"]+)"', attrs).group(1)
        if c not in ctx:
            continue
        start, end, dims = ctx[c]
        if any(b in d for d in dims for b in BAD_MEMBERS):
            continue
        v = _num(m.group(2), attrs)
        if v is None:
            continue
        out.append({"name": name, "start": start, "end": end, "dims": list(dims), "val": v} | meta)
    return out


def load_facts(refresh=False):
    if os.path.exists(STORE) and not refresh:
        return json.load(open(STORE))
    os.makedirs(RAW, exist_ok=True)
    facts = []
    for form, acc, filed, doc, rep in filings():
        h = _get(f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{acc.replace('-', '')}/{doc}", os.path.join(RAW, doc))
        if "<ix:nonFraction" not in h:
            continue   # 2019-Q1 이전은 인라인 XBRL이 아니다
        facts += parse(h, {"filed": filed, "form": form, "doc": doc, "report": rep})
    json.dump(facts, open(STORE, "w"))
    return facts


if __name__ == "__main__":
    f = load_facts(refresh=True)
    print(len(f), "facts", len({x["doc"] for x in f}), "filings")
