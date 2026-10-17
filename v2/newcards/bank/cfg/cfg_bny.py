# BNY 은행 카드 설정 — bank_fill.py(사전 등록 7판). 분기마다 손으로 고치는 값은 없다.
# GICS는 자산운용·수탁은행이지만 예금 조달·CET1 규제를 받는 은행 지주회사라 은행 경로(SCHW 선례, 2026-10-17 사용자 결정).
# ANALYST는 토요일 실행(fetch_analyst.py)이 고친다.
CIK = '0001390777'
CO = 'BNY'
REV_TAG = ('NoninterestIncome', 'InterestIncomeExpenseNet')   # 총수익 = 비이자수익(수수료 등) + 순이자수익 — 분기 단일 태그 없음(Revenues는 10-K 연간만)
PB = ['JPM', 'USB', 'FITB', 'RF', 'MTB', 'HBAN']   # 비교 차트에 그릴 은행 6곳(값이 없으면 빠진다)
COLOR = '#2a9db0'
BV_NOTE = "회사 TBVPS($32.81, 2026-06-30)는 영업권·무형자산 관련 이연법인세부채 $1.9B를 더해, 우리 값(더하지 않음)이 약 8% 낮다 — 영업권·무형자산이 보통주 자본의 약 49%라 다른 은행보다 차이가 크다"
PEER_NOTE = '수탁은행 STT·NTRS는 들어 있지 않다'   # 비교군 밖 은행의 동종업 문장에 붙는다(bank_fill PREM)
ANALYST = {'rating': 'Buy', 'n': 17, 'nt': 14, 'mean': 165.64, 'median': 162, 'low': 150, 'high': 182, 'sb': 6, 'b': 3, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-17'
NEWS = []   # 손 뉴스 없음 — 실적 보도자료 8-K는 news_auto.py가 넣는다
NEWS_DAYS = 400
