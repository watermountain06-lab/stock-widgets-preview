# C 은행 카드 설정 — bank_fill.py(사전 등록 7판, 2026-10-11). 분기마다 손으로 고치는 값은 없다.
# ANALYST는 토요일 실행(fetch_analyst.py)이 고친다.
CIK = '0000831001'
CO = 'Citigroup'
REV_TAG = 'Revenues'   # 순영업수익(이자비용 차감 뒤) 태그
PB = ['JPM', 'BAC', 'USB', 'FITB', 'MTB', 'RF']   # 비교 차트에 그릴 은행 6곳(값이 없으면 빠진다)
COLOR = '#0f6eb4'
BV_NOTE = ""
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 15, 'mean': 153.33, 'median': 155, 'low': 135, 'high': 165, 'sb': 13, 'b': 5, 'h': 5, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-17'
NEWS = []   # 손 뉴스 없음 — 실적 보도자료 8-K는 news_auto.py가 넣는다
NEWS_DAYS = 400
