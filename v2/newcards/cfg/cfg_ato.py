# ATO(애트모스 에너지) v2 카드 설정 — 자동 카드(AUTO). 회계연도 9월 30일(FY2026 = 2025-10~2026-09). 천연가스 배전(텍사스 등 8개 주), 텍사스 파이프라인·저장.
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-08-05), 실적 보도자료(Q4 FY25~Q3 FY26, 8-K 2.02항 — 장 마감 뒤 발표 → 다음 거래일 반응), StockAnalysis. 사전 조사 scratchpad pre/ATO.md.
# 엔진 입력(2026-10-25): 차입금 = 1년 안 $502.5M + 장기 $9,748.7M(DEBT_TOTAL_TAG), 현금 $521M. 일회성 없음. 겨울 난방 수요로 회계 2분기(1~3월) 이익이 가장 크다.
CIK = '0000731802'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-09-30', '2024-09-30'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Atmos Energy'
S_ = 'https://www.sec.gov/Archives/edgar/data/731802/'
SEC = S_
TENQ = S_ + '000073180226000102/ato-20260630.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000073180226000100/ato20260805exhibit991.htm', 'q2': S_ + '000073180226000086/ato20260506exhibit991.htm',
      'q1': S_ + '000073180226000011/ato20260203exhibit991.htm', 'q4': S_ + '000073180225000053/ato20251105exhibit991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="atoFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 50)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('가스관 교체·확장 설비투자가 감가상각보다 훨씬 커서 큰 차입금을 뺀 현금흐름 모델의 값이 낮게 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '난방 수요 때문에 회계 2분기(1~3월) 이익이 가장 크고 4분기(7~9월)가 가장 작다. 사채·신주로 투자 자금을 조달한다. '
              '연결 자회사(AEK)의 비소구 유동화 차입금은 회사 고유 태그라 차입금에 넣지 않았다(전체 차입금의 1% 미만).')
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
h = _re.sub(r'(id="atoDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="atoDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'SO', 'DUK', 'ED', 'AEE', 'XEL']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(ATO 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
SEG = [('가스 배전', 773.9, '#0067b1'), ('파이프라인·저장', 105.2, '#5ea3d8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q3 FY26, 외부 매출)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 마감 뒤 발표 → 다음 거래일. 넣지 않은 8-K: 사채 발행·신용 한도·주총·이사 선임.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 5일 — Q3 FY26 실적', '2026-08-06',
     '매출 $879M(1년 전 $839M) · 순이익 $243M · 희석 EPS $1.43(1년 전 $1.16) · 9개월 누계 EPS $7.33', 'q3', 'Atmos Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 6일 — Q2 FY26 실적', '2026-05-07',
     '매출 $1.96B · 순이익 $582M · 희석 EPS $3.47(1년 전 $3.03) — 연간 EPS 전망 상향', 'q2', 'Atmos Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 3일 — Q1 FY26 실적', '2026-02-04',
     '매출 $1.34B · 순이익 $403M · 희석 EPS $2.44(1년 전 $2.23)', 'q1', 'Atmos Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 5일 — FY2025 실적', '2025-11-06',
     'FY2025 희석 EPS $7.46 — 4분기(7~9월)만 보면 약 $1.06(연간 − 9개월)', 'q4', 'Atmos Energy 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 14, 'nt': 11, 'mean': 186.18, 'median': 184, 'low': 167, 'high': 206, 'sb': 2, 'b': 0, 'h': 12, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-25'


# ── 자동 카드 — 부문 2개(수동 지도, 외부 매출). 원문 대조: Q3 FY26 773.9/105.2(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"ato:DistributionSegmentMember": ["가스 배전", "#0067b1"], "ato:PipelineandStorageSegmentMember": ["파이프라인·저장", "#5ea3d8"]},
 "ignore": []
}
