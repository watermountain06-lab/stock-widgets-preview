#!/usr/bin/env python3
"""v2 시안: 배수의 5년 이력을 재구성해 백분위 기준선을 만든다.

왜 필요한가
-----------
카드의 5단계 평가 테이블은 배수마다 저/적정/고 세 기준선을 갖는데, 적정만
"자체 10년 중앙값"이라는 근거가 있고 저·고는 손으로 놓은 값이다. NVDA의 PER
저 기준선 15x는 5년 동안 한 번도 관측된 적이 없는 값이라(최저 26.5x) 점수를
중간으로 눌러버린다. 기준선 위치에 점수가 크게 흔들리므로, 70장을 한 줄로
세우면 기준선을 후하게 잡은 종목이 위로 간다.

그래서 기준선을 없애고 **그 종목 자신의 5년 배수 분포 안에서의 백분위**를
점수로 쓴다. 정의가 하나뿐이고, 잘리는 구간이 없고, 종목마다 눈금 폭이
달라지는 문제도 생기지 않는다.

미래 정보를 쓰지 않는다
-----------------------
각 거래일의 배수는 그날까지 **공시로 공개돼 있던** 재무제표만으로 계산한다.
SEC XBRL 항목의 `filed` 날짜를 그대로 쓰고, 그보다 나중에 제출된 수치는
그 날짜 이전 구간에 절대 반영하지 않는다.

분할 처리
---------
Yahoo 일봉은 분할이 소급 반영돼 있고 XBRL의 주식수는 당시 보고치라 서로
기준이 다르다. `fetch_eps_history.py`의 분할 표와 같은 규칙으로, 그 공시
이후에 일어난 분할 배수만큼 **주식수를 곱해** 오늘 기준으로 환산한다
(EPS는 같은 이유로 나눈다).

사용법
------
    EPS_HISTORY=scripts/NVDA_eps_history.json python3 v2/build_multiple_history.py NVDA
    EPS_HISTORY=scripts/NVDA_eps_history.json python3 v2/build_multiple_history.py NVDA --json out.json

EPS 이력이 없으면 PER만 빠진 채 계산된다. 만들려면:
    python3 scripts/fetch_eps_history.py NVDA --cik 0001045810 --out scripts/NVDA_eps_history.json
"""
import argparse
import json
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import fetch_eps_history as feh  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fx  # noqa: E402  재무 통화가 달러가 아닌 종목(TSM)의 환율

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

# 배수별로 필요한 XBRL 태그. 앞의 것부터 시도해 데이터가 있는 것을 쓴다.
FLOW_TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
                "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet"],
    "ocf": ["NetCashProvidedByUsedInOperatingActivities",
            "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment",
              "PaymentsToAcquireProductiveAssets"],
}
INSTANT_TAGS = {
    "equity": ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
    "shares": ["CommonStockSharesOutstanding", "EntityCommonStockSharesOutstanding"],
}

# EV/EBITDA
# ---------
# 기업가치의 구성은 친구에게 받은 기관용 모델(Canalyst 형식, BILL·JFrog·NYT)의
# Balance Sheet Summary 블록을 그대로 따른다.
#   Cash      = 현금성자산 + 단기투자
#   Debt      = 차입금 전부(단기·장기·신용공여·전환사채)
#   Net Debt  = Debt + 운용리스부채 - Cash      ← 리스를 부채로 본다
#   EV        = Net Debt + 시가총액 + 비지배지분 + 우선주 + 기타
# 같은 구성요소를 여러 태그가 나눠 담으므로 이쪽은 **합산**한다. 기간 항목처럼
# 중복을 걸러내면 안 된다(그러면 구성요소 하나만 남는다).
EV_COMPONENTS = {
    "cash": ["CashAndCashEquivalentsAtCarryingValue"],
    "sti": ["MarketableSecuritiesCurrent", "DebtSecuritiesCurrent", "ShortTermInvestments",
            "AvailableForSaleSecuritiesDebtSecuritiesCurrent"],
    "debt": ["LongTermDebtCurrent", "LongTermDebtNoncurrent", "ShortTermBorrowings",
             "CommercialPaper", "OtherShortTermBorrowings", "ConvertibleNotesPayableCurrent",
             "ConvertibleNotesPayableNoncurrent"],
    "lease": ["OperatingLeaseLiabilityCurrent", "OperatingLeaseLiabilityNoncurrent"],
    "nci": ["MinorityInterest"],
    # 전환우선주를 다른 태그로 내는 회사가 있다 — GOOGL 6.25% 의무전환 우선주 $18.0B
    # (2026, ConvertiblePreferredStock…). 이 태그를 안 보면 EV와 주당 내재가치에서 빠진다.
    "preferred": ["PreferredStockValue", "ConvertiblePreferredStockNonredeemableOrRedeemableIssuerOptionValue"],
}
# 감가상각은 회사마다 보고 구조가 다르다. NVDA는 합산 태그 하나로 내지만
# MSFT는 Depreciation과 AmortizationOfIntangibleAssets를 따로 낸다. 합산 태그가
# 있으면 그것을 쓰고(구성요소를 또 더하면 이중계상), 없을 때만 구성요소를 더한다.
DDA_COMBINED = ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization",
                "DepreciationAmortizationAndAccretionNet", "DepreciationAmortizationAndOther"]
DDA_PARTS = ["Depreciation", "AmortizationOfIntangibleAssets",
             "FinanceLeaseRightOfUseAssetAmortization"]

EBITDA_TAGS = {
    "opinc": ["OperatingIncomeLoss"],
    # NVDA는 2021-11 이전을 DepreciationAndAmortization으로만 보고했다. 이 태그를
    # 빼면 EV/EBITDA만 5년이 아니라 4년치가 된다(1016일 vs 1255일).
    "dda": ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization",
            "DepreciationAmortizationAndAccretionNet"],
}
# 본업 기준 PER에 쓰는 세율 = 최근 4분기 법인세 ÷ 세전이익 (build_dcf와 같은 정의)
CORE_TAX_TAGS = {
    "tax": ["IncomeTaxExpenseBenefit"],
    "pretax": ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
               "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments"],
}
CORE_EARNINGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "core_earnings.json")


def core_tickers():
    """본업 이익으로 PER을 계산할 종목(v2/core_earnings.json)."""
    if not os.path.exists(CORE_EARNINGS):
        return {}
    return {k: v for k, v in json.load(open(CORE_EARNINGS)).items() if not k.startswith("_")}


# 두 시리즈를 짝지을 때 허용하는 뒤처짐. 한 분기 늦은 보고(약 91일)는 받고,
# 두 분기 이상 비면 버린다.
MAX_PAIR_LAG_DAYS = 200


CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".sec_cache")


def _facts(cik):
    """회사의 XBRL 전체(companyfacts)를 **한 번만** 받아 캐시한다.

    태그마다 companyconcept를 부르면 한 종목에 15~20번을 호출하게 되고, 70장을
    돌리면 SEC가 요청 제한을 건다(검증 중 실제로 429에 막혔다). companyfacts는
    같은 내용을 한 번에 주므로 호출이 1/15로 줄고, 캐시가 있으면 0이 된다.
    새로 받으려면 이 디렉터리의 파일을 지운다.
    """
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{cik}_facts.json")
    if os.path.exists(path):
        try:
            return json.load(open(path))
        except Exception:
            pass
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    try:
        data = feh.curl_json(url)
    except Exception:
        return {}
    if "facts" in data:
        json.dump(data, open(path, "w"))
    return data


def concept(cik, tag, taxonomy="us-gaap"):
    """companyfacts 캐시에서 한 태그의 항목들을 꺼낸다."""
    facts = _facts(cik).get("facts", {}).get(taxonomy, {})
    units = facts.get(tag, {}).get("units", {})
    for key in ("USD", "shares", "USD/shares"):
        if units.get(key):
            return units[key]
    return []


def pick_tag(cik, names, taxonomy="us-gaap"):
    """후보 태그를 **전부 합친다**.

    회사는 같은 항목을 도중에 다른 태그로 옮긴다. NVDA는 매출을
    RevenueFromContractWithCustomerExcludingAssessedTax(2020년까지) →
    Revenues로, 설비투자를 PaymentsToAcquirePropertyPlantAndEquipment(2020년까지)
    → PaymentsToAcquireProductiveAssets로 옮겼다. 첫 번째로 값이 있는 태그만
    쓰면 시리즈가 2020년에 멈춘 채 조용히 낡은 값을 계속 내놓는다
    (그 상태로 PSR이 17.8x 대신 490x로 나왔다).

    같은 기간을 두 태그가 함께 보고하면 먼저 제출된 쪽을 쓴다
    (dedup_earliest_filed와 같은 규칙).
    """
    merged, used = [], []
    for name in names:
        rows = concept(cik, name, taxonomy)
        if rows:
            used.append(f"{name}({len(rows)})")
            merged.extend(rows)
    return ("+".join(used) if used else None), merged


def quarterly_flow(entries, ticker):
    """기간 항목(매출·영업현금흐름·설비투자)을 분기 단위로 환원한다.

    XBRL은 분기(약 90일)와 연간(약 365일)을 섞어 담고 있고, 4분기는 따로
    제출되지 않는 경우가 많아 연간에서 앞 세 분기를 빼서 만든다.
    """
    rows = [e for e in entries if "start" in e and "end" in e and "filed" in e]
    rows = feh.dedup_earliest_filed(rows)
    q = {e["end"]: e for e in rows if 80 <= feh.days_between(e) <= 100}

    # 현금흐름표는 분기가 아니라 회계연도 누계로 보고된다(2분기 10-Q에 6개월
    # 누계가 실린다). 그래서 같은 시작일을 공유하는 누계들을 끝나는 날짜 순으로
    # 세워 앞의 것을 빼면 그 분기 값이 나온다. 이 처리를 빼면 최근 분기가
    # 통째로 사라져 TTM이 한 분기 낡은 채로 계산된다(PCR이 42.5x 대신 58x).
    # 누계끼리만 묶으면 짝이 안 맞는다. 같은 회계연도 시작일을 공유하는 항목을
    # 길이와 무관하게 전부 모아야 3개월 → 6개월 → 9개월로 이어지는 사다리가 생긴다.
    by_start = {}
    for e in rows:
        by_start.setdefault(e["start"], []).append(e)
    for start, group in by_start.items():
        group.sort(key=lambda e: e["end"])
        for prev, cur in zip(group, group[1:]):
            gap = (date.fromisoformat(cur["end"]) - date.fromisoformat(prev["end"])).days
            if 80 <= gap <= 100 and cur["end"] not in q:
                q[cur["end"]] = {
                    "end": cur["end"],
                    "val": cur["val"] - prev["val"],
                    "filed": cur["filed"],
                    "start": prev["end"],
                }

    ann = [e for e in rows if feh.days_between(e) > 350]
    for a in ann:
        end = date.fromisoformat(a["end"])
        parts, cur = [], end
        ok = True
        for _ in range(3):  # 직전 세 분기를 거슬러 찾는다
            prev = None
            for e in q.values():
                d = (cur - date.fromisoformat(e["end"])).days
                if 80 <= d <= 100:
                    prev = e
                    break
            if prev is None:
                ok = False
                break
            parts.append(prev)
            cur = date.fromisoformat(prev["end"])
        if ok and a["end"] not in q:
            q[a["end"]] = {
                "end": a["end"],
                "val": a["val"] - sum(p["val"] for p in parts),
                "filed": a["filed"],
                "start": a["start"],
            }
    return sorted(q.values(), key=lambda e: e["end"])


def ttm_series(quarters, max_span_days=310):
    """분기 값 네 개를 더해 TTM을 만들고, 그 값이 공개된 날짜를 함께 남긴다.

    분기가 빠져 있으면 "네 개"가 1년이 아니라 2년에 걸칠 수 있다. NVDA의
    설비투자가 그랬다 — 표준 태그에 공백이 있어 546일짜리 TTM이 만들어졌고,
    그 앞에서는 27개월 동안 같은 값(1,176M)이 그대로 쓰였다. 창이 1년을 크게
    벗어나면 버린다.

    창은 **첫 분기와 마지막 분기의 결산일 사이**로 잰다. 붙어 있는 4분기는
    그 간격이 3분기, 즉 약 273일이다(분기 길이 84~98일 × 3 = 252~294일).
    문턱이 400일이던 동안에는 한 분기가 통째로 빠져 간격이 약 365일이 돼도
    그대로 통과했다(2026-09-22 Codex 발견 — NVDA capex의 2021-08-01 창이
    2020-07-26·2020-10-25·2021-05-02·2021-08-01로 만들어져 2021년 PCR 이력에
    분기 하나가 빠진 분모가 들어갔다). 310일이면 정상 창은 다 통과하고
    한 분기 누락은 걸린다.

    분기의 `start`로 재면 더 직접적일 것 같지만 그럴 수 없다. 연간에서 앞
    세 분기를 빼 만든 파생 분기는 `start`가 **연간 기간의 시작일**이라 1년
    길이로 잡힌다(그렇게 재면 정상 창까지 30개가 버려졌다).
    """
    out, dropped = [], 0
    for i in range(3, len(quarters)):
        window = quarters[i - 3:i + 1]
        span = (date.fromisoformat(window[-1]["end"]) - date.fromisoformat(window[0]["end"])).days
        if span > max_span_days:
            dropped += 1
            continue
        out.append({
            "end": window[-1]["end"],
            "val": sum(w["val"] for w in window),
            "available": max(w["filed"] for w in window),
        })
    if dropped:
        print(f"    ⚠ 1년을 넘는 TTM 창 {dropped}개 버림 (분기 공백)")
    return sorted(out, key=lambda e: e["available"])


def instant_series(entries, ticker, is_share_count):
    rows = [e for e in entries if "end" in e and "filed" in e and "start" not in e]
    rows = feh.dedup_earliest_filed_instant(rows) if hasattr(feh, "dedup_earliest_filed_instant") else rows
    best = {}
    for e in rows:
        key = e["end"]
        if key not in best or e["filed"] < best[key]["filed"]:
            best[key] = e
    out = []
    splits = feh.KNOWN_SPLITS.get(ticker, [])
    for e in best.values():
        val = e["val"]
        if is_share_count and splits:
            # 이 공시 이후에 일어난 분할만큼 주식수를 오늘 기준으로 늘린다
            val = val * feh.split_ratio(e["filed"], splits)
        out.append({"end": e["end"], "val": val, "available": e["filed"]})
    return sorted(out, key=lambda e: e["available"])


def dda_quarters(cik, ticker):
    """감가상각 분기 시리즈. 합산 태그 우선, 없으면 구성요소를 더한다."""
    tag, rows = pick_tag(cik, DDA_COMBINED)
    if rows:
        return tag, quarterly_flow(rows, ticker)
    # 구성요소마다 그 분기가 **처음 공시된 때**가 다르다. 작은 항목이 1년 뒤 비교
    # 수치로 처음 나오면(GOOGL 무형자산 상각 $0.12B·금융리스 상각 $0.1B), 예전에는
    # 분기 공개일을 가장 늦은 항목 날짜로 잡아 과거 분기 전체가 1년 늦게 "공개"된
    # 셈이 됐고 EV/EBITDA 이력이 44일만 남았다(2026-09-24). 결산 후 LATE_PART_DAYS
    # 안에 공시된 항목만 그 분기에 더한다 — 그때 알 수 없던 값은 빼는 것이 시점 규칙이다.
    LATE_PART_DAYS = 120
    per_end = {}
    used = []
    for name in DDA_PARTS:
        part = concept(cik, name)
        if not part:
            continue
        used.append(name)
        # 판정은 그 분기가 **처음 알려진 날**로 한다 — 같은 결산일로 끝나는 행(3개월이든
        # 누계든) 가운데 가장 이른 공시일. quarterly_flow가 고른 행의 공시일로 판정하면,
        # 제때 누계 차이로 계산됐던 분기가 1년 뒤 비교 수치(직접값)로 다시 실릴 때 지워진다
        # (Codex 지적, 2026-09-24).
        first_known = {}
        for r in part:
            if "filed" in r and "end" in r:
                first_known[r["end"]] = min(first_known.get(r["end"], r["filed"]), r["filed"])
        for e in quarterly_flow(part, ticker):
            known = first_known.get(e["end"], e["filed"])
            if (date.fromisoformat(known) - date.fromisoformat(e["end"])).days > LATE_PART_DAYS:
                continue
            slot = per_end.setdefault(e["end"], {"val": 0.0, "filed": e["filed"]})
            slot["val"] += e["val"]
            slot["filed"] = max(slot["filed"], e["filed"])
    out = [{"end": k, "val": v["val"], "filed": v["filed"], "start": k}
           for k, v in per_end.items()]
    return ("+".join(used) if used else None), sorted(out, key=lambda e: e["end"])


def annual_points(cik, tags, mode="sum"):
    """연 1회만 보고되는 항목을 TTM 시점값으로 만든다.

    MSFT는 2024년 이전 감가상각을 10-K에만 실었다(FY2019 $9.7B 등). 분기가 없어
    `quarterly_flow`가 아무것도 만들지 못하고, 그 결과 감가상각이 무형자산
    상각 $2B만으로 계산돼 EBITDA 마진 이력이 통째로 낮아졌다(매출의 1.5%).
    연간값 자체가 그 시점의 TTM이므로 그대로 쓴다.

    `mode`가 태그 여러 개를 어떻게 합칠지 정한다. 이 구분을 놓치면 조용히
    이중계상된다(2026-09-22에 `dda_ttm`에서 실제로 그랬다).

    - `"sum"` — **구성요소**다. 같은 결산일의 값들을 더한다(감가상각 + 무형자산
      상각처럼 한 줄이 여러 태그로 쪼개진 경우).
    - `"pick"` — **대체 태그**다. 회사가 같은 항목의 이름만 바꾼 것이라 더하면
      안 된다. 같은 결산일을 두 태그가 함께 내면 먼저 제출된 쪽을 쓴다
      (`pick_tag`·`dedup_earliest_filed`와 같은 규칙).
    """
    out = {}
    for tag in tags:
        for e in concept(cik, tag):
            if "start" not in e or "filed" not in e:
                continue
            if not (350 <= days_between_safe(e) <= 380):
                continue
            key = (tag, e["end"])
            if key not in out or e["filed"] < out[key]["filed"]:
                out[key] = e
    merged = {}
    for (tag, end), e in sorted(out.items(), key=lambda kv: kv[1]["filed"]):
        slot = merged.get(end)
        if slot is None:
            merged[end] = {"val": e["val"], "filed": e["filed"]}
        elif mode == "sum":
            slot["val"] += e["val"]
            slot["filed"] = max(slot["filed"], e["filed"])
        # mode == "pick": 먼저 제출된 쪽이 이미 들어가 있다(filed 순 정렬)
    return sorted(({"end": k, "val": v["val"], "available": v["filed"]}
                   for k, v in merged.items()), key=lambda e: e["available"])


def days_between_safe(e):
    try:
        return (date.fromisoformat(e["end"]) - date.fromisoformat(e["start"])).days
    except Exception:
        return -1


def component_sum(cik, tags):
    """구성요소 태그들을 **더해서** 하나의 시점 시리즈로 만든다.

    현금·차입금·리스처럼 한 줄이 여러 태그로 쪼개져 보고되는 항목용이다.
    같은 날짜에 어떤 태그가 없으면 그 항목은 0으로 본다(그 분기에 없었다는 뜻).
    공개 시점은 그 날짜를 구성한 태그들의 제출일 중 가장 늦은 것으로 잡는다.
    """
    per_date = {}
    seen_by_date = {}
    per_tag = {}
    for tag in tags:
        rows = [e for e in concept(cik, tag) if "end" in e and "filed" in e and "start" not in e]
        best = {}
        for e in rows:
            if e["end"] not in best or e["filed"] < best[e["end"]]["filed"]:
                best[e["end"]] = e
        for end, e in best.items():
            slot = per_date.setdefault(end, {"val": 0.0, "filed": e["filed"]})
            slot["val"] += e["val"]
            slot["filed"] = max(slot["filed"], e["filed"])
            seen_by_date.setdefault(end, []).append(tag)
            per_tag.setdefault(tag, {})[end] = e["val"]
    # 총계 태그와 그 세부내역 태그를 함께 보고하는 회사가 있다. 그런 날짜를
    # 그냥 더하면 부채가 두 번 들어간다. 여기서는 고치지 않고 드러내기만 한다 —
    # 어느 쪽이 총계인지는 회사마다 달라 자동 판정이 위험하기 때문이다.
    # 여러 태그가 같은 날짜를 보고하는 것 자체는 정상이다(유동+비유동을 더하는
    # 경우가 그렇다). 위험한 건 **한 태그가 나머지의 합과 같은 경우**다 —
    # 총계와 세부내역을 함께 태깅한 회사이고, 그대로 더하면 두 배가 된다.
    suspicious = []
    for d, tag_list in seen_by_date.items():
        if len(tag_list) < 3:
            continue
        parts = [per_tag[tg][d] for tg in tag_list if d in per_tag.get(tg, {})]
        if len(parts) < 3:
            continue
        biggest = max(parts)
        if abs(biggest - (sum(parts) - biggest)) < 0.01 * max(abs(biggest), 1):
            suspicious.append(d)
    if suspicious:
        print(f"    ⚠ 총계와 세부내역을 함께 보고한 날짜 {len(suspicious)}건"
              f" (예: {sorted(suspicious)[-1]}) — 이중계상 가능")
    return sorted(({"end": k, "val": v["val"], "available": v["filed"]}
                   for k, v in per_date.items()), key=lambda e: e["available"])


# 같은 항목의 **대체 태그**라 더하면 안 되는 EV 구성요소. 날짜마다 앞 태그 우선으로 하나만 쓴다.
# 우선주 총계(PreferredStockValue)와 전환우선주(ConvertiblePreferredStock…)를 함께 내는 회사는
# component_sum으로 더하면 두 배가 된다(Codex 지적, 2026-09-24).
PICK_COMPONENTS = {"preferred"}


def pick_instant(cik, tags):
    """시점값을 태그 목록 순서대로 골라 하나의 시리즈로 — 날짜마다 앞 태그가 우선."""
    per_date = {}
    for tag in tags:
        for e in concept(cik, tag):
            if "end" not in e or "filed" not in e or "start" in e:
                continue
            cur = per_date.get(e["end"])
            if cur is None or (cur["tag"] == tag and e["filed"] < cur["filed"]):
                if cur is None or cur["tag"] == tag:
                    per_date[e["end"]] = {"val": e["val"], "filed": e["filed"], "tag": tag}
    return sorted(({"end": k, "val": v["val"], "available": v["filed"]} for k, v in per_date.items()),
                  key=lambda e: e["available"])


def ev_component(cik, name, tags):
    return pick_instant(cik, tags) if name in PICK_COMPONENTS else component_sum(cik, tags)


def dda_ttm(cik, ticker):
    """감가상각 TTM 시리즈. 태그 구조가 두 갈래라 다루는 법이 다르다.

    - **대체 태그**(`DDA_COMBINED`): 같은 항목의 이름을 회사가 도중에 바꾼 것이다.
      NVDA는 2021-08까지 `DepreciationAndAmortization`으로, 그 뒤로는
      `DepreciationDepletionAndAmortization`으로 낸다. 이것들은 더하는 게 아니라
      **이어붙여야** 한다. `pick_tag`가 이미 한 줄기로 병합하므로 그 결과에서
      TTM을 하나 만든다.
    - **구성요소**(`DDA_PARTS`): 합산 태그가 아예 없는 회사다. MSFT는 무형자산
      상각은 분기로, 감가상각은 2024년까지 연 1회로 보고했다. 한 덩어리로 묶으면
      분기가 있는 쪽만 잡히고 연간만 있는 쪽이 통째로 빠진다(감가상각이 매출의
      1.5%로 나왔던 이유). 각 항목의 시리즈를 따로 만들고 평가 시점마다 더한다.

    2026-09-22 이전에는 이 둘을 구분하지 않고 `DDA_COMBINED`도 전부 더했다.
    NVDA에서 2021-08에 멈춘 옛 태그의 마지막 값 $1.154B이 영구히 더해져 최신
    D&A가 $3.687B 대신 $4.383B로 **18.9% 부풀어 있었다**(Codex 발견). 같은 값이
    EBITDA 마진 → 시나리오 내재가치 → 요구 성장률까지 흘러갔다.
    """
    def with_annuals(series, tags, mode):
        have = {e["end"] for e in series}
        for e in annual_points(cik, tags, mode=mode):
            if e["end"] not in have:
                series.append(e)
        return sorted(series, key=lambda e: (e["available"], e["end"]))

    combined, rows = pick_tag(cik, DDA_COMBINED)
    if rows:
        q = quarterly_flow(rows, ticker)
        series = with_annuals(ttm_series(q) if q else [], DDA_COMBINED, "pick")
        return combined, series

    per_tag = {}
    for tag in DDA_PARTS:
        part = concept(cik, tag)
        if not part:
            continue
        q = quarterly_flow(part, ticker)
        series = with_annuals(ttm_series(q) if q else [], [tag], "sum")
        if series:
            per_tag[tag] = series
    if not per_tag:
        return None, []

    # 평가 시점은 **공시일**이다. 예전에는 `available`에 결산일을 적어두고
    # 결산일로 조회해, 각 구성요소가 한 분기씩 밀린 값으로 더해졌다.
    out = []
    for day in sorted({e["available"] for s in per_tag.values() for e in s}):
        parts = []
        for s in per_tag.values():
            newest = None
            for e in s:
                if e["available"] <= day:
                    newest = e
                else:
                    break
            if newest is not None:
                parts.append(newest)
        if parts:
            out.append({"end": max(e["end"] for e in parts),
                        "val": sum(e["val"] for e in parts),
                        "available": day})
    return "+".join(per_tag), out


def check_fresh(series, last_day, max_lag_days=200):
    """시리즈가 최근 분기까지 닿는지 본다.

    태그 교체를 놓치면 옛 값이 조용히 계속 쓰이므로, 마지막 일봉보다 크게
    뒤처지면 눈에 띄게 표시한다.
    """
    if not series:
        return "  ← 비어 있음"
    lag = (date.fromisoformat(last_day) - date.fromisoformat(series[-1]["end"])).days
    return f"  ← ⚠ {lag}일 뒤처짐" if lag > max_lag_days else ""


def as_of(series, day):
    """그날까지 공개돼 있던 가장 최근 값."""
    val = None
    for e in series:
        if e["available"] <= day:
            val = e["val"]
        else:
            break
    return val


def load_daily(ticker):
    path = os.path.join(REPO, "v2", f"{ticker}_full_widget.html")
    if not os.path.exists(path):
        path = os.path.join(REPO, f"{ticker}_full_widget.html")
    html = open(path).read()
    m = re.search(rf"const {ticker}_DAILY\s*=\s*(\[.*?\]);", html, re.S)
    return json.loads(m.group(1).replace("'", '"'))


def percentile_rank(values, current):
    below = sum(1 for v in values if v < current)
    return below / len(values) * 100


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--json", help="결과를 저장할 경로")
    args = ap.parse_args()
    t = args.ticker.upper()
    cik = feh.CIKS.get(t)
    if not cik:
        sys.exit(f"{t}: CIK를 모른다. fetch_eps_history.py의 CIKS에 추가할 것")

    daily = load_daily(t)
    print(f"{t}: 일봉 {len(daily)}개 ({daily[0][0]} ~ {daily[-1][0]})")

    # EPS는 기존 스크립트가 이미 만든 형식을 그대로 쓴다
    eps_path = os.environ.get("EPS_HISTORY", "")
    eps = []
    if eps_path and os.path.exists(eps_path):
        eps = [{"available": e["available_date"], "val": e["ttm_eps"]}
               for e in json.load(open(eps_path)) if e.get("ttm_eps")]
        eps.sort(key=lambda e: e["available"])

    series = {}
    for name, tags in FLOW_TAGS.items():
        tag, rows = pick_tag(cik, tags)
        if not rows:
            print(f"  {name}: 태그 없음")
            continue
        q = quarterly_flow(rows, t)
        series[name] = ttm_series(q)
        stale = check_fresh(series[name], daily[-1][0])
        print(f"  {name}: {tag} — 분기 {len(q)}개 → TTM {len(series[name])}개"
              f" · 최신 {series[name][-1]['end'] if series[name] else '없음'}{stale}")
    for name, tags in INSTANT_TAGS.items():
        if name == "shares":
            # CommonStockSharesOutstanding은 us-gaap, EntityCommonStockSharesOutstanding은
            # dei에 산다. 둘 다 dei로 조회하면 앞의 것은 영영 안 잡힌다(Codex 지적).
            # 반대로 us-gaap만 쓰면 연 1회 10-K에만 실려 8개월씩 낡는다. 둘은 같은
            # 수량을 다른 곳에서 보고하는 것이므로 **합산이 아니라 병합**한다.
            t1, r1 = pick_tag(cik, ["CommonStockSharesOutstanding"], "us-gaap")
            t2, r2 = pick_tag(cik, ["EntityCommonStockSharesOutstanding"], "dei")
            tag = "+".join(x for x in (t1, t2) if x)
            rows = r1 + r2
        else:
            tag, rows = pick_tag(cik, tags, "us-gaap")
        if not rows:
            print(f"  {name}: 태그 없음")
            continue
        series[name] = instant_series(rows, t, is_share_count=(name == "shares"))
        stale = check_fresh(series[name], daily[-1][0])
        print(f"  {name}: {tag} — 시점 {len(series[name])}개"
              f" · 최신 {series[name][-1]['end'] if series[name] else '없음'}{stale}")

    # EV 구성요소(시점)와 EBITDA(기간)
    for name, tags in EV_COMPONENTS.items():
        series[name] = ev_component(cik, name, tags)
        if series[name]:
            print(f"  {name}: {len(series[name])}개 · 최신 {series[name][-1]['end']}"
                  f"{check_fresh(series[name], daily[-1][0])}")
        else:
            print(f"  {name}: 없음 (0으로 본다)")
    for name, tags in EBITDA_TAGS.items():
        if name == "dda":
            tag, q = dda_quarters(cik, t)
            if not q:
                print("  dda: 태그 없음")
                series[name] = []
                continue
        else:
            tag, rows = pick_tag(cik, tags)
            if not rows:
                print(f"  {name}: 태그 없음")
                series[name] = []
                continue
            q = quarterly_flow(rows, t)
        series[name] = ttm_series(q)
        print(f"  {name}: {tag} — 분기 {len(q)}개 → TTM {len(series[name])}개"
              f" · 최신 {series[name][-1]['end'] if series[name] else '없음'}"
              f"{check_fresh(series[name], daily[-1][0])}")

    core = t in core_tickers()
    if core:
        # 공시 순이익에 투자 평가이익이 크게 섞인 종목은 PER을 본업 이익으로 낸다.
        # GOOGL 2026 Q2: 영업이익 $40.8B, 영업외이익 $98.0B, 희석 EPS $9.11(본업만 약 $2.7).
        for name, tags in CORE_TAX_TAGS.items():
            tag, rows = pick_tag(cik, tags)
            series[name] = ttm_series(quarterly_flow(rows, t)) if rows else []
            print(f"  {name}: {tag} — TTM {len(series[name])}개 (본업 기준 PER용)")

    def core_earnings(d):
        """그날 공개돼 있던 최근 4분기 본업 이익 = 영업이익 × (1 − 법인세/세전이익), 같은 분기끼리."""
        parts = {n: [e for e in series.get(n, []) if e["available"] <= d] for n in ("opinc", "tax", "pretax")}
        if not all(parts.values()):
            return None
        common = set.intersection(*({e["end"] for e in v} for v in parts.values()))
        if not common:
            return None
        end = max(common)
        lead = max(v[-1]["end"] for v in parts.values())
        if (date.fromisoformat(lead) - date.fromisoformat(end)).days > MAX_PAIR_LAG_DAYS:
            return None
        o, tx, pt = ([e for e in parts[n] if e["end"] == end][-1]["val"] for n in ("opinc", "tax", "pretax"))
        if pt <= 0 or o <= 0:
            return None
        return o * (1 - tx / pt)

    out = {"ticker": t, "window": [daily[0][0], daily[-1][0]], "multiples": {},
           "perBasis": "core" if core else "diluted"}
    defs = {
        "PER": (lambda d, px: (mcap(d, px) / core_earnings(d)) if mcap(d, px) and core_earnings(d) else None) if core
        else (lambda d, px: px * fx.rate(t, d) / as_of(eps, d) if eps and as_of(eps, d) and as_of(eps, d) > 0 else None),
        "PSR": lambda d, px: mcap(d, px) / as_of(series.get("revenue", []), d)
        if mcap(d, px) and as_of(series.get("revenue", []), d) else None,
        "PBR": lambda d, px: mcap(d, px) / as_of(series.get("equity", []), d)
        if mcap(d, px) and as_of(series.get("equity", []), d) else None,
        "PCR": lambda d, px: (mcap(d, px) / fcf(d)) if mcap(d, px) and fcf(d) and fcf(d) > 0 else None,
        "EV/EBITDA": lambda d, px: (ev(d, px) / ebitda(d))
        if ev(d, px) and ebitda(d) and ebitda(d) > 0 else None,
    }

    def mcap(d, px):
        # 재무가 현지 통화(TSM 대만달러)면 달러 가격을 그날 환율로 바꿔 같은 통화끼리 나눈다(v2/fx.py).
        sh = as_of(series.get("shares", []), d)
        return px * fx.rate(t, d) * sh if sh else None

    def ev(d, px):
        m = mcap(d, px)
        if not m:
            return None
        cash = (as_of(series.get("cash", []), d) or 0) + (as_of(series.get("sti", []), d) or 0)
        debt = (as_of(series.get("debt", []), d) or 0) + (as_of(series.get("lease", []), d) or 0)
        extra = (as_of(series.get("nci", []), d) or 0) + (as_of(series.get("preferred", []), d) or 0)
        return m + debt - cash + extra

    def ebitda(d):
        o, a = paired("opinc", "dda", d)
        return (o + a) if (o is not None and a is not None) else None

    def paired(name_a, name_b, d):
        """두 시리즈에서 **같은 분기**의 값만 짝지어 돌려준다.

        영업현금흐름은 2분기까지 반영됐는데 설비투자는 1분기에 멈춰 있으면
        그대로 빼도 숫자는 나오지만 서로 다른 기간을 섞은 값이다(Codex 지적).
        """
        ea = [e for e in series.get(name_a, []) if e["available"] <= d]
        eb = [e for e in series.get(name_b, []) if e["available"] <= d]
        if not ea or not eb:
            return None, None
        if ea[-1]["end"] != eb[-1]["end"]:
            # 한쪽이 앞서 있으면 둘 다 가진 가장 최근 분기로 맞춘다
            common = {x["end"] for x in ea} & {x["end"] for x in eb}
            if not common:
                return None, None
            end = max(common)
            # 그 분기가 앞선 쪽의 최신 분기보다 한참 뒤처지면 쓰지 않는다.
            # NVDA는 2021~2023년 10-Q에서 설비투자를 회사 전용 태그(nvda:)로
            # 보고했고 companyfacts는 그 태그를 주지 않는다. 그 동안 짝이 맞는
            # "가장 최근" 분기를 찾다가 2012-10-28까지 거슬러 가서, 10년 전
            # FCF $0.6B를 2021~2024년 주가의 분모로 썼다(PCR 910배, 5년 중앙값
            # 64.97 → 381, 2026-09-23 발견). 그런 날은 값을 내지 않는다.
            lead = max(ea[-1]["end"], eb[-1]["end"])
            if (date.fromisoformat(lead) - date.fromisoformat(end)).days > MAX_PAIR_LAG_DAYS:
                return None, None
            ea = [x for x in ea if x["end"] == end]
            eb = [x for x in eb if x["end"] == end]
        return ea[-1]["val"], eb[-1]["val"]

    def fcf(d):
        o, c = paired("ocf", "capex", d)
        return (o - c) if (o is not None and c is not None) else None

    # 오늘 배수가 없을 때 적자(분모 0 이하)인지 가르는 분모. 본업 PER은 core_earnings가
    # 적자면 None을 돌려 가를 수 없어 넣지 않는다.
    DENOMS = {"PCR": fcf, "EV/EBITDA": ebitda,
              "PSR": lambda d: as_of(series.get("revenue", []), d),
              "PBR": lambda d: as_of(series.get("equity", []), d)}
    if not core:
        DENOMS["PER"] = lambda d: as_of(eps, d) if eps else None

    for label, fn in defs.items():
        pts = []
        for b in daily:
            try:
                v = fn(b[0], b[4])
            except Exception:
                v = None
            if v and v > 0:
                pts.append((b[0], v))
        if not pts:
            print(f"  {label}: 계산 불가")
            continue
        vals = [v for _, v in pts]
        cur = pts[-1][1]
        srt = sorted(vals)
        # 오늘 값이 없으면 마지막 양수 날의 값을 "현재"로 쓰면 안 된다(Codex 지적, 2026-09-24 AMZN:
        # TTM FCF −$11.6B인데 과거 양수일의 PCR 367x가 현재로 실렸다). 오늘 분모가 0 이하면
        # 가장 비싼 것과 같게 0점(사용자 결정, 동종업도 적자를 꼴찌로 센다), 분모 자체를 못 구하면
        # 점수를 내지 않아 평균에서 빠진다.
        stale_note = None
        if pts[-1][0] != daily[-1][0]:
            dfn = DENOMS.get(label)
            dv = dfn(daily[-1][0]) if dfn else None
            stale_note = "negative" if (dv is not None and dv <= 0) else "missing"

        def q(p):
            i = (len(srt) - 1) * p
            lo = int(i)
            hi = min(lo + 1, len(srt) - 1)
            return srt[lo] + (srt[hi] - srt[lo]) * (i - lo)

        pr = percentile_rank(vals, cur)
        if stale_note:
            cur, pr = None, 100.0
        out["multiples"][label] = {
            "days": len(pts), "current": round(cur, 2) if cur is not None else None,
            "min": round(srt[0], 2), "p10": round(q(.10), 2), "median": round(q(.50), 2),
            "p90": round(q(.90), 2), "max": round(srt[-1], 2),
            # 평균도 같이 낸다. 기본적 분석 점수의 밸류에이션 축이 "현재값이 5년
            # 평균에서 몇 % 떨어졌나"로 단계를 매기기 때문이다(build_fundamental_score).
            # 중앙값이 아니라 평균인 것은 그 산식이 그렇게 정의돼 있어서다.
            "mean": round(sum(vals) / len(vals), 2),
            "percentile": round(pr, 1),
            "score": None if stale_note == "missing" else round(100 - pr, 1),
        }
        if stale_note:
            out["multiples"][label]["currentNote"] = stale_note
        if label == "PER" and not stale_note:
            # 적정주가 밴드 — 최근 252거래일 PER의 p25~p75 × 현재 EPS, $10 반올림.
            # EPS_now = P_now / PER_now이므로 현재가 × (분위 PER ÷ 현재 PER)로 같다.
            # (2026-09-24 손값에서 스크립트로. NVDA $260~$370·AAPL $300~$330 재현)
            # 창은 **최근 252거래일**(일봉 날짜 기준)이다. 계산에 성공한 마지막 252개로 잡으면
            # 결측 구간이 있을 때 창이 과거로 늘어난다. 오늘 PER이 없으면 밴드를 내지 않는다(Codex).
            start_day = daily[-252][0] if len(daily) >= 252 else daily[0][0]
            yr = sorted(v for dd, v in pts if dd >= start_day)
            def yq(p):
                i = (len(yr) - 1) * p; lo = int(i); hi = min(lo + 1, len(yr) - 1)
                return yr[lo] + (yr[hi] - yr[lo]) * (i - lo)
            px_now = daily[-1][4]
            lo_px, hi_px = px_now * yq(.25) / cur, px_now * yq(.75) / cur
            out["fairBand"] = {"per_p25": round(yq(.25), 2), "per_p75": round(yq(.75), 2),
                               "low": int(round(lo_px / 10) * 10), "high": int(round(hi_px / 10) * 10),
                               "asOf": daily[-1][0], "basis": out["perBasis"]}
            print(f"  적정주가 밴드: PER {yq(.25):.1f}~{yq(.75):.1f}x → ${out['fairBand']['low']}~${out['fairBand']['high']}"
                  f" ({out['perBasis']})")
        m = out["multiples"][label]
        if stale_note:
            print(f"  {label}: 오늘 값 없음 ({'분모 0 이하 → 0점' if stale_note == 'negative' else '분모를 못 구함 → 평균에서 뺌'})")
            continue
        print(f"  {label}: 현재 {m['current']}  (최저 {m['min']} · 중앙 {m['median']} · 최고 {m['max']})"
              f"  하위 {m['percentile']}%  → 점수 {m['score']}  [{m['days']}일]")

    if args.json:
        json.dump(out, open(args.json, "w"), ensure_ascii=False, indent=1)
        print("저장:", args.json)


if __name__ == "__main__":
    main()
