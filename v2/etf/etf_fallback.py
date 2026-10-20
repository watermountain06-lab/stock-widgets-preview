#!/usr/bin/env python3
"""ETF 대체 단계 — etf_daily.py가 아예 돌지 못한 날(import 오류 등) 세 산출물을 "판정 보류"로 쓴다.

워크플로 v2_cards.yml에서 ETF 단계가 실패했을 때만 돈다. 표준 라이브러리만 쓰고 etf_daily.py를 import하지 않는다
(그 파일이 깨진 경우를 위해). 화면 문구는 v2/etf/template를 쓰지 않는 최소 페이지다.

    python3 v2/etf/etf_fallback.py [--etf SPY] [--out-root DIR]
"""
import argparse
import html
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REASON = "run_fail"
REASON_TEXT = "ETF 스크립트 실행 실패"
# etf_daily.py CHECK_KEYS와 같은 목록(그 파일을 import하지 않으므로 여기 다시 적는다)
CHECK_KEYS = ("status", "reason", "verdict", "nbar", "coverage", "range", "bar", "S", "builtFor", "ruleVersion", "pending")
CHECK_KINDS = ("fetch", "input", "file_date", "tools", "code_sig", "sig_err", "structure", "unclassified", "run")


def write_atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--etf", default="SPY")
    ap.add_argument("--out-root", default=str(ROOT))
    a = ap.parse_args()
    etf, out = a.etf, Path(a.out_root)
    try:
        P = json.loads((ROOT / "site_data" / "stocks.json").read_text(encoding="utf-8"))["priceSession"]
    except Exception:
        P = None   # 홈 JS는 builtFor가 없으면 묵음으로 그린다
    res = {"etf": etf, "status": "held", "reason": REASON, "reasonText": REASON_TEXT, "verdict": None, "nbar": None,
           "coverage": None, "range": None, "edgeNear": False, "bar": None, "S": None, "builtFor": P,
           "ruleVersion": None, "top10": [], "runAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "detail": "etf_daily.py가 끝까지 돌지 못했다 — Actions 로그를 본다", "pending": None,
           "evaluation": {"status": "held", "holds": [REASON], "S": None},
           "checks": dict({k: "unchecked" for k in CHECK_KINDS}, run="bad"), "checkDetail": {}}
    summary = {k: res[k] for k in ("etf", "status", "reason", "reasonText", "verdict", "nbar", "coverage", "range",
                                   "edgeNear", "bar", "S", "builtFor", "ruleVersion")}
    summary["top"] = []
    write_atomic(out / "v2" / "etf" / f"{etf}.json", json.dumps(res, ensure_ascii=False, indent=1) + "\n")
    d = out / "preview-only-etf-data.js"
    try:   # 다른 ETF 칸은 그대로 둔다(깨졌으면 새로)
        txt = d.read_text(encoding="utf-8")
        data = json.loads(txt[txt.index("window.ETF_DATA = ") + len("window.ETF_DATA = "):].rstrip().rstrip(";"))
        if not isinstance(data, dict):
            data = {}
    except Exception:
        data = {}
    data[etf] = summary
    write_atomic(d, "// preview 전용 ETF 요약(etf_fallback.py가 썼다)\n"
                 f"window.ETF_DATA = {json.dumps(data, ensure_ascii=False)};\n")
    write_atomic(out / f"preview-only-etf-{etf.lower()}.html",
                 '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
                 '<meta name="viewport" content="width=device-width, initial-scale=1">'
                 f'<title>{etf} ETF 판정</title><style>body{{margin:0;background:#f7f5ef;color:#1f2420;'
                 'font-family:system-ui,sans-serif}main{max-width:900px;margin:0 auto;padding:28px 16px}</style></head>'
                 f'<body><main data-status="held" data-etf="{html.escape(json.dumps({k: res[k] for k in CHECK_KEYS}, ensure_ascii=False), quote=True)}">'
                 f'<a href="index.html">← 홈</a><h1>{etf}</h1>'
                 f'<p>판정 보류 · {REASON_TEXT}. 카드 판정 세션 {P or "—"}.</p></main></body></html>\n')
    try:   # 관측 한 줄(알림의 "이어짐" 판정이 이 실행도 세게)
        with open(out / "v2" / "etf" / "date_obs.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({"etf": etf, "run_id": os.environ.get("GITHUB_RUN_ID"), "attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
                                "at": res["runAt"], "P": P, "S": None, "file_sha12": None, "eval": "held", "holds": [REASON],
                                "kept": None, "pending": None}, ensure_ascii=False, sort_keys=True) + "\n")
    except Exception:
        pass
    print(f"ETF_FAIL ETF {etf}: 대체 단계가 보류 산출물을 썼다 (P={P})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
