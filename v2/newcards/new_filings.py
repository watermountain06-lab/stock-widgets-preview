#!/usr/bin/env python3
"""카드 재무보다 새 분기 보고서(10-Q·10-K·20-F)가 SEC에 나온 카드를 찾는다 — 토요일 점검(2026-10-06 사용자 결정).

새 보고서는 자동으로 카드에 넣지 않는다(문장이 지난 분기 내용으로 쓰여 있고, 분기 갱신은 pipeline_checks.md의
점검을 거친다). 여기서는 "확인 대기" 목록만 만든다. 카드 재무 기준일 = {T}_FUNDAMENTAL.asOf(분기 말).

    python3 v2/newcards/new_filings.py            # 103장
    python3 v2/newcards/new_filings.py NVDA KO
출력: 한 줄에 한 카드("T: 10-Q 2026-09-30 기간 · 2026-10-28 접수 > 카드 2026-07-26"), 마지막 줄에 JSON {"pending": [...], "unchecked": [...]}.
6-K(ASML·TSM 분기 보고)와 한국 공시(SKHY)는 이 점검 밖이다.
"""
import importlib.util
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
sys.path.insert(0, os.path.join(REPO, "scripts"))
import fetch_eps_history as feh   # noqa: E402

UA = "kim research gptjhss@gmail.com"
FORMS = ("10-Q", "10-K", "20-F", "10-Q/A", "10-K/A", "20-F/A")
EXTRA_CIK = {"BRKB": "0001067983"}   # 손 카드(cfg 없음)
OUTSIDE = {"SKHY": "한국 공시(KIND)", "ASML": "6-K 분기 보고", "TSM": "6-K 분기 보고"}


def cik_of(T):
    p = os.path.join(HERE, "cfg", f"cfg_{T.lower()}.py")
    if os.path.exists(p):
        spec = importlib.util.spec_from_file_location("cfg", p)
        C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
        return C.CIK
    return feh.CIKS.get(T) or EXTRA_CIK.get(T)


def card_asof(T):
    """카드 재무의 (분기 말, 그 보고서 접수일)."""
    h = open(os.path.join(V2, f"{T}_full_widget.html"), encoding="utf-8").read()
    k = f"const {T}_FUNDAMENTAL = "
    if k not in h:
        return None, None
    d = json.JSONDecoder().raw_decode(h, h.index(k) + len(k))[0]
    return d.get("asOf"), d.get("filedAt")


def main():
    tickers = [a.upper() for a in sys.argv[1:]] or sorted(f.split("_")[0] for f in os.listdir(V2) if f.endswith("_full_widget.html"))
    pending, unchecked = [], []
    for T in tickers:
        if T in OUTSIDE:
            continue
        cik, (asof, filed) = cik_of(T), card_asof(T)
        if not cik or not asof:
            print(f"{T}: 점검 못 함(CIK {cik} · 카드 재무 기준일 {asof})")
            unchecked.append(T)
            continue
        try:
            req = urllib.request.Request(f"https://data.sec.gov/submissions/CIK{str(cik).zfill(10)}.json", headers={"User-Agent": UA})
            r = json.loads(urllib.request.urlopen(req, timeout=30).read())["filings"]["recent"]
        except Exception as e:
            print(f"{T}: SEC 조회 실패 {type(e).__name__}")
            unchecked.append(T)
            continue
        time.sleep(0.15)   # SEC 초당 10회 한도
        # 더 새 분기의 보고서, 또는 카드 분기의 정정 보고서(카드가 쓴 보고서보다 뒤에 접수, Codex)
        new = [(f, rd, fd) for f, rd, fd in zip(r["form"], r["reportDate"], r["filingDate"])
               if f in FORMS and rd and (rd > asof or (rd == asof and f.endswith("/A") and filed and fd > str(filed)[:10]))]
        if new:
            f, rd, fd = max(new, key=lambda x: x[1])
            print(f"{T}: {f} {rd} 기간 · {fd} 접수 > 카드 {asof}")
            pending.append({"ticker": T, "form": f, "period": rd, "filed": fd, "cardAsOf": asof})
    print(json.dumps({"pending": pending, "unchecked": unchecked}, ensure_ascii=False))


if __name__ == "__main__":
    main()
