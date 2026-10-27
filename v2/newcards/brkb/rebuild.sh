#!/bin/bash
# BRKB 카드 다시 만들기(2026-10-12, 전용 생성기). 매일 daily_price.py가 부른다 — 새 공시가 없으면 가격·숫자만 바뀐다.
#   bash v2/newcards/brkb/rebuild.sh
# SYNC_BASE: sync_fallbacks.py가 쓸 http 서버 주소(기본 http://localhost:8765)
set -e -o pipefail
cd "$(dirname "$0")/../../.."
T=BRKB
BK=$(mktemp -d); cp "v2/${T}_full_widget.html" "$BK/"
trap 'rc=$?; if [ $rc -ne 0 ]; then cp "$BK/${T}_full_widget.html" "v2/${T}_full_widget.html"; echo "실패 — 되돌림"; fi; rm -rf "$BK"' EXIT
python3 v2/newcards/brkb/brkb_sync.py | tail -2
python3 v2/newcards/price_arrays.py "$T" | tail -1
python3 v2/newcards/brkb/brkb_fill.py | tail -1
python3 v2/newcards/hand_refresh.py "$T" | tail -1
python3 v2/apply_theme.py "$T"
python3 v2/sync_fallbacks.py "$T" --base "${SYNC_BASE:-http://localhost:8765}" 2>&1 | tail -1
mkdir -p v2/.sec_cache/_work
python3 -c "
import re,sys;T=sys.argv[1];h=open(f'v2/{T}_full_widget.html').read();open(f'v2/.sec_cache/_work/{T}_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))" "$T"
node --check "v2/.sec_cache/_work/${T}_inline.js" && echo JS_OK
