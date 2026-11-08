# PEG(PSEG) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 198. 뉴저지 규제 전력·가스 배전(PSE&G), 원전 발전·기타(PSEG Power & Other).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-04), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표, 11시 콜, 8-K 장중 접수), StockAnalysis. 사전 조사 자료표 scratchpad pre/PEG.md.
# 엔진 입력(2026-10-24): D&A = 손익계산서 감가상각 줄(EXTRA_TAGS CostOfGoodsAndServicesSoldDepreciationAndAmortization — 기본 태그 없어 0이었다, TTM $1,279M). 차입금 $24,541M(CP 950 + 1년 안 850 + 장기 22,741).
# GAAP 이익에 원전 해체기금(NDT) 손익(영업이익 밖)과 에너지 계약 시가평가 손익(영업이익 안)이 섞여 분기마다 흔들린다 — 최근 4분기 합으로는 회사 기준 이익보다 약 5% 낮다.
CIK = '0000788784'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'PSEG'
S_ = 'https://www.sec.gov/Archives/edgar/data/788784/'
SEC = S_
TENQ = S_ + '000119312526332943/peg-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000119312526331660/d101695dex99.htm', 'q1': S_ + '000119312526205254/d63722dex99.htm',
      'q4': S_ + '000119312526073678/d57788dex99.htm', 'q3': S_ + '000119312525261789/d36283dex99.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="pegFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 40)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('GAAP 이익에는 원전 해체기금 투자 손익(영업이익 밖)과 에너지 계약 시가평가 손익(영업이익 안)이 들어 있어 분기마다 크게 흔들린다 — Q2 2026은 시가평가 손실 때문에 GAAP EPS가 1년 전보다 크게 줄었지만 회사 기준 이익은 늘었다. 최근 4분기 합으로는 차이가 작다. '
              '원전 생산 세액공제 때문에 실효세율이 낮다. 송배전망 설비투자가 영업현금흐름과 거의 같아 FCF가 작고, 현금흐름 모델은 이 투자를 계속 이어 간다고 보아 큰 차입금을 뺀 주당 지분가치가 세 시나리오 모두 0 이하다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. 판정의 현금흐름 표는 0 이하 값에 대한 현행 규칙(−2)이다. '
              '자기 이력 PER 분포에도 과거 분기의 시가평가·해체기금 손익과 적자 분기 제외가 영향을 준다.')
HEALTH_EXTRA = '설비투자 자금을 사채·기업어음으로 조달하는 구조라 차입금 비중이 높게 나온다 — 규제 유틸리티에서는 흔한 모습이다. 이자보상배율은 Q2 단일 분기 값이라 시가평가 손실에 눌려 있다(최근 4분기로는 더 높다).'   # 고정 문장(XEL과 같음)
# 현금흐름 0 이하 문구 보정 — XEL과 같은 POST(안건 E51)
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
h = _re.sub(r'(id="pegDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
PH = ['NEE', 'CEG', 'DUK', 'SO', 'AEP', 'XEL']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(PEG 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q2 2026 10-Q 주석 16 부문) — PSE&G 2,137 + PSEG Power & Other 534 = 2,671, 부문 간 거래 −117 → 2,554. 1년 전 2,031·920·−146.
SEG = [('PSE&G(규제 배전)', 2137.0, '#f26722'), ('PSEG Power·기타(원전)', 534.0, '#f7a26d')]
SEG_ADJ = -117.0
SEG_ADJ_LABEL = '부문 간 거래 제거'
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 회사 기준(non-GAAP) EPS·가이던스는 쓰지 않는다). 반응일: 보도자료 장 전(11시 콜), 8-K 장중 접수 → 같은 날.
# 넣지 않은 8-K: 사채 $500M(6/3), 투자자 자료(7/1), 이사 선임·주총.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 4일 — Q2 2026 실적', '2026-08-04',
     '매출 $2.55B(1년 전 $2.81B) · 순이익 $334M · 희석 EPS $0.67(1년 전 $1.17) — 에너지 계약 시가평가 손실 세전 $258M·해체기금 관련 이익 $153M(회사 조정 항목 기준) 포함', 'q2', 'PSEG 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 5일 — Q1 2026 실적', '2026-05-05',
     '매출 $3.85B · 순이익 $741M · 희석 EPS $1.48(1년 전 $1.18)', 'q1', 'PSEG 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 26일 — Q4 2025 실적', '2026-02-26',
     '매출 $2.92B · 순이익 $315M · 희석 EPS $0.63(1년 전 $0.57) · 2025년 희석 EPS $4.22 — 시가평가 손실 세전 $97M 포함', 'q4', 'PSEG 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 3일 — Q3 2025 실적', '2025-11-03',
     '매출 $3.23B · 순이익 $622M · 희석 EPS $1.24(1년 전 $1.04)', 'q3', 'PSEG 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 15, 'mean': 80.67, 'median': 80, 'low': 72.5, 'high': 87, 'sb': 7, 'b': 1, 'h': 15, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 2개(수동 지도, Revenues), 부문 간 거래는 SEG_ADJ. 원문 대조: Q2 2026 2,137/534/−117(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"peg:PublicServiceElectricandGasCompanyMember": ["PSE&G(규제 배전)", "#f26722"], "peg:PSEGPowerOtherMember": ["PSEG Power·기타(원전)", "#f7a26d"]},
 "ignore": []
}
