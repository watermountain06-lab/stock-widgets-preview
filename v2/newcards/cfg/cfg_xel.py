# XEL(엑셀 에너지) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 182. 규제 전력·가스 유틸리티(미네소타·콜로라도·텍사스·뉴멕시코 등 8개 주).
# 출처: SEC XBRL, Q2 2026 10-Q(2026-07-30 장 마감 뒤 접수), 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 보도자료는 발표일 장 전, 8-K는 전날 밤 접수), 8-K(Marshall 산불 소송 합의 2025-09, 요금 심사), StockAnalysis.
# 엔진 입력(2026-10-23): 매출 = RegulatedAndUnregulatedOperatingRevenue(EXTRA_TAGS·CONCEPTS_BY_CIK — Revenues 태그는 2019-09에 멈춤, NEE와 같은 경우).
# 설비투자(최근 4분기 약 $12.5B)가 영업현금흐름보다 커 FCF가 음수 — PCR 계산 불가. 차입금에 후순위채(하이브리드) 포함.
CIK = '0000072903'
CUR, YO, QO = '2026-06-30', '2025-06-30', '2026-03-31'
QLABEL, YL, QQL = 'Q2 2026', 'Q2 2025', 'Q1 2026'
L8 = ['Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Xcel Energy'
S_ = 'https://www.sec.gov/Archives/edgar/data/72903/'
SEC = S_
TENQ = S_ + '000007290326000154/xel-20260630.htm'; TENQ_NAME = 'Q2 2026 10-Q'
PR = {'q2': S_ + '000007290326000149/xcelearningsreleaseq22026.htm', 'q1': S_ + '000007290326000070/xcelearningsreleaseq12026.htm',
      'q4': S_ + '000007290326000006/xcelearningsreleaseq42025.htm', 'q3': S_ + '000007290325000254/xcelearningsreleaseq32025.htm'}
LINKS = {'mpuc': S_ + '000007290326000175/xel-20261009.htm', 'cpuc': S_ + '000007290326000160/xel-20260819.htm',
         'atm': 'https://www.sec.gov/Archives/edgar/data/72903/000119312526201734/d139315d8k.htm'}
FAIRBAND_TITLE = 'id="xelFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음). 규제 유틸리티 — 설비투자가 커서 FCF가 음수, 현금흐름 모델의 한계.
MODEL_NOTE = ('규제 유틸리티는 승인된 요금으로 투자 원금과 수익을 회수하는 구조라, 설비투자가 영업현금흐름보다 커서 FCF가 음수인 해에도 이익은 늘 수 있다 — 현금흐름 모델과 PCR은 이런 회사에서 의미가 약하고, 세 시나리오가 모두 0 이하라 현재가 요구 성장률도 해석할 수 없다(판정에는 다른 유틸리티 카드처럼 그대로 들어간다). '
              '연료·구매 전력·가스 원가는 요금으로 그대로 넘기므로 원가가 내리면 매출도 줄지만 이익에는 영향이 없다 — 매출 감소를 사업 위축으로 읽으면 안 된다. 차입금에는 후순위채가 들어 있고, 설비투자 자금 일부는 신주(선도 매각)로 조달해 주식 수가 늘고 있다.')
HEALTH_EXTRA = '설비투자 자금을 사채·후순위채·신주로 조달하는 구조라 차입금 비중이 높게 나온다 — 규제 유틸리티에서는 흔한 모습이다.'   # 고정 문장
PH = ['NEE', 'CEG', 'DUK', 'SO', 'AEP', 'D']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(XEL 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q2 2026 10-Q 부문, 부문 간 거래 포함) — 규제 전력 2,741 + 규제 가스 369 = 3,110, 기타·상계 9 → 총매출 3,119.
SEG = [('규제 전력', 2741.0, '#0072ce'), ('규제 가스', 369.0, '#5aa0e0')]
SEG_ADJ = 9.0
SEG_TITLE = '매출 구성 — 부문별'
SEG_ADJ_LABEL = '기타·부문 간 거래'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석 — 회사의 ongoing EPS·가이던스는 쓰지 않는다), 요금 동결안.
# 반응일: 실적 보도자료는 발표일 장 전(8-K는 그 전날 밤 동부 21~23시 접수, UTC 날짜 = 보도자료 날짜) → 같은 날.
# 미네소타 요금 동결안 8-K 2026-10-10T00:50Z = 금요일 10/9 저녁(동부) → 다음 세션 10/12(월).
# 콜로라도 요금 8-K 2026-08-21T00:58Z(8/20 저녁) → 8/21, 주식 판매 약정 8-K 2026-05-02T01:21Z(금 5/1 저녁) → 5/4.
# 넣지 않은 8-K: 사채·후순위채·채권 매입 제안, 이사, 주총, 다른 요금 심사 진행.
NEWS_RANGE = '2025.10 ~ 2026.10'
# 다음 실적: 10/7 회사 공지 — 10/29 장 전.
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-10-29', 'src': '10/7 회사 공지 — 장 시작 전 발표'}
NEWS = [
    ('neutral', '2026년 10월 9일 — 미네소타 전기요금 2년 동결안 제출', '2026-10-12',
     'NSP-미네소타가 예정된 요금 인상 심사 대신 2027~2028년 기본요금 동결안을 제출(배터리 투자 세액공제 조기 인식으로 상쇄)', 'mpuc', 'Xcel Energy 공시 (SEC 8-K)'),
    ('red', '2026년 8월 19일 — 콜로라도 전기요금 결정(구두)', '2026-08-21',
     '콜로라도 규제위원회가 요청 $356M 대신 연 $157M 인상·ROE 9.3%로 합의안 대부분 승인(8-K는 8/20 장 마감 뒤)', 'cpuc', 'Xcel Energy 공시 (SEC 8-K)'),
    ('neutral', '2026년 7월 30일 — Q2 2026 실적', '2026-07-30',
     'GAAP 순이익 $586M · 희석 EPS $0.93(1년 전 $0.75)', 'q2', 'Xcel Energy 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 30일 — Q1 2026 실적', '2026-04-30',
     'GAAP 순이익 $556M · 희석 EPS $0.89(1년 전 $0.84)', 'q1', 'Xcel Energy 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 1일 — 신주 최대 $4.3B 판매 약정(ATM·선도)', '2026-05-04',
     '설비투자 자금용으로 시장가 신주를 최대 $4.3B까지 판매할 수 있는 약정 — 주식 수가 늘어난다(8-K는 금요일 밤 접수)', 'atm', 'Xcel Energy 공시 (SEC 8-K)'),
    ('neutral', '2026년 2월 5일 — Q4 2025 실적', '2026-02-05',
     '2025년 GAAP 순이익 $2.02B · 희석 EPS $3.42(1년 전 $3.44, 산불 합의 비용 포함)', 'q4', 'Xcel Energy 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 30일 — Q3 2025 실적', '2025-10-30',
     'GAAP 순이익 $524M · 희석 EPS $0.88(1년 전 $1.21) — Marshall 산불 소송 합의(총 약 $640M, 보험 약 $350M) 세전 비용 약 $290M 포함', 'q3', 'Xcel Energy 실적 보도자료 (SEC 8-K)'),
]
# DCF가 0 이하일 때 요구 성장률·기본값 표시 보정(Codex·Fable r1) — JS가 실행 때 채우므로 JS 줄을 바꾼다. 일반 처리는 안건 E51
POST = [r'''
_R = '현금흐름 모델 값이 0 이하(FCF 음수)라 현재가 요구 성장률과 기본 시나리오 환산 성장률은 해석할 수 없다.'
_pairs = [
 ("if (req) req.textContent = noSol ? '연 ' + f1(d.requiredGrowth)",
  "if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.title = _XR; } else if (req) req.textContent = noSol ? '연 ' + f1(d.requiredGrowth)"),
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
h = _re.sub(r'(id="xelDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
ANALYST = {'rating': 'Strong Buy', 'n': 19, 'nt': 16, 'mean': 88.69, 'median': 89, 'low': 77, 'high': 97, 'sb': 13, 'b': 4, 'h': 2, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-23'


# ── 자동 카드 — 부문 2개(수동 지도, 부문 간 거래 포함 매출). 원문 대조: Q2 2026 2,741/369(2026-10-23) ──
AUTO = True
SEG_MAP = {
 "concepts": ["xel:RevenuesIncludingIntersegmentRevenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"xel:RegulatedElectricSegmentMember": ["규제 전력", "#0072ce"], "xel:RegulatedNaturalGasSegmentMember": ["규제 가스", "#5aa0e0"]},
 "ignore": []
}
