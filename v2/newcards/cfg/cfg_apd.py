# APD(에어 프로덕츠) v2 카드 설정 — 자동 카드(AUTO). 회계연도 9월 30일(FY26 = 2025-10 ~ 2026-09). 카드 순위 161(시총 159위). 산업용 가스(현장 공급·상업 판매), 가스 설비.
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-07-30), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 모두 동부 오전 6~8시대 접수 = 장 전), 8-K(청정 에너지 사업 철수·손상 2.06항 6/30), StockAnalysis.
# 2023-03까지 특수관계자 장기 차입금은 NotesPayableRelatedPartiesNoncurrent(2022-12 $658.4M) — DEBT_TOTAL_TAG 튜플이 표준 태그를 먼저 쓴다(Codex r1). FY24 4분기 EPS는 전체 기준 $8.75(역산과 같음).
# 엔진 입력(2026-10-22): 차입금 $17,667.5M = 단기 126.7 + 1년 안 769.5 + 장기 16,585.1 + 특수관계자 장기 186.2 — 2023년부터 장기 차입금을 특수관계자 축으로만 실어
# 요약 자료에 차원 없는 값이 없다 → BUILD dim_facts(overlay LongTermDebtNonrelatedApd·LongTermDebtRelatedApd) + DEBT_TOTAL_TAG(그 전 날짜는 차원 없는 태그). 기본은 단기 $126.7M뿐이었다.
# 비지배지분 $2,713M(합작 사업). 최근 4분기 영업이익은 사업 정리 손상 때문에 음수 — Q2 FY25 약 −$2.3B(사업·자산 정리 $3.7B의 대부분), Q3 FY26 세전 약 $2.9B(루이지애나 청정 에너지 단지·애리조나 그린 수소 철수).
# 현금흐름 모델 값이 0 이하로 나와 판정의 현금흐름 칸은 −2. 4분기 EPS FY24·FY25 보도자료 값.
BUILD = {'dim_facts': [('us-gaap:LongTermDebtAndCapitalLeaseObligations', 'us-gaap:RelatedPartyTransactionsByRelatedPartyAxis', 'us-gaap:NonrelatedPartyMember', 'LongTermDebtNonrelatedApd'),
                       ('us-gaap:LongTermDebtAndCapitalLeaseObligations', 'us-gaap:RelatedPartyTransactionsByRelatedPartyAxis', 'us-gaap:RelatedPartyMember', 'LongTermDebtRelatedApd')]}
CIK = '0000002969'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-09-30', '2024-09-30'), 'FY25'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Air Products'
S_ = 'https://www.sec.gov/Archives/edgar/data/2969/'
SEC = S_
TENQ = S_ + '000000296926000036/apd-20260630.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000000296926000034/exhibit99130jun26.htm', 'q2': S_ + '000000296926000018/exhibit99131mar26.htm',
      'q1': S_ + '000000296926000006/exhibit99131dec25.htm', 'q4': S_ + '000000296925000051/exhibit99130sep25.htm'}
LINKS = {'exit': 'https://www.sec.gov/Archives/edgar/data/2969/000119312526289427/d97956d8k.htm'}
FAIRBAND_TITLE = 'id="apdFairBand" title="최근 1년 PER 25~75% 구간 × 최근 4분기 희석 EPS. 최근 4분기 EPS가 사업 철수 손상으로 낮아 이 범위는 참고용이다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-80, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
YOY_NOTE = {'2026-06-30': 'Q3 FY26 영업손실·순손실에는 청정 에너지 사업 철수 손상 세전 약 $2.9B(주당 $9.92)가 들어 있다'}
# 고정 문장(숫자 없음). 손상, 합작 비지배지분.
MODEL_NOTE = ('0 이하가 나오는 주된 이유는 손상이 아니라 재투자다. 최근 4분기 설비투자가 감가상각의 세 배가 넘는데 투하자본 수익률은 할인율보다 낮아, 모델은 이익률이 회복하는 '
              '시나리오에서도 투자가 가치를 만들지 못한다고 계산하고 거기서 큰 차입금을 뺀다. 회사는 대형 수소 프로젝트를 정리해 설비투자를 줄이겠다고 밝혔고, 투자가 줄면 이 계산도 달라진다. '
              '판정 합계에서 이 현금흐름 칸(−2)이 가장 크게 작용한다. 최근 4분기 영업이익은 손상 때문에 음수라 PER은 빠지고, PCR은 큰 설비투자로 FCF가 줄어, EV/EBITDA는 손상으로 EBITDA가 줄어 일시적으로 높다.')   # Codex r1·Fable r1 필수
HEALTH_EXTRA = '순현금의 리스는 분기 보고서에 실린 비유동 운용리스만이다 — 1년 안에 갚을 유동 운용리스는 넣지 않았다.'   # 고정 문장(Codex r1 권장)
PH = ['LIN', 'ECL', 'SHW', 'DD', 'PPG', 'IFF']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '화학·소재 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(APD 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·포장·건자재가 섞여 있다. 차트에는 화학·소재 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 부문) — 미주 1,321.4 + 아시아 886.0 + 유럽 815.7 + 중동·인도 34.8 + 본사·기타(설비 판매) 103.1 = 3,161.0. 1년 전 1,261.0/810.0/770.5/38.3/142.9 → 3,022.7.
SEG = [('미주', 1321.4, '#009a44'), ('아시아', 886.0, '#5cc28a'), ('유럽', 815.7, '#006b2f'), ('본사·기타(설비 판매)', 103.1, '#a9d9bd'), ('중동·인도', 34.8, '#d4ecdf')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 최신 실적(Q3 FY26, 7/30)도 손으로 — 손상 금액을 적으려고. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K 2025-11-06T12:44Z·2026-01-30T12:40Z·04-30T10:50Z·07-30T10:58Z, 철수 8-K 06-30T12:08Z = 장 전 → 같은 날.
# 넣지 않은 8-K: 이사 불출마(2025-11-25), 주총(1/29).
NEWS_RANGE = '2025.11 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 30일 — Q3 FY26 실적 · 철수 손상', '2026-07-30',
     '매출 $3.16B(+4.6%) · 영업손실 $2.1B · 희석 EPS −$6.47 — 청정 에너지 사업 철수 손상 세전 약 $2.9B(주당 $9.92, 6/30에 예고) · NEOM 암모니아 Yara 판매 계약 체결', 'q3', 'Air Products 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 6월 30일 — 루이지애나·애리조나 수소 사업 철수 · NEOM 판매 계약', '2026-06-30',
     '루이지애나 청정 에너지 단지·애리조나 액화 수소 등에서 철수 — 세전 최대 $2.9B 손상·계약 해지 비용 예상(현금 지출은 $925M 이하 추정). 같은 발표에서 사우디 NEOM 그린 수소 사업의 암모니아를 Yara가 판매하는 계약을 마무리 중이라고 밝힘', 'exit', 'Air Products 공시 (SEC 8-K 2.06항)'),
    ('neutral', '2026년 4월 30일 — Q2 FY26 실적', '2026-04-30',
     '매출 +8.8% · 영업이익 $753M · 희석 EPS $3.19(1년 전 −$7.77 — 사업 정리 손상 분기)', 'q2', 'Air Products 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 30일 — Q1 FY26 실적', '2026-01-30',
     '매출 $3.1B(+6%) · 희석 EPS $3.04(+10%) · 영업이익률 23.7%', 'q1', 'Air Products 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 6일 — Q4 FY25 실적', '2025-11-06',
     '희석 EPS $0.02 — 사업·자산 정리 비용 세전 약 $795M 포함 · FY2025 계속사업 주당 −$1.74(정리 비용 세전 $3.7B)', 'q4', 'Air Products 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 17, 'mean': 337.71, 'median': 345, 'low': 305, 'high': 365, 'sb': 11, 'b': 5, 'h': 7, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(부문 5개). 원문 대조: Q3 FY26 1,321.4/886.0/815.7/103.1/34.8, 1년 전 1,261.0/810.0/770.5/142.9/38.3(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:Revenues"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "apd:AmericasSegmentMember": [
   "미주",
   "#009a44"
  ],
  "apd:AsiaSegmentMember": [
   "아시아",
   "#5cc28a"
  ],
  "apd:EuropeSegmentMember": [
   "유럽",
   "#006b2f"
  ],
  "us-gaap:CorporateAndOtherMember": [
   "본사·기타(설비 판매)",
   "#a9d9bd"
  ],
  "apd:MiddleEastAndIndiaSegmentMember": [
   "중동·인도",
   "#d4ecdf"
  ]
 },
 "ignore": []
}
