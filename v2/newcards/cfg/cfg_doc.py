CIK = '0000765880'
BUILD = {'no_dcf': '미완성 — 최근 4분기 순이익의 약 3분의 2가 매각·지배력 변경 이익'}
# DOC(헬스피크 프로퍼티스) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 리츠(REIT) — 외래 의료 건물·생명과학 연구소·시니어 주거(2026년 3월 Janus Living 상장, 81.6% 보유).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-03 접수, 카드 기준일 11-20 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 → 다음 세션).
# 엔진 입력(2026-11-22): 영업이익 = 매출 − 비용 합계 + 이자(DERIVED_OPINC — 손상·거래 비용은 영업 안, 매각 이익·지배력 변경 이익(기타 영업외)·합작 손익은 밖), 순이익 = 보통주 귀속,
#   설비투자 = 임대 비용·임차인 개선·반복 설비투자(9개월 $103.7M — 개발·재개발 $444.1M·인수 $2,307.3M 제외; 연간에만 있는 PaymentsToAcquireProductiveAssets 제외), 차입금 $9,382.3M(신용한도·CP·기간 대출·선순위채·담보),
#   비지배지분 $2,912.0M(Janus Living 공모분 $1,270.5M + 합작 $1,283.5M + 유닛 $357.9M) + 상환 가능 $27.4M. 4분기 EPS 2024·2020·2019는 보도자료 값.
# 일회성(E54): 최근 4분기 보통주 귀속 순이익 $377.1M(4분기 $113.8M + 1~9월 $263.3M). 매각 이익 $117.1M(4분기 56.4 + 1~9월 60.7) + 지배력 변경 이익 $138.3M(1분기 138.1 + 2분기 0.2 — 기타 영업외 $139.8M 중) ≈ $255M = 약 68% → 미완성.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 1, 0), '판정 보류'
CO = 'Healthpeak'
S_ = 'https://www.sec.gov/Archives/edgar/data/765880/'
SEC = S_
TENQ = S_ + '000162828026069522/peak-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000162828026068878/ex99109302026.htm', 'q2': S_ + '000162828026052608/ex99106302026.htm',
      'q1': S_ + '000162828026030561/ex99103312026.htm', 'q4': S_ + '000162828026004623/ex99112312025.htm',
      'q3old': S_ + '000162828025046095/ex99109302025.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="docFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 EPS의 약 3분의 2가 매각·지배력 변경 이익이다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (0, 30)
ACT_REASON = '리츠라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '투자'
CAPEX_LABEL = '설비투자(임대·임차인 개선·반복)'   # 개발·재개발·인수는 넣지 않는다
MODEL_NOTE = ('미완성 카드다. 최근 4분기 보통주 순이익 $377M(EPS $0.54)의 약 3분의 2가 일회성 이익이다 — 부동산 매각 이익 $117M과 2026년 1~9월 지배력 변경 이익 $138M(외래 의료 건물 6동 지분 80% 매각 약 $92M, 시니어 주거 합작 잔여 지분 46.5% 인수 약 $46M) — 연결 기준 합계가 보통주 순이익의 약 68%다. 이 이익을 빼면 PER이 크게 올라 PER 순위가 맞지 않는다 — 그래서 판정을 보류한다. 2026년 1분기가 빠지는 2027년 1분기 실적 뒤 다시 잰다. '
              '2026년 3월 시니어 주거 자회사 Janus Living(NYSE: JAN)을 상장해 약 $880M을 모았고 6·8월 추가 공모까지 1~9월 순 $2.1B를 조달했다(상장 직후 81.6%, 9월 말 69.2% 보유, 계속 연결). 시니어 주거 매출 증가(3분기 거주자 매출 $268M, 1년 전 $150M)는 인수와 합작 잔여 지분 인수로 연결 범위가 넓어진 덕이 크다. 공모 투자자 몫은 장부가 비지배지분($1.27B)이다. 7월에는 외래 의료 건물 86동을 합작으로 넘겨 Brookfield가 49%를 약 $1.0B에 샀다(전체 가치 약 $2.1B, 계속 연결) — 그래서 3분기에는 비지배지분 몫 이익이 보통주 순이익보다 컸고, 연결 매출·FCF 가운데 남의 몫이 늘어 PSR·PCR의 과거 비교가 덜 맞는다. 2024년 3월 Physicians Realty 합병 직후 1년의 배수 이력에는 합병 전 이익이 섞여 있다. 시니어 주거 인수 등 1~9월 부동산 인수가 $2.3B다. '
              '리츠는 업계가 보완 지표로 FFO를 쓴다 — 헬스피크의 2026년 FFO as Adjusted 전망은 주당 $1.76~1.78(GAAP EPS 전망은 $0.39~0.41로 낮췄다)이다. 사이트에는 리츠 전용 평가가 아직 없다. 영업이익은 매출에서 비용 합계를 빼고 이자를 되더한 값이다(손상·거래 비용 포함, 매각·지배력 변경 이익 제외).')
HEALTH_EXTRA = '의료 시설 매입·개발 자금을 채권·대출로 조달하는 리츠라 차입금 비중이 높게 나온다 — 리츠는 보통 부채를 자산 가치나 EBITDA 대비로 본다.'
PH = ['WELL', 'ARE', 'O', 'PLD', 'KIM', 'DLR']
PEER_FILE = 'peer_universe/real_estate.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '리츠 6곳 PER 비교 (점수는 S&P500 부동산 기준)', 'pbr': '리츠 PBR 비교', 'psr': '리츠 PSR 비교',
                'pcr': '리츠 PCR(FCF) 비교', 'evebitda': '리츠 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 부동산 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 부동산 대비 배수 순위 (v2/peer_universe/real_estate.json)'
PEER_TIP = ('S&P500 부동산(DOC 제외)과 배수 순위를 매긴 값이다.',
            '물류·데이터센터·의료·쇼핑몰·주택 리츠와 부동산 서비스가 섞여 있다. 차트에는 리츠 6곳이 보인다.')
SEG = [('임대 수익', 545.4, '#0b4f8a'), ('시니어 주거 거주자 매출', 268.3, '#4d8cc4'), ('이자·기타', 7.2, '#b5d0ea')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 손익계산서 항목별'
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 2일 장 마감 뒤 — Q3 2026 실적', '2026-11-03',
     '희석 EPS $0.02(1년 전 −$0.17) · FFO as Adjusted $0.44 · 2026년 FFO as Adjusted 전망 $1.76~1.78로 상향, GAAP EPS 전망은 $0.39~0.41로 하향 — 다음 날 주가 +0.4%', 'q3', 'Healthpeak 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 4일 장 마감 뒤 — Q2 2026 실적', '2026-08-05',
     '희석 EPS $0.08 · FFO as Adjusted $0.46 — 다음 날 주가 +0.8%', 'q2', 'Healthpeak 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 5일 장 마감 뒤 — Q1 2026 실적 · 전망 상향', '2026-05-06',
     '희석 EPS $0.28(지배력 변경 이익 $138M·매각 이익 $51M 포함) · FFO as Adjusted $0.45 · 3월 Janus Living 상장($880M 조달, 81.6% 보유)과 함께 2026년 전망 상향 — 다음 날 주가 +18.1%', 'q1', 'Healthpeak 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 2일 장 마감 뒤 — 2025년 연간 실적', '2026-02-03',
     '4분기 희석 EPS $0.16(매각 이익 포함) · FFO as Adjusted $0.47 · 월 배당 $0.10167(연 $1.22) — 다음 날 주가 −2.8%', 'q4', 'Healthpeak 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 23일 장 마감 뒤 — Q3 2025 실적', '2025-10-24',
     '희석 EPS −$0.17(연구소 합작 2곳의 투자 손상 $176M 포함) · FFO as Adjusted $0.46 — 다음 날 주가 +1.2%', 'q3old', 'Healthpeak 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 22, 'nt': 13, 'mean': 21.92, 'median': 22, 'low': 20, 'high': 24, 'sb': 5, 'b': 3, 'h': 14, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-22'

INCOMPLETE_SHORT = '매각·지배력 변경 이익이 큼'
INCOMPLETE_WHY = '최근 4분기 보통주 순이익 $377M(EPS 0.16+0.28+0.08+0.02 = $0.54)의 약 3분의 2가 일회성 이익이다 — 부동산 매각 이익 $117M(2025년 4분기 $56M, 2026년 1~9월 $61M)과 2026년 1~9월 지배력 변경 이익 $138M(외래 의료 건물 6동 지분 80% 매각 약 $92M, 시니어 주거 합작 잔여 지분 46.5% 인수 약 $46M)이다. 배수 판정이 왜곡돼 보류한다. 2026년 1분기가 최근 4분기에서 빠지는 2027년 1분기 실적 뒤 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 보통주 순이익 $377M(EPS 0.16+0.28+0.08+0.02 = $0.54)의 약 3분의 2가 일회성 이익이다 — 부동산 매각 이익 $117M(2025년 4분기 $56M, 2026년 1~9월 $61M)과 2026년 1~9월 지배력 변경 이익 $138M(외래 의료 건물 6동 지분 80% 매각 약 $92M, 시니어 주거 합작 잔여 지분 46.5% 인수 약 $46M)이다. 배수 판정이 왜곡돼 보류한다. 2026년 1분기가 최근 4분기에서 빠지는 2027년 1분기 실적 뒤 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 매각·지배력 변경 이익이 큼</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 매각·지배력 변경 이익이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="docFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">매각·지배력 변경 이익이 큼</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = h.replace('Q3 2026 10-Q 부문 표 (SEC)', 'Q3 2026 10-Q 손익계산서 (SEC)')
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·', '· GAAP 기준(영업이익은 부동산 매각 이익 제외) · FCF는 영업현금흐름 − 설비투자(기존 부동산 개량) ·')
h = h.replace('순차입금(리스 포함)', '순차입금').replace('차입금·리스 $', '차입금 $')
h = h.replace('합성 영업이익률(세전이익 기준)', '카드 기준 합성 영업이익률(매출 − 비용 + 이자)').replace('합성 영업이익(세전이익 기준)', '카드 기준 합성 영업이익(매출 − 비용 + 이자)')
h = h.replace('· GAAP 기준 · FCF는 영업현금흐름 − 설비투자(임대·임차인 개선·반복) ·', '· 매출·순이익은 GAAP, 영업이익은 카드 계산값(매각·지배력 변경 이익 제외) · FCF는 영업현금흐름 − 설비투자(임대·임차인 개선·반복) ·')
"""]

AUTO = True
SEG_MAP = {
 "concepts": [],
 "axis": None,
 "extra": {},
 "members": {"us-gaap:OperatingLeaseLeaseIncome": ["임대 수익", "#0b4f8a"],
             "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax": ["시니어 주거 거주자 매출", "#4d8cc4"],
             "us-gaap:InterestIncomeOperating": ["이자·기타", "#b5d0ea"]},
 "ignore": []
}
