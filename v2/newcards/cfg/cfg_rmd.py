# RMD(레즈메드) v2 카드 설정 — 자동 카드(AUTO). 회계연도 6월 30일. 카드 순위 198. 수면무호흡 치료 기기(CPAP)·마스크, 재택·요양 소프트웨어.
# 출처: SEC XBRL, FY2026 10-K(2026-08-14T01:17Z), 실적 보도자료(Q1~Q4 FY26, 8-K 2.02항 — 장 마감 뒤 발표, 4:30 ET), 8-K(MatrixCare 매각 계약 7/7, 감사인 교체 8/17, 자사주 ASR 9/1), StockAnalysis. 사전 조사 자료표 scratchpad pre/RMD.md.
# 엔진 입력(2026-10-24): 차입금 = DebtLongtermAndShorttermCombinedAmount $659.4M(DEBT_TOTAL_TAG — 기본 선택은 단기 $260M만), 4분기 EPS FY2022·2023·2024 보도자료 값. Q1 FY27 실적은 10월 말 예정.
CIK = '0000943819'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
FY_ENDS, FY_LABEL = ('2026-06-30', '2025-06-30'), 'FY2026'
VOTES, VERDICT = (1, 0, -1), '적정'
CO = 'ResMed'
S_ = 'https://www.sec.gov/Archives/edgar/data/943819/'
SEC = S_
TENQ = S_ + '000094381926000047/rmd-20260630.htm'; TENQ_NAME = 'FY2026 10-K'
PR = {'q4': S_ + '000119312526337962/d158732dex991.htm', 'q3': S_ + '000119312526197192/d146862dex991.htm', 'q2': S_ + '000119312526029326/d80310dex991.htm', 'q1': S_ + '000119312525258519/d92301dex991.htm'}
LINKS = {'mc': S_ + '000119312526297658/d88958d8k.htm'}
FAIRBAND_TITLE = 'id="rmdFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (20, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('요양 시설용 소프트웨어 MatrixCare를 매각하기로 해(계속사업으로 남아 과거 실적은 재작성되지 않음) 종결 뒤 소프트웨어 부문 매출이 줄고 매각 대금 현금이 들어온다. '
              '현금흐름 모델은 최근 1년 인수(Noctrix)와 MatrixCare를 매각 예정 자산(유동자산)으로 옮긴 회계 재분류까지 재투자로 세어 성장에 드는 재투자를 무겁게 잡는다 — 실제 설비투자는 감가상각보다 작다(안건 E46). '
              'Q4 FY26 영업이익에는 인공호흡기 Astral 현장 안전 조치 비용이 들어 있다. 차입금보다 현금이 많다. 감사인이 FY2027부터 KPMG에서 PwC로 바뀐다(이견 없음). '
              '자기 이력 점수는 5년 동안 높은 배수를 받아 온 이 종목 안에서 지금 배수가 낮은 편이라는 뜻이고, 현금흐름 모델은 그 높은 배수 자체를 인정하지 않는다 — 5년 뒤에는 낮은 장기 성장률과 적용 할인율로 잔존가치를 잡아 지금 시장 배수보다 낮은 배수가 된다.')
PH = ['ISRG', 'SYK', 'BSX', 'ABT', 'IDXX', 'DHR']
HEALTH_EXTRA = '당좌·유동비율에는 매각 예정 자산(MatrixCare)이 들어 있다. 이자비용보다 이자수익이 커 이자보상배율은 계산하지 않는다.'   # 고정 문장(Fable r1 2026-10-24)
# 이자보상배율 사유 보정(Codex r2) — 순이자수익이라 계산하지 않는다(연간 기준)
POST = [r'''
h = h.replace('<span class="diag-value">그 분기 이자비용 미공시</span>', '<span class="diag-value">순이자수익이라 미산출(FY2026 연간)</span>', 1)
h = h.replace('"note": "그 분기 이자비용 미공시"', '"note": "순이자수익이라 미산출(FY2026 연간)"', 1)
''']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {'pbr': 60}, {}, {}
CHART_TITLES = {'per': '의료기기 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(RMD 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·도구가 섞여 있다. 차트에는 의료기기 6곳만 보인다.')
# 매출(FY2026 10-K 부문, Q4 FY26) — 수면·호흡 1,292 + 요양 소프트웨어 172 = 1,464. 1년 전 1,181·167.
SEG = [('수면·호흡 건강', 1292.0, '#004b87'), ('요양·재택 소프트웨어', 172.0, '#6cace4')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다) + MatrixCare 매각 계약. 반응일: 8-K 장 마감 뒤 접수 → 다음 거래일.
# 넣지 않은 8-K: 감사인 교체(8/17, 이견 없음 — MODEL_NOTE), 자사주 ASR $450M(9/1), CFO 은퇴(4/30), 이사회.
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('red', '2026년 8월 6일 — Q4 FY26 실적', '2026-08-07',
     '매출 $1.46B(1년 전 $1.35B) · 순이익 $383M · 희석 EPS $2.64(1년 전 $2.58) — Astral 현장 안전 조치 비용 $41.9M 포함', 'q4', 'ResMed 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 7일 — MatrixCare 매각 계약', '2026-07-08',
     'Frazier Healthcare Partners에 현금 $490M — 연매출 약 $220M, 계속사업으로 남는다', 'mc', 'ResMed 공시 (SEC 8-K)'),
    ('red', '2026년 4월 30일 — Q3 FY26 실적', '2026-05-01',
     '매출 $1.43B · 순이익 $399M · 희석 EPS $2.74(1년 전 $2.48)', 'q3', 'ResMed 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 29일 — Q2 FY26 실적', '2026-01-30',
     '매출 $1.42B · 순이익 $393M · 희석 EPS $2.68(1년 전 $2.34)', 'q2', 'ResMed 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 30일 — Q1 FY26 실적', '2025-10-31',
     '매출 $1.34B · 순이익 $349M · 희석 EPS $2.37(1년 전 $2.11)', 'q1', 'ResMed 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 12, 'mean': 258.67, 'median': 260, 'low': 225, 'high': 320, 'sb': 7, 'b': 2, 'h': 10, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-31'


# ── 자동 카드 — 부문 2개(수동 지도). 원문 대조: Q4 FY26 1,292/172(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"rmd:SleepAndBreathingHealthMember": ["수면·호흡 건강", "#004b87"], "rmd:ResidentialCareSoftwareMember": ["요양·재택 소프트웨어", "#6cace4"]},
 "ignore": []
}
