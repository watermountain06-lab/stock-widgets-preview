# DAL(델타항공) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 189. 항공 여객·화물, 정유 부문(Monroe 정유소 — 대부분 외부 판매분이 매출에 들어간다).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-10T00:22Z 접수, 10/9 저녁), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 8-K 10:30 ET 장중 접수, 장 전 발표로 봄), StockAnalysis. 사전 조사 자료표 scratchpad pre/DAL.md.
# 엔진 입력(2026-10-23): 설비투자 = 항공기 + 지상 설비(SUM_TAGS_BY_CIK — 합계 태그 2026-03 멈춤, TTM $4,978M), 이자비용 = 10-Q '순 이자비용'(interest_extra.json — 총액 미공시, 태그 2018 멈춤),
# 과거 성장 창 2022-12-31부터(build_dcf HISTORY_WINDOW — 코로나 저점 기저효과), 재고 = 항공 관련 재고(INVENTORY_ALT, 당좌비율), 차입금 $12,105M + 금융리스·운용리스, 비영업 자산 = 지분 투자(Air France-KLM·LATAM·대한항공 등, 시가 평가) $3.4B, 4분기 EPS 2021·2022·2023·2025 보도자료 값.
CIK = '0000027904'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, 1), '적정~저평가'
CO = 'Delta'
S_ = 'https://www.sec.gov/Archives/edgar/data/27904/'
SEC = S_
TENQ = S_ + '000002790426000038/dal-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000002790426000035/deltaairlinesannouncessept.htm', 'q2': S_ + '000002790426000029/deltaairlinesannouncesjune.htm',
      'q1': S_ + '000002790426000020/deltaairlinesannouncesmarc.htm', 'q4': S_ + '000002790426000008/deltaairlinesannouncesdece.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="dalFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-20, 20)
ACT_REASON = ''
NONOP_WHAT = '지분 투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('GAAP 이익은 보유 지분(해외 항공사 등)의 시가 평가 손익과 정유 헤지 손익 때문에 분기마다 크게 흔들리고, 5년 이력 앞부분에는 코로나 적자·작은 이익 분기가 있어 GAAP PER로 보는 자기 이력 비교는 믿을 만한 정도가 제한된다 — 회사가 발표하는 조정 이익은 훨씬 고르다. '
              '매출에는 정유 부문의 외부 판매가 들어 있다 — 빼고 보면 Q3 2026 매출 증가율은 약 21%가 아니라 약 16%이고, 항공 부문 영업이익률은 연결보다 조금 높다. '
              '현금흐름 모델의 과거 성장률은 코로나 저점을 피하려 2022년 말부터 잰다. 비영업 자산은 시가로 평가하는 지분 투자만이고(지분법 투자는 빠짐), 연금 부채와 항공권·마일리지 선수금 같은 큰 영업 부채는 차입금에 넣지 않았다.')
HEALTH_EXTRA = '이자비용은 10-Q가 이자수익을 뺀 순액만 공시해 이자보상배율이 실제보다 높게 보일 수 있다.'   # 고정 문장(2026-10-23)
PH = ['UNP', 'CSX', 'UPS', 'GE', 'BA', 'UBER']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '운송·항공 관련 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(DAL 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·건설이 섞여 있다. 카드가 있는 항공사가 없어 차트에는 운송·항공 관련 6곳을 보인다.')
# 매출(Q3 2026 10-Q 주석 9 부문) — 항공 17,585 + 정유 2,967 − 부문 간 거래(정유→항공) 366 = 20,186. 1년 전 15,197·1,795·−319.
SEG = [('항공', 17585.0, '#003366'), ('정유', 2967.0, '#c8102e')]
SEG_ADJ = -366.0
SEG_ADJ_LABEL = '부문 간 거래 제거'
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다). 반응일: 8-K 장중(10:30 ET) 접수, 보도자료 장 전 → 같은 날.
# 넣지 않은 8-K: 항공기 주문(1/13 보잉 787-10 30대, 1/27 에어버스 31대 — 인도 2029~), 신용 한도(6/12), 투자자 자료·임원·주총.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 9일 — Q3 2026 실적', '2026-10-09',
     '매출 $20.19B(1년 전 $16.67B, 정유 외부 판매 포함) · 순이익 $756M · 희석 EPS $1.15(1년 전 $2.17) — 지분 투자 평가손 $218M·헤지 손실 $208M 포함', 'q3', 'Delta 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 10일 — Q2 2026 실적', '2026-07-10',
     '매출 $19.76B · 순이익 $1.60B · 희석 EPS $2.44(1년 전 $3.27) — 지분 투자 평가익 $349M·헤지 이익 $301M 포함', 'q2', 'Delta 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 8일 — Q1 2026 실적(GAAP 적자)', '2026-04-08',
     '매출 $15.85B · 순손실 $289M · 희석 EPS −$0.44(1년 전 $0.37) — 지분 투자 평가손 $550M·헤지 손실 $151M 포함', 'q1', 'Delta 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 13일 — Q4 2025 실적', '2026-01-13',
     '매출 $16.00B · 순이익 $1.22B · 희석 EPS $1.86(1년 전 $1.29) — 지분 투자 평가익 $205M 포함', 'q4', 'Delta 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 25, 'nt': 18, 'mean': 103.78, 'median': 102, 'low': 95, 'high': 125, 'sb': 19, 'b': 5, 'h': 0, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 부문 2개(수동 지도), 부문 간 거래 제거는 SEG_ADJ. 원문 대조: Q3 2026 17,585/2,967/−366(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"dal:AirlineMember": ["항공", "#003366"], "dal:RefineryMember": ["정유", "#c8102e"]},
 "ignore": []
}
