# NUE(뉴코어) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일(분기는 13주). 카드 순위 176. 미국 최대 철강사 — 전기로 제강(Steel mills), 철강 제품(Steel products), 원자재(Raw materials: DRI·고철).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-12 장 전 접수), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 마감 뒤), StockAnalysis.
# 엔진 입력(2026-10-23): 영업이익 줄이 없어 세전이익 + 순이자비용으로 합성(DERIVED_OPINC, Q2 2026 1,625 + 12 = 1,637), 차입금 = 단기 129 + 1년 안 장기·금융리스 581 + 장기·금융리스 6,389 = $7,099M(DEBT_TOTAL_TAG — 장기 태그가 2019년에 멈춤).
# 비지배지분 $1,157M(합작 제철소 Nucor-Yamato 등). 4분기 EPS 2021~2025는 보도자료 값(Q4_EPS_OVERRIDE).
CIK = '0000073309'
CUR, YO, QO = '2026-07-04', '2025-07-05', '2026-04-04'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Nucor'
S_ = 'https://www.sec.gov/Archives/edgar/data/73309/'
SEC = S_
TENQ = S_ + '000119312526345891/nue-20260704.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000119312526318190/d468854dex991.htm', 'q1': S_ + '000119312526182332/d150975dex991.htm',
      'q4': S_ + '000119312526022733/d20933dex991.htm', 'q3': S_ + '000119312525251721/d34902dex991.htm'}
LINKS = {'guide': 'https://nucor.com/news/?article=nucor-announces-guidance-for-the-third-quarter-of-2026-earnings-122997'}
FAIRBAND_TITLE = 'id="nueFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 경기 순환 — 이익이 철강 가격에 크게 달려 있다.
MODEL_NOTE = ('철강 가격에 따라 이익이 크게 오르내리는 경기 순환 업종이다 — 이익이 바닥일 때 PER이 높고 꼭대기일 때 낮아, 배수 이력은 이익의 위치와 함께 읽는다. '
              '시나리오 이름과 달리 보수가 가장 높다 — 보수는 호황기(2021~22)가 들어간 5년 중앙 이익률, 기본은 최근 2년, 낙관은 최근 4분기 이익률을 써서 값의 차이를 성장보다 이익률이 만든다. '
              '손익계산서에 영업이익 줄이 없어 세전이익에 순이자비용을 더해 영업이익으로 쓴다(지분법 이익·자산 손상·투자 평가이익도 들어간다) — 2026년 2분기에는 Helion 투자 평가이익과 과거 원재료 비용 환급 같은 일회성 이익이 이익률을 끌어올렸다. '
              '합작 제철소의 비지배지분은 장부가로만 빼는데 그 몫의 이익이 커서 내재가치가 다소 후하게 나올 수 있다.')
PH = ['STLD', 'FCX', 'VMC', 'MLM', 'CRH', 'LIN']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '철강·광산·건자재·산업용 가스 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(NUE 제외)와 배수 순위를 매긴 값이다.',
            '화학·산업용 가스·광산·포장·건자재가 섞여 있다. 차트에는 철강·광산·건자재·산업용 가스 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문 외부 매출) — 제철소 6,481 + 철강 제품 3,105 + 원자재 811 = 10,397(= 총매출). 1년 전 5,253·2,657·546 = 8,456.
SEG = [('제철소(Steel mills)', 6481.0, '#00539b'), ('철강 제품', 3105.0, '#5a8fc7'), ('원자재(DRI·고철)', 811.0, '#003566')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(외부 매출)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다).
# 반응일: 실적 8-K 2025-10-27T20:53Z·2026-01-26T21:51Z·04-27T20:56Z·07-27T20:43Z = 장 마감 뒤 → 다음 세션. 넣지 않은 8-K: 임원(12/4·2/20·3/3), 주총(5/19).
NEWS_RANGE = '2025.10 ~ 2026.09'
# Q3 가이던스 9/17 보도자료(회사 IR, 8-K 없음 — 발표 시각 미상, 9/17 +1.7%·9/18 −6.3%라 다음 세션으로 둠). 다음 실적: 회사 공지 — 10/26 장 마감 뒤.
NEXT_CONFIRMED = {'quarter_end': '2026-10-03', 'date': '2026-10-26', 'src': '회사 공지 — 장 마감 뒤 발표'}
NEWS = [
    ('red', '2026년 9월 17일 — Q3 2026 이익 가이던스', '2026-09-18',
     'Q3 희석 EPS $5.55~5.65 예상(Q2 $5.04) — 제철소·철강 제품 이익은 늘고 원자재 부문은 줄 전망 · 발표 시각을 확인하지 못해 반응은 다음 날(9/18) 종가 등락으로 적었다', 'guide', 'Nucor 보도자료'),
    ('green', '2026년 7월 27일 — Q2 2026 실적', '2026-07-28',
     '귀속 순이익 $1.16B · 희석 EPS $5.04(1년 전 $2.60, Helion 투자 평가이익 주당 $0.20 포함) · 매출 $10.4B(+23%) · 10-Q: 과거 원재료 비용 현금 환급으로 매출원가 $130M 감소', 'q2', 'Nucor 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 27일 — Q1 2026 실적', '2026-04-28',
     '귀속 순이익 $743M · 희석 EPS $3.23(1년 전 $0.67) · 제철소 분기 출하량 최대 · 2월 자사주 매입 한도 $4.0B 새로 승인', 'q1', 'Nucor 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 26일 — Q4 2025 실적', '2026-01-27',
     '귀속 순이익 $378M · 희석 EPS $1.64(1년 전 $1.22, 손상 주당 $0.09 포함) · 2025년 희석 EPS $7.52(1년 전 $8.46)', 'q4', 'Nucor 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 27일 — Q3 2025 실적', '2025-10-28',
     '귀속 순이익 $607M · 희석 EPS $2.63(1년 전 $1.05)', 'q3', 'Nucor 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 17, 'nt': 12, 'mean': 287.75, 'median': 295, 'low': 256, 'high': 306, 'sb': 10, 'b': 3, 'h': 3, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 부문 3개(수동 지도, 외부 매출). 원문 대조: Q2 2026 6,481/3,105/811(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"nue:SteelMillsMember": ["제철소(Steel mills)", "#00539b"], "nue:SteelProductsMember": ["철강 제품", "#5a8fc7"], "nue:RawMaterialsMember": ["원자재(DRI·고철)", "#003566"]},
 "ignore": []
}
