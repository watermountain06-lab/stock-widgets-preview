# AJG(아서 J. 갤러거) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 162(시총 160위). 보험 중개·위험 관리(클레임 대행).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 마감 뒤 접수), StockAnalysis.
# 엔진 입력(2026-10-22): 영업이익 줄이 없다 — 세전이익 + 이자비용(DERIVED_OPINC, Q2 2026 414 + 168 = 582). 설비투자 PaymentsForCapitalImprovements(태그 맵·CONCEPTS_BY_CIK).
# 인수 지출은 회사 고유 태그(ajg:PaymentsToAcquireBusinessesNetOfCashAndRestrictedCashAcquired)라 BUILD company_tags로 표준 이름에 싣는다 — 2025-08 AssuredPartners 인수 포함 최근 4분기 $14.7B.
# 현금 $1,386M(수탁 현금 $7,947M은 고객 돈이라 빼지 않음 — EV_TAGS_BY_CIK). 차입금 = 회사 차입 1,520 + 11,955 = $13,475M(프리미엄 금융 차입 $134M 제외). 4분기 EPS 2024 보도자료 값.
BUILD = {'company_tags': [('ajg:PaymentsToAcquireBusinessesNetOfCashAndRestrictedCashAcquired', 'PaymentsToAcquireBusinessesNetOfCashAcquired')]}
CIK = '0000354190'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, None, -2), '적정~고평가'
CO = 'Gallagher'
S_ = 'https://www.sec.gov/Archives/edgar/data/354190/'
SEC = S_
TENQ = S_ + '000162828026053489/ajg-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000162828026051070/a2ndquarter2026earningsrel.htm', 'q1': S_ + '000035419026000132/lab_exhibit991q1.htm',
      'q4': S_ + '000119312526029407/d38405dex991.htm', 'q3': S_ + '000119312525258781/d83473dex991.htm'}
LINKS = {'ap': S_ + '000035419025000019/ajg-20250818.htm'}
FAIRBAND_TITLE = 'id="ajgFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 인수로 크는 회사의 현금흐름 모델, 인수 무형자산 상각.
MODEL_NOTE = ('이 회사는 해마다 많은 중개사를 사들여 큰다 — 모델은 인수 지출을 재투자에 넣고, 투자 한 단위가 매출을 얼마나 늘리는지(투자 효율)로 앞으로의 재투자를 추정한다. '
              '최근 4분기에는 대형 인수(AssuredPartners)가 한꺼번에 들어가 투자 효율이 평소보다 크게 낮아져 보수·기본 시나리오를 누르고, 평소 효율을 쓰는 낙관 시나리오도 이 성장·이익률·순부채 가정에서는 0 이하다(판정의 현금흐름 칸은 이 계산 결과다). '
              '다만 이 회사는 대형 인수 전에도 모델 값과 주가의 차이가 컸다. 영업이익은 인수한 고객 목록의 상각비를 뺀 GAAP 값이라 회사가 발표하는 조정 이익보다 작다.')   # Codex r1 필수 · Fable r1 권장
HEALTH_EXTRA = '유동비율·부채비율에는 고객 수탁 자금(자산과 부채에 같은 금액)이 들어 있어 실제 지급능력보다 나쁘게 나온다. 반대로 차입금 의존도는 수탁 자산이 총자산을 키워 실제보다 좋게 나온다. 현금에는 제한 현금이 일부 들어 있고, 순현금 칸의 운용리스는 직전 연차 보고서(2025-12-31) 값이다.'   # 고정 문장(MRSH와 같은 구조)
PH = ['MRSH', 'AON', 'BRO', 'WTW', 'SPGI', 'MCO']
PEER_FILE = 'peer_universe/brokers_fees.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '보험 중개·금융 데이터 6곳 PER 비교 (점수는 중개사 + 결제·거래소·데이터 기준)', 'pbr': '보험 중개·금융 데이터 PBR 비교', 'psr': '보험 중개·금융 데이터 PSR 비교',
                'pcr': '보험 중개·금융 데이터 PCR(FCF) 비교', 'evebitda': '보험 중개·금융 데이터 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 보험 중개사와 결제·거래소·금융 데이터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 보험 중개 + 결제·거래소·금융 데이터 대비 배수 순위 (v2/peer_universe/brokers_fees.json)'
PEER_TIP = ('S&P500 보험 중개사(AJG 제외)와 결제·거래소·금융 데이터 회사(수수료로 버는 자산 경량 서비스)와 배수 순위를 매긴 값이다 — 중개사만으로는 비교 표본이 모자란다.',
            '카드 네트워크·결제 처리·거래소·신용평가 회사가 섞여 있어 성장·마진 구조가 다르다 — 차트의 중개사 4곳과 직접 비교할 것(차트에는 중개사 4곳과 신용평가 2곳만 보인다).')
# 매출(Q2 2026 10-Q 부문) — 중개 3,502 + 위험 관리 501(비용 환급 48 포함) = 4,003. 1년 전 2,787·435 → 3,222. 본사 부문 매출 0.
SEG = [('보험 중개', 3502.0, '#0b3d91'), ('위험 관리(클레임 대행)', 501.0, '#5b8bd6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 뉴스: 실적 4건은 손으로(매출은 비용 환급 포함 총수익 — 보도자료 표의 '환급 전 매출'과 다르다). 가이던스·조정 EPS·유기 성장률은 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K 2025-10-31T00:52Z·2026-01-30T02:20Z·05-01T00:19Z·07-31T00:18Z = 전날 장 마감 뒤 → 다음 세션.
# AssuredPartners 인수 완료 8-K 2025-08-18T16:18Z = 동부 12:18 장중 → 같은 날(Fable r1 권장 — Q4 +34%와 현금흐름 칸의 원인 사건).
# 넣지 않은 8-K: 투자자 행사(12/16·3/17·6/17 7.01항), 주총(5/13), 이사 별세(7/29), 회계 책임자 은퇴(8/27), 임원(3/12).
NEWS_RANGE = '2025.08 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 30일 — Q2 2026 실적', '2026-07-31',
     '총수익 $4.00B(+24%) · 희석 EPS $1.25(1년 전 $1.40 — 인수 대기 자금 이자수익 약 $144M, 세후 주당 약 $0.42 포함) · 인수 통합·고객 목록 상각 비용 증가', 'q2', 'Gallagher 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 30일 — Q1 2026 실적', '2026-05-01',
     '총수익 $4.76B(+28%) · 희석 EPS $3.16(1년 전 $2.72)', 'q1', 'Gallagher 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 29일 — Q4 2025 실적', '2026-01-30',
     '총수익 $3.63B(+34%, AssuredPartners 인수 효과) · 희석 EPS $0.58(1년 전 $1.12)', 'q4', 'Gallagher 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 30일 — Q3 2025 실적', '2025-10-31',
     '총수익 $3.37B(+20%) · 희석 EPS $1.04(1년 전 $1.39)', 'q3', 'Gallagher 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 8월 18일 — AssuredPartners 인수 완료', '2025-08-18',
     '미국 보험 중개사 AssuredPartners를 현금 약 $13.8B에 인수 완료 — 앞서 발행한 주식·채권 자금으로 치렀다', 'ap', 'Gallagher 공시 (SEC 8-K 2.01항)'),
]
# 다음 실적일: 2026-10-08 회사 공지 — 10/29 장 마감 뒤 발표, 오후 5시 15분(동부) 콜(Codex r1 필수)
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-29', 'src': '10/8 회사 공지 — 장 마감 뒤 발표, 콜 오후 5시 15분(동부)'}
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 17, 'mean': 285.41, 'median': 284, 'low': 242, 'high': 388, 'sb': 12, 'b': 4, 'h': 7, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'

# ── 자동 카드 — 부문 지도(중개·위험 관리, 본사 0은 ignore). 원문 대조: Q2 2026 3,502/501, 1년 전 2,787/435(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"ajg:BrokerageSegmentMember": ["보험 중개", "#0b3d91"], "ajg:RiskManagementSegmentMember": ["위험 관리(클레임 대행)", "#5b8bd6"]},
 "ignore": ["us-gaap:CorporateMember"]
}
