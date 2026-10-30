"""안건 E63(배수 엔진 as_of가 옛 결산일 값을 최신으로 고름) 시험 — 규칙마다 기대 숫자.
  python3 v2/research/test_e63.py            # 시험
  python3 v2/research/test_e63.py --mutate   # 변이 시험
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, V2)
sys.path.insert(0, os.path.join(os.path.dirname(V2), "scripts"))
import build_multiple_history as bmh  # noqa: E402

RESULTS = []


def check(name, cond):
    RESULTS.append((name, bool(cond)))


def row(end, available, val):
    return {"end": end, "available": available, "val": val}


def run():
    RESULTS.clear()
    # as_of: 나중 공시에서 처음 나온 옛 결산일(분사 전 비교 열)은 최신 값을 덮지 않는다(GEHC)
    s = [row("2023-03-31", "2023-04-25", 9), row("2022-06-30", "2023-07-25", 17), row("2023-06-30", "2023-07-25", 10)]
    check("뒤늦은 옛 결산일은 안 고름", bmh.as_of(s, "2023-08-01") == 10)
    s2 = [row("2023-06-30", "2023-07-25", 10), row("2022-06-30", "2023-07-25", 17)]
    check("같은 공시일 동률은 결산일이 늦은 행(목록 순서 무관)", bmh.as_of(s2, "2023-08-01") == 10)
    s3 = [row("2023-03-31", "2023-04-25", 9), row("2022-09-30", "2023-10-31", 16)]
    check("옛 결산일만 새로 나와도 이전 최신 유지", bmh.as_of(s3, "2023-11-01") == 9)
    check("공개 전 행은 안 씀", bmh.as_of(s, "2023-05-01") == 9 and bmh.as_of(s, "2023-04-01") is None)
    s4 = [row("2023-03-31", "2023-04-25", 9), row("2023-03-31", "2023-06-01", 11)]
    check("같은 결산일 정정은 늦은 공개", bmh.as_of(s4, "2023-06-02") == 11 and bmh.as_of(s4, "2023-05-01") == 9)
    s5 = [row("2023-03-31", "2023-04-25", 9), row("2024-12-31", "2023-05-01", 99)]
    check("결산일 > 공개일 오태깅 행은 안 고름", bmh.as_of(s5, "2023-06-01") == 9)
    e = [{"available": "2023-04-25", "val": 1.0}, {"available": "2023-07-25", "val": 2.0}]
    check("결산일 없는 행(예전 EPS 형식)은 공개 순서", bmh.as_of(e, "2023-08-01") == 2.0)
    n = [{"end": "2023-06-30", "available": "2023-07-25", "val": 5, "pref": 1}]
    check("as_of_entry는 행 자체(메타데이터 유지)", bmh.as_of_entry(n, "2023-08-01") is n[0])
    nv = [row("2023-03-31", "2023-04-25", 9), row("2023-06-30", "2023-07-25", None)]
    check("값이 None인 최신 행도 건너뛰지 않음(보류 표시 유지)", bmh.as_of_entry(nv, "2023-08-01")["end"] == "2023-06-30")

    # check_shares: 점을 고를 때도 같은 규칙(Codex 합성 예 — 정답 120M)
    keep = bmh.wa_quarters
    bmh.wa_quarters = lambda cik, t: []
    try:
        pts = [row("2026-06-30", "2026-07-20", 100e6), row("2026-06-30", "2026-08-01", 120e6), row("2026-03-31", "2026-08-01", 110e6)]
        o, _ = bmh.check_shares(pts, "0", "ZZZ")
        check("check_shares 뒤늦은 비교 열 대신 같은 결산일 정정값", bmh.as_of(o, "2026-08-02") == 120e6)
    finally:
        bmh.wa_quarters = keep

    # 연결 경로: instant_series 오태깅 선제외 — 같은 결산일의 잘못된 첫 공시 뒤 정상 공시가 살아남는다
    ent = [{"end": "2024-12-31", "filed": "2024-05-01", "val": 1.0, "form": "10-Q"},
           {"end": "2024-12-31", "filed": "2025-02-20", "val": 5.0, "form": "10-K"}]
    ser = bmh.instant_series(ent, "ZZZ", False)
    check("instant_series 오태깅 첫 공시 대신 정상 공시", [e["val"] for e in ser] == [5.0])
    # 연결 경로: component_sum이 분기 중간 날짜 행을 실제로 뺀다
    keep_c, keep_pe = bmh.concept, bmh._period_ends
    from datetime import date as _d
    facts = {"LongTermDebt": [{"end": "2024-03-31", "filed": "2024-05-01", "val": 40.0}],
             "CommercialPaper": [{"end": "2024-05-15", "filed": "2024-05-17", "val": 3.6}]}
    bmh.concept = lambda cik, tag, taxonomy="us-gaap": facts.get(tag, [])
    bmh._period_ends = lambda cik: [_d(2024, 3, 31), _d(2024, 6, 30)]
    try:
        cs = bmh.component_sum("0", ["LongTermDebt", "CommercialPaper"])
        check("component_sum 분기 중간 단독 행 제외 → 총계 40", bmh.as_of(cs, "2024-05-20") == 40.0)
    finally:
        bmh.concept, bmh._period_ends = keep_c, keep_pe
    # 결산일 목록을 기억하지 않는다 — 연구 재현처럼 자료를 바꿔 끼우면 새 결산일이 바로 보인다(Fable r2 필수)
    keep_c = bmh.concept
    try:
        bmh.concept = lambda cik, tag, taxonomy="us-gaap": [{"end": "2016-03-31"}] if tag == "Assets" else []
        a1 = bmh._near_period_end("0", "2026-06-30")
        bmh.concept = lambda cik, tag, taxonomy="us-gaap": [{"end": "2016-03-31"}, {"end": "2026-06-30"}] if tag == "Assets" else []
        check("자료가 바뀌면 결산일 목록도 바뀜(캐시 없음)", (not a1) and bmh._near_period_end("0", "2026-06-30"))
        bmh.concept = lambda cik, tag, taxonomy="us-gaap": ([{"end": "2026-06-30"}] if tag == "StockholdersEquity"
                                                           else [{"end": "2016-03-31"}] if tag == "Assets" else [])
        check("총자산에 없는 결산일도 자본 결산일로 인정", bmh._near_period_end("0", "2026-06-30"))
    finally:
        bmh.concept = keep_c
    # E65 시점 인식 합산: 구성요소가 늦게(비교 열로) 태깅돼도 먼저 공개된 구성요소 합은 그날부터 보인다
    keep_c, keep_pe = bmh.concept, bmh._period_ends
    facts = {"LongTermDebtNoncurrent": [{"end": "2025-12-31", "filed": "2026-01-29", "val": 58.0},
                                        {"end": "2025-09-30", "filed": "2025-10-30", "val": 28.0}],
             "LongTermDebtCurrent": [{"end": "2025-12-31", "filed": "2026-10-29", "val": 1.0},
                                     {"end": "2025-09-30", "filed": "2025-10-30", "val": 0.8}]}
    bmh.concept = lambda cik, tag, taxonomy="us-gaap": facts.get(tag, [])
    bmh._period_ends = lambda cik: [_d(2025, 9, 30), _d(2025, 12, 31)]
    try:
        cs = bmh.component_sum("0", ["LongTermDebtNoncurrent", "LongTermDebtCurrent"])
        check("E65 10-K 날부터 12-31 부분 합(58)", bmh.as_of(cs, "2026-02-01") == 58.0)
        check("E65 늦은 구성요소 공개 뒤 완전한 합(59)", bmh.as_of(cs, "2026-11-01") == 59.0)
        check("E65 결산일별 마지막 행 = 예전 값(합 59·최대 공시일)", {e["end"]: e for e in cs}["2025-12-31"]["available"] == "2026-10-29")
        check("E65 10-K 전에는 9-30 값", bmh.as_of(cs, "2026-01-01") == 28.8)
    finally:
        bmh.concept, bmh._period_ends = keep_c, keep_pe
    check("newest_row 모든 행 오태깅 → None", bmh.newest_row([row("2025-01-01", "2024-05-01", 1)]) is None)

    # 결산일 ±7일 가드
    keep_pe = bmh._period_ends
    from datetime import date
    bmh._period_ends = lambda cik: [date(2024, 3, 31), date(2024, 6, 30)]
    try:
        check("분기 중간 날짜는 결산일 근처 아님", not bmh._near_period_end("0", "2024-05-15"))
        check("결산일 이전 7일 안은 통과", bmh._near_period_end("0", "2024-03-25") and bmh._near_period_end("0", "2024-06-30"))
        check("결산일 다음 날짜는 막음(도입일·분사일)", not bmh._near_period_end("0", "2024-07-01") and not bmh._near_period_end("0", "2024-04-02"))
        check("결산일 이전 8일은 막음", not bmh._near_period_end("0", "2024-06-22"))
        bmh._period_ends = lambda cik: []
        check("결산일 근거 없으면 거르지 않음", bmh._near_period_end("0", "2024-05-15"))
    finally:
        bmh._period_ends = keep_pe
    return list(RESULTS)


MUTANTS = [
    ("결산일 대신 공개 순서", "        k = (e.get(\"end\") or \"\", e[\"available\"], i)", "        k = (\"\", e[\"available\"], i)"),
    ("오태깅 필터 제거", "        if e.get(\"end\") and e[\"end\"] > e[\"available\"]:\n            continue", "        if False:\n            continue"),
    ("정정 공개일 무시", "        k = (e.get(\"end\") or \"\", e[\"available\"], i)", "        k = (e.get(\"end\") or \"\", \"\", -i)"),
    ("공개 전 행 포함", "    while i < len(series) and series[i][\"available\"] <= day:", "    while i < len(series):"),
    ("check_shares 목록 마지막", "        p = newest_row([x for x in pts if x[\"available\"] <= day])", "        p = [x for x in pts if x[\"available\"] <= day][-1]"),
    ("가드 문턱 넓힘", "def _near_period_end(cik, end, before=7, after=0):", "def _near_period_end(cik, end, before=60, after=0):"),
    ("결산일 다음 날 허용", "def _near_period_end(cik, end, before=7, after=0):", "def _near_period_end(cik, end, before=7, after=7):"),
    ("결산일 목록 캐시", "    return sorted(ends)", "    return globals().setdefault(\"_PE_MEMO\", {}).setdefault(cik, sorted(ends))"),
    ("자본 결산일 무시", "    for tag in (\"Assets\", \"StockholdersEquity\",", "    for tag in (\"Assets\","),
    ("instant_series 선제외 제거", "    rows = [e for e in entries if \"end\" in e and \"filed\" in e and \"start\" not in e and e[\"end\"] <= e[\"filed\"]]", "    rows = [e for e in entries if \"end\" in e and \"filed\" in e and \"start\" not in e]"),
    ("component_sum 가드 미적용", "        rows = [e for e in rows if _near_period_end(cik, e[\"end\"])]", "        rows = rows"),
    ("E65 시점 합산 제거(마지막 행만)", "            out.append({\"end\": k, \"val\": acc, \"available\": f})", "            pass\n        out.append({\"end\": k, \"val\": acc, \"available\": f})"),
    ("근거 없을 때 막음", "        return True                      # 결산일 근거가 없으면 거르지 않는다", "        return False"),
]


def mutate():
    global bmh
    path = os.path.join(V2, "build_multiple_history.py")
    src0 = open(path).read()
    caught = 0
    for name, a, b in MUTANTS:
        assert src0.count(a) >= 1, f"변이 자리 없음: {name}"
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader("build_multiple_history", loader=None))
        mod.__file__ = path
        exec(compile(src0.replace(a, b, 1), path, "exec"), mod.__dict__)
        keep, bmh = bmh, mod
        try:
            red = [n for n, ok in run() if not ok]
        except Exception as ex:
            red = [f"예외 {type(ex).__name__}"]
        bmh = keep
        caught += bool(red)
        print(("잡음 " if red else "놓침 ") + name + (f" — {red[0]}" if red else ""))
    print(f"변이 {caught}/{len(MUTANTS)} 잡음")
    return caught == len(MUTANTS)


if __name__ == "__main__":
    if "--mutate" in sys.argv:
        sys.exit(0 if mutate() else 1)
    res = run()
    for n, ok in res:
        if not ok:
            print("실패", n)
    print(f"{sum(ok for _, ok in res)}/{len(res)} 통과")
    sys.exit(0 if all(ok for _, ok in res) else 1)
