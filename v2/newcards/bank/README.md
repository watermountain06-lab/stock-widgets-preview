# 은행 카드 채우기 스크립트 (v2/newcards/bank)

은행 세트(사전 등록 `v2/research/bank_rim_prereg.md`) 카드는 `newcards/fill.py`가 아니라 종목별 채우기 스크립트로 만든다. 세션 임시 폴더에 있던 것을 2026-10-02 저장소로 옮겼다. JPM 스크립트는 남아 있지 않아 2026-10-05 다시 만들었다(아래 JPM 항목).

| 파일 | 하는 일 |
|---|---|
| `{t}_rebuild.sh` | 한 번에 다시 만들기 — `bank_card.py`(관문·RIM·자기 이력·동종업 → `v2/{T}_bank.json`) → 기반 HTML 복사 → `{t}_fill.py` → `unify_js.py`(은행 공통 화면 규칙) → `sync_fallbacks.py` → JS 문법 검사 |
| `{t}_fill.py` | 기반 HTML(복제 + 배열)에 은행 데이터·문장을 채운다. 틀 문자열이 정확히 한 번씩 있는지 확인하며 바꾸므로 기반이 바뀌면 멈춘다 |
| `base/{t}_base.html` | 채우기 직전 카드(복제 + 배열). 루트 카드가 있는 은행은 `clone_card.py` + `{t}_arrays.py`, COF는 `build.py COF --data`로 만든 것 |
| `{t}_arrays.py` | 루트 카드(또는 인자로 준 카드 사본)의 일봉·배열을 v2 카드로 옮긴다 |

기반 갱신(2026-10-05, 9장 모두)
- 기반 HTML은 10-02 NVDA 틀로 만들어져 그 뒤 전 카드에 직접 넣은 화면 규칙(C14 끝난 분기 적중률·days_*, A9 흑자 초기, A7 경계, C1·C11 동종업, 음수 내재가치 표시, E13 문구 등)이 없었다 — 다시 만들면 그 규칙이 빠졌다. 9장 모두 지금 NVDA 틀을 `clone_card.py {T} --force`로 복제하고 `{t}_arrays.py <지금 카드 사본>`으로 그 카드의 배열을 넣어 기반을 다시 만들었다(COF는 루트 카드가 없어 `cof_arrays.py`를 새로).
- 지금 틀에는 은행 카드가 받지 않은 변경(A3 PER 해당 없음, 쏠림 안내, 일반 카드용 음수 시나리오 표기 등)이 있어 각 `{t}_fill.py` 6절에서 되돌린다(JPM에서 시작). 은행 공통 화면 규칙은 채우기 뒤 `unify_js.py`가 넣는다.
- 채우기 스크립트는 2026-10-05 상태(관문 개정 — BAC·WFC·COF 판정, AXP는 G1만 미통과로 보류였다가 같은 날 6판 10-1 영업권 이어쓰기로 고평가, SCHW 보류, 동종업 보정값)에 맞췄다. 확인: 9장 모두 정상 경로(`bank_card.py`부터)로 다시 만들면 커밋된 카드와 같다 — 다른 것은 GS·MS·WFC 동종업 차트의 BAC 막대가 9/29 값 1.87(손으로 넣었던 9/30 값 1.85를 바로잡음)과 공백 한 곳.
- `SKIP_BANK_CARD=1`(C는 `SKIP_BANK`도)이면 `bank_card.py`를 건너뛰고 지금 `{T}_bank.json`·`peer_universe/banks.json`으로 채운다(재현 확인용). 비교군 파일 날짜가 카드와 다르면 차트 값이 달라질 수 있다(경고 출력).
- JPM: `jpm_fill.py`는 `wfc_fill.py` 틀에 JPM 카드(ad61582)의 문장·손입력 값을 옮긴 것이다(2026-10-05 복원). 카드는 9/25 자료다.

다시 만들기: `bash v2/newcards/bank/{t}_rebuild.sh`(저장소 루트 기준 경로). 일봉을 새로 받으면 기반 HTML부터 다시 만든다 — COF는 `python3 v2/newcards/build.py COF --data` 뒤 `cp v2/COF_full_widget.html v2/newcards/bank/base/cof_base.html`.

주의
- 채우기 스크립트는 `v2/{T}_bank.json`과 `v2/peer_universe/banks.json`이 같은 때 만든 것이라고 가정한다(동종업 수 확인). `bank_card.py`를 건너뛰고 채우기만 돌리면 비교군 파일이 그 뒤 갱신된 은행(BAC·GS·WFC)은 확인에서 멈추고, MS는 비교 차트 값이 바뀐다(2026-10-02 확인). 반드시 `rebuild.sh`로 돌린다. 2026-10-02 네 장을 `rebuild.sh`로 다시 돌린 결과, C 데이터 보충 뒤 C의 P/TBV가 계산되어 비교 은행이 한 곳 늘어난 것이 차이의 원인이었다(판정은 네 장 모두 그대로).
- `peer_universe/banks.json`은 마지막으로 돌린 은행의 기준일로 덮어써진다. GS·MS·WFC 일봉은 9/29에서 끝나 그 뒤에는 기준일이 9/29가 되므로, 여러 장을 돌리면 9/30 기준 은행(BAC·COF 등)을 마지막에 돌린다.
- C는 `ixbrl_supplement.py`를 먼저 돌린다(스크립트에 포함). GS·MS·COF의 `rebuild.sh`는 SCHW 것을 그대로 옮겨 만들었다 — MS 우선주 오버레이(`adapters/ms_preferred.py`) 등 앞 단계가 필요하면 그 종목 `{t}_fill.py` 머리 설명을 먼저 본다.
- 손입력 값(분기 순수익·순이익, 자본비율, 뉴스·애널리스트)은 스크립트 안에 있다. 다음 분기 갱신 때 보도자료로 고친다.
