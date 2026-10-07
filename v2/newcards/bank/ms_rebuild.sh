set -e -o pipefail   # 파이프 안의 실패도 멈춘다(2026-10-06)
cd "$(dirname "$0")/../../.."   # 저장소 루트(스크립트 위치 기준, 2026-10-06)
B=v2/newcards/bank
# SKIP_BANK_CARD=1: bank_card.py를 건너뛰고 지금 MS_bank.json·peer_universe/banks.json으로 채우기만(기반 재현 확인용).
# 평소에는 돌린다 — banks.json을 MS 기준일(9/29)로 다시 써야 비교 차트 값·제목 날짜가 카드와 맞는다.
if [ -z "$SKIP_BANK_CARD" ]; then python3 v2/adapters/bank_card.py MS --json v2/MS_bank.json ${PRICE_ONLY:+--reuse-peers} | grep gates; fi
# head는 출력이 길면 채우기를 SIGPIPE로 죽인다(2026-10-06 AXP·JPM이 틀 값 그대로 남음) || exit 1
# 줄마다 따로 둬서 set -e가 각 단계 실패에서 멈춘다(주석이 줄 끝에 붙으면 뒤 명령이 사라진다, Codex 2026-10-06)
cp $B/base/ms_base.html v2/MS_full_widget.html
python3 $B/ms_fill.py | tail -6
python3 $B/unify_js.py MS
python3 v2/strip_caveats.py MS   # 값 옆 사유 글은 툴팁으로(2026-10-06)
python3 v2/sync_fallbacks.py MS ${SYNC_BASE:+--base $SYNC_BASE} 2>&1 | tail -1
python3 -c "
import re;h=open('v2/MS_full_widget.html').read();open('v2/.sec_cache/_work/MS_inline.js','w').write('\n;\n'.join(re.findall(r'<script>(.*?)</script>',h,re.S)))"
node --check v2/.sec_cache/_work/MS_inline.js && echo JS_OK
