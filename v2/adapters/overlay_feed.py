#!/usr/bin/env python3
"""오버레이를 합친 companyfacts로 redesign의 fetch_financials를 돌린다(2026-09-27, V).

fetch_financials는 SEC API를 직접 부른다. companyfacts가 최신 10-Q를 아직 싣지 않은 종목(V: 2026-07-29 10-Q)은
`ixbrl_supplement.py`가 오버레이에 보충한 값을 build_multiple_history._facts(캐시 + 오버레이)로 먹인다.

    python3 v2/adapters/overlay_feed.py V 0001403161
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
sys.path.insert(0, V2)
import build_multiple_history as bmh  # noqa: E402


def main(ticker, cik):
    sys.path.insert(0, os.path.join(os.path.dirname(REPO), "stock-widgets-redesign", "scripts"))
    import fetch_financials as ff
    ff.fetch_json = lambda url, ua: bmh._facts(cik)
    sys.argv = ["fetch_financials.py", ticker, "--cik", cik, "--years", "5",
                "--out", os.path.join(V2, "fundamental_data", f"{ticker}_financials.json")]
    ff.main()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2].zfill(10))
