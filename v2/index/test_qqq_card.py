#!/usr/bin/env python3
"""QQQ ETF 카드(index_daily.py --card QQQ, 2026-10-21) 검사 — 저장소를 건드리지 않는다(임시 폴더, 가짜 시세·NAV).

    python3 v2/index/test_qqq_card.py

NYSE 휴장일 달력(연말·대체 휴일·특별 휴장), Invesco NAV 대조(달력일 반복값·거래일 누락·비거래일 다른 값·중복·괴리·P일 게시 전·
prevP 없음·회전 창 첫 날이 주말), 표시 범위 보호, 펀드 PER·ICB 업종(받기 실패·목록 밖 이름 → 그 칸만), 판정 탭 이름,
대조 단계(etf_consistency.py — 어긋남 → 보류로 다시 써서 맞춤 / 다시 써도 어긋나면 종료 코드 1).
"""
import json
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "etf"))
import index_daily as ix  # noqa: E402
import test_index as TI  # noqa: E402

FAILS = []
P = "2026-10-16"


def check(name, ok, got=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  -> {got}"))
    if not ok:
        FAILS.append(name)


def series_from_calendar(lo, hi):
    """NYSE 달력의 거래일마다 종가(완만한 오름 + 2020-03 사건)."""
    out, c = [], 100.0
    for i, k in enumerate(ix.nyse_days(lo, hi)):
        c *= 0.9 if k == "2020-03-16" else (1.0004 if i % 5 else 0.9996)
        out.append((k, round(c, 2)))
    return out


def nav_doc(series, edit=None, first="2016-09-01"):
    """Invesco 형식: 달력일 전부(비거래일은 직전 거래일 값 반복), 새 날짜가 앞."""
    ys, pts, last, d0 = dict(series), [], None, date.fromisoformat(first)
    while d0.isoformat() <= series[-1][0]:
        k = d0.isoformat()
        if k in ys:
            last = round(ys[k] * 1.0003, 6)
        if last is not None:
            v = last
            if edit:
                k2, v = edit(k, v)
                if k2 is None:
                    d0 += timedelta(1)
                    continue
            pts.append({"date": d0.strftime("%m/%d/%Y"), "value": v})
        d0 += timedelta(1)
    return json.dumps({"cusip": "46090E103", "startDate": first, "lineChartData": [{"type": "NAV", "label": "NAV", "data": pts[::-1]}]})


SECT = json.dumps({"effectiveDate": "2026-09-30", "holdingWeights": [{"name": "Technology", "value": 68.0}, {"name": "Consumer Discretionary", "value": 15.1},
                   {"name": "Telecommunications", "value": 5.9}, {"name": "Health Care", "value": 3.8}, {"name": "Industrials", "value": 2.8},
                   {"name": "Consumer Staples", "value": 1.7}, {"name": "Basic Materials", "value": 1.2}, {"name": "Utilities", "value": 1.0},
                   {"name": "Energy", "value": 0.5}]})
CHARS = json.dumps({"effectiveDate": "2026-09-30", "priceToEarningsRatio": 29.480945, "forwardPriceToEarningsRatio": 25.75})
VERDICT = {"etf": "QQQ", "status": "ok", "verdict": "적정~고평가", "nbar": -2.02, "coverage": 0.777, "range": [-2.46, -0.91],
           "edgeNear": False, "bar": dict(TI.SPY_FAKE["bar"]), "S": P, "builtFor": P, "ruleVersion": "etf-v1",
           "expense": {"pct": 0.18, "source": "SEC 485BPOS", "url": "https://www.sec.gov/x"}, "holdingsSource": "Invesco",
           "top10": TI.SPY_FAKE["top10"], "cards": TI.SPY_FAKE["cards"]}


def run(tmp, series, nav=None, sect=SECT, chars=CHARS, verdict=VERDICT):
    tmp.mkdir(parents=True, exist_ok=True)
    (tmp / "y.json").write_text(TI.yahoo_json(series))
    prev = max(k for k, _ in series if k < P)
    (tmp / "s.json").write_text(json.dumps({"priceSession": P, "tickers": [{"price": {"session": P, "prevSession": prev}}] * 3}))
    (tmp / "nav.json").write_text(nav if nav is not None else nav_doc(series))
    (tmp / "sec.json").write_text(sect)
    (tmp / "ch.json").write_text(chars)
    (tmp / "dgs10.csv").write_text("observation_date,DGS10\n2026-10-15,5.10\n2026-10-16,5.09\n")
    (tmp / "v.json").write_text(json.dumps(verdict))
    args = [sys.executable, str(HERE / "index_daily.py"), "--card", "QQQ", "--out-root", str(tmp), "--yahoo", str(tmp / "y.json"),
            "--stocks", str(tmp / "s.json"), "--fred", str(tmp / "nav.json"), "--inv-sectors", str(tmp / "sec.json"),
            "--inv-chars", str(tmp / "ch.json"), "--dgs10", str(tmp / "dgs10.csv"), "--spy", str(tmp / "v.json")]
    p = subprocess.run(args, capture_output=True, text=True)
    res = json.loads((tmp / "v2" / "etf" / "QQQ_card.json").read_text())
    return p, res, (tmp / "preview-only-etf-qqq.html").read_text()


def main():
    # 달력
    days = set(ix.nyse_days("2016-01-01", "2026-12-31"))
    for k, want, why in (("2021-12-31", True, "새해 토요일 → 전날 거래"), ("2021-12-24", False, "성탄 토→금"), ("2022-06-20", False, "준틴스 일→월"),
                         ("2021-06-18", True, "준틴스는 2022년부터"), ("2023-01-02", False, "새해 일→월"), ("2018-12-05", False, "특별 휴장"),
                         ("2025-01-09", False, "특별 휴장"), ("2020-07-03", False, "독립기념일 토→금"), ("2022-12-26", False, "성탄 일→월"),
                         ("2017-01-02", False, "새해 일→월"), ("2024-03-29", False, "성금요일"), ("2026-11-27", True, "추수감사절 다음 날(조기 폐장) 거래")):
        check(f"달력: {k} {'거래' if want else '휴장'}({why})", (k in days) == want)
    s = series_from_calendar("2015-01-02", P)
    prevP = max(k for k, _ in s if k < P)
    ser = [x for x in s if x[0] <= P]
    nav = lambda **kw: ix.parse_invesco_nav(nav_doc(s, **kw))
    st, txt, _ = ix.cross_check_invesco(ser, nav(), P, prevP)
    check("NAV 대조: 정상 → ok", st == "ok", txt)
    st, txt, _ = ix.cross_check_invesco(ser + [("2026-10-17", 1.0)], nav(), P, prevP)
    check("NAV 대조: Yahoo에 P 뒤 날짜가 있어도 무시", st == "ok", txt)
    st, txt, _ = ix.cross_check_invesco([x for x in ser if x[0] != "2019-05-07"], nav(), P, prevP)
    check("NAV 대조: Yahoo 거래일 누락 → 날짜 불일치", st == "mismatch" and "날짜 불일치" in txt, txt)
    st, txt, _ = ix.cross_check_invesco(ser + [("2019-05-04", 50.0)], nav(), P, prevP)
    check("NAV 대조: Yahoo에 비거래일 날짜 → 날짜 불일치", st == "mismatch", txt)
    st, txt, _ = ix.cross_check_invesco(ser, nav(edit=lambda k, v: (None, v) if k == "2019-05-07" else (k, v)), P, prevP)
    check("NAV 대조: 거래일 NAV 없음 → 날짜 불일치", st == "mismatch" and "NAV 없는 거래일" in txt, txt)
    st, txt, _ = ix.cross_check_invesco(ser, nav(edit=lambda k, v: (k, v * 1.001) if k == "2019-05-04" else (k, v)), P, prevP)
    check("NAV 대조: 비거래일 NAV가 직전 값과 다름 → NAV 형식 변경", st == "mismatch" and "형식 변경" in txt, txt)
    pairs = nav() + [("2019-05-07", 1.0)]
    st, txt, _ = ix.cross_check_invesco(ser, pairs, P, prevP)
    check("NAV 대조: 날짜 중복 → NAV 형식 변경", st == "mismatch" and "형식 변경" in txt, txt)
    st, txt, _ = ix.cross_check_invesco(ser, nav(edit=lambda k, v: (k, 0.0) if k == "2019-05-07" else (k, v)), P, prevP)
    check("NAV 대조: 0 이하 값 → NAV 형식 변경", st == "mismatch", txt)
    st, txt, _ = ix.cross_check_invesco(ser, nav(edit=lambda k, v: (k, v * 1.012) if k == "2026-09-01" else (k, v)), P, prevP)
    check("NAV 대조: 최근 250거래일 괴리 1.2% → 불일치", st == "mismatch" and "차이가 큰 날" in txt, txt)
    st, txt, _ = ix.cross_check_invesco(ser, nav(edit=lambda k, v: (k, v * 0.982) if k == "2018-03-01" else (k, v)), P, prevP)
    check("NAV 대조: 그 앞 괴리 1.8% → ok", st == "ok", txt)
    st, txt, _ = ix.cross_check_invesco(ser, nav(edit=lambda k, v: (None, v) if k >= P else (k, v)), P, prevP)
    check("NAV 대조: P 하루 게시 전 → ok(대조 전 문구)", st == "ok" and "대조 전" in txt, txt)
    st, txt, _ = ix.cross_check_invesco(ser, nav(edit=lambda k, v: (None, v) if k >= prevP else (k, v)), P, prevP)
    check("NAV 대조: prevP까지 없음 → 대조 못 함", st == "unavailable", txt)
    for first in ("2016-10-01", "2016-10-02", "2017-01-01"):   # 토·일·새해 휴일
        st, txt, _ = ix.cross_check_invesco(ser, ix.parse_invesco_nav(nav_doc(s, first=first)), P, prevP)
        check(f"NAV 대조: 회전 창 첫 날 {first}(비거래일)도 ok", st == "ok", txt)
    st, txt, _ = ix.cross_check_invesco(ser, [], P, prevP)
    check("NAV 대조: NAV 없음 → 대조 못 함", st == "unavailable")
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        p, res, page = run(tmp / "ok", s)
        check("카드: ok · 시작일 = 대조 첫 거래일", res["status"] == "ok" and res["since"] == "2016-09-01", (res.get("reason"), res.get("detail"), p.stderr[-300:]))
        check("카드: 머리 PER (펀드) + Invesco 날짜 · 이익수익률 펀드 PER 표시", "PER (펀드)" in page and "Invesco 2026.09.30" in page and "펀드 PER 2026.09.30" in page)
        check("카드: 업종 ICB 도넛·비교 불가 주석", "업종 비중 (ICB, 펀드 기준)" in page and "GICS(SPY·DIA 카드)와 직접 비교 불가" in page and "기술" in page)
        check("카드: 판정 탭이 QQQ 이름·data-etf", "이 사이트 카드로 본 QQQ" in page and 'id="verdict" class="section" data-etf=' in page)
        check("카드: 출처 문구(NAV ±1%·±2% 안 확인·NYSE 휴장일)", "±1%, 그 앞 ±2% 안 확인" in page and "NYSE 휴장일" in page)
        check("카드: SPY 문구가 섞이지 않음", "SPY 보유" not in page and "SSGA" not in page and "본 SPY" not in page)
        p, res, page = run(tmp / "late", s, nav=nav_doc(s, first="2017-06-01"))
        check("카드: 대조 첫 날이 표시 범위보다 늦음 → 시세 보류(기간 모자람)", res["status"] == "held" and res["reason"] == "short", (res.get("reason"), res.get("detail")))
        p, res, page = run(tmp / "pe", s, chars="<html>")
        check("카드: PER 받기 실패 → 그 칸만 —(카드 ok)", res["status"] == "ok" and "PER 불러오지 못함" in page)
        bad = json.loads(SECT); bad["holdingWeights"][0]["name"] = "Technology Hardware"
        p, res, page = run(tmp / "sec", s, sect=json.dumps(bad))
        check("카드: ICB 목록 밖 이름 → 업종 칸만 불러오지 못함", res["status"] == "ok" and "업종 비중을 불러오지 못했다" in page)
        fin = json.loads(SECT); fin["holdingWeights"][-1] = {"name": "Financials", "value": 0.5}
        p, res, page = run(tmp / "fin", s, sect=json.dumps(fin))
        check("카드: 금융(ICB 11개 안) 나와도 그림", "금융" in page and "업종 비중을 불러오지 못했다" not in page)
        # 대조 단계 — 실제 카드 페이지(위 ok 실행)로
        import etf_consistency as EC
        import etf_daily as D
        root = tmp / "cons"
        (root / "v2" / "etf").mkdir(parents=True)
        (root / "site_data").mkdir()
        (root / "site_data" / "stocks.json").write_text(json.dumps({"priceSession": P}))
        res_v = dict(VERDICT, runAt="t", checks={}, checkDetail={}, pending=None, reason=None, reasonText=None, detail=None, counts=None,
                     ruleVersion="etf-v1", top10=[dict(t, n=None, excluded=[], lines=[t["company"]]) for t in VERDICT["top10"]],
                     cards=[dict(c, n=None, date=P, excluded=[]) for c in VERDICT["cards"]])
        D.write_outputs(res_v, root, "QQQ")
        card = (tmp / "ok" / "preview-only-etf-qqq.html").read_text()
        h = root / "preview-only-etf-qqq.html"
        h.write_text(card)   # 카드는 VERDICT(같은 값)로 그렸다
        check("대조: 같음 → 0", EC.run(root, ["QQQ"]) == 0)
        assert "&quot;verdict&quot;: &quot;적정~고평가&quot;" in card
        h.write_text(card.replace("&quot;verdict&quot;: &quot;적정~고평가&quot;", "&quot;verdict&quot;: &quot;고평가&quot;", 1))
        rc = EC.run(root, ["QQQ"])
        r2 = json.loads((root / "v2" / "etf" / "QQQ.json").read_text())
        page2 = h.read_text()
        obs = [json.loads(x) for x in (root / "v2" / "etf" / "date_obs.jsonl").read_text().splitlines()]
        check("대조: 어긋남 → 보류로 다시 써서 맞춤(0), 관측 selfcheck, run bad", rc == 0 and r2["status"] == "held" and r2["reason"] == "selfcheck"
              and obs[-1]["holds"] == ["selfcheck"] and r2["checks"]["run"] == "bad", (rc, r2.get("reason")))
        va, vb = card.find('<div id="verdict"'), card.find("<!-- DISCLAIMER")
        check("대조: 바꿔 끼운 앞·뒤 바이트는 원본 그대로", page2.startswith(card[:va]) and page2.endswith(card[vb:]))
        check("대조: 복구는 판정 탭만 바꿈 — 시세(차트·출처)는 그대로", "QQQ 차트 — 일봉" in page2 and "const SPX_DAILY" in page2
              and "자체 검사 불일치" in page2.split('id="verdict"')[1])
        h.write_text(page2.replace("&quot;selfcheck&quot;", "&quot;input&quot;", 1))
        def broken(h_, etf, res, P_):   # 바꿔 끼우기가 판정 칸 빈 페이지를 남긴다 → 다시 대조해도 어긋남
            h_.write_text('<p data-etf="{}">x</p>')
            return True
        rc = EC.run(root, ["QQQ"], card_page=broken)
        check("대조: 다시 쓴 뒤에도 어긋남 → 1(커밋·게시 막음)", rc == 1, rc)
        n_before = len((root / "v2" / "etf" / "date_obs.jsonl").read_text().splitlines())
        real_w = D.write_outputs
        D.write_outputs = lambda *a, **k: (_ for _ in ()).throw(OSError("x"))
        try:
            h.write_text('<p data-etf="{}">x</p>')
            rc = EC.run(root, ["QQQ"])
        finally:
            D.write_outputs = real_w
        n_after = len((root / "v2" / "etf" / "date_obs.jsonl").read_text().splitlines())
        check("대조: 다시 쓰기 실패 → 1, 관측 한 줄은 먼저 남김", rc == 1 and n_after == n_before + 1, (rc, n_before, n_after))
    import etf_daily as D2
    check("카드 페이지의 대조 칸 = etf_daily.CHECK_KEYS", tuple(ix.VERDICT_CHECK_KEYS) == tuple(D2.CHECK_KEYS))
    # 회전 창 앞쪽 비거래일에 값이 있어도(첫 거래일 전 NAV) 무시
    doc = json.loads(nav_doc(s, first="2016-10-03"))
    pts = doc["lineChartData"][0]["data"]
    pts += [{"date": "10/01/2016", "value": 1.0}, {"date": "10/02/2016", "value": 2.0}]
    st, txt, _ = ix.cross_check_invesco(ser, ix.parse_invesco_nav(json.dumps(doc)), P, prevP)
    check("NAV 대조: 첫 거래일 앞 비거래일 NAV(아무 값)는 무시", st == "ok", txt)
    print(f"\n{'모두 통과' if not FAILS else f'실패 {len(FAILS)}건: ' + ', '.join(FAILS)}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
