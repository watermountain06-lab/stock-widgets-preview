#!/usr/bin/env python3
"""SEC를 직접 부르는 두 스크립트에 TSM 어댑터 파일을 먹인다.

`scripts/fetch_eps_history.py`와 redesign의 `fetch_financials.py`는 SEC API를 직접 부른다.
TSM은 SEC에 쓸 만한 us-gaap 데이터가 없으므로(tsm_ifrs.py 참조), 두 스크립트의 네트워크
함수만 바꿔 끼워 `v2/.sec_cache/0001046179_facts.json`(어댑터 산출물)을 돌려준다.
두 스크립트의 계산 로직은 그대로 쓴다.

사용법
------
    python3 v2/adapters/tsm_feed.py eps         # → scripts/TSM_eps_history.json
    python3 v2/adapters/tsm_feed.py financials  # → v2/fundamental_data/TSM_financials.json
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
FACTS = os.path.join(V2, ".sec_cache", "0001046179_facts.json")
CIK = "0001046179"


def facts():
    return json.load(open(FACTS))


def run_eps():
    sys.path.insert(0, os.path.join(REPO, "scripts"))
    import fetch_eps_history as feh

    def fake(url):
        f = facts()
        if "companyconcept" in url:
            tag = url.rstrip(".json").split("/")[-1]
            return {"units": f["facts"]["us-gaap"][tag]["units"]}
        return f
    feh.curl_json = fake
    feh.KNOWN_SPLITS.setdefault("TSM", [])   # ADR 1:5 비율은 창 안에서 바뀌지 않았다
    sys.argv = ["fetch_eps_history.py", "TSM", "--cik", CIK,
                "--out", os.path.join(REPO, "scripts", "TSM_eps_history.json")]
    feh.main()


def run_financials():
    sys.path.insert(0, os.path.join(os.path.dirname(REPO), "stock-widgets-redesign", "scripts"))
    import fetch_financials as ff
    ff.fetch_json = lambda url, ua: facts()
    sys.argv = ["fetch_financials.py", "TSM", "--cik", CIK, "--years", "5",
                "--out", os.path.join(V2, "fundamental_data", "TSM_financials.json")]
    ff.main()


if __name__ == "__main__":
    {"eps": run_eps, "financials": run_financials}[sys.argv[1]]()
