"""TSMC 연결재무제표 한 부에서 v2가 쓰는 항목을 꺼낸다(대만달러, 원 단위).

반환: {"end", "kind"(Q1/Q2/Q3/FY), "is3": 당분기 3개월, "isy": 누적(연간), "bs": 기말, "cfy": 누적}
손익표 열: 분기 보고서 = 3개월 당기·전기, 누적 당기·전기(각 금액+%). 1분기·연간 = 당기·전기 두 쌍.
EPS 행은 % 열이 없다. 현금흐름표는 누적 당기·전기 금액만.
"""
import re

from tsm_reports import parse

K = 1000.0   # 표 단위: 천 대만달러

MONTHS = {"March": 3, "June": 6, "September": 9, "December": 12}


def _find(rows, pat, section=None, nth=0):
    hits = [r for r in rows if re.fullmatch(pat, r[1], re.I)
            and (section is None or re.search(section, r[0], re.I))]
    return hits[nth] if len(hits) > nth else None


def _period(path):
    t = open(path, encoding="utf-8", errors="ignore").read(3_000_000)
    x = re.sub(r"<[^>]+>", " ", t)
    x = re.sub(r"\s+", " ", x)
    m = re.search(r"CONSOLIDATED BALANCE SHEETS.{0,300}?(March|June|September|December) (\d{1,2}), (\d{4})", x)
    mon, year = MONTHS[m.group(1)], int(m.group(3))
    annual = bool(re.search(r"Years? Ended December 31", x[:400000])) and mon == 12
    kind = "FY" if annual else {3: "Q1", 6: "Q2", 9: "Q3"}[mon]
    end = f"{year}-{mon:02d}-{ {3: 31, 6: 30, 9: 30, 12: 31}[mon] }".replace(" ", "")
    return end, kind


def extract(path):
    end, kind = _period(path)
    p = parse(path)
    IS, BS, CF = p["is"], p["bs"], p["cf"]
    miss = []

    def is_pair(pat, nth=0, eps=False):
        r = _find(IS, pat, nth=nth)
        if not r:
            miss.append("is:" + pat)
            return None, None
        v = r[2]
        if eps:                       # EPS: [3M당기, 3M전기, 누적당기, 누적전기] 또는 [당기, 전기]
            return (v[0], v[2]) if len(v) >= 4 else (v[0], v[0])
        amounts = v[0::2] if len(v) in (4, 8) else v
        cur3 = amounts[0] * K
        cury = (amounts[2] if len(amounts) >= 4 else amounts[0]) * K
        return cur3, cury

    def bs(pat, section=None, nth=0, need=True):
        r = _find(BS, pat, section, nth)
        if not r:
            if need:
                miss.append("bs:" + pat)
            return 0.0
        return r[2][0] * K

    def cf(pat, section=None, need=True):
        r = _find(CF, pat, section)
        if not r:
            if need:
                miss.append("cf:" + pat)
            return 0.0
        return r[2][0] * K

    is3, isy = {}, {}
    for key, pat in [("revenue", r"NET REVENUE"), ("cogs", r"COST OF REVENUE"),
                     ("opinc", r"INCOME FROM OPERATIONS"), ("pretax", r"INCOME BEFORE INCOME TAX"),
                     ("tax", r"INCOME TAX EXPENSE"), ("ni_total", r"NET INCOME"),
                     ("rd", r"Research and development"), ("fincost", r"Finance costs")]:
        a, b = is_pair(pat)
        is3[key], isy[key] = a, b
    a, b = is_pair(r"Shareholders of the parent")          # 첫 번째 = 순이익 귀속(두 번째는 포괄이익)
    is3["ni"], isy["ni"] = a, b
    for key, pat in [("eps_d", r"Diluted earnings per share"), ("eps_b", r"Basic earnings per share")]:
        a, b = is_pair(pat, eps=True)
        is3[key], isy[key] = a, b
    for d in (is3, isy):
        if d.get("fincost") is not None:
            d["fincost"] = abs(d["fincost"])

    cur = r"CURRENT ASSETS"
    non = r"NONCURRENT ASSETS"
    b = {
        "cash": bs(r"Cash and cash equivalents"),
        "sti": sum(bs(p, cur, need=False) for p in [
            r"Financial assets at fair value through profit or loss",
            r"Financial assets at fair value through other comprehensive income",
            r"Financial assets at amortized cost"]),
        "ar": bs(r"Notes and accounts receivable, net") + bs(r"Receivables from related parties", need=False),
        "inv": bs(r"Inventories"),
        "ca": bs(r"Total current assets"),
        "assets": bs(r"Total assets|TOTAL"),
        "cl": bs(r"Total current liabilities"),
        "liab": bs(r"Total liabilities"),
        "ap": bs(r"Accounts payable") + bs(r"Payables to related parties", need=False),
        "st_debt": bs(r"Short-term loans", need=False),
        # 라벨이 서식마다 다르다: "Current portion of bonds and long-term bank loans"(옛) /
        # "Long-term liabilities - current portion"(새). 새 라벨을 놓쳐 2026 Q2 NT$1,674억이 빠졌다(Codex).
        "ltd_cur": bs(r"Current portion of bonds.*|Long-term liabilities\s*[-–—]\s*current portion", need=False),
        "ltd_non": bs(r"Bonds payable", need=False) + bs(r"Long-term bank loans", need=False),
        # 유동 리스부채는 별도 행이 없다(기타유동부채에 포함) — 비유동만 잡힌다. 규모가 작다.
        "lease": bs(r"Lease liabilities", need=False),
        "equity": bs(r"Total equity attributable to shareholders of the parent|Equity attributable to shareholders of the parent"),
        # 비지배지분 행 라벨에 특수 하이픈(U+2011)이 쓰여 매칭이 안 된다 — 총자본 − 지배지분으로 구한다.
        "nci": 0.0,
        "lti": sum(bs(p, non, need=False) for p in [
            r"Financial assets at fair value through profit or loss",
            r"Financial assets at fair value through other comprehensive income",
            r"Financial assets at amortized cost",
            r"Investments accounted for using equity method"]),
        # 액면 NT$10 — 보통주 자본금(천 대만달러) ÷ 10 = 주식 수
        "shares": bs(r"Common stock|Capital stock|Share capital") / 10.0,
    }
    total_eq = bs(r"Total equity")
    b["nci"] = max(total_eq - b["equity"], 0.0)
    c = {
        "ocf": cf(r"Net cash generated by operating activities"),
        # 취득 행이 처분 행보다 항상 앞에 온다. 옛 서식(2020~2023)은 괄호가 따로 된 칸이라
        # 부호가 사라지므로 절댓값을 쓴다.
        "capex": abs(cf(r"Property, plant and equipment")),
        "dep": cf(r"Depreciation expense"),
        "amort": cf(r"Amortization expense", need=False),
        "div": abs(cf(r"Cash dividends", need=False)),
    }
    return {"end": end, "kind": kind, "is3": is3, "isy": isy, "bs": b, "cfy": c, "missing": miss}
