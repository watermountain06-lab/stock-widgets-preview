#!/usr/bin/env python3
"""5년 보완 관문 3절 — 평가월 말 S&P500 구성 여부(시험 구간 2021-10 ~ 2024-03)를 위키백과 두 문서로 복원한다.

자료(.sp500_wiki_20261008/, 2026-10-08 MediaWiki API parse 결과 그대로): list.json = "List of S&P 500 companies"(현재 목록·Date added),
historical.json = "Historical components of the S&P 500"(편입·편출 표, id=changes). revid와 파일 SHA-256을 결과에 적는다.

규칙(사전 등록 3절 — 불명확하면 빼고 목록을 보고):
- clear_full: Date added ≤ 2021-10-01이고 2021-10-01 이후 그 티커의 편입·편출 기록이 없다 → 시험 구간 내내 구성종목.
- clear_from: 2021-10-01 < Date added ≤ 2024-03-31이고, 변경 표에 같은 날짜·같은 티커 편입이 있으며, 그 사이 같은 티커 편출이 없다 → 편입일부터.
- clear_none: Date added > 2024-03-31이고 2021-10-01 이후 같은 티커 편출 기록이 없다 → 시험 구간에 구성종목 아님.
- 위로 정해지지 않으면 아래 "첫 기록" 규칙을 한 번 더 쓰고(ILMN — 2024-06 편출, 2026-09 재편입), 그래도 안 되면(티커 변경·법인 승계 의심,
  날짜 없음) → ambiguous: 시험 구간에서 뺀다.
- 지금 목록에 없는 패널 종목(패널 유니버스를 만든 뒤 빠진 종목)은 변경 표에서 2021-10-01 이후 그 티커의 첫 기록으로 본다:
  첫 기록이 2024-03-31 뒤 편출 → clear_full(그때까지 계속 구성종목), 첫 기록이 구간 안 편입이고 다음 기록이 2024-03-31 뒤 편출 → clear_from,
  첫 기록이 2024-03-31 뒤 편입 → clear_none, 그 밖(기록 없음 등) → ambiguous. 변경 표는 2021년 이후 모든 편입·편출을 싣는다고 가정한다.
평가 행은 member_at(ticker, 평가일)이 True일 때만 주 분석에 들어간다. 동종업 비교군·백분위 모수에는 걸지 않는다.

    python3 v2/research/gate_membership.py     # → gate_membership.json
"""
import hashlib
import json
import os
import re
from datetime import datetime
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, ".sp500_wiki_20261008")
OUT = os.path.join(HERE, "gate_membership.json")
T0, T1 = "2021-10-01", "2024-03-31"
# 합병으로 티커만 바뀐 법인 승계 — 편입일 전에도 다른 티커로 구성종목이었으므로 구간이 불명확하다(사전 등록 3절, Codex 2026-10-08).
SUCCESSION = {"WBD": "2022-04-11 DISCA(Discovery, 같은 법인)를 빼고 편입 — WarnerMedia·Discovery 합병"}
TICKER_RE = re.compile(r"^[A-Z][A-Z0-9.]*$")


class _Tables(HTMLParser):
    def __init__(self):
        super().__init__(); self.tables, self.stack, self.row, self.cell = [], [], None, None

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "table":
            self.stack.append({"id": a.get("id"), "rows": []})
        elif tag == "tr" and self.stack:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = {"t": "", "rs": int(a.get("rowspan") or 1), "cs": int(a.get("colspan") or 1)}

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self.cell is not None:
            self.row.append(self.cell); self.cell = None
        elif tag == "tr" and self.row is not None and self.stack:
            self.stack[-1]["rows"].append(self.row); self.row = None
        elif tag == "table" and self.stack:
            self.tables.append(self.stack.pop())

    def handle_data(self, x):
        if self.cell is not None:
            self.cell["t"] += x


def _clean(x):
    return re.sub(r"\[\d+\]", "", x).strip()            # 각주 표시 "[n]"를 뗀다(Fable)


def _grid(tb):
    """rowspan·colspan을 풀어 직사각형 표로."""
    out, pend = [], {}
    for row in tb["rows"]:
        r, ci, k = [], 0, 0
        while k < len(row) or ci in pend:
            if ci in pend:
                txt, left = pend[ci]; r.append(txt)
                pend[ci] = (txt, left - 1)
                if left - 1 == 0:
                    del pend[ci]
                ci += 1; continue
            c = row[k]; k += 1
            for _ in range(c["cs"]):
                r.append(_clean(c["t"]))
                if c["rs"] > 1:
                    pend[ci] = (_clean(c["t"]), c["rs"] - 1)
                ci += 1
        out.append(r)
    return out


def _table(path, tid):
    d = json.load(open(path))
    p = _Tables(); p.feed(d["parse"]["text"])
    return d["parse"]["revid"], _grid(next(t for t in p.tables if t["id"] == tid))


def _iso(s):
    s = s.strip()
    for f in ("%Y-%m-%d", "%B %d, %Y"):
        try:
            return datetime.strptime(s, f).date().isoformat()
        except ValueError:
            pass
    return None


def _first_event(ev):
    """2021-10-01 이후 기록(시간순)의 첫 기록으로 구간을 정한다. 정하지 못하면 None."""
    f1 = ev[0] if ev else None
    f2 = ev[1] if len(ev) > 1 else None
    if f1 and f1[1] == "remove" and f1[0] > T1:
        return {"status": "clear_full", "start": None}
    if f1 and f1[1] == "add" and T0 <= f1[0] <= T1 and f2 and f2[1] == "remove" and f2[0] > T1:
        return {"status": "clear_from", "start": f1[0]}
    if f1 and f1[1] == "add" and f1[0] > T1:
        return {"status": "clear_none"}
    return None


def build(extra=()):
    rev_list, cons = _table(os.path.join(SRC, "list.json"), "constituents")
    rev_hist, chg = _table(os.path.join(SRC, "historical.json"), "changes")
    hdr = cons[0]
    assert len(hdr) == 8 and all(len(r) == 8 for r in cons[1:]), "구성표 열 수가 바뀌었다"
    assert all(len(r) in (6, 7) for r in chg[2:]), "변경표 열 수가 바뀌었다"   # 2015·2016 두 행은 출처 열이 없다(6열)
    i_sym, i_add, i_cik = hdr.index("Symbol"), hdr.index("Date added"), hdr.index("CIK")
    events = []                                    # (날짜, "add"/"remove", 티커)
    for r in chg[2:]:
        dt = _iso(r[0])
        if not dt:
            raise ValueError(f"변경표 날짜를 읽지 못함: {r[0]!r}")
        r[1], r[3] = r[1].rstrip(" |"), r[3].rstrip(" |")   # 2011·2013 세 행의 티커 끝에 "|"가 붙어 있다(ALLE·JCP·ITT)
        for x in (r[1], r[3]):
            if x and not TICKER_RE.match(x):
                raise ValueError(f"변경표 티커 형식: {x!r} ({r[0]})")
        if r[1]:
            events.append((dt, "add", r[1]))
        if r[3]:
            events.append((dt, "remove", r[3]))
    out = {}
    for r in cons[1:]:
        t, added, cik = r[i_sym], _iso(r[i_add]), r[i_cik]
        if not TICKER_RE.match(t):
            raise ValueError(f"구성표 티커 형식: {t!r}")
        ev = sorted(e for e in events if e[2] == t)
        after = [e for e in ev if e[0] >= T0]
        rec = {"cik": cik, "date_added": added, "events_since_2021_10": after}
        if t in SUCCESSION:
            rec.update(status="ambiguous", note="법인 승계: " + SUCCESSION[t])
        elif not added:
            rec.update(status="ambiguous", note="Date added 없음")
        elif added <= T0 and not after:
            rec.update(status="clear_full", start=added)
        elif T0 < added <= T1:
            # 편입 전 구간 안 편출(재편입)도, 편입 뒤 시험 종료 전 편출도 없어야 한다(Codex — 뒤쪽 검사가 빠져 있었다)
            if (added, "add", t) in ev and not any(e[1] == "remove" and e[0] <= T1 for e in after):
                rec.update(status="clear_from", start=added)
            else:
                rec.update(status="ambiguous", note="편입일이 변경 표와 맞지 않거나 구간 안 재편입")
        elif added > T1 and not any(e[1] == "remove" for e in after):
            rec.update(status="clear_none")
        else:
            fe = _first_event(after)
            rec.update(dict(fe, note="Date added로는 불명확, 변경 표 첫 기록으로 확정") if fe else
                       {"status": "ambiguous", "note": "구간 안 편출·재편입 또는 Date added와 변경 표 불일치"})
        out[t] = rec
    for t in extra:
        t = t.replace("-", ".")
        if t in out:
            continue
        ev = [e for e in sorted(e for e in events if e[2] == t) if e[0] >= T0]
        prior = [e for e in sorted(e for e in events if e[2] == t) if e[0] < T0]
        rec = {"cik": None, "date_added": None, "events_since_2021_10": ev, "not_in_current_list": True,
               "last_event_before_2021_10": prior[-1] if prior else None}
        if t in SUCCESSION:
            rec.update(status="ambiguous", note="법인 승계: " + SUCCESSION[t])
        else:
            rec.update(_first_event(ev) or {"status": "ambiguous", "note": "지금 목록에 없고 변경 표로 구간을 확정하지 못함"})
        out[t] = rec
    sha = {f: hashlib.sha256(open(os.path.join(SRC, f), "rb").read()).hexdigest() for f in ("list.json", "historical.json")}
    meta = {"revid_list": rev_list, "revid_historical": rev_hist, "sha256": sha, "window": [T0, T1],
            "counts": {s: sum(1 for x in out.values() if x["status"] == s) for s in ("clear_full", "clear_from", "clear_none", "ambiguous")}}
    json.dump({"meta": meta, "tickers": out}, open(OUT, "w"), ensure_ascii=False, indent=1)
    return meta, out


def member_at(rec, day):
    # 티커 표기: 패널은 BRK.B처럼 점 표기를 쓴다. 하이픈 표기가 오면 호출 쪽에서 점으로 바꿔 찾는다.
    """평가일에 구성종목이었나. ambiguous·없음은 None(주 분석에서 뺀다)."""
    if not rec:
        return None
    s = rec["status"]
    if s == "clear_full":
        return True
    if s == "clear_from":
        return day >= rec["start"]
    if s == "clear_none":
        return False
    return None


def panel_tickers():
    """verdict_replay 패널 유니버스(비금융, 제외 종목 뺌) — 지금 목록에 없는 종목도 판정하려고."""
    import sys
    sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
    import valuation_judges_test as v
    return sorted(r["ticker"] for r in json.load(open(v.SP500)) if r.get("sector") != "Financials" and r["ticker"] not in v.EXCLUDE)


if __name__ == "__main__":
    meta, out = build(panel_tickers())
    print(json.dumps(meta["counts"], ensure_ascii=False), meta["revid_list"], meta["revid_historical"])
    for t, r in sorted(out.items()):
        if r["status"] != "clear_full":
            print(t, r["status"], r.get("date_added"), r.get("note", ""), [e[:2] for e in r["events_since_2021_10"]])
