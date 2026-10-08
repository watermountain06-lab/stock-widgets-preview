# 분기 반영 절차 (v2 카드)

매일·토요일 재빌드는 **SEC 재무를 자동으로 넣지 않는다**(2026-10-06 사용자 결정). 새 10-Q·10-K는 사람이 점검을 거쳐 이 절차로 반영한다.
첫 사례는 COST FY2026 10-K(2026-10-08) — 원자료 기록 `newcards/quarterly/COST_Q4FY26.md`.

## 0. 시작 신호
- 토요일 실행의 `v2/daily_status.json` → `newFilings`(카드 재무보다 새 10-Q·10-K, `newcards/new_filings.py`), 또는 실적 발표 뒤 직접.
- 8-K 보도자료만 나오고 10-Q·10-K가 아직이면 기다린다(`research/pipeline_checks.md` 1-3). 카드 문장에는 보도자료 숫자를 "발표, 공시 전"으로만 적을 수 있다.

## 1. 기다릴 것 — 시점 규칙
- 카드의 배수·내재가치는 **카드 마지막 종가 날짜까지 제출된 공시만** 쓴다. 공시 제출일 **이후 첫 종가**가 카드에 들어온 뒤에 반영한다
  (COST: 10-K 10/7 제출 → 10/7 종가부터. 그 전에 돌리면 내재가치 블록은 옛 분기, 다른 칸은 새 분기로 섞인다).

## 2. 원자료 모으기 — `newcards/quarterly/{T}_{분기}.md`
설정 파일에 손으로 넣는 값을 출처와 함께 한 파일에 적는다(에이전트에게 맡겨도 된다. 값마다 문서·표 이름, 못 찾으면 "미확인").
- 공시 링크·접수번호·제출일, 분기·연간 손익(보도자료와 10-Q/K), 재무상태표(현금·단기투자·재고·매입채무·유동자산/부채·차입금·총자산·자본),
  자본배분(자사주·한도·배당), 운영 지표(매장·비교매출 등), 다음 실적일, 이 공시에서 새로 나온 것(사채·소송·회계 변경·가이던스).
- 점검(`research/pipeline_checks.md`): 2-1 4분기 EPS(연간 − 1~3분기 = 보도자료?), 3-1 분기 길이, 2-2 차입금 합, 보도자료와 공시의 숫자 차이.

## 3. 승인 — `v2/sec_approved.json`
- `{"CIK": "공시 제출일"}`을 더한다(같은 회사의 다음 분기면 날짜를 바꾼다). SEC 자료를 읽는 `build_multiple_history._facts`가 보충 자료(overlay)까지
  합친 뒤 그 날짜까지 제출된 자료만 쓰고, 캐시가 그보다 오래됐으면 SEC에서 새로 받는다 — GitHub Actions의 옛 캐시에서도 승인한 분기가 유지되고,
  승인하지 않은 다음 공시는 들어가지 않는다. 승인한 공시가 자료에 없으면(SEC 반영 지연) 그 카드는 멈추고 전날 상태로 남는다.
- 한계(Codex 2026-10-08): 이 상한은 `_facts`를 거치는 길에만 걸린다. 외국 기업 어댑터·`vendor/fetch_financials.py`·`fetch_eps_history.py`는
  직접 받지만 매일 가격 재빌드에서는 돌지 않는다. 토요일 비교군 갱신은 비교 종목(카드 아님)의 새 공시를 쓸 수 있다.

## 4. 설정 파일 손질 — `newcards/cfg/cfg_{t}.py`
분기마다 바뀌는 칸(COST 기준): `CUR·YO·QO`(분기 말 날짜), `QLABEL·YL·QQL`, `RELEASE`(보도자료 손익), `PR`·`PR_CUR`(보도자료 링크),
`TENQ·TENQ_NAME`(10-Q/K 링크), `FY_ENDS`, `L8`(8분기 라벨), `STAT3`, `NEXT·NEXT_OP·CHECK_WHEN`(다음 실적), `FY_LABEL`, `HEALTH_NOTE`,
`YOY_EXTRA`, `SEG·SEG_ADJ·SEG_NOTE`(제품군 매출), `CAPITAL`, `CHECK`(다음 확인 포인트), `FUND_ASOF_NOTE`, `NEWS`, `SUMMARY·BULL·BEAR`, 그리고
"공시 전" 안내 문장(PREMISE·FUND_TIP 등)을 지운다.
- 먼저 사본(`newcards/quarterly/cfg_{t}_{분기}_draft.py`)에 고쳐 두고 적용한다.
- `POST`의 생성 문구 치환은 분기 변수(`C.CUR`·`C.QLABEL`)로 쓴다 — 그래야 다음 분기에 이 블록을 다시 고치지 않는다(COST에서 바꿈).

## 5. 다시 만들기
```
cp v2/{T}_full_widget.html …  # 백업(카드·cfg·배수·EPS·재무·추적선·활동성)
REFRESH=1 python3 v2/newcards/build.py T --weekly     # EPS·재무·SEC·추적선까지 새로
```
- 채우기(fill.py)에서 멈추면 대개 4번에서 놓친 생성 문구다. 출력에 맞춰 cfg를 고친다.
- `python3 v2/newcards/compare_render.py T <백업 카드>`로 바뀐 줄을 모두 읽는다. 남은 옛 분기 표현(`Q3 FY26`, "10-K 전", 옛 날짜)을 찾는다.
- `python3 v2/newcards/check_literals.py T` — 문장 속 계산값 리터럴 0곳.
- 백테스트에 새 체크포인트를 넣는다: `python3 v2/refresh_backtest.py T` 뒤 `REFRESH=1 python3 v2/newcards/build.py T --price`.
  옛 카드에서 가져온 백테스트는 밴드가 지금 규칙과 달라 적중률이 바뀔 수 있다(COST 62.4% → 51.3%) — 바뀐 값을 보고에 적는다.
- 16주·12주처럼 길이가 다른 분기를 견주는 표는 주당 환산을 함께 적는다(COST `_qoq_week`).

## 6. 검토·반영
- Codex(코드·자료), Fable(카드 문장 ↔ 원자료 대조) 검토를 반영한다.
- preview 커밋(카드·cfg·원자료 기록·`sec_approved.json`·EPS/재무 파일) → `python3 pipeline/sync_v2_home.py` → 첫 화면.
- 판정이 바뀌면 목록으로 보고한다. 라이브(redesign) 승격은 승인 때.
