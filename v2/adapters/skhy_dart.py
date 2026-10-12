#!/usr/bin/env python3
"""SK하이닉스 정기보고서를 OpenDART에서 받는다 — KRX KIND 화면 긁기를 대신한다(2026-10-12, 사용자가 OpenDART 키 발급).

KIND 원문(skhy_reports.py)과 같은 보고서를 OpenDART 원문 API(document.xml)로 받아, 지금 추출기(skhy_extract.py)가 읽는
HTML 모양으로 바꿔 저장한다(DART 표 칸 TE·TU → td). 2026 반기보고서는 KIND 원문 추출값과 모든 항목이 같았다.
- 분기·반기보고서: 본문 문서(연결재무제표·주석 포함)
- 사업보고서: 첨부 가운데 연결감사보고서(추출이 FY·누락 없음·결산일 일치하는 것). KIND는 3월 초 "감사보고서 제출"을 썼고,
  DART에는 그 첨부가 없어 3월 중순 사업보고서에서 같은 연결감사보고서를 꺼낸다(숫자는 같고 반영이 약 2주 늦다).
- 정정 보고서([기재정정] 등)는 KIND 때처럼 건너뛴다.
- 지역별 매출은 DART 원문 표 칸의 XBRL 태그(ACONTEXT·ACODE)로 읽는다 — regions().

키: 환경 변수 OPENDART_KEY(GitHub Secret) 또는 DART_API_KEY, 없으면 ~/.config/second-brain/api_keys.env의 DART_API_KEY(값은 출력하지 않는다).
"""
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPORTS = os.path.join(V2, ".sec_cache", "skhy_reports")
MANIFEST = os.path.join(HERE, "skhy_manifest.json")
CORP = "00164779"   # SK하이닉스 DART 고유번호
API = "https://opendart.fss.or.kr/api/"
VIEW = "https://dart.fss.or.kr/dsaf001/main.do?rcpNo="


def key():
    k = os.environ.get("OPENDART_KEY") or os.environ.get("DART_API_KEY")
    if not k:
        for p in ("~/.config/second-brain/api_keys.env", "~/.config/second-brain/bond_keys.env"):
            p = os.path.expanduser(p)
            if os.path.exists(p):
                m = re.search(r"^DART_API_KEY=(\S+)", open(p).read(), re.M)
                if m:
                    return m.group(1)
    return k


def _get(ep, raw=False, **p):
    p["crtfc_key"] = key()
    for i in range(4):
        try:
            b = urllib.request.urlopen(API + ep + "?" + urllib.parse.urlencode(p), timeout=180).read()
            time.sleep(0.2)
            return b if raw else json.loads(b)
        except Exception:
            if i == 3:
                raise
            time.sleep(3 + 5 * i)


def to_html(x):
    return re.sub(r"<(/?)T[EU]\b", lambda m: f"<{m.group(1)}TD", x)


def periodic(bgn, end):
    """정기보고서 목록(분기·반기·사업보고서, 정정 제외) — [(접수일, 접수번호, 보고서명)]."""
    out, page = [], 1
    while True:
        r = _get("list.json", corp_code=CORP, bgn_de=bgn.replace("-", ""), end_de=end.replace("-", ""), pblntf_ty="A", page_no=page, page_count=100)
        if r.get("status") not in ("000", "013"):
            raise RuntimeError(f"DART list: {r.get('status')} {r.get('message')}")
        for x in r.get("list", []):
            nm = x["report_nm"].strip()
            if nm.startswith("[") or not re.match(r"(분기|반기|사업)보고서", nm):
                continue
            out.append((x["rcept_dt"], x["rcept_no"], nm))
        if page >= int(r.get("total_page") or 1):
            break
        page += 1
    return sorted(out)


def earnings(bgn, end):
    """잠정실적 공정공시(연결 영업(잠정)실적) [(접수일 YYYY-MM-DD, 접수번호)] — 실적 발표일·보도 링크용."""
    out, page = [], 1
    while True:
        r = _get("list.json", corp_code=CORP, bgn_de=bgn.replace("-", ""), end_de=end.replace("-", ""), pblntf_ty="I", page_no=page, page_count=100)
        if r.get("status") not in ("000", "013"):
            raise RuntimeError(f"DART list: {r.get('status')} {r.get('message')}")
        out += [(f"{x['rcept_dt'][:4]}-{x['rcept_dt'][4:6]}-{x['rcept_dt'][6:]}", x["rcept_no"]) for x in r.get("list", [])
                if "잠정" in x["report_nm"] and "실적" in x["report_nm"] and not x["report_nm"].strip().startswith("[")]
        if page >= int(r.get("total_page") or 1):
            break
        page += 1
    return sorted(out)


def _period(nm):
    """'반기보고서 (2026.06)' → ('2026-06-30', 2) / 사업보고서 → 4."""
    y, mo = re.search(r"\((\d{4})\.(\d{2})\)", nm).groups()
    n = {"03": 1, "06": 2, "09": 3, "12": 4}[mo]
    return f"{y}-{mo}-{'31' if mo in ('03', '12') else '30'}", n


def fetch(rcept_no, nm):
    """원문을 받아 저장 → (추출용 파일, 본문 파일). 사업보고서는 첨부 연결감사보고서를 추출용으로 고른다."""
    sys.path.insert(0, HERE)
    from skhy_extract import extract
    z = zipfile.ZipFile(io.BytesIO(_get("document.xml", raw=True, rcept_no=rcept_no)))
    os.makedirs(REPORTS, exist_ok=True)
    end, n = _period(nm)
    files = {}
    for name in z.namelist():
        p = os.path.join(REPORTS, f"dart_{name.rsplit('.', 1)[0]}.htm")
        open(p, "w", encoding="utf-8").write(to_html(z.read(name).decode("utf-8", "ignore")))
        files[name] = p
    main = files.get(f"{rcept_no}.xml") or next(iter(files.values()))
    if n < 4:
        return main, main
    for name, p in files.items():   # 연결감사보고서 첨부 — 별도 감사보고서는 비지배지분·지배 순이익이 없어 누락으로 걸러진다
        if p == main:
            continue
        try:
            r = extract(p)
        except BaseException:
            continue
        if r["kind"] == "FY" and r["end"] == end and not r["missing"]:
            return p, main
    raise RuntimeError(f"{nm} {rcept_no}: 연결감사보고서 첨부를 찾지 못했다")


def fetch_new():
    """manifest의 마지막 정기보고서 뒤에 나온 정기보고서를 받아 manifest에 더한다 → 새로 더한 항목 목록."""
    man = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else []
    have_periods = set()
    sys.path.insert(0, HERE)
    last = max((m["filed"][:10] for m in man), default="2019-01-01")
    for m in man:
        if m.get("period"):
            have_periods.add(m["period"])
    import datetime as dt
    added = []
    for dte, rc, nm in periodic((dt.date.fromisoformat(last) - dt.timedelta(days=30)).isoformat(), dt.date.today().isoformat()):
        end, n = _period(nm)
        filed = f"{dte[:4]}-{dte[4:6]}-{dte[6:]}"
        if filed <= last or end in have_periods or any(m.get("acptno") == rc for m in man):
            continue
        f_extract, f_main = fetch(rc, nm)
        e = {"filed": filed, "acptno": rc, "title": nm, "kind": "annual" if n == 4 else "periodic", "source": "dart", "period": end,
             "url": VIEW + rc, "file": os.path.basename(f_extract), "file_main": os.path.basename(f_main)}
        man.append(e)
        added.append(e)
    man.sort(key=lambda m: m["filed"])
    json.dump(man, open(MANIFEST, "w"), ensure_ascii=False, indent=1)
    return added


def doc_for_period(end):
    """그 분기의 DART 본문(지역별 매출 태그용) — manifest에 없으면(KIND 시절 항목) 받아 둔다."""
    man = json.load(open(MANIFEST))
    m = next((m for m in man if m.get("source") == "dart" and m.get("period") == end and m.get("file_main")), None)
    if m:
        return os.path.join(REPORTS, m["file_main"])
    p = os.path.join(REPORTS, f"dart_main_{end}.htm")
    if os.path.exists(p):
        return p
    y = int(end[:4]) + (1 if end.endswith("12-31") else 0)
    for dte, rc, nm in periodic(f"{y}-01-01", f"{y}-12-31"):
        if _period(nm)[0] == end:
            z = zipfile.ZipFile(io.BytesIO(_get("document.xml", raw=True, rcept_no=rc)))
            open(p, "w", encoding="utf-8").write(to_html(z.read(f"{rc}.xml").decode("utf-8", "ignore")))
            return p
    raise RuntimeError(f"{end} 정기보고서가 DART 목록에 없다")


# 순서가 중요하다 — 사업보고서의 아시아 멤버 이름에 "CountryOfDomicile"이 들어 있다(AsiaOtherThanCountryOfDomicileAndChina…), 유럽도 회사 고유 이름
REGION = [(r"Asia", "아시아(중국 제외)"), (r"Europe", "유럽"), (r"_USMember|UnitedStates", "미국"), (r"_CNMember|China", "중국"),
          (r"CountryOfDomicile|Korea", "국내")]


def regions(path):
    """지역별 매출(백만 원) {문맥 코드: {지역: 값}} — 문맥 코드 예: 'CFY2026dHYQ'(이번 반기 3개월), 'PFY2025dHYA'(1년 전 누적), 'CFY2025dFY'(연간).
    연결 기준(ConsolidatedMember)·지역 축(GeographicalAreasAxis)만. 모르는 지역이 나오면 '기타'."""
    x = open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r'<TD[^>]*ACODE="ifrs-full_Revenue"[^>]*ACONTEXT="([^"]+)"[^>]*>([^<]*)<', x):
        ctx, txt = m.group(1), m.group(2).strip()
        if "ConsolidatedMember" not in ctx or "GeographicalAreasAxis" not in ctx:
            continue
        code = ctx.split("_", 1)[0]
        if not re.match(r"[CP]FY\d{4}d", code):
            continue
        mem = ctx.rsplit("GeographicalAreasAxis_", 1)[1]
        name = next((n for pat, n in REGION if re.search(pat, mem)), "기타")
        v = txt.replace(",", "")
        if not re.fullmatch(r"\(?-?\d+\)?", v):
            continue
        val = -float(v.strip("()")) if v.startswith("(") else float(v)
        d = out.setdefault(code, {})
        if name in d and d[name] != val:
            raise ValueError(f"{code} {name}: 값이 둘({d[name]}, {val})")
        d[name] = val
    return out


if __name__ == "__main__":
    for e in fetch_new():
        print("추가:", e["filed"], e["title"], e["acptno"], e["file"])
