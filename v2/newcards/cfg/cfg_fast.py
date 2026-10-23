# FAST(파스테널) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 171(시총 170위). 산업용 소모품·체결 부품(패스너)·안전 용품 유통, 고객 현장 자판기·매장.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-19 장중), 실적 보도자료(Q3 2025~Q3 2026, 8-K 2.02항 — 보도자료 장 전, 8-K 장중), 8-K(CEO 승계 12/22, CFO 11/3), StockAnalysis.
# 2-for-1 분할 2025-05-22(KNOWN_SPLITS). 엔진 입력(2026-10-22): 감가상각 = Depreciation + AmortizationOfIntangibleAssets(합산 태그가 10-K 4개뿐이라 EV/EBITDA를 못 냈다, DDA_PARTS_BY_CIK).
# 차입금 $100M(1년 안 50 + 장기 50, 원문). 4분기 EPS 2024·2025 보도자료 값(분할 반영).
CIK = '0000815556'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Fastenal'
S_ = 'https://www.sec.gov/Archives/edgar/data/815556/'
SEC = S_
TENQ = S_ + '000081555626000049/fast-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000081555626000046/ex_99109302026earningsrele.htm', 'q2': S_ + '000081555626000037/ex_99106302026earningsrele.htm',
      'q1': S_ + '000081555626000019/ex_99103312026earningsrele.htm', 'q4': S_ + '000081555626000003/ex_99112312025earningsrele.htm',
      'q3_25': S_ + '000081555625000116/ex_99109302025earningsrele.htm'}
LINKS = {'cfo': S_ + '000081555625000121/ex_99110302025cfo.htm', 'ceo': S_ + '000081555625000123/ex_99112222025ceo.htm'}
FAIRBAND_TITLE = 'id="fastFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(분할 반영). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 꾸준한 성장·높은 배수, 거의 무차입.
MODEL_NOTE = ('차입금이 거의 없고 매출이 꾸준히 늘어 온 회사로, 지금 배수는 최근 5년 범위에서도 높은 쪽이다. 최근 분기 매출 성장은 빨라졌지만 매출총이익률은 1년 전보다 조금 낮다. '
              '현금흐름 내재가치는 이익률·재투자 효율이 과거 수준으로 돌아간다고 본 값이고, 매장·자판기 임차료는 이미 영업비용이라 운용리스는 순부채에서 빼지 않는다. EPS·주가는 분할(최근 2025년 5월) 뒤 기준이다.')   # Codex·Fable r1
PH = ['GWW', 'MSM', 'WSO', 'URI', 'CTAS', 'PH']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '산업재 유통·서비스 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(FAST 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·건설이 섞여 있다. 차트에는 산업재 유통·서비스 6곳만 보인다.')
# 매출(Q3 2026 10-Q 지역별) — 미국 2,035.2 + 캐나다·멕시코 342.1 + 북미 외 86.1 = 2,463.4. 1년 전 1,777.9·284.8·70.6.
SEG = [('미국', 2035.2, '#0054a4'), ('캐나다·멕시코', 342.1, '#5c94d1'), ('북미 외', 86.1, '#b3cce8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역별'
# 손 뉴스: 실적 5건(EPS는 GAAP 희석 — 가이던스 없음), CEO 승계.
# 반응일: 실적 보도자료 장 전 배포(Q3 2025는 보도자료 10/13 — 8-K 접수는 다음 날 10/14T17:20Z라 반응일은 보도자료 날짜, Fable r1 필수), 8-K 접수 UTC 2026-01-20T18:17Z·04-13T16:07Z·07-14T16:01Z·10-14T15:56Z = 장중 → 같은 날.
# CEO 승계 8-K 2025-12-22T18:16Z(장중) → 12/22. CFO 8-K 2025-11-04T02:12Z(11/3 동부 21:12) → 11/4. 넣지 않은 8-K: 이사·임원(4/29·6/12), 주총(4/24), 신용 약정(6/23).
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 14일 — Q3 2026 실적', '2026-10-14',
     '매출 $2.46B(+15.5%) · 희석 EPS $0.35(1년 전 $0.29, +19.8%)', 'q3', 'Fastenal 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 14일 — Q2 2026 실적', '2026-07-14',
     '매출 $2.39B(+14.7%) · 희석 EPS $0.33(1년 전 $0.29, +15.9%) · 매출총이익률 44.6%(1년 전 45.3%)', 'q2', 'Fastenal 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 13일 — Q1 2026 실적', '2026-04-13',
     '매출 $2.20B(+12.4%) · 희석 EPS $0.30(1년 전 $0.26) · 매출총이익률 44.6%(1년 전 45.1%)', 'q1', 'Fastenal 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 20일 — Q4 2025 실적', '2026-01-20',
     '매출 $2.03B(+11.1%) · 희석 EPS $0.26(1년 전 $0.23) · 매출총이익률 44.3%(1년 전 44.8%) · 2025년 매출 $8.20B(+8.7%)', 'q4', 'Fastenal 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 22일 — CEO 승계 발표', '2025-12-22',
     'Dan Florness CEO가 2026년 7월 16일 물러나고 Jeffery Watts 사장 겸 최고영업책임자가 CEO 승계', 'ceo', 'Fastenal 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 3일 — 새 CFO 선임', '2025-11-04',
     'Whirlpool·Beko Europe 출신 재무 책임자를 CFO로 영입(11월 10일 취임, 8-K 장 마감 뒤 접수 — 반응은 11/4)', 'cfo', 'Fastenal 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 13일 — Q3 2025 실적', '2025-10-13',
     '매출 $2.13B(+11.7%) · 희석 EPS $0.29(1년 전 $0.26) · 매출총이익률 45.3%(1년 전 44.9%)', 'q3_25', 'Fastenal 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 18, 'nt': 11, 'mean': 51.64, 'median': 51, 'low': 46, 'high': 60, 'sb': 6, 'b': 0, 'h': 7, 's': 3, 'ss': 2}
ANALYST_ASOF = '2026-10-22'

# ── 자동 카드 — 지역 3개. 원문 대조: Q3 2026 2,035.2/342.1/86.1, 1년 전 1,777.9/284.8/70.6(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "srt:StatementGeographicalAxis",
 "extra": {},
 "members": {
  "country:US": [
   "미국",
   "#0054a4"
  ],
  "fast:CanadaandMexicoMember": [
   "캐나다·멕시코",
   "#5c94d1"
  ],
  "fast:NonNorthAmericaMember": [
   "북미 외",
   "#b3cce8"
  ]
 },
 "ignore": []
}
