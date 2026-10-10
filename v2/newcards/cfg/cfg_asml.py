# ASML v2 카드 설정 — fill.py ASML. 회계연도 12월 31일(분기 말은 일요일, Q2 2026 = 2026-03-30~06-28). 재무는 유로(US GAAP 분기 요약, 6-K).
# 틀 시절 카드(2026-09 루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G2).
# 출처: 분기 실적 6-K 요약 재무제표(v2/adapters/asml_ifrs.py — 10-Q 없음), 2026 반기 법정보고서(6-K), 실적 보도자료(Q3 2025~Q2 2026), 주총 결과(4/22), StockAnalysis(2026-09-28).
# 통화: 배수·현금흐름 엔진은 v2/fx.py(나스닥 가격 × 그날 환율 ÷ 유로 재무). 카드의 분기 차트·FCF·Capex는 옛 카드처럼 분기 평균 ECB 환율로 달러 환산(PRE),
# 증감률은 유로 기준(POST). FCF·Capex는 옛 카드처럼 무형자산 투자까지 포함(엔진의 설비투자 태그는 유형자산만).
# 재현 모드: python3 v2/newcards/build.py ASML --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-25).
BUILD = {'feed': True}   # IFRS·유로 — EPS·재무는 adapters/asml_feed.py(build.py feed 옵션, 2026-10-05)
CIK = '0000937966'
CUR, YO, QO = '2026-06-28', '2025-06-29', '2026-03-29'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 9326.5, 'op': 3456.1, 'ni': 2917.6}   # Q2 2026 6-K US GAAP 요약 손익계산서(백만 유로)
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'ASML'
S_ = 'https://www.sec.gov/Archives/edgar/data/937966/'
SEC = S_
PR = {'q2': S_ + '000162828026048235/pressreleasefinancialresul.htm', 'q1': S_ + '000162828026025147/pressreleasefinancialresul.htm',
      'q4': S_ + '000162828026003701/pressreleasefinancialresul.htm', 'q3': S_ + '000162828025045043/pressreleasequarterlyresul.htm',
      'fs': S_ + '000162828026048235/financialstatementsusgaa.htm'}
PR_CUR = 'fs'
TENQ = S_ + '000162828026048235/statutoryinterimreport20.htm'; TENQ_NAME = '2026 반기 법정보고서'
LINKS = {'agm': S_ + '000162828026026703/asmldiscloses2026agmresults.htm'}
FAIRBAND_TITLE = 'id="asmlFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS(달러 환산) ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +{pct(HIST[\'growth_3y\'])})</span>'
OPM_RANGE, Y2 = (25, 45), (25, 45)
FCF_SUB = '€{FCF_EUR[cur] / 1e9:.2f}B · 영업현금 − 설비·무형 투자'
CAPEX_SUB = '€{CAP_EUR[cur] / 1e9:.2f}B · 설비 + 무형자산'
STAT3 = ('R&amp;D (Q2 2026)', '$1.48B', '€1.28B · 매출의 13.7%')
NEXT = ('10월 14일', '일정 · Q3 2026 (미국 장 전 발표)'); NEXT_OP = ('10월 14일', 'Q3 2026 (회사 공지)')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), '2025년'
HEALTH_NOTE = ('유동비율·당좌비율이 낮아 보이는 것은 유동부채의 대부분이 고객 선수금이기 때문이다(반기 법정보고서 IFRS 기준 유동부채 €22.4B 중 계약부채 €13.9B, US GAAP 요약은 €22.2B). '
               '차입금은 €3.7B로 모두 유로본드다(1년 안 만기 €1.7B 포함, 기업어음은 상반기에 모두 갚았다), 현금·단기투자는 €7.6B다. '
               '분기 요약 재무상태표는 유동부채를 한 줄로만 내서 유동 차입금은 반기·연말 값을 쓴다. '
               '이자보상배율은 분기 이자비용을 따로 공시하지 않아 해당 없음으로 두었다(2025년 연간 이자비용 €118M, 영업이익 €11.3B로 약 96배).')
ACT_REASON = ''
YOY_EXTRA = ''
FOOT_MID = ('US GAAP · 금액은 분기 평균 환율로 달러 환산, 증감률은 유로 기준 · FCF는 영업현금흐름 − 설비·무형자산 투자로, 고객 선수금 흐름에 따라 분기마다 크게 흔들린다(1분기 −€2.6B) · '
            '<a href="{PR[\'fs\']}" target="_blank" rel="noopener">ASML Q2 2026 US GAAP 요약 재무제표 (SEC 6-K) →</a>')
# 상반기 제품·서비스별 매출(백만 유로, 반기 법정보고서) — 분기 매출과 기간이 달라 SEG_ADJ는 PRE에서 맞춘다
SEG = [('EUV (NXE·EXE)', 7897.4, '#0f238c'), ('ArF 액침', 3331.7, '#3498db'), ('기타 DUV (ArF 건식·KrF·i-line)', 1253.0, '#7fb3e6'),
       ('계측·검사', 362.1, '#8a8fa8'), ('설치 기반 관리 (서비스·업그레이드)', 5249.2, '#f7b600')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품·서비스별'
SEG_PERIOD = '2026 상반기 · 2026.06.28까지'
SEG_NOTE = ('상반기 총매출 €18.09B(+17%) · 전년 상반기 대비 EUV +35%, ArF 액침 −23% · 시스템 매출은 로직 €6.44B·메모리 €6.40B · 지역별로 한국 39%, 대만 28%, 중국 16%(전년 24%) · 출처: '
            '<a href="{TENQ}" target="_blank" rel="noopener">ASML 2026 반기 법정보고서 (SEC 6-K) →</a>')
CAPITAL = [('자사주 매입 (Q2 2026, 현금흐름표)', '€1.08B'),
           ('남은 자사주 프로그램 (€12B, 2026~2028 · 6/28까지 약 170만 주·€2.1B 매입)', '약 €9.9B'),
           ('배당 지급 (Q2 2026, 2025년 최종배당 €2.70)', '2026 중간배당 €1.88(+17.5%)', '€1.04B')]
CHECK_WHEN = '2026년 10월 14일 · Q3 2026'
CHECK = ['3분기 매출 가이던스 €11.0~12.0B(전년 €7.5B)와 매출총이익률 55~57% 달성',
         '7월에 올린 연간 매출 €43~45B(2025년 €32.7B) 경로가 유지되는지',
         '2027년 EUV·DUV 액침 생산능력 30% 증설 계획의 진척과 설치 기반 매출(2분기 €2.76B, +32%)',
         '중국 매출 비중(상반기 16%, 전년 24%)과 수출 통제 논의의 영향']
NONOP_WHAT = '지분·장기투자'
PH = ['AMAT', 'LRCX', 'KLAC', 'TSM', 'MU', 'NVDA']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '반도체 장비·주요 고객 PER 비교', 'pbr': '반도체 장비·주요 고객 PBR 비교', 'psr': '반도체 장비·주요 고객 PSR 비교',
                'pcr': '반도체 장비·주요 고객 PCR(FCF) 비교', 'evebitda': '반도체 장비·주요 고객 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'GICS Information Technology 28종목 대비 배수 순위 (나스닥 가격 × 그날 환율 ÷ 유로 재무)'
FUND_ASOF_NOTE = 'Q2 2026 6-K US GAAP 분기 요약 (2026-07-15 공시)'
PREMISE = ('PER·PSR·EV/EBITDA가 자기 5년 이력의 상위 {max(100 - SM[k][\'percentile\'] for k in (\'PER\', \'PSR\', \'EV/EBITDA\')):.0f}% 안이라 {selfsc:.1f}점이고, IT 28종목 안에서도 비싼 쪽({peersc:.1f}점)이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다. '
           '과거 5년 성장(연 {pct(HIST[\'growth_5y\'])})과 영업이익률 30%대가 이어진다는 가정으로는 현재가에 한참 못 미친다.')
RISK = ('현재가가 정당하려면 5년간 매출이 매년 <strong data-vs="req">{pct(DCF[\'requiredGrowth\'])}</strong>씩 커야 한다(최근 3년 실제 연 {pct(HIST[\'growth_3y\'])}). '
        '회사의 2026년 가이던스(€43~45B)는 한 해 +32~38%다. 낙관 시나리오(최근 3년 성장)가 기본보다 낮게 나오는 것은 최근 3년 성장률이 5년 값보다 낮아서다.')
FUND_TIP = ('재무는 유로(US GAAP)다. ASML은 10-Q를 내지 않아 분기 실적 6-K의 요약 재무제표를 읽는다(v2/adapters/asml_ifrs.py). '
            '유동 차입금은 반기·연말에만 공시돼 1·3분기는 직전 값을 쓰고, 이자보상배율은 분기 이자비용이 없어 결측(점수에서 뺌, 2025년 약 96배)으로 두었다.')
SELF_TIP = '나스닥 가격을 그날 환율(ECB 기준환율)로 유로로 바꿔 유로 재무로 나눈 배수다. PER은 5년 상위 {100 - SM[\'PER\'][\'percentile\']:.0f}%, PSR은 상위 {math.ceil(100 - SM[\'PSR\'][\'percentile\'])}%, EV/EBITDA는 상위 {100 - SM[\'EV/EBITDA\'][\'percentile\']:.0f}%다.'
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다. ASML은 나스닥 가격을 그날 환율로 유로로 바꿔 유로 재무로 나눴다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(연 {pct(HIST[\'growth_3y\'])})에서 출발하고 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다. 5년 뒤 매출 약 €49B.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('', '2026년 7월 15일 미국 장 전 — Q2 2026 실적', '2026-07-15',
     '매출 €9.3B(+21%)·매출총이익률 54.0%·순이익 €2.9B · 연간 매출 가이던스를 €43~45B로 상향(4월 €36~40B) · 2027년 EUV·DUV 액침 생산능력 30% 증설 계획', 'q2', 'ASML 실적 보도자료 (SEC 6-K)'),
    ('neutral', '2026년 4월 22일 — 주주총회', None,
     '2025년 최종배당 €2.70 승인(연간 €7.50, +17%) · 발행주식 10% 이내 자사주 매입·소각 권한 · 감독이사 Benjamin Loh 선임', 'agm', 'ASML 주총 결과 (SEC 6-K)'),
    ('', '2026년 4월 15일 미국 장 전 — Q1 2026 실적', '2026-04-15',
     '매출 €8.8B(+13%)·매출총이익률 53.0% · 연간 매출 가이던스를 €36~40B로 상향(1월 €34~39B) · 수출 통제 논의 결과를 범위에 반영했다고 밝힘', 'q1', 'ASML 실적 보도자료 (SEC 6-K)'),
    ('', '2026년 1월 28일 미국 장 전 — Q4 2025 실적', '2026-01-28',
     '분기 매출 €9.7B(사상 최대, High NA 2대 포함) · 순수주 €13.2B(EUV €7.4B)·수주잔고 €38.8B · 2026~2028 자사주 €12B · 기술·IT 조직 간소화', 'q4', 'ASML 실적 보도자료 (SEC 6-K)'),
    ('', '2025년 10월 15일 미국 장 전 — Q3 2025 실적', '2025-10-15',
     '매출 €7.5B·매출총이익률 51.6% · 2026년 매출이 2025년보다 낮지 않을 것, 중국 매출은 크게 줄 것으로 예상 · Mistral AI 제휴(20-F 기준 €1.3B 투자, 지분 약 11%)', 'q3', 'ASML 실적 보도자료 (SEC 6-K)'),
]
SUMMARY = ('AI 투자로 EUV 수요가 늘어 올해 가이던스를 두 번 올렸다', '성장 가속·밸류 부담',
           ['2026년 매출 가이던스가 1월 €34~39B에서 4월 €36~40B, 7월 €43~45B로 올라갔다(2025년 €32.7B).',
            '상반기 EUV 시스템 매출이 €7.9B로 35% 늘어 DUV 액침 감소(−23%)를 메웠다. 2분기 영업이익률은 37.1%다.',
            '2027년 저NA EUV 생산능력을 올해 약 65대에서, DUV 액침을 약 130대에서 각각 30% 늘릴 계획이다.'],
           '중국 매출이 상반기 €2.9B로 22% 줄었고(비중 24% → 16%), 수출 통제 논의가 이어지고 있다. 고객 선수금 흐름 때문에 1분기 영업현금흐름이 −€2.2B였다.',
           'Q3 2026 실적(10월 14일)의 매출 €11.0~12.0B 가이던스 달성과 연간 €43~45B 경로, 2027년 증설 계획.')
BULL = [('수익성', '최근 4분기 영업이익률이 {pct(HIST[\'margin_now\'])}, 2분기는 37.1%로 올라왔다.'),
        ('성장', '올해 매출 가이던스 €43~45B는 지난해보다 32~38% 많고, 7월에 두 번째로 올렸다.'),
        ('주주환원', '2026~2028 자사주 €12B 프로그램을 시작했고, 중간배당을 €1.60에서 €1.88로 올렸다.')]
BEAR = [('밸류', '기본 내재가치가 현재가의 {DCF[\'base\'] / px * 100:.0f}%이고, PER이 자기 5년 이력의 상위 {100 - SM[\'PER\'][\'percentile\']:.0f}%다.'),
        ('중국', '상반기 중국 매출이 22% 줄었고, 회사는 수출 통제 논의를 가이던스 범위의 변수로 꼽았다.'),
        ('현금흐름', '선수금 흐름에 따라 분기 영업현금이 +€11.4B(2025년 4분기)에서 −€2.2B(2026년 1분기)까지 흔들린다.')]
ANALYST = {'rating': 'Strong Buy', 'n': 42, 'nt': 7, 'mean': 2354.7, 'median': 2400, 'low': 1650, 'high': 2873.87, 'sb': 31, 'b': 6, 'h': 4, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-10'

# 유로 재무 → 카드 표시(fill.py 1. 헤더 전에 exec): 무형자산 투자를 Capex에 더하고, 분기 값은 분기 평균 환율로 달러 환산. 증감률용 유로 값은 따로 둔다.
PRE = [r'''
import fx as _fx, statistics as _st
_ia = q(['PaymentsToAcquireIntangibleAssets'])
cap = {k: cap[k] + _ia.get(k, 0) for k in cap}
fcf = {k: ocf[k] - cap[k] for k in ocf if k in cap}
FCF_EUR, CAP_EUR = dict(fcf), dict(cap)
_E = {'rev': dict(rev), 'op': dict(op), 'ni': dict(ni_chart), 'fcf': dict(fcf)}
_fx.rate('ASML', C.CUR); _ds, _vs = _fx._load('EUR')
_qe = sorted(rev)
def _avg(k):
    p_ = max(x for x in _qe if x < k)
    return _st.mean([v for d_, v in zip(_ds, _vs) if p_ < d_ <= k])
_R = {k: _avg(k) for k in ks}
rev = dict(rev); op = dict(op); ni_chart = dict(ni_chart)
for _d in (rev, op, ni_chart, fcf, cap):
    for k in ks:
        if k in _d:
            _d[k] = _d[k] / _R[k]
yd_e = [f_(_E['rev'][cur], _E['rev'][yo]), f_(_E['op'][cur], _E['op'][yo]), f_(_E['ni'][cur], _E['ni'][yo]), f_(_E['fcf'].get(cur), _E['fcf'].get(yo))]
qd_e = [f_(_E['rev'][cur], _E['rev'][qo]), f_(_E['op'][cur], _E['op'][qo]), f_(_E['ni'][cur], _E['ni'][qo]), f_(_E['fcf'].get(cur), _E['fcf'].get(qo))]
C.SEG_ADJ = rev[cur] / 1e6 - sum(v for _, v, _ in C.SEG)   # 상반기 유로 구성 vs 분기 달러 매출 — 기간·통화가 달라 검사를 건너뛴다
''']
# fill.py의 증감 함수(f)는 PRE 뒤에 정의되므로 같은 식을 여기 둔다
PRE[0] = "f_ = lambda a, b_: '—' if a is None or b_ is None else ('흑자 전환' if a > 0 else '적자 지속') if b_ <= 0 else ('적자 전환' if a <= 0 else ('약 %.0f배' % (a / b_) if a / b_ >= 10 else ('0.0%' if abs(a / b_ - 1) < 0.0005 else '%+.1f%%' % ((a / b_ - 1) * 100))))\n" + PRE[0]

# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
POST = [r'''
# 헤더: 상장 형태·재무 통화(옛 카드)
one('NASDAQ(ADR) · 정보기술 · 반도체장비 · 🇳🇱 네덜란드</span>', 'NASDAQ(등록 보통주, ADR 아님) · 정보기술 · 반도체장비 · 🇳🇱 네덜란드 · 재무 유로(US GAAP)</span>')
# 역산 문장: 성장 모드는 틀이 빈칸(—)으로 둔다 — 옛 카드의 문장 틀(값은 카드 JS가 data-dcf-* 칸에 채운다)
one('<div class="reverse">—</div>', '<div class="reverse">지금 가격(<span data-dcf-price>$' + f'{px:.2f}' + '</span>)이 정당하려면 5년간 매출이 매년 <b data-dcf-req>' + pct(DCF['requiredGrowth']) + '</b>씩 커야 한다. 기본 시나리오(<span data-dcf-basev>$' + f"{DCF['base']:.0f}" + '</span>)를 같은 방식으로 환산하면 연 <span data-dcf-baseeq>' + pct(DCF['baseEquivGrowth']) + '</span>다.</div>')
# 분기 차트 아래 설명(환산·4분기 계절성)
one('<canvas id="asmlRevChart"></canvas>\n    </div>\n', '<canvas id="asmlRevChart"></canvas>\n    </div>\n'
    '    <div class="yoy-footnote" style="margin-top:8px;">US GAAP 유로 실적을 분기 평균 환율(ECB 기준환율)로 달러 환산했다. 4분기가 큰 것은 연말 출하(2025년 4분기 High NA 2대 매출 인식)가 몰려서다.</div>\n')
# 매입채무 미공시 설명: 반기·연말에만 공시(옛 카드)
assert h.count('분기 매입채무를 따로 공시하지 않아') >= 2   # JS 두 곳(정적 대체값은 sync_fallbacks가 렌더에서 다시 쓴다)
h = h.replace('분기 매입채무를 따로 공시하지 않아', '매입채무를 분기마다 공시하지 않아(반기·연말만)')
# 이자보상배율 메모(분기 이자비용 미공시)
one('"note": "이자비용 태그 없음", "label": "이자보상배율"', '"note": "분기 이자비용 미공시 · 2025년 약 96배", "label": "이자보상배율"')
# 증감률은 유로 기준(옛 카드)
one(f"deltas: [{tq(yd)}],", f"deltas: [{tq(yd_e)}],")
one(f"deltas: [{tq(qd)}],", f"deltas: [{tq(qd_e)}],")
# YoY·QoQ 각주: US GAAP·환율 설명과 6-K 요약 재무제표 링크
_fm = F(C.FOOT_MID)
h, _n = re.subn(r"(footnote: '기준일: [^']*?\) vs [^']*?\) · )GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · <a href=\"[^\"]*\" target=\"_blank\" rel=\"noopener\">[^<]*</a>'", lambda m: m.group(1) + _fm + "'", h)
assert _n == 2, _n
# 재무 건전성 메모 링크 이름(SEC 6-K)
one(f'{C.TENQ_NAME} (SEC) →</a></div>', f'{C.TENQ_NAME} (SEC 6-K) →</a></div>')
# 총자산증가율 메모(유로)
one(f'<span class="diag-note">{C.FY_LABEL} 말 ${a1 / 1000:.1f}B(전년 ${a0 / 1000:.1f}B) · 연간 지표</span>', f'<span class="diag-note">{C.FY_LABEL} 말 €{a1 / 1000:.1f}B(전년 €{a0 / 1000:.1f}B) · 연간 지표, 2026년 마감 전까지 동일</span>')
# 매출 구성: 상반기 유로(제목 기간, 범례·툴팁 통화)
one(f'<div class="card-title">{C.SEG_TITLE} ({QL} · {C.CUR.replace("-", ".")} 기준)</div>', f'<div class="card-title">{C.SEG_TITLE} ({C.SEG_PERIOD})</div>')
for _n_, _v, _c in C.SEG:
    one(f'{_n_} <strong style="color:var(--text);">${_v / 1000:.2f}B · ', f'{_n_} <strong style="color:var(--text);">€{_v / 1000:.2f}B · ')
one("return `${ctx.label}: $${(ctx.raw/1000).toFixed(1)}B (${pct}%)`;", "return `${ctx.label}: €${(ctx.raw/1000).toFixed(1)}B (${pct}%)`;   // 유로 그대로(Codex)")
sub(r'// ─── 매출 구성 도넛 차트 \([^)]*\) ───', '// ─── 매출 구성 도넛 차트 (2026 상반기, 백만 유로) ───')
# 기본적 분석 툴팁: 분기 자료는 6-K 요약
one(f"분기({QL}, 10-Q), 성장률은", f"분기({QL}, 6-K 분기 요약), 성장률은")
''']
