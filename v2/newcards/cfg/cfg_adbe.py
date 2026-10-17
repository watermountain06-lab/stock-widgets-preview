# ADBE(어도비) v2 카드 설정 — 자동 카드(AUTO). 회계연도 11월 말 무렵 금요일(52/53주, Q3 FY26 = 2026-05-30~08-28). 카드 순위 119(시총 116위).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-09-22), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 모두 장 마감 뒤 접수), 8-K(CEO 전환 2026-03-09·후임 발표 09-02,
# CFO 사임 06-08, 자사주 $25B 프로그램 04-21), StockAnalysis.
# 엔진 입력(2026-10-17): 차입금 = DebtCurrent + LongTermDebt(비유동분만 — 1년 안 만기 $1,597M이 빠졌었다, DEBT_TOTAL_TAG).
# 4분기 EPS 보도자료 값(FY2025 $4.45·FY2024 $3.79·FY2023 $3.23). Q2 FY26에 영업권 손상(주당 $0.17, 비현금 — 판정 계산 규칙이라 손대지 않음).
# 2026-04-28 Semrush 인수 완료($1.87B, 대부분 현금). FY2026 1분기부터 보고 부문 1개(옛 Digital Media·Digital Experience·Publishing 통합) — 매출 구성은 지역별.
CIK = '0000796343'
# 씨앗값 — quarter_auto가 매번 다시 정한다
CUR, YO, QO = '2026-08-28', '2025-08-29', '2026-05-29'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-11-28', '2024-11-29'), 'FY2025'
VOTES, VERDICT = (1, 1, 1), '저평가'
CO = 'Adobe'
S_ = 'https://www.sec.gov/Archives/edgar/data/796343/'
SEC = S_
TENQ = S_ + '000079634326000156/adbe-20260828.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000079634326000147/adbeex991q326.htm', 'q2': S_ + '000079634326000109/adbeex991q226.htm',
      'q1': S_ + '000079634326000048/adbeex991q126.htm', 'q4': S_ + '000079634325000135/adbeex991q425.htm'}
LINKS = {'ceo': S_ + '000079634326000144/adbeex9918-k9826.htm', 'bb': S_ + '000079634326000101/ex9918-k42126.htm',
         'ceo1': S_ + '000079634326000048/adbe-20260309.htm', 'ceo8k': S_ + '000079634326000144/adbe-20260902.htm', 'cfo': S_ + '000079634326000109/adbe-20260608.htm'}
FAIRBAND_TITLE = 'id="adbeFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (20, 45)
ACT_REASON = ''
NONOP_WHAT = '장기투자'
PH = ['CRM', 'MSFT', 'ORCL', 'PANW', 'IBM', 'CSCO']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소프트웨어·IT 6곳 PER 비교 (점수는 IT 카드 유니버스 전체)', 'pbr': '소프트웨어·IT PBR 비교', 'psr': '소프트웨어·IT PSR 비교',
                'pcr': '소프트웨어·IT PCR(FCF) 비교', 'evebitda': '소프트웨어·IT EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(ADBE 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어·IT 서비스 회사가 섞여 있다. 차트에는 소프트웨어·IT 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 지역별 매출) — 미주 3,974 + EMEA 1,852 + 아시아·태평양 934 = 6,760(연결 매출).
SEG = [('미주', 3974, '#eb1000'), ('EMEA', 1852, '#b00c00'), ('아시아·태평양', 934, '#f56b5c')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역별(보고 부문은 1개)'
# 손 뉴스: Q3 FY26 실적(9/10)은 news_auto가 SEC 숫자로 붙인다(빌드 전에 news_auto.py ADBE — 1차 빌드엔 빠졌다) — 그보다 뒤 손 항목은 없다. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일: 실적 8-K는 모두 동부 16시 전후 접수(장 마감 뒤) → 다음 거래일. 자사주 8-K 4/21 16:07 → 4/22.
# CEO 후임 발표(9/3 보도자료, 8-K는 9/8 접수)는 보도 시각 미표기 — 9/3 종가 +2.1%, 9/4 시가부터 낮게 출발해 9/4로 두고 제목에 밝힌다(Codex·Fable). 9/8 8-K(16:38 접수)의 Wadhwani 사임은 CEO 항목에 — 따로 두면 반응일 9/9가 9/10 자동 실적 항목을 중복으로 지운다.
NEWS_RANGE = '2025.12 ~ 2026.09'
NEWS = [
    ('red', '2026년 9월 3일 — 새 CEO 발표(보도 시각 미표기 · 등락은 9/4)', '2026-09-04',
     'Anil Chakravarthy(고객 경험 사업 사장) 12월 1일부터 사장·CEO · Shantanu Narayen은 집행 이사회 의장으로 · 9/3 종가는 +2.1% · 같은 일을 담은 9/8 8-K에 크리에이티비티·생산성 사업 사장 David Wadhwani 9월 27일 사임', 'ceo8k', 'Adobe 공시 (SEC 8-K — 보도자료 첨부)'),
    ('red', '2026년 6월 11일 장 마감 뒤 — Q2 FY26 실적·CFO 사임', '2026-06-12',
     '매출 $6.62B(+12.7%, 4/28 인수 완료한 Semrush 포함 — $1.87B, 대부분 현금) · 희석 EPS $4.25(영업권 손상 주당 $0.17 포함) · CFO Dan Durn 6월 15일 사임, Steve Day 임시 CFO', 'q2', 'Adobe 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 21일 장 마감 뒤 — 자사주 매입 $25B 승인', '2026-04-22',
     '2030년 4월 30일까지 최대 $25B', 'bb', 'Adobe 공시 (SEC 8-K)'),
    ('red', '2026년 3월 12일 장 마감 뒤 — Q1 FY26 실적·CEO 전환 공시', '2026-03-13',
     '매출 $6.40B(+12.0%) · 희석 EPS $4.60 · Shantanu Narayen CEO 전환 결정(후임 선임까지 유지, 의장은 계속)', 'q1', 'Adobe 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 10일 장 마감 뒤 — Q4 FY25 실적', '2025-12-11',
     '매출 $6.19B(+10.5%) · 희석 EPS $4.45(1년 전 $3.79)', 'q4', 'Adobe 실적 보도자료 (SEC 8-K)'),
]
# fetch_analyst.py가 채운다(한 줄 dict, 줄 뒤 주석 금지)
ANALYST = {'rating': 'Hold', 'n': 39, 'nt': 26, 'mean': 259.56, 'median': 250, 'low': 187.5, 'high': 373, 'sb': 5, 'b': 4, 'h': 24, 's': 1, 'ss': 5}
ANALYST_ASOF = '2026-10-17'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(손 표와 일치). 원문 대조: 10-Q 지역별 매출 Q3 FY26 3,974/1,852/934, 1년 전 3,555/1,586/847 = 연결 매출(2026-10-17) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:Revenues"
 ],
 "axis": "srt:StatementGeographicalAxis",
 "extra": {},
 "members": {
  "srt:AmericasMember": [
   "미주",
   "#eb1000"
  ],
  "us-gaap:EMEAMember": [
   "EMEA",
   "#b00c00"
  ],
  "srt:AsiaMember": [
   "아시아·태평양",
   "#f56b5c"
  ]
 },
 "ignore": []
}
