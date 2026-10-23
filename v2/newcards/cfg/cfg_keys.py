# KEYS(키사이트) v2 카드 설정 — 자동 카드(AUTO). 회계연도 10월 31일. 카드 순위 179. 전자 계측 장비·설계 소프트웨어 — 통신 솔루션(CSG), 전자 산업 솔루션(EISG).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-09-02 장 마감 뒤 접수), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 모두 장 마감 뒤), 8-K(Spirent·OSG·PowerArtist 인수 완료 2025-10), StockAnalysis.
# 엔진 입력(2026-10-23): 차입금 = 1년 안 700 + 장기 1,817 = $2,517M(엔진 값 = 원문), 이자비용 InterestExpenseNonoperating(CONCEPTS_BY_CIK), 인수 대금 $1,653M(build_dcf ACQ_FIXED — Viavi 매각 $399M 차감).
# 4분기 EPS FY2021·2023·2024·2025는 보도자료 값(Q4_EPS_OVERRIDE). 2025-10 Spirent·Synopsys 광학 솔루션(OSG)·PowerArtist 인수 — FY26 매출 증가에 인수분이 섞인다.
CIK = '0001601046'
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-10-31', '2024-10-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Keysight'
S_ = 'https://www.sec.gov/Archives/edgar/data/1601046/'
SEC = S_
TENQ = S_ + '000160104626000036/keys-20260731.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000160104626000029/exhibit991-q326pressrelease.htm', 'q2': S_ + '000160104626000019/exhibit991-q226pressrelease.htm',
      'q1': S_ + '000160104626000003/exhibit991-q126pressrelease.htm', 'q4': S_ + '000160104625000121/exhibit991-q425pressrelease.htm'}
LINKS = {'spirent': 'https://s22.q4cdn.com/444849635/files/doc_news/Keysight-Technologies-Completes-Acquisition-of-Spirent-Communications-PLC-2025.pdf'}
FAIRBAND_TITLE = 'id="keysFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 70)
ACT_REASON = ''
NONOP_WHAT = '장기 투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('2025년 10월 Spirent와 두 사업(Synopsys 광학 솔루션·PowerArtist)을 인수해 이번 회계연도 매출 증가에 인수분이 섞여 있다(Q3 매출 증가 가운데 인수 기여는 약 6%p) — 인수한 회사의 무형자산 상각 때문에 GAAP 이익이 회사가 발표하는 조정 이익보다 작다. '
              '현금흐름 모델은 최근 4분기 인수 대금(Viavi에 판 사업 대금을 뺀 값)을 재투자로 세고, 낮은 2년 중앙 이익률과 21% 세율로 수렴해 내재가치가 현재가보다 크게 낮게 나온다. '
              '최근 4분기 이익에는 2분기 관세 환급(영업이익 약 $57M)과 1분기 세금 환입 같은 일회성 항목이 들어 있다.')
PH = ['APH', 'TXN', 'CSCO', 'ANET', 'QCOM', 'DELL']   # 비교 자료(카드 유니버스 IT)에 값이 있는 종목만
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '전자 부품·하드웨어·반도체 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(KEYS 제외)과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 섞여 있다. 차트에는 전자 부품·하드웨어·반도체 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 부문) — 통신 솔루션 1,345 + 전자 산업 솔루션 501 = 1,846(= 총매출). 1년 전 940·412.
SEG = [('통신 솔루션(CSG)', 1345.0, '#e90029'), ('전자 산업 솔루션(EISG)', 501.0, '#f2667f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다), 인수 완료.
# 반응일: 실적 8-K 2025-11-25T02:08Z·2026-02-24T02:08Z·05-20T00:08Z·08-19T00:09Z = 전날 장 마감 뒤(동부 저녁) → 다음 세션. Spirent 완료 10/15(회사 발표 — 영국 거래, 미국 장 전), OSG·PowerArtist 10/17, 10/20 8-K는 설명자료(7.01).
# 다음 실적: 회사 공지 전(과거 Q4 발표일 요일 불규칙) — 카드 날짜는 추정.
# 넣지 않은 8-K: 이사·임원(11/20·3/12·8/26), 주총(3/19), 신용약정(4/21). 10/22 −8.7%는 1차 자료 없음(같은 날 반도체·장비 종목 동반 하락).
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('red', '2026년 8월 18일 — Q3 FY26 실적', '2026-08-19',
     '매출 $1.85B(1년 전 $1.35B, 인수 기여 약 6%p) · GAAP 순이익 $397M · 희석 EPS $2.30(1년 전 $1.10)', 'q3', 'Keysight 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 19일 — Q2 FY26 실적', '2026-05-20',
     '매출 $1.72B(1년 전 $1.31B) · GAAP 순이익 $349M · 희석 EPS $2.02(1년 전 $1.49) · 10-Q: 무효 판결 난 관세(IEEPA) 환급 인식으로 영업이익 약 $57M 일회성 증가', 'q2', 'Keysight 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 23일 — Q1 FY26 실적', '2026-02-24',
     '매출 $1.60B(1년 전 $1.30B) · GAAP 순이익 $281M · 희석 EPS $1.63(1년 전 $0.97) — 세전이익은 1년 전과 비슷하고 증가분은 법인세 환입 등 세금 효과', 'q1', 'Keysight 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 24일 — Q4 FY25 실적 · 자사주 $1.5B', '2025-11-25',
     '매출 $1.42B(1년 전 $1.29B) · GAAP 순이익 $229M · 희석 EPS $1.33(1년 전 −$0.42 — 그 분기 일회성 세금 비용) · 자사주 매입 $1.5B 새 프로그램', 'q4', 'Keysight 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 15일 — Spirent 인수 완료', '2025-10-15',
     '통신 시험 회사 Spirent 인수 마무리(일부 사업은 Viavi에 $399M에 매각) — 10/17에는 Synopsys 광학 솔루션 사업(OSG)·PowerArtist 인수도 완료', 'spirent', 'Keysight 보도자료'),
]
ANALYST = {'rating': 'Buy', 'n': 12, 'nt': 10, 'mean': 426.6, 'median': 425, 'low': 400, 'high': 487, 'sb': 7, 'b': 3, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 부문 2개(수동 지도). 원문 대조: Q3 FY26 1,345/501(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"keys:CommunicationsSolutionsGroupMember": ["통신 솔루션(CSG)", "#e90029"], "keys:ElectronicIndustrialSolutionsGroupMember": ["전자 산업 솔루션(EISG)", "#f2667f"]},
 "ignore": []
}
