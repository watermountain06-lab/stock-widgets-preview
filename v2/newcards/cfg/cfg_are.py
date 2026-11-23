CIK = '0001035443'
BUILD = {'no_dcf': '미완성 — 최근 4분기 GAAP 적자(부동산 손상)'}
# ARE(알렉산드리아 리얼 에스테이트) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 리츠(REIT) — 생명과학 연구 단지(보스턴·샌프란시스코·샌디에이고 등).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-26 접수, 카드 기준일 11-20 종가), 실적 자료(8-K 2.02항 supplemental — 모두 장 마감 뒤 16:0x 동부 → 다음 세션).
# 엔진 입력(2026-11-21): 영업이익 = 매출 − 비용 합계 + 이자비용(DERIVED_OPINC, O·INVH 방식 — 부동산 손상은 회사 배치대로 영업 안), 순이익 = 보통주 귀속,
#   설비투자 = "Additions to investments in real estate"(개발·재개발·개량 한 줄, 9개월 $1,328.1M), 차입금 = 선순위채 $10,820.7M + 후순위채 $985.1M + 신용한도·CP $1,091.2M = $12,897.0M, 비지배지분 $3,602M(합작 파트너).
# 미완성 사유: 최근 4분기 GAAP 적자(희석 EPS −6.35 + 2.10 − 0.43 − 3.74 = −8.42) — 부동산 손상 4분기 합 약 $2.58B(1,717.2 + 5.5 + 222.5 + 637.9). 1분기 흑자는 채무 조기상환 이익 $366M(9개월 누계 $363M) 덕.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Alexandria'
S_ = 'https://www.sec.gov/Archives/edgar/data/1035443/'
SEC = S_
TENQ = S_ + '000103544326000076/are-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000103544326000077/a3q26ex991supp.htm', 'q2': S_ + '000103544326000067/a2q26ex991supp.htm',
      'q1': S_ + '000103544326000045/a1q26ex991supp.htm', 'q4': S_ + '000103544326000014/a4q25ex991supp.htm',
      'q3old': S_ + '000103544325000199/a3q25ex991supp.htm', 'jsn': S_ + '000110465926097337/tm2622485d5_ex99-1.htm', 'divcut': S_ + '000103544325000211/ex992-2026guidance.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="areFairBand" title="미완성 카드라 적정주가를 표시하지 않는다(최근 4분기 GAAP 적자 — PER을 쓸 수 없다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (-220, 60)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(개발·재개발·개량)'   # 현금흐름표 한 줄
MODEL_NOTE = ('미완성 카드다. 최근 4분기 GAAP 순손실이다(희석 EPS −$8.42) — 개발 계획을 접고 자산을 매각 예정으로 돌리면서 부동산 손상을 크게 잡았다(2025년 4분기 $1.72B, 2026년 2분기 $0.22B, 3분기 $0.64B, 4분기 합 약 $2.58B). 손상이 회사 비용 합계 안이라 카드의 합성 영업이익(매출 − 비용 합계 + 이자)과 EBITDA도 0 이하다 — PER·EV/EBITDA를 쓸 수 없어 판정을 보류한다. 2026년 1분기 흑자(EPS $2.10)는 채무 조기상환 이익 $366M 덕이다(그 분기 투자 손익은 소폭 손실). 최근 4분기에는 2025년 4분기 부동산 매각 이익 $620M도 섞여 있어, 손상만 빼고 보면 흑자가 크게 보이지만 그 큰 이익들까지 ARE 몫으로 빼면 보통주 순이익은 약 $0.2B(주당 약 $1.2, 단순 추정 — 정상 이익이라는 뜻은 아니다)에 그친다. 손상을 뺀 카드 기준 합성 영업이익률은 약 18%다(2021년 값에는 그때 비용 합계 안에 있던 채무 상환 손실 $67M이 섞여 있다). 배당은 2025년 12월 분기 $1.32에서 $0.72로 45% 줄였다. '
              '리츠는 업계가 보완 지표로 FFO를 쓴다 — 회사 기준 FFO(as adjusted)는 주당 2025년 3분기 $2.22에서 2026년 3분기 $1.54로 줄었다. 사이트에는 리츠 전용 평가가 아직 없다. 지금 PSR·PBR이 5년 최저권인 것은 주가가 크게 내렸기 때문이고, 장부가치에는 앞으로 더 잡힐 수 있는 손상이 반영되지 않았을 수 있다. '
              '설비투자는 개발·재개발·개량이 현금흐름표 한 줄이라 함께 넣었다(1~9월 $1.33B). 합작 파트너 몫 비지배지분($3.6B)이 커서 기업가치에 더한다. 2026년 8월 후순위채 $1.0B(2057년 만기, 처음 이자 7.25% — 2032년부터 5년마다 재설정)를 발행했다.')
HEALTH_EXTRA = '연구 단지 개발 자금을 채권·기업어음으로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
PH = ['KIM', 'O', 'PLD', 'WELL', 'DLR', 'AMT']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(ARE 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 리츠 6곳이 보인다.')
SEG = [('임대 수익', 653.6, '#1b3a6b'), ('기타 수익', 17.6, '#b6c9e6')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 손익계산서 항목별'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('red', '2026년 10월 26일 장 마감 뒤 — Q3 2026 실적', '2026-10-27',
     '희석 EPS −$3.74(1년 전 −$1.38, 부동산 손상 $638M) · FFO as adjusted $1.54(1년 전 $2.22) — 다음 날 주가 −5.9%', 'q3', 'Alexandria 실적 자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 12일 — 후순위채 $1.0B 가격 확정', '2026-08-13',
     '2057년 만기 후순위채(Series A) $1.0B, 처음 이자 7.25%로 가격 확정(8월 21일 발행) — 다음 날 주가 +0.7%', 'jsn', 'Alexandria 보도자료 (SEC 8-K)'),
    ('red', '2026년 8월 3일 장 마감 뒤 — Q2 2026 실적', '2026-08-04',
     '희석 EPS −$0.43(1년 전 −$0.64, 손상 $222M) · FFO as adjusted $1.73(1년 전 $2.33) — 다음 날 주가 −7.8%', 'q2', 'Alexandria 실적 자료 (SEC 8-K)'),
    ('red', '2026년 4월 27일 장 마감 뒤 — Q1 2026 실적', '2026-04-28',
     '희석 EPS $2.10(채무 조기상환 이익 포함) · FFO as adjusted $1.73(1년 전 $2.30) — 다음 날 주가 −11.3%', 'q1', 'Alexandria 실적 자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 26일 장 마감 뒤 — 2025년 연간 실적', '2026-01-27',
     '4분기 희석 EPS −$6.35(부동산 손상 $1.72B) · FFO as adjusted $2.16 · 2025년 $9.01 — 다음 날 주가 +1.7%', 'q4', 'Alexandria 실적 자료 (SEC 8-K)'),
    ('red', '2025년 12월 3일 장 전 — 투자자의 날 · 배당 45% 삭감', '2025-12-03',
     '분기 배당 $1.32 → $0.72(45% 삭감, 연 약 $410M 유동성 확보)와 2026년 전망 발표 — 그날 주가 −10.1%', 'divcut', 'Alexandria 투자자의 날 자료 (SEC 8-K)'),
    ('red', '2025년 10월 27일 장 마감 뒤 — Q3 2025 실적', '2025-10-28',
     '희석 EPS −$1.38(손상 $324M) · FFO as adjusted $2.22 — 다음 날 주가 −19.2%', 'q3old', 'Alexandria 실적 자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 16, 'nt': 14, 'mean': 48.93, 'median': 50, 'low': 41, 'high': 59, 'sb': 2, 'b': 0, 'h': 9, 's': 3, 'ss': 2}
ANALYST_ASOF = '2026-11-23'

INCOMPLETE_SHORT = 'GAAP 적자(부동산 손상)'
INCOMPLETE_WHY = '최근 4분기 GAAP 순손실이다 — 희석 EPS −6.35 + 2.10 − 0.43 − 3.74 = −$8.42. 개발 계획을 접고 자산을 매각 예정으로 돌리며 부동산 손상을 크게 잡았다(2025년 4분기 $1.72B, 2026년 2분기 $0.22B, 3분기 $0.64B). PER을 쓸 수 없고 EV/EBITDA도 0 이하라 판정을 보류한다. 최근 4분기가 흑자로 돌아서고 일회성이 30% 아래일 때 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 순손실이다 — 희석 EPS −6.35 + 2.10 − 0.43 − 3.74 = −$8.42. 개발 계획을 접고 자산을 매각 예정으로 돌리며 부동산 손상을 크게 잡았다(2025년 4분기 $1.72B, 2026년 2분기 $0.22B, 3분기 $0.64B). PER을 쓸 수 없고 EV/EBITDA도 0 이하라 판정을 보류한다. 최근 4분기가 흑자로 돌아서고 일회성이 30% 아래일 때 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — GAAP 적자(부동산 손상)</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — GAAP 적자(부동산 손상). 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="areFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">GAAP 적자(부동산 손상)</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = h.replace('Q3 2026 10-Q 부문 표 (SEC)', 'Q3 2026 10-Q 손익계산서 (SEC)')
h = h.replace('차입금·리스 $', '차입금 $')
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·', '· GAAP 기준(영업이익은 부동산 매각 이익 제외) · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·')
h = h.replace('합성 영업이익률(세전이익 기준)', '카드 기준 합성 영업이익률').replace('합성 영업이익(세전이익 기준)', '카드 기준 합성 영업이익')
"""]

POST.append(r'''
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(개발·재개발·개량) ·', '· GAAP 기준(영업이익은 매출 − 비용 합계 + 이자 합성, 손상 포함) · FCF는 영업현금흐름 − 설비투자(개발·재개발·개량) ·')
h = h.replace('합성 영업이익률(세전이익 기준)', '합성 영업이익률(매출 − 비용 + 이자, 손상 포함)').replace('합성 영업이익(세전이익 기준)', '합성 영업이익(매출 − 비용 + 이자, 손상 포함)')
''')

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
 "axis": "srt:ProductOrServiceAxis",
 "extra": {},
 "members": {"are:IncomefromrentalsMember": ["임대 수익", "#1b3a6b"], "us-gaap:ProductAndServiceOtherMember": ["기타 수익", "#b6c9e6"]},
 "alias": {"are:IncomeFromRentalsMember": "are:IncomefromrentalsMember"},
 "ignore": []
}
