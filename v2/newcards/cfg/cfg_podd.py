# PODD(인슐렛) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 튜브 없는 착용형 인슐린 펌프 Omnipod(미국·해외), 약물 전달 기기(소규모).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/PODD.md.
# 엔진 입력(2026-10-25): 차입금 = 1년 안 포함 합계 $948.4M(DEBT_TOTAL_TAG), 현금 = 제한 현금 포함 줄 $534.9M(EV_TAGS cash — 기본 태그 2021-09 멈춤).
# 일회성: 자발적 의료기기 시정(MDC) 보증 비용 Q1 2026 $11.7M·Q2 2026 $25.0M(세전, 합계 주당 약 $0.40 세후 — 최근 4분기 EPS의 약 7.5%).
CIK = '0001145197'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -1), '적정'
CO = 'Insulet'
S_ = 'https://www.sec.gov/Archives/edgar/data/1145197/'
SEC = S_
TENQ = S_ + '000114519726000169/podd-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000114519726000167/podd2026-06x30ex991.htm', 'q1': S_ + '000114519726000100/podd2026-03x31ex991.htm',
      'q4': S_ + '000114519726000026/podd202512-31ex991.htm', 'q3': S_ + '000114519725000067/podd2025-09x30ex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="poddFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('매출이 해마다 20% 안팎 늘어 온 성장 기업이라 5년 이력 배수가 높다 — 2025년 이전에는 이익이 작아 PER이 매우 높았다. 주가는 2026년 들어 절반 넘게 내렸다. '
              '최근 4분기 이익에는 자발적 기기 시정 비용(세전 약 $37M)이 들어 있다.')
PH = ['DXCM', 'ABT', 'MDT', 'BSX', 'SYK', 'ISRG']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '의료기기 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(PODD 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·유통·생명과학 도구가 섞여 있다. 차트에는 의료기기 6곳만 보인다.')
# 매출(Q2 2026 10-Q 제품별) — 미국 Omnipod 544.1 + 해외 Omnipod 251.8 + 약물 전달 5.8 = 801.7.
SEG = [('Omnipod — 미국', 544.1, '#005eb8'), ('Omnipod — 해외', 251.8, '#6fa8dc'), ('약물 전달', 5.8, '#8dc63f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품·지역별(Q2 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07:04~07:11 동부 접수) → 같은 날. 넣지 않은 8-K: 신용 계약 개정(9/21), 경영진 교체.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('red', '2026년 8월 5일 — Q2 2026 실적', '2026-08-05',
     '매출 $802M(+23%) · 순이익 $95M · 희석 EPS $1.37(1년 전 $0.32) — 기기 시정 비용 세전 $25.0M 포함, 발표 당일 주가 −20%', 'q2', 'Insulet 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 6일 — Q1 2026 실적', '2026-05-06',
     '매출 $762M · 순이익 $91M · 희석 EPS $1.30(1년 전 $0.50) — 기기 시정 비용 세전 $11.7M 포함, 발표 당일 주가 −10%', 'q1', 'Insulet 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 18일 — Q4 2025 실적', '2026-02-18',
     '매출 $784M · 순이익 $102M · 희석 EPS $1.44(1년 전 $1.39) · 2025년 EPS $3.48', 'q4', 'Insulet 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 6일 — Q3 2025 실적', '2025-11-06',
     '매출 $706M · 순이익 $88M · 희석 EPS $1.24(1년 전 $1.08)', 'q3', 'Insulet 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 26, 'nt': 21, 'mean': 172.81, 'median': 175, 'low': 143, 'high': 216, 'sb': 11, 'b': 4, 'h': 11, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-29'


# ── 자동 카드 — 제품·지역 3개(수동 지도, ProductOmnipodMember는 미국+해외 합계라 뺌). 원문 대조: Q2 2026 544.1/251.8/5.8(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"podd:U.S.OmnipodMember": ["Omnipod — 미국", "#005eb8"], "podd:InternationalOmnipodMember": ["Omnipod — 해외", "#6fa8dc"], "podd:DrugDeliveryMember": ["약물 전달", "#8dc63f"]},
 "ignore": ["podd:ProductOmnipodMember"]
}
