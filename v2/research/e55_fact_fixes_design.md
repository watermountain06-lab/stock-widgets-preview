# E55 설계안 r2 — 잘못된 개별 사실·기간 정보 보정 장치 (`v2/fact_fixes.json`)

## r1 → r2 바뀐 것
- (Fable 2 — Claude 데이터 확인으로 확정) **LHX는 기간 정보(context) 전체가 잘못 달렸다.** 같은 10-K(0000202058-26-000015)·같은 기간(2025-10-04~2026-01-02, frame CY2025Q4)에 매출 $21,865M뿐 아니라 매출원가 $16,240M·영업이익 $2,110M·세전이익 $1,932M·순이자 −$597M·기타 영업외 $419M이 있고 모두 FY2025 연간 값이다. 매출만 고치면 영업이익·세전이익(EV/EBITDA·출발 이익률·세율)이 틀린 채 남는다 → **기간 정보 단위 보정**(그 공시·그 기간의 모든 태그)을 둔다. NTAP의 같은 기간(2021-10-31~2022-01-28)에는 순이익 $252M·배당 $0.50 등 8행이 더 있는데 실제 3분기 값과 같고, 틀린 것은 매출 $796M 하나 → **사실 단위 빼기**.
- (Codex 1, Fable 1) 일치 검사는 `concept()`에서 하지 않는다. concept는 조용히 적용만 하고, 일치 검사는 전체 캐시 기준 `validate_fixes(cik)`가 CIK마다 한 번(시험·회귀·스캔·카드 빌드 시작) — 연구 경로에서 아직 공시 전이라 행이 없는 것은 정상.
- (Fable 5·8) 고침마다 **적용 뒤 기대 상태**(`expect`)를 적고 validate_fixes가 엔진 결과로 단언한다(손 계산의 코드화).
- (Codex 3, Fable 3) set_start 복사본에서 `frame`을 지운다. `new_start − 1일`이 같은 태그의 직전 연간 행 `end`와 같은지 검사(LHX 2025-01-03).
- (Fable 4) 같은 값의 중복 일치는 전부 적용 + 경고(엄격 모드에서만 오류).
- (Fable 6) 고친 뒤 기간 검사를 엔진 상수와 맞춘다(분기 80~100, LONG_Q4·53주 105~120, 16주 112 허용, 연간 350~380).
- (Fable 11) 행 dict는 얕게 공유되므로(pit.filtered) 고칠 행만 새 dict로 만든다 — 연구 data 객체 불변도 시험.
- (Codex 4, Fable 8) 회귀 검사: 분기 시리즈 전후 차이의 **키 집합**을 단언하고, 대상 카드 안의 변화도 보정 경로에서 파생된 것인지 원인 표로.
- (Codex 2, Fable 10) 손 계산에 종료일을 붙인다(아래 6절).
- (Fable 7) 스캔 휴리스틱 보강. (Fable 9) 기초점수는 아래 결정 ②.

## 문제(원자료 확인)
| 종목 | 무엇이 틀렸나 | 엔진이 지금 쓰는 값 | 바른 값 |
|---|---|---|---|
| NTAP | 매출 사실 하나: start 2021-10-31, end 2022-01-28, $796M, accn 0000950170-22-002669(10-Q Q3 FY22, filed 2022-03-02, frame 없음) | 2022-01-28 분기 매출 $796M | 같은 10-Q의 start 2021-10-30 행 $1,614M(frame CY2021Q4) |
| LHX | 기간 정보: accn 0000202058-26-000015(10-K FY2025, filed 2026-02-12), start 2025-10-04, end 2026-01-02 — 6개 태그가 연간 값 | 2026-01-02 분기 매출 $21,865M·영업이익 $2,110M 등 | 연간(start 2025-01-04). 4분기는 엔진이 연간 − 9개월로 만든다(매출 21,865 − 16,217 = 5,648) |

## 1. 파일 형식
```json
{"_note": "...",
 "0001002047": [{
   "id": "NTAP-rev-FY22Q3-dup", "scope": "fact",
   "taxonomy": "us-gaap", "tag": "RevenueFromContractWithCustomerExcludingAssessedTax", "unit": "USD",
   "match": {"accn": "0000950170-22-002669", "start": "2021-10-31", "end": "2022-01-28", "val": 796000000},
   "action": "drop",
   "expect": [{"tag_list": "revenue", "quarter_end": "2022-01-28", "val": 1614000000}],
   "reason": "...", "source": "<10-Q 정확한 URL>"
 }],
 "0000202058": [{
   "id": "LHX-FY25-context", "scope": "context",
   "match": {"accn": "0000202058-26-000015", "start": "2025-10-04", "end": "2026-01-02"},
   "action": "set_start", "new_start": "2025-01-04",
   "expect_tags": ["RevenueFromContractWithCustomerExcludingAssessedTax", "CostOfGoodsAndServicesSold", "OperatingIncomeLoss",
                   "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
                   "InterestIncomeExpenseNonoperatingNet", "OtherNonoperatingIncomeExpense"],
   "expect": [{"tag_list": "revenue", "quarter_end": "2026-01-02", "val": 5648000000, "tol": 0.005},
              {"tag_list": "opinc", "quarter_end": "2026-01-02", "val": 393000000, "tol": 0.005}],
   "reason": "...", "source": "<10-K 정확한 URL>"
 }]}
```
- `scope="fact"`: 한 태그·한 단위의 한 행(accn·start·end·val 모두 일치). `scope="context"`: 그 accn·start·end를 가진 **모든 태그·단위**의 행. `expect_tags`와 실제로 걸린 태그 집합이 다르면 오류.
- `action`: `"drop"` | `"set_start"`(start만 바꾸고 frame 삭제, val·filed·accn·form 그대로).
- `id` 파일 안에서 유일. `source`는 정확한 공시 URL(`...` 금지 — 불러올 때 검사).

## 2. 적용
- `bmh.concept(cik, tag, taxonomy)`: 그 CIK·태그에 걸리는 고침을 적용한 **새 목록**을 돌려준다(고칠 행만 새 dict, 나머지는 원래 객체). 엔진 소비자(pick_tag → quarterly_flow·ttm_series·annual_points·instant_series, build_dcf, fill.py `q()`, 동종업 유니버스 bmh.main)와 연구(pit가 `_facts`를 바꿔 끼워도 concept를 거침)가 같은 값을 받는다.
- concept 안에서는 일치 여부를 따지지 않는다(아직 공시 전인 연구 시점에는 행이 없는 게 정상).
- `validate_fixes(cik)`: 전체 캐시(시점 절단 없음)로 (a) 일치 수(0개 → 경고 / 엄격 모드 오류, 같은 값 중복 → 경고) (b) context 범위의 태그 집합 = expect_tags (c) 고친 뒤 기간 길이(분기 80~100·105~120(LONG_Q4·53주)·112(16주)·연간 350~380) (d) set_start면 `new_start − 1일`이 같은 태그 직전 연간 행의 end (e) `expect`를 pick_tag → quarterly_flow 결과로 단언. 카드 빌드 시작·engine_regress·시험·스캔에서 부른다.

## 3. 적용 안 되는 곳
- `scripts/fetch_eps_history.py`(EPS 이력): NTAP·LHX의 잘못된 기간에 EPS 사실은 없다(확인한 행 목록에 EPS 태그 없음). 범위 밖으로 두되, validate_fixes가 같은 accn·기간의 EPS 태그 행을 찾으면 경고.
- redesign `fetch_financials`(기초점수 입력): NTAP 영향 없음(연간 정상, 잘못된 행은 2022년 분기). **LHX는 영향 있음** — FY2025 연간 매출이 분기 기간이라 연간 목록에서 빠지고 최신 연간이 FY2024($21,325M)에 멈춤. → 결정 ②.

## 4. 연구 경로
- 학습 패널·5년 관문 패널의 NTAP·LHX 행과, 둘을 동종업으로 쓰는 행의 동종업 칸이 바뀐다. 결정 ①. `verdict_replay._override_filed`·`provenance`, `engine_regress.py` ENGINE_GLOBS에 fact_fixes.json 추가.

## 5. 찾아내기 (`v2/research/scan_bad_facts.py`, 읽기 전용, 고침 적용 **전** 자료로)
- (a) 같은 accn·같은 end에 start가 0~3일 다른 흐름 행이 둘 이상이고 **값이 다른** 경우(0일 차 = 같은 start·end에 다른 값 포함).
- (b) 80~100일 행이 같은 태그 직전 1·2·3분기 합의 ±2%(누계를 분기로 태그) 또는 10-K 행이 분기 기간인데 앞 세 분기 합보다 큼(LHX형) — 이 경우 같은 accn·기간의 다른 태그도 함께 나열.
- (c) 엔진 분기 값이 앞뒤 분기 중앙값의 0.4~0.6배·1.7~2.3배·3.5~4.5배 구간(따로 표시). (a)·(b) 적중을 위로 정렬, (c)는 참고(2020 코로나·인수 급증 거짓 양성).
- 자동으로 고치지 않는다.

## 6. 검증
1. 새 시험 `v2/research/test_fact_fixes.py`: 가짜 companyfacts로 fact drop·context set_start, 일치 0개(경고/엄격 오류), 같은 값 중복(경고), accn 불일치(무적용), expect_tags 불일치 오류, 기간 검사(16주·17주 4분기 통과, 반기 길이 거부), new_start 경계 검사, frame 삭제, 캐시 원본·연구 data 객체 불변, **통합**: pick_tag → quarterly_flow를 거쳐 drop 뒤 q[2022-01-28] = 바른 값, set_start 뒤 연간 − 9개월로 4분기가 만들어지는지.
2. 변이: 일치 조건에서 accn 빼기, 원본 dict 수정, context 대신 fact만 고치기, frame 남기기 — 각각 1번이 빨개지는지.
3. 기존 카드: freeze → 빈 `{}` 전 카드 diff 0 → 고침 입력 뒤 전 카드 diff. 분기 시리즈 차이의 키 집합이 정확히 {NTAP 매출 2022-01-28}, {LHX 6개 태그의 2026-01-02 분기 + FY2025 연간 추가}인지 단언. 대상 카드 안의 다른 변화는 원인(보정 파생 / 동종업 전파)을 표로, 설명 안 되는 차이는 실패. 영향 밖 대표 카드 compare_render 동일.
4. 손 계산(종료일 명시): NTAP 2022-01-28 분기 매출 1,614, 2022-01-28 종료 TTM = Q4 FY21(2021-04-30) 1,555 + Q1 FY22(2021-07-30) 1,458 + Q2(2021-10-29) 1,566 + Q3(2022-01-28) 1,614 = 6,193(지금 엔진 5,375); LHX 2026-01-02 종료 TTM 매출 = 연간 21,865와 같아야 함, 2026-07-03 종료 TTM = Q3'25 5,659 + Q4'25 5,648 + Q1'26 5,744 + Q2'26 5,881 = 22,932. 영업이익 4분기 = 2,110 − 9개월 1,717 = 393.
5. 대상 초안 전후 비교표(NTAP·LHX: 점수·판정·내재가치·PSR·EV/EBITDA·출발 이익률·세율).
6. scan_bad_facts.py를 카드·S&P500 전체에 돌려 후보 목록 보고.

## 결정할 것
① 연구 경로: 지금 넣고 패널 재생성·재봉인(E57과 묶어 한 번). 권장: 넣는다.
② 기초점수(fetch_financials, redesign 저장소): LHX만 영향. LHX는 E55 뒤에도 자회사 우선주·워런트 규칙 때문에 보류다 → 권장: 지금은 엔진만, fetch_financials 보정은 LHX 보류 해제 때(그때까지 LHX 카드는 만들지 않음).

## 구현 기록 (2026-10-24, 사용자 승인 뒤)
- 리뷰: Codex(astra·medium)·Fable 2라운드 합의(필수 0건). 권장 반영: 검사는 카드가 보는 `_facts`(overlay 포함·승인일 절단) 한 경로로 일치 수·기대값을 함께 본다, context 범위는 (분류·태그·단위·값) 집합으로 고정, 기대값은 정확값, FACT_FIXES=off 스위치, 엄격 모드(FACT_FIXES_STRICT=1)는 시험·회귀에서만, 동종업 빌드(bmh.main)에서도 검사.
- 코드: `build_multiple_history.py` `concept()` → `_apply_fact_fixes`(사본), `_fact_fixes`(불러오기 검사), `validate_fixes`(main 시작), `fact_fixes.json`, `research/test_fact_fixes.py`(시험 21개·변이 5개 — accn 조건 변이는 처음에 못 잡아 다음 해 10-K 비교 열 행을 시험 자료에 더함), `research/scan_bad_facts.py`, `engine_regress.py` ENGINE_GLOBS·`verdict_replay.provenance`에 등록.
- 스캔으로 추가 발견: 같은 LHX FY2025 10-K가 FY2024 비교 열(2024-09-28~2025-01-03, 매출 $21,325M 등 6개 태그)도 4분기 기간으로 달았다. 원래 FY2024 10-K의 바른 연간 행이 먼저 공시돼 엔진 값은 이미 맞다(4분기 매출 5,523) — 같은 오류라 `LHX-FY24-comparative-context`로 함께 고침(결과 불변).
- 기초점수 입력(fetch_financials)의 LHX FY2025 연간 매출 누락은 결정 ②대로 LHX 보류 해제 때 고친다.
