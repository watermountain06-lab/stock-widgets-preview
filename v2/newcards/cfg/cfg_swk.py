CIK = '0000093556'
# SWK(스탠리 블랙앤데커) v2 카드 설정 — 자동 카드(AUTO), 정식 판정. 회계연도 12월 말 무렵 토요일(52/53주 — FY2025 53주). 공구·실외 장비(DeWalt·Craftsman·Stanley), 산업용 체결 부품(Engineered Fastening).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-04 접수, 카드 기준일 11-17 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 06~07시 동부 → 그날), CAM 매각 완료(8-K 7.01항 2026-04-06), Excel(HUSTLER) 매각 계약(8-K 7.01항 2026-09-04).
# 엔진 입력(2026-11-18): 영업이익 = 세전이익 + 이자비용 − 이자수익(DERIVED_OPINC — OperatingIncomeLoss 태그 2024-09에 멈춤) = 손익계산서 "Income from operations"(Q3 2026 $415.1M). 사업 매각 손익·손상·구조조정은 회사 줄처럼 영업 안.
# 일회성(E54 30% 규칙, 2026-11-18): 최근 4분기 GAAP 희석 EPS 5.59(1.04 + 0.39 + 2.33 + 1.83) 대 회사 조정 6.09(1.41 + 0.80 + 1.57 + 2.31).
#   회사 조정(세후 주당 순액): Q4 2025 +0.37, Q1 +0.41, Q2 −0.76(사업 매각 순이익 세전 $273.7M − 같은 분기 비용 $52.4M, 세금 −$105.7M), Q3 +0.48 → 순액 0.50(약 9%).
#   Q2를 비용·이익으로 나누면(Fable·Codex r1, Q2 비용 세금 효과 0~23% 가정) 비용 약 1.53~1.61(27~29%), 이익 약 1.03~1.12(18~20%) → 비용만도 30% 아래라 정식(여유 1~3%포인트).
#   관세 환급(Q2 약 $0.17, Q3 약 $0.67, 비용·세금 뺀 순액)은 회사가 조정하지 않아 회사 분류를 따른다 — 넣으면 이익 쪽 약 34~35%지만 순액(약 6%)·비용만(27~29%)은 30% 아래.
CUR, YO, QO = '2026-10-03', '2025-09-27', '2026-07-04'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2026-01-03', '2024-12-28'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'Stanley Black & Decker'
S_ = 'https://www.sec.gov/Archives/edgar/data/93556/'
SEC = S_
TENQ = S_ + '000009355626000039/swk-20261003.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000009355626000036/ex991q32026.htm', 'q2': S_ + '000009355626000028/ex991q22026.htm',
      'q1': S_ + '000009355626000013/ex991q12026.htm', 'q4': S_ + '000009355626000004/ex991q42025.htm',
      'cam': S_ + '000119312526142966/d97341d8k.htm', 'excel': S_ + '000119312526383511/d493257d8k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="swkFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (-10, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 GAAP 희석 EPS $5.59와 회사 조정 EPS $6.09는 크게 다르지 않지만, 그 안에서 큰 비용과 큰 이익이 상쇄됐다 — 구조조정·손상·공장 폐쇄 가속감가상각 등 회사가 조정에서 빼는 비용이 세후 주당 약 $1.5~1.6(GAAP EPS의 약 27~29% — 회사가 분기 순액만 내서 추정 범위), 2026년 2분기 항공 체결 부품 사업(CAM) 매각 이익이 약 $1.0~1.1(약 18~20%)이다. 순액은 약 9%이고 비용 쪽도 30% 아래라 GAAP 숫자를 그대로 쓴다. '
              '2026년 2·3분기 이익에는 관세 환급도 크게 들어 있다(관련 비용·세금 뺀 순액 주당 약 $0.17·$0.67, 3분기 매출총이익률 약 4.3%포인트 — 더 들어올지는 불확실) — 회사는 조정 EPS에도 넣었다. 이것까지 일회성 이익으로 보면 이익 쪽이 약 34~35%로 커지지만 순액과 비용 쪽은 30% 아래다. 3분기 실적 때 올린 연간 EPS 전망 폭도 환급 효과와 비슷하다. '
              '현금흐름 기본 시나리오는 최근 2년 중앙 이익률(2025년 손상·관세 부담 포함)에서 출발해 이 가정에서 0 이하로 나온다 — 회사 가치가 없다는 뜻이 아니라 그 이익률로는 차입금 약 $4.7B를 넘지 못한다는 뜻이다. 최근 4분기 영업이익률을 쓰는 낙관 시나리오만 양수인데, 그 이익률에는 CAM 등 사업 매각 순이익(약 1.6%포인트)과 관세 환급(약 1.1%포인트)이 들어 있어 빼면 약 6.7%다. 최근 4분기 FCF($1.7B)도 작년 4분기($883M)와 관세 환급이 들어 있어 회사의 2026년 FCF 전망($1.0~1.2B)보다 크다. '
              'CAM을 4월 6일 Howmet에 약 $1.8B 현금에 팔았고(회사 발표 순수령 약 $1.6B) — 그래서 체결 부품 매출이 1년 전보다 21% 줄었다(매각·환율 영향을 뺀 유기적 성장은 +2%, 회사 전체 유기적 성장은 3분기 +4%). 9월에는 잔디깎이 사업 Excel Industries(HUSTLER)를 Bad Boy Mowers에 팔기로 했다. 3분기에 자사주 $250M을 사 기존 한도를 다 썼고 10월 29일 $1B 새 한도를 승인했다. 회사는 2026년 GAAP EPS 전망을 $5.45~5.85로 올렸다. '
              '손익계산서에 영업이익 태그가 2024년 뒤로 없어 카드는 세전이익에 순이자비용을 더해 영업이익으로 쓴다(회사 "Income from operations"와 같다).')
PH = ['SNA', 'ITW', 'DOV', 'PNR', 'IR', 'EMR']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '공구·산업 기계 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(SWK 제외)와 배수 순위를 매긴 값이다.',
            '항공·방산·운송·기계·건설이 섞여 있다. 차트에는 공구·산업 기계 6곳만 보인다.')
# 매출(Q3 2026 보도자료 부문): 공구·실외 3,336.1 + 산업용 체결 부품 395.5 = 3,731.6(CAM 매각 뒤 — 1년 전 체결 부품 500.5에는 CAM 포함).
SEG = [('공구·실외 장비(DeWalt·Craftsman·Stanley)', 3336.1, '#1a1a1a'), ('산업용 체결 부품', 395.5, '#ffcc00')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 사업 부문별'
# 손 뉴스: 실적 4건 + CAM 매각 완료 + Excel 매각 계약. 반응일: 모두 장 전 → 그날(CAM 완료 8-K 12:59 UTC = 08:59 동부, Excel 8-K 19:02 UTC = 15:02 동부 장중 → 그날).
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('green', '2026년 11월 4일 장 전 — Q3 2026 실적', '2026-11-04',
     'GAAP 희석 EPS $1.83(관세 환급 약 $0.67 포함) · 조정 EPS $2.31 · 매출총이익률 39.0% · 자사주 $250M, 새 한도 $1B · 연간 GAAP EPS 전망 $5.45~5.85로 상향 — 그날 주가 +13.1%', 'q3', 'Stanley Black & Decker 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 9월 4일 — Excel Industries(HUSTLER) 매각 계약', '2026-09-04',
     '잔디깎이 회사 Excel Industries와 HUSTLER 브랜드 자산을 Bad Boy Mowers에 팔기로(규제 승인 필요) — 그날 주가 +0.9%', 'excel', 'Stanley Black & Decker 8-K'),
    ('neutral', '2026년 7월 29일 장 전 — Q2 2026 실적', '2026-07-29',
     'GAAP 희석 EPS $2.33(CAM 매각 이익·관세 환급 약 $0.17 포함) · 조정 EPS $1.57 · 연간 전망 상향 — 그날 주가 −1.2%', 'q2', 'Stanley Black & Decker 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 29일 장 전 — Q1 2026 실적', '2026-04-29',
     '매출 $3.8B(+3%) · GAAP 희석 EPS $0.39 · 조정 EPS $0.80 — 그날 주가 −3.1%', 'q1', 'Stanley Black & Decker 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 6일 장 전 — CAM 매각 완료', '2026-04-06',
     '항공 체결 부품 사업 Consolidated Aerospace Manufacturing을 Howmet Aerospace에 약 $1.8B 현금에 매각 완료 — 그날 주가 −1.0%', 'cam', 'Stanley Black & Decker 8-K'),
    ('green', '2026년 2월 4일 장 전 — 2025년 연간 실적', '2026-02-04',
     '4분기 GAAP 희석 EPS $1.04 · 조정 EPS $1.41 · 4분기 FCF $883M(연간 $688M) · CAM 매각 계약($1.8B) 발표 뒤 첫 실적 — 그날 주가 +4.5%', 'q4', 'Stanley Black & Decker 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 15, 'nt': 8, 'mean': 111.38, 'median': 115, 'low': 96, 'high': 140, 'sb': 3, 'b': 0, 'h': 12, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-22'

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"swk:ToolsAndOutdoorSegmentMember": ["공구·실외 장비(DeWalt·Craftsman·Stanley)", "#1a1a1a"], "swk:EngineeredFasteningSegmentMember": ["산업용 체결 부품", "#ffcc00"]},
 "ignore": []
}
