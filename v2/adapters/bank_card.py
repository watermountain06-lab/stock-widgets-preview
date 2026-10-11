#!/usr/bin/env python3
"""은행 카드 데이터 — research/bank_rim_prereg.md 4판. RIM·관문·자기 이력(P/TBV·PER)·동종업(S&P500 은행 13곳)·적정주가 밴드.

    python3 v2/adapters/bank_card.py JPM --json v2/JPM_bank.json

자기 이력 배수는 카드 일봉(루트 카드) 날짜마다 그날까지 접수된 분기말 TCE·주식 수·TTM EPS로 계산한다.
동종업은 같은 Bank 정의로 기준일 하루치를 계산해 v2/peer_universe/banks.json에 남긴다(가격은 Yahoo 종가).
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
sys.path.insert(0, HERE)
sys.path.insert(0, V2)
sys.path.insert(0, os.path.join(REPO, "scripts"))
import bank_rim as br  # noqa: E402
import build_multiple_history as bmh  # noqa: E402
import sector_universe as su  # noqa: E402
import fetch_eps_history as feh  # noqa: E402

SUBS = ("Diversified Banks", "Regional Banks")
PEER_DIR = os.path.join(V2, "peer_universe", "banks")
MIN_PEERS = 8


def eps_file(ticker, cik, directory):
    path = os.path.join(directory, f"{ticker}_eps_history.json")
    if not os.path.exists(path):
        subprocess.run([sys.executable, os.path.join(REPO, "scripts", "fetch_eps_history.py"), ticker,
                        "--cik", cik, "--out", path], capture_output=True, text=True)
        time.sleep(0.6)
    return path if os.path.exists(path) else None


def ptbv_steps(bank):
    """[(가용일, 분기말, TCE, 주식 수)] — P/TBV 분모 계단."""
    out = []
    for e in sorted(bank.se):
        t, s = bank.tce(e), bank.shares(e)
        if t and s:
            out.append((max(t[1], s[1]), e, t[0], s[0]))
    return sorted(out)


def pct_rank(vals, cur):
    return sum(1 for v in vals if v < cur) / len(vals) * 100


def _qavail(bank, e):
    """분기말 e가 열리는 날 — 회사 정의 자본 예외(WFC)가 있으면 보도자료일이 10-Q보다 빠르다(Codex)."""
    o = br.EQUITY_OVERRIDE.get(bank.t, {}).get(e) if bank.ov else None
    so = br.SHARES_OVERRIDE.get(bank.t, {}).get(e) if bank.ov else None
    # 주식 수도 보도자료 값일 때만(WFC) 보도자료일에 연다 — BAC처럼 주식 수는 10-Q 태그면 그 분기 P/TBV는 10-Q 날 열린다
    return min(bank.se[e][1], max(o["filed"], so["filed"])) if o and so else bank.se[e][1]


def self_history(bank, daily, eps_path):
    steps = ptbv_steps(bank)
    eps = json.load(open(eps_path)) if eps_path else []
    res = {}
    series = {"ptbv": [], "per": []}
    for d in daily:
        day, px = d[0], d[4]
        # 그날 접수된 가장 최근 분기말의 TCE만 쓴다(8-3) — 그 분기에 TCE가 없으면 그날은 빈 날
        avail = [e for e in bank.se if _qavail(bank, e) <= day]
        if avail:
            e = max(avail)
            st = [x for x in steps if x[1] == e and x[0] <= day]
            fresh = (br.date.fromisoformat(day) - br.date.fromisoformat(e)).days <= 200
            if st and fresh:
                _, _, t, s = st[-1]
                series["ptbv"].append((day, px * s / t if t > 0 else "negative"))
        ep = [p for p in eps if p["available_date"] <= day]
        if ep:
            v = ep[-1]["ttm_eps"]
            series["per"].append((day, px / v if v > 0 else "negative"))
    last = daily[-1][0]
    for k, ser in series.items():
        vals = [v for _, v in ser if isinstance(v, float)]
        n_all = len(ser)
        today = [v for dd, v in ser if dd == last]
        if not vals:
            res[k] = None
            continue
        srt = sorted(vals)
        q = lambda p: srt[int((len(srt) - 1) * p)]
        cur = today[0] if today else None
        neg = cur == "negative"
        cur_num = cur if isinstance(cur, float) else None
        res[k] = {"current": cur_num, "min": srt[0], "median": q(0.5), "max": srt[-1], "days": n_all,
                  "gapDays": len(daily) - n_all,
                  "percentile": (100.0 if neg else pct_rank(vals, cur_num)) if (neg or cur_num) else None,
                  "score": (0.0 if neg else 100 - pct_rank(vals, cur_num)) if (neg or cur_num) else None,   # 7-9: 분모 ≤ 0 → 꼴찌(0점)
                  "currentNote": None if cur_num else ("negative" if neg else "missing"),
                  "firstDay": ser[0][0] if ser else None}
        if k == "per" and cur_num:
            start = daily[-252][0] if len(daily) >= 252 else daily[0][0]
            yr = sorted(v for dd, v in ser if isinstance(v, float) and dd >= start)
            yq = lambda p: yr[int((len(yr) - 1) * p)]
            px = daily[-1][4]
            res["fairBand"] = {"per_p25": yq(0.25), "per_p75": yq(0.75),
                               "low": int(round(px * yq(0.25) / cur_num / 10) * 10),
                               "high": int(round(px * yq(0.75) / cur_num / 10) * 10), "asOf": last}
    return res


def peers(asof, self_ticker):
    rows = [r for r in su.sp500_rows() if r.get("subIndustry") in SUBS]
    os.makedirs(PEER_DIR, exist_ok=True)
    out = {"asOf": asof, "subIndustries": list(SUBS), "tickers": {}, "skipped": {}}
    for r in rows:
        t, cik = r["ticker"], str(r["cik"]).zfill(10)
        try:
            bars, splits = su.yahoo(t, asof)
            if not bars or bars[-1][0] != asof:
                out["skipped"][t] = "기준일 종가 없음"
                continue
            bank = br.Bank(t, cik, asof, overrides=True)   # 다른 은행도 회사 정의 보정값으로(5판 9-5, 2026-10-05 사용자 결정 — BAC가 동종업 1.66배·자기 카드 1.85배로 갈리던 것)
            m = br.multiples_on(bank, asof, bars[-1][4], eps_file(t, cik, PEER_DIR))
            if bank.ed >= 7 and "ptbv" in m:   # 7판 11-6: 그 분기 CE·TCE·S와 N5-1·N5-2를 통과해야 동종업 P/TBV에 든다
                ok7, why7 = br.peer_ok7(bank, m["ptbv_end"])
                if not ok7:
                    m.pop("ptbv"); m["ptbv_missing"] = f"7판 동종업 관문: {why7}"
            if "ptbv" not in m:
                out["skipped"][t + ":ptbv"] = m.get("ptbv_missing", "분기말 자본 자료 없음")
            m["tags"] = {"equity": "StockholdersEquity", "preferred": ("7판 표: " + (bank.pref_tbl.get("path") or "·".join(bank.pref_tbl.get("tags") or ["분리 불가"]))) if bank.pref_tbl is not None else "PreferredStockLiquidationPreferenceValue" if bank.pref_liq else ("PreferredStockValue" if bank.pref_val else "없음(우선주 이력 없음)" if not bank.pref_ever else "결측"),
                         "intangibles": "IntangibleAssetsNetExcludingGoodwill" if bank.ia else "Finite+Indefinite" if (bank.fin or bank.ind) else "OtherIntangibleAssetsNet" if bank.oth else "없음",
                         "shares": "Issued−Treasury" if bank.issued else "CommonStockSharesOutstanding"}
            out["tickers"][t] = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in m.items()}
        except Exception as e:
            out["skipped"][t] = f"오류: {type(e).__name__}: {e}"
        time.sleep(0.4)
    json.dump(out, open(os.path.join(V2, "peer_universe", "banks.json"), "w"), ensure_ascii=False, indent=1)
    return out


def peer_scores(self_ticker, mine, uni):
    res = {}
    for k in ("ptbv", "per"):
        mv = mine.get(k)
        vals = {t: v[k] for t, v in uni["tickers"].items() if t != self_ticker and k in v}
        if k == "ptbv":   # 유형자본 음수인 동종 종목은 뺀다 — 일반 카드의 PBR 규칙과 같다(C11, 2026-10-04)
            vals = {t: v for t, v in vals.items() if v != "negative"}
        if k == "per":   # 동종 종목 적자 PER은 꼴찌로 세지 않고 뺀다 — A3를 동종 종목에도(C9, 2026-10-04). 은행은 매출 태그가 없어 순이익률 2% 기준은 못 쓴다
            vals = {t: v for t, v in vals.items() if v != "negative"}
        if mv is None or len(vals) < MIN_PEERS:
            res[k] = {"score": None, "peers": len(vals), "note": "본인 값 없음" if mv is None else f"동종업 {len(vals)}곳뿐"}
            continue
        nums = sorted(v for v in vals.values() if v != "negative")
        cheaper = len(nums) if mv == "negative" else sum(1 for x in nums if x < mv)
        score = 0.0 if mv == "negative" else 100 - cheaper / len(vals) * 100
        res[k] = {"score": round(score, 1), "rank": cheaper + 1, "peers": len(vals),
                  "median": nums[len(nums) // 2] if nums else None, "value": mv}
    return res


def qends_before_n(end, n):
    """end 직전 n개 분기말(end 제외) — 신호 ④의 비교 창."""
    return br.qends_before(end, n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--json")
    ap.add_argument("--no-peers", action="store_true")
    ap.add_argument("--reuse-peers", action="store_true",
                    help="매일 가격 재빌드(2026-10-06) — 비교 은행 값을 새로 받지 않고 지금 peer_universe/banks.json(토요일 기준)을 쓴다")
    a = ap.parse_args()
    t = a.ticker.upper()
    cik = feh.CIKS.get(t) or next(str(r["cik"]).zfill(10) for r in su.sp500_rows() if r["ticker"] == t)
    daily = bmh.load_daily(t)
    asof, px = daily[-1][0], daily[-1][4]
    bank = br.Bank(t, cik, asof, overrides=True)   # 평가일(카드 일봉 마지막 날) 이후 접수 사실은 쓰지 않는다(Codex). 회사 정의 예외는 본인 카드에만
    frozen = None
    if bank.ed >= 7:
        # 7판 11-6: 최신 분기가 N1~N5를 통과하지 못하면 그 분기를 반영하지 않는다 — 그 분기 공시 전날을 기준으로 다시 만든다(가격은 그대로)
        L = max(e for e in bank.se if bank.se[e][1] <= asof)
        c7 = br.checks7(bank, L)
        if not c7["ok"]:
            frozen = {"quarter": L, "stop": c7["stop"], "detail": {k: c7[k] for k in c7["stop"]}, "skipped": []}
            # 직전 통과 분기까지 거슬러 올라간다 — 한 분기만 되돌리면 그 분기도 미통과일 때 그대로 계산했다(Codex 3차). 8개 분기 안에 없으면 RIM·P/TBV 기권
            for _ in range(8):
                cut = (date.fromisoformat(bank.se[L][1]) - timedelta(days=1)).isoformat()
                bank = br.Bank(t, cik, cut)
                if not bank.se:
                    break
                L = max(bank.se)
                c7 = br.checks7(bank, L)
                if c7["ok"]:
                    break
                frozen["skipped"].append(L)
            frozen["asof_cut"], frozen["used_quarter"] = cut, (L if c7["ok"] else None)
        g = {"N": c7}
    else:
        g = br.gates(bank, os.path.join(V2, "research", f"bank_gate_{t}.json"))
    r = br.rim(bank, price=px)
    eps_path = eps_file(t, cik, os.path.join(REPO, "scripts"))
    hist = self_history(bank, daily, eps_path)
    if bank.ed >= 7:
        if frozen and not frozen.get("used_quarter"):   # 통과한 분기가 없다 — RIM·P/TBV 기권
            r = {"abstain": "관문을 통과한 분기가 최근 8분기 안에 없음"}
            hist["ptbv"] = None
        if r.get("L") and (date.fromisoformat(asof) - date.fromisoformat(r["L"])).days > 200:   # 11-6: 갱신이 200일 넘게 멈추면 RIM도 기권(8-3의 P/TBV와 같은 기준, Fable 2차)
            r = {"abstain": f"재무 기준 분기 {r['L']}가 200일 넘게 낡음(관문 정지)"}
        r["reference_only"] = False
        r["frozen"] = frozen
        # 11-5 신호 ④(결과를 본 뒤 개정, 2026-10-11 사용자 결정): 출발 TTM의 네 분기 가운데 순이익이 최근 8개 분기 중앙값에서 40% 넘게 벗어난 분기가 있으면
        # 표시하고, 그 분기를 중앙값으로 바꾼 ROE를 함께 적는다. 1차 기준(TTM 대 8개 TTM 중앙값 15%)은 이익이 꾸준히 느는 은행 6곳에 켜졌다.
        if r.get("L"):
            L_ = r["L"]
            q8 = [bank.ni.get(e) for e in [L_] + br.qends_before(L_, 7)]
            if all(q8):
                med = sorted(x[0] for x in q8)[3:5]
                med = sum(med) / 2
                odd = [e for e in [L_] + br.qends_before(L_, 3) if med > 0 and abs(bank.ni[e][0] / med - 1) > 0.40]
                b0 = bank.ce(br.qends_before(L_, 4)[-1])
                n0 = bank.ni_ttm(L_)
                if odd and b0 and n0:
                    alt = n0[0] - sum(bank.ni[e][0] for e in odd) + med * len(odd)
                    r["signal4"] = {"quarters": odd, "median_q_ni": med, "roe_at_median": alt / b0[0],
                                    "note": "최근 8분기 중앙값에서 40% 넘게 벗어난 분기 — 일회성일 수도, 실적 수준 변화일 수도 있다"}
    else:
        # 관문 효력표(사전 등록 7-7): G1·G2 미통과 → P/TBV 없음(자기 이력·동종업), G2·G3·G4·G5 미통과 → RIM 참고용
        ok = {k: g[k]["pass"] for k in ("G1", "G2", "G3", "G4", "G5")}
        if not (ok["G1"] and ok["G2"]):
            hist["ptbv"] = None
        r["reference_only"] = not (ok["G2"] and ok["G3"] and ok["G4"] and ok["G5"])
    if getattr(bank, "unadjustable", None):
        r["unadjustable_quarters"] = sorted(bank.unadjustable)
    out = {"ticker": t, "asOf": asof, "price": px, "edition": bank.ed,
           "gates": ({"N": g["N"]["ok"]} if bank.ed >= 7 else {k: v["pass"] for k, v in g.items() if isinstance(v, dict)}),
           "gateRows": g, "rim": r, "self": hist}
    if not a.no_peers:
        uni = json.load(open(os.path.join(V2, "peer_universe", "banks.json"))) if a.reuse_peers else peers(asof, t)
        mine = {k: ("negative" if hist.get(k) and hist[k]["currentNote"] == "negative" else hist[k]["current"] if hist.get(k) else None)
                for k in ("ptbv", "per")}
        out["peer"] = peer_scores(t, mine, uni)
    print(json.dumps({k: out[k] for k in ("asOf", "price", "gates")}, ensure_ascii=False))
    print("RIM", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items() if k != "grid"})
    for k in ("ptbv", "per"):
        v = hist.get(k)
        print("자기", k, v and {kk: (round(vv, 3) if isinstance(vv, float) else vv) for kk, vv in v.items()})
    print("밴드", hist.get("fairBand"))
    if "peer" in out:
        print("동종업", out["peer"])
    if a.json:
        json.dump(out, open(a.json, "w"), ensure_ascii=False, indent=1, default=str)
        print("저장:", a.json)


if __name__ == "__main__":
    main()
