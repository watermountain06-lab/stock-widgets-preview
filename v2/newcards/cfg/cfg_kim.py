CIK = '0000879101'
BUILD = {'overlay': True, 'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted', 'company_tags': [('kim:TotalNetGainLossOnSaleOfOperatingProperties', 'GainOnSaleOfPropertiesKim', '2020-01-01'), ('kim:PaymentsForImprovementsToOperatingRealEstate', 'PaymentsForCapitalImprovements', '2020-01-01')]}   # Q3 10-Q가 요약 자료에 늦음(지주회사 + OP LLC 결합 공시) — 인라인 XBRL 보충; 2021년부터 EPS를 계속사업 희석 EPS 태그로만 낸다
# KIM(킴코 리얼티) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 12월 31일. 리츠(REIT) — 식료품점 중심 근린 쇼핑센터(UPREIT, 2023-01부터 Kimco Realty OP LLC와 결합 공시).
# 출처: SEC XBRL + 인라인 XBRL 보충(Q3 2026 10-Q 2026-10-29 12:10 동부 접수 — 요약 자료 미반영, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 06:5x 동부 → 그날).
# 엔진 입력(2026-11-21): 영업이익 = 영업이익 줄 − 부동산 매각 이익(DERIVED_OPINC, O·WELL처럼 손상은 영업 안), 순이익 = 보통주 귀속(EXTRA_TAGS·PREFER_TAGS),
#   설비투자 = 기존 부동산 개량 지출(회사 고유 태그, 9개월 $273.9M — 인수 $115.5M 제외), 차입금 = 무담보 채권 $8,043M + 담보 $429M = $8,472M,
#   우선주 = 청산가치 $483.5M, 비지배지분 $161.5M, 단기투자 제외(2010 낡은 값). 4분기 EPS는 보도자료 값(Q4_EPS_OVERRIDE).
# 일회성(E54): 최근 4분기 보통주 귀속 순이익 $719.2M(EPS 0.21+0.23+0.22+0.41 = 1.07). 회사가 FFO에서 빼는 매각 이익 $186.1M(연결 125.6 + 합작 60.5), 손상 $16.1M
#   → 순액 $170.0M = 23.6%, 이익만(대출 충당 환입·투자 이익 등 포함) 약 27%, 비용만 약 2% — 모두 30% 아래라 정식(GAAP + 문장, 2026-11-07 기준).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Kimco Realty'
S_ = 'https://www.sec.gov/Archives/edgar/data/879101/'
SEC = S_
TENQ = S_ + '000119312526437341/kim-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000119312526436941/kim-ex99_1.htm', 'q2': S_ + '000119312526331498/kim-ex99_1.htm',
      'q1': S_ + '000119312526193907/kim-ex99_1.htm', 'q4': S_ + '000119312526047615/kim-ex99_1.htm',
      'q3old': S_ + '000119312525257371/kim-ex99_1.htm', 'exch': S_ + '000114036126024883/ef20076085_ex99-2.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="kimFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). 리츠는 감가상각이 커서 PER이 높게 나온다 — PER만으로 낸 범위라 판정과 따로 읽는다. 최근 4분기 EPS의 약 4분의 1은 부동산 매각 이익에서 손상차손을 뺀 금액이라, 그것을 빼면 범위가 현재가 아래로 내려간다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 50)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(기존 부동산 개량)'   # 인수·개발 지출은 넣지 않는다(Codex r1 2026-11-21)
MODEL_NOTE = ('리츠는 건물 감가상각이 커서 GAAP 순이익이 실제 현금 창출보다 작게 나오고, 업계는 FFO(순이익에 부동산 감가상각·손상을 되더하고 매각 이익을 뺀 값)로 본다 — 킴코의 2026년 연간 FFO 전망은 주당 $1.84~1.86으로 최근 4분기 GAAP EPS($1.07)의 약 1.7배다. 이 카드는 다른 카드와 같은 GAAP 배수로 보므로 PER이 높게 나온다. 사이트에는 리츠 전용 평가(FFO·순자산가치)가 아직 없고, 현금흐름 내재가치가 0 이하인 것은 모델 구조 탓이다 — 감가상각을 뺀 영업이익을 장부 투하자본에 비춰 보면 자본수익률이 약 3%로 할인율 10%보다 낮아 성장할수록 가치가 깎이고(두 시나리오는 차입금을 빼기 전 사업 가치부터 0 이하), 실제로는 법인세가 거의 없는데 5년 뒤 세율을 일반 기업 21%로 수렴시키며, 거기서 순차입금(차입금 − 현금)·우선주·비지배지분 약 $8.6B를 뺀다. 합작 투자·기타 투자·대출채권 약 $1.7B는 자산가치를 따로 더하지 않고, 그 수익도 영업이익에서 빠져 있다. '
              '최근 4분기 순이익에는 회사가 FFO에서 빼는 부동산 매각 이익 $186M(합작 몫 $60M 포함)과 손상차손 $16M이 들어 있다(순 $170M, 순이익의 약 24% — 다른 조정 항목까지 이익 쪽에 넣어도 약 27%). 3분기 EPS $0.41이 1년 전 $0.19의 두 배가 넘은 것도 대부분 이 매각 이익이다. 영업이익은 매각 이익을 뺀 값(손상은 포함)으로 쓴다. 과거 5년 매출 성장률에는 Weingarten(2021년)·RPT(2024년) 합병으로 늘어난 매출이 들어 있다 — 3분기 동일 점포 순영업이익 증가율은 4.9%였다. '
              '설비투자는 기존 쇼핑센터 개량 지출만 넣었고 부동산 인수(1~9월 $115M)와 구조화 투자(메자닌 대출·우선 지분)는 넣지 않았다. 우선주(청산가치 $484M)는 주주가치에서 뺀다.')
HEALTH_EXTRA = '쇼핑센터 매입·보유 자금을 채권·대출로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
# 현금흐름 0 이하 보정 — ED·SO와 같은 POST
POST = [r'''
_R = '현금흐름 모델의 주당 지분가치가 0 이하라 현재가 요구 성장률·영업이익률은 해석할 수 없다.'
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
h = _re.sub(r'(id="oDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 역산 문장 덮어쓰기 방지는 fill.py 공통 처리(const _XR 카드)로 옮겼다(2026-11-21). 아래는 KIM 라벨·출처 문구
POST.append(r'''
import re as _re3
h = h.replace('순차입금(리스 포함)', '순차입금').replace('차입금·리스 $', '차입금 $')
h = h.replace('10-Q 부문 표 (SEC)', '10-Q 손익계산서 (SEC)')
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·', '· GAAP 기준(영업이익은 부동산 매각 이익 제외) · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·')
h = h.replace('합성 영업이익률(세전이익 기준)', '매각 이익 제외 영업이익률').replace('합성 영업이익(세전이익 기준)', '매각 이익 제외 영업이익')
''')
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률·영업이익률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="oDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['O', 'REG', 'FRT', 'PLD', 'WELL', 'PSA']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(KIM 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 리츠 6곳이 보인다.')
# 매출(Q3 2026 10-Q 손익계산서): 임대 수익(순) 539.7 + 관리·기타 수수료 6.4 = 546.1.
SEG = [('임대 수익', 539.7, '#1b4f9c'), ('관리·기타 수수료', 6.4, '#b4c9e8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 손익계산서 항목별'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('green', '2026년 10월 29일 장 전 — Q3 2026 실적', '2026-10-29',
     '보통주 순이익 $272M · 희석 EPS $0.41(1년 전 $0.19, 대부분 부동산 매각 이익) · FFO $0.47(+6.8%) · 임대 계약 기준 점유율 96.6% 사상 최고 · 2026년 FFO 전망 $1.84~1.86으로 상향 — 그날 주가 +4.4%', 'q3', 'Kimco 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 4일 장 전 — Q2 2026 실적', '2026-08-04',
     '보통주 순이익 $146M · 희석 EPS $0.22(1년 전 $0.23) · FFO $0.46(+4.5%) · 분기 배당 $0.28로 인상(직전 $0.26, 1년 전보다 12%) — 그날 주가 −1.6%', 'q2', 'Kimco 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 6월 11일 — 교환사채 발행', '2026-06-11',
     '6월 10일 $500M 발행 계획 발표 → 6월 11일 $525M로 늘려 가격 확정(이자 3.50%, 2031년 만기) → 6월 15일 옵션 포함 $600M 발행 — 6월 11일 주가 +1.5%', 'exch', 'Kimco 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 30일 장 전 — Q1 2026 실적', '2026-04-30',
     '보통주 순이익 $157M · 희석 EPS $0.23(1년 전 $0.18) · FFO $0.46(+4.5%) — 그날 주가 0.0%', 'q1', 'Kimco 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 12일 장 전 — 2025년 연간 실적', '2026-02-12',
     '4분기 보통주 순이익 $144M · 희석 EPS $0.21(1년 전 $0.23) · FFO $0.44(+4.8%) · 2025년 EPS $0.82 — 그날 주가 +1.5%', 'q4', 'Kimco 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 30일 장 전 — Q3 2025 실적', '2025-10-30',
     '보통주 순이익 $130M · 희석 EPS $0.19(1년 전 $0.19) · FFO $0.44 — 그날 주가 −1.9%', 'q3old', 'Kimco 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 20, 'mean': 26.56, 'median': 27, 'low': 23, 'high': 30, 'sb': 6, 'b': 4, 'h': 14, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-23'


AUTO = True
SEG_MAP = {
 "parts": [
  {
   "concepts": [],
   "axis": None,
   "extra": {},
   "members": {
    "us-gaap:OperatingLeaseLeaseIncome": ["임대 수익", "#1b4f9c"],
    "kim:ManagementFeeAndOtherFeeIncome": ["관리·기타 수수료", "#b4c9e8"]
   }
  }
 ]
}
# 부동산 매각 이익은 영업이익 줄 안에 회사 고유 태그로만 있다 — company_tags로 싣고 build_multiple_history.DERIVED_OPINC가 영업이익에서 뺀다
