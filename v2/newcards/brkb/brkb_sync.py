#!/usr/bin/env python3
"""BRKB 원문 저장소(.sec_cache/brk_facts.json)를 새 10-Q·10-K까지 채운다(2026-10-12, BRKB 생성기).

SEC 제출 목록(하루 한 번 받음)에 저장소보다 새 10-Q·10-K가 있으면 원문을 받아 사실을 다시 쌓고(adapters/brkb_facts.py),
재무 요약(fundamental_data/BRKB_financials.json — 매출 CAGR용)도 새로 받는다. 새 공시가 없으면 아무것도 하지 않는다.
카드가 그 공시를 쓰는 날은 brkb_fill.py가 정한다(마지막 종가일 하루 전까지 접수된 것만).
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.dirname(HERE))
import auto_card as ac  # noqa: E402

CIK = "0001067983"
STORE = os.path.join(V2, ".sec_cache", "brk_facts.json")
sub = ac._submissions(CIK)
latest = max((sub["filingDate"][i] for i, f in enumerate(sub["form"]) if f in ("10-Q", "10-K")), default=None)
have = max((f["filed"] for f in json.load(open(STORE)) if f["form"] in ("10-Q", "10-K")), default=None) if os.path.exists(STORE) else None
if latest and (have is None or latest > have):
    print(f"BRKB: 새 공시 {latest}(저장소 {have}) — 원문을 받아 사실을 다시 쌓는다", flush=True)
    subprocess.run([sys.executable, os.path.join(V2, "adapters", "brkb_facts.py")], check=True)
    subprocess.run([sys.executable, os.path.join(V2, "vendor", "fetch_financials.py"), "BRKB", "--cik", CIK, "--years", "5",
                    "--out", os.path.join(V2, "fundamental_data", "BRKB_financials.json")], check=True)
else:
    print(f"BRKB: 새 공시 없음(SEC {latest}, 저장소 {have})")
