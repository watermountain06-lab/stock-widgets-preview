#!/usr/bin/env python3
"""자동 카드(cfg AUTO = True) — 분기마다 사람이 고치던 칸을 SEC 자료와 규칙 문장으로 채운다(설계 D, 2026-10-10).

Claude 없이 GitHub Actions에서 돈다. fill.py가 두 번 부른다:
  apply(C, T)        카드 계산 전 — 분기 변수, 부문 표, 핵심 수치 칸(GAAP 희석 EPS), 자본배분, 다음 실적일, 보도자료 링크
  texts(C, ns)       계산 뒤 — 종합 해석·강세/약세·체크포인트·각주·설명 문장(ns = fill.py의 변수들)
문장 규칙(Fable 2026-10-10): 사실과 숫자만 쓰고 원인은 쓰지 않는다("유기적·가격·수요" 같은 말 금지).
1년 전이 0 이하이거나 증감이 ±50%를 넘으면 증감률 대신 수준을 적는다. 길이가 다른 분기(16주·12주)는 증감을 견주지 않는다.
회사가 따로 내는 숫자(가이던스·조정 EPS·유기적 성장·회사 계획)는 SEC 자료에 없어 자동 카드에 넣지 않는다.
어느 단계든 자료가 맞지 않으면 예외로 멈춘다 — 카드는 이전 분기에 남는다(daily_price.attempt가 되돌린다).
"""
import datetime as dt
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
sys.path.insert(0, HERE)
import quarter_auto as qa  # noqa: E402
import seg_xbrl as sx  # noqa: E402
import news_auto as na  # noqa: E402

bmh = qa.bmh
UA = "kim research gptjhss@gmail.com"
d = qa.d


def B(v):
    """백만 달러가 아닌 달러 값 → '$12.3B'."""
    s = f"${abs(v) / 1e9:.1f}B" if abs(v) >= 1e9 else f"${abs(v) / 1e6:,.0f}M"
    return ("−" if v < 0 else "") + s


def chg(a, b_, unit="%"):
    """증감 문장 조각. 1년 전 0 이하·부호 바뀜·±50% 넘음은 증감률 대신 말로(가드)."""
    if a is None or b_ is None:
        return None
    if b_ <= 0:
        return "흑자 전환" if a > 0 else "적자 지속"
    if a <= 0:
        return "적자 전환"
    r = a / b_ - 1
    if abs(r) > 0.5:
        return None
    return f"{r * 100:+.1f}%".replace("-", "−")


def usd(v):
    """주당 금액 — 센트 아래 자리가 있으면 그대로($1.4225), 없으면 두 자리($1.48)."""
    t = f"{abs(v):.4f}".rstrip("0")
    t = t if len(t.split(".")[1]) >= 2 else f"{abs(v):.2f}"
    return ("−$" if v < 0 else "$") + t


def money(v):
    """주당 금액 두 자리 — 음수는 '−$0.92'(Fable: '$-0.92' 금지)."""
    return ("−$" if v < 0 else "$") + f"{abs(v):.2f}"


def kdate(s):
    x = d(s)
    return f"{x.year}년 {x.month}월 {x.day}일"


SUBS = os.path.join(V2, ".sec_cache", "submissions")


def _submissions(cik):
    """SEC 제출 목록 — 하루 한 번 받고, 받기에 실패하면 마지막으로 받은 것을 쓴다(가격 갱신이 SEC 접속에 묶이지 않게, Codex)."""
    os.makedirs(SUBS, exist_ok=True)
    p = os.path.join(SUBS, f"{str(cik).zfill(10)}.json")
    fresh = os.path.exists(p) and dt.date.fromtimestamp(os.path.getmtime(p)) == dt.date.today()
    if not fresh:
        try:
            req = urllib.request.Request(f"https://data.sec.gov/submissions/CIK{str(cik).zfill(10)}.json", headers={"User-Agent": UA})
            r = json.loads(urllib.request.urlopen(req, timeout=30).read())["filings"]["recent"]
            json.dump(r, open(p, "w"))
            return r
        except Exception:
            if not os.path.exists(p):
                raise
    return json.load(open(p))


def _flow_rows(cik, tag, unit="USD"):
    return bmh._facts(cik).get("facts", {}).get("us-gaap", {}).get(tag, {}).get("units", {}).get(unit, [])


def ytd(cik, tags, end, fy_start):
    """회계연도 초부터 end까지 누계(현금흐름표). 없으면 None — 0으로 바꾸지 않는다(Codex)."""
    for tag in tags:
        rows = [r for r in _flow_rows(cik, tag) if r.get("end") == end and r.get("start")
                and abs((d(r["start"]) - fy_start).days) <= 10 and (d(end) - d(r["start"])).days <= 380]
        if rows:   # 같은 기간이 정정되면 가장 나중 공시 값(Codex) — 기간도 그 행의 시작일로
            r = sorted(rows, key=lambda r: r["filed"])[-1]
            return r["val"], d(end) - d(r["start"])
    return None, None


DPS_TAGS = (("CommonStockDividendsPerShareDeclared", "선언 기준"), ("CommonStockDividendsPerShareCashPaid", "지급 기준"))   # KO는 2018년부터 지급 기준만


def dps_quarter(cik, end, prev_end, fy_start, is_q4, tag=None):
    """그 분기의 주당 배당(선언 기준, 없으면 지급 기준). 10-K 4분기는 연간 − 9개월 누계(주당 배당은 합이라 뺄셈이 맞다).
    tag를 주지 않으면 값이 있는 첫 태그를 쓰고 (값, 태그)를 돌려준다."""
    if tag is None:
        for tg, _ in DPS_TAGS:
            v = dps_quarter(cik, end, prev_end, fy_start, is_q4, tg)
            if v is not None:
                return v, tg
        return None, None
    rows = _flow_rows(cik, tag, "USD/shares")
    q = [r for r in rows if r.get("end") == end and r.get("start") and 70 <= (d(end) - d(r["start"])).days <= 125]
    if q:
        return sorted(q, key=lambda r: r["filed"])[-1]["val"]
    if is_q4:
        fy = [r for r in rows if r.get("end") == end and r.get("start") and 350 <= (d(end) - d(r["start"])).days <= 380]
        n9 = [r for r in rows if r.get("end") == prev_end and r.get("start") and abs((d(r["start"]) - fy_start).days) <= 10]
        if fy and n9:
            return round(fy[0]["val"] - n9[0]["val"], 4)
    return None


def dps_series(cik, tag):
    """분기별 주당 배당 {분기 말: 값}. 분기 행, 없으면 **같은 공시 안의** 같은 시작일 누계끼리의 차 — 공시마다 분할 기준이 같다
    (BKNG: 상반기 누계는 분할 뒤 고친 $0.38, 9개월 누계는 고치기 전 $9.60이라 공시를 섞어 빼면 $9.22가 나왔다, Codex).
    같은 분기 값이 여러 공시에 있으면 나중 공시."""
    by_accn = {}
    for r in _flow_rows(cik, tag, "USD/shares"):
        if r.get("start"):
            by_accn.setdefault(r.get("accn"), []).append(r)
    out = {}   # 분기 말 -> (접수일, 값)
    def put(e_, filed, v):
        if e_ not in out or filed > out[e_][0]:
            out[e_] = (filed, v)
    for accn, rows in by_accn.items():
        for r in rows:
            if 70 <= (d(r["end"]) - d(r["start"])).days <= 125:
                put(r["end"], r["filed"], r["val"])
        ladders = {}
        for r in rows:
            ladders.setdefault(r["start"], []).append(r)
        for st, xs in ladders.items():
            xs.sort(key=lambda r: r["end"])
            for a_, b_ in zip(xs, xs[1:]):
                if 80 <= (d(b_["end"]) - d(a_["end"])).days <= 100:
                    if b_["end"] not in out or out[b_["end"]][0] < b_["filed"]:
                        put(b_["end"], b_["filed"], round(b_["val"] - a_["val"], 6))
    # 10-K 4분기: 연간(10-K)과 9개월 누계(3분기 10-Q)는 다른 공시다 — 공시를 넘는 차는 직전 분기 배당의 2배 이하일 때만 받는다
    # (분할 기준이 섞이면 BKNG처럼 크게 튄다, MU 4분기는 받는다)
    latest = {}
    for rows in by_accn.values():
        for r in rows:
            k = (r["start"], r["end"])
            if k not in latest or r["filed"] > latest[k]["filed"]:
                latest[k] = r
    ladders = {}
    for r in latest.values():
        ladders.setdefault(r["start"], []).append(r)
    for st, xs in ladders.items():
        xs.sort(key=lambda r: r["end"])
        for a_, b_ in zip(xs, xs[1:]):
            e_ = b_["end"]
            if e_ in out or not 80 <= (d(e_) - d(a_["end"])).days <= 100:
                continue
            v = round(b_["val"] - a_["val"], 6)
            prev = [out[k][1] for k in sorted(out) if k < e_ and out[k][1] > 0]
            if v > 0 and prev and v <= 2 * prev[-1]:
                put(e_, b_["filed"], v)
    return {k: v for k, (f_, v) in out.items()}


def latest_dps(cik, cur):
    """최근에 선언(없으면 지급)한 분기 배당과 1년 전 같은 값 — 분기에 선언이 없으면(BKNG는 1분기에 선언) 그 앞 분기.
    두 태그 가운데 더 최근 분기를 가진 쪽(선언 보고를 멈추고 지급으로 바꾼 회사, Codex)."""
    best = None
    for tag, label in DPS_TAGS:
        sr = dps_series(cik, tag)
        ks = sorted(k for k, v in sr.items() if k <= cur and v > 0 and (d(cur) - d(k)).days <= 200)
        if ks and (best is None or ks[-1] > best[3]):
            e = ks[-1]
            yo = [k for k, v in sr.items() if v > 0 and 350 <= (d(e) - d(k)).days <= 380]
            best = (sr[e], (sr[yo[-1]] if yo else None), label, e)
    return best or (None, None, None, None)


def adj_note(C):
    """부문 합과 매출의 차이 설명(TMO 부문 간 거래, CVX 지분법·기타 수익) — fill.py가 매출 기준을 다시 맞춘 뒤에도 부른다(Codex)."""
    seg_sum = sum(v for _, v, _ in C.SEG)
    if abs(C.SEG_ADJ) < 0.01 * max(seg_sum, 1):
        return ""
    return (f"부문 합 ${seg_sum / 1000:.2f}B에 부문 간 거래·조정 {'−' if C.SEG_ADJ < 0 else '+'}${abs(C.SEG_ADJ) / 1000:.2f}B를 더한 것이 매출이다"
            "(비율은 부문 합 기준) · ")


def apply(C, T):
    cik = str(C.CIK).zfill(10)
    r = qa.resolve(T)   # 기준표 날짜까지 접수된 자료로
    for k in ("CUR", "YO", "QO", "QLABEL", "YL", "QQL", "L8", "TENQ", "TENQ_NAME", "FY_ENDS", "FY_LABEL"):
        if r.get(k) is None:
            raise SystemExit(f"{T}: 자동 분기 변수 {k}를 정하지 못했다")
        setattr(C, k, r[k])
    ends, fy_ends = qa.quarters(T, cik)
    is_q4 = C.TENQ_NAME.endswith("10-K")
    fy_start = d(C.FY_ENDS[1] if is_q4 else C.FY_ENDS[0])
    qlen = {e: (d(e) - d(p)).days for p, e in zip(ends, ends[1:])}
    C._AUTO = {"qlen": qlen, "is_q4": is_q4, "fy_start": fy_start, "ends": ends}

    # 보고서 원문과 SEC 요약 자료의 분기 매출 대조 — 같은 값으로 자기 자신을 대조하지 않게(Codex)
    form = "10-K" if is_q4 else "10-Q"
    q3 = qa.filing(cik, C.QO, None)[1] if is_q4 else None
    M = getattr(C, "SEG_MAP", None)
    if not M:
        raise SystemExit(f"{T}: SEG_MAP이 없다 — 부문 지도를 먼저 만들 것")
    # 여러 축을 섞은 손 표(GOOGL 제품별 + Cloud 사업부)는 parts로 — 묶음마다 값을 꺼내 한 표로(2026-10-11)
    parts = M.get("parts") or [M]
    def vals_at(end, kform, q3u, q3e):
        out = {}
        for i_, P_ in enumerate(parts):   # 묶음마다 같은 멤버 이름이 나온다(AMGN 미국·해외 모두 ProductSales) — 묶음 번호로 구분
            v_ = sx.quarter_values(P_, kform, C.TENQ, end, q3_url=q3u, q3_end=q3e)
            if P_.get("all_as"):   # 이 묶음의 멤버는 모두 한 줄로(ABBV 치료 분야 — 신제품도 그 분야로)
                P_ = {**P_, "members": {k_: tuple(P_["all_as"]) for k_ in v_}}
            unknown = set(v_) - set(P_["members"]) - set(P_.get("ignore", [])) - set(P_.get("adjust", []))
            if unknown and P_.get("strict"):   # 묶음 전체를 쓰는 지도만 — 여러 축 지도는 원래 묶음에서 일부만 고른다(WMT·CAT) — 새 멤버면 멈춘다(Codex)
                raise ValueError(f"지도에 없는 부문 {sorted(unknown)} — SEG_MAP에 더할 것")
            parts[i_] = P_
            for k_ in P_["members"]:
                if k_ not in v_:
                    raise ValueError(f"부문 {k_}의 값이 없다(부문 재편?)")
                out[f"{i_}|{k_}" if len(parts) > 1 else k_] = v_[k_]
            for k_ in P_.get("adjust", []):
                if k_ in v_:
                    out[k_] = v_[k_]
        return out
    parts = [dict(P_) for P_ in parts]
    cur_v = vals_at(C.CUR, form, q3, C.QO)
    Mall = {"members": {(f"{i_}|{k_}" if len(parts) > 1 else k_): v_ for i_, P_ in enumerate(parts) for k_, v_ in P_["members"].items()},
            "ignore": [], "adjust": M.get("adjust", []), "other": M.get("other")}
    if is_q4:
        yo_q3 = ends[ends.index(C.YO) - 1]
        yo_v = vals_at(C.YO, "10-K", q3, yo_q3)
    else:
        yo_v = vals_at(C.YO, "10-Q", None, None)
    M = Mall
    ref_adj = abs(getattr(C, "SEG_ADJ", 0) or 0)   # 사람이 확인해 둔 본사·상계 조정의 크기(cfg 원래 값) — 허용 범위의 기준
    C._SEG_ADJ_HAND = getattr(C, "SEG_ADJ", 0) or 0
    C.SEG, C.SEG_ADJ = sx.table(M, cur_v)
    # 부문 합과 매출의 차이(본사·상계 등)는 남은 값으로 넣되, 매출의 3%를 넘으면 지도가 틀린 것으로 보고 멈춘다(2026-10-10)
    _, _rows = bmh.pick_tag(cik, bmh.FLOW_TAGS["revenue"])
    _rev = {e["end"]: e["val"] for e in bmh.quarterly_flow(_rows, T)}
    if C.CUR in _rev:
        resid = _rev[C.CUR] / 1e6 - sum(v for _, v, _ in C.SEG) - C.SEG_ADJ
        ref_signed = getattr(C, "_SEG_ADJ_REF", None)
        ref_signed = ref_adj if ref_signed is None else ref_signed
        # 차이는 매출의 3% 안이거나, 사람이 확인한 조정값(cfg SEG_ADJ, GLW 환헤지 −233·TMO 부문 간 거래 −566)과 같은 부호로 그 0.5~1.5배일 때만 —
        # 큰 조정값이 있다고 아무 차이나 받아들이지 않게(Codex 2026-10-10)
        orig = getattr(C, "_SEG_ADJ_HAND", 0)
        near_ref = orig and resid * orig > 0 and 0.5 * abs(orig) <= abs(resid) <= 1.5 * abs(orig)
        rem = getattr(C, "SEG_MAP", {}).get("remainder")
        if not rem and abs(resid) > 0.03 * _rev[C.CUR] / 1e6 and not near_ref:   # 나머지 줄이 있으면 그 검사(비중)를 아래에서
            raise SystemExit(f"{T}: 부문 합이 매출과 {resid:,.0f}백만 달러 다르다 — SEG_MAP 확인")
        if rem:   # 손 표의 "기타" 줄 = 매출 − 나머지 부문(AMAT·HD·META 등) — 비중이 손 표 때의 절반~2배를 벗어나면 멈춘다
            share = resid / (_rev[C.CUR] / 1e6)
            if resid < 0 or not (0.5 * rem[2] <= share <= 2 * rem[2] or abs(resid) < 0.005 * _rev[C.CUR] / 1e6):
                raise SystemExit(f"{T}: 나머지 줄 '{rem[0]}' 비중 {share:.1%}가 손 표 때({rem[2]:.1%})와 너무 다르다 — SEG_MAP 확인")
            C.SEG = sorted(C.SEG + [(rem[0], round(resid), rem[1])], key=lambda r_: -r_[1])
            C._AUTO["rem_name"] = rem[0]
        else:
            C.SEG_ADJ = round(C.SEG_ADJ + resid)
    _yt = sx.table(Mall_yo := {**M, "members": {k_: v_ for k_, v_ in M["members"].items() if k_ in yo_v}}, yo_v) if yo_v else ([], 0)
    yo_tab = {n: v for n, v, _ in _yt[0]}
    _rem = getattr(C, "SEG_MAP", {}).get("remainder")
    if _rem and C.YO in _rev:   # 1년 전 나머지 줄도 조정액을 빼고(Codex), 음수면 비교하지 않는다
        _ry = round(_rev[C.YO] / 1e6 - sum(yo_tab.values()) - _yt[1])
        if _ry >= 0:
            yo_tab[_rem[0]] = _ry
    C._AUTO["seg_yo"] = yo_tab
    C.RELEASE = {}   # 보도자료 숫자는 쓰지 않는다 — 부문 합 = 매출 대조(fill.py)가 원문과 요약 자료를 잇는다
    C.OPM_RANGE = (-1000, 1000)

    # 핵심 수치 칸: GAAP 희석 EPS(EPS 이력 파일 — 4분기는 연간에서 1~3분기를 뺀 값)
    eps = {e["quarter_end"]: e["quarter_eps"] for e in json.load(open(os.path.join(REPO, "scripts", f"{T}_eps_history.json")))}
    e_cur, e_yo = eps.get(C.CUR), eps.get(C.YO)
    if e_cur is None:
        raise SystemExit(f"{T}: {C.CUR} EPS가 이력 파일에 없다")
    c = chg(e_cur, e_yo) if e_yo is not None else None
    if c is None and e_yo and e_yo > 0 and e_cur > 0:   # EPS 칸은 ±50%를 넘어도 증감을 적는다(Fable — CRM·TXN만 빠졌다)
        c = f"{(e_cur / e_yo - 1) * 100:+.0f}%".replace("-", "−")
    core_note = " · 차트 순이익은 본업 기준(영업이익 + 순이자, 세후)" if T in json.load(open(os.path.join(V2, "core_earnings.json"))) else ""
    C.STAT3 = (f"희석 EPS ({C.QLABEL})", money(e_cur),
               "GAAP · " + (f"1년 전 {money(e_yo)} ({c})" if c else f"1년 전 {money(e_yo)}" if e_yo is not None else "1년 전 값 없음") + core_note)

    # 자본배분: 자사주 매입·배당 지급(올해 누계), 분기 주당 배당(선언 기준)
    def span(td):   # 회계연도가 1월에 시작하지 않으면 "연초"가 아니라 회계연도 누계로(Fable — AAPL 9/28 시작)
        st = d(C.CUR) - td
        if st.month == 1 and st.day <= 7:
            return f"연초~{d(C.CUR).month}/{d(C.CUR).day}, {round(td.days / 7)}주"
        return f"회계연도 누계 {st.year}.{st.month}.{st.day}~{d(C.CUR).year}.{d(C.CUR).month}.{d(C.CUR).day}, {round(td.days / 7)}주"   # 해를 밝힌다(MU 53주, Fable)
    bb, bbd = ytd(cik, ["PaymentsForRepurchaseOfCommonStock"], C.CUR, fy_start)
    dps, dps_yo, dlabel, dps_end = latest_dps(cik, C.CUR)
    dv, dvd = ytd(cik, ["PaymentsOfDividendsCommonStock"], C.CUR, fy_start)
    dv_pref = False
    if dv is None:   # 보통주 태그가 없으면 전체 배당 — 보통주 주당 배당이 없는 회사(BA)는 우선주 배당이라 따로 표시(Fable)
        dv, dvd = ytd(cik, ["PaymentsOfDividends"], C.CUR, fy_start)
        dv_pref = dv is not None and dps is None   # 최근 1년 안의 보통주 주당 배당이 없으면 우선주 배당(BA는 과거 보통주 이력이 있다, Codex)
    C._AUTO["dv_weeks"] = round(dvd.days / 7) if dvd else None
    yo_q3 = ends[ends.index(C.YO) - 1]
    C.CAPITAL = [(f"자사주 매입 ({span(bbd)})" if bb is not None else "자사주 매입", (B(bb) if bb else "없음") if bb is not None else "공시 없음"),
                 ((f"우선주 배당 ({span(dvd)})" if dv_pref else f"배당 지급 ({span(dvd)})") if dv is not None else "보통주 배당 지급",
                  B(dv) if dv is not None else ("공시 없음" if dps is not None else "없음")),   # 주당 배당이 있는데 지급액이 없으면 결측(GOOGL, Fable)
                 ((f"최근 분기 주당 배당 ({dlabel}, {d(dps_end).month}/{d(dps_end).day} 분기)",
                   ("1년 전 " + usd(dps_yo) + (f" · {chg(dps, dps_yo)}" if chg(dps, dps_yo) else "")) if dps_yo else "1년 전 배당 없음",
                   usd(dps)) if dps is not None else ("분기 주당 배당", "보통주 배당 없음", "—"))]
    C._AUTO.update({"bb": bb, "dv": dv if not dv_pref else None, "dps": dps, "dps_yo": dps_yo})
    gw = {r["end"]: r["val"] for r in sorted(_flow_rows(cik, "Goodwill"), key=lambda r: r["filed"])}
    C._AUTO["acq"] = bool(gw.get(C.CUR) and C.YO in gw and gw[C.CUR] > (gw[C.YO] or 0) * 1.15)   # 1년 전 영업권 0에서 생긴 인수도(Codex)   # 영업권이 1년에 15% 넘게 늘면 인수가 매출 성장에 섞였다(ABT, Fable)

    # 실적 보도자료 링크와 다음 실적일(작년 같은 분기의 실적 8-K + 364일, "예상")
    sub = _submissions(cik)
    rel = [(sub["filingDate"][i], sub["accessionNumber"][i], sub["primaryDocument"][i]) for i, f in enumerate(sub["form"])
           if f == "8-K" and "2.02" in sub["items"][i].split(",")]
    def is_results(x):   # 2.02항이라도 실적 보도자료만(ABBV는 분기 초에 IPR&D 선공시 8-K를 낸다, Fable)
        p_ = os.path.join(SUBS, f"exhibit_{x[1]}.json")
        if os.path.exists(p_) and "head" in json.load(open(p_)):   # 첫머리를 저장해 두고 판정은 매번(기준이 바뀌어도 다시 받지 않게)
            return bool(na.RESULTS.search(json.load(open(p_))["head"][:400]))
        try:
            url_, head_ = na.exhibit(cik, x[1], x[2])
        except Exception:
            return True   # 확인 못 하면 예전처럼(첫 2.02)
        json.dump({"url": url_, "head": head_[:400]}, open(p_, "w"))
        return bool(na.RESULTS.search(head_[:400]))
    def first_release(after, within=80):
        c_ = sorted(x for x in rel if 0 < (d(x[0]) - d(after)).days <= within)
        return next((x for x in c_ if is_results(x)), None)
    cur_rel = first_release(C.CUR)
    if cur_rel:
        _ex = os.path.join(SUBS, f"exhibit_{cur_rel[1]}.json")   # 보도자료 주소는 접수번호마다 한 번만 찾는다
        if os.path.exists(_ex):
            url = json.load(open(_ex))["url"]
        else:
            url, head = na.exhibit(cik, cur_rel[1], cur_rel[2])
            json.dump({"url": url}, open(_ex, "w"))
        C.PR, C.PR_CUR = {**C.PR, "auto": url}, "auto"   # 기존 뉴스의 보도자료 키(q1~q4)는 그대로 둔다(Codex)
    else:
        C.PR, C.PR_CUR = {**C.PR, "auto": C.TENQ}, "auto"
    i_yo = ends.index(C.YO)
    nxt_ago = ends[i_yo + 1] if i_yo + 1 < len(ends) else None
    ago_rel = first_release(nxt_ago) if nxt_ago else None
    nxt_end = d(nxt_ago) + dt.timedelta(days=364) if nxt_ago else d(C.CUR) + dt.timedelta(days=91)
    fye, n = qa.fiscal(nxt_end.isoformat(), fy_ends)
    nl = qa.label("fy" if "FY" in C.QLABEL else "cal", fye, n, qa.name_offset(C, fy_ends))
    if ago_rel:
        est = d(ago_rel[0]) + dt.timedelta(days=364)
        ago = d(ago_rel[0])
        C.NEXT = (f"{est.month}월 {est.day}일 무렵 예상", f"일정 · {nl} (작년 {ago.month}/{ago.day} 공시, 같은 요일로 추정)")
        C.NEXT_OP = (f"{est.month}월 {est.day}일 무렵", f"{nl} 예상")
        C.CHECK_WHEN = f"{est.year}년 {est.month}월 {est.day}일 무렵 (예상) · {nl}"
    else:
        C.NEXT = ("미정", f"일정 · {nl}")
        C.NEXT_OP = ("미정", f"{nl}")
        C.CHECK_WHEN = f"{nl}"
    C._AUTO["next_label"] = nl
    C.FUND_ASOF_NOTE = f"{C.TENQ_NAME}"
    lens = sorted({round(qlen[e] / 7) for e in ends[-8:] if e in qlen and 70 <= qlen[e] <= 130})   # 차트에 보이는 8분기 안에서만(Fable)
    C.FCF_SUB = "영업현금흐름 − 설비투자" + (f" · 분기 길이가 {'·'.join(map(str, lens))}주로 다르다" if len(lens) > 1 else "")
    C.CAPEX_SUB = "설비투자(현금흐름표)"


def texts(C, ns):
    """종합 해석·강세/약세·체크포인트·각주·설명 — fill.py가 계산한 값으로 규칙에 따라 쓴다."""
    A = C._AUTO
    rev, op, ni, fcf, capx = ns["rev"], ns["op"], ns["ni_gaap"], ns["fcf"], ns["cap"]
    cur, yo = ns["cur"], ns["yo"]
    SM, H, DCF, b = ns["SM"], ns["HIST"], ns["DCF"], ns["b"]
    px, selfsc, peersc = ns["px"], ns["selfsc"], ns["peersc"]
    QL = C.QLABEL
    same_len = abs(A["qlen"].get(cur, 91) - A["qlen"].get(yo, 91)) <= 5   # 흐름(yoy_at)과 같은 기준 — MU 14주 대 13주(7일)는 다르다(Fable)
    opm, opm_yo = op[cur] / rev[cur] * 100, op[yo] / rev[yo] * 100
    m5, m2, mn = H.get("margin_5y", 0) * 100, H.get("margin_2y", 0) * 100, H.get("margin_now", 0) * 100
    g3 = H["growth_3y"] * 100 if H.get("growth_3y") is not None else None   # 없으면 0으로 찍지 않는다(CB, Fable)
    _r = op[cur] / op[yo] - 1 if op[yo] > 0 else None
    odd_yo = op[yo] <= 0 or (_r is not None and abs(_r) > 0.5 and opm_yo < m5)   # 1년 전 분기 이익률이 낮아 이익 증감률이 크게 나온다 — 증감률 대신 수준
    r_rev = chg(rev[cur], rev[yo]) if same_len else None
    r_op = None if (odd_yo or not same_len) else chg(op[cur], op[yo])   # 길이가 다른 분기는 이익도 견주지 않는다(Codex)
    debt, cash = (b.get("debt") or 0), (b.get("cash") or 0) + (b.get("sti") or 0)
    lease = (b.get("lease") or 0) or 0   # 카드 Net Cash 줄과 같은 정의(차입금 + 리스, Fable)
    ttm_k = sorted(k for k in rev if k <= cur)[-4:]
    op_ttm = sum(op[k] for k in ttm_k)
    fcf_ok = len(ttm_k) == 4 and all(k in fcf for k in ttm_k)   # 네 분기가 다 있어야 합을 쓴다 — 빠진 분기를 0으로 치지 않는다(Codex)
    fcf_ttm = sum(fcf[k] for k in ttm_k) if fcf_ok else None
    rev_ttm = sum(rev[k] for k in ttm_k)
    per = SM.get("PER") or {}
    neg_dcf = DCF.get("base") is not None and DCF["base"] <= 0
    ratio = (DCF["base"] / px * 100) if DCF.get("base") and not neg_dcf else None   # 음수 내재가치는 비율로 쓰지 않는다(BA, Fable)
    pct_txt = lambda r: f"{r:.1f}%" if r < 10 else f"{r:.0f}%"   # CRWD 0.7%를 1%로 반올림하지 않게
    word = lambda sc: "싸다" if sc >= 70 else "비싸다" if sc < 30 else "중간"
    rel = lambda a, b_: "높다" if a > b_ + 0.5 else "낮다" if a < b_ - 0.5 else "비슷하다"

    # 종합 해석
    head = (f"{QL} 매출 {B(rev[cur])}" + (f"({r_rev})" if r_rev else "") + f", 영업이익률 {opm:.1f}%"
            + f"(1년 전 {opm_yo:.1f}%)"
            + f". 주가는 1년 새 {ns['CH_TXT'].replace('-', '−')}")
    # 성장 흐름: 최근 세 분기의 1년 전 대비 매출 증가율(같은 길이 분기끼리) — 3년 평균과 견주면 환율·인수가 섞인 한 분기로 "가속"이 나왔다(Fable)
    ks_all = sorted(k for k in rev if k <= cur)
    def yoy_at(k):   # 1년 전 분기와 길이가 다르면(6일 넘게) 흐름에서 뺀다(KO 1분기 +6일, Fable)
        j = [x for x in ks_all if 350 <= (d(k) - d(x)).days <= 380]
        if not j or rev[j[-1]] <= 0 or abs(A["qlen"].get(k, 91) - A["qlen"].get(j[-1], 91)) > 5:
            return None
        return (rev[k] / rev[j[-1]] - 1) * 100
    trend = [yoy_at(k) for k in ks_all[-3:]]
    trend_ok = all(x is not None for x in trend)
    gx = ("매출 성장(인수 포함)" if A.get("acq") else "매출 성장 빨라짐" if trend_ok and trend[2] > trend[1] + 1 and trend[1] >= trend[0] - 0.5 else
          "매출 성장 느려짐" if trend_ok and trend[2] < trend[1] - 1 and trend[1] <= trend[0] + 0.5 else "매출 성장 비슷")
    trend_txt = " → ".join(f"{x:+.1f}%".replace("-", "−") for x in trend) if trend_ok else ""
    vx = ("배수 5년 최저권" if selfsc >= 80 else "배수 5년 고점권" if selfsc <= 20 else
          "배수 싼 쪽" if selfsc >= 70 or peersc >= 70 else "배수 비싼 쪽" if selfsc < 30 or peersc < 30 else "배수 중간")   # 동종업 점수도 본다(CRM, Fable)
    bl = [f"매출 {B(rev[cur])}" + (f"({r_rev})" if r_rev else "") + f", 영업이익 {B(op[cur])}" + (f"({r_op})" if r_op else "")
          + f". 최근 4분기 영업이익률 {mn:.1f}%는 5년 중앙값 {m5:.1f}%보다 {rel(mn, m5)}.",
          (f"최근 4분기 FCF {B(fcf_ttm)}(매출의 {fcf_ttm / rev_ttm * 100:.1f}%), " if fcf_ok else "") + f"차입금 {B(debt)}, 현금·단기투자 {B(cash)}."]
    if A.get("dps") is not None:
        s = f"분기 주당 배당 {usd(A['dps'])}" + (f"(1년 전 {usd(A['dps_yo'])}, {chg(A['dps'], A['dps_yo'])})" if A.get("dps_yo") and chg(A["dps"], A["dps_yo"]) else "")
        if A.get("dv") is not None:
            s += f", 올해 들어 배당 {B(A['dv'])}"
        if A.get("bb") is not None:
            s += f"·자사주 매입 {B(A['bb'])}"
        bl.append(s + ".")
    dcf_txt = ("현금흐름 내재가치(기본)는 음수라 계산할 수 없다" if neg_dcf else
               f"현금흐름 내재가치(기본 ${DCF['base']:.2f})는 현재가의 {pct_txt(ratio)}다" if ratio else "")
    risk = f"세 칸이 {ns['VOTES_TXT']}, 합계 {ns['TOTAL_TXT']} “{ns['VERDICT']}”이다." + (f" {dcf_txt}." if dcf_txt else "")
    nxt = f"{C.CHECK_WHEN.split(' · ')[0]} {A['next_label']} 실적 공시."
    if trend_txt:
        bl.insert(1, f"최근 세 분기 매출 증가율(1년 전 대비, 환율·인수 포함): {trend_txt}.")
    C.SUMMARY = (head, f"{vx}·{gx}", [], risk, nxt)   # 숫자 목록은 싣지 않는다(2026-10-10 사용자 결정) — 같은 숫자가 기본적 분석 탭에 있다

    # 강세·약세: 후보마다 부호와 크기 — 큰 순으로 셋까지(가드에 걸린 지표는 뺀다)
    cand = []
    if r_rev:
        gv = float(r_rev.replace("−", "-").rstrip("%"))
        if g3 is not None:
            cand.append(("매출", (gv - g3) / 3, f"{QL} 매출 {r_rev}(보고 기준" + (", 인수 포함" if A.get("acq") else "") + f", 3년 연평균 {g3:.1f}%)."))
    if mn < 0:   # 영업적자는 강세 후보가 아니다(CRWD, Fable)
        cand.append(("마진", -1.0, f"최근 4분기 영업이익률 {mn:.1f}%(영업적자)."))
    else:
        cand.append(("마진", (mn - m5) / 2, f"최근 4분기 영업이익률 {mn:.1f}%(5년 중앙값 {m5:.1f}%)."))
    if cur in fcf and fcf[cur] < 0:   # 최근 분기 FCF 음수(투자 부담) — 4분기 합만 보면 가려진다(GOOGL, Fable)
        cand.append(("투자", -1.0, f"{QL} FCF {B(fcf[cur])}(설비투자 {B(capx.get(cur, 0))})."))
    if fcf_ok:
        fm = fcf_ttm / rev_ttm * 100
        cand.append(("현금", 1.0 if fm >= 10 else -1.0 if fm < 3 else 0, f"최근 4분기 FCF {B(fcf_ttm)}, 매출의 {fm:.1f}%."))
    nd = debt + lease - cash
    if nd < 0:   # 순현금이면 배수 대신 금액(MU, Fable)
        cand.append(("부채", 1.0, f"현금·단기투자가 차입금·리스보다 {B(-nd)} 많다(순현금)."))
    elif op_ttm > 0:
        lev = nd / op_ttm
        cand.append(("부채", 1.0 if lev <= 1 else -1.0 if lev >= 3 else 0, f"순차입금(리스 포함) {B(nd)}, 최근 4분기 영업이익의 {lev:.1f}배."))
    if H.get("growth_3y") is not None and H.get("growth_5y") and H["growth_3y"] * 100 < H["growth_5y"] * 100 - 1.5:
        cand.append(("성장", -0.7, f"3년 매출 성장률 연 {H['growth_3y'] * 100:.1f}%, 5년 연 {H['growth_5y'] * 100:.1f}%보다 낮다."))
    if A.get("dps") and A.get("dps_yo"):
        dg = (A["dps"] / A["dps_yo"] - 1) * 100
        cand.append(("환원", 1.0 if dg >= 3 else -1.0 if dg < 0 else 0, f"분기 주당 배당 {usd(A['dps'])}(1년 전보다 {dg:+.1f}%).".replace("+-", "−")))
    scored = [m for m in ns["VAL"]["self"]["metrics"] if m.get("current") is not None and m.get("score") is not None]
    span_y = lambda days: "5년" if (days or 0) >= 1200 else f"{(days or 0) / 252:.1f}년"
    name = {"per": "PER", "pbr": "PBR", "psr": "PSR", "pcr": "PCR", "evebitda": "EV/EBITDA"}
    lead = next((m for m in scored if m["metric"] == "per"), scored[0] if scored else None)   # 점수에 쓰인 배수로 설명(CRWD PER 제외, Fable)
    val_txt = (f"자기 이력 {selfsc:.0f}점(배수 {len(scored)}개) · {name[lead['metric']]} {lead['current']:.1f}배"
               f"({span_y(lead.get('days'))} 중앙값 {lead['median']:.1f}배)") if lead else f"자기 이력 {selfsc:.0f}점"
    cand.append(("밸류", (selfsc - 50) / 25, val_txt + "."))
    if neg_dcf:
        cand.append(("내재가치", -1.5, "현금흐름 내재가치(기본)는 음수 — 지금 이익률·성장으로는 계산할 수 없다."))
    elif ratio:
        cand.append(("내재가치", 1.0 if ratio >= 111 else -1.5 if ratio <= 67 else 0, f"현금흐름 내재가치(기본 ${DCF['base']:.2f})는 현재가의 {pct_txt(ratio)}."))
    yo_tab = A.get("seg_yo", {})
    if same_len:
        for n_, v_, _ in C.SEG:
            if n_ in yo_tab and yo_tab[n_] > 0 and v_ < yo_tab[n_] and v_ >= 0.1 * sum(x for _, x, _ in C.SEG):
                cand.append(("부문", -0.6 - (yo_tab[n_] - v_) / yo_tab[n_] * 10, f"{n_} 매출 {chg(v_, yo_tab[n_])}(1년 전 같은 분기 대비)."))
    _rows = {r_["metric"]: r_["value"] for ax in ns["FUND"]["axes"].values() for r_ in ax.get("rows", [])}
    if _rows.get("debtToEquity") and _rows["debtToEquity"] >= 300:
        cand.append(("부채", -1.0, f"부채비율(차입금 ÷ 자본) {_rows['debtToEquity']:.0f}%, 자본 {B(b.get('equity', 0))}."))
    if _rows.get("interestCoverage") is not None and _rows["interestCoverage"] < 3:
        cand.append(("이자", -1.0, f"이자보상배율 {_rows['interestCoverage']:.1f}배."))
    seen = set()
    cand = [c_ for c_ in sorted(cand, key=lambda c_: -abs(c_[1])) if abs(c_[1]) >= 0.5 and not (c_[0] in seen or seen.add(c_[0]))]
    C.BULL = [(a, t) for a, s, t in sorted([c_ for c_ in cand if c_[1] > 0], key=lambda c_: -c_[1])[:3]]
    C.BEAR = [(a, t) for a, s, t in sorted([c_ for c_ in cand if c_[1] < 0], key=lambda c_: c_[1])[:3]]
    if not C.BULL:
        C.BULL = [("—", "기준을 넘는 강세 지표가 없다.")]
    if not C.BEAR:
        C.BEAR = [("—", "기준을 넘는 약세 지표가 없다.")]

    # 다음 실적 체크포인트 — 숫자 기준이 있는 질문만
    ck = [f"매출 증가율(1년 전 대비)이 최근 흐름({trend_txt})보다 낮아지지 않는지" if trend_txt else
          (f"매출 증가율이 3년 연평균 {g3:.1f}% 안팎을 지키는지" if g3 is not None else f"매출 증가율({QL} {r_rev or '—'})이 이어지는지"),
          f"GAAP 영업이익률이 1년 전 같은 분기보다 높은지({QL} {opm:.1f}%, 1년 전 {opm_yo:.1f}%)",
]
    _dv_ann = (A["dv"] / max(1, A.get("dv_weeks") or 52) * 52) if A.get("dv") else None
    if fcf_ok and _dv_ann and _dv_ann > 0.5 * fcf_ttm:   # 배당이 FCF의 절반을 넘는 회사만(AAPL처럼 여유가 큰 곳은 뺀다, Fable)
        ck.append(f"FCF(최근 4분기 {B(fcf_ttm)})가 배당 지급(연 환산 약 {B(_dv_ann)})을 넘는지")
    if debt > 0 and op_ttm > 0 and (debt - cash) / op_ttm >= 2:
        ck.append(f"차입금 {B(debt)}이 줄어드는지")
    C.CHECK = ck

    # 각주·설명
    notes = []
    if not same_len:
        notes.append(f"{QL}는 {round(A['qlen'][cur] / 7)}주, {C.YL}는 {round(A['qlen'][yo] / 7)}주라 증감률을 견주지 않는다")
    if odd_yo and op[yo] <= 0:   # 음수 기저 — "낮아" 비교를 쓰지 않는다(BA, Fable)
        notes.append(f"1년 전 분기 영업이익이 0 이하(영업이익률 {opm_yo:.1f}%)라 영업이익 증감률을 쓰지 않는다")
    elif odd_yo:
        notes.append(f"1년 전 분기 영업이익률이 {opm_yo:.1f}%로 5년 중앙값({m5:.1f}%)보다 낮아 영업이익 증감률이 크게 나온다")
    C.YOY_EXTRA = "".join(n + " · " for n in notes)
    yo_tab = A.get("seg_yo", {})
    def segchg(a, b_):   # ±50%를 넘어도 적는다(MU 전부 '—'였다, Fable)
        c_ = chg(a, b_)
        if c_ or not (a and b_ and a > 0 and b_ > 0):
            return c_ or "—"
        return f"{a / b_:.1f}배" if a / b_ >= 2 else f"{(a / b_ - 1) * 100:+.0f}%".replace("-", "−")
    segs = [f"{n} {segchg(v, yo_tab.get(n))}" for n, v, _ in C.SEG if n in yo_tab]
    C.SEG_NOTE = adj_note(C) + ("1년 전 같은 분기보다 " + ", ".join(segs) + " · " if segs and same_len else "") + \
        f'출처: <a href="{C.TENQ}" target="_blank" rel="noopener">{C.TENQ_NAME} 부문 표 (SEC) →</a>'
    rows = {r["metric"]: r["value"] for ax in ns["FUND"]["axes"].values() for r in ax.get("rows", [])}
    hn = f"차입금 {B(debt)}, 현금·단기투자 {B(cash)}, 자본 {B((b.get('equity') or 0))}."
    extra_ = []
    if rows.get("currentRatio") is not None:
        extra_.append(f"유동비율 {rows['currentRatio']:.0f}%")
    if rows.get("interestCoverage") is not None:
        ic = rows["interestCoverage"]
        extra_.append(f"이자보상배율 {ic:.1f}배" if abs(ic) < 10 else f"이자보상배율 {ic:.0f}배")   # 10배 아래는 소수 한 자리(BA 0.26, Fable)
    C.HEALTH_NOTE = hn + (" " + ", ".join(extra_) + "." if extra_ else "")   # 유동비율 없을 때 '., ' 구두점(CB, Fable)
    C.FUND_TIP = f"점수는 {C.TENQ_NAME} 기준 재무로 계산했다."
    C.SELF_TIP = (f"{name[lead['metric']]} {lead['current']:.1f}배는 {span_y(lead.get('days'))} 분포의 하위 {lead.get('percentile', 0):.1f}%다(중앙값 {lead['median']:.1f}배)." if lead else "자기 이력 배수 분포 기준이다.")
    req = DCF.get("requiredMargin") if DCF.get("reqMode") == "margin" else None   # 0%도 해다 — is not None으로 본다(Codex)
    C.PREMISE = (f"{name[lead['metric']]} {lead['current']:.1f}배({span_y(lead.get('days'))} 중앙값 {lead['median']:.1f}배)로 자기 이력 {selfsc:.1f}점({word(selfsc)}), 동종업 {peersc:.1f}점({word(peersc)})이다. "
                 if lead else f"자기 이력 {selfsc:.1f}점({word(selfsc)}), 동종업 {peersc:.1f}점({word(peersc)})이다. ") + \
        (f"<strong>{dcf_txt}</strong>." if dcf_txt else "")
    if req is not None:
        tail = f" 현재가를 정당화하려면 영업이익률이 {req * 100:.1f}%까지 올라야 한다(최근 4분기 {mn:.1f}%, 5년 중앙값 {m5:.1f}%)."
    elif DCF.get("reqMode") == "margin":
        tail = f" 영업이익률을 100%로 올려도 이 모델로는 현재가에 닿지 않는다(최근 4분기 {mn:.1f}%)."   # TXN(Fable)
    elif DCF.get("requiredGrowth"):
        tail = f" 현재가를 정당화하려면 매출이 5년간 연 {DCF['requiredGrowth'] * 100:.1f}% 커야 한다."
    else:
        tail = ""
    if DCF.get("unavailable"):   # 보험사 등 현금흐름 미적용 — 내재가치 문장을 쓰지 않는다(CB, Fable)
        C.RISK = risk.replace(f" {dcf_txt}." if dcf_txt else "§", "")
        C.DCF_NOTE = "이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다)."
        C.PREMISE = C.PREMISE.split("<strong>")[0].rstrip()
        return _finish(C)
    fin_debt = debt + lease - (b.get("op_lease") or 0)   # build_dcf와 같은 정의 — 운용리스는 영업비용이라 빼지 않는다(Codex)
    C.RISK = risk + tail + f" 내재가치에서 차입금" + ("·금융리스" if lease - (b.get("op_lease") or 0) > 0 else "") + f" {B(fin_debt)}를 빼고 현금·단기투자 {B(cash)}를 더한다."
    term = 0.025   # build_dcf 영구성장률 — 시나리오 성장은 이보다 낮으면 이 값으로 둔다(build_dcf.scenarios)
    def story(g, start_what, m, m_what):
        g = g or term
        grow = (f"매출이 {start_what}(연 {g * 100:.1f}%)로 시작해 {term * 100:.1f}%로 식고" if g > term
                else f"{start_what}(연 {g * 100:.1f}%)이 영구성장률 {term * 100:.1f}%보다 낮아 5년 내내 {term * 100:.1f}%로 두고")
        return f"{grow}, 영업이익률이 {m_what} {m:.1f}%로 간다."
    C.STORIES = [story((H.get("growth_5y") or term) / 2, "5년 성장률의 절반", m5, "5년 중앙값"),
                 story(H.get("growth_5y"), "5년 성장률", m2, "최근 2년 중앙값"),
                 story(H.get("growth_3y"), "3년 성장률", mn, "최근 4분기")]
    if DCF.get("low") is not None:
        vs = [DCF["low"], DCF["base"], DCF["high"]]
        pos = [v for v in vs if v > 0]
        neg_n = len(vs) - len(pos)
        note = ((f"세 시나리오는 ${min(vs):.2f}~${max(vs):.2f}다. " if not neg_n else
                 f"세 시나리오 중 {neg_n}개는 음수라 계산할 수 없다" + ((f"(나머지 ${min(pos):.2f}~${max(pos):.2f}). " if len(pos) > 1 else f"(나머지 ${pos[0]:.2f}). ") if pos else ". "))   # 음수를 드러내지 않는다(BA·TMO, Fable)
                + f"영업이익률은 최근 4분기 {mn:.1f}%, 2년 중앙값 {m2:.1f}%, 5년 중앙값 {m5:.1f}%를 쓴다.")
        g_ = lambda g: max(g or term, term) * 100
        assume = (f"보수(성장 연 {g_((H.get('growth_5y') or term) / 2):.1f}%·이익률 {m5:.1f}%), 기본({g_(H.get('growth_5y')):.1f}%·{m2:.1f}%), "
                  f"낙관({g_(H.get('growth_3y')):.1f}%·{mn:.1f}%)")
        if abs(DCF["low"] - DCF["base"]) < 0.01:
            note += f" 보수와 기본이 같다 — {assume}."
        elif DCF["low"] > DCF["base"] or DCF["high"] < DCF["base"]:
            note += f" 시나리오 순서가 이름과 다르다 — 가정이 서로 엇갈린다: {assume}."   # 원인을 단정하지 않고 가정만(Fable)
        C.DCF_NOTE = note
    else:
        C.DCF_NOTE = ""
    return _finish(C)


def _finish(C):
    # 음수 표기: 문장 속 '-5.0%'·'$-' 를 '−'로(Fable) — 주소·날짜(앞이 글자·숫자·'/')는 건드리지 않는다
    import re as _re
    def fix(t):   # 태그 밖 글자에만 — 주소·class·CSS(margin-top:-2px)는 건드리지 않는다(Codex)
        if not isinstance(t, str):
            return t
        parts = _re.split(r"(<[^>]*>)", t)
        return "".join(p_ if p_.startswith("<") else _re.sub(r"(?<![\w/.])-(?=\$?\d)", "−", p_.replace("$-", "−$")) for p_ in parts)
    deep = lambda v: [deep(x) for x in v] if isinstance(v, list) else tuple(deep(x) for x in v) if isinstance(v, tuple) else fix(v)
    for k in ("SUMMARY", "BULL", "BEAR", "CHECK", "YOY_EXTRA", "SEG_NOTE", "HEALTH_NOTE", "PREMISE", "RISK", "DCF_NOTE", "STORIES", "SELF_TIP"):
        setattr(C, k, deep(getattr(C, k)))

    return None
