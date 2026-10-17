# EQIX(이퀴닉스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 118(시총 115위). 데이터센터 리츠.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-29), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 마감 뒤 접수), 8-K(CFO 승계 2025-12-03·선임 2026-03-10,
# atNorth 공동 인수 2026-02-27, 신용 약정 2026-07-27), StockAnalysis.
# 엔진 입력(2026-10-17): 설비투자는 2026년 2분기 누계부터 PaymentsToAcquireOtherPropertyPlantAndEquipment로만 내 EXTRA_TAGS(겹치는 기간 값 같음 — 부동산 취득은 뺌).
# 차입금 = 선순위채·대출 원금(LongTermDebt) + 금융리스(DEBT_TOTAL_TAG — 금융리스 $2,280M이 빠졌었다). 우선주 태그 2022년 멈춤 → preferred = [].
# 4분기 EPS 보도자료 값(2025 $2.69·2024 −$0.14·2022 $1.39·2021 $1.36). 리츠라 일반 기업 모델(GAAP EPS·FCF·DCF)을 그대로 쓴다 — FFO·AFFO는 쓰지 않는다(PLD·WELL 선례).
# 설비투자가 영업현금흐름보다 커 FCF 음수(PCR 0점), 투하자본이익률 약 4%가 할인율보다 낮아 현금흐름 내재가치 음수.
# Q2 2026 매출에 합작사(xScale) 대상 비반복 서비스 매출의 전년 대비 증가분 $124M(10-Q MD&A 'incremental' — 총액 아님, 판정 계산 규칙이라 손대지 않음).
CIK = '0001101239'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Equinix'
S_ = 'https://www.sec.gov/Archives/edgar/data/1101239/'
SEC = S_
TENQ = S_ + '000110123926000147/eqix-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000110123926000145/a991eqix-q226xpr.htm', 'q1': S_ + '000110123926000089/eqix-q126xpr.htm',
      'q4': S_ + '000110123926000030/february112026pressrelease-.htm', 'q3': S_ + '000110123925000061/october292025pressrelease-.htm'}
LINKS = {'cfo': S_ + '000110123926000058/cfoappointment_031026xfinal.htm', 'atnorth': S_ + '000110123926000051/a2026-geminipressreleasexf.htm',
         'cfoplan': S_ + '000110123925000083/a25-12x03pressrelease.htm',
         'sec': S_ + '000110123925000074/eqix-20251119.htm',
         'notes': 'https://www.sec.gov/Archives/edgar/data/1101239/000110465926092009/tm2622384d1_8k.htm'}
FAIRBAND_TITLE = 'id="eqixFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 30)
ACT_REASON = ''
MODEL_NOTE = '리츠에 일반 기업용 모델을 그대로 쓴 참고 값이다 — 실적 FCF는 유지·확장 설비투자를 함께 뺀 값(부동산 취득 제외, Q2 설비투자 $1.58B 중 회사가 유지 투자로 분류한 것은 $49M)이고, 현금흐름 내재가치는 영업이익·재투자 모델이라 리츠의 FFO·AFFO 기반 평가가 아니다.'
NONOP_WHAT = '지분법 투자'
PH = ['DLR', 'AMT', 'PLD', 'CCI', 'WELL', 'PSA']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(EQIX 제외)과 배수 순위를 매긴 값이다.',
            '데이터센터·통신탑·물류·헬스케어·리테일·주거 리츠가 섞여 있다. 리츠는 감가상각이 커 GAAP PER이 높게 나온다. 차트에는 데이터센터·통신탑·물류 등 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문 주석) — 미주 1,251 + EMEA 845 + 아시아·태평양 529 = 2,625(연결 매출). 미주 비반복 매출 184(1년 전 53)에 일회성 xScale 수수료.
SEG = [('미주', 1251, '#e4002b'), ('EMEA', 845, '#a8001f'), ('아시아·태평양', 529, '#f0667f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역 부문별'
# 손 뉴스: Q2 2026 실적(7/29)은 일회성 xScale 수수료를 함께 적으려고 손으로 쓴다(README). 가이던스는 쓰지 않는다.
# 반응일: 실적 8-K는 모두 동부 16시 11~20분 접수(장 마감 뒤) → 다음 거래일. atNorth 8-K 2/27 08:34 → 2/27. CFO 선임 8-K 3/10 09:04 → 3/10.
# CFO 승계 계획 8-K 12/3 16:38 접수(보도 시각 미표기) → 12/4. 채권 발행 8-K 8/6 16:12 → 8/7. SEC 조사 종결 8-K 11/20 08:57 → 11/20.
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('red', '2026년 8월 6일 장 마감 뒤 — 선순위채 $3.0B 발행 공시', '2026-08-07',
     '2029·2031·2033·2036년 만기 4종(연 5.0~5.8%) · 카드의 차입금(6/30 기준 $22.2B)에는 아직 들어 있지 않다', 'notes', 'Equinix 공시 (SEC 8-K)'),
    ('green', '2026년 7월 29일 장 마감 뒤 — Q2 2026 실적', '2026-07-30',
     '매출 $2.63B(+16.4% — 10-Q 기준 합작사 대상 비반복 서비스 매출이 1년 전보다 $124M 늘어난 것 포함) · 희석 EPS $4.83(1년 전 $3.75)', 'q2', 'Equinix 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 29일 장 마감 뒤 — Q1 2026 실적', '2026-04-30',
     '매출 $2.44B(+9.8%) · 희석 EPS $4.20(1년 전 $3.50)', 'q1', 'Equinix 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 3월 10일 — 새 CFO 선임', '2026-03-10',
     'Olivier Leonetti 3월 16일부터 CFO · Keith Taylor 은퇴', 'cfo', 'Equinix 공시 (SEC 8-K)'),
    ('green', '2026년 2월 27일 — atNorth 공동 인수 계약', '2026-02-27',
     '북유럽 데이터센터 atNorth, 기업가치 $4B · CPP Investments 약 60%·Equinix 약 40% · 규제 승인 등 조건', 'atnorth', 'Equinix 공시 (SEC 8-K)'),
    ('green', '2026년 2월 11일 장 마감 뒤 — Q4 2025 실적', '2026-02-12',
     '매출 $2.42B(+7.0%) · 희석 EPS $2.69(1년 전 −$0.14) · 2025년 EPS $13.76 · 분기 배당 $5.16(+10%)', 'q4', 'Equinix 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 12월 3일 — CFO 은퇴 계획 발표', '2025-12-04',
     'Keith Taylor CFO 2026년 은퇴 · 후임 선임까지 CFO 유지', 'cfoplan', 'Equinix 공시 (SEC 8-K)'),
    ('neutral', '2025년 11월 20일 — SEC 조사 종결 공시', '2025-11-20',
     '2024년 공매도 보고서 관련 SEC 조사 종결(11/19 통지) — 제재 권고 안 함 · 캘리포니아 북부 연방검찰도 추가 조치 예상 없음', 'sec', 'Equinix 공시 (SEC 8-K)'),
    ('green', '2025년 10월 29일 장 마감 뒤 — Q3 2025 실적', '2025-10-30',
     '매출 $2.32B(+5.2%) · 희석 EPS $3.81(1년 전 $3.10)', 'q3', 'Equinix 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 34, 'nt': 27, 'mean': 1241.81, 'median': 1250, 'low': 1015, 'high': 1400, 'sb': 23, 'b': 5, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-17'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-Q 부문 주석 Q2 2026 1,251/845/529, 1년 전 1,004/767/485 = 연결 매출(2026-10-17) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "eqix:AmericasSegmentMember": [
   "미주",
   "#e4002b"
  ],
  "eqix:EMEASegmentMember": [
   "EMEA",
   "#a8001f"
  ],
  "eqix:AsiaPacificSegmentMember": [
   "아시아·태평양",
   "#f0667f"
  ]
 },
 "ignore": []
}
