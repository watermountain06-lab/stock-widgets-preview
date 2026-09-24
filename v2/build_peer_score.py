#!/usr/bin/env python3
"""동종업 대비 밸류에이션 점수 — 같은 GICS 섹터 안에서 배수 순위를 매긴다.

왜 자기 이력만으로는 모자란가
------------------------------
`build_multiple_history.py`는 "이 종목의 배수가 **자기 5년 분포**에서 하위 몇 %인가"를
점수로 준다. NVDA는 89.2점이다(2026-09-23 PCR 짝맞춤 수정 후). 그런데 그 질문은 "다른 회사 대신 이걸 사야 하나"에
답하지 않는다. 계속 비싸지기만 한 종목은 자기 이력 대비로는 영원히 비싸고, 계속
싸지는 종목은 영원히 싸다.

같은 섹터 안에서 다시 세면 답이 달라진다. NVDA는 동종업 대비 47.5점이다. **44점이
벌어진다** — 이익 기준(PER)으로는 25종목 중 6위로 싸지만 자산·매출 기준(PBR·PSR)으로는
하위권이다. 마진이 예외적이라 같은 매출·자산에서 훨씬 많은 이익을 뽑기 때문이다.
두 점수를 평균으로 뭉개면 이 사실이 사라지므로 카드는 둘을 **나란히** 싣는다.

어떻게 세는가
-------------
섹터는 `v2/sectors.json`(GICS 11 분류, 70종목). 배수는 각 종목의
`site_data/valuation_base/{T}.json`에 있는 `value0`을 `site_data/stocks.json`의
현재 종가로 환산해 만든다(`price-ratio`는 비례, `ev-delta`는 EV에 시총 변화분을 더함).
**네트워크를 쓰지 않는다** — 70종목 SEC 조회는 429를 부른다.

점수는 배수마다 `100 - (나보다 싼 동종업 비율)`이다. 배수가 낮을수록 싸므로 점수가
높다. 다섯 배수의 단순평균이 최종값이다.

일부러 하지 않은 것
-------------------
- **피어를 손으로 고르지 않는다.** 카드의 `MULTIPLE_DATA`는 배수마다 AVGO·AMD·TSM을
  손으로 골라 두세 개만 쓰는데, 고르는 근거가 파일에 없고 날짜도 없다. 여기서는
  섹터 전체를 쓴다. 표본이 3개에서 25개로 늘고, 무엇을 넣고 뺄지 고민할 여지가 없다.
- **가중치를 주지 않는다.** 다섯 배수 단순평균이다. 업종별 가중은 근거가 생기면 붙인다.
- **회계 기준 차이를 보정하지 않는다.** IT 섹터에 TSM(IFRS)·ASML이 섞여 있고 파운드리와
  팹리스는 자산집약도가 다르다. 보정하려면 다시 손으로 고르는 일이 되므로, 보정 대신
  **표본 수를 늘려** 개별 차이가 순위에 미치는 영향을 줄였다. 한 종목이 순위를 뒤집지
  못한다는 뜻이지 비교가 공정해졌다는 뜻은 아니다.

무엇을 버리는가
---------------
- `frozen: true`인 배수. 그 값은 일부러 갱신을 멈춘 것이라 현재가로 환산하면 틀린다.
- `value0`이 없거나 0 이하인 배수(적자 종목의 음수 PER 등).
- 남은 표본이 `MIN_PEERS`개 미만인 배수. 서너 종목의 순위는 순위가 아니다.

사용법
------
    python3 v2/build_peer_score.py NVDA
    python3 v2/build_peer_score.py NVDA --json v2/NVDA_peer_score.json
    python3 v2/build_peer_score.py NVDA --self v2/NVDA_multiples.json
    python3 v2/build_peer_score.py NVDA --self v2/NVDA_multiples.json --card   # 카드 블록 교체
"""
import argparse
import json
import os
import statistics
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTORS = os.path.join(REPO, "v2", "sectors.json")
SECTOR_BORROW = {"Communication Services": ["Information Technology"],
                 # AMZN·HD·TSLA 3종목뿐(2026-09-24 사용자 결정, AMZN)
                 "Consumer Discretionary": ["Information Technology"]}
STOCKS = os.path.join(REPO, "site_data", "stocks.json")
VBASE = os.path.join(REPO, "site_data", "valuation_base")

METRICS = ["per", "pbr", "psr", "pcr", "evebitda"]
LABELS = {"per": "PER", "pbr": "PBR", "psr": "PSR",
          "pcr": "PCR", "evebitda": "EV/EBITDA"}
MIN_PEERS = 8          # 이보다 적으면 그 배수는 버린다


def load_sectors():
    d = json.load(open(SECTORS))
    return {k: v for k, v in d.items() if not k.startswith("_")}


def load_prices():
    d = json.load(open(STOCKS))["tickers"]
    rows = d.values() if isinstance(d, dict) else d
    return {r["ticker"]: r for r in rows}


def multiples_now(ticker, prices):
    """`value0`을 현재 종가로 환산한 배수. 못 구하면 그 배수는 빠진다."""
    path = os.path.join(VBASE, f"{ticker}.json")
    if not os.path.exists(path):
        return {}, None
    base = json.load(open(path))
    p0 = float(base["p0"])
    row = prices.get(ticker) or {}
    close = (row.get("price") or {}).get("close")
    if not close or p0 <= 0:
        return {}, base.get("cardAsOf")
    out = {}
    for m in base.get("metrics", []):
        if m.get("value0") is None or m.get("frozen"):
            continue
        v0 = float(m["value0"])
        if v0 <= 0:
            continue
        if m.get("method") == "ev-delta":
            ev0, mcap0 = float(m["ev0"]), float(m["mcap0"])
            ev = ev0 + (mcap0 * close / p0 - mcap0)
            out[m["metric"]] = ev / (ev0 / v0)       # EBITDA = ev0 / v0
        else:
            out[m["metric"]] = v0 * close / p0
    return out, base.get("cardAsOf")


SELF_KEYS = {"PER": "per", "PBR": "pbr", "PSR": "psr",
             "PCR": "pcr", "EV/EBITDA": "evebitda"}


def self_multiples(path):
    """본인 배수는 카드가 화면에 쓰는 값과 같아야 한다.

    동종업 값은 각 카드의 `valuation_base`에서 오는데, NVDA의 경우 그 기준선이
    **희석 가중평균 주식수**(24.285B)로 만들어져 있고 v2의 내재가치·백분위는
    **발행주식수**(24.100B, SEC dei)를 쓴다. 0.7% 차이지만 PBR이 24.1x와
    24.3x로, PCR이 43.4x와 43.8x로 갈린다. 카드가 한 화면에서 같은 배수를 두
    값으로 보여주는 것보다, 본인만 카드와 같은 기준으로 세는 편이 낫다고 봤다.
    동종업 기준과 0.7% 어긋나지만 순위는 한 칸 안에서 움직인다(실측).
    """
    d = json.load(open(path))["multiples"]
    # 오늘 분모가 0 이하(currentNote "negative")면 값 대신 NEGATIVE — 동종업 꼴찌로 센다.
    # 분모를 못 구한 날("missing")은 넣지 않아 그 배수가 빠진다.
    return {SELF_KEYS[k]: (v["current"] if v.get("current") is not None else NEGATIVE)
            for k, v in d.items() if k in SELF_KEYS
            and (v.get("current") is not None or v.get("currentNote") == "negative")}


NEGATIVE = "negative"


def peer_score(ticker, sectors, prices, self_path=None):
    sector = sectors.get(ticker)
    if not sector:
        sys.exit(f"{ticker}: v2/sectors.json에 섹터가 없다")
    # 표본이 작은 섹터는 가까운 큰 섹터를 빌려 온다(2026-09-24 사용자 결정, GOOGL).
    # GICS가 2018년 GOOGL·META를 IT에서 Communication Services로 옮겼고 이 유니버스에서는
    # 그 섹터가 6종목뿐이라 순위가 서지 않는다. 한 방향이다 — IT 종목의 동종업은 IT만 쓴다.
    borrowed = SECTOR_BORROW.get(sector, [])
    group = [t for t in sectors if sectors[t] == sector or sectors[t] in borrowed]
    data, asof = {}, {}
    for t in group:
        data[t], asof[t] = multiples_now(t, prices)
    core = False
    if self_path and os.path.exists(self_path):
        data[ticker] = {**data.get(ticker, {}), **self_multiples(self_path)}
        # 오늘 분모를 못 구한 배수("missing")는 valuation_base 쪽 값도 지워 순위에서 뺀다(Codex 2차).
        for k, v in json.load(open(self_path))["multiples"].items():
            if k in SELF_KEYS and v.get("currentNote") == "missing":
                data[ticker].pop(SELF_KEYS[k], None)
        core = json.load(open(self_path)).get("perBasis") == "core"
    rows, dropped = [], []
    for m in METRICS:
        # 본인 PER이 본업 기준이면 공시 EPS 기준인 동종업 PER과 잣대가 다르다. 동종업 전체를
        # 본업 기준으로 다시 계산하기 전까지는 PER을 동종업 점수에서 뺀다(Codex 지적, 2026-09-24).
        if m == "per" and core:
            dropped.append((m, "본인 PER은 본업 기준, 동종업은 공시 EPS 기준이라 비교에서 뺌"))
            continue
        vals = {t: v[m] for t, v in data.items() if m in v}
        if ticker not in vals:
            dropped.append((m, "본인 값 없음"))
            continue
        if len(vals) - 1 < MIN_PEERS:
            dropped.append((m, f"동종업 {len(vals)-1}개뿐"))
            continue
        mine = vals[ticker]
        peers = sorted(v for t, v in vals.items() if t != ticker)
        cheaper = len(peers) if mine == NEGATIVE else sum(1 for x in peers if x < mine)
        score = 100 - cheaper / len(peers) * 100
        rows.append({"metric": m, "value": mine, "rank": cheaper + 1,
                     "peers": len(peers), "median": statistics.median(peers),
                     "score": round(score, 1)})
    dates = [d for t, d in asof.items() if d and data.get(t)]
    if borrowed:
        sector = sector + " + " + " + ".join(borrowed)
    return {"ticker": ticker, "sector": sector, "groupSize": len(group),
            "metrics": rows, "dropped": dropped,
            "score": round(sum(r["score"] for r in rows) / len(rows), 1) if rows else None,
            "peerAsOf": [min(dates), max(dates)] if dates else None}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--json", help="결과 저장 경로")
    ap.add_argument("--self", dest="self_path",
                    help="자기 이력 점수를 읽을 build_multiple_history 결과 JSON")
    ap.add_argument("--card", action="store_true",
                    help="v2/<T>_full_widget.html의 VALUATION 블록을 교체한다 (--self 필요)")
    args = ap.parse_args()
    t = args.ticker.upper()

    r = peer_score(t, load_sectors(), load_prices(), args.self_path)
    print(f"{t} — {r['sector']} {r['groupSize']}종목 (본인 포함)")
    if r["peerAsOf"]:
        print(f"  동종업 기준일 {r['peerAsOf'][0]} ~ {r['peerAsOf'][1]}")
    print()
    print(f"  {'배수':10} {'본인':>8} {'동종업중앙':>10} {'순위':>10} {'점수':>7}")
    for row in r["metrics"]:
        vtxt = "적자" if row["value"] == NEGATIVE else f"{row['value']:.1f}"
        print(f"  {LABELS[row['metric']]:10} {vtxt:>8} {row['median']:10.1f}"
              f" {row['rank']:4d}/{row['peers']:<5} {row['score']:7.1f}")
    for m, why in r["dropped"]:
        print(f"  {LABELS[m]:10} {'—':>8} {'버림':>10} {why:>16}")
    print(f"\n  동종업 대비 = {r['score']}")

    if args.self_path and os.path.exists(args.self_path):
        d = json.load(open(args.self_path))["multiples"]
        sc = [v["score"] for v in d.values() if v.get("score") is not None]
        s = round(sum(sc) / len(sc), 1) if sc else None
        r["selfScore"] = s
        r["selfWindow"] = json.load(open(args.self_path)).get("window")
        print(f"  자기 이력 대비 = {s if s is not None else '—'}  (창 {r['selfWindow'][0]} ~ {r['selfWindow'][1]})")
        if r["score"] is None:
            # 동종업이 MIN_PEERS보다 적은 섹터(GOOGL의 Communication Services 6종목 등)는
            # 동종업 점수가 없다. 카드 블록에는 None으로 싣고 카드가 "표본 부족"으로 보인다.
            print("\n  동종업 점수 없음 — 격차 계산 생략")
        else:
            gap = abs(s - r["score"]) if s is not None else 0
            print(f"\n  두 점수의 격차 {gap:.1f}점"
                  + (" — 평균으로 뭉개지 말 것" if gap >= 20 else ""))

    if args.json:
        json.dump(r, open(args.json, "w"), ensure_ascii=False, indent=1)
        print("\n저장:", args.json)
    if args.card:
        if "selfScore" not in r:
            sys.exit("--card는 --self와 함께 쓴다 (두 점수를 한 블록에 싣는다)")
        sd = json.load(open(args.self_path))
        write_card(t, r, sd["multiples"], sd.get("perBasis", "diluted"))


SELF_KEYS = {"PER": "per", "PBR": "pbr", "PSR": "psr", "PCR": "pcr", "EV/EBITDA": "evebitda"}
BEGIN, END = "/* VALUATION:BEGIN */", "/* VALUATION:END */"


def write_card(ticker, r, self_multiples, per_basis="diluted"):
    """밸류에이션 탭의 두 점수 상자가 읽는 블록. 요약 격자도 같은 값을 쓴다."""
    import re
    out = {
        "peer": {"score": r["score"], "sector": r["sector"], "asOf": r["peerAsOf"],
                 "metrics": [{"metric": m["metric"], "score": m["score"],
                              "rank": m["rank"], "peers": m["peers"]} for m in r["metrics"]]},
        # perBasis "core"면 PER이 본업 이익 기준이다(v2/core_earnings.json). 카드가 라벨을 바꾼다.
        "self": {"score": r["selfScore"], "window": r["selfWindow"], "perBasis": per_basis,
                 # 동종업 상자와 같은 순서(METRICS)로 — 원본 JSON은 PER·PSR·PBR 순이다
                 "metrics": sorted(
                     [{"metric": SELF_KEYS[k], "score": v["score"], "percentile": v["percentile"],
                       "current": v["current"], "min": v["min"], "median": v["median"],
                       "max": v["max"], "days": v["days"], "currentNote": v.get("currentNote")}
                      for k, v in self_multiples.items()
                      if v.get("score") is not None or v.get("currentNote") == "missing"],
                     key=lambda m: METRICS.index(m["metric"]))},
    }
    path = os.path.join(REPO, "v2", f"{ticker}_full_widget.html")
    html = open(path, encoding="utf-8").read()
    pat = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    if len(pat.findall(html)) != 1:
        sys.exit(f"{path}: VALUATION 마커가 정확히 한 쌍이 아니다")
    block = f"{BEGIN}\nconst {ticker}_VALUATION = {json.dumps(out, ensure_ascii=False)};\n{END}"
    open(path, "w", encoding="utf-8").write(pat.sub(lambda _: block, html))
    print("교체:", path)


if __name__ == "__main__":
    main()
