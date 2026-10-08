#!/usr/bin/env python3
"""매일 재빌드 전에 환율 세 개와 SK하이닉스 원주 일봉을 새로 받는다(2026-10-08 사용자 결정).

fx.py(TSM 대만달러, SKHY 원, ASML 유로)와 adapters/skhy_krx.py는 v2/.sec_cache의 파일을 읽기만 한다.
받는 단계가 파이프라인에 없어서 9월 말에 손으로 받은 값에 멈춰 있었다 — 환율은 9/18(유로 9/28),
SKHY 원주는 9/23. fx.rate는 없는 날짜에 직전 값을 쓰므로, 그 뒤 모든 날이 9/18 환율로 계산됐다.

원칙(메모리 "Provider failure shapes"): 받기에 실패하거나 결과가 기존보다 짧거나 마지막 날짜가 더
이르면 **기존 파일을 그대로 둔다**. 새 파일은 임시 파일에 쓴 뒤 바꿔 끼운다. 이 스크립트는 언제나
종료 코드 0으로 끝난다 — 참고 자료가 하루 묵는 것이 카드 재빌드를 멈추는 것보다 낫다.

    python3 v2/fetch_refs.py
"""
import csv
import datetime as dt
import io
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "adapters"))
import fx  # noqa: E402

FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"
ECB = "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?format=csvdata"


def get(url):
    # curl 기본 User-Agent로 받는다. FRED는 "Mozilla/5.0"만 붙이면 연결을 끊는다(2026-10-08 확인).
    return subprocess.run(["curl", "-sf", "--max-time", "60", url],
                          capture_output=True, check=True).stdout.decode("utf-8")


def rows_of(path, column):
    """(날짜, 값) 목록 — 값이 '.'(휴일)인 행도 날짜는 센다."""
    if not os.path.exists(path):
        return []
    return [(r["observation_date"], r.get(column)) for r in csv.DictReader(open(path))]


def good_value(v):
    """fx._load가 읽을 수 있는 값: 빈칸·'.'(휴일 — FRED는 빈칸, 옛 파일은 '.') 또는 0보다 큰 유한한 숫자."""
    if v in ("", "."):
        return True
    try:
        x = float(v)
    except (TypeError, ValueError):
        return False
    return math.isfinite(x) and x > 0


def good_date(d):
    try:
        return dt.date.fromisoformat(d).isoformat() == d
    except (TypeError, ValueError):
        return False


def replace_if_newer(path, column, text):
    """검사를 모두 통과할 때만 바꿔 끼운다(Codex 2026-10-08): 열이 있고, 날짜는 올바르고 중복 없이
    오름차순이며, 값은 빈칸·'.' 또는 양의 유한수이고, 기존에 숫자로 있던 날짜는 새 자료에도 숫자로 있고,
    마지막 날짜가 기존보다 이르지 않을 것."""
    new = [(r.get("observation_date"), r.get(column)) for r in csv.DictReader(io.StringIO(text))]
    old = rows_of(path, column)
    if not new or any(v is None for _, v in new):
        return f"형식이 다르다(열 {column} 없음) — 기존 유지"
    dates = [d for d, _ in new]
    if not all(good_date(d) for d in dates) or dates != sorted(set(dates)):
        return "날짜가 잘못됐거나 중복·역순이다 — 기존 유지"
    if not all(good_value(v) for _, v in new):
        return "숫자가 아닌 값이나 0 이하 값이 있다 — 기존 유지"
    numeric = {d for d, v in new if v not in ("", ".")}
    lost = [d for d, v in old if v not in (None, "", ".") and d not in numeric]
    if lost:
        return f"기존에 있던 환율 {len(lost)}일이 빠지거나 비었다(예: {lost[0]}) — 기존 유지"
    if old and dates[-1] < old[-1][0]:
        return f"마지막 날짜가 더 이르다({dates[-1]}) — 기존 유지"
    tmp = path + ".tmp"
    with open(tmp, "w", newline="") as f:
        f.write(text if text.endswith("\n") else text + "\n")
    os.replace(tmp, path)
    return f"{old[-1][0] if old else '없음'} → {new[-1][0]} ({len(new)}행)"


def fred(cur):
    col = fx.COLUMN[cur]
    return replace_if_newer(fx.SERIES[cur], col, get(FRED.format(col)))


def ecb():
    src = csv.DictReader(io.StringIO(get(ECB)))
    out = io.StringIO()
    w = csv.writer(out, lineterminator="\n")
    w.writerow(["observation_date", "EURUSD"])
    for r in src:
        if r.get("TIME_PERIOD") and r.get("OBS_VALUE"):
            w.writerow([r["TIME_PERIOD"], r["OBS_VALUE"]])
    return replace_if_newer(fx.SERIES["EUR"], "EURUSD", out.getvalue())


def skhy():
    """Yahoo는 최근 10년만 주므로 시작일이 매일 밀린다. 기존 일봉에 새 일봉을 날짜별로 합친다(같은 날은 새 값).
    받기·검사·병합이 끝날 때까지 기존 파일에는 쓰지 않는다(Codex 2026-10-08)."""
    import skhy_krx
    old = skhy_krx.load() if os.path.exists(skhy_krx.OUT) else []
    new = skhy_krx.download()
    if not new:
        return "빈 응답 — 기존 유지"
    if not all(good_date(b[0]) and len(b) == 5 and all(good_value(x) and x not in ("", ".") for x in b[1:]) for b in new):
        return "날짜나 시·고·저·종 값이 잘못된 일봉이 있다 — 기존 유지"
    if old and new[-1][0] < old[-1][0]:
        return f"새 자료의 마지막 날짜가 더 이르다({new[-1][0]}) — 기존 유지"
    merged = {b[0]: b for b in old}
    merged.update({b[0]: b for b in new})
    bars = [merged[d] for d in sorted(merged)]
    tmp = skhy_krx.OUT + ".tmp"
    json.dump(bars, open(tmp, "w"))
    os.replace(tmp, skhy_krx.OUT)
    return f"{old[-1][0] if old else '없음'} → {bars[-1][0]} ({len(bars)}일)"


def main():
    jobs = [("원/달러 (FRED DEXKOUS)", lambda: fred("KRW")),
            ("대만달러/달러 (FRED DEXTAUS)", lambda: fred("TWD")),
            ("유로 (ECB)", ecb),
            ("SK하이닉스 원주 (Yahoo 000660.KS)", skhy)]
    for name, job in jobs:
        try:
            print(f"{name}: {job()}")
        except Exception as e:  # 받기 실패는 기존 파일을 두고 넘어간다
            print(f"{name}: 받기 실패 — 기존 유지 ({type(e).__name__}: {str(e)[:120]})")


if __name__ == "__main__":
    main()
