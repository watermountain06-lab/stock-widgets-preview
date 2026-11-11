# AEE(에이머런) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 미주리(Union Electric)·일리노이 전력·가스 배전, 송전.
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-03), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/AEE.md.
# 엔진 입력(2026-10-25): 차입금 = 단기 $1,220M + 1년 안 $1,524M + 장기 $19,064M = $21,808M(DEBT_TOTAL_TAG). 순이익 = 보통주 귀속(NI_TAGS — NetIncomeLoss 태그는 2017년에 멈춤).
# 일회성: 이월결손금 관련 세금 이익(Q3 2025 $0.18, Q4 2025 $0.14) — 최근 4분기 EPS 5.68의 약 6%.
NI_TAGS = ['NetIncomeLossAvailableToCommonStockholdersBasic', 'ProfitLoss']
CIK = '0001002910'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Ameren'
S_ = 'https://www.sec.gov/Archives/edgar/data/1002910/'
SEC = S_
TENQ = S_ + '000100291026000023/aee-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000100291026000020/q22026ex991earningsrelease.htm', 'q1': S_ + '000100291026000013/q12026ex991earningsrelease.htm',
      'q4': S_ + '000100291026000005/q42025ex991earningsrelease.htm', 'q3': S_ + '000100291025000127/q32025ex991earningsrelease.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="aeeFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 35)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('송배전 설비투자가 감가상각보다 훨씬 커서 큰 차입금을 뺀 현금흐름 모델의 값이 낮게 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '최근 4분기 GAAP 이익에는 이월결손금 관련 세금 이익(일회성)이 조금 들어 있다. 신주 발행(ATM)과 후순위 사채로 자금을 조달한다.')
HEALTH_EXTRA = '설비투자 자금을 사채·신주로 조달하는 구조라 차입금 비중이 높게 나온다 — 규제 유틸리티에서는 흔한 모습이다.'
# 현금흐름 0 이하 — SO와 같은 문구 보정(0 이하가 아니면 바뀌지 않는다)
POST = [r'''
_R = '현금흐름 모델의 주당 지분가치가 0 이하라(큰 차입금을 뺀 뒤) 기본 시나리오 환산 성장률은 해석할 수 없다.'
_pairs = [
 ("fill('[data-dcf-basev]', '$' + (Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base)));",
  "fill('[data-dcf-basev]', '$' + (Math.abs(D.base) < 10 ? D.base.toFixed(2) : Math.round(D.base)));\n  if (D.base <= 0) { const _rv = document.querySelector('#dcf .reverse'); if (_rv) _rv.textContent = _XR; }"),
 ("const tv = D.tvShare != null ? `잔존가치(5년 뒤)가 내재가치의 ${Math.round(D.tvShare * 100)}%` : '';",
  "const tv = D.base <= 0 ? '잔존가치 비중 — 내재가치가 0 이하라 의미 없음' : (D.tvShare != null ? `잔존가치(5년 뒤)가 내재가치의 ${Math.round(D.tvShare * 100)}%` : '');"),
 ("`현재가 $${price.toFixed(2)} 가 정당화되려면 5년 내내`\n          + ` 연 ${(d.requiredGrowth*100).toFixed(1)}% 매출 성장이 필요하다.`)",
  "(d.base <= 0 ? _XR : `현재가 $${price.toFixed(2)} 가 정당화되려면 5년 내내`\n          + ` 연 ${(d.requiredGrowth*100).toFixed(1)}% 매출 성장이 필요하다.`))"),
]
for _x, _y in _pairs:
    if _x in h:
        h = h.replace(_x, _y)
if 'const _XR' not in h:
    h = h.replace('<script>', '<script>\nconst _XR = ' + repr(_R) + ';', 1)
import re as _re
h = _re.sub(r'잔존가치\(5년 뒤\)가 내재가치의 [0-9,]+%', '잔존가치 비중 — 내재가치가 0 이하라 의미 없음', h)
h = _re.sub(r'(id="aeeDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="aeeDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'SO', 'DUK', 'ED', 'XEL', 'PEG']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(AEE 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 외부 고객 계약 매출) — 미주리 1,111 + 일리노이 전력 629 + 일리노이 가스 176 + 송전 176 = 2,092.
SEG = [('미주리(Union Electric)', 1111.0, '#0a5c8a'), ('일리노이 전력', 629.0, '#5fa3cc'), ('일리노이 가스', 176.0, '#a7cde4'), ('송전', 176.0, '#d8a23a')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 조정 EPS·가이던스는 쓰지 않는다). 반응일: 장 마감 뒤 발표 → 다음 거래일.
# 넣지 않은 8-K: 사채·신주(ATM)·후순위 사채, 임원·이사, 요금 청구(6/26 미주리 +$343M 요청 — 실적 줄에), IRP.
NEWS_RANGE = '2025.11 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 30일 — Q2 2026 실적', '2026-07-31',
     '매출 $2.09B(1년 전 $2.22B) · 순이익 $314M · 희석 EPS $1.13(1년 전 $1.01) · 6/26 미주리 전력 요금 인상 청구(연 $343M)', 'q2', 'Ameren 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 5일 — Q1 2026 실적', '2026-05-06',
     '매출 $2.18B · 순이익 $357M · 희석 EPS $1.28(1년 전 $1.07)', 'q1', 'Ameren 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 11일 — Q4 2025 실적', '2026-02-12',
     '순이익 $252M · 희석 EPS $0.92(1년 전 $0.77) — 세금 이익 $0.14 포함 · 2025년 희석 EPS $5.35', 'q4', 'Ameren 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 5일 — Q3 2025 실적', '2025-11-06',
     '매출 $2.70B · 순이익 $640M · 희석 EPS $2.35(1년 전 $1.70) — 세금 이익 $0.18 포함', 'q3', 'Ameren 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 19, 'nt': 14, 'mean': 115.58, 'median': 115, 'low': 104, 'high': 137, 'sb': 10, 'b': 1, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 4개(수동 지도). 원문 대조: Q2 2026 1,111/629/176/176(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax", "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"aee:UnionElectricCompanyMember": ["미주리(Union Electric)", "#0a5c8a"], "aee:AmerenIllinoisElectricDistributionSegmentMember": ["일리노이 전력", "#5fa3cc"],
             "aee:AmerenIllinoisGasSegmentMember": ["일리노이 가스", "#a7cde4"], "aee:AmerenTransmissionSegmentMember": ["송전", "#d8a23a"]},
 "ignore": ["aee:AmerenIllinoisTransmissionSegmentMember"]
}
