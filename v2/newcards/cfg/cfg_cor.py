# COR(센코라) v2 카드 설정 — 자동 카드(AUTO). 회계연도 9월 30일(FY26 = 2025-10 ~ 2026-09). 카드 순위 167(시총 166위). 의약품 도매 유통(미국·해외), 동물 의약품(MWI), 전문 진료 관리(MSO).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-08-05 장 마감 뒤), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 보도자료는 장 전, 8-K는 장중 접수), 8-K(OneOncology 12/15, MWI·Covetrus 2/18, 전망·AON 인수 10/21), StockAnalysis.
# 엔진 입력(2026-10-22): 감가상각 = 손익계산서 Depreciation(DepreciationNonproduction) + Amortization(AmortizationOfIntangibleAssets) — 합산 태그가 22개뿐이라 EV/EBITDA 이력이 55일이었다(DDA_PARTS_BY_CIK).
# 차입금 = 단기 279 + 장기 11,444 = $11,723M(DEBT_TOTAL_TAG — 내재가치 입력이 장기만 잡았다). 소송 충당 부채 장기 $3.77B + 유동 $396M ≈ $4.2B(오피오이드 합의 — 분할 지급)는 차입금에 넣지 않았다(엔진 규칙, 문장으로 밝힘).
# 매각 예정 자산 $3.84B(MWI 동물 의약품 — Covetrus와 합병 예정, 미완료). 4분기 EPS FY25 보도자료 값.
CIK = '0001140859'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-09-30', '2024-09-30'), 'FY25'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Cencora'
S_ = 'https://www.sec.gov/Archives/edgar/data/1140859/'
SEC = S_
TENQ = S_ + '000114085926000034/cor-20260630.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000114085926000032/exhibit991-q32026.htm', 'q2': S_ + '000114085926000018/exhibit991-q22026.htm',
      'q1': S_ + '000114085926000004/exhibit991-q12026.htm', 'q4': S_ + '000114085925000128/exhibit991-q42025.htm'}
LINKS = {'onco': S_ + '000110465925120852/tm2533461d1_ex99-1.htm', 'mwi': S_ + '000110465926016785/tm266695d1_ex99-1.htm',
         'wag': S_ + '000110465926094676/tm2622984d1_8k.htm', 'aon': S_ + '000110465926117576/tm2627778d1_ex99-1.htm'}
FAIRBAND_TITLE = 'id="corFairBand" title="최근 1년 PER 25~75% 구간 × 최근 4분기 희석 EPS. 순이익률이 2% 미만이라 PER은 점수에서 빠진다 — 이 범위는 참고용이다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-0.5, 2)
ACT_REASON = ''
NONOP_WHAT = '투자'
YOY_NOTE = {'2026-06-30': '최근 4분기 순이익에는 Q2 FY26 OneOncology 지분 재평가 이익 $1.1B가 들어 있고, Q4 FY25는 적자(희석 EPS −$1.75)였다'}
# 고정 문장(숫자 없음). 도매 유통의 얇은 마진, PER 제외, 소송 부채, 진행 중 거래.
MODEL_NOTE = ('의약품 도매는 매출이 매우 크고 이익률이 1% 안팎이라, 순이익률 2% 미만이면 PER을 빼는 카드 규칙에 걸려 PER이 점수에서 빠진다. 같은 이유로 작은 이익률 가정 차이가 '
              '현금흐름 내재가치를 크게 흔든다. 또 MWI 동물 의약품 사업을 매각 예정 자산(유동)으로 옮기면서 영업권 등 비유동 자산이 운전자본에 들어가, 모델이 그만큼을 재투자로 본다 — 0 이하 결과의 일부는 이 재분류 때문이다(빼도 기본 시나리오는 0 이하). '
              '오피오이드 소송 합의금으로 남은 분할 지급 부채는 차입금에 넣지 않았다. MWI의 기존 실적·자산은 숫자에 있고, Covetrus 합병 완료 효과와 새 인수(AON)는 아직 없다.')   # Codex r1 필수
PH = ['MCK', 'CAH', 'HSIC', 'UNH', 'CVS', 'CI']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '의약품 유통·의료 서비스 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(COR 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·의료기기·보험·서비스가 섞여 있어 이익률이 아주 낮은 도매 유통은 PSR이 늘 낮게 나온다. 차트에는 유통·의료 서비스 6곳만 보인다.')
# 매출(Q3 FY26 10-Q 부문) — 미국 헬스케어 74,860.8 + 해외 7,680.5 + 동물 의약품 1,519.8 + 기타 비전략 733.5 = 84,794.6, 부문 간 제거 −39.6 → 84,755. 1년 전 71,342.9·7,253.4·1,471.7·635.8.
SEG = [('미국 헬스케어 솔루션', 74860.8, '#461e7d'), ('해외 헬스케어 솔루션', 7680.5, '#8a63c2')]
SEG_ADJ = 2213.7   # 동물 의약품 1,519.8 + 기타 비전략 733.5 − 부문 간 제거 39.6(보고 부문 밖 — 본사 소관으로 공시)
SEG_TITLE = '매출 구성 — 부문별'
SEG_ADJ_LABEL = '동물 의약품·기타(보고 부문 밖)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS는 쓰지 않는다; 5/6 급락의 1차 자료상 원인인 매출 성장 전망 하향은 BSX 선례대로 적는다), 거래 3건.
# 반응일: 실적 보도자료는 장 전 배포, 8-K 접수 UTC 2025-11-05T16:33Z·2026-02-04T16:31Z·05-06T14:32Z·08-05T14:32Z = 장중 → 같은 날.
# OneOncology 8-K 2025-12-15T17:00Z → 12/15. MWI·Covetrus 8-K 2026-02-18T17:34Z → 2/18. AON·전망 8-K 2026-10-21T15:48Z → 10/21.
# Walgreens 8-K 2026-08-12T20:38Z(동부 16:38, 장 마감 뒤) → 8/13(Fable r1 필수).
# 넣지 않은 8-K: 채권 발행(2/10~2/13), 신용 약정(1/16·8/5), 임원·이사(1/22·3/17·5/29·6/15·8/14·9/25), 주총(3/6), EyeSouth 인수(3/23 — 작은 MSO 인수).
NEWS_RANGE = '2025.11 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 21일 — AON 인수 합의 · FY26 전망 상향', '2026-10-21',
     '종양 진료 네트워크 American Oncology Network 인수 합의(미완료) · FY26 결산 확정 전 조정 EPS 전망을 높임', 'aon', 'Cencora 보도자료 (SEC 8-K)'),
    ('red', '2026년 8월 12일 — Walgreens 일부 물량 이탈 공시', '2026-08-13',
     '7월 1일부터 주력 공급 계약 밖의 Walgreens 일부 물량이 다른 곳으로 옮겨 감(주력 계약은 그대로, 8/5 4분기 전망에 이미 반영) — 8-K는 장 마감 뒤라 반응은 다음 거래일(8/13) 기준, 8/12의 −5.9% 하락은 공시 전', 'wag', 'Cencora 공시 (SEC 8-K 7.01항)'),
    ('green', '2026년 8월 5일 — Q3 FY26 실적', '2026-08-05',
     '매출 $84.8B(+5.1%) · 희석 EPS $3.94(1년 전 $3.52)', 'q3', 'Cencora 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 6일 — Q2 FY26 실적', '2026-05-06',
     '매출 $78.4B(+3.8%) · 희석 EPS $8.40(OneOncology 재평가 이익 $1.1B 포함, 1년 전 $3.68) · FY26 매출 성장 전망 7~9% → 4~6%로 낮춤 · 공시된 악재: 일부 브랜드 의약품 제조사 가격 하락, 대형 우편 주문 고객 매출 감소, 2025년 종양·식료품 고객 이탈', 'q2', 'Cencora 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 18일 — MWI 동물 의약품, Covetrus와 합병 합의', '2026-02-18',
     'MWI를 Covetrus와 합쳐 현금 $1.25B·우선 지분 $800M을 받고 합병 회사 보통주 34.3%를 유지(미완료)', 'mwi', 'Cencora 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 4일 — Q1 FY26 실적', '2026-02-04',
     '매출 $85.9B(+5.5%) · 희석 EPS $2.87(1년 전 $2.50) · 해외 부문 영업이익 −13.9%(유럽 유통) · 미국 컨설팅 사업 자산 손상 $249.5M · OneOncology 인수 완료', 'q1', 'Cencora 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 15일 — OneOncology 경영권 인수 합의', '2025-12-15',
     'TPG가 가진 OneOncology 지분 대부분을 사들이기로 합의(종양 진료 관리 플랫폼) — 2026년 2월 완료', 'onco', 'Cencora 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 5일 — Q4 FY25 실적', '2025-11-05',
     '매출 $83.7B(+5.9%) · 희석 EPS −$1.75(PharmaLex 영업권 손상 $723.9M) · FY2025 매출 $321.3B(+9.3%)·희석 EPS $7.96', 'q4', 'Cencora 실적 보도자료 (SEC 8-K)'),
]
BB_TAGS = ['PaymentsForRepurchaseOfEquity']   # 자사주 매입 현금 지급(9개월 $1,000.1M) — 기본 태그가 없다(Codex r1)
# 다음 실적일: 10/21 보도자료 — 11/4 FY26 4분기 실적 콜(Codex r1 필수)
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-11-04', 'src': '10/21 회사 보도자료 — FY26 4분기 실적 콜 11월 4일'}
ANALYST = {'rating': 'Buy', 'n': 14, 'nt': 13, 'mean': 370.69, 'median': 375, 'low': 330, 'high': 400, 'sb': 7, 'b': 3, 'h': 4, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'

# ── 자동 카드 — 보고 부문 2개(동물 의약품·기타는 본사 소관 축이라 SEG_ADJ). 원문 대조: Q3 FY26 74,860.8/7,680.5, 1년 전 71,342.9/7,253.4(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:Revenues"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "cor:USHealthcareSolutionsMember": [
   "미국 헬스케어 솔루션",
   "#461e7d"
  ],
  "cor:InternationalHealthcareSolutionsMember": [
   "해외 헬스케어 솔루션",
   "#8a63c2"
  ]
 },
 "ignore": []
}
