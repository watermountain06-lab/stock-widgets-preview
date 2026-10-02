set -e
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
python3 v2/adapters/ixbrl_supplement.py 0000831001 | tail -1
python3 v2/adapters/bank_card.py C --json v2/C_bank.json | grep gates
cp $B/base/c_base.html v2/C_full_widget.html && python3 $B/c_fill.py | head -3 && python3 v2/sync_fallbacks.py C 2>&1 | tail -1
python3 -c "
import re;h=open('v2/C_full_widget.html').read();open('/tmp/C_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/C_inline.js && echo JS_OK
