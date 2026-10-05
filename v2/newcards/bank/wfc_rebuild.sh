set -e
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
# SKIP_BANK_CARD=1이면 bank_card.py를 건너뛰고 지금 있는 WFC_bank.json·peer_universe/banks.json으로 채운다(기반 재현 확인용, 2026-10-05)
[ -n "$SKIP_BANK_CARD" ] || python3 v2/adapters/bank_card.py WFC --json v2/WFC_bank.json | grep gates
cp $B/base/wfc_base.html v2/WFC_full_widget.html && python3 $B/wfc_fill.py | head -2 && python3 $B/unify_js.py WFC && python3 v2/sync_fallbacks.py WFC 2>&1 | tail -1
