#!/usr/bin/env python3
"""SPY ETF 카드(index_daily.py --card SPY, 2026-10-20) 검사 — 저장소를 건드리지 않는다(임시 폴더, 가짜 시세·NAV).

    python3 v2/index/test_spy_card.py

운용사 NAV 이력 읽기(표 아래 안내 줄 건너뜀), NAV 대조(날짜 빠짐·괴리·NAV 지연·장이 쉰 날 NAV), 카드 판정 탭(정상·보류·묵음·
운용사 파일 갱신 대기·자료 없음), 시세가 보류여도 판정 탭은 남는지, 산출물 경로(preview-only-etf-spy.html·v2/etf/SPY_card.json).
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "etf"))
import index_daily as ix  # noqa: E402
import test_index as TI  # noqa: E402
import test_etf as TE  # noqa: E402

FAILS = []
P = TI.P


def check(name, ok, got=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  -> {got}"))
    if not ok:
        FAILS.append(name)


def nav_rows(series, edit=None, start="2003-12-01"):
    from datetime import date
    rows = [["Fund Name:", "SPY"], ["Ticker Symbol:", "SPY"], [], ["Date", "NAV", "Shares Outstanding", "Total Net Assets"]]
    for k, c in reversed(series):
        if k < start:
            continue
        v = c * 1.0005
        if edit:
            k, v = edit(k, v)
            if k is None:
                continue
        rows.append([date.fromisoformat(k).strftime("%d-%b-%Y"), v, 1.0, 1.0])
    rows += [[], ["State Street Global Advisors (SSGA) is now State Street Investment Management."]]
    return rows


VERDICT_OK = {"etf": "SPY", "status": "ok", "verdict": "적정~고평가", "nbar": -2.02, "coverage": 0.777, "range": [-2.46, -0.91],
              "edgeNear": False, "bar": dict(TI.SPY_FAKE["bar"]), "S": P, "builtFor": P, "ruleVersion": "etf-v1",
              "expense": {"pct": 0.0945, "source": "SEC 485BPOS", "url": "https://www.sec.gov/x"},
              "holdingsSource": "State Street", "top10": TI.SPY_FAKE["top10"], "cards": TI.SPY_FAKE["cards"]}


def run(tmp, series, nav_edit=None, verdict=VERDICT_OK, nav=True, yahoo_text=None):
    (tmp / "y.json").write_text(yahoo_text if yahoo_text is not None else TI.yahoo_json(series))
    prev = max(k for k, _ in series if k < P)
    (tmp / "s.json").write_text(json.dumps({"priceSession": P, "tickers": [{"price": {"session": P, "prevSession": prev}}] * 3}))
    (tmp / "page.html").write_text(TI.ssga_page())
    (tmp / "dgs10.csv").write_text("observation_date,DGS10\n2026-10-15,5.10\n2026-10-16,5.09\n")
    (tmp / "spy.json").write_text(json.dumps(verdict) if verdict is not None else "")
    if nav:
        TE.xlsx(tmp / "nav.xlsx", nav_rows(series, nav_edit))
    args = [sys.executable, str(HERE / "index_daily.py"), "--card", "SPY", "--out-root", str(tmp), "--yahoo", str(tmp / "y.json"),
            "--stocks", str(tmp / "s.json"), "--ssga-page", str(tmp / "page.html"), "--spy", str(tmp / "spy.json"),
            "--dgs10", str(tmp / "dgs10.csv"), "--fred", str(tmp / ("nav.xlsx" if nav else "missing.xlsx"))]
    p = subprocess.run(args, capture_output=True, text=True)
    res = json.loads((tmp / "v2" / "etf" / "SPY_card.json").read_text())
    page = (tmp / "preview-only-etf-spy.html").read_text()
    return p, res, page


def main():
    s = TI.make_series()
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        p, res, page = run(tmp, s)
        check("정상: ok·NAV 대조 ok·SPY 카드 경로", res["status"] == "ok" and res["crossCheck"]["status"] == "ok" and res["index"] == "SPY"
              and not (tmp / "v2" / "index" / "SP500.json").exists(), (res.get("reason"), res.get("detail"), p.stderr[-300:]))
        check("정상: 계산 구간 = NAV 첫 날부터", res.get("since") == "2003-12-01", res.get("since"))
        check("정상: 판정 탭(판정·점수·덮은 비중·막대)", 'id="verdict"' in page and "적정~고평가" in page and "−2.02" in page and "77.7%" in page
              and "카드 판정</button>" in page)
        check("정상: 공개 JSON에 판정 원본을 다시 싣지 않음", "verdictData" not in res)
        check("정상: 머리·차트·구성 종목 글자가 SPY", "SPDR S&amp;P 500 ETF Trust" in page and "SPY 차트 — 일봉" in page and "지수 차트" not in page
              and "지수 비중" not in page and "FRED SP500" not in page)
        p, res, page = run(tmp, s, nav_edit=lambda k, v: (None, v) if k == "2019-05-07" else (k, v))
        check("NAV 없는 거래일 → 보류(대조 불일치), 판정 탭은 남음", res["status"] == "held" and res["reason"] == "cross_check"
              and "적정~고평가" in page, (res.get("reason"), res.get("detail")))
        p, res, page = run(tmp, s, nav_edit=lambda k, v: (k, v * 1.012) if k == "2026-09-01" else (k, v))
        check("최근 250세션 괴리 1.2% → 보류", res["status"] == "held" and res["reason"] == "cross_check", res.get("detail"))
        p, res, page = run(tmp, s, nav_edit=lambda k, v: (k, v * 1.018) if k == "2010-09-01" else (k, v))
        check("그 앞 괴리 1.8%(2% 안) → ok", res["status"] == "ok", res.get("detail"))
        p, res, page = run(tmp, s, nav_edit=lambda k, v: (k, v * 1.025) if k == "2010-09-01" else (k, v))
        check("그 앞 괴리 2.5% → 보류", res["status"] == "held" and res["reason"] == "cross_check", res.get("detail"))
        p, res, page = run(tmp, s, nav_edit=lambda k, v: (None, v) if k == P else (k, v))
        check("NAV가 S 하루 늦음 → ok(대조 전 표시)", res["status"] == "ok" and "대조 전" in res["crossCheck"]["text"], res.get("detail"))
        prevP = max(k for k, _ in s if k < P)
        p, res, page = run(tmp, s, nav_edit=lambda k, v: (None, v) if k >= prevP else (k, v))
        check("NAV가 직전 세션까지 없음 → 보류(대조 못 함)", res["status"] == "held" and res["reason"] == "cross_unavailable", res.get("detail"))
        p, res, page = run(tmp, s, nav=False)
        check("NAV 파일 없음 → 보류(대조 못 함), 판정 탭은 그대로", res["status"] == "held" and res["reason"] == "cross_unavailable"
              and "운용사 NAV" in res["reasonText"] and "적정~고평가" in page.split('id="verdict"')[1])
        # Yahoo가 거래일 하루를 빠뜨림 → 그날은 "시세 없는 NAV 날" → 불일치
        s_miss = [x for x in s if x[0] != "2019-05-07"]
        TE.xlsx(tmp / "nav.xlsx", nav_rows(s))   # NAV는 빠짐없이
        args_nav = tmp / "nav.xlsx"
        ix.use_profile("SPY")
        n_full = ix.parse_navhist(args_nav.read_bytes())
        st, txt = ix.cross_check_nav([x for x in s_miss if x[0] <= P], n_full, P, max(k for k, _ in s if k < P))
        check("Yahoo 거래일 누락 → 불일치", st == "mismatch" and "2019-05-07" in txt, txt)
        # 장이 쉰 날 NAV — 목록(NAV_ONLY_OK)에 든 날만 허용
        prevP = max(k for k, _ in s if k < P)
        ix.use_profile("SPY")
        TE.xlsx(tmp / "x.xlsx", nav_rows(s))
        n = ix.parse_navhist((tmp / "x.xlsx").read_bytes())
        ser = [p_ for p_ in s if p_[0] <= P and p_[0] not in ix.NAV_ONLY_OK]   # 그날 장이 쉼(시세 없음), NAV만 있음
        st, txt = ix.cross_check_nav(ser, n, P, prevP)
        check("목록의 휴장일 NAV 3일 → ok", st == "ok" and "NAV만 3일" in txt, txt)
        st, txt = ix.cross_check_nav([p_ for p_ in ser if p_[0] != "2015-06-03"], n, P, prevP)
        check("목록 밖 NAV만 있는 날 1일 → 불일치", st == "mismatch", txt)
        check("NAV 이력: 표 아래 안내 줄을 건너뜀(날짜 칸만 남음)", len(n) > 1000 and all(len(k) == 10 and k[4] == "-" for k in n))
        # 판정 탭
        stale = dict(VERDICT_OK, builtFor="2026-10-15")
        p, res, page = run(tmp, s, verdict=stale)
        check("판정 세션 ≠ 홈 세션 → 판정 탭 묵음", "묵음" in page and "적정~고평가" not in page.split('id="verdict"')[1])
        lag = dict(VERDICT_OK, builtFor="2026-10-15", S="2026-10-15", pending={"kind": "issuer_lag", "P": P, "S": "2026-10-14"})
        p, res, page = run(tmp, s, verdict=lag)
        check("운용사 파일 갱신 대기 → 판정 + 꼬리표", "운용사 파일 갱신 대기" in page and "적정~고평가" in page.split('id="verdict"')[1])
        p, res, page = run(tmp, s, verdict={"etf": "SPY", "status": "held", "reasonText": "보유 파일 날짜", "builtFor": P})
        check("판정 보류 → 사유", "보유 파일 날짜" in page.split('id="verdict"')[1])
        p, res, page = run(tmp, s, verdict=None)
        check("판정 자료 없음 → 불러오지 못함(시세 카드는 ok)", res["status"] == "ok" and "불러오지 못했다" in page.split('id="verdict"')[1])
        p, res, page = run(tmp, s, verdict=dict(VERDICT_OK, nbar=9))
        check("판정 자료 범위 밖 → 형식 오류", "형식 오류" in page.split('id="verdict"')[1])
        neg = dict(VERDICT_OK["bar"]); neg["저평가"], neg["적정"] = -0.05, neg["적정"] + 0.15   # 합은 1, 하나가 음수
        p, res, page = run(tmp, s, verdict=dict(VERDICT_OK, bar=neg))
        check("막대에 음수(합은 1) → 형식 오류(홈과 같음)", "형식 오류" in page.split('id="verdict"')[1])
        p, res, page = run(tmp, s, verdict=dict(VERDICT_OK, builtFor="2026-10-15", bar=dict(VERDICT_OK["bar"], 저평가=0.5)))
        check("묵음 대상이어도 형식이 틀리면 형식 오류(홈과 같은 순서)", "형식 오류" in page.split('id="verdict"')[1])
        p, res, page = run(tmp, s, verdict={"etf": "SPY", "status": "weird", "builtFor": P})
        check("모르는 status → 형식 오류(홈과 같음)", "형식 오류" in page.split('id="verdict"')[1])
        p, res, page = run(tmp, s, verdict=dict(VERDICT_OK, expense={"pct": "0.0945", "url": "https://x", "source": "SEC"}))
        v = page.split('id="verdict"')[1]
        check("보수율 칸만 이상 → 판정은 그대로, 보수 안내만 뺌", "적정~고평가" in v and "보수율" not in v)
        off = dict(VERDICT_OK["bar"]); off["고평가"], off["카드 없음"] = off["고평가"] - 0.05, off["카드 없음"] + 0.05
        p, res, page = run(tmp, s, verdict=dict(VERDICT_OK, bar=off))
        check("5등급 합 ≠ 덮은 비중 → 형식 오류(홈과 같음)", "형식 오류" in page.split('id="verdict"')[1])
    with tempfile.TemporaryDirectory() as t:   # 틀까지 깨지면 ETF 단계가 쓴 판정 페이지를 덮지 않는다
        tmp = Path(t)
        (tmp / "preview-only-etf-spy.html").write_text("VERDICT PAGE")
        real = ix.render
        ix.render = lambda r: (_ for _ in ()).throw(KeyError("x"))
        try:
            import contextlib, io
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                ix.main(["--card", "SPY", "--out-root", str(tmp), "--stocks", str(tmp / "없음.json"), "--yahoo", str(tmp / "없음.json")])
        finally:
            ix.render = real
        check("틀까지 깨지면 판정 페이지를 남기고 JSON만 보류", (tmp / "preview-only-etf-spy.html").read_text() == "VERDICT PAGE"
              and json.loads((tmp / "v2" / "etf" / "SPY_card.json").read_text())["status"] == "held")
    print(f"\n{'모두 통과' if not FAILS else f'실패 {len(FAILS)}건: ' + ', '.join(FAILS)}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
