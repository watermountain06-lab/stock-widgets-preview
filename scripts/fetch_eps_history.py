#!/usr/bin/env python3
"""Fetch quarterly diluted EPS history from SEC EDGAR and compute TTM EPS per quarter,
with each entry tagged by the date it was ACTUALLY first disclosed -- suitable as a
point-in-time anchor for a real (no-look-ahead) backtest.

Forked from stock-widgets-customer/scripts/fetch_quarterly_eps.py with one correctness
fix, found and verified during this build:

  That script's dedup kept the LATEST-filed XBRL entry per (start,end) period, to solve
  split-restatement (get the correctly-scaled value). This has a side effect that breaks
  point-in-time correctness: EDGAR shows the same historical quarter's number again in
  each subsequent filing's comparative column, so "latest filed" can be a YEAR OR MORE
  after the number was actually first disclosed. Verified on real NVDA data:
    - 2022-05-01 (Q1 FY23): original filing accn ...-22-000079, filed 2022-05-27, val 0.64
                            later comparative accn ...-23-000093, filed 2023-05-26, val 0.64
    (latest-filed dedup would tag this quarter "available" a full year late)

  Fix: apply per-entry split-correction FIRST (using apply_split_correction, unchanged
  logic, keyed off each entry's OWN filed date), THEN dedup by (start,end) keeping the
  EARLIEST-filed entry. This resolves the split-restatement duplicates specifically
  (0.64/10=0.064 either way for the case above) -- but a 2026-09-02 Codex review
  correctly flagged that "switching which one wins only fixes the date, not the value"
  is NOT a general guarantee: if EDGAR later restates a filing for a reason OTHER than
  a known stock split (a genuine accounting correction/restatement), the earliest-filed
  value can legitimately differ from a later-corrected one, and this function has no way
  to detect that case -- it would silently keep the (possibly since-corrected) earliest
  value forever. Checked directly against NVDA's full raw EDGAR history for this risk:
  15 (start,end) groups have split-corrected values that disagree by >0 across
  duplicates; only 1 has a relative spread >1% (2017-01-30~2017-07-30, where a single
  outlier 2018-02-28 filing shows roughly half the other two filings' value -- earliest
  and latest both agree at 0.0427, so "earliest wins" happens to land on the correct
  side here), the rest are sub-cent 2016-era quarters where the "mismatch" is source
  data's own 2-decimal rounding, not a real restatement. So: no material impact found
  for NVDA specifically, but this is a real residual limitation of the method, not a
  solved problem -- re-check this for any other ticker before trusting its output blindly.

Usage:
    python3 fetch_eps_history.py NVDA --cik 0001045810 --out data/eps_quarterly/NVDA.json
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import date, timedelta


def curl_json(url):
    result = subprocess.run(
        ["curl", "-s", "-A", "Mozilla/5.0 (research; contact gptjhss@gmail.com)", url],
        capture_output=True, text=True, timeout=30,
    )
    return json.loads(result.stdout)


def split_ratio(filed, split_dates):
    ratio = 1
    for eff_date, r in split_dates:
        if filed < eff_date:
            ratio *= r
    return ratio


def apply_split_correction(entries, split_dates):
    for e in entries:
        r = split_ratio(e["filed"], split_dates)
        if r != 1:
            e["val"] = round(e["val"] / r, 6)
    return entries


def dedup_earliest_filed(entries):
    """Dedup by (start, end), keep the EARLIEST `filed` date -- the true first-disclosure
    date, i.e. the honest point-in-time anchor. Magnitude is unaffected since
    apply_split_correction() has already normalized every entry's `val` to today's share
    count using its OWN filed date, before this function runs."""
    best = {}
    for e in entries:
        key = (e["start"], e["end"])
        if key not in best or e["filed"] < best[key]["filed"]:
            best[key] = e
    return list(best.values())


# 분사로 과거 기간을 다시 공시한 종목(2026-09-30 사용자 결정 "분사 뒤 단독 숫자만", GE). 같은 기간 값은 **가장 나중 공시**
# (계속사업 재작성)를 쓰고, 공개일은 처음 공시일로 둔다 — 분사 사업을 빼고 다시 적은 숫자가 원공시의 자리에 들어간다.
# 4분기는 연간 − 9개월 누계로 만든다(1분기 원공시가 분사 사업을 포함한 채 남아 있어 세 분기를 빼면 섞인다).
RESTATED_LATEST = {"GE", "DELL", "IBM", "WDC", "T", "DHR"}   # DHR: 2023-09 Veralto 분사(2026-10-02, GE 방식)
# T: 2022-04 WarnerMedia 분사(2026-10-02, GE 방식)   # WDC: 2025-02 SanDisk 분사 — 분사 전 분기가 계속사업 기준으로 재작성됐다(2026-10-02, GE 방식)
# IBM: 2021-11 Kyndryl 분사 — 2021년 분기가 재작성됐다(2026-10-01, GE 방식)   # DELL: 2021-11 VMware 분사(2026-10-01 사용자 결정 "GE와 같은 방식")


def dedup_for(entries, ticker):
    """RESTATED_LATEST 종목이면 (start, end)마다 나중 공시 값 + 처음 공시일, 아니면 dedup_earliest_filed."""
    if ticker not in RESTATED_LATEST:
        return dedup_earliest_filed(entries)
    first, last = {}, {}
    for e in entries:
        key = (e["start"], e["end"])
        if key not in first or e["filed"] < first[key]["filed"]:
            first[key] = e
        if key not in last or e["filed"] > last[key]["filed"]:
            last[key] = e
    return [{**last[k], "filed": first[k]["filed"]} for k in first]


def days_between(e):
    # Guard: a few filers have a malformed XBRL entry with no "start" (confirmed on GS,
    # one 2008 entry). Returning -1 makes it fail both the quarterly (80<=d<=100) and
    # annual (d>350) filters in main(), so it is dropped before dedup_earliest_filed()
    # -- which would otherwise KeyError on e["start"] too.
    if "start" not in e:
        return -1
    return (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days


# 연간을 소급 수정했는데 분기는 원공시라 "연간 − 1~3분기"가 섞이는 종목의 4분기 희석 EPS(분할 반영 값).
# CRWD FY26 4분기: 주식보상비용 인식 시점 오류(경미)를 10-K에서 고쳐 연간 −0.65 대 원공시 분기 합이 맞지 않아 0.24(분할 전)가 나왔다.
# 2026-03-03 보도자료 희석 EPS $0.15 ÷ 4 = 0.0375(2026-10-01, Fable).
# BA 2025 4분기: 1~3분기 적자(희석 주식 = 기본)와 4분기 흑자(전환우선주 희석 포함)의 주식 수가 달라 연간 $2.48 − 9개월 −$8.25 = $10.73이 나온다. 보도자료 $10.23.
# UBER 2025 4분기: 연간 − 9개월이 $0.16(분기마다 희석 주식 수가 다름, 3분기 세금 환입 $4.9B 분기 포함). 보도자료 $0.14.
# FTNT 2025 4분기: 연간 $2.42 − 9개월 $1.75 = $0.67, 보도자료 $0.68(적정주가 밴드 하단이 $90/$100로 갈림, Fable).
Q4_EPS_OVERRIDE = {"CRWD": {"2026-01-31": 0.0375}, "BA": {"2025-12-31": 10.23}, "UBER": {"2025-12-31": 0.14}, "FTNT": {"2025-12-31": 0.68},
                   # COF: 2025년 5월 Discover 인수로 희석 주식 수가 3.8억→6.4억 주로 바뀌어 연간 − 9개월 역산이 $4.33(보도자료 4분기 $3.26, Fable 2026-10-02)
                   "COF": {"2025-12-31": 3.26},
                   # CVNA: Up-C 구조라 희석 EPS의 전환 가정(비지배지분 포함 여부)이 분기마다 달라 연간 − 9개월 역산이 0.926(분할 반영) — 주주서한 4분기 희석 EPS $4.22 ÷ 5(2026-05 5:1 분할) = 0.844(Codex·Fable 2026-10-05)
                   "CVNA": {"2025-12-31": 0.844}}
KNOWN_SPLITS = {
    "NVDA": [("2021-07-20", 4), ("2024-06-07", 10)],
    # Verified 2026-09-02 against real EDGAR duplicate-filing detection (not just public
    # knowledge) for the cross-ticker valuation-IC backtest -- see
    # scripts/compute_valuation_ic.py. Detected ratios matched known split facts for all.
    "AAPL": [("2014-06-09", 7), ("2020-08-31", 4)],
    "AMZN": [("2022-06-06", 20)],
    "AVGO": [("2024-07-15", 10)],
    "GOOGL": [("2022-07-18", 20)],
    "TSLA": [("2020-08-31", 5), ("2022-08-25", 3)],
    "META": [],   # no splits ever -- confirmed empirically (no ratio>1.3 duplicate found)
    "MSFT": [],   # last split 2003, outside this data's reporting window -- confirmed empirically
    "MU": [],     # last split 2000-05-02, outside this data's reporting window -- WebSearch confirmed
    "JPM": [],    # last split 2000-06-12 (3-for-2), outside this data's reporting window -- WebSearch confirmed 2026-09-04
    "LLY": [],    # last split 1997-10-16 (2-for-1), outside this data's reporting window -- WebSearch confirmed 2026-09-04
    "WMT": [("2024-02-26", 3)],  # 3-for-1 split, effective 2024-02-26 -- WebSearch confirmed 2026-09-05 (corporate.walmart.com release), within this data's 5y window
    "AMD": [],    # last split 2000-08-22 (2-for-1), outside this data's reporting window -- WebSearch confirmed 2026-09-05
    "ASML": [],   # no split or share consolidation in the data window (2019~)
    "JNJ": [],    # last split 2001-06-13 (2-for-1), outside this data's reporting window -- WebSearch confirmed 2026-09-05
    "MA": [],     # last split 10-for-1 effective 2014-01, outside this data's reporting window -- WebSearch confirmed 2026-09-06
    "AMAT": [],   # last split 2002-04-16 (2-for-1), outside this data's reporting window
    "UNH": [],    # last split 2005-05-31 (2-for-1), outside this data's reporting window
    "GE": [("2021-08-02", 0.125)],  # 1-for-8 reverse split effective 2021-08-02 (GE 8-K 2021-07-30); spin-offs of GE HealthCare (2023-01-04) and GE Vernova (2024-04-02) are distributions, not splits
    "CVX": [],    # last split 2004-09-13 (2-for-1), outside this data's reporting window
    "PLTR": [],   # no splits since the 2020-09-30 direct listing -- Yahoo split events confirmed 2026-09-29
    "INTC": [],   # last split 2000 (2-for-1), outside this data's reporting window -- Yahoo split events confirmed 2026-09-29
    "XOM": [],    # last split 2001-07-19 (2-for-1), outside this data's reporting window -- WebSearch confirmed 2026-09-06
    "ORCL": [],   # last split 2000-10-13 (2-for-1), outside this data's reporting window -- WebSearch confirmed 2026-09-06
    "ABBV": [],   # no splits ever since 2013 Abbott spinoff -- WebSearch confirmed 2026-09-06
    "COST": [],   # last split 2000-01-03 (2-for-1), outside this data's reporting window -- confirmed empirically (no ratio>1.3 duplicate found in the full XBRL EPS history back to 2012)
    "LRCX": [("2024-10-02", 10)],  # 10-for-1 split, effective 2024-10-02 -- confirmed via LRCX FY2025 10-K text ("On October 2, 2024, the Company effected a 10-for-one stock split")
    "CAT": [],    # last split 2005-06-13 (2-for-1), outside this data's reporting window -- confirmed empirically (no ratio>1.3 duplicate found in fetched XBRL EPS history)
    "MRK": [],    # no stock split found -- the only >1.3x duplicate-value groups in the full XBRL history are 4 quarters from 2009 (Schering-Plough merger restatement, not a split), all outside this data's 5y window -- confirmed empirically 2026-09-07
    "CSCO": [],   # no split within the fetched XBRL history -- confirmed empirically 2026-09-07 (0 duplicate-value groups found at all)
    "KO": [],     # last split 2012-08 (2-for-1), outside this data's 5y reporting window -- confirmed empirically 2026-09-07 (7 duplicate-value groups found, all from 2010-2013 restatements pre-dating the window)
    "MS": [],     # last split 2000-01-27 (2-for-1), outside this data's 5y reporting window -- WebSearch confirmed 2026-09-09
    "DELL": [],   # no proportional stock split -- the 2021-11-02 "1973-for-1000"/"903-for-500" ratios some aggregators list are the VMware spinoff's Class V tracking-stock exchange into Class C, a fixed-ratio security conversion, not a market-wide split of existing Class C shares (no price discontinuity around 2021-11-02 in Yahoo daily data) -- confirmed empirically 2026-09-09 (0 duplicate-value groups with ratio>1.3 found in full XBRL EarningsPerShareDiluted history)
    "PG": [],     # last split 2004-06-21 (2-for-1), outside this data's 5y reporting window -- WebSearch confirmed 2026-09-09
    "PANW": [("2022-09-14", 3), ("2024-12-12", 2)],  # 3-for-1 effective 2022-09-14 added 2026-10-04 (C12 — Yahoo 5y split check found it missing; only loss-era FY2022 filings were affected, TTM was negative then)
     # 2-for-1 split, effected 2024-12-12 -- confirmed via PANW FY2025 10-K text ("On December 12, 2024, we effected a two-for-one stock split of our outstanding shares of common stock"); all share/per-share amounts retroactively adjusted by the company
    "HD": [],     # last split 1999-12-30 (3-for-2), far outside this data's XBRL window (HD's EarningsPerShareDiluted history starts at FY2007, earliest end 2008-02-03) -- WebSearch confirmed 2026-09-09 (13 splits between 1982 and 1999, none since) and confirmed empirically (0 of 121 (start,end) groups in the full XBRL EPS history have a duplicate-value ratio >1.3)
    "GS": [],     # GS has never split since its 1999 IPO -- confirmed empirically (no duplicate (start,end) group with ratio>1.3 in the full XBRL EarningsPerShareDiluted history)
    "NFLX": [("2025-11-14", 10)],  # 10-for-1 forward split -- confirmed via NFLX FY2025 10-K Item 5 / Q2 2026 10-Q Note 1 text ("On November 14, 2025, the Company completed a ten-for-one forward stock split of the Company's issued common stock"), record date 2025-11-10, split-adjusted trading from 2025-11-17. Boundary is the 11-14 completion date, not the 11-17 trading date, because split_ratio() compares each XBRL entry's FILED date: last pre-split filing 2025-10-22 (Q3'25 10-Q, EPS 5.87 -> 0.587), first post-split filing 2026-01-23 (FY25 10-K, EPS 2.53 as-filed)
    "PM": [],     # PM has never split since it began trading in 2008 -- the spin-off from Altria was a 1-for-1 distribution of PM shares to Altria holders (a separation, not a split of PM stock) -- WebSearch confirmed 2026-09-09 and confirmed empirically (0 of 123 (start,end) groups in the full XBRL EarningsPerShareDiluted history have a duplicate-value ratio >1.3)
    "WFC": [],    # last split 2-for-1 in August 2006 (announced 2006-06-27 as a 100% stock dividend, record date 2006-08-04, distributed 2006-08-11, split-adjusted from 2006-08-14 -- SEC 8-K exhibit 99.2, accession 0001193125-06-140458), far outside both this data's 5y price window and WFC's XBRL EarningsPerShareDiluted history (earliest end 2007-12-31) -- confirmed empirically 2026-09-10 (only 3 of 111 (start,end) groups have a duplicate-value ratio >1.3; all three are 2020 COVID-era loss quarters restated between the 2020 and 2021 filings at ratios 1.45/1.53/1.67, none a clean 1.5x or 2x split signature, and all pre-date the 5y window)
    "GEV": [],    # GE Vernova has never split. It began trading on the NYSE on 2024-04-02 as a spin-off from General Electric (now GE Aerospace): GE holders of record on 2024-03-19 received one GEV share for every four GE shares held (WebSearch confirmed 2026-09-10 against GE's own 2024-04-02 spin-off FAQ, and the FY2025 10-K's "On April 2, 2024 ... GE distributed all of the shares of our common stock to its stockholders"). That 1-for-4 distribution ratio is the rate at which a NEW security was handed to the PARENT's holders -- not a proportional split of GEV's own outstanding shares -- so nothing in GEV's per-share history is retroactively restated by it, and the price-adjustment factor vendors book for the event lands on the parent ticker (GE), not on GEV. Same distinction already documented for DELL's VMware Class V exchange and RTX's 2020-04-03 Carrier/Otis spin-off factor below. GEV's XBRL EarningsPerShareDiluted history begins at end 2022-12-31 (Form 10 carve-out combined financials); confirmed empirically 2026-09-10 that 0 of 21 (start,end) groups have a duplicate-value ratio >1.3.
    "RTX": [],    # no proportional stock split inside this data's window. Last true split was United Technologies' 2-for-1 on 2005-06-13 (earlier UTC 2-for-1s: 1999-05-18 -- board declared 1999-04-30, stock dividend issued 1999-05-17 per UTC's own 8-K/press release -- plus 1996-12-11, 1984-06-11, 1976-05-19); WebSearch confirmed 2026-09-10. That is outside RTX's XBRL EarningsPerShareDiluted history, which starts at end 2007-12-31, and far outside this data's 5y price window (from 2021-09-10). The "1589-for-1000 on 2020-04-03" that Investing.com/Seeking Alpha list in RTX's split column is NOT a split: on 2020-04-03 UTC completed the Carrier (0.5 sh/UTX sh) and Otis (0.25 sh/UTX sh) spin-offs and then merged with Raytheon Company (2.3348 RTX sh per RTC sh); price vendors book the ~1.589 spinoff price-adjustment factor as a split row -- the same aggregator artifact already documented for DELL's VMware Class V exchange above, and it too pre-dates the 5y window. Confirmed empirically 2026-09-10: 0 of 123 (start,end) groups in the full XBRL EPS history have a duplicate-value ratio >1.3, so no retroactive per-share restatement exists anywhere in the series.
    "ANET": [("2021-11-18", 4), ("2024-12-04", 4)],  # TWO 4-for-1 forward splits, both inside this data's 5y price window (which starts 2021-09-10) -- confirmed 2026-09-10 from ANET's OWN filings, not from an aggregator. (1) FY2021 10-K Note 1: "On November 1, 2021, we announced a four-for-one split ... effected in the form of a stock dividend. Each stockholder of record on November 11, 2021 received three additional shares ... distributed after close of trading on November 17, 2021", so split-adjusted trading begins 2021-11-18. (2) FY2025 10-K Note 1 + the 2024-12-03 8-K Item 5.03: "On November 7, 2024, the Company announced a four-for-one forward stock split ... effected through the filing of an amendment ... which became effective at 4:30 p.m. Eastern Time on December 3, 2024", so split-adjusted trading begins 2024-12-04. Each boundary is the split-adjusted TRADING date because split_ratio() compares each XBRL entry's FILED date, and both dates sit cleanly between the last pre-split filing and the first post-split one (2021: last pre 2021-11-02 Q3'21 10-Q EPS 2.81 -> 0.70; first post 2022-02-15 FY21 10-K. 2024: last pre 2024-11-08 Q3'24 10-Q EPS 2.33 -> 0.58; first post 2025-02-19 FY24 10-K EPS 2.23 as-filed). Confirmed empirically the same day: 14 of 88 (start,end) groups in the full XBRL EarningsPerShareDiluted history have a duplicate-value ratio >1.3, and every one is a clean ~4.00x step at exactly one of these two boundaries (e.g. FY2019 10.63 filed 2021-02-19 -> 2.66 filed 2022-02-15 = 3.996x; FY2022 4.27 filed 2024-02-13 -> 1.07 filed 2025-02-19 = 3.99x) -- no non-split restatement anywhere in the series. Yahoo's 5y daily series is already adjusted for BOTH (max single-day moves in the whole window are +20.4% on 2021-11-02, the Q3'21 earnings pop, and -22.4% on 2025-01-27, the DeepSeek AI-capex selloff; no >50% discontinuity at either split date).
    "TSM": [],    # 어댑터(v2/adapters/tsm_ifrs.py)가 EPS를 ADR 1주(= 보통주 5주) 기준으로 만든다. ADR 비율 1:5는 이 데이터 창(2020~) 안에서 바뀌지 않았다. TSMC 보통주는 액면분할이 없었다.
    "V": [],      # Visa 마지막 분할 2015-03-19(4:1), 데이터 창 밖
    "SKHY": [],   # 어댑터(v2/adapters/skhy_ifrs.py)가 EPS를 ADR 1주(= 보통주 0.1주) 기준으로 만든다. SK하이닉스 보통주는 데이터 창(2020~) 안에 액면분할이 없었다(발행주식 728,002,365주가 2020~2025 보고서에서 그대로, 2026 소각·ADR 신주로만 변동).
    "SPCX": [],   # 2026-05 5:1 분할은 상장(2026-06-12) 전이라 SEC 공시·가격 모두 분할 후 숫자다(10-Q "2026 Stock Split", 2026-09-25 확인)
    "SNDK": [],   # SanDisk has never split -- it only began trading 2025-02-13 (when-issued) / 2025-02-24 (regular-way, Nasdaq) after Western Digital distributed 80.1% of SanDisk on 2025-02-21 at one-third of a SNDK share per WDC share. That distribution ratio is the SPINOFF's exchange ratio applied to WDC holders, not a split of SNDK's own outstanding shares -- the same aggregator artifact already documented for DELL's VMware Class V exchange and RTX's 2020 Carrier/Otis spin-merge above, except here it belongs to the PARENT's price series, so it must never be applied to SNDK's own EPS history. Confirmed empirically 2026-09-10: SNDK's full XBRL EarningsPerShareDiluted history (20 entries, earliest end 2023-06-30, carve-out periods included) has 0 (start,end) groups with any duplicate-value disagreement at all, let alone a ratio >1.3.
    "TXN": [],    # 데이터 창(2021-09~) 안에 분할 없음 — Yahoo 분할 기록 없음(2026-10-01 확인)
    "C": [],      # 마지막 분할은 2011-05 1:10 병합으로 데이터 창 밖 — Yahoo 창 안 기록 없음(2026-10-01 확인)
    "NEE": [("2020-10-27", 4.0)],   # 4-for-1 split effective 2020-10-27 (Yahoo split event 2020-10-27, 2026-10-02)
    "BKNG": [("2026-04-06", 25.0)],   # 25-for-1 split, first split-adjusted session 2026-04-06 (Yahoo split event, 2026-10-02)
    "NOW": [("2025-12-18", 5.0)],   # 5-for-1 split, first split-adjusted session 2025-12-18 (Yahoo split event, 2026-10-02)
    "ISRG": [("2021-10-05", 3.0)],   # 3-for-1 split, first split-adjusted session 2021-10-05 (Yahoo split event, 2026-10-02)
    "FTNT": [("2022-06-23", 5.0)],   # 5-for-1 split, first split-adjusted session 2022-06-23 (Yahoo split event, 2026-10-02)
    "KLAC": [("2026-06-12", 10)],  # 10:1 정분할 — 2026-05-07 8-K 발표, 2026-06-11 23:59 정관 개정 효력(2026-06-12 8-K Item 5.03), 6/12부터 분할 후 거래. 2026-10-01 확인
    "IBM": [],    # 분할 없음 — 2021-11-04 Kyndryl 분사 조정 비율 1.046은 분할이 아니다(splits.py ignored, 2026-10-01)
    "TMO": [],    # 데이터 창(2021-09~) 안에 분할 없음 — Yahoo 기록 없음(2026-10-01)
    "AXP": [],    # 데이터 창 안에 분할 없음 — Yahoo 기록 없음(2026-10-01)
    "LIN": [],    # 데이터 창 안에 분할 없음 — Yahoo 기록 없음(2026-10-01)
    "CRWD": [("2026-07-02", 4)],   # 4:1 주식 배당형 분할 — 2026-06-03 8-K(기록일 6/25, 7/2부터 분할 기준 거래). 마지막 분할 전 공시 2026-06-04(Q1 FY27 10-Q), 첫 분할 후 2026-08-27(Q2 FY27 10-Q)
    "APH": [("2021-03-05", 2), ("2024-06-12", 2), ("2026-09-03", 2)],   # 2:1 세 번 — 마지막은 2026-08-06 8-K(기록일 8/17, 9/2 배분, 9/4 8-K "now been effected"). 분할 뒤 EPS 공시가 아직 없어 기존 공시 전부 ÷2
    "VZ": [], "MRVL": [], "AMGN": [], "CRM": [],
    "TMUS": [], "QCOM": [], "STX": [], "PEP": [], "SCHW": [], "DIS": [], "DE": [], "ADI": [], "GILD": [], "BLK": [], "ETN": [], "ABT": [], "WDC": [], "T": [], "MCD": [], "WELL": [], "UNP": [], "PFE": [], "COP": [], "DHR": [], "BA": [], "TJX": [], "BX": [], "GLW": [], "UBER": [], "VRTX": [], "CB": [], "PLD": [], "BMY": [], "PH": [], "PGR": [], "NEM": [], "ACN": [], "COF": [], "MPC": [],   # 데이터 창 안에 분할 없음 — Yahoo 기록 없음(2026-10-01)
}

CIKS = {
    "NVDA": "0001045810", "AAPL": "0000320193", "AMZN": "0001018724",
    "AVGO": "0001730168", "GOOGL": "0001652044", "META": "0001326801",
    "MSFT": "0000789019", "TSLA": "0001318605", "WMT": "0000104169",
    "AMD": "0000002488",
    # TSM: SEC에 us-gaap 데이터가 없어 v2/adapters/tsm_ifrs.py가 만든 캐시를 쓴다(tsm_feed.py로 실행).
    "TSM": "0001046179",
    "SPCX": "0001181412",
    "MU": "0000723125",
    "LLY": "0000059478",
    "JPM": "0000019617",
    # SKHY: SEC companyfacts가 비어 v2/adapters/skhy_ifrs.py(KIND 원문 K-IFRS)가 만든 캐시를 쓴다(skhy_feed.py로 실행).
    "SKHY": "0002120882",
    "V": "0001403161",
    "JNJ": "0000200406",
    # ASML: 10-Q가 없어 companyfacts는 연간 유로뿐 — v2/adapters/asml_ifrs.py(6-K US GAAP 분기 요약)가 만든 캐시를 쓴다(asml_feed.py로 실행).
    "ASML": "0000937966",
    "XOM": "0000034088",
    "INTC": "0000050863",
    "MA": "0001141391",
    "ABBV": "0001551152",
    "PLTR": "0001321655",
    "CVX": "0000093410",
    "COST": "0000909832",
    "LRCX": "0000707549",
    "KO": "0000021344",
    "CAT": "0000018230",
    "MRK": "0000310158",
    "AMAT": "0000006951",
    "UNH": "0000731766",
    "GE": "0000040545",
    "DELL": "0001571996",
    "MS": "0000895421",
    "PG": "0000080424",
    "NFLX": "0001065280",
    "HD": "0000354950",
    "PM": "0001413329",
    "PANW": "0001327567",
    "WFC": "0000072971",
    "ORCL": "0001341439",
    "BAC": "0000070858",
    "CSCO": "0000858877",
    "RTX": "0000101829",
    "SNDK": "0002023554",
    "GEV": "0001996810",
    "ANET": "0001596532",
    "TXN": "0000097476",
    "KLAC": "0000319201",
    "C": "0000831001",
    "IBM": "0000051143",
    "TMO": "0000097745",
    "AXP": "0000004962",
    "LIN": "0001707925",
    "CRWD": "0001535527",
    "VZ": "0000732712",
    "MRVL": "0001835632",
    "APH": "0000820313",
    "AMGN": "0000318154",
    "CRM": "0001108524",
    "TMUS": "0001283699",
    "DIS": "0001744489",
    "DE": "0000315189",
    "ADI": "0000006281",
    "GILD": "0000882095",
    "BLK": "0002012383",
    "ETN": "0001551182",
    "WDC": "0000106040",
    "T": "0000732717",
    "MCD": "0000063908",
    "WELL": "0000766704",
    "UNP": "0000100885",
    "PFE": "0000078003",
    "NEE": "0000753308",
    "COP": "0001163165",
    "DHR": "0000313616",
    "BA": "0000012927",
    "TJX": "0000109198",
    "BX": "0001393818",
    "GLW": "0000024741",
    "NOW": "0001373715",
    "ISRG": "0001035267",
    "UBER": "0001543151",
    "FTNT": "0001262039",
    "VRTX": "0000875320",
    "CB": "0000896159",
    "PLD": "0001045609",
    "BMY": "0000014272",
    "PH": "0000076334",
    "PGR": "0000080661",
    "BKNG": "0001075531",
    "NEM": "0001164727",
    "ACN": "0001467373",
    "COF": "0000927628",
    "MPC": "0001510295",
    "ABT": "0000001800",
    "QCOM": "0000804328",
    "STX": "0001137789",
    "PEP": "0000077476",
    "SCHW": "0000316709",
    "GS": "0000886982",
}


# 4분기가 16주(53주 해는 17주)인 52·53주 회계. 1분기 말 → 연말이 287일이 돼 280일 규칙에 걸려
# 2023-09-03(53주 FY2023) 4분기가 빠지고 그 뒤 TTM EPS가 약 12% 낮게 나왔다(COST, Fable 2026-09-29).
LONG_Q4_TICKERS = {"COST", "PEP"}   # PEP: 12·12·12·16주(2026-10-01)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--cik", required=True)
    ap.add_argument("--tag", default="EarningsPerShareDiluted")
    ap.add_argument("--out", required=True)
    # 분할 목록을 밖에서 넘긴다("YYYY-MM-DD:비율,…") — KNOWN_SPLITS에 없는 종목(S&P500 비교군)용. 없으면 분할 뒤 연간 EPS에서
    # 분할 전 분기 EPS를 빼 4분기 EPS가 크게 틀린다(ORLY 2025-06 15:1 → 2025년 4분기 −8.01, 안건 C12 2026-10-04).
    ap.add_argument("--splits", help='예: "2025-06-10:15" (KNOWN_SPLITS에 있으면 그쪽이 앞선다)')
    args = ap.parse_args()

    # --tag "A,B": A가 없는 (start, end) 기간만 B로 채운다. DELL은 계속사업 EPS 태그를 FY2023 뒤로 쓰지 않는다(분사 뒤 중단사업이
    # 없어 희석 EPS와 같다, 2026-10-01). 앞 태그를 다 받은 뒤 뒤 태그의 빈 기간을 더한다.
    tags = args.tag.split(",")
    if len(tags) > 1:
        entries, seen = [], set()
        for tg in tags:
            facts = curl_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{args.cik}.json")
            rows = facts["facts"]["us-gaap"].get(tg, {}).get("units", {}).get("USD/shares", [])
            if args.ticker.upper() in RESTATED_LATEST:
                # 재작성 종목은 태그를 가리지 않고 다 모은다 — 같은 기간은 dedup_for가 가장 나중 공시를 고른다(같은 날이면 앞 태그).
                # DELL FY2024 계속사업 $4.36(2024-03)보다 뒤 10-K의 희석 $4.60이 회사의 현재 숫자다(Codex, 2026-10-01).
                rows = [e for e in rows if "start" in e]
            else:
                rows = [e for e in rows if "start" in e and (e["start"], e["end"]) not in seen]
            seen |= {(e["start"], e["end"]) for e in rows}
            entries += rows
        data = None
    else:
        url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{args.cik}/us-gaap/{args.tag}.json"
        data = curl_json(url)
        entries = data["units"]["USD/shares"]
    if not entries:
        # companyconcept has a known intermittent indexing-lag bug (returns
        # units:{"USD/shares":{}} for a filer that has real data) -- confirmed
        # on KO twice (2026-09-06, 2026-09-07, >24h apart, still empty both
        # times, so not a transient blip). companyfacts serves the same
        # underlying data and has not shown this bug -- fall back to it.
        print(f"NOTE: companyconcept returned 0 entries for {args.ticker}, "
              f"falling back to companyfacts", file=sys.stderr)
        if len(tags) > 1:
            entries = []   # 여러 태그는 이미 companyfacts에서 읽었다 — 아래 오버레이(원문 인라인 XBRL)가 채운다(V, D66 2026-10-04)
        else:
            facts = curl_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{args.cik}.json")
            entries = facts["facts"]["us-gaap"][args.tag]["units"]["USD/shares"]

    # companyfacts·companyconcept가 최근 10-Q를 몇 달씩 싣지 않는 회사는 v2/adapters/ixbrl_supplement.py가 원문 인라인 XBRL로
    # v2/.sec_cache/overlay/{cik}.json을 만든다. 그 파일에 이 태그의 행이 있으면 SEC 데이터에 없는 (start, end)만 더한다 — C는
    # 2026년 1·2분기 10-Q가 빠져 최근 4분기 EPS가 2025-12에 멈췄다($6.99 대 실제 $9.26, PER 18.5배 대 14배, 2026-10-01).
    _ov = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "v2", ".sec_cache", "overlay", f"{args.cik}.json")
    if os.path.exists(_ov):
        _ovrows = [dict(r) for tg in tags for r in json.load(open(_ov)).get("us-gaap", {}).get(tg, [])
                   if r.get("unit", "USD/shares") == "USD/shares" and "start" in r]
        # 옛 CIK(predecessor_facts.py, BLK 2024 재편) 행은 같은 기간 새 CIK 비교 수치보다 앞선다 — 새 CIK는 그 기간을 1년 늦게 실어
        # 공시일이 밀린다(2023-09-30 분기가 2024-11-06로 보였다, 2026-10-01)
        _pred = {(r["start"], r["end"]) for r in _ovrows if str(r.get("src", "")).startswith("predecessor:")}
        if _pred:
            entries = [e for e in entries if (e.get("start"), e["end"]) not in _pred]
        _have = {(e.get("start"), e["end"]) for e in entries}
        _add = [r for r in _ovrows if (r["start"], r["end"]) not in _have]
        if _add:
            print(f"NOTE: overlay에서 {len(_add)}개 행 보충({args.ticker})", file=sys.stderr)
            entries = list(entries) + _add

    ticker_key = args.ticker.upper()
    if ticker_key not in KNOWN_SPLITS and args.splits is None:
        print(f"WARNING: no known-split table for {args.ticker} -- add an entry "
              f"(even an empty list, if verified split-free) before trusting this output.",
              file=sys.stderr)
    split_dates = KNOWN_SPLITS.get(ticker_key, [])
    if ticker_key not in KNOWN_SPLITS and args.splits:
        split_dates = [(d, float(r)) for d, r in (x.split(":") for x in args.splits.split(",") if x)]
    if split_dates:
        entries = apply_split_correction(entries, split_dates)

    if ticker_key in RESTATED_LATEST:
        # 10-K의 분기 비교 값도 재작성 값이다(DELL FY2024 분기 $0.86·$0.66·$1.42). 단위가 잘못 붙은 값(DELL FY2022 10-K
        # 계속사업 EPS 840000·−40000)은 주당 $1,000을 넘으면 버린다.
        entries = [e for e in entries if abs(e["val"]) < 1000]
    qforms = ("10-Q", "10-K") if ticker_key in RESTATED_LATEST else ("10-Q",)
    discrete = dedup_for([e for e in entries if e["form"] in qforms and 80 <= days_between(e) <= 100], ticker_key)
    if ticker_key in RESTATED_LATEST:
        # 10-K에만 있는 4분기 3개월 값은 처음 공시일을 그해 연간 실적의 처음 공시일로 당긴다(그날 연간 − 9개월로 이미 알 수 있었다).
        fy_first = {}
        for e in entries:
            if e["form"] == "10-K" and days_between(e) > 350:
                fy_first[e["end"]] = min(fy_first.get(e["end"], e["filed"]), e["filed"])
        discrete = [{**q, "filed": fy_first[q["end"]]} if q["end"] in fy_first and fy_first[q["end"]] < q["filed"] else q
                    for q in discrete]
    annual = dedup_for([e for e in entries if e["form"] == "10-K" and days_between(e) > 350], ticker_key)
    ytd9 = {(e["start"], e["end"]): e for e in dedup_for(
        [e for e in entries if e["form"] == "10-Q" and 260 <= days_between(e) <= 285], ticker_key)}

    # 분기 3개월 값이 빠진 분기는 같은 해 누계(6개월·9개월 10-Q)에서 나머지 분기를 빼 만든다(D66, 2026-10-04 — PPL 2026 1분기
    # 희석 EPS가 3개월 값으로 태그되지 않아, 빠진 채 마지막 네 행을 더하면 2025-06~2026-06 다섯 분기에 걸친 틀린 4분기 합이 나왔다).
    _ytd = dedup_for([e for e in entries if e["form"] == "10-Q" and (170 <= days_between(e) <= 195 or 260 <= days_between(e) <= 285)],
                     ticker_key)
    _have_end = {q["end"] for q in discrete}
    for y in sorted(_ytd, key=lambda e: e["end"]):
        ys, ye = date.fromisoformat(y["start"]), date.fromisoformat(y["end"])
        n = 2 if days_between(y) <= 195 else 3
        inside = sorted([q for q in discrete if date.fromisoformat(q["start"]) >= ys - timedelta(days=3)
                         and date.fromisoformat(q["end"]) <= ye], key=lambda q: q["end"])
        if len(inside) != n - 1:
            continue
        bounds = [ys] + [x for q in inside for x in (date.fromisoformat(q["start"]), date.fromisoformat(q["end"]) + timedelta(days=1))] + [ye + timedelta(days=1)]
        gaps = [(bounds[k], bounds[k + 1]) for k in range(0, len(bounds), 2) if (bounds[k + 1] - bounds[k]).days > 60]
        if len(gaps) != 1:
            continue
        g0, g1 = gaps[0]
        end = (g1 - timedelta(days=1)).isoformat()
        if end in _have_end:
            continue
        discrete.append({"start": g0.isoformat(), "end": end, "val": round(y["val"] - sum(q["val"] for q in inside), 4),
                         "accn": y["accn"], "fy": y.get("fy"), "fp": "Q-ytd-derived", "form": "10-Q",
                         # 빼는 데 쓴 값이 모두 나온 날에야 알 수 있다(Codex — CSCO 2009-10 누계 행이 2010-05에 처음 나옴)
                         "filed": max([y["filed"]] + [q["filed"] for q in inside])})
        _have_end.add(end)
    discrete.sort(key=lambda e: e["end"])
    annual.sort(key=lambda e: e["end"])

    quarters = list(discrete)
    for fy in annual:
        fy_end = fy["end"]
        fy_end_d = date.fromisoformat(fy_end)
        members = [
            q for q in discrete
            if date.fromisoformat(q["end"]) <= fy_end_d
            and (fy_end_d - date.fromisoformat(q["start"])).days <= 380
            and (fy_end_d - date.fromisoformat(q["end"])).days <= (295 if ticker_key in LONG_Q4_TICKERS else 280)
        ]
        if len(members) == 3 and not any(q["end"] == fy_end for q in discrete):
            q4_val = round(fy["val"] - sum(m["val"] for m in members), 4)
            last_q = max(members, key=lambda m: m["end"])
            nine = ytd9.get((fy["start"], last_q["end"]))
            if ticker_key in RESTATED_LATEST and nine:
                q4_val = round(fy["val"] - nine["val"], 4)   # 연간 − 9개월 누계(재작성 종목)
            if fy_end in Q4_EPS_OVERRIDE.get(ticker_key, {}):
                q4_val = Q4_EPS_OVERRIDE[ticker_key][fy_end]   # 보도자료 4분기 값(분할 반영) — 수정 연간 − 원공시 분기 섞임 방지
            quarters.append({
                "start": last_q["end"], "end": fy_end, "val": q4_val,
                "accn": fy["accn"], "fy": fy.get("fy"), "fp": "Q4-derived",
                # 누계로 메운 분기를 빼서 만든 4분기는 그 분기가 나온 날 뒤에야 알 수 있다(Codex, 2026-10-04)
                "form": "10-K-derived", "filed": max([fy["filed"]] + [m["filed"] for m in members if m.get("fp") == "Q-ytd-derived"]),
            })

    quarters.sort(key=lambda e: e["end"])
    # 결산일이 10일 안에 겹치는 분기는 하나만 둔다 — 시작일이 다른 연간 행 두 개가 같은 4분기를 두 번 만들었다(PPL 2009-12-31,
    # TAP 2008-12-28/31, Codex·Fable 2026-10-04). 공시 3개월 값을 먼저, 그다음 먼저 나온 값.
    _rank = lambda q: (0 if q.get("fp") not in ("Q4-derived", "Q-ytd-derived") else 1, q["filed"])
    _kept = []
    for q in sorted(quarters, key=lambda e: (e["end"], _rank(e))):
        if _kept and (date.fromisoformat(q["end"]) - date.fromisoformat(_kept[-1]["end"])).days <= 10:
            if _rank(q) < _rank(_kept[-1]):
                _kept[-1] = q
            continue
        _kept.append(q)
    quarters = _kept

    out = []
    for i, q in enumerate(quarters):
        if i < 3:
            continue
        # 네 분기가 1년 안에 있어야 한다 — 분기가 빠지면 마지막 네 행이 1년을 넘겨 틀린 합이 된다(D66, 2026-10-04: PPL·LEN·EMR·TAP)
        if not 240 <= (date.fromisoformat(q["end"]) - date.fromisoformat(quarters[i - 3]["end"])).days <= 300:
            continue
        ttm = round(sum(x["val"] for x in quarters[i - 3:i + 1]), 4)
        out.append({
            "quarter_end": q["end"], "quarter_eps": q["val"], "ttm_eps": ttm,
            "fp": q.get("fp"), "form": q["form"],
            # 누계에서 메운 분기가 들어 있으면 그 분기를 알 수 있게 된 날 뒤로(연간에서 뺀 4분기의 공개일 문제는 그 전부터 있던 것 — 안건 D66 남은 것) — 메운 값이 나중 공시에서 나온 경우(Codex·Fable, 2026-10-04).
            # 보통 분기의 filed는 dedup_for가 고른 행의 날짜라(재작성 비교 수치면 늦다) 전부의 최댓값을 쓰면 ADI 2021 합이 2022-11로 밀려 넣지 않는다.
            "available_date": max([q["filed"]] + [x["filed"] for x in quarters[i - 3:i + 1] if x.get("fp") == "Q-ytd-derived"]),
            "accn": q["accn"],
        })

    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    print(f"{args.ticker}: {len(discrete)} discrete quarters, {len(annual)} annual filings, "
          f"{len(out)} TTM-EPS points written to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
