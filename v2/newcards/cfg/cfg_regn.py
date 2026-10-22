# REGN(리제네론) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 144(시총 142위). 바이오의약품(Dupixent — Sanofi 협업, Eylea·Eylea HD, Libtayo).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장중 접수, 보도자료는 장 전), 8-K(Sanofi 협업 확대 2026-10-06 접수), StockAnalysis.
# 엔진 입력(2026-10-21): 주식 수는 표지 값(보통주 + Class A 1.82M = 102.95M, cover_shares — companyfacts 주식 수 태그는 2012년에 멈춤). 차입금 $1,986.6M(사채),
# 금융리스 $720.0M(차입금과 별도 줄, 2026년에 1년 안 만기로 이동), 현금 $2,455.8M + 단기 시장성 증권 $5,538.8M, 장기 시장성 증권 $9,828.3M은 비영업 자산.
# 4분기 EPS 2022~2025 보도자료 값. 분기 이익에 IPR&D(계약금·마일스톤) 비용이 섞인다(Q2 주당 $1.02).
BUILD = {'cover_shares': True}
CIK = '0000872589'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -1), '적정~고평가'
CO = 'Regeneron'
S_ = 'https://www.sec.gov/Archives/edgar/data/872589/'
SEC = S_
TENQ = S_ + '000087258926000025/regn-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000087258926000023/exhibit991q22026.htm', 'q1': S_ + '000087258926000014/exhibit991q12026.htm',
      'q4': S_ + '000087258926000004/exhibit991q42025.htm', 'q3': S_ + '000087258925000026/exhibit991q32025.htm'}
LINKS = {'psu': 'https://www.sec.gov/Archives/edgar/data/872589/000110465926112340/tm2626090d1_8k.htm',
         'pasatru': 'https://www.goodwinlaw.com/en/insights/blogs/2026/08/fda-approves-regenerons-pasatru-garetosmabgrts-for-fibrodysplasia-ossificans-progressiva',
         'fian': 'https://fiercebiotech.com/biotech/regeneron-rocked-failure-defining-catalyst-pivotal-melanoma-trial-misses',
         'sanofi': 'https://www.sec.gov/Archives/edgar/data/872589/000110465926113895/tm2627077d1_8k.htm'}
FAIRBAND_TITLE = 'id="regnFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 50)
ACT_REASON = ''
NONOP_WHAT = '장기 시장성 증권·비상장 지분'
# 고정 문장(숫자 없음). 협업 매출 구조, Eylea 경쟁, IPR&D 비용, 대규모 증권 보유.
MODEL_NOTE = ('매출의 큰 몫은 Sanofi와 이익을 나누는 Dupixent에서 받는 협업 매출이다 — Sanofi에 갚던 개발비 잔액이 다 갚아져 앞으로는 그 차감이 없어지는데, '
              '과거 이익률에서 출발하는 이 모델에는 그 변화가 들어 있지 않다. 직접 파는 Eylea는 바이오시밀러 경쟁과 고용량 제품 전환·가격 하락으로 줄고 있다. '
              '분기 이익에는 신약 계약금·마일스톤 같은 IPR&D 비용이 섞여 크게 흔들린다. 보유한 장기 시장성 증권·비상장 지분은 사업 가치와 따로 더한다.')   # Codex·Fable r1
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-30', 'src': '9/24 회사 공지 — 장 시작 전 발표, 콜 오전 8시 30분(동부)'}
PH = ['LLY', 'ABBV', 'VRTX', 'AMGN', 'GILD', 'BMY']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '대형 제약·바이오 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': '제약·바이오 PBR 비교', 'psr': '제약·바이오 PSR 비교',
                'pcr': '제약·바이오 PCR(FCF) 비교', 'evebitda': '제약·바이오 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(REGN 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·유통이 섞여 있다. 차트에는 대형 제약·바이오 6곳만 보인다.')
# 매출(Q2 2026 10-Q 손익계산서) — 제품 매출 1,642.4 + 협업 매출 2,455.0 + 기타 193.3 = 4,290.7. 1년 전 1,631.0/1,860.7/183.9 → 3,675.6.
SEG = [('협업 매출(Sanofi·Bayer)', 2455.0, '#0b5e9e'), ('제품 매출(Eylea·Libtayo 등)', 1642.4, '#4d93cf'), ('기타', 193.3, '#a9cbe8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 수익 종류별'
# 손 뉴스: 최신 실적(Q2 2026, 7/30)도 손으로 — 뒤에 10/1 Sanofi 계약이 있다. 가이던스·비GAAP EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부, 날짜도 UTC 값): 실적 8-K 2025-10-28T14:50Z·2026-01-30T16:51Z·04-29T14:50Z·07-30T14:48Z = 장중 접수(보도자료 장 전) → 같은 날.
# Sanofi 계약은 회사 발표 10/1(8-K는 10/6T15:51Z 접수) → 10/1.
# CEO·CSO 성과주식 8-K 2026-10-01T00:14Z = 9/30 20:14 → 10/1(Fable 필수). 회사 발표만 있는 사건: fianlimab 3상(5/15 금 오후 8시 19분 → 5/18), Pasatru 승인(8/19 오후 1시 58분 → 8/19)(Codex 필수).
# 넣지 않은 8-K: IPR&D 비용 사전 안내(2.02항 10/6·4/8·7/6·2025-10-06), JPM 학회 발언(1/12), 주총(6/18).
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 9월 30일 장 마감 뒤 — CEO·CSO 10년 성과주식 부여', '2026-10-01',
     '공동 창업자 두 명에게 한 번만 주는 10년 성과 연동 주식 — 상한 270만 주 + 290만 주(발행 주식의 약 5.4%) · 같은 날 Sanofi 발표와 반응이 섞인다', 'psu', 'Regeneron 공시 (SEC 8-K)'),
    ('green', '2026년 10월 1일 — Sanofi와 협업 확대(새 항체 4종)', '2026-10-01',
     'Sanofi가 계약금 $1.0B를 내고 개발·허가·판매 마일스톤으로 최대 $7.0B 추가, 이익은 반씩 · Dupixent 정보 접근 소송은 취하(8-K는 10/6 접수)', 'sanofi', 'Regeneron 공시 (SEC 8-K)'),
    ('green', '2026년 8월 19일 — Pasatru FDA 승인', '2026-08-19',
     '희귀 골질환(FOP) 성인 치료제(garetosmab) 승인 — FOP 치료제로는 두 번째(FDA) · 8-K 없음', 'pasatru', 'Goodwin Big Molecule Watch'),
    ('green', '2026년 7월 30일 — Q2 2026 실적', '2026-07-30',
     '매출 $4.29B(+17%) · 희석 EPS $12.23(1년 전 $12.81 — IPR&D 비용 주당 $1.02) · Dupixent 세계 매출 $6.0B(+38%) · Eylea HD 미국 $596M(+52%) · Sanofi 개발비 잔액 상환 완료', 'q2', 'Regeneron 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 15일 금요일 장 마감 뒤 — fianlimab 흑색종 3상 주요 평가변수 미달', '2026-05-18',
     'fianlimab + Libtayo 고용량군이 Keytruda 대비 무진행 생존을 통계적으로 유의하게 늘리지 못했다 — 8-K 없음', 'fian', 'Fierce Biotech'),
    ('red', '2026년 4월 29일 — Q1 2026 실적', '2026-04-29',
     '매출 $3.61B(+19%) · 희석 EPS $6.75(1년 전 $7.27 — IPR&D 비용 주당 $0.82) · 미국 Eylea 전체 −10% · 자사주 $3.0B 새 승인', 'q1', 'Regeneron 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 30일 — Q4 2025 실적', '2026-01-30',
     '매출 $3.88B(+3%) · 희석 EPS $7.86(1년 전 $8.06) · 2025년 매출 $14.34B·EPS $41.48 · 미국 Eylea 전체 2025년 −27%', 'q4', 'Regeneron 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 28일 — Q3 2025 실적', '2025-10-28',
     '매출 $3.75B(+1%) · 희석 EPS $13.62(1년 전 $11.54) · Dupixent 세계 매출 $4.86B(+27%) · 미국 Eylea 전체 −28%', 'q3', 'Regeneron 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 28, 'nt': 26, 'mean': 862.35, 'median': 865, 'low': 740, 'high': 1030, 'sb': 15, 'b': 4, 'h': 8, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-21'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(수익 종류 3개, 제품별 멤버는 ignore). 원문 대조: Q2 2026 2,455.0/1,642.4/193.3, 1년 전 1,860.7/1,631.0/183.9(2026-10-21) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {
  "regn:CollaborationRevenueMember": [
   "협업 매출(Sanofi·Bayer)",
   "#0b5e9e"
  ],
  "us-gaap:ProductMember": [
   "제품 매출(Eylea·Libtayo 등)",
   "#4d93cf"
  ],
  "us-gaap:ProductAndServiceOtherMember": [
   "기타",
   "#a9cbe8"
  ]
 },
 "ignore": [
  "regn:LIBTAYONetProductSalesMember",
  "regn:LynozyficMember",
  "regn:OtherProductsMember"
 ]
}
