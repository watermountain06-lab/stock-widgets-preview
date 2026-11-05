# CNP(센터포인트 에너지) v2 카드 설정 — 자동 카드(AUTO). 회계연도 12월 31일. 텍사스(휴스턴) 전력 송배전과 인디애나·오하이오·미네소타·텍사스 천연가스 배관 공급(규제 유틸리티).
# 출처: SEC XBRL + 인라인 XBRL 보충(BUILD overlay — companyfacts에 7/28 Q2·10/27 Q3 10-Q가 없다), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 06시 발표 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/CNP.md.
# 엔진 입력(2026-10-29): 차입금 = 단기 0 + 1년 안 기타 $1,106M + 장기 $23,677M = $24,783M(DEBT_TOTAL_TAG — 기본은 장기만; 1년 안 증권화채 $120M은 회사 고유 태그라 빠짐), 현금 $132M. 단기투자 $425M(ZENS 기초 주식)은 짝인 ZENS 지수부채 파생 $468M이 차입금에 없어 현금성에서 뺀다(EV_TAGS_BY_CIK sti 빈 목록). 매출은 총매출 Revenues 고정(PREFER_TAGS).
# 검토: Codex·Fable r1(2026-10-29) — 필수 데이터 오류 없음(매출 태그·ZENS 고침), 일회성 빼도 자기 이력 26.5·동종업 47.7로 판정 그대로.
# 일회성: 최근 4분기 GAAP 1.75 대 회사 조정 1.94(약 10% — TEEEF 임시 발전 설비 매 분기 0.03, 매각 관련 0.07, ZENS 평가 순 0). Ohio 가스 사업 매각(10/01 완료, $2.62B)은 Q4에 잡힌다.
BUILD = {'overlay': True}
CIK = '0001130310'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, -2), '적정~고평가'
CO = 'CenterPoint Energy'
S_ = 'https://www.sec.gov/Archives/edgar/data/1130310/'
SEC = S_
SEC0 = S_ + '000'   # 보도자료 8-K 중 세 건은 제출 대리인 접수 번호(0001104659-…)
TENQ = S_ + '000113031026000048/cnp-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': SEC0 + '110465926118963/tm2628051d1_ex99-1.htm', 'q2': SEC0 + '110465926087279/tm2621002d1_ex99-1.htm',
      'q1': SEC0 + '110465926047123/tm2612248d1_ex99-1.htm', 'q4': S_ + '000113031026000010/q4earningspressrelease_v.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="cnpFairBand" title="최근 1년 PER 25~75% 구간({FB[\'per_p25\']:.1f}~{FB[\'per_p75\']:.1f}배) × 최근 4분기 희석 EPS ${eps_ttm}(10달러 단위 반올림). PER만으로 낸 범위라 판정과 따로 읽는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = '유틸리티라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
MODEL_NOTE = ('전력망·가스관 설비 투자(9개월 $4.2B, 10년 $70.7B 계획)가 감가상각보다 훨씬 커서, 큰 차입금을 뺀 현금흐름 모델의 값이 낮게 나온다 — 규제 유틸리티는 그 투자가 요금 기준 자산이 되어 이익으로 돌아오는 구조라 현금흐름 모델과 PCR은 의미가 약하다. '
              '오하이오 가스 사업을 10월 1일 $2.62B에 팔아 최근 4분기 매출·이익에는 그 사업이 아직 들어 있다. 교환사채(ZENS) 상환용으로 들고 있는 주식 $425M은 짝인 ZENS 부채($468M)와 함께 움직여 현금에서 뺐다. 주식 선도 매각 약 2,490만 주(약 3.8%)가 아직 미결제라 주식 수가 늘 수 있다. SEC 요약 자료에 최신 10-Q가 아직 없어 원문 인라인 XBRL로 채웠다.')
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
h = _re.sub(r'(id="cnpDcfReq"[^>]*>)연 -[0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
h = _re.sub(r'현재가를 정당화하려면 매출이 5년간 연 [−-][0-9.]+% 커야 한다\. ', '현금흐름 값이 0 이하라 현재가 요구 성장률은 해석할 수 없다. ', h)
''']
# 헤더 '현재가 요구 성장' 칸 — 현금흐름 값이 0 이하이면 숫자 대신 '해석 부적합'(AEE Fable r1, 2026-10-25)
POST.append(r'''
h = h.replace("  if (req && price != null) {", "  if (req && d.base <= 0) { req.textContent = '해석 부적합'; req.style.color = 'var(--text3)'; const _c = req.closest('.meta-item'); if (_c) _c.title = '해석 부적합(현금흐름 0 이하) — 현금흐름 내재가치가 0 이하라 현재가 요구 성장률을 해석할 수 없다.'; }\n  if (req && price != null && d.base > 0) {", 1)
import re as _re2
h = _re2.sub(r'(id="cnpDcfReq"[^>]*>)연 [−-][0-9.]+%', lambda m: m.group(1) + '해석 부적합', h)
''')
PH = ['NEE', 'SO', 'DUK', 'AEP', 'XEL', 'AEE']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(CNP 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스, 독립 발전사, 수도가 섞여 있다. 차트에는 유틸리티 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 전력 1,549 + 천연가스 640 + 본사·기타 2 = 2,191.
SEG = [('전력(휴스턴 송배전 등)', 1549, '#0072ce'), ('천연가스 배관 공급', 640, '#78be20')]
SEG_ADJ = 2
SEG_TITLE = '매출 구성 — 부문별'   # 분기는 fill.py가 실제 값으로 붙인다 — 손으로 적으면 분기를 넘길 때 두 번 나온다(2026-10-30)
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 27일 장 전 — Q3 2026 실적', '2026-10-27',
     '매출 $2.19B(+10.2%) · 순이익 $331M · 희석 EPS $0.50(1년 전 $0.45) · 2026 조정 EPS 전망 1.90~1.92로 상향 — 당일 주가 +1.9%', 'q3', 'CenterPoint 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 28일 장 전 — Q2 2026 실적', '2026-07-28',
     '매출 $2.15B · 순이익 $244M · 희석 EPS $0.37(1년 전 $0.30)', 'q2', 'CenterPoint 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 23일 장 전 — Q1 2026 실적', '2026-04-23',
     '매출 $2.98B · 순이익 $316M · 희석 EPS $0.48(1년 전 $0.45) — 당일 주가 +2.5%', 'q1', 'CenterPoint 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 19일 장 전 — Q4 2025 실적', '2026-02-19',
     '매출 $2.51B · 순이익 $264M · 희석 EPS $0.40(1년 전 $0.38) · 2025년 EPS $1.60', 'q4', 'CenterPoint 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 16, 'mean': 44.13, 'median': 44, 'low': 39, 'high': 49, 'sb': 9, 'b': 1, 'h': 11, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-10-31'


# ── 자동 카드 — 부문 2개(영업 부문, 본사·기타 2는 조정). 원문 대조: Q3 2026 1,549/640(2026-10-29) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"cnp:ElectricSegmentMember": ["전력(휴스턴 송배전 등)", "#0072ce"], "cnp:NaturalGasSegmentMember": ["천연가스 배관 공급", "#78be20"]},
 "ignore": ["us-gaap:CorporateAndOtherMember"]
}
