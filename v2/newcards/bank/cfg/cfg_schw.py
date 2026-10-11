# SCHW 은행 카드 설정 — bank_fill.py(사전 등록 7판, 2026-10-11). 분기마다 손으로 고치는 값은 없다.
# ANALYST는 토요일 실행(fetch_analyst.py)이 고친다.
CIK = '0000316709'
CO = 'Charles Schwab'
REV_TAG = 'Revenues'   # 순영업수익(이자비용 차감 뒤) 태그
PB = ['JPM', 'USB', 'FITB', 'RF', 'MTB', 'HBAN']   # 비교 차트에 그릴 은행 6곳(값이 없으면 빠진다)
COLOR = '#00a0df'
BV_NOTE = ""
ANALYST = {'rating': 'Buy', 'n': 22, 'nt': 17, 'mean': 121.82, 'median': 125.0, 'low': 95.0, 'high': 145.0, 'sb': 11, 'b': 7, 'h': 3, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-05'
NEWS = []   # 손 뉴스 없음 — 실적 보도자료 8-K는 news_auto.py가 넣는다
NEWS_DAYS = 400
