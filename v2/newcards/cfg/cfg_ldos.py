# LDOS(레이도스) v2 카드 설정 — 자동 카드(AUTO). 52/53주 회계연도(FY2025는 2026-01-02 종료). 미국 정부 IT·국방·정보·보건 서비스와 시스템(공항 보안 검색 장비 포함).
# 출처: SEC XBRL, Q2 FY26 10-Q(2026-08-04, 분기말 7/3), 실적 보도자료(Q3 FY25~Q2 FY26, 8-K 2.02항), StockAnalysis. 사전 조사 scratchpad pre/LDOS.md.
# 엔진 입력(2026-10-25): 차입금 = 1년 안 $22M + 장기 $6,009M(DEBT_TOTAL_TAG), 현금 $748M, 비지배지분 $52M. 인수 = 최근 4분기 $2.35B(Entrust 2026-03-27 현금 $2.4B).
# 거래: Entrust 인수는 최근 4분기에 약 14주만 들어 있다(혼합). 보안·검색 사업(SES)은 Altaris JV로 넘겨 2026-10-05부터 지분법 41.5% — 분기말(7/3) 뒤라 카드에는 아직 연결 매출로 들어 있다.
CIK = '0001336920'
CUR, YO, QO = '2026-07-03', '2025-07-04', '2026-04-03'
QLABEL, YL, QQL = 'Q2 FY26', 'Q2 FY25', 'Q1 FY26'
L8 = ['Q3 FY24', 'Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26']
FY_ENDS, FY_LABEL = ('2026-01-02', '2025-01-03'), 'FY2025'
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'Leidos'
S_ = 'https://www.sec.gov/Archives/edgar/data/1336920/'
SEC = S_
TENQ = S_ + '000133692026000246/ldos-20260703.htm'; TENQ_NAME = 'Q2 FY26 10-Q'
PR = {'q2': S_ + '000133692026000243/ldos070326q2pressreleaseex.htm', 'q1': S_ + '000133692026000167/ldos040326q1pressreleaseex.htm',
      'q4': S_ + '000133692026000028/ldos1022026ex991.htm', 'q3': S_ + '000133692025000057/ldos100325q3pressreleaseex.htm'}
LINKS = {'entrust': 'https://www.sec.gov/Archives/edgar/data/1336920/000119312526130304/d112441d8k.htm'}
FAIRBAND_TITLE = 'id="ldosFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 15)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('매출의 대부분이 미국 정부(국방부·정보기관·보훈부 등) 계약이라 정부 예산·셧다운에 영향을 받는다. '
              'Entrust 인수($2.4B 현금, 2026-03)는 최근 4분기에 약 14주만 들어 있고 인수 대금이 현금흐름 모델의 최근 투자에 잡힌다. 보안·검색 사업은 10월 5일 JV로 넘겨 Q4 FY26부터 연결 매출에서 빠진다(Q3 FY26까지는 연결). '
              '현금흐름 모델은 최근 4분기 인수 대금 $2.35B를 재투자로 넣는데 Entrust 매출은 약 14주만 들어 있어 투자 효율이 낮게 잡힌다 — 인수를 평소 수준($0.3B)으로 보면 기본 약 $109(비율 1.24), Entrust 매출을 1년치로 보면 약 $96(1.42)으로 현금흐름 칸이 −1이 된다(정의 선택, 공개만). '
              '보수 시나리오가 음수이고 요구 성장률이 음수로 나오는 것은 이 낮은 투자 효율에서 성장이 오히려 가치를 깎는다는 모델 결과다 — 실제로 역성장해야 한다는 뜻이 아니다.')
PH = ['GD', 'NOC', 'LHX', 'J', 'HII', 'TDG']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '정부 IT·방산 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(LDOS 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 정부 IT·방산 6곳만 보인다.')
# 매출(Q2 FY26 10-Q 부문) — 정보·디지털 1,499 + 보건 1,086 + 국토안보 1,018 + 국방 955 = 4,558.
SEG = [('정보·디지털', 1499, '#6e2c8f'), ('보건', 1086, '#a97ac7'), ('국토안보(보안 검색 포함)', 1018, '#3a3a3a'), ('국방', 955, '#c9b3db')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건 + Entrust 인수 완료(EPS는 GAAP 희석). 반응일: Q3 FY25·Q1·Q2 FY26은 장 마감 뒤 → 다음 거래일, Q4 FY25는 장 전 → 같은 날, 인수 완료 8-K 3/30 장 전 → 3/30. 넣지 않은 8-K: SES JV 계약(4/14)·완료(10/5 — 분기 뒤).
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 3일 장 마감 뒤 — Q2 FY26 실적', '2026-08-04',
     '매출 $4.56B(+7.2%) · 지배주주 순이익 $354M · 희석 EPS $2.81(1년 전 $3.01) — 다음 날 주가 +10%', 'q2', 'Leidos 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 4일 장 마감 뒤 — Q1 FY26 실적', '2026-05-05',
     '매출 $4.40B · 지배주주 순이익 $328M · 희석 EPS $2.56(1년 전 $2.77) — 인수 비용 포함, 다음 날 주가 −8%', 'q1', 'Leidos 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 30일 — Entrust 인수 완료', '2026-03-30',
     '현금 약 $2.4B로 Entrust(KENE Parent, Inc.) 인수 완료(8-K 2.01)', 'entrust', 'Leidos 공시 (SEC 8-K)'),
    ('red', '2026년 2월 17일 — Q4 FY25 실적', '2026-02-17',
     '지배주주 순이익 $327M · 희석 EPS $2.53(1년 전 $2.12) · FY2025 EPS $11.14 — 발표 당일 주가 −8%', 'q4', 'Leidos 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 3일 장 마감 뒤 — Q3 FY25 실적', '2025-11-04',
     '매출 $4.47B · 지배주주 순이익 $367M · 희석 EPS $2.82(1년 전 $2.68)', 'q3', 'Leidos 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 17, 'nt': 12, 'mean': 146, 'median': 142, 'low': 127, 'high': 170, 'sb': 4, 'b': 2, 'h': 11, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 4개(수동 지도, 영업 부문 차원, Revenues). 원문 대조: Q2 FY26 1,499/1,086/1,018/955(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"ldos:IntelligenceAndDigitalSegmentMember": ["정보·디지털", "#6e2c8f"], "ldos:HealthSegmentMember": ["보건", "#a97ac7"],
             "ldos:HomelandSegmentMember": ["국토안보(보안 검색 포함)", "#3a3a3a"], "ldos:DefenseSegmentMember": ["국방", "#c9b3db"]},
 "ignore": []
}
