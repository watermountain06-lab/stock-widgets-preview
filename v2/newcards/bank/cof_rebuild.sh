set -e
set -o pipefail   # 채우기 스크립트가 확인에서 멈추면 head 뒤에서도 멈춘다
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
# SKIP_BANK_CARD=1 이면 bank_card.py를 건너뛰고 저장된 COF_bank.json·peer_universe/banks.json으로 채운다(기반 재현 확인용, 2026-10-05)
# 기반 다시 만들기(지금 NVDA 틀): cp v2/COF_full_widget.html /tmp/COF_card.html && python3 v2/clone_card.py COF --force --meta v2/newcards/meta/cof.json
#   && python3 $B/cof_arrays.py /tmp/COF_card.html && cp v2/COF_full_widget.html $B/base/cof_base.html
[ -n "$SKIP_BANK_CARD" ] || python3 v2/adapters/bank_card.py COF --json v2/COF_bank.json | grep gates
# head는 출력이 길면 채우기를 SIGPIPE로 죽인다(2026-10-06 AXP·JPM이 틀 값 그대로 남음)
# 줄마다 따로 둬서 set -e가 각 단계 실패에서 멈춘다(주석이 줄 끝에 붙으면 뒤 명령이 사라진다, Codex 2026-10-06)
cp $B/base/cof_base.html v2/COF_full_widget.html
python3 $B/cof_fill.py | tail -6
python3 $B/unify_js.py COF
python3 v2/strip_caveats.py COF   # 값 옆 사유 글은 툴팁으로(2026-10-06)
python3 v2/sync_fallbacks.py COF ${SYNC_BASE:+--base $SYNC_BASE} 2>&1 | tail -1
python3 -c "
import re;h=open('v2/COF_full_widget.html').read();open('/tmp/COF_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/COF_inline.js && echo JS_OK
