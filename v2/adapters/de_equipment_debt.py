#!/usr/bin/env python3
"""DE 장비 부문 차입금 — 금융 부문(John Deere Financial) 빚을 뺀 차입금 시리즈를 10-Q·10-K 보충 표에서 뽑는다(2026-10-01).

CAT 결정(2026-09-30 사용자)과 같은 규칙: EV·내재가치 차입금은 장비 부문 빚만 쓴다. 금융 부문 차입금(2026-08-02 약 $54.5B)은
할부·리스 채권과 묶인 영업 부채이고 그 이자비용은 손익계산서 비용 안에 있다(DE는 영업이익 줄이 없어 세전이익을 영업이익으로 본다).

DE는 "SUPPLEMENTAL CONSOLIDATING DATA"(장비 · 금융 · 제거 · 연결) 표를 인라인 XBRL 태그 없이 싣는다. 그래서 원문 표의
장비 부문 첫 열(그 공시의 결산일)을 읽어 DE 전용 이름으로 `v2/.sec_cache/overlay/0000315189.json`에 쓴다.
매 행마다 장비 + 금융 + 제거 = 연결이 맞는지 확인하고, 안 맞으면 그 공시는 건너뛴다.

    python3 v2/adapters/de_equipment_debt.py
"""
import html
import json
import os
import re
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
CIK = "0000315189"
UA = "Su-san Kim gptjhss@gmail.com"
RAW = os.path.join(V2, ".sec_cache", "de_filings")
OUT = os.path.join(V2, ".sec_cache", "overlay", f"{CIK}.json")
ROWS = {"Short-term borrowings": "DeEquipShortTermBorrowings",
        "Short-term securitization borrowings": "DeEquipSecuritizationBorrowings",
        "Long-term borrowings": "DeEquipLongTermBorrowings"}
SINCE = "2021-01-01"


def get(url, path=None):
    if path and os.path.exists(path):
        return open(path, encoding="utf-8", errors="ignore").read()
    txt = subprocess.run(["curl", "-s", "-A", UA, url], capture_output=True, text=True).stdout
    time.sleep(0.2)
    if path:
        open(path, "w").write(txt)
    return txt


def text(h):
    h = re.sub(r"(?is)<(script|style).*?</\1>", "", h)
    h = re.sub(r"<[^>]+>", " ", h)
    h = html.unescape(h).replace("​", " ").replace("\xa0", " ")
    return re.sub(r"\s+", " ", h)


def num(s):
    s = s.strip()
    neg = s.startswith("(")
    v = float(s.strip("()").replace(",", ""))
    return -v if neg else v


def balance_block(t):
    """보충 표 가운데 재무상태표 부분(장비·금융·제거·연결 열)."""
    for m in re.finditer(r"SUPPLEMENTAL CONSOLIDATING DATA", t):
        seg = t[m.start():m.start() + 25000]
        if "BALANCE SHEET" in seg[:600].upper():
            return seg
    return None


def row(seg, label):
    """라벨 뒤 숫자 목록(괄호 음수·$ 무시). 다음 알파벳 라벨 전까지."""
    m = re.search(re.escape(label) + r"\s+((?:\$?\s*\(?[\d,]+\)?\s+)+)", seg)
    if not m:
        return None
    return [num(x) for x in re.findall(r"\(?[\d,]+\)?", m.group(1))]


def main():
    os.makedirs(RAW, exist_ok=True)
    sub = json.loads(get(f"https://data.sec.gov/submissions/CIK{CIK}.json"))["filings"]["recent"]
    data = json.load(open(OUT)) if os.path.exists(OUT) else {}
    out = data.setdefault("us-gaap", {})
    for tag in ROWS.values():
        out[tag] = []
    for form, acc, filed, doc, rep in zip(sub["form"], sub["accessionNumber"], sub["filingDate"], sub["primaryDocument"], sub["reportDate"]):
        if form not in ("10-Q", "10-K") or filed < SINCE:
            continue
        h = get(f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{acc.replace('-', '')}/{doc}", os.path.join(RAW, doc))
        seg = balance_block(text(h))
        if not seg:
            print("표 없음", form, filed, doc)
            continue
        ncol = 3 if form == "10-Q" else 2   # 10-Q는 결산일·직전 연말·1년 전, 10-K는 올해·작년
        vals = {}
        for label, tag in ROWS.items():
            r = row(seg, label)
            if not r:
                vals[tag] = 0.0   # 그 시기에 없던 줄(유동화 차입이 장비 부문에 없던 때)
                continue
            # 열 묶음: 장비 · 금융 · (제거) · 연결, 묶음마다 ncol개. 장비 칸이 빈 줄(장비 부문에 그 차입이 없던 때)은 금융 · 연결 두 묶음.
            # 장비 + 금융 + 제거 = 연결이 첫 열에서 맞아야 받는다.
            k = len(r) // ncol if len(r) % ncol == 0 else 0
            if k == 2 and r[0] == r[ncol]:
                vals[tag] = 0.0
            elif k == 3 and abs(r[0] + r[ncol] - r[2 * ncol]) < 0.5:
                vals[tag] = r[0]
            elif k == 4 and abs(r[0] + r[ncol] + r[2 * ncol] - r[3 * ncol]) < 0.5:
                vals[tag] = r[0]
            elif tag == "DeEquipSecuritizationBorrowings" and len(r) >= 2 * ncol and 0 <= r[-ncol] - r[-2 * ncol] < 100:
                # 유동화 차입 줄은 장비 칸이 일부만 차 있어(1, 1, 빈칸) 열 수가 어긋난다. 이 줄은 제거 열이 없어
                # 장비 = 연결 − 금융(첫 열)으로 구한다(2026-08-02 6,095 − 6,094 = 1).
                vals[tag] = r[-ncol] - r[-2 * ncol]
            else:
                vals[tag] = None
        if any(v is None for v in vals.values()):
            print("열 부족 — 건너뜀", form, filed, vals)
            continue
        for tag, v in vals.items():
            out[tag].append({"end": rep, "val": v * 1e6, "accn": acc, "fp": "FY" if form == "10-K" else "Q",
                             "form": form, "filed": filed, "unit": "USD", "src": "10-Q/10-K 보충 표 장비 부문 열(원문)"})
        print(form, filed, rep, {k[6:]: v for k, v in vals.items()})
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(data, open(OUT, "w"), indent=1)
    print("저장:", OUT)


if __name__ == "__main__":
    main()
