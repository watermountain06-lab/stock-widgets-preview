#!/usr/bin/env python3
"""v2 시안: 내재가치(DCF)로 적정주가를 구한다.

왜 DCF인가
----------
카드가 지금 쓰는 두 지표는 모두 **상대 평가**다. 백분위는 "배수가 자기 과거보다
낮은가", 피어 판정은 "배수가 남들보다 낮은가"를 잰다. 둘 다 "이 회사가 그 값을
받을 만한가"에는 답하지 않는다. 그레이엄·버핏 방식은 회사가 앞으로 벌어들일
현금의 현재가치를 먼저 구하고, 주가가 거기서 얼마나 할인돼 있는지(안전마진)를
본다. 이 스크립트가 그 계산을 한다.

구조는 사용자가 기관에서 받은 Dechra DCF 모델(`~/Downloads/Dechra DCF Model (1).xlsx`)을
그대로 따른다:

    매출 → EBITDA → 감가상각 차감 → EBIT → 세금 → NOPAT
         → 설비투자·운전자본 증감 차감 → 무차입 잉여현금흐름
         → 할인 → 영구성장(GGM)과 출구배수 두 방법으로 기업가치
         → 두 값을 평균 → 순부채 차감 → 주주가치 → 주당 내재가치

Dechra 모델이 두 방법을 나란히 놓고 평균하는 이유는 둘이 크게 다르기 때문이다
(그 모델에서 £1,722m 대 £2,398m, 39% 차이). 그 격차 자체가 불확실성의 크기다.

가정은 숨기지 않는다
--------------------
DCF 결과는 성장률과 할인율에 크게 흔들린다. 그래서 (1) 모든 가정을 인자로 받아
출력에 그대로 찍고, (2) 할인율과 영구성장률을 바꿔가며 만든 민감도 표를 함께
낸다. 표의 폭이 좁으면 값을 믿을 만하고, 넓으면 그 자체가 경고다.

기초 수치는 `build_multiple_history.py`와 같은 방식으로 SEC XBRL에서 받는다
(그날까지 공시된 것만 쓰는 규칙도 같다).

사용법
------
    python3 v2/build_dcf.py NVDA --growth 45,30,22,16,12 --wacc 0.10 \
        --terminal 0.025 --exit-multiple 25
"""
import argparse
import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import build_multiple_history as bmh  # noqa: E402
import fetch_eps_history as feh  # noqa: E402

# 이력 창 시작일. 중앙값은 창 선택에 흔들린다 — NVDA 마진 중앙값이 창을
# 2021-01로 잡으면 49.4%, 2021-07로 잡으면 56.6%다. 한곳에 고정해 둔다.
WINDOW_START = "2021-07-01"
# 분사로 이력이 짧아진 종목의 (최근 4분기 시작 결산일, 최소 개수). GE: 계속사업(GE 에어로스페이스 단독) 재작성 값이
# 2023년 2분기부터 있어 최근 4분기 끝 2024-03-31부터 10개(2026-06까지). 3년·5년 성장률이 같은 약 2.25년 CAGR이 된다
# (2026-09-30 사용자 결정 "분사 뒤 단독 숫자만").
# SNDK: 2025-02 WDC에서 분사. 회사 공시의 단독(carve-out) 분기가 2023-10부터 있어 최근 4분기 끝 2024-09-27부터
# 8개(2026-07까지). 3년·5년 성장률이 같은 약 1.8년 CAGR이 된다(2026-10-01, GE 선례 적용).
# GEV: 2024-04 GE에서 분사. 단독(carve-out) 분기가 2023-01부터 있어 최근 4분기 끝 2023-12-31부터 11개(2026-06까지),
# 약 2.5년 CAGR(2026-10-01, SNDK와 같은 방식).
# IBM: 2021-11 Kyndryl 분사 — 2021년 분기는 재작성(계속사업) 값이 있지만 2020년 4분기는 원공시라 최근 4분기 끝 2021-12-31부터 19개,
# 약 4.5년 CAGR(2026-10-01, GE 방식).
HISTORY_WINDOW = {"GE": ("2024-03-31", 9), "SNDK": ("2024-09-27", 8), "GEV": ("2023-12-31", 11), "IBM": ("2021-12-31", 18),
                  # WDC: SanDisk 분사(2025-02). 분기 매출은 FY24부터 재작성 값이 있지만 영업이익은 FY25 1·2분기 10-Q가 비교 수치로 낸
                  # FY24 분기가 분사 전 원공시라(−596·−210·+94·−91, 계속사업 연간은 −403 — Codex) 네 분기가 모두 계속사업인 첫 최근
                  # 4분기 합은 FY25 말(2025-06-27)이다. 그 전 창은 5년 성장률 −5.3%(원공시)·57%(섞인 합)로 나왔다(2026-10-02, GE 방식).
                  # 이력이 1년(합 5개)뿐이라 3년·5년 성장률이 같은 값이다.
                  "WDC": ("2025-06-27", 5),
                  # T: WarnerMedia 분사(2022-04). 네 분기가 모두 분사 뒤인 첫 최근 4분기 합은 2023-03-31(2026-10-02).
                  "T": ("2023-03-31", 13),
                  # DHR: Veralto 분사 — 재작성 값으로 네 분기가 모두 계속사업인 첫 최근 4분기 합은 2022년 말(2026-10-02).
                  "DHR": ("2022-12-31", 13)}


def latest(series, asof=None):
    """그 시점까지 **공개돼 있던** 가장 최근 값. asof가 없으면 최신값.

    백테스트가 각 체크포인트에서 당시 공시만 쓰는 것과 같은 규칙이다. 이게
    없으면 내재가치가 시점마다 어떻게 변했는지 재현할 수 없고, 오늘 값 하나를
    과거 전체에 가로줄로 긋게 된다.
    """
    if not series:
        return None
    if asof is None:
        return series[-1]["val"]
    # 끝까지 훑는다 — 시리즈가 공시일 순서가 아니어도 그날까지 공개된 마지막 값을 놓치지 않게(C8, Codex). 공시일 순서인
    # 시리즈(component_sum·instant_series·ttm_series)는 예전과 결과가 같다(2026-10-03 계측: 뒤바뀐 입력 0건).
    ok = [e for e in series if e.get("available", e.get("end")) <= asof]
    return ok[-1]["val"] if ok else None


# 투자자산이 영업 자산인 회사(CIK) — 투자 수익이 영업이익 안에 있다. 값은 근거.
INVESTMENTS_OPERATING = {"0000731766": "UNH — 10-Q 손익계산서 Revenues에 'Investment and other income'(2026 Q2 $1,223M), Earnings from operations에 포함",
                         "0000040545": "GE — 런오프 보험 투자증권 $37.9B가 보험 부채 $36.2B를 받친다. 투자수익은 'Insurance revenue'(2026 Q2 $715M)로 매출·영업이익 안(2026-09-30 사용자 결정)"}


def base_inputs(ticker, asof=None):
    """기초 연도 수치를 SEC에서 모은다. 전부 최근 12개월(TTM) 기준이다."""
    cik = feh.CIKS[ticker]
    out = {}

    def ttm(tags):
        tag, rows = bmh.pick_tag(cik, tags)
        if not rows:
            return None
        return latest(bmh.ttm_series(bmh.quarterly_flow(rows, ticker)), asof)

    out["revenue"] = ttm(bmh.FLOW_TAGS["revenue"])
    out["opinc"] = ttm(bmh.EBITDA_TAGS["opinc"])
    _, dda_series = bmh.dda_ttm(cik, ticker)
    out["dda"] = latest(dda_series, asof) if dda_series else None
    out["capex"] = ttm(bmh.FLOW_TAGS["capex"])
    # 금융리스로 취득한 자산은 현금 설비투자에 안 잡힌다. 부채는 순부채에서
    # 차감하면서 그 부채가 산 자산의 취득은 투자로 세지 않으면 앞뒤가 안 맞는다.
    # MSFT는 TTM $24.6B로 주당 약 $7이다(Fable 계산).
    fl_capex = ttm(["RightOfUseAssetObtainedInExchangeForFinanceLeaseLiability"])
    out["capex_finance_lease"] = fl_capex or 0
    if fl_capex:
        out["capex"] = (out["capex"] or 0) + fl_capex
    # 인수 대금 — 한계 매출/자본(현금흐름 기준)의 재투자에 넣는다. 인수로 산 매출도 자본이 든다.
    # 태그가 끊긴 회사는 마지막 TTM이 몇 년 전 값이다(INTC: 2017년 Mobileye $14.5B가 "최근 1년"으로 쓰였다, Fable 2026-09-29).
    # 매출 TTM보다 200일 넘게 뒤처진 인수 대금은 최근 인수가 없던 것으로 보고 0으로 둔다(EV 구성요소 신선도 규칙과 같은 문턱).
    def ttm_fresh(tags, ref_tags):
        _, rows = bmh.pick_tag(cik, tags)
        _, rrows = bmh.pick_tag(cik, ref_tags)
        if not rows or not rrows:
            return None
        s = [e for e in bmh.ttm_series(bmh.quarterly_flow(rows, ticker)) if asof is None or e.get("available", e["end"]) <= asof]
        r = [e for e in bmh.ttm_series(bmh.quarterly_flow(rrows, ticker)) if asof is None or e.get("available", e["end"]) <= asof]
        if not s or not r:
            return None
        if (date.fromisoformat(r[-1]["end"]) - date.fromisoformat(s[-1]["end"])).days > 200:
            return None
        return s[-1]["val"]
    out["acquisitions"] = ttm_fresh(["PaymentsToAcquireBusinessesNetOfCashAcquired"], bmh.FLOW_TAGS["revenue"]) or 0
    out["tax"] = ttm(["IncomeTaxExpenseBenefit"])
    # 회사가 밝힌 일회성 법인세 항목은 세율에서 뺀다(v2/tax_oneoff.json, META). 같은 시점의 TTM 결산일 기준.
    _, trows = bmh.pick_tag(cik, ["IncomeTaxExpenseBenefit"])
    tser = [e for e in bmh.ttm_series(bmh.quarterly_flow(trows, ticker)) if asof is None or e["available"] <= asof] if trows else []
    if out["tax"] is not None and tser:
        out["tax"] -= bmh.oneoff_in_ttm(ticker, tser[-1]["end"], "tax", asof)
    # 세전이익도 매출보다 200일 넘게 뒤처지면 쓰지 않는다 — ORCL은 표준 태그가 2018-08에서 멈춰 2018년 TTM($12.8B)이
    # "최근 4분기"로 쓰였다(2026-10-01). 커밋된 카드 중 이 규칙에 걸리는 종목은 ORCL뿐이다(PG는 태그가 원래 없음).
    out["pretax"] = ttm_fresh(["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                               "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
                              bmh.FLOW_TAGS["revenue"])
    if cik in PRETAX_FROM_NI_TAX:
        # 세전이익을 표준 태그로 내지 않는 회사는 순이익 + 법인세로 만든다(ORCL Q1 FY27: 4,760 + 847 = 10-Q 5,607).
        ni_ttm, tx_ttm = ttm_fresh(["NetIncomeLoss"], bmh.FLOW_TAGS["revenue"]), ttm_fresh(["IncomeTaxExpenseBenefit"], bmh.FLOW_TAGS["revenue"])
        out["pretax"] = ni_ttm + tx_ttm if ni_ttm is not None and tx_ttm is not None else None

    # 비과세 일회성 세전 이익(tax_oneoff.json pretax — GEV Prolec 재평가 $3,992M)은 세율 분모에서 뺀다(본업 이익 세율과 같게, 2026-10-04)
    if out["pretax"] is not None and tser:
        out["pretax"] -= bmh.oneoff_in_ttm(ticker, tser[-1]["end"], "pretax", asof)

    for name, tags in bmh.EV_COMPONENTS.items():
        # asof를 빠뜨리면 과거 시점 계산에 오늘 대차대조표가 섞인다
        # (현금·단기투자·차입금·리스가 그랬다 — Codex 지적으로 발견).
        out[name] = latest(bmh.ev_component(cik, name, tags), asof)
    # 금융리스부채는 운용리스와 별개 태그라 EV_COMPONENTS["lease"]에 안 잡힌다.
    # MSFT는 $66.6B가 순부채에서 통째로 빠져 있었다(주당 약 $9).
    # 총계 태그가 있으면 그것만 쓴다. 셋을 모두 더하면 총계와 세부가 겹쳐
    # 금융리스가 두 배로 잡히는 회사가 나온다(Codex 지적).
    # 총계 태그가 세부(유동 + 비유동)보다 오래된 결산일에 멈췄으면 세부를 쓴다 — TMUS는 총계를 10-K에만 내
    # 2026-06-30에도 2025-12-31 $2,270M이 쓰였다(10-Q 세부 $1,178M + $1,121M = $2,299M, Codex, 2026-10-01).
    def _last_end(rows):
        ok = [e for e in rows if asof is None or e.get("available", e.get("end")) <= asof]
        return ok[-1]["end"] if ok else ""
    _fl_tot = bmh.component_sum(cik, ["FinanceLeaseLiability"])
    _fl_parts = bmh.component_sum(cik, ["FinanceLeaseLiabilityCurrent", "FinanceLeaseLiabilityNoncurrent"])
    fin_lease = latest(_fl_tot, asof)
    if not fin_lease or _last_end(_fl_parts) > _last_end(_fl_tot):
        fin_lease = latest(_fl_parts, asof) or fin_lease
    fin_lease = fin_lease or 0
    # 총차입금 태그를 지정한 회사(bmh.DEBT_TOTAL_TAG, MU = DebtAndCapitalLeaseObligations)는 금융리스가
    # 차입금에 이미 들어 있다 — 리스에 또 더하면 두 번 뺀다(MU 2026-05 $2.67B, 2026-09-26).
    # 합계 태그가 금융리스를 포함하는지는 태그 이름으로 가른다(LLY의 DebtCurrent+LongTermDebtNoncurrent는 불포함 — Fable).
    _tt = bmh.DEBT_TOTAL_TAG.get(cik)
    # 목록이면 태그 중 하나라도 CapitalLease를 담으면 포함으로 본다 — XOM의 LongTermDebtAndCapitalLeaseObligations는
    # 금융리스를 담는데 목록이라 빠져 금융리스 $2.66B가 두 번 빠졌다(Fable, 2026-09-29).
    _flat = [x for t in ([_tt] if isinstance(_tt, str) else (_tt or [])) for x in (t if isinstance(t, tuple) else (t,))]   # 튜플 묶음(KO)도 펼친다
    # DE: 장비 부문 차입금(보충 표 원문, 회사 고유 이름)은 금융리스를 이미 담는다(10-K 주석 24) — 이름으로 못 가려 목록에 둔다(Codex, 2026-10-01)
    # MCD: 재무상태표 리스부채(OperatingLeaseLiabilityCurrent·Noncurrent 태그)가 운용 + 금융리스 합계라(10-K 리스 주석 표, 2025-12 $694M·$14,147M)
    # 금융리스를 또 더하면 $2.35B가 두 번 빠진다(2026-10-02) — 같은 목록에 둔다.
    fl_in_debt = any("CapitalLease" in t or "FinanceLease" in t for t in _flat) or cik in ("0000315189", "0000063908")   # DE(장비 부문 차입금에 금융리스 포함)·MCD(리스 태그가 운용 + 금융 합계)
    # 운용리스(B16, 2026-10-03 사용자 결정): US GAAP 영업이익은 운용리스 비용(임차료)을 이미 뺐다. 그 부채를 순부채로 또 빼고
    # 투하자본에 넣으면 같은 비용이 두 번 든다(Codex·Fable DCF 검증). DCF는 운용리스를 영업비용으로 일관되게 보고
    # run_dcf·invested_capital에서 op_lease를 뺀다. "lease"는 총리스 그대로 둔다(카드 문장의 순차입금 표시가 쓴다).
    # MCD는 운용리스 태그가 금융리스 합계라 금융리스분을 뺀다. IFRS 16 회사(TSM·SKHY)는 리스 비용이 감가상각 + 이자라
    # 영업이익이 임차료를 빼지 않았으므로 리스를 빚으로 두는 지금 처리가 맞다 — 0.
    op_lease = out.get("lease") or 0
    if cik == "0000063908":
        op_lease = max(op_lease - fin_lease, 0)
    out["op_lease"] = 0 if ticker in IFRS_LEASE else op_lease
    if not fl_in_debt:
        out["lease"] = (out.get("lease") or 0) + fin_lease
    out["finance_lease"] = fin_lease

    _, srows = bmh.pick_tag(cik, ["CommonStockSharesOutstanding"], "us-gaap")
    _, drows = bmh.pick_tag(cik, ["EntityCommonStockSharesOutstanding"], "dei")
    out["shares"] = latest(bmh.instant_series(srows + drows, ticker, is_share_count=True), asof)

    # 지배주주 자본 태그가 멈추고 비지배지분 포함 총계만 내는 회사가 있다. AVGO는
    # StockholdersEquity가 2019-11($24.9B)에서 끝나고 그 뒤로는 포함 총계만 낸다
    # (2026-08 $99.7B). 멈춘 값을 쓰면 투하자본이 $75B 작게 잡혀 매출/자본이 부풀었다(2026-09-25).
    # 그 시점에 공개된 두 계열의 마지막 결산일을 비교해 총계가 200일 넘게 앞서면 총계 − 비지배지분.
    se_rows = bmh.component_sum(cik, ["StockholdersEquity"])
    incl_rows = bmh.component_sum(cik, ["StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"])

    def _last(series):
        r = [e for e in series if asof is None or e.get("available", e.get("end")) <= asof]
        return r[-1] if r else None

    se_last, incl_last = _last(se_rows), _last(incl_rows)
    if incl_last and (not se_last or (date.fromisoformat(incl_last["end"])
                                      - date.fromisoformat(se_last["end"])).days > 200):
        out["equity"] = incl_last["val"] - (out.get("nci") or 0)
        eq_rows = incl_rows
    else:
        out["equity"] = se_last["val"] if se_last else None
        eq_rows = se_rows
    # 비영업 투자자산 — 영업에 쓰이지 않는 지분·장기투자
    # Apple은 장기 채권 투자를 LongTermInvestments가 아니라 MarketableSecuritiesNoncurrent로
    # 보고한다(2026-06-27 $84.1B). 이 태그를 안 보면 그 자산이 주주가치에서 통째로 빠진다.
    # 그 태그를 예전에 쓰다 그만둔 회사(AMD 2014년 값 등)의 낡은 값을 집지 않도록,
    # 그 시점(asof)에 공개돼 있던 자기자본보다 200일 넘게 뒤처진 값은 버린다.
    # 판정은 반드시 asof 시점 기준이다. 전체 계열의 마지막 날짜로 판정하면 나중에 태그를
    # 그만둔 사실이 과거 계산에서 그때 유효했던 값까지 지운다(Codex 지적, 2026-09-24).
    def as_of_rows(series):
        if asof is None:
            return series
        return [e for e in series if e.get("available", e.get("end")) <= asof]

    def fresh_latest(series):
        s, eq = as_of_rows(series), as_of_rows(eq_rows)
        if not s:
            return None
        if eq and (date.fromisoformat(eq[-1]["end"]) - date.fromisoformat(s[-1]["end"])).days > 200:
            return None
        return s[-1]["val"]

    # 순현금 표시(build_fundamental_score.net_cash)가 채권성 장기투자만 따로 쓰므로 분리해 둔다.
    # MU는 같은 자산(10-Q "Long-term marketable investments", 2026-05 $4,106M)을 매도가능 채권 태그로만 낸다.
    # 앞 태그가 없거나 낡았을 때만 쓴다(AAPL은 앞 태그가 있어 불변 — Codex 지적, 2026-09-26).
    out["lt_marketable"] = (fresh_latest(bmh.component_sum(cik, ["MarketableSecuritiesNoncurrent"]))
                            or fresh_latest(bmh.component_sum(cik, ["AvailableForSaleSecuritiesDebtSecuritiesNoncurrent"])) or 0)
    # Alphabet은 비상장 지분을 OtherLongTermInvestments("Non-marketable securities",
    # 2026-06-30 $131.5B)로 보고한다. 모든 태그에 같은 신선도 필터를 건다 — 필터가 없던
    # 동안 GOOGL은 2025-09-30에 끊긴 EquitySecuritiesFvNi $7.1B를 계속 쓰고 있었다(2026-09-24).
    # 장기투자 태그(LongTermInvestments·OtherLongTermInvestments)는 지분증권을 포함해 보고하는
    # 경우가 많다. 둘 다 더하면 같은 자산이 두 번 들어가므로(Codex 지적), 장기투자 태그가
    # 있으면 그것만, 없을 때만 EquitySecuritiesFvNi를 쓴다. NVDA는 FvNi만, GOOGL은 OtherLTI만.
    lti_vals = [fresh_latest(bmh.component_sum(cik, [tag]))
                for tag in ("LongTermInvestments", "OtherLongTermInvestments")]
    # 장기투자 태그가 없으면 지분증권을 두 갈래로 더한다 — 공정가치 지분(FvNi)과 **시가 없는
    # 비상장 지분**(측정 대안, EquitySecuritiesWithoutReadilyDeterminableFairValueAmount).
    # AMZN은 비상장 지분 $122.3B가 이 태그뿐이라 주주가치에서 통째로 빠졌고, NVDA도 $47.9B가
    # 빠져 있었다(2026-09-24 사용자 결정으로 포함, NVDA 갱신). GOOGL·MSFT는 장기투자 태그 안에
    # 같은 자산이 있어 그쪽만 쓴다(이중계상 방지).
    equity_vals = [fresh_latest(bmh.component_sum(cik, [tag]))
                   for tag in ("EquitySecuritiesFvNi", "EquitySecuritiesWithoutReadilyDeterminableFairValueAmount")]
    # 존재는 None으로 판정한다 — 장기투자 값이 정상적인 0이어도 지분 태그로 넘어가면 안 된다(Codex 2차).
    has_lti = any(v is not None for v in lti_vals)
    out["nonop_assets"] = (sum(v or 0 for v in lti_vals) if has_lti
                           else sum(v or 0 for v in equity_vals)) + out["lt_marketable"]
    # 투자 수익을 매출·영업이익에 넣는 회사(보험 — UNH "Investment and other income")는 그 투자가 영업 자산이다.
    # 비영업 자산으로 또 더하면 수익을 두 번 센다(2026-09-30 사용자 결정 "장기투자는 빼고 현금은 두기").
    # 투하자본 계산에서도 영업 자산으로 남는다. 현금·단기투자는 다른 회사처럼 순현금에 둔다.
    if cik in INVESTMENTS_OPERATING:
        out["nonop_assets"] = 0.0
    # 종목 지정 비영업자산(v2/nonop_extra.json). 같은 태그가 회사마다 다른 자산을 담아
    # (AvailableForSaleSecuritiesDebtSecurities는 흔히 단기 시장성 채권 전체다) 일괄 적용하면
    # 현금·단기투자와 겹친다. 10-Q 주석으로 확인한 종목만 목록에 올린다(AMZN Anthropic 전환사채).
    extra_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nonop_extra.json")
    extra = json.load(open(extra_path)).get(ticker, []) if os.path.exists(extra_path) else []
    out["nonop_extra"] = sum(fresh_latest(bmh.component_sum(cik, [x["tag"]])) or 0 for x in extra if "tag" in x)
    # 표준 태그가 없는 자산은 10-Q 값으로 적는다({"value", "end", "filed"}). 공시일 이전 시점에는 쓰지 않고,
    # 더 새 값이 있으면 그것만 쓴다(같은 "name"끼리). TSLA SpaceX 지분·비트코인(2026-09-25).
    fixed = {}
    for x in extra:
        if "value" in x and (asof is None or x["filed"] <= asof):
            if x["name"] not in fixed or x["end"] > fixed[x["name"]]["end"]:
                fixed[x["name"]] = x
    out["nonop_extra"] += sum(x["value"] for x in fixed.values())
    out["nonop_assets"] += out["nonop_extra"]
    # 이미 단기투자에 든 태그(META 상장주식 — 10-Q 공정가치 표의 시장성 증권 합계 안)는 뺀다
    excluded = {x["exclude"] for x in extra if "exclude" in x}
    if "EquitySecuritiesFvNi" in excluded and not has_lti:
        out["nonop_assets"] -= equity_vals[0] or 0

    # 운전자본은 재고·매출채권처럼 영업에 묶인 돈만 본다. 현금과 차입금은 뺀다
    # (그 둘은 순부채 쪽에서 따로 계산되므로 여기 넣으면 두 번 센다).
    ac = latest(bmh.component_sum(cik, ["AssetsCurrent"]), asof)
    lc = latest(bmh.component_sum(cik, ["LiabilitiesCurrent"]), asof)
    if ac and lc:
        cash = (out.get("cash") or 0) + (out.get("sti") or 0)
        st_debt = current_debt(cik, asof)
        # 유동자산에는 상장주식 같은 투자자산도 들어 있다. 영업에 묶인 돈이
        # 아니므로 운전자본에서 뺀다. NVDA는 EquitySecuritiesFvNi $42.8B가
        # 섞여 운전자본이 매출의 32.6%로 잡혔다(실제 18.5% 수준).
        invest_assets = 0 if "EquitySecuritiesFvNi" in excluded else (
            latest(bmh.component_sum(cik, ["EquitySecuritiesFvNi"]), asof) or 0)
        out["invest_assets"] = invest_assets
        out["nwc"] = (ac - cash - invest_assets) - (lc - st_debt)
        _ac = [e for e in bmh.component_sum(cik, ["AssetsCurrent"]) if e.get("available", e["end"]) <= (asof or "9999")]
        out["nwc_end"] = _ac[-1]["end"] if _ac else None
    out["ticker"], out["asof"] = ticker, asof   # 한계 매출/자본 계산용(scenarios)

    # ── 데이터 품질(2026-09-25 사용자 결정) — 유니버스 427종목 중 34%가 아래 신호 하나 이상 ──
    out["dq"] = []
    # 주식 수: 표지·재무상태표 값이 없거나 희석 가중평균(분할 보정)의 0.5~2배 밖이면 희석 가중평균으로.
    # SPG는 한 클래스만 잡혀 8,000주로 주당 $6,834가 나왔다.
    import splits as _splits
    _, wrows = bmh.pick_tag(cik, ["WeightedAverageNumberOfDilutedSharesOutstanding"])
    wq = sorted([e for e in wrows if "start" in e and e.get("filed") and (asof is None or e["filed"] <= asof)
                 and 80 <= (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days <= 100],
                key=lambda e: (e["end"], e["filed"])) if wrows else []
    if wq:
        wd = wq[-1]["val"] * feh.split_ratio(wq[-1]["filed"], _splits.for_ticker(ticker))
        # 희석 가중평균을 백만 주 단위 숫자로 잘못 태깅한 회사(MCD 2026년 "711.1"주)는 대조값으로 쓸 수 없다 — 백만 배로 되돌린다
        # (100만 주 미만은 S&P500 기업으로 불가능). 그대로 두면 표지 주식 수 7.08억 주를 711주로 바꿔 주당 가치가 9천만 달러가 됐다(2026-10-02).
        if wd < 1e6:
            out["dq"].append(f"weighted_shares_unit:{wq[-1]['val']}->x1e6")
            wd *= 1e6
        sh = out.get("shares")
        if not sh or not (0.5 <= sh / wd <= 2.0):
            out["dq"].append(f"shares_fallback:{sh}->{wd:.0f}")
            out["shares"] = wd
    elif not out.get("shares") or out["shares"] < 1e7:
        # 대조할 희석 가중평균도 없는데 주식 수가 없거나 1,000만 주 미만(S&P500 기업으로는 불가능)이면
        # 계산하지 않는다(SPG는 2013년 이후 주식 수를 표준 태그로 내지 않아 8,000주가 잡혔다).
        out["dq"].append(f"shares_missing:{out.get('shares')}")
        out["shares"] = None
    # Up-C 구조(지주회사 주식 + 교환 가능한 파트너십 지분)는 영업이익 전체를 쓰므로 주식 수를 회사가 밝힌 경제적 전체 주식 수
    # (보통주·파트너십 지분, 미가득 참여분 포함 — BX "Distributable Earnings Shares Outstanding")로 바꾼다. 그대로 두면 BX는
    # Blackstone Holdings 지분(이익의 약 43%) 몫까지 Class A 7.5억 주에 몰려 주당 가치가 약 1.66배가 됐다(2026-10-02, Codex 1차 반영).
    if ticker in ECON_SHARES and out.get("shares"):
        rows = sorted(ECON_SHARES[ticker], key=lambda x: x["end"])
        ok = [x for x in rows if asof is None or x["filed"] <= asof]
        u = (ok[-1] if ok else rows[0])["value"]   # 공시 전 시점은 가장 이른 값(2024-09-30, 이후 값과 1% 안쪽)
        out["dq"].append(f"econ_shares:{out['shares']:.0f}->{u}")
        out["shares"] = u
    # 차입금: 최근 4분기 이자비용 ÷ 차입금이 15%를 넘거나, 이자비용이 $1억 넘는데 차입금이 0이면
    # 차입금이 빠졌을 가능성(회사 자체 태그 — CMCSA 장기차입금). 고치지 않고 표시만 한다(검증 패널 제외).
    interest = ttm(["InterestExpense", "InterestExpenseNonoperating", "InterestExpenseDebt"])
    debt_all = (out.get("debt") or 0)
    if interest and interest > 1e8 and (debt_all <= 0 or interest / debt_all > 0.15):
        out["dq"].append(f"debt_suspect:interest={interest / 1e9:.2f}B,debt={debt_all / 1e9:.2f}B")
    if effective_tax(out) != (out["tax"] / out["pretax"] if out.get("tax") is not None and out.get("pretax") else None):
        out["dq"].append("tax_fallback")
    return out


# 세전이익을 표준 태그로 내지 않는 회사(CIK) — 순이익 + 법인세로 만든다. ORCL은 2018-08 뒤로 회사 고유 태그만 쓴다.
# MRVL: 세전이익을 연간에만 태그해 분기 TTM이 없다 → 순이익 + 법인세(2026-10-01, 본업 기준 PER·순이익률·DCF 세율)
PRETAX_FROM_NI_TAX = {"0001341439", "0001835632"}


S2C_MAX = 10.0   # 매출/자본 상한 — 자본을 거의 안 쓰는 회사의 발산 방지


IFRS_LEASE = {"TSM", "SKHY"}     # IFRS 16 — 리스 비용이 영업이익 밖이라 리스부채는 빚(B16)


CURRENT_DEBT_FRESH_DAYS = 200
# 단기차입(ShortTermBorrowings) 태그가 유동 장기차입을 이미 담은 합계인 회사 — 같은 결산일 두 값이 2% 안(Fable 감사 2026-10-03).
# IBM(5.775 대 5.772)·PM·DVN·LITE·DOV·COO·HWM·APTV. 숫자가 비슷하다는 것만으로 일반화하지 않는다(Codex — 우연히 같을 수 있음).
STB_INCLUDES_CURRENT_LTD = {"0000051143", "0001413329", "0001090012", "0001633978", "0000029905", "0000711404", "0000004281", "0001521332"}


def current_debt(cik, asof):
    """운전자본에서 되돌릴 유동 차입(B17, 2026-10-03 사용자 결정 — 사전 등록 V1).

    예전에는 `LongTermDebtCurrent`(장기차입금 1년 내 만기분) 하나만 되돌려, 기업어음·단기차입·유동 금융리스가 늘면 운전자본이
    줄고 순투자가 작게 잡혔다(Codex). 유동자산 결산일(`AssetsCurrent`)을 기준으로 두 후보를 만든다.
      A = DebtCurrent(유동 차입 합계 — 유동 금융리스 포함)
      B = 유동 장기차입(LongTermDebtAndCapitalLeaseObligationsCurrent, 없으면 LongTermDebtCurrent)
          + 단기차입(ShortTermBorrowings, 없으면 CommercialPaper) + 유동 금융리스(합계 태그를 안 쓴 경우만)
    각 태그는 그 결산일 값, 없으면 결산일 이전 200일 안의 마지막 값(연말에만 공시하는 회사 — MCD). **결산일이 더 최근인 후보가
    이기고**(이어 쓴 옛 값이 같은 결산일 값을 이기지 않게 — Fable: VZ 2025-12 $18.6B 대 2026-06 $21.8B), 결산일이 같으면 큰 쪽.
    B의 결산일은 구성요소 중 가장 오래된 것으로 본다. 단기차입이 유동 장기차입을 이미 담은 회사(IBM·BMY)는 더하지 않는다.
    한계: 유동부채(LiabilitiesCurrent)는 base_inputs가 따로 latest로 고른다 — 유동자산과 결산일이 다를 수 있다(카드에서는 일치 확인).
    """
    ac_rows = [e for e in bmh.component_sum(cik, ["AssetsCurrent"]) if e.get("available", e["end"]) <= (asof or "9999")]
    if not ac_rows:
        return 0
    end = ac_rows[-1]["end"]

    def pick(tag):
        rows = [e for e in bmh.component_sum(cik, [tag]) if e.get("available", e["end"]) <= (asof or "9999")
                and e["end"] <= end and (date.fromisoformat(end) - date.fromisoformat(e["end"])).days <= CURRENT_DEBT_FRESH_DAYS]
        if not rows:
            return None
        r = sorted(rows, key=lambda e: (e["end"], e.get("available", "")))[-1]
        return r["end"], r["val"]

    def fresher(a, b):      # 결산일이 더 최근인 쪽, 같으면 a
        if a is None:
            return b
        if b is None:
            return a
        return a if a[0] >= b[0] else b

    A = pick("DebtCurrent")
    comb, ltd = pick("LongTermDebtAndCapitalLeaseObligationsCurrent"), pick("LongTermDebtCurrent")
    lt = fresher(comb, ltd)
    _stb, _cp = pick("ShortTermBorrowings"), pick("CommercialPaper")
    stb = fresher(_stb, _cp)
    stb_is_tag = stb is not None and stb is _stb        # 기업어음은 합계 태그가 될 수 없다 — "포함" 판단은 ShortTermBorrowings일 때만(Fable: PH 우연 일치)
    same = lambda x, y: x and y and x[0] == y[0] and abs(x[1] - y[1]) <= 0.02 * max(abs(x[1]), abs(y[1]), 1)
    # 단기차입 태그가 이미 유동 장기차입을 담은 합계인 회사가 있다(Fable 감사 2026-10-03). 같은 결산일에 유동 차입 합계(DebtCurrent)와
    # 같으면(BMY $1.027B) 합계로 본다 — 그 합계는 유동 금융리스까지 담는다. 유동 장기차입과만 비슷한 경우는 우연일 수 있어(Codex) 감사로
    # 확인한 회사만 명단(STB_INCLUDES_CURRENT_LTD)으로 처리한다.
    by_total = stb_is_tag and same(stb, A)
    inclusive = by_total or (stb_is_tag and cik in STB_INCLUDES_CURRENT_LTD and lt is not None)
    parts = [x for x in (lt, stb) if x]
    B = None
    if parts:
        B_val = max(x[1] for x in parts) if inclusive else sum(x[1] for x in parts)
        B_end = min(x[0] for x in parts)       # 가장 오래된 구성요소의 결산일로 비교 — 이어 쓴 옛 값이 같은 결산일 합계(A)를 이기지 않게(Codex)
    if (lt is not comb or comb is None) and not by_total:
        fl = pick("FinanceLeaseLiabilityCurrent")       # 금융리스만 있는 회사(REGN)도 넣는다
        if fl:
            B_val = (B_val if parts else 0) + fl[1]
            B_end = min(B_end, fl[0]) if parts else fl[0]
            parts = parts + [fl]
    if parts:
        B = (B_end, B_val)
    if A is None and B is None:
        return 0
    if A is None or B is None:
        return (A or B)[1]
    if A[0] != B[0]:
        return (A if A[0] > B[0] else B)[1]
    return max(A[1], B[1])


def invested_capital(base):
    """영업에 묶인 투하자본 = 자기자본 + 차입금 + 리스 − 현금·단기투자 − 비영업자산.

    운용리스(op_lease)는 뺀다 — 영업이익이 임차료를 이미 뺐으므로 사용권자산도 투하자본에 넣지 않는다(B16)."""
    return ((base.get("equity") or 0) + (base.get("debt") or 0) + (base.get("lease") or 0) - (base.get("op_lease") or 0)
            - (base.get("cash") or 0) - (base.get("sti") or 0) - (base.get("nonop_assets") or 0))


# 본국 법정세율. 실효세율이 뜻을 잃을 때(세전이익 ≤ 0, 0~40% 밖) 대신 쓴다(2026-09-25 사용자 결정).
STATUTORY_TAX = {"TSM": 0.20}
TERMINAL_STATUTORY = True   # 예측기간 세율을 법정세율로 수렴, 잔존은 법정세율(2단계, 2026-09-25)
TAX_OK = (0.0, 0.40)


def effective_tax(base):
    """최근 4분기 실효세율. 세전이익이 0 이하이거나 세율이 0~40% 밖이면 본국 법정세율.

    TRMB는 세전이익이 약 0이라 세율이 음수가 되어 세후 영업이익이 부풀었다(유니버스 55곳, 2026-09-25)."""
    tax, pre = base.get("tax"), base.get("pretax")
    if tax is not None and pre and pre > 0 and TAX_OK[0] <= tax / pre <= TAX_OK[1]:
        return tax / pre
    return STATUTORY_TAX.get(base.get("ticker"), 0.21)


# 경제적 전체 주식 수(분기 실적 보도자료 "Distributable Earnings Shares Outstanding" = 참여 보통주 + 참여 파트너십 지분, 분기 말).
ECON_SHARES = {"BX": [{"end": "2024-09-30", "value": 1221580941, "filed": "2024-10-17"},
                      {"end": "2024-12-31", "value": 1221171137, "filed": "2025-01-30"},
                      {"end": "2025-03-31", "value": 1221507649, "filed": "2025-04-17"},
                      {"end": "2025-06-30", "value": 1230142232, "filed": "2025-07-24"},
                      {"end": "2025-09-30", "value": 1229184102, "filed": "2025-10-23"},
                      {"end": "2025-12-31", "value": 1228769322, "filed": "2026-01-29"},
                      {"end": "2026-03-31", "value": 1230169747, "filed": "2026-04-23"},
                      {"end": "2026-06-30", "value": 1243813031, "filed": "2026-07-23"}]}


def run_dcf(base, growth, wacc, terminal, exit_mult, years=5,
            margin_path=None, s2c=None, tax_rate=None, roic_fade=0.5):
    """무차입 DCF — **매출/자본 비율(sales-to-capital)** 재투자 (2026-09-24 사용자 결정).

    FCF = NOPAT − 재투자,  NOPAT = 매출 × 영업이익률 × (1 − 세율),
    재투자 = 그 해 매출 증가분 ÷ 매출/자본 비율.

    예전 구조(설비투자 비율을 감가상각 수준으로 5년에 걸쳐 내리고, 감가상각은 투자를
    따라 올리고, EBITDA 마진은 고정)에는 두 결함이 있었다.
      1. 투자 비용(늘어난 상각)은 영업이익을 깎는데 그 투자가 버는 이익은 0이었다.
         AMZN "현재 마진 유지" 시나리오의 영업이익률이 12.1% → 7~10%로 떨어져 카드 문구와
         계산이 어긋났다(MSFT 46.8% → 38~43%).
      2. 영업이익률만 고정하면(중간 시도) 반대로 상각이 늘수록 현금이 남고, 4~5년차 순투자가
         음수가 되는 이음새가 생겼다(Fable·재계산 확인: AMZN −$19B, MSFT −$21B).
    성장을 자본으로 "사게" 하면 새 자본이 마진을 버는 것이 가정이 아니라 구조가 되고,
    잔존 재투자율 g/ROIC와 같은 식(한계 ROIC = 영업이익률 × (1−세율) × 매출/자본)이라
    이음새가 없다. 설비투자·감가상각·운전자본은 투하자본 안에 함께 들어 있어 따로 두지 않는다.

    `s2c`를 비우면 매출 ÷ 현재 투하자본(이력 평균 효율)을 쓴다.
    """
    rev0 = base["revenue"]
    margin0 = base["opinc"] / rev0
    # 세율 경로(2026-09-25 사용자 결정, 다모다란): 예측기간은 실효세율에서 법정세율로 선형 수렴하고
    # 잔존은 법정세율. 실효세율(AVGO 5%)이 잔존가치에 영구히 들어가던 문제를 막는다.
    # 세율을 직접 넘기면(tax_rate=) 경로 없이 그 값 하나를 쓴다.
    if tax_rate is None:
        t0 = effective_tax(base)
        t_stat = STATUTORY_TAX.get(base.get("ticker"), 0.21) if TERMINAL_STATUTORY else t0
        tax_path = [t0 + (t_stat - t0) * i / (years - 1) for i in range(years)] if years > 1 else [t_stat]
        tax_rate, tax_term = t0, t_stat
    else:
        tax_path, tax_term = [tax_rate] * years, tax_rate
    margins = margin_path or [margin0] * years
    invested = invested_capital(base)
    if s2c is None:
        # 투하자본이 0에 가깝거나 음수(순현금·비영업자산이 자본보다 큼)면 비율이 무한대로
        # 튄다. 상한 S2C_MAX로 막는다 — 0 경계 양쪽에서 값이 이어지게(Codex: 투하자본
        # 0.001→0에 가치가 78→−5로 뒤집히던 폴백 1.0을 대체). AAPL이 7.9로 가장 높다.
        s2c = min(rev0 / invested, S2C_MAX) if invested > 0 else S2C_MAX
    # 연도별 경로도 받는다(기본 시나리오: 최근 효율 → 평균). 잔존은 마지막 해 값을 쓴다.
    s2c_path = list(s2c) if isinstance(s2c, (list, tuple)) else [s2c] * years

    rows, rev = [], rev0
    for i in range(years):
        new_rev = rev * (1 + growth[i])
        ebit = new_rev * margins[i]
        nopat = ebit * (1 - tax_path[i])
        if REINVEST_LEAD:
            # 올해 투자가 **다음 해** 매출 증가를 만든다(잔존 고든 공식과 같은 시점 규약). 같은 해로 두면
            # ROIC = 할인율인데도 성장이 가치를 만든다 — 사전 등록 엔진 단위검정 ①에서 성장 30%에 +31%(2026-09-26).
            g_next = growth[i + 1] if i + 1 < years else terminal
            reinvest = new_rev * g_next / s2c_path[i]
        else:
            reinvest = (new_rev - rev) / s2c_path[i]
        fcf = nopat - reinvest
        rev = new_rev
        # 기중 할인(Dechra 모델과 같은 0.5년 관행)
        disc = 1 / (1 + wacc) ** (i + 0.5)
        rows.append({"year": i + 1, "revenue": rev, "ebit": ebit, "nopat": nopat,
                     "reinvest": reinvest, "fcf": fcf, "pv": fcf * disc})

    pv_sum = sum(r["pv"] for r in rows)
    if REINVEST_LEAD:
        # 1년차 매출 증가를 만들 투자는 지금(0년) 들어간다 — 빠뜨리면 첫해 성장이 공짜가 된다.
        # 기중 할인 규약에서 i년차 흐름은 i−0.5 시점이므로, 1년차 성장을 위한 투자는 −0.5 시점이다.
        reinvest0 = rev0 * growth[0] / s2c_path[0]
        pv_sum -= reinvest0 * (1 + wacc) ** 0.5
    last = rows[-1]

    # 잔존: 재투자율 = 영구성장률 / ROIC. 예측기간의 한계 ROIC는 마진 × (1−세율) × 매출/자본이고,
    # 잔존에서는 경쟁이 초과수익을 깎으므로 할인율 쪽으로 절반 수렴시킨다(roic_fade).
    # NVDA는 현재 ROIC가 78.5%라 그대로 두면 잔존 FCF가 NOPAT의 96.8%가 되고, 이 가정 하나가
    # 주당 $54를 만든다(검증에서 확인).
    roic = margins[-1] * (1 - tax_term) * s2c_path[-1]
    roic_t = wacc + (roic - wacc) * roic_fade if roic > wacc else roic
    # ROIC가 영구성장률 이하면 성장이 가치를 만들지 못한다 — 재투자율을 1로 두어 잔존 현금흐름이 0.
    reinvest_rate = min(max(terminal / roic_t, 0.0), 1.0) if roic_t > terminal else 1.0
    nopat_t = last["revenue"] * (1 + terminal) * margins[-1] * (1 - tax_term)
    fcf_t = nopat_t * (1 - reinvest_rate)

    tv_ggm = fcf_t / (wacc - terminal) if wacc > terminal else float("nan")
    # 예측기간 현금흐름을 기중(i+0.5)으로 할인하므로 잔존가치도 같은 기준으로 맞춘다.
    pv_ggm = tv_ggm / (1 + wacc) ** (years - 0.5)
    # 출구배수는 참고용이다(영업이익 배수). **영구성장 하나만 쓴다** — 두 방법을 평균내지
    # 않는다(2026-09-20 결정). exit_mult=0이면 예측기간 현재가치다.
    ev_exit = pv_sum + last["ebit"] * exit_mult / (1 + wacc) ** (years - 0.5)
    ev = pv_sum + pv_ggm

    net_debt = ((base.get("debt") or 0) + (base.get("lease") or 0) - (base.get("op_lease") or 0)   # 운용리스는 영업비용(B16)
                - (base.get("cash") or 0) - (base.get("sti") or 0))
    equity = (ev - net_debt - (base.get("nci") or 0) - (base.get("preferred") or 0)
              + (base.get("nonop_assets") or 0))
    return {"rows": rows, "pv_sum": pv_sum, "ev_ggm": ev, "ev_exit": ev_exit, "fcf_terminal": fcf_t,
            "ev": ev, "net_debt": net_debt, "equity": equity,
            "per_share": (equity / base["shares"]) if base.get("shares") else None, "tax_rate": tax_rate,
            "tax_terminal": tax_term,
            "margin0": margin0, "s2c": s2c_path[-1], "s2c_path": s2c_path, "invested": invested,
            "roic": roic, "roic_terminal": roic_t, "reinvest_rate": reinvest_rate}


def history(ticker, asof=None, window_start=None):
    """성장률·마진 이력을 SEC에서 뽑는다. 시나리오 가정의 출처다.

    사람이 성장률을 고르면 그게 답을 정하므로(순방향 DCF의 근본 문제),
    가정은 회사 자신의 실적 이력에서만 만든다.
    """
    cik = feh.CIKS[ticker]

    def ttm_map(tags):
        tag, rows = bmh.pick_tag(cik, tags)
        return {e["end"]: e for e in bmh.ttm_series(bmh.quarterly_flow(rows, ticker))} if rows else {}

    rev = ttm_map(bmh.FLOW_TAGS["revenue"])
    op = ttm_map(bmh.EBITDA_TAGS["opinc"])
    dates = sorted(set(rev) & set(op))

    # 한 분기가 **언제 세상에 나왔는지**는 결산일이 아니라 공시일이다. 예전에는
    # 결산일로 asof를 잘라, 2026-08-01 시점 계산에 아직 공시되지 않은 7월 분기
    # (공시 2026-08-26)가 들어갔다(Codex 발견). `base_inputs`는 `latest()`로
    # 공시일을 지키고 있었으므로 한 함수 안에서 두 기준이 섞여 있었다.
    def avail_of(x):
        return max(rev[x]["available"], op[x]["available"])

    # window_start: 과거 시점 재현은 그 시점 기준 약 5년 창을 쓴다(research/point_in_time_replay.py).
    hw = HISTORY_WINDOW.get(ticker, (WINDOW_START, 13))
    # 연구용 시점 재현(bmh.ASOF_REF)에서는 분사 이력 시작일이 평가일보다 뒤면 쓰지 않는다 — 나중에 정한 날짜라 그 전 평가일에는
    # 미래 정보다(WDC 2025, C8 — Codex). 카드 경로는 그대로.
    if bmh.ASOF_REF and asof and hw[0] > asof:
        hw = (WINDOW_START, 13)
    ws = window_start or hw[0]
    dates = [x for x in dates if x >= ws
             and (asof is None or avail_of(x) <= asof)]
    if len(dates) < hw[1]:
        return None
    # 영업이익률 이력 — run_dcf의 마진 경로와 같은 정의(2026-09-24, 전에는 EBITDA 마진).
    margins = {x: op[x]["val"] / rev[x]["val"] for x in dates}
    k = sorted(margins)

    def cagr(quarters):
        """실제 경과 연수로 나눈다. 분기 수가 모자라면 그만큼 짧은 기간의 CAGR이
        되므로(MSFT는 창 안 분기가 20개라 4.75년) 라벨이 아니라 실제 값을 쓴다.
        시작점은 **날짜로** 고른다 — 끝에서 quarters/4년(45일 여유) 이상 떨어진 가장 늦은 점, 없으면 가장 이른 점.
        예전엔 "quarters개 앞 점"이라 영업이익이 빈 분기가 있으면 3년 성장률이 4.75년 구간이 됐다(COP 2022년, Codex 2026-10-02).
        빈 분기가 없으면 결과가 같다."""
        # 성장률은 매출만 쓰므로 매출 최근 4분기 합 날짜(같은 창·공시일 조건)에서 고른다 — 영업이익이 빈 분기 때문에 빠지지 않게(COP).
        rk = sorted(x for x in rev if x >= ws and x <= k[-1] and (asof is None or rev[x]["available"] <= asof))
        if len(rk) - 1 < 4:
            return None
        d1 = date.fromisoformat(rk[-1])
        far = [x for x in rk[:-1] if (d1 - date.fromisoformat(x)).days >= quarters / 4 * 365.25 - 45]
        start = far[-1] if far else rk[0]
        if len(rk) - 1 - rk.index(start) < 4:
            return None
        d0 = date.fromisoformat(start)
        yrs = (d1 - d0).days / 365.25
        if yrs <= 0:
            return None
        return (rev[rk[-1]]["val"] / rev[start]["val"]) ** (1 / yrs) - 1

    import statistics as st
    g3, g5 = cagr(12), cagr(20)
    # 기저효과: 창 시작(2021-07)이 코로나 저점이라 5년 성장이 부푼 회사(NCLH 137%·CCL 119%)는
    # 5년이 3년보다 15%p 넘게 높고 30%를 넘으면 3년 성장으로 바꾼다(2026-09-25 사용자 결정).
    base_effect = g3 is not None and g5 is not None and g5 > 0.30 and g5 > g3 + 0.15
    return {
        "margin_now": margins[k[-1]],
        "margin_2y": st.median([margins[x] for x in k[-8:]]),
        "margin_5y": st.median(margins.values()),
        "growth_3y": g3, "growth_5y": g3 if base_effect else g5,
        "growth_5y_raw": g5, "growth_base_effect": base_effect,
        "quarters": len(k),
    }


SCENARIO_MARGIN_END = {"보수": "margin_5y", "기본": "margin_2y", "낙관": "margin_now"}


def margin_path_for(hist, scenario="기본", years=5):
    """`scenarios()`가 쓰는 마진 경로를 그대로 돌려준다.

    역방향 DCF를 특정 시나리오의 내재가치와 나란히 보여줄 때 쓴다. 여기에
    한 벌만 두는 이유는 두 곳에 같은 식을 적어두면 한쪽만 고쳐지기 때문이다.
    """
    m0 = hist["margin_now"]
    m_end = hist[SCENARIO_MARGIN_END[scenario]]
    return [m0 + (m_end - m0) * (i + 1) / years for i in range(years)]


def marginal_s2c(base):
    """최근 1년의 **한계** 매출/자본 — 현금흐름 기준(2026-09-24 사용자 결정).

        1년간 매출 증가 ÷ (설비투자 − 감가상각 + 운전자본 증가 + 인수)

    평균 비율(매출 ÷ 투하자본)에는 자본을 적게 쓰던 과거가 섞여 있다. 지금의 투자 파동
    (AI 데이터센터)의 효율을 따로 잰다(Fable 권고). 투하자본 증가(대차대조표)로 재면
    지분 평가이익과 태그 공백에 흔들렸다 — AMZN은 1년 전 공시에 Anthropic 전환사채
    태그가 없어 1년 전 투하자본이 약 $20B 부풀고 효율이 1.65로 나왔다(현금흐름 기준 1.38).
    순투자나 매출 증가가 0 이하면 정의하지 않는다(None → 평균 비율, 결과에 기록).
    """
    t, asof = base.get("ticker"), base.get("asof")
    if not t:
        return None
    # 기준일이 없으면 실행일이 아니라 카드 일봉의 마지막 날(종가일)이다(Codex).
    if not asof:
        try:
            asof = bmh.load_daily(t)[-1][0]
        except Exception:
            asof = date.today().isoformat()
    # 비교 시점은 날짜 − 365일이 아니라 **같은 분기의 1년 전 분기가 공시된 날**이다. 날짜로
    # 빼면 공시일이 하루만 어긋나도(AMZN 2026-07-31 대 2025-08-01) 한 분기 전과 비교해
    # 5분기 매출 증가를 4분기 투자로 나누게 된다(트랙 마지막 점 $89.2 ≠ 카드 $87.6에서 발견).
    cik = feh.CIKS[t]
    _, rrows = bmh.pick_tag(cik, bmh.FLOW_TAGS["revenue"])
    rev_ttm = bmh.ttm_series(bmh.quarterly_flow(rrows, t)) if rrows else []
    seen = [e for e in rev_ttm if e["available"] <= asof]
    if not seen:
        return None
    end_now = date.fromisoformat(seen[-1]["end"])
    prior = [e for e in rev_ttm
             if abs((end_now - date.fromisoformat(e["end"])).days - 365) <= 10 and e["available"] <= asof]   # 그날까지 공시분만(Codex)
    if not prior:
        return None
    try:
        b1 = base_inputs(t, prior[-1]["available"])
    except Exception:
        return None
    if not b1.get("revenue") or base.get("capex") is None or base.get("dda") is None:
        return None
    # 매출 증가는 1년 전 **같은 분기의 TTM 값**으로 잰다. b1(그 값이 공시된 날의 입력)의 매출은 그날 최신 TTM이라, 재공시로 분기
    # 공시일이 한꺼번에 늦게 찍힌 회사(UBER)는 3분기 전 TTM이 됐다(Fable, B17).
    d_rev = base["revenue"] - prior[-1]["val"]
    # 운전자본이 한쪽 시점에만 있으면 변화분을 0으로 본다 — 예전에는 (nwc or 0)이라 변화분이 운전자본 전체가 됐다(B17).
    d_nwc = (base["nwc"] - b1["nwc"]) if (base.get("nwc") is not None and b1.get("nwc") is not None) else 0.0
    # 두 운전자본의 결산일이 1년(±20일) 간격이 아니면 변화분을 0으로 본다 — 재공시로 분기 매출 공시일이 한꺼번에 늦게 찍힌 회사
    # (UBER 2025 분기가 모두 2026-01-12)는 "1년 전" 기준일의 대차대조표가 3분기 전이 돼 운전자본 변화가 3분기치만 잡혔다(Fable).
    e0, e1 = base.get("nwc_end"), b1.get("nwc_end")
    if not (e0 and e1) or abs((date.fromisoformat(e0) - date.fromisoformat(e1)).days - 365) > 20:
        d_nwc = 0.0
    net_inv = base["capex"] - base["dda"] + d_nwc + (base.get("acquisitions") or 0)
    if d_rev <= 0 or net_inv <= 0:
        return None
    # 평균 비율과 같은 상한 — 순투자가 작은 해에 비율이 발산한다(Codex: NVDA 2025-05 시점 14.4).
    return min(d_rev / net_inv, S2C_MAX)


def s2c_path_for(base, scenario="기본", years=5):
    """시나리오별 연도별 매출/자본. 보수 = 최근·평균 중 나쁜 쪽 유지, 기본 = 최근 → 평균으로 5년 회복,
    낙관 = 평균(2026-09-24 사용자 결정). 최근 효율을 못 구하면 평균만 쓴다."""
    avg = run_dcf(base, [0.0] * years, 0.10, 0.025, 0.0, years=years)["s2c_path"][0]
    # 1년 전 입력을 다시 모으는 계산이라 무겁다. 격자(25칸 × 3 시나리오)가 매번 부르므로 base에 캐시한다.
    if "_s2c_marginal" not in base:
        base["_s2c_marginal"] = marginal_s2c(base)
    m = base["_s2c_marginal"]
    if m is None or scenario == "낙관":
        return [avg] * years, (m is None)
    if scenario == "보수":
        # 최근 효율이 평균보다 **좋으면**(NVDA 3.46 대 2.51) 그걸 보수에 쓰면 보수가 아니다.
        # 둘 중 나쁜 쪽(자본이 더 드는 쪽)을 쓴다.
        return [min(m, avg)] * years, False
    return [m + (avg - m) * (i + 1) / years for i in range(years)], False


# ③ 10년 2단계 경로(research/two_stage_prereg.md). 채택 전까지 기본값은 지금 모델("fade").
PATH_MODE = "fade"
REINVEST_LEAD = True   # 재투자 시점 규약(엔진 단위검정 ①, 2026-09-26 사용자 결정으로 적용)
TWO_STAGE = {"years": 10, "hold": 3, "cap": 0.20, "roic_fade": 0.0}


def scenarios(base, hist, wacc, terminal, years=5, path=None):
    """보수·기본·낙관 세 시나리오. 가정은 전부 회사 자기 이력에서 온다.

    성장과 마진을 함께 움직인다. 성장만 흔들면 마진 위험이 빠진 범위가 되고,
    NVDA에서는 그 차이가 주당 $224 대 $150이었다.

    path="two_stage": 10년 예측, 1~hold년 g0(상한 cap) 유지 후 10년차까지 영구성장으로 선형 수렴,
    마진·매출/자본은 5년 경로 뒤 유지, 잔존 ROIC는 할인율로 완전 수렴(roic_fade 0).
    """
    path = path or PATH_MODE
    two = path == "two_stage"
    n = TWO_STAGE["years"] if two else years

    def fade(g0):
        g0 = max(g0, terminal)
        if not two:
            return [g0 + (terminal - g0) * i / (years - 1) for i in range(years)]
        g0 = min(g0, TWO_STAGE["cap"])
        h = TWO_STAGE["hold"]
        # 1~h년 g0, h+1년부터 n년차에 정확히 영구성장률이 되도록 선형
        return [g0 if i < h else g0 + (terminal - g0) * (i - h + 1) / (n - h) for i in range(n)]

    def extend(xs):
        return list(xs) + [xs[-1]] * (n - len(xs))

    plans = [
        ("보수", (hist["growth_5y"] or terminal) / 2, "5년 CAGR의 절반 · 마진 5년 중앙값"),
        ("기본", hist["growth_5y"] or terminal, "5년 CAGR · 마진 최근 2년 중앙값"),
        ("낙관", hist["growth_3y"] or terminal, "3년 CAGR · 마진 현재 유지"),
    ]
    out = []
    for name, g0, desc in plans:
        m_path = extend(margin_path_for(hist, name, years))
        s_path, fell_back = s2c_path_for(base, name, years)
        s_path = extend(s_path)
        r = run_dcf(base, fade(g0), wacc, terminal, 0.0, years=n, margin_path=m_path, s2c=s_path,
                    roic_fade=TWO_STAGE["roic_fade"] if two else 0.5)
        # 실제로 쓴 매출/자본을 남긴다 — 최근 효율을 못 구해 평균으로 떨어지면 조용히 바뀌지 않게(Fable).
        out.append({"name": name, "desc": desc, "growth0": max(g0, terminal),
                    "margin_end": m_path[-1], "per_share": r["per_share"], "roic": r["roic"],
                    "tv_share": ((r["ev"] - r["pv_sum"]) / r["ev"]) if r["ev"] and r["ev"] > 0 else None,
                    "s2c_path": s_path, "s2c_fallback": fell_back,
                    "nonop_per_share": ((base.get("nonop_assets") or 0) / base["shares"]) if base.get("shares") else 0.0})
    return out


def implied_growth(base, price, wacc, terminal, years=5, lo=-0.5, hi=2.0,
                   margin_path=None, s2c=None):
    """역방향 DCF — **현재가가 요구하는 매출 성장률**을 되찾는다.

    순방향 DCF는 내가 넣은 성장 경로를 계산기에 통과시켜 다시 나에게 보여준다.
    성장 경로가 답을 정한다면 결국 입력의 재진술이다. 반대로 돌리면 사람이
    실제로 판단할 수 있는 질문이 된다 — "이 회사가 5년간 연 X%씩 클 수 있나?"

    예측기간 내내 같은 성장률을 쓰고 이후 영구성장률로 넘어간다고 두고,
    주당 내재가치가 현재가와 같아지는 X를 이분법으로 찾는다.

    `margin_path`를 비우면 현재 마진을 그대로 유지한다. 그런데 이 값을 어떤
    시나리오의 내재가치와 나란히 보여줄 거라면 **그 시나리오의 마진 경로를
    같이 넘겨야 한다.** NVDA에서 마진 가정만 바꿔도 요구 성장률이 23.9%(현재
    마진 유지) / 25.3%(기본 시나리오) / 27.3%(보수 시나리오)로 갈린다. 서로
    다른 전제의 두 숫자를 한 화면에 붙이면 비교가 성립하지 않는다.
    """
    def value_at(g):
        return run_dcf(base, [g] * years, wacc, terminal, 0.0, years=years,
                       margin_path=margin_path, s2c=s2c)["per_share"]

    # 매출/자본 재투자에서는 가치가 성장률에 대해 단조 증가한다는 보장이 없다 — ROIC가
    # 할인율보다 낮으면 성장할수록 재투자가 가치를 깎는다(Codex 지적). 그래서 전 구간을
    # 1%p 간격으로 훑어 현재가를 처음 가로지르는 구간을 찾고, 그 안에서만 이분법을 쓴다.
    # 가로지르는 곳이 없으면 None(어떤 일정 성장률로도 현재가가 설명되지 않는다).
    steps = int(round((hi - lo) / 0.01))
    grid = [lo + (hi - lo) * i / steps for i in range(steps + 1)]
    vals = [value_at(g) for g in grid]
    for (g0, v0), (g1, v1) in zip(zip(grid, vals), zip(grid[1:], vals[1:])):
        if v0 == price:
            return g0
        if (v0 - price) * (v1 - price) < 0:
            a_, b_, fa = g0, g1, v0 - price
            for _ in range(50):
                mid = (a_ + b_) / 2
                fm = value_at(mid) - price
                if fa * fm <= 0:
                    b_ = mid
                else:
                    a_, fa = mid, fm
            return (a_ + b_) / 2
    return None


def implied_margin(base, price, wacc, terminal, growth, years=5, s2c=None, lo=-0.5, hi=1.0):
    """역방향 DCF (마진판) — 성장 경로를 고정하고 **현재가가 요구하는 영업이익률**을 찾는다.

    자본수익률이 할인율에 가까운 종목은 성장이 가치를 거의 만들지 못해 요구 성장률이
    발산한다(AMZN: ROIC 약 16% 대 할인율 10%, 요구 성장 53%, 보수 141%). 그런 가격은
    성장이 아니라 마진 확대에 대한 베팅이라 이 질문이 맞다(2026-09-24 사용자 결정).
    마진이 오르면 NOPAT과 한계 ROIC가 함께 오르므로 가치는 마진에 대해 단조 증가한다.
    """
    def value_at(m):
        return run_dcf(base, growth, wacc, terminal, 0.0, years=years,
                       margin_path=[m] * years, s2c=s2c)["per_share"]

    if value_at(lo) > price or value_at(hi) < price:
        return None
    for _ in range(60):
        mid = (lo + hi) / 2
        if value_at(mid) < price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# 요구 성장률이 최근 5년 실제 성장의 이 배수를 넘으면 "성장만으로는 설명 불가"로 보고
# 요구 마진을 대신 보인다(2026-09-24 사용자 결정).
REQ_GROWTH_MULTIPLE = 3.0


def past_growth(ticker, years=3):
    """실제 매출 성장률(연평균). 요구 성장률과 비교할 기준점이다."""
    cik = feh.CIKS[ticker]
    tag, rows = bmh.pick_tag(cik, bmh.FLOW_TAGS["revenue"])
    ttm = bmh.ttm_series(bmh.quarterly_flow(rows, ticker))
    if len(ttm) < years * 4 + 1:
        return None
    now, then = ttm[-1]["val"], ttm[-1 - years * 4]["val"]
    return (now / then) ** (1 / years) - 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--growth", default="45,30,22,16,12",
                    help="5년 매출성장률(%%), 쉼표 구분. 기본값은 예시일 뿐 근거가 아니다")
    ap.add_argument("--wacc", type=float, default=0.10)
    ap.add_argument("--terminal", type=float, default=0.025)
    ap.add_argument("--exit-multiple", type=float, default=25.0)
    ap.add_argument("--price", type=float, help="비교할 현재가 (생략하면 카드에서 읽는다)")
    ap.add_argument("--json", help="결과 저장 경로")
    args = ap.parse_args()

    t = args.ticker.upper()
    growth = [float(x) / 100 for x in args.growth.split(",")]
    base = base_inputs(t)
    hist = history(t)
    price_usd = args.price or bmh.load_daily(t)[-1][4]
    # 재무가 현지 통화(TSM 대만달러)면 계산은 현지 통화 가격으로, 주당 가치 표시는 달러로(v2/fx.py, Codex).
    import fx
    r_fx = fx.rate(t, bmh.load_daily(t)[-1][0])
    price = price_usd * r_fx

    print(f"{t} 기초 수치 (TTM)")
    print(f"  매출 {base['revenue']/1e9:.1f}B · 영업이익 {base['opinc']/1e9:.1f}B"
          f" · 투하자본 {invested_capital(base)/1e9:.1f}B · 주식수 {base['shares']/1e9:.2f}B")
    print(f"  현금+단기투자 {((base.get('cash') or 0)+(base.get('sti') or 0))/1e9:.1f}B"
          f" · 차입금+리스 {((base.get('debt') or 0)+(base.get('lease') or 0))/1e9:.1f}B"
          f" (그중 운용리스 {(base.get('op_lease') or 0)/1e9:.1f}B는 영업비용으로 보고 순부채에서 뺌 — B16)")

    r = run_dcf(base, growth, args.wacc, args.terminal, args.exit_multiple)
    print(f"\n가정: 성장 {args.growth}% · 할인율 {args.wacc:.1%} · 영구성장 {args.terminal:.1%}"
          f" · 출구배수 {args.exit_multiple}x · 실효세율 {r['tax_rate']:.1%}")
    print(f"      영업이익률 {r['margin0']:.1%} 유지 · 매출/자본 {r['s2c']:.2f}"
          f" (투하자본 {r['invested']/1e9:.0f}B) · 한계 ROIC {r['roic']:.1%}")
    print("\n연도별 무차입 잉여현금흐름 (B$)")
    for row in r["rows"]:
        print(f"  {row['year']}년차  매출 {row['revenue']/1e9:8.1f}  영업이익 {row['ebit']/1e9:7.1f}"
              f"  재투자 {row['reinvest']/1e9:6.1f}"
              f"  FCF {row['fcf']/1e9:7.1f}  현재가치 {row['pv']/1e9:7.1f}")
    print(f"\n  예측기간 현재가치 합 {r['pv_sum']/1e9:.0f}B")
    print(f"  기업가치 {r['ev']/1e9:.0f}B (영구성장 기준)"
          f" · 잔존 ROIC {r['roic_terminal']:.1%} → 재투자율 {r['reinvest_rate']:.1%}")
    print(f"  순부채 {r['net_debt']/1e9:.0f}B → 주주가치 {r['equity']/1e9:.0f}B")
    print(f"\n  주당 내재가치 ${r['per_share'] / r_fx:.2f}   현재가 ${price_usd:.2f}")
    margin = (r["per_share"] - price) / r["per_share"] * 100
    upside = (r["per_share"] - price) / price * 100
    print(f"  안전마진(내재가치 대비 할인율) {margin:+.1f}%"
          f" · 현재가 대비 수익률 {upside:+.1f}%  ({'저평가' if margin > 0 else '고평가'})")

    print("\n민감도 — 주당 내재가치 ($)")
    waccs = [args.wacc - 0.02, args.wacc - 0.01, args.wacc, args.wacc + 0.01, args.wacc + 0.02]
    terms = [args.terminal - 0.01, args.terminal - 0.005, args.terminal,
             args.terminal + 0.005, args.terminal + 0.01]
    print("   영구성장↓/할인율→ " + "".join(f"{w:>9.1%}" for w in waccs))
    for g in terms:
        cells = []
        for w in waccs:
            v = run_dcf(base, growth, w, g, args.exit_multiple)["per_share"] / r_fx
            cells.append(f"{v:9.0f}")
        print(f"   {g:>16.1%} " + "".join(cells))

    # 역방향 — 현재가가 요구하는 성장률
    #
    # 마진 가정마다 답이 달라지므로 시나리오별로 전부 찍는다. 카드에 한 숫자만
    # 실을 거라면 **옆에 나란히 놓일 내재가치와 같은 시나리오**의 값을 써야 한다.
    past3 = past_growth(t, 3)
    past5 = past_growth(t, 5)
    print("\n역방향 — 현재가가 요구하는 것")
    print(f"  {'가정':22s} {'요구 매출 성장률(5년)':>18s}")
    for name in ["낙관", "기본", "보수"]:
        mp = margin_path_for(hist, name)
        req = implied_growth(base, price, args.wacc, args.terminal, margin_path=mp,
                             s2c=s2c_path_for(base, name)[0])
        label = f"{name} (마진 {mp[-1]:.1%}로 수렴)"
        print(f"  {label:22s} " + (f"{req:>17.1%}" if req is not None else f"{'범위 밖':>18s}"))
    print(f"  ↑ ${price_usd:.2f} 기준 · 이후 영구 {args.terminal:.1%} · 할인율 {args.wacc:.1%}")
    if past3:
        print(f"  실제 최근 3년 연평균 매출 성장률 {past3:+.1%}"
              + (f" · 5년 {past5:+.1%}" if past5 else ""))
    print("  → 이 성장률이 달성 가능해 보이면 현재가는 정당하고, 무리해 보이면 비싸다")

    if args.json:
        json.dump({"ticker": t, "price": price_usd, "per_share": r["per_share"] / r_fx,
                   "margin_pct": margin, "assumptions": {
                       "growth": growth, "wacc": args.wacc, "terminal": args.terminal,
                       "exit_multiple": args.exit_multiple, "tax_rate": r["tax_rate"],
                       "model": "sales-to-capital (2026-09-24)", "margin": "operating (EBIT)",
                       "s2c": r["s2c"]}},
                  open(args.json, "w"), ensure_ascii=False, indent=1)
        print("\n저장:", args.json)


if __name__ == "__main__":
    main()
