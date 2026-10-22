# MSI(모토로라 솔루션스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일(분기 말은 52·53주 — Q2 2026은 7/4). 카드 순위 146(시총 144위).
# 공공안전 무전(LMR)·영상 보안·관제 소프트웨어. 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05 장 마감 뒤 접수), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 마감 뒤 접수),
# 8-K(자사주 한도 증액 2026-09-09), StockAnalysis.
# 엔진 입력(2026-10-21): 차입금 $9,032M(단기 $615 + 장기 $8,417) · 현금 $710M = 원문. 단기투자 줄은 없다 — 엔진이 2015-10 단기투자 $276M을 더하던 것은
# build_dcf의 재무상태표 항목 신선도 검사로 버린다(공통, 2026-10-21). 인수 대금은 회사 고유 태그("Acquisitions and investments, net")라 요약 자료에 없다 —
# build_dcf.ACQ_FIXED에 원문 최근 4분기 $4,676M(2025-08 Silvus $4.4B 포함)을 적었다(Codex r1 필수: 빠지면 기본 $162 → 넣으면 $122). 4분기 EPS 2024·2025 보도자료 값. 자본이 작아 PBR이 매우 높다(자사주 누적).
BUILD = {}
CIK = '0000068505'
CUR, YO, QO = '2026-07-04', '2025-06-28', '2026-04-04'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Motorola Solutions'
S_ = 'https://www.sec.gov/Archives/edgar/data/68505/'
SEC = S_
TENQ = S_ + '000006850526000028/msi-20260704.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000006850526000027/msiq22026pressrelease.htm', 'q1': S_ + '000006850526000018/msiq12026pressrelease.htm',
      'q4': S_ + '000006850526000006/msiq42025pressrelease.htm', 'q3': S_ + '000006850525000050/msiq32025pressrelease.htm'}
LINKS = {'dfend': 'https://www.motorolasolutions.com/newsroom/press-releases/motorola-solutions-completes-acquisition-of-dfend-solutions.html', 'bb': 'https://www.sec.gov/Archives/edgar/data/68505/000119312526386490/d492220dex991.htm'}
FAIRBAND_TITLE = 'id="msiFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 35)
ACT_REASON = ''
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-11-04', 'src': '10/19 회사 공지 — 장 마감 뒤 발표, 콜 오후 5시(동부)'}   # Codex r1 필수
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 잦은 인수, 정부 고객·수주잔고, 자사주로 작은 자본.
MODEL_NOTE = ('매출 성장에는 인수(무선 통신·영상·관제·드론 대응)가 섞여 있고, 큰 인수가 있던 해에는 그 대금이 재투자로 잡혀 현금흐름 가치를 크게 낮춘다. '
              '고객 대부분이 정부·공공기관이라 수주잔고가 길고 매출이 안정적인 편이다. 자사주 매입으로 자본이 작아 PBR과 부채비율이 높게 나온다.')
PH = ['APH', 'CSCO', 'ANET', 'IBM', 'DELL', 'STX']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '통신·IT 장비 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': '통신·IT 장비 PBR 비교', 'psr': '통신·IT 장비 PSR 비교',
                'pcr': '통신·IT 장비 PCR(FCF) 비교', 'evebitda': '통신·IT 장비 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(MSI 제외)과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 섞여 있다. 차트에는 통신·IT 장비 회사만 보인다.')
# 매출(Q2 2026 10-Q 주석 부문) — 제품·시스템 통합 1,908 + 소프트웨어·서비스 1,225 = 3,133. 1년 전 1,653/1,112 → 2,765.
SEG = [('제품·시스템 통합(무전기·영상 장비)', 1908, '#005eb8'), ('소프트웨어·서비스', 1225, '#4c92d6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 사업 부문별'
# 손 뉴스: 최신 실적(Q2 2026, 8/5)도 손으로 — 뒤에 9/9 자사주 한도 증액이 있다. 가이던스·비GAAP EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부, 날짜도 UTC 값): 실적 8-K 2025-10-31T00:12Z = 10/30 20:12 → 10/31, 2026-02-12T02:12Z → 2/12, 05-08T00:14Z → 5/8, 08-06T00:12Z → 8/6.
# 자사주 8-K 2026-09-10T00:22Z = 9/9 20:22 → 9/10.
# 넣지 않은 8-K: 이사 선임(2025-11-19·2026-03-13), 주총(5/21), 회사채 $350M(8/18).
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 9일 장 마감 뒤 — 자사주 한도 $2B 증액', '2026-09-10',
     '누적 승인 $20B로(2분기 말 남은 한도 약 $0.6B에 더함, 기한 없음)', 'bb', 'Motorola Solutions 공시 (SEC 8-K)'),
    ('neutral', '2026년 8월 20일 — D-Fend Solutions 인수 완료', '2026-08-20',
     '드론 대응(무선 사이버 장악) 기술 회사를 $1.5B에 인수(5월 31일 계약) — 회사 발표, 8-K 없음', 'dfend', 'Motorola Solutions 보도자료'),
    ('green', '2026년 8월 5일 장 마감 뒤 — Q2 2026 실적', '2026-08-06',
     '매출 $3.13B(+13%) · 희석 EPS $3.33(1년 전 $3.04) · 영업이익 $809M(+17%) — 관세(IEEPA) 환급 $60M(영업이익률 1.9%p) 포함', 'q2', 'Motorola Solutions 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 7일 장 마감 뒤 — Q1 2026 실적', '2026-05-08',
     '매출 $2.71B(+7%) · 희석 EPS $2.18(1년 전 $2.53) · 영업이익 $525M(1년 전 $582M) · 분기 말 수주잔고 $15.7B(+11%)', 'q1', 'Motorola Solutions 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 11일 장 마감 뒤 — Q4 2025 실적', '2026-02-12',
     '매출 $3.38B(+12%) · 희석 EPS $3.86(1년 전 $3.56) · 2025년 매출 $11.68B·EPS $12.75', 'q4', 'Motorola Solutions 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 30일 장 마감 뒤 — Q3 2025 실적', '2025-10-31',
     '매출 $3.01B(+8%) · 희석 EPS $3.33(1년 전 $3.29) · 8월 Silvus Technologies 인수 완료 분기', 'q3', 'Motorola Solutions 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 14, 'nt': 8, 'mean': 525.13, 'median': 530, 'low': 476, 'high': 550, 'sb': 7, 'b': 5, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-21'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(부문 2개). 원문 대조: Q2 2026 1,908/1,225, 1년 전 1,653/1,112(2026-10-21) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "msi:ProductAndSystemsIntegrationSegmentMember": [
   "제품·시스템 통합(무전기·영상 장비)",
   "#005eb8"
  ],
  "msi:ServicesAndSoftwareSegmentMember": [
   "소프트웨어·서비스",
   "#4c92d6"
  ]
 },
 "ignore": []
}
