#!/usr/bin/env python3
"""S&P 500 지수 카드(index_daily.py) 검사 — 저장소를 건드리지 않는다(임시 폴더에 가짜 시세를 만들어 돈다).

    python3 v2/index/test_index.py

가짜 시세는 1970년부터 평일마다 종가를 만들고, 2020-03에 사건(±3% 하루, −10%·−20% 낙폭, 회복·사상 최고)을 심는다.
돌연변이 검사: 날짜 어긋남·FRED 불일치·FRED 없음·FRED 지연·FRED 이상값·Yahoo 누락일(FRED 구간 안과 뒤)·시세 깨짐·
자체 검사 실패·화면 만들기 실패(틀이 깨진 경우 포함)가 세 산출물을 보류로 쓰는지. 사건 경계(정확히 −10%·−20%, 전고점과 같은 날 회복)와 끝난 달 판정은 작은 시세로 직접 검사한다.
"""
import json
import subprocess
import sys
import tempfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import index_daily as ix  # noqa: E402

FAILS = []
P = "2026-10-16"


def check(name, ok, got=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  -> {got}"))
    if not ok:
        FAILS.append(name)


def make_series():
    """평일 종가. 2016-10-20부터 사건을 심는다."""
    out, c, day = [], 100.0, date(1970, 1, 2)
    end = date.fromisoformat(P)
    i = 0
    while day <= end:
        if day.weekday() < 5:
            i += 1
            k = day.isoformat()
            if k == "2020-03-02":
                c *= 0.88          # −12% 하루(낙폭 −10% 진입, 하루 급락)
            elif k == "2020-03-03":
                c *= 0.90          # 낙폭 −20% 진입
            elif k == "2020-03-04":
                c *= 1.035         # 하루 +3.5%(문턱 3%와 4% 사이)
            elif "2020-03-05" <= k <= "2020-12-31":
                c *= 1.0012
            else:
                c *= 1.0003 if i % 7 else 0.9995
            out.append((k, round(c, 2)))
        day += timedelta(days=1)
    return out


def yahoo_json(series):
    ts = [int(datetime(*map(int, k.split("-")), 21, 0, tzinfo=timezone.utc).timestamp()) for k, _ in series]
    return json.dumps({"chart": {"result": [{"timestamp": ts, "indicators": {"quote": [{"close": [c for _, c in series]}]}}]}})


def fred_csv(series, edit=None):
    rows = ["observation_date,SP500"] + [f"{k},{c:.2f}" for k, c in series if k >= "2016-10-20"]
    if edit:
        rows = [edit(r) for r in rows]
    return "\n".join(rows) + "\n"


def run(tmp, series, P=P, fred=True, fred_edit=None, yahoo_text=None, fred_series=None, prev=None):
    (tmp / "y.json").write_text(yahoo_text if yahoo_text is not None else yahoo_json(series))
    prev = prev or (max(k for k, _ in series if k < P) if any(k < P for k, _ in series) else None)
    (tmp / "s.json").write_text(json.dumps({"priceSession": P, "tickers": [{"price": {"session": P, "prevSession": prev}}] * 3}))
    args = [sys.executable, str(HERE / "index_daily.py"), "--out-root", str(tmp), "--yahoo", str(tmp / "y.json"),
            "--stocks", str(tmp / "s.json")]
    if fred:
        (tmp / "f.csv").write_text(fred_csv(fred_series or series, fred_edit))
        args += ["--fred", str(tmp / "f.csv")]
    else:
        args += ["--fred", str(tmp / "missing.csv")]
    p = subprocess.run(args, capture_output=True, text=True)
    res = json.loads((tmp / "v2" / "index" / "SP500.json").read_text())
    pages = [(tmp / f).read_text() for f in ("preview-only-index-sp500.html", "preview-only-index-sp500-events.html")]
    return p, res, pages


def main():
    s = make_series()
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        p, res, pages = run(tmp, s)
        check("정상 실행 ok", res["status"] == "ok" and p.returncode == 0, (res.get("reason"), p.stderr[-300:]))
        check("대조 ok", res.get("crossCheck", {}).get("status") == "ok", res.get("crossCheck"))
        check("두 페이지 data-status ok", all('data-status="ok"' in x for x in pages))
        check("탭 링크 양쪽", all("preview-only-index-sp500-events.html" in x and 'href="preview-only-index-sp500.html"' in x for x in pages))
        labels = [r["label"] for r in res["returns"]]
        check("기간 6칸(1개월·6개월·1년·3년·5년·YTD)", labels == ["1개월", "6개월", "1년", "3년", "5년", "YTD"], labels)
        check("3년·5년만 연 환산", [("annual" in r) for r in res["returns"]] == [False, False, False, True, True, False])
        ys = dict(s)
        r1 = res["returns"][0]
        check("1개월 기준일 = 09-16 이하 마지막", r1["base"] == max(k for k in ys if k <= "2026-09-16"), r1)
        check("1개월 값", abs(ys[P] / ys[r1["base"]] - 1 - r1["ret"]) < 1e-12)
        types = {e["type"] for e in res["events"]}
        check("사건 종류 5가지", types == {"up", "down", "dd", "recover", "ath"}, types)
        dd = sorted(e["date"] for e in res["events"] if e["type"] == "dd")
        check("낙폭 −10%·−20% 진입일", dd == ["2020-03-02", "2020-03-03"], dd)
        rec = [e for e in res["events"] if e["type"] == "recover"]
        check("전고점 회복 1번", len(rec) == 1 and rec[0]["date"] > "2020-03-04", rec)
        mv = sorted((e["date"], e["type"]) for e in res["events"] if e["type"] in ("up", "down"))
        check("±3% 하루", mv == [("2020-03-02", "down"), ("2020-03-03", "down"), ("2020-03-04", "up")], mv)
        check("사건은 최근 10년만", min(e["date"] for e in res["events"]) > "2016-10-16")
        rows = res["monthly"]["rows"]
        check("월별 10년", [r["year"] for r in rows] == list(range(2017, 2027)))
        check("진행 중인 달 표시", rows[-1]["months"][9]["partial"] and rows[-1]["months"][10] is None)
        check("최근 12개월 막대 12칸, 마지막이 진행 중", len(res["monthly"]["last12"]) == 12 and res["monthly"]["last12"][-1]["partial"])
        check("오늘의 지수·환율 비교 없음", "환율" not in pages[0])

        p, res, pages = run(tmp, s, P="2026-10-19")
        check("홈 세션보다 시세가 늦으면 보류", res["status"] == "held" and res["reason"] == "date_mismatch", res.get("reason"))
        check("보류 페이지 둘 다 held, 숫자 없음", all('data-status="held"' in x for x in pages) and "기간별 수익률" not in pages[0]
              and 'id="f-main"' not in pages[1])

        p, res, _ = run(tmp, s + [("2026-10-19", 9999.0)])
        check("P 이후 막대는 버린다", res["status"] == "ok" and res["S"] == P and res["close"] == round(s[-1][1], 2), res.get("reason"))

        recent = s[-5][0]
        p, res, _ = run(tmp, s, fred_edit=lambda r: r.replace(recent + ",", recent + ",1") if r.startswith(recent) else r)
        check("최근 FRED 불일치면 보류", res["status"] == "held" and res["reason"] == "cross_check", res.get("reason"))
        old = "2018-05-15"
        p, res, _ = run(tmp, s, fred_edit=lambda r: f"{old},{float(r.split(',')[1]) * 1.01:.2f}" if r.startswith(old) else r)
        check("옛 날짜 1% 차이면 보류", res["status"] == "held" and res["reason"] == "cross_check", res.get("reason"))
        p, res, _ = run(tmp, s, fred_edit=lambda r: f"{old},{float(r.split(',')[1]) + 0.05:.2f}" if r.startswith(old) else r)
        check("옛 날짜 소수 둘째 자리 차이는 통과", res["status"] == "ok", res.get("reason"))

        p, res, pages = run(tmp, s, fred=False)
        check("FRED 없으면 보류(대조 못 함)", res["status"] == "held" and res["reason"] == "cross_unavailable", res.get("reason"))
        check("'대조 못 함'이 두 페이지에", all("대조 못 함" in x for x in pages))
        p, res, _ = run(tmp, s, fred_series=s[:-1])
        check("FRED 1세션 지연은 통과, '대조 전' 표시", res["status"] == "ok" and "대조 전" in res["crossCheck"]["text"], res.get("reason"))
        p, res, _ = run(tmp, s, fred_series=s[:-2])
        check("FRED 2세션 지연이면 보류", res["status"] == "held" and res["reason"] == "cross_unavailable", res.get("reason"))
        p, res, _ = run(tmp, s[:-2] + s[-1:], fred_series=s[:-3], prev=s[-2][0])
        check("FRED 끝 뒤에서 Yahoo가 하루 빠뜨리면 보류", res["status"] == "held" and res["reason"] == "date_mismatch", res.get("reason"))
        nan_day = s[-10][0]
        p, res, _ = run(tmp, s, fred_edit=lambda r: f"{nan_day},NaN" if r.startswith(nan_day) else r)
        check("FRED 값이 NaN이면 보류", res["status"] == "held" and res["reason"] == "cross_unavailable", res.get("reason"))
        gap = s[:-100] + s[-99:]
        p, res, _ = run(tmp, gap, fred_series=s)
        check("Yahoo가 하루 빠뜨리면 보류", res["status"] == "held" and res["reason"] == "cross_check", res.get("reason"))

        p, res, pages = run(tmp, s, yahoo_text="{not json")
        check("시세 깨지면 보류(fetch_fail)", res["status"] == "held" and res["reason"] == "fetch_fail" and p.returncode == 0)

        spiked = [(k, 99999.0 if k == "2010-05-03" else c) for k, c in s]
        p, res2, _ = run(tmp, spiked)
        p, res, _ = run(tmp, s)
        check("대조 구간 앞 값은 결과에 안 들어감", res2["status"] == "ok" and res2["ath"] == res["ath"] and res2["events"] == res["events"]
              and res2["chart"] == res["chart"] and res["since"] == "2016-10-20", (res2.get("ath"), res.get("since")))
        check("그림·사건이 대조 구간 첫 날 앞으로 안 나감", min(v[0][0] for v in res["chart"].values()) >= "2016-10-20"
              and min(e["date"] for e in res["events"]) >= "2016-10-20")
        p, res, _ = run(tmp, s[-300:])
        check("시세 기간 모자라면 보류", res["status"] == "held" and res["reason"] == "short", res.get("reason"))

    # 화면 만들기 실패 → 세 산출물 모두 보류
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        (tmp / "y.json").write_text(yahoo_json(s))
        (tmp / "s.json").write_text(json.dumps({"priceSession": P, "tickers": [{"price": {"session": P, "prevSession": s[-2][0]}}]}))
        (tmp / "f.csv").write_text(fred_csv(s))
        real, calls = ix.render, []

        def broken(res):
            calls.append(res["status"])
            if res["status"] == "ok":
                raise KeyError("x")
            return real(res)
        ix.render = broken
        try:
            ix.main(["--out-root", str(tmp), "--yahoo", str(tmp / "y.json"), "--fred", str(tmp / "f.csv"), "--stocks", str(tmp / "s.json")])
        finally:
            ix.render = real
        res = json.loads((tmp / "v2" / "index" / "SP500.json").read_text())
        pages = [(tmp / f).read_text() for f in ("preview-only-index-sp500.html", "preview-only-index-sp500-events.html")]
        check("화면 실패면 JSON·두 페이지 모두 보류", res["status"] == "held" and res["reason"] == "run_fail"
              and all('data-status="held"' in x for x in pages), (res.get("status"), calls))
        args = ["--out-root", str(tmp), "--yahoo", str(tmp / "y.json"), "--fred", str(tmp / "f.csv"), "--stocks", str(tmp / "s.json")]

        def always_broken(res):
            raise KeyError("x")
        ix.render = always_broken
        try:
            ix.main(args)
        finally:
            ix.render = real
        pages = [(tmp / f).read_text() for f in ("preview-only-index-sp500.html", "preview-only-index-sp500-events.html")]
        check("틀까지 깨지면 최소 보류 페이지", all('data-status="held"' in x and "<style" not in x for x in pages))
        real_sc = ix.selfcheck

        def bad_sc(res, series):
            raise AssertionError("x")
        ix.selfcheck = bad_sc
        try:
            ix.main(args)
        finally:
            ix.selfcheck = real_sc
        res = json.loads((tmp / "v2" / "index" / "SP500.json").read_text())
        check("자체 검사 실패면 main이 보류(run_fail)", res["status"] == "held" and res["reason"] == "run_fail", res.get("reason"))

    # 사건 경계: 정확히 −10%·−20%, 전고점과 같은 날 회복, 그다음 새 최고
    tiny = [("2020-01-01", 100.0), ("2020-01-02", 90.0), ("2020-01-03", 80.0), ("2020-01-06", 100.0), ("2020-01-07", 101.0)]
    ev = sorted((e["date"], e["type"]) for e in ix.events([("2019-12-31", 99.0)] + tiny, "2020-01-07"))
    want = sorted([("2020-01-01", "ath"), ("2020-01-02", "down"), ("2020-01-02", "dd"), ("2020-01-03", "down"), ("2020-01-03", "dd"),
                   ("2020-01-06", "up"), ("2020-01-06", "recover"), ("2020-01-07", "ath")])
    check("정확히 −10%·−20% 진입, 같은 값 회복, 다음 날 최고", ev == want, ev)
    again = [("2020-01-01", 100.0), ("2020-01-02", 90.0), ("2020-01-03", 100.0), ("2020-01-06", 90.0)]
    ev = [(e["date"], e["type"]) for e in ix.events([("2019-12-31", 99.0)] + again, "2020-01-06") if e["type"] in ("dd", "recover")]
    check("회복 뒤 다시 −10%면 새 진입", sorted(ev) == [("2020-01-02", "dd"), ("2020-01-03", "recover"), ("2020-01-06", "dd")], ev)
    edge = [("2020-01-01", 100.0), ("2020-01-02", 103.0), ("2020-01-03", 107.0), ("2020-01-06", 103.79)]   # 107→103.79는 정확히 −3%지만 float로는 −0.0299…
    mv = sorted((e["date"], e["type"]) for e in ix.events([("2019-12-31", 100.0)] + edge, "2020-01-06") if e["type"] in ("up", "down"))
    check("정확히 +3%·−3%도 사건", mv == [("2020-01-02", "up"), ("2020-01-03", "up"), ("2020-01-06", "down")], mv)
    # 끝난 달: S가 그 달 마지막 평일이면 진행 중 아님
    check("09-30(수)은 끝난 달", ix.month_done("2026-09-30") and not ix.month_done("2026-09-29"))
    check("10-30(금)은 끝난 달(주말 건너뜀)", ix.month_done("2026-10-30"))
    ms = [p for p in s if p[0] <= "2026-09-30"]
    m = ix.monthly(ms, ms[-1][0])
    check("끝난 달은 평균에 들어감", m["rows"][-1]["months"][8]["partial"] is False and m["stats"][8]["n"] == 10, m["stats"][8])

    # 자체 검사 돌연변이: 월별 곱 ≠ YTD
    res = ix.compute(s, {k: round(c, 2) for k, c in s if k >= "2016-10-20"}, P, s[-2][0])
    res["monthly"]["rows"][-1]["months"][0]["ret"] += 0.01
    try:
        ix.selfcheck(res, s)
        check("자체 검사가 월별 곱 ≠ YTD를 잡음", False, "통과해 버림")
    except AssertionError:
        check("자체 검사가 월별 곱 ≠ YTD를 잡음", True)
    res = ix.compute(s, {k: round(c, 2) for k, c in s if k >= "2016-10-20"}, P, s[-2][0])
    res["returns"][2]["ret"] += 0.01
    try:
        ix.selfcheck(res, s)
        check("자체 검사가 수익률 변조를 잡음", False, "통과해 버림")
    except AssertionError:
        check("자체 검사가 수익률 변조를 잡음", True)
    check("3월 31일 − 1개월 = 2월 말", ix.minus_months(date(2026, 3, 31), 1) == date(2026, 2, 28))
    check("윤년 2월 29일 − 12개월 = 2월 28일", ix.minus_months(date(2024, 2, 29), 12) == date(2023, 2, 28))

    print("\n" + ("모두 통과" if not FAILS else f"실패 {len(FAILS)}개: {FAILS}"))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
