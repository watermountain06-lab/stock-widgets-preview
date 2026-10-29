"""보통주 자본(안건 E44, 설계 shares_equity_design.md r8 §2) 시험 — 가짜 사실 자료로 규칙마다 기대 숫자를 본다.
  python3 v2/research/test_common_equity.py            # 시험
  python3 v2/research/test_common_equity.py --mutate   # 변이 시험
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, V2)
sys.path.insert(0, os.path.join(os.path.dirname(V2), "scripts"))
import build_multiple_history as bmh  # noqa: E402
import common_equity as ce  # noqa: E402

CIK, T = "0000000001", "ZZZ"
RESULTS = []


def facts(**tags):
    """{태그: [(결산일, 값, 공시일)]} → _instants 대체."""
    rows = {k: [{"end": e, "val": v, "filed": f} for e, v, f in xs] for k, xs in tags.items()}
    return lambda cik, tag: rows.get(tag, [])


def eq(*xs):
    return [{"end": e, "val": v, "available": a} for e, v, a in xs]


def run_ce(fx, equity, cik=CIK):
    ce._instants = fx
    ce.warnings.clear()
    bmh.ASOF_REF = None
    return ce.ce_series(cik, T, equity)


def check(name, cond):
    RESULTS.append((name, bool(cond)))


def vals(out):
    return [x["val"] for x in out]


def run():
    RESULTS.clear()
    E1 = eq(("2025-12-31", 1000.0, "2026-02-10"))
    SE = "StockholdersEquity"
    TOT = "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"
    # 우선주 장부가 차감 — 0보다 큰 첫 태그 하나(합산 안 함)
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")], "PreferredStockValue": [("2025-12-31", 100.0, "2026-02-10")],
                        "PreferredStockLiquidationPreferenceValue": [("2025-12-31", 150.0, "2026-02-10")]}), E1)
    check("우선주 장부가 차감(첫 태그만, 합산 안 함)", vals(o) == [900.0])
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")], "PreferredStockValue": [("2025-12-31", 0.0, "2026-02-10")],
                        "PreferredStockLiquidationPreferenceValue": [("2025-12-31", 150.0, "2026-02-10")]}), E1)
    check("장부 태그 0 → 다음 태그(청산가) + 경고", vals(o) == [850.0] and any("청산가" in w for w in ce.warnings))
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")],
                        "ConvertiblePreferredStockNonredeemableOrRedeemableIssuerOptionValue": [("2025-12-31", 30.0, "2026-02-10")]}), E1)
    check("전환우선주 태그(GOOGL형)", vals(o) == [970.0])
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")], "PreferredStockValue": [("2025-12-31", 100.0, "2026-02-10")]}),
               E1, cik="0001101239")
    check("CE_PREF_OVERRIDE [](EQIX) → 차감 안 함", vals(o) == [1000.0])
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-03-01")], "PreferredStockValue": [("2025-12-31", 100.0, "2026-03-01")]}),
               eq(("2025-12-31", 1000.0, "2026-02-10")))
    check("공시일이 뒤인 우선주 값은 안 씀(filed ≤ 관측일)", vals(o) == [1000.0])
    # 비지배지분 포함 총계 되돌림
    o = run_ce(facts(**{TOT: [("2025-12-31", 1000.0, "2026-02-10")], "MinorityInterest": [("2025-12-31", 80.0, "2026-02-10")]}), E1)
    check("총계 → 같은 결산일 비지배지분 빼기", vals(o) == [920.0])
    o = run_ce(facts(**{TOT: [("2025-12-31", 1000.0, "2026-02-10")], "MinorityInterest": [("2025-06-30", 80.0, "2025-08-01")]}), E1)
    check("비지배지분이 같은 날 없고 400일 안 보고 있음 → 이어 씀(SO형)", vals(o) == [920.0] and any("이어 씀" in w for w in ce.warnings))
    o = run_ce(facts(**{TOT: [("2025-12-31", 1000.0, "2026-02-10")], "MinorityInterest": [("2018-06-30", 9.0, "2018-08-01")]}), E1)
    check("마지막 비지배지분 보고가 400일보다 오래됨 → 0(AVGO·V·SYK형)", vals(o) == [1000.0])
    o = run_ce(facts(**{TOT: [("2025-12-31", 1000.0, "2026-02-10")]}), E1)
    check("비지배지분 보고가 한 번도 없음 → 0", vals(o) == [1000.0])
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")], TOT: [("2025-12-31", 1080.0, "2026-02-10")]}), E1)
    check("지배주주 자본 값이면 되돌리지 않음", vals(o) == [1000.0])
    # P가 그 결산일에 없을 때(§2.2)
    pv = [("2025-06-30", 100.0, "2025-08-01")]
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")], "PreferredStockValue": pv}), E1)
    check("400일 안 → 직전 값 이어 씀 + 경고", vals(o) == [900.0] and any("이어 씀" in w for w in ce.warnings))
    old = [("2023-06-30", 100.0, "2023-08-01")]
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")], "PreferredStockValue": old,
                        "PreferredStockSharesOutstanding": [("2025-12-31", 5.0, "2026-02-10")]}), E1)
    check("400일 넘음 + 주식 수 > 0 → None(기권)", vals(o) == [None])
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")], "PreferredStockValue": old}), E1)
    check("400일 넘음 + 주식 수 증거 없음 → 상환으로 보고 0(MRK형)", vals(o) == [1000.0])
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")]}), E1)
    check("우선주가 한 번도 없음 → 0", vals(o) == [1000.0])
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")], "PreferredStockValue": pv,
                        "PreferredStockSharesOutstanding": [("2025-12-31", 0.0, "2026-02-10")]}), E1)
    check("그 결산일 주식 수 0 → 상환 증거 → 0", vals(o) == [1000.0])
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")], "PreferredStockValue": [("2025-03-31", 100.0, "2025-05-01")],
                        "PreferredStockSharesOutstanding": [("2025-09-30", 0.0, "2025-11-01")]}), E1)
    check("사이에 상환 증거 → 옛 값 되살아나지 않음", vals(o) == [1000.0])
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")], "PreferredStockValue": [("2025-12-31", 0.0, "2026-02-10")]}), E1)
    check("액면 0만(MET형) → 상환 증거 아님, 우선주 없음이면 0", vals(o) == [1000.0])
    o = run_ce(facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")], "PreferredStockValue": pv + [("2025-12-31", 0.0, "2026-02-10")]}), E1)
    check("액면 0 태그가 있어도 직전 양수 이어 씀(MET형)", vals(o) == [900.0])
    # 음수 CE는 지금 엔진 처리 그대로(값만 넘김)
    o = run_ce(facts(**{SE: [("2025-12-31", 50.0, "2026-02-10")], "PreferredStockValue": [("2025-12-31", 100.0, "2026-02-10")]}),
               eq(("2025-12-31", 50.0, "2026-02-10")))
    check("우선주를 빼서 CE ≤ 0이어도 값은 그대로 넘김", vals(o) == [-50.0])
    # 연구 모드
    ce._instants = facts(**{SE: [("2025-12-31", 1000.0, "2026-02-10")], "PreferredStockValue": [("2025-12-31", 100.0, "2026-02-10")]})
    bmh.ASOF_REF = "2026-12-01"
    o = ce.ce_series(CIK, T, E1)
    bmh.ASOF_REF = None
    check("연구 모드(ASOF_REF) → equity 그대로", vals(o) == [1000.0])
    return RESULTS


MUTANTS = [
    ("합산(첫 태그 대신)", "            if v is not None and v > 0:\n                return v, tg\n        return None",
     "            pass\n        tot = sum(max(_val_at(rows, end, avail) or 0, 0) for tg, rows in self.tags)\n        return (tot, self.tags[0][0]) if tot > 0 else None"),
    ("400일 기권 주식 수 증거 무시", "            if any((_val_at(rows, end, avail) or 0) > 0 for rows in self.share_rows):", "            if True:"),
    ("400일 기권 규칙 제거", "        if _days(end, e1) > CARRY_DAYS:", "        if False:"),
    ("액면 0을 상환으로 봄", "            if v is not None and v == 0:\n                return True", "            if v is not None and v == 0:\n                return True\n        for tg, rows in self.tags:\n            if _val_at(rows, end, avail) == 0:\n                return True"),
    ("비지배지분 400일 이어 쓰기 제거(늘 0)", "                    if recent:", "                    if False:"),
    ("비지배지분 없으면 늘 기권", "                        n = 0", "                        out.append(dict(e, val=None, pref=None))\n                        continue"),
    ("비지배지분 이어 쓰기 400일 창 제거", " and _days(end, r[\"end\"]) <= CARRY_DAYS],", "],"),
    ("되돌림 제거", "                v = tv - n", "                pass"),
    ("상환 뒤 되살아남", "        if any(self.redeemed(m, avail) for m in mids) or \\", "        if False and any(self.redeemed(m, avail) for m in mids) or \\"),
    ("EQIX 덮어쓰기 무시", "        tags = CE_PREF_OVERRIDE.get(cik, CE_PREF_TAGS)", "        tags = CE_PREF_TAGS"),
    ("연구 모드 스위치 제거", "    if bmh.ASOF_REF is not None or not equity:", "    if not equity:"),
    ("공시일 검사 제거", "    c = [r for r in rows if r[\"end\"] == end and r[\"filed\"] <= avail]", "    c = [r for r in rows if r[\"end\"] == end]"),
]


def mutate():
    global ce
    src0 = open(os.path.join(V2, "common_equity.py")).read()
    caught = 0
    for name, a, b in MUTANTS:
        assert src0.count(a) >= 1, f"변이 자리 없음: {name}"
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader("common_equity", loader=None))
        mod.__file__ = os.path.join(V2, "common_equity.py")
        exec(compile(src0.replace(a, b, 1), mod.__file__, "exec"), mod.__dict__)
        keep, ce = ce, mod
        try:
            red = [n for n, ok in run() if not ok]
        except Exception as ex:
            red = [f"예외 {type(ex).__name__}"]
        ce = keep
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
            print("실패:", n)
    print(f"{sum(ok for _, ok in res)}/{len(res)} 통과")
    sys.exit(0 if all(ok for _, ok in res) else 1)
