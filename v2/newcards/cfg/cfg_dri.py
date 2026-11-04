BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # 중단사업 손실이 매 분기 조금씩 있다 — 희석 EPS 총액(Q1 FY27 2.04)이 아니라 계속사업(2.05)을 쓴다(회사 가이드·헤드라인도 계속사업)
NI_TAGS = ['IncomeLossFromContinuingOperations', 'NetIncomeLoss']
# DRI(다든 레스토랑) v2 카드 설정 — 자동 카드(AUTO). 회계연도 5월 마지막 일요일(52/53주 — FY26은 53주, Q4 FY26 14주). 외식 체인 — 올리브가든, 롱혼스테이크하우스, 파인다이닝(루스크리스·캐피털그릴·에디브이스), 기타(야드하우스·체더스·추이스 등).
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-10-02), 실적 보도자료(Q2 FY26~Q1 FY27, 8-K 2.02항 — 장 전 07시 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/DRI.md.
# 엔진 입력(2026-11-03): 계속사업 희석 EPS(BUILD eps_tag — 중단사업 손실이 매 분기 조금씩), 순이익도 계속사업(NI_TAGS). 차입금 = 단기(CP + 1년 안 채권) $979.7M + 장기 $1,636.1M = $2,615.8M(DEBT_TOTAL_TAG).
# 리스 $5,974M = 운용 $4,214M + 금융 $1,760M(금융리스는 대차대조표 기타부채 안 — 내재가치는 금융리스만 뺀다). 차입금 반영일 DEBT_AVAILABLE_FIX(2022-05·2023-05·2026-05).
# EV/EBITDA의 리스 처리(운용 포함·금융 제외)는 엔진 공통 설계 — 백로그 ⑩. 금융리스를 넣으면 15.7배로 더 비싸다(표 −1 같음, Fable). Q4 FY22·FY24 EPS는 보도자료 계속사업 값(Q4_EPS_OVERRIDE).
# 2026-10-30 사용자 결정(공시 대기만으로 보류하지 않는다) — Q2 FY27 실적(12월 중순 예상) 전 Q1 기준. 일회성: 최근 4분기 계속사업 10.30 중 폐점·손상·통합 비용 주당 0.44(4.3%, 비용 쪽).
CIK = '0000940944'
CUR, YO, QO = '2026-08-30', '2025-08-24', '2026-05-31'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-05-31', '2025-05-25'), 'FY2026'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Darden Restaurants'
S_ = 'https://www.sec.gov/Archives/edgar/data/940944/'
SEC = S_
TENQ = S_ + '000094094426000042/dri-20260830.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000094094426000032/exhibit991-q1fy27.htm', 'q4': S_ + '000094094426000016/exhibit991-q4fy26.htm', 'q3': S_ + '000094094426000005/exhibit991-q3fy26.htm', 'q2': S_ + '000094094425000067/exhibit991-q2fy26.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="driFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기에는 53주 해(FY26)의 14주짜리 4분기가 들어 있어 이익이 약 2% 부풀어 있다(53번째 주 EPS $0.25). '
              '내재가치는 차입금 $2.6B와 금융리스 $1.8B를 뺀다(운용리스 $4.2B는 임차료가 이미 영업비용에 들어 있어 빼지 않는다). 이익잉여금이 결손이고 자사주 매입으로 자본이 작아 PBR이 높다. '
              '동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['MCD', 'SBUX', 'CMG', 'YUM', 'DPZ', 'HLT']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '외식 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(DRI 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 외식·호텔 6곳만 보인다.')
# 매출(Q1 FY27 10-Q 부문, ConsolidationItemsAxis 영업 부문 값) — 1,329.8 + 860.9 + 304.2 + 705.4 = 3,200.3(연결과 일치).
SEG = [('올리브가든', 1329.8, '#5a2a1a'), ('롱혼스테이크하우스', 860.9, '#b8913f'), ('파인다이닝', 304.2, '#1f2a44'), ('기타 브랜드', 705.4, '#3f5e3a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q1 FY27)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07시 동부) → 같은 날.
NEWS_RANGE = '2025.12 ~ 2026.09'
NEWS = [
    ('red', '2026년 9월 24일 장 전 — Q1 FY27 실적', '2026-09-24',
     '매출 $3.20B(+5.1%) · 계속사업 순이익 $234M · 계속사업 희석 EPS $2.05(1년 전 $2.19, 캐나다 매각 이익 포함) · FY27 EPS 전망 $11.10~11.35 — 당일 주가 −3.0%', 'q1', 'Darden 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 6월 25일 장 전 — Q4 FY26 실적', '2026-06-25',
     '매출 $3.72B(14주, +13.7%) · 순이익 $405M · 계속사업 희석 EPS $3.54(1년 전 $2.58) · FY26 매출 $13.21B · EPS $10.44 — 당일 주가 −0.3%', 'q4', 'Darden 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 19일 장 전 — Q3 FY26 실적', '2026-03-19',
     '매출 $3.35B(+5.9%) · 순이익 $307M · 계속사업 희석 EPS $2.68(1년 전 $2.74, 바하마브리즈 손상 포함) — 당일 주가 +1.8%', 'q3', 'Darden 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 18일 장 전 — Q2 FY26 실적', '2025-12-18',
     '매출 $3.10B(+7.3%) · 순이익 $237M · 계속사업 희석 EPS $2.03(1년 전 $1.82) — 당일 주가 +1.8%', 'q2', 'Darden 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 28, 'nt': 21, 'mean': 236.05, 'median': 237, 'low': 210, 'high': 276, 'sb': 16, 'b': 2, 'h': 9, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-04'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q1 FY27 1,329.8/860.9/304.2/705.4(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"dri:OliveGardenSegmentMember": ["올리브가든", "#5a2a1a"], "dri:LongHornSteakhouseSegmentMember": ["롱혼스테이크하우스", "#b8913f"], "dri:FineDiningSegmentMember": ["파인다이닝", "#1f2a44"], "us-gaap:AllOtherSegmentsMember": ["기타 브랜드", "#3f5e3a"]},
 "ignore": []
}
