set -e
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
python3 v2/adapters/bank_card.py SCHW --json v2/SCHW_bank.json | grep gates
cp $B/base/schw_base.html v2/SCHW_full_widget.html && python3 $B/schw_fill.py | head -6 || exit 1 && python3 v2/sync_fallbacks.py SCHW 2>&1 | tail -1
python3 -c "
import re;h=open('v2/SCHW_full_widget.html').read();open('/tmp/SCHW_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/SCHW_inline.js && echo JS_OK
