#!/usr/bin/env python3
"""관리의료 보험 초과이익모형(RIM) — research/insurer_rim_prereg.md 1판 구현(UNH·ELV, 2026-10-17).

    python3 v2/adapters/insurer_rim.py ELV --json v2/ELV_rim.json

정의는 사전 등록 문서가 원본이다. 수렴 방식·r·시나리오·민감도 격자는 은행 7판(bank_rim.rim_value)을 그대로 쓰고,
회사별 태그는 research/insurer_sec_tags.json, 급변 승인은 research/insurer_ack.json({회사: {분기말: {reason, approved}}}).
평가일 = 카드 일봉 마지막 날(공시 기준표 sec_approved.json 날짜를 넘지 않는다). 그날까지 접수된 SEC 사실만 쓴다(11-0·7-2).
"""
import argparse
import json
import os
import statistics
import sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_rim as br  # noqa: E402

bmh = br.bmh
R, FADE = br.R, br.FADE
ROE_HI = 0.80   # 요구 ROE 탐색 상한(§3 — 은행 60%와 다른 한 가지)
TAGS = json.load(open(os.path.join(V2, "research", "insurer_sec_tags.json")))
ACK = os.path.join(V2, "research", "insurer_ack.json")
QEND = ("03-31", "06-30", "09-30", "12-31")
# 판정 문턱(§3) — 현재가 ÷ 기본. fill.py 현금흐름 표·카드 JS dcfLevel과 같아야 한다(fill.py가 대조한다)
SCORE_TABLE = ((0.7, 1), (0.9, 1), (1.1, 0), (1.5, -1))


def score_of(ratio):
    for lim, s in SCORE_TABLE:
        if ratio <= lim:
            return s
    return -2


def ytd_quarters(cik, tag, asof):
    """{분기말: (분기값, 가용일)} — 연초 누적끼리 뺀 값(1분기 = 1분기 누적, 4분기 = 연간 − 9개월 누계). 같은 기간은 평가일까지
    가장 먼저 접수된 값, 가용일은 두 누적 값 접수일 중 늦은 쪽(7-2). 회계연도 = 달력 연도(UNH·ELV)."""
    cum = {}
    for f in br._facts(cik, tag):
        if "start" not in f or (asof and f["filed"] > asof) or f["start"][5:] != "01-01" or f["start"][:4] != f["end"][:4] or f["end"][5:] not in QEND:
            continue
        if f["end"] not in cum or f["filed"] < cum[f["end"]][1]:
            cum[f["end"]] = (f["val"], f["filed"])
    out = {}
    for e, (v, fd) in cum.items():
        if e.endswith("03-31"):
            out[e] = (v, fd)
            continue
        p = br.qends_before(e, 1)[0]
        if p in cum:
            out[e] = (v - cum[p][0], max(fd, cum[p][1]))
    return out


class Insurer:
    def __init__(self, ticker, asof):
        self.t, self.asof, self.ed = ticker, asof, 7   # ed: bank_rim.ytd_diff_q가 평가일 이후 접수를 빼는 조건
        cfg = TAGS[ticker]
        self.cik = c = cfg["cik"]
        ce = cfg["ce"]
        if "tag" in ce:
            self.ce_raw = br.instant(c, ce["tag"], asof)
        else:   # UNH: 비지배지분 포함 자본 − 비지배지분, 같은 결산일 두 값이 모두 있을 때만(2-1)
            a, b = br.instant(c, ce["plus"], asof), br.instant(c, ce["minus"], asof)
            self.ce_raw = {e: (a[e][0] - b[e][0], max(a[e][1], b[e][1])) for e in a if e in b}
        self.so = br.instant(c, cfg["shares"], asof)
        self.pref = br.instant(c, "PreferredStockValue", asof)
        self.gw = br.instant(c, "Goodwill", asof)
        self.oci = br.instant(c, "AccumulatedOtherComprehensiveIncomeLossNetOfTax", asof)
        self.ni_tag = cfg["ni"]
        self.ni = ytd_quarters(c, cfg["ni"], asof)   # RIM 입력은 누적 차분(§4 N2·7-2) — 3개월 직접값을 먼저 쓰지 않는다(dr 구현 r1 Codex)
        self.div = br.flow_q(c, [cfg["div"]], ticker, asof)
        self.buy = br.flow_q(c, [cfg["buy"]], ticker, asof)
        self.iss = br.flow_q(c, [cfg["iss"]], ticker, asof)

    # 2-1·7-9: CE ≤ 0이면 없음(직전 분기로 대신하지 않는 즉시 기권은 run()이 따로 본다)
    def ce(self, e):
        v = self.ce_raw.get(e)
        return v if v and v[0] > 0 else None

    def shares(self, e):
        v = self.so.get(e)
        return v if v and v[0] > 0 else None

    def ttm(self, series, end):
        ks = [end] + br.qends_before(end, 3)
        if not all(k in series for k in ks):
            return None
        return (sum(series[k][0] for k in ks), max(series[k][1] for k in ks))

    def ni_ttm(self, end):
        return self.ttm(self.ni, end)

    def bad79(self, e):
        """7-9: 그 분기말 CE ≤ 0 또는 S ≤ 0(값이 있는데 0 이하)."""
        return (e in self.ce_raw and self.ce_raw[e][0] <= 0) or (e in self.so and self.so[e][0] <= 0)

    # 2-4: NI_TTM ÷ 4분기 전 분기말 CE — 두 분기말 CE가 양수이고 그 분기 S가 0 이하가 아닐 때만(7-9, dr 구현 r1 Codex)
    def roe(self, end):
        b_ = br.qends_before(end, 4)[-1]
        n, b0 = self.ni_ttm(end), self.ce(b_)
        if not n or not b0 or not self.ce(end) or self.bad79(end) or self.bad79(b_):
            return None
        return (n[0] / b0[0], max(n[1], b0[1]))

    # 2-6: 배당·매입은 네 분기 모두 필수, 발행은 분기별로 없으면 그 분기 0
    def payout_ttm(self, end):
        d, b = self.ttm(self.div, end), self.ttm(self.buy, end)
        if d is None or b is None:
            return None
        ks = [end] + br.qends_before(end, 3)
        iss = [self.iss[k] for k in ks if k in self.iss]
        i_v = sum(x[0] for x in iss)
        return {"div": d[0], "buy": b[0], "iss": i_v, "net": d[0] + b[0] - i_v,
                "filed": max([d[1], b[1]] + [x[1] for x in iss])}

    def retention(self, end):
        n, p = self.ni_ttm(end), self.payout_ttm(end)
        if not n or not p or n[0] <= 0:
            return None
        raw = 1 - p["net"] / n[0]
        return {"b": min(max(raw, 0.0), 1.0), "raw": raw, "clipped": not 0.0 <= raw <= 1.0}

    def latest(self):
        """평가일까지 접수된 가장 최근 분기말(CE 원값·NI·주식 수 가운데 하나라도 있는 분기)."""
        ks = [e for e in set(self.ce_raw) | set(self.ni) | set(self.so) if e[5:] in QEND]
        return max(ks) if ks else None

    def filed_of(self, e):
        """그 분기 공시의 접수일 — 이 분기를 빼고 다시 계산할 때 그 전날로 자른다."""
        fs = [d[e][1] for d in (self.ce_raw, self.so, self.ni) if e in d]
        return min(fs) if fs else None


def _acks(ticker, eval_date):
    """N4 승인 — 승인일 ≤ 평가일인 것만(나중 승인이 과거 평가를 바꾸지 않게)."""
    a = json.load(open(ACK)).get(ticker, {}) if os.path.exists(ACK) else {}
    return {e: v for e, v in a.items() if not e.startswith("_") and v.get("approved") and v["approved"] <= eval_date}


def checks(ins, end, eval_date):
    """§4 관문 N1·N2·N4·N5-1 — {N1.., ok, stop}. 미통과면 그 분기를 RIM에 쓰지 않는다(직전 통과 분기 사용)."""
    res = {}
    prev = br.qends_before(end, 1)[0]
    rt = ins.retention(end)
    miss = [k for k, v in (("CE", ins.ce(end)), ("S", ins.shares(end)), ("NI", ins.ni.get(end)), ("NI TTM", ins.ni_ttm(end)),
                           ("기초 CE", ins.ce(br.qends_before(end, 4)[-1])), ("순환원 TTM", ins.payout_ttm(end)), ("유보율", rt),
                           ("출발 ROE", ins.roe(end))) if not v]   # 출발 ROE(7-9 포함)가 없으면 직전 통과 분기로(dr 구현 r2 Codex)
    if (ins.pref.get(end) or (0,))[0]:   # 우선주 0(N1) — 직전 분기로 물러날 때도 우선주가 있던 분기를 쓰지 않는다(dr 구현 r1 Codex)
        miss.append("우선주 0 아님")
    res["N1"] = {"pass": not miss, "missing": miss}
    # N2 분기 NI — 같은 공시의 3개월 직접값 대 누적 차분(1분기는 같은 값이라 보지 않는다)
    d3 = br._q3m(ins.cik, ins.ni_tag, end, asof=ins.asof)
    yd = br.ytd_diff_q(ins, ins.ni_tag, end)
    if d3 and yd is not None and not end.endswith("03-31"):
        diff = abs(yd - d3[0])
        res["N2"] = {"pass": diff <= 5e6 or (diff <= 50e6 and diff <= 0.10 * abs(d3[0])), "diff_m": round(diff / 1e6, 1)}
    else:
        res["N2"] = {"pass": True, "note": "직접값 없음(4분기·1분기) — N5-1로 대신"}
    # N4 급변 — 이번 분기와 앞 네 분기 가운데 승인 없는 급변
    ackd = _acks(ins.t, eval_date)

    def jumps(e):
        p_ = br.qends_before(e, 1)[0]
        a1, a0, s1, s0 = ins.ce(e), ins.ce(p_), ins.shares(e), ins.shares(p_)
        j = []
        # BVPS·주식 수·영업권을 따로 본다 — 자본 결측이 주식 수 급변 검사를 막지 않게(dr 구현 r1 Codex)
        if a1 and a0 and s1 and s0:
            if abs((a1[0] / s1[0]) / (a0[0] / s0[0]) - 1) > 0.10:
                j.append("BVPS ±10% 초과")
        elif e == end:
            j_unk.append("BVPS")
        if s1 and s0:
            if abs(s1[0] / s0[0] - 1) > 0.10:
                j.append("주식 수 ±10% 초과")   # 분할도 여기서 멈춘다(2-5 분할 조정은 아직 없음 — 생기면 승인 또는 새 판)
        elif e == end:
            j_unk.append("주식 수")
        g1, g0 = ins.gw.get(e), ins.gw.get(p_)
        if g1 and g0 and g1[0] > g0[0] * 1.2:
            j.append("영업권 20% 넘게 증가")
        return j
    j_unk = []
    pend = {e: jumps(e) for e in [end] + br.qends_before(end, 4)}
    pend = {e: j for e, j in pend.items() if j and e not in ackd}
    res["N4"] = {"pass": not pend, "unacked": pend, "ack": ackd.get(end), **({"note": "직전 분기 값 없음(" + "·".join(j_unk) + ") — 확인 불가로 통과"} if j_unk else {})}
    # N5-1 EPS 대조 — 1~3분기는 RIM 입력 NI(누적 차분) ÷ 3개월 기본 가중평균 대 3개월 EPS, 4분기는 연간끼리(dr 구현 r1 Codex)
    if end.endswith("12-31"):
        ni_ = br._fy(ins.cik, ins.ni_tag, end, asof=ins.asof)
        wa = br._fy(ins.cik, "WeightedAverageNumberOfSharesOutstandingBasic", end, "shares", ins.asof)
        eps = br._fy(ins.cik, "EarningsPerShareBasic", end, "USD/shares", ins.asof)
    else:
        ni_ = (ins.ni.get(end) or (None,))[0]
        wa = (br._q3m(ins.cik, "WeightedAverageNumberOfSharesOutstandingBasic", end, "shares", ins.asof) or (None,))[0]
        eps = (br._q3m(ins.cik, "EarningsPerShareBasic", end, "USD/shares", ins.asof) or (None,))[0]
    if ni_ is not None and wa and eps is not None:   # NI = 0도 대조한다(0과 결측을 구분)
        ok = abs(ni_ / wa - eps) <= 0.011 if eps == 0 else (abs(ni_ / wa / eps - 1) <= 0.01 or abs(ni_ / wa - eps) <= 0.011)
        res["N5_1"] = {"pass": ok, "ni_per_share": round(ni_ / wa, 4), "eps": eps}
    else:
        res["N5_1"] = {"pass": None, "note": "EPS·가중평균 주식 수 결측 — 확인 불가로 통과"}
    stop = [k for k, v in res.items() if v.get("pass") is False]
    return {"end": end, **res, "ok": not stop, "stop": stop, "unverifiable": [k for k, v in res.items() if v.get("pass") is None]}


def _abstain(why, **kw):
    return {"unavailable": why, "low": None, "base": None, "high": None, **kw}


def run(ticker, asof, price, eval_date=None):
    """asof = 자료 기준(평가일과 공시 기준표 날짜 중 이른 날), eval_date = 평가일(카드 일봉 마지막 날 — 200일·승인일 비교)."""
    eval_date = eval_date or asof
    ins = Insurer(ticker, asof)
    L = ins.latest()
    if not L:
        return _abstain("재무 자료 없음")
    # 즉시 기권(§4) — 최신 분기 기준, 직전 분기 값으로 대신하지 않는다
    c0, s0 = ins.ce_raw.get(L), ins.so.get(L)
    if (c0 and c0[0] <= 0) or (s0 and s0[0] <= 0):
        return _abstain(f"{L} 보통주 자본 또는 주식 수가 0 이하(7-9)", L=L)
    if (ins.pref.get(L) or (0,))[0]:
        return _abstain(f"{L} 우선주가 생겼다 — 이 판의 정의는 우선주가 없다는 전제(새 판으로 우선주 조정을 등록할 것)", L=L)
    n8_latest = sum(1 for e in [L] + br.qends_before(L, 7) if ins.roe(e))
    if n8_latest < 6:   # 즉시 기권(§4) — 최신 기준 2년 창이 모자라면 직전 분기로 물러나 우회하지 않는다(dr 구현 r1 Codex)
        return _abstain(f"2년 ROE 중앙값을 낼 분기가 {n8_latest}개뿐(최소 6개, 7-8)", L=L)
    # 관문 — 미통과면 직전 통과 분기(그 분기 공시 전날까지 접수된 자료로 다시), 최대 8분기
    g = checks(ins, L, eval_date)
    frozen = None
    if not g["ok"]:
        frozen = {"quarter": L, "stop": g["stop"], "detail": {k: g[k] for k in g["stop"]}, "skipped": []}
        used = None
        for _ in range(8):
            f_ = ins.filed_of(L)
            if not f_:
                break
            cut = (date.fromisoformat(f_) - timedelta(days=1)).isoformat()
            ins = Insurer(ticker, cut)
            L = ins.latest()
            if not L:
                break
            g = checks(ins, L, eval_date)
            if g["ok"]:
                used = L
                break
            frozen["skipped"].append(L)
        frozen["used_quarter"] = used
        if not used:
            return _abstain("관문을 통과한 분기가 최근 8분기 안에 없음", frozen=frozen)
    if (date.fromisoformat(eval_date) - date.fromisoformat(L)).days > 200:
        return _abstain(f"기준 분기 {L}가 평가일보다 200일 넘게 앞섬", frozen=frozen)
    ce, S = ins.ce(L)[0], ins.shares(L)[0]
    roe0 = ins.roe(L)[0]
    rt = ins.retention(L)
    b = rt["b"]
    hist = [ins.roe(e) for e in [L] + br.qends_before(L, 19)]   # 7-8 고정 달력 창
    h20, h8 = [x[0] for x in hist if x], [x[0] for x in hist[:8] if x]
    roe5 = statistics.median(h20) if len(h20) >= 16 else None
    roe2 = statistics.median(h8) if len(h8) >= 6 else None
    if roe2 is None:
        return _abstain(f"2년 ROE 중앙값을 낼 분기가 {len(h8)}개뿐(최소 6개, 7-8)", L=L, frozen=frozen)
    val = lambda end_, r_=R, lam=FADE: br.rim_value(ce, roe0, end_, b, r_, lam)
    vb = val(roe2)
    if vb is None:
        return _abstain("잔존 성장이 할인율 이상(r − g_T ≤ 0)", L=L, frozen=frozen)
    v5, vh = (val(roe5) if roe5 is not None else None), val(roe0)
    out = {"L": L, "asOf": eval_date, "price": price, "ce": ce, "shares": S, "bvps": ce / S, "roe0": roe0, "roe2y": roe2, "roe5y": roe5,
           "n20": len(h20), "n8": len(h8), "b": b, "bRaw": rt["raw"], "bClipped": rt["clipped"],
           "payout": {k: v for k, v in ins.payout_ttm(L).items() if k != "filed"}, "niTtm": ins.ni_ttm(L)[0],
           "ceBegin": ins.ce(br.qends_before(L, 4)[-1])[0], "goodwill": (ins.gw.get(L) or (None,))[0],
           "oci": (ins.oci.get(L) or (None,))[0],
           "low": v5 / S if v5 is not None else None, "base": vb / S, "high": vh / S if vh is not None else None,
           "rimQuarter": L if frozen else None, "frozen": frozen, "gates": g,
           # 입력 가용일(11-0) — 쓴 사실 가운데 가장 늦은 접수일
           "inputsFiled": max(ins.ce(L)[1], ins.shares(L)[1], ins.ni_ttm(L)[1], ins.payout_ttm(L)["filed"], ins.ce(br.qends_before(L, 4)[-1])[1])}
    rq = br.required_roe(ce, b, price * S, hi=ROE_HI)
    out["requiredRoe"] = rq
    out["grid"] = {f"{r_:.2f}|{lam}": (lambda v: v / S if v is not None else None)(val(roe2, r_, lam))
                   for r_ in (0.08, 0.09, 0.10, 0.11, 0.12) for lam in (0.0, 0.5, 1.0)}
    out["ratio"] = price / out["base"] if out["base"] > 0 else None
    out["score"] = score_of(out["ratio"]) if out["ratio"] is not None else -2
    hard = []
    if roe2 < R:
        hard.append("roe_below_r")   # ① 기본 ROE_end < r
    if b == 0:
        hard.append("b_zero")   # ②
    if rq is None:
        hard.append("no_required_roe")   # ③
    # ④ 출발 TTM 네 분기 가운데 최근 8분기 NI 중앙값에서 40% 넘게 벗어난 분기 — 모두 동시에 중앙값으로 바꾼 ROE(표시 전용, 2-7)
    q8 = [ins.ni.get(e) for e in [L] + br.qends_before(L, 7)]
    if all(q8):
        med = statistics.median(x[0] for x in q8)
        odd = [e for e in [L] + br.qends_before(L, 3) if med > 0 and abs(ins.ni[e][0] / med - 1) > 0.40]
        if med > 0 and odd:
            alt = out["niTtm"] - sum(ins.ni[e][0] for e in odd) + med * len(odd)
            out["signal4"] = {"quarters": odd, "ratios": [round(ins.ni[e][0] / med, 2) for e in odd], "ni": [ins.ni[e][0] for e in odd], "median_q_ni": med,
                              "roe_at_median": alt / out["ceBegin"]}
            hard.append("signal4")
    out["hard"] = hard
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--json")
    a = ap.parse_args()
    t = a.ticker.upper()
    daily = bmh.load_daily(t)
    asof, px = daily[-1][0], daily[-1][4]
    cap = bmh._approved().get(TAGS[t]["cik"])
    r = run(t, min(asof, cap) if cap else asof, px, eval_date=asof)
    r["asOf"], r["price"] = asof, px
    show = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k not in ("grid", "gates", "frozen")}
    print(t, json.dumps(show, ensure_ascii=False, default=str))
    if r.get("gates"):
        print("관문", {k: v for k, v in r["gates"].items() if k not in ("end",)})
    if r.get("frozen"):
        print("직전 통과 분기", r["frozen"])
    if a.json:
        json.dump(r, open(a.json, "w"), ensure_ascii=False, indent=1, default=str)
        print("저장:", a.json)


if __name__ == "__main__":
    main()
