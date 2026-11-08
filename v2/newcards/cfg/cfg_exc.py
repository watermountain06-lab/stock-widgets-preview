# EXC(엑셀론) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 송배전 전력·가스 공급 — ComEd(시카고)·PECO(필라델피아)·BGE(볼티모어)·Pepco Holdings(워싱턴 DC 일대), 규제 유틸리티.
# 출처: SEC XBRL + 인라인 XBRL 보충(BUILD overlay — companyfacts에 7/30 Q2 10-Q가 없다), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 전 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/EXC.md.
# 엔진 입력(2026-10-28): 차입금 = 단기 + 1년 안 + 장기 + 금융신탁(DEBT_TOTAL_TAG, 엔진 $52,283M — 금융신탁 $390M은 회사 태그라 빠짐, 원문 합계 $52,673M), 현금 $1,813M, 순이익은 보통주 귀속(NetIncomeLoss는 2013에 멈춤 — EXTRA_TAGS).
# 일회성: 최근 4분기 주당 0.06(2.2%, 비용 관리·규제 사안). 2022-02 Constellation 분사로 그 전 이력은 재작성 계속사업 값.
BUILD = {'overlay': True, 'eps_tag': 'IncomeLossFromContinuingOperationsPerDilutedShare,EarningsPerShareDiluted'}   # 2022 분기 EPS는 계속사업 태그에만 있다(분사 해)
CIK = '0001109357'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, -2), '적정~고평가'
CO = 'Exelon'
S_ = 'https://www.sec.gov/Archives/edgar/data/1109357/'
SEC = S_
TENQ = S_ + '000110935726000080/exc-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000110935726000077/exc-20260730ex991.htm', 'q1': S_ + '000110935726000061/exc-20260506ex991.htm',
      'q4': S_ + '000110935726000014/exc-20260212ex991.htm', 'q3': S_ + '000110935725000179/exc-20251104ex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="excFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('송배전망 설비 투자(상반기 $4.6B)가 감가상각보다 훨씬 커서, 큰 차입금을 뺀 현금흐름 모델의 값이 낮게 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '2022년 2월 발전 사업(Constellation)을 분사해 그 전 매출·이익 이력은 재작성된 계속사업 값을 쓰고, EPS 이력은 분사 뒤(2022)부터다. 차입금에는 금융신탁 차입금 $390M(회사 고유 태그)이 빠져 있다. 신주 선도 매각(약 1,840만 주 미결제)과 전환사채가 있어 주식 수가 늘 수 있다. '
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
h = _re.sub(r'(id="excDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="excDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'SO', 'DUK', 'ED', 'AEE', 'XEL']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(EXC 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 부문 간 포함) — ComEd 1,985 + Pepco Holdings 1,712 + BGE 1,218 + PECO 1,062 = 5,977, 본사·기타 471 − 부문 간 481 = −10 → 5,967.
SEG = [('ComEd(시카고)', 1985, '#5f259f'), ('Pepco Holdings(DC 일대)', 1712, '#8a63c2'), ('BGE(볼티모어)', 1218, '#a98bd1'), ('PECO(필라델피아)', 1062, '#f2a900')]
SEG_ADJ = -10
SEG_SUM_LABEL, SEG_ADJ_LABEL = '4개 유틸리티 합', '본사·기타와 부문 간 거래'
SEG_TITLE = '매출 구성 — 유틸리티 자회사별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(06:52~07:00 동부) → 같은 날. Q3 2026 실적은 아직(10-28 기준). 넣지 않은 8-K: 사채·신주 선도 매각, 임원, 주총.
NEWS_RANGE = '2025.11 ~ 2026.07'
NEWS = [
    ('red', '2026년 7월 30일 장 전 — Q2 2026 실적', '2026-07-30',
     '매출 $5.97B(+9.9%) · 순이익 $396M · 희석 EPS $0.39(1년 전 $0.39) · 2026년 조정 EPS 전망 $2.81~2.91 재확인 — 당일 주가 −3.1%', 'q2', 'Exelon 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 6일 장 전 — Q1 2026 실적', '2026-05-06',
     '매출 $7.24B · 순이익 $919M · 희석 EPS $0.90(1년 전 $0.90) — 당일 주가 −2.5%', 'q1', 'Exelon 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 12일 장 전 — Q4 2025 실적', '2026-02-12',
     '매출 $5.41B · 순이익 $593M · 희석 EPS $0.58(1년 전 $0.64) · 2025년 EPS $2.73 — 당일 주가 +7.0%', 'q4', 'Exelon 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 4일 장 전 — Q3 2025 실적', '2025-11-04',
     '매출 $6.71B · 순이익 $875M · 희석 EPS $0.86(1년 전 $0.70)', 'q3', 'Exelon 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 22, 'nt': 15, 'mean': 47, 'median': 46, 'low': 41, 'high': 57, 'sb': 4, 'b': 0, 'h': 17, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 유틸리티 자회사 4개(영업 부문 차원), 본사·기타와 부문 간 거래는 SEG_ADJ. 원문 대조: Q2 2026 1,985/1,712/1,218/1,062(2026-10-28) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"exc:CommonwealthEdisonCoMember": ["ComEd(시카고)", "#5f259f"], "exc:PepcoHoldingsLLCMember": ["Pepco Holdings(DC 일대)", "#8a63c2"],
             "exc:BaltimoreGasAndElectricCompanyMember": ["BGE(볼티모어)", "#a98bd1"], "exc:PECOEnergyCoMember": ["PECO(필라델피아)", "#f2a900"]},
 "ignore": ["exc:PotomacElectricPowerCompanyMember", "exc:DelmarvaPowerandLightCompanyMember", "exc:AtlanticCityElectricCompanyMember", "us-gaap:CorporateAndOtherMember"]
}
