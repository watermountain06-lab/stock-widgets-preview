# NDSN(노드슨) v2 카드 설정 — 자동 카드(AUTO). 회계연도 10월 31일(FY2026 = 2025-11~2026-10). 정밀 디스펜싱·코팅·접착 장비(IPS), 의료용 유체 부품(MFS), 반도체·전자 검사·디스펜싱 장비(ATS).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-08-20), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/NDSN.md.
# 엔진 입력(2026-10-25): 기본 경로 — 차입금 LongTermDebt $1,731.0M(기업어음 $192M·1년 안 $10M 포함 합계), 현금 $113.4M.
# D&A = 감가상각 + 무형자산 상각(DDA_PARTS_BY_CIK — 10-K 합산 태그에 상각만 실린 해가 있어 4분기가 음수였다; FY21~24 합 일치).
# 일회성: Q1 소수 지분 투자 평가이익(세후 $16.7M), Q2 연금 일부 이전 정산 손실(세전 $24.0M)·투자 평가손실 — 9개월 순 세후 −$20.6M(최근 4분기 EPS의 약 4%).
CIK = '0000072331'
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-10-31', '2024-10-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Nordson'
S_ = 'https://www.sec.gov/Archives/edgar/data/72331/'
SEC = S_
TENQ = S_ + '000007233126000054/ndsn-20260731.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000007233126000052/ndsn-q320268kxex991.htm', 'q2': S_ + '000007233126000022/ndsn-q220268kxex991.htm',
      'q1': S_ + '000007233126000011/ndsn-q120268kxex991.htm', 'q4': S_ + '000007233125000138/ndsn-20251213xex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="ndsnFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 35)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('반도체·전자 장비(ATS) 매출이 업황에 따라 크게 오르내린다 — Q3 FY26에 1년 전보다 28% 늘었다. 소수 지분 기술 투자의 평가손익이 분기 이익을 흔든다 — 최근 4분기 순 일회성(세후 약 −$21M)을 빼도 자기 이력 점수는 약 28로 30에 못 미친다. '
              '10월 23일 스위스 센서 회사 Contrinex(기업가치 약 $168M) 인수를 끝냈는데, 7월 말 재무상태표 뒤라 카드에 없다.')
PH = ['ITW', 'DOV', 'IEX', 'IR', 'PH', 'GWW']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '산업 기계 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(NDSN 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 산업 기계 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 부문) — 산업 정밀 367.2 + 의료·유체 230.5 + 첨단 기술 219.9 = 817.6(반올림, 총 817.7).
SEG = [('산업 정밀 솔루션', 367.2, '#0067a5'), ('의료·유체 시스템', 230.5, '#5aa0d0'), ('첨단 기술(반도체·전자)', 219.9, '#7a7a7a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:31~16:34 동부 접수) → 다음 거래일. 넣지 않은 8-K: 임원 퇴직 정책, 신용 계약, 기업어음 프로그램, 주총, Contrinex 인수 완료(10/23).
NEWS_RANGE = '2025.12 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 19일 장 마감 뒤 — Q3 FY26 실적', '2026-08-20',
     '매출 $818M(+10%) · 순이익 $153M · 희석 EPS $2.73(1년 전 $2.22) — 다음 날 주가 +8%', 'q3', 'Nordson 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 20일 장 마감 뒤 — Q2 FY26 실적', '2026-05-21',
     '매출 $741M · 순이익 $117M · 희석 EPS $2.09(1년 전 $1.97) — 연금 정산 손실 세전 $24M 포함', 'q2', 'Nordson 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 18일 장 마감 뒤 — Q1 FY26 실적', '2026-02-19',
     '매출 $670M · 순이익 $133M · 희석 EPS $2.38(1년 전 $1.65) — 투자 평가이익 세후 $16.7M 포함', 'q1', 'Nordson 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 10일 장 마감 뒤 — Q4 FY25 실적', '2025-12-11',
     '매출 $752M · 순이익 $152M · 희석 EPS $2.69(1년 전 $2.12) · FY2025 EPS $8.51', 'q4', 'Nordson 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 7, 'nt': 4, 'mean': 364, 'median': 370, 'low': 351, 'high': 375, 'sb': 4, 'b': 0, 'h': 2, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 3개(수동 지도, 영업 부문 차원). 원문 대조: Q3 FY26 367.2/230.5/219.9(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"ndsn:IndustrialPrecisionsSolutionsMember": ["산업 정밀 솔루션", "#0067a5"], "ndsn:MedicalFluidSystemsMember": ["의료·유체 시스템", "#5aa0d0"],
             "ndsn:AdvancedTechnologySystemsMember": ["첨단 기술(반도체·전자)", "#7a7a7a"]},
 "ignore": []
}
