# AOS(A. O. 스미스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 가정용·상업용 온수기와 보일러(북미), 온수기·정수기(중국·인도 등 해외).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/AOS.md.
# 엔진 입력(2026-10-25): 기본 경로 — 차입금 1년 안 $39.5M + 장기 $598.0M(Leonard Valve 인수용 기간 대출 $470M 포함), 현금 $181.3M. 인수 = 최근 4분기 $470M(Leonard Valve 2026-01-06).
# 일회성 작음(Q2 2026 구조조정·손상 세전 $22.6M, 주당 $0.12 — 최근 4분기 EPS의 약 3%).
BUILD = {'cover_shares': True}   # 보통주 + Class A 두 클래스 — 표지 주식 수가 클래스별뿐이라 한 클래스(75.7M)만 잡혔다(희석 가중 약 138M, META·NKE·DDOG 방식)
CIK = '0000091142'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, -1), '적정~저평가'
CO = 'A. O. Smith'
S_ = 'https://www.sec.gov/Archives/edgar/data/91142/'
SEC = S_
TENQ = S_ + '000009114226000098/aos-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000009114226000096/a6302026exhibit991.htm', 'q1': S_ + '000009114226000082/a3312026exhibit991.htm',
      'q4': S_ + '000009114226000005/a12312025exhibit991.htm', 'q3': S_ + '000009114225000148/a9302025exhibit991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="aosFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('북미 온수기 교체 수요가 매출의 대부분이라 경기에 덜 흔들리지만, 중국 소비 부진으로 해외 부문 매출이 줄고 있다. '
              'Leonard Valve 인수($470M, 2026-01)가 최근 4분기 투자에 들어 있어 투자 효율이 매우 낮게 잡힌다 — 보수 시나리오가 음수이고 요구 성장률이 음수로 나오는 이유다 — 이 낮은 효율에서는 성장이 가치를 깎아 역성장(−39%)과 고성장(+45%) 둘 다 현재가를 맞추는 해가 되므로 요구 성장률은 해석하지 않는다(인수를 빼면 비율 약 1.35). 운용리스는 순현금 칸에만 넣고 현금흐름 모델에서는 영업비용으로 본다. 현금흐름 비율은 문턱 1.5에 가까워 주식 수를 희석 가중으로 쓰면 −2로 바뀐다. 2026년 4월 북미 정수 사업 구조조정을 발표했다. Q3 2026 실적이 10월 말 나올 예정이다.')
PH = ['CARR', 'TT', 'LII', 'JCI', 'MAS', 'ALLE']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '건물 설비 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(AOS 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 건물 설비 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 외부 매출) — 북미 816.3 + 해외 188.0 = 1,004.3.
SEG = [('북미', 816.3, '#00539b'), ('해외(중국·인도 등)', 188.0, '#c8102e')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q2 2026, 외부 매출)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:57~06:58 동부 접수) → 같은 날. 넣지 않은 8-K: 기간 대출(1/6), 주총.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 30일 — Q2 2026 실적', '2026-07-30',
     '매출 $1.00B · 순이익 $125M · 희석 EPS $0.91(1년 전 $1.07) — 구조조정·손상 세전 $22.6M 포함', 'q2', 'A. O. Smith 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 30일 — Q1 2026 실적', '2026-04-30',
     '매출 $946M · 순이익 $118M · 희석 EPS $0.85(1년 전 $0.95) — Leonard Valve 인수 비용 포함', 'q1', 'A. O. Smith 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 29일 — Q4 2025 실적', '2026-01-29',
     '매출 $913M · 순이익 $125M · 희석 EPS $0.90(1년 전 $0.75) · 2025년 EPS $3.85 — 발표 당일 주가 +5%', 'q4', 'A. O. Smith 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 28일 — Q3 2025 실적', '2025-10-28',
     '매출 $943M · 순이익 $132M · 희석 EPS $0.94(1년 전 $0.82)', 'q3', 'A. O. Smith 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 13, 'nt': 8, 'mean': 64.38, 'median': 67, 'low': 55, 'high': 72, 'sb': 2, 'b': 1, 'h': 8, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 2개(수동 지도, 외부 매출 — 영업 부문 차원 없는 값). 원문 대조: Q2 2026 816.3/188.0(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"aos:NorthAmericaSegmentMember": ["북미", "#00539b"], "aos:RestOfWorldMember": ["해외(중국·인도 등)", "#c8102e"]},
 "ignore": ["aos:ReportableSegmentsMember"]
}
