"""일회성 손익 장치(안건 E54, 설계 e54_v2_design.md r13 — 1단계) 시험.

가짜 종목(ZZZ) 고정 자료로 각 규칙의 기대 숫자를 본다. pipeline/test_pipeline.py는 건드리지 않는다.
  python3 v2/research/test_eps_oneoff.py            # 시험
  python3 v2/research/test_eps_oneoff.py --mutate   # 변이 시험(규칙을 하나씩 지우면 시험이 빨개지는지)
"""
import importlib
import json
import os
import sys
import tempfile
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, V2)
sys.path.insert(0, os.path.join(os.path.dirname(V2), "scripts"))
import build_multiple_history as bmh  # noqa: E402
import eps_oneoff as eo  # noqa: E402

T = "ZZZ"
TMP = tempfile.mkdtemp(prefix="e54_test_")
QS = []
_d = date(2021, 3, 31)
while _d <= date(2026, 6, 30):
    QS.append(_d.isoformat())
    m = _d.month + 3
    y = _d.year + (m > 12)
    m = m - 12 if m > 12 else m
    nxt = date(y, m, 28) + timedelta(days=4)
    _d = nxt - timedelta(days=nxt.day)


def eps_rows(qeps=None, ttm=None, fp=None):
    """분기 EPS 0.5(TTM 2.00) 기본. qeps·ttm·fp는 {결산일: 값}으로 덮는다."""
    qeps, ttm, fp = qeps or {}, ttm or {}, fp or {}
    rows = []
    for i, q in enumerate(QS):
        qe = qeps.get(q, 0.5)
        rows.append({"quarter_end": q, "quarter_eps": qe, "fp": fp.get(q, f"Q{(int(q[5:7]) // 3)}"),
                     "available_date": (date.fromisoformat(q) + timedelta(days=40)).isoformat()})
    for i, r in enumerate(rows):
        r["ttm_eps"] = ttm.get(r["quarter_end"], round(sum(x["quarter_eps"] for x in rows[max(0, i - 3):i + 1]), 6) if i >= 3 else None)
    return rows


def item(q, cats=("impairment",), eps=0.10, pre=None, tax=None, filed=None, **kw):
    pre = pre if pre is not None else (eps * 100 if eps is not None else 1000.0)
    tax = tax if tax is not None else 0.0
    it = {"id": kw.pop("id", f"{q}-{'-'.join(cats)}-{eps}"), "quarter_end": q, "filed": filed or q, "categories": list(cats),
          "line": "pretax", "adj_pretax": pre, "adj_tax": tax, "tax_basis": "disclosed", "tax_source": "src",
          "shares": 100, "shares_source": "10-Q", "eps_shares": 100,
          "tags": {"pretax_dcf": "PT", "pretax_includes": True, "pretax_a8": "PT", "pretax_a8_includes": True},
          "desc": kw.pop("desc", f"d-{q}-{cats}-{eps}"), "source": "url"}
    if eps is not None:
        it["adj_eps"] = eps
    else:
        it.pop("eps_shares")
    it.update(kw)
    return it


def setup(items, scan_q=None, facts=None, tax_oneoff=None, splits=None):
    data = {"_note": "test", T: {"scan": {"quarters": scan_q if scan_q is not None else QS, "sources": {"x": "y"},
                                          "gain_scan": True, "quarter_facts": facts or {}}, "items": items}}
    p = os.path.join(TMP, "eps_oneoff.json")
    json.dump(data, open(p, "w"))
    eo.EPS_ONEOFF = p
    tp = os.path.join(TMP, "tax_oneoff.json")
    json.dump({T: tax_oneoff or []}, open(tp, "w"))
    bmh.TAX_ONEOFF = tp
    eo._splits = (lambda t: splits or [])
    eo.eps_rows_for = (lambda t: None)
    bmh.ASOF_REF = None
    bmh.core_tickers = (lambda: {})
    eo.reset()


CAP = "2027-01-01"
E = "2026-06-30"
RESULTS = []


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))


def approx(a, b, tol=1e-6):
    return a is not None and abs(a - b) <= tol


def raises(fn):
    try:
        fn()
    except eo.OneoffError:
        return True
    return False


def run():
    RESULTS.clear()
    R = eps_rows()
    # ---- 반복(§3)
    w = QS[QS.index(E) - 7:QS.index(E) + 1]       # E로 끝나는 8분기 창
    setup([item(E, eps=0.30), item(w[1], eps=0.25, id="old1")])
    check("반복 창에 2번 → 적용", approx(eo.eps_adjust(T, R, E, CAP), 0.30))
    setup([item(E, eps=0.30), item(w[1], eps=0.25, id="o1"), item(w[2], eps=0.25, id="o2")])
    check("반복 창에 3번 → 안 함", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
    E2 = QS[QS.index(E) - 1]                        # 셋 중 하나가 창 밖으로 나간 다음 E를 흉내: 창 시작 앞 분기에 셋째
    w2 = QS[QS.index(E2) - 7:QS.index(E2) + 1]
    setup([item(E2, eps=0.30), item(w2[1], eps=0.25, id="o1"), item(QS[QS.index(w2[0]) - 1], eps=0.25, id="o2")])
    check("셋째가 창 밖이면 다시 적용", approx(eo.eps_adjust(T, R, E2, CAP), 0.30))
    setup([item(E, cats=("impairment", "restructuring"), eps=0.30), item(w[1], cats=("restructuring",), eps=0.25, id="o1"),
           item(w[2], cats=("restructuring",), eps=0.25, id="o2")])
    check("묶음은 든 범주마다 셈 — restructuring 반복이면 묶음 전체 안 씀", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
    setup([item(E, eps=0.30), item(w[1], eps=0.25, id="o1"), item(w[2], eps=0.25, id="o2", out_of_scope_mixed=True)])
    check("out_of_scope_mixed는 세기만(반복 3번)", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
    # r15(2026-10-30): 반복 셈은 문턱을 넘는 분기만 — 소액 항목 셋은 반복이 아니다
    setup([item(E, eps=0.30), item(w[1], eps=0.0001, id="o1"), item(w[2], eps=0.0001, id="o2")])
    check("r15 소액 항목(문턱 아래) 3번은 반복 아님 → 적용", approx(eo.eps_adjust(T, R, E, CAP), 0.30))
    setup([item(E, eps=0.30), item(w[1], eps=0.19, id="o1"), item(w[2], eps=0.21, id="o2")])
    check("r15 문턱(|G| 2.00의 10%) 아래 0.19는 안 셈 → 2번 → 적용", approx(eo.eps_adjust(T, R, E, CAP), 0.30))
    setup([item(E, eps=0.30), item(w[1], eps=0.15, id="o1"), item(w[1], eps=0.10, id="o1b", desc="o1b"), item(w[2], eps=0.25, id="o2")])
    check("r15 같은 분기 같은 범주는 합으로 셈(0.15 + 0.10) → 3번 → 안 함", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
    _rev, _ni = eo.revenue_ttm, eo.net_income_ttm
    try:
        eo.revenue_ttm = lambda t, e, c: 1e6                    # 매출 1% 바닥 = $10,000
        eo.net_income_ttm = lambda t, e, c: 1000.0              # 순이익률 0.1% < 2% → 바닥 적용(r16)
        setup([item(E, eps=0.30, pre=9000.0)])
        check("r15 매출 1% 바닥 아래(세전 $9,000) → 안 함", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
        setup([item(E, eps=0.30, pre=11000.0)])
        check("r15 매출 1% 바닥 위(세전 $11,000) → 적용", approx(eo.eps_adjust(T, R, E, CAP), 0.30))
        setup([item(E, eps=0.30, pre=20000.0), item(w[1], eps=0.25, pre=5000.0, id="o1"), item(w[2], eps=0.25, pre=20000.0, id="o2"),
               item(w[3], eps=0.25, pre=20000.0, id="o3")])
        check("r15 반복 셈도 매출 바닥 — 세전 $5,000 분기는 안 셈 → 3번 → 안 함", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
        setup([item(E, eps=0.30, pre=20000.0), item(w[1], eps=0.25, pre=5000.0, id="o1"), item(w[2], eps=0.25, pre=20000.0, id="o2")])
        check("r15 매출 바닥 아래 분기 빼면 2번 → 적용", approx(eo.eps_adjust(T, R, E, CAP), 0.30))
        eo.net_income_ttm = lambda t, e, c: 50000.0             # 순이익률 5% ≥ 2% → 바닥 없음(r16, COR형)
        setup([item(E, eps=0.30, pre=9000.0)])
        check("r16 순이익률 2% 이상이면 매출 바닥 없음 → 세전 $9,000도 적용", approx(eo.eps_adjust(T, R, E, CAP), 0.30))
        eo.net_income_ttm = lambda t, e, c: -50000.0            # 순손실 −5% < 2% → 바닥 적용(r16, Codex)
        setup([item(E, eps=0.30, pre=9000.0)])
        check("r16 적자(순이익률 −5%)면 바닥 적용 → 세전 $9,000 안 함", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
        eo.net_income_ttm = lambda t, e, c: 20000.0             # 정확히 2% → 바닥 없음
        setup([item(E, eps=0.30, pre=9000.0)])
        check("r16 순이익률 정확히 2%면 바닥 없음", approx(eo.eps_adjust(T, R, E, CAP), 0.30))
        eo.net_income_ttm = lambda t, e, c: None
        setup([item(E, eps=0.30, pre=9000.0)])
        check("r16 순이익 없으면 바닥 없이 판정", approx(eo.eps_adjust(T, R, E, CAP), 0.30))
    finally:
        eo.revenue_ttm, eo.net_income_ttm = _rev, _ni
    # r16 만성 항목: 크기와 상관없이 8분기 중 6번 이상이면 반복
    setup([item(E, eps=0.30)] + [item(w[k], eps=0.0001, id=f"c{k}") for k in range(1, 6)])
    check("r16 소액 항목 E 포함 6번 → 반복 → 안 함", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
    setup([item(E, eps=0.30)] + [item(w[k], eps=0.0001, id=f"c{k}") for k in range(0, 4)])   # 구성 4분기(w4~w7) 밖 4번 + E
    check("r16 소액 항목 E 포함 5번 → 반복 아님 → 적용", approx(eo.eps_adjust(T, R, E, CAP), 0.30))
    # r15 실제 매출 경로(revenue_ttm): cap 뒤 재작성은 분기화 전에 버린다(Codex r15 필수)
    import fetch_eps_history as _feh
    _pt, _ck, _rl = bmh.concept, dict(_feh.CIKS), set(_feh.RESTATED_LATEST)
    try:
        _feh.CIKS[T] = "0000000000"
        _feh.RESTATED_LATEST.add(T)
        _qs = [("2024-01-01", "2024-03-31"), ("2024-04-01", "2024-06-30"), ("2024-07-01", "2024-09-30"), ("2024-10-01", "2024-12-31")]
        _rv = [{"start": a_, "end": b_, "val": 100.0, "filed": "2025-02-01", "form": "10-K"} for a_, b_ in _qs] + \
              [{"start": a_, "end": b_, "val": 200.0, "filed": "2026-02-01", "form": "10-K"} for a_, b_ in _qs]
        # concept 단계에서 주입 — pick_tag 안의 태그 선택까지 실제 경로로(cap은 그보다 먼저 걸려야 한다, Codex r16)
        bmh.concept = lambda cik, tag, taxonomy="us-gaap": [dict(x) for x in _rv] if tag == "Revenues" else []
        eo.reset()
        check("r15 매출 TTM은 cap 당시 값(재작성 전 400)", approx(eo.revenue_ttm(T, "2024-12-31", "2025-03-01"), 400.0))
        eo.reset()
        check("r15 매출 TTM cap 뒤면 재작성 값(800)", approx(eo.revenue_ttm(T, "2024-12-31", "2026-03-01"), 800.0))
        _feh.CIKS.pop(T, None)
        eo.reset()
        check("r15 CIK 없으면 매출 None(바닥 없이 판정)", eo.revenue_ttm(T, "2024-12-31", "2026-03-01") is None)
    finally:
        bmh.concept = _pt
        _feh.CIKS.clear(); _feh.CIKS.update(_ck)
        _feh.RESTATED_LATEST.clear(); _feh.RESTATED_LATEST.update(_rl)
        eo.reset()
    setup([item(E, eps=0.30), item(w[1], eps=0.30, id="o1"), item(w[1], eps=-0.25, id="o1b", desc="o1b"), item(w[2], eps=0.25, id="o2")])
    check("r15 같은 분기 상쇄(+0.30 −0.25 = 0.05)는 안 셈 → E·w2 2번 → 적용", approx(eo.eps_adjust(T, R, E, CAP), 0.30))
    setup([item(E, eps=0.30, out_of_scope_mixed=True)])
    check("out_of_scope_mixed는 적용 안 함", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
    setup([item(E, eps=0.30)], scan_q=[q for q in QS if q != w[3]])
    check("안 훑은 분기가 창에 있으면 조정 0", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
    E0 = QS[10]
    setup([item(E0, eps=0.30)], scan_q=QS[3:])
    check("E₀ 앞 7분기를 훑었으면 E₀ 조정", approx(eo.eps_adjust(T, R, E0, CAP), 0.30))
    setup([item(E0, eps=0.30)], scan_q=QS[4:])
    check("E₀ 앞 7분기 중 하나라도 안 훑었으면 0", approx(eo.eps_adjust(T, R, E0, CAP), 0.0))
    # ---- 문턱(§4) — G = 2.00
    for a, want, nm in [(0.22, 0.0, "A +0.22 → 9.91% 안 함"), (0.23, 0.23, "A +0.23 → 10.31% 함"), (-0.20, -0.20, "A −0.20 → 10.0% 함")]:
        setup([item(E, eps=a)])
        check("문턱 " + nm, approx(eo.eps_adjust(T, R, E, CAP), want))
    setup([item(E, eps=0.30, id="p"), item(E, eps=-0.30, id="m", desc="m")])
    check("A = 0(상쇄) → 안 함", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
    Rz = eps_rows(qeps={q: 0.0 for q in QS})
    setup([item(E, eps=0.30, pre=500.0, tax=100.0, id="p"), item(E, eps=-0.30, pre=-500.0, tax=-100.0, id="m", desc="m")])
    check("A = 0이면 G = 0이어도 적용 없음(세율도 그대로)", eo.tax_adjust(T, Rz, E, "PT", "dcf", CAP) is None)
    Rn = eps_rows(qeps={q: -0.25 for q in QS})
    same = lambda ni, e: {E: {"ni_q": ni, "eps_q": e, "shares_gaap_q": 100, "shares_basic_q": 100, "shares_adj_q": 100, "qf_filed": E}}
    setup([item(E, eps=0.30)], facts=same(-25.0, -0.25))
    check("G −1.00·A +0.30 → 30% 함", approx(eo.eps_adjust(T, Rn, E, CAP), 0.30))
    Rs = eps_rows(qeps={q: -0.025 for q in QS})
    setup([item(E, eps=0.50)], facts=same(-2.5, -0.025))
    check("G −0.10·A +0.50 → 125% 함", approx(eo.eps_adjust(T, Rs, E, CAP), 0.50))
    q3 = QS[QS.index(E) - 3]
    setup([item(q3, eps=3.0, id="p"), item(E, eps=-3.0, id="m", desc="m")])
    En = QS[QS.index(E) + 1] if QS.index(E) + 1 < len(QS) else None
    check("상쇄 +3·−3 → 안 함", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
    setup([item(E, eps=0.30, id="big"), item(QS[QS.index(E) - 1], eps=0.01, id="small")])
    check("적용하면 문턱 아래 항목도 함께", approx(eo.eps_adjust(T, R, E, CAP), 0.31))
    setup([item("2026-05-31", eps=0.30)], scan_q=QS + ["2026-05-31"])
    check("E에 EPS 파일 행 없음 → 조정 0", approx(eo.eps_adjust(T, R, "2026-05-31", CAP), 0.0))
    # G에 tax_oneoff가 들어간다: tax_oneoff eps +1.0 → G 3.00, A 0.25 → 7.7% 안 함
    setup([item(E, eps=0.25)], tax_oneoff=[{"quarter_end": E, "filed": E, "eps": 1.0, "tax": 1.0}])
    check("G는 tax_oneoff를 뺀 뒤의 EPS", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
    # ---- 시점
    setup([item(E, eps=0.30, filed="2027-02-01")])
    check("filed > cap이면 안 셈", approx(eo.eps_adjust(T, R, E, CAP), 0.0))
    setup([item(E, eps=0.30)])
    bmh.ASOF_REF = "2026-12-01"
    check("연구 모드(ASOF_REF) → 조정 0", approx(eo.eps_adjust(T, R, E, CAP), 0.0) and not eo.has(T))
    bmh.ASOF_REF = None
    # ---- 세금(§5)
    it = item(E, eps=None, pre=1000.0, tax=210.0, tax_basis="statutory_assumed")
    setup([it])
    check("statutory_assumed 21% 통과", approx(eo.item_tax(it, CAP), 210.0))
    setup([item(E, eps=None, pre=1000.0, tax=220.0, tax_basis="statutory_assumed")])
    check("statutory_assumed 0.5% 밖 → 오류", raises(lambda: eo.load(T)))
    setup([item(E, eps=None, pre=1000.0, tax=5.0, tax_basis="equity_method")])
    check("equity_method adj_tax ≠ 0 → 오류", raises(lambda: eo.load(T)))
    setup([item(E, eps=None, pre=1000.0, tax=0.0, tax_basis="nontaxable")])
    check("nontaxable에 tax_note·tax_source_filed 없음 → 오류", raises(lambda: eo.load(T)))
    it = item(E, eps=None, pre=1000.0, tax=0.0, tax_basis="nontaxable", tax_note="10-K 세율 조정표", tax_source_filed="2026-12-15")
    setup([it])
    check("10-K 확인 전 cap → 21% 추정", approx(eo.item_tax(it, "2026-11-01"), 210.0))
    check("10-K 확인 뒤 cap → 0", approx(eo.item_tax(it, "2026-12-20"), 0.0))
    a = item(E, eps=None, pre=300e6, tax=75e6, tax_basis="disclosed_total", total_id="g", total_tax=100e6, id="a")
    b = item(E, eps=None, pre=100e6, tax=25e6, tax_basis="disclosed_total", total_id="g", id="b", desc="b")
    setup([a, b])
    check("총액 배분 합 = 총액 통과", eo.load(T) is not None)
    b2 = dict(b, adj_tax=40e6)
    setup([a, b2])
    check("총액 배분 합 ≠ 총액 → 오류", raises(lambda: eo.load(T)))
    setup([dict(a, adj_tax=25e6), dict(b, adj_tax=75e6)])
    check("총액 배분 합은 맞지만 세전 비율이 아님 → 오류", raises(lambda: eo.load(T)))
    setup([dict(a, adj_pretax=300e6), dict(b, adj_pretax=-100e6)])
    check("남은 항목 부호 섞임 → 오류(순서 6)", raises(lambda: eo.load(T)))
    setup([item(E, eps=0.6, pre=100.0, tax=40.0, tax_basis="implied_from_eps")])
    check("implied_from_eps 역산 일치(100 − 0.6 × 100 = 40) 통과", eo.load(T) is not None)
    setup([item(E, eps=0.6, pre=100.0, tax=0.0, tax_basis="implied_from_eps", parent_share=0.6)])
    check("implied_from_eps 역산 ÷ parent_share(100 − 60/0.6 = 0) 통과", eo.load(T) is not None)
    setup([item(E, eps=0.6e7, pre=100e7, tax=10e7, tax_basis="implied_from_eps")])
    check("implied_from_eps 역산 불일치 → 오류", raises(lambda: eo.load(T)))
    setup([item(E, eps=0.30, pre=100.0, tax=0.0)])
    eo.load(T)
    check("공시 주당 값과 세후 금액 크기 차이 → 경고", any("허용 폭 밖" in x for x in eo.warnings))
    setup([item(E, eps=0.30, pre=1000.0, tax=210.0, tax_basis="statutory_assumed")])
    check("추정 세금이 공시 주당 값과 허용 폭 밖 → 오류(순서 2로)", raises(lambda: eo.load(T)))
    setup([item(E, eps=0.30, pre=30.0, tax=40.0)])
    eo.load(T)
    check("공시 세금이 세전보다 큼 → 이상 공시 경고", any("세전보다 크거나" in x for x in eo.warnings))
    setup([item(E, eps=-0.5, pre=1000.0, tax=210.0, tax_basis="statutory_assumed")])
    check("추정 세금 + 부호 다른 공시 EPS → 오류", raises(lambda: eo.load(T)))
    setup([item(E, eps=-0.5, pre=1000.0, tax=210.0)])
    eo.load(T)
    check("공시 세금 + 부호 다른 공시 EPS → 경고만", any("부호가 다름" in x for x in eo.warnings))
    # ---- 주당 값
    it = item(E, eps=None, pre=1000.0, tax=210.0, shares=1000)
    check("computed = (세전 − 세금) ÷ 주식", approx(eo.adj_eps_gaap(it, CAP), 0.79))
    it = item(E, eps=None, pre=100.0, tax=0.0, shares=100, parent_share=0.6)
    check("parent_share 0.6", approx(eo.adj_eps_gaap(it, CAP), 0.6))
    it = item(E, eps=0.6667, eps_shares=120, shares=100)
    check("공시 주당 120주 → 100주 GAAP 환산 0.80004", approx(eo.adj_eps_gaap(it, CAP), 0.80004))
    it = item(E, eps=0.4167, eps_shares=120, shares=100)
    check("공시 주당 0.4167 → 0.50004", approx(eo.adj_eps_gaap(it, CAP), 0.50004))
    setup([item(E, eps=0.60, filed="2025-01-01")], splits=[("2026-01-01", 2.0)])
    check("분할 2:1 전 공시 → 절반", approx(eo.eps_adjust(T, R, E, CAP), 0.30))
    # ---- 분모 전환(§5) — 분기 EPS −1.00(GAAP 분모 = 기본 100), 나머지 분기 +1.00
    Rd = eps_rows(qeps={q: (-1.0 if q == E else 1.0) for q in QS})
    f = {E: {"ni_q": -100.0, "eps_q": -1.00, "shares_gaap_q": 100, "shares_basic_q": 100, "shares_adj_q": 120, "qf_filed": E}}
    setup([item(E, eps=None, pre=200.0, tax=0.0, shares=100)], facts=f)
    check("적자 → 흑자 Δ = 100/120 − (−1.00) = 1.833333", approx(eo.eps_adjust(T, Rd, E, CAP), 1.833333, 1e-5))
    setup([item(E, eps=None, pre=80.0, tax=0.0, shares=100, id="a"),
           item(E, eps=None, pre=50.0, tax=0.0, shares=100, id="b", desc="b", categories=["litigation"]),
           item(w[1], cats=("litigation",), eps=0.25, id="o1"), item(w[2], cats=("litigation",), eps=0.25, id="o2")], facts=f)
    check("반복으로 빠진 +50 → N* −20 → 분모 그대로, 조정 0.80", approx(eo.eps_adjust(T, Rd, E, CAP), 0.80))
    f2 = {E: dict(f[E], shares_adj_q=100)}
    setup([item(E, eps=None, pre=200.0, tax=0.0, shares=100)], facts=f2,
          tax_oneoff=[{"quarter_end": E, "filed": E, "eps": 0.50, "tax": 50.0}])
    # 분모 100(조정 주식 수 = 기본) → S = GAAP라 단순 합 경로: 2.00. tax_oneoff 0.50은 엔진이 따로 더한다
    check("조정 주식 수 = GAAP면 단순 합", approx(eo.eps_adjust(T, Rd, E, CAP), 2.0))
    f3 = {E: dict(f[E], shares_adj_q=120)}
    setup([item(E, eps=None, pre=200.0, tax=0.0, shares=100)], facts=f3,
          tax_oneoff=[{"quarter_end": E, "filed": E, "eps": 0.50, "tax": 50.0}])
    # N* = −100 + 200 + T(0.50 × 100) = 150 → 150/120 = 1.25 → Δ = 2.25, 엔진이 더한 0.50을 빼서 1.75
    check("적용 +200·T +50 → Δ 2.25(tax_oneoff 몫은 대신함)", approx(eo.eps_adjust(T, Rd, E, CAP) + 0.50, 2.25))
    # T_q 분할: tax_oneoff eps는 오늘 주식 기준 −2.10(2:1 분할 반영) → 공시 당시 −4.20 × 357.5 = −1,501.5
    f4 = {E: {"ni_q": -1000.0, "eps_q": -2.80, "shares_gaap_q": 357, "shares_basic_q": 357, "shares_adj_q": 360.0,
              "qf_filed": "2025-08-01"}}
    Rp = eps_rows(qeps={q: (-1.40 if q == E else 1.0) for q in QS})
    setup([item(E, eps=None, pre=4000.0, tax=0.0, shares=357, filed="2025-08-01")], facts=f4, splits=[("2026-01-01", 2.0)],
          tax_oneoff=[{"quarter_end": E, "filed": E, "eps": -2.10, "tax": -1500.0}])
    N = -1000.0 + 4000.0 + (-2.10 * 2 * 357)
    want = N / 360.0 / 2 - (-1.40) - (-2.10)
    check("T_q = eps × split × 분모(PANW형), Δ ÷ split", approx(eo.eps_adjust(T, Rp, E, CAP), want, 1e-6), f"{want:.6f}")
    f5 = {E: dict(f[E], eps_q=-0.90)}
    setup([item(E, eps=None, pre=200.0, tax=0.0, shares=100)], facts=f5)
    v = eo.eps_adjust(T, Rd, E, CAP)
    check("기준 일치 실패(Q1~Q3) → 단순 합 + 경고", approx(v, 2.0) and any("다름" in x for x in eo.warnings))
    Rq4 = eps_rows(qeps={q: (-1.0 if q == E else 1.0) for q in QS}, fp={E: "Q4-derived"})
    setup([item(E, eps=None, pre=200.0, tax=0.0, shares=100)], facts=f5)
    v = eo.eps_adjust(T, Rq4, E, CAP)
    check("Q4-derived 차이 → 경고만, Δ 그대로", approx(v, 1.833333, 1e-5) and any("파생·기타 분기" in x for x in eo.warnings))
    setup([item(E, eps=None, pre=200.0, tax=0.0, shares=100)], facts={E: dict(f[E], shares_adj_q=None)})
    v = eo.eps_adjust(T, Rd, E, CAP)
    check("조정 주식 수 없음 → 단순 합 + 경고", approx(v, 2.0) and any("조정 EPS 주식 수 없음" in x for x in eo.warnings))
    setup([item(E, eps=None, pre=200.0, tax=0.0, shares=100)])
    check("부호 바뀌는 분기에 quarter_facts 없음 → 오류", raises(lambda: eo.eps_adjust(T, Rd, E, CAP)))
    # ---- 구성 분기 증명(v1 3.1)
    Rb = eps_rows(ttm={E: 2.5})
    setup([item(E, eps=0.30)])
    check("합 ≠ ttm → 오류", raises(lambda: eo.eps_adjust(T, Rb, E, CAP)))
    Rg = [r for r in R if r["quarter_end"] != QS[QS.index(E) - 2]]
    setup([item(E, eps=0.30)])
    check("분기 행 결손(310일 넘음) → 오류", raises(lambda: eo.eps_adjust(T, Rg, E, CAP)))
    setup([item(QS[2], eps=0.30)])
    check("항목이 400일 밖이면 증명 안 함", approx(eo.eps_adjust(T, Rb, E, CAP), 0.0))
    setup([item(QS[1], eps=0.30)])
    v = eo.eps_adjust(T, R, QS[2], CAP)
    check("파일 첫 세 행(앞선 분기 < 3)은 오류가 아니라 조정 안 함 + 경고", approx(v, 0.0) and any("3개 미만" in x for x in eo.warnings))
    setup([item(QS[1], eps=0.30)])
    check("파일 첫 세 분기라도 같은 결산일 행 둘 → 오류", raises(lambda: eo.eps_adjust(T, R + [dict(R[2], available_date="2021-12-01")], QS[2], CAP)))
    # ---- 세율(§6·§12)
    setup([item(E, eps=0.30, pre=500.0, tax=100.0)])
    ta = eo.tax_adjust(T, R, E, "PT", "dcf", CAP)
    check("세율: 적용 항목 Σ세전·Σ세금", ta is not None and approx(ta[0], 500.0) and approx(ta[1], 100.0))
    setup([item(E, eps=0.30, pre=500.0, tax=100.0)])
    check("선언 태그 ≠ 엔진 선택 → 오류", raises(lambda: eo.tax_adjust(T, R, E, "OTHER", "dcf", CAP)))
    it = item(E, eps=0.30, pre=500.0, tax=100.0)
    it["tags"]["pretax_includes"] = False
    setup([it])
    check("세전 태그가 항목을 안 담으면 세율 미반영", eo.tax_adjust(T, R, E, "PT", "dcf", CAP) is None)
    setup([item(E, eps=0.10, pre=500.0, tax=100.0)])
    check("문턱 아래면 세율도 안 함", eo.tax_adjust(T, R, E, "PT", "dcf", CAP) is None)
    check("A8: o ≤ 0 → None", eo.a8_rate(-1, 100, 20, 0, 0, 0, (50, 10)) is None)
    check("A8: GAAP 적자인데 조정 세전 > 0 → 조정 세율", approx(eo.a8_rate(10, -20, -5, 0, 0, 0, (100, 21)), 16 / 80))
    check("A8: 조정 세전 ≤ 0·GAAP > 0 → GAAP 세율", approx(eo.a8_rate(10, 100, 20, 0, 0, 0, (-150, -30)), 0.20))
    check("A8: 둘 다 ≤ 0 → None", eo.a8_rate(10, -10, 0, 0, 0, 0, (-5, 0)) is None)
    # ---- 두 파일·형식
    setup([item(E, eps=0.30)], tax_oneoff=[{"quarter_end": E, "filed": E, "eps": 0, "tax": 0, "pretax": 100}])
    check("tax_oneoff pretax 같은 분기 → 오류", raises(lambda: eo.load(T)))
    setup([item(E, eps=0.30)], tax_oneoff=[{"quarter_end": E, "filed": E, "eps": 0, "tax": 0, "pretax": 0}])
    check("tax_oneoff pretax 칸이 0이어도 오류", raises(lambda: eo.load(T)))
    bmh.core_tickers = (lambda: {T: {}})
    it = item(E, eps=0.30)
    del it["tags"]["pretax_a8_includes"]
    setup([it]); bmh.core_tickers = (lambda: {T: {}})
    check("core 종목은 pretax_a8_includes 필수", raises(lambda: eo.load(T)))
    bmh.core_tickers = (lambda: {})
    setup([item(E, eps=0.30, id="x"), item(QS[3], eps=0.30, id="x")])
    check("id 중복 → 오류", raises(lambda: eo.load(T)))
    setup([item(E, cats=("hedge",), eps=0.30)])
    check("범주 밖 → 오류", raises(lambda: eo.load(T)))
    setup([item(E, eps=0.30)], scan_q=QS[:-1])
    check("항목 분기가 scan에 없음 → 오류", raises(lambda: eo.load(T)))
    # ---- 태그 라벨(엔진 pick_tag 표시: "태그(행 수)", 여러 태그는 +)
    setup([item(E, eps=0.30)])
    check("라벨 PT(211) = 선언 PT", eo.tax_adjust(T, R, E, "PT(211)", "dcf", CAP) is not None)
    check("라벨 PT(71)+X(81)에 선언 PT 포함", eo.tax_adjust(T, R, E, "PT(71)+X(81)", "dcf", CAP) is not None)
    check("라벨 X(5)에 선언 PT 없음 → 오류", raises(lambda: eo.tax_adjust(T, R, E, "X(5)", "dcf", CAP)))
    # ---- 세금 TTM 구성 분기
    setup([item(E, eps=0.30, pre=30.0, tax=0.0)])
    check("항목 분기가 세금 TTM 구성 분기 밖 → 세율 미반영 + 경고",
          eo.tax_adjust(T, R, E, "PT", "dcf", CAP, tax_quarters={QS[0]}) is None and any("구성 분기" in x for x in eo.warnings))
    check("항목 분기가 구성 분기 안 → 세율 반영", eo.tax_adjust(T, R, E, "PT", "dcf", CAP, tax_quarters=set(QS[-4:])) is not None)
    # ---- E 행 공시일 ≤ cap
    setup([item(E, eps=0.30)])
    late = R[QS.index(E)]["available_date"]
    check("E 행 공시일이 cap 뒤면 조정 안 함(세율 경로)", eo.tax_adjust(T, R, E, "PT", "dcf", "2026-07-01") is None and late > "2026-07-01")
    # ---- 같은 결산일 행
    dup = dict(R[QS.index(E)], ttm_eps=9.9, available_date="2026-08-20")
    setup([item(E, eps=0.30)])
    check("같은 결산일 행 둘 중 증명 넘는 하나를 씀", approx(eo.eps_adjust(T, R + [dup], E, CAP), 0.30))
    dup2 = dict(R[QS.index(E)], available_date="2026-08-20")
    setup([item(E, eps=0.30)])
    check("같은 결산일 행 둘 다 증명 → 오류", raises(lambda: eo.eps_adjust(T, R + [dup2], E, CAP)))
    # ---- 반복 창 결손
    Rgap = [r for r in R if r["quarter_end"] != QS[QS.index(E) - 5]]
    setup([item(E, eps=0.30)])
    v = eo.eps_adjust(T, Rgap, E, CAP)
    check("반복 창 분기 결손(달력 9분기) → 조정 안 함 + 경고", approx(v, 0.0) and any("연속 8분기" in x for x in eo.warnings))
    # ---- 경계값: A = G/9 정확히(부동소수)
    setup([item(E, eps=2.0 / 9)])
    check("A = G/9 경계 → 적용", approx(eo.eps_adjust(T, R, E, CAP), 2.0 / 9))
    # ---- quarter_facts 불러오기 검사
    ff = {E: {"ni_q": -100.0, "eps_q": -1.00, "shares_gaap_q": 150, "shares_basic_q": 150, "qf_filed": E}}
    setup([item(E, eps=None, pre=200.0, tax=0.0, shares=100)], facts=ff)
    check("항목 shares ≠ shares_gaap_q → 오류", raises(lambda: eo.load(T)))
    setup([item(E, eps=None, pre=200.0, tax=0.0, shares=100)], facts={E: {"ni_q": -100.0, "eps_q": -1.0, "shares_gaap_q": 100, "qf_filed": E}})
    check("quarter_facts 칸 없음 → 오류", raises(lambda: eo.load(T)))
    setup([item(E, eps=None, pre=200.0, tax=0.0, shares=100)],
          facts={E: {"ni_q": -150.0, "eps_q": -1.0, "shares_gaap_q": 100, "shares_basic_q": 100, "qf_filed": E}})
    eo.load(T)
    check("ni_q ÷ 주식 대 eps_q 다름 → 경고", any("ni_q ÷ shares_gaap_q" in x for x in eo.warnings))
    # ---- T_q 때문에만 부호가 바뀌는 분기
    setup([item(E, eps=0.50)], tax_oneoff=[{"quarter_end": E, "filed": E, "eps": 0.80, "tax": 80.0}])
    check("tax_oneoff 몫까지 넣어 부호가 바뀌면 quarter_facts 필수", raises(lambda: eo.eps_adjust(T, Rd, E, CAP)))
    qa = QS[QS.index(E) - 1]
    setup([item(qa, eps=0.50)], facts={E: {"ni_q": -100.0, "eps_q": -1.0, "shares_gaap_q": 100, "shares_basic_q": 100,
                                           "shares_adj_q": 120, "qf_filed": E}},
          tax_oneoff=[{"quarter_end": E, "filed": E, "eps": 2.0, "tax": 200.0}])
    check("장치 항목이 없는 분기도 T_q로 부호가 바뀌면 Δ로 대신(0.5 + 1.833333 − 2.0)",
          approx(eo.eps_adjust(T, Rd, E, CAP), 0.5 + (100 / 120 + 1.0) - 2.0, 1e-6))
    # ---- 2라운드: 16주 4분기·탈락 행·EPS 0 분기·T만 있는 분기·캐시·여러 태그 라벨
    Q16 = list(QS)
    R16 = eps_rows()
    k = QS.index(E) - 4                               # 창 안 한 간격을 112일로(16주 4분기 흉내 — 앞 분기 결산일을 당김)
    moved = (date.fromisoformat(QS[k]) - timedelta(days=21)).isoformat()
    for r in R16:
        if r["quarter_end"] == QS[k]:
            r["quarter_end"] = moved
    setup([item(E, eps=0.30)], scan_q=[moved if q == QS[k] else q for q in QS])
    check("16주 4분기 간격(112일)은 결손 아님 → 적용", approx(eo.eps_adjust(T, R16, E, CAP), 0.30))
    dup = dict(R[QS.index(E)], ttm_eps=9.9, available_date="2026-08-20")
    setup([item(E, eps=0.30)])
    check("증명 못 넘은 같은 결산일 행에는 조정 안 붙음", approx(eo.eps_adjust(T, R + [dup], E, CAP, row=dup), 0.0)
          and approx(eo.eps_adjust(T, R + [dup], E, CAP, row=R[QS.index(E)]), 0.30))
    bad = dict(R[QS.index(E)], quarter_eps=9.0)      # 공시일·TTM은 같고 분기 EPS만 다름 → 증명 탈락
    setup([item(E, eps=0.30)])
    check("공시일·TTM이 같아도 분기 EPS가 다른 탈락 행에는 조정 안 붙음", approx(eo.eps_adjust(T, R + [bad], E, CAP, row=bad), 0.0))
    R0 = eps_rows(qeps={q: (0.0 if q == E else 0.7) for q in QS})
    setup([item(E, eps=0.30)])
    check("GAAP 분기 EPS 0(반올림된 적자일 수 있음) → 조정 뒤 흑자면 quarter_facts 필수", raises(lambda: eo.eps_adjust(T, R0, E, CAP)))
    qa = QS[QS.index(E) - 1]
    Rt = eps_rows(qeps={q: (-1.0 if q == qa else 1.0) for q in QS})
    setup([item(E, eps=0.60)], tax_oneoff=[{"quarter_end": qa, "filed": qa, "eps": 1.50, "tax": 150.0}])
    check("장치 항목 없는 분기도 tax_oneoff로 부호 바뀌면 quarter_facts 필수", raises(lambda: eo.eps_adjust(T, Rt, E, CAP)))
    setup([item(E, eps=0.30)])
    L1 = eps_rows(); v1 = eo.eps_adjust(T, L1, E, CAP)
    L1[QS.index(E)]["ttm_eps"] = 2.5                 # 같은 리스트(같은 id)의 내용만 바뀜
    check("내용이 바뀐 리스트는 캐시를 쓰지 않음(증명 실패 → 오류)", approx(v1, 0.30) and raises(lambda: eo.eps_adjust(T, L1, E, CAP)))
    setup([item(E, eps=0.30)])
    eo._tag_has_quarter = (lambda t, tags, q: False)
    check("여러 태그 라벨에서 선언 태그가 그 분기를 공급하지 않으면 오류", raises(lambda: eo.tax_adjust(T, R, E, "PT(3)+X(4)", "dcf", CAP)))
    eo._tag_has_quarter = (lambda t, tags, q: True)
    check("여러 태그 라벨에서 공급 태그면 통과", eo.tax_adjust(T, R, E, "PT(3)+X(4)", "dcf", CAP) is not None)
    setup([item(E, eps=0.30)])
    eo._tag_has_quarter = (lambda t, tags, q: len(tags) > 1)
    ta = eo.tax_adjust(T, R, E, "PT(3)+X(4)", "dcf", CAP)
    check("태그 전환 분기(합친 흐름에만 있음) → 경고만, 세율 반영", ta is not None and any("합친 세전 흐름" in x for x in eo.warnings))
    setup([item(E, eps=0.30)])
    eo._tag_has_quarter = (lambda t, tags, q: tags == ["X"] or len(tags) > 1)   # 다른 태그 X가 그 분기를 공급
    check("다른 태그가 그 분기를 공급하면 선언 잘못 → 오류", raises(lambda: eo.tax_adjust(T, R, E, "PT(3)+X(4)", "dcf", CAP)))
    # ---- 순서·반복 실행
    its = [item(E, eps=0.30, id="a"), item(QS[QS.index(E) - 1], eps=0.05, id="b"), item(w[0], cats=("litigation",), eps=0.02, id="c")]
    setup(its)
    v1 = eo.eps_adjust(T, R, E, CAP)
    setup(list(reversed(its)))
    v2 = eo.eps_adjust(T, R, E, CAP)
    v3 = eo.eps_adjust(T, R, E, CAP)
    check("항목 순서를 바꿔도·두 번 돌려도 같음", approx(v1, v2) and approx(v2, v3) and approx(v1, 0.35))
    return RESULTS


MUTANTS = [
    ("r15 반복 셈 크기 무시", "        if abs(e_) + EPS_TOL >= THRESHOLD * abs(G) and abs(u_) >= floor_usd and (e_ or u_):", "        if True:"),
    ("r15 반복 셈 매출 바닥 제거", "abs(e_) + EPS_TOL >= THRESHOLD * abs(G) and abs(u_) >= floor_usd and", "abs(e_) + EPS_TOL >= THRESHOLD * abs(G) and"),
    ("r15 매출 cap 선필터 제거", "[e for e in _concept(c, tag, taxonomy) if e.get(\"filed\", \"\") <= cap]", "_concept(c, tag, taxonomy)"),
    ("r16 만성 6번 규칙 제거", "REPEAT_PRESENT = 6", "REPEAT_PRESENT = 99"),
    ("r16 만성 문턱 6 → 5", "REPEAT_PRESENT = 6", "REPEAT_PRESENT = 5"),
    ("r16 저마진 조건 제거(항상 바닥)", "        elif rev > 0 and ni / rev < LOW_MARGIN:", "        elif True:"),
    ("r16 순이익률 절댓값", "        elif rev > 0 and ni / rev < LOW_MARGIN:", "        elif abs(ni) < LOW_MARGIN * abs(rev):"),
    ("r16 순이익 없으면 바닥", "        if ni is None:\n", "        if False:\n"),
    ("r15 적용 매출 바닥 제거", "    if abs(sum(it[\"adj_pretax\"] for it in cand)) < floor_usd:", "    if False:"),
    ("r15 반복 셈 분기 합 대신 항목별", "                s_[0] += adj_eps_gaap(it, cap) / _split_ratio(it[\"filed\"], sp)", "                s_[0] = max(s_[0], adj_eps_gaap(it, cap) / _split_ratio(it[\"filed\"], sp))"),
    ("반복 셈 3 → 4", "REPEAT_MIN = 3", "REPEAT_MIN = 4"),
    ("안 훑은 분기 검사 제거", "    if not set(window) <= scan_q:\n        return None", "    if False:\n        return None"),
    ("반복 창 8 → 4", "REPEAT_WINDOW = 8", "REPEAT_WINDOW = 4"),
    ("반복 창 결손 검사 제거", " or max(gaps) > QUARTER_GAP_MAX", ""),
    ("문턱 분모 max 제거", "THRESHOLD * max(abs(G), abs(G + A))", "THRESHOLD * abs(G)"),
    ("문턱 경계 오차 허용 제거", "abs(A) + EPS_TOL <", "abs(A) <"),
    ("A = 0 규칙 제거", "    if A == 0:\n        return None\n", ""),
    ("부호 뒤집기", "        return it[\"adj_eps\"] * it[\"eps_shares\"] / it[\"shares\"]", "        return -it[\"adj_eps\"] * it[\"eps_shares\"] / it[\"shares\"]"),
    ("filed ≤ cap 제거", "items = [it for it in rec[\"items\"] if it[\"filed\"] <= cap]", "items = list(rec[\"items\"])"),
    ("E 행 공시일 ≤ cap 제거", " and e.get(\"available_date\", \"\") <= cap]", "]"),
    ("연구 모드 스위치 제거", "    if research_mode():\n        return None\n", ""),
    ("비과세 10-K 전 추정 제거", "        return STATUTORY * it[\"adj_pretax\"]\n    return it[\"adj_tax\"]", "        pass\n    return it[\"adj_tax\"]"),
    ("parent_share 무시", "* it.get(\"parent_share\", 1) / it[\"shares\"]", "/ it[\"shares\"]"),
    ("A8 양수 검사를 조정 앞으로", "    if o <= 0:\n        return None\n    pa =", "    if o <= 0 or pt <= 0:\n        return None\n    pa ="),
    ("T_q 분할 무시", "T = t_eps * r * f[\"shares_gaap_q\"]", "T = t_eps * f[\"shares_gaap_q\"]"),
    ("Δ 분할 무시", "delta = N / S / r - fq", "delta = N / S - fq"),
    ("tax_oneoff 몫 대신 안 함", "total += delta - t_eps", "total += delta"),
    ("부호 판정에서 T_q 뺌", "(fq + simple + t_eps > 0)", "(fq + simple > 0)"),
    ("구성 분기 증명 제거", "    if pr is None:\n        raise", "    if pr is None and False:\n        raise"),
    ("같은 결산일 둘 다 증명 오류 제거", "    if len(ok) > 1:\n        raise", "    if False:\n        raise"),
    ("세전 포함 검사 제거", "        if not it[\"tags\"].get(inc_key):\n            continue\n", ""),
    ("태그 대조 제거", "        if decl not in chosen:", "        if False:"),
    ("라벨 행 수 떼기 제거", "re.sub(r\"\\(\\d+\\)$\", \"\", x.strip())", "x.strip()"),
    ("세금 구성 분기 검사 제거", "        if tax_quarters is not None and it[\"quarter_end\"] not in tax_quarters:", "        if False:"),
    ("두 파일 pretax 0 놓침", "if \"pretax\" in x}", "if x.get(\"pretax\")}"),
    ("quarter_facts 주식 수 검사 제거", "            if it[\"quarter_end\"] == q and it[\"shares\"] != f[\"shares_gaap_q\"]:", "            if False:"),
    ("결손 문턱 160 → 100(16주 분기 오판)", "QUARTER_GAP_MAX = 160", "QUARTER_GAP_MAX = 100"),
    ("탈락 행 조정 차단 제거", "    if row is not None and row is not j[\"row\"]", "    if False and row is not j[\"row\"]"),
    ("EPS 0 분기 사실 요구 제거", "and fq is not None and (fq > 0)", "and fq not in (None, 0) and (fq > 0)"),
    ("행 비교에서 분기 EPS 뺌", "r.get(\"ttm_eps\"), r.get(\"quarter_eps\"), r.get(\"fp\"), r.get(\"accn\"))", "r.get(\"ttm_eps\"))"),
    ("T만 있는 분기 사실 요구 제거", "if (its or t_eps) and fq", "if its and fq"),
    ("캐시 키를 리스트 id로", "_fingerprint(eps_rows))", "id(eps_rows))"),
    ("여러 태그 공급 검사 제거", "        if len(chosen) > 1 and not _tag_has_quarter(", "        if False and not _tag_has_quarter("),
    ("태그 전환 예외에서 다른 태그 공급 검사 제거", "            if not any(_tag_has_quarter(ticker, [x], it[\"quarter_end\"]) for x in chosen - {decl}) \\\n                    and _tag", "            if _tag"),
    ("파일 첫 세 행 예외 제거", "    if _ordered_quarters(eps_rows).index(E) < 3:", "    if False:"),
    ("첫 세 분기 중복 검사 제거", "        if len(same) > 1:\n            raise OneoffError(f\"{ticker} {E}: 같은 결산일 EPS 행 둘 이상(파일 첫 세 분기)\")", "        if False:\n            raise OneoffError(\"x\")"),
    ("역산 세금 검사 제거", "        if abs(tax - want) > max(1e6, 0.005 * abs(want)):", "        if False:"),
    ("총액 비례 검사 제거", "            if abs(it[\"adj_tax\"] - want) > max(1e6, 0.005 * abs(want)):", "            if False:"),
]


def mutate():
    src0 = open(os.path.join(V2, "eps_oneoff.py")).read()
    caught = 0
    for name, a, b in MUTANTS:
        assert src0.count(a) >= 1, f"변이 자리 없음: {name}"
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader("eps_oneoff", loader=None))
        mod.__file__ = os.path.join(V2, "eps_oneoff.py")
        exec(compile(src0.replace(a, b), mod.__file__, "exec"), mod.__dict__)
        global eo
        keep = eo
        eo = mod
        try:
            res = run()
            red = [n for n, ok, _ in res if not ok]
        except Exception as ex:          # 변이로 예외가 나도 잡힌 것
            red = [f"예외 {type(ex).__name__}"]
        eo = keep
        caught += bool(red)
        print(("잡음 " if red else "놓침 ") + name + (f" — {red[0]}" if red else ""))
    print(f"변이 {caught}/{len(MUTANTS)} 잡음")
    return caught == len(MUTANTS)


if __name__ == "__main__":
    import importlib.util  # noqa: F401
    if "--mutate" in sys.argv:
        sys.exit(0 if mutate() else 1)
    res = run()
    for n, ok, d in res:
        if not ok:
            print("실패:", n, d)
    print(f"{sum(ok for _, ok, _ in res)}/{len(res)} 통과")
    sys.exit(0 if all(ok for _, ok, _ in res) else 1)
