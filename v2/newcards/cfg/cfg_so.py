# SO(서던 컴퍼니) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 201(시총 111위). 미국 남동부 규제 전력(조지아·앨라배마·미시시피)·가스 배전, 서던 파워(발전).
# 요약 자료 누락(사용자 결정 2026-10-24): SEC 요약 자료(companyfacts)에서 Q2가 빠져 Q1 2026까지라 Q1 10-Q(2026-04-30) 기준으로 만든다 — preflight ALLOW_LAGGED, 기준표 2026-04-30.
# Q2 10-Q(7/30)는 요약 자료에 아직 없다. 실리는 날 매일 실행(auto_approve)이 새 분기로 넘겨받는지 시험한다. 자본·비지배지분은 10-K에만 나눠 태깅돼 2025년 말 값($36,016M·$2,851M)이 쓰인다(Q1 원문 $37,122M·$2,790M, 영향 작음 — Codex r1).
# 출처: SEC XBRL, Q1 2026 10-Q, 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 10-Q는 전날 밤 접수, 보도자료·8-K는 발표일, 1시 콜), StockAnalysis. 사전 조사 자료표 scratchpad pre/SO.md.
# 엔진 입력(2026-10-24): 차입금 = 단기 1,673 + 1년 안 5,701 + 장기 67,148 = $74,522M(DEBT_TOTAL_TAG — 1년 안이 빠졌다), 4분기 EPS 2022 보도자료 값.
# 회사가 빼는 항목(풍력 리파워링 가속상각 — 영업이익 안, 부채 상환 손실, Nicor 손실)이 최근 4분기 GAAP EPS를 약 10% 깎는다(PEG와 같은 기준으로 문장 설명).
CIK = '0000092122'
CUR, YO, QO = '2026-03-31', '2025-03-31', '2025-12-31'
QLABEL, YL, QQL = 'Q1 2026', 'Q1 2025', 'Q4 2025'
L8 = ['Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, -1, -2), '고평가'
CO = 'Southern Company'
S_ = 'https://www.sec.gov/Archives/edgar/data/92122/'
SEC = S_
TENQ = S_ + '000009212226000034/so-20260331.htm'; TENQ_NAME = 'Q1 2026 10-Q'
PR = {'q2': S_ + '000009212226000056/ex99-pressreleaseq22026.htm', 'q1': S_ + '000009212226000036/ex99-pressreleaseq12026.htm',
      'q4': S_ + '000009212226000008/ex99-pressreleaseq42025.htm', 'q3': S_ + '000009212225000086/ex99-pressreleaseq32025.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="soFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 35)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('SEC 요약 자료에서 최근 분기가 빠져 있어, 이 카드의 재무는 요약 자료에 실린 마지막 분기 기준이다 — 최신 10-Q는 나왔지만 숫자는 그보다 한두 분기 이전일 수 있다(자료가 돌아오면 자동으로 바뀐다; 실적 뉴스는 발표 기준). 분기 자본·비지배지분은 연말에만 나눠 공시해 그 값을 쓴다. '
              'GAAP 이익에는 풍력 발전 설비 교체에 따른 가속상각(영업이익 안)과 부채 조기 상환 손실 같은 회사 제외 항목이 거의 매 분기 들어 있어, 최근 4분기 합으로 회사 기준 이익보다 낮다. '
              '송배전·발전 설비투자가 영업현금흐름보다 커서 큰 차입금을 뺀 현금흐름 모델의 주당 지분가치가 세 시나리오 모두 0 이하다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. 판정의 현금흐름 표는 0 이하 값에 대한 현행 규칙(−2)이다. '
              '지분 단위(2028년 주식 매입 계약)·전환사채·선도 매각 주식으로 주식 수가 늘 예정이다. 동종업 점수가 판정 문턱 근처라 새 분기가 반영되면 판정이 바뀔 수 있다.')
HEALTH_EXTRA = '설비투자 자금을 사채·후순위채·전환사채·신주로 조달하는 구조라 차입금 비중이 높게 나온다 — 규제 유틸리티에서는 흔한 모습이다.'   # 고정 문장(XEL과 같음)
# 현금흐름 0 이하 문구 보정 — PEG와 같은 POST(안건 E51)
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
h = _re.sub(r'(id="soDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 다음 실적 칸 보정(Fable r1 필수) — 10-Q는 이미 접수됐고, 기다리는 것은 SEC 요약 자료 반영이다
POST.append(r'''
h = h.replace('다음 확인 포인트 · Q2 2026 실적 공시.', '다음 확인 포인트 · SEC 요약 자료의 Q2 반영(나오면 카드가 자동으로 바뀐다)과 Q3 2026 실적.', 1)
h = h.replace('실적 7/30 발표, 보고서 반영 대기', '실적 7/30 발표·10-Q 접수, SEC 요약 자료 반영 대기', 1)
h = h.replace('<span class="op-sub">Q2 2026 · 반영 대기</span>', '<span class="op-sub">Q2 2026 · 요약 자료 반영 대기</span>', 1)
h = h.replace('Q2 2026 실적은 발표됐고 카드는 10-Q·10-K 접수 뒤 반영', 'Q2 2026 실적·10-Q는 나왔고 카드는 SEC 요약 자료에 실린 뒤 반영(다음은 Q3, 10월 말 예상)', 1)
''')
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="soDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'DUK', 'AEP', 'XEL', 'PEG', 'CEG']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(SO 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q1 2026 10-Q 부문) — 전력 회사 5,482 + 서던 파워 681 + 가스 2,191 + 기타 218 = 8,572, 부문 간 거래 −175(전력 −141·기타 −34) → 8,397.
SEG = [('규제 전력 회사', 5482.0, '#1f4e9c'), ('서던 컴퍼니 가스', 2191.0, '#7aa3e0'), ('서던 파워(발전)', 681.0, '#0f2c5e')]
SEG_ADJ = 43.0
SEG_ADJ_LABEL = '기타 218 − 부문 간 거래 175'
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(Q2 2026 포함 — 재무는 Q1 기준, EPS는 GAAP 희석, 회사 기준 EPS·가이던스는 쓰지 않는다). 반응일: 보도자료 발표일(1시 콜, 10-Q 전날 밤·8-K 당일 장중) → 같은 날.
# 넣지 않은 8-K: 전환사채·지분 단위·후순위채 발행, DOE 대출 보증(2/25), ATM(6/8), 정관(10/22).
NEWS_RANGE = '2025.10 ~ 2026.07'
NEWS = [
    ('neutral', '2026년 7월 30일 — Q2 2026 실적(카드 재무는 Q1 기준)', '2026-07-30',
     '매출 $6.98B · 순이익 $1.17B · 희석 EPS $1.03(1년 전 $0.79) — 가속상각 세전 $143M 포함', 'q2', 'Southern 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 30일 — Q1 2026 실적', '2026-04-30',
     '매출 $8.40B · 순이익 $1.36B · 희석 EPS $1.20(1년 전 $1.21) — 가속상각 세전 $154M 포함', 'q1', 'Southern 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 19일 — Q4 2025 실적', '2026-02-19',
     '매출 $6.98B · 순이익 $416M · 희석 EPS $0.38(1년 전 $0.48) · 2025년 희석 EPS $3.92 — 가속상각·부채 상환 손실·Nicor 손실 포함', 'q4', 'Southern 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 30일 — Q3 2025 실적', '2025-10-30',
     '매출 $7.82B · 순이익 $1.71B · 희석 EPS $1.54(1년 전 $1.39)', 'q3', 'Southern 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 24, 'nt': 15, 'mean': 95.77, 'median': 98, 'low': 74, 'high': 106, 'sb': 7, 'b': 1, 'h': 13, 's': 1, 'ss': 2}
ANALYST_ASOF = '2026-10-24'


# ── 자동 카드 — 부문 4개(수동 지도, Revenues), 부문 간 거래는 SEG_ADJ. 원문 대조: Q1 2026 5,482/681/2,191/218/−175(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"so:TraditionalElectricOperatingCompaniesMember": ["규제 전력 회사", "#1f4e9c"], "so:SouthernCompanyGasMember": ["서던 컴퍼니 가스", "#7aa3e0"],
             "so:SouthernPowerMember": ["서던 파워(발전)", "#0f2c5e"]},
 "ignore": []
}
