# HD v2 카드 설정 — fill.py HD. 틀 시절 카드를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G6).
# 재현 모드: python3 v2/newcards/build.py HD --from-card (일봉·이동평균·백테스트는 지금 카드에서).
BUILD = {}
CIK = '0000354950'
CUR, YO, QO = '2026-08-02', '2025-08-03', '2026-05-03'
QLABEL, YL, QQL = 'Q2 FY26', 'Q2 FY25', 'Q1 FY26'
RELEASE = {'rev': 47861, 'op': 6839, 'ni': 4766}   # Q2 FY2026 보도자료 손익계산서(백만 달러)
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'The Home Depot'
S_ = 'https://www.sec.gov/Archives/edgar/data/354950/'
SEC = S_
PR = {'q2': S_ + '000035495026000145/hd_exhibit991x08022026.htm', 'q1': S_ + '000035495026000101/hd_exhibit991x05032026.htm',
      'q4': S_ + '000035495026000026/hd_exhibit991x02012026.htm', 'q3': S_ + '000035495025000238/hd_exhibit991x11022025.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000162828026058715/hd-20260802.htm'; TENQ_NAME = 'Q2 FY2026 10-Q'
LINKS = {'ceo': S_ + '000035495026000141/exhibit991august2026.htm'}
FY_ENDS = ('2026-02-01', '2025-02-02')
L8 = ['Q3 FY24', 'Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26']
FAIRBAND_TITLE = 'id="hdFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}. 주가가 1년 새 {-ch:.0f}% 내려 지금 PER({SM[\'PER\'][\'current\']:.1f}배)이 그 구간 아래라 현재가가 밴드보다 낮다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('R&amp;D (Q2 FY26)', '해당 없음', '연구개발비를 따로 공시하지 않는다')
OPM_RANGE, Y2 = (5, 16), (5, 16)
NEXT = ('11월 중순 예상', '일정 · Q3 FY26 (회사 미확정)')
NEXT_OP = ('11월 중순', 'Q3 FY26 예상')
FY_LABEL = 'FY2025'
HEALTH_NOTE = '유동비율 107.8%, 재고($26.8B)를 뺀 당좌비율 31.1%다. 차입금은 $52.9B(기업어음 $4.2B + 1년 안 만기 $4.7B + 장기 $44.0B, 금융리스 포함)이고 현금은 $2.1B다. 상반기에 장기차입금 $3.0B를 갚았다. 부채비율 558%는 누적 자사주($96.0B)로 자본이 $16.6B로 작아서다.'
YOY_EXTRA = ''
SEG = [('건축 자재', 14432, '#f96302'), ('인테리어(데코)', 13929, '#ffb07a'), ('공구·원예 등(하드라인)', 14445, '#9b59b6'), ('기타(SRS·GMS 등)', 5055, '#94a3b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 품목군별 매출'
SEG_NOTE = '주력 매장 매출은 1년 전보다 1.5% 늘었고, 기타(전문 유통 자회사)는 $3.1B → $5.1B로 늘었다 · 비교 가능 매출 +1.7%(미국 +1.3%) · 출처: <a href="https://www.sec.gov/Archives/edgar/data/354950/000162828026058715/hd-20260802.htm" target="_blank" rel="noopener">Q2 FY2026 10-Q (SEC) →</a>'
CAPITAL = [('자사주 매입 (2024년 3월부터 중단)', '$0'), ('잔여 바이백 승인 한도 (2026.08.02 기준, $15.0B 중)', '약 $11.7B'), ('배당 (Q2 FY26 지급)', '분기 $2.33(2월 1.3% 인상)', '$2.3B')]
CHECK_WHEN = '2026년 11월 중순 (예상) · Q3 FY26'
CHECK = ['연간 전망(매출 +2.5~4.5%, 비교 가능 매출 0~+2%, 영업이익률 12.4~12.6%, EPS 0~+4%) 유지 — 관세 환급(IEEPA)으로 연료·원가 상승을 일부 메운다는 전제', '비교 가능 매출(2분기 +1.7%)과 주택 경기 — 회사는 고객이 작은 공사 위주로 움직인다고 했다', '에드워드 데커 CEO의 의료 휴직(8월 12일 발표)과 임시 운영 체제', '차입금 상환(상반기 $3.0B)과 2024년 3월부터 멈춘 자사주 매입 재개 여부']
NONOP_WHAT = '지분·장기투자'
PH = ['LOW', 'TSCO', 'TJX', 'WSM', 'ULTA', 'BBY']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '주택·소매 유통 PER 비교', 'pbr': '주택·소매 유통 PBR 비교', 'psr': '주택·소매 유통 PSR 비교', 'pcr': '주택·소매 유통 PCR(FCF) 비교', 'evebitda': '주택·소매 유통 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&amp;P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 47종목 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
FUND_ASOF_NOTE = 'Q2 FY26 10-Q (2026-08-25 공시)'
PREMISE = '주가가 1년 새 {-ch:.0f}% 내렸고 {HD_LOW_PREM}. PSR·PCR이 5년 중 가장 싼 쪽이고 자기 이력은 {selfsc:.1f}점이다. 다만 PBR {SM[\'PBR\'][\'score\']:.0f}점은 자본이 $0.2~1.8B에 그쳤던 2022~2024년이 이력에 섞인 탓이다. S&P500 경기소비재 안에서는 {peersc:.1f}점({score_word(peersc)})이다. <strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.'
RISK = '매출이 지난 5년 속도(연 {pct(HIST[\'growth_5y\'])})로 크다가 식는다면, 현재가가 정당하려면 영업이익률이 <strong data-vs="req">{pct(DCF[\'requiredMargin\'])}</strong>여야 한다(최근 4분기 {pct(HIST[\'margin_now\'])}, 회사의 올해 전망 12.4~12.6%). 낙관 시나리오와 기본이 ${DCF[\'base\']:.0f}로 같다. 낙관은 3년 성장률({pct(HIST[\'growth_3y\'])})과 최근 4분기 마진({pct(HIST[\'margin_now\'])})이 5년 성장률·2년 마진({pct(HIST[\'margin_2y\'])})보다 낮지만, 기본이 쓰는 최근 1년 매출/자본(0.48)이 평균보다 낮아 재투자가 커서 두 효과가 비슷하게 상쇄된다.'
FUND_TIP = '당좌비율 1점은 재고가 큰 유통 구조, 부채비율 1점은 자사주로 자본이 작아서다. 영업이익 3년 연 증가율 −4.6%(1점)는 FY2022 정점 대비다.'
SELF_TIP = 'PSR {SM[\'PSR\'][\'current\']:.2f}배·PCR {SM[\'PCR\'][\'current\']:.1f}배는 5년 중 가장 싼 쪽이다. PBR {SM[\'PBR\'][\'current\']:.1f}배가 {SM[\'PBR\'][\'score\']:.0f}점인 것은 누적 자사주로 자본이 작아 비교 기준이 왜곡돼서다(자본이 작은 회사의 PBR 규칙은 v2.1에서 미룸). 자본이 음수였던 2022년 상반기는 빠져 PBR 이력이 {SM[\'PBR\'][\'days\'] / 252:.1f}년이고, 자본이 $0.2~1.8B에 그친 2022년 하반기~2024년 초가 PBR 수백~{SM[\'PBR\'][\'max\']:,.0f}배로 들어가 있다(규칙대로 두고 명시, 2026-10-01 결정).'
PEER_TIP = ('S&P500 경기소비재(47종목)와 배수 순위를 매긴 값이다(카드 유니버스는 IT와 섞여 있어 넓혔다).', '유통·자동차·여행·외식·의류 등이 섞여 있다. PBR은 자사주로 자본이 작은 회사가 많아 흔들린다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.', '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.', '3년 성장률(연 {pct(HIST[\'growth_3y\'])})에서 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [('', '2026년 8월 18일 장 전 — Q2 FY2026 실적', '2026-08-18', '매출 $47.9B(+5.7%, 비교 가능 +1.7%)·EPS $4.79(조정 $4.92) · 기대 이상, 연간 전망 유지(관세 환급 반영)', 'q2', 'The Home Depot 실적 보도자료 (SEC 8-K)'), ('neutral', '2026년 8월 12일 장 전 — CEO 의료 휴직', '2026-08-12', '에드워드 데커 의장 겸 CEO가 일시 의료 휴직 · 앤마리 캠벨 수석부사장이 운영, 리처드 맥페일 CFO가 재무·전문 유통 자회사를 맡는다', 'ceo', 'The Home Depot 공시 (SEC 8-K)'), ('', '2026년 5월 19일 장 전 — Q1 FY2026 실적', '2026-05-19', '매출 $41.8B(+4.8%, 비교 가능 +0.6%)·EPS $3.30(조정 $3.43) · 연간 전망 유지', 'q1', 'The Home Depot 실적 보도자료 (SEC 8-K)'), ('', '2026년 2월 24일 장 전 — Q4 FY2025 실적·FY2026 전망', '2026-02-24', 'FY2025 매출 $164.7B(+3.2%)·EPS $14.23 · 배당 1.3% 인상 · FY2026 EPS 0~+4% 전망', 'q4', 'The Home Depot 실적 보도자료 (SEC 8-K)'), ('', '2025년 11월 18일 장 전 — Q3 FY2025 실적', '2025-11-18', '매출 $41.4B(+2.8%, GMS 약 $0.9B 포함)·EPS $3.62 · 폭풍 피해 수요 부족 등으로 회사 기대에 못 미침, 연간 전망 수정', 'q3', 'The Home Depot 실적 보도자료 (SEC 8-K)')]
SUMMARY = ('매장 매출은 0~2%대로 정체하고 인수로 매출을 늘리는 중, 주가는 1년 새 크게 내렸다', '저성장·조정', ['비교 가능 매출 증가율은 1분기 +0.6%, 2분기 +1.7%였고, 회사는 올해 0~+2%를 전망한다.', "GMS(2025년 9월)·Mingledorff's(2026년 5월) 인수로 전문 시공업자 대상 매출이 늘었고, 자사주 매입은 2024년 3월부터 멈춘 채 차입금을 갚고 있다.", '주가는 1년 새 {ch:.0f}%이고, {HD_LOW_TXT}. 8월에는 CEO가 의료 휴직에 들어갔다.'], '배수는 5년 중 싼 쪽이지만, 현금흐름 모델로는 현재가의 {DCF[\'base\'] / px * 100:.0f}%만 설명된다.', 'Q3 FY26 실적(11월 중순 예상)의 비교 가능 매출과 연간 전망 유지, CEO 복귀 여부.')
BULL = [('배수', 'PSR {SM[\'PSR\'][\'current\']:.2f}배·PCR {SM[\'PCR\'][\'current\']:.1f}배가 5년 중 가장 싼 쪽, PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배).'), ('실적', '2분기 실적이 회사 기대를 넘었고 연간 전망을 유지했다.'), ('배당', '분기 배당 $2.33, 2분기 지급 $2.3B.')]
BEAR = [('성장', '비교 가능 매출 0~+2%, 영업이익 3년 연 −4.6%.'), ('부채', '차입금 $52.9B, 자사주 매입 중단 상태.'), ('경영', '8월부터 CEO 의료 휴직으로 임시 운영 체제다.')]
ANALYST = {'rating': 'Buy', 'n': 36, 'nt': 21, 'mean': 392.76, 'median': 400, 'low': 342, 'high': 425, 'sb': 18, 'b': 4, 'h': 14, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-10'
POST = [r'''
# QoQ 각주의 계절성 설명, 보도자료 이름은 회계연도 표기, 총자산 메모(회계연도 말 날짜·GMS)
one("vs 2026.05.03(Q1 FY26) · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · <a", "vs 2026.05.03(Q1 FY26) · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · 매출·이익은 성수기인 2분기가 1분기보다 크다(FCF는 예외) · <a")
h = h.replace('The Home Depot Q2 FY26 실적 보도자료 (SEC 8-K)', 'The Home Depot Q2 FY2026 실적 보도자료 (SEC 8-K)')
one('FY2025 말 $105.1B(전년 $96.1B) · 연간 지표</span>', 'FY2025 말(2026-02-01) $105.1B(전년 $96.1B, GMS 인수 반영) · 연간 지표</span>')
# 분기 차트 아래 설명(옛 카드)
one('<canvas id="hdRevChart"></canvas>\n    </div>\n', '<canvas id="hdRevChart"></canvas>\n    </div>\n'
    '    <div class="yoy-footnote" style="margin-top:8px;">회계연도는 1월 말·2월 초에 끝난다(Q2 FY26 = 2026년 5~7월). 2분기가 매출·마진이 가장 큰 성수기다. FY2024는 53주라 4분기에 한 주(매출 약 $2.5B)가 더 있었다. 2025년 9월 GMS, 2026년 5월 Mingledorff\'s를 인수해(전문 시공업자 대상 유통) 매출이 늘었다.</div>\n')
''']

# 1년 최저 종가 문장(2026-10-06 10/5 갱신 — '9월 29일 종가가 1년 최저'가 그 뒤 더 내려 틀렸다, Fable)
_hd_low = ("_lo = min(D[-253:], key=lambda r: r[4]); _today = _lo[0] == D[-1][0]; "
           "HD_LOW_TXT = '오늘 종가가 1년 최저다' if _today else f'1년 최저는 {int(_lo[0][5:7])}월 {int(_lo[0][8:])}일 종가 ${_lo[4]:.2f}다'; "
           "HD_LOW_PREM = f'오늘이 1년 최저(${px:.2f})다' if _today else f'1년 최저는 {int(_lo[0][5:7])}월 {int(_lo[0][8:])}일 종가 ${_lo[4]:.2f}다'")
PRE = [_hd_low]   # 2026-10-06 매일 재빌드: 1년 최저가 오늘이 아니어도 문장이 맞게(그전에는 그날 멈췄다)


# ── 자동 카드(설계 D, 2026-10-11) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose2·3 제안(손 표와 숫자 일치 — 여러 축·나머지 줄) ──
AUTO = True
SEG_MAP = {
 "parts": [
  {
   "concepts": [
    "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
   ],
   "axis": "us-gaap:StatementBusinessSegmentsAxis",
   "extra": {
    "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember",
    "srt:ProductOrServiceAxis": "hd:MajorProductLineBuildingMaterialsMember"
   },
   "members": {
    "hd:PrimarySegmentMember": [
     "건축 자재",
     "#f96302"
    ]
   }
  },
  {
   "concepts": [
    "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
   ],
   "axis": "srt:ConsolidationItemsAxis",
   "extra": {
    "srt:ProductOrServiceAxis": "hd:MajorProductLineHardlinesMember",
    "us-gaap:StatementBusinessSegmentsAxis": "hd:PrimarySegmentMember"
   },
   "members": {
    "us-gaap:OperatingSegmentsMember": [
     "공구·원예 등(하드라인)",
     "#9b59b6"
    ]
   }
  },
  {
   "concepts": [
    "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
   ],
   "axis": "srt:ConsolidationItemsAxis",
   "extra": {
    "srt:ProductOrServiceAxis": "hd:MajorProductLineDcorMember",
    "us-gaap:StatementBusinessSegmentsAxis": "hd:PrimarySegmentMember"
   },
   "members": {
    "us-gaap:OperatingSegmentsMember": [
     "인테리어(데코)",
     "#ffb07a"
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
    "us-gaap:AllOtherSegmentsMember": [
     "기타(SRS·GMS 등)",
     "#94a3b8"
    ]
   }
  }
 ]
}
# 손 문구 블록 정리: 화면 구조 고침만 남기고 분기 문장·날짜 박힌 치환·손 데이터 블록은 뺐다(자동 카드는 못 찾으면 건너뜀)
POST = []
