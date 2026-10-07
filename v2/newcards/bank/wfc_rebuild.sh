set -e -o pipefail   # 파이프 안의 실패도 멈춘다(2026-10-06)
cd "$(dirname "$0")/../../.."   # 저장소 루트(스크립트 위치 기준, 2026-10-06)
B=v2/newcards/bank
# SKIP_BANK_CARD=1이면 bank_card.py를 건너뛰고 지금 있는 WFC_bank.json·peer_universe/banks.json으로 채운다(기반 재현 확인용, 2026-10-05)
[ -n "$SKIP_BANK_CARD" ] || python3 v2/adapters/bank_card.py WFC --json v2/WFC_bank.json ${PRICE_ONLY:+--reuse-peers} | grep gates
# head는 출력이 길면 채우기를 SIGPIPE로 죽인다(2026-10-06 AXP·JPM이 틀 값 그대로 남음)
# 줄마다 따로 둬서 set -e가 각 단계 실패에서 멈춘다(주석이 줄 끝에 붙으면 뒤 명령이 사라진다, Codex 2026-10-06)
cp $B/base/wfc_base.html v2/WFC_full_widget.html
python3 $B/wfc_fill.py | tail -2
python3 $B/unify_js.py WFC
python3 v2/strip_caveats.py WFC   # 값 옆 사유 글은 툴팁으로(2026-10-06)
python3 v2/sync_fallbacks.py WFC 2>&1 | tail -1
