# DGX(퀘스트 다이어그노스틱스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 미국 최대 임상 검사 서비스 — 혈액·진단 검사(진단 정보 서비스 부문이 매출의 98%).
# 출처: SEC XBRL(10/23 Q3 2026 10-Q까지 요약 자료에 있음), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/DGX.md.
# 엔진 입력(2026-10-27): 차입금 $5,550M(1년 안 $10M 포함), 현금 $797M, 비지배지분 = 자본 안 $318M + 상환가능 $81M(EV_TAGS_BY_CIK — 2026 Corewell Health 검사 합작으로 늘었다).
# 일회성: 구조조정·우발대가 평가 등 최근 4분기 주당 순 ±3% 안(회사 조정 EPS는 무형자산 상각을 빼서 높다 — 쓰지 않는다). 10/22 사이버 보안 사고(환자 기록 일부 접근) 비용은 아직 반영 안 됨.
CIK = '0001022079'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Quest Diagnostics'
S_ = 'https://www.sec.gov/Archives/edgar/data/1022079/'
SEC = S_
TENQ = S_ + '000102207926000108/dgx-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000102207926000097/dgx093020268-kex991.htm', 'q2': S_ + '000102207926000067/dgx063020268-kex991.htm',
      'q1': S_ + '000102207926000040/dgx033120268-kex991.htm', 'q4': S_ + '000102207926000005/dgx123120258-kexhibit991.htm'}
LINKS = {'cyber': S_ + '000094787126000941/ss6979200_8k.htm'}
FAIRBAND_TITLE = 'id="dgxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('2021~2022년은 코로나 검사 수요로 매출·이익이 크게 늘었던 구간이다 — 5년 매출 성장률은 그 고점에서 재서 낮게, 3년 성장률은 2023년 저점에서 재서 높게 나온다. '
              '2026년 Corewell Health와 검사 합작을 세워 비지배지분이 커졌다. 10월 22일 공시한 사이버 보안 사고(환자 기록 일부 접근, 조사 중)의 비용은 아직 이익에 반영되지 않았다.')
PH = ['UNH', 'CVS', 'MCK', 'COR', 'TMO', 'DHR']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '헬스케어 서비스·진단 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(DGX 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·유통·서비스가 섞여 있다. 차트에는 헬스케어 서비스·진단 장비 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 진단 정보 서비스 3,035 + 기타 62 = 3,097.
SEG = [('진단 정보 서비스', 3035, '#00857c'), ('기타', 62, '#6cc0b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: 실적 4건 + 사이버 사고(EPS는 GAAP 희석). 반응일: 장 전 발표(06:46~06:53 동부) → 같은 날. 넣지 않은 8-K: 임원, 주총, 사채 발행, 투자자 발표 자료(1/12).
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 22일 장 전 — Q3 2026 실적', '2026-10-22',
     '매출 $3.10B(+10.0%) · 순이익 $312M · 희석 EPS $2.78(1년 전 $2.16)', 'q3', 'Quest Diagnostics 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 10월 22일 장 전 — 사이버 보안 사고 공시', '2026-10-22',
     '검사 관리 시스템(Quanum LSM) 무단 접근, 환자 기록 일부 접근 추정 — 범위 조사 중, 회사는 운영·환자 서비스에 중대한 차질은 없었다고 밝힘(같은 날 Q3 실적과 겹쳐 주가 반응은 하나)', 'cyber', 'Quest Diagnostics 8-K (SEC)'),
    ('green', '2026년 7월 23일 장 전 — Q2 2026 실적', '2026-07-23',
     '매출 $3.04B · 순이익 $320M · 희석 EPS $2.84(1년 전 $2.47) — 당일 주가 +8.6%', 'q2', 'Quest Diagnostics 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 21일 장 전 — Q1 2026 실적', '2026-04-21',
     '매출 $2.90B · 순이익 $252M · 희석 EPS $2.24(1년 전 $1.94) — 당일 주가 +4.4%', 'q1', 'Quest Diagnostics 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 10일 장 전 — Q4 2025 실적', '2026-02-10',
     '매출 $2.81B · 순이익 $245M · 희석 EPS $2.18(1년 전 $1.95) · 2025년 EPS $8.75 — 당일 주가 +7.4%', 'q4', 'Quest Diagnostics 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 17, 'nt': 10, 'mean': 257.2, 'median': 260, 'low': 245, 'high': 265, 'sb': 7, 'b': 2, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-27'


# ── 자동 카드 — 부문 2개. 원문 대조: Q3 2026 3,035/62(2026-10-27) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"dgx:DiagnosticInformationServicesBusinessMember": ["진단 정보 서비스", "#00857c"], "us-gaap:AllOtherSegmentsMember": ["기타", "#6cc0b8"]},
 "ignore": []
}
