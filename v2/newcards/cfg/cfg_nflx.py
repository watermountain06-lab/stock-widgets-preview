# NFLX(넷플릭스) v2 카드 설정 — fill.py NFLX. 회계연도 12월 31일. 시총 41위(루트 카드 있음). 2025년 11월 10:1 액면분할(주당 값은 분할 뒤 기준).
# 틀 시절 카드를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G1).
# 출처: SEC XBRL, Q2 2026 10-Q, 주주 서한(Q3 2025~Q2 2026), 8-K(WBD 인수·전액 현금 변경·해지, 자사주 승인, 액면분할), StockAnalysis(2026-10-01).
# 재현 모드: python3 v2/newcards/build.py NFLX --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-29).
BUILD = {}
CIK = '0001065280'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 12560, 'op': 4193, 'ni': 3401}   # Q2 2026 손익(백만 달러) — SEC XBRL, 옛 카드(매출 $12.56B)와 같다
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'Netflix'
S_ = 'https://www.sec.gov/Archives/edgar/data/1065280/'
SEC = S_
PR = {'q2': S_ + '000106528026000211/ex991_q226.htm', 'q1': S_ + '000106528026000137/ex991_q126.htm',
      'q4': S_ + '000106528026000033/ex991_q425.htm', 'q3': S_ + '000106528025000404/ex991_q325.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000106528026000212/nflx-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'buyback': S_ + '000106528026000139/nflx-20260422.htm', 'wbdend': 'https://www.sec.gov/Archives/edgar/data/1065280/000119312526082247/d120618d8k.htm',
         'wbdcash': 'https://www.sec.gov/Archives/edgar/data/1065280/000119312526015951/d37713d8k.htm',
         'wbd': 'https://www.sec.gov/Archives/edgar/data/1065280/000119312525308651/d65144d8k.htm', 'split': S_ + '000106528025000407/ex991_q425stocksplit.htm'}
FAIRBAND_TITLE = ('id="nflxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}. '
                  '이 EPS에는 1분기 WBD 인수 위약금 $2.8B(세전, 최근 4분기 세전이익의 약 17%)가 들어 있다."')
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +{HIST[\'growth_3y\'] * 100:.1f}%)</span>'
OPM_RANGE, Y2 = (15, 40), (15, 40)
FCF_SUB = '영업현금흐름 − 설비투자(위약금 관련 세금 납부 포함)'
CAPEX_SUB = '유형자산 취득(콘텐츠 투자는 영업현금에 포함)'
STAT3 = ('R&amp;D (Q2 2026)', '$1.01B', '기술·개발비, 매출의 8.0%')
NEXT = ('10월 중순 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('10월 중순', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), '2025년'
HEALTH_NOTE = ('유동비율 {FR[\'currentRatio\']:.1f}%이고 재고가 없어 당좌비율도 같다. 차입금은 $14.3B(1년 안 만기 $2.5B + 장기 $11.8B)이고 현금·단기투자는 $9.1B다. '
               '자산의 절반 넘게($33.8B)가 콘텐츠 자산이다. 7월에 2036년 만기 사채 $1.0B를 발행했다.')
ACT_REASON = ''
YOY_EXTRA = ''
FN_EXTRA = '1분기 순이익·FCF에는 WBD 위약금(세전 $2.8B, 순이익에는 세후)이 들어 있다 · '   # YoY·QoQ 각주(옛 카드는 GAAP 기준 바로 뒤)
SEG = [('미국·캐나다(UCAN)', 5432, '#e50914'), ('유럽·중동·아프리카(EMEA)', 4034, '#b20710'), ('중남미(LATAM)', 1584, '#f5a623'), ('아시아·태평양(APAC)', 1510, '#94a3b8')]
SEG_ADJ = 0   # 네 지역 합 = 보고 매출 12,560
SEG_TITLE = '매출 구성 — 지역별 매출'
SEG_NOTE = ('1년 전 대비 매출 증가율은 UCAN +10%(가격 인상이 분기 일부에만 반영), EMEA +14%, LATAM +21%, APAC +16% · '
            '회사는 2026년 광고 매출이 약 $3B로 2025년의 2배가 될 것으로 본다 · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Q2 2026 주주 서한 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (Q2 2026, 분기 최대)', '$4.7B'),
           ('잔여 바이백 승인 한도 (2분기 말, 4월 $25B 추가 승인)', '$27.1B'),
           ('배당 (Q2 2026)', '배당 없음', '해당 없음')]
CHECK_WHEN = '2026년 10월 중순 (예상) · Q3 2026'
CHECK = ['3분기 전망(매출 $12.86B, +12%·영업이익률 33.2%·EPS $0.82)과 연간 전망(매출 $51.0~51.4B, 영업이익률 31.5%) 달성',
         '미국·캐나다 가격 인상 효과(2분기 매출 +10%)와 성장 둔화 여부 — 3분기 전망 +12%는 1년 전 +17%보다 낮다',
         '광고 매출(2026년 약 $3B 전망)과 연간 FCF 약 $12.5B',
         'WBD 인수 무산 뒤 자본 배분 — 잔여 자사주 한도 $27.1B와 "선별적 인수합병"']
NONOP_WHAT = '투자'
PH = ['GOOGL', 'META', 'AMZN', 'DIS']
PEER_FILE = None   # 옛 카드 비교 막대(9/29 종가)는 AMZN이 들어 있어 통신서비스 S&P500 파일이 아니라 카드 기준으로 낸다
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
MISS_WHY = {('DIS', 'evebitda'): ' 값 없음'}
CHART_TITLES = {'per': '미디어·플랫폼 대형주 PER 비교', 'pbr': '미디어·플랫폼 대형주 PBR 비교', 'psr': '미디어·플랫폼 대형주 PSR 비교',
                'pcr': '미디어·플랫폼 대형주 PCR(FCF) 비교', 'evebitda': '미디어·플랫폼 대형주 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 커뮤니케이션 서비스 섹터와 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'Communication Services + Information Technology 카드 유니버스 대비 배수 순위'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-17 공시)'
PREMISE = ('주가가 1년 새 {ch:.0f}%(10월 고점 종가 $124.14에서 7월 저점 $67.60까지는 -46%) 내려, PER·EV/EBITDA·PCR은 자기 5년 이력의 하위 약 10%, PBR·PSR은 중앙값 아래다'
           '({selfsc:.1f}점, PER {SM[\'PER\'][\'current\']:.1f}배 대 5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배). '
           '통신서비스+IT 카드 유니버스 안에서도 싼 쪽({peersc:.1f}점, 동종업 가격 기준일 {PEER_DATES})이다. '
           'PER은 1분기 WBD 위약금 $2.8B(세전, 최근 4분기 세전이익의 약 17%)가 든 GAAP EPS ${eps_ttm} 기준이라 그만큼 낮게 나온다(본업 기준 문턱 20% 아래라 GAAP 유지). '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('현재가가 정당하려면 5년간 매출이 연 <strong>{pct(DCF[\'requiredGrowth\'])}</strong>씩 커야 한다(지난 5년 실제 연 {pct(HIST[\'growth_5y\'])}, 회사의 2026년 전망 +13~14%). '
        '기본 시나리오는 최근 1년 매출/자본 {S2C_M:.2f}(매출 $1당 투자 약 ${1 / S2C_M:.2f})에서 출발해 평균 {S2C_A:.2f}(약 ${1 / S2C_A:.2f})로 내려간다(낙관·보수는 평균). '
        '2026년 단기차입 $2.5B를 운전자본에서 되돌리면서 최근 1년 효율이 정의됐다(2026-10-03 B17). 콘텐츠 투자는 영업현금흐름 안에서 빠져나가 설비투자에 잡히지 않는다.')
FUND_TIP = ('순이익률 {GP[\'netMargin\'][\'value\']:.1f}%({GP[\'netMargin\'][\'points\']}점)·영업이익률 {GP[\'opMargin\'][\'value\']:.1f}%({GP[\'opMargin\'][\'points\']}점)로 수익성 점수가 높다. '
            '순이익률에는 1분기 WBD 위약금이 들어 있지 않다(분기 기준 2분기 값).')
SELF_TIP = ('PER {SM[\'PER\'][\'current\']:.1f}배·EV/EBITDA {SM[\'EV/EBITDA\'][\'current\']:.1f}배·PCR {SM[\'PCR\'][\'current\']:.1f}배가 5년 하위 약 10% 안이다'
            '(PCR 이력 최고 {SM[\'PCR\'][\'max\']:,.0f}배는 FCF가 0 근처였던 분기 값).')
PEER_TIP = ('통신서비스 섹터가 카드 유니버스에 적어 IT를 합쳐 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어 등 사업모델이 다른 고배수 종목이 섞여 있다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(연 {pct(HIST[\'growth_3y\'])})에서 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('', '2026년 7월 16일 장 마감 후 — Q2 2026 실적', '2026-07-17',
     '매출 $12.56B(+13%)·영업이익률 33.4%·EPS $0.80 · 연간 매출 전망 $51.0~51.4B로 좁힘 · 자사주 $4.7B(분기 최대)', 'q2', 'Netflix 주주 서한 (SEC 8-K)'),
    ('green', '2026년 4월 22일 — 자사주 $25B 추가 승인', None,
     '기존 잔여 $6.8B(3월 말)에 더해 $25B, 기한 없음', 'buyback', 'Netflix 공시 (SEC 8-K)'),
    ('', '2026년 4월 16일 장 마감 후 — Q1 2026 실적', '2026-04-17',
     '매출 $12.25B(+16%)·영업이익률 32.3% · EPS $1.23(WBD 위약금 $2.8B 포함) · 연간 FCF 전망 $11B → $12.5B · 리드 헤이스팅스 이사회 재선 불출마', 'q1', 'Netflix 주주 서한 (SEC 8-K)'),
    ('neutral', '2026년 2월 26~27일 — WBD 인수 계약 해지', '2026-02-27',
     'WBD가 파라마운트 스카이댄스 제안을 우월 제안으로 정하자 넷플릭스는 재협상하지 않았고, 해지 위약금 $2.8B를 받았다', 'wbdend', 'Netflix 공시 (SEC 8-K)'),
    ('', '2026년 1월 20일 장 마감 후 — Q4 2025 실적', '2026-01-21',
     '2025년 매출 $45.2B(+16%) · 4분기 영업이익률 24.5% · 2026년 매출 전망 $50.7~51.7B', 'q4', 'Netflix 주주 서한 (SEC 8-K)'),
    ('neutral', '2026년 1월 20일 장 전 — WBD 인수를 전액 현금으로 변경', '2026-01-20',
     '1월 19일 합의: 주당 $27.75를 현금과 넷플릭스 주식 대신 전액 현금으로 · 브리지 대출 약정 $42.2B로 증액', 'wbdcash', 'Netflix 공시 (SEC 8-K)'),
    ('neutral', '2025년 12월 5일 장 전 — 워너브러더스 인수 계약', '2025-12-05',
     'WBD 스튜디오·HBO Max를 주당 $27.75(기업가치 약 $82.7B, 현금+주식)에 인수 계약 · $59B 브리지 대출 약정', 'wbd', 'Netflix 공시 (SEC 8-K)'),
    ('neutral', '2025년 10월 30일 장 마감 후 — 10:1 액면분할 발표', '2025-10-31',
     '11월 10일 기준 주주에게 1주당 9주 추가, 11월 17일부터 분할 가격으로 거래', 'split', 'Netflix 공시 (SEC 8-K)'),
    ('', '2025년 10월 21일 장 마감 후 — Q3 2025 실적', '2025-10-22',
     '매출 $11.51B(+17%) · 영업이익률 28.2%(브라질 세무 분쟁 비용 반영, 전망 밖)', 'q3', 'Netflix 주주 서한 (SEC 8-K)'),
]
SUMMARY = ('실적은 대체로 전망대로 나왔지만 발표 다음 날마다 주가가 내렸고, 1년 새 약 {-ch:.0f}% 하락했다', '조정·성장률 둔화',
           ['주가는 1년 새 {ch:.0f}%이고, 최근 네 번의 실적 발표 다음 날 모두 내렸다(2025-10 -10%, 2026-01 -2%, 2026-04 -10%, 2026-07 -7%).',
            '2025년 12월 WBD 인수 계약을 맺었다가 2026년 2월 파라마운트 제안에 밀려 해지했고, 위약금 $2.8B를 받았다. 계약 기간(12/5~2/26) 주가는 -18%였고, 해지가 알려진 2월 27일에는 +14%였다.',
            '매출 성장률은 2025년 4분기 +17.6%에서 2026년 2분기 +13.4%, 3분기 전망 +11.7%로 내려오는 중이다.'],
           '배수는 5년 중 가장 싼 쪽이지만, 현금흐름 모델로는 현재가의 {DCF[\'base\'] / px * 100:.0f}%만 설명된다. PER에는 일회성 위약금이 들어 있다.',
           'Q3 2026 실적(10월 중순 예상)의 매출 성장률과 광고 매출, 자사주 매입 속도.')
BULL = [('수익성', '2분기 영업이익률 {op[cur] / rev[cur] * 100:.1f}%, 3분기 전망 33.2%(1년 전 28.2%는 브라질 세무 비용 반영).'),
        ('배수', 'PER·EV/EBITDA·PCR이 5년 하위 약 10% 안이다(PER {SM[\'PER\'][\'current\']:.1f}배).'),
        ('환원', '2분기 자사주 $4.7B(분기 최대), 잔여 한도 $27.1B.')]
BEAR = [('성장', '매출 성장률이 17.6% → 13.4% → 3분기 전망 11.7%로 내려오고 있다.'),
        ('밸류', '기본 내재가치는 현재가의 {DCF[\'base\'] / px * 100:.0f}%이고, 현재가는 연 {pct(DCF[\'requiredGrowth\'])} 성장을 요구한다.'),
        ('인수', 'WBD 인수는 무산됐지만 회사는 "선별적 인수합병"을 자본 배분 우선순위에 두고 있다.')]
ANALYST = {'rating': 'Buy', 'n': 51, 'nt': 31, 'mean': 93.35, 'median': 92, 'low': 57, 'high': 135, 'sb': 28, 'b': 7, 'h': 15, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-10'
REV_FOOT = ('1분기 순이익 $5.3B가 튀는 것은 워너브러더스(WBD) 인수 계약 해지 위약금 $2.8B가 영업외 수익("interest and other income")으로 들어와서다. '
            '영업이익률은 1분기 {op[qo] / rev[qo] * 100:.1f}%, 2분기 {op[cur] / rev[cur] * 100:.1f}%였고, 회사는 2026년 연간 31.5%를 전망한다. 2025년 11월 10:1 액면분할로 주당 값은 모두 분할 뒤 기준이다.')
REVERSE = ('지금 가격(<span data-dcf-price>${px:.2f}</span>)이 정당하려면 5년간 매출이 매년 <b data-dcf-req>{pct(DCF[\'requiredGrowth\'])}</b>씩 커야 한다(마진은 기본 시나리오 경로). '
           '기본 시나리오(<span data-dcf-basev>${DCF[\'base\']:.0f}</span>)를 같은 방식으로 환산하면 연 <span data-dcf-baseeq>{pct(DCF[\'baseEquivGrowth\'])}</span>다.')

# 카드 한정 패치 — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
PRE = [r'''
FR = {r_['metric']: r_['value'] for r_ in FUND['axes']['health']['rows']}
GP = {r_['metric']: r_ for r_ in FUND['axes']['growthProfit']['rows']}
_s2a = bd.s2c_path_for(b, '낙관')[0][0]
S2C_A, S2C_M = _s2a, (b.get('_s2c_marginal') or _s2a)
PEER_DATES = '~'.join(f"{int(d_[5:7])}/{int(d_[8:10])}" for d_ in VAL['peer']['asOf'])
''']
POST = [r'''
# 총자산증가율 메모 꼬리
sub(r'(<span class="diag-label">총자산증가율</span><span class="diag-value">[^<]*</span><span class="diag-note">2025년 말 [^<]*· 연간 지표)(</span>)', lambda m_: m_.group(1) + ', 2026년 마감 전까지 동일' + m_.group(2))
# 분기 차트 아래 설명, 성장 모드 역산 문장(fill.py는 '—'만 남긴다)
one(f'<canvas id="{t}RevChart"></canvas>\n    </div>\n', f'<canvas id="{t}RevChart"></canvas>\n    </div>\n    <div class="yoy-footnote" style="margin-top:8px;">' + F(C.REV_FOOT) + '</div>\n')
one('<div class="reverse">—</div>', '<div class="reverse">' + F(C.REVERSE) + '</div>')
# YoY·QoQ 각주: 위약금 설명(GAAP 기준 뒤), 링크 이름은 주주 서한
for _a in (f"{C.YO.replace('-', '.')}({C.YL})", f"{C.QO.replace('-', '.')}({C.QQL})"):
    one(f"vs {_a} · GAAP 기준 · FCF는", f"vs {_a} · GAAP 기준 · " + C.FN_EXTRA + "FCF는")
h = h.replace(f'{C.CO} {QL} 실적 보도자료 (SEC 8-K) →', f'{C.CO} {QL} 주주 서한 (SEC 8-K) →')
''']


# ── 자동 카드(설계 D, 2026-10-10) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose.py 제안(손 표와 숫자 일치) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:Revenues"
 ],
 "axis": "srt:StatementGeographicalAxis",
 "extra": {
  "srt:ProductOrServiceAxis": "nflx:StreamingMember"
 },
 "members": {
  "nflx:UnitedStatesAndCanadaMember": [
   "미국·캐나다(UCAN)",
   "#e50914"
  ],
  "us-gaap:EMEAMember": [
   "유럽·중동·아프리카(EMEA)",
   "#b20710"
  ],
  "srt:LatinAmericaMember": [
   "중남미(LATAM)",
   "#f5a623"
  ],
  "srt:AsiaPacificMember": [
   "아시아·태평양(APAC)",
   "#94a3b8"
  ]
 },
 "ignore": []
}
# 손 문구 블록 정리: 화면 구조 고침만 남기고 분기 문장·날짜 박힌 치환·시간이 지나면 틀려지는 문장은 뺐다. 덩어리마다 따로 실행(자동 카드는 못 찾으면 건너뜀)
POST = ['one(\'<div class="reverse">—</div>\', \'<div class="reverse">\' + F(C.REVERSE) + \'</div>\')', "h = h.replace(f'{C.CO} {QL} 실적 보도자료 (SEC 8-K) →', f'{C.CO} {QL} 주주 서한 (SEC 8-K) →')"]
