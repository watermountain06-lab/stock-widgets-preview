#!/usr/bin/env python3
"""ETF 일상 운영 자동화(2026-10-20 설계 dr 합의) 검사 — 저장소를 건드리지 않는다(임시 폴더, 가짜 gh).

    python3 v2/etf/test_etf_auto.py

갱신 대기 유지·해제(keep_on_lag), 종류별 검사 상태(checks), 관측 기록(date_obs.jsonl), 서명 스크립트·판정 추출기의 종료와
조각 컴파일 검사, 승인 스크립트(etf_approve.py), 알림(etf_alerts.py — 종류로 찾기, 키 바뀌면 댓글, ok일 때만 닫기,
검사 못 함이면 유지, 이어질 때만 알리는 종류).
"""
import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import etf_daily  # noqa: E402
import etf_alerts  # noqa: E402
import etf_approve  # noqa: E402
import test_etf as T  # noqa: E402  (가짜 xlsx·카드 사본 도우미)

FAILS = []


def check(name, ok, got=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  -> {got}"))
    if not ok:
        FAILS.append(name)


def held_res(S, keys=("file_date",)):
    return {"status": "held", "S": S, "reasons": [{"key": k, "text": k, "detail": ""} for k in keys]}


def ok_prev(built, S=None):
    return {"status": "ok", "verdict": "적정", "builtFor": built, "S": S or built, "nbar": 0.0}


def test_keep():
    real = etf_daily.prev_session
    etf_daily.prev_session = lambda p, v2: {"2026-10-20": "2026-10-19", "2026-10-19": "2026-10-16"}.get(p)
    try:
        k = etf_daily.keep_on_lag
        r = k(held_res("2026-10-19"), ok_prev("2026-10-19"), "2026-10-20", None)
        check("S<P, 직전 = P 직전 세션 판정 → 유지 issuer_lag", r and r["pending"] == {"kind": "issuer_lag", "P": "2026-10-20", "S": "2026-10-19"}
              and r["builtFor"] == "2026-10-19" and r["status"] == "ok", r)
        r = k(held_res("2026-10-16"), ok_prev("2026-10-20"), "2026-10-20", None)
        check("S<P, 직전이 이미 P 세션 판정 → 유지 issuer_lag", r and r["pending"]["kind"] == "issuer_lag" and r["builtFor"] == "2026-10-20", r)
        rv = dict(held_res("2026-10-19"), ruleVersion="2")
        check("그 뒤 규칙 버전이 바뀜 → 보류", k(rv, dict(ok_prev("2026-10-19"), ruleVersion="1"), "2026-10-20", None) is None)
        ih = dict(held_res("2026-10-19"), inputHash={"extractor": "b"})
        check("그 뒤 판정 추출기가 바뀜 → 보류", k(ih, dict(ok_prev("2026-10-19"), inputHash={"extractor": "a"}), "2026-10-20", None) is None)
        check("S<P, 직전이 두 세션 전 → 보류", k(held_res("2026-10-16"), ok_prev("2026-10-16"), "2026-10-20", None) is None)
        check("다른 사유가 섞이면 → 보류", k(held_res("2026-10-19", ("file_date", "code_sig")), ok_prev("2026-10-19"), "2026-10-20", None) is None)
        check("직전이 보류 → 보류", k(held_res("2026-10-19"), {"status": "held", "builtFor": "2026-10-19"}, "2026-10-20", None) is None)
        check("직전 판정의 S ≠ builtFor → 보류", k(held_res("2026-10-19"), ok_prev("2026-10-19", S="2026-10-16"), "2026-10-20", None) is None)
        r = k(held_res("2026-10-21"), ok_prev("2026-10-20"), "2026-10-20", None)
        check("S>P, 직전 = P 세션 판정 → 유지 home_lag", r and r["pending"]["kind"] == "home_lag", r)
        check("S>P, 직전이 P 세션 아님 → 보류", k(held_res("2026-10-21"), ok_prev("2026-10-19"), "2026-10-20", None) is None)
        check("달력에 P 없음 → 보류", k(held_res("2026-10-30"), ok_prev("2026-10-30"), "2026-10-31", None) is None)
        etf_daily.prev_session = lambda p, v2: (_ for _ in ()).throw(ValueError("x"))
        check("달력 읽기 실패 → 보류", k(held_res("2026-10-19"), ok_prev("2026-10-19"), "2026-10-20", None) is None)
    finally:
        etf_daily.prev_session = real


def test_runs(tmp, v2, P, asof):
    # S = P면 직전 산출물의 pending이 사라진다(새 판정으로 덮음)
    out = tmp / "out"
    (out / "v2" / "etf").mkdir(parents=True, exist_ok=True)
    (out / "v2" / "etf" / "SPY.json").write_text(json.dumps(dict(ok_prev(P), pending={"kind": "issuer_lag", "P": P, "S": "x"})))
    p, r, _ = T.run(tmp, v2, asof=asof, P=P)
    check("S = P 실행이면 pending 해제", r and r["status"] == "ok" and not r.get("pending"), r and r.get("pending"))
    check("정상 실행 checks 모두 ok", r and all(v == "ok" for v in r["checks"].values()), r and r["checks"])
    obs = [json.loads(x) for x in (out / "v2" / "etf" / "date_obs.jsonl").read_text().splitlines()]
    check("관측 한 줄(P·S·해시·평가)", obs and obs[-1]["P"] == P and obs[-1]["S"] == P and obs[-1]["eval"] == "ok"
          and len(obs[-1]["file_sha12"] or "") == 12 and obs[-1]["kept"] is None, obs[-1:])
    # 받기 실패도 한 줄(S·해시 null), checks: fetch bad, 나머지 검사 못 함
    (tmp / "stocks.json").write_text(json.dumps({"priceSession": P}))
    subprocess.run([sys.executable, str(HERE / "etf_daily.py"), "--out-root", str(out), "--v2", str(v2), "--stocks", str(tmp / "stocks.json"),
                    "--private", str(tmp / "private"), "--cfg", str(tmp / "cfg.json"), "--xlsx", str(tmp / "없는파일.xlsx")],
                   capture_output=True, text=True)
    r = json.loads((out / "v2" / "etf" / "SPY.json").read_text())
    obs = [json.loads(x) for x in (out / "v2" / "etf" / "date_obs.jsonl").read_text().splitlines()]
    check("받기 실패: 관측 한 줄(S·해시 null)", obs[-1]["S"] is None and obs[-1]["file_sha12"] is None and "fetch_fail" in obs[-1]["holds"], obs[-1])
    check("받기 실패: fetch bad, 뒤 종류는 검사 못 함", r["checks"]["fetch"] == "bad" and r["checks"]["code_sig"] == "unchecked"
          and r["checks"]["file_date"] == "unchecked", r["checks"])
    # 입력 오류(머리 줄 없음): input bad, 도구·서명 검사 못 함
    T.xlsx(tmp / "bad.xlsx", [["Holdings:", f"As of {asof}"], [], ["아무 머리"]])
    subprocess.run([sys.executable, str(HERE / "etf_daily.py"), "--out-root", str(out), "--v2", str(v2), "--stocks", str(tmp / "stocks.json"),
                    "--private", str(tmp / "private"), "--cfg", str(tmp / "cfg.json"), "--xlsx", str(tmp / "bad.xlsx")], capture_output=True, text=True)
    r = json.loads((out / "v2" / "etf" / "SPY.json").read_text())
    obs = [json.loads(x) for x in (out / "v2" / "etf" / "date_obs.jsonl").read_text().splitlines()]
    check("입력 오류: 관측 holds가 알림의 input 사유와 맞음", set(obs[-1]["holds"]) & etf_alerts.CONSEC["input"][1], obs[-1]["holds"])
    check("입력 오류: input bad, tools·code_sig 검사 못 함", r["checks"]["input"] == "bad" and r["checks"]["tools"] == "unchecked"
          and r["checks"]["code_sig"] == "unchecked", r["checks"])
    # 미승인 해시: code_sig bad + 구조화 상세(해시 → 카드)
    p, r, _ = T.run(tmp, v2, asof=asof, P=P, cfg_edit=lambda c: c.update(approvedVerdictCode={}))
    d = r["checkDetail"].get("code_sig") or {}
    check("미승인 해시: checks bad + 해시→카드 상세", r["checks"]["code_sig"] == "bad" and d and all(isinstance(v, list) for v in d.values())
          and "NVDA" in sum(d.values(), []), d)


def test_scanners(tmp):
    v2 = tmp / "scan" / "v2"
    (v2 / "etf").mkdir(parents=True)
    (v2 / "research").mkdir()
    shutil.copy(HERE / "verdict_code_sig.js", v2 / "etf")
    shutil.copy(HERE.parent / "research" / "extract_card_verdicts.js", v2 / "research")
    (v2 / "OK_full_widget.html").write_text("<script>function dcfLevel(p,D){ return 1 }\n// 종합 평가 자동 판정\n(function(){ var x=1; })();\n// 끝 개행 없는 주석")
    (v2 / "RX_full_widget.html").write_text("<script>// 종합 평가 자동 판정\n(function(){ var r=/\\}/; if (x>30) {} })();\n")
    (v2 / "NC_full_widget.html").write_text("<script>// 종합 평가 자동 판정\n(function(){ var a=1; /* 닫히지 않는 주석")
    (v2 / "LC_full_widget.html").write_text("<script>// 종합 평가 자동 판정\n(function(){ var a=1; // 개행 없이 끝나는 주석")
    for name, script in (("서명", v2 / "etf" / "verdict_code_sig.js"), ("추출기", v2 / "research" / "extract_card_verdicts.js")):
        try:
            p = subprocess.run(["node", str(script)], capture_output=True, text=True, timeout=30)
            check(f"{name}: 개행 없는 끝 주석·닫히지 않은 주석에서도 끝남", p.returncode == 0, p.returncode)
        except subprocess.TimeoutExpired:
            check(f"{name}: 개행 없는 끝 주석·닫히지 않은 주석에서도 끝남", False, "30초 초과")
    out = json.loads(subprocess.run(["node", str(v2 / "etf" / "verdict_code_sig.js")], capture_output=True, text=True).stdout)
    check("서명: 정규식 속 }로 일찍 잘리면 오류(컴파일 실패)", isinstance(out["RX"], dict) and "컴파일" in out["RX"]["error"], out["RX"])
    check("서명: 닫히지 않은 주석이면 오류", isinstance(out["NC"], dict) and "끝 없음" in out["NC"]["error"], out["NC"])
    check("서명: 판정 범위 안에서 개행 없이 끝나는 // 주석이면 오류", isinstance(out["LC"], dict) and "끝 없음" in out["LC"]["error"], out["LC"])
    check("서명: 정상 카드는 해시", isinstance(out["OK"], str) and len(out["OK"]) == 12, out["OK"])
    txt = json.loads(subprocess.run(["node", str(v2 / "etf" / "verdict_code_sig.js"), "--text"], capture_output=True, text=True).stdout)
    import hashlib
    check("서명 --text: sha256(text) 앞 12자 = 해시", hashlib.sha256(txt["OK"]["text"].encode()).hexdigest()[:12] == out["OK"])


def test_approve(tmp, v2):
    cfg = tmp / "acfg.json"
    base = json.loads((HERE / "ticker_alias.json").read_text(encoding="utf-8"))
    base["approvedVerdictCode"] = {}
    cfg.write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    src = tmp / "asrc"
    sig = json.loads(subprocess.run(["node", str(v2 / "etf" / "verdict_code_sig.js")], capture_output=True, text=True).stdout)
    h = sig["NVDA"]
    with contextlib.redirect_stdout(io.StringIO()):
        rc_bad = etf_approve.main(["--hashes", "0123456789ab", "--v2", str(v2), "--cfg", str(cfg), "--src", str(src)])
        rc_fmt = etf_approve.main(["--hashes", "XYZ", "--v2", str(v2), "--cfg", str(cfg), "--src", str(src)])
        rc = etf_approve.main(["--hashes", h, "--note", "시험", "--v2", str(v2), "--cfg", str(cfg), "--src", str(src)])
        after1 = cfg.read_text(encoding="utf-8")
        rc2 = etf_approve.main(["--hashes", h, "--v2", str(v2), "--cfg", str(cfg), "--src", str(src)])
    check("승인: 지금 카드가 안 내는 해시 거부(2)", rc_bad == 2)
    check("승인: 해시 형식 아님 거부(2)", rc_fmt == 2)
    a = json.loads(after1)["approvedVerdictCode"]
    check("승인: 목록에 추가 + 원문 저장(해시 검증)", rc == 0 and h in a and "시험" in a[h] and (src / f"{h}.js").exists()
          and __import__("hashlib").sha256((src / f"{h}.js").read_text(encoding="utf-8").encode()).hexdigest()[:12] == h, a)
    check("승인: 같은 해시 다시 → 무해(설정 그대로)", rc2 == 0 and cfg.read_text(encoding="utf-8") == after1)


class FakeGH:
    def __init__(self, issues=None):
        self.issues, self.calls, self.n = list(issues or []), [], 100

    def __call__(self, args, stdin=None):
        self.calls.append((args[:2], stdin))
        if args[:2] == ["issue", "list"]:
            return json.dumps(self.issues)
        if args[:2] == ["issue", "create"]:
            self.n += 1
            self.issues.append({"number": self.n, "title": args[args.index("--title") + 1], "body": stdin})
        if args[:2] == ["issue", "edit"]:
            for i in self.issues:
                if str(i["number"]) == args[2]:
                    i["body"] = stdin
        if args[:2] == ["issue", "close"]:
            self.issues = [i for i in self.issues if str(i["number"]) != args[2]]
        return ""


def acts_of(gh):
    return [a[0][1] for a in gh.calls if a[0][1] != "list"]


def test_alerts(tmp, v2):
    root = tmp / "alert"
    (root / "v2" / "etf").mkdir(parents=True)
    spy, obs = root / "v2" / "etf" / "SPY.json", root / "v2" / "etf" / "date_obs.jsonl"
    allok = {k: "ok" for k in etf_daily.CHECK_KINDS}

    def put(checks, detail=None, runs=(), S="2026-10-16", P="2026-10-19", last_at="t"):
        spy.write_text(json.dumps({"etf": "SPY", "runAt": "t", "builtFor": "2026-10-19", "checks": checks, "checkDetail": detail or {}, "reasons": []}))
        rows = [{"etf": "SPY", "holds": h, "S": S, "P": P, "at": "old"} for h in runs]
        if rows:
            rows[-1]["at"] = last_at
        obs.write_text("".join(json.dumps(r) + "\n" for r in rows))

    gh = FakeGH()
    put(dict(allok, code_sig="bad"), {"code_sig": {"aaaaaaaaaaaa": ["NVDA"]}})
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh)
    check("알림: code_sig 새 이슈", acts_of(gh) == ["create"] and gh.issues[0]["title"].startswith("[ETF SPY code_sig]")
          and "etf-key: " in gh.issues[0]["body"] and "hashes = `aaaaaaaaaaaa`" in gh.issues[0]["body"], acts_of(gh))
    gh.calls.clear()
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh)
    check("알림: 같은 키 → 아무것도 안 함", acts_of(gh) == [], acts_of(gh))
    put(dict(allok, code_sig="bad"), {"code_sig": {"aaaaaaaaaaaa": ["NVDA"], "bbbbbbbbbbbb": ["JPM"]}})
    gh.calls.clear()
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh)
    check("알림: 키 바뀜 → 같은 이슈에 댓글·본문 갱신(새 이슈 아님)", acts_of(gh) == ["comment", "edit"] and len(gh.issues) == 1, acts_of(gh))
    put(dict(allok, code_sig="unchecked", tools="bad", fetch="bad"), runs=[["fetch_fail"]])
    gh.calls.clear()
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh)
    check("알림: 검사 못 함이면 code_sig 이슈 유지, 받기 실패 1회는 알림 없음", acts_of(gh) == [] and len(gh.issues) == 1, acts_of(gh))
    put(dict(allok, code_sig="unchecked", fetch="bad"), runs=[["fetch_fail"], ["fetch_fail"]])
    gh.calls.clear()
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh)
    check("알림: 받기 실패 2회 연속 → 새 이슈(fetch)", acts_of(gh) == ["create"] and any(i["title"].startswith("[ETF SPY fetch]") for i in gh.issues))
    put(dict(allok, structure="bad"), {"structure": ["JPM"]}, runs=[["structure"]])
    gh.calls.clear()
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh)
    titles = sorted(i["title"].split("]")[0] for i in gh.issues)
    check("알림: code_sig ok → code_sig만 닫고, fetch ok → 닫고, structure 새로", acts_of(gh).count("close") == 2 and titles == ["[ETF SPY structure"], (acts_of(gh), titles))
    gh2 = FakeGH()
    put(dict(allok, file_date="bad"), runs=[["file_date"]] * 5)
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh2)
    check("알림: 날짜 보류 5회 연속은 알림 없음(저녁마다 정상)", acts_of(gh2) == [])
    put(dict(allok, file_date="bad"), runs=[["file_date"]] * 6, S="2026-10-21", P="2026-10-20")
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh2)
    check("알림: 홈 세션 지연(S>P) 6회는 알림 없음", acts_of(gh2) == [])
    put(dict(allok, file_date="bad"), runs=[["file_date"]] * 6)
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh2)
    check("알림: 운용사 지연 6회 연속 → 알림", acts_of(gh2) == ["create"])
    gh4 = FakeGH()
    put(dict(allok, tools="ok"), runs=[["tools"], ["tools"]])
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh4)
    check("알림: 이번 실행 ok면 과거 연속 실패가 있어도 알림 없음", acts_of(gh4) == [])
    put(dict(allok, tools="unchecked"), runs=[["tools"], ["tools"]])
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh4)
    check("알림: 이번 실행이 검사 못 함이면 알림 없음", acts_of(gh4) == [])
    put(dict(allok, tools="bad"), runs=[["tools"], ["tools"]], last_at="다른 실행")
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh4)
    check("알림: 실행 기록 마지막 줄이 이번 실행이 아니면 판단 안 함", acts_of(gh4) == [])
    put(dict(allok, tools="bad"), runs=[["tools"], ["tools"]])
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh4)
    check("알림: 이번 bad + 2회 연속 → 알림(tools)", acts_of(gh4) == ["create"])
    gh5 = FakeGH()
    real_body, etf_alerts.code_sig_body = etf_alerts.code_sig_body, lambda res, v2, repo: "```diff\n" + "+x\n" * 30000 + "```\n링크"
    try:
        put(dict(allok, code_sig="bad"), {"code_sig": {"cccccccccccc": ["NVDA"]}})
        etf_alerts.run("SPY", root, v2, "o/r", runner=gh5)
    finally:
        etf_alerts.code_sig_body = real_body
    b = gh5.issues[0]["body"] if gh5.issues else ""
    check("알림: 본문이 길면 diff를 빼고 링크만으로 연다", acts_of(gh5) == ["create"] and len(b) <= etf_alerts.BODY_MAX and "생략" in b, len(b))
    # diff를 빼도 긴 본문(대상 티커가 아주 많음): 표식이 남아 두 번째 실행은 아무것도 안 함
    gh6 = FakeGH()
    many = [f"T{i:05d}" for i in range(6000)]
    put(dict(allok, unclassified="bad"), {"unclassified": many})
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh6)
    gh6.calls.clear()
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh6)
    b = gh6.issues[0]["body"] if gh6.issues else ""
    check("알림: 아주 긴 본문도 한도 안 + 표식 보존 → 두 번째 실행 무동작", len(b) <= etf_alerts.BODY_MAX and "etf-key: " in b and acts_of(gh6) == [], (len(b), acts_of(gh6)))
    # 같은 실행이 두 줄(본 단계 + 대체 단계)이면 한 번으로 센다
    gh7 = FakeGH()
    put(dict(allok, run="bad"), runs=[["selfcheck"], ["run_fail"]])
    rows = [json.loads(x) for x in obs.read_text().splitlines()]
    for r in rows:
        r.update(run_id="9", attempt="1")
    obs.write_text("".join(json.dumps(r) + "\n" for r in rows))
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh7)
    check("알림: 같은 실행의 두 줄은 한 번 — 2회 연속 아님", acts_of(gh7) == [], acts_of(gh7))
    gh3 = FakeGH()
    put(dict(allok, unclassified="bad"), {"unclassified": ["ZZZ1"]})
    etf_alerts.run("SPY", root, v2, "o/r", runner=gh3)
    check("알림: 분류 안 됨 → 새 이슈(대상 티커)", acts_of(gh3) == ["create"] and "ZZZ1" in gh3.issues[0]["body"])


def test_fallback_and_hang(tmp, v2, P, asof):
    import etf_fallback
    check("대체 단계의 검사 종류·확인 키 = 본 단계", etf_fallback.CHECK_KINDS == etf_daily.CHECK_KINDS and etf_fallback.CHECK_KEYS == etf_daily.CHECK_KEYS)
    # 대체 단계: 검사 결과 run bad(나머지 검사 못 함) + 관측 한 줄
    out = tmp / "fb"
    (out / "v2" / "etf").mkdir(parents=True)
    subprocess.run([sys.executable, str(HERE / "etf_fallback.py"), "--out-root", str(out)], capture_output=True, text=True)
    r = json.loads((out / "v2" / "etf" / "SPY.json").read_text())
    obs = [json.loads(x) for x in (out / "v2" / "etf" / "date_obs.jsonl").read_text().splitlines()]
    check("대체 단계: run bad·나머지 검사 못 함·관측 한 줄", r["checks"]["run"] == "bad" and r["checks"]["code_sig"] == "unchecked"
          and obs[-1]["holds"] == ["run_fail"] and obs[-1]["at"] == r["runAt"], (r.get("checks"), obs[-1:]))
    # 문제 카드(판정 범위 안에서 개행 없이 끝나는 //)가 있어도 ETF 계산 전체가 끝난다
    v2h = tmp / "hang" / "v2"
    shutil.copytree(v2, v2h)
    (v2h / "LC_full_widget.html").write_text("<script>// 종합 평가 자동 판정\n(function(){ var a=1; // 개행 없이 끝나는 주석")
    try:
        p = subprocess.run([sys.executable, str(HERE / "etf_daily.py"), "--out-root", str(tmp / "hang" / "out"), "--v2", str(v2h),
                            "--stocks", str(tmp / "stocks.json"), "--private", str(tmp / "hang" / "pv"), "--cfg", str(tmp / "cfg.json"),
                            "--xlsx", str(tmp / "h.xlsx")], capture_output=True, text=True, timeout=180)
        r = json.loads((tmp / "hang" / "out" / "v2" / "etf" / "SPY.json").read_text())
        check("문제 카드가 있어도 ETF 계산이 끝남(도구 실패 아님)", p.returncode == 0 and r["checks"]["tools"] == "ok", r.get("checks"))
    except subprocess.TimeoutExpired:
        check("문제 카드가 있어도 ETF 계산이 끝남(도구 실패 아님)", False, "180초 초과")
    # 유지한 산출물: 입력 해시·받은 시각은 판정을 낸 직전 것, 이번 것은 pending에
    o2 = tmp / "keep"
    (o2 / "v2" / "etf").mkdir(parents=True)
    T.run(tmp, v2, asof=asof, P=P)   # tmp/out에 정상 판정
    prev = json.loads((tmp / "out" / "v2" / "etf" / "SPY.json").read_text())
    (o2 / "v2" / "etf" / "SPY.json").write_text(json.dumps(prev))
    T.xlsx(tmp / "old.xlsx", T.holdings("15-Oct-2026", T.base_lines()))
    subprocess.run([sys.executable, str(HERE / "etf_daily.py"), "--out-root", str(o2), "--v2", str(v2), "--stocks", str(tmp / "stocks.json"),
                    "--private", str(tmp / "pv2"), "--cfg", str(tmp / "cfg.json"), "--xlsx", str(tmp / "old.xlsx")], capture_output=True, text=True)
    r = json.loads((o2 / "v2" / "etf" / "SPY.json").read_text())
    check("유지: 입력 해시는 직전 것, 이번 해시·시각은 pending에", r.get("pending") and r["inputHash"] == prev["inputHash"]
          and r["pending"]["inputHash"]["xlsx"] != prev["inputHash"]["xlsx"] and r["pending"].get("at") == r["runAt"]
          and r.get("fetchedAt") == prev.get("fetchedAt") and r.get("ruleVersion") == prev.get("ruleVersion")
          and r["pending"].get("ruleVersion"), r.get("pending"))


def main():
    test_keep()
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        v2 = T.tree(tmp)
        P = json.loads(subprocess.run(["node", str(v2 / "research" / "extract_card_verdicts.js")], capture_output=True, text=True).stdout)["NVDA"]["date"]
        asof = __import__("datetime").datetime.strptime(P, "%Y-%m-%d").strftime("%d-%b-%Y")
        test_runs(tmp, v2, P, asof)
        test_fallback_and_hang(tmp, v2, P, asof)
        test_scanners(tmp)
        test_approve(tmp, v2)
        test_alerts(tmp, v2)
    print(f"\n{'모두 통과' if not FAILS else f'실패 {len(FAILS)}건: ' + ', '.join(FAILS)}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
