# CVS(CVS 헬스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 109.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 시작 전 접수), 8-K(이사회 의장 선임 2025-11-20), StockAnalysis.
# 엔진 입력(2026-10-15): 순투자수익(Net investment income)이 매출·영업이익 안이라 장기투자 $33.2B는 보험 자산(건강보험·본사 보험 사업) — 비영업 자산에 더하지 않는다
# (build_dcf INVESTMENTS_OPERATING, UNH와 같은 처리). 차입금 = 단기차입 + 1년 안 만기 + 장기(리스 포함 태그 — 금융리스 $1.3B가 재무상태표 장기차입금 두 줄 안,
# build_multiple_history DEBT_TOTAL_TAG). 4분기 EPS 보도자료 값(2025 $2.30). 최근 4분기 순이익률 2% 미만이라 PER은 점수에서 빠진다(A3).
# 최근 4분기 영업이익에 2025년 3분기 영업권 손상 $5.7B(Health Care Delivery — Oak Street·Signify)가 들어 있어 현금흐름 내재가치가 음수다(일회성 빼기는 판정 계산 규칙 — 손대지 않음).
CIK = '0000064803'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'CVS Health'
S_ = 'https://www.sec.gov/Archives/edgar/data/64803/'
SEC = S_
TENQ = S_ + '000006480326000098/cvs-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q1': S_ + '000006480326000051/cvs_ex99x1q1-26.htm', 'q4': S_ + '000006480326000009/cvs_ex99x1q4-25.htm',
      'q3': S_ + '000006480325000036/cvs_ex99x1q3-25.htm'}
LINKS = {'chair': S_ + '000119312525289805/d172430dex991.htm'}
FAIRBAND_TITLE = 'id="cvsFairBand" title="최근 1년 PER 25~75% 구간 × 최근 4분기 희석 EPS. 최근 4분기 순이익률이 2% 미만이라 PER은 점수에 쓰지 않는다(A3) — 범위는 참고로만 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-4, 6)
ACT_REASON = ''
BB_NONE = {'2026-06-30': '없음 · 10-Q 주석'}   # 현금흐름표 줄·태그 없음 — Q2 2026 10-Q "did not repurchase any shares"(상반기), 남은 승인 $11.5B. 그 분기에만 쓰인다 — 새 10-Q마다 주석을 확인해 줄을 더한다
NONOP_WHAT = '지분·장기투자'
PH = ['UNH', 'ELV', 'CI', 'HUM', 'CNC', 'MCK']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '헬스케어 6곳 PER 비교 — HUM·CNC·MCK는 순이익률 2% 미만이라 PER 없음', 'pbr': '헬스케어 PBR 비교', 'psr': '헬스케어 PSR 비교',
                'pcr': '헬스케어 PCR(FCF) 비교', 'evebitda': '헬스케어 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(CVS 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·유통 회사가 섞여 있다. 보험·약국·유통 회사는 매출이 커 PSR이 낮게 나온다. 차트에는 보험·유통 6곳만 보인다.')
# 부문(Q2 2026 10-Q 부문 주석, 외부 고객 매출) — 건강보험 36,999 + 의료 서비스 45,389 + 약국·소비자 23,054 + 본사·기타 13 = 105,455,
# 여기에 순투자수익 641을 더하면 연결 매출 106,096. 본사·기타($13M)는 뺀다.
SEG = [('의료 서비스', 45389, '#cc0000'), ('건강보험', 36999, '#7a1fa2'), ('약국·소비자', 23054, '#e07b39')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(외부 고객, 순투자수익·본사 제외)'
# 손 뉴스: Q2 2026 실적(8/5)은 news_auto가 SEC 숫자로 붙인다 — 그보다 뒤 손 항목(8/17 이사회 변경)은 넣지 않았다(README).
# 가이던스는 손 뉴스에도 쓰지 않는다 — 자동 실적 항목에는 가이던스가 없어 옛 전망이 마지막으로 보인다(Codex 2026-10-15, 투자자의 날 항목도 뺌).
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('green', '2026년 5월 6일 — Q1 2026 실적', '2026-05-06',
     '매출 $100.4B(+6.2%) · 희석 EPS $2.30(1년 전 $1.41)', 'q1', 'CVS Health 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 10일 — Q4 2025 실적', '2026-02-10',
     '매출 $105.7B(+8.2%) · 희석 EPS $2.30(1년 전 $1.30) · 2025년 EPS $1.39', 'q4', 'CVS Health 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 20일 장 마감 뒤 — CEO의 이사회 의장 겸임 결정', '2025-11-21',
     'David Joyner CEO가 2026년 1월 1일부터 의장 · Roger Farah(현 의장)는 이사로 남음', 'chair', 'CVS Health 공시 (SEC 8-K)'),
    ('red', '2025년 10월 29일 — Q3 2025 실적', '2025-10-29',
     '매출 $102.9B(+7.8%) · 희석 EPS −$3.13(1년 전 $0.07) — Health Care Delivery 영업권 손상 $5.7B 포함 · 9월 22일 Omnicare 파산 신청으로 연결 제외(이익 $483M)', 'q3', 'CVS Health 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Strong Buy', 'n': 27, 'nt': 21, 'mean': 113, 'median': 113, 'low': 92, 'high': 125, 'sb': 18, 'b': 7, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-17'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-Q 부문 주석 외부 고객 매출 Q2 2026 36,999/45,389/23,054, 1년 전 35,831/40,118/22,466,
# 본사·기타 13·13은 ignore. 순투자수익(641·487)은 부문 외부 매출 밖이라 합 = 연결 매출 − 순투자수익(2026-10-15) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "cvs:PremiumsEarnedNetAndRevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "cvs:HealthServicesSegmentMember": [
   "의료 서비스",
   "#cc0000"
  ],
  "cvs:HealthCareBenefitsSegmentMember": [
   "건강보험",
   "#7a1fa2"
  ],
  "cvs:PharmacyAndConsumerHealthSegmentMember": [
   "약국·소비자",
   "#e07b39"
  ]
 },
 "ignore": [
  "cvs:CorporateAndOtherSegmentMember"
 ]
}
