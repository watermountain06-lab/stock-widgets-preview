# ETR(엔터지) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 루이지애나·텍사스·아칸소·미시시피 전력 공급, 원자력 발전(규제 유틸리티).
# 출처: SEC XBRL + 인라인 XBRL 보충(BUILD overlay — companyfacts에 7/31 Q2 10-Q가 없다), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/ETR.md.
# 엔진 입력(2026-10-28): 차입금 = 단기(CP 포함) $1,570M + 장기(1년 안 포함) $33,058M = $34,627M, 현금 $3,854M, 순이익은 보통주 귀속(연결 NetIncomeLoss가 2023에 멈춤 — EXTRA_TAGS),
# 원자력 해체 신탁 기금($6,722M, LongTermInvestments 안)은 비영업 자산으로 더하지 않는다(INVESTMENTS_OPERATING). 일회성: 최근 4분기 Independence 발전소 손상 주당 0.03(0.8%)뿐.
BUILD = {'overlay': True}
CIK = '0000065984'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, -2), '고평가'
CO = 'Entergy'
S_ = 'https://www.sec.gov/Archives/edgar/data/65984/'
SEC = S_
TENQ = S_ + '000006598426000283/etr-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000006598426000279/earningsrelease2q26_ex991.htm', 'q1': S_ + '000006598426000217/earningsrelease1q26_ex991.htm',
      'q4': S_ + '000006598426000164/earningsrelease4q25_ex991.htm', 'q3': S_ + '000006598425000126/earningsrelease3q25_ex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="etrFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('데이터센터 전력 수요에 맞춘 발전·송전 설비 투자(상반기 $5.0B)가 감가상각보다 훨씬 커서, 큰 차입금을 뺀 현금흐름 모델의 값이 낮게 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '원자력 해체 신탁 기금은 해체 부채 전용이라 주주 몫 자산으로 더하지 않았다. 2024-12 2대1 주식 분할 전 값은 분할 기준으로 맞췄다. 9월 2일 신주 선도 결제로 1,110만 주(+2.4%)를 이미 인도했고(카드 주식 수는 6/30 기준), 1,925만 주 선도 계약이 더 남아 있다. 2023년 4분기 세무 감사 종결 이익(주당 약 2.06)이 든 1년 구간은 PER이 낮게 나와 5년 최저·중앙값을 끌어내린다. '
              'SEC 요약 자료에 최신 10-Q가 아직 없어 원문 인라인 XBRL로 채웠다.')
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
h = _re.sub(r'(id="etrDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="etrDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'SO', 'DUK', 'ED', 'AEE', 'XEL']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(ETR 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
SEG = [('유틸리티', 3513.5, '#00a3e0'), ('모회사·기타', 10.2, '#7fcff0')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07:49~08:32 동부) → 같은 날. Q3 2026 실적은 아직(10-28 기준). 넣지 않은 8-K: 사채·신주 선도 매각, 발전소 리스, 임원, 주총.
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('red', '2026년 7월 29일 장 전 — Q2 2026 실적', '2026-07-29',
     '매출 $3.52B(+5.9%) · 순이익 $483M · 희석 EPS $1.03(1년 전 $1.05) · 2026년 조정 EPS 전망 $4.25~4.45 유지 — 당일 주가 −4.0%', 'q2', 'Entergy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 29일 장 전 — Q1 2026 실적', '2026-04-29',
     '매출 $3.19B · 순이익 $385M · 희석 EPS $0.83(1년 전 $0.82) — Independence 발전소 지분 매각 관련 손상 포함', 'q1', 'Entergy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 12일 장 전 — Q4 2025 실적', '2026-02-12',
     '매출 $2.96B · 순이익 $236M · 희석 EPS $0.51(1년 전 $0.65) · 2025년 EPS $3.91', 'q4', 'Entergy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 29일 장 전 — Q3 2025 실적', '2025-10-29',
     '매출 $3.81B · 순이익 $694M · 희석 EPS $1.53(1년 전 $1.50)', 'q3', 'Entergy 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 24, 'nt': 15, 'mean': 122.43, 'median': 123.5, 'low': 101, 'high': 133, 'sb': 14, 'b': 4, 'h': 5, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 2개(영업 부문 차원). 원문 대조: Q2 2026 3,513.5/10.2(2026-10-28) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"etr:UtilityMember": ["유틸리티", "#00a3e0"], "us-gaap:CorporateAndOtherMember": ["모회사·기타", "#7fcff0"]},
 "ignore": []
}
