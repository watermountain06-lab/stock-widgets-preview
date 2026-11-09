CIK = '0001383312'
# BR(브로드리지) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 6월 말(FY27 = 2026-07~2027-06). 투자자 소통(주총 의결권·공시 배포, ICS)·증권 거래 처리 기술(GTO).
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-11-03 12:43 동부 장중 → 그날, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 06:5x~07:5x 동부 → 그날).
# 보류 목록 D군(안건 E54) — 30% 규칙: 최근 4분기 GAAP 희석 EPS 9.05(2.42 + 2.36 + 3.44 + 0.83) 대 회사 조정 EPS 9.69(1.59 + 2.72 + 3.82 + 1.56).
#   인수 상각은 반복 비용. 일회성(세전 주당): 디지털 자산(Canton Coin) 평가손익 −1.59 · −0.05 · +0.10 · +0.35, 투자 이익 −0.06(Q4), 인수·구조조정 비용 0.06 · 0.07 · 0.03 · 0.15
#   → 순 이익 약 0.94(세후 약 0.72, GAAP의 약 8%), 이익만 세후 약 1.29(약 14%), 비용만 세후 약 0.58(약 6%) — 어느 쪽도 30% 아래라 정식(2026-11-09).
# 엔진 입력(2026-11-09): 차입금 $3,347.1M(장기, 1년 안 만기 0), 현금 $284.1M. 세전이익 태그 IncomeLossAttributableToParent(PRETAX_TAG_BY_CIK·fetch_financials).
#   4분기 EPS FY25·FY26은 보도자료(Q4_EPS_OVERRIDE — 역산 3.17·3.42, 보도자료 3.16·3.44).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-06-30', '2025-06-30'), 'FY2026'
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'Broadridge'
S_ = 'https://www.sec.gov/Archives/edgar/data/1383312/'
SEC = S_
TENQ = S_ + '000162828026069260/br-20260930.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000138331226000030/ex991earningsrelease1q2027.htm', 'q4': S_ + '000138331226000022/ex991earningsrelease4q2026.htm',
      'q3': S_ + '000138331226000013/ex991earningsrelease3q2026.htm', 'q2': S_ + '000138331226000005/ex991earningsrelease2q2026.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="brFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 35)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 GAAP 희석 EPS($9.05)는 회사 조정 EPS($9.69)보다 조금 낮다 — 회사가 더하는 인수 무형자산 상각(반복 비용이라 카드는 GAAP 그대로 둔다)과 회사가 빼는 디지털 자산 평가이익이 서로 상당 부분 상쇄된 결과다. '
              '일회성은 회사가 보유한 디지털 자산(Canton Coin)의 평가손익이 가장 크다 — 2025년 12월 분기에 평가이익(주당 약 $1.59)이 GAAP를 부풀렸고, 2026년 9월 분기에는 코인과 CNTN 관련 평가손실 합계(주당 약 $0.35)가 GAAP를 깎았다. '
              '여기에 인수·구조조정 비용(FY26 생산 시설 한 곳 정리, 2026년 9월 분기부터 AI·생산성 계획에 따른 인력 감축 퇴직금 $15.2M — 회사는 확대를 검토 중)을 더해도 순액은 세후 추정 약 $0.72로 최근 4분기 GAAP 이익의 약 8%(이익만 따로 보면 약 14%)라 30% 기준 아래다. 다만 코인 시세에 따라 분기 GAAP가 크게 흔들린다. '
              '2025년 12월 분기에 Canton Coin 일부(3.42억 개, 당시 공정가치 $53M)를 Canton 디지털 자산 트레저리 회사(CNTN, 옛 Tharimmune) 워런트와 맞바꿨다. '
              '본업은 꾸준하다 — 반복 매출이 Q1 FY27에 +11%(유기 +9%)였다. 총매출이 +5%에 그친 것은 펀드 주총 안내 같은 이벤트성 매출이 41% 줄었기 때문이다(분기마다 크게 흔들린다). 회사는 FY27 반복 매출 +6~8%(고정환율), 조정 EPS +8~12%, 조정 영업이익률 약 21%를 예상하지만, GAAP 희석 EPS는 FY26에 든 코인 평가이익이 빠져 −8~−4% 감소로 안내한다(코인 손익은 전망에서 제외). FY26 조정 EPS는 $9.60(+12%)였고 배당을 12% 올려 연 $4.36으로 20년 연속 인상했다. '
              '2026년 1월 유럽 펀드 유통 플랫폼 Acolin, 4월 선물·옵션 주문 체결 시스템 CQG를 현금 $173M(이연·조건부 대가 별도)에 샀다. 5월 2036년 만기 5.75% 채권 $500M을 발행해 2026년 만기 채권을 갚았다. Q1 FY27에 자사주 $200M을 샀고, 8월 새 자사주 한도 $1.5B를 승인했다(9월 말 잔여 $1.3B). 보유 코인은 15억 개($185M, 원가 약 $15M)로 70%는 2029년 중반까지 잠겨 있다. 순현금 칸의 ‘장기 채권’ $234M은 연금·퇴직저축 관련 증권과 CNTN 주식이라 현금처럼 쓸 수 있는 돈이 아니다(빼면 주당 약 $2 낮아진다). '
              '주가는 2025년 12월 고점 약 $232에서 2026년 6월 약 $135까지 내렸다가 11월에 일부 회복했다.')
PH = ['IBM', 'MSFT', 'ORCL', 'CRM', 'CSCO', 'DELL']   # 카드 가격 비교(multiples_now)가 되는 IT 카드만(IT·GEN·TRMB와 같은 묶음)
PEER_FILE = None   # IT는 섹터 파일 없이 카드 유니버스 — 비교 차트도 카드 가격
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': 'IT 서비스·소프트웨어·하드웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(BR 제외)과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 섞여 있다. 차트에는 IT 서비스·소프트웨어·하드웨어 6곳만 보인다(금융 인프라 회사는 비교 가능한 카드가 없다).')
# 매출(Q1 FY27 보도자료 부문): 투자자 소통(ICS) 1,153.2 + 거래 처리 기술(GTO) 515.5 = 1,668.7.
SEG = [('투자자 소통(ICS — 주총·공시 배포)', 1153.2, '#002f6c'), ('거래 처리 기술(GTO)', 515.5, '#00a9e0')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건. 반응일: 장 전 → 그날. 색은 사건 성격, 수치는 그날 주가.
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 3일 장 전 — Q1 FY27 실적', '2026-11-03',
     '반복 매출 +11%(유기 +9%) · 이벤트성 매출 −41% · GAAP 희석 EPS $0.83(−41% — 1년 전 코인 평가이익이 올해 평가손실로 바뀐 영향) · 조정 EPS $1.56(+3%) · 자사주 $200M · FY27 전망 유지 — 그날 주가 −0.2%', 'q1', 'Broadridge 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 8월 4일 장 전 — FY26 4분기 실적 · FY27 전망', '2026-08-04',
     'FY26 GAAP·조정 EPS 모두 $9.60(조정 +12%) · 배당 12% 인상(연 $4.36) · FY27 반복 매출 +6~8%, 조정 EPS +8~12% 전망 — 그날 주가 +7.0%', 'q4', 'Broadridge 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 30일 장 전 — Q3 FY26 실적', '2026-04-30',
     '반복 매출 +7% · GAAP 희석 EPS $2.36(+15%) · 조정 EPS $2.72(+11%) · 연간 전망 상향 — 그날 주가 −4.2%', 'q3', 'Broadridge 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 3일 장 전 — Q2 FY26 실적', '2026-02-03',
     '반복 매출 +9% · GAAP 희석 EPS $2.42(디지털 자산 평가이익 주당 약 $1.59 포함) · 조정 EPS $1.59(+2%) · 조정 EPS 전망 상향 — 그날 주가 −6.2%', 'q2', 'Broadridge 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 9, 'nt': 6, 'mean': 205.33, 'median': 214, 'low': 180, 'high': 230, 'sb': 1, 'b': 4, 'h': 4, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-09'


POST = [r"""
_c1 = h[h.index('<strong style="color:var(--accent2);">①</strong>'):]; _c1 = _c1[:_c1.index('</div>')]
h = h.replace(_c1, '<strong style="color:var(--accent2);">①</strong> 반복 매출 성장(고정환율)이 FY27 전망 +6~8% 안에 있는지(Q1 +11%) — 이벤트성 매출(펀드 주총 안내 등)은 분기마다 크게 흔들려 따로 본다', 1)
h = h.replace('<span class="bb-text">Q1 FY27 매출 +5.0%(보고 기준, 3년 연평균 6.8%).', '<span class="bb-text">Q1 FY27 총매출 +5.0% — 이벤트성 매출 −41%가 깎았고 반복 매출은 +11%였다.', 1)
h = h.replace('<span class="tag">배수 5년 최저권·매출 성장 느려짐', '<span class="tag">배수 5년 최저권·이벤트성 매출 감소', 1)
h = h.replace('<div class="yoy-footnote" id="fundFootnote"></div>', '<div class="yoy-footnote" id="fundFootnote"></div>\n    <div class="yoy-footnote">BR은 주총 시즌인 3·6월 분기에 매출·이익·현금이 몰린다(10-Q 계절성) — 전분기(QoQ) 감소는 대부분 계절성이다. 1년 전 대비 순이익 감소는 대부분 디지털 자산 평가손익(1년 전 이익 → 올해 손실)과 구조조정 비용 탓이다.</div>', 1)
"""]

# ── 자동 카드 — 부문 지도(seg_map_propose 뒤 원문 대조). 원문: Q1 FY27 보도자료 1,153.2 + 515.5 = 1,668.7 ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"br:InvestorCommunicationSolutionsMember": ["투자자 소통(ICS — 주총·공시 배포)", "#002f6c"],
             "br:GlobalTechnologyAndOperationsMember": ["거래 처리 기술(GTO)", "#00a9e0"]},
 "ignore": ["br:ReportableSegmentsMember"]
}
