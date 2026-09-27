#!/usr/bin/env python3
"""SK하이닉스 원주(KRX 000660) 일봉 — SKHY 자기 이력 배수의 분포를 만든다(2026-09-27 사용자 결정).

SKHY ADR은 2026-07-10 상장이라 이력이 짧다. 사용자 결정: **현재 배수는 ADR 가격**(투자자가 실제 내는 값),
**5년 분포는 원주 가격**으로 만든다. 원주 종가(원)를 ADR 1주 상당 달러로 바꿔(÷10 ÷ 그날 환율) 넘기면,
build_multiple_history가 다시 그날 환율을 곱해 원화 재무로 나누므로 결국 원주 가격 ÷ 원주 재무가 된다.
그러면 ADR 프리미엄(2026-09 약 +43%)만큼 현재 값이 분포보다 비싸게 찍힌다 — 의도한 것이다.

가격은 Yahoo 000660.KS(종가, 배당 미조정). 거래량 0인 날은 버린다(KR 티커 규칙).

    python3 v2/adapters/skhy_krx.py   → v2/.sec_cache/skhy_krx_000660.json  [[날짜, 시, 고, 저, 종(원)], …]
"""
import datetime as D
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
OUT = os.path.join(V2, ".sec_cache", "skhy_krx_000660.json")


def fetch():
    raw = subprocess.run(["curl", "-s", "-A", "Mozilla/5.0",
                          "https://query1.finance.yahoo.com/v8/finance/chart/000660.KS?range=10y&interval=1d"],
                         capture_output=True, check=True).stdout
    r = json.loads(raw)["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    tz = D.timezone(D.timedelta(seconds=r["meta"].get("gmtoffset", 32400)))
    bars = []
    for i, ts in enumerate(r["timestamp"]):
        c, v = q["close"][i], q["volume"][i]
        if c is None or not v:
            continue
        day = D.datetime.fromtimestamp(ts, tz).date().isoformat()
        bars.append([day, q["open"][i], q["high"][i], q["low"][i], c])
    json.dump(bars, open(OUT, "w"))
    print(f"저장: {OUT} — {len(bars)}일 ({bars[0][0]} ~ {bars[-1][0]})")
    return bars


def load():
    return json.load(open(OUT))


if __name__ == "__main__":
    fetch()
