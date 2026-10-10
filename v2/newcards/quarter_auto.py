#!/usr/bin/env python3
"""카드 분기 변수를 SEC 자료에서 정한다 — Claude 없이 매 분기 자동 갱신(설계 D 1단계, 2026-10-10).

카드 설정(cfg)의 CUR·YO·QO(분기 말), QLABEL·YL·QQL(분기 이름), L8(8분기 이름), TENQ·TENQ_NAME(보고서 링크),
FY_ENDS·FY_LABEL을 사람이 분기마다 고쳐 왔다. 여기서는 공시 기준표(v2/sec_approved.json)까지 접수된 자료만으로
같은 값을 만든다.

- 분기 말: 매출의 분기 값(build_multiple_history.quarterly_flow — 누계 차감, 4분기 = 연간 − 1~3분기)의 끝 날짜.
  CUR = 가장 최근, QO = 그 앞, YO = 1년 전 같은 분기(350~380일 앞).
- 회계연도: 10-K 연간 행의 끝 날짜(회계연도 말). 분기 번호 = 직전 회계연도 말 뒤로 몇 번째 분기인가.
  분기 행의 fy·fp는 쓰지 않는다 — 비교 수치는 그 행을 실은 공시의 fy·fp를 달고 있다(Codex 2026-10-10).
- 이름 꼴: 지금 cfg의 QLABEL 꼴을 따른다('Q2 2026' 또는 'Q3 FY26'). 회계연도 이름 = 회계연도 말이 속한 해.
- 보고서: SEC 제출 목록에서 그 분기 말(reportDate)의 10-Q·10-K(기준표 날짜까지 접수, 정정 제외).

    python3 v2/newcards/quarter_auto.py PEP              # 지금 기준표 날짜로
    python3 v2/newcards/quarter_auto.py PEP --cap 2026-10-08
    python3 v2/newcards/quarter_auto.py --check          # 카드 전부: 사람이 넣은 cfg 값과 대조
"""
import argparse
import datetime as dt
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, V2)
import build_multiple_history as bmh  # noqa: E402

feh = bmh.feh
UA = "kim research gptjhss@gmail.com"
FIELDS = ("CUR", "YO", "QO", "QLABEL", "YL", "QQL", "L8", "TENQ", "TENQ_NAME", "FY_ENDS", "FY_LABEL")


def cfg(T):
    sp = importlib.util.spec_from_file_location("cfg", os.path.join(HERE, "cfg", f"cfg_{T.lower()}.py"))
    C = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(C)
    return C


def d(s):
    return dt.date.fromisoformat(s)


def quarters(T, cik):
    """매출 분기 값의 끝 날짜들(오름차순)과 회계연도 말들."""
    _, rows = bmh.pick_tag(cik, bmh.FLOW_TAGS["revenue"])
    q = bmh.quarterly_flow(rows, T)
    ends = sorted(e["end"] for e in q)
    facts = bmh._facts(cik).get("facts", {}).get("us-gaap", {})
    fy_ends = set()
    for tag in bmh.FLOW_TAGS["revenue"]:
        for r in facts.get(tag, {}).get("units", {}).get("USD", []):
            if r.get("form", "").startswith("10-K") and "start" in r and 350 <= (d(r["end"]) - d(r["start"])).days <= 380:
                fy_ends.add(r["end"])
    return ends, sorted(fy_ends)


def fiscal(end, fy_ends):
    """분기 말 → (회계연도 말, 분기 번호). 다음 회계연도 말이 아직 없으면 직전 것 + 1년(±7일)로 본다."""
    e = d(end)
    past = [d(x) for x in fy_ends if d(x) < e]
    nxt = [d(x) for x in fy_ends if d(x) >= e]
    if nxt:
        fye = nxt[0]
        start = past[-1] if past else fye - dt.timedelta(days=364)
    elif past:
        # 새 회계연도의 10-K가 아직 없다 — 회계연도 말을 1년씩 밀되 시작점도 함께 민다(새 회계연도 1분기를 4분기로 세지 않게, Codex)
        fye = past[-1] + dt.timedelta(days=364)
        while fye < e - dt.timedelta(days=7):
            fye += dt.timedelta(days=364)
        start = fye - dt.timedelta(days=364)
    else:
        return None, None
    n = round((e - start).days / 91.3)   # 분기는 12~17주 — 몇 번째 분기인지 날 수로(16주 4분기도 4)
    n = max(1, min(4, n))
    if abs((fye - e).days) <= 7:
        n = 4
    return fye, n


def fy_year(fye):
    """회계연도의 기준 해 — 52·53주 회계연도는 말일이 12/31 또는 1/7처럼 해를 넘나든다. 1월 1~10일에 끝나면 전년으로 본다(Codex)."""
    return fye.year - 1 if fye.month == 1 and fye.day <= 10 else fye.year   # 1월 말 결산(CRM·WMT)은 그 해 그대로


def label(style, fye, n, off=0):
    y = fy_year(fye) + off
    return f"Q{n} FY{y % 100:02d}" if style == "fy" else f"Q{n} {y}"


def name_offset(C, fy_ends):
    """회사의 회계연도 이름 규칙 — 끝난 해(대부분) 또는 시작한 해(HD: 2026-02-01에 끝난 해가 FY2025). 카드의 지금 이름표에서 읽는다."""
    if hasattr(C, "FY_NAME_OFFSET"):   # 한 번 정해 cfg에 적어 두면 그 값을 쓴다 — 매번 이름표에서 다시 읽으면 한 번 틀린 이름이 굳는다(Codex)
        return C.FY_NAME_OFFSET
    fye, n = fiscal(C.CUR, fy_ends)
    m = re.search(r"(\d{4}|FY(\d\d))", C.QLABEL)
    if not fye or not m:
        return 0
    y = int(m.group(2)) + 2000 if m.group(2) else int(m.group(1))
    return y - fy_year(fye)


def filing(cik, end, cap):
    """그 분기 말의 10-Q·10-K(기준표 날짜까지 접수, 정정 제외)."""
    import urllib.request
    req = urllib.request.Request(f"https://data.sec.gov/submissions/CIK{str(cik).zfill(10)}.json", headers={"User-Agent": UA})
    r = json.loads(urllib.request.urlopen(req, timeout=30).read())["filings"]["recent"]
    for i, f in enumerate(r["form"]):
        if f in ("10-Q", "10-K") and r["reportDate"][i] == end and (not cap or r["filingDate"][i] <= cap):
            return f, f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{r['accessionNumber'][i].replace('-', '')}/{r['primaryDocument'][i]}"
    return None, None


def resolve(T, cap=None, net=True):
    orig = bmh._approved
    try:
        return _resolve(T, cap, net)
    finally:
        bmh._approved = orig   # 시험용 기준일이 같은 프로세스의 다른 계산으로 새지 않게(Codex)


def _resolve(T, cap, net):
    C = cfg(T)
    cik = str(C.CIK).zfill(10)
    if cap:
        base = bmh._approved
        bmh._approved = lambda: {**base(), cik: cap}
    cap = cap or bmh._approved().get(cik)
    ends, fy_ends = quarters(T, cik)
    # 결산월을 바꾼 회사(전환기 보고서)는 분기 번호를 잘못 셀 수 있다 — 멈추고 사람에게 넘긴다(Codex)
    for a_, b_ in zip(fy_ends, fy_ends[1:]):
        if not 350 <= (d(b_) - d(a_)).days <= 380 and d(b_) > d(ends[-9]) - dt.timedelta(days=400):
            raise SystemExit(f"{T}: 회계연도 말 간격이 1년이 아니다({a_} → {b_}) — 결산월 변경?")
    # 최근 9분기가 끊김 없이 이어져야 한다(분기 하나가 빠지면 L8이 건너뛴다, Codex)
    for a_, b_ in zip(ends[-9:], ends[-8:]):
        if not 75 <= (d(b_) - d(a_)).days <= 130:
            raise SystemExit(f"{T}: 분기 사이가 끊겼다({a_} → {b_})")
    if len(ends) < 9:
        raise SystemExit(f"{T}: 분기 값이 {len(ends)}개뿐이다")
    cur = ends[-1]
    qo = ends[-2]
    yo = [x for x in ends if 350 <= (d(cur) - d(x)).days <= 380]
    if not yo:
        raise SystemExit(f"{T}: 1년 전 같은 분기가 없다({cur})")
    yo = yo[-1]
    style = "fy" if "FY" in C.QLABEL else "cal"
    off = name_offset(C, fy_ends)
    lab = {}
    for e in ends[-9:] + [yo]:
        fye, n = fiscal(e, fy_ends)
        if not fye:
            raise SystemExit(f"{T}: 회계연도 말을 모른다")
        lab[e] = (label(style, fye, n, off), fye, n)
    out = {"CUR": cur, "YO": yo, "QO": qo, "QLABEL": lab[cur][0], "YL": lab[yo][0], "QQL": lab[qo][0],
           "L8": [lab[e][0] for e in ends[-8:]]}
    past_fye = [x for x in fy_ends if x <= cur]
    out["FY_ENDS"] = tuple(sorted(past_fye)[-2:][::-1]) if len(past_fye) >= 2 else None
    if past_fye:   # 카드가 쓰던 꼴을 따른다: 'FY2025' · 'FY25' · '2025년'
        y, old = fy_year(d(past_fye[-1])) + name_offset(C, fy_ends), str(getattr(C, "FY_LABEL", "") or "")
        out["FY_LABEL"] = (f"{y}년" if old.endswith("년") else f"FY{y % 100:02d}" if re.fullmatch(r"FY\d\d", old) else f"FY{y}")
    else:
        out["FY_LABEL"] = None
    if net:
        form, url = filing(cik, cur, cap)
        out["TENQ"] = url
        n = lab[cur][2]
        y = fy_year(lab[cur][1]) + off
        long_ = "FY20" in str(getattr(C, "TENQ_NAME", ""))   # 카드가 쓰던 꼴: 'FY2026' 또는 'FY26'
        fy = f"FY{y}" if long_ or style != "fy" else f"FY{y % 100:02d}"
        qn = lab[cur][0].replace(f"FY{y % 100:02d}", f"FY{y}") if long_ else lab[cur][0]
        out["TENQ_NAME"] = (f"{fy} 10-K" if form == "10-K" else f"{qn} 10-Q") if form else None
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--cap")
    ap.add_argument("--check", action="store_true", help="cfg에 사람이 넣은 값과 대조")
    a = ap.parse_args()
    tickers = [x.upper() for x in a.tickers] or sorted(f[4:-3].upper() for f in os.listdir(os.path.join(HERE, "cfg")) if f.startswith("cfg_"))
    bad = 0
    for T in tickers:
        if T in ("ASML", "TSM", "SKHY", "COF"):
            continue
        try:
            got = resolve(T, a.cap, net=a.check or True)
        except SystemExit as e:
            print(f"{T}: 실패 — {e}"); bad += 1; continue
        except Exception as e:
            print(f"{T}: 오류 {type(e).__name__} {e}"); bad += 1; continue
        if not a.check:
            print(T, json.dumps(got, ensure_ascii=False)); continue
        C = cfg(T)
        diff = []
        for k in FIELDS:
            want = getattr(C, k, None)
            if k == "FY_ENDS" and want is not None:
                want = tuple(want)
            if want is not None and got.get(k) != want:
                diff.append(f"{k}: cfg {want!r} / 자동 {got.get(k)!r}")
        if diff:
            bad += 1
            print(f"{T}: 다름 — " + " | ".join(diff))
        else:
            print(f"{T}: 같음")
    print(f"끝 — 어긋남 {bad}")


if __name__ == "__main__":
    main()
