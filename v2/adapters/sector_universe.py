#!/usr/bin/env python3
"""표본이 모자란 섹터의 동종업 비교군을 S&P500 구성종목으로 넓힌다(2026-09-27 사용자 결정, LLY).

사이트 비교 유니버스(site_data/valuation_base, 카드 종목 약 70개)에 헬스케어는 7종목뿐이라
배수마다 동종업이 2~6곳이어서 `build_peer_score.MIN_PEERS`(8)를 못 넘었다. 여기서는
S&P500의 같은 GICS 섹터 종목(stock-widgets-redesign/scripts/sp500.json) 전체에 대해
**카드와 같은 엔진**(build_multiple_history)으로 기준일의 다섯 배수를 계산해 파일 하나로 남긴다.
build_peer_score는 SECTOR_UNIVERSE에 적힌 섹터만 이 파일을 비교군으로 쓴다(다른 섹터는 그대로).

    python3 v2/adapters/sector_universe.py "Health Care" --asof 2026-09-25

- 가격: Yahoo 일봉(1년), 기준일 종가까지. 분할 기록도 같은 요청에서 받는다.
- EPS: scripts/fetch_eps_history.py(카드와 같은 SEC 희석 EPS). 분할 손 목록이 없으므로
  EPS 이력이 멈췄거나(마지막 분기가 기준일보다 200일 넘게 앞섬) 보정하지 못한 분할이 400일 안에 있으면 그 종목의 PER은 뺀다(2026-10-04 — 예전 400일 분할 가드를 바꿈).
- 배수 정의·적자 처리(음수면 "negative")·분모 결측은 카드와 같다. 점수에서는 음수 PCR만 동종업 꼴찌로 세고 음수 EV/EBITDA·PBR은
  build_peer_score가 비교에서 뺀다(C11, 2026-10-04 — PBR 음수는 self_multiples가 이미 뺀다). PER은 A3(순이익률 2% 미만·적자 → 해당 없음)라
  self_multiples가 빼고, 뺀 종목은 파일의 perNA에 남긴다(C9, 2026-10-04 — 동종 종목에도 A3).
- 생존자 표본(현재 구성종목)이다. 기준일 하나의 횡단면이라 과거 백분위와는 무관하다.
- SEC 요청은 종목마다 쉬어 간다(429 방지). 이미 받은 companyfacts는 .sec_cache를 쓴다.
"""
import argparse
import contextlib
import io
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
sys.path.insert(0, V2)
sys.path.insert(0, os.path.join(REPO, "scripts"))
import build_multiple_history as bmh  # noqa: E402
import build_peer_score as ps  # noqa: E402
import fetch_eps_history as feh  # noqa: E402

SP500 = os.path.join(V2, "vendor", "sp500.json")   # redesign/scripts에서 복사(v2/vendor/README.md)
OUT_DIR = os.path.join(V2, "peer_universe")
UA = "Mozilla/5.0"   # 긴 브라우저 UA는 Yahoo가 429로 막았다(2026-09-27)


def sp500_rows():
    d = json.load(open(SP500))
    rows = d if isinstance(d, list) else d.get("tickers", d)
    return list(rows.values()) if isinstance(rows, dict) else rows


def yahoo(ticker, asof):
    sym = ticker.replace(".", "-")
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1y&interval=1d&events=split"
    # urllib는 Yahoo가 429로 막는다 — curl로 받는다(reference_stock_widgets_yahoo_kr_ticker).
    raw = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, text=True, timeout=60).stdout
    r = json.loads(raw)["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    bars = []
    for i, ts in enumerate(r["timestamp"]):
        day = time.strftime("%Y-%m-%d", time.gmtime(ts + r.get("gmtoffset", 0)))
        if day > asof or q["close"][i] is None or not q["volume"][i]:
            continue
        bars.append([day, q["open"][i], q["high"][i], q["low"][i], q["close"][i], q["volume"][i]])
    # 분할만 센다 — Yahoo는 스핀오프 가격 조정계수도 splits로 준다(SPGI 2026-07-01 1057:1000, Fable).
    # 비율이 1.5 이상(또는 0.67 이하)인 것만 분할로 본다.
    splits = sorted(time.strftime("%Y-%m-%d", time.gmtime(s["date"]))
                    for s in (r.get("events", {}).get("splits") or {}).values()
                    if s.get("denominator") and not (0.67 < s["numerator"] / s["denominator"] < 1.5))
    return bars, splits


def split_history(ticker):
    """최근 5년 주식분할(날짜, 비율) — EPS 이력의 분할 보정용(C12, 2026-10-04). 1y 일봉 요청의 분할만으로는 그보다 오래된 분할을
    못 보고, 분할 뒤 연간 EPS − 분할 전 분기 EPS로 4분기를 역산하다 크게 틀렸다(ORLY 2025-06 15:1 → 2025년 4분기 −8.01).
    Yahoo는 스핀오프 가격 조정도 splits로 주므로(DD 2025-11 2.39 — Qnity 분사) 분모 4 이하 분수(2:1·3:2·4:3·5:4·1:5 등)에 가까운
    것만 분할로 본다. 비율 모양만으로 분사를 완전히 가를 수는 없다(Codex) — 걸러진 값은 출력으로 남겨 손으로 본다."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker.replace('.', '-')}?range=5y&interval=3mo&events=split"
    raw = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, text=True, timeout=60).stdout
    r = json.loads(raw)["chart"]["result"][0]
    out = []
    for s in (r.get("events", {}).get("splits") or {}).values():
        if not s.get("denominator"):
            continue
        k = s["numerator"] / s["denominator"]
        big = k if k >= 1 else 1 / k
        day = time.strftime("%Y-%m-%d", time.gmtime(s["date"]))
        if big >= 1.25 and any(abs(big * q - round(big * q)) < 0.005 for q in (1, 2, 3, 4)):   # 0.02면 FTV 1.327(Ralliant 분사)을 4:3으로 받았다(Fable)
            out.append((day, round(k, 6)))
        elif big >= 1.25:
            print(f"  {ticker}: Yahoo 분할 {day} 비율 {k:.4f}는 단순 분수가 아니라 분사 조정으로 보고 뺐다 — 확인 필요", file=sys.stderr)
    return sorted(out)


# 희석 EPS를 주식 종류별(차원)로만 태그하는 종목 — EPS를 받기 전에 원문 XBRL에서 상장 종류 값을 오버레이에 채운다(D66, 2026-10-05).
# 오버레이(.sec_cache)는 저장소 밖이라, 이 단계가 없으면 새로 받을 때 다시 "EPS 이력 멈춤"으로 빠진다(Fable).
CLASS_EPS = {"HSY": "us-gaap:CommonStockMember", "CVNA": "us-gaap:CommonClassAMember", "KKR": "us-gaap:CommonStockMember"}   # KKR: D29(2026-10-05)


# 희석 EPS 태그에 빈 기간이 있어 기본 EPS로 메워도 되는 종목 — 겹치는 분기마다 기본 = 희석을 확인했다.
# LEN: 2024-12~2026-08 분기·누계 행에서 기본과 희석이 모두 같고, FY2025 10-K 연간(7.98)은 기본 EPS 태그에만 있다(2026-10-04).
BASIC_EPS_OK = {"LEN"}


def one(ticker, cik, asof, eps_dir):
    bars, splits = yahoo(ticker, asof)
    if not bars or bars[-1][0] != asof:
        return None, f"기준일 종가 없음({bars[-1][0] if bars else '—'})", None
    eps_path = os.path.join(eps_dir, f"{ticker}_eps_history.json")
    sh = split_history(ticker)
    # 5년 안에 분할이 있으면 캐시가 있어도 다시 받는다 — 보정 전에 받은 파일이 그대로 통과하지 않게(Codex, 2026-10-04)
    # 토요일 비교군 갱신이면 기준표 밖 회사(카드 아닌 비교 종목)의 EPS도 새로 받는다 — 재무(_facts)와 같은 날짜로(2026-10-08)
    fresh = bool(os.environ.get("SEC_REFRESH_UNLISTED")) and str(cik).zfill(10) not in bmh._approved()
    if not os.path.exists(eps_path) or sh or os.environ.get("REFETCH_EPS") or fresh:
        if ticker in CLASS_EPS:
            since = f"{int(asof[:4]) - 2}{asof[4:]}"
            subprocess.run([sys.executable, os.path.join(HERE, "ixbrl_class_eps.py"), cik, CLASS_EPS[ticker], since],
                           capture_output=True, text=True)
        r = subprocess.run([sys.executable, os.path.join(REPO, "scripts", "fetch_eps_history.py"), ticker,
                        "--cik", cik, "--out", eps_path, "--splits", ",".join(f"{d}:{k}" for d, k in sh),
                        # 희석 EPS가 없는 기간은 계속사업 희석 EPS로 — MNST·KIM·WEC·GD는 몇 년째 그 태그로만 공시한다(D66, 2026-10-04)
                        # 기본 = 희석을 확인한 종목만 빈 기간을 기본 EPS로(BASIC_EPS_OK — LEN FY2025 연간은 기본 EPS 태그에만 있다, Fable·Codex 2026-10-04)
                        "--tag", "EarningsPerShareDiluted,IncomeLossFromContinuingOperationsPerDilutedShare" + (",EarningsPerShareBasic" if ticker in BASIC_EPS_OK else "")],
                       capture_output=True, text=True)
        if r.returncode and fresh:   # 토요일 갱신에서 EPS 받기 실패 — 옛 파일로 계산하고 보고에 남긴다(Codex 2026-10-08)
            with open(os.path.join(bmh.CACHE_DIR, "_refresh_failed.txt"), "a") as f:
                f.write(f"{str(cik).zfill(10)} eps {ticker}\n")
        time.sleep(0.6)
    feh.CIKS[ticker] = cik
    orig = bmh.load_daily
    bmh.load_daily = lambda t, path=None: bars
    out = os.path.join(eps_dir, f"{ticker}_multiples.json")
    old_argv, old_env = sys.argv, os.environ.get("EPS_HISTORY")
    try:
        sys.argv = ["x", ticker, "--json", out]
        os.environ["EPS_HISTORY"] = eps_path if os.path.exists(eps_path) else ""
        with contextlib.redirect_stdout(io.StringIO()):
            bmh.main()
    finally:
        bmh.load_daily, sys.argv = orig, old_argv
        if old_env is None:
            os.environ.pop("EPS_HISTORY", None)
        else:
            os.environ["EPS_HISTORY"] = old_env
    m = ps.self_multiples(out)      # 카드 본인 값과 같은 규칙(음수 → negative, 결측 → 제외, PER 해당 없음 → 제외)
    pna = json.load(open(out)).get("perNA")
    # 예전에는 기준일 전 400일 안에 분할이 있으면 PER을 뺐다. EPS를 5년 분할 기록으로 보정하게 되어(C12) 그 가드를 두 조건으로 바꿨다
    # (2026-10-04): ① EPS 이력이 멈춤 — 마지막 분기가 기준일보다 200일 넘게 앞서면(MNST 2011·CVNA 2024 — 태그 문제),
    # ② 1y 일봉의 분할 가운데 EPS 보정에 쓰지 못한 것(단순 분수가 아니라 걸러진 분할 비율)이 400일 안에 있으면.
    note = None
    rows = json.load(open(eps_path)) if os.path.exists(eps_path) else []
    last_q = max((r["quarter_end"] for r in rows if r.get("quarter_end")), default=None)
    days = lambda a_, b_: (time.mktime(time.strptime(a_, "%Y-%m-%d")) - time.mktime(time.strptime(b_, "%Y-%m-%d"))) / 86400
    used = {d for d, _ in sh}
    unfixed = [s for s in splits if 0 <= days(asof, s) <= 400 and not any(abs(days(s, d)) <= 5 for d in used)]
    if "per" in m and (last_q is None or days(asof, last_q) > 200):
        m.pop("per")
        note = f"EPS 이력 멈춤(마지막 분기 {last_q}) — PER 제외"
    elif "per" in m and unfixed:
        m.pop("per")
        note = f"보정하지 못한 분할 {unfixed[-1]} — PER 제외"
    elif "per" not in m and not pna and m:
        # PER만 조용히 비던 경우(D29 — KKR·ARES): 이력이 없으면 사유를 남긴다(Codex 2026-10-05)
        note = ("EPS 이력 없음(희석 EPS 표준 태그를 못 찾음) — PER 제외" if not rows
                else f"PER 계산 불가(마지막 분기 {last_q}, 4분기 합이 0 이하이거나 없음) — PER 제외")
    return m, note, pna


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sector")
    ap.add_argument("--asof", required=True)
    # 섹터 안의 하위 업종만(쉼표 구분) — V: 결제 + 거래소·데이터(2026-09-27 사용자 결정)
    ap.add_argument("--sub", help='예: "Transaction & Payment Processing Services,Financial Exchanges & Data"')
    ap.add_argument("--name", help="파일 이름(기본: 섹터 이름)")
    a = ap.parse_args()
    subs = [x.strip() for x in a.sub.split(",")] if a.sub else None
    rows = [r for r in sp500_rows() if r.get("sector") == a.sector and (not subs or r.get("subIndustry") in subs)]
    slug = a.name or a.sector.lower().replace(" ", "_")
    eps_dir = os.path.join(OUT_DIR, slug)
    os.makedirs(eps_dir, exist_ok=True)
    res = {"sector": a.sector, "subIndustries": subs, "asOf": a.asof, "source": "S&P500 현재 구성종목(sp500.json) · 카드와 같은 엔진",
           "tickers": {}, "skipped": {}}
    for r in rows:
        t = (r.get("ticker") or r.get("symbol")).replace("-", ".")
        cik = str(r.get("cik")).zfill(10)
        try:
            m, note, pna = one(t, cik, a.asof, eps_dir)
        except Exception as e:  # 한 종목 실패가 전체를 멈추지 않게
            m, note, pna = None, f"오류: {type(e).__name__}: {e}", None
        if m is None:
            res["skipped"][t] = note
        else:
            res["tickers"][t] = m
            if pna:   # A3 동종 종목(C9) — PER을 뺀 근거
                res.setdefault("perNA", {"rule": "기준일 최근 4분기 GAAP 순이익률 < 2% 또는 적자면 PER 비교에서 뺀다(A3·C9)", "tickers": {}})["tickers"][t] = pna
            if note:
                res["skipped"][t] = note
        print(t, "→", m if m is not None else note, flush=True)
        time.sleep(0.4)
    path = os.path.join(OUT_DIR, f"{slug}.json")
    json.dump(res, open(path, "w"), ensure_ascii=False, indent=1)
    print("저장:", path, len(res["tickers"]), "종목")


if __name__ == "__main__":
    main()
