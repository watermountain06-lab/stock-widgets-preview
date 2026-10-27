# HCA(HCA 헬스케어) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 미국 최대 영리 병원 운영사 — 병원 약 190곳, 외과 센터·응급실(National·American·Atlantic 3개 그룹).
# 출처: SEC XBRL + 인라인 XBRL 보충(BUILD overlay — companyfacts에 7/28 Q2 10-Q가 없다), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/HCA.md.
# 엔진 입력(2026-10-25): 영업이익 = 세전이익 + 이자비용(DERIVED_OPINC — 손익계산서에 영업이익 줄이 없다), 차입금 = 총차입금 $49,718M(DEBT_TOTAL_TAG — CP·1년 안 포함), 현금 $1,013M, 비지배지분 $3,433M(병원 합작 지분).
# 일회성: 회사 조정은 시설 매각 손익뿐(최근 4분기 주당 −0.16, 약 0.5%). Q2 2026에 플로리다 메디케이드 지정 지급 소급분(2024-10~2025년분 세전 약 $423M, 회사 조정 안 함)이 들어 있다 — 주당 약 1.2(추정).
BUILD = {'overlay': True}
CIK = '0000860730'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -1), '적정'
CO = 'HCA'
S_ = 'https://www.sec.gov/Archives/edgar/data/860730/'
SEC = S_
TENQ = S_ + '000119312526321077/hca-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000119312526315151/hca-ex99_1.htm', 'q1': S_ + '000119312526174933/hca-ex99_1.htm',
      'q4': S_ + '000119312526023323/hca-ex99_1.htm', 'q3': S_ + '000119312525249345/hca-ex99_1.htm',
      'pre': S_ + '000119312526302539/hca-ex99_1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="hcaFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('손익계산서에 영업이익 줄이 없어 세전이익에 이자비용을 더해 영업이익으로 쓴다(시설 매각 손익은 영업으로 둔다). '
              '자사주를 많이 사서 주주 자본이 마이너스(−$6.6B)라 PBR·부채비율은 해석하기 어렵다. 병원 합작 지분(비지배지분 $3.4B)은 기업가치에서 뺀다. '
              'Q2 2026 이익에는 플로리다 메디케이드 지정 지급의 지난 기간분(세전 약 $423M)이 들어 있다. SEC 요약 자료에 최신 10-Q가 아직 없어 원문 인라인 XBRL로 채웠다.')
HEALTH_EXTRA = '자사주 매입으로 주주 자본이 마이너스라 부채비율 같은 자본 기준 비율은 숫자가 크게 나오거나 계산되지 않는다.'
PH = ['UNH', 'CVS', 'ELV', 'MCK', 'COR', 'ISRG']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '헬스케어 서비스 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(HCA 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·유통·병원이 섞여 있다. 차트에는 헬스케어 서비스 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — Atlantic 7,573 + American 6,582 + National 5,251 = 19,406, 본사·기타 824 → 20,230.
SEG = [('Atlantic 그룹', 7573, '#e05206'), ('American 그룹', 6582, '#f5a26b'), ('National 그룹', 5251, '#3c3c3c')]
SEG_ADJ = 824
SEG_SUM_LABEL, SEG_ADJ_LABEL = '3개 그룹 합', '본사·기타 매출'
SEG_TITLE = '매출 구성 — 지역 그룹별(Q2 2026)'
# 손 뉴스: 실적 4건 + Q2 사전 발표(가이던스 하향). 반응일: 장 전 발표(07:10~07:45 동부) → 같은 날. 넣지 않은 8-K: 사채 발행·상환, CP 한도, 임원, 주총.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 24일 장 전 — Q2 2026 실적', '2026-07-24',
     '매출 $20.23B(+8.7%) · 순이익 $1.70B · 희석 EPS $7.62(1년 전 $6.83) — 플로리다 메디케이드 지정 지급 소급분 포함', 'q2', 'HCA 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 14일 장 전 — Q2 사전 발표·연간 전망 하향', '2026-07-14',
     '연간 희석 EPS 전망 $28.70~30.50으로 낮춤(이전 $29.10~31.50) — 건강보험 거래소 가입자 이탈, 당일 주가 −7%', 'pre', 'HCA 사전 발표 (SEC 8-K)'),
    ('red', '2026년 4월 24일 장 전 — Q1 2026 실적', '2026-04-24',
     '매출 $19.11B · 순이익 $1.62B · 희석 EPS $7.15(1년 전 $6.45) — 당일 주가 −9%', 'q1', 'HCA 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 27일 장 전 — Q4 2025 실적', '2026-01-27',
     '매출 $19.51B · 순이익 $1.88B · 희석 EPS $8.14(1년 전 $5.63) · 2025년 EPS $28.33 — 당일 주가 +7%', 'q4', 'HCA 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 24일 장 전 — Q3 2025 실적', '2025-10-24',
     '매출 $19.16B · 순이익 $1.64B · 희석 EPS $6.96(1년 전 $4.88)', 'q3', 'HCA 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 26, 'nt': 21, 'mean': 462.05, 'median': 475, 'low': 380, 'high': 579, 'sb': 14, 'b': 1, 'h': 9, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 지역 그룹 3개(영업 부문 차원), 본사·기타 824는 SEG_ADJ. 원문 대조: Q2 2026 7,573/6,582/5,251(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"hca:AtlanticGroupMember": ["Atlantic 그룹", "#e05206"], "hca:AmericanGroupMember": ["American 그룹", "#f5a26b"],
             "hca:NationalGroupMember": ["National 그룹", "#3c3c3c"]},
 "ignore": []
}
