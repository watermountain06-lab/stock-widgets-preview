# NI(나이소스) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 6개 주 천연가스 배전(Columbia Gas)과 인디애나 전력·가스(NIPSCO, 소수 지분 19.9%는 외부 투자자).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-28 06:38 동부 장 전 → 그날, 카드 기준일 11-06 종가), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 06:3x 동부 → 그날).
# 보류 목록 D군(안건 E54) — 30% 규칙: 최근 4분기 GAAP 희석 EPS 1.95(0.53 + 1.06 + 0.09 + 0.27) 대 회사 조정 EPS 2.00(0.51 + 1.06 + 0.16 + 0.27) — 차이 약 3%라 정식(2026-11-08).
# 엔진 입력(2026-10-25 등록, 2026-11-08 Q3 갱신): 차입금 = 단기 $692.0M + 1년 안 $1,098.4M + 장기 $15,612.6M(DEBT_TOTAL_TAG), 현금 $70M, 비지배지분 $2,319.8M(NIPSCO 소수 지분).
# 세전이익 = IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic(PRETAX_TAG_BY_CIK — 표준 세전 태그 없음). 매출 태그가 2024-09 뒤 Revenues → 고객 계약 매출로 바뀌어(대체 수익 분기 약 $40~60M 빠짐) 이력이 약간 끊긴다.
CIK = '0001111711'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'NiSource'
S_ = 'https://www.sec.gov/Archives/edgar/data/1111711/'
SEC = S_
TENQ = S_ + '000111171126000100/nix-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000111171126000099/ni-ex991_20260930.htm', 'q2': S_ + '000111171126000087/ni-ex991_20260630.htm',
      'q1': S_ + '000111171126000044/ni-ex991_20260331.htm', 'q4': S_ + '000111171126000026/ni-ex991_20251231.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="niFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('가스관·송배전망·발전 설비투자가 감가상각보다 훨씬 커서 큰 차입금을 뺀 현금흐름 모델의 값이 낮게 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '난방 수요 때문에 1분기 이익이 가장 크고 2·3분기는 작다. NIPSCO 지분 19.9%는 외부 투자자 몫(비지배지분)이고, 신주(ATM)로 투자 자금을 조달해 주식 수가 늘고 있다. '
              '최근 4분기 GAAP 희석 EPS($1.95)는 회사 조정 EPS($2.00)와 거의 같다 — 주요 차이는 2026년 4월 NIPSCO 노조 직장폐쇄 기간 대체 인력 비용($21.4M)과 구조조정 컨설팅·퇴직금 등 비용 절감 프로그램 비용, 날씨 보정이다. 자기 이력 점수가 판정 문턱(30) 바로 위라, 주가가 몇 % 오르거나 배수 하나가 조금 비싸져도 합계가 ‘고평가’로 바뀔 수 있다. 현금흐름 모델이 0 이하로 나오는 것은 규제기관이 허용하는 수익률(자기자본이익률 9.6~10%)이 이 모델의 할인율(10%)과 같거나 낮기 때문이라, 이 칸의 −2는 ‘비싸다’보다 ‘이 모델이 규제 유틸리티에 잘 맞지 않는다’에 가깝다. '
              'NIPSCO가 Amazon·Alphabet에 이어 10월 Microsoft와도 데이터센터 전력 계약을 맺었다(2028년부터 최대 788MW, 인디애나 규제위원회(IURC) 승인 대기) — 발전 설비는 자회사 GenCo가 짓고, 회사는 세 계약으로 기존 고객 절감 효과가 약 $1.75B라고 밝혔다. 회사는 2026년 조정 EPS를 $2.02~2.07 범위 위쪽으로 좁히고, 2027년 $2.22~2.30을 처음 제시했으며, 2027~2033년 조정 EPS 연평균 성장 목표를 10~11%로 올렸다(같은 기간 설비투자 $40.0B, 그중 데이터센터 $8.0B). 비지배지분은 NIPSCO와 GenCo 지주회사 각 19.9%(GenCo 몫은 2025년 10월 Blackstone)다. 7월 IURC가 인디애나 전력사의 허용 수익률·요금 조정 제도를 조사하기 시작했고, 8월 폭풍 정전 복구도 조사 중이다. '
              '지난 1년 하이브리드 채권 $1.75B·선순위채 $1.25B를 발행했고 신주 발행(ATM) 한도 $1.5B를 두고 있다 — 9개월 순이자비용이 33% 늘었다.')
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
# 현금흐름 0 이하일 때 마진 역산 문장(64.9% 등)이 '해석 부적합' 헤더와 부딪치지 않게(Codex·Fable r1, 2026-11-09)
POST.append(r"""
h = h.replace("if (D.reqMode === 'margin') document.querySelectorAll('#dcf .reverse')", "if (D.reqMode === 'margin' && D.base > 0) document.querySelectorAll('#dcf .reverse')", 1)
_c3 = h[h.index('<strong style="color:var(--accent2);">③</strong>'):]; _c3 = _c3[:_c3.index('</div>')]
h = h.replace(_c3, '<strong style="color:var(--accent2);">③</strong> 배당성향 — 연 배당 $1.20이 2026년 조정 EPS 전망($2.02~2.07)의 60% 안팎에 머무는지(설비투자가 커 FCF는 늘 음수라 FCF와 배당 비교는 의미가 약하다)', 1)
if '<strong style="color:var(--accent2);">④</strong>' in h:
    _c4 = h[h.index('<strong style="color:var(--accent2);">④</strong>'):]; _c4 = _c4[:_c4.index('</div>')]
    h = h.replace(_c4, '<strong style="color:var(--accent2);">④</strong> 차입금 증가가 요금 기준 자산 증가와 보조를 맞추는지, Ohio 가스 요금안($351M) 등 요금 사건이 진행되는지', 1)
""")
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
# 매출(Q3 2026 10-Q 부문, 고객 계약 매출) — NIPSCO 795.7 + Columbia 492.9 + 본사·기타 10.5 = 1,299.1, 기타 수익 50.3을 더해 총영업수익 1,349.4.
SEG = [('NIPSCO(인디애나 전력·가스)', 795.7, '#00467f'), ('Columbia(가스 배전)', 492.9, '#4f8fc6')]
SEG_ADJ = 60.8
SEG_ADJ_LABEL = '본사·기타 고객 매출 $10.5M과 기타 수익(대체 수익 등) $50.3M'
SEG_TITLE = '매출 구성 — 부문별(고객 계약 매출)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:35~06:39 동부 접수) → 같은 날. 넣지 않은 8-K: 데이터센터 전력 계약(2025-09), ATM, 사채·하이브리드 채권 발행, 신용 한도, 배터리 저장 계약(10/16), 주총.
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 28일 장 전 — Q3 2026 실적', '2026-10-28',
     '매출 $1.35B · 희석 EPS $0.27(1년 전 $0.20) · 조정 EPS $0.27 · 2026 조정 EPS 범위 위쪽으로 좁힘 · 2027~2033 조정 EPS 연 10~11% 목표 · Microsoft와 GenCo 계약 — 그날 주가 +0.6%', 'q3', 'NiSource 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 5일 — Q2 2026 실적', '2026-08-05',
     '매출 $1.29B · 순이익 $46M · 희석 EPS $0.09(1년 전 $0.22) · 조정 EPS $0.16 — 업무 연속성 비용·날씨 영향 포함 — 그날 주가 −3.6%', 'q2', 'NiSource 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 6일 — Q1 2026 실적', '2026-05-06',
     '매출 $2.32B · 순이익 $511M · 희석 EPS $1.06(1년 전 $1.00) · Amazon·Alphabet 계약으로 고객 절감 약 $1.4B · 장기 성장 목표 상향 — 그날 주가 −1.4%', 'q1', 'NiSource 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 11일 — Q4 2025 실적', '2026-02-11',
     '순이익 $258M · 희석 EPS $0.53(1년 전 $0.47) · 2025년 EPS $1.95, 조정 $1.90(전망 상회) — 그날 주가 −0.2%', 'q4', 'NiSource 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 17, 'nt': 15, 'mean': 48.37, 'median': 49, 'low': 43, 'high': 52, 'sb': 10, 'b': 3, 'h': 4, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-09'


# ── 자동 카드 — 부문 2개(수동 지도, 고객 계약 매출). 원문 대조: Q3 2026 795.7/492.9 + 기타 10.5(2026-11-08) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"nix:NIPSCOOperationsMember": ["NIPSCO(인디애나 전력·가스)", "#00467f"], "nix:ColumbiaOperationsMember": ["Columbia(가스 배전)", "#4f8fc6"]},
 "ignore": []
}
