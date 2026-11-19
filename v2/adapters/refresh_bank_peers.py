"""S&P500 은행 비교군(bank_card.SUBS) 가운데 카드 아닌 은행의 SEC 재무(companyfacts)와 EPS 파일을 새로 받는다 —
토요일 주간 실행(daily_price.weekly_pre)이 SEC_REFRESH_UNLISTED=세션으로 돌린다(안건 E73, 2026-11-19).

섹터 비교군은 토요일마다 refresh_peer_files.py(sector_universe.one)가 카드 아닌 회사의 재무·EPS를 새로 받는데, 은행 비교군은 그
목록 밖이라 처음 받은 뒤로 갱신되지 않았다 — 순이익(관문 N1·N5)과 EPS 파일(v2/peer_universe/banks/*_eps_history.json, 동종업 PER)이
2026-09~10에 멈춰 있었다(Fable 은행 9판 검토 2026-11-19). 섹터와 같은 규칙: 기준표(sec_approved) 밖 회사만, EPS는 같은 날짜로.
카드 은행(기준표에 있는 회사)의 재무·EPS는 카드 쪽 규칙을 따르므로 여기서 건드리지 않는다.
받기 실패는 .sec_cache/_refresh_failed.txt에 적는다(주간 상태 problems로 알림 — 옛 자료로 계산).

    SEC_REFRESH_UNLISTED=2026-11-21 python3 v2/adapters/refresh_bank_peers.py
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.dirname(HERE)
REPO = os.path.dirname(V2)
sys.path[:0] = [HERE, V2]
import bank_card as bc  # noqa: E402
import build_multiple_history as bmh  # noqa: E402


def main():
    if not os.environ.get("SEC_REFRESH_UNLISTED"):
        sys.exit("SEC_REFRESH_UNLISTED(세션 날짜)가 없으면 캐시를 그대로 읽기만 한다 — 주간 실행에서만 돌릴 것")
    rows = [r for r in bc.su.sp500_rows() if r.get("subIndustry") in bc.SUBS]
    appr = bmh._approved()
    failed_path = os.path.join(bmh.CACHE_DIR, "_refresh_failed.txt")
    before = open(failed_path).read() if os.path.exists(failed_path) else ""
    os.makedirs(bc.PEER_DIR, exist_ok=True)
    targets, eps_fail = [], []
    for r in sorted(rows, key=lambda r: r["ticker"]):
        t, cik = r["ticker"], str(r["cik"]).zfill(10)
        if cik in appr:
            continue   # 카드 은행 — 기준표 공시일 규칙
        targets.append(t)
        bmh._facts(cik)   # SEC_REFRESH_UNLISTED면 이번 실행에 한 번 새로 받는다(실패는 _facts가 실패 파일에 적는다)
        out = os.path.join(bc.PEER_DIR, f"{t}_eps_history.json")
        p = subprocess.run([sys.executable, os.path.join(REPO, "scripts", "fetch_eps_history.py"), t, "--cik", cik, "--out", out],
                           capture_output=True, text=True)
        if p.returncode:
            eps_fail.append(t)
            with open(failed_path, "a") as f:
                f.write(f"{cik} eps {t}\n")
        time.sleep(0.6)
    after = open(failed_path).read() if os.path.exists(failed_path) else ""
    new_fail = [l for l in after[len(before):].splitlines() if l.strip()]
    print(f"은행 비교군(카드 아닌 {len(targets)}곳: {' '.join(targets)}) 재무·EPS 새로 받기 — "
          + (f"실패 {len(new_fail)}건(옛 자료 사용): {', '.join(new_fail)}" if new_fail else "실패 없음"))
    return 1 if new_fail else 0


if __name__ == "__main__":
    sys.exit(main())
