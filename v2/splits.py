"""주식분할 목록 — 주식 수를 오늘 기준으로 맞추는 데 쓴다(build_multiple_history.instant_series).

2026-09-25 발견(Fable, S&P500 검증): 가격은 분할 조정돼 있는데 주식 수는 손으로 적은
`fetch_eps_history.KNOWN_SPLITS`에 있는 종목만 보정했다. 목록에 없는 종목(BKNG 25:1 · KLAC 10:1 ·
CRWD 4:1 · APH 2:1 …)은 분할 전 공시의 주식 수가 작게 잡혀 주당 가치가 부풀고 PBR·PSR·EV가
낮게 나왔다(BKNG 현재가 ÷ 내재가치 0.03 → 분할 반영 0.8). 카드 70장 중 32장이 목록에 없었다.

순서
----
1. `KNOWN_SPLITS`에 있으면 그것(손으로 확인한 목록)이 우선한다.
2. 없으면 Yahoo `events=split`(10년)을 받아 캐시(`v2/.sec_cache/splits_{T}.json`, 7일)한다.
   Yahoo는 분사(스핀오프) 조정도 "분할"로 싣는다(GE 1.281·1.253, IBM 1.046). 주식 수를 바꾸지
   않는 이벤트라 **비율 1.45 이상 또는 0.7 이하만** 분할로 받고 나머지는 `ignored`에 남긴다.
3. `OVERRIDE`에 넣으면(검증 스크립트가 오프라인 데이터로 채운다) 그것을 쓴다.
"""
import json
import os
import subprocess
from datetime import date, datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, ".sec_cache")
OVERRIDE = {}
YAHOO_SYMBOL = {"BRKB": "BRK-B"}
MIN_UP, MAX_DOWN = 1.45, 0.70


def clean(raw):
    """[(날짜, 비율)] 중 분할로 볼 것과 버릴 것을 가른다."""
    keep, ignored = [], []
    for d, r in raw:
        (keep if (r >= MIN_UP or r <= MAX_DOWN) else ignored).append((d, r))
    return sorted(keep), sorted(ignored)


def _fetch_yahoo(ticker):
    sym = YAHOO_SYMBOL.get(ticker, ticker)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=10y&interval=1mo&events=split"
    r = subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", url], capture_output=True, timeout=30)
    data = json.loads(r.stdout)
    res = (data.get("chart", {}).get("result") or [{}])[0]
    ev = (res.get("events") or {}).get("splits") or {}
    raw = []
    for k, s in ev.items():
        day = datetime.fromtimestamp(int(s.get("date", k)), timezone.utc).date().isoformat()
        num, den = float(s.get("numerator") or 0), float(s.get("denominator") or 0)
        if num > 0 and den > 0:
            raw.append((day, num / den))
    return raw


def for_ticker(ticker):
    """분할 목록 [(적용일, 비율)]. 비율 > 1은 정분할(주식 수 증가), < 1은 병합."""
    if ticker in OVERRIDE:
        return clean(OVERRIDE[ticker])[0]
    import fetch_eps_history as feh   # scripts/ 가 sys.path에 있어야 한다(build_multiple_history가 넣는다)
    if ticker in feh.KNOWN_SPLITS:
        return list(feh.KNOWN_SPLITS[ticker])
    path = os.path.join(CACHE, f"splits_{ticker}.json")
    if os.path.exists(path):
        c = json.load(open(path))
        if (date.today() - date.fromisoformat(c["fetched"])).days <= 7:
            return [tuple(x) for x in c["splits"]]
    try:
        raw = _fetch_yahoo(ticker)
    except Exception:
        return []
    keep, ignored = clean(raw)
    os.makedirs(CACHE, exist_ok=True)
    json.dump({"fetched": date.today().isoformat(), "splits": keep, "ignored": ignored}, open(path, "w"))
    return keep
