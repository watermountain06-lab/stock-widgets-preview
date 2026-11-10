# DHI(D.R. 호튼) v2 카드 설정 — 자동 카드(AUTO). 회계연도 9월 30일. 카드 순위 200(시총 275위). 미국 최대 주택 건설사 — 단독주택·임대 주택, 택지 개발(Forestar 62%), 주택 금융.
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-07-21), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 장 전 발표, 8:30 콜, 8-K 장중 접수), 8-K(자사주 $5B 추가 승인 9/15), StockAnalysis. 사전 조사 자료표 scratchpad pre/DHI.md.
# 엔진 입력(2026-10-24): 영업이익 = 세전이익(DERIVED_OPINC — 영업이익 줄 없음, 이자는 대부분 자본화돼 매출원가), 차입금 = 재무상태표 한 줄 NotesPayable $7,112.6M(DEBT_TOTAL_TAG — 주택 금융 모기지 환매 약정 $1.8B 포함),
# 비지배지분 $587M(Forestar 38%), 4분기 EPS FY2021~2025 보도자료 값. FY2026 4분기 실적은 10/29 장 전 — 파이프라인이 새 10-K로 자동 갱신.
CIK = '0000882184'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-09-30', '2024-09-30'), 'FY2025'
VOTES, VERDICT = (-1, 1, -1), '적정~고평가'
CO = 'D.R. Horton'
S_ = 'https://www.sec.gov/Archives/edgar/data/882184/'
SEC = S_
TENQ = S_ + '000088218426000096/dhi-20260630.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000088218426000092/a6302026exhibit991.htm', 'q2': S_ + '000088218426000062/a3312026exhibit991.htm',
      'q1': S_ + '000088218426000007/a12312025exhibit991.htm', 'q4': S_ + '000088218425000044/a9302025exhibit991.htm'}
LINKS = {'bb': S_ + '000088218426000108/dhi-20260915.htm'}
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-29', 'src': 'Q3 FY26 실적 보도자료(8-K) — 10/29 장 시작 전 발표'}
FAIRBAND_TITLE = 'id="dhiFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 25)
ACT_REASON = '주택 건설사라 재고(택지·건설 중 주택)가 커서 일반 제조업 기준 회전 지표는 길게 나온다'
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('2021~2022년 주택 경기 정점 뒤 금리 상승으로 판매 단가 할인이 커져 이익률이 내려오는 중이다 — 5년 이력 앞부분의 높은 이익이 과거 배수를 낮춰 지금이 상대적으로 비싸 보이게 한다. 현금흐름 시나리오는 이익률이 순서를 정해, 과거 고마진으로 회복을 가정한 보수 쪽이 가장 높다. '
              '손익계산서에 영업이익 줄이 없어 세전이익을 영업이익으로 쓴다 — 이자비용은 대부분 자본화돼 매출원가로 나가고, 임대·모기지 이자수익도 반복 영업 수익이다. 차입금에는 주택 금융 자회사의 모기지 환매 약정이 들어 있는데 담보인 판매 대기 모기지 대출은 따로 더하지 않아 내재가치가 조금 보수적이다. '
              'Forestar는 62%만 가진 상장 자회사라 나머지 38%를 비지배지분으로 뺀다. 자사주를 크게 사들인다.')
HEALTH_EXTRA = '재무상태표가 유동·비유동을 나누지 않는 주택 건설사 형식이라 유동·당좌비율을 계산하지 않는다. 재고(택지·건설 중 주택)가 자산의 대부분이다.'   # 고정 문장(Fable r1 2026-10-24)
PH = ['LEN', 'PHM', 'NVR', 'HD', 'LOW']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '주택 건설·주거 5곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(DHI 제외)와 배수 순위를 매긴 값이다.',
            '유통·자동차·외식·여행·주택 건설이 섞여 있다. 차트에는 주택 건설·주거 관련 5곳만 보인다.')
# 매출(Q3 FY26 10-Q 부문) — 주택 건설 8,686.2 + Forestar 407.0 + 임대 266.1 + 금융 220.7 = 9,580.0, 부문 간 거래·기타 −352.9 → 9,227.1.
SEG = [('주택 건설', 8686.2, '#0a3161'), ('Forestar(택지)', 407.0, '#4a7ab8'), ('임대 주택', 266.1, '#05203f'), ('주택 금융', 220.7, '#9db6d6')]
SEG_ADJ = -352.9
SEG_ADJ_LABEL = '부문 간 거래 제거'
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 회사는 조정 EPS를 내지 않는다) + 자사주 승인. 반응일: 보도자료 장 전(8:30 콜), 8-K 장중 접수 → 같은 날. 자사주 8-K 9/15 21:09Z(장 마감 뒤) → 9/16.
# 넣지 않은 8-K: 신용 한도(3/31·5/12), 주총(1/16). SK Builders 인수(약 $80M, 2025-10, 8-K 없음)는 작다.
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 15일 — 자사주 $5.0B 추가 승인', '2026-09-16',
     'FY2026 자사주 매입 예상을 $3.25B 이상으로 올림(8-K 장 마감 뒤)', 'bb', 'D.R. Horton 공시 (SEC 8-K)'),
    ('neutral', '2026년 7월 21일 — Q3 FY26 실적', '2026-07-21',
     '매출 $9.23B(1년 전 $9.23B) · 순이익 $905M · 희석 EPS $3.20(1년 전 $3.36)', 'q3', 'D.R. Horton 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 21일 — Q2 FY26 실적', '2026-04-21',
     '매출 $7.56B · 순이익 $648M · 희석 EPS $2.24(1년 전 $2.58)', 'q2', 'D.R. Horton 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 20일 — Q1 FY26 실적', '2026-01-20',
     '매출 $6.89B · 순이익 $595M · 희석 EPS $2.03(1년 전 $2.61)', 'q1', 'D.R. Horton 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 28일 — Q4 FY25 실적', '2025-10-28',
     '매출 $9.68B · 순이익 $905M · 희석 EPS $3.04(1년 전 $3.92) · 2025 회계연도 희석 EPS $11.57', 'q4', 'D.R. Horton 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 21, 'nt': 13, 'mean': 146.92, 'median': 147, 'low': 114, 'high': 186, 'sb': 4, 'b': 0, 'h': 14, 's': 2, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 4개(수동 지도, Revenues), 부문 간 거래는 SEG_ADJ. 원문 대조: Q3 FY26 8,686.2/407.0/266.1/220.7/−352.9(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"dhi:HomeBuildingOpsMember": ["주택 건설", "#0a3161"], "dhi:ForestarGroupMember": ["Forestar(택지)", "#4a7ab8"],
             "dhi:RentalMember": ["임대 주택", "#05203f"], "dhi:FinancialServicesMember": ["주택 금융", "#9db6d6"]},
 "ignore": ["dhi:EliminationsAndOtherMember"]
}
