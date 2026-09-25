#!/usr/bin/env python3
"""v2 시안: 시점별 DCF와 그 성적표.

왜 필요한가
-----------
오늘 기준 내재가치 하나를 차트에 가로줄로 그으면 "2021년에도 내재가치가
$318이었다"고 말하는 셈이 된다. 실제로는 실적이 바뀔 때마다 내재가치도 바뀐다.
백테스트가 체크포인트마다 그 시점 공시만으로 PER 밴드를 다시 만드는 것과
같은 규칙을 DCF에도 적용한다.

그리고 그렇게 만들면 DCF에도 **성적표**가 생긴다. "저평가라고 말한 시점 이후
주가가 올랐는가"를 세어볼 수 있다. 내재가치 계산은 원래 몇 년을 기다려야
맞았는지 알 수 있는데, 과거 시점으로 돌아가 계산하면 그 기다림을 건너뛴다.

미래 정보를 쓰지 않는다
-----------------------
각 시점의 입력은 `build_dcf.base_inputs(ticker, asof=...)`가 그날까지 공시된
것만 고른다. 성장·마진 이력도 같은 규칙이다. 판정 이후의 주가만 결과 쪽에
쓴다.

읽을 때 주의 — 이 성적표는 화면에 올리지 않는다
-----------------------------------------------
이 모델은 과거 성장률을 미래에 투영하므로 **실적이 좋아지면 내재가치도 뒤따라
올라간다.** 즉 저평가 판정이 실적을 앞서가지 않고 뒤따라가는 구조다. 성적표가
좋게 나와도 그것이 예측력의 증거는 아니다. 표본도 분기 단위라 十여 개뿐이고,
연속한 시점은 대부분 같은 재무제표를 공유해 독립 시행이 아니다.

2026-09-22에 NVDA로 실제로 확인했다. 한때 카드 헤더에 "내재가치 신뢰도 71%"로
올라가 있던 숫자인데, 검정 두 가지를 다 통과하지 못했다.

- **기간을 바꾸면 무너진다.** 같은 판정으로 21/63/126/189/252거래일을 재면
  75% / 50% / 71% / 17% / 20%가 나온다. 71%는 126일을 고른 결과다.
- **장기에서 기준선을 못 넘는다.** 같은 판정일에 그냥 사기만 했을 때와 비교하면
  126일은 모델 71% 대 57%로 모델이 앞서지만, 189일은 17% 대 100%,
  252일은 20% 대 100%다. 모델이 다섯 번 외친 "고평가" 뒤로 NVDA가 전부 올랐다.

처음에는 여기서 구간 안 **모든 거래일**의 상승률(126일 81%)을 기준선으로 써서
"126일에서도 기준선을 못 넘는다"고 적었는데, 짝이 맞지 않는 비교였다. 모델은
판정일 7개에서만 말하는데 기준선은 390일에서 말한 것이다. 2026-09-22에 Codex와
Fable이 독립적으로 같은 지적을 했다.

내재가치는 2년 동안 4.65배가 됐고 주가는 1.67배였다. 모델이 주가보다 빠르게
실적을 쫓아간 것이다. 그래서 헤더에서 그 칸을 빼고 역방향 DCF(현재가 요구
성장률)로 바꿨다. 이 스크립트는 여전히 쓸모가 있다 — 시점별 내재가치 띠를
차트에 그리는 원천이다. 다만 **성적표는 진단용이지 카드에 실을 성과가 아니다.**

사용법
------
    python3 v2/build_dcf_track.py NVDA
    python3 v2/build_dcf_track.py NVDA --horizon 126 --json out.json
"""
import argparse
import json
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import build_dcf as d  # noqa: E402
import build_multiple_history as bmh  # noqa: E402
import fx  # noqa: E402


def quarter_ends(ticker, start="2022-01-01"):
    """분기 실적이 공개된 날짜들. 그 시점마다 내재가치를 다시 계산한다."""
    cik = d.feh.CIKS[ticker]
    tag, rows = bmh.pick_tag(cik, bmh.FLOW_TAGS["revenue"])
    ttm = bmh.ttm_series(bmh.quarterly_flow(rows, ticker))
    return [e["available"] for e in ttm if e["available"] >= start]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--wacc", type=float, default=0.10)
    ap.add_argument("--terminal", type=float, default=0.025)
    ap.add_argument("--horizon", type=int, default=126, help="판정 이후 며칠 뒤 주가를 볼지(거래일)")
    ap.add_argument("--json", help="결과 저장 경로")
    args = ap.parse_args()
    t = args.ticker.upper()

    daily = bmh.load_daily(t)
    dates = [b[0] for b in daily]
    closes = {b[0]: b[4] for b in daily}

    # 성적표 검정에 쓸 보유기간들. 하나만 보면 그 하나를 고른 결과를 본다.
    HORIZONS = sorted({21, 63, 126, 189, 252, args.horizon})

    def idx_at(day):
        prior = [i for i, x in enumerate(dates) if x <= day]
        return prior[-1] if prior else None

    def price_at(day):
        i = idx_at(day)
        return closes[dates[i]] if i is not None else None

    def forward(day, bars):
        idx = [i for i, x in enumerate(dates) if x <= day]
        if not idx:
            return None
        j = idx[-1] + bars
        return closes[dates[j]] if j < len(dates) else None

    points = []
    for day in quarter_ends(t):
        base = d.base_inputs(t, asof=day)
        hist = d.history(t, asof=day)
        if not base.get("revenue") or not base.get("shares") or not hist:
            continue
        try:
            # 재무가 현지 통화(TSM)면 그 시점 환율로 달러로 되돌려 그날 ADR 가격과 비교한다(v2/fx.py).
            r = fx.rate(t, day)
            scs = {x["name"]: x["per_share"] / r for x in d.scenarios(base, hist, args.wacc, args.terminal)}
        except Exception:
            continue
        px = price_at(day)
        fwd = forward(day, args.horizon)
        points.append({
            "date": day, "price": px,
            "low": scs["보수"], "base": scs["기본"], "high": scs["낙관"],
            "forward_price": fwd,
            "forward_return": (fwd / px - 1) if (fwd and px) else None,
        })

    print(f"{t} — 시점별 DCF (WACC {args.wacc:.0%} · 영구성장 {args.terminal:.1%}"
          f" · 이후 {args.horizon}거래일 수익률)")
    print(f"{'시점':12s} {'주가':>8s} {'낮은성장':>9s} {'기본':>8s} {'높은성장':>9s} {'판정':>12s} {'이후수익률':>10s}")
    for p in points:
        if p["price"] < p["low"]:
            verdict = "저평가(낮은성장)"
        elif p["price"] < p["base"]:
            verdict = "저평가(기본)"
        elif p["price"] < p["high"]:
            verdict = "고평가(기본)"
        else:
            verdict = "고평가(전부)"
        r = f"{p['forward_return']*100:+9.1f}%" if p["forward_return"] is not None else "        —"
        print(f"{p['date']:12s} {p['price']:8.2f} {p['low']:9.0f} {p['base']:8.0f} {p['high']:9.0f}"
              f" {verdict:>14s} {r}")

    # 성적표 — 판정별로 이후 수익률을 모은다
    print("\n판정별 이후 수익률")
    buckets = {}
    for p in points:
        if p["forward_return"] is None:
            continue
        key = "주가 < 낮은성장" if p["price"] < p["low"] else (
            "주가 < 기본" if p["price"] < p["base"] else (
                "주가 < 높은성장" if p["price"] < p["high"] else "주가 > 전부"))
        buckets.setdefault(key, []).append(p["forward_return"])
    for key in ["주가 < 낮은성장", "주가 < 기본", "주가 < 높은성장", "주가 > 전부"]:
        rs = buckets.get(key, [])
        if not rs:
            print(f"  {key:16s} 표본 없음")
            continue
        # 표본이 짝수면 `sorted(rs)[n//2]`는 가운데가 아니라 위쪽 값이다.
        # 2건짜리 칸에서 +19.6%가 아니라 +31.9%로 나왔다(Codex 발견).
        med = statistics.median(rs)
        up = sum(1 for x in rs if x > 0)
        print(f"  {key:16s} 표본 {len(rs):2d}개 · 중앙 수익률 {med*100:+6.1f}% · 상승 {up}/{len(rs)}")
    # ── 성적표를 믿기 전에 통과해야 하는 두 가지 ──
    # 2026-09-22 NVDA에서 둘 다 통과하지 못했다. 그래서 카드 헤더의
    # "내재가치 신뢰도 71%"를 뺐다. 같은 착각을 다음 종목에서 반복하지 않으려고
    # 여기서 매번 같이 찍는다.
    def hit_rate(h):
        hit = tot = 0
        for p in points:
            i = idx_at(p["date"])
            if i is None or i + h >= len(dates):
                continue
            r = closes[dates[i + h]] / p["price"] - 1
            cheap = p["price"] < p["base"]
            tot += 1
            hit += 1 if ((r > 0) if cheap else (r < 0)) else 0
        return hit, tot

    print("\n① 보유기간을 바꿔도 같은 성적이 나오는가 (판정은 고정)")
    for h in HORIZONS:
        hit, tot = hit_rate(h)
        pct = f" = {hit/tot*100:.0f}%" if tot else ""
        mark = "  ← 지금 쓰는 값" if h == args.horizon else ""
        print(f"  {h:3d}거래일 보유 → 방향 적중 {hit}/{tot}{pct}{mark}")
    print("  기간마다 답이 크게 달라지면 그 숫자는 기간 선택의 결과지 모델의 성적이 아니다.")

    # ② 기준선은 **같은 날**이어야 한다.
    #
    # 처음에는 구간 안 모든 거래일의 상승률(126일이면 315/390 = 81%)을 기준선으로
    # 썼는데, 그건 짝이 맞지 않는 비교다. 모델은 분기 판정일 7개에서만 말하고
    # 기준선은 390일에서 말한다. Codex와 Fable이 독립적으로 같은 지적을 했고,
    # 같은 판정일로 맞추면 126일에서는 모델이 오히려 앞선다(71% 대 57%).
    # 전 거래일 상승률은 시장 국면을 설명할 뿐 모델의 추가 예측력을 재지 못한다.
    def always_buy(h):
        """같은 판정일에 아무 판단 없이 사기만 했을 때의 방향 적중."""
        hit = tot = 0
        for p in points:
            i = idx_at(p["date"])
            if i is None or i + h >= len(dates):
                continue
            tot += 1
            hit += 1 if closes[dates[i + h]] / p["price"] - 1 > 0 else 0
        return hit, tot

    print("\n② 같은 판정일에 그냥 샀을 때보다 나은가 (짝지은 기준선)")
    i0, i1 = idx_at(points[0]["date"]), idx_at(points[-1]["date"])
    for h in HORIZONS:
        hit, tot = hit_rate(h)
        bh, bt = always_buy(h)
        if not tot:
            print(f"  {h:3d}거래일 보유 → 표본 없음")
            continue
        rs = [closes[dates[i + h]] / closes[dates[i]] - 1
              for i in range(i0, i1 + 1) if i + h < len(dates)]
        env = f" · 참고: 같은 구간 전 거래일 상승 {sum(1 for x in rs if x > 0)}/{len(rs)}" if rs else ""
        print(f"  {h:3d}거래일 보유 → 모델 {hit}/{tot} = {hit/tot*100:.0f}%"
              f" · 그냥 매수 {bh}/{bt} = {bh/bt*100:.0f}%{env}")
    print(f"  표본이 {len(points)}개뿐이고 연속 시점이 재무제표를 공유하므로,"
          "\n  어느 쪽이 앞서든 통계적 우월성을 주장할 수 없다. 방향만 본다.")

    print("\n⚠ 연속한 시점은 대부분 같은 재무제표를 공유해 독립 시행이 아니다."
          "\n⚠ 이 모델은 과거 성장률을 투영하므로 내재가치가 실적을 뒤따라 오른다."
          " 성적표가 좋아도 예측력의 증거가 아니다.")

    if args.json:
        json.dump({"ticker": t, "wacc": args.wacc, "horizon": args.horizon, "points": points},
                  open(args.json, "w"), ensure_ascii=False, indent=1)
        print("저장:", args.json)


if __name__ == "__main__":
    main()
