set -e
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
python3 v2/adapters/bank_card.py JPM --json v2/JPM_bank.json | grep gates
cp $B/base/jpm_base.html v2/JPM_full_widget.html && python3 $B/jpm_fill.py | head -2 && python3 $B/unify_js.py JPM && python3 v2/sync_fallbacks.py JPM 2>&1 | tail -1
python3 -c "
import re;h=open('v2/JPM_full_widget.html').read();open('/tmp/JPM_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/JPM_inline.js && echo JS_OK
