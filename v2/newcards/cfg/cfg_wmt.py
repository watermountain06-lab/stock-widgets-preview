# WMT v2 카드 설정 — fill.py WMT. 틀 시절 카드를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G6).
# 재현 모드: python3 v2/newcards/build.py WMT --from-card (일봉·이동평균·백테스트는 지금 카드에서).
BUILD = {}
CIK = '0000104169'
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q2 FY27', 'Q2 FY26', 'Q1 FY27'
RELEASE = {'rev': 186100, 'op': 9383, 'ni': 6366}   # Q2 FY27 보도자료(백만 달러) — 순매출(엔진 매출 태그). 카드 차트는 총수익(PRE)
PRE = ["rev = q(['Revenues'])   # 옛 카드 차트·YoY는 총수익(순매출 + 회원 수수료 등, Q2 $187.9B) — 배수·내재가치는 순매출"]
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Walmart'
S_ = 'https://www.sec.gov/Archives/edgar/data/104169/'
SEC = S_
PR = {'q2': S_ + '000010416926000145/earningsreleasefy27q2.htm', 'q1': S_ + '000010416926000095/earningsreleasefy27q1.htm',
      'q4': S_ + '000010416926000032/earningsreleasefy26q4.htm', 'q3': S_ + '000010416925000177/earningsreleasefy26q3.htm'}
PR_CUR = 'q2'
TENQ = PR['q2']; TENQ_NAME = 'Q2 FY27 실적 보도자료'   # 옛 카드 건전성 메모엔 링크가 없다(POST에서 뺀다)
LINKS = {'ceo': S_ + '000010416925000172/pressrelease111425.htm', 'nasdaq': S_ + '000010416925000177/pressrelease-transfertonas.htm'}
FY_ENDS = ('2026-01-31', '2025-01-31')
L8 = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27', 'Q2 FY27']
FAIRBAND_TITLE = 'id="wmtFairBand" title="최근 1년 PER {FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배(25~75% 구간) × 현재 EPS. 최근 1년이 5년 이력(중앙값 {SM[\'PER\'][\'median\']:.1f}배)보다 비싼 구간이라, 현재가가 이 밴드 아래여도 5년 기준 PER로는 중간이다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
FCF_SUB = '현금창출력'
CAPEX_SUB = '미래 재투자'
STAT3 = ('R&amp;D (Q2 FY27)', '해당 없음', '유통업 — 연구개발비를 따로 공시하지 않는다')
OPM_RANGE, Y2 = (0, 8), (0, 8)
NEXT = ('11월 중순 예상', '일정 · Q3 FY27')
NEXT_OP = ('11월 중순', 'Q3 FY27 예상')
FY_LABEL = 'FY26'
HEALTH_NOTE = '유동비율 76.7%·당좌비율 23.4%로 낮지만, 재고를 팔아 공급업체 대금을 치르는 유통업 구조다(재고 소진 41일, 매입채무 지급 42일). 총차입금은 금융리스 포함 $57.2B(보도자료)다. 이자보상배율 14.7배는 2분기 부채 이자 $137M에 들어간 일회성 이자비용 감소 $0.5B(미인식 세무 혜택 변동, 10-Q 법인세 주석)를 되돌린 값이다.'
YOY_EXTRA = ''
FOOT_MID = '매출은 총수익(순매출 + 회원 수수료 등, 배수·내재가치는 순매출 Q2 $186.1B를 쓴다) · 2분기 매출원가에 관세 환급 약 $2.9B 차감 · 순이익에는 지분 투자 평가손실(2분기 기타 손실 $1.2B)이 들어 있다'   # 옛 카드 두 각주의 'GAAP 기준'과 'FCF' 사이 설명
SEG = [('Walmart U.S.', 125200, '#0071ce'), ('Walmart International', 35200, '#ffc220'), ("Sam's Club U.S.", 25700, '#3498db')]   # 보도자료 $B 한 자리(옛 도넛 그대로)를 백만 달러로
SEG_ADJ = 187937 - 186100   # 차트 매출은 총수익(PRE) — 세 부문 순매출 합 $186.1B와의 차이는 회원 수수료 등
SEG_TITLE = '매출 구성 — 부문별 순매출'
SEG_NOTE = '전년 대비 Walmart U.S. +3.5%(기존점 +2.6%), International +12.8%(고정 환율 +7.9%), Sam\'s Club +8.8% · 부문 영업이익 성장은 +20.6%·+16.6%·+44.3% · 출처: <a href="https://www.sec.gov/Archives/edgar/data/104169/000010416926000145/earningsreleasefy27q2.htm" target="_blank" rel="noopener">Walmart Q2 FY27 실적 보도자료 (SEC 8-K) →</a>'
CAPITAL = [('자사주 매입 (상반기, 4,230만 주)', '$5.1B'), ('잔여 바이백 승인 한도 (2026년 2월 $30B 승인)', '$25.1B'), ('배당 지급 (상반기)', '연 $0.99로 인상(2월)', '$3.9B')]
CHECK_WHEN = '2026년 11월 중순 (예상) · Q3 FY27'
CHECK = ['3분기 가이던스 달성 여부 — 순매출 +3.0~3.75%, 조정 영업이익 +2~4%(고정 환율), 조정 EPS $0.62~0.64', '미국 기존점 매출(2분기 +2.6%)이 약국 디플레이션 역풍(125bp)을 넘어 다시 오르는지', '남은 관세 환급을 가격 인하에 다시 쓰는 동안 매출총이익률(2분기 +96bp)이 유지되는지', '광고(+38%)·회원 수수료(+17%)가 영업이익률(최근 4분기 {pct(HIST[\'margin_now\'])})을 얼마나 끌어올리는지']
NONOP_WHAT = '지분·장기투자'
PH = ['COST', 'TGT', 'DG', 'DLTR', 'KR', 'SYY']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '대형 유통 PER 비교', 'pbr': '대형 유통 PBR 비교', 'psr': '대형 유통 PSR 비교', 'pcr': '대형 유통 PCR(FCF) 비교', 'evebitda': '대형 유통 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 필수소비재 섹터(S&amp;P500 34종목)보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 34종목 대비 배수 순위(v2/peer_universe/consumer_staples.json)'
FUND_ASOF_NOTE = 'Q2 FY27 10-Q (2026-08-28 공시)'
PREMISE = '자기 5년 이력으로는 PER이 중간이고 나머지 네 배수가 비싼 쪽이라 {selfsc:.1f}점({score_word(selfsc)})이며, S&P500 필수소비재 34종목 안에서는 {peersc:.1f}점({score_word(peersc)})이다. <strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다. 영업이익률 {int(HIST[\'margin_now\'] * 100)}%대에 매출 성장 연 {HIST[\'growth_5y\'] * 100:.0f}%인 회사는 할인율 10%에서 현재가에 한참 못 미친다.'
RISK = '매출이 지난 5년 속도(연 {pct(HIST[\'growth_5y\'])})로 크다가 식는다면, 현재가가 정당하려면 영업이익률이 <strong data-vs="req">{pct(DCF[\'requiredMargin\'])}</strong>여야 한다(최근 4분기 {pct(HIST[\'margin_now\'])}, 5년 중앙값 {pct(HIST[\'margin_5y\'])}). 광고·회원 수익이 마진을 얼마나 올리느냐가 관건이다.'
FUND_TIP = "이자보상배율은 2분기 부채 이자에 들어간 일회성 이자비용 감소 $0.5B(미인식 세무 혜택 변동)를 되돌려 계산했다(v2/interest_extra.json). 매출채권은 'Receivables, net'(ReceivablesNetCurrent)을 썼다."
SELF_TIP = 'PER {SM[\'PER\'][\'current\']:.1f}배는 5년 이력의 {SM[\'PER\'][\'percentile\']:.0f}% 지점(중간)이고 PSR·PBR·PCR·EV/EBITDA는 상위 {min(100 - SM[k][\'percentile\'] for k in (\'PSR\', \'PBR\', \'PCR\', \'EV/EBITDA\')):.0f}~{max(100 - SM[k][\'percentile\'] for k in (\'PSR\', \'PBR\', \'PCR\', \'EV/EBITDA\')):.0f}% 안쪽이다. 2024년 2월 3:1 분할은 EPS 이력에 반영했다.'
PEER_TIP = ('S&P500 필수소비재 34종목과 배수 순위를 매긴 값이다(카드 유니버스엔 필수소비재가 6종목뿐이라 넓혔다).', '유통·식품·음료·생활용품·담배가 섞여 있다. 매출 배수는 마진이 얇은 유통업체가 낮게 나온다. COST는 분기 길이가 불규칙해(12·12·12·16주) 엔진의 최근 4분기 합산에서 빠져 PER·PBR만 계산됐다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 내려간다.', '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 내려간다.', '3년 성장률(연 {pct(HIST[\'growth_3y\'])})에서 출발하고 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다. 5년 뒤 순매출 약 $880B.']
DCF_NOTE = ''
NEWS_RANGE = '2025.11 ~ 2026.09'
NEWS = [('', '2026년 8월 20일 개장 전 — Q2 FY27 실적', '2026-08-20', '매출 $187.9B(+5.9%) · 영업이익 +28.8%(조정·고정 환율 +17.4%, 둘 다 관세 환급 약 $2.9B 포함 · 회사는 환급을 빼면 가이던스 상단이라 했다) · 미국 기존점 +2.6% · FY27 가이던스 상향', 'q2', 'Walmart 실적 보도자료 (SEC 8-K)'), ('', '2026년 5월 21일 개장 전 — Q1 FY27 실적', '2026-05-21', '매출 +7.3% · 영업이익 +5.0%(물류 연료비 부담 250bp) · 이커머스 +26% · FY27 가이던스 유지', 'q1', 'Walmart 실적 보도자료 (SEC 8-K)'), ('', '2026년 2월 19일 개장 전 — Q4 FY26 실적', '2026-02-19', '매출 $190.7B(+5.6%) · 영업이익 +10.8% · 자사주 $30B 승인 · 연 배당 $0.99로 인상 · FY27 조정 EPS $2.75~2.85', 'q4', 'Walmart 실적 보도자료 (SEC 8-K)'), ('neutral', '2025년 12월 9일 — 나스닥으로 상장 이전', None, 'NYSE에서 나스닥 글로벌 셀렉트로 옮겼다 · 티커 WMT 유지(11/20 발표)', 'nasdaq', 'Walmart 발표 (SEC 8-K)'), ('', '2025년 11월 20일 개장 전 — Q3 FY26 실적', '2025-11-20', '매출 +5.8% · 조정 EPS $0.62 · 이커머스 +27% · FY26 가이던스 상향', 'q3', 'Walmart 실적 보도자료 (SEC 8-K)'), ('neutral', '2025년 11월 14일 — CEO 교체 발표', '2025-11-14', '더그 맥밀런 CEO 1월 말 은퇴 · 2월 1일부터 존 퍼너(월마트 U.S. CEO)가 CEO', 'ceo', 'Walmart 발표 (SEC 8-K)')]
SUMMARY = ('이커머스·광고·회원 수익으로 이익이 매출보다 빨리 는다', '안정 성장·밸류 부담', ['네 분기 매출 성장률이 5.6~7.3%였고, 글로벌 이커머스는 매 분기 23~27% 늘었다. 2분기 광고는 38%, 회원 수수료는 17% 늘었다.', '2분기 영업이익 +28.8%(조정 +17.4%)에는 둘 다 관세 환급 약 $2.9B가 들어 있다. 회사는 남은 환급을 대부분 가격 인하에 다시 쓴다고 했다.', '2월에 존 퍼너가 CEO가 됐고, 12월에 나스닥으로 상장을 옮겼다. 2월에 자사주 $30B를 승인했다.'], '미국 기존점 매출 증가율이 4.5% → 4.6% → 4.1% → 2.6%로 둔화했다(2분기엔 약국 디플레이션 125bp). 최근 두 실적일(5월 가이던스 유지, 8월 상향) 모두 주가가 −7%, −9% 빠졌다.', 'Q3 FY27 실적(11월 중순 예상)에서 순매출 +3.0~3.75%·조정 영업이익 +2~4% 가이던스, 미국 기존점 매출 반등.')
BULL = [('이커머스', '2분기 글로벌 이커머스 +23%, 광고 +38%, 회원 수수료 +17%였다.'), ('가이던스', 'FY27 조정 영업이익 전망을 +7.0~8.5%로 올렸다(고정 환율).'), ('주주환원', '상반기 자사주 $5.1B·배당 $3.9B를 썼고, $30B 승인 중 $25.1B가 남았다.')]
BEAR = [('밸류', '기본 내재가치가 현재가의 {DCF[\'base\'] / px * 100:.0f}%이고, 현재가가 정당하려면 영업이익률 {pct(DCF[\'requiredMargin\'])}가 필요하다.'), ('성장 둔화', '미국 기존점 매출 증가율이 2.6%로 낮아졌고, 3분기 조정 영업이익 가이던스는 +2~4%다.'), ('현금흐름', '상반기 잉여현금흐름이 $5.5B로 $1.4B 줄었다. 설비투자가 $14.2B로 늘었다.')]
ANALYST = {'rating': 'Buy', 'n': 43, 'nt': 28, 'mean': 128.86, 'median': 130, 'low': 110, 'high': 155, 'sb': 27, 'b': 10, 'h': 5, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-10'
POST = [r'''
for _cmp in ('2025.07.31(Q2 FY26)', '2026.04.30(Q1 FY27)'):
    one("vs " + _cmp + " · GAAP 기준 · FCF는", "vs " + _cmp + " · GAAP 기준 · " + C.FOOT_MID + " · FCF는")
# 건전성 메모엔 링크가 없었다
one(' <a href="' + C.TENQ + '" target="_blank" rel="noopener">' + C.TENQ_NAME + ' (SEC) →</a></div>', '</div>')
one('FY26 말 $284.7B(전년 $260.8B) · 연간 지표</span>', 'FY26 $284.7B(전기 $260.8B) · 연간 지표, FY27 마감 전까지 동일</span>')
# 헤더 거래소·업종 줄(옛 카드 — 2025-12-09 나스닥 이전, 1월 말 결산)
sub(r'(<span style="font-size:11px;color:var\(--accent\);font-weight:600;">)[^<]*(</span>)', lambda m: m.group(1) + 'NASDAQ(2025.12.09 NYSE에서 이전) · 필수소비재 · 대형 유통 · 1월 말 결산' + m.group(2))
one('<div class="card-title">자본배분 · 주주환원 (Q2 FY27 · 2026.07.31 기준)</div>', '<div class="card-title">자본배분 · 주주환원 (FY27 상반기 · 2026.07.31 기준)</div>')
'''
]


# ── 자동 카드(설계 D, 2026-10-11) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose2·3 제안(손 표와 숫자 일치 — 여러 축·나머지 줄) ──
AUTO = True
SEG_MAP = {
 "parts": [
  {
   "concepts": [
    "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
   ],
   "axis": "srt:ConsolidationItemsAxis",
   "extra": {
    "us-gaap:StatementBusinessSegmentsAxis": "wmt:WalmartInternationalMember"
   },
   "members": {
    "us-gaap:OperatingSegmentsMember": [
     "Walmart International",
     "#ffc220"
    ]
   }
  },
  {
   "concepts": [
    "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
   ],
   "axis": "srt:ConsolidationItemsAxis",
   "extra": {
    "us-gaap:StatementBusinessSegmentsAxis": "wmt:WalmartUSMember"
   },
   "members": {
    "us-gaap:OperatingSegmentsMember": [
     "Walmart U.S.",
     "#0071ce"
    ]
   }
  },
  {
   "concepts": [
    "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
   ],
   "axis": "us-gaap:StatementBusinessSegmentsAxis",
   "extra": {},
   "members": {
    "wmt:SamsClubUSMember": [
     "Sam's Club U.S.",
     "#3498db"
    ]
   }
  }
 ]
}
# 손 문구 블록 정리: 화면 구조 고침만 남기고 분기 문장·날짜 박힌 치환·손 데이터 블록은 뺐다(자동 카드는 못 찾으면 건너뜀)
POST = ['sub(r\'(<span style="font-size:11px;color:var\\(--accent\\);font-weight:600;">)[^<]*(</span>)\', lambda m: m.group(1) + \'NASDAQ(2025.12.09 NYSE에서 이전) · 필수소비재 · 대형 유통 · 1월 말 결산\' + m.group(2))']
