set -e
cd "$(dirname "$0")/../../.."   # 저장소 루트(복제본에서 돌려도 그 복제본 기준)
B=v2/newcards/bank
# SKIP_BANK_CARD=1 이면 bank_card.py를 건너뛰고 커밋된 GS_bank.json·peer_universe/banks.json으로 채운다(기반 재현 확인용).
# SYNC_BASE=http://localhost:PORT 로 sync_fallbacks의 http 서버 주소를 바꾼다(기본 8765).
if [ -z "$SKIP_BANK_CARD" ]; then python3 v2/adapters/bank_card.py GS --json v2/GS_bank.json | grep gates; fi
cp $B/base/gs_base.html v2/GS_full_widget.html && python3 $B/gs_fill.py | head -6 || exit 1 && python3 $B/unify_js.py GS && python3 v2/sync_fallbacks.py GS --base "${SYNC_BASE:-http://localhost:8765}" 2>&1 | tail -1
python3 -c "
import re;h=open('v2/GS_full_widget.html').read();open('/tmp/GS_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/GS_inline.js && echo JS_OK
