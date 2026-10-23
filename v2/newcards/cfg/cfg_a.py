# A(애질런트) v2 카드 설정 — 자동 카드(AUTO). 회계연도 10월 31일. 카드 순위 183. 생명과학·진단 분석 장비 — 생명과학·진단(LDG), CrossLab(소모품·서비스), 응용 시장(AMG).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-09-01 장 마감 뒤 접수, 분기 끝 7/31), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 모두 장 마감 뒤), StockAnalysis.
# 엔진 입력(2026-10-23): 차입금 = 단기 304 + 장기 3,645 = $3,949M(DEBT_TOTAL_TAG), 4분기 EPS FY2022·2023·2024는 보도자료 값(Q4_EPS_OVERRIDE).
# Biocare $950M 인수(2026-06-24, 병리 진단 — Q3 FY26 안). 6월 사채 $600M 발행.
CIK = '0001090872'
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-10-31', '2024-10-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Agilent'
S_ = 'https://www.sec.gov/Archives/edgar/data/1090872/'
SEC = S_
TENQ = S_ + '000109087226000064/a-20260731.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000109087226000062/exhibit991-q326pressrelease.htm', 'q2': S_ + '000109087226000052/exhibit991-q226pressrelease.htm',
      'q1': S_ + '000109087226000015/exhibit991-q126pressrelease.htm', 'q4': S_ + '000109087225000070/exhibit991-q425pressrelease.htm'}
LINKS = {'tenq': S_ + '000109087226000064/a-20260731.htm'}
FAIRBAND_TITLE = 'id="aFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '장기 투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('6월에 병리 진단 회사 Biocare를 인수(사채 $600M 등으로 조달)해 최근 분기부터 매출에 더해졌다 — 회사의 핵심 성장(환율·인수 효과 제외)은 보고 성장보다 낮다. Q3 이익에는 관세 환급 일회성이 들어 있다(회사 조정 실적 기준 순이익 약 $17M, EPS 약 $0.06, 영업이익률 약 1%p). '
              '인수 무형자산 상각 때문에 GAAP 이익이 회사가 발표하는 조정 이익보다 작다. 현금흐름 내재가치가 현재가보다 크게 낮은 것은 인수 때문만이 아니다 — 인수 전인 6월에도 기본값은 현재가의 3분의 1 남짓이었다. 할인율 10%·영구성장 2.5%에 비해 FCF 수익률이 낮은(PCR이 높은) 탓이 크고, 인수 대금을 재투자로 센 효과는 작다.')
PH = ['TMO', 'DHR', 'WAT', 'MTD', 'RVTY', 'IQV']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP = {'pbr': 60}, {}
CHART_NOTE = {'pbr': ' (MTD는 자사주 매입으로 자본이 거의 0이라 PBR이 수천 배 — 차트에서 뺐다)'}
CHART_TITLES = {'per': '생명과학 도구 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(A 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·도구가 섞여 있다. 차트에는 생명과학 도구 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 부문) — CrossLab 786 + 생명과학·진단 746 + 응용 시장 346 = 1,878(= 총매출). 1년 전 744·670·324.
SEG = [('CrossLab(소모품·서비스)', 786.0, '#0085d5'), ('생명과학·진단', 746.0, '#5aaee5'), ('응용 시장', 346.0, '#00578c')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다), 인수.
# 반응일: 실적 8-K 2025-11-24T21:11Z·2026-02-25T21:06Z·05-27T20:06Z·08-26T20:06Z = 장 마감 뒤 → 다음 세션. Biocare 인수는 8-K 없음(10-Q 주석) — 실적 줄에.
# 넣지 않은 8-K: 임원·이사(CFO 10/27·법무 3/31·5/4·회계 3/5·의장 은퇴 9/2), 주총(3/18), 사채(6/25).
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 26일 — Q3 FY26 실적', '2026-08-27',
     '매출 $1.88B(+8.1%, 핵심 +7.3%) · GAAP 순이익 $362M · 희석 EPS $1.28(1년 전 $1.18) · 관세 환급 일회성 포함(회사 조정 실적 기준 EPS 약 $0.06) · 10-Q: 6/24 Biocare 인수 완료($950M, 병리 진단 — 6/25 사채 $600M 발행)', 'q3', 'Agilent 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 27일 — Q2 FY26 실적', '2026-05-28',
     '매출 $1.83B(+10.0%, 핵심 +6.3%) · GAAP 순이익 $339M · 희석 EPS $1.20(1년 전 $0.75)', 'q2', 'Agilent 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 25일 — Q1 FY26 실적', '2026-02-26',
     '매출 $1.80B(+7.0%, 핵심 +4.4%) · GAAP 순이익 $305M · 희석 EPS $1.07(1년 전 $1.11)', 'q1', 'Agilent 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 24일 — Q4 FY25 실적', '2025-11-25',
     '매출 $1.86B(+9.4%, 핵심 +7.2%) · GAAP 순이익 $434M · 희석 EPS $1.53(1년 전 $1.22)', 'q4', 'Agilent 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 22, 'nt': 18, 'mean': 176.67, 'median': 181, 'low': 135, 'high': 196, 'sb': 11, 'b': 4, 'h': 7, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 부문 3개(수동 지도). 원문 대조: Q3 FY26 786/746/346(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"a:AgilentCrossLabMember": ["CrossLab(소모품·서비스)", "#0085d5"], "a:LifeSciencesAndDiagnosticsMarketsMember": ["생명과학·진단", "#5aaee5"], "a:AppliedMarketsMember": ["응용 시장", "#00578c"]},
 "ignore": []
}
