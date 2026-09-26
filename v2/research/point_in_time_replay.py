#!/usr/bin/env python3
"""과거 시점 재현 — 그때 공시된 자료만으로 그때 내재가치 판정을 다시 낸다(research/two_stage_prereg.md ②).

가격은 Yahoo 일봉(분할 보정 종가, 배당 미보정 'close'). 카드 코드의 주식 수도 오늘 분할 기준으로
보정되므로 둘을 같은 기준으로 비교한다. 창은 그 시점 기준 약 5년(21분기).

    python3 v2/research/point_in_time_replay.py
"""
import contextlib
import datetime as dt
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build_dcf as d  # noqa: E402

CASES = [  # (종목, 날짜, 사건, 기대 조건)
    ("AAPL", "2016-03-31", "버크셔 첫 매수", "le0.9"),
    ("AAPL", "2024-06-28", "버크셔 대량 매도", "ge1.1"),
    ("META", "2022-11-03", "저점", "le0.9"),
    ("TSLA", "2021-11-04", "고점 부근", "gt1.5"),
    ("NVDA", "2022-10-14", "저점 부근(기록만)", None),
]
CONFIGS = [("지금", False, "fade"), ("시점수정", True, "fade"), ("A 2단계", True, "two_stage")]


def close_on(ticker, day):
    t0 = int(dt.datetime.fromisoformat(day).timestamp()) - 10 * 86400
    t1 = int(dt.datetime.fromisoformat(day).timestamp()) + 86400
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={t0}&period2={t1}&interval=1d"
    raw = subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", url], capture_output=True, text=True).stdout
    r = json.loads(raw)["chart"]["result"][0]
    rows = [(dt.date.fromtimestamp(ts).isoformat(), c) for ts, c in zip(r["timestamp"], r["indicators"]["quote"][0]["close"]) if c]
    rows = [x for x in rows if x[0] <= day]
    return rows[-1]


def ok(ratio, cond):
    if cond is None or ratio is None:
        return None
    op, v = cond[:2], float(cond[2:])
    return {"le": ratio <= v, "ge": ratio >= v, "gt": ratio > v}[op]


def main():
    out = []
    for t, day, what, cond in CASES:
        pday, px = close_on(t, day)
        ws = (dt.date.fromisoformat(day) - dt.timedelta(days=int(5.25 * 365.25))).isoformat()
        row = {"t": t, "day": day, "price_day": pday, "px": round(px, 2), "what": what, "cond": cond}
        for name, lead, path in CONFIGS:
            d.REINVEST_LEAD = lead
            with contextlib.redirect_stdout(io.StringIO()):
                b = d.base_inputs(t, day)
                h = d.history(t, day, window_start=ws)
                sc = d.scenarios(b, h, 0.10, 0.025, path=path) if h else None
            base = sc[1]["per_share"] if sc else None
            ratio = px / base if base and base > 0 else None
            row[name] = {"base": round(base, 2) if base else None, "ratio": round(ratio, 2) if ratio else None,
                         "hit": ok(ratio, cond), "g5": round(h["growth_5y"], 3) if h else None,
                         "margin": round(h["margin_now"], 3) if h else None}
        out.append(row)
        print(t, day, what, f"${px:.2f}", {k: (row[k]["base"], row[k]["ratio"], row[k]["hit"]) for k, _, _ in CONFIGS})
    d.REINVEST_LEAD = False
    json.dump(out, open(os.path.join(HERE, "point_in_time_replay_result.json"), "w"), ensure_ascii=False, indent=1)
    for k, _, _ in CONFIGS:
        hits = [r[k]["hit"] for r in out if r[k]["hit"] is not None]
        print(f"{k}: 적중 {sum(hits)}/{len(hits)}")


if __name__ == "__main__":
    main()
