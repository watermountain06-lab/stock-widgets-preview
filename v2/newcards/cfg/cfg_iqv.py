# IQV(아이큐비아) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 제약 임상시험 대행(R&D 솔루션)과 헬스케어 데이터·분석·영업 지원(커머셜 솔루션).
# 출처: SEC XBRL(10/27 Q3 2026 10-Q까지 요약 자료에 있음), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 07시 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/IQV_q3.md.
# 엔진 입력(2026-10-28): 차입금 $16,067M(1년 안 $1,244M 포함 — 순차입 약 $13.8B, 조정 EBITDA의 3.45배), 현금 $2,249M + 단기 시장성 증권 $173M, 비지배지분 $131M, 지분법 투자 $438M.
# 일회성: 회사 조정 EPS는 인수 상각·주식 보상까지 빼서 쓰지 않는다. 그 밖의 조정(구조조정·지분법·기타) 최근 4분기 세전 순 +$104M ≈ 주당 0.62(세전 기준 GAAP 8.23의 약 7.5%).
CIK = '0001478242'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'IQVIA'
S_ = 'https://www.sec.gov/Archives/edgar/data/1478242/'
SEC = S_
TENQ = S_ + '000162828026067646/iqv-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000162828026067406/iqv-q3x2026earningspressre.htm', 'q2': S_ + '000162828026049923/iqv-q2x2026earningspressre.htm',
      'q1': S_ + '000162828026030118/iqv-q1x2026earningspressre.htm', 'q4': S_ + '000162828026005605/iqv-q4x2025earningspressre.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="iqvFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('인수 무형자산 상각(분기 약 $160M)이 커서 GAAP EPS가 회사 조정 EPS의 약 60%다 — 카드는 GAAP를 쓴다. '
              '차입금이 많아(순차입 약 $13.8B) 현금흐름 모델에서 사업 가치의 큰 몫이 빠진다. 2026년 1월 부문을 둘(커머셜·R&D)로 다시 나눠 1년 전 값은 재작성 기준이다. 현금흐름 시나리오는 기본(투하자본 효율 1.62 → 0.84로 낮아짐)이 낙관(0.84 고정, 이익률도 낮음)보다 높게 나온다 — 순차입 약 $13.9B를 빼고 나면 주당 값이 작다.')
PH = ['TMO', 'DHR', 'A', 'MTD', 'IDXX', 'WST']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '생명과학 도구·서비스 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(IQV 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·유통·서비스가 섞여 있다. 차트에는 생명과학 도구·서비스 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — R&D 솔루션 2,639 + 커머셜 솔루션 1,789 = 4,428. 누계는 커머셜을 TechnologyAndAnalyticsSolutionsMember로 태그(같은 부문).
SEG = [('R&D 솔루션(임상 대행)', 2639, '#00396b'), ('커머셜 솔루션(데이터·분석)', 1789, '#3fa9f5')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 27일 장 전 — Q3 2026 실적', '2026-10-27',
     '매출 $4.43B(+8.0%) · 순이익 $350M · 희석 EPS $2.10(1년 전 $1.93) · 2026년 매출 전망 $17.35~17.50B로 올림', 'q3', 'IQVIA 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 28일 장 전 — Q2 2026 실적', '2026-07-28',
     '매출 $4.37B · 순이익 $256M · 희석 EPS $1.53(1년 전 $1.54) — 당일 주가 +13.9%', 'q2', 'IQVIA 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 5일 장 전 — Q1 2026 실적', '2026-05-05',
     '매출 $4.15B · 순이익 $274M · 희석 EPS $1.61(1년 전 $1.40) — 당일 주가 +9.6%', 'q1', 'IQVIA 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 5일 장 전 — Q4 2025 실적', '2026-02-05',
     '매출 $4.36B · 순이익 $514M · 희석 EPS $2.99(1년 전 $2.42) · 2025년 EPS $7.84 — 당일 주가 −10.7%', 'q4', 'IQVIA 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 20, 'nt': 15, 'mean': 309.2, 'median': 310, 'low': 240, 'high': 346, 'sb': 16, 'b': 2, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-31'


# ── 자동 카드 — 부문 2개(누계는 커머셜을 TechnologyAndAnalyticsSolutionsMember로 태그해 ignore — 분기 값만 쓴다). 원문 대조: Q3 2026 2,639/1,789(2026-10-28) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"iqv:ResearchAndDevelopmentSolutionsMember": ["R&D 솔루션(임상 대행)", "#00396b"],
             "iqv:CommercialSolutionsMember": ["커머셜 솔루션(데이터·분석)", "#3fa9f5"]},
 "ignore": ["iqv:TechnologyAndAnalyticsSolutionsMember"]
}
