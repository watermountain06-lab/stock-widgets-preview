# ED(콘솔리데이티드 에디슨) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 203(시총 255위). 뉴욕시·웨스트체스터 전력·가스·증기 배전(CECONY), 오렌지 앤 록랜드(O&R).
# 요약 자료 누락(사용자 결정 2026-10-24): SEC 요약 자료(companyfacts)에서 Q2가 빠져 Q1 2026 10-Q(2026-05-07) 기준 — preflight ALLOW_LAGGED, 기준표 2026-05-07.
# 출처: SEC XBRL, Q1 2026 10-Q, 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 장 마감 뒤 10-Q와 함께), StockAnalysis. 사전 조사 자료표 scratchpad pre/ED.md.
# 엔진 입력(2026-10-24): 차입금 = CP 869 + 1년 안 250 + 장기 25,554 = $26,673M(DEBT_TOTAL_TAG — 장기를 분기에 LongTermDebtFairValue로 낸다), 설비투자 = PaymentsForConstructionInProcess(EXTRA_TAGS — 기본 2019 멈춤),
# 매출 = Revenues(EXCLUDE_TAGS 고객 계약 매출), 4분기 EPS 2025 보도자료 값. Q1 2026 EPS에 MVP 지분 매각 이익(세후 $134M, EPS $0.37 — 영업이익 밖, 최근 4분기 EPS의 약 6%).
CIK = '0001047862'
CUR, YO, QO = '2026-03-31', '2025-03-31', '2025-12-31'
QLABEL, YL, QQL = 'Q1 2026', 'Q1 2025', 'Q4 2025'
L8 = ['Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 1, -2), '적정~고평가'
CO = 'Con Edison'
S_ = 'https://www.sec.gov/Archives/edgar/data/1047862/'
SEC = S_
TENQ = S_ + '000104786226000091/ed-20260331.htm'; TENQ_NAME = 'Q1 2026 10-Q'
PR = {'q2': S_ + '000104786226000143/ed-20260630xexx991.htm', 'q1': S_ + '000104786226000092/ed-20260331xexx991.htm',
      'q4': S_ + '000104786226000028/ed-20251231xexx991.htm', 'q3': S_ + '000104786225000139/ed-2025930xexx991jp.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="edFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('SEC 요약 자료에서 최근 분기가 빠져 있어, 이 카드의 재무는 요약 자료에 실린 마지막 분기 기준이다 — 최신 10-Q는 나왔지만 숫자는 그보다 한두 분기 이전일 수 있다(자료가 돌아오면 자동으로 바뀐다; 실적 뉴스는 발표 기준). '
              'Q1 2026 GAAP 이익에는 천연가스관(MVP) 지분 매각 이익이 영업이익 밖에 들어 있어 최근 4분기 PER이 그만큼 낮게 나온다. 난방 수요 때문에 겨울이 낀 1분기 이익이 가장 크다. '
              '송배전 설비투자가 감가상각보다 훨씬 커서 큰 차입금을 뺀 현금흐름 모델의 값이 낮게 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '신주 발행 프로그램으로 주식 수가 늘 수 있다.')
HEALTH_EXTRA = '설비투자 자금을 사채·신주로 조달하는 구조라 차입금 비중이 높게 나온다 — 규제 유틸리티에서는 흔한 모습이다.'   # 고정 문장(XEL과 같음)
# 현금흐름 0 이하·다음 실적 칸 보정 — SO와 같은 POST(0 이하가 아니면 해당 줄은 바뀌지 않는다)
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
h = _re.sub(r'(id="edDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 다음 실적 칸 보정(Fable r1 필수) — 10-Q는 이미 접수됐고, 기다리는 것은 SEC 요약 자료 반영이다
POST.append(r'''
h = h.replace('다음 확인 포인트 · Q2 2026 실적 공시.', '다음 확인 포인트 · SEC 요약 자료의 Q2 반영(나오면 카드가 자동으로 바뀐다)과 Q3 2026 실적.', 1)
h = h.replace('실적 8/6 발표, 보고서 반영 대기', '실적 8/6 발표·10-Q 접수, SEC 요약 자료 반영 대기', 1)
h = h.replace('<span class="op-sub">Q2 2026 · 반영 대기</span>', '<span class="op-sub">Q2 2026 · 요약 자료 반영 대기</span>', 1)
h = h.replace('Q2 2026 실적은 발표됐고 카드는 10-Q·10-K 접수 뒤 반영', 'Q2 2026 실적·10-Q는 나왔고 카드는 SEC 요약 자료에 실린 뒤 반영(다음은 Q3, 11월 초 예상)', 1)
''')
# 배당 칸 보정(Codex r1 필수) — 지급 기준 마지막 값이 Q3 2025다
POST.append(r'''
h = h.replace('최근 분기 주당 배당 (지급 기준, 9/30 분기)', '주당 배당 (지급 기준 마지막 값 — Q3 2025, Q1 2026 선언은 $0.89)', 1)
''')
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="edDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'SO', 'DUK', 'AEP', 'XEL', 'PEG']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(ED 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q1 2026 10-Q 주석 M, 법인별) — CECONY 4,654(전력 2,758·가스 1,464·증기 432, 내부 −27) + O&R 441 = 5,095, 송전·기타 0.
SEG = [('CECONY(뉴욕시)', 4654.0, '#0078c1'), ('O&R', 441.0, '#7fbce6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 자회사별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 주당 배당 칸은 CommonStockDividendsPerShareDeclared가 없어 지급 기준 마지막 값(Q3 2025 $0.85)에 멈춘다 — Q1 2026 선언 $0.89(Fable r1 권장, 엔진 공통).
# 손 뉴스: 실적 4건(Q2 2026 포함 — 재무는 Q1 기준, EPS는 GAAP 희석, 회사 기준 EPS·가이던스는 쓰지 않는다). 반응일: 보도자료·8-K 장 마감 뒤 → 다음 거래일.
# 넣지 않은 8-K: 요금 합의(2025-11·2026-09), 사채·텀론·선도 매각·ATM·신용 한도, MVP 매각 계약(2025-11-24, 금액 작음 — Q1 뉴스에), 임원·주총.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 6일 — Q2 2026 실적(카드 재무는 Q1 기준)', '2026-08-07',
     '매출 $4.07B · 순이익 $308M · 희석 EPS $0.83(1년 전 $0.68)', 'q2', 'Con Edison 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 7일 — Q1 2026 실적', '2026-05-08',
     '매출 $5.10B · 순이익 $924M · 희석 EPS $2.54(1년 전 $2.25) — MVP 지분 매각 이익 세후 $134M(EPS $0.37) 포함', 'q1', 'Con Edison 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 19일 — Q4 2025 실적', '2026-02-20',
     '매출 $4.00B · 순이익 $297M · 희석 EPS $0.82(1년 전 $0.89) · 2025년 희석 EPS $5.64', 'q4', 'Con Edison 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 6일 — Q3 2025 실적', '2025-11-07',
     '매출 $4.53B · 순이익 $688M · 희석 EPS $1.90(1년 전 $1.69)', 'q3', 'Con Edison 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 19, 'nt': 14, 'mean': 108, 'median': 109, 'low': 87, 'high': 130, 'sb': 3, 'b': 0, 'h': 9, 's': 4, 'ss': 3}
ANALYST_ASOF = '2026-10-31'


# ── 자동 카드 — 자회사 2개(수동 지도, 법인 축). 원문 대조: Q1 2026 4,654/441(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "dei:LegalEntityAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"ed:ConsolidatedEdisonCompanyofNewYorkInc.Member": ["CECONY(뉴욕시)", "#0078c1"], "ed:OrangeAndRocklandUtilitiesIncMember": ["O&R", "#7fbce6"]},
 "ignore": []
}
