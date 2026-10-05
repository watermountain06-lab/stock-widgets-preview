set -e
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
python3 v2/adapters/bank_card.py AXP --json v2/AXP_bank.json | grep gates
cp $B/base/axp_base.html v2/AXP_full_widget.html && python3 $B/axp_fill.py | head -3 && python3 $B/unify_js.py AXP && python3 v2/sync_fallbacks.py AXP 2>&1 | tail -1
python3 -c "
import re;h=open('v2/AXP_full_widget.html').read();open('/tmp/AXP_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/AXP_inline.js && echo JS_OK
