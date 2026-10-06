# MRK(머크) v2 카드 설정 — fill.py MRK. 회계연도 12월 31일. 루트 카드 있음.
# 틀 시절 카드(루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-07), 실적 보도자료(Q3 2025~Q2 2026), StockAnalysis(2026-09-29).
# 엔진: 손익계산서에 영업이익 줄이 없어 영업이익 = 세전이익 − 기타(수익)비용 순액(DERIVED_OPINC) — build_multiple_history.
# 재현 모드: python3 v2/newcards/build.py MRK --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-29).
CIK = '0000310158'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 16607}   # Q2 2026 매출(제품군 합, 백만 달러)
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Merck'
S_ = 'https://www.sec.gov/Archives/edgar/data/310158/'
SEC = S_
PR = {'q2': S_ + '000110465926090045/tm2621496d1_ex99-1.htm', 'q1': S_ + '000110465926052081/tm2612241d1_ex99-1.htm',
      'q4': S_ + '000110465926009495/tm264564d1_ex99-1.htm', 'q3': S_ + '000110465925103974/tm2529620d1_ex99-1.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000031015826000212/mrk-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {}
PRE = [r'''
FR = {r['metric']: r['value'] for ax in FUND['axes'].values() for r in ax['rows']}
''']
FAIRBAND_TITLE = ('id="mrkFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}. '
                  '이 EPS에는 인수 IPR&D 일회성 비용(주당 $5.93)이 들어 있어 밴드가 현재가보다 훨씬 낮게 잡힌다 — 빼면 EPS 약 $7.18."')
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (-30, 50), (-30, 50)
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('R&amp;D (Q2 2026)', '$9.74B', 'Terns 인수 IPR&D $5.7B 포함')
NEXT = ('10월 말 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('10월 말', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), '2025년'
HEALTH_NOTE = ('유동비율 {FR[\'currentRatio\']:.1f}%다. 차입금은 $53.9B(1년 안 만기·단기 $2.8B + 장기 $51.1B)이고 현금·단기투자는 $7.1B다. '
               '2025년 9월·12월과 2026년 5월에 사채를 발행했고, 현금은 연초 $14.6B에서 줄었다. 이자보상배율 1점은 인수 IPR&D 때문에 2분기 합성 영업이익이 적자(−${-op[cur] / 1e9:.2f}B)라서다.')
ACT_REASON = ''
YOY_EXTRA = ''
OPNOTE = '영업이익은 세전이익 − 기타(수익)비용 순액 · 2분기 영업이익·순이익에는 Terns 인수 IPR&D $5.7B(주당 $2.31) 포함 · '
SEG = [('키트루다(QLEX 포함)', 8367, '#00857c'), ('그 밖의 의약품·백신', 6393, '#3498db'), ('동물 건강', 1775, '#f7b600'), ('기타', 72, '#9b59b6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품군별 매출'
SEG_NOTE = ('키트루다 한 제품이 매출의 절반이다 · 성장 제품: 윈레브에어 $588M(+75%), 가다실 $1.17B(+4%), 동물 건강 +8% · '
            '출처: <a href="{TENQ}" target="_blank" rel="noopener">Q2 2026 10-Q (SEC) →</a>, <a href="{PR[\'q2\']}" target="_blank" rel="noopener">보도자료</a>')
CAPITAL = [('자사주 매입 (2026년 상반기)', '$1.6B'),
           ('잔여 바이백 승인 한도 (2026.06.30 기준, 2026년 약 $3.0B 매입 예정)', '$5.7B'),
           ('배당 (Q2 2026 선언)', '분기 $0.85(2025년 11월 $0.81에서 인상)', '$2.1B')]
CHECK_WHEN = '2026년 10월 말 (예상) · Q3 2026'
CHECK = ['연간 전망(매출 $66.3~67.3B, 비GAAP EPS $2.66~2.76 — Cidara 주당 $3.62·Terns 주당 $2.43 비용 포함) 유지 여부',
         '매출의 절반인 키트루다와 피하주사형 키트루다 QLEX(2분기 $463M) 전환 속도',
         '새 제품(윈레브에어 +75%, 새로 승인된 리프펜드라·이드빈소)의 매출 기여',
         '추가 자산 인수와 그에 따른 R&D 일회성 비용 — 2026년 상반기 두 건 $14.7B(대부분 IPR&D)']
NONOP_WHAT = '지분·장기투자'
PH = ['LLY', 'JNJ', 'ABBV', 'PFE', 'BMY', 'AMGN']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '대형 제약 PER 비교', 'pbr': '대형 제약 PBR 비교', 'psr': '대형 제약 PSR 비교',
                'pcr': '대형 제약 PCR(FCF) 비교', 'evebitda': '대형 제약 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&amp;P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-08-07 공시)'
PREMISE = ('<strong>세 칸 모두 인수 IPR&D 일회성 비용(1년 안 두 건, 주당 $5.93)의 영향을 크게 받는다.</strong> '
           '최근 4분기 EPS는 ${eps_ttm}라 PER {SM[\'PER\'][\'current\']:.0f}배로 자기 5년 이력({selfsc:.1f}점)·S&P500 헬스케어({peersc:.1f}점) 모두 비싼 쪽이지만, '
           '두 비용을 빼면 EPS 약 $7.18, PER 약 {px / 7.18:.0f}배로 5년 중앙값({SM[\'PER\'][\'median\']:.0f}배) 근처다. PSR·PBR은 비용과 무관하게 5년 상위 {math.ceil(100 - min(SM[\'PSR\'][\'percentile\'], SM[\'PBR\'][\'percentile\']))}% 안이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다. 주가는 1년 새 {ch:.0f}% 올랐다.')
RISK = ('현재가가 정당하려면 영업이익률이 <strong data-vs="req">{pct(DCF[\'requiredMargin\'])}</strong>여야 한다. '
        '최근 4분기 {pct(HIST[\'margin_now\'])}는 IPR&D 비용 때문에 낮고, 최근 2년 중앙값은 {pct(HIST[\'margin_2y\'])}다. '
        '낙관 시나리오가 음수인 것은 IPR&D로 눌린 마진 {pct(HIST[\'margin_now\'])}를 영구히 쓰기 때문이고, 보수 시나리오도 음수인 것은 최근 1년 인수 현금 $18.8B가 투자로 잡혀 매출/자본이 0.18로 낮아서다. '
        '기본 시나리오도 {pct(HIST[\'margin_now\'])}에서 출발해 5년에 걸쳐 회복하므로 IPR&D 영향이 섞여 있다 — 마진을 처음부터 2년 중앙값으로 두어도 약 $55~62(현재가의 37~41%)라 판정은 같다. '
        '규칙대로 GAAP 이익을 쓰고 일회성 비용을 빼지 않았다(2026-09-30 결정).')
FUND_TIP = '영업이익률·순이익률·이자보상배율이 각 1점인 것은 2분기 Terns 인수 IPR&D $5.7B 때문이다(그 분기만의 일회성 비용). 영업이익 줄이 없어 세전이익에서 기타(수익)비용을 되돌려 만들었다.'
SELF_TIP = ('PER {SM[\'PER\'][\'current\']:.0f}배·EV/EBITDA {SM[\'EV/EBITDA\'][\'current\']:.0f}배는 인수 IPR&D로 이익이 눌린 값이다(두 비용을 빼면 PER 약 {px / 7.18:.0f}배). '
            'PSR {SM[\'PSR\'][\'current\']:.1f}배·PBR {SM[\'PBR\'][\'current\']:.1f}배는 5년 상위 {math.ceil(100 - min(SM[\'PSR\'][\'percentile\'], SM[\'PBR\'][\'percentile\']))}% 안이다.')
PEER_TIP = ('S&P500 헬스케어와 배수 순위를 매긴 값이다(카드 유니버스 헬스케어가 적어 넓혔다).',
            '제약·바이오·의료기기·보험·서비스가 섞여 있다. 머크의 PER·EV/EBITDA는 인수 IPR&D 비용이 든 값이라 가장 비싼 쪽으로 나온다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(연 {pct(HIST[\'growth_3y\'])})에서 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}(IPR&D로 눌린 값)가 이어진다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('', '2026년 8월 4일 장 전 — Q2 2026 실적', '2026-08-04',
     '매출 $16.6B(+5%)·GAAP 주당 −$0.54(Terns 인수 비용 $2.31 포함) · 키트루다 $8.4B · 윈레브에어 +75% · 연간 매출 전망 $66.3~67.3B로 좁히며 상향 · 리프펜드라 FDA 승인', 'q2', 'Merck 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 4월 30일 장 전 — Q1 2026 실적', '2026-04-30',
     '매출 $16.3B(+5%)·GAAP 주당 −$1.72(Cidara 인수 비용 $3.62 포함) · Terns 인수 계획 · 이드빈소(HIV) FDA 승인', 'q1', 'Merck 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 2월 3일 장 전 — Q4 2025 실적', '2026-02-03',
     '2025년 매출 $65.0B(+1%)·GAAP EPS $7.28(비GAAP $8.98) · Verona·Cidara 인수로 포트폴리오 전환', 'q4', 'Merck 실적 보도자료 (SEC 8-K)'),
    ('', '2025년 10월 30일 장 전 — Q3 2025 실적', '2025-10-30',
     '매출 $17.3B(+4%)·GAAP EPS $2.32(비GAAP $2.58) · Verona Pharma 인수 완료', 'q3', 'Merck 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('연이은 신약 인수로 GAAP 이익은 적자가 났지만 주가는 1년 새 크게 올랐다', '인수·전환기',
           ['2026년 1·2분기에 Cidara($9.0B)·Terns($5.7B)를 인수하며 개발 중 신약 비용을 한 번에 처리해 두 분기 모두 GAAP 적자였다.',
            '매출은 분기마다 약 5% 늘었고, 키트루다가 매출의 절반이다. 윈레브에어(+75%)와 새 승인 제품이 뒤를 받친다.',
            '주가는 1년 새 {ch:.0f}% 올랐고, 8월 말 고점(종가 $156.45)보다 {(1 - px / 156.45) * 100:.0f}% 낮다.'],
           '이 카드의 PER·EV/EBITDA·내재가치는 일회성 인수 비용이 든 GAAP 이익을 쓴다. 비용을 빼면 PER은 약 {px / 7.18:.0f}배다.',
           'Q3 2026 실적(10월 말 예상)의 연간 전망 유지, 키트루다 QLEX 전환, 추가 인수.')
BULL = [('성장', '매출이 분기마다 약 5% 늘었고, 7월에 연간 매출 전망을 좁히며 올렸다.'),
        ('신제품', '윈레브에어 2분기 $588M(+75%), 리프펜드라·이드빈소가 새로 승인됐다.'),
        ('환원', '분기 배당 $0.85, 상반기 자사주 $1.6B.')]
BEAR = [('집중', '키트루다 한 제품이 매출의 50%다.'),
        ('인수 비용', '2026년 상반기 두 건의 인수로 R&D 일회성 비용 $14.7B(대부분 IPR&D)를 처리했고, 차입금이 $53.9B로 늘었다.'),
        ('밸류', 'PSR·PBR이 5년 상위 {math.ceil(100 - min(SM[\'PSR\'][\'percentile\'], SM[\'PBR\'][\'percentile\']))}% 안이고 기본 내재가치는 현재가의 {DCF[\'base\'] / px * 100:.0f}%다.')]
ANALYST = {'rating': 'Buy', 'n': 28, 'nt': 22, 'mean': 161.16, 'median': 170, 'low': 105, 'high': 180, 'sb': 15, 'b': 5, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-05'

# 옛 카드 끝의 음수 표기 정리 스크립트(카드 한정 — 틀 JS가 "$-12"·"-6.5%"로 찍던 것, INTC 카드에도 있다)
NEG_FIX_JS = '<script>\n// 음수 표기 정리(카드 한정, 틀 과제) — 틀 JS가 음수 금액·비율을 "$-12", "-6.5%"로 찍는다. 텍스트 노드만 바꾸고 날짜(2026-06-27)는 건드리지 않는다.\n(function(){\n  const RX1 = /\\$-(\\d)/g, RX2 = /(^|[\\s(~·])-(\\d)/g;\n  const fix = root => {\n    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);\n    let n;\n    while ((n = w.nextNode())) {\n      const p = n.parentElement && n.parentElement.tagName;\n      if (p === \'SCRIPT\' || p === \'STYLE\') continue;\n      const t = n.textContent;\n      if (t.indexOf(\'-\') < 0) continue;\n      const u = t.replace(RX1, \'−$$$1\').replace(RX2, \'$1−$2\');\n      if (u !== t) n.textContent = u;\n    }\n  };\n  const run = () => fix(document.body);\n  run();\n  new MutationObserver(run).observe(document.body, {childList: true, subtree: true, characterData: true});\n})();\n</script>\n'
REQ_MULT_EXACT = True   # 옛 카드는 "지난 5년의 N배다"
POST = [r'''
# 분기 차트 아래 설명(IPR&D 적자)
one('<canvas id="mrkRevChart"></canvas>\n    </div>\n', '<canvas id="mrkRevChart"></canvas>\n    </div>\n'
    '    <div class="yoy-footnote" style="margin-top:8px;">2026년 1·2분기 적자는 두 건의 자산 인수에서 산 개발 중 신약(IPR&D)을 한 번에 R&D 비용으로 처리해서다(회사가 밝힌 인수 관련 R&D 일회성 비용, 대부분 IPR&D) — 1분기 Cidara(독감 예방 항바이러스 MK-1406, $9.0B), 2분기 Terns(백혈병 치료 후보 MK-4208, $5.7B)(10-Q). 영업이익 줄이 없어 세전이익에서 기타(수익)비용을 되돌려 만들었다.</div>\n')
# 두 각주 모두 영업이익 산식·IPR&D 설명(옛 카드 그대로)
assert h.count('GAAP 기준 · FCF는 영업현금흐름') == 2
h = h.replace('GAAP 기준 · FCF는 영업현금흐름', 'GAAP 기준 · ' + C.OPNOTE + 'FCF는 영업현금흐름')
# 총자산증가율 메모(Verona 인수)·꼬리
one('</script>\n</body>', '</script>\n' + C.NEG_FIX_JS + '</body>')
one("(전년 $117.1B) · 연간 지표</span>", "(전년 $117.1B, Verona 인수 반영) · 연간 지표, 2026년 마감 전까지 동일</span>")
''']
