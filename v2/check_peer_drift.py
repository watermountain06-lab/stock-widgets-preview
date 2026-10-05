#!/usr/bin/env python3
"""카드의 동종업 칸이 지금 비교군 자료로 다시 계산한 값과 같은지 본다(2026-10-04).

한 카드의 자기 배수를 고치면 그 값이 다른 카드의 비교군(카드 유니버스·S&P500 비교군 파일)에도 들어간다.
그런데 다른 카드의 동종업 칸은 다시 계산하지 않아 어긋났다 — 2026-10-04에 4장(COST·GE 카드가 비교군 값을
채운 뒤의 WMT·CAT, IT 카드 값이 고쳐진 뒤의 FTNT, XOM). 일일 파이프라인은 밸류에이션 탭을 건드리지 않으므로,
카드 배수나 비교군 파일을 고친 뒤에는 이 점검을 돌려 어긋난 카드를 다시 계산한다.
비교 종목은 카드 자신의 배수와 같은 날(자기 이력 창의 끝) 종가로 환산한다(build_peer_score 기본) — 오늘 종가로 하면
주가 움직임만으로 30장이 어긋나 보였다(Fable).

    python3 v2/check_peer_drift.py            # 어긋난 카드 목록(동종업 점수·표 변화)
    python3 v2/check_peer_drift.py NVDA AMD   # 일부만

카드에 쓰지 않는다(build_peer_score.py --json으로 계산만). 은행·보험·BRKB처럼 동종업을 따로 내는 카드는 뺀다.
"""
import json
import os
import subprocess
import sys
import tempfile

V2 = os.path.dirname(os.path.abspath(__file__))
# build_peer_score 일반 경로를 쓰지 않는 카드 — BRKB(두 기둥 어댑터), COF(은행 카드 어댑터: PTBV·PER 음수 제외).
# 다른 금융 카드는 일반 경로로 다시 계산해도 카드 값과 같았다(2026-10-04 전 카드 대조).
SKIP = {"BRKB", "COF"}


def card_peer(t):
    h = open(os.path.join(V2, f"{t}_full_widget.html"), encoding="utf-8").read()
    k = f"const {t}_VALUATION = "
    if k not in h:
        return None
    return json.JSONDecoder().raw_decode(h, h.index(k) + len(k))[0]["peer"]


def fresh_peer(t):
    with tempfile.NamedTemporaryFile(suffix=".json") as f:
        r = subprocess.run([sys.executable, os.path.join(V2, "build_peer_score.py"), t, "--self",
                            os.path.join(V2, f"{t}_multiples.json"), "--json", f.name], capture_output=True, text=True)
        if r.returncode != 0:
            return None
        return json.load(open(f.name))


def vote(s):
    return None if s is None else (1 if s >= 70 else -1 if s < 30 else 0)


def main():
    tickers = sys.argv[1:] or sorted(f.split("_")[0] for f in os.listdir(V2) if f.endswith("_full_widget.html"))
    drift, failed, nomult = 0, [], []
    for t in tickers:
        if t in SKIP:
            continue
        if not os.path.exists(os.path.join(V2, f"{t}_multiples.json")):
            nomult.append(t)            # 은행 RIM 카드 등 — 자기 이력 JSON이 없어 이 점검 밖
            continue
        try:
            c, r = card_peer(t), fresh_peer(t)
        except Exception as e:          # 카드 블록이 깨졌거나 JSON을 못 읽음 — 실패로 센다(Codex)
            print(f"{t}: 읽기 실패 {type(e).__name__}")
            c = r = None
        if c is None or r is None:
            failed.append(t)
            print(f"{t}: 계산 실패")
            continue
        cm = {m["metric"]: (m["score"], m["rank"], m["peers"]) for m in c["metrics"]}
        rm = {m["metric"]: (m["score"], m["rank"], m["peers"]) for m in r["metrics"]}
        if c["score"] == r["score"] and cm == rm:
            continue
        drift += 1
        ch = {m: (cm.get(m), rm.get(m)) for m in sorted(set(cm) | set(rm)) if cm.get(m) != rm.get(m)}
        flag = "  ← 표 바뀜" if vote(c["score"]) != vote(r["score"]) else ""
        print(f"{t}: 동종업 {c['score']} → {r['score']}{flag}  {ch}")
    print(f"어긋난 카드 {drift}장 · 계산 실패 {len(failed)}장 {failed} · 점검 밖(_multiples.json 없음) {nomult} · 제외 {sorted(SKIP)}")
    sys.exit(2 if failed else 1 if drift else 0)


if __name__ == "__main__":
    main()
