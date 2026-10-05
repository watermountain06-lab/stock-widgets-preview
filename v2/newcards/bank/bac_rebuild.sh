set -e
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
python3 v2/adapters/bank_card.py BAC --json v2/BAC_bank.json | grep gates
cp $B/base/bac_base.html v2/BAC_full_widget.html && python3 $B/bac_fill.py | head -3 && python3 $B/unify_js.py BAC && python3 v2/sync_fallbacks.py BAC 2>&1 | tail -1
python3 -c "
import re;h=open('v2/BAC_full_widget.html').read();open('/tmp/BAC_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/BAC_inline.js && echo JS_OK
