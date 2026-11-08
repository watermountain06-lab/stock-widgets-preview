# DUK(듀크 에너지) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 카드 순위 202(시총 116위). 미국 남동부·중서부 규제 전력(캐롤라이나·플로리다·인디애나·오하이오·켄터키)·가스 배전.
# 요약 자료 누락(사용자 결정 2026-10-24): SEC 요약 자료(companyfacts)에서 Q2가 빠져 Q1 2026 10-Q(2026-05-05) 기준 — preflight ALLOW_LAGGED, 기준표 2026-05-05.
# 출처: SEC XBRL, Q1 2026 10-Q, 실적 보도자료(Q3 2025~Q2 2026, 8-K 2.02항 — 전날 밤 접수, 발표일 10시 콜), 8-K(플로리다 지분 매각 3/3, 테네시 가스 매각 4/1), StockAnalysis. 사전 조사 자료표 scratchpad pre/DUK.md.
# 엔진 입력(2026-10-24): 매출 = RegulatedAndUnregulatedOperatingRevenue(EXTRA_TAGS + EXCLUDE_TAGS — Revenues 2017 멈춤, 고객 계약 매출 태그는 대체 매출 빠짐), 차입금 $90,245M(엔진 기본값 = 원문, 폭풍 복구 채권 등 VIE 포함),
# 비지배지분 $2,021M(브룩필드 플로리다 지분 포함). 우선주 $973M(장부, 청산 $1.0B)는 태그가 없어 빠진다(EV의 약 1%). 4분기 EPS 2021·2023·2025 보도자료 값, 2022는 재작성 값.
# Q1 2026 영업이익에 테네시 가스 매각 이익 세전 $384M(영업이익의 14%)이 있으나 EPS에서는 규제 정산 비용과 거의 상쇄된다.
CIK = '0001326160'
CUR, YO, QO = '2026-03-31', '2025-03-31', '2025-12-31'
QLABEL, YL, QQL = 'Q1 2026', 'Q1 2025', 'Q4 2025'
L8 = ['Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'Duke Energy'
S_ = 'https://www.sec.gov/Archives/edgar/data/1326160/'
SEC = S_
TENQ = S_ + '000132616026000026/duk-20260331.htm'; TENQ_NAME = 'Q1 2026 10-Q'
PR = {'q2': S_ + '000132616026000037/er-20260630xearningsreleas.htm', 'q1': S_ + '000132616026000022/er-20260331xearningsreleas.htm',
      'q4': S_ + '000132616026000007/er-20251231xearningsreleas.htm', 'q3': S_ + '000132616025000190/er-20250930xearningsreleas.htm'}
NEXT_CONFIRMED = {'quarter_end': '2026-09-30', 'date': '2026-11-05', 'src': '회사 공지 — 11/5 오전 7시(동부) 발표(Codex r1)'}
LINKS = {'tn': S_ + '000110465926038007/tm2610676d1_8k.htm', 'fl': S_ + '000110465926022610/tm267351d1_8k.htm'}
FAIRBAND_TITLE = 'id="dukFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 35)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
# 고정 문장(숫자 없음).
MODEL_NOTE = ('SEC 요약 자료에서 최근 분기가 빠져 있어, 이 카드의 재무는 요약 자료에 실린 마지막 분기 기준이다 — 최신 10-Q는 나왔지만 숫자는 그보다 한두 분기 이전일 수 있다(자료가 돌아오면 자동으로 바뀐다; 실적 뉴스는 발표 기준). '
              '2026년 1분기에 테네시 가스 사업을 팔고(세전 이익이 Q1 영업이익의 약 14%) 플로리다 전력 자회사 지분 일부를 Brookfield에 넘겨, 영업이익에 매각 이익이 들어갔고(EPS에서는 규제 정산 비용과 거의 상쇄) 앞으로 플로리다 이익의 일부가 비지배지분으로 간다. '
              '송배전·발전 설비투자가 영업현금흐름보다 커서 큰 차입금을 뺀 현금흐름 모델의 주당 지분가치가 세 시나리오 모두 0 이하다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. 판정의 현금흐름 표는 0 이하 값에 대한 현행 규칙(−2)이다. '
              '우선주(장부 약 $1.0B)는 최근 태그가 없어 계산에서 빠진다. 신주 발행 프로그램·지분 단위·전환사채로 주식 수가 늘 예정이다.')
HEALTH_EXTRA = '설비투자 자금을 사채·전환사채·신주로 조달하는 구조라 차입금 비중이 높게 나온다 — 규제 유틸리티에서는 흔한 모습이다.'   # 고정 문장(XEL과 같음)
# 현금흐름 0 이하·다음 실적 칸 보정 — SO와 같은 POST
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
h = _re.sub(r'(id="dukDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 다음 실적 칸 보정(Fable r1 필수) — 10-Q는 이미 접수됐고, 기다리는 것은 SEC 요약 자료 반영이다
POST.append(r'''
h = h.replace('다음 확인 포인트 · Q2 2026 실적 공시.', '다음 확인 포인트 · SEC 요약 자료의 Q2 반영(나오면 카드가 자동으로 바뀐다)과 Q3 2026 실적.', 1)
h = h.replace('실적 8/4 발표, 보고서 반영 대기', '실적 8/4 발표·10-Q 접수, SEC 요약 자료 반영 대기', 1)
h = h.replace('<span class="op-sub">Q2 2026 · 반영 대기</span>', '<span class="op-sub">Q2 2026 · 요약 자료 반영 대기</span>', 1)
h = h.replace('Q2 2026 실적은 발표됐고 카드는 10-Q·10-K 접수 뒤 반영', 'Q2 2026 실적·10-Q는 나왔고 카드는 SEC 요약 자료에 실린 뒤 반영(다음은 Q3, 10월 말 예상)', 1)
''')
# 확정 일정(11/5 Q3) — 위 POST 뒤에 돌아야 그 문구를 고칠 수 있다(Codex r2·r3)
POST.append(r'''
h = h.replace('(다음은 Q3, 10월 말 예상)', '(다음은 Q3 — 11월 5일 오전 7시(동부) 발표, 회사 공지)', 1)
h = h.replace('<div class="stat-value">8월 4일 발표됨</div>', '<div class="stat-value">11월 5일(Q3) · Q2는 8월 4일 발표됨</div>', 1)
h = h.replace('<span class="op-val">8월 4일 발표됨 <span class="op-sub">Q2 2026 · 요약 자료 반영 대기</span></span>', '<span class="op-val">11월 5일(Q3) <span class="op-sub">Q2는 8월 4일 발표 · 요약 자료 반영 대기</span></span>', 1)
''')
PH = ['NEE', 'SO', 'AEP', 'XEL', 'PEG', 'CEG']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(DUK 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q1 2026 10-Q 부문) — 전력·인프라 7,878 + 가스·인프라 1,333 = 9,211, 기타 42 − 부문 간 거래 75 → 9,178.
SEG = [('전력·인프라', 7878.0, '#00a1de'), ('가스·인프라', 1333.0, '#7fcdf0')]
SEG_ADJ = -33.0
SEG_ADJ_LABEL = '기타 42 − 부문 간 거래 75'
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
# 손 뉴스: 실적 4건(Q2 2026 포함 — 재무는 Q1 기준, EPS는 GAAP 희석, 회사 기준 EPS·가이던스는 쓰지 않는다) + 매각 2건. 반응일: 실적 8-K는 전날 밤 접수·발표일 장 전 → 발표일.
# 플로리다 지분 8-K 3/3 19:48Z(장 마감 전) → 3/3, 테네시 매각 8-K 4/1 03:37Z(전날 밤) → 4/1.
# 넣지 않은 8-K: 사채·전환사채·지분 단위(8/13)·ATM, 요금 정산(7.01), 이사·주총.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('neutral', '2026년 8월 4일 — Q2 2026 실적(카드 재무는 Q1 기준)', '2026-08-04',
     '매출 $7.59B · 보통주 순이익 $1.08B · 희석 EPS $1.38(1년 전 $1.25) — 규제 정산 비용 포함', 'q2', 'Duke 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 5일 — Q1 2026 실적', '2026-05-05',
     '매출 $9.18B · 보통주 순이익 $1.54B · 희석 EPS $1.97(1년 전 $1.76) — 자산 매각 이익(EPS +$0.22)과 규제 정산 비용(−$0.19) 포함', 'q1', 'Duke 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 31일 — 테네시 가스 사업(Piedmont) 매각 완료', '2026-04-01',
     'Spire에 현금 $2.48B — 세전 이익 $368M(Q1)', 'tn', 'Duke 공시 (SEC 8-K)'),
    ('neutral', '2026년 3월 3일 — 플로리다 전력 지분 9.2% Brookfield에', '2026-03-03',
     '약 $2.8B — 2028년까지 19.7%(총 약 $6B)로 늘어나는 계약', 'fl', 'Duke 공시 (SEC 8-K)'),
    ('green', '2026년 2월 10일 — Q4 2025 실적', '2026-02-10',
     '매출 $7.94B · 보통주 순이익 $1.17B · 희석 EPS $1.50(1년 전 $1.54) · 2025년 희석 EPS $6.31', 'q4', 'Duke 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 11월 7일 — Q3 2025 실적', '2025-11-07',
     '매출 $8.54B · 보통주 순이익 $1.41B · 희석 EPS $1.81(1년 전 $1.60)', 'q3', 'Duke 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 15, 'mean': 132.6, 'median': 130, 'low': 123, 'high': 146, 'sb': 9, 'b': 2, 'h': 12, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# ── 자동 카드 — 부문 2개(수동 지도, RegulatedAndUnregulatedOperatingRevenue), 기타·부문 간 거래는 SEG_ADJ. 원문 대조: Q1 2026 7,878/1,333/42/−75(2026-10-24) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RegulatedAndUnregulatedOperatingRevenue"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"duk:ElectricUtilitiesandInfrastructureMember": ["전력·인프라", "#00a1de"], "duk:GasUtilitiesandInfrastructureMember": ["가스·인프라", "#7fcdf0"]},
 "ignore": []
}
