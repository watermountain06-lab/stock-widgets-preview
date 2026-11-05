# RJF 은행 카드 설정 — bank_fill.py(사전 등록 7판). 분기마다 손으로 고치는 값은 없다.
# ANALYST는 토요일 실행(fetch_analyst.py)이 고친다.
# 2026-11-05 사용자 결정: 자산관리·증권 + 은행 부문(예금) 지주라 일반 카드 대신 은행 방식(P/TBV·RIM). 회계연도 9월 30일 —
# bank_fill·bank_rim이 결산월을 10-K에서 읽는다(같은 날 엔진 수정). 분기 이름은 회사 회계 분기(Q3 FY26 = 2026-06-30).
# 검토(Codex·Fable r1·r2, 2026-11-05): (0, −1, −1) 재현. 환원 정의 — 현금흐름표 매입(원천징수 포함 $1,672M) + 보통주 배당 $423M − 직원 주식 발행 $38M = $2,057M이면
# 지금($1,977M)보다 +$80M, RIM −2 경계는 +$117M. 직원 주식 발행(ProceedsFromIssuanceOfSharesUnder…)은 엔진 기본 발행 태그 밖이라 0(빼면 RIM이 조금 오른다 — 방향만 보수적).
# 일회성 시험: 회사 조정은 인수 관련 비용뿐(세후 Q1~Q3 FY26 $15/22/25M, 상각·보상이 매 분기 반복) — 최근 4분기 약 $80M을 더해도 RIM 비율 약 1.41(−1), 동종업 PER 점수 15~23(−1)으로 표 불변.
CIK = '0000720005'
CO = 'Raymond James'
REV_TAG = 'RevenuesNetOfInterestExpense'   # 순수익(이자비용 차감 뒤, 회사 헤드라인 "Net revenues") — Revenues는 이자수익 포함 총수익이라 쓰지 않는다
PB = ['JPM', 'USB', 'FITB', 'RF', 'MTB', 'HBAN']   # 비교 차트에 그릴 은행 6곳(값이 없으면 빠진다) — SCHW와 같은 묶음
COLOR = '#003c71'
BV_NOTE = "10-Q는 영업권·무형자산을 합친 한 줄로만 내서 카드는 FY2025 10-K 값($1,847M)을 이어 쓴다. 2026-06-30 10-Q 합계는 $2,608M(2026년 GreensLedge·Clark Capital 인수)이라 이 TBVPS는 약 $3.96 높고 P/TBV는 낮게 나온다(10-Q 합계로 계산하면 TBVPS $52.52, P/TBV 3.21배). 바로잡아도 표는 같다 — 자기 이력은 P/TBV 점수 13.6과 PER 52가 방향이 갈려 0, 동종업은 P/TBV가 비싼 쪽 2번째에서 가장 비싼 쪽으로(점수 8.3 → 0) 가도 PER 15.4와 함께 −1"   # 2026-11-05 계산
PEER_NOTE = '증권·자산관리 회사 SCHW·MS·GS는 들어 있지 않다'
ANALYST = {'rating': 'Buy', 'n': 16, 'nt': 11, 'mean': 181.91, 'median': 179, 'low': 160, 'high': 205, 'sb': 3, 'b': 3, 'h': 10, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-04'
NEWS = []   # 손 뉴스 없음 — 실적 보도자료 8-K는 news_auto.py가 넣는다
NEWS_DAYS = 400
