#!/usr/bin/env python3
"""ETF 판정 알림 — 사람 손이 필요한 보류를 GitHub 이슈로 알린다(2026-10-20 설계 dr 합의).

    python3 v2/etf/etf_alerts.py [--etf SPY,QQQ] [--dry-run]

모든 ETF 단계·대조 단계가 끝난 뒤 한 번 돈다(2026-10-21 QQQ 설계 dr r3). code_sig(카드 판정 코드 해시)는 ETF 공통이라
이슈 하나 "[ETF code_sig]"로 모은다(키 = 미승인 해시 합집합, 본문 표식 <!-- etf-hashes: … -->). 검사 못 한 ETF가 있으면
그 ETF가 전에 낸 미승인 해시(아직 승인 목록에 없는 것)를 남긴다. 닫기: 모든 ETF가 이번 실행에서 명시적으로 ok일 때만.
그 밖 종류는 ETF마다 "[ETF <ETF> 종류]". 산출물의 runId가 이번 Actions 실행이 아니면 그 ETF는 모든 종류를 "검사 못 함"으로 본다.

입력: v2/etf/<ETF>.json의 checks(종류별 bad/ok/unchecked)·checkDetail(구조화 상세)과 v2/etf/date_obs.jsonl(실행 기록).
종류마다 열린 이슈는 최대 하나(라벨 etf-alert, 제목 접두 "[ETF <ETF> 종류]"로 찾는다). 사건 키는 본문 끝 표식
<!-- etf-key: ... -->(키의 sha256 앞 12자 — 본문을 줄여도 잘리지 않게). 열린 이슈가 없고 문제가 있으면 새로, 키가 바뀌면 댓글 + 표식 갱신, 같으면 아무것도 안 함.
닫기는 그 종류가 이번 실행에서 "검사 완료·문제 없음(ok)"일 때만 — "검사 못 함(unchecked)"이면 그대로 둔다.
- 바로 알림: code_sig(미승인 판정 코드 해시 — diff와 승인 방법), sig_err(서명을 못 잰 카드), structure, unclassified.
- 이어질 때만: 이번 실행 결과가 bad일 때만 실행 기록을 본다(ok면 해소, 검사 못 함이면 그대로). fetch·input·tools·run은
  2회 연속, file_date는 운용사 지연(S < P)만 6회 연속(하루 세 번 실행이라 약 이틀 — 저녁마다 하루 늦는 것은 정상이고 아침에
  풀린다; 홈 세션 지연 S > P는 알리지 않는다). 실행 기록의 마지막 줄이 이번 실행이 아니면 판단하지 않는다.
- 본문이 20,000자를 넘으면 diff를 빼고 링크만으로 연다.
알림이 실패해도(권한·API) 판정·관측 산출물에는 영향이 없다 — 워크플로에서 continue-on-error.
"""
import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ETF_DIR = Path(__file__).resolve().parent
LABEL = "etf-alert"
CONSEC = {"fetch": (2, {"fetch_fail"}), "input": (2, {"input"}), "tools": (2, {"tools"}),
          "run": (2, {"run_fail", "selfcheck"}), "file_date": (6, {"file_date"})}
BODY_MAX = 20000   # GitHub 이슈 본문 한도(65,536자) 아래로 — 넘으면 diff 없이 링크만으로 다시 시도
IMMEDIATE = ("code_sig", "sig_err", "structure", "unclassified")
KIND_TEXT = {"code_sig": "카드 판정 코드 변경 — 승인 필요", "sig_err": "판정 코드 서명을 못 잰 카드 — 카드 파일 확인",
             "structure": "카드 판정 구조 변경", "unclassified": "분류 안 되는 보유 줄 — 설정(company·nonEquity) 추가",
             "fetch": "운용사 파일을 받지 못함(이어짐)", "input": "운용사 파일 모양 오류(이어짐)",
             "tools": "카드 판정 추출기 실패(이어짐)", "run": "ETF 스크립트 실패(이어짐)",
             "file_date": "운용사 보유 파일이 이틀째 홈 세션과 다름"}
DIFF_MAX = 200


def gh(args, stdin=None):
    """gh CLI 호출(시험에서 바꿔 끼운다)."""
    p = subprocess.run(["gh"] + args, input=stdin, capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        raise RuntimeError(f"gh {args[0]} {args[1] if len(args) > 1 else ''} 실패({p.returncode})")
    return p.stdout


def last_runs(obs_path, etf, n):
    try:
        rows = [json.loads(x) for x in obs_path.read_text(encoding="utf-8").splitlines() if x.strip()]
    except Exception:
        return []
    # 같은 실행(run_id·attempt)이 두 줄을 남기면(본 단계가 쓰고 죽은 뒤 대체 단계가 또 씀) 마지막 줄만 센다
    out = []
    for r in (r for r in rows if r.get("etf") == etf):
        if out and r.get("run_id") and (r.get("run_id"), r.get("attempt")) == (out[-1].get("run_id"), out[-1].get("attempt")):
            out[-1] = r
        else:
            out.append(r)
    return out[-n:]


def fresh(res):
    """산출물이 이번 Actions 실행이 쓴 것인가(로컬 실행이면 늘 참). 아니면 모든 종류를 "검사 못 함"으로 본다 —
    본 단계·대체 단계가 모두 쓰기 전에 죽어 지난 산출물이 남은 경우(QQQ 구현 dr r1)."""
    r = os.environ.get("GITHUB_RUN_ID")
    return not r or res.get("runId") == f"{r}.{os.environ.get('GITHUB_RUN_ATTEMPT', '1')}"


def states(res, obs):
    """{종류: ("bad", 키) | ("ok", None) | ("unchecked", None)}."""
    ck, dt, out = (res.get("checks") or {}) if fresh(res) else {}, res.get("checkDetail") or {}, {}
    # 산출물은 지난 실행 것인데(복구가 JSON을 쓰기 전에 실패) 이번 실행이 관측에 실행 실패를 남겼으면 run만 bad로 센다(QQQ 구현 dr r2)
    rid, att = os.environ.get("GITHUB_RUN_ID"), os.environ.get("GITHUB_RUN_ATTEMPT", "1")
    run_obs = (not fresh(res) and rid and obs and obs[-1].get("run_id") == rid and str(obs[-1].get("attempt") or "1") == att
               and {"run_fail", "selfcheck"} & set(obs[-1].get("holds") or []))
    if run_obs:
        ck = {"run": "bad"}
    for k in IMMEDIATE:
        st = ck.get(k, "unchecked")
        if st == "bad":
            d = dt.get(k)
            key = (",".join(sorted(d)) if isinstance(d, (dict, list)) else k) or k
            out[k] = ("bad", f"{k}:{key}")
        else:
            out[k] = (st if st in ("ok", "unchecked") else "unchecked", None)
    # 이어질 때만 알리는 종류: 이번 실행 결과가 먼저 — ok면 해소, 검사 못 함이면 그대로, bad일 때만 실행 기록을 본다.
    # 실행 기록의 마지막 줄이 이번 실행(at = runAt)이 아니면(기록 실패) 판단하지 않는다.
    this_run = bool(obs) and (obs[-1].get("at") == res.get("runAt") or bool(run_obs))
    for k, (n, reasons) in CONSEC.items():
        st = ck.get(k, "unchecked")
        if st != "bad":
            out[k] = (st if st in ("ok", "unchecked") else "unchecked", None)
            continue
        runs = obs[-n:]
        def hit(r):
            if not reasons & set(r.get("holds") or []):
                return False
            # 날짜는 운용사 지연(S < P)만 센다 — 홈 세션 지연(S > P)은 알림 없음(설계 A.2)
            return k != "file_date" or bool(r.get("S") and r.get("P") and r["S"] < r["P"])
        out[k] = ("bad", k) if this_run and len(runs) == n and all(hit(r) for r in runs) else ("unchecked", None)
    return out


def code_sig_body(res, v2, repo):
    """미승인 해시마다 카드·승인 원문 중 diff가 가장 작은 것과의 unified diff."""
    un = (res.get("checkDetail") or {}).get("code_sig") or {}
    try:
        p = subprocess.run(["node", str(v2 / "etf" / "verdict_code_sig.js"), "--text"], capture_output=True, text=True, timeout=600)
        cur = {v["hash"]: v["text"] for v in json.loads(p.stdout).values() if isinstance(v, dict) and "hash" in v}
    except Exception:
        cur = {}
    src = {f.stem: f.read_text(encoding="utf-8") for f in sorted((ETF_DIR / "approved_src").glob("*.js"))}
    parts = []
    for h, cards in un.items():
        parts.append(f"### 새 해시 `{h}` — 카드 {len(cards)}장: {', '.join(cards[:20])}{' …' if len(cards) > 20 else ''}")
        if h not in cur:
            parts.append("지금 원문을 다시 만들지 못했다 — 카드 파일을 직접 본다.")
            continue
        if not src:
            parts.append("승인 원문이 없어 비교 불가.")
            continue
        best = min(src, key=lambda a: sum(1 for x in difflib.unified_diff(src[a].splitlines(), cur[h].splitlines(), lineterm="")))
        diff = list(difflib.unified_diff(src[best].splitlines(), cur[h].splitlines(), f"승인 {best}", f"새 {h}", lineterm=""))
        cut = len(diff) > DIFF_MAX
        parts.append(f"가장 가까운 승인 원문 `{best}` 대비 diff{' (앞 ' + str(DIFF_MAX) + '줄만 — 전체는 아래 링크)' if cut else ''}:")
        parts.append("```diff\n" + "\n".join(diff[:DIFF_MAX]) + "\n```")
        if repo:
            parts.append(f"- 승인 원문: https://github.com/{repo}/blob/main/v2/etf/approved_src/{best}.js\n"
                         f"- 카드 파일: https://github.com/{repo}/blob/main/v2/{cards[0]}_full_widget.html")
    hs = ",".join(un)
    parts.append(f"\n**승인하려면** diff를 확인한 뒤 Actions → \"ETF approve verdict code\" → Run workflow, hashes = `{hs}`. "
                 "승인 직후 판정이 바로 나온다는 보장은 없다(그 시각 운용사 파일이 늦으면 갱신 대기·보류). "
                 "적용 여부의 기준은 main의 승인 커밋(v2/etf/ticker_alias.json)이다 — 보통 이 이슈에 '승인 적용 커밋' 댓글도 달린다. "
                 "다음 ETF 실행이 문제없음을 확인하면 이 이슈는 닫힌다.")
    return "\n\n".join(parts)


def body_for(kind, key, res, v2, repo):
    session = (res.get("pending") or {}).get("P") or res.get("builtFor")
    head = f"**{KIND_TEXT[kind]}** — ETF {res.get('etf')} · 실행 {res.get('runAt')} · 홈 세션 {session}\n\n"
    if kind == "code_sig":
        main = code_sig_body(res, v2, repo)
    else:
        d = (res.get("checkDetail") or {}).get(kind)
        target = ", ".join(d) if isinstance(d, list) else (d or "—")
        reasons = "; ".join(f"{r['text']}: {r.get('detail') or ''}" for r in res.get("reasons") or [])
        main = f"대상: {target}" + (f"\n\n보류 사유: {reasons}" if reasons else "")
    return head + main


def run(etf, root, v2, repo, dry=False, runner=gh):
    res = json.loads((root / "v2" / "etf" / f"{etf}.json").read_text(encoding="utf-8"))
    obs = last_runs(root / "v2" / "etf" / "date_obs.jsonl", etf, 12)
    st = states(res, obs)
    issues = json.loads(runner(["issue", "list", "--label", LABEL, "--state", "open", "--limit", "100",
                                "--json", "number,title,body"]) or "[]")
    acts = []
    for kind, (state, key) in st.items():
        if kind == "code_sig":
            continue   # ETF 공통 이슈 — run_code_sig
        prefix = f"[ETF {etf} {kind}]"
        mine = [i for i in issues if i["title"].startswith(prefix)]
        cur = mine[0] if mine else None
        old_key = (re.search(r"<!-- etf-key: (.*?) -->", cur["body"] or "") or [None, None])[1] if cur else None
        if state == "bad":
            key = hashlib.sha256(key.encode()).hexdigest()[:12]   # 표식은 고정 길이 — 본문을 줄여도 잘리지 않게
            mark = f"\n\n<!-- etf-key: {key} -->"
            body = body_for(kind, key, res, v2, repo)
            if len(body) + len(mark) > BODY_MAX:   # diff가 길면 링크만 — 이슈가 아예 안 열리는 것보다 낫다
                body = re.sub(r"```diff\n.*?```", "(diff가 길어 생략 — 아래 링크에서 승인 원문과 카드 파일을 비교한다)", body, flags=re.S)
                body = body[:BODY_MAX - len(mark) - 20] + ("\n…(잘림)" if len(body) > BODY_MAX - len(mark) - 20 else "")
            body += mark
            if not cur:
                acts.append(("create", kind))
                if not dry:
                    runner(["issue", "create", "--label", LABEL, "--title", f"{prefix} {KIND_TEXT[kind]}", "--body-file", "-"], body)
            elif old_key != key:
                acts.append(("comment", kind))
                if not dry:
                    runner(["issue", "comment", str(cur["number"]), "--body-file", "-"], "사건이 바뀌었다.\n\n" + body)
                    runner(["issue", "edit", str(cur["number"]), "--body-file", "-"], body)
        elif state == "ok" and cur:
            acts.append(("close", kind))
            if not dry:
                runner(["issue", "close", str(cur["number"]), "--comment", f"이번 실행({res.get('runAt')})에서 문제없음을 확인해 닫는다."])
    return acts


CODE_SIG_TITLE = "[ETF code_sig]"
LEGACY_CODE_SIG = ("[ETF SPY code_sig]",)


def issue_hashes(body):
    m = re.search(r"<!-- etf-hashes: ([0-9a-f,]*) -->", body or "")
    return [h for h in (m.group(1).split(",") if m else []) if h]


def run_code_sig(etfs, root, v2, repo, dry=False, runner=gh, approved=None):
    """ETF 공통 code_sig 이슈. approved = 설정의 승인 해시 집합(닫기·남기기 판단)."""
    if approved is None:
        try:
            approved = set(json.loads((root / "v2" / "etf" / "ticker_alias.json").read_text(encoding="utf-8"))["approvedVerdictCode"])
        except Exception:   # noqa: BLE001
            approved = set()
    ress = {}
    for e in etfs:
        try:
            ress[e] = json.loads((root / "v2" / "etf" / f"{e}.json").read_text(encoding="utf-8"))
        except Exception:   # noqa: BLE001
            ress[e] = {}
    st = {e: ((r.get("checks") or {}).get("code_sig", "unchecked") if fresh(r) else "unchecked") for e, r in ress.items()}
    issues = json.loads(runner(["issue", "list", "--label", LABEL, "--state", "open", "--limit", "100",
                                "--json", "number,title,body"]) or "[]")
    cur = next((i for i in issues if i["title"].startswith(CODE_SIG_TITLE) or i["title"].startswith(LEGACY_CODE_SIG)), None)
    old = issue_hashes(cur["body"]) if cur else []
    merged = {}
    for e, r in ress.items():
        if st[e] == "bad":
            for h, cards in ((r.get("checkDetail") or {}).get("code_sig") or {}).items():
                merged.setdefault(h, set()).update(f"{c}({e})" for c in cards)
    if any(v == "unchecked" for v in st.values()):   # 검사 못 한 ETF — 전에 낸 미승인 해시는 확인될 때까지 남긴다
        for h in old:
            if h not in approved:
                merged.setdefault(h, set()).add("검사 대기")
    acts = []
    if "bad" in st.values():
        hashes = sorted(merged)
        key = hashlib.sha256(",".join(hashes).encode()).hexdigest()[:12]
        mark = f"\n\n<!-- etf-key: {key} -->\n<!-- etf-hashes: {','.join(hashes)} -->"
        newest = max((r.get("runAt") or "" for r in ress.values()), default="")
        pseudo = {"etf": " · ".join(f"{e} {st[e]}" for e in etfs), "runAt": newest,
                  "builtFor": next((r.get("builtFor") for r in ress.values() if r.get("builtFor")), None),
                  "checkDetail": {"code_sig": {h: sorted(c) for h, c in merged.items()}}}
        body = body_for("code_sig", key, pseudo, v2, repo)
        if len(body) + len(mark) > BODY_MAX:
            body = re.sub(r"```diff\n.*?```", "(diff가 길어 생략 — 아래 링크에서 승인 원문과 카드 파일을 비교한다)", body, flags=re.S)
            body = body[:BODY_MAX - len(mark) - 20] + "\n…(잘림)"
        body += mark
        old_key = (re.search(r"<!-- etf-key: (.*?) -->", cur["body"] or "") or [None, None])[1] if cur else None
        if not cur:
            acts.append(("create", "code_sig"))
            if not dry:
                runner(["issue", "create", "--label", LABEL, "--title", f"{CODE_SIG_TITLE} {KIND_TEXT['code_sig']}", "--body-file", "-"], body)
        elif old_key != key:
            acts.append(("comment", "code_sig"))
            if not dry:
                runner(["issue", "comment", str(cur["number"]), "--body-file", "-"], "사건이 바뀌었다.\n\n" + body)
                runner(["issue", "edit", str(cur["number"]), "--body-file", "-"], body)
    elif cur and all(v == "ok" for v in st.values()):   # 모든 ETF가 이번 실행에서 명시적으로 ok일 때만(설계 r3 C-3)
        acts.append(("close", "code_sig"))
        if not dry:
            runner(["issue", "close", str(cur["number"]), "--comment",
                    "이번 실행에서 판정 코드 해시 문제가 없음을 확인해 닫는다(" + ", ".join(f"{e} {v}" for e, v in st.items()) + ")."])
    return acts


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--etf", default="SPY,QQQ", help="쉼표로 여러 ETF")
    ap.add_argument("--root", default=str(ETF_DIR.parents[1]))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root)
    try:
        if not a.dry_run:
            gh(["label", "create", LABEL, "--color", "B60205", "--description", "ETF 판정 알림(자동)", "--force"])
        etfs = [e.strip() for e in a.etf.split(",") if e.strip()]
        repo, acts = os.environ.get("GITHUB_REPOSITORY"), []
        for e in etfs:
            try:
                acts += [(x, f"{e} {k}") for x, k in run(e, root, root / "v2", repo, a.dry_run)]
            except Exception as ex:   # 한 ETF의 알림 실패가 다른 ETF를 막지 않게
                acts.append(("실패", f"{e} {type(ex).__name__}"))
        acts += run_code_sig(etfs, root, root / "v2", repo, a.dry_run)
        line = f"ETF 알림 {a.etf}: " + (", ".join(f"{x}:{k}" for x, k in acts) or "할 일 없음")
    except Exception as ex:   # 알림 실패는 판정에 영향 없음 — 요약에만 남긴다
        line = f"ETF 알림 {a.etf} 실패: {type(ex).__name__} {str(ex)[:120]}"
    print(line)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(f"- {line}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
