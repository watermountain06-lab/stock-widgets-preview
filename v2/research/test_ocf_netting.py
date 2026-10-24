#!/usr/bin/env python3
"""E57 청산 담보금 빼기 시험 — 가짜 자료(규칙) + CBOE 실물(원문 값 고정).

    python3 v2/research/test_ocf_netting.py            # 시험
    python3 v2/research/test_ocf_netting.py --mutate   # 변이 시험
"""
import contextlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build_multiple_history as bmh  # noqa: E402

CIK = "0009999998"
OCF = "NetCashProvidedByUsedInOperatingActivities"
COL = "CollateralTest"
CFG = {"tag": COL, "company_tag": "test:Col", "sign": -1, "era_filed": "2020-10-30", "era_accn": "B-20Q3",
       "exempt_period_end_through": "2020-06-30", "confirmed_none": ["B-OK"]}


def row(start, end, val, accn, filed, form="10-Q"):
    return {"start": start, "end": end, "val": val, "accn": accn, "filed": filed, "form": form, "fy": int(end[:4]), "fp": "Q"}


def data(extra_ocf=(), extra_col=(), drop_col=()):
    ocf = [row("2019-01-01", "2019-09-30", 300, "B-20Q3", "2020-10-30"),          # 인수 전 비교 열(태그 없음) — 그대로
           row("2020-01-01", "2020-09-30", 900, "B-20Q3", "2020-10-30"),
           row("2020-01-01", "2020-06-30", 500, "B-20Q2", "2020-07-31"),          # 시대 전 공시 — 그대로
           row("2020-01-01", "2020-03-31", 200, "B-20Q1", "2020-05-01"),
           row("2020-01-01", "2020-12-31", 1100, "B-20K", "2021-02-19", "10-K"),
           row("2021-01-01", "2021-03-31", 260, "B-21Q1", "2021-04-30"),
           row("2020-01-01", "2020-03-31", 200, "B-21Q1", "2021-04-30"),          # 인수 전 기간 비교 열 — 그대로(면제)
           row("2021-01-01", "2021-06-30", 520, "B-21Q2", "2021-07-30"),
           row("2021-01-01", "2021-09-30", 780, "B-21Q3", "2021-10-29")] + list(extra_ocf)
    col = [row("2020-01-01", "2020-09-30", -400, "B-20Q3", "2020-10-30"), row("2020-01-01", "2020-12-31", -450, "B-20K", "2021-02-19", "10-K"),
           row("2021-01-01", "2021-03-31", 60, "B-21Q1", "2021-04-30"), row("2021-01-01", "2021-06-30", -100, "B-21Q2", "2021-07-30"),
           row("2021-01-01", "2021-09-30", 30, "B-21Q3", "2021-10-29")] + list(extra_col)
    col = [r for r in col if (r["start"], r["end"], r["accn"]) not in drop_col]
    return {"facts": {"us-gaap": {OCF: {"units": {"USD": ocf}}, COL: {"units": {"USD": col}}}}}


class Env:
    def __init__(self, d, strict=False):
        self.d, self.strict = d, strict

    def __enter__(self):
        self.old = (bmh._facts, bmh.OCF_NETTING.get(CIK), os.environ.get("OCF_NETTING_STRICT"))
        bmh._facts = lambda c: self.d if c == CIK else {}
        bmh.OCF_NETTING[CIK] = CFG
        if self.strict:
            os.environ["OCF_NETTING_STRICT"] = "1"
        else:
            os.environ.pop("OCF_NETTING_STRICT", None)
        return self

    def __exit__(self, *a):
        bmh._facts = self.old[0]
        bmh.OCF_NETTING.pop(CIK, None)
        if self.old[2] is None:
            os.environ.pop("OCF_NETTING_STRICT", None)
        else:
            os.environ["OCF_NETTING_STRICT"] = self.old[2]


def ytd():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rows = bmh.pick_tag(CIK, [OCF])[1]
    return {(r["start"], r["end"], r["accn"]): r["val"] for r in rows}, buf.getvalue()


def cases():
    out = []

    def check(name, cond):
        out.append((name, bool(cond)))

    with Env(data()):
        y, log = ytd()
        check("시대 안 짝 있음: 9개월 2020 = 900 − 400 = 500", y.get(("2020-01-01", "2020-09-30", "B-20Q3")) == 500)
        check("부호: Q1 2021 = 260 − (−1)×60 → 320", y.get(("2021-01-01", "2021-03-31", "B-21Q1")) == 320)
        check("인수 전 비교 열(시대 공시, 결산 2019-09) 그대로", y.get(("2019-01-01", "2019-09-30", "B-20Q3")) == 300)
        check("시대 전 공시 그대로", y.get(("2020-01-01", "2020-06-30", "B-20Q2")) == 500)
        check("결산 2020-03-31 비교 열(시대 공시)도 면제", y.get(("2020-01-01", "2020-03-31", "B-21Q1")) == 200)
        check("경고 없음", "ocf_netting" not in log)
        with contextlib.redirect_stdout(io.StringIO()):
            q = {e["end"]: e["val"] for e in bmh.quarterly_flow(bmh.pick_tag(CIK, [OCF])[1], "TEST")}
        check("분기 역산: Q3 2021 = (780+30) − (520−100) = 390", q.get("2021-09-30") == 390)
        check("분기 역산: Q4 2020 = (1100−450) − (900−400) = 150", q.get("2020-12-31") == 150)
    # 다른 영업현금흐름 후보 태그의 시대 안 행도 같은 규칙
    d = data(); d["facts"]["us-gaap"]["NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"] = {"units": {"USD": [
        row("2021-01-01", "2021-09-30", 780, "B-21Q3", "2021-10-29"), row("2021-01-01", "2022-03-31", 999, "B-ZZ", "2022-04-29")]}}
    with Env(d):
        with contextlib.redirect_stdout(io.StringIO()):
            rr = {(r["start"], r["end"], r["accn"]): r["val"] for r in bmh.pick_tag(CIK, bmh.FLOW_TAGS["ocf"])[1]}
        check("…ContinuingOperations 시대 안 짝 없는 행 제외", ("2021-01-01", "2022-03-31", "B-ZZ") not in rr)
    # 짝 없는 시대 안 행 → 제외 + 경고, 엄격 모드 오류
    with Env(data(drop_col=[("2021-01-01", "2021-06-30", "B-21Q2")])):
        y, log = ytd()
        check("짝 없음 → 그 행 제외", ("2021-01-01", "2021-06-30", "B-21Q2") not in y)
        check("짝 없음 → 경고", "짝 없는 영업현금흐름 1행 제외" in log)
        check("같은 accn의 다른 행은 그대로 조정", y.get(("2021-01-01", "2021-03-31", "B-21Q1")) == 320)
    try:
        with Env(data(drop_col=[("2021-01-01", "2021-06-30", "B-21Q2")]), strict=True):
            ytd()
        check("엄격 모드 → 멈춤", False)
    except RuntimeError:
        check("엄격 모드 → 멈춤", True)
    # confirmed_none
    with Env(data(extra_ocf=[row("2021-01-01", "2021-12-31", 1000, "B-OK", "2022-02-18", "10-K"),
                             row("2021-01-01", "2021-12-31", 999, "B-NO", "2022-03-01", "10-K")])):
        y, log = ytd()
        check("confirmed_none accn → 짝 없어도 그대로", y.get(("2021-01-01", "2021-12-31", "B-OK")) == 1000)
        check("같은 기간 다른 accn에는 전파 안 됨(제외)", ("2021-01-01", "2021-12-31", "B-NO") not in y)
    with Env(data(extra_ocf=[row("2021-01-01", "2021-12-31", 1000, "B-OK", "2022-02-18", "10-K")],
                  extra_col=[row("2021-01-01", "2021-12-31", -200, "B-OK", "2022-02-18", "10-K")])):
        y, _ = ytd()
        check("confirmed_none accn에도 짝이 있으면 조정", y.get(("2021-01-01", "2021-12-31", "B-OK")) == 800)
    # accn 짝: 같은 기간을 다른 공시가 다른 담보금 값으로
    with Env(data(extra_ocf=[row("2021-01-01", "2021-03-31", 260, "B-22Q1", "2022-04-29")],
                  extra_col=[row("2021-01-01", "2021-03-31", 90, "B-22Q1", "2022-04-29")])):
        y, _ = ytd()
        check("accn별 짝: 원 공시 320, 다음 해 비교 열 350", y.get(("2021-01-01", "2021-03-31", "B-21Q1")) == 320
              and y.get(("2021-01-01", "2021-03-31", "B-22Q1")) == 350)
    # 빌드 시작 검사: 최신 행 짝 없음 → 계산 불가로 멈춤
    os.makedirs(os.path.join(bmh.CACHE_DIR, "_test"), exist_ok=True)
    real_dir = bmh.CACHE_DIR
    try:
        import json
        import tempfile
        tmp = tempfile.mkdtemp()
        bmh.CACHE_DIR = tmp
        d = data(drop_col=[("2021-01-01", "2021-09-30", "B-21Q3")])
        json.dump(d, open(os.path.join(tmp, f"{CIK}_facts.json"), "w"))
        with Env(d):
            try:
                bmh.check_ocf_netting(CIK)
                check("최신 영업현금흐름 짝 없음 → 멈춤(PCR 계산 불가)", False)
            except RuntimeError as e:
                check("최신 영업현금흐름 짝 없음 → 멈춤(PCR 계산 불가)", "최근 영업현금흐름" in str(e))
        d2 = data(extra_ocf=[row("2021-01-01", "2021-09-30", 781, "B-X", "2021-10-29")])
        json.dump(d2, open(os.path.join(tmp, f"{CIK}_facts.json"), "w"))
        with Env(d2):
            try:
                bmh.check_ocf_netting(CIK)
                check("같은 기간·공시일 accn 둘 → 오류", False)
            except RuntimeError as e:
                check("같은 기간·공시일 accn 둘 → 오류", "accn 둘" in str(e))
        d3 = data(extra_ocf=[row("2021-01-01", "2021-09-30", 780, "B-A", "2021-11-15", "10-Q/A")])
        json.dump(d3, open(os.path.join(tmp, f"{CIK}_facts.json"), "w"))
        with Env(d3):
            try:
                bmh.check_ocf_netting(CIK)
                check("시대 안 정정 공시 → 오류", False)
            except RuntimeError as e:
                check("시대 안 정정 공시 → 오류", "form" in str(e))
    finally:
        bmh.CACHE_DIR = real_dir
    return out


def cboe_real():
    """CBOE 실물 — 원문 10-Q·10-K에서 뽑은 값(2026-10-24, e57 설계 표)."""
    out = []
    c = "0001374310"
    if not os.path.exists(os.path.join(bmh.CACHE_DIR, f"{c}_facts.json")):
        return [("CBOE 실물(캐시 없음 — 건너뜀)", True)]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        used, rows = bmh.pick_tag(c, bmh.FLOW_TAGS["ocf"])
        q = {e["end"]: round(e["val"] / 1e6, 1) for e in bmh.quarterly_flow(rows, "CBOE")}
    y = {(r["start"], r["end"]): round(r["val"] / 1e6, 1) for r in rows}
    exp_y = {("2026-01-01", "2026-03-31"): 82.0, ("2026-01-01", "2026-06-30"): 513.6, ("2025-01-01", "2025-12-31"): 1224.1,
             ("2025-01-01", "2025-09-30"): 846.3, ("2022-01-01", "2022-12-31"): 868.6, ("2021-01-01", "2021-12-31"): 663.0}
    for k, v in exp_y.items():
        out.append((f"CBOE 누계 {k[0]}~{k[1]} = {v}", y.get(k) == v))
    out.append(("CBOE 2분기 2026 단독 = 431.6", q.get("2026-06-30") == 431.6))
    out.append(("CBOE 4분기 2025 단독 = 377.8", q.get("2025-12-31") == 377.8))
    alt = [r for r in bmh.concept(c, "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations")
           if r.get("filed", "") >= bmh.OCF_NETTING[c]["era_filed"] and r["end"] > bmh.OCF_NETTING[c]["exempt_period_end_through"]]
    out.append(("CBOE 담보금 시대 안 영업현금흐름은 주 태그뿐(…ContinuingOperations 시대 안 0행)", not alt))
    out.append(("CBOE 짝 없는 행 경고 없음", "ocf_netting" not in buf.getvalue()))
    col = bmh.concept(c, bmh.OCF_NETTING[c]["tag"])
    first = min(col, key=lambda r: r["filed"]) if col else {}
    out.append(("담보금 첫 공시 = 고정 era(2020-10-30, 0001558370-20-012101)",
                first.get("filed") == bmh.OCF_NETTING[c]["era_filed"] and first.get("accn") == bmh.OCF_NETTING[c]["era_accn"]))
    out.append(("overlay 단위 USD 원 단위(Q1 2026 원 값 −1,878,000,000)",
                any(r["end"] == "2026-03-31" and r["start"] == "2026-01-01" and r["val"] == -1878000000 for r in col)))
    # 부호 앵커: 재무상태표 증거금 부채 1,618.2 → 3,443.9(+1,825.7, 2025-12-31 → 2026-03-31) — 영향(+)과 같은 방향
    effect = bmh.OCF_NETTING[c]["sign"] * -1878.0
    out.append(("부호 앵커: 영향 부호 == 증거금 부채 증가(+1,825.7) 방향", (effect > 0) == (3443.9 - 1618.2 > 0)))
    return out


def run(real=True):
    res = cases() + (cboe_real() if real else [])
    bad = [n for n, ok in res if not ok]
    for n, ok in res:
        print(("  ok  " if ok else "  FAIL") + " " + n)
    return bad


def mutate():
    orig, ok = bmh.net_ocf, True

    def flip(cik, rows):                     # 부호 뒤집기
        cfg = bmh.OCF_NETTING.get(str(cik).zfill(10))
        if cfg:
            cfg = dict(cfg, sign=-cfg["sign"]); saved = bmh.OCF_NETTING[str(cik).zfill(10)]; bmh.OCF_NETTING[str(cik).zfill(10)] = cfg
            try:
                return orig(cik, rows)
            finally:
                bmh.OCF_NETTING[str(cik).zfill(10)] = saved
        return orig(cik, rows)

    def no_accn(cik, rows):                  # accn 짝 조건 제거
        cfg = bmh.OCF_NETTING.get(str(cik).zfill(10))
        if not cfg:
            return rows
        coll = {(r.get("start"), r["end"]): r["val"] for r in bmh.concept(cik, cfg["tag"])}
        return [dict(r, val=r["val"] - cfg["sign"] * coll[(r.get("start"), r["end"])]) if (r.get("start"), r["end"]) in coll else r for r in rows]

    def pass_unmatched(cik, rows):           # 짝 없는 행 조용히 통과(중단영업 방식)
        cfg = bmh.OCF_NETTING.get(str(cik).zfill(10))
        if not cfg:
            return rows
        coll = {(r.get("start"), r["end"], r.get("accn")): r["val"] for r in bmh.concept(cik, cfg["tag"])}
        return [dict(r, val=r["val"] - cfg["sign"] * coll[k]) if (k := (r.get("start"), r["end"], r.get("accn"))) in coll else r for r in rows]

    def no_exempt(cik, rows):                # 인수 전 기간 면제 제거
        cfg = bmh.OCF_NETTING.get(str(cik).zfill(10))
        if not cfg:
            return rows
        saved = bmh.OCF_NETTING[str(cik).zfill(10)]
        bmh.OCF_NETTING[str(cik).zfill(10)] = dict(cfg, exempt_period_end_through="0000-00-00")
        try:
            return orig(cik, rows)
        finally:
            bmh.OCF_NETTING[str(cik).zfill(10)] = saved

    for name, fn in (("부호 뒤집기", flip), ("accn 짝 조건 제거", no_accn), ("짝 없는 행 통과", pass_unmatched), ("인수 전 면제 제거", no_exempt)):
        bmh.net_ocf = fn
        with contextlib.redirect_stdout(io.StringIO()):
            bad = run()
        print(f"변이 [{name}]: 실패 {len(bad)}건 {'(잡힘)' if bad else '(못 잡음!)'}")
        ok &= bool(bad)
        bmh.net_ocf = orig
    return ok


if __name__ == "__main__":
    if "--mutate" in sys.argv:
        sys.exit(0 if mutate() else 1)
    bad = run()
    print("결과:", "통과" if not bad else f"실패 {len(bad)}건")
    sys.exit(1 if bad else 0)
