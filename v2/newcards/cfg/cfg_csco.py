# CSCO(시스코) v2 카드 설정 — fill.py CSCO. 회계연도 7월 마지막 토요일(Q4 FY26 = 2026-04-26~07-25). 시총 루트 카드 있음.
# 틀 시절 카드(루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G4).
# 출처: SEC XBRL, FY2026 10-K(2026-09-02), 실적 보도자료(Q1~Q4 FY2026), 8-K(이사 사임 3/31), StockAnalysis(2026-10-01).
# 감가상각 분기 표준 태그가 없어 EV/EBITDA 자기 이력이 없다(엔진 그대로 — 판정 칸은 네 배수).
# 재현 모드: python3 v2/newcards/build.py CSCO --from-card (일봉·이동평균·백테스트는 지금 카드에서).
BUILD = {}
CIK = '0000858877'
CUR, YO, QO = '2026-07-25', '2025-07-26', '2026-04-25'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
RELEASE = {'rev': 17252, 'op': 4264, 'ni': 3859}   # Q4 FY26 손익(백만 달러) — 옛 카드 YoY 막대 $17.25B·$4.26B·$3.86B와 같다
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Cisco'
S_ = 'https://www.sec.gov/Archives/edgar/data/858877/'
SEC = S_
PR = {'q4': S_ + '000085887726000106/exhibit991pressrelease-q4f.htm', 'q3': S_ + '000085887726000075/exhibit991pressrelease-q3f.htm',
      'q2': S_ + '000085887726000006/exhibit991pressrelease-q2f.htm', 'q1': S_ + '000119312525277624/d484663dex991.htm'}
PR_CUR = 'q4'
TENQ = S_ + '000085887726000132/csco-20260725.htm'; TENQ_NAME = 'FY2026 10-K'
LINKS = {'director': S_ + '000085887726000048/csco-20260331.htm'}
FAIRBAND_TITLE = 'id="cscoFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
OPM_RANGE, Y2 = (15, 30), (15, 30)
FCF_SUB = '영업현금흐름 − 설비투자'
CAPEX_SUB = '유형자산 취득(현금흐름표)'
STAT3 = ('R&amp;D (Q4 FY26)', '$2.43B', '매출의 14%')
NEXT = ('11월 중순 예상', '일정 · Q1 FY27 (회사 미확정)'); NEXT_OP = ('11월 중순', 'Q1 FY27 예상')
FY_ENDS, FY_LABEL = ('2026-07-25', '2025-07-26'), 'FY2026'
HEALTH_NOTE = ('차입금은 $29.5B(단기 $10.2B — 기업어음 $6.7B와 1년 안 만기 $3.5B — + 장기 $19.4B)이고 현금·단기투자는 $15.9B다. '
               '유동비율 93.1%는 유동부채에 기업어음과 이연매출(선수 구독·서비스료)이 커서다.')
ACT_REASON = ''
YOY_EXTRA = ''
SEG = [('네트워킹', 9791, '#049fd9'), ('서비스', 3793, '#94a3b8'), ('보안', 2226, '#f0c040'), ('협업', 1167, '#5aa9e6'), ('관측성', 275, '#64748b')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품군·서비스'
SEG_NOTE = ('1년 전보다 네트워킹 +28%, 보안 +14%, 협업 +12%, 관측성 +6%, 서비스 제자리 · 하이퍼스케일러 AI 인프라 주문 FY2026 $9.3B(4분기 $4B), FY2027 매출 약 $7.5B 예상 · '
            '출처: <a href="{PR[\'q4\']}" target="_blank" rel="noopener">Q4 FY2026 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (Q4 FY26, 약 1,300만 주 · 평균 $111.53)', '$1.5B'),
           ('잔여 바이백 승인 한도 (2026.07.25 기준, 기한 없음)', '$8.1B'),
           ('배당 (Q4 FY26 지급, 분기 $0.42)', 'FY2026 합계 $6.6B', '$1.7B')]
CHECK_WHEN = '2026년 11월 중순 (예상) · Q1 FY27'
CHECK = ['회사 전망 — Q1 FY27 매출 $18.0~18.2B, GAAP EPS $1.08~1.10(비GAAP $1.32~1.34)',
         'FY2027 전망(매출 $72.2~73.4B, GAAP EPS $4.00~4.06) 유지',
         '하이퍼스케일러 AI 인프라 매출(FY2027 약 $7.5B 예상)과 네트워킹 성장(4분기 +28%)',
         '5월 발표한 구조조정(최대 $1B, 세전) 남은 비용과 자사주 매입($8.1B 한도)']
NONOP_WHAT = '장기투자'
PH = ['ANET', 'IBM', 'DELL', 'APH', 'QCOM', 'MSFT']
PEER_FILE = None
CHART_CAP, SELF_CAP = {}, {}
CHART_NOTE = {'evebitda': ' (CSCO 본인 이력은 감가상각 분기 태그가 없어 계산 불가)'}
CHART_TITLES = {'per': '네트워크·하드웨어·소프트웨어 6곳 PER 비교 (점수는 IT 카드 유니버스 24~27곳 기준)', 'pbr': '네트워크·IT 하드웨어 PBR 비교',
                'psr': '네트워크·IT 하드웨어 PSR 비교', 'pcr': '네트워크·IT 하드웨어 PCR(FCF) 비교', 'evebitda': '네트워크·IT 하드웨어 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
FUND_ASOF_NOTE = 'FY2026 10-K (2026-09-02 공시)'
PREMISE = ('주가가 1년 새 {ch:.0f}% 올라 PER {SM[\'PER\'][\'current\']:.1f}배·PSR {SM[\'PSR\'][\'current\']:.1f}배·PBR·PCR이 모두 5년 중 상위 10% 안이라 자기 이력 {selfsc:.1f}점이다. '
           '카드 유니버스 IT 안에서는 반도체·AI 종목보다 싸 {peersc:.1f}점이다. <strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>다.')
RISK = ('세 칸이 {sgn(VOTES[0])}·{sgn(VOTES[1])}·{sgn(VOTES[2])}{jo_ro(VOTES[2])} 합계 {TOTAL_TXT} “{VERDICT}”다. 현재가가 정당하려면 영업이익률이 {pct(DCF[\'requiredMargin\'])}여야 한다(최근 4분기 {pct(HIST[\'margin_now\'])}). '
        'SEC 데이터의 감가상각 태그가 유형자산 몫 연 $0.7B뿐이라(현금흐름표의 감가상각·상각 등 전체는 $2.5B) EV/EBITDA 자기 이력을 만들 수 없고 내재가치의 재투자도 크게 잡혔다 — '
        '그래도 현재가는 기본 가치의 약 {px / DCF[\'base\']:.0f}배라 판정은 같다.')
FUND_TIP = '유동비율 1점은 기업어음과 이연매출이 커서이고, 매출·영업이익 3년 성장률이 낮아(연 3.6%·0.7%) 성장 점수가 2점씩이다.'
SELF_TIP = ('PER {SM[\'PER\'][\'current\']:.1f}배(5년 중앙값 {SM[\'PER\'][\'median\']:.1f}배)·PSR·PBR·PCR 모두 5년 상위 10% 안이다. '
            'EV/EBITDA는 감가상각을 분기로 공시한 표준 태그가 없어 자기 이력이 없다(규칙대로 두고 명시, 2026-10-01).')
PEER_TIP = ('같은 GICS 섹터(Information Technology) 카드 유니버스 안에서 배수 순위를 매긴 값이다.',
            '반도체·AI 종목이 많아 CSCO의 배수는 그 안에서 싼 쪽이다(PSR 27곳 중 6번째로 쌈).')
STORIES = ['5년 성장률의 절반(연 {pct(HIST[\'growth_5y\'] / 2)})에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 간다.',
           '5년 성장률(연 {pct(HIST[\'growth_5y\'])})에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 간다.',
           '3년 성장률(연 {pct(HIST[\'growth_3y\'])})에서 식고, 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다.']
DCF_NOTE = ('보수 가치가 가장 높은 것은 보수 시나리오가 쓰는 5년 중앙 영업이익률({pct(HIST[\'margin_5y\'])})이 기본의 2년 중앙값({pct(HIST[\'margin_2y\'])})보다 '
            '높아서다(이름과 순서가 뒤집힘).')
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('', '2026년 8월 12일 장 마감 후 — Q4 FY2026 실적', '2026-08-13',
     '매출 $17.3B(+18%, 사상 최대)·EPS $0.97(비GAAP $1.22) · 네트워킹 +28% · AI 인프라 주문 FY26 $9.3B · FY27 매출 $72.2~73.4B 전망', 'q4', 'Cisco 실적 보도자료 (SEC 8-K)'),
    ('', '2026년 5월 13일 장 마감 후 — Q3 FY2026 실적·구조조정', '2026-05-14',
     '매출 $15.8B(사상 최대)·EPS $0.85(비GAAP $1.06) · 실리콘·광학·보안·AI에 투자하려 최대 $1B(세전) 구조조정 발표', 'q3', 'Cisco 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 31일 — 이사 사임', None,
     '대니얼 슐먼 이사가 버라이즌 CEO 취임으로 5월 21일 사임', 'director', 'Cisco 공시 (SEC 8-K)'),
    ('', '2026년 2월 11일 장 마감 후 — Q2 FY2026 실적', '2026-02-12',
     '매출 $15.3B·EPS $0.80(비GAAP $1.04)', 'q2', 'Cisco 실적 보도자료 (SEC 8-K)'),
    ('', '2025년 11월 12일 장 마감 후 — Q1 FY2026 실적', '2025-11-13',
     '매출 $14.9B·EPS $0.72(비GAAP $1.00)', 'q1', 'Cisco 실적 보도자료 (SEC 8-K)'),
]
SUMMARY = ('AI 데이터센터 네트워킹 수요로 Q4 매출이 18%(FY2026 +12%) 늘고 주가는 1년 새 {ch:.0f}% 올라 5년 중 가장 비싼 쪽', 'AI 네트워킹·고평가 쪽',
           ['Q4 FY26 매출 $17.3B(+18%)로 사상 최대, 제품 매출 +24%·네트워킹 +28%였다.',
            '하이퍼스케일러 AI 인프라 주문이 FY2026 $9.3B였고, 회사는 FY2027에 이 매출 약 $7.5B를 예상한다.',
            '5월에 최대 $1B 구조조정을 발표했고, 4분기에 자사주 $1.5B·배당 $1.7B를 돌려줬다.'],
           '자기 이력 배수가 모두 5년 상위 10% 안이고, 현금흐름 모델로는 현재가의 {DCF[\'base\'] / px * 100:.0f}%만 설명된다.',
           'Q1 FY27 실적(11월 중순 예상)의 매출 $18.0~18.2B 전망 달성과 AI 인프라 주문.')
BULL = [('성장', 'Q4 FY26 매출 +18%, 네트워킹 +28%, AI 인프라 주문 FY26 $9.3B.'),
        ('전망', 'FY2027 매출 $72.2~73.4B(+14~16%), GAAP EPS $4.00~4.06.'),
        ('환원', '4분기 자사주 $1.5B·배당 $1.7B, 남은 매입 한도 $8.1B.')]
BEAR = [('밸류', 'PER {SM[\'PER\'][\'current\']:.1f}배 등 네 배수가 5년 상위 10% 안, 현금흐름 내재가치 ${DCF[\'base\']:.0f}.'),
        ('서비스', '서비스 매출은 1년 전과 같아 성장이 제품에 기댄다.'),
        ('비용', '최대 $1B 구조조정 — FY2027에 남은 비용이 반영된다.')]
ANALYST = {'rating': 'Buy', 'n': 29, 'nt': 16, 'mean': 138.44, 'median': 139, 'low': 110, 'high': 165, 'sb': 14, 'b': 5, 'h': 10, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-10'

REV_FOOTNOTE = ('회계연도는 7월 마지막 토요일 무렵에 끝난다(Q4 FY26 = 2026년 4월 말~7월). '
                'Q4 FY26 영업이익에는 5월 발표한 구조조정 등 비용 $511M(세전, FY2026 합계 $693M)이 들어 있다.')
MISSING_NOTE = ''   # 없는 배수(EV/EBITDA) 칸 — 옛 카드는 배지에 사유를 적고 메모는 비웠다
MISSING_CUR, MISSING_BADGE = '계산 불가', '감가상각 분기 태그 없음 · 평균 제외'

# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
POST = [r'''
# 보도자료 링크 글자: 옛 카드는 회계연도 네 자리(Q4 FY2026)
h = h.replace(f"{C.CO} {QL} 실적 보도자료 (SEC 8-K) →", f"{C.CO} Q4 FY2026 실적 보도자료 (SEC 8-K) →")
# 분기 차트 아래 설명(회계연도·구조조정 비용)
one(f'<canvas id="{t}RevChart"></canvas>\n    </div>\n', f'<canvas id="{t}RevChart"></canvas>\n    </div>\n'
    f'    <div class="yoy-footnote" style="margin-top:8px;">{C.REV_FOOTNOTE}</div>\n')
# 없는 배수 칸: 현재값·배지 글자(옛 카드 그대로)
_i = h.index('const haveM = new Set'); _j = h.index("['peer', 'self'].forEach(k => {", _i)
_seg = h[_i:_j]
_seg2 = _seg.replace("f('cur').textContent = '—';", f"f('cur').textContent = {json.dumps(C.MISSING_CUR, ensure_ascii=False)};", 1).replace(
    "f('badge').textContent = '계산 불가';", f"f('badge').textContent = {json.dumps(C.MISSING_BADGE, ensure_ascii=False)};", 1)
assert _seg2 != _seg; h = h[:_i] + _seg2 + h[_j:]
''']
