CIK = '0001754301'
BUILD = {'no_dcf': '평가 불가 — 로쿠 인수(2026-11-06 마감)가 재무에 아직 없고, 최근 4분기 일회성이 GAAP 이익의 약 37%', 'cover_shares': True}
# FOXA(폭스) v2 카드 설정 — 자동 카드(AUTO), 평가 불가(판정 보류의 한 종류, 2026-11-19 사용자 결정: "지금 만들고 평가 불가를 달아줘").
# 회계연도 6월 30일. 케이블 네트워크(폭스 뉴스·FS1 등), 텔레비전(폭스 방송·방송국·Tubi). 2026-11-06 로쿠 인수 마감.
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-11-02 접수, 카드 기준일 11-17 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 07~09시 동부 → 그날), 로쿠 인수 8-K(06-15 장 전 발표, 11-06 장 마감 뒤 마감 공시).
# 평가 불가 이유: (1) 로쿠 인수(신주 약 1.445억 주 + 현금 약 $14.1B, 기간 대출 $2.0B·브리지 $8.4B → 11월 채권 발행(순수입 약 $8.32B)·보유 현금으로 브리지 상환)가 11-06에 끝나
#   가격(11-17)에는 로쿠가 들어 있는데 카드의 이익·차입금·주식 수(9월 말·표지)에는 없다 — 시가총액은 약 4분의 1 작게(신주 144.5 ÷ 인수 뒤 566.3M주), 차입금은 약 $10.4B 작게 잡혀 배수가 모두 어긋난다.
#   (2) 최근 4분기 GAAP 희석 EPS 4.71(0.52 + 0.38 + 1.61 + 2.20) 대 회사 조정 EPS 6.47(0.82 + 1.32 + 1.79 + 2.54) — 순 일회성 1.76(37%), 대부분 지분증권 평가손실(Flutter 등, 비영업).
# 엔진 입력(2026-11-19): 영업이익 = 세전이익 − 순이자 − 기타 비영업 − 지분법(DERIVED_OPINC — 영업이익 줄 없음), 순이익 = 보통주 귀속(EXTRA_TAGS), 표지 주식 수 클래스 A + B 합산(cover_shares).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-06-30', '2025-06-30'), 'FY2026'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Fox'
S_ = 'https://www.sec.gov/Archives/edgar/data/1754301/'
SEC = S_
TENQ = S_ + '000162828026068670/fox-20260930.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000162828026068663/foxearningsreleaseq127.htm', 'q4': S_ + '000162828026053892/foxq42026earningsrelease.htm',
      'q3': S_ + '000162828026033145/foxearningsreleaseq326.htm', 'q2': S_ + '000162828026005277/foxearningsreleaseq226.htm',
      'roku': S_ + '000119312526451888/d141597d8k.htm', 'roku_deal': S_ + '000119312526270285/d151410d8k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="foxaFairBand" title="평가 불가 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(로쿠 인수가 재무에 아직 없다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (평가 불가 — 현금흐름 보류)</span>'
Y2 = (0, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('평가 불가 카드다. 폭스는 2026년 11월 6일 로쿠 인수를 마쳤다 — 로쿠 주주에게 FOXA 약 1.445억 주(기존 주식의 약 3분의 1, 인수 뒤 지분 약 26%)와 현금 약 $14.1B를 줬다. 현금 대가 가운데 $10.4B는 기간 대출 $2.0B와 브리지 대출 $8.4B로 조달했고(브리지는 11월 13일 채권 발행 순수입 약 $8.32B와 보유 현금으로 상환), 나머지 약 $3.7B는 보유 현금 등으로 냈다. '
              '카드 기준일(11월 17일) 주가에는 로쿠가 들어 있지만, 카드의 매출·이익·차입금·주식 수는 인수 전인 9월 말·10-Q 표지 값이다. 같은 주가로 보면 카드의 시가총액은 실제보다 약 4분의 1 작고, 차입금은 약 $10.4B 작으며, 현금($4.5B)도 인수 전 값이다. 그래서 PBR·PSR·EV/EBITDA는 시가총액·차입금 때문에, PER은 이익에 로쿠 손익·새 이자 비용·신주 희석이 없어서 실제와 어긋난다. '
              '로쿠가 반영된 첫 분기(FY27 2분기, 12월 말) 10-Q가 나오는 2027년 2월(예상)에 다시 만든다. 그때도 로쿠 실적은 11월 6일 뒤 약 두 달분뿐이라 온전한 비교는 그 뒤 분기들이 쌓여야 한다. '
              '이와 별개로 최근 4분기 GAAP 희석 EPS $4.71에는 회사가 조정에서 빼는 항목이 순 주당 $1.76(약 37%) 들어 있다 — 대부분 지분증권 평가손실(Flutter 등) 같은 비영업 항목이다. '
              '손익계산서에 영업이익 줄이 없어 카드는 세전이익에서 순이자·기타 비영업 손익·지분법 손익을 빼서 영업이익으로 쓴다(회사 조정 EBITDA와 다르다). 주식 수는 클래스 A(FOXA)와 의결권 있는 클래스 B(FOX)를 더한 값이다.')
PH = ['NWSA', 'DIS', 'CMCSA', 'WBD', 'CHTR', 'NFLX']
PEER_FILE = 'peer_universe/communication_services.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '미디어 6곳 PER 비교 (점수는 S&P500 커뮤니케이션 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 커뮤니케이션 서비스 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 커뮤니케이션 서비스 대비 배수 순위 (v2/peer_universe/communication_services.json)'
PEER_TIP = ('S&P500 커뮤니케이션 서비스(FOXA 제외)와 배수 순위를 매긴 값이다.',
            '인터넷 플랫폼·미디어·통신이 섞여 있다. 차트에는 미디어·통신 6곳이 보인다. 로쿠 인수가 반영되지 않은 값이라 참고로만 본다.')
# 매출(Q1 FY27 보도자료 부문): 케이블 네트워크 1,803 + 텔레비전 2,713 = 4,516, 본사·기타 246 − 부문 간 제거 191 = +55 → 4,571.
SEG = [('텔레비전(폭스 방송·방송국·Tubi)', 2713.0, '#3a6fb0'), ('케이블 네트워크(폭스 뉴스·FS1 등)', 1803.0, '#1a1a1a')]
SEG_ADJ = 55
SEG_ADJ_LABEL = '본사·기타 − 부문 간 제거'
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(EPS는 GAAP 희석) + 로쿠 인수 발표·마감. 반응일: 실적 보도자료 장 전(07~09시 동부) → 그날, 로쿠 발표 06-15 07:13 동부 → 그날, 마감 공시 11-06 16:21 동부 → 11-09(월).
NEWS_RANGE = '2026.05 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 6일 — 로쿠 인수 마감(8-K는 장 마감 뒤 접수)', '2026-11-09',
     '로쿠 주주에게 FOXA 약 1.445억 주와 현금 약 $14.1B 지급, 기간 대출 $2.0B·브리지 $8.4B 차입(11월 13일 채권 발행으로 브리지 상환), 2년 안 연간 비용 시너지 약 $400M 목표 — 8-K 다음 거래일 주가 +1.6%(마감 당일 −1.5%)', 'roku', 'Fox 8-K·보도자료 (SEC)'),
    ('green', '2026년 11월 2일 장 전 — Q1 FY27 실적', '2026-11-02',
     '매출 $4.57B(+22%) · 순이익 $943M · 희석 EPS $2.20(1년 전 $1.32) · 조정 EPS $2.54 — 그날 주가 −0.8%', 'q1', 'Fox 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 8월 6일 장 전 — Q4 FY26 실적', '2026-08-06',
     '매출 $4.21B(+28%) · 순이익 $691M · 희석 EPS $1.61(1년 전 $1.57) · 조정 EPS $1.79 — 그날 주가 +5.3%', 'q4', 'Fox 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 6월 15일 장 전 — 로쿠 인수 합의 발표', '2026-06-15',
     '로쿠 전체를 현금·주식으로 인수하기로 합의(대규모 차입·신주 발행) — 그날 주가 −16.8%', 'roku_deal', 'Fox 8-K (SEC)'),
    ('neutral', '2026년 5월 11일 장 전 — Q3 FY26 실적', '2026-05-11',
     '매출 $3.99B(−9%) · 순이익 $166M(지분증권 평가손실 등 비영업 −$499M) · 희석 EPS $0.38(1년 전 $0.75) · 조정 EPS $1.32 — 그날 주가 +7.6%', 'q3', 'Fox 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 14, 'mean': 78.43, 'median': 80, 'low': 60, 'high': 95, 'sb': 11, 'b': 3, 'h': 7, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-21'

ONEOFF_QUARTERS = {'2025-12-31': '주당 0.30 — 비영업 0.37(지분증권 평가 등) · 구조조정·손상 0.03 · 세금 −0.10',
                   '2026-03-31': '주당 0.94 — 비영업 1.16(지분증권 평가 등) · 구조조정·손상 0.07 · 세금 −0.29',
                   '2026-06-30': '주당 0.18 — 구조조정·손상 0.26 · 비영업 −0.03 · 세금 −0.06 · 반올림 0.01',
                   '2026-09-30': '주당 0.34 — 비영업 0.33(Flutter 평가손실) · 구조조정·손상 0.04 · 세금 −0.04 · 반올림 0.01'}

INCOMPLETE_LABEL = '평가 불가'   # fill.py 표시 이름(기본 '미완성')
INCOMPLETE_SHORT = '평가 불가 — 로쿠 인수 미반영'
INCOMPLETE_WHY = '2026년 11월 6일 끝난 로쿠 인수(신주 약 1.445억 주·현금 약 $14.1B)가 주가에는 들어 있는데 카드의 이익·차입금·주식 수(9월 말)에는 없어 배수가 모두 어긋난다. 최근 4분기 일회성도 GAAP 이익의 약 37%다. 로쿠가 반영된 첫 10-Q(2027년 2월 예상) 뒤 다시 만든다'
POST = [r"""
import re as _re0
_w = '2026년 11월 6일 끝난 로쿠 인수(신주 약 1.445억 주·현금 약 $14.1B)가 주가에는 들어 있는데 카드의 이익·차입금·주식 수(9월 말)에는 없어 배수가 모두 어긋난다. 최근 4분기 일회성도 GAAP 이익의 약 37%다. 로쿠가 반영된 첫 10-Q(2027년 2월 예상) 뒤 다시 만든다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">평가 불가</span><span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">로쿠 인수가 재무에 아직 없다 · 2027년 2월(예상) 10-Q 뒤 다시 만든다</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '평가 불가 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 하지 않는다(자기 이력·동종업 점수는 인수 전 값이라 참고로만 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '평가 불가 — 로쿠 인수 미반영. 종합 판정과 함께 현금흐름 내재가치도 계산하지 않았다.')
h = _re0.sub(r'(id="foxaFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">평가 불가 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(평가 불가)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '평가 불가 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '평가 불가 — ')
h = h.replace('계산 불가 — 평가 불가 — ', '평가 불가 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">평가 불가 — 로쿠 인수 미반영</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = h.replace('미완성 카드라 종합 판정을 보류한다', '평가 불가 카드라 종합 판정을 하지 않는다')
h = h.replace('보류(미완성)', '보류(평가 불가)')
h = h.replace("'\\n미완성 카드 — 두 점수는 참고값이라 합산하지 않는다'", "'\\n평가 불가 카드(로쿠 인수 미반영) — 두 점수는 인수 전 참고값이라 합산하지 않는다'", 1)
# Fable r1 필수: 재무 건전성 구역에도 로쿠 경고, Bear에 로쿠 줄
h = h.replace('<span>재무 건전성 — 안정성·활동성 (Q1 FY27 · 2026.09.30 기준)</span></div>', '<span>재무 건전성 — 안정성·활동성 (Q1 FY27 · 2026.09.30 기준)</span></div>\n    <div class="note" style="margin:6px 0 10px;color:var(--gold);">⚠ 9월 말(로쿠 인수 전) 값이다. 11월 6일 인수로 차입금이 약 $10.4B 늘고 현금 약 $3.7B가 나가, 지금 재무 상태와 다르다.</div>', 1)
h = h.replace('<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">—</span><span class="bb-text">기준을 넘는 약세 지표가 없다.</span></div>', '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">인수</span><span class="bb-text">로쿠 인수로 차입금이 약 $10.4B 늘고 신주(기존의 약 3분의 1)가 나왔는데, 이 카드의 수치(9월 말)에는 아직 없다 — 위 강세 항목도 인수 전 기준이다.</span></div>', 1)
# 실행 때 JS가 [data-verdict]를 판정 문자열로 다시 채운다 — FOXA만 '평가 불가'로(2026-11-19 사용자 결정)
h = h.replace("FOXA_VERDICT = (!dcfIn || seated.length < 2) ? '판정 보류'", "FOXA_VERDICT = (!dcfIn || seated.length < 2) ? '평가 불가'", 1)
h = h.replace("return (js[2][1] == null || s.length < 2) ? '판정 보류'", "return (js[2][1] == null || s.length < 2) ? '평가 불가'", 1)
h = h.replace('<span class="vs-verdict" data-verdict>판정 보류</span>', '<span class="vs-verdict" data-verdict>평가 불가</span>', 1)
h = h.replace("'\\n미완성 카드 — 두 점수는 참고값이라 합산하지 않는다'", "'\\n평가 불가 카드(로쿠 인수 미반영) — 두 점수는 참고값이라 합산하지 않는다'", 1)
"""]

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"fox:TelevisionSegmentMember": ["텔레비전(폭스 방송·방송국·Tubi)", "#3a6fb0"], "fox:CableNetworkProgrammingSegmentMember": ["케이블 네트워크(폭스 뉴스·FS1 등)", "#1a1a1a"]},
 "ignore": []
}
