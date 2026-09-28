#!/usr/bin/env python3
"""Visa(V) — 클래스 A 기준 희석 EPS와 "환산 클래스 A" 주식 수를 공시 인라인 XBRL에서 꺼낸다(2026-09-27).

Visa는 EPS·주식 수를 클래스(A·B-1·B-2·B-3·C)별 차원으로만 낸다. companyfacts는 차원 값을 싣지 않아
EarningsPerShareDiluted가 없고(companyconcept 404), 시점 주식 수는 2010년 값(4.7억 주)만 남아
PSR이 4배로 나왔다(실제 약 16배). 시가총액 주식 수는 분기말 환산 총수(v:SharesOutstandingAsConvertedBasis,
클래스 A·B·C·우선주를 A로 환산한 합계, Q3 FY26 18.80억 주)를 쓴다. 클래스 A 희석 EPS는 순이익 ÷ 희석 가중평균
환산 주식 수다(Q3 FY26 $5,628M ÷ 1,898M주 = $2.97).
클래스별 표지 주식 수를 그냥 더하면 B·C의 전환 비율이 달라 틀린다(META 방식은 쓰지 않는다).

- EPS: EarningsPerShareDiluted(StatementClassOfStockAxis = CommonClassAMember), 3개월·누적·연간 행.
- 주식 수: 분기말 환산 총수 v:SharesOutstandingAsConvertedBasis(차원 없음, 클래스 A·B·C·우선주 환산 합계)를 쓴다.
  그 태그가 없는 공시만 클래스 A 희석 가중평균의 3개월 값(4분기는 (12 × 연간 − 9 × 3분기 누적) ÷ 3)으로 채운다.
- 결과: `v2/.sec_cache/overlay/0001403161.json`(us-gaap EarningsPerShareDiluted, dei EntityCommonStockSharesOutstanding).

    python3 v2/adapters/visa_classA.py        # 오버레이 생성
    python3 v2/adapters/visa_classA.py eps    # → scripts/V_eps_history.json (fetch_eps_history를 오버레이로 먹임)
"""
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
sys.path.insert(0, HERE)
sys.path.insert(0, V2)
from cover_shares import get  # noqa: E402

CIK = "0001403161"
SINCE = "2019-06-01"
RAW = os.path.join(V2, ".sec_cache", "v_filings")
OUT = os.path.join(V2, ".sec_cache", "overlay", f"{CIK}.json")
CLASS_A = "us-gaap:CommonClassAMember"


def facts_in(h):
    ctx = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        b = m.group(2)
        s, e = re.search(r"<xbrli:startDate>([^<]+)<", b), re.search(r"<xbrli:endDate>([^<]+)<", b)
        mems = re.findall(r'dimension="([^"]+)">([^<]+)<', b)
        if s and e and mems == [("us-gaap:StatementClassOfStockAxis", CLASS_A)]:
            ctx[m.group(1)] = (s.group(1), e.group(1))
    # 분기말 환산 주식 수(차원 없는 v:SharesOutstandingAsConvertedBasis — 클래스 A·B·C·우선주 환산 합계)
    inst = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        b = m.group(2)
        i = re.search(r"<xbrli:instant>([^<]+)<", b)
        if i and "<xbrldi:" not in b:
            inst[m.group(1)] = i.group(1)
    out = {"eps": {}, "wsh": {}, "conv": {}}
    for m in re.finditer(r'<ix:nonFraction([^>]*name="v:SharesOutstandingAsConvertedBasis"[^>]*)>(.*?)</ix:nonFraction>', h, re.S):
        attrs, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
        c = re.search(r'contextRef="([^"]+)"', attrs).group(1)
        if c in inst and re.match(r"^[\d,.]+$", txt):
            sc = re.search(r'scale="(-?\d+)"', attrs)
            out["conv"][inst[c]] = float(txt.replace(",", "")) * 10 ** (int(sc.group(1)) if sc else 0)
    for key, name in (("eps", "us-gaap:EarningsPerShareDiluted"), ("wsh", "us-gaap:WeightedAverageNumberOfDilutedSharesOutstanding")):
        for m in re.finditer(r'<ix:nonFraction([^>]*name="%s"[^>]*)>(.*?)</ix:nonFraction>' % re.escape(name), h, re.S):
            attrs, txt = m.group(1), re.sub(r"<[^>]+>", "", m.group(2)).strip()
            c = re.search(r'contextRef="([^"]+)"', attrs).group(1)
            if c not in ctx or not re.match(r"^[\d,.]+$", txt):
                continue
            sc = re.search(r'scale="(-?\d+)"', attrs)
            v = float(txt.replace(",", "")) * 10 ** (int(sc.group(1)) if sc else 0)
            if 'sign="-"' in attrs:
                v = -v
            out[key][ctx[c]] = v
    return out


def days(s, e):
    return (date.fromisoformat(e) - date.fromisoformat(s)).days


def build():
    import subprocess
    os.makedirs(RAW, exist_ok=True)
    subj = json.loads(get(f"https://data.sec.gov/submissions/CIK{CIK}.json"))["filings"]
    pages = [subj["recent"]] + [json.loads(get(f"https://data.sec.gov/submissions/{f['name']}"))
                                for f in subj.get("files", []) if f.get("filingTo", "9999") >= SINCE]
    listing = sorted({x for sub in pages for x in zip(sub["form"], sub["accessionNumber"], sub["filingDate"], sub["primaryDocument"])},
                     key=lambda x: x[2])
    eps_rows, wq = [], {}          # wq: (start, end) → (val, filed, accn, form)
    conv = {}                       # 분기말 → (환산 주식 수, filed, accn, form) — 그 분기 공시가 처음 낸 값
    y9 = {}                         # 9개월 누적 가중평균 (start, end) → val
    fyw = []                        # 연간 가중평균
    for form, acc, filed, doc in listing:
        if form not in ("10-Q", "10-K") or filed < SINCE:
            continue
        url = f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{acc.replace('-', '')}/{doc}"
        f = facts_in(get(url, os.path.join(RAW, doc)))
        if not f["eps"]:
            print("  ⚠ 클래스 A EPS 없음:", form, filed, doc)
            continue
        cur_end = max(e for _, e in f["eps"])
        if cur_end in f["conv"] and cur_end not in conv:
            conv[cur_end] = (f["conv"][cur_end], filed, acc, form)
        for (s, e), v in f["eps"].items():
            n = days(s, e)
            fp = "FY" if n > 350 else ("Q" if n < 100 else "YTD")
            eps_rows.append({"start": s, "end": e, "val": v, "accn": acc, "form": form, "fp": fp,
                             "filed": filed, "unit": "USD/shares"})
        for (s, e), v in f["wsh"].items():
            if e != cur_end:
                continue
            n = days(s, e)
            if n < 100:
                wq[(s, e)] = (v, filed, acc, form)
            elif 250 < n < 290:
                y9[(s, e)] = v
            elif n > 350:
                fyw.append((s, e, v, filed, acc, form))
        print(form, filed, cur_end, "EPS", {k[0][5:] + "~" + k[1][5:]: v for k, v in f["eps"].items() if k[1] == cur_end},
              "주식", {k[0][5:]: round(v / 1e6) for k, v in f["wsh"].items() if k[1] == cur_end})
    sh_rows = [{"end": e, "val": v, "filed": fl, "form": fm, "accn": a, "unit": "shares", "basis": "클래스 A 희석 가중평균(환산)"}
               for (s, e), (v, fl, a, fm) in wq.items()]
    for s, e, v, fl, a, fm in fyw:
        q3 = [x for (ss, ee), x in y9.items() if ss == s]
        if q3:
            sh_rows.append({"end": e, "val": (12 * v - 9 * q3[0]) / 3, "filed": fl, "form": fm, "accn": a, "unit": "shares",
                            "basis": "4분기 = (12×연간 − 9×3분기 누적) ÷ 3"})
    # 분기말 환산 총수가 있는 분기는 그 값을 쓴다(가중평균보다 시점에 맞다 — Q3 FY26 18.80억 vs 가중 18.98억, Codex)
    by_end = {r["end"]: r for r in sh_rows}
    for e, (v, fl, a, fm) in conv.items():
        by_end[e] = {"end": e, "val": v, "filed": fl, "form": fm, "accn": a, "unit": "shares", "basis": "분기말 환산 총수(v:SharesOutstandingAsConvertedBasis)"}
    sh_rows = sorted(by_end.values(), key=lambda r: r["end"])
    data = json.load(open(OUT)) if os.path.exists(OUT) else {}
    data.setdefault("us-gaap", {})["EarningsPerShareDiluted"] = eps_rows
    data.setdefault("dei", {})["EntityCommonStockSharesOutstanding"] = sh_rows
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(data, open(OUT, "w"), indent=1)
    print(f"저장: {OUT} — EPS {len(eps_rows)}행, 주식 수 {len(sh_rows)}행")


def run_eps():
    sys.path.insert(0, os.path.join(REPO, "scripts"))
    import fetch_eps_history as feh
    import build_multiple_history as bmh
    rows = [r for r in bmh.concept(CIK, "EarningsPerShareDiluted")]
    feh.curl_json = lambda url: {"units": {"USD/shares": rows}}
    sys.argv = ["fetch_eps_history.py", "V", "--cik", CIK, "--out", os.path.join(REPO, "scripts", "V_eps_history.json")]
    feh.main()


if __name__ == "__main__":
    run_eps() if sys.argv[1:] == ["eps"] else build()
