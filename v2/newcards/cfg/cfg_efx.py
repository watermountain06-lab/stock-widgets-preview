# EFX(에퀴팩스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 신용정보(미국 소비자·기업 신용 보고서), 소득·고용 확인(Workforce Solutions — The Work Number), 해외 신용정보.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-20), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/EFX.md.
# 엔진 입력(2026-10-25): 차입금 = 1년 안 $157.7M + 장기 $5,049.0M(DEBT_TOTAL_TAG — LongTermDebt 태그는 10-K만), 현금 $192.9M, 비지배지분 = 상환가능 $120.8M + $20.5M(EV_TAGS nci).
# 일회성: 소송 합의 충당(Q4 2025 세후 $0.18, Q2 2026 세후 $0.25 — 최근 4분기 EPS 6.19의 약 7%).
CIK = '0000033185'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'Equifax'
S_ = 'https://www.sec.gov/Archives/edgar/data/33185/'
SEC = S_
TENQ = S_ + '000003318526000044/efx-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000003318526000037/exhibit99120260930.htm', 'q2': S_ + '000003318526000024/exhibit99120260630.htm',
      'q1': S_ + '000003318526000016/exhibit99120260331.htm', 'q4': S_ + '000003318526000004/a2025q48-kexhibit991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="efxFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 25)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('인수로 생긴 무형자산 상각(분기 약 $60M)이 커서 GAAP 이익이 회사 조정 이익보다 낮다. 데이터·클라우드 전환 투자(자본화 소프트웨어 포함)로 감가상각도 크다. '
              '미국 주택담보대출 시장 경기에 따라 신용조회 수요가 크게 오르내린다. 최근 4분기 이익에는 소송 합의 충당(주당 약 $0.43)이 들어 있다 — 빼도 세 표는 같다. '
              '운용리스 부채는 10-Q에서 기타 부채에 묶여 태깅되지 않아 리스 포함 순차입금에 빠져 있다(2025년 말 미할인 지급약정 $149M). '
              '현금흐름 모델 값이 낮은 것은 영업권이 투하자본의 대부분이라(매출/자본 약 0.70배) 투하자본 이익률이 할인율과 비슷해 성장이 가치를 거의 더하지 못하기 때문이다.')
PH = ['VRSK', 'ADP', 'PAYX', 'BR', 'CTAS', 'LDOS']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '전문 서비스 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(EFX 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·전기 설비·전문 서비스가 섞여 있다. 차트에는 전문 서비스 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — Workforce 693.9 + 미국 소비자 정보 599.1 + 해외 399.5 = 1,692.5.
SEG = [('소득·고용 확인(Workforce)', 693.9, '#9e1b32'), ('미국 신용정보(USIS)', 599.1, '#d4697d'), ('해외', 399.5, '#3d3d3d')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:31~06:32 동부 접수) → 같은 날. 넣지 않은 8-K: 신용 한도, 주총, 정관, 사채 $1B(7/29).
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 20일 — Q3 2026 실적', '2026-10-20',
     '매출 $1.69B(+9.6%) · 순이익 $212M · 희석 EPS $1.79(1년 전 $1.29 — 구조조정 포함) — 발표 당일 주가 +11%', 'q3', 'Equifax 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 21일 — Q2 2026 실적', '2026-07-21',
     '매출 $1.70B · 순이익 $184M · 희석 EPS $1.54(1년 전 $1.53) — 소송 합의 충당 세전 $40M(보험 차감 후) 포함', 'q2', 'Equifax 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 21일 — Q1 2026 실적', '2026-04-21',
     '매출 $1.65B · 순이익 $172M · 희석 EPS $1.42(1년 전 $1.06)', 'q1', 'Equifax 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 4일 — Q4 2025 실적', '2026-02-04',
     '매출 $1.55B · 순이익 $176M · 희석 EPS $1.44(1년 전 $1.39) — 소송 합의 충당 세전 $30M 포함 · 2025년 EPS $5.32', 'q4', 'Equifax 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 20, 'mean': 201.3, 'median': 201, 'low': 155, 'high': 245, 'sb': 13, 'b': 5, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 3개(수동 지도, 영업 부문 차원). 원문 대조: Q3 2026 693.9/599.1/399.5(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"efx:WorkforceSolutionsMember": ["소득·고용 확인(Workforce)", "#9e1b32"], "efx:UnitedStatesConsumerInformationSolutionsMember": ["미국 신용정보(USIS)", "#d4697d"],
             "efx:InternationalMember": ["해외", "#3d3d3d"]},
 "ignore": []
}
