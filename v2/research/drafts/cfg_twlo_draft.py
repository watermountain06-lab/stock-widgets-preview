# TWLO(트윌리오) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 클라우드 커뮤니케이션 플랫폼(문자·음성·이메일·고객 데이터 API).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-07), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/TWLO.md.
# 보류였던 카드(일회성 — 안건 E54 보류). 사용자 결정 2026-10-24: 만들어 보고 판정이 흔들리면 다시 보류.
# 엔진 입력(2026-10-24): Q2 2026 이연법인세 평가충당금 환입 $944.1M(주당 $5.91)은 tax_oneoff로 PER·세율에서 뺀다. D&A = 감가상각 + 무형자산 상각(DDA_PARTS_BY_CIK — 합산 태그는 누계뿐).
# Q4 2025 지분법 투자 손상 $80.6M(주당 약 $0.53, 영업이익 밖)은 빼는 장치가 없어 최근 4분기 EPS에 남는다 — MODEL_NOTE.
CIK = '0001447669'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Twilio'
S_ = 'https://www.sec.gov/Archives/edgar/data/1447669/'
SEC = S_
TENQ = S_ + '000144766926000092/twlo-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000144766926000088/twloq226ex991.htm', 'q1': S_ + '000144766926000046/twloq126ex991.htm',
      'q4': S_ + '000144766926000010/twloq425ex991.htm', 'q3': S_ + '000144766925000147/twloq325ex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="twloFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-10, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('2024년 3분기까지 GAAP 적자였다 — 자기 이력의 PER 비교는 흑자로 돌아선 뒤 짧은 기간뿐이다. '
              'Q2 2026의 큰 GAAP 이익은 대부분 이연법인세 평가충당금 환입(비현금)이라 PER과 세율 계산에서 뺐다. '
              'Q4 2025 지분법 투자 손상(영업이익 밖)은 빼는 장치가 없어 최근 4분기 EPS가 그만큼 낮고 PER이 높게 나온다. '
              '주식보상비용이 커서 GAAP 이익이 회사가 앞세우는 비GAAP 이익보다 크게 낮다.')
PH = ['CRM', 'ORCL', 'CRWD', 'PANW', 'MSFT', 'PLTR']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소프트웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': '소프트웨어 PBR 비교', 'psr': '소프트웨어 PSR 비교',
                'pcr': '소프트웨어 PCR(FCF) 비교', 'evebitda': '소프트웨어 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(TWLO 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 소프트웨어 6곳만 보인다.')
# 매출(Q2 2026 10-Q, 단일 부문 — 지역별) — 미국 961.4 + 해외 537.7 = 1,499.1.
SEG = [('미국', 961.4, '#f22f46'), ('해외', 537.7, '#f7838f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역별(Q2 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 비GAAP·가이던스는 쓰지 않는다). 반응일: 장 마감 뒤 발표 → 다음 거래일. 넣지 않은 8-K: 이사 선임(3/24), 주총(6/17).
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 6일 — Q2 2026 실적', '2026-08-07',
     '매출 $1.50B(1년 전 $1.23B) · 희석 EPS $6.68 — 이연법인세 평가충당금 환입 $944M(주당 $5.91) 포함 · 선급 네트워크 서비스 손상 $32.8M(영업비용 안) — 발표 다음 날 주가 +25%', 'q2', 'Twilio 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 30일 — Q1 2026 실적', '2026-05-01',
     '매출 $1.41B · 희석 EPS $0.57(1년 전 $0.12) — 발표 다음 날 주가 +24%', 'q1', 'Twilio 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 12일 — Q4 2025 실적', '2026-02-13',
     '매출 $1.37B · 희석 EPS −$0.30(1년 전 −$0.08) — 지분법 투자 손상 $80.6M 포함 · 2025년 희석 EPS $0.21', 'q4', 'Twilio 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 30일 — Q3 2025 실적', '2025-10-31',
     '매출 $1.30B · 희석 EPS $0.23(1년 전 −$0.06) — 발표 다음 날 주가 +20%', 'q3', 'Twilio 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 31, 'nt': 25, 'mean': 270.52, 'median': 270, 'low': 165, 'high': 335, 'sb': 19, 'b': 6, 'h': 4, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-24'


# ── 자동 카드 — 지역 2개(수동 지도). 원문 대조: Q2 2026 961.4/537.7(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:StatementGeographicalAxis",
 "extra": {},
 "members": {"country:US": ["미국", "#f22f46"], "us-gaap:NonUsMember": ["해외", "#f7838f"]},
 "ignore": []
}
