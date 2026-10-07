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
결과: v2/daily_status.json(카드별 상태·마지막 봉·판정 전후) — 종료 코드 0 = 실패 없음, 1 = 실패 있음.
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
                 [PY, "v2/strip_caveats.py", T], [PY, "v2/sync_fallbacks.py", T]]
    elif T in HAND:
        steps = [[PY, "v2/newcards/price_arrays.py", T], [PY, "v2/sync_fallbacks.py", T]]
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


def main():
    want = [a.upper() for a in sys.argv[1:]]
    tickers = want or (gen_tickers() + BANKS + HAND)
    work = os.path.join(V2, ".sec_cache", "_work", "daily")
    os.makedirs(work, exist_ok=True)
    before = verdicts()
    status = {"started": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "cards": {}}
    for T in tickers:
        bk = {}
        for p in touched(T):
            if os.path.exists(os.path.join(REPO, p)):
                bk[p] = os.path.join(work, p.replace("/", "__"))
                shutil.copy2(os.path.join(REPO, p), bk[p])
            else:
                bk[p] = None
        t0 = time.time()
        for attempt in (1, 2):   # 렌더용 Chrome이 가끔 시간 초과로 멈춘다(2026-10-06 TMUS) — 한 번 더
            try:
                rc, out = one(T, work)
            except subprocess.TimeoutExpired:
                rc, out = 124, "시간 초과"
            if rc == 0:
                break
            restore(bk)
        if rc:
            restore(bk)   # 전날 상태로
            tail = [l for l in out.strip().splitlines() if l.strip()][-6:]
            status["cards"][T] = {"status": "failed", "seconds": round(time.time() - t0), "why": tail}
            print(f"{T}: 실패 — {tail[-1][:200] if tail else ''}", flush=True)
        else:
            status["cards"][T] = {"status": "ok", "seconds": round(time.time() - t0)}
            print(f"{T}: ok ({round(time.time() - t0)}초)", flush=True)
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
    sys.exit(1 if status["failed"] else 0)


if __name__ == "__main__":
    main()
