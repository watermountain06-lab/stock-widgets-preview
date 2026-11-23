CIK = '0001705696'
BUILD = {'no_dcf': '미완성 — 비현금 신용손실 충당금 변동이 최근 4분기 순이익의 약 33%', 'company_tags': [('vici:FinancingReceivableExcludingAccruedInterestNetInvestmentInLeaseAndLoansCreditLossExpenseReversal', 'CeclVici', '2020-01-01'), ('vici:FinancingReceivableNetInvestmentInLeaseAndLoansCreditLossExpenseReversal', 'CeclVici', '2020-01-01')]}
# VICI(비치 프로퍼티스) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 리츠(REIT) — 카지노·체험형 부동산 순임대(트리플넷, 시저스·MGM 등) + 부동산 담보 대출.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-28 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 → 다음 세션).
# 엔진 입력(2026-11-22): 영업이익 = 세전이익 + 이자비용 − 이자수익 + 신용손실 충당금 변동(DERIVED_OPINC, 충당금은 회사 고유 태그) — 손익계산서에 영업이익 줄이 없다.
#   차입금 = LongTermDebt $16,916.9M, 비지배 $427.9M, 금융리스 $860.6M은 전대 리스 자산과 짝이라 더하지 않음(build_dcf·재무점수 목록). 감가상각이 거의 없다(판매형·금융 리스 회계).
# 일회성(E54, 2026-11-22 사용자 결정 — 충당금 변동을 일회성으로): 4분기 +153.1 · 1분기 −118.8 · 2분기 +271.1 · 3분기 +458.0 = 순 $763.4M(32.5%), 비용만 $882.2M(37.6%) → 미완성.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, 0), '판정 보류'
CO = 'VICI'
S_ = 'https://www.sec.gov/Archives/edgar/data/1705696/'
SEC = S_
TENQ = S_ + '000170569626000120/vici-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000170569626000119/viciq32026earningsrelease.htm', 'q2': S_ + '000170569626000088/viciq22026earningsrelease.htm',
      'q1': S_ + '000170569626000068/viciq12026earningsrelease.htm', 'q4': S_ + '000170569626000033/viciq42025earningsrelease.htm',
      'q3old': S_ + '000170569625000130/viciq32025earningsrelease.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="viciFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(비현금 신용손실 충당금 변동이 최근 4분기 순이익의 약 33%다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (0, 110)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(골프장 등 — 순임대라 작다)'
MODEL_NOTE = ('미완성 카드다. 최근 4분기 보통주 순이익 $2,346M(EPS $2.18)이 비현금 신용손실 충당금 변동에 크게 흔들린다 — 순액 $763M(순이익의 약 33%)이 비용으로 들어갔다. 2026년 3분기 $458M 가운데 $313M은 최대 임차인 시저스 관련으로, 시저스 담보부채의 신용등급 강등과 지역·졸리엣 임대 갱신 기간(2035년 8월부터) 신용손실 재추정이 함께 들어 있고, 나머지는 임차인 주가 하락·대출 회수 가정·모형 연례 갱신에서 나왔다. 현금이 나가는 비용은 아니지만(2022년부터 쌓기만 했고 실제 손실 처리는 아직 없다) 배수 판정을 왜곡해 보류한다. 충당금을 빼면 EPS는 약 $2.87로 PER 약 8배이고, AFFO 기준으로도 낮은 편이다. '
              'VICI는 임대를 판매형 리스·리스 금융채권으로 회계 처리해 건물 감가상각이 거의 없다 — 그래서 GAAP 순이익이 사실상 FFO와 같고, 감가상각을 빼는 다른 리츠와 PER·PBR을 같은 자로 잴 수 없다(동종업 점수가 싸게 나오는 구조). 자기 이력 비교는 합병(2022년 MGP, 2023년 초 MGM Grand·Mandalay) 뒤인 2023년 5월부터만 한다. 회사는 AFFO를 주 지표로 쓴다 — 2026년 AFFO 전망은 주당 $2.47~2.48로 올렸다. 사이트에는 리츠 전용 평가가 아직 없다. '
              '영업이익은 세전이익에 이자비용을 되더하고 이자수익을 뺀 뒤 충당금 변동을 되더한 카드 계산값이다(손익계산서에 영업이익 줄이 없다). 임대료의 약 70%가 시저스와 MGM 두 임차인에게서 나온다. 2026년 4월 30일 골든 엔터테인먼트의 네바다 카지노 7곳(약 $1.15B, 2025년 11월 발표)을 인수했고, 10월 27일 자사주 매입 한도 $2.0B를 승인했다. 임차인이 직접 내는 토지 전대 리스 부채 $861M은 같은 금액의 전대 리스 자산과 짝이라 순차입금에 더하지 않았다.')
HEALTH_EXTRA = '카지노 부동산 매입 자금을 채권으로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 EBITDA 대비로 본다.'
PH = ['O', 'SPG', 'PLD', 'AMT', 'KIM', 'HST']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(VICI 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 순임대·쇼핑몰·호텔 리츠 등 6곳이 보인다.')
SEG = [('판매형 리스 수익', 556.7, '#1b365d'), ('리스 금융채권·대출 수익', 482.6, '#5b7fa6'), ('기타 수익', 19.0, '#c5d3e3'), ('골프장 운영', 7.1, '#e3eaf3')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 손익계산서 항목별'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('green', '2026년 10월 28일 장 마감 뒤 — Q3 2026 실적', '2026-10-29',
     '희석 EPS $0.31(충당금 변동 $458M 비용) · AFFO 주당 $0.62(+4.3%) · 2026년 AFFO 전망 주당 $2.47~2.48로 상향 · 분기 배당 $0.46 · 전날(10월 27일) 자사주 매입 한도 $2.0B 승인 — 다음 날 주가 +4.3%', 'q3', 'VICI 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 29일 장 마감 뒤 — Q2 2026 실적', '2026-07-30',
     '희석 EPS $0.48(충당금 변동 $271M 비용) · AFFO 주당 $0.62 · 4월 30일 골든 엔터테인먼트 네바다 카지노 7곳 인수 완료(약 $1.15B) — 다음 날 주가 −3.0%', 'q2', 'VICI 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 29일 장 마감 뒤 — Q1 2026 실적', '2026-04-30',
     '희석 EPS $0.82(충당금 환입 $119M 포함) · AFFO 주당 $0.61 · One Beverly Hills 메자닌 대출 약정 총 $1.5B(증가분 $1.05B) — 다음 날 주가 +2.1%', 'q1', 'VICI 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 25일 장 마감 뒤 — 2025년 연간 실적', '2026-02-26',
     '4분기 희석 EPS $0.57(충당금 변동 $153M 비용) · AFFO 주당 $0.60 · 2025년 11월 발표한 골든 엔터테인먼트 카지노 7곳 인수 진행 — 다음 날 주가 −1.5%', 'q4', 'VICI 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 30일 장 마감 뒤 — Q3 2025 실적', '2025-10-31',
     '희석 EPS $0.71 · AFFO 주당 $0.60(+5.3%) · 분기 배당 $0.45 — 다음 날 주가 +1.6%', 'q3old', 'VICI 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 25, 'nt': 17, 'mean': 29.4, 'median': 30, 'low': 24, 'high': 39, 'sb': 12, 'b': 4, 'h': 9, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-23'

INCOMPLETE_SHORT = '신용손실 충당금 변동이 큼'
INCOMPLETE_WHY = '최근 4분기 보통주 순이익 $2,346M(EPS 0.57+0.82+0.48+0.31 = $2.18)이 비현금 신용손실 충당금 변동에 크게 흔들린다 — 2025년 4분기 비용 $153M, 2026년 1분기 환입 $119M, 2분기 비용 $271M, 3분기 비용 $458M(그중 $313M은 시저스 담보부채 신용등급 강등과 지역·졸리엣 임대 갱신 기간 재추정, 나머지는 임차인 주가·대출 가정·모형 연례 갱신)으로 순액 $763M, 순이익의 약 33%다(비용만 약 38%). 회사도 AFFO에서 매 분기 빼는 항목이다. 배수 판정이 왜곡돼 보류한다. 충당금 변동이 순이익의 30% 아래로 줄어드는 분기에 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 보통주 순이익 $2,346M(EPS 0.57+0.82+0.48+0.31 = $2.18)이 비현금 신용손실 충당금 변동에 크게 흔들린다 — 2025년 4분기 비용 $153M, 2026년 1분기 환입 $119M, 2분기 비용 $271M, 3분기 비용 $458M(그중 $313M은 시저스 담보부채 신용등급 강등과 지역·졸리엣 임대 갱신 기간 재추정, 나머지는 임차인 주가·대출 가정·모형 연례 갱신)으로 순액 $763M, 순이익의 약 33%다(비용만 약 38%). 회사도 AFFO에서 매 분기 빼는 항목이다. 배수 판정이 왜곡돼 보류한다. 충당금 변동이 순이익의 30% 아래로 줄어드는 분기에 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 신용손실 충당금 변동이 큼</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 신용손실 충당금 변동이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="viciFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">신용손실 충당금 변동이 큼</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = h.replace('합성 영업이익률(세전이익 기준)', '카드 기준 영업이익률(충당금 변동 제외)').replace('합성 영업이익(세전이익 기준)', '카드 기준 영업이익(충당금 변동 제외)')
h = h.replace('Q3 2026 10-Q 부문 표 (SEC)', 'Q3 2026 10-Q 손익계산서 (SEC)')
"""]

AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {"us-gaap:SalesTypeLeaseInterestIncome": ["판매형 리스 수익", "#1b365d"],
             "us-gaap:InterestAndDividendIncomeOperating": ["리스 금융채권·대출 수익", "#5b7fa6"],
             "us-gaap:OtherIncome": ["기타 수익", "#c5d3e3"],
             "vici:IncomeFromGolfOperations": ["골프장 운영", "#e3eaf3"]},
 "ignore": []
}
