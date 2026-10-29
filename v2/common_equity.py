"""보통주 자본(CE) — PBR 분모에서 우선주를 뺀다(안건 E44, 설계 `research/shares_equity_design.md` r9 §2).

CE(d) = 지배주주 자본 − P(d). 지배주주 자본은 엔진 equity 시리즈 값이고, 그 결산일 값이 비지배지분 포함 총계
(…IncludingPortionAttributableToNoncontrollingInterest)에서 왔으면 비지배지분을 빼서 되돌린다 — 같은 결산일 값, 없으면 400일 안
마지막 보고를 이어 쓰고(그 사이 '지배주주 자본 = 총계' 관측이 있으면 0), 그보다 오래됐거나 없으면 0(추정).
P(d)는 자본 안 비전환 우선주 장부가 — 손입력(CE_PREF_MANUAL)이 있으면 그것, 아니면 CE_PREF_TAGS 중 그 결산일에 0보다 큰 첫 태그
(액면 태그가 같은 결산일 청산가의 1/10 미만이면 청산가). 없으면 상환 증거(주식 수 0, 의미 있던 금액 태그가 명시적 0, PREF_REDEEMED)가
있으면 0, 아니면 직전 값을 400일까지 이어 쓰고, 넘으면 마지막 우선주 주식 수 관측이 0보다 크면 기권(None), 아니면 0(추정).
값을 정할 수 없는 날짜는 val None(그 날짜 PBR 없음). 추정이 들어간 행은 ce_note에 남긴다.
EV의 회사별 우선주 덮어쓰기는 EV 전용이다 — CE는 CE_PREF_OVERRIDE·CE_PREF_MANUAL만 따른다. 은행 경로·기본적 분석 점수는 바꾸지 않는다.
연구 모드(bmh.ASOF_REF)에서는 지금 equity 그대로(설계 §5 — 12-01 패널은 옛 정의).
"""
from datetime import date

CE_PREF_TAGS = ["PreferredStockValue", "PreferredStockIncludingAdditionalPaidInCapital",
                "PreferredStockIncludingAdditionalPaidInCapitalNetOfDiscount", "PreferredStockValueOutstanding",
                "ConvertiblePreferredStockNonredeemableOrRedeemableIssuerOptionValue",
                "PreferredStockLiquidationPreferenceValue"]          # 마지막(청산가)은 경고
LIQ_TAG = "PreferredStockLiquidationPreferenceValue"
PAR_TAG = "PreferredStockValue"
PAR_RATIO = 10           # 액면 태그 × 10 < 같은 결산일 청산가면 액면으로 보고 청산가를 쓴다(GE $6M 대 $5.9B)
PREF_SHARE_TAGS = ["PreferredStockSharesOutstanding", "PreferredStockSharesIssued"]   # 유통이 앞, 없을 때만 발행
MATERIAL = 1e7           # 명시적 0을 상환 증거로 볼 직전 금액의 하한($10M — 액면만 태깅하는 회사(MET·BMY)와 가르기)
# 회사별 CE 우선주 태그(빈 목록 = 우선주 없음). EV 덮어쓰기(EV_TAGS_BY_CIK "preferred")와 따로 둔다(설계 §2.1).
CE_PREF_OVERRIDE = {"0001101239": []}   # EQIX — 우선주 없음
# 표준 태그가 없거나 틀린 비전환 우선주 장부가(손입력, 원문 출처) {cik: [{"from", "until", "value", "filed", "source"}]} — 설계 r9
import json as _json
import os as _os
_MANUAL = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "ce_pref_manual.json")
CE_PREF_MANUAL = {k: v for k, v in (_json.load(open(_MANUAL)) if _os.path.exists(_MANUAL) else {}).items() if not k.startswith("_")}
# 회사별 상환 증거 {cik: [{"date": 상환일, "filed": 그 사실의 공시일, "source": …}]}
PREF_REDEEMED = {}
CARRY_DAYS = 400

warnings = []


def _warn(msg):
    if msg not in warnings:
        warnings.append(msg)


def _bmh():
    import build_multiple_history as bmh
    return bmh


def _days(a, b):
    return (date.fromisoformat(a) - date.fromisoformat(b)).days


def _instants(cik, tag):
    """그 태그의 시점 값 [{end, filed, val}] (기간 값 제외)."""
    _, rows = _bmh().pick_tag(cik, [tag])
    return [r for r in (rows or []) if "start" not in r and r.get("end") and r.get("filed")]


def _val_at(rows, end, avail):
    """결산일 end, 공시일 ≤ avail인 값(가장 늦게 공시된 것). 없으면 None."""
    c = [r for r in rows if r["end"] == end and r["filed"] <= avail]
    return sorted(c, key=lambda r: r["filed"])[-1]["val"] if c else None


class _Pref:
    def __init__(self, cik, ticker):
        self.cik, self.t = cik, ticker
        tags = CE_PREF_OVERRIDE.get(cik, CE_PREF_TAGS)
        self.tags = [(tg, _instants(cik, tg)) for tg in tags]
        self.liq = _instants(cik, LIQ_TAG) if tags else []
        self.shares = [_instants(cik, tg) for tg in PREF_SHARE_TAGS] if tags else []
        self.manual = CE_PREF_MANUAL.get(cik, [])
        self.note = None

    def direct(self, end, avail):
        """그 결산일에 0보다 큰 첫 태그 값 — (값, 태그) 또는 None. 합산하지 않는다."""
        for tg, rows in self.tags:
            v = _val_at(rows, end, avail)
            if v is not None and v > 0:
                if tg == PAR_TAG:
                    lq = _val_at(self.liq, end, avail)
                    if lq and lq > PAR_RATIO * v:
                        _warn(f"{self.t} {end}: 우선주 장부 태그 {v:,.0f}가 청산가 {lq:,.0f}의 1/{PAR_RATIO} 미만 — 액면으로 보고 청산가로 차감")
                        return lq, LIQ_TAG
                return v, tg
        return None

    def share_obs(self, end, avail):
        """end 이하 마지막 우선주 주식 수 관측 (결산일, 값) — 유통 주식 수가 있으면 그것, 없을 때만 발행 주식 수."""
        for rows in self.shares:
            c = [r for r in rows if r["end"] <= end and r["filed"] <= avail]
            if c:
                r = max(c, key=lambda r: (r["end"], r["filed"]))
                return r["end"], r["val"]
        return None

    def explicit_zero(self, end, avail):
        """의미 있던 금액 태그(직전 양수 ≥ $10M)가 그 결산일에 명시적 0 — 상환 증거(DHR·PGR·HWM). 늘 0인 액면 태그(MET)는 아님."""
        for tg, rows in self.tags:
            if _val_at(rows, end, avail) == 0:
                prior = [r for r in rows if r["end"] < end and r["filed"] <= avail]
                if prior and max(prior, key=lambda r: (r["end"], r["filed"]))["val"] >= MATERIAL:
                    return True
        return False

    def redeemed(self, end, avail):
        so = self.share_obs(end, avail)
        if so and so[0] == end and so[1] == 0:
            return True
        if self.explicit_zero(end, avail):
            return True
        return any(x["date"] == end and x["filed"] <= avail for x in PREF_REDEEMED.get(self.cik, []))

    def p(self, end, avail):
        """P(end) — 0 이상 값, 또는 None(기권). self.note에 추정 여부를 남긴다."""
        self.note = None
        for x in self.manual:
            if x["from"] <= end and (x.get("until") is None or end <= x["until"]) and x["filed"] <= avail:
                self.note = "pref_manual"
                return float(x["value"])
        if not self.tags:
            return 0.0
        d = self.direct(end, avail)
        if d:
            if d[1] == LIQ_TAG:
                _warn(f"{self.t} {end}: 우선주 장부가 태그 없음 — 청산가 태그로 차감")
            return float(d[0])
        if self.redeemed(end, avail):
            return 0.0
        so = self.share_obs(end, avail)
        ends = sorted({r["end"] for _, rows in self.tags for r in rows if r["end"] < end and r["filed"] <= avail})
        prev = [e for e in ends if self.direct(e, avail)]
        if not prev:
            if so and so[1] > 0:
                # 주식 수 태그는 수권 주식(PLTR 20억)·명목 주식(UAL 2주)·작은 우선주(BMY 2,991주)가 섞여 증거로 쓰면 멀쩡한 PBR이 사라진다 —
                # 경고·표시만 하고 0(실제 보유 회사는 손입력 CE_PREF_MANUAL로, 2026-10-29 전 카드 점검)
                _warn(f"{self.t} {end}: 우선주 주식 수 {so[1]:,.0f}({so[0]})는 있는데 금액이 한 번도 없음 — 0으로 두고 점검 표시")
                self.note = "pref_shares_no_amount"
            return 0.0
        e1 = prev[-1]
        mids = sorted({r["end"] for rows in self.shares for r in rows if e1 < r["end"] <= end}
                      | {r["end"] for _, rows in self.tags for r in rows if e1 < r["end"] <= end})
        red = [m for m in mids if self.redeemed(m, avail)] + \
              [x["date"] for x in PREF_REDEEMED.get(self.cik, []) if e1 < x["date"] <= end and x["filed"] <= avail]
        if red:
            # 상환 뒤에 우선주 주식 수 > 0이 다시 관측되면(새 발행 — AXP 2019~ 1,600주) 금액이 없으니 기권, 아니면 0
            if so and so[1] > 0 and so[0] > max(red):
                _warn(f"{self.t} {end}: 상환 뒤 우선주 주식 수 {so[1]:,.0f}({so[0]})가 다시 관측됨 — 금액이 없어 0으로 두고 점검 표시")
                self.note = "pref_shares_no_amount"
            return 0.0
        prev_sh = [r for rows in self.shares[:1] for r in rows if r["end"] <= e1 and r["filed"] <= avail]
        if so and prev_sh and so[1] < max(prev_sh, key=lambda r: (r["end"], r["filed"]))["val"]:
            _warn(f"{self.t} {end}: 우선주 주식 수가 {e1} 뒤 줄었는데 금액이 없음(부분 상환?) — 옛 금액 이어 씀")
        if _days(end, e1) > CARRY_DAYS:
            if so and so[1] > 0 and _days(end, so[0]) <= CARRY_DAYS:
                _warn(f"{self.t} {end}: 우선주 주식 수 {so[1]:,.0f}({so[0]})는 있는데 금액이 {e1} 뒤로 {CARRY_DAYS}일 넘게 없음 — 0으로 두고 점검 표시")
                self.note = "pref_shares_no_amount"
                return 0.0
            _warn(f"{self.t} {end}: 우선주 금액이 {e1} 뒤로 {CARRY_DAYS}일 넘게 없고 주식 수 증거도 없음 — 잔액 미확인, 정책상 0 추정")
            self.note = "pref_est0"
            return 0.0
        _warn(f"{self.t} {end}: 우선주 값 없음 — {e1} 값 이어 씀")
        self.note = "pref_carry"
        return float(self.direct(e1, avail)[0])


def ce_series(cik, ticker, equity):
    """엔진 equity 시리즈([{end, val, available}])를 보통주 자본으로 바꾼 시리즈. 값을 정할 수 없는 날짜는 val None으로 남긴다 —
    빼면 그날 조회가 직전 값을 집어 PBR이 계산된다(설계 §2: 그 날짜 PBR은 None). 추정이 들어간 행은 ce_note."""
    bmh = _bmh()
    if bmh.ASOF_REF is not None or not equity:
        return equity
    parent = _instants(cik, "StockholdersEquity")
    total = _instants(cik, "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest")
    nci = _instants(cik, "MinorityInterest")
    # 지배주주 자본 = 총계로 관측된 결산일(비지배지분 0 관측) — 그 뒤로는 옛 비지배지분을 이어 쓰지 않는다(JNJ Kenvue 2023)
    tot_by = {(x["end"], x["filed"]): x["val"] for x in total}
    zero_obs = sorted({r["end"] for r in parent if tot_by.get((r["end"], r["filed"])) == r["val"]})
    pref = _Pref(cik, ticker)
    out = []
    for e in equity:
        end, av, v = e["end"], e["available"], e["val"]
        notes = []
        pv = _val_at(parent, end, av)
        if pv is None or pv != v:
            tv = _val_at(total, end, av)
            if tv is not None and tv == v:
                n = _val_at(nci, end, av)
                if n is None:
                    recent = sorted([r for r in nci if r["end"] < end and r["filed"] <= av and _days(end, r["end"]) <= CARRY_DAYS],
                                    key=lambda r: (r["end"], r["filed"]))
                    if recent and not any(recent[-1]["end"] < z < end for z in zero_obs):
                        n = recent[-1]["val"]
                        notes.append("nci_carry")
                        _warn(f"{ticker} {end}: 같은 결산일 비지배지분 없음 — {recent[-1]['end']} 값 이어 씀")
                    else:
                        n = 0
                        notes.append("nci_est0")
                        _warn(f"{ticker} {end}: 같은 결산일 비지배지분 없음 — 400일 안 보고 없음(또는 그 뒤 0 관측) — 정책상 0 추정")
                v = tv - n
            elif pv is not None:
                _warn(f"{ticker} {end}: 엔진 자본 {v:,.0f}가 지배주주 자본 {pv:,.0f}·총계 {tv}와 다름 — 그대로 씀")
        p = pref.p(end, av)
        if pref.note:
            notes.append(pref.note)
        if p is None:
            out.append(dict(e, val=None, pref=None, ce_note=notes + ["pref_hold"]))
            continue
        out.append(dict(e, val=v - p, pref=p, ce_note=notes) if notes else dict(e, val=v - p, pref=p))
    return out
