# WTW(윌리스 타워스 왓슨) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 보험 중개·위험 자문(R&B) + 보건·퇴직·인재 컨설팅(HWC) 2개 부문. 아일랜드 법인.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-29 12:01 동부 장중 → 같은 날), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 모두 06시 무렵 장 전 → 같은 날 반응). 사전 조사 scratchpad pre/WTW.md.
# 엔진 입력(2026-11-05): FY2023·2024·2025 10-K가 연간 총 EPS를 중단영업 EPS 태그에도 붙여(9.95·−0.96·16.26) 배수 엔진이 4분기에서 빼 최근 4분기 EPS 0.01(PER 33,737배)이 나왔다 —
# 중단영업은 없다. Q4_EPS_OVERRIDE(보도자료 7.62·12.25, 2023 역산 5.90) + Q4_OVERRIDE_BASIS "continuing"으로 막았다. 순이익은 WTW 귀속 NetIncomeLoss(비지배 $76M).
# 차입 $6,532M = LongTermDebtCurrent 749 + Noncurrent 5,783(축 없는 LongTermDebt $9,685M은 10-K 만기표에 미래 이자를 더한 값이라 쓰지 않는다). 수탁 자산 $11,057M = 수탁 부채(회사 고유 태그), 수탁 현금 $3,410M은 엔진 현금($1,946M) 밖.
# 설비투자는 2019~2024 회사 고유 태그 + PaymentsToDevelopSoftware로 나뉘었다가 PaymentsToAcquireProductiveAssets로 합쳐져(소급 재분류) PCR 이력이 FY2025 10-K(2026-02-25) 뒤 176거래일뿐이다.
# 인수: Newfront(2026-01-27, 선지급 $1.05B), Cushon(04-30). TRANZACT 매각(2024-12-31)은 중단영업이 아니다.
CIK = '0001140536'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'WTW'
S_ = 'https://www.sec.gov/Archives/edgar/data/1140536/'
SEC = S_
TENQ = S_ + '000119312526437327/wtw-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000117184326006942/exh_991.htm', 'q2': S_ + '000117184326005042/exh_991.htm',
      'q1': S_ + '000117184326002866/exh_991.htm', 'q4': S_ + '000117184326000577/exh_991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="wtwFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (10, 35)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('자기 이력의 PCR은 FY2025 10-K(2026년 2월 25일) 뒤만 계산된다 — 그 전 설비투자가 회사 고유 태그로 나뉘어 있다가 한 줄로 합쳐져(소급 재분류) SEC 요약 자료에서 이어지지 않는다. '
              '10-K가 연간 총 EPS를 중단영업 EPS 태그에도 붙여 두어(실제 중단영업은 없다) 4분기 EPS는 보도자료 값을 쓴다. 보수 시나리오가 낮은 것은 5년 영업이익률 중앙값에 2024년 TRANZACT 손상·처분손실이 들어 있고 최근 1년 인수 지출을 재투자로 세기 때문이다.')
HEALTH_EXTRA = '유동비율·부채비율에는 고객 수탁 자산과 수탁 부채(같은 금액)가 들어 있어 실제 지급능력보다 나쁘게 나온다.'
PH = ['AJG', 'AON', 'MRSH', 'BRO', 'SPGI', 'MCO']
PEER_FILE = 'peer_universe/brokers_fees.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '보험 중개·금융 데이터 6곳 PER 비교 (점수는 중개사 + 결제·거래소·데이터 기준)', 'pbr': '보험 중개·금융 데이터 PBR 비교', 'psr': '보험 중개·금융 데이터 PSR 비교',
                'pcr': '보험 중개·금융 데이터 PCR(FCF) 비교', 'evebitda': '보험 중개·금융 데이터 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 보험 중개사와 결제·거래소·금융 데이터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 보험 중개 + 결제·거래소·금융 데이터 대비 배수 순위 (v2/peer_universe/brokers_fees.json)'
PEER_TIP = ('S&P500 보험 중개사(WTW 제외 4곳)와 결제·거래소·금융 데이터 회사(수수료로 버는 자산 경량 서비스)와 배수 순위를 매긴 값이다 — 중개사만으로는 비교 표본(8곳)이 모자란다.',
            '결제 처리·카드 네트워크·거래소가 섞여 있어 성장·마진 구조가 다르다. 차트에는 보험 중개·금융 데이터 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 표, 영업 부문 Revenues) — HWC 1,350 + R&B 1,087 = 2,437, 본사·환급 21 + 이자 2는 SEG_ADJ — 합 2,460.
SEG = [('보건·퇴직·인재 컨설팅(HWC)', 1350, '#702082'), ('위험 자문·보험 중개(R&B)', 1087, '#2c1b4f')]
SEG_ADJ = 23
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: Q3 2026 실적(10/29)은 news_auto가 SEC 숫자로 붙인다. 반응일: 장 전 발표 → 같은 날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('green', '2026년 7월 30일 장 전 — Q2 2026 실적', '2026-07-30',
     '매출 $2.47B(+9.1%) · 희석 EPS $2.43(1년 전 $3.32) · 조정 EPS $3.35 — 당일 주가 +6.4%', 'q2', 'WTW 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 30일 장 전 — Q1 2026 실적', '2026-04-30',
     '매출 $2.41B(+8.5%) · 희석 EPS $3.10(1년 전 $2.33) · 조정 EPS $3.72 — 당일 주가 −11.7%', 'q1', 'WTW 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 3일 장 전 — Q4 2025 실적', '2026-02-03',
     '매출 $2.94B · 희석 EPS $7.62(1년 전 $12.25) · 조정 EPS $8.12 — 당일 주가 +5.8%', 'q4', 'WTW 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 18, 'mean': 372.17, 'median': 370, 'low': 325, 'high': 455, 'sb': 12, 'b': 2, 'h': 7, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-05'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(영업 부문 Revenues, 손 표와 일치, 2026-11-05) ──
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
  "wtw:HealthWealthAndCareerMember": [
   "보건·퇴직·인재 컨설팅(HWC)",
   "#702082"
  ],
  "wtw:RiskAndBrokingMember": [
   "위험 자문·보험 중개(R&B)",
   "#2c1b4f"
  ]
 },
 "ignore": []
}
