# NOC(노스럽 그러먼) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 155(시총 153위). 방산 — 항공(B-21 폭격기), 방어 시스템(미사일·탄약), 임무 시스템, 우주.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-20 장 마감 뒤 접수), 실적 보도자료(Q3 2025~Q3 2026, 8-K 2.02항 — 동부 오전 접수, 보도자료는 장 전), 8-K(CFO 교체 2025-11-06), StockAnalysis.
# 엔진 입력(2026-10-22): 차입금 $15,197M(1년 안 764 + 장기 14,433) · 현금 $3,744M · 운용리스 $2,202M(비유동) = 원문. 기본 태그 그대로.
# 세전이익이 영업이익보다 큰 것은 연금 비영업 이익(FAS 연금 이익·시가평가) 때문 — 현금흐름 모델은 영업이익 기준이라 연금 이익과 연금 순자산($3,447M − 부채 $1,076M)을 모두 넣지 않는다.
# 4분기 EPS 2023·2025 보도자료 값(2025 Q4에는 연금 시가평가 이익 세후 $394M).
BUILD = {}
CIK = '0001133421'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'Northrop Grumman'
S_ = 'https://www.sec.gov/Archives/edgar/data/1133421/'
SEC = S_
TENQ = S_ + '000113342126000038/noc-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000113342126000037/noc-09302026xearningsrelea.htm', 'q2': S_ + '000113342126000033/noc-06302026xearningsrelea.htm',
      'q1': S_ + '000113342126000015/noc-03312026xearningsrelea.htm', 'q4': S_ + '000113342126000002/noc-12312025xearningsrelea.htm'}
LINKS = {'q3_25': S_ + '000113342125000052/noc-09302025xearningsrelea.htm', 'cfo': S_ + '000162828025050297/noc-form8xk110325xex991.htm'}
FAIRBAND_TITLE = 'id="nocFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 최근 4분기 EPS에는 연금 시가평가 이익이 들어 있다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 연금 이익, 방산 계약 특성.
MODEL_NOTE = ('순이익과 EPS에는 비영업 연금 이익(연말 시가평가 포함)이 들어 있어, PER은 연금 이익을 뺀 순이익 기준보다 낮게 나온다. 현금흐름 모델은 영업이익(영업 연금 비용 조정 포함)에서 출발하므로 비영업 연금 이익은 반영하지 않고, 연금 순자산은 회수 제약과 세금 때문에 더하지 않았다. '   # Codex r1 필수
              '매출 대부분이 미국 정부 계약이라 국방 예산과 대형 사업(B-21 등)의 손익 조정에 따라 분기 이익이 흔들린다.')
PH = ['LMT', 'GD', 'RTX', 'LHX', 'HII', 'TDG']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '방산 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(NOC 제외)와 배수 순위를 매긴 값이다.',
            '기계·운송·서비스·건설이 섞여 있다. 차트에는 방산 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문, 부문 간 거래 포함) — 항공 3,575 + 임무 3,155 + 우주 2,749 + 방어 2,307 = 11,786, 부문 간 거래 −664 → 연결 11,122. 1년 전 3,142/3,093/2,698/2,059.
SEG = [('항공(Aeronautics)', 3575.0, '#00274c'), ('임무 시스템', 3155.0, '#4f6f99'), ('우주', 2749.0, '#8fa9cc'), ('방어 시스템', 2307.0, '#c0392b')]
SEG_ADJ = -664.0
SEG_TITLE = '매출 구성 — 부문별(부문 간 거래 포함)'
SEG_ADJ_LABEL = '부문 간 거래'
# 손 뉴스: 최신 실적(Q3 2026, 10/20)은 news_auto. 가이던스·MTM 조정 EPS는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K 2025-10-21T14:29Z·2026-01-27T16:44Z·04-21T14:44Z·07-21T14:45Z = 장중 접수(보도자료 장 전) → 같은 날.
# CFO 교체 8-K 2025-11-07T03:04Z = 11/6 22:04 → 보도자료 11/6자 — 반응일 11/7. 넣지 않은 8-K: 이사 선임(2/13), 주총(5/21), 임원(8/21).
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('red', '2026년 7월 21일 — Q2 2026 실적', '2026-07-21',
     '매출 $10.9B(+5%) · 희석 EPS $7.68(1년 전 $8.15 — 교육 서비스 사업 매각 이익 $1.04 포함) · GEM 63XL 로켓 모터 비용 증가 등 불리한 추정 조정 · 수주잔고 사상 최대', 'q2', 'Northrop Grumman 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 21일 — Q1 2026 실적', '2026-04-21',
     '매출 $9.9B(+4%) · 희석 EPS $6.14(1년 전 $3.32 — B-21 폭격기 손실 충당 $477M 반영 분기)', 'q1', 'Northrop Grumman 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 27일 — Q4 2025 실적', '2026-01-27',
     '매출 $11.7B(+10%) · 희석 EPS $9.99 — 연금 시가평가 이익 세후 $394M 포함 · 2025년 매출 $42.0B(+2%)·EPS $29.08', 'q4', 'Northrop Grumman 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 6일 장 마감 뒤 — CFO 교체', '2025-11-07',
     'John Greene이 2026년 1월 7일 CFO로 취임하고 Ken Crews는 2월 회사를 떠난다', 'cfo', 'Northrop Grumman 공시 (SEC 8-K)'),
    ('neutral', '2025년 10월 21일 — Q3 2025 실적', '2025-10-21',
     '매출 $10.4B(+4%) · 희석 EPS $7.67(1년 전 $7.00) · 2025년 EPS 전망 상향', 'q3_25', 'Northrop Grumman 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 26, 'nt': 19, 'mean': 634.42, 'median': 640, 'low': 430, 'high': 815, 'sb': 11, 'b': 3, 'h': 11, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-22'


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(부문 4개, 부문 간 거래 포함 총액 — 차감은 SEG_ADJ, TMO와 같은 처리). 원문 대조: Q3 2026 3,575/3,155/2,749/2,307, 1년 전 3,142/3,093/2,698/2,059(2026-10-22) ──
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
  "noc:AeronauticsSystemsMember": [
   "항공(Aeronautics)",
   "#00274c"
  ],
  "noc:MissionSystemsMember": [
   "임무 시스템",
   "#4f6f99"
  ],
  "noc:SpaceSystemsMember": [
   "우주",
   "#8fa9cc"
  ],
  "noc:DefenseSystemsMember": [
   "방어 시스템",
   "#c0392b"
  ]
 },
 "ignore": []
}
