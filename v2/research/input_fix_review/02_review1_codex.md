**판정: 고정 전에 필수 수정이 필요합니다.** 특히 F3(b)는 정상 가중평균을 오염시켜 PKG 오류를 유지하고, F4는 적용 위치에 따라 LIN을 고치지 못합니다. 파일 수정·금지 함수 실행·수익률 및 평가일 뒤 가격 열람은 하지 않았습니다. 아래 경로는 저장소 기준입니다.

1. **규칙이 목표 사례를 고치는가 — 필수 수정**

   **F1: 방향은 맞지만 적용 경로를 확정해야 합니다.** MMM의 149.398에 분사 계수를 곱하고 EPS에서 같은 계수를 제거하면 시가총액은 바로잡히고 PER은 유지됩니다. 다만 정확한 표현은 **“분사 조정만 제거하고 진짜 분할은 현재 기준으로 유지”**입니다. 모든 가격이 당시 실제 종가가 되는 것은 아닙니다.

   카드 자기 이력은 HTML의 `DAILY` 종가를 직접 사용하며, EPS는 별도 파일에서 읽습니다([가격 로더](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:1355), [EPS 로더](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:1426), [배수 계산](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:1661)). 연구의 `pit.eps_ttm`만 고쳐서는 카드까지 맞춰지지 않습니다. 동종업도 저장된 유니버스 또는 `valuation_base`를 현재 종가로 환산하는 별도 경로입니다([build_peer_score.py:168](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_peer_score.py:168), [233행](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_peer_score.py:233)). **원래 가격과 가치 비교용 가격을 분리하고, EPS 파일·비교군 재생성까지 지정**해야 합니다. `KNOWN_SPLITS`가 있으면 Yahoo 목록을 건너뛰므로 무시된 사건 수집 경로도 필요합니다([splits.py:52](/Users/watermountain/Workspace/stock-widgets-preview/v2/splits.py:52)). GE·T·DHR·IBM은 카드 이력 시작일이 분사 이후로 제한되어 있어 “영향 예상”도 재확인이 필요합니다.

   **F2(a): 기간별 병합은 타당하지만 공시 시점 처리가 불완전합니다.** NVDA처럼 태그를 옮긴 회사는 모든 태그를 이어 붙이되, **같은 `(start,end)` 안에서만** 우선순위를 적용해야 합니다. 태그 목록 순서만 바꾸면 후속 `dedup_earliest_filed`가 다시 먼저 공시된 값을 선택합니다([build_multiple_history.py:562](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:562), [fetch_eps_history.py:87](/Users/watermountain/Workspace/stock-widgets-preview/scripts/fetch_eps_history.py:87)). 높은 순위의 태그가 나중에 공개되면 그 공개일부터 교체하고, 이전 일별 이력에는 기존 값을 유지해야 합니다. 평가일 단위 필터만으로는 자기 이력의 모든 날짜까지 보장하지 못합니다.

   PM 로컬 원자료에서 2017Q2 총액 **$19.319B는 2017-07-27**, 순액 **$6.917B는 2018-07-26** 최초 공시입니다. 따라서 “PM 2018 TTM ≈ $29.6B”는 평가일·결산일을 특정해야 하며, 순액을 2017년부터 소급 적용하면 안 됩니다. MA는 계약매출이 **순매출보다 큰 총액**인 반례입니다. 기존 제외 유지가 맞으며, 태그 이름만으로 총액·부분액을 일반화하면 안 됩니다([build_multiple_history.py:533](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:533)).

   **GD 원인은 확인했습니다.** 계약매출 태그의 잘못된 2017년 9개월 **$28.923B**, 연간 **$21.845B**를 차감해 Q4 **−$7.078B**, TTM **$15.618B**가 생성됩니다. 같은 기간 `Revenues`를 우선하는 메모리 계산에서는 FY2017 **$30.973B**, FY2018 **$36.193B**로 복구됐습니다. “분기말 날짜 차이·원인 미확인”을 이 근거로 교체할 수 있습니다([누계 차감 코드](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:633); 원자료 `v2/research/.facts_20261002/0000040533_facts.json`).

   **F2(b): 기존 안전조건을 보존해야 합니다.** 현재 코드는 정상적인 “Q4에만 발생한 항목”을 보호하려고 양수 9개월 누계를 요구합니다. 초안의 단순 2% 조건은 이를 제거합니다. 매출에 한정하고, 앞선 분기·누계가 실제로 존재하며 모순됨을 확인한 뒤 제외해야 합니다([build_multiple_history.py:614](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:614)).

2. **목표 밖 회귀 및 F3·F4 위험 — 필수 수정**

   **F3(b)는 PKG를 고치지 못합니다.** 2023-05-03 공시의 표지 **89,932,185,000주**, 희석 가중평균 **89,400,000주**의 비율은 약 **1,006배**입니다. 초안대로면 정상 가중평균에 ×1,000을 적용하고, 이후 0.5~2배 대조도 통과합니다. 현재 DCF가 정상 가중평균으로 피하던 오류까지 전파합니다([build_dcf.py:314](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_dcf.py:314); 원자료 `0000075677_facts.json`). **비율만으로 어느 쪽이 틀렸는지 결정하지 말고**, 인접 공시·연간 주식 수 등 독립 근거로 단위를 판별해야 합니다. 표지가 없을 때 무조건 ×1e6하는 기존 규칙도 천 단위 오류를 남깁니다.

   F3(c)는 **연간 EPS와 유도 Q4까지** 검사해야 합니다. `pit.eps_ttm`은 연간 EPS에서 세 분기를 빼 Q4를 만듭니다. 분기만 교정하면 잘못된 연간 값이 다시 들어옵니다. 대체 분자는 보통주 귀속·희석 EPS와 일치하는 이익이어야 하고, 분모 단위·분할 기준·공개일도 일치해야 합니다. 결측 분기가 생기면 비연속 네 분기를 합치지 않는 검사도 필요합니다([pit.py:77](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/pit.py:77)).

   **F4의 0.5배는 탐지 기준이지 합산 근거가 아닙니다.** LIN은 회사별 태그 분기에서 조기 반환하므로 공통 폴백 부분만 수정하면 그대로 **$3.179B**입니다([build_multiple_history.py:1193](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:1193)). 모든 차입금 경로에 적용하되, `LongTermDebt`의 유동분 포함 여부와 단기 태그의 중복을 먼저 확정해야 합니다. 비유동분만 뜻하면 단기 차입 외 **유동성 장기차입금이 빠질 수 있고**, 포함 총계에 유동분을 다시 더하면 중복됩니다. 기존 코드도 TSLA를 별도 구분합니다([1225행](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:1225)). 총계 대체 뒤 리스 포함 장기태그를 다시 더하지 않는 처리와 구성요소의 최대 공개일도 필수입니다.

   **F2의 카드 영향은 PM·ORCL로 제한되지 않습니다.** 전역 순위 변경은 103장 전체의 매출·성장률·DCF에 영향을 줄 수 있고, 비교군 수정은 입력이 정상인 카드의 동종업 점수도 바꿉니다. “목표 밖 불변” 대신 **직접 입력 교정 / 비교군을 통한 변화 / 설명되지 않는 변화**를 구분해야 합니다. 이번 검토에서 103장 전체 영향량은 확인하지 않았습니다.

3. **확인 기준·순서·절차 — 필수 수정, 기본 방향은 정상**

   수정별 커밋·회귀·패널 차이·재봉인과 12-01 전 학습 분석 금지는 적절합니다. 다음을 보강해야 합니다.

   - **기준선 두 개:** 저장된 옛 학습 패널과의 차이, 수정 직전 동일 코드·동일 입력으로 생성한 기준선과의 차이를 분리하십시오. 그래야 기존 엔진 변경과 F1~F4 효과가 섞이지 않습니다.
   - **검증은 입력부터:** 가격·주식 수·EPS의 기준 일치, 선택 태그·기간·공개일, 분기/연간 매출 연결, 차입금 구성 합계를 먼저 통과시켜야 합니다. “같은 자릿수”와 차입금 ±10%만으로는 부족합니다. **틀린 표지 값 자체를 정답으로 삼아서도 안 됩니다.**
   - **읽기 전용 회귀 진입점 명시:** 카드 자기 이력 생성은 현재 `main()` 안에 있습니다. `compute()` 계열이라는 표현만으로는 충분하지 않습니다. 캐시 갱신·네트워크·파일 저장이 없는 호출 경로를 정하고 비교군 산출물까지 검증해야 합니다.
   - **각 수정의 패널 차이와 최종 재생성을 구분:** 원본은 보존하고 단계별 해시·차이를 남긴 뒤, 최종 검증된 코드·입력·설정·파생 파일로 학습/시험 양쪽을 봉인하십시오. 검증 완료는 preview 반영보다 앞에 두는 편이 맞습니다.
   - **금지는 실행 방식과 무관하게:** `analyze_set`뿐 아니라 다른 스크립트·수동 계산을 통한 수익률 기반 선택 재실행도 금지한다고 명시하십시오. 입력·판정 차이 관찰은 허용하되 판정 이동을 최적화 목표로 삼지 않아야 합니다.

4. **“하지 않는 것”·“한계”의 정직성 — 필수 수정 / 권고**

   **“시험 구간 수익률은 아직 아무도 보지 않았다”는 과도합니다.** 기존 관문 문서는 TSLA·META·NVDA의 시험 구간 사례를 결과를 알고 엔진 설계에 사용했다고 명시합니다. **“봉인된 시험 패널에 수익률을 붙여 분석하지 않았다”**로 좁히고 기존 노출 이력을 유지하십시오([five_year_gate_prereg.md:107](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/five_year_gate_prereg.md:107), [124행](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/five_year_gate_prereg.md:124)).

   **S1 유지와 PER 제외 민감도는 정상**입니다. 다만 7/358은 특정 월의 관찰이고, PER 전체 제외는 TCJA만 제거한 실험이 아닙니다. 이를 명시해야 합니다.

   한계에는 **사건 비율만으로 분사·진짜 분할을 분류하는 오류**, EPS 대체의 근사성, 0.5배 이상 차입금 누락, 미해결 이력 커버리지를 추가하는 것을 권합니다. “목표를 못 맞추면 한계로 적는다”는 허용하되, **목표 밖 새 오류가 발견되면 배포를 멈춘다**는 조건과 구분해야 합니다.