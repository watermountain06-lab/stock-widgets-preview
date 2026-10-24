# E54 설계 최종본 — 세전 일회성 손익 장치 (`v2/eps_oneoff.json`)

5라운드(Codex astra·medium + Fable) 뒤 본문을 r5 결정으로 맞춘 판. 계산 규칙은 r5와 같다.

## 사용자 결정 (2026-10-24)
① 동종업 경로는 예외로 인정하고 바뀌는 카드를 보고 ② 반복 평가손익(지분·코인·헤지)은 별도 안건 ③·⑤ 항목별 세금 효과(0 포함)를 회사가 밝힌 항목만 넣고, 넣은 항목은 세전이익·세금에서도 함께 뺀다 ④ 연구 경로(verdict_replay·5년 관문)에 지금 넣는다 ⑥ 주당 영향이 세전뿐이거나 없는 종목(FANG·TWLO·COHR)은 보류 유지.

## 1. 범위
- 일회성만: 손상·감액, 사업·자산 매각 손익, 소송 합의·벌금, 계약 해지 손익.
- **이번 대상: ADM 하나.** 보도자료가 항목별 세전·세후 금액과 세후 주당 영향을 밝힌다(2025-06~2026-06 다섯 분기). Wilmar 벌금·이익 몫은 지분법 손익(원래 세후)이라 세금 효과 0.
- ADM은 엔진 영업이익 태그·합성 규칙이 없어 이번에는 `line="pretax"`(EPS·세율만)로 넣고 `opinc_status: "undefined"`를 적는다. ADM 카드에 영업이익 합성 규칙을 넣는 날, 불러오기 검사가 이 표시를 오류로 바꿔 위치를 다시 정하게 한다.
- **KR은 빠진다**: KR EPS 이력 파일(카드·연구 공통)에 16주 1분기와 4분기 행이 없고 `ttm_eps`가 1년 반에 걸친 4행 합이다. 새 안건(EPS 이력의 16주 분기)이 먼저다. KR은 파일에 넣지 않고, KR형 실패는 가짜 종목 시험으로만 본다.
- 계속 보류: FANG·TWLO·COHR(결정 ⑥), ROP·ILMN·COIN·VST·EQT(결정 ②). DAL 카드는 바꾸지 않는다.

## 2. 파일 형식
```json
{"_note": "...",
 "ADM": [{
   "id": "ADM-2025Q3-impairment",
   "quarter_end": "2025-09-30", "filed": "2025-11-04",
   "line": "pretax", "opinc_status": "undefined",
   "adj_pretax": 261000000, "adj_tax": 60000000, "adj_eps": 0.41,
   "tax_basis": "disclosed",
   "tags": {"pretax_dcf": "<엔진 DCF 세율 경로가 고르는 세전이익 태그 또는 합성 경로 이름>", "pretax_includes": true},
   "desc": "Impairment, exit, restructuring and settlement contingencies", "source": "https://www.sec.gov/Archives/...ex99..."
 }]}
```
- 부호: 모든 adj 칸은 "GAAP 숫자에 **더하면** 항목이 빠지는 값"(손실 +, 이익 −). adj_eps는 세후·단일 분기, 공시 당시 주식 기준. adj_tax는 법인세비용에 더하는 값(손실 add-back이면 +).
- `tax_basis`: `"disclosed"`(세전·세후 둘 다 공시) | `"equity_method"`(지분법 손익, adj_tax = 0) | `"disclosed_anomalous"`(세금이 세전보다 크거나 부호가 다른 공시 — 경고만).
- `line`: `"pretax"`(영업이익 밖, 세전이익 안) | `"opinc"`(영업이익 안 — `tags.opinc`·`opinc_includes`·`tags.dda`·`dda_excludes` 필수). `tags.pretax_a8`은 core 종목만.

**불러올 때 검사(오류로 멈춤)**: 칸·형식, `id` 유일, (quarter_end, desc) 중복 금지, adj_tax 필수, tax_basis 규칙, `adj_eps ≠ 0`이면 `sign(adj_eps) == sign(adj_pretax − adj_tax)`(주당 0.00 허용), `*_includes·dda_excludes`는 참이어야 함, `opinc_status="undefined"`인데 그 CIK에 엔진 영업이익(태그·DERIVED_OPINC)이 있으면 오류, tax_oneoff.json 같은 종목·분기에 `pretax` 칸이 있으면 오류.

**진입점별 검사(그 진입점이 가진 달력으로)**: 항목 결산일이 그 지표의 분기 달력(EPS 파일 분기 / 세금·세전이익 quarterly_flow 결산일)에 없으면 오류. 카드 모드 cap과 base_inputs 최신 TTM의 기준 차이는 경고.

**시험 때 검사**: `|adj_eps × 그 분기 가중평균 희석 주식 수(공시 당시)|`가 `|adj_pretax − adj_tax|`의 ±10% 또는 주당 ±$0.006 안.

## 3. 적용 방식
### 3.1 구성 분기
- 세금·세전이익(·영업이익) TTM: `bmh.ttm_quarters(quarters, ttm_end)` — `ttm_series`와 같은 창(연속 4개, 끝~끝 310일 이하)의 결산일 4개. 분기 `start`는 쓰지 않는다.
- 엔진 함수 서명은 그대로 두고 `_entry` 변형을 추가: `latest_entry`(항목 전체 + 고른 태그), `ttm_fresh_entry`, `paired_entry`(최종 선택 결산일). 기존 호출부는 바뀌지 않는다(빈 파일 diff 0).
- EPS 파일(카드 PER·백테스트·연구 대체 경로): 그 행 이하 연속 4행이 (a) `ttm_eps == quarter_eps 4개 합`(±0.011) 그리고 (b) 첫~끝 결산일 ≤ 310일일 때만 구성 분기로 인정. **지정 종목이고, 그 행 TTM에 들어갈 수 있는 항목(행 결산일 − 항목 결산일이 0~400일)이 있을 때만** 검사하고, 못 넘으면 오류. `drop_stale_quarters`는 이 판정 안에서만 쓴다(전 종목 EPS 시리즈에는 쓰지 않음).
- 연구 `pit.eps_ttm`: 각 TTM 행에 원천 분기 결산일 `q_ends`를 함께 돌려준다. 원천 필터(80~100일)는 고치지 않는다(16주 분기 종목은 pit 행이 없어 파일 경로로 감 — 새 안건에 기록).
- 항목은 `quarter_end`가 구성 결산일 4개 중 하나일 때만 더한다.

### 3.2 적용 표
| 지표 | 더하는 값 | 항목 |
|---|---|---|
| PER EPS(현재·5년 이력·밴드·백테스트) | Σ adj_eps ÷ split_ratio(filed, 그 EPS와 같은 분할 목록) | 전부 |
| DCF 세율: 세전이익 TTM / 법인세 TTM | Σ adj_pretax / Σ adj_tax | 전부 — **세금·세전이익 TTM 결산일이 같을 때만**, 다르면 건너뛰고 경고 |
| 영업이익 TTM·현금흐름 영업이익률 이력·EV/EBITDA·A8 영업이익 | Σ adj_pretax | line=opinc(이번 대상 없음 — 가짜 종목 시험으로만 검증) |
| A8 세율(카드, core 종목) | 위 세율 규칙 | 전부(이번 대상 없음) |
| D&A | 0 | — |
- A8(카드): 원본 결측 확인 → 조정 → 조정 값으로 양수 검사 → 세율·이익.
- 입력 목록·시리즈는 고치지 않는다. tax_oneoff.json은 그대로(부호·330일 창·시점·분할 규칙 유지)이고 두 파일은 각자 규칙으로 계산해 더한다.

### 3.3 시점
- 카드 모드(`bmh.ASOF_REF is None`): 모든 경로가 같은 항목 집합 `filed ≤ 카드 공시 기준 cap`(없으면 오늘), 과거 TTM에도 소급.
- 연구 모드: `filed ≤ asof`. EPS는 행마다 `filed ≤ 그 행 available`. 항목 공시일 F가 늦으면 F 시점 최신 행의 TTM이 항목 분기를 포함할 때만 F에 그 최신 행 값 + 항목으로 관측 추가, 이탈했으면 추가 없음, 같은 날 사건은 합침.

## 4. 연구 경로
- `verdict_replay.py`: EPS(:327·:332)에 3.3 규칙(pit `q_ends` / 파일 증명), `_override_filed`·`provenance`에 eps_oneoff.json. 연구 `core_earnings`·`a8_core_replay.py`는 넣지 않는다(연구 A8은 GAAP 경로 그대로). `c14_*`는 12-01 실행 문서가 부르지 않으면 넣지 않는다.
- `engine_regress.py` ENGINE_GLOBS에 추가.
- ADM은 학습 패널 28행(현금흐름 계산 0행 — 영업이익 없음, 자기 이력 칸 28행)·5년 관문 패널 30행에 있다. 승인 뒤 두 패널 재생성 → 바뀐 행 보고(허용: ADM 행의 자기 이력·EPS 관련 칸, ADM을 동종업으로 쓰는 행의 동종업 칸) → 재봉인 → 친구 엔진 사전 등록 변경 기록. 수익률 붙이지 않음.

## 5. 카드 문장
실제로 적용된 경로 목록(PER·현금흐름 세율·[opinc면] 출발 이익률·영업이익률 이력·EV/EBITDA·본업 이익)에서 만든다. 세율을 건너뛰었으면 넣지 않는다. "분기 표와 기초점수의 영업이익률·이자보상은 GAAP 그대로"를 함께.

## 6. 검증
1. 새 시험 `v2/research/test_eps_oneoff.py`(test_pipeline.py 무수정). 고정 자료: 가짜 종목(KR형 112·84·84·84일, 53주형 91·98·91·84일, 파생 4분기, 빈 분기 1개, KR형 '합은 맞지만 1년 반' EPS 파일).
   - 손 계산 3건: line=pretax(세율·EPS, 영업이익 불변) · adj_tax=0 지분법(세율 분모·EPS) · line=opinc + adj_tax(영업이익 TTM·EBITDA·이력 이익률·세율·EPS).
   - 경계: TTM 편입·이탈, 첫 구성 분기가 파생 4분기·그 앞 항목은 이탈, 달력에 없는 결산일 오류, 빈 분기·KR형 파일 증명 실패 오류, 증명은 항목 근처 행에서만, 두 파일 pretax 중복 오류, dda_excludes 거짓 오류, adj_tax 빈칸 오류, opinc_status undefined인데 엔진 영업이익 있음 오류, 세금·세전 TTM 결산일 다름 → 세율 건너뜀 + 경고(EPS는 조정).
   - 늦은 공시: (i) F > 10-Q 공시일 → F부터 (ii) F > 다음 분기 공시이고 다음 TTM에도 항목 → F에 최신 행 기준 관측 (iii) 이탈 뒤 F → 없음.
   - 분할: F 뒤 2:1 분할 → adj_eps 절반.
2. 변이 시험(각각 위 시험이 빨개져야 함): 부호 뒤집기, filed 검사 제거, 종목 검사 제거, 330일 창(빈 분기 사례), 관측 추가 규칙 제거(늦은 공시 (i)·(ii)), 일반 태그 대조 제거(선언·선택 불일치 시험 — 시험용 PRETAX_TAG_BY_CIK 주입), 지분법 포함 검사 제거(지분법 제외 태그 + equity_method 시험).
3. 기존 카드: freeze → (a) 빈 `{}` 전 카드 diff 0 (b) ADM 항목 입력 뒤 전 카드 diff — 허용: ADM 초안과 ADM을 동종업으로 쓰는 카드의 동종업 점수·그 점수가 들어간 판정. 바뀐 카드별 크기 표. 영향 밖 대표 카드 compare_render 동일.
4. 손 계산(실물): ADM 한 TTM — 10-Q·10-K 원문의 분기 GAAP 희석 EPS(4분기는 보도자료 GAAP 분기 EPS, 연간 − 9개월과 ±$0.03 안인지 함께) 합 + Σadj_eps를 엔진 PER EPS와 대조. 세율도 같은 TTM으로.
5. ADM 전후 비교표: PER(현재·5년 위치)·자기 이력 점수·세율. EV/EBITDA·출발 이익률은 "해당 없음(영업이익 없음)". 세율을 건너뛰었으면 그렇게 표기.
6. pipeline/test_pipeline.py 실행.

## 새 안건 제안
- E58(가칭) EPS 이력의 16주 분기: KR(1분기 16주) EPS 파일에 1·4분기 행이 없고 TTM이 1년 반에 걸친다. `pit.eps_ttm`도 80~100일 필터로 16주 분기를 버려 KR은 행 0개 → 연구도 같은 파일. 카드·연구 KR 자기 이력이 틀렸을 수 있다. 같은 회계 구조(12·12·12·16주 등) 종목 전수 확인 필요.
