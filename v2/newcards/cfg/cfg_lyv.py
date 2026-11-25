CIK = '0001335258'
BUILD = {'no_dcf': '미완성 — 최근 4분기 희석 EPS 적자·법적 충당($450M)이 지배 순이익보다 크다'}   # 2026-11-07·08 사용자 규칙(GAAP 적자·일회성 30% 이상이면 미완성)
# LYV(라이브 네이션) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 말. 공연 기획(Concerts), 티켓 판매(Ticketmaster), 스폰서십·광고.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-05 장 마감 뒤 접수, 카드 기준일 11-17 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 16:1x~16:2x 동부 → 다음 거래일).
# 일회성(E54): 최근 4분기 희석 EPS −0.17(−1.06 − 1.85 + 1.05 + 1.69 — 2025년 4분기는 연간 −0.24 − 9개월 0.82) — 적자라 미완성.
#   지배 순이익은 +$151M(4분기 −202.1 + 2026년 9개월 353.2)로 흑자인데 EPS가 적자인 것은 상환 가능 비지배지분의 가치 조정이 보통주 몫에서 빠지기 때문(회사 "Reconciliation to net income available to common stockholders").
#   2026년 1분기 정부 조사·소송 관련 충당 $450M(본사 비용 안, 10-Q 주석 6)이 지배 순이익의 약 3배 → 일회성 기준으로도 미완성.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, -1, 0), '판정 보류'
CO = 'Live Nation'
S_ = 'https://www.sec.gov/Archives/edgar/data/1335258/'
SEC = S_
TENQ = S_ + '000133525826000053/lyv-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000133525826000052/lyv-2026q3xex991er.htm', 'q2': S_ + '000133525826000034/lyv-2026q2xex991er.htm',
      'q1': S_ + '000133525826000018/lyv-2026q1xex991er.htm', 'q4': S_ + '000133525826000007/lyv-2025q4xex991er.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="lyvFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 희석 EPS가 적자다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (-30, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 최근 4분기 GAAP 이익이 적자이거나 일회성이 30% 이상이면 판정을 보류하는데, LYV는 최근 4분기 희석 EPS가 −$0.17로 적자다. 지배 순이익은 +$151M로 흑자지만, 상환 가능 비지배지분(OCESA 등 합작 파트너 지분)의 가치 조정이 분기마다 약 $41~47M씩, 최근 4분기 합계 $176M 보통주 몫에서 빠져 보통주 몫은 −$24M이 된다. −$0.17은 분기 희석 EPS의 합이다(2025년 4분기는 계절적 적자 분기로 지배 순손실 −$202M). '
              '2026년 1분기에는 정부 조사·소송 관련 충당 $450M을 본사 비용으로 잡아 그 분기 영업손실(−$371M)이 났다 — 최근 4분기 지배 순이익보다 크다. 회사는 이 충당과 주식보상·감가상각을 뺀 자체 지표인 조정 영업이익(AOI)으로 2026년 두 자릿수 성장을 말하지만, GAAP 영업이익은 1~9월 −25%다. FTC 소송 등 남은 소송에서 충당이 더 나오면 다시 일회성으로 센다. '
              '분기마다 다시 센다. 2026년 4분기 실적(2027년 2월 예상)에서는 4분기 희석 EPS가 −$0.89보다 좋아야 최근 4분기 EPS가 흑자가 되는데(4분기는 해마다 적자 분기), 그래도 충당 분기가 남아 미완성은 유지된다. 미완성을 풀 수 있는 가장 이른 시점은 충당 분기가 빠지는 2027년 1분기 실적(5월 예상)이다. '
              '주주 자본이 작아(9월 말 지배 몫 $457M) PBR은 의미가 거의 없다. 현금 $8.3B에는 공연·티켓 대금으로 맡아 둔 고객 현금 약 $2.7B가 들어 있어(회사가 말하는 자유 현금은 $2.3B) 순현금을 그대로 회사 돈으로 읽으면 안 된다. 고객 현금을 빼면 순차입금은 약 $6.3B다. 리스는 장기 운용리스($2.16B)만 넣었고 금융리스는 차입금 안에 있다. 영업이익 대비 순차입금·EV/EBITDA는 충당 $450M이 깎은 영업이익 기준이다. 공연 매출은 계절성이 커서(2·3분기 최대, 3분기 FCF는 공연 대금이 나가 해마다 약하다) 분기 비교는 1년 전 같은 분기와 해야 한다. 10월에 $730M·€600M 채권을 냈고 일부는 기존 채권 상환에 쓴다. 순이익 차트와 이익률은 보통주 몫(가치 조정 뒤) 기준이다.')
PH = ['DIS', 'NWSA', 'CMCSA', 'GOOGL', 'META', 'CHTR']
PEER_FILE = 'peer_universe/communication_services.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '미디어·인터넷 6곳 PER 비교 (점수는 S&P500 커뮤니케이션 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 커뮤니케이션 서비스 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 커뮤니케이션 서비스 대비 배수 순위 (v2/peer_universe/communication_services.json)'
PEER_TIP = ('S&P500 커뮤니케이션 서비스(LYV 제외)와 배수 순위를 매긴 값이다.',
            '인터넷 플랫폼·미디어·통신이 섞여 있고 공연 회사는 LYV뿐이다. 차트에는 미디어·인터넷 6곳이 보인다.')
# 매출(Q3 2026 보도자료 부문): 공연 8,746.4 + 티켓 870.3 + 스폰서십·광고 505.7 = 10,122.4, 기타·제거 −17.4 → 10,105.0.
SEG = [('공연(Concerts)', 8746.4, '#d6001c'), ('티켓(Ticketmaster)', 870.3, '#1a1a1a'), ('스폰서십·광고', 505.7, '#f08a96')]
SEG_ADJ = -17.4
SEG_ADJ_LABEL = '기타·제거'
SEG_TITLE = '매출 구성 — 사업 부문별'
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('green', '2026년 11월 5일 장 마감 뒤 — Q3 2026 실적', '2026-11-06',
     '매출 $10.1B(+19%) · 영업이익 $892M(+13%) · 희석 EPS $1.69 · 관객 6,100만 명(+19%) — 다음 거래일 주가 −3.3%', 'q3', 'Live Nation 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 30일 장 마감 뒤 — Q2 2026 실적', '2026-07-31',
     '매출 $7.7B(+9%) · 영업이익 $522M(+7%) · 희석 EPS $1.05 · AOI +2%(공연 −14%, 티켓 +14%) — 다음 거래일 주가 −5.1%', 'q2', 'Live Nation 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 5일 장 마감 뒤 — Q1 2026 실적', '2026-05-06',
     '매출 $3.8B(+12%) · 법적 충당 $450M으로 영업손실 $371M · 희석 주당 손실 $1.85 · AOI $371M(+9%) — 다음 거래일 주가 +6.7%', 'q1', 'Live Nation 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 19일 장 마감 뒤 — 2025년 연간 실적', '2026-02-20',
     '연간 매출 $25.2B(+9%) · 영업이익 $1.3B(+52%) · 연간 희석 EPS −$0.24(상환 가능 비지배지분 조정) — 다음 거래일 주가 +3.3%', 'q4', 'Live Nation 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 25, 'nt': 22, 'mean': 204.59, 'median': 210, 'low': 155, 'high': 221, 'sb': 17, 'b': 3, 'h': 3, 's': 1, 'ss': 1}
ANALYST_ASOF = '2026-11-23'

NI_TAGS = ['NetIncomeLossAvailableToCommonStockholdersBasic']   # 재무 JSON 이익률(엔진 기본 = 보통주 몫)과 맞춤(Codex 2026-11-18)

ONEOFF_QUARTERS = {'2025-12-31': '희석 EPS −1.06 — 계절적 적자 분기의 지배 순손실 −$202M + 상환 가능 비지배지분 가치 조정 $45M',
                   '2026-03-31': '정부 조사·소송 관련 법적 충당 $450M(본사 비용)',
                   '2026-06-30': '없음', '2026-09-30': '없음'}

INCOMPLETE_SHORT = '법적 충당·EPS 적자'
INCOMPLETE_WHY = '최근 4분기 희석 EPS가 적자(−$0.17)이고, 2026년 1분기 정부 조사·소송 관련 법적 충당($450M)이 최근 4분기 지배 순이익($151M)보다 커서 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 가장 이른 해제 시점은 충당 분기가 빠지는 2027년 5월'
POST = [r"""
import re as _re0
_w = '최근 4분기 희석 EPS가 적자(−$0.17)이고, 2026년 1분기 정부 조사·소송 관련 법적 충당($450M)이 최근 4분기 지배 순이익($151M)보다 커서 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 가장 이른 해제 시점은 충당 분기가 빠지는 2027년 5월'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 법적 충당·EPS 적자 · 매 분기 재검토, 가장 이른 해제 2027년 5월</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 법적 충당·EPS 적자. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="lyvFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">법적 충당·EPS 적자</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"lyv:ConcertsMember": ["공연(Concerts)", "#d6001c"], "lyv:TicketingMember": ["티켓(Ticketmaster)", "#1a1a1a"], "lyv:SponsorshipAndAdvertisingMember": ["스폰서십·광고", "#f08a96"]},
 "ignore": ["us-gaap:CorporateMember"]
}
