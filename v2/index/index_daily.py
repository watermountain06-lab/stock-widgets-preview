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

    python3 v2/index/index_daily.py [--card SP500|SPY|QQQ|DIA|IWM|TLT|GLD] [--out-root DIR] [--yahoo FILE] [--fred FILE] [--stocks FILE]

--card SPY(2026-10-20 사용자 결정): 같은 틀로 SPY ETF 카드를 만든다 — 시세는 Yahoo SPY 일봉(시장 가격, 배당 제외),
대조는 FRED 대신 운용사(State Street)가 공시하는 SPY NAV 이력(2003-12부터; --card DIA도 같은 방식, 2026-10-21): 날짜가 빠짐없이 있고 종가가 NAV와 가까워야
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
              "verdict": False, "navKind": "fred", "verdictJson": None, "etf": "SPY", "nonEqText": "현금·권리 줄",
              "page": "https://www.ssga.com/us/en/intermediary/etfs/spdr-sp-500-etf-trust-spy", "sectorCount": 11},
    "SPY": {"key": "SPY", "name": "SPY", "sym": "SPY", "symText": "SPY", "ref": "운용사 NAV",
            "json": "v2/etf/SPY_card.json", "html": "preview-only-etf-spy.html",
            "title": "SPY ETF", "badge": "SPY", "kind": "ETF · S&amp;P 500을 따라감 · 시장 가격(배당 제외)",
            "company": "SPDR S&amp;P 500 ETF Trust", "current": "SPY · ETF", "backnav": "",
            "chart": "SPY 차트", "retTitle": "SPY 시장 가격(배당 제외)", "what": "ETF 시세", "weightOf": "SPY 비중",
            "closeNote": "SPY 시장 가격(배당 제외), 운용사 NAV와 대조한 종가(마지막 날은 NAV 게시 전이면 대조 전)",
            "span": "운용사 NAV 대조 구간({since}부터)",
            "lede": "SPY는 S&amp;P 500 지수를 따라가는 ETF다(State Street). 업종 비중은 운용사가 공개하는 지수 기준, 상위 10개 회사와 카드 비중은 SPY 보유 기준이다.",
            "verdict": True, "navKind": "ssga", "verdictJson": "v2/etf/SPY.json", "etf": "SPY", "nonEqText": "현금·권리 줄",
            "page": "https://www.ssga.com/us/en/intermediary/etfs/spdr-sp-500-etf-trust-spy", "navFile": "spy", "sectorCount": 11},
    # DIA(2026-10-21, 설계 dr r1): SPY와 같은 운용사·형식. 다우존스(DJIA)는 주가 가중 30종목이라 GICS 업종이 9개뿐(실측) — 기대 개수 9,
    # 바뀌면 업종 칸만 실패(설정 갱신). NAV 대조·허용 폭·휴장일 NAV 목록은 SPY와 같다(DIA 실측이 안에 든다).
    "DIA": {"key": "DIA", "name": "DIA", "sym": "DIA", "symText": "DIA", "ref": "운용사 NAV",
            "json": "v2/etf/DIA_card.json", "html": "preview-only-etf-dia.html",
            "title": "DIA ETF", "badge": "DIA", "kind": "ETF · 다우존스 산업평균(30종목, 주가 가중)을 따라감 · 시장 가격(배당 제외)",
            "company": "SPDR Dow Jones Industrial Average ETF Trust", "current": "DIA · ETF", "backnav": "",
            "chart": "DIA 차트", "retTitle": "DIA 시장 가격(배당 제외)", "what": "ETF 시세", "weightOf": "DIA 비중",
            "closeNote": "DIA 시장 가격(배당 제외), 운용사 NAV와 대조한 종가(마지막 날은 NAV 게시 전이면 대조 전)",
            "span": "운용사 NAV 대조 구간({since}부터)",
            "lede": "DIA는 다우존스 산업평균(DJIA) 30종목을 따라가는 ETF다(State Street). DJIA는 시가총액이 아니라 주가 가중 지수라 주가가 높은 종목의 비중이 크다. 업종 비중과 PER은 운용사가 공개하는 지수 기준, 상위 10개 회사와 카드 비중은 DIA 보유 기준이다.",
            "verdict": True, "navKind": "ssga", "verdictJson": "v2/etf/DIA.json", "etf": "DIA", "nonEqText": "현금·권리 줄",
            "page": "https://www.ssga.com/us/en/intermediary/etfs/spdr-dow-jones-industrial-average-etf-trust-dia", "navFile": "dia", "sectorCount": 9},
    # QQQ(2026-10-21, 설계 dr r1~r3): 대조는 Invesco NAV 이력(회전 창, 달력일 — 비거래일은 직전 값 반복). 업종(ICB)·PER은 펀드 기준.
    # IWM(2026-10-21, 사용자 결정): 러셀 2000 — 가격 카드만(판정 없음). iShares가 보유·NAV 이력 파일을 막아(로컬·Actions) 과거 가격은
    # 대조하지 못하고, 상품 페이지의 최근 하루 NAV만 대조한다(navKind page_nav). 구성 종목 탭 없음(상위 보유·업종을 읽을 수 없다).
    "IWM": {"key": "IWM", "name": "IWM", "sym": "IWM", "symText": "IWM", "ref": "운용사 NAV(최근 하루)",
            "json": "v2/etf/IWM_card.json", "html": "preview-only-etf-iwm.html",
            "title": "IWM ETF", "badge": "IWM", "kind": "ETF · 러셀 2000(미국 소형주 약 2,000개)을 따라감 · 시장 가격(배당 제외)",
            "company": "iShares Russell 2000 ETF", "current": "IWM · ETF", "backnav": "",
            "chart": "IWM 차트", "retTitle": "IWM 시장 가격(배당 제외)", "what": "ETF 시세", "weightOf": "IWM 비중",
            "closeNote": "IWM 시장 가격(배당 제외). 과거 종가는 운용사 자료와 대조하지 못했다 — 최근 하루 NAV만 확인",
            "span": "계산 구간({since}부터 — 표시에 필요한 범위만)",
            "lede": "",
            "verdict": False, "noVerdict": True, "navKind": "page_nav", "verdictJson": None, "etf": "IWM", "nonEqText": "",
            "page": "https://www.ishares.com/us/products/239710/ishares-russell-2000-etf", "homePrice": True},
    # GLD·TLT(2026-10-21, 사용자 결정 + 설계 dr r1~r5 합의): 가격 카드만(판정 없음). asset이 equity가 아니면 보유·SSGA 페이지·업종·PER·
    # DGS10을 읽지도 부르지도 않고, 머리·출처 줄은 asset별 함수가 만든다. compute(대조·창 자르기)는 navKind로 가른다.
    # GLD: 운용사(SPDR Gold Trust) 과거 자료 파일의 공식 종가와 카드 구간 전체를 날마다 대조(navKind gld_archive).
    "GLD": {"key": "GLD", "name": "GLD", "sym": "GLD", "symText": "GLD", "ref": "운용사 종가",
            "json": "v2/etf/GLD_card.json", "html": "preview-only-etf-gld.html",
            "title": "GLD ETF", "badge": "GLD", "kind": "ETF · 금 실물을 담는 신탁 · 시장 가격(분배금 없음)",
            "company": "SPDR Gold Shares (SPDR Gold Trust)", "current": "GLD · ETF", "backnav": "",
            "chart": "GLD 차트", "retTitle": "GLD 시장 가격(분배금 없음)", "what": "ETF 시세", "weightOf": "GLD 비중",
            "closeNote": "GLD 한 주의 시장 가격(분배금 없음). 운용사 과거 자료 파일의 종가와 날마다 대조한 종가(마지막 날은 운용사 게시 전이면 대조 전)",
            "span": "운용사 종가 대조 구간({since}부터)", "lede": "", "retBasis": "분배금 없음",
            "verdict": False, "noVerdict": True, "navKind": "gld_archive", "asset": "gold", "verdictJson": None, "etf": "GLD", "nonEqText": "",
            "noVerdictText": "GLD는 금 실물을 담는 신탁이다 — 기업 이익으로 매기는 이 사이트 카드 판정을 할 대상이 없다. 이 카드는 가격·수익률만 보여 준다.",
            "archive": "https://api.spdrgoldshares.com/api/v1/historical-archive?product=gld&exchange=NYSE&lang=en",
            "page": "https://www.spdrgoldshares.com/usa/gld/",
            "fee": ("스폰서 수수료 연 0.40%", "SEC 10-Q 2026-08-04",
                    "https://www.sec.gov/Archives/edgar/data/1222333/000143774926025680/gld20260630_10q.htm"),
            "homePrice": True},
    # TLT: IWM과 같은 하루 NAV 대조(page_nav) — NAV는 TLT 펀드에 연결된 JSON-LD 요소에서만(parse_ishares_fund), 지표는 그 펀드 지표 블록에서만.
    "TLT": {"key": "TLT", "name": "TLT", "sym": "TLT", "symText": "TLT", "ref": "운용사 NAV(최근 하루)",
            "json": "v2/etf/TLT_card.json", "html": "preview-only-etf-tlt.html",
            "title": "TLT ETF", "badge": "TLT", "kind": "ETF · 미국 국채(만기 20년 이상)를 담음 · 시장 가격(분배금 제외)",
            "company": "iShares 20+ Year Treasury Bond ETF", "current": "TLT · ETF", "backnav": "",
            "chart": "TLT 차트", "retTitle": "TLT 시장 가격(분배금 제외)", "what": "ETF 시세", "weightOf": "TLT 비중",
            "closeNote": "TLT 시장 가격(분배금 제외). 과거 종가는 운용사 자료와 대조하지 못했다 — 최근 하루 NAV만 확인",
            "span": "계산 구간({since}부터 — 표시에 필요한 범위만)", "lede": "", "retBasis": "분배금 제외",
            "verdict": False, "noVerdict": True, "navKind": "page_nav", "asset": "bond", "verdictJson": None, "etf": "TLT", "nonEqText": "",
            "noVerdictText": "TLT는 미국 국채를 담는 펀드다 — 기업 이익으로 매기는 이 사이트 카드 판정을 할 대상이 없다. 이 카드는 가격·수익률만 보여 준다.",
            "page": "https://www.ishares.com/us/products/239454/ishares-20-year-treasury-bond-etf", "ticker": "TLT",
            "fee": ("총보수 0.15%", "SEC 497K 2026-06-29",
                    "https://www.sec.gov/Archives/edgar/data/1100663/000119312526287948/d128154d497k.htm"),
            "homePrice": True},
    "QQQ": {"key": "QQQ", "name": "QQQ", "sym": "QQQ", "symText": "QQQ", "ref": "운용사 NAV",
            "json": "v2/etf/QQQ_card.json", "html": "preview-only-etf-qqq.html",
            "title": "QQQ ETF", "badge": "QQQ", "kind": "ETF · 나스닥 100을 따라감 · 시장 가격(배당 제외)",
            "company": "Invesco QQQ Trust, Series 1", "current": "QQQ · ETF", "backnav": "",
            "chart": "QQQ 차트", "retTitle": "QQQ 시장 가격(배당 제외)", "what": "ETF 시세", "weightOf": "QQQ 비중",
            "closeNote": "QQQ 시장 가격(배당 제외), 운용사 NAV와 대조한 종가(마지막 날은 NAV 게시 전이면 대조 전)",
            "span": "운용사 NAV 대조 구간({since}부터 — Invesco가 최근 약 10년만 준다)",
            "lede": "QQQ는 나스닥 100 지수를 따라가는 ETF다(Invesco). 업종 비중과 PER은 운용사가 공개하는 펀드 기준, 상위 10개 회사와 카드 비중은 QQQ 보유 기준이다.",
            "verdict": True, "navKind": "invesco", "verdictJson": "v2/etf/QQQ.json", "etf": "QQQ",
            "nonEqText": "비주식으로 확인된 현금·통화·통화담보·지수선물·합성현금 줄"},
}
PROF = PROFILES["SP500"]


def asset():
    return PROF.get("asset", "equity")


class _Done(Exception):
    """금·채권 카드가 주식형 부가 자료 단계를 건너뛸 때(같은 try 안의 보류·실패 처리를 그대로 쓰려고)."""


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
    return "ok", (f"State Street {PROF['etf']} NAV 이력과 {len(both)}일({lo}~{hi}) 대조: 거래일마다 NAV 있음"
                  + (f"(장이 쉰 날 NAV만 {len(extra)}일)" if extra else "")
                  + f", 종가와 NAV 차이 최대 {worst[1] * 100:+.2f}%({worst[0]}), 최근 {RECENT_EXACT}세션 최대 "
                  + f"{max(abs(g) for _, g in recent) * 100:.2f}%"
                  + (f" · 마지막 {S} 종가는 NAV 게시 전이라 대조 전(Yahoo 값)" if lag else ""))


INVESCO_API = "https://dng-api.invesco.com/cache/v1/accounts/en_US/shareclasses/{cusip}{path}"
QQQ_CUSIP = "46090E103"
NYSE_SPECIAL_CLOSED = {"2018-12-05", "2025-01-09"}   # 국가 애도일(부시·카터) — 새로 생기면 더한다(그날 Yahoo가 비어 날짜 대조가 알린다)


def easter(y):
    a, b, c = y % 19, y // 100, y % 100
    d_, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d_ - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    return date(y, (h + l_ - 7 * m + 114) // 31, (h + l_ - 7 * m + 114) % 31 + 1)


def nyse_holidays(y):
    """NYSE 휴장일 규칙(출처: NYSE 휴장일 공지). 새해가 토요일이면 대체 휴장 없음(2021-12-31 거래), 일요일이면 1/2.
    독립기념일·준틴스(2022~)·성탄은 토→금, 일→월. 2016-09~2026-10 Yahoo QQQ 거래일 2,547일과 일치 확인(2026-10-21)."""
    def nth(m, wd, n):
        d0 = date(y, m, 1)
        return d0 + timedelta((wd - d0.weekday()) % 7 + 7 * (n - 1))
    def last_mon(m):
        d0 = date(y, m + 1, 1) - timedelta(1)
        return d0 - timedelta((d0.weekday() - 0) % 7)
    def obs(d0):
        return d0 - timedelta(1) if d0.weekday() == 5 else d0 + timedelta(1) if d0.weekday() == 6 else d0
    h = {nth(1, 0, 3), nth(2, 0, 3), easter(y) - timedelta(2), last_mon(5), obs(date(y, 7, 4)), nth(9, 0, 1),
         nth(11, 3, 4), obs(date(y, 12, 25))}
    nd = date(y, 1, 1)
    if nd.weekday() == 6:
        h.add(date(y, 1, 2))
    elif nd.weekday() < 5:
        h.add(nd)
    if y >= 2022:
        h.add(obs(date(y, 6, 19)))
    return h


def nyse_days(lo, hi):
    """lo~hi(포함) NYSE 거래일 iso 목록. 조기 폐장은 거래일."""
    out, d0, cache = [], d(lo), {}
    while d0 <= d(hi):
        if d0.weekday() < 5 and d0 not in cache.setdefault(d0.year, nyse_holidays(d0.year)) and d0.isoformat() not in NYSE_SPECIAL_CLOSED:
            out.append(d0.isoformat())
        d0 += timedelta(1)
    return out


def fetch_invesco(path, cusip=QQQ_CUSIP):
    req = urllib.request.Request(INVESCO_API.format(cusip=cusip, path=path), headers={"User-Agent": "Mozilla/5.0 (stock-widgets-preview ETF card)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def parse_invesco_nav(text):
    """Invesco navs JSON → [(날짜 iso, 값)] 그대로(중복·이상값 판단은 대조에서 — "NAV 형식 변경"으로)."""
    v = json.loads(text)
    rows = next(x["data"] for x in v["lineChartData"] if x.get("type") == "NAV")
    return [(datetime.strptime(p["date"], "%m/%d/%Y").date().isoformat(), p["value"]) for p in rows]


def cross_check_invesco(series, nav_pairs, P, prevP):
    """형식 B NAV 대조(설계 dr r2·r3). 거래일 = Yahoo와 독립인 NYSE 규칙 달력. 비교는 NAV 첫 날 이후 첫 거래일 ~ P.
    ① Yahoo 날짜 = 달력 ② 달력 거래일마다 NAV(P 하루는 게시 전 허용, prevP까지는 필수) ③ 비거래일 NAV = 직전 거래일 NAV
    ④ NAV 중복·비유한·0 이하 → 형식 변경 ⑤ 괴리 최근 250거래일 ±1.0%, 그 앞 ±2.0%. (상태, 설명, nav dict)."""
    if not nav_pairs:
        return "unavailable", "운용사 NAV 이력에 닿지 못함", None
    seen, nav = set(), {}
    for k, v in nav_pairs:
        if k in seen or not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v) or v <= 0:
            return "mismatch", f"NAV 형식 변경: {k} 중복이거나 값이 이상함", None
        seen.add(k)
        nav[k] = float(v)
    cal = nyse_days(min(nav), P)
    if len(cal) < RECENT_EXACT:
        return "unavailable", f"NAV 구간 거래일이 {len(cal)}일뿐", None
    first, hi = cal[0], max(k for k in nav if k <= P) if any(k <= P for k in nav) else None
    if hi is None or hi < prevP:
        return "unavailable", f"NAV가 {hi}까지만 있음 — 직전 세션 {prevP}까지 없다", None
    ys = {k: c for k, c in series if first <= k <= P}
    calset = set(cal)
    if set(ys) != calset:
        odd = sorted(set(ys) ^ calset)
        return "mismatch", f"날짜 불일치: 시세와 NYSE 달력이 {len(odd)}일 다름 (첫 날 {odd[0]})", None
    lag = hi < P
    missing = [k for k in cal if k <= hi and k not in nav]
    if missing:
        return "mismatch", f"날짜 불일치: NAV 없는 거래일 {len(missing)}일 (첫 날 {missing[0]})", None
    last_t = None
    for k in sorted(nav):
        if k < first or k > hi:
            continue
        if k in calset:
            last_t = nav[k]
        elif last_t is not None and abs(nav[k] / last_t - 1) > 1e-9:
            return "mismatch", f"NAV 형식 변경: 비거래일 {k}의 NAV가 직전 거래일 값과 다름", None
    both = [k for k in cal if k <= hi]
    gaps = [(k, ys[k] / nav[k] - 1) for k in both]
    recent, old = gaps[-RECENT_EXACT:], gaps[:-RECENT_EXACT]
    bad = [k for k, g in recent if abs(g) > NAV_RECENT_TOL] + [k for k, g in old if abs(g) > NAV_OLD_TOL]
    if bad:
        return "mismatch", f"종가와 NAV 차이가 큰 날 {len(bad)}일 (첫 날 {min(bad)})", None
    worst = max(gaps, key=lambda t: abs(t[1]))
    return "ok", (f"Invesco QQQ NAV 이력과 {len(both)}거래일({first}~{both[-1]}) 대조: 거래일마다 NAV 있음, 비거래일 NAV는 직전 값 반복, "
                  f"종가와 NAV 차이 최대 {worst[1] * 100:+.2f}%({worst[0]}), 최근 {RECENT_EXACT}거래일 최대 "
                  f"{max(abs(g) for _, g in recent) * 100:.2f}%"
                  + (f" · 마지막 {P} 종가는 NAV 게시 전이라 대조 전(Yahoo 값)" if lag else "")), {k: nav[k] for k in both}


def parse_ishares_page(text):
    """iShares 상품 페이지(서버 렌더)에서 최근 NAV·기준일(JSON-LD "NAV as of" 묶음 — 정확히 하나), 펀드 PER·기준일, 보유 종목 수.
    NAV 묶음이 없거나 둘 이상이 서로 다르거나 숫자가 이상하면 nav None(→ 대조 못 함). PER·보유 수는 못 읽으면 그 칸만 None."""
    out = {"nav": None, "navDate": None, "pe": None, "peAsOf": None, "holdings": None, "holdingsAsOf": None}
    hits = set(re.findall(r'"name":"NAV as of","value":"([^"]+)","unitText":"USD","valueReference":\{"@type":"PropertyValue",'
                          r'"name":"As of Dates","value":"([A-Z][a-z]{2} \d{1,2}, \d{4})"\}', text))
    if len(hits) == 1:
        v, dt_ = next(iter(hits))
        try:
            x = float(v.replace(",", ""))
            if math.isfinite(x) and x > 0:
                out["nav"], out["navDate"] = x, datetime.strptime(dt_, "%b %d, %Y").date().isoformat()
        except ValueError:
            pass
    plain = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text)))
    try:   # PER·보유 수는 칸마다 따로 — 못 읽어도 NAV(대조)는 그대로
        m = re.search(r"P/E Ratio ([0-9]+(?:\.[0-9]+)?) as of ([A-Z][a-z]{2} \d{1,2}, \d{4})", plain)
        if m and 3 < float(m.group(1)) < 100:
            out["pe"], out["peAsOf"] = float(m.group(1)), datetime.strptime(m.group(2), "%b %d, %Y").date().isoformat()
    except ValueError:
        out["pe"] = out["peAsOf"] = None
    try:
        m = re.search(r"Number of Holdings ([0-9,]+) as of ([A-Z][a-z]{2} \d{1,2}, \d{4})", plain)
        if m:
            out["holdings"], out["holdingsAsOf"] = int(m.group(1).replace(",", "")), datetime.strptime(m.group(2), "%b %d, %Y").date().isoformat()
    except ValueError:
        out["holdings"] = out["holdingsAsOf"] = None
    return out


NAV_DAY_TOL = 0.010   # 최근 하루: |종가 / NAV − 1| ≤ 1.0%(SPY·QQQ·DIA의 최근 250세션 허용 폭과 같다)


def cross_check_page(series, info, P, prevP):
    """page_nav(IWM): 운용사 페이지의 최근 하루 NAV를 그날 Yahoo 종가와 대조. NAV 날짜는 홈 세션 P 또는 직전 세션 prevP여야 한다
    (저녁엔 P의 NAV가 아직일 수 있다). 미래 날짜·그날 종가 없음 → 불일치, prevP보다 이르면 대조 못 함. 과거 구간은 대조하지 않는다."""
    if not info or info.get("nav") is None:
        return "unavailable", "운용사 페이지에서 NAV를 읽지 못함"
    nd = info["navDate"]
    if nd > P:
        return "mismatch", f"운용사 NAV 날짜 {nd}가 홈 세션 {P}보다 뒤"
    if nd < prevP:
        return "unavailable", f"운용사 NAV가 {nd}까지만 있음 — 직전 세션 {prevP}까지 없다"
    ys = dict(series)
    if nd not in ys:
        return "mismatch", f"NAV 날짜 {nd}의 종가가 시세에 없음"
    g = ys[nd] / info["nav"] - 1
    if abs(g) > NAV_DAY_TOL + 1e-12:
        return "mismatch", f"종가와 NAV 차이가 허용 범위(±1%)를 넘음: {nd} {g * 100:+.2f}%"
    return "ok", (f"iShares 상품 페이지의 {nd} NAV와 그날 종가 차이 {g * 100:+.2f}%(±1% 안)"
                  + (f" · 마지막 {P} 종가는 NAV 게시 전이라 대조 전" if nd < P else "")
                  + " · 그 앞 과거 종가는 운용사 이력 파일을 자동으로 받지 못해 대조하지 못했다")


# ---------- GLD(금) — 운용사 과거 자료 파일 ----------
# SPDR Gold Trust 과거 자료 xlsx(spdrgoldshares.com 과거 자료 페이지의 다운로드). 시트 "US GLD Historical Archive", 휴장일은 모든 칸이
# "US Holiday". 파일 첫 시트에 재배포 금지 문구가 있어 파일은 대조에만 쓰고 다시 게시하지 않는다(2026-10-21 설계 dr r1~r5).
GLD_SHEET = "US GLD Historical Archive"
GLD_COLS = ("Date", "Closing Price", "Ounces of Gold per Share", "Tonnes of Gold")
GLD_HOLIDAY = "US Holiday"
GLD_TOL = 0.001   # 종가 대 종가: |Yahoo / 운용사 − 1| ≤ 0.1%(2015-11~2026-10 실측 최대 0.042%)
# 운용사 달력 표기 예외 {날짜: 사유} — 처음엔 비어 있다. 면제하는 것은 달력 검사뿐(평일 줄 없음, "US Holiday"인데 Yahoo 종가 있음,
# 운용사 숫자 종가인데 Yahoo 없음)이고, 가격 차이·값 이상은 면제하지 않는다. 면제된 날 수는 출처 줄에 "대조 제외 n일"로 적는다.
GLD_CAL_OK = {}


def read_xlsx_sheet(body, name):
    """xlsx의 이름이 name인 시트를 [[셀…]…]로(표준 라이브러리만). 시트가 없으면 ValueError."""
    import xml.etree.ElementTree as XT
    import zipfile
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
          "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
    z = zipfile.ZipFile(io.BytesIO(body))
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in XT.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
            shared.append("".join(t.text or "" for t in si.iter(f"{{{ns['m']}}}t")))
    wb = XT.fromstring(z.read("xl/workbook.xml"))
    hit = [s for s in wb.findall("m:sheets/m:sheet", ns) if s.get("name") == name]
    if len(hit) != 1:
        raise ValueError(f"시트 {name!r} {len(hit)}개")
    rid = hit[0].get(f"{{{ns['r']}}}id")
    rels = XT.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = next(x.get("Target") for x in rels if x.get("Id") == rid)
    sheet = XT.fromstring(z.read("xl/" + target.lstrip("/").removeprefix("xl/")))
    rows = []
    for row in sheet.iter(f"{{{ns['m']}}}row"):
        cells = {}
        for c in row.findall("m:c", ns):
            idx = 0
            for ch in re.match(r"[A-Z]+", c.get("r")).group(0):
                idx = idx * 26 + (ord(ch) - 64)
            t, v = c.get("t"), c.find("m:v", ns)
            if t == "s":
                val = shared[int(v.text)] if v is not None else None
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter(f"{{{ns['m']}}}t"))
            elif t in ("str", "b", "e"):
                val = v.text if v is not None else None
            else:
                val = float(v.text) if v is not None and v.text not in (None, "") else None
            cells[idx - 1] = val
        rows.append([cells.get(i) for i in range(max(cells) + 1)] if cells else [])
    return rows


def fetch_gld_archive():
    req = urllib.request.Request(PROF["archive"], headers={"User-Agent": "Mozilla/5.0 (stock-widgets-preview ETF card)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def parse_gld_archive(body):
    """GLD 과거 자료 xlsx → [(날짜 iso, 줄)] 날짜 오름차순. 줄 = 원래 셀 목록(값 검사는 대조가 창 안 줄에만 한다).
    파일 전체 검사: zip(xlsx)인가, 시트 이름, 머리 열 이름(필요한 열이 정확히 하나씩), 모든 줄의 날짜 파싱·엄격 오름차순·중복 없음.
    하나라도 어긋나면 ValueError(→ 대조 못 함). 반환: {"rows": [...], "col": {열 이름: 위치}}."""
    if not isinstance(body, (bytes, bytearray)) or not body.startswith(b"PK"):
        raise ValueError("운용사 파일이 xlsx가 아니다(차단 페이지 등)")
    rows = read_xlsx_sheet(body, GLD_SHEET)
    if not rows or not rows[0]:
        raise ValueError("머리 줄 없음")
    head = [str(x).strip() if x is not None else "" for x in rows[0]]
    col = {}
    for name in GLD_COLS:
        if head.count(name) != 1:
            raise ValueError(f"머리 열 {name!r} {head.count(name)}개")
        col[name] = head.index(name)
    out, last = [], None
    for r in rows[1:]:
        if not r or all(x in (None, "") for x in r):
            continue
        raw = r[col["Date"]] if len(r) > col["Date"] else None
        if not isinstance(raw, str) or not re.fullmatch(r"\d{1,2}-[A-Z][a-z]{2}-\d{4}", raw.strip()):
            raise ValueError(f"날짜를 읽지 못함: {raw!r}")
        k = datetime.strptime(raw.strip(), "%d-%b-%Y").date().isoformat()
        if last is not None and k <= last:
            raise ValueError(f"날짜 순서·중복 {last} → {k}")
        last = k
        out.append((k, r))
    if not out:
        raise ValueError("자료 줄 없음")
    return {"rows": out, "col": col}


def _pos(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) and x > 0


def cross_check_gld(series, arch, S, prevP):
    """GLD: 이미 창으로 자른 Yahoo 종가(series)를 운용사 종가와 날마다 대조. arch = parse_gld_archive 결과(None이면 대조 못 함).
    반환 (상태, 글, 구조 칸) — 구조 칸 {since, checkedThrough, pendingDate, maxGap, maxGapDate, exempt, oz, ozAsOf, tonnes}."""
    if not arch or arch.get("err"):
        return "unavailable", "운용사 과거 자료 파일을 받지 못했거나 모양이 다름" + (f" — {arch['err']}" if arch and arch.get("err") else ""), None
    first, P = series[0][0], S
    col = arch["col"]
    ci, oi, ti = col["Closing Price"], col["Ounces of Gold per Share"], col["Tonnes of Gold"]
    rows = [(k, r) for k, r in arch["rows"] if first <= k <= P]   # 창 밖·P 이후 줄의 값은 보지 않는다
    iss, hol = {}, set()
    di = col["Date"]
    for k, r in rows:
        cells = [r[i] if len(r) > i else None for i in (ci, oi, ti)]
        rest = [x for i, x in enumerate(r) if i != di and x not in (None, "")]   # 날짜 빼고 값이 있는 모든 칸
        if all(isinstance(x, str) and x.strip() == GLD_HOLIDAY for x in cells) and all(isinstance(x, str) and x.strip() == GLD_HOLIDAY for x in rest):
            hol.add(k)
        elif _pos(cells[0]):
            iss[k] = r
        else:
            return "unavailable", f"운용사 파일 {k} 줄의 종가가 숫자가 아니거나 0 이하({cells[0]!r})", None
    if not iss:
        return "unavailable", f"운용사 파일에 {first}~{P} 종가가 없음", None
    through = max(iss)
    if through < prevP:
        return "unavailable", f"운용사 종가가 {through}까지만 있음 — 직전 세션 {prevP}까지 없다", None
    ys = dict(series)
    exempt = set()
    # 평일 완전성: 창 첫날~through의 모든 평일이 운용사 파일에 줄(숫자 또는 US Holiday)로 있어야 한다(양쪽에서 같이 빠진 날을 잡는다)
    day, end = d(first), d(through)
    have = set(iss) | hol
    while day <= end:
        k = day.isoformat()
        if day.weekday() < 5 and k not in have:
            if k in GLD_CAL_OK:
                exempt.add(k)
            else:
                return "unavailable", f"운용사 파일에 평일 {k} 줄이 없음", None
        day += timedelta(days=1)
    for k in sorted(hol):
        if k in ys:
            if k in GLD_CAL_OK:
                exempt.add(k)
                continue
            return "mismatch", f"운용사가 휴장으로 표기한 {k}에 시장 종가가 있음(가격 차이 아님 — 달력 불일치)", None
    for k, _ in series:
        if k > through:
            break
        if k not in iss and k not in hol and k not in exempt:
            if k in GLD_CAL_OK:
                exempt.add(k)
                continue
            return "mismatch", f"{k} 시장 종가는 있는데 운용사 종가가 없음", None
    worst = (None, 0.0)
    for k in sorted(iss):
        if k not in ys:
            if k in GLD_CAL_OK:
                exempt.add(k)
                continue
            return "mismatch", f"운용사 종가 {k}가 시세에 없음", None
        g = ys[k] / iss[k][ci] - 1
        if abs(g) > GLD_TOL + 1e-12:
            return "mismatch", f"종가 차이가 허용 범위(±{GLD_TOL * 100:g}%)를 넘음: {k} 시장 {ys[k]:.2f} · 운용사 {iss[k][ci]:.2f} ({g * 100:+.3f}%)", None
        if worst[0] is None or abs(g) > abs(worst[1]):
            worst = (k, g)
    pending = None
    if through < P:
        pending = P   # through == prevP(위에서 확인) — P 줄이 휴장 표기면 위 달력 검사가 이미 불일치로 냈다
    last = iss[through]
    oz, tn = (last[oi] if len(last) > oi else None), (last[ti] if len(last) > ti else None)
    info = {"since": first, "checkedThrough": through, "pendingDate": pending, "maxGap": worst[1], "maxGapDate": worst[0],
            "exempt": len(exempt), "oz": oz if _pos(oz) else None, "tonnes": tn if _pos(tn) else None, "ozAsOf": through}
    same = all(abs(ys[k] - iss[k][ci]) < 0.005 for k in iss if k in ys)   # 센트 단위로 모두 같으면 "최대 0.000%" 대신 그렇게 적는다
    text = (f"운용사 과거 자료 파일의 종가와 {first}~{through} 날마다 대조("
            + ("모든 날 센트 단위까지 같음" if same else f"차이 최대 {abs(worst[1]) * 100:.3f}%, {worst[0]}") + ")"
            + (f" · 대조 제외 {len(exempt)}일(운용사 달력 표기 예외)" if exempt else "")
            + (f" · 마지막 {P} 종가는 운용사 게시 전이라 대조 전" if pending else ""))
    return "ok", text, info


# ---------- TLT(채권) — iShares 상품 페이지 ----------

NUM = r"(?:[0-9]{1,3}(?:,[0-9]{3})+|[0-9]+)(?:\.[0-9]+)?"   # 숫자 전체 형식 — 쉼표는 세 자리 구분만


def _ldjson_scripts(text):
    """HTML 파서로 실제 <script type="application/ld+json"> 요소의 내용만(주석 속 글자는 요소가 아니라 빠진다)."""
    from html.parser import HTMLParser

    class J(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=False)
            self.on, self.cur, self.out = False, [], []

        def handle_starttag(self, tag, attrs):
            if tag == "script" and dict(attrs).get("type") == "application/ld+json":
                self.on, self.cur = True, []

        def handle_endtag(self, tag):
            if tag == "script" and self.on:
                self.out.append("".join(self.cur))
                self.on = False

        def handle_data(self, data):
            if self.on:
                self.cur.append(data)

    j = J()
    j.feed(text)
    j.close()
    return j.out


def parse_ishares_fund(text, ticker):
    """iShares 상품 페이지 JSON-LD에서 ticker 펀드에 연결된 NAV(값·USD·기준일)와 12개월 분배수익률을 읽는다.
    조건: identifier에 {propertyID ticker, value ticker}가 있는 InvestmentFund가 정확히 하나(@id 비어 있지 않음), "NAV as of"를 가진
    요소가 정확히 하나이고 그 about.@id가 그 펀드 @id. 어긋나면 nav None과 why(구체 사유). NAV는 유한한 양수·단위 USD·날짜 파싱일 때만."""
    out = {"nav": None, "navDate": None, "ty": None, "tyAsOf": None, "why": None}
    graph = []
    for body in _ldjson_scripts(text):
        try:
            j = json.loads(body)
        except ValueError:
            continue
        for o in (j if isinstance(j, list) else j.get("@graph") or [j]):
            if isinstance(o, dict):
                graph.append(o)
    def is_fund(o):
        ty = o.get("@type")
        ty = ty if isinstance(ty, list) else [ty]
        ids = o.get("identifier") if isinstance(o.get("identifier"), list) else [o.get("identifier")]
        return "InvestmentFund" in ty and any(isinstance(i, dict) and i.get("propertyID") == "ticker" and i.get("value") == ticker for i in ids)
    funds = [o for o in graph if is_fund(o)]
    if len(funds) != 1 or not isinstance(funds[0].get("@id"), str) or not funds[0]["@id"].strip():
        out["why"] = f"페이지가 {ticker} 펀드를 가리키지 않음(펀드 객체 {len(funds)}개)"
        return out
    fid = funds[0]["@id"]
    navs = [o for o in graph if any(isinstance(p, dict) and p.get("name") == "NAV as of" for p in o.get("additionalProperty") or [])]
    if len(navs) != 1:
        out["why"] = f"NAV 요소가 {len(navs)}개"
        return out
    about = (navs[0].get("about") or {}).get("@id") if isinstance(navs[0].get("about"), dict) else None
    if not isinstance(about, str) or not about.strip() or about != fid:
        out["why"] = f"NAV 요소가 {ticker} 펀드에 연결돼 있지 않음"
        return out
    props = [p for p in navs[0]["additionalProperty"] if isinstance(p, dict)]
    def bundle(name, unit):
        hit = [p for p in props if p.get("name") == name]
        if len(hit) != 1:
            return None
        p = hit[0]
        ref = p.get("valueReference") if isinstance(p.get("valueReference"), dict) else {}
        v, dt_ = p.get("value"), ref.get("value") if ref.get("name") == "As of Dates" else None
        if unit is not None and p.get("unitText") != unit:
            return None
        if not isinstance(v, str) or not isinstance(dt_, str):
            return None
        pat = rf"({NUM})%" if unit is None else rf"({NUM})"   # 숫자 전체 문자열(수익률은 % 하나)
        mv = re.fullmatch(pat, v.strip())
        if not mv:
            return None
        try:
            x = float(mv.group(1).replace(",", ""))
            k = datetime.strptime(dt_.strip(), "%b %d, %Y").date().isoformat()
        except ValueError:
            return None
        return (x, k) if math.isfinite(x) else None
    nb = bundle("NAV as of", "USD")
    if not nb or not nb[0] > 0:
        out["why"] = "운용사 페이지에서 NAV를 읽지 못함(값·단위·날짜)"
        return out
    out["nav"], out["navDate"] = nb
    tb = bundle("12m Trailing Yield as of", None)
    if tb and 0 < tb[0] < 30:
        out["ty"], out["tyAsOf"] = tb[0] / 100, tb[1]
    return out


def _element_text(text, attr, value):
    """HTML 파서로 attr="value"인 요소를 찾아, 정확히 하나면 그 안 글자(주석·script·style 제외)를, 아니면 None."""
    from html.parser import HTMLParser
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    class B(HTMLParser):
        def __init__(self):
            super().__init__(convert_charrefs=True)
            self.stack, self.hits, self.cap, self.buf, self.skip = [], 0, None, [], 0

        def handle_starttag(self, tag, attrs):
            if any(k == attr and v == value for k, v in attrs):
                self.hits += 1
                if self.cap is None and tag not in VOID:
                    self.cap = len(self.stack)
            if tag in ("script", "style"):
                self.skip += 1
            if tag not in VOID:
                self.stack.append(tag)

        def handle_startendtag(self, tag, attrs):
            if any(k == attr and v == value for k, v in attrs):
                self.hits += 1

        def handle_endtag(self, tag):
            if tag in ("script", "style") and self.skip:
                self.skip -= 1
            if tag in self.stack:
                while self.stack:
                    t = self.stack.pop()
                    if self.cap is not None and len(self.stack) == self.cap:
                        # 대상 요소가 자기 닫는 태그로 닫혀야 정상 — 바깥 태그에 밀려 닫히면 깨진 블록
                        self.done, self.broken = (True, False) if t == tag else (False, True)
                        self.cap = None
                    if t == tag:
                        break

        def handle_data(self, data):
            if self.cap is not None and not self.skip:
                self.buf.append(data)

    b = B()
    b.done = b.broken = False
    b.feed(text)
    b.close()
    if b.hits != 1 or not b.done or b.broken:
        return None   # 요소가 없거나 둘 이상이거나 닫히지 않음
    return re.sub(r"\s+", " ", " ".join(b.buf))


BOND_METRICS = (("dur", "Effective Duration", "yrs"), ("wam", "Weighted Avg Maturity", "yrs"),
                ("ytm", "Average Yield to Maturity", "%"), ("n", "Number of Holdings", ""))


def parse_bond_metrics(text, P, prevP):
    """TLT 펀드 지표 블록(data-id="fundamentalsAndRisk-container", 페이지에 정확히 하나) 안 글자에서만 네 지표를 읽는다.
    지표 이름이 나올 때마다 후보 하나 — 뒤에 "값 단위 as of 날짜"가 오는지 검사, 하나라도 깨졌거나 서로 다른 묶음이 둘 이상이면 그 지표 None.
    반환 {키: (값, 기준일) | None}."""
    out = {k: None for k, _, _ in BOND_METRICS}
    plain = _element_text(text, "data-id", "fundamentalsAndRisk-container")
    if plain is None:
        return out
    for key, name, unit in BOND_METRICS:
        cands, bad = set(), False
        for m in re.finditer(re.escape(name) + r"(?! \()", plain):
            tail = plain[m.end():m.end() + 160]
            mm = re.match(rf" (?:More Info [^0-9\-]*?)?(-?{NUM})(?![0-9,.])(%| yrs|)\s*as of ([A-Z][a-z]{{2}} \d{{1,2}}, \d{{4}})(?![0-9A-Za-z])", tail)
            if not mm or mm.group(2).strip() != unit:
                bad = True
                break
            try:
                x = float(mm.group(1).replace(",", ""))
                k = datetime.strptime(mm.group(3), "%b %d, %Y").date().isoformat()
            except ValueError:
                bad = True
                break
            if not math.isfinite(x) or not (prevP <= k <= P):
                bad = True
                break
            if key == "n":
                ok = x == int(x) and x > 0 and "." not in mm.group(1)
            elif key in ("dur", "wam"):
                ok = x > 0
            else:
                ok = 0 < x < 30
            if not ok:
                bad = True
                break
            cands.add((x / 100 if unit == "%" else int(x) if key == "n" else x, k))
        if not bad and len(cands) == 1:
            out[key] = next(iter(cands))
    return out


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
    nav_date, hist = None, None
    if PROF["navKind"] == "gld_archive":
        # 표시 범위(page_nav와 같은 창)로 먼저 자르고 그 안에서만 날마다 대조 — 창 밖(2004~2014) 차이는 보지 않는다
        need = min(minus_months(d(S), 12 * YEARS_SHOWN).isoformat(), f"{int(S[:4]) - YEARS_SHOWN}-12-01")
        k0 = max(i for i, p in enumerate(series) if p[0] < need) if series[0][0] < need else 0
        series = series[k0:]
        cc, cc_text, hist = cross_check_gld(series, fred, S, prevP)
        if cc != "ok":
            raise Hold("cross_check" if cc == "mismatch" else "cross_unavailable", cc_text)
        fred = {series[0][0]: None}
    elif PROF["navKind"] == "page_nav":
        if asset() != "equity" and isinstance(fred, dict) and fred.get("why"):   # TLT: 상품 확인·NAV 읽기 실패의 구체 사유
            raise Hold("cross_unavailable", fred["why"])
        cc, cc_text = cross_check_page(series, fred, S, prevP)
        nav_date = (fred or {}).get("navDate") if cc == "ok" else None   # 홈 칸이 산문을 다시 읽지 않게 구조 칸으로
        if cc != "ok":
            raise Hold("cross_check" if cc == "mismatch" else "cross_unavailable", cc_text)
        # 대조 구간이 없으니 표시에 필요한 범위만: 사건 10년(P − 120개월)·월별 표(P 연도 −10년 12월) 중 이른 날의 직전 종가부터
        need = min(minus_months(d(S), 12 * YEARS_SHOWN).isoformat(), f"{int(S[:4]) - YEARS_SHOWN}-12-01")
        k0 = max(i for i, p in enumerate(series) if p[0] < need) if series[0][0] < need else 0
        series = series[k0:]
        fred = {series[0][0]: None}   # 아래 공통 경로가 min(fred)로 자르는 자리 — 같은 첫 날
    elif PROF["navKind"] == "invesco":
        cc, cc_text, fred = cross_check_invesco(series, fred, S, prevP)
    else:
        cc, cc_text = (cross_check_nav if PROF["navKind"] == "ssga" else cross_check)(series, fred, S, prevP)
    if cc != "ok":
        raise Hold("cross_check" if cc == "mismatch" else "cross_unavailable", cc_text)
    series = [p for p in series if p[0] >= min(fred)]   # 대조된 구간만(그 앞 Yahoo 값은 쓰지 않는다; fred = 대조 자료 — SPY·QQQ는 NAV)
    if PROF["key"] != "SP500":   # 표시가 쓰는 구간이 대조 구간 안에 있어야(QQQ NAV는 회전 창 — 매 실행 실제 첫 날로 판단)
        # 월별 10년 표의 첫 해(P 연도 −9) 직전 12월 말 종가가 있어야 한다 — 5년 수익률 기준일은 그보다 늦다.
        # 사건(최근 10년)은 구간 앞을 자를 뿐 기준 종가가 필요 없어 보지 않는다(월초 주말 하루 차이로 헛보류하지 않게, QQQ 구현 dr r1).
        dec = f"{int(S[:4]) - YEARS_SHOWN}-12"
        if not any(k.startswith(dec) for k, _ in series):
            raise Hold("short", f"대조 구간 첫 날 {series[0][0]} — 월별 표에 필요한 {dec} 말 종가가 없다")
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
            "crossCheck": {"status": cc, "text": cc_text, **({"navDate": nav_date} if nav_date else {}),
                           **({k: hist[k] for k in ("since", "checkedThrough", "pendingDate", "maxGap", "maxGapDate", "exempt")} if hist else {})},
            **({"gold": {"oz": hist["oz"], "tonnes": hist["tonnes"], "asOf": hist["ozAsOf"]}} if hist else {})}


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
            f'낙폭·회복의 고점과 최고 종가는 {PROF["span"].format(since=kdate(res["since"]))} 안에서만 본다 — 그 앞 값은 쓰지 않는다. '
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


# ICB 산업 11개(QQQ, Invesco 펀드 업종) — GICS(SPY)와 다른 분류라 색도 따로(이름마다 고정, 사용자 결정 2026-10-21)
ICB_KO = {"Technology": ("기술", "#0f766e"), "Telecommunications": ("통신", "#14b8a6"), "Health Care": ("헬스케어", "#e11d48"),
          "Financials": ("금융", "#b45309"), "Real Estate": ("부동산", "#a16207"), "Consumer Discretionary": ("경기소비재", "#ea580c"),
          "Consumer Staples": ("필수소비재", "#f59e0b"), "Industrials": ("산업재", "#475569"), "Basic Materials": ("기초소재", "#78716c"),
          "Energy": ("에너지", "#7c2d12"), "Utilities": ("유틸리티", "#0369a1")}


def parse_invesco_sectors(text):
    """Invesco weightedHoldings(breakdown=sector) — ICB 산업, 펀드 기준, 월말. 목록 밖 이름·합 99.5~100.5 밖이면 예외(그 칸만 비움)."""
    v = json.loads(text)
    rows = [(x["name"], float(x["value"])) for x in v["holdingWeights"]]
    if not rows or any(n not in ICB_KO for n, _ in rows) or len({n for n, _ in rows}) != len(rows) or not all(0 <= w <= 100 for _, w in rows):
        raise ValueError("업종 칸 모양이 다름")
    if abs(sum(w for _, w in rows) - 100) > 0.5:
        raise ValueError("업종 합이 100%가 아님")
    return {"asOf": datetime.strptime(v["effectiveDate"], "%Y-%m-%d").date().isoformat(), "rows": sorted(rows, key=lambda r: -r[1]), "kind": "icb"}


def parse_invesco_chars(text):
    """Invesco fundCharacteristics — priceToEarningsRatio(펀드, 가중 조화평균, trailing)와 기준일. 3~100배 밖이면 예외."""
    v = json.loads(text)
    pe = v.get("priceToEarningsRatio")
    if not isinstance(pe, (int, float)) or isinstance(pe, bool) or not 3 < pe < 100:
        raise ValueError("PER 범위가 이상함")
    return {"pe": float(pe), "peAsOf": datetime.strptime(v["effectiveDate"], "%Y-%m-%d").date().isoformat()}


def parse_sectors(text, count=11):
    """펀드 페이지의 <input id="index-sector-breakdown">. GICS 이름 count개(SPY 11, DIA 9 — 프로필 sectorCount), 이름은 GICS 11개 안,
    중복 없음, 비중마다 0~100, 합 99.5~100.5%가 아니면 예외."""
    m = re.search(r'<input type="hidden" id="index-sector-breakdown" value="(\{.*?\})"\s*/>', text, re.S)
    if not m:
        raise ValueError("index-sector-breakdown 없음")
    v = json.loads(html.unescape(m.group(1)))
    rows = [(a["name"]["value"], float(a["weight"]["originalValue"])) for a in v["attrArray"]]
    if (len(rows) != count or len({n for n, _ in rows}) != count or not {n for n, _ in rows} <= set(SECTOR_KO)
            or not all(0 <= w <= 100 for _, w in rows)):
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
    sec, spy = c.get("sectors"), c.get("holdings") or c.get("spy")   # "holdings" = 그 ETF 보유(2026-10-21 이름 바꿈, 옛 키 "spy"도 읽음)
    parts = ['  <div class="section-title">구성 종목 — 무엇으로 이루어져 있나</div>\n'
             f'  <div class="lede">{PROF["lede"]}</div>']
    if sec:
        # 도넛(가운데 "11개 · 업종 · 날짜") + 오른쪽 색 막대 범례(가장 큰 업종을 끝으로). 색은 비중 순위로 정해 밝기가 서로 다르다.
        tot, stops, legend, mx = sum(w for _, w in sec["rows"]), [], [], sec["rows"][0][1]
        acc = 0.0
        icb = sec.get("kind") == "icb"
        cols = [ICB_KO[n][1] for n, _ in sec["rows"]] if icb else SECTOR_COLORS
        for (n, w), c in zip(sec["rows"], cols):
            a0, acc = acc, acc + w / tot * 100
            stops.append(f"{c} {a0:.2f}% {acc:.2f}%")
            legend.append(f'<span class="sw" style="background:{c}"></span><span>{ICB_KO[n][0] if icb else SECTOR_KO[n]}</span>'
                          f'<span class="sb"><i style="width:{w / mx * 100:.1f}%;background:{c}"></i></span><b>{w:.1f}%</b>')
        top3 = sum(w for _, w in sec["rows"][:3])
        title = f'업종 비중 (ICB, 펀드 기준)' if icb else f'업종 비중 (GICS {len(sec["rows"])}개)'
        note = (f'Invesco가 공개하는 QQQ 펀드 업종 비중 — ICB 분류(Invesco, 펀드 기준) · GICS(SPY·DIA 카드)와 직접 비교 불가 · {kdate(sec["asOf"])} 기준. 막대는 가장 큰 업종을 끝으로 맞춘 길이.'
                if icb else f'State Street {PROF["etf"]} 펀드 페이지의 지수 업종 비중, {kdate(sec["asOf"])} 기준. 막대는 가장 큰 업종을 끝으로 맞춘 길이.')
        parts.append(f'  <div class="card"><div class="pie-head"><div class="card-title">{title}</div><span class="sub">상위 3개 업종 {top3:.1f}%</span></div>'
                     f'<div class="pie-wrap"><div class="pie" role="img" aria-label="업종 비중 도넛 그래프" style="background:conic-gradient({", ".join(stops)})">'
                     f'<div class="pie-hole"><b>{len(sec["rows"])}개</b><span>업종 · {kdate(sec["asOf"])}</span></div></div>'
                     f'<div class="pie-legend">{"".join(legend)}</div></div>'
                     f'<div class="note">{note}</div></div>')
    else:
        parts.append('  <div class="card"><div class="card-title">업종 비중</div><div class="note">운용사 자료에서 업종 비중을 불러오지 못했다.</div></div>')
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
                     f'<div class="note">{k}개 합계 {top_sum * 100:.1f}%' + (f' ({PROF["etf"]} 자료에 10개가 다 오지 않았다)' if k != 10 else "") + f'. {PROF["etf"]} 보유 파일 {kdate(spy["S"] or "—")} 기준, {PROF["nonEqText"]}을 뺀 주식 비중(같은 회사의 여러 주식은 합침). '
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
                    f'<div class="note">막대 = {PROF["etf"]} 주식 비중을 그 회사 카드의 판정으로 나눈 것. 제목의 비중은 판정 보류·그 밖 제외 카드까지 포함한다 '
                    '(카드 판정 탭의 "덮은 비중"은 판정이 있는 카드만). 카드 없는 회사는 대부분 작은 회사들이다.</div>')
        else:
            why = (f' {PROF["etf"]} 판정 보류' + (f'({html.escape(spy["reasonText"])})' if spy.get("reasonText") else "")
                   + '라 판정별 비중 막대는 뺐다.') if spy.get("held") else ""
            head = (f'<div class="card-title">이 사이트에 카드가 있는 종목 {len(spy["cards"])}개</div>'
                    + (f'<div class="note">{why.strip()}</div>' if why else ""))
        parts.append(f'  <div class="card">{head}<details class="fold-in"><summary>종목 보기</summary>{chips_html}</details></div>')
    else:
        parts.append(f'  <div class="card"><div class="card-title">상위 10개 회사</div><div class="note">{PROF["etf"]} 보유 자료를 불러오지 못했다.</div></div>')
    return "\n".join(parts)


def safe_holdings(res):
    """구성 종목 탭은 지수 시세와 따로다 — 그리다 실패해도 이 탭만 비우고 카드는 그대로 낸다."""
    try:
        return render_holdings(res)
    except Exception:   # noqa: BLE001
        traceback.print_exc()
        return ('  <div class="section-title">구성 종목</div>\n'
                '  <div class="card"><div class="note">구성 종목 자료를 그리지 못했다.</div></div>')


# etf_daily.CHECK_KEYS와 같은 칸 — 카드 페이지에도 판정 원본의 이 칸들을 심어 대조 단계(v2/etf/etf_consistency.py)가 세 산출물을 맞춰 본다
VERDICT_CHECK_KEYS = ("status", "reason", "verdict", "nbar", "coverage", "range", "bar", "S", "builtFor", "ruleVersion", "pending")


def verdict_attr(full):
    d = {k: full.get(k) for k in VERDICT_CHECK_KEYS} if isinstance(full, dict) else {}
    return html.escape(json.dumps(d, ensure_ascii=False), quote=True)


def render_verdict(full, P):
    """ETF 카드의 "카드 판정" 탭 — v2/etf/<ETF>.json(etf_daily.py)을 그대로 옮긴다. 규칙: v2/research/etf_verdict_prereg.md.
    홈 줄과 같은 묵음 규칙: 판정 세션(builtFor)이 홈 세션 P와 다르면 판정을 지우고 사유만(운용사 파일 갱신 대기는 예외)."""
    E = PROF["etf"]
    head = f'  <div class="section-title">카드 판정 — 이 사이트 카드로 본 {E}</div>\n'
    lede = (f'  <div class="lede">{E}가 담은 종목 중 이 사이트에 카드가 있는 종목의 판정을 보유 비중으로 평균한 것이다. '
            f'{E}나 지수 자체의 내재가치 평가가 아니다. 참고용 · 매수 기준 아님 · 예측 신호로 검증되지 않음.</div>\n')
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
        try:   # 상위 10개 중 판정에 쓴 카드의 비중 ÷ 덮은 비중(SPY 10-16 51.3%처럼 ETF마다 다르다 — 고정 문구 대신 계산)
            top_share = sum(t["weight"] for t in full["top10"] if t.get("card") and t.get("n") is not None) / cov
            top_share = top_share if 0 <= top_share <= 1 else None
        except Exception:   # noqa: BLE001
            top_share = None
        ex = full.get("expense") if isinstance(full.get("expense"), dict) else {}
        if not (fin(ex.get("pct")) and isinstance(ex.get("url"), str) and isinstance(ex.get("source"), str)):
            ex = {}   # 보수·출처가 이상하면 그 안내만 뺀다(판정은 그대로)
        src = (f'보유 비중: {html.escape(full.get("holdingsSource") or "State Street")} (기준일 {kdate(full["S"])}) — 원본 파일은 다시 게시하지 않는다. '
               f'카드 판정: 이 사이트 v2 카드, {kdate(full["builtFor"])} 종가. 규칙 {html.escape(str(full.get("ruleVersion") or "—"))}.'
               + (f' 보수율 {ex["pct"]:.4f}% — <a href="{html.escape(ex["url"], quote=True)}">{html.escape(ex["source"])}</a>.' if ex.get("pct") is not None and ex.get("url") else ""))
        return (head + lede
                + f'  <div class="card"><div class="ret-strip verdict-strip">{strip}</div></div>\n'
                + f'  <div class="card"><div class="card-title">등급별 보유 비중</div><div class="vbar" role="img" aria-label="등급별 보유 비중">{segs}</div>'
                  f'<div class="vbar-lab">{labs}</div><div class="note">분모는 {PROF["nonEqText"]}을 뺀 보유 비중 전체(분류 안 된 비중 포함, 파생상품 노출은 평가하지 않음). 상위 10개 회사와 종목별 판정은 구성 종목 탭에 있다.</div></div>\n'
                + '  <div class="card"><div class="card-title">읽는 법과 한계</div><div class="note">카드 점수는 −4(고평가 쪽)부터 +3(저평가 쪽)까지라 비대칭이다 — '
                  '현금흐름 "매우 싸다"도 +1만 주기 때문에 평균은 아래로 기운다. 평균은 극단을 지우므로 막대를 함께 본다. '
                  + (f'상위 10개 회사가 판정에 쓴 비중의 {top_share * 100:.0f}%를 차지한다. ' if top_share is not None else '')
                  + '카드가 없는 종목은 대부분 지수의 작은 쪽이라 이 점수는 대형주 평균에 가깝다.</div>'
                  f'<div class="note">{src}</div></div>')
    except Exception:   # noqa: BLE001 — 판정 탭만 비우고 카드는 낸다
        traceback.print_exc()
        return box("판정 보류", "판정 자료를 그리지 못했다.")


def render_no_verdict():
    """판정 없는 가격 카드(IWM·TLT·GLD)의 "카드 판정" 탭 — 하지 않는 이유만(덮은 비중은 재지 못했으니 숫자를 말하지 않는다)."""
    E = PROF["etf"]
    if PROF.get("noVerdictText"):
        return (f'  <div class="section-title">카드 판정 — 판정하지 않음</div>\n'
                f'  <div class="card held-box"><div class="card-title">판정하지 않음</div><div class="note">{PROF["noVerdictText"]}</div></div>')
    return (f'  <div class="section-title">카드 판정 — 판정하지 않음</div>\n'
            f'  <div class="card held-box"><div class="card-title">판정하지 않음</div><div class="note">'
            f'{E}는 미국 소형주 약 2,000개를 담는다 — 카드 판정을 보유 비중으로 평균하는 방식은 이렇게 많은 소형 종목에 맞지 않는다(사용자 결정 2026-10-21). '
            '운용사 보유 파일도 자동으로 받지 못해 이 사이트 카드가 그 비중을 얼마나 덮는지 잴 수 없다. '
            '그래서 SPY·QQQ·DIA처럼 카드 판정을 보유 비중으로 평균하지 않는다. 이 카드는 가격·수익률만 보여 준다.</div></div>')


def fee_html():
    lab, src, url = PROF["fee"]
    return f'{lab}(<a href="{html.escape(url, quote=True)}">{src}</a>)'


def head_common(by):
    return [meta_item("1년 수익률", pct(by["1년"]["ret"]), color(by["1년"]["ret"]), PROF["closeNote"], f'기준 {kdate(by["1년"]["base"])} 종가'),
            meta_item("5년 연 환산", pct(by["5년"]["annual"]), color(by["5년"]["annual"]), f'5년 누적 수익률을 1년마다로 바꾼 값({PROF["retBasis"]})',
                      f'5년 누적 {pct(by["5년"]["ret"])}')]


def render_head_gold(res, by):
    """GLD 머리: 1년·5년 + 1주당 금·보유 금(운용사 공개 자료, P 이하 마지막 대조일 값). 못 읽은 칸은 "—"(대체값 없음)."""
    g = res.get("gold") or {}
    oz, tn, asof = g.get("oz"), g.get("tonnes"), g.get("asOf")
    src = f'SPDR Gold Trust 공개 자료 {kdate(asof)}' if asof else "불러오지 못함"
    gold_note = (f'GLD 한 주의 거래 가격이다. 금 1온스 값이 아니다 — 1주에 든 금은 {oz:.4f}온스이고, 비용 충당으로 1주에 든 금은 조금씩 줄어든다.'
                 if oz else 'GLD 한 주의 거래 가격이다. 금 1온스 값이 아니다 — 1주에 든 금은 1온스보다 적고, 비용 충당으로 조금씩 줄어든다.')
    return "\n".join(head_common(by) + [
        meta_item("1주당 금", f'{oz:.4f}온스' if oz else "—", "var(--text)", "운용사가 공개하는 1주당 금 보유량(Ounces of Gold per Share)", src),
        meta_item("보유 금", f'{tn:,.1f}톤' if tn else "—", "var(--text)", "신탁이 보유한 금 전체(Tonnes of Gold)", src),
        f'    <div style="grid-column:1 / -1;font-size:11px;color:var(--text3);">{gold_note} {fee_html()}. 분배금은 없다.</div>'])


def render_head_bond(res, by):
    """TLT 머리: 1년·5년 + 평균 만기수익률·유효 듀레이션(iShares 지표 블록). 미 국채 금리와 나란히 두지 않는다. 못 읽은 칸·문장은 뺀다."""
    b = (res.get("constituents") or {}).get("bond") or {}
    ytm, dur, wam, n, ty = b.get("ytm"), b.get("dur"), b.get("wam"), b.get("n"), b.get("ty")
    sub = lambda x: f'iShares {kdate(x[1])}' if x else "불러오지 못함"
    extra = [f'12개월 분배수익률 {ty[0] * 100:.2f}%(NAV 기준, iShares {kdate(ty[1])})' if ty else None,
             f'보유 {n[0]:,}종목(iShares {kdate(n[1])})' if n else None,
             f'가중 평균 만기 {wam[0]:.2f}년(iShares {kdate(wam[1])})' if wam else None, fee_html()]
    return "\n".join(head_common(by) + [
        meta_item("평균 만기수익률", f'{ytm[0] * 100:.2f}%' if ytm else "—", "var(--text)",
                  "iShares Average Yield to Maturity — 보유 채권의 가중 평균, 보수 차감 전. 펀드는 만기가 없어 확정 수익이 아니다", sub(ytm)),
        meta_item("유효 듀레이션", f'{dur[0]:.2f}년' if dur else "—", "var(--text)",
                  (f"장기 국채 수익률이 고르게 1%p 오를 때 가격이 약 {round(dur[0])}% 내린다는 1차 근사(iShares Effective Duration)" if dur else ""), sub(dur)),
        '    <div style="grid-column:1 / -1;font-size:11px;color:var(--text3);">' + " · ".join(x for x in extra if x) + '. '
        '수익률은 분배금 수령·재투자를 넣지 않은 시장 가격 기준이다. TLT는 매달 분배금을 준다. '
        '<b>과거 종가는 운용사 자료와 대조하지 못했다 — 최근 하루 NAV만 확인.</b></div>'])


def sources_other(cc):
    if asset() == "gold":
        return (f'시세: Yahoo Finance GLD 일봉(시장 가격, 분배금 없음). 종가를 SPDR Gold Trust(스폰서 World Gold Trust Services) {cc}. '
                '시가·고가·저가(캔들과 차트의 최고·최저 표시)는 Yahoo 값 그대로다(대조하지 않음). 운용사 파일은 다시 게시하지 않고, 금 현물 가격은 싣지 않는다.')
    return (f'시세: Yahoo Finance TLT 일봉(시장 가격, 분배금 제외). {cc}. 시가·고가·저가도 Yahoo 값 그대로다. '
            '만기수익률·듀레이션·가중 평균 만기·분배수익률·보유 수는 iShares 상품 페이지의 TLT 지표, 각 기준일.')


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
              "NAVEXTRA": ('<button class="nav-btn" onclick="showSection(\'verdict\', this)">⚖️ 카드 판정</button>' if PROF["verdict"] else
                           '<button class="nav-btn" onclick="showSection(\'verdict\', this)">⚖️ 판정하지 않음</button>' if PROF.get("noVerdict") else ""),
              # 구성 종목 탭은 상위 보유·업종을 읽을 수 있는 카드만(IWM은 숨김 — 운용사 자료를 확보하지 못함)
              "HOLDINGSNAV": ("" if PROF["navKind"] == "page_nav" or asset() != "equity" else '<button class="nav-btn" onclick="showSection(\'holdings\', this)">🧩 구성 종목</button>'),
              "VERDICT": (f'<div id="verdict" class="section" data-etf="{verdict_attr(res.get("verdictData"))}">\n'
                          f'{render_verdict(res.get("verdictData"), res.get("builtFor"))}\n</div>' if PROF["verdict"] else
                          f'<div id="verdict" class="section">\n{render_no_verdict()}\n</div>' if PROF.get("noVerdict") else "")}
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
    if asset() != "equity":   # 금·채권: 보유·PER·국채 칸을 만들지 않는다(주식형 경로는 아래 그대로)
        meta = render_head_gold(res, by) if asset() == "gold" else render_head_bond(res, by)
        dl = res["daily"]
        m = dict(common, PRICE=price, META=meta, CHART=fill(CHART_HTML, common), RETURNS=render_returns(res),
                 MONTHLY=render_monthly(res), EVENTS=render_events(res), HOLDINGS="", SOURCES=sources_other(cc),
                 DAILY=json.dumps(dl["rows"], separators=(",", ":")), MA=json.dumps(dl["ma"], separators=(",", ":")),
                 RANGE_BASE=json.dumps(dl["base"]))
        return fill(head, m) + fill(body, m)
    cons = res.get("constituents") or {}
    ch, tsy = cons.get("chars"), cons.get("dgs10")
    na = "불러오지 못함"
    ey_val = (f'{100 / ch["pe"]:.2f}%' if ch else "—") + " · " + (f'{tsy["value"] * 100:.2f}%' if tsy else "—")
    fund_pe = PROF["navKind"] in ("invesco", "page_nav")   # QQQ·IWM: 펀드 PER(운용사) — SPY·DIA는 지수 PER(SSGA), 라벨·출처 줄로 구분
    src = {"invesco": "Invesco", "page_nav": "iShares"}.get(PROF["navKind"], "SSGA")
    pe_tip = {"invesco": "Invesco QQQ 펀드 특성 Price/earnings ratio — Invesco 페이지 설명: 가중 조화평균(Weighted Harmonic Average), 월말",
              "page_nav": "iShares 상품 페이지 P/E Ratio — 페이지 설명: 보유 종목마다 최근 종가 ÷ 최근 회계연도 EPS, 음수 PER 제외(펀드 기준)"}.get(
        PROF["navKind"], f"State Street {PROF['etf']} 펀드 페이지 Index Characteristics: Price/Earnings(페이지에 계산 정의 없음)")
    ey_sub = (((f'펀드 PER{"(적자 종목 제외)" if PROF["navKind"] == "page_nav" else ""} {kdate(ch["peAsOf"])}' if fund_pe else f'SSGA {kdate(ch["peAsOf"])}') if ch else "PER 불러오지 못함") + " / "
              + (f'FRED {kdate(tsy["date"])}' if tsy else "국채 불러오지 못함"))
    meta = "\n".join([
        meta_item("1년 수익률", pct(by["1년"]["ret"]), color(by["1년"]["ret"]), PROF["closeNote"],
                  f'기준 {kdate(by["1년"]["base"])} 종가'),
        meta_item("5년 연 환산", pct(by["5년"]["annual"]), color(by["5년"]["annual"]), "5년 누적 수익률을 1년마다로 바꾼 값(배당 제외)",
                  f'5년 누적 {pct(by["5년"]["ret"])}'),
        meta_item("PER (펀드, 적자 종목 제외)" if PROF["navKind"] == "page_nav" else "PER (펀드)" if fund_pe else "PER (지수)", f'{ch["pe"]:.1f}배' if ch else "—", "var(--text)",
                  pe_tip,
                  f'{src} {kdate(ch["peAsOf"])}' if ch else na),
        meta_item("이익수익률 · 미 10년 국채", ey_val, "var(--text)",
                  f"이익수익률 = 1 ÷ PER({src} {'펀드' if fund_pe else 'Price/Earnings'}). 미 10년 국채 = FRED DGS10. 두 숫자를 나란히 둘 뿐, 판정이 아니다", ey_sub),
        '    <div style="grid-column:1 / -1;font-size:11px;color:var(--text3);">PER과 이익수익률은 오늘 값이라 과거와 비교하지 않는다. 이 값만으로 저평가·고평가를 판정하지 않는다.'
        + ((f' 보유 {cons["count"]["holdings"]:,}종목(iShares, {kdate(cons["count"]["holdingsAsOf"])}) — 상위 보유·업종 자료는 싣지 않는다.'
            if (cons.get("count") or {}).get("holdings") else " 상위 보유·업종 자료는 싣지 않는다.") if PROF["navKind"] == "page_nav" else "")
        + (' <b>과거 종가는 운용사 자료와 대조하지 못했다 — 최근 하루 NAV만 확인.</b>' if PROF["navKind"] == "page_nav" else "") + '</div>',
    ])
    dl = res["daily"]
    m = dict(common, PRICE=price, META=meta, CHART=fill(CHART_HTML, common), RETURNS=render_returns(res),
             MONTHLY=render_monthly(res), EVENTS=render_events(res), HOLDINGS=safe_holdings(res),
             SOURCES=((f'시세: Yahoo Finance {PROF["symText"]} 일봉(시장 가격, 배당 제외). 종가를 State Street가 공시하는 {PROF["etf"]} NAV 이력과 대조 — 최근 250세션 ±1%, 그 앞 ±2% 안 확인 — {cc}. '
                       '시가·고가·저가(캔들과 차트의 최고·최저 표시)는 NAV 이력에 없어 Yahoo 값 그대로다.') if PROF["navKind"] == "ssga" else
                      (f'시세: Yahoo Finance IWM 일봉(시장 가격, 배당 제외). {cc}. 시가·고가·저가도 Yahoo 값 그대로다.') if PROF["navKind"] == "page_nav" else
                      (f'시세: Yahoo Finance QQQ 일봉(시장 가격, 배당 제외). 종가를 Invesco가 공개하는 QQQ NAV와 대조 — 최근 {RECENT_EXACT}거래일 ±{NAV_RECENT_TOL * 100:g}%, 그 앞 ±{NAV_OLD_TOL * 100:g}% 안 확인 — {cc}. '
                       '거래일은 NYSE 휴장일 규칙으로 정한다. 시가·고가·저가는 NAV에 없어 Yahoo 값 그대로다.') if PROF["navKind"] == "invesco" else
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


def price_summary(res, P, prevP=None):
    """홈 데이터 가격형 칸(kind price). 정상이면 종가·하루 등락·1년 수익률·대조 정보, 아니면 보류 사유만.
    check: "day"(IWM·TLT — 최근 하루 NAV, navDate) / "history"(GLD — since~checkedThrough 날마다, pendingDate). prevSession은 홈 직전 세션."""
    hist = PROF["navKind"] == "gld_archive"
    base = {"etf": PROF["etf"], "kind": "price", "status": res["status"], "builtFor": res.get("builtFor") or P, "S": res.get("S"),
            "check": "history" if hist else "day", "prevSession": prevP}
    if res["status"] != "ok":
        return dict(base, reasonText=res.get("reasonText") or "자료 보류")
    if res.get("prevSession") != prevP:
        raise ValueError(f"직전 세션 불일치 {res.get('prevSession')} · {prevP}")
    by = {r["label"]: r for r in res["returns"]}
    cc = res.get("crossCheck") or {}
    out = dict(base, close=res["close"], chg=res["chg"], ret1y=by["1년"]["ret"])
    if hist:
        return dict(out, since=cc.get("since"), checkedThrough=cc.get("checkedThrough"), pendingDate=cc.get("pendingDate"))
    return dict(out, navDate=cc.get("navDate"))


def write_home_price(out, res, P, prevP=None):
    sys.path.insert(0, str(ROOT / "v2" / "etf"))
    import etf_daily as ED   # noqa: E402 — 홈 데이터 파일 읽기·쓰기 규칙을 같이 쓴다(다른 칸을 지우지 않게)
    d_ = out / "preview-only-etf-data.js"
    data = ED.read_data_js(d_)
    data[PROF["etf"]] = price_summary(res, P, prevP)
    ED.write_atomic(d_, "// preview 전용 ETF 요약(v2/etf/etf_daily.py가 쓴다 — 손으로 고치지 않는다; 가격형 칸은 v2/index/index_daily.py)\n"
                        f"{ED.DATA_PREFIX}{json.dumps(data, ensure_ascii=False)};\n")


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
    ap.add_argument("--inv-sectors", help="Invesco 업종 JSON 파일(시험용, --card QQQ)")
    ap.add_argument("--inv-chars", help="Invesco 펀드 특성 JSON 파일(시험용, --card QQQ)")
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
            if PROF["navKind"] == "ssga":   # 대조 자료 = 운용사 NAV 이력
                fred = parse_navhist(Path(a.fred).read_bytes() if a.fred else fetch_navhist(PROF["navFile"]))
            elif PROF["navKind"] == "gld_archive":   # 운용사 과거 자료 xlsx — 모양이 다르면 그 사유를 대조 못 함 사유로
                try:
                    fred = parse_gld_archive(Path(a.fred).read_bytes() if a.fred else fetch_gld_archive())
                except Exception as e:   # noqa: BLE001
                    fred = {"err": f"{type(e).__name__}: {e}"[:200]}
            elif PROF["navKind"] == "page_nav" and asset() == "bond":   # TLT: 펀드에 연결된 JSON-LD 요소에서만 NAV(원문은 지표에도 쓴다)
                ptext = Path(a.fred).read_text(encoding="utf-8") if a.fred else http_get(PROF["page"])
                fred = parse_ishares_fund(ptext, PROF["ticker"])
            elif PROF["navKind"] == "page_nav":   # 운용사 상품 페이지에서 최근 하루 NAV(+ PER·보유 수)
                fred = parse_ishares_page(Path(a.fred).read_text(encoding="utf-8") if a.fred else http_get(PROF["page"]))
            elif PROF["navKind"] == "invesco":   # 날짜·값 쌍 그대로(중복·이상값은 대조가 "NAV 형식 변경"으로)
                fred = parse_invesco_nav(Path(a.fred).read_text(encoding="utf-8") if a.fred else fetch_invesco("/navs?idType=cusip&productType=ETF"))
            else:
                fred = parse_fred(Path(a.fred).read_text(encoding="utf-8") if a.fred else fetch_fred())
            if not fred:
                fred = None
        except Exception:
            fred = None
        res = compute(series, fred, P, prevP, ohlc)
        selfcheck(res, [p for p in series if p[0] <= P])
        if asset() != "equity":   # 금·채권: 보유·SSGA 페이지·업종·PER·DGS10을 읽지 않는다
            cons = {"holdings": None, "sectors": None, "chars": None}
            if asset() == "bond":   # 대조에 쓴 같은 페이지 원문에서(다시 받지 않는다)
                try:
                    bm = parse_bond_metrics(ptext, P, prevP)
                except Exception:   # noqa: BLE001 — 지표만 비운다(NAV 대조는 그대로)
                    traceback.print_exc()
                    bm = {k: None for k, _, _ in BOND_METRICS}
                ty, tya = fred.get("ty"), fred.get("tyAsOf")
                bm["ty"] = (round(ty, 6), tya) if ty is not None and tya and prevP <= tya <= P else None
                cons["bond"] = bm
            res["constituents"] = cons
            raise _Done()
        cons = {"holdings": read_spy(a.spy or out / (PROF["verdictJson"] or "v2/etf/SPY.json")) if PROF["navKind"] != "page_nav" else None,
                "sectors": None, "chars": None}
        page = ""
        if PROF["navKind"] == "page_nav":   # PER·보유 수는 대조에 쓴 같은 페이지에서(따로 받지 않는다)
            info = fred if isinstance(fred, dict) else {}
            cons["chars"] = {"pe": info["pe"], "peAsOf": info["peAsOf"]} if info.get("pe") else None
            cons["count"] = {"holdings": info.get("holdings"), "holdingsAsOf": info.get("holdingsAsOf")}
        elif PROF["navKind"] != "invesco":
            try:   # 운용사 페이지 실패는 그 칸들만 비운다
                page = Path(a.ssga_page).read_text(encoding="utf-8") if a.ssga_page else http_get(PROF["page"])
            except Exception:   # noqa: BLE001
                page = ""
        try:   # 미 10년 국채(FRED DGS10): S 이하 마지막 값. 실패하면 그 값만 비운다
            dg = parse_fred(Path(a.dgs10).read_text(encoding="utf-8") if a.dgs10 else fetch_fred("DGS10"))
            k = max(d_ for d_ in dg if d_ <= res["S"])
            cons["dgs10"] = {"date": k, "value": round(dg[k] / 100, 6)} if 0 < dg[k] < 20 else None
        except Exception:   # noqa: BLE001
            cons["dgs10"] = None
        if PROF["navKind"] == "invesco":   # 업종(ICB)·PER(펀드) — 실패하면 그 칸만 비운다
            for key, fn, path_, arg in (("sectors", parse_invesco_sectors, "/weightedHoldings/fund?idType=cusip&breakdown=sector&productType=ETF", a.inv_sectors),
                                        ("chars", parse_invesco_chars, "?expand=nav&idType=cusip&variationType=fundCharacteristics&productType=ETF", a.inv_chars)):
                try:
                    cons[key] = fn(Path(arg).read_text(encoding="utf-8") if arg else fetch_invesco(path_))
                except Exception:   # noqa: BLE001
                    cons[key] = None
        elif PROF["navKind"] != "page_nav":
            for key, fn in (("sectors", lambda t: parse_sectors(t, PROF["sectorCount"])), ("chars", parse_chars)):
                try:
                    cons[key] = fn(page)
                except Exception:   # noqa: BLE001
                    cons[key] = None
        res["constituents"] = cons
    except _Done:
        pass
    except Hold as h:
        res = {"status": "held", "reason": h.reason, "reasonText": REASON_TEXT[h.reason], "detail": h.detail,
               "builtFor": P, "S": None}
    except Exception as e:   # noqa: BLE001 — 어떤 실패도 보류로 쓰고 종목 게시는 막지 않는다
        traceback.print_exc()
        res = {"status": "held", "reason": "run_fail", "reasonText": REASON_TEXT["run_fail"],
               "detail": type(e).__name__, "builtFor": P, "S": None}
    res["index"], res["name"] = PROF["key"], PROF["name"]
    r_id = os.environ.get("GITHUB_RUN_ID")   # 알림이 이번 실행 산출물인지 가린다(가격형 카드 보류 알림, 2026-10-21)
    res["runId"] = f"{r_id}.{os.environ.get('GITHUB_RUN_ATTEMPT', '1')}" if r_id else None
    res["runAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    res["source"] = f'Yahoo Finance {PROF["symText"]} 일봉 종가'
    if PROF["verdict"]:   # 판정 탭: 시세가 보류여도 판정은 따로 보인다
        try:
            res["verdictData"] = json.loads((Path(a.spy) if a.spy else out / PROF["verdictJson"]).read_text(encoding="utf-8"))
        except Exception:   # noqa: BLE001
            res["verdictData"] = None
    res, page = pages_for(res, P)
    public = {k: v for k, v in res.items() if k not in ("daily", "verdictData")}   # 캔들 자료는 페이지 안에만, 판정은 SPY.json에 이미 있다
    files = {out / PROF["json"]: json.dumps(public, ensure_ascii=False, indent=1) + "\n"}
    if page is not None:
        files[out / PROF["html"]] = page
    if PROF.get("homePrice"):
        # 가격 카드(판정 단계 없음): ① 홈 칸 → ② 카드 HTML → ③ 카드 JSON. JSON(runId)이 "이번 실행이 끝까지 썼다"는 표시라 맨 마지막 —
        # 앞이 실패하면 뒤를 쓰지 않고 멈춘다. 알림(etf_alerts run_price)은 JSON runId가 이번 실행이 아니면 "갱신 실패"를 연다(설계 dr r3~r5).
        try:
            if page is None:   # 가격 카드는 틀 없는 최소 페이지까지 늘 만든다 — 없으면 완료 표시(JSON)를 쓰지 않는다
                raise RuntimeError("카드 페이지 없음")
            write_home_price(out, res, P, prevP)
            write_all({out / PROF["html"]: page})
            write_all({out / PROF["json"]: files[out / PROF["json"]]})
        except Exception as ex:   # noqa: BLE001
            line = f"ETF_FAIL {PROF['key']} 쓰기 실패 {type(ex).__name__} — 이번 실행 산출물 미완"
            print(line)
            if os.environ.get("GITHUB_STEP_SUMMARY"):
                with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
                    f.write(line + "\n")
            return 1
    else:
        write_all(files)
    line = (f"{'ETF CARD' if PROF['verdict'] or PROF.get('noVerdict') else 'INDEX'} {PROF['key']}: {res['status']}"
            + (f" S={res['S']} close={res['close']} cross={res['crossCheck']['status']} events={len(res['events'])}"
               if res["status"] == "ok" else f" reason={res['reason']} ({res.get('detail', '')})"))
    print(line)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(line + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
