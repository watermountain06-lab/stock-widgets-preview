#!/usr/bin/env python3
"""SK하이닉스 보고서 HTML(KIND 원문)에서 연결재무제표 숫자를 꺼낸다 — skhy_ifrs.py가 쓴다.

표는 제목이 아니라 **내용**으로 찾는다(2020년 보고서는 제목 다음에 표가 바로 오지 않고, 감사보고서는
제목이 "연 결 포 괄 …"처럼 띄어 쓰여 있다). 문서 앞쪽의 요약재무정보 표는 행 수·항목으로 거른다.
단위는 백만원. 반환값은 원(×1e6)이 아니라 **백만원 그대로**다.

    extract(path) → {"kind": "Q1"|"Q2"|"Q3"|"FY", "end": "YYYY-MM-DD",
                     "is3": {...} (분기 3개월, Q1은 누적과 같음), "isy": {...} (1월 1일부터 누적),
                     "bs": {...}, "cfy": {...} (누적), "missing": [...]}
"""
import html as H
import re
import sys

NUM = re.compile(r"^\(?-?[\d,]+(\.\d+)?\)?$")


def num(s):
    s = s.replace(" ", "")
    if s in ("-", "", "—"):
        return 0.0
    neg = s.startswith("(") or s.startswith("-")
    v = float(s.strip("()-").replace(",", ""))
    return -v if neg else v


def norm(label):
    s = re.sub(r"\(주[\d,\s]*\)|\(주석[\d,\s]*\)|\(손실\)|\(수익\)|\(이익\)|\(단위\s*:?\s*원\)|\(원\)", "", label)
    s = re.sub(r"^[ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩ\dA-Za-z]+\s*[.)]\s*", "", s.strip())
    s = re.sub(r"^\(?\d+\)\s*", "", s)
    return re.sub(r"[\s·ㆍ&nbsp;]", "", s)


def tables(h):
    out = []
    for tm in re.finditer(r"<table.*?</table>", h, re.S | re.I):
        rows = []
        for tr in re.findall(r"<tr.*?</tr>", tm.group(0), re.S | re.I):
            cells = [re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", "", c))).strip()
                     for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S | re.I)]
            if cells:
                rows.append(cells)
        out.append((tm.start(), rows))
    return out


def values(row, note_col):
    """행에서 숫자 칸만(주석 칸 제외)."""
    cells = row[1:]
    if note_col is not None and len(cells) > note_col - 1:
        cells = cells[:note_col - 1] + cells[note_col:]
    cells = [re.sub(r"\s*원$", "", c) for c in cells]      # 감사보고서 주당이익 "13,989 원"
    return [num(c) for c in cells if c and NUM.match(c.replace(" ", ""))]


def note_index(rows):
    for r in rows[:4]:
        for i, c in enumerate(r):
            if re.sub(r"\s|&nbsp;", "", c) in ("주석", "주 석"):
                return i
    return None


def labels(rows):
    return {norm(r[0]) for r in rows if r}


def find(tabs, need, min_rows):
    for pos, rows in tabs:
        ls = labels(rows)
        if any(l.startswith("[") for l in ls):      # 요약재무정보 표("[유동자산]")는 건너뛴다
            continue
        if len(rows) >= min_rows and all(any(n in l for l in ls) for n in need):
            return pos, rows
    return None, None


def rowvals(rows, keys, section=None, first_only=True):
    """keys 중 하나와 이름이 같은 행의 숫자들. section이 (시작키, 끝키)면 그 사이 행만."""
    active = section is None
    for r in rows:
        n = norm(r[0])
        if section:
            if n in section[0]:
                active = True
                continue
            if active and n in section[1]:
                active = False
        if active and n in keys:
            return r
    return None


def extract(path):
    h = open(path, encoding="utf-8", errors="ignore").read()
    tabs = tables(h)
    res = {"missing": []}
    # ── 기간 판별 ──
    m = re.search(r"(\d{4})[.년]\s*0?1[.월]\s*0?1일?\s*부터\s*(\d{4})[.년]\s*(\d{1,2})[.월]\s*(\d{1,2})", re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h[:3_000_000])))
    # 표에서 찾는 쪽이 안전하다 — 아래에서 손익 표 머리로 다시 정한다
    is_pos, is_rows = find(tabs, ["매출원가", "영업이익", "법인세비용"], 15)
    bs_pos, bs_rows = find(tabs, ["재고자산", "자산총계", "부채총계", "유동부채"], 25)
    cf_pos, cf_rows = find(tabs, ["영업활동현금흐름", "투자활동현금흐름", "재무활동현금흐름"], 15)
    if not (is_rows and bs_rows and cf_rows):
        raise SystemExit(f"{path}: 표 못 찾음 is={bool(is_rows)} bs={bool(bs_rows)} cf={bool(cf_rows)}")
    # 기간: 손익 표 앞 1500자 안의 "YYYY.MM.DD 까지"
    head = re.sub(r"<[^>]+>|&nbsp;", " ", h[max(0, is_pos - 3000):is_pos])
    ends = re.findall(r"(\d{4})[.년]\s*(\d{1,2})[.월]\s*(\d{1,2})일?\s*까지", head)
    if not ends:
        raise SystemExit(f"{path}: 기간 못 찾음")
    y, mo, d = ends[-2] if len(ends) >= 2 else ends[-1]
    y, mo = int(y), int(mo)
    res["end"] = f"{y}-{mo:02d}-{int(d):02d}"
    res["kind"] = {3: "Q1", 6: "Q2", 9: "Q3", 12: "FY"}[mo]
    three = any("3개월" in c for r in is_rows[:3] for c in r)
    nc = note_index(is_rows)

    def isv(keys):
        r = rowvals(is_rows, keys)
        if not r:
            return None, None
        v = values(r, nc)
        if not v:
            return None, None
        if three:
            return v[0], v[1]          # 3개월, 누적
        return v[0], v[0]             # 1분기 또는 연간
    IS = {"revenue": {"매출액", "매출", "수익(매출액)", "영업수익"},
          "cogs": {"매출원가"},
          "opinc": {"영업이익", "영업이익(손실)"},
          "pretax": {"법인세비용차감전순이익", "법인세차감전순이익", "법인세비용차감전순이익(손실)", "법인세차감전순이익(손실)"},
          "tax": {"법인세비용", "법인세비용(수익)"},
          "ni_total": {"당기순이익", "분기순이익", "반기순이익", "당기순이익(손실)", "분기순이익(손실)", "반기순이익(손실)"},
          "fin_income": {"금융수익"}, "fin_cost": {"금융비용"},
          "eps_b": {"기본주당이익", "기본주당순이익", "기본주당분기순이익", "기본주당반기순이익", "기본주당당기순이익"},
          "eps_d": {"희석주당이익", "희석주당순이익", "희석주당분기순이익", "희석주당반기순이익", "희석주당당기순이익"}}
    is3, isy = {}, {}
    for k, keys in IS.items():
        # 주당이익 행은 "(단위 : 원)"이 붙는다
        r = None
        for row in is_rows:
            n = re.sub(r"\(단위:?원\)", "", norm(row[0]))
            if n in keys:
                r = row
                break
        if r is None:
            res["missing"].append(k)
            continue
        v = values(r, nc)
        if not v:
            res["missing"].append(k)
            continue
        is3[k], isy[k] = (v[0], v[1]) if three else (v[0], v[0])
    # 지배기업 소유주 귀속 순이익 — "순이익의 귀속" 다음 첫 "지배기업의 소유주지분"
    after = False
    for row in is_rows:
        n = norm(row[0])
        if "순이익의귀속" in n or "순손익의귀속" in n:
            after = True
            continue
        if after and ("지배기업" in n and "소유" in n):
            v = values(row, nc)
            is3["ni"], isy["ni"] = (v[0], v[1]) if three else (v[0], v[0])
            break
    if "ni" not in is3:
        res["missing"].append("ni")
    res["is3"], res["isy"] = is3, isy

    # ── 재무상태표 ──
    bnc = note_index(bs_rows)
    sec = {}
    cur = None
    for row in bs_rows:
        n = norm(row[0])
        v = values(row, bnc)
        if n in ("유동자산",):
            cur = "ca"
        elif n in ("비유동자산",):
            cur = "nca"
        elif n in ("유동부채",):
            cur = "cl"
        elif n in ("비유동부채",):
            cur = "ncl"
        elif n in ("자본",) or n.startswith("지배기업"):
            cur = "eq"
        sec.setdefault(cur, []).append((n, v[0] if v else None))
    flat = [x for s in sec.values() for x in s]

    def first(keys, where=None):
        for n, v in (sec.get(where, []) if where else flat):
            if n in keys and v is not None:
                return v
        return None

    def total(pred, where):
        return sum(v for n, v in sec.get(where, []) if v is not None and pred(n))
    bs = {
        "cash": first({"현금및현금성자산"}),
        "sti": total(lambda n: n in ("단기금융상품", "단기투자자산", "단기투자증권"), "ca"),
        "ar": first({"매출채권", "매출채권및기타채권"}, "ca"),
        "inv": first({"재고자산"}, "ca"),
        "ca": first({"유동자산"}), "assets": first({"자산총계"}),
        "cl": first({"유동부채"}), "liab": first({"부채총계"}),
        "ap": first({"매입채무", "매입채무및기타채무"}, "cl"),
        "st_debt": total(lambda n: n in ("차입금", "단기차입금", "유동성장기부채", "유동성사채", "유동성장기차입금", "사채"), "cl"),
        "lt_debt": total(lambda n: n in ("차입금", "장기차입금", "사채"), "ncl"),
        "lease_cur": total(lambda n: n == "리스부채", "cl"),
        "lease_non": total(lambda n: n == "리스부채", "ncl"),
        "equity": next((v for n, v in sec.get("eq", []) if n.startswith("지배기업") and v is not None), None),
        "nci": first({"비지배지분"}, "eq") or 0.0,
        "lti": total(lambda n: n in ("장기금융상품", "장기투자자산", "장기투자증권"), "nca"),
        "equity_method": total(lambda n: n.startswith("관계기업") or n.startswith("공동기업"), "nca"),
    }
    for k, v in bs.items():
        if v is None:
            res["missing"].append("bs." + k)
    res["bs"] = bs

    # ── 현금흐름표(누적) ──
    cnc = note_index(cf_rows)

    def cfv(pred):
        for row in cf_rows:
            n = norm(row[0])
            if pred(n):
                v = values(row, cnc)
                if v:
                    return v[0]
        return None
    cfy = {"ocf": cfv(lambda n: n == "영업활동현금흐름"),
           "capex_ppe": cfv(lambda n: n in ("유형자산의취득",)),
           "capex_int": cfv(lambda n: n in ("무형자산의취득",)),
           "int_paid": cfv(lambda n: n in ("이자의지급",)),
           "div": cfv(lambda n: n in ("배당금의지급",)),
           "buyback": cfv(lambda n: n in ("자기주식의취득",)) or 0.0}
    for k in ("ocf", "capex_ppe", "capex_int"):
        if cfy[k] is None:
            res["missing"].append("cf." + k)
    # 감가상각·무형자산상각 — "비용의 성격별 분류" 주석(손익 표 뒤 첫 표, "원재료…" 행과 "감가상각…" 행).
    # 현금흐름표 주석은 2021년 이전 보고서에 감가상각 행이 없어, 모든 해에 있는 이 주석으로 통일한다(2026-09-27).
    # 1분기·연간은 첫 값(= 누적), 반기·3분기는 [3개월, 누적, …]의 둘째 값.
    da = None
    for pos, rows in tabs:
        if pos <= is_pos:
            continue
        ls = [norm(r[0]) for r in rows]
        if any(l.startswith("원재료") for l in ls) and any(l.startswith("감가상각") for l in ls):
            r = next(r for r in rows if norm(r[0]).startswith("감가상각"))
            v = values(r, None)
            da = v[1] if res["kind"] in ("Q2", "Q3") else v[0]
            break
    if da is None:
        res["missing"].append("cf.da")
    cfy["da"] = da

    # ── 주식 수(보통주, 발행 − 자기주식) — 분기·반기보고서 "주식의 총수 등" 표, 없으면 주석의 주주 현황표 ──
    res["shares"] = None
    for pos, rows in tabs:
        ls = [norm(r[0]) for r in rows]
        if any("발행주식의총수" in l for l in ls) and any("유통주식수" in l for l in ls):
            r = next(r for r in rows if "유통주식수" in norm(r[0]))
            res["shares"] = values(r, None)[0]
            break
    if res["shares"] is None:
        for pos, rows in tabs:
            ls = [norm(r[0]) for r in rows]
            if any(l.startswith("자기주식") for l in ls) and any(l.startswith("합계") for l in ls) and \
                    any("소유주식수" in c.replace(" ", "") for r in rows[:3] for c in r):
                tot = next(values(r, None)[0] for r in rows if norm(r[0]).startswith("합계"))
                tr = next(values(r, None)[0] for r in rows if norm(r[0]).startswith("자기주식"))
                res["shares"] = tot - tr
                break
    if res["shares"] is None:
        res["missing"].append("shares")
    res["cfy"] = {k: (abs(v) if k in ("capex_ppe", "capex_int", "int_paid", "div", "buyback") and v is not None else v)
                  for k, v in cfy.items()}
    return res


if __name__ == "__main__":
    import json
    r = extract(sys.argv[1])
    print(json.dumps(r, ensure_ascii=False, indent=1))
