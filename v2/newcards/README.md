# v2 카드 만들기 도구 (2026-10-02)

71위부터 루트 카드 없이 만든 새 종목과, 루트 카드에서 옮긴 일부 종목(VZ·TMUS·DE 등)의 v2 카드를 다시 만드는 도구다.
그동안 세션 임시 폴더(scratchpad)에만 있던 것을 옮겨 왔다. 절차의 원칙(숫자 지어내지 않기, 배열 손으로 치지 않기, Codex·브라우저 검토)은
`/ticker` 스킬 플레이북(stock-widgets-redesign/.claude/skills/ticker/playbook.md)의 "v2 새 종목" 절을 따른다.

## 파일

| 파일 | 하는 일 |
|---|---|
| `build.py T [--data]` | 한 장을 처음부터 다시 만든다: 복제 → EPS → 배열 → 재무 → 배수·비교군·기본적 분석·활동성 → 현금흐름 → 채우기 → 검사 |
| `fill.py T` | 문장·표 채우기(공통). 종목별 내용은 `cfg/cfg_{t}.py` |
| `cfg/cfg_{t}.py` | 종목별 설정 — 판정 표, 보도자료 링크, 문장, 뉴스, 투자 포인트, 애널리스트. `BUILD` 사전은 빌드 옵션 |
| `meta/{t}.json` | 새 종목 헤더(이름·업종·색·시총 순위·앞뒤 카드 링크) — `clone_card.py --meta` |
| `yahoo/{t}.json` | 새 종목 Yahoo 일봉(2020-01~) — `new_ticker_arrays.py` |
| `root_arrays.py T` | 루트 카드가 있는 종목은 배열을 루트 카드에서 옮긴다 |
| `aph_root_arrays_special.py` | APH만 — 분할 안전장치로 루트가 멈춰 Yahoo 일봉으로 다시 만든 기록(그대로는 못 돌림, `/tmp/aph_rows.json` 필요) |

`BUILD` 옵션: `eps_tag`(분사 종목 계속사업 EPS — WDC), `bt_start`(백테스트 일봉 시작일 — WDC·T), `overlay`(companyfacts 지연 — ABT·WELL·NEE).

## 새 종목 순서

1. 시총 순위 확인(StockAnalysis `marketCap`). `scripts/fetch_eps_history.py` CIKS·KNOWN_SPLITS, `v2/build_activity_score.py` CIKS, `v2/sectors.json`에 등록.
2. `meta/{t}.json`을 쓰고(앞 카드의 `next`도 고친다), Yahoo 일봉을 `yahoo/{t}.json`으로 받는다 —
   `curl -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/T?period1=1577836800&period2=1790899200&interval=1d&events=div%2Csplits"`
   (긴 브라우저 UA는 429). `events.splits`에 분사 조정 비율(1.45 미만)이 있으면 분사 종목이다 — 아래 "분사".
3. `python3 v2/newcards/build.py T --data` — 숫자만 만든다. 여기서 아래 "점검"을 모두 본다.
4. SEC 원문(10-Q·보도자료·8-K)을 받아 `cfg/cfg_{t}.py`를 쓴다(비슷한 종목의 cfg를 복사해 시작).
5. `python3 v2/newcards/build.py T` — 채우기·검사까지. 브라우저(http://localhost:8765/v2/T_full_widget.html) 콘솔 오류·NVDA 틀 잔재 확인.
6. Codex 검토 → Fable 검토 → 고치고 Codex 2차 → `v2/CARD_ITEMS.md`에 기록, 공통 과제는 `v2/research/after_100_cards_agenda.md`.

StockAnalysis 애널리스트 페이지는 `curl -A "curl/8.4.0"`(짧은 "Mozilla/5.0"은 403). `recommendations` 마지막 항목과 `targets`를 쓴다.

## 점검 (`--data` 뒤, cfg 쓰기 전)

- **분기 표가 최신 10-Q까지 있나** — 없으면 companyfacts 지연. `BUILD['overlay']=True`(인라인 XBRL 보충). 보충 전에 만든 배열·백테스트는 다시 만든다(ABT: 2분기 EPS가 빠져 적중률이 달랐다).
- **매출·영업이익을 10-Q 손익계산서와 대조** — 영업이익 줄이 없으면 `DERIVED_OPINC`(ETN·PFE·WELL), 매출 태그가 섞이거나 반올림 주석 값이면 `EXCLUDE_TAGS`·`EXTRA_TAGS`·`PREFER_TAGS`(PFE·NEE·WELL).
- **차입금·현금·단기투자·리스를 재무상태표와 대조** — 1년 안 만기 차입금 누락(ETN·T·UNP), 멈춘 단기투자 태그(T·MCD·PFE), 리스 태그가 이미 금융리스 포함(MCD), 주식 수 단위 오류(MCD 711.1).
- **현금흐름 시나리오** — 음수·순서 역전(낙관 < 기본)은 원인을 찾아 문장으로 적는다. 인수 대금이 큰 해는 매출/자본이 극단적이다.
- **비교군** — S&P500 섹터 파일을 처음 만들면 이상값(PSR 수백 배, 0)부터 본다(부동산).

## 분사 종목 (GE·DELL·IBM·WDC·T)

`RESTATED_LATEST`, 자기 이력 창(`build_multiple_history.HISTORY_START`)은 **재작성 숫자가 처음 공시된 날** — 첫 분사 후 재무상태표 날이 아니다(WDC는 그 사이 PSR이 29.8배로 튀었다). 최근 4분기 합이 모두 분사 뒤 분기여야 한다(T). DCF 이력(`build_dcf.HISTORY_WINDOW`)은 네 분기가 모두 재작성인 첫 최근 4분기 합부터(WDC는 영업이익이 FY24 분기에서 섞였다). 백테스트는 `bt_start`로 같은 날부터.

## 다시 만들 때

`build.py`는 카드를 덮어쓴다. 비교군(카드 유니버스 가격)은 매일 갱신되므로 같은 cfg로 다시 만들어도 동종업 점수가 조금 달라질 수 있다(WDC 55.3 → 56.8, 2026-10-02) — 판정이 바뀌면 cfg의 VOTES·문장도 고친다(fill.py가 assert로 멈춘다).
