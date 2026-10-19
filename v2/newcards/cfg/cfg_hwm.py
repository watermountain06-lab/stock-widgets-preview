# HWM(하우멧 에어로스페이스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 130(시총 128위). 항공기 엔진 부품·체결재·구조물, 트럭 단조 휠.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-06), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장중 접수), 8-K(CFO 교체 2025-10-20, 우선주 상환 2025-11-17,
# CAM 인수 계약 2025-12-22·완료 2026-04-06, 선순위채 2025-11·2026-02), StockAnalysis.
# 2020-04 Arconic 분리 뒤 이름 변경(옛 Arconic Inc.) — 자기 이력 창(2021-10~)은 분리 뒤라 일반 경로.
# 엔진 입력(2026-10-19): 차입금 $4,501M(1년 안 $1 + 기업어음 $450 + 장기 $4,050) = 원문. 이자비용은 손익계산서 "Interest expense, net"(InterestIncomeExpenseNonoperatingNet)만 분기로
# 내 vendor/fetch_financials.CONCEPTS_BY_CIK(LOW·EMR 방식 — 없으면 이자보상배율 "미공시"). 우선주($55M)는 2025-12-17 상환, 비지배지분 없음(낡은 태그 값은 0).
# 4분기 EPS: 2024년만 보도자료 $0.77(역산 $0.76). Q1 2026 영업이익에 Savannah 단조 공장 매각 이익 $93M(10-Q 주석 E) — 뉴스에 적음.
# 2026년 상반기 CAM·Brunner 합산 인수 순현금 $1,929M은 현금흐름 순투자에 안 들어간다 — 인수 태그가 2025년에 없어 최근 4분기 합을 못 만든다(엔진, 안건 E31).
CIK = '0000004281'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Howmet Aerospace'
S_ = 'https://www.sec.gov/Archives/edgar/data/4281/'
SEC = S_
TENQ = S_ + '000000428126000025/hwm-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q1': S_ + '000110465926056645/tm2613779d1_ex99-1.htm', 'q4': S_ + '000110465926013832/tm266060d1_ex99-1.htm',
      'q3': S_ + '000110465925104005/tm2529740d1_ex99-1.htm'}
LINKS = {'cam_close': S_ + '000110465926039791/tm2611168d1_8k.htm', 'cam_deal': S_ + '000110465925123518/tm2534069d1_ex99-1.htm',
         'notes26': S_ + '000110465926016568/tm266060d2_8k.htm', 'pref': S_ + '000110465925112874/tm2531260d1_8k.htm',
         'cfo': S_ + '000110465925101524/tm2529267d1_8k.htm'}
FAIRBAND_TITLE = 'id="hwmFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 60)
ACT_REASON = ''
NONOP_WHAT = '장기투자'
# 고정 문장(숫자 없음 — 분기마다 고치지 않는다). 현금흐름 값이 작은 이유(Fable 필수 2026-10-19).
MODEL_NOTE = ('투하자본의 큰 몫이 과거 인수에서 생긴 영업권·무형자산이라 평균 매출/자본이 낮고, 이 모델은 매출을 늘릴 때마다 큰 재투자가 든다고 본다 — '
              '실제 잉여현금흐름보다 훨씬 작은 현금흐름을 가정한 값이라, 이 회사에서는 현재가와의 차이가 크게 나온다.')
PH = ['GE', 'RTX', 'TDG', 'GD', 'LMT', 'BA']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '항공·방산 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '항공·방산 PBR 비교', 'psr': '항공·방산 PSR 비교',
                'pcr': '항공·방산 PCR(FCF) 비교', 'evebitda': '항공·방산 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(HWM 제외)와 배수 순위를 매긴 값이다.',
            '기계·항공·운송·건설·업무 서비스 회사가 섞여 있다. 차트에는 항공·방산 6곳만 보인다.')
# 매출(Q2 2026 10-Q 주석 D 부문 표 — 외부 매출) — 엔진 부품 1,373 + 체결재 589 + 구조물 269 + 단조 휠 316 = 2,547(연결 매출). 부문 간 매출 11은 제외.
# 2026년 1분기 부문 재편(티타늄 합금 공장을 엔진 부품 → 구조물) — 10-Q의 1년 전 값(1,038/431/308/276)은 재편 기준. 체결재 +37%에 CAM 인수(4/6) 포함.
SEG = [('엔진 부품', 1373, '#003da5'), ('체결재(패스너)', 589, '#4f8fdc'), ('구조물(티타늄 등)', 269, '#8fb3dc'), ('단조 휠(트럭)', 316, '#6b7280')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 보고 부문별(외부 매출)'
# 손 뉴스: 최신 실적(Q2 2026, 8/6)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤(같은 날 포함) 손 항목은 없다. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K는 모두 10~12시 접수(장중) → 같은 날. CAM 완료 8-K 4/6 13:00 → 4/6, 선순위채 가격 결정 8-K 2/17 22:13 → 2/18(종결 8-K 3/3은 넣지 않음, Fable),
# CAM 계약 8-K 12/22 13:46 → 12/22, 우선주 8-K 11/17 11:04 → 11/17, CFO 8-K 10/22 20:06 → 10/23.
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('green', '2026년 5월 7일 — Q1 2026 실적', '2026-05-07',
     '매출 $2.31B(+19%) · 희석 EPS $1.44(1년 전 $0.84) · Savannah 단조 공장 매각 이익 $93M 포함(10-Q)', 'q1', 'Howmet 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 6일 — CAM 인수 완료', '2026-04-06',
     'Stanley Black & Decker의 항공 체결재 회사 Consolidated Aerospace Manufacturing을 현금 약 $1.8B에 인수(조정 전) · 2월 6일 Brunner(체결재, 약 $120M)도 인수 — Q2 체결재 외부 매출 +37%는 주로 두 인수와 상업·방산 항공 시장 성장, 구조물 −13%는 Savannah 공장 매각·제품 정리(10-Q)', 'cam_close', 'Howmet 공시 (SEC 8-K)'),
    ('neutral', '2026년 2월 17일 장 마감 뒤 — 선순위채 $1.2B 가격 결정', '2026-02-18',
     '2028년 만기 $400M(연 3.750%) · 2029년 $300M(3.900%) · 2036년 $500M(4.750%) · CAM 인수 자금(기업어음 등 $600M과 함께) · 3월 3일 발행 종결', 'notes26', 'Howmet 공시 (SEC 8-K)'),
    ('green', '2026년 2월 12일 — Q4 2025 실적', '2026-02-12',
     '매출 $2.17B(+15%) · 희석 EPS $0.92(1년 전 $0.77) · 2025년 매출 $8.25B·EPS $3.71', 'q4', 'Howmet 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 22일 — CAM 인수 계약', '2025-12-22',
     '항공·방산 체결재·유체 피팅 회사 · 전액 현금 약 $1.8B · 회사 전망 CAM 2026년 매출 약 $485~495M', 'cam_deal', 'Howmet 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 17일 — 우선주 전량 상환 발표', '2025-11-17',
     '$3.75 누적 우선주 546,024주를 12월 17일 주당 $100 + 미지급 배당 $0.8125에 상환', 'pref', 'Howmet 공시 (SEC 8-K)'),
    ('green', '2025년 10월 30일 — Q3 2025 실적', '2025-10-30',
     '매출 $2.09B(+14%) · 희석 EPS $0.95(1년 전 $0.81)', 'q3', 'Howmet 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 22일 장 마감 뒤 — CFO 교체 발표', '2025-10-23',
     'Ken Giacobbe CFO가 10월 20일 은퇴 결정, 12월 말 은퇴 · Hexcel CFO Patrick Winterlich가 12월 1일부터 CFO', 'cfo', 'Howmet 공시 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Strong Buy', 'n': 22, 'nt': 17, 'mean': 323.41, 'median': 335, 'low': 255, 'high': 375, 'sb': 15, 'b': 4, 'h': 3, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-19'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(보고 부문 축 4개, 외부 매출). 원문 대조: Q2 2026 1,373/589/269/316(합 2,547 = 연결), 1년 전 1,038/431/308/276(재편 기준, 2026-10-19) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "hwm:EngineProductsSegmentMember": [
   "엔진 부품",
   "#003da5"
  ],
  "hwm:FasteningSystemsMember": [
   "체결재(패스너)",
   "#4f8fdc"
  ],
  "hwm:EngineeredStructuresMember": [
   "구조물(티타늄 등)",
   "#8fb3dc"
  ],
  "hwm:ForgedWheelsMember": [
   "단조 휠(트럭)",
   "#6b7280"
  ]
 },
 "ignore": []
}
