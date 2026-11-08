BUILD = {'no_dcf': '미완성 — 일회성 비용 처리 대기'}   # 2026-11-03 사용자 결정 — 미완성 카드(판정 보류)
# GPC(제뉴인 파츠) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 자동차 부품 유통(북미 NAPA·해외)과 산업 부품(Motion — 2027년 1분기 분사 예정, 2026-02-17 발표).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-20), 실적 보도자료(Q4 2025~Q3 2026, 8-K 2.02항 — 장 전 07시 동부 → 같은 날 반응), StockAnalysis. 사전 조사 scratchpad pre/GPC.md.
# 미완성 사유(E54): Q4 2025 연금 정산 손실 등(세전 $1,113M, 주당 −5.94)으로 최근 4분기 GAAP EPS가 0.25(회사 조정 7.54)라 PER이 의미 없다 — 2026-11-03 사용자 결정에 따라 미완성 카드.
# 엔진 입력: 차입금 = 단기(CP 포함) $388M + 1년 안 $250M + 장기 $4,472M = $5,110M(DEBT_TOTAL_TAG — 기본은 CP 이중 합산). 현금은 제한 현금 포함 합계 태그 $763M. 영업이익 태그 없음(2016에 멈춤) → DERIVED_OPINC(세전 − 영업외 손익 합계 = GrossProfit − OperatingExpenses).
# Q4 2025 EPS 보도자료 값. 이자비용은 interest_extra.json(순이자, 2026 10-Q 태그 전환). 리스 $2,134M은 2025-12 10-K 값(차입금은 2026-09). 보류 전 점수: 자기 이력 59.0(PER 빠짐), 동종업 60.9. 리스는 10-K 총액 $2,134M(EV_TAGS_BY_CIK).
CIK = '0000040987'
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Genuine Parts'
S_ = 'https://www.sec.gov/Archives/edgar/data/40987/'
SEC = S_
TENQ = S_ + '000004098726000041/gpc-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000004098726000037/gpc-earnq32026.htm', 'q2': S_ + '000004098726000031/gpc-earnq22026.htm', 'q1': S_ + '000004098726000015/gpc-earnq12026.htm', 'q4': S_ + '000119312526053013/d44894dex991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="gpcFairBand" title="최근 4분기 EPS가 연금 정산 손실로 거의 0이라 PER 구간으로 낸 적정주가가 의미 없어 표시하지 않는다."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 영업이익률 (최근 4분기 {pct(HIST[\'margin_now\'])})</span>'
Y2 = (0, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2025년 4분기 연금 정산 손실(세전, 주당 $5.34) 등으로 최근 4분기 이익이 거의 0이라 PER을 쓸 수 없고, 일회성을 빼면 판정이 크게 달라진다. '
              '산업 부품(Motion)은 2027년 1분기 분사를 목표로 하고 있어(조건부) 그 뒤 실적·주가 기준이 끊긴다. 동종업 점수는 S&P500 경기소비재 기준이다.')
PH = ['AZO', 'ORLY', 'TSCO', 'HD', 'LOW', 'BBY']
PEER_FILE = 'peer_universe/consumer_discretionary.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '자동차 부품·소매 6곳 PER 비교 (점수는 S&P500 경기소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 경기소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 경기소비재 대비 배수 순위 (v2/peer_universe/consumer_discretionary.json)'
PEER_TIP = ('S&P500 경기소비재(GPC 제외)와 배수 순위를 매긴 값이다.',
            '자동차·주택·외식·호텔·소매가 섞여 있다. 차트에는 자동차 부품·소매 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문) — 2,540.3 + 2,408.6 + 1,572.4 = 6,521.3.
SEG = [('북미 자동차', 2540.3, '#0b3b8c'), ('산업 부품(Motion)', 2408.6, '#f2a900'), ('해외 자동차', 1572.4, '#5f6b73')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별(Q3 2026)'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석). 반응일: 장 전 발표(07시 동부) → 같은 날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 20일 장 전 — Q3 2026 실적', '2026-10-20',
     '매출 $6.52B(+4.2%) · 순이익 $224M · 희석 EPS $1.62(1년 전 $1.62) · 조정 EPS $2.07 · 연간 전망 상단 하향 — 당일 주가 −5.1%', 'q3', 'Genuine Parts 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 21일 장 전 — Q2 2026 실적', '2026-07-21',
     '매출 $6.54B(+6.0%) · 순이익 $228M · 희석 EPS $1.65(1년 전 $1.83) · 조정 EPS $2.15 — 당일 주가 −2.7%', 'q2', 'Genuine Parts 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 21일 장 전 — Q1 2026 실적', '2026-04-21',
     '매출 $6.26B(+6.8%) · 순이익 $189M · 희석 EPS $1.37(1년 전 $1.40) · 조정 EPS $1.77 — 당일 주가 +2.1%', 'q1', 'Genuine Parts 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 17일 장 전 — Q4 2025 실적·분사 발표', '2026-02-17',
     '매출 $6.01B(+4.1%) · 순손실 $609M · 희석 EPS −$4.39(연금 정산 손실 포함, 1년 전 $0.96) · 조정 EPS $1.55 · 산업 부문 분사 발표 — 당일 주가 −14.6%', 'q4', 'Genuine Parts 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 11, 'nt': 8, 'mean': 143.75, 'median': 150, 'low': 122, 'high': 170, 'sb': 4, 'b': 1, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# 미완성 카드 표시(2026-11-03 사용자 결정 — C·D·E 보류 카드는 있는 자료로 만들고 판정 보류 + 이유를 잘 보이게, SPCX 방식). BUILD no_dcf가 판정을 보류로 만들고, 보험사용 문구를 미완성 사유로 바꾼다.
INCOMPLETE_SHORT = '일회성 비용 처리 대기'
INCOMPLETE_WHY = '2025년 4분기 연금 정산 손실 등 일회성으로 최근 4분기 EPS가 거의 0이라, 빼고 계산하면 판정이 크게 달라진다 — 일회성 처리 규칙(안건 E54)이 정해질 때까지 보류'
POST = [r"""
_w = '2025년 4분기 연금 정산 손실 등 일회성으로 최근 4분기 EPS가 거의 0이라, 빼고 계산하면 판정이 크게 달라진다 — 일회성 처리 규칙(안건 E54)이 정해질 때까지 보류'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 일회성 비용 처리 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 일회성 비용 처리 대기. 현금흐름 내재가치는 계산하지 않았다.')
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")   # 툴팁이 '계산 불가 — 미완성 — …'로 겹쳤다(Codex 2026-11-03)
"""]


# ── 자동 카드 — 부문(축 하나만 붙은 값). 원문 대조: Q3 2026 2,540.3/2,408.6/1,572.4(2026-11-03) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"gpc:NorthAmericaAutomotiveMember": ["북미 자동차", "#0b3b8c"], "gpc:IndustrialPartsMember": ["산업 부품(Motion)", "#f2a900"], "gpc:InternationalAutomotiveMember": ["해외 자동차", "#5f6b73"]},
 "ignore": []
}
