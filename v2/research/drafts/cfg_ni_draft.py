# NI(나이소스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 6개 주 천연가스 배전(Columbia Gas)과 인디애나 전력·가스(NIPSCO, 소수 지분 19.9%는 외부 투자자).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-05), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/NI.md.
# 엔진 입력(2026-10-25): 차입금 = 단기 $692.0M + 1년 안 $1,098.4M + 장기 $15,612.6M(DEBT_TOTAL_TAG), 현금 $70M, 비지배지분 $2,319.8M(NIPSCO 소수 지분).
# 세전이익 = IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic(PRETAX_TAG_BY_CIK — 표준 세전 태그 없음). 매출 태그가 2024-09 뒤 Revenues → 고객 계약 매출로 바뀌어(대체 수익 분기 약 $40~60M 빠짐) 이력이 약간 끊긴다.
CIK = '0001111711'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'NiSource'
S_ = 'https://www.sec.gov/Archives/edgar/data/1111711/'
SEC = S_
TENQ = S_ + '000111171126000088/nix-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000111171126000087/ni-ex991_20260630.htm', 'q1': S_ + '000111171126000044/ni-ex991_20260331.htm',
      'q4': S_ + '000111171126000026/ni-ex991_20251231.htm', 'q3': S_ + '000111171125000054/ni-ex991_20250930.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="niFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('가스관·송배전망·발전 설비투자가 감가상각보다 훨씬 커서 큰 차입금을 뺀 현금흐름 모델의 값이 낮게 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '난방 수요 때문에 1분기 이익이 가장 크고 2·3분기는 작다. NIPSCO 지분 19.9%는 외부 투자자 몫(비지배지분)이고, 신주(ATM)로 투자 자금을 조달해 주식 수가 늘고 있다.')
HEALTH_EXTRA = '설비투자 자금을 사채·하이브리드 채권·신주로 조달하는 구조라 차입금 비중이 높게 나온다 — 규제 유틸리티에서는 흔한 모습이다.'
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
h = _re.sub(r'(id="niDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="niDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'SO', 'DUK', 'AEE', 'ATO', 'CMS']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(NI 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 고객 계약 매출) — NIPSCO 704.7 + Columbia 584.8 = 1,289.5.
SEG = [('NIPSCO(인디애나 전력·가스)', 704.7, '#00467f'), ('Columbia(가스 배전)', 584.8, '#4f8fc6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q2 2026, 고객 계약 매출)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:35~06:39 동부 접수) → 같은 날. 넣지 않은 8-K: 데이터센터 전력 계약(2025-09), ATM, 사채·하이브리드 채권 발행, 신용 한도, 배터리 저장 계약(10/16), 주총.
NEWS_RANGE = '2025.10 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 5일 — Q2 2026 실적', '2026-08-05',
     '매출 $1.29B · 순이익 $46M · 희석 EPS $0.09(1년 전 $0.22) — 업무 연속성 비용 $21.4M·날씨 영향 포함(세전)', 'q2', 'NiSource 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 6일 — Q1 2026 실적', '2026-05-06',
     '매출 $2.32B · 순이익 $511M · 희석 EPS $1.06(1년 전 $1.00)', 'q1', 'NiSource 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 11일 — Q4 2025 실적', '2026-02-11',
     '순이익 $258M · 희석 EPS $0.53(1년 전 $0.47) · 2025년 EPS $1.95', 'q4', 'NiSource 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 29일 — Q3 2025 실적', '2025-10-29',
     '매출 $1.24B · 순이익 $95M · 희석 EPS $0.20(1년 전 $0.19)', 'q3', 'NiSource 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 17, 'nt': 15, 'mean': 48.43, 'median': 49, 'low': 43, 'high': 52, 'sb': 10, 'b': 3, 'h': 4, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 2개(수동 지도, 고객 계약 매출). 원문 대조: Q2 2026 704.7/584.8(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"nix:NIPSCOOperationsMember": ["NIPSCO(인디애나 전력·가스)", "#00467f"], "nix:ColumbiaOperationsMember": ["Columbia(가스 배전)", "#4f8fc6"]},
 "ignore": []
}
