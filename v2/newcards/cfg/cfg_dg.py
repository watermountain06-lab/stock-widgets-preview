# DG(달러 제너럴) v2 카드 설정 — 자동 카드(AUTO). 회계연도 1월 말 무렵 금요일(52·53주 — FY2025는 2026-01-30에 끝남). 미국 소도시 중심 저가 잡화 체인, 단일 부문.
# 출처: SEC XBRL, Q2 FY26 10-Q(2026-08-27), 실적 보도자료(Q3 FY25~Q2 FY26, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), 8-K(CEO 승계 2026-03-24), StockAnalysis. 사전 조사 scratchpad pre/DG.md.
# 엔진 입력(2026-10-25): 차입금 = 1년 안 $12.7M + 장기 $4,558.1M(DEBT_TOTAL_TAG), 현금 $1,590M, 운용리스 $11.2B(리스로).
# 일회성: Q2 FY26 관세 환급(재투자 뒤 순 주당 약 $0.25) — 최근 4분기 EPS 7.69의 약 3%. 1년 전 Q4 FY24 매장 정리 비용(주당 −$0.81)이 전년 대비를 키운다.
CIK = '0000029534'
CUR, YO, QO = '2026-07-31', '2025-08-01', '2026-05-01'
QLABEL, YL, QQL = 'Q2 FY26', 'Q2 FY25', 'Q1 FY26'
L8 = ['Q3 FY24', 'Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26']
FY_ENDS, FY_LABEL = ('2026-01-30', '2025-01-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'Dollar General'
S_ = 'https://www.sec.gov/Archives/edgar/data/29534/'
SEC = S_
TENQ = S_ + '000110465926101932/dg-20260731x10q.htm'; TENQ_NAME = 'Q2 FY26 10-Q'
PR = {'q2': S_ + '000110465926101918/tm2623914d1_ex99.htm', 'q1': S_ + '000110465926069198/tm2616084d1_ex99.htm',
      'q4': S_ + '000110465926026697/tm268519d1_ex99.htm', 'q3': S_ + '000110465925118286/tm2532496d1_ex99.htm'}
LINKS = {'ceo': S_ + '000110465926033643/tm269511d1_ex99.htm'}
FAIRBAND_TITLE = 'id="dgFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 10)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('회계연도가 1월 말에 끝나 FY2025는 2025년 2월~2026년 1월이다. 매장 운용리스가 커서 차입금과 따로 본다. '
              '2024년 매장 정리 비용으로 이익이 크게 줄었다가 회복하는 중이라 전년 대비 증가율이 크게 나온다. Q2 FY26 이익에는 관세 환급(일회성)이 조금 들어 있다.')
PH = ['WMT', 'COST', 'TGT', 'KR', 'DLTR', 'PG']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유통 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': '유통 PBR 비교', 'psr': '유통 PSR 비교',
                'pcr': '유통 PCR(FCF) 비교', 'evebitda': '유통 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(DG 제외)와 배수 순위를 매긴 값이다.',
            '음식료·생활용품·담배·유통이 섞여 있다. 차트에는 유통 6곳만 보인다.')
# 매출(Q2 FY26 10-Q, 품목별) — 소모품 9,263.0 + 계절상품 1,187.7 + 가정용품 536.6 + 의류 303.1 = 11,290.4.
SEG = [('소모품', 9263.0, '#e6b800'), ('계절상품', 1187.7, '#f2d966'), ('가정용품', 536.6, '#a68a1a'), ('의류', 303.1, '#d9cfa0')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 품목별(Q2 FY26)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석) + CEO 승계. 반응일: 장 전 발표 → 같은 날, CEO 승계 8-K 3/24 → 3/24. 넣지 않은 8-K: COO 선임, 이사·법무 책임자 은퇴.
NEWS_RANGE = '2025.12 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 27일 — Q2 FY26 실적', '2026-08-27',
     '매출 $11.29B(+5.2%) · 순이익 $550M · 희석 EPS $2.48(1년 전 $1.86) — 관세 환급(순 주당 약 $0.25) 포함', 'q2', 'Dollar General 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 6월 2일 — Q1 FY26 실적', '2026-06-02',
     '매출 $10.79B · 순이익 $444M · 희석 EPS $2.00(1년 전 $1.78)', 'q1', 'Dollar General 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 24일 — CEO 승계 발표', '2026-03-24',
     'Todd Vasos의 후임으로 Jerry Fleeman을 영입 — 2027년 1월 1일부터 CEO', 'ceo', 'Dollar General 공시 (SEC 8-K)'),
    ('red', '2026년 3월 12일 — Q4 FY25 실적', '2026-03-12',
     '매출 $10.91B · 순이익 $426M · 희석 EPS $1.93(1년 전 $0.87 — 매장 정리 비용) — 발표 당일 주가 −6%', 'q4', 'Dollar General 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 4일 — Q3 FY25 실적', '2025-12-04',
     '매출 $10.65B · 순이익 $283M · 희석 EPS $1.28(1년 전 $0.89) — 발표 당일 주가 +14%', 'q3', 'Dollar General 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 31, 'nt': 23, 'mean': 143.91, 'median': 140, 'low': 110, 'high': 176, 'sb': 10, 'b': 3, 'h': 17, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 품목 4개(수동 지도). 원문 대조: Q2 FY26 9,263.0/1,187.7/536.6/303.1(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"dg:ConsumablesMember": ["소모품", "#e6b800"], "dg:SeasonalMember": ["계절상품", "#f2d966"], "dg:HomeProductsMember": ["가정용품", "#a68a1a"], "dg:ApparelMember": ["의류", "#d9cfa0"]},
 "ignore": []
}
