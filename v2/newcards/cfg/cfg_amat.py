# AMAT(어플라이드 머티어리얼즈) v2 카드 설정 — fill.py AMAT. 회계연도 10월 마지막 일요일(Q3 FY26 = 2026-04-27~07-26).
# 틀 시절 카드(2026-09 루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G2).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-08-20), 실적 보도자료(Q4 FY25~Q3 FY26), 8-K(인력 감축 10/23, BIS 합의 2/11), StockAnalysis(2026-09-28).
# 재현 모드: python3 v2/newcards/build.py AMAT --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-29).
CIK = '0000006951'
CUR, YO, QO = '2026-07-26', '2025-07-27', '2026-04-26'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
RELEASE = {'rev': 9115, 'op': 3075, 'ni': 2538}   # Q3 FY26 10-Q 손익계산서(백만 달러, 부문 합 9,115와 같다)
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Applied Materials'
S_ = 'https://www.sec.gov/Archives/edgar/data/6951/'
SEC = S_
PR = {'q3': S_ + '000162828026056699/exhibit991q32026earningsre.htm', 'q2': S_ + '000162828026035071/exhibit991q22026earningsre.htm',
      'q1': S_ + '000162828026007661/exhibit991q12026earningsre.htm', 'q4': S_ + '000162828025051998/exhibit991q42025earningsre.htm'}
PR_CUR = 'q3'
TENQ = S_ + '000162828026058235/amat-20260726.htm'; TENQ_NAME = 'Q3 FY2026 10-Q'
LINKS = {'bis': S_ + '000162828026007444/amat-20260211.htm', 'layoff': S_ + '000162828025046107/amat-20251023.htm'}
FAIRBAND_TITLE = ('id="amatFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 GAAP EPS(회사가 밝힌 일회성 세금 2건은 이력 EPS에서 뺐다). '
                  '5년 PER 중앙값({SM[\'PER\'][\'median\']:.1f}배)과 다른 창이다. 비GAAP EPS 기준이면 밴드가 약 6% 낮다."')
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (마진 100%로도 불가)</span>'
OPM_RANGE, Y2 = (15, 40), (15, 40)
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('R&amp;D (Q3 FY26)', '$1.1B', '매출의 12.1%')
NEXT = ('11월 중순 예상', '일정 · Q4 FY26 (회사 미확정)'); NEXT_OP = ('11월 중순', 'Q4 FY26 예상')
FY_ENDS, FY_LABEL = ('2025-10-26', '2024-10-27'), 'FY2025'
HEALTH_NOTE = ('유동비율 242.3%, 재고($6.6B)를 뺀 당좌비율 178.9%다. 차입금은 $6.5B(단기 $1.3B — 1년 안 만기 사채 $1.2B + 기업어음 $0.1B, 장기 $5.2B)이고 '
               '현금·단기투자는 $9.2B, 장기투자는 $5.3B다. 매출채권이 $7.7B로 연초($5.2B)보다 48% 늘었다.')
ACT_REASON = ''
YOY_EXTRA = '2분기 순이익에는 전략 투자 이익 등 영업외 이익이 들어 있다 · '
SEG = [('반도체 장비(Semiconductor Systems)', 7040, '#569bbe'), ('글로벌 서비스(AGS)', 1781, '#f7b600'), ('디스플레이·기타', 294, '#9b59b6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별 매출'
SEG_NOTE = ('반도체 장비 매출 중 파운드리·로직 67% · D램 26% · 낸드 7%, 부문 영업이익률 37.7% · 지역별로 중국이 28%(1년 전 35%) · 출처: '
            '<a href="{PR[\'q3\']}" target="_blank" rel="noopener">Q3 FY2026 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (Q3 FY26)', '$0.44B'),
           ('잔여 바이백 승인 한도 (2026.07.26 기준)', '약 $12.8B'),
           ('배당 (Q3 FY26)', '분기 $0.53(5월 15% 인상, 9년 연속)', '$0.42B')]
CHECK_WHEN = '2026년 11월 중순 (예상) · Q4 FY26'
CHECK = ['4분기 가이던스 매출 $10.25B(±$0.5B)·비GAAP EPS $4.02(±$0.20) 달성 — 3분기보다 매출 약 12% 많은 수준',
         '회사가 "또 한 번의 강한 성장"이라고 한 2027년 전망의 구체화',
         '반도체 장비 부문 D램 비중(3분기 26%)과 중국 매출 비중(28%)의 변화',
         '매출채권 증가(연초 대비 +48%)와 영업현금흐름']
NONOP_WHAT = '지분·장기투자'   # 옛 카드 JS가 쓰던 표기(정적 문구 "장기투자 $5.3B"는 JS가 덮어썼다)
PH = ['LRCX', 'KLAC', 'ASML', 'TSM', 'MU', 'NVDA']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '반도체 장비·주요 고객 PER 비교', 'pbr': '반도체 장비·주요 고객 PBR 비교', 'psr': '반도체 장비·주요 고객 PSR 비교',
                'pcr': '반도체 장비·주요 고객 PCR(FCF) 비교', 'evebitda': '반도체 장비·주요 고객 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'GICS Information Technology 대비 배수 순위'
FUND_ASOF_NOTE = 'Q3 FY26 10-Q (2026-08-20 공시)'
PREMISE = ('다섯 배수 모두 자기 5년 이력의 상위 {100 - min(v_[\'percentile\'] for v_ in SM.values()):.0f}% 안이라 {selfsc:.1f}점이다(PER {SM[\'PER\'][\'current\']:.1f}배, 5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배; EV/EBITDA는 5년 최고). '
           '카드 유니버스 IT 종목 안에서는 중간({peersc:.1f}점, 동종업 가격 기준일 9/11)이다. PER은 GAAP EPS(9개월 지분투자 평가이익 $927M 포함) 기준이고, '
           '비GAAP 최근 4분기 EPS $10.91로는 약 {px / 10.91:.0f}배다. <strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다. '
           '주가는 1년 새 {ch:.0f}% 올랐다가 6월 말 고점(종가 $723)에서 {(1 - px / 723.0) * 100:.0f}% 내려왔다.')
RISK = ('이 모델로는 영업이익률을 100%로 잡아도 현재가에 닿지 않는다 — 현재가가 최근 4분기 매출의 약 {SM[\'PSR\'][\'current\']:.0f}배라서다. '
        '일정 성장으로 맞추려면 5년간 연 {pct(DCF[\'requiredGrowth\'])}가 필요하다(지난 5년 실제 연 {pct(HIST[\'growth_5y\'])}). '
        '회사의 4분기 가이던스 매출 $10.25B는 1년 전 분기보다 51% 많고, 회사는 2027년에도 강한 성장을 예상한다고 밝혔다. '
        '낙관 시나리오가 기본과 거의 같은 것은 최근 3년 성장률({pct(HIST[\'growth_3y\'])})이 5년 값보다 낮아서다.')
FUND_TIP = '순이익률 27.8%(5점)·유동성이 점수를 끌어올렸고, 매출 3년 연 증가율 3.2%·영업이익 2.1%는 연간(FY2025까지) 기준이라 2026년 급증이 아직 안 들어갔다.'
SELF_TIP = '다섯 배수 모두 5년 백분위 {min(v_[\'percentile\'] for v_ in SM.values()):.0f}~{max(v_[\'percentile\'] for v_ in SM.values()):.0f}%로 가장 비싼 쪽이다. EV/EBITDA {SM[\'EV/EBITDA\'][\'current\']:.1f}배는 5년 최고치다.'
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(연 {pct(HIST[\'growth_3y\'])})에서 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('', '2026년 8월 13일 장 마감 후 — Q3 FY2026 실적', '2026-08-14',
     '매출 $9.12B(사상 최대, 회사 역사상 최대 전 분기 대비 증가)·GAAP EPS $3.17(비GAAP $3.50) · 영업이익률 33.7% · 4분기 가이던스 $10.25B · 2027년도 강한 성장 예상', 'q3', 'Applied Materials 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 5월 14일 장 마감 후 — Q2 FY2026 실적', '2026-05-15',
     '매출 $7.91B(사상 최대)·GAAP EPS $3.51(비GAAP $2.86) · 2026년 반도체 장비 사업 30% 넘게 성장 예상 · 배당 15% 인상($0.53)', 'q2', 'Applied Materials 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 2월 12일 장 마감 후 — Q1 FY2026 실적', '2026-02-13',
     '매출 $7.01B·GAAP EPS $2.54(비GAAP $2.38) · 2026년 반도체 장비 사업 20% 넘게 성장 예상', 'q1', 'Applied Materials 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 11일 장 마감 후 — 미국 상무부(BIS) 합의', '2026-02-12',
     '중국 고객 출하·수출통제 준수 조사 합의, $252.5M 일시 납부 · 법무부·SEC 조사는 조치 없이 종결', 'bis', 'Applied Materials 공시 (SEC 8-K)'),
    ('', '2025년 11월 13일 장 마감 후 — Q4 FY2025 실적', '2025-11-14',
     'FY2025 매출 $28.4B(+4%, 6년 연속 성장)·EPS $8.66 · 4분기 매출 $6.80B(−3%) · 2026년 하반기 수요 증가 대비', 'q4', 'Applied Materials 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 23일 장 마감 후 — 인력 감축 계획', '2025-10-24',
     '전 세계 인력의 약 4% 감축, 비용 $160~180M(대부분 퇴직금)', 'layoff', 'Applied Materials 공시 (SEC 8-K)'),
]
SUMMARY = ('AI 반도체 투자 확대로 매출이 분기마다 사상 최대를 경신했다', '고성장·밸류 부담',
           ['3분기 매출이 $9.12B로 1년 전보다 25% 늘었고, 4분기 가이던스는 $10.25B다.',
            '회사는 2026년 반도체 장비 사업 성장 전망을 1분기 "20% 넘게"에서 2분기 "30% 넘게"로 올렸고, 3분기에 한 번 더 올렸다.',
            '주가는 1년 새 {ch:.0f}% 올랐고, 6월 말 고점(종가 $723)에서 {(1 - px / 723.0) * 100:.0f}% 내려와 있다.'],
           '현재가는 최근 4분기 매출의 약 {SM[\'PSR\'][\'current\']:.0f}배로, 모델에서는 영업이익률 100%로도 설명되지 않는다. 2월에 수출통제 관련으로 상무부에 $252.5M를 냈고, 중국 매출 비중은 28%다.',
           'Q4 FY26 실적(11월 중순 예상)의 가이던스 달성과 2027년 전망.')
BULL = [('성장', '3분기 매출 +25%, 4분기 가이던스는 1년 전보다 51% 많은 $10.25B다.'),
        ('수익성', '매출총이익률이 13분기 연속 1년 전보다 올랐고, 3분기 영업이익률은 33.7%다.'),
        ('현금', '3분기 영업현금흐름 $3.04B(사상 최대), 자사주 잔여 한도 약 $12.8B.')]
BEAR = [('밸류', '다섯 배수 모두 5년 상위 {100 - min(v_[\'percentile\'] for v_ in SM.values()):.0f}% 안이고, 기본 내재가치는 현재가의 {DCF[\'base\'] / px * 100:.0f}%다.'),
        ('규제', '중국 매출이 28%이고, 2월에 수출통제 관련으로 $252.5M를 냈다.'),
        ('변동성', '주가가 6월 말 고점에서 {(1 - px / 723.0) * 100:.0f}% 내려왔다.')]
ANALYST = {'rating': 'Strong Buy', 'n': 40, 'nt': 27, 'mean': 676.52, 'median': 683, 'low': 500, 'high': 900, 'sb': 29, 'b': 4, 'h': 7, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-06'

REQ_MULT_EXACT = True   # 옛 카드 툴팁: "지난 5년의 6.9배"

# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
POST = [r'''
# 분기 차트 아래 설명(회계연도·3분기 최대 매출·2분기 영업외 이익)
one('<canvas id="amatRevChart"></canvas>\n    </div>\n', '<canvas id="amatRevChart"></canvas>\n    </div>\n'
    '    <div class="yoy-footnote" style="margin-top:8px;">회계연도는 10월 마지막 일요일에 끝난다(Q3 FY26 = 2026년 4~7월). 3분기 매출 $9.12B는 사상 최대이고 1년 전보다 25% 많다. 회사의 4분기 가이던스는 $10.25B(±$0.5B)다. 2분기 순이익이 영업이익보다 큰 것은 전략 투자 평가이익 등 영업외 이익 때문이다.</div>\n')
# 요구 성장률 배수는 소수 한 자리(옛 카드 "6.9배")
for _o in ("${Math.round(d.requiredGrowth / d.growth5y)}배다.`", "${Math.round(D.requiredGrowth / D.growth5y)}배다.`"):
    one(_o, _o.replace('Math.round(', '(').replace('5y)}', '5y).toFixed(1)}'))
# QoQ 각주에도 영업외 이익 설명(옛 카드는 두 각주 모두)
one(f"vs {C.QO.replace('-', '.')}({C.QQL}) · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · <a", f"vs {C.QO.replace('-', '.')}({C.QQL}) · GAAP 기준 · FCF는 영업현금흐름 − 설비투자 · " + C.YOY_EXTRA + "<a")
# 각주 링크 이름(옛 카드: Q3 FY2026)
assert h.count(f'{C.CO} {QL} 실적 보도자료 (SEC 8-K)') == 2
h = h.replace(f'{C.CO} {QL} 실적 보도자료 (SEC 8-K)', f'{C.CO} Q3 FY2026 실적 보도자료 (SEC 8-K)')
# 총자산증가율 메모(옛 카드 표기: 결산일과 "FY2026 10-K 전까지 동일")
one(f'<span class="diag-note">{C.FY_LABEL} 말 ${a1 / 1000:.1f}B(전년 ${a0 / 1000:.1f}B) · 연간 지표</span>', f'<span class="diag-note">{C.FY_LABEL} 말({C.FY_ENDS[0]}) ${a1 / 1000:.1f}B(전년 ${a0 / 1000:.1f}B) · 연간 지표, FY2026 10-K 전까지 동일</span>')
''']
