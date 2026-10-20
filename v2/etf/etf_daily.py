#!/usr/bin/env python3
"""ETF 판정(etf-v1) — 보유 비중 가중으로 카드 판정을 합산한다(2026-10-19 사용자 결정, dr 5라운드 합의).

규칙의 기준은 v2/research/etf_verdict_prereg.md다. 이 파일은 그 규칙을 그대로 옮긴다 — 바꿀 때는 그 문서를 먼저 고친다.

    python3 v2/etf/etf_daily.py                 # SPY: 운용사 파일을 받아 계산하고 세 산출물을 쓴다
    python3 v2/etf/etf_daily.py --xlsx F.xlsx   # 받지 않고 그 파일로(검사·재현용)
    python3 v2/etf/etf_daily.py --out-root DIR  # 산출물을 DIR 아래에 쓴다(저장소를 건드리지 않는 검사용)

산출물(어떤 실패에서도 셋 다 쓰고 종료 코드 0 — 실패는 "판정 보류 + 사유"로 쓴다):
  v2/etf/SPY.json               계산 결과(공개). 운용사 원본 줄은 넣지 않는다 — 상위 10개 비중만(2026-10-19 사용자 결정,
                                운용사 고지 "may not be reproduced ... without SSGA's express written consent").
  preview-only-etf-spy.html     ETF 카드 페이지(preview 전용)
  preview-only-etf-data.js      홈 시장 지표 구역이 읽는 요약(window.ETF_DATA)
원본 xlsx와 줄 단위 계산은 v2/etf/.private/(커밋하지 않음)에만 남기고, 공개 쪽에는 xlsx sha256만 남긴다.
"""
import argparse
import hashlib
import html
import json
import math
import os
import re
import subprocess
import sys
import traceback
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ETF_DIR = ROOT / "v2" / "etf"
CFG_PATH = ETF_DIR / "ticker_alias.json"
TEMPLATE = ETF_DIR / "template" / "etf_template.html"

TIERS = ["저평가", "적정~저평가", "적정", "적정~고평가", "고평가"]
BAR_KEYS = TIERS + ["카드 없음", "판정 보류", "그 밖 제외", "분류 안 됨"]
COVER_MIN = 0.70          # 덮은 비중 문턱(사용자 결정)
UNCLASSIFIED_MAX = 0.005  # 분류 안 됨이 D의 0.5%를 넘으면 보류
LABEL_SHARE = 0.30        # 덮은 비중 부족일 때 날짜 불일치·추출 오류가 D의 30% 이상이면 그것을 대표 사유로
EDGE = 0.25               # 문턱 ±0.25 안이면 "경계 근처"(표시만)
LO, HI = -4.0, 3.0        # 카드 점수 범위(척도 [−4, +3])

# 보류 사유 — 닫힌 어휘(산출물의 reasonText로 홈·카드 페이지에 그대로 보인다). 순서가 대표 사유 우선순위다(규칙 9).
REASONS = {
    "run_fail": "ETF 스크립트 실행 실패",
    "fetch_fail": "보유 파일 받기 실패",
    "selfcheck": "자체 검사 불일치",
    "input": "입력 오류",
    "file_date": "보유 파일 날짜",
    "tools": "카드 판정 추출기 실패",
    "code_sig": "카드 판정 코드 변경 — 승인 필요",
    "structure": "카드 판정 구조 변경",
    "unclassified": "분류 안 됨",
    "extract": "카드 추출 오류",
    "date_mismatch": "카드 날짜 불일치",
    "coverage": "덮은 비중 부족",
}
# 카드 한 장의 제외 사유 — 여러 개면 이 순서의 첫 것이 대표(막대 칸을 정한다), 나머지도 기록한다.
CARD_EXCL = ["extract", "rule_mismatch", "date_mismatch", "held_card"]
CARD_EXCL_LABEL = {"extract": "추출 오류", "rule_mismatch": "규칙 불일치", "date_mismatch": "날짜 불일치", "held_card": "판정 보류"}
THIRD_NAMES = {"현금흐름", "초과이익"}


class Hold(Exception):
    """ETF 전체를 판정 보류로 끝내는 조건(규칙 1·3·5·7)."""
    def __init__(self, key, detail="", holds=None):
        super().__init__(detail)
        self.key, self.detail = key, detail
        self.holds = holds or [(key, detail)]   # 함께 모인 다른 보류 조건(규칙 9 — 대표는 우선순위로)


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def write_atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


# ── 보유 파일 ───────────────────────────────────────────────

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (stock-widgets-preview ETF)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        body = r.read()
    if not body.startswith(b"PK"):
        raise Hold("fetch_fail", f"xlsx가 아니다({len(body)}바이트)")
    return body


def read_xlsx(body):
    """첫 시트를 [[셀…]…]로. 표준 라이브러리만 쓴다(Actions에 openpyxl을 더 깔지 않게)."""
    import io
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
          "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}
    z = zipfile.ZipFile(io.BytesIO(body))
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
            shared.append("".join(t.text or "" for t in si.iter(f"{{{ns['m']}}}t")))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rid = wb.find("m:sheets/m:sheet", ns).get(f"{{{ns['r']}}}id")
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = next(x.get("Target") for x in rels if x.get("Id") == rid)
    sheet = ET.fromstring(z.read("xl/" + target.lstrip("/").removeprefix("xl/")))
    rows = []
    for row in sheet.iter(f"{{{ns['m']}}}row"):
        cells = {}
        for c in row.findall("m:c", ns):
            col = re.match(r"[A-Z]+", c.get("r")).group(0)
            idx = 0
            for ch in col:
                idx = idx * 26 + (ord(ch) - 64)
            t, v = c.get("t"), c.find("m:v", ns)
            if t == "s":
                val = shared[int(v.text)] if v is not None else None
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter(f"{{{ns['m']}}}t"))
            elif t in ("str", "b"):
                val = v.text if v is not None else None
            else:
                val = float(v.text) if v is not None and v.text not in (None, "") else None
            cells[idx - 1] = val
        r_i = int(row.get("r")) - 1
        while len(rows) < r_i:
            rows.append([])
        rows.append([cells.get(i) for i in range(max(cells) + 1)] if cells else [])
    return rows


def parse_holdings(rows, ctx=None):
    """규칙 1: 머리 줄·기준일을 찾고, 머리 줄 뒤 첫 빈 줄까지를 데이터 줄로 본다(그 뒤는 면책 문구)."""
    s_date = None
    for r in rows[:10]:
        if r and r[0] == "Holdings:" and len(r) > 1 and isinstance(r[1], str):
            m = re.fullmatch(r"As of (\d{1,2})-([A-Za-z]{3})-(\d{4})", r[1].strip())
            if m:
                s_date = datetime.strptime(f"{m[1]}-{m[2]}-{m[3]}", "%d-%b-%Y").strftime("%Y-%m-%d")
                if ctx is not None:
                    ctx["S"] = s_date   # 아래 입력 오류로 멈춰도 S는 기록한다(규칙 7)
    if not s_date:
        raise Hold("input", "기준일(As of) 줄을 못 찾음")
    hi = next((i for i, r in enumerate(rows) if r and "Ticker" in r and "Weight" in r and "Identifier" in r), None)
    if hi is None:
        raise Hold("input", "머리 줄(Ticker·Weight·Identifier)을 못 찾음")
    head = [str(c) if c is not None else "" for c in rows[hi]]
    col = {k: (head.index(k) if k in head else 10 ** 6) for k in ("Name", "Ticker", "Identifier", "Weight")}
    out = []
    for k_row, r in enumerate(rows[hi + 1:], 1):
        if not r or all(c is None or (isinstance(c, str) and not c.strip()) for c in r):
            break
        g = lambda k: r[col[k]] if col[k] < len(r) else None
        w = g("Weight")
        if not isinstance(w, float) or not math.isfinite(w) or w < 0:
            raise Hold("input", f"데이터 {k_row}번째 줄(티커 {str(g('Ticker') or '')[:8]})의 Weight가 0 이상의 수가 아니다")
        out.append({"name": str(g("Name") or "").strip(), "ticker": str(g("Ticker") or "").strip(),
                    "ident": str(g("Identifier") or "").strip(), "w_raw": w})
    if not out:
        raise Hold("input", "데이터 줄이 없다")
    ids = [x["ident"] for x in out if x["ident"] and x["ident"] != "-"]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        tick = sorted({x["ticker"] for x in out if x["ident"] in dup})[:5]
        raise Hold("input", f"같은 Identifier가 두 줄 이상인 묶음 {len(dup)}개(티커 {', '.join(tick)})")
    return s_date, out


# ── 카드 ────────────────────────────────────────────────────

def run_node(script):
    """추출기·서명 스크립트. 어떤 실패든(node 없음·시간 초과·비정상 종료·깨진 JSON) 'tools'로."""
    try:
        p = subprocess.run(["node", str(script)], capture_output=True, text=True, timeout=600)
        if p.returncode != 0:
            raise Hold("tools", f"{script.name} 종료 코드 {p.returncode}")
        out = json.loads(p.stdout)
        if not isinstance(out, dict):
            raise ValueError("사전이 아님")
        return out
    except Hold:
        raise
    except Exception as ex:
        raise Hold("tools", f"{script.name} {type(ex).__name__}")


def card_score(judges):
    """카드 JS와 같은 식(v2/newcards/template/NVDA_template.html '종합 평가 자동 판정')."""
    seated = [j for j in judges if j[1] is not None]
    maxw = sum(j[3] for j in seated)
    n = sum(j[1] for j in seated) * 4 / maxw if maxw else None
    if judges[2][1] is None or len(seated) < 2:
        return n, "판정 보류"
    m = n if n is not None else 0
    return n, ("저평가" if m >= 3 else "적정~저평가" if m >= 1 else "적정" if m > -1 else "적정~고평가" if m > -3 else "고평가")


def structure_ok(judges):
    """규칙 5 구조 서명: 심판 3명 [자기 이력, 동종업, 현금흐름|초과이익], 가중치 [1,1,2], 표 값 집합."""
    if not isinstance(judges, list) or len(judges) != 3:
        return False
    if not all(isinstance(j, list) and len(j) >= 4 and isinstance(j[0], str) for j in judges):
        return False
    names = [j[0] for j in judges]
    if names[:2] != ["자기 이력", "동종업"] or names[2] not in THIRD_NAMES:
        return False
    if [j[3] for j in judges] != [1, 1, 2]:
        return False
    return (judges[0][1] in (-1, 0, 1, None) and judges[1][1] in (-1, 0, 1, None)
            and judges[2][1] in (1, 0, -1, -2, None))


def tier_of(n):
    return "저평가" if n >= 3 else "적정~저평가" if n >= 1 else "적정" if n > -1 else "적정~고평가" if n > -3 else "고평가"


def prev_session(p, v2):
    """P 직전 거래 세션 — NVDA 카드 일봉 날짜를 거래일 달력으로 쓴다(대안 B 전용)."""
    h = (v2 / "NVDA_full_widget.html").read_text(encoding="utf-8")
    i = h.index("const NVDA_DAILY")
    dates = re.findall(r'\["(\d{4}-\d{2}-\d{2})"', h[i:h.index("];", i)])
    if p not in dates:
        raise Hold("file_date", f"달력(NVDA 일봉)에 P={p}가 없다")
    k = dates.index(p)
    return dates[k - 1] if k else None


# ── 계산 ────────────────────────────────────────────────────

def compute(etf, cfg, xlsx, P, v2, ctx):
    """규칙 1~11. 입력 오류(규칙 1)만 바로 멈추고, 나머지 보류 조건은 모두 모아 규칙 9 우선순위로 대표 하나를 고른다.
    ctx에는 파싱 직후 S를 넣는다(보류여도 S·P를 기록한다 — 규칙 7)."""
    fund = cfg["funds"][etf]
    S, rows = parse_holdings(read_xlsx(xlsx), ctx)
    holds = []   # (사유 키, 상세) — 상세에는 운용사 Identifier·비중을 넣지 않는다(공개된다)

    # 규칙 7 날짜
    ok_s = {P}
    if cfg.get("dateRule") == "prev_ok":
        ps = prev_session(P, v2)
        if ps:
            ok_s.add(ps)
    if S not in ok_s:
        holds.append(("file_date", f"보유 파일 기준일 {S} ≠ 허용 {sorted(ok_s)} (P={P}, 규칙 {cfg.get('dateRule')})"))

    try:
        verdicts = run_node(v2 / "research" / "extract_card_verdicts.js")
        sigs = run_node(v2 / "etf" / "verdict_code_sig.js")
    except Hold as h:   # 카드 없이는 더 셀 수 없다 — 지금까지 모은 조건과 함께 멈춘다
        raise Hold(h.key, h.detail, holds + [(h.key, h.detail)])
    nonq, comp_map, approved = cfg["nonEquity"], cfg["company"], cfg["approvedVerdictCode"]

    # 규칙 2 분류, 규칙 3 분모
    for x in rows:
        comp = comp_map.get(x["ticker"], x["ticker"])
        x["company"] = comp
        if x["ident"] in nonq:
            x["cls"] = "비주식"
        elif comp in verdicts:
            x["cls"] = "매핑"
        elif re.fullmatch(r"[A-Z][A-Z.]{0,6}", x["ticker"]) and x["ident"] and x["ident"] != "-":
            x["cls"] = "카드 없음"
        else:
            x["cls"] = "분류 안 됨"
    D = sum(x["w_raw"] for x in rows if x["cls"] != "비주식")
    if not D > 0:
        raise Hold("input", "분모 D가 0")
    for x in rows:
        x["w"] = x["w_raw"] / D if x["cls"] != "비주식" else None
    unclassified = sum(x["w"] for x in rows if x["cls"] == "분류 안 됨")
    if unclassified > UNCLASSIFIED_MAX:
        n_un = sum(1 for x in rows if x["cls"] == "분류 안 됨")
        holds.append(("unclassified", f"분류 안 됨 {n_un}줄, D의 {unclassified:.2%} > 0.5%"))

    # 규칙 4 회사 단위로 합침
    comps = {}
    for x in rows:
        if x["cls"] in ("매핑", "카드 없음"):
            c = comps.setdefault(x["company"], {"company": x["company"], "name": x["name"], "w": 0.0, "cls": x["cls"], "lines": []})
            c["w"] += x["w"]
            c["lines"].append(x["ticker"])

    # 규칙 5 서명 — 매핑된 카드 전부, 추출 성공 여부보다 먼저 → 규칙 4·6 카드별
    bad_sig, sig_err, bad_struct, cards = [], [], [], []
    for c in comps.values():
        if c["cls"] != "매핑":
            continue
        v = verdicts[c["company"]]
        sg = sigs.get(c["company"])
        if not isinstance(sg, str):
            sig_err.append(c["company"])        # 해시를 못 쟀다 — 카드 파일을 고칠 일(승인할 해시가 없다)
        elif sg not in approved:
            bad_sig.append(c["company"])
        rec = {"card": c["company"], "w": c["w"], "verdict": v.get("verdict"), "date": v.get("date"), "n": None, "excl": []}
        if "error" in v or not v.get("judges"):
            rec["excl"].append("extract")
        elif not structure_ok(v["judges"]):
            bad_struct.append(c["company"])
            rec["excl"].append("extract")
        else:
            n, again = card_score(v["judges"])
            rec["n"] = n
            if again != v.get("verdict"):
                rec["excl"].append("rule_mismatch")
            if not v.get("date"):
                rec["excl"].append("extract")
            elif v["date"] != P:
                rec["excl"].append("date_mismatch")
            if v.get("verdict") == "판정 보류":
                rec["excl"].append("held_card")
        rec["excl"] = [k for k in CARD_EXCL if k in rec["excl"]]
        cards.append(rec)
    if bad_sig or sig_err:
        parts = []
        if bad_sig:
            parts.append(f"승인 목록에 없는 판정 코드 해시 {len(bad_sig)}장: {', '.join(sorted(bad_sig)[:8])}")
        if sig_err:
            parts.append(f"판정 코드 서명을 못 잰 카드 {len(sig_err)}장(카드 파일 확인): {', '.join(sorted(sig_err)[:8])}")
        holds.append(("code_sig", " / ".join(parts)))
    if bad_struct:
        holds.append(("structure", f"구조 서명이 다른 카드 {len(bad_struct)}장: {', '.join(sorted(bad_struct)[:8])}"))

    used = [r for r in cards if not r["excl"]]
    c_cov = sum(r["w"] for r in used)
    bar = {k: 0.0 for k in BAR_KEYS}
    for r in cards:
        if not r["excl"]:
            bar[r["verdict"]] += r["w"]
        elif r["excl"][0] == "held_card":
            bar["판정 보류"] += r["w"]
        else:
            bar["그 밖 제외"] += r["w"]
    bar["카드 없음"] = sum(c["w"] for c in comps.values() if c["cls"] == "카드 없음")
    bar["분류 안 됨"] = unclassified
    share = {k: sum(r["w"] for r in cards if r["excl"] and r["excl"][0] == k) for k in ("extract", "date_mismatch")}

    nbar = sum(r["w"] * r["n"] for r in used) / c_cov if c_cov > 0 else None
    if c_cov < COVER_MIN:
        big = max(share, key=share.get)
        k = big if share[big] >= LABEL_SHARE else "coverage"
        holds.append((k, f"덮은 비중 {c_cov:.2%} < 70%"))
    order = list(REASONS)
    holds.sort(key=lambda h: order.index(h[0]))
    status = "held" if holds else "ok"
    reason = holds[0][0] if holds else None
    verdict = tier_of(nbar) if status == "ok" else None
    rng = [c_cov * nbar + (1 - c_cov) * LO, c_cov * nbar + (1 - c_cov) * HI] if status == "ok" else None
    edge = status == "ok" and min(abs(nbar - t) for t in (3, 1, -1, -3)) < EDGE

    top = sorted(comps.values(), key=lambda c: -c["w"])[:10]
    vmap = {r["card"]: r for r in cards}

    def pub_n(r):   # 공개 점수는 판정에 쓴 카드만(보류 카드는 +4가 나올 수 있다 — 범위 표기와 어긋나지 않게)
        return r["n"] if not r["excl"] else None
    top10 = [{"company": c["company"], "name": c["name"], "lines": c["lines"], "weight": c["w"],
              "card": c["company"] if c["cls"] == "매핑" else None,
              "verdict": vmap[c["company"]]["verdict"] if c["cls"] == "매핑" else None,
              "n": pub_n(vmap[c["company"]]) if c["cls"] == "매핑" else None,
              "excluded": [CARD_EXCL_LABEL[k] for k in vmap[c["company"]]["excl"]] if c["cls"] == "매핑" else []} for c in top]

    result = {
        "etf": etf, "name": fund["name"], "status": status, "reason": reason,
        "reasonText": REASONS[reason] if reason else None,
        "reasons": [{"key": k, "text": REASONS[k], "detail": d} for k, d in holds],
        "detail": holds[0][1] if holds else None,
        "verdict": verdict, "nbar": nbar if status == "ok" else None, "coverage": c_cov,
        "range": rng, "edgeNear": edge, "bar": bar, "top10": top10,
        "counts": {"lines": len(rows), "nonEquity": sum(1 for x in rows if x["cls"] == "비주식"),
                   "companies": len(comps), "cardsMatched": len(cards), "cardsUsed": len(used),
                   "cardsExcluded": {CARD_EXCL_LABEL[k]: sum(1 for r in cards if r["excl"] and r["excl"][0] == k) for k in CARD_EXCL}},
        "cards": [{"card": r["card"], "verdict": r["verdict"], "n": pub_n(r), "date": r["date"],
                   "excluded": [CARD_EXCL_LABEL[k] for k in r["excl"]]} for r in sorted(cards, key=lambda r: r["card"])],
        "S": S, "builtFor": P,
        "expense": {"pct": fund["expensePct"], "source": fund["expenseSource"], "url": fund["expenseUrl"]},
        "holdingsSource": fund["holdingsSource"],
    }
    private = {"rows": rows, "cards": cards, "D_raw": D, "nbar_raw": nbar}
    return result, private


def held(etf, cfg, key, detail, P, S=None, holds=None):
    hs = sorted(holds or [(key, detail)], key=lambda h: list(REASONS).index(h[0]))
    key, detail = hs[0]
    fund = cfg["funds"][etf] if cfg and etf in cfg.get("funds", {}) else {}
    return {"etf": etf, "name": fund.get("name", etf), "status": "held", "reason": key, "reasonText": REASONS[key],
            "detail": detail, "reasons": [{"key": k, "text": REASONS[k], "detail": d} for k, d in hs], "verdict": None, "nbar": None, "coverage": None, "range": None, "edgeNear": False,
            "bar": None, "top10": [], "counts": None, "cards": [], "S": S, "builtFor": P,
            "expense": ({"pct": fund["expensePct"], "source": fund["expenseSource"], "url": fund["expenseUrl"]} if fund else None),
            "holdingsSource": fund.get("holdingsSource")}


# ── 산출물 ──────────────────────────────────────────────────

CHECK_KEYS = ("status", "reason", "verdict", "nbar", "coverage", "range", "bar", "S", "builtFor", "ruleVersion")


def summary(res):
    """홈 요약 — 카드 페이지·SPY.json과 같은 값(자체 검사가 대조한다)."""
    keys = ("etf", "name", "status", "reason", "reasonText", "verdict", "nbar", "coverage", "range", "edgeNear",
            "bar", "S", "builtFor", "ruleVersion", "expense")
    s = {k: res.get(k) for k in keys}
    s["top"] = [{"company": t["company"], "weight": t["weight"], "verdict": t["verdict"], "card": t["card"]} for t in res.get("top10", [])[:5]]
    return s


def fmt_pct(x, d=1):
    return "—" if x is None else f"{x * 100:.{d}f}%"


def render_html(res):
    tpl = TEMPLATE.read_text(encoding="utf-8")
    ok = res["status"] == "ok"
    e = html.escape
    rows = []
    for t in res.get("top10", []):
        link = f'<a href="{e(t["card"])}_full_widget.html">{e(t["company"])}</a>' if t["card"] else e(t["company"])
        n_txt = "—" if t["n"] is None else format(t["n"], "+.2f").replace("-", "−")
        ex = [x for x in t.get("excluded", []) if x != t["verdict"]]
        if not t["card"]:
            vt = "카드 없음"
        elif ex:
            vt = f'{t["verdict"] or "—"} (제외: {", ".join(ex)})'
        else:
            vt = t["verdict"]
        rows.append(f'<tr><td>{link}</td><td>{e(t["name"])}</td><td class="num">{fmt_pct(t["weight"], 2)}</td>'
                    f'<td>{e(vt)}</td><td class="num">{n_txt}</td></tr>')
    bar = res.get("bar") or {}
    segs = "".join(f'<span class="seg seg-{i}" style="width:{bar.get(k, 0) * 100:.3f}%" title="{e(k)} {fmt_pct(bar.get(k))}"></span>'
                   for i, k in enumerate(BAR_KEYS) if bar.get(k))
    legend = "".join(f'<li><span class="sw seg-{i}"></span>{e(k)} <b class="num">{fmt_pct(bar.get(k))}</b></li>'
                     for i, k in enumerate(BAR_KEYS) if bar.get(k)) or "<li>—</li>"
    excl = res.get("counts", {}) or {}
    rng = res.get("range")
    val = {
        "ETF": e(res["etf"]), "NAME": e(res.get("name") or res["etf"]),
        "VERDICT": e(res["verdict"]) if ok else f'판정 보류 · {e(res["reasonText"])}',
        "NBAR": format(res["nbar"], "+.2f").replace("-", "−") if ok else "—",
        "COVERAGE": fmt_pct(res.get("coverage")),
        "RANGE": (format(rng[0], "+.2f") + " ~ " + format(rng[1], "+.2f")).replace("-", "−") if rng else "—",
        "EDGE": '<span class="edge">경계 근처</span>' if res.get("edgeNear") else "",
        "S": e(res.get("S") or "—"), "BUILTFOR": e(res.get("builtFor") or "—"),
        "EXPENSE": f'{res["expense"]["pct"]:.4f}%' if res.get("expense") else "—",
        "EXPENSE_SRC": e(res["expense"]["source"]) if res.get("expense") else "",
        "EXPENSE_URL": e(res["expense"]["url"]) if res.get("expense") else "#",
        "BAR": segs, "LEGEND": legend, "TOP10": "".join(rows) or '<tr><td colspan="5">—</td></tr>',
        "CARDS_USED": str(excl.get("cardsUsed", "—")), "CARDS_MATCHED": str(excl.get("cardsMatched", "—")),
        "DETAIL": e("; ".join(f'{r["text"]}: {r["detail"]}' for r in res.get("reasons", [])) or (res.get("detail") or "")),
        "SOURCE": e(res.get("holdingsSource") or ""),
        "RULE": e(res.get("ruleVersion") or ""),
        "DATA": e(json.dumps({k: res.get(k) for k in CHECK_KEYS}, ensure_ascii=False), quote=True),
        "STATUS": e(res["status"]),
    }
    return re.sub(r"\{\{([A-Z0-9_]+)\}\}", lambda m: val[m.group(1)], tpl)


DATA_PREFIX = "window.ETF_DATA = "


def read_data_js(path):
    """홈 데이터 파일의 ETF 요약 전부(다른 ETF 칸을 지우지 않게). 없거나 깨졌으면 빈 사전."""
    try:
        txt = path.read_text(encoding="utf-8")
        data = json.loads(txt[txt.index(DATA_PREFIX) + len(DATA_PREFIX):].rstrip().rstrip(";"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def write_outputs(res, out_root, etf):
    t = etf.lower()
    j = out_root / "v2" / "etf" / f"{etf}.json"
    h = out_root / f"preview-only-etf-{t}.html"
    d = out_root / "preview-only-etf-data.js"
    data = read_data_js(d)
    data[etf] = summary(res)
    write_atomic(j, json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    write_atomic(h, render_html(res))
    write_atomic(d, "// preview 전용 ETF 요약(v2/etf/etf_daily.py가 쓴다 — 손으로 고치지 않는다)\n"
                    f"{DATA_PREFIX}{json.dumps(data, ensure_ascii=False)};\n")
    return j, h, d


def selfcheck(res, private, paths):
    """규칙 12: 불변식 + 세 산출물이 같은 값인지. 문제 목록을 돌려준다(비면 통과)."""
    errs = []
    tol = 1e-9
    if res.get("bar") is not None and private:
        rows, cards = private["rows"], private["cards"]
        sw = sum(x["w"] for x in rows if x["w"] is not None)
        if abs(sw - 1) > tol: errs.append(f"Σw={sw}")
        if abs(sum(res["bar"].values()) - 1) > 1e-6: errs.append(f"막대 합 {sum(res['bar'].values())}")
        if not 0 <= res["coverage"] <= 1: errs.append("c 범위")
        used = [r for r in cards if not r["excl"]]
        if abs(sum(res["bar"][k] for k in TIERS) - res["coverage"]) > tol: errs.append("5등급 막대 합 ≠ c")
        if any(not (LO <= r["n"] <= HI) for r in used): errs.append("n 범위 밖")
    if res["status"] == "ok":
        lo, hi = res["range"]
        if not lo <= res["nbar"] <= hi: errs.append("범위가 n̄를 안 덮음")
        if res["coverage"] < COVER_MIN: errs.append("c<0.70인데 ok")
    errs += consistency(res, paths)
    return errs


def consistency(res, paths):
    j, h, d = paths
    try:
        a = json.loads(j.read_text(encoding="utf-8"))
        b = read_data_js(d).get(res["etf"], {})
        m = re.search(r'data-etf="([^"]*)"', h.read_text(encoding="utf-8"))
        c = json.loads(html.unescape(m.group(1))) if m else {}
    except Exception as ex:
        return [f"산출물 읽기 실패 {type(ex).__name__}"]
    return [f"산출물 불일치: {k}" for k in CHECK_KEYS if not (a.get(k) == res.get(k) == b.get(k) == c.get(k))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--etf", default="SPY")
    ap.add_argument("--xlsx", help="받지 않고 이 파일로")
    ap.add_argument("--out-root", default=str(ROOT))
    ap.add_argument("--v2", default=str(ROOT / "v2"), help="카드·추출기가 있는 v2 폴더(검사용 사본)")
    ap.add_argument("--stocks", default=str(ROOT / "site_data" / "stocks.json"))
    ap.add_argument("--private", default=os.environ.get("ETF_PRIVATE_DIR", str(ETF_DIR / ".private")))
    ap.add_argument("--cfg", default=str(CFG_PATH), help="설정 파일(검사용 사본)")
    a = ap.parse_args()
    etf, out_root, v2, pv = a.etf, Path(a.out_root), Path(a.v2), Path(a.private)
    run_at, fetched_at, cfg, P, xlsx = now_utc(), None, None, None, None
    ctx, inputs, private = {"S": None}, {}, None
    try:
        cfg = json.loads(Path(a.cfg).read_text(encoding="utf-8"))
        P = json.loads(Path(a.stocks).read_text(encoding="utf-8"))["priceSession"]
        try:
            xlsx = Path(a.xlsx).read_bytes() if a.xlsx else fetch(cfg["funds"][etf]["holdingsUrl"])
        except Hold:
            raise
        except Exception as ex:
            raise Hold("fetch_fail", type(ex).__name__)
        fetched_at = now_utc()
        inputs["xlsx"] = sha(xlsx)
        for k, p in (("alias", Path(a.cfg)), ("extractor", v2 / "research" / "extract_card_verdicts.js"),
                     ("sigScript", v2 / "etf" / "verdict_code_sig.js"), ("script", Path(__file__))):
            inputs[k] = sha(p.read_bytes())[:16]
        res, private = compute(etf, cfg, xlsx, P, v2, ctx)
    except Hold as h:
        res = held(etf, cfg, h.key, h.detail, P, ctx["S"], h.holds)
    except Exception as ex:
        # 공개 산출물·로그(공개 저장소 Actions)에는 예외 종류만 — 원본 값이 메시지에 섞일 수 있다. 전체는 비공개 폴더에.
        res = held(etf, cfg, "run_fail", type(ex).__name__, P, ctx["S"])
        pv.mkdir(parents=True, exist_ok=True)
        (pv / f"{etf}_traceback.txt").write_text(traceback.format_exc(), encoding="utf-8")
    meta = {"ruleVersion": (cfg or {}).get("ruleVersion"), "dateRule": (cfg or {}).get("dateRule"),
            "runAt": run_at, "fetchedAt": fetched_at, "inputHash": inputs}
    res.update(meta)
    paths = write_outputs(res, out_root, etf)
    errs = selfcheck(res, private, paths)
    if errs:
        prior = [(x["key"], x["detail"]) for x in res.get("reasons", [])]
        res = held(etf, cfg, "selfcheck", "; ".join(errs)[:300], P, ctx["S"], [("selfcheck", "; ".join(errs)[:300])] + prior)
        res.update(meta)
        paths = write_outputs(res, out_root, etf)
        left = consistency(res, paths)
        if left:   # 보류로 다시 쓴 셋도 어긋나면 손으로 볼 일 — 로그에 남긴다(홈은 형식 검사로 보류를 그린다)
            print("ETF_FAIL 자체 검사 재작성 뒤에도 불일치: " + "; ".join(left))
    if xlsx is not None:   # 원본과 줄 단위 계산은 비공개 폴더에만(커밋하지 않는다)
        pv.mkdir(parents=True, exist_ok=True)
        tag = ctx["S"] or "unknown"
        (pv / f"{etf}_{tag}.xlsx").write_bytes(xlsx)
        if private:
            write_atomic(pv / f"{etf}_{tag}_calc.json", json.dumps(private, ensure_ascii=False, indent=1))
    line = (f"ETF {etf}: {res['status']} " + (f"{res['verdict']} n̄={res['nbar']:+.3f} c={res['coverage']:.2%}"
            if res["status"] == "ok" else f"보류({res['reasonText']}) {res.get('detail') or ''}") + f" S={res.get('S')} P={P}")
    print(line if res["status"] == "ok" else "ETF_FAIL " + line)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(f"- {line}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
