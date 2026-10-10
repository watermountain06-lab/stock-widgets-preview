# NEM(뉴몬트) v2 카드 설정 — fill.py NEM. 회계연도 12월 31일. 시총 97위(S&P500 현재 시총 순, 2026-10-02 StockAnalysis 기준, 루트 카드 없음).
BUILD = {'overlay': True,
         'company_tags': [('nem:InventoryOtherThanOreStockpilesOnLeachpadsNetOfReserves', 'InventoryNet'),
                          ('nem:InventoryOreStockpilesOnLeachPadsCurrentNet', 'InventoryOreStockpilesCurrentNem'),   # 이름만 빌린 자리 — overlay_feed SUM·활동성 INV_SUM_BY_CIK가 재고에 더한다
                          ('nem:LeaseAndOtherFinancingObligationsCurrent', 'FinanceLeaseLiabilityCurrent'),
                          ('nem:LeaseAndOtherFinancingObligationsNoncurrent', 'FinanceLeaseLiabilityNoncurrent')]}
CIK = '0001164727'
# 출처: SEC XBRL(+ 회사 고유 태그 보충: 재고·리스 및 기타 금융채무), Q2 2026 10-Q(2026-07-23), 실적 보도자료(Q3 2025~Q2 2026, SEC 접수 모두 오후 4시 5~6분 = 장 마감 후 → 다음 거래일 반응),
# 8-K(Barrick과 NGM 합의 8/13 접수·8/10 발표), StockAnalysis.
# 엔진 수정(2026-10-02): 영업이익 줄이 없어 세전이익 − 영업외손익(DERIVED_OPINC), 이자비용 표준 태그가 2013년에 멈춰 손입력(interest_extra.json),
# 운용리스·우선주 태그 멈춤(EV_TAGS_BY_CIK), 차입금에 리스·기타 금융채무 포함(DEBT_TOTAL_TAG), 활동성 매출원가 태그(build_activity_score COGS_TAG_BY_CIK).
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 6118, 'op': 3096, 'ni': 2202, 'ocf': 2924, 'cap': 719}   # 10-Q(영업이익 = 매출 6,118 − 총비용 3,022), 현금흐름은 상반기 − 1분기
VOTES, VERDICT = (0, 0, 1), '적정~저평가'
CO = 'Newmont'
S_ = 'https://www.sec.gov/Archives/edgar/data/1164727/'
SEC = S_
PR = {'q2': S_ + '000116472726000034/newmontq22026earningsrelea.htm', 'q1': S_ + '000116472726000017/newmontq12026earningsrelea.htm',
      'q4': S_ + '000116472726000009/newmontq42025earningsand20.htm', 'q3': S_ + '000116472725000044/newmontq32025earningsrelea.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000116472726000036/nem-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'ngm': 'https://www.sec.gov/Archives/edgar/data/1164727/000110465926095968/tm2623048d1_8k.htm', 'tenq': TENQ}
FAIRBAND_TITLE = 'id="nemFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(회사가 따로 밝힌 파푸아뉴기니·가나 미송금 이익 과세 $0.55B를 뺀 값, 10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
OPM_RANGE, Y2 = (0, 70), (0, 70)
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '광산 개발·설비 취득(현금흐름표)'
STAT3 = ('금 실현 가격 (Q2 2026)', '$4,414/oz', '1년 전 $3,320 · 1분기 $4,900')
NEXT = ('10월 하순 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('10월 하순', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('6월 말 현금은 $9.0B, 차입금은 $5.1B, 리스·기타 금융채무는 $0.5B라 회사 기준 순현금이 약 $3.4B다(카드 순현금 칸은 운용리스 $0.1B까지 빼 $3.3B). '
               '8월 Barrick과의 합의로 네바다 합작사(NGM) 관련 현금 $1.95B를 Barrick에 내기로 했다.')
ACT_REASON = ''
YOY_EXTRA = '매출 +15% · 영업이익 +1%(1년 전 분기의 자산 매각 이익 $699M을 빼면 약 +31%) · 금 실현 가격 +33% · '
SEG = [('금 도레', 4280, '#d4a017'), ('정광·기타(구리·은·아연·납 포함)', 1838, '#e8c766')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 판매 형태별'
SEG_NOTE = ('1년 전보다 금 도레 +30.0%, 정광·기타 −9.2% · 출처: <a href="{TENQ}" target="_blank" rel="noopener">Q2 2026 10-Q 주석 5 (SEC) →</a>')
CAPITAL = [('자사주 매입 (2026 상반기)', '$3.5B'),
           ('자사주 매입 승인 추가 (4월)', '$6.0B'),
           ('분기 배당 (2026)', '$0.26', '+4%')]
CHECK_WHEN = '2026년 10월 하순 (예상) · Q3 2026'
CHECK = ['금 실현 가격(2분기 $4,414, 1분기 $4,900)',
         'Cadia 정상화 뒤 첫 온전한 분기(2분기 Cadia 금 생산 3.4만 온스, 1분기 9.4만 온스)',
         'NGM 출자 완료와 Barrick 지급 $1.95B',
         '2026 생산 전망 530만 온스(귀속) 유지 여부']
NONOP_WHAT = '지분법 투자·시장성 증권'
PH = ['FCX', 'NUE', 'LIN', 'APD', 'SHW', 'ECL']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소재 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': '소재 PBR 비교', 'psr': '소재 PSR 비교',
                'pcr': '소재 PCR(FCF) 비교', 'evebitda': '소재 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-23 공시)'
PREMISE = ('이익 기준 배수(PER {SM[\'PER\'][\'current\']:.1f}배 대 5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배 — 회사가 따로 밝힌 파푸아뉴기니·가나 미송금 이익 과세 $0.55B를 뺀 EPS 기준)는 5년 중 싼 쪽이지만 PSR·PBR은 비싼 쪽이라 자기 이력 {selfsc:.1f}점(중간)이다. '
           'S&P500 소재 안에서는 {peersc:.1f}점(중간)이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가보다 높지만</strong>, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}를 출발점으로 한다.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”다. 현재가를 정당화하려면 5년 매출 성장이 연 {pct(DCF[\'requiredGrowth\'])}면 된다(실제 5년 연 {pct(HIST[\'growth_5y\'])}). '
        '실제 5년 성장에는 금값 상승과 2023년 11월 Newcrest 인수가 함께 들어 있고, 지금 이익률은 최근 금값 수준에서 나온 값이다.')
FUND_TIP = ('차입금(리스·기타 금융채무 포함)이 총자산의 9.7%이고 현금이 더 많다. 이자보상배율은 손익계산서 이자비용 $35M(표준 태그가 2013년에 멈춰 손입력)으로 쟀다. '
            '당좌비율·활동성의 재고는 재고 + 유동 광석 비축분, 매출원가는 감가상각을 뺀 판매원가 기준이다.')
SELF_TIP = '최근 4분기 영업이익률이 {pct(HIST[\'margin_now\'])}로 높아 이익 기준 배수(PER·PCR·EV/EBITDA)는 5년 중 싼 쪽, 매출·자산 기준 배수(PSR·PBR)는 비싼 쪽이다.'
PEER_TIP = ('S&P500 소재(NEM 제외)와 배수 순위를 매긴 값이다.',
            '화학·건자재·포장·철강이 대부분이고 광산은 FCX(구리)와 NEM뿐이다. 차트에는 6곳만 보인다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})로 시작해 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('세 시나리오 폭이 넓다. 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}(금 실현 가격이 지금의 절반 아래였던 2024년 초 등 포함)로 돌아가면 “보수”, '
            '최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 가면 “기본”, 지금 {pct(HIST[\'margin_now\'])}가 이어지면 “낙관”이다. 값을 가르는 것은 금값이 만든 이익률이다. 지난 시점의 모델 값(DCF 시나리오 선)은 그때의 이익률·성장률로 다시 계산한 것이라 “기본” 선은 2025년 상반기에 0 근처였다.')
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 8월 10일 — Barrick과 네바다 합작사(NGM) 분쟁 종결', None,
     'Fourmile·Fiberline·Mike 프로젝트를 NGM에 출자하고 Newmont가 Barrick에 $1.95B 지급 · Barrick 북미 금 자산 상장에 동의', 'ngm', 'Newmont 공시 (SEC 8-K)'),
    ('red', '2026년 7월 23일 장 마감 후 — Q2 2026 실적', '2026-07-24',
     '매출 $6.1B(+15%) · EPS $2.06(조정 $2.10) · 금 실현 가격 $4,414(1분기 $4,900) · 2분기 기준 최대 FCF $2.2B · 다음 날 주가 −1.6%', 'q2', 'Newmont 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 14일 — Cadia 지진 활동으로 조업 일시 중단', None,
     '6월 중순 정상화 · 2분기 구리 생산 전 분기 대비 −43% · Cadia 금 생산 9.4만→3.4만 온스(전사 금 생산 −1%)', 'tenq', 'Newmont Q2 2026 10-Q·보도자료 (SEC)'),
    ('green', '2026년 4월 23일 장 마감 후 — Q1 2026 실적', '2026-04-24',
     '매출 $7.3B · EPS $3.00(조정 $2.90) · 분기 최대 FCF $3.1B · 자사주 매입 승인 $6.0B 추가 · 다음 날 주가 +8.7%', 'q1', 'Newmont 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 19일 장 마감 후 — Q4 2025 실적·2026 전망', '2026-02-20',
     '2025년 순이익 $7.2B · FCF $7.3B · 4분기 EPS $1.19(조정 $2.52) · 다음 날 주가 −2.6%', 'q4', 'Newmont 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 23일 장 마감 후 — Q3 2025 실적', '2025-10-24',
     '순이익 $1.8B · EPS $1.67(조정 $1.71) · 3분기 기준 최대 FCF $1.6B · 다음 날 주가 −6.2%', 'q3', 'Newmont 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('금값이 오르며 이익이 크게 늘었고, 주가는 1년 새 {CH_TXT}', '금값 수혜·자사주',
           ['2분기 매출 $6.1B(+15%), EPS $2.06이었다. 금 실현 가격 $4,414는 1년 전($3,320)보다 높고 1분기($4,900)보다 낮았다.',
            'Cadia가 4월 지진 활동으로 차질을 빚다 6월 중순 정상화됐고, 2분기 구리 생산은 전 분기보다 43% 줄었다.',
            '상반기 자사주 $3.5B를 샀고, 8월 Barrick과 NGM 분쟁을 끝내며 $1.95B를 내기로 했다.'],
           '이익 기준 배수는 5년 중 싼 쪽, 매출·자산 기준 배수는 비싼 쪽이고, 현금흐름 모델 기본값은 주당 ${DCF[\'base\']:.2f}로 현재가보다 높다. 이 모델은 최근 금값의 이익률에서 출발한다.',
           '10월 하순 Q3 2026 실적(회사 미확정).')
BULL = [('현금흐름', '상반기 영업현금흐름 $6.7B, FCF $5.3B.'),
        ('재무', '현금 $9.0B가 차입금·리스·기타 금융채무 $5.6B보다 많다.'),
        ('주주환원', '상반기 자사주 $3.5B, 4월 승인 $6.0B 추가.')]
BEAR = [('금값', '영업이익률 {HIST[\'margin_now\'] * 100:.0f}%는 최근 금값 수준에서 나온 값이다.'),
        ('Cadia', '4월 지진 활동으로 차질, 6월 중순 정상화. 2분기 구리 생산 −43%.'),
        ('NGM 지급', 'Barrick에 현금 $1.95B 지급 예정.')]
MISS_WHY = {('APD', 'per'): ' 적자'}   # C9 뒤 동종 파일은 perNA로 옮겨 'negative'가 빠졌다 — 카드 표기 그대로
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 15, 'mean': 141.57, 'median': 144, 'low': 110, 'high': 175, 'sb': 15, 'b': 5, 'h': 2, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-06'


# ── 자동 카드(설계 D, 2026-10-10) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose.py 제안(손 표와 숫자 일치) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {
  "nem:GoldDoreMember": [
   "금 도레",
   "#d4a017"
  ],
  "nem:SalesFromConcentrateAndOtherProductionMember": [
   "정광·기타(구리·은·아연·납 포함)",
   "#e8c766"
  ]
 },
 "ignore": []
}
