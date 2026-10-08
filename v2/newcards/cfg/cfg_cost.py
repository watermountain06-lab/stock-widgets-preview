# COST v2 카드 설정 — fill.py COST. 틀 시절 카드를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G6).
# 재현 모드: python3 v2/newcards/build.py COST --from-card (일봉·이동평균·백테스트는 지금 카드에서).
BUILD = {}
CIK = '0000909832'
CUR, YO, QO = '2026-08-30', '2025-08-31', '2026-05-10'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
RELEASE = {'rev': 95723, 'op': 3801, 'ni': 2998}   # Q4 FY2026(16주) 보도자료 손익계산서(백만 달러, 매출 = 순매출 + 회원비) — quarterly/COST_Q4FY26.md
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Costco'
S_ = 'https://www.sec.gov/Archives/edgar/data/909832/'
SEC = S_
PR = {'q3': S_ + '000090983226000046/costex9918-k52826.htm', 'q2': S_ + '000090983226000025/costex9918-k3526.htm',
      'q1': S_ + '000090983225000164/costex9918-k121125.htm', 'q4fy25': S_ + '000090983225000093/costex9918-k92525.htm',
      'q4': S_ + '000090983226000084/costex9918-k92426.htm', 'div': S_ + '000090983226000041/costex9918-k41526.htm'}
PR_CUR = 'q4'
TENQ = S_ + '000090983226000093/cost-20260830.htm'; TENQ_NAME = 'FY2026 10-K'
FY_ENDS = ('2026-08-30', '2025-08-31')
REQ_MULT_EXACT = True   # 옛 카드는 요구 성장률 배수를 실제 값으로 적었다("지난 5년 실제의 5배")
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
FAIRBAND_TITLE = 'id="costFairBand"'   # 옛 카드는 적정주가 칸에 설명(title)이 없었다
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('R&amp;D (Q4 FY26)', '해당 없음', '연구개발비를 따로 공시하지 않는다')
OPM_RANGE, Y2 = (0, 6), (0, 6)
NEXT = ('12월 중순 예상', '일정 · Q1 FY27 (회사 미확정)')
NEXT_OP = ('12월 중순', 'Q1 FY27 예상')
FY_LABEL = 'FY2026'
HEALTH_NOTE = '유동비율 {FR[\'currentRatio\']:.1f}%, 재고($19.3B)를 뺀 당좌비율 {FR[\'quickRatio\']:.1f}%다. 창고형 유통은 재고를 매입 대금 지급 전에 파는 구조라(매입채무 $22.6B > 재고 $19.3B) 유동비율이 낮게 나온다. 차입금은 장기 사채 등 $6.2B이고 그중 2027년 5·6월 만기 $2.25B는 유동부채다. 연말 단기차입금은 없다(10-K). 현금·단기투자는 $21.3B라 순현금이다. FY2026 이자보상배율은 영업이익 $11.7B ÷ 이자비용 $0.15B(약 81배)다.'
YOY_EXTRA = ''
RELEASE_PREV = {'rev': 70527, 'op': 2815, 'ni': 2192}   # 직전 분기(Q3 FY2026, 12주) 보도자료 — 전분기 대비 주당 환산용
SEG = [('식품·잡화', 36163, '#005daa'), ('비식품', 23253, '#e31837'), ('창고 부대사업(주유·약국 등)', 21318, '#3498db'), ('신선식품', 13139, '#f7b600')]   # Q4 = FY2026(10-K Note 11) − Q3 10-Q 36주 누계
SEG_TITLE = '매출 구성 — 제품군별 순매출'
SEG_ADJ = 95723 - 93873   # 회원비 $1,850M(순매출 밖) — 도넛은 순매출 제품군만
SEG_NOTE = '판매 마진은 얇고 회원비 수익이 영업이익의 약 절반 규모다 · 4분기 회원비 $1.85B(순매출 밖)는 영업이익 $3.80B의 49%에 해당한다 · 4분기 품목별 매출은 10-K 연간 값에서 3분기 누계를 뺀 값이다 · 출처: <a href="https://www.sec.gov/Archives/edgar/data/909832/000090983226000093/cost-20260830.htm" target="_blank" rel="noopener">FY2026 10-K (SEC) →</a>'
CAPITAL = [('자사주 매입 (Q4 FY26, 25.3만 주)', '$0.24B'), ('잔여 바이백 승인 한도 (2026.08.30 기준, $4B 한도 2027년 1월 만료)', '$1.12B'), ('배당 (Q4 FY26 선언, 7/7)', '분기 $1.47(4월 13% 인상)', '$0.65B')]
CHECK_WHEN = '2026년 12월 중순 (예상) · Q1 FY27'
CHECK = ['Q1 FY27 실적(12월 중순 예상) — 4분기의 관세 환급 일회성 이익(주당 $0.15)이 빠진 뒤의 이익 증가율', '유가·환율을 뺀 비교매출 증가율(4분기 +6.7%, 연간 +6.6%)이 이어지는지', '회원비 증가(4분기 $1.85B, +7.3%)와 디지털 매출(4분기 비교 +19.5%)', 'FY2027 계획 — 설비투자 약 $7.5B, 신규 창고 최대 33곳(10-K)']
NONOP_WHAT = '지분·장기투자'
PH = ['WMT', 'TGT', 'DG', 'DLTR', 'KR', 'SYY']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '대형 유통 PER 비교', 'pbr': '대형 유통 PBR 비교', 'psr': '대형 유통 PSR 비교', 'pcr': '대형 유통 PCR(FCF) 비교', 'evebitda': '대형 유통 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&amp;P500 필수소비재 34종목보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 34종목 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
FUND_ASOF_NOTE = 'FY2026 10-K (2026-10-07 공시)'
PREMISE = '자기 5년 이력으로는 중간({selfsc:.1f}점)이다 — 다섯 배수 모두 5년 중앙값 근처다(PER {SM[\'PER\'][\'current\']:.1f}배, 5년 범위 {SM[\'PER\'][\'min\']:.0f}~{SM[\'PER\'][\'max\']:.0f}배). S&P500 필수소비재 34종목 안에서는 비싼 쪽({peersc:.1f}점)이다. <strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.'
RISK = '매출이 지난 5년 속도(연 {pct(HIST[\'growth_5y\'])})로 크다가 식는다면, 현재가가 정당하려면 영업이익률이 <strong data-vs="req">{pct(DCF[\'requiredMargin\'])}</strong>여야 한다(최근 4분기 {pct(HIST[\'margin_now\'])}, 5년 중앙값 {pct(HIST[\'margin_5y\'])}). 지금의 약 {DCF[\'requiredMargin\'] / HIST[\'margin_now\']:.0f}배이고, 지난 5년 분기 영업이익률은 3.1~4.0% 사이였다. 성장만으로 맞추려면 연 {DCF[\'requiredGrowth\'] * 100:.0f}%가 필요하다.'
FUND_TIP = '영업이익률 {FR[\'opMargin\']:.1f}%({FPT[\'opMargin\']}점)는 창고형 유통의 얇은 판매 마진 때문이고, 회원비 수익이 영업이익의 약 절반 규모다.'
SELF_TIP = "다섯 배수 모두 5년 백분위 {min(v['percentile'] for v in SM.values()):.0f}~{max(v['percentile'] for v in SM.values()):.0f}%로 중앙값 근처다. 코스트코는 5년 내내 PER {SM['PER']['min']:.0f}~{SM['PER']['max']:.0f}배였기 때문에 '중간'이 싸다는 뜻은 아니다."
PEER_TIP = ('S&P500 필수소비재 34종목과 배수 순위를 매긴 값이다(카드 유니버스 필수소비재가 적어 넓혔다).', '식품·음료·생활용품 제조사와 유통이 섞여 있다. 유통은 마진이 얇아 PSR이 낮게 나오고, 1분기가 16주인 KR는 최근 4분기 합계를 못 만들어 PER·PSR·PCR·EV/EBITDA가 빠져 있다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.', '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.', '3년 성장률(연 {pct(HIST[\'growth_3y\'])})에서 식고, 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.09 ~ 2026.09'
NEWS = [('', '2026년 9월 24일 장 마감 후 — Q4 FY2026 실적', '2026-09-25', '4분기(16주) 순매출 $93.9B(+11.2%)·EPS $6.75(관세 환급 일회성 $0.15 포함) · 연간 EPS $20.76(+14%) · 비교매출 +9.4%(유가·환율 제외 +6.7%) · 창고 939곳', 'q4', 'Costco 실적 보도자료 (SEC 8-K)'), ('', '2026년 5월 28일 장 마감 후 — Q3 FY2026 실적', '2026-05-29', '순매출 $69.15B(+11.6%) · EPS $4.93(+15%) · 비교매출 +9.8%(조정 +6.6%) · 디지털 +21.5%', 'q3', 'Costco 실적 보도자료 (SEC 8-K)'), ('', '2026년 4월 15일 장 마감 후 — 배당 인상', '2026-04-16', '분기 배당 $1.30 → $1.47(+13%, 연 $5.88)', 'div', 'Costco 공시 (SEC 8-K)'), ('', '2026년 3월 5일 장 마감 후 — Q2 FY2026 실적', '2026-03-06', '순매출 $68.24B(+9.1%) · EPS $4.58(+14%) · 비교매출 +7.4%(조정 +6.7%)', 'q2', 'Costco 실적 보도자료 (SEC 8-K)'), ('', '2025년 12월 11일 장 마감 후 — Q1 FY2026 실적', '2025-12-12', '순매출 $65.98B(+8.2%) · EPS $4.50(주식보상 세금 이익 $0.16 포함) · 비교매출 +6.4%', 'q1', 'Costco 실적 보도자료 (SEC 8-K)'), ('', '2025년 9월 25일 장 마감 후 — Q4 FY2025 실적', '2025-09-26', '4분기(16주) 순매출 $84.4B(+8.0%)·EPS $5.87 · 연간 EPS $18.21(+10%)', 'q4fy25', 'Costco 실적 보도자료 (SEC 8-K)')]
SUMMARY = ('실적은 매 분기 좋아졌지만 주가는 1년 전 수준이다', '안정 성장·높은 배수', ['FY2026 순매출이 $297.2B로 10.1%, 순이익이 $9.2B로 14% 늘었다. 유가·환율을 뺀 비교매출은 연간 +6.6%였다.', '회원비 수익이 연간 $5.9B로 11% 늘었고, 영업이익($11.7B)의 약 절반 규모다.', '주가는 5월 고점(종가 $1,094)에서 {(1 - px / 1094.32) * 100:.0f}% 내려와 1년 전보다 {abs(ch):.1f}% {"높다" if ch > 0 else "낮다"}. PER은 여전히 {SM[\'PER\'][\'current\']:.0f}배다.'], '4분기 이익에는 관세 환급 일회성 이익(주당 $0.15)이 들어 있다. 영업이익률은 {HIST[\'margin_now\'] * 100:.0f}% 안팎이라 성장률이 조금만 꺾여도 배수가 흔들릴 수 있다.', 'Q1 FY27 실적(12월 중순 예상)의 비교매출과 회원비, 관세 환급 일회성 이익이 빠진 뒤의 이익 증가율.')
BULL = [('성장', 'FY2026 순매출 +10.1%, 순이익 +14%로 이익이 매출보다 빨리 늘었다.'), ('회원', '회원비 수익이 연간 $5.9B(+11%)로 영업이익의 약 절반 규모다.'), ('재무', '현금·단기투자 $21.3B가 차입금 $6.2B보다 많다(FY2026 말).')]
BEAR = [('밸류', '기본 내재가치가 현재가의 {DCF[\'base\'] / px * 100:.0f}%이고, 동종업 34종목 중 PCR·EV/EBITDA가 가장 비싼 쪽이다.'), ('마진', '현재가가 정당하려면 영업이익률 {pct(DCF[\'requiredMargin\'])}가 필요한데 지금은 {pct(HIST[\'margin_now\'])}다.'), ('일회성', '4분기 EPS $6.75에는 관세 환급 일회성 이익 $0.15가 들어 있다.')]
ANALYST = {'rating': 'Buy', 'n': 39, 'nt': 25, 'mean': 1084.48, 'median': 1095, 'low': 781, 'high': 1315, 'sb': 20, 'b': 4, 'h': 13, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-10-06'
PRE = [r'''
FR = {r_['metric']: r_['value'] for ax_ in FUND['axes'].values() for r_ in ax_.get('rows', [])}   # 기본적 분석 지표 값·점수(E26)
FPT = {r_['metric']: r_['points'] for ax_ in FUND['axes'].values() for r_ in ax_.get('rows', [])}
''']
POST = [r'''
# 분기 표기(12주·16주)·매출 정의(옛 카드 두 각주), 보도자료 이름은 회계연도 표기 — 분기 변수(CUR·QLABEL 등)로 써서 분기마다 이 블록은 그대로 둔다(2026-10-08)
_d = lambda x: x.replace('-', '.')
_w = lambda q: '16주' if q.startswith('Q4') else '12주'   # 코스트코 회계 규칙: 1~3분기 12주, 4분기 16주
_fy = lambda q: q.replace(' FY', ' FY20')
def _qoq_week():   # 16주 분기와 12주 분기를 견주면 증가율이 기간 차이만큼 커 보인다 — 주당(週當) 환산을 함께 적는다(Fable 2026-10-08)
    wc, wp = (16 if C.QLABEL.startswith('Q4') else 12), (16 if C.QQL.startswith('Q4') else 12)
    if wc == wp:
        return ''
    g = {k: (C.RELEASE[k] / wc) / (C.RELEASE_PREV[k] / wp) - 1 for k in ('rev', 'op', 'ni')}
    return f"{wc}주 대 {wp}주 비교라 주당 환산으로는 매출 {g['rev'] * 100:+.1f}%·영업이익 {g['op'] * 100:+.1f}%·순이익 {g['ni'] * 100:+.1f}% · "
one(f"기준일: {_d(C.CUR)}({C.QLABEL}) vs {_d(C.YO)}({C.YL}) · GAAP 기준 · ", f"기준일: {_d(C.CUR)}({C.QLABEL}, {_w(C.QLABEL)}) vs {_d(C.YO)}({C.YL}, {_w(C.YL)}) · GAAP 기준 · 매출은 순매출 + 회원비 · ")
one(f"기준일: {_d(C.CUR)}({C.QLABEL}) vs {_d(C.QO)}({C.QQL}) · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · <a", f"기준일: {_d(C.CUR)}({C.QLABEL}, {_w(C.QLABEL)}) vs {_d(C.QO)}({C.QQL}, {_w(C.QQL)}) · GAAP 기준 · 매출은 순매출 + 회원비 · FCF는 영업현금흐름 − 설비투자 · " + _qoq_week() + C.YOY_EXTRA + "<a")
h = h.replace(f'Costco {C.QLABEL} 실적 보도자료 (SEC 8-K)', f'Costco {_fy(C.QLABEL)} 실적 보도자료 (SEC 8-K)')
one(f'매출 구성 — 제품군별 순매출 ({C.QLABEL} · {_d(C.CUR)} 기준)', f'매출 구성 — 제품군별 순매출 ({C.QLABEL} · {_d(C.CUR)} 기준, {_w(C.QLABEL)})')
# 분기 차트 아래 설명(옛 카드)
one('<canvas id="costRevChart"></canvas>\n    </div>\n', '<canvas id="costRevChart"></canvas>\n    </div>\n'
    '    <div class="yoy-footnote" style="margin-top:8px;">회계연도는 9월 초에 시작하고 1~3분기는 12주, 4분기는 16주다(4분기 막대가 큰 이유). 매출은 순매출 + 회원비다.</div>\n')
''']
