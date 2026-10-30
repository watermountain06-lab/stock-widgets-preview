# CF(CF 인더스트리) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 질소 비료(암모니아·요소·UAN·질산암모늄) — 북미·영국 공장, 저탄소 암모니아(Blue Point 합작 40%).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-06), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/CF.md.
# 엔진 입력(2026-10-25): 차입금 $3,216M(전부 장기), 현금 = 제한 현금 포함 줄 $2,480M(EV_TAGS cash — 기본 태그 2019 멈춤), 비지배지분 $3,172M(CF Nitrogen 합작 CHS 지분 등), 순이익 = 보통주 귀속 태그(EV_TAGS 대체).
# 일회성: Q1 2026 Orica 소송 합의 이익 세전 $170M·보험금 $25M, Q2 2026 영업중단 보험금 $50M — 합계 세전 $245M(최근 4분기 EPS의 약 9%).
CIK = '0001324404'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, 1), '적정~저평가'
CO = 'CF Industries'
S_ = 'https://www.sec.gov/Archives/edgar/data/1324404/'
SEC = S_
TENQ = S_ + '000132440426000019/cf-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000132440426000017/cf-08052026_ex991xearnings.htm', 'q1': S_ + '000132440426000011/cf-05062026_ex991xearnings.htm',
      'q4': S_ + '000132440426000003/cf-02182026_ex991xearnings.htm', 'q3': S_ + '000132440425000028/cf-11052025_ex991xearnings.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="cfFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 50)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('비료 가격과 천연가스 가격 차이로 이익이 크게 오르내린다 — 2022년 가스 대란 때 이익이 최고였고 5년 이력에 그 고점이 섞여 있다. 2026년 상반기 이익은 1년 전의 두 배다. '
              '최근 4분기 영업이익에는 소송 합의·보험금(세전 $245M, Q2 자산 손상 $23M과 함께)이 들어 있다 — 빼면 영업이익률이 약 3%포인트 낮아지고 현금흐름 기본 약 $163(비율 0.74)이 되지만 동종업 점수는 그대로라 세 표는 같다. '
              '현금흐름 시나리오는 이력 기반이라 사이클 고점의 높은 이익률에서 출발한다(정상화 가치가 아니다). 비지배지분($3.2B — CHS의 CF Nitrogen 지분 등)은 EV에 더하고 주주 몫 가치에서 뺀다.')
PH = ['MOS', 'NUE', 'DOW', 'LYB', 'APD', 'LIN']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '화학·비료 등 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(CF 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·건자재·포장재가 섞여 있다. 차트에는 화학·비료 등 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 요소 759 + UAN 613 + 암모니아 586 + 기타 193 + 질산암모늄 71 = 2,222. 기타는 OtherProductsMember만(AllOtherSegmentsMember와 같은 값 중복 태그).
SEG = [('요소', 759, '#00843d'), ('UAN(액체 비료)', 613, '#6cbf84'), ('암모니아', 586, '#1d3c6e'), ('기타 제품', 193, '#a8b8d0'), ('질산암모늄', 71, '#c7e3cf')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 제품별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표(16:42~16:50 동부 접수) → 다음 거래일. 넣지 않은 8-K: 임원 교체, 신용 한도, 사채, Blue Point 옵션, Orica 합의(3/16 — Q1 실적 항목), 주총.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 5일 장 마감 뒤 — Q2 2026 실적', '2026-08-06',
     '매출 $2.22B(+18%) · 지배주주 순이익 $727M · 희석 EPS $4.73(1년 전 $2.37) — 영업중단 보험금 세전 $50M 포함', 'q2', 'CF Industries 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 6일 장 마감 뒤 — Q1 2026 실적', '2026-05-07',
     '매출 $1.99B · 지배주주 순이익 $615M · 희석 EPS $3.98(1년 전 $1.85) — Orica 소송 합의 이익 세전 $170M 포함', 'q1', 'CF Industries 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 18일 장 마감 뒤 — Q4 2025 실적', '2026-02-19',
     '매출 $1.87B · 지배주주 순이익 $404M · 희석 EPS $2.59(1년 전 $1.89) · 2025년 EPS $8.97', 'q4', 'CF Industries 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 5일 장 마감 뒤 — Q3 2025 실적', '2025-11-06',
     '매출 $1.66B · 지배주주 순이익 $353M · 희석 EPS $2.19(1년 전 $1.55)', 'q3', 'CF Industries 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 22, 'nt': 15, 'mean': 126.73, 'median': 123, 'low': 110, 'high': 162, 'sb': 3, 'b': 3, 'h': 13, 's': 1, 'ss': 2}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 제품 부문 5개(수동 지도, 기타는 OtherProductsMember만). 원문 대조: Q2 2026 759/613/586/193/71(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"cf:UreaMember": ["요소", "#00843d"], "cf:UANMember": ["UAN(액체 비료)", "#6cbf84"], "cf:AmmoniaMember": ["암모니아", "#1d3c6e"],
             "cf:OtherProductsMember": ["기타 제품", "#a8b8d0"], "cf:AmmoniumNitrateSegmentMember": ["질산암모늄", "#c7e3cf"]},
 "ignore": ["us-gaap:AllOtherSegmentsMember"]
}
