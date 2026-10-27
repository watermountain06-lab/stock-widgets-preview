#!/usr/bin/env python3
"""IWM 가격 카드(index_daily.py --card IWM, 2026-10-21 — 판정 없음) 검사 — 저장소를 건드리지 않는다(임시 폴더, 가짜 시세·페이지).

    python3 v2/index/test_iwm_card.py

iShares 상품 페이지 읽기(JSON-LD NAV 묶음 하나·여러 개·없음, PER·보유 수), 하루 NAV 대조(P·prevP·더 이름·미래·그날 종가 없음·
±1% 경계), 계산 구간(사건 10년·월별 표가 들어감), 화면(PER 적자 종목 제외 라벨, 구성 종목 탭 없음, 판정하지 않음 탭, 대조 못 함 고지,
다른 ETF 문구 섞임 없음), 홈 데이터 IWM 칸(가격형, 다른 칸 보존, 보류 모양), 가격형 보류 알림(이번 실행만).
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "etf"))
import index_daily as ix  # noqa: E402
import test_index as TI  # noqa: E402

FAILS = []
P = TI.P


def check(name, ok, got=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  -> {got}"))
    if not ok:
        FAILS.append(name)


def page(nav="100.00", day="Oct 16, 2026", extra="", pe="17.73", hold="1,980"):
    ld = ('{"@type":"PropertyValue","name":"NAV as of","value":"%s","unitText":"USD","valueReference":'
          '{"@type":"PropertyValue","name":"As of Dates","value":"%s"}}' % (nav, day)) if nav is not None else ""
    return (f'<script type="application/ld+json">{{"additionalProperty":[{ld}{extra}]}}</script>'
            f'<div>P/E Ratio</div><div>{pe} as of Oct 16, 2026</div><div>Number of Holdings</div><div>{hold} as of Oct 16, 2026</div>')


def run(tmp, series, pg, data_js=None):
    tmp.mkdir(parents=True, exist_ok=True)
    (tmp / "y.json").write_text(TI.yahoo_json(series))
    prev = max(k for k, _ in series if k < P)
    (tmp / "s.json").write_text(json.dumps({"priceSession": P, "tickers": [{"price": {"session": P, "prevSession": prev}}] * 3}))
    (tmp / "page.html").write_text(pg)
    (tmp / "dgs10.csv").write_text("observation_date,DGS10\n2026-10-15,5.10\n2026-10-16,5.09\n")
    if data_js is not None:
        (tmp / "preview-only-etf-data.js").write_text(data_js)
    p = subprocess.run([sys.executable, str(HERE / "index_daily.py"), "--card", "IWM", "--out-root", str(tmp), "--yahoo", str(tmp / "y.json"),
                        "--stocks", str(tmp / "s.json"), "--fred", str(tmp / "page.html"), "--dgs10", str(tmp / "dgs10.csv")],
                       capture_output=True, text=True)
    res = json.loads((tmp / "v2" / "etf" / "IWM_card.json").read_text())
    html_ = (tmp / "preview-only-etf-iwm.html").read_text()
    txt = (tmp / "preview-only-etf-data.js").read_text()
    data = json.loads(txt.split("window.ETF_DATA = ", 1)[1].rstrip().rstrip(";"))
    return p, res, html_, data


def main():
    s = TI.make_series()
    ys = dict(s)
    prevP = max(k for k, _ in s if k < P)
    near = lambda k, f=1.0: f"{ys[k] * f:.4f}"
    # 페이지 읽기
    info = ix.parse_ishares_page(page(nav=near(P)))
    check("페이지: NAV·날짜·PER·보유 수", info["nav"] == float(near(P)) and info["navDate"] == P and info["pe"] == 17.73 and info["holdings"] == 1980, info)
    dup = ',{"@type":"PropertyValue","name":"NAV as of","value":"1.00","unitText":"USD","valueReference":{"@type":"PropertyValue","name":"As of Dates","value":"Oct 16, 2026"}}'
    check("페이지: NAV 묶음이 둘이고 서로 다르면 NAV 없음", ix.parse_ishares_page(page(nav=near(P), extra=dup))["nav"] is None)
    check("페이지: NAV 묶음 없음 → NAV 없음", ix.parse_ishares_page(page(nav=None))["nav"] is None)
    check("페이지: NAV가 0 → 없음", ix.parse_ishares_page(page(nav="0"))["nav"] is None)
    check("페이지: PER 범위 밖 → PER 없음(NAV는 그대로)", ix.parse_ishares_page(page(nav=near(P), pe="500"))["pe"] is None)
    bad_dates = page(nav=near(P)).replace("17.73 as of Oct 16, 2026", "17.73 as of Oct 32, 2026").replace("1,980 as of Oct 16, 2026", "1,980 as of Feb 30, 2026")
    bi = ix.parse_ishares_page(bad_dates)
    check("페이지: PER·보유 수 날짜가 이상해도 NAV는 그대로(그 칸만 없음)", bi["nav"] == float(near(P)) and bi["pe"] is None and bi["holdings"] is None, bi)
    # 하루 대조
    ser = [x for x in s if x[0] <= P]
    cc = lambda pg: ix.cross_check_page(ser, ix.parse_ishares_page(pg), P, prevP)
    check("대조: P의 NAV, 차이 0 → ok", cc(page(nav=near(P)))[0] == "ok")
    d_prev = __import__("datetime").date.fromisoformat(prevP).strftime("%b %d, %Y").replace(" 0", " ")
    st, txt = cc(page(nav=near(prevP), day=d_prev))
    check("대조: prevP의 NAV(저녁) → ok, P는 대조 전 문구", st == "ok" and "대조 전" in txt, txt)
    old = max(k for k, _ in s if k < prevP)
    st, txt = cc(page(nav=near(old), day=__import__("datetime").date.fromisoformat(old).strftime("%b %d, %Y").replace(" 0", " ")))
    check("대조: prevP보다 이른 NAV → 대조 못 함", st == "unavailable", txt)
    st, txt = cc(page(nav=near(P), day="Oct 17, 2026"))
    check("대조: 미래 날짜 NAV → 불일치", st == "mismatch", txt)
    st, txt = ix.cross_check_page([x for x in ser if x[0] != prevP], {"nav": ys[prevP], "navDate": prevP}, P, prevP)
    check("대조: NAV 날짜(prevP)의 종가가 시세에 없음 → 불일치", st == "mismatch" and "종가가 시세에 없음" in txt, txt)
    check("대조: 차이 0.5% → ok, 1.5% → 불일치", cc(page(nav=near(P, 1 / 1.005)))[0] == "ok" and cc(page(nav=near(P, 1 / 1.015)))[0] == "mismatch")
    exact = ys[P] / 1.01
    check("대조: 정확히 +1%·−1% → ok(경계 포함)", ix.cross_check_page(ser, {"nav": exact, "navDate": P}, P, prevP)[0] == "ok"
          and ix.cross_check_page(ser, {"nav": ys[P] / 0.99, "navDate": P}, P, prevP)[0] == "ok")
    check("대조: NAV 없음 → 대조 못 함", ix.cross_check_page(ser, {"nav": None}, P, prevP)[0] == "unavailable")
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        others = 'window.ETF_DATA = {"SPY": {"etf": "SPY", "status": "ok"}, "QQQ": {"etf": "QQQ", "status": "held"}, "DIA": {"etf": "DIA"}};\n'
        p, res, h, data = run(tmp / "ok", s, page(nav=near(P)), others)
        check("카드: ok, 계산 구간에 사건 10년·월별 표가 들어감", res["status"] == "ok" and res["since"] < f"{int(P[:4]) - 10}-12-01"
              and res["since"] < ix.minus_months(ix.d(P), 120).isoformat(), (res.get("reason"), res.get("detail"), res.get("since"), p.stderr[-200:]))
        check("카드: PER (펀드, 적자 종목 제외) · iShares 날짜 · 보유 1,980종목", "PER (펀드, 적자 종목 제외)" in h and "iShares 2026.10.16" in h and "보유 1,980종목" in h)
        check("카드: 구성 종목 탭 없음, 판정하지 않음 탭·버튼", "showSection('holdings'" not in h and "카드 판정 — 판정하지 않음" in h
              and "⚖️ 판정하지 않음</button>" in h and "⚖️ 카드 판정</button>" not in h)
        check("카드: 과거 대조 못 함 고지(머리·출처)", "과거 종가는 운용사 자료와 대조하지 못했다" in h and "자동으로 받지 못해 대조하지 못했다" in h)
        check("카드: 다른 ETF 문구 섞임 없음·단정 문구 없음", all(x not in h for x in ("SSGA", "Invesco", "State Street", "막아", "대형주 위주")))
        check("홈 칸: IWM 가격형 정상(종가·등락·1년·NAV 날짜), 다른 칸 그대로", data["IWM"]["kind"] == "price" and data["IWM"]["status"] == "ok"
              and data["IWM"]["navDate"] == P and data["SPY"] == {"etf": "SPY", "status": "ok"} and data["QQQ"]["status"] == "held" and "DIA" in data, data.get("IWM"))
        p, res, h, data = run(tmp / "none", s, page(nav=None), others)
        check("카드: 페이지에 NAV 없음 → 시세 보류(대조 못 함), 홈 칸 보류 사유", res["status"] == "held" and res["reason"] == "cross_unavailable"
              and data["IWM"]["status"] == "held" and "운용사 NAV" in data["IWM"]["reasonText"], (res.get("reason"), data.get("IWM")))
        p, res, h, data = run(tmp / "bad", s, page(nav=near(P, 1 / 1.05)), others)
        check("카드: NAV 차이 5% → 시세 보류, 홈 칸 보류(사유만, 가격 없음)", res["status"] == "held" and data["IWM"]["status"] == "held"
              and "close" not in data["IWM"] and data["IWM"]["reasonText"] and data["SPY"] == {"etf": "SPY", "status": "ok"}, data.get("IWM"))
        # 가격형 보류 알림
        import etf_alerts as EA
        sys.path.insert(0, str(HERE.parent / "etf"))
        import test_etf_auto as TA
        gh = TA.FakeGH()
        root = tmp / "bad"
        saved = {k: os.environ.get(k) for k in ("GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT")}
        os.environ["GITHUB_RUN_ID"], os.environ["GITHUB_RUN_ATTEMPT"] = "5", "1"
        try:
            r = json.loads((root / "v2" / "etf" / "IWM_card.json").read_text())
            r["runId"] = "4.1"   # 지난 실행(이번 5.1이 아님) — 시험 환경의 실행 ID와 무관하게
            (root / "v2" / "etf" / "IWM_card.json").write_text(json.dumps(r))
            # 2026-10-21 GLD·TLT 설계 dr r3~r5: 이번 실행 JSON이 아니면(단계 실패·쓰기 중단) "갱신 실패" 이슈 — 예전엔 아무것도 안 했다
            a0 = EA.run_price("IWM", root, "o/r", runner=gh)
            check("알림: 지난 실행 산출물(runId 다름) → 이슈 [ETF IWM price] 갱신 실패",
                  [x for x, _ in a0] == ["create"] and gh.issues[0]["title"] == "[ETF IWM price] 가격 카드 갱신 실패", a0)
            r["runId"] = "5.1"
            (root / "v2" / "etf" / "IWM_card.json").write_text(json.dumps(r))
            a1 = EA.run_price("IWM", root, "o/r", runner=gh)
            check("알림: 이어서 이번 실행 보류 → 같은 이슈에 사건 바뀜", [x for x, _ in a1] == ["comment"] and len(gh.issues) == 1
                  and "시세 보류" in gh.issues[0]["body"], a1)
            r.update(status="ok")
            (root / "v2" / "etf" / "IWM_card.json").write_text(json.dumps(r))
            a2 = EA.run_price("IWM", root, "o/r", runner=gh)
            check("알림: 정상 → 닫음", [x for x, _ in a2] == ["close"] and not gh.issues, a2)
        finally:
            for k, v in saved.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
    # 홈 가격형 카드(브라우저 코드를 node로): 정상·자료 없음·세션 다름·보류·형식 오류
    js = HERE.parents[1] / "etf.js"
    probe = ("global.window={StockData:{meta:{priceSession:'%s'}}};global.document={readyState:'loading',addEventListener(){}};"
             "global.matchMedia=()=>({matches:false});let src=require('fs').readFileSync(%s,'utf8').replace(\"if (document.readyState === 'loading')\","
             "'window.__t={etfCard:etfCard}; if (document.readyState === \\'loading\\')');eval(src);const s=x=>x.replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ');"
             "const ok={etf:'IWM',kind:'price',status:'ok',builtFor:'%s',S:'%s',close:275.78,chg:0.0166,ret1y:0.111,navDate:'%s'};"
             "console.log(JSON.stringify([s(window.__t.etfCard('IWM',ok)),s(window.__t.etfCard('IWM',undefined)),"
             "s(window.__t.etfCard('IWM',Object.assign({},ok,{builtFor:'2000-01-03'}))),"
             "s(window.__t.etfCard('IWM',{etf:'IWM',kind:'price',status:'held',builtFor:'%s',reasonText:'대조 불일치'})),"
             "s(window.__t.etfCard('IWM',Object.assign({},ok,{close:-1})))]))") % (P, json.dumps(str(js)), P, P, P, P)
    out = json.loads(subprocess.run(["node", "-e", probe], capture_output=True, text=True).stdout or "[]")
    check("홈 가격형: 정상(종가·가격 카드·NAV 하루만 대조)·자료 없음·세션 다름(갱신 대기)·보류(사유)·형식 오류",
          len(out) == 5 and "275.78" in out[0] and "가격 카드" in out[0] and "NAV 하루만 대조" in out[0] and "불러오지 못함" in out[1]
          and "갱신 대기" in out[2] and "대조 불일치" in out[3] and "형식 오류" in out[4], out)
    print(f"\n{'모두 통과' if not FAILS else f'실패 {len(FAILS)}건: ' + ', '.join(FAILS)}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
