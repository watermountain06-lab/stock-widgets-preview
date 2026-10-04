#!/usr/bin/env python3
"""카드의 밴드 백테스트(BACKTEST)를 다시 만들고, 실적 발표를 넘긴 구간을 표시한다(안건 C1, 2026-10-01 사용자 결정 — 2026-10-03 적용).

결정: 흑자 공백(또는 자료 공백)으로 한 체크포인트가 다음 실적 발표를 넘겨 이어지면 그 구간은 적중률에서 뺀다. 끝난 체크포인트가
4개 미만이면 적중률 "해당 없음". 이 스크립트는 카드에 이미 들어 있는 일봉({T}_DAILY)과 scripts/{T}_eps_history.json으로
scripts/compute_earnings_backtest_band.py(카드와 같은 기본 설정)를 다시 돌리고, 각 체크포인트에 `spans_earnings`(구간 안에 든
다른 실적 공시 수)를 붙여 BACKTEST만 바꾼다. 카드 JS({T}_BAND_HIT)는 spans_earnings > 0인 구간을 빼고 센다.

다른 실적 공시 = EPS 이력의 분기(quarter_end)마다 첫 공시일을 잡아, 체크포인트 날짜 뒤부터 구간 끝 전까지 든 분기 수. 다시 계산한 배열의
체크포인트 날짜는 그 자체가 EPS 공시일이라(compute_earnings_backtest_band.py) 같은 분기를 따로 거를 필요가 없고, 같은 분기의 재공시는
분기 단위로 묶여 한 번만 센다(Codex·Fable 2026-10-03 — 처음 둔 45일 완충은 근거가 맞지 않아 뺐다).
EPS 이력에 빠진 분기가 있으면 그 실적은 보이지 않는다(공시 자체가 없는 공백은 세지 못함).

루트 카드에서 손으로 확인한 PER 제외 창(일회성 비용으로 TTM EPS가 눌린 기간)은 EXCLUDE_PER_WINDOW로 넘긴다 — 빠뜨리면 밴드가 그 기간의
부푼 PER까지 담아 넓어진다(Fable 2026-10-03, IBM 2024-02-26 상단 24.6 → 67.8배).
TSM·ASML은 루트 배열을 그대로 둔다: v2 EPS 이력이 현지 통화(대만달러·유로)라 달러 가격으로 나눈 PER에 환율 변동이 섞인다(안건 C10).
PANW도 루트(분할 뒤만 남긴) 배열을 둔다(D20 — 일회성 세금 이익 처리와 함께 다시 정한다). 루트 JSON의 기본값과 다른 설정(제외 창·GEV 1년 창)은 위 표로 넘긴다 — 63개 전수 확인(Fable).

    python3 v2/refresh_backtest.py ORCL            # 다시 계산 + 표시, 카드에 쓴다
    python3 v2/refresh_backtest.py ORCL --flag-only  # 다시 계산하지 않고 지금 배열에 표시만
    python3 v2/refresh_backtest.py ORCL --dry-run
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
# 루트 백테스트 JSON(stock-widgets-redesign/scripts/{T}_earnings_backtest.json)의 exclude_per_window — 일회성 비용 기간
EXCLUDE_PER_WINDOW = {
    "IBM": ("2022-10-25", "2023-10-30"),   # 연금 정산 비용
    # QCOM ("2025-11-05", "2026-04-28") 세금 비용 창은 2026-10-04 뺐다 — 그 세금 항목을 tax_oneoff.json이 EPS에서 직접 뺀다(A8 ①)
    "ABBV": ("2025-11-04", "2026-02-19"),
    "AMD": ("2023-05-03", "2024-01-30"),
}
# 다시 계산하지 않고 지금(루트) 배열에 표시만 — TSM·ASML 현지 통화 EPS(C10), PANW는 D20으로 한동안 루트 배열을 지켰다가 A9·A8 ①로 풀었다(2026-10-04).
KEEP_ROOT = {"TSM", "ASML"}   # PANW는 2026-10-04 뺐다 — 흑자 초기(A9 B6)와 일회성 세금(A8 ①)을 반영하니 v2 재계산 밴드가 정상(폭 1.3~2.9배)
# 체크포인트가 실적 발표일인 루트 배열(EPS 공시일은 몇 주 뒤) — 같은 분기 공시를 거르는 45일. PANW 배열은 체크포인트가 곧 공시일이라 0일(Codex)
RELEASE_DATE_CHECKPOINTS = {"TSM", "ASML"}
KEEP_EMPTY = {"BA", "COF"}   # 적정주가 밴드·백테스트를 카드 결정으로 비운 종목(CARD_ITEMS BA 규칙)
# 루트 JSON의 trailing_years가 기본(2년)과 다른 종목 — GEV는 2024-04 상장이라 직전 1년 PER로 잰다
TRAILING_YEARS = {"GEV": 1}


def js_array(h, name):
    """카드의 const {name} = [...] 배열 위치(시작, 끝)와 값."""
    m = re.search(rf"const {name}\s*=\s*\[", h)
    if not m:
        return None, None, None
    st, d, ins, esc = m.end() - 1, 0, None, False
    for i in range(st, len(h)):
        ch = h[i]
        if ins:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == ins:
                ins = None
            continue
        if ch in "\"'":
            ins = ch
        elif ch == "`" or h.startswith("//", i) or h.startswith("/*", i):
            raise ValueError(f"{name}: 배열 안에 템플릿 문자열·주석이 있어 단순 파서로 못 읽는다")
        elif ch == "[":
            d += 1
        elif ch == "]":
            d -= 1
            if d == 0:
                raw = h[st:i + 1]
                node = subprocess.run(["node", "-e", f"process.stdout.write(JSON.stringify({raw}))"], capture_output=True, text=True)
                if node.returncode != 0:
                    raise ValueError(f"{name}: node 평가 실패 — {node.stderr[-200:]}")
                return st, i + 1, json.loads(node.stdout)
    return None, None, None


def first_filings(eps_rows):
    """분기마다 첫 공시일."""
    first = {}
    for e in eps_rows:
        q, d = e.get("quarter_end"), e.get("available_date")
        if q and d and (q not in first or d < first[q]):
            first[q] = d
    return sorted(first.values())


def ramp_windows(eps_rows, last_day):
    """흑자 초기 구간(A9, 2026-10-04 사용자 결정 B6) — 파일 안에서 처음 흑자 TTM이 된 공시일부터, 최근 4분기가 모두 흑자 분기가 된
    공시일 전날까지. 이 구간의 PER은 EPS가 아주 작아 수백~수천 배라(PANW 2023 TTM 0.04→0.3) 밴드 표본에서 빼고, 그 안의 체크포인트는
    적중률에서 뺀다. 한 번 흑자였다가 일회성 손실로 적자가 된 뒤의 회복(NEM·BMY)은 해당하지 않는다(그 전에 흑자 TTM이 있다).
    부호만 본다(크기를 보지 않음 — 백테스트 스크립트 docstring 6번): 구간 안에 적자 분기가 하나라도 끼면 네 분기 셈을 다시 시작해 구간이 길어진다
    (UBER 2024년 1분기 지분 평가 손실로 2024-08 → 2025-05, 일부러 보수적으로 둔다). 첫 흑자 때 이미 네 분기가 모두 흑자면 구간이 0이다
    (PLTR — 흑자 초기 PER 약 250배는 이 규칙으로 안 걸린다)."""
    # 분기 순서(quarter_end)로 센다 — 공시일 순으로 세면 나중 비교 열로 실린 옛 분기가 끼어 순서가 어긋난다(PANW, Codex)
    rows = sorted([e for e in eps_rows if e.get("available_date") and e.get("quarter_end") and e.get("ttm_eps") is not None],
                  key=lambda e: e["quarter_end"])
    out = []
    for i, e in enumerate(rows):
        if i and rows[i - 1]["ttm_eps"] <= 0 < e["ttm_eps"] and not any(r["ttm_eps"] > 0 for r in rows[:i]):
            end = None
            for j in range(max(i, 3), len(rows)):
                if all(r.get("quarter_eps") is not None and r["quarter_eps"] > 0 for r in rows[j - 3:j + 1]):
                    end = max(r["available_date"] for r in rows[j - 3:j + 1])   # 네 분기가 모두 공시된 날
                    break
            start = e["available_date"]
            if end is None:
                out.append([start, last_day])   # 아직 안 끝난 구간은 마지막 날까지
            elif end > start:
                out.append([start, (date.fromisoformat(end) - timedelta(days=1)).isoformat()])
    return out


def flag(bt, eps_dates, last_day, lag_days=0, ramps=()):
    """lag_days — 발표일 체크포인트 루트 배열(RELEASE_DATE_CHECKPOINTS)은 체크포인트가 실적 발표일이고 EPS 공시일(6-K·20-F)이 몇 주 뒤라, 같은 분기 공시를 거르려고 45일을 둔다."""
    for cp in bt:
        end = last_day if cp.get("is_open") else (cp.get("period_end_date") or last_day)
        start = (date.fromisoformat(cp["checkpoint_date"]) + timedelta(days=lag_days)).isoformat()
        cp["spans_earnings"] = sum(1 for x in eps_dates if start < x < end)
        if any(ws <= cp["checkpoint_date"] <= we for ws, we in ramps):
            cp["early_profit"] = True   # A9 B6 — 흑자 초기 구간의 체크포인트
    return bt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--flag-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    t = a.ticker.upper()
    if t in KEEP_EMPTY and not a.flag_only:
        sys.exit(f"{t}: 백테스트를 일부러 비운 카드다(BA 규칙) — 다시 계산하지 않는다")
    p = os.path.join(HERE, f"{t}_full_widget.html")
    h = open(p, encoding="utf-8").read()
    _, _, daily = js_array(h, f"{t}_DAILY")
    st, en, bt_old = js_array(h, f"{t}_BACKTEST")
    assert daily and st is not None, "카드에 DAILY·BACKTEST 배열이 없다"
    eps_path = os.path.join(REPO, "scripts", f"{t}_eps_history.json")
    eps_rows = json.load(open(eps_path))
    eps_dates = first_filings(eps_rows)
    ramps = ramp_windows(eps_rows, daily[-1][0])
    if a.flag_only or t in KEEP_ROOT:
        bt = bt_old
    else:
        # 분사 종목은 자기 이력과 같은 시작일부터(build_multiple_history.HISTORY_START — 분사 전 PER이 섞이지 않게, WDC·T 선례)
        sys.path.insert(0, HERE)
        import build_multiple_history as bmh
        bt_start = bmh.HISTORY_START.get(t)
        work = tempfile.mkdtemp(prefix=f"{t}_bt_")
        # 회사가 밝힌 일회성 법인세 항목(v2/tax_oneoff.json)은 카드 PER과 같게 TTM EPS에서 뺀다(A8 ①, 2026-10-04)
        import build_multiple_history as bmh2
        adj = [{**e, "ttm_eps": round(e["ttm_eps"] + bmh2.oneoff_in_ttm(t, e.get("quarter_end"), "eps"), 6)}
               if e.get("ttm_eps") is not None else e for e in eps_rows]
        if adj != eps_rows:
            eps_path = os.path.join(work, "eps_adj.json")
            json.dump(adj, open(eps_path, "w"))
        tmp, out = os.path.join(work, "daily.json"), os.path.join(work, "backtest.json")
        json.dump({"daily": [b for b in daily if not bt_start or b[0] >= bt_start]}, open(tmp, "w"))
        cmd = [sys.executable, os.path.join(REPO, "scripts", "compute_earnings_backtest_band.py"), t,
               "--eps", eps_path, "--daily-json", tmp, "--out", out]
        if t in TRAILING_YEARS:
            cmd += ["--trailing-years", str(TRAILING_YEARS[t])]
        if t in EXCLUDE_PER_WINDOW:
            cmd += ["--exclude-per-window", *EXCLUDE_PER_WINDOW[t]]
        if ramps:
            wj = os.path.join(work, "ramps.json")
            json.dump(ramps, open(wj, "w"))
            cmd += ["--exclude-per-windows-json", wj]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(r.stderr[-500:])
        bt = json.load(open(out))["checkpoints"]
    bt = flag(bt, eps_dates, daily[-1][0], 45 if t in RELEASE_DATE_CHECKPOINTS else 0, () if t in KEEP_ROOT else ramps)
    if t in KEEP_ROOT:
        # 루트 배열의 열린 구간이 다음 실적을 넘긴 건 흑자 공백이 아니라 배열이 멈춘 탓 — C1 제외 대상이 아니다(Fable 2026-10-03, PANW).
        # 빼면 놓친 날만 사라져 적중률이 오른다. 표시만 남기고 센다.
        for cp in bt:
            if cp.get("is_open") and cp["spans_earnings"]:
                cp["stale_missing"] = [x for x in eps_dates if x > cp["checkpoint_date"]]   # 반영 못 한 실적 공시일
                cp["spans_earnings"] = 0
    same = [c for c in bt if any(o["checkpoint_date"] == c["checkpoint_date"] for o in bt_old)]
    diffs = [c["checkpoint_date"] for c in same
             if {k: v for k, v in c.items() if k not in ("spans_earnings", "is_open", "period_end_date", "realized_low", "realized_high", "zone")}
             != {k: v for k, v in next(o for o in bt_old if o["checkpoint_date"] == c["checkpoint_date"]).items()
                 if k not in ("spans_earnings", "is_open", "period_end_date", "realized_low", "realized_high", "zone")}]
    print(t, f"체크포인트 {len(bt_old)} → {len(bt)}", "새로:", [c["checkpoint_date"] for c in bt if c not in same],
          "밴드가 달라진 기존 체크포인트:", diffs, "실적을 넘긴 구간:",
          [(c["checkpoint_date"], c["spans_earnings"], c.get("is_open")) for c in bt if c["spans_earnings"]])
    if a.dry_run:
        return
    h = h[:st] + json.dumps(bt, ensure_ascii=False, separators=(", ", ": ")) + h[en:]
    open(p, "w", encoding="utf-8").write(h)
    print("교체:", p)


if __name__ == "__main__":
    main()
