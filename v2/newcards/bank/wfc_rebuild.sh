set -e
cd /Users/watermountain/Workspace/stock-widgets-preview
B=v2/newcards/bank
python3 v2/adapters/bank_card.py WFC --json v2/WFC_bank.json | grep gates
cp $B/base/wfc_base.html v2/WFC_full_widget.html && python3 $B/wfc_fill.py | head -2 && python3 $B/unify_js.py WFC && python3 v2/sync_fallbacks.py WFC 2>&1 | tail -1
