# 은행 카드 채우기 스크립트 (v2/newcards/bank)

은행 세트(사전 등록 `v2/research/bank_rim_prereg.md`) 카드는 `newcards/fill.py`가 아니라 종목별 채우기 스크립트로 만든다. 세션 임시 폴더에 있던 것을 2026-10-02 저장소로 옮겼다(JPM 스크립트는 남아 있지 않아 없음).

| 파일 | 하는 일 |
|---|---|
| `{t}_rebuild.sh` | 한 번에 다시 만들기 — `bank_card.py`(관문·RIM·자기 이력·동종업 → `v2/{T}_bank.json`) → 기반 HTML 복사 → `{t}_fill.py` → `sync_fallbacks.py` → JS 문법 검사 |
| `{t}_fill.py` | 기반 HTML(복제 + 배열)에 은행 데이터·문장을 채운다. 틀 문자열이 정확히 한 번씩 있는지 확인하며 바꾸므로 기반이 바뀌면 멈춘다 |
| `base/{t}_base.html` | 채우기 직전 카드(복제 + 배열). 루트 카드가 있는 은행은 `clone_card.py` + `{t}_arrays.py`, COF는 `build.py COF --data`로 만든 것 |
| `{t}_arrays.py` | 루트 카드 일봉·배열을 v2 카드로 옮긴다(루트 카드 있는 은행만) |

다시 만들기: `bash v2/newcards/bank/{t}_rebuild.sh`(저장소 루트 기준 경로). 일봉을 새로 받으면 기반 HTML부터 다시 만든다 — COF는 `python3 v2/newcards/build.py COF --data` 뒤 `cp v2/COF_full_widget.html v2/newcards/bank/base/cof_base.html`.

주의
- 채우기 스크립트는 `v2/{T}_bank.json`과 `v2/peer_universe/banks.json`이 같은 때 만든 것이라고 가정한다(동종업 수 확인). `bank_card.py`를 건너뛰고 채우기만 돌리면 비교군 파일이 그 뒤 갱신된 은행(BAC·GS·WFC)은 확인에서 멈추고, MS는 비교 차트 값이 바뀐다(2026-10-02 확인). 반드시 `rebuild.sh`로 돌린다.
- C는 `ixbrl_supplement.py`를 먼저 돌린다(스크립트에 포함). GS·MS·COF의 `rebuild.sh`는 SCHW 것을 그대로 옮겨 만들었다 — MS 우선주 오버레이(`adapters/ms_preferred.py`) 등 앞 단계가 필요하면 그 종목 `{t}_fill.py` 머리 설명을 먼저 본다.
- 손입력 값(분기 순수익·순이익, 자본비율, 뉴스·애널리스트)은 스크립트 안에 있다. 다음 분기 갱신 때 보도자료로 고친다.
