# JBHT(J.B. 헌트) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 철도 연계 컨테이너 운송(인터모달, JBI), 전용 트럭 계약 운송(DCS), 화물 중개(ICS), 트럭 운송(JBT), 최종 배송(FMS).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-23 장중), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/JBHT.md.
# 엔진 입력(2026-10-25): 기본 경로 — 차입금 장기 $1,123.8M(1년 안 0), 현금 $3.75M. 일회성 거의 없음(분기 세율 차이만).
CIK = '0000728535'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'J.B. Hunt'
S_ = 'https://www.sec.gov/Archives/edgar/data/728535/'
SEC = S_
TENQ = S_ + '000143774926033365/jbht20260930_10q.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000143774926032715/ex_1025956.htm', 'q2': S_ + '000143774926023629/ex_987956.htm',
      'q1': S_ + '000143774926012396/ex_945603.htm', 'q4': S_ + '000143774926001357/ex_907715.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="jbhtFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 15)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('트럭 운임 사이클에 따라 이익이 크게 오르내린다 — 2022년 고점 뒤 2023~2024년 이익이 줄었다가 회복 중이라 5년 이력에 그 고점이 섞여 있다. '
              '매출에는 연료 할증료(Q3 2026 $671M, 1년 전보다 74% 증가)가 들어 있어 유가에 따라 매출 성장률이 부풀거나 줄어든다(Q3 성장률: 포함 20.4%, 제외 12.7%) — PSR과 현금흐름 모델 성장률도 할증료 포함 기준이다. '
              '리스 부채는 2025년 말 값이다(10-Q는 리스를 태깅하지 않음).')
PH = ['ODFL', 'UNP', 'CSX', 'NSC', 'EXPD', 'UPS']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '운송 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(JBHT 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 운송 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문, 부문 간 거래 제거 전) — JBI 1,827.6 + DCS 960.2 + ICS 433.8 + JBT 260.8 + FMS 200.1 = 3,682.5, 제거 −5.7 → 3,676.8.
SEG = [('인터모달(JBI)', 1827.6, '#c8102e'), ('전용 트럭(DCS)', 960.2, '#e8707f'), ('화물 중개(ICS)', 433.8, '#1d1d1b'), ('트럭 운송(JBT)', 260.8, '#f5a3a3'), ('최종 배송(FMS)', 200.1, '#8a8a8a')]
SEG_ADJ = -5.7
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:19~16:26 동부 접수) → 다음 거래일. 넣지 않은 8-K: 신용 계약, 나스닥 텍사스 이중 상장, 주총.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 15일 장 마감 뒤 — Q3 2026 실적', '2026-10-16',
     '매출 $3.68B(+20%, 연료 할증료 포함) · 순이익 $172M · 희석 EPS $1.82(1년 전 $1.76)', 'q3', 'J.B. Hunt 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 15일 장 마감 뒤 — Q2 2026 실적', '2026-07-16',
     '매출 $3.50B · 순이익 $181M · 희석 EPS $1.91(1년 전 $1.31) — 다음 날 주가 +8%', 'q2', 'J.B. Hunt 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 15일 장 마감 뒤 — Q1 2026 실적', '2026-04-16',
     '매출 $3.06B · 순이익 $142M · 희석 EPS $1.49(1년 전 $1.17) — 다음 날 주가 +6%', 'q1', 'J.B. Hunt 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 15일 장 마감 뒤 — Q4 2025 실적', '2026-01-16',
     '순이익 $181M · 희석 EPS $1.90(1년 전 $1.53 — 무형자산 손상 포함) · 2025년 EPS $6.12', 'q4', 'J.B. Hunt 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 20, 'mean': 283.55, 'median': 289, 'low': 195, 'high': 325, 'sb': 12, 'b': 3, 'h': 7, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 5개(수동 지도, 영업 부문 차원). 원문 대조: Q3 2026 1,827.6/960.2/433.8/260.8/200.1, 제거 −5.7(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"jbht:JBIMember": ["인터모달(JBI)", "#c8102e"], "jbht:DCSMember": ["전용 트럭(DCS)", "#e8707f"], "jbht:ICSMember": ["화물 중개(ICS)", "#1d1d1b"],
             "jbht:JBTMember": ["트럭 운송(JBT)", "#f5a3a3"], "jbht:FMSMember": ["최종 배송(FMS)", "#8a8a8a"]},
 "ignore": []
}
