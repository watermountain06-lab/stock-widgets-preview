#!/usr/bin/env python3
"""v2 카드를 홈 카드로 내보낸다 — v2 재빌드 끝에 돈다(2026-10-07 사용자 결정: 홈 틀은 그대로, 카드·등급·점수만 v2로).

1. v2/{T}_full_widget.html 을 저장소 루트의 {T}_full_widget.html 로 복사한다(홈 링크·이전/다음 링크는 이미 루트 기준이다).
   v2/ 폴더가 원본이고 루트는 내보낸 사본이다 — 루트 카드를 손으로 고치지 않는다.
2. site_data/stocks.json 의 등급(tier)을 v2 판정으로, 점수(score)를 v2 기본적 분석 점수로 바꾼다.
   v2 판정 '적정~고평가'는 홈 7단계 이름 '고평가~적정'으로, '판정 보류'는 등급 없음(missing)으로 둔다.
   v2 점수는 재무건전성·성장·수익성만 본 점수다(밸류에이션 축 제외) — 은행·보험처럼 점수가 없는 카드는 excluded.
3. 등급이 바뀐 종목은 tier_history.json에 'changed'(ruleVersion v2-verdict)로 남긴다.

    python3 pipeline/sync_v2_home.py            # 고친다
    python3 pipeline/sync_v2_home.py --check    # 쓰지 않고, 다르면 종료 코드 1
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2 = ROOT / "v2"
TIER = {"저평가": "저평가", "적정~저평가": "적정~저평가", "적정": "적정", "적정~고평가": "고평가~적정", "고평가": "고평가"}
RULE = "v2-verdict"


def fundamental(T):
    h = (V2 / f"{T}_full_widget.html").read_text(encoding="utf-8")
    k = f"const {T}_FUNDAMENTAL = "
    if k not in h:
        return None
    return json.JSONDecoder().raw_decode(h, h.index(k) + len(k))[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    verd = json.loads(subprocess.run(["node", str(V2 / "research" / "extract_card_verdicts.js")],
                                     capture_output=True, text=True, check=True).stdout)
    sp = ROOT / "site_data" / "stocks.json"
    data = json.loads(sp.read_text(encoding="utf-8"))
    before = json.dumps(data, sort_keys=True)
    hp = ROOT / "site_data" / "tier_history.json"
    hist = json.loads(hp.read_text(encoding="utf-8")) if hp.exists() else []
    changed, copied = [], []
    for t in data["tickers"]:
        T = t["ticker"]
        src = V2 / f"{T}_full_widget.html"
        if not src.exists() or T not in verd:
            sys.exit(f"{T}: v2 카드가 없다 — 홈 목록과 v2 카드가 어긋났다")
        dst = ROOT / f"{T}_full_widget.html"
        if not dst.exists() or dst.read_bytes() != src.read_bytes():
            copied.append(T)
            if not a.check:
                shutil.copyfile(src, dst)
        v = verd[T]
        tier_v = TIER.get(v["verdict"])
        tier = ({"value": tier_v, "raw": v["verdict"], "status": "valid" if tier_v == v["verdict"] else "normalized",
                 "note": "v2 카드 판정(자기 이력·동종업·현금흐름)"} if tier_v else
                {"value": None, "raw": v["verdict"], "status": "missing", "note": "v2 카드 판정 보류"})
        f = fundamental(T) or {}
        if isinstance(f.get("score"), (int, float)):
            score = {"status": "available", "total": f["score"], "grade": f.get("grade"),
                     "financialsAsOf": f.get("asOf"), "valuationAsOf": v.get("date"),
                     "qualityFlags": f.get("qualityFlags") or []}
        else:
            score = {"status": "excluded", "reason": "v2 기본적 분석 점수 없음(" + ", ".join(f.get("qualityFlags") or ["금융"]) + ")"}
        if t.get("tier", {}).get("value") != tier["value"]:
            changed.append((T, t.get("tier", {}).get("value"), tier["value"]))
            entry = {"ticker": T, "evaluatedAt": v.get("date"), "stages": None, "weights": None, "weightedAvg": None,
                     "machineTier": tier["value"], "previousTier": t.get("tier", {}).get("value"),
                     "publishedTier": tier["value"], "decision": "changed", "ruleVersion": RULE}
            same = [e for e in hist if (e["ticker"], e["evaluatedAt"], e["ruleVersion"]) == (T, entry["evaluatedAt"], RULE)]
            if same:   # 같은 날 다시 바뀌면(토요일 비교군 갱신 등) 그날 기록을 고친다 — 날짜·규칙이 키라 두 줄을 둘 수 없다(Codex)
                same[0].update(machineTier=tier["value"], publishedTier=tier["value"])
            else:
                hist.append(entry)
        t["tier"], t["score"], t["cardAsOf"] = tier, score, v.get("date") or t["cardAsOf"]
    data["scoreVersion"] = "v2"
    print(f"카드 복사 {len(copied)}장 · 등급 변경 {len(changed)}")
    for c in changed:
        print("  ", c)
    if a.check:   # 카드·등급만이 아니라 점수·기준일·판정 상태까지 전부(Codex)
        sys.exit(1 if copied or json.dumps(data, sort_keys=True) != before else 0)
    sp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    hp.write_text(json.dumps(hist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
