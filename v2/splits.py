"""주식분할 목록 — 주식 수를 오늘 기준으로 맞추는 데 쓴다(build_multiple_history.instant_series).

2026-09-25 발견(Fable, S&P500 검증): 가격은 분할 조정돼 있는데 주식 수는 손으로 적은
`fetch_eps_history.KNOWN_SPLITS`에 있는 종목만 보정했다. 목록에 없는 종목(BKNG 25:1 · KLAC 10:1 ·
CRWD 4:1 · APH 2:1 …)은 분할 전 공시의 주식 수가 작게 잡혀 주당 가치가 부풀고 PBR·PSR·EV가
낮게 나왔다(BKNG 현재가 ÷ 내재가치 0.03 → 분할 반영 0.8). 카드 70장 중 32장이 목록에 없었다.

순서
----
1. `KNOWN_SPLITS`에 있으면 그것(손으로 확인한 목록)이 우선한다.
2. 없으면 폴리곤 분할 목록(`site_data/polygon_daily/_splits.json`, 미국 전 종목 2015년부터,
   `pipeline/polygon_bars.py`가 매일 가격 갱신에서 더한다)에서 읽는다. 2026-11-25부터 — 가격이
   폴리곤 adjusted=true(분할 조정)로 바뀌어서 주식 수도 같은 목록으로 맞춘다. 그전에는 Yahoo
   `events=split`(10년)을 종목마다 받아 `v2/.sec_cache/splits_{T}.json`에 7일 캐시했다.
   목록에는 분사·주식 배당 조정도 섞여 있다(Yahoo의 GE 1.281·IBM 1.046, 폴리곤의 1.05 같은 주식 배당).
   주식 수를 크게 바꾸지 않는 이벤트라 **비율 1.45 이상 또는 0.7 이하만** 분할로 받는다.
   목록이 7일 넘게 묵었고 키가 있으면 먼저 새로 받는다(그때 `_splits.json`이 바뀐다 — 로컬 실행이면
   그 파일도 변경으로 남는다). 목록이 없거나 그 새로 받기가 실패하면 예외 — 예전처럼 조용히 빈
   목록을 주면 분할 종목의 주식 수가 틀린 채로 배수가 나온다. 매일 가격 갱신이 목록을 커밋하므로
   v2 카드 워크플로(키 없음)는 받지 않고 읽기만 한다.
   주의: SNDK(2026-11-20 8:1)는 `KNOWN_SPLITS`에 "분할 없음"으로 적혀 있어 1번이 이 목록을 이긴다.
3. `OVERRIDE`에 넣으면(검증 스크립트가 오프라인 데이터로 채운다) 그것을 쓴다.
"""
import os
import sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "pipeline"))
import polygon_bars as pg  # noqa: E402
OVERRIDE = {}
YAHOO_SYMBOL = {"BRKB": "BRK-B"}
MIN_UP, MAX_DOWN = 1.45, 0.70


def clean(raw):
    """[(날짜, 비율)] 중 분할로 볼 것과 버릴 것을 가른다."""
    keep, ignored = [], []
    for d, r in raw:
        (keep if (r >= MIN_UP or r <= MAX_DOWN) else ignored).append((d, r))
    return sorted(keep), sorted(ignored)


def _polygon(ticker):
    """[(적용일, 비율)] 원자료 — 폴리곤 분할 목록에서."""
    sp = pg.load_splits()
    if not sp.get("checked"):
        raise RuntimeError("폴리곤 분할 목록이 없다 — python3 pipeline/polygon_bars.py splits-init")
    today = pg.datetime.now(pg.ET).date()   # the list's dates are ET dates
    if date.fromisoformat(sp["checked"]) < today - timedelta(days=7) and pg.api_key():
        pg.update_splits(today.isoformat())
    return pg.splits_for(pg.psym(YAHOO_SYMBOL.get(ticker, ticker)))


def for_ticker(ticker):
    """분할 목록 [(적용일, 비율)]. 비율 > 1은 정분할(주식 수 증가), < 1은 병합."""
    if ticker in OVERRIDE:
        return clean(OVERRIDE[ticker])[0]
    import fetch_eps_history as feh   # scripts/ 가 sys.path에 있어야 한다(build_multiple_history가 넣는다)
    if ticker in feh.KNOWN_SPLITS:
        return list(feh.KNOWN_SPLITS[ticker])
    return clean(_polygon(ticker))[0]
