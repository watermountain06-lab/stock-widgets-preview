CIK = '0000864749'
BUILD = {'no_dcf': '미완성 — 2분기 운송·물류(T&L) 영업권 손상으로 최근 4분기 GAAP가 적자'}   # 2026-11-08 사용자 규칙(일회성이 GAAP를 적자로 만들면 미완성)
# TRMB(트림블) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 말 가까운 금요일(2026-01-02). 건설 소프트웨어(AECO)·측위 장비(Field Systems)·운송 물류(T&L).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-04 16:14 동부 장 마감 뒤 → 11-05, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 06:0x~07:0x 동부 → 그날),
#        2026 기한부 대출(2026-10-02 16:08 동부 → 10-05).
# 엔진 입력(2026-11-08): 차입금 $1,533.5M, 현금 $214.5M. 4분기 EPS 2025는 보도자료(Q4_EPS_OVERRIDE — 역산 0.66, 보도자료 0.65). 자본 StockholdersEquity(fetch_financials).
# 일회성(E54): 최근 4분기 GAAP 희석 EPS −0.70(0.65 + 0.42 − 2.02 + 0.25) 대 회사 조정 EPS 3.51(1.00 + 0.79 + 0.86 + 0.86).
#   Q2 2026 T&L 영업권 손상 $562.0M(영업외 비용, 주당 약 $2.4 — 세금 효과 거의 없음) → GAAP를 적자로 만든다. 인수 상각·주식 보상은 반복 비용.
CUR, YO, QO = '2026-10-02', '2025-10-03', '2026-07-03'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2026-01-02', '2025-01-03'), 'FY2025'
VOTES, VERDICT = (1, 1, 0), '판정 보류'
CO = 'Trimble'
S_ = 'https://www.sec.gov/Archives/edgar/data/864749/'
SEC = S_
TENQ = S_ + '000086474926000121/trmb-20261002.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000086474926000119/a2026q3-8kex991.htm', 'q2': S_ + '000086474926000106/a2026q2-8kex991_00version.htm',
      'q1': S_ + '000086474926000061/a2026q1-8kex991.htm', 'q4': S_ + '000086474926000006/a2025q4-8kex991.htm',
      'q3p': S_ + '000086474925000283/a2025q3-8kex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="trmbFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 GAAP가 영업권 손상으로 적자)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 일회성이 최근 4분기 GAAP 이익을 적자로 만들면 판정을 보류하는데, TRMB는 2026년 2분기 운송·물류(T&L) 부문 영업권 손상 $562M(비현금, 주당 약 $2.4)으로 최근 4분기 GAAP 희석 EPS가 −$0.70이다(회사 조정 EPS는 $3.51). '
              '손상은 영업 밖 비용으로 잡혀 영업이익에는 들어 있지 않고, 세금 공제도 되지 않는다. 손상 분기는 2027년 2분기 실적(8월 예상) 때 최근 4분기에서 빠지며, 그때 GAAP 이익과 다른 일회성을 다시 확인해 판정을 재검토한다. 3분기 순이익($59M)이 1년 전($112M)의 절반으로 준 데는 일회성 세무 충당 비용으로 실효세율이 51%까지 오른 영향이 크다(1년 전에는 독일 세율 인하에 따른 이연세 이익이 있었다). '
              '본업은 꾸준하다 — 연간 반복 매출(ARR)이 $2.56B(+11%, 유기 +10%), 3분기 매출 $967M(+7%), 회사 조정 영업이익률 27%대다. 회사는 2026년 매출을 $3.91~3.94B, 조정 EPS를 $3.63~3.69로 제시했다. '
              '다만 11월 4일 실적 날 주가가 17.3% 빠졌다. 공시에 이유는 없고, 그날 바뀐 것은 이렇다 — ARR 증가율이 2분기 +14%에서 +11%(유기 12%→10%)로 낮아졌고, GAAP EPS $0.25가 회사 자체 3분기 전망 $0.39~0.44를 일회성 세금으로 크게 밑돌았으며, 연간 GAAP EPS 전망이 −$0.07~−0.12에서 −$0.49~−0.55로 내려갔고, 연간 조정 전망은 범위만 좁혔다(4분기 조정 EPS $1.13~1.19). 매출·조정 EPS는 회사 전망 범위 안이었다. '
              '4월에 건설 문서 AI 회사 Document Crunch를 $246M에 샀다. 자사주는 연초부터 9개월 동안 $553M어치를 샀고(1분기 $317M·3분기 $232M), 8월에는 옛 한도(잔여 $608M)를 취소하고 새 한도 $1.0B를 승인했다(10월 2일 잔여 $768M). 10월에는 $500M 기한부 대출 한도(2년 만기, 2027년 1월까지 인출)를 새로 열었다. '
              '회사는 이전부터 공시한 재무보고 내부통제의 중대한 약점(전산 일반 통제·매출·세금 통제)을 2027년까지 고치겠다고 밝혔다. 5월 주총 무렵 감사위원장이 바뀌었고, 11월에는 재무 전문가 이사(Tenable CFO Matthew Brown)를 감사위원회에 더했다. '
              '최근 4분기 GAAP가 적자라 PER 숫자는 나오지 않으며, 평가와 평균에서 뺀다.')
PH = ['IBM', 'MSFT', 'ORCL', 'CRM', 'CSCO', 'DELL']   # 카드 가격 비교(multiples_now)가 되는 IT 카드만(IT·GEN과 같은 묶음)
PEER_FILE = None   # IT는 섹터 파일 없이 카드 유니버스 — 비교 차트도 카드 가격
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': 'IT 서비스·소프트웨어·하드웨어 6곳 PER 비교 (점수는 카드 유니버스 IT 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = '카드 유니버스 IT 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = '카드 유니버스 IT 종목 대비 배수 순위'
PEER_TIP = ('카드 유니버스 IT 종목(TRMB 제외)과 배수 순위를 매긴 값이다.',
            '반도체·소프트웨어·하드웨어가 섞여 있다. 차트에는 IT 서비스·소프트웨어·하드웨어 6곳만 보인다(건설·측위 소프트웨어 회사는 비교 가능한 카드가 없다).')
# 매출(Q3 2026 보도자료 부문): 건설 소프트웨어(AECO) 395.0 + 측위 장비(Field Systems) 435.8 + 운송·물류(T&L) 136.0 = 966.8.
SEG = [('측위 장비(Field Systems)', 435.8, '#0063a3'), ('건설 소프트웨어(AECO)', 395.0, '#ffbe00'), ('운송·물류(T&L)', 136.0, '#a9c6e0')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 5건. 반응일: 장 전 → 그날. 색은 사건 성격, 수치는 그날 주가.
NEWS_RANGE = '2025.11 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 4일 장 전 — Q3 2026 실적', '2026-11-04',
     '매출 $967M(+7%) · GAAP 희석 EPS $0.25 · 조정 EPS $0.86 · ARR $2.56B(+11%, 2분기 +14%에서 둔화) · 연간 전망 범위 좁힘 — 그날 주가 −17.3%', 'q3', 'Trimble 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 8월 12일 장 전 — Q2 2026 실적', '2026-08-12',
     '매출 $972M(+11%) · GAAP 희석 EPS −$2.02(T&L 영업권 손상 $562M) · 조정 EPS $0.86 · 연간 전망 상향 · 자사주 매입 한도 $1.0B 새로 승인 — 그날 주가 −2.8%', 'q2', 'Trimble 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 6일 장 전 — Q1 2026 실적', '2026-05-06',
     '매출 $940M(+12%) · GAAP 희석 EPS $0.42 · 조정 EPS $0.79 · 자사주 $317M · 연간 전망 상향 — 그날 주가 −7.2%', 'q1', 'Trimble 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 10일 장 전 — 2025년 연간 실적', '2026-02-10',
     '4분기 매출 $970M(유기 +4%) · GAAP 희석 EPS $0.65 · 조정 EPS $1.00 · ARR $2.39B · 2026년 전망 첫 제시 — 그날 주가 +2.9%', 'q4', 'Trimble 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 5일 장 전 — Q3 2025 실적', '2025-11-05',
     '매출 $901M(유기 +10%) · GAAP 희석 EPS $0.46 · 조정 EPS $0.81 · 연간 전망 상향 — 그날 주가 +2.5%', 'q3p', 'Trimble 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Strong Buy', 'n': 13, 'nt': 9, 'mean': 73.89, 'median': 73, 'low': 60, 'high': 87, 'sb': 10, 'b': 2, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'

# 파이프라인 자동 재판정용 — 일회성이 든 분기(결산일: 항목).
ONEOFF_QUARTERS = {'2026-07-03': '운송·물류(T&L) 영업권 손상 $562.0M(영업외, 주당 약 2.4)'}

# 미완성 카드 표시(2026-11-08 사용자 규칙, D·SRE 방식).
INCOMPLETE_SHORT = '영업권 손상으로 GAAP 적자'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익이 2026년 2분기 운송·물류 영업권 손상($562M)으로 적자다 — 배수 판정이 왜곡돼 보류한다. 판정 재개는 이르면 2027년 8월(2027년 2분기 실적) 뒤'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익이 2026년 2분기 운송·물류 영업권 손상($562M)으로 적자다 — 배수 판정이 왜곡돼 보류한다. 판정 재개는 이르면 2027년 8월(2027년 2분기 실적) 뒤'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 영업권 손상으로 GAAP 적자 · 판정 재개 이르면 2027년 8월</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 영업권 손상으로 GAAP 적자. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="trmbFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">영업권 손상으로 GAAP 적자</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
# 자동 지표 기준으로 비는 Bear 칸에 원문 위험을 적는다(Codex r1)
_be = '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">—</span><span class="bb-text">기준을 넘는 약세 지표가 없다.</span></div>'
assert _be in h
h = h.replace(_be, '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">성장</span><span class="bb-text">연간 반복 매출(ARR) 증가율이 2분기 +14%에서 3분기 +11%로 낮아졌다 — 실적 날 주가 −17.3%.</span></div>\n      <div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">통제</span><span class="bb-text">재무보고 내부통제의 중대한 약점이 남아 있다(2027년 개선 목표).</span></div>', 1)
h = h.replace('Q4 2026 실적 공시.', 'Q4 2026 실적 공시 — 숫자 점검만, 판정 재개는 2027년 2분기 실적 뒤(이르면 8월).', 1)
h = h.replace('순현금 −$1.5B ÷ 0.23B주 · 현금·단기투자 $0.2B − 차입금·리스 $1.7B', '순현금 −$1.5B ÷ 0.23B주(10/30 표지) · 현금·단기투자 $0.2B − 차입금 $1.5B·운용리스 $0.17B(FY2025 말)', 1)
h = h.replace('+ ` − 차입금·리스 ${B(N.debt + N.lease)}`;', '+ ` − 차입금 ${B(N.debt)}·운용리스 ${B(N.lease)}(FY2025 말 값)`;', 1)
"""]

# ── 자동 카드 — 부문 지도(seg_map_propose 뒤 원문 대조). 원문: Q3 2026 보도자료 435.8 + 395.0 + 136.0 = 966.8 ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"trmb:FieldSystemsMember": ["측위 장비(Field Systems)", "#0063a3"],
             "trmb:ArchitectsEngineersConstructionAndOwnersMember": ["건설 소프트웨어(AECO)", "#ffbe00"],
             "trmb:TransportationAndLogisticsMember": ["운송·물류(T&L)", "#a9c6e0"]}
}
