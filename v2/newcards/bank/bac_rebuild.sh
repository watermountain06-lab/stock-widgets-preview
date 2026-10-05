set -e
# SKIP_BANK_CARD=1 이면 bank_card.py를 건너뛰고 커밋된 BAC_bank.json·peer_universe/banks.json으로 채운다(기반 재현 확인용, 2026-10-05).
# SYNC_BASE로 sync_fallbacks.py가 쓸 로컬 서버 주소를 바꿀 수 있다(기본 http://localhost:8765).
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
if [ -z "$SKIP_BANK_CARD" ]; then python3 v2/adapters/bank_card.py BAC --json v2/BAC_bank.json | grep gates; fi
cp $B/base/bac_base.html v2/BAC_full_widget.html && python3 $B/bac_fill.py | head -3 && python3 $B/unify_js.py BAC && python3 v2/sync_fallbacks.py BAC --base "${SYNC_BASE:-http://localhost:8765}" 2>&1 | tail -1
python3 -c "
import re;h=open('v2/BAC_full_widget.html').read();open('/tmp/BAC_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/BAC_inline.js && echo JS_OK
