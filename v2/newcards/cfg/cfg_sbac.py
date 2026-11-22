CIK = '0001034054'
BUILD = {}
# SBAC(SBA 커뮤니케이션스) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 12월 31일. 리츠(REIT) — 통신 타워 임대(미국·중남미·아프리카) + 타워 공사(사이트 개발).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-05 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 → 다음 세션).
# 엔진 입력(2026-11-22): 영업이익 = 보고 값, 순이익 = SBA 귀속, 설비투자 = 현금흐름표 Capital expenditures(9개월 $183.6M — 타워·부지 인수 $204.7M 제외),
#   차입금 = 1년 안 $3,557.5M + 장기 $9,338.5M = $12,895.9M, 비지배 = 상환 가능 $92.9M, 자본 = 주주 결손 −$4,834.8M(PBR 해당 없음).
# 일회성(E54, 세후 기준 — 2026-11-22 사용자 결정): 최근 4분기 SBA 귀속 순이익 약 $984M(EPS 3.47+1.74+1.87+2.19 = 9.27). 회사가 순이익 안에 있다고 밝힌 세후 항목 —
#   이익 쪽: 캐나다 매각 이익 $226.3M(관련 세금 4분기 $36.0M·1분기 $5.8M·2분기 $2.8M을 비용으로) + 환율 이익 $18.1M + 3분기 스왑 지정 해제 이익 $19.0M + 9개월 자산 매각 이익 $16.3M ≈ $244M(24.7%),
#   비용 쪽: 환율 손실 $11.9M, 채무 조기상환 손실 $20.1M, 브라질 세금 $5.1M, 캐나다 세금(1·2분기) $8.6M ≈ $46M(4.6%) → 30% 아래라 정식. 4분기 성격 미확인 기타 이익 약 $45M까지 넣으면 이익 쪽 29.4%(Codex·Fable r1).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, -2), '적정~고평가'
CO = 'SBA'
S_ = 'https://www.sec.gov/Archives/edgar/data/1034054/'
SEC = S_
TENQ = S_ + '000103405426000013/sbac-20260930x10q.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000119312526443666/d185668dex991.htm', 'q2': S_ + '000119312526330639/d154311dex991.htm',
      'q1': S_ + '000119312526191545/d49075dex991.htm', 'q4': S_ + '000119312526076767/d106126dex991.htm',
      'q3old': S_ + '000119312525262644/d94208dex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="sbacFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). 최근 4분기 EPS에는 2025년 4분기 캐나다 사업 매각 이익이 들어 있다 — PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 60)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(타워 신축·개량 — 인수 제외)'
MODEL_NOTE = ('통신 타워 리츠는 업계가 AFFO를 주로 본다 — SBA의 최근 분기 AFFO는 주당 $3.19(1년 전 $3.30)이고, GAAP 순이익과의 차이는 손상·철거비, 비현금 세금, 주식보상 등에서 난다. 이 카드는 다른 카드와 같은 GAAP 배수로 본다. 사이트에는 리츠 전용 평가가 아직 없다. '
              '최근 4분기 순이익 $985M(EPS $9.27)에는 2025년 4분기 캐나다 사업 매각 이익 $226M(관련 세금을 빼면 약 $182M), 환율 재평가 이익, 2026년 3분기 금리스왑 지정 해제 이익 $19M과 자산 매각 이익 $16M(칠레·에콰도르 포함)이 들어 있다 — 세후로 이익 쪽 약 25%, 비용 쪽(채무 조기상환 손실·환율 손실·일회성 세금) 약 5%라 사이트 기준(세후 30%) 아래에서 정식 카드로 둔다. 다만 2025년 4분기 기타 이익 가운데 성격을 확인하지 못한 약 $45M까지 일회성으로 치면 이익 쪽이 약 29%로 기준에 가깝다. 매각 이익을 빼면 EPS는 약 $7.5로 PER이 23배 안팎이고, 헤더의 적정주가 범위도 매각 이익이 든 EPS에 곱한 값이라 그만큼 높게 나온다. '
              '2024년부터 감가상각이 연 $716M(2023년)에서 $270M(2024년)으로 크게 줄어, 영업이익률과 GAAP EPS가 그 해부터 한 단계 올라갔다(영업이익 + 감가상각은 거의 제자리). 그래서 PER·영업이익률의 5년 비교에서 지금이 실제보다 싸고 좋아 보인다 — 자기 이력 점수가 높은 데는 이 효과와 매각 이익, 주가가 2021~2022년 고점보다 많이 내려온 영향이 함께 있다(PSR·PCR·EV/EBITDA도 5년 바닥권). '
              '미국 타워 임대 매출은 Sprint·EchoStar 해지로 1년 전보다 줄었고, 늘어난 쪽은 해외다. 해외 자회사 대여금의 환율 재평가가 분기마다 순이익을 흔든다. 누적 결손으로 주주 자본이 음수(−$4.8B)라 PBR은 해당 없다. 1년 안 만기 차입금 $3.6B는 타워 증권의 예상 상환일이 다가온 몫이다(법적 만기는 2051년) — 11월 무담보 기간 대출 $2.0B와 CP·신용한도로 갚아 간다. 칠레·에콰도르 타워를 팔았고 페루 매각을 약정했다.')
HEALTH_EXTRA = '타워 매입 자금을 채권으로 조달하고 주주 자본이 음수라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 EBITDA 대비로 본다.'
PH = ['AMT', 'CCI', 'EQIX', 'DLR', 'O', 'PLD']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '통신 타워·데이터센터 리츠 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(SBAC 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 통신 타워(AMT·CCI)와 데이터센터 리츠 등 6곳이 보인다.')
SEG = [('미국 타워 임대', 454.4, '#c8102e'), ('해외 타워 임대', 211.0, '#e05a6b'), ('타워 공사(사이트 개발)', 48.6, '#f4c2c8')]
SEG_ADJ = 0
SEG_TITLE = '부문별 매출'
NEWS_RANGE = '2025.11 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 2일 장 마감 뒤 — Q3 2026 실적', '2026-11-03',
     '희석 EPS $2.19 · AFFO 주당 $3.19(1년 전 $3.30) · 칠레·에콰도르 타워 매각, 페루 매각 약정 · CP 프로그램 $2.5B 개설 — 다음 날 주가 −0.1%', 'q3', 'SBA 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 8월 3일 장 마감 뒤 — Q2 2026 실적', '2026-08-04',
     '희석 EPS $1.87 · AFFO 주당 $3.05 · 첫 투자등급 무담보 채권 $3.5B 발행, S&P 등급 BBB로 상향 — 다음 날 주가 +4.7%', 'q2', 'SBA 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 29일 장 마감 뒤 — Q1 2026 실적', '2026-04-30',
     '희석 EPS $1.74 · AFFO 주당 $3.03 · 2026년 전망 전 항목 상향 — 다음 날 주가 +2.4%', 'q1', 'SBA 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 26일 장 마감 뒤 — 2025년 연간 실적', '2026-02-27',
     '4분기 희석 EPS $3.47(캐나다 사업 매각 이익 $226M 포함) · AFFO 주당 $3.19 · 분기 배당 약 13% 인상(주당 $1.25) — 다음 날 주가 +4.7%', 'q4', 'SBA 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 3일 장 마감 뒤 — Q3 2025 실적', '2025-11-04',
     '희석 EPS $2.20 · AFFO 주당 $3.30 · 캐나다 타워 매각 완료(분기 말 뒤), 버라이즌과 장기 임대 계약 — 다음 날 주가 +1.4%', 'q3old', 'SBA 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 22, 'nt': 14, 'mean': 218.07, 'median': 215, 'low': 200, 'high': 256, 'sb': 7, 'b': 4, 'h': 11, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-22'
POST = [r"""
h = h.replace('Q3 2026 10-Q 부문 표 (SEC)', 'Q3 2026 10-Q 부문 주석 (SEC)')
import re as _rs
h = _rs.sub(r'잔존가치\(5년 뒤\)가 내재가치의 ([0-9]+)%', r'잔존가치(5년 뒤)가 영업 기업가치의 \1%', h)
h = h.replace('`잔존가치(5년 뒤)가 내재가치의 ${', '`잔존가치(5년 뒤)가 영업 기업가치의 ${')
h = _rs.sub(r'(Q4 2026 GAAP 영업이익률이 1년 전 같은 분기\(Q4 2025 [0-9.]+%\)보다 높은지)', r'\1(Q4 2025는 손상·철거비 $82M으로 눌린 분기다)', h)
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
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"sbac:DomesticSiteLeasingRevenueMember": ["미국 타워 임대", "#c8102e"],
             "sbac:InternationalSiteLeasingRevenueMember": ["해외 타워 임대", "#e05a6b"],
             "sbac:SiteDevelopmentConstructionMember": ["타워 공사(사이트 개발)", "#f4c2c8"]},
 "ignore": []
}
