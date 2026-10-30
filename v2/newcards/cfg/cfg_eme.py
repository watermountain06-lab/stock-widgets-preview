# EME(엠코 그룹) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 미국 전기·기계 설비 공사(데이터센터·제조·의료 시설), 건물 서비스, 산업 서비스.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/EME.md.
# 엔진 입력(2026-10-25): 차입금 없음(리볼버 미사용), 현금 $924M, 운용리스 $0.5B. 2025년 Miller Electric 인수.
# 일회성: Q4 2025 영국 사업 매각 이익 세전 $144.9M(영업이익 안, 세후 주당 약 $2.67 — 최근 4분기 GAAP EPS의 약 8%). 빼고 재계산해도 표 (0, 0, −1) 유지(Codex·Fable r1, 2026-10-25).
CIK = '0000105634'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -1), '적정'
CO = 'EMCOR'
S_ = 'https://www.sec.gov/Archives/edgar/data/105634/'
SEC = S_
TENQ = S_ + '000010563426000110/eme-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000010563426000112/eme-ex991_2026630xq2.htm', 'q1': S_ + '000010563426000048/eme-ex991_2026331xq1.htm',
      'q4': S_ + '000010563426000027/eme-ex991_20251231xq4.htm', 'q3': S_ + '000010563425000082/eme-ex991_2025930xq3.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="emeFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 15)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 GAAP 이익에는 Q4 2025 영국 사업 매각 이익(세전 $145M, 영업이익 안 일회성)이 들어 있다 — PER·EV/EBITDA가 그만큼 낮고 현금흐름 모델의 이익률도 높게 잡힌다(빼면 영업이익률 약 9.6%). 빼고 다시 계산해도 세 표는 같다. '
              '데이터센터·제조 시설 공사 수요로 매출과 이익률이 빠르게 늘었다 — 과거 5년 이익률 중앙값은 지금보다 낮다. 영국 부문은 팔아서 매출이 0이다.')
PH = ['PWR', 'FIX', 'ETN', 'GE', 'TT', 'J']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '설비 공사·전기 설비 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(EME 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비가 섞여 있다. 차트에는 설비 공사·전기 설비 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 외부 매출) — 기계 2,300.9 + 전기 1,662.5 + 건물 서비스 837.7 + 산업 서비스 353.8 = 5,154.9(영국 0 — 매각).
SEG = [('기계 설비 공사', 2300.9, '#d9541e'), ('전기 설비 공사', 1662.5, '#ed9c78'), ('건물 서비스', 837.7, '#a8431a'), ('산업 서비스', 353.8, '#f4c7b3')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표 → 같은 날(Q4 2025는 장중 접수 → 같은 날). 넣지 않은 8-K: 이사·주총, 광산 안전 명령(MOR PPM, 7/31).
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('green', '2026년 7월 30일 — Q2 2026 실적', '2026-07-30',
     '매출 $5.15B(+19.8%) · 순이익 $404M · 희석 EPS $9.06(1년 전 $6.72) — 발표 당일 주가 +19%', 'q2', 'EMCOR 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 29일 — Q1 2026 실적', '2026-04-29',
     '매출 $4.63B · 순이익 $306M · 희석 EPS $6.84(1년 전 $5.26)', 'q1', 'EMCOR 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 26일 — Q4 2025 실적', '2026-02-26',
     '매출 $4.51B · 순이익 $435M · 희석 EPS $9.68(1년 전 $6.32) — 영국 사업 매각 이익 세전 $144.9M 포함(회사 조정 EPS $7.19)', 'q4', 'EMCOR 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 30일 — Q3 2025 실적', '2025-10-30',
     '매출 $4.30B · 순이익 $295M · 희석 EPS $6.57(1년 전 $5.80) — 발표 당일 주가 −17%', 'q3', 'EMCOR 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 11, 'nt': 7, 'mean': 1020.43, 'median': 1047, 'low': 795, 'high': 1200, 'sb': 7, 'b': 0, 'h': 4, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 4개(수동 지도, 외부 매출). 원문 대조: Q2 2026 2,300.9/1,662.5/837.7/353.8(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:StatementGeographicalAxis": "country:US"},
 "members": {"eme:UnitedStatesMechanicalConstructionAndFacilitiesServicesMember": ["기계 설비 공사", "#d9541e"], "eme:UnitedStatesElectricalConstructionAndFacilitiesServicesMember": ["전기 설비 공사", "#ed9c78"],
             "eme:UnitedStatesBuildingServicesMember": ["건물 서비스", "#a8431a"], "eme:UnitedStatesIndustrialServicesMember": ["산업 서비스", "#f4c7b3"]},
 "ignore": ["eme:UnitedKingdomBuildingServicesMemberMember"]
}
