# MSFT(마이크로소프트) v2 카드 설정 — fill.py MSFT. 회계연도 6월 30일(Q4 FY26 = 2026-06-30, 최신 공시는 FY26 10-K). 시총 상위(루트 카드 있음).
# 틀 시절 카드(2026-09-24 루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G1).
# 출처: SEC XBRL, FY26 10-K(2026-07-29), 실적 보도자료(Q1~Q4 FY26), 8-K(부문 개편 9/2), Microsoft 공식 블로그(OpenAI), StockAnalysis(2026-09-22).
# 재현 모드: python3 v2/newcards/build.py MSFT --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-23).
BUILD = {}
CIK = '0000789019'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
RELEASE = {'rev': 90007, 'op': 40603, 'ni': 35766}   # Q4 FY26 손익(백만 달러) — SEC XBRL, 옛 카드 뉴스(매출 $90.0B)와 같다
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Microsoft'
S_ = 'https://www.sec.gov/Archives/edgar/data/789019/'
SEC = S_
PR = {'q4': S_ + '000119312526323632/msft-ex99_1.htm', 'q3': S_ + '000119312526191457/msft-ex99_1.htm',
      'q2': S_ + '000119312526027198/msft-ex99_1.htm', 'q1': S_ + '000119312525256310/msft-ex99_1.htm'}
PR_CUR = 'q4'
TENQ = S_ + '000119312526323660/msft-20260630.htm'; TENQ_NAME = 'FY26 10-K'
LINKS = {'seg': S_ + '000119312526380280/d291965dex991.htm',
         'openai2': 'https://blogs.microsoft.com/blog/2026/04/27/the-next-phase-of-the-microsoft-openai-partnership/',
         'openai1': 'https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/'}
FAIRBAND_TITLE = 'id="msftFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +{HIST[\'growth_3y\'] * 100:.1f}%)</span>'
OPM_RANGE, Y2 = (40, 52), (40, 52)
FCF_SUB = '현금창출력'
CAPEX_SUB = '미래 재투자'
STAT3 = ('R&amp;D (Q4 FY26)', '$10.0B', '기술 경쟁력 투자')
NEXT = ('10월 말 예상', '일정 · Q1 FY27'); NEXT_OP = ('10월 말', 'Q1 FY27 예상')
FY_ENDS, FY_LABEL = ('2026-06-30', '2025-06-30'), 'FY26'
ASSET_NEXT_FY = 'FY27'
HEALTH_NOTE = ('유동비율은 기준보다 낮지만 차입금의존도 {FR[\'debtDependency\']:.1f}%, 이자보상배율 {FR[\'interestCoverage\']:.0f}배로 상환 부담은 작다. '
               '데이터센터 확충을 금융리스로도 조달해 금융리스 부채가 $66.6B다(FY26 10-K).')
ACT_REASON = ''
YOY_EXTRA = ''
SEG = [('Intelligent Cloud', 39300, '#3498db'), ('Productivity and Business Processes', 37800, '#a2c3fa'), ('More Personal Computing', 12900, '#5c6282')]
SEG_ADJ = 7   # 옛 카드 도넛은 부문 매출을 $0.1B 단위로 적었다(합 90,000 대 보고 매출 90,007)
SEG_TITLE = '매출 구성 — 사업 부문'
SEG_NOTE = ('출처: <a href="{PR[\'q4\']}" target="_blank" rel="noopener">Microsoft Q4 FY26 실적발표 (SEC 8-K) →</a> · Azure +43% · '
            'FY27부터 두 부문(Agents and Infra / Devices and Consumer)으로 개편')
CAPITAL = [('자사주 매입 (Q4 FY26)', '$4.6B'),
           ('잔여 매입 승인 한도 ($60B 중)', '$40.6B'),
           ('배당 (Q4 FY26 · 주당 $0.91)', '', '$6.8B')]
CAPITAL_FOOT = '현금흐름표 지급액 기준(자사주 매입에 임직원 원천징수분 포함) · 출처: <a href="{TENQ}" target="_blank" rel="noopener">Microsoft FY26 10-K (SEC) →</a>'
CHECK_WHEN = '2026년 10월 말 (예상) · Q1 FY2027'
CHECK = ['매출이 회사 전망($89.85~90.95B, 9월 2일 새 부문 기준으로 조정)을 달성하는지',
         'Azure가 Q4 +43%의 성장을 이어가고, 상업용 잔여 수행의무 $678B(+84%)가 매출로 바뀌는 속도',
         '설비투자(Q4 $35.8B, 금융리스 별도)가 잉여현금흐름(Q4 $19.6B)을 더 깎는지',
         '새 두 부문(Agents and Infra / Devices and Consumer)으로 처음 내는 실적에서 사업별 수익성이 어떻게 보이는지']
NONOP_WHAT = '지분·장기투자'
PH = ['AAPL', 'GOOGL', 'AMZN', 'NVDA']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}   # 옛 카드의 AMZN PCR 367배(축 밖)는 지금 카드 값이 작아 자르지 않는다
CHART_TITLES = {'per': '빅테크 PER 비교 (GOOGL·AMZN은 본업 기준)', 'pbr': '빅테크 PBR 비교', 'psr': '빅테크 PSR 비교',
                'pcr': '빅테크 PCR(FCF) 비교', 'evebitda': '빅테크 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'GICS Information Technology 23~27종목 대비 배수 순위'
FUND_ASOF_NOTE = 'FY26 10-K (2026-07-29 공시) — 4분기는 10-Q가 없어 연간 기간을 쓴다'
PREMISE = ('배수로는 동종업·자기 5년 이력 모두 중간이지만, <strong>현금흐름 내재가치는 현재가의 절반에 못 미친다.</strong> '
           '설비투자가 매출의 {b[\'capex\'] / b[\'revenue\'] * 100:.0f}%라 현금흐름이 이익을 따라가지 못한다.')
RISK = ('현재가가 정당하려면 5년간 매출이 매년 <strong data-vs="req">{pct(DCF[\'requiredGrowth\'])}</strong>씩 커야 한다. '
        '최근 3년 실제 성장은 연 {pct(HIST[\'growth_3y\'])}였고, AI 투자로 떨어진 투자 효율이 5년에 걸쳐 과거 평균으로 돌아온다는 가정이다.')
FUND_TIP = '6월 결산이라 최신 기간이 FY26 연간(10-K)이다.'
SELF_TIP = 'PCR만 5년 중 가장 비싼 쪽(상위 {100 - SM[\'PCR\'][\'percentile\']:.0f}%)이고 PER·PBR·PSR·EV/EBITDA는 하위 쪽이다 — 설비투자로 현금흐름이 줄어서다.'
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['지난 5년 성장 속도의 절반에서 출발해 점점 식고, 영업이익률은 지난 5년 중앙값({pct(HIST[\'margin_5y\'])})으로 내려온다. 매출 $1을 늘리는 데 ${INV[\'보수\']:.2f}를 투자한다(최근 1년 수준).',
           '지난 5년의 성장 속도로 출발해 점점 식고, 영업이익률은 최근 2년 중앙값({pct(HIST[\'margin_2y\'])})으로 서서히 내려온다. 매출 $1당 투자는 최근 1년 ${INV[\'recent\']:.2f}에서 5년에 걸쳐 과거 평균 ${INV[\'avg\']:.2f}로 돌아온다.',
           '최근 3년의 성장 속도로 출발해 점점 식고, 지금 영업이익률({pct(HIST[\'margin_now\'])})이 그대로 간다. 매출 $1당 투자는 과거 평균 ${INV[\'avg\']:.2f}다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 2일 발표 · 9월 3일 반응 — 사업 부문 개편', '2026-09-03',
     'FY27부터 세 부문을 두 부문(Agents and Infra / Devices and Consumer)으로 개편, 과거 실적 재작성', 'seg', 'Microsoft 발표 자료'),
    ('', '2026년 7월 29일 발표 · 7월 30일 반응 — Q4 FY26 실적', '2026-07-30',
     '매출 $90.0B(+18%) · Azure +43% · FY26 Azure 매출 첫 $100B 돌파', 'q4', 'Microsoft 실적 발표'),
    ('', '2026년 4월 29일 발표 · 4월 30일 반응 — Q3 FY26 실적', '2026-04-30',
     '매출 $82.9B(+18%) · Azure +40% · AI 사업 연환산 매출 $37B(+123%)', 'q3', 'Microsoft 실적 발표'),
    ('neutral', '2026년 4월 27일 — OpenAI 계약 개정', '2026-04-27',
     'OpenAI 모델 독점 사용권 종료 · Microsoft의 수익 배분 지급 중단(OpenAI의 지급은 2030년까지 상한 내 유지)', 'openai2', 'Microsoft 공식 블로그'),
    ('', '2026년 1월 28일 발표 · 1월 29일 반응 — Q2 FY26 실적', '2026-01-29',
     '매출 $81.3B(+17%) · Azure +39%(직전 +40%) · 순이익 +60%(OpenAI 영향 제외 시 +23%)', 'q2', 'Microsoft 실적 발표'),
    ('', '2025년 10월 29일 발표 · 10월 30일 반응 — Q1 FY26 실적', '2025-10-30',
     '매출 $77.7B(+18%) · Azure +40% · 영업이익 +24%', 'q1', 'Microsoft 실적 발표'),
    ('neutral', '2025년 10월 28일 — OpenAI 재편 합의', '2025-10-28',
     'OpenAI 공익법인 전환에 합의, Microsoft 지분 약 27%(약 $135B) · OpenAI의 Azure 추가 구매 $250B', 'openai1', 'Microsoft 공식 블로그'),
]
SUMMARY = ('Azure 성장이 설비투자를 따라잡는지', '중립·투자 부담 경계',
           ['매 분기 매출이 17~18% 늘었고 Azure 성장률은 40% → 39% → 40% → 43%로 FY26 말에 빨라졌다. FY26 Azure 매출은 처음 $100B를 넘었다.',
            'OpenAI와의 관계가 두 번 바뀌었다. 2025년 10월에 지분 약 27%로 재편됐고, 2026년 4월에 독점 관계가 끝났다.',
            '9월 2일 FY27부터 사업 부문을 두 개(Agents and Infra / Devices and Consumer)로 바꾼다고 발표했다.'],
           '실적 다음날 반응이 −10.0%(1월)에서 +15.5%(7월)까지 크게 흔들렸고, 6월 한 달 주가는 −17.2%로 최근 5년 중 가장 많이 떨어졌다.',
           'Q1 FY27 실적(10월 말 예상)에서 매출이 전망($89.85~90.95B)을 넘는지, Azure 성장이 이어지는지.')
BULL = [('Azure', 'Azure 성장률이 Q4 +43%로 빨라졌고 FY26 Azure 매출이 처음 $100B를 넘었다.'),
        ('수주', '상업용 잔여 수행의무가 $678B로 1년 새 84% 늘었다.'),
        ('AI 매출', 'AI 사업의 연환산 매출이 $37B로 1년 새 123% 늘었다(Q3 FY26).')]
BEAR = [('투자 부담', '설비투자가 Q4 $35.8B(금융리스 별도)로 늘어 잉여현금흐름이 1년 새 23% 줄었다.'),
        ('OpenAI', '4월 계약 개정으로 OpenAI 모델 독점 사용권이 끝났다.'),
        ('밸류에이션', '현재가가 내재가치 기본 시나리오의 {px / DCF[\'base\']:.1f}배다.')]
ANALYST = {'rating': 'Strong Buy', 'n': 55, 'nt': 35, 'mean': 579.21, 'median': 575, 'low': 440, 'high': 725, 'sb': 39, 'b': 14, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-05'
REV_FOOT = '6월 결산 · Q2 FY26 순이익에는 영업외이익 $10.0B가 들어 있다(영업이익 $38.3B).'   # 분기 차트 아래(옛 카드 그대로)
REVERSE = ('지금 가격(<span data-dcf-price>${px:.2f}</span>)이 정당하려면 5년간 매출이 매년 <b data-dcf-req>{pct(DCF[\'requiredGrowth\'])}</b>씩 커야 한다. '
           '기본 시나리오(<span data-dcf-basev>${DCF[\'base\']:.0f}</span>)를 같은 방식으로 환산하면 연 <span data-dcf-baseeq>{pct(DCF[\'baseEquivGrowth\'])}</span>다.')   # 성장 모드 역산 문장(JS가 칸을 채운다)

# 카드 한정 패치 — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다(AAPL과 같은 묶음).
PRE = [r'''
FR = {r_['metric']: r_['value'] for r_ in FUND['axes']['health']['rows']}
_s2 = {s_: bd.s2c_path_for(b, s_)[0] for s_ in ('보수', '기본', '낙관')}
INV = {'보수': 1 / _s2['보수'][0], 'avg': 1 / _s2['낙관'][0], 'recent': 1 / (b.get('_s2c_marginal') or _s2['낙관'][0])}
''']
POST = [r'''
sub(r'(<span class="diag-label">총자산증가율</span><span class="diag-value">)([+-])([\d.]+%</span><span class="diag-note">)' + C.FY_LABEL + r' 말 (\$[\d.]+B)\(전년 (\$[\d.]+B)\) · 연간 지표(</span>)',
    lambda m_: m_.group(1) + m_.group(2).replace('-', '−') + m_.group(3) + C.FY_LABEL + ' ' + m_.group(4) + '(전기 ' + m_.group(5) + ') · 연간 지표, ' + C.ASSET_NEXT_FY + ' 마감 전까지 동일' + m_.group(6))
# 분기 차트 아래 설명, 성장 모드 역산 문장(fill.py는 '—'만 남긴다 — 마진 모드만 JS가 문장을 쓴다)
one(f'<canvas id="{t}RevChart"></canvas>\n    </div>\n', f'<canvas id="{t}RevChart"></canvas>\n    </div>\n    <div class="yoy-footnote" style="margin-top:8px;">' + F(C.REV_FOOT) + '</div>\n')
one('<div class="reverse">—</div>', '<div class="reverse">' + F(C.REVERSE) + '</div>')
one('            <span class="zone-tag" style="background:rgba(240,192,64,0.18);color:var(--gold);"></span>\n', '')
sub(r'(<div class="card-title">자본배분 · 주주환원 [^<]*</div>\n      <div class="zone-list">.*?\n      </div>\n)', lambda m_: m_.group(1) + '      <div class="yoy-footnote" style="margin-top:14px;">' + F(C.CAPITAL_FOOT) + '</div>\n')
''']
