# MMM(3M) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 138(시총 136위). 산업용·안전·운송·전자·소비자 소재.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-20 장 마감 뒤 접수 → 기준일 10/21), 실적 보도자료(Q3 2025~Q3 2026, 8-K 2.02항), 8-K 7.01(Amazon 워런트 2026-10-19), 3M 보도자료(Madison 2026-03-19), StockAnalysis.
# 분사: 2024-04-01 Solventum(헬스케어) — GE 방식(RESTATED_LATEST, HISTORY_START 2024-07-26, DCF HISTORY_WINDOW 2024-03-31부터). 1196:1000은 분사 가격 조정이지 분할이 아니다(KNOWN_SPLITS []).
# 엔진 입력(2026-10-21): 차입금 $14,997M(DebtCurrent 2,439 + LongTermDebtNoncurrent 12,558 — 기본은 장기만), 현금 $4,835M(제한 현금 포함 태그 — 기본 태그는 2017년에 멈춤), 시장성 증권 $310M(매도가능 채권 태그).
# 인수 대금 Madison $1,910M: 1년 전 인수 줄이 없어 엔진 최근 4분기가 0이었다 → build_dcf.ACQ_MISSING_AS_ZERO(2025년 "인수 줄 없음 = 0" 확인). Solventum 지분(유동자산 안)은
# 표준 태그가 2026-03에서 멈춰 nonop_extra.json에 분기별 10-Q 값(2024-06~2026-09, 최신 $2,254M, "current" — 운전자본에서도 뺌). 이 둘을 바로잡아 최근 매출/자본 1.27배(평균 대체 해제, Codex r1).
# Bain 청구권: 상환가능 비지배지분 $971M(nci 태그 추가) + 순풋옵션 파생부채 $340M(nonop_extra 음수) — 10-Q가 비지배지분을 파생상품 가치를 고려해 측정한다고 적어 겹치지 않는다.
BUILD = {}
CIK = '0000066740'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = '3M'
S_ = 'https://www.sec.gov/Archives/edgar/data/66740/'
SEC = S_
TENQ = S_ + '000006674026000311/mmm-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000006674026000308/q32026-8kerexx991.htm', 'q2': S_ + '000006674026000242/q22026-8kerexx991.htm',
      'q1': S_ + '000006674026000171/q12026-8kerexx991.htm', 'q4': S_ + '000006674026000003/q42025-8kerexx991.htm',
      'q3p': S_ + '000006674025000086/q32025-8kerexx991.htm'}
LINKS = {'amzn': S_ + '000006674026000303/mmm-20261019.htm',
         'madison': 'https://investors.3m.com/news-events/press-releases/detail/1922/3m-to-create-a-leading-fire-and-safety-business'}
FAIRBAND_TITLE = 'id="mmmFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 연 {pct(HIST[\'growth_5y\'])} — 분사 뒤)</span>'
Y2 = (10, 60)
GROWTH_SPAN = '분사 뒤 계속사업 이력(2024-03 이후)'   # 역산 설명의 '지난 5년' 자리(Fable r1 필수)
SELF_SPAN = '분사 뒤, 2024-07 이후'   # 자기 이력 '5년' 표기 자리
ACT_REASON = ''
NONOP_WHAT = '남은 Solventum 지분 등 투자'
# 고정 문장(숫자 없음). 분사 뒤 짧은 이력, 소송·PFAS 비용, Solventum 지분 평가 손익, 작은 자본.
MODEL_NOTE = ('이력은 Solventum(헬스케어) 분사 뒤 계속사업 숫자만 써서 짧다. 영업이익에는 귀마개·PFAS 소송과 PFAS 생산 철수 비용이 분기마다 섞이고, '
              '순이익에는 남은 Solventum 지분의 평가 손익이 들어가 PER과 분기 EPS가 크게 흔들린다. 소송 합의 비용과 자사주 매입으로 자본이 작아 PBR·부채비율이 높게 나온다. 소송·환경 미지급금은 차입금 밖의 큰 부채라 이 모델의 순부채에 들어가지 않는다.')
PH = ['HON', 'GE', 'EMR', 'ITW', 'ETN', 'DOV']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '산업재 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '산업재 PBR 비교', 'psr': '산업재 PSR 비교',
                'pcr': '산업재 PCR(FCF) 비교', 'evebitda': '산업재 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(MMM 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·건설 회사가 섞여 있다. 차트에는 복합 산업재 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 안전·산업 3,182 + 운송·전자 1,999 + 소비자 1,307 = 6,488, 본사·기타 96을 더해 6,584. 1년 전 2,917/1,992/1,312, 본사 296 → 6,517.
SEG = [('안전·산업', 3182, '#e4002b'), ('운송·전자', 1999, '#ff6b6b'), ('소비자', 1307, '#ffb3b3')]
SEG_ADJ = 96
SEG_TITLE = '매출 구성 — 사업 부문별'
SEG_ADJ_LABEL = '본사·기타(매각·정리 중인 사업 등)'
# 손 뉴스: 최신 실적(Q3 2026, 10/20)도 손으로 쓴다 — 하루 전 Amazon 8-K(10/19)가 자동 항목 창(d−1)에 걸린다. 가이던스·조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K는 모두 장중 접수(보도자료는 장 전) — Q3 10/20 14:35 → 10/20, Q2 7/21 → 7/21, Q1 4/21 → 4/21, Q4 1/20 16:34 → 1/20, Q3 2025 10/21 → 10/21.
# Amazon 8-K 접수 2026-10-20 00:55 UTC = 10/19(월) 20:55 동부(장 마감 뒤) → 반응일 10/20, 실적과 같은 날(Codex r1 필수 — 처음엔 하루 틀리게 읽었다). Madison은 8-K 없음(3M 보도자료 3/19, 7/1 완료).
# 넣지 않은 8-K: 이사 선임(2/5·6/8), 주총(5/13), 대출 약정(5/6 Madison 인수 자금 $1.43B·8/19 신용 한도), 유로 회사채(9/10).
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 20일 — Q3 2026 실적', '2026-10-20',
     '매출 $6.58B(+1.0%) · 희석 EPS $2.63(1년 전 $1.55 — 이번 분기에 Solventum 지분 평가이익 주당 $0.60) · 영업이익률 23.7%', 'q3', '3M 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 10월 19일 장 마감 뒤 — Amazon과 데이터센터 공급 확대 · 워런트 발행', '2026-10-20',
     'Amazon 자회사에 3M 주식 최대 316만 주를 주당 $164.89에 살 수 있는 7년 워런트 — 85%는 Amazon의 광연결 등 데이터센터 제품 구매액에 따라 확정(누적 $6B에서 전부) · 주가 반응은 다음 날 Q3 실적과 섞인다', 'amzn', '3M 공시 (SEC 8-K)'),
    ('green', '2026년 7월 21일 — Q2 2026 실적', '2026-07-21',
     '매출 $6.50B(+2.4%) · 희석 EPS $1.78(1년 전 $1.34 — 이번 분기에 Dyneon(독일 PFAS 생산 자회사) 매각 손실 주당 $0.61, Solventum 지분 평가이익 주당 $0.60) · 영업이익률 15.1%(1년 전 18.0%)', 'q2', '3M 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 21일 — Q1 2026 실적', '2026-04-21',
     '매출 $6.03B(+1.3%) · 희석 EPS $1.23(1년 전 $2.04 — 이번 분기에 Solventum 지분 평가손 주당 $0.67)', 'q1', '3M 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 19일 — Madison Fire & Rescue 인수 발표', '2026-03-19',
     'Bain Capital과 함께 $1.95B에 인수하고 3M의 Scott Safety와 합친 새 회사 지분 50.1%를 갖는다(7월 1일 완료)', 'madison', '3M 보도자료 (SEC 공시 없음)'),
    ('red', '2026년 1월 20일 — Q4 2025 실적', '2026-01-20',
     '매출 $6.13B(+2.0%) · 희석 EPS $1.07(1년 전 $1.33) · 영업이익률 13.0%(1년 전 18.1%) · 2025년 매출 $24.95B·EPS $6.00', 'q4', '3M 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 21일 — Q3 2025 실적', '2025-10-21',
     '매출 $6.52B(+3.5%) · 희석 EPS $1.55(1년 전 $2.48 — 1년 전 분기에 Solventum 지분 평가이익 주당 $1.05)', 'q3p', '3M 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 19, 'nt': 12, 'mean': 190.92, 'median': 197, 'low': 135, 'high': 218, 'sb': 8, 'b': 1, 'h': 8, 's': 2, 'ss': 0}
ANALYST_ASOF = '2026-10-21'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(사업 부문 3개). 본사·기타는 SEG_ADJ(분기마다 다시 정함).
# 원문 대조: Q3 2026 3,182/1,999/1,307(본사 96), 1년 전 2,917/1,992/1,312(본사 296)(2026-10-21) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "mmm:SafetyAndIndustrialSegmentMember": [
   "안전·산업",
   "#e4002b"
  ],
  "mmm:TransportationAndElectronicsSegmentMember": [
   "운송·전자",
   "#ff6b6b"
  ],
  "mmm:ConsumerSegmentMember": [
   "소비자",
   "#ffb3b3"
  ]
 },
 "ignore": []
}
