# IDXX(아이덱스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 191. 반려동물 진단(동물병원 검사기·시약·외부 검사실·소프트웨어), 수질 검사, 축산 진단.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-04T20:16Z), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표, 8:30 콜, 8-K 오전 6시대 접수), StockAnalysis. 사전 조사 자료표 scratchpad pre/IDXX.md.
# Q3 2026 실적은 아직(작년 11/3 발표) — 다음 분기 10-Q가 나오면 다시 만든다.
# 엔진 입력(2026-10-24): 차입금 = 신용한도 차입 519(텀론 $250M 포함) + 1년 안 사채 150 + 장기 사채 299.9 = $968.9M(DEBT_TOTAL_TAG — 기본 목록에 신용한도가 빠졌다), 4분기 EPS 2021·2023·2025 보도자료 값.
CIK = '0000874716'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'IDEXX'
S_ = 'https://www.sec.gov/Archives/edgar/data/874716/'
SEC = S_
TENQ = S_ + '000087471626000123/idxx-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000110465926090033/tm2622041d1_ex99-1.htm', 'q1': S_ + '000110465926055203/tm2613510d1_ex99-1.htm',
      'q4': S_ + '000110465926008904/tm264623d1_ex99-1.htm', 'q3': S_ + '000110465925105185/tm2530045d1_ex99-1.htm'}
LINKS = {'ceo': S_ + '000110465926003103/tm262817d1_8k.htm', 'covet': 'https://ir.idexx.com/news-events/press-releases/detail/417/idexx-laboratories-acquires-covetai-to-advance-veterinary-workflow-intelligence'}
# 다음 실적: 2026-10-01 회사 공지 — 11/2 장 전 발표, 오전 8:30(동부) 콜(Codex r1 필수)
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-11-02', 'src': '10/1 회사 공지 — 장 시작 전 발표, 콜 오전 8:30(동부)'}
FAIRBAND_TITLE = 'id="idxxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (20, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('검사기를 깔고 시약·검사 서비스로 반복 매출을 내는 구조라 이익률이 높고 자본이 적게 든다. 자사주를 꾸준히 사들여 자본이 작아 PBR이 매우 높게 나온다. '
              '최근 GAAP EPS에는 주식보상 관련 세금 혜택이 조금씩 더해져 있다 — 회사가 발표하는 비교 가능 EPS는 이것과 환율 효과 등을 뺀다. '
              '지난 1년 주가가 고점에서 크게 내린 구간에 대해, 회사 공시에서는 실적 발표 외에 하락을 직접 설명할 결정적 악재를 확인하지 못했다. '
              '자기 이력 점수는 5년 내내 높은 PER을 받아 온 이 종목 안에서 지금 배수가 낮은 편이라는 뜻이고, 현금흐름 모델은 그 높은 배수 자체를 인정하지 않는다 — 5년 뒤에는 낮은 장기 성장률과 적용 할인율로 잔존가치를 잡아 지금 시장이 매기는 배수보다 훨씬 낮은 배수가 된다. 그래서 두 판정은 같은 질문이 아니다. '
              '2026년 5월 최고경영자가 내부 승진자로 바뀌었다.')
PH = ['ZTS', 'TMO', 'DHR', 'A', 'MTD', 'ISRG']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {'pbr': 60}, {}, {}
CHART_TITLES = {'per': '동물 건강·진단 도구 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(IDXX 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·도구가 섞여 있다. 차트에는 동물 건강·진단 도구 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 반려동물 1,118.2 + 수질 58.6 + 축산 35.2 = 1,212.0, 기타 4.6 → 1,216.6. 1년 전 1,022.4·51.0·31.8·4.3.
SEG = [('반려동물(CAG)', 1118.2, '#e2231a'), ('수질', 58.6, '#f07c74'), ('축산·가금·낙농', 35.2, '#9c150f')]
SEG_ADJ = 4.6
SEG_ADJ_LABEL = '기타'
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 비교 가능 EPS·가이던스는 쓰지 않는다) + CEO 교체 발표. 반응일: 8-K 장 전 접수(오전 6시대·CEO 8-K 8:33 ET) → 같은 날.
# 넣지 않은 8-K: 신용약정 연장(2025-11-13, 순차입 증가 없음), 이사·임원 변경, 주총.
NEWS_RANGE = '2025.11 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 16일 — 동물병원 업무 AI 회사 CoVetAI 인수', '2026-09-16',
     '금액 비공개(별도 8-K 없음)', 'covet', 'IDEXX 보도자료'),
    ('green', '2026년 8월 4일 — Q2 2026 실적', '2026-08-04',
     '매출 $1.22B(1년 전 $1.11B) · 순이익 $338M · 희석 EPS $4.27(1년 전 $3.63) — 검사기 판매는 전년 신제품(inVue) 출시 기저로 −19%, 반복 매출 +11%', 'q2', 'IDEXX 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 5일 — Q1 2026 실적', '2026-05-05',
     '매출 $1.14B · 순이익 $278M · 희석 EPS $3.47(1년 전 $2.96)', 'q1', 'IDEXX 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 2일 — Q4 2025 실적', '2026-02-02',
     '매출 $1.09B · 순이익 $248M · 희석 EPS $3.08(1년 전 $2.62) · 2025년 희석 EPS $13.08', 'q4', 'IDEXX 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 13일 — 최고경영자 교체 발표', '2026-01-13',
     'Jay Mazelsky가 5월 12일 최고경영자에서 이사회 의장(Executive Chair)으로 옮기고 2027년 주총 뒤 퇴임 — 후임은 내부 승진 Michael Erickson', 'ceo', 'IDEXX 공시 (SEC 8-K)'),
    ('green', '2025년 11월 3일 — Q3 2025 실적', '2025-11-03',
     '매출 $1.11B · 순이익 $275M · 희석 EPS $3.40(1년 전 $2.80) — 발표 날 주가 +15%', 'q3', 'IDEXX 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 14, 'nt': 9, 'mean': 723.89, 'median': 710, 'low': 665, 'high': 810, 'sb': 5, 'b': 4, 'h': 4, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 3개(수동 지도), 기타는 SEG_ADJ. 원문 대조: Q2 2026 1,118.2/58.6/35.2/기타 4.6(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"idxx:CompanionAnimalGroupSegmentMember": ["반려동물(CAG)", "#e2231a"], "idxx:WaterSegmentMember": ["수질", "#f07c74"],
             "idxx:LivestockAndPoultryDiagnosticsSegmentMember": ["축산·가금·낙농", "#9c150f"]},
 "ignore": []
}
