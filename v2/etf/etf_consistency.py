#!/usr/bin/env python3
"""ETF 산출물 대조 단계(2026-10-21, QQQ 설계 dr r2·r3) — 카드 단계(index_daily.py --card)가 판정 페이지를 덮어쓴 뒤,
커밋 전에 ETF마다 세 산출물(v2/etf/<ETF>.json · 홈 데이터 preview-only-etf-data.js의 그 칸 · 최종 페이지
preview-only-etf-<etf>.html의 data-etf)이 같은 판정 칸(etf_daily.CHECK_KEYS)을 갖는지 본다.

어긋나면 그 ETF만 "자체 검사 불일치" 보류 하나로 JSON·홈 칸을 다시 쓰고, 카드 페이지는 시세 부분을 그대로 두고 판정 탭만
같은 보류로 바꿔 끼운 다음(카드 판정 탭이 없는 페이지면 판정 페이지) **다시 대조**한다. 관측 기록 한 줄(holds selfcheck — 알림 run 종류)은
다시 쓰기 전에 남긴다.
다시 대조해도 어긋나거나 다시 쓰기가 실패하면 종료 코드 1 — 워크플로는 커밋·게시를 건너뛴다(다음 실행이 다시 평가).

    python3 v2/etf/etf_consistency.py --etf SPY,QQQ
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import etf_daily as D  # noqa: E402

ROOT = HERE.parents[1]


def paths(out, etf):
    return (out / "v2" / "etf" / f"{etf}.json", out / f"preview-only-etf-{etf.lower()}.html", out / "preview-only-etf-data.js")


def check(out, etf):
    j, h, d = paths(out, etf)
    try:
        res = json.loads(j.read_text(encoding="utf-8"))
    except Exception as ex:   # noqa: BLE001
        return None, [f"{etf}.json 읽기 실패 {type(ex).__name__}"]
    return res, D.consistency(res, (j, h, d))


def splice_card(html_path, etf, res, P):
    """카드 페이지의 판정 탭만 res로 다시 그려 바꿔 끼운다(시세 부분은 그대로 — 다시 받지 않는다, QQQ 구현 dr r1).
    카드 판정 탭이 없는 페이지(판정만 있는 페이지)면 False — write_outputs가 쓴 판정 페이지를 그대로 둔다."""
    sys.path.insert(0, str(ROOT / "v2" / "index"))
    import index_daily as ix   # noqa: E402
    page = html_path.read_text(encoding="utf-8") if html_path.exists() else ""
    a = page.find('<div id="verdict" class="section"')
    b = page.find("<!-- DISCLAIMER", a)
    if a < 0 or b < 0 or etf not in ix.PROFILES or not page[a:b].rstrip().endswith("</div>"):
        return False   # 경계가 예상과 다르면(틀이 바뀜) 바꿔 끼우지 않고 판정 페이지로
    ix.use_profile(etf)
    block = f'<div id="verdict" class="section" data-etf="{ix.verdict_attr(res)}">\n{ix.render_verdict(res, P)}\n</div>\n\n'
    D.write_atomic(html_path, page[:a] + block + page[b:])
    return True


def repair(out, etf, errs, card_page):
    """보류 하나로 세 곳을 다시 쓴다. 성공하면 True. 관측 한 줄은 다시 쓰기 전에 남긴다(실패해도 run 종류로 알리게)."""
    try:
        cfg = json.loads(D.CFG_PATH.read_text(encoding="utf-8"))
        P = json.loads((out / "site_data" / "stocks.json").read_text(encoding="utf-8"))["priceSession"]
    except Exception:   # noqa: BLE001
        cfg, P = None, None
    res = D.held(etf, cfg, "selfcheck", "대조 단계: " + "; ".join(errs)[:300], P)
    run_at = D.now_utc()
    res.update(ruleVersion=(cfg or {}).get("ruleVersion"), dateRule=(cfg or {}).get("dateRule"), runAt=run_at, fetchedAt=None,
               inputHash={}, pending=None, evaluation={"status": "held", "holds": ["selfcheck"], "S": None},
               checks=dict({k: "unchecked" for k in D.CHECK_KINDS}, run="bad"), checkDetail={}, runId=D.run_id())
    try:
        D.append_obs(out / "v2" / "etf" / "date_obs.jsonl", {
            "etf": etf, "run_id": os.environ.get("GITHUB_RUN_ID"), "attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "at": run_at, "P": P, "S": None, "file_sha12": None, "eval": "held", "holds": ["selfcheck"], "kept": None, "pending": None})
    except Exception as ex:   # noqa: BLE001
        print(f"ETF_FAIL 대조 {etf}: 관측 기록 실패 {type(ex).__name__}")
    h = paths(out, etf)[1]
    try:
        old = h.read_text(encoding="utf-8") if h.exists() else None
        D.write_outputs(res, out, etf)   # JSON·홈 칸·판정 페이지
        if old is not None:   # 카드 페이지였으면 되돌려 놓고 판정 탭만 바꿔 끼운다
            D.write_atomic(h, old)
            if not card_page(h, etf, res, P):
                D.write_atomic(h, D.render_html(res))
    except Exception as ex:   # noqa: BLE001
        print(f"ETF_FAIL 대조 {etf}: 다시 쓰기 실패 {type(ex).__name__}")
        return False
    return True


def run(out, etfs, card_page=splice_card):
    bad, why = 0, []
    for etf in etfs:
        res, errs = check(out, etf)
        if not errs:
            print(f"대조 {etf}: 세 산출물 같음")
            continue
        print(f"ETF_FAIL 대조 {etf}: {'; '.join(errs)} — 보류로 다시 쓴다")
        if not repair(out, etf, errs, card_page):
            bad += 1
            why.append(f"{etf}: 다시 쓰기 실패")
            continue
        _, errs2 = check(out, etf)
        if errs2:
            print(f"ETF_FAIL 대조 {etf}: 다시 쓴 뒤에도 불일치 — {'; '.join(errs2)}")
            bad += 1
            why.append(f"{etf}: 다시 쓴 뒤에도 불일치({'; '.join(errs2)[:200]})")
    if os.environ.get("GITHUB_STEP_SUMMARY") and bad:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(f"- 대조 단계 실패 — 이번 실행은 커밋·게시하지 않는다: {' / '.join(why)}\n")
    return 1 if bad else 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--etf", default="SPY,QQQ,DIA")
    ap.add_argument("--out-root", default=str(ROOT))
    a = ap.parse_args(argv)
    return run(Path(a.out_root), [e.strip() for e in a.etf.split(",") if e.strip()])


if __name__ == "__main__":
    sys.exit(main())
