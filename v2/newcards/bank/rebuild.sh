#!/bin/bash
# 은행 카드 공통 다시 만들기 — 사전 등록 8판(2026-11-06, research/bank_v8_design.md; 7판 2026-10-11). 종목별 {t}_rebuild.sh를 대신한다.
#   bash v2/newcards/bank/rebuild.sh JPM
# PRICE_ONLY=1: 매일 가격 재빌드 — 비교 은행 값은 토요일 것(peer_universe/banks.json)을 쓰고 원문 값 수집·공시 보충을 건너뛴다.
# SKIP_BANK_CARD=1: 지금 v2/{T}_bank.json으로 채우기만(재현 확인용).
# SYNC_BASE: sync_fallbacks.py가 쓸 http 서버 주소(기본 http://localhost:8765, 저장소 루트에서 띄운 것)
set -e -o pipefail
cd "$(dirname "$0")/../../.."
B=v2/newcards/bank
T=$(echo "$1" | tr a-z A-Z); t=$(echo "$1" | tr A-Z a-z)
[ -f "$B/base/${t}_base.html" ] || { echo "기반 HTML 없음: $B/base/${t}_base.html"; exit 2; }
# 실패하면 카드·은행 자료를 시작 전으로 되돌린다(직접 실행할 때 — daily_price.py는 따로 되돌린다, Codex)
BK=$(mktemp -d); for f in "v2/${T}_full_widget.html" "v2/${T}_bank.json"; do [ -f "$f" ] && cp "$f" "$BK/"; done
trap 'rc=$?; if [ $rc -ne 0 ]; then for f in "v2/${T}_full_widget.html" "v2/${T}_bank.json"; do [ -f "$BK/$(basename $f)" ] && cp "$BK/$(basename $f)" "$f"; done; echo "실패 — 되돌림"; fi; rm -rf "$BK"' EXIT
if [ -z "$SKIP_BANK_CARD" ]; then
  if [ -z "$PRICE_ONLY" ]; then
    [ "$T" = "C" ] && python3 v2/adapters/ixbrl_supplement.py 0000831001 | tail -1
    # 새 10-Q·10-K 원문 값 — 비교 은행 전부(8판 §8: 카드 없는 PNC 등이 2026-06에서 멈췄다, 2026-11-06)는 하루 한 번만,
    # 그 뒤 카드는 그 종목만(제출 목록 요청이 카드 13장 × 은행 21곳으로 불어나지 않게 — Codex). 받은 분기는 건너뛴다. 마지막 줄 = 실패 요약
    STAMP="v2/.sec_cache/_work/bank_sv_all.$(date +%Y-%m-%d)"; mkdir -p v2/.sec_cache/_work
    if [ -f "$STAMP" ]; then python3 v2/adapters/bank_sec_values.py "$T" | tail -1
    else python3 v2/adapters/bank_sec_values.py --stamp "$STAMP" | tail -1; fi   # 표식은 실패가 없을 때만 파이썬이 남긴다
  fi
  BANK_EDITION=8 python3 v2/adapters/bank_card.py "$T" --json "v2/${T}_bank.json" ${PRICE_ONLY:+--reuse-peers} | grep gates
fi
cp "$B/base/${t}_base.html" "v2/${T}_full_widget.html"
BANK_EDITION=8 python3 "$B/bank_fill.py" "$T" | tail -2
python3 "$B/unify_js.py" "$T"
python3 v2/strip_caveats.py "$T"
python3 v2/apply_theme.py "$T"
python3 v2/sync_fallbacks.py "$T" --base "${SYNC_BASE:-http://localhost:8765}" 2>&1 | tail -1
python3 -c "
import re,sys;T=sys.argv[1];h=open(f'v2/{T}_full_widget.html').read();open(f'v2/.sec_cache/_work/{T}_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))" "$T"
node --check "v2/.sec_cache/_work/${T}_inline.js" && echo JS_OK
