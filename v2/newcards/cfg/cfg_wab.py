# WAB(웹텍) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 187. 철도 장비·서비스 — 화물(기관차·부품·디지털), 여객(Transit).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-21 장중 접수 → 기준일 10/22), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 보도자료는 장 전, 8:30 콜), StockAnalysis. 사전 조사 자료표 scratchpad pre/WAB.md.
# 엔진 입력(2026-10-23): 현금 = 제한 현금 포함 $489M(EV_TAGS — 기본 태그 2022 멈춤), 차입금 = 1년 안 1,714 + 장기 4,665 = $6,379M(엔진 값 = 원문), 4분기 EPS 2022·2023·2024 보도자료 값.
# 인수(10-Q, 8-K 없음): Evident Inspection Technologies 약 $1.8B(2025-07), Frauscher(2025-12), Dellner Couplers 약 $1.05B(2026-02) — 매출 증가에 인수분이 섞인다. 10/1 $2B 기업어음 프로그램.
CIK = '0000943452'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Wabtec'
S_ = 'https://www.sec.gov/Archives/edgar/data/943452/'
SEC = S_
TENQ = S_ + '000162828026066629/wab-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000094345226000017/a3q26pressreleaseword.htm', 'q2': S_ + '000162828026049105/a2q26pressreleaseword.htm',
      'q1': S_ + '000162828026026384/a1q26pressreleaseword.htm', 'q4': S_ + '000162828026007113/a4q2025pressrelease.htm'}
LINKS = {'tenq': S_ + '000162828026066629/wab-20260930.htm'}
FAIRBAND_TITLE = 'id="wabFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('2025~2026년 세 건의 인수(검사 기술·철도 신호·연결기)로 매출 증가에 인수분이 섞여 있고, 인수 무형자산 상각 때문에 GAAP 이익이 회사가 발표하는 조정 이익보다 작다. '
              '현금흐름 내재가치가 낮은 주된 이유는 최근 4분기 인수 대금 약 $1.8B를 성장에 든 재투자로 넣어 자본 효율(매출/투하자본)이 낮게 잡히고, 자본수익률이 할인율보다 낮아 성장이 가치를 더하지 못하기 때문이다. '
              '인수 전후가 섞인 평균 효율을 앞으로의 투자에 그대로 적용한 결과이고, \'어떤 성장률로도 닿지 않는다\'는 이 모델의 이익률·자본 효율 가정 안에서의 말이다. '
              '1년 안에 갚을 차입금이 크다. 10월에 만든 $2B 기업어음 프로그램은 기존 신용 한도가 뒷받침해 전체 차입 한도를 늘리지 않으며, 실제 차환은 따로 이뤄져야 한다.')
PH = ['CAT', 'DE', 'CMI', 'PCAR', 'ETN', 'PH']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '기계·장비 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(WAB 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·기계·운송·건설이 섞여 있다. 차트에는 기계·장비 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 외부 매출) — 화물 2,237 + 여객 883 = 3,120(= 총매출). 1년 전 2,093·793.
SEG = [('화물(Freight)', 2237.0, '#c8102e'), ('여객(Transit)', 883.0, '#e06a7b')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다). 반응일: 보도자료 장 전(8:30 콜), 8-K는 장중 접수 → 같은 날.
# 넣지 않은 8-K: 투자자 자료(3/3), 주총(5/15), 기업어음 프로그램(10/1). Dellner 인수(2/10, 8-K 없음 — 10-Q 주석, Fable·Codex r1 권장) 추가. 연간 조정 EPS 전망 상향은 가이던스라 쓰지 않는다.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 21일 — Q3 2026 실적', '2026-10-21',
     '매출 $3.12B(1년 전 $2.89B) · 순이익 $409M · 희석 EPS $2.42(1년 전 $1.81)', 'q3', 'Wabtec 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 22일 — Q2 2026 실적', '2026-07-22',
     '매출 $3.18B · 순이익 $395M · 희석 EPS $2.33(1년 전 $1.96)', 'q2', 'Wabtec 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 22일 — Q1 2026 실적', '2026-04-22',
     '매출 $2.95B · 순이익 $362M · 희석 EPS $2.12(1년 전 $1.88)', 'q1', 'Wabtec 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 11일 — Q4 2025 실적', '2026-02-11',
     '매출 $2.97B · 순이익 $202M · 희석 EPS $1.18(1년 전 $1.23) — 구조조정 비용 세후 $61M(EPS $0.36) 포함', 'q4', 'Wabtec 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 10일 — 철도 연결기 회사 Dellner Couplers 인수 완료', '2026-02-10',
     '약 $1.05B — 2025년 7월 Evident 검사 기술(약 $1.8B), 12월 Frauscher(철도 신호)에 이은 세 번째 인수(별도 8-K 없음, 10-Q 인수 주석)', 'tenq', 'Wabtec Q3 2026 10-Q (SEC)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 12, 'nt': 6, 'mean': 331, 'median': 332, 'low': 315, 'high': 355, 'sb': 9, 'b': 1, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 부문 2개(수동 지도). 원문 대조: Q3 2026 2,237/883(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"wab:FreightSegmentMember": ["화물(Freight)", "#c8102e"], "wab:TransitSegmentMember": ["여객(Transit)", "#e06a7b"]},
 "ignore": []
}
