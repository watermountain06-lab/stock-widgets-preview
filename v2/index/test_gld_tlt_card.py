#!/usr/bin/env python3
"""GLD(금)·TLT(미국 20년+ 국채) 가격 카드(index_daily.py --card GLD|TLT, 2026-10-21 — 판정 없음) 검사.
저장소를 건드리지 않는다(임시 폴더, 가짜 시세·xlsx·페이지).

    python3 v2/index/test_gld_tlt_card.py

GLD: 운용사 과거 자료 xlsx 읽기(시트 이름·머리 열·날짜·차단 페이지), 창 안 날마다 종가 대조(±0.1% 경계 양쪽, 휴장 표기 충돌, 운용사만
있는 날, 빠진 평일, 파일 끝 = prevP → 대조 전, 끝 < prevP, P 이후 줄 무시, 창 밖 값 무시, 달력 예외 상수), 머리 값(1주당 금·보유 금).
TLT: 펀드에 연결된 JSON-LD 요소에서만 NAV(값 검사·연결 검사·키 순서), 지표 블록 안에서만 지표(후보·범위·날짜·중복).
화면 문구(숨은 섹션 포함 전체), 홈 칸·홈 JS(대조 방식별 검사·날짜 관계·옛 IWM 칸), 쓰기 순서 실패 주입, 갱신 실패 알림.
"""
import io
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "etf"))
import index_daily as ix  # noqa: E402
import test_index as TI  # noqa: E402

FAILS = []
P = TI.P
HEAD = ["Date", "Closing Price", "Ounces of Gold per Share", "NAV/Share at 10:30am NYT", "Tonnes of Gold"]


def check(name, ok, got=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  -> {got}"))
    if not ok:
        FAILS.append(name)


def xlsx(sheets):
    """{시트 이름: [[셀…]…]} → xlsx 바이트(인라인 문자열·숫자만, 표준 라이브러리)."""
    def col(i):
        s = ""
        i += 1
        while i:
            i, r = divmod(i - 1, 26)
            s = chr(65 + r) + s
        return s
    b = io.BytesIO()
    z = zipfile.ZipFile(b, "w")
    names = list(sheets)
    z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
    z.writestr("xl/workbook.xml", '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
               'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
               + "".join(f'<sheet name="{escape(n)}" sheetId="{i + 1}" r:id="rId{i + 1}"/>' for i, n in enumerate(names)) + '</sheets></workbook>')
    z.writestr("xl/_rels/workbook.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               + "".join(f'<Relationship Id="rId{i + 1}" Target="worksheets/sheet{i + 1}.xml"/>' for i in range(len(names))) + '</Relationships>')
    for i, n in enumerate(names):
        rows = []
        for ri, r in enumerate(sheets[n]):
            cells = []
            for ci, v in enumerate(r):
                ref = f"{col(ci)}{ri + 1}"
                if v is None:
                    continue
                if isinstance(v, (int, float)):
                    cells.append(f'<c r="{ref}"><v>{v!r}</v></c>')
                else:
                    cells.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(v))}</t></is></c>')
            rows.append(f'<row r="{ri + 1}">{"".join(cells)}</row>')
        z.writestr(f"xl/worksheets/sheet{i + 1}.xml", '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'
                   + "".join(rows) + '</sheetData></worksheet>')
    z.close()
    return b.getvalue()


def dmy(k):
    return date.fromisoformat(k).strftime("%d-%b-%Y")


def gld_rows(series, until=P, change=None, holidays=(), drop=(), extra=()):
    """운용사 줄: 시세의 평일마다 같은 종가(change {날짜: 값}), holidays는 US Holiday 줄, drop은 줄 없음, extra는 (날짜, 줄) 추가."""
    rows = [HEAD]
    ys = dict(series)
    day, end = date(2004, 11, 18), date.fromisoformat(until)
    add = dict(extra)
    while day <= end:
        k = day.isoformat()
        if k in add:
            rows.append([dmy(k)] + add[k])
        elif k in drop:
            pass
        elif k in holidays:
            rows.append([dmy(k)] + ["US Holiday"] * 4)
        elif k in ys:
            c = (change or {}).get(k, round(ys[k], 4))
            rows.append([dmy(k), c, 0.0917, c * 1.001 if isinstance(c, (int, float)) else c, 1060.18])
        day += timedelta(days=1)
    for k, r in extra:
        if k > until:
            rows.append([dmy(k)] + r)
    return rows


def gld_file(rows):
    return xlsx({"Disclaimer": [["no redistribution"]], ix.GLD_SHEET: rows})


def tlt_page(nav="80.0900", day="Oct 16, 2026", ticker="TLT", about="#fund", fid="#fund", ty="4.86%", ty_day="Oct 16, 2026",
             order=False, stray="", block=None, outside=""):
    navp = ({"@type": "PropertyValue", "name": "NAV as of", "unitText": "USD", "value": nav,
             "valueReference": {"@type": "PropertyValue", "name": "As of Dates", "value": day}} if not order else
            {"valueReference": {"value": day, "name": "As of Dates", "@type": "PropertyValue"}, "value": nav, "unitText": "USD", "name": "NAV as of"})
    g = [{"@type": ["InvestmentFund", "FinancialProduct"], "@id": fid, "name": "iShares 20+ Year Treasury Bond ETF",
          "identifier": [{"@type": "PropertyValue", "propertyID": "ticker", "value": ticker}]},
         {"@type": "WebPageElement", "@id": "#key", "about": {"@id": about}, "additionalProperty": [
             navp, {"@type": "PropertyValue", "name": "12m Trailing Yield as of", "value": ty,
                    "valueReference": {"@type": "PropertyValue", "name": "As of Dates", "value": ty_day}}]}]
    if block is None:
        block = ('<div data-id="fundamentalsAndRisk-container"><div><span>Effective Duration</span> <span>14.85 yrs</span> as of Oct 16, 2026</div>'
                 '<div>Weighted Avg Maturity 26.04 yrs as of Oct 16, 2026</div><div>Average Yield to Maturity 5.48% as of Oct 16, 2026</div>'
                 '<div>Number of Holdings 47 as of Oct 16, 2026</div></div>')
    return (f'<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": g})}</script>'
            f'{stray}{block}{outside}')


def run(card, tmp, series, src, data_js=None, env=None):
    tmp.mkdir(parents=True, exist_ok=True)
    (tmp / "y.json").write_text(TI.yahoo_json(series))
    prev = max(k for k, _ in series if k < P)
    (tmp / "s.json").write_text(json.dumps({"priceSession": P, "tickers": [{"price": {"session": P, "prevSession": prev}}] * 3}))
    f = tmp / ("gld.xlsx" if card == "GLD" else "page.html")
    (f.write_bytes if isinstance(src, bytes) else f.write_text)(src)
    if data_js is not None:
        (tmp / "preview-only-etf-data.js").write_text(data_js)
    e = dict(os.environ, **(env or {}))
    p = subprocess.run([sys.executable, str(HERE / "index_daily.py"), "--card", card, "--out-root", str(tmp), "--yahoo", str(tmp / "y.json"),
                        "--stocks", str(tmp / "s.json"), "--fred", str(f), "--dgs10", str(tmp / "nope.csv")],
                       capture_output=True, text=True, env=e)
    res = json.loads((tmp / "v2" / "etf" / f"{card}_card.json").read_text())
    h = (tmp / f"preview-only-etf-{card.lower()}.html").read_text()
    txt = (tmp / "preview-only-etf-data.js").read_text()
    return p, res, h, json.loads(txt.split("window.ETF_DATA = ", 1)[1].rstrip().rstrip(";"))


def main():
    s = [x for x in TI.make_series() if x[0] <= P]
    ys = dict(s)
    prevP = max(k for k, _ in s if k < P)
    need = min(ix.minus_months(ix.d(P), 120).isoformat(), f"{int(P[:4]) - 10}-12-01")
    first = max(k for k, _ in s if k < need)
    win = [x for x in s if x[0] >= first]
    ix.use_profile("GLD")

    def cg(rows, cal=None, ser=None):
        saved = dict(ix.GLD_CAL_OK)
        ix.GLD_CAL_OK.clear()
        ix.GLD_CAL_OK.update(cal or {})
        try:
            try:
                arch = ix.parse_gld_archive(gld_file(rows))
            except ValueError as e:
                return "unavailable", str(e), None
            return ix.cross_check_gld(ser or win, arch, P, prevP)
        finally:
            ix.GLD_CAL_OK.clear()
            ix.GLD_CAL_OK.update(saved)

    # ---- GLD 파일 읽기·대조 ----
    st, txt, info = cg(gld_rows(s))
    check("GLD: 모두 일치 → ok, 대조 구간·끝·최대 차이", st == "ok" and info["since"] == first and info["checkedThrough"] == P
          and info["pendingDate"] is None and abs(info["maxGap"]) < 1e-4 and info["oz"] == 0.0917 and info["tonnes"] == 1060.18, (st, txt))
    mid = win[len(win) // 2][0]
    for f_, want, lab in ((1 / 1.001, "ok", "+0.1% 정확히"), (1 / 0.999, "ok", "−0.1% 정확히"),
                          (1 / 1.00101, "mismatch", "+0.101%"), (1 / 0.99899, "mismatch", "−0.101%")):
        st, txt, _ = cg(gld_rows(s, change={mid: ys[mid] * f_}))
        check(f"GLD: 차이 {lab} → {want}", st == want, txt)
    st, txt, _ = cg(gld_rows(s, holidays={mid}))
    check("GLD: 운용사 US Holiday인데 시장 종가 있음 → 불일치(달력, 가격 차이 아님)", st == "mismatch" and "달력" in txt, txt)
    sat = next(k for k in (date.fromisoformat(mid) + timedelta(days=i) for i in range(7)) if k.weekday() == 5).isoformat()
    st, txt, _ = cg(gld_rows(s, extra=[(sat, [ys[mid], 0.0917, ys[mid], 1060.18])]))
    check("GLD: 운용사에만 숫자 종가가 있는 날 → 불일치", st == "mismatch" and "시세에 없음" in txt, txt)
    st, txt, _ = cg(gld_rows(s, drop={mid}))
    check("GLD: 운용사에만 평일 줄 없음 → 대조 못 함", st == "unavailable" and "평일" in txt, txt)
    st, txt, _ = cg(gld_rows(s, drop={mid}), ser=[x for x in win if x[0] != mid])
    check("GLD: 양쪽에서 같이 빠진 평일 → 대조 못 함", st == "unavailable" and "평일" in txt, txt)
    st, txt, _ = cg(gld_rows(s), ser=[x for x in win if x[0] != mid])
    check("GLD: 평일 운용사 숫자 종가인데 시세에 없음 → 불일치", st == "mismatch" and "시세에 없음" in txt, txt)
    rows = gld_rows(s, holidays={mid})
    i_mid = next(i for i, r in enumerate(rows) if r[0] == dmy(mid))
    rows[i_mid][3] = 123.4   # NAV 칸만 숫자 — 일부 칸만 휴장 표기
    st, txt, _ = cg(rows, ser=[x for x in win if x[0] != mid])
    check("GLD: 일부 칸만 US Holiday인 줄 → 대조 못 함", st == "unavailable", txt)
    st, txt, info = cg(gld_rows(s, until=prevP))
    check("GLD: 파일 끝 = prevP → ok, P는 대조 전", st == "ok" and info["checkedThrough"] == prevP and info["pendingDate"] == P and "대조 전" in txt, txt)
    old = max(k for k, _ in s if k < prevP)
    st, txt, _ = cg(gld_rows(s, until=old))
    check("GLD: 파일 끝 < prevP → 대조 못 함", st == "unavailable", txt)
    st, txt, _ = cg(gld_rows(s, holidays={P}))
    check("GLD: P 줄이 US Holiday인데 P 종가 있음 → 불일치(게시 지연 아님)", st == "mismatch" and P in txt, txt)
    st, txt, _ = cg(gld_rows(s, holidays={first}))
    check("GLD: 창 첫날이 US Holiday로 표기 → 불일치", st == "mismatch", txt)
    after = [("2026-10-19", ["oops", "x", "x", "x"]), ("2026-10-20", [None, None, None, None])]
    st, txt, info = cg(gld_rows(s, extra=after))
    check("GLD: P 이후 이상한 줄은 무시(머리 값은 P 이하에서)", st == "ok" and info["checkedThrough"] == P and info["oz"] == 0.0917, txt)
    for bad in (float("nan"), 0, -3.0, "n/a"):
        st, txt, _ = cg(gld_rows(s, change={mid: bad}))
        check(f"GLD: 창 안 종가 {bad!r} → 대조 못 함", st == "unavailable", txt)
    early = "2008-03-03"
    st, txt, _ = cg(gld_rows(s, change={early: ys[early] * 1.05}))
    check("GLD: 창 밖(2008) 차이는 무관", st == "ok", txt)
    rows = gld_rows(s)
    rows.insert(5, ["2004/11/25", 1, 1, 1, 1])
    st, txt, _ = cg(rows)
    check("GLD: 날짜를 못 읽는 줄(창 밖이라도) → 대조 못 함", st == "unavailable" and "날짜" in txt, txt)
    rows = gld_rows(s)
    rows[0] = ["Date", "Close", "Ounces of Gold per Share", "NAV", "Tonnes of Gold"]
    st, txt, _ = cg(rows)
    check("GLD: 머리 열 이름 바뀜 → 대조 못 함", st == "unavailable" and "Closing Price" in txt, txt)
    try:
        ix.parse_gld_archive(xlsx({"Other": gld_rows(s)}))
        check("GLD: 시트 없음 → 대조 못 함", False)
    except ValueError as e:
        check("GLD: 시트 없음 → 대조 못 함", "시트" in str(e), e)
    try:
        ix.parse_gld_archive(b"<html>blocked</html>")
        check("GLD: 차단 HTML(200) → 대조 못 함", False)
    except ValueError as e:
        check("GLD: 차단 HTML(200) → 대조 못 함", "xlsx" in str(e), e)
    rows = gld_rows(s)
    rows[-1][4] = "bad"
    rows[-1][2] = -1
    st, txt, info = cg(rows)
    check("GLD: 마지막 줄 톤·온스 이상 → 그 칸만 없음(대조 ok)", st == "ok" and info["tonnes"] is None and info["oz"] is None, info)
    st, txt, info = cg(gld_rows(s, holidays={mid}), cal={mid: "시험"})
    check("GLD: 달력 예외 날짜는 달력 검사만 면제하고 셈", st == "ok" and info["exempt"] == 1 and "대조 제외 1일" in txt, txt)
    st, txt, _ = cg(gld_rows(s, change={mid: ys[mid] * 1.05}), cal={mid: "시험"})
    check("GLD: 달력 예외 날짜라도 가격 차이는 면제 안 함", st == "mismatch", txt)

    # ---- TLT 페이지 ----
    f = ix.parse_ishares_fund(tlt_page(), "TLT")
    check("TLT: 펀드에 연결된 NAV·12개월 분배수익률", f["nav"] == 80.09 and f["navDate"] == P and abs(f["ty"] - 0.0486) < 1e-12 and f["why"] is None, f)
    for v in ("NaN", "inf", "0", "-80.09", "", "80.09x"):
        check(f"TLT: NAV {v!r} → 없음", ix.parse_ishares_fund(tlt_page(nav=v), "TLT")["nav"] is None)
    check("TLT: NAV 단위 EUR → 없음", ix.parse_ishares_fund(tlt_page().replace('"USD"', '"EUR"'), "TLT")["nav"] is None)
    w = ix.parse_ishares_fund(tlt_page(about="#other"), "TLT")
    check("TLT: NAV 요소가 다른 펀드에 연결 → 없음(사유)", w["nav"] is None and "연결" in w["why"], w)
    w = ix.parse_ishares_fund(tlt_page(ticker="IEF"), "TLT")
    check("TLT: TLT 펀드 객체 없음 → 없음(사유)", w["nav"] is None and "TLT" in w["why"], w)
    w = ix.parse_ishares_fund(tlt_page(fid="", about=""), "TLT")
    check("TLT: @id·about 빈 문자열 → 없음", w["nav"] is None, w)
    stray = '<script>{"name":"NAV as of","value":"1.00","unitText":"USD","valueReference":{"@type":"PropertyValue","name":"As of Dates","value":"Oct 16, 2026"}}</script>'
    w = ix.parse_ishares_fund(tlt_page(order=True, stray=stray), "TLT")
    check("TLT: 키 순서가 바뀐 연결 요소 + 다른 곳의 옛 형식 NAV 문자열 → 연결 요소 값", w["nav"] == 80.09, w)
    check("TLT: 12개월 분배수익률 '4.86' (% 없음) → 그 값만 없음", ix.parse_ishares_fund(tlt_page(ty="4.86"), "TLT")["ty"] is None)
    bm = ix.parse_bond_metrics(tlt_page(), P, prevP)
    check("TLT 지표: 블록 안 네 지표", bm == {"dur": (14.85, P), "wam": (26.04, P), "ytm": (0.0548, P), "n": (47, P)}, bm)
    blk = '<div data-id="fundamentalsAndRisk-container">Effective Duration 14.85 yrs as of Oct 16, 2026</div>'
    check("TLT 지표: 블록 둘 → 모두 없음", all(v is None for v in ix.parse_bond_metrics(tlt_page(block=blk + blk), P, prevP).values()))
    check("TLT 지표: 블록 없음 + 블록 밖(관련 상품)에만 지표 → 없음",
          all(v is None for v in ix.parse_bond_metrics(tlt_page(block="", outside="<div>Effective Duration 7.10 yrs as of Oct 16, 2026</div>"), P, prevP).values()))
    def one(txt_, key):
        return ix.parse_bond_metrics(tlt_page(block=f'<div data-id="fundamentalsAndRisk-container">{txt_}</div>'), P, prevP)[key]
    check("TLT 지표: 같은 지표 (14.85, P)·(14.85, 옛 날짜) → 없음",
          one("Effective Duration 14.85 yrs as of Oct 16, 2026 Effective Duration 14.85 yrs as of Oct 01, 2026", "dur") is None)
    check("TLT 지표: 깨진 후보 + 정상 후보 → 없음", one("Effective Duration n/a Effective Duration 14.85 yrs as of Oct 16, 2026", "dur") is None)
    check("TLT 지표: 완전히 같은 묶음 둘 → 하나로", one("Effective Duration 14.85 yrs as of Oct 16, 2026 Effective Duration 14.85 yrs as of Oct 16, 2026", "dur") == (14.85, P))
    check("TLT 지표: 음수 듀레이션 → 없음", one("Effective Duration -1.20 yrs as of Oct 16, 2026", "dur") is None)
    check("TLT 지표: 소수 보유 수 → 없음", one("Number of Holdings 47.5 as of Oct 16, 2026", "n") is None)
    check("TLT 지표: 수익률 30% 이상 → 없음", one("Average Yield to Maturity 31.00% as of Oct 16, 2026", "ytm") is None)
    check("TLT 지표: 단위 다름(yrs 대신 %) → 없음", one("Effective Duration 14.85% as of Oct 16, 2026", "dur") is None)
    check("TLT 지표: 날짜가 P보다 뒤 → 없음", one("Effective Duration 14.85 yrs as of Oct 19, 2026", "dur") is None)
    split = ('<div data-id="fundamentalsAndRisk-container">Effective Duration 14.85 yrs as of Oct 16, 2026 <!-- </div> -->'
             ' Effective Duration 19.00 yrs as of Oct 16, 2026</div>')
    check("TLT 지표: 주석 속 </div>로 블록을 쪼갠 상충 값 → 없음", ix.parse_bond_metrics(tlt_page(block=split), P, prevP)["dur"] is None)
    fake = '<!-- <div data-id="fundamentalsAndRisk-container">Effective Duration 9.99 yrs as of Oct 16, 2026</div> -->'
    check("TLT 지표: 주석 속 가짜 블록은 세지 않음", ix.parse_bond_metrics(tlt_page(stray=fake), P, prevP)["dur"] == (14.85, P))
    scr = '<script>var t = \'<div data-id="fundamentalsAndRisk-container">Effective Duration 9.99 yrs as of Oct 16, 2026</div>\';</script>'
    check("TLT 지표: script 속 가짜 블록은 세지 않음", ix.parse_bond_metrics(tlt_page(stray=scr), P, prevP)["dur"] == (14.85, P))
    check("TLT 지표: 블록 안 주석 속 지표는 후보 아님",
          one("Effective Duration 14.85 yrs as of Oct 16, 2026 <!-- Effective Duration 9.99 yrs as of Oct 16, 2026 -->", "dur") == (14.85, P))
    unclosed = ('<section><div data-id="fundamentalsAndRisk-container">Effective Duration 14.85 yrs as of Oct 16, 2026</section>')
    check("TLT 지표: 대상 블록이 바깥 태그에 밀려 닫힘 → 없음", ix.parse_bond_metrics(tlt_page(block=unclosed), P, prevP)["dur"] is None)
    check("TLT 지표: 보유 수 '4,7'(쉼표 위치 틀림) → 없음", one("Number of Holdings 4,7 as of Oct 16, 2026", "n") is None)
    check("TLT 지표: 보유 수 '1,980'(세 자리 구분) → 1980", one("Number of Holdings 1,980 as of Oct 16, 2026", "n") == (1980, P))
    pg = tlt_page()
    commented = pg.replace('<script type="application/ld+json">', '<!-- <script type="application/ld+json">').replace("</script>", "</script> -->", 1)
    check("TLT: 주석 속 JSON-LD만 있음 → NAV 없음", ix.parse_ishares_fund(commented, "TLT")["nav"] is None, commented[:80])
    check("TLT: NAV '8,0.09'(쉼표 위치 틀림) → 없음", ix.parse_ishares_fund(tlt_page(nav="8,0.09"), "TLT")["nav"] is None)
    check("TLT: 분배수익률 '4,.86%' → 그 값만 없음", ix.parse_ishares_fund(tlt_page(ty="4,.86%"), "TLT")["ty"] is None)
    check("TLT 지표: 날짜 뒤에 숫자가 붙음(20260) → 없음", one("Effective Duration 14.85 yrs as of Oct 16, 20260", "dur") is None)
    check("TLT: 12개월 분배수익률 '4.86%%' → 그 값만 없음", ix.parse_ishares_fund(tlt_page(ty="4.86%%"), "TLT")["ty"] is None
          and ix.parse_ishares_fund(tlt_page(ty="4.86%%"), "TLT")["nav"] == 80.09)
    check("TLT 지표: Number of Holdings (Long) 같은 다른 이름은 후보 아님", one("Number of Holdings 47 as of Oct 16, 2026 Number of Holdings (Long) 50", "n") == (47, P))

    # ---- 카드 끝까지(임시 폴더) ----
    tn = f"{ys[P]:.4f}"   # 가짜 시세에 맞춘 TLT NAV(차이 0)
    others = ('window.ETF_DATA = {"SPY": {"etf": "SPY", "status": "ok"}, "IWM": {"etf": "IWM", "kind": "price", "status": "ok", "builtFor": "%s"}};\n' % P)
    forbid = ("PER (", "이익수익률", "^GSPC", "SSGA", "S&amp;P 500", "S&P 500", "IWM", "배당 제외", "Invesco", "State Street",
              "Apple", "Microsoft", "NVIDIA", "미 10년 국채", "구성 종목 자료")
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        p, res, h, data = run("GLD", tmp / "g", s, gld_file(gld_rows(s)), others)
        check("카드 GLD: ok, 구간 대조 구조 칸", res["status"] == "ok" and res["crossCheck"]["checkedThrough"] == P and res["since"] == first,
              (res.get("reason"), res.get("detail"), p.stderr[-300:]))
        check("카드 GLD: 문구(금 1온스 값이 아니다·분배금 없음·스폰서 수수료·OHLC 대조 안 함)",
              all(x in h for x in ("금 1온스 값이 아니다", "0.0917온스", "1,060.2톤", "분배금 없음", "스폰서 수수료 연 0.40%", "SEC 10-Q 2026-08-04",
                                   "대조하지 않음", "World Gold Trust Services", "SPDR Gold Trust 공개 자료")), h[h.find("meta-item"):][:600])
        bad = [x for x in forbid if x in h]
        check("카드 GLD: 숨은 섹션 포함 다른 ETF·주식형 문구 없음, 구성 종목 탭 없음", not bad and "showSection('holdings'" not in h, bad)
        check("홈 칸 GLD: history·since·checkedThrough·pendingDate null·prevSession, 다른 칸 그대로",
              data["GLD"]["check"] == "history" and data["GLD"]["checkedThrough"] == P and data["GLD"]["pendingDate"] is None
              and data["GLD"]["prevSession"] == prevP and data["SPY"] == {"etf": "SPY", "status": "ok"} and data["IWM"]["builtFor"] == P, data.get("GLD"))
        p, res, h, data = run("GLD", tmp / "g2", s, b"<html>blocked</html>", others)
        check("카드 GLD: 차단 페이지 → 시세 보류(사유 구체), 홈 칸 보류", res["status"] == "held" and res["reason"] == "cross_unavailable"
              and "xlsx" in res["detail"] and data["GLD"]["status"] == "held", (res.get("detail"), data.get("GLD")))
        bad = [x for x in forbid if x in h]
        check("카드 GLD 보류 화면: 다른 ETF·주식형 문구 없음", not bad, bad)
        p, res, h, data = run("TLT", tmp / "t", s, tlt_page(nav=tn), others)
        check("카드 TLT: ok, NAV 하루 대조", res["status"] == "ok" and res["crossCheck"]["navDate"] == P, (res.get("reason"), res.get("detail"), p.stderr[-300:]))
        check("카드 TLT: 문구(분배금 제외·하루 NAV만·지표·보수, 국채 금리 칸 없음)",
              all(x in h for x in ("분배금 제외", "최근 하루 NAV만 확인", "5.48%", "14.85년", "약 15%", "12개월 분배수익률 4.86%", "보유 47종목(iShares 2026.10.16)",
                                   "가중 평균 만기 26.04년", "총보수 0.15%", "SEC 497K 2026-06-29", "매달 분배금")), h[h.find("meta-item"):][:800])
        bad = [x for x in forbid if x in h]
        check("카드 TLT: 숨은 섹션 포함 다른 ETF·주식형 문구 없음, 구성 종목 탭 없음", not bad and "showSection('holdings'" not in h, bad)
        check("홈 칸 TLT: day·navDate·prevSession", data["TLT"]["check"] == "day" and data["TLT"]["navDate"] == P and data["TLT"]["prevSession"] == prevP, data.get("TLT"))
        p, res, h, data = run("TLT", tmp / "t2", s, tlt_page(nav=tn, about="#other"), others)
        check("카드 TLT: NAV가 TLT에 연결 안 됨 → 시세 보류(구체 사유)", res["status"] == "held" and "연결" in res["detail"], res.get("detail"))
        p, res, h, data = run("TLT", tmp / "t3", s, tlt_page(nav=tn, block=""), others)
        check("카드 TLT: 지표 블록 없음 → 지표 칸만 —, 딸린 문장 없음, 카드 ok", res["status"] == "ok" and "약 15%" not in h and "보유 47종목" not in h
              and "12개월 분배수익률 4.86%" in h, res.get("status"))
        # 쓰기 순서 실패 주입(한 프로세스 — 함수만 바꾼다)
        d0 = tmp / "w"
        run("TLT", d0, s, tlt_page(nav=tn), others)
        before = {f_: (d0 / f_).read_text() for f_ in ("preview-only-etf-tlt.html", "v2/etf/TLT_card.json", "preview-only-etf-data.js")}
        args = ["--card", "TLT", "--out-root", str(d0), "--yahoo", str(d0 / "y.json"), "--stocks", str(d0 / "s.json"),
                "--fred", str(d0 / "page.html"), "--dgs10", str(d0 / "nope.csv")]
        (d0 / "page.html").write_text(tlt_page(nav=f"{ys[P] * 0.9:.4f}"))   # 이번 실행은 보류가 될 입력(ok → held 전환)
        orig_home, orig_all = ix.write_home_price, ix.write_all
        try:
            ix.write_home_price = lambda *a, **k: (_ for _ in ()).throw(OSError("home"))
            rc = ix.main(args)
            after = {f_: (d0 / f_).read_text() for f_ in before}
            check("쓰기: 홈 실패 → 카드 HTML·JSON 안 씀, 비정상 종료", rc == 1 and after == before, rc)
            ix.write_home_price = orig_home
            calls = []
            def fail_html(files):
                calls.append(list(files))
                if any(str(k).endswith(".html") for k in files):
                    raise OSError("html")
                return orig_all(files)
            ix.write_all = fail_html
            rc = ix.main(args)
            after = {f_: (d0 / f_).read_text() for f_ in before}
            check("쓰기: HTML 실패(ok → held 도중) → 홈만 새 값, JSON 옛것, 비정상 종료", rc == 1 and after["v2/etf/TLT_card.json"] == before["v2/etf/TLT_card.json"]
                  and after["preview-only-etf-tlt.html"] == before["preview-only-etf-tlt.html"] and '"TLT": {"etf": "TLT", "kind": "price", "status": "held"' in after["preview-only-etf-data.js"], rc)
            def fail_json(files):
                if any(str(k).endswith(".json") for k in files):
                    raise OSError("json")
                return orig_all(files)
            ix.write_all = fail_json
            rc = ix.main(args)
            check("쓰기: JSON 실패 → 비정상 종료, JSON 옛것", rc == 1 and (d0 / "v2/etf/TLT_card.json").read_text() == before["v2/etf/TLT_card.json"], rc)
            ix.write_all = orig_all
            orig_pages = ix.pages_for
            ix.pages_for = lambda res, P: (res, None)
            try:
                rc = ix.main(args)
            finally:
                ix.pages_for = orig_pages
            check("쓰기: 카드 페이지 없음 → 완료 JSON 안 씀, 비정상 종료", rc == 1 and (d0 / "v2/etf/TLT_card.json").read_text() == before["v2/etf/TLT_card.json"], rc)
        finally:
            ix.write_home_price, ix.write_all = orig_home, orig_all
        # 알림: JSON이 옛 실행 것이면 갱신 실패
        import etf_alerts as EA
        import test_etf_auto as TA
        gh = TA.FakeGH()
        saved = {k: os.environ.get(k) for k in ("GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT")}
        os.environ["GITHUB_RUN_ID"], os.environ["GITHUB_RUN_ATTEMPT"] = "9", "1"
        try:
            a0 = EA.run_price("TLT", d0, "o/r", runner=gh)
            check("알림: TLT JSON이 이번 실행 것이 아님 → [ETF TLT price] 갱신 실패", [x for x, _ in a0] == ["create"]
                  and gh.issues[0]["title"] == "[ETF TLT price] 가격 카드 갱신 실패" and "etf-key: stale" in gh.issues[0]["body"], gh.issues)
            a1 = EA.run_price("GLD", tmp / "nothing", "o/r", runner=gh)
            check("알림: GLD JSON 없음 → 갱신 실패", [x for x, _ in a1] == ["create"] and gh.issues[-1]["title"].startswith("[ETF GLD price]"), a1)
        finally:
            for k, v in saved.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v

    # ---- 홈 JS(node) ----
    js = HERE.parents[1] / "preview-only-etf.js"
    probe = ("global.window={StockData:{meta:{priceSession:'%s'}}};global.document={readyState:'loading',addEventListener(){}};"
             "global.matchMedia=()=>({matches:false});let src=require('fs').readFileSync(%s,'utf8').replace(\"if (document.readyState === 'loading')\","
             "'window.__t={etfCard:etfCard,cardsHtml:cardsHtml}; if (document.readyState === \\'loading\\')');eval(src);"
             "const s=x=>x.replace(/<[^>]+>/g,' ').replace(/\\s+/g,' ');const P='%s',Q='%s';"
             "const g={etf:'GLD',kind:'price',status:'ok',builtFor:P,S:P,check:'history',prevSession:Q,close:377.65,chg:-0.005,ret1y:-0.06,since:'2016-10-19',checkedThrough:P,pendingDate:null};"
             "const t={etf:'TLT',kind:'price',status:'ok',builtFor:P,S:P,check:'day',prevSession:Q,close:80.13,chg:0.008,ret1y:-0.12,navDate:P};"
             "const A=(o,x)=>Object.assign({},o,x);const C=(k,d)=>s(window.__t.etfCard(k,d));"
             "console.log(JSON.stringify({gok:C('GLD',g),gpend:C('GLD',A(g,{checkedThrough:Q,pendingDate:P})),tok:C('TLT',t),tprev:C('TLT',A(t,{navDate:Q})),"
             "bad:[C('GLD',A(g,{checkedThrough:Q})),C('GLD',A(g,{checkedThrough:'2026-10-19'})),C('GLD',A(g,{since:'2026-10-17'})),"
             "C('GLD',A(g,{checkedThrough:Q,pendingDate:Q})),C('GLD',A(g,{prevSession:'2026-10-21',checkedThrough:'2026-10-21',pendingDate:P})),"
             "C('GLD',A(g,{check:'day',navDate:P})),C('TLT',A(t,{check:'history'})),C('TLT',A(t,{navDate:'2026-10-14'})),C('TLT',A(t,{check:undefined})),"
             "C('TLT',A(t,{close:0})),C('TLT',A(t,{prevSession:'2026-02-30'})),C('TLT',A(t,{etf:'GLD'}))],"
             "iwmOld:C('IWM',{etf:'IWM',kind:'price',status:'ok',builtFor:P,S:P,close:275.78,chg:0.01,ret1y:0.1,navDate:Q}),"
             "order:window.__t.cardsHtml().map(x=>(x.match(/etf-tk\">([A-Z]+)/)||[])[1])}))") % (P, json.dumps(str(js)), P, prevP)
    r = subprocess.run(["node", "-e", probe], capture_output=True, text=True)
    out = json.loads(r.stdout or "{}") if r.returncode == 0 else {}
    check("홈 JS: 카드 6장 순서(가격형 3)", out.get("order") == ["SPY", "QQQ", "DIA", "IWM", "TLT", "GLD"], (out.get("order"), r.stderr[-300:]))
    check("홈 JS: GLD history 문구", "운용사 종가와 2016.10.19~%s 대조" % P.replace("-", ".") in out.get("gok", "") and "날마다 대조" in out.get("gok", ""), out.get("gok"))
    check("홈 JS: GLD 대조 전", "%s 종가는 대조 전" % P.replace("-", ".") in out.get("gpend", ""), out.get("gpend"))
    check("홈 JS: TLT day 문구·분배금 제외, prevP NAV도 ok", "하루만 대조" in out.get("tok", "") and "(분배금 제외)" in out.get("tok", "")
          and "80.13" in out.get("tprev", ""), (out.get("tok"), out.get("tprev")))
    bads = out.get("bad") or []
    check("홈 JS: 날짜 관계·대조 방식·필수 칸 어긋남 12가지 → 모두 형식 오류", len(bads) == 12 and all("형식 오류" in x for x in bads),
          [i for i, x in enumerate(bads) if "형식 오류" not in x])
    check("홈 JS: check 없는 옛 IWM 칸(navDate = 직전 세션)도 예전처럼 정상", "275.78" in out.get("iwmOld", ""), out.get("iwmOld"))
    print(f"\n{'모두 통과' if not FAILS else f'실패 {len(FAILS)}건: ' + ', '.join(FAILS)}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
