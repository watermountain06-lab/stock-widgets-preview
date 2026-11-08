# ROL(롤린스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 해충 방제 서비스(Orkin, HomeTeam, Clark, Saela 등) — 주거·상업·흰개미.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-22), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/ROL.md.
# 엔진 입력(2026-10-25): 차입금 = 기업어음 $239.6M + LongTermDebt $487.6M(합산 대체 경로 — LongTermLineOfCredit은 같은 금액이라 더하지 않음), 현금 $129.1M. 인수 = 최근 4분기 $184M(작은 인수 여러 건).
# 일회성 작음(조정 EPS와 차이 약 5% — 주식보상·인수 비용).
CIK = '0000084839'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, -1, -2), '적정~고평가'
CO = 'Rollins'
S_ = 'https://www.sec.gov/Archives/edgar/data/84839/'
SEC = S_
TENQ = S_ + '000008483926000045/rol-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000008483926000042/rol-20261021xex991.htm', 'q2': S_ + '000008483926000038/rol-20260722xex991.htm',
      'q1': S_ + '000008483926000019/rol-20260422xex991.htm', 'q4': S_ + '000008483926000003/rol-20260211xex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="rolFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 25)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('경기와 덜 연동되는 반복 서비스라 오래 높은 배수를 받아 왔는데, 주가가 2026년 2월 고점에서 절반 가까이 내렸다(성장 둔화). '
              'EPS 이력은 2022년부터만 쓴다(요약 자료에 2015~2021 분기 EPS가 거의 없다). 작은 해충 방제 회사를 해마다 여러 곳 인수해 성장률에 인수 효과가 섞인다. 매출은 주거·상업·흰개미 서비스로 나뉜다(보고 부문은 하나).')
PH = ['CTAS', 'RSG', 'WM', 'ADP', 'PAYX', 'CPRT']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '반복 서비스 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(ROL 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비·서비스가 섞여 있다. 차트에는 반복 서비스 6곳만 보인다.')
# 매출(Q3 2026 10-Q 서비스별) — 주거 499.7 + 상업 360.7 + 흰개미·부대 217.9 + 기타 6.7 + 가맹 4.6 = 1,089.7.
SEG = [('주거', 499.7, '#e31b23'), ('상업', 360.7, '#003366'), ('흰개미·부대 서비스', 217.9, '#f28a8f'), ('기타', 6.7, '#c4c4c4'), ('가맹점', 4.6, '#8aa4c4')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 서비스별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:06~16:07 동부 접수) → 다음 거래일. 넣지 않은 8-K: 대주주 지분 매각과 회사 자사주 매입(2025-11), 작은 인수.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 21일 장 마감 뒤 — Q3 2026 실적', '2026-10-22',
     '매출 $1.09B(+6.2%) · 순이익 $158M · 희석 EPS $0.33(1년 전 $0.34) — 다음 날 주가 +6%', 'q3', 'Rollins 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 22일 장 마감 뒤 — Q2 2026 실적', '2026-07-23',
     '매출 $1.08B · 순이익 $144M · 희석 EPS $0.30(1년 전 $0.29) — 다음 날 주가 −9%', 'q2', 'Rollins 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 22일 장 마감 뒤 — Q1 2026 실적', '2026-04-23',
     '매출 $906M · 순이익 $108M · 희석 EPS $0.22(1년 전 $0.22)', 'q1', 'Rollins 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 11일 장 마감 뒤 — Q4 2025 실적', '2026-02-12',
     '매출 $913M · 순이익 $116M · 희석 EPS $0.24(1년 전 $0.22) · 2025년 EPS $1.09 — 다음 날 주가 −11%', 'q4', 'Rollins 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 19, 'nt': 12, 'mean': 37.17, 'median': 37, 'low': 26, 'high': 49, 'sb': 5, 'b': 3, 'h': 9, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 서비스 5개(수동 지도). 원문 대조: Q3 2026 499.7/360.7/217.9/6.7/4.6(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"rol:ResidentialRevenueMember": ["주거", "#e31b23"], "rol:CommercialRevenueMember": ["상업", "#003366"], "rol:TermiteAndAncillaryRevenuesMember": ["흰개미·부대 서비스", "#f28a8f"],
             "rol:OtherRevenueMember": ["기타", "#c4c4c4"], "us-gaap:FranchiseMember": ["가맹점", "#8aa4c4"]},
 "ignore": []
}
