"""재무제표 통화가 달러가 아닌 종목의 환율 — 가격(달러)과 재무(현지 통화)가 만나는 곳에서만 쓴다.

TSM(2026-09-25 사용자 결정): 어댑터(v2/adapters/tsm_ifrs.py)가 재무를 **대만달러 그대로** 둔다.
분기 평균 환율로 미리 달러 환산하면 가격(매일 환율)과 이익(분기마다 다른 환율)이 섞여, 대만달러가
급변한 구간(2025-06 등)에 PER은 위로·PBR은 아래로 최대 10% 밀렸다(Fable). 그래서 배수는
**ADR 가격 × 그날 환율**(대만달러)을 대만달러 재무로 나누고, 주당 가치는 계산 뒤 그날 환율로 달러로 되돌린다.
남는 차이는 ADR 프리미엄(ADR이 본주보다 비싸게 거래되는 몫)뿐이다.

companyfacts 모양을 맞추려고 어댑터 파일의 단위 키는 "USD"지만 **값은 대만달러**다.

    rate("TSM", "2026-09-23") → 그날(없으면 직전 영업일) 1달러당 대만달러
    rate("AAPL", …) → 1.0
"""
import bisect
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CURRENCY = {"TSM": "TWD"}
SERIES = {"TWD": os.path.join(HERE, ".sec_cache", "fx_DEXTAUS.csv")}   # 연준 H.10 (FRED DEXTAUS)
_cache = {}


def _load(cur):
    if cur not in _cache:
        rows = []
        for r in csv.DictReader(open(SERIES[cur])):
            v = r.get("DEXTAUS")
            if v and v != ".":
                rows.append((r["observation_date"], float(v)))
        rows.sort()
        _cache[cur] = ([d for d, _ in rows], [v for _, v in rows])
    return _cache[cur]


def rate(ticker, day):
    """현지 통화 / 1달러. 달러 재무 종목은 1.0."""
    cur = CURRENCY.get(ticker)
    if not cur:
        return 1.0
    ds, vs = _load(cur)
    i = bisect.bisect_right(ds, day) - 1
    if i < 0:
        raise ValueError(f"{ticker}: {day} 이전 환율 없음")
    return vs[i]


def is_local(ticker):
    return ticker in CURRENCY
