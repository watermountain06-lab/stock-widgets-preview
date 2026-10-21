# WM(웨이스트 매니지먼트) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 133(시총 131위). 생활·산업 폐기물 수거·매립, 재활용, 매립가스 에너지, 의료 폐기물(Stericycle, 2024-11 인수).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-29), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 마감 뒤 접수), 8-K(COO 선임 2026-05-13, CEO 승계 2026-08-26), StockAnalysis.
# 엔진 입력(2026-10-21): 차입금 $23,356M(1년 안 $1,075 + 장기 $22,281 — 금융리스 포함) = 원문(DEBT_TOTAL_TAG). 단기투자 태그는 2013년 값이라 뺌, 리스는 운용리스만(연간 $1,010M) — EV_TAGS_BY_CIK.
# 이자비용은 손익계산서 "Interest expense, net"(InterestIncomeExpenseNonoperatingNet)만 분기로 낸다 → vendor/fetch_financials.CONCEPTS_BY_CIK(LOW·EMR·HWM 방식).
# 비연결 투자 $738M(그중 저소득 주택 세액공제 투자 $577M — 혜택은 법인세 감소로 들어와 이미 세율에 반영, 나머지는 신탁 관련 자산 등)은 비영업 자산에 더하지 않는다(엔진 기본: 비상장 지분 $57M만).
# EquitySecuritiesFvNi는 2020-12 값($314M)이 운전자본 차감에 남아 있다 — 1년 전·지금 양쪽에 같은 값이라 운전자본 변화에는 영향 없음.
# 인수 대금 최근 4분기: 2026년 1분기 누계 태그가 없어 엔진이 2025년 연간 $395M을 쓴다(원문 계산 $395 − $366 + $85 = $114M, 안건 E31 계열 — 판정 영향 작음).
# 4분기 EPS: 2021·2024는 보도자료 값(Q4_EPS_OVERRIDE).
CIK = '0000823768'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'WM'
S_ = 'https://www.sec.gov/Archives/edgar/data/823768/'
SEC = S_
TENQ = S_ + '000110465926088016/wm-20260630x10q.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000110465926087575/tm2621414d1_ex99-1.htm', 'q1': S_ + '000110465926050425/tm2612889d1_ex99-1.htm',
      'q4': S_ + '000110465926007476/tm264211d1_ex99-1.htm', 'q3': S_ + '000110465925102615/tm2529298d1_ex99-1.htm'}
LINKS = {'ceo': S_ + '000110465926101077/tm2624023d1_ex99-1.htm', 'coo': S_ + '000110465926059860/tm2614440d1_ex99-1.htm'}
FAIRBAND_TITLE = 'id="wmFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 60)
ACT_REASON = ''
# 다음 실적일: 2026-09-24 Business Wire 공지 — 10/27 장 마감 뒤 발표, 10/28 오전 10시 콜(Codex r1 필수)
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-27', 'src': '9/24 회사 공지 — 장 마감 뒤'}
NONOP_WHAT = '비상장 지분'
# 고정 문장(숫자 없음). 시나리오 역전의 원인(Fable 필수 2026-10-21 — 엔진 문장은 성장·이익률만 보여 준다)과 성장률의 인수 몫.
MODEL_NOTE = ('기본 시나리오는 최근 1년 매출/자본 효율에서 평균으로 옮겨 가고 낙관 시나리오는 평균만 쓴다 — 최근 효율이 평균보다 좋으면 낙관이 기본보다 낮게 나온다. '
              '3년·5년 매출 성장률에는 2024년 11월 Stericycle(의료 폐기물) 인수로 더해진 매출이 들어 있다.')
PH = ['RSG', 'CTAS', 'ROL', 'VLTO', 'UNP', 'CPRT']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '폐기물·사업 서비스 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '폐기물·사업 서비스 PBR 비교', 'psr': '폐기물·사업 서비스 PSR 비교',
                'pcr': '폐기물·사업 서비스 PCR(FCF) 비교', 'evebitda': '폐기물·사업 서비스 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(WM 제외)와 배수 순위를 매긴 값이다.',
            '기계·항공·운송·건설·업무 서비스 회사가 섞여 있다. 차트에는 폐기물·사업 서비스 6곳만 보인다.')
# 매출(Q2 2026 10-Q 주석 7 부문 표 — 순매출, 부문 간 매출 제외) — 동부 2,406 + 서부 2,291 + 기타 부수 서비스 782 + 재활용 403 + 재생에너지 157 + 의료 폐기물 638 = 6,677,
# 본사·기타 7을 더해 연결 6,684. 1년 전 2,292/2,251/738/381/115/646, 본사·기타 7 → 6,430.
SEG = [('수거·매립 동부', 2406, '#1c8a3e'), ('수거·매립 서부', 2291, '#5fb878'), ('기타 부수 서비스', 782, '#a7d7b3'), ('의료 폐기물(Stericycle)', 638, '#2b6cb0'),
       ('재활용 처리·판매', 403, '#f2b81d'), ('재생에너지(매립가스)', 157, '#9ca3af')]
SEG_ADJ = 7
SEG_TITLE = '매출 구성 — 보고 부문별(순매출)'
# 손 뉴스: 최신 실적(Q2 2026, 7/28 장 마감 뒤)도 손으로 쓴다 — 그 뒤 손 항목(8/26 CEO 승계)이 있으면 자동 항목이 빠진다. Q3 실적부터 다시 자동. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): CEO 8-K 8/26 12:37(장 전) → 8/26, Q2 8-K 7/28 20:42 → 7/29, COO 5/13 13:09(장 전) → 5/13, Q1 4/28 20:41 → 4/29,
# Q4 1/28 22:08 → 1/29, Q3 10/27 20:40 → 10/28.
# 넣지 않은 8-K: 신용 계약 개정(3/25), 임원 보상·전 CFO 퇴직(3/6·3/13), 주총(5/14), 퇴직연금 거래 정지 공지(2025-11-20).
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 26일 — CEO 승계: John Morris 사장이 내년 1월 CEO', '2026-08-26',
     'Jim Fish CEO가 은퇴·이사회 사임 계획 · John Morris 사장이 2027년 1월 4일부터 사장 겸 CEO, 이사회 합류', 'ceo', 'WM 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 28일 장 마감 뒤 — Q2 2026 실적', '2026-07-29',
     '매출 $6.68B(+4%) · 희석 EPS $1.95(1년 전 $1.80) · 분기 주주환원 $1B 넘음(보도자료)', 'q2', 'WM 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 13일 — Tara Hemmer COO 선임', '2026-05-13',
     'Morris 사장이 겸하던 최고운영책임자(COO)에 Tara Hemmer 부사장 · 재활용·재생에너지 등 지속가능 사업도 계속 맡음 · 의료 폐기물 부문장 Rafael Carrasco 7월 은퇴', 'coo', 'WM 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 28일 장 마감 뒤 — Q1 2026 실적', '2026-04-29',
     '매출 $6.23B(+3%) · 희석 EPS $1.79(1년 전 $1.58)', 'q1', 'WM 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 28일 장 마감 뒤 — Q4 2025 실적', '2026-01-29',
     '매출 $6.31B(+7%) · 희석 EPS $1.83(1년 전 $1.48) · 2025년 매출 $25.20B·EPS $6.70 · 2026년 연간 배당을 $0.48 올린 $3.78로 할 의향(이사회) · 2025년 12월 발표한 $3.0B 자사주 매입 승인으로 2026년 약 $2B 매입 재개 예정', 'q4', 'WM 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 27일 장 마감 뒤 — Q3 2025 실적', '2025-10-28',
     '매출 $6.44B(+15% — 2024년 11월 Stericycle 인수 효과 포함) · 희석 EPS $1.49(1년 전 $1.88) · 자산 손상·특별 항목 손실 $213M 포함(보도자료)', 'q3', 'WM 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 28, 'nt': 19, 'mean': 255.16, 'median': 261, 'low': 220, 'high': 277, 'sb': 16, 'b': 3, 'h': 9, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-21'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(보고 부문 축 6개, 순매출). 소계 Collection and Disposal은 ignore, 본사·기타는 adjust(합계 대조에만).
# 원문 대조: Q2 2026 2,406/2,291/782/638/403/157 + 7, 1년 전 2,292/2,251/738/646/381/115 + 7, Q1 2026도 같은 지도로 값이 나옴(2026-10-21).
# FY2025 10-K는 동부·서부·기타 부수 멤버가 2025년 3분기 10-Q에 없어 4분기 값을 못 만든다 — 2026년 분기 10-Q에는 있어 FY2026 10-K부터는 된다.
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "wm:EastTierRegionAreasMember": [
   "수거·매립 동부",
   "#1c8a3e"
  ],
  "wm:WestTierRegionAreasMember": [
   "수거·매립 서부",
   "#5fb878"
  ],
  "us-gaap:AllOtherSegmentsMember": [
   "기타 부수 서비스",
   "#a7d7b3"
  ],
  "wm:HealthcareSolutionsMember": [
   "의료 폐기물(Stericycle)",
   "#2b6cb0"
  ],
  "wm:RecyclingProcessingAndSalesMember": [
   "재활용 처리·판매",
   "#f2b81d"
  ],
  "wm:RenewableEnergySegmentMember": [
   "재생에너지(매립가스)",
   "#9ca3af"
  ]
 },
 "ignore": [
  "wm:CollectionAndDisposalMember"
 ],
 "adjust": [
  "us-gaap:CorporateAndOtherMember"
 ]
}
