#!/usr/bin/env python3
"""매일 가격 재빌드 — v2 카드 103장을 새 종가로 다시 만든다(2026-10-06 사용자 결정).

규칙(사용자 결정):
  - 매일: 103장 모두 새 종가로 재빌드. 점수·판정·문장 숫자가 그날 종가에 맞춰진다.
    SEC·EPS·재무·비교군 파일·애널리스트·내재가치 추적선은 받지 않는다(토요일 전체 재빌드 몫).
  - 판정이 바뀐 카드는 그대로 반영하고 목록으로 남긴다.
  - 한 장이 실패하면(문장 전제 확인, 데이터 검사, JS 오류) 그 카드는 전날 상태로 되돌리고 실패로 적는다.

카드 종류별 길:
  생성기 카드(cfg 있는 91장)  REFRESH=1 build.py T --price
  은행 9장                    기반·카드 배열에 새 종가(price_arrays.py) → {t}_rebuild.sh
  NVDA(틀 카드)               새 종가 → 배수·비교군·내재가치 블록 → 대체값 동기화(손문장은 그대로)
  BRKB·SPCX(손 카드)          새 종가 → 대체값 동기화(배수·판정 칸은 토요일·손 갱신 몫)

    python3 v2/newcards/daily_price.py                 # 전부
    python3 v2/newcards/daily_price.py KO GILD JPM     # 일부
    python3 v2/newcards/daily_price.py --weekly        # 토요일: 비교군 파일·애널리스트를 새로 받고 → 103장 → 비교군 어긋남 점검 → 새 분기 보고서 점검
결과: v2/daily_status.json(카드별 상태·마지막 봉·판정 전후) — 종료 코드 0 = 실패 없음, 1 = 실패 있음.

토요일 모드도 SEC 재무는 새로 받지 않는다. 카드 재무보다 새 10-Q·10-K가 나온 카드는 `newFilings`에 "확인 대기"로만 적는다
(문장이 지난 분기 내용이고, 분기 갱신은 research/pipeline_checks.md의 점검을 거친다 — 2026-10-06).
"""
import json
import os
import shutil
import signal
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
PY = sys.executable
BANKS = ["COF", "AXP", "BAC", "C", "GS", "JPM", "MS", "SCHW", "WFC"]   # COF 먼저 — AXP 카드가 COF_bank.json(같은 날짜)을 참고로 읽는다
HAND = ["NVDA", "BRKB", "SPCX"]
STATUS = os.path.join(V2, "daily_status.json")


def gen_tickers():
    return sorted(f[4:-3].upper() for f in os.listdir(os.path.join(HERE, "cfg"))
                  if f.startswith("cfg_") and f.endswith(".py") and f[4:-3].upper() not in BANKS)


def run(args, env=None, timeout=900):
    """자식 프로세스를 자기 그룹으로 띄워, 시간 초과면 그룹째 끝내고 기다린다 — 남은 렌더·빌드가 되돌린 카드를 덮어쓰지 않게(Codex 2026-10-06)."""
    pr = subprocess.Popen(args, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, start_new_session=True)
    try:
        out, _ = pr.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(pr.pid, signal.SIGKILL)
        pr.communicate()
        raise
    return pr.returncode, out


def verdicts():
    rc, out = run(["node", os.path.join(V2, "research", "extract_card_verdicts.js")])
    return json.loads(out) if rc == 0 else {}


def touched(T):
    """실패하면 되돌릴 파일 — 카드, cfg(REFRESH가 표를 고친다), 배수 파일, 은행 기반·은행 자료."""
    t = T.lower()
    paths = [f"v2/{T}_full_widget.html", f"v2/newcards/cfg/cfg_{t}.py", f"v2/{T}_multiples.json",
             f"v2/{T}_bank.json", f"v2/newcards/bank/base/{t}_base.html", "v2/newcards/refresh_changes.jsonl",
             "v2/peer_universe/banks.json", f"scripts/{T}_eps_history.json", f"v2/{T}_dcf_track.json"]
    return paths   # 없던 파일은 실패하면 지운다(Codex 2026-10-06 — 되돌린 판정 변경이 기록에 남지 않게)


def restore(bk):
    for p, b in bk.items():
        if b:
            shutil.copy2(b, os.path.join(REPO, p))
        elif os.path.exists(os.path.join(REPO, p)):
            os.remove(os.path.join(REPO, p))


def one(T, work):
    t = T.lower()
    if T in BANKS:
        for target in (f"v2/newcards/bank/base/{t}_base.html", f"v2/{T}_full_widget.html"):
            rc, out = run([PY, "v2/newcards/price_arrays.py", T, "--card", target])
            if rc:
                return rc, out
        return run(["bash", f"v2/newcards/bank/{t}_rebuild.sh"], env=dict(os.environ, PRICE_ONLY="1"))   # 비교 은행·공시 보충은 토요일 몫
    if T == "NVDA":
        steps = [[PY, "v2/newcards/price_arrays.py", T],
                 [PY, "v2/build_multiple_history.py", T, "--json", f"v2/{T}_multiples.json"],
                 [PY, "v2/build_peer_score.py", T, "--self", f"v2/{T}_multiples.json", "--card"],
                 [PY, "v2/build_dcf_block.py", T], [PY, "v2/build_dcf_grid.py", T],
                 [PY, "v2/strip_caveats.py", T], [PY, "v2/apply_theme.py", T], [PY, "v2/sync_fallbacks.py", T]]
    elif T in HAND:
        steps = [[PY, "v2/newcards/price_arrays.py", T], [PY, "v2/apply_theme.py", T], [PY, "v2/sync_fallbacks.py", T]]
    else:
        return run([PY, "v2/newcards/build.py", T, "--price"], env=dict(os.environ, REFRESH="1"))
    log = ""
    for s in steps:
        env = dict(os.environ, EPS_HISTORY=f"scripts/{T}_eps_history.json") if "build_multiple_history" in s[1] else None
        rc, out = run(s, env=env)
        log += out
        if rc:
            return rc, log
    return 0, log


def weekly_pre(status):
    """비교군 파일(S&P500 섹터)과 애널리스트를 기준 세션으로 새로 받는다. 실패하면 멈춘다(카드는 그대로)."""
    session = json.load(open(os.path.join(REPO, "site_data", "stocks.json")))["priceSession"]
    pdir = os.path.join(V2, "peer_universe")
    old = {f: json.load(open(os.path.join(pdir, f))) for f in os.listdir(pdir) if f.endswith(".json") and f != "banks.json"}
    rc, out = run([PY, "v2/adapters/refresh_peer_files.py", "--asof", session], timeout=7200)
    status["peerFiles"] = out.strip().splitlines()[-14:]
    if rc:   # 반쯤 받은 파일이 커밋되지 않게 이전 파일로 되돌리고 멈춘다(Codex)
        for f, o in old.items():
            json.dump(o, open(os.path.join(pdir, f), "w"), ensure_ascii=False, indent=1)
        print(out[-2000:]); sys.exit("비교군 파일 갱신 실패 — 이전 파일로 되돌렸고 카드는 건드리지 않았다")
    # Yahoo가 그 세션 봉을 늦게 주는 종목은 "기준일 종가 없음"으로 빠진다(2026-10-06 시험: 저녁 9시에 돌려 섹터마다 7~11종목).
    # 비교군이 줄면 판정이 흔들리므로, 새로 빠진 종목이 3개 이상인 섹터는 이전 파일을 그대로 쓴다.
    kept = []
    for f, o in old.items():
        n = json.load(open(os.path.join(pdir, f)))
        miss = [k for k, v in n.get("skipped", {}).items() if "기준일 종가 없음" in str(v) and k not in o.get("skipped", {})]
        if len(miss) >= 3:
            json.dump(o, open(os.path.join(pdir, f), "w"), ensure_ascii=False, indent=1)
            kept.append(f"{f}: 새로 빠진 {len(miss)}종목 — 이전 파일({o.get('asOf')}) 유지")
    status["peerFilesKept"] = kept
    if kept:
        print("\n".join(kept), flush=True)
    rc, out = run([PY, "v2/newcards/fetch_analyst.py"] + gen_tickers(), timeout=3600)
    status["analystFailed"] = [l for l in out.splitlines() if "실패" in l]
    if rc or status["analystFailed"]:   # 실패한 종목은 지난주 값 그대로 — 알림에 넣는다(Codex)
        status["problems"].append(f"애널리스트 받기 실패 {len(status['analystFailed'])}종목(rc {rc})")


def weekly_post(status, work):
    """비교군 파일에 카드 값을 넣고(sync_peer_rows), 동종업 칸이 어긋난 카드를 다시 만들고, 새 분기 보고서를 점검한다."""
    rc, out = run([PY, "v2/adapters/sync_peer_rows.py"])
    if rc:
        status["problems"].append("sync_peer_rows 실패: " + out.strip()[-300:])
    rc, out = run([PY, "v2/check_peer_drift.py"])
    if rc == 2:   # 0 = 어긋남 없음, 1 = 어긋남 있음(아래에서 다시 만든다), 2 = 계산 실패
        status["problems"].append("check_peer_drift 계산 실패: " + out.strip().splitlines()[-1][:300])
    drifted = sorted({l.split(":")[0] for l in out.splitlines() if ": 동종업 " in l})
    status["peerDrift"] = drifted
    for T in drifted:
        print(f"{T}: 동종업 어긋남 — 다시 만든다", flush=True)
        status["cards"][T] = attempt(T, work)
    rc, out = run([PY, "v2/newcards/new_filings.py"])
    try:
        nf = json.loads(out.strip().splitlines()[-1])
        status["newFilings"], status["filingChecksMissed"] = nf["pending"], nf["unchecked"]
        if nf["unchecked"]:
            status["problems"].append(f"새 분기 보고서 점검 못 한 카드 {nf['unchecked']}")
    except Exception:
        status["problems"].append("new_filings 실패: " + out.strip()[-300:])


def attempt(T, work):
    bk = {}
    for p in touched(T):
        if os.path.exists(os.path.join(REPO, p)):
            bk[p] = os.path.join(work, p.replace("/", "__"))
            shutil.copy2(os.path.join(REPO, p), bk[p])
        else:
            bk[p] = None
    t0 = time.time()
    for _ in (1, 2):   # 렌더용 Chrome이 가끔 시간 초과로 멈춘다(2026-10-06 TMUS) — 한 번 더
        try:
            rc, out = one(T, work)
        except subprocess.TimeoutExpired:
            rc, out = 124, "시간 초과"
        if rc == 0:
            break
        restore(bk)   # 전날 상태로
    if rc:
        tail = [l for l in out.strip().splitlines() if l.strip()][-6:]
        print(f"{T}: 실패 — {tail[-1][:200] if tail else ''}", flush=True)
        return {"status": "failed", "seconds": round(time.time() - t0), "why": tail}
    print(f"{T}: ok ({round(time.time() - t0)}초)", flush=True)
    return {"status": "ok", "seconds": round(time.time() - t0)}


def check_approved():
    """카드 회사가 모두 공시 기준표(v2/sec_approved.json)에 있는지 — 빠진 카드는 새 10-Q·10-K가 그대로 들어간다(Codex 2026-10-08).
    새 카드를 더하면 그 카드가 쓰는 공시 접수일(FUNDAMENTAL.filedAt)을 표에 넣어야 한다."""
    import new_filings as nf
    table = json.load(open(os.path.join(V2, "sec_approved.json")))
    miss = [T for T in sorted(f.split("_")[0] for f in os.listdir(V2) if f.endswith("_full_widget.html"))
            if T not in nf.OUTSIDE and str(nf.cik_of(T)).zfill(10) not in table]
    sys.path.insert(0, V2); import build_multiple_history as bmh
    bmh._approved()   # 날짜 형식까지 여기서 본다 — 토요일 비교군 작업 중간에 종목별 오류로 흩어지지 않게(Codex)
    miss += [T for T in sorted(f.split("_")[0] for f in os.listdir(V2) if f.endswith("_full_widget.html"))
             if T not in nf.OUTSIDE and str(nf.cik_of(T)).zfill(10) in table and not table[str(nf.cik_of(T)).zfill(10)]]
    if miss:
        sys.exit(f"공시 기준표에 없는 카드 {len(miss)}장: {' '.join(miss)} — v2/sec_approved.json에 FUNDAMENTAL.filedAt을 넣을 것")


def main():
    weekly = "--weekly" in sys.argv
    check_approved()
    session = json.load(open(os.path.join(REPO, "site_data", "stocks.json")))["priceSession"]
    if "--skip-if-current" in sys.argv and not weekly and os.path.exists(STATUS):
        # 가격 작업은 하루 세 번까지 돈다(늦은 봉 대비) — 같은 세션을 이미 실패 없이 끝냈으면 건너뛴다
        old = json.load(open(STATUS))
        # 종목마다 홈 가격 세션이 다르다(Yahoo가 늦게 준 종목은 전날 세션) — 카드 하나라도 자기 세션보다 뒤면 건너뛰지 않는다
        # (2026-10-08: 10/6 실행 때 10/5에 머문 11장이 그 뒤 "이미 끝났다"로 계속 건너뛰어져 건강 점검에 걸렸다)
        own = {e["ticker"]: e["price"].get("session") for e in json.load(open(os.path.join(REPO, "site_data", "stocks.json")))["tickers"]}
        behind = [t for t, v in old.get("cards", {}).items() if own.get(t) and v.get("date") and v["date"] < own[t]]
        if old.get("session") == session and old.get("full") and not old.get("failed") and not old.get("problems") and old.get("finished") and not behind:
            print(f"{session} 세션은 이미 끝났다({old['finished']}) — 건너뜀"); return
        if behind:
            print(f"자기 세션보다 뒤처진 카드 {len(behind)}장 — 다시 만든다: {' '.join(sorted(behind))}", flush=True)
    want = [a.upper() for a in sys.argv[1:] if not a.startswith("--")]
    tickers = want or (gen_tickers() + BANKS + HAND)
    work = os.path.join(V2, ".sec_cache", "_work", "daily")
    os.makedirs(work, exist_ok=True)
    before = verdicts()
    status = {"mode": "weekly" if weekly else "daily", "session": session, "full": not want, "problems": [], "started": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "cards": {}}
    if weekly:
        weekly_pre(status)
    for T in tickers:
        status["cards"][T] = attempt(T, work)
    if weekly:
        weekly_post(status, work)
    after = verdicts()
    changes = []
    for T in tickers:
        o, n = before.get(T), after.get(T)
        if not o or not n:
            continue
        oj, nj = [j[1] for j in o["judges"]], [j[1] for j in n["judges"]]
        status["cards"][T].update({"date": n.get("date"), "verdict": n["verdict"]})
        if o["verdict"] != n["verdict"] or oj != nj:
            changes.append({"ticker": T, "old": [oj, o["verdict"]], "new": [nj, n["verdict"]]})
    status["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    status["verdictChanges"] = changes
    status["failed"] = [T for T, v in status["cards"].items() if v["status"] == "failed"]
    json.dump(status, open(STATUS, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"끝 — ok {sum(v['status'] == 'ok' for v in status['cards'].values())} · 실패 {status['failed']} · 판정·표 변경 {len(changes)}")
    for c in changes:
        print("  ", c)
    for p in status["problems"]:
        print("문제:", p)
    sys.exit(1 if status["failed"] or status["problems"] else 0)


if __name__ == "__main__":
    main()
