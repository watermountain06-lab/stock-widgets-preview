BUILD = {}
# PHM(펄트그룹) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 주택 건설(펄트·센텍스·델웹·디바인)과 모기지 금융(Pulte Mortgage).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-22), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 07시 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/PHM.md.
# 엔진 입력(2026-11-03): 영업이익 태그 없음 → DERIVED_OPINC(세전 Domestic 태그 − 이자수익 − 기타 영업외 − 지분법, TTM $2,273.8M), 세전 태그 PRETAX_TAG_BY_CIK. 차입금 = 주택건설 NotesPayable $1,808.9M(DEBT_TOTAL_TAG).
# 모기지 자회사 환매 차입 $383.2M은 매각 예정 대출($433.9M)로 담보된 운전자본성이라 제외 — 금융 부문 이익은 영업이익에 들어 있다. 운용리스 $123.2M, 우선주 없음(EV_TAGS_BY_CIK). Q4 2021~2024 EPS는 보도자료 값.
# 일회성: Q4 2025 제조 자산 매각 비용 $81M + 토지 손상 $35M − 보험 환입 $34M(세전 순 $82M, EPS 3.4%). 되돌려도 현금흐름 비율 0.957 → 0.937(0표 그대로, scratchpad phm_e54).
# 처음 DERIVED_OPINC 부호를 반대로 넣어 영업외 이익이 더해졌고(비율 0.912), 그 값으로 미완성 판정을 냈다가 Codex·Fable r1 지적으로 고쳤다.
CIK = '0000822416'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 1, 0), '적정'
CO = 'PulteGroup'
S_ = 'https://www.sec.gov/Archives/edgar/data/822416/'
SEC = S_
TENQ = S_ + '000082241626000043/phm-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000082241626000041/ex991earningspr9302026.htm', 'q2': S_ + '000082241626000034/ex991earningspr06302026.htm', 'q1': S_ + '000082241626000021/ex991earningspr3312026.htm', 'q4': S_ + '000082241626000003/ex-991xearningsrelease4q20.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="phmFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('2025년 4분기 이익에 제조 자산 매각 비용·토지 손상(보험 환입 차감, 세전 순 $82M)이 들어 있다. 되돌려도 판정은 같다. '
              '이자 대부분이 재고(토지·주택)에 자본화돼 손익계산서 이자비용이 거의 0이다. 모기지 자회사 차입($0.4B)은 대출 자산으로 담보돼 차입금에 넣지 않는다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['DHI', 'LEN', 'NVR', 'HD', 'LOW', 'TSCO']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '주택 건설·주택 소매 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(PHM 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 주택 건설·주택 소매 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 — 주택건설 지역 7개는 SubsegmentsAxis, 금융은 부문 축) — 1,102.8 + 794.2 + 681.5 + 664.4 + 361.6 + 254.6 + 7.8 + 107.0 = 3,973.8.
SEG = [('플로리다', 1102.8, '#00447c'), ('웨스트', 794.2, '#7ab800'), ('사우스이스트', 681.5, '#3d7cc9'), ('미드웨스트', 664.4, '#a3c96b'), ('텍사스', 361.6, '#8a8d8f'), ('노스이스트', 254.6, '#b9c4d0'), ('금융 서비스', 107.0, '#d9a441'), ('기타 주택건설(토지 매각)', 7.8, '#d6d8da')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역·부문별(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07시 동부) → 같은 날.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 22일 장 전 — Q3 2026 실적', '2026-10-22',
     '매출 $3.97B(−9.8%) · 순이익 $476M · 희석 EPS $2.53(1년 전 $2.96) · 토지 손상 $26M 포함 — 당일 주가 +5.8%', 'q3', 'PulteGroup 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 22일 장 전 — Q2 2026 실적', '2026-07-22',
     '매출 $3.98B(−9.6%) · 순이익 $472M · 희석 EPS $2.48(1년 전 $3.03) — 당일 주가 +2.0%', 'q2', 'PulteGroup 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 23일 장 전 — Q1 2026 실적', '2026-04-23',
     '매출 $3.41B(−12.4%) · 순이익 $347M · 희석 EPS $1.79(1년 전 $2.57) · 자사주 $1.5B 추가 승인 — 당일 주가 +2.4%', 'q1', 'PulteGroup 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 29일 장 전 — Q4 2025 실적', '2026-01-29',
     '매출 $4.61B(−6.3%) · 순이익 $502M · 희석 EPS $2.56(1년 전 $4.43, 보험 환입 포함) · 제조 자산 매각 비용 주당 $0.31 포함 — 당일 주가 +3.2%', 'q4', 'PulteGroup 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 1, 'nt': 1, 'mean': 0, 'median': 0, 'low': 0, 'high': 0, 'sb': 0, 'b': 0, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-03'


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 지역 7개 + 금융 107.0(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "parts": [
  {"concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], "axis": "us-gaap:SubsegmentsAxis", "extra": {"us-gaap:StatementBusinessSegmentsAxis": "phm:HomeBuildingSegmentMember", "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
   "members": {"stpr:FL": ["플로리다", "#00447c"], "phm:WestMemberMember": ["웨스트", "#7ab800"], "phm:SoutheastMember": ["사우스이스트", "#3d7cc9"], "phm:MidwestMemberMember": ["미드웨스트", "#a3c96b"], "stpr:TX": ["텍사스", "#8a8d8f"], "phm:NortheastMember": ["노스이스트", "#b9c4d0"], "phm:OtherHomebuildingMember": ["기타 주택건설(토지 매각)", "#d6d8da"]},
   "ignore": []},
  {"concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], "axis": "us-gaap:StatementBusinessSegmentsAxis", "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
   "members": {"phm:FinancialServicesMember": ["금융 서비스", "#d9a441"]},
   "ignore": ["phm:HomeBuildingSegmentMember"]}
 ]
}
