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
# 사전 등록 판 — 7판(11절, 10-Q 정의로 통일·보도자료 손입력 없음)은 사용자가 결과를 보고 적용을 정할 때까지 BANK_EDITION=7로만 켠다(2026-10-11)
EDITION = int(os.environ.get("BANK_EDITION", "6"))
_ST = os.path.join(V2, "research", "bank_sec_tags.json")
_SV = os.path.join(V2, "research", "bank_sec_values.json")
SEC_TAGS = json.load(open(_ST)) if os.path.exists(_ST) else {"preferred": {}, "cet1": {"_default": {"tag": ""}}}
SEC_VALUES = json.load(open(_SV)) if os.path.exists(_SV) else {}
ACK = os.path.join(V2, "research", "bank_ack.json")   # 7판 N4 — 사람이 확인한 급변 분기 {은행: {분기말: 사유}}
# 자사주 매입 현금 태그가 다른 은행. MS는 현금흐름표 "Repurchases of common stock"을 StockRepurchasedDuringPeriodValue로 낸다
# (PaymentsForRepurchaseOfCommonStock은 2013년에 멈춤, 2026-10-01). 우선주 잔액은 회사 고유 태그라 adapters/ms_preferred.py가 overlay에 싣는다.
BUY_TAGS = {"MS": ["StockRepurchasedDuringPeriodValue"]}
# 보통주 배당 현금을 PaymentsOfDividendsCommonStock 대신 다른 태그로 내는 은행(BAC: DividendsCommonStockCash, 2026-10-01)
DIV_COM_TAGS = {"BAC": ["DividendsCommonStockCash"],
                "SCHW": ["DividendsCommonStockCash"]}   # SCHW: PaymentsOfDividends − DividendsPreferredStock 폴백의 우선주 태그가 없다(…Cash로만), BAC와 같은 선언 기준(2026-10-01)


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


def ever(cik, tag, asof=None):
    """그 태그가 평가일까지 한 번이라도 접수됐는가 — 7판 11-0: 미래 행을 보지 않는다(6판까지는 asof 없이 썼다)."""
    return any(not asof or f["filed"] <= asof for f in _facts(cik, tag))


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
    def __init__(self, ticker, cik, asof=None, overrides=False, edition=None):
        # overrides: 회사 정의 주식 수·자본 예외(GS·WFC)는 그 종목 카드에서만 쓴다 — 동종업 계산에 넣으면 커밋된 다른 은행 카드 점수가 바뀐다
        self.ed = edition or EDITION
        if self.ed >= 7:   # 7판 11-1: 회사 정의 보정 폐지
            overrides = False
        self.t, self.cik, self.asof, self.ov = ticker, cik, asof, overrides
        c = cik
        # 7판: 원문 인라인 XBRL 값(adapters/bank_sec_values.py) — 평가일까지 접수된 공시의 것만(11-0)
        self.secv = {e: r for e, r in SEC_VALUES.get(ticker, {}).items() if not asof or r["filed"] <= asof} if self.ed >= 7 else {}
        self.pref_tbl = SEC_TAGS["preferred"].get(ticker) if self.ed >= 7 else None
        self.se = instant(c, "StockholdersEquity", asof)
        self.pref_liq = instant(c, "PreferredStockLiquidationPreferenceValue", asof)
        self.pref_val = instant(c, "PreferredStockValue", asof)
        self.pref_ever = (ever(c, "PreferredStockLiquidationPreferenceValue", asof if self.ed >= 7 else None)
                          or ever(c, "PreferredStockValue", asof if self.ed >= 7 else None))
        self.pref_sh = instant(c, "PreferredStockSharesOutstanding", asof) if ticker in PREF_PRICE else {}
        self.gw = instant(c, "Goodwill", asof)
        self.ia = instant(c, "IntangibleAssetsNetExcludingGoodwill", asof)
        for e_, r_ in self.secv.items():   # 7판: 원문 값이 더 먼저 접수됐으면(companyfacts가 늦게 싣거나 나중 공시 값으로 바뀐 분기) 원문 값과 그 접수일(Codex 2차)
            for d_, k_ in ((self.se, "se"), (self.gw, "gw")):
                if r_.get(k_) and (e_ not in d_ or r_["filed"] < d_[e_][1]):
                    d_[e_] = (r_[k_], r_["filed"])
        self.fin = instant(c, "FiniteLivedIntangibleAssetsNet", asof)
        self.ind = instant(c, "IndefiniteLivedIntangibleAssetsExcludingGoodwill", asof)
        self.oth = instant(c, "OtherIntangibleAssetsNet", asof)
        _ea = asof if self.ed >= 7 else None
        self.fin_ever, self.ind_ever = ever(c, "FiniteLivedIntangibleAssetsNet", _ea), ever(c, "IndefiniteLivedIntangibleAssetsExcludingGoodwill", _ea)
        self.issued = instant(c, "CommonStockSharesIssued", asof)
        self.tr = {**instant(c, "TreasuryStockShares", asof), **instant(c, "TreasuryStockCommonShares", asof)}
        self.cso = instant(c, "CommonStockSharesOutstanding", asof)
        self.ni = flow_q(c, ["NetIncomeLossAvailableToCommonStockholdersBasic"], ticker, asof)
        self.div_all = flow_q(c, ["PaymentsOfDividends"], ticker, asof)
        self.div_com = flow_q(c, DIV_COM_TAGS.get(ticker, ["PaymentsOfDividendsCommonStock"]), ticker, asof)
        self.div_pref = flow_q(c, ["DividendsPreferredStock"], ticker, asof)
        self.buy = flow_q(c, BUY_TAGS.get(ticker, ["PaymentsForRepurchaseOfCommonStock"]), ticker, asof)
        self.iss = flow_q(c, ["ProceedsFromIssuanceOfCommonStock"], ticker, asof)
        self.iss_ever = ever(c, "ProceedsFromIssuanceOfCommonStock", asof if self.ed >= 7 else None)
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
        if self.pref_tbl is not None and not self.pref_tbl.get("path"):
            return self._ce7(end)
        p = self.pref_liq.get(end) or self.pref_val.get(end)
        if self.t in PREF_PRICE and end in self.pref_sh:   # 종목 예외(AXP) — 발행 우선주 수 × 주당 상환가
            p = (self.pref_sh[end][0] * PREF_PRICE[self.t], self.pref_sh[end][1])
        if p is None:
            if self.pref_ever:
                return None
            p = (0, self.se[end][1])
        v = self.se[end][0] - p[0]
        return (v, max(self.se[end][1], p[1])) if v > 0 else None

    def _pref7(self, end):
        """7판 11-2: 은행별 우선주 장부금액 태그 표(research/bank_sec_tags.json) — companyfacts, 없으면 원문 값. (값, 접수일) 또는 None."""
        for tag in self.pref_tbl.get("tags", []):
            if tag.startswith("us-gaap:"):
                v = instant(self.cik, tag.split(":")[1], self.asof).get(end)
                if v:
                    self._pref_tag = getattr(self, "_pref_tag", {}); self._pref_tag[end] = tag
                    return v
            r = self.secv.get(end)
            if r and r.get("pref") is not None and (r.get("pref_tag") or "").lower() == tag.lower():
                self._pref_tag = getattr(self, "_pref_tag", {}); self._pref_tag[end] = tag
                return (r["pref"], r["filed"])
        return None

    def _ce7(self, end):
        if not self.pref_tbl.get("tags"):   # PNC — 우선주가 자본잉여금에 합쳐져 분리할 수 없다(N5-2와 같은 결과: CE 없음)
            return None
        p = self._pref7(end)
        if p is None:
            any_pref = any(r.get("pref") for r in self.secv.values()) or any(
                instant(self.cik, t.split(":")[1], self.asof) for t in self.pref_tbl["tags"] if t.startswith("us-gaap:"))
            if any_pref:
                return None   # 우선주가 있던 은행인데 이 분기 값이 없다 — 0으로 두지 않는다
            p = (0, self.se[end][1])
        v = self.se[end][0] - p[0]
        return (v, max(self.se[end][1], p[1])) if v > 0 else None

    def _ia_std(self, end):
        if end in self.ia:
            return self.ia[end]
        if end in self.fin or end in self.ind:
            f = self.fin.get(end) or ((0, "") if not self.fin_ever else None)
            i = self.ind.get(end) or ((0, "") if not self.ind_ever else None)
            return None if f is None or i is None else (f[0] + i[0], max(f[1], i[1]))
        return self.oth.get(end)

    def _ia7(self, end):
        """7판 11-3: 표준 태그 → 그 공시의 회사 고유 무형자산 태그 → 그 공시와 직전 네 공시에 무형자산 값이 하나도 없으면 0 → 아니면 400일 이어쓰기."""
        v = self._ia_std(end)
        if v is not None:
            return v
        r = self.secv.get(end)
        if r and r.get("ia") is not None:
            return (r["ia"], r["filed"])
        prev = [end] + qends_before(end, 4)
        if all(e in self.secv and self.secv[e].get("ia") is None and self._ia_std(e) is None for e in prev):
            return (0.0, self.secv[end]["filed"])   # 재무상태표에 따로 표시하지 않음(WFC 2023년 뒤)
        cands = [(e, self._ia_std(e) or ((self.secv[e]["ia"], self.secv[e]["filed"]) if self.secv.get(e, {}).get("ia") is not None else None))
                 for e in sorted(set(self.secv) | set(self.ia) | set(self.fin) | set(self.oth)) if e < end]
        ref = (self.secv.get(end) or {}).get("filed") or (self.se.get(end) or (None, None))[1]   # 400일은 접수일 기준(11-3, Codex 2차)
        cands = [(e, x) for e, x in cands if x and ref and (date.fromisoformat(ref) - date.fromisoformat(x[1])).days <= 400]
        return cands[-1][1] if cands else None

    # 1-2 (+7-6)
    def tce(self, end):
        o = EQUITY_OVERRIDE.get(self.t, {}).get(end) if self.ov else None   # WFC 한정 예외: 보도자료 회사 정의 TCE
        if o and not (self.asof and o["filed"] > self.asof):
            return (o["tce_m"] * 1e6, o["filed"])
        c = self.ce(end)
        if not c:
            return None
        gw = self.gw.get(end) or self._carry_goodwill(end)   # 6판 10-1: 영업권도 400일까지 이어 쓴다(AXP — 연말에만 태그)
        if gw is None:
            return None
        if self.ed >= 7:
            ia = self._ia7(end)
            if ia is None:
                return None
            return (c[0] - gw[0] - ia[0], max(c[1], gw[1], ia[1]))
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
        v = c[0] - gw[0] - ia[0]
        return (v, max(c[1], gw[1], ia[1]))

    def _carry_goodwill(self, end):
        """그 결산일 이전 가장 최근 영업권 값, 400일 이내만(사전 등록 6판 10-1 — 무형자산 8-1과 같은 규칙)."""
        cands = [(e, v) for e, v in self.gw.items()
                 if e < end and (date.fromisoformat(end) - date.fromisoformat(e)).days <= 400]
        return max(cands)[1] if cands else None

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
        r = self.secv.get(end)
        if r and r.get("shares"):   # 7판: 그 분기 원문 값(가장 먼저 접수 — companyfacts는 나중 공시의 반올림 값으로 바뀐 분기가 있다, WFC 2024 1분기)
            cf = self._shares_cf(end)
            return (r["shares"], r["filed"]) if not cf or r["filed"] <= cf[1] else cf
        return self._shares_cf(end)

    def _shares_cf(self, end):
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
        """특별 항목 NI 조정액(세후, 보통주). 확인 안 한 분기면 None. 7판(11-5)은 특별 항목을 쓰지 않는다(GAAP)."""
        if self.ed >= 7:
            return 0.0
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
        if self.ed >= 7:
            return t
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
    """G5용 — 3개월 직접 공시값을 쓰지 않고 연초 누적(10-Q·10-K)끼리 뺀 분기값. 7판은 평가일까지 접수된 것만(11-0)."""
    y = end[:4]
    start = f"{y}-01-01"
    cum = {}
    for f in _facts(bank.cik, tag):
        if bank.ed >= 7 and bank.asof and f["filed"] > bank.asof:
            continue
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
    # 5판 개정 9-1(2026-10-05 사용자 결정): 회사가 대조할 값을 공시하지 않으면 "확인 불가"로 두고 남은 독립 대조로 판단한다.
    #   G1 — 회사 TBVPS가 없으면 우리 TCE·주식 수를 그 분기에 만들 수 있을 때만 통과(못 만들면 실제 미통과)
    #   G2 — BVPS가 없으면 CE 금액(±0.5%) + 그 분기 G1 TBVPS 대조(주식 수 확인), CE 금액이 없으면 BVPS(±0.5%); 둘 다 없으면 미통과
    g1_ok = lambda r: (r[3] is not None and abs(r[3]) <= 0.015) or (r[2] is None and r[1] is not None)
    g1_checked = lambda r: r[3] is not None and abs(r[3]) <= 0.015
    def g2_ok(r, r1):
        bv_ok = r[3] is not None and abs(r[3]) <= 0.005
        ce_ok = r[4] is not None and abs(r[4]) <= 0.005
        has_bv = r[2] is not None
        if has_bv and r[4] is not None:
            return bv_ok and ce_ok
        if not has_bv and r[4] is not None:
            return ce_ok and g1_checked(r1)          # BVPS 미공시 → CE 금액 + TBVPS로 주식 수 확인
        if has_bv:
            return bv_ok                             # CE 금액 미공시 → BVPS만
        return False
    res["G1"] = {"rows": rows1, "pass": all(g1_ok(r) for r in rows1),
                 "unverifiable": sum(1 for r in rows1 if r[2] is None and r[1] is not None)}
    res["G2"] = {"rows": rows2, "pass": all(g2_ok(r, r1) for r, r1 in zip(rows2, rows1)),
                 "unverifiable": sum(1 for r in rows2 if r[2] is None or r[4] is None)}
    # 9-2: 회사가 공시한 소급 재작성으로 누적 차분이 어긋난 분기는 관문 JSON의 recast_adjust_m(출처 함께)만큼 보정해 대조한다(BAC 4Q25 −119)
    adj5 = {q: (g["quarters"][q].get("recast_adjust_m") or 0.0) for q in g["quarters"]}
    g5_ok = lambda r: r[3] is not None and (abs(r[3]) <= 50 or (adj5.get(r[0]) and abs(r[3] - adj5[r[0]]) <= 50))
    res["G5"] = {"rows": rows5, "pass": all(g5_ok(r) for r in rows5),
                 "restated": [r[0] for r in rows5 if r[3] is not None and abs(r[3]) > 50 and g5_ok(r)]}
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
    # 5판 개정 9-2: 우리 연간 NI(가장 먼저 접수된 분기 값의 합, 7-2)가 10-K와 어긋나도, 그 해 분기 가운데 나중에 다시 공시된 값으로 바꿔
    # 합치면 10-K와 ±$50M이면 "통과(재작성)"(WFC 2021 1분기 4,363 → 4,256).
    def g3_ok(r):
        nim_ok = r[1] is not None and r[2] is not None and abs(r[1] - r[2]) <= 50
        roe_ok = r[4] is not None and r[5] is not None and abs(r[4] - r[5]) <= 0.015
        return nim_ok and roe_ok
    def g3_restated(r):
        """우리 값 − 10-K 차이가 그 해 3개월 분기 값의 나중 공시 수정(가장 먼저 − 가장 나중)으로 ±$50M 안에서 설명되면 재작성."""
        if r[1] is None or r[2] is None or abs(r[1] - r[2]) <= 50:
            return False
        late, early = {}, {}
        for f in _facts(bank.cik, "NetIncomeLossAvailableToCommonStockholdersBasic"):
            if "start" not in f or f["start"][:4] != r[0] or f["filed"] > bank.asof:
                continue
            if not 80 <= (date.fromisoformat(f["end"]) - date.fromisoformat(f["start"])).days <= 100:
                continue
            key = (f["start"], f["end"])
            if key not in late or f["filed"] > late[key]["filed"]:
                late[key] = f
            if key not in early or f["filed"] < early[key]["filed"]:
                early[key] = f
        rev = sum((early[k]["val"] - late[k]["val"]) / 1e6 for k in late)
        return abs(rev) > 0 and abs((r[1] - r[2]) - rev) <= 50 and r[4] is not None and r[5] is not None and abs(r[4] - r[5]) <= 0.015
    res["G3"] = {"rows": rows3, "pass": all(g3_ok(r) or g3_restated(r) for r in rows3),
                 "restated": [r[0] for r in rows3 if not g3_ok(r) and g3_restated(r)]}
    rows4 = []
    for q, v in sorted(g["quarters"].items()):
        n, p = bank.ni_ttm(q), bank.payout_ttm(q)
        ours = p[0] / n[0] if n and p and n[0] > 0 else None
        cv = v.get("net_payout_ltm")
        rows4.append((q, ours, cv, None if ours is None or cv is None else ours - cv))
    # 9-1: 회사가 순환원율을 공시하지 않으면 "확인 불가"로 통과(우리 값은 있어야 한다) — 카드에 적는다
    # 최근 4분기 NI ≤ 0이면 순환원율은 정의되지 않는다(COF 2025-06 — Discover 인수 충당금) — 회사 값도 없으면 확인 불가로 본다
    _ni_neg = {r[0] for r in rows4 if r[1] is None and (bank.ni_ttm(r[0]) or (1,))[0] <= 0}
    res["G4"] = {"rows": rows4, "pass": all((r[3] is not None and abs(r[3]) <= 0.10) or (r[2] is None and (r[1] is not None or r[0] in _ni_neg)) for r in rows4),
                 "unverifiable": sum(1 for r in rows4 if r[2] is None)}
    if missing:
        for k in ("G1", "G2", "G3", "G4", "G5"):
            res[k]["pass"] = False
    return res


# ── 7판 관문 N1~N5(11-6, 2026-10-11 초안) — 보도자료 대조 대신 SEC 자료 안의 대조 ─────────────
def _q3m(cik, tag, end, unit_key=None, asof=None):
    """그 분기(약 3개월) 직접 공시값 — 평가일까지 접수된 것 가운데 가장 먼저 접수된 것. (값, 접수일)."""
    u = bmh._facts(cik).get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {})
    rows = [r for k, rs in u.items() if unit_key is None or k == unit_key for r in rs if not asof or r["filed"] <= asof]
    rows = [r for r in rows if r.get("end") == end and r.get("start") and 80 <= (date.fromisoformat(end) - date.fromisoformat(r["start"])).days <= 100]
    return (sorted(rows, key=lambda r: r["filed"])[0]["val"], sorted(rows, key=lambda r: r["filed"])[0]["filed"]) if rows else None


def _fy(cik, tag, end, unit_key=None, asof=None):
    u = bmh._facts(cik).get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {})
    rows = [r for k, rs in u.items() if unit_key is None or k == unit_key for r in rs if not asof or r["filed"] <= asof]
    rows = [r for r in rows if r.get("end") == end and r.get("start") and 350 <= (date.fromisoformat(end) - date.fromisoformat(r["start"])).days <= 380]
    return sorted(rows, key=lambda r: r["filed"])[0]["val"] if rows else None


def peer_ok7(bank, end):
    """7판 11-6 동종업: 그 분기 CE·TCE·S가 만들어지고 N5-1(EPS 대조)·N5-2(우선주 차감)를 통과하는가 — 아니면 그날 동종업 P/TBV에서 뺀다."""
    c = checks7(bank, end)
    core = all((bank.ce(end), bank.tce(end), bank.shares(end)))
    bad = [k for k in ("N5_1", "N5_2") if c.get(k, {}).get("pass") is False]
    return core and not bad, ("CE·TCE·주식 수 중 결측" if not core else "") + ("·".join(bad) + " 미통과" if bad else "")


def checks7(bank, end):
    """{N1.., ok, stop_reasons, flags} — 최신 분기 end에 대해. 하나라도 미통과면 ok False(그 분기를 카드에 반영하지 않는다)."""
    res, stop, flags = {}, [], []
    prev = qends_before(end, 1)[0]
    ce, tce, s = bank.ce(end), bank.tce(end), bank.shares(end)
    # N1 완전성
    miss = [k for k, v in (("CE", ce), ("TCE", tce), ("S", s), ("NI", bank.ni.get(end)), ("NI TTM", bank.ni_ttm(end)),
                           ("기초 CE", bank.ce(qends_before(end, 4)[-1])), ("순환원 TTM", bank.payout_ttm(end)), ("유보율", bank.retention(end))) if not v]
    # 효력(11-6 효력표): CE·TCE·S·NI가 없으면 분기 정지. RIM 입력(TTM·기초 CE·순환원·유보율)만 없으면 정지하지 않고 RIM만 기권(2장 규칙) — 배수는 새 분기로(Fable 2차)
    core = [k for k in miss if k in ("CE", "TCE", "S", "NI")]
    res["N1"] = {"pass": not core, "missing": core, "rim_missing": [k for k in miss if k not in core]}
    # N2 분기 NI: 직접값 vs 누적 차분
    d3 = _q3m(bank.cik, "NetIncomeLossAvailableToCommonStockholdersBasic", end, asof=bank.asof)
    nq = bank.ni.get(end)
    yd = ytd_diff_q(bank, "NetIncomeLossAvailableToCommonStockholdersBasic", end)   # 누적끼리 뺀 값 — bank.ni는 직접값을 먼저 쓰므로 그것과 견주면 같은 값끼리 비교한다(Codex)
    if d3 and yd is not None and not end.endswith("03-31"):
        diff = abs(yd - d3[0])
        res["N2"] = {"pass": diff <= 5e6 or (diff <= 50e6 and diff <= 0.10 * abs(d3[0])), "diff_m": round(diff / 1e6, 1)}
    else:
        res["N2"] = {"pass": True, "note": "직접값 없음(4분기) — N5-1로 대신"}
    # N3 우선주 연속성 — 자본 이동 전체 대조는 자본변동표의 비표준 항목 때문에 정상 분기를 멈췄다(COF 2026 2분기 +$1.9B 미설명),
    # 발행·상환 현금 대조는 회사 고유 태그 때문에 정상 발행을 멈췄다(WFC 2024 3분기 +$2.0B, 2026-10-11 시험).
    # 목적(우선주 태그가 잘못 잡혀 CE가 계단처럼 뛰는 것 — BAC 10-K 회사 고유 태그 329)에 맞춰: 1년 전 같은 분기와 같은 태그이고 값이 절반~2배 안.
    if bank.pref_tbl is not None and not bank.pref_tbl.get("path") and bank.pref_tbl.get("tags"):
        ya = qends_before(end, 4)[-1]
        p1, p0 = bank._pref7(end), bank._pref7(ya)
        t1, t0 = getattr(bank, "_pref_tag", {}).get(end), getattr(bank, "_pref_tag", {}).get(ya)
        if p1 and p0:
            r_ = p1[0] / p0[0] if p0[0] else None
            res["N3"] = {"pass": t1 == t0 and r_ is not None and 0.5 <= r_ <= 2.0, "tag": t1, "tag_yago": t0, "ratio": r_ and round(r_, 3)}
        elif not p1 and not p0:
            res["N3"] = {"pass": True, "note": "우선주 없음"}
        else:
            res["N3"] = {"pass": False, "note": "우선주 값이 한쪽 분기에만 있다", "now": p1 and round(p1[0] / 1e6), "yago": p0 and round(p0[0] / 1e6)}
    else:
        res["N3"] = {"pass": True, "note": "우선주 표 경로 밖(AXP 상환가·표 없는 은행)"}
    # N3b 자본 수준 — CE를 자본 구성요소 합(보통주 + 자본잉여금 + 이익잉여금 + 기타포괄손익 − 자기주식)과 견줘, 그 비율이 1년 전 같은 분기보다 1%p 넘게 변하면 정지.
    # 수준 자체가 아니라 변화를 본다 — GS(주식보상 항목)·AXP·COF(자본잉여금에 우선주)는 구성이 달라 4~8%가 늘 있다(2026-10-11 시험). Fable 2차: 보도자료 G2가 잡던 수준 오류의 대체.
    def _comp(e):
        I = lambda t: (instant(bank.cik, t, bank.asof).get(e) or (None,))[0]
        cs = I("CommonStocksIncludingAdditionalPaidInCapital")
        if cs is None:
            a_ = I("AdditionalPaidInCapitalCommonStock") or I("AdditionalPaidInCapital")
            cs = (I("CommonStockValue") or 0) + a_ if a_ is not None else None
        re_, ao = I("RetainedEarningsAccumulatedDeficit"), I("AccumulatedOtherComprehensiveIncomeLossNetOfTax")
        tr = I("TreasuryStockValue") or I("TreasuryStockCommonValue") or 0
        c_ = bank.ce(e)
        if not (c_ and cs is not None and re_ is not None and ao is not None):
            return None
        tot = cs + re_ + ao - tr
        pf = c_ and bank.se.get(e) and bank.se[e][0] - c_[0]   # 우리가 뺀 우선주(자본잉여금에 우선주를 넣는 은행 — COF·AXP)
        return (tot / c_[0] - 1, (tot - (pf or 0)) / c_[0] - 1)
    ya = qends_before(end, 4)[-1]
    k1, k0 = _comp(end), _comp(ya)
    if k1 is not None and k0 is not None:   # 1년 전에 더 잘 맞던 쪽(우선주를 뺀 합 또는 그냥 합)을 같은 방식으로 이번 분기에도
        j = 0 if abs(k0[0]) <= abs(k0[1]) else 1
        k1, k0 = k1[j], k0[j]
    res["N3b"] = ({"pass": abs(k1 - k0) <= 0.01, "gap_now": round(k1, 4), "gap_yago": round(k0, 4)} if k1 is not None and k0 is not None
                  else {"pass": None, "note": "자본 구성요소 결측"})
    # N4 급변
    cp, sp = bank.ce(prev), bank.shares(prev)
    jumps = []
    if ce and s and cp and sp:
        if abs((ce[0] / s[0]) / (cp[0] / sp[0]) - 1) > 0.10:
            jumps.append("BVPS ±10% 초과")
        if abs(s[0] / sp[0] - 1) > 0.10:
            jumps.append("주식 수 ±10% 초과")
    g0, g1 = bank.gw.get(prev) or bank._carry_goodwill(prev), bank.gw.get(end)
    if g0 and g1 and g1[0] > g0[0] * 1.2:
        jumps.append("영업권 20% 넘게 증가")
    ackd = json.load(open(ACK)).get(bank.t, {}) if os.path.exists(ACK) else {}
    def _jumps(e):
        p_ = qends_before(e, 1)[0]
        a1, a0, s1, s0 = bank.ce(e), bank.ce(p_), bank.shares(e), bank.shares(p_)
        j = []
        if a1 and a0 and s1 and s0:
            if abs((a1[0] / s1[0]) / (a0[0] / s0[0]) - 1) > 0.10:
                j.append("BVPS ±10% 초과")
            if abs(s1[0] / s0[0] - 1) > 0.10:
                j.append("주식 수 ±10% 초과")
        g0_, g1_ = bank.gw.get(p_) or bank._carry_goodwill(p_), bank.gw.get(e)
        if g0_ and g1_ and g1_[0] > g0_[0] * 1.2:
            j.append("영업권 20% 넘게 증가")
        return j
    # 승인되지 않은 급변은 다음 분기에 저절로 풀리지 않는다 — 이번 분기와 앞 4개 분기 가운데 ack 없는 급변이 있으면 정지(Codex 2차)
    pend = {e: _jumps(e) for e in [end] + qends_before(end, 4)}
    pend = {e: j for e, j in pend.items() if j and e not in ackd}
    res["N4"] = {"pass": not pend, "jumps": jumps, "unacked": pend, "ack": ackd.get(end)}
    # N5-1 EPS 대조
    if d3 is not None or end.endswith("12-31"):
        ni_ = d3[0] if d3 else _fy(bank.cik, "NetIncomeLossAvailableToCommonStockholdersBasic", end, asof=bank.asof)
        wa = (_q3m(bank.cik, "WeightedAverageNumberOfSharesOutstandingBasic", end, "shares", bank.asof) or (None,))[0] if d3 else _fy(bank.cik, "WeightedAverageNumberOfSharesOutstandingBasic", end, "shares", bank.asof)
        eps = (_q3m(bank.cik, "EarningsPerShareBasic", end, "USD/shares", bank.asof) or (None,))[0] if d3 else _fy(bank.cik, "EarningsPerShareBasic", end, "USD/shares", bank.asof)
        if ni_ and wa and eps:
            res["N5_1"] = {"pass": abs(ni_ / wa / eps - 1) <= 0.01 or abs(ni_ / wa - eps) <= 0.011, "ratio": round(ni_ / wa / eps, 4)}
        else:
            res["N5_1"] = {"pass": None, "note": "EPS·가중평균 주식 수 결측"}
        if d3 and wa and s and abs(s[0] - wa) / s[0] > 0.02:   # 4분기는 연간 평균이라 자사주 매입 은행이 늘 걸린다 — 1~3분기만
            flags.append(f"분기말 주식 수가 기본 가중평균과 {abs(s[0] - wa) / s[0] * 100:.1f}% 다르다")
    # N5-2 우선주 배당이 있는데 우선주 차감 0
    pd = bank.ttm(bank.div_pref, end)
    pz = bank.pref_tbl is not None and not bank.pref_tbl.get("path") and bank.pref_tbl.get("tags") and bank._pref7(end) is None and ce
    res["N5_2"] = {"pass": not (pd and pd[0] > 0 and (pz or (ce and bank.se.get(end) and abs(bank.se[end][0] - ce[0]) < 1)))}
    for k in ("N3", "N3b"):   # 사람이 확인한 분기(research/bank_ack.json)는 N3·N3b도 푼다 — 우선주 새 발행·전액 상환(Fable 2차)
        if res.get(k, {}).get("pass") is False and end in ackd:
            res[k]["pass"], res[k]["ack"] = True, ackd[end]
    for k, v in res.items():
        if v.get("pass") is False:
            stop.append(k)
    return {"end": end, **res, "ok": not stop, "stop": stop, "flags": flags,
            "unverifiable": [k for k, v in res.items() if v.get("pass") is None]}
