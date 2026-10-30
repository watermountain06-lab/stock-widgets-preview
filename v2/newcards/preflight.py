#!/usr/bin/env python3
"""새 카드 공시 기준 검사(C6, dr 2026-10-13) — 한 카드 안에 서로 다른 공시가 섞이지 않게.

    python3 v2/newcards/preflight.py VLO --asof 2026-10-12     # 빌드 전(build.py가 새 종목이면 자동으로 부른다)
    python3 v2/newcards/preflight.py VLO --after               # 빌드 뒤: 카드 재무의 접수일 = 기준표, 매일 실행이 재빌드 고리에 빠지지 않는지

규칙(빌드 전)
- 쓰는 공시 = SEC 제출 목록의 가장 최근 **원본** 10-Q/10-K. 재무 수집기(vendor/fetch_financials.py)가 원본만 읽어서 정정 공시를 기준으로 삼으면
  재무(원본)와 배수·활동성(정정)이 섞이고, 기준표가 카드 재무 접수일보다 뒤가 되어 매일 --weekly로 돈다(daily_price.auto_quarter_due).
- 그 원본이 SEC 요약 자료(companyfacts)에 실려 있어야 한다(없으면 build_multiple_history._facts가 멈춘다).
- 그 원본 뒤에 정정(10-Q/A·10-K/A)이 접수돼 있으면 멈춘다 — 사람이 처리(정정 처리 방침이 정해지기 전까지 그 종목은 보류).
- v2/sec_approved.json[10자리 CIK] = 그 원본의 접수일(filingDate). 없거나 다르면 고칠 값을 알려 주고 멈춘다.
- --asof는 그 공시 접수 뒤 첫 확정 세션 이상.
종료 코드 0 = 통과, 1 = 멈춤(이유 출력).
"""
import argparse
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
sys.path.insert(0, HERE)
sys.path.insert(0, V2)
sys.path.insert(0, os.path.join(REPO, "scripts"))


def cik_of(T):
    for d in (os.path.join(HERE, "bank", "cfg"), os.path.join(HERE, "cfg")):
        p = os.path.join(d, f"cfg_{T.lower()}.py")
        if os.path.exists(p):
            sp = importlib.util.spec_from_file_location("cfg", p)
            C = importlib.util.module_from_spec(sp)
            sp.loader.exec_module(C)
            return str(C.CIK).zfill(10)
    import fetch_eps_history as feh   # cfg를 아직 안 쓴 새 종목
    return str(feh.CIKS[T]).zfill(10)


# SEC 요약 자료(companyfacts·companyconcept)에서 최근 분기가 빠진 종목 — 최신 원본이 아직 안 실렸으면 실린 것 중 가장 최근 원본을 기준으로 만든다
# (2026-10-24 사용자 결정). 합산 공시 때문이 아니다: BIIB는 단일 법인이고, NEE는 10-02에 받은 자료에 Q2가 있었는데 지금은 Q1까지만 있다 — SEC 쪽에서 빠진 상태로 본다.
# 기준표(sec_approved)를 그 공시일로 두면 매일 실행(auto_approve)이 자료가 돌아온 날 그때 실린 가장 최근 공시로 스스로 넘겨받는다.
ALLOW_LAGGED = {"SO", "DUK", "ED", "BIIB"}


# 인라인 XBRL 보충으로 만들 수 있게 허용한 종목 — 시험 3장(2026-10-25 사용자 결정). 넓힐 때 여기에 더한다.
OVERLAY_OK = {"PPG", "MDLZ", "GD", "CDNS", "ETR", "EXC", "VMC", "AEP", "CNP", "VRSK", "EVRG", "LNT"}   # JCI는 시험 중 보류(이자 정의 — skipped_cards E)


def overlay_has(T, cik, accn, form=None, filed=None):
    """cfg에 BUILD overlay를 켠 종목이고, 인라인 XBRL 보충 파일(.sec_cache/overlay/{cik}.json)에 그 공시(접수 번호)의 행이 실제로 있는가.
    요약 자료가 몇 달째 최신 10-Q를 싣지 않는 종목을 원문 보충으로 만들 때만 쓴다(2026-10-25 사용자 결정 — 시험 3장 PPG·MDLZ·JCI, JCI는 보류)."""
    p = os.path.join(HERE, "cfg", f"cfg_{T.lower()}.py")
    if not os.path.exists(p):
        return False
    sp = importlib.util.spec_from_file_location("cfg_ov", p)
    C = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(C)
    if T not in OVERLAY_OK or not getattr(C, "BUILD", {}).get("overlay"):
        return False
    op = os.path.join(V2, ".sec_cache", "overlay", f"{cik}.json")
    if not os.path.exists(op):
        return False
    ov = json.load(open(op))
    # 그 공시 행이 하나만 있어도 통과하던 것을 막는다(Codex r1): 그 공시 기간말에 희석 EPS 행과 태그 30개 이상이 있어야 한다
    hit = {}
    for tx in ov.values():
        if not isinstance(tx, dict):
            continue
        for tag, rows_ in tx.items():
            for x in rows_ if isinstance(rows_, list) else []:
                if (x.get("accn") == accn and x.get("src") == "ixbrl" and (form is None or x.get("form") == form)
                        and (filed is None or x.get("filed") == filed)):
                    hit.setdefault(x.get("end"), set()).add(tag)
    if not hit:
        return False
    tags = max(hit.values(), key=len)   # 그 공시 기간말(태그가 가장 많은 날짜) — 표지 주식수 날짜(MDLZ 7/24)는 태그가 하나뿐
    return len(tags) >= 30 and bool(tags & {"EarningsPerShareDiluted", "IncomeLossFromContinuingOperationsPerDilutedShare"})


def before(T, asof):
    import daily_price as dp
    import fetch_eps_history as feh
    cik = cik_of(T)
    try:   # 새 카드 검사는 캐시(_submissions — 당일 재사용·실패 시 옛 캐시)를 쓰지 않고 늘 새로 받는다(Codex 2026-10-13)
        r = feh.curl_json(f"https://data.sec.gov/submissions/CIK{cik}.json")["filings"]["recent"]
    except Exception as e:
        return [f"{T}: SEC 제출 목록을 새로 받지 못했다({type(e).__name__}) — 다시 시도"]
    rows = sorted(((r["filingDate"][i], r["acceptanceDateTime"][i], f, r["accessionNumber"][i]) for i, f in enumerate(r["form"])
                   if f in ("10-Q", "10-K", "10-Q/A", "10-K/A")), reverse=True)
    orig = next((x for x in rows if x[2] in ("10-Q", "10-K")), None)
    if not orig:
        return [f"{T}: SEC 제출 목록에 10-Q/10-K가 없다"]
    filed, accepted, form, accn = orig
    bad = []
    amend = [x for x in rows if x[2].endswith("/A") and x[1] > accepted]   # 접수 시각으로 — 같은 날 정정도 잡는다(Codex)
    if amend:
        bad.append(f"{T}: 원본 {form} {filed} 뒤에 정정 공시가 있다({', '.join(f'{x[2]} {x[0]}' for x in amend)}) — 사람이 처리(정정 처리 방침 전까지 보류)")
    facts = feh.curl_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json")
    have = any(x.get("filed") == filed and x.get("form") == form for tx in facts.get("facts", {}).values()
               for tg in tx.values() for rows_ in tg.get("units", {}).values() for x in rows_)
    if not have and T in ALLOW_LAGGED:
        for x in rows:
            if x[2] in ("10-Q", "10-K") and any(y.get("filed") == x[0] and y.get("form") == x[2] for tx in facts.get("facts", {}).values()
                                              for tg in tx.values() for rows_ in tg.get("units", {}).values() for y in rows_):
                print(f"{T}: 최신 {form} {filed}이 요약 자료에 아직 없다 — 실린 {x[2]} {x[0]}를 기준으로(ALLOW_LAGGED)")
                filed, accepted, form, accn = x
                have = True
                # 고른 원본 뒤 정정도 다시 본다 — 최신 원본 기준 검사는 그 사이의 정정(예: Q1/A)을 놓친다(Codex r1)
                am2 = [y for y in rows if y[2].endswith("/A") and y[1] > accepted and y not in amend]
                if am2:
                    bad.append(f"{T}: 원본 {form} {filed} 뒤에 정정 공시가 있다({', '.join(f'{y[2]} {y[0]}' for y in am2)}) — 사람이 처리")
                break
    if not have and overlay_has(T, cik, accn, form, filed):
        print(f"{T}: 최신 {form} {filed}이 요약 자료에 아직 없다 — 인라인 XBRL 보충 파일에 그 공시 행이 있어 그것으로 만든다(BUILD overlay)")
        have = True
    if not have:
        bad.append(f"{T}: {form} {filed}({accn})이 SEC 요약 자료(companyfacts)에 아직 없다 — 실린 뒤에 만든다")
    else:
        json.dump(facts, open(os.path.join(V2, ".sec_cache", f"{cik}_facts.json"), "w"))   # 같은 자료로 빌드하게(daily_price.auto_approve와 같은 처리)
    table = json.load(open(os.path.join(V2, "sec_approved.json")))
    if table.get(cik) != filed:
        bad.append(f'{T}: v2/sec_approved.json에 "{cik}": "{filed}"를 넣을 것(지금 {table.get(cik)!r})')
    first = dp.first_session_after(accepted)
    if asof and asof < first:
        bad.append(f"{T}: --asof {asof}가 {form} 접수({accepted}) 뒤 첫 세션 {first}보다 앞이다")
    print(f"{T}: 기준 공시 {form} {filed} (접수 {accepted}, 첫 세션 {first}), CIK {cik}")
    return bad


def after(T):
    import daily_price as dp
    import new_filings as nf
    cik = cik_of(T)
    table = json.load(open(os.path.join(V2, "sec_approved.json")))
    asof, filed = nf.card_asof(T)
    bad = []
    if not filed or table.get(cik) != str(filed)[:10]:
        bad.append(f"{T}: 카드 재무 접수일(FUNDAMENTAL.filedAt) {filed} ≠ 기준표 {table.get(cik)} — 매일 실행의 기준과 어긋난다")
    if dp.auto_quarter_due(T):
        bad.append(f"{T}: auto_quarter_due가 참 — 매일 실행이 이 카드를 날마다 --weekly로 다시 만든다")
    print(f"{T}: 카드 재무 {asof} (접수 {filed}), 기준표 {table.get(cik)}")
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--asof")
    ap.add_argument("--after", action="store_true")
    a = ap.parse_args()
    T = a.ticker.upper()
    bad = after(T) if a.after else before(T, a.asof)
    for b in bad:
        print("  멈춤 —", b)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
