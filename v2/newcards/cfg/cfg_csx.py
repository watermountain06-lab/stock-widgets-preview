# CSX(CSX) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 126(시총 124위). 미국 동부 철도 화물.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-22), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 마감 뒤 접수), 8-K(CEO 교체 2025-09-28, CFO 교체 2025-10-29,
# 디지털·기술 총괄 퇴사 2026-05-14, COO 은퇴 2026-10-12), StockAnalysis.
# 엔진 입력(2026-10-18): 차입금 = LongTermDebtAndCapitalLeaseObligations(Current) 두 태그 — 기본 선택이 2012년에 멈춘 LongTermDebt($9,832M)를 잡았다
# (원문 $1,702M + $17,162M = $18,864M, DEBT_TOTAL_TAG). 현금 태그 2022 멈춤($1,958M) → 합계 태그($1,007M). 차입금에 금융리스가 있어 리스는 운용리스만.
# 감가상각: 손익계산서 줄 태그가 Depreciation(2022 10-Q까지) → DepreciationDepletionAndAmortization — 한 구성요소로 묶음(DDA_PARTS_BY_CIK, 새 태그 우선;
# 없으면 2021년 분기 공개일이 1년 뒤로 밀려 EV/EBITDA 이력이 921일). 3:1 분할(2021-06-29) KNOWN_SPLITS. 4분기 EPS 보도자료 값(2025 $0.39·2024 $0.38).
# 지분법 투자 $2.68B(TTX·Conrail 등)는 그 이익이 영업비용(장비 임차료)에서 빠지므로 영업 자산 — 비영업 자산에 더하지 않는다(엔진 기본).
# 리스: 운용리스 총액(유동 + 비유동) 태그는 10-K에만 있어 2025년 말 $546M을 쓴다(10-Q에는 비유동분 $493M만 — 유동분이 없어 총액을 만들지 않음, Codex).
CIK = '0000277948'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'CSX'
S_ = 'https://www.sec.gov/Archives/edgar/data/277948/'
SEC = S_
TENQ = S_ + '000027794826000032/csx-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000027794826000031/pressrelease_q22026.htm', 'q1': S_ + '000027794826000013/pressrelease_q12026.htm',
      'q4': S_ + '000027794826000003/pressrelease_q42025.htm', 'q3': S_ + '000027794825000053/pressrelease_q32025.htm'}
LINKS = {'coo': S_ + '000027794826000034/csx-20261012.htm', 'cdto': S_ + '000095010326007181/dp246573_8k.htm',
         'cfo': S_ + '000095010325013783/dp236450_8k.htm', 'ceo': S_ + '000095010325012355/dp234871_8k.htm'}
FAIRBAND_TITLE = 'id="csxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (20, 45)
ACT_REASON = ''
NONOP_WHAT = '장기투자'
PH = ['UNP', 'NSC', 'ODFL', 'JBHT', 'FDX', 'UPS']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '철도·화물 운송 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '철도·화물 운송 PBR 비교', 'psr': '철도·화물 운송 PSR 비교',
                'pcr': '철도·화물 운송 PCR(FCF) 비교', 'evebitda': '철도·화물 운송 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(CSX 제외)와 배수 순위를 매긴 값이다.',
            '기계·항공·운송·건설·업무 서비스 회사가 섞여 있다. 차트에는 철도·화물 운송 6곳만 보인다.')
# 매출(Q2 2026 10-Q 주석 8 품목별, 단일 회계 단위) — 일반 화물 2,446 + 인터모달 620 + 석탄 520 + 트럭 226 + 기타 123 = 3,935(연결 매출).
SEG = [('일반 화물', 2446, '#00467f'), ('인터모달', 620, '#4a7fb3'), ('석탄', 520, '#333f48'), ('트럭(Quality Carriers)', 226, '#8fb3dc'), ('기타', 123, '#9a9a9a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 품목별'
# 손 뉴스: 10/12 COO 은퇴(8-K 10/13)가 Q2 실적(7/22) 뒤라 Q2도 손으로 쓴다(README). 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K는 모두 20~21시 접수(장 마감 뒤) → 다음 거래일. COO 8-K 10/13 12:00(장중) → 10/13(보도자료는 10/12 자 — 시각 미표기),
# CDTO·자사주 8-K 5/14 13:30 → 5/14(같은 8-K의 5.02·8.01항 — 따로 적음, Fable), CFO 8-K 10/29 12:35 → 10/29, CEO 8-K 9/29 12:00 → 9/29(이사회 결정 9/28 일요일).
NEWS_RANGE = '2025.09 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 12일 — COO 은퇴 발표(보도 시각 미표기 · 등락은 8-K를 낸 10/13)', '2026-10-13',
     'Michael Cory 수석부사장·COO가 10월 12일 COO에서 물러남 · 전환 기간 자문을 맡고 2027년 5월 8일 퇴직(은퇴)', 'coo', 'CSX 공시 (SEC 8-K)'),
    ('green', '2026년 7월 22일 장 마감 뒤 — Q2 2026 실적', '2026-07-23',
     '매출 $3.94B(+10%, 분기 최대 — 유류 할증·물량·운임) · 희석 EPS $0.54(1년 전 $0.44)', 'q2', 'CSX 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 14일 — 자사주 매입 $5B 추가 승인', '2026-05-14',
     '5월 12일 이사회 결정 · 3월 말 남은 한도 약 $989M에 $5B를 더함', 'cdto', 'CSX 공시 (SEC 8-K)'),
    ('neutral', '2026년 5월 14일 — 디지털·기술 총괄 퇴사', '2026-05-14',
     'Stephen Fortune 수석부사장(최고 디지털·기술 책임자) 퇴사', 'cdto', 'CSX 공시 (SEC 8-K)'),
    ('green', '2026년 4월 22일 장 마감 뒤 — Q1 2026 실적', '2026-04-23',
     '매출 $3.48B(+2%) · 희석 EPS $0.43(1년 전 $0.34)', 'q1', 'CSX 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 22일 장 마감 뒤 — Q4 2025 실적', '2026-01-23',
     '매출 $3.51B(−1%) · 희석 EPS $0.39(1년 전 $0.38) · 인력 감축·기술 투자 정리 비용 약 $50M 포함 · 2025년 매출 $14.09B·EPS $1.54', 'q4', 'CSX 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 29일 — CFO 교체', '2025-10-29',
     '최고상업책임자 Kevin Boone이 CFO로(즉시) · Sean Pelkey 퇴사', 'cfo', 'CSX 공시 (SEC 8-K)'),
    ('red', '2025년 10월 16일 장 마감 뒤 — Q3 2025 실적', '2025-10-17',
     '매출 $3.59B(−1%) · 희석 EPS $0.37(1년 전 $0.46) · 비현금 영업권 손상 $164M 포함', 'q3', 'CSX 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 9월 28일 — CEO 교체', '2025-09-29',
     '이사회가 Stephen Angel을 사장·CEO로 선임(Joseph Hinrichs 후임)', 'ceo', 'CSX 공시 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 25, 'nt': 22, 'mean': 52.73, 'median': 54, 'low': 32, 'high': 60, 'sb': 13, 'b': 4, 'h': 6, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-18'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 일반 화물 소계 아래 7품목은 ignore(소계에 포함).
# 원문 대조: 10-Q 주석 8 Q2 2026 2,446/620/520/226/123, 1년 전 2,257/491/477/211/138 = 연결 매출(2026-10-18) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {
  "csx:TotalMerchandiseMember": ["일반 화물", "#00467f"],
  "csx:IntermodalMember": ["인터모달", "#4a7fb3"],
  "csx:CoalServicesMember": ["석탄", "#333f48"],
  "csx:TruckingMember": ["트럭(Quality Carriers)", "#8fb3dc"],
  "csx:OtherServicesMember": ["기타", "#9a9a9a"]
 },
 "ignore": [
  "csx:ChemicalsMember", "csx:AgriculturalandFoodProductsMember", "csx:AutomotiveMember", "csx:ForestProductsMember",
  "csx:MetalsandEquipmentMember", "csx:MineralsMember", "csx:FertilizersMember"
 ]
}
