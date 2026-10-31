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
             "LongTermDebtCurrent": [{"end": "2025-12-31", "filed": "2026-10-29", "val": 1.0}]}   # META형: 직전 9-30에는 없던 구성요소가 늦게
    bmh.concept = lambda cik, tag, taxonomy="us-gaap": facts.get(tag, [])
    bmh._period_ends = lambda cik: [_d(2025, 9, 30), _d(2025, 12, 31)]
    try:
        cs = bmh.component_sum("0", ["LongTermDebtNoncurrent", "LongTermDebtCurrent"])
        check("E65 10-K 날부터 12-31 부분 합(58)", bmh.as_of(cs, "2026-02-01") == 58.0)
        check("E65 늦은 구성요소 공개 뒤 완전한 합(59)", bmh.as_of(cs, "2026-11-01") == 59.0)
        check("E65 결산일별 마지막 행 = 예전 값(합 59·최대 공시일)", {e["end"]: e for e in cs}["2025-12-31"]["available"] == "2026-10-29")
        check("E65 10-K 전에는 9-30 값", bmh.as_of(cs, "2026-01-01") == 28.0)
        # EXC형: 직전 결산일에 있던 큰 구성요소가 늦게 오면 부분 합을 내지 않는다 → 직전 분기 완전한 합 유지
        facts.clear()
        facts.update({"ShortTermBorrowings": [{"end": "2025-09-30", "filed": "2025-10-30", "val": 0.5},
                                              {"end": "2025-12-31", "filed": "2026-02-12", "val": 0.6}],
                      "LongTermDebtNoncurrent": [{"end": "2025-09-30", "filed": "2025-10-30", "val": 47.0},
                                                 {"end": "2025-12-31", "filed": "2026-05-06", "val": 47.4}]})
        cs = bmh.component_sum("0", ["ShortTermBorrowings", "LongTermDebtNoncurrent"])
        check("E65 EXC형 늦은 큰 구성요소 → 부분 합 안 냄(9-30 47.5 유지)", bmh.as_of(cs, "2026-02-13") == 47.5)
        check("E65 EXC형 늦은 구성요소 공개 뒤 완전한 합 48.0", abs(bmh.as_of(cs, "2026-05-07") - 48.0) < 1e-9)
        # GS형: 연말에만 태깅되는 구성요소 — 직전 분기(9-30)에는 없고 1년 전 12-31에 있던 태그가 늦게 오면 부분 합 안 냄
        facts.clear()
        facts.update({"LongTermDebtNoncurrent": [{"end": q, "filed": f, "val": 5.0 if q == "2025-12-31" else 4.0} for q, f in
                                                 (("2024-12-31", "2025-02-20"), ("2025-03-31", "2025-05-01"), ("2025-06-30", "2025-08-01"),
                                                  ("2025-09-30", "2025-11-01"), ("2025-12-31", "2026-02-20"))],
                      "ShortTermBorrowings": [{"end": "2024-12-31", "filed": "2025-02-20", "val": 60.0},
                                              {"end": "2025-12-31", "filed": "2027-02-20", "val": 61.0}]})
        bmh._period_ends = lambda cik: [_d(2024, 12, 31), _d(2025, 3, 31), _d(2025, 6, 30), _d(2025, 9, 30), _d(2025, 12, 31)]
        cs = bmh.component_sum("0", ["LongTermDebtNoncurrent", "ShortTermBorrowings"])
        check("E65 GS형 연말 태그 늦음 → 부분 합 안 냄(9-30 값 4 유지)", bmh.as_of(cs, "2026-03-01") == 4.0)
    finally:
        bmh.concept, bmh._period_ends = keep_c, keep_pe
    # E66 현금 합계 대체: 기본 태그 직전 결산일(그 합계 행 공개일까지 공개된 것)보다 200일 넘게 뒤 결산일만, 제한현금은 뺀다
    keep_pi = bmh.pick_instant
    try:
        tot = [{"end": q, "val": v, "available": f} for q, v, f in (("2021-12-31", 5.0, "2022-02-01"), ("2022-06-30", 6.0, "2022-08-01"),
                                                                    ("2024-09-30", 8.5, "2024-11-01"))]
        rst = []
        bmh.pick_instant = lambda cik, tags: [dict(x) for x in (tot if "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents" in tags
                                                                else rst if "RestrictedCash" in tags else [])]
        base_cash = [{"end": "2021-09-30", "val": 4.0, "available": "2021-11-01"}, {"end": "2024-09-30", "val": 8.0, "available": "2024-11-01"}]
        f = bmh._cash_total_fill("0", base_cash)
        check("E66 직전 기본보다 273일 뒤(2022-06) 합계로 채움", bmh.as_of(f, "2023-01-01") == 6.0)
        check("E66 92일 뒤(2021-12)는 안 채움", bmh.as_of(f, "2022-03-01") == 4.0)
        check("E66 같은 결산일은 기본 태그(8.0, 합계 8.5 아님)", bmh.as_of(f, "2024-12-01") == 8.0)
        # 시점: 나중 기본 행(2022-09, 11월 공시)이 생겨도 5월에 공개된 합계(2022-06 아님, 2022-03 — 182일)는 그대로 안 채움
        tot[:] = [{"end": "2022-03-31", "val": 5.5, "available": "2022-05-01"}]
        base_l = [{"end": "2021-12-31", "val": 4.0, "available": "2022-02-01"}, {"end": "2022-09-30", "val": 7.0, "available": "2022-11-01"}]
        check("E66 미래 기본 행이 과거 판정을 바꾸지 않음(90일 → 안 채움)", len(bmh._cash_total_fill("0", base_l)) == 2)
        tot[:] = [{"end": "2025-03-31", "val": 6.0, "available": "2025-05-01"}]
        rst[:] = [{"end": "2025-03-31", "val": 0.5, "available": "2025-05-01"}]
        f3 = bmh._cash_total_fill("0", [{"end": "2024-03-31", "val": 4.0, "available": "2024-05-01"}])
        check("E66 제한현금은 뺀다(6.0 − 0.5)", bmh.as_of(f3, "2025-06-01") == 5.5)
    finally:
        bmh.pick_instant = keep_pi
    # E62 중단영업 주당 손익 빼기(카드 모드) — 분기마다 파일 값이 총 EPS인지 계속영업인지 확인
    keep_ps, keep_ar = bmh._ps_facts, bmh.ASOF_REF
    try:
        F = {"disc": [("2024-01-01", "2024-03-31", 0.10, "2024-05-01"), ("2024-04-01", "2024-06-30", 2.10, "2024-08-01"),
                      ("2024-01-01", "2024-09-30", 2.00, "2024-11-01"), ("2024-01-01", "2024-06-30", 2.20, "2024-08-01"),
                      ("2024-01-01", "2024-12-31", 4.90, "2025-02-10"), ("2024-07-01", "2024-09-30", -0.10, "2025-01-15")],
             "cont": [("2024-01-01", "2024-03-31", 1.00, "2024-05-01"), ("2024-04-01", "2024-06-30", 1.00, "2024-08-01"),
                      ("2024-07-01", "2024-09-30", 1.00, "2024-11-01"), ("2024-01-01", "2024-12-31", 4.00, "2025-02-10"),
                      ("2024-01-01", "2024-09-30", 3.00, "2024-11-01")],
             "tot": [("2024-01-01", "2024-03-31", 1.10, "2024-05-01"), ("2024-04-01", "2024-06-30", 3.10, "2024-08-01"),
                     ("2024-07-01", "2024-09-30", 0.90, "2024-11-01")]}
        bmh._ps_facts = lambda t, tags: F["disc" if tags == bmh.DISC_EPS_TAGS else "cont" if tags == bmh.CONT_EPS_TAGS else "tot"]
        bmh.ASOF_REF = None
        rows62 = [{"quarter_end": "2024-03-31", "quarter_eps": 1.10, "available_date": "2024-05-01"},
                  {"quarter_end": "2024-06-30", "quarter_eps": 3.10, "available_date": "2024-08-01"},
                  {"quarter_end": "2024-09-30", "quarter_eps": 0.90, "available_date": "2024-11-01"},
                  {"quarter_end": "2024-12-31", "quarter_eps": 3.90, "available_date": "2025-02-10"}]
        check("E62 3개월 값", abs(bmh.disc_eps_quarter("ZZZ", "2024-06-30", "2024-09-01") - 2.10) < 1e-9)
        check("E62 3개월 값이 아직 없으면 누계 차(9월 2.00 − 6월 2.20)", abs(bmh.disc_eps_quarter("ZZZ", "2024-09-30", "2024-12-01") + 0.20) < 1e-9)
        check("E62 4분기 = 연간 − 9개월", abs(bmh.disc_eps_quarter("ZZZ", "2024-12-31", "2025-03-01") - 2.90) < 1e-9)
        check("E62 공시 전 사실은 안 씀", bmh.disc_eps_quarter("ZZZ", "2024-12-31", "2025-01-01") == 0.0)
        # 파일이 총 EPS(1.10·3.10·0.90·3.90=4.0+2.9)인 분기는 뺀다: 0.10 + 2.10 − 0.10 + 2.90
        check("E62 총 EPS 분기들은 중단영업 합을 뺌", abs(bmh.disc_in_ttm("ZZZ", rows62, "2024-12-31", "2025-03-01") + 5.00) < 1e-9)
        # SNPS형: 4분기 파일 값이 이미 계속영업(1.00)이면 그 분기는 안 뺀다
        rows_c = rows62[:3] + [{"quarter_end": "2024-12-31", "quarter_eps": 1.00, "available_date": "2025-02-10"}]
        check("E62 파일이 이미 계속영업인 분기는 안 뺌(SNPS형)", abs(bmh.disc_in_ttm("ZZZ", rows_c, "2024-12-31", "2025-03-01") + 2.10) < 1e-9)
        check("E62 그 분기 제거 확인(E54 건너뛰기 조건)", bmh.disc_removed("ZZZ", rows62, "2024-06-30", "2025-03-01")
              and not bmh.disc_removed("ZZZ", rows_c, "2024-12-31", "2025-03-01"))
        rows_u = rows62[:3] + [{"quarter_end": "2024-12-31", "quarter_eps": 7.77, "available_date": "2025-02-10"}]
        check("E62 가를 수 없는 분기(파일 값이 총·계속 어느 쪽도 아님)는 안 뺌", abs(bmh.disc_in_ttm("ZZZ", rows_u, "2024-12-31", "2025-03-01") + 2.10) < 1e-9)
        F["disc"].append(("2025-01-01", "2025-03-31", 0.015, "2025-05-01"))
        F["cont"].append(("2025-01-01", "2025-03-31", 1.00, "2025-05-01"))
        check("E62 파일 = 계속영업이면 작은 중단영업(0.015)도 안 뺌", bmh.disc_quarter_status("ZZZ", 1.00, "2025-03-31", "2025-06-01") == (0.0, "already"))
        bmh.ASOF_REF = "2025-03-01"
        check("E62 연구 모드는 0", bmh.disc_in_ttm("ZZZ", rows62, "2024-12-31", "2025-03-01") == 0.0)
        bmh.ASOF_REF = None
        gap = rows62[:2] + [{"quarter_end": "2024-12-31", "quarter_eps": 3.90, "available_date": "2025-02-10"},
                            {"quarter_end": "2025-03-31", "quarter_eps": 1.0, "available_date": "2025-05-01"}]
        check("E62 이웃 분기 간격 120일 넘으면 0", bmh.disc_in_ttm("ZZZ", gap, "2025-03-31", "2025-06-01") == 0.0)
    finally:
        bmh._ps_facts, bmh.ASOF_REF = keep_ps, keep_ar
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
    ("E65 태그 포함 조건 제거", "            if i == len(parts) or (prev_tags is not None and seen >= prev_tags):", "            if True:"),
    ("E65 직전 4개 → 직전 1개", "        recent = (recent + [{t for _, _, t in parts}])[-4:]", "        recent = [{t for _, _, t in parts}]"),
    ("E66 현금 대체 간격 문턱 200 → 60", "        if (date.fromisoformat(e[\"end\"]) - date.fromisoformat(max(prev))).days > 200:", "        if (date.fromisoformat(e[\"end\"]) - date.fromisoformat(max(prev))).days > 60:"),
    ("E66 같은 결산일도 합계로", "        if any(b[\"end\"] == e[\"end\"] for b in known):\n            continue", "        if False:\n            continue"),
    ("E66 제한현금 안 뺌", "            fill.append(dict(e, val=e[\"val\"] - _rc(e[\"end\"], e[\"available\"]), _note=\"cash_total_tag\"))", "            fill.append(dict(e, _note=\"cash_total_tag\"))"),
    ("E62 이미 계속영업 판정 제거", "    if cont is not None and abs(file_q - cont) <= 0.011:\n        return 0.0, \"already\"", "    if False:\n        return 0.0, \"already\""),
    ("E62 판정 불가도 뺌", "    return 0.0, \"unknown\"", "    return -disc, \"unknown\""),
    ("E62 공시일 무시", "    rows = [r for r in facts if r[1] == q_end and r[3] <= upto]", "    rows = [r for r in facts if r[1] == q_end]"),
    ("E62 누계 차 제거", "            return y[2] - min(prev, key=lambda r: r[3])[2]", "            return y[2]"),
    ("E62 간격 검사 제거", "    if any((date.fromisoformat(b) - date.fromisoformat(a)).days > 120 for a, b in zip(qs, qs[1:])):\n        return None", "    if False:\n        return None"),
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
