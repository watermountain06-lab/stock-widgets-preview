# MRNA(모더나) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 132(시총 130위). mRNA 백신(COVID·RSV·독감)과 항암 치료제(intismeran, Merck 공동).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-31), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항), 8-K(신용 계약 2025-11-24, FDA 독감 RTF 2026-02-10, Arbutus·Genevant 합의 2026-03-03,
# 전환사채 2026-09-01, COO 선임 2026-09-30), Merck·Moderna 공동 보도자료(intismeran 3상 2026-08-19)·Moderna 보도자료(독감 백신 승인 2026-08-06) — 둘 다 8-K 없음, StockAnalysis.
# 엔진 입력(2026-10-21): 현금 $1,723M·단기투자 $3,415M·장기투자 $1,772M(비영업 자산)·차입금 $591M(Ares 기간 대출)·운용리스 $659M·금융리스 $37M·주식 수 399.2M = 원문.
# 적자라 PER은 "해당 없음"(A3), EPS가 음수라 PER 밴드 백테스트 체크포인트 0개. 최근 4분기 영업이익에 Arbutus·Genevant 합의 비용 $884M(매출원가, 10-Q 주석 12)이 들어 있다(B2 — GAAP 유지, 뉴스에 적음).
# 6/30 미지급비용에 합의금 $950M이 남아 있다(3분기 지급) — 운전자본이 그만큼 음수. 9월 전환사채 $3.0B(순조달 약 $2,957M)는 Q3 10-Q부터 차입금에 들어간다.
# 4분기 EPS: 2022·2023·2025는 보도자료 값(Q4_EPS_OVERRIDE).
CIK = '0001682852'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Moderna'
S_ = 'https://www.sec.gov/Archives/edgar/data/1682852/'
SEC = S_
TENQ = S_ + '000168285226000150/mrna-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000168285226000147/exhibit9912026q2pressrelea.htm', 'q1': S_ + '000168285226000057/exhibit9912026q1pressrelea.htm',
      'q4': S_ + '000168285226000015/exhibit9912025q4pressrelea.htm', 'q3': S_ + '000168285225000073/exhibit9912025q3pressrelea.htm'}
LINKS = {'coo': S_ + '000119312526408289/d18337dex991.htm', 'conv': S_ + '000119312526378505/d108896d8k.htm',
         'p3': 'https://www.merck.com/news/merck-and-moderna-announce-phase-3-interpath-001-trial-of-intismeran-autogene-plus-keytruda-met-endpoints-of-recurrence-free-survival-rfs-and-distant-metastasis-free-survival-dmfs-in-patient/',
         'flu': 'https://www.newswire.com/news/moderna-receives-u-s-fda-approval-for-influenza-vaccine-mflusiva', 'aday': S_ + '000162828025053318/exhibit9912025analystday.htm', 'settle': S_ + '000168285226000047/mrna-20260303.htm',
         'rtf': S_ + '000168285226000012/exhibit991-02102026.htm',}
FAIRBAND_TITLE = ('id="mrnaFairBand" title="{(\'최근 1년 PER 25~75% 구간(\' + format(FB[\'per_p25\'], \'.1f\') + \'~\' + format(FB[\'per_p75\'], \'.1f\') + \'배) × 최근 4분기 희석 EPS $\' + str(eps_ttm) + \'(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다.\') if FB else \'최근 4분기 순손실이라 PER로 범위를 낼 수 없다.\'}"')   # 적자면 FB 없음 — 흑자 전환 뒤에는 범위(조건식)
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 60)
ACT_REASON = '매출원가·재고 공시가 첫 상업 판매(2020년)부터라 5년 비교 분기가 모자람'
NONOP_WHAT = '장기 투자증권'
# 고정 문장(숫자 없음 — 분기마다 고치지 않는다).
MODEL_NOTE = ('영업적자인 회사라 이 모델은 최근 이익률을 출발점으로 삼아 가치가 음수로 나온다 — 항암 치료제·새 백신의 허가 여부와 출시 뒤 매출은 '
              '과거 실적에 없어 따로 넣지 않는다. 현재가에 그런 기대가 들어 있다고 보면 이 값과의 차이가 크게 나오는 이유가 된다.')
PH = ['PFE', 'MRK', 'REGN', 'VRTX', 'AMGN', 'BIIB']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '제약·바이오 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': '제약·바이오 PBR 비교', 'psr': '제약·바이오 PSR 비교',
                'pcr': '제약·바이오 PCR(FCF) 비교', 'evebitda': '제약·바이오 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(MRNA 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·서비스 회사가 섞여 있다. 차트에는 제약·바이오 6곳만 보인다.')
# 매출(Q2 2026 10-Q 주석 3 제품별 순매출 + 주석 4 기타 매출) — COVID(Spikevax·mNEXSPIKE) 91 + RSV(mRESVIA) 3 + 기타 매출 51(위탁 생산 대기 31·협력 15·보조금 2·라이선스 3) = 총매출 145.
# 1년 전 114 + 0 + 28 = 142.
SEG = [('COVID 백신(Spikevax·mNEXSPIKE)', 91, '#d71e28'), ('기타 매출(협력·위탁 생산 등)', 51, '#9ca3af'), ('RSV 백신(mRESVIA)', 3, '#e88a8f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품별 순매출과 기타 매출'
# 손 뉴스: 최신 실적(Q2 2026, 7/31)도 손으로 쓴다 — 그 뒤 손 항목(8/6 독감 승인, 8/19 3상, 8/27 전환사채, 9/30 COO)이 있으면 자동 항목이 빠진다. Q3 실적부터 다시 자동. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): COO 8-K 9/30 15:15 → 9/30, 전환사채는 발표 보도자료 8/27(8-K 최초 사건일 8/27, 그날 −4.6% — Fable r1; 완료 8-K는 9/1 20:37), Q2 8-K 7/31 15:03 → 7/31, Q1 5/1 14:32 → 5/1,
# Q4 2/13 17:02 → 2/13, FDA RTF 8-K 2/11 04:02(=2/10 23:02) → 2/11, Q3 11/6 17:03 → 11/6, 신용 계약 8-K 11/25 02:29(=11/24 21:29) → 11/25.
# 3상: 8-K 없음 — Merck·Moderna 공동 보도자료 8/19 06:45 EDT(장 전, Merck 웹사이트) → 8/19(그날 +177%). 독감 승인: FDA 8/5, 보도자료 8/6(시각 미표시) → 8/6.
# 애널리스트 데이 8-K 11/20 17:12 → 11/20(Ares 대출 최초 발표 — 11/24 신용 계약 8-K는 세부라 따로 넣지 않음, Codex r1).
# 합의: 보도자료 3/3 16:15 ET(장 마감 뒤, Stockwatch 전재) → 3/4. 8-K는 3/5 01:20 ET 접수.
# 넣지 않은 8-K: 신용 계약 세부(11/24), 주총(11/13·5/11), 주주 서한(1/5), JPM 예비 실적(1/12 — Q4 실적과 겹침), 이사 선임(7/8).
NEWS_RANGE = '2025.11 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 30일 — 최고운영책임자(COO) 신설: Juan Andres 복귀', '2026-09-30',
     '10월 5일부터 COO(제조 조직 총괄) · Jerh Collins 기술운영·품질 책임자 퇴임 · 미국 독감 백신·EU 독감+COVID 복합 백신 승인으로 승인 백신 5개, intismeran 출시 준비를 이유로 듦', 'coo', 'Moderna 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 27일 — 전환사채 발행 발표(9월 1일 $3.0B 완료)', '2026-08-27',
     '8월 27일 보도자료(발표 시각 미확인)로 처음 $2.0B 제안 → 8월 28일 $2.6B로 늘려 가격 결정(전환가 약 $210.58) → 추가분 $400M까지 9월 1일 완료 · 2032년 만기 무이자 전환사채 $3.0B · 순조달 약 $2,957M 중 $328.8M은 희석을 줄이는 캡드콜 비용 · 전환 시 약 1,425만 주(최대 2,101만 주) · 항암 사업 투자·부채 상환 등에 쓸 수 있다', 'conv', 'Moderna 공시 (SEC 8-K)'),
    ('green', '2026년 8월 19일 — 항암 치료제 intismeran 흑색종 3상 성공', '2026-08-19',
     'Merck와 공동 개발한 개인 맞춤 mRNA 항암 치료제 · 절제한 IIB~IV기 흑색종 보조 치료(KEYTRUDA 병용) 3상 INTerpath-001(1,137명, 2:1 배정)이 사전에 정한 중간 분석에서 무재발 생존(주요 목표)·원격 전이 없는 생존 개선 · 3상 위험비는 미공개, 전체 생존은 계속 평가 · 규제 당국과 허가 신청 협의 예정 · SEC 공시 없음', 'p3', 'Merck·Moderna 공동 보도자료 (Merck 웹사이트)'),
    ('green', '2026년 8월 6일 — 미국 FDA, 독감 백신 mFLUSIVA 승인', '2026-08-06',
     'mRNA-1010 · 50세 이상(65세 이상은 면역 반응 기반 가속 승인 — 확증 시험 조건) · 미국 4번째·전 세계 5번째 승인 제품 · 2월 접수 거부 뒤 심사 · FDA 승인일 8월 5일, 보도자료 8월 6일(발표 시각 미표시) · SEC 공시 없음', 'flu', 'Moderna 보도자료 (Newswire)'),
    ('neutral', '2026년 7월 31일 — Q2 2026 실적', '2026-07-31',
     '매출 $0.15B(+2%) · 희석 EPS −$1.97(1년 전 −$2.13) · 노로바이러스 백신 3상 중간 분석이 조기 성공 기준 미달(시험 계속)', 'q2', 'Moderna 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 1일 — Q1 2026 실적', '2026-05-01',
     '매출 $0.39B(1년 전 $0.11B) · 희석 EPS −$3.40(1년 전 −$2.52) · Arbutus·Genevant 합의 비용 약 $0.9B 포함', 'q1', 'Moderna 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 3일 장 마감 뒤 — Arbutus·Genevant 특허 소송 합의', '2026-03-04',
     '전 세계 소송 종결 · $950M 일시금(3분기 지급), 앞으로 로열티 없음 · 미국 정부 납품분 항소(§1498)에서 지면 최대 $1.3B 추가', 'settle', 'Moderna 공시 (SEC 8-K)'),
    ('neutral', '2026년 2월 13일 — Q4 2025 실적', '2026-02-13',
     '매출 $0.68B(−30%) · 희석 EPS −$2.11(1년 전 −$2.91) · 2025년 매출 $1.94B·EPS −$7.26', 'q4', 'Moderna 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 10일 장 마감 뒤 — FDA, 독감 백신 허가 신청 접수 거부', '2026-02-11',
     'mRNA-1010 허가 신청에 접수 거부(RTF) 서한 — 비교 백신(표준 용량 독감 백신) 선택이 유일한 사유 · Type A 회의 요청 · EU·캐나다·호주는 심사 중 · 2026년 재무 전망 영향 없다고 밝힘', 'rtf', 'Moderna 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 20일 — 애널리스트 데이 · Ares 기간 대출 최대 $1.5B', '2025-11-20',
     '3년 계획 — 2026년 매출 최대 10% 성장, 2028년 현금 손익분기 목표 · 2026·2027년 GAAP 영업비용 각 약 $0.5B 추가 절감 · Ares에서 5년 만기 기간 대출 최대 $1.5B(첫 $600M, SOFR + 5.50% — 계약 세부는 11/24 8-K)', 'aday', 'Moderna 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 6일 — Q3 2025 실적', '2025-11-06',
     '매출 $1.02B(−45%) · 희석 EPS −$0.51(1년 전 $0.03)', 'q3', 'Moderna 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Hold', 'n': 23, 'nt': 16, 'mean': 118.13, 'median': 125, 'low': 45, 'high': 220, 'sb': 4, 'b': 1, 'h': 14, 's': 2, 'ss': 2}
ANALYST_ASOF = '2026-10-21'


# ── 자동 카드 — 부문 지도는 제품 축(srt:ProductOrServiceAxis)에서 COVID·RSV·기타 매출(ProductAndServiceOther) 세 멤버. 순매출 소계와 기타 매출의 세부 4개는 ignore.
# seg_map_propose 1판은 RSV $3M이 라이선스 $3M과 같아 1개만 맞췄다 — 손으로 고름. 원문 대조: Q2 2026 91/3/51, 1년 전 114/0/28, Q1 2026 345/7/37(2026-10-21).
# FY2025 10-K는 위탁 생산 대기 멤버가 2025년 3분기 10-Q에 없어 4분기 값을 못 만든다(ignore 멤버도 검사에 걸림) — 2026년 분기 10-Q에는 있어 FY2026 10-K부터는 된다.
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {
  "mrna:COVID19Member": [
   "COVID 백신(Spikevax·mNEXSPIKE)",
   "#d71e28"
  ],
  "us-gaap:ProductAndServiceOtherMember": [
   "기타 매출(협력·위탁 생산 등)",
   "#9ca3af"
  ],
  "mrna:RSVMember": [
   "RSV 백신(mRESVIA)",
   "#e88a8f"
  ]
 },
 "ignore": [
  "mrna:ProductSalesMember",
  "mrna:StandReadyManufacturingMember",
  "mrna:CollaborationArrangementIncludingArrangementsWithAffiliateMember",
  "us-gaap:GrantMember",
  "mrna:LicenseAndRoyaltyMember"
 ]
}
