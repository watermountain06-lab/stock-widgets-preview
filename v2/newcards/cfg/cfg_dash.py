# DASH(도어대시) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 159(시총 157위). 음식·생활용품 배달 플랫폼(DoorDash, 2022년 인수한 Wolt, 2025-10 인수한 Deliveroo).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05 장 뒤 접수), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 마감 뒤 접수), 8-K(Deliveroo 인수 완료 2025-10-02, 네바다 이전 9/18), StockAnalysis.
# 엔진 입력(2026-10-22): 다중 클래스(A·B) → 주식 수는 표지 값(BUILD cover_shares, 433.3M). 차입금 = Deliveroo 인수 자금 전환사채 $2,727M(DEBT_TOTAL_TAG — 기본 태그는 2021년에 멈춰 0이었다).
# 현금 $4,424M · 단기투자 $923M · 장기투자 $869M = 원문. 인수 대금 최근 4분기 $3,008M(Deliveroo). 이자비용 분기 태그 없음(이자보상배율 빠짐). 4분기 EPS 2024·2025 보도자료 값.
# 전환사채: 0% 2030년 만기, 원금 $2,750M, 전환가 $291.97(현재가의 약 1.6배 — 희석은 반영 안 함, 캡드콜 헤지 있음). 이자율 0%라 이자비용이 거의 없다(Fable r1).
BUILD = {'cover_shares': True}
CIK = '0001792789'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'DoorDash'
S_ = 'https://www.sec.gov/Archives/edgar/data/1792789/'
SEC = S_
TENQ = S_ + '000179278926000050/dash-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000179278926000048/proddashex991-pressrelease.htm', 'q1': S_ + '000179278926000036/proddashex991-pressrelease.htm',
      'q4': S_ + '000179278926000012/prodq4dashex991-pressrelea.htm', 'q3': S_ + '000179278925000018/proddashex991-pressrelease.htm'}
LINKS = {'roo': 'https://www.sec.gov/Archives/edgar/data/1792789/000114036125037039/ef20056500_ex99-1.htm', 'nv': 'https://www.sec.gov/Archives/edgar/data/1792789/000114036126037109/ef20081998_8k.htm'}
FAIRBAND_TITLE = 'id="dashFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-10, 20)
ACT_REASON = ''
NONOP_WHAT = '장기 투자·지분'
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-11-04', 'src': '10/9 회사 공지 — 장 마감 뒤 발표, 콜 오후 4시 30분(동부)'}   # Codex r1 필수
# 고정 문장(숫자 없음). 주식보상, 인수 효과, 낮은 GAAP 이익률.
MODEL_NOTE = ('GAAP 영업이익률이 주식보상비용과 인수 무형자산 상각 때문에 낮아, 최근 이익률에서 출발하는 이 모델은 빠른 매출 성장에도 가치를 작게 계산한다. '
              '최근 매출 증가율에는 Deliveroo 인수 효과가 크게 들어 있고, 최근 4분기 인수 지출(Deliveroo)이 재투자 계산에 들어가 있다. 카드의 FCF는 자본화한 소프트웨어 개발비를 빼지 않아 회사가 발표하는 FCF보다 크다.')   # Codex r1 필수(DDOG와 같은 표기)
PH = ['ABNB', 'BKNG', 'AMZN', 'EXPE', 'CMG', 'MCD']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '플랫폼·소비 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(DASH 제외)와 배수 순위를 매긴 값이다.',
            '자동차·소매·외식·여행이 섞여 있다. 차트에는 플랫폼·소비 6곳만 보인다.')
# 매출(Q2 2026 10-Q 지역별) — 미국 3,457 + 해외 997 = 4,454. 1년 전 2,829/455 → 3,284. 단일 부문.
SEG = [('미국', 3457.0, '#eb1700'), ('해외(Wolt·Deliveroo 등)', 997.0, '#f5674f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역별(단일 부문)'
# 손 뉴스: 최신 실적(Q2 2026, 8/5)도 손으로 — 9/18 네바다 이전 손 항목보다 앞선 자동 항목은 빠지므로. 가이던스·조정 EBITDA는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K 2025-11-06T02:09Z·2026-02-19T02:08Z·05-07T00:10Z·08-06T00:12Z = 장 마감 뒤 → 다음 날.
# 네바다 이전 8-K 2026-09-19T00:05Z = 9/18 20:05(장 뒤, 효력 9/18) → 9/21. 넣지 않은 8-K: 이사 선임(1/20), 주총(6/12·8/11).
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 18일 — 델라웨어에서 네바다로 법인 이전', '2026-09-21',
     '8월 6일 과반 주주의 서면 동의로 승인, 9월 18일 네바다 법인으로 전환(8-K는 그날 장 마감 뒤)', 'nv', 'DoorDash 공시 (SEC 8-K)'),
    ('green', '2026년 8월 5일 장 마감 뒤 — Q2 2026 실적', '2026-08-06',
     '매출 $4.45B(+36%) · 주문 9.7억 건(+27%) · 희석 EPS $0.46(1년 전 $0.65)', 'q2', 'DoorDash 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 6일 장 마감 뒤 — Q1 2026 실적', '2026-05-07',
     '매출 $4.04B(+33%) · 주문 9.3억 건(+27%) · 희석 EPS $0.42(1년 전 $0.44)', 'q1', 'DoorDash 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 18일 장 마감 뒤 — Q4 2025 실적', '2026-02-19',
     '매출 $3.96B(+38%, Deliveroo 첫 완전 분기) · 주문 9.0억 건(+32%) · 희석 EPS $0.48(1년 전 $0.33) · 2025년 EPS $2.13', 'q4', 'DoorDash 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 5일 장 마감 뒤 — Q3 2025 실적 · 2026년 투자 확대 계획', '2025-11-06',
     '매출 $3.45B(+27%) · 주문 7.8억 건(+21%) · 희석 EPS $0.55(1년 전 $0.38) · 2026년 신규 사업·플랫폼 투자를 2025년보다 수억 달러 늘릴 계획', 'q3', 'DoorDash 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 2일 — Deliveroo 인수 완료', '2025-10-02',
     '영국 배달 회사 Deliveroo 인수를 마쳤다(현금 지출 약 $2.95B, 취득 현금 차감 — 10-Q 현금흐름표) · 4분기부터 실적에 반영', 'roo', 'DoorDash 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 45, 'nt': 32, 'mean': 253.59, 'median': 260, 'low': 185, 'high': 350, 'sb': 27, 'b': 9, 'h': 9, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 손으로(지역 축: 미국 country:US + 해외 NonUs). 원문 대조: Q2 2026 3,457/997, 1년 전 2,829/455(2026-10-22) ──
AUTO = True
SEG_MAP = {"concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], "axis": "srt:StatementGeographicalAxis", "extra": {},
           "members": {"country:US": ["미국", "#eb1700"], "us-gaap:NonUsMember": ["해외(Wolt·Deliveroo 등)", "#f5674f"]}, "ignore": []}
