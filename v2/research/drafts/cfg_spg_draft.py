# 보류 초안(2026-10-22) — v2/research/skipped_cards.md SPG 줄. 다시 만들 때 v2/newcards/cfg/cfg_spg.py로 옮기고 등록(fetch_eps CIKS·activity·sectors·sec_approved)부터.
# SPG(사이먼 프로퍼티) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 163(시총 161위). 쇼핑몰·프리미엄 아웃렛 리츠(UPREIT).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-10), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 모두 동부 오후 4시대 접수 = 장 마감 뒤), 8-K(자사주 2/5, 경영진 3/24), StockAnalysis.
# 리츠: WELL·PLD·EQIX 선례대로 일반 규칙(영업이익 = 10-Q "Operating income before other items"), FFO는 판정에 쓰지 않는다. 순이익 = 보통주 귀속(NI_TAGS).
# 엔진 입력(2026-10-22): 운영 파트너십 외부 파트너 유닛 55,826,340(지분 14.7%, 보통주와 1:1 교환) — build_dcf SHARES_ADD로 주식에 더하고 비지배지분은 부동산분($382M, EV_TAGS_BY_CIK)만.
# 주식 수는 보통주 + B주 8,000(표지 클래스별, BUILD cover_shares). 합작 지분법 투자($5.4B, 손실 초과 배분 $1.8B 차감 전)와 그 이익은 모델에 없다(안건 E41).
# 4분기 EPS 2025 보도자료 $9.35(Taubman 잔여 지분 인수에 따른 재평가 이익 $2.89B 포함 — 최근 4분기 PER을 낮춘다).
BUILD = {'cover_shares': True}
NI_TAGS = ['NetIncomeLossAvailableToCommonStockholdersBasic']
CIK = '0001063761'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Simon'
S_ = 'https://www.sec.gov/Archives/edgar/data/1063761/'
SEC = S_
TENQ = S_ + '000110465926093360/spg-20260630x10q.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000110465926093361/tm2620726d2_ex99-1.htm', 'q1': S_ + '000110465926058646/tm2611645d2_ex99-1.htm',
      'q4': S_ + '000110465926009209/tm263695d2_ex99-1.htm', 'q3': S_ + '000110465925105545/tm2528944d2_ex99-1.htm'}
LINKS = {'ceo': S_ + '000110465926033931/tm269613d1_ex99-1.htm', 'buyback': S_ + '000110465926010999/tm265229d2_ex99-1.htm'}
FAIRBAND_TITLE = 'id="spgFairBand" title="최근 1년 PER 25~75% 구간 × 최근 4분기 희석 EPS. 최근 4분기 EPS에 Taubman 재평가 이익(일회성)이 들어 있어 이 범위는 참고용이다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 80)
ACT_REASON = ''
NONOP_WHAT = '투자'
YOY_NOTE = {'2026-06-30': '최근 4분기 순이익에는 Q4 2025 Taubman 잔여 지분 인수 재평가 이익 $2.89B(일회성·비현금)가 들어 있어 PER이 실제보다 낮게 나온다'}
# 고정 문장(숫자 없음). 리츠에 일반 모델, 유닛, 합작 지분, 일회성 이익.
MODEL_NOTE = ('리츠에 일반 기업용 모델을 그대로 쓴 참고 값이다 — 현금흐름 내재가치는 영업이익·재투자 모델이라 리츠의 FFO 기반 평가가 아니고, 합작 쇼핑몰 지분(지분법 투자)과 그 이익은 모델에 들어 있지 않다. '
              '운영 파트너십 외부 파트너 유닛은 보통주와 1:1로 교환되므로 주당 내재가치는 주식과 유닛을 합친 수로 나눈다. 최근 4분기 순이익에는 큰 일회성 재평가 이익이 있어 PER과 자기 이력 PER 점수가 실제보다 싸게 보인다.')
HEALTH_EXTRA = '부채비율이 매우 높게 나오는 것은 누적 배당과 감가상각으로 장부상 자본이 작기 때문이다 — 리츠는 보통 부채를 자산 가치나 이익 대비로 본다.'
PH = ['PLD', 'WELL', 'EQIX', 'O', 'AMT', 'PSA']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(SPG 제외)과 배수 순위를 매긴 값이다.',
            '쇼핑몰·물류·데이터센터·통신탑·주거·헬스케어 리츠가 섞여 있다. 차트에는 대형 리츠 6곳만 보인다.')
# 매출(Q2 2026 10-Q 손익계산서) — 임대 수익 1,659.7 + 관리 수수료·기타 40.8 + 기타 수익 90.1 = 1,790.6. 1년 전 1,379.5·37.9·81.1 → 1,498.5.
SEG = [('임대 수익', 1659.7, '#1d3c6e'), ('기타 수익', 90.1, '#6b8fc7'), ('관리 수수료·기타', 40.8, '#a8bfe0')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 손익계산서 항목별'
# 손 뉴스: 실적 4건(EPS는 GAAP 보통주 귀속 — 보도자료의 FFO는 쓰지 않는다), 경영진 교체, 자사주. 가이던스는 쓰지 않는다.
# 반응일(SEC acceptanceDateTime UTC → 동부): 실적 8-K 2025-11-03T21:08Z·2026-02-02T21:12Z·05-11T20:07Z·08-10T20:07Z = 장 마감 뒤 → 다음 세션.
# 자사주 8-K 2026-02-05T21:44Z → 2/6. David Simon 별세(3/22) 보도자료는 3/23자, 8-K는 3/24T21:07Z — 반응일은 보도자료 날인 3/23(첫 공개일).
# 넣지 않은 8-K: 신용 약정(3/5), 주총(5/15), 임원(2/5 5.02항).
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 10일 — Q2 2026 실적', '2026-08-11',
     '총매출 $1.79B(+19.5%) · 희석 EPS $1.49(1년 전 $1.70 — 투자 관련 비현금 이익 $0.21 포함)', 'q2', 'Simon 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 11일 — Q1 2026 실적', '2026-05-12',
     '총매출 $1.76B(+19%) · 희석 EPS $1.48(1년 전 $1.27) · 미국 몰·아웃렛 입점률 96.0%', 'q1', 'Simon 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 23일 — David Simon 회장 겸 CEO 별세', '2026-03-23',
     '3월 22일 별세 — 아들 Eli Simon(COO)이 CEO·사장, Larry Glasscock이 비상임 이사회 의장', 'ceo', 'Simon 보도자료·공시 (SEC 8-K)'),
    ('green', '2026년 2월 5일 — 자사주 매입 $2.0B 승인', '2026-02-06',
     '새 보통주 매입 프로그램 최대 $2.0B', 'buyback', 'Simon 공시 (SEC 8-K)'),
    ('neutral', '2026년 2월 2일 — Q4 2025 실적', '2026-02-03',
     '희석 EPS $9.35(1년 전 $2.04) — Taubman 잔여 지분 인수에 따른 비현금 재평가 이익 $2.89B 포함', 'q4', 'Simon 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 3일 — Q3 2025 실적', '2025-11-04',
     '희석 EPS $1.86(1년 전 $1.46)', 'q3', 'Simon 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 18, 'mean': 227.56, 'median': 222, 'low': 205, 'high': 275, 'sb': 5, 'b': 1, 'h': 15, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-22'
# Codex r1 필수(반영 전 보류): ① 상환가능 지분 $271.8M(외부 우선유닛 $10.5M + 기타 $261.3M, TemporaryEquityCarryingAmountIncludingPortionAttributableToNoncontrollingInterests)도 EV·주주가치에서 뺄 것
# ② 배수 시가총액에 유닛 가치(55.8M × 주가) — 배수 엔진에 시점별 유닛 수 장치가 필요. 권장: 2025-10-31 Taubman 잔여 12% 인수·연결 뉴스, 적정주가 밴드에 일회성 경고.

# ── 자동 카드 — 손익계산서 항목 3개(축 없음). 원문 대조: Q2 2026 1,659.7/90.1/40.8, 1년 전 1,379.5/81.1/37.9(2026-10-22) ──
AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {"us-gaap:OperatingLeaseLeaseIncome": ["임대 수익", "#1d3c6e"], "us-gaap:OtherIncome": ["기타 수익", "#6b8fc7"],
             "spg:ManagementFeesAndOtherRevenues": ["관리 수수료·기타", "#a8bfe0"]},
 "ignore": []
}
