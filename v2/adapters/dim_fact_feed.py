#!/usr/bin/env python3
"""차원(축·멤버)이 붙은 원문 XBRL 값 하나를 overlay의 이름 붙인 태그로 싣는다 — 분기마다 손으로 옮기지 않게(2026-10-17, PWR).

SEC companyfacts에는 차원 값이 없다. PWR은 장기투자(LongTermInvestments) 안의 "비통합 지분법 투자"를
us-gaap:EquityMethodInvestments + 축 srt:ScheduleOfEquityMethodInvestmentEquityMethodInvesteeNameAxis
= pwr:NonIntegralUnconsolidatedAffiliatesMember 로만 낸다. since 이후 10-Q·10-K 원문(부문 표와 같은 캐시
`.sec_cache/ixbrl/{접수번호}.json`, newcards/seg_xbrl.facts)에서 **그 축·멤버 하나만 붙은 시점 값**을 꺼내
`.sec_cache/overlay/{cik}.json`의 us-gaap 아래 std_tag 이름으로 더한다. 같은 결산일은 처음 공시한 행만(나중 공시의
비교 수치를 앞당겨 쓰지 않는다 — 공개일은 그 공시의 접수일). 정정 공시(10-Q/A·10-K/A)도 읽어, 값을 바꿨으면 멈춘다.

멈춤(0이 아닌 종료 코드): 가장 최근 10-Q·10-K에 그 결산일 값이 없으면 — 멤버 이름이 바뀌었거나 항목이 없어진 것이라,
옛 값으로 조용히 계산하지 않고 빌드를 멈춘다(dr 2026-10-17, Fable). 원문에서 사실이 하나도 안 나오면 받은 것을 버린다.

    python3 v2/adapters/dim_fact_feed.py 0001050915 us-gaap:EquityMethodInvestments \\
        srt:ScheduleOfEquityMethodInvestmentEquityMethodInvesteeNameAxis pwr:NonIntegralUnconsolidatedAffiliatesMember \\
        EquityMethodInvestmentsNonIntegralPwr --since 2021-01-01
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(V2, "newcards"))
import seg_xbrl  # noqa: E402

OVERLAY = os.path.join(V2, ".sec_cache", "overlay")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cik"); ap.add_argument("concept"); ap.add_argument("axis"); ap.add_argument("member"); ap.add_argument("std_tag")
    ap.add_argument("--since", default="2021-01-01")
    a = ap.parse_args()
    cik = a.cik.zfill(10)
    subj = json.loads(seg_xbrl._get(f"https://data.sec.gov/submissions/CIK{cik}.json"))["filings"]
    # "recent"는 최근 1,000건뿐 — 과거 목록 페이지까지 읽어 처음 공시를 놓치지 않는다(Codex r2)
    pages = [subj["recent"]] + [json.loads(seg_xbrl._get(f"https://data.sec.gov/submissions/{f_['name']}"))
                                for f_ in subj.get("files", []) if f_.get("filingTo", "9999") >= a.since]
    filings = sorted({(f, fm, acc, doc, rd) for sub in pages for fm, acc, f, doc, rd in zip(sub["form"], sub["accessionNumber"], sub["filingDate"],
                     sub["primaryDocument"], sub["reportDate"]) if fm in ("10-Q", "10-K", "10-Q/A", "10-K/A") and f >= a.since and doc.endswith((".htm", ".html"))})
    if not filings:
        sys.exit(f"{cik}: {a.since} 뒤 10-Q·10-K가 없다")
    op = os.path.join(OVERLAY, f"{cik}.json")
    data = json.load(open(op)) if os.path.exists(op) else {}
    rows = data.setdefault("us-gaap", {}).setdefault(a.std_tag, [])
    have = {r["end"]: r for r in rows}
    want = ((a.axis, a.member),)
    added, latest_ok = 0, False
    # 검증 대상은 결산일이 가장 늦은 정기 공시(10-Q·10-K) — 그 뒤 접수된 과거 분기 정정 공시(/A)가 검증을 대신하지 않게(Codex r3)
    target = max(((rd, f, acc) for f, fm, acc, doc, rd in filings if not fm.endswith("/A")), default=None)
    for filed, form, acc, doc, rd in filings:   # 오래된 공시부터 — 같은 결산일은 처음 공시가 남는다
        url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}"
        facts = seg_xbrl.facts(url)
        if not facts and form.endswith("/A"):   # XBRL 없는 축약 정정 공시(표지·첨부 보정)는 정상 — 건너뛴다(Codex r4)
            print(f"{form} {filed}: XBRL 사실 없음(축약 정정) — 건너뜀")
            continue
        if not facts:   # 원본 공시인데 사실이 없으면 오류 페이지·빈 원문 — 성공으로 남기지 않는다
            p_ = os.path.join(seg_xbrl.CACHE, f"{acc.replace('-', '')}.json")
            if os.path.exists(p_):
                os.remove(p_)
            sys.exit(f"{form} {filed} {acc}: 원문에서 XBRL 사실을 못 읽었다 — 다시 시도")
        got = {}
        for name, s, e, dims, v in facts:
            if name == a.concept and s is None and tuple(dims) == want:
                if e in got and abs(got[e] - v) > 0.5:   # 한 공시 안에서 같은 결산일 값이 엇갈리면 고르지 않는다(Codex r2)
                    sys.exit(f"멈춤: {form} {filed} {acc}에 {e} 값이 둘({got[e]:,.0f}·{v:,.0f})")
                got[e] = v
        for e, v in sorted(got.items()):
            if e in have:
                # 처음 공시 행을 남긴다. 정정 공시(/A)가 값을 바꿨으면 조용히 섞지 않고 멈춘다(Codex·Fable r2)
                if form.endswith("/A") and abs(have[e]["val"] - v) > 0.005 * max(abs(v), 1):
                    sys.exit(f"멈춤: 정정 공시 {form} {filed}가 {e} 값을 {have[e]['val']:,.0f} → {v:,.0f}로 바꿨다 — 적용 방식을 정할 것")
                continue
            row = {"end": e, "val": v, "accn": acc, "fp": "FY" if form.startswith("10-K") else "Q", "form": form, "filed": filed,
                   "unit": "USD", "src": f"dim:{a.concept}|{a.axis}={a.member}"}
            rows.append(row); have[e] = row; added += 1
        if target and (rd, filed, acc) == target:
            latest_ok = rd in got
        print(f"{form} {filed}: {len(got)}개 시점" + (f" (결산일 {rd} 값 {got[rd] / 1e6:,.1f}M)" if rd in got else f" (결산일 {rd} 값 없음)"))
    if not latest_ok:   # 검증에 실패하면 저장하지 않는다 — 실패한 상태가 캐시로 남아 다음 실행이 건너뛰지 않게(Codex r2)
        sys.exit(f"멈춤: 가장 최근 정기 공시(결산일 {target[0] if target else '?'}, 접수 {target[1] if target else '?'})에 {a.member} 값이 없다 — 멤버 이름·항목을 원문에서 확인하고 cfg BUILD['dim_facts']를 고칠 것")
    rows.sort(key=lambda r: (r["end"], r["filed"]))
    os.makedirs(OVERLAY, exist_ok=True)
    json.dump(data, open(op, "w"), indent=1)
    # 확인한 마지막 공시 접수일 — 내용 없는 정정 공시(/A)가 승인되면 태그 행 접수일이 승인일보다 계속 앞서 매일 다시 받던 것을 막는다(Fable r3).
    # overlay 본문은 엔진이 태그 표로 읽으므로 따로 둔다.
    ck = os.path.join(OVERLAY, f"{cik}.dimcheck.json")
    marks = json.load(open(ck)) if os.path.exists(ck) else {}
    marks[a.std_tag] = filings[-1][0]
    json.dump(marks, open(ck, "w"), indent=1)
    print(f"저장: {op} ({a.std_tag} +{added}행)")


if __name__ == "__main__":
    main()
