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
    """
    from datetime import date
    rows = (data.get("facts", {}).get("us-gaap", {}).get("EarningsPerShareDiluted", {}).get("units", {}).get("USD/shares", []))
    pdays = lambda e: (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days if "start" in e else -1
    ents = []
    for e in rows:
        e = dict(e)
        ratio = 1.0
        for s in splits:
            if e["filed"] < s["date"]:
                ratio *= s["ratio"]
        e["val"] = e["val"] / ratio
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
    quarters = list(qs)
    for f in fy:
        fe = date.fromisoformat(f["end"])
        mem = [q for q in qs if date.fromisoformat(q["end"]) <= fe and (fe - date.fromisoformat(q["start"])).days <= 380
               and (fe - date.fromisoformat(q["end"])).days <= 280]
        if len(mem) == 3 and not any(q["end"] == f["end"] for q in qs):
            quarters.append({"end": f["end"], "start": max(mem, key=lambda m: m["end"])["end"],
                             "val": f["val"] - sum(m["val"] for m in mem), "filed": max([f["filed"]] + [m["filed"] for m in mem])})
    quarters.sort(key=lambda e: e["end"])
    out = []
    for i in range(3, len(quarters)):
        w = quarters[i - 3:i + 1]
        out.append({"quarter_end": w[-1]["end"], "available": max(x["filed"] for x in w), "val": round(sum(x["val"] for x in w), 4)})
    return sorted(out, key=lambda e: e["available"])
