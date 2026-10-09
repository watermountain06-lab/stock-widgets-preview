**판정은 ‘문제’입니다.** 리츠 외에도 PKG·HAL·FOX의 배수 입력 오류, LIN의 과거 장기부채 누락, CCL의 주식수 보정 오류를 확인했습니다. 파일 수정 없이 계산했으며, 가격 파일·수익률·결과 JSON은 열지 않았습니다.

아래 월별 값의 출처는 [시험 패널](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/gate_test_panel.json:1)과 [학습 패널](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/verdict_replay_panel.json:1)입니다. 단일행 JSON이므로 종목·월을 함께 적었습니다.

1. **월별 비율·칸별 분포 — 정상인 계산, 비교 해석은 판단 보류.**  
   학습 2024-10→11에 `dcf_ok`로 바뀌는 **108종목 모두** 고정 창의 유효 이력이 **12→13개**가 됩니다. 218/394→326/394, 즉 55.3%→82.7%의 차이를 전부 설명합니다. 오류보다는 최소 13개 조건의 시작 경계 효과입니다([`history()`](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_dcf.py:598)). 시험은 롤링 창이라 같은 결측 집중이 없습니다. 따라서 학습 전체 평균과의 단순 비교에는 영향을 주며, **학습 2024-10 제외 수치도 보조 보고**하는 것이 좋습니다.  
   자기 이력 중앙값 48.9→44.1, D 중앙값 −0.78→−0.94는 시기·구성종목·DCF 창이 모두 달라 원인을 시장 국면 하나로 돌릴 수 없습니다. 동종업 중앙값 50.7→50.9가 비슷한 것도 순위 구조상 자연스럽습니다. 아래 입력 오류를 처리하기 전에는 분포 차이를 경제적 신호로 확정하지 못합니다.

2. **배수 이상값 — 정상과 문제가 섞여 있음.**

   | 대상 | 확인 결과 |
   |---|---|
   | PODD·SJM PER | **정상 산술.** 각각 2023-06·2024-01의 TTM EPS가 **$0.01**이라 28,834·13,155배. 거의 0인 분모입니다. EPS가 작아진 일회성 항목의 전체 연결은 **확인 못 함**. |
   | CLX·FTNT PBR | **정상 산술.** 2023-03말 자본이 각각 **$3M·$11.4M**. CLX는 당분기 손상차손 $445M도 확인됩니다. [CLX 공시](https://www.sec.gov/Archives/edgar/data/21076/000002107623000015/clx-20230331.htm), [FTNT 공시](https://www.sec.gov/Archives/edgar/data/1262039/000126203923000021/ftnt-20230331.htm). |
   | APD PCR | **정상 산술.** 2023-04 기준 OCF $3,104.7M−설비투자 $3,096.9M＝**FCF $7.8M**, 따라서 8,381배. |
   | PKG PCR·EV/EBITDA | **문제.** 2023-07 배수에 **89,932,185,000주**가 들어갑니다. 분모 FCF $726.7M·EBITDA $1,791.6M는 작지 않습니다. 주식수 1,000배 오류이며, DCF만 별도로 보정합니다. [해당 공시](https://www.sec.gov/Archives/edgar/data/75677/000095017023016955/pkg-20230331.htm). |
   | CPT PSR | **문제.** 2023-08 분모 매출 $2.844M는 임대료를 제외한 계약매출입니다. DCF 결측이어도 PSR과 비교군은 오염됩니다. |
   | HAL·FOX의 0.0 | **문제.** HAL 2024-02 PER은 실제로 0.00001257: EPS TTM **2,790,000**을 사용합니다. 원문 분기 EPS $0.79가 로컬 태그에는 790,000으로 있습니다. FOX는 2019-03의 **1주**를 계속 사용합니다. [HAL 공시](https://www.sec.gov/Archives/edgar/data/45012/000004501223000056/hal-20230930.htm). |

   **순위도 실제로 바뀝니다.** 같은 월 비교군을 유지한 단일 입력 교정 계산에서 PKG 2023-07 PCR은 18,977.7→18.98배, 해당 배수 동종업 점수는 **22.7→72.7**입니다. HAL PER을 100만 배 바로잡으면 **100→42.1점**입니다. 정상적인 큰 배수는 크기 자체가 평균을 폭발시키지는 않지만, 잘못된 값은 순서 자체를 바꿉니다([순위 산식](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/verdict_replay.py:455)). PKG 자기 이력은 당시 PER 외 네 배수가 모두 0.1점입니다. **교정 후 일별 자기 이력 점수 전체는 확인 못 함**입니다. 학습에도 PKG PCR 28,424배(2026-02), HAL 극소 PER, FOX·FOXA 극소 배수가 남습니다.

3. **공시 특이점 — 문제·판단 보류.**  
   **TCJA는 남습니다.** MSFT FY2018 EPS $2.13, 보정액 0을 확인했습니다. 회사가 밝힌 TCJA 영향은 EPS −$1.75이며, 이 EPS 구간은 시험 초기의 5년 자기 이력 창에 포함됩니다. 학습 2024-10의 창에서는 2018년이 빠집니다. 따라서 두 구간의 자기 이력 비교에 비대칭이 있습니다([EPS 구성](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/pit.py:53), [MSFT 연차보고서](https://www.microsoft.com/investor/reports/ar18/index.html)). 정확한 점수 영향은 **확인 못 함**입니다.  
   **ASC 606:** 리츠 외에도 MA·GE처럼 태그 의미가 다른 사례가 있고 현재 코드에 회사별 제외가 있습니다. 이를 모두 2018년 전환 때문이라고 확정하거나 추가 종목을 전수 공시 대조하지는 못했습니다([태그 예외](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:533)).  
   **ASC 842:** WMT 운용리스 입력은 2019-03 평가에서 0, 06 평가에서 **$17.467B**로 증가하며 공시와 부합합니다. EV 이력에 회계기준 단절이 생깁니다. 두 시점 `debt_suspect`는 없으며, 이 플래그는 리스가 아니라 이자/차입금 조건입니다. 전 종목의 2019 전후 EV/EBITDA·플래그 변화는 **확인 못 함**입니다([조건](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_dcf.py:344), [WMT 공시](https://stock.walmart.com/sec-filings/all-sec-filings/content/0000104169-19-000024/0000104169-19-000024.pdf)).  
   **분할·분사:** 월간 가격 급변 0건만으로 정합성을 입증할 수 없습니다. 시험 DCF 결측은 GE 30개월, IBM 28개월, T 13개월, DHR 15개월입니다. 특히 GE는 전부 `history,opinc` 결측으로, 분사 창만의 문제가 아닙니다([분사 설정](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_dcf.py:62)).

4. **리츠 처리 권고 — 문제: 회사별 엔진 수정이 우선.**  
   보고용이어도 잘못된 총매출이 카드·PSR·비교군에 공유되므로 **확인된 회사·기간에 한정해 총매출 정의를 고치는 방안**을 권합니다. `pick_tag`의 전역 우선순위 변경은 피해야 합니다. WELL은 이미 계약매출 제외 예외가 있어, 안 걸렸다는 사실을 리츠 전체의 정상 근거로 쓰면 안 됩니다. PLD·WELL은 수정 전후 불변 여부를 확인할 대조 사례입니다([공유 태그 처리](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:562)).  
   수정 전후 입력·판정 차이와 학습 영향도 남기고 재봉인하되, **12-01 선택 재실행은 요구되지 않습니다**([최신 변경 기록](/Users/watermountain/Workspace/stock-widgets-preview/v2/research/five_year_gate_prereg.md:130)). 당장 수정하지 않는다면 원본과 해당 행 제외 민감도를 병기할 수 있지만, 평가 행만 빼면 비교군 오염이 남는다는 한계를 명시해야 합니다.

5. **시험 전부 결측 7종목 — 문제: 주로 추출된 공시 이력의 부족.**  
   2024-03 시점 엔진이 만들 수 있는 영업이익 TTM 수는 **BMY 9, HON 0, JNJ 11, KLAC 11, NEM 9, ROL 9개**입니다. 13개 미만이므로 결측 처리는 규칙대로입니다. HON은 분기 자료가 있어도 연말 공백 때문에 유효 TTM이 만들어지지 않습니다. BMY·JNJ·KLAC·NEM은 합성 영업이익에 필요한 같은 공시의 태그 조합이 제한됩니다([합성 조건](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:509), [이력 조건](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_dcf.py:604)). VTRS는 13개에 도달한 마지막 두 달이 이미 알려진 오류입니다.  
   즉 **회사의 실적이 없다는 뜻이 아니라 현재 자료·태그 경로의 커버리지 부족**입니다. 옛 공시의 자체 태그를 보충하면 얼마나 복구되는지는 **확인 못 함**입니다.

6. **내재가치 급변 — 문제 사례와 정상 입력 변화가 혼재.**  
   **LIN은 문제:** 2023-01→02 $86.62→$28.21. 이전 입력 부채 $3.179B는 당시 공시 총부채 **$15.338B**보다 $12.159B 작습니다. 원자료에 `LongTermDebt`가 있지만 현재 회사별 태그 목록이 이를 놓칩니다. 정상적인 분기 변화만으로 설명하면 안 됩니다([엔진](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_multiple_history.py:1045), [2022Q3 공시](https://www.sec.gov/Archives/edgar/data/1707925/000162828022027183/lin-20220930.htm)). EXR은 알려진 매출 오류로 분류합니다.  
   **ATO·IR은 판단 보류:** 각각 $1.12→$11.21(2023-05), $0.357→$12.91(2023-02). 한계 매출/자본이 **0.545→10, 0.811→10**으로 바뀝니다. ATO의 규제자산 $2.02B 회수, IR의 연간 영업이익 $817.3M는 공시와 부합하지만, 가치 급변에는 재투자 모델의 민감도가 큽니다([산식](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_dcf.py:662), [ATO 공시](https://www.sec.gov/Archives/edgar/data/731802/000073180223000013/ato-20230331.htm), [IR 실적](https://investors.irco.com/news/news-details/2023/Ingersoll-Rand-Reports-Record-Fourth-Quarter-and-Full-Year-2022-Results/default.aspx)).  
   **INTC·XOM은 확인한 계산 경로상 정상:** INTC 2023-07의 기본 마진 중앙값 21.75%→15.52%, XOM 2023-02는 4.56%→11.86%로 바뀌며 저장 가치를 재현합니다. INTC의 0.0은 실제 **$0.0292**입니다. 52건 전부의 공시 대조는 **확인 못 함**입니다.

7. **추가로 보고 전에 처리할 문제 — CCL 보정 오류와 검증 범위 표시.**  
   CCL 2023-01의 −$88,914는 코로나 실적만의 결과가 아닙니다. 엔진이 표지 **1,113,479,515주를 희석 가중평균 1,185,000주로 교체**합니다. 같은 자료의 연간 희석 주식수는 1,180,000,000주로, 분기 태그의 천 배 단위 불일치가 강하게 드러납니다. 현재 `<100만 주` 보정 조건을 살짝 넘어서 검사를 통과합니다([보정 코드](/Users/watermountain/Workspace/stock-widgets-preview/v2/build_dcf.py:314)). 음수 가치의 V0 등급은 같아도 가치 금액은 잘못됩니다.  
   **PKG·HAL·FOX·LIN·CCL의 입력 오류를 우선 처리하고**, 남은 공시 대조·자기 이력 교정 영향은 미확인 범위로 남겨야 합니다. 현재 상태를 ‘수익률 없는 검증 완료’로 기록하기에는 이릅니다.