# 보관 중인 카드

매일 실행(`daily_price.py`)은 `v2/newcards/cfg/`와 `v2/*_full_widget.html`을 보고 카드를 돈다. 잠시 빼 둘 카드의 cfg와 v2 카드 파일을 여기에 둔다.

| 카드 | 보관한 날 | 이유 | 되살리기 |
|---|---|---|---|
| CBOE | 2026-10-24 | Actions 캐시 문제가 풀릴 때까지 푸시·실행 보류(사용자 결정). 카드는 01d32775에서 만들었다 | `git mv`로 `cfg_cboe.py` → `v2/newcards/cfg/`, `CBOE_full_widget.html` → `v2/`, 그다음 `add_v2_ticker.py CBOE --name "Cboe Global Markets"` → `sync_v2_home.py` → `build_index.py` → `validate_site_data.py`, BIIB 다음·NTAP 이전 링크를 CBOE로 되돌린다 |
