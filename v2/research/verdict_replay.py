#!/usr/bin/env python3
"""종합 판정 시점 재현 — verdict_replay_prereg.md(2026-09-30 고정)를 그대로 구현한다.

S&P500 통제 유니버스(금융·제외 4종목 빼고)를 매월 마지막 거래일마다 **그때 공시된 자료만으로** 세 칸
(자기 이력·동종업·현금흐름)을 다시 매기고, 현금흐름 칸의 네 변형(V0 지금 · V1 비중 축소 · V2 시장 백분위 ·
V3 업종 백분위)으로 카드 JS와 같은 합산 규칙의 판정을 낸다.

- 현금흐름: build_dcf.base_inputs(asof)·history(asof)·scenarios(기본값 그대로 — REINVEST_LEAD·PATH_MODE).
- 자기 이력: build_multiple_history.main()의 시리즈·배수 계산을 그대로 옮겼다(엔진 파일은 고치지 않는다).
  평가일 기준 과거 5년 창, 오늘 분모 0 이하 → 0점, 분모 없음 → 그 배수 제외(카드 규칙).
- 동종업: 평가일 같은 날 S&P500 같은 GICS 섹터(자기 제외) 배수 순위 — build_peer_score.peer_score와 같은 산식.
  동종업 쪽은 모두 공시 희석 EPS 기준 PER(카드의 S&P500 비교군 파일과 같은 기준), 본인 PER이 본업 기준이면 PER을 뺀다.

자료: research/.prices10y(10년 일봉·분할), .facts_20261002(지금 엔진 태그), .eps_20261002 — fetch_replay_data.py.

    python3 v2/research/verdict_replay.py            # 패널 생성 + 분석
    python3 v2/research/verdict_replay.py --analyze  # 저장된 패널로 분석만

5년 보완 관문(`five_year_gate_prereg.md`)용 패널은 수익률 없이 행만 만든다(4절 1단계 — 기본 실행과 분석은 그대로):

    python3 v2/research/verdict_replay.py --build-only --dcf-window rolling --months 2021-10 2024-03 --panel PATH   # 시험 구간
    python3 v2/research/verdict_replay.py --build-only --dcf-window rolling --months 2024-06 2026-09 --panel PATH   # 학습 구간 롤링 재실행
"""
import contextlib
import functools
import io
import json
import math
import os
import subprocess
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, V2)
import numpy as np  # noqa: E402
from scipy.stats import spearmanr, rankdata  # noqa: E402
import valuation_judges_test as v  # noqa: E402  (boot_weighted, SP500, EXCLUDE, d = build_dcf)
import build_multiple_history as bmh  # noqa: E402
import pit  # noqa: E402  (C8 — 평가일마다 그날까지 공시된 행만)
pit.capture(bmh)
import splits as _splits  # noqa: E402

d = v.d
PRICES = os.path.join(HERE, ".prices10y")
FACTS = os.path.join(HERE, ".facts_20261002")
EPS_DIR = os.path.join(HERE, ".eps_20261002")
PANEL = os.path.join(HERE, "verdict_replay_panel.json")
RESULT = os.path.join(HERE, "verdict_replay_result.json")
START_MONTH = "2024-06"
END_MONTH = "2026-09"
BAR_START = "2019-05-01"          # 2024-10 평가일의 5년 창을 덮는다
# 현금흐름 칸의 이력 창: "fixed" = 카드와 같은 고정 창(build_dcf.WINDOW_START 2021-07-01~), "rolling" = 평가일 기준 5.25년
# (five_year_gate_prereg.md 2절 — 관문 패널에서만). 기본 실행은 fixed 그대로.
DCF_WINDOW = "fixed"
HASH_LEN = 16                     # 관문 봉인은 전체 길이(64)
METRICS = ["PER", "PBR", "PSR", "PCR", "EV/EBITDA"]
MIN_PEERS = 8
LEARN = ("2024-10", "2026-03")
HOLD_FROM = "2026-04"
H_MAIN, H_AUX = 126, 63
NEG = "negative"


# ───────────────────────── 패널 ─────────────────────────

def multiple_series(t, cik, daily, eps):
    """build_multiple_history.main()과 같은 시리즈로 날짜별 배수와 분모를 낸다.

    돌려주는 것: {label: {day: value>0 | NEG | None}} (NEG = 그날 분모 0 이하), core 여부,
    그리고 동종업용 희석 PER(본업 종목도 공시 EPS 기준).
    """
    series = {}
    for name, tags in bmh.FLOW_TAGS.items():
        tag, rows = bmh.pick_tag(cik, tags)
        if rows:
            series[name] = bmh.ttm_series(bmh.quarterly_flow(rows, t))
    for name, tags in bmh.INSTANT_TAGS.items():
        if name == "shares":
            t1, r1 = bmh.pick_tag(cik, ["CommonStockSharesOutstanding"], "us-gaap")
            t2, r2 = bmh.pick_tag(cik, ["EntityCommonStockSharesOutstanding"], "dei")
            rows = r1 + r2
            if cik in bmh.SHARES_WA_FALLBACK:
                _, rw = bmh.pick_tag(cik, ["WeightedAverageNumberOfSharesOutstandingBasic"], "us-gaap")
                first = min((r["end"] for r in r2 if "start" not in r), default="9999-12-31")
                extra = [{k: x for k, x in r.items() if k != "start"} for r in rw if "start" in r and r["end"] < first
                         and 80 <= (date.fromisoformat(r["end"]) - date.fromisoformat(r["start"])).days <= 100]
                rows = rows + extra
        else:
            tag, rows = bmh.pick_tag(cik, tags, "us-gaap")
        if rows:
            series[name] = bmh.instant_series(rows, t, is_share_count=(name == "shares"))
    for name, tags in bmh.EV_COMPONENTS.items():
        series[name] = bmh.ev_component(cik, name, tags)
    for name, tags in bmh.EBITDA_TAGS.items():
        if name == "dda":
            tag, q = bmh.dda_quarters(cik, t)
        else:
            tag, rows = bmh.pick_tag(cik, tags)
            q = bmh.quarterly_flow(rows, t) if rows else []
        series[name] = bmh.ttm_series(q) if q else []
    core = t in bmh.core_tickers()
    if core:
        for name, tags in bmh.CORE_TAX_TAGS.items():
            tag, rows = bmh.pick_tag(cik, tags)
            series[name] = bmh.ttm_series(bmh.quarterly_flow(rows, t)) if rows else []
            if name == "pretax" and not series[name]:
                _, nr = bmh.pick_tag(cik, ["NetIncomeLoss"]); _, tr = bmh.pick_tag(cik, bmh.CORE_TAX_TAGS["tax"])
                nq = {e["end"]: e for e in bmh.quarterly_flow(nr, t)}; tq = {e["end"]: e for e in bmh.quarterly_flow(tr, t)}
                merged = [dict(nq[k], val=nq[k]["val"] + tq[k]["val"], filed=max(nq[k]["filed"], tq[k]["filed"])) for k in sorted(nq) if k in tq]
                series[name] = bmh.ttm_series(merged)
    as_of = bmh.as_of

    def core_earnings(dd):
        parts = {n: [e for e in series.get(n, []) if e["available"] <= dd] for n in ("opinc", "tax", "pretax")}
        if not all(parts.values()):
            return None
        common = set.intersection(*({e["end"] for e in x} for x in parts.values()))
        if not common:
            return None
        end = max(common)
        lead = max(x[-1]["end"] for x in parts.values())
        if (date.fromisoformat(lead) - date.fromisoformat(end)).days > bmh.MAX_PAIR_LAG_DAYS:
            return None
        o, tx, pt = ([e for e in parts[n] if e["end"] == end][-1]["val"] for n in ("opinc", "tax", "pretax"))
        if pt <= 0 or o <= 0:
            return None
        r = tx / pt
        if bmh.core_tickers().get(t, {}).get("statutory_fallback") and not 0.0 <= r <= 0.40:
            r = 0.21
        return o * (1 - r)

    def mcap(dd, px):
        sh = as_of(series.get("shares", []), dd)
        return px * bmh.fx.rate(t, dd) * sh if sh else None

    def ev(dd, px):
        m = mcap(dd, px)
        if not m:
            return None
        cash = (as_of(series.get("cash", []), dd) or 0) + (as_of(series.get("sti", []), dd) or 0)
        debt = (as_of(series.get("debt", []), dd) or 0) + (as_of(series.get("lease", []), dd) or 0)
        extra = (as_of(series.get("nci", []), dd) or 0) + (as_of(series.get("preferred", []), dd) or 0)
        return m + debt - cash + extra

    def paired(a, b, dd):
        ea = [e for e in series.get(a, []) if e["available"] <= dd]
        eb = [e for e in series.get(b, []) if e["available"] <= dd]
        if not ea or not eb:
            return None, None
        if ea[-1]["end"] != eb[-1]["end"]:
            common = {x["end"] for x in ea} & {x["end"] for x in eb}
            if not common:
                return None, None
            end = max(common)
            lead = max(ea[-1]["end"], eb[-1]["end"])
            if (date.fromisoformat(lead) - date.fromisoformat(end)).days > bmh.MAX_PAIR_LAG_DAYS:
                return None, None
            ea = [x for x in ea if x["end"] == end]
            eb = [x for x in eb if x["end"] == end]
        return ea[-1]["val"], eb[-1]["val"]

    def ebitda(dd):
        o, a = paired("opinc", "dda", dd)
        return (o + a) if (o is not None and a is not None) else None

    def fcf(dd):
        o, c = paired("ocf", "capex", dd)
        return (o - c) if (o is not None and c is not None) else None

    eps_now = lambda dd: as_of(eps, dd) if eps else None
    per_dil = lambda dd, px: px * bmh.fx.rate(t, dd) / eps_now(dd) if eps_now(dd) and eps_now(dd) > 0 else None
    defs = {
        "PER": (lambda dd, px: (mcap(dd, px) / core_earnings(dd)) if mcap(dd, px) and core_earnings(dd) else None) if core else per_dil,
        "PSR": lambda dd, px: mcap(dd, px) / as_of(series.get("revenue", []), dd) if mcap(dd, px) and as_of(series.get("revenue", []), dd) else None,
        "PBR": lambda dd, px: mcap(dd, px) / as_of(series.get("equity", []), dd) if mcap(dd, px) and as_of(series.get("equity", []), dd) else None,
        "PCR": lambda dd, px: (mcap(dd, px) / fcf(dd)) if mcap(dd, px) and fcf(dd) and fcf(dd) > 0 else None,
        "EV/EBITDA": lambda dd, px: (ev(dd, px) / ebitda(dd)) if ev(dd, px) and ebitda(dd) and ebitda(dd) > 0 else None,
    }
    denoms = {"PCR": fcf, "EV/EBITDA": ebitda,
              "PSR": lambda dd: as_of(series.get("revenue", []), dd),
              "PBR": lambda dd: as_of(series.get("equity", []), dd)}
    if not core:
        denoms["PER"] = eps_now
    out = {}
    for label, fn in defs.items():
        out[label] = {}
        for dd, px in daily:
            try:
                x = fn(dd, px)
            except Exception:
                x = None
            out[label][dd] = x if (x and x > 0) else None
    neg = {}   # 평가일에만 분모 부호를 본다(분석에서 필요)
    return out, core, denoms, per_dil


def self_score_at(vals, denom, day, window_start):
    """카드 자기 이력 한 배수: 창 안 양수 값들에서 오늘 값의 백분위 → 점수(100 − 백분위)."""
    pts = [x for dd, x in vals.items() if window_start <= dd <= day and x]
    if not pts:
        return None, None                         # 계산 불가 → 배수 자체가 없다
    cur = vals.get(day)
    if cur:
        pr = sum(1 for x in pts if x < cur) / len(pts) * 100
        return round(100 - pr, 1), cur
    dv = denom(day) if denom else None
    if dv is not None and dv <= 0:
        return 0.0, NEG                           # 오늘 분모 0 이하 → 0점(가장 비싼 쪽)
    return None, None                             # 분모를 못 구함 → 평균에서 뺌


def _dir_hash(path):
    import hashlib
    h = hashlib.sha256()
    for f in sorted(os.listdir(path)):
        h.update(f.encode()); h.update(open(os.path.join(path, f), "rb").read())
    return h.hexdigest()[:HASH_LEN]


def provenance():
    """엔진 커밋 + 미커밋 여부 + 이 스크립트·입력 자료 해시(Codex — HEAD만으로는 실행 코드가 확정되지 않는다)."""
    import hashlib
    git = lambda *a: subprocess.run(["git", "-C", V2, *a], capture_output=True, text=True).stdout.strip()
    engine = ["build_dcf.py", "build_multiple_history.py", "build_peer_score.py", "splits.py", "fx.py",
              "core_earnings.json", "tax_oneoff.json", "share_adjust.json", "sectors.json"]
    return {"engine_commit": git("rev-parse", "HEAD"),
            "engine_dirty": git("status", "--porcelain", "--", *engine),
            "script_sha256": hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()[:HASH_LEN],
            "pit_sha256": hashlib.sha256(open(os.path.join(HERE, "pit.py"), "rb").read()).hexdigest()[:HASH_LEN],
            "engine_sha256": {f: hashlib.sha256(open(os.path.join(V2, f), "rb").read()).hexdigest()[:HASH_LEN] for f in engine if os.path.exists(os.path.join(V2, f))},
            "inputs": {k: _dir_hash(p) for k, p in (("prices10y", PRICES), ("facts", FACTS), ("eps", EPS_DIR))},
            "redesign_commit": subprocess.run(["git", "-C", os.path.dirname(v.DATA), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()}


def _override_filed(t):
    """종목별 손 보정 파일에 적힌 공시일(filed) 모음."""
    out = set()
    def walk(x):
        if isinstance(x, dict):
            if isinstance(x.get("filed"), str):
                out.add(x["filed"])
            for y in x.values():
                walk(y)
        elif isinstance(x, list):
            for y in x:
                walk(y)
    for f in ("nonop_extra.json", "interest_extra.json", "tax_oneoff.json"):
        p = os.path.join(V2, f)
        if os.path.exists(p):
            walk(json.load(open(p)).get(t))
    return out


def dcf_window_start(t, day):
    """현금흐름 칸 이력 창의 시작일. fixed면 None(build_dcf 기본 — 카드와 같다).
    rolling(five_year_gate_prereg.md 2절): ws = 평가일 − int(5.25 × 365.25)일. 분사 종목(HISTORY_WINDOW)은 그 시작일이 평가일 이전이면
    max(ws, 분사 시작일)을 넘긴다 — history()는 window_start를 받으면 분사 시작일을 무시하므로(build_dcf.py `ws = window_start or hw[0]`)
    여기서 맞춘다. 최소 개수는 history()가 정한다: 분사 시작일이 평가일 이전이면 종목별 값, 뒤면 ASOF_REF 되돌림으로 13."""
    if DCF_WINDOW == "fixed":
        return None
    from datetime import timedelta
    ws = (date.fromisoformat(day) - timedelta(days=int(5.25 * 365.25))).isoformat()
    hw = d.HISTORY_WINDOW.get(t)
    if hw and hw[0] <= day:
        ws = max(ws, hw[0])
    return ws


def build(panel_path=PANEL):
    uni = [r for r in json.load(open(v.SP500)) if r.get("sector") != "Financials"]
    rows = []
    for k, r in enumerate(uni):
        t, cik = r["ticker"], r["cik"].zfill(10)
        # 유니버스: 통제 유니버스(sp500_eps 파일이 있는 종목)와 같은 멤버십
        if t in v.EXCLUDE or not os.path.exists(os.path.join(v.EPS_DIR, t.replace(".", "-") + ".json")):
            continue
        pf = os.path.join(PRICES, f"{t}.json")
        fp = os.path.join(FACTS, f"{cik}_facts.json")
        if not os.path.exists(pf) or not os.path.exists(fp):
            continue
        data = json.load(open(fp))
        if not data.get("facts"):
            continue
        pj = json.load(open(pf))
        bars = sorted(pj["daily"], key=lambda b: b["date"])
        dates, closes = [b["date"] for b in bars], [b["c"] for b in bars]
        pf5 = v.price_file(t)                              # 통제 유니버스 멤버십 그대로: sp500_5y 파일 · 700봉 이상
        if not pf5 or len(json.load(open(pf5))["daily"]) < 700:
            continue
        _splits.OVERRIDE[t] = [(s["date"], s["ratio"]) for s in (pj.get("splits") or [])]
        d.feh.CIKS[t] = cik
        bmh._facts = functools.lru_cache(maxsize=2)(lambda c, _data=data: _data if c == cik else {})
        for fn in ("concept",):
            if hasattr(getattr(bmh, fn), "cache_clear"):
                getattr(bmh, fn).cache_clear()
        ep = os.path.join(EPS_DIR, f"{t}.json")
        # F1(input_fix_prereg 1절): Yahoo가 분사·주식 배당을 0.70 < r < 1.45 비율의 분할로 기록해 그 전 가격을 r로 나눠 둔다.
        # splits.clean()이 그 사건을 주식 수 보정에서 버리므로 가치 비교용 가격(배수 시리즈·DCF 비교)은 사건 전 봉에 r을 곱해 되돌리고,
        # EPS도 그 사건으로 나누지 않는다. 재작성 종목(RESTATED_LATEST)은 평가일 공시 상태가 사건일 이후면 재무가 이미 분사 사업을 뺐으므로
        # 그 사건은 되돌리지 않는다. 수익률(add_returns)은 조정 가격(px) 그대로.
        keep_sp, ign_sp = _splits.clean([(s_["date"], s_["ratio"]) for s_ in (pj.get("splits") or [])])

        def restore_for(state):
            return tuple((d0, r0) for d0, r0 in ign_sp
                         if not (t in d.feh.RESTATED_LATEST and state is not None and state >= d0))

        def then_factor(dd, restore):
            f_ = 1.0
            for d0, r0 in restore:
                if dd < d0:
                    f_ *= r0
            return f_

        eps_cache = {}

        def eps_for(restore):
            """C8: EPS TTM은 SEC 자료로 다시 만들어 공개일을 구성 분기 중 가장 늦은 첫 공시일로(pit.eps_ttm). 자료가 없으면 EPS 파일.
            분할 목록은 진짜 분할 + 되돌리지 않는 분사 사건(F1)."""
            if restore not in eps_cache:
                sp = [{"date": d0, "ratio": r0} for d0, r0 in sorted(keep_sp + [x for x in ign_sp if x not in restore])]
                e1 = [{"available": e["available"], "val": e["val"] + bmh.oneoff_in_ttm(t, e["quarter_end"], "eps", asof=e["available"])}
                      for e in pit.eps_ttm(data, sp) if e["val"]]
                if not e1 and os.path.exists(ep):
                    e1 = sorted(({"available": e["available_date"],
                                  "val": e["ttm_eps"] + bmh.oneoff_in_ttm(t, e.get("quarter_end"), "eps", asof=e["available_date"])}
                                 for e in json.load(open(ep)) if e.get("ttm_eps")), key=lambda e: e["available"])
                eps_cache[restore] = e1
            return eps_cache[restore]

        daily_cache = {}

        def daily_for(restore):
            if restore not in daily_cache:
                daily_cache[restore] = [(dd, c * then_factor(dd, restore)) for dd, c in zip(dates, closes) if dd >= BAR_START]
            return daily_cache[restore]
        # C8(2026-10-03, Codex·Fable 2차): 모든 종목의 현금흐름과 배수 시리즈를 (공시 상태, 감가상각 합산 태그 판정) 단위로
        # 그날까지 공시된 행만으로 계산한다. 한 번 만든 시리즈를 쓰면 1년 뒤 비교 수치로 다시 실린 분기가 공개일을 늦추는 등
        # 공개 시점이 미래 공시에 따라 바뀌었다(PEP·KO, Fable). 감가상각 판정은 평가일 기준(공시 없이 730일 문턱을 넘을 수 있음).
        filed_all = sorted({row.get("filed") for ns in data["facts"].values() for vv in ns.values()
                            for rr in vv["units"].values() for row in rr if row.get("filed")})
        month_ends = {}
        for i, dd in enumerate(dates):
            month_ends[dd[:7]] = i
        cache, mcache = {}, {}
        override_filed = sorted(_override_filed(t))
        hstart = bmh.HISTORY_START.get(t, "0000")
        for mth, i in sorted(month_ends.items()):
            if mth < START_MONTH or mth > END_MONTH:
                continue
            day, px = dates[i], closes[i]
            state = max((f for f in filed_all if f <= day), default=None)
            if state is None:
                continue
            restore = restore_for(state)
            px_then = px * then_factor(day, restore)
            eps = eps_for(restore)
            daily = daily_for(restore)
            try:
                pit.install(bmh, cik, data, state, ref=day)
                # 감가상각 경로: 합산 태그 판정과 실제로 쓴 경로(합산·구성요소 대체)를 함께 키에 넣는다(XYL·IEX, Fable 3차)
                with contextlib.redirect_stdout(io.StringIO()):
                    dflag = (bmh.live_combined(cik)[0] is not None, bmh.dda_quarters(cik, t)[0])
            except Exception:
                dflag = None
            finally:
                pit.reset(bmh)
            # 평가일에 따라 달라지는 엔진 분기를 모두 키에 넣는다: 감가상각 합산 태그 판정, 분사 이력 시작일(HISTORY_WINDOW —
            # 연구 모드에서는 그 날짜가 지난 평가일에만 적용)이 지났는지(WDC 2025-05 대 06, Codex 2차).
            hw = d.HISTORY_WINDOW.get(t)
            # 손으로 넣은 보정값(nonop_extra·interest_extra·tax_oneoff)은 자체 공시일로 걸러진다 — SEC 공시 목록에 없는 날짜라
            # 키에 따로 넣는다(KO nonop_extra 2026-07, Fable 2차).
            ovr = max((f for f in override_filed if f <= day), default="")
            key = (state, dflag, bool(hw and hw[0] <= day), ovr, restore)
            # 롤링 창이면 공시 상태가 같아도 창이 밀려 분기가 빠지므로 현금흐름 캐시 키에 유효 시작일을 넣는다(관문 2절, Codex·Fable).
            # 배수 시리즈 캐시(mcache)는 창과 무관해 그대로 key를 쓴다.
            dws = dcf_window_start(t, day)
            dkey = key + (dws,)
            if dkey not in cache:
                res = {"dq": [], "base": None, "ok": False}
                try:
                    pit.install(bmh, cik, data, state, ref=day)
                    # 롤링 창의 분사 종목 최소 개수는 ASOF_REF 되돌림에 기대므로 평가일 기준이 걸려 있어야 한다(Fable M2)
                    assert dws is None or bmh.ASOF_REF == day, (t, day, bmh.ASOF_REF)
                    with contextlib.redirect_stdout(io.StringIO()):
                        b = d.base_inputs(t, day)
                        h = d.history(t, day, window_start=dws)
                        res["dq"] = b.get("dq") or []
                        ok = bool(h and b.get("revenue") and b.get("shares") and b.get("opinc") is not None)
                        # 현금흐름이 안 나온 이유를 남긴다 — 데이터 공백과 엔진 오류를 가르려고(관문 4절 3단계, Codex·Fable)
                        res["why"] = None if ok else ",".join(k for k, bad in (("history", not h), ("revenue", not b.get("revenue")),
                                                                                ("shares", not b.get("shares")), ("opinc", b.get("opinc") is None)) if bad)
                        sc = d.scenarios(b, h, 0.10, 0.025) if ok else None
                        if sc and sc[1]["per_share"] is not None and math.isfinite(sc[1]["per_share"]):
                            res["base"], res["ok"] = sc[1]["per_share"], True
                        elif ok:
                            res["why"] = "scenario"
                except AssertionError:
                    raise
                except Exception as e:
                    res["err"] = str(e)[:60]
                    res["why"] = "error"
                finally:
                    pit.reset(bmh)
                cache[dkey] = res
            res = cache[dkey]
            if key not in mcache:
                try:
                    pit.install(bmh, cik, data, state, ref=day)
                    with contextlib.redirect_stdout(io.StringIO()):
                        mcache[key] = multiple_series(t, cik, daily, eps)
                except Exception as e:
                    print("배수 실패", t, day, str(e)[:60], flush=True)
                    mcache[key] = (None, False, {}, None)
                finally:
                    pit.reset(bmh)
            mv_day, core_day, den_day, pdil_day = mcache[key]
            y, m_, dd_ = day.split("-")
            # 분사 종목의 자기 이력 시작일은 그 날짜가 지난 평가일에만 적용한다(그 전 평가일에 쓰면 미래 정보 — Codex)
            wstart = f"{int(y) - 5}-{m_}-{dd_}"
            if hstart <= day:
                wstart = max(wstart, hstart)
            selfm, peerv = {}, {}
            if mv_day:
                for lab in METRICS:
                    sc_, cur = self_score_at(mv_day[lab], den_day.get(lab), day, wstart)
                    if sc_ is not None:
                        selfm[lab] = sc_
                    elif lab in mv_day and any(x for dd2, x in mv_day[lab].items() if wstart <= dd2 <= day):
                        selfm[lab] = None                     # 분모 없음(카드: currentNote missing)
                    # 동종업용 값(공시 EPS 기준 PER)
                    if lab == "PER" and core_day:
                        x = pdil_day(day, px_then) if pdil_day else None
                        e_ = bmh.as_of(eps, day) if eps else None
                        peerv["PER_dil"] = x if x else (NEG if (e_ is not None and e_ <= 0) else None)
                        continue
                    # 동종업 값은 자기 이력 창과 무관하게 그날 배수 · 분모 부호로(Codex)
                    x = mv_day[lab].get(day)
                    if x:
                        peerv[lab] = x
                    else:
                        dn = den_day.get(lab)
                        dv = dn(day) if dn else None
                        peerv[lab] = NEG if (dv is not None and dv <= 0) else None
            rows.append({"t": t, "sec": r["sector"], "d": day, "m": mth, "i": i, "px": px, "px_then": px_then,
                         "dq": res["dq"], "dcf_ok": res["ok"], "base": res["base"], "dcf_ws": dws,
                         "dcf_why": res.get("why"), "dcf_err": res.get("err"),
                         "self": selfm, "peer": peerv, "core": core_day})
        if k % 25 == 0:
            print(k, t, len(rows), flush=True)
    meta = provenance() | {"built": date.today().isoformat(), "roster": sorted({r["t"] for r in rows}),
                           "config": {"months": [START_MONTH, END_MONTH], "bar_start": BAR_START, "dcf_window": DCF_WINDOW}}
    json.dump({"meta": meta, "rows": rows}, open(panel_path, "w"))
    return meta, rows


# ───────────────────────── 판정 ─────────────────────────

GRADES = ["고평가", "적정~고평가", "적정", "적정~저평가", "저평가"]          # 비싼 → 싼 (서수 0..4)
LEVELS = ["매우 싸다", "싸다", "적정", "비싸다", "매우 비싸다"]
SCORE_V0 = {"매우 싸다": 1, "싸다": 1, "적정": 0, "비싸다": -1, "매우 비싸다": -2}
SCORE_V1 = {"매우 싸다": 1, "싸다": 1, "적정": 0, "비싸다": -1, "매우 비싸다": -1}
VARIANTS = {"V0": (SCORE_V0, 2), "V1": (SCORE_V1, 1), "V2": (SCORE_V0, 2), "V3": (SCORE_V0, 2)}


def ratio_level(px, base):
    if base is None:
        return None
    if base <= 0:
        return "매우 비싸다"
    x = px / base
    return LEVELS[0] if x <= .7 else LEVELS[1] if x <= .9 else LEVELS[2] if x <= 1.1 else LEVELS[3] if x <= 1.5 else LEVELS[4]


def pct_level(q):
    """q = 싼 쪽부터의 순위 비율(0~1]."""
    return LEVELS[0] if q <= .10 else LEVELS[1] if q <= .30 else LEVELS[2] if q <= .70 else LEVELS[3] if q <= .90 else LEVELS[4]


def D_of(r):
    if r["base"] is None:
        return None
    return -math.log(r.get("px_then", r["px"]) / r["base"]) if r["base"] > 0 else -math.inf


def peer_scores(rows):
    """같은 날·같은 GICS 섹터(자기 제외) 순위 — build_peer_score.peer_score와 같은 산식."""
    by = {}
    for r in rows:
        by.setdefault((r["d"], r["sec"]), []).append(r)
    for (day, sec), g in by.items():
        for r in g:
            mets = []
            for lab in METRICS:
                if lab == "PER" and r["core"]:
                    continue                                       # 본인 본업 PER ↔ 동종업 공시 PER: 뺀다
                mine = r["peer"].get(lab)
                if mine is None:
                    continue
                key = lambda o: o["peer"].get("PER_dil") if (lab == "PER" and o["core"]) else o["peer"].get(lab)
                peers_all = [key(o) for o in g if o is not r and key(o) is not None]
                if len(peers_all) < MIN_PEERS:
                    continue
                pos = [x for x in peers_all if x != NEG]
                cheaper = len(pos) if mine == NEG else sum(1 for x in pos if x < mine)
                mets.append(round(100 - cheaper / len(peers_all) * 100, 1))     # 카드: 배수 점수 소수 첫째 자리
            r["peer_score"] = round(sum(mets) / len(mets), 1) if mets else None
            r["peer_n"] = len(mets)


def seat_multiple(score, n):
    return None if (score is None or n < 3) else (1 if score >= 70 else -1 if score < 30 else 0)


def verdict(judges):
    """judges = [(vote|None, weight)] — 카드 JS 그대로."""
    seated = [(x, w) for x, w in judges if x is not None]
    if judges[2][0] is None or len(seated) < 2:
        return None, None
    maxw = sum(w for _, w in seated)
    n = sum(x for x, _ in seated) * 4 / maxw
    g = "저평가" if n >= 3 else "적정~저평가" if n >= 1 else "적정" if n > -1 else "적정~고평가" if n > -3 else "고평가"
    return g, n


ALT_FINITE = False      # 민감도: 0 이하 행을 백분위 모수에서 빼고(유한값끼리 순위) 매우 비싸다로 둔다(Fable — 사전 등록 문구 해석 차이)
DROP_SELF = False       # 민감도: 자기 이력 칸을 앉히지 않는다(Fable — 판정 IC가 자기 이력에 끌리는지)


def assign(rows):
    """행마다 세 칸 표와 변형별 판정. V2·V3 백분위는 같은 달·같은 표본(필터 적용 뒤) 안에서."""
    for r in rows:
        sv = [x for x in r["self"].values() if x is not None]
        r["self_score"] = round(sum(sv) / len(sv), 1) if sv else None
        r["self_vote"] = None if DROP_SELF else seat_multiple(r["self_score"], len(sv))
        r["peer_vote"] = seat_multiple(r.get("peer_score"), r.get("peer_n", 0))
        r["D"] = D_of(r)
        r["lv_V0"] = ratio_level(r.get("px_then", r["px"]), r["base"]) if r["dcf_ok"] else None   # F1: 가치 비교는 당시 종가
    months = {}
    for r in rows:
        if r["lv_V0"] is not None:
            months.setdefault(r["m"], []).append(r)
    for m, g in months.items():
        def qs(grp):
            if ALT_FINITE:
                grp = [x for x in grp if x["D"] != -math.inf]
                if not grp:
                    return {}
            Ds = np.array([x["D"] for x in grp])
            ranks = rankdata(-Ds, method="average")                  # 1 = 가장 쌈
            return {id(x): ranks[j] / len(grp) for j, x in enumerate(grp)}
        qm = qs(g)
        bysec = {}
        for x in g:
            bysec.setdefault(x["sec"], []).append(x)
        qsec = {}
        for sec, gg in bysec.items():
            if len([x for x in gg if not (ALT_FINITE and x["D"] == -math.inf)]) >= 10:
                qsec.update(qs(gg))
        for x in g:
            x["lv_V2"] = "매우 비싸다" if x["D"] == -math.inf else pct_level(qm[id(x)])
            x["lv_V3"] = ("매우 비싸다" if x["D"] == -math.inf else pct_level(qsec[id(x)])) if (id(x) in qsec or (x["D"] == -math.inf and x["sec"] in {y["sec"] for y in g if id(y) in qsec})) else x["lv_V2"]
    for r in rows:
        r["lv_V1"] = r["lv_V0"]
        for name, (smap, w) in VARIANTS.items():
            lv = r.get(f"lv_{name}")
            g, n = verdict([(r["self_vote"], 1), (r["peer_vote"], 1), (smap[lv] if lv else None, w)])
            r[f"g_{name}"], r[f"n_{name}"] = g, n


def add_returns(rows):
    cache = {}
    for r in rows:
        if r["t"] not in cache:
            bars = sorted(json.load(open(os.path.join(PRICES, f"{r['t']}.json")))["daily"], key=lambda b: b["date"])
            cache[r["t"]] = ({b["date"]: k for k, b in enumerate(bars)}, [b["c"] for b in bars])
        idx, cs = cache[r["t"]]
        i = idx[r["d"]]                                   # 위치가 아니라 날짜로 찾는다(Codex)
        assert abs(cs[i] - r["px"]) < 1e-6 * max(1, r["px"]), (r["t"], r["d"])
        for h in (H_MAIN, H_AUX):
            r[f"r{h}"] = (cs[i + h] / cs[i] - 1) if i + h < len(cs) else None


def wmean_ci(vals, w):
    if not w:
        return None, None
    return float(np.average(vals, weights=w)), v.boot_weighted(vals, w)


def analyze_set(rows, label):
    assign(rows)
    issued = [r for r in rows if r["g_V0"] is not None]
    out = {"label": label, "rows": len(rows), "issued": len(issued), "tickers": len({r["t"] for r in issued})}
    # 기준선: 같은 달 · 같은 필터 · 판정이 나온 종목의 동일가중 평균
    for h in (H_MAIN, H_AUX):
        base = {}
        for r in issued:
            if r[f"r{h}"] is not None:
                base.setdefault(r["m"], []).append(r[f"r{h}"])
        for r in issued:
            b = base.get(r["m"])
            r[f"x{h}"] = (r[f"r{h}"] - float(np.mean(b))) if (r[f"r{h}"] is not None and b and len(b) >= v.MIN_MONTH_N) else None
    months_all = sorted({r["m"] for r in issued})
    # 학습·홀드아웃 달: 그 달 판정 종목이 모두 h거래일 수익률을 가진 달
    def complete(m, h):
        g = [r for r in issued if r["m"] == m]
        return len(g) >= v.MIN_MONTH_N and all(r[f"r{h}"] is not None for r in g)
    learn = [m for m in months_all if LEARN[0] <= m <= LEARN[1] and complete(m, H_MAIN)]
    hold126 = [m for m in months_all if m >= HOLD_FROM and complete(m, H_MAIN)]
    hold63 = [m for m in months_all if m >= HOLD_FROM and complete(m, H_AUX)]
    out["months"] = {"learn": learn, "holdout_126": hold126, "holdout_63": hold63,
                     "learn_incomplete": [m for m in months_all if LEARN[0] <= m <= LEARN[1] and not complete(m, H_MAIN)]}
    last_m = max(months_all)

    def dist(rs, name):
        c = {g: 0 for g in GRADES}
        for r in rs:
            c[r[f"g_{name}"]] += 1
        n = sum(c.values())
        sh = {g: c[g] / n for g in GRADES} if n else {}
        return {"n": n, "share": sh, "top": max(sh, key=sh.get) if sh else None, "top_share": max(sh.values()) if sh else None}

    def ic_series(rs, months, key, h):
        ics, w, ms = [], [], []
        for m in months:
            g = [r for r in rs if r["m"] == m and r.get(f"x{h}") is not None and key(r) is not None]
            if len(g) < v.MIN_MONTH_N:
                continue
            a = [key(r) for r in g]
            if len(set(a)) < 2:
                continue
            ics.append(spearmanr(a, [r[f"x{h}"] for r in g]).correlation); w.append(len(g)); ms.append(m)
        return ics, w, ms

    def ic(rs, months, key, h):
        ics, w, ms = ic_series(rs, months, key, h)
        mu, ci = wmean_ci(ics, w)
        return {"IC": mu, "ci": ci, "months": len(w), "monthly": dict(zip(ms, [round(x, 4) for x in ics]))}

    def dic(rs, months, ka, kb, h):
        diffs, w = [], []
        for m in months:
            g = [r for r in rs if r["m"] == m and r.get(f"x{h}") is not None and ka(r) is not None and kb(r) is not None]
            if len(g) < v.MIN_MONTH_N:
                continue
            y = [r[f"x{h}"] for r in g]
            a, b = [ka(r) for r in g], [kb(r) for r in g]
            if len(set(a)) < 2 or len(set(b)) < 2:
                continue
            diffs.append(spearmanr(a, y).correlation - spearmanr(b, y).correlation); w.append(len(g))
        mu, ci = wmean_ci(diffs, w)
        return {"dIC": mu, "ci": ci, "months": len(w)}

    for name in VARIANTS:
        o = {}
        L = [r for r in issued if r["m"] in learn]
        o["dist_learn"] = dist(L, name)
        o["dist_last"] = dist([r for r in issued if r["m"] == last_m], name) | {"month": last_m}
        o["dist_all"] = dist(issued, name)
        tab = {}
        for g in GRADES:
            xs = [r[f"x{H_MAIN}"] for r in L if r[f"g_{name}"] == g and r.get(f"x{H_MAIN}") is not None]
            tab[g] = {"n": len(xs), "mean": float(np.mean(xs)) if xs else None,
                      "median": float(np.median(xs)) if xs else None}
        o["grade_returns_learn"] = tab
        present = [g for g in GRADES if tab[g]["n"] > 0]
        o["grade_median_spearman"] = (float(spearmanr([GRADES.index(g) for g in present], [tab[g]["median"] for g in present]).correlation)
                                      if len(present) >= 3 else None)
        o["grade_mean_spearman"] = (float(spearmanr([GRADES.index(g) for g in present], [tab[g]["mean"] for g in present]).correlation)
                                    if len(present) >= 3 else None)
        o["IC_cont_learn"] = ic(issued, learn, lambda r, nm=name: r[f"n_{nm}"], H_MAIN)
        o["IC_grade_learn"] = ic(issued, learn, lambda r, nm=name: GRADES.index(r[f"g_{nm}"]), H_MAIN)
        o["IC_cont_hold63"] = ic(issued, hold63, lambda r, nm=name: r[f"n_{nm}"], H_AUX)
        o["IC_cont_learn63"] = ic(issued, learn, lambda r, nm=name: r[f"n_{nm}"], H_AUX)
        if hold126:
            o["IC_cont_hold126"] = ic(issued, hold126, lambda r, nm=name: r[f"n_{nm}"], H_MAIN)
        out[name] = o
    for name in ("V1", "V2", "V3"):
        ka = lambda r, nm=name: r[f"n_{nm}"]
        kb = lambda r: r["n_V0"]
        out[f"dIC_{name}_V0"] = {"learn_126": dic(issued, learn, ka, kb, H_MAIN),
                                 "learn_63": dic(issued, learn, ka, kb, H_AUX),
                                 "hold_63": dic(issued, hold63, ka, kb, H_AUX)}
        if hold126:
            out[f"dIC_{name}_V0"]["hold_126"] = dic(issued, hold126, ka, kb, H_MAIN)
    # 칸별 IC(판정이 나온 표본, 그 칸이 앉은 행)
    out["judge_IC_learn"] = {
        "self": ic(issued, learn, lambda r: r["self_score"] if r["self_vote"] is not None else None, H_MAIN),
        "peer": ic(issued, learn, lambda r: r["peer_score"] if r["peer_vote"] is not None else None, H_MAIN),
        "dcf_D": ic(issued, learn, lambda r: r["D"] if r["D"] != -math.inf else -1e9, H_MAIN),
    }
    for k2, x in out["judge_IC_learn"].items():
        x["review_flag"] = bool(x["ci"] and x["ci"][1] < 0)
    # 현금흐름 칸 단계 분포(V0) — 쏠림 확인
    c = {}
    for r in issued:
        if r["m"] in learn:
            c[r["lv_V0"]] = c.get(r["lv_V0"], 0) + 1
    tot = sum(c.values())
    out["dcf_level_dist_learn_V0"] = {k2: round(x / tot, 3) for k2, x in c.items()} if tot else {}
    return out


def rule(res):
    """사전 등록 '판정 규칙' — 학습 구간."""
    def check(name):
        o, dd = res[name], res[f"dIC_{name}_V0"]
        ok = lambda x, f: (x is not None) and f(x)
        # ④ = 보고 3번의 연속 판정 점수(반올림 전 4표 환산 합) IC. 5등급 서수 IC는 참고로만 보고(Codex).
        c = {"1_dIC>0": ok(dd["learn_126"]["dIC"], lambda x: x > 0),
             "2_median_spearman>=0.8": ok(o["grade_median_spearman"], lambda x: x >= 0.8),
             "3_top_share<0.5": ok(o["dist_learn"]["top_share"], lambda x: x < 0.5),
             "4_raw_IC>=0": ok(o["IC_cont_learn"]["IC"], lambda x: x >= 0)}
        c["ref_grade_IC>=0"] = ok(o["IC_grade_learn"]["IC"], lambda x: x >= 0)
        h = dd.get("hold_126")
        # ⑤ 홀드아웃 126일이 3개월 이상일 때만, V2·V3에만
        ld = dd["learn_126"]["dIC"]
        c["5_holdout_sign"] = (None if name == "V1" or len(res["months"]["holdout_126"]) < 3 or not h
                               or h["dIC"] is None or ld is None else ((h["dIC"] > 0) == (ld > 0)))
        ci = dd["learn_126"]["ci"]
        return {"checks": c, "pass": all(x for k, x in c.items() if x is not None and not k.startswith("ref_")),
                "weak_evidence": not (ci and ci[0] > 0)}
    out = {n: check(n) for n in ("V1", "V2", "V3")}
    cand = [n for n in ("V2", "V3") if out[n]["pass"]]
    if cand:
        pick = max(cand, key=lambda n: res[f"dIC_{n}_V0"]["learn_126"]["dIC"])
    elif out["V1"]["pass"]:
        pick = "V1"
    else:
        pick = "V0"
    out["adopt_candidate"] = pick
    return out


def apply_cards(rows_filtered, month="2026-09"):
    """6번 보고 — 카드에 표시된 자기 이력·동종업 표는 그대로 두고 현금흐름 칸만 변형별로 바꿨을 때의 판정.

    V2·V3: 카드의 D(카드 가격 ÷ 카드 기본 내재가치)를 그 달 패널(dq 필터 적용, 현금흐름 계산된 행)의
    시장·섹터 분포에 끼워 넣는다(같은 종목의 패널 행은 기준에서 뺀다). 금융 카드는 패널에 금융이 없어
    V0·V1만 낸다(2026-10-02 사용자 결정 — 적용 범위 밖).
    """
    cards = json.loads(subprocess.run(["node", os.path.join(HERE, "extract_card_verdicts.js")], capture_output=True, text=True).stdout)
    sec = {r["ticker"]: r.get("sector") for r in json.load(open(v.SP500))}
    sec_v2 = json.load(open(os.path.join(V2, "sectors.json")))
    ref = [r for r in rows_filtered if r["m"] == month and r["dcf_ok"]]
    out = {}
    for T, c in sorted(cards.items()):
        if "error" in c:
            raise RuntimeError(f"{T}: 카드 판정 추출 실패 — {c['error']}")
        s_ = sec.get(T) or sec.get(T.replace("BRKB", "BRK.B")) or (sec_v2.get(T) if isinstance(sec_v2.get(T), str) else None)
        js = c["judges"]          # [자기 이력, 동종업, 현금흐름(은행 RIM 카드는 "초과이익")] — 위치로 읽는다
        sv, pv, dv0 = js[0][1], js[1][1], js[2][1]
        lv0 = js[2][2] if dv0 is not None else None
        row = {"sector": s_, "card_verdict": c["verdict"], "self": js[0][2], "self_vote": sv, "third_judge": js[2][0],
               "peer": js[1][2], "peer_vote": pv, "dcf_label": lv0, "ratio": c["ratio"], "price_date": c["date"]}
        g0, _ = verdict([(sv, 1), (pv, 1), (SCORE_V0[lv0] if lv0 else None, 2)])
        row["V0"] = g0 or "판정 보류"
        row["V0_matches_card"] = row["V0"] == c["verdict"]
        g1, _ = verdict([(sv, 1), (pv, 1), (SCORE_V1[lv0] if lv0 else None, 1)])
        row["V1"] = g1 or "판정 보류"
        if s_ == "Financials":
            row["V2"] = row["V3"] = "범위 밖(금융)"
        else:
            if lv0 is None:
                Dc = None
            elif c["base"] is not None and c["base"] <= 0:
                Dc = -math.inf
            else:
                Dc = -math.log(c["ratio"])
            for name, pool in (("V2", [r for r in ref if r["t"] != T]),
                               ("V3", [r for r in ref if r["t"] != T and r["sec"] == s_])):
                if name == "V3" and len(pool) + 1 < 10:             # 카드 자신까지 넣어 10개(패널 V3와 같은 기준)
                    row["V3"], row["lv_V3"] = row["V2"], row.get("lv_V2")
                    continue
                if Dc is None:
                    lv = None
                elif Dc == -math.inf:
                    lv = "매우 비싸다"
                else:
                    Ds = [D_of(r) for r in pool]
                    q = (1 + sum(1 for x in Ds if x > Dc) + 0.5 * sum(1 for x in Ds if x == Dc)) / (len(Ds) + 1)
                    lv = pct_level(q)
                    row[f"q_{name}"] = round(q, 3)
                row[f"lv_{name}"] = lv
                g, _ = verdict([(sv, 1), (pv, 1), (SCORE_V0[lv] if lv else None, 2)])
                row[name] = g or "판정 보류"
        out[T] = row
    return out


def build_only():
    """관문 4절 1단계: 수익률·카드 적용 없이 행만 만들어 저장하고, 수익률 없는 점검 요약만 찍는다."""
    global START_MONTH, END_MONTH, BAR_START, DCF_WINDOW, HASH_LEN
    a = sys.argv
    i = a.index("--months"); START_MONTH, END_MONTH = a[i + 1], a[i + 2]
    DCF_WINDOW = a[a.index("--dcf-window") + 1]
    assert DCF_WINDOW in ("fixed", "rolling"), DCF_WINDOW
    out = a[a.index("--panel") + 1]
    assert os.path.abspath(out) != os.path.abspath(PANEL), "학습 패널을 덮어쓰지 않는다"
    # 시험 구간은 2021-10 평가일의 자기 이력 5년 창(2016-10~)을 덮도록 봉 시작을 당긴다(가격 파일이 2016-10-03부터).
    # 학습 구간 롤링 재실행은 기본값(2019-05)을 그대로 둬 고정 창 결과와 창 말고는 같은 입력이 되게 한다(Fable M1).
    if START_MONTH < "2024-06":
        BAR_START = "2016-01-01"
    HASH_LEN = 64
    meta, rows = build(out)
    import collections
    by = collections.defaultdict(lambda: [0, 0, 0])
    for r in rows:
        x = by[r["m"]]; x[0] += 1; x[1] += bool(r["dcf_ok"]); x[2] += bool(r["dq"])
    print("\n월, 행, 현금흐름 계산됨, dq 있음")
    for m in sorted(by):
        print(m, *by[m])
    print("종목", len(meta["roster"]), "· 저장", out)


def main():
    if "--build-only" in sys.argv:
        return build_only()
    if "--analyze" in sys.argv:
        pj = json.load(open(PANEL)); meta, rows = pj["meta"], pj["rows"]
    else:
        meta, rows = build()
    add_returns(rows)
    peer_scores(rows)    # 동종업은 필터와 무관하게 그날 섹터 전체로(카드도 데이터 품질로 동종업을 거르지 않는다)
    bad = lambda r: any(str(x).startswith(("debt_suspect", "shares_missing")) for x in r["dq"])
    res = {"meta": meta}
    for label, rs in (("dq_filtered", [r for r in rows if not bad(r)]), ("dq_unfiltered", rows)):
        rs = [dict(r) for r in rs]
        res[label] = analyze_set(rs, label)
        res[label]["rule"] = rule(res[label])
    # 민감도(판정에 쓰지 않음)
    global ALT_FINITE, DROP_SELF
    res["sensitivity"] = {}
    for key, (af, ds) in (("finite_percentile", (True, False)), ("no_self_judge", (False, True))):
        ALT_FINITE, DROP_SELF = af, ds
        try:
            x = analyze_set([dict(r) for r in rows if not bad(r)], key)
        finally:
            ALT_FINITE, DROP_SELF = False, False
        res["sensitivity"][key] = {n: {"IC_cont": x[n]["IC_cont_learn"]["IC"], "top_share": x[n]["dist_learn"]["top_share"],
                                       "median_rho": x[n]["grade_median_spearman"], "dist": x[n]["dist_learn"]["share"]} for n in VARIANTS}
        res["sensitivity"][key]["dIC"] = {n: x[f"dIC_{n}_V0"]["learn_126"] for n in ("V1", "V2", "V3")}
        res["sensitivity"][key]["rule"] = rule(x)["adopt_candidate"]
    ALT_FINITE, DROP_SELF = False, False
    filt = [dict(r) for r in rows if not bad(r)]
    for r in filt:
        r["D"] = D_of(r)
    res["cards"] = apply_cards(filt)
    res["analysis_provenance"] = provenance()
    cs = res["cards"]
    assert all(c["V0_matches_card"] for c in cs.values()), [t for t, c in cs.items() if not c["V0_matches_card"]]
    res["cards_summary"] = {"n_cards": len(cs), "V0_matches_card": sum(c["V0_matches_card"] for c in cs.values())}
    for name in ("V1", "V2", "V3"):
        ch = {t: f"{c['card_verdict']} → {c[name]}" for t, c in cs.items()
              if c[name] != c["card_verdict"] and not c[name].startswith("범위")}
        res["cards_summary"][name] = {"changed": len(ch), "list": ch,
                                      "out_of_scope": sorted(t for t, c in cs.items() if c[name].startswith("범위"))}
    json.dump(res, open(RESULT, "w"), ensure_ascii=False, indent=1)
    for label in ("dq_filtered", "dq_unfiltered"):
        x = res[label]
        print(f"\n== {label}: 행 {x['rows']} · 판정 {x['issued']} · 종목 {x['tickers']} · 학습 {len(x['months']['learn'])}개월 "
              f"· 홀드아웃126 {len(x['months']['holdout_126'])} · 63 {len(x['months']['holdout_63'])}")
        for n in VARIANTS:
            o = x[n]
            print(f"  {n}: 최다 {o['dist_learn']['top']} {o['dist_learn']['top_share']} · 중앙값 ρ {o['grade_median_spearman']}"
                  f" · IC연속 {o['IC_cont_learn']['IC']} {o['IC_cont_learn']['ci']}")
        for n in ("V1", "V2", "V3"):
            print(f"  ΔIC {n}−V0 {x[f'dIC_{n}_V0']['learn_126']}")
        print("  규칙:", json.dumps(x["rule"], ensure_ascii=False))


if __name__ == "__main__":
    main()
