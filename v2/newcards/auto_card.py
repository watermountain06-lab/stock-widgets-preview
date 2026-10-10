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
        if rows:
            return sorted(rows, key=lambda r: r["filed"])[0]["val"], d(end) - d(rows[0]["start"])
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
        return sorted(q, key=lambda r: r["filed"])[0]["val"]
    if is_q4:
        fy = [r for r in rows if r.get("end") == end and r.get("start") and 350 <= (d(end) - d(r["start"])).days <= 380]
        n9 = [r for r in rows if r.get("end") == prev_end and r.get("start") and abs((d(r["start"]) - fy_start).days) <= 10]
        if fy and n9:
            return round(fy[0]["val"] - n9[0]["val"], 4)
    return None


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
    cur_v = sx.quarter_values(M, form, C.TENQ, C.CUR, q3_url=q3, q3_end=C.QO)
    if is_q4:
        yo_q3 = ends[ends.index(C.YO) - 1]
        yo_v = sx.quarter_values(M, "10-K", C.TENQ, C.YO, q3_url=q3, q3_end=yo_q3)
    else:
        yo_v = sx.quarter_values(M, "10-Q", C.TENQ, C.YO)
    ref_adj = abs(getattr(C, "SEG_ADJ", 0) or 0)   # 사람이 확인해 둔 본사·상계 조정의 크기(cfg 원래 값) — 허용 범위의 기준
    C.SEG, C.SEG_ADJ = sx.table(M, cur_v)
    # 부문 합과 매출의 차이(본사·상계 등)는 남은 값으로 넣되, 매출의 3%를 넘으면 지도가 틀린 것으로 보고 멈춘다(2026-10-10)
    _, _rows = bmh.pick_tag(cik, bmh.FLOW_TAGS["revenue"])
    _rev = {e["end"]: e["val"] for e in bmh.quarterly_flow(_rows, T)}
    if C.CUR in _rev:
        resid = _rev[C.CUR] / 1e6 - sum(v for _, v, _ in C.SEG) - C.SEG_ADJ
        if abs(resid) > max(0.03 * _rev[C.CUR] / 1e6, 1.5 * ref_adj):   # GLW 환헤지 −233·TMO 부문 간 거래 −566은 정상
            raise SystemExit(f"{T}: 부문 합이 매출과 {resid:,.0f}백만 달러 다르다 — SEG_MAP 확인")
        C.SEG_ADJ = round(C.SEG_ADJ + resid)
    yo_tab = {n: v for n, v, _ in sx.table(M, yo_v)[0]} if yo_v else {}
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
    core_note = " · 차트 순이익은 본업 기준" if T in json.load(open(os.path.join(V2, "core_earnings.json"))) else ""
    C.STAT3 = (f"희석 EPS ({C.QLABEL})", f"${e_cur:.2f}".replace("$-", "−$"),
               "GAAP · " + (f"1년 전 ${e_yo:.2f} ({c})" if c else f"1년 전 ${e_yo:.2f}" if e_yo is not None else "1년 전 값 없음") + core_note)

    # 자본배분: 자사주 매입·배당 지급(올해 누계), 분기 주당 배당(선언 기준)
    def span(td):   # 회계연도가 1월에 시작하지 않으면 "연초"가 아니라 회계연도 누계로(Fable — AAPL 9/28 시작)
        st = d(C.CUR) - td
        if st.month == 1 and st.day <= 7:
            return f"연초~{d(C.CUR).month}/{d(C.CUR).day}, {round(td.days / 7)}주"
        return f"회계연도 누계 {st.month}/{st.day}~{d(C.CUR).month}/{d(C.CUR).day}, {round(td.days / 7)}주"
    bb, bbd = ytd(cik, ["PaymentsForRepurchaseOfCommonStock"], C.CUR, fy_start)
    dv, dvd = ytd(cik, ["PaymentsOfDividendsCommonStock", "PaymentsOfDividends"], C.CUR, fy_start)
    C._AUTO["dv_weeks"] = round(dvd.days / 7) if dvd else None
    yo_q3 = ends[ends.index(C.YO) - 1]
    dps, dtag = dps_quarter(cik, C.CUR, C.QO, fy_start, is_q4)
    dps_yo = dps_quarter(cik, C.YO, yo_q3, d(C.FY_ENDS[1]) if not is_q4 else d(ends[0]), is_q4, dtag) if dps is not None else None
    if dps is not None and is_q4:   # 4분기 1년 전: 전년 연간 − 전년 9개월(전년 회계연도 시작은 FY_ENDS 두 칸 앞)
        prev_fy = [x for x in fy_ends if d(x) < d(C.YO)]
        dps_yo = dps_quarter(cik, C.YO, yo_q3, d(prev_fy[-1]) if prev_fy else fy_start, True, dtag)
    C.CAPITAL = [(f"자사주 매입 ({span(bbd)})" if bb is not None else "자사주 매입", B(bb) if bb is not None else "공시 없음"),
                 (f"배당 지급 ({span(dvd)})" if dv is not None else "배당 지급", B(dv) if dv is not None else "공시 없음"),
                 (f"분기 주당 배당 ({dict(DPS_TAGS).get(dtag, '선언 기준')})",
                  ("1년 전 " + usd(dps_yo) + (f" · {chg(dps, dps_yo)}" if chg(dps, dps_yo) else "")) if dps_yo else "1년 전 값 없음",
                  usd(dps) if dps is not None else "공시 없음")]
    C._AUTO.update({"bb": bb, "dv": dv, "dps": dps, "dps_yo": dps_yo})
    gw = {r["end"]: r["val"] for r in sorted(_flow_rows(cik, "Goodwill"), key=lambda r: r["filed"])}
    C._AUTO["acq"] = bool(gw.get(C.CUR) and gw.get(C.YO) and gw[C.CUR] > gw[C.YO] * 1.15)   # 영업권이 1년에 15% 넘게 늘면 인수가 매출 성장에 섞였다(ABT, Fable)

    # 실적 보도자료 링크와 다음 실적일(작년 같은 분기의 실적 8-K + 364일, "예상")
    sub = _submissions(cik)
    rel = [(sub["filingDate"][i], sub["accessionNumber"][i], sub["primaryDocument"][i]) for i, f in enumerate(sub["form"])
           if f == "8-K" and "2.02" in sub["items"][i].split(",")]
    def first_release(after, within=80):
        c_ = sorted(x for x in rel if 0 < (d(x[0]) - d(after)).days <= within)
        return c_[0] if c_ else None
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
        C.NEXT = (f"{est.month}월 {est.day}일 무렵 예상", f"일정 · {nl} (작년 발표일로 추정)")
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
    same_len = abs(A["qlen"].get(cur, 91) - A["qlen"].get(yo, 91)) <= 7
    opm, opm_yo = op[cur] / rev[cur] * 100, op[yo] / rev[yo] * 100
    m5, m2, mn = H.get("margin_5y", 0) * 100, H.get("margin_2y", 0) * 100, H.get("margin_now", 0) * 100
    g3 = H.get("growth_3y", 0) * 100
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
    ratio = (DCF["base"] / px * 100) if DCF.get("base") else None
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
    risk = f"세 칸이 {ns['VOTES_TXT']}, 합계 {ns['TOTAL_TXT']} “{ns['VERDICT']}”이다." + (f" 현금흐름 내재가치(기본 ${DCF['base']:.2f})는 현재가의 {ratio:.0f}%다." if ratio else "")
    nxt = f"{C.CHECK_WHEN.split(' · ')[0]} {A['next_label']} 실적 공시."
    if trend_txt:
        bl.insert(1, f"최근 세 분기 매출 증가율(1년 전 대비, 환율·인수 포함): {trend_txt}.")
    C.SUMMARY = (head, f"{vx}·{gx}", [], risk, nxt)   # 숫자 목록은 싣지 않는다(2026-10-10 사용자 결정) — 같은 숫자가 기본적 분석 탭에 있다

    # 강세·약세: 후보마다 부호와 크기 — 큰 순으로 셋까지(가드에 걸린 지표는 뺀다)
    cand = []
    if r_rev:
        gv = float(r_rev.replace("−", "-").rstrip("%"))
        cand.append(("매출", (gv - g3) / 3, f"{QL} 매출 {r_rev}(보고 기준" + (", 인수 포함" if A.get("acq") else "") + f", 3년 연평균 {g3:.1f}%)."))
    cand.append(("마진", (mn - m5) / 2, f"최근 4분기 영업이익률 {mn:.1f}%(5년 중앙값 {m5:.1f}%)."))
    if fcf_ok:
        fm = fcf_ttm / rev_ttm * 100
        cand.append(("현금", 1.0 if fm >= 10 else -1.0 if fm < 3 else 0, f"최근 4분기 FCF {B(fcf_ttm)}, 매출의 {fm:.1f}%."))
    if op_ttm > 0:
        lev = (debt + lease - cash) / op_ttm
        cand.append(("부채", 1.0 if lev <= 1 else -1.0 if lev >= 3 else 0, f"순차입금(리스 포함) {B(debt + lease - cash)}, 최근 4분기 영업이익의 {lev:.1f}배."))
    if H.get("growth_3y") is not None and H.get("growth_5y") and H["growth_3y"] * 100 < H["growth_5y"] * 100 - 1.5:
        cand.append(("성장", -0.7, f"3년 매출 성장률 연 {H['growth_3y'] * 100:.1f}%, 5년 연 {H['growth_5y'] * 100:.1f}%보다 낮다."))
    if A.get("dps") and A.get("dps_yo"):
        dg = (A["dps"] / A["dps_yo"] - 1) * 100
        cand.append(("환원", 1.0 if dg >= 3 else -1.0 if dg < 0 else 0, f"분기 주당 배당 {usd(A['dps'])}(1년 전보다 {dg:+.1f}%).".replace("+-", "−")))
    if per.get("current"):
        cand.append(("밸류", (selfsc - 50) / 25, f"자기 이력 {selfsc:.0f}점(다섯 배수의 5년 위치) · PER {per['current']:.1f}배(5년 중앙값 {per['median']:.1f}배)."))
    if ratio:
        cand.append(("내재가치", 1.0 if ratio >= 111 else -1.5 if ratio <= 67 else 0, f"현금흐름 내재가치(기본 ${DCF['base']:.2f})는 현재가의 {ratio:.0f}%."))
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
    ck = [f"매출 증가율(1년 전 대비)이 최근 흐름({trend_txt})보다 낮아지지 않는지" if trend_txt else f"매출 증가율이 3년 연평균 {g3:.1f}% 안팎을 지키는지",
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
    if odd_yo:
        notes.append(f"1년 전 분기 영업이익률이 {opm_yo:.1f}%로 5년 중앙값({m5:.1f}%)보다 낮아 영업이익 증감률이 크게 나온다")
    C.YOY_EXTRA = "".join(n + " · " for n in notes)
    yo_tab = A.get("seg_yo", {})
    segs = [f"{n} {chg(v, yo_tab.get(n)) or '—'}" for n, v, _ in C.SEG if n in yo_tab]
    C.SEG_NOTE = ("1년 전 같은 분기보다 " + ", ".join(segs) + " · " if segs and same_len else "") + \
        f'출처: <a href="{C.TENQ}" target="_blank" rel="noopener">{C.TENQ_NAME} 부문 표 (SEC) →</a>'
    rows = {r["metric"]: r["value"] for ax in ns["FUND"]["axes"].values() for r in ax.get("rows", [])}
    hn = f"차입금 {B(debt)}, 현금·단기투자 {B(cash)}, 자본 {B(b.get('equity', 0))}."
    if rows.get("currentRatio") is not None:
        hn += f" 유동비율 {rows['currentRatio']:.0f}%"
    if rows.get("interestCoverage") is not None:
        hn += f", 이자보상배율 {rows['interestCoverage']:.0f}배"   # 칸 표시(정수)와 맞춘다
    C.HEALTH_NOTE = hn + "."
    C.FUND_TIP = f"점수는 {C.TENQ_NAME} 기준 재무로 계산했다."
    C.SELF_TIP = (f"PER {per['current']:.1f}배는 5년 분포의 하위 {per.get('percentile', 0):.1f}%다(중앙값 {per['median']:.1f}배)." if per.get("current") else "자기 이력 배수 분포 기준이다.")
    req = DCF.get("requiredMargin") if DCF.get("reqMode") == "margin" else None
    C.PREMISE = (f"PER {per['current']:.1f}배(5년 중앙값 {per['median']:.1f}배)로 자기 이력 {selfsc:.1f}점({word(selfsc)}), 동종업 {peersc:.1f}점({word(peersc)})이다. "
                 if per.get("current") else f"자기 이력 {selfsc:.1f}점({word(selfsc)}), 동종업 {peersc:.1f}점({word(peersc)})이다. ") + \
        (f"<strong>현금흐름 내재가치(기본 ${DCF['base']:.2f})는 현재가의 {ratio:.0f}%</strong>다." if ratio else "")
    if req:
        tail = f" 현재가를 정당화하려면 영업이익률이 {req * 100:.1f}%까지 올라야 한다(최근 4분기 {mn:.1f}%, 5년 중앙값 {m5:.1f}%)."
    elif DCF.get("reqMode") == "margin":
        tail = f" 영업이익률을 100%로 올려도 이 모델로는 현재가에 닿지 않는다(최근 4분기 {mn:.1f}%)."   # TXN(Fable)
    elif DCF.get("requiredGrowth"):
        tail = f" 현재가를 정당화하려면 매출이 5년간 연 {DCF['requiredGrowth'] * 100:.1f}% 커야 한다."
    else:
        tail = ""
    C.RISK = risk + tail + f" 내재가치에서 차입금·리스 {B(debt + lease)}를 빼고 현금·단기투자 {B(cash)}를 더한다."
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
        note = f"세 시나리오는 ${min(vs):.2f}~${max(vs):.2f}다. 영업이익률은 최근 4분기 {mn:.1f}%, 2년 중앙값 {m2:.1f}%, 5년 중앙값 {m5:.1f}%를 쓴다."
        if abs(DCF["low"] - DCF["base"]) < 0.01:
            note += " 보수와 기본이 같다 — 두 시나리오의 성장률이 모두 영구성장률 하한(2.5%)이고 이익률도 같아서다."
        elif DCF["low"] > DCF["base"] or DCF["high"] < DCF["base"]:
            note += " 시나리오 순서가 뒤집혀 있다 — 성장률보다 이익률 가정(보수 5년·기본 2년·낙관 최근)의 차이가 커서다."
        C.DCF_NOTE = note
    else:
        C.DCF_NOTE = ""
