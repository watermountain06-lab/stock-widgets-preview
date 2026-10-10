#!/usr/bin/env python3
"""엔진 수정의 카드 회귀 — 카드를 쓰지 않고, 같은 입력으로 수정 전·후 엔진의 카드 값을 비교한다
(input_fix_prereg.md 2절 "카드 103장 회귀", 3절 2단계).

작업 나무(sandbox)는 이 저장소의 git worktree다. 만들 때 기준 커밋(BASE)의 카드·설정을 그대로 얼리고,
git이 추적하지 않는 입력(.sec_cache·data/·연구 자료)은 APFS 복제(cp -c)로 붙인다 — 디스크를 거의 쓰지 않는다.
실행마다 나무를 BASE로 되돌리고 엔진 파일만 바꿔 끼운 뒤, 카드 일봉 기준일 그대로 엔진 단계를 나무 안에서 돌린다.
진짜 저장소의 카드·캐시는 건드리지 않는다. 네트워크는 프록시를 죽은 포트로 돌려 막는다(캐시가 없으면 실패로 남는다).

    python3 v2/research/engine_regress.py freeze              # 작업 나무 만들기(BASE = 지금 HEAD)
    python3 v2/research/engine_regress.py run base            # 기준선: BASE 엔진
    python3 v2/research/engine_regress.py run f1 --engine working   # 지금 작업 트리의 엔진 파일로
    python3 v2/research/engine_regress.py diff base f1 [--expect CVX,XOM]
    python3 v2/research/engine_regress.py fidelity base       # 기준선 블록이 실제 카드 블록과 같은지(도구 점검)

카드 경로: 일반 카드는 build_multiple_history → build_peer_score --card → build_dcf_block(일일 갱신과 같은 엔진 단계),
은행 카드는 adapters/bank_card.py --reuse-peers의 JSON, 손 카드(BRKB·SPCX)는 엔진을 거치지 않아 뺀다.
판정은 카드 자신의 판정 코드(extract_card_verdicts.js)로 꺼낸다. 비교군 파일(peer_universe)은 얼린 것을 쓴다 —
비교군 재생성을 거친 변화는 이 도구 밖이다(input_fix_prereg 2절 "비교군을 거친 변화"는 따로 잰다).

도구 점검(2026-10-10, BASE 537398c): 기준선 블록·판정이 실제 카드와 같은 카드 97장. 어댑터 카드 ASML(DCF 0.2% — 환율 계열 추정)·
SKHY(자기 이력 배열)는 카드 빌드 경로(build.py feed)와 조금 달라 실제 카드와 다르다 — 두 카드는 도구 안의 전·후 비교로만 읽는다.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
ROOT = os.path.join(REPO, ".regress")              # .gitignore
TREE = os.path.join(ROOT, "tree")
RUNS = os.path.join(ROOT, "runs")
META = os.path.join(ROOT, "meta.json")
PY = sys.executable
SELF = "v2/research/engine_regress.py"

# git이 추적하지 않는 입력 — 나무에 복제로 붙인다
UNTRACKED_INPUTS = ["v2/.sec_cache", "data", "v2/research/.prices10y", "v2/research/.facts_20261002",
                    "v2/research/.eps_20261002", "v2/research/.sp500_wiki_20261008"]
# 엔진으로 보는 파일(바꿔 끼우는 대상). 카드 HTML·일봉·공시 승인일 같은 입력 자료는 넣지 않는다.
ENGINE_GLOBS = [":(glob)v2/*.py", ":(glob)v2/adapters/*.py", ":(glob)v2/research/*.py", ":(glob)scripts/*.py",   # 하위 폴더는 넣지 않는다
                "v2/core_earnings.json", "v2/tax_oneoff.json", "v2/share_adjust.json", "v2/nonop_extra.json",
                "v2/interest_extra.json", "v2/tax_rate_addback.json", "v2/sectors.json"]
BANKS = ["COF", "AXP", "BAC", "C", "GS", "JPM", "MS", "SCHW", "WFC"]      # newcards/daily_price.py와 같다
HAND = ["BRKB", "SPCX"]                                                     # NVDA는 엔진 단계를 거친다
NO_NET = {k: "http://127.0.0.1:9" for k in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "all_proxy")}


def sh(cmd, cwd=None, env=None, check=True):
    r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit(f"실패: {' '.join(cmd)}\n{(r.stdout + r.stderr)[-1500:]}")
    return r


def git(*a, cwd=REPO, check=True):
    return sh(["git", "-C", cwd, *a], check=check).stdout.strip()


def freeze(_args):
    if os.path.exists(TREE):
        raise SystemExit(f"이미 있다: {TREE} — 새로 얼리려면 `git worktree remove --force {TREE}` 뒤 {ROOT}를 지운다")
    base = git("rev-parse", "HEAD")
    os.makedirs(ROOT, exist_ok=True)
    git("worktree", "add", "--detach", TREE, base)
    for p in UNTRACKED_INPUTS:
        src = os.path.join(REPO, p)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(os.path.join(TREE, p)), exist_ok=True)
            sh(["cp", "-c", "-R", src, os.path.join(TREE, p)])        # APFS 복제
    json.dump({"base": base, "frozen": time.strftime("%Y-%m-%d %H:%M"), "inputs": UNTRACKED_INPUTS},
              open(META, "w"), indent=1)
    print("작업 나무", TREE, "BASE", base[:8])


def engine_files(ref):
    """BASE와 달라진 엔진 파일 목록과 그 내용을 줄 곳. ref = 'working'(지금 작업 트리) 또는 커밋."""
    base = json.load(open(META))["base"]
    if ref == "working":
        changed = git("diff", "--name-only", base, "--", *ENGINE_GLOBS).split()
        changed += git("ls-files", "--others", "--exclude-standard", "--", *ENGINE_GLOBS).split()
        changed = [c for c in changed if c != SELF]          # 이 도구 자신은 엔진이 아니다
        return sorted(set(changed)), lambda p: open(os.path.join(REPO, p), "rb").read() if os.path.exists(os.path.join(REPO, p)) else None
    changed = git("diff", "--name-only", base, ref, "--", *ENGINE_GLOBS).split()
    def blob(p):
        r = sh(["git", "-C", REPO, "show", f"{ref}:{p}"], check=False)
        return r.stdout.encode() if r.returncode == 0 else None
    return sorted(set(changed)), blob


def reset_tree():
    base = json.load(open(META))["base"]
    git("checkout", "-f", base, "--", ".", cwd=TREE)
    git("clean", "-fdq", cwd=TREE)                         # 추적 안 하는 새 파일만 지운다(무시 파일·복제 입력은 그대로)


def cards():
    return sorted(os.path.basename(p)[:-len("_full_widget.html")] for p in glob.glob(os.path.join(TREE, "v2", "*_full_widget.html")))


def no_dcf(T):
    p = os.path.join(TREE, "v2", "newcards", "cfg", f"cfg_{T.lower()}.py")
    return os.path.exists(p) and "'no_dcf'" in open(p, encoding="utf-8").read()


def blocks(T):
    """나무 카드의 VALUATION·DCF 블록(JSON)."""
    h = open(os.path.join(TREE, "v2", f"{T}_full_widget.html"), encoding="utf-8").read()
    out = {}
    m = re.search(r"/\* VALUATION:BEGIN \*/(.*?)/\* VALUATION:END \*/", h, re.S)
    if m:
        v = re.search(rf"const {T}_VALUATION\s*=\s*(\{{.*\}});", m.group(1), re.S)
        out["valuation"] = json.loads(v.group(1)) if v else None
    d = re.search(rf"const {T}_DCF = (\{{.*?\}});", h, re.S)
    out["dcf"] = json.loads(d.group(1)) if d else None
    return out


def run(args):
    label = args.label
    reset_tree()
    files, blob = engine_files(args.engine) if args.engine != "base" else ([], None)
    _swap(files, blob)
    if args.peers:                                          # 다시 만든 비교군 파일로(peers 명령)
        for f in glob.glob(os.path.join(PEERS, args.peers, "*.json")):
            shutil.copy2(f, os.path.join(TREE, "v2", "peer_universe"))
    env0 = dict(os.environ, **NO_NET)
    res = {"_meta": {"label": label, "engine": args.engine, "peers": args.peers, "swapped": files, "base": json.load(open(META))["base"],
                     "ran": time.strftime("%Y-%m-%d %H:%M")}}
    todo = [T for T in cards() if T not in HAND and (not args.only or T in args.only.split(","))]
    t0 = time.time()
    for k, T in enumerate(todo):
        r = {}
        try:
            if T in BANKS:
                out = os.path.join(ROOT, "work", f"{label}_{T}_bank.json")
                os.makedirs(os.path.dirname(out), exist_ok=True)
                p = sh([PY, "v2/adapters/bank_card.py", T, "--json", out, "--reuse-peers"], cwd=TREE, env=env0, check=False)
                if p.returncode:
                    r["error"] = (p.stdout + p.stderr)[-400:]
                else:
                    r["bank"] = json.load(open(out))
            else:
                mj = os.path.join(TREE, "v2", f"{T}_multiples.json")
                steps = [[PY, "v2/build_multiple_history.py", T, "--json", mj],
                         [PY, "v2/build_peer_score.py", T, "--self", mj, "--card"]]
                if not no_dcf(T):                          # 보험사(CB·PGR)는 현금흐름 모델을 쓰지 않는다 — build.py와 같다
                    steps.append([PY, "v2/build_dcf_block.py", T])
                for s in steps:
                    env = dict(env0, EPS_HISTORY=f"scripts/{T}_eps_history.json") if "build_multiple_history" in s[1] else env0
                    p = sh(s, cwd=TREE, env=env, check=False)
                    if p.returncode:
                        r["error"] = f"{os.path.basename(s[1])}: " + (p.stdout + p.stderr)[-400:]
                        break
                if "error" not in r:
                    r.update(blocks(T))
                    r["multiples"] = {k2: {x: v.get(x) for x in ("current", "score", "currentNote")}
                                      for k2, v in json.load(open(mj))["multiples"].items()}
        except Exception as e:
            r["error"] = f"{type(e).__name__}: {e}"[:400]
        res[T] = r
        if k % 10 == 0:
            print(k, T, "오류" if "error" in r else "", f"{time.time() - t0:.0f}s", flush=True)
    # 카드 자신의 판정 코드로 판정을 꺼낸다(나무 카드)
    p = sh(["node", "v2/research/extract_card_verdicts.js"], cwd=TREE, check=False)
    if p.returncode == 0:
        ver = json.loads(p.stdout)
        for T, v in ver.items():
            if T in res:
                res[T]["verdict"] = {k2: v.get(k2) for k2 in ("verdict", "judges", "dcfLabel", "ratio", "error")}
    else:
        res["_meta"]["verdict_error"] = p.stderr[-400:]
    os.makedirs(RUNS, exist_ok=True)
    json.dump(res, open(os.path.join(RUNS, f"{label}.json"), "w"), ensure_ascii=False, indent=1)
    bad = [T for T, r in res.items() if not T.startswith("_") and "error" in r]
    print(f"저장 {label}: 카드 {len(todo)} · 오류 {len(bad)} {bad[:12]} · 바꾼 엔진 파일 {len(files)} · {time.time() - t0:.0f}s")


def _flat(x, pre=""):
    if isinstance(x, dict):
        o = {}
        for k, v in x.items():
            o.update(_flat(v, f"{pre}.{k}" if pre else str(k)))
        return o
    if isinstance(x, list):
        return {pre: json.dumps(x, ensure_ascii=False, sort_keys=True)}
    return {pre: x}


def _same(a, b):
    if isinstance(a, float) and isinstance(b, float):
        return abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b))
    return a == b


def diff(args):
    A = json.load(open(os.path.join(RUNS, f"{args.a}.json")))
    B = json.load(open(os.path.join(RUNS, f"{args.b}.json")))
    expect = set(args.expect.split(",")) if args.expect else set()
    changed = {}
    only = sorted(t for t in set(A) ^ set(B) if not t.startswith("_"))
    if only:
        print("한쪽 실행에만 있는 카드(비교 안 함):", only)
    for T in sorted(set(A) & set(B)):
        if T.startswith("_"):
            continue
        fa, fb = _flat(A.get(T, {})), _flat(B.get(T, {}))
        d = [(k, fa.get(k), fb.get(k)) for k in sorted(set(fa) | set(fb)) if not _same(fa.get(k), fb.get(k))]
        if d:
            changed[T] = d
    print(f"{args.a} → {args.b}: 바뀐 카드 {len(changed)} / {len([t for t in A if not t.startswith('_')])}")
    print("바꾼 엔진 파일:", B["_meta"].get("swapped"))
    for T, d in changed.items():
        tag = "기대" if T in expect else "** 기대 밖 **"
        vA, vB = (A.get(T, {}).get("verdict") or {}).get("verdict"), (B.get(T, {}).get("verdict") or {}).get("verdict")
        print(f"\n{T} [{tag}] 항목 {len(d)}" + (f" · 판정 {vA} → {vB}" if vA != vB else ""))
        for k, x, y in d[:args.show]:
            print(f"   {k}: {x} → {y}")
        if len(d) > args.show:
            print(f"   … {len(d) - args.show}개 더")
    out = [T for T in changed if T not in expect]
    if expect:
        print(f"\n기대 밖 변화 {len(out)}: {out}")


def fidelity(args):
    """기준선 실행의 블록이 저장소의 실제 카드 블록과 같은지 — 같은 입력이면 같아야 한다(도구가 카드 경로를 재현하는지)."""
    A = json.load(open(os.path.join(RUNS, f"{args.label}.json")))
    reset_tree()
    same, diffs = 0, {}
    p = sh(["node", "v2/research/extract_card_verdicts.js"], cwd=TREE, check=False)
    real_v = json.loads(p.stdout) if p.returncode == 0 else {}
    for T, r in A.items():
        if T.startswith("_") or "error" in r:
            continue
        if "bank" in r:                                    # 은행: 커밋된 v2/{T}_bank.json과
            bp = os.path.join(TREE, "v2", f"{T}_bank.json")
            real = {"bank": json.load(open(bp)) if os.path.exists(bp) else None}
        else:
            real = blocks(T)                               # 되돌린 나무 = BASE 카드
        rv = real_v.get(T) or {}
        real["verdict"] = {k2: rv.get(k2) for k2 in ("verdict", "judges", "dcfLabel", "ratio", "error")}
        d = [k for k in real if json.dumps(real.get(k), sort_keys=True) != json.dumps(r.get(k), sort_keys=True)]
        if d:
            fa, fb = _flat({k: real.get(k) for k in d}), _flat({k: r.get(k) for k in d})
            diffs[T] = [(k, fa.get(k), fb.get(k)) for k in sorted(set(fa) | set(fb)) if not _same(fa.get(k), fb.get(k))]
        else:
            same += 1
    print(f"실제 카드와 같은 카드 {same}, 다른 카드 {len(diffs)}")
    for T, d in diffs.items():
        print(f"  {T}: {len(d)}개 — " + "; ".join(f"{k}: {x} → {y}" for k, x, y in d[:4]))


PANEL_SCRIPT = r'''
import sys, os, json
os.chdir("v2/research"); sys.path.insert(0, os.getcwd())
import verdict_replay as vr
which, out = sys.argv[1], sys.argv[2]
if which == "test":                                   # 관문 시험 패널 설정(verdict_replay.build_only와 같다)
    vr.START_MONTH, vr.END_MONTH, vr.BAR_START, vr.DCF_WINDOW, vr.HASH_LEN = "2021-10", "2024-03", "2016-01-01", "rolling", 64
meta, rows = vr.build(out)
print("rows", len(rows))
'''


def _swap(files, blob):
    for p in files:
        b = blob(p)
        dst = os.path.join(TREE, p)
        if b is None:
            if os.path.exists(dst):
                os.remove(dst)
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "wb").write(b)


def panel(args):
    """작업 나무에서 엔진을 바꿔 끼우고 학습(learn)·시험(test) 패널을 만든다. 수익률은 붙이지 않는다."""
    reset_tree()
    files, blob = engine_files(args.engine) if args.engine != "base" else ([], None)
    _swap(files, blob)
    os.makedirs(os.path.join(ROOT, "panels"), exist_ok=True)
    for which in args.which.split(","):
        out = os.path.join(ROOT, "panels", f"{args.label}_{which}.json")
        t0 = time.time()
        p = sh([PY, "-c", PANEL_SCRIPT, which, out], cwd=TREE, env=dict(os.environ, **NO_NET), check=False)
        print(which, (p.stdout + p.stderr).strip().splitlines()[-1][:300], f"{time.time() - t0:.0f}s", "→", out, flush=True)


def _panel_rows(path):
    sys.path.insert(0, HERE)
    import verdict_replay as vr
    rows = json.load(open(path))["rows"]
    # 가치 비교 가격(F1 px_then)이 있으면 그것으로 칸 표를 낸다 — 고친 verdict_replay.assign과 같은 결과(이 함수는 수익률을 쓰지 않는다)
    for r in rows:
        if "px_then" in r:
            r["_px"], r["px"] = r["px"], r["px_then"]
    vr.peer_scores(rows)
    vr.assign(rows)
    for r in rows:
        if "_px" in r:
            r["px"] = r.pop("_px")
    return {(r["t"], r["m"]): r for r in rows}


def paneldiff(args):
    """두 패널의 행 차이 — 입력(px_then·base·self·peer·dq)과 칸 표·V0 판정. 수익률은 없다."""
    A, B = _panel_rows(args.a), _panel_rows(args.b)
    keys = sorted(set(A) & set(B))
    print(f"행 {len(A)} → {len(B)} (공통 {len(keys)}, 한쪽에만 {len(set(A) ^ set(B))})")
    fields = ["px_then", "base", "dcf_ok", "self", "peer", "dq", "self_vote", "peer_vote", "lv_V0", "g_V0"]
    ch = {f: [] for f in fields}
    for k in keys:
        a, b = A[k], B[k]
        for f in fields:
            x = a.get(f, a.get("px")) if f == "px_then" else a.get(f)
            y = b.get(f, b.get("px")) if f == "px_then" else b.get(f)
            if json.dumps(x, sort_keys=True, default=str) != json.dumps(y, sort_keys=True, default=str):
                ch[f].append((k, x, y))
    for f in fields:
        tick = sorted({k[0] for k, _, _ in ch[f]})
        print(f"{f:10} 바뀐 행 {len(ch[f]):5}  종목 {len(tick):3} {tick[:args.show]}")
    for f in ("lv_V0", "g_V0"):
        for k, x, y in ch[f][:args.show]:
            print(f"   {f} {k[0]} {k[1]}: {x} → {y}")
    if args.ticker:
        for k in keys:
            if k[0] == args.ticker:
                a, b = A[k], B[k]
                print(k[1], "px", a["px"], "px_then", a.get("px_then", a["px"]), "→", b.get("px_then", b["px"]),
                      "base", a["base"], "→", b["base"], "PER", a["peer"].get("PER"), "→", b["peer"].get("PER"),
                      "lv", a.get("lv_V0"), "→", b.get("lv_V0"))


BIN = os.path.join(ROOT, "bin")
FIXTURE = os.path.join(ROOT, "curl_fixture")
PEERS = os.path.join(ROOT, "peers")
FAKE_CURL = r'''#!/usr/bin/env python3
# engine_regress의 curl 대역: 기록(record) 때는 진짜 curl을 부르고 응답을 남기고, 재생(replay) 때는 남긴 응답만 돌려준다.
import hashlib, os, subprocess, sys
a = sys.argv[1:]
url = [x for x in a if x.startswith("http")][-1]
data = a[a.index("--data") + 1] if "--data" in a else ""
key = hashlib.sha256((url + "\n" + data).encode()).hexdigest()
fx = os.environ["CURL_FIXTURE"]
p = os.path.join(fx, key + ".out")
if os.path.exists(p):
    sys.stdout.buffer.write(open(p, "rb").read()); sys.exit(0)
if os.environ.get("CURL_MODE") != "record":
    open(os.path.join(fx, "_misses.txt"), "a").write(url + "\n")
    sys.stderr.write("fixture miss " + url + "\n"); sys.exit(7)
r = subprocess.run(["/usr/bin/curl"] + a, capture_output=True)
if r.returncode == 0 and r.stdout:
    open(p, "wb").write(r.stdout)
    open(os.path.join(fx, "_index.txt"), "a").write(key + " " + url + "\n")
sys.stdout.buffer.write(r.stdout); sys.stderr.buffer.write(r.stderr); sys.exit(r.returncode)
'''


def _curl_env(record):
    os.makedirs(BIN, exist_ok=True)
    os.makedirs(FIXTURE, exist_ok=True)
    p = os.path.join(BIN, "curl")
    open(p, "w").write(FAKE_CURL)
    os.chmod(p, 0o755)
    env = dict(os.environ, PATH=BIN + ":" + os.environ["PATH"], CURL_FIXTURE=FIXTURE, CURL_MODE="record" if record else "replay")
    if not record:
        env.update(NO_NET)
    return env


def peers(args):
    """S&P500 비교군 파일을 엔진을 바꿔 끼운 나무에서 다시 만든다(주간 실행과 같은 refresh_peer_files → sync_peer_rows).
    네트워크 응답(Yahoo 일봉·분할, SEC)은 처음 한 번 기록(--record)하고 그 뒤에는 그 기록만 재생한다 — 수정 전·후가 같은 입력을 본다.
    한계: sync_peer_rows는 얼린(BASE) 카드 값을 넣는다. 고친 카드 값이 비교군 행으로 다시 들어가는 2차 효과는 재지 않는다."""
    reset_tree()
    files, blob = engine_files(args.engine) if args.engine != "base" else ([], None)
    _swap(files, blob)
    meta = json.load(open(META))
    asof = args.asof or meta.get("peers_asof") or json.load(open(os.path.join(TREE, "site_data", "stocks.json")))["priceSession"]
    env = _curl_env(args.record)
    miss0 = sum(1 for _ in open(os.path.join(FIXTURE, "_misses.txt"))) if os.path.exists(os.path.join(FIXTURE, "_misses.txt")) else 0
    t0 = time.time()
    p = sh([PY, "v2/adapters/refresh_peer_files.py", "--asof", asof], cwd=TREE, env=env, check=False)
    if p.returncode:
        raise SystemExit("refresh_peer_files 실패:\n" + (p.stdout + p.stderr)[-1500:])
    p2 = sh([PY, "v2/adapters/sync_peer_rows.py"], cwd=TREE, env=env, check=False)
    if p2.returncode:
        raise SystemExit("sync_peer_rows 실패:\n" + (p2.stdout + p2.stderr)[-1500:])
    out = os.path.join(PEERS, args.label)
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    for f in glob.glob(os.path.join(TREE, "v2", "peer_universe", "*.json")):
        shutil.copy2(f, out)
    if args.record:
        meta["peers_asof"] = asof
        json.dump(meta, open(META, "w"), indent=1)
    miss1 = sum(1 for _ in open(os.path.join(FIXTURE, "_misses.txt"))) if os.path.exists(os.path.join(FIXTURE, "_misses.txt")) else 0
    print(f"비교군 {args.label}: 기준일 {asof} · 파일 {len(os.listdir(out))} · 재생 실패 {miss1 - miss0} · {time.time() - t0:.0f}s")
    for f in sorted(os.listdir(out)):
        d = json.load(open(os.path.join(out, f)))
        print(f"   {f}: 종목 {len(d.get('tickers', {}))} · 제외 {len(d.get('skipped', {}))}")


def peersdiff(args):
    """두 비교군 실행의 종목·배수 차이."""
    A, B = os.path.join(PEERS, args.a), os.path.join(PEERS, args.b)
    for f in sorted(set(os.listdir(A)) | set(os.listdir(B))):
        a = json.load(open(os.path.join(A, f))) if os.path.exists(os.path.join(A, f)) else {}
        b = json.load(open(os.path.join(B, f))) if os.path.exists(os.path.join(B, f)) else {}
        ta, tb = a.get("tickers", {}), b.get("tickers", {})
        ch = []
        for t in sorted(set(ta) | set(tb)):
            for k in sorted(set(ta.get(t, {})) | set(tb.get(t, {}))):
                x, y = ta.get(t, {}).get(k), tb.get(t, {}).get(k)
                if not _same(x, y):
                    ch.append(f"{t}.{k}: {x} → {y}")
        sk = sorted(set(a.get("skipped", {})) ^ set(b.get("skipped", {})))
        if ch or sk:
            print(f"{f}: 값 {len(ch)} · 제외 목록 차이 {sk[:8]}")
            for c in ch[:args.show]:
                print("   ", c)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("freeze")
    r = sub.add_parser("run"); r.add_argument("label"); r.add_argument("--engine", default="base"); r.add_argument("--only"); r.add_argument("--peers")
    pe = sub.add_parser("peers"); pe.add_argument("label"); pe.add_argument("--engine", default="base"); pe.add_argument("--record", action="store_true"); pe.add_argument("--asof")
    pf = sub.add_parser("peersdiff"); pf.add_argument("a"); pf.add_argument("b"); pf.add_argument("--show", type=int, default=15)
    d = sub.add_parser("diff"); d.add_argument("a"); d.add_argument("b"); d.add_argument("--expect"); d.add_argument("--show", type=int, default=8)
    f = sub.add_parser("fidelity"); f.add_argument("label")
    pn = sub.add_parser("panel"); pn.add_argument("label"); pn.add_argument("--engine", default="base"); pn.add_argument("--which", default="learn,test")
    pd = sub.add_parser("paneldiff"); pd.add_argument("a"); pd.add_argument("b"); pd.add_argument("--show", type=int, default=12); pd.add_argument("--ticker")
    a = ap.parse_args()
    {"freeze": freeze, "run": run, "diff": diff, "fidelity": fidelity, "panel": panel, "paneldiff": paneldiff,
     "peers": peers, "peersdiff": peersdiff}[a.cmd](a)


if __name__ == "__main__":
    main()
