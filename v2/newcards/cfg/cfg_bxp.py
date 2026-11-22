CIK = '0001037540'
BUILD = {'overlay': True, 'no_dcf': '미완성 — 최근 4분기 순이익의 4할 넘게 부동산 매각 이익'}
# BXP(옛 Boston Properties) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 리츠(REIT) — 보스턴·뉴욕·샌프란시스코·워싱턴 등 도심 프리미엄 오피스(UPREIT).
# 출처: SEC XBRL + 인라인 XBRL 보충(Q3 2026 10-Q 2026-11-06 요약 자료 미반영, 카드 기준일 11-20 종가), 실적 자료(8-K 2.02항 supplemental — 모두 장 마감 뒤 → 다음 세션).
# 엔진 입력(2026-11-21): 영업이익 = 매출 − 비용 합계(DERIVED_OPINC — 합작 손익·매각 이익·손상·이자는 회사 배치대로 밖), 순이익 = BXP 보통주 귀속,
#   설비투자 = 건물·개발 전 개량 + 임차인 개선(SUM_TAGS_BY_CIK, 9개월 $84.7M + $289.9M — 공사 중 개발 $574.0M·인수 제외), 차입금 6줄 합 $16,590.5M(담보·선순위·교환사채·신용한도·기간 대출·CP),
#   비지배지분 = 운영 파트너십 유닛 $555.1M + 부동산 파트너십 $2,057.3M, 금융리스 $351.0M. 4분기 EPS 2024는 실적 자료 값.
# 일회성(E54): 최근 4분기 보통주 귀속 순이익 $533.1M(4분기 248.5 + 101.6 + 68.6 + 114.5). FFO 조정표의 매각 이익: 연결 187.3(156.4·13.4·7.0·10.4) + 합작 매각·연결 93.8(51.4·41.2·1.2·0) = $281.1M = 52.7%(유닛 몫 조정 전),
#   손상 $34.9M → 순액 46.2%, 분기별 BXP 귀속률로 어림하면 약 41.6% → 미완성(Codex r1 재계산).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, 0), '판정 보류'
CO = 'BXP'
S_ = 'https://www.sec.gov/Archives/edgar/data/1037540/'
SEC = S_
TENQ = S_ + '000103754026000043/bxp-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000103754026000041/q32026supplemental.htm', 'q2': S_ + '000103754026000031/q22026supplemental.htm',
      'q1': S_ + '000103754026000015/q12026supplemental.htm', 'q4': S_ + '000103754026000003/q42025supplemental.htm',
      'q3old': S_ + '000103754025000010/q32025supplemental.htm', 'sumner': S_ + '000103754026000026/bxp-20260527.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="bxpFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 EPS의 절반가량이 부동산 매각 이익이다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (0, 50)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(개량·임차인 개선)'   # 공사 중 개발·인수는 넣지 않는다
MODEL_NOTE = ('미완성 카드다. 최근 4분기 보통주 순이익 $533M(EPS $3.34)의 절반가량이 부동산 매각 이익이다 — 연결 매각 이익 $187M(대부분 2025년 4분기 $156M)과 합작사 매각·연결 이익 $94M(2025년 4분기 $51M, 2026년 1분기 $41M), 합계 $281M이다(유닛 보유자 몫 조정 전 약 53%, 손상 $35M을 빼도 약 46%, 유닛 몫을 어림해 빼도 약 42%). 이 이익을 빼면 PER이 크게 올라 PER 순위가 맞지 않는다 — 그래서 판정을 보류한다. 2025년 9월 투자자의 날에 밝힌 자산 매각 계획(2026년 5월 워싱턴 Sumner Square $63M 매각 계약 등)이 이어져 매각 이익이 다시 나올 수 있다. 2025년 4분기가 빠지는 2026년 4분기 실적 뒤 다시 잰다(회사의 2026년 EPS 전망 $2.35~2.37 기준이면 매각 이익 비중이 줄어든다). 배당은 2025년 9월 분기 $0.98에서 $0.70으로 줄였다. '
              '리츠는 업계가 보완 지표로 FFO를 쓴다 — BXP의 2026년 연간 FFO 전망은 주당 $7.06~7.08이다(3분기 $1.89). 사이트에는 리츠 전용 평가가 아직 없다. 영업이익은 매출에서 비용 합계(감가상각 포함)를 뺀 값이고 합작 손익·매각 이익·손상·이자는 넣지 않았다. '
              '차입금은 담보·선순위채·교환사채·신용한도·기간 대출·기업어음 여섯 줄 합($16.6B)이다. FCF의 설비투자는 건물 개량과 임차인 개선만 넣었고 공사 중 개발(1~9월 $574M)은 넣지 않았다 — 개발을 넣으면 FCF가 0 근처라, 지금 FCF·PCR(동종업 PCR 1위)은 이 정의 때문에 넉넉해 보인다. 9월 말 차입금은 10월 1일 2.75% 채권 $1.0B 상환(8월 6.05% 채권 $700M으로 차환) 전 값이고, 10월 GM 빌딩 임차인 Weil, Gotshal & Manges가 청산을 권고했다. 합작 파트너 몫(부동산 파트너십 $2.1B)과 운영 파트너십 유닛($0.6B)은 기업가치에 더한다.')
HEALTH_EXTRA = '오피스 매입·개발 자금을 채권·대출로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
PH = ['ARE', 'KIM', 'O', 'PLD', 'WELL', 'DLR']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(BXP 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 리츠 6곳이 보인다.')
SEG = [('임대 수익', 846.2, '#1565c0'), ('주차·기타', 38.3, '#3fa9f5'), ('호텔', 13.2, '#7fc4f8'), ('개발·관리 서비스', 9.8, '#bcdcf7'), ('관리 계약 인건비 상환', 4.0, '#dbeafb')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 손익계산서 항목별'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 10월 27일 장 마감 뒤 — Q3 2026 실적', '2026-10-28',
     '보통주 순이익 $114M · 희석 EPS $0.71(1년 전 −$0.77, 매각 이익 $10M 덕에 전망 상회) · FFO $1.89(직전 분기 $1.78) · 2026년 FFO 전망 $7.06~7.08 — 다음 날 주가 +1.0%', 'q3', 'BXP 실적 자료 (SEC 8-K)'),
    ('green', '2026년 7월 28일 장 마감 뒤 — Q2 2026 실적', '2026-07-29',
     '희석 EPS $0.43(손상 $18M 포함) · FFO $1.78 · 연간 FFO 전망 $6.99~7.05로 상향 — 다음 날 주가 +4.3%', 'q2', 'BXP 실적 자료 (SEC 8-K)'),
    ('red', '2026년 5월 29일 장 마감 뒤 — Sumner Square 매각 계약·손상', '2026-06-01',
     '자산 매각 계획에 따라 워싱턴 Sumner Square를 $63M에 파는 계약(5월 27일) — 손상을 잡는다는 8-K(2.06항) — 다음 거래일 주가 −1.5%', 'sumner', 'BXP 공시 (SEC 8-K)'),
    ('red', '2026년 4월 28일 장 마감 뒤 — Q1 2026 실적', '2026-04-29',
     '희석 EPS $0.64(합작 매각 이익 $41M 등 매각 이익 포함) · FFO $1.59(직전 분기 $1.76) — 다음 날 주가 −2.6%', 'q1', 'BXP 실적 자료 (SEC 8-K)'),
    ('red', '2026년 1월 27일 장 마감 뒤 — 2025년 연간 실적', '2026-01-28',
     '4분기 보통주 순이익 $248M · 희석 EPS $1.56(매각 이익 $156M·합작 매각·연결 이익 $51M 포함, 1년 전 −$1.45) · FFO $1.76 · 2026년 FFO 전망 $6.88~7.04 — 다음 날 주가 −1.6%', 'q4', 'BXP 실적 자료 (SEC 8-K)'),
    ('red', '2025년 10월 28일 장 마감 뒤 — Q3 2025 실적', '2025-10-29',
     '희석 EPS −$0.77(합작 손실·손상 포함) · FFO $1.74 — 다음 날 주가 −5.0%', 'q3old', 'BXP 실적 자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 22, 'nt': 16, 'mean': 72.19, 'median': 70, 'low': 60, 'high': 85, 'sb': 7, 'b': 4, 'h': 11, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-22'

INCOMPLETE_SHORT = '부동산 매각 이익이 큼'
INCOMPLETE_WHY = '최근 4분기 보통주 순이익 $533M(EPS 1.56+0.64+0.43+0.71 = $3.34)의 절반가량이 부동산 매각 이익이다 — 연결 매각 이익 $187M과 합작사 매각·연결 이익 $94M(2025년 4분기 $51M, 2026년 1분기 $41M) 등 $281M(유닛 보유자 몫 조정 전 약 53%, 손상 $35M을 빼도 약 46%, 유닛 몫을 어림해 빼도 약 42%)이라 배수 판정이 왜곡돼 보류한다. 2025년 4분기가 최근 4분기에서 빠지는 2026년 4분기 실적(2027년 1월 말) 뒤 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 보통주 순이익 $533M(EPS 1.56+0.64+0.43+0.71 = $3.34)의 절반가량이 부동산 매각 이익이다 — 연결 매각 이익 $187M과 합작사 매각·연결 이익 $94M(2025년 4분기 $51M, 2026년 1분기 $41M) 등 $281M(유닛 보유자 몫 조정 전 약 53%, 손상 $35M을 빼도 약 46%, 유닛 몫을 어림해 빼도 약 42%)이라 배수 판정이 왜곡돼 보류한다. 2025년 4분기가 최근 4분기에서 빠지는 2026년 4분기 실적(2027년 1월 말) 뒤 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 부동산 매각 이익이 큼</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 부동산 매각 이익이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="bxpFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
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
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(개량·임차인 개선) ·', '· 매출·순이익은 GAAP, 영업이익은 카드 계산값(매출 − 비용 합계) · FCF는 영업현금흐름 − 설비투자(개량·임차인 개선) ·')
h = h.replace('합성 영업이익률(세전이익 기준)', '카드 기준 합성 영업이익률(매출 − 비용)').replace('합성 영업이익(세전이익 기준)', '카드 기준 합성 영업이익(매출 − 비용)')
"""]

AUTO = True
SEG_MAP = {
 "parts": [
  {"concepts": [], "axis": None, "extra": {}, "members": {"us-gaap:OperatingLeaseLeaseIncome": ["임대 수익", "#1565c0"]}},
  {"concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"], "axis": "srt:ProductOrServiceAxis", "extra": {},
   "members": {"bxp:ParkingandOtherMember": ["주차·기타", "#3fa9f5"], "srt:HotelMember": ["호텔", "#7fc4f8"],
               "us-gaap:ManagementServiceMember": ["개발·관리 서비스", "#bcdcf7"], "us-gaap:RealEstateOtherMember": ["관리 계약 인건비 상환", "#dbeafb"]}}
 ]
}
