# NVDA v2 카드 설정 — fill.py NVDA. 회계연도 1월 말(52·53주). 자동 카드(2026-10-11) — 분기마다 고치던 칸은 auto_card가 채운다.
# 틀 시절 카드(2026-09 루트 카드에서 손으로 옮긴 것)를 생성기로 다시 만들기 위해 지금 카드의 내용을 옮겼다(2026-10-05, 틀 통일 G2).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05), 실적 보도자료(Q3 2025~Q2 2026), 8-K(OpenAI 10/6, ZT 매각 10/27, Meta 2/24, 회사채 8/17), StockAnalysis(2026-09-27).
# 재현 모드: python3 v2/newcards/build.py AMD --from-card (일봉·이동평균·백테스트는 지금 카드에서, 마지막 종가 2026-09-25).
CIK = '0001045810'
CUR, YO, QO = '2026-07-26', '2025-07-27', '2026-04-26'
QLABEL, YL, QQL = 'Q2 FY27', 'Q2 FY26', 'Q1 FY27'
L8 = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27', 'Q2 FY27']
RELEASE = {}
VOTES, VERDICT = (1, 0, 1), '적정~저평가'
CO = 'NVIDIA'
S_ = 'https://www.sec.gov/Archives/edgar/data/1045810/'
SEC = S_
PR = {}
PR_CUR = None
TENQ = S_; TENQ_NAME = 'Q2 FY27 10-Q'   # auto_card가 채운다
LINKS = {}
FAIRBAND_TITLE = 'id="nvdaFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 3년 +{pct(HIST[\'growth_3y\'])})</span>'
OPM_RANGE, Y2 = (-10, 30), (-5, 20)
FCF_SUB = '현금창출력'
CAPEX_SUB = '미래 재투자'
STAT3 = ('R&amp;D (Q2 2026)', '$2.5B', '기술 경쟁력 투자')
NEXT = ('11월 초 예상', '일정 · Q3 2026'); NEXT_OP = ('11월 초', 'Q3 2026 예상')
FY_ENDS, FY_LABEL = ('2026-01-25', '2025-01-26'), 'FY2026'
HEALTH_NOTE = ''
ACT_REASON = ''
YOY_EXTRA = ''   # 옛 카드는 설명을 "GAAP 기준" 바로 뒤에 두었다 — POST에서 같은 자리에
FOOT_EXTRA = ''
SEG = [('하이퍼스케일', 48710, '#7c6ad6'), ('AI 클라우드·산업·기업', 40313, '#4d7a00'), ('엣지 컴퓨팅', 7198, '#3b82f6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 시장 플랫폼별'
SEG_NOTE = ('전년 대비 데이터센터 +107%, 클라이언트 +23%, 게이밍 −31%(세미커스텀 감소), 임베디드 +19% · 출처: '
            '<a href="{PR[\'q2\']}" target="_blank" rel="noopener">AMD Q2 2026 실적 보도자료 (SEC 8-K) →</a>')
CAPITAL = [('자사주 매입 (상반기, 110만 주 · 2분기엔 없음)', '$0.22B'),
           ('잔여 바이백 승인 한도 (총 $14B 중, 6월 말)', '$9.2B'),
           ('배당', '배당 없음', '해당 없음')]
CAPITAL_PERIOD = '2026년 상반기'
CHECK_WHEN = '2026년 11월 초 (예상) · Q3 2026'
CHECK = ['3분기 매출 가이던스 약 $13.0B(±$0.3B, +41%)와 비GAAP 매출총이익률 약 56% 달성',
         '회사가 말한 하반기 데이터센터 가속 — MI450·Helios 랙 출하가 매출로 확인되는지',
         'OpenAI·Meta 워런트의 첫 트랜치(각 1GW 인도)가 베스팅되는지 — 최대 3.2억 주 희석의 시작',
         'GAAP 영업이익률(2분기 17%)이 인수 무형자산 상각(분기 약 $0.55B)을 넘어 얼마나 오르는지']
NONOP_WHAT = '지분·장기투자'
PH = ['AMD', 'AVGO', 'TSM', 'MU', 'QCOM', 'INTC']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '반도체 대형주 PER 비교', 'pbr': '반도체 대형주 PBR 비교', 'psr': '반도체 대형주 PSR 비교',
                'pcr': '반도체 대형주 PCR(FCF) 비교', 'evebitda': '반도체 대형주 EV/EBITDA 비교'}
PEER_NAME_TITLE = '같은 IT 섹터 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'GICS Information Technology 대비 배수 순위'
FUND_ASOF_NOTE = 'Q2 2026 10-Q (2026-08-05 공시)'
PREMISE = ('다섯 배수 모두 자기 5년 이력의 비싼 쪽({selfsc:.1f}점)이고, IT 28종목 안에서도 가장 비싼 쪽({peersc:.1f}점)이다. '
           'PSR {SM[\'PSR\'][\'current\']:.1f}배는 5년 최고 수준이다. <strong>현금흐름 내재가치(기본 ${DCF[\'base\']:.0f})는 현재가의 {DCF[\'base\'] / px * 100:.0f}%</strong>로, '
           '과거 실적만으로는 현재가를 설명할 수 없다.')
RISK = ''
PEER_TIP = ('같은 GICS 섹터(Information Technology) 안에서 배수 순위를 매긴 값이다.',
            '회계 기준이 다른 종목(IFRS)과 사업모델이 다른 종목(파운드리)이 섞여 있다.')
STORIES = ['5년 성장률의 절반(연 {HIST[\'growth_5y\'] * 50:.0f}%)에서 식고, 영업이익률이 5년 중앙값 {pct(HIST[\'margin_5y\'])}로 내려간다.',
           '5년 성장률(연 {HIST[\'growth_5y\'] * 100:.0f}%)에서 식고, 영업이익률이 최근 2년 중앙값 {pct(HIST[\'margin_2y\'])}로 내려간다.',
           '3년 성장률(연 {HIST[\'growth_3y\'] * 100:.0f}%)에서 출발하고 최근 4분기 영업이익률 {pct(HIST[\'margin_now\'])}가 이어진다. 5년 뒤 매출 약 $76B.']
DCF_NOTE = ''
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = []   # 실적 보도자료 8-K는 news_auto.py가 넣는다
NEWS_DAYS = 400
SUMMARY = ('데이터센터 AI가 성장을 이끌고, 대형 GPU 계약을 워런트로 묶었다', '고성장·희석 변수',
           ['매출 성장률이 36%(Q3 2025) → 34% → 38% → 50%로 올라갔다. 2분기 데이터센터 매출 $6.7B(+107%)가 매출의 58%다.',
            'OpenAI(2025년 10월)·Meta(2026년 2월)와 각각 최대 6GW GPU 계약을 맺고, 각각 최대 1.6억 주 워런트(행사가 $0.01)를 줬다. 6월 말까지 베스팅된 물량은 없다.',
            '2분기 실적과 함께 Anthropic과 MI450 최대 2GW 협력을 발표했고, 3분기 매출 가이던스는 약 $13.0B(+41%)다.'],
           '두 워런트가 모두 베스팅되면 주식이 3.2억 주(지금의 약 20%) 늘어난다. GAAP 영업이익률은 인수 무형자산 상각($0.54B)과 주식보상($0.50B) 때문에 17%로 비GAAP 27%보다 낮다.',
           'Q3 2026 실적(11월 초 예상)에서 $13.0B 가이던스, MI450·Helios 출하, 워런트 첫 트랜치 베스팅 여부.')
BULL = [('데이터센터', '2분기 데이터센터 매출이 $6.7B로 1년 새 두 배를 넘었다(+107%).'),
        ('고객', 'OpenAI·Meta와 각각 최대 6GW GPU 계약, Anthropic과 최대 2GW 협력을 맺었다.'),
        ('재무', '유동비율 260.9%, 차입금 $3.2B로 차입금의존도가 3.8%다.')]
BEAR = [('밸류', 'PSR {SM[\'PSR\'][\'current\']:.1f}배가 5년 최고 수준이고, 기본 내재가치(${DCF[\'base\']:.0f})가 현재가에 한참 못 미친다.'),
        ('희석', '두 워런트가 모두 베스팅되면 주식이 약 20% 늘어난다(행사가 $0.01).'),
        ('게이밍', '2분기 게이밍 매출이 $779M로 31% 줄었다(세미커스텀 감소).')]
ANALYST = {'rating': 'Strong Buy', 'n': 62, 'nt': 39, 'mean': 323.87, 'median': 315, 'low': 250, 'high': 500, 'sb': 49, 'b': 10, 'h': 2, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-10-13'

# 카드 한정 패치(fill.py 끝에서 exec) — 틀 시절 카드에 있던 내용을 같은 자리에 되살린다.
PRE = []
POST = []
# ── 자동 카드(2026-10-11) — NVDA는 원래 틀 카드였다(newcards/template/NVDA_template.html). 이제 다른 카드처럼 그 틀을 복제해 생성기로 만든다 ──
AUTO = True
SEG_MAP = {"concepts": ["us-gaap:Revenues", "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
           "axis": "srt:ProductOrServiceAxis", "extra": {},
           "members": {"nvda:HyperscaleMember": ("하이퍼스케일", "#7c6ad6"),
                       "nvda:AICloudsIndustrialEnterpriseMember": ("AI 클라우드·산업·기업", "#4d7a00"),
                       "nvda:EdgeComputingMember": ("엣지 컴퓨팅", "#3b82f6")},
           "ignore": ["nvda:DataCenterMember"],   # 하이퍼스케일 + AI 클라우드의 합계 줄(겹친다)
           "other": "기타"}
