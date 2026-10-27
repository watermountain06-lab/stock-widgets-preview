#!/usr/bin/env python3
"""companyfacts에 아직 안 들어온 최신 10-Q/10-K를 원문 인라인 XBRL에서 보충한다(2026-09-27, V).

SEC companyfacts는 가끔 최근 공시를 몇 달씩 싣지 않는다(JPM 카드의 C: 2026 10-Q 없음, V: 2026-07-29 10-Q 없음).
그 공시의 원문(인라인 XBRL)에서 **차원 없는** us-gaap·dei 수치만 꺼내 companyfacts 행 모양
({start?, end, val, accn, fy?, fp, form, filed})으로 `v2/.sec_cache/overlay/{cik}.json`에 더한다.
기존 오버레이의 다른 태그·행은 보존하고, 같은 (start, end, filed) 행은 다시 쓰지 않는다.

    python3 v2/adapters/ixbrl_supplement.py 0001403161
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cover_shares import get  # noqa: E402

CACHE = os.path.join(V2, ".sec_cache")


def facts_cache(cik):
    """companyfacts 캐시를 읽는다 — 없으면 받아서 저장한다. Actions의 SEC 캐시는 토요일에만 저장되므로 주중에 새로 만든 카드는
    캐시에 없고, 읽기만 하던 이 단계가 FileNotFoundError로 멈췄다(2026-10-26 매일 실행에서 CDNS 실패 — 10-25 추가된 카드)."""
    p = os.path.join(CACHE, f"{cik}_facts.json")
    if os.path.exists(p):
        try:
            return json.load(open(p))
        except ValueError:   # 토요일 캐시 저장이 중간에 끊겨 잘린 파일 — 없는 것으로 보고 받는다(Fable)
            pass
    try:
        d = json.loads(get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json") or "{}")
    except ValueError:   # 오류 쪽지(HTML·빈 응답)를 캐시에 쓰지 않는다
        d = {}
    if not isinstance(d, dict) or not isinstance(d.get("facts"), dict):   # null·오류 쪽지도 같은 문장으로(Codex)
        sys.exit(f"{cik}: companyfacts를 받지 못했고 캐시에도 없다 — 보충을 할 수 없다")
    os.makedirs(CACHE, exist_ok=True)
    tmp = p + ".part"   # 중간에 끊겨 반쪽 파일이 남으면 다음 실행이 받지 않고 그 파일로 멈춘다(Codex)
    json.dump(d, open(tmp, "w"))
    os.replace(tmp, p)
    return d


def parse(h, prefixes=("us-gaap:", "dei:")):
    ctx = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        b = m.group(2)
        if "<xbrldi:explicitMember" in b or "<xbrldi:typedMember" in b:
            continue
        s, e, i = (re.search(rf"<xbrli:{k}>([^<]+)<", b) for k in ("startDate", "endDate", "instant"))
        ctx[m.group(1)] = (s.group(1), e.group(1)) if s and e else (None, i.group(1)) if i else None
    unit = {m.group(1): m.group(2) for m in re.finditer(r'<xbrli:unit id="([^"]+)">(.*?)</xbrli:unit>', h, re.S)}
    out = []
    for m in re.finditer(r'<ix:nonFraction([^>]*)>(.*?)</ix:nonFraction>', h, re.S):
        a = m.group(1)
        name = re.search(r'name="([^"]+)"', a).group(1)
        if not name.startswith(prefixes):
            continue
        c = ctx.get(re.search(r'contextRef="([^"]+)"', a).group(1))
        txt = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if c and "fixed-zero" in a:
            txt = "0"                                   # ixt:fixed-zero("—")는 0이다(Codex)
        if not c or not re.match(r"^[\d,.]+$", txt):
            continue
        sc = re.search(r'scale="(-?\d+)"', a)
        v = float(txt.replace(",", "")) * 10 ** (int(sc.group(1)) if sc else 0)
        if 'sign="-"' in a:
            v = -v
        ub = unit.get((re.search(r'unitRef="([^"]+)"', a) or [None, ""])[1], "")
        u = "USD/shares" if "shares" in ub and "USD" in ub else "shares" if "shares" in ub else "USD" if "USD" in ub else "pure"
        out.append((name, c[0], c[1], v, u))
    return out


def main(cik):
    cik = cik.zfill(10)
    facts = facts_cache(cik)
    have = {r["filed"] for t in facts["facts"].get("us-gaap", {}).values() for rows in t["units"].values() for r in rows}
    last = max(have)
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik}.json"))["filings"]["recent"]
    op = os.path.join(CACHE, "overlay", f"{cik}.json")
    data = json.load(open(op)) if os.path.exists(op) else {}
    raw = os.path.join(CACHE, f"ix_{cik}")
    os.makedirs(raw, exist_ok=True)
    added = 0
    for form, acc, filed, doc in zip(sub["form"], sub["accessionNumber"], sub["filingDate"], sub["primaryDocument"]):
        # 공시별로 본다 — companyfacts가 더 새 공시는 싣고 그 앞 공시를 빠뜨리면(SEC가 가끔 그런다) 마지막 날짜로 재면 그 앞
        # 공시를 건너뛰어 보충이 비고, _facts가 "승인한 공시가 SEC 자료에 없다"로 멈춘다. 2026-10-24~26 12개사 실측으로
        # 더 받게 되는 공시는 0건이었다(Fable)
        if form not in ("10-Q", "10-K") or filed in have:
            continue
        h = get(f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}", os.path.join(raw, doc))
        fp = "FY" if form == "10-K" else "Q"
        seen = set()
        for name, s, e, v, u in parse(h):
            tax, tag = name.split(":")
            key = (tag, s, e)
            if key in seen:
                continue
            seen.add(key)
            rows = data.setdefault(tax, {}).setdefault(tag, [])
            if any(r.get("start") == s and r["end"] == e and r["filed"] == filed for r in rows):
                continue
            row = {"end": e, "val": v, "accn": acc, "fp": fp, "form": form, "filed": filed, "unit": u, "src": "ixbrl"}
            if s:
                row["start"] = s
            rows.append(row)
            added += 1
        print(f"{form} {filed} {doc}: 보충 {len(seen)}개 사실")
    os.makedirs(os.path.dirname(op), exist_ok=True)
    json.dump(data, open(op, "w"), indent=1)
    print(f"저장: {op} (+{added}행, companyfacts 마지막 공시 {last})")


if __name__ == "__main__":
    main(sys.argv[1])
