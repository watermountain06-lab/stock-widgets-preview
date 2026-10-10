# TXN(텍사스 인스트루먼트) v2 카드 설정 — fill.py TXN. 회계연도 12월 31일(Q2 2026 = 2026-04-01~06-30). 시총 49위(루트 카드 있음).
# 틀 시절 카드(2026-10-01 루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G3).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-24), 실적 보도자료(Q3 2025~Q2 2026), 8-K(의장 교체 10/16, Silicon Labs 2/4, CFO 6/2, 배당 9/17), StockAnalysis(2026-10-01).
# 엔진: 이자비용은 InterestAndDebtExpense로만 내 build_fundamental_score가 10-Q 손입력 값을 쓴다.
# 재현 모드: python3 v2/newcards/build.py TXN --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-30).
BUILD = {}
CIK = '0000097476'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 5463, 'op': 2310, 'ni': 1980, 'ocf': 2703, 'cap': 514}   # Q2 2026 보도자료·10-Q(백만 달러)
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'TI'
S_ = 'https://www.sec.gov/Archives/edgar/data/97476/'
SEC = S_
PR = {'q2': S_ + '000009747626000148/q22026txnex99-eredgar.htm', 'q1': S_ + '000009747626000097/q12026txnex99-eredgar.htm',
      'q4': S_ + '000009747626000003/q42025txnex99-eredgar.htm', 'q3': S_ + '000009747625000056/q32025txnex99-eredgarversi.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000009747626000152/txn-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'div': S_ + '000095010326014118/dp253473_ex99.htm', 'cfo': S_ + '000095010326008325/dp247795_8k.htm',
         'slab': S_ + '000119312526036727/d100130dex991.htm', 'chair': S_ + '000095010325013275/dp235861_ex99.htm'}
FAIRBAND_TITLE = 'id="txnFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (마진 100%로도 불가)</span>'
OPM_RANGE, Y2 = (25, 50), (25, 50)
FCF_SUB = '영업현금흐름 − 설비투자 · 회사 FCF $2.74B는 CHIPS법 보조금 $0.55B 포함'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('R&amp;D (Q2 2026)', '$0.54B', '연구개발 · 매출의 9.8%')
NEXT = ('10월 하순 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('10월 하순', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('차입금은 회사채 $14.1B(1년 안 만기 $1.15B)이고 현금 $3.66B·단기 투자 $3.34B가 있다. '
               '이자보상배율 {FUND_IC:.1f}배는 10-Q의 2분기 이자비용 $141M 기준이다(회사가 표준과 다른 항목명으로 공시해 10-Q 원문 값을 썼다). '
               'Silicon Labs 인수(기업가치 약 $7.5B, 현금)는 2027년 상반기 종결 예정이고, 현금과 차입($5B 지연 인출 대출 약정)으로 치른다.')
ACT_REASON = ''
YOY_EXTRA = '설비투자가 1년 새 ${r1(cap[yo])}B → ${r1(cap[cur])}B로 줄어 FCF가 커졌다 · '
SEG = [('아날로그', 4365, '#0f6eb4'), ('임베디드 프로세싱', 788, '#c8102e'), ('기타', 310, '#94a3b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별 매출'
SEG_NOTE = ('1년 전보다 아날로그 +26%, 임베디드 프로세싱 +16%, 기타 −2% · 부문 영업이익은 아날로그 $1.99B·임베디드 $0.17B · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Q2 2026 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (Q2 2026)', '$0.03B'),
           ('잔여 바이백 승인 한도 (2026.06.30 기준)', '$18.61B'),
           ('배당 (Q2 2026 지급)', '9월 발표: 10월 결의 시 $1.52', '$1.30B')]
CHECK_WHEN = '2026년 10월 하순 (예상) · Q3 2026'
CHECK = ['3분기 전망 — 매출 $5.65~6.15B, EPS $2.23~2.57',
         '산업·데이터센터·자동차 수요 회복이 이어지는지(2분기 매출 +23%)',
         '설비투자 감소(2분기 ${r1(cap[cur])}B)와 CHIPS법 보조금으로 늘어난 FCF',
         'Silicon Labs 인수 승인 진행(2027년 상반기 종결 예정)과 인수 차입']
NONOP_WHAT = '지분·장기투자'
PH = ['QCOM', 'INTC', 'AVGO', 'NVDA', 'MU', 'AMAT']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '반도체 6곳 PER 비교 (점수는 IT 카드 유니버스 기준)', 'pbr': '반도체 PBR 비교', 'psr': '반도체 PSR 비교',
                'pcr': '반도체 PCR(FCF) 비교', 'evebitda': '반도체 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-24 공시)'
PREMISE = ('주가가 1년 새 {CH_TXT} 올라 PER {SM[\'PER\'][\'current\']:.1f}배·PSR·PBR·EV/EBITDA가 5년 중 상위 {math.ceil(100 - min(SM[\'PER\'][\'percentile\'], SM[\'PSR\'][\'percentile\'], SM[\'PBR\'][\'percentile\'], SM[\'EV/EBITDA\'][\'percentile\']))}% 안이라 자기 이력 {selfsc:.1f}점이다'
           '(PCR {SM[\'PCR\'][\'current\']:.1f}배만 중간). 카드 유니버스 IT 안에서는 {peersc:.1f}점으로 중간이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {sgn(VOTES[0])}·{sgn(VOTES[1])}·{sgn(VOTES[2])}{jo_ro(VOTES[2])} 합계 {TOTAL_TXT} “{VERDICT}”다. 매출이 2023~2024년 줄었다가 회복 중이라 '
        '5년 성장률이 연 {pct(HIST[\'growth_5y\'])}·3년 {pct(HIST[\'growth_3y\'])}뿐이고, 영업이익률을 100%로 올려도 현재가에 닿지 않는다'
        '(일정 성장이면 5년 내내 연 {pct(DCF[\'requiredGrowth\'])}). 세 시나리오 모두 성장률은 하한 2.5%로 같고(영업이익률과 매출/자본 가정이 다르다), '
        '보수 시나리오(${DCF[\'low\']:.0f})가 가장 높은 것은 5년 영업이익률 중앙값({pct(HIST[\'margin_5y\'])})이 최근 2년({pct(HIST[\'margin_2y\'])})보다 높아서다.')
FUND_TIP = ('매출·영업이익 3년 CAGR(연간 FY2022→FY2025 기준)이 음수(1점)인 것은 2022년 정점 뒤 2023~2024년 매출이 줄었기 때문이다'
            '(내재가치 탭의 3년 성장률은 분기 TTM 기준이라 값이 다르다). 이자보상배율은 10-Q 이자비용 손입력 값이다.')
SELF_TIP = 'PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PSR·PBR·EV/EBITDA가 5년 중 비싼 쪽이다. PCR은 설비투자가 줄어 FCF가 커지면서 중간이다.'
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['성장률이 영구성장률 2.5%보다 낮아(5년 연 {pct(HIST[\'growth_5y\'])}·3년 {pct(HIST[\'growth_3y\'])}, 분기 TTM 기준) 5년 내내 2.5%로 두고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '성장률은 같은 이유로 5년 내내 2.5%, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '성장률은 같은 이유로 5년 내내 2.5%, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 17일 장 마감 후 — 배당 7% 인상 예정', '2026-09-18',
     '분기 배당을 $1.42에서 $1.52로 올릴 예정(10월 이사회 결의 조건, 23년 연속 인상)', 'div', 'TI 공시 (SEC 8-K)'),
    ('', '2026년 7월 22일 장 마감 후 — Q2 2026 실적', '2026-07-23',
     '매출 $5.46B(+23%)·EPS $2.14 · 3분기 매출 전망 $5.65~6.15B', 'q2', 'TI 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 6월 2일 장 마감 후 — CFO 교체', '2026-06-03',
     '라파엘 리자르디 CFO가 은퇴하고 줄리 넥트가 8월 1일 맡는다', 'cfo', 'TI 공시 (SEC 8-K)'),
    ('', '2026년 4월 22일 장 마감 후 — Q1 2026 실적', '2026-04-23',
     '매출 $4.83B(+19%)·EPS $1.68 · 산업·데이터센터가 성장을 이끎', 'q1', 'TI 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 2월 4일 개장 전 — Silicon Labs 인수 발표', '2026-02-04',
     '주당 $231 현금, 기업가치 약 $7.5B · 종결 뒤 3년 안 연 약 $450M 비용 절감 목표 · 2027년 상반기 종결 예정', 'slab', 'TI·Silicon Labs 공동 보도자료 (SEC 8-K)'),
    ('', '2026년 1월 27일 장 마감 후 — Q4 2025 실적', '2026-01-28',
     '매출 $4.42B(+10%)·EPS $1.27', 'q4', 'TI 실적 보도자료 (SEC 8-K)'),
    ('', '2025년 10월 21일 장 마감 후 — Q3 2025 실적', '2025-10-22',
     '매출 $4.74B(+14%)·EPS $1.48', 'q3', 'TI 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 16일 장 마감 후 — 이사회 의장 교체', '2025-10-17',
     '하비브 일란 CEO가 이사회 의장을 겸하고 리치 템플턴 의장은 은퇴한다', 'chair', 'TI 공시 (SEC 8-K)'),
]
SUMMARY = ('아날로그 반도체 수요 회복으로 2분기 매출이 23% 늘고 Silicon Labs 인수를 추진, 주가는 1년 새 {CH_TXT}', '회복기·높은 배수',
           ['2분기 매출 $5.46B(+23%), 영업이익 $2.31B(+48%), EPS $2.14(+52%)였고 산업·데이터센터·자동차가 성장을 이끌었다.',
            '설비투자가 줄고 CHIPS법 보조금이 들어와 최근 4분기 회사 FCF(보조금 포함)가 $6.5B(1년 전 $1.8B)로 늘었다.',
            '2월 Silicon Labs를 약 $7.5B(현금)에 사기로 했고, 9월에 배당을 7% 올리겠다고 밝혔다(10월 이사회 결의 조건).'],
           '실적은 회복 중이지만 PER·PSR·EV/EBITDA가 5년 중 비싼 쪽이고, 5년 성장률이 연 {pct(HIST[\'growth_5y\'])}라 현금흐름 모델로는 현재가의 {DCF[\'base\'] / px * 100:.0f}%만 설명된다.',
           'Q3 2026 실적(10월 하순 예상)의 매출 $5.65~6.15B 전망 달성과 회복 지속 여부.')
BULL = [('회복', '2분기 매출 +23%, 영업이익 +48%, 3분기 전망도 전 분기보다 높다.'),
        ('현금', '최근 4분기 회사 FCF $6.5B(CHIPS법 보조금 포함, 카드 PCR은 보조금을 뺀 영업현금 − 설비투자 기준).'),
        ('환원', '배당 23년 연속 인상 예정(분기 $1.42 → $1.52), 자사주 한도 $18.6B.')]
BEAR = [('밸류', 'PER {SM[\'PER\'][\'current\']:.0f}배 — 5년 중앙값 {SM[\'PER\'][\'median\']:.0f}배, 현금흐름 기본 ${DCF[\'base\']:.0f}.'),
        ('성장', '5년 매출 성장 연 {pct(HIST[\'growth_5y\'])} — 2023~2024년 감소 뒤 회복 중.'),
        ('인수', 'Silicon Labs 인수 $7.5B를 현금·차입으로 치른다(종결 2027년 상반기 예정).')]
ANALYST = {'rating': 'Buy', 'n': 36, 'nt': 25, 'mean': 324.08, 'median': 330, 'low': 220, 'high': 405, 'sb': 17, 'b': 3, 'h': 14, 's': 0, 'ss': 2}
ANALYST_ASOF = '2026-10-06'
PRE = [r'''
FUND_IC = [r_['value'] for r_ in FUND['axes']['health']['rows'] if r_['metric'] == 'interestCoverage'][0]   # 손입력 이자비용 기준 이자보상배율
''']

# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
POST = [r'''
# 시나리오 순서 설명(보수가 가장 높다) — 옛 카드의 별도 노트
one('<div class="note" data-dcf-nonop hidden></div>\n', '<div class="note" data-dcf-nonop hidden></div>\n'
    + F('    <div class="note">보수 시나리오(${DCF[\'low\']:.0f})가 기본(${DCF[\'base\']:.0f})·낙관(${DCF[\'high\']:.0f})보다 높다. 보수는 5년 영업이익률 중앙값({pct(HIST[\'margin_5y\'])}), 기본은 최근 2년 중앙값({pct(HIST[\'margin_2y\'])})으로 가는데 5년 쪽이 더 높기 때문이다.</div>\n'))
# 역산 문장: 5년 성장률이 영구성장률 2.5%보다 낮아 모델이 하한을 쓴다 — "지난 5년 속도로 크다가 식는"이 아니라 하한 문구(옛 카드)
one("매출이 지난 5년 속도(연 ${f1(d.growth5y)})로 크다가 식는 동안`", "매출이 연 2.5%(5년 성장률 연 ${f1(d.growth5y)}이 영구성장률보다 낮아 하한 적용)로 5년 내내 크는 동안`")
one("매출이 지난 5년 속도(연 ${pc(D.growth5y)})로 크다가 식는 동안`", "매출이 연 2.5%(5년 성장률 연 ${pc(D.growth5y)}이 영구성장률보다 낮아 하한 적용)로 5년 내내 크는 동안`")
''']


# ── 자동 카드(설계 D, 2026-10-10) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose.py 제안(손 표와 숫자 일치) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {
  "txn:AnalogSegmentMember": [
   "아날로그",
   "#0f6eb4"
  ],
  "txn:EmbeddedProcessingSegmentMember": [
   "임베디드 프로세싱",
   "#c8102e"
  ],
  "us-gaap:AllOtherSegmentsMember": [
   "기타",
   "#94a3b8"
  ]
 },
 "ignore": []
}
POST = [r'''
# 역산 문장: 5년 성장률이 영구성장률 2.5%보다 낮으면 모델이 하한을 쓴다 — 그때만 하한 문구로(자동 카드: 조건부)
if (HIST.get('growth_5y') or 0) < 0.025:
    one("매출이 지난 5년 속도(연 ${f1(d.growth5y)})로 크다가 식는 동안`", "매출이 연 2.5%(5년 성장률 연 ${f1(d.growth5y)}이 영구성장률보다 낮아 하한 적용)로 5년 내내 크는 동안`")
    one("매출이 지난 5년 속도(연 ${pc(D.growth5y)})로 크다가 식는 동안`", "매출이 연 2.5%(5년 성장률 연 ${pc(D.growth5y)}이 영구성장률보다 낮아 하한 적용)로 5년 내내 크는 동안`")
''']   # 손 문구 블록 정리: 구조 표시만 남기고 분기 문장·날짜 박힌 치환은 뺐다
