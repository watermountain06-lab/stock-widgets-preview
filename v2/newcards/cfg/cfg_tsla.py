# TSLA v2 카드 설정 — fill.py TSLA. 틀 시절 카드를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-23), Tesla Q1~Q2 2026·Q3~Q4 2025 Update(8-K), 인도량 발표(8-K), 2025 CEO 성과 보상 주총(8-K 11/7), StockAnalysis(2026-09-25).
# 일회성 세금(tax_oneoff.json), 시가총액 주식 수는 미획득 성과 제한주 제외(엔진). 동종업 점수는 경기소비재 + IT(엔진), 비교 차트는 빅테크 6곳(카드 가격).
# 재현 모드: python3 v2/newcards/build.py TSLA --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-24).
BUILD = {}
CIK = '0001318605'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 28236, 'op': 398, 'ni': 1114, 'ocf': 4697}   # Q2 2026 Update(백만 달러, 순이익은 보통주 귀속). 회사 설비투자 $5,789M은 에너지 시스템 구입 포함
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Tesla'
S_ = 'https://www.sec.gov/Archives/edgar/data/1318605/'
SEC = S_
PR = {'q2': S_ + '000162828026049213/exhibit991.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000162828026049270/tsla-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'d2': S_ + '000162828026046717/exhibit99111111.htm', 'q1': S_ + '000162828026026551/exhibit991.htm', 'd1': S_ + '000162828026022956/exhibit9911111.htm', 'q4': S_ + '000162828026003837/exhibit991.htm', 'ceo': S_ + '000110465925108507/tm2530590d1_8k.htm', 'q3': S_ + '000162828025045861/exhibit991.htm'}   # 분기 Update는 뉴스 링크라 PR이 아니라 여기(실적 보도자료 이름이 'Update')
FAIRBAND_TITLE = 'id="tslaFairBand"'   # 옛 카드는 툴팁이 없었다
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (0, 15), (0, 15)
FCF_SUB = '현금창출력'
CAPEX_SUB = '미래 재투자'
STAT3 = ('R&amp;D (Q2 2026)', '$2.4B', '기술 경쟁력 투자')
NEXT = ('10월 하순 예상', '일정 · Q3 2026'); NEXT_OP = ('10월 하순', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY25'
HEALTH_NOTE = '유동비율 {FR[\'currentRatio\']:.0f}%·당좌비율 {FR[\'quickRatio\']:.0f}%로 단기 지급 여력은 넉넉하다. 현금·단기투자 $43.5B이 차입금 $9.1B보다 훨씬 많아 순현금이다. 이자보상배율 {FR[\'interestCoverage\']:.1f}배는 차입이 많아서가 아니라 2분기 영업이익이 $0.4B로 작아서 낮게 나온 값이다.'
ACT_REASON = ''
YOY_EXTRA = ''
SEG = [('자동차', 20516, '#E31937'), ('에너지 발전·저장', 3139, '#2ecc71'), ('서비스·기타', 4581, '#3498db')]
SEG_ADJ = 0   # 세 사업 합 = 보고 매출 28,236
SEG_TITLE = '매출 구성 — 사업별'
SEG_NOTE = '전년 대비 자동차 +23%, 에너지 +13%, 서비스·기타 +50%(사상 최대 이익) · 출처: <a href="{PR[\'q2\']}" target="_blank" rel="noopener">Tesla Q2 2026 Update (SEC 8-K) →</a>'
CAPITAL = [('설비투자 (Q2 2026)', '$5.79B'), ('설비투자 (2026년 상반기)', '$8.28B'), ('SpaceX 지분 (2026-03 $2.0B 투자, 6월 말 공정가치)', '', '$3.01B')]
CHECK_WHEN = '2026년 10월 하순 (예상) · Q3 2026'
CHECK = ['10월 초 3분기 인도량이 1년 전 기록(497,099대)을 넘는지', '영업이익률이 2분기 1.4%에서 반등하는지(2분기 영업비용 +47%)', '설비투자가 늘어난 속에서 잉여현금흐름(2분기 −$1.1B)이 플러스로 돌아오는지', 'Cybercab·Semi 양산 속도와 로보택시 운영 도시(현재 미국 7곳)가 얼마나 늘었는지']
NONOP_WHAT = '지분·장기투자'
PH = ['NVDA', 'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
PEER_FILE = None   # 비교 차트는 빅테크 카드 가격(build_peer_score.multiples_now), 점수는 엔진의 경기소비재 + IT
CHART_CAP = {}
SELF_CAP = {'per': 0, 'pcr': 0, 'evebitda': 0}   # TSLA 막대는 축 밖(옛 카드)
CHART_NOTE = {'per': ' (TSLA는 축 밖)', 'pcr': ' (TSLA는 축 밖)', 'evebitda': ' (TSLA는 축 밖)'}
MISS_WHY = {('AMZN', 'pcr'): ' 잉여현금흐름 적자'}
CHART_TITLES = {'per': '빅테크 PER 비교', 'pbr': '빅테크 PBR 비교', 'psr': '빅테크 PSR 비교', 'pcr': '빅테크 PCR(FCF) 비교', 'evebitda': '빅테크 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 경기소비재 섹터와 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'GICS 경기소비재 + IT 섹터 대비 배수 순위'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-23 공시)'
PREMISE = '동종업과 자기 5년 이력 모두 비싼 쪽이고, <strong>현금흐름 내재가치(기본 시나리오)는 현재가의 {DCF[\'base\'] / px * 100:.0f}%다.</strong> 지금 가격은 자동차·에너지 사업이 벌어들이는 현금보다 로보택시·Optimus 같은 앞으로의 사업에 거는 기대를 반영하는데, 이 모델은 아직 매출이 없는 사업을 값으로 매기지 않는다.'
RISK = ('매출이 지난 5년 속도(연 {pct(HIST[\'growth_5y\'])})로 크다가 식는다면, 현재가가 정당하려면 영업이익률이 <strong data-vs="req">{pct(DCF[\'requiredMargin\'])}</strong>여야 한다(지금 {pct(HIST[\'margin_now\'])}). '
        '지금 마진으로 성장만으로 맞추려면 5년 내내 연 {DCF[\'requiredGrowth\'] * 100:.0f}%가 필요하다(지난 5년 {HIST[\'growth_5y\'] * 100:.1f}%의 10배 이상).')
FUND_TIP = '2분기 영업이익률 {FR[\'opMargin\']:.1f}%는 영업비용이 전년 대비 47% 늘어서다. 순이익($1.1B)에는 SpaceX 지분 평가이익(2분기 $1.0B)이 들어 있다.'
SELF_TIP = 'PER {SM[\'PER\'][\'current\']:.0f}배는 5년 중 상위 {100 - SM[\'PER\'][\'percentile\']:.0f}%다. 시가총액은 머스크의 미획득 성과 제한주 423.7M주(2025-08~2026-04에는 임시 보상 96M주도)를 뺀 주식 수(3.53B)로 계산했다. EV/EBITDA의 감가상각은 SEC 태그상 감가상각만이라 회사 발표(상각·손상 포함, 최근 4분기 $6.48B)보다 작고, 그만큼 배수가 약 10% 높게 나온다.'
PEER_TIP = ('GICS 경기소비재 섹터에 IT 섹터를 더해 배수 순위를 매긴 값이다.', '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['5년 성장 속도(연 {pct(HIST[\'growth_5y\'])})의 절반에서 출발하고, 영업이익률은 5년 중앙값({pct(HIST[\'margin_5y\'])})으로 오른다. 매출 $1당 투자 $0.54.',
           '5년 성장 속도로 출발하고, 영업이익률은 2년 중앙값({pct(HIST[\'margin_2y\'])})으로 오른다. 매출 $1당 투자는 $0.30에서 $0.54로 는다.',
           '3년 성장 속도(연 {pct(HIST[\'growth_3y\'])})와 지금 영업이익률({pct(HIST[\'margin_now\'])})이 이어진다. 성장·마진이 가장 낮아 세 시나리오 중 가장 낮다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('red', '2026년 7월 22일 발표 · 7월 23일 반응 — Q2 2026 실적', '2026-07-23',
     '매출 $28.2B(+26%) · 영업이익 $0.4B(영업이익률 1.4%) · 설비투자 $5.8B로 잉여현금흐름 −$1.1B · Cybercab 텍사스 생산 시작', 'q2', 'Tesla Q2 2026 Update (SEC 8-K)'),
    ('neutral', '2026년 7월 2일 — Q2 인도량', '2026-07-02',
     '인도 480,126대(2분기 기준 최대) · 생산 451,758대 · 에너지 저장 13.5GWh', 'd2', 'Tesla 인도량 발표 (SEC 8-K)'),
    ('', '2026년 4월 22일 발표 · 4월 23일 반응 — Q1 2026 실적', '2026-04-23',
     '매출 $22.4B(+16%) · 영업이익률 4.2% · 인도 358,023대', 'q1', 'Tesla Q1 2026 Update (SEC 8-K)'),
    ('red', '2026년 4월 2일 — Q1 인도량', '2026-04-02',
     '인도 358,023대 · 생산 408,386대로 인도가 생산보다 5만 대 적다 · 에너지 저장 8.8GWh', 'd1', 'Tesla 인도량 발표 (SEC 8-K)'),
    ('', '2026년 1월 28일 발표 · 1월 29일 반응 — Q4 2025 실적', '2026-01-29',
     '매출 $24.9B(−3%) · 영업이익률 5.7% · 2025년 인도 1,636,129대', 'q4', 'Tesla Q4 2025 Update (SEC 8-K)'),
    ('neutral', '2025년 11월 6일 주총 · 11월 7일 반응 — CEO 성과 보상 승인', '2025-11-07',
     '머스크에게 성과 조건부 제한주 약 4.24억 주를 주는 2025 CEO 성과 보상을 주주가 승인(목표 차량 2,000만 대·조정 EBITDA $400B 등)', 'ceo', 'Tesla 공시 (SEC 8-K)'),
    ('', '2025년 10월 22일 발표 · 10월 23일 반응 — Q3 2025 실적', '2025-10-23',
     '매출 $28.1B(+12%) · 인도 497,099대로 분기 최대 · 영업이익률 5.8%', 'q3', 'Tesla Q3 2025 Update (SEC 8-K)'),
]
SUMMARY = ('자동차 이익은 줄고, 가치는 로보택시·AI 기대에 걸려 있다', '투자 확대·수익성 약화', ['영업이익률이 1년 새 4.1%(Q2 2025)에서 1.4%(Q2 2026)로 내려왔다. 2분기 영업비용이 전년 대비 47% 늘었다.', '설비투자가 분기 $2.4B에서 $5.8B로 늘어 2분기 잉여현금흐름이 −$1.1B가 됐다. Cybercab 생산을 시작했고, Semi는 올해 생산 예정이며, Fremont에 Optimus 라인을 짓고 있다.', '로보택시는 미국 7개 대도시에서 운영 중이고, 차를 살 때 FSD(감독형) 구독을 고르는 비율이 늘고 있다.'], '머스크 보상 주식이 크게 늘었다(2025년 11월 성과 보상 약 4.24억 주 승인, 2026년 2분기 2018년 보상 행사로 순증 약 1.9억 주). 실적 발표 다음날 주가가 오른 것은 네 번 중 한 번(Q3 2025)뿐이다.', '10월 초 3분기 인도량과 10월 하순 실적에서 영업이익률이 1.4%에서 반등하는지, 잉여현금흐름이 플러스로 돌아오는지.')
BULL = [('신사업', 'Cybercab 생산을 시작했고, 로보택시가 미국 7개 대도시에서 운영된다.'), ('서비스', '서비스·기타 매출이 전년 대비 50% 늘며 사상 최대 이익률을 냈다.'), ('현금', '현금·단기투자 $43.5B가 차입금 $9.1B보다 훨씬 많다.')]
BEAR = [('수익성', '2분기 영업이익률이 1.4%이고, 영업이익은 전년 대비 57% 줄었다.'), ('밸류', '현재가가 기본 내재가치의 약 {px / DCF[\'base\']:.0f}배이고, PER {SM[\'PER\'][\'current\']:.0f}배로 비교군에서 가장 비싸다.'), ('희석', '머스크 보상으로 발행 주식이 1년 새 3.23B에서 3.95B로 늘었다(미획득 4.24억 주 포함).')]
ANALYST = {'rating': 'Buy', 'n': 43, 'mean': 396.94, 'median': 415, 'low': 125, 'high': 600, 'sb': 15, 'b': 4, 'h': 20, 's': 2, 'ss': 2}
ANALYST_ASOF = '2026-09-25'
REQ_MULT_EXACT = False   # 옛 카드는 "3배를 넘는다"(틀 문구)
# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
PRE = [r'''
FR = {r_['metric']: r_['value'] for ax_ in FUND['axes'].values() for r_ in ax_.get('rows', [])}   # 기본적 분석 지표 값(E26)
''']
POST = [r'''
# 자본배분 칸: 옛 카드는 설비투자·SpaceX 지분·배당 없음 네 줄과 설명(틀의 세 줄 구조와 다름) — 옛 블록을 그대로
sub(r'(<div class="card-title">자본배분 · 주주환원 \(Q2 2026 · 2026\.06\.30 기준\)</div>\n).*?(\n    </div>\n  </div>)', lambda m: m.group(1) + C.CAPITAL_HTML + m.group(2))
# YoY·QoQ 각주: 옛 카드 문구(보통주 귀속·2024년 분기 소급 수정 전, Update 원문 링크)
sub(r"footnote: '기준일: 2026\.06\.30\(Q2 2026\) vs 2025\.06\.30[^\n]*'", lambda m: C.FOOTNOTES[0])
sub(r"footnote: '기준일: 2026\.06\.30\(Q2 2026\) vs 2026\.03\.31[^\n]*'", lambda m: C.FOOTNOTES[1])
# 총자산증가율 메모(옛 카드 표기)
one(f'FY25 말 ${a1 / 1000:.1f}B(전년 ${a0 / 1000:.1f}B) · 연간 지표</span>', f'FY25 ${a1 / 1000:.1f}B(전기 ${a0 / 1000:.1f}B) · 연간 지표, FY26 마감 전까지 동일</span>')
# 음수 FCF 칸: '$-1.09B' 대신 '−$1.09B'
h = h.replace(f'<div class="stat-value">${r1(fcf[cur])}B</div>', f'<div class="stat-value">−${abs(r1(fcf[cur]))}B</div>', 1) if fcf[cur] < 0 else h
''']
CAPITAL_HTML = '      <div class="zone-list">\n        <div class="zone-item">\n          <span class="zone-label">설비투자 (Q2 2026)</span>\n          <span class="zone-val">$5.79B</span>\n        </div>\n        <div class="zone-item">\n          <span class="zone-label">설비투자 (2026년 상반기)</span>\n          <span class="zone-val">$8.28B</span>\n        </div>\n        <div class="zone-item">\n          <span class="zone-label">SpaceX 지분 (2026-03 $2.0B 투자, 6월 말 공정가치)</span>\n          <span class="zone-val">$3.01B</span>\n        </div>\n        <div class="zone-item">\n          <span class="zone-label">배당 · 자사주 매입</span>\n          <span class="zone-val">없음</span>\n        </div>\n      </div>\n      <div class="yoy-footnote" style="margin-top:14px;">설비투자는 1년 전 분기 $2.39B에서 $5.79B로 늘었다. 회사는 Cybercab·Semi·Megafactory·Optimus 라인 투자를 진행 중이라고 밝혔다. SpaceX 지분은 구 xAI 우선주를 전환한 것이다 · 출처: <a href="https://www.sec.gov/Archives/edgar/data/1318605/000162828026049270/tsla-20260630.htm" target="_blank" rel="noopener">Tesla Q2 2026 10-Q →</a></div>'
FOOTNOTES = ['footnote: \'기준일: 2026.06.30(Q2 2026) vs 2025.06.30(Q2 2025) · GAAP 기준(순이익은 보통주 귀속, 2024년 분기는 암호자산 회계기준 소급 수정 전 값) · FCF는 영업현금흐름 − 설비투자 · <a href="https://www.sec.gov/Archives/edgar/data/1318605/000162828026049213/exhibit991.htm" target="_blank" rel="noopener">Tesla Q2 2026 Update 원문 (SEC 8-K) →</a>\'', 'footnote: \'기준일: 2026.06.30(Q2 2026) vs 2026.03.31(Q1 2026) · GAAP 기준(순이익은 보통주 귀속, 2024년 분기는 암호자산 회계기준 소급 수정 전 값) · FCF는 영업현금흐름 − 설비투자 · <a href="https://www.sec.gov/Archives/edgar/data/1318605/000162828026049213/exhibit991.htm" target="_blank" rel="noopener">Tesla Q2 2026 Update 원문 (SEC 8-K) →</a>\'']

