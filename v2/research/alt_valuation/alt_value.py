"""DCF 말고 다른 절대가치 방법을 방법별로 나란히 계산한다 — 검증용 실험(카드·main·12-01 패널에 쓰지 않는다).

평가일 하나(학습 패널의 마지막 달)에서 S&P500 비금융 종목마다 DCF·RIM·그레이엄·DDM의 주당 가치와 등급을 낸다.
수익률은 쓰지 않는다. 가격·DCF 기본 내재가치는 봉인된 학습 패널(F1~F4 기준판) 그 달 행을 그대로 쓴다.
가정은 alt_valuation/README.md에 결과를 보기 전에 적었다.

    python3 v2/research/alt_valuation/alt_value.py            # → alt_valuation/alt_value_<월>.json
"""
import contextlib
import functools
import io
import json
import math
import os
import statistics
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.dirname(HERE)
sys.path.insert(0, RES)
sys.path.insert(0, os.path.dirname(RES))
import verdict_replay as vr  # noqa: E402
import pit  # noqa: E402
import splits as _splits  # noqa: E402

bmh, d = vr.bmh, vr.d
MONTH = "2026-09"
R = 0.10                 # 할인율 — DCF와 같다
RIM_YEARS = 10           # ROE가 할인율까지 선형으로 내려가는 해 수(그 뒤 초과이익 0)
DDM_YEARS, DDM_TERM, DDM_GCAP = 5, 0.025, 0.10
EPS_STALE = 200          # EPS 기간 끝이 이보다 오래되면 표시만 한다(F5b와 같은 날수 — 값은 그대로 쓴다)
CARDS = {os.path.basename(p)[:-len("_full_widget.html")] for p in
         __import__("glob").glob(os.path.join(os.path.dirname(RES), "*_full_widget.html"))}


def level(px, value):
    return vr.ratio_level(px, value)


def graham(eps, bps):
    return math.sqrt(22.5 * eps * bps) if eps and bps and eps > 0 and bps > 0 else None


def rim(bps, eps, payout):
    """B0 + Σ (ROE_t − r)·B_(t−1) / (1+r)^t. ROE는 지금 값에서 RIM_YEARS년에 걸쳐 r로 선형, 자본은 ROE·(1−배당성향)만큼 큰다."""
    if not bps or bps <= 0 or eps is None:
        return None
    roe0 = eps / bps
    b, v = bps, bps
    for t in range(1, RIM_YEARS + 1):
        roe = roe0 + (R - roe0) * t / RIM_YEARS
        v += (roe - R) * b / (1 + R) ** t
        b *= 1 + roe * (1 - payout)
    return v


def ddm(dps_hist):
    """최근 5개 회계연도 모두 배당한 종목만. 5년 배당 성장률(0~10%로 자름)로 5년, 그 뒤 2.5%."""
    if len(dps_hist) < 6 or any(x <= 0 for x in dps_hist[-6:]):
        return None, None
    d0, d5 = dps_hist[-1], dps_hist[-6]
    g = min(max((d0 / d5) ** (1 / 5) - 1, 0.0), DDM_GCAP)
    v, dt = 0.0, d0
    for t in range(1, DDM_YEARS + 1):
        dt *= 1 + g
        v += dt / (1 + R) ** t
    v += dt * (1 + DDM_TERM) / (R - DDM_TERM) / (1 + R) ** DDM_YEARS
    return v, g


def fy_dps(data, day, split_list):
    """그날까지 공시된 회계연도 주당 배당(선언 기준, 없으면 지급 기준) — 첫 공시값, 분할은 공시일 기준으로 맞춘다."""
    g = data.get("facts", {}).get("us-gaap", {})
    for tag in ("CommonStockDividendsPerShareDeclared", "CommonStockDividendsPerShareCashPaid"):
        best = {}
        for r in g.get(tag, {}).get("units", {}).get("USD/shares", []):
            if "start" not in r or r.get("filed", "9999") > day:
                continue
            days = (date.fromisoformat(r["end"]) - date.fromisoformat(r["start"])).days
            if not 350 <= days <= 380:
                continue
            if r["end"] not in best or r["filed"] < best[r["end"]]["filed"]:
                best[r["end"]] = r
        if best:
            out = []
            for end in sorted(best):
                r = best[end]
                ratio = 1.0
                for s in split_list:
                    if r["filed"] < s["date"]:
                        ratio *= s["ratio"]
                out.append(r["val"] / ratio)
            return out, tag
    return [], None


def main():
    rows = [r for r in json.load(open(vr.PANEL))["rows"] if r["m"] == MONTH]
    cik = {r["ticker"]: r["cik"].zfill(10) for r in json.load(open(vr.v.SP500))}
    out = []
    for k, r in enumerate(rows):
        t, day = r["t"], r["d"]
        c = cik[t]
        data = json.load(open(os.path.join(vr.FACTS, f"{c}_facts.json")))
        pj = json.load(open(os.path.join(vr.PRICES, f"{t}.json")))
        keep_sp, ign_sp = _splits.clean([(s["date"], s["ratio"]) for s in (pj.get("splits") or [])])
        split_list = [{"date": d0, "ratio": r0} for d0, r0 in sorted(keep_sp + ign_sp)]
        _splits.OVERRIDE[t] = [(s["date"], s["ratio"]) for s in (pj.get("splits") or [])]
        d.feh.CIKS[t] = c
        bmh._facts = functools.lru_cache(maxsize=2)(lambda cc, _data=data: _data if cc == c else {})
        state = max((row.get("filed") for ns in data["facts"].values() for vv in ns.values()
                     for rr in vv["units"].values() for row in rr if row.get("filed") and row["filed"] <= day), default=None)
        rec = {"t": t, "sec": r["sec"], "card": t in CARDS, "px": r.get("px_then", r["px"]), "dcf": r["base"] if r["dcf_ok"] else None}
        try:
            pit.install(bmh, c, data, state, ref=day)
            with contextlib.redirect_stdout(io.StringIO()):
                b = d.base_inputs(t, day)
        except Exception as e:
            b = {}
            rec["err"] = str(e)[:60]
        finally:
            pit.reset(bmh)
        eps_l = [e for e in pit.eps_ttm(data, split_list) if e["available"] <= day and e["val"]]
        eps_e = eps_l[-1] if eps_l else None
        eps = eps_e["val"] if eps_e else None
        rec["eps_age"] = (date.fromisoformat(day) - date.fromisoformat(eps_e["quarter_end"])).days if eps_e else None
        sh, eq = b.get("shares"), b.get("equity")
        bps = eq / sh if (sh and eq is not None) else None
        dps, dtag = fy_dps(data, day, split_list)
        payout = min(max(dps[-1] / eps, 0.0), 1.0) if (dps and eps and eps > 0) else 0.0
        dv, g = ddm(dps)
        rec.update({"eps": eps, "bps": bps, "roe": (eps / bps) if (eps is not None and bps and bps > 0) else None,
                    "dps": dps[-1] if dps else None, "dps_tag": dtag, "payout": payout, "ddm_g": g,
                    "graham": graham(eps, bps), "rim": rim(bps, eps, payout), "ddm": dv})
        vals = {m: rec[m] for m in ("dcf", "rim", "graham", "ddm") if rec[m] is not None}
        rec["n_methods"] = len(vals)
        rec["median"] = statistics.median(vals.values()) if len(vals) >= 2 else None
        for m in ("dcf", "rim", "graham", "ddm", "median"):
            rec[f"lv_{m}"] = level(rec["px"], rec[m]) if rec[m] is not None else None
            rec[f"x_{m}"] = (rec["px"] / rec[m]) if (rec[m] and rec[m] > 0) else None
        out.append(rec)
        if k % 50 == 0:
            print(k, t, flush=True)
    path = os.path.join(HERE, f"alt_value_{MONTH}.json")
    json.dump({"month": MONTH, "r": R, "n": len(out), "rows": out}, open(path, "w"), indent=1, default=str)
    print("rows", len(out), "→", path)


if __name__ == "__main__":
    main()
