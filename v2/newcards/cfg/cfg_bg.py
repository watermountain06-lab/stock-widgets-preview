CIK = '0001996862'
BUILD = {'no_dcf': '미완성 — Viterra 통합 비용·연금 정산·사탕수수 공장 매각 관련 손실 등 회사 특별 항목이 최근 4분기 GAAP 이익의 약 33%'}   # 2026-11-07·08 사용자 규칙(일회성 30% 이상이면 미완성, 회사 분류를 따른다)
# BG(번기) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 말. 대두·연질 유지 작물 압착·정제, 열대유·특수 원료, 곡물 유통·제분(2025년 7월 Viterra 합병).
# 출처: SEC XBRL(2023-11 스위스 이전으로 새 CIK — 이력 2021년부터), Q3 2026 10-Q(2026-10-29 접수, 카드 기준일 11-17 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 06~09시 동부 → 그날).
# 엔진 입력(2026-11-18): 영업이익 = 세전이익 + 이자비용 − 이자·기타 수익(DERIVED_OPINC — 영업이익 줄 없음). 지분법 이익은 영업에 남는다. Q4 2025 EPS는 보도자료 계속사업 0.49(역산 −0.02, Q4_EPS_OVERRIDE).
# 일회성(E54): 최근 4분기 계속사업 GAAP 희석 EPS 5.95(0.49 + 0.35 + 3.47 + 1.64 — 보도자료) 대 회사 조정 8.38(1.99 + 1.83 + 2.00 + 2.56).
#   회사 "certain (gains) & charges"(세후 주당): Q4 2025 0.95(연금 정산 0.46·Viterra 통합 0.29·장기 투자 손상 0.15·지분법 투자 충당 0.05), Q1 0.20(통합), Q2 0.20(통합), Q3 0.64(매각 예정 브라질 사탕수수 공장 손상 $66M·헤지 손실 $16M = 0.43·통합 0.10·우크라이나 전쟁 0.11) → 1.99(약 33%) → 미완성.
#   회사는 상품·운임·환 계약의 평가 시차(mark-to-market timing)도 조정에서 뺀다 — 0.55·1.28·−1.67·0.28 = 0.44(분기마다 크게 오가는 시차, 1년 합으로는 작다). 합치면 2.43(약 41%).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Bunge'
S_ = 'https://www.sec.gov/Archives/edgar/data/1996862/'
SEC = S_
TENQ = S_ + '000162828026068130/bg-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000162828026068051/epr09302026.htm', 'q2': S_ + '000162828026050334/epr06302026.htm',
      'q1': S_ + '000162828026028079/epr03312026.htm', 'q4': S_ + '000162828026005261/epr123120254.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="bgFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(회사 특별 항목이 최근 4분기 GAAP 이익을 크게 깎는다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (-10, 30)
ACT_REASON = ''
BB_TAGS = ['TreasuryStockValueAcquiredCostMethod']   # 자사주 매입은 자본변동표 태그로만(9개월 1,966,107주 $249M, 2분기에 끝냄 — 새 $3.0B 한도)(Codex·Fable r1)
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 최근 4분기 GAAP 이익 대비 일회성이 순액이나 비용만으로(세후) 30% 이상이거나 GAAP가 적자면 판정을 보류하는데, BG는 회사가 조정에서 빼는 특별 항목이 최근 4분기 계속사업 GAAP 희석 EPS $5.95의 약 33%($1.99)다 — 2025년 4분기 연금 정산($0.46)·장기 투자 손상, 매 분기 나오는 Viterra 통합 비용, 2026년 3분기 매각 예정 브라질 사탕수수 공장 손상·헤지 손실($0.43) 등이다. '
              '회사는 여기에 상품·운임·환 계약의 평가 시차도 빼서 조정 EPS($8.38)를 낸다 — 이 시차는 분기마다 주당 −$1.67~+$1.28로 크게 오가 분기 GAAP 이익을 흔든다(1년 합은 $0.44). '
              '분기마다 다시 센다. 가장 큰 2025년 4분기 항목이 빠지는 2026년 4분기 실적(2027년 2월 초 예상)이 주요 확인 시점이다 — 그때 남는 특별 항목은 주당 약 $1.05(9개월 누계 공시 기준)이고 분모에는 새 4분기 GAAP 이익이 더해진다 — 새 특별 항목이 없고 4분기 GAAP EPS를 0에서 $3.37 사이(회사 전망에서 나온 4분기 조정 EPS 상단)로 가정하면 약 12~19%라 30% 아래가 될 가능성이 높다. 실제 비중은 4분기 실적이 나오면 다시 계산한다. 상품 평가 시차는 되돌아오는 항목이라 이 30% 검정에는 넣지 않는다. '
              '곡물 회사라 매출이 크고 이익률이 얇다(최근 4분기 순이익률 1.2% — 2% 아래라 PER을 점수에서 뺀다). 2025년 7월 2일 Viterra와 합병해(주식 약 6,560만 주 발행) 2026년 1·2분기 매출이 1년 전보다 약 88% 늘었다 — 3분기부터는 1년 전 같은 분기에도 Viterra가 들어 있다(3분기 +7.4%). 최근 4분기·연간 비교와 성장률에는 합병 효과가 섞여 있다. 2023년 11월 지주회사 설립 관할을 버뮤다에서 스위스로 옮기며(등록 사무소 제네바, 운영 본사는 미국) SEC 등록 번호가 바뀌어, 카드가 새 번호에서 모은 이력은 2021년부터이고 배수 비교 기간은 약 2.7년이다. '
              '영업현금흐름은 곡물·유지 재고와 증거금 같은 운전자본 변동에 크게 흔들려, 2026년 9개월은 −$2.3B(회사가 운전자본 변동 등을 빼고 내는 조정 영업자금은 +$2.0B)였다 — 그래서 카드의 FCF·PCR이 음수로 나온다. 회사는 2026년 조정 EPS 전망 $9.25~9.75를 유지했다(3분기 실적 때).')
PH = ['ADM', 'MDLZ', 'SYY', 'PEP', 'KDP', 'HSY']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '식품·농산물 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(BG 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·생활용품·유통이 섞여 있다. 차트에는 곡물 동종 ADM과 식품·음료 5곳이 보인다.')
# 매출(Q3 2026 10-Q 부문, 외부 고객): 대두 압착·정제 11,442 + 연질 유지 작물 4,302 + 열대유·특수 원료 1,295 + 곡물 유통·제분 6,764 = 23,803, 본사·기타 1 → 23,804.
SEG = [('대두 압착·정제', 11442, '#00573f'), ('곡물 유통·제분(Viterra 포함)', 6764, '#f2a900'), ('연질 유지 작물(카놀라·해바라기) 압착·정제', 4302, '#5a9e7c'), ('열대유·특수 원료', 1295, '#c9a227')]
SEG_ADJ = 1
SEG_ADJ_LABEL = '본사·기타'
SEG_TITLE = '매출 구성 — 사업 부문별'
# 손 뉴스: 실적 4건. 반응일: 모두 장 전 → 그날.
NEWS_RANGE = '2026.02 ~ 2026.10'
NEWS = [
    ('neutral', '2026년 10월 29일 장 전 — Q3 2026 실적', '2026-10-29',
     'GAAP 희석 EPS $1.64(매각 예정 브라질 사탕수수 공장 손상·헤지 손실 $82M 포함) · 조정 EPS $2.56 · 2026년 조정 EPS 전망 $9.25~9.75 유지 — 그날 주가 −4.7%', 'q3', 'Bunge 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 29일 장 전 — Q2 2026 실적', '2026-07-29',
     'GAAP 희석 EPS $3.47(상품 평가 시차 이익 주당 $1.67 포함) · 조정 EPS $2.00 — 그날 주가 −8.2%', 'q2', 'Bunge 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 29일 장 전 — Q1 2026 실적', '2026-04-29',
     'GAAP 희석 EPS $0.35(상품 평가 시차 손실 주당 $1.28 포함) · 조정 EPS $1.83 — 그날 주가 0.0%', 'q1', 'Bunge 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 4일 장 전 — 2025년 연간 실적', '2026-02-04',
     '4분기 계속사업 GAAP 희석 EPS $0.49(연금 정산 등 특별 항목 주당 $0.95) · 조정 EPS $1.99 · 연간 조정 EPS $7.57 — 그날 주가 +0.3%', 'q4', 'Bunge 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 9, 'nt': 7, 'mean': 142, 'median': 140, 'low': 130, 'high': 155, 'sb': 5, 'b': 3, 'h': 1, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-21'

# 재검토 기록용(자동 재판정 코드는 아직 없음) — 회사 특별 항목(세후 주당, +는 비용).
ONEOFF_QUARTERS = {'2025-12-31': '0.95 — 연금 정산 0.46 · Viterra 통합 0.29 · 장기 투자 손상 0.15 · 지분법 투자 충당 0.05 (평가 시차 +0.55 별도)',
                   '2026-03-31': '0.20 — Viterra 통합 (평가 시차 +1.28 별도)',
                   '2026-06-30': '0.20 — Viterra 통합 (평가 시차 −1.67 별도)',
                   '2026-09-30': '0.64 — 매각 예정 사탕수수 공장 관련 0.43(4분기 종결 때 추가 항목 가능) · 통합 0.10 · 우크라이나 전쟁 0.11 (평가 시차 +0.28 별도)'}

INCOMPLETE_SHORT = '특별 항목이 이익의 약 3분의 1'
INCOMPLETE_WHY = '회사가 조정에서 빼는 특별 항목(연금 정산·Viterra 통합·사탕수수 공장 매각 관련 손실 등)이 최근 4분기 계속사업 GAAP EPS($5.95)의 약 33%라 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 주요 확인은 2027년 2월 초(2025년 4분기 항목이 빠질 때)'
POST = [r"""
import re as _re0
_w = '회사가 조정에서 빼는 특별 항목(연금 정산·Viterra 통합·사탕수수 공장 매각 관련 손실 등)이 최근 4분기 계속사업 GAAP EPS($5.95)의 약 33%라 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 주요 확인은 2027년 2월 초(2025년 4분기 항목이 빠질 때)'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 특별 항목이 이익의 약 3분의 1 · 매 분기 재검토, 주요 확인 2027년 2월 초</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 특별 항목이 이익의 약 3분의 1. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="bgFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">특별 항목이 이익의 약 3분의 1</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"bg:SoybeanProcessingAndRefiningMember": ["대두 압착·정제", "#00573f"], "bg:GrainMerchandisingAndMillingMember": ["곡물 유통·제분(Viterra 포함)", "#f2a900"], "bg:SoftseedProcessingAndRefiningMember": ["연질 유지 작물(카놀라·해바라기) 압착·정제", "#5a9e7c"], "bg:TropicalOilsAndSpecialtyIngredientsMember": ["열대유·특수 원료", "#c9a227"]},
 "ignore": []
}
