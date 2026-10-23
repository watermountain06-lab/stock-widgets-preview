# OKE(원오케이) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 174. 미드스트림 — 천연가스 수집·처리, NGL, 천연가스 파이프라인, 정제유·원유.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-04 장 마감 뒤 접수), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 마감 뒤), 8-K(Brazos 인수·Apollo 지분 투자 8/30, 지배 구조 재편·채권 공개매수 9/15), StockAnalysis.
# 엔진 입력(2026-10-23): 차입금 = 1년 안 750 + 단기 1,499 + 장기 30,773 = $33,022M(엔진 값 = 원문), 비지배지분 = 100 + 상환 가능 44(EV_TAGS_BY_CIK), 이자비용 InterestExpenseNonoperating(CONCEPTS_BY_CIK).
# 8/30 합의: Brazos 퍼미안 자산 $4.425B 현금 인수 + Apollo의 $9B 무의결권 소수 지분 투자(그중 $5B로 차입금 상환). Apollo 9/10 완료(8-K12B — 같은 날 지주회사 재편, CIK 그대로·옛 회사는 ONEOK, L.L.C.), Brazos 10/6 완료(회사 보도자료, 8-K 없음).
# 둘 다 Q2 뒤라 숫자에 없다 — Q3 10-Q부터 비지배지분 약 $9B 증가·차입금 감소(Codex·Fable r1 필수).
NI_TAGS = ['NetIncomeLossAvailableToCommonStockholdersBasic', 'NetIncomeLoss']
CIK = '0001039684'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '적정'
CO = 'ONEOK'
S_ = 'https://www.sec.gov/Archives/edgar/data/1039684/'
SEC = S_
TENQ = S_ + '000103968426000029/oke-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000103968426000027/okeq22026earningsrelease.htm', 'q1': S_ + '000103968426000015/okeq12026earningsrelease.htm',
      'q4': S_ + '000103968426000004/okeq42025earningsrelease.htm', 'q3': S_ + '000103968425000121/okeq32025earningsrelease.htm'}
LINKS = {'brazos': S_ + '000119312526377023/d405989dex991.htm', 'apollo': S_ + '000119312526387972/d81803d8k12b.htm',
         'brazos_close': 'https://ir.oneok.com/news-and-events/press-releases/2026/10-06-2026-211615960'}
FAIRBAND_TITLE = 'id="okeFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])}, 인수 포함)</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 상품 가격 매출, 차입 큰 구조, 미완료 거래.
MODEL_NOTE = ('매출의 상당 부분이 NGL·정제유 판매라 상품 가격에 따라 매출이 크게 오르내린다 — 이익은 수수료 계약과 물량에 더 달려 있어 PSR보다 이익 배수가 낫다. '
              '과거 매출 성장에는 Magellan·EnLink·Medallion 인수와 상품 가격이 섞여 있어 유기적 성장으로 읽으면 안 된다 — 낙관 시나리오가 가장 낮은 것은 높은 성장에 낮은 최근 이익률을 붙이고, 재투자 효율도 기본(최근 효율에서 평균으로)과 달리 처음부터 평균을 써 재투자가 커지기 때문이다. '
              'Apollo의 대규모 소수 지분 투자(9월 완료 — 3분기부터, 일부로 차입금 상환)와 Brazos 자산 인수(10월 완료 — 4분기부터)는 기준 분기 뒤라 숫자에 없다 — 차입금이 줄고 비지배지분과 그 몫의 이익이 새로 생기며, 보통주 몫 이익에 주는 순효과는 이자 절감·인수 이익과 함께 봐야 한다.')
PH = ['TRGP', 'WMB', 'KMI', 'XOM', 'CVX', 'COP']
PEER_FILE = 'peer_universe/energy.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '미드스트림 3곳·대형 에너지 3곳 PER 비교 (점수는 S&P500 에너지 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 에너지 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 에너지 대비 배수 순위 (v2/peer_universe/energy.json)'
PEER_TIP = ('S&P500 에너지(OKE 제외)와 배수 순위를 매긴 값이다.',
            '석유·가스 생산, 정유, 서비스, 미드스트림이 섞여 있다. 차트에는 미드스트림 3곳과 대형 에너지 3곳만 보인다.')
# 매출(Q2 2026 10-Q 부문 매출, 고객 계약) — 정제유·원유 7,134 + NGL 4,593 + 수집·처리 1,878 + 천연가스 파이프라인 449 = 14,054, 부문 간 거래 −2,005 → 총매출 12,049. 1년 전 2,908·3,871·1,848·405.
SEG = [('정제유·원유', 7134.0, '#e31837'), ('NGL', 4593.0, '#f06a7e'), ('천연가스 수집·처리', 1878.0, '#9e0f25'), ('천연가스 파이프라인', 449.0, '#f7b3bd')]
SEG_ADJ = -2005   # 부문 간 거래 제거(부문 매출 합 14,054 − 총매출 12,049)
SEG_TITLE = '매출 구성 — 부문별(부문 간 거래 제거 전)'
SEG_ADJ_LABEL = '부문 간 거래 제거'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EBITDA·가이던스는 쓰지 않는다), 인수·지분 투자.
# 반응일: 실적 8-K 2025-10-29T00:43Z·2026-02-24T02:21Z·04-29T00:22Z·08-04T00:22Z = 전날 장 마감 뒤 → 다음 세션.
# Brazos·Apollo 보도자료 8/30(일) — 8-K 9/1T01:09Z → 첫 세션 8/31. 넣지 않은 8-K: 이사(1/26·3/25), 주총(5/21), 지분 매각 약정·채권 공개매수(9/15).
NEWS_RANGE = '2025.10 ~ 2026.10'
# Brazos 완료 10/6 보도자료(발표 시각 미상 — 날짜 기준), Apollo 완료 9/10 보도자료·8-K12B 2026-09-11T00:47Z(장 마감 뒤) → 9/11. 다음 실적: 10/5 회사 공지 — 10/27 장 마감 뒤, 콜 10/28.
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-27', 'src': '10/5 회사 공지 — 장 마감 뒤 발표, 콜 10/28 오전 11시(동부)'}
NEWS = [
    ('neutral', '2026년 10월 6일 — Brazos 퍼미안 자산 인수 완료', '2026-10-06',
     '미들랜드 분지 수집·처리 자산 인수를 현금 약 $4.425B에 마무리', 'brazos_close', 'ONEOK 보도자료'),
    ('neutral', '2026년 9월 10일 — Apollo $9B 소수 지분 투자 완료 · 지주회사 재편', '2026-09-11',
     'Apollo가 새 중간 지주회사(ONEOK Holdings)의 무의결권 B급 지분에 $9B 투자 — 신용평가사들은 신용 개선으로 평가, 같은 날 지주회사 구조로 재편', 'apollo', 'ONEOK 공시 (SEC 8-K12B)'),
    ('green', '2026년 8월 30일 — Brazos 퍼미안 자산 인수 · Apollo $9B 지분 투자', '2026-08-31',
     'Brazos Midstream 미들랜드 분지 수집·처리 자산을 현금 $4.425B에 인수 합의 — 자금은 Apollo의 $9B 무의결권 소수 지분 투자(그중 $5B로 차입금 상환)', 'brazos', 'ONEOK 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 3일 — Q2 2026 실적', '2026-08-04',
     'ONEOK 귀속 순이익 $966M(1년 전 $841M) · 희석 EPS $1.53(1년 전 $1.34)', 'q2', 'ONEOK 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 28일 — Q1 2026 실적', '2026-04-29',
     'ONEOK 귀속 순이익 $774M(1년 전 $636M) · 희석 EPS $1.23(1년 전 $1.04)', 'q1', 'ONEOK 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 23일 — Q4 2025 실적', '2026-02-24',
     '희석 EPS $1.55 · 2025년 ONEOK 귀속 순이익 $3.39B·희석 EPS $5.42', 'q4', 'ONEOK 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 28일 — Q3 2025 실적', '2025-10-29',
     'ONEOK 귀속 순이익 $939M(1년 전 $693M) · 희석 EPS $1.49(1년 전 $1.18)', 'q3', 'ONEOK 실적 보도자료 (SEC 8-K)'),
]
# 템플릿 보정(Codex r1): 시나리오 순서가 뒤집혀 보수·낙관 둘 다 현재가 아래 — 세 값 범위로. 체크포인트 ①은 상품 가격 매출이라 영업이익과 함께(Fable r1)
POST = [r'''
h = h.replace('보수~낙관 시나리오가 현재가를 사이에 둬', '세 시나리오 범위가 현재가를 사이에 둬')
h = h.replace('보다 낮아지지 않는지', '보다 낮아지지 않는지 — 상품 가격에 따라 움직이는 매출이라 목표가 아니다, 물량·영업이익 증가와 나눠 본다', 1)
''']
ANALYST = {'rating': 'Buy', 'n': 22, 'nt': 19, 'mean': 100.63, 'median': 100, 'low': 88, 'high': 112, 'sb': 7, 'b': 2, 'h': 13, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-23'

# ── 자동 카드 — 부문 4개(고객 계약 매출). 원문 대조: Q2 2026 7,134/4,593/1,878/449(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "oke:RefinedProductsAndCrudeOilMember": [
   "정제유·원유",
   "#e31837"
  ],
  "oke:NaturalGasLiquidsMember": [
   "NGL",
   "#f06a7e"
  ],
  "oke:NaturalGasGatheringAndProcessingMember": [
   "천연가스 수집·처리",
   "#9e0f25"
  ],
  "oke:WhollyOwnedInterstateNaturalGasPipelinesMember": [
   "천연가스 파이프라인",
   "#f7b3bd"
  ]
 },
 "ignore": []
}
