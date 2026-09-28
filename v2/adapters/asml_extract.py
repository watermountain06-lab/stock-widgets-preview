#!/usr/bin/env python3
"""ASML 분기 US GAAP 첨부에서 "Quarterly Summary"(최근 5개 분기) 손익·재무상태·현금흐름을 꺼낸다.

원문은 표가 아니라 위치 지정 텍스트라 태그를 걷어 낸 뒤 "날짜 5개 머리 + (라벨 + 값 5개) 줄"을 읽는다.
    extract(path) → {"IS": {분기말: {라벨: 값}}, "BS": …, "CF": …}  (백만 유로, 주당 값은 유로)
"""
import html as H
import re
import sys
from datetime import datetime

MON = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?"
NUM = r"(?:\(?-?[\d,]+(?:\.\d+)?\)?%?|—|-)"


def flat(path):
    h = open(path, encoding="utf-8", errors="ignore").read()
    t = H.unescape(re.sub(r"<[^>]+>", " ", h))
    t = re.sub(r"\s+", " ", t)
    return re.sub(r"\(\s*([\d,.]+)\s*\)", r"(\1)", t)  # 2020년 초 파일은 "(1,301.1 )"처럼 괄호 안에 공백


def val(s):
    s = s.replace(",", "").replace("%", "")
    if s in ("—", "-"):
        return 0.0
    neg = s.startswith("(")
    v = float(s.strip("()"))
    return -v if neg else v


HEAD = re.compile(rf"((?:{MON} \d{{1,2}}, ?){{5}})\s*(\([^)]*\))?\s*((?:\d{{4}} ){{4}}\d{{4}})")
ROW = re.compile(rf"([A-Za-z][A-Za-z ,’'()&/\-:]*?[A-Za-z):])\s+({NUM}(?:\s+{NUM}){{4}})(?=\s+[A-Za-z|]|\s*$)")


def quarter_ends(t):
    """문서의 5분기 머리는 파일마다 한 종류뿐이다(27개 파일 확인) — 그 날짜 5개."""
    tuples = {}
    for m in HEAD.finditer(t):
        dates = re.findall(rf"({MON}) (\d{{1,2}})", m.group(1))
        ends = tuple(datetime.strptime(f"{mo[:3]} {d} {y}", "%b %d %Y").date().isoformat()
                     for (mo, d), y in zip(dates, m.group(3).split()))
        tuples[ends] = tuples.get(ends, 0) + 1
    if len(tuples) != 1:
        raise ValueError(f"5분기 머리가 한 종류가 아님: {tuples}")
    return list(tuples)[0]


def extract(path):
    """{분기말: {라벨: 값}} — 값 5개가 이어진 줄만 읽는다(2열·4열 비교표는 저절로 빠진다).
    머리가 표 앞에 오기도 뒤에 오기도 해서(2026년 현금흐름) 블록으로 자르지 않고 문서 전체를 읽는다.
    라벨 앞에 목차·머리 글자가 붙을 수 있으니 찾을 때는 get()으로 끝부분을 맞춘다."""
    t = flat(path)
    ends = quarter_ends(HEAD.sub(" ", t) and t)
    body = HEAD.sub(" | ", t)
    res = {e: {} for e in ends}
    for r in ROW.finditer(body):
        label = r.group(1).strip()
        vals = [val(v) for v in r.group(2).split()]
        for e, v in zip(ends, vals):
            res[e].setdefault(label, v)
    return res


def ytd_eps(path):
    """본문 손익계산서(3개월 2열 + 누적 2열)의 **누적** 주당순이익 {"basic": …, "diluted": …}.
    1분기 보고서는 2열뿐이라 None. 분기 EPS를 더하면 주식 수 변화 때문에 1~3센트 어긋난다(Codex: 2025년 합 24.72 대 실제 24.71).
    라벨 뒤 각주 번호(2020년 "Diluted … 3 1.86")를 건너뛴다."""
    t = flat(path)
    out = {}
    for key, lab in (("basic", "Basic"), ("diluted", "Diluted")):
        m = re.search(lab + r" net income per ordinary share(?: \d)?((?: \d+\.\d\d){2,5})", t)
        vals = m.group(1).split() if m else []
        if len(vals) != 4:
            return None
        out[key] = float(vals[-1])
    return out


def get(rows, name, default=None):
    """라벨 끝부분이 name과 같은 첫 값."""
    if name in rows:
        return rows[name]
    for k, v in rows.items():
        if k.endswith(" " + name):
            return v
    return default


if __name__ == "__main__":
    r = extract(sys.argv[1])
    last = max(r)
    print(sorted(r))
    for k, v in r[last].items():
        print(f"  {v:>12,.1f}  {k[-90:]}")
