CIK = '0001043277'
BUILD = {'no_dcf': '미완성 — RXO 합병 종결 대기'}   # 2026-11-03 사용자 결정(보류 C군 → 미완성 카드), 2026-11-07 제작
# CHRW(C.H. 로빈슨) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 화물 중개(북미 육상 NAST)·국제 포워딩(Global Forwarding).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-30 12:56 동부 장중 → 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — Q4 2025~Q2 2026 16:1x~16:3x 장 마감 뒤 → 다음 거래일, Q3 2026 08:03 장 전 → 같은 날),
#        RXO 합병 8-K(2026-10-05 08:20 장 전).
# 미완성 사유: 2026-10-04 RXO 합병 계약 — RXO 1주당 기본 $17.25 + CHRW 0.0856주(선택: 현금 $30.25 또는 0.1992주, 비례 배분), 2027년 상반기 종결 예상, 특정 해지 사유 시 RXO가 $175M(8-K).
#   CHRW는 인수자라 주가가 묶이지는 않지만 종결 뒤 재무가 이어지지 않는다(보류 C군 사유). Lipe 배심 평결(2026-07-23): 총 $604M(+판결 전 이자 $107M) 중 23% 귀속이나 연대책임 가능,
#   회사는 소액 충당(10-Q), 사고당 보험 $155M. 2026-06-22 DeSpir Logistics 인수(취득현금 차감 후 $77.8M, 작음). 참고 점수 자기 36.7·동종 56.0.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'C.H. Robinson'
S_ = 'https://www.sec.gov/Archives/edgar/data/1043277/'
SEC = S_
TENQ = S_ + '000104327726000043/chrw-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000104327726000039/ex991earningsreleaseq30930.htm', 'q2': S_ + '000104327726000027/ex991earningsreleaseq20630.htm',
      'q1': S_ + '000104327726000014/ex991earningsreleaseq10331.htm', 'q4': S_ + '000104327726000005/ex991earningsreleaseq41231.htm',
      'deal': S_ + '000119312526413203/d115124d8k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="chrwFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(RXO 합병 종결 대기)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 45)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 10월 화물 중개사 RXO를 주식·현금으로 인수하기로 합의했다(RXO 1주당 기본 $17.25 + CHRW 0.0856주, 2027년 상반기 종결 예상). 종결되면 매출·주식 수·차입이 크게 바뀌어 지금 재무로 낸 판정이 이어지지 않으므로 판정을 보류한다 — 자기 이력·동종업 점수는 참고값이다. '
              '2026년 7월 텍사스 배심이 2021년 트럭 사고 소송에서 총 $604M(판결 전 이자 $107M 별도) 손해배상을 평결했다 — 회사 몫은 23%지만 연대책임이 인정되면 전액을 질 수도 있다. 회사는 배상액 전액이 유지될 가능성은 높지 않다고 보고 즉시 항소할 방침이며 소액만 충당금으로 잡았다(사고당 보험 $155M, 자기부담 $5M). '
              '2026년 2~3분기 매출이 크게 늘었지만(+19%·+30%) 주로 트럭·해상·항공 운임 상승 영향이고 3분기는 트럭 물동량 증가도 보탰다 — 매출총이익은 +7%·+15%로 매출보다 덜 늘었다.')
PH = ['EXPD', 'JBHT', 'ODFL', 'UPS', 'FDX', 'UNP']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '물류·운송 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': '물류·운송 PBR 비교', 'psr': '물류·운송 PSR 비교',
                'pcr': '물류·운송 PCR(FCF) 비교', 'evebitda': '물류·운송 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(CHRW 제외)와 배수 순위를 매긴 값이다.',
            '기계·항공·운송·건설·업무 서비스 회사가 섞여 있다. 차트에는 물류·운송 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문): NAST 3,829.2 + Global Forwarding 1,149.1 = 부문 4,978.3, 본사·기타(Robinson Fresh 등) 379.8 → 5,358.1.
SEG = [('북미 육상(NAST)', 3829.2, '#00539b'), ('국제 포워딩', 1149.1, '#4c86c6'), ('기타(Robinson Fresh 등)', 379.8, '#c9c9c9')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 3건(GAAP 희석 EPS) + RXO 합병. 최신 Q3 2026(10-28 장 전)은 news_auto.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 5일 장 전 — RXO 인수 합의(주식 + 현금)', '2026-10-05',
     'RXO 1주당 기본 $17.25 + CHRW 0.0856주 · 2027년 상반기 종결 예상 · 특정 해지 사유 시 RXO가 $175M — 당일 주가 −10.8%', 'deal', 'C.H. Robinson 공시 (SEC 8-K)'),
    ('red', '2026년 7월 29일 장 마감 뒤 — Q2 2026 실적', '2026-07-30',
     '매출 $4.93B(+19.3%) · 순이익 $187M · 희석 EPS $1.56(1년 전 $1.26) — 다음 날 주가 −15.4%', 'q2', 'C.H. Robinson 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 29일 장 마감 뒤 — Q1 2026 실적', '2026-04-30',
     '매출 $4.01B(−0.8%) · 순이익 $147M · 희석 EPS $1.22(1년 전 $1.11) — 다음 날 주가 −2.5%', 'q1', 'C.H. Robinson 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 1월 28일 장 마감 뒤 — Q4 2025 실적', '2026-01-29',
     '매출 $3.91B(−6.5%) · 순이익 $136M · 희석 EPS $1.12(1년 전 $1.22) — 다음 날 주가 +5.1%', 'q4', 'C.H. Robinson 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 23, 'mean': 180.35, 'median': 183, 'low': 91, 'high': 235, 'sb': 14, 'b': 4, 'h': 5, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# 미완성 카드 표시(2026-11-03 사용자 결정, FISV·MLM·NSC·PTC 방식).
INCOMPLETE_SHORT = 'RXO 합병 종결 대기'
INCOMPLETE_WHY = '2026년 10월 RXO를 주식·현금으로 인수하기로 합의했다(2027년 상반기 종결 예상) — 종결되면 매출·주식 수·차입이 크게 바뀌어 지금 재무로 낸 판정이 이어지지 않고, 2026년 7월 배심 평결(최대 $604M + 이자, 회사는 소액만 충당)도 결론이 나지 않았다. 종결 뒤 분기가 쌓이면 다시 본다'
POST = [r"""
import re as _re0
_w = '2026년 10월 RXO를 주식·현금으로 인수하기로 합의했다(2027년 상반기 종결 예상) — 종결되면 매출·주식 수·차입이 크게 바뀌어 지금 재무로 낸 판정이 이어지지 않고, 2026년 7월 배심 평결(최대 $604M + 이자, 회사는 소액만 충당)도 결론이 나지 않았다. 종결 뒤 분기가 쌓이면 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — RXO 합병 종결 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — RXO 합병 종결 대기. 합병 뒤 재무가 크게 바뀌어 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="chrwFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)   # 미완성 — PER 구간 범위를 보이지 않는다(FISV처럼, Codex·Fable r1)
import re as _re3
h = _re3.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re3.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")

h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">RXO 합병 종결 대기</span>', h, count=1)
for _id in ('chrwDcfVerdict', 'chrwDcfBox', 'dcfPickValue'):
    h = h.replace(f'id="{_id}">계산 불가<', f'id="{_id}">보류(미완성)<')

h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)   # 참고 점수를 약점으로 올리지 않는다(Fable r1)
"""]


# ── 자동 카드 — 부문 지도(손 작성). 원문 대조: Q3 2026 10-Q NAST 3,829.2 + 포워딩 1,149.1, 본사·기타 379.8 = 5,358.1(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"chrw:NorthAmericanServiceTransportationNASTMember": ["북미 육상(NAST)", "#00539b"], "chrw:GlobalForwardingMember": ["국제 포워딩", "#4c86c6"]},
 "ignore": [],
 "remainder": ["기타(Robinson Fresh 등)", "#c9c9c9", 0.071]   # 매출 − 두 부문(본사·기타 줄 — Q3 2026 379.8 = 7.1%, 1년 전 384.8)
}
