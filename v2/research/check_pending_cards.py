#!/usr/bin/env python3
"""보류 카드 대기 목록(skipped_cards.md)의 A 묶음(공시 대기)이 풀렸는지 확인한다 — 읽기 전용.

    python3 v2/research/check_pending_cards.py            # A 묶음 전부
    python3 v2/research/check_pending_cards.py SPGI CAH   # 고른 카드만

확인 칸:
  SEC          — 가장 최근 10-Q·10-K(정정 제외)가 SEC 요약 자료(companyfacts)에 실렸는가
  10-Q≥날짜    — 그 날짜 이후에 끝나는 분기의 10-Q가 나왔고 요약 자료에 실렸는가(10-K도 같은 방식)
"실렸다"는 그 보고서의 결산일·접수 번호를 가진 희석(또는 기본) EPS 사실이 있는가로 본다.
파일을 쓰지 않는다(SEC 응답은 메모리에서만 쓴다).
"""
import json, os, re, subprocess, sys, time

UA = "stock-widgets research gptjhss@gmail.com"
HERE = os.path.dirname(os.path.abspath(__file__))
SKIP = os.path.join(HERE, "skipped_cards.md")


def get(url):
    for _ in range(3):
        out = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True).stdout
        try:
            return json.loads(out)
        except json.JSONDecodeError:
            time.sleep(1)
    raise RuntimeError(f"SEC 응답을 읽지 못했다: {url}")


def section_a():
    """A 묶음 표에서 (카드, 확인 코드, 다시 볼 때)를 읽는다."""
    rows, on = [], False
    for line in open(SKIP, encoding="utf-8"):
        if line.startswith("## "):
            on = line.startswith("## A.")
            continue
        m = re.match(r"^\| ([A-Z.]+) \| `([^`]+)` \| ([^|]*)\|", line) if on else None
        if m:
            rows.append((m.group(1), m.group(2), m.group(3).strip()))
    return rows


def check(cik, code):
    r = get(f"https://data.sec.gov/submissions/CIK{cik}.json")["filings"]["recent"]
    filings = [(r["form"][i], r["reportDate"][i], r["filingDate"][i], r["accessionNumber"][i])
               for i in range(len(r["form"])) if r["form"][i] in ("10-Q", "10-K")]
    if code == "SEC":
        want = filings[:4]   # 최근 4개 보고서가 모두 실려야 최근 4분기를 만든다(CAH — 10-K는 실렸는데 앞 10-Q가 빠짐, 2026-10-24)
    else:
        form, day = re.match(r"(10-[QK])≥(\d{4}-\d{2}-\d{2})", code).groups()
        want = [f for f in filings if f[0] == form and f[1] >= day][-1:]
    if not want:
        return "대기", "아직 해당 보고서 없음"
    facts = get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json").get("facts", {}).get("us-gaap", {})
    rows = [x for tag in ("EarningsPerShareDiluted", "EarningsPerShareBasic") for x in facts.get(tag, {}).get("units", {}).get("USD/shares", [])]
    missing = [f for f in want if not any(x.get("end") == f[1] and x.get("accn") == f[3] for x in rows)]
    form, rep, filed, accn = want[0]
    if not missing:
        return "준비됨", f"{form} {rep}(접수 {filed}) 요약 자료에 있음" + (" — 최근 보고서 4개 모두" if code == "SEC" else "")
    m = missing[0]
    return "자료 대기", f"{m[0]} {m[1]}(접수 {m[2]}) 나왔지만 요약 자료에 없음" + (f" 외 {len(missing) - 1}건" if len(missing) > 1 else "")


def main():
    pick = set(sys.argv[1:])
    rows = [r for r in section_a() if not pick or r[0] in pick]
    ciks = {v["ticker"]: str(v["cik_str"]).zfill(10) for v in get("https://www.sec.gov/files/company_tickers.json").values()}
    out = []
    for t, code, when in rows:
        cik = ciks.get(t)
        if not cik:
            out.append((t, code, "확인 불가", "SEC 티커 목록에 없음(티커 변경?)"))
            continue
        try:
            st, note = check(cik, code)
        except Exception as e:  # 한 종목 실패로 전체를 멈추지 않는다
            st, note = "확인 불가", str(e)[:80]
        out.append((t, code, st, note))
        time.sleep(0.25)   # SEC 초당 10회 제한
    order = {"준비됨": 0, "자료 대기": 1, "대기": 2, "확인 불가": 3}
    print("| 카드 | 확인 | 상태 | 내용 |\n|---|---|---|---|")
    for t, code, st, note in sorted(out, key=lambda x: (order[x[2]], x[0])):
        print(f"| {t} | {code} | {st} | {note} |")
    print(f"\n준비됨 {sum(o[2] == '준비됨' for o in out)} / {len(out)}")


if __name__ == "__main__":
    main()
