"""보통주 자본(CE) — PBR 분모에서 우선주를 뺀다(안건 E44, 설계 `research/shares_equity_design.md` r7 §2).

CE(d) = 지배주주 자본 − P(d). 지배주주 자본은 엔진 equity 시리즈 값이고, 그 결산일 값이 비지배지분 포함 총계
(…IncludingPortionAttributableToNoncontrollingInterest)에서 왔으면 같은 결산일 MinorityInterest를 빼서 되돌린다(없으면 그 날짜 None).
P(d)는 자본 안 비전환(또는 카드별 표에서 보통주로 보지 않은) 우선주 장부가 — CE_PREF_TAGS 중 그 결산일에 0보다 큰 첫 태그 하나.
없으면 상환 증거가 있을 때만 0, 아니면 직전 0보다 큰 값을 400일까지 이어 쓰고(경고), 넘으면 None(기권). 한 번도 없으면 0.
EV의 회사별 우선주 덮어쓰기는 EV 전용이다 — CE는 CE_PREF_OVERRIDE만 따른다. 은행 경로·기본적 분석 점수는 바꾸지 않는다.
연구 모드(bmh.ASOF_REF)에서는 지금 equity 그대로(설계 §5 — 12-01 패널은 옛 정의).
"""
from datetime import date

CE_PREF_TAGS = ["PreferredStockValue", "PreferredStockIncludingAdditionalPaidInCapital",
                "PreferredStockIncludingAdditionalPaidInCapitalNetOfDiscount", "PreferredStockValueOutstanding",
                "ConvertiblePreferredStockNonredeemableOrRedeemableIssuerOptionValue",
                "PreferredStockLiquidationPreferenceValue"]          # 마지막(청산가)은 경고
PREF_SHARE_TAGS = ["PreferredStockSharesOutstanding", "PreferredStockSharesIssued"]
# 회사별 CE 우선주 태그(빈 목록 = 우선주 없음). EV 덮어쓰기(EV_TAGS_BY_CIK "preferred")와 따로 둔다(설계 §2.1).
CE_PREF_OVERRIDE = {"0001101239": []}   # EQIX — 우선주 없음
# 회사별 상환 증거 {cik: [{"date": 상환일, "filed": 그 사실의 공시일, "source": …}]} — 우선주 주식 수 0 태그가 없는 회사
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
        self.share_rows = [_instants(cik, tg) for tg in PREF_SHARE_TAGS] if tags else []

    def direct(self, end, avail):
        """그 결산일에 0보다 큰 첫 태그 값 — (값, 태그) 또는 None. 합산하지 않는다."""
        for tg, rows in self.tags:
            v = _val_at(rows, end, avail)
            if v is not None and v > 0:
                return v, tg
        return None

    def redeemed(self, end, avail):
        for rows in self.share_rows:
            v = _val_at(rows, end, avail)
            if v is not None and v == 0:
                return True
        return any(x["date"] <= end and x["filed"] <= avail for x in PREF_REDEEMED.get(self.cik, []))

    def p(self, end, avail):
        """P(end) — 0 이상 값, 또는 None(400일 넘게 이어 써야 해서 기권)."""
        if not self.tags:
            return 0.0
        d = self.direct(end, avail)
        if d:
            if d[1] == "PreferredStockLiquidationPreferenceValue":
                _warn(f"{self.t} {end}: 우선주 장부가 태그 없음 — 청산가 태그로 차감")
            return float(d[0])
        if self.redeemed(end, avail):
            return 0.0
        ends = sorted({r["end"] for _, rows in self.tags for r in rows if r["end"] < end and r["filed"] <= avail})
        prev = [e for e in ends if self.direct(e, avail)]
        if not prev:
            return 0.0
        e1 = prev[-1]
        mids = sorted({r["end"] for rows in self.share_rows for r in rows if e1 < r["end"] <= end})
        if any(self.redeemed(m, avail) for m in mids) or \
                any(e1 < x["date"] <= end and x["filed"] <= avail for x in PREF_REDEEMED.get(self.cik, [])):
            return 0.0
        if _days(end, e1) > CARRY_DAYS:
            # 400일 넘게 값이 없으면: 그 결산일 우선주 주식 수 > 0(아직 있다는 증거)이면 기권, 아니면 상환된 것으로 보고 0(설계 r8 —
            # MRK 2009·CL 2010·AMT 2014·PEP 2017처럼 오래전 우선주를 0 주식 수 태그 없이 없앤 회사가 몇 년씩 기권되던 것)
            if any((_val_at(rows, end, avail) or 0) > 0 for rows in self.share_rows):
                _warn(f"{self.t} {end}: 우선주 주식 수는 있는데 금액이 {e1} 뒤로 {CARRY_DAYS}일 넘게 없음 — 그 날짜 PBR 기권")
                return None
            _warn(f"{self.t} {end}: 우선주 금액이 {e1} 뒤로 {CARRY_DAYS}일 넘게 없고 주식 수 증거도 없음 — 상환으로 보고 0")
            return 0.0
        _warn(f"{self.t} {end}: 우선주 값 없음 — {e1} 값 이어 씀")
        return float(self.direct(e1, avail)[0])


def ce_series(cik, ticker, equity):
    """엔진 equity 시리즈([{end, val, available}])를 보통주 자본으로 바꾼 시리즈. 값을 정할 수 없는 날짜는 val None으로 남긴다 —
    빼면 그날 조회가 직전 값을 집어 PBR이 계산된다(설계 §2: 그 날짜 PBR은 None)."""
    bmh = _bmh()
    if bmh.ASOF_REF is not None or not equity:
        return equity
    parent = _instants(cik, "StockholdersEquity")
    total = _instants(cik, "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest")
    nci = _instants(cik, "MinorityInterest")
    pref = _Pref(cik, ticker)
    out = []
    for e in equity:
        end, av, v = e["end"], e["available"], e["val"]
        pv = _val_at(parent, end, av)
        if pv is None or pv != v:
            tv = _val_at(total, end, av)
            if tv is not None and tv == v:
                n = _val_at(nci, end, av)
                if n is None:
                    # 같은 결산일 비지배지분이 없을 때: 400일 안에 보고가 있으면 그 값을 이어 쓰고(경고 — SO처럼 띄엄띄엄 내는 회사),
                    # 마지막 보고가 400일보다 오래됐거나 한 번도 없으면 비지배지분이 없어 보고를 멈춘 것으로 보고 0
                    # (설계 r8 — AVGO 2018·V 2011·SYK 2018 뒤로 총계 태그만, 우선주 이어 쓰기와 같은 400일)
                    recent = sorted([r for r in nci if r["end"] < end and r["filed"] <= av and _days(end, r["end"]) <= CARRY_DAYS],
                                    key=lambda r: (r["end"], r["filed"]))
                    if recent:
                        n = recent[-1]["val"]
                        _warn(f"{ticker} {end}: 같은 결산일 비지배지분 없음 — {recent[-1]['end']} 값 이어 씀")
                    else:
                        n = 0
                v = tv - n
        p = pref.p(end, av)
        if p is None:
            out.append(dict(e, val=None, pref=None))
            continue
        out.append(dict(e, val=v - p, pref=p))
    return out
