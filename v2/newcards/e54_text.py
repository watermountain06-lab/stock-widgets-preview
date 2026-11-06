"""일회성 손익 장치(안건 E54, v2/eps_oneoff.py)가 이 카드에서 실제로 뺀 것을 카드 문장으로 적는다(설계 e54_v2_design §12 '카드 문장').

- 자기 이력 설명(SELF_TIP): 최근 4분기 PER에서 뺀 항목과 조정 전 → 조정 뒤 EPS, 지난 이력 구간 중 조정된 결산일 수.
- 현금흐름 설명(DCF_NOTE): 세율을 조정했을 때만 한 문장.
- 이익률·EV/EBITDA는 GAAP 그대로라는 것, 영업이익 안의 항목은 이익률에 남아 있다는 것.
행 선택(as_of_entry)·최종 EPS(eps_adjust)는 엔진(build_multiple_history 3078~3093)과 같은 함수로 다시 센다 — 숫자를 손으로 쓰지 않는다(Codex r1)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import eps_oneoff as eo  # noqa: E402

CAT = {"impairment": "손상", "divestiture": "사업 매각", "litigation": "소송", "termination": "계약 해지",
       "iprd": "인수 연구개발(IPR&D)", "restructuring": "구조조정"}


def _ql(q):
    return f"{q[:4]}.{q[5:7]}"


def _mn(v):
    v = abs(v) / 1e6
    return f"${v / 1000:.1f}B" if v >= 1000 else f"${v:,.0f}M"


def _usd(v):
    return ("−" if v < 0 else "") + f"${abs(v):.2f}"


def facts(T, cik, window, bmh):
    """{'cur': {'E', 'before', 'after', 'items'} 또는 None, 'hist': [조정된 결산일]} — 장치가 없으면 None."""
    if not eo.has(T):
        return None
    rows = eo.eps_rows_for(T) or []
    cap = bmh._approved().get(str(cik).zfill(10))
    # 엔진과 같은 목록: cap 이하 공시, 장치 종목은 EPS 0 행도 — 공개일 순서
    ser = sorted(({"available": e["available_date"], "end": e.get("quarter_end"), "row": e} for e in rows
                  if e.get("ttm_eps") is not None and (not cap or e["available_date"] <= cap)), key=lambda x: x["available"])
    if not ser:
        return None
    adj = lambda x: eo.eps_adjust(T, rows, x["end"], cap, row=x["row"]) if x.get("end") else 0.0
    cur_x = bmh.as_of_entry(ser, window[1])
    # 이력 창 안에서 그날그날 엔진이 고른 행(창 시작일과 창 안 공개일마다)
    days = [window[0]] + sorted({x["available"] for x in ser if window[0] < x["available"] <= window[1]})
    seen, hist = set(), []
    for d in days:
        x = bmh.as_of_entry(ser, d)
        if x is None or x is cur_x or id(x) in seen:
            continue
        seen.add(id(x))
        if adj(x):
            hist.append(x["end"])
    cur = None
    if cur_x is not None and cur_x.get("end"):
        a = adj(cur_x)
        if a:
            e = cur_x["row"]
            tx = bmh.oneoff_in_ttm(T, e["quarter_end"], "eps")                            # 일회성 세금(tax_oneoff)
            dc = bmh.disc_in_ttm(T, rows, e["quarter_end"], e["available_date"])           # 중단영업(E62)
            before = e["ttm_eps"] + tx + dc
            j = eo.judge(T, rows, e["quarter_end"], cap)
            sp = eo._splits(T)
            cur = {"E": e["quarter_end"], "raw": e["ttm_eps"], "tx": tx, "dc": dc, "before": before, "after": before + a,
                   "items": [(it, eo.adj_eps_gaap(it, cap) / eo._split_ratio(it["filed"], sp)) for it in j["applied"]]}
    return {"cur": cur, "hist": sorted(hist)}


def sentences(f, tax_on, basis="diluted"):
    """(자기 이력 문장, 현금흐름 문장)."""
    if not f or (not f["cur"] and not f["hist"]):
        return "", ""
    s = []
    c = f["cur"]
    tail = ("반복 기준(최근 8분기 중 문턱을 넘은 분기가 3번 이상이거나 6번 이상 나온 범주)에 걸린 항목과 인수 통합 비용은 빼지 않는다. "
            "영업이익률·EV/EBITDA는 GAAP 그대로다.")
    opin = c and any(it.get("line") == "opinc" for it, _ in c["items"])
    if basis != "diluted":
        # 본업 PER 카드(core 등)는 희석 EPS 조정이 PER에 쓰이지 않는다 — 장치는 본업 이익의 세율에만 닿는다(Codex r1, SNPS)
        if c:
            s.append("이 카드의 PER은 본업 이익 기준이라, PER 쪽에서는 일회성 손익 조정을 본업 이익에 쓰는 세율에만 반영했다.")
        s.append(tail)
        if opin:   # 설계 §12는 PER 기준과 상관없이 적는다 — 본업 이익 자체에 남는다(Fable r1)
            s.append("영업이익 안에 있는 항목의 손익은 이익률과 본업 이익에 그대로 남아 있다.")
        d = "현금흐름 세율도 일회성 항목을 뺀 세전이익·세금으로 계산했다(이익률은 GAAP)." if (c and tax_on) else ""
        return " ".join(s), d
    if c:
        grp = {}
        for it, _ in c["items"]:
            k = (it["quarter_end"], tuple(it["categories"]), it["adj_pretax"] < 0)
            grp[k] = grp.get(k, 0.0) + it["adj_pretax"]
        its = sorted(grp.items(), key=lambda x: -abs(x[1]))

        def lab(cats, gain):
            return "·".join(CAT[x] for x in cats) + (" 이익" if gain else " 손실" if cats == ("divestiture",) else " 비용")
        lst = ", ".join(f"{_ql(q)} 분기 {lab(cats, gain)} 세전 {_mn(v)}" for (q, cats, gain), v in its[:4])
        more = f" 외 {len(its) - 4}묶음" if len(its) > 4 else ""
        pre = []   # 조정 전 값이 공시 희석 EPS와 다르면 그 단계를 밝힌다(SBUX 일회성 세금, Fable r1)
        if abs(c["tx"]) >= 0.005:   # tx > 0: 일회성 세금 비용을 되돌림, tx < 0: 일회성 세금 이익을 뺌
            pre.append(f"일회성 세금 {'비용' if c['tx'] > 0 else '이익'}(${abs(c['tx']):.2f})")
        if abs(c["dc"]) >= 0.005:
            pre.append(f"중단영업 {'손실' if c['dc'] > 0 else '이익'}(${abs(c['dc']):.2f})")
        b0 = (f"공시 희석 EPS {_usd(c['raw'])}에서 {'·'.join(pre)}을 덜어 낸 {_usd(c['before'])}" if pre else f"조정 전 {_usd(c['before'])}")
        s.append(f"PER은 최근 4분기 희석 EPS에서 일회성 손익을 뺀 값으로 계산했다({b0} → 조정 뒤 {_usd(c['after'])} — {lst}{more}).")
    if f["hist"]:
        h = f["hist"]
        span = _ql(h[0]) if len(h) == 1 else f"{_ql(h[0])}~{_ql(h[-1])}"
        s.append(f"자기 이력 PER의 지난 구간 중 {len(h)}개 결산일({span})도 같은 규칙으로 일회성을 뺐다." if c else
                 f"지금 PER의 최근 4분기에는 뺀 일회성 손익이 없고, 자기 이력 PER의 지난 구간 중 {len(h)}개 결산일({span})은 일회성 손익(손상·매각·소송·계약 해지·IPR&D·구조조정)을 뺀 EPS로 계산했다.")
    s.append(tail)
    if opin:
        s.append("영업이익 안에 있는 항목의 손익은 이익률에 그대로 남아 있다.")
    d = "현금흐름 세율도 같은 일회성 항목을 뺀 세전이익·세금으로 계산했다(이익률은 GAAP)." if (c and tax_on) else ""
    return " ".join(s), d


def apply(C, T, cik, MUL, bmh, bd):
    f = facts(T, cik, MUL.get("window") or ["0000-00-00", "9999-12-31"], bmh)
    if not f:
        return None
    tax_on = bool(bd.base_inputs(T).get("_eps_oneoff_tax"))
    st, dt = sentences(f, tax_on, MUL.get("perBasis") or "diluted")
    if st and getattr(C, "SELF_TIP", None) is not None and st not in C.SELF_TIP:
        C.SELF_TIP = (C.SELF_TIP.rstrip() + " " + st).strip()
    if dt and dt not in (getattr(C, "DCF_NOTE", "") or ""):
        C.DCF_NOTE = ((getattr(C, "DCF_NOTE", "") or "").rstrip() + " " + dt).strip()
    return f
