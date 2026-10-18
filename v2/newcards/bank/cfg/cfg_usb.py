# USB 은행 카드 설정 — bank_fill.py(사전 등록 7판). 분기마다 손으로 고치는 값은 없다.
# ANALYST는 토요일 실행(fetch_analyst.py)이 고친다.
CIK = '0000036104'
CO = 'U.S. Bancorp'
REV_TAG = ('NoninterestIncome', 'InterestIncomeExpenseNet')   # GAAP 총수익 = 비이자수익 + 순이자수익 — Revenues 태그($7,712M, Q2 2026)는 과세등가 조정 $26M을 더한 값이라 비이자수익이 섞였다(Codex 2026-10-17)
PB = ['JPM', 'PNC', 'TFC', 'FITB', 'MTB', 'HBAN']   # 비교 차트에 그릴 은행 6곳(값이 없으면 빠진다)
COLOR = '#d71e28'
BV_NOTE = "회사 TBVPS는 영업권·무형자산 관련 이연법인세를 더해 우리 값(이연법인세 미가산)보다 크다 — 무형자산에서 MSR은 빼고 계산한다(사전 등록 11-3)"
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 20, 'mean': 69, 'median': 68, 'low': 61, 'high': 76, 'sb': 13, 'b': 3, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-17'
NEWS = []   # 손 뉴스 없음 — 실적 보도자료 8-K는 news_auto.py가 넣는다
NEWS_DAYS = 400
