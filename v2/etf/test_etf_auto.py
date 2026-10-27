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

    def both(root, v2, gh):   # ETF별 알림 + ETF 공통 code_sig 이슈(2026-10-21) — 승인 목록은 비었다고 본다
        return etf_alerts.run("SPY", root, v2, "o/r", runner=gh) + etf_alerts.run_code_sig(["SPY"], root, v2, "o/r", runner=gh, approved=set())

    def put(checks, detail=None, runs=(), S="2026-10-16", P="2026-10-19", last_at="t"):
        spy.write_text(json.dumps({"etf": "SPY", "runAt": "t", "builtFor": "2026-10-19", "checks": checks, "checkDetail": detail or {}, "reasons": []}))
        rows = [{"etf": "SPY", "holds": h, "S": S, "P": P, "at": "old"} for h in runs]
        if rows:
            rows[-1]["at"] = last_at
        obs.write_text("".join(json.dumps(r) + "\n" for r in rows))

    gh = FakeGH()
    put(dict(allok, code_sig="bad"), {"code_sig": {"aaaaaaaaaaaa": ["NVDA"]}})
    both(root, v2, gh)
    check("알림: code_sig 새 이슈", acts_of(gh) == ["create"] and gh.issues[0]["title"].startswith("[ETF code_sig]")
          and "etf-key: " in gh.issues[0]["body"] and "hashes = `aaaaaaaaaaaa`" in gh.issues[0]["body"], acts_of(gh))
    gh.calls.clear()
    both(root, v2, gh)
    check("알림: 같은 키 → 아무것도 안 함", acts_of(gh) == [], acts_of(gh))
    put(dict(allok, code_sig="bad"), {"code_sig": {"aaaaaaaaaaaa": ["NVDA"], "bbbbbbbbbbbb": ["JPM"]}})
    gh.calls.clear()
    both(root, v2, gh)
    check("알림: 키 바뀜 → 같은 이슈에 댓글·본문 갱신(새 이슈 아님)", acts_of(gh) == ["comment", "edit"] and len(gh.issues) == 1, acts_of(gh))
    put(dict(allok, code_sig="unchecked", tools="bad", fetch="bad"), runs=[["fetch_fail"]])
    gh.calls.clear()
    both(root, v2, gh)
    check("알림: 검사 못 함이면 code_sig 이슈 유지, 받기 실패 1회는 알림 없음", acts_of(gh) == [] and len(gh.issues) == 1, acts_of(gh))
    put(dict(allok, code_sig="unchecked", fetch="bad"), runs=[["fetch_fail"], ["fetch_fail"]])
    gh.calls.clear()
    both(root, v2, gh)
    check("알림: 받기 실패 2회 연속 → 새 이슈(fetch)", acts_of(gh) == ["create"] and any(i["title"].startswith("[ETF SPY fetch]") for i in gh.issues))
    put(dict(allok, structure="bad"), {"structure": ["JPM"]}, runs=[["structure"]])
    gh.calls.clear()
    both(root, v2, gh)
    titles = sorted(i["title"].split("]")[0] for i in gh.issues)
    check("알림: code_sig ok → code_sig만 닫고, fetch ok → 닫고, structure 새로", acts_of(gh).count("close") == 2 and titles == ["[ETF SPY structure"], (acts_of(gh), titles))
    gh2 = FakeGH()
    put(dict(allok, file_date="bad"), runs=[["file_date"]] * 5)
    both(root, v2, gh2)
    check("알림: 날짜 보류 5회 연속은 알림 없음(저녁마다 정상)", acts_of(gh2) == [])
    put(dict(allok, file_date="bad"), runs=[["file_date"]] * 6, S="2026-10-21", P="2026-10-20")
    both(root, v2, gh2)
    check("알림: 홈 세션 지연(S>P) 6회는 알림 없음", acts_of(gh2) == [])
    put(dict(allok, file_date="bad"), runs=[["file_date"]] * 6)
    both(root, v2, gh2)
    check("알림: 운용사 지연 6회 연속 → 알림", acts_of(gh2) == ["create"])
    gh4 = FakeGH()
    put(dict(allok, tools="ok"), runs=[["tools"], ["tools"]])
    both(root, v2, gh4)
    check("알림: 이번 실행 ok면 과거 연속 실패가 있어도 알림 없음", acts_of(gh4) == [])
    put(dict(allok, tools="unchecked"), runs=[["tools"], ["tools"]])
    both(root, v2, gh4)
    check("알림: 이번 실행이 검사 못 함이면 알림 없음", acts_of(gh4) == [])
    put(dict(allok, tools="bad"), runs=[["tools"], ["tools"]], last_at="다른 실행")
    both(root, v2, gh4)
    check("알림: 실행 기록 마지막 줄이 이번 실행이 아니면 판단 안 함", acts_of(gh4) == [])
    put(dict(allok, tools="bad"), runs=[["tools"], ["tools"]])
    both(root, v2, gh4)
    check("알림: 이번 bad + 2회 연속 → 알림(tools)", acts_of(gh4) == ["create"])
    gh5 = FakeGH()
    real_body, etf_alerts.code_sig_body = etf_alerts.code_sig_body, lambda res, v2, repo: "```diff\n" + "+x\n" * 30000 + "```\n링크"
    try:
        put(dict(allok, code_sig="bad"), {"code_sig": {"cccccccccccc": ["NVDA"]}})
        both(root, v2, gh5)
    finally:
        etf_alerts.code_sig_body = real_body
    b = gh5.issues[0]["body"] if gh5.issues else ""
    check("알림: 본문이 길면 diff를 빼고 링크만으로 연다", acts_of(gh5) == ["create"] and len(b) <= etf_alerts.BODY_MAX and "생략" in b, len(b))
    # diff를 빼도 긴 본문(대상 티커가 아주 많음): 표식이 남아 두 번째 실행은 아무것도 안 함
    gh6 = FakeGH()
    many = [f"T{i:05d}" for i in range(6000)]
    put(dict(allok, unclassified="bad"), {"unclassified": many})
    both(root, v2, gh6)
    gh6.calls.clear()
    both(root, v2, gh6)
    b = gh6.issues[0]["body"] if gh6.issues else ""
    check("알림: 아주 긴 본문도 한도 안 + 표식 보존 → 두 번째 실행 무동작", len(b) <= etf_alerts.BODY_MAX and "etf-key: " in b and acts_of(gh6) == [], (len(b), acts_of(gh6)))
    # 같은 실행이 두 줄(본 단계 + 대체 단계)이면 한 번으로 센다
    gh7 = FakeGH()
    put(dict(allok, run="bad"), runs=[["selfcheck"], ["run_fail"]])
    rows = [json.loads(x) for x in obs.read_text().splitlines()]
    for r in rows:
        r.update(run_id="9", attempt="1")
    obs.write_text("".join(json.dumps(r) + "\n" for r in rows))
    both(root, v2, gh7)
    check("알림: 같은 실행의 두 줄은 한 번 — 2회 연속 아님", acts_of(gh7) == [], acts_of(gh7))
    gh3 = FakeGH()
    put(dict(allok, unclassified="bad"), {"unclassified": ["ZZZ1"]})
    both(root, v2, gh3)
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


def test_code_sig_common(tmp, v2):
    root = tmp / "cs"
    (root / "v2" / "etf").mkdir(parents=True)
    allok = {k: "ok" for k in etf_daily.CHECK_KINDS}

    def put(etf, cs, hashes=None):
        (root / "v2" / "etf" / f"{etf}.json").write_text(json.dumps({"etf": etf, "runAt": "t", "builtFor": "2026-10-19",
            "checks": dict(allok, code_sig=cs), "checkDetail": {"code_sig": hashes} if hashes else {}, "reasons": []}))
    gh = FakeGH()
    put("SPY", "bad", {"aaaaaaaaaaaa": ["NVDA"]}); put("QQQ", "bad", {"aaaaaaaaaaaa": ["NVDA"], "bbbbbbbbbbbb": ["ASML"]})
    a1 = etf_alerts.run_code_sig(["SPY", "QQQ"], root, v2, "o/r", runner=gh, approved=set())
    b = gh.issues[0]["body"] if gh.issues else ""
    check("공통 code_sig: 두 ETF가 같은 해시여도 이슈 하나, 키 = 합집합", [x for x, _ in a1] == ["create"] and len(gh.issues) == 1
          and "etf-hashes: aaaaaaaaaaaa,bbbbbbbbbbbb" in b and gh.issues[0]["title"].startswith("[ETF code_sig]"), (a1, b[-120:]))
    put("SPY", "ok"); put("QQQ", "unchecked")
    a2 = etf_alerts.run_code_sig(["SPY", "QQQ"], root, v2, "o/r", runner=gh, approved=set())
    check("공통 code_sig: 한 ETF가 검사 못 함이면 열린 채로(닫지 않음)", a2 == [] and len(gh.issues) == 1, a2)
    put("SPY", "bad", {"cccccccccccc": ["JPM"]}); put("QQQ", "unchecked")
    a3 = etf_alerts.run_code_sig(["SPY", "QQQ"], root, v2, "o/r", runner=gh, approved={"aaaaaaaaaaaa"})
    b = gh.issues[0]["body"]
    check("공통 code_sig: 검사 못 한 ETF의 옛 미승인 해시는 남김(승인된 것은 뺌)", [x for x, _ in a3] == ["comment"]
          and "etf-hashes: bbbbbbbbbbbb,cccccccccccc" in b, b[-120:])
    put("SPY", "ok"); put("QQQ", "unchecked")
    a4 = etf_alerts.run_code_sig(["SPY", "QQQ"], root, v2, "o/r", runner=gh, approved={"bbbbbbbbbbbb", "cccccccccccc"})
    check("공통 code_sig: 해시가 모두 승인됐어도 검사 못 한 ETF가 있으면 열린 채로", a4 == [] and len(gh.issues) == 1, a4)
    put("SPY", "ok"); put("QQQ", "ok")
    a4b = etf_alerts.run_code_sig(["SPY", "QQQ"], root, v2, "o/r", runner=gh, approved=set())
    check("공통 code_sig: 모든 ETF가 이번 실행에서 ok → 닫음", [x for x, _ in a4b] == ["close"] and not gh.issues, a4b)
    # 승인 목록을 실제 설정 파일 경로에서 읽는지(approved 인자 없이)
    import shutil as _sh
    _sh.copy(HERE / "ticker_alias.json", root / "v2" / "etf" / "ticker_alias.json")
    real_ok = next(iter(json.loads((HERE / "ticker_alias.json").read_text(encoding="utf-8"))["approvedVerdictCode"]))
    gh8 = FakeGH([{"number": 5, "title": "[ETF code_sig] x", "body": f"<!-- etf-hashes: {real_ok},ffffffffffff -->"}])
    put("SPY", "bad", {"cccccccccccc": ["JPM"]}); put("QQQ", "unchecked")
    etf_alerts.run_code_sig(["SPY", "QQQ"], root, v2, "o/r", runner=gh8)
    b8 = gh8.issues[0]["body"]
    check("공통 code_sig: 실제 설정의 승인 목록으로 옛 해시를 거른다", f"etf-hashes: cccccccccccc,ffffffffffff" in b8 and real_ok not in b8.split("etf-hashes:")[1], b8[-90:])
    # 이번 실행 것이 아닌 산출물(runId 다름)은 검사 못 함
    import os as _os
    gh3 = FakeGH([{"number": 9, "title": "[ETF code_sig] x", "body": "<!-- etf-hashes: eeeeeeeeeeee -->"}])
    put("SPY", "ok"); put("QQQ", "ok")
    _os.environ["GITHUB_RUN_ID"], _os.environ["GITHUB_RUN_ATTEMPT"] = "77", "1"
    try:
        a6 = etf_alerts.run_code_sig(["SPY", "QQQ"], root, v2, "o/r", runner=gh3, approved=set())
        st6 = etf_alerts.states(json.loads((root / "v2" / "etf" / "SPY.json").read_text()), [])
    finally:
        del _os.environ["GITHUB_RUN_ID"], _os.environ["GITHUB_RUN_ATTEMPT"]
    check("공통 code_sig: 지난 실행의 산출물(runId 없음·다름)이면 ok여도 닫지 않음", a6 == [] and len(gh3.issues) == 1, a6)
    check("알림: 지난 실행의 산출물이면 모든 종류 검사 못 함", all(v[0] == "unchecked" for v in st6.values()), st6)
    # 지난 실행 산출물 + 이번 실행 관측에 실행 실패(복구 쓰기 실패) → run만 bad(2회 연속이면 알림), 다른 종류는 검사 못 함
    _os.environ["GITHUB_RUN_ID"], _os.environ["GITHUB_RUN_ATTEMPT"] = "77", "1"
    try:
        old = json.loads((root / "v2" / "etf" / "SPY.json").read_text())
        obs7 = [{"etf": "SPY", "holds": ["selfcheck"], "run_id": "76", "attempt": "1", "at": "a"},
                {"etf": "SPY", "holds": ["selfcheck"], "run_id": "77", "attempt": "1", "at": "b"}]
        st7 = etf_alerts.states(old, obs7)
    finally:
        del _os.environ["GITHUB_RUN_ID"], _os.environ["GITHUB_RUN_ATTEMPT"]
    check("알림: 지난 산출물 + 이번 실행 관측 selfcheck → run bad, code_sig는 검사 못 함", st7["run"][0] == "bad" and st7["code_sig"][0] == "unchecked", st7)
    gh2 = FakeGH([{"number": 7, "title": "[ETF SPY code_sig] 옛 제목", "body": "<!-- etf-hashes: dddddddddddd -->"}])
    put("SPY", "ok"); put("QQQ", "ok")
    a5 = etf_alerts.run_code_sig(["SPY", "QQQ"], root, v2, "o/r", runner=gh2, approved=set())
    check("공통 code_sig: 옛 제목 이슈도 찾고, 모두 ok면 닫음", [x for x, _ in a5] == ["close"], a5)


def test_isolation(tmp, v2, P, asof):
    """두 ETF 격리: QQQ 본 단계·대체 단계가 홈 데이터의 SPY 칸과 SPY 산출물을 건드리지 않는다(설계 r2 C-1)."""
    T.run(tmp, v2, asof=asof, P=P)   # tmp/out에 SPY 정상
    out = tmp / "out"
    data = lambda: etf_daily.read_data_js(out / "preview-only-etf-data.js")
    spy0, spyj0 = data().get("SPY"), (out / "v2" / "etf" / "SPY.json").read_text()
    subprocess.run([sys.executable, str(HERE / "etf_fallback.py"), "--etf", "QQQ", "--out-root", str(out)], capture_output=True, text=True)
    d1 = data()
    check("격리: QQQ 대체 단계 뒤 SPY 칸·SPY.json 그대로, QQQ 칸 보류", d1.get("SPY") == spy0 and d1.get("QQQ", {}).get("status") == "held"
          and (out / "v2" / "etf" / "SPY.json").read_text() == spyj0 and (out / "preview-only-etf-qqq.html").exists(), list(d1))
    (tmp / "qbad.json").write_text("not json")
    subprocess.run([sys.executable, str(HERE / "etf_daily.py"), "--etf", "QQQ", "--json", str(tmp / "qbad.json"), "--out-root", str(out),
                    "--v2", str(v2), "--stocks", str(tmp / "stocks.json"), "--private", str(tmp / "pvq"), "--cfg", str(HERE / "ticker_alias.json")],
                   capture_output=True, text=True)
    d2 = data()
    check("격리: QQQ 본 단계 보류(입력 오류) 뒤에도 SPY 칸 그대로", d2.get("SPY") == spy0 and d2.get("QQQ", {}).get("status") == "held", d2.get("QQQ"))
    # DIA(2026-10-21): 실제 설정으로 형식 A가 골라지고 DIA 산출물만 쓴다(SPY·QQQ 칸 그대로)
    qqq0 = d2.get("QQQ")
    T.xlsx(tmp / "dia.xlsx", T.holdings(asof, T.base_lines()))
    subprocess.run([sys.executable, str(HERE / "etf_daily.py"), "--etf", "DIA", "--xlsx", str(tmp / "dia.xlsx"), "--out-root", str(out),
                    "--v2", str(v2), "--stocks", str(tmp / "stocks.json"), "--private", str(tmp / "pvd"), "--cfg", str(HERE / "ticker_alias.json")],
                   capture_output=True, text=True)
    d3 = data()
    rd = json.loads((out / "v2" / "etf" / "DIA.json").read_text())
    check("DIA: 실제 설정 → 정상 판정(ok)·형식 A·DIA 산출물·보수 0.16, SPY·QQQ 칸 그대로", rd["status"] == "ok" and rd["verdict"] and rd["inputFormat"] == "ssga_xlsx" and rd["expense"]["pct"] == 0.16
          and d3.get("SPY") == spy0 and d3.get("QQQ") == qqq0 and "DIA" in d3 and (out / "preview-only-etf-dia.html").exists(), (rd.get("status"), rd.get("reason")))
    subprocess.run([sys.executable, str(HERE / "etf_fallback.py"), "--etf", "DIA", "--out-root", str(out)], capture_output=True, text=True)
    d4 = data()
    check("격리: DIA 대체 단계 뒤 SPY·QQQ 칸 그대로", d4.get("SPY") == spy0 and d4.get("QQQ") == qqq0 and d4["DIA"]["status"] == "held")
    # 가격형 칸(IWM — 카드 생성기가 씀)을 판정 단계·대체 단계가 지우지 않는다
    data_now = etf_daily.read_data_js(out / "preview-only-etf-data.js")
    data_now["IWM"] = {"etf": "IWM", "kind": "price", "status": "ok", "builtFor": P}
    etf_daily.write_atomic(out / "preview-only-etf-data.js", etf_daily.DATA_PREFIX + json.dumps(data_now, ensure_ascii=False) + ";\n")
    subprocess.run([sys.executable, str(HERE / "etf_fallback.py"), "--etf", "QQQ", "--out-root", str(out)], capture_output=True, text=True)
    subprocess.run([sys.executable, str(HERE / "etf_daily.py"), "--etf", "DIA", "--xlsx", str(tmp / "dia.xlsx"), "--out-root", str(out),
                    "--v2", str(v2), "--stocks", str(tmp / "stocks.json"), "--private", str(tmp / "pvd"), "--cfg", str(HERE / "ticker_alias.json")],
                   capture_output=True, text=True)
    check("격리: 판정·대체 단계가 가격형 IWM 칸을 지우지 않음", data().get("IWM", {}).get("kind") == "price")


def test_invesco(tmp, v2, P):
    """입력 형식 B(Invesco JSON) — 설계 dr r1~r3."""
    cfg = json.loads((HERE / "ticker_alias.json").read_text(encoding="utf-8"))
    fund = cfg["funds"]["QQQ"]

    def row(t, w, typ="COM", cus=None):
        return {"ticker": t, "issuerName": t, "cusip": cus if cus is not None else f"C{t}", "percentageOfTotalNetAssets": w, "securityTypeCode": typ}
    base = [row("NVDA", 50.0), row("AAPL", 30.0), row("ZZZZ", 19.0), row("ASML", 1.0, "DRNY"),
            row("NQZ6", 0.14, "IFUT", "NQZ6"), row(None, -0.14, "SYN", "NQZ6"), row("USDPDV", None, "CURR", None), row(None, 0.01, "CURRCOL", "USDMTM")]
    doc = lambda rows, **k: json.dumps(dict({"effectiveDate": P, "holdings": rows}, **k)).encode()

    def hold(body):
        try:
            etf_daily.parse_invesco(body, fund)
            return None
        except etf_daily.Hold as h:
            return h.key
    S, rows = etf_daily.parse_invesco(doc(base), fund)
    pre = {r["ticker"] or r["ident"]: r["pre"] for r in rows}
    check("형식 B: 비주식 4종(null·음수 비중·같은 식별자 공유 허용), 주식은 분류 대기", S == P and pre["NQZ6"] == "비주식" and pre["USDPDV"] == "비주식"
          and pre["USDMTM"] == "비주식" and pre["NVDA"] is None and pre["ASML"] is None, pre)
    check("형식 B: JSON 아님 → 받기 실패", hold(b"<html>blocked</html>") == "fetch_fail")
    check("형식 B: 최상위가 배열 → 입력 오류", hold(b"[]") == "input")
    check("형식 B: 날짜 칸 없음·가짜 날짜 → 입력 오류", hold(json.dumps({"holdings": base}).encode()) == "input"
          and hold(doc(base, effectiveDate="2026-02-30")) == "input")
    check("형식 B: 빈 holdings → 입력 오류", hold(doc([])) == "input")
    for bad, name in ((None, "null"), (-1.0, "음수"), (True, "bool"), ("5", "문자열"), (float("inf"), "Infinity")):
        b = doc([row("NVDA", bad)] + base[1:]) if name != "Infinity" else json.dumps({"effectiveDate": P, "holdings": [row("NVDA", 1e400)] + base[1:]}).encode()
        check(f"형식 B: 주식 비중 {name} → 입력 오류", hold(b) == "input", hold(b))
    check("형식 B: 모르는 종류의 비중이 null·음수 → 입력 오류", hold(doc(base + [row("XX", None, "WARR")])) == "input"
          and hold(doc(base + [row("XX", -1.0, "WARR")])) == "input")
    check("형식 B: ticker·cusip이 문자열·null이 아님 → 입력 오류", hold(doc(base + [dict(row("XY", 1.0), ticker=123)])) == "input"
          and hold(doc(base + [dict(row("XY", 1.0), cusip={})])) == "input")
    check("형식 B: 주식과 비주식이 같은 cusip → 입력 오류", hold(doc(base + [row("NQX", 1.0, "COM", "NQZ6")])) == "input")
    check("형식 B: 같은 cusip 주식 두 줄 → 입력 오류", hold(doc(base + [row("NVDX", 1.0, "COM", "CNVDA")])) == "input")
    S, rows = etf_daily.parse_invesco(doc(base + [row("NVDA", 0.5, "WARR", "W1"), row("MSFT", 0.5, "COM", "")]), fund)
    pre = {(r["ticker"], r["type"]): r["pre"] for r in rows}
    check("형식 B: 모르는 종류는 카드 티커와 같아도 분류 안 됨, cusip 빈 주식도 분류 안 됨", pre[("NVDA", "WARR")] == "분류 안 됨"
          and pre[("MSFT", "COM")] == "분류 안 됨", pre)
    # 계산까지: 분모 = 비주식 뺀 전부(분류 안 됨 포함)
    tmpq = tmp / "inv"
    tmpq.mkdir()
    (tmpq / "q.json").write_bytes(doc(base))
    (tmpq / "stocks.json").write_text(json.dumps({"priceSession": P}))
    c2 = dict(cfg)
    (tmpq / "cfg.json").write_text(json.dumps(c2, ensure_ascii=False))
    p = subprocess.run([sys.executable, str(HERE / "etf_daily.py"), "--etf", "QQQ", "--json", str(tmpq / "q.json"), "--out-root", str(tmpq / "out"),
                        "--v2", str(v2), "--stocks", str(tmpq / "stocks.json"), "--private", str(tmpq / "pv"), "--cfg", str(tmpq / "cfg.json")],
                       capture_output=True, text=True)
    r = json.loads((tmpq / "out" / "v2" / "etf" / "QQQ.json").read_text())
    calc = json.loads(next((tmpq / "pv").glob("QQQ_*_calc.json")).read_text())
    D = calc["D_raw"]
    check("형식 B 계산: D = 비주식 뺀 비중 합(100), 산출물 inputFormat·json 해시", abs(D - 100.0) < 1e-9 and r["inputFormat"] == "invesco_json"
          and "json" in r["inputHash"] and r["counts"]["nonEquity"] == 4, (D, r.get("inputFormat"), r.get("counts")))
    obs = [json.loads(x) for x in (tmpq / "out" / "v2" / "etf" / "date_obs.jsonl").read_text().splitlines()]
    check("형식 B: 관측 한 줄(etf QQQ, 파일 해시)", obs[-1]["etf"] == "QQQ" and len(obs[-1]["file_sha12"] or "") == 12, obs[-1:])


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
        test_code_sig_common(tmp, v2)
        test_invesco(tmp, v2, P)
        test_isolation(tmp, v2, P, asof)
    print(f"\n{'모두 통과' if not FAILS else f'실패 {len(FAILS)}건: ' + ', '.join(FAILS)}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
