#!/usr/bin/env python3
"""E55 fact_fixes 시험 — 가짜 companyfacts로 엔진 경로(pick_tag → quarterly_flow)까지 통과시킨다.

    python3 v2/research/test_fact_fixes.py            # 시험
    python3 v2/research/test_fact_fixes.py --mutate   # 변이 시험: 장치를 일부러 망가뜨린 판마다 시험이 실패하는지
"""
import contextlib
import copy
import io
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build_multiple_history as bmh  # noqa: E402

CIK = "0009999999"
REV = "RevenueFromContractWithCustomerExcludingAssessedTax"
OP = "OperatingIncomeLoss"


def row(start, end, val, accn, filed, form="10-Q", frame=None):
    r = {"start": start, "end": end, "val": val, "accn": accn, "filed": filed, "form": form,
         "fy": int(end[:4]), "fp": "FY" if form == "10-K" else "Q"}
    if frame:
        r["frame"] = frame
    return r


def facts():
    """가짜 회사: 달력 분기. 2025 Q1~Q3 10-Q(누계 포함), FY2025 10-K는 매출 연간 값을 4분기 기간으로 단 오류(LHX형)."""
    q = [("2025-01-01", "2025-03-31", 100, "A-25Q1", "2025-04-30"), ("2025-04-01", "2025-06-30", 110, "A-25Q2", "2025-07-30"),
         ("2025-07-01", "2025-09-30", 120, "A-25Q3", "2025-10-30")]
    rev = [row(s, e, v, a, f) for s, e, v, a, f in q]
    rev += [row("2025-01-01", "2025-06-30", 210, "A-25Q2", "2025-07-30"), row("2025-01-01", "2025-09-30", 330, "A-25Q3", "2025-10-30")]
    rev += [row("2024-01-01", "2024-12-31", 400, "A-24K", "2025-02-10", "10-K")]
    rev += [row("2025-10-01", "2025-12-31", 460, "A-25K", "2026-02-10", "10-K", frame="CY2025Q4")]   # 연간 460을 4분기 기간으로
    rev += [row("2025-10-01", "2025-12-31", 130, "A-26K", "2027-02-10", "10-K")]   # 다음 해 10-K의 바른 4분기 비교 값 — 고치면 안 된다
    # NTAP형: 같은 10-Q·같은 날 시작일 하루 다른 중복(2026 Q1)
    rev += [row("2026-01-01", "2026-03-31", 140, "A-26Q1", "2026-04-30"), row("2026-01-02", "2026-03-31", 70, "A-26Q1", "2026-04-30")]
    op = [row("2025-01-01", "2025-09-30", 33, "A-25Q3", "2025-10-30"), row("2025-01-01", "2025-06-30", 21, "A-25Q2", "2025-07-30"),
          row("2025-01-01", "2025-03-31", 10, "A-25Q1", "2025-04-30"),
          row("2025-10-01", "2025-12-31", 46, "A-25K", "2026-02-10", "10-K", frame="CY2025Q4"),
          row("2024-01-01", "2024-12-31", 40, "A-24K", "2025-02-10", "10-K")]
    return {"facts": {"us-gaap": {REV: {"units": {"USD": rev}}, OP: {"units": {"USD": op}}}}}


FIXES = {
    CIK: [
        {"id": "T-ctx", "scope": "context", "match": {"accn": "A-25K", "start": "2025-10-01", "end": "2025-12-31"},
         "action": "set_start", "new_start": "2025-01-01",
         "expect_tags": [["us-gaap", REV, "USD", 460], ["us-gaap", OP, "USD", 46]],
         "expect": [{"series": "revenue", "quarter_end": "2025-12-31", "val": 130}, {"series": "opinc", "quarter_end": "2025-12-31", "val": 13}],
         "source": "https://www.sec.gov/Archives/edgar/data/9999999/x/"},
        {"id": "T-fact", "scope": "fact", "taxonomy": "us-gaap", "tag": REV, "unit": "USD",
         "match": {"accn": "A-26Q1", "start": "2026-01-02", "end": "2026-03-31", "val": 70}, "action": "drop",
         "expect": [{"series": "revenue", "quarter_end": "2026-03-31", "val": 140}],
         "source": "https://www.sec.gov/Archives/edgar/data/9999999/y/"},
    ]
}


class Env:
    """가짜 자료와 고침 파일을 엔진에 끼운다."""
    def __init__(self, data, fixes):
        self.data, self.fixes = data, fixes

    def __enter__(self):
        self.tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump({"_note": "test", **self.fixes}, self.tmp); self.tmp.close()
        self.old = (bmh._facts, os.environ.get("FACT_FIXES"))
        bmh._facts = lambda c: self.data if c == CIK else {}
        os.environ["FACT_FIXES"] = self.tmp.name
        bmh._FIXES_CACHE.clear()
        return self

    def __exit__(self, *a):
        bmh._facts = self.old[0]
        if self.old[1] is None:
            os.environ.pop("FACT_FIXES", None)
        else:
            os.environ["FACT_FIXES"] = self.old[1]
        bmh._FIXES_CACHE.clear()
        os.unlink(self.tmp.name)


def q(series):
    tags = {"revenue": bmh.FLOW_TAGS["revenue"], "opinc": bmh.EBITDA_TAGS["opinc"]}[series]
    with contextlib.redirect_stdout(io.StringIO()):
        return {e["end"]: e["val"] for e in bmh.quarterly_flow(bmh.pick_tag(CIK, tags)[1], "TEST")}


def validate(**kw):
    with contextlib.redirect_stdout(io.StringIO()):
        return bmh.validate_fixes(CIK, "TEST", strict=False, **kw)


def cases():
    out = []

    def check(name, cond):
        out.append((name, bool(cond)))

    data = facts()
    with Env(data, {}):
        before_rev, before_op = q("revenue"), q("opinc")
    check("고침 없음: LHX형 4분기 = 연간 값(460)", before_rev.get("2025-12-31") == 460)
    snap = copy.deepcopy(data)
    with Env(data, FIXES):
        rev, op = q("revenue"), q("opinc")
        check("context set_start → 4분기 매출 = 460 − 330 = 130", rev.get("2025-12-31") == 130)
        check("context set_start → 4분기 영업이익 = 46 − 33 = 13", op.get("2025-12-31") == 13)
        check("fact drop → 2026-03-31 분기 = 140", rev.get("2026-03-31") == 140)
        check("다른 분기 그대로", all(rev[k] == before_rev[k] for k in ("2025-03-31", "2025-06-30", "2025-09-30")))
        check("바뀐 분기 키 집합이 정확히 두 개", {k for k in set(rev) | set(before_rev) if rev.get(k) != before_rev.get(k)} == {"2025-12-31", "2026-03-31"})
        fixed = [r for r in bmh.concept(CIK, REV) if r.get("accn") == "A-25K"]
        check("set_start 행의 frame 삭제", fixed and "frame" not in fixed[0] and fixed[0]["start"] == "2025-01-01")
        check("검사 통과(문제 0)", validate() == [])
        later = [r for r in bmh.concept(CIK, REV) if r.get("accn") == "A-26K"]
        check("다른 공시의 같은 기간 행은 그대로(accn 조건)", later and later[0]["start"] == "2025-10-01" and later[0]["val"] == 130)
    check("캐시 원본 dict 불변", data == snap)
    d0 = facts()
    with Env(d0, {}):
        check("고침 없음 → concept가 원래 목록 객체를 그대로", bmh.concept(CIK, REV) is d0["facts"]["us-gaap"][REV]["units"]["USD"])
    # 일치 0개
    f0 = copy.deepcopy(FIXES); f0[CIK][1]["match"]["val"] = 71
    with Env(facts(), f0):
        p = validate()
        check("일치 0개 → 문제", any("일치하는 행 없음" in x for x in p))
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                bmh.validate_fixes(CIK, "TEST", strict=True)
            check("엄격 모드 → 멈춤", False)
        except SystemExit:
            check("엄격 모드 → 멈춤", True)
        check("accn·값 불일치 → 적용 안 됨", q("revenue").get("2026-03-31") in (70, 140) and q("revenue").get("2026-03-31") == before_rev.get("2026-03-31"))
    # expect_tags 불일치
    f1 = copy.deepcopy(FIXES); f1[CIK][0]["expect_tags"] = f1[CIK][0]["expect_tags"][:1]
    with Env(facts(), f1):
        check("context 사실 집합 ≠ expect_tags → 문제", any("expect_tags" in x for x in validate()))
    # 기간 검사·new_start 경계
    f2 = copy.deepcopy(FIXES); f2[CIK][0]["new_start"] = "2025-07-01"
    with Env(facts(), f2):
        p = validate()
        check("고친 기간이 연간 아님 → 문제", any("연간 350~380 아님" in x for x in p))
    f3 = copy.deepcopy(FIXES); f3[CIK][0]["new_start"] = "2025-01-03"
    with Env(facts(), f3):
        check("new_start 전날이 직전 연간 결산일 아님 → 문제", any("직전 연간 결산일" in x for x in validate()))
    # 같은 값 중복 일치 → 경고만, 모두 적용
    d4 = facts(); d4["facts"]["us-gaap"][REV]["units"]["USD"].append(dict(d4["facts"]["us-gaap"][REV]["units"]["USD"][-1]))
    with Env(d4, FIXES):
        check("같은 값 중복 → 문제 아님·모두 빠짐", validate() == [] and q("revenue").get("2026-03-31") == 140)
    # expect 단언이 실제 값을 본다
    f5 = copy.deepcopy(FIXES); f5[CIK][1]["expect"][0]["val"] = 141
    with Env(facts(), f5):
        check("expect 불일치 → 문제", any("기대 141" in x for x in validate()))
    # 불러오기 검사
    f6 = copy.deepcopy(FIXES); f6[CIK][1]["source"] = "https://www.sec.gov/..."
    try:
        with Env(facts(), f6):
            bmh._fact_fixes()
        check("source에 ... → 불러오기 오류", False)
    except SystemExit:
        check("source에 ... → 불러오기 오류", True)
    # 끄기
    with Env(facts(), FIXES):
        os.environ["FACT_FIXES"] = "off"; bmh._FIXES_CACHE.clear()
        check("FACT_FIXES=off → 고침 전 값", q("revenue").get("2025-12-31") == 460)
    return out


def run():
    res = cases()
    bad = [n for n, ok in res if not ok]
    for n, ok in res:
        print(("  ok  " if ok else "  FAIL") + " " + n)
    return bad


MUTANTS = {
    "accn 조건 제거": lambda f, tx, tg, u, r: (r.get("start") == f["match"]["start"] and r.get("end") == f["match"]["end"]
                                          and (f["scope"] == "context" or (f["tag"] == tg and r.get("val") == f["match"]["val"]))),
    "fact 범위에서 값 조건 제거": lambda f, tx, tg, u, r: (r.get("accn") == f["match"]["accn"] and r.get("start") == f["match"]["start"]
                                                 and r.get("end") == f["match"]["end"] and (f["scope"] == "context" or f["tag"] == tg)),
}


def mutate():
    orig_hits, orig_apply, ok = bmh._fix_hits, bmh._apply_fact_fixes, True
    for name, fn in MUTANTS.items():
        bmh._fix_hits = fn
        with contextlib.redirect_stdout(io.StringIO()):
            bad = run()
        print(f"변이 [{name}]: 실패 {len(bad)}건 {'(잡힘)' if bad else '(못 잡음!)'}")
        ok &= bool(bad)
        bmh._fix_hits = orig_hits

    def apply_in_place(cik, tag, taxonomy, unit, rows):          # 원본 dict 직접 수정
        for f in bmh._fact_fixes().get(cik, []):
            for r in rows:
                if orig_hits(f, taxonomy, tag, unit, r) and f["action"] == "set_start":
                    r["start"] = f["new_start"]
        return orig_apply(cik, tag, taxonomy, unit, rows)

    def apply_keep_frame(cik, tag, taxonomy, unit, rows):
        out = orig_apply(cik, tag, taxonomy, unit, rows)
        for r0, r in zip(rows, out):
            if "frame" in r0 and "frame" not in r:
                r["frame"] = r0["frame"]
        return out

    def apply_fact_only(cik, tag, taxonomy, unit, rows):        # context 범위를 무시
        saved = bmh._FIXES_CACHE.copy()
        for k in bmh._FIXES_CACHE:
            bmh._FIXES_CACHE[k] = {c: [f for f in fs if f["scope"] == "fact"] for c, fs in bmh._FIXES_CACHE[k].items()}
        try:
            return orig_apply(cik, tag, taxonomy, unit, rows)
        finally:
            bmh._FIXES_CACHE.update(saved)

    for name, fn in (("원본 dict 수정", apply_in_place), ("frame 남기기", apply_keep_frame), ("context 대신 fact만", apply_fact_only)):
        bmh._apply_fact_fixes = fn
        with contextlib.redirect_stdout(io.StringIO()):
            bad = run()
        print(f"변이 [{name}]: 실패 {len(bad)}건 {'(잡힘)' if bad else '(못 잡음!)'}")
        ok &= bool(bad)
        bmh._apply_fact_fixes = orig_apply
    return ok


if __name__ == "__main__":
    if "--mutate" in sys.argv:
        sys.exit(0 if mutate() else 1)
    bad = run()
    print("결과:", "통과" if not bad else f"실패 {len(bad)}건")
    sys.exit(1 if bad else 0)
