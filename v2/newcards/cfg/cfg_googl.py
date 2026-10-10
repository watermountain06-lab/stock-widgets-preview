# GOOGL(알파벳) v2 카드 설정 — fill.py GOOGL. 회계연도 12월 31일. 시총 상위(루트 카드 있음). 본업 기준 종목(core_earnings.json — 비상장 지분 평가이익).
# 틀 시절 카드(2026-09-24 루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G1).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-23), 실적 보도자료(Q3 2025~Q2 2026), 8-K(주식 발행 6/1), Al Jazeera(광고기술 판결), StockAnalysis(2026-09-17).
# 재현 모드: python3 v2/newcards/build.py GOOGL --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-23).
BUILD = {}
CIK = '0001652044'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 119796, 'op': 40770, 'ni': 112193}   # Q2 2026 손익(백만 달러, 공시 순이익) — SEC XBRL, 옛 카드(매출 $119.8B, 공시 순이익 $112.2B)와 같다
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Alphabet'
S_ = 'https://www.sec.gov/Archives/edgar/data/1652044/'
SEC = S_
PR = {'q2': S_ + '000165204426000066/googexhibit991q22026.htm', 'q1': S_ + '000165204426000043/googexhibit991q12026.htm',
      'q4': S_ + '000165204426000012/googexhibit991q42025.htm', 'q3': S_ + '000165204425000087/googexhibit991q32025.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000165204426000071/goog-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'adtech': 'https://www.aljazeera.com/economy/2026/9/2/us-judge-rejects-bid-to-break-up-googles-ad-business',
         'equity': 'https://www.sec.gov/Archives/edgar/data/1652044/000119312526257724/d83560dex991.htm',
         'tenq': TENQ}
FAIRBAND_TITLE = 'id="googlFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 EPS ${eps_ttm}(본업 기준, 10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +{HIST[\'growth_3y\'] * 100:.1f}%)</span>'
OPM_RANGE, Y2 = (25, 40), (25, 40)
FCF_SUB = '현금창출력'
CAPEX_SUB = '미래 재투자'
STAT3 = ('R&amp;D (Q2 2026)', '$18.2B', '기술 경쟁력 투자')
NEXT = ('10월 말 예상', '일정 · Q3 2026'); NEXT_OP = ('10월 말', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY25'
ASSET_NEXT_FY = 'FY26'
HEALTH_NOTE = ('유동비율·이자보상배율은 기준을 크게 넘는다. 2026년 상반기에 AI 인프라 투자 재원으로 회사채 $51.8B, 6.25% 의무전환 우선주 $18.0B, '
               '보통주를 발행했고 자사주 매입은 멈췄다(Q2 2026 10-Q).')
ACT_REASON = ''
YOY_EXTRA = ''
SEG = [('검색 등', 63271, '#a2c3fa'), ('Google Cloud', 24768, '#3498db'), ('구독·플랫폼·기기', 12911, '#4285f4'), ('YouTube 광고', 11055, '#0c55ce'),
       ('네트워크', 7303, '#5c6282'), ('기타(Other Bets·헤지)', 488, '#2e3347')]
SEG_ADJ = 0   # 여섯 칸 합 = 보고 매출 119,796
SEG_TITLE = '매출 구성 — 사업별'
SEG_NOTE = '출처: <a href="{TENQ}" target="_blank" rel="noopener">Alphabet Q2 2026 10-Q (SEC) →</a> · Cloud 수주잔고 $513.9B'
CAPITAL = [('자사주 매입 (2026 상반기)', '없음'),
           ('잔여 매입 승인 한도', '$69.5B'),
           ('배당 (Q2 2026 · 주당 $0.22)', '', '$2.7B')]
CAPITAL_EXTRA = [('인수 (Wiz $29.5B · Intersect $5.9B)', '$35.4B')]   # 틀은 세 칸 — 네 번째 칸
CAPITAL_FOOT = '현금흐름표 지급액 기준 · 출처: <a href="{TENQ}" target="_blank" rel="noopener">Alphabet Q2 2026 10-Q (SEC) →</a>'
CHECK_WHEN = '2026년 10월 말 (예상) · Q3 2026'
CHECK = ['Google Cloud가 Q2 $24.8B(+82%)의 성장을 이어가고, 수주잔고 $513.9B가 매출로 바뀌는 속도가 빨라지는지',
         '설비투자가 콜에서 올린 올해 전망($195~205B) 안에서 움직이는지, 잉여현금흐름(Q2 −$5.9B)이 플러스로 돌아오는지',
         '검색 매출이 Q2 $63.3B(+17%)의 성장을 유지하는지',
         '비상장 지분 평가이익이 이번에도 순이익을 얼마나 흔드는지(Q2 영업외이익 $98.0B)']
NONOP_WHAT = '지분·장기투자'
PH = ['AAPL', 'MSFT', 'AMZN', 'NVDA']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}   # 옛 카드의 AMZN PCR 367배(축 밖)는 지금 카드 값이 작아 자르지 않는다
# 비교 막대는 각 카드의 배수 기준(build_peer_score.multiples_now) — 옛 카드는 네 종목 PER을 모두 본업 기준으로 손으로 냈다
CHART_TITLES = {'per': '빅테크 PER 비교 (GOOGL·AMZN은 본업 기준)', 'pbr': '빅테크 PBR 비교', 'psr': '빅테크 PSR 비교',
                'pcr': '빅테크 PCR(FCF) 비교', 'evebitda': '빅테크 EV/EBITDA 비교'}
PEER_NAME_TITLE = '커뮤니케이션 서비스와 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'Communication Services + Information Technology 29~33종목 대비 배수 순위 (PER 제외 네 배수)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-23 공시)'
PREMISE = '동종업 안에서는 자산 기준 배수가 싼 편이지만, <strong>자기 5년 이력으로는 PER·PSR·PCR이 비싼 쪽이고 현금흐름 내재가치는 현재가의 절반에 못 미친다.</strong>'
RISK = ('현재가가 정당하려면 5년간 매출이 매년 <strong data-vs="req">{pct(DCF[\'requiredGrowth\'])}</strong>씩 커야 한다. '
        '최근 3년 실제 성장은 연 {pct(HIST[\'growth_3y\'])}였고, AI 투자로 떨어진 투자 효율이 5년에 걸쳐 과거 평균으로 돌아온다는 가정이다.')
FUND_TIP = '순이익률은 비상장 지분 평가이익을 뺀 본업 기준((영업이익 + 순이자) × (1 − 실효세율))이다.'
SELF_TIP = 'PER은 본업 기준이다. EV/EBITDA는 감가상각 공시가 2023년부터라 이력이 {SM[\'EV/EBITDA\'][\'days\'] / 252:.1f}년뿐이다.'
PEER_TIP = ('같은 GICS 섹터(Communication Services + Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.\\nCommunication Services가 6종목뿐이라 IT 섹터를 합쳐 순위를 매겼다.'
            '\\nPER은 본업 기준이라 공시 EPS 기준인 동종업과 잣대가 달라 이 점수에서 뺐다.')
STORIES = ['지난 5년 성장 속도의 절반에서 출발해 점점 식고, 영업이익률은 지난 5년 중앙값({pct(HIST[\'margin_5y\'])})으로 내려온다. 매출 $1을 늘리는 데 ${INV[\'보수\']:.2f}를 투자한다(최근 1년 수준).',
           '지난 5년의 성장 속도로 출발해 점점 식고, 영업이익률은 최근 2년 중앙값({pct(HIST[\'margin_2y\'])})으로 서서히 내려온다. 매출 $1당 투자는 최근 1년 ${INV[\'recent\']:.2f}에서 5년에 걸쳐 과거 평균 ${INV[\'avg\']:.2f}로 돌아온다.',
           '최근 3년의 성장 속도로 출발해 점점 식고, 지금 영업이익률({pct(HIST[\'margin_now\'])})이 그대로 간다. 매출 $1당 투자는 과거 평균 ${INV[\'avg\']:.2f}다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('green', '2026년 9월 2일 — 광고기술 반독점 구제조치 판결', '2026-09-02',
     '법원이 광고 거래소(AdX) 매각 등 법무부의 구조적 구제조치를 모두 기각하고 행위 규제만 채택', 'adtech', 'Al Jazeera'),
    ('', '2026년 7월 22일 발표 · 7월 23일 반응 — Q2 2026 실적', '2026-07-23',
     '매출 $119.8B(+24%) · 클라우드 $24.8B(+82%) · 설비투자 $44.9B로 잉여현금흐름 적자', 'q2', 'Alphabet 실적 발표'),
    ('neutral', '2026년 6월 1일 발표 · 6월 2일 반응 — 주식 $80B 발행', '2026-06-02',
     'AI 인프라 재원으로 주식 $80B 발행 계획(인수 공모 $30B · ATM $40B) · 버크셔 해서웨이 $10B 사모 참여', 'equity', 'Alphabet 보도자료'),
    ('', '2026년 4월 29일 발표 · 4월 30일 반응 — Q1 2026 실적', '2026-04-30',
     '매출 $109.9B(+22%) · 클라우드 +63% · 클라우드 수주잔고 $460B 이상 · 배당 5% 인상', 'q1', 'Alphabet 실적 발표'),
    ('neutral', '2026년 3월 11일 — Wiz 인수 완료', '2026-03-11',
     '클라우드 보안 기업 Wiz를 $29.5B에 인수 완료(전날 재생에너지 개발사 Intersect $5.9B 인수 완료)', 'tenq', 'Alphabet 10-Q'),
    ('', '2026년 2월 4일 발표 · 2월 5일 반응 — Q4 2025 실적', '2026-02-05',
     '매출 $113.8B(+18%) · 연간 매출 첫 $400B 돌파 · 클라우드 +48%', 'q4', 'Alphabet 실적 발표'),
    ('', '2025년 10월 29일 발표 · 10월 30일 반응 — Q3 2025 실적', '2025-10-30',
     '첫 $100B 분기(매출 $102.3B, +16%) · EC 벌금 $3.5B 반영 · 클라우드 수주잔고 $155B', 'q3', 'Alphabet 실적 발표'),
]
SUMMARY = ('클라우드가 이끄는 성장, AI 투자 재원은 외부 조달', '우호적·투자 부담 경계',
           ['12분기 연속 매출이 두 자릿수로 늘었고 2026 Q2 매출은 $119.8B(+24%)다. 클라우드 성장률은 48% → 63% → 82%로 빨라졌다.',
            '설비투자가 Q2 $44.9B로 늘어 잉여현금흐름이 적자(−$5.9B)가 됐고, 6월에 주식 $80B 발행을 발표해 재원을 마련했다.',
            '9월 2일 광고기술 반독점 사건에서 광고 거래소 매각 청구가 기각됐다.'],
           '2026 상반기 순이익이 크게 늘어난 것은 대부분 비상장 지분 평가이익 때문이다(상반기 영업외이익 $135.7B). 실적 발표 다음날 주가가 오른 것은 네 번 중 두 번이다.',
           'Q3 2026 실적(10월 말 예상)에서 설비투자 전망($195~205B) 속에 잉여현금흐름이 플러스로 돌아오는지, 클라우드 성장이 이어지는지.')
BULL = [('클라우드', '클라우드 매출이 Q2 $24.8B(+82%)로 빨라졌고 수주잔고가 $513.9B다.'),
        ('검색', '검색 매출이 Q2 $63.3B로 1년 전보다 17% 늘었다.'),
        ('규제', '광고기술 반독점 사건에서 광고 거래소 매각 청구가 기각됐다(9월 2일).')]
BEAR = [('투자 부담', '설비투자가 Q2 $44.9B로 늘어 잉여현금흐름이 적자(−$5.9B)가 됐다.'),
        ('희석', '6월에 주식 $80B 발행을 발표했고 올해 자사주 매입을 멈췄다.'),
        ('밸류에이션', '현재가가 내재가치 기본 시나리오의 {px / DCF[\'base\']:.1f}배이고 본업 PER이 자기 5년 중 상위 {100 - SM[\'PER\'][\'percentile\']:.0f}%다.')]
ANALYST = {'rating': 'Strong Buy', 'n': 62, 'nt': 34, 'mean': 430.38, 'median': 430, 'low': 355, 'high': 515, 'sb': 44, 'b': 13, 'h': 5, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-10'
REV_FOOT = '본업 순이익 = (영업이익 + 순이자) × (1 − 그 분기 실효세율). 공시 순이익은 비상장 지분 평가이익 등 영업외이익이 들어가 2026 Q1 $62.6B·Q2 $112.2B다.'
REVERSE = ('지금 가격(<span data-dcf-price>${px:.2f}</span>)이 정당하려면 5년간 매출이 매년 <b data-dcf-req>{pct(DCF[\'requiredGrowth\'])}</b>씩 커야 한다. '
           '기본 시나리오(<span data-dcf-basev>${DCF[\'base\']:.0f}</span>)를 같은 방식으로 환산하면 연 <span data-dcf-baseeq>{pct(DCF[\'baseEquivGrowth\'])}</span>다.')

ACT_BLOCK_OLD = '    <div class="activity-grid">\n      <div class="act-card">\n        <div class="act-icon">💳</div>\n        <div><div class="act-label">매출채권 회전율·회전기간</div><div class="act-value" data-act-turn="dso">7.77회</div><div class="act-sub" data-act-sub="dso">47.0일 만에 현금화 · 직전 분기 46.7일 대비 +0.3일</div></div>\n      </div>\n      <div class="act-card">\n        <div class="act-icon">📦</div>\n        <div><div class="act-label">재고자산 회전율·회전기간</div><div class="act-value" data-act-turn="dio">50.69회</div><div class="act-sub" data-act-sub="dio">7.2일 재고 보유 · 직전 분기 7.2일 대비 ±0.0일</div></div>\n      </div>\n      <div class="act-card">\n        <div class="act-icon">🧾</div>\n        <div><div class="act-label">매입채무 회전율·지급기간</div><div class="act-value" data-act-turn="dpo">25.35회</div><div class="act-sub" data-act-sub="dpo">14.4일 만에 지급 · 직전 분기 14.5일 대비 −0.1일</div></div>\n      </div>\n      <div class="act-card">\n        <div class="act-icon">🔄</div>\n        <div><div class="act-label">영업순환주기</div><div class="act-value" data-act-days="op">54.1일</div><div class="act-sub" data-act-sub="op">재고보유+매출채권 회전기간 · 직전 분기 54.0일 대비 +0.1일</div></div>\n      </div>\n    </div>\n    <div class="ccc-card">\n      <div class="ccc-head">\n        <div class="ccc-head-label">⏱️ 현금창출주기 (CCC)</div>\n        <div class="ccc-head-value" data-act-days="ccc">39.7일</div>\n      </div>\n      <div class="ccc-explain" id="actCccExplain">재고를 사서 판매 대금을 회수하기까지 54.1일이 걸리는데, 그중 14.4일은 매입채무(외상)로 버티고 나머지 <strong style="color:var(--gold);">39.7일은 회사가 직접 현금으로 메워야</strong> 하는 기간이다. 직전 분기 39.5일보다 0.2일 길어졌다.</div>\n      <div class="tl-bar-wrap" id="actBar">\n        <div class="tl-marker" style="left: 26.6%; height: 18px;"></div>\n        <div class="tl-marker-label" style="left: 26.6%; transform: translateX(-50%);">매입채무 지급 14.4일</div>\n        <div class="tl-bar">\n          <div class="tl-seg-inv" style="width: 13.3%;">재고보유 7.2일</div>\n          <div class="tl-seg-ar" style="width: 86.9%;">매출채권회수 47.0일</div>\n        </div>\n        <div class="tl-ccc-span" style="left: 26.6%; width: 73.4%;"></div>\n      </div>\n    </div>'   # 활동성 상세(숨김 — status stale) 옛 카드 그대로, 틀(NVDA) 숫자 대신

# 카드 한정 패치 — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다(AAPL·MSFT와 같은 묶음 + 음수 FCF 칸, 자본배분 네 번째 칸).
PRE = [r'''
FR = {r_['metric']: r_['value'] for r_ in FUND['axes']['health']['rows']}
_s2 = {s_: bd.s2c_path_for(b, s_)[0] for s_ in ('보수', '기본', '낙관')}
INV = {'보수': 1 / _s2['보수'][0], 'avg': 1 / _s2['낙관'][0], 'recent': 1 / (b.get('_s2c_marginal') or _s2['낙관'][0])}
''']
POST = [r'''
sub(r'(<span class="diag-label">총자산증가율</span><span class="diag-value">)([+-])([\d.]+%</span><span class="diag-note">)' + C.FY_LABEL + r' 말 (\$[\d.]+B)\(전년 (\$[\d.]+B)\) · 연간 지표(</span>)',
    lambda m_: m_.group(1) + m_.group(2).replace('-', '−') + m_.group(3) + C.FY_LABEL + ' ' + m_.group(4) + '(전기 ' + m_.group(5) + ') · 연간 지표, ' + C.ASSET_NEXT_FY + ' 마감 전까지 동일' + m_.group(6))
one(f'<canvas id="{t}RevChart"></canvas>\n    </div>\n', f'<canvas id="{t}RevChart"></canvas>\n    </div>\n    <div class="yoy-footnote" style="margin-top:8px;">' + F(C.REV_FOOT) + '</div>\n')
one('<div class="reverse">—</div>', '<div class="reverse">' + F(C.REVERSE) + '</div>')
one('            <span class="zone-tag" style="background:rgba(240,192,64,0.18);color:var(--gold);"></span>\n', '')
sub(r'(<div class="card-title">자본배분 · 주주환원 [^<]*</div>\n      <div class="zone-list">.*?)(\n      </div>\n)',
    lambda m_: m_.group(1) + ''.join(f'\n        <div class="zone-item">\n          <span class="zone-label">{l_}</span>\n          <span class="zone-val">{v_}</span>\n        </div>' for l_, v_ in C.CAPITAL_EXTRA)
    + m_.group(2) + '      <div class="yoy-footnote" style="margin-top:14px;">' + F(C.CAPITAL_FOOT) + '</div>\n')
# 활동성이 stale이면 상세가 숨겨지지만 틀(NVDA) 숫자가 남는다 — 옛 카드 블록으로
sub(r'    <div class="activity-grid">.*?<div class="tl-ccc-span"[^>]*></div>\n      </div>\n    </div>', lambda m_: C.ACT_BLOCK_OLD)
# 음수 FCF 칸: "$-5.93B" → "−$5.93B"
one(f'<div class="stat-label">FCF ({QL})</div>\n      <div class="stat-value">$-', f'<div class="stat-label">FCF ({QL})</div>\n      <div class="stat-value">−$')
''']
