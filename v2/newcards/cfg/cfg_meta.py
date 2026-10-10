# META(메타 플랫폼스) v2 카드 설정 — fill.py META. 회계연도 12월 31일. 시총 상위(루트 카드 있음). PER은 일회성 법인세 제외 EPS(tax_oneoff).
# 틀 시절 카드(2026-09-24 루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G1).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30), 실적 보도자료(Q3 2025~Q2 2026), 8-K(회사채 5/4), Meta Newsroom, TechCrunch, Motley Fool, StockAnalysis(2026-09-25).
# 재현 모드: python3 v2/newcards/build.py META --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-24).
BUILD = {}
CIK = '0001326801'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 60801, 'op': 18775, 'ni': 15848}   # Q2 2026 손익(백만 달러) — SEC XBRL, 옛 카드(매출 $60.8B)와 같다
VOTES, VERDICT = (0, 0, -1), '적정~고평가'
CO = 'Meta'
S_ = 'https://www.sec.gov/Archives/edgar/data/1326801/'
SEC = S_
PR = {'q2': S_ + '000162828026050596/meta-06302026xexhibit991.htm', 'q1': S_ + '000162828026028364/meta-03312026xexhibit991.htm',
      'q4': S_ + '000162828026003832/meta-12312025xexhibit991.htm', 'q3': S_ + '000162828025047114/meta-09302025xexhibit991.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000162828026050705/meta-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'connect': 'https://techcrunch.com/2026/09/23/everything-new-coming-to-metas-ai-agent-muse/',
         'top1': 'https://www.fool.com/coverage/stock-market-today/2026/09/21/stock-market-today-sept-21-meta-surges-on-excitement-over-muse-personal-ai-agent/',
         'muse': 'https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/',
         'bond': S_ + '000119312526204128/d134616d8k.htm'}
FAIRBAND_TITLE = 'id="metaFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 EPS ${eps_ttm}(일회성 법인세 제외, 10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +{HIST[\'growth_3y\'] * 100:.1f}%)</span>'
OPM_RANGE, Y2 = (25, 55), (25, 55)
FCF_SUB = '현금창출력'
CAPEX_SUB = '미래 재투자'
STAT3 = ('R&amp;D (Q2 2026)', '$21.7B', '기술 경쟁력 투자')
NEXT = ('10월 말 예상', '일정 · Q3 2026'); NEXT_OP = ('10월 말', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY25'
ASSET_NEXT_FY = 'FY26'
HEALTH_NOTE = ('유동비율 {FR[\'currentRatio\']:.0f}%로 단기 지급 여력은 넉넉하고, 이자보상배율은 {FR[\'interestCoverage\']:.1f}배다. '
               '설비투자 재원으로 회사채를 2025년 11월 $30B, 2026년 5월 $25B 발행해 장기차입금이 $58.7B(2025년 말)에서 $83.7B가 됐다. '
               '현금·유가증권 $90.3B이 차입금보다 조금 많지만, 리스부채까지 더하면 순차입금이다.')
ACT_REASON = ''
YOY_EXTRA = '(회사 발표 FCF는 금융리스 원금 상환까지 빼 $0.78B) · '
SEG = [('광고', 59363, '#1877F2'), ('기타(앱 부문)', 1007, '#f97316'), ('Reality Labs', 431, '#8a8fa8')]
SEG_ADJ = 0   # 세 칸 합 = 보고 매출 60,801
SEG_TITLE = '매출 구성 — 부문별'
SEG_NOTE = ('광고 매출은 노출 +14%, 광고 단가 +12%로 전년 대비 27% 늘었다. Reality Labs는 영업손실 $4.6B · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Meta Q2 2026 실적 발표 (SEC 8-K) →</a>')
CAPITAL = [('설비투자 (Q2 2026, 금융리스 원금 포함)', '$31.1B'),
           ('2026년 설비투자 전망 (7월)', '$130~145B'),
           ('배당 (Q2 2026, 주당 $0.525)', '', '$1.35B')]
CAPITAL_EXTRA = [('자사주 매입 (2026년 상반기)', '$0')]   # 틀은 세 칸 — 네 번째 칸
CAPITAL_FOOT = ('자사주 매입은 2025년 4분기부터 멈췄다(잔여 한도 $25.03B). 2025년 한 해 매입액은 $26.26B였다 · '
                '출처: <a href="{TENQ}" target="_blank" rel="noopener">Meta Q2 2026 10-Q →</a>')
CHECK_WHEN = '2026년 10월 말 (예상) · Q3 2026'
CHECK = ['매출이 가이던스 $61~64B(중간값 기준 전년 대비 약 +22%)에 드는지',
         '연간 비용 전망 $165~169B 안에서 "2026년 영업이익이 2025년($83.3B)보다 많다"는 약속을 지킬 수 있는지(상반기 $41.6B)',
         '설비투자(연 $130~145B 전망)가 잉여현금흐름을 얼마나 더 깎는지(Q2 회사 발표 FCF $0.78B)',
         '9월 출시한 Muse의 이용자·유료 전환 수치를 처음 밝히는지, 청소년 관련 재판 결과가 나오는지']
NONOP_WHAT = '지분·장기투자'
PH = ['GOOGL', 'MSFT', 'AMZN', 'AAPL', 'NFLX']
PEER_FILE = None
CHART_CAP, SELF_CAP = {'pbr': 30}, {}
CHART_NOTE = {'pbr': ' (AAPL은 축 밖)'}   # 옛 카드 그대로 — AAPL PBR 약 45배. 옛 PCR 제목의 "AMZN 잉여현금흐름 적자"는 지금 AMZN 카드 값(양수)이라 뺐다
CHART_TITLES = {'per': '빅테크 PER 비교', 'pbr': '빅테크 PBR 비교', 'psr': '빅테크 PSR 비교',
                'pcr': '빅테크 PCR(FCF) 비교', 'evebitda': '빅테크 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 커뮤니케이션 서비스 섹터와 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'GICS Information Technology 대비 배수 순위 (카드 공통 섹터 차용)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-30 공시)'
PREMISE = ('동종업 안에서는 {score_word(peersc)}({peersc:.1f}점)이지만 다섯 배수 모두 자기 5년 이력의 중앙값보다 비싼 쪽이고(PCR은 5년 중 최고), '
           '<strong>현금흐름 내재가치(기본 시나리오)는 현재가의 {DCF[\'base\'] / px * 100:.0f}%다.</strong> '
           '2분기 설비투자가 매출의 절반까지 늘어 잉여현금흐름이 줄어든 것이 크다. 현재가 ÷ 기본 내재가치가 {px / DCF[\'base\']:.2f}로 "매우 비싸다"(1.5 초과)이고, '
           '자기 이력 점수({selfsc:.1f})는 "비싸다" 기준 30 바로 {"아래" if selfsc < 30 else "위"}다.')
RISK = ('현재가가 정당하려면 5년간 매출이 매년 <strong data-vs="req">{pct(DCF[\'requiredGrowth\'])}</strong>씩 커야 한다. '
        '최근 약 5년(19분기) 실제 성장은 연 {pct(HIST[\'growth_5y\'])}였고, 3분기 가이던스 중간값($62.5B)은 전년 대비 약 22% 성장이다.')
FUND_TIP = '2분기 영업이익률 {op[cur] / rev[cur] * 100:.1f}%에는 법적 비용 $2.40B와 감원 비용 $1.18B가 들어 있다.'
SELF_TIP = 'PCR은 5년 중 가장 비싼 자리다(설비투자로 잉여현금흐름이 줄었다). PER은 일회성 법인세(회사가 밝힌 두 건과 연간 세율에서 역산한 4분기 환입)를 뺀 EPS로 계산했다.'
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['지난 5년 성장 속도의 절반에서 출발해 점점 식고, 영업이익률은 지난 5년 중앙값({pct(HIST[\'margin_5y\'])})에 맞춘다. 매출 $1을 늘리는 데 ${INV[\'보수\']:.2f}를 투자한다(최근 1년 — 과거 평균 ${INV[\'avg\']:.2f}보다 자본이 더 드는 쪽).',
           '지난 5년의 성장 속도로 출발해 점점 식고, 영업이익률은 최근 2년 중앙값({pct(HIST[\'margin_2y\'])})으로 서서히 올라간다. 매출 $1당 투자는 최근 1년 ${INV[\'recent\']:.2f}에서 5년에 걸쳐 과거 평균 ${INV[\'avg\']:.2f}로 돌아온다.',
           '최근 3년의 성장 속도로 출발해 점점 식고, 지금 영업이익률({pct(HIST[\'margin_now\'])})이 그대로 간다. 매출 $1당 투자는 과거 평균 ${INV[\'avg\']:.2f}다. 지금 마진이 법적 비용·감원 비용으로 2년 중앙값보다 낮아, 마진만 보면 기본보다 보수적이다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 23일 발표 · 9월 24일 반응 — Meta Connect', '2026-09-24',
     'Muse에 실시간 아바타·전용 이메일·Mac 앱을 붙이고 AI 안경 연동 예고 · Walmart·Best Buy 등 쇼핑 제휴와 Stripe·Shopify 결제 연동', 'connect', 'TechCrunch'),
    ('green', '2026년 9월 21일 — Muse 미국 앱스토어 1위', '2026-09-21',
     '출시 2주 만에 Muse가 미국 앱스토어 1위 · Wells Fargo 목표주가 $640 → $796', 'top1', 'Motley Fool'),
    ('', '2026년 9월 8일 발표 · 9월 9일 반응 — 개인 AI 에이전트 Muse 출시', '2026-09-09',
     '일정·쇼핑·예약을 대신 처리하는 Muse를 미국에 출시 · 기본 무료, 더 많이 쓰는 사람을 위한 유료 요금제', 'muse', 'Meta Newsroom'),
    ('red', '2026년 7월 29일 발표 · 7월 30일 반응 — Q2 2026 실적', '2026-07-30',
     '매출 $60.8B(+28%)로 가이던스 $58~61B 상단 근처 · 비용 +55%(법적 비용 $2.40B·감원 $1.18B 포함)로 영업이익 −8% · 설비투자 전망 $130~145B', 'q2', 'Meta 실적 발표 (SEC 8-K)'),
    ('neutral', '2026년 5월 4일 — 회사채 $25B 발행', '2026-05-04',
     '5~40년 만기 6개 트랜치로 $25B 발행 완료 · 2025년 11월 $30B에 이은 두 번째 대규모 발행', 'bond', 'Meta 공시 (SEC 8-K)'),
    ('', '2026년 4월 29일 발표 · 4월 30일 반응 — Q1 2026 실적', '2026-04-30',
     '매출 $56.3B(+33%)로 가이던스 $53.5~56.5B 상단 근처 · 설비투자 전망 $115~135B → $125~145B 상향 · 일회성 세금 환입 $8.03B', 'q1', 'Meta 실적 발표 (SEC 8-K)'),
    ('', '2026년 1월 28일 발표 · 1월 29일 반응 — Q4 2025 실적', '2026-01-29',
     '매출 $59.9B(+24%)로 가이던스 $56~59B 상회 · 2026년 설비투자 $115~135B 제시, 영업이익은 2025년보다 많을 것', 'q4', 'Meta 실적 발표 (SEC 8-K)'),
    ('red', '2025년 10월 29일 발표 · 10월 30일 반응 — Q3 2025 실적', '2025-10-30',
     '매출 $51.2B(+26%) · 일회성 비현금 법인세 $15.93B로 순이익 $2.7B(−83%) · 2025년 설비투자 전망 $70~72B로 상향', 'q3', 'Meta 실적 발표 (SEC 8-K)'),
]
SUMMARY = ('AI 에이전트 Muse가 새 성장 동력으로 떠올랐다', '우호적·투자 부담',
           ['매출이 네 분기 연속 20% 넘게 늘었다(전년 대비 26% → 24% → 33% → 28%). 광고 노출과 단가가 함께 올랐다.',
            '9월 8일 출시한 Muse가 2주 만에 미국 앱스토어 1위에 올랐고, Connect(9/23)에서 안경 연동과 쇼핑 제휴를 발표했다. 주가는 9월에만 약 36% 올랐다.',
            '설비투자 전망이 1월 $115~135B → 4월 $125~145B → 7월 $130~145B로 올라갔다.'],
           '비용이 매출보다 빨리 는다(2분기 비용 +55%, 영업이익 −8%). 회사는 청소년 관련 재판에서 중대한 손실이 날 수 있다고 경고했고, 실적 발표 다음날 주가가 오른 것은 네 번 중 한 번(Q4 2025)뿐이다.',
           'Q3 2026 실적(10월 말 예상)에서 매출 $61~64B 가이던스를 넘는지, Muse 이용자·유료 전환 수치를 밝히는지.')
BULL = [('광고', '2분기 광고 노출 +14%, 광고 단가 +12%로 광고 매출이 27% 늘었다.'),
        ('Muse', '9월 출시한 개인 AI 에이전트가 2주 만에 미국 앱스토어 1위에 올랐고, 유료 요금제를 함께 내놓았다.'),
        ('사용자', '하루 활성 사용자(DAP)가 36억 명이라, 새 서비스를 바로 넓힐 바탕이 있다.')]
BEAR = [('설비투자', '2026년 설비투자 전망이 $130~145B이고, 2분기 회사 발표 잉여현금흐름은 $0.78B였다.'),
        ('법적 위험', '2분기 법적 비용이 $2.40B였고, 회사는 청소년 관련 재판에서 중대한 손실이 날 수 있다고 밝혔다.'),
        ('밸류', '현재가가 기본 내재가치의 약 {px / DCF[\'base\']:.1f}배이고, PCR은 자기 5년 중 가장 비싼 자리다.')]
ANALYST = {'rating': 'Strong Buy', 'n': 63, 'nt': 42, 'mean': 808.55, 'median': 810, 'low': 580, 'high': 1000, 'sb': 47, 'b': 8, 'h': 7, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-10'
REVERSE = ('지금 가격(<span data-dcf-price>${px:.2f}</span>)이 정당하려면 5년간 매출이 매년 <b data-dcf-req>{pct(DCF[\'requiredGrowth\'])}</b>씩 커야 한다. '
           '기본 시나리오(<span data-dcf-basev>${DCF[\'base\']:.0f}</span>)를 같은 방식으로 환산하면 연 <span data-dcf-baseeq>{pct(DCF[\'baseEquivGrowth\'])}</span>다.')

# 카드 한정 패치 — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다(AAPL·MSFT·GOOGL과 같은 묶음 + 자본배분 네 번째 칸, QoQ 각주).
PRE = [r'''
FR = {r_['metric']: r_['value'] for r_ in FUND['axes']['health']['rows']}
_s2 = {s_: bd.s2c_path_for(b, s_)[0] for s_ in ('보수', '기본', '낙관')}
INV = {'보수': 1 / _s2['보수'][0], 'avg': 1 / _s2['낙관'][0], 'recent': 1 / (b.get('_s2c_marginal') or _s2['낙관'][0])}
''']
POST = [r'''
sub(r'(<span class="diag-label">총자산증가율</span><span class="diag-value">)([+-])([\d.]+%</span><span class="diag-note">)' + C.FY_LABEL + r' 말 (\$[\d.]+B)\(전년 (\$[\d.]+B)\) · 연간 지표(</span>)',
    lambda m_: m_.group(1) + m_.group(2).replace('-', '−') + m_.group(3) + C.FY_LABEL + ' ' + m_.group(4) + '(전기 ' + m_.group(5) + ') · 연간 지표, ' + C.ASSET_NEXT_FY + ' 마감 전까지 동일' + m_.group(6))
one('<div class="reverse">—</div>', '<div class="reverse">' + F(C.REVERSE) + '</div>')
one('            <span class="zone-tag" style="background:rgba(240,192,64,0.18);color:var(--gold);"></span>\n', '')
sub(r'(<div class="card-title">자본배분 · 주주환원 [^<]*</div>\n      <div class="zone-list">.*?)(\n      </div>\n)',
    lambda m_: m_.group(1) + ''.join(f'\n        <div class="zone-item">\n          <span class="zone-label">{l_}</span>\n          <span class="zone-val">{v_}</span>\n        </div>' for l_, v_ in C.CAPITAL_EXTRA)
    + m_.group(2) + '      <div class="yoy-footnote" style="margin-top:14px;">' + F(C.CAPITAL_FOOT) + '</div>\n')
# 재고 없는 회사의 재고 회전율 칸: 틀의 '재고 없음'(2026-10-05 META Infinity회 수정)을 fill.py가 '해당 없음'으로 덮는다 — 옛 카드 문구로
one("el.textContent = dd > 0 ? (365 / dd).toFixed(2) + '회' : '해당 없음'; });", "el.textContent = dd > 0 ? (365 / dd).toFixed(2) + '회' : (el.dataset.actTurn === 'dio' ? '재고 없음' : '해당 없음'); });")
# FCF 정의 각주: 옛 카드는 "설비투자(회사 발표 …)"로 붙여 썼고 QoQ에도 있었다
h = h.replace('FCF는 영업현금흐름 − 설비투자 · ' + C.YOY_EXTRA, 'FCF는 영업현금흐름 − 설비투자' + C.YOY_EXTRA, 1)
one(f"vs {C.QO.replace('-', '.')}({C.QQL}) · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · <a", f"vs {C.QO.replace('-', '.')}({C.QQL}) · GAAP 기준 · FCF는 영업현금흐름 − 설비투자" + C.YOY_EXTRA + "<a")
''']
