CIK = '0000100493'
BUILD = {'no_dcf': '미완성 — 최근 4분기 일회성(구조조정·소송 충당·경영진 교체·지분 손상)이 GAAP 순이익보다 크다', 'cover_shares': True}
# TSN(타이슨 푸드) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 9월 말 무렵 토요일(52/53주 — FY26은 53주, Q4 FY26은 14주).
# 출처: SEC XBRL, FY26 10-K(2026-11-16 07:50 동부 장 전 접수, 카드 기준일 11-18 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 07시대 동부 → 그날), 쇠고기 구조조정(08-13 16:29 장 마감 뒤 → 다음 날)·전망 하향(09-03 09:13 장 전 → 그날)·CEO(05-28 08:04 → 그날). FY26 감가상각은 보충 파일 손 행(1,398 = 1,167 + 231).
# 엔진 입력(2026-11-19): 차입금 = 1년 안 $848M + 장기(금융리스 포함) $6,902M = $7,750M(DEBT_TOTAL_TAG — 기본 합산은 거의 0), 표지 주식 수 클래스 A + B(cover_shares), Q4 FY26 EPS −0.22(보도자료, 역산 −0.21).
# 일회성(E54): FY26 GAAP 순이익 $453M(희석 EPS 1.28) 대 회사 조정(53주 조정 전) $1,232M — 세후 조정 $779M(구조조정 342·소송 충당 300·경영진 교체 83·지분 손상 54) = GAAP의 172%.
#   소송 충당(해마다 나옴)을 반복분으로 쳐도 $479M = 106% → 미완성. 분기 GAAP EPS 0.24·0.73·0.52·−0.22, 조정 0.97·0.87·0.99·0.61(Q4 14주).
CUR, YO, QO = '2026-10-03', '2025-09-27', '2026-06-27'
QLABEL, YL, QQL = 'Q4 FY26', 'Q4 FY25', 'Q3 FY26'
L8 = ['Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26']
FY_ENDS, FY_LABEL = ('2026-10-03', '2025-09-27'), 'FY2026'
VOTES, VERDICT = (0, 1, 0), '판정 보류'
CO = 'Tyson'
S_ = 'https://www.sec.gov/Archives/edgar/data/100493/'
SEC = S_
TENQ = S_ + '000010049326000079/tsn-20261003.htm'; TENQ_NAME = 'FY2026 10-K'
PR = {'q4': S_ + '000010049326000077/tsn2026q4exh-991.htm', 'q3': S_ + '000010049326000057/tsn2026q3exh-991.htm',
      'q2': S_ + '000010049326000019/tsn2026q2exh-991.htm', 'q1': S_ + '000010049326000005/tsn2026q1exh-991.htm',
      'beef': S_ + '000010049326000063/tsn2026pressreleasedatedau.htm', 'outlook': S_ + '000010049326000067/tsn2026pressreleasedatedse.htm',
      'ceo': S_ + '000010049326000026/tsn-20260528.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="tsnFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 일회성이 GAAP 이익보다 크다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (-10, 10)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 최근 4분기 GAAP 이익이 적자이거나 일회성이 30% 이상이면 판정을 보류하는데, 타이슨은 FY26 GAAP 순이익 $453M(희석 EPS $1.28)보다 회사가 조정에서 빼는 항목이 세후 $779M로 더 크다 — 구조조정(대부분 쇠고기 공장 정리) $342M, 가격 담합 소송 등 충당 $300M, 경영진 교체 비용 $83M, 지분 투자 손상 $54M이다. 회사 조정 EPS로는 $3.44다. '
              '소송 충당은 해마다 나왔지만(FY25 세후 $563M) 그것을 반복 비용으로 쳐도 나머지 일회성이 GAAP 이익보다 크다. 분기마다 다시 세지만, 이미 승인된 구조조정의 남은 비용은 세전 $27M뿐이어도 회사는 새 조치가 승인되면 추가 비용이 난다고 밝혔고, 4분기 FY26에 잡힌 일회성(세후 $302M)은 FY27 4분기 실적(2027년 11월 예상) 때 최근 4분기에서 빠진다. 해제 여부는 매 분기 일회성 ÷ GAAP 이익 비율로 다시 판정한다. '
              '이익은 소 사육 두수 부족으로 쇠고기 부문이 큰 적자(FY26 영업손실 GAAP $1,215M, 회사 조정 $654M)를 내는 가운데 닭고기·가공식품 부문(FY26 조정 영업이익 $1,859M·$1,332M)이 받치는 구조다. 회사는 FY27 쇠고기 조정 손익을 −$300M~+$100M, 전사 매출을 FY26(52주 환산) 대비 3.5~5.5% 감소로 내다본다. FY26은 53주라 4분기가 14주였고, 회사 조정 수치는 그 한 주를 뺀 값이다. '
              '10월 4일 Jeffrey K. Schomburger가 CEO에 올랐다. 주식 수는 클래스 A와 클래스 B(Tyson 가문 보유)를 더한 값이다. 매출에서 차감된 소송 충당(FY26 $358M) 때문에 매출 증가율도 조금 흔들린다.')
PH = ['HRL', 'CAG', 'GIS', 'KHC', 'ADM', 'BG']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '식품·농산물 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(TSN 제외)와 배수 순위를 매긴 값이다.',
            '음료·생활용품·유통·식품이 섞여 있고, 마진이 얇은 육류 가공은 업종 구조 때문에 매출 대비 배수가 낮게 나타날 수 있다 — 높은 점수가 곧 저평가는 아니다. 차트에는 식품·농산물 6곳만 보인다.')
# 매출(Q4 FY26 보도자료 부문, 14주): 쇠고기 5,295 + 닭고기 4,811 + 가공식품 2,754 + 돼지고기 1,560 + 해외 667 = 15,087, 부문 간 −502 → 14,585.
SEG = [('쇠고기', 5295.0, '#8b1e2d'), ('닭고기', 4811.0, '#e31837'), ('가공식품(Jimmy Dean·Hillshire 등)', 2754.0, '#003da5'), ('돼지고기', 1560.0, '#f28a8a'), ('해외·기타', 667.0, '#9aa7b8')]
SEG_ADJ = -502
SEG_ADJ_LABEL = '부문 간 거래 제거'
SEG_TITLE = '매출 구성 — 부문별'
NEWS_RANGE = '2026.05 ~ 2026.11'
NEWS = [
    ('red', '2026년 11월 16일 장 전 — Q4 FY26 실적', '2026-11-16',
     '매출 $14.59B(+5.2%, 14주) · 희석 주당 손실 $0.22(구조조정·소송 충당) · 조정 EPS $0.61(−47%) · FY26 GAAP EPS $1.28 · FY27 조정 영업이익 전망 $1.7~2.15B — 그날 주가 +8.7%', 'q4', 'Tyson 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 9월 3일 장 전 — FY26 전망 하향', '2026-09-03',
     '소 부족·가격 급변으로 쇠고기 부문 조정 영업손실 전망(52주 기준)을 $625~775M(직전 $500~650M)으로, 전사 조정 영업이익 전망을 $1.85~2.05B로 낮춤 — 그날 주가 −7.3%', 'outlook', 'Tyson 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 13일 장 마감 뒤 — 쇠고기 공장 재편', '2026-08-14',
     '쇠고기 사업을 중부 3개 공장 중심으로 재편, Joslin(일리노이)·Eagle Mountain(유타) 운영 종료, Pasco(워싱턴) 매각 추진 — 다음 날 주가 +3.2%', 'beef', 'Tyson 보도자료 (SEC 8-K)'),
    ('green', '2026년 8월 3일 장 전 — Q3 FY26 실적', '2026-08-03',
     '매출 $13.87B(보합) · 희석 EPS $0.52(1년 전 $0.17) · 조정 EPS $0.99(+9%) — 그날 주가 +2.8%', 'q3', 'Tyson 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 28일 장 전 — 새 CEO 선임 발표', '2026-05-28',
     'Jeffrey K. Schomburger를 10월 4일자 CEO로 선임 — 그날 주가 −6.1%', 'ceo', 'Tyson 8-K'),
]
ANALYST = {'rating': 'Hold', 'n': 13, 'nt': 10, 'mean': 69.6, 'median': 72, 'low': 60, 'high': 75, 'sb': 2, 'b': 2, 'h': 8, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-22'

ONEOFF_QUARTERS = {'2025-12-27': '주당 0.73 — 소송 충당·구조조정 등(조정 0.97 − GAAP 0.24)',
                   '2026-03-28': '주당 0.14(조정 0.87 − GAAP 0.73)',
                   '2026-06-27': '주당 0.47(조정 0.99 − GAAP 0.52)',
                   '2026-10-03': '세후 $302M(주당 0.87 — 구조조정 0.56·소송 충당 0.28·경영진 교체 0.03; −0.22 + 0.87 + 희석 0.01 − 추가 1주 0.05 = 조정 EPS 0.61(13주 기준))'}

INCOMPLETE_SHORT = '일회성이 GAAP 이익보다 큼'
INCOMPLETE_WHY = '최근 4분기(FY26) GAAP 순이익 $453M보다 회사가 조정에서 빼는 항목(세후 $779M — 구조조정 $342M·소송 충당 $300M·경영진 교체 $83M·지분 투자 손상 $54M)이 커서 배수 판정이 왜곡돼 보류한다. 소송 충당을 해마다 나오는 비용으로 쳐도 일회성이 GAAP 이익보다 크다. 분기마다 다시 센다'
POST = [r"""
import re as _re0
_w = '최근 4분기(FY26) GAAP 순이익 $453M보다 회사가 조정에서 빼는 항목(세후 $779M — 구조조정 $342M·소송 충당 $300M·경영진 교체 $83M·지분 투자 손상 $54M)이 커서 배수 판정이 왜곡돼 보류한다. 소송 충당을 해마다 나오는 비용으로 쳐도 일회성이 GAAP 이익보다 크다. 분기마다 다시 센다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 일회성이 GAAP 이익보다 큼 · 매 분기 재검토</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 일회성이 GAAP 이익보다 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="tsnFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">일회성이 GAAP 이익보다 큼</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]

# Fable r1: 배당 칸 — 주당 배당 태그가 없어 비었다(보도자료: 분기 $0.51 지급, 12월 15일 지급분부터 $0.52로 인상)
POST.append(r"""
h = h.replace('>주당 배당 태그 없음(배당 지급은 위 칸)</span>\n            <span class="zone-val">—</span>', '>분기 배당(Class A, 12월 15일 지급분부터 $0.52)</span>\n            <span class="zone-val">$0.51</span>', 1)
""")

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"tsn:BeefMember": ["쇠고기", "#8b1e2d"], "tsn:ChickenMember": ["닭고기", "#e31837"], "tsn:PreparedFoodsMember": ["가공식품(Jimmy Dean·Hillshire 등)", "#003da5"], "tsn:PorkMember": ["돼지고기", "#f28a8a"], "tsn:InternationalMember": ["해외·기타", "#9aa7b8"]},
 "ignore": ["tsn:IntersegmentRevenuesMember", "tsn:BeefAndPorkSegmentsMember", "us-gaap:CorporateMember", "us-gaap:CorporateAndOtherMember"]
}
