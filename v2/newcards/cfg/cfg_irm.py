CIK = '0001020569'
BUILD = {}
# IRM(아이언 마운틴) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 12월 31일. 리츠(REIT) — 기록·정보 관리(문서 보관·파쇄) + 데이터센터 + 자산 수명주기 관리(ALM).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-05 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 시작 전 → 같은 날 반응).
# 엔진 입력(2026-11-22): 차입금 = LongTermDebt $17,972.2M(금융리스 포함 — 리스 칸에는 운용리스만, FISV 방식), 현금 = $188.2M(재무상태표 줄 태그),
#   비지배 $325.3M + 상환 가능 $62.2M, 자본 −$1,388M(자본 잠식 → PBR 해당 없음). 4분기 EPS 2025는 보도자료 값(0.30).
# 일회성(E54): 달러 기준(각 분기 보도자료 조정표) — 인수·통합 $12.7M, 구조조정 $43.5M(2025년 말 끝난 3년 프로그램), 처분·감액 손실 $44.1M, 기타 영업외 $51.2M(인수 대금 후불 채무 재평가 손실 등, 환율 이익과 상계) = 세전 $151.4M,
#   보통주 순이익 $458.5M의 33.0%. 회사 조정표 세금 행 −$28.6M을 반영한 세후 $122.8M = 26.8% → 세후 기준(2026-11-22 사용자 결정: 일회성은 세후로 비교) 30% 아래라 정식(Fable r1 달러 재계산).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Iron Mountain'
S_ = 'https://www.sec.gov/Archives/edgar/data/1020569/'
SEC = S_
TENQ = S_ + '000102056926000084/irm-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000102056926000081/q32026earningspressrelea.htm', 'q2': S_ + '000102056926000068/final-q22026earningspres.htm',
      'q1': S_ + '000102056926000036/q12026earningspressrelea.htm', 'q4': S_ + '000102056926000009/q42025earningspressrelea.htm',
      'q3old': S_ + '000102056925000203/q32025earningspressrelea.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="irmFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). 리츠는 감가상각이 커서 PER이 높게 나온다 — PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(데이터센터 개발 포함)'
MODEL_NOTE = ('리츠는 건물 감가상각이 커서 GAAP 순이익이 실제 현금 창출보다 작게 나오고, 업계는 FFO·AFFO를 보완 지표로 쓴다 — 회사의 2026년 AFFO 전망은 주당 $5.94~6.00, 조정 EBITDA는 $2.95~2.98B이다. 이 카드는 다른 카드와 같은 GAAP 배수로 보므로 PER이 높게 나온다. 사이트에는 리츠 전용 평가가 아직 없다. '
              '최근 4분기 보통주 순이익 $459M(EPS $1.53)에는 회사가 조정 EPS에서 빼는 비용이 세전 $151M 들어 있다 — 2025년 4분기 구조조정 $43M(2025년 말 끝난 3년 프로그램), 자산 처분·감액 손실 $44M, 인수 대금 후불 채무 재평가 손실 등 기타 영업외 비용 $51M(환율 이익과 상계한 값), 인수·통합 $13M. 세전으로는 순이익의 약 33%지만 회사 조정표의 세금 행을 반영하면 약 27%라, 세후로 비교하는 사이트 기준(30%) 아래에서 정식 카드로 둔다 — 경계에 가깝다. 지난 3년 EPS에도 구조조정 비용이 들어 있어 5년 PER 중앙값도 높게 나온다. '
              '아이언 마운틴은 기록 보관(매출의 약 72%)을 기반으로 데이터센터·자산 수명주기 관리를 넓히는 중이라 설비투자가 크다(최근 4분기 $2.2B — 대부분 데이터센터 개발, 유지 설비투자는 일부). 그래서 FCF가 음수로 나오고 PCR은 해당 없다. 누적 배당이 회계상 이익을 넘고 기타포괄손실이 쌓여 지배주주 자본이 음수(−$1.4B)라 PBR은 해당 없다. 4분기 배당은 주당 $0.993으로 15% 올렸다. 1년 안 만기 차입금이 $1.2B로 늘어 유동비율이 낮다. 차입금 $18.0B에는 금융리스($0.57B)가 들어 있어 따로 더하지 않는다. '
              '현금흐름 내재가치는 이 모델의 가정에서 리츠에 낮게 나온다 — 감가상각을 뺀 영업이익의 자본수익률이 할인율 10%보다 낮고, 실제로는 법인세가 적은데 5년 뒤 세율을 21%로 수렴시키며, 대규모 성장 투자가 재투자로 잡힌다.')
HEALTH_EXTRA = '데이터센터 개발 자금을 채권으로 조달하고 자본이 음수라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 EBITDA 대비로 본다.'
PH = ['EQIX', 'DLR', 'AMT', 'PSA', 'O', 'PLD']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(IRM 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 데이터센터·통신탑·창고 리츠 등 6곳이 보인다.')
SEG = [('기록·정보 관리', 1433.1, '#0d2c54'), ('데이터센터', 273.6, '#3f6ea5'), ('기타(자산 수명주기 관리 등)', 283.9, '#b9cde6')]
SEG_ADJ = 0
SEG_TITLE = '부문별 매출'
NEWS_RANGE = '2025.11 ~ 2026.11'
NEWS = [
    ('red', '2026년 11월 5일 장 시작 전 — Q3 2026 실적', '2026-11-05',
     '매출 $1.99B(+13.5%) · 희석 EPS $0.41 · 조정 EPS $0.64 · AFFO 주당 $1.53 · 2026년 전망 상향(AFFO 주당 $5.94~6.00) · 4분기 배당 15% 인상(주당 $0.993) — 그날 주가 −11.1%', 'q3', 'Iron Mountain 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 5일 장 시작 전 — Q2 2026 실적', '2026-08-05',
     '희석 EPS $0.34 · 조정 EPS $0.60 · AFFO 주당 $1.44 · 2026년 전망 상향 — 그날 주가 +1.3%', 'q2', 'Iron Mountain 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 30일 장 시작 전 — Q1 2026 실적', '2026-04-30',
     '희석 EPS $0.48 · 조정 EPS $0.60(+40%) · AFFO 주당 $1.43(+22%) · 2026년 전망 상향 — 그날 주가 +10.0%', 'q1', 'Iron Mountain 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 12일 장 시작 전 — 2025년 연간 실적', '2026-02-12',
     '4분기 희석 EPS $0.30(구조조정 비용 포함) · 조정 EPS $0.61 · 2025년 AFFO 주당 $5.17 · 2026년 AFFO 전망 주당 $5.69~5.79 — 그날 주가 +5.8%', 'q4', 'Iron Mountain 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 5일 장 시작 전 — Q3 2025 실적', '2025-11-05',
     '희석 EPS $0.28 · 조정 EPS $0.54 · AFFO 주당 $1.32 — 그날 주가 −2.8%', 'q3old', 'Iron Mountain 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 12, 'nt': 10, 'mean': 140.2, 'median': 140, 'low': 124, 'high': 155, 'sb': 7, 'b': 4, 'h': 0, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-22'

POST = [r"""
h = h.replace('Q3 2026 10-Q 부문 표 (SEC)', 'Q3 2026 10-Q 부문 주석 (SEC)')
import re as _ri
h = _ri.sub(r'잔존가치\(5년 뒤\)가 내재가치의 ([0-9]+)%', r'잔존가치(5년 뒤)가 영업 기업가치의 \1%', h)
h = h.replace('`잔존가치(5년 뒤)가 내재가치의 ${', '`잔존가치(5년 뒤)가 영업 기업가치의 ${')
"""]

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
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"irm:GlobalRecordsandInformationManagementBusinessMember": ["기록·정보 관리", "#0d2c54"],
             "irm:GlobalDataCenterBusinessMember": ["데이터센터", "#3f6ea5"],
             "us-gaap:CorporateAndOtherMember": ["기타(자산 수명주기 관리 등)", "#b9cde6"]},
 "ignore": ["us-gaap:ReportableSegmentAggregationBeforeOtherOperatingSegmentMember"]
}
