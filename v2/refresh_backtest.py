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

차트 5년 전체(2026-10-08 사용자 결정): v2/backtest_pre/{T}.json(build_backtest_pre.py)의 종가 중 **DAILY 첫날 이전 봉만** 앞에 붙여
직전 2년 PER 표본으로 쓴다. 체크포인트는 구간 끝이 DAILY 첫날 뒤인 것만 남긴다 — 차트 첫날에 걸친 직전 체크포인트는 남기고 적중·실현 범위는
차트 안 봉으로만 센다(카드 JS도 DAILY 안 봉만 센다). 걸친 구간의 zone·realized_per_*는 compute가 낸 전체 구간 값 그대로다(JS는 쓰지 않음).
DAILY가 앞에서 잘려 체크포인트가 차트 밖으로 완전히 나가거나 환율 카드의 걸친 구간이 바뀌면 daily_price.band_catch_up이 다시 돌린다.
보관 파일 문제(없음·겹침 불일치·만료)는 종료 코드 3으로 끝난다 — 일일 갱신은 이때 백테스트를 그대로 두고 경고만 남긴다.
EPS는 분기마다 처음 공시된 행만 쓴다(drop_stale_quarters — 같은 분기의 뒤늦은 재공시·정정도 뺀다).
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
KEEP_ROOT = set()   # TSM·ASML은 C10(2026-10-04)으로 환율 환산해 다시 계산   # PANW는 2026-10-04 뺐다 — 흑자 초기(A9 B6)와 일회성 세금(A8 ①)을 반영하니 v2 재계산 밴드가 정상(폭 1.3~2.9배)
# 체크포인트가 실적 발표일인 루트 배열(EPS 공시일은 몇 주 뒤) — 같은 분기 공시를 거르는 45일. PANW 배열은 체크포인트가 곧 공시일이라 0일(Codex)
RELEASE_DATE_CHECKPOINTS = set()   # 루트 배열을 쓰는 종목이 없어졌다(C10)
# 체크포인트 밴드에 필요한 직전 PER 표본(거래일) — 1년 미만 표본의 밴드는 너무 좁아 뜻이 없다(C14 ①, 2026-10-04 — UBER 125일·폭 1.1배).
# 252가 아니라 240 — 달력 1년은 휴일에 따라 거래일 249~252라 252면 1~3일 차로 갈렸다(VRTX·GEV, Fable)
MIN_SAMPLE_DAYS = 240
KEEP_EMPTY = {"BA", "COF"}   # 적정주가 밴드·백테스트를 카드 결정으로 비운 종목(CARD_ITEMS BA 규칙)
# 루트 JSON의 trailing_years가 기본(2년)과 다른 종목 — GEV는 2024-04 상장이라 직전 1년 PER로 잰다
TRAILING_YEARS = {}   # GEV 1년 창은 2026-10-04 뺐다 — 상장(2024-04) 뒤 2년이 차 기본 2년 창을 쓸 수 있고, 1년 창은 최소 표본(C14 ①)을 못 채운다(Fable)


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


PRE_DIR = os.path.join(HERE, "backtest_pre")
PRE_TOL = 0.005      # 보관 파일과 DAILY가 겹치는 날 종가 차이 허용(분할 미반영은 2배 이상 차이로 걸린다)


def _pre_fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(3)


def pre_bars(t, daily):
    """DAILY 첫날 이전 보관 종가를 [date,c,c,c,c,0]로. 보관 대상이 아닌 카드(build_backtest_pre.SKIP)는 [](DAILY만).
    파일이 없거나 검사가 틀리면 종료 코드 3 — 조용히 짧은 백테스트로 돌아가지 않게(Codex 2026-10-08)."""
    import build_backtest_pre as bbp
    p = os.path.join(PRE_DIR, f"{t}.json")
    if t in bbp.SKIP:
        return []
    if not os.path.exists(p):
        _pre_fail(f"{t}: 보관 파일 {p}이 없다 — python3 v2/build_backtest_pre.py {t}")
    doc = json.load(open(p))
    closes = doc["closes"]
    ds = [c[0] for c in closes]
    if doc.get("ticker") != t or ds != sorted(set(ds)) or not all(isinstance(c[1], (int, float)) and c[1] > 0 for c in closes):
        _pre_fail(f"{t}: 보관 파일 형식 오류(종목·정렬·중복·종가)")
    d0 = daily[0][0]
    if doc["last"] < d0:
        _pre_fail(f"{t}: 보관 파일({doc['last']}까지)이 DAILY 첫날 {d0}에 못 미친다 — python3 v2/build_backtest_pre.py --yahoo {t}")
    pm = dict(map(tuple, closes))
    dm = {b[0]: b[4] for b in daily}
    lo, hi = d0, doc["last"]
    a_dates = sorted(d for d in pm if lo <= d <= hi)
    b_dates = sorted(d for d in dm if lo <= d <= hi)
    if len(b_dates) < 20 or a_dates != b_dates:
        _pre_fail(f"{t}: 보관 파일과 DAILY의 겹치는 거래일이 다르다({len(a_dates)} 대 {len(b_dates)}, 20일 미만이면 만료) — "
                  f"python3 v2/build_backtest_pre.py --yahoo {t}")
    bad = [(d, pm[d], dm[d]) for d in b_dates if abs(pm[d] - dm[d]) > PRE_TOL * dm[d]]
    if bad:
        _pre_fail(f"{t}: 보관 파일과 DAILY 종가가 {PRE_TOL:.1%} 넘게 다르다(분할 미반영?) {bad[:3]} — python3 v2/build_backtest_pre.py --yahoo {t}")
    return [[d, c, c, c, c, 0] for d, c in closes if d < d0]


def drop_stale_quarters(rows):
    """공시일 순으로 보며, 그 날짜 전에(또는 같은 날 다른 행으로) 이미 더 최근 분기가 공시된 행을 뺀다. (남은 행, 뺀 (분기, 공시일))."""
    keyed = [r for r in rows if r.get("quarter_end") and r.get("available_date")]
    best = {}
    for r in keyed:
        best[r["available_date"]] = max(best.get(r["available_date"], ""), r["quarter_end"])
    seen, latest = "", {}
    for d in sorted(best):
        latest[d] = seen          # 그 날짜 전까지 공시된 가장 최근 분기
        seen = max(seen, best[d])
    stale = [(r["quarter_end"], r["available_date"]) for r in keyed
             if r["quarter_end"] <= latest[r["available_date"]] or r["quarter_end"] < best[r["available_date"]]]
    drop = set(stale)
    return [r for r in rows if (r.get("quarter_end"), r.get("available_date")) not in drop], sorted(stale)


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
        # 늦게 실린 옛 분기 행(그 공시일에 이미 더 최근 분기가 나와 있던 행 — ADI 2022-11-22의 2020·2021 분기, 10-K 비교 열)은 빼고 넘긴다.
        # compute는 공시일 순으로만 정렬해 같은 날 행마다 체크포인트를 만들고(구간 0일 → 끝까지 '진행 중'), TTM도 파일 순서에 기댄다(2026-10-08).
        adj, stale = drop_stale_quarters(adj)
        if stale:
            print(t, "늦게 실린 옛 분기 행 제외:", stale)
        if adj != eps_rows:
            eps_path = os.path.join(work, "eps_adj.json")
            json.dump(adj, open(eps_path, "w"))
        tmp, out = os.path.join(work, "daily.json"), os.path.join(work, "backtest.json")
        # 재무가 현지 통화인 ADR(TSM 대만달러·ASML 유로)은 카드 PER과 같게 달러 가격 × 그날 환율로 현지 통화 가격을 만들어
        # 현지 통화 EPS로 나누고, 밴드 가격은 체크포인트 날 환율로 달러로 되돌린다(C10, 2026-10-04 — v2/fx.py 규칙)
        import fx
        cur = fx.CURRENCY.get(t)
        pre = pre_bars(t, daily)
        bars = [b for b in pre + daily if not bt_start or b[0] >= bt_start]
        if cur:
            bars = [[b[0]] + [round(x * fx.rate(t, b[0]), 4) for x in b[1:5]] + b[5:] for b in bars]
        json.dump({"daily": bars}, open(tmp, "w"))
        cmd = [sys.executable, os.path.join(REPO, "scripts", "compute_earnings_backtest_band.py"), t,
               "--eps", eps_path, "--daily-json", tmp, "--out", out]
        cmd += ["--min-sample-days", str(MIN_SAMPLE_DAYS), "--end-at-next-filing"]
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
        if cur:
            # 적중은 현지 통화 가격 공간에서 센다 — 달러 밴드를 체크포인트 날 환율로 고정하면 구간 안의 환율 변동(TSM 2025 2~5월
            # 약 9%)이 적중에 섞인다(Fable). 카드 JS는 days_*가 있으면 그것을 쓴다. 표시용 밴드·실현 범위는 달러.
            for cp in bt:
                r = fx.rate(t, cp["checkpoint_date"])
                end = cp.get("period_end_date") or daily[-1][0]
                lo_l, hi_l = cp["predicted_low"], cp["predicted_high"]
                loc = [b for b in bars if cp["checkpoint_date"] < b[0] <= end and b[0] >= daily[0][0]]   # 차트 안 봉만
                usd = [b for b in daily if cp["checkpoint_date"] < b[0] <= end]
                cp["days_total"] = len(loc)
                cp["days_in"] = sum(1 for b in loc if lo_l <= b[4] <= hi_l)
                cp["days_below"] = sum(1 for b in loc if b[4] < lo_l)
                cp["days_above"] = sum(1 for b in loc if b[4] > hi_l)
                cp["predicted_low"], cp["predicted_high"] = round(lo_l / r, 2), round(hi_l / r, 2)
                if usd:
                    cp["realized_price_low"] = min(b[4] for b in usd)
                    cp["realized_price_high"] = max(b[4] for b in usd)
                cp["fx_rate"] = r   # 표시 밴드를 달러로 되돌린 환율(현지 통화/달러, 체크포인트 날)
        # 차트 창: 구간 끝이 DAILY 첫날 이전인 체크포인트는 버리고, 첫날에 걸친 체크포인트의 실현 범위는 차트 안 봉으로 다시 잰다
        d0 = daily[0][0]
        bt = [cp for cp in bt if cp.get("is_open") or (cp.get("period_end_date") or daily[-1][0]) >= d0]
        for cp in bt:
            if cp["checkpoint_date"] < d0:
                end = daily[-1][0] if cp.get("is_open") else (cp.get("period_end_date") or daily[-1][0])
                inwin = [b[4] for b in daily if d0 <= b[0] <= end]
                if inwin and not cur:
                    cp["realized_price_low"], cp["realized_price_high"] = min(inwin), max(inwin)
                cp["clipped_from"] = d0
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
