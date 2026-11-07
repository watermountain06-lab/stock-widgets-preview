# MTB 은행 카드 설정 — bank_fill.py(사전 등록 7판). 분기마다 손으로 고치는 값은 없다.
# ANALYST는 토요일 실행(fetch_analyst.py)이 고친다.
CIK = '0000036270'
CO = 'M&T Bank'
REV_TAG = ('NoninterestIncome', 'InterestIncomeExpenseNet')   # GAAP 총수익 = 비이자수익 + 순이자수익(Q3 2026 743 + 1,793 = $2,536M) — Revenues 태그는 2023-12에 멈춤
PB = ['USB', 'PNC', 'FITB', 'HBAN', 'CFG', 'RF']   # 비교 차트에 그릴 은행 6곳(값이 없으면 빠진다)
COLOR = '#00704a'
BV_NOTE = "MSR(주택담보대출 서비스권)은 원래 기타자산이라 무형자산에 들지 않아 TBV에서 따로 빼지 않는다 — 2026년부터 공정가치로 바꿔(2026-09 $572M) 그날 이익잉여금이 $197M(주당 약 $1.4) 늘었다. 회사 TBVPS는 무형자산 관련 이연법인세를 더해 우리 값보다 조금 크다"   # Fable r1 2026-11-07
ANALYST = {'rating': 'Hold', 'n': 22, 'nt': 20, 'mean': 248.63, 'median': 248.5, 'low': 198, 'high': 300, 'sb': 3, 'b': 3, 'h': 14, 's': 0, 'ss': 2}
ANALYST_ASOF = '2026-11-07'
NEWS = []   # 손 뉴스 없음 — 실적 보도자료 8-K는 news_auto.py가 넣는다
NEWS_DAYS = 400
