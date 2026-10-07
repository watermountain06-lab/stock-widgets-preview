# PM v2 카드 설정 — fill.py PM. 틀 시절 카드를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G6).
# 재현 모드: python3 v2/newcards/build.py PM --from-card (일봉·이동평균·백테스트는 지금 카드에서).
BUILD = {}
CIK = '0001413329'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
RELEASE = {'rev': 11192, 'op': 4530, 'ni': 2817}   # Q2 2026 보도자료 손익계산서(백만 달러, 순이익은 PMI 귀속)
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Philip Morris International'
S_ = 'https://www.sec.gov/Archives/edgar/data/1413329/'
SEC = S_
PR = {'q2': S_ + '000162828026049107/earningsreleasepm-ex991xq2.htm', 'q1': S_ + '000162828026026385/earningsreleasepm-ex991xq1.htm',
      'q4': S_ + '000162828026005932/earningsreleasepm-ex991xq4.htm', 'q3': S_ + '000162828025045579/earningsreleasepm-ex991xq3.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000162828026049493/pm-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
FY_ENDS = ('2025-12-31', '2024-12-31')
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FAIRBAND_TITLE = 'id="pmFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm:.2f}. PER만으로 낸 범위라, 자기 이력·동종업·현금흐름 내재가치를 함께 보는 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '유형자산 취득(현금흐름표) · 올해 전망 $1.4~1.6B'
STAT3 = ('R&amp;D (Q2 2026)', '해당 없음', '분기 연구개발비를 따로 공시하지 않는다')
OPM_RANGE, Y2 = (30, 42), (30, 42)
NEXT = ('10월 하순 예상', '일정 · Q3 2026 (회사 미확정)')
NEXT_OP = ('10월 하순', 'Q3 2026 예상')
FY_LABEL = 'FY2025'
HEALTH_NOTE = '유동비율 98.0%, 재고($11.4B, 숙성 중인 잎담배 포함)를 뺀 당좌비율 54.9%다. 차입금은 $49.1B(단기 $3.3B + 1년 안 만기 $3.4B + 장기 $42.4B)이고 현금은 $6.0B다. 6월 29일 기간대출 €1.0B(약 $1.1B)를 미리 갚았고, 회사는 연말 순차입금 ÷ 조정 EBITDA 2.0배 근처를 목표로 한다. PMI 귀속 자본이 −$8.6B(비지배지분 포함 −$6.7B, 자본잠식)라 부채비율과 PBR은 계산되지 않는다. 이자보상배율 18.6배는 2분기 순이자비용 $243M(이자수익 차감 후, 회사가 총액을 따로 내지 않음) 기준이다.'
YOY_EXTRA = '순이익 감소는 RBH 지분 손상 $511M(주당 $0.33) 때문 · '
SEG = [('해외 비연소(IQOS 등)', 3877, '#0f6eb4'), ('해외 연소(궐련)', 6459, '#94a3b8'), ('미국(ZYN 등)', 856, '#f0c040')]
SEG_ADJ = 0   # 세 부문 합 = 보고 매출 11,192
SEG_TITLE = '매출 구성 — 부문별 매출'
SEG_NOTE = '비연소 제품 전체(미국 포함)가 매출의 약 42%다 · 1년 전보다 해외 비연소 +14.2%, 해외 연소 +9.8%(가격 인상 10.0%), 미국 −0.7%(ZYN 출하 +1.8%) · 2026년 1월부터 지역 4부문을 3부문으로 바꿨다 · 출처: <a href="https://www.sec.gov/Archives/edgar/data/1413329/000162828026049107/earningsreleasepm-ex991xq2.htm" target="_blank" rel="noopener">Q2 2026 실적 보도자료 (SEC 8-K) →</a>'
CAPITAL = [('자사주 매입 (올해 계획 없음)', '$0'), ('순차입금 ÷ 조정 EBITDA 목표 (2026년 말, 회사 전망)', '약 2.0배'), ('배당 (Q2 2026 지급, 분기 $1.47)', '9월 $1.60으로 8.8% 인상', '$2.3B')]
CHECK_WHEN = '2026년 10월 하순 (예상) · Q3 2026'
CHECK = ['3분기 조정 EPS 전망 $2.29~2.34(9월 8일 환율만 반영해 올림)와 연간 조정 EPS $8.35~8.50 유지', '미국 ZYN — 2분기 출하 +1.8%, 소비자 구매는 제자리~소폭 증가. 새 제품(ZYN ULTRA 등)과 하반기 미국 투자 확대의 효과', '일본 IQOS — 4월 가격 인상 뒤 2분기 조정 판매량 −3.4%(인상 전 사재기 효과를 빼면 +1.0%, 회사 예상 범위)에서 회복하는지', '차입금 감축(연말 순차입금 ÷ 조정 EBITDA 2.0배 근처 목표)과 자사주 매입 없는 현금 사용']
NONOP_WHAT = '지분·장기투자'
PH = ['MO', 'KO', 'PEP', 'PG', 'MDLZ', 'KMB']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '담배·음료·생활용품 PER 비교 (필수소비재 34종목 중 6곳)', 'pbr': '담배·음료·생활용품 PBR 비교 (PM 자본 음수)', 'psr': '담배·음료·생활용품 PSR 비교', 'pcr': '담배·음료·생활용품 PCR(FCF) 비교', 'evebitda': '담배·음료·생활용품 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&amp;P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-24 공시)'
PREMISE = '주가가 1년 새 {ch:.0f}% 올라 자기 이력에서 네 배수가 모두 비싼 쪽이라 {selfsc:.1f}점이다(PSR {SM[\'PSR\'][\'current\']:.1f}배는 5년 상위 {100 - SM[\'PSR\'][\'percentile\']:.0f}%, EV/EBITDA는 최근 2.5년 기준). PBR은 자본이 음수라 계산하지 않는다. S&P500 필수소비재 34종목 안에서는 {peersc:.1f}점으로 비싼 쪽(30 미만)이라 동종업도 −1이다. 적자·순이익률 2% 미만 동종 종목을 PER 비교에서 빼면서(2026-10-04) 30.0점에서 내려왔고, 판정(고평가)은 그대로다. <strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.'
RISK = '매출이 지난 5년 속도(연 {pct(HIST[\'growth_5y\'])})로 크다가 식는다면, 현재가가 정당하려면 영업이익률이 <strong data-vs="req">{pct(DCF[\'requiredMargin\'])}</strong>여야 한다(최근 4분기 {pct(HIST[\'margin_now\'])}). PER {SM[\'PER\'][\'current\']:.1f}배는 GAAP EPS 기준이라 2분기 RBH 손상(주당 $0.33)이 들어 있다. 회사의 올해 조정 EPS 전망($8.35~8.50)으로 보면 약 {px / ((8.35 + 8.50) / 2):.0f}배다.'
FUND_TIP = '유동비율 1점·부채비율 1점(자본 음수)이 건전성을 끌어내리고, 영업이익률 40%대·순이익률 25%가 수익성을 받친다. 이자보상배율은 순이자비용 기준이다(회사가 총액을 따로 내지 않음).'
SELF_TIP = 'PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PSR {SM[\'PSR\'][\'current\']:.1f}배·PCR {SM[\'PCR\'][\'current\']:.1f}배 모두 5년 중 비싼 쪽이다. EV/EBITDA는 2022년 3분기~2023년 4분기 감가상각이 SEC 표준 태그에 없어 최근 2.5년 이력으로 본다(규칙대로 두고 명시, 2026-10-01 결정). PBR은 자본 음수(−$8.6B)라 빠졌다.'
PEER_TIP = ('S&P500 필수소비재(34종목)와 배수 순위를 매긴 값이다.', '담배·음료·식품·생활용품·유통이 섞여 있다. PM은 PSR이 25곳 중 두 번째로 높고 PER은 중간이다. PBR은 자본 음수로 빠졌다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {HIST[\'margin_5y\'] * 100:.2f}%로 간다.', '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {HIST[\'margin_2y\'] * 100:.2f}%로 간다(두 마진이 거의 같아 보수·기본 차이는 성장률에서 온다).', '3년 성장률(연 {pct(HIST[\'growth_3y\'])})에서 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [('green', '2026년 9월 18일 장 전 — 배당 8.8% 인상', '2026-09-18', '분기 배당 $1.47 → $1.60(연 $6.40) · 2008년 상장 뒤 해마다 인상', 'https://www.sec.gov/Archives/edgar/data/1413329/000162828026062621/september2026dividend.htm', 'Philip Morris International 공시 (SEC 8-K)'), ('', '2026년 9월 8일 장 전 — 연간 EPS 전망 상향(환율만)', '2026-09-08', '연간 조정 EPS $8.35~8.50(+10.7~12.7%) · 3분기 $2.29~2.34 · 나머지 가정은 7월과 같음', 'https://www.sec.gov/Archives/edgar/data/1413329/000162828026060806/a2026barclaysrelease.htm', 'Philip Morris International 공시 (SEC 8-K)'), ('neutral', '2026년 8월 24일 장 전 — Altria와 궐련 위탁생산', '2026-08-24', '해외 계열사가 Philip Morris USA(Altria)와 궐련 위탁생산 계약 · 첫 출하 2027년 초 · 2026년 실적 영향은 크지 않다고 밝힘', 'https://www.sec.gov/Archives/edgar/data/1413329/000162828026058513/a2026-08x24pressrelease.htm', 'Philip Morris International 공시 (SEC 8-K)'), ('', '2026년 7월 22일 장 전 — Q2 2026 실적', '2026-07-22', '매출 $11.2B(+10.4%, 첫 $11B 돌파)·EPS $1.80(조정 $2.20, +15.2%) · RBH 지분 손상 $511M · IQOS 출하 +7.6%', 'q2', 'Philip Morris International 실적 보도자료 (SEC 8-K)'), ('neutral', '2026년 5월 20일 장 전 — CFO 교체 발표', '2026-05-20', '마시모 안돌리나 유럽 대표가 8월 1일부터 그룹 CFO · 에마뉘엘 바보 CFO는 2027년 3월까지 CEO 자문역', 'https://www.sec.gov/Archives/edgar/data/1413329/000162828026036721/a2026-05x20release.htm', 'Philip Morris International 공시 (SEC 8-K)'), ('', '2026년 4월 22일 장 전 — Q1 2026 실적', '2026-04-22', '매출 $10.1B(+9.1%)·EPS $1.56(조정 $1.96, +16.0%) · 인도 소수 지분 공정가치 평가손으로 GAAP EPS 감소', 'q1', 'Philip Morris International 실적 보도자료 (SEC 8-K)'), ('', '2026년 2월 6일 장 전 — Q4 2025 실적', '2026-02-06', '2025년 매출 $40B 돌파·EPS $7.26(조정 $7.54, +14.8%) · 비연소 매출 비중 41.5% · 2026~2028 성장 목표 제시', 'q4', 'Philip Morris International 실적 보도자료 (SEC 8-K)'), ('', '2025년 10월 21일 장 전 — Q3 2025 실적', '2025-10-21', 'EPS $2.23(조정 $2.24, +17.3%) · 연간 조정 EPS 전망 상향 · 비연소 출하 +16.6%', 'q3', 'Philip Morris International 실적 보도자료 (SEC 8-K)')]
SUMMARY = ('해외 IQOS가 성장을 끌고 미국 ZYN은 숨 고르기, 주가는 1년 새 {ch:.0f}% 올라 배수가 비싼 쪽', '비연소 성장·고평가', ['2분기 매출이 처음으로 $11B를 넘었고(+10.4%), 조정 EPS는 $2.20(+15.2%)였다. 해외 비연소 매출이 14.2% 늘었다.', '미국 ZYN은 작년 2분기 재고 효과에도 출하가 1.8% 늘었지만, 소비자 구매는 커지는 시장에서 제자리~소폭 증가에 그쳤다(회사는 경쟁 환경 탓으로 봤다). 새 제품과 하반기 투자 확대로 대응한다. 6월 30일 FDA가 ZYN 20종에 위험저감 표시(MRTP)를 허가했다.', '9월에 연간 조정 EPS 전망을 환율 덕에 올렸고, 배당을 8.8% 인상했다. 올해 자사주 매입은 하지 않고 차입금을 줄인다.'], '자기 이력 배수가 모두 비싼 쪽이고, 현금흐름 모델로는 현재가의 {DCF[\'base\'] / px * 100:.0f}%만 설명된다.', 'Q3 2026 실적(10월 하순 예상)의 조정 EPS($2.29~2.34 전망)와 미국 ZYN 회복 여부.')
BULL = [('성장', '2분기 매출 +10.4%, 해외 비연소 +14.2%, IQOS 출하 +7.6%.'), ('수익성', '영업이익률 40.5%(2분기), 연간 조정 EPS 전망 +10.7~12.7%.'), ('배당', '분기 $1.60으로 8.8% 인상, 상장 뒤 해마다 올렸다.')]
BEAR = [('밸류', 'PER {SM[\'PER\'][\'current\']:.1f}배·PSR {SM[\'PSR\'][\'current\']:.1f}배가 5년 중 비싼 쪽, 현금흐름 내재가치 ${DCF[\'base\']:.0f}.'), ('미국', 'ZYN 출하 +1.8%, 소비자 구매는 제자리~소폭 증가이고 경쟁이 고르지 않다(회사 표현).'), ('부채', '차입금 $49.1B, 자본 −$8.6B(자본잠식).')]
ANALYST = {'rating': 'Buy', 'n': 16, 'nt': 9, 'mean': 208.89, 'median': 215, 'low': 175, 'high': 225, 'sb': 9, 'b': 3, 'h': 4, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-06'
MISSING_NOTE = ''
POST = [r'''
# QoQ 각주: 1분기 FCF 음수 설명(옛 카드)
one("vs 2026.03.31(Q1 2026) · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · <a", "vs 2026.03.31(Q1 2026) · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · 1분기 FCF는 −$0.75B(1분기 영업현금흐름이 최근 5년 중 3년 음수) · <a")
# 자본 음수라 자기 이력에 없는 PBR 칸: '계산 불가' · '자본 음수 · 평균 제외'(옛 카드, 2026-10-01)
one("    if (f('cur')) f('cur').textContent = '—';\n    if (f('badge')) { f('badge').className = 'hist-badge mid'; f('badge').textContent = '계산 불가'; }",
    "    if (f('cur')) f('cur').textContent = '계산 불가';\n    if (f('badge')) { f('badge').className = 'hist-badge mid'; f('badge').textContent = '자본 음수 · 평균 제외'; }")
one('뒤집어 점수로 썼고 PBR를 뺀 4개를 평균했다.', '뒤집어 점수로 썼고 네 개를 평균했다(PBR은 자본 음수로 제외).')
# 분기 차트 아래 설명(옛 카드)
one('<canvas id="pmRevChart"></canvas>\n    </div>\n', '<canvas id="pmRevChart"></canvas>\n    </div>\n'
    '    <div class="yoy-footnote" style="margin-top:8px;">2024년 4분기 순손실은 캐나다 관계회사 RBH 지분 손상 $2,316M(비현금, FY2025 10-K) 때문이다. 2026년 2분기 순이익에도 RBH 지분 추가 손상 $511M(주당 $0.33)이 들어 있다. 1분기 영업현금흐름은 최근 5년 중 3년이 음수였다(2026년 −$399M).</div>\n')
''']
