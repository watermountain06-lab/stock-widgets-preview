# HPE(휴렛팩커드 엔터프라이즈) v2 카드 설정 — 자동 카드(AUTO). 회계연도 10월 31일. 카드 순위 145(시총 143위). 서버·스토리지(Cloud & AI)·네트워크(Juniper 포함).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-09-03), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 모두 장 마감 뒤 접수), 8-K(H3C 지분 매각·Elliott 협약·이사), StockAnalysis.
# 엔진 입력(2026-10-21): 차입금 $20,244M(DebtCurrent "Notes payable and short-term borrowings" $2,901 + 장기 $17,343 — 기본은 LongTermDebtCurrent $2,137만 잡아 $764M이 빠졌다).
# 2024-09 발행 Series C 의무전환 우선주 $1.5B(3,000만 주 × $50, 2027-09 보통주 전환)는 nonop_extra "kind": "preferred"로 주주가치에서만 뺀다(투하자본 무관 — Codex r1). 우선주 태그는 2021년 옛 우선주, 비지배 태그는 2024-07에 멈춰 둘 다 끔
# (10-Q 비지배 $62M은 태그가 없어 빠진다 — 주당 약 $0.05). 운용리스는 10-K 값. 4분기 EPS FY24·FY25 보도자료 값.
# 차입금에는 HPE Financial Services의 리스·금융 채권을 받치는 차입이 들어 있다 — 금융 채권 $9.7B 중 유동 $3.8B만 운전자본, 장기 $5.9B는 어디에도 안 더해진다.
BUILD = {}
CIK = '0001645590'
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-10-31', '2024-10-31'), 'FY2025'
VOTES, VERDICT = (-1, 1, -2), '적정~고평가'
CO = 'HPE'
S_ = 'https://www.sec.gov/Archives/edgar/data/1645590/'
SEC = S_
TENQ = S_ + '000164559026000080/hpe-20260731.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000164559026000078/ex-991x922026x8k.htm', 'q2': S_ + '000164559026000052/ex-991x612026x8k.htm',
      'q1': S_ + '000164559026000028/ex-991x392026x8k.htm', 'q4': S_ + '000164559025000126/ex-991x1242025x8k.htm'}
LINKS = {'netday': S_ + '000164559026000084/hpenetworkinginvestorday20.htm', 'h3c': S_ + '000164559026000045/hpe-20260513.htm'}
FAIRBAND_TITLE = 'id="hpeFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-10, 20)
ACT_REASON = ''
NONOP_WHAT = '장기 투자'
# 고정 문장(숫자 없음). Juniper 인수로 커진 매출, 과거 낮은 이익률에서 출발하는 모델, 금융 자회사 차입, 의무전환 우선주.
MODEL_NOTE = ('매출 증가에는 2025년 7월 완료한 Juniper Networks 인수분이 크게 섞여 있다. 이 모델은 과거 영업이익률(영업권 손상·인수 비용이 든 해 포함)에서 출발하고, '
              '그 이익률에서는 투하자본 수익률이 영구성장률보다 낮아 성장할수록 가치가 줄어 주주가치가 0 이하로 나온다 — 최근 이익률 개선은 거의 반영되지 않는다. '
              '연결 차입금에는 금융 자회사(리스·할부)의 차입이 섞여 있고 그 채권은 일부만 운전자본에 들어가므로, 순부채를 본업의 부채 부담으로 그대로 읽지 않는다. '
              '보통주로 바뀔 의무전환 우선주는 청산 우선액으로 주주가치에서 뺐다.')   # Codex r1 필수 3건
PH = ['DELL', 'CSCO', 'ANET', 'IBM', 'STX', 'APH']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': 'IT 하드웨어·네트워크 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'IT 하드웨어 PBR 비교', 'psr': 'IT 하드웨어 PSR 비교',
                'pcr': 'IT 하드웨어 PCR(FCF) 비교', 'evebitda': 'IT 하드웨어 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(HPE 제외)과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 섞여 있다. 차트에는 IT 하드웨어·네트워크 회사만 보인다.')
# 매출(Q3 FY26 10-Q 주석 2 부문) — Cloud & AI 9,042 + Networking 2,893 + 기업 투자·기타 278 = 12,213. 1년 전 7,212/1,654/270 → 9,136.
SEG = [('Cloud & AI(서버·스토리지·금융)', 9042, '#01a982'), ('네트워크(Juniper 포함)', 2893, '#4fd1b1'), ('기업 투자·기타', 278, '#a8e8d6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 사업 부문별'
# 손 뉴스: 최신 실적(Q3 FY26, 9/2)도 손으로 — 뒤 9/30 네트워크 투자자 행사(7.01)는 넣지 않았다. 가이던스·비GAAP는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부, 날짜도 UTC 값): 실적 8-K 2025-12-05T02:07Z = 12/4 21:07 → 12/5, 2026-03-10T00:08Z → 3/10, 06-02T00:09Z → 6/2, 09-03T00:06Z → 9/3.
# H3C 지분 매각 완료 8-K 2026-05-14T15:28Z → 5/14(계약 1.01항 2025-11-17·12-01).
# 투자자 행사 8-K 2026-09-30T15:49Z = 11:49 장중 → 9/30(Fable 권장). 넣지 않은 8-K: 이사 사임·선임(2025-11-12·2026-02-06·7/24), 회사채 $2.0B(3/18·3/23), 주총(4/3), 7.01 자료(2/4·5/4·8/4).
# 의무전환 우선주는 청산 우선액 $1.5B로 뺐다 — 희석 주식 수(10-Q 1,449M 대 발행 1,328M)에는 전환분이 들어가 경제적 가치는 더 클 수 있다(Fable 권장, 판정 불변).
NEWS_RANGE = '2025.12 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 30일 — 네트워크 투자자 행사', '2026-09-30',
     'Juniper 비용 시너지 목표를 연 $600M 이상에서 $800M(FY28 말)으로 올리고, Vultr에서 AMD Helios AI 랙 $1.2B 첫 주문을 받았다고 발표', 'netday', 'HPE 공시 (SEC 8-K 7.01)'),
    ('green', '2026년 9월 2일 장 마감 뒤 — Q3 FY26 실적', '2026-09-03',
     '매출 $12.2B(+34%) · 희석 EPS $1.06(1년 전 $0.21 — 이번 분기에 H3C 지분 매각 이익 $444M) · 영업이익률 11.4%(1년 전 2.7%)', 'q3', 'HPE 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 6월 1일 장 마감 뒤 — Q2 FY26 실적 · Elliott 협약 수정', '2026-06-02',
     '매출 $10.7B(+40%) · 희석 EPS $0.44(1년 전 −$0.82 — 그 분기는 영업권 손상) · 같은 8-K에 Elliott와의 협약 수정(2027년 주총까지 이사회 14명 이하)·Christopher Hsu 이사 선임', 'q2', 'HPE 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 13일 — H3C 지분 매각(5월 28일 잔여분까지 전량)', '2026-05-14',
     '중국 H3C Technologies 지분 13.8%를 5월 13일 약 $987M에, 남은 5.2%를 5월 28일 약 $370M에 넘겼다(2025년 11월 계약) · 8-K는 5/14 장중 접수 — 주가는 전날부터 올라 이 공시만의 반응으로 보기 어렵다', 'h3c', 'HPE 공시 (SEC 8-K)'),
    ('neutral', '2026년 3월 9일 장 마감 뒤 — Q1 FY26 실적', '2026-03-10',
     '매출 $9.3B(+18%) · 희석 EPS $0.31(1년 전 $0.44)', 'q1', 'HPE 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 4일 장 마감 뒤 — Q4 FY25 실적', '2025-12-05',
     '매출 $9.7B(+14%) · 희석 EPS $0.11(1년 전 $0.99) · Juniper 인수를 끝낸 첫 회계연도 마감', 'q4', 'HPE 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 18, 'mean': 73.67, 'median': 72, 'low': 62, 'high': 92, 'sb': 10, 'b': 4, 'h': 10, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-21'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(부문 3개). 원문 대조: Q3 FY26 9,042/2,893/278, 1년 전 7,212/1,654/270(2026-10-21) ──
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
  "hpe:CloudAISegmentMember": [
   "Cloud & AI(서버·스토리지·금융)",
   "#01a982"
  ],
  "hpe:NetworkingMember": [
   "네트워크(Juniper 포함)",
   "#4fd1b1"
  ],
  "us-gaap:CorporateAndOtherMember": [
   "기업 투자·기타",
   "#a8e8d6"
  ]
 },
 "ignore": []
}
