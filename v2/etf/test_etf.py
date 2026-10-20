#!/usr/bin/env python3
"""ETF 판정(etf_daily.py) 검사 — 저장소를 건드리지 않는다(임시 폴더에 카드 사본·가짜 보유 파일을 만들어 돈다).

    python3 v2/etf/test_etf.py

운용사 원본은 저장소에 둘 수 없어(사전 등록 "입력") 보유 파일은 표준 라이브러리로 만든 가짜 xlsx다. 카드는 실제 v2 카드 몇 장의 사본이다.
돌연변이 검사(사전 등록 검증 계획): 판정 단어가 그대로인 카드 코드 변경 3종이 ETF를 보류로 떨어뜨리는지, 날짜·입력·받기·자체 검사 실패가
세 산출물을 보류로 쓰는지, 대체 단계가 깨진 본체 대신 보류를 쓰는지.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "v2"
CARDS = ["NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "AVGO", "JPM", "BRKB", "ELV"]
FAILS = []


def check(name, ok, got=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  -> {got}"))
    if not ok:
        FAILS.append(name)


def xlsx(path, rows):
    """rows: [[셀…]…] — 문자열은 inlineStr, 수는 숫자 셀."""
    def cell(ref, v):
        if v is None:
            return ""
        if isinstance(v, (int, float)):
            return f'<c r="{ref}"><v>{v}</v></c>'
        return f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(v))}</t></is></c>'
    body = "".join(f'<row r="{i + 1}">' + "".join(cell(f"{chr(65 + j)}{i + 1}", v) for j, v in enumerate(r)) + "</row>"
                   for i, r in enumerate(rows) if r)
    m = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    rel = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
        z.writestr("xl/workbook.xml", f'<?xml version="1.0"?><workbook xmlns="{m}" xmlns:r="{rel}"><sheets><sheet name="h" sheetId="1" r:id="rId1"/></sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="worksheet" Target="worksheets/sheet1.xml"/></Relationships>')
        z.writestr("xl/worksheets/sheet1.xml", f'<?xml version="1.0"?><worksheet xmlns="{m}"><sheetData>{body}</sheetData></worksheet>')


def holdings(asof="16-Oct-2026", lines=None):
    head = [["Fund Name:", "State Street SPDR S&P 500 ETF Trust"], ["Ticker Symbol:", "SPY"], ["Holdings:", f"As of {asof}"], [],
            ["Name", "Ticker", "Identifier", "SEDOL", "Weight", "Sector", "Shares Held", "Local Currency"]]
    tail = [[], ["The whole or any part of this work may not be reproduced (가짜 면책 문구)"]]
    return head + lines + tail


def base_lines():
    w = {"NVDA": 8.0, "AAPL": 7.5, "MSFT": 6.0, "GOOGL": 3.0, "GOOG": 2.5, "AMZN": 3.7, "META": 2.4, "AVGO": 2.4,
         "JPM": 1.4, "BRK.B": 1.5, "ELV": 0.15}
    rows = [[f"CO {t}", t, f"ID{t.replace('.', '')}", "-", v, "-", 1.0, "USD"] for t, v in w.items()]
    rows += [["NO CARD CO", "ZZZ", "IDZZZ", "-", 2.0, "-", 1.0, "USD"], ["US DOLLAR", "-", "999USDZ92", "-", 0.3, "-", 1.0, "USD"]]
    return rows


def tree(tmp, mutate=None):
    """임시 v2 사본: 추출기·서명 스크립트 + 카드 몇 장. mutate(텍스트) → 텍스트를 모든 카드에 적용."""
    v2 = tmp / "v2"
    (v2 / "research").mkdir(parents=True)
    (v2 / "etf").mkdir()
    shutil.copy(V2 / "research" / "extract_card_verdicts.js", v2 / "research")
    shutil.copy(V2 / "etf" / "verdict_code_sig.js", v2 / "etf")
    for t in CARDS:
        h = (V2 / f"{t}_full_widget.html").read_text(encoding="utf-8")
        (v2 / f"{t}_full_widget.html").write_text(mutate(h, t) if mutate else h, encoding="utf-8")
    return v2


def run(tmp, v2, lines=None, asof="16-Oct-2026", P="2026-10-16", cfg_edit=None, no_xlsx=False, script=None):
    out = tmp / "out"
    out.mkdir(exist_ok=True)
    (tmp / "stocks.json").write_text(json.dumps({"priceSession": P}))
    cfg = json.loads((V2 / "etf" / "ticker_alias.json").read_text(encoding="utf-8"))
    if cfg_edit:
        cfg_edit(cfg)
    (tmp / "cfg.json").write_text(json.dumps(cfg, ensure_ascii=False))
    x = tmp / "h.xlsx"
    xlsx(x, holdings(asof, lines if lines is not None else base_lines()))
    cmd = [sys.executable, str(script or V2 / "etf" / "etf_daily.py"), "--out-root", str(out), "--v2", str(v2),
           "--stocks", str(tmp / "stocks.json"), "--private", str(tmp / "private"), "--cfg", str(tmp / "cfg.json")]
    if not no_xlsx:
        cmd += ["--xlsx", str(x)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    res = json.loads((out / "v2" / "etf" / "SPY.json").read_text(encoding="utf-8")) if (out / "v2" / "etf" / "SPY.json").exists() else None
    return p, res, out


def expected(v2, lines, P):
    """판정을 따로 계산한다(etf_daily.py를 쓰지 않는다)."""
    ver = json.loads(subprocess.run(["node", str(v2 / "research" / "extract_card_verdicts.js")], capture_output=True, text=True).stdout)
    alias = {"BRK.B": "BRKB", "GOOG": "GOOGL"}
    D = sum(r[4] for r in lines if r[2] != "999USDZ92")
    num = cov = 0.0
    for r in lines:
        c = ver.get(alias.get(r[1], r[1]))
        if not c or c["verdict"] == "판정 보류" or c["date"] != P:
            continue
        s = [j for j in c["judges"] if j[1] is not None]
        n = 4 * sum(j[1] for j in s) / sum(j[3] for j in s)
        num += r[4] / D * n
        cov += r[4] / D
    return num / cov, cov


def main():
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        v2 = tree(tmp)
        P = json.loads(subprocess.run(["node", str(v2 / "research" / "extract_card_verdicts.js")], capture_output=True, text=True).stdout)["NVDA"]["date"]
        asof = __import__("datetime").datetime.strptime(P, "%Y-%m-%d").strftime("%d-%b-%Y")

        # 1 기준: 정상 판정, 따로 계산한 값과 같음, 세 산출물·원본 비공개
        p, r, out = run(tmp, v2, asof=asof, P=P)
        nb, cv = expected(v2, base_lines(), P)
        check("기준 판정 ok", r and r["status"] == "ok", (r or {}).get("reasonText") or p.stdout + p.stderr)
        check("n̄ 따로 계산과 같음", r and abs(r["nbar"] - nb) < 1e-12, (r or {}).get("nbar"))
        check("c 따로 계산과 같음", r and abs(r["coverage"] - cv) < 1e-12, (r or {}).get("coverage"))
        check("GOOG+GOOGL 한 회사", r and any(t["company"] == "GOOGL" and t["lines"] == ["GOOGL", "GOOG"] for t in r["top10"]))
        check("세 산출물", all((out / f).exists() for f in ("v2/etf/SPY.json", "preview-only-etf-spy.html", "preview-only-etf-data.js")))
        check("공개 SPY.json에 Identifier 없음", "IDNVDA" not in (out / "v2/etf/SPY.json").read_text(encoding="utf-8"))
        check("종료 코드 0", p.returncode == 0, p.returncode)

        # 2 돌연변이: 판정 단어는 그대로인 카드 코드 변경 → 코드 서명이 보류로
        muts = {
            "현금흐름 가중치 2→1": lambda h, t: h.replace("lv.label, 2],", "lv.label, 1],"),
            "안 쓰이는 +2 표 추가": lambda h, t: h.replace("'매우 싸다': 1,", "'매우 싸다': 1, '초싸다': 2,"),
            "자기 이력 문턱 70→60": lambda h, t: h.replace("s >= 70 ? 1", "s >= 60 ? 1"),
        }
        for name, m in muts.items():
            with tempfile.TemporaryDirectory() as d2:
                t2 = Path(d2)
                v2m = tree(t2, m)
                changed = sum((v2m / f"{c}_full_widget.html").read_text(encoding="utf-8") != (V2 / f"{c}_full_widget.html").read_text(encoding="utf-8") for c in CARDS)
                p, r, _ = run(t2, v2m, asof=asof, P=P)
                check(f"돌연변이 '{name}'({changed}장 바뀜) → 코드 변경 보류", changed and r and r["reason"] == "code_sig", (r or {}).get("reason"))

        # 3 구조 서명: 해시를 승인해도 가중치 1이면 구조가 잡는다
        with tempfile.TemporaryDirectory() as d2:
            t2 = Path(d2)
            v2m = tree(t2, muts["현금흐름 가중치 2→1"])
            sig = json.loads(subprocess.run(["node", str(v2m / "etf" / "verdict_code_sig.js")], capture_output=True, text=True).stdout)
            p, r, _ = run(t2, v2m, asof=asof, P=P, cfg_edit=lambda c: c["approvedVerdictCode"].update({h: "test" for h in sig.values() if isinstance(h, str)}))
            check("승인된 해시 + 가중치 1 → 구조 변경 보류", r and r["reason"] == "structure", (r or {}).get("reason"))

        # 4 날짜
        p, r, _ = run(tmp, v2, asof="15-Oct-2026", P=P)
        check("S ≠ P → 보유 파일 날짜 보류", r and r["reason"] == "file_date", (r or {}).get("reason"))
        with tempfile.TemporaryDirectory() as d2:
            t2 = Path(d2)
            v2m = tree(t2, lambda h, t: h.replace(f'["{P}",', '["2099-01-01",') if t == "NVDA" else h)
            p, r, _ = run(t2, v2m, asof=asof, P=P)
            ex = r and next((c for c in r["cards"] if c["card"] == "NVDA"), {})
            check("카드 하나 날짜 다름 → 그 카드만 날짜 불일치 제외", r and ex.get("excluded") == ["날짜 불일치"], ex)

        # 5 입력
        bad = base_lines(); bad[0][4] = -1.0
        p, r, _ = run(tmp, v2, lines=bad, asof=asof, P=P)
        check("음수 Weight → 입력 오류", r and r["reason"] == "input", (r or {}).get("reason"))
        bad = base_lines(); bad[1][4] = None
        p, r, _ = run(tmp, v2, lines=bad, asof=asof, P=P)
        check("빈 Weight → 입력 오류", r and r["reason"] == "input", (r or {}).get("reason"))
        bad = base_lines(); bad.append(["DUP", "DUPX", "IDNVDA", "-", 0.1, "-", 1.0, "USD"])
        p, r, _ = run(tmp, v2, lines=bad, asof=asof, P=P)
        check("같은 Identifier 두 줄 → 입력 오류", r and r["reason"] == "input", (r or {}).get("reason"))
        bad = base_lines(); bad.append(["WEIRD", "12345X", "", "-", 5.0, "-", 1.0, "USD"])
        p, r, _ = run(tmp, v2, lines=bad, asof=asof, P=P)
        check("분류 안 됨 > 0.5% → 보류", r and r["reason"] == "unclassified", (r or {}).get("reason"))

        # 5b 오류 경로에서도 운용사 Identifier·비중이 공개 산출물에 안 샌다
        for bad_name, bad in (("음수", [r[:4] + [-1.0] + r[5:] if i == 0 else r for i, r in enumerate(base_lines())]),
                              ("중복", base_lines() + [["DUP", "DUPX", "IDNVDA", "-", 0.1, "-", 1.0, "USD"]])):
            p, r, out = run(tmp, v2, lines=bad, asof=asof, P=P)
            pub = "".join((out / f).read_text(encoding="utf-8") for f in ("v2/etf/SPY.json", "preview-only-etf-spy.html", "preview-only-etf-data.js")) + p.stdout
            check(f"입력 오류({bad_name}) 공개 산출물·로그에 Identifier·Weight 없음", "IDNVDA" not in pub and "-1.0" not in pub, [s for s in ("IDNVDA", "-1.0") if s in pub])

        # 5c 보류여도 S를 기록, 사유 우선순위(분류 안 됨 + 코드 변경 → 코드 변경, 둘 다 기록)
        p, r, _ = run(tmp, v2, asof="15-Oct-2026", P=P)
        check("보유 파일 날짜 보류에도 S 기록", r and r["S"] == "2026-10-15", (r or {}).get("S"))
        with tempfile.TemporaryDirectory() as d2:
            t2 = Path(d2)
            v2m = tree(t2, lambda h, t: h.replace("s >= 70 ? 1", "s >= 60 ? 1"))
            bad = base_lines(); bad.append(["WEIRD", "12345X", "", "-", 5.0, "-", 1.0, "USD"])
            p, r, _ = run(t2, v2m, lines=bad, asof=asof, P=P)
            keys = [x["key"] for x in (r or {}).get("reasons", [])]
            check("분류 안 됨 + 코드 변경 → 대표 코드 변경, 둘 다 기록", r and r["reason"] == "code_sig" and "unclassified" in keys, keys)

        # 5e 추출기가 통째로 실패해도 먼저 모은 날짜 보류가 대표(우선순위), 둘 다 기록
        with tempfile.TemporaryDirectory() as d2:
            t2 = Path(d2)
            v2m = tree(t2)
            (v2m / "research" / "extract_card_verdicts.js").write_text("process.exit(3)\n")
            p, r, _ = run(t2, v2m, asof="15-Oct-2026", P=P)
            keys = [x["key"] for x in (r or {}).get("reasons", [])]
            check("추출기 실패 + S≠P → 대표 보유 파일 날짜, 추출기 실패도 기록", r and r["reason"] == "file_date" and "tools" in keys, keys)
            (v2m / "research" / "extract_card_verdicts.js").write_text("console.log('not json')\n")
            p, r, _ = run(t2, v2m, asof=asof, P=P)
            check("추출기 깨진 출력 → 카드 판정 추출기 실패", r and r["reason"] == "tools", (r or {}).get("reason"))

        # 5f 입력 오류에도 S 기록, 한 자리 날짜
        bad = base_lines(); bad[0][4] = -1.0
        p, r, _ = run(tmp, v2, lines=bad, asof=asof, P=P)
        check("입력 오류 보류에도 S 기록", r and r["S"] == P, (r or {}).get("S"))
        p, r, _ = run(tmp, v2, asof="6-Oct-2026", P="2026-10-06")
        check("한 자리 날짜 'As of 6-Oct-2026' 읽음", r and r["S"] == "2026-10-06", (r or {}).get("S"))

        # 5d 추출이 깨진 카드도 서명을 본다
        with tempfile.TemporaryDirectory() as d2:
            t2 = Path(d2)
            v2m = tree(t2, lambda h, t: h.replace("종합 평가 자동 판정", "종합 평가") if t == "ELV" else h)
            p, r, _ = run(t2, v2m, asof=asof, P=P)
            check("추출 실패 카드(ELV) → 코드 변경 보류(작은 카드라도)", r and r["reason"] == "code_sig", (r or {}).get("reasons"))

        # 6 덮은 비중 부족
        low = base_lines(); low[-2][4] = 40.0
        p, r, _ = run(tmp, v2, lines=low, asof=asof, P=P)
        check("c < 70% → 덮은 비중 부족", r and r["reason"] == "coverage" and r["verdict"] is None, (r or {}).get("reason"))

        # 7 받기 실패 → 세 산출물 보류
        p, r, out = run(tmp, v2, asof=asof, P=P, no_xlsx=True, cfg_edit=lambda c: c["funds"]["SPY"].update({"holdingsUrl": "http://127.0.0.1:9/none.xlsx"}))
        dj = (out / "preview-only-etf-data.js").read_text(encoding="utf-8")
        check("받기 실패 → 보류, 데이터 파일도 보류", r and r["reason"] == "fetch_fail" and '"status": "held"' in dj, (r or {}).get("reason"))

        # 8 본체가 깨지면 대체 단계
        broken = tmp / "broken.py"
        broken.write_text("import this_module_does_not_exist\n")
        p, r, out = run(tmp, v2, asof=asof, P=P, script=broken)
        check("깨진 본체는 0이 아닌 종료(워크플로가 대체 단계를 부름)", p.returncode != 0, p.returncode)
        fb = subprocess.run([sys.executable, str(V2 / "etf" / "etf_fallback.py"), "--out-root", str(out)], capture_output=True, text=True)
        r = json.loads((out / "v2/etf/SPY.json").read_text(encoding="utf-8"))
        html_ok = 'data-status="held"' in (out / "preview-only-etf-spy.html").read_text(encoding="utf-8")
        check("대체 단계 → 세 산출물 보류(카드 페이지 포함)", fb.returncode == 0 and r["reason"] == "run_fail" and html_ok, r.get("reason"))
        sys.path.insert(0, str(V2 / "etf"))
        import etf_daily as ed
        left = ed.consistency(r, (out / "v2/etf/SPY.json", out / "preview-only-etf-spy.html", out / "preview-only-etf-data.js"))
        check("대체 단계 세 산출물도 서로 일치", not left, left)
        (out / "preview-only-etf-data.js").write_text("window.ETF_DATA = [];\n", encoding="utf-8")
        p, r, out = run(tmp, v2, asof=asof, P=P)
        check("데이터 파일이 배열이어도 본체 정상", p.returncode == 0 and r["status"] == "ok", p.returncode)

        # 9 자체 검사: 산출물 하나를 어긋나게 쓰면 잡는가
        sys.path.insert(0, str(V2 / "etf"))
        import etf_daily
        orig = etf_daily.summary
        # 정상 판정일 때만 홈 데이터의 n̄를 어긋나게 쓰는 결함(보류로 다시 쓸 때는 정상)
        etf_daily.summary = lambda res: dict(orig(res), nbar=res["nbar"] + 1 if res.get("nbar") is not None else None)
        p2, r2, out2 = None, None, tmp / "out_sc"
        sys.argv = ["etf_daily.py", "--out-root", str(out2), "--v2", str(v2), "--stocks", str(tmp / "stocks.json"),
                    "--private", str(tmp / "private"), "--cfg", str(tmp / "cfg.json"), "--xlsx", str(tmp / "h.xlsx")]
        xlsx(tmp / "h.xlsx", holdings(asof, base_lines()))
        (tmp / "stocks.json").write_text(json.dumps({"priceSession": P}))
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()):
            etf_daily.main()
        etf_daily.summary = orig
        r = json.loads((out2 / "v2/etf/SPY.json").read_text(encoding="utf-8"))
        check("홈 데이터만 어긋나면 자체 검사 → 보류", r["reason"] == "selfcheck", r.get("reason"))
        left = etf_daily.consistency(r, (out2 / "v2/etf/SPY.json", out2 / "preview-only-etf-spy.html", out2 / "preview-only-etf-data.js"))
        check("자체 검사 재작성 뒤 세 산출물 일치", not left, left)

        # 10 다른 ETF 칸은 지우지 않는다
        dj = out2 / "preview-only-etf-data.js"
        dj.write_text('window.ETF_DATA = {"QQQ": {"status": "held"}, "SPY": {}};\n', encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            etf_daily.main()
        check("데이터 파일의 다른 ETF 칸 유지", "QQQ" in etf_daily.read_data_js(dj))

    print(f"\n{'모두 통과' if not FAILS else f'실패 {len(FAILS)}건: ' + ', '.join(FAILS)}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
