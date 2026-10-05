"""A8 본업 이익 정의 — S&P500 시점 재현(사전 등록: a8_core_prereg.md).

2026-10-03 패널(verdict_replay_panel.json)의 다른 배수·현금흐름 칸은 그대로 두고 PER만 변형(A·B·B+·C·C+)마다 새로 계산한다.
평가일마다 그날까지 공시된 TTM으로 대상 여부를 정하고, 대상이면 그 평가일의 5년 자기 이력 전체를 그 기준으로 낸다(카드와 같음).

    python3 a8_core_replay.py            # PER 시리즈 계산 + 분석
    python3 a8_core_replay.py --analyze  # 저장된 PER 결과로 분석만
"""
import contextlib
import io
import json
import math
import os
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402
import verdict_replay as vr  # noqa: E402
from verdict_replay import bmh, pit, v, NEG  # noqa: E402

d = v.d
OUT_PER = os.environ.get("A8_OUT") or os.path.join(HERE, "a8_core_per.json")
RESULT = os.path.join(HERE, "a8_core_result.json")
# 변경 기록 ①: 이자 태그를 다시 받아 합친 캐시(2026-10-02까지 공시분)
FACTS = os.path.join(HERE, ".facts_a8")
# 변경 기록 ③: 보험 영업이 있는 회사 — 투자수익이 매출 줄이라 이자수익을 0으로
INSURER_SUB = {"Managed Health Care"}
INSURER_EXTRA = {"CI", "CVS"}
VARIANTS = ["A", "B", "B+", "C", "C+"]
THRESH = 0.20
NET_TAGS = ["InterestIncomeExpenseNonoperatingNet", "InterestIncomeExpenseNet"]
INC_TAGS = ["InvestmentIncomeInterest", "InterestIncomeOther", "InvestmentIncomeInterestAndDividend", "InterestIncomeNonoperating"]
EXP_TAGS = ["InterestExpenseNonoperating", "InterestExpense", "InterestExpenseDebt", "InterestAndDebtExpense"]


def ttm(cik, t, tags):
    _, rows = bmh.pick_tag(cik, tags)
    return bmh.ttm_series(bmh.quarterly_flow(rows, t)) if rows else []


def at_end(series, end, dd):
    xs = [e for e in series if e["end"] == end and e["available"] <= dd]
    return xs[-1]["val"] if xs else None


def state_series(t, cik):
    """그 공시 상태에서 PER 변형에 필요한 TTM 시리즈."""
    s = {"opinc": ttm(cik, t, bmh.EBITDA_TAGS["opinc"])}
    for name, tags in bmh.CORE_TAX_TAGS.items():
        s[name] = ttm(cik, t, tags)
    if not s["pretax"]:          # 세전 태그가 연간에만 있는 회사 — 엔진과 같은 대체
        _, nr = bmh.pick_tag(cik, ["NetIncomeLoss"]); _, tr = bmh.pick_tag(cik, bmh.CORE_TAX_TAGS["tax"])
        nq = {e["end"]: e for e in bmh.quarterly_flow(nr, t)}; tq = {e["end"]: e for e in bmh.quarterly_flow(tr, t)}
        merged = [dict(nq[k], val=nq[k]["val"] + tq[k]["val"], filed=max(nq[k]["filed"], tq[k]["filed"])) for k in sorted(nq) if k in tq]
        s["pretax"] = bmh.ttm_series(merged)
    # 순이자 태그는 종목마다 시기별로 바뀐다(NOW: 이자비용 태그가 2022년 InterestExpense → 지금 InterestExpenseDebt).
    # pick_tag 하나로 고르면 끊긴 태그가 잡혀 값이 빈다 — 태그마다 시리즈를 두고 그 분기에 값이 있는 첫 태그를 쓴다.
    for name, tags in (("net", NET_TAGS), ("inc", INC_TAGS), ("exp", EXP_TAGS)):
        s[name] = [x for x in (ttm(cik, t, [tg]) for tg in tags) if x]
        # 변경 기록 ②: 결측 판정은 분기 행으로 — 그 태그의 공시 행 (결산일, 공시일)
        s["raw_" + name] = [(r["end"], r.get("filed", "")) for tg in tags for r in bmh.pick_tag(cik, [tg])[1]]
    t1, r1 = bmh.pick_tag(cik, ["CommonStockSharesOutstanding"], "us-gaap")
    t2, r2 = bmh.pick_tag(cik, ["EntityCommonStockSharesOutstanding"], "dei")
    rows = r1 + r2
    if cik in bmh.SHARES_WA_FALLBACK:
        _, rw = bmh.pick_tag(cik, ["WeightedAverageNumberOfSharesOutstandingBasic"], "us-gaap")
        first = min((r["end"] for r in r2 if "start" not in r), default="9999-12-31")
        rows = rows + [{k: x for k, x in r.items() if k != "start"} for r in rw if "start" in r and r["end"] < first
                       and 80 <= (date.fromisoformat(r["end"]) - date.fromisoformat(r["start"])).days <= 100]
    s["shares"] = bmh.instant_series(rows, t, is_share_count=True) if rows else []
    return s


def parts_at(t, s, dd):
    """그날 공개된 같은 분기의 (영업이익, 세전, 법인세, 순이자|None, 결산일)."""
    parts = {n: [e for e in s[n] if e["available"] <= dd] for n in ("opinc", "tax", "pretax")}
    if not all(parts.values()):
        return None
    common = set.intersection(*({e["end"] for e in x} for x in parts.values()))
    if not common:
        return None
    end = max(common)
    lead = max(x[-1]["end"] for x in parts.values())
    if (date.fromisoformat(lead) - date.fromisoformat(end)).days > bmh.MAX_PAIR_LAG_DAYS:
        return None
    o, tx, pt = (at_end(s[n], end, dd) for n in ("opinc", "tax", "pretax"))
    if s.get("ni_zero"):
        return o, pt, tx, 0.0, end                       # 변경 기록 ③: 이자가 영업이익 안에 있다(DE)
    net = component(s["net"], s["raw_net"], end, dd)
    if net not in (None, ABSENT):
        ni = net
    else:
        a, b = component(s["inc"], s["raw_inc"], end, dd), component(s["exp"], s["raw_exp"], end, dd)
        if s.get("no_income") and a is not None:
            a = ABSENT                                    # 변경 기록 ③: 보험사 투자수익은 매출 줄
        if a == ABSENT and b == ABSENT:
            ni = None                                    # 순이자 태그가 그 무렵 하나도 없다 → 결측
        elif a is None or b is None:
            ni = None                                    # 태그는 살아 있는데 그 분기 값이 없다 → 결측
        else:
            ni = (0.0 if a == ABSENT else a) - (0.0 if b == ABSENT else b)
    return o, pt, tx, ni, end


ABSENT = "absent"


def component(sers, raw, end, dd):
    """그 분기 값이 있는 첫 태그의 값. 어느 태그도 결산일 ±200일 안에 공시 행이 없으면 ABSENT(그 무렵 태그 안 씀),
    행은 있는데 4분기 합을 못 만들면 None(결측) — 변경 기록 ②: 4분기 합 시리즈가 아니라 분기 행으로 본다(Codex)."""
    for ser in sers:
        x = at_end(ser, end, dd)
        if x is not None:
            return x
    e = date.fromisoformat(end)
    near = any(abs((date.fromisoformat(en) - e).days) <= bmh.MAX_PAIR_LAG_DAYS for en, fd in raw if fd <= dd)
    return None if near else ABSENT


def rate(t, pt, tx, end, dd, engine_card):
    pt_rate = pt - bmh.oneoff_in_ttm(t, end, "pretax", dd)
    if engine_card:                   # A의 카드 종목: 엔진 그대로
        r = (tx - bmh.oneoff_in_ttm(t, end, "tax", dd)) / pt_rate if pt_rate > 0 else tx / pt
        if bmh.core_tickers().get(t, {}).get("statutory_fallback") and not 0.0 <= r <= 0.40:
            r = 0.21
        return r
    if pt_rate <= 0:
        return 0.21
    r = (tx - bmh.oneoff_in_ttm(t, end, "tax", dd)) / pt_rate
    return r if 0.0 <= r <= 0.40 else 0.21


def core_value(t, s, dd, basis, engine_card=False):
    """basis 'op' = 영업이익 × (1 − 세율), 'opi' = (영업이익 + 순이자) × (1 − 세율)."""
    p = parts_at(t, s, dd)
    if not p:
        return None
    o, pt, tx, ni, end = p
    if engine_card and pt <= 0:
        return None
    b = o if basis == "op" else (o + ni if ni is not None else None)
    if b is None or b <= 0:
        return None
    return b * (1 - rate(t, pt, tx, end, dd, engine_card))


def trigger(t, s, dd, variant):
    """평가일 TTM으로 대상 여부. 돌려주는 것: (basis|None, 태그 결측 여부)."""
    if variant == "A":
        return ("op_card" if t in bmh.core_tickers() else None), False
    p = parts_at(t, s, dd)
    if not p:
        return None, False
    o, pt, tx, ni, end = p
    if variant in ("B", "B+"):
        if o <= 0:
            return None, False
        x = (pt - o) / o
        hit = abs(x) >= THRESH if variant == "B" else x >= THRESH
        return ("op" if hit else None), False
    if ni is None:
        # 변경 기록 ④: 순이자 결측이면 core_earnings.json 종목은 A 그대로
        return ("op_card" if t in bmh.core_tickers() else None), True
    base = o + ni
    if base <= 0:
        return None, False
    x = (pt - o - ni) / base
    hit = abs(x) >= THRESH if variant == "C" else x >= THRESH
    return ("opi" if hit else None), False


def build():
    panel = json.load(open(vr.PANEL))
    by_t = {}
    for r in panel["rows"]:
        by_t.setdefault(r["t"], []).append(r)
    uni = {r["ticker"]: r for r in json.load(open(v.SP500))}
    # 변경 기록 ③: 엔진이 영업이익을 세전이익에서 이자 조정 없이 만드는 종목(DERIVED_OPINC) — 이자가 이미 영업이익 안
    ni_zero = {c for c, (base, comps) in bmh.DERIVED_OPINC.items()
               if "BeforeIncomeTaxes" in base and "Interest" not in repr(comps)}
    out = {}
    only = set(filter(None, os.environ.get("A8_ONLY", "").split(",")))
    for k, (t, rows) in enumerate(sorted(by_t.items())):
        if only and t not in only:
            continue
        cik = uni[t]["cik"].zfill(10)
        data = json.load(open(os.path.join(FACTS, f"{cik}_facts.json")))
        pj = json.load(open(os.path.join(vr.PRICES, f"{t}.json")))
        bars = sorted(pj["daily"], key=lambda b: b["date"])
        daily = [(b["date"], b["c"]) for b in bars if b["date"] >= vr.BAR_START]
        vr._splits.OVERRIDE[t] = [(x["date"], x["ratio"]) for x in (pj.get("splits") or [])]
        d.feh.CIKS[t] = cik
        ep = os.path.join(vr.EPS_DIR, f"{t}.json")
        eps = [{"available": e["available"], "val": e["val"] + bmh.oneoff_in_ttm(t, e["quarter_end"], "eps", asof=e["available"])}
               for e in pit.eps_ttm(data, pj.get("splits") or []) if e["val"]]
        if not eps and os.path.exists(ep):
            eps = sorted(({"available": e["available_date"],
                           "val": e["ttm_eps"] + bmh.oneoff_in_ttm(t, e.get("quarter_end"), "eps", asof=e["available_date"])}
                          for e in json.load(open(ep)) if e.get("ttm_eps")), key=lambda e: e["available"])
        eps_now = lambda dd: bmh.as_of(eps, dd) if eps else None
        filed_all = sorted({row.get("filed") for ns in data["facts"].values() for vv in ns.values()
                            for rr in vv["units"].values() for row in rr if row.get("filed")})
        override_filed = sorted(vr._override_filed(t))
        hstart = bmh.HISTORY_START.get(t, "0000")
        scache, pcache = {}, {}
        res = {}
        for r in rows:
            day, px = r["d"], r["px"]
            state = max((f for f in filed_all if f <= day), default=None)
            ovr = max((f for f in override_filed if f <= day), default="")
            key = (state, ovr)
            if key not in scache:
                try:
                    pit.install(bmh, cik, data, state, ref=day)
                    with contextlib.redirect_stdout(io.StringIO()):
                        scache[key] = state_series(t, cik)
                        scache[key]["ni_zero"] = cik in ni_zero
                        scache[key]["no_income"] = uni[t].get("subIndustry") in INSURER_SUB or t in INSURER_EXTRA
                except Exception as e:
                    print("시리즈 실패", t, day, str(e)[:60], flush=True)
                    scache[key] = None
                finally:
                    pit.reset(bmh)
            s = scache[key]
            y, m_, dd_ = day.split("-")
            wstart = f"{int(y) - 5}-{m_}-{dd_}"
            if hstart <= day:
                wstart = max(wstart, hstart)
            per_dil = lambda dd, p: p * bmh.fx.rate(t, dd) / eps_now(dd) if eps_now(dd) and eps_now(dd) > 0 else None
            e_ = eps_now(day)
            dil_today = per_dil(day, px)
            dil_peer = dil_today if dil_today else (NEG if (e_ is not None and e_ <= 0) else None)
            rr = {}
            for var in VARIANTS:
                basis, miss = trigger(t, s, day, var) if s else (None, False)
                ck = (key, basis)
                if ck not in pcache:
                    if basis is None:
                        vals = {dd: per_dil(dd, p) for dd, p in daily}
                    else:
                        def mcap(dd, p):
                            sh = bmh.as_of(s["shares"], dd)
                            return p * bmh.fx.rate(t, dd) * sh if sh else None
                        bk, eng = ("op", True) if basis == "op_card" else (basis, False)
                        vals = {}
                        for dd, p in daily:
                            m = mcap(dd, p)
                            c = core_value(t, s, dd, bk, eng) if m else None
                            vals[dd] = m / c if (m and c) else None
                    pcache[ck] = {dd: (x if (x and x > 0) else None) for dd, x in vals.items()}
                vals = pcache[ck]
                if basis is None:
                    sc_, _ = vr.self_score_at(vals, eps_now, day, wstart)
                else:
                    sc_, _ = vr.self_score_at(vals, None, day, wstart)
                has = any(x for dd2, x in vals.items() if wstart <= dd2 <= day)
                rr[var] = {"core": basis is not None, "basis": basis, "miss": miss,
                           "noparts": (s is None) or (parts_at(t, s, day) is None),
                           "self": sc_, "has": has, "peer_dil": dil_peer}
            res[day] = rr
        out[t] = res
        if k % 25 == 0:
            print(k, t, flush=True)
    json.dump({"meta": vr.provenance() | {"built": date.today().isoformat(), "panel_meta": panel["meta"]}, "per": out},
              open(OUT_PER, "w"))
    return panel


def rows_for(panel, per, var):
    rows = []
    for r0 in panel["rows"]:
        x = per.get(r0["t"], {}).get(r0["d"], {}).get(var)
        r = dict(r0, self=dict(r0["self"]), peer=dict(r0["peer"]))
        if x is None:
            rows.append(r); continue
        if x["self"] is not None:
            r["self"]["PER"] = x["self"]
        elif x["has"]:
            r["self"]["PER"] = None
        else:
            r["self"].pop("PER", None)
        r["peer"].pop("PER", None); r["peer"].pop("PER_dil", None)
        if x["core"]:
            r["peer"]["PER_dil"] = x["peer_dil"]
        else:
            r["peer"]["PER"] = x["peer_dil"]
        r["core"] = x["core"]
        r["basis"] = x["basis"]; r["miss"] = x["miss"]; r["noparts"] = x.get("noparts")
        rows.append(r)
    return rows


def analyze(panel, per):
    bad = lambda r: any(str(x).startswith(("debt_suspect", "shares_missing")) for x in r["dq"])
    res = {"meta": json.load(open(OUT_PER))["meta"] if os.path.exists(OUT_PER) else None}
    # 패널 대조: A의 PER 자기 점수가 패널과 다른 행
    diff = sum(1 for r in panel["rows"] if (per.get(r["t"], {}).get(r["d"], {}).get("A") or {}).get("self") != r["self"].get("PER")
               and not ((per.get(r["t"], {}).get(r["d"], {}).get("A") or {}).get("self") is None and "PER" not in r["self"]))
    res["A_vs_panel_self_PER_diff_rows"] = diff
    built = {}
    for var in VARIANTS:
        rs = rows_for(panel, per, var)
        vr.add_returns(rs)
        vr.peer_scores(rs)
        built[var] = rs
    for label, keep in (("dq_filtered", lambda r: not bad(r)), ("dq_unfiltered", lambda r: True)):
        sets = {var: [r for r in built[var] if keep(r)] for var in VARIANTS}
        for var in VARIANTS:
            vr.assign(sets[var])
        idx = {var: {(r["t"], r["d"]): r for r in sets[var]} for var in VARIANTS}
        issued_A = [r for r in sets["A"] if r["g_V0"] is not None]
        base = {h: {} for h in (vr.H_MAIN, vr.H_AUX)}
        for h in base:
            for r in issued_A:
                if r[f"r{h}"] is not None:
                    base[h].setdefault(r["m"], []).append(r[f"r{h}"])
        def xret(r, h):
            b = base[h].get(r["m"])
            return (r[f"r{h}"] - float(np.mean(b))) if (r[f"r{h}"] is not None and b and len(b) >= v.MIN_MONTH_N) else None
        months = sorted({r["m"] for r in issued_A})
        def complete(m, h):
            g = [r for r in issued_A if r["m"] == m]
            return len(g) >= v.MIN_MONTH_N and all(r[f"r{h}"] is not None for r in g)
        learn = [m for m in months if vr.LEARN[0] <= m <= vr.LEARN[1] and complete(m, vr.H_MAIN)]
        hold63 = [m for m in months if m >= vr.HOLD_FROM and complete(m, vr.H_AUX)]
        hold126 = [m for m in months if m >= vr.HOLD_FROM and complete(m, vr.H_MAIN)]
        out = {"months": {"learn": learn, "holdout_63": hold63, "holdout_126": hold126}}
        keys = {"verdict": lambda r: r["n_V0"],
                "self": lambda r: r["self_score"] if r["self_vote"] is not None else None,
                "peer": lambda r: r["peer_score"] if r["peer_vote"] is not None else None}

        def ic(var, mlist, key, h):
            ics, w = [], []
            for m in mlist:
                g = [(key(r), xret(r, h)) for r in sets[var] if r["m"] == m and r["g_V0"] is not None]
                g = [(a, b) for a, b in g if a is not None and b is not None]
                if len(g) < v.MIN_MONTH_N or len({a for a, _ in g}) < 2:
                    continue
                ics.append(spearmanr([a for a, _ in g], [b for _, b in g]).correlation); w.append(len(g))
            mu, ci = vr.wmean_ci(ics, w)
            return {"IC": mu, "ci": ci, "months": len(w)}

        norm = lambda b: None if b is None else ("opi" if b == "opi" else "op")

        def dic(var, mlist, key, h, only_switched=False, min_n=None):
            diffs, w = [], []
            for m in mlist:
                g = []
                for r in sets["A"]:
                    if r["m"] != m:
                        continue
                    q = idx[var].get((r["t"], r["d"]))
                    if q is None or r["g_V0"] is None or q["g_V0"] is None:
                        continue
                    if only_switched and norm(q.get("basis")) == norm(r.get("basis")):
                        continue
                    a, b, y = key(q), key(r), xret(r, h)
                    if a is None or b is None or y is None:
                        continue
                    g.append((a, b, y))
                if len(g) < (min_n or v.MIN_MONTH_N) or len({x[0] for x in g}) < 2 or len({x[1] for x in g}) < 2:
                    continue
                y = [x[2] for x in g]
                diffs.append(spearmanr([x[0] for x in g], y).correlation - spearmanr([x[1] for x in g], y).correlation)
                w.append(len(g))
            mu, ci = vr.wmean_ci(diffs, w)
            return {"dIC": mu, "ci": ci, "months": len(w)}

        last = max(months)
        for var in VARIANTS:
            rs = sets[var]
            o = {"core_share_all": round(sum(1 for r in rs if r.get("core")) / len(rs), 4),
                 "core_share_last": round(sum(1 for r in rs if r.get("core") and r["m"] == last) / max(1, sum(1 for r in rs if r["m"] == last)), 4),
                 "core_rows": sum(1 for r in rs if r.get("core")),
                 "basis_diff_vs_A": sum(1 for r in rs if norm(r.get("basis")) != norm((idx["A"].get((r["t"], r["d"])) or {}).get("basis"))),
                 "noparts_rows": sum(1 for r in rs if r.get("noparts")), "rows": len(rs),
                 "tag_missing_rows": sum(1 for r in rs if r.get("miss")),
                 "verdict_changed_vs_A": sum(1 for r in rs if r["g_V0"] != (idx["A"].get((r["t"], r["d"])) or {}).get("g_V0")),
                 "issued": sum(1 for r in rs if r["g_V0"] is not None)}
            for kn, kf in keys.items():
                o[f"IC_{kn}_learn126"] = ic(var, learn, kf, vr.H_MAIN)
            o["IC_verdict_hold63"] = ic(var, hold63, keys["verdict"], vr.H_AUX)
            if var != "A":
                for kn, kf in keys.items():
                    o[f"dIC_{kn}_learn126"] = dic(var, learn, kf, vr.H_MAIN)
                o["dIC_verdict_learn63"] = dic(var, learn, keys["verdict"], vr.H_AUX)
                o["dIC_verdict_hold63"] = dic(var, hold63, keys["verdict"], vr.H_AUX)
                if hold126:
                    o["dIC_verdict_hold126"] = dic(var, hold126, keys["verdict"], vr.H_MAIN)
                # 변경 기록 ⑤: 기준이 A와 다른 행만의 짝지은 ΔIC(서술, 달마다 10행 이상)
                perself = lambda r: r["self"].get("PER")
                o["switched_dIC_learn126"] = {kn: dic(var, learn, kf, vr.H_MAIN, only_switched=True, min_n=10)
                                              for kn, kf in (("PER_self", perself), ("self", keys["self"]), ("verdict", keys["verdict"]))}
                # 기준이 A와 다른 행의 PER 자기 점수 IC(서술)
                sw = [(r, idx["A"].get((r["t"], r["d"]))) for r in rs if r["m"] in learn]
                sw = [(r, a) for r, a in sw if a is not None and norm(r.get("basis")) != norm(a.get("basis"))]
                ys = [(r["self"].get("PER"), xret(a, vr.H_MAIN)) for r, a in sw]
                ys = [(a, b) for a, b in ys if a is not None and b is not None]
                o["switched_rows_PER_self_pooled_IC"] = (float(spearmanr([a for a, _ in ys], [b for _, b in ys]).correlation)
                                                         if len(ys) >= 30 else None, len(ys))
                ci = o["dIC_verdict_learn126"]["ci"]; pt_ = o["dIC_verdict_learn126"]["dIC"]
                h63 = o["dIC_verdict_hold63"]["dIC"]
                o["rule_fail"] = bool((ci and ci[1] < 0) or (h63 is not None and pt_ is not None and h63 < 0 and pt_ < -0.01))
            out[var] = o
        order = ["C", "C+", "B+", "B"]
        out["recommend"] = next((x for x in order if not out[x]["rule_fail"]), "A")
        res[label] = out
    json.dump(res, open(RESULT, "w"), ensure_ascii=False, indent=1)
    for label in ("dq_filtered", "dq_unfiltered"):
        x = res[label]
        print(f"\n== {label} 학습 {len(x['months']['learn'])}개월 · 홀드아웃63 {len(x['months']['holdout_63'])}")
        for var in VARIANTS:
            o = x[var]
            print(f"  {var}: 본업 행 {o['core_share_all']:.1%}(최근 {o['core_share_last']:.1%}) · A와 기준 다른 행 {o['basis_diff_vs_A']}"
                  f" · 태그결측 {o['tag_missing_rows']} · 판정 바뀐 행 {o['verdict_changed_vs_A']} · IC판정 {o['IC_verdict_learn126']['IC']:.4f}")
            if var != "A":
                f = lambda z: f"{z['dIC']:+.4f} {[round(c, 4) for c in z['ci']] if z['ci'] else None}" if z["dIC"] is not None else "None"
                print(f"     ΔIC 판정 {f(o['dIC_verdict_learn126'])} · 자기 {f(o['dIC_self_learn126'])} · 동종업 {f(o['dIC_peer_learn126'])}"
                      f" · 홀드63 {f(o['dIC_verdict_hold63'])} · 탈락 {o['rule_fail']} · 바뀐행 PER IC {o['switched_rows_PER_self_pooled_IC']}")
                print("     바뀐 행만 ΔIC:", {k: f(z) for k, z in o["switched_dIC_learn126"].items()},
                      f"· 평가 불가 행 {o['noparts_rows']}/{o['rows']}")
        print("  추천:", x["recommend"])


def main():
    if "--analyze" in sys.argv:
        panel = json.load(open(vr.PANEL))
    else:
        panel = build()
    analyze(panel, json.load(open(OUT_PER))["per"])


if __name__ == "__main__":
    main()
