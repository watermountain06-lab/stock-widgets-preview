# TDG(트랜스다임) v2 카드 설정 — 자동 카드(AUTO). 회계연도 9월 30일(FY26 = 2025-10 ~ 2026-09, 분기 말은 토요일). 카드 순위 170(시총 169위). 항공기 부품(독점 애프터마켓 중심), 인수로 성장.
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-06-27 분기, 8/4 장 마감 뒤 접수), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 보도자료 장 전, 8-K 장중), 8-K(인수·철회·차입), StockAnalysis.
# 엔진 입력(2026-10-22): 감가상각 = Depreciation + AmortizationOfIntangibleAssets(합산 태그가 30개뿐이라 EV/EBITDA 이력 56일 → 1,255일, DDA_PARTS_BY_CIK).
# 차입금 = 1년 안 139 + 매출채권 유동화 725 + 장기 32,621 = $33,485M(DEBT_TOTAL_TAG — 유동화 차입이 빠져 있었다; 장기 태그는 금융리스 포함). 비지배지분 = 9 + 상환 가능 81.
# 자기자본이 −$9.8B(특별배당·자사주를 빚으로 한 결과) — PBR 계산 불가. 4분기 EPS FY24 보도자료 값. GAAP EPS는 스톡옵션 배당 상당액 지급만큼 줄어든다.
CIK = '0001260221'
CUR, YO, QO = '2026-06-27', '2025-06-28', '2026-03-28'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-09-30', '2024-09-30'), 'FY25'
VOTES, VERDICT = (1, -1, -2), '적정~고평가'
CO = 'TransDigm'
S_ = 'https://www.sec.gov/Archives/edgar/data/1260221/'
SEC = S_
TENQ = S_ + '000126022126000053/tdg-20260627.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000126022126000052/exhibit991tdg2026q3earning.htm', 'q2': S_ + '000126022126000039/exhibit991tdg2026q2earning.htm',
      'q1': S_ + '000126022126000015/exhibit991tdg2026q1earning.htm', 'q4': S_ + '000126022125000078/exhibit991tdg2025q4earning.htm'}
LINKS = {'stellant': S_ + '000126022126000044/tdg-20260710.htm', 'pi': S_ + '000126022126000064/tdg-20260928.htm',
         'jpe': S_ + '000126022126000031/tdg-20260407.htm', 'notes': S_ + '000126022126000059/tdg-20260914.htm'}
FAIRBAND_TITLE = 'id="tdgFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 60)
ACT_REASON = ''
NONOP_WHAT = '투자'
YOY_NOTE = {'2026-06-27': 'Q3 FY26 매출 +22.5% 가운데 기존 사업(유기) 성장은 +12.6%($284M)이고 인수한 회사 매출이 $220M(+9.8%p)이다 — 시장별 칸의 상업 애프터마켓 보고 성장 +30.1%에는 인수(Jet Parts·Victor Sierra) 효과가 들어 있다(보도자료의 애프터마켓 +17%는 집계 기준이 다르다)'}   # Fable·Codex r1 필수
# 고정 문장(숫자 없음). 음수 자본, 고배당·고차입 구조, 인수로 크는 회사, GAAP EPS의 배당 상당액.
MODEL_NOTE = ('특별배당과 자사주 매입을 빚으로 해 와서 자기자본이 마이너스다 — PBR은 계산되지 않고, 차입금이 매우 커서 순차입금이 내재가치를 크게 깎는다. '
              '회사는 해마다 부품 회사를 사들여 크므로 모델은 인수 지출을 재투자로 본다. 카드 숫자는 6월 말 기준이라 그 뒤의 Prince & Izant 인수에 따른 현금 감소와 9월 회사채 발행·차환에 따른 차입금 변동이 들어 있지 않다. GAAP EPS는 스톡옵션 보유자에게 주는 배당 상당액만큼 줄어, 특별배당이 있던 분기의 PER이 높게 보일 수 있다.')
PH = ['HEI', 'GE', 'HWM', 'RTX', 'GD', 'LHX']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '항공·방산 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '항공·방산 PBR 비교', 'psr': '항공·방산 PSR 비교',
                'pcr': '항공·방산 PCR(FCF) 비교', 'evebitda': '항공·방산 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(TDG 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·건설이 섞여 있다. 차트에는 항공·방산 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 시장 경로별) — 국방 1,148 + 상업 애프터마켓 908 + 상업 OEM 639 + 비항공 46 = 2,741. 1년 전 963·698·536·40 → 2,237.
SEG = [('국방', 1148.0, '#1b365d'), ('상업 애프터마켓', 908.0, '#6d87b0'), ('상업 OEM', 639.0, '#a9bbd6'), ('비항공', 46.0, '#dbe3ef')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 시장 경로별'
# 손 뉴스: 실적 4건(EPS는 GAAP — 조정 EPS·가이던스는 쓰지 않는다), 인수·철회 3건, 차환. 
# 반응일: 실적 보도자료는 장 전 배포, 8-K 접수 UTC 2025-11-12T17:18Z·2026-02-03T17:19Z·05-05T15:17Z·08-04T15:17Z = 장중 → 같은 날.
# Stellant 철회 8-K 2026-07-13T14:45Z(장중) → 7/13. P&I 인수 합의 7/27T15:16Z → 7/27, 완료 9/28T15:42Z → 9/28. Jet Parts·Victor Sierra 완료 4/7T17:19Z → 4/7. 회사채 발행 착수·공개매수 8-K 9/14T17:04Z(장중) → 9/14(Fable r1).
# 넣지 않은 8-K: CEO 교체 확인(10/1·10/3 — 5월 발표분), 이사(10/23·7/24), Simmonds 완료(10/6 — 6월 합의분), 합의만 하고 철회된 Stellant 합의(12/31), Jet Parts 합의(1/16), 차입(2·4월), 주총(3/5), Extant 자산 인수(9/21 — 작음).
NEWS_RANGE = '2025.11 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 28일 — Prince & Izant 인수 완료', '2026-09-28',
     '경납땜 합금·특수 금속 부품 회사 Prince & Izant(항공기 엔진 연료 노즐 등)를 약 $1.07B 현금에 인수 완료(7월 합의)', 'pi', 'TransDigm 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 9월 14일 — 회사채 $3.0B 발행 조건 확정 · 2028년 만기 채권 공개매수', '2026-09-14',
     '2035년 만기 선순위 담보채 $3.0B(6.75%, 처음 $2.5B에서 늘림, 9/28 발행 완료)로 2028년 만기 채권을 사들이고 남는 돈은 일반 목적 — 총차입금이 늘어난다', 'notes', 'TransDigm 공시 (SEC 8-K)'),
    ('neutral', '2026년 8월 4일 — Q3 FY26 실적', '2026-08-04',
     '매출 $2.74B(+23%) · 순이익 $540M(+10%) · 희석 EPS $9.39(1년 전 $8.47) · 상업 애프터마켓 +17%', 'q3', 'TransDigm 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 13일 — Stellant 인수 철회', '2026-07-13',
     '규제 심사가 길어져 약 $960M 규모 Stellant Systems 인수를 철회 — 4월 이 인수용으로 빌린 $1.5B는 그대로', 'stellant', 'TransDigm 공시 (SEC 8-K)'),
    ('green', '2026년 5월 5일 — Q2 FY26 실적', '2026-05-05',
     '매출 $2.54B(+18.3%) · 순이익 $536M(+11.9%) · 희석 EPS $9.20(1년 전 $8.24)', 'q2', 'TransDigm 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 7일 — Jet Parts Engineering·Victor Sierra 인수 완료', '2026-04-07',
     '항공기 독립 대체 부품·서비스 회사 두 곳을 약 $2.2B에 인수 완료(1월 합의, 2월 회사채·대출로 조달)', 'jpe', 'TransDigm 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 3일 — Q1 FY26 실적', '2026-02-03',
     '매출 $2.29B(+13.9%, 유기 +7.4%) · 순이익 $445M(−9.7%, 차입 증가로 이자비용 늘어) · 희석 EPS $6.62(1년 전 $7.62) · 상업 애프터마켓·국방이 한 자릿수 후반 성장으로 둔화', 'q1', 'TransDigm 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 12일 — Q4 FY25 실적', '2025-11-12',
     '매출 $2.44B(+11.5%) · 순이익 $609M(+30.1%) · 희석 EPS $7.75(1년 전 $5.80, 8월 선언·9/12 지급한 $90 특별배당의 옵션 배당 상당액으로 주당 $2.75 감소) · FY25 EPS $32.08', 'q4', 'TransDigm 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 14, 'mean': 1411.86, 'median': 1400, 'low': 1200, 'high': 1745, 'sb': 9, 'b': 3, 'h': 11, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'

# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(시장 경로 4개). 원문 대조: Q3 FY26 1,148/908/639/46, 1년 전 963/698/536/40(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:Revenues"
 ],
 "axis": "tdg:SalesMarketTypeAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "tdg:DefenseMember": [
   "국방",
   "#1b365d"
  ],
  "tdg:CommercialAftermarketMember": [
   "상업 애프터마켓",
   "#6d87b0"
  ],
  "tdg:CommercialOEMMember": [
   "상업 OEM",
   "#a9bbd6"
  ],
  "tdg:NonAviationMember": [
   "비항공",
   "#dbe3ef"
  ]
 },
 "ignore": []
}

# 템플릿 보정(Fable r1): 체크포인트 ③ 방향, 주주환원 '배당 지급'은 옵션 배당 상당액
POST = [r'''
h = re.sub(r"차입금 \$[\d.]+B이 줄어드는지", "6월 말 뒤 P&I 인수(현금)와 9월 회사채 발행·차환 이후 현금·차입금·순차입금이 어떻게 바뀌었는지", h)
h = h.replace('<span class="zone-label">배당 지급 (회계연도', '<span class="zone-label">옵션 배당 상당액 지급 (회계연도')
''']

