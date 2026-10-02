#!/usr/bin/env python3
"""v2 카드 한 장을 처음부터 다시 만든다 — 복제 → EPS → 배열 → 재무 → 배수·비교군·기본적 분석·활동성 → 현금흐름 → 채우기 → 검사.

    python3 v2/newcards/build.py WDC            # 전체
    python3 v2/newcards/build.py WDC --data     # 채우기(fill.py) 전까지만 — 새 종목 설정(cfg)을 쓰기 전 숫자 확인용

종목별 내용은 cfg/cfg_{t}.py, 빌드 옵션은 그 안의 BUILD 사전:
  eps_tag  : EPS 태그(분사 종목은 계속사업 EPS — WDC)
  bt_start : 백테스트에 쓸 일봉 시작일(분사 종목 — 재작성 숫자가 처음 나온 날)
  company_tags : [(회사 고유 태그, 표준 태그)] — 설비투자 등을 회사 고유 태그로만 내는 종목(COP)
  overlay  : SEC companyfacts가 최신 10-Q를 아직 싣지 않은 종목 — 인라인 XBRL 보충(adapters/ixbrl_supplement.py) 뒤
             재무는 adapters/overlay_feed.py, 활동성은 병합 facts로
새 종목(71위~)은 meta/{t}.json(헤더 값)과 yahoo/{t}.json(Yahoo 일봉)이 있어야 하고, 없으면 루트 카드가 있는 종목으로 보고
배열을 루트 카드에서 옮긴다(root_arrays.py). 절차·주의점은 이 폴더의 README.md.
"""
import argparse
import importlib.util
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
REDESIGN = os.path.join(os.path.dirname(REPO), "stock-widgets-redesign")
PY = sys.executable


def run(args, show=None, check=True):
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True)
    out = r.stdout + r.stderr
    if show:
        for line in out.splitlines():
            if re.search(show, line):
                print("   ", line[:400])
    if check and r.returncode != 0:
        print(out[-2000:])
        raise SystemExit(f"실패: {' '.join(args[:3])}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ticker")
    ap.add_argument("--data", action="store_true", help="채우기 전까지만")
    ap.add_argument("--asof", default="2026-09-30")
    a = ap.parse_args()
    T = a.ticker.upper(); t = T.lower()
    spec = importlib.util.spec_from_file_location("cfg", os.path.join(HERE, "cfg", f"cfg_{t}.py"))
    if os.path.exists(spec.origin):
        C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
        B, cik = getattr(C, "BUILD", {}), C.CIK
    else:   # 설정을 아직 안 쓴 새 종목(--data 단계) — CIK는 fetch_eps_history 목록에서
        sys.path.insert(0, os.path.join(REPO, "scripts")); import fetch_eps_history as feh
        B, cik = {}, feh.CIKS[T]
    meta, yahoo = os.path.join(HERE, "meta", f"{t}.json"), os.path.join(HERE, "yahoo", f"{t}.json")
    new = os.path.exists(meta)
    card = f"v2/{T}_full_widget.html"

    if B.get("overlay"):
        print("· 인라인 XBRL 보충"); run([PY, "v2/adapters/ixbrl_supplement.py", cik], show=r"보충|저장")
    for ctag, stag in B.get("company_tags", []):   # 회사 고유 태그 → 표준 태그(adapters/company_tag_feed.py, COP 설비투자)
        print(f"· 회사 고유 태그 {ctag} → {stag}"); run([PY, "v2/adapters/company_tag_feed.py", cik, ctag, stag], show=r"저장")
    print("· EPS")
    eps = [PY, "scripts/fetch_eps_history.py", T, "--cik", cik, "--out", f"scripts/{T}_eps_history.json"]
    if B.get("eps_tag"):
        eps[5:5] = ["--tag", B["eps_tag"]]
    run(eps, show=r"TTM-EPS points")
    print("· 복제·배열")
    run([PY, "v2/clone_card.py", T, "--force"] + (["--meta", meta] if new else []))
    if new:
        arr = [PY, "v2/new_ticker_arrays.py", T, "--yahoo", yahoo, "--asof", a.asof]
        if B.get("bt_start"):
            arr += ["--bt-start", B["bt_start"]]
        run(arr, show=r"^arrays|checkpoints")
    else:
        run([PY, os.path.join(HERE, "root_arrays.py"), T], show=r"^arrays")
    print("· 재무")
    if B.get("overlay"):
        run([PY, "v2/adapters/overlay_feed.py", T, cik], show=r"Wrote")
    else:
        run([PY, os.path.join(REDESIGN, "scripts", "fetch_financials.py"), T, "--cik", cik, "--years", "5",
             "--out", f"v2/fundamental_data/{T}_financials.json"], show=r"Wrote")
    print("· 배수·비교군·기본적 분석·활동성")
    env_eps = dict(os.environ, EPS_HISTORY=f"scripts/{T}_eps_history.json")
    r = subprocess.run([PY, "v2/build_multiple_history.py", T, "--json", f"v2/{T}_multiples.json"], cwd=REPO,
                       capture_output=True, text=True, env=env_eps)
    for line in (r.stdout + r.stderr).splitlines():
        if re.search(r"적정주가|^  (PER|PBR|PSR|PCR|EV)|⚠", line):
            print("   ", line[:300])
    run([PY, "v2/build_peer_score.py", T, "--self", f"v2/{T}_multiples.json", "--card"], show=r"대비 =|^  (PER|PBR|PSR|PCR|EV)")
    run([PY, "v2/build_fundamental_score.py", T, "--card"], show=r"기본적 분석 =|^    ")
    if B.get("overlay"):
        merged = f"/tmp/{T}_facts_merged.json"
        sys.path.insert(0, V2); os.chdir(V2)
        import build_multiple_history as bmh
        json.dump(bmh._facts(cik), open(merged, "w")); os.chdir(REPO)
        run([PY, "v2/build_activity_score.py", T, "--facts", merged], show=r'"score"|"reason"')
    else:
        run([PY, "v2/build_activity_score.py", T], show=r'"score"|"reason"')
    print("· 현금흐름")
    run([PY, "v2/build_dcf_block.py", T], show=rf"^{T} |⚠")
    run([PY, "v2/build_dcf_grid.py", T])
    run([PY, "v2/build_dcf_track.py", T, "--json", f"v2/{T}_dcf_track.json"])
    d = json.load(open(os.path.join(V2, f"{T}_dcf_track.json")))
    p = os.path.join(REPO, card); h = open(p, encoding="utf-8").read()
    pts = [f'{{d:"{x["date"]}",low:{round(x["low"], 1)},base:{round(x["base"], 1)},high:{round(x["high"], 1)}}}' for x in d["points"]]
    old = re.search(rf"const {T}_DCF_TRACK = \[.*?\];", h, re.S).group(0)
    h = h.replace(old, f"const {T}_DCF_TRACK = [" + ",".join(pts) + "];", 1)
    open(p, "w", encoding="utf-8").write(h)
    if a.data:
        print("데이터 단계 끝 — cfg/cfg_%s.py를 쓰고 --data 없이 다시 실행" % t)
        return
    print("· 채우기")
    run([PY, os.path.join(HERE, "fill.py"), T], show=r"^ok|^peers")
    run([PY, "v2/sync_fallbacks.py", T], show=r".")
    js = "/tmp/%s_inline.js" % T
    open(js, "w").write("\n;\n".join(re.findall(r"<script>(.*?)</script>", open(p, encoding="utf-8").read(), re.S)))
    run(["node", "--check", js])
    print("JS_OK", card)


if __name__ == "__main__":
    main()
