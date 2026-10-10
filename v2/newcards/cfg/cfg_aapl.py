# AAPL(애플) v2 카드 설정 — fill.py AAPL. 회계연도 9월 마지막 토요일(FY26 = 2025-09-28 ~ 2026-09-26, Q3 FY26 = 2026-06-27). 시총 1~2위(루트 카드 있음).
# 틀 시절 카드(2026-09-24 루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G1).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-07-31), 실적 보도자료(Q4 FY25~Q3 FY26), Apple Newsroom, StockAnalysis(2026-09-23).
# 재현 모드: python3 v2/newcards/build.py AAPL --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-23).
BUILD = {}
CIK = '0000320193'
CUR, YO, QO = '2026-06-27', '2025-06-28', '2026-03-28'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
RELEASE = {'rev': 109417, 'op': 35695, 'ni': 29789}   # Q3 FY26 손익계산서(백만 달러) — SEC XBRL, 옛 카드 뉴스(매출 $109.4B)와 같다
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Apple'
S_ = 'https://www.sec.gov/Archives/edgar/data/320193/'
SEC = S_
PR = {'q3': S_ + '000032019326000018/a8-kex991q3202606272026.htm', 'q2': S_ + '000032019326000011/a8-kex991q2202603282026.htm',
      'q1': S_ + '000032019326000005/a8-kex991q1202612272025.htm', 'q4': S_ + '000032019325000077/a8-kex991q4202509272025.htm'}
PR_CUR = 'q3'
TENQ = S_ + '000032019326000020/aapl-20260627.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
LINKS = {'duo': 'https://www.apple.com/newsroom/2026/09/apple-unveils-iphone-duo/',
         'wwdc': 'https://www.apple.com/newsroom/2026/06/apple-introduces-siri-ai-a-profoundly-more-capable-and-personal-assistant/',
         'ceo': 'https://www.apple.com/newsroom/2026/04/tim-cook-to-become-apple-executive-chairman-john-ternus-to-become-apple-ceo/'}
FAIRBAND_TITLE = 'id="aaplFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (25, 40), (25, 40)
FCF_SUB = '현금창출력'
CAPEX_SUB = '미래 재투자'
STAT3 = ('R&amp;D (Q3 FY26)', '$11.7B', '기술 경쟁력 투자')
NEXT = ('10월 말 예상', '일정 · Q4 FY26'); NEXT_OP = ('10월 말', 'Q4 FY26 예상')
FY_ENDS, FY_LABEL = ('2025-09-27', '2024-09-28'), 'FY25'
HEALTH_NOTE = ('유동비율 {FR[\'currentRatio\']:.1f}%·부채비율 {FR[\'debtToEquity\']:.1f}%는 기준보다 약하지만, 자기자본이 얇은 것은 오랜 자사주 매입 때문이다. '
               'FY25 말(2025.09.27) 이후 상업어음은 $8.0B에서 $2.0B로, 장기차입금(유동 포함)은 $90.7B에서 $82.3B로 줄었고 자기자본은 $73.7B에서 $107.5B로 늘었다(Q3 FY26 10-Q 대차대조표).')
ACT_REASON = ''
YOY_EXTRA = ''
SEG = [('iPhone', 54252, '#c4c8ca'), ('Services', 30739, '#3498db'), ('Mac', 10352, '#a6acaf'), ('Wearables·Home·Acc.', 7883, '#767f83'), ('iPad', 6191, '#5c6282')]
SEG_ADJ = 0   # 다섯 제품·서비스 합 = 보고 매출 109,417
SEG_TITLE = '매출 구성 — 제품·서비스'
SEG_NOTE = '출처: <a href="{TENQ}" target="_blank" rel="noopener">Apple Q3 FY26 Form 10-Q (SEC) →</a>'
CAPITAL = [('자사주 매입 (Q3 FY26)', '$25.1B'),
           ('자사주 매입 (최근 4분기)', '$82.2B'),
           ('배당 (Q3 FY26 · 주당 $0.27)', '', '$4.0B')]
CAPITAL_FOOT = '현금흐름표 지급액 기준 · 출처: <a href="{TENQ}" target="_blank" rel="noopener">Apple Q3 FY26 Form 10-Q (SEC) →</a>'
CHECK_WHEN = '2026년 10월 말 (예상) · Q4 FY2026'
CHECK = ['매출이 가이던스(전년 대비 +9~11%, 환율 역풍 2.5%p 포함)와 매출총이익률 47~48%(관세 환급 효과 약 1%p 포함)를 달성하는지',
         '첨단 공정 칩 공급 제약이 iPhone·Mac·iPad 출하를 얼마나 묶었는지, Q3 iPhone $54.3B(+22%)의 흐름이 이어지는지',
         'Services가 Q3 $30.7B(+12%)의 성장률을 유지하는지',
         '9월 1일 취임한 John Ternus CEO 체제의 첫 실적 발표에서 자본배분 방침이 바뀌는지']
NONOP_WHAT = '지분·장기투자'
PH = ['MSFT', 'GOOGL', 'AMZN', 'NVDA']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}   # 옛 카드의 AMZN PCR 367배(축 밖)는 지금 카드 값 16.8배라 자르지 않는다
CHART_TITLES = {'per': '빅테크 PER 비교', 'pbr': '빅테크 PBR 비교', 'psr': '빅테크 PSR 비교',
                'pcr': '빅테크 PCR(FCF) 비교', 'evebitda': '빅테크 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'GICS Information Technology 23~27종목 대비 배수 순위'
FUND_ASOF_NOTE = 'Q3 FY26 10-Q (2026-07-31 공시)'
PREMISE = '동종업 안에서는 매출·현금흐름 기준 배수가 중간보다 싼 편이지만, <strong>다섯 배수 모두 자기 5년 이력의 비싼 쪽에 있고 현금흐름 내재가치는 현재가에 한참 못 미친다.</strong>'
RISK = ('매출이 지난 5년 속도(연 {pct(HIST[\'growth_5y\'])})로 크다가 식는다면, 현재가가 정당하려면 영업이익률이 <strong data-vs="req">{pct(DCF[\'requiredMargin\'])}</strong>여야 한다(지금 {pct(HIST[\'margin_now\'])}). '
        '성장만으로 맞추려면 연 {pct(DCF[\'requiredGrowth\'])}가 필요한데 최근 3년 실제 성장은 연 {pct(HIST[\'growth_3y\'])}였다.')
FUND_TIP = '이자비용을 따로 공시하지 않아 이자보상배율 칸은 0점이다.'
SELF_TIP = '다섯 배수 모두 5년 분포의 비싼 쪽이다(PER 상위 {100 - SM[\'PER\'][\'percentile\']:.0f}%, PSR·EV/EBITDA 상위 {100 - min(SM[\'PSR\'][\'percentile\'], SM[\'EV/EBITDA\'][\'percentile\']):.0f}%).'
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['지난 5년 성장 속도의 절반에서 출발해 점점 식고, 영업이익률은 지난 5년 중앙값({pct(HIST[\'margin_5y\'])})으로 내려온다. 매출 $1을 늘리는 데 ${INV[\'보수\']:.2f}를 투자한다(최근 1년 수준).',
           '지난 5년의 성장 속도로 출발해 점점 식고, 영업이익률은 최근 2년 중앙값({pct(HIST[\'margin_2y\'])})으로 서서히 내려온다. 매출 $1당 투자는 최근 1년 ${INV[\'recent\']:.2f}에서 5년에 걸쳐 과거 평균 ${INV[\'avg\']:.2f}로 돌아온다.',
           '최근 3년의 성장 속도로 출발해 점점 식고, 지금 영업이익률({pct(HIST[\'margin_now\'])})이 그대로 간다. 매출 $1당 투자는 과거 평균 ${INV[\'avg\']:.2f}다.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 9일 — 신제품 발표', '2026-09-09',
     '첫 폴더블 iPhone Duo($1,999, 10월 23일 출시)와 iPhone 18 Pro·Pro Max 공개 · Ternus CEO 체제 첫 발표', 'duo', 'Apple Newsroom'),
    ('', '2026년 7월 30일 발표 · 7월 31일 반응 — Q3 FY26 실적', '2026-07-31',
     '매출 $109.4B(+16%) · EPS $2.02(+29%, 관세 환급 $0.11 포함) · 다음 분기 가이던스 +9~11%(공급 제약)', 'q3', 'Apple 실적 발표'),
    ('neutral', '2026년 6월 8일 — WWDC26', '2026-06-08',
     'Siri AI와 차세대 Apple Intelligence 공개 · 사용자 베타는 연내, 중국 미제공 · EU는 iOS 초기 미제공', 'wwdc', 'Apple Newsroom'),
    ('', '2026년 4월 30일 발표 · 5월 1일 반응 — Q2 FY26 실적', '2026-05-01',
     '매출 $111.2B(+17%) · iPhone $57.0B 3월 분기 최대 · 배당 4% 인상, 자사주 $100B 추가 승인', 'q2', 'Apple 실적 발표'),
    ('neutral', '2026년 4월 20일 발표 · 4월 21일 반응 — CEO 교체', '2026-04-21',
     'Tim Cook은 이사회 의장, 하드웨어 담당 John Ternus가 9월 1일부터 CEO', 'ceo', 'Apple Newsroom'),
    ('', '2026년 1월 29일 발표 · 1월 30일 반응 — Q1 FY26 실적', '2026-01-30',
     '매출 $143.8B(+16%) 역대 최대 · iPhone $85.3B 역대 최대 · EPS $2.84(+19%)', 'q1', 'Apple 실적 발표'),
    ('', '2025년 10월 30일 발표 · 10월 31일 반응 — Q4 FY25 실적', '2025-10-31',
     '매출 $102.5B(+8%) 9월 분기 최대 · FY25 매출 $416B', 'q4', 'Apple 실적 발표'),
]
SUMMARY = ('네 분기 연속 분기 매출 기록', '우호적·공급 경계',
           ['네 분기 연속 같은 분기 기준 매출 기록을 세웠다. 전년 대비 성장률은 8% → 16% → 17% → 16%로 올라왔다.',
            '다음 분기(Q4 FY26) 가이던스는 +9~11%다. 첨단 공정 칩 공급 제약과 환율 역풍 2.5%p가 들어 있다.',
            '9월 1일 John Ternus가 CEO에 취임했고, 9일 첫 폴더블 iPhone Duo($1,999)를 공개했다.'],
           'Q3 이익에는 관세 환급이 들어 있다(매출총이익률 약 2%p, EPS $0.11). 실적 발표 다음날 주가가 오른 것은 네 번 중 두 번이다.',
           'Q4 FY26 실적(10월 말 예상)에서 +9~11% 가이던스를 넘는지, iPhone Duo 출시(10월 23일) 뒤 공급 제약이 풀리는지.')
BULL = [('수요', '네 분기 연속 같은 분기 기준 매출 기록을 세웠고 Q3 iPhone 매출은 $54.3B(+22%)였다.'),
        ('서비스', 'Services 매출이 Q3 $30.7B(+12%)로 전체의 28%를 차지한다.'),
        ('주주환원', '최근 4분기 자사주 매입이 $82.2B이고 4월에 $100B를 추가 승인했다.')]
BEAR = [('밸류에이션', '현재가가 내재가치 기본 시나리오의 {px / DCF[\'base\']:.1f}배이고 다섯 배수 모두 자기 5년 이력의 비싼 쪽이다.'),
        ('공급 제약', '첨단 공정 칩 공급 제약으로 Q4 가이던스를 Q3 성장률(+16%)보다 낮은 +9~11%로 제시했다.'),
        ('일회성 이익', 'Q3 매출총이익률 50.1%에는 관세 환급 효과 약 2%p가 들어 있다.')]
ANALYST = {'rating': 'Buy', 'n': 44, 'nt': 27, 'mean': 334.73, 'median': 340, 'low': 245, 'high': 400, 'sb': 19, 'b': 6, 'h': 13, 's': 3, 'ss': 3}
ANALYST_ASOF = '2026-10-06'


# 카드 한정 패치 — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
PRE = [r'''
# 안정성 비율(건전성 메모)과 시나리오별 매출 $1당 투자(= 1 ÷ 매출/자본, build_dcf.s2c_path_for) — 이야기 칸 숫자
FR = {r_['metric']: r_['value'] for r_ in FUND['axes']['health']['rows']}
_s2 = {s_: bd.s2c_path_for(b, s_)[0] for s_ in ('보수', '기본', '낙관')}
INV = {'보수': 1 / _s2['보수'][0], 'avg': 1 / _s2['낙관'][0], 'recent': 1 / (b.get('_s2c_marginal') or _s2['낙관'][0])}
''']
POST = [r'''
# 총자산증가율 메모: 옛 카드 표기(회계연도 라벨, 전기, 마감 전까지 동일)
sub(r'(<span class="diag-label">총자산증가율</span><span class="diag-value">)([+-])([\d.]+%</span><span class="diag-note">)FY25 말 (\$[\d.]+B)\(전년 (\$[\d.]+B)\) · 연간 지표(</span>)',
    lambda m_: m_.group(1) + m_.group(2).replace('-', '−') + m_.group(3) + 'FY25 ' + m_.group(4) + '(전기 ' + m_.group(5) + ') · 연간 지표, FY26 마감 전까지 동일' + m_.group(6))
# 이자보상배율 줄 메모(이자비용 미공시)
sub(r'(<div class="diag-row" data-fund-metric="interestCoverage">\n\s*<div class="diag-left"><span class="diag-label">이자보상배율</span><span class="diag-value">[^<]*</span>)(</div>)',
    lambda m_: m_.group(1) + '<span class="diag-note">이자비용을 따로 공시하지 않아 계산할 수 없다 · 점수는 결측 규칙대로 0점</span>' + m_.group(2))
# 자본배분: 배당 칸 꼬리표 없음, 출처 각주
one('            <span class="zone-tag" style="background:rgba(240,192,64,0.18);color:var(--gold);"></span>\n', '')
sub(r'(<div class="card-title">자본배분 · 주주환원 [^<]*</div>\n      <div class="zone-list">.*?\n      </div>\n)', lambda m_: m_.group(1) + '      <div class="yoy-footnote" style="margin-top:14px;">' + F(C.CAPITAL_FOOT) + '</div>\n')
''']


# ── 자동 카드(설계 D, 2026-10-10) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose.py 제안(손 표와 숫자 일치) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"
 ],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {
  "aapl:IPhoneMember": [
   "iPhone",
   "#c4c8ca"
  ],
  "us-gaap:ServiceMember": [
   "Services",
   "#3498db"
  ],
  "aapl:MacMember": [
   "Mac",
   "#a6acaf"
  ],
  "aapl:WearablesHomeandAccessoriesMember": [
   "Wearables·Home·Acc.",
   "#767f83"
  ],
  "aapl:IPadMember": [
   "iPad",
   "#5c6282"
  ]
 },
 "ignore": [
  "us-gaap:ProductMember"
 ]
}
POST = [r'''
# 이자보상배율 줄 메모(이자비용 미공시 — 회사 사정, 분기와 무관)
sub(r'(<div class="diag-row" data-fund-metric="interestCoverage">\n\s*<div class="diag-left"><span class="diag-label">이자보상배율</span><span class="diag-value">[^<]*</span>)(</div>)',
    lambda m_: m_.group(1) + '<span class="diag-note">이자비용을 따로 공시하지 않아 계산할 수 없다 · 점수는 결측 규칙대로 0점</span>' + m_.group(2))
''']   # 손 문구 블록 정리: 구조 표시만 남기고 분기 문장·날짜 박힌 치환은 뺐다
