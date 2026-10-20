# preview 화면과 라이브 화면의 차이

2026-10-17 사용자 결정(dr 5라운드 합의). 화면 코드(index.html·today.html·market-news.html과 그 CSS·JS)는
**preview가 원본**이다. 디자인·구현은 preview에서 먼저 만들고, 사용자가 말할 때만 라이브
(stock-widgets-redesign, stock-as.kro.kr)로 손으로 옮긴다. 라이브 화면 파일은 직접 고치지 않는다 — 고친 일이
생기면 그 변경을 preview에 손으로 옮긴다(자동 검사 없음, 잊으면 다음 승격이 덮어쓴다).
자동 승격(라이브 `scripts/auto_promote.sh`)은 카드와 데이터 파일만 옮기고 화면 파일은 옮기지 않는다.

이 파일은 사람용이다. 기계 검사는 `check_live_leak.py` 하나다.

## 1. preview 전용 — 라이브로 옮기지 않는다

| 이름 | 무엇 | 위치 |
|---|---|---|
| `range` | 시총 순위 구간 토글 [전체][1~100위][101~200위] | `preview-only.js`, `preview-only.css`, index.html의 `preview-only:range` 꼬리표 줄 4개(파일 싣기 2, 필터 1, 초기화 1) |
| `portfolio` | Google 로그인(Firebase, 나만 쓰기)으로 여는 Portfolio 탭(원칙·실제 자산·관심 종목·모의 운용 기록, 2026-10-19). 머리 메뉴에 `Portfolio` 링크를 덧붙인다 | `preview-only-portfolio.html`·`.js`·`.css`·`-config.js`, 설정 순서 `pipeline/portfolio/SETUP.md`, 전략 비교 설계 `pipeline/portfolio/STRATEGY_DESIGN.md`와 일별 고정 기록 `site_data/strategy_ledger/`(`pipeline/site_ui/build_strategy_ledger.py`, 공개 시세·판정만, 2026-10-19), 재생 엔진 `preview-only-portfolio-engine.js`, 전략 비교·기록 관리 구역 `preview-only-portfolio-strategy.js`, 하위 탭과 "한눈에"(내 자산·실제 매매 기록·이번 달 운용·전략 도넛) `preview-only-portfolio-home.js`(시험 `pipeline/portfolio/test_strategy_engine.mjs`·`test_strategy_view.mjs`, 2026-10-20), 규칙 틀 `firestore.rules`(이메일은 자리표시자 — 실제 값은 Firebase 콘솔에만), 가짜 데이터 `sample.json`, `preview-only.js` 아래쪽 메뉴 함수, today.html·market-news.html의 `preview-only:portfolio` 꼬리표 줄 1개씩(index.html은 range 줄이 같은 파일을 싣는다) |
| `etf` | 홈 "시장 지표" 접힘 구역 맨 위의 ETF 선택 칩과 요약 줄(판정·점수·덮은 비중·등급 막대·상위 5개), ETF 카드 페이지(2026-10-19, 첫 ETF SPY). 참고용·매수 기준 아님, 규칙은 `v2/research/etf_verdict_prereg.md` | `preview-only-etf.js`·`.css`, 별도 워크플로 `etf_index.yml`이 쓰는 `preview-only-etf-data.js`·`preview-only-etf-spy.html`·`v2/etf/date_obs.jsonl`(`v2/etf/etf_daily.py`, 대체 `etf_fallback.py`, 알림 `etf_alerts.py`, 승인 `etf_approve.py`·`etf_approve.yml`, 승인 원문 `v2/etf/approved_src/`), index.html의 `preview-only:etf` 꼬리표 줄 3개(CSS·데이터·JS, JS는 `?v=2` — 갱신 대기 표시) |
| `index` | S&P 500 지수 카드(2026-10-20): 종목 카드(NVDA_full_widget.html)와 같은 틀 — 머리(현재가, 요약 4칸: 1년 수익률·5년 연 환산·PER(SSGA 지수)·이익수익률 vs 미 10년 국채, "판정하지 않는다" 한 줄), 일봉 캔들+MA5·20·60·120(1개월~5년, 시작점 = 기간별 수익률 기준일), 아래 탭 4개(기간별 수익률 / 월별 등락률 / 구성 종목 / 시계열 사건 — 종목 카드 4색). 시세 계산은 FRED SP500 대조 구간(최근 10년)만 써서 "사상 최고"가 아니라 "구간 최고". 구성 종목 탭·머리 PER·국채는 SSGA SPY 펀드 페이지(업종 비중·PER), FRED DGS10, v2/etf/SPY.json(상위 10개·카드 판정 비중)을 읽고, 못 읽으면 그 칸만 비운다. 홈 시장 지표 S&P 500 칸 아래 링크, SPY 카드와 서로 링크 | 별도 워크플로 `etf_index.yml`이 쓰는 `preview-only-index-sp500.html`·`v2/index/SP500.json`(`v2/index/index_daily.py`, 틀 `v2/index/template/card_head.html`(종목 카드 <head> 사본)·`index_card.html`), 홈 링크는 `preview-only-etf.js`의 `linkIndex`(index.html 변경 없음) |

portfolio의 내 데이터는 preview 저장소에 두지 않는다(저장소에는 가짜 `sample.json`만). Firestore에만 있고, 보호는 Firestore 규칙이 맡는다.
소유자 이메일은 공개 저장소 어디에도 쓰지 않는다. index.html은 range 줄의 `preview-only.js?v=2`로 메뉴 함수를 싣는다 — 그 파일을 바꾸면 index의 버전도 함께 올린다(2026-10-19 portfolio 메뉴 추가분은 etf 줄을 넣을 때 `v=2`로 올렸다).
실제 값(보유·금액)은 vault `finance/portfolio.md` 규칙을 바꾸기 전에는 넣지 않는다(2026-10-19 사용자 보류) — 그때까지 가짜 데이터만.

규칙: preview 전용 기능은 본체를 `preview-only.*`에 두고, index.html에는 꼬리표(`preview-only:<이름>`)를 단 **독립된 줄**로만
연결한다(기존 줄 안에 끼우지 않는다). 새 기능을 더하면 이 표와 `check_live_leak.py`의 식별자 목록을 함께 늘린다.

## 2. 승격 후보 — preview에만 있고, 라이브로 갈지는 사용자가 정한다

표식 없이 제자리에 있다. 옮길 때는 묶음 단위로 함께 옮긴다.

| 묶음 | 함께 옮길 것 (index.html) |
|---|---|
| 탭 4개 | `#tab-bar` 버튼 HTML(라이브의 `<h2>매력도별 종목</h2>` 자리), 탭 클릭 처리, 기본 `view = 'rank'`, 순위별 보기를 표로(`function card()` 삭제, `panel.classList.add('table-view')`, 카드 분기 삭제, caption의 `rank:` 항목) — 라이브 render()의 sector·change 분기는 이미 있다 |
| 카드 경로 데이터화 (먼저 옮길 것) | `today.js`의 `cardBase`·`card`, `value-gap.js`의 `STOCKS`·`CARD_BASE`·`cardHref`와 분기 팝업 링크. 카드 주소를 각 사이트 `stock-data.js`의 `href`에서 읽어(preview 루트, 라이브 `cards/`) 같은 코드가 두 사이트에서 그대로 맞다(2026-10-17). 옮기면 손으로 경로를 바꿀 일이 없다 — 이 묶음 없이 두 파일을 다른 이유로 옮기면 라이브 링크가 깨지므로 함께 옮긴다 |
| Tracking 날짜 한 줄 (2026-10-20) | today.html의 `.tk-days-wrap`(◀ ▶ 버튼으로 감싼 날짜 줄), today.js의 `showDay`·`navState`와 ◀ ▶ 처리, `renderDays` 끝의 `showDay()`, tracking.css 끝의 "날짜 줄" 블록, 버전 `tracking.css?v=3`·`today.js?v=tracking-3` |
| 즐겨찾기 | `.fav-toggle`·`.fav-btn` CSS, `#data-panel` 7열 너비 CSS(즐겨찾기 열과 반드시 함께), "즐겨찾기만 보기" 체크박스, `FAV_KEY`·`favorites`·`saveFavorites`·`STAR`·`favCell`, 필터의 `(!favOnly || favorites.has(d.ticker))`, ★ 머리칸과 칸, 빈 목록 문구, ★ 클릭 처리 |

## 3. 라이브로 옮길 때 되돌리거나 빼는 것

| 무엇 | preview | 라이브 |
|---|---|---|
| index.html STOCKS_DATA 전용 `<script>` | 있음(build_index.py·validate와 라이브 build_home.py·승격 관문이 읽는다) | 옮기지 않는다 |
| index.html `stock-data.js?v=` | `preview-1` | 라이브 값 유지 |

## 4. 승격 순서 (사용자가 말할 때만)

1. 사용자가 고른 2절 묶음을 라이브 작업 트리에 옮긴다. 1절 꼬리표 줄과 `preview-only.*`는 옮기지 않고, 3절을 적용한다.
2. 라이브에서 `python3 tooling/build_static.py`(dist 사본).
3. `python3 ~/Workspace/stock-widgets-preview/pipeline/site_ui/check_live_leak.py ~/Workspace/stock-widgets-redesign` — 커밋 전.
4. 라이브 `python3 -m unittest discover -s tooling`, 로컬 서버로 화면 확인.
5. 사용자 승인 뒤 라이브 커밋·push. 옮긴 묶음을 2절에서 지운다.

한계: 누출 검사는 꼬리표·식별자만 본다. 꼬리표를 빼먹은 preview 전용 코드는 못 잡는다 —
4번 화면 확인과 라이브 diff가 최종 확인이다.

## 등락률별 순위 숫자 (2026-10-17 결정)

순위 칸 숫자는 언제나 현재 등록된 전체 종목 기준이다. 구간·검색·즐겨찾기는 보이는 행만 줄인다. 동률은 비교 함수에
규칙이 없고, 지금은 저장 순서(시총 순)와 안정 정렬 때문에 시총 순으로 갈린다(약속이 아닌 현재 관찰).
