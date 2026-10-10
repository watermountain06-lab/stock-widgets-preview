#!/usr/bin/env python3
"""부문별 매출을 10-Q·10-K 원문 인라인 XBRL에서 꺼낸다 — Claude 없이 매 분기 자동 갱신(설계 D, 2026-10-10).

companyfacts(SEC 요약 자료)에는 차원(부문·제품군)이 붙은 값이 없어, 부문 표는 사람이 분기마다 옮겨 적었다.
여기서는 그 분기 보고서 원문에서 cfg의 SEG_MAP이 가리키는 값을 꺼낸다.

SEG_MAP = {"concepts": ["us-gaap:Revenues", ...],         # 앞의 것부터
           "axis": "us-gaap:StatementBusinessSegmentsAxis",
           "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},   # 함께 붙어야 하는 차원(없으면 {})
           "members": {"pep:PepsiCoBeveragesNorthAmericaMember": ("북미 음료(PBNA)", "#004b93"), ...},
           "ignore": ["us-gaap:ProductMember"],             # 같은 축의 소계 — 쓰지 않는다
           "adjust": ["us-gaap:MembershipMember"],          # 표에는 안 넣고 매출 합 대조에만 더한다(COST 회비 — 예전 SEG_ADJ)
           "alias": {"cost:FoodsAndSundriesMember": "cost:FoodandSundriesMember"},   # 같은 항목의 다른 이름(COST가 10-Q·10-K에서 다르게 붙였다)
           "other": "기타"}                                  # 지도에 없는 멤버를 묶을 이름(없으면 새 멤버가 나오면 멈춘다)

- 분기 값: 그 분기 말에 끝나는 약 1분기(70~125일) 기간. 10-K(4분기)는 연간 − 같은 회계연도 3분기 10-Q의 누계.
- 1년 전 같은 분기: 같은 보고서의 비교 기간(10-K면 전년 연간 − 전년 3분기 누계, 3분기 10-Q의 비교 누계로).
- 검사: 부문 합이 SEC 매출과 1.5백만 달러 안에서 맞아야 한다(SEG_ADJ로 본사·조정 차이를 cfg에 적을 수 있다).
  지도에 없는 멤버가 나오거나 값이 비면 멈춘다 — 카드는 이전 분기에 남는다.
원문은 .sec_cache/ixbrl/{접수번호}.json으로 한 번만 받는다.
"""
import datetime as dt
import html as htmlmod
import json
import os
import re
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
CACHE = os.path.join(V2, ".sec_cache", "ixbrl")
UA = "kim research gptjhss@gmail.com"


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")


def facts(url):
    """원문 인라인 XBRL의 숫자 사실: [(이름, 시작, 끝, ((차원, 멤버), ...), 값)]. 접수번호별로 저장해 둔다."""
    accn = re.search(r"/(\d{18})/", url).group(1)
    path = os.path.join(CACHE, f"{accn}.json")
    if os.path.exists(path):
        return [tuple(x[:3]) + (tuple(tuple(p) for p in x[3]), x[4]) for x in json.load(open(path))]
    h = _get(url)
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
    os.makedirs(CACHE, exist_ok=True)
    json.dump(out, open(path, "w"))
    return out


def _days(s, e):
    return (dt.date.fromisoformat(e) - dt.date.fromisoformat(s)).days


def by_member(fs, M, start_ok, end):
    """end에 끝나고 기간 길이가 start_ok(일수)를 만족하는 값을 멤버별로 — 지정한 차원만 붙은 것."""
    want_extra = set(M.get("extra", {}).items())
    for concept in M["concepts"]:
        got = {}
        for name, s, e, dims, v in fs:
            if name != concept or e != end or not s or not start_ok(_days(s, e)):
                continue
            ax = [m for d_, m in dims if d_ == M["axis"]]
            rest = {(d_, m) for d_, m in dims if d_ != M["axis"]}
            if len(ax) == 1 and rest == want_extra:
                ax = [M.get("alias", {}).get(ax[0], ax[0])]
                if ax[0] in got and got[ax[0]] != v:
                    raise ValueError(f"{concept} {ax[0]} {end}: 값이 둘({got[ax[0]]}, {v})")
                got[ax[0]] = v
        if got:
            return got
    return {}


def by_concept(fs, M, start_ok, end):
    """axis가 None인 묶음 — 멤버 자리에 차원 없는 개념(보험사 순보험료·MCD 가맹 수익 등, 2026-10-11)."""
    got = {}
    for name, s, e, dims, v in fs:
        if name in M["members"] and e == end and s and not dims and start_ok(_days(s, e)):
            if name in got and got[name] != v:
                raise ValueError(f"{name} {end}: 값이 둘({got[name]}, {v})")
            got[name] = v
    return got


def quarter_values(M, form, url, end, q3_url=None, q3_end=None):
    """분기 값 {멤버: 값}. 10-K면 연간 − 같은 회계연도 3분기 10-Q의 9개월 누계."""
    if M.get("axis") is None:
        fs = facts(url)
        if form == "10-Q":
            return by_concept(fs, M, lambda n: 70 <= n <= 125, end)
        fy = by_concept(fs, M, lambda n: 350 <= n <= 380, end)
        ytd = by_concept(facts(q3_url), M, lambda n: 230 <= n <= 290, q3_end)
        return {k: fy[k] - ytd[k] for k in fy if k in ytd}
    fs = facts(url)
    if form == "10-Q":
        return by_member(fs, M, lambda n: 70 <= n <= 125, end)
    fy = by_member(fs, M, lambda n: 350 <= n <= 380, end)
    if not q3_url:
        raise ValueError("10-K 4분기는 3분기 10-Q가 있어야 한다")
    ytd = by_member(facts(q3_url), M, lambda n: 230 <= n <= 290, q3_end)
    if set(fy) - set(ytd):
        raise ValueError(f"연간에만 있는 멤버 {sorted(set(fy) - set(ytd))} — 4분기 값을 만들 수 없다")
    return {k: fy[k] - ytd[k] for k in fy}


def table(M, vals):
    """(cfg SEG 꼴 [(이름, 백만 달러, 색)], 조정 합 백만 달러) — 지도에 없는 멤버는 other로 묶거나 멈춘다."""
    rows, other = [], 0.0
    skip = set(M.get("ignore", [])) | set(M.get("adjust", []))
    adj = round(sum(vals.get(k, 0) for k in M.get("adjust", [])) / 1e6)
    unknown = [k for k in vals if k not in M["members"] and k not in skip]
    if unknown and not M.get("other"):
        raise ValueError(f"지도에 없는 부문 {unknown} — SEG_MAP에 더할 것")
    agg = {}   # 여러 멤버를 한 줄로 묶을 수 있다(같은 이름) — 손 표의 "기타" 등
    for k, (name, color) in M["members"].items():
        if k not in vals:
            raise ValueError(f"부문 {k}의 값이 없다(부문 재편?)")
        v0, c0 = agg.get(name, (0.0, color))
        agg[name] = (v0 + vals[k], c0)
    for name, (v, color) in agg.items():
        rows.append((name, round(v / 1e6), color))
    for k in unknown:
        other += vals[k]
    if unknown:
        rows.append((M["other"], round(other / 1e6), "#94a3b8"))
    return sorted(rows, key=lambda r: -r[1]), adj
