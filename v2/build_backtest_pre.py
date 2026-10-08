#!/usr/bin/env python3
"""밴드 백테스트 앞쪽 종가 보관 파일(v2/backtest_pre/{T}.json)을 만든다 — 2026-10-08 사용자 결정(차트 5년 전체를 덮는 백테스트).

카드 DAILY는 1,255봉(약 5년)만 들고 매일 앞에서 잘린다(pipeline/update_cards.py MAX_BARS·trim_front). 예상밴드는 체크포인트 직전 2년 PER로
만들므로 차트 첫 2년에는 체크포인트가 없었다. refresh_backtest.py가 이 파일에서 **DAILY 첫날 이전 봉만** 앞에 붙여 표본으로 쓴다
(차트·DAILY 자체는 바뀌지 않는다). 파일은 PRE_START부터 만든 날까지의 종가를 들고 있어 DAILY 첫날이 그날을 지나기 전(약 5년)까지 덮는다.

출처: 연구용 10년 일봉(research/.prices10y, Yahoo quote.close — 분할 반영·배당 미반영, 카드 DAILY와 같은 기준)이 있으면 그것,
없으면(ASML·TSM) 카드 갱신과 같은 Yahoo 차트(range=10y, quote.close, 미국 동부 날짜). 분할이 나면 카드는 멈추고 사람이 다시 만든다 —
그때 이 파일도 이 스크립트로 다시 만든다(refresh_backtest의 겹침 검사가 빠뜨림을 잡는다).

    python3 v2/build_backtest_pre.py            # 카드 전부(EPS 이력·밴드가 없는 카드는 건너뜀)
    python3 v2/build_backtest_pre.py NVDA MSFT
    python3 v2/build_backtest_pre.py --yahoo NVDA   # 연구 캐시 대신 Yahoo에서 새로 받는다(분할 뒤·만료 때 — 연구 캐시는 갱신되지 않는다)
"""
import glob
import hashlib
import json
import os
import sys
import urllib.parse
from datetime import date, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(HERE, "backtest_pre")
PRE_START = "2019-01-01"     # 차트 첫날(2021-10) 직전 체크포인트의 2년 표본까지 덮는다(Codex 2026-10-08)
RESEARCH = os.path.join(HERE, "research", ".prices10y")
RESEARCH_NAME = {"BRKB": "BRK.B"}
YAHOO_ONLY = {"ASML": "ASML", "TSM": "TSM"}
# 앞쪽 가격을 만들 수 없는 카드: SKHY는 2026-07 상장 ADR(그 전 가격은 한국 보통주 환산이 필요 — 이번 범위 밖), BRKB·SPCX는 EPS 이력이 없어 밴드가 없다.
SKIP = {"SKHY": "2026-07 상장 ADR — 앞쪽 가격 없음", "BRKB": "EPS 이력 없음", "SPCX": "EPS 이력 없음"}


def from_research(t):
    p = os.path.join(RESEARCH, f"{RESEARCH_NAME.get(t, t)}.json")
    if not os.path.exists(p):
        return None, None
    raw = open(p, "rb").read()
    rows = [[b["date"], b["c"]] for b in json.loads(raw)["daily"] if b["date"] >= PRE_START and b.get("c")]
    return rows, {"source": f"research/.prices10y/{os.path.basename(p)}", "source_sha256": hashlib.sha256(raw).hexdigest()}


def from_yahoo(sym):
    sys.path.insert(0, os.path.join(REPO, "pipeline"))
    import fetch_prices as fp   # update_cards와 같은 http·시간대
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym, safe='')}?range=10y&interval=1d&events=split"
    raw = fp.http_get(url)
    r = json.loads(raw)["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    rows = []
    for i, ts in enumerate(r.get("timestamp") or []):
        c = q["close"][i]
        if c is None:
            continue
        d = datetime.fromtimestamp(ts, fp.ET).date().isoformat()
        if d >= PRE_START and d < date.today().isoformat():
            rows.append([d, round(c, 4)])
    return rows, {"source": f"yahoo chart {sym} range=10y quote.close (ET)", "source_sha256": hashlib.sha256(raw if isinstance(raw, bytes) else raw.encode()).hexdigest()}


def main():
    yahoo = "--yahoo" in sys.argv
    want = [a.upper() for a in sys.argv[1:] if not a.startswith("--")] or sorted(os.path.basename(p).split("_full_widget")[0] for p in glob.glob(os.path.join(HERE, "*_full_widget.html")))
    os.makedirs(OUT, exist_ok=True)
    for t in want:
        if t in SKIP:
            print(t, "건너뜀:", SKIP[t]); continue
        if not os.path.exists(os.path.join(REPO, "scripts", f"{t}_eps_history.json")):
            print(t, "건너뜀: EPS 이력 없음"); continue
        if yahoo or t in YAHOO_ONLY:
            rows, meta = from_yahoo(YAHOO_ONLY.get(t, RESEARCH_NAME.get(t, t).replace(".", "-")))
        else:
            rows, meta = from_research(t)
        if not rows:
            print(t, "가격 없음 — 만들지 않음"); continue
        dates = [r[0] for r in rows]
        assert dates == sorted(set(dates)), f"{t}: 날짜 중복·역순"
        assert all(r[1] > 0 for r in rows), f"{t}: 0 이하 종가"
        doc = {"ticker": t, "built": date.today().isoformat(), "pre_start": PRE_START, "first": dates[0], "last": dates[-1],
               **meta, "closes": rows}
        json.dump(doc, open(os.path.join(OUT, f"{t}.json"), "w"), separators=(",", ":"))
        print(t, dates[0], "~", dates[-1], len(rows), meta["source"])


if __name__ == "__main__":
    main()
