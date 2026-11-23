CIK = '0001057352'
BUILD = {'company_tags': [('csgp:PaymentsToAcquirePropertyAndEquipmentAndOtherAssets', 'CapexOtherCsgp', '2020-01-01')]}
# CSGP(코스타 그룹) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 12월 31일. 리츠가 아닌 부동산 정보·온라인 장터 회사(CoStar·LoopNet·Apartments.com·Homes.com·Domain·Matterport).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-28 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 → 다음 세션).
# 엔진 입력(2026-11-22): 영업이익·순이익 = 보고 값, 설비투자 = 사옥·캠퍼스 + 일반 설비(SUM_TAGS, 인수 $788.8M은 밖), 차입금 = 장기 $994M(선순위채), 현금 $500M, 비지배 $17M. 4분기 EPS 2025·2024는 보도자료 값(0.11·0.15).
# 일회성(E54, 세후 기준 — 2026-11-22 사용자 결정): 최근 4분기 순이익 $179M(47+3+55+74). 조정 순이익 조정표 분기별(주식보상·인수 무형자산 상각은 반복이라 제외) —
#   비용 쪽: 인수·통합 7·7·5·15 = $34M, 합의 이자 $9M(2분기), 구조조정 $4M = 세전 $47M → 회사 가정 세율 26%로 세후 약 $35M(19%); Domain 사무실 손상 $10M까지 넣으면 약 24%.
#   이익 쪽: 판결 회수 이익 $24M(합의·손상 순액 −$15M) → 30%와 거리가 있어 정식(Codex·Fable r1: 투자·통화 손실 $23M은 2025년 3분기라 최근 4분기 밖).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'CoStar'
S_ = 'https://www.sec.gov/Archives/edgar/data/1057352/'
SEC = S_
TENQ = S_ + '000105735226000083/csgp-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000105735226000078/q32026earningspressrelease.htm', 'q2': S_ + '000105735226000061/q2fy262026earningspressr.htm',
      'q1': S_ + '000105735226000030/q12026earningspressrelea.htm', 'q4': S_ + '000105735226000012/q42025earningspressrelea.htm',
      'q3old': S_ + '000105735225000116/q32025earningspressrelease.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="csgpFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). 최근 1년 PER은 이익이 막 흑자로 돌아선 시기라 매우 높다 — PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-10, 20)
ACT_REASON = '구독·광고 중심이라 재고 회전(Matterport 카메라 재고 $20M뿐)의 대표성이 낮다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(인수 제외)'
MODEL_NOTE = ('리츠가 아니라 상업·주거 부동산 정보와 온라인 장터(CoStar·LoopNet·Apartments.com·Homes.com, 호주 Domain)를 파는 회사다 — 사이트 분류상 S&P500 부동산과 비교하지만 비교 대상 대부분이 리츠라 동종업 점수는 참고로만 본다. '
              '2023~2025년 주거용 포털 Homes.com에 마케팅을 크게 쓰고 Matterport(2025년 2월)·Domain(2025년 8월)을 사들이며 GAAP 이익이 바닥까지 내려갔다가(2025년 연간 EPS $0.02) 2026년 다시 늘고 있다. 배수 다섯 개 모두 이익이 정상이던 2022~2023년(PER 69~133배)보다도 낮고 주가가 1년 새 절반 넘게 내려 자기 이력 점수가 높다 — 다만 5년 중앙값과 헤더의 PER 구간 적정주가는 이익 바닥기의 수백~수천 배 PER로 부풀어 있어, 적정주가 칸은 해석하지 않는다. '
              '최근 4분기 순이익 $179M에는 회사가 조정 순이익에서 빼는 비용(인수·통합 $34M, 합의 이자 $9M, 구조조정 $4M)이 세전 $47M, 회사 가정 세율 26%로 세후 약 $35M(약 19%) 들어 있고, 판결 회수 이익 $24M도 있다 — 사이트 기준(세후 30%) 아래라 정식 카드다. 회사의 조정 EPS는 주식보상·인수 무형자산 상각까지 되더해 최근 4분기 분기 합 $1.24다. '
              '보고 매출 증가율에는 Domain·Zonda 인수 효과가 커서, 인수를 맞춘 3분기 성장은 약 6%다. 현금흐름 모델은 매년 인수 대금을 따로 빼지는 않지만, 과거 인수 지출과 영업권을 재투자 효율에 넣어 성장에 인수만큼 자본이 든다고 가정한다 — 이익률도 이익 바닥기 값이 섞여 낮게 잡힌다. 8월 Zonda(신축 주택 정보, 약 $0.8B)를 샀고 10월 Vexcel(항공 영상, 약 $0.73B) 인수를 발표했다.')
HEALTH_EXTRA = '차입금은 고정 금리 선순위채 $1.0B다. 현금은 2025년 말 $1.6B에서 자사주 매입($0.67B)·Zonda 인수($0.79B)·판결 지급으로 $0.5B로 줄었고, Vexcel 인수에는 신용한도를 쓸 계획이라 차입이 늘 수 있다.'
PH = ['CBRE', 'PLD', 'AMT', 'EQIX', 'SPG', 'O']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '부동산 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(CSGP 제외)과 배수 순위를 매긴 값이다.',
            '비교 대상 대부분이 리츠(물류·데이터센터·의료·쇼핑몰·주택)이고 부동산 서비스는 CBRE 정도라, 정보·온라인 장터 회사인 코스타와는 사업이 다르다. 차트에는 CBRE와 리츠 5곳이 보인다.')
SEG = [('상업용 부동산(CoStar·LoopNet 등)', 492, '#1f3a93'), ('주거용 부동산(Apartments.com·Homes.com·Domain 등)', 460, '#5b7bd5')]
SEG_ADJ = 0
SEG_TITLE = '부문별 매출'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('red', '2026년 10월 27일 장 마감 뒤 — Q3 2026 실적', '2026-10-28',
     '매출 $952M(+14%) · 희석 EPS $0.18 · 조정 EPS $0.38 · 조정 EBITDA $229M(2배) · 순신규 계약 $37M(1년 전 $84M) · 2026년 조정 EBITDA 전망 상향, 4분기 매출 전망은 약 +10% · Vexcel 인수 발표 — 다음 날 주가 −14.0%', 'q3', 'CoStar 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 28일 장 마감 뒤 — Q2 2026 실적', '2026-07-29',
     '매출 $925M(+18%) · 희석 EPS $0.14 · 조정 EPS $0.32 · 순신규 계약 $69M · 2026년 매출 전망 하향($3.715~3.755B) — 다음 날 주가 −1.6%', 'q2', 'CoStar 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 28일 장 마감 뒤 — Q1 2026 실적', '2026-04-29',
     '매출 $897M(+23%) · 희석 EPS $0.01 · 조정 EPS $0.23 — 다음 날 주가 −5.1%', 'q1', 'CoStar 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 24일 장 마감 뒤 — 2025년 연간 실적', '2026-02-25',
     '4분기 매출 $900M(+27%) · 희석 EPS $0.11 · 2025년 순이익 $7M(Matterport·Domain 인수 비용) · 조정 순이익 $364M — 다음 날 주가 −8.9%', 'q4', 'CoStar 실적 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 28일 장 마감 뒤 — Q3 2025 실적', '2025-10-29',
     '매출 $834M(+20%) · 희석 EPS −$0.07 · 조정 EBITDA $115M(+51%) — 다음 날 주가 −9.9%', 'q3old', 'CoStar 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 14, 'mean': 34.64, 'median': 34, 'low': 26, 'high': 45, 'sb': 8, 'b': 4, 'h': 8, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-23'
POST = [r"""
h = h.replace('Q3 2026 10-Q 부문 표 (SEC)', 'Q3 2026 10-Q 부문 주석 (SEC)')
import re as _rc
h = _rc.sub(r'잔존가치\(5년 뒤\)가 내재가치의 ([0-9]+)%', r'잔존가치(5년 뒤)가 영업 기업가치의 \1%', h)
h = h.replace('`잔존가치(5년 뒤)가 내재가치의 ${', '`잔존가치(5년 뒤)가 영업 기업가치의 ${')
h = _rc.sub(r'(id="csgpFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해석 부적합\3', h, count=1)
h = h.replace('최근 1년 PER은 이익이 막 흑자로 돌아선 시기라 매우 높다 — PER만으로 낸 범위라 판정과 따로 읽는다.', '최근 1년 PER은 이익이 막 흑자로 돌아선 시기라 수백~수천 배여서, 이 구간으로 낸 적정주가는 해석하지 않는다(판정과 무관).')
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
 "members": {"csgp:CommercialRealEstateSegmentMember": ["상업용 부동산(CoStar·LoopNet 등)", "#1f3a93"],
             "csgp:ResidentialRealEstateSegmentMember": ["주거용 부동산(Apartments.com·Homes.com·Domain 등)", "#5b7bd5"]},
 "ignore": []
}
