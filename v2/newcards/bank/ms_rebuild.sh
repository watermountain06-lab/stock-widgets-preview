set -e
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
# SKIP_BANK_CARD=1: bank_card.py를 건너뛰고 지금 MS_bank.json·peer_universe/banks.json으로 채우기만(기반 재현 확인용).
# 평소에는 돌린다 — banks.json을 MS 기준일(9/29)로 다시 써야 비교 차트 값·제목 날짜가 카드와 맞는다.
if [ -z "$SKIP_BANK_CARD" ]; then python3 v2/adapters/bank_card.py MS --json v2/MS_bank.json | grep gates; fi
cp $B/base/ms_base.html v2/MS_full_widget.html && python3 $B/ms_fill.py | head -6 || exit 1 && python3 $B/unify_js.py MS && python3 v2/sync_fallbacks.py MS ${SYNC_BASE:+--base $SYNC_BASE} 2>&1 | tail -1
python3 -c "
import re;h=open('v2/MS_full_widget.html').read();open('/tmp/MS_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/MS_inline.js && echo JS_OK
