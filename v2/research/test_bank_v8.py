#!/usr/bin/env python3
"""은행 사전 등록 8판 시험 — research/bank_v8_design.md §5-1·§5-2.

가짜 인스턴스(adapters/bank_sec_values)와 가짜 Bank(adapters/bank_rim)로 8판 규칙을 확인한다.
PNC 실제 자료로 하는 확인(가용일·누계 차분 4분기)도 몇 개 섞여 있다(로컬 companyfacts 캐시를 읽는다).

    python3 v2/research/test_bank_v8.py            # 시험
    python3 v2/research/test_bank_v8.py --mutate   # 변이 시험: 규칙을 일부러 망가뜨린 판마다 시험이 실패하는지
"""
import contextlib
import io
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(V2, "adapters"))
sys.path.insert(0, V2)
import bank_sec_values as bsv  # noqa: E402
import bank_rim as br  # noqa: E402

EM = {"concept": "us-gaap:StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
      "axis": "us-gaap:StatementEquityComponentsAxis", "member": "us-gaap:PreferredStockIncludingAdditionalPaidInCapitalMember"}
COMMON_M = "us-gaap:CommonStockIncludingAdditionalPaidInCapitalMember"
END = "2026-06-30"
FAKE = "0009999998"
PNC = "0000713676"


# ── 가짜 인스턴스 ─────────────────────────────────────────────────────────
def inst(facts, end=END):
    """facts: [(이름, 멤버 목록, 값, 단위 id)] — 시점 사실만. 단위 id: USD·EUR·PS(USD/shares)."""
    ctx, body, n = {}, [], 0
    for name, members, v, u in facts:
        key = tuple(members)
        if key not in ctx:
            ctx[key] = f"c{len(ctx)}"
        n += 1
        body.append(f'<{name} contextRef="{ctx[key]}" unitRef="{u}" decimals="-6" id="f{n}">{v}</{name}>')
    cx = "".join(
        f'<xbrli:context id="{cid}"><xbrli:entity><xbrli:identifier scheme="x">1</xbrli:identifier>'
        + ("<xbrli:segment>" + "".join(f'<xbrldi:explicitMember dimension="{a}">{m}</xbrldi:explicitMember>' for a, m in key)
           + "</xbrli:segment>" if key else "")
        + f"</xbrli:entity><xbrli:period><xbrli:instant>{end}</xbrli:instant></xbrli:period></xbrli:context>"
        for key, cid in ctx.items())
    un = ('<xbrli:unit id="USD"><xbrli:measure>iso4217:USD</xbrli:measure></xbrli:unit>'
          '<xbrli:unit id="EUR"><xbrli:measure>iso4217:EUR</xbrli:measure></xbrli:unit>'
          '<xbrli:unit id="PS"><xbrli:divide><xbrli:unitNumerator><xbrli:measure>iso4217:USD</xbrli:measure></xbrli:unitNumerator>'
          '<xbrli:unitDenominator><xbrli:measure>xbrli:shares</xbrli:measure></xbrli:unitDenominator></xbrli:divide></xbrli:unit>')
    return "<xbrli:xbrl>" + cx + un + "".join(body) + "</xbrli:xbrl>"


AX = EM["axis"]
BASE = [("us-gaap:StockholdersEquity", [], 64008e6, "USD"), ("us-gaap:AdditionalPaidInCapital", [], 21999e6, "USD"),
        (EM["concept"], [(AX, COMMON_M)], 16119e6, "USD")]


def mv(extra, base=BASE):
    return bsv.member_values(bsv._parse_instance(inst(base + extra)), END, EM)


CASES = []


def case(fn):
    CASES.append(fn)
    return fn


# §1-2 추출
@case
def member_single_value():
    assert mv([(EM["concept"], [(AX, EM["member"])], 5880e6, "USD")]) == {"pref_member": 5880e6, "apic": 21999e6}


@case
def member_two_same_and_two_different():
    same = mv([(EM["concept"], [(AX, EM["member"])], 5880e6, "USD")] * 2)
    diff = mv([(EM["concept"], [(AX, EM["member"])], 5880e6, "USD"), (EM["concept"], [(AX, EM["member"])], 5881e6, "USD")])
    assert same["pref_member"] == 5880e6 and diff["pref_member"] is None, (same, diff)


@case
def member_extra_axis_ignored():
    r = mv([(EM["concept"], [(AX, EM["member"]), ("us-gaap:ConsolidationItemsAxis", "us-gaap:OperatingSegmentsMember")], 1e6, "USD")])
    assert r["pref_member"] is None, r


@case
def member_non_usd_ignored():
    r = mv([(EM["concept"], [(AX, EM["member"])], 5880e6, "USD"), (EM["concept"], [(AX, EM["member"])], 9e9, "EUR")])
    assert r["pref_member"] == 5880e6, r
    assert bsv._parse_instance(inst([("us-gaap:EarningsPerShareBasic", [], 3.1, "PS")]))[0][5] == "iso4217:USD/xbrli:shares"


@case
def member_mixed_with_common_member_picks_preferred_only():
    r = mv([(EM["concept"], [(AX, EM["member"])], 5880e6, "USD")])
    assert r["pref_member"] == 5880e6 != 16119e6, r


@case
def apic_missing_is_none():
    r = mv([(EM["concept"], [(AX, EM["member"])], 5880e6, "USD")], base=BASE[:1] + BASE[2:])
    assert r["apic"] is None, r


# §1-3 재추출·§1-5 정정 — main()의 건너뛰기 판단과 filings()의 최초 공시 선택
FS6 = bsv._parse_instance(inst(BASE + [(EM["concept"], [(AX, EM["member"])], 5880e6, "USD")]))


def run_main(record, cache_v, em=True):
    calls = []
    d = tempfile.mkdtemp()
    out, tg = os.path.join(d, "v.json"), os.path.join(d, "t.json")
    json.dump({"PNC": {END: record}} if record else {}, open(out, "w"))
    json.dump({"preferred": {"PNC": {"tags": [], **({"equity_member": EM} if em else {})}}, "cet1": {"_default": {"tag": "x:Y"}}}, open(tg, "w"))
    keep = {k: getattr(bsv, k) for k in ("OUT", "TAGS", "peers", "CARDS", "filings", "cache_version", "facts6")}
    argv = sys.argv
    try:
        bsv.OUT, bsv.TAGS, bsv.CARDS = out, tg, {}
        bsv.peers = lambda: {"PNC": PNC}
        bsv.filings = lambda cik: [(END, "2026-08-05", "A1", "doc.htm", "10-Q")]
        bsv.cache_version = lambda accn: cache_v
        bsv.facts6 = lambda cik, accn, primary, end, refetch=False: calls.append(refetch) or FS6
        sys.argv = ["bank_sec_values.py"]
        bsv.main()
    finally:
        for k, v in keep.items():
            setattr(bsv, k, v)
        sys.argv = argv
    return calls, json.load(open(out))["PNC"][END]


@case
def refetch_when_record_lacks_member_and_cache_v1():
    calls, rec = run_main({"accn": "A1", "filed": "2026-08-05", "se": 1.0}, 1)
    assert calls == [True] and rec["pref_member"] == 5880e6 and rec["apic"] == 21999e6, (calls, rec)


@case
def reread_without_refetch_when_cache_v2():
    calls, _ = run_main({"accn": "A1", "filed": "2026-08-05"}, bsv.EXTRACT_VERSION)
    assert calls == [False], calls


@case
def skip_when_record_has_member_and_cache_v2():
    calls, _ = run_main({"accn": "A1", "filed": "2026-08-05", "pref_member": 1.0, "apic": 2.0}, bsv.EXTRACT_VERSION)
    assert calls == [], calls


@case
def refetch_when_record_has_member_but_cache_v1():
    calls, _ = run_main({"accn": "A1", "filed": "2026-08-05", "pref_member": 1.0, "apic": 2.0}, 1)
    assert calls == [True], calls


@case
def bank_without_equity_member_keeps_old_skip():
    calls, rec = run_main({"accn": "A1", "filed": "2026-08-05"}, 1, em=False)
    assert calls == [] and "pref_member" not in rec, (calls, rec)


@case
def filings_takes_earliest_original_not_amendment():
    sub = {"filings": {"recent": {"form": ["10-Q/A", "10-Q", "10-Q"], "reportDate": [END] * 3,
                                  "filingDate": ["2026-07-01", "2026-09-01", "2026-08-05"],
                                  "accessionNumber": ["AMD", "LATE", "FIRST"], "primaryDocument": ["a", "b", "c"]}, "files": []}}
    keep = bsv._get
    try:
        bsv._get = lambda url, raw=False: json.dumps(sub)
        fl = bsv.filings(PNC)
    finally:
        bsv._get = keep
    assert [x[2] for x in fl] == ["FIRST"], fl


# ── 가짜 Bank ────────────────────────────────────────────────────────────
Q = [END] + br.qends_before(END, 9)
F = "2026-08-05"


def _fb_class():
    class FB(br.Bank):   # 변이 시험이 모듈을 다시 불러오면 새 Bank를 이어받도록 매번 만든다
        def __init__(self, ed=8, em=True, pm=None, sh=None, se=None, pdq=None, div_pref=None):
            self.ed, self.t, self.cik, self.asof, self.ov = ed, "FAKE", FAKE, None, False
            self.pref_tbl = {"tags": [], "equity_member": EM} if em else None
            self.eq_mem = EM if (em and ed >= 8) else None
            self.se = {e: (100e9, F) for e in Q} if se is None else se
            self.secv = {e: {"filed": F, "apic": 20e9, **({"pref_member": (pm or {}).get(e, 5e9)} if (pm or {}).get(e, 5e9) is not None else {})} for e in Q}
            self.pref_liq, self.pref_val, self.pref_ever, self.pref_sh = {}, {e: (0.0, F) for e in Q}, True, {}
            self.gw = {e: (10e9, F) for e in Q}
            self._sh = {e: ((sh or {}).get(e, 1e9), F) for e in Q}
            self.ni = {e: (1e9, F) for e in Q}
            self.div_pref = div_pref or {}
            if pdq is not None:   # 없으면 실제 flow_q(가짜 companyfacts FAKE_FACTS)로
                self._pdq8 = pdq

        def tce(self, end):
            return self.ce(end)

        def shares(self, end):
            return self._sh.get(end)

        def ni_ttm(self, end, adjusted=False):
            return (4e9, F)

        def payout_ttm(self, end):
            return (2e9, F)

        def retention(self, end):
            return 0.5

        def ttm(self, series, end):
            v = [series.get(e) for e in [end] + br.qends_before(end, 3)]
            return (sum(x[0] for x in v), F) if all(v) else None

        def _carry_goodwill(self, end):
            return None
    return FB


def FB(*a, **k):
    return _fb_class()(*a, **k)



FAKE_FACTS = {}   # 가짜 은행의 companyfacts(us-gaap 태그 → 행 목록) — 시험마다 채우고 비운다
_orig_facts = br.bmh._facts
br.bmh._facts = lambda c: {"facts": {"us-gaap": {t: {"units": {"USD": rows}} for t, rows in FAKE_FACTS.items()}}} if c == FAKE else _orig_facts(c)


def ack_file(entries):
    d = tempfile.mkdtemp()
    p = os.path.join(d, "ack.json")
    json.dump(entries, open(p, "w"))
    return p


@contextlib.contextmanager
def acks(entries):
    keep = br.ACK
    br.ACK = ack_file(entries)
    try:
        yield
    finally:
        br.ACK = keep


# §1-6 CE 연결
@case
def ce_equity_member_path():
    assert FB().ce(END) == (95e9, F)


@case
def ce_missing_member_does_not_fall_back_to_par():
    b = FB(pm={END: None})
    assert b.ce(END) is None, b.ce(END)   # 1-1 경로(액면 0)로 떨어지면 CE = SE = 100e9


@case
def ce_pref_above_apic_is_none():
    assert FB(pm={END: 25e9}).ce(END) is None


@case
def ce_edition7_ignores_equity_member():
    b = FB(ed=7)
    assert b.eq_mem is None and b.ce(END) is None   # 7판: tags [] → _ce7 → CE 없음(지금과 같음)


@case
def bank_without_equity_member_uses_old_path():
    assert FB(em=False).ce(END) == (100e9, F)   # 표 없는 은행 1-1 경로(우선주 0) 그대로


# §1-7 N3
def n3(pm, end=END):
    with acks({}):
        return br.checks7(FB(pm=pm), end)["N3"]


@case
def n3_boundaries():
    ya = br.qends_before(END, 4)[-1]
    assert n3({ya: 10e9})["pass"] and n3({ya: 2.5e9})["pass"], "0.5·2.0 경계 통과"
    assert not n3({ya: 5e9 / 0.49})["pass"] and not n3({ya: 5e9 / 2.01})["pass"], "0.49·2.01 정지"


@case
def n3_one_side_only_stops():
    ya = br.qends_before(END, 4)[-1]
    assert n3({ya: None})["pass"] is False and n3({ya: 30e9})["pass"] is False   # 1년 전 값 없음·APIC 초과로 경로 값 없음


# §3 N5-2
def pdq(*per_tag):
    return [(t, d) for t, d in zip(br.PREF_DIV_TAGS8, per_tag)]


@case
def n52_first_tag_then_next_and_zero_is_value():
    b = FB(pdq=pdq({END: (0.0, F)}, {END: (9.0, F), Q[1]: (7.0, F)}))
    assert b.pref_div_q8(END)[0] == 0.0 and b.pref_div_q8(Q[1])[0] == 7.0 and b.pref_div_q8(Q[2]) is None


@case
def n52_one_positive_quarter_with_zero_deduction_stops():
    b = FB(em=False, pdq=pdq({Q[2]: (5e6, F)}))
    with acks({}):
        r = br.checks7(b, END)["N5_2"]
    assert r["pass"] is False and r["quarters"] == [Q[2]], r


@case
def n52_quarter_without_ce_not_targeted():
    se = {e: (100e9, F) for e in Q if e != Q[2]}   # TFC형 — 그 분기 StockholdersEquity 없음
    b = FB(em=False, se=se, pdq=pdq({Q[2]: (5e6, F)}))
    with acks({}):
        assert br.checks7(b, END)["N5_2"]["pass"] is True


@case
def n52_equity_member_bank_passes():
    b = FB(pdq=pdq({e: (78e6, F) for e in Q[:4]}))
    with acks({}):
        r = br.checks7(b, END)
    assert r["N5_2"]["pass"] is True and abs(r["N3"]["div_yield_ref"] - 312e6 / 5e9) < 1e-9, r["N3"]


@case
def n52_mixed_missing_quarters():
    b = FB(em=False, pdq=pdq({END: (0.0, F)}, {Q[3]: (4e6, F)}))   # 두 분기 결측, 한 분기 0, 한 분기 양수
    with acks({}):
        assert br.checks7(b, END)["N5_2"]["quarters"] == [Q[3]]


@case
def n52_q4_from_annual_minus_ytd_real_pnc():
    b = br.Bank("PNC", PNC, "2026-10-01", edition=8)
    q = [b.pref_div_q8(e) for e in ("2025-03-31", "2025-06-30", "2025-09-30", "2025-12-31")]
    fy = br._fy(PNC, q[-1][2], "2025-12-31", asof="2026-10-01")
    assert all(q) and fy and abs(sum(x[0] for x in q) - fy) < 1, (q, fy)


# §4 N4 승인
def n4(ack, ed=8, end="2026-03-31"):
    b = FB(ed=ed, em=False, sh={e: (1.3e9 if e >= "2026-03-31" else 1e9) for e in Q})
    with acks(ack):
        return br.checks7(b, end)


@case
def n4_no_ack_stops_exact_ack_passes():
    assert n4({})["N4"]["pass"] is False
    assert n4({"FAKE": {"2026-03-31": {"reason": "합병", "edition_min": 8, "source": "x"}}})["N4"]["pass"] is True


@case
def n4_other_quarter_ack_stops():
    assert n4({"FAKE": {"2025-12-31": {"reason": "x", "edition_min": 8, "source": "x"}}})["N4"]["pass"] is False


@case
def n4_window_boundary():
    fut = ["2026-09-30", "2026-12-31", "2027-03-31", "2027-06-30"]
    b = FB(em=False)
    for e in fut:
        b.se[e], b.secv[e], b.gw[e], b.ni[e] = (100e9, F), {"filed": F, "apic": 20e9, "pref_member": 5e9}, (10e9, F), (1e9, F)
    b._sh = {e: (1.3e9 if e >= "2026-03-31" else 1e9, F) for e in Q + fut}
    with acks({}):
        inside, outside = br.checks7(b, "2027-03-31")["N4"], br.checks7(b, "2027-06-30")["N4"]
    assert inside["pass"] is False and list(inside["unacked"]) == ["2026-03-31"], inside   # 앞 네 분기 안 — 급변 분기가 원인
    assert outside["pass"] is True, outside   # 다섯 분기 앞이면 창 밖


@case
def n4_edition_min_ignored_in_edition7():
    assert n4({"FAKE": {"2026-03-31": {"reason": "x", "edition_min": 8, "source": "x"}}}, ed=7)["N4"]["pass"] is False
    assert n4({"FAKE": {"2026-03-31": "문자열 승인"}}, ed=7)["N4"]["pass"] is True


@contextlib.contextmanager
def comps(by_end):
    """N3b용 자본 구성요소(가짜 은행) — {분기말: 구성요소 합}. 보통주+자본잉여금 칸에 합을 넣고 나머지는 0."""
    keep = br.instant
    def fake(cik, tag, asof=None):
        if cik != FAKE:
            return keep(cik, tag, asof)
        if tag == "CommonStocksIncludingAdditionalPaidInCapital":
            return {e: (v, F) for e, v in by_end.items()}
        return {e: (0.0, F) for e in by_end} if tag in ("RetainedEarningsAccumulatedDeficit", "AccumulatedOtherComprehensiveIncomeLossNetOfTax") else {}
    br.instant = fake
    try:
        yield
    finally:
        br.instant = keep


@case
def ack_clears_n3b_too():
    e1, ya = "2026-03-31", br.qends_before("2026-03-31", 4)[-1]
    with comps({e1: 99e9, ya: 95e9}):   # CE 95e9 대비 1년 전 0%, 이번 +4.2% → N3b 정지
        with acks({}):
            r0 = br.checks7(FB(), e1)
        with acks({"FAKE": {e1: {"reason": "x", "edition_min": 8, "source": "x"}}}):
            r1 = br.checks7(FB(), e1)
    assert r0["N3b"]["pass"] is False and r1["N3b"]["pass"] is True, (r0["N3b"], r1["N3b"])


@case
def ack_does_not_clear_n1():
    b = FB(pm={"2026-03-31": None})   # 이번 분기 차원 값 없음 → CE 없음
    with acks({"FAKE": {"2026-03-31": {"reason": "x", "edition_min": 8, "source": "x"}}}):
        r = br.checks7(b, "2026-03-31")
    assert r["N1"]["pass"] is False and "N1" in r["stop"], r["N1"]


@case
def ack_also_clears_n3_but_not_n1_n5():
    ya = br.qends_before("2026-03-31", 4)[-1]
    b = FB(sh={e: (1.3e9 if e >= "2026-03-31" else 1e9) for e in Q}, pm={ya: None},
           pdq=pdq({"2026-03-31": (5e6, F)}))
    with acks({"FAKE": {"2026-03-31": {"reason": "x", "edition_min": 8, "source": "x"}}}):
        r = br.checks7(b, "2026-03-31")
    assert r["N3"]["pass"] is True and r["N4"]["pass"] is True, r
    b2 = FB(em=False, sh=b._sh and {e: (1.3e9 if e >= "2026-03-31" else 1e9) for e in Q}, pdq=pdq({"2026-03-31": (5e6, F)}))
    with acks({"FAKE": {"2026-03-31": "x"}}):
        r2 = br.checks7(b2, "2026-03-31")
    assert r2["N5_2"]["pass"] is False and "N5_2" in r2["stop"], r2


# 효력표 — 동종업
@case
def peer_ok7_n52_excludes_n3_n4_do_not():
    with acks({}):
        ok_bad, why = br.peer_ok7(FB(em=False, pdq=pdq({END: (5e6, F)})), END)
        ok_n4, _ = br.peer_ok7(FB(sh={e: (1.3e9 if e >= "2026-03-31" else 1e9) for e in Q}), END)
        b3 = FB(pm={br.qends_before(END, 4)[-1]: None})
        n3_fail, ok_n3 = br.checks7(b3, END)["N3"]["pass"], br.peer_ok7(b3, END)[0]
    assert ok_bad is False and "N5_2" in why and ok_n4 is True and n3_fail is False and ok_n3 is True, (why, n3_fail)


@case
def edition7_paths_untouched():
    with acks({}):
        r = br.checks7(FB(ed=7, em=False, pdq=pdq({Q[2]: (5e6, F)})), END)["N5_2"]   # 7판 N5-2는 TTM(DividendsPreferredStock) — 새 태그를 보지 않는다
    real7 = br.Bank("PNC", PNC, "2026-10-26", edition=7)
    assert r["pass"] is True and real7.eq_mem is None and real7.ce(END) is None, r


@case
def n52_q4_is_annual_minus_nine_month_ytd():
    def row(start, end, val, form, fp):
        return {"start": start, "end": end, "val": val, "filed": "2026-02-20" if form == "10-K" else "2025-11-01", "form": form, "fp": fp, "fy": 2025, "accn": "A" + fp}
    FAKE_FACTS["DividendsPreferredStockCash"] = [
        row("2025-01-01", "2025-03-31", 70e6, "10-Q", "Q1"), row("2025-04-01", "2025-06-30", 80e6, "10-Q", "Q2"),
        row("2025-01-01", "2025-06-30", 150e6, "10-Q", "Q2"), row("2025-07-01", "2025-09-30", 90e6, "10-Q", "Q3"),
        row("2025-01-01", "2025-09-30", 240e6, "10-Q", "Q3"), row("2025-01-01", "2025-12-31", 340e6, "10-K", "FY")]
    try:
        b = FB(em=False)
        q4, q3 = b.pref_div_q8("2025-12-31"), b.pref_div_q8("2025-09-30")
    finally:
        FAKE_FACTS.clear()
    assert q4 and abs(q4[0] - 100e6) < 1 and q4[2] == "DividendsPreferredStockCash" and abs(q3[0] - 90e6) < 1, (q4, q3)


# 가용일 — PNC 실제 자료(2026-06 10-Q 접수 2026-08-05)
@case
def availability_real_pnc():
    before = br.Bank("PNC", PNC, "2026-08-04", edition=8)
    after = br.Bank("PNC", PNC, "2026-08-05", edition=8)
    assert before.ce(END) is None and round(after.ce(END)[0] / 1e6) == 58128 and after.ce(END)[1] == "2026-08-05", after.ce(END)


def run():
    bad = []
    for fn in CASES:
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                fn()
        except Exception as e:   # 단언 실패뿐 아니라 변이가 만든 오류도 실패로 센다
            bad.append(f"{fn.__name__}: {type(e).__name__} {e}")
    return bad


RIM_MUTANTS = {
    "APIC 상한 제거": ("0 < pm <= ap", "0 < pm"),
    "1-1 경로로 떨어지기 허용": ("        if p is None:   # 1-1 청산가·액면 경로로 떨어지지 않는다",
                          "        p = p or self.pref_liq.get(end) or self.pref_val.get(end)\n        if p is None:   # 1-1 청산가·액면 경로로 떨어지지 않는다"),
    "N3에서 차원 값 경로 제외": ("    if bank.eq_mem:   # 8판 §1-7", "    if False:   # 8판 §1-7"),
    "N5-2를 TTM 합으로 되돌림": ("    if bank.ed >= 8:   # 8판 §3", "    if False:   # 8판 §3"),
    "ack 판 무시": ('if isinstance(v, str) or edition >= v.get("edition_min", 0)', "if True"),
    "차원 값 경로 판 관문 제거": ('.get("equity_member") if self.ed >= 8 else None', '.get("equity_member")'),
    "N5-2 판 관문 제거": ("    if bank.ed >= 8:   # 8판 §3", "    if True:   # 8판 §3"),
}
SV_MUTANTS = {
    "멤버를 '포함'으로 느슨하게": ('d == ((em["axis"], em["member"]),)', '(em["axis"], em["member"]) in d'),
    "단위 검사 제거": ('and u == "iso4217:USD"]\n    ap', ']\n    ap'),
    "재추출 끔": ("refetch = bool(em) and cache_version(accn) != EXTRACT_VERSION", "refetch = False"),
}


def mutate():
    import importlib
    global bsv, br
    ok = True
    for name, (old, new) in list(RIM_MUTANTS.items()) + list(SV_MUTANTS.items()):
        mod = br if name in RIM_MUTANTS else bsv
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
