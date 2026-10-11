"""연구용 시점 재현 도구(C8, 2026-10-03 사용자 결정 — 연구 재현만 시점 기준, 카드는 그대로).

엔진은 분사 재작성 종목(fetch_eps_history.RESTATED_LATEST)에 "나중 공시 값 + 처음 공시일"을 쓴다(2026-09-30 사용자 결정 — 카드의
자기 이력이 분사 전후로 섞이지 않게). 과거 평가일에서는 그 평가일 뒤에 나온 재작성 값이 미리 보이므로, 연구 패널은 평가일마다
**그날까지 공시된 SEC 행만** 엔진에 넘긴다. 감가상각 합산 태그의 "멈춤" 판정 기준일도 평가일로 맞춘다(bmh.ASOF_REF).

    import pit
    pit.install(bmh, cik, data, asof)   # 이 평가일의 시점 자료로 엔진이 계산하게
    pit.reset(bmh)                      # 끝나면 되돌린다
"""
import functools


def filtered(data, asof):
    """companyfacts 축약본에서 filed ≤ asof인 행만 남긴다."""
    out = {"cik": data.get("cik"), "entityName": data.get("entityName"), "facts": {}}
    for ns, tags in (data.get("facts") or {}).items():
        out["facts"][ns] = {}
        for tag, v in tags.items():
            units = {u: [r for r in rows if r.get("filed", "9999") <= asof] for u, rows in v.get("units", {}).items()}
            units = {u: rows for u, rows in units.items() if rows}
            if units:
                out["facts"][ns][tag] = {**{k: x for k, x in v.items() if k != "units"}, "units": units}
    return out


_ORIG = {}


def capture(bmh):
    """엔진 원래의 자료 로더를 기억한다 — 연구 스크립트가 로더를 바꾸기 전에 한 번 부른다(Codex 2차)."""
    _ORIG["facts"] = bmh._facts


def install(bmh, cik, data, asof, ref=None):
    """asof까지 공시된 행만 엔진에 넘긴다. ref는 감가상각 합산 태그 멈춤 판정 기준일(기본 asof)."""
    fd = filtered(data, asof)
    bmh._facts = functools.lru_cache(maxsize=2)(lambda c, _d=fd: _d if c == cik else {})
    if hasattr(bmh.concept, "cache_clear"):
        bmh.concept.cache_clear()
    bmh.ASOF_REF = ref or asof


def reset(bmh):
    """기준일과 자료 로더를 되돌린다(Codex — 로더가 걸러진 채 남지 않게)."""
    bmh.ASOF_REF = None
    if "facts" in _ORIG:
        bmh._facts = _ORIG["facts"]


def eps_ttm(data, splits):
    """희석 EPS TTM을 SEC 자료로 다시 만든다 — 공개일은 **구성 네 분기 가운데 가장 늦은 첫 공시일**(C8, Codex 2차).

    통제 유니버스 EPS 파일(fetch_control_universe.fetch_eps)은 마지막 분기 공시일만 적어, 앞 분기가 나중에 처음 공시된 경우
    (TTM의 2.4%, 87종목, 중앙 187일) 미래 정보가 섞였다. 분기·연간 선택·4분기 유도·분할 보정은 그 함수와 같다.

    F3 (c)(input_fix_prereg, 2026-10-10): 절댓값이 1,000을 넘는 희석 EPS(HAL 2022-10~2024-11 공시분 ×1e6)는 버리고 같은 기간
    순이익(기간마다 보통주 귀속 희석 순이익, 없으면 NetIncomeLoss) ÷ 희석 가중평균으로 대신한다. 분할 보정은 가중평균 공시일 기준
    (그 숫자의 주식 단위), 공개일은 순이익·가중평균 중 늦은 공시일. 연간 EPS가 없는 회계연도는 그해 분기 중 대신한 것이 있을 때만
    (연간 순이익 − 세 분기 순이익) ÷ 연간 희석 가중평균으로 4분기를 만든다 — 미래 공시의 오류 여부에 기대지 않게(Codex).
    F3 (d): 네 분기는 종료일이 서로 다르고, 각 분기는 앞 분기 끝 **다음 날부터 8일 안**에 시작해야(겹침·건너뜀 금지) 하며,
    첫 시작~끝 종료가 400일 안이어야 TTM이 된다(WAT 2017 같은 분기 중복, 53주 해 4분기 누락 창).
    """
    from datetime import date, timedelta
    gaap = data.get("facts", {}).get("us-gaap", {})
    rows = (gaap.get("EarningsPerShareDiluted", {}).get("units", {}).get("USD/shares", []))
    pdays = lambda e: (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days if "start" in e else -1

    def first_by_period(tag, unit):
        b = {}
        for e in gaap.get(tag, {}).get("units", {}).get(unit, []):
            if "start" in e and e.get("filed"):
                k = (e["start"], e["end"])
                if k not in b or e["filed"] < b[k]["filed"]:
                    b[k] = e
        return b
    ni = {**first_by_period("NetIncomeLoss", "USD"), **first_by_period("NetIncomeLossAvailableToCommonStockholdersDiluted", "USD")}
    wa = first_by_period("WeightedAverageNumberOfDilutedSharesOutstanding", "shares")

    def split_div(val, filed):
        ratio = 1.0
        for s in splits:
            if filed < s["date"]:
                ratio *= s["ratio"]
        return val / ratio

    def from_ni(k):
        """(start, end) 기간의 순이익 ÷ 희석 가중평균 — 분할은 가중평균 공시일 기준, 공개일은 둘 중 늦은 날."""
        n_, w_ = ni.get(k), wa.get(k)
        if not (n_ and w_ and w_["val"]):
            return None
        return {"start": k[0], "end": k[1], "val": n_["val"] / split_div(w_["val"], w_["filed"]) * 1.0,
                "filed": max(n_["filed"], w_["filed"]), "replaced": True}

    def wa_adj(w_):
        return split_div(w_["val"], w_["filed"])
    ents = []
    for e in rows:
        e = dict(e)
        if abs(e["val"]) > 1000:
            r = from_ni((e.get("start"), e["end"]))
            if r is None:
                continue                                   # 대신할 수 없으면 버린다
            r["form"] = e.get("form")
            r["val"] = ni[(r["start"], r["end"])]["val"] / wa_adj(wa[(r["start"], r["end"])])
            ents.append(r)
            continue
        e["val"] = split_div(e["val"], e["filed"])
        ents.append(e)

    def first(sel):
        b = {}
        for e in sel:
            k = (e["start"], e["end"])
            if k not in b or e["filed"] < b[k]["filed"]:
                b[k] = e
        return sorted(b.values(), key=lambda e: e["end"])
    qs = first([e for e in ents if e.get("form") == "10-Q" and 80 <= pdays(e) <= 100])
    fy = first([e for e in ents if e.get("form") == "10-K" and pdays(e) > 350])
    have = {f["end"] for f in fy}
    for (st, en), n_ in ni.items():
        # 연간 EPS가 없는 해: 그해 안의 분기 중 대신한 것이 있을 때만 순이익으로 연간을 만든다
        if en in have or pdays(n_) <= 350 or (st, en) not in wa:
            continue
        if not any(q.get("replaced") and q["start"] >= st and q["end"] <= en for q in qs):
            continue
        w_ = wa[(st, en)]
        if w_["val"]:
            fy.append({"start": st, "end": en, "val": n_["val"] / wa_adj(w_), "filed": max(n_["filed"], w_["filed"]),
                       "replaced": True, "_ni": n_, "_wa": w_})
    fy.sort(key=lambda e: e["end"])
    quarters = list(qs)
    for f in fy:
        fe = date.fromisoformat(f["end"])
        mem = [q for q in qs if date.fromisoformat(q["end"]) <= fe and (fe - date.fromisoformat(q["start"])).days <= 380
               and (fe - date.fromisoformat(q["end"])).days <= 280]
        if len(mem) == 3 and not any(q["end"] == f["end"] for q in qs):
            last = max(mem, key=lambda m: m["end"])["end"]
            if "_ni" in f:
                qn = [ni.get((m["start"], m["end"])) for m in mem]
                if not all(qn):
                    continue
                v = (f["_ni"]["val"] - sum(x["val"] for x in qn)) / wa_adj(f["_wa"])
                filed = max([f["filed"]] + [x["filed"] for x in qn] + [m["filed"] for m in mem])
            else:
                v, filed = f["val"] - sum(m["val"] for m in mem), max([f["filed"]] + [m["filed"] for m in mem])
            quarters.append({"end": f["end"], "start": (date.fromisoformat(last) + timedelta(days=1)).isoformat(), "val": v,
                             "filed": filed, "replaced": bool(f.get("replaced") or any(m.get("replaced") for m in mem))})
    quarters.sort(key=lambda e: e["end"])

    def contiguous(w):
        if len({x["end"] for x in w}) < 4:
            return False
        for prev, cur in zip(w, w[1:]):
            gap = (date.fromisoformat(cur["start"]) - date.fromisoformat(prev["end"])).days
            if not 1 <= gap <= 8:                          # 앞 분기 끝 다음 날부터 8일 안(겹침·건너뜀 금지)
                return False
        return (date.fromisoformat(w[-1]["end"]) - date.fromisoformat(w[0]["start"])).days <= 400
    out = []
    for i in range(3, len(quarters)):
        w = quarters[i - 3:i + 1]
        if not contiguous(w):
            continue
        out.append({"quarter_end": w[-1]["end"], "available": max(x["filed"] for x in w), "val": round(sum(x["val"] for x in w), 4),
                    **({"replaced": True} if any(x.get("replaced") for x in w) else {})})
    return sorted(out, key=lambda e: e["available"])
