#!/usr/bin/env python3
"""은행 심사 세트 — research/bank_rim_prereg.md 3판 구현(JPM 첫 적용).

    python3 v2/adapters/bank_rim.py JPM --gates                 # 관문 G1~G5
    python3 v2/adapters/bank_rim.py JPM --json v2/JPM_bank.json # RIM·배수·동종업·격자 전부

정의는 사전 등록 문서가 원본이다. 모든 값은 평가 시점까지 접수된 SEC 사실만 쓴다(같은 기간은 가장 먼저 접수된 값,
그 값 자신의 접수일이 가용일). 회사 공시 대조값(관문)은 실적 보도자료에서 옮긴 v2/research/bank_gate_JPM.json을 읽는다.
"""
import json
import os
import statistics
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
sys.path.insert(0, V2)
sys.path.insert(0, os.path.join(REPO, "scripts"))
import build_multiple_history as bmh  # noqa: E402

R, G_CAP, FADE = 0.10, 0.025, 0.5
ITEMS = os.path.join(V2, "bank_items.json")
# 자사주 매입 현금 태그가 다른 은행. MS는 현금흐름표 "Repurchases of common stock"을 StockRepurchasedDuringPeriodValue로 낸다
# (PaymentsForRepurchaseOfCommonStock은 2013년에 멈춤, 2026-10-01). 우선주 잔액은 회사 고유 태그라 adapters/ms_preferred.py가 overlay에 싣는다.
BUY_TAGS = {"MS": ["StockRepurchasedDuringPeriodValue"]}
# 보통주 배당 현금을 PaymentsOfDividendsCommonStock 대신 다른 태그로 내는 은행(BAC: DividendsCommonStockCash, 2026-10-01)
DIV_COM_TAGS = {"BAC": ["DividendsCommonStockCash"]}


# ── 사실 읽기 ────────────────────────────────────────────────────────────
def _facts(cik, tag):
    u = bmh._facts(cik).get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {})
    return u.get("USD") or u.get("shares") or []


def instant(cik, tag, asof=None):
    """{결산일: (값, 접수일)} — 시점 사실, asof 이전 접수만, 같은 결산일은 가장 먼저 접수된 값."""
    out = {}
    for f in _facts(cik, tag):
        if "start" in f or (asof and f["filed"] > asof):
            continue
        if f["end"] not in out or f["filed"] < out[f["end"]][1]:
            out[f["end"]] = (f["val"], f["filed"])
    return out


def ever(cik, tag):
    return bool(_facts(cik, tag))


def flow_q(cik, tags, ticker, asof=None):
    """{분기말: (분기값, 가용일)} — 카드 엔진 quarterly_flow(누적 차분). asof 이전 접수 사실만."""
    _, rows = bmh.pick_tag(cik, tags)
    if asof:
        rows = [r for r in rows if r["filed"] <= asof]
    # 분기말이 3·6·9·12월 말이 아닌 값(GS의 2008년 이전 11월 결산 시절 등)은 쓰지 않는다(2026-10-01)
    q = {e["end"]: (e["val"], e["filed"]) for e in bmh.quarterly_flow(rows, ticker)
         if e["end"][5:] in ("03-31", "06-30", "09-30", "12-31")}
    # 누적 차분으로 만든 분기값의 가용일은 두 누적값 접수일 중 늦은 날이다(7-2, Codex). 같은 회계연도의
    # 직전 분기 사실 접수일까지 포함해 늦은 쪽으로 잡는다(보수적).
    out = {}
    for e, (v, f) in q.items():
        prev = qends_before(e, 1)[0]
        pf = q.get(prev, (None, f))[1] if not e.endswith("03-31") else f
        out[e] = (v, max(f, pf))
    return out


def qends_before(end, n):
    y, m = int(end[:4]), int(end[5:7])
    out = []
    for _ in range(n):
        m -= 3
        if m <= 0:
            m += 12
            y -= 1
        d = {3: 31, 6: 30, 9: 30, 12: 31}[m]
        out.append(f"{y}-{m:02d}-{d}")
    return out


# ── 1장 정의 ─────────────────────────────────────────────────────────────
_SO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "research", "bank_shares_override.json")
SHARES_OVERRIDE = {k: v for k, v in json.load(open(_SO)).items() if not k.startswith("_")} if os.path.exists(_SO) else {}


_EO = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "research", "bank_equity_override.json")
EQUITY_OVERRIDE = {k: v for k, v in json.load(open(_EO)).items() if not k.startswith("_")} if os.path.exists(_EO) else {}


# 우선주 장부·청산가 태그가 0·없음인데 우선주가 있는 회사 — 청산가 = 발행 우선주 수 × 주당 상환가(10-K). AXP: 1,600주 × $1,000,000
# = $1.6B(재무상태표 우선주 장부가 "—", 회사 BVPS는 이를 뺀 값, 2026-10-01). 종목별로만 적용한다.
PREF_PRICE = {"AXP": 1_000_000}


class Bank:
    def __init__(self, ticker, cik, asof=None, overrides=False):
        # overrides: 회사 정의 주식 수·자본 예외(GS·WFC)는 그 종목 카드에서만 쓴다 — 동종업 계산에 넣으면 커밋된 다른 은행 카드 점수가 바뀐다
        self.t, self.cik, self.asof, self.ov = ticker, cik, asof, overrides
        c = cik
        self.se = instant(c, "StockholdersEquity", asof)
        self.pref_liq = instant(c, "PreferredStockLiquidationPreferenceValue", asof)
        self.pref_val = instant(c, "PreferredStockValue", asof)
        self.pref_ever = ever(c, "PreferredStockLiquidationPreferenceValue") or ever(c, "PreferredStockValue")
        self.pref_sh = instant(c, "PreferredStockSharesOutstanding", asof) if ticker in PREF_PRICE else {}
        self.gw = instant(c, "Goodwill", asof)
        self.ia = instant(c, "IntangibleAssetsNetExcludingGoodwill", asof)
        self.fin = instant(c, "FiniteLivedIntangibleAssetsNet", asof)
        self.ind = instant(c, "IndefiniteLivedIntangibleAssetsExcludingGoodwill", asof)
        self.oth = instant(c, "OtherIntangibleAssetsNet", asof)
        self.fin_ever, self.ind_ever = ever(c, "FiniteLivedIntangibleAssetsNet"), ever(c, "IndefiniteLivedIntangibleAssetsExcludingGoodwill")
        self.issued = instant(c, "CommonStockSharesIssued", asof)
        self.tr = {**instant(c, "TreasuryStockShares", asof), **instant(c, "TreasuryStockCommonShares", asof)}
        self.cso = instant(c, "CommonStockSharesOutstanding", asof)
        self.ni = flow_q(c, ["NetIncomeLossAvailableToCommonStockholdersBasic"], ticker, asof)
        self.div_all = flow_q(c, ["PaymentsOfDividends"], ticker, asof)
        self.div_com = flow_q(c, DIV_COM_TAGS.get(ticker, ["PaymentsOfDividendsCommonStock"]), ticker, asof)
        self.div_pref = flow_q(c, ["DividendsPreferredStock"], ticker, asof)
        self.buy = flow_q(c, BUY_TAGS.get(ticker, ["PaymentsForRepurchaseOfCommonStock"]), ticker, asof)
        self.iss = flow_q(c, ["ProceedsFromIssuanceOfCommonStock"], ticker, asof)
        self.iss_ever = ever(c, "ProceedsFromIssuanceOfCommonStock")
        wd = {}
        for f in _facts(c, "WeightedAverageNumberOfDilutedSharesOutstanding"):
            if "start" not in f or (asof and f["filed"] > asof):
                continue
            days = (date.fromisoformat(f["end"]) - date.fromisoformat(f["start"])).days
            if 80 <= days <= 100 and (f["end"] not in wd or f["filed"] < wd[f["end"]][1]):
                wd[f["end"]] = (f["val"], f["filed"])
        self.wdil = wd
        items = json.load(open(ITEMS)).get(ticker, {}) if os.path.exists(ITEMS) else {}
        self.items = {k: v for k, v in items.items() if not asof or v["filed"] <= asof}

    # 1-1
    def ce(self, end):
        o = EQUITY_OVERRIDE.get(self.t, {}).get(end) if self.ov else None   # WFC 한정 예외: 보도자료 회사 정의 CE(research/bank_equity_override.json)
        if o and not (self.asof and o["filed"] > self.asof):
            return (o["ce_m"] * 1e6, o["filed"])
        if end not in self.se:
            return None
        p = self.pref_liq.get(end) or self.pref_val.get(end)
        if self.t in PREF_PRICE and end in self.pref_sh:   # 종목 예외(AXP) — 발행 우선주 수 × 주당 상환가
            p = (self.pref_sh[end][0] * PREF_PRICE[self.t], self.pref_sh[end][1])
        if p is None:
            if self.pref_ever:
                return None
            p = (0, self.se[end][1])
        v = self.se[end][0] - p[0]
        return (v, max(self.se[end][1], p[1])) if v > 0 else None

    # 1-2 (+7-6)
    def tce(self, end):
        o = EQUITY_OVERRIDE.get(self.t, {}).get(end) if self.ov else None   # WFC 한정 예외: 보도자료 회사 정의 TCE
        if o and not (self.asof and o["filed"] > self.asof):
            return (o["tce_m"] * 1e6, o["filed"])
        c = self.ce(end)
        if not c or end not in self.gw:
            return None
        if end in self.ia:
            ia = self.ia[end]
        elif end in self.fin or end in self.ind:
            f = self.fin.get(end) or ((0, "") if not self.fin_ever else None)
            i = self.ind.get(end) or ((0, "") if not self.ind_ever else None)
            if f is None or i is None:
                return None
            ia = (f[0] + i[0], max(f[1], i[1]))
        elif end in self.oth:
            ia = self.oth[end]
        else:
            ia = self._carry_intangibles(end)   # 4판 8-1: 직전 값을 400일까지 이어 쓴다
            if ia is None:
                return None
        v = c[0] - self.gw[end][0] - ia[0]
        return (v, max(c[1], self.gw[end][1], ia[1]))

    def _carry_intangibles(self, end):
        """그 결산일 이전 가장 최근 무형자산 값(1-2 우선순위), 400일 이내만(사전 등록 8-1)."""
        cands = []
        for e in set(self.ia) | set(self.fin) | set(self.ind) | set(self.oth):
            if e >= end or (date.fromisoformat(end) - date.fromisoformat(e)).days > 400:
                continue
            if e in self.ia:
                v = self.ia[e]
            elif e in self.fin or e in self.ind:
                f = self.fin.get(e) or ((0, "") if not self.fin_ever else None)
                i = self.ind.get(e) or ((0, "") if not self.ind_ever else None)
                if f is None or i is None:
                    continue
                v = (f[0] + i[0], max(f[1], i[1]))
            else:
                v = self.oth[e]
            cands.append((e, v))
        return max(cands)[1] if cands else None

    # 1-6 (GS·WFC 예외: research/bank_shares_override.json의 회사 정의 주식 수 — GS 사용자 결정, WFC Claude 추천 결정, 2026-10-01. 본인 카드만)
    def shares(self, end):
        o = SHARES_OVERRIDE.get(self.t, {}).get(end) if self.ov else None
        if o and not (self.asof and o["filed"] > self.asof):
            return (o["shares_m"] * 1e6, o["filed"])
        if end in self.issued and end in self.tr:
            v = self.issued[end][0] - self.tr[end][0]
            return (v, max(self.issued[end][1], self.tr[end][1])) if v > 0 else None
        if end in self.cso and self.cso[end][0] > 0:
            return self.cso[end]
        return None

    def quarters(self):
        return sorted(e for e in self.ni if e.endswith(("03-31", "06-30", "09-30", "12-31")))

    def ttm(self, series, end):
        ks = [end] + qends_before(end, 3)
        if not all(k in series for k in ks):
            return None
        return (sum(series[k][0] for k in ks), max(series[k][1] for k in ks))

    def item_adj(self, end):
        """특별 항목 NI 조정액(세후, 보통주). 확인 안 한 분기면 None."""
        if end not in self.items:
            return None
        its = self.items[end]["items"]
        # 7-5: ① 항목별 EPS × 희석 주식 수 ② 회사가 밝힌 세후 보통주 금액 ③ 둘 다 없으면 조정 불가(0, 표시)
        direct = sum(i["ni"] for i in its if "eps" not in i and "ni" in i)
        self.unadjustable = getattr(self, "unadjustable", set()) | {end for i in its if "eps" not in i and "ni" not in i}
        eps = sum(i["eps"] for i in its if "eps" in i)
        if not eps:
            return float(direct)
        wd = self.wdil.get(end)
        if wd is None and self.items[end].get("wdil"):   # 4판 8-2: 4분기는 보충자료 손입력
            wd = (self.items[end]["wdil"], self.items[end]["filed"])
        return None if wd is None else eps * wd[0] + direct

    def ni_ttm(self, end, adjusted=False):
        t = self.ttm(self.ni, end)
        if not t or not adjusted:
            return t
        adj = [self.item_adj(k) for k in [end] + qends_before(end, 3)]
        if any(a is None for a in adj):
            return None
        wd_f = [self.wdil[k][1] for k in [end] + qends_before(end, 3) if k in self.wdil]
        return (t[0] - sum(adj), max([t[1]] + [self.items[k]["filed"] for k in [end] + qends_before(end, 3)] + wd_f))

    # 1-4 관측 ROE = NI_TTM ÷ 기초 CE
    def roe(self, end, adjusted=False):
        n = self.ni_ttm(end, adjusted)
        b = self.ce(qends_before(end, 4)[-1])
        if not n or not b:
            return None
        return (n[0] / b[0], max(n[1], b[1]))

    # 1-7 (+7-3)
    def payout_ttm(self, end):
        div = self.ttm(self.div_com, end)
        if div is None:
            a, p = self.ttm(self.div_all, end), self.ttm(self.div_pref, end)
            if a is None or p is None:
                return None
            div = (a[0] - p[0], max(a[1], p[1]))
        buy = self.ttm(self.buy, end)
        if buy is None:
            return None
        # 발행 태그가 없거나 그 4분기에 끊겼으면 0(1-7 — 임직원 주식보상 발행은 현금이 아니다)
        iss = self.ttm(self.iss, end) or (0.0, div[1])
        return (div[0] + buy[0] - iss[0], max(div[1], buy[1], iss[1]))

    def retention(self, end):
        n = self.ni_ttm(end, adjusted=True)
        p = self.payout_ttm(end)
        if not n or not p or n[0] <= 0:
            return None
        return (min(max(1 - p[0] / n[0], 0.0), 1.0), max(n[1], p[1]))

    def latest_quarter(self):
        """평가 시점까지 접수된 가장 최근 분기말. 그 분기의 RIM 입력이 모자라면 None(기권) —
        더 오래된 분기로 내려가지 않는다(Codex, 8-3과 같은 원칙)."""
        if not self.se:
            return None
        e = max(self.se)
        return e if (self.ce(e) and self.shares(e) and self.roe(e) and self.retention(e)) else None


# ── 2장 RIM ─────────────────────────────────────────────────────────────
def rim_value(B0, roe0, roe_end, b, r=R, lam=FADE, years=5):
    B, pv = B0, 0.0
    for i in range(1, years + 1):
        roe = roe0 + (roe_end - roe0) * i / years
        pv += (roe - r) * B / (1 + r) ** i
        B = B * (1 + roe * b)
    roe5 = roe_end
    roe_t = r + (roe5 - r) * (1 - lam) if roe5 > r else roe5
    b_t = min(b, G_CAP / roe_t) if roe_t > 0 else b
    g_t = roe_t * b_t
    if r - g_t <= 0:
        return None
    tv = (roe_t - r) * B / (r - g_t)
    return B0 + pv + tv / (1 + r) ** years


def required_roe(B0, b, target, r=R, lam=FADE):
    lo, hi = 0.0, 0.60
    f = lambda x: rim_value(B0, x, x, b, r, lam)
    flo, fhi = f(lo), f(hi)
    if flo is None or fhi is None or not (flo <= target <= fhi):
        return None
    for _ in range(80):
        mid = (lo + hi) / 2
        if f(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def rim(bank, price=None):
    L = bank.latest_quarter()
    if not L:
        return {"abstain": "RIM 입력 없음"}
    ce, S = bank.ce(L)[0], bank.shares(L)[0]
    roe0 = bank.roe(L, adjusted=True)
    b = bank.retention(L)[0]
    if roe0 is None:
        return {"abstain": "출발 TTM에 특별 항목 미확인 분기", "L": L}
    roe0 = roe0[0]
    hist = [bank.roe(e) for e in [L] + qends_before(L, 19)]
    h20 = [x[0] for x in hist if x]
    h8 = [x[0] for x in hist[:8] if x]
    out = {"L": L, "ce": ce, "shares": S, "bvps": ce / S, "roe0": roe0, "roe0_gaap": bank.roe(L)[0], "b": b,
           "roe_5y_median": statistics.median(h20) if len(h20) >= 16 else None,
           "roe_2y_median": statistics.median(h8) if len(h8) >= 6 else None, "n20": len(h20), "n8": len(h8)}
    ends = {"보수": out["roe_5y_median"], "기본": out["roe_2y_median"], "낙관": roe0}
    for name, re_ in ends.items():
        v = rim_value(ce, roe0, re_, b) if re_ is not None else None
        out[name] = v / S if v is not None else None
    if price is not None:
        rq = required_roe(ce, b, price * S)
        out["required_roe"] = rq
    grid = {}
    for r in (0.08, 0.09, 0.10, 0.11, 0.12):
        for lam in (0.0, 0.5, 1.0):
            v = rim_value(ce, roe0, ends["기본"], b, r, lam) if ends["기본"] is not None else None
            grid[f"{r:.2f}|{lam}"] = v / S if v is not None else None
    out["grid"] = grid
    return out


# ── 3장 배수(현재값) ─────────────────────────────────────────────────────
def eps_ttm(ticker, day, eps_path):
    pts = json.load(open(eps_path))
    cur = None
    for p in pts:
        if p["available_date"] <= day:
            cur = p["ttm_eps"]
    return cur


def multiples_on(bank, day, close, eps_path):
    """그날 공시된 가장 최근 분기말 기준 P/TBV·PER. 분모 ≤ 0이면 'negative'."""
    out = {}
    # 그날 접수된 가장 최근 분기말 하나만 본다. 그 분기의 TCE를 못 만들거나 200일 넘게 낡았으면 P/TBV 없음
    # — 더 오래된 분기로 내려가지 않는다(PNC 2016·WFC 2021 값이 쓰였다, 결과를 본 뒤 개정 8-3).
    avail = [e for e in bank.se if bank.se[e][1] <= day]
    if avail:
        e = max(avail)
        t, s = bank.tce(e), bank.shares(e)
        fresh = (date.fromisoformat(day) - date.fromisoformat(e)).days <= 200
        if t and s and fresh and t[1] <= day and s[1] <= day:
            out["ptbv"] = (close * s[0] / t[0]) if t[0] > 0 else "negative"
            out["ptbv_end"] = e
        else:
            out["ptbv_missing"] = (f"분기말 {e}가 200일 넘게 낡음(SEC companyfacts 미반영)" if not fresh
                                   else f"분기말 {e}의 유형자본을 만들 수 없음(우선주·무형자산 태그, 1-1·1-2·8-1)")
    if eps_path and os.path.exists(eps_path):
        eps = eps_ttm(bank.t, day, eps_path)
        if eps is not None:
            out["per"] = close / eps if eps > 0 else "negative"
    return out


if __name__ == "__main__":
    print("라이브러리 — 실행 스크립트는 v2/adapters/bank_card.py")


# ── 4장 관문 ─────────────────────────────────────────────────────────────
GATE_Q = ["2024-09-30", "2024-12-31", "2025-03-31", "2025-06-30", "2025-09-30", "2025-12-31", "2026-03-31", "2026-06-30"]
GATE_Y = ["2021", "2022", "2023", "2024", "2025"]


def ytd_diff_q(bank, tag, end):
    """G5용 — 3개월 직접 공시값을 쓰지 않고 연초 누적(10-Q·10-K)끼리 뺀 분기값."""
    y = end[:4]
    start = f"{y}-01-01"
    cum = {}
    for f in _facts(bank.cik, tag):
        if f.get("start") == start and f["end"].startswith(y) and (f["end"] not in cum or f["filed"] < cum[f["end"]]["filed"]):
            cum[f["end"]] = f
    if end not in cum:
        return None
    if end.endswith("03-31"):
        return cum[end]["val"]
    prev = qends_before(end, 1)[0]
    return None if prev not in cum else cum[end]["val"] - cum[prev]["val"]


def gates(bank, gate_path):
    g = json.load(open(gate_path))
    missing = [q for q in GATE_Q if q not in g["quarters"]] + [y for y in GATE_Y if y not in g["years"]]
    g["quarters"] = {q: g["quarters"].get(q, {}) for q in GATE_Q}
    g["years"] = {y: g["years"].get(y, {}) for y in GATE_Y}
    res = {"missing_targets": missing}
    rows1, rows2, rows5 = [], [], []
    for q, v in sorted(g["quarters"].items()):
        ce, t, s = bank.ce(q), bank.tce(q), bank.shares(q)
        tb = t[0] / s[0] if t and s else None
        bv = ce[0] / s[0] if ce and s else None
        c1, c2, c3, c5 = v.get("tbvps"), v.get("bvps"), v.get("ce_m"), v.get("ni_common_m")
        rows1.append((q, tb, c1, None if tb is None or not c1 else tb / c1 - 1))
        rows2.append((q, bv, c2, None if bv is None or not c2 else bv / c2 - 1,
                      None if not ce or not c3 else ce[0] / 1e6 / c3 - 1))
        nq = ytd_diff_q(bank, "NetIncomeLossAvailableToCommonStockholdersBasic", q)   # 누적 차분(Codex)
        rows5.append((q, nq and nq / 1e6, c5, None if nq is None or c5 is None else nq / 1e6 - c5))
    res["G1"] = {"rows": rows1, "pass": all(r[3] is not None and abs(r[3]) <= 0.015 for r in rows1)}
    res["G2"] = {"rows": rows2, "pass": all(r[3] is not None and r[4] is not None and abs(r[3]) <= 0.005 and abs(r[4]) <= 0.005 for r in rows2)}
    res["G5"] = {"rows": rows5, "pass": all(r[3] is not None and abs(r[3]) <= 50 for r in rows5)}
    rows3 = []
    ann = {}
    for f in _facts(bank.cik, "NetIncomeLossAvailableToCommonStockholdersBasic"):
        if f.get("form") == "10-K" and "start" in f and f["end"].endswith("12-31") and \
                350 <= (date.fromisoformat(f["end"]) - date.fromisoformat(f["start"])).days <= 380:
            if f["end"] not in ann or f["filed"] < ann[f["end"]]["filed"]:
                ann[f["end"]] = f
    for fy, v in sorted(g["years"].items()):
        end = f"{fy}-12-31"
        ours = bank.ttm(bank.ni, end)
        ces = [bank.ce(e) for e in [end] + qends_before(end, 4)]
        k = ann.get(end)
        roe = ours[0] / (sum(c[0] for c in ces) / 5) if ours and all(ces) else None
        rows3.append((fy, ours and ours[0] / 1e6, k and k["val"] / 1e6, v.get("ni_common_m"), roe, v.get("roe")))
    res["G3"] = {"rows": rows3, "pass": all(r[1] is not None and r[2] is not None and abs(r[1] - r[2]) <= 50
                                            and r[4] is not None and r[5] is not None and abs(r[4] - r[5]) <= 0.015 for r in rows3)}
    rows4 = []
    for q, v in sorted(g["quarters"].items()):
        n, p = bank.ni_ttm(q), bank.payout_ttm(q)
        ours = p[0] / n[0] if n and p and n[0] > 0 else None
        cv = v.get("net_payout_ltm")
        rows4.append((q, ours, cv, None if ours is None or cv is None else ours - cv))
    res["G4"] = {"rows": rows4, "pass": all(r[3] is not None and abs(r[3]) <= 0.10 for r in rows4)}
    if missing:
        for k in ("G1", "G2", "G3", "G4", "G5"):
            res[k]["pass"] = False
    return res
