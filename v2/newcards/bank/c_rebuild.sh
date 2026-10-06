set -e -o pipefail   # 파이프 안의 실패도 멈춘다(2026-10-06)
# SKIP_BANK=1(또는 SKIP_BANK_CARD=1) 이면 ixbrl_supplement·bank_card를 건너뛰고 커밋된 v2/C_bank.json·peer_universe/banks.json으로 채운다(기반 재현 확인용, 2026-10-05).
# SYNC_BASE로 sync_fallbacks의 http 서버 주소를 바꾼다(기본 http://localhost:8765).
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
if [ -z "$SKIP_BANK$SKIP_BANK_CARD" ]; then
python3 v2/adapters/ixbrl_supplement.py 0000831001 | tail -1
python3 v2/adapters/bank_card.py C --json v2/C_bank.json | grep gates
fi
# head는 출력이 길면 채우기를 SIGPIPE로 죽인다(2026-10-06 AXP·JPM이 틀 값 그대로 남음)
# 줄마다 따로 둬서 set -e가 각 단계 실패에서 멈춘다(주석이 줄 끝에 붙으면 뒤 명령이 사라진다, Codex 2026-10-06)
cp $B/base/c_base.html v2/C_full_widget.html
python3 $B/c_fill.py | tail -3
python3 $B/unify_js.py C
python3 v2/sync_fallbacks.py C --base "${SYNC_BASE:-http://localhost:8765}" 2>&1 | tail -1
python3 -c "
import re;h=open('v2/C_full_widget.html').read();open('/tmp/C_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check /tmp/C_inline.js && echo JS_OK
