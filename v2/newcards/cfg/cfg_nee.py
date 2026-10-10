# NEE(넥스트에라 에너지) v2 카드 설정 — _core_fill.py NEE. 회계연도 12월 31일. 시총 82위(S&P500 현재 시총 순, 루트 카드 없음).
# 배열은 v2/new_ticker_arrays.py(Yahoo 일봉, 2020-10-27 4:1 분할은 KNOWN_SPLITS). 출처: SEC XBRL(+ 2분기 10-Q 인라인 XBRL 보충), Q2 2026 10-Q(2026-07-24),
# 실적 보도자료(Q3 2025~Q2 2026), 8-K(투자자 설명회 12/8, Dominion Energy 합병 합의 5/15, 합병 진행 8/11·8/25·9/14), StockAnalysis.
# 엔진 수정(2026-10-02): 총매출 = RegulatedAndUnregulatedOperatingRevenue(옛 태그는 0.1B 반올림 주석 값), 설비투자·이자비용은 회사 고유 태그라 없음
# (PCR 계산 불가, 이자비용은 v2/interest_extra.json 손입력). 비교군 S&P500 유틸리티(SECTOR_UNIVERSE Utilities).
BUILD = {'overlay': True}
CIK = '0000753308'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
RELEASE = {'rev': 7534, 'op': 2238, 'ni': 3144}
VOTES, VERDICT = (1, -1, -2), '적정~고평가'
CO = 'NextEra Energy'
S_ = 'https://www.sec.gov/Archives/edgar/data/753308/'
SEC = S_
PR = {'q2': S_ + '000075330826000058/neeq22026exhibit99.htm', 'q1': S_ + '000075330826000028/neeq12026exhibit99.htm',
      'q4': S_ + '000075330826000007/neeq42025exhibit99.htm', 'q3': S_ + '000075330825000055/neeq32025exhibit99.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000075330826000060/nee-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
LINKS = {'dom': S_ + '000110465926063001/tm2614888d1_ex99-1.htm', 'va': S_ + '000110465926107537/tm2625368d1_8k.htm',
         'inv': S_ + '000075330825000064/nee-20251208.htm', '_unused': S_}
FAIRBAND_TITLE = 'id="neeFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다. 최근 4분기 GAAP EPS(${eps_ttm})가 회사 조정 EPS(2026년 전망 $3.92~4.02)보다 높아(헤지 평가손익·원전 해체 기금 평가손익 등) 범위가 현재가 위에 있다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (10, 45), (0, 50)
FCF_SUB = '설비투자가 회사 고유 태그라 표준 데이터로 계산하지 않음 · FPL 2분기 설비투자 약 $2.8B'
CAPEX_SUB = '회사 고유 태그(표준 데이터 없음)'
STAT3 = ('조정 EPS (Q2 2026)', '$1.15', '+9.5% · 회사 조정 · GAAP $1.50')
NEXT = ('10월 하순 예상', '일정 · Q3 2026 (회사 미확정)'); NEXT_OP = ('10월 하순', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
HEALTH_NOTE = ('차입금은 $110.2B(기업어음 $1.7B + 기타 단기 $4.3B + 1년 안 만기 $5.4B + 장기 $98.8B)이고 현금은 $2.9B, 자회사 소수주주 지분은 $11.0B다. '
               '5월 15일 Dominion Energy와 합병(Dominion 1주당 NEE 0.8138주 + 총 $3.6억 현금 비례 배분)하기로 했고, 회사는 2027년 하반기 완료를 예상한다. 합병 뒤 NEE 주주가 약 74.5%를 가진다.')
ACT_REASON = '매출원가 합계 표준 태그가 없음(유틸리티 — 연료·운영비를 따로 공시)'
YOY_EXTRA = 'FPL 매출 +4%, NEER 매출 +32% · 조정 EPS +9.5% · GAAP 순이익 +55%(헤지 평가손익·원전 해체 기금 평가손익 등) · '
SEG = [('FPL(플로리다 전력)', 4896, '#0a7c3e'), ('NEER(재생에너지 등)', 2532, '#3fbf6f'), ('본사·기타', 106, '#94a3b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 사업부별 매출'
SEG_NOTE = ('1년 전보다 FPL +4%, NEER +32% · FPL 규제 자본 약 +9.3%, NEER 2분기 수주 3.6GW · '
            '출처: <a href="{TENQ}" target="_blank" rel="noopener">Q2 2026 10-Q (SEC) →</a>')
CAPITAL = [('배당 지급 (상반기)', '$2.6B'),
           ('자사주 매입', '없음'),
           ('주당 배당 성장 목표', '2026년까지 연 약 10%', '2027~2028년 연 6%')]
CHECK_WHEN = '2026년 10월 하순 (예상) · Q3 2026'
CHECK = ['2026년 조정 EPS 전망 $3.92~4.02(상단 목표)와 2032년까지 연 8% 이상 성장 목표',
         'Dominion Energy 합병 — 규제 승인과 2027년 하반기 완료 목표(9월 버지니아 혜택안 강화)',
         'NEER 재생에너지·저장장치 수주(2분기 3.6GW)와 FPL 규제 자본 성장',
         '차입금 $110.2B와 합병 뒤 신용등급']
NONOP_WHAT = '투자'
PH = ['DUK', 'SO', 'D', 'AEP', 'CEG', 'VST']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '대형 유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': '대형 유틸리티 PBR 비교', 'psr': '대형 유틸리티 PSR 비교',
                'pcr': '대형 유틸리티 PCR(FCF) 비교', 'evebitda': '대형 유틸리티 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-07-24 공시, 인라인 XBRL 보충)'
PREMISE = ('GAAP EPS가 크게 늘어 PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PSR·PBR이 5년 중 싼 쪽이고 EV/EBITDA도 중앙값보다 조금 싸 자기 이력 {selfsc:.1f}점(싸다)이다(PCR은 설비투자 태그가 없어 없음). '
           'S&P500 유틸리티 안에서는 PER만 싼 쪽이고 PBR·PSR·EV/EBITDA는 가장 비싼 쪽이라 {peersc:.1f}점(비싸다)이다. '
           '<strong>현금흐름 내재가치는 세 시나리오 모두 음수</strong>다.')
RISK = ('세 칸이 {VOTES_TXT}, 합계 {TOTAL_TXT} “{VERDICT}”다. 현금흐름 {sgn(VOTES[2])}{jo(VOTES[2], \'은\', \'는\')} 투하자본이익률(약 {DCF[\'hardDetail\'][\'roic\'] * 100:.0f}%)이 할인율 10%보다 크게 낮아 성장할수록 가치가 줄고, 차입금 $110.2B와 소수주주 지분 $11.0B를 빼기 때문이다. '
        '유틸리티는 규제 수익률로 자본을 늘려 이익을 내는 구조라 이 모델과 잘 맞지 않는다. 자기 이력 {sgn(VOTES[0])}{jo(VOTES[0], \'은\', \'는\')} GAAP EPS에 헤지·원전 해체 기금 평가손익 등이 들어 PER이 낮아진 영향이 크다(조정 EPS 기준 PER 약 {px / 3.97:.0f}배).')
FUND_TIP = '유동비율·당좌비율은 유틸리티 특성상 낮다. 이자보상배율은 이자비용이 회사 고유 태그라 10-Q 손익계산서 값($487M, 금리 파생상품 평가손익 포함)을 손으로 넣었다. 차입금의존도는 기업어음·기타 단기차입($6.0B)을 포함한 값이다. 순이익률이 높은 것은 헤지·원전 해체 기금 평가손익 등 영업 밖 이익 때문이다.'
SELF_TIP = 'PER {SM[\'PER\'][\'current\']:.1f}배는 GAAP EPS 기준이다(조정 EPS 기준 약 {px / 3.97:.0f}배). PCR은 설비투자를 표준 데이터로 구할 수 없어 계산하지 않는다.'
PEER_TIP = ('S&P500 유틸리티(NEE 제외 30종목)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스·수도와 발전 회사가 섞여 있다. NEE는 재생에너지 사업이 커서 매출·자본 대비 배수가 가장 높은 편이다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})으로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})로 시작해 식고, 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}에서 5년에 걸쳐 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '매출이 3년 성장률(최근 4분기 합 기준, 연 {pct(HIST[\'growth_3y\'])})로 시작해 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('세 시나리오 모두 음수다. 투하자본이익률(약 {DCF[\'hardDetail\'][\'roic\'] * 100:.0f}%)이 할인율 10%보다 낮아 성장에 드는 투자가 버는 돈보다 크고, 최근 증분 매출/자본을 구하지 못해 이력 평균을 쓴다. '
            '설비투자 태그가 없어 재투자는 매출/자본으로만 잡혔다. Dominion Energy 합병은 넣지 않았다.')
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 14일 — 버지니아 혜택안 강화', None,
     'Dominion Energy와 합병 관련 버지니아 고객 혜택안을 늘려 발표', 'va', 'NextEra Energy 공시 (SEC 8-K)'),
    ('neutral', '2026년 7월 24일 장 시작 전 — Q2 2026 실적', '2026-07-24',
     '매출 $7.5B(+12%) · EPS $1.50(조정 $1.15, +9.5%) · NEER 수주 3.6GW · 당일 주가 0.0%', 'q2', 'NextEra Energy 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 18일 — Dominion Energy 합병 발표(5/15 합의)', '2026-05-18',
     'Dominion 1주당 NEE 0.8138주 + 총 $3.6억 현금 — 합병 뒤 NEE 주주 약 74.5% · 발표 때 완료까지 12~18개월 예상 · 당일 주가 −4.6%', 'dom', 'NextEra Energy·Dominion 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 23일 장 시작 전 — Q1 2026 실적', '2026-04-23',
     '매출 $6.7B · EPS $1.04(조정 $1.09, +10%) · NEER 수주 4GW(분기 최대) · 당일 주가 +6.9%', 'q1', 'NextEra Energy 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 27일 장 시작 전 — Q4 2025 실적', '2026-01-27',
     'EPS $0.73(조정 $0.54) · 연간 조정 EPS $3.71 · 당일 주가 +2.0%', 'q4', 'NextEra Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 8일 — 투자자 설명회', None,
     '2026년 조정 EPS 전망을 $3.92~4.02로 올리고 2032년까지 성장 목표 연장', 'inv', 'NextEra Energy 공시 (SEC 8-K)'),
    ('red', '2025년 10월 28일 장 시작 전 — Q3 2025 실적', '2025-10-28',
     'EPS $1.18(조정 $1.13, +9.7%) · Google과 원전(Duane Arnold) 재가동 협력 · 당일 주가 −2.9%', 'q3', 'NextEra Energy 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('조정 EPS가 연 10% 가까이 늘고 Dominion Energy와 합병하기로 한 가운데, 주가는 1년 새 {CH_TXT}', 'Dominion 합병·재생에너지',
           ['2분기 매출 $7.5B(+12%) 가운데 FPL이 $4.9B(+4%), 재생에너지 중심 NEER가 $2.5B(+32%)였다.',
            '5월 Dominion Energy와 합병(주식 교환 중심)에 합의했고 발표 날 주가가 −4.6%였다. 합병 뒤 NEE 주주가 약 74.5%를 가진다.',
            'GAAP EPS는 헤지·원전 해체 기금 평가손익 등으로 조정 EPS보다 높다(2분기 $1.50 대 $1.15).'],
           '자기 이력으로는 GAAP PER이 낮아 싸지만 유틸리티 안에서는 비싸고, 현금흐름 모델은 음수다.',
           'Q3 2026 실적(10월 하순 예상)과 Dominion 합병 승인 일정.')
BULL = [('성장', '조정 EPS +9.5%, 2032년까지 연 8% 이상 목표.'),
        ('재생에너지', 'NEER 분기 수주 3.6~4GW.'),
        ('배당', '2026년까지 주당 배당 연 약 10% 성장 목표.')]
BEAR = [('합병 위험', 'Dominion 합병 규제 승인 불확실, 발표일 −4.6%.'),
        ('부채', '차입금 $110.2B.'),
        ('밸류에이션', '유틸리티 안에서 PBR·PSR·EV/EBITDA 가장 비싼 쪽.')]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 16, 'mean': 97.63, 'median': 102, 'low': 56, 'high': 112, 'sb': 11, 'b': 3, 'h': 6, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-10'
