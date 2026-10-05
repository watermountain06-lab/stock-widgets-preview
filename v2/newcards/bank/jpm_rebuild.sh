set -e
cd "$(dirname "$0")/../../.."   # 저장소 루트(스크립트 위치 기준)
B=v2/newcards/bank
# SKIP_BANK_CARD=1: 지금 커밋된 JPM_bank.json·peer_universe/banks.json 그대로 채우기만 한다(재현 확인용). 보통은 bank_card.py부터 돈다.
# SYNC_BASE: sync_fallbacks.py가 쓸 http 서버 주소(기본 http://localhost:8765, 저장소 루트에서 띄운 것)
if [ -z "$SKIP_BANK_CARD" ]; then python3 v2/adapters/bank_card.py JPM --json v2/JPM_bank.json | grep gates; fi
cp $B/base/jpm_base.html v2/JPM_full_widget.html && python3 $B/jpm_fill.py | head -2 && python3 $B/unify_js.py JPM && python3 v2/sync_fallbacks.py JPM --base "${SYNC_BASE:-http://localhost:8765}" 2>&1 | tail -1
python3 -c "
import re;h=open('v2/JPM_full_widget.html').read();open('/tmp/JPM_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/JPM_inline.js && echo JS_OK
