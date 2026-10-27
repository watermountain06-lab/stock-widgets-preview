# STLD(스틸 다이내믹스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 미국 전기로 철강사 — 철강, 금속 재활용, 철강 구조물(조이스트·데크), 알루미늄 압연(2025년 가동).
# 출처: SEC XBRL(10/23 Q3 2026 10-Q까지 요약 자료에 있음), 실적 보도자료(Q3 2025~Q3 2026, 8-K 2.02항 — 장 마감 뒤 저녁 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/STLD.md.
# 엔진 입력(2026-10-27): 차입금 $4,204M(1년 안 $20.9M + 장기 $4,183M), 현금 $929M, 비지배지분 −$206M(자본 안, 알루미늄 합작 손실) — 상환가능 비지배지분 $143M(메자닌)은 엔진이 읽지 않는다(주당 약 $1).
# 일회성: Q2 2026 알루미늄 이전 손상 $16.5M(주당 약 0.09) — 최근 4분기 EPS 13.55의 1% 미만. 철강 경기 순환 — 최근 4분기는 가격 강세 구간.
CIK = '0001022671'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Steel Dynamics'
S_ = 'https://www.sec.gov/Archives/edgar/data/1022671/'
SEC = S_
TENQ = S_ + '000110465926118461/stld-20260930x10q.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000110465926117217/tm2627861d2_ex99-1.htm', 'q2': S_ + '000110465926085277/tm2620920d1_ex99-1.htm',
      'q1': S_ + '000110465926045938/tm2612296d1_ex99-1.htm', 'q4': S_ + '000110465926006889/tm264071d1_ex99-1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="stldFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('철강은 경기에 따라 이익이 크게 오르내린다 — 2022년 EPS $21.0에서 2025년 $7.99까지 내려왔다가 2026년 가격 강세로 다시 올랐다(최근 4분기 $13.55). '
              '5년 이력 배수와 마진 중앙값에 호황기(2021~2022)가 섞여 있다. 2025-12 New Process Steel 나머지 지분(55%)을 사들여 연결해 1년 전과의 매출 비교(+34.8%)에 인수 효과가 섞여 있다. 알루미늄 압연 공장이 2025년 가동을 시작해 초기 비용과 이전 손상이 이익을 눌렀다. '
              '상환가능 비지배지분 $143M은 엔진이 읽지 않아 기업가치에서 빠진다(주당 약 $1).')
PH = ['NUE', 'FCX', 'VMC', 'MLM', 'CF', 'LIN']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소재 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(STLD 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·건자재·포장재가 섞여 있다. 차트에는 철강·금속·건자재·화학 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문, 부문 간 매출 포함) — 철강 4,521.4 + 금속 재활용 1,255.7 + 알루미늄 493.5 + 철강 구조물 468.7 + 본사·기타 602.3 = 7,341.6, 부문 간 −832.2 → 6,509.4.
SEG = [('철강', 4521.4, '#003b71'), ('금속 재활용', 1255.7, '#5b8fc7'), ('알루미늄', 493.5, '#c8102e'), ('철강 구조물', 468.7, '#9aa5b1'), ('본사·기타', 602.3, '#d9d9d9')]
SEG_ADJ = -832.2
SEG_TITLE = '매출 구성 — 부문별(Q3 2026, 부문 간 매출 포함)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 저녁 발표 → 다음 거래일, Q4 2025만 당일 오전 발표(보도자료 1/26, 콘퍼런스콜 1/26 11:00 동부 — Fable r1) → 같은 날. 넣지 않은 8-K: 사채 발행·상환, BlueScope 인수 제안(미성사), 임원(CEO 교체 2027-01), 배당, 분기 전망 7.01.
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 19일 장 마감 뒤 — Q3 2026 실적', '2026-10-20',
     '매출 $6.51B(+34.8%) · 순이익 $756M · 희석 EPS $5.26(1년 전 $2.74)', 'q3', 'Steel Dynamics 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 20일 장 마감 뒤 — Q2 2026 실적', '2026-07-21',
     '매출 $6.09B · 순이익 $534M · 희석 EPS $3.69(1년 전 $2.01) — 알루미늄 이전 손상 $16.5M 포함', 'q2', 'Steel Dynamics 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 20일 장 마감 뒤 — Q1 2026 실적', '2026-04-21',
     '매출 $5.20B · 순이익 $403M · 희석 EPS $2.78(1년 전 $1.44) — 다음 날 주가 +5.2%', 'q1', 'Steel Dynamics 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 26일 장 전 — Q4 2025 실적', '2026-01-26',
     '매출 $4.4B · 순이익 $266M · 희석 EPS $1.82(1년 전 $1.36) · 2025년 EPS $7.99 — 당일 주가 −4.4%', 'q4', 'Steel Dynamics 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 14, 'nt': 10, 'mean': 274.6, 'median': 275, 'low': 260, 'high': 299, 'sb': 7, 'b': 2, 'h': 4, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-27'


# ── 자동 카드 — 부문 5개(부문 간 매출 포함, 본사·기타 포함), 부문 간 제거는 SEG_ADJ. 원문 대조: Q3 2026 4,521.4/1,255.7/493.5/468.7/602.3(2026-10-27) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidatedEntitiesAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"stld:SteelOperationsMember": ["철강", "#003b71"], "stld:MetalsRecyclingOperationsMember": ["금속 재활용", "#5b8fc7"],
             "stld:AluminumOperationsMember": ["알루미늄", "#c8102e"], "stld:SteelFabricationOperationsMember": ["철강 구조물", "#9aa5b1"],
             "us-gaap:CorporateAndOtherMember": ["본사·기타", "#d9d9d9"]},
 "ignore": []
}
