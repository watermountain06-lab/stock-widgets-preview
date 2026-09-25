"""TSMC 분기·연간 연결재무제표(6-K 첨부 HTML, 대만 IFRS) 파서.

SEC companyfacts에는 TSM의 FY2025 20-F가 2건만 들어가 있고 분기 XBRL이 없다(2026-09-25 확인).
대신 매 분기 6-K에 감사인 검토를 받은 연결재무제표가 HTML로 붙는다. 표 구조가 일정하다 —
행 = 라벨 + (금액, %) 쌍(재무상태표·손익), 현금흐름표는 금액만. 단위는 천 대만달러.

이 모듈은 한 보고서에서 세 표(재무상태표 · 포괄손익계산서 · 현금흐름표)의 **당기 열**만
라벨 → 금액(대만달러, 천 단위를 원 단위로 환산) 사전으로 꺼낸다. 태그 매핑과 환율은 tsm_ifrs.py.
"""
import html
import re

HEADS = {
    "bs": "CONSOLIDATED BALANCE SHEETS",
    "is": "CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME",
    "eq": "CONSOLIDATED STATEMENTS OF CHANGES IN EQUITY",
    "cf": "CONSOLIDATED STATEMENTS OF CASH FLOWS",
    "notes": "NOTES TO CONSOLIDATED FINANCIAL STATEMENTS",
}
NUM = re.compile(r"^\(?-?\$?\s*[\d,]+(?:\.\d+)?\)?$")


def _cells(tr):
    out = []
    for td in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S):
        s = html.unescape(re.sub(r"<[^>]+>", "", td)).replace("\xa0", " ").strip()
        if s and s != "$":
            out.append(s)
    return out


def _num(s):
    s = s.replace("$", "").replace(",", "").strip()
    if s in ("-", "—", "–"):
        return 0.0
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()").strip()
    v = float(s)
    return -v if neg else v


def _is_num(s):
    return s in ("-", "—", "–") or bool(NUM.match(s.replace(" ", "")))


def _region(t, key, nxt):
    a = t.find(HEADS[key])
    if a < 0:
        return ""
    b = t.find(HEADS[nxt], a + 1)
    return t[a:b if b > 0 else a + 400000]


def rows(region):
    """(구역, 라벨, [숫자...]) 목록. 구역은 바로 앞의 숫자 없는 머리 행(예: "Acquisitions of:",
    "CURRENT ASSETS") — 같은 라벨이 두 번 나오는 표(현금흐름표의 유형자산 취득·처분,
    재무상태표의 유동·비유동 금융자산)를 가르는 데 쓴다."""
    out, section = [], ""
    for tr in re.findall(r"<tr[^>]*>.*?</tr>", region, re.S):
        c = _cells(tr)
        if not c or _is_num(c[0]):
            continue
        label = re.sub(r"\s*\(Notes? [^)]*\)", "", c[0]).strip()
        vals = [x for x in c[1:] if _is_num(x)]
        if not vals:
            if not re.fullmatch(r"(Amount|%|\(.*\)|[A-Z][a-z]+ \d+, \d{4}.*)", label):
                section = label
            continue
        out.append((section, label, [_num(v) for v in vals]))
    return out


def current(vals, ncols, pct=True):
    """행의 숫자에서 당기 열(첫 금액)을 꺼낸다. % 열이 끼어 있으면 금액은 짝수 자리다."""
    if pct and len(vals) == 2 * ncols:
        return vals[0]
    if len(vals) == ncols or not pct:
        return vals[0]
    return vals[0]


def parse(path):
    t = open(path, encoding="utf-8", errors="ignore").read()
    return {
        "bs": rows(_region(t, "bs", "is")),
        "is": rows(_region(t, "is", "eq")),
        "cf": rows(_region(t, "cf", "notes")),
    }
