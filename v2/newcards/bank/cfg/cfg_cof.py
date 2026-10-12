# COF 은행 카드 설정 — bank_fill.py(사전 등록 7판, 2026-10-11). 분기마다 손으로 고치는 값은 없다.
# ANALYST는 토요일 실행(fetch_analyst.py)이 고친다.
CIK = '0000927628'
CO = 'Capital One'
REV_TAG = 'Revenues'   # 순영업수익(이자비용 차감 뒤) 태그
PB = ['JPM', 'USB', 'FITB', 'RF', 'MTB', 'HBAN']   # 비교 차트에 그릴 은행 6곳(값이 없으면 빠진다)
COLOR = '#004977'
BV_NOTE = "회사 TBVPS는 인수 무형자산의 이연법인세를 더해, 우리 값(더하지 않음)이 2025년 2분기 인수 뒤 약 6% 낮게 나온다"
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 19, 'mean': 254.47, 'median': 259, 'low': 219, 'high': 300, 'sb': 14, 'b': 5, 'h': 5, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-12'
NEWS = []   # 손 뉴스 없음 — 실적 보도자료 8-K는 news_auto.py가 넣는다
NEWS_DAYS = 400
