# PPL(PPL) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 켄터키(LG&E·KU)·펜실베이니아(PPL Electric)·로드아일랜드(Rhode Island Energy) 규제 전력·가스, 부문 3개.
# 출처: SEC XBRL + 인라인 XBRL 보충(BUILD overlay — companyfacts에 8/7 Q2 10-Q가 없다), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 07:4x~07:5x 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/PPL.md.
# 엔진 입력(2026-10-30): 차입금 = 단기 $65M + 1년 안 장기부채 $469M + 장기 $19,789M = $20,323M(DEBT_TOTAL_TAG — 교환사채·지분단위 포함), D&A = 감가상각 + 현금흐름표 상각(DDA_PARTS_BY_CIK), 낡은 단기투자·우선주·비지배지분 제외(EV_TAGS_BY_CIK).
# 2026-10-30 사용자 결정(공시 대기만으로 보류하지 않는다) — Q3 10-Q(11월 초 예상) 전 Q2 기준. 희석 EPS는 계속사업 우선(2021 영국 사업 중단사업), Q4 2022~2025는 보도자료 값(Q4_EPS_OVERRIDE). 자기 이력은 2023-08-04부터(HISTORY_START — EPS 이력 2021~2022 공백·로드아일랜드 인수).
# 일회성: 최근 4분기 GAAP 1.69 대 회사 조정 1.85(약 9.5% — IT 전환·고객 시스템 통합·인수 통합·ISO-NE ROE 환급, 대부분 매 분기 반복되는 규제 비용성).
BUILD = {'overlay': True, 'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # Q2 2026 10-Q 원문 인라인 XBRL 보충, 2021 영국 사업 중단사업 — 계속사업 EPS 우선
CIK = '0000922224'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'PPL'
S_ = 'https://www.sec.gov/Archives/edgar/data/922224/'
SEC = S_
SEC0 = S_ + '000'   # 보도자료 8-K 중 세 건은 제출 대리인 접수 번호(0001104659-…)
TENQ = S_ + '000092222426000044/ppl-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000092222426000042/ppl-6302026exhibit991.htm', 'q1': S_ + '000092222426000024/ppl-3312026exhibit991.htm',
      'q4': S_ + '000092222426000006/ppl-12312025exhibit991.htm', 'q3': S_ + '000092222425000049/ppl-9302025exhibit991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="pplFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('전력망·발전 설비 투자(상반기 $2.3B)가 감가상각보다 훨씬 커서, 큰 차입금(약 $20.3B)을 뺀 현금흐름 모델의 값이 0 아래로 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '2025-11 교환사채 $1.15B와 2026-02 지분단위(후순위채 + 주식 매입 계약)를 발행해 주식 수가 늘 수 있다. 2022-05 로드아일랜드 인수로 5년 매출 성장률이 높게 나온다. Q2 10-Q가 SEC 요약 자료에 아직 없어 원문 인라인 XBRL로 채웠다.')
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
h = _re.sub(r'(id="pplDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="pplDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'SO', 'DUK', 'AEP', 'XEL', 'AEE']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(PPL 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문) — 켄터키 888 + 펜실베이니아 744 + 로드아일랜드 479 = 2,111(본사 0).
SEG = [('켄터키 규제', 888, '#003a70'), ('펜실베이니아 규제', 744, '#f6a01a'), ('로드아일랜드 규제', 479, '#5b9bd5')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q2 2026)'
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 7일 장 전 — Q2 2026 실적', '2026-08-07',
     '매출 $2.11B(+4.2%) · 순이익 $230M · 희석 EPS $0.30(1년 전 $0.25) · 조정 EPS $0.33 · 2026 조정 EPS 전망 1.90~1.98 유지 — 당일 주가 +2.4%', 'q2', 'PPL 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 8일 장 전 — Q1 2026 실적', '2026-05-08',
     '매출 $2.77B(+10.8%) · 순이익 $452M · 희석 EPS $0.60(1년 전 $0.56) — ISO-NE ROE 환급 등 주당 $0.03 포함 — 당일 주가 −2.3%', 'q1', 'PPL 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 20일 장 전 — Q4 2025 실적', '2026-02-20',
     '매출 $2.27B · 순이익 $266M · 희석 EPS $0.36(1년 전 $0.24) · 2025년 EPS $1.59 — 당일 주가 +1.3%', 'q4', 'PPL 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 5일 장 전 — Q3 2025 실적', '2025-11-05',
     '매출 $2.24B · 순이익 $318M · 희석 EPS $0.43(1년 전 $0.29) — 당일 주가 +0.3%', 'q3', 'PPL 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 19, 'nt': 16, 'mean': 40.06, 'median': 41, 'low': 35, 'high': 44, 'sb': 11, 'b': 4, 'h': 4, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-30'


# ── 자동 카드 — 원문 대조: Q2 2026 888/744/479(2026-10-30) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"ppl:KentuckyRegulatedMember": ["켄터키 규제", "#003a70"], "ppl:PennsylvaniaRegulatedMember": ["펜실베이니아 규제", "#f6a01a"], "ppl:RhodeIslandRegulatedMember": ["로드아일랜드 규제", "#5b9bd5"]},
 "ignore": ["ppl:TotalSegmentsMember", "ppl:CorporateMember"]
}
