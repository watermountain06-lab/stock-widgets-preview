#!/usr/bin/env python3
"""기본적 분석 점수 — 배점은 동결 모델 그대로 쓰고 입력만 최신 분기로 바꾼다.

왜 따로 만드나
--------------
redesign의 `compute_fundamental_score.py`(v1.0.1, 2026-08-25 동결)는 **연간치만**
쓴다. 코드에서 기준일을 이렇게 정한다.

    revenue_annual = [e for e in fin["revenue"]["annual"] if e.get("val") is not None]
    financials_as_of = max((e["end"] for e in revenue_annual), default=None)

NVDA는 1월 결산이라 최신 연간치가 FY2026(2026-01-25)이고 다음 연간치는 2027년
2월에나 나온다. 그래서 점수가 항상 최대 12개월 뒤처진다 — 카드가 "지금 사기에
얼마나 가치 있나"를 묻는데 대차대조표는 반년 전 것이다.

재무 파일에는 이미 8/26 제출 10-Q(Q2 FY27, 2026-07-26)가 `latestQuarter`로 들어
있는데 계산기가 참조하지 않는다. **데이터가 낡은 게 아니라 모델이 안 쓴다.**

NVDA에서 실제로 무엇을 놓치는가
--------------------------------
장기차입금이 FY2026의 $7.5B에서 Q2 FY27에 **$32.4B로 4.3배** 늘었다. 연간 기준
차입금의존도는 4.1%(5점)인데 분기 기준은 10.4%(4점)다. 이 한 칸이 기본적 분석
점수를 98.0에서 96.1로 내린다. 반년 사이 자본구조가 바뀌었다는 사실이 연간
기준으로는 내년 2월까지 보이지 않는다.

무엇을 바꾸고 무엇을 그대로 두나
--------------------------------
**배점 구간(버킷)은 손대지 않는다.** `fundamental_score_config_v1.json`을 그대로
읽는다. 기준을 같이 바꾸면 점수 차이가 입력 때문인지 기준 때문인지 알 수 없다.

- **재무건전성 5개**: 전부 최신 분기로 계산한다. 넷은 대차대조표 시점값이고
  이자보상배율은 비율이라 한 분기로도 뜻이 통한다.
- **마진 2개**: 최신 분기의 매출 대비 비율. 비율이므로 연환산이 필요 없다.
- **성장률 2개(CAGR)**: 연간 시계열 그대로 둔다. 여러 해가 필요한 값이라
  분기로 바꿀 수 없다.
- **밸류에이션 축은 계산하지 않는다.** 이 점수의 정의가 "재무제표에서 나온 것"
  이기 때문이다. 배수 비교는 `build_peer_score.py`와 `build_multiple_history.py`가
  따로 답한다. 따라서 만점은 33+34 = 67이고 100점으로 환산한다.

`--basis annual`로 돌리면 redesign v1과 같은 입력을 쓴다. 두 저장소가 갈리지
않았는지 확인하는 용도다 — v1의 (재무건전성 + 성장·수익성 축) ÷ 67 × 100과 같아야
한다. 2026-09-23 은행 제외 60종목 전부 일치(NVDA 98.0). 예전 문서의 98.1은 축 점수를
먼저 반올림하고 더한 값이었다(31.7 + 34 → 98.06). v1은 반올림 전 값으로 더한다
(31.68 + 34 → 98.03).

결측 처리와 해석 제한 표시(`qualityFlags`)는 v1 규칙을 그대로 따른다 — 아래
score_items() 앞의 주석 참고.

사용법
------
    python3 v2/build_fundamental_score.py NVDA
    python3 v2/build_fundamental_score.py NVDA --basis annual      # 검산
    python3 v2/build_fundamental_score.py NVDA --json v2/NVDA_fundamental.json
    python3 v2/build_fundamental_score.py NVDA --card    # 카드의 FUNDAMENTAL 블록 교체
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CONFIG = os.path.join(REPO, "v2", "fundamental_score_config_v1.json")
DEFAULT_DATA = os.path.join(REPO, "v2", "fundamental_data")

HEALTH = ["currentRatio", "quickRatio", "debtDependency",
          "interestCoverage", "debtToEquity"]
GROWTH = ["revenueCagr", "opIncomeCagr", "opMargin", "netMargin"]

# 결측 처리는 v1(`stock-widgets-redesign/scripts/compute_fundamental_score.py`)을
# 그대로 옮긴다. 2026-09-23 이전 v2는 이 규칙을 빠뜨려서 NVDA 밖에서는 v1보다
# 나빴다(Fable 검증, 은행 제외 60종목):
#   - 결측 항목이 0점이 됐다(v1은 쓸 수 있는 항목으로 재척도). MRK 63.1 → 21.3.
#   - 음수 자본이 0점·무표시(v1은 1점 + negative_equity). ABBV·DELL·PM.
#   - 총부채 결측 시 자산 − 자본 역산, 재고 결측 시 0 대입, 영업이익 추정
#     (세전이익 + 이자비용), 적자·흑자 전환 CAGR 고정점이 전부 없었다.
#   - 분기값이 없으면 연간 최신값으로 조용히 떨어졌다. KLAC은 2015년 영업이익을
#     2026년 매출로 나눠 OPM 5.7%(실제 약 40%)가 나왔다 — v1이 이미 고친 결함.
# 검산: `--basis annual`은 v1의 재무건전성·성장수익성 축과 같은 값을 내야 한다.


def _core_tickers():
    path = os.path.join(REPO, "v2", "core_earnings.json")
    if not os.path.exists(path):
        return set()
    return {k for k in json.load(open(path)) if not k.startswith("_")}


def _rows(fin, key):
    return [e for e in fin.get(key, {}).get("annual", []) if e.get("val") is not None]


def _q(fin, key):
    q = fin.get(key, {}).get("latestQuarter")
    return q if q and q.get("val") is not None else None


def instant_series(fin, key, basis):
    """대차대조표 값. 분기 기준이면 연간 이력 뒤에 최신 분기 시점값을 붙인다."""
    rows = _rows(fin, key)
    q = _q(fin, key) if basis == "quarter" else None
    if q and (not rows or q["end"] > max(e["end"] for e in rows)):
        rows = rows + [{"end": q["end"], "val": q["val"]}]
    return rows


def latest_instant(entries):
    usable = [e for e in entries if e.get("val") is not None]
    return max(usable, key=lambda e: e["end"])["val"] if usable else None


def instant_pair(a, b):
    """두 시점값을 **같은 결산일**에서 꺼낸다(v1 instant_pair)."""
    ba = {e["end"]: e["val"] for e in a if e.get("val") is not None}
    bb = {e["end"]: e["val"] for e in b if e.get("val") is not None}
    shared = sorted(set(ba) & set(bb))
    if not shared:
        return None, None, None
    end = shared[-1]
    return ba[end], bb[end], end


def value_at(entries, end):
    for e in entries:
        if e.get("end") == end and e.get("val") is not None:
            return e["val"]
    return None


def bucket_points(value, spec):
    """동결 설정의 버킷을 그대로 적용한다. 경계는 upper_exclusive."""
    if value is None:
        return None
    for b in spec["buckets"]:
        u = b["upper_exclusive"]
        if u is None or value < u:
            return b["points"]
    return spec["buckets"][-1]["points"]


def operating_income_annual(fin):
    """(연간 영업이익, 추정 여부). 태그가 아예 없으면 세전이익 + 이자비용(v1)."""
    op = _rows(fin, "operatingIncome")
    if op:
        return op, False
    interest = {e["end"]: e["val"] for e in _rows(fin, "interestExpense")}
    est = [{"end": e["end"], "val": e["val"] + abs(interest[e["end"]])}
           for e in _rows(fin, "pretaxIncome") if e["end"] in interest]
    return est, bool(est)


def quarter_flow(fin, key, end):
    """최신 분기 흐름값. 매출과 **같은 분기**일 때만 쓴다."""
    q = _q(fin, key)
    return q["val"] if q and q["end"] == end else None


def operating_income_quarter(fin, end):
    op = quarter_flow(fin, "operatingIncome", end)
    if op is not None:
        return op, False
    pt, ie = quarter_flow(fin, "pretaxIncome", end), quarter_flow(fin, "interestExpense", end)
    if pt is not None and ie is not None:
        return pt + abs(ie), True
    return None, False


def find_cagr_pair(entries, target_years):
    from datetime import date
    usable = sorted([e for e in entries if e.get("val") is not None], key=lambda e: e["end"])
    if len(usable) < 2:
        return None
    latest = usable[-1]
    le = date.fromisoformat(latest["end"])
    best, diff = None, None
    for e in usable[:-1]:
        back = (le - date.fromisoformat(e["end"])).days
        if back <= 0:
            continue
        d = abs(back - target_years * 365.25)
        if diff is None or d < diff:
            best, diff = e, d
    if best is None:
        return None
    return best, latest, (le - date.fromisoformat(best["end"])).days / 365.25


def growth_metric(entries, target_years, spec):
    """부호가 바뀌면 고정점(v1): 흑자전환 4 · 적자전환 1 · 적자 지속 1."""
    pair = find_cagr_pair(entries, target_years)
    if pair is None:
        return None
    base, latest, yrs = pair
    b, l = base["val"], latest["val"]
    if b > 0 and l > 0:
        v = ((l / b) ** (1 / yrs) - 1) * 100
        return {"value": v, "points": bucket_points(round(v, 1), spec)}
    if b <= 0 < l:
        return {"value": None, "points": 4, "note": "흑자 전환"}
    if l <= 0 < b:
        return {"value": None, "points": 1, "note": "적자 전환"}
    return {"value": None, "points": 1, "note": "적자 지속"}


def annual_is_newer(fin):
    """연간 보고서(10-K)가 최신 10-Q보다 새로운가. 회계연도 말 직후 종목이 그렇다 —
    4분기는 10-Q가 없어 latestQuarter가 한 분기 전(3분기)에 머문다. MSFT는 FY26 10-K
    (2026-06-30, 7/29 공시)가 있는데 3월 분기로 계산되고 있었다(2026-09-24)."""
    lq = (fin.get("revenue", {}).get("latestQuarter") or {})
    rev_a = _rows(fin, "revenue")
    return bool(lq and rev_a and max(e["end"] for e in rev_a) > lq["end"])


def score_items(fin, config, basis):
    """항목별 (값, 점수, 상태). 분기 기준은 대차대조표·마진·이자보상에 최신 분기를 쓴다."""
    h, g = config["health"]["ratios"], config["growth_profit"]["metrics"]
    items, flags = {}, []
    S = lambda k: instant_series(fin, k, basis)

    # 연간이 더 새로우면 흐름값(마진·이자보상)도 연간을 쓴다 — 가장 최신 기간이다.
    rev_q = _q(fin, "revenue") if basis == "quarter" and not annual_is_newer(fin) else None
    q_end = rev_q["end"] if rev_q else None
    op_annual, op_est_annual = operating_income_annual(fin)

    # 유동·당좌 — 같은 결산일, 재고 결측은 0(v1)
    ca, cl, end = instant_pair(S("currentAssets"), S("currentLiabilities"))
    if ca is not None and cl:
        items["currentRatio"] = {"value": ca / cl * 100}
        inv = value_at(S("inventory"), end) or 0
        items["quickRatio"] = {"value": (ca - inv) / cl * 100}

    # 차입금의존도 — 차입금 태그가 둘 다 없으면 무차입과 결측을 못 가르므로 결측(v1)
    sd, ld, assets = S("shortTermDebt"), S("longTermDebt"), latest_instant(S("assets"))
    if (sd or ld) and assets:
        items["debtDependency"] = {"value": ((latest_instant(sd) or 0) + (latest_instant(ld) or 0)) / assets * 100}

    # 이자보상배율 — 분기 기준이면 최신 분기 영업이익·이자비용(같은 분기)
    if basis == "quarter" and q_end:
        op, est = operating_income_quarter(fin, q_end)
        op_end = q_end if op is not None else None
    else:
        e = max(op_annual, key=lambda x: x["end"], default=None)
        op, est, op_end = (e["val"], op_est_annual, e["end"]) if e else (None, False, None)
    if est:
        flags.append("operating_income_estimated")
    # 태그가 아예 있는지는 연간·분기 전체로 보지만, 나누는 값은 영업이익과 **같은
    # 기간**이어야 한다. 최신 분기가 회계연도 말이면 연간·분기 이자비용이 같은
    # 결산일로 겹친다 — 섞으면 분기 영업이익을 연간 이자비용으로 나눈다(Codex).
    has_interest_tag = bool(_rows(fin, "interestExpense") or _q(fin, "interestExpense"))
    if op is not None:
        if op <= 0:
            items["interestCoverage"] = {"value": None, "points": 1, "note": "영업적자"}
        elif not has_interest_tag:
            items["interestCoverage"] = {"value": None, "points": 5, "note": "이자비용 태그 없음"}
        else:
            iv = (quarter_flow(fin, "interestExpense", op_end) if basis == "quarter" and q_end
                  else value_at(_rows(fin, "interestExpense"), op_end))
            if iv == 0:
                items["interestCoverage"] = {"value": None, "points": 5, "note": "이자비용 0"}
            elif iv is not None:
                items["interestCoverage"] = {"value": op / abs(iv)}

    # 부채비율 — 총부채 결측이면 자산 − 자본, 음수 자본은 1점 + 표시(v1)
    tl, eq, _ = instant_pair(S("totalLiabilities"), S("equityAttributableToParent"))
    if tl is None:
        a, e2, _ = instant_pair(S("assets"), S("equityAttributableToParent"))
        if a is not None and e2 is not None:
            tl, eq = a - e2, e2
    if tl is not None and eq is not None:
        if eq <= 0:
            items["debtToEquity"] = {"value": None, "points": 1, "note": "자본 음수"}
            flags.append("negative_equity")
        else:
            items["debtToEquity"] = {"value": tl / eq * 100}

    # 성장 — 연간 CAGR. 영업이익 태깅이 매출보다 먼저 끝났으면 쓰지 않는다(v1)
    rev_a = _rows(fin, "revenue")
    look = config["growth_profit"]["cagr_lookback_years_target"]
    r = growth_metric(rev_a, look, g["revenueCagr"])
    if r:
        items["revenueCagr"] = r
    rev_end = max((e["end"] for e in rev_a), default=None)
    op_a_end = max((e["end"] for e in op_annual), default=None)
    if op_a_end is not None and op_a_end == rev_end:
        r = growth_metric(op_annual, look, g["opIncomeCagr"])
        if r:
            items["opIncomeCagr"] = r
        if op_est_annual:
            flags.append("operating_income_estimated")

    # 마진 — 분기 기준은 최신 분기, 연간 기준은 최신 연도. 분자·분모는 같은 기간.
    ni_key = "netIncomeAttributableToParent" if (_rows(fin, "netIncomeAttributableToParent") or _q(fin, "netIncomeAttributableToParent")) else "netIncome"
    # 지배주주 순이익 태그가 멈췄으면 연결 순이익으로 간다. AVGO는 우선주 전환(2023) 뒤
    # NetIncomeLossAvailableToCommonStockholdersBasic을 FY2024에서 멈춰, 최신 분기 순이익률이 비었다.
    def _last_end(key):
        ends = [e["end"] for e in _rows(fin, key)] + [(_q(fin, key) or {}).get("end", "")]
        return max(ends) if ends else ""
    if ni_key != "netIncome" and _last_end(ni_key) < _last_end("netIncome"):
        ni_key = "netIncome"
    if basis == "quarter" and q_end:
        rv = rev_q["val"]
        op_m, _ = operating_income_quarter(fin, q_end)
        ni = quarter_flow(fin, ni_key, q_end)
    else:
        rv = latest_instant(rev_a)
        op_m = value_at(op_annual, rev_end) if op_a_end == rev_end else None
        ni = latest_instant(_rows(fin, ni_key))
    if rv:
        if op_m is not None:
            items["opMargin"] = {"value": op_m / rv * 100}
        core = fin.get("ticker") in _core_tickers()
        if core and op_m is not None:
            # 본업 기준(v2/core_earnings.json) — 순이익 대신 영업이익 × (1 − 실효세율).
            # GOOGL 2026 Q2 순이익률 93.6%는 비상장 지분 재평가 이익 때문이다(2026-09-24 사용자 결정).
            import build_dcf as d
            b = d.base_inputs(fin["ticker"])
            # 법인세 0은 정상 값이다(0을 거짓으로 보고 21%로 바꾸면 안 된다). 세전이익이 0 이하면
            # 실효세율이 뜻을 잃으므로 본업 순이익률을 내지 않는다 — PER 경로와 같은 처리(Codex).
            tax, pretax = b.get("tax"), b.get("pretax")
            if tax is not None and pretax is not None and pretax > 0:
                items["netMargin"] = {"value": op_m * (1 - tax / pretax) / rv * 100, "basis": "core"}
        elif ni is not None:
            items["netMargin"] = {"value": ni / rv * 100}

    for k, it in items.items():
        spec = h.get(k) or g.get(k)
        if "points" not in it:
            # v1은 소수 첫째 자리로 반올림한 값으로 버킷을 정한다
            it["points"] = bucket_points(round(it["value"], 1), spec)
    if basis == "quarter" and not q_end and not annual_is_newer(fin):
        flags.append("no_latest_quarter")
    return items, sorted(set(flags))


def compute(ticker, fin, config, basis):
    items, flags = score_items(fin, config, basis)
    weights, gate = config["axis_weights"], config["coverage_gate"]

    axes = {}
    for name, keys, cfg_key in (("health", HEALTH, "health"),
                                ("growthProfit", GROWTH, "growth_profit")):
        specs = config[cfg_key].get("ratios") or config[cfg_key].get("metrics")
        rows, pts = [], []
        for k in keys:
            it = items.get(k, {})
            rows.append({"metric": k, "value": it.get("value"), "points": it.get("points"),
                         "note": it.get("note"),
                         "label": specs[k].get("label", k), "unit": specs[k].get("unit"),
                         "higherIsBetter": specs[k].get("higher_is_better", True),
                         "buckets": specs[k]["buckets"]})
            if it.get("points") is not None:
                pts.append(it["points"])
        w = weights["health" if name == "health" else "growth_profit"]
        # 쓸 수 있는 항목만으로 축 만점에 맞춘다(v1). 결측을 0점으로 세지 않는다.
        raw = sum(pts) / (5 * len(pts)) * w if pts else None
        axes[name] = {"rows": rows, "used": len(pts), "pointsRaw": raw,
                      "points": round(raw, 1) if raw is not None else None, "max": w}

    if not axes["health"]["used"] >= gate["min_health_ratios"]:
        flags.append("health_ratios_below_gate")
    if not axes["growthProfit"]["used"] >= gate["min_growth_profit_metrics"]:
        flags.append("growth_metrics_below_gate")

    total_max = axes["health"]["max"] + axes["growthProfit"]["max"]
    raws = [a["pointsRaw"] for a in axes.values()]
    score = round(sum(raws) / total_max * 100, 1) if None not in raws else None
    cuts = config["grade_cuts"]
    grade = (next((g for g, c in sorted(cuts.items(), key=lambda kv: -kv[1]) if score >= c), "미흡")
             if score is not None else None)

    lq = (fin.get("revenue", {}).get("latestQuarter") or {})
    rev_a = _rows(fin, "revenue")
    use_q = basis == "quarter" and lq and not annual_is_newer(fin)
    as_of = lq.get("end") if use_q else (max(e["end"] for e in rev_a) if rev_a else None)
    filed = lq.get("filed") if use_q else (max(rev_a, key=lambda e: e["end"]).get("filed") if rev_a else None)
    return {"ticker": ticker, "basis": basis, "asOf": as_of,
            "filedAt": filed, "periodSource": "10-Q" if use_q else "10-K",
            "score": score, "grade": grade, "qualityFlags": sorted(set(flags)),
            "axes": axes, "axisMaxTotal": total_max,
            "note": "밸류에이션 축은 제외한다 — 이 점수는 재무제표에서 나온 것만 본다",
            "configVersion": config.get("version")}


def show(res, config):
    labels = {}
    for cfg_key in ("health", "growth_profit"):
        specs = config[cfg_key].get("ratios") or config[cfg_key].get("metrics")
        for k, v in specs.items():
            labels[k] = v.get("label", k)
    print(f"{res['ticker']} — 기본적 분석 ({'최신 분기' if res['basis']=='quarter' else '연간'} 기준)")
    print(f"  기준일 {res['asOf']}" + (f" · 공시 {res['filedAt']}" if res["filedAt"] else ""))
    print()
    for name, ko in (("health", "재무건전성"), ("growthProfit", "성장·수익성")):
        a = res["axes"][name]
        print(f"  {ko}  {a['points']}/{a['max']}   (쓴 항목 {a['used']}개)")
        for row in a["rows"]:
            v = row["value"]
            vs = "—" if v is None else (f"{v:>10.1f}" if abs(v) < 1e8 else "     매우큼")
            print(f"    {labels.get(row['metric'], row['metric']):14}{vs}  {row['points']}점"
                  + (f"  ({row['note']})" if row.get("note") else ""))
    print(f"\n  기본적 분석 = {res['score']} / 100   ({res['grade']})")
    if res["qualityFlags"]:
        print("  표시:", ", ".join(res["qualityFlags"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--basis", choices=["quarter", "annual"], default="quarter")
    ap.add_argument("--financials")
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    ap.add_argument("--json")
    ap.add_argument("--card", action="store_true",
                    help="v2/<T>_full_widget.html의 FUNDAMENTAL 블록을 교체한다 (최신 분기 기준만)")
    args = ap.parse_args()
    t = args.ticker.upper()

    path = args.financials or os.path.join(DEFAULT_DATA, f"{t}_financials.json")
    if not os.path.exists(path):
        sys.exit(f"{t}: 재무 파일이 없다 — {path}\n"
                 f"  redesign의 fetch_financials.py --years 5 결과를 {DEFAULT_DATA}/ 에 둔다")
    config = json.load(open(args.config))
    if t in config.get("bank_exclude_tickers", []):
        sys.exit(f"{t}: 은행은 v1에서 채점하지 않는다 (대차대조표 구조가 다르다)")

    res = compute(t, json.load(open(path)), config, args.basis)
    show(res, config)
    if args.json:
        json.dump(res, open(args.json, "w"), ensure_ascii=False, indent=1)
        print("\n저장:", args.json)
    if args.card:
        if args.basis != "quarter":
            sys.exit("--card는 최신 분기 기준으로만 쓴다")
        write_card(t, res)


def net_cash(ticker):
    """순현금 — 내재가치 탭의 DCF와 **같은 입력, 같은 정의**를 쓴다.

    현금 + 단기투자 − 차입금 − 리스. 지분증권(상장주식·비상장 지분)은 넣지 않는다.
    DCF가 그것을 "비영업 투자자산"으로 따로 더하기 때문이다. 2026-09-23 이전 카드는
    지분증권 $42.8B를 넣은 순현금 $66.0B를 희석 가중평균 24.29B주로 나눠 $2.72를
    적었고, 같은 카드의 DCF는 순부채 −$18B를 쓰고 있었다.
    """
    import build_dcf as d
    b = d.base_inputs(ticker)
    # 장기 채권(MarketableSecuritiesNoncurrent, 국채·회사채)은 만기만 길 뿐 현금에 가깝다.
    # 빼면 AAPL이 순현금 $48.4B인데 순부채 −$2.44/주로 보인다(2026-09-24 사용자 결정으로 포함).
    # 지분증권은 여전히 넣지 않는다.
    # 재무가 현지 통화(TSM 대만달러)면 카드의 달러 표시를 위해 가장 최근 환율로 바꾼다(v2/fx.py).
    import fx
    r = fx.rate(ticker, d.bmh.load_daily(ticker)[-1][0])
    parts = {k: (b.get(k) or 0) / r for k in ("cash", "sti", "lt_marketable", "debt", "lease")}
    net = parts["cash"] + parts["sti"] + parts["lt_marketable"] - parts["debt"] - parts["lease"]
    sh = b.get("shares")   # SEC 데이터에 주식 수가 없는 신규 상장(SPCX)이면 주당 값은 비운다
    return {**parts, "shares": sh, "net": net, "perShare": (net / sh) if sh else None}


BEGIN, END = "/* FUNDAMENTAL:BEGIN */", "/* FUNDAMENTAL:END */"


def write_card(ticker, res):
    import re
    out = {**res, "netCash": net_cash(ticker)}
    path = os.path.join(REPO, "v2", f"{ticker}_full_widget.html")
    html = open(path, encoding="utf-8").read()
    pat = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    if len(pat.findall(html)) != 1:
        sys.exit(f"{path}: FUNDAMENTAL 마커가 정확히 한 쌍이 아니다")
    block = f"{BEGIN}\nconst {ticker}_FUNDAMENTAL = {json.dumps(out, ensure_ascii=False)};\n{END}"
    open(path, "w", encoding="utf-8").write(pat.sub(lambda _: block, html))
    print("교체:", path)


if __name__ == "__main__":
    main()
