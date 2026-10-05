set -e
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
python3 v2/adapters/bank_card.py MS --json v2/MS_bank.json | grep gates
cp $B/base/ms_base.html v2/MS_full_widget.html && python3 $B/ms_fill.py | head -6 || exit 1 && python3 $B/unify_js.py MS && python3 v2/sync_fallbacks.py MS 2>&1 | tail -1
python3 -c "
import re;h=open('v2/MS_full_widget.html').read();open('/tmp/MS_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/MS_inline.js && echo JS_OK
