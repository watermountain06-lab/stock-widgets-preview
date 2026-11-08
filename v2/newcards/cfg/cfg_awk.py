CIK = '0001410636'
BUILD = {'no_dcf': '미완성 — Essential 합병 종결 대기'}   # 2026-11-03 사용자 결정(보류 C군 → 미완성 카드), 2026-11-07 제작
# AWK(아메리칸 워터 웍스) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 규제 상수도·하수도(Regulated Businesses) + 기타(군 기지 수도 운영 MSG 등).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-28 16:27 동부 장 마감 뒤 → 첫 세션 10-29, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — Q4 2025~Q3 2026 모두 16:2x~16:3x 장 마감 뒤 → 다음 거래일),
#        Essential 합병 발표 보도자료(8-K 2025-10-27), NJBPU 합의서 8-K(2026-11-05 16:34 장 마감 뒤 → 11-06).
# 미완성 사유: 2025-10-26 Essential Utilities(WTRG) 전액 주식 합병 계약 — WTRG 1주당 AWK 0.305주, 종결 뒤 AWK 주주 약 69%·Essential 주주 약 31%(완전 희석 기준) → 주식 수 약 45% 증가,
#   Essential의 가스 사업(요율 기반 $4.2B)도 들어온다. 주주총회 승인 2026-02-10, HSR 대기기간 만료 2026-08-14, 주 규제위원회 승인 중 켄터키·오하이오·버지니아 받음, 뉴저지는 2026-11-02 전원 합의서 제출(승인 대기).
#   회사 예상 종결 2027년 1분기 말. 인수자라 주가가 묶이지는 않지만 종결 뒤 재무가 이어지지 않는다(보류 C군 사유).
# 엔진 입력(2026-11-07): 매출은 RegulatedAndUnregulatedOperatingRevenue(Revenues 태그 2015-06 멈춤), 이자비용 InterestExpenseNonoperating(InterestExpense 2015-09 멈춤),
#   차입금 = CP $1,449M + 1년 안 장기 $898M + 장기 $13,987M = $16,334M(DEBT_TOTAL_TAG — 기본 LongTermDebt는 2020 멈춤). 상환 우선주 $3M.
# 일회성(E54): 회사 조정 항목은 합병 비용(2026 9개월 $15M, 영업비용 안)·날씨 영향·HOS 매각 대금 어음의 추가 이자수익(2025 9개월 주당 $0.11 — 2026-02-13 전액 상환) — 모두 E54 6범주 밖이라 GAAP 그대로(크기도 9개월 순이익의 2% 미만). HOS $0.11은 세전, 세후 $0.08(Codex r1).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, -1, 0), '판정 보류'
CO = 'American Water'
S_ = 'https://www.sec.gov/Archives/edgar/data/1410636/'
SEC = S_
TENQ = S_ + '000141063626000149/awk-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000141063626000150/ex991-9302026q3pressrelease.htm', 'q2': S_ + '000141063626000121/ex991-6302026q2pressrelease.htm',
      'q1': S_ + '000141063626000064/ex991-3312026q1pressrelease.htm', 'q4': S_ + '000141063626000035/ex991-12312025q4pressrelea.htm',
      'deal': S_ + '000119312525250643/d866666dex991.htm', 'nj': S_ + '000141063626000160/awk-20261102.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="awkFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(Essential 합병 종결 대기)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 50)   # 영업이익률 32~43%(Codex r2 — 0~30이면 점이 모두 축 밖)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2025년 10월 같은 수도 회사 Essential Utilities를 전액 주식으로 합병하기로 합의했다(Essential 1주당 AWK 0.305주 — 종결 뒤 기존 AWK 주주 몫 약 69%). 종결되면 주식 수가 약 45% 늘고(발표 때 완전 희석 지분 69:31로 역산) Essential의 가스 사업까지 들어와 지금 재무로 낸 판정이 이어지지 않으므로 판정을 보류한다 — 자기 이력·동종업 점수는 참고값이다. '
              '두 회사 주주총회는 2026년 2월 승인했고, 주 규제위원회 승인 등 종결 조건이 남아 있다(켄터키·오하이오·버지니아는 승인, 뉴저지는 11월 전원 합의서를 내 승인 대기). 회사는 2027년 1분기 말 종결을 예상한다. '
              '요금은 주 규제위원회가 정하는 규제 사업이라 이익이 경기보다 요금 인상 결정에 따라 움직인다. 설비투자가 영업현금흐름보다 커서(2026년 투자 계획 $3.7B, 수도 회사 인수 포함) 부족분을 차입과 신주로 메운다. '
              '2025년 이익에는 매각한 가정용 수도 보증 사업(HOS) 대금 어음의 이자수익이 들어 있었는데 2026년 2월 전액 상환돼 연결 이자수익 전체가 크게 줄었다(9개월 $67M → $18M).')
PH = ['XEL', 'DUK', 'ED', 'WEC', 'AEE', 'SO']
PEER_FILE = 'peer_universe/utilities.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '유틸리티 6곳 PER 비교 (점수는 S&P500 유틸리티 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 유틸리티 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 유틸리티 대비 배수 순위 (v2/peer_universe/utilities.json)'
PEER_TIP = ('S&P500 유틸리티(AWK 제외)와 배수 순위를 매긴 값이다.',
            '규제 전력·가스와 독립 발전사가 섞여 있고 수도 회사는 AWK뿐이다. 차트에는 규제 전력·가스 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문): Regulated Businesses 1,403 + 기타(Corporate and reconciling — 주로 군 기지 수도 운영 MSG) 107 = 1,510.
SEG = [('규제 상수도·하수도', 1403.0, '#0072ce'), ('기타(군 기지 수도 운영 등)', 107.0, '#c9c9c9')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 뉴저지 합의서 + 실적 4건(GAAP 희석 EPS). 뉴저지 항목(11-05)이 Q3 실적(10-28)보다 늦어 news_auto가 Q3를 붙이지 않으므로 Q3도 손으로 쓴다. 반응일: 장 마감 뒤 → 다음 거래일.
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 5일 장 마감 뒤 — Essential 합병 뉴저지 합의서 공개', '2026-11-06',
     '뉴저지 규제위원회(NJBPU) 심사에서 위원회 직원·소비자 대변인 등 모든 당사자와 합의서 제출(11-02) · 위원회 승인 대기 — 다음 날 주가 −1.4%', 'nj', 'American Water 공시 (SEC 8-K)'),
    ('green', '2026년 10월 28일 장 마감 뒤 — Q3 2026 실적', '2026-10-29',
     '매출 $1.51B(+4.1%) · 순이익 $387M · 희석 EPS $1.94(1년 전 $1.94) · 2027년 합병 전 단독 기준 조정 EPS 전망 $6.53~6.63 첫 제시 — 다음 날 주가 +1.7%', 'q3', 'American Water 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 29일 장 마감 뒤 — Q2 2026 실적', '2026-07-30',
     '매출 $1.36B(+6.2%) · 순이익 $315M · 희석 EPS $1.61(1년 전 $1.48) — 다음 날 주가 −0.9%', 'q2', 'American Water 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 29일 장 마감 뒤 — Q1 2026 실적', '2026-04-30',
     '매출 $1.21B(+5.7%) · 순이익 $196M · 희석 EPS $1.00(1년 전 $1.05) — 다음 날 주가 −2.7%', 'q1', 'American Water 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 18일 장 마감 뒤 — Q4 2025 실적', '2026-02-19',
     '매출 $1.27B(+5.8%) · 순이익 $238M · 희석 EPS $1.22(1년 전 $1.22) — 다음 날 주가 +0.2%', 'q4', 'American Water 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 13, 'nt': 7, 'mean': 142, 'median': 140, 'low': 127, 'high': 162, 'sb': 3, 'b': 0, 'h': 9, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-08'


# 미완성 카드 표시(2026-11-03 사용자 결정, FISV·MLM·NSC·PTC·CHRW 방식).
INCOMPLETE_SHORT = 'Essential 합병 종결 대기'
INCOMPLETE_WHY = '2025년 10월 Essential Utilities를 전액 주식으로 합병하기로 합의했다(2027년 1분기 말 종결 예상) — 종결되면 주식 수가 약 45% 늘고 가스 사업까지 들어와 지금 재무로 낸 판정이 이어지지 않는다. 종결 뒤 분기가 쌓이면 다시 본다'
POST = [r"""
import re as _re0
_w = '2025년 10월 Essential Utilities를 전액 주식으로 합병하기로 합의했다(2027년 1분기 말 종결 예상) — 종결되면 주식 수가 약 45% 늘고 가스 사업까지 들어와 지금 재무로 낸 판정이 이어지지 않는다. 종결 뒤 분기가 쌓이면 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — Essential 합병 종결 대기</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — Essential 합병 종결 대기. 합병 뒤 재무가 크게 바뀌어 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="awkFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)   # 미완성 — PER 구간 범위를 보이지 않는다(FISV·CHRW처럼)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")

h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">Essential 합병 종결 대기</span>', h, count=1)
for _id in ('awkDcfVerdict', 'awkDcfBox', 'dcfPickValue'):
    h = h.replace(f'id="{_id}">계산 불가<', f'id="{_id}">보류(미완성)<')

h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)   # 참고 점수를 약점으로 올리지 않는다
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)   # 참고 점수를 강점으로도 올리지 않는다
"""]


# ── 자동 카드 — 부문 지도(손 작성). 원문 대조: Q3 2026 10-Q 규제 사업 1,403 + 기타 107 = 1,510(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RegulatedAndUnregulatedOperatingRevenue"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"awk:RegulatedBusinessMember": ["규제 상수도·하수도", "#0072ce"]},
 "ignore": [],
 "remainder": ["기타(군 기지 수도 운영 등)", "#c9c9c9", 0.071]   # 매출 − 규제 사업(Corporate and reconciling 줄 — 주로 MSG, Q3 2026 107 = 7.1%)
}
