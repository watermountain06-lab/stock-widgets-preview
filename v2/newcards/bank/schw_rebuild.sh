set -e -o pipefail   # 파이프 안의 실패도 멈춘다(2026-10-06)
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
# SKIP_BANK_CARD=1이면 bank_card.py를 건너뛰고 저장소의 SCHW_bank.json·banks.json으로 채운다(기반 재현 확인용, 2026-10-05). 보통은 비워 둔다.
[ -n "$SKIP_BANK_CARD" ] || python3 v2/adapters/bank_card.py SCHW --json v2/SCHW_bank.json ${PRICE_ONLY:+--reuse-peers} | grep gates
# head는 출력이 길면 채우기를 SIGPIPE로 죽인다(2026-10-06 AXP·JPM이 틀 값 그대로 남음) || exit 1
# 줄마다 따로 둬서 set -e가 각 단계 실패에서 멈춘다(주석이 줄 끝에 붙으면 뒤 명령이 사라진다, Codex 2026-10-06)
cp $B/base/schw_base.html v2/SCHW_full_widget.html
python3 $B/schw_fill.py | tail -6
python3 $B/unify_js.py SCHW
python3 v2/strip_caveats.py SCHW   # 값 옆 사유 글은 툴팁으로(2026-10-06)
python3 v2/sync_fallbacks.py SCHW ${SYNC_BASE:+--base $SYNC_BASE} 2>&1 | tail -1
python3 -c "
import re;h=open('v2/SCHW_full_widget.html').read();open('/tmp/SCHW_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/SCHW_inline.js && echo JS_OK
