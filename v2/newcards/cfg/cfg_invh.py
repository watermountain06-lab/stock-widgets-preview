CIK = '0001687229'
BUILD = {'no_dcf': '미완성 — 최근 4분기 순이익의 약 6할이 주택 매각 이익'}
# INVH(인비테이션 홈즈) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 리츠(REIT) — 미국 단독주택 임대(2026년부터 주택 건설 사업 일부 인수).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-29 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 접수 → 다음 세션).
# 엔진 입력(2026-11-21): 영업이익 = 매출 − 비용 합계 + 이자비용(DERIVED_OPINC, O 방식 — 재해·손상은 영업 안, 매각 이익·합작 손익·채무 조정 손실은 밖), 순이익 = 보통주 귀속,
#   일회성 순액(합작 해산 손실 약 $30.4M·채무 조정 손실 $8.7M 상계) 54.5%.
#   설비투자 = "Other capital expenditures"(기존 주택 개량, 9개월 $180.8M — 인수·초기 리노베이션 $197.1M, 택지·건설 $80.1M, 합작 투자 $221.0M 제외), 차입금 $8,740.2M(담보·무담보 채권·기간 대출·신용한도).
# 일회성(E54): 최근 4분기 보통주 귀속 순이익 $680.1M(4분기 $144.3M + 1~9월 $535.8M, 희석 EPS 0.24+0.26+0.37+0.27 = 1.14). 매각 이익 $410.0M(4분기 54.5 + 1~9월 355.6) = 60.3% → 미완성.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, 0), '판정 보류'
CO = 'Invitation Homes'
S_ = 'https://www.sec.gov/Archives/edgar/data/1687229/'
SEC = S_
TENQ = S_ + '000168722926000056/invh-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000168722926000053/q32026supplemental.htm', 'q2': S_ + '000168722926000041/q22026supplemental.htm',
      'q1': S_ + '000168722926000030/q12026supplemental.htm', 'q4': S_ + '000168722926000013/q42025supplemental.htm',
      'q3old': S_ + '000168722925000047/q32025supplemental.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="invhFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 EPS의 약 6할이 주택 매각 이익이다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (0, 40)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(기존 주택 개량)'   # 인수·초기 리노베이션·택지·합작 투자는 넣지 않는다
MODEL_NOTE = ('미완성 카드다. 최근 4분기 보통주 순이익 $680M(EPS $1.14)의 약 60%가 단독주택 매각 이익 $410M이다. 회사는 주가가 자산가치보다 크게 싸면 주택 매각 대금으로 자사주를 계속 산다는 방침이라(2026년 1~9월 자사주 매입 $798M) 매각 이익이 한두 분기로 끝나지 않을 수 있다 — 최근 4분기가 흑자이고 일회성이 순이익의 30% 아래로 내려올 때 다시 잰다. 이 이익을 빼면(순이익 비중으로 단순 추산) PER이 약 58배로 올라 PER 순위가 맞지 않는다 — 그래서 판정을 보류한다. 매각 이익이 분모를 직접 부풀리는 것은 PER이고, 나머지 네 배수(PSR·PBR·PCR·EV/EBITDA)가 5년 바닥권인 데는 주가 하락(2021년 11월보다 약 36%)과 그동안 늘어난 매출·자산·차입금이 함께 반영돼 있다. 3분기에는 Pathway 합작 해산 손실 약 $30M과 채무 조정 손실 $9M도 있어, 두 손실을 상계해도 최근 4분기 매각 이익 순액은 순이익의 약 55%다. '
              '리츠는 건물 감가상각이 커서 GAAP 순이익이 실제 현금 창출과 다르고, 업계는 보완 지표로 FFO를 쓴다 — 인비테이션 홈즈의 2026년 연간 Core FFO 전망은 주당 $1.94~1.98이다. 사이트에는 리츠 전용 평가가 아직 없다. 영업이익은 매출에서 이자를 뺀 비용 합계를 뺀 값(재해·손상은 포함, 매각 이익·합작 손익은 제외)으로 쓴다. '
              '2026년 1월 14일 주택 건설사 ResiBuilt를 인수해 매출에 주택 건설 매출(1~9월 $129M)이 새로 들어갔다 — 그래서 2026년 매출 증가율 대부분이 인수 효과다(3분기 매출 +6.3% 중 건설 매출을 빼면 +1.1%). FCF의 설비투자는 기존 주택 개량 지출만 넣었고 주택 인수·초기 리노베이션(1~9월 $197M), 택지·건설($80M), 합작 투자($221M)는 넣지 않았다.')
HEALTH_EXTRA = '주택 매입 자금을 채권·대출로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
PH = ['MAA', 'EQR', 'AVB', 'UDR', 'CPT', 'ESS']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '주거 리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(INVH 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 아파트 임대 리츠 6곳이 보인다.')
# 매출(Q3 2026 10-Q 손익계산서): 임대·기타 부동산 수익 675.5 + 관리 수수료 19.9 + 주택 건설 35.8 = 731.3. 1년 전 666.2·22.0·0.
SEG = [('임대·기타 부동산 수익', 675.5, '#1f8a3d'), ('주택 건설 매출', 35.8, '#7cc95a'), ('관리 수수료', 19.9, '#cdeec0')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 손익계산서 항목별'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 10월 28일 장 마감 뒤 — Q3 2026 실적', '2026-10-29',
     '보통주 순이익 $158M · 희석 EPS $0.27(1년 전 $0.22 — 주택 매각 이익 $136M, Pathway 합작 해산 손실 약 $30M·채무 조정 손실 $9M 포함) · 2026년 Core FFO 전망 $1.94~1.98로 좁힘(중간값 $1.95 → $1.96) — 다음 날 주가 −0.4%', 'q3', 'Invitation Homes 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 29일 장 마감 뒤 — Q2 2026 실적', '2026-07-30',
     '보통주 순이익 $218M · 희석 EPS $0.37(매각 이익 $132M 포함) · 자사주 누적 2,281만 주 약 $600M · Core FFO 전망 중간값 $1.95 — 다음 날 주가 −1.5%', 'q2', 'Invitation Homes 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 29일 장 마감 뒤 — Q1 2026 실적', '2026-04-30',
     '보통주 순이익 $160M · 희석 EPS $0.26(1년 전 $0.27) · 자사주 1,933만 주 $500M 매입으로 한도 소진 — 다음 날 주가 +2.5%', 'q1', 'Invitation Homes 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 18일 장 마감 뒤 — 2025년 연간 실적', '2026-02-19',
     '4분기 보통주 순이익 $144M · 희석 EPS $0.24 · 2026년 Core FFO 전망 $1.90~1.98(2025년 실적 $1.91) — 다음 날 주가 −4.3%', 'q4', 'Invitation Homes 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 29일 장 마감 뒤 — Q3 2025 실적', '2025-10-30',
     '희석 EPS $0.22 · 2025년 Core FFO 전망 $1.90~1.94로 상향 — 다음 날 주가 +3.4%', 'q3old', 'Invitation Homes 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 25, 'nt': 16, 'mean': 32.31, 'median': 33, 'low': 28, 'high': 36, 'sb': 9, 'b': 5, 'h': 11, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-23'

INCOMPLETE_SHORT = '주택 매각 이익이 큼'
INCOMPLETE_WHY = '최근 4분기 EPS($1.14)의 약 6할이 단독주택 매각 이익이다 — 매각 이익 $410M(2025년 4분기 $54M + 2026년 1~9월 $356M)이 보통주 순이익 $680M의 약 60%라 배수 판정이 왜곡돼 보류한다. 회사는 주가가 자산가치보다 크게 싸면 주택 매각 대금으로 자사주를 산다는 방침이라 매각 이익이 계속 크다 — 최근 4분기가 흑자이고 일회성이 순이익의 30% 아래로 내려올 때 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 EPS($1.14)의 약 6할이 단독주택 매각 이익이다 — 매각 이익 $410M(2025년 4분기 $54M + 2026년 1~9월 $356M)이 보통주 순이익 $680M의 약 60%라 배수 판정이 왜곡돼 보류한다. 회사는 주가가 자산가치보다 크게 싸면 주택 매각 대금으로 자사주를 산다는 방침이라 매각 이익이 계속 크다 — 최근 4분기가 흑자이고 일회성이 순이익의 30% 아래로 내려올 때 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 주택 매각 이익이 큼</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 주택 매각 이익이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="invhFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">주택 매각 이익이 큼</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = h.replace('Q3 2026 10-Q 부문 표 (SEC)', 'Q3 2026 10-Q 손익계산서 (SEC)')
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·', '· GAAP 기준(영업이익은 부동산 매각 이익 제외) · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·')
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(기존 주택 개량) ·', '· GAAP 기준(영업이익은 매각 이익·합작 손익 제외 합성) · FCF는 영업현금흐름 − 설비투자(기존 주택 개량) ·')
h = h.replace('합성 영업이익률(세전이익 기준)', '매각 이익 제외 영업이익률').replace('합성 영업이익(세전이익 기준)', '매각 이익 제외 영업이익')
"""]

AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {"us-gaap:SubleaseIncome": ["임대·기타 부동산 수익", "#1f8a3d"],
             "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax": ["주택 건설 매출", "#7cc95a"],
             "us-gaap:RevenueNotFromContractWithCustomer": ["관리 수수료", "#cdeec0"]},
 "ignore": []
}
