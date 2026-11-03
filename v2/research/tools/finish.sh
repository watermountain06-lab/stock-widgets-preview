#!/bin/zsh
# finish.sh T — 데이터·빌드·백테스트·대체값·점검·preflight·글자 더미
T=$1; t=${T:l}; SP=${CARD_WORK:-/tmp/card_work}; mkdir -p $SP; [ -x /opt/miniconda3/bin/python3 ] && export PATH=/opt/miniconda3/bin:$PATH
cd ~/Workspace/stock-widgets-preview
REFRESH=1 SYNC_BASE=http://localhost:8777 python3 v2/newcards/build.py $T --data --asof ${ASOF:-2026-10-23} > $SP/${t}_dF.log 2>&1 || { echo "DATA FAIL"; tail -5 $SP/${t}_dF.log; }
[ -f v2/backtest_pre/$T.json ] || { python3 v2/build_backtest_pre.py $T 2>&1 | tail -1 | grep -q "가격 없음" && python3 v2/build_backtest_pre.py $T --yahoo 2>&1 | tail -1; }
REFRESH=1 SYNC_BASE=http://localhost:8777 python3 v2/newcards/build.py $T --asof ${ASOF:-2026-10-23} > $SP/${t}_bF.log 2>&1 || { echo "BUILD FAIL"; grep -B3 "Error" $SP/${t}_bF.log | tail -6; }
grep "ok $T" $SP/${t}_bF.log | cut -c1-140
python3 v2/refresh_backtest.py $T 2>&1 | tail -1 | cut -c1-40
python3 v2/sync_fallbacks.py $T --base http://localhost:8777 2>&1 | tail -1
python3 v2/newcards/check_literals.py $T --strict 2>&1 | tail -1
git checkout -- v2/newcards/refresh_changes.jsonl
python3 v2/newcards/preflight.py $T --after 2>&1 | tail -1
python3 - <<PY
import sys; sys.path.insert(0,'v2/newcards')
import compare_render as c
t,ti=c.dump('http://localhost:8777/v2/${T}_full_widget.html','${T}')
open('$SP/${t}_text.txt','w').write('\n'.join(t)+'\n\n==== TITLES ====\n'+'\n'.join(ti))
PY
