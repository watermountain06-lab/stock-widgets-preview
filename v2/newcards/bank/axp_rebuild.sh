set -e
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
# SKIP_BANK_CARD=1이면 bank_card.py를 건너뛰고 지금 커밋된 AXP_bank.json·peer_universe/banks.json으로 채운다(기반 재현 확인용, 2026-10-05)
if [ -z "$SKIP_BANK_CARD" ]; then python3 v2/adapters/bank_card.py AXP --json v2/AXP_bank.json | grep gates; fi
cp $B/base/axp_base.html v2/AXP_full_widget.html && python3 $B/axp_fill.py | head -3 && python3 $B/unify_js.py AXP && python3 v2/sync_fallbacks.py AXP 2>&1 | tail -1
python3 -c "
import re;h=open('v2/AXP_full_widget.html').read();open('/tmp/AXP_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/AXP_inline.js && echo JS_OK
