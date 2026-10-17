#!/usr/bin/env python3
"""은행 사전 등록 7판 초안(11-2·11-3·11-7, 2026-10-11) — companyfacts에 없는 값을 10-Q·10-K 원문 인라인 XBRL에서 분기별로 모은다.

companyfacts(SEC 요약 자료)에는 표준 태그만 있다. 우선주 장부금액을 회사 고유 태그로 적는 은행(BAC 10-Q),
무형자산을 회사 고유 태그로 적거나 아예 표시하지 않는 은행(WFC·PNC·JPM 10-Q), CET1 비율 태그는 원문을 봐야 한다.
값마다 그 공시의 접수번호·접수일을 붙여 가용일 규칙(11-0)을 지킨다. 결과는 커밋하는 파일이라 Actions 캐시와 상관없이 이어진다.

    python3 v2/adapters/bank_sec_values.py            # 카드 9곳 + 동종업 13곳, 없는 분기만 더한다
    python3 v2/adapters/bank_sec_values.py BAC WFC

결과: v2/research/bank_sec_values.json
  {T: {분기말: {"form", "accn", "filed", "pref", "pref_tag", "ia", "ia_tag", "cet1", "cet1_tag"}}}
  pref·ia·cet1이 None이면 그 공시 원문에 없다는 뜻(0이 아니다). 받기·읽기에 실패한 분기는 적지 않는다(다음 실행에서 다시).
"""
import html as htmlmod
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
OUT = os.path.join(V2, "research", "bank_sec_values.json")
TAGS = os.path.join(V2, "research", "bank_sec_tags.json")
CACHE = os.path.join(V2, ".sec_cache", "ixbrl_bank")
UA = "kim research gptjhss@gmail.com"
SINCE = "2020-06-30"   # 5년 자기 이력 + 출발 TTM·기초 자본
CARDS = {"JPM": "0000019617", "BAC": "0000070858", "WFC": "0000072971", "GS": "0000886982", "MS": "0000895421",
         "C": "0000831001", "AXP": "0000004962", "SCHW": "0000316709", "COF": "0000927628", "BNY": "0001390777"}
IA_STD = ["us-gaap:IntangibleAssetsNetExcludingGoodwill", "us-gaap:FiniteLivedIntangibleAssetsNet",
          "us-gaap:IndefiniteLivedIntangibleAssetsExcludingGoodwill", "us-gaap:OtherIntangibleAssetsNet"]
IA_CUSTOM = re.compile(r"^(?!us-gaap:)\w+:\w*Intangible\w*$", re.I)
IA_SKIP = re.compile(r"MortgageServicing|IncludingGoodwill|Gross|Accumulated|Amortization|Impairment|Acquired|Addition|DeferredTax|Useful|Goodwill(?!$)|AndGoodwill|Translation", re.I)


def _get(url, raw=False):
    for k in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            b = urllib.request.urlopen(req, timeout=90).read()
            time.sleep(0.12)
            return b if raw else b.decode("utf-8", "ignore")
        except Exception:
            if k == 3:
                raise
            time.sleep(2 + 3 * k)


def filings(cik):
    """10-Q·10-K(정정 제외) [(분기말, 접수일, 접수번호, 주 문서)] — 최근 목록과 옛 목록 페이지 모두."""
    sub = json.loads(_get(f"https://data.sec.gov/submissions/CIK{cik}.json"))["filings"]
    pages = [sub["recent"]] + [json.loads(_get(f"https://data.sec.gov/submissions/{f['name']}")) for f in sub.get("files", [])
                                if f.get("filingTo", "9999") >= SINCE]
    out = {}
    for p in pages:
        for i, form in enumerate(p["form"]):
            rd = p["reportDate"][i]
            if form in ("10-Q", "10-K") and rd and rd >= SINCE and rd[5:] in ("03-31", "06-30", "09-30", "12-31"):
                key = rd
                cand = (rd, p["filingDate"][i], p["accessionNumber"][i], p["primaryDocument"][i], form)
                if key not in out or cand[1] < out[key][1]:   # 가장 먼저 접수된 원 공시
                    out[key] = cand
    return [out[k] for k in sorted(out)]


def _parse(h):
    ctx = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        body = m.group(2)
        dims = tuple(sorted(re.findall(r'<xbrldi:explicitMember dimension="([^"]+)">\s*([^<\s]+)\s*</xbrldi:explicitMember>', body)))
        s = re.search(r"<xbrli:startDate>([^<]+)", body)
        e = re.search(r"<xbrli:endDate>([^<]+)", body) or re.search(r"<xbrli:instant>([^<]+)", body)
        ctx[m.group(1)] = (s.group(1) if s else None, e.group(1) if e else None, dims)
    out = []
    for m in re.finditer(r"<ix:nonFraction([^>]*)>(.*?)</ix:nonFraction>", h, re.S):
        a = m.group(1)
        if 'xsi:nil="true"' in a:
            continue
        name = re.search(r'name="([^"]+)"', a).group(1)
        c = ctx.get(re.search(r'contextRef="([^"]+)"', a).group(1))
        if not c:
            continue
        txt = htmlmod.unescape(re.sub(r"<[^>]+>", "", m.group(2))).replace(",", "").strip()
        fmt = re.search(r'format="([^"]+)"', a)
        if fmt and ("zerodash" in fmt.group(1) or "fixed-zero" in fmt.group(1)):
            v = 0.0
        else:
            try:
                v = float(txt)
            except ValueError:
                continue
        sc = re.search(r'scale="(-?\d+)"', a)
        v *= 10 ** int(sc.group(1) if sc else 0)
        if 'sign="-"' in a:
            v = -v
        out.append((name, c[0], c[1], c[2], v))
    return out


def _parse_instance(x):
    """XBRL 인스턴스(EDGAR가 인라인 원문에서 뽑아 둔 {문서}_htm.xml) — 사실이 한 파일에 다 있다(여러 문서로 나뉜 10-K도)."""
    ctx = {}
    for m in re.finditer(r'<(?:xbrli:)?context id="([^"]+)">(.*?)</(?:xbrli:)?context>', x, re.S):
        body = m.group(2)
        dims = tuple(sorted(re.findall(r'<xbrldi:explicitMember dimension="([^"]+)">\s*([^<\s]+)\s*</xbrldi:explicitMember>', body)))
        if "typedMember" in body:
            dims += (("typed", "typed"),)
        s_ = re.search(r"<(?:xbrli:)?startDate>([^<]+)", body)
        e_ = re.search(r"<(?:xbrli:)?endDate>([^<]+)", body) or re.search(r"<(?:xbrli:)?instant>([^<]+)", body)
        ctx[m.group(1)] = (s_.group(1).strip() if s_ else None, e_.group(1).strip() if e_ else None, dims)
    out = []
    for m in re.finditer(r'<([A-Za-z][\w-]*:[A-Za-z]\w*)\s([^>]*contextRef="([^"]+)"[^>]*)>([^<]*)</\1>', x):
        name, attrs, cref, txt = m.groups()
        if "unitRef=" not in attrs or cref not in ctx:
            continue
        try:
            v = float(txt.strip())
        except ValueError:
            continue
        c = ctx[cref]
        out.append((name, c[0], c[1], c[2], v))
    return out


def facts(cik, accn, primary, end):
    """그 공시의 XBRL 사실(인스턴스 파일). 접수번호마다 한 번 받아 둔다."""
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, f"{accn}.json")
    if os.path.exists(p):
        return [tuple(x[:3]) + (tuple(tuple(d) for d in x[3]), x[4]) for x in json.load(open(p))]
    base = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accn.replace('-', '')}/"
    names = [x["name"] for x in json.loads(_get(base + "index.json"))["directory"]["item"]]
    inst = [n for n in names if n.endswith("_htm.xml")] or [n for n in names if re.search(r"\d{8}\.xml$", n) and not re.search(r"_(cal|def|lab|pre)\.xml$", n)]
    if not inst:
        raise ValueError(f"{accn}: XBRL 인스턴스 파일이 없다")
    fs = _parse_instance(_get(base + inst[0]))
    if not any(n == "us-gaap:StockholdersEquity" and e == end and not s and not d for n, s, e, d, v in fs):
        raise ValueError(f"{accn}: {end} 자본이 인스턴스에 없다")
    json.dump(fs, open(p, "w"))
    return fs


def pick(fs, end, names):
    for n in names:   # 태그 이름 대소문자가 해마다 다르다(BAC RedeemableandNonRedeemable → RedeemableAndNonRedeemable)
        v = [x for nm, s, e, d, x in fs if nm.lower() == n.lower() and e == end and not s and not d]
        if v:
            return v[0], n
    return None, None


def values(T, cik, fs, end, tags):
    pt = tags["preferred"].get(T, {})
    pref, ptag = (None, None) if pt.get("path") or not pt.get("tags") else pick(fs, end, pt["tags"])
    ia, itag = pick(fs, end, IA_STD[:1])
    if ia is None:   # 유한 + 비한정을 함께 적은 은행은 둘을 더한다(1-2와 같다 — 첫 태그만 쓰면 비한정만큼 TCE가 커진다, Codex 2차)
        f_, _ = pick(fs, end, ["us-gaap:FiniteLivedIntangibleAssetsNet"])
        i_, _ = pick(fs, end, ["us-gaap:IndefiniteLivedIntangibleAssetsExcludingGoodwill"])
        ia, itag = ((f_ or 0) + (i_ or 0), "Finite+Indefinite") if (f_ is not None or i_ is not None) else pick(fs, end, IA_STD[3:])
    if ia is None:   # 11-3: 회사 고유 무형자산 태그(MSR·영업권 포함 이름 제외)
        cust = sorted({n for n, s, e, d, x in fs if e == end and not s and not d and IA_CUSTOM.match(n) and not IA_SKIP.search(n)})
        ia, itag = pick(fs, end, cust) if cust else (None, None)
    ct = tags["cet1"].get(T, tags["cet1"]["_default"])["tag"]
    cet1, ctag = pick(fs, end, [ct, "us-gaap:CommonEquityTierOneCapitalRatio"])
    if cet1 is None:   # 표준방식(Standardized) 값 — 지주회사(연결·모회사) 것만, 은행 자회사 값은 뺀다(WFC 2026-06 10.26%, 자회사 12.07%)
        v = [x for nm, s, e, d, x in fs if nm.lower() in (ct.lower(), "us-gaap:commonequitytieronecapitalratio") and e == end and not s and d
             and any(re.search(r"Standardized", m_, re.I) for _, m_ in d)
             and all(re.search(r"Standardized|ParentCompany|Consolidated", m_, re.I) for _, m_ in d)]
        cet1, ctag = (v[0], ct + " (Standardized)") if len(set(v)) == 1 else (None, None)
    iss, _ = pick(fs, end, ["us-gaap:CommonStockSharesIssued"])
    tr, _ = pick(fs, end, ["us-gaap:TreasuryStockCommonShares", "us-gaap:TreasuryStockShares", "wfc:TreasuryStockCommonAndPreferredShares"])   # WFC는 회사 고유 태그(보통주·우선주 합 — 우선주 자기주식은 없다고 보고 대조로 확인)
    so, _ = pick(fs, end, ["us-gaap:CommonStockSharesOutstanding"])
    sh = iss - tr if iss and tr and iss > tr else so   # 1-6과 같은 순서(발행 − 자기주식, 없으면 유통) — companyfacts에 늦게 들어온 분기(WFC 2023~2024)용
    se, _ = pick(fs, end, ["us-gaap:StockholdersEquity"])
    gw, _ = pick(fs, end, ["us-gaap:Goodwill"])
    return {"pref": pref, "pref_tag": ptag, "ia": ia, "ia_tag": itag, "cet1": cet1, "cet1_tag": ctag, "shares": sh, "se": se, "gw": gw}


def peers():
    sys.path.insert(0, HERE)
    sys.path.insert(0, V2)
    import bank_card as bc
    return {r["ticker"]: str(r["cik"]).zfill(10) for r in bc.su.sp500_rows() if r.get("subIndustry") in bc.SUBS}


def main():
    want = [a.upper() for a in sys.argv[1:] if not a.startswith("--")]
    banks = {**peers(), **CARDS}
    if want:
        banks = {t: banks[t] for t in want}
    tags = json.load(open(TAGS))
    data = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for T, cik in sorted(banks.items()):
        have = data.setdefault(T, {})
        try:
            fl = filings(cik)
        except Exception as e:
            print(f"{T}: 목록 실패 {type(e).__name__}")
            continue
        added = 0
        for end, filed, accn, primary, form in fl:
            if end in have and have[end].get("accn") == accn:
                continue
            try:
                fs = facts(cik, accn, primary, end)
            except Exception as e:
                print(f"  {T} {end}: 받기 실패 {type(e).__name__}")
                continue
            have[end] = {"form": form, "accn": accn, "filed": filed, **values(T, cik, fs, end, tags)}
            added += 1
        print(f"{T}: 분기 {len(have)}개(새로 {added})", flush=True)
        json.dump(data, open(OUT, "w"), ensure_ascii=False, indent=0, sort_keys=True)


if __name__ == "__main__":
    main()
