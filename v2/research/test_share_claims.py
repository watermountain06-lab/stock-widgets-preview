"""카드별 전환·교환 증권 표(설계 shares_equity_design.md r9 §3) 시험 — 가짜 종목, 규칙마다 기대 숫자.
  python3 v2/research/test_share_claims.py            # 시험
  python3 v2/research/test_share_claims.py --mutate   # 변이 시험
"""
import importlib.util
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, V2)
sys.path.insert(0, os.path.join(os.path.dirname(V2), "scripts"))
import build_multiple_history as bmh  # noqa: E402
import share_claims as sc  # noqa: E402

T = "ZZZ"
TMP = tempfile.mkdtemp(prefix="sc_test_")
RESULTS = []


def setup(items):
    p = os.path.join(TMP, "share_claims.json")
    json.dump({T: items}, open(p, "w"))
    sc.SHARE_CLAIMS = p
    bmh.ASOF_REF = None
    sc.reset()


def check(name, cond):
    RESULTS.append((name, bool(cond)))


def approx(a, b, tol=1e-6):
    return a is not None and abs(a - b) <= tol


def raises(fn, exc):
    try:
        fn()
    except exc:
        return True
    return False


def it(kind, rows, paired=None, **kw):
    return dict({"id": f"x-{kind}", "kind": kind, "rows": rows, "paired": paired or [], "source": "u"}, **kw)


def run():
    RESULTS.clear()
    D = "2026-08-15"
    obs = {"equity": "2026-06-30", "nci": "2026-06-30", "preferred": "2026-06-30", "debt": "2026-06-30", "dcf_pref": "2026-06-30"}
    # 고정 전환우선주
    setup([it("conv_pref_fixed", [{"end": "2026-06-30", "filed": "2026-08-01", "wa_shares": 10, "conv_shares": 20}],
              [{"end": "2026-06-30", "filed": "2026-08-01", "pref_ev": 5.0, "dcf_pref": 6.0, "pref_in_p": 7.0, "ce_add": 0.0}])])
    check("conv_pref_fixed: 표지 + 전환 주식", approx(sc.adjusted_shares(T, D, 50, 100, "2026-06-30"), 120))
    check("희석 가중평균 대체 날짜: WA − wa_shares + 날짜 값(110 − 10 + 20)",
          approx(sc.adjusted_shares(T, D, 50, 110, "2026-06-30", True, "2026-04-01", "2026-06-30"), 120))
    c = sc.claims(T, D, 50, obs)
    check("짝 금액: 같은 결산일 행", c["pref_ev"] == 5 and c["dcf_pref"] == 6 and c["pref_in_p"] == 7)
    check("CE 되돌림 = ce_add + pref_in_p", approx(sc.ce_extra(c), 7))
    check("filed > d인 행은 안 씀(쓸 행이 없으면 보류)", raises(lambda: sc.adjusted_shares(T, "2026-07-15", 50, 100, "2026-06-30"), sc.ClaimHold))
    # 의무전환 비율 구간
    r = {"end": "2026-06-30", "filed": "2026-08-01", "wa_shares": 0, "pref_shares": 10, "liq_per_share": 1000,
         "min_rate": 2.0, "max_rate": 2.5, "initial_price": 400, "threshold_price": 500}
    setup([it("conv_pref_mandatory", [r], [{"end": "2026-06-30", "filed": "2026-08-01", "pref_ev": 0, "dcf_pref": 0, "pref_in_p": 0}])])
    check("의무전환: 가격 < Initial → 최대 비율", approx(sc.adjusted_shares(T, D, 300, 0, "2026-06-30"), 25))
    check("의무전환: Initial~Threshold → 청산가 ÷ 가격", approx(sc.adjusted_shares(T, D, 450, 0, "2026-06-30"), 10 * 1000 / 450))
    check("의무전환: 가격 > Threshold → 최소 비율", approx(sc.adjusted_shares(T, D, 600, 0, "2026-06-30"), 20))
    # 전환사채
    setup([it("conv_debt_net", [{"end": "2026-06-30", "filed": "2026-08-01", "wa_shares": 0, "principal": 1000, "conv_price": 50}])])
    check("conv_debt_net: max(0, N × (1 − K/가격)) — 가격 100 → 10", approx(sc.adjusted_shares(T, D, 100, 0, "2026-06-30"), 10))
    check("conv_debt_net: 외가격 → 0", approx(sc.adjusted_shares(T, D, 40, 0, "2026-06-30"), 0))
    setup([it("conv_debt_full", [{"end": "2026-06-30", "filed": "2026-08-01", "wa_shares": 0, "principal": 1000, "conv_price": 50}],
              [{"end": "2026-06-30", "filed": "2026-08-01", "principal_in_debt": 990.0}])])
    check("conv_debt_full 내가격: N주 + 차입금에서 장부가 빼고 CE에 더함",
          approx(sc.adjusted_shares(T, D, 60, 0, "2026-06-30"), 20) and sc.claims(T, D, 60, obs)["principal_in_debt"] == 990
          and approx(sc.ce_extra(sc.claims(T, D, 60, obs)), 990))
    check("conv_debt_full 외가격: 주식 0·차입금 그대로", approx(sc.adjusted_shares(T, D, 40, 0, "2026-06-30"), 0)
          and sc.claims(T, D, 40, obs)["principal_in_debt"] == 0)
    # 경제적 전체 주식 수(BX)
    setup([it("econ_shares", [{"end": "2026-06-30", "filed": "2026-07-23", "wa_shares": 0, "econ_shares": 1243}],
              [{"end": "2026-06-30", "filed": "2026-08-07", "nci_remove": 0, "ce_add": 4943.0}]),
           it("conv_pref_fixed", [{"end": "2026-06-30", "filed": "2026-08-01", "wa_shares": 0, "conv_shares": 20}],
              [{"end": "2026-06-30", "filed": "2026-08-01", "pref_ev": 0, "dcf_pref": 0, "pref_in_p": 0, "ce_add": 0}], id="y")])
    check("econ_shares는 S를 대체(다른 항목 더하지 않음)", approx(sc.adjusted_shares(T, D, 50, 750, "2026-06-30"), 1243))
    check("econ_shares는 WA 대체 날짜에도 대체", approx(sc.adjusted_shares(T, D, 50, 900, "2026-06-30", True, "2026-04-01", "2026-06-30"), 1243))
    check("짝 금액은 엔진 관측 결산일로 — 10-Q(08-07) 전에는 옛 결산일 행",
          raises(lambda: sc.claims(T, "2026-07-30", 50, obs), sc.ClaimHold))
    # 같은 결산일 짝 행이 없음 → 보류, carry_paired → 이어 씀
    setup([it("exchange_units", [{"end": "2026-06-30", "filed": "2026-08-01", "wa_shares": 0, "units": 55}],
              [{"end": "2026-03-31", "filed": "2026-05-01", "nci_remove": 0, "ce_add": 700.0}])])
    check("짝 행 없음 → ClaimHold(그 종목만 보류)", raises(lambda: sc.claims(T, D, 50, obs), sc.ClaimHold))
    setup([it("exchange_units", [{"end": "2026-06-30", "filed": "2026-08-01", "wa_shares": 0, "units": 55}],
              [{"end": "2026-03-31", "filed": "2026-05-01", "nci_remove": 0, "ce_add": 700.0}], carry_paired=True)])
    check("carry_paired → 이전 행 이어 씀", sc.claims(T, D, 50, obs)["ce_add"] == 700)
    check("짝 시리즈가 엔진에 없는데 표 금액 ≠ 0 → 보류", raises(lambda: sc.claims(T, D, 50, dict(obs, equity=None)), sc.ClaimHold))
    # 기간: 전환·상환
    base_rows = [{"end": "2026-03-31", "filed": "2026-05-01", "wa_shares": 20, "conv_shares": 20}]
    base_pair = [{"end": "2026-03-31", "filed": "2026-05-01", "pref_ev": 5, "dcf_pref": 5, "pref_in_p": 5, "ce_add": 0}]
    setup([it("conv_pref_fixed", base_rows, base_pair, end_shares="2026-06-30", end_claims="2026-06-30", converted="2026-05-15")])
    check("표지 결산일 ≥ end_shares → 더하지 않음(표지가 담음)", approx(sc.adjusted_shares(T, D, 50, 100, "2026-06-30"), 100))
    check("표지 결산일 < end_shares → 더함", approx(sc.adjusted_shares(T, D, 50, 100, "2026-03-31"), 120))
    check("재무상태표 결산일 ≥ end_claims → 짝 금액 0", sc.claims(T, D, 50, obs)["pref_ev"] == 0)
    check("WA 분기 시작 ≥ converted → 더하지도 빼지도 않음",
          approx(sc.adjusted_shares(T, D, 50, 120, "2026-06-30", True, "2026-07-01", "2026-09-30"), 120))
    setup([it("conv_pref_fixed", base_rows, base_pair, redeemed="2026-06-15", redeemed_filed="2026-06-16")])
    check("현금 상환 공시 뒤 → 주식·청구권 함께 끝", approx(sc.adjusted_shares(T, D, 50, 100, "2026-03-31"), 100)
          and sc.claims(T, D, 50, dict(obs, preferred="2026-03-31", equity="2026-03-31", dcf_pref="2026-03-31"))["pref_ev"] == 0)
    setup([it("conv_pref_fixed", base_rows, base_pair, start="2026-04-01")])
    check("발행 전 날짜 → 없음", approx(sc.adjusted_shares(T, "2026-03-15", 50, 100, "2026-03-31"), 100))
    setup([it("conv_pref_fixed", base_rows, base_pair, start="2026-04-20")])
    check("발행 전 날짜(시작일 있음) → 없음", approx(sc.adjusted_shares(T, "2026-04-15", 50, 100, "2025-12-31"), 100))
    setup([it("conv_pref_fixed", base_rows, base_pair, backfill_first=True)])
    check("backfill_first → 첫 값", approx(sc.adjusted_shares(T, "2026-04-15", 50, 100, "2025-12-31"), 120))
    # 검토 1라운드 보강
    setup([it("conv_pref_fixed", base_rows, base_pair, start="2026-02-01")])
    check("발행 뒤 첫 행 공시 전 → 보류(사건 행 필요)", raises(lambda: sc.adjusted_shares(T, "2026-03-01", 50, 100, "2025-12-31"), sc.ClaimHold))
    setup([it("conv_pref_fixed", base_rows, base_pair)])
    check("시작일 없는 증권이 첫 행 전 → 보류(backfill_first 필요)", raises(lambda: sc.adjusted_shares(T, "2026-04-15", 50, 100, "2025-12-31"), sc.ClaimHold))
    rows2 = base_rows + [{"end": "2026-03-31", "filed": "2026-09-01", "wa_shares": 30, "conv_shares": 20}]
    setup([it("conv_pref_fixed", rows2, base_pair)])
    check("WA 대체: 뒤 공시의 정정 몫은 안 씀(110 − 20 + 20 = 110)",
          approx(sc.adjusted_shares(T, "2026-08-15", 50, 110, "2026-03-31", True, "2026-01-01", "2026-03-31"), 110))
    setup([it("conv_pref_fixed", base_rows, base_pair, start="2025-01-01")])
    check("WA 대체 분기 행 없음(발행 뒤) → 보류",
          raises(lambda: sc.adjusted_shares(T, D, 50, 110, "2026-06-30", True, "2026-04-01", "2026-06-30"), sc.ClaimHold))
    setup([it("conv_debt_full", [{"end": "2026-06-30", "filed": "2026-08-01", "wa_shares": 70, "principal": 0, "conv_price": 16.21,
                                  "converted_shares": 137606}], [{"end": "2026-06-30", "filed": "2026-08-01", "principal_in_debt": 0}])])
    check("전환 끝난 사채 → 실제 전환 주식(가격 무관)", approx(sc.adjusted_shares(T, D, 1, 0, "2026-06-30"), 137606))
    setup([it("conv_pref_fixed", base_rows, [{"end": "2026-03-31", "filed": "2026-05-01", "pref_ev": 9, "dcf_pref": 0, "pref_in_p": 0, "ce_add": 0}])])
    check("짝 시리즈 없는데 표 금액 ≠ 0 → 보류", raises(lambda: sc.claims(T, D, 50, dict(obs, preferred=None)), sc.ClaimHold))
    setup([it("conv_pref_fixed", base_rows, [{"end": "2026-06-30", "filed": "2026-08-01", "pref_ev": 1, "dcf_pref": 1, "pref_in_p": 1, "ce_add": 0}],
              carry_paired=True)])
    check("carry_paired인데 이전 행 없음 → 보류", raises(lambda: sc.claims(T, D, 50, dict(obs, preferred="2026-03-31")), sc.ClaimHold))
    # 검토 2라운드
    setup([it("conv_debt_full", [{"end": "2026-06-30", "filed": "2026-08-01", "wa_shares": 0, "principal": 0, "conv_price": 16.21,
                                  "converted_shares": 137606}], [{"end": "2026-03-31", "filed": "2026-05-01", "principal_in_debt": 99}])])
    check("전환 끝난 사채는 외가격이어도 이전 결산일 차입금을 뺀다", approx(sc.claims(T, D, 1, dict(obs, debt="2026-03-31"))["principal_in_debt"], 99))
    setup([it("conv_pref_fixed", base_rows, [{"end": "2025-12-31", "filed": "2026-02-01", "pref_ev": 9, "dcf_pref": 9, "pref_in_p": 0, "ce_add": 0},
                                             {"end": "2026-03-31", "filed": "2026-05-01", "pref_ev": 0, "dcf_pref": 0, "pref_in_p": 0, "ce_add": 0}])])
    check("시리즈 없음: 최신 짝 행이 0이면 과거 금액 무관하게 통과", sc.claims(T, D, 50, {"preferred": None})["pref_ev"] == 0)
    # 형식·연구 모드
    setup([it("conv_pref_fixed", [{"end": "2026-03-31", "filed": "2026-05-01", "conv_shares": 20}], base_pair)])
    check("rows에 wa_shares 없음 → 형식 오류", raises(lambda: sc.load(T), sc.ClaimError))
    setup([it("conv_pref_fixed", base_rows, base_pair)])
    bmh.ASOF_REF = "2026-12-01"
    check("연구 모드 → 표 없음", not sc.has(T) and approx(sc.adjusted_shares(T, D, 50, 100, "2026-03-31"), 100))
    bmh.ASOF_REF = None
    return RESULTS


MUTANTS = [
    ("WA 대체 날짜 wa_shares 빼기 제거", "                sub += wr[-1][\"wa_shares\"]", "                pass"),
    ("econ_shares 대체 제거", "        if it[\"kind\"] == \"econ_shares\":\n            return float(r[\"econ_shares\"])", "        if False:\n            return 0"),
    ("end_shares 검사 제거", "        elif it.get(\"end_shares\") and base_end and base_end >= it[\"end_shares\"]:", "        elif False:"),
    ("end_claims 검사 제거", "            if it.get(\"end_claims\") and e >= it[\"end_claims\"]:", "            if False:"),
    ("converted 검사 제거", "            if it.get(\"converted\") and wa_start and wa_start >= it[\"converted\"]:", "            if False:"),
    ("상환 검사 제거", "    if it.get(\"redeemed_filed\") and it[\"redeemed_filed\"] <= d:\n        return False", "    if False:\n        return False"),
    ("의무전환 구간 뒤집기", "    if price > r[\"threshold_price\"]:\n        return r[\"min_rate\"]", "    if price > r[\"threshold_price\"]:\n        return r[\"max_rate\"]"),
    ("conv_debt_net 공식 오류", "        return max(0.0, n * (1 - r[\"conv_price\"] / price))", "        return n"),
    ("conv_debt_full 외가격 제거", "    return n if price >= r[\"conv_price\"] else 0.0", "    return n"),
    ("짝 금액 결산일 무시", "            same = [p for p in it[\"paired\"] if p[\"end\"] == e and p[\"filed\"] <= d]", "            same = [p for p in it[\"paired\"] if p[\"filed\"] <= d]"),
    ("carry_paired 무시(늘 이어 씀)", "            elif it.get(\"carry_paired\"):", "            elif True:"),
    ("CE 되돌림 pref_in_p 뺌", "    return c[\"ce_add\"] + c[\"pref_in_p\"] + c[\"principal_in_debt\"]", "    return c[\"ce_add\"] + c[\"principal_in_debt\"]"),
    ("backfill_first 무시(늘 채움)", "    if it.get(\"backfill_first\") and it[\"rows\"]:", "    if it[\"rows\"]:"),
    ("연구 모드 스위치 제거", "    if _bmh().ASOF_REF is not None:\n        return None", "    if False:\n        return None"),
    ("전환 완료 차입금 예외 제거", "            if f == \"principal_in_debt\" and not _done and", "            if f == \"principal_in_debt\" and"),
    ("시리즈 없음 검사가 과거 전체를 봄", "                if _cur and (max(_cur, key=lambda p: (p[\"end\"], p[\"filed\"])).get(f) or 0) != 0 \\", "                if any((p.get(f) or 0) != 0 for p in _cur) \\"),
    ("발행 뒤 행 없음 보류 제거", "            if it.get(\"start\") and d >= it[\"start\"]:\n                raise", "            if False:\n                raise"),
    ("WA 정정 행 공시일 무시", "            wr = [x for x in it[\"rows\"] if x[\"end\"] == wa_end and x[\"filed\"] <= d]", "            wr = [x for x in it[\"rows\"] if x[\"end\"] == wa_end]"),
    ("WA 행 없음 보류 제거", "                if not (it.get(\"start\") and wa_end < it[\"start\"]):\n                    raise", "                if False:\n                    raise"),
    ("전환 주식 보존 제거", "    if r.get(\"converted_shares\") is not None and not r[\"principal\"]:", "    if False:"),
    ("짝 시리즈 없음 검사 제거", "                if _cur and (max(", "                if False and (max("),
    ("carry 이전 행 없음 보류 제거", "                    raise ClaimHold(f\"{ticker} {it['id']}: carry_paired인데", "                    continue\n                    raise ClaimHold(f\"{ticker} {it['id']}: carry_paired인데"),
    ("filed 검사 제거", "    c = [r for r in it[\"rows\"] if r[\"filed\"] <= d]", "    c = list(it[\"rows\"])"),
]


def mutate():
    global sc
    src0 = open(os.path.join(V2, "share_claims.py")).read()
    caught = 0
    for name, a, b in MUTANTS:
        assert src0.count(a) >= 1, f"변이 자리 없음: {name}"
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader("share_claims", loader=None))
        mod.__file__ = os.path.join(V2, "share_claims.py")
        exec(compile(src0.replace(a, b, 1), mod.__file__, "exec"), mod.__dict__)
        keep, sc = sc, mod
        try:
            red = [n for n, ok in run() if not ok]
        except Exception as ex:
            red = [f"예외 {type(ex).__name__}"]
        sc = keep
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
