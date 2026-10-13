#!/usr/bin/env python3
"""버크셔 카드의 분기 숫자 — 10-Q/10-K 원문(인라인 XBRL + MD&A 글)에서 읽는다(2026-10-12, BRKB 생성기).

카드가 쓰는 값 가운데 XBRL에 없는 것(회사 정의 세후 사업별 영업이익 표, 보험 플로트, 상장주식 상위 5종목 비중)은
MD&A 문장을 정해진 꼴로 읽는다. 꼴이 바뀌면 추측하지 않고 멈춘다(BrkbParseError) — 그 분기는 사람이 본다.
세후 표는 행을 다 더한 값이 표의 순이익과 같은지(±$2M, 반올림)로 스스로 점검한다.

    from brkb_quarter import quarter
    q = quarter("2026-06-30", asof="2026-10-09")   # 그 분기 3개월 값 + 1년 전·직전 분기 + 재무상태표
"""
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from brkb_facts import load_facts  # noqa: E402
from brkb_pillars import text_of  # noqa: E402

FACTS = load_facts()
IO, RUE = ["InsuranceAndOtherMember"], ["RailroadUtilitiesAndEnergyMember"]


class BrkbParseError(RuntimeError):
    pass


# ── 공시 목록 ────────────────────────────────────────────────────────────
def docs(asof=None):
    """[(분기 말, 양식, 접수일, 문서)] — 분기마다 가장 먼저 접수된 10-Q/10-K, asof까지."""
    best = {}
    for f in FACTS:
        if f["form"] not in ("10-Q", "10-K") or (asof and f["filed"] > asof):
            continue
        k = f["report"]
        if k not in best or f["filed"] < best[k][2]:
            best[k] = (k, f["form"], f["filed"], f["doc"])
    return [best[k] for k in sorted(best)]


def doc_for(end, asof=None):
    d = next((x for x in docs(asof) if x[0] == end), None)
    if not d:
        raise BrkbParseError(f"{end} 공시가 없다")
    return d


def prev_q(end):
    y, md = int(end[:4]), end[5:]
    return {"03-31": f"{y - 1}-12-31", "06-30": f"{y}-03-31", "09-30": f"{y}-06-30", "12-31": f"{y}-09-30"}[md]


def year_ago(end):
    return f"{int(end[:4]) - 1}{end[4:]}"


# ── MD&A 세후 사업별 표 ──────────────────────────────────────────────────
# 행 이름 → 키. 이름이 바뀌어 온 행(BNSF←Railroad, BHE←Utilities and energy, 투자 손익 이름 셋)을 다 받는다.
# 모르는 이름의 행은 영업 사업으로 본다(Pilot Travel Centers, Non-controlled businesses — 회사도 영업이익에 넣는다).
KEYS = [("uw", r"^Insurance – underwriting"), ("invinc", r"^Insurance – investment income"),
        ("rail", r"^(?:BNSF|Railroad)\b"), ("energy", r"^(?:Berkshire Hathaway Energy|BHE\b|Utilities and energy)"),
        ("msr", r"^Manufacturing, service and retailing"),
        ("gains", r"^Investment (?:and derivative )?(?:contract )?gains"),
        ("otti", r"^Other-than-temporary impairment"), ("other", r"^Other$"),
        ("ni", r"^Net earnings(?: \(loss\))? attributable to Berkshire")]
NONOPER = ("gains", "otti", "ni")   # 회사 정의 영업이익(세후) = 표의 나머지 행 합
NUM = r"\(\s*[\d,]+\s*\)|[\d,]*\d|—"


def _num(s):
    s = s.strip()
    if s == "—":
        return 0.0
    v = float(s.strip("() ").replace(",", ""))
    return -v if s.startswith("(") else v


def seg_table(doc):
    """{행 키: [열 값($M)…]} — 10-Q 1분기 [이번, 1년 전], 2·3분기 [이번, 1년 전, 누계, 1년 전 누계], 10-K [올해, 작년, 재작년].
    모르는 행은 'x:행 이름' 키(영업 사업). 열 수는 머리의 연도 수로 정한다."""
    t = text_of(doc)
    i = t.find("disaggregated in the table that follows")
    k = t.find("(in millions).", i)
    if i < 0 or k < 0 or k - i > 400:
        raise BrkbParseError(f"{doc}: 세후 사업별 표를 찾지 못했다")
    body = t[k + 14:k + 3000]
    b0 = body.find("Insurance – underwriting")
    if b0 < 0:
        raise BrkbParseError(f"{doc}: 세후 표 첫 행(Insurance – underwriting)이 없다")
    n = len(re.findall(r"\b(?:19|20)\d\d\b", body[:b0]))
    if n not in (2, 3, 4):
        raise BrkbParseError(f"{doc}: 세후 표 머리의 연도 수 {n}")
    out, pos, body = {}, 0, body[b0:]
    while True:
        m = re.search(r"\$?\s*(" + NUM + r")", body[pos:])
        if not m:
            raise BrkbParseError(f"{doc}: 세후 표가 순이익 행 전에 끝났다")
        label = re.sub(r"\s*\*$", "", body[pos:pos + m.start()].strip(" $"))
        vals, q = [], pos + m.start()
        for _ in range(n):
            mm = re.match(r"\s*\$?\s*(" + NUM + r")", body[q:])
            if not mm:
                raise BrkbParseError(f"{doc}: '{label}' 행 값이 {n}개가 아니다")
            vals.append(_num(mm.group(1)))
            q += mm.end()
        key = next((kk for kk, pat in KEYS if re.search(pat, label)), "x:" + label)
        if key in out:
            raise BrkbParseError(f"{doc}: 세후 표에 '{key}' 행이 둘")
        out[key] = vals
        pos = q
        if key == "ni":
            break
        if len(out) > 15:
            raise BrkbParseError(f"{doc}: 세후 표 행이 너무 많다(순이익 행을 못 찾음)")
    for need in ("uw", "invinc", "rail", "energy", "msr", "gains", "ni"):
        if need not in out:
            raise BrkbParseError(f"{doc}: 세후 표에 '{need}' 행이 없다 — 행 {list(out)}")
    for c in range(n):   # 행을 다 더하면 순이익 — 안 맞으면 행을 잘못 읽은 것
        s_ = sum(v[c] for kk, v in out.items() if kk != "ni")
        if abs(s_ - out["ni"][c]) > 2:
            raise BrkbParseError(f"{doc}: 세후 표 {c + 1}열 합 {s_:,.0f} ≠ 순이익 {out['ni'][c]:,.0f}")
    return out


def _col(tab, c):
    d = {k: v[c] for k, v in tab.items()}
    for k in ("otti", "other"):
        d.setdefault(k, 0.0)
    d["oper"] = sum(v for k, v in d.items() if k not in NONOPER)
    return d


def seg_quarter(end, asof=None):
    """(그 분기 3개월, 1년 전 같은 분기) 세후 표 — 4분기는 연간 − 3분기 누계."""
    _, form, _, doc = doc_for(end, asof)
    tab = seg_table(doc)
    if form == "10-Q":
        return _col(tab, 0), _col(tab, 1)
    y = int(end[:4])
    q3 = seg_table(doc_for(f"{y}-09-30", asof)[3])
    if len(q3["ni"]) != 4:
        raise BrkbParseError(f"{y} 3분기 10-Q 세후 표에 누계 열이 없다")
    if set(tab) != set(q3):   # 연말 10-K에서 사라진 사업 행은 제조·서비스·소매에 합쳐진 것(2024 Pilot) — 3분기 누계 쪽도 거기에 더한다(Codex)
        gone, new = set(q3) - set(tab), set(tab) - set(q3)
        if new or any(not k.startswith("x:") for k in gone):
            raise BrkbParseError(f"{y} 10-K와 3분기 10-Q의 세후 표 행이 다르다: {sorted(gone | new)}")
        for k in gone:
            q3["msr"] = [a_ + b_ for a_, b_ in zip(q3["msr"], q3.pop(k))]
    cur = {k: tab[k][0] - q3[k][2] for k in tab}
    yo = {k: tab[k][1] - q3[k][3] for k in tab}
    return _col({k: [v] for k, v in cur.items()}, 0), _col({k: [v] for k, v in yo.items()}, 0)


# ── 본문 문장 ────────────────────────────────────────────────────────────
def float_of(doc):
    """(플로트 $B, 연초 대비 변화 $B 또는 None)."""
    t = text_of(doc)
    m = re.search(r"[Ff]loat (?:was approximately|approximated|was) \$([\d.]+) billion (?:at|as of) [A-Z][a-z]+ \d+, \d{4}", t)
    if not m:
        raise BrkbParseError(f"{doc}: 플로트 문장을 찾지 못했다")
    v = float(m.group(1))
    ch = re.match(r", an? (increase|decrease) of approximately \$([\d.]+) billion", t[m.end():m.end() + 120])
    if ch:
        return v, (1 if ch.group(1) == "increase" else -1) * float(ch.group(2))
    if re.match(r",? (?:and )?(?:essentially )?unchanged", t[m.end():m.end() + 60]):
        return v, 0.0
    return v, None


QW = {1: "first", 2: "second", 3: "third"}


def fx_of(doc, qn):
    """'기타'에 든 외화 차입금 환산 손익(세후, $M) (이번 분기, 1년 전 분기) — 확실한 문장 꼴 둘만 읽고, 못 읽으면 None(선택 정보).
    10-Q 2·3분기: '…exchange gains were $326 million in the second quarter … compared to losses of $877 million in the second quarter'
    10-Q 1분기: '…exchange rate gains of $249 million in 2026 compared to losses of $713 million in 2025'. 10-K(4분기)는 읽지 않는다."""
    if qn not in QW:
        return None
    t = text_of(doc)
    amt = lambda v, u: float(v.replace(",", "")) * (1000 if u == "billion" else 1)
    sg = lambda w: 1 if w == "gains" else -1
    m = re.search(r"after-tax foreign currency exchange (?:rate )?(gains|losses) (?:were|of) \$([\d.,]+) (million|billion) in the "
                  + QW[qn] + r" quarter[^.]{0,160}?compared to (?:after-tax )?(gains|losses) of \$([\d.,]+) (million|billion) in the " + QW[qn] + " quarter", t)
    if not m and qn == 1:
        m = re.search(r"after-tax foreign currency exchange (?:rate )?(gains|losses) of \$([\d.,]+) (million|billion) in \d{4} compared to "
                      r"(?:after-tax )?(gains|losses) of \$([\d.,]+) (million|billion) in \d{4}", t)
    if not m:
        return None
    return sg(m.group(1)) * amt(m.group(2), m.group(3)), sg(m.group(4)) * amt(m.group(5), m.group(6))


def top5_of(doc):
    """(상위 5종목 비중 %, 종목 이름 목록) — 문장 꼴 둘(2025년 뒤 '…represented 66 %', 그 전 각주 'Approximately 70 % … five companies (…)')."""
    t = text_of(doc)
    D = r"[A-Z][a-z]+ \d+, \d{4}"
    m = re.search(r"five largest holdings at " + D + r"(?: and (?:" + D + r"|\d{4}))? represented (\d+) ?%", t)
    if m:
        n = re.search(r"The five largest holdings at (?:each date|" + D + r") were (.+?)\. (?=[A-Z])", t[m.end():m.end() + 600])
        names = n.group(1) if n else ""
    else:
        m = re.search(r"[Aa]pproximately (\d+) ?% of the aggregate fair value (?:of [^.]{0,60})?was concentrated in five companies(?: \(([^)]*)\))?", t)
        if not m:
            raise BrkbParseError(f"{doc}: 상위 5종목 비중 문장을 찾지 못했다")
        names = re.sub(r" – \$ ?[\d.]+ billion", "", m.group(2) or "")
    out = [x.strip() for x in re.split(r";\s*(?:and\s+)?|,\s*(?:and\s+)?(?=[A-Z])|\s+and\s+(?=[A-Z])", names) if x.strip()]
    return int(m.group(1)), out


# ── XBRL 값 ──────────────────────────────────────────────────────────────
def _pick(name, dims, start, end, asof):
    s = sorted(dims)
    c = [f for f in FACTS if f["name"] == name and f["start"] == start and f["end"] == end
         and sorted(f["dims"]) == s and (asof is None or f["filed"] <= asof)]
    return min(c, key=lambda f: f["filed"])["val"] if c else None


def _qstart(end):
    return {"03-31": "01-01", "06-30": "04-01", "09-30": "07-01", "12-31": "10-01"}[end[5:]]


def flow_q(name, dims, end, asof):
    """3개월 값 — 3개월 사실이 없으면 누계 차(4분기 = 연간 − 9개월)."""
    y = end[:4]
    v = _pick(name, dims, f"{y}-{_qstart(end)}", end, asof)
    if v is not None:
        return v
    cur = _pick(name, dims, f"{y}-01-01", end, asof)
    if cur is None:
        return None
    if end.endswith("03-31"):
        return cur
    p = _pick(name, dims, f"{y}-01-01", prev_q(end), asof)
    return None if p is None else cur - p


def flow_ytd(name, dims, end, asof):
    y = end[:4]
    v = _pick(name, dims, f"{y}-01-01", end, asof)
    if v is None and end.endswith("03-31"):
        v = _pick(name, dims, f"{y}-01-01", end, asof)
    if v is None:   # 3개월 사실만 내는 태그(자사주)는 분기를 더한다
        qs = [e for e in (f"{y}-03-31", f"{y}-06-30", f"{y}-09-30", f"{y}-12-31") if e <= end]
        vals = [flow_q(name, dims, e, asof) for e in qs]
        v = None if any(x is None for x in vals) else sum(vals)
    return v


def bal(name, dims, end, asof):
    return _pick(name, dims, None, end, asof)


def buyback_q(e, asof):
    """자사주 매입(원가) 3개월 — 자본변동표 원가 태그, 없으면 현금흐름표 태그, 둘 다 없으면 0(사지 않은 분기는 태그를 안 낸다: 2024 3분기~2025)."""
    v = flow_q("TreasuryStockValueAcquiredCostMethod", [], e, asof)
    if v is None:
        v = flow_q("PaymentsForRepurchaseOfCommonStock", [], e, asof)
    return 0.0 if v is None else v


def quarter(end, asof=None):
    """카드 한 분기 묶음. 값은 달러(세후 표는 $M → 달러로 바꿈)."""
    form, filed, doc = doc_for(end, asof)[1:]
    cur, yo = seg_quarter(end, asof)
    pq = prev_q(end)
    try:
        pcur, _ = seg_quarter(pq, asof)
    except BrkbParseError:
        pcur = None
    m = lambda d: {k: v * 1e6 for k, v in d.items()} if d else None
    rev = lambda e: (lambda a, b: None if None in (a, b) else a + b)(flow_q("Revenues", IO, e, asof), flow_q("Revenues", RUE, e, asof))
    ocf = lambda e: flow_q("NetCashProvidedByUsedInOperatingActivities", [], e, asof)
    capx = lambda e: flow_q("PaymentsToAcquirePropertyPlantAndEquipment", [], e, asof)
    fcf = lambda e: (lambda a, b: None if None in (a, b) else a - b)(ocf(e), capx(e))
    fl, fl_ch = float_of(doc)
    t5, t5_names = top5_of(doc)
    q = {"end": end, "form": form, "filed": filed, "doc": doc,
         "seg": m(cur), "seg_yo": m(yo), "seg_prev": m(pcur),
         "rev": rev(end), "rev_yo": rev(year_ago(end)), "rev_prev": rev(pq),
         "ni": flow_q("NetIncomeLoss", [], end, asof), "ni_yo": flow_q("NetIncomeLoss", [], year_ago(end), asof),
         "ni_prev": flow_q("NetIncomeLoss", [], pq, asof),
         "fcf": fcf(end), "fcf_yo": fcf(year_ago(end)), "fcf_prev": fcf(pq), "capex": capx(end),
         "buyback": buyback_q(end, asof),
         "buyback_ytd": sum(buyback_q(e, asof) for e in (f"{end[:4]}-03-31", f"{end[:4]}-06-30", f"{end[:4]}-09-30", f"{end[:4]}-12-31") if e <= end),
         "acq_ytd": flow_ytd("PaymentsToAcquireBusinessesNetOfCashAcquired", [], end, asof),
         "cash_io": bal("CashAndCashEquivalentsAtCarryingValue", IO, end, asof),
         "cash_rue": bal("CashAndCashEquivalentsAtCarryingValue", RUE, end, asof),
         "tbills": bal("USTreasuryBills", IO, end, asof),
         "eq_fv": bal("EquitySecuritiesFvNi", IO, end, asof),
         "debt_io": bal("DebtAndCapitalLeaseObligations", IO, end, asof),
         "debt_rue": bal("DebtAndCapitalLeaseObligations", RUE, end, asof),
         "float": fl * 1e9, "float_ytd_change": None if fl_ch is None else fl_ch * 1e9,
         "top5_pct": t5, "top5": t5_names}
    miss = [k for k in ("rev", "rev_yo", "ni", "ni_yo", "fcf", "buyback", "buyback_ytd", "cash_io", "tbills", "eq_fv", "debt_io", "debt_rue") if q[k] is None]
    if miss:
        raise BrkbParseError(f"{end}: XBRL 값 없음 {miss}")
    return q


def last_end(asof):
    d = docs(asof)
    return d[-1][0] if d else None


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else dt.date.today().isoformat()
    e = last_end(a)
    q = quarter(e, a)
    print(json.dumps({k: (round(v / 1e9, 3) if isinstance(v, float) and abs(v) > 1e6 else v) for k, v in q.items()
                      if not isinstance(v, dict)}, ensure_ascii=False, indent=1))
    print({k: round(v / 1e9, 3) for k, v in q["seg"].items()})
