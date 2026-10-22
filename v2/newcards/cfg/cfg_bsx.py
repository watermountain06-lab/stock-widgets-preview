# BSX(보스턴 사이언티픽) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 165(시총 164위). 의료기기(심혈관 — 전기생리·Watchman·스텐트, 메드서지 — 내시경·비뇨기·신경조절).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-03), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 보도자료는 장 전, 8-K는 장중 접수), 8-K(Penumbra 1/15, 임상 3/30, MiRus·ASR 5/18, 구조조정 7/27, 사이버 사고 8/26·9/8, 조직 개편 10/7), StockAnalysis.
# 엔진 입력(2026-10-22): 차입금 = 1년 안 1,709(DebtCurrent) + 장기 10,915 = $12,624M(DEBT_TOTAL_TAG — 1년 안 부분이 빠져 있었다). 순이익은 보통주 귀속(NetIncomeLoss 태그가 2010년에 멈춤).
# 기타 투자 $2,245M(MiRus 지분 34% $1.5B 포함)는 비영업 자산. Penumbra 인수($14.5B, 현금·주식)는 FTC 추가 자료 요청으로 아직 미완료 — 숫자에 없다.
# 주가는 2025-10 약 $104에서 기준일 $44.51로 떨어졌다(분할 아님). 이익은 늘었는데 배수가 크게 내려가 자기 이력 점수가 거의 만점이다.
NI_TAGS = ['NetIncomeLossAvailableToCommonStockholdersBasic', 'ProfitLoss']
CIK = '0000885725'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Boston Scientific'
S_ = 'https://www.sec.gov/Archives/edgar/data/885725/'
SEC = S_
TENQ = S_ + '000088572526000053/bsx-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000088572526000051/q22026earningsrelease.htm', 'q1': S_ + '000088572526000031/q12026earningsrelease.htm',
      'q4': S_ + '000088572526000006/q42025earningsrelease.htm', 'q3': S_ + '000088572525000046/q32025earningsrelease.htm'}
LINKS = {'pen': 'https://www.sec.gov/Archives/edgar/data/885725/000094787126000034/ss5822817_ex9901.htm',
         'trial': S_ + '000088572526000029/ex992-pressrelease.htm', 'mirus': S_ + '000088572526000041/exhibit991-pressrelease_fi.htm',
         'asr': S_ + '000088572526000042/exhibit991-pressrelease_fi.htm', 'cyber1': S_ + '000088572526000056/bsx-20260826.htm',
         'cyber2': S_ + '000088572526000059/bsx-20260907.htm', 'restr': S_ + '000088572526000049/bsx-20260721.htm',
         'cyber3': 'https://news.bostonscientific.com/9-09-26-cyber-update-archive', 'restr2': S_ + '000088572526000064/ex991-octoberbscpressrelea.htm'}
FAIRBAND_TITLE = 'id="bsxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
YOY_NOTE = {'2026-06-30': 'Q1 2026 순이익에는 법인세 이익 $176M(세금이 마이너스)이 들어 있어 최근 4분기 EPS가 그만큼 크다'}
# 고정 문장(숫자 없음). 급락, 사이버 사고, 미완료 인수.
MODEL_NOTE = ('주가가 1년 사이 크게 떨어지는 동안 매출·이익은 늘어 배수가 5년 중 가장 낮은 쪽에 있다 — 자기 이력 점수가 높은 이유다. 다만 회사는 올해 연간 성장 전망을 두 번 낮췄고, '
              '8월 사이버 공격으로 제조·출하에 차질이 생겨 3분기·연간 실적이 기존 전망에 못 미칠 것이라고 밝혔다(9월 9일 운영은 복구). 사이버 사고의 영향은 아직 이 카드의 숫자(2분기까지)에 없다. 회사는 전기생리 경쟁 심화와 일부 Watchman 시술 둔화가 이미 2분기 매출에 영향을 줬다고 10-Q에 적었다. 발표만 된 Penumbra 인수도 숫자에 들어 있지 않다. '
              '현금흐름 내재가치가 낮은 것은 최근 인수로 투하자본이 커져 매출 대비 자본 효율이 낮게 잡히고, 모델이 그만큼 큰 재투자를 요구하기 때문이다(낙관 시나리오는 처음부터 이 낮은 효율을 쓴다).')   # Codex r1 필수
PH = ['MDT', 'SYK', 'ABT', 'EW', 'ISRG', 'BDX']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '의료기기 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': '의료기기 PBR 비교', 'psr': '의료기기 PSR 비교',
                'pcr': '의료기기 PCR(FCF) 비교', 'evebitda': '의료기기 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(BSX 제외)와 배수 순위를 매긴 값이다.',
            '제약·바이오·보험·의료기기·서비스가 섞여 있다. 차트에는 의료기기 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 심혈관 3,624 + 메드서지 1,818 = 5,442. 1년 전 3,345·1,716 → 5,061.
SEG = [('심혈관', 3624.0, '#0a3d8f'), ('메드서지', 1818.0, '#5a8fd6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석, 조정 EPS는 쓰지 않는다 — 다만 연간 매출 성장 전망 경로는 주가 급락의 1차 자료상 원인이라 적는다, Codex·Fable r1 필수), 인수·투자·자사주·임상·구조조정·사이버 사고.
# 반응일: 보도자료는 장 전 배포, 8-K 접수 시각 UTC 2025-10-22T14:32Z·2026-02-04T16:33Z·04-22T14:34Z·07-29T14:33Z = 장중 → 같은 날.
# Penumbra 8-K(7.01) 2026-01-15T17:21Z → 1/15. 임상 3/30T14:14Z → 3/30. MiRus·ASR 5/18T15:15Z → 5/18. 구조조정 7/28T00:06Z(7/27 동부 20:06) → 7/28.
# 사이버 8/26T14:06Z → 8/26, 9/8T14:15Z → 9/8, 9/9 복구 공지(회사 웹사이트, 동부 19:53) → 9/10. 조직 개편 10/7T14:11Z → 10/7. 넣지 않은 8-K: 임원(10/23·11/19·2/5·2/23·9/23), 신용 약정(1/15·2/26), 주총(5/5).
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 7일 — COO 선임·3개 부문 체제', '2026-10-07',
     'Joseph Fitzgerald를 2027년 1월부터 COO로 — 보고 부문을 중재 치료·리듬 솔루션·메드서지 3개로 바꾼다', 'restr2', 'Boston Scientific 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 9월 9일 — 제조·출하 완전 복구', '2026-09-10',
     '제조·주문 처리·출하가 모두 복구되고 주문 적체를 줄이는 중이라고 공지(동부 오후 7시 53분)', 'cyber3', 'Boston Scientific 웹사이트 공지'),
    ('red', '2026년 9월 8일 — 사이버 사고, 실적 전망 미달 예고', '2026-09-08',
     '8월 25일 사이버 공격으로 제조·출하 차질 — 3분기·연간 매출 성장과 조정 EPS 전망 범위를 맞추기 어렵다고 공시(1.05항)', 'cyber2', 'Boston Scientific 공시 (SEC 8-K)'),
    ('red', '2026년 8월 26일 — 사이버 공격으로 전 세계 운영 차질', '2026-08-26',
     '8월 25일 정보 시스템 침입을 확인 — 일부 시스템 접근 제한으로 운영 차질', 'cyber1', 'Boston Scientific 공시 (SEC 8-K)'),
    ('neutral', '2026년 7월 29일 — Q2 2026 실적', '2026-07-29',
     '매출 $5.44B(+7.5%) · 희석 EPS $0.61(1년 전 $0.53) · 연간 매출 성장 전망(보고 기준)을 7.0~8.5%에서 5.5~6.5%로 다시 낮춤', 'q2', 'Boston Scientific 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 27일 — 새 구조조정 계획', '2026-07-28',
     '7월 21일 이사회 승인 — 생산 라인 이전 등 공급망 최적화·조직 개편, 세전 비용 약 $700~800M·연 비용 절감 약 $500M 예상(2.05항)', 'restr', 'Boston Scientific 공시 (SEC 8-K)'),
    ('green', '2026년 5월 18일 — MiRus 지분 투자 · 자사주 $2B ASR', '2026-05-18',
     'TAVR 개발사 MiRus 지분 약 34%에 $1.5B(인수 옵션 포함) · JPMorgan과 $2B 가속 자사주 매입', 'mirus', 'Boston Scientific 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 22일 — Q1 2026 실적', '2026-04-22',
     '매출 $5.20B(+11.6%) · 희석 EPS $0.90(1년 전 $0.45, 법인세 이익 포함) · 연간 매출 성장 전망(보고 기준)을 2월의 10.5~11.5%에서 7.0~8.5%로 낮춤', 'q1', 'Boston Scientific 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 28일 — CHAMPION-AF 임상 결과', '2026-03-30',
     'Watchman FLX가 항응고제 대비 1차 치료 임상의 모든 1·2차 목표를 충족(3/28 ACC 발표·NEJM 게재, 보도자료 8-K 3/30) — 같은 날 HI-PEITHO 임상 긍정 결과도 발표, 첫 거래일 주가 하락 원인은 공시로 확인되지 않음', 'trial', 'Boston Scientific 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 4일 — Q4 2025 실적', '2026-02-04',
     '매출 $5.29B(+15.9%) · 희석 EPS $0.45(1년 전 $0.38) · 2025년 매출 $20.07B(+19.9%) · 2026년 매출 성장 전망 10.5~11.5% — 이날 주가 하락을 두고 3월 5일 주주 집단소송 제기(10-Q)', 'q4', 'Boston Scientific 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 15일 — Penumbra 인수 합의', '2026-01-15',
     '혈전 제거 기기 회사 Penumbra를 주당 $374(기업가치 약 $14.5B, 현금·주식)에 인수 합의 — 3월 FTC 추가 자료 요청, 미완료', 'pen', 'Boston Scientific 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 22일 — Q3 2025 실적', '2025-10-22',
     '매출 $5.07B(+20.3%) · 희석 EPS $0.51(1년 전 $0.32)', 'q3', 'Boston Scientific 실적 보도자료 (SEC 8-K)'),
]
# 다음 실적일: 9/8 8-K(1.05항) — 10/28(수) 3분기 실적 콜에서 연간 전망 갱신(Codex r1 필수)
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-28', 'src': '9/8 회사 공시(8-K) — 3분기 실적 콜 10월 28일'}
ANALYST = {'rating': 'Buy', 'n': 31, 'nt': 23, 'mean': 57.13, 'median': 56, 'low': 48, 'high': 70, 'sb': 18, 'b': 7, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'

# ── 자동 카드 — 부문 2개. 원문 대조: Q2 2026 3,624/1,818, 1년 전 3,345/1,716(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"bsx:CardiovascularMember": ["심혈관", "#0a3d8f"], "bsx:MedsurgMember": ["메드서지", "#5a8fd6"]},
 "ignore": []
}
