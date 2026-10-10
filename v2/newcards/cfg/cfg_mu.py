# MU(마이크론) v2 카드 설정 — fill.py MU. 회계연도는 8월 말 목요일 무렵(Q3 FY26 = 2026-02-27~05-28). 시총 루트 카드 있음.
# 틀 시절 카드(루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G3).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-06-25), 실적 보도자료(Q4 FY25~Q3 FY26), 8-K(사채 공개매수 3/25, 경영진 8/26), StockAnalysis(2026-09-26).
# 재현 모드: python3 v2/newcards/build.py MU --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-25).
BUILD = {}
CIK = '0000723125'
CUR, YO, QO = '2026-05-28', '2025-05-29', '2026-02-26'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
RELEASE = {'rev': 41456, 'op': 33318, 'ni': 28243}   # Q3 FY26 보도자료(백만 달러)
VOTES, VERDICT = (0, 1, -1), '적정'
CO = 'Micron'
S_ = 'https://www.sec.gov/Archives/edgar/data/723125/'
SEC = S_
PR = {'q3': S_ + '000072312526000013/a2026q3ex991-pressrelease.htm', 'q2': S_ + '000072312526000004/a2026q2ex991-pressrelease.htm',
      'q1': S_ + '000072312525000044/a2026q1ex991-pressrelease.htm', 'q4': S_ + '000072312525000024/a2025q4ex991-pressrelease.htm'}
PR_CUR = 'q3'
TENQ = S_ + '000072312526000015/mu-20260528.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
LINKS = {'mgmt': S_ + '000110465926101067/tm2624017d1_ex99-1.htm', 'tender': S_ + '000110465926034174/tm269755d1_ex99-1.htm'}
FAIRBAND_TITLE = 'id="muFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +{HIST[\'growth_3y\'] * 100:.1f}%)</span>'
OPM_RANGE, Y2 = (0, 90), (0, 90)
FCF_SUB = '현금창출력'
CAPEX_SUB = '미래 재투자'
STAT3 = ('R&amp;D (Q3 FY26)', '$1.32B', '기술 경쟁력 투자')
NEXT = ('9월 30일', '일정 · Q4 FY26 (확정)'); NEXT_OP = ('9월 30일', 'Q4 FY26')
FY_ENDS, FY_LABEL = ('2025-08-28', '2024-08-29'), 'FY25'
HEALTH_NOTE = ('현금·투자자산 $30.1B가 차입금 $5.7B(금융리스 포함)의 다섯 배를 넘는다. 올해 9개월 동안 차입금 $9.4B를 갚았고, 3월에는 사채 6종을 공개매수해 $4.3B가 응모됐다. '
               '3분기 이자비용은 0이라 이자보상배율은 계산하지 않고 만점으로 둔다.')
ACT_REASON = ''
YOY_EXTRA = ''
SEG = [('클라우드 메모리', 13769, '#0071c5'), ('코어 데이터센터', 11524, '#5aa9e6'), ('모바일·클라이언트', 11521, '#f0c040'), ('자동차·임베디드', 4634, '#2ecc71')]
SEG_ADJ = 8   # 보고 매출 41,456 − 네 사업부 합 41,448(옛 카드 도넛 그대로)
SEG_TITLE = '매출 구성 — 사업부별'
SEG_NOTE = ('네 사업부 모두 영업이익률 75~86% · 1년 전 대비 클라우드 메모리 4.1배, 코어 데이터센터 7.5배 · '
            '출처: <a href="{PR[\'q3\']}" target="_blank" rel="noopener">Micron Q3 FY26 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('설비투자 (올해 계획, 정부 보조금 차감)', '약 $27B'),
           ('차입금 상환 (FY26 9개월)', '$9.38B'),
           ('배당 (분기, 3월 30% 인상)', '$0.115 → $0.15', '$0.15/주')]
CHECK_WHEN = '2026년 9월 30일 · Q4 FY2026'
CHECK = ['매출이 가이던스 $50.0B(±$1.0B)에 닿는지',
         '매출총이익률이 가이던스 약 86%를 지키는지 (3분기 84.6%)',
         '전략 고객 계약이 얼마나 늘고, 약정한 현금 예치금(약 $18B)이 들어오는지',
         'FY26 설비투자(순액 약 $27B)와 FY27 투자 계획 — 공급이 늘면 가격이 꺾일 수 있다']
NONOP_WHAT = '지분·장기투자'
PH = ['NVDA', 'AVGO', 'TSM']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': 'AI 반도체 PER 비교', 'pbr': 'AI 반도체 PBR 비교', 'psr': 'AI 반도체 PSR 비교',
                'pcr': 'AI 반도체 PCR(FCF) 비교', 'evebitda': 'AI 반도체 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'GICS Information Technology 28종목 대비 배수 순위'
FUND_ASOF_NOTE = 'Q3 FY26 10-Q (2026-06-25 공시)'
PREMISE = ('이익 기준(PER·EV/EBITDA)으로는 AI 반도체 동종업보다 싸지만, 자기 5년 이력으로는 자산·매출 배수가 5년 중 가장 높은 쪽이다. '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다. '
           '기본 시나리오는 성장률이 5년 평균(연 {HIST[\'growth_5y\'] * 100:.0f}%)에서 식고 최근 4분기 영업이익률({pct(HIST[\'margin_now\'])})이 최근 2년 중앙값({pct(HIST[\'margin_2y\'])})으로 돌아간다고 본다. '
           '1년 PER 범위로 잡은 적정주가(${FB[\'low\']:,}~${FB[\'high\']:,}) 안에 현재가가 있지만, 그 범위는 지금의 호황기 이익에 PER을 곱한 값이다.')
RISK = ('메모리 가격이 공급 부족으로 오른 만큼 이익이 커졌다. 영업이익률이 최근 2년 중앙값({pct(HIST[\'margin_2y\'])})으로 돌아가면 기본 내재가치는 <strong data-vs="dcf">${DCF[\'base\']:.0f}</strong>이고, '
        '현재가가 정당하려면 5년간 매출이 매년 <strong data-vs="req">{pct(DCF[\'requiredGrowth\'])}</strong>씩 커야 한다.')
FUND_TIP = '3분기 영업이익률 {FR[\'opMargin\']:.1f}%로 마진은 만점이다. 성장률은 FY25까지의 연간값이라 올해의 급증은 아직 들어가 있지 않다.'
SELF_TIP = 'PSR {SM[\'PSR\'][\'current\']:.1f}배·PBR {SM[\'PBR\'][\'current\']:.1f}배가 5년 중 상위 {math.ceil(100 - min(SM[\'PSR\'][\'percentile\'], SM[\'PBR\'][\'percentile\']))}%다. 같은 5년 안에서 가장 낮았던 PBR은 {SM[\'PBR\'][\'min\']:.1f}배다.'
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['5년 성장률의 절반(연 {HIST[\'growth_5y\'] / 2 * 100:.0f}%)에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 돌아간다.',
           '5년 성장률(연 {HIST[\'growth_5y\'] * 100:.0f}%)에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 돌아간다.',
           '3년 성장률(연 {HIST[\'growth_3y\'] * 100:.0f}%)에서 출발하고 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다. 5년 뒤 매출 약 $398B.']
DCF_NOTE = ''
NEWS_RANGE = '2025.09 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 8월 26일 개장 전 — 경영진 개편', '2026-08-26',
     '마니시 바티아를 사장 겸 COO, 스콧 디보어를 사장 겸 최고기술·제품책임자로 승진', 'mgmt', 'Micron 발표 (SEC 8-K)'),
    ('', '2026년 6월 24일 장 마감 후 발표 · 6월 25일 반응 — Q3 FY26 실적', '2026-06-25',
     '매출 $41.46B(1년 전 $9.30B) · 영업이익률 80.4% · 다년 전략 고객 계약 체결 · Q4 가이던스 $50.0B', 'q3', 'Micron 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 25일 개장 전 — 사채 공개매수 개시', '2026-03-25',
     '2031~2035년 만기 사채 6종($5.4B) 전액 공개매수를 시작 · 3월 31일 마감 결과 $4.32B 응모(4월 1일 발표)', 'tender', 'Micron 발표 (SEC 8-K)'),
    ('', '2026년 3월 18일 장 마감 후 발표 · 3월 19일 반응 — Q2 FY26 실적', '2026-03-19',
     '매출 $23.86B(+196%) · 매출총이익률 74.4% · 분기 배당 30% 인상 · Q3 가이던스 $33.5B', 'q2', 'Micron 실적 보도자료 (SEC 8-K)'),
    ('', '2025년 12월 17일 장 마감 후 발표 · 12월 18일 반응 — Q1 FY26 실적', '2025-12-18',
     '매출 $13.64B(+57%) · 역대 최대 잉여현금흐름 · Q2 가이던스 $18.7B', 'q1', 'Micron 실적 보도자료 (SEC 8-K)'),
    ('', '2025년 9월 23일 장 마감 후 발표 · 9월 24일 반응 — Q4 FY25 실적', '2025-09-24',
     '매출 $11.32B(+46%) · FY25 매출 $37.38B(+49%) · Q1 가이던스 $12.5B', 'q4', 'Micron 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('AI 수요와 공급 부족으로 메모리 가격이 뛰었다', '초호황·사이클 경계',
           ['분기 매출이 $11.32B(Q4 FY25) → $13.64B → $23.86B → $41.46B(Q3 FY26)로 늘었고, 매출총이익률은 44.7%에서 84.6%가 됐다.',
            '회사는 수요가 공급을 넘어 가격이 오르고 전 제품의 수익성이 좋아졌다고 밝혔다. 다음 분기 가이던스는 매출 $50.0B, 매출총이익률 약 86%다.',
            '다년 전략 고객 계약(인수하지 않아도 대금을 내는 take-or-pay)을 맺었다. 대형 계약은 가격 상·하한이 있고, 고객 예치금·재무 약정 $22B를 받기로 했다.'],
           '이익은 공급 부족에 따른 가격 상승에서 나왔다. 회사는 올해 설비투자를 약 $27B로 잡았고, FY25 매출의 절반 이상이 상위 10개 고객에서 나왔으며, 중국에서는 핵심 정보기반시설 운영자의 구매가 막혀 있다.',
           'Q4 FY26 실적(9월 30일)에서 매출 $50.0B·매출총이익률 약 86% 가이던스를 지키는지, 전략 고객 계약과 예치금 유입이 얼마나 늘었는지.')
BULL = [('AI 수요', 'HBM4를 주요 고객 플랫폼용으로 대량 출하하고, 네 사업부 모두 영업이익률이 75% 이상이다.'),
        ('계약', '다년 take-or-pay 계약에 가격 하한이 있어 회사는 하한가에서도 과거 최고 마진을 넘는다고 본다.'),
        ('재무', '현금·투자자산 $30.1B가 차입금 $5.7B보다 훨씬 많고, 올해 차입금 $9.4B를 갚았다.')]
BEAR = [('사이클', '이익이 공급 부족에 따른 가격 상승에서 나와, 공급이 늘면 가격이 꺾일 수 있다.'),
        ('설비투자', '올해 순 설비투자가 약 $27B라, 가격이 꺾이면 늘어난 설비의 고정비 부담이 커진다.'),
        ('집중', 'FY25 매출의 절반 이상이 상위 10개 고객이고, 중국은 핵심 기반시설 구매가 막혀 있다.')]
ANALYST = {'rating': 'Strong Buy', 'n': 49, 'nt': 30, 'mean': 1599.5, 'median': 1540, 'low': 1200, 'high': 2200, 'sb': 36, 'b': 9, 'h': 3, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-06'
PRE = [r'''
FR = {r_['metric']: r_['value'] for ax_ in FUND['axes'].values() for r_ in ax_.get('rows', [])}   # 기본적 분석 지표 값
''']
# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
POST = [r'''
one("  const usd = v => '$' + (Number.isInteger(v) ? v : v.toFixed(2));", "  const usd = v => v == null ? '—' : '$' + (Number.isInteger(v) ? v.toLocaleString('en-US') : v.toFixed(2));   // 중간값 없음·천 단위(카드 한정)")
# 분기 비교 각주: FCF의 설비투자는 총액(비GAAP)
assert h.count(' · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · ') == 2
h = h.replace(' · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · ', ' · GAAP 기준 · FCF는 영업현금흐름 − 설비투자(총액, 비GAAP) · ')
# 총자산증가율 메모(옛 카드 표기)
one('<span class="diag-note">FY25 말 $82.8B(전년 $69.4B) · 연간 지표</span>', '<span class="diag-note">FY25 $82.8B(전기 $69.4B) · 연간 지표, FY26 마감 전까지 동일</span>')
# 자본배분 네 번째 줄(자사주 매입)과 아래 각주 — 옛 카드는 네 줄
one('        <div class="zone-item">\n          <span class="zone-label">배당 (분기, 3월 30% 인상)</span>',
    '        <div class="zone-item">\n          <span class="zone-label">자사주 매입 (FY26 9개월, 3분기는 없음)</span>\n          <span class="zone-val">$0.65B</span>\n        </div>\n'
    '        <div class="zone-item">\n          <span class="zone-label">배당 (분기, 3월 30% 인상)</span>')
sub(r'(<span class="zone-val">\$0\.15/주</span>\n          </div>\n        </div>\n      </div>\n)',
    lambda m: m.group(1) + '      <div class="yoy-footnote" style="margin-top:14px;">전략 고객 계약으로 고객 예치금·재무 약정 $22B를 받기로 했고 그중 약 $18B가 현금 예치금이다 · 출처: <a href="' + C.TENQ + '" target="_blank" rel="noopener">Micron Q3 FY26 10-Q →</a></div>\n')
# 역산 문장: 성장 모드(reqMode growth)는 JS가 문장을 쓰지 않고 칸만 채운다 — 틀의 칸 있는 문장을 되살린다(fill.py가 '—'로 비움)
assert DCF['reqMode'] == 'growth'
one('<div class="reverse">—</div>', F('<div class="reverse">지금 가격(<span data-dcf-price>${px:.2f}</span>)이 정당하려면 5년간 매출이 매년 <b data-dcf-req>{pct(DCF[\'requiredGrowth\'])}</b>씩 커야 한다. '
    '기본 시나리오(<span data-dcf-basev>${DCF[\'base\']:.0f}</span>)를 같은 방식으로 환산하면 연 <span data-dcf-baseeq>{pct(DCF[\'baseEquivGrowth\'])}</span>다.</div>'))
# PER 차트 단위(옛 카드 PER(TTM))
one("unit: 'PER', max:", "unit: 'PER(TTM)', max:")
''']


# ── 자동 카드(설계 D, 2026-10-10) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose.py 제안(손 표와 숫자 일치) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {
  "srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"
 },
 "members": {
  "mu:CMBUMember": [
   "클라우드 메모리",
   "#0071c5"
  ],
  "mu:CDBUMember": [
   "코어 데이터센터",
   "#5aa9e6"
  ],
  "mu:MCBUMember": [
   "모바일·클라이언트",
   "#f0c040"
  ],
  "mu:AEBUMember": [
   "자동차·임베디드",
   "#2ecc71"
  ]
 },
 "ignore": [
  "us-gaap:AllOtherSegmentsMember"
 ]
}
# 손 문구 블록 정리: 화면 구조 고침만 남기고 분기 문장·날짜 박힌 치환·시간이 지나면 틀려지는 문장은 뺐다. 덩어리마다 따로 실행(자동 카드는 못 찾으면 건너뜀)
POST = ['\none("  const usd = v => \'$\' + (Number.isInteger(v) ? v : v.toFixed(2));", "  const usd = v => v == null ? \'—\' : \'$\' + (Number.isInteger(v) ? v.toLocaleString(\'en-US\') : v.toFixed(2));   // 중간값 없음·천 단위(카드 한정)")', "# 분기 비교 각주: FCF의 설비투자는 총액(비GAAP)\nassert h.count(' · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · ') == 2\nh = h.replace(' · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · ', ' · GAAP 기준 · FCF는 영업현금흐름 − 설비투자(총액, 비GAAP) · ')", '# 역산 문장: 성장 모드(reqMode growth)는 JS가 문장을 쓰지 않고 칸만 채운다 — 틀의 칸 있는 문장을 되살린다(fill.py가 \'—\'로 비움)\nif DCF[\'reqMode\'] == \'growth\':\n one(\'<div class="reverse">—</div>\', F(\'<div class="reverse">지금 가격(<span data-dcf-price>${px:.2f}</span>)이 정당하려면 5년간 매출이 매년 <b data-dcf-req>{pct(DCF[\\\'requiredGrowth\\\'])}</b>씩 커야 한다. \'\n    \'기본 시나리오(<span data-dcf-basev>${DCF[\\\'base\\\']:.0f}</span>)를 같은 방식으로 환산하면 연 <span data-dcf-baseeq>{pct(DCF[\\\'baseEquivGrowth\\\'])}</span>다.</div>\'))', '# PER 차트 단위(옛 카드 PER(TTM))\none("unit: \'PER\', max:", "unit: \'PER(TTM)\', max:")']
