# CTAS(신타스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 5월 31일(FY27 = 2026-06 ~ 2027-05). 카드 순위 150(시총 148위). 유니폼 대여·세탁, 구급·안전 용품, 방화 서비스.
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-10-07), 실적 보도자료(Q1~Q4 FY26, Q1 FY27 — 8-K 2.02항 장중 접수, 보도자료는 장 전), 8-K(UniFirst 제안 2025-12-22·합병 계약 2026-03-11·FTC 2차 자료 요청 6/12·FTC 시기 합의 10/6), StockAnalysis.
# 엔진 입력(2026-10-22): 감가상각 이력 = 현금흐름표 Depreciation + "Amortization"(DDA_PARTS_BY_CIK — 합산 태그는 분기 행이 듬성듬성해 EV/EBITDA 이력이 138일뿐이었다).
# 차입금 $2,428.8M(1년 안 $999.3M + 장기 $1,429.6M) · 현금 $243.6M = 원문. 4-for-1 분할 2024-09-12(KNOWN_SPLITS). 4분기 EPS FY23~FY25 보도자료 값.
# 투자 $448.9M(Investments)은 회사 설명상 주로 보험 해약환급금(10-K 회계정책). 관련 이연보상 부채의 금액·대응 관계는 원문에서 확인하지 못했다
# (추정 단서: 이연법인세자산 "Deferred compensation and other" $132.1M — 기타 항목 포함). 양쪽을 따로 조정하지 않는 단순화 가정. 자산만 더하면 주당 약 +$1.13(Codex r1·r2).
# UniFirst 인수(주당 현금 $155 + CTAS 0.7720주, 기업가치 약 $5.5B)는 미완료 — FTC와 12/11 전에는 완료하지 않기로 합의(10/6 8-K). 카드 숫자에는 반영 안 됨.
BUILD = {}
CIK = '0000723254'
CUR, YO, QO = '2026-08-31', '2025-08-31', '2026-05-31'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-05-31', '2025-05-31'), 'FY26'
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Cintas'
S_ = 'https://www.sec.gov/Archives/edgar/data/723254/'
SEC = S_
TENQ = S_ + '000072325426000047/ctas-20260831.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000072325426000044/ex992026-8x31.htm', 'q4': S_ + '000072325426000025/ex992026-5x31.htm',
      'q3': S_ + '000072325426000006/ex992026-2x28.htm', 'q2': S_ + '000072325425000038/ex992025-11x30.htm'}
LINKS = {'unf_prop': 'https://www.sec.gov/Archives/edgar/data/723254/000095010325016413/dp239029_ex9901.htm',
         'unf_deal': 'https://www.sec.gov/Archives/edgar/data/723254/000095010326003567/dp243132_ex9901.htm',
         'ftc2': S_ + '000095010326008890/dp248355_8k.htm', 'ftc_time': S_ + '000095010326015293/dp254677_8k.htm'}
FAIRBAND_TITLE = 'id="ctasFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 대기 중인 UniFirst 인수, 높은 배수의 이력.
MODEL_NOTE = ('대기 중인 UniFirst 인수(현금과 주식 지급)는 완료 전이라 UniFirst 실적·인수 대금 조달·신주 발행이 매출·차입금·주식 수에 들어 있지 않다(이미 쓴 거래 비용은 영업이익에 들어 있다). '
              '투자자산은 주로 보험 해약환급금인데, 관련 이연보상 부채의 금액·대응 관계를 확인하지 못해 양쪽 모두 내재가치에서 따로 조정하지 않았다(단순화 가정). 이 회사는 5년 내내 높은 배수에서 거래돼 자기 이력의 중간도 시장 평균보다 비싸다.')   # Codex r1
PH = ['ADP', 'PAYX', 'WM', 'RSG', 'ROL', 'FAST']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '사업 서비스 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(CTAS 제외)와 배수 순위를 매긴 값이다.',
            '항공우주·기계·운송·건설이 섞여 있다. 차트에는 기업 대상 반복 서비스 회사 6곳만 보인다.')
# 매출(Q1 FY27 10-Q 서비스별) — 유니폼 대여·시설 2,294.7 + 구급·안전 388.5 + 방화 252.3 + 유니폼 직판 78.4 = 3,014.0. 1년 전 2,091.1/334.7/221.9/70.5 → 2,718.1.
SEG = [('유니폼 대여·시설 서비스', 2294.7, '#0b4ea2'), ('구급·안전 서비스', 388.5, '#5b8fd6'), ('방화 서비스', 252.3, '#e4572e'), ('유니폼 직판', 78.4, '#a9c4ea')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 서비스별'
# 손 뉴스: 최신 실적(Q1 FY27, 9/23)도 손으로 — UniFirst 거래 비용을 적으려고. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K 모두 16:31Z 전후 = 12:31 동부 장중 접수, 보도자료는 그날 아침 → 같은 날.
# UniFirst: 제안 공개 보도자료 12/22(8-K 접수 22:30Z = 17:30 동부, 12/22 주가 +2.36%), 합병 계약 3/11(8-K 14:39Z = 10:39 동부, 보도자료 3/11).
# FTC 2차 자료 요청 8-K 6/12 16:01Z → 6/12. FTC 시기 합의 8-K 10/7T01:22Z = 10/6 21:22 → 10/7.
# 넣지 않은 8-K: 사장 겸 COO 선임(8/3), 이사 불출마(8/27), 신용 약정(3/31), 주총(10/31).
NEWS_RANGE = '2025.12 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 6일 장 마감 뒤 — UniFirst 인수, FTC와 시기 합의', '2026-10-07',
     'FTC 2차 자료 요청에 응했다고 10월 2일 인증하고, FTC가 조사를 먼저 끝내지 않으면 12월 11일 전에는 완료하지 않기로 합의 · 캐나다 경쟁국 추가 자료도 9월 29일 제출 · 회사는 연내 완료를 예상', 'ftc_time', 'Cintas 공시 (SEC 8-K)'),
    ('green', '2026년 9월 23일 — Q1 FY27 실적', '2026-09-23',
     '매출 $3.01B(+10.9%, 인수·환율·영업일 수를 뺀 유기적 +8.9%) · 희석 EPS $1.36(1년 전 $1.20) · UniFirst 거래 비용 $14.4M 포함', 'q1', 'Cintas 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 15일 — Q4 FY26 실적', '2026-07-15',
     '매출 $2.91B(+8.9%) · 희석 EPS $1.26(1년 전 $1.09) · UniFirst 거래 비용 $14.0M 포함', 'q4', 'Cintas 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 6월 12일 — UniFirst 인수, FTC 2차 자료 요청', '2026-06-12',
     '6월 11일 FTC가 추가 자료를 요청해 심사 대기 기간이 늘었다 · 같은 날 UniFirst 주주총회는 합병 승인', 'ftc2', 'Cintas 공시 (SEC 8-K)'),
    ('neutral', '2026년 3월 25일 — Q3 FY26 실적', '2026-03-25',
     '매출 $2.84B(+8.9%) · 희석 EPS $1.24(1년 전 $1.13)', 'q3', 'Cintas 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 11일 — UniFirst 인수 계약', '2026-03-11',
     'UniFirst 주당 현금 $155 + CTAS 0.7720주(3/9 종가 기준 $310), 기업가치 약 $5.5B · 완료 뒤 4년 안에 비용 절감 약 $375M 목표', 'unf_deal', 'Cintas·UniFirst 공동 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 22일 — UniFirst 인수 제안 공개', '2025-12-22',
     'UniFirst 이사회에 주당 현금 $275(약 $5.2B) 제안을 냈다고 공개', 'unf_prop', 'Cintas 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 18일 — Q2 FY26 실적', '2025-12-18',
     '매출 $2.80B(+9.3%) · 희석 EPS $1.21(1년 전 $1.09)', 'q2', 'Cintas 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 12, 'mean': 222.08, 'median': 230, 'low': 181, 'high': 250, 'sb': 8, 'b': 2, 'h': 9, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(서비스 4개). 원문 대조: Q1 FY27 2,294.7/388.5/252.3/78.4, 1년 전 2,091.1/334.7/221.9/70.5(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "ctas:UniformRentalAndFacilityServicesSegmentMember": [
   "유니폼 대여·시설 서비스",
   "#0b4ea2"
  ],
  "ctas:FirstAidAndSafetyServicesSegmentMember": [
   "구급·안전 서비스",
   "#5b8fd6"
  ],
  "ctas:FireProtectionServicesMember": [
   "방화 서비스",
   "#e4572e"
  ],
  "ctas:UniformDirectSalesMember": [
   "유니폼 직판",
   "#a9c4ea"
  ]
 },
 "ignore": []
}
