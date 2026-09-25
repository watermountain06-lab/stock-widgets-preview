#!/usr/bin/env python3
"""S&P500 통제 유니버스의 SEC companyfacts를 받아 v2 스크립트가 쓰는 태그만 남겨 캐시한다.

디스크가 빠듯해(2026-09-25 여유 12GB) 원본 전체(종목당 3~5MB)를 두지 않는다. 남기는 태그는
build_multiple_history · build_dcf · build_fundamental_score · fetch_financials 소스에 적힌 태그 이름의 합집합.
재개 가능 — 이미 받은 종목은 건너뛴다.

    python3 v2/research/fetch_universe_facts.py
"""
import json
import os
import re
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
OUT = os.path.join(HERE, ".facts")
SP500 = "/Users/watermountain/Workspace/stock-widgets-redesign/scripts/sp500.json"
SOURCES = [os.path.join(V2, f) for f in ("build_multiple_history.py", "build_dcf.py", "build_fundamental_score.py")] + \
    ["/Users/watermountain/Workspace/stock-widgets-redesign/scripts/fetch_financials.py"]
UA = "kim research gptjhss@gmail.com"


def wanted_tags():
    tags = set()
    for p in SOURCES:
        tags |= set(re.findall(r'"([A-Z][A-Za-z]{3,})"', open(p, encoding="utf-8").read()))
    return tags


def main():
    os.makedirs(OUT, exist_ok=True)
    keep = wanted_tags()
    uni = json.load(open(SP500))
    done = 0
    for row in uni:
        cik = row["cik"].zfill(10)
        path = os.path.join(OUT, f"{cik}_facts.json")
        if os.path.exists(path):
            continue
        r = subprocess.run(["curl", "-s", "-A", UA, f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"],
                           capture_output=True)
        try:
            data = json.loads(r.stdout)
        except Exception:
            print("실패", row["ticker"]); time.sleep(1); continue
        facts = data.get("facts", {})
        slim = {ns: {t: v for t, v in tags.items() if t in keep} for ns, tags in facts.items() if ns in ("us-gaap", "dei")}
        json.dump({"cik": data.get("cik"), "entityName": data.get("entityName"), "facts": slim}, open(path, "w"))
        done += 1
        if done % 50 == 0:
            print(done, "종목")
        time.sleep(0.15)
    print("완료", done, "새로 받음")


if __name__ == "__main__":
    main()
