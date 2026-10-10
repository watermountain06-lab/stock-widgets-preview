# CRWD(크라우드스트라이크) v2 카드 설정 — fill.py CRWD. 회계연도 1월 31일(Q2 FY27 = 2026-05~07). 시총 루트 카드 있음. 2026-07 4:1 분할.
# 틀 시절 카드(루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G4).
# 출처: SEC XBRL, Q2 FY27 10-Q(2026-08-27), 실적 보도자료(Q3 FY26~Q2 FY27), 8-K(CEO 보상 12/29, 자사주 4/6), StockAnalysis(2026-10-01).
# 재고가 없는 회사(활동성 재고 0일), 감가상각 분기 태그가 회사 고유라 EV/EBITDA 없음, PER 해당 없음(순이익률 2% 미만, A3).
# 분기 차트: FY26 4분기에 주식보상비용 인식 시점 오류를 고쳐 회사가 수정값을 낸 분기는 수정값(OVERRIDE_OP_NI — Q4 FY26 보도자료 비교 열,
#   Q1·Q2 FY27 10-Q 비교 열). Q3 FY25·Q3 FY26은 원공시.
# 재현 모드: python3 v2/newcards/build.py CRWD --from-card (일봉·이동평균·백테스트는 지금 카드에서).
BUILD = {}
CIK = '0001535527'
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q2 FY27', 'Q2 FY26', 'Q1 FY27'
L8 = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27', 'Q2 FY27']
RELEASE = {'rev': 1471, 'op': -33, 'ni': 5}   # Q2 FY27 보도자료(백만 달러) — 매출 $1.47B, GAAP 영업손실 $33M, 순이익 $5M
OVERRIDE_OP_NI = [('2025-01-31', -79.305, -86.286),    # Q4 FY25 — Q4 FY26 보도자료 비교 열(수정)
                  ('2025-04-30', -118.713, -104.264),  # Q1 FY26 — Q1 FY27 10-Q 비교 열(수정)
                  ('2025-07-31', -105.457, -70.153),   # Q2 FY26 — Q2 FY27 10-Q 비교 열(수정)
                  ('2026-01-31', -6.900, 38.691)]      # Q4 FY26 — Q4 FY26 보도자료(연간 10-K − 원공시 9개월 파생값 대신)
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'CrowdStrike'
S_ = 'https://www.sec.gov/Archives/edgar/data/1535527/'
SEC = S_
PR = {'q2': S_ + '000153552726000029/crwd-20260826xex991.htm', 'q1': S_ + '000153552726000022/crwd-20260603xex991.htm',
      'q4': S_ + '000153552726000007/crwd-20260303xex991.htm', 'q3': S_ + '000153552725000030/crwd-20251202xex991.htm'}
PR_CUR = 'q2'
TENQ = S_ + '000153552726000031/crwd-20260731.htm'; TENQ_NAME = 'Q2 FY27 10-Q'
LINKS = {'buyback': S_ + '000153552726000013/sharerepurchaseincreasepre.htm', 'tenq': TENQ,
         'ceo': S_ + '000110465925124912/tm2534248d1_8k.htm'}
# PER 해당 없음이라 엔진이 밴드를 내지 않는다(fairBand None) — 옛 카드 설명(9월 말 계산값)을 그대로 둔다.
FAIRBAND_TITLE = ('id="crwdFairBand" title="최근 1년 PER 25~75% 구간(5,363~6,264배) × 최근 4분기 희석 EPS ${eps_ttm}로 내면 $210~$250이지만, '
                  '최근 4분기 GAAP 순이익이 거의 0이고 흑자 PER이 1년 중 약 한 달뿐이라 범위로 쓰지 않는다."')
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률</span>'
OPM_RANGE, Y2 = (-15, 5), (-15, 5)
FCF_SUB = '영업현금흐름 − 유형자산 취득 · 회사 FCF $0.38B(내부 사용 소프트웨어 자본화도 뺀 정의)'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('R&amp;D (Q2 FY27)', '$0.44B', '연구개발(GAAP) · 매출의 30.2%')
NEXT = ('12월 초 예상', '일정 · Q3 FY27 (회사 미확정)'); NEXT_OP = ('12월 초', 'Q3 FY27 예상')
FY_ENDS, FY_LABEL = ('2026-01-31', '2025-01-31'), 'FY2026'
HEALTH_NOTE = ('현금 $5.0B에 차입금은 회사채 $0.75B뿐이라 순현금이다. 현금은 2월 인수(Seraphic·SGNL, $0.88B)로 연초 $5.23B에서 줄었다. '
               '유동부채에 이연수익 $3.5B(구독 선수금)가 있어 유동비율이 그만큼 낮게 나온다. 이자보상배율 1점은 GAAP 영업손실 때문이다.')
ACT_REASON = ''
YOY_EXTRA = '영업이익·순이익은 1년 전 적자에서 줄거나 흑자로 바뀌었다 · '
SEG = [('미국', 954.464, '#e01f3d'), ('유럽·중동·아프리카', 263.698, '#5aa9e6'), ('아시아·태평양', 157.893, '#94a3b8'), ('기타', 94.842, '#f0c040')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 지역별 매출'
SEG_NOTE = ('고객 주소 기준 · 1년 전보다 미국 +22%, 유럽·중동·아프리카 +40%, 아시아·태평양 +34%, 기타 +21% · 매출의 95%가 구독(구독 $1.40B, 전문 서비스 $0.07B) · '
            '출처: <a href="{TENQ}" target="_blank" rel="noopener">Q2 FY27 10-Q 지역 표 (SEC) →</a>')
CAPITAL = [('자사주 매입 (Q1 FY27 $176M, Q2 FY27 없음)', '상반기 $0.18B'),
           ('자사주 매입 승인 한도 (4월 $0.5B 증액 뒤 총액)', '$1.5B'),
           ('배당', '지급하지 않음', '$0')]
CHECK_WHEN = '2026년 12월 초 (예상) · Q3 FY27'
CHECK = ['3분기 가이던스 매출 $1.523~1.529B, 비GAAP EPS $0.31을 넘는지',
         '순신규 ARR(2분기 $333M, +51%)과 올려 잡은 연간 순신규 ARR 성장 34%',
         'GAAP 영업손익(2분기 −$33M)이 흑자로 돌아서는지와 주식보상비용(2분기 $377M)',
         'Falcon Flex 고객의 기말 ARR(2분기 $2.29B, +101%)']
NONOP_WHAT = '지분·장기투자'
PH = ['PANW', 'PLTR', 'MSFT', 'ORCL', 'CRM', 'IBM']
PEER_FILE = None
CHART_CAP, SELF_CAP = {}, {'per': 170}   # PER 6,619배(해당 없음)가 축을 늘리지 않게 — 옛 카드 축 200
CHART_NOTE = {'evebitda': ' (CRWD 값 없음)'}
CHART_TITLES = {'per': '보안·소프트웨어 6곳 PER 비교 (점수는 IT 카드 유니버스 기준)', 'pbr': '보안·소프트웨어 PBR 비교', 'psr': '보안·소프트웨어 PSR 비교',
                'pcr': '보안·소프트웨어 PCR(FCF) 비교', 'evebitda': '보안·소프트웨어 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위(EV/EBITDA 없음)'
FUND_ASOF_NOTE = 'Q2 FY27 10-Q (2026-08-27 공시)'
PREMISE = ('PSR {SM[\'PSR\'][\'current\']:.1f}배·PBR {SM[\'PBR\'][\'current\']:.1f}배·PCR {SM[\'PCR\'][\'current\']:.0f}배가 5년 중 가장 비싼 쪽(상위 {math.ceil(max(100 - SM[k][\'percentile\'] for k in (\'PSR\', \'PBR\', \'PCR\')))}% 안)이고, '
           'PER {SM[\'PER\'][\'current\']:,.0f}배는 최근 4분기 GAAP 순이익이 거의 0이라(순이익률 1.1%) 점수에서 뺀다(PER 해당 없음, 순이익률 2% 미만 규칙). '
           '자기 이력 {selfsc:.1f}점, 카드 유니버스 IT 안에서도 나머지 세 배수가 모두 가장 비싼 쪽이라 {peersc:.1f}점이다(EV/EBITDA는 감가상각 태그가 회사 고유라 계산하지 않는다). '
           '<strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.2f})는 현재가의 {DCF[\'base\'] / px * 100:.1f}%</strong>다.')
RISK = ('세 칸이 {sgn(VOTES[0])}·{sgn(VOTES[1])}·{sgn(VOTES[2])}{jo_ro(VOTES[2])} 합계 {TOTAL_TXT} “{VERDICT}”다. GAAP 영업이익률이 최근 4분기 {pct(HIST[\'margin_now\'])}(주식보상비용 포함, 회사 비GAAP 2분기 25%)라 '
        '영업이익률을 100%로 올려도 현재가에 닿지 않는다(해 없음). 성장률은 5년 연 {pct(HIST[\'growth_5y\'])}·3년 연 {pct(HIST[\'growth_3y\'])}로 높지만 모델은 GAAP 이익률에서 출발한다.')
FUND_TIP = '매출 CAGR 29.0%는 5점이지만, GAAP 영업손실(주식보상비용 포함)로 영업이익 CAGR·영업이익률·이자보상배율이 1점이다.'
SELF_TIP = ('PSR {SM[\'PSR\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PSR\'][\'median\']:.1f}배)·PBR·PCR이 5년 중 가장 비싼 쪽이다. '
            'PER은 GAAP 순이익이 흑자였던 {SM[\'PER\'][\'days\']}일만 이력이 있다. 7월 4:1 분할 전 주가·주식 수는 분할 기준으로 맞췄다.')
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['5년 성장률(분기 누적 기준)의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(분기 누적 기준, 연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(분기 누적 기준, 연 {pct(HIST[\'growth_3y\'])})에서 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('세 시나리오 모두 GAAP 영업이익률이 음수(주식보상비용 포함)라 사업 가치가 0 이하이고, 기본 ${DCF[\'base\']:.2f}는 순현금(주당 $4.10)보다 작다. '
            '영업이익률이 음수라 매출이 빨리 클수록 손실이 커져 성장 가정이 가장 높은 기본이 가장 낮다. 회사 비GAAP 영업이익률(2분기 25%)이나 잉여현금흐름으로 보면 전혀 다른 숫자가 나온다.')
NEWS_RANGE = '2025.12 ~ 2026.08'
NEWS = [
    ('', '2026년 8월 26일 장 마감 후 — Q2 FY27 실적', '2026-08-27',
     '매출 $1.47B(+26%) · 순신규 ARR $333M(+51%, 최대) · GAAP 순이익 $5M·영업손실 $33M · 연간 순신규 ARR 성장 가이던스 34%로 상향', 'q2', 'CrowdStrike 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 2일 — 4:1 주식 분할 시행', None,
     '6월 25일 기준 주주에게 1주당 3주를 더 주는 주식 배당 방식, 7월 2일부터 분할 기준 거래', 'q1', 'CrowdStrike 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 6월 3일 장 마감 후 — Q1 FY27 실적·주식 분할 발표', '2026-06-04',
     '매출 $1.39B(+26%) · 순신규 ARR $256M(+32%) · GAAP 순이익 $28M · 4:1 분할 발표', 'q1', 'CrowdStrike 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 6일 개장 전 — 자사주 매입 한도 증액', '2026-04-06',
     '자사주 매입 한도를 $0.5B 늘려 총 $1.5B로', 'buyback', 'CrowdStrike 공시 (SEC 8-K)'),
    ('', '2026년 3월 3일 장 마감 후 — Q4 FY26 실적', '2026-03-04',
     '매출 $1.31B(+23%) · 기말 ARR $5.25B(+24%) · GAAP 순이익 $39M으로 흑자', 'q4', 'CrowdStrike 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 3일·20일 — Seraphic·SGNL 인수 종결', None,
     '브라우저 보안 Seraphic($327.5M 현금)과 신원 보안 SGNL($627.9M 현금) 인수 종결 · 상반기 인수 현금 $0.88B', 'tenq', 'CrowdStrike Q2 FY27 10-Q 주석 12 (SEC)'),
    ('neutral', '2025년 12월 29일 장 마감 후 — CEO 성과 주식 보상', '2025-12-30',
     '이사회가 12월 22일 조지 커츠 CEO에게 성과 조건부 주식 보상을 승인', 'ceo', 'CrowdStrike 공시 (SEC 8-K)'),
    ('', '2025년 12월 2일 장 마감 후 — Q3 FY26 실적', '2025-12-03',
     '매출 $1.23B(+22%) · 순신규 ARR $265M(+73%) · GAAP 순손실 $34M', 'q3', 'CrowdStrike 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('순신규 ARR이 빨라지고 Falcon Flex가 퍼지며 주가는 1년 새 {CH_TXT}', '고성장·초고배수',
           ['2분기 매출 $1.47B(+26%), 순신규 ARR $333M(+51%)으로 분기 최대였다.',
            '연간 순신규 ARR 성장 가이던스를 34%로 올렸고, Falcon Flex 고객 ARR이 $2.29B(+101%)다.',
            'GAAP 영업손실은 $33M으로 줄었지만 주식보상비용이 $377M이다. 비GAAP 영업이익은 $372M이다.'],
           '배수가 5년 이력과 IT 카드 유니버스 모두에서 가장 비싼 쪽이고, GAAP 영업이익률이 음수라 현금흐름 모델은 주당 ${DCF[\'base\']:.2f}이다.',
           'Q3 FY27 실적(12월 초 예상)의 순신규 ARR과 GAAP 영업이익 흑자 전환.')
BULL = [('성장', '매출 +26%, 순신규 ARR $333M(+51%), 기말 ARR $5.84B(+25%).'),
        ('현금', '2분기 영업현금 $530M, 회사 FCF $377M, 현금 $5.0B.'),
        ('플랫폼', 'Falcon Flex 고객 ARR $2.29B(+101%), 6개 이상 모듈 고객 51%.')]
BEAR = [('밸류', 'PSR {SM[\'PSR\'][\'current\']:.0f}배. 5년 이력과 IT 카드 유니버스 모두에서 가장 비싼 쪽이다.'),
        ('이익', 'GAAP 영업손실이 이어지고(2분기 −$33M) 주식보상비용이 2분기 $377M이다.'),
        ('희석', '기본 가중평균 주식 수가 1년 새 9.996억 주에서 10.194억 주로 2.0% 늘었다(주식보상).')]
ANALYST = {'rating': 'Buy', 'n': 53, 'nt': 38, 'mean': 241.54, 'median': 250, 'low': 125, 'high': 425, 'sb': 30, 'b': 10, 'h': 12, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-10-06'
MISSING_NOTE = '감가상각 태그가 회사 고유'   # 없는 배수(EV/EBITDA) 칸 메모(옛 카드)
REV_FOOTNOTE = ('GAAP 기준이다. 영업이익에는 주식보상비용(2분기 $0.38B)이 들어 있어 회사가 내는 비GAAP 영업이익(2분기 $0.37B)과 크게 다르다. '
                'FY26 4분기에 주식보상비용 인식 시점 오류(경미)를 고쳐 과거 분기를 수정했다. 회사가 수정값을 낸 분기(Q4 FY25·Q1·Q2·Q4 FY26)는 수정값, Q3 FY25·Q3 FY26은 원공시다.')

# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
POST = [r'''
# 분기 차트 아래 설명(주식보상·수정 분기)
one(f'<canvas id="{t}RevChart"></canvas>\n    </div>\n', f'<canvas id="{t}RevChart"></canvas>\n    </div>\n'
    f'    <div class="yoy-footnote" style="margin-top:8px;">{C.REV_FOOTNOTE}</div>\n')
# YoY·QoQ 각주의 FCF 정의: 옛 카드는 "유형자산 취득"
assert h.count(" · FCF는 영업현금흐름 − 설비투자 · ") == 2
h = h.replace(" · FCF는 영업현금흐름 − 설비투자 · ", " · FCF는 영업현금흐름 − 유형자산 취득 · ")
# 총자산증가율 메모: 회계연도 끝 달(옛 카드)
one("FY2026 말 $", "FY2026 말(2026-01) $")
# 동종업 팁: 뺀 배수 설명(옛 카드 문장)
one("뒤집어 점수로 썼고 PER·EV/EBITDA를 뺀 3개를 평균했다.", "뒤집어 점수로 썼고 EV/EBITDA와 PER(해당 없음 — 순이익률 2% 미만)을 뺀 세 개를 평균했다.")
# PER 이력 메모: 흑자였던 날 수(카드 한정, Fable — 옛 카드)
one("const nt = f('note'); if (nt) nt.textContent = m.days < 1200 ?", "const nt = f('note'); if (nt) nt.textContent = m.metric === 'per' && m.days < 1200 ? `흑자였던 ${m.days}일 이력` : m.days < 1200 ?")
# 시나리오 범위 툴팁: 기본이 가장 낮다(옛 카드)
one("(세 시나리오 최대·최소 기준)` : '';", "(세 시나리오 최대·최소 기준, 기본이 가장 낮다)` : '';")
''']


# ── 자동 카드(설계 D, 2026-10-10) — 분기마다 고치던 칸을 auto_card.py가 채운다. 부문 지도는 seg_map_propose.py 제안(손 표와 숫자 일치) ──
AUTO = True
SEG_MAP = {
 "concepts": [
  "us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"
 ],
 "axis": "srt:StatementGeographicalAxis",
 "extra": {},
 "members": {
  "country:US": [
   "미국",
   "#e01f3d"
  ],
  "us-gaap:EMEAMember": [
   "유럽·중동·아프리카",
   "#5aa9e6"
  ],
  "srt:AsiaPacificMember": [
   "아시아·태평양",
   "#94a3b8"
  ],
  "crwd:OtherCountriesMember": [
   "기타",
   "#f0c040"
  ]
 },
 "ignore": []
}
# 손 문구 블록 정리: 화면 구조 고침만 남기고 분기 문장·날짜 박힌 치환·시간이 지나면 틀려지는 문장은 뺐다. 덩어리마다 따로 실행(자동 카드는 못 찾으면 건너뜀)
POST = ['# YoY·QoQ 각주의 FCF 정의: 옛 카드는 "유형자산 취득"\nassert h.count(" · FCF는 영업현금흐름 − 설비투자 · ") == 2\nh = h.replace(" · FCF는 영업현금흐름 − 설비투자 · ", " · FCF는 영업현금흐름 − 유형자산 취득 · ")', '# 동종업 팁: 뺀 배수 설명(옛 카드 문장)\none("뒤집어 점수로 썼고 PER·EV/EBITDA를 뺀 3개를 평균했다.", "뒤집어 점수로 썼고 EV/EBITDA와 PER(해당 없음 — 순이익률 2% 미만)을 뺀 세 개를 평균했다.")', '# PER 이력 메모: 흑자였던 날 수(카드 한정, Fable — 옛 카드)\none("const nt = f(\'note\'); if (nt) nt.textContent = m.days < 1200 ?", "const nt = f(\'note\'); if (nt) nt.textContent = m.metric === \'per\' && m.days < 1200 ? `흑자였던 ${m.days}일 이력` : m.days < 1200 ?")']
