BUILD = {'company_tags': [('mar:DepreciationAmortizationAndOtherExcludingCapitalizedContractCostAmortization', 'DepreciationAmortizationAndAccretionNet'), ('mar:DepreciationAmortizationandOtherExcludingCapitalizedContractCostAmortization', 'DepreciationAmortizationAndAccretionNet')]}   # 손익계산서 감가상각 줄 — 2023-05 공시까지는 'and' 소문자 태그
CIK = '0001048286'
# MAR(메리어트) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 137(시총 135위). 호텔 프랜차이즈·위탁 운영(자산 경량), 로열티 프로그램(Bonvoy).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-03), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 전 접수), StockAnalysis.
# 엔진 입력(2026-10-21): 차입금 $16,915M(1년 안 $460 + 장기 $16,455, 금융리스 포함 — DEBT_TOTAL_TAG; 기본 선택은 LongTermDebt $23M을 잡았다). 현금 $462M = 원문.
# 감가상각은 회사 고유 태그(손익계산서 "Depreciation, amortization, and other" — 계약 투자 상각 제외)를 company_tags로(2023-05까지는 'and' 소문자 태그). 비지배지분 태그 2010년 멈춤 → nci [].
# 감가상각 줄에 2026 Q2 호텔 매각 예정 손상차손 $68M이 들어 있다(10-Q 주석 7) — DCF 순투자가 그만큼 작게 잡힌다(판정 영향 없음). 호텔 계약 취득 현금 지출(상반기 $251M, 영업현금흐름 안)은 DCF 재투자에 따로 안 들어간다 — 엔진 설계(안건 E33 ⑧).
# 자본 음수(자사주 매입 누적) — PBR·부채비율 해당 없음(MO·LOW·SBUX와 같은 일반 경로). 4분기 EPS 2022~2025 보도자료 값.
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Marriott'
S_ = 'https://www.sec.gov/Archives/edgar/data/1048286/'
SEC = S_
TENQ = S_ + '000104828626000035/mar-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q1': S_ + '000104828626000012/mar-2026q1xex99earningsrel.htm', 'q4': S_ + '000104828626000005/mar-2025q4xex99earningsrel.htm',
      'q3': S_ + '000104828625000011/mar-2025q3xex99earningsrel.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="marFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])} — 코로나 저점 기준)</span>'   # Fable 필수 2026-10-21
Y2 = (10, 60)
ACT_REASON = '매출원가 합계 표준 태그가 없음(호텔 위탁·프랜차이즈 — 비용 환급 매출과 환급 비용을 따로 공시)'
NONOP_WHAT = '지분법 투자'
# 고정 문장(숫자 없음). 비용 환급 매출(Codex: 같은 금액이 아니라 인식 시차로 분기 손익), 코로나 저점에서 출발한 장기 성장률(Fable 필수), 감가상각 정의(Codex·Fable).
MODEL_NOTE = ('매출의 대부분은 위탁·프랜차이즈 호텔 비용을 돌려받는 비용 환급 매출이다 — 장기적으로 이익을 남기도록 설계되지 않았지만 인식 시차로 분기 손익이 생기고, '
              '영업이익률·PSR 같은 매출 기준 값은 수수료 사업의 실제 수익성보다 낮게 보인다. 과거 매출 성장률은 코로나로 매출이 크게 줄었던 해에서 출발해 회복분이 크다 — 최근 성장은 그보다 훨씬 낮다. '
              '감가상각은 손익계산서 줄(손상차손 포함, 환급 비용 속 감가상각·계약 투자 상각 제외)이라 EBITDA가 회사 조정 EBITDA와 다르다. 호텔 계약을 따내려고 쓰는 현금(계약 취득 비용)은 이 모델의 재투자에 따로 들어가지 않는다. 자사주 매입으로 자본이 음수라 장부가 기준 배수는 쓰지 않는다.')
# 다음 실적일: 2026-10-09 회사 공지 — 11/2 오전 7시(동부) 발표, 8시 콜(Codex r1 필수)
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-11-02', 'src': '10/9 회사 공지 — 장 시작 전(동부 오전 7시경)'}
PH = ['HLT', 'BKNG', 'EXPE', 'RCL', 'CCL', 'MCD']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '호텔·여행 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': '호텔·여행 PBR 비교', 'psr': '호텔·여행 PSR 비교',
                'pcr': '호텔·여행 PCR(FCF) 비교', 'evebitda': '호텔·여행 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(MAR 제외)와 배수 순위를 매긴 값이다.',
            '유통·자동차·외식·호텔·여행·의류 회사가 섞여 있다. 차트에는 호텔·여행 6곳(맥도날드는 프랜차이즈 비교)만 보인다.')
# 매출(Q2 2026 10-Q 주석 10 부문 매출 — 비용 환급 매출 포함) — 미국·캐나다 5,263 + EMEA 610 + 중화권 164 + 아태(APEC) 273 = 6,310, 본사·기타 761을 더해 7,071.
# 1년 전 4,962/655/152/256, 본사 719 → 6,744.
SEG = [('미국·캐나다', 5263, '#8c1d40'), ('유럽·중동·아프리카', 610, '#c0506f'), ('아시아·태평양(중국 제외)', 273, '#e3a1b4'), ('중화권', 164, '#f2c9d5')]
SEG_ADJ = 761
SEG_TITLE = '매출 구성 — 지역 부문별(비용 환급 매출 포함)'
SEG_ADJ_LABEL = '본사·기타(신용카드 수수료 등)'
# 손 뉴스: 최신 실적(Q2 2026, 8/3 장 전)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤 손 항목 없음(8/13 회사채·9/24 신용 약정은 넣지 않음). 가이던스·조정 EPS·RevPAR 전망은 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K는 모두 장 전 — Q1 5/6 11:00 → 5/6, Q4 2/10 12:00 → 2/10, Q3 11/4 12:00 → 11/4.
# 넣지 않은 8-K: 임원(1/9 미국·캐나다 사장 은퇴, 2/6 이사), 회사채(2/20·8/13), 주총(5/13), 신용 약정(9/24).
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('green', '2026년 5월 6일 — Q1 2026 실적', '2026-05-06',
     '매출 $6.65B(+6%) · 희석 EPS $2.43(1년 전 $2.39) · 전 세계 객실당 매출(RevPAR) +4.2% · 순객실 1년 새 +4.5%', 'q1', 'Marriott 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 10일 — Q4 2025 실적', '2026-02-10',
     '매출 $6.69B(+4%) · 희석 EPS $1.65(1년 전 $1.63) · 2025년 매출 $26.19B·EPS $9.51 · 4분기 RevPAR 전 세계 +1.9%(미국·캐나다 −0.1%)', 'q4', 'Marriott 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 4일 — Q3 2025 실적', '2025-11-04',
     '매출 $6.49B(+4%) · 희석 EPS $2.67(1년 전 $2.07) · RevPAR 전 세계 +0.5%(미국·캐나다 −0.4%, 해외 +2.6%)', 'q3', 'Marriott 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 29, 'nt': 20, 'mean': 394.35, 'median': 400, 'low': 343, 'high': 426, 'sb': 13, 'b': 1, 'h': 13, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-21'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(지역 부문 4개, 부문 매출 — 비용 환급 매출 포함). 본사·기타는 SEG_ADJ(분기마다 다시 정함).
# 원문 대조: Q2 2026 5,263/610/273/164(본사 761), 1년 전 4,962/655/256/152(본사 719)(2026-10-21) ──
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
  "mar:USAndCanadaSegmentMember": [
   "미국·캐나다",
   "#8c1d40"
  ],
  "mar:EMEASegmentMember": [
   "유럽·중동·아프리카",
   "#c0506f"
  ],
  "mar:APECMember": [
   "아시아·태평양(중국 제외)",
   "#e3a1b4"
  ],
  "mar:GreaterChinaMember": [
   "중화권",
   "#f2c9d5"
  ]
 },
 "ignore": []
}
