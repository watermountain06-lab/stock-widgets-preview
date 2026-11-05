BUILD = {'overlay': True, 'no_dcf': '손해보험사라 현금흐름 모델을 쓰지 않는다'}   # CB·PGR과 같은 방식(2026-10-02 사용자 결정)
# L(로우스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 지주회사 — CNA(손해보험, 약 92%)·Boardwalk 파이프라인·Loews 호텔·본사.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-02 07:36 동부 장 전 → 같은 날), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 모두 06시대 장 전 → 같은 날). 사전 조사 scratchpad pre/L.md.
# 엔진 입력(2026-11-05): 차입 = 장기 $8,417M + 유동 $521M = $8,938M(연결, DEBT_TOTAL_TAG — 본사 차입은 $1.8B), 현금 Cash $505M, 단기투자 $5,715M은 대부분 CNA 보험 운용자산(일부 본사)이라 분류상 뺌.
# 순이익·자본은 Loews 귀속(비지배 $839M). 우선주 태그 경고(2014)는 발행 0이라 무해.
NO_DCF_SKEW = True   # 금융 카드 — 현금흐름 칸 쏠림 메모(A0) 없음
CIK = '0000060086'
OP_DISPLAY = (['IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest'], [(['InterestExpense'], 1)])   # 카드 표시용 영업이익 = 세전이익 + 이자비용(CB와 같음)
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, 0), '판정 보류'
CO = 'Loews'
S_ = 'https://www.sec.gov/Archives/edgar/data/60086/'
SEC = S_
TENQ = S_ + '000006008626000056/l-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000006008626000054/exhibit991-q32026.htm', 'q2': S_ + '000006008626000045/exhibit991-q22026.htm', 'q1': S_ + '000006008626000029/exhibit991-q12026.htm', 'q4': S_ + '000006008626000005/exhibit991-q42025.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="lFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (현금흐름 미적용)</span>'
Y2 = (0, 40)
ACT_REASON = '보험사라 재고·매출채권 회전으로 보는 활동성이 맞지 않는다'
NONOP_WHAT = '투자'
PH = ['CB', 'TRV', 'ALL', 'AIG', 'HIG', 'WRB']
PEER_FILE = 'peer_universe/insurers.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '보험 6곳 PER 비교 (점수는 S&P500 보험사 기준)', 'pbr': '보험 PBR 비교', 'psr': '보험 PSR 비교',
                'pcr': '보험 PCR(FCF) 비교', 'evebitda': '보험 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 보험사(손해·종합·생명)보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 보험사 대비 배수 순위 (v2/peer_universe/insurers.json)'
PEER_TIP = ('S&P500 손해·종합·생명보험 15곳(L 제외)과 배수 순위를 매긴 값이다.', '생명보험사는 장부가·매출 구조가 달라 PBR·PSR 비교가 거칠다. 차트에는 손해보험 6곳만 보인다.')
MODEL_NOTE = ('보험 자회사 CNA가 매출의 약 80%라 보험사 비교군에 넣었고, 현금흐름 내재가치는 계산하지 않아 판정 보류다(자기 이력·동종업 점수는 참고). 차입금 $8.9B은 자회사(CNA·Boardwalk·호텔) 차입까지 합친 연결 값이고 본사 차입은 $1.8B다 — 본사는 자회사 차입을 보증하지 않고, 본사 현금·투자자산은 $4.4B다. 단기투자 $5.7B(대부분 CNA 보험 운용자산, 일부 본사)는 현금에서 뺐다. CNA의 3분기 합산비율은 97.0%다.'
              'PCR이 5년 이력 위쪽인 것은 Boardwalk 설비투자가 늘고(9개월 $725M) 영업현금흐름이 줄었기 때문이다. 3분기에는 CNA 장기요양보험 연례 점검 비용이 들어 있다.')
SEG = [('CNA 손해보험', 3821, '#0c2340'), ('Boardwalk 파이프라인', 616, '#4f6d8f'), ('Loews 호텔', 250, '#a9bacd')]
SEG_ADJ = 72   # 본사(투자 수익 등)
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: Q3 2026 실적은 news_auto가 SEC 숫자로 붙인다. 반응일은 발표 시각 기준.
NEWS_RANGE = '2026.01 ~ 2026.11'
NEWS = [
    ('green', '2026년 8월 3일 장 전 — Q2 2026 실적', '2026-08-03',
     'Loews 순이익 $444M · 희석 EPS $2.16(1년 전 $1.87) — 당일 주가 +0.2%', 'q2', 'Loews 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 4일 장 전 — Q1 2026 실적', '2026-05-04',
     'Loews 순이익 $337M · 희석 EPS $1.63(1년 전 $1.74) — 당일 주가 −5.9%', 'q1', 'Loews 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 9일 장 전 — Q4 2025 실적', '2026-02-09',
     'Loews 순이익 $402M · 희석 EPS $1.94(1년 전 $0.86) — 당일 주가 −0.3%', 'q4', 'Loews 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 0, 'nt': 0, 'mean': 0, 'median': 0, 'low': 0, 'high': 0, 'sb': 0, 'b': 0, 'h': 0, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-04'


POST = [r"""
h = h.replace('순차입금(리스 포함) $', '순차입금(리스 포함, 보증 없는 자회사 차입 포함 — 본사는 순현금) $', 1)   # Codex r2 2026-11-05
h = h.replace('GAAP 영업이익 $', '영업이익(세전 + 이자 추정) $')
# 애널리스트 의견이 StockAnalysis에 집계되지 않는다(2026-11-05) — 자리표시 값이 'Hold 1명 · $0 · −100%'로 보이지 않게 두 칸을 한 줄로 바꾸고 JS를 막는다(Codex·Fable r1)
import re as _rel
h, _n = _rel.subn(r'<div class="op-cell">\s*<span class="op-label">애널리스트 <span data-an="n">.*?</div>\s*<div class="op-cell">\s*<span class="op-label">평균 목표주가.*?</div>',
                  '<div class="op-cell">\n        <span class="op-label">애널리스트 의견</span>\n        <span class="op-val">집계 없음 <span class="op-sub">StockAnalysis에 의견·목표가 자료가 없다</span></span>\n      </div>', h, count=1, flags=_rel.S)
assert _n == 1, '애널리스트 칸을 못 찾음'
h = h.replace("(function(){\n  const A = L_ANALYST,", "(function(){\n  if (!L_ANALYST.n) return;   // 의견 자료 없음\n  const A = L_ANALYST,", 1)   # 손익계산서에 영업이익 줄이 없다 — OP_DISPLAY 합성값(Codex r1 2026-11-05)
"""]


# ── 자동 카드 — 부문 지도(손 표와 일치, 2026-11-05) ──
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
  "l:CnaFinancialCorporationMember": [
   "CNA 손해보험",
   "#0c2340"
  ],
  "l:BoardwalkPipelinePartnersLpMember": [
   "Boardwalk 파이프라인",
   "#4f6d8f"
  ],
  "l:LoewsHotelsHoldingCorporationMember": [
   "Loews 호텔",
   "#a9bacd"
  ]
 },
 "ignore": []
}
