#!/usr/bin/env python3
"""TSM 어댑터 — TSMC 연결재무제표(6-K, 대만 IFRS)를 SEC companyfacts 모양으로 바꾼다.

왜 필요한가 (2026-09-25)
------------------------
v2 스크립트(배수·기본적 분석·활동성·내재가치)는 전부 SEC companyfacts의 us-gaap 태그를 읽는다.
TSM은 20-F(IFRS)를 내고, companyfacts에는 FY2025 20-F가 2건만 들어가 있으며 분기 XBRL이 없다.
대신 매 분기 6-K에 감사인 검토를 받은 연결재무제표가 HTML로 붙는다(연간은 2월 공시).

무엇을 하는가
-------------
1. 보고서(manifest)마다 tsm_extract로 손익(3개월·누적)·재무상태·현금흐름(누적)을 꺼낸다.
2. 분기별 값을 대만달러로 만든다 — 손익 Q1~Q3는 3개월 값, Q4 = 연간 − 3분기 누적.
   현금흐름은 누적의 차이. 2019 상반기는 분기 보고서가 없어 한 덩어리(H1)로 둔다.
3. 값은 **대만달러 그대로** 둔다(VALUES_CURRENCY). 가격(ADR, 달러)과 만나는 곳 — 배수·내재가치·
   주당 순현금 — 에서 v2/fx.py가 그날 환율을 곱하거나 나눈다. 주식 수·EPS는 **ADR 1주(= 보통주 5주)**.
   (처음에는 분기 평균 환율로 달러 환산했으나 가격의 매일 환율과 섞여 배수가 최대 10% 흔들렸다.)
4. us-gaap 태그 이름·form(10-Q/10-K)·fp·filed로 companyfacts JSON을 써서
   `v2/.sec_cache/0001046179_facts.json`에 둔다. 그러면 v2 스크립트가 그대로 읽는다.

한계
----
- 배수는 ADR 가격 기준이라 ADR 프리미엄(본주 대비 웃돈)이 들어 있고, 그 프리미엄 변동이 자기 이력 백분위에 섞인다.
- 성장률·마진은 대만달러 기준이다(환율 효과 없음).
- 분기 보고서는 대만 IFRS(TIFRS)다. 20-F(국제 IFRS)와 미세하게 다를 수 있다.
- 'filed'는 연결재무제표 6-K 공시일이다. 실적 발표(보통 한 달 앞)보다 늦어 보수적이다.
- 유동 리스부채는 별도 행이 없어 비유동만 잡힌다.

사용법
------
    python3 v2/adapters/tsm_ifrs.py            # manifest의 보고서로 캐시 파일 생성
    python3 v2/adapters/tsm_ifrs.py --refresh  # 최근 6-K에서 새 연결재무제표를 찾아 manifest에 추가
"""
import argparse
import csv
import io
import json
import os
import statistics
import subprocess
import sys
import time
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tsm_extract import extract  # noqa: E402

V2 = os.path.dirname(HERE)
CACHE = os.path.join(V2, ".sec_cache")
REPORTS = os.path.join(CACHE, "tsm_reports")
MANIFEST = os.path.join(HERE, "tsm_manifest.json")
FX_PATH = os.path.join(CACHE, "fx_DEXTAUS.csv")
OUT = os.path.join(CACHE, "0001046179_facts.json")
CIK = "0001046179"
UA = "kim research gptjhss@gmail.com"
ADS_RATIO = 5          # 1 ADS = 보통주 5주 (예전 ADR 조사에서 확인, 출처 기록)
# 값의 통화. "TWD"면 환산하지 않고 대만달러 그대로 둔다(2026-09-25 사용자 결정, Fable 지적 —
# 분기 평균 환율 환산은 가격의 매일 환율과 섞여 배수를 최대 10% 흔들었다). 가격과 만나는 곳의
# 환율은 v2/fx.py가 맡는다. 단위 키는 스크립트 호환을 위해 "USD"로 두지만 값은 대만달러다.
VALUES_CURRENCY = "TWD"

FLOW_TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax"],
    "cogs": ["CostOfRevenue", "CostOfGoodsAndServicesSold"],
    "opinc": ["OperatingIncomeLoss"],
    "pretax": ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest"],
    "tax": ["IncomeTaxExpenseBenefit"],
    "ni": ["NetIncomeLoss"],
    "ni_total": ["ProfitLoss"],
    "fincost": ["InterestExpense"],
    "rd": ["ResearchAndDevelopmentExpense"],
}
CF_TAGS = {
    "ocf": ["NetCashProvidedByUsedInOperatingActivities"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment"],
    "da": ["DepreciationDepletionAndAmortization"],
    "div": ["PaymentsOfDividendsCommonStock"],
}
BS_TAGS = {
    "cash": ["CashAndCashEquivalentsAtCarryingValue"],
    "sti": ["ShortTermInvestments"],
    "ar": ["AccountsReceivableNetCurrent"],
    "inv": ["InventoryNet"],
    "assets": ["Assets"],
    "ca": ["AssetsCurrent"],
    "cl": ["LiabilitiesCurrent"],
    "liab": ["Liabilities"],
    "ap": ["AccountsPayableCurrent"],
    # 단기차입금은 따로 싣지 않고 유동성 장기부채와 합쳐 LongTermDebtCurrent·DebtCurrent 두 태그로 싣는다.
    # fetch_financials는 단기부채 태그를 ShortTermBorrowings부터 찾는데, 0짜리 행이 있으면 거기서 멈춰
    # 유동성 장기부채(2026 Q2 NT$1,674억)를 놓쳤다. build_multiple_history는 DebtCurrent를 읽지 않아 이중 계산이 없다.
    "cur_debt": ["LongTermDebtCurrent", "DebtCurrent"],
    "ltd_non": ["LongTermDebtNoncurrent"],
    "lease": ["OperatingLeaseLiabilityNoncurrent"],
    "equity": ["StockholdersEquity"],
    "nci": ["MinorityInterest"],
    "lti": ["LongTermInvestments"],
}
QEND = {1: "03-31", 2: "06-30", 3: "09-30", 4: "12-31"}
QSTART = {1: "01-01", 2: "04-01", 3: "07-01", 4: "10-01"}


def curl(url, out=None):
    args = ["curl", "-s", "-A", UA, url] + (["-o", out] if out else [])
    r = subprocess.run(args, capture_output=True, check=True)
    return r.stdout


def load_fx():
    if not os.path.exists(FX_PATH) or (date.today() - date.fromtimestamp(os.path.getmtime(FX_PATH))).days > 1:
        os.makedirs(CACHE, exist_ok=True)
        data = curl("https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXTAUS")
        open(FX_PATH, "wb").write(data)
    fx = {}
    for row in csv.DictReader(io.StringIO(open(FX_PATH).read())):
        v = row.get("DEXTAUS")
        if v and v != ".":
            fx[row["observation_date"]] = float(v)
    return fx


def fx_avg(fx, start, end):
    if VALUES_CURRENCY == "TWD":
        return 1.0
    vals = [v for d, v in fx.items() if start <= d <= end]
    if not vals:
        raise SystemExit(f"환율 없음: {start}~{end}")
    return statistics.mean(vals)


def fx_end(fx, end):
    if VALUES_CURRENCY == "TWD":
        return 1.0
    ds = [d for d in fx if d <= end]
    return fx[max(ds)]


def refresh_manifest():
    """최근 6-K에서 1.5MB 넘는 htm(연결재무제표)을 찾아 manifest에 추가한다."""
    man = json.load(open(MANIFEST))
    last = max(m["filed"] for m in man)
    sub = json.loads(curl(f"https://data.sec.gov/submissions/CIK{CIK}.json"))["filings"]["recent"]
    for i, f in enumerate(sub["form"]):
        d, acc = sub["filingDate"][i], sub["accessionNumber"][i]
        if f != "6-K" or d <= last:
            continue
        idx = json.loads(curl(f"https://www.sec.gov/Archives/edgar/data/1046179/{acc.replace('-', '')}/index.json"))
        big = [it["name"] for it in idx.get("directory", {}).get("item", [])
               if it["name"].lower().endswith(".htm") and int(it.get("size") or 0) > 1_500_000
               and "uncons" not in it["name"].lower() and "standalone" not in it["name"].lower()]
        if big:
            man.append({"filed": d, "accn": acc, "file": f"{d}_{sorted(big)[0]}",
                        "url": f"https://www.sec.gov/Archives/edgar/data/1046179/{acc.replace('-', '')}/{sorted(big)[0]}"})
            print("추가:", d, acc, sorted(big)[0])
        time.sleep(0.2)
    man.sort(key=lambda m: m["filed"])
    json.dump(man, open(MANIFEST, "w"), indent=1)


def ensure_reports(man):
    os.makedirs(REPORTS, exist_ok=True)
    for m in man:
        p = os.path.join(REPORTS, m["file"])
        if not os.path.exists(p):
            curl(m["url"], p)
            time.sleep(0.3)


def build():
    man = json.load(open(MANIFEST))
    ensure_reports(man)
    fx = load_fx()
    rep = {}
    for m in man:
        r = extract(os.path.join(REPORTS, m["file"]))
        if r["missing"]:
            raise SystemExit(f"{m['file']}: 항목 누락 {r['missing']}")
        r["filed"], r["accn"] = m["filed"], m["accn"]
        rep[(int(r["end"][:4]), r["kind"])] = r

    facts = {}

    def add(tag, unit, row):
        facts.setdefault(tag, {"units": {}})["units"].setdefault(unit, []).append(row)

    years = sorted({y for y, _ in rep})
    for y in years:
        q = {k: rep.get((y, k)) for k in ("Q1", "Q2", "Q3", "FY")}
        # ── 손익: 분기 3개월 값(대만달러) ──
        disc = {}          # 분기 번호 → {key: twd}
        for n, k in ((1, "Q1"), (2, "Q2"), (3, "Q3")):
            if q[k]:
                disc[n] = dict(q[k]["is3"])
        h1 = None
        if q["Q3"] and not (q["Q1"] and q["Q2"]):
            # 2019: 1·2분기 보고서가 없다 → 상반기 = 3분기 누적 − 3분기 3개월(한 덩어리)
            h1 = {k: q["Q3"]["isy"][k] - q["Q3"]["is3"][k] for k in q["Q3"]["isy"]}
        if q["FY"] and q["Q3"]:
            disc[4] = {k: q["FY"]["isy"][k] - q["Q3"]["isy"][k] for k in q["FY"]["isy"]}
        # ── 현금흐름: 누적의 차이 ──
        cf_disc = {}
        prev = None
        for n, k in ((1, "Q1"), (2, "Q2"), (3, "Q3"), (4, "FY")):
            cur = q[k]["cfy"] if q[k] else None
            if cur is not None:
                if n == 1:
                    cf_disc[1] = dict(cur)
                elif prev is not None:
                    cf_disc[n] = {kk: cur[kk] - prev[kk] for kk in cur}
            prev = cur if cur is not None else None
        cf_h1 = None
        if q["Q3"] and not q["Q2"]:
            cf_h1 = "ytd9"          # 2019: 3분기 누적을 한 덩어리로(아래에서 9개월 평균 환율)

        # ── 달러 환산 ──
        def conv_flows(dct, rate):
            out = {k: (v / rate if v is not None else None) for k, v in dct.items()
                   if k not in ("eps_d", "eps_b")}
            for e in ("eps_d", "eps_b"):
                if e in dct and dct[e] is not None:
                    out[e] = dct[e] * ADS_RATIO / rate
            return out

        usd, rate = {}, {}
        for n, d in disc.items():
            rate[n] = fx_avg(fx, f"{y}-{QSTART[n]}", f"{y}-{QEND[n]}")
            usd[n] = conv_flows(d, rate[n])
        h1_usd = conv_flows(h1, fx_avg(fx, f"{y}-01-01", f"{y}-06-30")) if h1 else None
        cf_usd = {n: {k: v / fx_avg(fx, f"{y}-{QSTART[n]}", f"{y}-{QEND[n]}") for k, v in d.items()}
                  for n, d in cf_disc.items()}
        cf9 = None
        if cf_h1 and q["Q3"]:
            cf9 = {k: v / fx_avg(fx, f"{y}-01-01", f"{y}-09-30") for k, v in q["Q3"]["cfy"].items()}

        def meta(k, n_end, start, form, fp):
            r = q[k]
            return {"start": start, "end": f"{y}-{QEND[n_end]}", "accn": r["accn"], "fy": y,
                    "fp": fp, "form": form, "filed": r["filed"]}

        # 3개월 행(Q1~Q3)과 누적 행(Q2·Q3), 연간 행
        for key, tags in FLOW_TAGS.items():
            for n, k in ((1, "Q1"), (2, "Q2"), (3, "Q3")):
                if n in usd and q[k] and usd[n].get(key) is not None:
                    for tg in tags:
                        add(tg, "USD", {**meta(k, n, f"{y}-{QSTART[n]}", "10-Q", k), "val": usd[n][key]})
                # 누적(1월 1일부터)
                if n >= 2 and q[k]:
                    parts = [usd.get(i, {}).get(key) for i in range(1, n + 1)]
                    if all(p is not None for p in parts):
                        ytd = sum(parts)
                    elif h1_usd and n == 3 and usd.get(3, {}).get(key) is not None:
                        ytd = h1_usd[key] + usd[3][key]
                    else:
                        continue
                    for tg in tags:
                        add(tg, "USD", {**meta(k, n, f"{y}-01-01", "10-Q", k), "val": ytd})
            if q["FY"] and 4 in usd:
                parts = [usd.get(i, {}).get(key) for i in (1, 2, 3, 4)]
                if all(p is not None for p in parts):
                    fy = sum(parts)
                elif h1_usd and all(usd.get(i, {}).get(key) is not None for i in (3, 4)):
                    fy = h1_usd[key] + usd[3][key] + usd[4][key]
                else:
                    fy = None
                if fy is not None:
                    for tg in tags:
                        add(tg, "USD", {**meta("FY", 4, f"{y}-01-01", "10-K", "FY"), "val": fy})
        # EPS (ADR 1주, USD). 1·2분기가 없는 해(2019)는 싣지 않는다 — fetch_eps_history가 Q4를
        # "연간 − 1~3분기"로 만들기 때문에, 일부 분기만 있으면 TTM이 엉뚱한 분기를 묶는다(Codex:
        # 2020 Q3 TTM이 2019 Q4 대신 2019 Q3를 넣어 3.06, 맞는 값 3.17).
        eps_ok = q["Q1"] is not None      # 1분기 보고서가 없는 해(2019)만 뺀다. 진행 중인 해(2026)는 둔다
        for key, tag in (("eps_d", "EarningsPerShareDiluted"), ("eps_b", "EarningsPerShareBasic")) if eps_ok else ():
            for n, k in ((1, "Q1"), (2, "Q2"), (3, "Q3")):
                if n in usd and q[k]:
                    add(tag, "USD/shares", {**meta(k, n, f"{y}-{QSTART[n]}", "10-Q", k), "val": round(usd[n][key], 4)})
            if q["FY"] and 4 in usd:
                parts = [usd.get(i, {}).get(key) for i in (1, 2, 3, 4)]
                fy = sum(parts) if all(p is not None for p in parts) else (
                    h1_usd[key] + usd[3][key] + usd[4][key] if h1_usd else None)
                if fy is not None:
                    add(tag, "USD/shares", {**meta("FY", 4, f"{y}-01-01", "10-K", "FY"), "val": round(fy, 4)})
        # 현금흐름: 누적 행(US 10-Q처럼 누적만) + 연간
        for key, tags in CF_TAGS.items():
            src = "da" if key == "da" else key
            for n, k in ((1, "Q1"), (2, "Q2"), (3, "Q3"), (4, "FY")):
                if not q[k]:
                    continue
                parts = []
                for i in range(1, n + 1):
                    d = cf_usd.get(i)
                    parts.append(None if d is None else (d["dep"] + d["amort"] if src == "da" else d[src]))
                if all(p is not None for p in parts):
                    ytd = sum(parts)
                elif cf9 is not None and n >= 3 and all(cf_usd.get(i) is not None for i in range(4, n + 1)):
                    base9 = cf9["dep"] + cf9["amort"] if src == "da" else cf9[src]
                    ytd = base9 + sum((cf_usd[i]["dep"] + cf_usd[i]["amort"] if src == "da" else cf_usd[i][src])
                                      for i in range(4, n + 1))
                else:
                    continue
                form, fp = ("10-K", "FY") if k == "FY" else ("10-Q", k)
                for tg in tags:
                    add(tg, "USD", {**meta(k, n, f"{y}-01-01", form, fp), "val": ytd})
        # 재무상태표: 기말 환율, 주식 수는 ADR 기준
        for n, k in ((1, "Q1"), (2, "Q2"), (3, "Q3"), (4, "FY")):
            r = q[k]
            if not r:
                continue
            end = f"{y}-{QEND[n]}"
            rt = fx_end(fx, end)
            form, fp = ("10-K", "FY") if k == "FY" else ("10-Q", k)
            base = {"end": end, "accn": r["accn"], "fy": y, "fp": fp, "form": form, "filed": r["filed"]}
            bsv = dict(r["bs"], cur_debt=r["bs"]["st_debt"] + r["bs"]["ltd_cur"])
            for key, tags in BS_TAGS.items():
                for tg in tags:
                    add(tg, "USD", {**base, "val": bsv[key] / rt})
            add("CommonStockSharesOutstanding", "shares", {**base, "val": r["bs"]["shares"] / ADS_RATIO})

    shares = facts.pop("CommonStockSharesOutstanding")
    out = {"cik": int(CIK), "entityName": "TAIWAN SEMICONDUCTOR MANUFACTURING CO LTD (v2 adapter)",
           "facts": {"us-gaap": {**facts, "CommonStockSharesOutstanding": shares},
                     "dei": {"EntityCommonStockSharesOutstanding": shares}},
           "_adapter": {"source": "TSMC consolidated financial statements (6-K, TIFRS)",
                        "fx": "FRED DEXTAUS (Fed H.10)", "adsRatio": ADS_RATIO,
                        "valuesCurrency": VALUES_CURRENCY,
                        "reports": len(man), "built": date.today().isoformat()}}
    os.makedirs(CACHE, exist_ok=True)
    json.dump(out, open(OUT, "w"))
    print(f"저장: {OUT} — 보고서 {len(man)}건, 태그 {len(facts) + 1}개")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    if a.refresh:
        refresh_manifest()
    build()
