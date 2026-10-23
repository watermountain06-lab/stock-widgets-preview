# ALL(올스테이트) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 166(시총 165위). 미국 개인 손해보험(자동차·주택), 보호 서비스(보증·신원 보호 등).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05 장 마감 뒤), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 장 마감 뒤 접수), 월간 자연재해 손실 8-K(7.01항), StockAnalysis.
# 손해보험사라 현금흐름 모델은 미적용(TRV·CB·PGR과 같은 방식) — 판정 보류.
# 엔진 입력(2026-10-22): 차입금 $7,492M(재무상태표 "Debt" — 합계 태그는 2025-12에 멈춰 LongTermDebt로 채움, 값 같음). 현금 $840M(단기 증권은 보험 운용자산이라 뺌 — TRV와 같음).
# 우선주 $2,001M(PreferredStockIncludingAdditionalPaidInCapital, 청산가치 $2,050M — EV_TAGS_BY_CIK). PBR 분모의 자기자본에는 우선주가 들어 있다(안건 E44). 4분기 EPS 2025 보도자료 값.
BUILD = {'no_dcf': '손해보험사라 현금흐름 모델을 쓰지 않는다'}
NO_DCF_SKEW = True   # 금융 카드 — 현금흐름 칸 쏠림 메모(A0) 없음
NI_TAGS = ['NetIncomeLossAvailableToCommonStockholdersBasic', 'NetIncomeLoss']
CIK = '0000899051'
OP_DISPLAY = (['NetIncomeLoss'], [(['IncomeTaxExpenseBenefit'], 1), (['InterestExpenseOperating', 'InterestExpense'], 1)])   # 카드 표시용 영업이익 = 순이익 + 법인세 + 이자비용(= 세전이익 + 이자비용, TRV·CB와 같은 뜻 — 세전이익 태그가 2025-12에 멈춰서). Q2 2026: 3,271 + 871 + 96 = 4,238
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, None, 0), '판정 보류'
CO = 'Allstate'
S_ = 'https://www.sec.gov/Archives/edgar/data/899051/'
SEC = S_
TENQ = S_ + '000089905126000118/all-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000089905126000117/allcorp63026earningsreleas.htm', 'q1': S_ + '000089905126000074/allcorp33126earningsreleas.htm',
      'q4': S_ + '000089905126000013/allcorp123125earningsrelea.htm', 'q3': S_ + '000089905125000100/allcorp93025earningsreleas.htm'}
LINKS = {'cat': S_ + '000089905126000150/exhibit99newsrelease101526.htm', 'cfo': S_ + '000089905126000109/exhibit991lowncfoappointme.htm'}
FAIRBAND_TITLE = 'id="allFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (현금흐름 미적용)</span>'
OPM_RANGE, Y2 = (-50, 50), (0, 30)
ACT_REASON = '보험사라 재고·매출채권 회전으로 보는 활동성이 맞지 않는다'
HEALTH_EXTRA = '보험사라 부채에서 보험금 준비금·미경과보험료 같은 보험 부채 비중이 크고, 유동·당좌비율과 활동성은 맞지 않는다. 자기자본에는 보유 채권의 평가손익과 우선주가 들어 있다. 현금 칸에는 보험 운용자산인 단기 증권을 넣지 않았다.'
NONOP_WHAT = '투자'
YOY_NOTE = {'2026-06-30': 'Q2 2026 세전이익 $4,142M에는 투자·파생상품 순이익 $1,055M(약 25%, 1년 전 −$144M)이 들어 있고, 1년 전 분기 세전이익에는 사업 매각 이익 $890M이 있었다'}   # Codex r2 권장
# 고정 문장(숫자 없음). 현금흐름 미적용, 보험료 인상·낮은 자연재해 손실로 이익이 사상 최대 수준 — PER이 낮은 이유, 이익 변동.
MODEL_NOTE = ('손해보험사라 현금흐름 모델을 쓰지 않아 판정을 보류한다. 최근 4분기는 자동차·주택 보험료 인상이 쌓이고 자연재해 손실이 평소보다 적고 과거 준비금 환입까지 겹쳐 이익이 매우 컸다 — '
              '보유 주식·채권의 투자 평가·처분 이익과 사업 매각 이익도 이익을 키웠다(되풀이를 전제할 수 없다). PER이 5년 중 가장 낮은 쪽인 이유다. 손해보험 이익은 자연재해와 사고 빈도에 따라 크게 흔들리므로 이 수준이 이어진다고 볼 수는 없다. '
              '동종업 칸은 쓸 수 있는 배수가 적어 판정 표에서 빠진다(점수는 참고).')
STORIES = ['보험사라 현금흐름 모델을 쓰지 않는다.', '보험사라 현금흐름 모델을 쓰지 않는다.', '보험사라 현금흐름 모델을 쓰지 않는다.']
DCF_NOTE = '손해보험사는 보험료를 먼저 받고 보험금을 나중에 내는 구조라 일반 기업의 잉여현금흐름 모델이 맞지 않는다. 현금흐름 칸이 비어 TRV·CB·PGR처럼 판정을 보류한다(두 배수 칸은 참고로 표시).'
PH = ['PGR', 'TRV', 'CB', 'AIG', 'HIG', 'WRB']
PEER_FILE = 'peer_universe/insurers.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '손해보험 6곳 PER 비교 (점수는 S&P500 보험사 기준)', 'pbr': '손해보험 PBR 비교', 'psr': '손해보험 PSR 비교',
                'pcr': '손해보험 PCR(FCF) 비교', 'evebitda': '손해보험 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 보험사(손해·종합·생명)보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 보험사 대비 배수 순위 (v2/peer_universe/insurers.json)'
PEER_TIP = ('S&P500 손해·종합·생명보험사(ALL 제외, 보험 중개사 제외)와 배수 순위를 매긴 값이다.',
            '생명보험사가 섞여 있다. 차트에는 손해보험 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문 수익 표) — Allstate Protection 15,486 = 보험료 14,918 + 기타 568(XBRL은 PremiumsEarnedNet × 부문 축으로 태깅 — 경과보험료 아님, Fable r1). 나머지 3,110(보호 서비스 961·투자 수익·기타)을 더해 총수익 18,596. 1년 전 14,850.
SEG = [('손해보험 부문 수익(보험료·기타)', 15486, '#0033a0')]
SEG_ADJ = 3110
SEG_TITLE = '매출 구성 — 손해보험 부문 수익(보험료·기타)와 그 밖의 수익'
SEG_ADJ_LABEL = '보호 서비스·투자 수익·기타'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS는 쓰지 않는다), 3분기 자연재해 손실, CFO. 가이던스는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K 2025-11-06T02:17Z·2026-02-05T02:17Z·04-30T00:15Z·08-06T00:15Z = 전날 장 마감 뒤 → 다음 세션.
# 9월·3분기 자연재해 8-K 2026-10-15T15:41Z(장중) → 10/15. CFO 8-K 2026-07-15T00:39Z(7/14 동부 20:39) → 7/15.
# 넣지 않은 8-K: 월간 자연재해 손실(매달 7.01항 — 3분기 합계만 넣음), 임원 교체(2025-10-01·11-20), 주총(5/27).
NEWS_RANGE = '2025.11 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 15일 — 3분기 자연재해 손실 $1.65B', '2026-10-15',
     '9월 자연재해 손실 추정 $220M, 3분기 합계 $1.65B(세후 $1.30B) — 1년 전 3분기 $558M보다 크다', 'cat', 'Allstate 보도자료 (SEC 8-K)'),
    ('green', '2026년 8월 5일 — Q2 2026 실적', '2026-08-06',
     '총수익 $18.6B(+11.8%) · 희석 EPS $12.51(1년 전 $7.76) · 손해보험 합산비율 86.6%(4.5%p 개선) · 자연재해 손실 $1.72B · 자사주 매입 $1.0B', 'q2', 'Allstate 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 14일 — 새 CFO 선임', '2026-07-15',
     'Chris Lown을 8월 3일부터 CFO로 선임', 'cfo', 'Allstate 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 29일 — Q1 2026 실적', '2026-04-30',
     '총수익 $16.9B(+3.0%) · 희석 EPS $9.25(1년 전 $2.11 — 그 분기 LA 산불 등 자연재해 손실 $2.2B) · 합산비율 82.0%', 'q1', 'Allstate 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 4일 — Q4 2025 실적 · 배당 인상 · 자사주 $4B', '2026-02-05',
     '총수익 $17.3B(+5.1%) · 희석 EPS $14.37(1년 전 $7.07) · 합산비율 72.9% · 분기 배당 $1.08로 인상, 자사주 매입 $4.0B 새 프로그램', 'q4', 'Allstate 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 5일 — Q3 2025 실적', '2025-11-06',
     '총수익 $17.3B(+3.8%) · 희석 EPS $13.95(1년 전 $4.33, 단체 건강 사업 매각 이익 세전 $720M 포함) · 합산비율 80.1%(16.3%p 개선) · 자연재해 손실 $558M(1년 전 $1.70B)', 'q3', 'Allstate 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 25, 'nt': 20, 'mean': 267.5, 'median': 266, 'low': 215, 'high': 340, 'sb': 9, 'b': 2, 'h': 10, 's': 2, 'ss': 2}
ANALYST_ASOF = '2026-10-22'

# ── 자동 카드 — 부문 지도는 손으로(TRV와 같은 경과보험료 기준). 10-Q XBRL PremiumsEarnedNet × 부문 축: Q2 2026 15,486, 1년 전 14,850(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:PremiumsEarnedNet"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"all:PropertyLiabilityMember": ["손해보험 부문 수익(보험료·기타)", "#0033a0"]},
 "ignore": []
}
