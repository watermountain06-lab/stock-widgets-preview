#!/usr/bin/env python3
"""E36·D61 시험 — 가짜 companyfacts로 vendor/fetch_financials.build_result(최신 분기 태그 고르기)와
build_fundamental_score.interest_coverage_item(순이자 표기·부호)을 확인한다(research/e36_d61_design.md §3).

    python3 v2/research/test_e36_d61.py            # 시험
    python3 v2/research/test_e36_d61.py --mutate   # 변이 시험: 규칙을 일부러 망가뜨린 판마다 시험이 실패하는지
"""
import contextlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "vendor"))
import fetch_financials as ff  # noqa: E402
import build_fundamental_score as bfs  # noqa: E402

CIK = "0009999999"
A, B, C = "InterestExpense", "InterestExpenseNonoperating", "InterestExpenseDebt"


def r(start, end, val, filed, form="10-Q", accn="0000000000-00-000001"):
    return {"start": start, "end": end, "val": val, "filed": filed, "form": form, "accn": accn,
            "fy": int(end[:4]), "fp": "FY" if form == "10-K" else "Q"}


def facts(**tags):
    return {t: {"units": {"USD": rows}} for t, rows in tags.items()}


# A: 연간 이력 있음, 3개월은 2024-06에서 멈춤. B: 3개월이 2026-06까지, 2024년 겹침.
A_ROWS = [r("2022-01-01", "2022-12-31", 400, "2023-02-01", "10-K"), r("2023-01-01", "2023-12-31", 410, "2024-02-01", "10-K"),
          r("2024-01-01", "2024-03-31", 100, "2024-05-01"), r("2024-04-01", "2024-06-30", 101, "2024-08-01")]
B_SAME = [r("2024-01-01", "2024-03-31", 100, "2024-05-01"), r("2024-04-01", "2024-06-30", 101, "2024-08-01"),
          r("2026-04-01", "2026-06-30", 120, "2026-08-01")]


def interest(fx, cik=CIK):
    tags = ff.CONCEPTS_BY_CIK.get(cik, {}).get("interestExpense", ff.CONCEPTS["interestExpense"])
    res = ff.extract_concept(fx, tags)
    return ff.refine_latest_quarter(fx, tags, res, "interestExpense") if "interestExpense" not in ff.LATEST_Q_BY_CIK.get(cik, {}) else res


CASES = []


def case(fn):
    CASES.append(fn)
    return fn


@case
def switch_when_two_overlaps_match():
    res = interest(facts(**{A: A_ROWS, B: B_SAME}))
    assert res["latestQuarter"]["end"] == "2026-06-30" and res["latestQuarterTag"] == B, res
    assert res["tag"] == A and res["annual"]   # 연간은 A 그대로


@case
def warn_when_one_overlap():
    b = [B_SAME[1], B_SAME[2]]
    res = interest(facts(**{A: A_ROWS, B: b}))
    assert res["latestQuarter"]["end"] == "2024-06-30" and "warnings" in res, res


@case
def warn_when_any_overlap_over_2pct():
    b = [B_SAME[0], dict(B_SAME[1], val=110), B_SAME[2]]   # 101 대 110 = 8.2%
    res = interest(facts(**{A: A_ROWS, B: b}))
    assert res["latestQuarter"]["end"] == "2024-06-30" and "warnings" in res, res


@case
def boundary_exactly_2pct_passes():
    a = A_ROWS[:3] + [dict(A_ROWS[3], val=98)]
    b = [B_SAME[0], dict(B_SAME[1], val=100), B_SAME[2]]   # |B−A| = 2 = 0.02 × 100 정확히
    res = interest(facts(**{A: a, B: b}))
    assert res.get("latestQuarterTag") == B, res


@case
def zero_only_overlap_does_not_switch():
    a = A_ROWS[:2] + [dict(A_ROWS[2], val=0), dict(A_ROWS[3], val=0)]
    b = [dict(B_SAME[0], val=0), dict(B_SAME[1], val=0), B_SAME[2]]
    res = interest(facts(**{A: a, B: b}))
    assert "latestQuarterTag" not in res and "warnings" in res, res


@case
def ytd_only_candidate_warns():
    b = B_SAME[:2] + [r("2026-01-01", "2026-06-30", 240, "2026-08-01")]   # 최신이 6개월 누계뿐
    res = interest(facts(**{A: A_ROWS, B: b}))
    assert res["latestQuarter"]["end"] == "2024-06-30" and any("ytd_only" in w for w in res.get("warnings", [])), res


@case
def next_candidate_after_failure():
    bad = [B_SAME[0], dict(B_SAME[1], val=150), r("2026-07-01", "2026-09-30", 130, "2026-11-01")]   # 더 새롭지만 정의 다름
    res = interest(facts(**{A: A_ROWS, B: bad, C: B_SAME}))
    assert res.get("latestQuarterTag") == C and res["latestQuarter"]["end"] == "2026-06-30", res


@case
def restatement_latest_filed_wins():
    b = [B_SAME[0], dict(B_SAME[1], val=130, filed="2024-08-01"), dict(B_SAME[1], val=101, filed="2025-08-01", accn="x2"), B_SAME[2]]
    res = interest(facts(**{A: A_ROWS, B: b}))
    assert res.get("latestQuarterTag") == B, res


@case
def latest_q_by_cik_skips_general_rule():
    cik = next(iter(k for k, v in ff.LATEST_Q_BY_CIK.items() if "interestExpense" in v))
    res = interest(facts(**{A: A_ROWS, B: B_SAME}), cik=cik)
    assert "latestQuarterTag" not in res, res   # interest()가 일반 규칙을 건너뜀(build_result는 지정 태그로 교체)


@case
def build_result_uses_rule_only_for_scope():
    fx = facts(**{A: A_ROWS, B: B_SAME})
    out = ff.build_result(fx, CIK)
    assert out["interestExpense"].get("latestQuarterTag") == B
    assert "operatingCashFlow" not in ff.REFINE_KEYS and "capex" not in ff.REFINE_KEYS


# D61 — interest_coverage_item(op, iv, src_tag, manual, adj)
NET = "InterestIncomeExpenseNonoperatingNet"


@case
def net_cost_with_adjust():
    item, flag = bfs.interest_coverage_item(300, -100, NET, None, 50)   # b 100, c 150
    assert abs(item["value"] - 2.0) < 1e-9 and item["note"] == "순이자 기준" and flag is None, item


@case
def net_income_flips_to_cost_by_adjust():
    item, _ = bfs.interest_coverage_item(300, 20, NET, None, 50)   # b −20, c 30
    assert abs(item["value"] - 10.0) < 1e-9 and item["note"] == "순이자 기준", item


@case
def net_zero_and_income_are_missing():
    z, _ = bfs.interest_coverage_item(300, 0, NET, None, 0)
    p, _ = bfs.interest_coverage_item(300, 20, NET, None, 0)
    assert z["points"] is None and "순이자 0" in z["note"] and p["points"] is None and "순이자 수익" in p["note"], (z, p)


@case
def gross_zero_is_five_points():
    item, _ = bfs.interest_coverage_item(300, 0, A, None, 0)
    assert item["points"] == 5 and item["note"] == "이자비용 0", item


@case
def gross_negative_sign_abs_and_adjust_direction():
    dis, _ = bfs.interest_coverage_item(3624, -1812, A, None, 0)   # DIS 연간형 — 지금 코드 op/abs(iv)와 같음
    assert abs(dis["value"] - 2.0) < 1e-9 and dis["note"] == "음수 부호로 공시(절댓값)", dis
    item, _ = bfs.interest_coverage_item(300, -100, A, None, 50)   # b 100, c 150 — 방향 유지
    assert abs(item["value"] - 2.0) < 1e-9, item


@case
def gross_adjust_exceeding_cost_is_anomaly():
    item, flag = bfs.interest_coverage_item(300, 100, A, None, -150)
    assert item["points"] is None and flag == "interest_adjust_exceeds_cost", (item, flag)


@case
def manual_net_flag_and_gross_manual():
    m, _ = bfs.interest_coverage_item(729, 243, None, {"value": 243, "net": True}, 0)   # PM형 손입력 순이자(양수 = 비용 크기)
    g, _ = bfs.interest_coverage_item(856, 428, None, {"value": 428}, 0)   # RTX형 총이자 손입력
    assert abs(m["value"] - 3.0) < 1e-9 and m["note"] == "순이자 기준" and "note" not in g, (m, g)


@case
def combined_e36_switch_to_net_tag_then_d61():
    a = A_ROWS
    netb = [dict(x, val=-x["val"]) for x in B_SAME]   # 분기만 순이자 태그로 — 같은 크기, 음수 부호
    fx = facts(**{A: a, NET: netb})
    res = ff.refine_latest_quarter(fx, [A, NET], ff.extract_concept(fx, [A, NET]), "interestExpense")
    # 부호가 반대라 2% 확인에서 떨어진다 — 정의(부호 관례)가 다른 태그로는 자동으로 바꾸지 않는다
    assert "latestQuarterTag" not in res, res
    # 회사별 지정(LATEST_Q_BY_CIK)처럼 분기 태그가 순이자로 정해진 경우의 D61 판정은 분기 출처를 따른다
    item, _ = bfs.interest_coverage_item(240, -120, NET, None, 0)
    assert abs(item["value"] - 2.0) < 1e-9 and item["note"] == "순이자 기준", item


def run():
    bad = []
    for fn in CASES:
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                fn()
        except Exception as e:   # 단언 실패뿐 아니라 변이가 만든 오류도 실패로 센다
            bad.append(f"{fn.__name__}: {e}")
    return bad


MUTANTS = {
    "겹침 2개 조건 제거": ("len(common) >= 2", "len(common) >= 1"),
    "모두 → 하나라도": ("and all(abs(na[c]", "and any(abs(na[c]"),
    "0 아닌 겹침 조건 제거": ('and any(na[c]["val"] != 0 or nb[c]["val"] != 0 for c in common)', ""),
    "누계뿐 경고 제거": ('if le and (not qb or le > qb["end"]) and (not qa or le > qa["end"]):', "if False:"),
}
BFS_MUTANTS = {
    "비용 크기 변환 제거": ('b = -iv if (net and not manual) else abs(iv)', 'b = iv'),
    "순이자 0 → 5점": ('return ({"value": None, "points": None, "note": "순이자 0(이자비용 미공시)"} if net', 'return ({"value": None, "points": 5, "note": "순이자 0(이자비용 미공시)"} if net'),
}


def mutate():
    import importlib
    ok = True
    for name, (old, new) in list(MUTANTS.items()) + list(BFS_MUTANTS.items()):
        mod = ff if name in MUTANTS else bfs
        path = mod.__file__
        src = open(path).read()
        assert src.count(old) == 1, f"{name}: 원문을 못 찾음"
        try:
            open(path, "w").write(src.replace(old, new))
            importlib.reload(mod)
            fails = run()
            print(f"{'잡힘' if fails else '못 잡음'} — {name}: 실패 {len(fails)}")
            ok &= bool(fails)
        finally:
            open(path, "w").write(src)
            importlib.reload(mod)
    return ok


if __name__ == "__main__":
    if "--mutate" in sys.argv:
        sys.exit(0 if mutate() else 1)
    fails = run()
    for f in fails:
        print("실패", f)
    print(f"{len(CASES) - len(fails)}/{len(CASES)} 통과")
    sys.exit(1 if fails else 0)
