#!/usr/bin/env python3
"""ETF 판정 — 카드 판정 코드 해시 승인(사람이 diff를 보고 실행한다, 2026-10-20 설계 dr 합의·사용자 결정).

    python3 v2/etf/etf_approve.py --hashes abc123def456,0123456789ab --note "12-01 판정 구조 변경 승인"
    python3 v2/etf/etf_approve.py --bootstrap      # 이미 승인 목록에 있는 해시의 원문만 approved_src/에 채운다

하는 일: 서명 스크립트(verdict_code_sig.js --text)로 지금 카드가 내는 해시와 원문을 받아, 승인할 해시마다
(1) 그 해시를 내는 카드가 지금 있는지 (2) sha256(원문) 앞 12자가 그 해시인지 확인한 뒤
ticker_alias.json approvedVerdictCode에 더하고 원문을 approved_src/<해시>.js로 저장한다. 이미 승인된 해시는 그대로 둔다
(같은 해시로 다시 돌려도 무해). 지금 카드가 내지 않는 해시는 거부한다(종료 코드 2).
ETF 재평가·이슈 닫기는 워크플로(etf_approve.yml)가 승인 커밋 뒤 etf_index.yml을 다시 부른다.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ETF_DIR = Path(__file__).resolve().parent
CFG = ETF_DIR / "ticker_alias.json"
SRC = ETF_DIR / "approved_src"


def current_texts(v2):
    """{해시: 원문} — 지금 카드들이 내는 것(해시 검증 통과분만)."""
    p = subprocess.run(["node", str(v2 / "etf" / "verdict_code_sig.js"), "--text"], capture_output=True, text=True, timeout=600)
    if p.returncode != 0:
        raise SystemExit(f"서명 스크립트 실패(종료 코드 {p.returncode})")
    out = {}
    for card, v in json.loads(p.stdout).items():
        if isinstance(v, dict) and "hash" in v and hashlib.sha256(v["text"].encode()).hexdigest()[:12] == v["hash"]:
            out.setdefault(v["hash"], {"text": v["text"], "cards": []})["cards"].append(card)
    return out


def write_cfg(cfg, path):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--hashes", default="", help="쉼표로 나눈 해시(12자)")
    ap.add_argument("--note", default="")
    ap.add_argument("--bootstrap", action="store_true")
    ap.add_argument("--remaining", action="store_true",
                    help="표준 입력의 이슈 본문 표식 <!-- etf-hashes: … --> 중 아직 승인 목록에 없는 해시를 찍는다(승인 워크플로 댓글용)")
    ap.add_argument("--v2", default=str(ETF_DIR.parent))
    ap.add_argument("--cfg", default=str(CFG))
    ap.add_argument("--src", default=str(SRC))
    a = ap.parse_args(argv)
    cfg_path, src = Path(a.cfg), Path(a.src)
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    approved = cfg["approvedVerdictCode"]
    if a.remaining:
        m = re.search(r"<!-- etf-hashes: ([0-9a-f,]*) -->", sys.stdin.read())
        hs = [h for h in (m.group(1).split(",") if m else []) if h]
        rest = [h for h in hs if h not in approved]
        print(", ".join(rest) if rest else ("없음" if hs else "이슈에 해시 표식 없음"))
        return 0
    texts = current_texts(Path(a.v2))
    src.mkdir(parents=True, exist_ok=True)
    if a.bootstrap:
        done = []
        for h in approved:
            if h in texts and not (src / f"{h}.js").exists():
                (src / f"{h}.js").write_text(texts[h]["text"], encoding="utf-8")
                done.append(h)
        missing = [h for h in approved if not (src / f"{h}.js").exists()]
        print(f"원문 채움 {len(done)}개 {done} · 원문 없음(지금 카드가 안 냄) {missing}")
        return 0
    want = [h.strip() for h in a.hashes.split(",") if h.strip()]
    if not want or any(len(h) != 12 or any(c not in "0123456789abcdef" for c in h) for h in want):
        print("해시는 12자리 소문자 16진수, 쉼표로 나눈다")
        return 2
    unknown = [h for h in want if h not in texts]
    if unknown:
        print(f"지금 어느 카드도 내지 않는 해시라 승인하지 않는다: {unknown}")
        return 2
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    run = os.environ.get("GITHUB_RUN_ID", "local")
    added = []
    for h in want:
        (src / f"{h}.js").write_text(texts[h]["text"], encoding="utf-8")
        if h not in approved:
            cards = texts[h]["cards"]
            approved[h] = (f"승인 {day}: {a.note or '메모 없음'} — 카드 {len(cards)}장({', '.join(cards[:5])}"
                           f"{'…' if len(cards) > 5 else ''}) (run {run})")
            added.append(h)
    if added:
        write_cfg(cfg, cfg_path)
    print(f"승인 추가 {added} · 이미 승인됨 {[h for h in want if h not in added]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
