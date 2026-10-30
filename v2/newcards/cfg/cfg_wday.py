# WDAY(워크데이) v2 카드 설정 — 자동 카드(AUTO). 회계연도 1월 31일(FY2027 = 2026-02-01~2027-01-31). 카드 순위 192. 기업용 클라우드 인사·재무 소프트웨어(구독).
# 출처: SEC XBRL, Q2 FY27 10-Q(2026-08-28T00:11Z), 실적 보도자료(Q3 FY26~Q2 FY27, 8-K 2.02항 — 장 마감 뒤 발표, 4:30 ET 콜), 8-K(구조조정 2/4·9/29, CEO 교체 2/9, 사채 10/23), StockAnalysis. 사전 조사 자료표 scratchpad pre/WDAY.md.
# 엔진 입력(2026-10-24): 일회성 세금 혜택 Q2 FY27 $374M(EPS $1.52)은 tax_oneoff.json, 4분기 EPS FY2021·2022·2024·2025·2026 보도자료 값, 인수 TTM $2.1B(Paradox·Sana).
# 차입금 $2,989M은 7/31 기준 — 10/23 사채 $2.5B 발행(2027 만기 $1.0B 상환 예정)은 다음 분기 재무상태표부터. 단일 부문 — 매출 구성은 구독·전문 서비스.
# 다중 클래스(A·B) — 표지 주식 수가 클래스별뿐이라 companyfacts 주식 수가 2018년에 멈췄다 → BUILD cover_shares(DDOG 방식, Codex r1)
BUILD = {'cover_shares': True}
CIK = '0001327811'
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q2 FY27', 'Q2 FY26', 'Q1 FY27'
L8 = ['Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27', 'Q2 FY27']
FY_ENDS, FY_LABEL = ('2026-01-31', '2025-01-31'), 'FY2026'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Workday'
S_ = 'https://www.sec.gov/Archives/edgar/data/1327811/'
SEC = S_
TENQ = S_ + '000132781126000044/wday-20260731.htm'; TENQ_NAME = 'Q2 FY27 10-Q'
PR = {'q2': S_ + '000132781126000042/wday-07312026x991.htm', 'q1': S_ + '000132781126000024/wday-04302026x991.htm',
      'q4': S_ + '000132781126000010/wday-01312026x991.htm', 'q3': S_ + '000132781125000196/wday-10312025x991.htm'}
LINKS = {'reorg': S_ + '000132781126000048/wday-20260929.htm', 'ceo': S_ + '000132781126000007/wday-20260206.htm',
         'reorg1': S_ + '000132781126000004/wday-20260130.htm', 'notes': S_ + '000110465926118496/tm2626731d6_8k.htm'}
FAIRBAND_TITLE = 'id="wdayFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('주식보상비용이 커서 GAAP 영업이익률이 회사가 발표하는 조정 이익률보다 훨씬 낮고, 이 모델은 GAAP 이익률에서 출발한다. '
              '현금흐름 내재가치가 보고 FCF에 비해 매우 낮은 주된 이유는 최근 4분기 인수 대금(Paradox·Sana)을 성장에 든 재투자로 넣어 자본 효율이 낮게 잡히고, 자본수익률이 할인율보다 낮아 성장이 가치를 더하지 못하기 때문이다. 보수 시나리오가 0 이하인 것은 모델 계산상 그렇다는 뜻이지 주주가 돈을 더 내야 한다는 뜻이 아니다. '
              'Q2 FY27 GAAP 이익에는 지식재산 이전에 따른 일회성 세금 혜택이 있어 PER의 최근 4분기 EPS와 내재가치 세율에서 뺐다(분기 EPS·순이익률 칸에는 그대로 있다). 5년 이력 앞부분은 GAAP 적자·이익이 작던 시기라 PER·EV/EBITDA 이력이 매우 넓다. '
              '10월 새 사채 발행분은 다음 분기 재무상태표부터 차입금에 들어간다 — 일부는 2027년 만기 사채 상환, 나머지는 일반 목적이고, 이자율이 기존 사채보다 높아 이자 부담이 커진다.')
PH = ['CRWD', 'PANW', 'CRM', 'MSFT', 'ORCL', 'PLTR']
PEER_FILE = None
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소프트웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': '소프트웨어 PBR 비교', 'psr': '소프트웨어 PSR 비교',
                'pcr': '소프트웨어 PCR(FCF) 비교', 'evebitda': '소프트웨어 EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(WDAY 제외)과 배수 순위를 매긴 값이다.',
            '반도체·하드웨어·소프트웨어가 섞여 있다. 차트에는 소프트웨어 6곳만 보인다.')
# 매출(Q2 FY27 10-Q) — 구독 2,471 + 전문 서비스 178 = 2,649. 단일 부문.
SEG = [('구독', 2471.0, '#0875e1'), ('전문 서비스', 178.0, '#f5a623')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 구독·서비스'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다) + 구조조정 2건 + CEO 교체. 반응일: 실적·구조조정 8-K는 장 마감 뒤 → 다음 거래일, CEO 8-K 2/9 18:31Z(장중) → 2/9.
# 자사주 $4.0B 추가 승인(2026-08, 10-Q 주석 — 8-K 없음)은 Q2 실적 뉴스에 붙였다(Codex r2). 넣지 않은 8-K: 사채 $2.5B(10/23 저녁, 반응 없음 — MODEL_NOTE), 신용 한도(10/1), C1.ai 인수 계약(10/13, 금액 비공개), 보상 정책.
NEWS_RANGE = '2025.11 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 29일 — 두 번째 구조조정 발표', '2026-09-30',
     '인력 약 2.5% 감축, 비용 $65~80M(대부분 Q3 FY27) — 매출 전망은 유지', 'reorg', 'Workday 공시 (SEC 8-K)'),
    ('green', '2026년 8월 27일 — Q2 FY27 실적', '2026-08-28',
     '매출 $2.65B(1년 전 $2.35B) · 순이익 $632M · 희석 EPS $2.57(1년 전 $0.84) — 일회성 세금 혜택 $374M(EPS $1.52) 포함 · 기존 자사주 매입 한도 소진, 8월 $4.0B 추가 승인(10-Q)', 'q2', 'Workday 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 21일 — Q1 FY27 실적', '2026-05-22',
     '매출 $2.54B · 순이익 $222M · 희석 EPS $0.87(1년 전 $0.25)', 'q1', 'Workday 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 24일 — Q4 FY26 실적', '2026-02-25',
     '매출 $2.53B · 순이익 $145M · 희석 EPS $0.55(1년 전 $0.35) — 구조조정 비용 $130M 포함', 'q4', 'Workday 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 9일 — 창업자 Aneel Bhusri CEO 복귀', '2026-02-09',
     'Carl Eschenbach 최고경영자 퇴임', 'ceo', 'Workday 공시 (SEC 8-K)'),
    ('red', '2026년 2월 4일 — 구조조정 발표', '2026-02-05',
     '인력 약 2% 감축, 비용 약 $135M(Q4 FY26)', 'reorg1', 'Workday 공시 (SEC 8-K)'),
    ('red', '2025년 11월 25일 — Q3 FY26 실적', '2025-11-26',
     '매출 $2.43B · 순이익 $252M · 희석 EPS $0.94(1년 전 $0.72) — 발표 다음 날 주가 −8%', 'q3', 'Workday 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 42, 'nt': 29, 'mean': 208.66, 'median': 210, 'low': 92, 'high': 275, 'sb': 14, 'b': 5, 'h': 20, 's': 2, 'ss': 1}
ANALYST_ASOF = '2026-10-24'


# ── 자동 카드 — 구독·서비스 2개(수동 지도, 제품·서비스 축). 원문 대조: Q2 FY27 2,471/178(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"wday:SubscriptionServicesMember": ["구독", "#0875e1"], "wday:ProfessionalServicesMember": ["전문 서비스", "#f5a623"]},
 "ignore": []
}
