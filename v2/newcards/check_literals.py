#!/usr/bin/env python3
"""cfg 문장에 숫자로 박힌 계산값을 찾는다(안건 E26, 2026-10-05).

생성기(fill.py)는 cfg 문장 안의 {표현식}을 그때 데이터로 채운다. 그런데 틀 통일로 옮긴 cfg에는 옛 카드 문장이 그대로 들어가
배수·백분위·점수·현금흐름 값·현재가 같은 계산값이 숫자로 적힌 곳이 많다 — 지금 카드에서는 맞지만 새 자료로 다시 만들면
그 문장만 옛 값으로 남는다. 이 스크립트는 cfg의 문자열 상수에서 {…} 밖의 숫자를 뽑아, 지금 카드 데이터 블록의 계산값과
같은 자리 수로 맞는 것을 알린다(같으면 표현식으로 바꿔야 할 후보). 카드 파일은 읽기만 한다.

    python3 v2/newcards/check_literals.py            # 전 cfg 요약
    python3 v2/newcards/check_literals.py AAPL MSFT  # 자세히(문장 속 위치)

한계: 우연히 같은 숫자(예: 연도·분기 수)도 걸릴 수 있다 — 2자리 이하 정수는 빼고, 소수·%·$·배가 붙은 숫자만 본다.
보도자료 숫자(분기 매출 등)는 카드 데이터 블록에 없으므로 걸리지 않는다(그건 분기마다 손으로 고치는 값이다).
"""
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
NUM = re.compile(r"(\$)?(−|-)?(\d+(?:,\d{3})*(?:\.\d+)?)(%p|%|배)?")


def card_values(T):
    """단위별 계산값 — '$'(현재가·내재가치), '배'(배수·현재가÷기본), '%'(백분위·요구율·현재가 대비), ''(점수)."""
    h = open(os.path.join(V2, f"{T}_full_widget.html"), encoding="utf-8").read()
    dec = json.JSONDecoder()

    def blk(name):
        k = f"const {T}_{name} = "
        return dec.raw_decode(h, h.index(k) + len(k))[0] if k in h else None
    vals = {"$": {}, "배": {}, "%": {}, "": {}}
    V = blk("VALUATION")
    if V:
        for side in ("self", "peer"):
            if V[side].get("score") is not None:
                vals[""][f"{side}.score"] = V[side]["score"]
            for m in V[side].get("metrics", []):
                for f in ("current", "median", "min", "max"):
                    if isinstance(m.get(f), (int, float)):
                        vals["배"][f"{side}.{m['metric']}.{f}"] = m[f]
                if isinstance(m.get("percentile"), (int, float)):
                    vals["%"][f"{side}.{m['metric']}.pct"] = m["percentile"]
                    vals["%"][f"{side}.{m['metric']}.top"] = 100 - m["percentile"]
                if isinstance(m.get("score"), (int, float)):
                    vals[""][f"{side}.{m['metric']}.score"] = m["score"]
    D = blk("DCF")
    daily = re.search(rf"const {T}_DAILY\s*=\s*(\[.*?\]);", h, re.S)
    px = json.loads(daily.group(1))[-1][4] if daily else None
    if px:
        vals["$"]["price"] = px
    if D:
        for f in ("low", "base", "high", "nonopPerShare"):
            if isinstance(D.get(f), (int, float)):
                vals["$"][f"dcf.{f}"] = D[f]
                if px and D[f] > 0:
                    vals["%"][f"dcf.{f}/price"] = D[f] / px * 100
        for f in ("requiredGrowth", "requiredMargin", "marginNow", "growth5y", "baseEquivGrowth"):
            if isinstance(D.get(f), (int, float)):
                vals["%"][f"dcf.{f}"] = D[f] * 100
        if px and isinstance(D.get("base"), (int, float)) and D["base"] > 0:
            vals["배"]["price/base"] = px / D["base"]
    return vals


def forms(v):
    """계산값이 문장에 적힐 만한 모양들(반올림 0·1·2자리)."""
    out = set()
    for nd in (0, 1, 2):
        s = f"{abs(v):,.{nd}f}"
        out.add(s)
        out.add(s.replace(",", ""))
    return out


def literals(text):
    text = re.sub(r"\{[^{}]*\}", " ", text)          # f-string 표현식은 뺀다
    text = re.sub(r"https?://\S+", " ", text)
    for m in NUM.finditer(text):
        num, unit = m.group(3), m.group(4) or ""
        after = text[m.end():m.end() + 1]
        if m.group(1):
            if after in "BMK조억":                         # $9.4B 같은 금액은 계산값이 아니다
                continue
            unit = "$"
        elif unit == "%p":
            continue
        elif not unit and "." not in num:
            continue                                    # 맨 정수(연도·개수)는 잡음
        if unit == "%" and num in ("2.5", "10"):
            continue                                    # 영구성장률 2.5%·할인율 10%는 모델 상수다
        near = text[max(0, m.start() - 30):m.start()]
        if unit == "%" and not re.search(r"상위|하위|백분위|현재가|요구|내재가치|영업이익률|이력|성장률", near):
            continue                                    # 가이던스·부문 증감 같은 보도자료 %는 계산값이 아니다
        if unit == "배" and not re.search(r"PER|PBR|PSR|PCR|EV|배수|현재가|중앙값|이력", near):
            continue
        yield unit, m.group(0), num, text[max(0, m.start() - 25):m.end() + 15].replace("\n", " ")


def strings(C):
    for k in dir(C):
        if k.startswith("_") or k in ("NEWS", "PR", "LINKS", "SEC", "S_", "TENQ", "RELEASE", "SEG", "CAPITAL", "ANALYST", "POST", "PRE"):
            continue
        v = getattr(C, k)
        if isinstance(v, str):
            yield k, v
        elif isinstance(v, (list, tuple)):
            for i, x in enumerate(v):
                if isinstance(x, str):
                    yield f"{k}[{i}]", x
                elif isinstance(x, (list, tuple)):
                    for j, y in enumerate(x):
                        if isinstance(y, str):
                            yield f"{k}[{i}][{j}]", y


def check(T, verbose):
    spec = importlib.util.spec_from_file_location("cfg", os.path.join(HERE, "cfg", f"cfg_{T.lower()}.py"))
    C = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(C)
    vals = card_values(T)
    idx = {u: {} for u in vals}
    for u, d in vals.items():
        for name, v in d.items():
            for f in forms(v):
                idx[u].setdefault(f, []).append(name)
    hits = []
    for key, s in strings(C):
        for unit, tok, num, ctx in literals(s):
            n = num.replace(",", "")
            names = idx.get(unit, {}).get(n) or idx.get(unit, {}).get(num)
            if names:
                hits.append((key, tok, names[:2], ctx))
    if verbose:
        for key, tok, names, ctx in hits:
            print(f"  {key}: {tok}  ← {', '.join(names)}  …{ctx}…")
    return hits


def main():
    args = [a.upper() for a in sys.argv[1:]]
    tickers = args or sorted(f[4:-3].upper() for f in os.listdir(os.path.join(HERE, "cfg")) if f.startswith("cfg_") and f.endswith(".py"))
    total = 0
    rows = []
    for T in tickers:
        if not os.path.exists(os.path.join(V2, f"{T}_full_widget.html")):
            continue
        try:
            hits = check(T, bool(args))
        except Exception as e:
            print(f"{T}: 확인 실패 {type(e).__name__}: {e}")
            continue
        total += len(hits)
        rows.append((len(hits), T))
        if args:
            print(f"{T}: {len(hits)}곳")
    if not args:
        print("cfg별 계산값 리터럴 수(많은 순):", ", ".join(f"{t} {n}" for n, t in sorted(rows, reverse=True) if n))
        print(f"합계 {total}곳 · 0곳인 cfg {sum(1 for n, _ in rows if n == 0)}장 / {len(rows)}장")


if __name__ == "__main__":
    main()
