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

    # 결산일 ±7일 가드
    keep_pe = bmh._period_ends
    from datetime import date
    bmh._period_ends = lambda cik: [date(2024, 3, 31), date(2024, 6, 30)]
    try:
        check("분기 중간 날짜는 결산일 근처 아님", not bmh._near_period_end("0", "2024-05-15"))
        check("결산일 ±7일 안은 통과", bmh._near_period_end("0", "2024-07-06") and bmh._near_period_end("0", "2024-03-25"))
        check("±8일은 막음", not bmh._near_period_end("0", "2024-07-08"))
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
    ("가드 문턱 넓힘", "def _near_period_end(cik, end, days=7):", "def _near_period_end(cik, end, days=60):"),
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
