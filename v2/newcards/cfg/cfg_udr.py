CIK = '0000074208'
BUILD = {'no_dcf': '미완성 — 최근 4분기 순이익의 대부분이 부동산 매각 이익', 'dim_facts': [('us-gaap:PreferredStockValue', 'us-gaap:StatementClassOfStockAxis', 'us-gaap:SeriesEPreferredStockMember', 'PreferredStockSeriesEUdr')]}   # Series E 우선주는 주식 종류 차원으로만 공시 — 배수 EV·PBR의 우선주로(EV_TAGS_BY_CIK)   # 2026-11-21 일회성 기준(≥30%)으로 미완성
# UDR v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 임대 아파트 리츠(UPREIT — United Dominion Realty L.P.).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-03 15:47 동부 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 동부 오후 4시대 = 장 마감 뒤 → 다음 세션, 10-21 잠정 실적·Apollo 합작은 장 전 08:05 → 그날).
# 엔진 입력(2026-11-21): 영업이익 = 영업이익 줄 − 부동산 매각 이익(DERIVED_OPINC, KIM·O처럼), 순이익 = 보통주 귀속(EXTRA_TAGS·PREFER_TAGS),
#   설비투자 = 기존 부동산 개량 지출(9개월 $171.3M — 인수 $283.7M·개발 $78.1M·비부동산 $10.9M 제외), 차입금 = 담보 $931.5M + 무담보 $4,824.8M = $5,756.3M,
#   비지배지분 = 운영 파트너십 유닛 $799.2M(상환 가능, 7월 청산한 DownREIT 교환분 포함) + $0.3M, 우선주 Series E $43.2M(원문 차원 값 — BUILD dim_facts), 단기투자 제외. 4분기 EPS 2024·2022는 보도자료 값.
# 일회성(E54): 최근 4분기 보통주 귀속 순이익 $692.9M(4분기 $221.7M + 1~9월 $471.3M, 희석 EPS 0.67+0.57+0.21+0.67 = 2.12).
#   부동산 매각 이익 $578.2M(4분기 $195.0M + 1~9월 $383.2M, 유닛 보유자 몫을 빼기 전) = 약 83% → 30% 기준을 크게 넘어 미완성(2026-11-07 기준).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, 0), '판정 보류'
CO = 'UDR'
S_ = 'https://www.sec.gov/Archives/edgar/data/74208/'
SEC = S_
TENQ = S_ + '000007420826000087/udr-20260930x10q.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000007420826000084/udr-ex99d1.htm', 'q2': S_ + '000007420826000070/udr-20260727xex99d1.htm',
      'q1': S_ + '000007420826000045/udr-20260429xex99d1.htm', 'q4': S_ + '000007420826000009/udr-20260209xex99d1.htm',
      'q3old': S_ + '000007420825000069/udr-20251029xex99d1.htm', 'apollo': S_ + '000007420826000081/udr-ex99d2.htm',
      'prelim': S_ + '000007420826000081/udr-ex99d1.htm', 'buyback': S_ + '000007420826000052/udr-20260504xex99d1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="udrFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 EPS의 대부분이 부동산 매각 이익이다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (0, 50)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(기존 부동산 개량)'   # 인수·개발 지출은 넣지 않는다(Codex r1 2026-11-21)
MODEL_NOTE = ('미완성 카드다. 최근 4분기 EPS($2.12)의 대부분이 아파트 단지 매각 이익이다 — 매각 이익 $578M은 보통주 순이익 $693M의 약 83%(단순 비교)이고, 유닛 보유자 배분율을 적용한 추정으로도 약 78%다(리츠라 법인세는 거의 없다). 이 이익을 빼면 PER이 몇 배로 커져, 지금 PER과 그것이 들어간 자기 이력·동종업 점수는 실제보다 싸게 보인다 — 그래서 판정을 보류한다. 2026년 연간 전망에도 큰 매각 이익이 들어 있어(전망 EPS $1.58~1.60 중 매각 이익 $1.10) 2026년 1~3분기가 차례로 빠지는 2027년 2·3분기 실적 때 다시 잰다(자동으로 정식이 되지는 않는다). 3분기 매각 이익 $190M에는 내슈빌 단지를 LaSalle 합작에 넣으며 남긴 지분을 다시 잰 이익이 섞여 있다. '
              '리츠는 건물 감가상각이 커서 GAAP 순이익이 실제 현금 창출과 다르고, 업계는 FFO(순이익에 부동산 감가상각을 되더하고 매각 이익을 뺀 값)로 본다 — UDR의 2026년 연간 FFO as Adjusted 전망은 주당 $2.54~2.56이다. 사이트에는 리츠 전용 평가가 아직 없다. 영업이익은 매각 이익을 뺀 값(손상은 포함)으로 쓴다. '
              '2026년 10월 Apollo와 아파트 19곳(약 $2.0B)의 합작을 만들어 Apollo가 약 3분의 2 지분에 $1.34B를 넣었다 — UDR은 3분의 1을 갖고 연결한다(10월 30일 완료라 9월 말 재무상태표에는 아직 없다). 현금은 지분율(UDR 33%·Apollo 67%)대로 나누다가 매각·청산 때 Apollo가 원금과 목표 수익률(처음 7.0%, 뒤에 7.3%·7.6%)을 채우면 나머지가 UDR로 가고, UDR은 5~10년차에 조건부로 Apollo 지분을 되살 권리가 있다. 다음 분기부터 Apollo 몫이 비지배지분으로 잡힌다. 운영 파트너십 유닛(2026년 7월 청산한 DownREIT 교환분 포함, 상환 가능 비지배지분 $799M)은 주식 수에 넣지 않고 EV의 비지배지분으로 더했다 — PSR·PCR은 보통주 시가총액을 연결 매출·FCF와 비교한 값이다.')
HEALTH_EXTRA = '아파트 매입·보유 자금을 채권·대출로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
PH = ['EQR', 'AVB', 'MAA', 'ESS', 'CPT', 'INVH']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '아파트 리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(UDR 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 아파트·단독주택 임대 리츠 6곳이 보인다.')
# 매출(Q3 2026 10-Q 손익계산서): 임대 수익 424.6 + 합작 관리·기타 수수료 3.5 = 428.1. 1년 전 429.3·2.6.
SEG = [('임대 수익', 424.6, '#2f7d1f'), ('합작 관리·기타 수수료', 3.5, '#c6e2b8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 손익계산서 항목별'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 2일 장 마감 뒤 — Q3 2026 실적', '2026-11-03',
     '보통주 순이익 $215M · 희석 EPS $0.67(1년 전 $0.12, 대부분 단지 매각 이익) · FFOA $0.65(1년 전과 같음) · 2026년 FFOA 전망 $2.54~2.56(10월 21일 잠정 발표 때 범위를 좁히며 중간값 +$0.02) — 다음 날 주가 +0.1%', 'q3', 'UDR 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 10월 21일 장 전 — Apollo와 $2.0B 합작 발표 · 잠정 실적', '2026-10-21',
     '아파트 19곳(7,059가구, 약 $2.0B) 합작 계획 — Apollo가 약 3분의 2 지분에 $1.34B를 넣고 UDR은 3분의 1 보유·운영(10월 30일 완료). 같은 날 3분기 잠정 EPS $0.67·연간 FFOA 전망 중간값 상향 — 그날 주가 +1.8%', 'apollo', 'UDR 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 27일 장 마감 뒤 — Q2 2026 실적', '2026-07-28',
     '보통주 순이익 $68M · 희석 EPS $0.21(1년 전 $0.11) · FFOA $0.64(1년 전과 같음) · 연간 전망 상향 — 다음 날 주가 −0.7%', 'q2', 'UDR 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 4일 장 마감 뒤 — 자사주 매입 한도 확대', '2026-05-05',
     '매입 한도를 2,500만 주 늘려 모두 약 3,000만 주(당시 주가로 $1B 이상) — 다음 날 주가 +1.6%', 'buyback', 'UDR 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 29일 장 마감 뒤 — Q1 2026 실적', '2026-04-30',
     '보통주 순이익 $189M · 희석 EPS $0.57(1년 전 $0.23, 단지 4곳 매각 대금 $362M) · FFOA $0.62(+2%) — 다음 날 주가 +0.5%', 'q1', 'UDR 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 2월 9일 장 마감 뒤 — 2025년 연간 실적', '2026-02-10',
     '4분기 희석 EPS $0.67(1년 전 −$0.02) · FFOA $0.64(+2%) · 2025년 EPS $1.13 · 배당 인상 — 다음 날 주가 +4.3%', 'q4', 'UDR 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 10월 29일 장 마감 뒤 — Q3 2025 실적', '2025-10-30',
     '희석 EPS $0.12 · FFOA $0.65(+5%) — 다음 날 주가 +0.2%', 'q3old', 'UDR 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 22, 'nt': 17, 'mean': 39.88, 'median': 39, 'low': 34, 'high': 45, 'sb': 8, 'b': 1, 'h': 11, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-11-21'

INCOMPLETE_SHORT = '부동산 매각 이익이 큼'
INCOMPLETE_WHY = '최근 4분기 EPS($2.12)의 대부분이 아파트 단지 매각 이익이다 — 매각 이익 $578M이 보통주 순이익 $693M의 약 83%(단순 비교 — 유닛 배분율 적용 추정 약 78%)라 배수 판정이 왜곡돼 보류한다. 2026년 매각 이익이 최근 4분기에서 빠지는 2027년 하반기 무렵 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 EPS($2.12)의 대부분이 아파트 단지 매각 이익이다 — 매각 이익 $578M이 보통주 순이익 $693M의 약 83%(단순 비교 — 유닛 배분율 적용 추정 약 78%)라 배수 판정이 왜곡돼 보류한다. 2026년 매각 이익이 최근 4분기에서 빠지는 2027년 하반기 무렵 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 부동산 매각 이익이 큼</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 부동산 매각 이익이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="udrFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
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
h = h.replace('순차입금(리스 포함)', '순차입금').replace('차입금·리스 $', '차입금 $')
h = h.replace('Q3 2026 10-Q 부문 표 (SEC)', 'Q3 2026 10-Q 손익계산서 (SEC)')
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·', '· GAAP 기준(영업이익은 부동산 매각 이익 제외) · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·')
h = h.replace('합성 영업이익률(세전이익 기준)', '매각 이익 제외 영업이익률').replace('합성 영업이익(세전이익 기준)', '매각 이익 제외 영업이익')
"""]

AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {"us-gaap:OperatingLeaseLeaseIncome": ["임대 수익", "#2f7d1f"],
             "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax": ["합작 관리·기타 수수료", "#c6e2b8"]},
 "ignore": []
}
