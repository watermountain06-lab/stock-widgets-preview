set -e -o pipefail   # 파이프 안의 실패도 멈춘다(2026-10-06)
cd "$(dirname "$0")/../../.."   # 저장소 루트(스크립트 위치 기준, 2026-10-06)
B=v2/newcards/bank
# SYNC_BASE로 sync_fallbacks.py가 쓸 로컬 서버 주소를 바꿀 수 있다(기본 http://localhost:8765).
# SKIP_BANK_CARD=1이면 bank_card.py를 건너뛰고 지금 커밋된 AXP_bank.json·peer_universe/banks.json으로 채운다(기반 재현 확인용, 2026-10-05)
if [ -z "$SKIP_BANK_CARD" ]; then python3 v2/adapters/bank_card.py AXP --json v2/AXP_bank.json ${PRICE_ONLY:+--reuse-peers} | grep gates; fi
# head는 출력이 길면 채우기를 SIGPIPE로 죽인다(2026-10-06 AXP·JPM이 틀 값 그대로 남음)
# 줄마다 따로 둬서 set -e가 각 단계 실패에서 멈춘다(주석이 줄 끝에 붙으면 뒤 명령이 사라진다, Codex 2026-10-06)
cp $B/base/axp_base.html v2/AXP_full_widget.html
python3 $B/axp_fill.py | tail -3
python3 $B/unify_js.py AXP
python3 v2/strip_caveats.py AXP   # 값 옆 사유 글은 툴팁으로(2026-10-06)
python3 v2/sync_fallbacks.py AXP --base "${SYNC_BASE:-http://localhost:8765}" 2>&1 | tail -1
python3 -c "
import re;h=open('v2/AXP_full_widget.html').read();open('v2/.sec_cache/_work/AXP_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check v2/.sec_cache/_work/AXP_inline.js && echo JS_OK
