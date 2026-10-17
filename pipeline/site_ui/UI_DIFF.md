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

규칙: preview 전용 기능은 본체를 `preview-only.*`에 두고, index.html에는 꼬리표(`preview-only:<이름>`)를 단 **독립된 줄**로만
연결한다(기존 줄 안에 끼우지 않는다). 새 기능을 더하면 이 표와 `check_live_leak.py`의 식별자 목록을 함께 늘린다.

## 2. 승격 후보 — preview에만 있고, 라이브로 갈지는 사용자가 정한다

표식 없이 제자리에 있다. 옮길 때는 묶음 단위로 함께 옮긴다.

| 묶음 | 함께 옮길 것 (index.html) |
|---|---|
| 탭 4개 | `#tab-bar` 버튼 HTML(라이브의 `<h2>매력도별 종목</h2>` 자리), 탭 클릭 처리, 기본 `view = 'rank'`, 순위별 보기를 표로(`function card()` 삭제, `panel.classList.add('table-view')`, 카드 분기 삭제, caption의 `rank:` 항목) — 라이브 render()의 sector·change 분기는 이미 있다 |
| 즐겨찾기 | `.fav-toggle`·`.fav-btn` CSS, `#data-panel` 7열 너비 CSS(즐겨찾기 열과 반드시 함께), "즐겨찾기만 보기" 체크박스, `FAV_KEY`·`favorites`·`saveFavorites`·`STAR`·`favCell`, 필터의 `(!favOnly || favorites.has(d.ticker))`, ★ 머리칸과 칸, 빈 목록 문구, ★ 클릭 처리 |

## 3. 라이브로 옮길 때 되돌리거나 빼는 것

| 무엇 | preview | 라이브 |
|---|---|---|
| 카드 경로 `today.js` | `const card=t=>''+encodeURIComponent(t)+…` | `'cards/'+` |
| 카드 경로 `value-gap.js` | `href="' + esc(s.ticker)` | `href="cards/' + esc(s.ticker)` |
| index.html STOCKS_DATA 전용 `<script>` | 있음(build_index.py·validate와 라이브 build_home.py·승격 관문이 읽는다) | 옮기지 않는다 |
| index.html `stock-data.js?v=` | `preview-1` | 라이브 값 유지 |

## 4. 승격 순서 (사용자가 말할 때만)

1. 사용자가 고른 2절 묶음을 라이브 작업 트리에 옮긴다. 1절 꼬리표 줄과 `preview-only.*`는 옮기지 않고, 3절을 적용한다.
2. 라이브에서 `python3 tooling/build_static.py`(dist 사본).
3. `python3 ~/Workspace/stock-widgets-preview/pipeline/site_ui/check_live_leak.py ~/Workspace/stock-widgets-redesign` — 커밋 전.
4. 라이브 `python3 -m unittest discover -s tooling`, 로컬 서버로 화면 확인.
5. 사용자 승인 뒤 라이브 커밋·push. 옮긴 묶음을 2절에서 지운다.

한계: 누출 검사는 꼬리표·식별자만 본다. 꼬리표를 빼먹은 preview 전용 코드와 3절 경로 되돌리기 누락은 못 잡는다 —
4번 화면 확인과 라이브 diff가 최종 확인이다.

## 등락률별 순위 숫자 (2026-10-17 결정)

순위 칸 숫자는 언제나 현재 등록된 전체 종목 기준이다. 구간·검색·즐겨찾기는 보이는 행만 줄인다. 동률은 비교 함수에
규칙이 없고, 지금은 저장 순서(시총 순)와 안정 정렬 때문에 시총 순으로 갈린다(약속이 아닌 현재 관찰).
