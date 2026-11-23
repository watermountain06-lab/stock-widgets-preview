CIK = '0001004980'
BUILD = {'overlay': True, 'company_tags': [('pcg:DepreciationAmortizationDecommissioning', 'DepreciationDepletionAndAmortization')]}
# PCG(PG&E) v2 카드 설정 — 자동 카드(AUTO), 정식. 회계연도 12월 31일. 북·중부 캘리포니아 규제 전력·가스(Pacific Gas and Electric Company = Utility) + 지주회사.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-21 20:52 동부 접수 → 첫 세션 10-22, 카드 기준일 11-17 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 저녁 → 다음 날).
# 요약 자료 누락: SEC companyfacts가 Q3 2026 10-Q를 아직 싣지 않아 인라인 XBRL 보충(BUILD overlay, preflight OVERLAY_OK)으로 만든다(SRE·D와 같은 경우).
# 엔진 입력(2026-11-18): 주식 수 = 재무상태표 유통 주식(9월 말 2,202,416,553주) — 표지 2,680,173,293주에는 Utility가 가진 지주 주식 477,743,590주가 들어 있어
#   (EPS에서도 제외) 표지 값을 뺐다(EXCLUDE_TAGS). 순이익 = 보통주 귀속(NetIncomeLoss 2025-12 멈춤 — EXTRA_TAGS). 감가상각 = 회사 고유 태그
#   pcg:DepreciationAmortizationDecommissioning(현금흐름표 "Depreciation, amortization, and decommissioning", company_tags).
#   필수전환우선주 $1,579M은 희석 주식 수에 이미 들어 있고(Q3 희석 2,285M) EV에는 우선주로 더한다. 비지배지분 $252M = Utility 우선주.
# 일회성(E54): 최근 4분기 GAAP 희석 EPS 1.35(0.29 + 0.39 + 0.33 + 0.34) 대 회사 핵심 EPS 1.60(0.36 + 0.43 + 0.40 + 0.41) — 비핵심 세후 $564M
#   (Q4 2025 145 + 2026년 9개월 419) ÷ GAAP 희석 기준 이익 $3,054M(우선주 배당 더함; 기본 보통주 귀속 $2,982M이면 18.9%) = 18.5%, 집계행 기준 이익 항목(파산·법률 −29, SB 901 −3, 세금 −5)을 빼고 비용만 $601M = 19.7%(분기별로 쪼개면 약 19.9%)
#   → 둘 다 30% 미만이라 정식. 가장 큰 항목인 산불 기금 기여 상각(4분기 $323M)은 매 분기 반복된다(2026-11-16 LH 규칙으로도 반복분).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, -2), '적정'
CO = 'PG&E'
S_ = 'https://www.sec.gov/Archives/edgar/data/1004980/'
SEC = S_
TENQ = S_ + '000100498026000055/pcg-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000100498026000056/pge-q32026pressrelease.htm', 'q2': S_ + '000100498026000047/pge-q22026pressrelease.htm',
      'q1': S_ + '000100498026000032/pge-q12026pressrelease.htm', 'q4': S_ + '000100498026000008/pge-q42025pressrelease.htm',
      'sb492': S_ + '000199937126019256/pcg-8k_083126.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="pcgFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(1달러 단위). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('주가는 캘리포니아 산불 책임 제도에 크게 흔들린다. 8월 31일 회사가 새 산불 법안(SB 492)이 자금 조달 위험을 충분히 풀지 못한다고 밝힌 날 주가가 하루 −20% 빠졌고, '
              '9월 2일에는 전략 검토 착수와 2027년 설비투자 $2B 축소(13.4 → 11.4B), 2028~2030년 투자 계획 철회를 알렸다. 이런 제도 위험은 과거 배수와 비교하는 이 카드의 점수에 들어 있지 않다. '
              '회사는 산불 기금 기여 상각·조사 구제·과거 규제 영향 등을 "비핵심"으로 빼서 핵심 EPS를 내는데, 최근 4분기 비핵심은 GAAP 이익의 약 19%이고 가장 큰 산불 기금 상각은 매 분기 나온다 — 카드는 GAAP 그대로 쓴다. '
              '송배전 설비투자가 감가상각보다 훨씬 커서 큰 차입금을 뺀 현금흐름 모델의 값이 낮게 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '표지의 주식 수 26.8억 주에는 자회사(Utility)가 가진 지주 주식 4.78억 주가 들어 있어, 카드는 실제 유통 주식 22.0억 주로 시가총액을 계산한다. 필수전환우선주($1,579M)가 보통주로 바뀌면 주식이 약 4% 늘어난다(희석 EPS에는 이미 반영). 배당은 분기 주당 $0.05다.')
HEALTH_EXTRA = '설비투자 자금을 주로 사채로 조달해 차입금 비중이 높게 나온다(회사는 2030년까지 신주 발행 계획이 없다고 밝혔다). 다만 신용평가사 한 곳은 아직 Utility를 투자등급 아래로 평가하고, 회사는 투자등급 회복을 핵심 목표로 둔다.'
# 현금흐름 0 이하 보정 — ED·SO와 같은 POST
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
h = _re.sub(r'(id="pcgDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="pcgDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
# Codex·Fable r1(2026-11-18): 배당 칸 — 엔진의 주당 배당 태그가 2024년에 멈춰 "없음"으로 나왔다(10-Q 배당 표: 분기 $0.05, 9개월 지급 $330M)
POST.append(r"""
h = h.replace('<span class="zone-label">보통주 배당 지급</span>\n          <span class="zone-val">없음</span>', '<span class="zone-label">보통주 배당 지급</span>\n          <span class="zone-val">$330M(1~9월)</span>', 1)
h = h.replace('>보통주 배당 없음</span>\n            <span class="zone-val">—</span>', '>분기 배당</span>\n            <span class="zone-val">$0.05</span>', 1)
import re as _re4
h = _re4.sub(r'(id="pcgFairBand"[^>]*>)\$20 ~ \$20(<)', r'\1$17 ~ $18\2', h, count=1)   # 엔진은 10달러 단위 반올림 — 12.49~13.55배 × $1.35 = $16.9~18.3
""")
PH = ['EIX', 'SRE', 'NEE', 'DUK', 'SO', 'AEP']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(PCG 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다(EIX·SRE는 같은 캘리포니아). 대부분은 캘리포니아 산불 책임 부담과 투자등급 미달 할인이 없어, PCG의 낮은 배수에는 그 위험을 반영한 할인이 들어 있을 수 있다.')
# 매출(Q3 2026 10-Q 손익계산서): 전력 4,660 + 가스 1,528 = 6,188.
SEG = [('전력', 4660.0, '#0067b1'), ('가스', 1528.0, '#f2a900')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 전력·가스'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석, Q4 2025 포함 — Codex r1) + SB 492 입장 8-K(08-31 08:00 동부 장 전 → 그날). 반응일: 실적 보도자료는 장 마감 뒤 저녁 → 다음 날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 21일 장 마감 뒤 — Q3 2026 실적', '2026-10-22',
     '매출 $6.19B(−1%) · 영업이익 $1.25B(+3%) · 희석 EPS $0.34(1년 전 $0.37) · 핵심 EPS $0.41 · 2026년 핵심 EPS 전망 $1.64~1.66 유지 — 다음 날 주가 −1.3%', 'q3', 'PG&E 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 8월 31일 장 전 — 산불 법안(SB 492)이 부족하다는 입장', '2026-08-31',
     '회사가 SB 492가 산불 책임 제도의 자금 조달 위험을 충분히 풀지 못한다고 밝히고 9월 2일 투자자 설명을 예고 — 당일 주가 −20.1%. 9월 2일 전략 검토·2027년 설비투자 $2B 축소 발표(당일 −5.2%, Q3 10-Q에 기재)', 'sb492', 'PG&E 8-K (SEC)'),
    ('neutral', '2026년 7월 22일 장 마감 뒤 — Q2 2026 실적', '2026-07-23',
     '희석 EPS $0.33(1년 전 $0.24) · 핵심 EPS $0.40 · 6월 Utility 채권 $2.2B 발행 — 다음 날 주가 −3.1%', 'q2', 'PG&E 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 22일 장 마감 뒤 — Q1 2026 실적', '2026-04-23',
     '매출 $6.88B · 희석 EPS $0.39(1년 전 $0.28) · 핵심 EPS $0.43 — 다음 날 주가 −0.3%', 'q1', 'PG&E 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 11일 장 마감 뒤 — Q4 2025 실적', '2026-02-12',
     '매출 $6.80B · 희석 EPS $0.29(1년 전 $0.30) · 2025년 희석 EPS $1.18 · 핵심 EPS $0.36 · 2026년 핵심 EPS 전망 $1.64~1.66 — 다음 날 주가 +2.7%', 'q4', 'PG&E 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 17, 'nt': 15, 'mean': 18.3, 'median': 19, 'low': 14, 'high': 24, 'sb': 7, 'b': 2, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-23'


# ── 자동 카드 — 전력·가스(제품 축). 원문 대조: Q3 2026 4,660/1,528(2026-11-18) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"us-gaap:ElectricityMember": ["전력", "#0067b1"], "us-gaap:NaturalGasUsRegulatedMember": ["가스", "#f2a900"]},
 "ignore": []
}
