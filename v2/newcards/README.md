# v2 카드 만들기 도구 (2026-10-02)

v2 비은행 카드를 다시 만드는 공통 생성기다. 2026-10-05 틀 통일로 틀 시절 카드 47장(AAPL~XOM, KO 포함)도 cfg를 갖게 되어 SPCX·NVDA(틀 자체)·BRKB·은행을 뺀 91장이 모두 이 도구로 다시 만들어진다(은행 9장은 `bank/`).
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

`BUILD` 옵션(2026-10-05 추가): `feed`(외국 기업 — EPS·재무를 `v2/adapters/{t}_feed.py`로, 활동성은 그 캐시 facts — ASML·TSM·SKHY), `eps_cmd`(EPS 단계를 다른 명령으로 — V `visa_classA.py eps`), `sum_tags`(재무 항목을 여러 태그 합으로 다시 채운 뒤 기본적 분석 — XOM 재고, 대상은 `adapters/financials_sum_tags.py`의 SUMS).

cfg 선택 항목(2026-10-05 추가): `ANALYST_ASOF`(애널리스트 기준일), `REQ_MULT_EXACT`(요구 성장률을 '지난 5년의 N배'로), `REVERSE`(성장 모드 역산 문장 — 없으면 표준 문장), `PBR_GAP_NEG_EQUITY=False`(자본이 늘 양수였던 종목의 PBR 이력 공백 배지), `NO_DCF_SKEW`(현금흐름 칸 쏠림 메모 끄기 — 금융), `NONOP_NEG_SIGN`(비영업 자산 줄 음수 '−$'), `PRE`/`POST`(채우기 앞뒤에 실행하는 종목별 코드).

`BUILD` 옵션: `eps_tag`(분사 종목 계속사업 EPS — WDC), `bt_start`(백테스트 일봉 시작일 — WDC·T), `overlay`(companyfacts 지연 — ABT·WELL·NEE, 또는 재무 태그 별칭이 필요할 때 — BA 재고), `company_tags`(회사 고유 태그 — COP 설비투자, NEM 재고·리스). 재무 데이터의 총계 태그가 없으면 `adapters/overlay_feed.py`의 `SUM`(구성 줄 합 — ACN 총부채, NEM 재고 + 광석 비축분, 옛 행이 있으면 `REPLACE`)을 쓰고 `overlay`를 켠다. 활동성 매출원가·재고 예외는 `build_activity_score.py`의 `COGS_TAG_BY_CIK`·`INV_SUM_BY_CIK`.

은행(COF)은 이 생성기가 아니라 은행 세트 경로다: `build.py T --data`(cfg에 `no_dcf`)로 복제·배열 → `research/bank_gate_T.json`·`bank_items.json`(필요하면 `research/bank_equity_override.json`) → `adapters/bank_card.py T --json v2/T_bank.json` → 은행 채우기 스크립트(`v2/newcards/bank/cof_fill.py`, 설명은 그 폴더 README) → `sync_fallbacks.py`.

`BUILD['no_dcf']`(사유 문자열): 현금흐름 모델 미적용 — DCF 블록을 사유만 남긴 빈 값으로 두고 카드가 BRKB처럼 "판정 보류"(보험사 CB, 2026-10-02 사용자 결정).

cfg 선택 항목: `NI_TAGS`(분기 순이익 태그 — PH는 2021년 뒤 ProfitLoss), `OP_DISPLAY`(영업이익 줄이 없는 종목의 카드 표시용 영업이익 — CB 세전이익 + 이자비용, 엔진 배수에는 안 씀), `SELF_SPAN`(자기 이력이 5년보다 짧을 때 "5년" 표기를 바꿈 — DHR·BA), `GROWTH_SPAN`(현금흐름 역산 설명의 "지난 5년"을 실제 이력으로 — DHR).

## 새 종목 순서

1. 시총 순위 확인(StockAnalysis `marketCap`). `scripts/fetch_eps_history.py` CIKS·KNOWN_SPLITS, `v2/build_activity_score.py` CIKS, `v2/sectors.json`에 등록.
2. `meta/{t}.json`을 쓰고(앞 카드의 `next`도 고친다), Yahoo 일봉을 `yahoo/{t}.json`으로 받는다 —
   `curl -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/T?period1=1577836800&period2=1791590400&interval=1d&events=div%2Csplits"`
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
- **영업이익 줄이 없는 손익계산서** — 세전이익에서 영업외 항목을 되돌려 `DERIVED_OPINC`(COP·TJX·BX). **재고 태그 이름**이 InventoryNet이 아니면 당좌비율 = 유동비율, 재고 0일이 된다(BA).
- **주식 수** — Up-C(BX)는 교환 가능한 파트너십 지분을 현금흐름 주식 수에 더한다(`build_dcf.UNITS_EXTRA`). 적자·흑자가 섞인 해의 4분기 EPS는 보도자료와 대조(BA `Q4_EPS_OVERRIDE`).

## 분사 종목 (GE·DELL·IBM·WDC·T)

`RESTATED_LATEST`, 자기 이력 창(`build_multiple_history.HISTORY_START`)은 **재작성 숫자가 처음 공시된 날** — 첫 분사 후 재무상태표 날이 아니다(WDC는 그 사이 PSR이 29.8배로 튀었다). 최근 4분기 합이 모두 분사 뒤 분기여야 한다(T). DCF 이력(`build_dcf.HISTORY_WINDOW`)은 네 분기가 모두 재작성인 첫 최근 4분기 합부터(WDC는 영업이익이 FY24 분기에서 섞였다). 백테스트는 `bt_start`로 같은 날부터.

## 다시 만들 때

**재현 모드(`--from-card`, 2026-10-05)** — 배열(일봉·이동평균·백테스트)을 루트 카드가 아니라 지금 v2 카드의 사본에서 옮겨, 가격·날짜가 그 카드와 같다. 생성기·cfg를 고친 뒤 카드가 바뀌지 않았는지 볼 때 쓴다: `git show HEAD:v2/T_full_widget.html > /tmp/T_h.html; python3 v2/newcards/build.py T --from-card; python3 v2/newcards/compare_render.py T /tmp/T_h.html`(보이는 글자·툴팁 줄 비교) + `node v2/research/extract_card_verdicts.js`(판정 칸). 복제본에서 돌릴 때는 `--sync-base http://localhost:PORT`. 카드에 직접 고친 내용은 반드시 cfg나 fill.py에도 넣는다 — 안 넣으면 다시 만들 때 되돌아간다(2026-10-05 생성기 카드 43장 점검에서 36장이 그랬다).

cfg 문장에 계산값을 숫자로 적지 말고 `{표현식}`으로 — 틀 통일로 옮긴 cfg에 남은 리터럴은 안건 E26.

`build.py`는 카드를 덮어쓴다. 비교군(카드 유니버스 가격)은 매일 갱신되므로 같은 cfg로 다시 만들어도 동종업 점수가 조금 달라질 수 있다(WDC 55.3 → 56.8, 2026-10-02) — 판정이 바뀌면 cfg의 VOTES·문장도 고친다(fill.py가 assert로 멈춘다).
