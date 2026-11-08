# FIS(피델리티 내셔널 인포메이션 서비시스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 은행·자본시장 금융 소프트웨어·결제 처리 — 부문 Banking·Capital Markets·Corporate and Other.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-04 16:15 동부 장 마감 뒤 → 첫 세션 11-05), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 모두 07시대 장 전 → 같은 날). 사전 조사 scratchpad pre/FIS.md.
# 큰 사건: 2026-01-09 Global Payments의 Issuer Solutions 인수(대가 $13,473M = 현금 $7,695M + Worldpay 지분 $5,762M + 주식)와 Worldpay 지분 45% 전량 매각을 함께 마감 — 매각 이익 세전 약 $2,200M(세후 $2,206M, 주당 약 4.27)이 지분법 줄에 있다.
# 차입 $20,769M = 기업어음 $3,904M + 장기 $16,865M(2026-03 채권 발행으로 인수 대출 상환), 현금 $740M.
CIK = '0001136893'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'FIS'
S_ = 'https://www.sec.gov/Archives/edgar/data/1136893/'
SEC = S_
TENQ = S_ + '000113689326000063/fis-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000113689326000061/q32026ex991.htm', 'q2': S_ + '000113689326000046/q22026ex991.htm',
      'q1': S_ + '000113689326000038/q12026ex991.htm', 'q4': S_ + '000113689326000009/q42025ex991.htm'}
LINKS = {'tenq': S_ + '000113689326000063/fis-20260930.htm', 'deal': S_ + '000119312526009759/d947945d8k.htm'}
FAIRBAND_TITLE = 'id="fisFairBand" title="최근 4분기 EPS에 Worldpay 지분 매각 이익(주당 약 4.27)이 들어 있어 PER 구간으로 낸 적정주가가 부풀므로 표시하지 않는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
GROWTH_SPAN = 'Worldpay 지분 매각(2024-01) 뒤 이력(2024-06 이후)'   # 역산 설명의 '지난 5년' 자리 — build_dcf.HISTORY_WINDOW와 짝
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('2026년 1분기 이익의 대부분은 Worldpay 지분 매각 이익(세후 $2.2B)이다. 그래서 최근 4분기 EPS가 실제 영업보다 크게 나오고 PER이 낮아 보인다. '
              '2026년 1월 Global Payments의 카드 발급 처리 사업(Issuer Solutions)을 인수해 1년 전보다 매출이 크게 늘었다(3분기 Banking 부문 +41%, 인수 제외 +4%). '
              '현금흐름 모델은 Worldpay 매각(2024-01) 뒤 이력만 쓰고, 그 매출 성장률에는 Issuer Solutions 인수 매출이 들어 있다(회사 유기 성장 3~4%) — 투하자본 대비 수익률(약 4.6%)이 모델 할인율(10%)보다 낮아 성장이 빠를수록 가치가 더 낮게 나온다. 설비투자에는 자본화 소프트웨어(9개월 $657M)가 들어 있지 않다(엔진 공통 정의) — 현금흐름 모델의 재투자는 인수 대금 $7.9B 때문에 크게 잡힌다. Banking 부문 영업권은 공정가치 여유가 약 7%뿐이라 4분기 연례 점검에서 손상 위험이 있다고 회사가 밝혔다. 비교 종목은 S&P500 결제·거래소·금융 데이터 18곳 중 FIS를 뺀 17곳이다.')
PRE = ['FB = None']
PH = ['FISV', 'GPN', 'JKHY', 'PYPL', 'V', 'MA']
PEER_FILE = 'peer_universe/payments_exchanges.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '결제 처리 6곳 PER 비교 (점수는 S&P500 결제·거래소·금융 데이터 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 결제·거래소·금융 데이터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 결제·거래소·금융 데이터 대비 배수 순위 (v2/peer_universe/payments_exchanges.json)'
PEER_TIP = ('S&P500 결제 처리·거래소·금융 데이터 18곳 중 FIS를 뺀 17곳과 배수 순위를 매긴 값이다.',
            '카드 네트워크·결제 처리·거래소·신용평가가 섞여 있어 성장·마진 구조가 다르다. 차트에는 결제 처리 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 표) — Banking 2,548 + Capital Markets 823 + Corporate and Other 83 = 3,454.
SEG = [('Banking(은행 솔루션)', 2548, '#4bcd3e'), ('Capital Markets(자본시장)', 823, '#015b7e'), ('기타', 83, '#a5d6e3')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: Q3 2026 실적은 가이던스 하향·CFO 사임과 함께 발표돼 손 항목으로 쓴다(자동 항목은 빠진다). 반응일: 모두 장 전 → 같은 날.
NEWS_RANGE = '2026.01 ~ 2026.11'
NEWS = [
    ('red', '2026년 11월 4일 장 마감 뒤 — CFO 사임(10-Q 공시)', None,
     'James Kehoe CFO가 11월 5일 물러나고 Alexandra Brooks(최고회계책임자)가 임시 CFO를 맡는다 — 별도 8-K 없이 3분기 10-Q 5항으로 공시', 'tenq', 'FIS 10-Q (SEC)'),
    ('red', '2026년 11월 4일 장 전 — Q3 2026 실적·전망 하향', '2026-11-04',
     '매출 $3.45B(+27%, Issuer Solutions 인수 포함) · 희석 EPS $0.69(1년 전 $0.50) · 조정 EPS $1.61 · 2026년 조정 EPS 전망 $5.82~5.89로 낮춤 — 당일 주가 −23.7%', 'q3', 'FIS 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 8월 4일 장 전 — Q2 2026 실적', '2026-08-04',
     '매출 $3.38B · 희석 EPS $0.45(1년 전 −$0.90) · 조정 EPS $1.48 — 당일 주가 −1.2%', 'q2', 'FIS 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 8일 장 전 — Q1 2026 실적', '2026-05-08',
     '매출 $3.30B · 희석 EPS $4.58(1년 전 $0.15, Worldpay 지분 매각 이익 포함) · 조정 EPS $1.36 — 당일 주가 −8.0%', 'q1', 'FIS 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 24일 장 전 — Q4 2025 실적', '2026-02-24',
     '매출 $2.81B · 희석 EPS $0.98(1년 전 $0.52) · 조정 EPS $1.68 — 당일 주가 +1.4%', 'q4', 'FIS 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 12일 장 전 — Issuer Solutions 인수·Worldpay 지분 매각 마감', None,
     '1월 9일 Global Payments의 Issuer Solutions를 $13.5B(현금 $7.7B + Worldpay 지분)에 인수하고 Worldpay 지분 45%를 모두 넘김', 'deal', 'FIS 공시 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 29, 'nt': 20, 'mean': 37.2, 'median': 35, 'low': 30, 'high': 54, 'sb': 5, 'b': 2, 'h': 21, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


POST = [r"""
h = h.replace('<div class="stat-sub">영업현금흐름 − 설비투자</div>', '<div class="stat-sub">영업현금흐름 − 설비투자(자본화 소프트웨어 제외)</div>', 1)   # Codex r2
h = h.replace('</span> 종가 기준</span>', '</span> 장중 기준</span>', 1)   # 10-Q가 11-04 장 마감 뒤라 11-05 장중 가격으로 만들었다 — 매일 실행이 종가로 고친다(2026-11-05)
"""]


# ── 자동 카드 — 부문 지도는 seg_map_propose.py 1판(원문 대조 Q3 2026 2,548/823/83, 2026-11-05) ──
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
  "fis:BankingSolutionsMember": [
   "Banking(은행 솔루션)",
   "#4bcd3e"
  ],
  "fis:CapitalMarketSolutionsMember": [
   "Capital Markets(자본시장)",
   "#015b7e"
  ],
  "us-gaap:CorporateAndOtherMember": [
   "기타",
   "#a5d6e3"
  ]
 },
 "ignore": []
}
