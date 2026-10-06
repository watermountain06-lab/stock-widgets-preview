# LLY(일라이 릴리) v2 카드 설정 — fill.py LLY. 회계연도 12월 31일. 루트 카드 있음.
# 틀 시절 카드(루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05), 실적 보도자료(Q3 2025~Q2 2026), 8-K(회사채 5/20), StockAnalysis(2026-09-27).
# 엔진: 10-Q 손익계산서에 영업이익 줄이 없어 영업이익 = 세전이익 − 영업외손익, 이자비용 분기 태그가 끊겨 v2/interest_extra.json — build_multiple_history.
# 재현 모드: python3 v2/newcards/build.py LLY --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-25).
CIK = '0000059478'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 22974}   # Q2 2026 보도자료 매출(제품 합, 백만 달러)
VOTES, VERDICT = (1, -1, -2), '적정~고평가'
CO = 'Lilly'
S_ = 'https://www.sec.gov/Archives/edgar/data/59478/'
SEC = S_
PR = {'q2': S_ + '000005947826000077/q226lillysalesandearningsp.htm', 'q1': S_ + '000005947826000043/q126lillysalesandearningsp.htm',
      'q4': S_ + '000005947826000008/q425lillysalesandearningsp.htm', 'q3': S_ + '000005947825000251/q325lillysalesandearningsp.htm'}
PR_CUR = 'q2'
TENQ = ''; TENQ_NAME = 'Q2 2026 10-Q'   # 옛 카드는 건전성 메모에 10-Q 링크가 없었다(자본배분 각주에 있다) — POST에서 링크를 뺀다
TENQ_CF = S_ + '000005947826000081/lly-20260630.htm'
LINKS = {'notes': S_ + '000119312526232707/d148580d8k.htm'}
PRE = [r'''
FR = {r['metric']: r['value'] for ax in FUND['axes'].values() for r in ax['rows']}
LO2 = math.ceil(round(max(SM[k_]['percentile'] for k_ in ('PER', 'EV/EBITDA')), 1))   # PER·EV/EBITDA 중 높은 백분위의 '하위 N% 안'(올림)
''']
FAIRBAND_TITLE = 'id="llyFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +{HIST[\'growth_3y\'] * 100:.1f}%)</span>'
OPM_RANGE, Y2 = (0, 60), (0, 60)
FCF_SUB = '현금창출력'
CAPEX_SUB = '미래 재투자'
STAT3 = ('R&amp;D (Q2 2026)', '$3.82B', '기술 경쟁력 투자')
NEXT = ('10월 말 예상', '일정 · Q3 2026'); NEXT_OP = ('10월 말', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY25'
HEALTH_NOTE = ('차입금이 연초 $42.5B에서 $54.9B로 늘었다. 5월에 회사채 $9.0B를 발행했고, 상반기 인수에 현금 $9.8B를 썼다. '
               '자기자본이 $33.9B로 작아 부채비율이 {FR[\'debtToEquity\']:.0f}%다. 이자비용 분기 태그가 2025년 9월 분기 뒤로 끊겨, '
               '이자보상배율은 10-Q 부문 주석의 2분기 이자비용 $345M을 손으로 넣어 계산했다(약 {FR[\'interestCoverage\']:.0f}배).')
ACT_REASON = ''
YOY_EXTRA = ''
OPNOTE = ('영업이익은 세전이익 − 영업외손익(10-Q 손익계산서에 영업이익 줄이 없다, 보도자료 값과 같음) · '
          'FCF는 영업현금흐름 − 설비투자(비GAAP)이며 투자활동으로 잡히는 IPR&D 매입 현금은 빠져 있다 · ')
SEG = [('Mounjaro', 9943, '#d52b1e'), ('Zepbound', 4928, '#f07b72'), ('기타 핵심 제품 6종', 835, '#f0c040'), ('그 밖의 제품', 7268, '#94a3b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품별'
SEG_NOTE = ('전년 대비 Mounjaro +91%, Zepbound +46% · 기타 핵심 제품은 Jaypirca·Ebglyss·Kisunla·Omvoh·Inluriyo·Foundayo · '
            '출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Lilly Q2 2026 실적 보도자료 (SEC 8-K) →</a>')
# 자본배분 칸은 옛 카드처럼 네 줄 + 각주(POST가 통째로 바꾼다 — 생성기 틀은 세 줄)
CAPITAL = [('자사주 매입', '$3.96B'), ('배당 지급', '$3.09B'), ('배당 지급', '', '$3.09B')]
CAPITAL_ZONES = '      <div class="zone-list">\n        <div class="zone-item">\n          <span class="zone-label">인수 (현금, 인수한 회사 현금 차감)</span>\n          <span class="zone-val">$9.81B</span>\n        </div>\n        <div class="zone-item">\n          <span class="zone-label">임상 단계 신약 권리 매입 (IPR&amp;D)</span>\n          <span class="zone-val">$3.49B</span>\n        </div>\n        <div class="zone-item">\n          <span class="zone-label">자사주 매입</span>\n          <span class="zone-val">$3.96B</span>\n        </div>\n        <div class="zone-item">\n          <span class="zone-label">배당 지급</span>\n          <span class="zone-val">$3.09B</span>\n        </div>\n      </div>\n      <div class="yoy-footnote" style="margin-top:14px;">IPR&amp;D 매입은 현금흐름표에선 투자, 손익계산서에선 즉시 비용이다 · 설비투자 $5.26B는 별도 · 5월에 회사채 $9.0B 발행 · 출처: <a href="{C.TENQ_CF}" target="_blank" rel="noopener">Lilly Q2 2026 10-Q 현금흐름표 →</a></div>\n'   # 옛 카드에서 스크립트로 옮김
CHECK_WHEN = '2026년 10월 말 (예상) · Q3 2026'
CHECK = ['연간 매출 가이던스 $85.0~87.0B에 맞춰 가는지 (상반기 $42.8B)',
         '실현 가격 하락 폭 (2분기 전 세계 −13%, 미국 −3%, 미국 밖 −36%)',
         '먹는 비만약 Foundayo의 매출 (2분기 $98M)',
         '사들인 임상 단계 신약 권리(IPR&amp;D)의 비용 처리가 3분기에도 이익을 크게 깎는지 (2분기 $2.8B, 주당 $3.03)']
NONOP_WHAT = '지분·장기투자'
PH = ['ABBV', 'JNJ', 'MRK', 'PFE', 'BMY', 'AMGN']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '대형 제약 PER 비교', 'pbr': '대형 제약 PBR 비교', 'psr': '대형 제약 PSR 비교',
                'pcr': '대형 제약 PCR(FCF) 비교', 'evebitda': '대형 제약 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 헬스케어 섹터(S&amp;P500 59종목)보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 59종목 대비 배수 순위(v2/peer_universe/health_care.json)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-08-05 공시)'
PREMISE = ('자기 5년 이력으로는 PER·EV/EBITDA가 하위 {LO2}% 안이라 싼 편이지만, S&P500 헬스케어 59종목 안에서는 다섯 배수 모두 비싼 쪽(동종업 {peersc:.1f}점)이고, '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다. '
           '기본 시나리오는 성장률이 5년 평균(연 {HIST[\'growth_5y\'] * 100:.0f}%)에서 식고 최근 4분기 영업이익률({pct(HIST[\'margin_now\'])})이 최근 2년 중앙값({pct(HIST[\'margin_2y\'])})으로 내려온다고 본다.')
RISK = ('영업이익률에는 자산 인수·라이선스로 사들인 임상 단계 신약 권리(IPR&amp;D)의 즉시 비용 처리분(2분기 $2.8B)이 들어 있어 분기마다 크게 흔들린다. '
        '현재가가 정당하려면 5년간 매출이 매년 <strong data-vs="req">{pct(DCF[\'requiredGrowth\'])}</strong>씩 커야 한다(최근 3년 실제 연 {pct(HIST[\'growth_3y\'])}).')
FUND_TIP = ('영업이익은 세전이익 − 영업외손익으로 만든 값이다(10-Q 손익계산서에 영업이익 줄이 없다, 보도자료 값과 같다). '
            '이자보상배율은 이자비용 분기 태그가 끊겨 10-Q 부문 주석 값($345M)을 손으로 넣었다(v2/interest_extra.json). '
            'FCF에는 투자활동으로 잡히는 IPR&D 매입 현금이 빠져 있어 PCR이 그만큼 낮게 나온다.')
SELF_TIP = ('PER {SM[\'PER\'][\'current\']:.1f}배·EV/EBITDA {SM[\'EV/EBITDA\'][\'current\']:.1f}배가 5년 중 하위 {LO2}% 안이다. 5년 사이 이익이 매출보다 빨리 늘어 배수가 내려왔다. '
            '주식 수는 직원복리신탁 보유 50M주를 뺀 값(891M)이다.')
PEER_TIP = ('S&P500 헬스케어 59종목과 배수 순위를 매긴 값이다(카드 유니버스엔 헬스케어가 7종목뿐이라 넓혔다).',
            '제약·바이오·의료기기·유통·관리의료가 섞여 있다. 매출 배수는 마진이 얇은 유통·보험사가 크게 낮다.')
STORIES = ['5년 성장률의 절반(연 {HIST[\'growth_5y\'] / 2 * 100:.0f}%)에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 내려간다.',
           '5년 성장률(연 {HIST[\'growth_5y\'] * 100:.0f}%)에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 내려간다.',
           '3년 성장률(연 {HIST[\'growth_3y\'] * 100:.0f}%)에서 출발하고 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다. 5년 뒤 매출 약 $200B.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('', '2026년 8월 5일 개장 전 — Q2 2026 실적', '2026-08-05',
     '매출 $23.0B(+48%) · 연간 가이던스 $85~87B로 상향 · EPS $7.94(IPR&amp;D 비용 $2.8B, 주당 $3.03 반영)', 'q2', 'Lilly 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 20일 — 회사채 $9.0B 발행 완료', None,
     '2028~2066년 만기 변동·고정금리 사채 8종 $9.0B 발행', 'notes', 'Lilly 공시 (SEC 8-K)'),
    ('', '2026년 4월 30일 개장 전 — Q1 2026 실적', '2026-04-30',
     '매출 $19.8B(+56%) · 먹는 비만약 Foundayo FDA 승인 · 연간 가이던스 $82~85B로 상향 · 4건 인수 합의', 'q1', 'Lilly 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 2월 4일 개장 전 — Q4 2025 실적', '2026-02-04',
     '매출 $19.3B(+43%) · 2026 가이던스 $80~83B · 미국 정부와 비만약 접근 확대 합의', 'q4', 'Lilly 실적 보도자료 (SEC 8-K)'),
    ('', '2025년 10월 30일 개장 전 — Q3 2025 실적', '2025-10-30',
     '매출 $17.60B(+54%) · 연간 가이던스 $63.0~63.5B로 상향 · Inluriyo FDA 승인', 'q3', 'Lilly 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('비만·당뇨약 두 제품이 성장을 끌고, 인수로 다음 성장을 산다', '고성장·가격 하락',
           ['매출 성장률이 네 분기 동안 54% → 43% → 56% → 48%였다. 2분기 Mounjaro $9.9B(+91%)와 Zepbound $4.9B(+46%)가 매출의 65%다.',
            '판매량은 60% 늘었지만 실현 가격은 13% 내렸다. 미국 밖은 중국 보험 약가 목록(NRDL) 등재 등으로 36% 내렸다.',
            '2분기에 4곳을 인수했고 분기 뒤 3곳을 더 인수했다. 사들인 신약 권리(IPR&amp;D) 비용 $2.8B가 2분기 EPS에 주당 $3.03 반영됐다.'],
           '두 제품 의존도가 높고 가격은 계속 내려간다. 인수에 쓴 돈이 늘어 차입금이 연초 $42.5B에서 $54.9B가 됐다.',
           'Q3 2026 실적(10월 말 예상)에서 연간 가이던스 $85~87B 경로, 가격 하락 폭, Foundayo 매출.')
BULL = [('수요', '2분기 판매량이 60% 늘었고 올해 매출 가이던스를 두 번 올렸다.'),
        ('파이프라인', 'Foundayo가 승인됐고 retatrutide는 2027년 1분기 미국 허가 신청을 계획한다.'),
        ('마진', '2분기 매출총이익률이 85.8%로 1년 전보다 1.5%p 올랐다.')]
BEAR = [('가격', '2분기 실현 가격이 13% 내렸고 미국 밖은 36% 내렸다.'),
        ('집중', 'Mounjaro와 Zepbound가 2분기 매출의 65%다.'),
        ('사업개발 비용', 'IPR&amp;D 비용이 2분기 $2.8B로 이익을 흔들고, 인수로 차입금이 $54.9B로 늘었다.')]
ANALYST = {'rating': 'Buy', 'n': 30, 'nt': 22, 'mean': 1359.91, 'median': 1400, 'low': 940, 'high': 1600, 'sb': 19, 'b': 6, 'h': 3, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-05'

# 현재가 역산 문장(성장 모드) — 생성기는 틀 문장을 지우고 '—'만 남긴다(JS는 마진 모드만 문장을 쓴다). 옛 카드 문장을 되살린다(JS가 data-dcf-* 칸을 채운다).
REVERSE = ('지금 가격(<span data-dcf-price>${px:.2f}</span>)이 정당하려면 5년간 매출이 매년 <b data-dcf-req>{pct(DCF[\'requiredGrowth\'])}</b>씩 커야 한다. '
           '기본 시나리오(<span data-dcf-basev>${DCF[\'base\']:.0f}</span>)를 같은 방식으로 환산하면 연 <span data-dcf-baseeq>{pct(DCF[\'baseEquivGrowth\'])}</span>다.')
REQ_MULT_EXACT = False   # 옛 카드는 틀 문구("3배를 넘는다") 그대로
POST = [r'''
# 현재가 역산 문장(성장 모드)
one('<div class="reverse">—</div>', '<div class="reverse">' + F(C.REVERSE) + '</div>')
# 건전성 메모: 옛 카드에는 10-Q 링크가 없었다
one(' <a href="" target="_blank" rel="noopener">Q2 2026 10-Q (SEC) →</a></div>', '</div>')
# 두 각주 모두 영업이익 산식·FCF 설명(옛 카드 그대로)
assert h.count('GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · ') == 2
h = h.replace('GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · ', 'GAAP 기준 · ' + C.OPNOTE)
# 총자산증가율 메모 꼬리
one("(전년 $78.7B) · 연간 지표</span>", "(전년 $78.7B) · 연간 지표, FY26 마감 전까지 동일</span>")
# 자본배분: 상반기 누계 네 줄 + 각주(옛 카드 그대로)
one('<div class="card-title">자본배분 · 주주환원 (Q2 2026 · 2026.06.30 기준)</div>', '<div class="card-title">자본배분 · 주주환원 (2026년 상반기 · 2026.06.30 기준)</div>')
# 애널리스트 중앙값 미공개(null) — 옛 카드의 null 안전·천 단위 쉼표 usd(카드 한정)
one("  const usd = v => '$' + (Number.isInteger(v) ? v : v.toFixed(2));", "  const usd = v => v == null ? '—' : '$' + (Number.isInteger(v) ? v.toLocaleString('en-US') : v.toFixed(2));")
sub(r'(?<=자본배분 · 주주환원 \(2026년 상반기 · 2026\.06\.30 기준\)</div>\n)      <div class="zone-list">\n.*?\n      </div>\n(?=    </div>\n  </div>\n\n  <!-- ══════════ 6\.)', F(C.CAPITAL_ZONES))
''']
