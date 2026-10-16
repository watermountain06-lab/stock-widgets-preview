# SYK(스트라이커) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 111.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-31), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 마감 뒤 접수, 동부 20~21시), 8-K(사장·COO 선임 2025-12-04,
# 사이버 보안 사고 2026-03-11, CEO 교체 2026-10-06), StockAnalysis.
# 엔진 입력(2026-10-16): 감가상각은 현금흐름표 "Depreciation" + "Amortization of intangible assets"(구성요소 경로) — DepreciationDepletionAndAmortization(부문 주석 전체 D&A)은
# 분기 값이 2024년부터라 EV/EBITDA 이력이 짧고 DCF와 정의가 어긋나 EXCLUDE_TAGS(build_multiple_history). 4분기 EPS는 역산 = 보도자료(2025 $2.20·2024 $1.41).
# 차입금 = 유동(DebtCurrent, 기업어음 포함) + 비유동(DEBT_TOTAL_TAG). 비지배지분 태그가 2018년($9M)에 멈춰 EV_TAGS_BY_CIK nci = [](지금 재무상태표에 줄 없음).
# 감가상각을 현금흐름표 기준으로 둔 이유(잠정): 대여 수술기구 상각은 판관비에 있고(10-K 회계정책), 그 구입비는 설비투자 줄에 없다 — 영업현금흐름 어디에 있는지는
# 공시로 확정하지 못했다(추정 — Codex 2차). 전체 D&A를 DCF 순투자에 쓰면 상각만 되돌리고 구입비는 못 뺄 수 있어 현금흐름표 두 줄을 쓴다.
# EBITDA는 부문 주석 전체 D&A($404M)보다 분기 약 $108M 낮게 잡힌다(공통 안건 — EBITDA·DCF 감가상각 분리, Codex 2026-10-16).
CIK = '0000310764'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Stryker'
S_ = 'https://www.sec.gov/Archives/edgar/data/310764/'
SEC = S_
TENQ = S_ + '000031076426000050/syk-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000031076426000048/sykex991earningsq22026.htm', 'q1': S_ + '000031076426000025/sykex991earningsq12026.htm',
      'q4': S_ + '000031076426000006/sykex991earningsq42025.htm', 'q3': S_ + '000031076425000126/sykex991earningsq32025.htm'}
LINKS = {'ceo': S_ + '000119312526414956/d84795d8k.htm', 'cyber': S_ + '000119312526102460/d76279d8k.htm',
         'coo': S_ + '000119312525308097/d78127d8k.htm'}
FAIRBAND_TITLE = 'id="sykFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (5, 30)
ACT_REASON = ''
BB_NONE = {'2026-06-30': '프로그램 매입 없음 · 10-Q 주석'}   # 현금흐름표 매입 줄·태그 없음 — Q2 2026 10-Q "did not repurchase any shares"(상반기), 남은 승인 $1,033M. 새 10-Q마다 주석 확인
NONOP_WHAT = '장기투자'
PH = ['BSX', 'MDT', 'ABT', 'ISRG', 'ZBH', 'BDX']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {'evebitda': ' · SYK EBITDA는 현금흐름표 감가상각 기준(판관비 안 대여 수술기구 상각 등 제외)이라 부문 주석 전체 감가상각 기준보다 배수가 높게 나온다'}
CHART_TITLES = {'per': '의료기기 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': '의료기기 PBR 비교', 'psr': '의료기기 PSR 비교',
                'pcr': '의료기기 PCR(FCF) 비교', 'evebitda': '의료기기 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(SYK 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·유통 회사가 섞여 있다. 보험·유통 회사는 매출이 커 PSR이 낮게 나온다. 차트에는 의료기기 6곳만 보인다.')
# 부문(Q2 2026 10-Q 부문 주석) — 의료·수술·신경 3,625 + 정형외과 2,964 = 연결 매출 6,589(1년 전 3,305 + 2,717 = 6,022, 2026년 조직 개편 반영 재작성).
SEG = [('의료·수술·신경', 3625, '#e3a008'), ('정형외과', 2964, '#3a3a3a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: Q2 2026 실적(7/30)도 손으로 쓴다 — 그 뒤 CEO 교체(10/6)를 넣으면 자동 실적 항목이 빠지기 때문(README). 가이던스는 손 뉴스에 쓰지 않는다.
# 반응일: 실적 8-K는 동부 20~21시 접수 → 다음 거래일. 사이버 사고 8-K는 3/11 21:24(동부) → 3/12. CEO 교체 8-K는 10/6 12:08(장중) → 10/6.
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 6일 — CEO 교체 결정', '2026-10-06',
     'Kevin Lobo(의장·CEO)가 2026년 말 CEO에서 물러나 2027년 1월 1일부터 상근 이사회 의장(Executive Chair) · Spencer Stiles(사장·COO)가 CEO', 'ceo', 'Stryker 공시 (SEC 8-K)'),
    ('red', '2026년 7월 30일 장 마감 뒤 — Q2 2026 실적', '2026-07-31',
     '매출 $6.59B(+9.4%) · 희석 EPS $3.30(1년 전 $2.29)', 'q2', 'Stryker 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 30일 장 마감 뒤 — Q1 2026 실적', '2026-05-01',
     '매출 $6.02B(+2.6%) · 희석 EPS $1.93(1년 전 $1.69) · 3월 사이버 사고가 있던 분기', 'q1', 'Stryker 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 11일 장 마감 뒤 — 사이버 보안 사고 공시', '2026-03-12',
     'Microsoft 환경 전반 중단 · 공시 시점에 랜섬웨어·악성코드 징후 없다고 판단, 중대성 판단 안 함', 'cyber', 'Stryker 공시 (SEC 8-K)'),
    ('green', '2026년 1월 29일 장 마감 뒤 — Q4 2025 실적', '2026-01-30',
     '매출 $7.17B(+11.4%) · 희석 EPS $2.20(1년 전 $1.41) · 2025년 EPS $8.40', 'q4', 'Stryker 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 4일 장 마감 뒤 — 사장·COO 선임', None,
     'Spencer Stiles(정형외과 그룹 사장) 2026년 1월 1일부터 사장·COO · 후임 정형외과 그룹 사장 Dylan Crotty', 'coo', 'Stryker 공시 (SEC 8-K)'),
    ('red', '2025년 10월 30일 장 마감 뒤 — Q3 2025 실적', '2025-10-31',
     '매출 $6.06B(+10.3%) · 희석 EPS $2.22(1년 전 $2.16)', 'q3', 'Stryker 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Buy', 'n': 29, 'nt': 24, 'mean': 364.83, 'median': 370, 'low': 298, 'high': 420, 'sb': 15, 'b': 8, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-16'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-Q 부문 주석 Q2 2026 3,625/2,964, 1년 전 3,305/2,717, 합 = 연결 매출(6,589·6,022)(2026-10-16) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:Revenues"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "syk:MedSurgAndNeurotechnologyMember": [
   "의료·수술·신경",
   "#e3a008"
  ],
  "syk:OrthopaedicsAndSpineMember": [
   "정형외과",
   "#3a3a3a"
  ]
 },
 "ignore": []
}
