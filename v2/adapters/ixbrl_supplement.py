#!/usr/bin/env python3
"""companyfacts에 아직 안 들어온 최신 10-Q/10-K를 원문 인라인 XBRL에서 보충한다(2026-09-27, V).

SEC companyfacts는 가끔 최근 공시를 몇 달씩 싣지 않는다(JPM 카드의 C: 2026 10-Q 없음, V: 2026-07-29 10-Q 없음).
그 공시의 원문(인라인 XBRL)에서 **차원 없는** us-gaap·dei 수치만 꺼내 companyfacts 행 모양
({start?, end, val, accn, fy?, fp, form, filed})으로 `v2/.sec_cache/overlay/{cik}.json`에 더한다.
기존 오버레이의 다른 태그·행은 보존하고, 같은 (start, end, filed) 행은 다시 쓰지 않는다.

    python3 v2/adapters/ixbrl_supplement.py 0001403161
"""
import json
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from cover_shares import UA, get  # noqa: E402

CACHE = os.path.join(V2, ".sec_cache")


def facts_cache(cik):
    """companyfacts 캐시를 읽는다 — 없으면 받아서 저장한다. Actions의 SEC 캐시는 토요일에만 저장되므로 주중에 새로 만든 카드는
    캐시에 없고, 읽기만 하던 이 단계가 FileNotFoundError로 멈췄다(2026-10-26 매일 실행에서 CDNS 실패 — 10-25 추가된 카드)."""
    p = os.path.join(CACHE, f"{cik}_facts.json")
    if os.path.exists(p):
        try:
            return json.load(open(p))
        except ValueError:   # 토요일 캐시 저장이 중간에 끊겨 잘린 파일 — 없는 것으로 보고 받는다(Fable)
            pass
    try:
        d = json.loads(get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json") or "{}")
    except ValueError:   # 오류 쪽지(HTML·빈 응답)를 캐시에 쓰지 않는다
        d = {}
    if not isinstance(d, dict) or not isinstance(d.get("facts"), dict):   # null·오류 쪽지도 같은 문장으로(Codex)
        sys.exit(f"{cik}: companyfacts를 받지 못했고 캐시에도 없다 — 보충을 할 수 없다")
    os.makedirs(CACHE, exist_ok=True)
    tmp = p + ".part"   # 중간에 끊겨 반쪽 파일이 남으면 다음 실행이 받지 않고 그 파일로 멈춘다(Codex)
    json.dump(d, open(tmp, "w"))
    os.replace(tmp, p)
    return d


def parse(h, prefixes=("us-gaap:", "dei:")):
    ctx = {}
    for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', h, re.S):
        b = m.group(2)
        if "<xbrldi:explicitMember" in b or "<xbrldi:typedMember" in b:
            continue
        s, e, i = (re.search(rf"<xbrli:{k}>([^<]+)<", b) for k in ("startDate", "endDate", "instant"))
        ctx[m.group(1)] = (s.group(1), e.group(1)) if s and e else (None, i.group(1)) if i else None
    unit = {m.group(1): m.group(2) for m in re.finditer(r'<xbrli:unit id="([^"]+)">(.*?)</xbrli:unit>', h, re.S)}
    out = []
    for m in re.finditer(r'<ix:nonFraction([^>]*)>(.*?)</ix:nonFraction>', h, re.S):
        a = m.group(1)
        name = re.search(r'name="([^"]+)"', a).group(1)
        if not name.startswith(prefixes):
            continue
        c = ctx.get(re.search(r'contextRef="([^"]+)"', a).group(1))
        txt = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        if c and "fixed-zero" in a:
            txt = "0"                                   # ixt:fixed-zero("—")는 0이다(Codex)
        if not c or not re.match(r"^[\d,.]+$", txt):
            continue
        sc = re.search(r'scale="(-?\d+)"', a)
        v = float(txt.replace(",", "")) * 10 ** (int(sc.group(1)) if sc else 0)
        if 'sign="-"' in a:
            v = -v
        ub = unit.get((re.search(r'unitRef="([^"]+)"', a) or [None, ""])[1], "")
        u = "USD/shares" if "shares" in ub and "USD" in ub else "shares" if "shares" in ub else "USD" if "USD" in ub else "pure"
        out.append((name, c[0], c[1], v, u))
    return out


def fetch_doc(url, path):
    """공시 원문을 받아 **성공했을 때만** 캐시하고, 이 어댑터가 확인해 받은 파일만 다시 쓴다.

    공통 `cover_shares.get(url, path)`은 `curl -s`(−f 없음)의 출력을 성공 여부와 상관없이 캐시하고 다음 호출에 그대로
    돌려준다. 빈 응답·403·429 쪽지나 중간에 끊긴 본문이 한 번 박히면 다시 받을 길이 없어, build.py가 낡음을 보고 다시
    불러도 0행으로 끝난다(dr r1 Fable 필수). 본문에 `ix:nonFraction`이 있는지만 보면 끊긴 본문을 못 걸러내고(dr r2 Codex 필수),
    `</html>`로 끝나는 완결된 오류 페이지도 못 걸러낸다(dr r3 Codex 필수) — 게다가 이 원문 폴더(`ix_{cik}`)는 company_tag_feed·
    ixbrl_class_eps·dim_member_supplement도 공통 get으로 쓴다. 그래서 **내용으로 판정하지 않고** 이 어댑터가 종료 코드로
    확인해 받은 파일에만 `.ok` 표식을 두고, 표식 없는 파일은 출처를 알 수 없는 것으로 보아 지우고 다시 받는다.
    재시도는 curl 안의 `--retry`가 아니라 시도마다 따로 부른다 — 내부 재시도는 앞 시도의 부분 본문이 stdout에 남아
    성공 본문과 이어붙은 채 종료 코드 0으로 올 수 있다(dr r3 Codex 필수).
    """
    ok = path + ".ok"
    if os.path.exists(path) and os.path.exists(ok):
        return open(path, encoding="utf-8", errors="ignore").read()
    # 쌍이 맞지 않으면 둘 다 치운다 — 표식만 남은 채 원문을 다시 쓰다 끊기면, 그 표식이 반쪽 원문을 인증해 다음 실행이
    # 그대로 쓴다(dr r4 Codex 필수). 원문은 임시 이름에 쓰고 교체한 뒤에 표식을 만든다.
    for f in (path, ok):
        try:
            os.remove(f)
            print(f"원문 캐시와 표식이 맞지 않다 — 지우고 다시 받는다: {os.path.basename(f)}")
        except FileNotFoundError:
            pass
    # 시도 셋을 다 써도 최악 3×120초 + 대기 7.5초로, 카드 하나의 제한 시간(daily_price 900초)과 SEC 요청 속도 안에 둔다.
    # 가장 큰 원문이 20MB라 120초면 170KB/s 이상이면 되고, 넘기면 종료 코드 28로 끝나 캐시하지 않는다(dr r4 Codex 권장).
    for i, wait in ((1, 0.5), (2, 2), (3, 5)):
        r = subprocess.run(["curl", "-sS", "-f", "--max-time", "120", "-A", UA, url], capture_output=True, text=True)
        time.sleep(wait)
        if r.returncode == 0:
            tmp = f"{path}.{os.getpid()}.part"
            try:
                with open(tmp, "w") as f:
                    f.write(r.stdout)
                os.replace(tmp, path)
            except BaseException:
                try:
                    os.remove(tmp)
                except FileNotFoundError:
                    pass
                raise
            open(ok, "w").close()
            return r.stdout
        print(f"원문 받기 실패(curl {r.returncode}, {i}번째 시도) — 캐시하지 않는다: {url}"
              + (f" [{r.stderr.strip()[:200]}]" if r.stderr.strip() else ""))   # -sS가 이유를 stderr에 쓴다(403인지 시간 초과인지)
    return ""


def save(path, obj):
    """반쪽 파일을 남기지 않고 쓴다 — 이 파일들은 저장소에 커밋되므로(2026-10-29) 잘린 JSON이 올라가면 그 종목의 모든 실행이
    json.load에서 죽고, 저장소 판이 기준이라 캐시 복원으로도 벗어나지 못한다(dr r1 Codex·Fable 권장). facts_cache와 같은 꼴."""
    tmp = f"{path}.{os.getpid()}.part"   # 같은 폴더에 둔다(os.replace는 같은 파일시스템이어야 한다). .gitignore가 *.part를 뺀다
    try:
        with open(tmp, "w") as f:
            json.dump(obj, f, indent=1)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.remove(tmp)
        except FileNotFoundError:
            pass
        raise


def main(cik):
    cik = cik.zfill(10)
    facts = facts_cache(cik)
    have = {r["filed"] for t in facts["facts"].get("us-gaap", {}).values() for rows in t["units"].values() for r in rows}
    last = max(have)
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{cik}.json"))["filings"]["recent"]
    op = os.path.join(CACHE, "overlay", f"{cik}.json")
    data = json.load(open(op)) if os.path.exists(op) else {}
    raw = os.path.join(CACHE, f"ix_{cik}")
    os.makedirs(raw, exist_ok=True)
    added = 0
    for form, acc, filed, doc in zip(sub["form"], sub["accessionNumber"], sub["filingDate"], sub["primaryDocument"]):
        # 공시별로 본다 — companyfacts가 더 새 공시는 싣고 그 앞 공시를 빠뜨리면(SEC가 가끔 그런다) 마지막 날짜로 재면 그 앞
        # 공시를 건너뛰어 보충이 비고, _facts가 "승인한 공시가 SEC 자료에 없다"로 멈춘다. 2026-10-24~26 12개사 실측으로
        # 더 받게 되는 공시는 0건이었다(Fable)
        if form not in ("10-Q", "10-K") or filed in have:
            continue
        h = fetch_doc(f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}",
                      os.path.join(raw, doc))
        if "ix:nonFraction" not in h:
            # 받기 실패(빈 문자열)이거나, 인라인 XBRL 도입 전의 평문 HTML이다. 어느 쪽이든 이 공시는 보충할 수 없다 —
            # 받기 실패는 fetch_doc이 캐시하지 않으므로 다음 실행이 다시 받고, 승인 공시가 이 경우면 아래에서 표식을 남기지 않는다.
            print(f"{form} {filed} {doc}: 인라인 XBRL 사실이 없다({len(h)}바이트) — 건너뛴다")
            continue
        fp = "FY" if form == "10-K" else "Q"
        seen = set()
        for name, s, e, v, u in parse(h):
            tax, tag = name.split(":")
            key = (tag, s, e)
            if key in seen:
                continue
            seen.add(key)
            rows = data.setdefault(tax, {}).setdefault(tag, [])
            if any(r.get("start") == s and r["end"] == e and r["filed"] == filed for r in rows):
                continue
            row = {"end": e, "val": v, "accn": acc, "fp": fp, "form": form, "filed": filed, "unit": u, "src": "ixbrl"}
            if s:
                row["start"] = s
            rows.append(row)
            added += 1
        print(f"{form} {filed} {doc}: 보충 {len(seen)}개 사실")
    os.makedirs(os.path.dirname(op), exist_ok=True)
    save(op, data)
    print(f"저장: {op} (+{added}행, companyfacts 마지막 공시 {last})")
    # build.py가 "승인 공시는 더 채울 것이 없다"를 읽는 표식(dim_facts·회사 태그와 같은 .dimcheck.json의 "ixbrl" 키, 2026-10-29).
    # 보충을 저장소에 두기 시작하면서 build.py가 "승인 공시보다 낡은 보충"을 보면 다시 받게 했는데, 받을 것이 없는 종목까지
    # 매일 원문을 받게 되므로 한 번 훑은 사실을 남긴다. 채우지 못했는데 표식을 남기면(받기 실패·빈 응답) 조용히 빠진 채로
    # 굳으므로, 승인 공시가 companyfacts에 있거나 이번에 보충에 들어왔을 때, 또는 이 스크립트가 다룰 수 없는 서식(10-Q/A 등)일
    # 때만 남긴다 — 그 밖에는 표식 없이 두어 다음 실행이 다시 받고, 그때까지 카드는 _facts에서 멈춘다.
    appr = json.load(open(os.path.join(V2, "sec_approved.json"))).get(cik, "")
    if appr:
        forms = {fm for fm, f in zip(sub["form"], sub["filingDate"]) if f == appr}
        filled = appr in have or any(r.get("filed") == appr and r.get("src") == "ixbrl"
                                     for tags in data.values() for rows in tags.values() for r in rows)
        # 제출 목록에서 승인일 공시를 찾지 못했으면(목록 지연·기준표 날짜 오기입) "다룰 수 없는 서식"이 아니다 — 표식을 남기면
        # 재시도가 영구히 막힌다(dr r1 Codex 필수). 서식을 실제로 찾았고 그것이 10-Q·10-K가 아닐 때만 미지원으로 본다.
        unsupported = bool(forms) and not (forms & {"10-Q", "10-K"})
        if filled or unsupported:
            ck = os.path.join(CACHE, "overlay", f"{cik}.dimcheck.json")
            marks = json.load(open(ck)) if os.path.exists(ck) else {}
            marks["ixbrl"] = max(appr, marks.get("ixbrl", ""))
            save(ck, marks)
            print(f"표식: ixbrl {marks['ixbrl']}" + ("" if filled else f" (이 스크립트가 다루지 않는 서식 {sorted(forms)})"))
        else:
            why = f"{appr}를 채우지 못했다" if forms else f"{appr}가 제출 목록에 없다"
            print(f"표식 없음: 승인 공시 {why} — 다음 실행이 다시 받는다")


if __name__ == "__main__":
    main(sys.argv[1])
