# SYF 은행 카드 설정 — bank_fill.py(사전 등록 7판). 분기마다 손으로 고치는 값은 없다.
# ANALYST는 토요일 실행(fetch_analyst.py)이 고친다.
# 2026-11-04 사용자 결정: 소비자 금융(제휴 신용카드)·저축은행 지주라 일반 카드 대신 은행 방식(P/TBV·RIM). 매출·영업이익 태그가 없다.
CIK = '0001601712'
CO = 'Synchrony'
REV_TAG = ('NoninterestIncome', 'InterestIncomeExpenseNet')   # 총수익 = 기타수익 + 순이자수익(Q3 2026 $4,914M) — Revenues 계열 태그 없음. 제휴사 몫(RSA, Q3 $1,096M)은 차감 전
PB = ['JPM', 'USB', 'PNC', 'FITB', 'RF', 'KEY']   # 비교 차트에 그릴 은행 6곳(값이 없으면 빠진다) — 카드 전업사(COF·AXP)는 S&P500 은행 비교군 밖
COLOR = '#3c3c3c'
BV_NOTE = "2026년 2분기 내부 사용 소프트웨어를 무형자산에서 빼 회사가 과거 TBV를 다시 계산했다 — 2026-03 이전 우리 TBV는 소프트웨어가 무형자산에 든(재작성 전) 값이라 약 8% 낮고, 그래서 1년 전 대비 증가율이 크게 나온다(회사 재작성 기준 $40.28 → $42.79, +6.2%). 효율성 비율은 제휴사 몫(RSA) 차감 전 수익 기준이라 회사 발표(Q3 2026 35.9%)보다 낮다. CET1(12.9%)은 축이 붙은 태그로만 내 카드에 빠져 있다"   # Codex·Fable r1 2026-11-04
PEER_NOTE = '카드 전업사 COF·AXP는 들어 있지 않다'   # 비교군은 예대 은행 — 업종이 다르다(Codex r1)
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 17, 'mean': 87.41, 'median': 87, 'low': 77, 'high': 104, 'sb': 10, 'b': 4, 'h': 9, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'
NEWS = []   # 손 뉴스 없음 — 실적 보도자료 8-K는 news_auto.py가 넣는다
NEWS_DAYS = 400
