# DELL(델 테크놀로지스) v2 카드 설정 — fill.py DELL. 회계연도 1월 말·2월 초 금요일(Q2 FY27 = 2026-05-02~07-31). 시총 루트 카드 있음.
# 틀 시절 카드(루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G4).
# 출처: SEC XBRL, Q2 FY2027 10-Q(2026-09-08), 실적 보도자료(Q3 FY26~Q2 FY27), 8-K(애널리스트 미팅 10/7, 텍사스 이전 7/1, 사채 9/15), StockAnalysis(2026-10-01).
# 분사 종목(2021-11 VMware, RESTATED_LATEST — GE 방식): 자기 이력 창은 2022-03-24부터(SELF_SPAN). 자본 음수라 PBR 없음.
# 금융 자회사 DFS 빚은 차입금에 넣는다(2026-10-01 결정). 재현 모드: python3 v2/newcards/build.py DELL --from-card.
BUILD = {'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # 분사 종목 — 계속사업 희석 EPS 우선(카드 EPS 파일과 같다; 기본 태그만 쓰면 2022년 세 분기가 빠져 자기 이력 PER이 달라진다, D66 회귀 기록)
CIK = '0001571996'
CUR, YO, QO = '2026-07-31', '2025-08-01', '2026-05-01'
QLABEL, YL, QQL = 'Q2 FY27', 'Q2 FY26', 'Q1 FY27'
L8 = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27', 'Q2 FY27']
RELEASE = {'rev': 46971, 'op': 5385, 'ni': 4133}   # Q2 FY27 손익(백만 달러) — 옛 카드 YoY 막대 $46.97B·$5.38B·$4.13B와 같다
VOTES, VERDICT = (-1, 1, -2), '적정~고평가'
CO = 'Dell Technologies'
S_ = 'https://www.sec.gov/Archives/edgar/data/1571996/'
SEC = S_
PR = {'q2': S_ + '000157199626000039/exhibit991earnings8kq2fy27.htm', 'q1': S_ + '000157199626000021/exhibit991earnings8kq1fy27.htm',
      'q4': S_ + '000157199626000003/exhibit991earnings8kq4fy26.htm', 'q3': S_ + '000157199625000118/exhibit991earnings8kq3fy26.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000157199626000046/dell-20260731.htm'; TENQ_NAME = 'Q2 FY2027 10-Q'
LINKS = {'notes': S_ + '000119312526391976/d172674d8k.htm', 'texas': S_ + '000157199626000036/dell-20260625.htm',
         'analyst': S_ + '000119312525232662/d55706dex992.htm'}
FAIRBAND_TITLE = ('id="dellFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm:.1f}. '
                  '1년 전 시점의 최근 4분기 EPS는 $6.86이었다(약 {eps_ttm / 6.86:.1f}배로 늘어 PER 구간이 넓다)."')
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (0, 15), (0, 15)
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('R&amp;D (Q2 FY27)', '$1.11B', '매출의 2.4%')
NEXT = ('11월 하순 예상', '일정 · Q3 FY27 (회사 미확정)'); NEXT_OP = ('11월 하순', 'Q3 FY27 예상')
FY_ENDS, FY_LABEL = ('2026-01-30', '2025-01-31'), 'FY2026'
HEALTH_NOTE = ('유동비율 96.2%, 재고($21.3B, 연초 $10.4B의 약 2배)를 뺀 당좌비율 70.8%다. 차입금은 $34.5B(단기 $8.5B + 장기 $26.0B, 그중 금융 자회사 DFS 빚 $9.6B — '
               '회사가 DFS에 배분한 몫까지 더한 DFS 관련 부채는 $20.7B)이고 현금은 $11.6B다. 자본은 누적 자사주($20.0B)를 빼고 −$1.4B라 PBR·부채비율은 계산되지 않는다. '
               '분기 뒤 9월 15일에 사채 $5.0B를 더 발행했다.')
ACT_REASON = ''
YOY_EXTRA = ''
FCF_NOTE = '(재고·매출채권 증가로 영업현금이 순이익보다 적다)'   # YoY·QoQ 각주의 FCF 정의 뒤에 붙는다(옛 카드)
SEG = [('AI 최적화 서버', 16401, '#007db8'), ('일반 서버·네트워킹', 10531, '#6cb4ea'), ('스토리지', 4850, '#9b59b6'),
       ('PC 등 클라이언트(CSG)', 15034, '#f7b600'), ('기타', 155, '#94a3b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 품목별 매출'
SEG_NOTE = ('인프라(ISG) 매출 +89%, 영업이익률 15.0% · 클라이언트(CSG) +20%, 7.6% · AI 서버 2분기 수주 $60.9B, 잔고 $95B · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Q2 FY2027 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (Q2 FY27, 950만 주 · 상반기 $5.4B)', '약 $3.8B'),
           ('잔여 바이백 승인 한도 (2026.07.31 기준)', '$10.4B'),
           ('배당 (FY27 상반기 지급)', '분기 $0.63(2월 20% 인상)', '$0.9B')]
CHECK_WHEN = '2026년 11월 하순 (예상) · Q3 FY27'
CHECK = ['3분기 가이던스(매출 $49.0B, GAAP EPS $6.10)와 연간 전망(매출 $192B, AI 서버 $74B, GAAP EPS $24.37) 달성',
         'AI 서버 잔고 $95B의 매출 전환 속도와 새 수주',
         '인프라(ISG) 영업이익률 15.0%가 유지되는지 — 1년 전 8.8%',
         '재고(연초의 약 2배)·매출채권과 영업현금흐름(2분기 $2.2B, 1년 전보다 13% 적음), 사채 발행 뒤 차입금']
NONOP_WHAT = '장기투자 $2.7B'
PH = ['AAPL', 'CSCO', 'ANET', 'IBM']
PEER_FILE = None
CHART_CAP, SELF_CAP = {}, {}
CHART_NOTE = {'pbr': ' (DELL 자본 음수)'}
CHART_TITLES = {'per': 'IT 하드웨어·네트워크 PER 비교', 'pbr': 'IT 하드웨어·네트워크 PBR 비교', 'psr': 'IT 하드웨어·네트워크 PSR 비교',
                'pcr': 'IT 하드웨어·네트워크 PCR(FCF) 비교', 'evebitda': 'IT 하드웨어·네트워크 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'GICS Information Technology 카드 유니버스 대비 배수 순위'
FUND_ASOF_NOTE = 'Q2 FY27 10-Q (2026-09-08 공시)'
SELF_SPAN = 'VMware 분사 뒤 2022-03부터 약 4.5년'   # 제목·툴팁 모두(fill.py SELF_SPAN, Fable 2026-10-05)
PREMISE = ('VMware 분사 뒤(약 {SM[\'PER\'][\'days\'] / 252:.1f}년) 자기 이력에서 네 배수가 모두 상위 10% 안이라 {selfsc:.1f}점이다(PBR은 자본이 음수라 계산하지 않는다). '
           '카드 유니버스 IT 종목 안에서는 싼 쪽({peersc:.1f}점)이다. <strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('현재가가 정당하려면 영업이익률이 <strong data-vs="req">{pct(DCF[\'requiredMargin\'])}</strong>여야 한다(최근 4분기 {pct(HIST[\'margin_now\'])}, 2분기 단독 {opm[-1]:.1f}%). '
        '모델의 성장 출발점은 5년 연 {pct(HIST[\'growth_5y\'])}·3년 {pct(HIST[\'growth_3y\'])}인데, 회사의 FY27 전망은 매출 +69%다 — 한 해 급증이 이력에 아직 다 들어가지 않았다. '
        '낙관 시나리오(${DCF[\'high\']:.0f})도 현재가의 {DCF[\'high\'] / px * 100:.0f}%다. 차입금에는 금융 자회사 DFS 빚 $9.6B를 넣었다(이자가 영업이익 밖, 2026-10-01 결정).')
FUND_TIP = ('매출 3년 연 증가율 3.5%·영업이익 12.2%는 FY2026까지 연간 값이라 FY27 급증이 아직 안 들어갔다. '
            '부채비율은 자본이 음수(−$1.4B)라 1점, 이자보상배율은 이자비용 태그가 없어 빠졌다.')
SELF_TIP = ('VMware 분사 뒤(2022-03-24~) 창이다. 네 배수 모두 그 창의 상위 10% 안이다(PSR {SM[\'PSR\'][\'current\']:.2f}배는 상위 {100 - SM[\'PSR\'][\'percentile\']:.0f}%). PBR은 자본 음수(−$1.4B)라 빠졌다. '
            '이력 앞쪽(2022년 3~12월)의 낮은 PER은 Boomi 매각 이익이 든 EPS 때문이다.')
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어처럼 마진 구조가 다른 고배수 종목이 섞여 있어, 하드웨어인 델은 PSR이 낮게(1위) 나온다. PBR은 자본 음수로 빠졌다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(연 {pct(HIST[\'growth_3y\'])})에서 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 15일 — 사채 $5.0B 발행', None,
     '2029·2031·2033·2037년 만기 선순위 사채(금리 5.1~5.9%) — 6월 발행에 이어 분기 뒤 차입 증가', 'notes', 'Dell Technologies 공시 (SEC 8-K)'),
    ('', '2026년 9월 1일 장 마감 후 — Q2 FY2027 실적', '2026-09-02',
     '매출 $47.0B(+58%)·EPS $6.34(비GAAP $7.04) · AI 서버 수주 $60.9B·잔고 $95B · 연간 매출 전망 $192B로 $25B 상향', 'q2', 'Dell Technologies 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 1일 — 본사 법인 텍사스로 이전', None,
     '설립 준거지를 델라웨어에서 텍사스로 변경(주주 권리 일부 달라짐)', 'texas', 'Dell Technologies 공시 (SEC 8-K)'),
    ('', '2026년 5월 28일 장 마감 후 — Q1 FY2027 실적', '2026-05-29',
     '매출 $43.8B(+88%)·EPS $5.24 · AI 서버 매출 $16.1B · 연간 AI 서버 전망 $60B, 매출 전망 $167B로 상향', 'q1', 'Dell Technologies 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 2월 26일 장 마감 후 — Q4 FY2026 실적', '2026-02-27',
     'FY26 매출 $113.5B(+19%)·EPS $8.68 · AI 잔고 $43B · 배당 20% 인상, 자사주 한도 $10B 추가 · FY27 매출 전망 $140B', 'q4', 'Dell Technologies 실적 보도자료 (SEC 8-K)'),
    ('', '2025년 11월 25일 장 마감 후 — Q3 FY2026 실적', '2025-11-26',
     '매출 $27.0B(+11%)·EPS $2.28 · AI 서버 수주 $12.3B, 잔고 $18.4B · 데이비드 케네디 CFO 정식 선임', 'q3', 'Dell Technologies 실적 보도자료 (SEC 8-K)'),
    ('', '2025년 10월 7일 — 증권 애널리스트 미팅', '2025-10-07',
     '장기 목표 상향: 매출 연 7~9%(이전 3~4%), 비GAAP EPS 연 15% 이상(이전 8%), 배당 연 10% 이상 인상을 FY2030까지', 'analyst', 'Dell Technologies 보도자료 (SEC 8-K)'),
]
SUMMARY = ('AI 서버 수요로 매출이 60% 가까이, 이익은 몇 배로 늘었고 주가는 1년 새 {1 + ch / 100:.0f}배가 됐다', '급성장·밸류 부담',
           ['2분기 매출이 1년 전보다 58% 늘었고 EPS는 $6.34로 약 3.7배다. 회사는 연간 매출 전망을 2월 $140B에서 $167B, $192B로 두 번 올렸다.',
            'AI 서버 잔고가 $18.4B(2025년 10월 말)에서 $95B(2026년 7월 말)로 커졌다.',
            '주가는 1년 새 {CH_TXT}이고, 최근 세 번의 실적 발표 다음 날 각각 +22%·+33%·+16% 올랐다.'],
           '영업현금흐름이 이익만큼 늘지 않았고(2분기 $2.2B, 순이익 $4.1B), 재고가 연초의 약 2배다. 분기 뒤 사채 $5.0B를 더 발행했다.',
           'Q3 FY27 실적(11월 하순 예상)의 가이던스 달성과 AI 잔고 전환.')
BULL = [('성장', '2분기 매출 +58%, 연간 매출 전망 $192B(+69%).'),
        ('잔고', 'AI 서버 잔고 $95B, 2분기 수주 $60.9B.'),
        ('환원', '2분기 주주환원 $4.3B(사상 최대), 배당 20% 인상.')]
BEAR = [('밸류', '자기 이력 네 배수가 모두 상위 10% 안이고, 기본 내재가치는 현재가의 {DCF[\'base\'] / px * 100:.0f}%다.'),
        ('현금', '영업현금흐름 $2.2B가 순이익 $4.1B의 절반 수준, 재고 $21.3B.'),
        ('부채', '차입금 $34.5B에 분기 뒤 사채 $5.0B 추가, 자본 음수.')]
ANALYST = {'rating': 'Buy', 'n': 29, 'nt': 22, 'mean': 577.91, 'median': 600, 'low': 290, 'high': 735, 'sb': 14, 'b': 6, 'h': 8, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-10'
MISSING_NOTE = ''   # 없는 배수(PBR — 자본 음수) 칸: 옛 카드는 배지에 사유를 적고 메모는 비웠다
MISSING_CUR, MISSING_BADGE = '계산 불가', '자본 음수 · 평균 제외'
REV_FOOTNOTE = ('회계연도는 1월 말·2월 초에 끝난다(Q2 FY27 = 2026년 5~7월). 2분기 매출 $47.0B는 1년 전보다 58% 많고, 그중 AI 서버가 $16.4B다. '
                '회사의 3분기 가이던스는 매출 $49.0B다.')

# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
POST = [r'''
# 보도자료 링크 글자: 옛 카드는 회계연도 네 자리(Q2 FY2027)
h = h.replace(f"{C.CO} {QL} 실적 보도자료 (SEC 8-K) →", f"{C.CO} Q2 FY2027 실적 보도자료 (SEC 8-K) →")
# 분기 차트 아래 설명(회계연도·AI 서버)
one(f'<canvas id="{t}RevChart"></canvas>\n    </div>\n', f'<canvas id="{t}RevChart"></canvas>\n    </div>\n'
    f'    <div class="yoy-footnote" style="margin-top:8px;">{C.REV_FOOTNOTE}</div>\n')
# YoY·QoQ 각주: FCF 정의 뒤 설명(옛 카드)
assert h.count(" · FCF는 영업현금흐름 − 설비투자 · ") == 2
h = h.replace(" · FCF는 영업현금흐름 − 설비투자 · ", " · FCF는 영업현금흐름 − 설비투자" + C.FCF_NOTE + " · ")
# 총자산증가율 메모: 회계연도 끝 날·연간 지표 꼬리(옛 카드)
one("FY2026 말 $", "FY2026 말(2026-01-30) $")
one("(전년 $79.7B) · 연간 지표</span>", "(전년 $79.7B) · 연간 지표, FY2027 10-K 전까지 동일</span>")
# 없는 배수 칸: 현재값·배지 글자(옛 카드 그대로 — CSCO와 같은 패치)
_i = h.index('const haveM = new Set'); _j = h.index("['peer', 'self'].forEach(k => {", _i)
_seg = h[_i:_j]
_seg2 = _seg.replace("f('cur').textContent = '—';", f"f('cur').textContent = {json.dumps(C.MISSING_CUR, ensure_ascii=False)};", 1).replace(
    "f('badge').textContent = '계산 불가';", f"f('badge').textContent = {json.dumps(C.MISSING_BADGE, ensure_ascii=False)};", 1)
assert _seg2 != _seg; h = h[:_i] + _seg2 + h[_j:]
''']


# ── 자동 카드(설계 D, 2026-10-11) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose2·3 제안(손 표와 숫자 일치 — 여러 축·나머지 줄) ──
AUTO = True
SEG_MAP = {
 "parts": [
  {
   "concepts": [
    "us-gaap:Revenues"
   ],
   "axis": "srt:ConsolidationItemsAxis",
   "extra": {
    "us-gaap:StatementBusinessSegmentsAxis": "dell:ClientSolutionsMember"
   },
   "members": {
    "us-gaap:OperatingSegmentsMember": [
     "PC 등 클라이언트(CSG)",
     "#f7b600"
    ]
   }
  },
  {
   "concepts": [
    "us-gaap:Revenues"
   ],
   "axis": "us-gaap:StatementBusinessSegmentsAxis",
   "extra": {
    "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember",
    "srt:ProductOrServiceAxis": "dell:StorageMember"
   },
   "members": {
    "dell:InfrastructureSolutionsGroupMember": [
     "스토리지",
     "#9b59b6"
    ]
   }
  },
  {
   "concepts": [
    "us-gaap:Revenues"
   ],
   "axis": "srt:ConsolidationItemsAxis",
   "extra": {},
   "members": {
    "us-gaap:CorporateNonSegmentMember": [
     "기타",
     "#94a3b8"
    ]
   }
  },
  {
   "concepts": [
    "us-gaap:Revenues"
   ],
   "axis": "srt:ProductOrServiceAxis",
   "extra": {
    "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember",
    "us-gaap:StatementBusinessSegmentsAxis": "dell:InfrastructureSolutionsGroupMember"
   },
   "members": {
    "dell:AIOptimizedServersAndNetworkingMember": [
     "AI 최적화 서버",
     "#007db8"
    ],
    "dell:TraditionalServersAndNetworkingMember": [
     "일반 서버·네트워킹",
     "#6cb4ea"
    ]
   }
  }
 ]
}
# 손 문구 블록 정리: 화면 구조 고침만 남기고 분기 문장·날짜 박힌 치환·손 데이터 블록은 뺐다(자동 카드는 못 찾으면 건너뜀)
POST = ['# 없는 배수 칸: 현재값·배지 글자(옛 카드 그대로 — CSCO와 같은 패치)\n_i = h.index(\'const haveM = new Set\'); _j = h.index("[\'peer\', \'self\'].forEach(k => {", _i)\n_seg = h[_i:_j]\n_seg2 = _seg.replace("f(\'cur\').textContent = \'—\';", f"f(\'cur\').textContent = {json.dumps(C.MISSING_CUR, ensure_ascii=False)};", 1).replace(\n    "f(\'badge\').textContent = \'계산 불가\';", f"f(\'badge\').textContent = {json.dumps(C.MISSING_BADGE, ensure_ascii=False)};", 1)\nassert _seg2 != _seg; h = h[:_i] + _seg2 + h[_j:]']
