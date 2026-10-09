1. **1차 지적은 대부분 반영됐지만, 두 조건이 빠졌습니다.**
   - **필수 수정 ① F2(b):** “9개월 누계가 있을 때”를 **“9개월 누계가 양수일 때”**로 명확히 해야 합니다. 현재 `_bad_q`는 `r["val"] > 0`을 요구합니다. “기존 안전 조건 유지”라는 괄호와 본문이 일치하지 않습니다. 원자료 대조에서 당장 해당 반례는 발견되지 않았지만, 기존 보호 조건을 약화시키는 문구입니다. [코드 근거](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:620)
   - **필수 수정 ② F3(c):** 1차에서 요구한 **연간 EPS·유도 Q4 검사와 대체값 구성요소의 최대 공시일 적용**이 명시되지 않았습니다. HAL의 ‘연간 EPS 없음’ 대안은 반영됐지만, 연간 EPS가 있는 경로는 여전히 연간값에서 세 분기를 빼므로 검사 범위를 적어야 합니다. 원자료에서 2016년 이후 연간 EPS 절댓값 1,000 초과 사례는 발견되지 않았습니다. [유도·가용일 코드](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/pit.py:77)

2. **새 규칙의 코드·원자료 대조 결과입니다.**
   - **F2(a): 적합합니다.** GD FY2017은 같은 공시의 총매출 **30.973B > 계약매출 21.845B**여서 교정 대상이고, BLK FY2023 **11.012B < 17.859B**는 교체되지 않습니다. 지정된 나머지 11종목에도 조건을 만족하는 충돌이 확인됐습니다. 같은 값의 공시 순서 보존도 반영됐습니다. [GD 원자료](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/.facts_20261002/0000040533_facts.json)
   - **F3(b): 확인한 사례에 적합합니다.** 표지와 대조하면 TER·DLR·CCL·UDR·COP는 ×1,000, MCD·KO는 ×1,000,000, NVR·TPL은 ×1입니다. PKG는 WA **89.4M**을 유지하여 잘못된 표지 **89.932B**를 대조에서 탈락시킵니다. [PKG 원자료](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/.facts_20261002/0000075677_facts.json)
   - **필수 수정 ③ F3(d): 400일 상한만으로 비연속 네 분기를 막지는 못합니다.** WAT 원자료의 `2017Q2 → 2017Q3 → 시작일만 다른 2017Q3 → 2018Q1`은 **363일**이라 통과합니다. 현재 코드는 `(start,end)`별로 보존하므로 그대로 재현됩니다. **중복 분기와 이웃 분기의 연속성 검사**를 명시해야 합니다. 이는 새로 생긴 오류가 아니라, 1차의 비연속 합산 방지 요구가 남은 경우입니다. [WAT 원자료](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/.facts_20261002/0001000697_facts.json), [합산 코드](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/pit.py:69)
   - **F4·dq: 반영 방향이 맞습니다.** LIN은 총계 태그가 없는 해당 종료일에 **12.159B + 3.179B = 15.338B**로 복구됩니다. 총계 우선·손 목록 경로 포함·금융/CAT/DE/BX/VRTX 제외·중복 방지 조건도 반영됐습니다. dq 필터는 기존 두 접두어만 유지한다는 결정과 일치합니다. 다만 기존 dq 발생 여부가 달라지면 통과 행은 달라질 수 있습니다. [LIN 원자료](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/.facts_20261002/0001707925_facts.json), [필터](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/verdict_replay.py:792)

3. **필수 수정 3개.**

파일 수정·금지 함수 실행·금지 자료 열람 없이 확인했습니다.