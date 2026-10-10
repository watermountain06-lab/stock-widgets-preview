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
    순이익(보통주 귀속, 없으면 NetIncomeLoss) ÷ 희석 가중평균으로 대신한다. 그런 회사가 연간 EPS를 내지 않으면(HAL) 4분기는
    (연간 순이익 − 세 분기 순이익) ÷ 연간 희석 가중평균. 대신한 값의 공개일은 구성요소 중 가장 늦은 공시일.
    F3 (d): 네 분기는 종료일이 서로 다르고 겹치지 않으며 이어져야(시작이 앞 분기 끝에서 8일 안) 하고, 첫 시작~끝 종료가 400일 안이어야
    TTM이 된다 — 같은 분기가 시작일만 달리 두 번 들어가거나(WAT 2017) 빠진 분기를 건너뛰어 더하지 않게.
    """
    from datetime import date
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
    bad = any(abs(e["val"]) > 1000 for e in rows)
    ni = wa = {}
    if bad:
        ni = first_by_period("NetIncomeLossAvailableToCommonStockholdersDiluted", "USD") or first_by_period("NetIncomeLoss", "USD")
        wa = first_by_period("WeightedAverageNumberOfDilutedSharesOutstanding", "shares")

    def split_div(val, filed):
        ratio = 1.0
        for s in splits:
            if filed < s["date"]:
                ratio *= s["ratio"]
        return val / ratio
    ents = []
    for e in rows:
        e = dict(e)
        if abs(e["val"]) > 1000:
            k = (e.get("start"), e["end"])
            n_, w_ = ni.get(k), wa.get(k)
            if not (n_ and w_ and w_["val"]):
                continue                                   # 대신할 수 없으면 버린다
            e["val"], e["filed"], e["replaced"] = n_["val"] / w_["val"], max(e["filed"], n_["filed"], w_["filed"]), True
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
    if bad:
        # 연간 EPS 행이 없는 회계연도는 순이익·가중평균으로 연간 값을 만든다(4분기 유도용)
        have = {f["end"] for f in fy}
        for (st, en), n_ in ni.items():
            w_ = wa.get((st, en))
            if en not in have and w_ and w_["val"] and pdays(n_) > 350:
                fy.append({"start": st, "end": en, "val": split_div(n_["val"] / w_["val"], max(n_["filed"], w_["filed"])),
                           "filed": max(n_["filed"], w_["filed"]), "replaced": True, "_ni": n_, "_wa": w_})
        fy.sort(key=lambda e: e["end"])
    quarters = list(qs)
    for f in fy:
        fe = date.fromisoformat(f["end"])
        mem = [q for q in qs if date.fromisoformat(q["end"]) <= fe and (fe - date.fromisoformat(q["start"])).days <= 380
               and (fe - date.fromisoformat(q["end"])).days <= 280]
        if len(mem) == 3 and not any(q["end"] == f["end"] for q in qs):
            if "_ni" in f:
                # 순이익으로 만든 연간: 4분기 = (연간 순이익 − 세 분기 순이익) ÷ 연간 희석 가중평균
                qn = [ni.get((m["start"], m["end"])) for m in mem]
                if not all(qn):
                    continue
                v = split_div((f["_ni"]["val"] - sum(x["val"] for x in qn)) / f["_wa"]["val"], f["filed"])
                filed = max([f["filed"]] + [x["filed"] for x in qn] + [m["filed"] for m in mem])
            else:
                v, filed = f["val"] - sum(m["val"] for m in mem), max([f["filed"]] + [m["filed"] for m in mem])
            quarters.append({"end": f["end"], "start": max(mem, key=lambda m: m["end"])["end"], "val": v, "filed": filed})
    quarters.sort(key=lambda e: e["end"])

    def contiguous(w):
        ends = [x["end"] for x in w]
        if len(set(ends)) < 4:
            return False
        for prev, cur in zip(w, w[1:]):
            if abs((date.fromisoformat(cur["start"]) - date.fromisoformat(prev["end"])).days) > 8:
                return False
        return (date.fromisoformat(w[-1]["end"]) - date.fromisoformat(w[0]["start"])).days <= 400
    out = []
    for i in range(3, len(quarters)):
        w = quarters[i - 3:i + 1]
        if not contiguous(w):
            continue
        out.append({"quarter_end": w[-1]["end"], "available": max(x["filed"] for x in w), "val": round(sum(x["val"] for x in w), 4)})
    return sorted(out, key=lambda e: e["available"])
