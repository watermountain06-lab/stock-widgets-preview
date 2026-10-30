"""일회성 손익 빼기 장치(안건 E54, 설계 `research/e54_v2_design.md` r13 — 1단계).

`v2/eps_oneoff.json`에는 회사 공시에서 찾은 **사실**만 둔다(6개 범주 항목, 계산 재료, 훑은 분기). 적용 여부는 엔진이
TTM 결산일 E마다 정한다 — 반복 판정(같은 범주가 8분기 중 3번 이상이면 빼지 않음 — 그 분기 그 범주 항목이 문턱을 넘을 때만 1번)
→ 크기 문턱(최근 4분기 EPS의 10% **그리고** 최근 4분기 매출의 1%) → 적용. 문턱 두 조건은 설계 r15(2026-10-30 사용자 결정).
1단계(12-01 v2.1 A-2 전)는 세 곳만 바꾼다: PER EPS(현재·자기 이력·밴드·백테스트), 현금흐름 세율, A8 본업 이익의 세율.
영업이익·이익률·D&A·EV/EBITDA는 바꾸지 않는다(설계 §12 — 이 경로의 코드는 만들지 않는다).

부호: 모든 adj 칸은 GAAP 숫자에 **더하면** 항목이 빠지는 값(손실 +, 이익 −). tax_oneoff.json과 같다.
연구 모드(`bmh.ASOF_REF`가 있을 때)에는 빈 목록 — 12-01 패널은 봉인된 GAAP 규칙을 그대로 쓴다(설계 §7).

입력 칸(종목마다 {"scan", "items"}):
- scan: quarters(훑은 결산일), sources, gain_scan: true, quarter_facts{q: ni_q(지배주주 귀속), eps_q(GAAP 희석, 공시 당시),
  shares_gaap_q(eps_q 분모), shares_basic_q, shares_adj_q(있으면), qf_filed(이 값들의 공시일 — 분할 기준)}
- item: id, quarter_end, filed, categories, line(opinc|pretax), adj_pretax, adj_tax, tax_basis, shares, shares_source,
  tags{pretax_dcf, pretax_includes, [core 종목] pretax_a8, pretax_a8_includes}, desc, source,
  선택: adj_eps·eps_shares(공시 주당 값), parent_share, out_of_scope_mixed, tax_source, tax_note·tax_source_filed(nontaxable),
  total_id·total_tax(disclosed_total), disclosed_anomalous, mismatch_note, opinc_includes·dda_includes_item(1단계 경고만)
"""
import json
import os
import re
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
EPS_ONEOFF = os.path.join(HERE, "eps_oneoff.json")

CATEGORIES = {"impairment", "divestiture", "litigation", "termination", "iprd", "restructuring"}
TAX_BASES = {"disclosed", "implied_from_eps", "equity_method", "nontaxable", "disclosed_total", "statutory_assumed"}
STATUTORY = 0.21
REPEAT_WINDOW = 8      # 반복 창: E로 끝나는 연속 8개 분기
REPEAT_MIN = 3         # 창 안에서 같은 범주가 있는 분기 수가 이 이상이면 반복
QUARTER_GAP_MAX = 160  # 창 안 이웃 결산일 간격이 이보다 길면 분기가 빠진 것 — 정상은 84~98일, 16주 4분기(COST·PEP) 112~130일, 한 분기 결손은 168일 이상
THRESHOLD = 0.10       # |A| ≥ 10% × max(|G|, |G + A|)
REV_FLOOR = 0.01       # 그리고 |Σ adj_pretax| ≥ 1% × 최근 4분기 매출 — 이익이 0 근처면 10% 문턱이 거의 0이 돼 작은 항목도 넘었다(CRWD $38M = 10.3%, r15)
EPS_TOL = 1e-9         # 문턱 경계(A = G/9 등)를 부동소수 오차로 떨어뜨리지 않게
PROOF_SUM_TOL = 0.011  # v1 3.1 (a) ttm_eps = 구성 4행 quarter_eps 합
PROOF_SPAN_DAYS = 310  # v1 3.1 (b) 첫~끝 결산일
PROOF_RANGE_DAYS = 400 # 증명을 할 항목 범위: E 행 결산일 − 항목 결산일 0~400일
NCI_LIMIT = 0.05       # 귀속 미공시 항목: 비지배 순이익이 최근 4분기 순이익의 5% 이상이면 적용하지 않음
FACT_TOL = 0.01        # quarter_facts 대조(주당 $0.01)
INPUT_TOL = (0.10, 0.006)  # 공시 주당 값 대 세후 금액(±10% 또는 주당 ±$0.006, v1 입력 검사)

_cache = {}
warnings = []          # 불러오기·적용 경고(카드 빌드 로그용). 오류는 예외로 멈춘다.


class OneoffError(Exception):
    pass


def _warn(msg):
    if msg not in warnings:
        warnings.append(msg)


def _bmh():
    import build_multiple_history as bmh
    return bmh


def research_mode():
    return _bmh().ASOF_REF is not None


def _days(a, b):
    return (date.fromisoformat(a) - date.fromisoformat(b)).days


def tag_names(label):
    """엔진 pick_tag 라벨("태그(행 수)" 또는 "A(71)+B(81)")을 태그명 집합으로. "NI+TAX"(순이익 + 법인세 합성)는 그대로."""
    if label is None:
        return set()
    if label == "NI+TAX":
        return {"NI+TAX"}
    return {re.sub(r"\(\d+\)$", "", x.strip()) for x in str(label).split("+") if x.strip()}


# ---------------------------------------------------------------- 불러오기와 검사(설계 §8)

def _check_item(t, it, scan_q, core):
    need = ["id", "quarter_end", "filed", "categories", "line", "adj_pretax", "adj_tax", "tax_basis", "shares", "shares_source",
            "tags", "desc", "source"]
    miss = [k for k in need if k not in it]
    if miss:
        raise OneoffError(f"{t} {it.get('id')}: 칸 없음 {miss}")
    if not it["categories"] or not set(it["categories"]) <= CATEGORIES:
        raise OneoffError(f"{t} {it['id']}: categories {it['categories']}는 6개 범주 밖")
    if it["line"] not in ("opinc", "pretax"):
        raise OneoffError(f"{t} {it['id']}: line {it['line']}")
    if it["tax_basis"] not in TAX_BASES:
        raise OneoffError(f"{t} {it['id']}: tax_basis {it['tax_basis']}")
    if not isinstance(it["shares"], int) or it["shares"] <= 0:
        raise OneoffError(f"{t} {it['id']}: shares는 주 단위 양의 정수")
    ps = it.get("parent_share", 1)
    if not 0 < ps <= 1:
        raise OneoffError(f"{t} {it['id']}: parent_share {ps}")
    if "adj_eps" in it and "eps_shares" not in it:
        raise OneoffError(f"{t} {it['id']}: 공시 adj_eps에는 eps_shares 필수")
    tags = it["tags"]
    if "pretax_dcf" not in tags or "pretax_includes" not in tags:
        raise OneoffError(f"{t} {it['id']}: tags.pretax_dcf·pretax_includes 필수")
    if core and ("pretax_a8" not in tags or "pretax_a8_includes" not in tags):
        raise OneoffError(f"{t} {it['id']}: core 종목은 tags.pretax_a8·pretax_a8_includes 필수(A8 세율 — DCF 증명으로 대신하지 않음)")
    if it["line"] == "opinc" and ("opinc_includes" not in it or "dda_includes_item" not in it):
        _warn(f"{t} {it['id']}: line=opinc인데 opinc_includes·dda_includes_item 없음(1단계는 경고만, 설계 §12)")
    if it["quarter_end"] not in scan_q:
        raise OneoffError(f"{t} {it['id']}: 항목 분기 {it['quarter_end']}가 scan.quarters에 없음")
    b, pre, tax = it["tax_basis"], it["adj_pretax"], it["adj_tax"]
    if b == "disclosed" and not it.get("tax_source"):
        raise OneoffError(f"{t} {it['id']}: disclosed 세금에는 tax_source 필수")
    if b == "implied_from_eps":
        if "adj_eps" not in it:
            raise OneoffError(f"{t} {it['id']}: implied_from_eps에는 공시 adj_eps 필수")
        want = pre - it["adj_eps"] * it["eps_shares"] / ps          # 설계 §5 순서 2
        if abs(tax - want) > max(1e6, 0.005 * abs(want)):
            raise OneoffError(f"{t} {it['id']}: implied_from_eps 세금 {tax:,.0f} ≠ 역산 {want:,.0f}")
    if b in ("equity_method", "nontaxable") and tax != 0:
        raise OneoffError(f"{t} {it['id']}: {b}는 adj_tax = 0")
    if b == "nontaxable" and not (it.get("tax_note") and it.get("tax_source_filed")):
        raise OneoffError(f"{t} {it['id']}: nontaxable에는 tax_note·tax_source_filed 필수")
    if b == "statutory_assumed" and abs(tax - STATUTORY * pre) > 0.005 * abs(pre):
        raise OneoffError(f"{t} {it['id']}: statutory_assumed 세금이 21%와 0.5% 넘게 다름")
    if b == "disclosed_total" and "total_id" not in it:
        raise OneoffError(f"{t} {it['id']}: disclosed_total에는 total_id 필수")
    # 이상 공시: 세금이 세전보다 크거나 부호가 다르면(공시 세금) 경고만 — disclosed_anomalous로 표시(설계 §5)
    if b == "disclosed" and pre and tax and (abs(tax) > abs(pre) or (tax > 0) != (pre > 0)):
        _warn(f"{t} {it['id']}: 공시 세금이 세전보다 크거나 부호가 다름" + ("" if it.get("disclosed_anomalous") else " — disclosed_anomalous 표시 없음"))
    # 공시 주당 값과 세후 금액: 부호가 다르면 공시 세금이면 경고·추정 세금이면 오류, 크기가 허용 폭 밖이면 경고(mismatch_note)
    if "adj_eps" in it and b != "implied_from_eps":
        after = (pre - tax) * ps
        per = it["adj_eps"] * it["eps_shares"]
        if it["adj_eps"] != 0 and after != 0 and (it["adj_eps"] > 0) != (after > 0):
            if b == "disclosed" or it.get("disclosed_anomalous"):
                _warn(f"{t} {it['id']}: 공시 주당 값과 세후 금액 부호가 다름 — {it.get('mismatch_note', 'mismatch_note 없음')}")
            else:
                raise OneoffError(f"{t} {it['id']}: 추정 세금({b})인데 공시 주당 값과 부호가 다름 — 순서 2(implied_from_eps)로")
        elif abs(per - after) > max(INPUT_TOL[0] * abs(after), INPUT_TOL[1] * it["eps_shares"]):
            if b in ("disclosed_total", "statutory_assumed"):
                raise OneoffError(f"{t} {it['id']}: 추정 세금({b})이 공시 주당 값과 허용 폭 밖 — 순서 2(implied_from_eps)로(설계 §9)")
            _warn(f"{t} {it['id']}: 공시 주당 값 × 주식 {per:,.0f} 대 세후 {after:,.0f} — 허용 폭 밖"
                  + ("" if it.get("mismatch_note") else " (mismatch_note 없음)"))


def _check_totals(t, items):
    """disclosed_total: 총액 − (1~4 세금)을 남은 항목의 세전 비율로 나눈 값이어야 한다. 남은 항목 없음·부호 섞임·세전 합 0이면 쓰지 않는다."""
    groups = {}
    for it in items:
        if it.get("total_id"):
            groups.setdefault(it["total_id"], []).append(it)
    for gid, g in groups.items():
        tot = [it["total_tax"] for it in g if "total_tax" in it]
        if len(tot) != 1:
            raise OneoffError(f"{t} total_id {gid}: total_tax(총액)는 한 항목에 한 번")
        fixed = [it for it in g if it["tax_basis"] != "disclosed_total"]
        rest = [it for it in g if it["tax_basis"] == "disclosed_total"]
        if not rest:
            raise OneoffError(f"{t} total_id {gid}: 남은(disclosed_total) 항목 없음 — 순서 6")
        pres = [it["adj_pretax"] for it in rest]
        if sum(pres) == 0 or (min(pres) < 0 < max(pres)):
            raise OneoffError(f"{t} total_id {gid}: 남은 항목 세전 합 0 또는 부호 섞임 — 순서 6")
        remain = tot[0] - sum(it["adj_tax"] for it in fixed)
        for it in rest:
            want = remain * it["adj_pretax"] / sum(pres)
            if abs(it["adj_tax"] - want) > max(1e6, 0.005 * abs(want)):
                raise OneoffError(f"{t} {it['id']}: 총액 배분 {it['adj_tax']:,.0f} ≠ 세전 비율 {want:,.0f}")


def _check_facts(t, scan, items):
    facts = scan.get("quarter_facts") or {}
    need = ["ni_q", "eps_q", "shares_gaap_q", "shares_basic_q", "qf_filed"]
    for q, f in facts.items():
        miss = [k for k in need if k not in f]
        if miss:
            raise OneoffError(f"{t} quarter_facts {q}: 칸 없음 {miss}")
        for it in items:
            if it["quarter_end"] == q and it["shares"] != f["shares_gaap_q"]:
                raise OneoffError(f"{t} {it['id']}: shares {it['shares']} ≠ quarter_facts shares_gaap_q {f['shares_gaap_q']}")
        if abs(f["ni_q"] / f["shares_gaap_q"] - f["eps_q"]) > FACT_TOL:
            _warn(f"{t} {q}: ni_q ÷ shares_gaap_q {f['ni_q'] / f['shares_gaap_q']:.4f} 대 eps_q {f['eps_q']} — 같은 공시 기준인지 확인")
    rows = eps_rows_for(t)
    if rows:
        sp = _splits(t)
        _, byq = _rows_by_q(rows)
        for q, f in facts.items():
            r = byq.get(q)
            if r and r[0].get("quarter_eps") is not None:
                d = round(abs(f["eps_q"] / _split_ratio(f["qf_filed"], sp) - r[0]["quarter_eps"]), 4)
                if d > FACT_TOL:
                    _warn(f"{t} {q}: eps_q가 EPS 파일 분기값과 {d} 다름(fp {r[0].get('fp')})")


def load(ticker):
    """그 종목의 {"items", "scan"} — 파일에 없거나 연구 모드면 None. 형식이 틀리면 멈춘다."""
    if research_mode():
        return None
    if "_all" not in _cache:
        raw = json.load(open(EPS_ONEOFF)) if os.path.exists(EPS_ONEOFF) else {}
        _cache["_all"] = {k: v for k, v in raw.items() if not k.startswith("_")}
    rec = _cache["_all"].get(ticker)
    if not rec:
        return None
    if ticker in _cache:
        return _cache[ticker]
    scan = rec.get("scan") or {}
    if not scan.get("quarters") or not scan.get("sources") or scan.get("gain_scan") is not True:
        raise OneoffError(f"{ticker}: scan(quarters·sources·gain_scan: true) 필수")
    items = rec.get("items", [])
    ids = [it.get("id") for it in items]
    if len(ids) != len(set(ids)):
        raise OneoffError(f"{ticker}: id 중복")
    keys = [(it.get("quarter_end"), it.get("desc")) for it in items]
    if len(keys) != len(set(keys)):
        raise OneoffError(f"{ticker}: (quarter_end, desc) 중복")
    core = ticker in _bmh().core_tickers()
    for it in items:
        _check_item(ticker, it, set(scan["quarters"]), core)
    _check_totals(ticker, items)
    _check_two_files(ticker, items)
    _check_facts(ticker, scan, items)
    out = {"items": items, "scan": scan}
    _cache[ticker] = out
    return out


def _tax_oneoff_all(ticker):
    bmh = _bmh()
    key = ("_tax", bmh.TAX_ONEOFF)
    if key not in _cache:
        _cache[key] = json.load(open(bmh.TAX_ONEOFF)) if os.path.exists(bmh.TAX_ONEOFF) else {}
    return _cache[key].get(ticker, [])


def _check_two_files(ticker, items):
    """tax_oneoff.json 같은 종목·분기에 pretax 칸이 있으면(값이 0이어도) 오류(설계 §6 "두 파일")."""
    tq = {x["quarter_end"] for x in _tax_oneoff_all(ticker) if "pretax" in x}
    clash = sorted({it["quarter_end"] for it in items} & tq)
    if clash:
        raise OneoffError(f"{ticker}: tax_oneoff.json pretax 칸과 같은 분기 {clash}")


def reset():
    _cache.clear()
    warnings.clear()


# ---------------------------------------------------------------- 세금·주당 값(설계 §5)

def _splits(ticker):
    """EPS 파일을 만든 것과 같은 분할 목록(fetch_eps_history.KNOWN_SPLITS) — 출처가 다르면 A·Δ가 파일과 어긋난다(Fable)."""
    import fetch_eps_history as feh
    return feh.KNOWN_SPLITS.get(ticker, [])


def _split_ratio(filed, sp):
    import fetch_eps_history as feh
    return feh.split_ratio(filed, sp) if sp else 1


def item_tax(it, cap):
    """그 cap에서 쓸 adj_tax. 비과세(순서 4)가 cap 뒤에 확인됐으면 그 전 계산은 법정 21% 추정(설계 §5 — tax_source_filed)."""
    if it["tax_basis"] == "nontaxable" and it.get("tax_source_filed", "") > cap:
        return STATUTORY * it["adj_pretax"]
    return it["adj_tax"]


def adj_eps_gaap(it, cap):
    """GAAP 분모 기준 세후 주당 영향(공시 당시 주식 기준 — 분할 보정은 합칠 때)."""
    if "adj_eps" in it:
        return it["adj_eps"] * it["eps_shares"] / it["shares"]
    return (it["adj_pretax"] - item_tax(it, cap)) * it.get("parent_share", 1) / it["shares"]


def _nci_blocked(ticker, it):
    """귀속을 밝히지 않은 항목은 그 종목 비지배 순이익이 최근 4분기 순이익의 5% 이상이면 쓰지 않는다(nci_unknown)."""
    if "parent_share" in it:
        return False
    key = ("_nci", ticker, it["quarter_end"])
    if key in _cache:
        return _cache[key]
    bmh = _bmh()
    import fetch_eps_history as feh
    cik = feh.CIKS.get(ticker)
    blocked = False
    if cik:
        def ttm_at(tags):
            _, rows = bmh.pick_tag(cik, tags)
            if not rows:
                return None
            s = [e for e in bmh.ttm_series(bmh.quarterly_flow(rows, ticker)) if e["end"] <= it["quarter_end"]]
            return s[-1]["val"] if s and s[-1]["end"] == it["quarter_end"] else None
        nci = ttm_at(["NetIncomeLossAttributableToNoncontrollingInterest"])
        ni = ttm_at(["NetIncomeLoss"])
        if nci is not None and ni is not None and nci != 0 and (ni == 0 or abs(nci) >= NCI_LIMIT * abs(ni)):
            _warn(f"{ticker} {it['id']}: 비지배 순이익 {nci:,.0f} 대 순이익 {ni:,.0f} — 귀속(parent_share) 미공시라 적용 안 함(nci_unknown)")
            blocked = True
    _cache[key] = blocked
    return blocked


# ---------------------------------------------------------------- EPS 파일 구성 분기(v1 3.1)

def _rows_by_q(eps_rows):
    rows = sorted([e for e in eps_rows if e.get("quarter_end")], key=lambda e: (e["quarter_end"], e.get("available_date", "")))
    byq = {}
    for e in rows:
        byq.setdefault(e["quarter_end"], []).append(e)
    return rows, byq


def _ordered_quarters(eps_rows):
    return sorted({e["quarter_end"] for e in eps_rows if e.get("quarter_end")})


def proof(eps_rows, E):
    """E 행과 구성 4분기 결산일 — v1 3.1 (a) 합 ±0.011 (b) 첫~끝 ≤ 310일. 못 넘으면 None.

    E 결산일 행이 둘 이상이면 증명을 넘는 행 하나를 쓰고, 둘 다 넘으면 오류. 구성 분기(E 앞 3개)에 행이 둘 이상이면 증명 실패."""
    qs = _ordered_quarters(eps_rows)
    if E not in qs:
        return None
    i = qs.index(E)
    if i < 3:
        return None
    four = qs[i - 3:i + 1]
    _, byq = _rows_by_q(eps_rows)
    if any(len(byq[q]) != 1 for q in four[:3]):
        return None
    if _days(four[-1], four[0]) > PROOF_SPAN_DAYS:
        return None
    vals = [byq[q][0].get("quarter_eps") for q in four[:3]]
    if None in vals:
        return None
    ok = [r for r in byq[E] if r.get("quarter_eps") is not None and r.get("ttm_eps") is not None
          and abs(sum(vals) + r["quarter_eps"] - r["ttm_eps"]) <= PROOF_SUM_TOL]
    if len(ok) > 1:
        raise OneoffError(f"{E}: 같은 결산일 EPS 행 둘 이상이 모두 증명을 넘음")
    return (ok[0], four) if ok else None


# ---------------------------------------------------------------- 판정(설계 §3·§4)과 EPS 조정

def _cap(ticker, cap):
    return cap or date.today().isoformat()


def judge(ticker, eps_rows, E, cap=None):
    """TTM 결산일 E의 판정 — {"applied": [항목], "four": [구성 결산일], "row": E 행} 또는 None(조정 없음).

    eps_rows는 그 종목 EPS 파일 전체 행(구성 분기·반복 창은 분기 달력이다). 판정 대상 E 행은 공시일이 cap 이하여야 한다."""
    rec = load(ticker)
    if not rec:
        return None
    cap = _cap(ticker, cap)
    key = ("_judge", ticker, E, cap, _fingerprint(eps_rows))
    if key in _cache:
        return _cache[key]
    _cache[key] = res = _judge(ticker, rec, eps_rows, E, cap)
    return res


def _fingerprint(eps_rows):
    """판정 캐시 키 — 리스트 id는 해제 뒤 재사용될 수 있어 내용으로 만든다(Fable)."""
    return hash(tuple((e.get("quarter_end"), e.get("available_date"), e.get("ttm_eps"), e.get("quarter_eps")) for e in eps_rows))


def _judge(ticker, rec, eps_rows, E, cap):
    items = [it for it in rec["items"] if it["filed"] <= cap]
    near = [it for it in items if 0 <= _days(E, it["quarter_end"]) <= PROOF_RANGE_DAYS]
    if not near:
        return None
    same = [e for e in eps_rows if e.get("quarter_end") == E and e.get("available_date", "") <= cap]
    if not same:
        _warn(f"{ticker} {E}: cap {cap}까지 공개된 EPS 파일 행 없음 — 조정 안 함")
        return None
    if _ordered_quarters(eps_rows).index(E) < 3:
        # E 앞 고유 결산 분기가 3개 미만(분사·상장 직후 — 파일 첫 세 분기)이면 구성 분기를 증명할 수 없다. 깨진 파일이 아니므로 오류가 아니라
        # 조정 안 함 + 경고(E 행이 없을 때와 같은 처리, 2026-10-29 CARR 시범 — 2019-12~2020-06). 같은 결산일 행이 둘이면 그대로 오류.
        if len(same) > 1:
            raise OneoffError(f"{ticker} {E}: 같은 결산일 EPS 행 둘 이상(파일 첫 세 분기)")
        _warn(f"{ticker} {E}: E 앞 결산 분기가 3개 미만 — 조정 안 함")
        return None
    pr = proof([e for e in eps_rows if e.get("quarter_end") != E] + same, E)
    if pr is None:
        raise OneoffError(f"{ticker} {E}: EPS 파일 구성 분기 증명 실패(v1 3.1 — 합 ±0.011·310일)")
    row, four = pr
    scan_q = set(rec["scan"]["quarters"])
    qs = _ordered_quarters(eps_rows)
    i = qs.index(E)
    window = qs[max(0, i - REPEAT_WINDOW + 1):i + 1]
    gaps = [_days(b, a) for a, b in zip(window, window[1:])]
    if len(window) < REPEAT_WINDOW or max(gaps) > QUARTER_GAP_MAX:
        _warn(f"{ticker} {E}: 반복 창이 연속 8분기가 아님(파일 분기 부족·결손) — 조정 안 함")
        return None
    if not set(window) <= scan_q:
        return None                      # 안 훑은 분기가 창에 있으면 판정하지 않는다(0번으로 세지 않음)
    bmh = _bmh()
    sp = _splits(ticker)
    G = row["ttm_eps"] + bmh.oneoff_in_ttm(ticker, E, "eps")
    rev = revenue_ttm(ticker, E, cap)
    if rev is None:
        _warn(f"{ticker} {E}: 최근 4분기 매출 없음 — 매출 1% 바닥 없이 판정")
    floor_usd = REV_FLOOR * abs(rev) if rev else 0.0
    # 반복 셈(r15, 2026-10-30 사용자 결정): 그 분기 그 범주 항목의 합이 문턱(E의 |G| 10%, 그리고 매출 1%)을 넘을 때만 1번.
    # 예전에는 크기를 보지 않아 매 분기 소액 IPR&D·처분 손익이 큰 일회성까지 반복으로 만들었다(MRK IPR&D $13.8B, E54 입구 선별).
    sums = {}
    for it in items:
        if it["quarter_end"] in window:
            for c in set(it["categories"]):
                s_ = sums.setdefault((c, it["quarter_end"]), [0.0, 0.0])
                s_[0] += adj_eps_gaap(it, cap) / _split_ratio(it["filed"], sp)
                s_[1] += it["adj_pretax"]
    counts = {}
    for (c, q), (e_, u_) in sums.items():
        if abs(e_) + EPS_TOL >= THRESHOLD * abs(G) and abs(u_) >= floor_usd and (e_ or u_):
            counts.setdefault(c, set()).add(q)
    repeat = {c for c, qset in counts.items() if len(qset) >= REPEAT_MIN}
    cand = [it for it in items if it["quarter_end"] in four and not (set(it["categories"]) & repeat)
            and not it.get("out_of_scope_mixed") and not _nci_blocked(ticker, it)]
    if not cand:
        return None
    A = sum(adj_eps_gaap(it, cap) / _split_ratio(it["filed"], sp) for it in cand)
    if A == 0:
        return None
    if abs(A) + EPS_TOL < THRESHOLD * max(abs(G), abs(G + A)):
        return None
    if abs(sum(it["adj_pretax"] for it in cand)) < floor_usd:
        return None                      # 매출 1% 바닥(r15)
    return {"applied": cand, "four": four, "row": row, "A": A, "G": G}


def revenue_ttm(ticker, E, cap):
    """엔진 매출 TTM(FLOW_TAGS revenue → quarterly_flow → ttm_series) 가운데 결산일 E, 공개일 ≤ cap인 값. 없으면 None."""
    key = ("_rev", ticker, E, cap)
    if key not in _cache:
        import fetch_eps_history as feh
        bmh = _bmh()
        cik = feh.CIKS.get(ticker)
        v = None
        if cik:
            _, rows = bmh.pick_tag(cik, bmh.FLOW_TAGS["revenue"])
            # cap 뒤 공시(재작성)를 분기화 **전에** 버린다 — 재작성 종목(RESTATED_LATEST)은 quarterly_flow가 최신 값에 최초 공시일을
            # 붙여, 계산 뒤 공개일 검사로는 cap 뒤 재작성 값이 통과했다(Codex r15)
            rows = [e for e in rows if e.get("filed", "") <= cap]
            if rows:
                ok = [e for e in bmh.ttm_series(bmh.quarterly_flow(rows, ticker)) if e["end"] == E and e["available"] <= cap]
                v = ok[-1]["val"] if ok else None
        _cache[key] = v
    return _cache[key]


def _tax_oneoff_items(ticker, E, q):
    """엔진 카드 EPS 읽기가 E에 실제로 더한 tax_oneoff 항목 중 결산일이 q인 것(같은 호출 — asof 없이 330일 창)."""
    return [it for it in _tax_oneoff_all(ticker) if 0 <= _days(E, it["quarter_end"]) < 330 and it["quarter_end"] == q]


def eps_adjust(ticker, eps_rows, E, cap=None, row=None):
    """E 행 ttm_eps에 더할 값(오늘 주식 기준). 엔진은 이미 tax_oneoff eps를 더했다 — 분모가 바뀐 분기는 그 몫을 빼고 Δ_q로 대신한다.

    row: 엔진이 조정하려는 그 행. 같은 결산일 행이 둘 이상이면 판정이 고른(증명을 넘은) 행에만 조정을 붙인다(Codex r2)."""
    j = judge(ticker, eps_rows, E, cap)
    if not j:
        return 0.0
    _k = lambda r: (r.get("available_date"), r.get("ttm_eps"), r.get("quarter_eps"), r.get("fp"), r.get("accn"))
    if row is not None and row is not j["row"] and _k(row) != _k(j["row"]):
        _warn(f"{ticker} {E}: 증명을 넘지 못한 같은 결산일 행({row.get('available_date')}) — 조정 안 함")
        return 0.0
    cap = _cap(ticker, cap)
    rec = load(ticker)
    facts = rec["scan"].get("quarter_facts", {})
    sp = _splits(ticker)
    _, byq = _rows_by_q(eps_rows)
    total = 0.0
    for q in j["four"]:
        its = [it for it in j["applied"] if it["quarter_end"] == q]
        tax_its = _tax_oneoff_items(ticker, E, q)
        simple = sum(adj_eps_gaap(it, cap) / _split_ratio(it["filed"], sp) for it in its)
        file_row = j["row"] if q == E else byq[q][0]
        fq = file_row.get("quarter_eps")
        t_eps = sum(x.get("eps", 0) for x in tax_its)
        f = facts.get(q)
        if not f:
            # 분모가 바뀔 수 있는 분기(GAAP 분기 EPS와 조정 뒤 부호가 다름 — tax_oneoff 몫 포함)는 사실 입력이 필수
            if (its or t_eps) and fq is not None and (fq > 0) != (fq + simple + t_eps > 0):
                raise OneoffError(f"{ticker} {q}: 분모가 바뀔 수 있는 분기인데 scan.quarter_facts 없음")
            total += simple
            continue
        r = _split_ratio(f["qf_filed"], sp)
        T = t_eps * r * f["shares_gaap_q"]
        N = f["ni_q"] + sum((it["adj_pretax"] - item_tax(it, cap)) * it.get("parent_share", 1) for it in its) + T
        S = f["shares_gaap_q"]
        if f["ni_q"] < 0 < N:
            if not f.get("shares_adj_q"):
                _warn(f"{ticker} {q}: 적자 → 흑자인데 회사 조정 EPS 주식 수 없음 — 분모 그대로(단순 합)")
                total += simple
                continue
            S = f["shares_adj_q"]
        elif f["ni_q"] > 0 > N:
            S = f["shares_basic_q"]
        if S == f["shares_gaap_q"]:
            total += simple
            continue
        # 기준 일치 검사(설계 §5 분모 5): 손입력 eps_q가 파일 분기값과 같은 공시 기준인지. 보고 분기(Q1~Q4)는 계산 조건,
        # 파생 분기(연간·누계 − 앞 분기, fp …derived)와 그 밖 표기(FY·Q)는 경고만 — 보고 분기 EPS와 다른 것이 정상이라.
        diff = round(abs(f["eps_q"] / r - fq), 4)
        strict = str(file_row.get("fp", "")) in ("Q1", "Q2", "Q3", "Q4")
        if diff > FACT_TOL:
            if strict:
                _warn(f"{ticker} {q}: eps_q {f['eps_q']} ÷ 분할 {r}가 파일 {fq}와 다름 — 분모 그대로(단순 합)")
                total += simple
                continue
            _warn(f"{ticker} {q}: 파생·기타 분기(fp {file_row.get('fp')}) — eps_q와 파일 값 차이 {diff}(경고만)")
        delta = N / S / r - fq
        total += delta - t_eps
    return total


# ---------------------------------------------------------------- 세율(설계 §6 둘째 줄, §12 A8)

def tax_adjust(ticker, eps_rows, E, chosen_label, which, cap=None, tax_quarters=None):
    """세율 TTM 결산일 E에 더할 (Σadj_pretax, Σadj_tax, 항목 id) — 적용된 항목 중 세전 태그가 그 항목을 담는 것만.

    which: "dcf"(tags.pretax_dcf) 또는 "a8"(tags.pretax_a8). E와 결산일이 같은 EPS 파일 행의 판정을 쓴다.
    chosen_label: 엔진 pick_tag 라벨(행 수 표시는 떼고 대조). tax_quarters: 세금·세전 TTM의 구성 결산일 — 항목 분기가
    그 안에 있어야 한다(v1 3.1, 없으면 그 항목은 세율에 넣지 않고 경고)."""
    j = judge(ticker, eps_rows, E, cap) if eps_rows is not None else None
    if not j:
        return None
    cap = _cap(ticker, cap)
    key, inc_key = ("pretax_dcf", "pretax_includes") if which == "dcf" else ("pretax_a8", "pretax_a8_includes")
    chosen = tag_names(chosen_label)
    pre = tax = 0.0
    used = []
    for it in j["applied"]:
        decl = it["tags"].get(key)
        if decl is None:
            raise OneoffError(f"{ticker} {it['id']}: tags.{key} 없음")
        if decl not in chosen:
            raise OneoffError(f"{ticker} {it['id']}: 선언한 세전 태그 {decl} ∉ 엔진 선택 {sorted(chosen)}")
        if len(chosen) > 1 and not _tag_has_quarter(ticker, [decl], it["quarter_end"]):
            # 여러 태그를 이어 쓰는 종목은 그 분기를 실제로 공급한 태그를 적어야 포함 증명이 뜻을 가진다(Fable r2).
            # 단 연중에 태그를 바꿔 그 분기가 합친 흐름에만 있으면(연간 − 3분기 합성 — AMGN·ITW·XYL 4분기) 어느 태그도 공급하지 않으므로 경고만(Fable r3).
            if not any(_tag_has_quarter(ticker, [x], it["quarter_end"]) for x in chosen - {decl}) \
                    and _tag_has_quarter(ticker, sorted(chosen), it["quarter_end"]):
                _warn(f"{ticker} {it['id']}: {it['quarter_end']}는 합친 세전 흐름에만 있음(태그 전환 분기) — 선언 태그 {decl} 대조는 경고만")
            else:
                raise OneoffError(f"{ticker} {it['id']}: 선언한 세전 태그 {decl}에 {it['quarter_end']} 분기 값이 없음 — 그 분기를 공급한 태그를 적을 것")
        if not it["tags"].get(inc_key):
            continue
        if tax_quarters is not None and it["quarter_end"] not in tax_quarters:
            _warn(f"{ticker} {it['id']}: 세금 TTM 구성 분기 {tax_quarters}에 없음 — 세율에 넣지 않음")
            continue
        pre += it["adj_pretax"]
        tax += item_tax(it, cap)
        used.append(it["id"])
    return (pre, tax, used) if used else None


def _tag_has_quarter(ticker, tags, q):
    """태그(들)의 분기 흐름에 결산일 q가 있는지 — (ticker, 태그, q)마다 한 번만 계산(core_earnings가 날마다 부른다)."""
    key = ("_tagq", ticker, tuple(sorted(tags)), q)
    if key in _cache:
        return _cache[key]
    import fetch_eps_history as feh
    cik = feh.CIKS.get(ticker)
    if not cik:
        return True                      # 시험용 가짜 종목
    bmh = _bmh()
    _, rows = bmh.pick_tag(cik, list(tags))
    _cache[key] = any(e["end"] == q for e in bmh.quarterly_flow(rows, ticker)) if rows else False
    return _cache[key]


def a8_rate(o, pt, tx, pre_off, tax_off, addback, ea):
    """A8 본업 이익 세율 — 이 장치 항목이 그 결산일에 적용됐을 때의 순서(설계 §12): o ≤ 0이면 None, 조정 세전 > 0이면 조정 세율,
    아니면 GAAP 세전 > 0일 때만 GAAP 세율, 아니면 None. 적용된 항목이 없으면 엔진은 이 함수를 부르지 않는다(지금 코드 그대로)."""
    if o <= 0:
        return None
    pa = pt - pre_off + addback + ea[0]
    ta = tx - tax_off + ea[1]
    if pa > 0:
        return ta / pa
    if pt > 0:
        return tx / pt
    return None


def ttm_quarters(quarters, E):
    """분기 흐름 목록(quarterly_flow)에서 E로 끝나는 연속 4분기 결산일 — ttm_series와 같은 창(첫~끝 310일). 없으면 None."""
    ends = sorted({q["end"] for q in quarters if q["end"] <= E})
    if not ends or ends[-1] != E or len(ends) < 4:
        return None
    four = ends[-4:]
    return four if _days(four[-1], four[0]) <= PROOF_SPAN_DAYS else None


def eps_rows_for(ticker):
    """카드 EPS 파일 행(scripts/<T>_eps_history.json) — 세율 경로가 판정을 빌려 쓸 때."""
    key = ("_rows", ticker)
    if key not in _cache:
        p = os.path.join(os.path.dirname(HERE), "scripts", f"{ticker}_eps_history.json")
        _cache[key] = json.load(open(p)) if os.path.exists(p) else None
    return _cache[key]


def has(ticker):
    return load(ticker) is not None
