#!/usr/bin/env python3
"""v2 카드 한 장을 처음부터 다시 만든다 — 복제 → EPS → 배열 → 재무 → 배수·비교군·기본적 분석·활동성 → 현금흐름 → 채우기 → 검사.

    python3 v2/newcards/build.py WDC            # 전체
    python3 v2/newcards/build.py WDC --data     # 채우기(fill.py) 전까지만 — 새 종목 설정(cfg)을 쓰기 전 숫자 확인용

종목별 내용은 cfg/cfg_{t}.py, 빌드 옵션은 그 안의 BUILD 사전:
  eps_tag  : EPS 태그(분사 종목은 계속사업 EPS — WDC)
  bt_start : 백테스트에 쓸 일봉 시작일(분사 종목 — 재작성 숫자가 처음 나온 날)
  company_tags : [(회사 고유 태그, 표준 태그)] — 설비투자 등을 회사 고유 태그로만 내는 종목(COP)
  no_dcf   : 현금흐름 모델 미적용 사유(보험사 — CB). DCF 칸은 '계산 불가 · 사유', 판정은 두 칸으로
  feed     : 외국 기업(IFRS·현지 통화 — ASML·TSM·SKHY) — EPS·재무를 v2/adapters/{t}_feed.py(eps|financials)로, 활동성은 그 캐시 facts로
  eps_cmd  : EPS 단계를 다른 명령으로(주식 종류별 EPS만 내는 V — ['v2/adapters/visa_classA.py', 'eps'])
  share_events : 분기 뒤 주식 발행을 '주식 + 순수입금'으로 오버레이에(adapters/share_events.py, v2/share_events.json — INTC)
  sum_tags : 재무 파일 항목을 여러 태그 합으로 다시 채운 뒤 기본적 분석(adapters/financials_sum_tags.py — XOM 재고)
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
    ap.add_argument("--sync-base", default=None, help="sync_fallbacks에 넘길 http 서버 주소(복제본에서 돌릴 때 — 기본 8765)")
    ap.add_argument("--from-card", action="store_true",
                    help="재현 모드 — 배열을 루트 카드가 아니라 지금 v2 카드의 사본에서 옮긴다(가격·날짜가 그 카드와 같다, 2026-10-05)")
    ap.add_argument("--price", action="store_true",
                    help="매일 가격 재빌드(2026-10-06) — 지금 카드에 새 종가를 붙여(price_arrays.py) 그 배열로 다시 만든다. "
                         "SEC·EPS·재무는 받지 않고(캐시·이전 파일), 내재가치 추적선은 지금 카드의 것을 그대로 둔다")
    ap.add_argument("--weekly", action="store_true",
                    help="토요일 전체 재빌드(2026-10-06) — 배열은 --price와 같이 지금 카드 + 새 종가, 자료(SEC·EPS·재무·추적선)는 모두 새로")
    a = ap.parse_args()
    if a.weekly:
        a.price = True
    net = not a.price or a.weekly   # 자료를 새로 받는가(전체·토요일) — 매일 가격 재빌드만 False
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
    WORK = os.path.join(REPO, "v2", ".sec_cache", "_work"); os.makedirs(WORK, exist_ok=True)   # 저장소 안(gitignore) — /tmp는 체크아웃끼리 겹친다(Codex 2026-10-06)
    if a.price:   # 지금 카드를 떠서 새 종가를 붙이고, 그 사본을 배열 원본으로 쓴다(--from-card와 같은 길)
        a.from_card = True
        src = os.path.join(WORK, f"{T}_from_card.html")
        open(src, "w", encoding="utf-8").write(open(os.path.join(REPO, card), encoding="utf-8").read())
        print("· 새 종가")
        run([PY, os.path.join(HERE, "price_arrays.py"), T, "--card", src], show=r".")
        a.asof = re.findall(r'\["(\d{4}-\d{2}-\d{2})",', re.search(rf"const {T}_DAILY\s*=\s*(\[.*?\]);", open(src, encoding="utf-8").read()).group(1))[-1]
        track_old = re.search(rf"const {T}_DCF_TRACK = \[.*?\];", open(src, encoding="utf-8").read(), re.S).group(0)

    if B.get("overlay") and net:
        print("· 인라인 XBRL 보충"); run([PY, "v2/adapters/ixbrl_supplement.py", cik], show=r"보충|저장")
    if B.get("share_events") and net:   # v2.1 D-1(2026-10-05)
        print("· 분기 뒤 주식 발행 이벤트"); run([PY, "v2/adapters/share_events.py", T], show=r".")
    for ctag, stag in (B.get("company_tags", []) if net else []):   # 회사 고유 태그 → 표준 태그(adapters/company_tag_feed.py, COP 설비투자)
        print(f"· 회사 고유 태그 {ctag} → {stag}"); run([PY, "v2/adapters/company_tag_feed.py", cik, ctag, stag], show=r"저장")
    print("· EPS")
    eps = [PY, "scripts/fetch_eps_history.py", T, "--cik", cik, "--out", f"scripts/{T}_eps_history.json"]
    if B.get("eps_tag"):
        eps[5:5] = ["--tag", B["eps_tag"]]
    if B.get("feed"):   # 외국 기업 어댑터(2026-10-05, 틀 통일 — ASML·TSM·SKHY)
        eps = [PY, f"v2/adapters/{t}_feed.py", "eps"]
    elif B.get("eps_cmd"):
        eps = [PY] + list(B["eps_cmd"])
    if net:
        run(eps, show=r"TTM-EPS points|저장")
    print("· 복제·배열")
    src = None
    if a.from_card and not a.price:   # 덮어쓰기 전에 지금 카드를 떠 둔다
        src = os.path.join(WORK, f"{T}_from_card.html")
        open(src, "w", encoding="utf-8").write(open(os.path.join(REPO, card), encoding="utf-8").read())
    fb = os.path.join(WORK, f"{T}_before_build.html")   # 루트 카드에 없는 배열(백테스트 등)을 예전 카드에서 가져오도록 떠 둔다
    if os.path.exists(os.path.join(REPO, card)):
        open(fb, "w", encoding="utf-8").write(open(os.path.join(REPO, card), encoding="utf-8").read())
        os.environ["ROOT_ARRAYS_FALLBACK"] = fb
    run([PY, "v2/clone_card.py", T, "--force"] + (["--meta", meta] if new else []))
    if a.price:
        src = os.path.join(WORK, f"{T}_from_card.html")
    if src:
        run([PY, os.path.join(HERE, "root_arrays.py"), T, src], show=r"^arrays")
    elif new:
        arr = [PY, "v2/new_ticker_arrays.py", T, "--yahoo", yahoo, "--asof", a.asof]
        if B.get("bt_start"):
            arr += ["--bt-start", B["bt_start"]]
        run(arr, show=r"^arrays|checkpoints")
    else:
        run([PY, os.path.join(HERE, "root_arrays.py"), T], show=r"^arrays")
    print("· 재무")
    if not net:
        print("    (가격 재빌드 — 이전 재무 파일)")
    elif B.get("feed"):
        run([PY, f"v2/adapters/{t}_feed.py", "financials"], show=r"Wrote|저장")
    elif B.get("overlay"):
        run([PY, "v2/adapters/overlay_feed.py", T, cik], show=r"Wrote")
    else:
        run([PY, os.path.join(V2, "vendor", "fetch_financials.py"), T, "--cik", cik, "--years", "5",
             "--out", f"v2/fundamental_data/{T}_financials.json"], show=r"Wrote")
    print("· 배수·비교군·기본적 분석·활동성")
    env_eps = dict(os.environ, EPS_HISTORY=f"scripts/{T}_eps_history.json")
    r = subprocess.run([PY, "v2/build_multiple_history.py", T, "--json", f"v2/{T}_multiples.json"], cwd=REPO,
                       capture_output=True, text=True, env=env_eps)
    for line in (r.stdout + r.stderr).splitlines():
        if re.search(r"적정주가|^  (PER|PBR|PSR|PCR|EV)|⚠", line):
            print("   ", line[:300])
    if r.returncode != 0:   # 실패하면 예전 배수 파일로 이어 가지 않는다(Codex 2026-10-06)
        sys.exit(f"build_multiple_history 실패({r.returncode}):\n{(r.stdout + r.stderr)[-1500:]}")
    run([PY, "v2/build_peer_score.py", T, "--self", f"v2/{T}_multiples.json", "--card"], show=r"대비 =|^  (PER|PBR|PSR|PCR|EV)")
    if B.get("sum_tags") and net:
        run([PY, "v2/adapters/financials_sum_tags.py", T], show=r".")
    run([PY, "v2/build_fundamental_score.py", T, "--card"], show=r"기본적 분석 =|^    ")
    if B.get("overlay"):
        merged = os.path.join(WORK, f"{T}_facts_merged.json")
        sys.path.insert(0, V2); os.chdir(V2)
        import build_multiple_history as bmh
        json.dump(bmh._facts(cik), open(merged, "w")); os.chdir(REPO)
        run([PY, "v2/build_activity_score.py", T, "--facts", merged], show=r'"score"|"reason"')
    elif B.get("feed"):
        run([PY, "v2/build_activity_score.py", T, "--facts", f"v2/.sec_cache/{cik}_facts.json"], show=r'"score"|"reason"')
    else:
        run([PY, "v2/build_activity_score.py", T], show=r'"score"|"reason"')
    p = os.path.join(REPO, card)
    if B.get("no_dcf"):   # 현금흐름 모델 미적용(보험사 — CB, 2026-10-02 사용자 결정, BRKB 방식). 카드 JS가 base == null이면 사유만 적는다.
        print("· 현금흐름 미적용 —", B["no_dcf"])
        h = open(p, encoding="utf-8").read()
        blk = {"low": None, "base": None, "high": None, "requiredGrowth": None, "baseEquivGrowth": None, "reqMode": "growth",
               "requiredMargin": None, "marginNow": None, "growth5y": None, "nonopPerShare": 0, "s2cFallback": False,
               "asOf": a.asof, "unavailable": B["no_dcf"], "hard": [], "hardDetail": {}}
        h = re.sub(rf"const {T}_DCF = \{{.*?\}};[^\n]*", lambda _: f"const {T}_DCF = {json.dumps(blk, ensure_ascii=False)};   // no_dcf", h, count=1, flags=re.S)
        h = re.sub(rf"const {T}_DCF_GRID = .*", f"const {T}_DCF_GRID = null;", h, count=1)
        h = re.sub(rf"const {T}_DCF_TRACK = \[.*?\];", f"const {T}_DCF_TRACK = [];", h, count=1, flags=re.S)
        # 직접 바꿔보기 결과 칸의 대체값 — 틀(NVDA)의 '주당 $297'이 남지 않게(2026-10-06, CB·PGR). JS는 표가 없으면 같은 글을 쓴다.
        h, k = re.subn(r'<span style="[^"]*" id="dcfPickValue">[^<]*</span><span style="[^"]*" id="dcfPickUpside">[^<]*</span>',
                       '<span style="color: var(--text3);" id="dcfPickValue">계산 불가</span><span id="dcfPickUpside"></span>', h, count=1)
        assert k == 1, "dcfPickValue 대체값 자리를 못 찾음"
        open(p, "w", encoding="utf-8").write(h)
    else:
        print("· 현금흐름")
        run([PY, "v2/build_dcf_block.py", T], show=rf"^{T} |⚠")
        run([PY, "v2/build_dcf_grid.py", T])
        h = open(p, encoding="utf-8").read()
        old = re.search(rf"const {T}_DCF_TRACK = \[.*?\];", h, re.S).group(0)
        if not net:   # 추적선은 분기 공시 때만 바뀐다(67초 걸리는 단계) — 지금 카드의 것을 그대로
            new_track = track_old
        else:
            run([PY, "v2/build_dcf_track.py", T, "--json", f"v2/{T}_dcf_track.json"])
            d = json.load(open(os.path.join(V2, f"{T}_dcf_track.json")))
            pts = [f'{{d:"{x["date"]}",low:{round(x["low"], 1)},base:{round(x["base"], 1)},high:{round(x["high"], 1)}}}' for x in d["points"]]
            new_track = f"const {T}_DCF_TRACK = [" + ",".join(pts) + "];"
        h = h.replace(old, new_track, 1)
        open(p, "w", encoding="utf-8").write(h)
    if a.data:
        print("데이터 단계 끝 — cfg/cfg_%s.py를 쓰고 --data 없이 다시 실행" % t)
        return
    print("· 채우기")
    run([PY, os.path.join(HERE, "fill.py"), T], show=r"^ok|^peers")
    run([PY, "v2/strip_caveats.py", T])   # 값 옆 사유 글은 툴팁으로(2026-10-06 사용자 결정)
    run([PY, "v2/sync_fallbacks.py", T] + (["--base", a.sync_base] if a.sync_base else []), show=r".")
    js = os.path.join(WORK, "%s_inline.js" % T)
    open(js, "w").write("\n;\n".join(re.findall(r"<script>(.*?)</script>", open(p, encoding="utf-8").read(), re.S)))
    run(["node", "--check", js])
    print("JS_OK", card)


if __name__ == "__main__":
    main()
