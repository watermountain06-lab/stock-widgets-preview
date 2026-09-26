#!/usr/bin/env python3
"""BRKB 두 기둥 내재가치 — research/brkb_two_pillar_prereg.md 4판 구현.

    python3 v2/adapters/brkb_pillars.py            # 관문 G1~G3 + 분기별 가치 + 기술 통계
    python3 v2/adapters/brkb_pillars.py --json out.json

주당 내재가치 = (투자 기둥 + 영업 기둥 이익 ÷ 10%) ÷ 기말 B주 환산 주식 수. 모든 값은 평가 시점 t까지
공시된 10-Q/10-K만 쓴다(같은 기간 값은 처음 공시된 것). 정의는 사전 등록 문서가 원본이다.
"""
import datetime as dt
import html
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from brkb_facts import load_facts, RAW  # noqa: E402

TAX, RATE = 0.21, 0.10
SUBGROUPS = ("GeicoMember", "BerkshireHathawayPrimaryGroupMember", "BerkshireHathawayReinsuranceGroupMember")
IO = ["InsuranceAndOtherMember"]
FACTS = load_facts()
BY = {}
for f in FACTS:
    BY.setdefault(f["name"], []).append(f)


def qends(first="2019-03-31", last="2026-06-30"):
    out, y, q = [], int(first[:4]), (int(first[5:7]) - 1) // 3 + 1
    while True:
        e = f"{y}-{['03-31', '06-30', '09-30', '12-31'][q - 1]}"
        if e > last:
            return out
        out.append(e)
        q += 1
        if q == 5:
            y, q = y + 1, 1


def pick(name, pred, start, end, asof):
    """조건을 만족하는 (start, end) 사실 중 asof까지 공시된, 가장 먼저 공시된 값."""
    c = [f for f in BY.get(name, []) if f["start"] == start and f["end"] == end and pred(f["dims"])
         and (asof is None or f["filed"] <= asof)]
    return min(c, key=lambda f: f["filed"])["val"] if c else None


def exact(dims):
    s = sorted(dims)
    return lambda d: sorted(d) == s


# ── 흐름 항목: 연초부터 누적(ytd) 값 ─────────────────────────────────────────
def ytd_simple(name, pred):
    def f(year, end, asof):
        return pick(name, pred, f"{year}-01-01", end, asof)
    return f


def ytd_sum_members(name, members):
    """투자처 멤버별 사실의 합(지분법 손상). 하나도 없으면 None."""
    def f(year, end, asof):
        vals = [pick(name, exact([m]), f"{year}-01-01", end, asof) for m in members]
        vals = [v for v in vals if v is not None]
        # 분기 사실만 있고 누적이 없는 경우: 같은 해 3개월 사실을 더한다
        if not vals:
            q = [pick(name, exact([m]), s, e, asof) for m in members for s, e in quarters_in(year, end)]
            q = [v for v in q if v is not None]
            return sum(q) if q else None
        return sum(vals)
    return f


def quarters_in(year, end):
    out = []
    for s, e in [("01-01", "03-31"), ("04-01", "06-30"), ("07-01", "09-30"), ("10-01", "12-31")]:
        if f"{year}-{e}" <= end:
            out.append((f"{year}-{s}", f"{year}-{e}"))
    return out


def uw_ytd(year, end, asof):
    """보험 인수손익(세전) 누적 — 세 하위 그룹 합. 새 체계(2024 10-K~) 먼저, 없으면 옛 체계."""
    def one(system, sg, start, e):
        if system == "new":
            name = "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"
            pr = lambda d: sg in d and "UnderwritingMember" in d and "InvestmentsSegmentMember" not in d \
                and set(d) <= {sg, "UnderwritingMember", "BerkshireHathawayInsuranceGroupMember", "OperatingSegmentsMember"}
        else:
            name = "OperatingIncomeLoss"
            pr = lambda d: sg in d and "InvestmentIncomeMember" not in d \
                and set(d) <= {sg, "BerkshireHathawayInsuranceGroupMember", "OperatingSegmentsMember",
                               "PremiumsEarnedNetMember", "InsuranceUnderwritingMember"}
        return pick(name, pr, start, e, asof)
    best = None
    for system in ("new", "old"):
        vals = [one(system, sg, f"{year}-01-01", end) for sg in SUBGROUPS]
        if all(v is not None for v in vals):
            cand = sum(vals)
            # 두 체계가 다 있으면 먼저 공시된 쪽(시점 규칙) — 새 체계는 늦게 공시되므로 옛 체계가 이긴다
            if best is None:
                best = cand
            elif system == "old":
                best = cand
    if best is None:
        # 누적이 없으면 3개월 사실의 합(10-Q 일부)
        qs = []
        for s, e in quarters_in(year, end):
            v = None
            for system in ("old", "new"):
                vals = [one(system, sg, s, e) for sg in SUBGROUPS]
                if all(x is not None for x in vals):
                    v = sum(vals)
                    break
            if v is None:
                return None
            qs.append(v)
        best = sum(qs)
    return best


ITEMS = {
    # 핵심 항목(없으면 기권)
    "ni": (ytd_simple("NetIncomeLoss", exact([])), True),
    "gains": (ytd_simple("GainLossOnInvestments", exact([])), True),
    "invinc": (ytd_simple("InvestmentIncomeInterestDividendAndOther", exact(IO)), True),
    "uw": (uw_ytd, True),
    # 산발 항목(없으면 0)
    "deriv": (lambda y, e, a: (ytd_simple("GainLossOnDerivativeInstrumentsNetPretax",
                                          exact(["EquityContractMember", "NondesignatedMember"]) if y == 2020 else exact([]))(y, e, a)), False),
    "imp": (ytd_simple("GoodwillAndIntangibleAssetImpairment", exact(IO)), False),
    "otti": (ytd_sum_members("EquityMethodInvestmentOtherThanTemporaryImpairment",
                             ["TheKraftHeinzCompanyMember", "OccidentalPetroleumCorporationMember"]), False),
    "buyback": (ytd_simple("PaymentsForRepurchaseOfCommonStock", exact([])), False),
}


def ytd(item, year, end, asof):
    fn, core = ITEMS[item]
    v = fn(year, end, asof)
    if v is None and not core:
        return 0.0
    return v


def last_reported(t):
    """t까지 공시된 가장 최근 분기 말(순이익 누적이 공시된 분기)."""
    for e in reversed(qends(last=t)):
        if ytd("ni", int(e[:4]), e, t) is not None:
            return e
    return None


def ttm(item, L, asof):
    y, md = int(L[:4]), L[5:]
    cur = ytd(item, y, L, asof)
    if md == "12-31":
        return cur
    ann = ytd(item, y - 1, f"{y - 1}-12-31", asof)
    prev = ytd(item, y - 1, f"{y - 1}-{md}", asof)
    if None in (cur, ann, prev):
        return None
    return cur + ann - prev


def quarter_value(item, e, asof):
    y = int(e[:4])
    cur = ytd(item, y, e, asof)
    prev_e = {"03-31": None, "06-30": "03-31", "09-30": "06-30", "12-31": "09-30"}[e[5:]]
    if cur is None:
        return None
    if prev_e is None:
        return cur
    p = ytd(item, y, f"{y}-{prev_e}", asof)
    return None if p is None else cur - p


def impairment_after_tax(L, asof):
    """영업권·무형자산 손상 세후(최근 4분기). 연도별 10-K 세율 조정표의 공제 불가분 세효과로 세후를 만든다.
    그 해 10-K가 아직 없거나 태그가 없으면 None(기권)."""
    y, md = int(L[:4]), L[5:]
    parts = [(y, ytd("imp", y, L, asof))]
    if md != "12-31":
        ann, prev = ytd("imp", y - 1, f"{y - 1}-12-31", asof), ytd("imp", y - 1, f"{y - 1}-{md}", asof)
        parts.append((y - 1, ann - prev))
    total = 0.0
    for yr, amt in parts:
        if not amt:
            continue
        eff = pick("IncomeTaxReconciliationNondeductibleExpenseImpairmentLosses", exact([]), f"{yr}-01-01", f"{yr}-12-31", asof)
        full = ytd("imp", yr, f"{yr}-12-31", asof)
        if eff is None or not full:
            return None
        total += amt * (1 - TAX) + eff * amt / full
    return total


def balance(name, dims, e, asof, fallback=None):
    v = pick(name, exact(dims), None, e, asof)
    if v is None and fallback is not None:
        v = pick(name, exact(fallback), None, e, asof)
    return v


def pillars(t, rate=RATE):
    """평가 시점 t(분기 말)의 두 기둥. 기권이면 이유를 담아 돌려준다."""
    L = last_reported(t)
    if L is None:
        return {"t": t, "abstain": "공시 없음"}
    r = {"t": t, "L": L}
    for it in ("ni", "gains", "invinc", "uw", "deriv", "otti", "buyback"):
        r[it] = ttm(it, L, t)
    if any(r[k] is None for k in ("ni", "gains", "invinc", "uw")):
        r["abstain"] = "핵심 흐름 항목 없음: " + ",".join(k for k in ("ni", "gains", "invinc", "uw") if r[k] is None)
        return r
    r["imp_at"] = impairment_after_tax(L, t)
    if r["imp_at"] is None:
        r["abstain"] = "영업권 손상 세후 확인 불가(그 해 10-K 세율 조정표 없음)"
        return r
    r["op_norm"] = r["ni"] - (r["gains"] + r["deriv"]) * (1 - TAX) + r["imp_at"] + r["otti"] * (1 - TAX)
    r["e2"] = r["op_norm"] - (r["invinc"] + r["uw"]) * (1 - TAX)
    bs = {"cash": balance("CashAndCashEquivalentsAtCarryingValue", IO, L, t),
          "tbills": balance("USTreasuryBills", IO, L, t),
          "bonds": balance("AvailableForSaleSecuritiesDebtSecurities", IO, L, t, fallback=[]),
          "eq_fv": balance("EquitySecuritiesFvNi", IO, L, t, fallback=[]),
          "eq_cost": balance("EquitySecuritiesFvNiCost", [], L, t),
          # 2025-09 10-Q부터 같은 줄("Payables for purchases of U.S. Treasury Bills")을 다른 태그로 낸다
          # (2026-06-30 $771M, 10-Q 대조). 결과를 본 뒤 고친 추출 오류 — 사전 등록 문서에 표시.
          "payable": (balance("PayableForPurchaseOfUSTreasuryBills", IO, L, t)
                      if balance("PayableForPurchaseOfUSTreasuryBills", IO, L, t) is not None
                      else balance("OtherPayablesToBrokerDealersAndClearingOrganizations", IO, L, t)) or 0.0,
          "sharesA": balance("CommonStockSharesOutstanding", ["EquivalentClassAMember"], L, t),
          "equity": balance("StockholdersEquity", [], L, t)}
    r.update(bs)
    miss = [k for k in ("cash", "tbills", "bonds", "eq_fv", "eq_cost", "sharesA") if bs[k] is None]
    if miss:
        r["abstain"] = "핵심 재무상태표 항목 없음: " + ",".join(miss)
        return r
    r["p1"] = bs["cash"] + bs["tbills"] + bs["bonds"] + bs["eq_fv"] - bs["payable"] - max(bs["eq_fv"] - bs["eq_cost"], 0) * TAX
    r["sharesB"] = bs["sharesA"] * 1500
    r["iv"] = (r["p1"] + r["e2"] / rate) / r["sharesB"]
    r["iv_9"] = (r["p1"] + r["e2"] / 0.09) / r["sharesB"]
    r["iv_11"] = (r["p1"] + r["e2"] / 0.11) / r["sharesB"]
    r["bvps"] = bs["equity"] / r["sharesB"] if bs["equity"] else None
    # 시나리오: 연간 영업 기둥 이익(FY2019~, t까지 공시된 10-K)
    fy = {}
    for y in range(2019, int(L[:4]) + 1):
        e = f"{y}-12-31"
        if e > L:
            break
        rr = {it: ytd(it, y, e, t) for it in ("ni", "gains", "invinc", "uw", "deriv", "otti")}
        if any(rr[k] is None for k in ("ni", "gains", "invinc", "uw")):
            continue
        ia = impairment_after_tax(e, t)
        if ia is None:
            continue
        op = rr["ni"] - (rr["gains"] + rr["deriv"]) * (1 - TAX) + ia + rr["otti"] * (1 - TAX)
        fy[y] = op - (rr["invinc"] + rr["uw"]) * (1 - TAX)
    r["fy_e2"] = fy
    ys = sorted(fy)[-5:]
    if ys:
        lo = min(fy[y] for y in ys)
        g = 0.0
        if len(ys) >= 2 and fy[ys[0]] > 0 and fy[ys[-1]] > 0:
            g = (fy[ys[-1]] / fy[ys[0]]) ** (1 / (ys[-1] - ys[0])) - 1
        g = min(max(g, 0.0), 0.10)
        r["iv_low"] = (r["p1"] + lo / rate) / r["sharesB"]
        r["iv_high"] = (r["p1"] + r["e2"] * (1 + g) / rate) / r["sharesB"]
        r["growth"] = g
    return r


# ── 관문 ─────────────────────────────────────────────────────────────────
def g1():
    """분기 정확성: 누적 차분으로 만든 분기값 vs 공시된 3개월 사실(있을 때). 인수손익 두 체계 대조."""
    names = {"ni": ("NetIncomeLoss", exact([])), "gains": ("GainLossOnInvestments", exact([])),
             "invinc": ("InvestmentIncomeInterestDividendAndOther", exact(IO)),
             "imp": ("GoodwillAndIntangibleAssetImpairment", exact(IO))}
    bad, checked = [], 0
    for e in qends(first="2019-06-30"):
        if e[5:] == "03-31":
            continue
        y = int(e[:4])
        s = {"06-30": f"{y}-04-01", "09-30": f"{y}-07-01", "12-31": f"{y}-10-01"}[e[5:]]
        for k, (nm, pr) in names.items():
            direct = pick(nm, pr, s, e, None)
            derived = quarter_value(k, e, None)
            if direct is None or derived is None:
                continue
            checked += 1
            if abs(direct - derived) > 1e6:
                bad.append((k, e, direct, derived))
    # 인수손익 두 체계 대조(FY2022·2023)
    uw_cmp = {}
    for y in (2022, 2023):
        def sysval(system):
            name = ("IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"
                    if system == "new" else "OperatingIncomeLoss")
            vals = []
            for sg in SUBGROUPS:
                if system == "new":
                    pr = lambda d, sg=sg: sg in d and "UnderwritingMember" in d and set(d) <= {sg, "UnderwritingMember", "BerkshireHathawayInsuranceGroupMember", "OperatingSegmentsMember"}
                else:
                    pr = lambda d, sg=sg: sg in d and "InvestmentIncomeMember" not in d and set(d) <= {sg, "BerkshireHathawayInsuranceGroupMember", "OperatingSegmentsMember", "PremiumsEarnedNetMember", "InsuranceUnderwritingMember"}
                vals.append(pick(name, pr, f"{y}-01-01", f"{y}-12-31", None))
            return sum(vals) if all(v is not None for v in vals) else None
        uw_cmp[y] = (sysval("old"), sysval("new"))
    uw_ok = all(o is not None and n is not None and abs(o - n) <= 0.01 * abs(o) for o, n in uw_cmp.values())
    return {"checked": checked, "mismatch": bad, "uw_systems": uw_cmp, "uw_ok": uw_ok}


def text_of(doc):
    t = re.sub(r"<[^>]+>", " ", open(os.path.join(RAW, doc), encoding="utf-8", errors="ignore").read())
    return re.sub(r"\s+", " ", html.unescape(t))


def tenk_doc(fy):
    docs = sorted({(f["filed"], f["doc"]) for f in FACTS if f["form"] == "10-K" and f.get("report") == f"{fy}-12-31"})
    return docs[0][1] if docs else None


def company_table(fy):
    """10-K MD&A '순이익 세그먼트 분해' 표(세후, 첫 열 = 그 회계연도)."""
    t = text_of(tenk_doc(fy))
    i = t.find("disaggregated in the table that follows")
    seg = t[i:i + 1500]
    num = lambda s: -float(s.strip("() ").replace(",", "")) if "(" in s else float(s.replace(",", ""))
    rows = {}
    for label, key in [(r"Insurance – underwriting", "uw"), (r"Insurance – investment income", "invinc"),
                       (r"Investment (?:and derivative gains/losses|gains \(losses\)|and derivative contract gains \(losses\))", "gains"),
                       (r"Other-than-temporary impairment[^$\d(]*", "otti"),
                       (r"Net earnings(?: \(loss\))? attributable to Berkshire[^$]*shareholders", "ni")]:
        m = re.search(label + r"\s*\$?\s*(\(?[\d,]+\s*\)?|—)", seg)
        rows[key] = (0.0 if m.group(1) == "—" else num(m.group(1)) * 1e6) if m else None
    return rows


def g2():
    out = {}
    for fy in range(2019, 2026):
        e = f"{fy}-12-31"
        ct = company_table(fy)
        ni, g, d = ytd("ni", fy, e, None), ytd("gains", fy, e, None), ytd("deriv", fy, e, None)
        otti, imp_at = ytd("otti", fy, e, None), impairment_after_tax(e, None)
        ours = ni - (g + d) * (1 - TAX) + (imp_at or 0) + otti * (1 - TAX)
        company = ct["ni"] - (ct["gains"] or 0) - (ct.get("otti") or 0)
        tax_tag = pick("GainLossOnInvestmentsAndGainLossOnDerivativeInstrumentsTax", lambda dd: True, f"{fy}-01-01", e, None)
        adj1 = imp_at or 0
        adj2 = ((g + d) - tax_tag - (g + d) * (1 - TAX)) if tax_tag is not None else 0.0
        adj3 = (otti * (1 - TAX) - (-(ct.get("otti") or 0))) if otti else 0.0
        resid = (ours - company) - adj1 - adj2 - adj3
        out[fy] = {"ours": ours, "company": company, "adj_imp": adj1, "adj_gain_tax": adj2, "adj_otti_tax": adj3,
                   "resid": resid, "resid_pct": resid / abs(company), "tax_tag": tax_tag is not None,
                   "invinc_ours_at": ytd("invinc", fy, e, None) * (1 - TAX), "invinc_company": ct["invinc"],
                   "uw_ours_at": (ytd("uw", fy, e, None) or 0) * (1 - TAX), "uw_company": ct["uw"]}
    return out


def g3():
    out = {}
    for fy in range(2020, 2025):
        e = f"{fy}-12-31"
        t = text_of(tenk_doc(fy))
        m = re.search(r"insurance and other businesses held cash, cash equivalents and U\.S\. Treasury Bills( \(net of payables for unsettled purchases\))? of \$([\d.]+) billion", t)
        cash = balance("CashAndCashEquivalentsAtCarryingValue", IO, e, None)
        tb = balance("USTreasuryBills", IO, e, None)
        pay = balance("PayableForPurchaseOfUSTreasuryBills", IO, e, None) or 0.0
        net = bool(m and m.group(1))
        ours = cash + tb - (pay if net else 0.0)
        company = float(m.group(2)) * 1e9 if m else None
        # 주식 수: 기말 A주 환산 vs 10-K 표지 클래스별(표지 기준일)
        sh = balance("CommonStockSharesOutstanding", ["EquivalentClassAMember"], e, None)
        doc = tenk_doc(fy)
        cov = [f for f in FACTS if f["doc"] == doc and f["name"] == "EntityCommonStockSharesOutstanding"]
        a = next((f["val"] for f in cov if "CommonClassAMember" in f["dims"]), None)
        b = next((f["val"] for f in cov if "CommonClassBMember" in f["dims"]), None)
        cover = a + b / 1500 if a is not None and b is not None else None
        out[fy] = {"ours_cash_tb": ours, "company_cash_tb": company, "net_of_payables": net,
                   "cash_pct": (ours - company) / company if company else None,
                   "shares_end": sh, "shares_cover": cover, "shares_pct": (sh - cover) / cover if cover else None}
    return out


# ── 가격·기술 통계 ───────────────────────────────────────────────────────
def prices():
    path = os.path.join(V2, ".sec_cache", "brkb_prices.json")
    if not os.path.exists(path):
        t0 = int(dt.datetime(2019, 12, 1).timestamp())
        t1 = int(dt.datetime(2026, 9, 26).timestamp())
        raw = subprocess.run(["curl", "-s", "-A", "Mozilla/5.0",
                              f"https://query1.finance.yahoo.com/v8/finance/chart/BRK-B?period1={t0}&period2={t1}&interval=1d"],
                             capture_output=True, text=True).stdout
        r = json.loads(raw)["chart"]["result"][0]
        rows = [(dt.datetime.fromtimestamp(ts, dt.timezone.utc).date().isoformat(), c) for ts, c in
                zip(r["timestamp"], r["indicators"]["quote"][0]["close"]) if c]
        json.dump(rows, open(path, "w"))
    return json.load(open(path))


def close_on(rows, day):
    c = [x for x in rows if x[0] <= day]
    return c[-1][1] if c else None


def spearman(a, b):
    import numpy as np
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    # 동점은 평균 순위
    def avg_rank(x):
        x = np.asarray(x, float)
        order = np.argsort(x)
        ranks = np.empty(len(x))
        i = 0
        while i < len(x):
            j = i
            while j + 1 < len(x) and x[order[j + 1]] == x[order[i]]:
                j += 1
            ranks[order[i:j + 1]] = (i + j) / 2
            i = j + 1
        return ranks
    ra, rb = avg_rank(a), avg_rank(b)
    return float(np.corrcoef(ra, rb)[0, 1])


def describe(series, px):
    import numpy as np
    pts = [s for s in series if "iv" in s and s["t"] not in ("2020-09-30", "2024-09-30") and s["t"] <= "2026-03-31"]
    rows = []
    for s in pts:
        e = s["t"]
        nq = qends(first=e, last="2026-06-30")[1] if len(qends(first=e, last="2026-06-30")) > 1 else None
        if nq is None:
            continue
        bb = quarter_value("buyback", nq, None)
        p = close_on(px, e)
        mcap = p * s["sharesB"]
        rows.append({"t": e, "ratio": p / s["iv"], "pb": p / s["bvps"] if s["bvps"] else None,
                     "bb_mcap": (bb or 0) / mcap, "bb_p1": (bb or 0) / s["p1"]})
    r = [x["ratio"] for x in rows]
    pb = [x["pb"] for x in rows]
    bm = [x["bb_mcap"] for x in rows]
    bp = [x["bb_p1"] for x in rows]
    rho, rho_pb = spearman(r, bm), spearman(pb, bm)
    rng = np.random.default_rng(7)
    diffs = []
    n = len(rows)
    for _ in range(5000):
        idx = []
        while len(idx) < n:
            st = rng.integers(0, n)
            idx += [(st + k) % n for k in range(4)]
        idx = idx[:n]
        a = [r[i] for i in idx]
        b = [pb[i] for i in idx]
        c = [bm[i] for i in idx]
        if len(set(c)) < 2:
            continue
        diffs.append(spearman(a, c) - spearman(b, c))
    lo, hi = (float(np.percentile(diffs, 5)), float(np.percentile(diffs, 95))) if diffs else (None, None)
    nz = [i for i in range(n) if bm[i] > 0]
    return {"n": n, "rho": rho, "rho_pb": rho_pb, "diff": rho - rho_pb, "diff_ci90": [lo, hi],
            "rho_nonzero": spearman([r[i] for i in nz], [bm[i] for i in nz]) if len(nz) > 3 else None,
            "n_nonzero": len(nz), "rho_bb_p1": spearman(r, bp), "rows": rows}


def main():
    px = prices()
    series = []
    for t in qends(first="2020-03-31", last="2026-06-30"):
        s = pillars(t)
        p = close_on(px, t)
        if "iv" in s:
            s["price"] = p
            s["ratio"] = p / s["iv"]
        series.append(s)
    res = {"g1": g1(), "g2": g2(), "g3": g3(), "series": series}
    evals = [s for s in series]
    abst = [s for s in evals if "abstain" in s]
    res["abstain_rate"] = len(abst) / len(evals)
    res["describe"] = describe(series, px)
    return res


if __name__ == "__main__":
    res = main()
    out = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
    if out:
        json.dump(res, open(out, "w"), ensure_ascii=False, indent=1, default=str)
    g1r, g2r, g3r = res["g1"], res["g2"], res["g3"]
    print("G1 대조", g1r["checked"], "건 · 불일치", len(g1r["mismatch"]), g1r["mismatch"][:5], "· 인수 두 체계", g1r["uw_systems"], "ok" if g1r["uw_ok"] else "실패")
    print("기권 비율", f"{res['abstain_rate']:.0%}", [(s["t"], s["abstain"]) for s in res["series"] if "abstain" in s])
    for fy, v in g2r.items():
        print("G2", fy, f"ours {v['ours']/1e9:.2f} company {v['company']/1e9:.2f} resid {v['resid']/1e9:+.2f} ({v['resid_pct']:+.1%}) tax_tag {v['tax_tag']}",
              f"| 투자수익 ours {v['invinc_ours_at']/1e9:.2f} co {v['invinc_company']/1e9 if v['invinc_company'] else None} | 인수 ours {v['uw_ours_at']/1e9:.2f} co {v['uw_company']/1e9 if v['uw_company'] else None}")
    for fy, v in g3r.items():
        print("G3", fy, v)
