# vendor — stock-widgets-redesign에서 가져온 파일

GitHub Actions에서 v2 카드를 다시 만들려면 이 저장소만으로 돌아야 해서(2026-10-06), redesign 저장소의 두 파일을 복사해 둔다.
원본: `stock-widgets-redesign/scripts/` (복사 시점 커밋 62ea77f). 원본을 고치면 여기에도 복사한다.

| 파일 | 쓰는 곳 |
|---|---|
| `fetch_financials.py` | `newcards/build.py`(재무), `adapters/overlay_feed.py`·`asml_feed.py`·`tsm_feed.py`·`skhy_feed.py` |
| `sp500.json` | `adapters/sector_universe.py`(섹터 비교군), `bank_card.py`(은행 비교군, sector_universe 경유) |
