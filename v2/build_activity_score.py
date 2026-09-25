#!/usr/bin/env python3
"""기본적 분석 탭의 활동성 칸 — 매출채권·재고에 현금이 묶이는 기간과 그 색.

무엇을 재나
-----------
    DSO = 365 × 평균 매출채권 ÷ TTM 매출
    DIO = 365 × 평균 재고     ÷ TTM 매출원가
    DPO = 365 × 평균 매입채무 ÷ TTM 매출원가   (매입액 대신 매출원가를 쓴 근사)
    O   = DSO + DIO                            (영업순환주기)
    CCC = O − DPO

평균 잔액은 TTM 창의 분기별 (기초+기말)/2를 다시 평균한다 —
(X[t-4] + 2X[t-3] + 2X[t-2] + 2X[t-1] + X[t]) / 8. 기초·기말 두 점만 쓰면 한 분기
말 급등에 크게 흔들린다. NVDA Q2 FY27은 매출채권이 $40.7B → $63.1B로 뛰어서
기말잔액 DSO 76.0일 / 두 점 평균 54.7일 / 다섯 점 평균 47.6일이었다.

재고는 원가로 장부에 잡히므로 DIO의 분모는 매출원가다. 매출로 나누면 마진이
오를 때 DIO가 기계적으로 눌린다(NVDA 매출총이익률 63.8% → 74.7%에서 약 30%).

색 — 자기 5년 이력 대비 위치
---------------------------
색은 **O로만** 정한다. DPO는 빼는데, 지급을 늦추면 CCC가 줄어 초록을 얻는
구멍이 생기기 때문이다. CCC는 보여주되 색을 붙이지 않는다.

    점수 = 100 × (직전 20분기 중 O가 지금보다 길었던 수 + 동률 × 0.5) ÷ 20

카드 공통 문턱 30/70을 쓴다(초록 70↑ · 노랑 30~70 · 빨강 30↓). 뜻은 "자기
과거보다 현금이 짧게/길게 묶여 있다"이지 "펀더멘털이 좋다/나쁘다"가 아니다.
재고가 는 게 양산 준비인지 적체인지는 색이 모른다.

점수 숫자는 카드에 싣지 않는다. 이웃 TTM 창은 네 분기 중 세 분기가 겹쳐 20개
값의 1차 자기상관이 0.87이고, 독립 관측은 2~4개 수준이다. 5점 단위 숫자는
가짜 정밀도라서 카드는 "이보다 길었던 적 n번 · 범위"로 적는다.

이 방법이 흔들리는지 (2026-09-23 Fable 검증)
    잔액 방식 4 × 분모 2 × 창 12/20/40분기 = 24개 변형에서 NVDA는 빨강 18 ·
    노랑 6 · 초록 0. 노랑 6개는 전부 매출 분모(부적절)였다.

한계
    - 사업이 그대로여도 5년 전 분기가 창에서 빠지면 색이 바뀐다. 인수로 재고가
      계단식으로 는 회사는 약 2년 빨강이다가 저절로 초록으로 흘러간다.
    - 5년 이력 자체가 비정상이면(코로나, 2021-22 공급망) 초록은 "부풀었던
      과거보다 낫다"에 불과하다.
    - 다른 종목으로 넓힐 때는 태그를 종목마다 점검한다. 금융채권을 가진
      회사(CAT·DE·F·GM)와 비거래 채권이 큰 회사(AAPL)는 DSO 뜻이 다르다.
      태그가 없으면 0으로 채우지 말고 N/A.

사용법
------
    python3 v2/build_activity_score.py NVDA            # SEC에서 받아 카드에 넣는다
    python3 v2/build_activity_score.py NVDA --dry-run
    python3 v2/build_activity_score.py NVDA --facts companyfacts.json
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CIKS = {"NVDA": "0001045810", "AAPL": "0000320193", "GOOGL": "0001652044", "MSFT": "0000789019", "AMZN": "0001018724", "TSM": "0001046179", "SPCX": "0001181412"}
UA = "stock-widgets research gptjhss@gmail.com"

# 앞에 있는 태그가 우선한다. 같은 분기에 둘 다 있으면 뒤 태그는 버린다.
TAGS = {
    "revenue": ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax"],
    "cogs": ["CostOfRevenue", "CostOfGoodsAndServicesSold"],
    "ar": ["AccountsReceivableNetCurrent"],
    "inventory": ["InventoryNet"],
    "ap": ["AccountsPayableCurrent"],
}
HISTORY = 20            # 비교할 직전 분기 수 (5년)
GREEN, RED = 70, 30     # 카드 공통 문턱

BEGIN, END = "/* ACTIVITY:BEGIN */", "/* ACTIVITY:END */"


def load_facts(ticker, path=None):
    if path:
        return json.load(open(path))
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{CIKS[ticker]}.json"
    raw = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, check=True).stdout
    return json.loads(raw)


def _days(a, b):
    return (dt.date.fromisoformat(b) - dt.date.fromisoformat(a)).days


def _by_filed(gaap, tag):
    """한 태그의 관측을 공시일 순으로. 같은 날짜의 값은 뒤(정정)가 이긴다.

    SEC는 이전 공시의 값을 다음 보고서에서 고쳐 싣는다. NVDA 2021-01-31
    매입채무는 $1.201B였다가 2022-03-18 공시에서 $1.149B로 정정됐다. 잔액은
    처음 값, 매출은 정정 값을 쓰면 한 비율 안에 두 세대가 섞인다.
    """
    return sorted(gaap.get(tag, {}).get("units", {}).get("USD", []), key=lambda u: u.get("filed", ""))


def quarterly_flow(gaap, tags):
    """분기 흐름값. 4분기는 연간 − 앞 세 분기로 만든다."""
    out = {}
    for tag in tags:
        seen = {}
        for u in _by_filed(gaap, tag):      # 정정 공시가 뒤에 와서 덮어쓴다
            if "start" in u:
                seen.setdefault(u["end"], {})[_days(u["start"], u["end"])] = u["val"]
        for end, by_len in seen.items():
            if end in out:
                continue
            q = [n for n in by_len if 80 <= n <= 100]
            if q:
                out[end] = by_len[q[0]]
        for end in sorted(seen):
            if end in out:
                continue
            fy = [n for n in seen[end] if 350 <= n <= 380]
            prev = [k for k in sorted(out) if k < end][-3:]
            # 앞 세 분기가 같은 회계연도 안이어야 한다 (1분기 말 → 4분기 말 273~280일)
            if fy and len(prev) == 3 and _days(prev[0], end) < 300:
                out[end] = seen[end][fy[0]] - sum(out[k] for k in prev)
    return out


def instant(gaap, tags):
    out = {}
    for tag in tags:
        mine = {}
        for u in _by_filed(gaap, tag):      # 태그 안에서는 가장 늦게 공시된 값
            if "start" not in u:
                mine[u["end"]] = u["val"]
        for end, val in mine.items():       # 태그 사이에서는 앞 태그가 우선
            out.setdefault(end, val)
    return out


def series(facts):
    gaap = facts["facts"]["us-gaap"]
    rev, cogs = quarterly_flow(gaap, TAGS["revenue"]), quarterly_flow(gaap, TAGS["cogs"])
    ar, inv, ap = (instant(gaap, TAGS[k]) for k in ("ar", "inventory", "ap"))
    qs = [e for e in sorted(rev) if all(e in d for d in (cogs, ar, inv, ap))]

    def avg(x, i):
        k = qs[i - 4:i + 1]
        return (x[k[0]] + 2 * x[k[1]] + 2 * x[k[2]] + 2 * x[k[3]] + x[k[4]]) / 8

    rows = []
    for i in range(4, len(qs)):
        if _days(qs[i - 4], qs[i]) > 400:       # 분기가 비어 있으면 TTM이 아니다
            continue
        r = sum(rev[k] for k in qs[i - 3:i + 1])
        c = sum(cogs[k] for k in qs[i - 3:i + 1])
        dso, dio, dpo = 365 * avg(ar, i) / r, 365 * avg(inv, i) / c, 365 * avg(ap, i) / c
        rows.append({"end": qs[i], "dso": dso, "dio": dio, "dpo": dpo,
                     "op": dso + dio, "ccc": dso + dio - dpo})
    return rows


def rank(values, cur):
    """직전 HISTORY개 중 지금보다 긴 수와 점수(짧을수록 높음)."""
    longer = sum(v > cur for v in values)
    ties = sum(v == cur for v in values)
    return longer, 100 * (longer + 0.5 * ties) / len(values)


def build(ticker, facts):
    rows = series(facts)
    if len(rows) < HISTORY + 1:
        return {"ticker": ticker, "status": "N/A", "reason": "5년 비교 이력 부족"}
    cur, prev, hist = rows[-1], rows[-2], rows[-HISTORY - 1:-1]
    # 최신 매출 분기보다 한참 뒤처진 값은 싣지 않는다. GOOGL은 재고를 2023-12~2025-09에
    # 따로 공시하지 않아 네 항목이 다 있는 마지막 분기가 2023-09였고, 3년 전 값이 그대로
    # 카드에 나왔다(2026-09-24).
    gaap = facts["facts"]["us-gaap"]
    latest_rev = max(quarterly_flow(gaap, TAGS["revenue"]))
    if _days(cur["end"], latest_rev) > 200:
        after = [e for e in quarterly_flow(gaap, TAGS["revenue"]) if e > cur["end"]]
        why = {"ar": "매출채권", "inventory": "재고", "ap": "매입채무", "cogs": "매출원가"}
        have = {k: instant(gaap, TAGS[k]) for k in ("ar", "inventory", "ap")}
        have["cogs"] = quarterly_flow(gaap, TAGS["cogs"])
        missing = [why[k] for k in ("ar", "inventory", "ap", "cogs") if any(e not in have[k] for e in after)]
        return {"ticker": ticker, "status": "stale", "asOf": cur["end"],
                "reason": f"{'·'.join(missing) or '일부 항목'} 공시가 끊긴 분기가 있어"
                          f" 최근 4분기를 계산할 수 없다(마지막 계산 가능 {cur['end']})"}
    longer, score = rank([h["op"] for h in hist], cur["op"])
    tone = "green" if score >= GREEN else ("red" if score <= RED else "yellow")
    r1 = lambda v: round(v, 1)
    return {
        "ticker": ticker, "status": "ok", "asOf": cur["end"], "prevAsOf": prev["end"],
        "now": {k: r1(cur[k]) for k in ("dso", "dio", "dpo", "op", "ccc")},
        "prev": {k: r1(prev[k]) for k in ("dso", "dio", "dpo", "op", "ccc")},
        "history": {"n": HISTORY, "from": hist[0]["end"], "to": hist[-1]["end"],
                    "min": r1(min(h["op"] for h in hist)), "max": r1(max(h["op"] for h in hist)),
                    "longer": longer,
                    "dsoLonger": rank([h["dso"] for h in hist], cur["dso"])[0],
                    "dioLonger": rank([h["dio"] for h in hist], cur["dio"])[0]},
        "score": score, "tone": tone,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--facts", help="SEC companyfacts JSON (생략하면 받아온다)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    t = args.ticker.upper()

    res = build(t, load_facts(t, args.facts))
    print(json.dumps(res, ensure_ascii=False, indent=1))
    if args.dry_run:
        return
    json.dump(res, open(os.path.join(HERE, f"{t}_activity.json"), "w"), ensure_ascii=False, indent=1)

    path = os.path.join(HERE, f"{t}_full_widget.html")
    html = open(path, encoding="utf-8").read()
    pat = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    if len(pat.findall(html)) != 1:
        sys.exit(f"{path}: ACTIVITY 마커가 정확히 한 쌍이 아니다")
    block = f"{BEGIN}\nconst {t}_ACTIVITY = {json.dumps(res, ensure_ascii=False)};\n{END}"
    open(path, "w", encoding="utf-8").write(pat.sub(lambda _: block, html))
    print("교체:", path)


if __name__ == "__main__":
    main()
