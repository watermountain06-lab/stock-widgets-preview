CIK = '0000034903'
BUILD = {'overlay': True, 'no_dcf': '미완성 — 최근 4분기 순이익의 약 4할이 부동산 매각 이익',
         'company_tags': [('frt:GainOnSaleOfRealEstate', 'GainOnSaleFrt', '2022-01-01'), ('frt:GainOnSaleOfRealEstateAndChangeInControlOfInterest', 'GainOnSaleFrt', '2020-01-01'),
                          ('frt:NewMarketTaxCreditTransactionIncome', 'NmtcIncomeFrt', '2022-01-01'), ('frt:DeconsolidationOfVIEGainLossAmount', 'DeconsolidationGainFrt', '2022-01-01'),
                          ('frt:CapitalExpendituresOther', 'PaymentsForCapitalImprovements', '2020-01-01')],
         'dim_facts': [('us-gaap:PreferredStockValue', 'us-gaap:StatementClassOfStockAxis', 'frt:A5.0SeriesCCumulativeRedeemablePreferredMember', 'PreferredSeriesCFrt'),
                       ('us-gaap:PreferredStockValue', 'us-gaap:StatementClassOfStockAxis', 'frt:A5417Series1CumulativeConvertiblePreferredMember', 'PreferredSeries1Frt')]}
# FRT(페더럴 리얼티) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 리츠(REIT) — 도심·교외 고급 쇼핑센터와 복합단지(Santana Row 등).
# 출처: SEC XBRL + 인라인 XBRL 보충(Q2·Q3 2026 10-Q 요약 자료 미반영 — Q3 10-Q 2026-10-30 07:33 동부 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 분기 실적은 장 전 07:3x 동부 → 그날, 연간 실적 2026-02-12는 장 마감 뒤 → 다음 날).
# 엔진 입력(2026-11-21): 영업이익 = 영업이익 줄 − 부동산 매각 이익 − NMTC 거래 이익 − 합작 연결 제외 이익(DERIVED_OPINC — 회사 고유 태그를 company_tags로), 순이익 = 보통주 귀속,
#   설비투자 = "Capital expenditures - other"(기존 부동산 개량, 9개월 $89.9M — 개발·재개발 $128.1M·인수 $85.4M 제외), 차입금 = 담보 $496.7M + 차입 $997.1M + 선순위채 $3,389.8M = $4,883.6M,
#   비지배지분 $68.0M + 상환 가능 $188.5M, 우선주 Series C $150M + 전환 Series 1 $9.8M(차원 값 — dim_facts). 4분기 EPS 2025·2024·2022·2021·2019는 보도자료 값.
# 일회성(E54): 최근 4분기 보통주 귀속 순이익 $432.7M(4분기 $127.7M + 1~9월 $304.9M, 희석 EPS 1.48+1.81+0.97+0.74 = 5.00). FFO 조정표의 매각 이익 $186.2M(4분기 72.4 + 1~9월 113.8) = 43.0%,
#   손상 $7.4M(4분기) = 1.7%, 순액 41.3% → 30% 기준을 넘어 미완성(2026-11-07 기준).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Federal Realty'
S_ = 'https://www.sec.gov/Archives/edgar/data/34903/'
SEC = S_
TENQ = S_ + '000003490326000056/frt-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000003490326000054/frt-9302026xex991.htm', 'q2': S_ + '000003490326000040/frt-6302026xex991.htm',
      'q1': S_ + '000003490326000025/frt-3312026xex991.htm', 'q4': S_ + '000003490326000016/frt-12312025xex991.htm',
      'q3old': S_ + '000003490325000062/frt-9302025xex991.htm', 'exch': S_ + '000119312526344547/d117646d8k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="frtFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 EPS의 약 4할이 부동산 매각 이익이다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (0, 60)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
BB_TAGS = ['PaymentsForRepurchaseOfEquity']   # 자사주 매입 현금 지급(9개월 $59.2M — 3분기 591,113주 약 $65.0M 매입·소각)(Codex r1)
CAPEX_LABEL = '설비투자(기존 부동산 개량)'   # 개발·재개발·인수 지출은 넣지 않는다
MODEL_NOTE = ('미완성 카드다. 최근 4분기 EPS($5.00)의 약 4할이 부동산 매각 이익이다 — 매각 이익 $186M(2025년 4분기 $72M, 2026년 1~9월 $114M — 2026년 1분기 매각 이익 $93M은 대부분 2월 Santana Row의 Misora 아파트 매각)이 보통주 순이익 $433M의 약 43%다. 이 이익을 빼면 EPS가 약 $2.9로 줄어 PER이 약 38배가 되므로, 지금 PER과 그것이 들어간 자기 이력·동종업 점수는 실제보다 싸게 보인다 — 그래서 판정을 보류한다. 2026년 1분기가 최근 4분기에서 빠지는 2027년 1분기 실적 무렵 다시 잰다(자동으로 정식이 되지는 않는다). '
              '리츠는 건물 감가상각이 커서 GAAP 순이익이 실제 현금 창출과 다르고, 업계는 보완 지표로 FFO(순이익에 부동산 감가상각·손상을 되더하고 매각 이익을 뺀 값)를 쓴다 — 페더럴의 2026년 연간 Nareit·Core FFO 전망은 주당 $7.54~7.58이다. 사이트에는 리츠 전용 평가가 아직 없다. 영업이익은 매각 이익·신시장 세액공제 거래 이익·합작 연결 제외 이익을 뺀 값(손상은 포함)으로 쓴다. '
              'FCF의 설비투자는 기존 건물 개량 지출만 넣었고 개발·재개발(1~9월 $128M)과 인수($85M)는 넣지 않았다. 비전환 우선주(Series C $150M)와 비지배지분(상환 가능 $189M 포함)은 기업가치에 더한다(전환 우선주 Series 1 $10M은 작아서 빠져 있다). 2026년 8월 교환사채 $460M(이자 3.5%, 교환가 약 $138.54)을 발행했고, 10월 1일 앨라배마 버밍햄의 쇼핑센터 The Summit을 $508M에 샀다(현금과 신용한도로 조달 — 9월 말 차입금 $4.9B에는 아직 없다).')
HEALTH_EXTRA = '쇼핑센터 매입·개발 자금을 채권·대출로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
PH = ['KIM', 'REG', 'O', 'PLD', 'WELL', 'PSA']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(FRT 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 리츠 6곳이 보인다.')
# 매출(Q3 2026 10-Q 손익계산서): 임대 수익 329.6 + 기타 부동산 수익 9.4 + 대출 이자 0.03 = 339.0. 1년 전 313.2·8.8·0.3.
SEG = [('임대 수익', 329.6, '#12355b'), ('기타 부동산 수익', 9.4, '#b2c8e2')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 손익계산서 항목별'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 10월 30일 장 전 — Q3 2026 실적', '2026-10-30',
     '보통주 순이익 $64M · 희석 EPS $0.74(1년 전 $0.69) · Nareit FFO $1.87(1년 전 $1.77) · 2026년 FFO 전망 $7.54~7.58로 상향(직전 $7.48~7.56) · 10월 1일 The Summit(버밍햄) $508M 인수 — 그날 주가 −1.1%', 'q3', 'Federal Realty 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 6일 — 교환사채 $460M 조건 확정', '2026-08-06',
     '운영 파트너십의 2031년 만기 교환사채 $460M(이자 3.5%, 교환가 약 $138.54 — 그날 종가 $117.91의 17.5% 위) 조건 확정, 8월 11일 발행 — 그날 주가 −3.2%(발표 시각은 원문에 없다)', 'exch', 'Federal Realty 공시 (SEC 8-K)'),
    ('neutral', '2026년 7월 31일 장 전 — Q2 2026 실적', '2026-07-31',
     '희석 EPS $0.97(1년 전 $1.78 — 1년 전엔 매각 이익과 일회성 세액공제 이익이 컸다) · Nareit FFO $1.88(1년 전 $1.91, 세액공제 $0.15 포함) · 연간 FFO 전망 $7.48~7.56으로 상향 — 그날 주가 0.0%', 'q2', 'Federal Realty 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 1일 장 전 — Q1 2026 실적', '2026-05-01',
     '희석 EPS $1.81(1년 전 $0.72 — Santana Row의 Misora 매각 등 매각 이익 $93M) · Nareit FFO $1.88(+10.6%) — 그날 주가 +4.0%', 'q1', 'Federal Realty 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 12일 장 마감 뒤 — 2025년 연간 실적', '2026-02-13',
     '4분기 희석 EPS $1.48(1년 전 $0.75, 매각 이익 $72M 포함) · Nareit FFO $1.84(1년 전 $1.73) · 2025년 Nareit FFO $7.22(+6.6%, 일회성 세액공제 포함 — Core FFO $7.06, +4.3%) — 다음 날 주가 0.0%', 'q4', 'Federal Realty 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 31일 장 전 — Q3 2025 실적', '2025-10-31',
     '희석 EPS $0.69(1년 전 $0.70) · Nareit FFO $1.77 — 그날 주가 +1.4%', 'q3old', 'Federal Realty 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 19, 'nt': 16, 'mean': 126.31, 'median': 126, 'low': 116, 'high': 143, 'sb': 8, 'b': 5, 'h': 6, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-23'

INCOMPLETE_SHORT = '부동산 매각 이익이 큼'
INCOMPLETE_WHY = '최근 4분기 EPS($5.00)의 약 4할이 부동산 매각 이익이다 — 매각 이익 $186M(2025년 4분기 $72M + 2026년 1~9월 $114M, 2026년 1분기 매각 이익 $93M은 대부분 2월 Santana Row의 Misora 아파트 매각)이 보통주 순이익 $433M의 약 43%(손상 $7M을 빼도 41%)라 배수 판정이 왜곡돼 보류한다. 2026년 1분기 매각 이익이 최근 4분기에서 빠지는 2027년 1분기 실적 뒤 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 EPS($5.00)의 약 4할이 부동산 매각 이익이다 — 매각 이익 $186M(2025년 4분기 $72M + 2026년 1~9월 $114M, 2026년 1분기 매각 이익 $93M은 대부분 2월 Santana Row의 Misora 아파트 매각)이 보통주 순이익 $433M의 약 43%(손상 $7M을 빼도 41%)라 배수 판정이 왜곡돼 보류한다. 2026년 1분기 매각 이익이 최근 4분기에서 빠지는 2027년 1분기 실적 뒤 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 부동산 매각 이익이 큼</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 부동산 매각 이익이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="frtFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
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
h = h.replace('합성 영업이익률(세전이익 기준)', '매각 이익 제외 영업이익률').replace('합성 영업이익(세전이익 기준)', '매각 이익 제외 영업이익')
"""]

# 배당 칸 — 보통주 배당 지급 태그가 없다(현금흐름표 한 줄이 보통주·우선주 합계 "Dividends paid to common and preferred shareholders" 1~9월 $298.2M, Fable r1)
POST.append(r'''
import re as _rd
h = _rd.sub(r'<span class="zone-label">보통주 배당 지급</span>(\s*)<span class="zone-val">공시 없음</span>', r'<span class="zone-label">배당 지급 (1~9월 — 보통주·우선주 합계)</span>\1<span class="zone-val">$298M</span>', h, count=1)
''')

AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {"us-gaap:OperatingLeaseLeaseIncome": ["임대 수익", "#12355b"],
             "frt:OtherPropertyIncome": ["기타 부동산 수익", "#b2c8e2"],
             "frt:RevenueMortgageInterest": ["기타 부동산 수익", "#b2c8e2"]},
 "other": "기타 부동산 수익",
 "ignore": []
}
