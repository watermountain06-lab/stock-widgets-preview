# RCL(로열 캐리비안) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 158(시총 156위). 크루즈 여행(Royal Caribbean International·Celebrity·Silversea).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-28 장 뒤 접수), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 동부 오전 접수, 보도자료는 장 전), 8-K(Perfect Day Mexico 5/20, Sandals 합작 9/23, 사채·대출), StockAnalysis.
# 엔진 입력(2026-10-22): 차입금 $22,836M = 1년 안 1,573 + 장기 21,263(DEBT_TOTAL_TAG — 1년 안 만기가 빠져 $21,263M이었다; 금융리스 포함 태그).
# 세율 2%(build_dcf STATUTORY_TAX — 라이베리아 법인, 국제 해운 소득은 미국 세법 883조로 면세, Q2 2026 세전 $1,150M에 세금 $14M; 세금 태그가 듬성해 21%로 떨어졌다).
# 현금 $875M · 운용리스 $682M · 비지배 $225M = 원문. 선박 투자(설비투자 $7.2B/년)가 커 최근 4분기 FCF가 작다. 2020~2022 코로나 기간이 5년 이력에 남아 성장률 기저 효과(growth_base_effect).
# 4분기 EPS 2021~2024 보도자료 값(전환사채 희석 주식 수 차이로 역산과 다르다).
BUILD = {}
CIK = '0000884887'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'Royal Caribbean'
S_ = 'https://www.sec.gov/Archives/edgar/data/884887/'
SEC = S_
TENQ = S_ + '000088488726000038/rcl-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000088488726000036/a2026q2earningsrelease.htm', 'q1': S_ + '000088488726000024/a2026q1earningsrelease.htm',
      'q4': S_ + '000088488726000003/a10k2025earningsrelease8-k.htm', 'q3': S_ + '000088488725000146/a2025q3earningsrelease8-k.htm'}
LINKS = {'mexico': S_ + '000110465926064412/tm2615230d1_8k.htm', 'sandals': S_ + '000110465926109755/tm2625963d1_ex99-1.htm'}
FAIRBAND_TITLE = 'id="rclFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-20, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
CHECK_DEBT = {'2026-06-30': 'Sandals 지분 인수(약 $3B, 전액 차입 조달, 2027년 초 완료 예정) 뒤 차입금(분기 말 {debt})이 어디서 멈추는지'}   # Fable r1 필수
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-27', 'src': '10/8 회사 공지 — 콜 오전 10시(동부)'}   # Codex r1
# 고정 문장(숫자 없음). 코로나 기저, 선박 투자, 세금.
MODEL_NOTE = ('5년 이력에 코로나로 운항을 멈춘 기간이 들어 있어 이익률과 배수 이력이 크게 흔들린다(성장률은 기저 효과 때문에 3년 기준). 새 선박 투자가 커서 최근 분기 현금흐름(FCF)이 음수로 내려갈 수 있고, '
              '국제 해운 소득이 대부분 면세라 세율은 실효 수준에 맞춘 가정(낮은 한 자릿수)을 썼다.')   # Codex r1 권장
PH = ['CCL', 'NCLH', 'BKNG', 'MAR', 'HLT', 'EXPE']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '여행·숙박 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(RCL 제외)와 배수 순위를 매긴 값이다.',
            '자동차·온라인·소매·외식이 섞여 있다. 차트에는 크루즈·여행·숙박 6곳만 보인다.')
# 매출(Q2 2026 10-Q) — 승선권 3,344 + 선상·기타 1,488 = 4,832. 1년 전 3,199/1,339 → 4,538. 단일 부문.
SEG = [('승선권(Passenger ticket)', 3344.0, '#0a2a5e'), ('선상·기타(Onboard and other)', 1488.0, '#3a6bb3')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 수입 종류별(단일 부문)'
# 손 뉴스: 최신 실적(Q2 2026, 7/28)은 news_auto — 그 뒤 손 항목(9/23 Sandals)이 있어 자동 항목이 빠지므로 Q2도 손으로.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K 2025-10-28T14:34Z·2026-01-29T16:32Z·04-30T14:31Z·07-28T14:32Z = 장중 접수(보도자료 장 전) → 같은 날.
# Perfect Day Mexico: 장관 발언 5/19(8-K 본문) → 반응일 5/19(Fable r1 필수 — 회사 대응 8-K는 5/20 장 뒤). Sandals: 9/22 언론 선보도 −6.1%, 8-K는 9/23. Sandals 8-K 2026-09-23T14:01Z(보도자료 그날 아침) → 9/23.
# 넣지 않은 8-K: 사채·대출(2025-10-01, 2026-02-13·02-27·08-07·08-20), 이사 선임(2/17·7/20), 주총(5/28).
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 23일 — Sandals 리조트 합작', '2026-09-23',
     'Sandals·Beaches 리조트 지분 50%를 약 $3B(선행 EBITDA 약 10배)에 인수하기로 계약 — 전액 차입으로 조달, 2027년 초 완료 예정(이 카드의 차입금·내재가치는 거래 전 기준) · 전날 보도 뒤 9/22 −6.1%', 'sandals', 'Royal Caribbean 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 28일 — Q2 2026 실적', '2026-07-28',
     '매출 $4.83B(+6.5%) · 희석 EPS $4.20(1년 전 $4.41) · 연간 조정 EPS 전망 상향', 'q2', 'Royal Caribbean 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 19일 — Perfect Day Mexico 인허가 거부 발언', '2026-05-19',
     '멕시코 환경부 장관이 첫 환경 인허가 신청을 거부하겠다고 밝혔다 — 회사는 5월 20일 장 뒤 자료를 더 내겠다고 대응 공시(8-K)', 'mexico', 'Royal Caribbean 공시 (SEC 8-K)'),
    ('green', '2026년 4월 30일 — Q1 2026 실적', '2026-04-30',
     '매출 $4.45B(+11.3%) · 희석 EPS $3.48(1년 전 $2.70) · 3월·4월 초 지정학 영향으로 지중해 예약 둔화 뒤 회복 · 연간 조정 EPS 전망 하향', 'q1', 'Royal Caribbean 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 29일 — Q4 2025 실적', '2026-01-29',
     '매출 $4.26B(+13.3%) · 희석 EPS $2.76(1년 전 $2.02) · 2025년 EPS $15.61', 'q4', 'Royal Caribbean 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 28일 — Q3 2025 실적', '2025-10-28',
     '매출 $5.14B(+5.2%) · 희석 EPS $5.74(1년 전 $4.21)', 'q3', 'Royal Caribbean 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 29, 'nt': 21, 'mean': 350.48, 'median': 355, 'low': 298, 'high': 425, 'sb': 19, 'b': 4, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 손으로(수입 종류 축, 항구 비용 세부는 ignore). 원문 대조: Q2 2026 3,344/1,488, 1년 전 3,199/1,339(2026-10-22) ──
AUTO = True
SEG_MAP = {"concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], "axis": "srt:ProductOrServiceAxis", "extra": {},
           "members": {"us-gaap:PassengerMember": ["승선권(Passenger ticket)", "#0a2a5e"], "us-gaap:ProductAndServiceOtherMember": ["선상·기타(Onboard and other)", "#3a6bb3"]},
           "ignore": ["rcl:PortCostsMember", "rcl:CruiseItineraryMember", "rcl:OtherProductsAndServicesMember"]}
