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
    val = None
    for e in series:
        if e.get("available", e.get("end")) <= asof:
            val = e["val"]
        else:
            break
    return val


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
    out["acquisitions"] = ttm(["PaymentsToAcquireBusinessesNetOfCashAcquired"]) or 0
    out["tax"] = ttm(["IncomeTaxExpenseBenefit"])
    out["pretax"] = ttm(["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                         "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"])

    for name, tags in bmh.EV_COMPONENTS.items():
        # asof를 빠뜨리면 과거 시점 계산에 오늘 대차대조표가 섞인다
        # (현금·단기투자·차입금·리스가 그랬다 — Codex 지적으로 발견).
        out[name] = latest(bmh.ev_component(cik, name, tags), asof)
    # 금융리스부채는 운용리스와 별개 태그라 EV_COMPONENTS["lease"]에 안 잡힌다.
    # MSFT는 $66.6B가 순부채에서 통째로 빠져 있었다(주당 약 $9).
    # 총계 태그가 있으면 그것만 쓴다. 셋을 모두 더하면 총계와 세부가 겹쳐
    # 금융리스가 두 배로 잡히는 회사가 나온다(Codex 지적).
    fin_lease = latest(bmh.component_sum(cik, ["FinanceLeaseLiability"]), asof)
    if not fin_lease:
        fin_lease = latest(bmh.component_sum(cik, ["FinanceLeaseLiabilityCurrent",
                                                   "FinanceLeaseLiabilityNoncurrent"]), asof)
    fin_lease = fin_lease or 0
    out["lease"] = (out.get("lease") or 0) + fin_lease
    out["finance_lease"] = fin_lease

    _, srows = bmh.pick_tag(cik, ["CommonStockSharesOutstanding"], "us-gaap")
    _, drows = bmh.pick_tag(cik, ["EntityCommonStockSharesOutstanding"], "dei")
    out["shares"] = latest(bmh.instant_series(srows + drows, ticker, is_share_count=True), asof)

    out["equity"] = latest(bmh.component_sum(cik, ["StockholdersEquity"]), asof)
    # 비영업 투자자산 — 영업에 쓰이지 않는 지분·장기투자
    # Apple은 장기 채권 투자를 LongTermInvestments가 아니라 MarketableSecuritiesNoncurrent로
    # 보고한다(2026-06-27 $84.1B). 이 태그를 안 보면 그 자산이 주주가치에서 통째로 빠진다.
    # 그 태그를 예전에 쓰다 그만둔 회사(AMD 2014년 값 등)의 낡은 값을 집지 않도록,
    # 그 시점(asof)에 공개돼 있던 자기자본보다 200일 넘게 뒤처진 값은 버린다.
    # 판정은 반드시 asof 시점 기준이다. 전체 계열의 마지막 날짜로 판정하면 나중에 태그를
    # 그만둔 사실이 과거 계산에서 그때 유효했던 값까지 지운다(Codex 지적, 2026-09-24).
    eq_rows = bmh.component_sum(cik, ["StockholdersEquity"])

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
    out["lt_marketable"] = fresh_latest(bmh.component_sum(cik, ["MarketableSecuritiesNoncurrent"])) or 0
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
    # 종목 지정 비영업자산(v2/nonop_extra.json). 같은 태그가 회사마다 다른 자산을 담아
    # (AvailableForSaleSecuritiesDebtSecurities는 흔히 단기 시장성 채권 전체다) 일괄 적용하면
    # 현금·단기투자와 겹친다. 10-Q 주석으로 확인한 종목만 목록에 올린다(AMZN Anthropic 전환사채).
    extra_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nonop_extra.json")
    extra = json.load(open(extra_path)).get(ticker, []) if os.path.exists(extra_path) else []
    out["nonop_extra"] = sum(fresh_latest(bmh.component_sum(cik, [x["tag"]])) or 0 for x in extra)
    out["nonop_assets"] += out["nonop_extra"]

    # 운전자본은 재고·매출채권처럼 영업에 묶인 돈만 본다. 현금과 차입금은 뺀다
    # (그 둘은 순부채 쪽에서 따로 계산되므로 여기 넣으면 두 번 센다).
    ac = latest(bmh.component_sum(cik, ["AssetsCurrent"]), asof)
    lc = latest(bmh.component_sum(cik, ["LiabilitiesCurrent"]), asof)
    if ac and lc:
        cash = (out.get("cash") or 0) + (out.get("sti") or 0)
        st_debt = latest(bmh.component_sum(cik, ["LongTermDebtCurrent"]), asof) or 0
        # 유동자산에는 상장주식 같은 투자자산도 들어 있다. 영업에 묶인 돈이
        # 아니므로 운전자본에서 뺀다. NVDA는 EquitySecuritiesFvNi $42.8B가
        # 섞여 운전자본이 매출의 32.6%로 잡혔다(실제 18.5% 수준).
        invest_assets = latest(bmh.component_sum(cik, ["EquitySecuritiesFvNi"]), asof) or 0
        out["invest_assets"] = invest_assets
        out["nwc"] = (ac - cash - invest_assets) - (lc - st_debt)
    out["ticker"], out["asof"] = ticker, asof   # 한계 매출/자본 계산용(scenarios)
    return out


S2C_MAX = 10.0   # 매출/자본 상한 — 자본을 거의 안 쓰는 회사의 발산 방지


def invested_capital(base):
    """영업에 묶인 투하자본 = 자기자본 + 차입금 + 리스 − 현금·단기투자 − 비영업자산."""
    return ((base.get("equity") or 0) + (base.get("debt") or 0) + (base.get("lease") or 0)
            - (base.get("cash") or 0) - (base.get("sti") or 0) - (base.get("nonop_assets") or 0))


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
    tax_rate = tax_rate if tax_rate is not None else (
        base["tax"] / base["pretax"] if base.get("tax") and base.get("pretax") else 0.21)
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
        nopat = ebit * (1 - tax_rate)
        reinvest = (new_rev - rev) / s2c_path[i]
        fcf = nopat - reinvest
        rev = new_rev
        # 기중 할인(Dechra 모델과 같은 0.5년 관행)
        disc = 1 / (1 + wacc) ** (i + 0.5)
        rows.append({"year": i + 1, "revenue": rev, "ebit": ebit, "nopat": nopat,
                     "reinvest": reinvest, "fcf": fcf, "pv": fcf * disc})

    pv_sum = sum(r["pv"] for r in rows)
    last = rows[-1]

    # 잔존: 재투자율 = 영구성장률 / ROIC. 예측기간의 한계 ROIC는 마진 × (1−세율) × 매출/자본이고,
    # 잔존에서는 경쟁이 초과수익을 깎으므로 할인율 쪽으로 절반 수렴시킨다(roic_fade).
    # NVDA는 현재 ROIC가 78.5%라 그대로 두면 잔존 FCF가 NOPAT의 96.8%가 되고, 이 가정 하나가
    # 주당 $54를 만든다(검증에서 확인).
    roic = margins[-1] * (1 - tax_rate) * s2c_path[-1]
    roic_t = wacc + (roic - wacc) * roic_fade if roic > wacc else roic
    # ROIC가 영구성장률 이하면 성장이 가치를 만들지 못한다 — 재투자율을 1로 두어 잔존 현금흐름이 0.
    reinvest_rate = min(max(terminal / roic_t, 0.0), 1.0) if roic_t > terminal else 1.0
    nopat_t = last["revenue"] * (1 + terminal) * margins[-1] * (1 - tax_rate)
    fcf_t = nopat_t * (1 - reinvest_rate)

    tv_ggm = fcf_t / (wacc - terminal) if wacc > terminal else float("nan")
    # 예측기간 현금흐름을 기중(i+0.5)으로 할인하므로 잔존가치도 같은 기준으로 맞춘다.
    pv_ggm = tv_ggm / (1 + wacc) ** (years - 0.5)
    # 출구배수는 참고용이다(영업이익 배수). **영구성장 하나만 쓴다** — 두 방법을 평균내지
    # 않는다(2026-09-20 결정). exit_mult=0이면 예측기간 현재가치다.
    ev_exit = pv_sum + last["ebit"] * exit_mult / (1 + wacc) ** (years - 0.5)
    ev = pv_sum + pv_ggm

    net_debt = ((base.get("debt") or 0) + (base.get("lease") or 0)
                - (base.get("cash") or 0) - (base.get("sti") or 0))
    equity = (ev - net_debt - (base.get("nci") or 0) - (base.get("preferred") or 0)
              + (base.get("nonop_assets") or 0))
    return {"rows": rows, "pv_sum": pv_sum, "ev_ggm": ev, "ev_exit": ev_exit, "fcf_terminal": fcf_t,
            "ev": ev, "net_debt": net_debt, "equity": equity,
            "per_share": equity / base["shares"], "tax_rate": tax_rate,
            "margin0": margin0, "s2c": s2c_path[-1], "s2c_path": s2c_path, "invested": invested,
            "roic": roic, "roic_terminal": roic_t, "reinvest_rate": reinvest_rate}


def history(ticker, asof=None):
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

    dates = [x for x in dates if x >= WINDOW_START
             and (asof is None or avail_of(x) <= asof)]
    if len(dates) < 13:
        return None
    # 영업이익률 이력 — run_dcf의 마진 경로와 같은 정의(2026-09-24, 전에는 EBITDA 마진).
    margins = {x: op[x]["val"] / rev[x]["val"] for x in dates}
    k = sorted(margins)

    def cagr(quarters):
        """실제 경과 연수로 나눈다. 분기 수가 모자라면 그만큼 짧은 기간의 CAGR이
        되므로(MSFT는 창 안 분기가 20개라 4.75년) 라벨이 아니라 실제 값을 쓴다."""
        n = min(quarters, len(k) - 1)
        if n < 4:
            return None
        d0 = date.fromisoformat(k[-1 - n])
        d1 = date.fromisoformat(k[-1])
        yrs = (d1 - d0).days / 365.25
        if yrs <= 0:
            return None
        return (rev[k[-1]]["val"] / rev[k[-1 - n]]["val"]) ** (1 / yrs) - 1

    import statistics as st
    return {
        "margin_now": margins[k[-1]],
        "margin_2y": st.median([margins[x] for x in k[-8:]]),
        "margin_5y": st.median(margins.values()),
        "growth_3y": cagr(12), "growth_5y": cagr(20),
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
             if abs((end_now - date.fromisoformat(e["end"])).days - 365) <= 10]
    if not prior:
        return None
    try:
        b1 = base_inputs(t, prior[-1]["available"])
    except Exception:
        return None
    if not b1.get("revenue") or base.get("capex") is None or base.get("dda") is None:
        return None
    d_rev = base["revenue"] - b1["revenue"]
    net_inv = (base["capex"] - base["dda"] + ((base.get("nwc") or 0) - (b1.get("nwc") or 0))
               + (base.get("acquisitions") or 0))
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


def scenarios(base, hist, wacc, terminal, years=5):
    """보수·기본·낙관 세 시나리오. 가정은 전부 회사 자기 이력에서 온다.

    성장과 마진을 함께 움직인다. 성장만 흔들면 마진 위험이 빠진 범위가 되고,
    NVDA에서는 그 차이가 주당 $224 대 $150이었다.
    """
    def fade(g0):
        g0 = max(g0, terminal)
        return [g0 + (terminal - g0) * i / (years - 1) for i in range(years)]

    plans = [
        ("보수", (hist["growth_5y"] or terminal) / 2, "5년 CAGR의 절반 · 마진 5년 중앙값"),
        ("기본", hist["growth_5y"] or terminal, "5년 CAGR · 마진 최근 2년 중앙값"),
        ("낙관", hist["growth_3y"] or terminal, "3년 CAGR · 마진 현재 유지"),
    ]
    out = []
    for name, g0, desc in plans:
        m_path = margin_path_for(hist, name, years)
        s_path, fell_back = s2c_path_for(base, name, years)
        r = run_dcf(base, fade(g0), wacc, terminal, 0.0, years=years, margin_path=m_path, s2c=s_path)
        # 실제로 쓴 매출/자본을 남긴다 — 최근 효율을 못 구해 평균으로 떨어지면 조용히 바뀌지 않게(Fable).
        out.append({"name": name, "desc": desc, "growth0": max(g0, terminal),
                    "margin_end": m_path[-1], "per_share": r["per_share"], "roic": r["roic"],
                    "s2c_path": s_path, "s2c_fallback": fell_back,
                    "nonop_per_share": (base.get("nonop_assets") or 0) / base["shares"]})
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
    price = args.price or bmh.load_daily(t)[-1][4]

    print(f"{t} 기초 수치 (TTM)")
    print(f"  매출 {base['revenue']/1e9:.1f}B · 영업이익 {base['opinc']/1e9:.1f}B"
          f" · 투하자본 {invested_capital(base)/1e9:.1f}B · 주식수 {base['shares']/1e9:.2f}B")
    print(f"  현금+단기투자 {((base.get('cash') or 0)+(base.get('sti') or 0))/1e9:.1f}B"
          f" · 차입금+리스 {((base.get('debt') or 0)+(base.get('lease') or 0))/1e9:.1f}B")

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
    print(f"\n  주당 내재가치 ${r['per_share']:.2f}   현재가 ${price:.2f}")
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
            v = run_dcf(base, growth, w, g, args.exit_multiple)["per_share"]
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
    print(f"  ↑ ${price:.2f} 기준 · 이후 영구 {args.terminal:.1%} · 할인율 {args.wacc:.1%}")
    if past3:
        print(f"  실제 최근 3년 연평균 매출 성장률 {past3:+.1%}"
              + (f" · 5년 {past5:+.1%}" if past5 else ""))
    print("  → 이 성장률이 달성 가능해 보이면 현재가는 정당하고, 무리해 보이면 비싸다")

    if args.json:
        json.dump({"ticker": t, "price": price, "per_share": r["per_share"],
                   "margin_pct": margin, "assumptions": {
                       "growth": growth, "wacc": args.wacc, "terminal": args.terminal,
                       "exit_multiple": args.exit_multiple, "tax_rate": r["tax_rate"],
                       "model": "sales-to-capital (2026-09-24)", "margin": "operating (EBIT)",
                       "s2c": r["s2c"]}},
                  open(args.json, "w"), ensure_ascii=False, indent=1)
        print("\n저장:", args.json)


if __name__ == "__main__":
    main()
