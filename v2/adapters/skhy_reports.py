#!/usr/bin/env python3
"""SK하이닉스(SKHY) 원문 보고서 받기 — KRX KIND 공시 뷰어에서 분기·반기보고서와 연결감사보고서 HTML을 받는다.

왜 KIND인가 (2026-09-27)
------------------------
SEC에는 2026-07 상장 뒤의 6-K·424B4뿐이라(companyfacts 사실상 비어 있음) 5년 분기 재무가 없다.
DART 목록 검색은 curl에 응하지 않고(오류 페이지로 넘김), OpenDART는 키가 필요하다.
KIND(한국거래소 공시)는 같은 원문을 싣고, 회사별 공시 목록(POST)과 문서 경로를 curl로 준다.

- 분기·반기보고서: 목록 제목 "분기보고서(일반법인)"·"반기보고서(일반법인)" → 본문 문서
- 연간: 사업보고서는 KIND 목록에 없어, "감사보고서 제출" 공시에 붙은 **연결감사보고서**(감사 완료 연결재무제표)를 쓴다.

    python3 v2/adapters/skhy_reports.py          # manifest 갱신 + 없는 원문 받기
"""
import json
import os
import re
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPORTS = os.path.join(V2, ".sec_cache", "skhy_reports")
MANIFEST = os.path.join(HERE, "skhy_manifest.json")
KIND = "https://kind.krx.co.kr"
UA = "Mozilla/5.0"


def curl(url, data=None, ref=None):
    args = ["curl", "-s", "-A", UA] + (["-e", ref] if ref else []) + (["-X", "POST", "--data", data] if data else []) + [url]
    return subprocess.run(args, capture_output=True, check=True).stdout.decode("utf-8", "ignore")


def disclosures(start="2020-01-01", end=None):
    end = end or time.strftime("%Y-%m-%d")
    rows = []
    for pg in range(1, 60):
        h = curl(f"{KIND}/disclosure/searchdisclosurebycorp.do",
                 f"method=searchDisclosureByCorpSub&forward=searchdisclosurebycorp_sub&currentPageSize=100&pageIndex={pg}"
                 f"&orderMode=1&orderStat=D&repIsuSrtCd=A000660&isurCd=00066&fromDate={start}&toDate={end}",
                 f"{KIND}/disclosure/searchdisclosurebycorp.do")
        got = re.findall(r"<td[^>]*>\s*(\d{4}-\d\d-\d\d \d\d:\d\d)\s*</td>.*?openDisclsViewer\('(\d+)'[^>]*>\s*([^<]+?)\s*<", h, re.S)
        if not got or (rows and got[0] in rows):   # 마지막 쪽을 넘기면 KIND는 마지막 쪽을 되풀이한다
            break
        rows += got
        time.sleep(0.4)
    return rows


def doc_options(acptno):
    h = curl(f"{KIND}/common/disclsviewer.do?method=search&acptno={acptno}")
    return [(v.split("|")[0], t.strip()) for v, t in re.findall(r"<option value='([0-9|YN]+)'[^>]*>([^<]*)", h)]


def doc_path(docno):
    h = curl(f"{KIND}/common/disclsviewer.do?method=searchContents&docNo={docno}")
    m = re.search(r"setPath\('[^']*','([^']+)'", h)
    return m.group(1) if m else None


def refresh():
    man = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else []
    have = {m["acptno"] for m in man}
    for when, acpt, title in disclosures():
        if "기재정정" in title or acpt in have:
            continue
        kind = None
        if re.match(r"(분기|반기)보고서", title):
            kind = "periodic"
        elif title.startswith("감사보고서 제출"):
            kind = "audit"
        if not kind:
            continue
        opts = doc_options(acpt)
        if kind == "periodic":
            doc = opts[0][0] if opts else None
        else:
            doc = next((d for d, t in opts if t.startswith("연결감사보고서")), None)
        url = doc_path(doc) if doc else None
        if not url:
            print("문서 없음:", when, acpt, title)
            continue
        have.add(acpt)
        man.append({"filed": when, "acptno": acpt, "title": title, "kind": kind, "docNo": doc,
                    "url": url.replace("http://", "https://"), "file": f"{acpt}_{doc}.htm"})
        print("추가:", when, title, doc)
        time.sleep(0.4)
    man.sort(key=lambda m: m["filed"])
    json.dump(man, open(MANIFEST, "w"), ensure_ascii=False, indent=1)
    os.makedirs(REPORTS, exist_ok=True)
    for m in man:
        p = os.path.join(REPORTS, m["file"])
        if not os.path.exists(p):
            raw = subprocess.run(["curl", "-s", "-A", UA, m["url"]], capture_output=True, check=True).stdout
            open(p, "wb").write(raw)
            time.sleep(0.4)
    return man


if __name__ == "__main__":
    man = refresh()
    print(len(man), "건")
