# SNPS(시놉시스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 10월 말(Q3 FY26 = 2026-05~07). 카드 순위 136(시총 134위). 반도체 설계 자동화(EDA)·설계 IP, 공학 시뮬레이션(Ansys, 2025-07-17 인수).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-08-26), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 모두 장 마감 뒤 접수), 8-K(구조조정 2025-11-12, NVIDIA 지분 투자 2025-12-01,
# 자사주 가속 매입 2026-03-02·10-05, Elliott 협력 합의 2026-05-27), StockAnalysis.
# 엔진 입력(2026-10-21): 차입금 $10,037M(1년 안 $1,020 + 장기 $9,017)·현금 $3,606M·자본 $31,153M = 원문. 최근 4분기에 Ansys가 모두 들어 있고, 인수 대금은 그 창 밖(2025년 7월)이라 인수 대금 0.
# 본업 기준(core_earnings.json): 최근 4분기 세전이익이 영업이익보다 62% 많다 — Q3 FY26 Processor IP 매각 이익 $425.4M(영업외). PER·적정주가·순이익률은 본업 이익으로.
# 4분기 EPS: FY25 2.39·FY24 1.79(계속사업, 보도자료 — FY24 역산 7.13에는 소프트웨어 보안 사업 매각 이익이 든 중단사업이 섞였다).
CIK = '0000883241'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-10-31', '2024-10-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Synopsys'
S_ = 'https://www.sec.gov/Archives/edgar/data/883241/'
SEC = S_
TENQ = S_ + '000088324126000025/snps-20260731.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000119312526368620/d157153dex991.htm', 'q2': S_ + '000119312526241911/d126227dex991.htm',
      'q1': S_ + '000119312526071601/d921168dex991.htm', 'q4': S_ + '000119312525314200/d29055dex991.htm'}
LINKS = {'iday': 'https://news.synopsys.com/2026-09-30-Synopsys-Details-Growth-Strategy-and-Long-term-Financial-Model-at-2026-Investor-Day', 'asr_oct': S_ + '000119312526413359/d830308dex991.htm', 'elliott': S_ + '000119312526241920/d96543dex991.htm',
         'asr_mar': S_ + '000119312526084396/d113900d8k.htm', 'nvda': S_ + '000119312525303209/d36680dex991.htm',
         'restr': S_ + '000119312525276232/d48382d8k.htm'}
FAIRBAND_TITLE = 'id="snpsFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 본업 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 60)
ACT_REASON = ''
NONOP_WHAT = '장기 투자'
# 고정 문장(숫자 없음). Ansys 인수가 모델·배수·성장률에 미치는 영향(Codex·Fable 2026-10-21 — 상각 뒤 이익과 FCF의 차이, 인수 매출이 섞인 성장률, 인수 전과 섞인 자기 이력).
MODEL_NOTE = ('Ansys 인수로 투하자본의 큰 몫이 영업권과 인수 무형자산이고, 인수 무형자산 상각(현금이 나가지 않는 비용)이 GAAP 영업이익을 누른다 — 본업 EPS·PER·적정주가는 '
              '상각 뒤 영업이익 기준이라 FCF보다 훨씬 작은 이익을 보고, 그래서 PER이 매우 높게 나온다. 현금흐름 내재가치는 그 낮은 이익률에 큰 투하자본에 맞춘 재투자 부담과 순차입금 차감이 더해져 음수다. '
              '과거 매출 성장률과 분기 증가율에는 인수로 더해진 매출이 들어 있고, 인수 뒤 한 해가 온전히 지난 분기부터는 전년 같은 분기에도 Ansys 실적이 온전히 포함되어 보고 증가율이 크게 낮아질 수 있다. '
              '자기 이력의 PBR·PSR·EV/EBITDA 분포에는 인수 전 기간이 섞여 있어, 상각에 눌린 PER과 방향이 다르게 나온다.')
PH = ['CRM', 'MSFT', 'ORCL', 'PANW', 'IBM', 'CRWD']   # INTU는 카드 유니버스 배수 날짜가 비어 fill.py가 멈춘다. CDNS는 카드 없음(보류), ADBE는 카드 유니버스 배수 값이 없어 fill.py가 멈춘다(INTU 때 확인)
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소프트웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': '소프트웨어 PBR 비교', 'psr': '소프트웨어 PSR 비교',
                'pcr': '소프트웨어 PCR(FCF) 비교', 'evebitda': '소프트웨어 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(SNPS 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 소프트웨어 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 부문 — Design Automation(Ansys 포함) 2,003.0 + Design IP 473.8 = 2,476.8. 1년 전 1,312.1·427.6 → 1,739.7). Ansys 분기 기여 $622.2M(10-Q).
SEG = [('설계 자동화(EDA·Ansys)', 2003.0, '#5a2d82'), ('설계 IP', 473.8, '#a888d4')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 보고 부문별'
# 손 뉴스: 최신 실적(Q3 FY26, 8/26 장 마감 뒤)도 손으로 쓴다 — 그 뒤 손 항목(10/5 자사주 $1B)이 있으면 자동 항목이 빠진다. Q4 FY26 실적부터 다시 자동. 가이던스·비GAAP EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 자사주 8-K 10/5 17:21 → 10/5, Q3 8/27 00:21(=8/26 20:21) → 8/27, Q2·Elliott 5/28 00:13·00:15(=5/27 20시) → 5/28,
# 자사주 3/2 19:15 → 3/2, Q1 2/26 02:15(=2/25 21:15) → 2/26, Q4 FY25 12/11 02:12(=12/10 21:12) → 12/11, NVIDIA 12/1 18:49 → 12/1, 구조조정 11/12 19:15 → 11/12.
# 투자자의 날 9/30: 8-K 없음 — 회사 보도자료(PR Newswire, 시각 미표시) → 9/30. 가이던스(FY27 매출 목표)는 쓰지 않는다.
# 넣지 않은 8-K: 임원(11/4 CRO·2/19 이사·8/12 법무 책임자), 주총(4/20).
NEWS_RANGE = '2025.11 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 5일 — 자사주 $1B 가속 매입(ASR)', '2026-10-05',
     'JPMorgan과 $1B 가속 매입 계약 · 첫 인도 약 173.5만 주, 나머지는 2027년 1월 5일까지 정산', 'asr_oct', 'Synopsys 보도자료 (SEC 8-K)'),
    ('green', '2026년 9월 30일 — 투자자의 날: Amazon IP 계약 · OpenAI 협력', '2026-09-30',
     'Amazon과 맞춤형 반도체 IP 계약, OpenAI와 칩 설계 특화 모델 GPT-Synopsys를 함께 개발하는 선호 파트너 관계 · 응용 최적화 IP(AOIP)로 확장 · 잉여현금흐름의 최대 50%를 자사주 매입에 쓰고 수개월 안에 약 $1B 매입 예정 · 발표 시각 미표시, SEC 공시 없음', 'iday', 'Synopsys 보도자료 (PR Newswire)'),
    ('green', '2026년 8월 26일 장 마감 뒤 — Q3 FY26 실적', '2026-08-27',
     '매출 $2.48B(+42%, Ansys 기여 $622M) · 희석 EPS $2.84(1년 전 $1.50) · Processor IP 매각 이익 $425.4M 포함(10-Q, 6월 1일 GlobalFoundries에 매각) · 8월 이사회가 구조조정 비용 전망을 $425M~$500M으로 올림(FY2027 말 완료 예정, 10-Q)', 'q3', 'Synopsys 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 27일 장 마감 뒤 — Q2 FY26 실적 · Elliott 협력 합의', '2026-05-28',
     '매출 $2.28B(+42%) · 희석 EPS $0.09(1년 전 계속사업 $2.24) · 같은 날 행동주의 펀드 Elliott과 협력 합의, Jesse Cohn을 6월 1일부터 이사로', 'q2', 'Synopsys 실적 보도자료·공시 (SEC 8-K)'),
    ('green', '2026년 3월 2일 — 자사주 $250M 가속 매입(ASR)', '2026-03-02',
     'Bank of Nova Scotia와 $250M 가속 매입 계약 · 2월 25일 자사주 매입 한도 $2.0B로 다시 채움', 'asr_mar', 'Synopsys 공시 (SEC 8-K)'),
    ('neutral', '2026년 2월 25일 장 마감 뒤 — Q1 FY26 실적', '2026-02-26',
     '매출 $2.41B(+66%) · 희석 EPS $0.34(1년 전 $1.89) · 인수 무형자산 상각·구조조정 비용이 GAAP 이익을 누름(보도자료 조정표)', 'q1', 'Synopsys 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 10일 장 마감 뒤 — Q4 FY25 실적', '2025-12-11',
     '매출 $2.26B(+38%, Ansys 기여 $668M) · 계속사업 희석 EPS $2.39(1년 전 $1.79) · FY2025 매출 $7.05B(+15%)·EPS $8.07', 'q4', 'Synopsys 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 1일 — NVIDIA $2B 지분 투자', '2025-12-01',
     'NVIDIA가 Synopsys 보통주 4,821,717주를 주당 $414.79에 사들임(총 $2B, 사모) · GPU 가속 설계·시뮬레이션 협력 확대', 'nvda', 'Synopsys·NVIDIA 공동 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 12일 — 구조조정: 인력 약 10% 감축', '2025-11-12',
     'Ansys 인수 뒤 효율화 · 세전 비용 $300M~$350M 예상(2026년 8월 $425M~$500M으로 상향) · 인력 감축 대부분은 FY2026에', 'restr', 'Synopsys 공시 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Strong Buy', 'n': 25, 'nt': 18, 'mean': 588.44, 'median': 600, 'low': 420, 'high': 700, 'sb': 20, 'b': 4, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-21'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(보고 부문 축 2개). 원문 대조: Q3 FY26 2,003.0/473.8, 1년 전 1,312.1/427.6(2026-10-21) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "snps:DesignAutomationSegmentMember": [
   "설계 자동화(EDA·Ansys)",
   "#5a2d82"
  ],
  "snps:DesignIPSegmentMember": [
   "설계 IP",
   "#a888d4"
  ]
 },
 "ignore": []
}
