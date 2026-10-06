#!/usr/bin/env python3
"""S&P500 섹터 비교군 파일을 한 기준일로 다시 만든다(2026-10-06, 카드 10/5 갱신).

각 파일은 `sector_universe.py`로 만들고, 그동안 파일에 손으로 했던 두 가지를 규칙으로 다시 적용한다:
  1. 이상값 제외 — PSR이 60배를 넘거나 어떤 배수가 0이면 그 배수를 빼고 skipped에 적는다(2026-10-02 WELL 카드, 리츠 매출·주식 수 태그 오류).
  2. 보험사 PSR 제외 — HIG·MET는 매출 태그가 일부 매출만 담아 PSR이 20배를 넘는다(2026-10-02, 보험사 PSR은 대개 1~3배).
카드가 있는 종목의 행을 그 카드의 엔진 값으로 바꾸는 일은 카드를 다시 만든 뒤 `sync_peer_rows.py`가 한다.

    python3 v2/adapters/refresh_peer_files.py --asof 2026-10-05            # 전부
    python3 v2/adapters/refresh_peer_files.py --asof 2026-10-05 energy     # 일부
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
OUT = os.path.join(V2, "peer_universe")
FILES = {
    "communication_services": ("Communication Services", None),
    "consumer_discretionary": ("Consumer Discretionary", None),
    "consumer_staples": ("Consumer Staples", None),
    "energy": ("Energy", None),
    "health_care": ("Health Care", None),
    "industrials": ("Industrials", None),
    "materials": ("Materials", None),
    "real_estate": ("Real Estate", None),
    "utilities": ("Utilities", None),
    "asset_managers": ("Financials", "Asset Management & Custody Banks"),
    "insurers": ("Financials", "Property & Casualty Insurance,Multi-line Insurance,Life & Health Insurance"),
    "payments_exchanges": ("Financials", "Transaction & Payment Processing Services,Financial Exchanges & Data"),
}
# 행 전체를 빼는 종목 — 분사 직후라 가격(분사 뒤)과 재무(분사 전)가 섞인다
ROW_SKIP = {"materials": {"CTVA": "10/1 사업 분리(분사) — 주가 $77.65 → $12.57, 분할 기록 없음. 분사 뒤 가격과 분사 전 재무가 섞여 배수가 의미 없음(2026-10-06)"}}
MANUAL_SKIP = {"insurers": {("HIG", "psr"): "매출 태그가 일부 매출만 담아 PSR이 과대(보험사 PSR은 대개 1~3배, 2026-10-02)",
                            ("MET", "psr"): "매출 태그가 일부 매출만 담아 PSR이 과대(보험사 PSR은 대개 1~3배, 2026-10-02)"}}


def outliers(name, d):
    sk = d.setdefault("skipped", {})
    for t, why in ROW_SKIP.get(name, {}).items():
        if d["tickers"].pop(t, None) is not None:
            sk[t] = why
    for t, row in d["tickers"].items():
        for k in list(row):
            v = row[k]
            if not isinstance(v, (int, float)):
                continue
            why = None
            if (k == "psr" and v > 60) or v == 0:
                why = f"이상값 {v} 제외 — 매출·주식 수 태그 오류 의심(PSR 60배 초과 또는 0, 2026-10-02 WELL 카드 규칙)"
            elif (t, k) in MANUAL_SKIP.get(name, {}):
                why = MANUAL_SKIP[name][(t, k)] + f" — {v}"
            if why:
                del row[k]
                sk[f"{t}:{k}"] = why


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--asof", required=True)
    ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    failed = []
    for name in a.names or list(FILES):
        sector, sub = FILES[name]
        cmd = [sys.executable, os.path.join(HERE, "sector_universe.py"), sector, "--asof", a.asof, "--name", name]
        if sub:
            cmd += ["--sub", sub]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"{name}: 실패\n{r.stdout[-800:]}{r.stderr[-800:]}")
            failed.append(name)
            continue
        p = os.path.join(OUT, f"{name}.json")
        d = json.load(open(p))
        outliers(name, d)
        json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
        print(f"{name}: {len(d['tickers'])}종목 · 제외 {len(d.get('skipped', {}))} · 기준일 {d.get('asOf')}")
    if failed:   # 실패한 파일은 예전 기준일로 남는다 — 섞인 채 넘어가지 않게 멈춘다(Codex 2026-10-06)
        sys.exit(f"실패 {failed} — 기준일이 섞였다")


if __name__ == "__main__":
    main()
