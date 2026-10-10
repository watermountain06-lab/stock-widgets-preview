# AMZN(아마존) v2 카드 설정 — fill.py AMZN. 회계연도 12월 31일. 시총 상위(루트 카드 있음). 본업 기준 종목(core_earnings.json — Anthropic 등 투자 평가이익).
# 틀 시절 카드(2026-09-24 루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G1).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-31), 실적 보도자료(Q3 2025~Q2 2026), 8-K(기간대출 6/10, Globalstar 4/14, OpenAI 2/27), StockAnalysis(2026-09-21).
# 재현 모드: python3 v2/newcards/build.py AMZN --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-23).
BUILD = {}
CIK = '0001018724'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 200606, 'op': 27461, 'ni': 62647}   # Q2 2026 손익(백만 달러, 공시 순이익) — SEC XBRL, 옛 카드(매출 $200.6B, 공시 순이익 $62.6B)와 같다
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Amazon'
S_ = 'https://www.sec.gov/Archives/edgar/data/1018724/'
SEC = S_
PR = {'q2': S_ + '000101872426000024/amzn-20260630xex991.htm', 'q1': S_ + '000101872426000012/amzn-20260331xex991.htm',
      'q4': S_ + '000101872426000002/amzn-20251231xex991.htm', 'q3': S_ + '000101872425000121/amzn-20250930xex991.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000101872426000026/amzn-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'loan': S_ + '000110465926072140/tm2613616d4_8k.htm', 'globalstar': S_ + '000110465926042880/tm2611746d1_ex99-1.htm',
         'openai': S_ + '000110465926021050/tm267374d1_ex99-1.htm'}
FAIRBAND_TITLE = 'id="amznFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 EPS ${eps_ttm}(본업 기준, 10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (5, 16), (8, 16)
FCF_SUB = '현금창출력'
CAPEX_SUB = '미래 재투자'
STAT3 = ('기술·인프라 비용 (Q2 2026)', '$33.2B', 'AWS·AI 인프라 포함')
NEXT = ('10월 말 예상', '일정 · Q3 2026'); NEXT_OP = ('10월 말', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY25'
ASSET_NEXT_FY = 'FY26'
HEALTH_NOTE = ('유동비율 {FR[\'currentRatio\']:.1f}%·당좌비율 {FR[\'quickRatio\']:.1f}%로 단기 지급 여력은 빠듯한 편이고, 부채비율은 {FR[\'debtToEquity\']:.1f}%다. '
               'AI 투자 재원을 차입으로도 조달해 6월에 은행 기간대출 계약을, 9월에 파운드화 회사채 £4.25B를 발행했다(8-K).')
ACT_REASON = ''
YOY_EXTRA = ''
SEG = [('북미', 116200, '#ffb74d'), ('AWS', 42200, '#3498db'), ('해외', 42200, '#8a6d3b')]
SEG_ADJ = 6   # 옛 카드 도넛은 부문 매출을 $0.1B 단위로 적었다(합 200,600 대 보고 매출 200,606)
SEG_TITLE = '매출 구성 — 사업 부문'
SEG_NOTE = ('출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Amazon Q2 2026 실적발표 (SEC 8-K) →</a> · '
            '영업이익은 AWS $16.6B · 북미 $9.1B · 해외 $1.7B')
CAPITAL = [('설비투자 (Q2 2026)', '$54.2B'),
           ('OpenAI 투자 약정 (2월, 초기 $15B)', '$50B'),
           ('배당 · 자사주 매입', '', '없음')]
CAPITAL_FOOT = '주주환원 대신 AI 인프라와 지분 투자에 쓴다 · 출처: <a href="{TENQ}" target="_blank" rel="noopener">Amazon Q2 2026 10-Q (SEC) →</a>'
CHECK_WHEN = '2026년 10월 말 (예상) · Q3 2026'
CHECK = ['매출($197.0~202.0B, +9~12%)과 영업이익($22.5~26.5B) 전망을 달성하는지',
         'AWS가 Q2 +37%(18분기 만에 최고)의 성장을 이어가는지',
         '설비투자(Q2 $54.2B)로 최근 4분기 잉여현금흐름 −$11.6B(설비투자 총액 차감, 회사 발표 기준으로는 −$7.6B)가 바뀌는지',
         'Anthropic·OpenAI 투자 평가이익이 이번에도 순이익을 얼마나 흔드는지(Q2 영업외이익 $53.4B)']
NONOP_WHAT = '지분·장기투자'
PH = ['AAPL', 'MSFT', 'GOOGL', 'NVDA']
PEER_FILE = None
CHART_CAP, SELF_CAP = {}, {}
CHART_NOTE = {'pcr': ' (AMZN은 FCF 적자로 계산 불가)'}
# 비교 막대는 각 카드의 배수 기준(build_peer_score.multiples_now) — 옛 카드는 2026-09-23 루트 카드 일봉으로 직접 계산했다
CHART_TITLES = {'per': '빅테크 PER 비교 (AMZN·GOOGL은 본업 기준)', 'pbr': '빅테크 PBR 비교', 'psr': '빅테크 PSR 비교',
                'pcr': '빅테크 PCR(FCF) 비교', 'evebitda': '빅테크 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 경기소비재 섹터와 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'GICS 경기소비재 + IT 섹터 대비 배수 순위 (본업 기준 PER은 제외, 네 배수)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-31 공시)'
PREMISE = ('배수로는 동종업 {peersc:.1f}점·자기 5년 이력 {selfsc:.1f}점으로 둘 다 중앙값보다 싼 쪽이지만, <strong>현금흐름 내재가치는 현재가에 크게 못 미친다.</strong> '
           '설비투자가 매출의 {b[\'capex\'] / b[\'revenue\'] * 100:.1f}%로 영업현금흐름을 넘어서 최근 4분기 잉여현금흐름이 마이너스다. '
           '자본수익률이 할인율에 가까워 과거 성장으로는 가격이 설명되지 않고, 가격에는 마진 확대 기대가 담겨 있다.')
RISK = ('매출이 지난 5년 속도(연 {pct(HIST[\'growth_5y\'])})로 크다가 식는다면, 현재가가 정당하려면 영업이익률이 <strong data-vs="req">{pct(DCF[\'requiredMargin\'])}</strong>여야 한다(지금 {pct(HIST[\'margin_now\'])}). '
        '성장만으로 맞추려면 연 {pct(DCF[\'requiredGrowth\'])}가 필요해, 가격은 성장보다 마진 확대에 거는 기대로 읽힌다(AWS 영업이익률은 Q2 39%).')
FUND_TIP = '순이익률은 본업 기준이다(Anthropic 등 투자 평가이익 제외).'
SELF_TIP = 'PBR·EV/EBITDA·PER은 5년 중 싼 쪽이다. PCR은 최근 4분기 잉여현금흐름이 적자라 계산되지 않아 0점으로 셌다.'
PEER_TIP = ('GICS 경기소비재 섹터에 IT 섹터를 더해 배수 순위를 매긴 값이다.',
            'PER은 본업 기준이라 공시 기준인 다른 종목과 섞지 않고 빼서 네 배수를 평균했다.')
STORIES = ['지난 5년 성장 속도의 절반에서 출발해 점점 식고, 영업이익률은 지난 5년 중앙값({pct(HIST[\'margin_5y\'])})으로 내려온다. 매출 $1을 늘리는 데 ${INV[\'보수\']:.2f}를 투자한다(최근 1년 수준).',
           '지난 5년의 성장 속도로 출발해 점점 식고, 영업이익률은 최근 2년 중앙값({pct(HIST[\'margin_2y\'])})으로 서서히 내려온다. 매출 $1당 투자는 최근 1년 ${INV[\'recent\']:.2f}에서 5년에 걸쳐 과거 평균 ${INV[\'avg\']:.2f}로 돌아온다.',
           '최근 3년의 성장 속도로 출발해 점점 식고, 지금 영업이익률({pct(HIST[\'margin_now\'])})이 그대로 간다. 매출 $1당 투자는 과거 평균 ${INV[\'avg\']:.2f}다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('', '2026년 7월 30일 발표 · 7월 31일 반응 — Q2 2026 실적', '2026-07-31',
     '매출 $200.6B(+20%)로 가이던스 상단 $199.0B 상회 · AWS $42.2B(+37%, 18분기 만에 최고) · 순이익 $62.6B에 Anthropic 중심 영업외이익 $53.4B 포함', 'q2', 'Amazon 실적 발표 (SEC)'),
    ('neutral', '2026년 6월 10일 공시 — $17.5B 기간대출 계약', '2026-06-10',
     '씨티은행 등과 무담보 기간대출 $17.5B 계약(6월 8일 체결) · 3월 달러·유로, 6월 캐나다달러 회사채에 이은 차입', 'loan', 'Amazon 8-K (SEC)'),
    ('', '2026년 4월 29일 발표 · 4월 30일 반응 — Q1 2026 실적', '2026-04-30',
     '매출 $181.5B(+17%)로 가이던스 상단 $178.5B 상회 · AWS $37.6B(+28%) · 순이익 $30.3B에 Anthropic 평가이익 $16.8B 포함', 'q1', 'Amazon 실적 발표 (SEC)'),
    ('neutral', '2026년 4월 14일 — Globalstar 인수 합의', '2026-04-14',
     '위성통신 Globalstar를 주당 $90(현금 또는 주식)에 인수 · Amazon Leo에 휴대폰 직접 연결 서비스 추가, 아이폰 위성 서비스도 맡기로 · 2027년 완료 예정', 'globalstar', 'Amazon 보도자료 (SEC)'),
    ('green', '2026년 2월 27일 — OpenAI 전략적 제휴', '2026-02-27',
     'OpenAI에 $50B 투자(초기 $15B) · OpenAI가 AWS에서 Trainium 2GW 사용, 기존 $38B 계약을 8년간 $100B 확대 · AWS가 OpenAI Frontier 외부 유통 담당', 'openai', 'Amazon·OpenAI 보도자료 (SEC)'),
    ('', '2026년 2월 5일 발표 · 2월 6일 반응 — Q4 2025 실적', '2026-02-06',
     '매출 $213.4B(+14%)로 가이던스 상단 $213.0B 상회 · AWS $35.6B(+24%) · 이탈리아 세금 분쟁·감원·매장 손상 등 특별비용 3건 반영', 'q4', 'Amazon 실적 발표 (SEC)'),
    ('', '2025년 10월 30일 발표 · 10월 31일 반응 — Q3 2025 실적', '2025-10-31',
     '매출 $180.2B(+13%) · AWS $33.0B(+20%) · FTC 합의금 $2.5B·감원 비용 $1.8B로 영업이익 $17.4B 제자리, 순이익 $21.2B에 Anthropic 평가이익 $9.5B 포함', 'q3', 'Amazon 실적 발표 (SEC)'),
]
SUMMARY = ('AWS 성장이 다시 빨라지고, AI 투자는 차입으로도 조달한다', '우호적·재무 부담 경계',
           ['세 분기 연속 매출이 직전 가이던스 상단을 넘었다. AWS 성장률은 전년 대비 20% → 24% → 28% → 37%로 빨라졌다.',
            '2월 OpenAI와 제휴하며 $50B 투자를 약정했고, OpenAI는 AWS에서 Trainium 2GW를 쓰기로 했다.',
            '공시 순이익은 Anthropic 지분 평가이익으로 크게 부풀었다(Q2 영업외이익 $53.4B). 이 카드는 본업 순이익으로 평가한다.'],
           '설비투자(Q2 $54.2B)가 영업현금흐름을 넘어 최근 4분기 잉여현금흐름이 −$11.6B다(설비투자 총액 차감). 지난 11월부터 달러·유로·캐나다달러·파운드 회사채와 $17.5B 기간대출로 차입을 늘렸다.',
           'Q3 2026 실적(10월 말 예상)에서 매출 전망 $197.0~202.0B를 넘는지, AWS 성장이 이어지는지, 잉여현금흐름이 플러스로 돌아서는지.')
BULL = [('AWS 가속', 'AWS 성장률이 네 분기 연속 빨라져 +37%가 됐고, Q2 영업이익 $27.5B 중 $16.6B를 벌었다.'),
        ('마진', '영업이익률이 Q3 2025 {op[\'2025-09-30\'] / rev[\'2025-09-30\'] * 100:.1f}%에서 Q2 2026 {op[\'2026-06-30\'] / rev[\'2026-06-30\'] * 100:.1f}%로 올랐다.'),
        ('AI 계약', 'OpenAI가 AWS 계약을 8년간 $100B 늘리고 Trainium 2GW를 쓰기로 했다.')]
BEAR = [('현금흐름', '설비투자가 영업현금흐름을 넘어 최근 4분기 잉여현금흐름이 −$11.6B다(설비투자 총액 차감).'),
        ('차입', 'AI 투자 재원을 회사채와 $17.5B 기간대출로도 조달해 부채비율이 {FR[\'debtToEquity\']:.1f}%다.'),
        ('이익의 질', 'Q2 공시 순이익 $62.6B에 Anthropic 중심 투자 평가이익 $53.4B(세전)가 들어 있어 지분 가치에 따라 크게 흔들린다.')]
ANALYST = {'rating': 'Strong Buy', 'n': 60, 'nt': 45, 'mean': 331.29, 'median': 330, 'low': 230, 'high': 400, 'sb': 42, 'b': 16, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-10'
REV_FOOT = '본업 순이익 = (영업이익 + 순이자) × (1 − 그 분기 실효세율). 공시 순이익은 Anthropic 등 투자 평가이익이 들어가 2026 Q1 $30.3B·Q2 $62.6B다.'

# 카드 한정 패치 — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다(AAPL·MSFT·GOOGL과 같은 묶음).
PRE = [r'''
FR = {r_['metric']: r_['value'] for r_ in FUND['axes']['health']['rows']}
_s2 = {s_: bd.s2c_path_for(b, s_)[0] for s_ in ('보수', '기본', '낙관')}
INV = {'보수': 1 / _s2['보수'][0], 'avg': 1 / _s2['낙관'][0], 'recent': 1 / (b.get('_s2c_marginal') or _s2['낙관'][0])}
''']
POST = [r'''
sub(r'(<span class="diag-label">총자산증가율</span><span class="diag-value">)([+-])([\d.]+%</span><span class="diag-note">)' + C.FY_LABEL + r' 말 (\$[\d.]+B)\(전년 (\$[\d.]+B)\) · 연간 지표(</span>)',
    lambda m_: m_.group(1) + m_.group(2).replace('-', '−') + m_.group(3) + C.FY_LABEL + ' ' + m_.group(4) + '(전기 ' + m_.group(5) + ') · 연간 지표, ' + C.ASSET_NEXT_FY + ' 마감 전까지 동일' + m_.group(6))
one(f'<canvas id="{t}RevChart"></canvas>\n    </div>\n', f'<canvas id="{t}RevChart"></canvas>\n    </div>\n    <div class="yoy-footnote" style="margin-top:8px;">' + F(C.REV_FOOT) + '</div>\n')
one('            <span class="zone-tag" style="background:rgba(240,192,64,0.18);color:var(--gold);"></span>\n', '')
sub(r'(<div class="card-title">자본배분 · 주주환원 [^<]*</div>\n      <div class="zone-list">.*?\n      </div>\n)', lambda m_: m_.group(1) + '      <div class="yoy-footnote" style="margin-top:14px;">' + F(C.CAPITAL_FOOT) + '</div>\n')
# QoQ FCF 증감 문구: 둘 다 적자면 틀은 '적자 지속' — 옛 카드는 적자 폭이 준 것을 '적자 축소'로 적었다
if fcf[cur] < 0 and fcf[qo] < 0 and fcf[cur] > fcf[qo]:
    sub(r"(curLabel: '" + QL + r"', cmpLabel: '" + C.QQL + r"',.*?deltas: \[[^\]]*)'적자 지속'\]", lambda m_: m_.group(1) + "'적자 축소']")
# 음수 FCF 칸
one(f'<div class="stat-label">FCF ({QL})</div>\n      <div class="stat-value">$-', f'<div class="stat-label">FCF ({QL})</div>\n      <div class="stat-value">−$')
# 동종업 툴팁 둘째 줄: 옛 카드 문장(PER 제외는 셋째 줄이 설명)
h = h.replace('`\\n배수마다 "나보다 싼 종목이 몇 %인가"를 뒤집어 점수로 썼고 PER를 뺀 4개를 평균했다.`', '`\\n배수마다 "나보다 싼 종목이 몇 %인가"를 뒤집어 점수로 썼다.`', 1)
''']
