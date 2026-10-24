# E57 설계안 r4 — 청산 담보금 흐름을 영업현금흐름에서 빼는 장치

## r3 → r4 바뀐 것
- (Fable 1 — Claude가 원문으로 확인) **인수 전 기간 면제**: Q3 2020 10-Q의 9개월 2019 열(영업현금흐름 395.1, 담보금 태그 없음)과 FY2021 10-K의 FY2019 열(632.8, 태그 없음)처럼 era 공시의 인수 전 비교 열에는 담보금 값이 없다(흐름 자체가 없던 기간). → **기간 결산일 ≤ 2020-06-30인 행은 공시일과 상관없이 그대로**(cfg `era_period_end_after = "2020-06-30"`). 9개월 2020(−771.9)·FY2020(−812.1)처럼 인수 전후에 걸친 기간은 태그가 있어 정상 조정된다.
- (Codex 1, Fable 3) 최신성 문장 방향 정정: 영업현금흐름 TTM 결산일이 매출 TTM 결산일보다 **이르면**(최신 누계가 빠져 낡은 TTM) 계산 불가. 시험으로 고정.
- (Codex 2, Fable 2) 연속성: 본 기간 행이 빠져 분기가 비면 `ttm_series`가 창 길이 310일 초과로 그 TTM을 버린다(연속 4분기만) → 최신 TTM이 앞당겨지고 위 최신성 검사가 계산 불가로 둔다. 시험: FY2025 10-K 행만 제외하고 Q1 2026은 남긴 자료에서 PCR이 계산 불가인지.
- (Codex 3) confirmed_none 시험: 등록 accn의 짝 없는 행 통과, 같은 기간 다른 accn에는 전파 안 됨, 등록 accn에 짝이 있으면 조정. 등록은 그 공시의 모든 대상 기간을 확인한 뒤에만(문서에 적음).
- (Fable 4) 단언: CBOE companyfacts 영업현금흐름 행의 form은 era 안에서 10-K·10-Q뿐(정정 공시는 2013년뿐 — 확인).
- (Fable 5·6) net_ocf의 충돌 검사는 원본 companyfacts JSON을 직접 읽는다. era 공시 시험은 overlay 행의 `min(filed) == era_filed`·그 행 accn == era_accn.
- (Fable 7·8) 앞 라운드 문구 정리: era는 cfg 고정(overlay 유추 아님), 날짜 표식은 피드 갱신 트리거로만, 동종업 방향은 현재 TTM 부호로. 2분기 표기는 "영향 −934.8 → 뺀 값 = −503.2 − (−934.8) = 431.6".

## r2 → r3 바뀐 것
- (Codex 1·2, Fable 1·2) **시대 안 짝 없는 행은 하나의 규칙**: 담보금 시대(아래 era) 안의 영업현금흐름 행은 같은 (start, end, accn) 담보금 행이 있어야 한다. 없으면 — 그 accn이 원문으로 "조정 불필요"를 확인해 cfg `ocf_netting_confirmed_none`에 적은 공시가 아닌 한 — **그 행을 뺀다**(카드 빌드: 경고 + 실행 요약 표시, 시험·회귀: 오류). "훑었는데 태그 없음 → 그대로 통과" 갈래와 날짜 표식(`scanned_to`) 판정을 없앤다. 태그 변경·차원 전환·파싱 실패·정정 공시·.htm 아닌 공시 모두 같은 규칙으로 막힌다.
- (Fable 4 — Claude가 원문으로 확인) **era 시작을 cfg에 고정**: Q3 2020 10-Q(accn 0001558370-20-012101, filed 2020-10-30)가 그 태그가 처음 나오는 공시이고 Q2 2020(0001558370-20-008849)·Q1 2020 10-Q에는 없다(EuroCCP 인수 2020-07 뒤 첫 분기). era = `filed ≥ 2020-10-30`. overlay에서 era를 유추하지 않는다. 시험에 "overlay의 첫 담보금 행 공시 == 고정 era 공시"를 단언한다(overlay가 첫 공시를 빠뜨리면 빨개짐).
- (Codex 4, Fable 5 — 원문 값 확보) 9개월 2025(Q3 2025 10-Q accn 0001628280-25-047680): 보고 영업현금흐름 1,400.5, 담보금 원 값 −554.2 → 뺀 값 846.3. 4분기 2025 = 1,224.1 − 846.3 = 377.8. 9개월 2024 비교 열: 1,811.0, −1,163.4.
- (Fable 3, Codex 권장) 최신성: 영업현금흐름 TTM의 결산일이 매출 TTM 결산일보다 이르면(최신 누계 행이 빠짐) PCR·FCF는 계산 불가 + 경고. build.py는 companyfacts 최신 공시가 company_tags 표식보다 새로우면 피드를 먼저 돌린다(기존 `_ct_stale` 경로). 동종업 쪽도 같은 판정이라 CBOE가 빠지면 그 칸에서 빠진다(그날 diff 원인 표에 표시).
- (Codex 3, Fable 6) accn 충돌 검사는 **원본 companyfacts 영업현금흐름 행**에서, 합치기 전에, era 안 행만.
- (Codex 5) 동종업 방향 예측은 현재 TTM에만(현재 TTM 영향 부호로). 자기 이력은 기간마다 부호가 다르다(FY2022는 영업현금흐름 651.1 → 868.6으로 늘어 PCR 하락).
- (Fable 8·9·10) 비교 열 행 제외는 원 공시 행이 있으면 결과가 같고 없으면 사다리에 구멍(의도) — 문서에 적음. overlay는 누적 보존(재생성 금지 — recent 창이 밀리면 초기 공시를 못 받는다), 필요하면 `filings.files`도 읽도록 피드 확장은 별도. 빌린 이름이 overlay us-gaap 키 열거 경로에 잡히지 않는지 확인(구현 때). net_ocf는 `dict(r, val=...)` 사본.
- (Fable 7) 증거금 부채 앵커는 사실 확인용 상수이고, 시험에서는 부호 회귀 고정이다(표현 정정).

## r1 → r2 바뀐 것
- (Fable 2 — Claude가 원문으로 확인) CBOE Q1 2026 10-Q 영업활동의 담보금 관련 줄은 **"Restricted cash … (included in margin deposits, default fund, and interoperability fund) 1,878.0" 하나뿐**이고 부채 쪽 상쇄 줄은 없다(나머지 줄: 매출채권·법인세·기타 자산·매입채무·Section 31·이연수익 등). 재무상태표 부채 "Margin deposits, default fund, and interoperability fund"는 1,618.2 → 3,443.9(+1,825.7) — 현금흐름 영향 +1,878.0과 방향·크기가 맞아 부호 규칙의 독립 근거다. 시험에 이 두 앵커를 고정한다.
- (Fable 1, Codex 2) 짝 없는 행 판정을 자료로 계산할 수 있게 바꾼다(아래 1절). "담보금 시대"의 시작은 overlay에서 그 태그가 처음 나온 공시일(첫 행, Cboe의 EuroCCP 인수 2020년 뒤)로 정하고 그 전 공시의 영업현금흐름은 그대로 둔다.
- (Codex 1 → 권장으로 판정) `company_tag_feed`는 submissions `recent`만 훑는다 — CBOE는 recent 1,004건이 2015-05까지, 10-Q·10-K 45건이라 2019년 이후 공시는 모두 들어 있다(확인). 일반 안전장치로 "필요한 공시(영업현금흐름 행이 있는 담보금 시대 accn)가 overlay 훑은 범위에 모두 있는지" 검사를 넣는다.
- (Codex 3) 공급 단계 중복 키(같은 기간·같은 공시일)는 accn이 다른 두 공시를 하나로 합칠 수 있다. 공유 어댑터는 바꾸지 않고, 네팅 대상 CIK에서 companyfacts 영업현금흐름에 같은 (start, end, filed)·다른 accn 행이 있으면 오류로 둔다(CBOE는 0건 — 확인). 정정 공시(10-K/A·10-Q/A)는 2013-05-02 것뿐이라 담보금 시대 전이다(확인).
- (Fable 3) 중단영업 빼기 패턴(짝 없으면 원 값 통과)을 복사하지 않고 별도 함수 `net_ocf(cik, rows)`로 둔다.
- (Fable 4, Codex 5) CBOE를 동종업으로 쓰는 카드 목록을 먼저 뽑고, 동종업 쪽 CBOE 영업현금흐름 TTM == CBOE 자기 카드 값을 단언, 변화 방향 사전 예측(CBOE PCR 상승 → 그 동종업 PCR 분포 위쪽 이동). 전후 비교표에 분기 차트 값 추가.
- (Fable 5·6·7) 시험 보강: 9개월 누계·4분기 역산 실물 값, 같은 기간을 두 공시가 다른 담보금 값으로 보고하는 가짜 자료(accn 조건 변이용), 비교 열 "—"(태그 없음) 처리.
- (Fable 8·10·11) 공시 종류별 부호 문장 삭제(CBOE는 10-K·10-Q 같음), overlay 단위(USD 원 단위) 단언, CBOE 영업현금흐름 태그가 `NetCashProvidedByUsedInOperatingActivities` 하나인지 단언.
- (Codex 4) 최신 누계 행이 빠지면 그 지표(PCR·FCF)를 계산 불가로 두고 옛 값을 현재처럼 쓰지 않는다.
- (Codex·Fable) 문구: NDAQ·ICE·CME는 "자기 지표 직접 조정 없음; CBOE 동종업 경유 변화는 보고 대상".

## 사실(원문 16개 공시 + 엔진 확인, 2026-10-24)
| 회사 | 담보금 흐름이 있는 곳 | 태그 | 엔진 영향 |
|---|---|---|---|
| **CBOE** | **영업활동** "Restricted cash and cash equivalents and customer bank deposits (included in margin deposits, default fund, and interoperability fund)" | `cboe:IncreaseDecreaseInRestrictedCashClearingFund`(차원 없음, 2020~2026 같은 이름). 영업현금흐름 영향 = −(XBRL 값), 10-K·10-Q 모두 | 영업현금흐름(PCR·FCF)이 왜곡 |
| NDAQ | 투자·재무활동 | `ndaq:PaymentsForProceedsFromDefaultFundsAndMarginDeposits`·`ndaq:IncreaseDecreaseInDefaultFundContributionsAndMarginDeposits` | 없음 |
| ICE | 재무·투자활동 | `ice:IncreaseDecreaseMarginDepositsAndGuarantyFunds` 등 | 없음 |
| CME | 재무활동 | `cme:ChangeInPerformanceBondAndGuarantyFundContributions`(10-K·10-Q 부호가 반대) | 없음 |
- CBOE 값(누계, $M): Q1 2026 원 값 −1,878.0 → 영향 +1,878.0(보고 영업현금흐름 1,960.0, 뺀 값 82.0) / 6개월 −943.2 → +943.2(1,456.8 → 513.6) / FY2025 −528.5(1,752.6 → 1,224.1) / FY2022 +217.5(651.1 → 868.6) / FY2021 +66.2(596.8 → 663.0). 2분기 단독 = 943.2 − 1,878.0 = −934.8, 2분기 영업현금흐름(뺀 값) = (1,456.8 − 1,960.0) + 934.8 = +431.6.
- NDAQ·ICE·CME는 담보금을 현금 합계(제한 현금)에 넣지만, 엔진 현금은 `CashAndCashEquivalentsAtCarryingValue`(제한 현금 제외)라 순부채에도 섞이지 않는다(엔진 실행: NDAQ $365M·ICE $1,067M·CME $2,144M). → **기존 카드 세 장은 영향 없음.**
- CBOE 현금흐름 모델의 운전자본(유동자산 − 현금 − 투자자산 − (유동부채 − 단기차입))은 담보금 자산(제한 현금)과 회원 증거금 부채가 서로 상쇄돼 지금 $363M, 1년 전 $75M(매출 $5.1B 대비 작음) — 이번 범위에서는 손대지 않고 CBOE 카드 만들 때 E46(매각 예정 자산)과 함께 본다.
- 엔진에서 영업현금흐름을 쓰는 곳: PCR(자기 이력·동종업), 카드 FCF 문장·분기 차트(fill.py `q()`). 현금흐름 모델(영업이익 기반 FCF)·기초점수는 영업현금흐름을 쓰지 않는다. CBOE는 연구 패널에 없다(금융 업종 제외) → 연구 경로 영향 없음.

## 1. 장치
- 값 싣기: 기존 `company_tags`(adapters/company_tag_feed.py — 원문 인라인 XBRL에서 차원 없는 회사 고유 태그를 공시마다 꺼내 `.sec_cache/overlay/{cik}.json`에 빌린 표준 이름으로 저장, 비교 열 포함, accn·filed 그대로)로 `cboe:IncreaseDecreaseInRestrictedCashClearingFund`를 빌린 이름 `IncreaseDecreaseInRestrictedCashClearingFundCboe`에 싣는다(cfg_cboe `BUILD['company_tags']`, since 2019-01-01).
- 빼기: `build_multiple_history.py`에 `OCF_NETTING = {"0001374310": [("IncreaseDecreaseInRestrictedCashClearingFundCboe", -1)]}`(태그, 영향 부호). `pick_tag`의 영업현금흐름 처리(이미 중단영업 현금흐름을 같은 (start, end, accn)끼리 빼는 자리, AMD)에서 같은 방식으로 **영향을 뺀다**: `OCF_ex = OCF − sign × raw`(CBOE: OCF + raw). 누계 행끼리 빼므로 분기 역산(quarterly_flow)이 그대로 맞는다.
- `net_ocf(cik, rows)`(별도 함수, 사본으로):
  - cfg: `era_filed = "2020-10-30"`, `era_accn = "0001558370-20-012101"`, `era_period_end_after = "2020-06-30"`, `sign = -1`, `ocf_netting_confirmed_none = []`(원문으로 그 공시의 모든 대상 기간이 조정 불필요임을 확인한 accn만).
  - `filed < era_filed` → 그대로. 기간 결산일 ≤ `era_period_end_after`(2020-06-30, 인수 전) → 공시일과 상관없이 그대로. era 안: 같은 (start, end, accn) 담보금 행 있음 → `OCF − sign × raw`; 없음 → accn이 confirmed_none이면 그대로, 아니면 그 행 제외(카드: 경고·요약 표시 / 시험·회귀: 오류).
  - 원본 companyfacts 영업현금흐름에서 era 안 같은 (start, end, filed)·다른 accn이 있으면 오류.
  - 영업현금흐름 TTM 결산일 < 매출 TTM 결산일이면 PCR·FCF 계산 불가.

- 부호: CBOE는 10-K·10-Q 모두 영향 = −raw(sign = −1). 앵커 두 개(영업활동 담보금 줄 1개, 재무상태표 증거금 부채 증감과 같은 방향)로 시험에 고정.

## 2. 적용 범위
- 바뀌는 것: CBOE PCR(현재·자기 이력·동종업), FCF 문장·분기 차트, 그리고 CBOE를 동종업으로 쓰는 카드의 PCR 동종업 점수(E54 결정 ①과 같이 보고).
- 바뀌지 않는 것: 다른 카드의 자기 지표(NDAQ·ICE·CME 포함 — 직접 조정 없음), 현금흐름 모델, 기초점수, 연구 패널. CBOE 동종업 경유 변화는 보고 대상.
- 카드 문장: CBOE 카드에 "영업현금흐름·FCF·PCR은 청산소 담보금 유출입(회원 증거금·디폴트 펀드)을 뺀 값" 한 줄.

## 3. 검증
1. 새 시험 `v2/research/test_ocf_netting.py`: 가짜 자료로 누계 빼기·분기 역산, 짝 없는 행 처리(시기 전 그대로 / 시기 안 빠짐 → 행 제외 + 경고, 엄격 모드 오류), 부호 규칙, 지정 CIK만 작동.
2. 실물: CBOE Q1 2026 영업현금흐름 82.0, Q2 2026 단독 431.6, FY2025 1,224.1, FY2022 868.6, FY2021 663.0, 9개월 2025 뺀 값 846.3(= 1,400.5 − 554.2), 4분기 2025 단독 377.8을 원문 값으로 고정해 엔진 결과와 대조. 앵커: Q1 2026 영업활동 담보금 줄 1개, 재무상태표 증거금 부채 +1,825.7(같은 방향). overlay 단위 USD, 영업현금흐름 태그 하나.
3. 변이: 부호 뒤집기(앵커 시험이 빨개져야 함), accn 짝 조건 제거(같은 기간을 두 공시가 다른 값으로 보고하는 가짜 자료), 짝 없는 행 조용히 통과(같은 accn에 다른 짝은 있는데 이 행만 없는 자료), 미훑음 공시 통과 — 각각.
4. 기존 카드: CBOE를 동종업으로 쓰는 카드 목록을 먼저 뽑는다. freeze → 장치 넣고 전 카드 diff — 허용: CBOE 초안, 그 목록 카드의 PCR 동종업 점수와 그 점수 때문에 바뀐 판정(원인 표). 동종업 쪽 CBOE 영업현금흐름 TTM == 자기 카드 값 단언. 그 밖은 0.
5. CBOE 초안 전후 비교표(PCR 현재·5년 위치·자기 이력·동종업 점수·판정·FCF 문장·분기 차트 값).
6. pipeline/test_pipeline.py.

## 결정할 것
① 짝 없는 행(시기 안)을 "그 행 빼기 + 경고"로 할지, "빌드 멈춤"으로 할지. 권장: 카드 빌드는 빼기 + 경고(실행 요약에 표시), 시험·회귀는 멈춤.
② CBOE의 매각 예정 자산(호주·캐나다) 재분류가 운전자본에 섞이는 문제(E46)는 이번 범위 밖 — CBOE 카드를 만들 때 E46 처리 여부를 따로 정한다.

## 구현 기록 (2026-10-24, 사용자 승인 뒤)
- 리뷰: Codex(astra·medium)·Fable 4라운드 합의(필수 0건).
- 코드: `build_multiple_history.py` `OCF_NETTING`(CBOE 설정 한 곳 — 부호도 여기만), `net_ocf()`(pick_tag의 영업현금흐름 후보 태그 모두에 — 주 태그는 중단영업 빼기 뒤), `check_ocf_netting()`(main 시작 — 원본 companyfacts의 시대 안 accn 충돌·양식·최신 행 짝, RuntimeError라 동종업 유니버스에서는 그 종목만 빠짐). `research/test_ocf_netting.py`(규칙 시험 + CBOE 실물 고정값·앵커, 변이 4개 모두 잡힘).
- 값 싣기: `company_tag_feed.py 0001374310 cboe:IncreaseDecreaseInRestrictedCashClearingFund IncreaseDecreaseInRestrictedCashClearingFundCboe --since 2020-01-01` → overlay 48행(2020-10-30 10-Q가 첫 행, 그 전 3개 공시 0행). CBOE 카드를 만들 때 cfg `BUILD['company_tags']`에 같은 줄을 넣는다(매일 실행이 새 공시 뒤 다시 받게).
- 실물 결과: 뺀 영업현금흐름 Q1 2026 82.0, Q2 2026 431.6, 9개월 2025 846.3, 4분기 2025 377.8, FY2025 1,224.1, FY2022 868.6, FY2021 663.0, 최근 4분기(2026-06) 1,046.7(보고 1,962.8). PCR 14.7 → 27.7(10-01 종가).
- 구현 중 발견: CBOE는 영업현금흐름을 `…ContinuingOperations` 태그로도 34행 냈다(2013~2017 공시, 시대 밖이라 지금 영향 없음) — 후보 태그 모두에 같은 규칙을 걸어 나중에 태그를 바꿔도 빼지 않은 값이 들어오지 않게 했다.
- 피드 User-Agent는 기존 어댑터 값("kim research …")을 그대로 쓴다.
