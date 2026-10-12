# GS 은행 카드 설정 — bank_fill.py(사전 등록 7판, 2026-10-11). 분기마다 손으로 고치는 값은 없다.
# ANALYST는 토요일 실행(fetch_analyst.py)이 고친다.
CIK = '0000886982'
CO = 'Goldman Sachs'
REV_TAG = 'RevenuesNetOfInterestExpense'   # 순영업수익(이자비용 차감 뒤) 태그
PB = ['JPM', 'BAC', 'USB', 'FITB', 'RF', 'MTB']   # 비교 차트에 그릴 은행 6곳(값이 없으면 빠진다)
COLOR = '#0f6eb4'
BV_NOTE = "회사 기본주식 수(근무 조건 없는 RSU 포함)보다 분기말 유통 주식 수가 2~4% 적어 BVPS가 회사 발표보다 그만큼 높게 나온다"
ANALYST = {'rating': 'Hold', 'n': 26, 'nt': 16, 'mean': 1098.38, 'median': 1066, 'low': 955, 'high': 1299, 'sb': 7, 'b': 1, 'h': 16, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-12'
NEWS = []   # 손 뉴스 없음 — 실적 보도자료 8-K는 news_auto.py가 넣는다
NEWS_DAYS = 400
