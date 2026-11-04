# 카드 제작 보조 도구

v2 새 카드를 만들 때 쓰는 손 도구다. 실행 절차의 기준은 `v2/newcards/README.md`이고, 여기 도구는 그 절차를 줄여 주는 보조다. 작업 로그·원문 캐시는 `CARD_WORK`(기본 `/tmp/card_work`)에 쓴다 — 저장소에는 쓰지 않는다.

예전에는 Claude 세션 임시 폴더(scratchpad)에 두었는데 임시 폴더 정리로 지워져(2026-11-03) 저장소로 옮겼다.

| 도구 | 쓰는 법 | 하는 일 |
|---|---|---|
| `prep.py` | `python3 v2/research/tools/prep.py T CIK "섹터" "이름" "#색1,#색2,#색3" "거래소 · 업종 — 설명" --register` | 공시 목록·companyfacts 핵심 태그 확인, `--register`면 fetch_eps_history CIKS·KNOWN_SPLITS(Yahoo 분할 — 분사 가격 조정이면 손으로 비울 것)·activity CIKS·sectors·sec_approved·meta·cfg 뼈대 등록 |
| `unreg.py` | `python3 v2/research/tools/unreg.py T CIK` | `prep.py --register` 되돌리기(카드 파일도 지움) |
| `finish.sh` | `ASOF=YYYY-MM-DD v2/research/tools/finish.sh T` | 데이터 단계·빌드·백테스트·대체값·글자 점검·preflight·글자 더미(`$CARD_WORK/{t}_text.txt`). Yahoo 가격은 다시 받지 않는다 |
| `link.py` | `python3 v2/research/tools/link.py PREV NEW` | 앞 카드의 "다음" 링크를 새 카드로, 새 카드의 "이전" 링크를 앞 카드로 |
| `logo.py` | `python3 v2/research/tools/logo.py T "검색어"` | 위키미디어에서 로고를 받아 `logos/{t}.png`(128px, 흰 배경) — 자회사·다른 회사 로고가 걸릴 수 있으니 눈으로 확인 |
| `badge.py` | `python3 v2/research/tools/badge.py T "#hex"` | 로고를 못 찾을 때 티커 글자 원형 배지 |

`finish.sh`는 `/opt/miniconda3/bin/python3`이 있으면 그것을 먼저 쓴다(셸에 따라 인증서 없는 다른 python3가 잡혀 SEC 요청이 실패했다, 2026-11-03).

생성 스크립트(gen_*.py)로 cfg를 다시 만들면 `fetch_analyst.py`가 넣은 애널리스트 줄이 자리표시(1명 Hold·$0)로 돌아간다. cfg를 다시 만들었으면 빌드 직전에 `python3 v2/newcards/fetch_analyst.py T`를 다시 돌리고, 등록 전에 `grep "'n': 1, 'nt': 1, 'mean': 0" v2/newcards/cfg/cfg_t.py`가 0인지 확인한다(2026-11-03 — 10장이 자리표시로 등록·푸시됐다).
