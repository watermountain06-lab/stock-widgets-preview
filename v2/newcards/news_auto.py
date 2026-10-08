#!/usr/bin/env python3
"""카드 뉴스에 새 실적 발표를 자동으로 더한다 — SEC 8-K 2.02항(실적 보도자료)만(2026-10-08 사용자 결정, 1안).

카드 뉴스(cfg의 NEWS)는 사람이 쓴 목록이라 매일 재빌드에서 바뀌지 않아, 실적 시즌에 옛 분기 소식에 머물렀다.
여기서는 각 카드의 마지막 손 뉴스보다 뒤에 나온 실적 발표 8-K를 찾아 v2/news_auto.json에 적는다.
fill.py가 카드를 만들 때 이 목록을 뉴스 맨 위에 넣는다. 항목에는 날짜·제목·보도자료 링크만 있다 —
매출·이익 숫자는 넣지 않는다(검증 없이 숫자를 카드에 올리지 않는다). 숫자는 분기 반영(v2/QUARTERLY_UPDATE.md) 때
사람이 손 뉴스로 쓰고, 그러면 같은 발표의 자동 항목은 빠진다(fill.py의 중복 판정).

배당·임원 변경 등 다른 공시는 8.01·5.02항에 여러 사건이 섞여 있어 목록만으로 무엇인지 알 수 없다 — 넣지 않는다.
ASML·TSM(6-K)·SKHY(한국 공시)와 은행·NVDA·BRKB·SPCX(cfg 뉴스 없음)는 이 점검 밖이다.

    python3 v2/newcards/news_auto.py            # cfg 카드 전부
    python3 v2/newcards/news_auto.py PEP COST
실패한 카드는 이전 항목을 그대로 두고 마지막 줄 JSON의 "failed"에 적는다.
"""
import datetime as dt
import importlib.util
import json
import os
import re
import sys
import time
import urllib.request
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
OUT = os.path.join(V2, "news_auto.json")
UA = "kim research gptjhss@gmail.com"
OUTSIDE = {"ASML", "TSM", "SKHY"}
KDATE = re.compile(r"(\d{4})년 (\d{1,2})월 (\d{1,2})일")


def get(url):
    for k in range(3):   # SEC 요청 제한(429)·일시 오류는 잠깐 쉬고 다시(Codex)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            return json.loads(urllib.request.urlopen(req, timeout=30).read())
        except Exception:
            if k == 2:
                raise
            time.sleep(2 + 4 * k)


def cfg(T):
    p = os.path.join(HERE, "cfg", f"cfg_{T.lower()}.py")
    sp = importlib.util.spec_from_file_location("cfg", p)
    C = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(C)
    return C


def hand_dates(C):
    """손 뉴스 항목의 날짜(제목 속 'YYYY년 M월 D일'과 반응일) — 자동 항목 중복 판정에 쓴다."""
    out, today = [], dt.date.today()
    for n in C.NEWS:
        m = KDATE.search(n[1] or "")
        if m:
            out.append(dt.date(int(m[1]), int(m[2]), int(m[3])))
        if n[2]:
            out.append(dt.date.fromisoformat(n[2]))
    return [d for d in out if d <= today]   # 앞으로의 일정 항목(예: "12월 1일 — 예정")이 그 전 실적을 막지 않게(Codex)


ET = ZoneInfo("America/New_York")
# 실적 보도자료 첫머리 — 2.02항이라도 가이던스 수정(ABBV IPR&D 2026-10-06)·인도량(TSLA 2026-10-02)처럼 실적 발표가 아닌 공시가 있다
# 첫머리 300자(제목 부분)만 본다 — 본문의 "실적은 ○일에 발표한다"(TSLA 인도량 보도자료)에 걸리지 않게
RESULTS = re.compile(r"\b(reports?|announces?)\b.{0,120}?\bresults\b|earnings release|results for the (first|second|third|fourth|fiscal)", re.I)


def when(acc):
    """접수 시각(SEC acceptanceDateTime, UTC — COST 9/24 장 마감 후 보도자료가 09-25T00:17Z) → 미국 동부 (날짜, 때)."""
    t = dt.datetime.strptime(acc[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc).astimezone(ET)
    hm = t.hour * 60 + t.minute
    return t.date(), ("장 시작 전" if hm < 9 * 60 + 30 else "장중" if hm < 16 * 60 else "장 마감 후")


def text(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    t = urllib.request.urlopen(req, timeout=30).read(60000).decode("utf-8", "ignore")
    t = re.sub(r"&#160;|&nbsp;", " ", re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"&#8217;|&#39;", "'", re.sub(r"&#38;|&amp;", "&", t))
    return re.sub(r"\s+", " ", re.sub(r"&#?\w+;", " ", t)).strip()


def exhibit(cik, accn, primary):
    """보도자료(EX-99) 문서 주소와 첫머리 — 파일 이름이 회사마다 달라(ACN q4fy26earnings8-kexhibit.htm) 문서 첫 줄의 형식 표시로 찾는다."""
    base = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accn.replace('-', '')}/"
    names = [x["name"] for x in get(base + "index.json")["directory"]["item"]]
    cands = [n for n in names if n.endswith((".htm", ".html")) and n != primary and "index" not in n and not re.match(r"R\d+\.htm", n)]
    cands.sort(key=lambda n: 0 if re.search(r"99", n) else 1)
    first = None
    for n in cands[:8]:   # 보도자료가 여럿이면(EX-99.1 가이던스, EX-99.2 실적) 실적인 것을 고른다(Codex)
        head = text(base + n)[:600]
        time.sleep(0.12)
        if head.startswith("EX-99"):
            if RESULTS.search(head[:300]):
                return base + n, head
            first = first or (base + n, head)
    return first or (base + f"{accn}-index.html", "")


def one(T, old):
    C = cfg(T)
    hand = hand_dates(C)
    since = max(hand) if hand else dt.date.today() - dt.timedelta(days=120)
    r = get(f"https://data.sec.gov/submissions/CIK{str(C.CIK).zfill(10)}.json")["filings"]["recent"]
    known = {e["accn"]: e for e in old}
    items = []
    for i, form in enumerate(r["form"]):
        if form != "8-K" or "2.02" not in r["items"][i].split(","):
            continue
        d, part = when(r["acceptanceDateTime"][i])
        if d <= since:
            continue
        accn = r["accessionNumber"][i]
        e = known.get(accn)
        if not e or not e.get("head"):   # 첫머리를 못 읽은 항목은 다음 실행에서 다시 찾는다
            url, head = exhibit(C.CIK, accn, r["primaryDocument"][i])
            e = {"accn": accn, "url": url, "head": head[:400]}
        e["results"] = bool(RESULTS.search(e["head"][:300]))   # 판정 규칙이 바뀌면 저장된 첫머리로 다시 판정한다
        e.update({"filed": r["filingDate"][i], "accepted": r["acceptanceDateTime"][i][:19], "date": d.isoformat(), "after_close": part == "장 마감 후"})
        items.append(e)
    return sorted(items, key=lambda e: e["accepted"], reverse=True)   # 실적 발표가 아닌 2.02항도 남긴다("results": false) — 카드엔 안 넣는다


def main():
    want = [a.upper() for a in sys.argv[1:]]
    tickers = want or sorted(f[4:-3].upper() for f in os.listdir(os.path.join(HERE, "cfg")) if f.startswith("cfg_") and f.endswith(".py"))
    data = json.load(open(OUT)) if os.path.exists(OUT) else {}
    failed = []
    for T in tickers:
        if T in OUTSIDE:
            continue
        try:
            C = cfg(T)
            if not hasattr(C, "NEWS") or not hasattr(C, "CIK"):
                continue
            items = one(T, data.get(T, []))
        except Exception as ex:
            print(f"{T}: 실패 {type(ex).__name__} {str(ex)[:120]}")
            failed.append(T)
            continue
        time.sleep(0.15)   # SEC 초당 10회 한도
        if items:
            print(f"{T}: 2.02항 {len(items)}건 — " + ", ".join(f"{e['date']}{' 장 마감 후' if e['after_close'] else ''} {'실적' if e['results'] else '실적 아님: ' + e['head'][:70]}" for e in items))
            data[T] = items
        else:
            data.pop(T, None)
    json.dump(data, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(json.dumps({"cards": sum(any(e["results"] for e in v) for v in data.values()), "failed": failed}, ensure_ascii=False))
    if failed:   # 워크플로 단계는 continue-on-error — 실패는 실행 화면에 경고로 남고 재빌드는 어제 목록으로 한다
        sys.exit(1)


if __name__ == "__main__":
    main()
