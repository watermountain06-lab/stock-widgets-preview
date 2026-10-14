# v2 카드 만들기 — 실행 절차의 기준 (2026-10-13)

**새 카드를 만들거나 다시 만드는 실행 순서는 이 파일 하나가 기준이다.** `v2/CARD_ITEMS.md`는 카드별 기록·결정이고, 그 안의 옛 "새 카드 시작 절차"(루트 카드 시절)는 따르지 않는다.
방법론·산식의 기준은 따로 있다: 은행 `v2/research/bank_rim_prereg.md`, 판정 구조 `v2/research/verdict_structure_prereg.md`, 백테스트 `v2/refresh_backtest.py` 머리 설명.
원칙(숫자 지어내지 않기, 배열 손으로 치지 않기, Codex·Fable 검토)은 `/ticker` 스킬 플레이북(stock-widgets-redesign/.claude/skills/ticker/playbook.md)과 같다.

지금 카드 103장: 비은행 생성기 카드 92장이 **AUTO**(cfg `AUTO = True` — 새 10-Q·10-K를 매일 실행이 스스로 반영하고 문장도 규칙으로 다시 쓴다), 은행 9장은 `bank/`(사전 등록 7판, 공통 `bank_fill.py`), 손 카드는 BRKB(전용 생성기 `brkb/`)·SPCX(`hand_refresh.py`)뿐이다.
매일·토요일 실행은 `daily_price.py`(GitHub Actions `.github/workflows/v2_cards.yml`)가 cfg가 있는 카드를 모두 돈다 — 새 카드를 워크플로에 따로 등록하지 않는다.

## 파일

| 파일 | 하는 일 |
|---|---|
| `build.py T [--data] [--asof D]` | 한 장을 만든다: 복제(틀 `template/NVDA_template.html`) → EPS → 배열 → 재무 → 배수·비교군·기본적 분석·활동성 → 현금흐름 → 채우기 → 대체값 → JS 검사. `--price`·`--weekly`는 매일·토요일 실행용, `--from-card`는 재현용 |
| `preflight.py T --asof D` / `--after` | 새 종목 공시 기준 검사(빌드 전 — build.py가 자동으로 부른다) / 빌드 뒤 카드 재무 접수일 = 기준표 확인 |
| `fill.py T` | 문장·표 채우기(공통). AUTO면 `auto_card.py`가 분기 칸·규칙 문장을 채운다 |
| `auto_card.py`, `quarter_auto.py`, `seg_xbrl.py` | AUTO 카드: 분기 변수(공시 기준표까지 접수된 자료로), 부문 표(인라인 XBRL), 규칙 문장(사실·숫자만 — 원인·가이던스·조정 EPS는 쓰지 않는다) |
| `seg_map_propose.py`, `…2.py`, `…3.py` | 손으로 적은 `SEG`와 맞는 XBRL 멤버를 찾아 `SEG_MAP`을 제안(2판 부분합, 3판 여러 축·나머지) |
| `fetch_analyst.py T` | cfg의 `ANALYST`·`ANALYST_ASOF`를 StockAnalysis에서 고친다(토요일 자동) |
| `news_auto.py T` | 실적 8-K(2.02항)를 `v2/news_auto.json`에 — fill.py가 뉴스 맨 위에 넣는다 |
| `daily_price.py [T…]` | 매일 실행(가격 재빌드, 새 공시 자동 승인 `auto_approve`, 백테스트 갱신, 토요일 비교군·애널리스트) |
| `check_literals.py T [--strict]` | cfg 문장에 계산값이 숫자로 박혔는지(후보 — 우연히 같은 숫자일 수 있다) |
| `compare_render.py T OLD.html` | 두 카드의 보이는 글자·툴팁 비교(배열·판정은 따로) |
| `cfg/cfg_{t}.py` | 종목별 설정. `BUILD` 사전은 빌드 옵션 |
| `meta/{t}.json`, `yahoo/{t}.json` | 새 종목 헤더(이름·업종·색·카드 순위·앞뒤 링크), Yahoo 일봉 |
| `root_arrays.py`, `aph_root_arrays_special.py` | 루트 카드 시절 배열 이식(기록) |
| `bank/` | 은행 카드(README 따로) · `brkb/` BRKB 전용 생성기 |

## 준비

- 저장소 루트에서 http 서버: `python3 -m http.server 8765`(포트를 쓰고 있으면 다른 포트 + `--sync-base http://localhost:PORT`, 은행은 `SYNC_BASE`). **그 포트가 이 저장소를 띄우고 있는지** `lsof -p $(lsof -t -iTCP:PORT -sTCP:LISTEN) | grep cwd`로 확인한다 — 다른 체크아웃을 띄운 서버가 200을 돌려준다(2026-10-13).
- Node(JS 문법 검사), Chrome(`compare_render`·`sync_fallbacks`, 경로가 다르면 `CHROME`).

## 새 종목 순서 (비은행 → AUTO 카드)

1. **순위** — `python3 ../stock-widgets-redesign/scripts/check_rank_gaps.py`(redesign 저장소에 있다). 시총 순위는 StockAnalysis `marketCap`. **카드 순위(cardRank)는 시총 순위가 아니라 카드 목록 끝 번호**(지금 104부터 — `site_data/stocks.json`, 검사기가 중복·공백을 막는다).
2. **등록** — `scripts/fetch_eps_history.py` CIKS·KNOWN_SPLITS, `v2/build_activity_score.py` CIKS, `v2/sectors.json`.
3. **헤더·일봉** — `meta/{t}.json`(`current` = "T · 시총 {cardRank}위", `prev`·`next`). 앞 카드 `meta`의 `next`도 고치고 **앞 카드를 다시 빌드**한다(meta는 복제 때만 읽힌다 — 매일 `--price` 실행도 다시 복제하므로 다음 날엔 반영되지만, 그날 양방향 링크를 확인하려면 바로). 일봉:
   `curl -A "Mozilla/5.0" "https://query1.finance.yahoo.com/v8/finance/chart/T?period1=1577836800&period2=$(date +%s)&interval=1d&events=div%2Csplits" -o v2/newcards/yahoo/t.json`
   (긴 브라우저 UA는 429. 기준일 뒤 봉은 `new_ticker_arrays.py`가 버리므로 지금 시각까지 받아도 된다). `events.splits`에 1.45 미만 비율이 있으면 분사 종목 — 아래 "분사". 일봉 1,375개(약 5.5년) 미만이면 이 경로로 못 만든다(짧은 상장 — 사용자에게 묻는다).
4. **공시 기준 먼저** — 쓰는 공시는 **SEC 요약 자료(companyfacts)에 실린 가장 최근 원본 10-Q/10-K**다(재무 수집기가 원본만 읽는다). `v2/sec_approved.json`에 `"10자리 CIK": "그 접수일"`을 넣고, 기준일(asof)은 그 공시 접수 뒤 첫 확정 세션 이상. 그 원본 뒤에 정정(10-Q/A·10-K/A)이 있으면 **멈추고 사용자에게 묻는다**(정정 처리 방침 전까지 보류). `python3 v2/newcards/preflight.py T --asof <세션>`이 이 셋을 확인한다(build.py도 새 종목이면 자동으로 부른다). **기준표에 없는 카드가 있으면 매일 실행 전체가 멈춘다**(`daily_price.check_approved`).
5. `python3 v2/newcards/build.py T --data --asof <세션>` — 숫자만. 아래 "점검"을 모두 본다.
6. **cfg** — SEC 원문(10-Q·보도자료·8-K)으로 `cfg/cfg_{t}.py`를 쓴다(비슷한 AUTO 종목 cfg를 복사해 시작). 어떤 키를 손으로 쓰는지는 아래 "cfg 키". 문장에 계산값은 숫자가 아니라 `{표현식}`. 처음부터 AUTO로 만드는 카드는 덮어써지는 키를 쓰지 않는다(VLO가 첫 사례 — `cfg/cfg_vlo.py`가 최소 cfg 본보기). `ANALYST = {...}`는 **한 줄, 줄 뒤 주석 없이**(fetch_analyst가 줄째 바꾼다 — 아니면 "ANALYST 한 줄이 없다"). **뉴스**: 최신 분기 실적은 손으로 쓰지 않는다 — `news_auto`가 SEC 숫자로 붙이는데, 그 실적 발표보다 **뒤 날짜의 손 항목이 하나라도 있으면 자동 항목이 빠진다**(fill.py). `NEWS`의 반응일(세 번째 칸)은 카드 일봉에 있는 거래일, 실적 반응일은 SEC 접수 시각(UTC)을 동부 시간으로 바꿔 16시 이후면 다음 거래일. 8-K 내용은 원문에 있는 것만(같은 날 다른 발표를 합치지 않는다).
7. **부문 지도** — `SEG`(원문 부문 표를 손으로) → `seg_map_propose.py T`(맞는 게 없으면 2판·3판) → **원문과 대조**(어느 축인지, 본사·상계 조정, 1년 전 값까지) → `ignore`·`adjust`·`strict`·`other`를 정해 `SEG_MAP`, `AUTO = True`(제안은 `seg_map_proposals.json`에 있다 — cfg 끝에 옮긴다). 빌드가 통과했다고 지도가 맞는 것은 아니다.
8. `python3 v2/newcards/fetch_analyst.py T` · `python3 v2/newcards/news_auto.py T` · `python3 v2/newcards/quarter_auto.py T --check`(cfg 씨앗 분기 변수와 자동 값이 같아야 — 다르면 종료 코드 1. **새 종목 T만** 돌린다 — 인자 없이 돌리면 분기가 바뀐 옛 카드의 낡은 씨앗(MU·PEP·TENQ 등 8장, 2026-10-13)이 어긋남으로 나오지만 빌드는 자동 값을 쓰므로 영향 없다).
9. `python3 v2/newcards/build.py T --asof <세션>`(첫 빌드는 `REFRESH=1`을 붙여 계산된 판정을 cfg `VOTES`에 쓰게 하고, 값을 확인한다) → **현행 백테스트 규칙**: `python3 v2/build_backtest_pre.py T`(연구 가격 캐시에 없는 종목은 `--yahoo T`, "가격 없음 — 만들지 않음"이 나오면 산출물이 없는 것) → `python3 v2/refresh_backtest.py T` → `python3 v2/sync_fallbacks.py T [--base …]` → `python3 v2/newcards/check_literals.py T --strict`(0곳, 남으면 검토).
10. **확인** — 브라우저(콘솔 오류 0, NVDA 틀 잔재 `grep -i "nvda\|nvidia\|FY27\|확인 필요"`, 구성요소 개수 `detail-toggle` 2·`val-item` 5·`data-fund-metric=` 5) → Codex → Fable(비판만) → 고치고 Codex 2차. `python3 v2/newcards/preflight.py T --after`(카드 재무 접수일 = 기준표, 매일 재빌드 고리 없음).
11. **홈 등록** — `python3 pipeline/add_v2_ticker.py T`(stocks.json 항목: 카드 순위·이름·업종·주식 수) (가격 칸도 카드 일봉 마지막 두 종가로 채운다 — **`fetch_prices.py --tickers T`는 쓰지 않는다**: 나머지 종목을 "stale"로 바꾸고, 장 마감 뒤에는 홈 가격 세션을 다음 날로 올린다(MO 2026-10-13)) → 로고 `logos/{t}.png` → `python3 pipeline/sync_v2_home.py`(루트로 복사, 등급·점수·등급 이력 — **바뀐 v2 카드를 전부 복사하므로 다른 카드 빌드가 도는 중에는 돌리지 않는다**, 반쯤 쓴 카드가 루트로 간다) → `python3 pipeline/build_index.py` → `python3 pipeline/validate_site_data.py`.
12. **매일 실행 시험** — `python3 v2/newcards/daily_price.py T`(상태 단어 확인 — 카드를 새 종가로 다시 만든다, 리뷰 뒤에 돌린다). 이 시험은 `v2/daily_status.json`을 그 종목 하나로 덮어쓴다 — 커밋 전에 `git checkout v2/daily_status.json`.
13. **기록** — `v2/CARD_ITEMS.md` 카드 절, 공통 과제는 `v2/research/after_100_cards_agenda.md` 사례. 라이브(redesign) 승격은 사용자가 말할 때만(`sync_cards.py`·`build_home.py`·`build_value_gap`).

## cfg 키 (AUTO 카드)

| 구분 | 키 |
|---|---|
| 손으로 쓰고 쓰이는 키 | CO·CIK·S_·SEC·LINKS·PR(손 링크 사전 — auto가 `auto` 링크를 합치고 뉴스가 쓴다)·PH·PEER_FILE·CHART_TITLES·CHART_CAP·SELF_CAP·CHART_NOTE·PEER_NAME_TITLE·PEER_COMMENT·PEER_TIP·NEWS·NEWS_RANGE·ANALYST·ANALYST_ASOF·FAIRBAND_TITLE·HEADER_REQ_LABEL·SEG_TITLE·Y2·NONOP_WHAT·SEG_MAP·AUTO·BUILD·PRE/POST·VOTES/VERDICT(첫 빌드 `REFRESH=1`로 계산값) |
| 씨앗값(cfg에 있어야 하고 auto가 매번 다시 정함) | CUR·QLABEL(없으면 멈춤 — 이름 꼴과 회계연도를 여기서 읽는다)·FY_LABEL·TENQ_NAME(없으면 기본 꼴로 조용히 진행 — 꼴이 맞는지 `quarter_auto --check`로)·YO·QO·YL·QQL·L8·TENQ·FY_ENDS·FY_NAME_OFFSET(필요하면) |
| 씨앗값(검사 기준) | SEG_ADJ — 원문에서 확인한 본사·상계 조정액. 부문 합 검사의 허용 기준(같은 부호 0.5~1.5배)으로 읽은 뒤 다시 정한다. 0이면 매출 3% 규칙만 남아 큰 조정이 있는 종목(GLW·TMO)은 멈춘다. SEC 자동 카드만(AUTO_OUTSIDE는 0) |
| 제안기 입력 | SEG(seg_map_propose 입력 — 채울 때는 SEG_MAP에서 다시 만든다) |
| auto가 덮어써 손으로 쓰지 않는 키 | SUMMARY·BULL·BEAR·PREMISE·RISK·STORIES·DCF_NOTE·HEALTH_NOTE·FUND_TIP·SELF_TIP·CHECK·CHECK_WHEN·YOY_EXTRA·SEG_NOTE·STAT3·CAPITAL·NEXT·NEXT_OP·FUND_ASOF_NOTE·OPM_RANGE·PR_CUR·FCF_SUB·CAPEX_SUB, RELEASE는 비움 |
| 있을 때만 | CAPEX_LABEL(설비투자 태그가 다른 지출을 합칠 때 FCF·설비투자 칸 이름 — VLO)·OP_DISPLAY·NI_TAGS·SELF_SPAN·GROWTH_SPAN·REVERSE·ACT_REASON·REQ_MULT_EXACT·PBR_GAP_NEG_EQUITY·NO_DCF_SKEW·NONOP_NEG_SIGN·AUTO_OUTSIDE(외국 발행사 — ASML·TSM 6-K, SKHY OpenDART) |

`BUILD` 옵션: `overlay`(companyfacts 지연 — 인라인 XBRL 보충, 또는 재무 태그 별칭·합 `adapters/overlay_feed.py`의 `ALIAS`·`SUM`·`REPLACE`), `company_tags`(회사 고유 태그 — COP·PSX 설비투자, LMT 감가상각, NEM 재고·리스. 보충 자료는 `.sec_cache/overlay`에만 있고 Actions 캐시는 토요일에만 저장되므로, 캐시에 그 행이 없으면 매일 실행도 받아 온다 — 2026-10-13 PSX가 그날 밤 설비투자 없이 빌드됐다), `feed`(외국 기업 어댑터 `v2/adapters/{t}_feed.py`), `eps_cmd`(V), `eps_tag`(분사 종목 계속사업 EPS — WDC), `bt_start`(백테스트 시작일 — WDC·T), `sum_tags`(XOM 재고), `share_events`(분기 뒤 주식 발행), `no_dcf`(사유 — 현금흐름 미적용, "판정 보류": 보험 CB·PGR, 은행 기반 HTML 제작용 COF). 활동성 예외는 `build_activity_score.py`의 `COGS_TAG_BY_CIK`·`INV_SUM_BY_CIK`.

## 점검 (`--data` 뒤, cfg 쓰기 전)

- **분기 표가 기준 공시까지 있나** — 없으면 companyfacts 지연. `BUILD['overlay']=True`. 보충 전에 만든 배열·백테스트는 다시 만든다(ABT).
- **매출·영업이익을 10-Q 손익계산서와 대조** — 영업이익 줄이 없으면 `DERIVED_OPINC`(ETN·PFE·WELL·COP·TJX·BX), 매출 태그가 섞이면 `EXCLUDE_TAGS`·`EXTRA_TAGS`·`PREFER_TAGS`(PFE·NEE·WELL).
- **차입금·현금·단기투자·리스·우선주·비지배지분을 재무상태표와 대조** — 경고 `N일 뒤처짐`은 멈춘 태그다(옛 값이 조용히 쓰인다): 1년 안 만기 누락(ETN·T·UNP), 멈춘 단기투자(T·MCD·PFE), 차입금 2012년 태그(MPC), 리스에 금융리스 포함(MCD), `⚠ 데이터 품질: debt_total_fallback`(공정가치 주석의 금융리스 뺀 차입금으로 대체됨 — VLO는 재무상태표 두 줄로 고침). **설비투자(capex) 경고도 같다** — 현금흐름표 줄이 차원으로만 태깅되면 멈춘다(VLO 2026 10-Q, VIE 차원 → `EXTRA_TAGS`로 대체 태그). 고칠 곳 `build_multiple_history.py`의 `DEBT_TOTAL_TAG`·`EV_TAGS_BY_CIK`. `⚠ 데이터 품질: debt_suspect` → 10-Q 총차입금과 대조, 비유동분만 태깅하면 `DEBT_NONCURRENT_ONLY`.
- **감가상각** — EV/EBITDA 5년 최고가 수십~수백 배거나 EBITDA가 영업이익과 거의 같으면 D&A 태그가 일부 줄만 잡은 것이다(VLO 판관비 줄 D&A, AMGN, MCD) → `EXCLUDE_TAGS`로 빼고 현금흐름표 D&A와 대조. DCF 순투자(설비투자 − 감가상각)도 같은 값을 쓴다.
- **주식 수** — 다중 클래스는 `v2/adapters/cover_shares.py`(META), Up-C는 `build_dcf.UNITS_EXTRA`(BX), 단위 오류(MCD).
- **1차 출처로 확인할 입력** — 금액을 밝힌 일회성 법인세 `v2/tax_oneoff.json`(META), 성과 조건부 제한주 `v2/share_adjust.json`(TSLA), 표준 태그 없는 비영업 자산 `v2/nonop_extra.json`(비상장 지분·지분법·암호자산, 이미 단기투자에 든 상장주식은 `exclude`), 본업 기준 `v2/core_earnings.json`((세전 − 영업) ÷ 영업 ≥ 20%).
- **4분기 EPS** — "연간 − 9개월" 역산을 보도자료 4분기 희석 EPS와 대조, 다르면 `Q4_EPS_OVERRIDE`(BA·UBER·FTNT·CRWD·COF).
- **현금흐름 시나리오** — 음수·순서 역전은 원인을 찾는다(문장은 auto가 쓰지만 원인 확인은 사람). 인수 대금이 큰 해는 매출/자본이 극단적이다.
- **비교군** — S&P500 섹터 파일을 처음 만들면 이상값부터(부동산).
- **틀 구조 불변** — 블록을 지우거나 새로 짜지 않는다. 안 맞는 칸은 같은 자리에 "해당 없음"과 이유.

## 은행 (비교군 S&P500 은행, 사전 등록 7판)

1. 위 1~4(순위·등록·meta·일봉·공시 기준).
2. 기반 HTML: `newcards/cfg/cfg_{t}.py`에 `CIK`와 `BUILD = {'no_dcf': '은행 — RIM으로 따로 계산'}`만 두고(일반 현금흐름 계산을 건너뛰게 — COF 선례 `cfg/cfg_cof.py`) `build.py T --data --asof <세션>` → 결과 카드를 `bank/base/{t}_base.html`로 복사.
3. `bank/cfg/cfg_{t}.py`(CIK·CO·REV_TAG·PB·COLOR·BV_NOTE·ANALYST·NEWS=[] — 기존 은행 cfg 참고), `daily_price.BANKS`(순서 유지 — COF 먼저), `v2/adapters/bank_sec_values.py` `CARDS`, 우선주가 있으면 `v2/research/bank_sec_tags.json`, `v2/bank_items.json`(특별 항목), `fundamental_score_config_v1.json` `bank_exclude_tickers`, `sec_approved.json`.
4. `bash v2/newcards/bank/rebuild.sh T` → 현행 백테스트(`build_backtest_pre.py T` → `refresh_backtest.py T`) → 카드의 `BACKTEST`를 `bank/base/{t}_base.html`에도 옮기고(`daily_price.py`의 은행 백테스트 처리와 같은 방식) `rebuild.sh T`를 다시 돌려 남는지 확인.
5. `peer_universe/banks.json`은 `bank_card.py`가 S&P500 Diversified·Regional Banks에서 만드는 **산출물**이다 — 손으로 고치지 않는다. 기준일은 마지막으로 돌린 은행의 것이라 여러 장을 돌리면 최신 기준일 은행을 마지막에 돌린다.
6. 홈 등록·기록은 위 11~13과 같다.

## 분사 종목 (GE·DELL·IBM·WDC·T)

**분사가 끝났는데 아직 재작성 숫자가 없으면 만들지 않는다** — 공시 재무에는 떨어져 나간 사업이 남아 있고 주가는 분사 뒤라 PER·DCF가 섞인다. 10-Q의 "discontinued operations" 문단으로 재작성 시점을 확인하고 그 보고서 뒤로 미룬다(SPGI: Mobility 2026-07-01 분사, Q3 2026 10-Q부터 재작성 — 2026-10-13 보류). 교환 공개매수(split-off)도 같다 — 끝나면 주식 수가 바로 줄고 재무는 다음 보고서에서 재작성된다(MDT: MiniMed 교환 2026-10-09 마감, 보류). 진행 여부는 8-K 1.01·2.01항과 SC TO-I/A로 본다.

`RESTATED_LATEST`, 자기 이력 창(`build_multiple_history.HISTORY_START`)은 **재작성 숫자가 처음 공시된 날**. 최근 4분기 합이 모두 분사 뒤 분기여야 한다(T). DCF 이력(`build_dcf.HISTORY_WINDOW`)은 네 분기가 모두 재작성인 첫 최근 4분기 합부터. 백테스트는 `bt_start`로 같은 날부터.

## 다시 만들 때

**재현 모드(`--from-card`)** — 배열을 지금 v2 카드 사본에서 옮겨 가격·날짜가 같다(EPS·재무·비교군은 새로 받으므로 자료 변화로도 숫자가 바뀔 수 있다). 생성기·cfg를 고친 뒤:
`git show HEAD:v2/T_full_widget.html > /tmp/T_h.html; python3 v2/newcards/build.py T --from-card; python3 v2/newcards/compare_render.py T /tmp/T_h.html` + `node v2/research/extract_card_verdicts.js`(판정 칸). 카드에 직접 고친 내용은 반드시 cfg나 fill.py에도 넣는다.

`build.py`는 카드를 덮어쓴다. 비교군 가격은 매일 바뀌므로 같은 cfg로 다시 만들어도 동종업 점수가 조금 달라질 수 있다 — 판정이 바뀌면 cfg `VOTES`도 고친다(`REFRESH=1`이면 자동, 아니면 fill.py가 멈춘다).

## 함정 기록 (2026-10-13 고침)

- `build.py --asof` 기본값이 2026-09-30에 고정돼 새 카드가 9/30에서 잘리거나 no_dcf 카드의 asOf에 박혔다 → 새 종목만 필수, 나머지는 카드 일봉 마지막 날.
- `new_ticker_arrays.py`가 백테스트 실패에도 옛 `/tmp` 결과를 읽을 수 있었다 → 실행마다 새 임시 폴더, 실패하면 멈춤.
- 은행 예외가 COF 이름으로 하드코딩 → `bank/cfg` 목록(`check_peer_drift.py`·`quarter_auto.py`·`seg_map_propose.py`).
- `quarter_auto --check`·`check_literals`가 어긋남·오류에도 종료 코드 0 → 비정상 종료.
- `compare_render`가 양쪽 렌더 실패(빈 출력)를 "같음"으로 → 렌더 실패면 멈춤.
- 새 카드의 공시 기준을 고르는 단계가 없어 재무(원본)와 배수·활동성(정정)이 섞일 수 있었다 → `preflight.py`.
- 남은 과제: 기존 AUTO 카드의 정정 공시 처리(자동 승인이 10-Q/A·10-K/A를 받으면 재무 접수일과 어긋나 그 카드가 매일 `--weekly`로 돈다) — 사용자 결정 대기.
