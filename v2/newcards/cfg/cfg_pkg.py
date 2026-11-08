CIK = '0000075677'
# PKG(패키징 코퍼레이션 오브 아메리카) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 골판지 원지(containerboard) 공장 + 골판지 상자 공장(Packaging 부문), 백상지(Paper 부문).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-05 12:07 동부 장중 접수 → 첫 세션 11-05, 카드 기준일 11-06 종가), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 모두 장 마감 뒤 → 다음 거래일),
#        Wallula 구조조정 8-K(2025-12-04, 2.05·2.06항).
# 엔진 입력(2026-11-07): 현금 $534.6M + 단기 유가증권 $150.3M, 장기차입 $3,969.7M(Greif 인수 차입 포함), 리스 $437M, 자본 $4,805M. 감가상각은 합산 태그가 2015~2023에 비어
#   구성요소(Depreciation + AmortizationOfIntangibleAssets) 경로(build_multiple_history DDA_PARTS_BY_CIK — 이것 없이는 EV/EBITDA 이력 252일).
# 일회성(E54): 최근 4분기 특별항목 주당 $1.99(Q4 2025 1.19·Q1 0.49·Q2 0.20·Q3 0.11) = GAAP EPS 8.12의 약 24.5%. 내용은 Wallula 공장 구조조정($205M 예상 — 손상·가속상각 $165M + 현금 $40M),
#   골판지 상자 공장 폐쇄, Greif 인수·통합 비용(E54 범주 밖), 공장 화재. 회사 표는 Wallula와 공장 폐쇄를 다른 줄로 적지만 E54 범주로는 둘 다 restructuring(공장 폐쇄·감원·사업 퇴출) —
#   8분기(Q4 2024~Q3 2026) 8/8에 있다(Q2 2025는 폐쇄 공장 부동산 매각 이익(divestiture)과 폐쇄비용이 상계된 순이익 −0.19). E54 반복 기준(있는 분기 ≥ 6)으로 빼지 않는다 — GAAP 그대로 + 문장(JBL 선례).
#   견고성(Codex·Fable r1): Wallula만 빼면(TTM $1.56) EPS 9.68·PER 25.8배, 특별항목 전부 빼면 10.11·24.7배 — 자기 이력 점수 약 15로 −1 유지, 영업이익률을 올려도 현금흐름 약 1.95배로 −2 유지. Wallula 가속상각은 영업이익 안이라 현금흐름 이익률(11.2%)도 그만큼 낮다(A-2 결정 전 영업이익 조정 없음).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'Packaging Corporation of America'
S_ = 'https://www.sec.gov/Archives/edgar/data/75677/'
SEC = S_
TENQ = S_ + '000119312526449161/pkg-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000119312526428056/pkg-ex99_1.htm', 'q2': S_ + '000119312526312651/pkg-ex99_1.htm',
      'q1': S_ + '000119312526171009/pkg-ex99_1.htm', 'q4': S_ + '000119312526025053/pkg-ex99_1.htm',
      'wallula': S_ + '000119312525307535/d50663d8k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="pkgFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('최근 4분기 GAAP 이익에는 회사가 따로 빼는 특별항목이 주당 약 $2 들어 있다 — 대부분 Wallula 원지 공장 2호기·크라프트 펄프 설비 폐쇄(2026년 1분기 완료, 세전 약 $188M — 설비 손상·가속상각이 대부분)와 골판지 상자 공장 폐쇄 비용이고, 인수 비용·공장 화재도 조금 있다. '
              '공장 폐쇄·구조조정 비용은 최근 2년 매 분기 있어 일회성으로 빼지 않고 GAAP 그대로 쓴다(특별항목을 모두 빼면 최근 4분기 EPS가 약 25% 높아지지만 세 칸의 판정은 같다). 가속상각이 영업이익 안이라 현금흐름 모델의 현재 이익률도 그만큼 낮게 잡힌다. '
              '2025년 3분기 Greif 원지 사업 인수(현금 약 $1.8B, 차입으로 조달)로 매출과 차입금이 늘었다. 원지·골판지 가격에 따라 이익이 크게 오르내리는 경기 업종이다.')
PH = ['IP', 'SW', 'AMCR', 'BALL', 'AVY', 'CRH']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '포장재 등 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(PKG 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·건자재·포장재가 섞여 있다. 차트에는 포장재 등 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 — 부문 축만 붙은 값): Packaging 2,414.0 + Paper 163.2 + Corporate and Other 24.5 = 연결 2,601.7(1년 전 2,128.1 + 161.2 + 24.1 = 2,313.4).
SEG = [('포장(원지·골판지 상자)', 2414.0, '#00563f'), ('제지(백상지)', 163.2, '#8fc9a6'), ('본사·기타', 24.5, '#c9c9c9')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 3건 + Wallula 구조조정(GAAP 희석 EPS, 특별항목 제외 EPS). 최신 Q3 2026(10-21 장 마감 뒤)은 news_auto가 붙인다. 반응일: 장 마감 뒤 → 다음 거래일.
NEWS_RANGE = '2025.12 ~ 2026.10'
NEWS = [
    ('green', '2026년 7월 22일 장 마감 뒤 — Q2 2026 실적', '2026-07-23',
     '매출 $2.49B(+14.7%) · 순이익 $192M · 희석 EPS $2.15(1년 전 $2.67) · 특별항목 제외 $2.35 — 다음 날 주가 +2.5%', 'q2', 'PCA 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 22일 장 마감 뒤 — Q1 2026 실적', '2026-04-23',
     '매출 $2.37B(+10.6%) · 순이익 $171M · 희석 EPS $1.91(1년 전 $2.26) · 특별항목 제외 $2.40 — 다음 날 주가 +4.8%', 'q1', 'PCA 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 27일 장 마감 뒤 — Q4 2025 실적', '2026-01-28',
     '매출 $2.36B(+10.1%) · 순이익 $102M · 희석 EPS $1.13(1년 전 $2.45) · 특별항목 제외 $2.32(Wallula 구조조정 등 $1.19) — 다음 날 주가 −2.7%', 'q4', 'PCA 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 3일 — Wallula 원지 공장 일부 폐쇄 발표', '2025-12-04',
     '2호기·크라프트 펄프 설비 영구 폐쇄(연 생산능력 25만 톤 축소, 약 200명 감원) · 세전 구조조정 비용 약 $205M(손상·가속상각 $165M + 현금 $40M) 대부분 2025년 4분기·2026년 1분기', 'wallula', 'PCA 공시 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 10, 'nt': 6, 'mean': 281, 'median': 289, 'low': 245, 'high': 322, 'sb': 6, 'b': 1, 'h': 2, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 지도(손 작성). 원문 대조: Q3 2026 10-Q 부문 축만 붙은 매출 2,414.0/163.2/24.5 = 연결 2,601.7, 1년 전 2,313.4(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"pkg:PackagingMember": ["포장(원지·골판지 상자)", "#00563f"], "pkg:PaperMember": ["제지(백상지)", "#8fc9a6"],
             "us-gaap:CorporateAndOtherMember": ["본사·기타", "#c9c9c9"]},
 "ignore": []
}
