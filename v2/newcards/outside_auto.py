#!/usr/bin/env python3
"""외국 발행사 자동 카드(ASML·TSM) — 10-Q 대신 6-K 원문에서 분기를 읽는다(2026-10-11, 사용자 결정: 15장도 자동으로).

ASML·TSM은 SEC에 10-Q를 내지 않는다. 재무는 어댑터(v2/adapters/asml_ifrs.py·tsm_ifrs.py)가 6-K 원문을
companyfacts 모양(현지 통화)으로 바꾼 파일을 쓴다. 이 파일은 자동 카드가 10-Q 대신 쓸 것을 모은다.

- refresh(T, s)     새 6-K 원문을 받아 어댑터 재무를 다시 만든다. 새 분기에 직전 분기에 있던 항목이 빠지면(라벨이 바뀌어
                    값이 조용히 0이 되는 것 — TSM 2026 Q2 유동성 장기부채 선례) 예전 파일로 되돌리고 멈춘다.
- report(T, end)    그 분기를 처음 실은 재무제표 6-K(주소·접수일·이름).
- seg(T, end, yo)   부문 매출 {이름: 백만 현지 통화} — ASML 시스템·서비스(분기 요약), TSM 공정별 웨이퍼 + 웨이퍼 외(연결재무제표 주석).
- release(T, after) 실적 보도자료 6-K(접수일, 주소) — ASML은 재무제표와 같은 6-K, TSM은 따로 먼저 낸다.
"""
import datetime as dt
import html as htmlmod
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
AD = os.path.join(V2, "adapters")
UA = "kim research gptjhss@gmail.com"
CIK = {"ASML": "0000937966", "TSM": "0001046179"}
SUBS = os.path.join(V2, ".sec_cache", "submissions")
d = dt.date.fromisoformat


def _manifest(T):
    return json.load(open(os.path.join(AD, f"{T.lower()}_manifest.json")))


def _reports_dir(T):
    return os.path.join(V2, ".sec_cache", f"{T.lower()}_reports")


def _url(T, m):
    if m.get("url"):
        return m["url"]
    return f"https://www.sec.gov/Archives/edgar/data/{int(CIK[T])}/{m['accn'].replace('-', '')}/{m['file'].split('_', 1)[1]}"


def _flat(path):
    t = htmlmod.unescape(re.sub(r"<[^>]+>", " ", open(path, encoding="utf-8", errors="ignore").read()))
    return re.sub(r"\s+", " ", t)


def report(T, end):
    """그 분기 말 뒤 처음 나온 재무제표 6-K(분기 말 뒤 120일 안). TSM 4분기는 연간 연결재무제표(2월 말)."""
    c = [m for m in _manifest(T) if 0 < (d(m["filed"]) - d(end)).days <= 120]
    if not c:
        return None
    m = sorted(c, key=lambda m: m["filed"])[0]
    return {**m, "url": _url(T, m), "path": os.path.join(_reports_dir(T), m["file"])}


# ── 부문 매출 ──
def _asml_seg(rep, end, yo):
    sys.path.insert(0, AD)
    import asml_extract as ax
    r = ax.extract(rep["path"])
    out = []
    for e in (end, yo):
        if e not in r:
            raise ValueError(f"ASML 분기 요약에 {e} 열이 없다")
        row = r[e]
        sysv, svc = row.get("Net system sales"), row.get("Net service and field option sales")
        if sysv is None or svc is None:
            raise ValueError(f"ASML {e}: 시스템·서비스 매출 줄을 못 찾았다")
        out.append({"노광 시스템": sysv, "설치 기반 관리 (서비스·업그레이드)": svc})
    return out


NODE = re.compile(r"((?:\d+(?:/\d+)?-nanometer(?:-0\.13 micron)?)|(?:0\.\d+(?:/0\.\d+)? micron(?: and above)?))"   # 연간 보고서는 0.11/0.13·0.15/0.18 micron으로 더 잘게 낸다
                  r"((?:\s+\$?\s*(?:\d[\d,]*(?![\d,/\-.])|-(?!\w)))+)")


def _bucket(label):
    n = re.match(r"(\d+)", label)
    if label.startswith("0."):   # 마이크론 공정
        return "16나노 이상"
    n = int(n.group(1)) if n else 999
    return "3·2나노" if n <= 3 else "5나노" if n == 5 else "7나노" if n == 7 else "16나노 이상"


def _tsm_tables(path):
    """연결재무제표 주석의 공정별(Resolution)·제품별(Product) 표 — 열마다 {구분: 천 대만달러}."""
    t = _flat(path)
    m = re.search(r"Resolution((?:\s+\d{4})+)(.*?)Wafer revenue", t)
    if not m:
        raise ValueError("TSM 공정별 매출 표를 못 찾았다")
    ncol = len(m.group(1).split())
    num = lambda s: 0.0 if s == "-" else float(s.replace(",", ""))
    cols = [{} for _ in range(ncol)]
    seen = 0
    for lab, vs in NODE.findall(m.group(2)):
        xs = [x for x in re.findall(r"\d[\d,]*|-", vs.replace("$", " "))]
        if len(xs) != ncol:
            raise ValueError(f"TSM 공정별 표 '{lab}' 열이 {len(xs)}개(머리 {ncol}개)")
        seen += 1
        for i, x in enumerate(xs):
            b = _bucket(lab)
            cols[i][b] = cols[i].get(b, 0.0) + num(x)
    if seen < 8:
        raise ValueError(f"TSM 공정별 표 줄이 {seen}개뿐이다")
    p = re.search(r"Product((?:\s+\d{4})+)\s+Wafer((?:\s+\$?\s*[\d,]+)+)\s+Others((?:\s+\$?\s*[\d,]+)+)", t)
    if not p:
        raise ValueError("TSM 제품별 매출 표를 못 찾았다")
    wafer = [num(x) for x in re.findall(r"[\d,]+", p.group(2))][:ncol]
    other = [num(x) for x in re.findall(r"[\d,]+", p.group(3))][:ncol]   # 뒤에 붙는 합계 줄은 버린다
    if len(wafer) != ncol or len(other) != ncol:
        raise ValueError("TSM 제품별 표 열 수가 공정별 표와 다르다")
    for i in range(ncol):
        if abs(sum(cols[i].values()) - wafer[i]) > 2:   # 공정별 합 = 웨이퍼 매출(천 대만달러, 반올림 2 안)
            raise ValueError(f"TSM 공정별 합 {sum(cols[i].values()):,.0f}이 웨이퍼 매출 {wafer[i]:,.0f}과 다르다(열 {i})")
        cols[i]["웨이퍼 외 매출"] = other[i]
    return cols


def _tsm_seg(T, rep, end, yo, q3_end):
    cols = _tsm_tables(rep["path"])
    if not q3_end:   # 1~3분기: 3개월(올해, 1년 전)이 앞 두 열(1분기는 두 열뿐, 2·3분기는 누계 두 열이 뒤에)
        if len(cols) not in (2, 4):
            raise ValueError(f"TSM 공정별 표 열이 {len(cols)}개")
        cur, old = cols[0], cols[1]
    elif len(cols) == 2:   # 4분기(q3_end를 준다): 연간(올해, 1년 전) − 3분기 보고서의 9개월 누계
        r3 = report(T, q3_end)
        c3 = _tsm_tables(r3["path"]) if r3 else None
        if not c3 or len(c3) != 4:
            raise ValueError("TSM 4분기: 3분기 연결재무제표의 9개월 누계가 없다")
        keys = set(cols[0]) | set(c3[2])
        cur = {k: cols[0].get(k, 0) - c3[2].get(k, 0) for k in keys}
        old = {k: cols[1].get(k, 0) - c3[3].get(k, 0) for k in keys}
    else:
        raise ValueError(f"TSM 공정별 표 열이 {len(cols)}개")
    return [{k: v / 1000 for k, v in x.items()} for x in (cur, old)]   # 천 → 백만 대만달러


def seg(T, end, yo, q3_end=None):
    rep = report(T, end)
    if not rep or not os.path.exists(rep["path"]):
        raise ValueError(f"{T}: {end} 재무제표 6-K 원문이 없다")
    if T == "ASML":
        return _asml_seg(rep, end, yo)
    return _tsm_seg(T, rep, end, yo, q3_end)


def dps(T, end):
    """TSM 분기 주당 현금배당(보통주 1주, 대만달러) — 연결재무제표 주석의 이사회 결의 표에서 가장 최근 분기(첫 열). 없으면 None."""
    rep = report(T, end)
    if T != "TSM" or not rep or not os.path.exists(rep["path"]):
        return None
    m = re.search(r"Cash dividends per share \(NT\$\)\s+\$?\s*([\d.]+)", _flat(rep["path"]))
    return float(m.group(1)) if m else None


# ── 실적 보도자료 ──
def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=30).read()


HEAD = {"ASML": re.compile(r"ASML reports .{0,80}?\bnet (sales|income)\b", re.I),   # 4분기는 "…net income in 2025"(분기 이름 없음)
        "TSM": re.compile(r"TSMC Reports (First|Second|Third|Fourth) Quarter", re.I)}


def _six_k_head(T, accn):
    """6-K 안에서 실적 보도자료 문서를 찾는다(접수번호마다 한 번 받아 둔다)."""
    os.makedirs(SUBS, exist_ok=True)
    p = os.path.join(SUBS, f"sixk_{accn}.json")
    if os.path.exists(p):
        return json.load(open(p))
    base = f"https://www.sec.gov/Archives/edgar/data/{int(CIK[T])}/{accn.replace('-', '')}/"
    items = json.loads(_get(base + "index.json"))["directory"]["item"]
    names = sorted([x["name"] for x in items if x["name"].lower().endswith((".htm", ".html")) and "index" not in x["name"]
             and int(x.get("size") or 0) < 1_500_000],   # 연결재무제표(큰 파일)는 보도자료가 아니다
                   key=lambda n: 0 if "press" in n.lower() else 1)   # ASML은 같은 6-K에 발표 자료(presentation)도 있다 — 보도자료 먼저
    found = {"url": None, "head": ""}
    for n in names[:6]:
        t = re.sub(r"\s+", " ", htmlmod.unescape(re.sub(r"<[^>]+>", " ", _get(base + n)[:60000].decode("utf-8", "ignore"))))[:800]
        time.sleep(0.12)
        if HEAD[T].search(t):
            found = {"url": base + n, "head": t[:400]}
            break
    json.dump(found, open(p, "w"))
    return found


def release(T, after, within=60, subs=None):
    """분기 말(after) 뒤 within일 안의 첫 실적 보도자료 6-K → (접수일, 주소) 또는 None."""
    r = subs
    if r is None:
        import auto_card as ac
        r = ac._submissions(CIK[T])
    c = sorted((r["filingDate"][i], r["accessionNumber"][i]) for i, f in enumerate(r["form"])
               if f == "6-K" and 0 < (d(r["filingDate"][i]) - d(after)).days <= within)
    for filed, accn in c:
        h = _six_k_head(T, accn)
        if h["url"]:
            return filed, h["url"]
    return None


# ── 새 분기 받기 ──
def _tags_at(facts, end):
    """그 날짜에 0이 아닌 값이 있는 태그(기간 끝 또는 시점) — 라벨이 바뀌면 추출기가 0을 넣는다(TSM need=False, Codex)."""
    out = set()
    for tag, x in facts["facts"].get("us-gaap", {}).items():
        for rows in x.get("units", {}).values():
            if any(r_.get("end") == end and r_.get("val") for r_ in rows):
                out.add(tag)
    return out


def _ends(facts):
    """매출이 있는 분기 말 — 3개월 행, 그리고 연간 행의 끝(TSM 4분기는 연간 누계로만 있다, Codex)."""
    rows = []
    for tag in ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"):
        for rs in facts["facts"].get("us-gaap", {}).get(tag, {}).get("units", {}).values():
            rows += [r_["end"] for r_ in rs if r_.get("start") and (80 <= (d(r_["end"]) - d(r_["start"])).days <= 100
                                                                    or 350 <= (d(r_["end"]) - d(r_["start"])).days <= 380)]
    return sorted(set(rows))


def _asml_fetch():
    """새 6-K(마지막 manifest 날짜 뒤)에서 US GAAP 요약 재무제표 첨부만 받는다 — asml_reports.py는 2020년부터 모든 6-K 목록을
    매번 다시 훑어 매일 실행에는 무겁다."""
    man_p = os.path.join(AD, "asml_manifest.json")
    man = json.load(open(man_p))
    last = max(m["filed"] for m in man)
    r = json.loads(_get(f"https://data.sec.gov/submissions/CIK{CIK['ASML']}.json"))["filings"]["recent"]
    for i, f in enumerate(r["form"]):
        filed, acc = r["filingDate"][i], r["accessionNumber"][i]
        if f != "6-K" or filed <= last or any(m["accn"] == acc for m in man):
            continue
        base = f"https://www.sec.gov/Archives/edgar/data/{int(CIK['ASML'])}/{acc.replace('-', '')}/"
        names = [x["name"] for x in json.loads(_get(base + "index.json"))["directory"]["item"] if x["name"].lower().endswith(".htm")]
        cand = [n for n in names if "usgaa" in n.lower() or ("financialstatements" in n.lower() and "ifrs" not in n.lower())]
        time.sleep(0.15)
        if not cand:
            continue
        os.makedirs(_reports_dir("ASML"), exist_ok=True)
        data = _get(base + cand[0])
        open(os.path.join(_reports_dir("ASML"), f"{filed}_{cand[0]}"), "wb").write(data)
        man.append({"filed": filed, "accepted": r["acceptanceDateTime"][i], "accn": acc, "file": f"{filed}_{cand[0]}"})
    man.sort(key=lambda m: m["filed"])
    json.dump(man, open(man_p, "w"), indent=1)


def _paths(T):
    return [os.path.join(V2, ".sec_cache", f"{CIK[T]}_facts.json"), os.path.join(AD, f"{T.lower()}_manifest.json")]


def commit(T):
    """카드가 새 분기로 만들어졌다 — 예전 파일(.bak)을 지운다."""
    for p in _paths(T):
        if os.path.exists(p + ".bak"):
            os.remove(p + ".bak")


def revert(T):
    """카드가 실패했다 — 어댑터 재무를 예전 것으로(카드는 attempt가 이미 되돌렸다)."""
    for p in _paths(T):
        if os.path.exists(p + ".bak"):
            shutil.move(p + ".bak", p)


def ensure(T):
    """커밋된 manifest와 어댑터 재무(.sec_cache)를 맞춘다 — Actions 캐시는 토요일에만 저장돼, 평일에 받은 새 6-K가
    다음 실행에서 캐시에 없을 수 있다. 원문이 없으면 받고, 재무가 manifest보다 오래면 다시 만든다. 반환: 다시 만들었는가."""
    man = _manifest(T)
    os.makedirs(_reports_dir(T), exist_ok=True)
    got = False
    for m in man:
        p = os.path.join(_reports_dir(T), m["file"])
        if not os.path.exists(p) or not os.path.getsize(p):
            data = _get(_url(T, m))   # 받은 뒤에 쓴다 — 실패하면 빈 파일이 남아 다음 실행이 받지 않았다(Codex)
            open(p, "wb").write(data)
            time.sleep(0.15)
            got = True
    fp = _paths(T)[0]
    have = 0
    if os.path.exists(fp):
        f = json.load(open(fp))
        have = max((r_.get("filed", "") for x in f["facts"].get("us-gaap", {}).values() for rs in x.get("units", {}).values() for r_ in rs), default="")
    # 재무가 manifest보다 새것이어도(새 분기를 만든 뒤 커밋·push가 실패하고 캐시만 저장된 경우) 다시 만든다(Codex)
    if got or not os.path.exists(fp) or have != max(m["filed"] for m in man):
        subprocess.run([sys.executable, os.path.join(AD, f"{T.lower()}_ifrs.py")], check=True, capture_output=True, timeout=900)
        return True
    return False


def latest_end(T):
    return _ends(json.load(open(_paths(T)[0])))[-1]


def refresh(T, session):
    """새 6-K 원문을 받아 어댑터 재무를 다시 만든다 → (새 분기 말 또는 None, 메시지).
    접수일이 오늘 세션 이후인 원문은 아직 쓰지 않는다(첫 종가 뒤에 반영 — 10-Q 카드와 같은 규칙).
    새 분기에 직전 분기에 있던 항목이 빠졌으면 예전 파일로 되돌린다."""
    t = T.lower()
    facts_p = os.path.join(V2, ".sec_cache", f"{CIK[T]}_facts.json")
    man_p = os.path.join(AD, f"{t}_manifest.json")
    bak = {p: p + ".bak" for p in (facts_p, man_p)}
    for p, b in bak.items():
        shutil.copy(p, b)
    old_ends = _ends(json.load(open(facts_p)))
    try:
        if T == "ASML":
            _asml_fetch()
        else:
            subprocess.run([sys.executable, os.path.join(AD, "tsm_ifrs.py"), "--refresh"], check=True, capture_output=True, timeout=900)
            # tsm_ifrs.py --refresh는 재무까지 만든다 — 접수일 검사 뒤 다시 만든다
        man = json.load(open(man_p))
        late = [m for m in man if m["filed"] >= session and m not in json.load(open(bak[man_p]))]
        if late:   # 첫 종가 전 — 원문은 다음 실행에서 쓴다
            json.dump([m for m in man if m not in late], open(man_p, "w"), indent=1)
        subprocess.run([sys.executable, os.path.join(AD, f"{t}_ifrs.py")], check=True, capture_output=True, timeout=900)
        f = json.load(open(facts_p))
        ends = _ends(f)
        new = [e for e in ends if e not in old_ends and (not old_ends or e > old_ends[-1])]
        if not new:
            for p, b in bak.items():
                shutil.move(b, p)
            return None, ("첫 종가 전 원문 대기" if late else "")
        cur = new[-1]
        # 1년 전 같은 분기와 견준다 — 직전 분기와 견주면 반기·연말에만 공시하는 항목(ASML 유동 차입금)이 정상 분기에서 걸린다(Codex)
        prev = [e for e in ends if 350 <= (d(cur) - d(e)).days <= 380]
        if not prev:
            raise ValueError(f"새 분기 {cur}의 1년 전 같은 분기가 어댑터 재무에 없다")
        miss = sorted(_tags_at(f, prev[-1]) - _tags_at(f, cur))
        if miss:
            raise ValueError(f"새 분기 {cur}에 1년 전 같은 분기({prev[-1]})에 있던 항목이 없거나 0이다: {miss} — 원문 라벨이 바뀌었을 수 있다")
        return cur, f"새 분기 {cur}"   # 예전 파일(.bak)은 카드가 끝난 뒤 commit·revert가 정리한다
    except Exception as e:
        for p, b in bak.items():
            if os.path.exists(b):
                shutil.move(b, p)
        msg = e.stderr.decode("utf-8", "ignore")[-300:] if isinstance(e, subprocess.CalledProcessError) and e.stderr else str(e)
        raise RuntimeError(f"{T}: 6-K 재무 갱신 실패 — {msg}") from None


if __name__ == "__main__":
    import quarter_auto as qa
    for T in sys.argv[1:] or ["ASML", "TSM"]:
        r = qa.resolve(T, net=False)
        rep = report(T, r["CUR"])
        print(T, r["CUR"], rep and rep["url"])
        fye, n = qa.fiscal(r["CUR"], qa.quarters(T, CIK[T])[1])
        ends = qa.quarters(T, CIK[T])[0]
        cur, old = seg(T, r["CUR"], r["YO"], ends[ends.index(r["CUR"]) - 1])
        print(" seg", {k: round(v) for k, v in cur.items()}, "| yo", {k: round(v) for k, v in old.items()})
        print(" release", release(T, r["CUR"]))
