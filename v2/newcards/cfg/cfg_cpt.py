CIK = '0000906345'
BUILD = {'no_dcf': '미완성 — 최근 4분기 순이익보다 부동산 매각 이익이 크다', 'company_tags': [('cpt:GainOnAcquisitionOfUnconsolidatedJointVentureInterests', 'JvAcquisitionGainCpt', '2021-01-01')]}
# CPT(캠든 프로퍼티 트러스트) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 리츠(REIT) — 미국 남부(선벨트) 임대 아파트.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-06 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 → 다음 세션).
# 엔진 입력(2026-11-21): 매출 = 부동산 수익(OperatingLeaseLeaseIncome — 매출 합계 줄 없음, 관리 수수료는 영업외), 영업이익 = 세전이익 + 이자 − 매각 이익 − 투자 이익 − 2022년 합작 지분 인수 재평가 이익(DERIVED_OPINC),
#   순이익 = 보통주 귀속, 설비투자 = 개발·개량(토지 포함, 한 줄 — 인수 제외), 차입금 = LongTermDebt $4,228.3M(무담보 $3,921.5M + 담보 $306.8M, 9월 말 CP 잔액 0).
# 일회성(E54): 최근 4분기 보통주 귀속 순이익 $1,117.7M(4분기 $156.0M + 1~9월 $961.6M). 매각 이익 $1,169.6M(4분기 128.0 + 1~9월 1,041.6 — 7월 캘리포니아 포트폴리오 약 $1.0B) = 105% → 미완성.
#   그 밖에 토지 개발 손상 $86.4M(3분기), RealPage 합의 등 기타 영업외 비용(1분기 약 $60M).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, 0), '판정 보류'
CO = 'Camden'
S_ = 'https://www.sec.gov/Archives/edgar/data/906345/'
SEC = S_
TENQ = S_ + '000162828026071470/cpt-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000162828026071117/exhibit991earningsrelease3.htm', 'q2': S_ + '000162828026051083/exhibit991earningsrelease2.htm',
      'q1': S_ + '000162828026028942/exhibit991earningsrelease1.htm', 'q4': S_ + '000162828026005842/exhibit991earningsrelease4.htm',
      'q3old': S_ + '000162828025050242/exhibit991earningsrelease3.htm', 'ceo': S_ + '000119312526127725/d55686d8k.htm', 'realpage': S_ + '000162828026024527/cpt-20260407.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="cptFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 순이익보다 부동산 매각 이익이 크다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (-10, 40)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(개발·개량)'   # 현금흐름표 한 줄, 인수 제외
MODEL_NOTE = ('미완성 카드다. 최근 4분기 보통주 순이익 $1.12B(EPS $10.73)보다 부동산 매각 이익($1.17B)이 더 크다 — 2026년 7월 캘리포니아 아파트 11곳(3,620가구)을 약 $1.6B에 팔아 약 $1.0B 이익을 냈다. 지금 낮은 PER은 이 이익 때문이고, 단순히 빼면 약 −$52M이다(세금·비지배 조정 전 비교) — 그래서 판정을 보류한다. 2026년 3분기가 최근 4분기에서 빠지는 2027년 3분기 실적 뒤 다시 잰다. '
              '같은 이유로 PBR(매각 이익으로 자본이 약 $0.75B 늘었다)과 PSR(분모가 매각 전 매출)도 낮게 나온다. 최근 4분기에는 토지 개발 손상 $99M(3분기 $86M, 작년 4분기 $13M)과 RealPage 임대료 담합 집단소송 합의 $53M 등 기타 영업외 비용도 있다(법무부·여러 주의 소송은 남아 있다). 매출 −3.7%는 매각 효과이고 동일 자산 매출은 3분기 −0.1%다. 리츠는 업계가 보완 지표로 FFO를 쓴다 — 캠든의 2026년 Core FFO 전망은 주당 $6.73~6.77이다(3분기 $1.71). 사이트에는 리츠 전용 평가가 아직 없다. '
              '손익계산서에 매출 합계와 영업이익 줄이 없어 매출은 부동산 수익, 영업이익은 세전이익에 이자를 더하고 매각 이익(2022년 합작 지분 인수 재평가 이익 포함)을 뺀 값으로 쓴다(손상·소송 비용·투자 손익은 포함). 매각 대금 중 약 $0.9B로 신용한도·기업어음을 갚았고, 9월 말 제한 현금 중 $427M은 1031 교환용으로 묶여 있다(카드의 현금에는 들어가지 않는다). 2026년 1~9월 선벨트 단지 인수 $750M, 자사주 454만 주 $473M을 샀다. 2026년 3월 CEO가 Ric Campo에서 Alex Jessett로 바뀌었다(Campo는 이사회 의장).')
HEALTH_EXTRA = '아파트 매입·개발 자금을 채권·대출로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
PH = ['MAA', 'EQR', 'AVB', 'UDR', 'ESS', 'INVH']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '아파트 리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(CPT 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 주거 리츠 6곳이 보인다.')
SEG = [('부동산 수익(임대료·관련 서비스)', 381.1, '#5a9e2f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부동산 수익(관리 수수료는 영업외)'
NEWS_RANGE = '2025.11 ~ 2026.11'
NEWS = [
    ('red', '2026년 11월 5일 장 마감 뒤 — Q3 2026 실적', '2026-11-06',
     '보통주 순이익 $900M · 희석 EPS $8.71(캘리포니아 매각 이익 약 $1.0B, 토지 개발 손상 $86M 포함) · Core FFO $1.71(전망 중간값 $1.69) · 동일 자산 매출·NOI 전망 하향 — 다음 날 주가 −4.1%', 'q3', 'Camden 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 30일 장 마감 뒤 — Q2 2026 실적 · 캘리포니아 매각', '2026-07-31',
     '희석 EPS $0.18 · Core FFO $1.68 · 7월 29일 캘리포니아 아파트 11곳을 약 $1.625B에 매각 — 다음 날 주가 −2.2%', 'q2', 'Camden 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 30일 장 마감 뒤 — Q1 2026 실적', '2026-05-01',
     '희석 EPS $0.40(RealPage 합의 등 비용과 매각 이익 함께 포함) · Core FFO $1.70 — 다음 날 주가 −0.5%', 'q1', 'Camden 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 9일 장 마감 뒤 — RealPage 집단소송 합의', '2026-04-10',
     '4월 7일 RealPage 임대료 담합 집단소송 합의($53M, 10월 법원 최종 승인) — 합의금은 기타 영업외 비용으로, Core FFO에서는 빠진다, 정부 소송은 남음 — 다음 날 주가 +1.1%', 'realpage', 'Camden 공시 (SEC 8-K)'),
    ('neutral', '2026년 3월 27일 장 전 — CEO 교체', '2026-03-27',
     '3월 24일부로 Alex Jessett가 CEO, Ric Campo는 이사회 의장(Executive Chairman) — 그날 주가 −0.7%', 'ceo', 'Camden 공시 (SEC 8-K)'),
    ('neutral', '2026년 2월 5일 장 마감 뒤 — 2025년 연간 실적', '2026-02-06',
     '4분기 희석 EPS $1.44(매각 이익 $128M 포함) · Core FFO $1.76 · 2025년 Core FFO $6.88 — 다음 날 주가 +0.1%', 'q4', 'Camden 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 11월 6일 장 마감 뒤 — Q3 2025 실적', '2025-11-07',
     '희석 EPS $1.00 · Core FFO $1.70 — 다음 날 주가 +2.5%', 'q3old', 'Camden 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 24, 'nt': 17, 'mean': 109.31, 'median': 107, 'low': 101, 'high': 132, 'sb': 6, 'b': 1, 'h': 15, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-11-23'

INCOMPLETE_SHORT = '부동산 매각 이익이 큼'
INCOMPLETE_WHY = '최근 4분기 보통주 순이익 $1.12B(EPS 1.44+0.40+0.18+8.71 = $10.73)보다 부동산 매각 이익($1.17B)이 더 크다 — 2026년 7월 캘리포니아 아파트 11곳($1.6B)을 팔아 약 $1.0B 이익을 냈다. 이 이익을 빼면 적자 근처라 배수 판정이 왜곡돼 보류한다. 2026년 3분기가 최근 4분기에서 빠지는 2027년 3분기 실적 뒤 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 보통주 순이익 $1.12B(EPS 1.44+0.40+0.18+8.71 = $10.73)보다 부동산 매각 이익($1.17B)이 더 크다 — 2026년 7월 캘리포니아 아파트 11곳($1.6B)을 팔아 약 $1.0B 이익을 냈다. 이 이익을 빼면 적자 근처라 배수 판정이 왜곡돼 보류한다. 2026년 3분기가 최근 4분기에서 빠지는 2027년 3분기 실적 뒤 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 부동산 매각 이익이 큼</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 부동산 매각 이익이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="cptFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">부동산 매각 이익이 큼</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = h.replace('Q3 2026 10-Q 부문 표 (SEC)', 'Q3 2026 10-Q 손익계산서 (SEC)')
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·', '· GAAP 기준(영업이익은 부동산 매각 이익 제외) · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·')
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(개발·개량) ·', '· 매출·순이익은 GAAP, 영업이익은 카드 계산값(매각 이익 제외) · FCF는 영업현금흐름 − 설비투자(개발·개량) ·')
h = h.replace('합성 영업이익률(세전이익 기준)', '카드 기준 합성 영업이익률(매각 이익 제외)').replace('합성 영업이익(세전이익 기준)', '카드 기준 합성 영업이익(매각 이익 제외)')
"""]

AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {"us-gaap:OperatingLeaseLeaseIncome": ["부동산 수익(임대료·관련 서비스)", "#5a9e2f"]},
 "ignore": []
}
