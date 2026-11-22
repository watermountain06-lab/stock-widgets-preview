CIK = '0000910606'
BUILD = {'overlay': True, 'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # Q2·Q3 10-Q가 요약 자료에 늦음(Regency Centers LP 결합 공시) — 인라인 XBRL 보충; EPS는 2019년부터 계속사업 희석 EPS 태그로만
# REG(리전시 센터스) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 12월 31일. 리츠(REIT) — 식료품점 중심 근린 쇼핑센터(UPREIT, Regency Centers L.P.와 결합 공시).
# 출처: SEC XBRL + 인라인 XBRL 보충(Q2·Q3 2026 10-Q 요약 자료 미반영 — Q3 10-Q 2026-11-06 14:39 동부 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 16~17시 동부 → 다음 세션).
# 엔진 입력(2026-11-21): 영업이익 = 매출 − 영업비용 합계(손익계산서에 영업이익 줄이 없다 — DERIVED_OPINC; 손상·매각 이익·이자·투자 이익은 회사 배치대로 영업 밖),
#   순이익 = 보통주 귀속(EXTRA_TAGS·PREFER_TAGS), 설비투자 = 개발·개량 지출(현금흐름표 한 줄, 9개월 $317.7M — 인수 $58.4M 제외), 차입금 = 채권 $4,772.1M + 신용한도 $115.0M = $4,887.1M,
#   우선주 Series A·B $225M, 비지배지분 $272.5M(교환 가능 운영 파트너십 유닛 + 합작 파트너 몫). 4분기 EPS는 보도자료 값(Q4_EPS_OVERRIDE 2021~2025).
# 일회성(E54): 최근 4분기 보통주 귀속 순이익 $511.7M(4분기 $199.1M + 1~9월 $312.6M, 희석 EPS 1.09+0.68+0.61+0.41 = 2.79). 회사가 FFO에서 빼는 매각 이익(합작 몫 포함) $139.0M(4분기 93.3 + 1~9월 45.7) = 27.2%,
#   손상 $65.1M(3분기 65.1, 4분기 −0.03) = 12.7% → 순액 $73.9M = 14.4%. 이익만 27%·비용만 13%·순액 14% — 모두 30% 아래라 정식(2026-11-07·11-13 기준).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Regency Centers'
S_ = 'https://www.sec.gov/Archives/edgar/data/910606/'
SEC = S_
TENQ = S_ + '000119312526451423/reg-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000119312526450159/reg-ex99_1.htm', 'q2': S_ + '000119312526323784/reg-ex99_1.htm',
      'q1': S_ + '000119312526191872/reg-ex99_1.htm', 'q4': S_ + '000119312526039477/reg-ex99_1.htm',
      'q3old': S_ + '000119312525253799/reg-ex99_1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="regFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). 리츠는 감가상각이 커서 PER이 높게 나온다 — PER만으로 낸 범위라 판정과 따로 읽는다. 최근 4분기 EPS에는 매각 이익(약 27%)과 손상(약 13%)이 함께 들어 있고, 다음 실적 발표 뒤 2025년 4분기 EPS $1.09가 빠지면 — 지금 PER 구간이 그대로이고 회사 전망대로라면 — 최근 4분기 EPS가 약 $2.3으로 줄어 범위가 현재가 아래로 내려간다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 50)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(개발·개량)'   # 현금흐름표 한 줄 — 신규 개발과 기존 건물 개량이 함께, 인수 제외
MODEL_NOTE = ('리츠는 건물 감가상각이 커서 GAAP 순이익이 실제 현금 창출보다 작게 나오고, 업계는 FFO(순이익에 부동산 감가상각·손상을 되더하고 매각 이익을 뺀 값)로 본다 — 리전시의 2026년 연간 Nareit FFO 전망은 주당 $4.86~4.88로 지난 4분기 GAAP EPS($2.79)의 약 1.7배다(전망과 지난 실적이라 기간은 다르다). 이 카드는 다른 카드와 같은 GAAP 배수로 보므로 PER이 높게 나온다. 사이트에는 리츠 전용 평가(FFO·순자산가치)가 아직 없고, 현금흐름 내재가치가 0 이하인 것은 모델 구조 탓이다 — 감가상각을 뺀 영업이익을 장부 투하자본에 비춰 보면 자본수익률이 할인율 10%보다 낮아 성장할수록 가치가 깎이고, 실제로는 법인세가 거의 없는데 세금 자료가 없어 처음부터 일반 기업 세율 21%를 쓰며, 거기서 순차입금·우선주·비지배지분을 뺀다. '
              '손익계산서에 영업이익 줄이 없어 영업이익은 매출에서 영업비용(감가상각 포함)을 뺀 값으로 쓴다 — 회사 배치대로 손상·매각 이익·이자는 영업 밖이다. 최근 4분기 순이익에는 회사가 FFO에서 빼는 매각 이익 $139M(2025년 4분기 $93M — 대부분 합작사와 건물을 맞바꾼 현물 분배 이익 $72M으로 현금이 들어오지 않았다 — 과 2026년 1~9월 $46M)과 2026년 3분기 부동산 손상 $65M이 들어 있다(이익 쪽 약 27%, 비용 쪽 약 13%, 순액 약 14%). 다음 실적 발표 뒤에는 2025년 4분기(EPS $1.09)가 빠져, 회사의 2026년 GAAP EPS 전망($2.31~2.33, 직전 $2.48~2.52에서 내림)대로면 최근 4분기 EPS가 약 $2.3으로 줄고 같은 주가에서 PER이 5년 중앙값 위로 올라간다. '
              '설비투자는 신규 개발과 기존 건물 개량이 현금흐름표 한 줄이라 함께 넣었고(그래서 FCF가 배당보다 작게 나온다 — 회사가 보는 AFFO는 Core Operating Earnings에서 유지·임대 관련 지출만 빼고 부채비용·파생상품·주식보상 등을 조정한 값이라 개발 지출이 빠져 있다), 부동산 인수(1~9월 $58M)는 넣지 않았다 — 현금흐름 모델의 재투자는 실제 지출이 아니라 매출 증가 ÷ 매출/투하자본으로 따로 추정한다. 합작 투자(지분법)는 지분법 이익만 순이익에 들어오고 그 자산은 내재가치에 따로 더하지 않는다. 우선주(Series A·B $225M)는 주주가치에서 뺀다.')
HEALTH_EXTRA = '쇼핑센터 매입·개발 자금을 채권·대출로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
PH = ['KIM', 'FRT', 'O', 'PLD', 'WELL', 'PSA']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(REG 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 리츠 6곳이 보인다.')
# 매출(Q3 2026 10-Q 손익계산서): 임대 수익 408.7 + 기타 부동산 수익 3.2 + 관리·거래·기타 수수료 7.1 = 419.1. 1년 전 377.8·3.1·6.7.
SEG = [('임대 수익', 408.7, '#d9622b'), ('관리·거래·기타 수수료', 7.1, '#e8a23a'), ('기타 부동산 수익', 3.2, '#f3d3a8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 손익계산서 항목별'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 5일 장 마감 뒤 — Q3 2026 실적', '2026-11-06',
     '보통주 순이익 $75M · 희석 EPS $0.41(1년 전 $0.58 — 부동산 손상 $65M, 매각 이익 $24M) · Nareit FFO $1.23(1년 전 $1.15) · 2026년 FFO 전망 $4.86~4.88로 상향, GAAP EPS 전망은 $2.31~2.33으로 하향 · 분기 배당 $0.800(+6%) — 다음 날 주가 −1.9%', 'q3', 'Regency 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 29일 장 마감 뒤 — Q2 2026 실적', '2026-07-30',
     '희석 EPS $0.61(1년 전 $0.56) · Nareit FFO $1.21 · 동일 점포 NOI +3.8% · 연간 FFO 전망 $4.84~4.88로 상향 — 다음 날 주가 −0.9%', 'q2', 'Regency 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 29일 장 마감 뒤 — Q1 2026 실적', '2026-04-30',
     '희석 EPS $0.68(1년 전 $0.58) · Nareit FFO $1.20 · 동일 점포 NOI +4.4% — 다음 날 주가 −1.9%', 'q1', 'Regency 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 5일 장 마감 뒤 — 2025년 연간 실적', '2026-02-06',
     '4분기 보통주 순이익 $199M · 희석 EPS $1.09(1년 전 $0.46, 합작 현물 분배 이익 $72M 포함) · Nareit FFO $1.17 · 2025년 FFO $4.64(+7.9%) — 다음 날 주가 −0.3%', 'q4', 'Regency 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 28일 장 마감 뒤 — Q3 2025 실적', '2025-10-29',
     '희석 EPS $0.58(1년 전 $0.54) · Nareit FFO $1.15 · 2025년 FFO 전망 $4.62~4.64로 상향 — 다음 날 주가 −3.1%', 'q3old', 'Regency 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 15, 'mean': 83.93, 'median': 85, 'low': 76, 'high': 88, 'sb': 7, 'b': 5, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-22'
POST = [r'''
h = h.replace('순차입금(리스 포함)', '순차입금').replace('차입금·리스 $', '차입금 $')
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(개발·개량) ·', '· GAAP 기준(영업이익 = 매출 − 영업비용, 손상·매각 이익 제외) · FCF는 영업현금흐름 − 설비투자(개발·개량) ·')
h = h.replace('10-Q 부문 표 (SEC)', '10-Q 손익계산서 (SEC)')
h = h.replace('합성 영업이익률(세전이익 기준)', '합성 영업이익률(매출 − 영업비용)').replace('합성 영업이익(세전이익 기준)', '합성 영업이익(매출 − 영업비용)')
''']

# 현금흐름 0 이하 보정 — ED·SO와 같은 POST
POST += [r'''
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
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률·영업이익률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="oDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')

AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {"us-gaap:LeaseIncome": ["임대 수익", "#d9622b"],
             "reg:RevenuesFromManagementTransactionAndOtherFees": ["관리·거래·기타 수수료", "#e8a23a"],
             "us-gaap:OtherOperatingIncome": ["기타 부동산 수익", "#f3d3a8"]},
 "ignore": []
}
