"""카드별 전환·교환 증권 표(안건 D28·D46·E35·E44, 설계 `research/shares_equity_design.md` r9 §3) — `v2/share_claims.json`.

원칙(§1): 어떤 증권을 보통주로 볼 때는 시가총액 주식 수 S에 더하고, 같은 증권을 EV 청구권·DCF 차감·자본 차감에서 뺀다. 한 증권은 한쪽으로만.
주식 수 쪽 `rows`는 날짜 d에 `filed ≤ d`인 가장 최근 행(첫 행 이전은 `backfill_first`일 때만 첫 값), 짝 금액 `paired`는 그날 엔진이 쓰는
재무상태표 관측의 결산일과 `end`가 같은 행(`carry_paired`면 그 이전 마지막 행, 아니면 ClaimHold — 그 종목 카드만 보류).
연구 모드(bmh.ASOF_REF)에서는 표를 읽지 않는다(§5 — 연구는 지금 상수 ECON_SHARES·SHARES_ADD를 DCF에만).
"""
import json
import os
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
SHARE_CLAIMS = os.path.join(HERE, "share_claims.json")
KINDS = {"exchange_units", "econ_shares", "conv_debt_net", "conv_debt_full", "conv_pref_fixed", "conv_pref_mandatory"}
ROW_FIELDS = {"econ_shares": ["econ_shares"], "exchange_units": ["units"], "conv_debt_net": ["principal", "conv_price"],
              "conv_debt_full": ["principal", "conv_price"], "conv_pref_fixed": ["conv_shares"],
              "conv_pref_mandatory": ["pref_shares", "liq_per_share", "min_rate", "max_rate", "initial_price", "threshold_price"]}
PAIRED_FIELDS = {"econ_shares": ["nci_remove", "ce_add"], "exchange_units": ["nci_remove", "ce_add"], "conv_debt_net": [],
                 "conv_debt_full": ["principal_in_debt"], "conv_pref_fixed": ["pref_ev", "dcf_pref", "pref_in_p", "ce_add"],
                 "conv_pref_mandatory": ["pref_ev", "dcf_pref", "pref_in_p"]}
# 짝 금액 칸 → 그 금액을 대조할 엔진 관측(그날 그 시리즈 관측의 결산일로 행을 찾는다)
PAIRED_OBS = {"nci_remove": "nci", "ce_add": "equity", "pref_in_p": "equity", "pref_ev": "preferred", "dcf_pref": "dcf_pref",
              "principal_in_debt": "debt"}

_cache = {}


class ClaimError(Exception):
    """표 형식 오류 — 불러오기에서 멈춘다."""


class ClaimHold(Exception):
    """짝 금액이 그 결산일에 없다 — 그 종목 카드만 보류(dq), 빌드 전체는 멈추지 않는다."""


def _bmh():
    import build_multiple_history as bmh
    return bmh


def _check(t, it):
    for k in ("id", "kind", "rows", "paired", "source"):
        if k not in it:
            raise ClaimError(f"{t} {it.get('id')}: 칸 없음 {k}")
    if it["kind"] not in KINDS:
        raise ClaimError(f"{t} {it['id']}: kind {it['kind']}")
    for r in it["rows"]:
        miss = [k for k in ["end", "filed", "wa_shares"] + ROW_FIELDS[it["kind"]] if k not in r]
        if miss:
            raise ClaimError(f"{t} {it['id']} {r.get('end')}: rows 칸 없음 {miss}")
    for r in it["paired"]:
        miss = [k for k in ["end", "filed"] + PAIRED_FIELDS[it["kind"]] if k not in r]
        if miss:
            raise ClaimError(f"{t} {it['id']} {r.get('end')}: paired 칸 없음 {miss}")
    if it.get("redeemed") and not it.get("redeemed_filed"):
        raise ClaimError(f"{t} {it['id']}: redeemed에는 redeemed_filed 필수")


def load(ticker):
    """그 종목 증권 목록 또는 None(표에 없거나 연구 모드)."""
    if _bmh().ASOF_REF is not None:
        return None
    if "_all" not in _cache:
        raw = json.load(open(SHARE_CLAIMS)) if os.path.exists(SHARE_CLAIMS) else {}
        _cache["_all"] = {k: v for k, v in raw.items() if not k.startswith("_")}
    items = _cache["_all"].get(ticker)
    if not items:
        return None
    if ticker not in _cache:
        for it in items:
            _check(ticker, it)
            it["rows"] = sorted(it["rows"], key=lambda r: (r["end"], r["filed"]))
            it["paired"] = sorted(it["paired"], key=lambda r: (r["end"], r["filed"]))
        _cache[ticker] = items
    return _cache[ticker]


def has(ticker):
    return load(ticker) is not None


def reset():
    _cache.clear()


def _row(it, d):
    c = [r for r in it["rows"] if r["filed"] <= d]
    if c:
        return max(c, key=lambda r: (r["end"], r["filed"]))
    if it.get("backfill_first") and it["rows"]:
        return it["rows"][0]
    return None


def _active(it, d):
    if it.get("start") and d < it["start"]:
        return False
    if it.get("redeemed_filed") and it["redeemed_filed"] <= d:
        return False                    # 현금 상환: 주식 수와 청구권을 같은 날 끝낸다(§3.3)
    return True


def _mandatory_rate(r, price):
    if price is None:
        return r["max_rate"]
    if price > r["threshold_price"]:
        return r["min_rate"]
    if price >= r["initial_price"]:
        return r["liq_per_share"] / price
    return r["max_rate"]


def _shares_of(it, r, price):
    k = it["kind"]
    if k == "econ_shares":
        return r["econ_shares"]
    if k == "exchange_units":
        return r["units"]
    if k == "conv_pref_fixed":
        return r["conv_shares"]
    if k == "conv_pref_mandatory":
        return r["pref_shares"] * _mandatory_rate(r, price)
    if r.get("converted_shares") is not None and not r["principal"]:
        return r["converted_shares"]     # 전환이 끝난 분기 — 가격·남은 원금으로 다시 계산하지 않고 실제 결제 주식(§3.3, Codex)
    n = r["principal"] / r["conv_price"]
    if price is None:
        return 0.0
    if k == "conv_debt_net":
        return max(0.0, n * (1 - r["conv_price"] / price))
    return n if price >= r["conv_price"] else 0.0       # conv_debt_full


def adjusted_shares(ticker, d, price, base, base_end, base_is_wa=False, wa_start=None, wa_end=None):
    """그날 시가총액 주식 수 — base(엔진 표지 또는 희석 가중평균)에 표를 적용한 값.

    base_end: base 관측의 결산일(표지면 표지 결산일). base_is_wa: base가 희석 가중평균(그 분기 wa_start~wa_end)이면 True —
    S = WA − Σ(그 분기 wa_shares) + Σ(날짜 d 주식 수)(§3.2). econ_shares는 어느 경우에도 S를 그 값으로 대체한다."""
    items = load(ticker)
    if not items or base is None:
        return base
    add, sub = 0.0, 0.0
    for it in items:
        if not _active(it, d):
            continue
        r = _row(it, d)
        if r is None:
            if it.get("start") and d >= it["start"]:
                raise ClaimHold(f"{ticker} {it['id']}: 발행({it['start']}) 뒤 {d}에 쓸 주식 수 행 없음(사건 행 필요)")
            if not it.get("start"):
                raise ClaimHold(f"{ticker} {it['id']}: {d}에 쓸 주식 수 행 없음(창 시작 전부터 있던 증권 — backfill_first 또는 이른 행)")
            continue
        if it["kind"] == "econ_shares":
            return float(r["econ_shares"])
        if base_is_wa:
            if it.get("converted") and wa_start and wa_start >= it["converted"]:
                continue                 # 그 분기 WA가 전환 주식을 보통주로 온전히 담음
            wr = [x for x in it["rows"] if x["end"] == wa_end and x["filed"] <= d]
            if not wr:
                if not (it.get("start") and wa_end < it["start"]):
                    raise ClaimHold(f"{ticker} {it['id']}: 희석 가중평균 대체 분기 {wa_end}의 wa_shares 행 없음")
            elif wr[-1]["wa_shares"] is None:
                raise ClaimHold(f"{ticker} {it['id']}: 희석 가중평균 대체 분기 {wa_end}의 wa_shares 미확인")
            else:
                sub += wr[-1]["wa_shares"]
        elif it.get("end_shares") and base_end and base_end >= it["end_shares"]:
            continue                     # 표지가 이미 전환 주식을 담음
        add += _shares_of(it, r, price)
    return base - sub + add


def claims(ticker, d, price, obs_end):
    """그날 엔진 관측(obs_end: {"equity", "nci", "preferred", "debt", "dcf_pref"} → 그 시리즈 관측 결산일, 시리즈가 없으면 None)에
    맞춘 짝 금액 합 {nci_remove, ce_add, pref_in_p, pref_ev, dcf_pref, principal_in_debt}. 같은 결산일 행이 없으면 carry_paired면
    이전 마지막 행, 아니면 ClaimHold."""
    out = {k: 0.0 for k in PAIRED_OBS}
    items = load(ticker)
    if not items:
        return out
    for it in items:
        if not _active(it, d):
            continue
        r = _row(it, d)
        for f in PAIRED_FIELDS[it["kind"]]:
            series = PAIRED_OBS[f]
            if series not in obs_end:
                continue                  # 이 호출자는 그 칸을 쓰지 않는다(배수 엔진에는 DCF 우선주 dcf_pref가 없다)
            e = obs_end[series]
            if e is None:
                # 짝 시리즈가 엔진에 없다(덮어쓰기로 비었음 — HPE) → 그 칸은 0이어야 한다(아니면 표 금액이 어디에도 실리지 않은 것)
                if any((p.get(f) or 0) != 0 for p in it["paired"] if p["filed"] <= d):
                    raise ClaimHold(f"{ticker} {it['id']}: {series} 시리즈가 엔진에 없는데 표 {f}가 0이 아님")
                continue
            if it.get("end_claims") and e >= it["end_claims"]:
                continue                  # 그 재무상태표 결산일에는 청구권이 이미 사라졌다
            if f == "principal_in_debt" and (r is None or price is None or price < r["conv_price"]):
                continue                  # conv_debt_full 외가격 — 원금은 차입금에 남는다
            same = [p for p in it["paired"] if p["end"] == e and p["filed"] <= d]
            if same:
                v = same[-1][f]
            elif it.get("carry_paired"):
                prior = [p for p in it["paired"] if p["end"] <= e and p["filed"] <= d]
                if not prior:
                    if it.get("start") and e < it["start"]:
                        continue          # 발행 전 결산일 — 그 증권은 아직 없었다
                    raise ClaimHold(f"{ticker} {it['id']}: carry_paired인데 {e} 이전 짝 행 없음")
                v = prior[-1][f]
            else:
                if it.get("start") and e < it["start"][:10] and not [p for p in it["paired"] if p["end"] <= e]:
                    continue              # 발행 전 결산일 — 그 증권은 아직 없었다
                raise ClaimHold(f"{ticker} {it['id']}: {series} 관측 결산일 {e}에 짝 금액 {f} 행 없음")
            if v is None:
                raise ClaimHold(f"{ticker} {it['id']}: {e} {f} 미확인")
            out[f] += v
    return out


def ce_extra(c):
    """CE에 더할 값 — ce_add + pref_in_p(P에서 그 증권을 되돌림) + 내가격 전부 주식 전환사채의 principal_in_debt(전환되면 자본)."""
    return c["ce_add"] + c["pref_in_p"] + c["principal_in_debt"]
