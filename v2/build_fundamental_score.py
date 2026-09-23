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
점수를 98.1에서 96.1로 내린다. 반년 사이 자본구조가 바뀌었다는 사실이 연간
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

`--basis annual`로 돌리면 redesign의 계산과 같은 입력을 쓴다. 두 저장소가 갈리지
않았는지 확인하는 용도다 — NVDA에서 98.1이 나와야 한다.

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


def annual(fin, key):
    rows = [e for e in fin.get(key, {}).get("annual", []) if e.get("val") is not None]
    return sorted(rows, key=lambda e: e["end"])


def latest_annual(fin, key):
    rows = annual(fin, key)
    return rows[-1]["val"] if rows else None


def latest_quarter(fin, key):
    q = fin.get(key, {}).get("latestQuarter")
    return q.get("val") if q else None


def bucket_points(value, spec):
    """동결 설정의 버킷을 그대로 적용한다. 경계는 upper_exclusive."""
    if value is None:
        return None
    for b in spec["buckets"]:
        u = b["upper_exclusive"]
        if u is None or value < u:
            return b["points"]
    return spec["buckets"][-1]["points"]


def cagr(rows, years):
    """실제 경과 연수로 나눈다. 부호가 바뀌면(적자→흑자 등) 계산하지 않는다."""
    if len(rows) < 2:
        return None
    n = min(years, len(rows) - 1)
    a, b = rows[-1 - n]["val"], rows[-1]["val"]
    if a is None or b is None or a <= 0 or b <= 0:
        return None
    return ((b / a) ** (1 / n) - 1) * 100


def ratios(fin, basis):
    """basis='quarter'면 최신 분기, 'annual'이면 최신 연간치를 쓴다."""
    get = latest_quarter if basis == "quarter" else latest_annual

    def g(k):
        v = get(fin, k)
        return v if v is not None else latest_annual(fin, k)

    ca, cl, inv = g("currentAssets"), g("currentLiabilities"), g("inventory")
    std, ltd, assets = g("shortTermDebt"), g("longTermDebt"), g("assets")
    tl, eq = g("totalLiabilities"), g("equityAttributableToParent")
    op, ie = g("operatingIncome"), g("interestExpense")
    rev, ni = g("revenue"), g("netIncome")
    out = {}
    out["currentRatio"] = ca / cl * 100 if ca and cl else None
    out["quickRatio"] = (ca - inv) / cl * 100 if ca and cl and inv is not None else None
    out["debtDependency"] = ((std or 0) + (ltd or 0)) / assets * 100 if assets else None
    out["interestCoverage"] = (op / ie if op and ie and op > 0 else
                               (1e9 if op and not ie else None))
    out["debtToEquity"] = tl / eq * 100 if tl and eq and eq > 0 else None
    out["opMargin"] = op / rev * 100 if op is not None and rev else None
    out["netMargin"] = ni / rev * 100 if ni is not None and rev else None
    return out


def compute(ticker, fin, config, basis):
    look = config["growth_profit"]["cagr_lookback_years_target"]
    r = ratios(fin, basis)
    r["revenueCagr"] = cagr(annual(fin, "revenue"), look)
    r["opIncomeCagr"] = cagr(annual(fin, "operatingIncome"), look)

    axes = {}
    for name, keys, cfg_key in (("health", HEALTH, "health"),
                                ("growthProfit", GROWTH, "growth_profit")):
        cfg = config[cfg_key]
        specs = cfg.get("ratios") or cfg.get("metrics")
        rows, raw, used = [], 0, 0
        for k in keys:
            pts = bucket_points(r.get(k), specs[k])
            rows.append({"metric": k, "value": r.get(k), "points": pts,
                         "label": specs[k].get("label", k), "unit": specs[k].get("unit"),
                         "higherIsBetter": specs[k].get("higher_is_better", True),
                         "buckets": specs[k]["buckets"]})
            if pts is not None:
                raw += pts
                used += 1
        axes[name] = {"rows": rows, "raw": raw, "used": used,
                      "points": round(raw * cfg["scale_to_axis"], 1),
                      "max": round(cfg["max_raw_points"] * cfg["scale_to_axis"], 1)}

    total_max = axes["health"]["max"] + axes["growthProfit"]["max"]
    total = axes["health"]["points"] + axes["growthProfit"]["points"]
    score = round(total / total_max * 100, 1)
    cuts = config["grade_cuts"]
    grade = next((g for g, c in sorted(cuts.items(), key=lambda kv: -kv[1])
                  if score >= c), "미흡")

    lq = (fin.get("revenue", {}).get("latestQuarter") or {})
    as_of = lq.get("end") if basis == "quarter" else (
        annual(fin, "revenue")[-1]["end"] if annual(fin, "revenue") else None)
    return {"ticker": ticker, "basis": basis, "asOf": as_of,
            "filedAt": lq.get("filed") if basis == "quarter" else None,
            "score": score, "grade": grade,
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
        print(f"  {ko}  {a['points']}/{a['max']}   (원점수 {a['raw']}/{a['used']*5})")
        for row in a["rows"]:
            v = row["value"]
            vs = "—" if v is None else (f"{v:>10.1f}" if abs(v) < 1e8 else "     매우큼")
            print(f"    {labels.get(row['metric'], row['metric']):14}{vs}  {row['points']}점")
    print(f"\n  기본적 분석 = {res['score']} / 100   ({res['grade']})")


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
    parts = {k: b.get(k) or 0 for k in ("cash", "sti", "debt", "lease")}
    net = parts["cash"] + parts["sti"] - parts["debt"] - parts["lease"]
    return {**parts, "shares": b["shares"], "net": net, "perShare": net / b["shares"]}


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
