# MCK(맥케슨) v2 카드 설정 — 자동 카드(AUTO). 회계연도 3월 말(FY27 1분기 = 2026-04~06). 카드 순위 108.
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-08-05), 실적 보도자료(Q2 FY26~Q1 FY27, 8-K 2.02항 — 모두 장 마감 뒤 접수), 8-K(
# CFO 교체 2026-03-04, 사이버 보안 사고 2026-08-25, Option Care Health 인수 계약 2026-10-06), StockAnalysis.
# 엔진 입력(2026-10-13): 감가상각은 현금흐름표 D&A(DepreciationAndAmortization = 감가상각 + 상각, FY26 $729M) — DepreciationDepletionAndAmortization($287M)은 일부라
# EXCLUDE_TAGS(분기 D&A 태그가 2025년부터라 EV/EBITDA 자기 이력이 짧다). 비지배지분 = 일반 $376M + 상환 가능 $2,563M(Core Ventures 30%·Apollo 의료·수술 부문
# 전환우선주, EV_TAGS_BY_CIK). 4분기 EPS 보도자료 값(FY26 $13.71·FY25 $10.01). 최근 4분기 순이익률 2% 미만이라 PER은 점수에서 빠진다(A3). 자본 음수 — PBR 해당 없음.
# 의료·수술 부문 분리는 계획 단계(10-Q 분리 비용만, 중단사업 아님) — 분리가 끝나면 README 분사 규칙대로 재작성 뒤 다시 만든다.
CIK = '0000927653'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-03-31', '2025-03-31'), 'FY2026'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'McKesson'
S_ = 'https://www.sec.gov/Archives/edgar/data/927653/'
SEC = S_
TENQ = S_ + '000092765326000234/mck-20260630.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000092765326000232/mck_exhibit991x6302026.htm', 'q4': S_ + '000092765326000066/mck_exhibit991x3312026.htm',
      'q3': S_ + '000092765326000015/mck_exhibit991x12312025.htm', 'q2': S_ + '000092765325000138/mck_exhibit991x9302025.htm'}
LINKS = {'opch': S_ + '000092765326000253/mck-20261006.htm', 'cyber': S_ + '000092765326000247/mck-20260825.htm',
         'cfo': S_ + '000092765326000035/mck-20260303.htm'}
FAIRBAND_TITLE = 'id="mckFairBand" title="최근 1년 PER 25~75% 구간 × 최근 4분기 희석 EPS. 최근 4분기 순이익률이 2% 미만이라 PER은 점수에 쓰지 않는다(A3) — 범위는 참고로만 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 3)
ACT_REASON = ''
NONOP_WHAT = '지분·장기투자'
PH = ['COR', 'CAH', 'CVS', 'CI', 'UNH', 'HSIC']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '헬스케어 6곳 PER 비교 — 유통 3사(COR·CAH)와 CVS는 순이익률 2% 미만이라 PER 없음', 'pbr': '헬스케어 PBR 비교', 'psr': '헬스케어 PSR 비교',
                'pcr': '헬스케어 PCR(FCF) 비교', 'evebitda': '헬스케어 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(MCK 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·유통 회사가 섞여 있다. 의약품 유통사는 매출이 커 PSR이 낮게 나온다. 차트에는 유통·보험 6곳만 보인다.')
# 부문(Q1 FY27 10-Q Note 13) — 북미 의약품 86,773 + 종양·다전문 14,222 + 처방 기술 1,566 + 의료·수술 2,819 = 105,380(연결 매출). 1년 전 Other $305M은 매각한 노르웨이 사업.
SEG = [('북미 의약품', 86773, '#005a8c'), ('종양·다전문', 14222, '#2e9bd6'), ('의료·수술', 2819, '#e07b39'), ('처방 기술', 1566, '#6aa84f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: Q1 FY27 실적(8/5 장 마감 뒤)도 손으로 쓴다 — 그 뒤 사이버 사고(8/25)·Option Care 인수 계약(10/6)을 넣으면 자동 실적 항목이 빠지기 때문(README).
NEWS_RANGE = '2025.11 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 6일 — Option Care Health 인수 계약(CD&R과 공동)', '2026-10-06',
     '주당 $32.05, 기업가치 약 $5.8B — CD&R 약 51%, McKesson 약 $1.4B 투자로 약 49% · CD&R 지분을 나중에 McKesson이 인수하는 틀 포함', 'opch', 'McKesson 공시 (SEC 8-K)'),
    ('red', '2026년 8월 28일 장 마감 뒤 — 사이버 보안 사고 공시', '2026-08-31',
     '8월 25일 발견 · 조사 초기, 공시 시점에 중대성 판단 안 함', 'cyber', 'McKesson 공시 (SEC 8-K)'),
    ('red', '2026년 8월 5일 장 마감 뒤 — Q1 FY27 실적', '2026-08-06',
     '매출 $105.4B(+8%) · 희석 EPS $5.15(1년 전 $6.25) · 분기 배당 $0.94(+15%) · 자사주 매입 $2.5B(가속 매입 $2.25B 포함)', 'q1', 'McKesson 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 7일 장 마감 뒤 — Q4 FY26 실적', '2026-05-08',
     '매출 $96.3B(+6%) · 희석 EPS $13.71(1년 전 $10.01) · FY26 EPS $38.38 · 자사주 매입 승인 $5.0B 증액', 'q4', 'McKesson 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 5일 — 새 CFO 선임 공시', None,
     'Kenny Cheung(전 Sysco) 3월 4일 선임, 5월 29일 취임 · Britt Vitalone 은퇴', 'cfo', 'McKesson 공시 (SEC 8-K)'),
    ('green', '2026년 2월 4일 장 마감 뒤 — Q3 FY26 실적', '2026-02-05',
     '매출 $106.2B(+11%) · 희석 EPS $9.59 · 1월 30일 노르웨이 사업 매각 완료', 'q3', 'McKesson 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 5일 장 마감 뒤 — Q2 FY26 실적', '2025-11-06',
     '매출 $103.2B(+10%) · 희석 EPS $8.92 · 2분기부터 4개 부문으로 공시', 'q2', 'McKesson 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 16, 'nt': 14, 'mean': 996.86, 'median': 1000, 'low': 845, 'high': 1200, 'sb': 10, 'b': 3, 'h': 3, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-17'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-Q Note 13 Q1 FY27 86,773/14,222/2,819/1,566, 1년 전 82,729/10,658/2,701/1,434 + Other 305(노르웨이, 2026-01 매각) = 97,827(2026-10-14) ──
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
  "mck:NorthAmericanPharmaceuticalSegmentMember": [
   "북미 의약품",
   "#005a8c"
  ],
  "mck:OncologyAndMultispecialtySegmentMember": [
   "종양·다전문",
   "#2e9bd6"
  ],
  "mck:MedicalSurgicalSolutionsSegmentMember": [
   "의료·수술",
   "#e07b39"
  ],
  "mck:PrescriptionTechnologySolutionsSegmentMember": [
   "처방 기술",
   "#6aa84f"
  ]
 },
 "ignore": []
}
