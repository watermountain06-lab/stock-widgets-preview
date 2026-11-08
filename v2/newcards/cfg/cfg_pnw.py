# PNW(피나클 웨스트) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 애리조나 규제 전력회사 APS(Palo Verde 원전 지분 포함) 지주회사. PNW·APS 공동 공시(보도자료는 APS CIK 7286 아래).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-08-04 장 전), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/PNW.md.
# 엔진 입력(2026-10-25): 기본 경로 — 차입금 단기 $818.6M + 1년 안 $775.0M + 장기 $9,775.8M, 현금 $9.1M, 비지배지분 $40.3M. 운용리스 $5.1B(에너지 저장·전력 구매 계약 리스, 1년 새 급증).
# 세전 = IncomeLossIncludingPortionAttributableToNoncontrollingInterest(PRETAX_TAG_BY_CIK — 10-Q는 이 태그만). 일회성 없음. 여름(3분기)에 이익이 몰린다.
CIK = '0000764622'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 1, -2), '적정~고평가'
CO = 'Pinnacle West'
S_ = 'https://www.sec.gov/Archives/edgar/data/7286/'
SEC = 'https://www.sec.gov/Archives/edgar/data/764622/'
TENQ = 'https://www.sec.gov/Archives/edgar/data/764622/000076462226000041/pnw-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000076462226000040/a8-kpnw063026exhibit991.htm', 'q1': S_ + '000076462226000026/a8-kpnw033126exhibit991.htm',
      'q4': S_ + '000076462226000010/pnw202512318kexhibit991.htm', 'q3': S_ + '000076462225000086/a8-kpnw093025exhibit991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="pnwFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('발전·송배전 설비투자(연 약 $2.6B)가 감가상각(약 $1.0B)보다 훨씬 커서 큰 차입금을 뺀 현금흐름 모델의 값이 낮게 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '에어컨 수요 때문에 3분기 이익이 1년 이익의 약 3분의 2이고 4·1분기는 0 근처다. 에너지 저장·가스 전력 구매 계약을 리스로 잡아 운용리스 부채가 1년 새 $3.7B에서 $5.1B로 커졌다 — 리스 포함 순차입금에는 들어가지만, 영업이익이 임차료를 이미 뺀 값이라 EV/EBITDA의 EV와 현금흐름 모델은 운용리스를 빚으로 보지 않는다. 신주(ATM·선도 매도)로 자금을 조달해 주식 수가 늘고 있다.')
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
h = _re.sub(r'(id="pnwDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="pnwDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'SO', 'DUK', 'AEE', 'ATO', 'ED']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(PNW 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q2 2026 10-Q 고객 계약 매출) — 소매 비주거 708.3 + 소매 주거 695.7 + 송전 29.2 + 도매 13.7 + 기타 8.9 = 1,455.8.
SEG = [('소매 — 상업·산업', 708.3, '#e35205'), ('소매 — 주거', 695.7, '#f39a6b'), ('송전', 29.2, '#3b5998'), ('도매', 13.7, '#8ea3cc'), ('기타', 8.9, '#bbbbbb')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 고객·서비스별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(08:18~08:24 동부 접수) → 같은 날. 넣지 않은 8-K: 월간 투자자 자료(7.01), 선도 매도·ATM, 신용 한도.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 4일 — Q2 2026 실적', '2026-08-04',
     '매출 $1.46B(+7.1%) · 순이익 $179M · 희석 EPS $1.43(1년 전 $1.58 — 이자·감가상각 증가)', 'q2', 'Pinnacle West 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 4일 — Q1 2026 실적', '2026-05-04',
     '매출 $1.15B · 순이익 $33M · 희석 EPS $0.27(1년 전 −$0.04)', 'q1', 'Pinnacle West 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 25일 — Q4 2025 실적', '2026-02-25',
     '매출 $1.13B · 순이익 $15M · 희석 EPS $0.13(1년 전 −$0.06) · 2025년 EPS $5.05', 'q4', 'Pinnacle West 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 3일 — Q3 2025 실적', '2025-11-03',
     '매출 $1.82B · 순이익 $413M · 희석 EPS $3.39(1년 전 $3.37)', 'q3', 'Pinnacle West 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 18, 'nt': 13, 'mean': 104.81, 'median': 106, 'low': 91, 'high': 119.5, 'sb': 5, 'b': 1, 'h': 11, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 두 묶음(소매는 고객 축, 나머지는 서비스 축). 원문 대조: Q2 2026 708.3/695.7/29.2/13.7/8.9(2026-10-25) ──
AUTO = True
SEG_MAP = {
 "parts": [
  {"concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], "axis": "srt:MajorCustomersAxis",
   "extra": {"srt:ProductOrServiceAxis": "pnw:RetailElectricServiceMember"},
   "members": {"pnw:RetailNonResidentialMember": ["소매 — 상업·산업", "#e35205"], "pnw:RetailResidentialMember": ["소매 — 주거", "#f39a6b"]}, "ignore": []},
  {"concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"], "axis": "srt:ProductOrServiceAxis", "extra": {},
   "members": {"pnw:TransmissionServicesMember": ["송전", "#3b5998"], "pnw:WholesaleMember": ["도매", "#8ea3cc"], "pnw:OtherServicesMember": ["기타", "#bbbbbb"]},
   "ignore": ["pnw:RetailElectricServiceMember", "pnw:ElectricandTransmissionServiceMember"]}
 ]
}
