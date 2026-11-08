# AEP(아메리칸 일렉트릭 파워) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 미국 11개 주 전력 공급·송배전, 미국 최대 송전망(규제 유틸리티).
# 출처: SEC XBRL + 인라인 XBRL 보충(BUILD overlay — companyfacts에 7/30 Q2·10/28 Q3 10-Q가 없다), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 07시 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/AEP_q3.md.
# 엔진 입력(2026-10-28): 차입금 = 단기(유동화 900 + CP 등) + 장기(1년 안 포함) = $54,416M(DEBT_TOTAL_TAG — 기본은 CP를 한 번 더 셌다), 설비투자 = 공사 지출만(발전소 인수 9개월 $2.4B는 태그가 2023-12부터라 빼고 설명에 밝힌다 — 합산하면 그 전 이력이 사라졌다),
# 감가상각 = 유틸리티 비용 태그(DDA_PARTS_BY_CIK — 합산 태그 분기 행이 2011년에 멈춤), 순이익 = 보통주 귀속(NetIncomeLoss 없음). 일회성: 최근 4분기 주당 순 −0.23(3.6%, 소프트웨어 손상·평가손익 등).
BUILD = {'overlay': True}
CIK = '0000004904'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 0, -2), '고평가'
CO = 'AEP'
S_ = 'https://www.sec.gov/Archives/edgar/data/4904/'
SEC = S_
TENQ = S_ + '000000490426000072/aep-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000000490426000069/a3q20268kpressreleaseex991.htm', 'q2': S_ + '000000490426000055/a2q20268kpressreleaseex991.htm',
      'q1': S_ + '000000490426000031/a1q20268kpressreleaseex991.htm', 'q4': S_ + '000000490426000011/a4q20258kpressreleaseex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="aepFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('데이터센터 전력 수요에 맞춘 송전·발전 투자(9개월 $11.5B, 2027~2031 $100B 계획)가 감가상각보다 훨씬 커서, 큰 차입금을 뺀 현금흐름 모델의 값이 낮게 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '설비투자에는 공사 지출만 넣었다 — 발전소 인수(9개월 $2.4B)는 빠져 있어 실제 투자는 더 크다. 매출은 손익계산서 총매출 기준이다. 신주 선도 매각 약 4,800만 주(약 8.8%)가 아직 미결제라 주식 수가 늘 수 있다. SEC 요약 자료에 최신 10-Q가 아직 없어 원문 인라인 XBRL로 채웠다.')
HEALTH_EXTRA = '설비투자 자금을 사채·신주로 조달하는 구조라 차입금 비중이 높게 나온다 — 규제 유틸리티에서는 흔한 모습이다.'
# 현금흐름 0 이하 — SO·ATO와 같은 문구 보정(0 이하가 아니면 바뀌지 않는다)
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
h = _re.sub(r'(id="aepDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="aepDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'SO', 'DUK', 'ED', 'AEE', 'XEL']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(AEP 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문, 외부 매출) — 수직통합 유틸리티 3,923 + 송배전 회사 1,853 + 발전·마케팅 922 + 송전 운영 133 + 본사 1 = 6,832.
SEG = [('수직통합 유틸리티', 3923, '#0067b1'), ('송배전 회사', 1853, '#6aa9dc'), ('발전·마케팅', 922, '#f2a900'), ('송전 운영', 133, '#9bb8d3')]
SEG_ADJ = 1
SEG_TITLE = '매출 구성 — 부문별(외부 매출)'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 28일 장 전 — Q3 2026 실적', '2026-10-28',
     '매출 $6.83B(+13.7%) · 순이익 $1.19B · 희석 EPS $2.16(1년 전 $1.81) · 2027~2031 $100B 투자 계획, 조정 EPS 연 9~11% 성장 전망', 'q3', 'AEP 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 30일 장 전 — Q2 2026 실적', '2026-07-30',
     '매출 $5.45B · 순이익 $713M · 희석 EPS $1.30(1년 전 $2.29 — 규제 결정 일회성 이익)', 'q2', 'AEP 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 5일 장 전 — Q1 2026 실적', '2026-05-05',
     '매출 $6.02B · 순이익 $874M · 희석 EPS $1.60(1년 전 $1.50)', 'q1', 'AEP 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 12일 장 전 — Q4 2025 실적', '2026-02-12',
     '매출 $5.31B · 순이익 $582M · 2025년 희석 EPS $6.66 — 소프트웨어 손상 포함, 당일 주가 +3.4%', 'q4', 'AEP 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 19, 'mean': 140.49, 'median': 140.5, 'low': 126, 'high': 153, 'sb': 13, 'b': 3, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 4개(외부 매출 — 관계사 축 NonrelatedPartyMember + 영업 부문). 원문 대조: Q3 2026 3,923/1,853/922/133(2026-10-28) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember", "us-gaap:RelatedPartyTransactionsByRelatedPartyAxis": "us-gaap:NonrelatedPartyMember"},
 "members": {"aep:VerticallyIntegratedUtilitiesSegmentMember": ["수직통합 유틸리티", "#0067b1"], "aep:TransmissionAndDistributionCompaniesMember": ["송배전 회사", "#6aa9dc"],
             "aep:GenerationAndMarketingMember": ["발전·마케팅", "#f2a900"], "aep:TransmissionOperationsMember": ["송전 운영", "#9bb8d3"]},
 "ignore": ["aep:AEPTransmissionHoldcoMember"]
}
