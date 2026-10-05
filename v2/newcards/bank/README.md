# 은행 카드 채우기 스크립트 (v2/newcards/bank)

은행 세트(사전 등록 `v2/research/bank_rim_prereg.md`) 카드는 `newcards/fill.py`가 아니라 종목별 채우기 스크립트로 만든다. 세션 임시 폴더에 있던 것을 2026-10-02 저장소로 옮겼다. JPM 스크립트는 남아 있지 않아 2026-10-05 다시 만들었다(아래 JPM 항목).

| 파일 | 하는 일 |
|---|---|
| `{t}_rebuild.sh` | 한 번에 다시 만들기 — `bank_card.py`(관문·RIM·자기 이력·동종업 → `v2/{T}_bank.json`) → 기반 HTML 복사 → `{t}_fill.py` → `sync_fallbacks.py` → JS 문법 검사 |
| `{t}_fill.py` | 기반 HTML(복제 + 배열)에 은행 데이터·문장을 채운다. 틀 문자열이 정확히 한 번씩 있는지 확인하며 바꾸므로 기반이 바뀌면 멈춘다 |
| `base/{t}_base.html` | 채우기 직전 카드(복제 + 배열). 루트 카드가 있는 은행은 `clone_card.py` + `{t}_arrays.py`, COF는 `build.py COF --data`로 만든 것 |
| `{t}_arrays.py` | 루트 카드 일봉·배열을 v2 카드로 옮긴다(루트 카드 있는 은행만) |

JPM(2026-10-05 복원)
- `jpm_fill.py`는 `wfc_fill.py` 틀에 그때 `v2/JPM_full_widget.html`(ad61582)의 문장·손입력 값을 옮긴 것이다. `base/jpm_base.html`은 지금 NVDA 틀을 `clone_card.py JPM --force`로 복제하고 `jpm_arrays.py <그 카드 사본>`으로 그 카드의 배열(마지막 봉 2026-09-25)을 넣어 만들었다. 이 기반 + 그때의 `JPM_bank.json` + 9/25 기준 `peer_universe/banks.json`(16b9e28)으로 채우기 → `unify_js.py` → `sync_fallbacks.py`를 돌리면 카드가 바이트 단위로 같게 나온다(sync 전에는 대체값 52곳만 다르다).
- 지금 NVDA 틀에는 은행 카드가 받지 않은 변경(A3 PER 해당 없음, 쏠림 안내, 음수 시나리오 표기)이 있어 `jpm_fill.py` 6절에서 되돌린다. 다른 은행 기반은 10-02 틀이라 이 절이 없다.
- 동종업 문장(C·HBAN 사정, 비교 은행 8곳·12곳, 유형자본 결측 은행)과 위험 문장(현재가 ÷ 기본 가치 1.51)은 2026-09-27 데이터에 맞춘 손문장이라, 값이 바뀌면 확인에서 멈춘다. 2026-10-05에 `bank_card.py JPM`을 다시 돌려 보니 C의 P/TBV가 계산되어 P/TBV 비교 은행이 9곳, PER 순위 12/12(점수 8.3)로 바뀌므로, `rebuild.sh`는 이 문장들을 고칠 때까지 멈춘다(판정은 그대로 고평가 −4).

다시 만들기: `bash v2/newcards/bank/{t}_rebuild.sh`(저장소 루트 기준 경로). 일봉을 새로 받으면 기반 HTML부터 다시 만든다 — COF는 `python3 v2/newcards/build.py COF --data` 뒤 `cp v2/COF_full_widget.html v2/newcards/bank/base/cof_base.html`.

주의
- 채우기 스크립트는 `v2/{T}_bank.json`과 `v2/peer_universe/banks.json`이 같은 때 만든 것이라고 가정한다(동종업 수 확인). `bank_card.py`를 건너뛰고 채우기만 돌리면 비교군 파일이 그 뒤 갱신된 은행(BAC·GS·WFC)은 확인에서 멈추고, MS는 비교 차트 값이 바뀐다(2026-10-02 확인). 반드시 `rebuild.sh`로 돌린다. 2026-10-02 네 장을 `rebuild.sh`로 다시 돌린 결과, C 데이터 보충 뒤 C의 P/TBV가 계산되어 비교 은행이 한 곳 늘어난 것이 차이의 원인이었다(판정은 네 장 모두 그대로).
- `peer_universe/banks.json`은 마지막으로 돌린 은행의 기준일로 덮어써진다. GS·MS·WFC 일봉은 9/29에서 끝나 그 뒤에는 기준일이 9/29가 되므로, 여러 장을 돌리면 9/30 기준 은행(BAC·COF 등)을 마지막에 돌린다.
- C는 `ixbrl_supplement.py`를 먼저 돌린다(스크립트에 포함). GS·MS·COF의 `rebuild.sh`는 SCHW 것을 그대로 옮겨 만들었다 — MS 우선주 오버레이(`adapters/ms_preferred.py`) 등 앞 단계가 필요하면 그 종목 `{t}_fill.py` 머리 설명을 먼저 본다.
- 손입력 값(분기 순수익·순이익, 자본비율, 뉴스·애널리스트)은 스크립트 안에 있다. 다음 분기 갱신 때 보도자료로 고친다.
