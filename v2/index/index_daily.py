#!/usr/bin/env python3
"""지수 카드 틀(preview 전용, 2026-10-20) — 지금 게시하는 것은 --card SPY(SPY ETF 카드)뿐이다. S&P 500 지수 카드 페이지는
같은 날 지웠고(사용자 결정: 지수를 나타내는 카드는 거래소에서 거래되는 ETF 기준), 아래 SP500 설명은 시험용 프로필이다.

S&P 500 지수 카드 — 종목 카드와 같은 틀: 캔들 차트·기간별 수익률·월별 등락률·구성 종목·시계열 사건.

구성 종목 탭과 머리 PER·국채 칸은 지수 시세 계산과 따로다: SSGA SPY 펀드 페이지(업종 비중·PER), FRED DGS10, v2/etf/SPY.json
(상위 10개·카드 판정 비중)을 읽고, 못 읽거나 모양이 틀리면 그 칸만 비운다(카드는 보류하지 않는다).

자료: Yahoo ^GSPC 일봉 종가(홈 시장 지표 macro.json과 같은 출처). FRED SP500(S&P Dow Jones Indices 제공, 최근 10년)과
겹치는 날짜를 모두 대조한다 — 날짜 집합이 같아야 하고, 최근 250세션은 소수 둘째 자리까지 같아야 하며, 그 앞은 0.2% 안이어야 한다.
계산·표시는 FRED 대조 구간(첫 FRED 날짜부터)의 종가만 쓴다 — 그래서 "사상 최고"가 아니라 "그날 이후 최고"다(2026-10-20 dr r3,
사용자 결정). FRED는 하루 늦게 올라오므로 S 하루는 "대조 전"으로 적고 쓴다. 어긋나거나, FRED에 닿지 못하거나, FRED 값이 이상하거나,
FRED가 직전 세션까지 없으면 카드를 "보류"로 쓴다.

세션: 홈 카드 세션 P와 직전 세션(site_data/stocks.json priceSession, 종목들의 prevSession)까지의 종가만 쓴다. Yahoo 마지막 두
종가 날짜가 그 둘과 다르면 보류.
가격 지수라 배당은 빠진다. 사건은 가격으로만 감지하고 원인 설명을 붙이지 않는다.

    python3 v2/index/index_daily.py [--card SP500|SPY] [--out-root DIR] [--yahoo FILE] [--fred FILE] [--stocks FILE]

--card SPY(2026-10-20 사용자 결정): 같은 틀로 SPY ETF 카드를 만든다 — 시세는 Yahoo SPY 일봉(시장 가격, 배당 제외),
대조는 FRED 대신 운용사(State Street)가 공시하는 SPY NAV 이력(2003-12부터): 날짜가 빠짐없이 있고 종가가 NAV와 가까워야
한다(아래 NAV_TOL). 계산·표시는 NAV 대조 구간만 쓴다. 판정 탭은 v2/etf/SPY.json(etf_daily.py 산출물)을 읽어 그린다.
"""
import argparse
import csv
import html
import io
import json
import math
import os
import re
import sys
import time
import traceback
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ET = timezone(timedelta(hours=-5))   # 날짜만 쓴다 — Yahoo 일봉 timestamp(개장 시각)는 서머타임과 무관하게 같은 날짜
YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{sym}?period1=0&period2={end}&interval=1d"
NAVHIST = "https://www.ssga.com/library-content/products/fund-data/etfs/us/navhist-us-en-{t}.xlsx"
NAV_RECENT_TOL = 0.010   # 최근 250세션: 시장 종가가 NAV의 ±1.0% 안(2026-10-20 실측 최대 0.49%)
NAV_OLD_TOL = 0.020      # 그 앞: ±2.0% 안(2003-12~ 실측 최대 −1.61%, 2008-10-10 금융위기; 2016-10~ 최대 0.90%)
# 장이 쉰 날인데 NAV만 있는 날 — 이 목록만 허용한다(2026-10-20 실측 3일). 다른 날은 Yahoo가 거래일을 빠뜨린 것일 수 있어 불일치.
NAV_ONLY_OK = {"2012-10-29", "2012-10-30", "2014-04-18"}   # 허리케인 샌디 휴장 2일, 성금요일
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
FRED_API = ("https://api.stlouisfed.org/fred/series/observations?series_id={sid}&api_key={key}"
            "&file_type=json&observation_start={start}")
UA = "Mozilla/5.0 (stock-widgets-preview index card)"
RECENT_EXACT = 250       # 최근 250세션은 소수 둘째 자리까지 같아야
OLD_TOL = 0.002          # 그 앞은 0.2% 안
BIG_MOVE = 0.03          # 하루 ±3% 이상
DRAWDOWNS = (0.10, 0.20)
PERIODS = (("1개월", 1), ("6개월", 6), ("1년", 12), ("3년", 36), ("5년", 60))
YEARS_SHOWN = 10
REASON_TEXT = {"fetch_fail": "Yahoo 시세를 받지 못함", "date_mismatch": "종가 날짜가 홈 세션과 다름",
               "cross_check": "FRED(S&P DJI) 대조 불일치", "run_fail": "스크립트 실행 실패",
               "short": "시세 기간이 모자람", "no_session": "홈 세션을 읽지 못함", "ohlc": "시가·고가·저가 이상", "cross_unavailable": "FRED(S&P DJI) 대조 못 함"}


def use_profile(key):
    global PROF
    PROF = PROFILES[key]
    REASON_TEXT.update(cross_check=f'{PROF["ref"]} 대조 불일치', cross_unavailable=f'{PROF["ref"]} 대조 못 함')
EPS = 1e-9               # 경계(정확히 −10%·±3%)에서 부동소수점 오차로 사건을 놓치지 않게

# 카드마다 다른 것(시세 심볼·대조 출처·글자·산출물). main이 --card로 PROF를 고른다.
PROFILES = {
    "SP500": {"key": "SP500", "name": "S&P 500", "sym": "%5EGSPC", "symText": "^GSPC", "ref": "FRED(S&P DJI)",
              "json": "v2/index/SP500.json", "html": "preview-only-index-sp500.html",
              "title": "S&amp;P 500 지수", "badge": "S&amp;P 500", "kind": "지수 · 미국 대형주 500개 · 가격 지수(배당 제외)",
              "company": "S&amp;P 500 Index", "current": "S&amp;P 500 · 지수",
              "backnav": '<a class="back-bar-nav" href="preview-only-etf-spy.html">SPY 카드 ▶</a>',
              "chart": "지수 차트", "retTitle": "가격 지수(배당 제외)", "what": "지수 시세", "weightOf": "지수 비중",
              "closeNote": "가격 지수(배당 제외), FRED와 대조한 종가(마지막 날은 FRED 게시 전이면 대조 전)",
              "span": "FRED 대조 구간(최근 10년, 첫 날이 매일 하루씩 밀린다)",
              "lede": "S&amp;P 500은 미국 대형주 약 500개를 시가총액 비중으로 묶은 지수다. 업종 비중은 지수 기준, 상위 10개 회사와 카드 비중은 지수를 따라가는 SPY(State Street) 보유 기준이다.",
              "verdict": False},
    "SPY": {"key": "SPY", "name": "SPY", "sym": "SPY", "symText": "SPY", "ref": "운용사 NAV",
            "json": "v2/etf/SPY_card.json", "html": "preview-only-etf-spy.html",
            "title": "SPY ETF", "badge": "SPY", "kind": "ETF · S&amp;P 500을 따라감 · 시장 가격(배당 제외)",
            "company": "SPDR S&amp;P 500 ETF Trust", "current": "SPY · ETF", "backnav": "",
            "chart": "SPY 차트", "retTitle": "SPY 시장 가격(배당 제외)", "what": "ETF 시세", "weightOf": "SPY 비중",
            "closeNote": "SPY 시장 가격(배당 제외), 운용사 NAV와 대조한 종가(마지막 날은 NAV 게시 전이면 대조 전)",
            "span": "운용사 NAV 대조 구간(2003년 12월부터)",
            "lede": "SPY는 S&amp;P 500 지수를 따라가는 ETF다(State Street). 업종 비중은 운용사가 공개하는 지수 기준, 상위 10개 회사와 카드 비중은 SPY 보유 기준이다.",
            "verdict": True},
}
PROF = PROFILES["SP500"]


class Hold(Exception):
    def __init__(self, reason, detail=""):
        super().__init__(reason)
        self.reason, self.detail = reason, detail


def http_get(url, timeout=60, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8")
        except Exception as e:   # noqa: BLE001 — 재시도 뒤 호출자가 분류한다
            last = e
            time.sleep(2 * (i + 1))
    raise last


def parse_yahoo(text):
    """[(date iso, close)] 오래된 순. 빈 종가는 버린다. 같은 날짜가 두 번이면 뒤의 것."""
    body = json.loads(text).get("chart") or {}
    if not body.get("result"):
        raise ValueError("Yahoo: no chart result")
    r = body["result"][0]
    by = {}
    for ts, c in zip(r.get("timestamp") or [], r["indicators"]["quote"][0]["close"]):
        if c is None or not math.isfinite(c) or c <= 0:
            continue
        by[datetime.fromtimestamp(ts, ET).date().isoformat()] = float(c)
    return sorted(by.items())


def parse_ohlc(text):
    """{date: (시가, 고가, 저가)} — 캔들 차트용. 종가는 parse_yahoo 값(FRED 대조)을 쓴다. 빈 값은 버린다."""
    r = json.loads(text)["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    by = {}
    for ts, o, h, lo in zip(r.get("timestamp") or [], q.get("open") or [], q.get("high") or [], q.get("low") or []):
        if None in (o, h, lo):
            continue
        by[datetime.fromtimestamp(ts, ET).date().isoformat()] = (float(o), float(h), float(lo))
    return by



def parse_fred(text):
    t = text.lstrip()
    if t.startswith("{"):
        obs = json.loads(t).get("observations") or []
        pairs = [(o["date"], o.get("value")) for o in obs]
    else:
        pairs = [(r[0], r[1]) for r in list(csv.reader(io.StringIO(text)))[1:] if len(r) == 2]
    out = {}
    for k, v in pairs:
        if v in (None, "", "."):
            continue            # FRED가 휴장일에 비워 두는 칸
        x = float(v)
        if not math.isfinite(x) or x <= 0:
            raise ValueError(f"FRED {k}: 값이 이상함")   # → 대조 못 함 → 보류
        out[k] = x
    return out


def fetch_fred(sid="SP500"):
    key = os.environ.get("FRED_API_KEY", "").strip()
    if key:   # 키는 URL에만 쓰고 출력하지 않는다(예외 메시지도 버린다)
        start = (date.today() - timedelta(days=11 * 366)).isoformat()
        try:
            return http_get(FRED_API.format(sid=sid, key=urllib.parse.quote(key, safe=""), start=start))
        except Exception:   # noqa: BLE001 — 키가 틀리거나 API가 막히면 공개 CSV로
            pass
    return http_get(FRED_CSV.format(sid=sid))


def parse_navhist(body):
    """운용사 NAV 이력 xlsx → {날짜: NAV}. 표준 라이브러리 xlsx 읽기는 etf_daily.read_xlsx를 같이 쓴다."""
    sys.path.insert(0, str(ROOT / "v2" / "etf"))
    from etf_daily import read_xlsx   # noqa: E402
    out, head = {}, False
    for r in read_xlsx(body):
        if r and str(r[0]).strip() == "Date" and len(r) > 1 and str(r[1]).strip() == "NAV":
            head = True
            continue
        if not head or not r or not r[0]:
            continue
        if not re.fullmatch(r"\d{2}-[A-Z][a-z]{2}-\d{4}", str(r[0]).strip()):
            continue   # 표 아래 안내 문구 줄(운용사 이름 바뀜 안내 등)
        k = datetime.strptime(str(r[0]).strip(), "%d-%b-%Y").date().isoformat()
        x = float(r[1])
        if not math.isfinite(x) or x <= 0:
            raise ValueError(f"NAV {k}: 값이 이상함")
        out[k] = x
    if not head:
        raise ValueError("NAV 이력 머리 줄 없음")
    return out


def fetch_navhist(t="spy"):
    req = urllib.request.Request(NAVHIST.format(t=t), headers={"User-Agent": "Mozilla/5.0 (stock-widgets-preview ETF card)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
    if not body.startswith(b"PK"):
        raise ValueError("NAV 이력이 xlsx가 아니다")
    return body


def cross_check_nav(series, nav, S, prevP):
    """ETF 카드: 시장 종가(Yahoo)를 운용사 NAV 이력과 대조. 상태 ok | mismatch | unavailable — ok만 게시한다.
    NAV는 적어도 prevP까지 있어야 하고(S 하루는 게시 전이면 대조 전), NAV 구간의 거래일은 모두 NAV가 있어야 한다.
    장이 쉰 날 NAV만 있는 날은 NAV_ONLY_OK에 든 날만 둔다(그 밖은 Yahoo 거래일 누락으로 보고 불일치). 종가와 NAV 차이(괴리)는 최근 250세션 ±1.0%, 그 앞 ±2.0% 안."""
    if not nav:
        return "unavailable", "운용사 NAV 이력에 닿지 못함"
    ys = dict(series)
    f_days = sorted(k for k in nav if k <= S)
    if len(f_days) < RECENT_EXACT:
        return "unavailable", f"NAV 날짜가 {len(f_days)}개뿐"
    lo, hi = f_days[0], f_days[-1]
    if hi < prevP:
        return "unavailable", f"NAV가 {hi}까지만 있음 — 직전 세션 {prevP}까지 없다"
    lag = hi < S
    only_y = [k for k, _ in series if lo <= k <= hi and k not in nav]
    extra = [k for k in f_days if k not in ys]
    if only_y or set(extra) - NAV_ONLY_OK:
        odd = sorted(set(extra) - NAV_ONLY_OK)
        return "mismatch", (f"날짜 불일치: NAV 없는 거래일 {len(only_y)}일, 시세 없는 NAV 날 {len(odd)}일 (첫 날 {(only_y or odd)[0]})"
                            + (" — 실제 휴장일이면 NAV_ONLY_OK에 더한다" if odd and not only_y else ""))
    both = [k for k in f_days if k in ys]
    gaps = [(k, ys[k] / nav[k] - 1) for k in both]
    recent, old = gaps[-RECENT_EXACT:], gaps[:-RECENT_EXACT]
    bad = [k for k, g in recent if abs(g) > NAV_RECENT_TOL] + [k for k, g in old if abs(g) > NAV_OLD_TOL]
    if bad:
        return "mismatch", f"종가와 NAV 차이가 큰 날 {len(bad)}일 (첫 날 {min(bad)})"
    worst = max(gaps, key=lambda t: abs(t[1]))
    return "ok", (f"State Street SPY NAV 이력과 {len(both)}일({lo}~{hi}) 대조: 거래일마다 NAV 있음"
                  + (f"(장이 쉰 날 NAV만 {len(extra)}일)" if extra else "")
                  + f", 종가와 NAV 차이 최대 {worst[1] * 100:+.2f}%({worst[0]}), 최근 {RECENT_EXACT}세션 최대 "
                  + f"{max(abs(g) for _, g in recent) * 100:.2f}%"
                  + (f" · 마지막 {S} 종가는 NAV 게시 전이라 대조 전(Yahoo 값)" if lag else ""))


# ---------- 계산 ----------

def d(s):
    return date.fromisoformat(s)


def minus_months(day, k):
    y, m = divmod(day.year * 12 + day.month - 1 - k, 12)
    m += 1
    last = (date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)).day
    return date(y, m, min(day.day, last))


def close_on_or_before(series, day):
    """day 이하 마지막 (날짜, 종가). 없으면 None."""
    lo, hi, iso = 0, len(series), day.isoformat()
    while lo < hi:
        mid = (lo + hi) // 2
        if series[mid][0] <= iso:
            lo = mid + 1
        else:
            hi = mid
    return series[lo - 1] if lo else None


def cross_check(series, fred, S, prevP):
    """(상태, 설명). 상태: ok | mismatch | unavailable — ok만 게시한다.
    prevP = 홈 시세 파일이 적은 S 직전 세션(종목 131개의 prevSession). FRED는 적어도 prevP까지 있어야 하고, 그 구간의 날짜 집합이
    같아야 한다 — 그러면 대조 전인 값은 S 하루뿐이고, S 직전 날짜가 prevP인지는 compute가 따로 본다."""
    if not fred:
        return "unavailable", "FRED에 닿지 못함"
    ys = dict(series)
    f_days = sorted(k for k in fred if k <= S)
    if len(f_days) < RECENT_EXACT:
        return "unavailable", f"FRED 날짜가 {len(f_days)}개뿐"
    lo, hi = f_days[0], f_days[-1]
    if hi < prevP:
        return "unavailable", f"FRED가 {hi}까지만 있음 — 직전 세션 {prevP}까지 없다"
    lag = hi < S
    only_f = [k for k in f_days if k not in ys]
    only_y = [k for k, _ in series if lo <= k <= hi and k not in fred]
    if only_f or only_y:
        return "mismatch", f"날짜 불일치: Yahoo에 없는 날 {len(only_f)}일, FRED에 없는 날 {len(only_y)}일 (첫 날 {(only_f or only_y)[0]})"
    recent = f_days[-RECENT_EXACT:]
    bad_recent = [k for k in recent if abs(round(ys[k], 2) - fred[k]) > 0.0051]
    old_diffs = [(k, abs(ys[k] / fred[k] - 1)) for k in f_days[:-RECENT_EXACT]]
    bad_old = [k for k, r in old_diffs if r > OLD_TOL]
    small = sum(1 for k, r in old_diffs if abs(round(ys[k], 2) - fred[k]) > 0.0051)
    if bad_recent or bad_old:
        return "mismatch", f"최근 {RECENT_EXACT}세션 불일치 {len(bad_recent)}일, 그 앞 0.2% 초과 {len(bad_old)}일 (첫 날 {(bad_recent or bad_old)[0]})"
    worst = max((r for _, r in old_diffs), default=0.0)
    return "ok", (f"FRED SP500과 {len(f_days)}일({lo}~{hi}) 대조: 날짜 모두 같음, 최근 {RECENT_EXACT}세션 값 모두 같음, "
                  f"그 앞 {small}일이 소수 둘째 자리에서 다름(최대 {worst * 100:.2f}%)"
                  + (f" · 마지막 {S} 종가는 FRED 미게시로 대조 전(Yahoo 값)" if lag else ""))


def window_stats(series, base, S):
    """기준일(포함)~S 종가로: 기간 최고·최저 종가, 최대 낙폭(고점→저점), 상승일 비율, 연 환산 변동성(하루 등락률 표본 표준편차 × √252)."""
    w = [p for p in series if base <= p[0] <= S]
    hi, lo = max(w, key=lambda p: p[1]), min(w, key=lambda p: p[1])
    peak, mdd, mdd_peak, mdd_trough = w[0], 0.0, w[0][0], w[0][0]
    for k, c in w:
        if c > peak[1]:
            peak = (k, c)
        dd = c / peak[1] - 1
        if dd < mdd:
            mdd, mdd_peak, mdd_trough = dd, peak[0], k
    ch = [w[i][1] / w[i - 1][1] - 1 for i in range(1, len(w))]
    mean = sum(ch) / len(ch)
    vol = math.sqrt(sum((x - mean) ** 2 for x in ch) / (len(ch) - 1)) * math.sqrt(252) if len(ch) > 1 else None
    return {"hi": [hi[0], round(hi[1], 2)], "lo": [lo[0], round(lo[1], 2)],
            "mdd": {"ret": mdd, "peak": mdd_peak, "trough": mdd_trough},
            "upDays": sum(x > 0 for x in ch), "days": len(ch), "vol": vol}


def returns(series, S):
    sd, sc = d(S), series[-1][1]
    out = []
    for label, k in PERIODS:
        b = close_on_or_before(series, minus_months(sd, k))
        if b is None:
            raise Hold("short", f"{label} 기준 종가 없음")
        r = sc / b[1] - 1
        row = {"label": label, "months": k, "base": b[0], "baseClose": round(b[1], 2), "ret": r,
               "stats": window_stats(series, b[0], S)}
        if k >= 36:
            row["annual"] = (1 + r) ** (12 / k) - 1
        out.append(row)
    b = close_on_or_before(series, date(sd.year - 1, 12, 31))
    out.append({"label": "YTD", "months": None, "base": b[0], "baseClose": round(b[1], 2), "ret": sc / b[1] - 1,
                "stats": window_stats(series, b[0], S)})
    return out


def month_ends(series):
    """{(y, m): (마지막 날짜, 종가)}"""
    me = {}
    for k, c in series:
        me[(int(k[:4]), int(k[5:7]))] = (k, c)
    return me


def month_done(S):
    """S가 그 달 마지막 평일이면 끝난 달로 본다(월말 휴장일은 모른다 — 그날은 다음 세션 실행에서 풀린다)."""
    n = d(S) + timedelta(days=1)
    while n.weekday() >= 5:
        n += timedelta(days=1)
    return n.month != d(S).month


def monthly(series, S):
    me = month_ends(series)
    sy, sm = int(S[:4]), int(S[5:7])
    open_m = not month_done(S)
    years = list(range(sy - YEARS_SHOWN + 1, sy + 1))
    rows = []
    for y in years:
        cells = []
        for m in range(1, 13):
            prev = me.get((y - (m == 1), 12 if m == 1 else m - 1))
            cur = me.get((y, m))
            if (y, m) > (sy, sm) or not prev or not cur:
                cells.append(None)
                continue
            cells.append({"ret": cur[1] / prev[1] - 1, "partial": open_m and (y, m) == (sy, sm)})
        pe, ce = me.get((y - 1, 12)), (me.get((y, 12)) if y < sy else (S, series[-1][1]))
        annual = {"ret": ce[1] / pe[1] - 1, "partial": y == sy and (sm < 12 or open_m)} if pe and ce else None
        rows.append({"year": y, "months": cells, "annual": annual})
    stats = []
    for m in range(12):
        vals = [r["months"][m]["ret"] for r in rows if r["months"][m] and not r["months"][m]["partial"]]
        stats.append({"mean": sum(vals) / len(vals), "up": sum(v > 0 for v in vals), "n": len(vals)} if vals else None)
    last12 = []
    y, m = sy, sm
    for _ in range(12):
        prev, cur = me.get((y - (m == 1), 12 if m == 1 else m - 1)), me.get((y, m))
        ym = f"{y}-{m:02d}"
        days = [p for p in series if p[0][:7] == ym]
        ups = sum(1 for i, p in enumerate(series) if p[0][:7] == ym and i > 0 and p[1] > series[i - 1][1])
        hi, lo = max(days, key=lambda p: p[1]), min(days, key=lambda p: p[1])
        last12.append({"ym": ym, "ret": cur[1] / prev[1] - 1, "partial": open_m and (y, m) == (sy, sm),
                       "close": round(cur[1], 2), "chg": round(cur[1] - prev[1], 2), "hi": [hi[0], round(hi[1], 2)],
                       "lo": [lo[0], round(lo[1], 2)], "days": len(days), "upDays": ups, "same": stats[m - 1]})
        y, m = (y - 1, 12) if m == 1 else (y, m - 1)
    return {"rows": rows, "stats": stats, "last12": last12[::-1]}


def events(series, S):
    """가격 사건(최근 10년, series 첫 날 이후). 최고·고점은 series 안에서만 본다 — compute가 FRED 대조 구간만 넘긴다.
    회복은 −10% 이상 빠진 뒤 전고점 이상으로 돌아온 첫날."""
    start = minus_months(d(S), 12 * YEARS_SHOWN).isoformat()
    out, peak, peak_day, hit, trough = [], 0.0, None, set(), 0.0
    prev = None
    for k, c in series:
        show = k >= start
        ch = c / prev - 1 if prev is not None else 0.0
        if prev is not None and show and abs(ch) >= BIG_MOVE - EPS:
            out.append({"date": k, "close": round(c, 2), "chg": ch, "type": "up" if ch > 0 else "down",
                        "text": f"하루 {'상승' if ch > 0 else '하락'} {abs(ch) * 100:.2f}%"})
        if hit and c >= peak * (1 - EPS):
            if show:
                out.append({"date": k, "close": round(c, 2), "chg": ch, "type": "recover",
                            "text": f"전고점 회복 — 고점 {kdate(peak_day)}, 최대 낙폭 {pct(trough)}"})
            hit, trough = set(), 0.0
        if c > peak:
            if show and peak_day:
                out.append({"date": k, "close": round(c, 2), "chg": ch, "type": "ath", "text": f"{kdate(series[0][0])} 이후 최고 종가"})
            peak, peak_day, hit, trough = c, k, set(), 0.0
        else:
            dd = c / peak - 1
            trough = min(trough, dd)
            for t in DRAWDOWNS:
                if dd <= -t + EPS and t not in hit:
                    hit.add(t)
                    if show:
                        out.append({"date": k, "close": round(c, 2), "chg": ch, "type": "dd", "level": t,
                                    "text": f"고점 대비 −{int(t * 100)}% 진입 — 고점 {kdate(peak_day)}"})
        prev = c
    return out[::-1]


CHART_RANGES = (("1M", 1), ("6M", 6), ("1Y", 12), ("3Y", 36), ("5Y", 60))   # 종목 카드 차트 버튼과 같은 다섯 기간
MA_N = (5, 20, 60, 120)


def daily_block(series, ohlc, S):
    """캔들 차트 자료: 5년 기준일부터 [날짜, 시가, 고가, 저가, 종가], 이동평균(대조된 종가로 계산), 기간별 기준일.
    시가·고가·저가는 Yahoo 값뿐(FRED는 종가만 준다) — 모양이 말이 안 되면 보류한다."""
    sd = d(S)
    base = {key: close_on_or_before(series, minus_months(sd, k))[0] for key, k in CHART_RANGES}
    start = next(i for i, (k, _) in enumerate(series) if k == base["5Y"])
    rows, closes = [], [c for _, c in series]
    for k, c in series[start:]:
        if k not in ohlc:
            raise Hold("ohlc", f"{k} 시가·고가·저가 없음")
        o, h, lo = ohlc[k]
        if not all(math.isfinite(x) and x > 0 for x in (o, h, lo)) or lo > min(o, c) + 0.011 or h < max(o, c) - 0.011:
            raise Hold("ohlc", f"{k} 시가·고가·저가가 종가와 맞지 않음")
        rows.append([k, round(o, 2), round(h, 2), round(lo, 2), round(c, 2)])
    ma = {}
    for n in MA_N:
        vals = []
        for i in range(start, len(series)):
            vals.append(round(sum(closes[i - n + 1:i + 1]) / n, 2) if i >= n - 1 else None)
        ma[f"ma{n}"] = vals
    return {"rows": rows, "ma": ma, "base": base}


def compute(series, fred, P, prevP, ohlc):
    if not P or not prevP:
        raise Hold("no_session", "홈 시세 파일에서 세션을 읽지 못함")
    series = [p for p in series if p[0] <= P]
    if len(series) < 260 * 5:
        raise Hold("short", f"종가 {len(series)}개")
    S = series[-1][0]
    if S != P or series[-2][0] != prevP:
        raise Hold("date_mismatch", f"마지막 두 종가 {series[-2][0]}·{S}, 홈 세션 {prevP}·{P}")
    cc, cc_text = (cross_check_nav if PROF["key"] == "SPY" else cross_check)(series, fred, S, prevP)
    if cc != "ok":
        raise Hold("cross_check" if cc == "mismatch" else "cross_unavailable", cc_text)
    series = [p for p in series if p[0] >= min(fred)]   # 대조된 구간만(그 앞 Yahoo 값은 쓰지 않는다; fred = 대조 자료 — SPY는 NAV)
    close, prev = series[-1][1], series[-2][1]
    b1 = close_on_or_before(series, minus_months(d(S), 12))
    yr = [p for p in series if p[0] >= b1[0]]   # 1년 수익률·1년 그림과 같은 창(기준일 포함), 52주 아님
    hi = max(yr, key=lambda p: p[1])
    lo = min(yr, key=lambda p: p[1])
    ath = max(series, key=lambda p: p[1])
    return {"status": "ok", "S": S, "builtFor": P, "close": round(close, 2), "prevSession": series[-2][0],
            "chg": close / prev - 1, "hi1y": {"date": hi[0], "close": round(hi[1], 2), "from": close / hi[1] - 1},
            "lo1y": {"date": lo[0], "close": round(lo[1], 2), "from": close / lo[1] - 1},
            "rangeHigh": {"date": ath[0], "close": round(ath[1], 2), "from": close / ath[1] - 1}, "since": series[0][0],
            "returns": returns(series, S), "monthly": monthly(series, S), "events": events(series, S),
            "daily": daily_block(series, ohlc, S),
            "crossCheck": {"status": cc, "text": cc_text}}


# ---------- 화면 ----------
# 종목 카드(NVDA_full_widget.html)와 같은 틀: template/card_head.html(그 카드의 <head>) + template/index_card.html.

MINUS = "−"
CHART_HTML = """  <div class="section-title" id="techHeaderTitle">{{CHARTNAME}} — 일봉 캔들스틱 · 1년 수익률 <span id="techHeaderReturn"></span></div>
  <div class="price-chart-container">
    <div style="margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
      <div class="range-toggle" id="spxRangeToggle">
        <button class="range-btn" data-range="1M">1개월</button>
        <button class="range-btn" data-range="6M">6개월</button>
        <button class="range-btn active" data-range="1Y">1년</button>
        <button class="range-btn" data-range="3Y">3년</button>
        <button class="range-btn" data-range="5Y">5년</button>
      </div>
    </div>
    <svg id="spxCandleSvg" viewBox="0 0 720 240" width="100%" style="display:block;background:var(--bg3);border-radius:8px;padding:4px;" role="img" aria-label="{{BADGE}} 일봉 캔들스틱 차트"></svg>
    <div style="margin-top:10px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
      <div style="font-size:11px;color:var(--text3);" id="techRangeSummary"></div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
        <button class="ma-toggle-btn" data-ma="ma5" style="color:var(--ma5);border-color:var(--ma5);">● MA5</button>
        <button class="ma-toggle-btn" data-ma="ma20" style="color:var(--ma20);border-color:var(--ma20);">● MA20</button>
        <button class="ma-toggle-btn" data-ma="ma60" style="color:var(--ma60);border-color:var(--ma60);">● MA60</button>
        <button class="ma-toggle-btn" data-ma="ma120" style="color:var(--ma120);border-color:var(--ma120);">● MA120</button>
        <button class="ma-toggle-btn" data-ma="pricelabels" style="color:var(--text2);border-color:var(--text2);margin-left:4px;">◆ 가격라벨</button>
      </div>
    </div>
  </div>"""


def pct(x, dg=1, sign=True):
    if x is None:
        return "—"
    s = f"{abs(x) * 100:.{dg}f}%"
    return (("+" if x > 0 else MINUS if x < 0 else "") if sign else "") + s


def num(x):
    return f"{x:,.2f}"


def color(x):
    return "var(--green)" if x > 0 else "var(--red)" if x < 0 else "var(--text2)"


def kdate(s):
    return s.replace("-", ".")


def kday(s):
    y, m, dd = s.split("-")
    return f"{int(y)}년 {int(m)}월 {int(dd)}일"


def meta_item(label, value, col, title="", sub=""):
    t = f' title="{html.escape(title, quote=True)}"' if title else ""
    s2 = f'<span style="font-size:11px;color:var(--text3);margin-top:2px;">{sub}</span>' if sub else ""
    return (f'    <div class="meta-item"><span class="meta-label">{label}</span>'
            f'<span class="meta-value"{t} style="font-size:22px;color:{col};">{value}</span>{s2}</div>')


def bars_svg(items, label, W=720, H=220):
    """막대 그림(월별·연도별 공용). items: [(아래 글자, 값, 진행 중?)]"""
    pL, pR, top, mid = 8, 8, 26, 110
    mx = max(abs(v) for _, v, _ in items) or 0.01
    colW = (W - pL - pR) / len(items)
    g = [f'<line class="zero" x1="{pL}" x2="{W - pR}" y1="{mid}" y2="{mid}"/>']
    for i, (lab, r, partial) in enumerate(items):
        h = abs(r) / mx * (mid - top)
        cx = pL + (i + 0.5) * colW
        y = mid - h if r >= 0 else mid
        c = "up" if r >= 0 else "down"
        bw = min(colW * 0.6, 60)
        g.append(f'<rect class="bar-{c}{" partial" if partial else ""}" x="{cx - bw / 2:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(h, 0.8):.1f}" rx="3">'
                 f'<title>{lab} {pct(r, 2)}{" (진행 중)" if partial else ""}</title></rect>')
        ty = (y - 6) if r >= 0 else (y + h + 13)
        g.append(f'<text class="val {c}" x="{cx:.1f}" y="{ty:.1f}" text-anchor="middle">{pct(r)}</text>')
        g.append(f'<text class="mon" x="{cx:.1f}" y="{H - 6}" text-anchor="middle">{lab}</text>')
    return f'<svg class="m12" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">{"".join(g)}</svg>'


def fold(title, inner):
    """접었다 펴는 카드(처음엔 접힘) — 제목 줄을 누르면 펼친다."""
    return (f'  <details class="card fold"><summary class="card-title">{title}</summary>{inner}</details>')


def range_cards(res):
    """기간 중 최고·최저·최대 낙폭: 막대 = 그 기간의 시간 축(시작일~기준일). 최고·최저 종가 날짜에 동그라미,
    낙폭 구간(고점일→저점일)은 빨간 띠. 아래에 값·날짜(시안 1-C), 오른쪽 위 낙폭 칩."""
    out, end = [], d(res["S"])
    for r in res["returns"]:
        st, mdd = r["stats"], r["stats"]["mdd"]
        start = d(r["base"])
        span = (end - start).days or 1
        X = lambda iso: (d(iso) - start).days / span * 100
        x_hi, x_lo, x_pk, x_tr = X(st["hi"][0]), X(st["lo"][0]), X(mdd["peak"]), X(mdd["trough"])
        out.append(
            '<div class="rng-card">'
            f'<div class="rng-head"><b>{r["label"]}</b>' + (f'<span class="dd-chip">낙폭 {pct(mdd["ret"])}</span>' if mdd["ret"] < 0 else "") + '</div>'
            '<div class="rng-bar">'
            + (f'<span class="rng-dd" style="left:{x_pk:.1f}%;width:{max(x_tr - x_pk, 0.6):.1f}%" title="낙폭 {pct(mdd["ret"])} · {kdate(mdd["peak"])} → {kdate(mdd["trough"])}"></span>'
               if mdd["ret"] < 0 else "") +
            f'<span class="rng-pt lo" style="left:{x_lo:.1f}%" title="최저 {num(st["lo"][1])} · {kdate(st["lo"][0])}"></span>'
            f'<span class="rng-pt hi" style="left:{x_hi:.1f}%" title="최고 {num(st["hi"][1])} · {kdate(st["hi"][0])}"></span></div>'
            f'<div class="rng-axis"><span>{kdate(r["base"][2:])}</span><span>{kdate(res["S"][2:])}</span></div>'
            f'<div class="rng-ends"><span><i class="pt lo"></i>최저<br><b>{num(st["lo"][1])}</b><br>{kdate(st["lo"][0][2:])}</span>'
            f'<span class="r"><i class="pt hi"></i>최고<br><b>{num(st["hi"][1])}</b><br>{kdate(st["hi"][0][2:])}</span></div>'
            + (f'<div class="rng-foot">낙폭 {kdate(mdd["peak"][2:])} → {kdate(mdd["trough"][2:])}</div>' if mdd["ret"] < 0 else
               '<div class="rng-foot">이 기간에는 앞선 최고 종가 아래로 내려간 적이 없다</div>') + '</div>')
    legend = ('<div class="viz-legend"><span><i class="lg-pt hi"></i>최고 종가</span><span><i class="lg-pt lo"></i>최저 종가</span>'
              '<span><i class="lg-dd"></i>낙폭 구간(고점 → 저점)</span>'
              f'<span>막대 = 기간 시작(수익률 기준일) ~ {kdate(res["S"])}</span></div>')
    return (legend + f'<div class="rng-grid">{"".join(out)}</div>'
            '<div class="note">낙폭 = 기간 안에서 앞선 최고 종가에서 그 뒤 최저 종가까지 가장 크게 빠진 폭. 여기 최고·최저는 기준일 종가부터 센 '
            '종가라, 기준일 다음 날부터 장중 값으로 그리는 차트의 최고·최저와 다를 수 있다.</div>')


def month_dots(res):
    """달마다 자세히: 그 달(채운 점) vs 같은 달 평균(빈 고리) — 시안 2-B를 2-C처럼 열과 줄로 정리."""
    m12 = res["monthly"]["last12"]
    first_year = res["monthly"]["rows"][0]["year"]
    vals = [abs(x["ret"]) for x in m12] + [abs(x["same"]["mean"]) for x in m12 if x["same"]]
    scale = max(math.ceil(max(vals) * 100), 1) / 100        # 좌우 끝 = ±(가장 큰 값을 올린 정수 %)
    X = lambda v: 50 + v / scale * 50
    rows = []
    for x in reversed(m12):
        same, r = x["same"], x["ret"]
        c = "up" if r >= 0 else "down"
        plot = '<span class="md-zero"></span>'
        if same:
            a, b = sorted((X(r), X(same["mean"])))
            plot += (f'<span class="md-link" style="left:{a:.1f}%;width:{b - a:.1f}%"></span>'
                     f'<span class="md-ring" style="left:{X(same["mean"]):.1f}%"></span>')
        plot += f'<span class="md-dot {c}{" partial" if x["partial"] else ""}" style="left:{X(r):.1f}%"></span>'
        tag = ' <span class="sub">진행 중</span>' if x["partial"] else ""
        same_txt = f'{pct(same["mean"])} <span class="sub">· {same["up"]}/{same["n"]}</span>' if same else "—"
        rows.append(f'<div class="md-row"><span class="lbl">{kdate(x["ym"])}{tag}</span><span class="num-c">{num(x["close"])}</span>'
                    f'<span class="md-plot" title="{x["ym"]} {pct(r, 2)} · 같은 달 평균 {pct(same["mean"], 2) if same else "—"}">{plot}</span>'
                    f'<b class="num-c" style="color:{color(r)}">{pct(r)}</b><span class="num-c muted">{same_txt}</span></div>')
    s = f"{scale * 100:.0f}%"
    head = (f'<div class="md-row md-headrow"><span>달</span><span class="num-c">월말 종가</span>'
            f'<span class="md-axis"><span>{MINUS}{s}</span><span>0</span><span>+{s}</span></span>'
            f'<span class="num-c">등락률</span><span class="num-c">같은 달 평균 · 오른 해</span></div>')
    legend = ('<div class="viz-legend"><span><i class="lg-dot solid"></i>그 달 등락률</span>'
              f'<span><i class="lg-ring"></i>같은 달 평균({first_year}~)</span></div>')
    return (legend + f'<div class="wrap"><div class="md-grid">{head}{"".join(rows)}</div></div>'
            '<div class="note">점과 고리 사이 선이 길수록 그 달이 평소와 달랐다는 뜻이다. 같은 달 평균은 끝난 같은 달들의 평균, '
            '오른 해 / 센 해(진행 중인 달은 빼고 센다). 과거 평균은 앞날을 말해 주지 않는다.</div>')


def render_returns(res):
    cells = []
    for r in res["returns"]:
        sub = f'연 {pct(r["annual"])}' if "annual" in r else "&nbsp;"
        cells.append(f'<div class="op-cell"><span class="op-label">{r["label"]}</span>'
                     f'<span class="op-val" style="color:{color(r["ret"])}">{pct(r["ret"])}</span>'
                     f'<span class="op-sub">{sub}</span><span class="op-base">기준 {kdate(r["base"])} 종가</span></div>')
    years = [(str(x["year"]) + ("(YTD)" if x["annual"]["partial"] else ""), x["annual"]["ret"], x["annual"]["partial"])
             for x in res["monthly"]["rows"][-5:] if x["annual"]]
    return (
        f'  <div class="section-title">기간별 수익률 — {PROF["retTitle"]}</div>\n'
        f'  <div class="card"><div class="ret-strip">{"".join(cells)}</div></div>\n'
        f'{fold("기간 중 최고·최저 종가·최대 낙폭", range_cards(res))}\n'
        f'  <div class="card"><div class="card-title">연도별 수익률 — 최근 5년</div>{bars_svg(years, "연도별 수익률")}'
        '<div class="note">올해는 연초 대비(YTD), 흐린 막대.</div></div>')


def render_monthly(res):
    m12 = res["monthly"]["last12"]
    bars = bars_svg([(f'{x["ym"][2:4]}.{x["ym"][5:]}', x["ret"], x["partial"]) for x in m12], "최근 12개월 월별 등락률")
    ups = sum(x["ret"] > 0 for x in m12)
    best, worst = max(m12, key=lambda x: x["ret"]), min(m12, key=lambda x: x["ret"])
    partial = m12[-1]["partial"]
    line = (f'오른 달 {ups} / 12 · 가장 좋았던 달 {kdate(best["ym"])} <b style="color:{color(best["ret"])}">{pct(best["ret"])}</b> · '
            f'가장 나빴던 달 {kdate(worst["ym"])} <b style="color:{color(worst["ret"])}">{pct(worst["ret"])}</b>')
    return (
        '  <div class="section-title">월별 등락률 — 최근 12개월</div>\n'
        f'  <div class="card">{bars}<div class="m12-line">{line}</div>'
        + (f'<div class="note">흐린 막대는 진행 중인 달({kdate(res["S"])}까지).</div>' if partial else '') + '</div>\n'
        f'{fold("달마다 자세히", month_dots(res))}')


def timeline_items(res):
    since = kdate(res["since"])
    out, ath_by_year = [], {}
    for e in res["events"]:            # 새 날짜가 앞
        if e["type"] == "ath":
            ath_by_year.setdefault(e["date"][:4], []).append(e)
            continue
        chip_c = "up" if e["chg"] > 0 else "down" if e["chg"] < 0 else "flat"
        chip = f'<span class="tl-reaction {chip_c}">{pct(e["chg"])}</span>'
        if e["type"] in ("up", "down"):
            dot = "green" if e["type"] == "up" else "red"
            head = "하루 상승" if e["type"] == "up" else "하루 하락"
            title = f'종가 {num(e["close"])} · 전날 대비 {pct(e["chg"], 2)}'
        elif e["type"] == "dd":   # −20%(약세장)는 초대형 이벤트, −10%는 부정
            dot = "" if e.get("level", 0) >= 0.2 else "red"
            head, title = "고점 대비 낙폭", f'{e["text"]} · 종가 {num(e["close"])}'
        else:
            dot, head, title = "green", "전고점 회복", f'{e["text"]} · 종가 {num(e["close"])}'
        out.append((e["date"], f'      <div class="tl-item"><div class="tl-dot {dot}"></div>'
                                f'<div class="tl-date">{kday(e["date"])} — {head}{chip}</div>'
                                f'<div class="tl-title">{html.escape(title)}</div></div>'))
    for y, es in ath_by_year.items():  # 최고 종가 경신은 해마다 한 줄로 묶는다(많은 해는 50일 넘음)
        first, last = es[-1], es[0]
        out.append((last["date"], f'      <div class="tl-item"><div class="tl-dot neutral"></div>'
                                  f'<div class="tl-date">{y}년 — 최고 종가 경신 {len(es)}일</div>'
                                  f'<div class="tl-title">첫 경신 {kdate(first["date"])} {num(first["close"])} · '
                                  f'마지막 {kdate(last["date"])} {num(last["close"])}</div>'
                                  f'<div class="tl-desc">{since} 이후 종가 최고를 넘은 날</div></div>'))
    out.sort(key=lambda t: t[0], reverse=True)
    return "\n".join(t[1] for t in out)


def render_events(res):
    since = kdate(max(res["since"], minus_months(d(res["S"]), 12 * YEARS_SHOWN).isoformat()))
    legend = "".join(f'<span style="display:flex;align-items:center;gap:5px;"><span style="width:10px;height:10px;border-radius:50%;'
                     f'background:{c};display:inline-block;"></span>{t}</span>'
                     for c, t in (("var(--event-major)", "초대형 이벤트"), ("var(--green)", "긍정"),
                                  ("var(--red)", "부정"), ("var(--event-neutral)", "중립")))   # 종목 카드 시계열 뉴스와 같은 4색·같은 범례
    return (f'  <div class="section-title">시계열 사건 ({since} ~ {kdate(res["S"])})</div>\n'
            '  <div class="card"><div class="card-title">읽는 법</div>'
            '<div style="font-size:12.5px;color:var(--text2);line-height:1.6;">종가만 보고 자동으로 찾은 날이다. 원인 설명이나 기사는 붙이지 않는다. '
            f'낙폭·회복의 고점과 최고 종가는 {PROF["span"]} 안에서만 본다 — 그 앞 값은 쓰지 않는다. '
            '전고점 회복은 −10% 이상 빠진 뒤 전고점 이상으로 돌아온 첫날이다. 색은 종목 카드와 같은 4색이다 — '
            '초대형 이벤트: 고점 대비 −20% 진입(약세장) · 긍정: 하루 +3% 이상, 전고점 회복 · 부정: 하루 −3% 이하, 고점 대비 −10% 진입 · '
            '중립: 해마다 묶은 최고 종가 경신.</div></div>\n'
            f'  <div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:16px;font-size:11px;color:var(--text2);">{legend}</div>\n'
            f'  <div class="card">\n    <div class="timeline" id="newsTimeline">\n{timeline_items(res)}\n    </div>\n'
            '    <div class="tl-pager" id="newsPager"></div>\n  </div>')


# ---------- 구성 종목 ----------
# 업종 비중: SSGA SPY 펀드 페이지가 공개하는 "Index Sector Breakdown"(GICS 11개 합계). 상위 10개·카드 있는 종목: SPY 판정이
# 이미 공개하는 v2/etf/SPY.json(운용사 원본 파일은 공개하지 않는다 — v2/research/etf_verdict_prereg.md). 어느 쪽을 못 읽어도
# 그 칸만 "불러오지 못함"으로 쓰고 지수 카드는 보류하지 않는다(이 탭의 값은 지수 시세 계산에 쓰이지 않는다).

SSGA_PAGE = "https://www.ssga.com/us/en/intermediary/etfs/spdr-sp-500-etf-trust-spy"
SECTOR_KO = {"Information Technology": "정보기술", "Financials": "금융", "Communication Services": "커뮤니케이션 서비스",
             "Health Care": "헬스케어", "Consumer Discretionary": "경기소비재", "Industrials": "산업재",
             "Consumer Staples": "필수소비재", "Energy": "에너지", "Utilities": "유틸리티", "Real Estate": "부동산",
             "Materials": "소재"}
SECTOR_COLORS = ("#6551c9", "#2563eb", "#0e9f9e", "#d97706", "#db5a8a", "#64748b", "#a99bf0", "#92400e", "#7fb5f5", "#86dccd", "#cdd3dd")
BAR_TIERS = (("저평가", "#1f7a4d"), ("적정~저평가", "#5cae7f"), ("적정", "#c9c5b3"), ("적정~고평가", "#e6935a"),
             ("고평가", "#d92d20"), ("판정 보류", "#6b7280"), ("카드 없음", "#9aa3b5"), ("그 밖 제외", "#4b5563"),
             ("분류 안 됨", "#111827"))   # 홈 SPY 줄(preview-only-etf.css etf-seg)과 같은 색
VERDICT_ORDER = ("저평가", "적정~저평가", "적정", "적정~고평가", "고평가", "판정 보류")


def parse_sectors(text):
    """펀드 페이지의 <input id="index-sector-breakdown">. GICS 11개, 합 99.5~100.5%가 아니면 예외."""
    m = re.search(r'<input type="hidden" id="index-sector-breakdown" value="(\{.*?\})"\s*/>', text, re.S)
    if not m:
        raise ValueError("index-sector-breakdown 없음")
    v = json.loads(html.unescape(m.group(1)))
    rows = [(a["name"]["value"], float(a["weight"]["originalValue"])) for a in v["attrArray"]]
    if len(rows) != 11 or {n for n, _ in rows} != set(SECTOR_KO) or not all(0 <= w <= 100 for _, w in rows):
        raise ValueError("업종 칸 모양이 다름")
    if abs(sum(w for _, w in rows) - 100) > 0.5:
        raise ValueError("업종 합이 100%가 아님")
    asof = datetime.strptime(v["asOfDate"].replace("as of ", "").strip(), "%b %d %Y").date().isoformat()
    return {"asOf": asof, "rows": sorted(rows, key=lambda r: -r[1])}


def parse_chars(text):
    """펀드 페이지의 Index Characteristics에서 PER(Price/Earnings — 페이지에 정의가 없어 후행이라 단정하지 않는다)과 기준일만
    읽는다 — 긁어 오는 값을 최소로(2026-10-20). 이름표 바로 다음 칸이 숫자가 아니거나 3~100배 밖이면 예외."""
    toks = [t.strip() for t in re.sub(r"<[^>]+>", "\n", html.unescape(text)).split("\n") if t.strip()]
    i = toks.index("Index Characteristics")
    j = toks.index("Price/Earnings", i)
    if "Fund Characteristics" in toks[i:j]:
        raise ValueError("지수·펀드 구역이 섞임")   # 펀드 P/E를 지수 것으로 읽지 않는다
    pe = toks[j + 1]                       # 이름표 바로 다음 칸만 — 비어 있으면 다른 지표(FY1)를 대신 읽지 않는다
    if not re.fullmatch(r"\d+(\.\d+)?", pe):
        raise ValueError("Price/Earnings 값 없음")
    asof = next(t for t in toks[i:i + 3] if t.startswith("as of "))
    out = {"pe": float(pe), "peAsOf": datetime.strptime(asof[6:].strip(), "%b %d %Y").date().isoformat()}
    if not 3 < out["pe"] < 100:
        raise ValueError("PER 범위가 이상함")
    return out


def read_spy(path):
    """SPY 판정 공개 산출물에서 상위 10개·카드 있는 종목·판정별 비중. 없거나 모양이 틀리면 None(이 칸만 비운다).
    SPY가 보류(status≠ok)여도 보유 비중·카드 목록은 그 보유 파일 기준으로 보여 주되, 판정별 비중 막대는 뺀다."""
    try:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        top10, seen = [], set()
        for t in d["top10"]:
            w = t["weight"]
            if not (isinstance(t["company"], str) and isinstance(w, (int, float)) and 0 < w <= 1) or t["company"] in seen:
                raise ValueError("top10 모양")
            seen.add(t["company"])
            card = t.get("card") if isinstance(t.get("card"), str) and re.fullmatch(r"[A-Z0-9.]{1,10}", t["card"]) else None
            top10.append({"company": t["company"], "name": t.get("name") if isinstance(t.get("name"), str) else None,
                          "weight": w, "card": card,
                          "verdict": t.get("verdict") if t.get("verdict") in VERDICT_ORDER else None})
        cards = {}
        for c in d["cards"]:
            if (isinstance(c, dict) and isinstance(c.get("card"), str) and re.fullmatch(r"[A-Z0-9.]{1,10}", c["card"])
                    and c.get("verdict") in VERDICT_ORDER):
                cards[c["card"]] = c["verdict"]
        if not top10 or not cards:
            return None
        bar = d.get("bar") if isinstance(d.get("bar"), dict) else None
        if bar and not (set(bar) <= set(dict(BAR_TIERS)) and all(isinstance(v, (int, float)) and 0 <= v <= 1 for v in bar.values())
                        and abs(sum(bar.values()) - 1) < 1e-6):
            bar = None   # 모양이 틀리거나 모르는 칸이 있으면 막대만 뺀다
        held = d.get("status") != "ok"
        return {"S": d.get("S") if isinstance(d.get("S"), str) else None, "held": held,
                "reasonText": d.get("reasonText") if isinstance(d.get("reasonText"), str) else None,
                "bar": None if held else bar, "top10": top10, "cards": sorted(cards.items())}
    except Exception:   # noqa: BLE001
        return None


def verdict_color(v):
    return ("var(--green)" if v in ("저평가", "적정~저평가") else "var(--red)" if v in ("적정~고평가", "고평가")
            else "var(--text3)" if v == "판정 보류" else "var(--text2)")


def render_holdings(res):
    c = res.get("constituents") or {}
    sec, spy = c.get("sectors"), c.get("spy")
    parts = ['  <div class="section-title">구성 종목 — 무엇으로 이루어져 있나</div>\n'
             f'  <div class="lede">{PROF["lede"]}</div>']
    if sec:
        # 도넛(가운데 "11개 · 업종 · 날짜") + 오른쪽 색 막대 범례(가장 큰 업종을 끝으로). 색은 비중 순위로 정해 밝기가 서로 다르다.
        tot, stops, legend, mx = sum(w for _, w in sec["rows"]), [], [], sec["rows"][0][1]
        acc = 0.0
        for (n, w), c in zip(sec["rows"], SECTOR_COLORS):
            a0, acc = acc, acc + w / tot * 100
            stops.append(f"{c} {a0:.2f}% {acc:.2f}%")
            legend.append(f'<span class="sw" style="background:{c}"></span><span>{SECTOR_KO[n]}</span>'
                          f'<span class="sb"><i style="width:{w / mx * 100:.1f}%;background:{c}"></i></span><b>{w:.1f}%</b>')
        top3 = sum(w for _, w in sec["rows"][:3])
        parts.append(f'  <div class="card"><div class="pie-head"><div class="card-title">업종 비중 (GICS 11개)</div><span class="sub">상위 3개 업종 {top3:.1f}%</span></div>'
                     f'<div class="pie-wrap"><div class="pie" role="img" aria-label="업종 비중 도넛 그래프" style="background:conic-gradient({", ".join(stops)})">'
                     f'<div class="pie-hole"><b>{len(sec["rows"])}개</b><span>업종 · {kdate(sec["asOf"])}</span></div></div>'
                     f'<div class="pie-legend">{"".join(legend)}</div></div>'
                     f'<div class="note">State Street SPY 펀드 페이지의 지수 업종 비중, {kdate(sec["asOf"])} 기준. 막대는 가장 큰 업종을 끝으로 맞춘 길이.</div></div>')
    else:
        parts.append('  <div class="card"><div class="card-title">업종 비중</div><div class="note">운용사 페이지에서 업종 비중을 불러오지 못했다.</div></div>')
    if spy:
        mx = max(t["weight"] for t in spy["top10"])
        rows = []
        for i, t in enumerate(spy["top10"], 1):
            name = html.escape(t["name"] or t["company"])
            tick = (f'<a href="{html.escape(t["card"], quote=True)}_full_widget.html">{html.escape(t["company"])}</a>' if t.get("card")
                    else html.escape(t["company"]))
            ver = f'<span class="vchip" style="color:{verdict_color(t["verdict"])}">{t["verdict"]}</span>' if t.get("verdict") else ""
            rows.append(f'<div class="hb-row top"><span class="hb-lab"><span class="rank">{i}</span><b>{tick}</b> <span class="sub">{name}</span></span>'
                        f'<span class="hb-track"><i style="width:{t["weight"] / mx * 100:.1f}%"></i></span><b class="hb-val">{t["weight"] * 100:.1f}%</b>{ver}</div>')
        top_sum = sum(t["weight"] for t in spy["top10"])
        k = len(spy["top10"])
        parts.append(f'  <div class="card"><div class="card-title">상위 {k}개 회사</div>{"".join(rows)}'
                     f'<div class="note">{k}개 합계 {top_sum * 100:.1f}%' + (" (SPY 자료에 10개가 다 오지 않았다)" if k != 10 else "") + f'. SPY 보유 파일 {kdate(spy["S"] or "—")} 기준, 현금·권리 줄을 뺀 주식 비중(같은 회사의 여러 주식은 합침). '
                     '오른쪽 글자는 이 사이트 카드의 판정이다.</div></div>')
        colors = dict(BAR_TIERS)
        groups = []
        for v in VERDICT_ORDER:
            names = [k for k, vv in spy["cards"] if vv == v]
            if names:
                chips = "".join(f'<a class="tchip" href="{k}_full_widget.html"><i style="background:{colors[v]}"></i>{k}</a>' for k in names)
                groups.append(f'<div class="vg"><div class="vg-head"><i class="vdot" style="background:{colors[v]}"></i>{v} <span class="sub">{len(names)}개</span></div>'
                              f'<div class="vg-chips">{chips}</div></div>')
        chips_html = ("".join(groups) + '<div class="note">누르면 그 종목 카드로 간다. 판정은 각 카드의 판정(참고용·매수 기준 아님).</div>')
        bar = spy.get("bar")
        if bar:
            covered = 1 - sum(bar.get(k, 0) for k in ("카드 없음", "분류 안 됨"))   # 판정 보류·그 밖 제외도 카드가 있는 회사
            segs = "".join(f'<span style="width:{bar[k] * 100:.2f}%;background:{c}" title="{k} {bar[k] * 100:.1f}%"></span>'
                           for k, c in BAR_TIERS if bar.get(k))
            labs = "".join(f'<span><i style="background:{c}"></i>{k} <b>{bar[k] * 100:.1f}%</b></span>' for k, c in BAR_TIERS if bar.get(k))
            head = (f'<div class="card-title">이 사이트에 카드가 있는 종목 {len(spy["cards"])}개 · {PROF["weightOf"]}의 {covered * 100:.1f}%</div>'
                    f'<div class="vbar" role="img" aria-label="판정별 {PROF["weightOf"]}">{segs}</div><div class="vbar-lab">{labs}</div>'
                    f'<div class="note">막대 = SPY 주식 비중을 그 회사 카드의 판정으로 나눈 것. 제목의 비중은 판정 보류·그 밖 제외 카드까지 포함한다 '
                    '(SPY 판정 카드의 "덮은 비중"은 판정이 있는 카드만). 카드 없는 회사는 대부분 작은 회사들이다.</div>')
        else:
            why = (f' SPY 판정 보류' + (f'({html.escape(spy["reasonText"])})' if spy.get("reasonText") else "")
                   + '라 판정별 비중 막대는 뺐다.') if spy.get("held") else ""
            head = (f'<div class="card-title">이 사이트에 카드가 있는 종목 {len(spy["cards"])}개</div>'
                    + (f'<div class="note">{why.strip()}</div>' if why else ""))
        parts.append(f'  <div class="card">{head}<details class="fold-in"><summary>종목 보기</summary>{chips_html}</details></div>')
    else:
        parts.append('  <div class="card"><div class="card-title">상위 10개 회사</div><div class="note">SPY 보유 자료를 불러오지 못했다.</div></div>')
    return "\n".join(parts)


def safe_holdings(res):
    """구성 종목 탭은 지수 시세와 따로다 — 그리다 실패해도 이 탭만 비우고 카드는 그대로 낸다."""
    try:
        return render_holdings(res)
    except Exception:   # noqa: BLE001
        traceback.print_exc()
        return ('  <div class="section-title">구성 종목</div>\n'
                '  <div class="card"><div class="note">구성 종목 자료를 그리지 못했다.</div></div>')


def render_verdict(full, P):
    """SPY 카드의 "카드 판정" 탭 — v2/etf/SPY.json(etf_daily.py)을 그대로 옮긴다. 규칙: v2/research/etf_verdict_prereg.md.
    홈 줄과 같은 묵음 규칙: 판정 세션(builtFor)이 홈 세션 P와 다르면 판정을 지우고 사유만(운용사 파일 갱신 대기는 예외)."""
    head = '  <div class="section-title">카드 판정 — 이 사이트 카드로 본 SPY</div>\n'
    lede = ('  <div class="lede">SPY가 담은 종목 중 이 사이트에 카드가 있는 종목의 판정을 보유 비중으로 평균한 것이다. '
            'SPY나 지수 자체의 내재가치 평가가 아니다. 참고용 · 매수 기준 아님 · 예측 신호로 검증되지 않음.</div>\n')
    def box(title, text):
        return head + lede + f'  <div class="card held-box"><div class="card-title">{title}</div><div class="note">{text}</div></div>'
    try:
        if full is None:
            return box("판정 보류", "판정 자료를 불러오지 못했다.")
        # 홈 줄(preview-only-etf.js valid() → 묵음 → 보류)과 같은 순서·같은 검사 — 같은 자료가 두 화면에서 다른 사유를 내지 않게
        fin = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
        tiers = [k for k, _ in BAR_TIERS]
        bad = not isinstance(full, dict) or full.get("status") not in ("ok", "held")
        if not bad and full["status"] == "held":
            bad = not isinstance(full.get("reasonText"), str)
        elif not bad:
            v, nbar, cov, rng, bar = full.get("verdict"), full.get("nbar"), full.get("coverage"), full.get("range"), full.get("bar")
            pdv = full.get("pending")
            bad = (v not in VERDICT_ORDER[:5] or not fin(nbar) or not (-4 <= nbar <= 3) or not fin(cov) or not (0.7 <= cov <= 1)
                   or not isinstance(bar, dict) or not all(fin(bar.get(k)) and 0 <= bar[k] <= 1 for k in tiers)
                   or abs(sum(bar[k] for k in tiers) - 1) > 1e-6 or abs(sum(bar[k] for k in tiers[:5]) - cov) > 1e-6
                   or not isinstance(full.get("S"), str)
                   or (pdv is not None and not (isinstance(pdv, dict) and pdv.get("kind") in ("issuer_lag", "home_lag") and isinstance(pdv.get("P"), str))))
        if bad:
            return box("판정 보류", "판정 자료 형식 오류.")
        pd = full.get("pending") if full.get("status") == "ok" and isinstance(full.get("pending"), dict) else None
        lag_issuer = bool(pd and pd.get("kind") == "issuer_lag" and pd.get("P") == P)
        lag_home = bool(pd and pd.get("kind") == "home_lag" and full.get("builtFor") == P)
        if not full.get("builtFor") or (full["builtFor"] != P and not lag_issuer):
            return box("판정 보류", f'묵음 — 판정 세션 {html.escape(kdate(full.get("builtFor") or "—"))}이 홈 세션 {html.escape(kdate(P or "—"))}과 다르다.')
        if full["status"] != "ok":
            return box("판정 보류", html.escape(full.get("reasonText") or "사유 미상") + (f' · {html.escape(full["detail"])}' if full.get("detail") else ""))
        if not (isinstance(rng, list) and len(rng) == 2 and all(fin(x) for x in rng)):
            rng = None   # 범위 칸만 비운다(홈 줄은 범위를 쓰지 않는다)
        tag = ("운용사 파일 갱신 대기 · 판정 기준 " + kdate(full["builtFor"]) if lag_issuer else "홈 가격 세션 갱신 대기" if lag_home
               else "경계 근처" if full.get("edgeNear") else "")
        sg = lambda x: f"{x:+.2f}".replace("-", MINUS)
        cells = [("ETF 판정", f'<span style="color:{verdict_color(v)}">{v}</span>', tag or "&nbsp;"),
                 ("가중평균 점수 n̄", sg(nbar), "−4(고평가 쪽) ~ +3(저평가 쪽)"),
                 ("카드가 덮은 비중", f"{cov * 100:.1f}%", "70% 미만이면 판정하지 않는다"),
                 ("덮지 못한 비중을 극단에 둔 범위", f"{sg(rng[0])} ~ {sg(rng[1])}" if rng else "—", "&nbsp;")]
        strip = "".join(f'<div class="op-cell"><span class="op-label">{a}</span><span class="op-val">{b}</span><span class="op-sub">{c}</span></div>'
                        for a, b, c in cells)
        segs = "".join(f'<span style="width:{bar[k] * 100:.2f}%;background:{c}" title="{k} {bar[k] * 100:.1f}%"></span>'
                       for k, c in BAR_TIERS if bar.get(k))
        labs = "".join(f'<span><i style="background:{c}"></i>{k} <b>{bar[k] * 100:.1f}%</b></span>' for k, c in BAR_TIERS if bar.get(k))
        ex = full.get("expense") if isinstance(full.get("expense"), dict) else {}
        if not (fin(ex.get("pct")) and isinstance(ex.get("url"), str) and isinstance(ex.get("source"), str)):
            ex = {}   # 보수·출처가 이상하면 그 안내만 뺀다(판정은 그대로)
        src = (f'보유 비중: {html.escape(full.get("holdingsSource") or "State Street")} (기준일 {kdate(full["S"])}) — 원본 파일은 다시 게시하지 않는다. '
               f'카드 판정: 이 사이트 v2 카드, {kdate(full["builtFor"])} 종가. 규칙 {html.escape(str(full.get("ruleVersion") or "—"))}.'
               + (f' 보수율 {ex["pct"]:.4f}% — <a href="{html.escape(ex["url"], quote=True)}">{html.escape(ex["source"])}</a>.' if ex.get("pct") is not None and ex.get("url") else ""))
        return (head + lede
                + f'  <div class="card"><div class="ret-strip verdict-strip">{strip}</div></div>\n'
                + f'  <div class="card"><div class="card-title">등급별 보유 비중</div><div class="vbar" role="img" aria-label="등급별 보유 비중">{segs}</div>'
                  f'<div class="vbar-lab">{labs}</div><div class="note">분모는 현금·권리 줄을 뺀 주식 보유 전체. 상위 10개 회사와 종목별 판정은 구성 종목 탭에 있다.</div></div>\n'
                + '  <div class="card"><div class="card-title">읽는 법과 한계</div><div class="note">카드 점수는 −4(고평가 쪽)부터 +3(저평가 쪽)까지라 비대칭이다 — '
                  '현금흐름 "매우 싸다"도 +1만 주기 때문에 평균은 아래로 기운다. 평균은 극단을 지우므로 막대를 함께 본다. 상위 10개 회사가 판정에 쓴 비중의 '
                  '절반쯤을 차지한다. 카드가 없는 종목은 대부분 지수의 작은 쪽이라 이 점수는 대형주 평균에 가깝다.</div>'
                  f'<div class="note">{src}</div></div>')
    except Exception:   # noqa: BLE001 — 판정 탭만 비우고 카드는 낸다
        traceback.print_exc()
        return box("판정 보류", "판정 자료를 그리지 못했다.")


def fill(tpl, m):
    for k, v in m.items():
        tpl = tpl.replace("{{" + k + "}}", v)
    return tpl


def render(res):
    head = (HERE / "template" / "card_head.html").read_text(encoding="utf-8")
    body = (HERE / "template" / "index_card.html").read_text(encoding="utf-8")
    cc = html.escape((res.get("crossCheck") or {}).get("text", ""))
    common = {"TITLE": f'{PROF["title"]} — US stock 가치를 말하다', "STATUS": res["status"],
              "S": kdate(res.get("S") or "—"), "BADGE": PROF["badge"], "KIND": PROF["kind"], "COMPANY": PROF["company"],
              "CURRENT": PROF["current"], "BACKNAV": PROF["backnav"], "CHARTNAME": PROF["chart"], "WHAT": PROF["what"],
              "NAVEXTRA": ('<button class="nav-btn" onclick="showSection(\'verdict\', this)">⚖️ 카드 판정</button>' if PROF["verdict"] else ""),
              "VERDICT": (f'<div id="verdict" class="section">\n{render_verdict(res.get("verdictData"), res.get("builtFor"))}\n</div>'
                          if PROF["verdict"] else "")}
    if res["status"] != "ok":
        msg = ('  <div class="card held-box"><div class="card-title">자료 보류</div>'
               f'<div style="font-size:14px;font-weight:700;color:var(--text);">{html.escape(res["reasonText"])}</div>'
               f'<div style="font-size:12px;color:var(--text2);margin-top:6px;">{html.escape(res.get("detail", ""))} · 홈 세션 '
               f'{html.escape(kdate(res.get("builtFor") or "—"))}</div></div>')
        m = dict(common, PRICE="—", META="", CHART=msg, RETURNS="", MONTHLY="", EVENTS="", HOLDINGS="",
                 SOURCES=f'시세: Yahoo Finance {PROF["symText"]} 일봉.', DAILY="[]", MA='{"ma5":[],"ma20":[],"ma60":[],"ma120":[]}',
                 RANGE_BASE="{}")
        return fill(head, m) + fill(body, m)
    by = {r["label"]: r for r in res["returns"]}
    arrow = "▲" if res["chg"] > 0 else "▼" if res["chg"] < 0 else ""
    price = f'<span class="price-change" style="color:{color(res["chg"])};">{arrow} {pct(res["chg"], 2)}</span> {num(res["close"])}'
    cons = res.get("constituents") or {}
    ch, tsy = cons.get("chars"), cons.get("dgs10")
    na = "불러오지 못함"
    ey_val = (f'{100 / ch["pe"]:.2f}%' if ch else "—") + " · " + (f'{tsy["value"] * 100:.2f}%' if tsy else "—")
    ey_sub = ((f'SSGA {kdate(ch["peAsOf"])}' if ch else "PER 불러오지 못함") + " / "
              + (f'FRED {kdate(tsy["date"])}' if tsy else "국채 불러오지 못함"))
    meta = "\n".join([
        meta_item("1년 수익률", pct(by["1년"]["ret"]), color(by["1년"]["ret"]), PROF["closeNote"],
                  f'기준 {kdate(by["1년"]["base"])} 종가'),
        meta_item("5년 연 환산", pct(by["5년"]["annual"]), color(by["5년"]["annual"]), "5년 누적 수익률을 1년마다로 바꾼 값(배당 제외)",
                  f'5년 누적 {pct(by["5년"]["ret"])}'),
        meta_item("PER (지수)", f'{ch["pe"]:.1f}배' if ch else "—", "var(--text)",
                  "State Street SPY 펀드 페이지 Index Characteristics: Price/Earnings(페이지에 계산 정의 없음)", f'SSGA {kdate(ch["peAsOf"])}' if ch else na),
        meta_item("이익수익률 · 미 10년 국채", ey_val, "var(--text)",
                  "이익수익률 = 1 ÷ PER(SSGA Price/Earnings). 미 10년 국채 = FRED DGS10. 두 숫자를 나란히 둘 뿐, 판정이 아니다", ey_sub),
        '    <div style="grid-column:1 / -1;font-size:11px;color:var(--text3);">PER과 이익수익률은 오늘 값이라 과거와 비교하지 않는다. 이 값만으로 저평가·고평가를 판정하지 않는다.</div>',
    ])
    dl = res["daily"]
    m = dict(common, PRICE=price, META=meta, CHART=fill(CHART_HTML, common), RETURNS=render_returns(res),
             MONTHLY=render_monthly(res), EVENTS=render_events(res), HOLDINGS=safe_holdings(res),
             SOURCES=((f'시세: Yahoo Finance SPY 일봉(시장 가격, 배당 제외). 종가는 State Street가 공시하는 SPY NAV 이력과 대조 — {cc}. '
                       '시가·고가·저가(캔들과 차트의 최고·최저 표시)는 NAV 이력에 없어 Yahoo 값 그대로다.') if PROF["key"] == "SPY" else
                      (f'시세: Yahoo Finance ^GSPC 일봉. 종가는 FRED SP500(S&amp;P Dow Jones Indices)과 대조 — {cc}. '
                       '시가·고가·저가(캔들과 차트의 최고·최저 표시)는 FRED에 없어 Yahoo 값 그대로다.')),
             DAILY=json.dumps(dl["rows"], separators=(",", ":")), MA=json.dumps(dl["ma"], separators=(",", ":")),
             RANGE_BASE=json.dumps(dl["base"]))
    return fill(head, m) + fill(body, m)


# ---------- 실행 ----------

def selfcheck(res, series):
    """내놓기 전 불변식 — 어긋나면 예외(→ 보류)."""
    if res["status"] != "ok":
        return
    ys = dict(series)
    assert abs(ys[res["S"]] - res["close"]) < 0.006
    for r in res["returns"]:
        assert abs(res["close"] / r["baseClose"] - 1 - r["ret"]) < 1e-3, r["label"]
        assert r["base"] < res["S"]
    ytd = next(r for r in res["returns"] if r["label"] == "YTD")
    cur = next(x for x in res["monthly"]["rows"] if x["year"] == int(res["S"][:4]))
    assert abs(cur["annual"]["ret"] - ytd["ret"]) < 1e-12
    prod = 1.0
    for c in cur["months"]:
        if c:
            prod *= 1 + c["ret"]
    assert abs(prod - 1 - ytd["ret"]) < 1e-9          # 월별 곱 = YTD
    dl, by = res["daily"], {r["label"]: r for r in res["returns"]}
    assert dl["rows"][-1][0] == res["S"] and all(abs(r[4] - ys[r[0]]) < 0.006 for r in dl["rows"])   # 캔들 종가 = 대조된 종가
    assert all(len(v) == len(dl["rows"]) for v in dl["ma"].values())
    for key, label in (("1M", "1개월"), ("6M", "6개월"), ("1Y", "1년"), ("3Y", "3년"), ("5Y", "5년")):
        assert dl["base"][key] == by[label]["base"], key   # 차트 제목 수익률 = 기간별 수익률 칸
    assert all(e["date"] <= res["S"] for e in res["events"])


def read_sessions(path):
    """(P, P 직전 세션). 직전 세션은 홈 시세 파일 종목들의 price.prevSession — P 세션인 종목이 모두 같은 값을 적었을 때만."""
    data = json.loads(path.read_text(encoding="utf-8"))
    P = data["priceSession"]
    prev = {(t.get("price") or {}).get("prevSession") for t in data.get("tickers") or []
            if (t.get("price") or {}).get("session") == P}
    return P, (prev.pop() if len(prev) == 1 else None)


def write_all(files):
    """산출물(JSON·페이지)을 임시 파일로 모두 쓴 뒤에야 바꿔 넣는다 — 임시 파일 쓰기가 실패하면 모두 어제 것으로 남는다
    (바꿔 넣는 os.replace 도중 실패하면 앞 것만 바뀔 수 있다 — 둘을 한꺼번에 바꾸는 장치는 없다)."""
    tmps = []
    try:
        for path, text in files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_name(path.name + ".tmp")
            tmp.write_text(text, encoding="utf-8")
            tmps.append((tmp, path))
    except Exception:
        for tmp, _ in tmps:
            tmp.unlink(missing_ok=True)
        raise
    for tmp, path in tmps:
        os.replace(tmp, path)


def held_res(reason, detail, P):
    return {"status": "held", "reason": reason, "reasonText": REASON_TEXT[reason], "detail": detail,
            "builtFor": P, "S": None, "index": PROF["key"], "name": PROF["name"], "source": f'Yahoo Finance {PROF["symText"]} 일봉 종가'}


def pages_for(res, P):
    """렌더링이 실패해도 보류 페이지를 쓴다 — 틀이 깨졌으면 틀 없는 최소 페이지."""
    try:
        return res, render(res)
    except Exception as e:   # noqa: BLE001
        traceback.print_exc()
        res = dict(held_res("run_fail", f"화면 만들기 실패({type(e).__name__})", P), runAt=res.get("runAt"), verdictData=res.get("verdictData"))
    try:
        return res, render(res)
    except Exception:   # noqa: BLE001
        traceback.print_exc()
        if PROF["verdict"]:
            return res, None   # ETF 카드: 틀까지 깨졌으면 페이지를 쓰지 않는다 — ETF 단계가 쓴 판정 페이지가 남는다
        page = ('<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
                f'<title>{PROF["title"]}</title></head><body><main data-status="held" style="max-width:900px;margin:0 auto;padding:28px 16px">'
                f'<a href="index.html">← 홈</a><h1>{PROF["badge"]}</h1><p>자료 보류 · {REASON_TEXT["run_fail"]}. 홈 세션 {html.escape(P or "—")}.</p>'
                '</main></body></html>\n')
        return res, page


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--card", choices=sorted(PROFILES), default="SPY")   # 지수 카드 페이지는 2026-10-20 지웠다 — SP500은 시험에서만 고른다
    ap.add_argument("--out-root", default=str(ROOT))
    ap.add_argument("--yahoo", help="Yahoo chart JSON 파일(시험용)")
    ap.add_argument("--fred", help="FRED CSV/JSON 파일(시험용) — --card SPY면 운용사 NAV 이력 xlsx 파일")
    ap.add_argument("--stocks", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--spy", help="SPY 판정 공개 산출물(기본: <out-root>/v2/etf/SPY.json)")
    ap.add_argument("--ssga-page", help="SSGA SPY 펀드 페이지 HTML 파일(시험용; 없으면 받는다)")
    ap.add_argument("--dgs10", help="FRED DGS10 CSV 파일(시험용; 없으면 받는다)")
    a = ap.parse_args(argv)
    use_profile(a.card)
    out = Path(a.out_root)
    P, prevP, series = None, None, []
    try:
        try:
            P, prevP = read_sessions(Path(a.stocks))
        except Exception:
            pass
        try:
            ytext = Path(a.yahoo).read_text(encoding="utf-8") if a.yahoo else http_get(YAHOO.format(sym=PROF["sym"], end=int(time.time()) + 86400))
            series = parse_yahoo(ytext)
            ohlc = parse_ohlc(ytext)
        except Exception as e:
            raise Hold("fetch_fail", type(e).__name__)
        try:
            if PROF["key"] == "SPY":   # 대조 자료 = 운용사 NAV 이력
                fred = parse_navhist(Path(a.fred).read_bytes() if a.fred else fetch_navhist())
            else:
                fred = parse_fred(Path(a.fred).read_text(encoding="utf-8") if a.fred else fetch_fred())
            if not fred:
                fred = None
        except Exception:
            fred = None
        res = compute(series, fred, P, prevP, ohlc)
        selfcheck(res, [p for p in series if p[0] <= P])
        cons = {"spy": read_spy(a.spy or out / "v2" / "etf" / "SPY.json"), "sectors": None, "chars": None}
        try:   # 운용사 페이지 실패는 그 칸들만 비운다
            page = Path(a.ssga_page).read_text(encoding="utf-8") if a.ssga_page else http_get(SSGA_PAGE)
        except Exception:   # noqa: BLE001
            page = ""
        try:   # 미 10년 국채(FRED DGS10): S 이하 마지막 값. 실패하면 그 값만 비운다
            dg = parse_fred(Path(a.dgs10).read_text(encoding="utf-8") if a.dgs10 else fetch_fred("DGS10"))
            k = max(d_ for d_ in dg if d_ <= res["S"])
            cons["dgs10"] = {"date": k, "value": round(dg[k] / 100, 6)} if 0 < dg[k] < 20 else None
        except Exception:   # noqa: BLE001
            cons["dgs10"] = None
        for key, fn in (("sectors", parse_sectors), ("chars", parse_chars)):
            try:
                cons[key] = fn(page)
            except Exception:   # noqa: BLE001
                cons[key] = None
        res["constituents"] = cons
    except Hold as h:
        res = {"status": "held", "reason": h.reason, "reasonText": REASON_TEXT[h.reason], "detail": h.detail,
               "builtFor": P, "S": None}
    except Exception as e:   # noqa: BLE001 — 어떤 실패도 보류로 쓰고 종목 게시는 막지 않는다
        traceback.print_exc()
        res = {"status": "held", "reason": "run_fail", "reasonText": REASON_TEXT["run_fail"],
               "detail": type(e).__name__, "builtFor": P, "S": None}
    res["index"], res["name"] = PROF["key"], PROF["name"]
    res["runAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    res["source"] = f'Yahoo Finance {PROF["symText"]} 일봉 종가'
    if PROF["verdict"]:   # 판정 탭: 시세가 보류여도 판정은 따로 보인다
        try:
            res["verdictData"] = json.loads((Path(a.spy) if a.spy else out / "v2" / "etf" / "SPY.json").read_text(encoding="utf-8"))
        except Exception:   # noqa: BLE001
            res["verdictData"] = None
    res, page = pages_for(res, P)
    public = {k: v for k, v in res.items() if k not in ("daily", "verdictData")}   # 캔들 자료는 페이지 안에만, 판정은 SPY.json에 이미 있다
    files = {out / PROF["json"]: json.dumps(public, ensure_ascii=False, indent=1) + "\n"}
    if page is not None:
        files[out / PROF["html"]] = page
    write_all(files)
    line = (f"{'ETF CARD' if PROF['verdict'] else 'INDEX'} {PROF['key']}: {res['status']}"
            + (f" S={res['S']} close={res['close']} cross={res['crossCheck']['status']} events={len(res['events'])}"
               if res["status"] == "ok" else f" reason={res['reason']} ({res.get('detail', '')})"))
    print(line)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
