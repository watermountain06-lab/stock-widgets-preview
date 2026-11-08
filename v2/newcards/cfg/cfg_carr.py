CIK = '0001783180'
BUILD = {'no_dcf': '미완성 — 유럽 사업 영업권 손상으로 GAAP 적자'}   # 2026-11-07 — 일회성 30% 이상(GAAP 적자) 기준으로 미완성(사용자 결정 기준)
# CARR(캐리어 글로벌) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 냉난방 공조(미주·유럽·아태 중동 아프리카) + 운송 냉장(Transicold).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-29 14:45 동부 장중 → 첫 세션 10-29, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 07:0x 동부 → 그날),
#        채권 발행 8-K(2026-11-04 16:15 동부 → 11-05). 사전 조사(2026-10-28)는 Q3 손상 전이라 일회성 27%로 봤으나 Q3 10-Q로 GAAP 적자가 돼 미완성.
# 엔진 입력(2026-11-07): 차입금 = 단기·1년 안 $1,482M + 장기 $9,992M = $11,474M, 현금 $1,354M, 비지배지분 $367M.
#   4분기 EPS는 보도자료 계속사업 희석 EPS(Q4 2024 −0.05·Q4 2025 0.03 — Q4_OVERRIDE_BASIS continuing, 총 EPS에 중단사업 매각 이익이 섞임).
# 일회성: Q3 2026 유럽 냉난방 사업부(Climate Solutions Europe) 영업권 손상 $3.1B → 분기 계속사업 EPS −3.16(조정 0.87).
#   최근 4분기 계속사업 GAAP EPS 약 −2.25(0.03 + 0.28 + 0.60 − 3.16) 대 조정 2.64(0.34 + 0.57 + 0.86 + 0.87). 손상은 2027년 3분기 10-Q부터 최근 4분기에서 빠진다.
NI_TAGS = ['NetIncomeLossFromContinuingOperationsAvailableToCommonShareholdersBasic', 'NetIncomeLoss']   # 순이익은 계속사업(2022-12부터 이 태그) — 뉴스·보도자료와 같게(Codex r1)
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Carrier Global'
S_ = 'https://www.sec.gov/Archives/edgar/data/1783180/'
SEC = S_
TENQ = S_ + '000178318026000037/carr-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000178318026000035/a99-q32026earningsexhibit.htm', 'q2': S_ + '000178318026000030/a99-q22026earningsexhibit.htm',
      'q1': S_ + '000178318026000023/a99-q12026earningsexhibit.htm', 'q4': S_ + '000178318026000005/a8-kerexhibit99xq42025.htm',
      'notes': S_ + '000121390026115944/ea0310805-8k_carrier.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="carrFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(2026년 3분기 유럽 사업 영업권 손상 $3.1B로 최근 4분기 GAAP 이익이 적자다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-40, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 2026년 3분기에 유럽 냉난방 사업부(Climate Solutions Europe)의 영업권 $3.1B를 손상 처리했다 — 회사는 유럽 수요 약화(정부 정책·보조금 변화), 보일러에서 히트펌프로의 전환 속도 변화, 금리 상승 등으로 그 사업의 예상 실적을 낮췄다고 밝혔다. '
              '그래서 3분기 계속사업 희석 EPS가 −$3.16(조정 $0.87)이고 최근 4분기 GAAP EPS가 약 −$2.25로 적자라 PER은 점수에서 빠지며, 손상이 영업이익에 들어가 EBITDA가 크게 낮아져 EV/EBITDA도 뜻이 없다(참고 점수의 자기 이력 평균에는 들어 있다). '
              '본업은 좋아지는 흐름이다 — 3분기 유기 매출 +15%, 데이터센터 주문이 약 300% 늘었고 회사 전체 수주잔고는 $8.5B를 넘었다(1년 전보다 약 60% 증가). 다만 3분기 조정 EPS $0.87에도 관세(IEEPA) 환급 순효과 약 $0.10이 들어 있다. 7월 1일 유럽의 Riello 사업을 $438M에, 8월 3일 NORESCO 사업을 팔았다(두 매각으로 연간 매출 약 $350M 감소). 2026년 전망은 3분기에 매출을 약 $23B에서 $23.8~24.0B로 올리고 조정 EPS는 약 $2.90에서 $2.85~2.90으로 좁혔다. 배당 칸의 $0.48은 6월 분기에 두 번 선언된 합계이고, 실제 분기 배당은 주당 $0.24다(10월 선언). '
              '자기 이력·동종업 점수는 참고값이고 판정은 보류한다. 손상 분기가 최근 4분기에서 빠지는 2027년 3분기 10-Q 뒤 정식 판정으로 다시 본다.')
PH = ['TT', 'JCI', 'LII', 'EMR', 'ETN', 'HON']
PEER_FILE = 'peer_universe/industrials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '건물 설비·산업재 6곳 PER 비교 (점수는 S&P500 산업재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 산업재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 산업재 대비 배수 순위 (v2/peer_universe/industrials.json)'
PEER_TIP = ('S&P500 산업재(CARR 제외)와 배수 순위를 매긴 값이다.',
            '기계·운송·국방·건설이 섞여 있다. 차트에는 냉난방·건물 설비 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 외부 매출): 미주 3,354 + 유럽 1,335 + 아태·중동·아프리카 848 + 운송 726 = 6,263.
SEG = [('냉난방 미주', 3354.0, '#0033a0'), ('냉난방 유럽', 1335.0, '#00a0df'), ('냉난방 아태·중동·아프리카', 848.0, '#7fb9e6'), ('운송 냉장', 726.0, '#c9c9c9')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(Q3는 손상이 함께 나와 손 항목) + 채권 발행. 반응일: 실적 8-K 장 전 → 그날.
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 4일 장 마감 뒤 — 채권 $1.5B 발행', '2026-11-05',
     '11월 2일 가격 결정, 4일 발행 완료 — 2029년 만기 5.000% $750M · 2033년 만기 5.350% $750M, 2027년 2월 만기 채권 상환 등 차환 용도 — 공시 다음 날 주가 −4.4%(원인은 공시에 없음)', 'notes', 'Carrier 공시 (SEC 8-K)'),
    ('neutral', '2026년 10월 29일 장 전 — Q3 2026 실적', '2026-10-29',
     '매출 $6.26B(+12%, 유기 +15%) · 계속사업 희석 EPS −$3.16(유럽 사업 영업권 손상 $3.1B) · 조정 EPS $0.87(+30%) · 데이터센터 주문 약 +300% · 회사 수주잔고 $8.5B 이상 · 조정 EPS에 관세 환급 순효과 약 $0.10 포함 · 연간 매출 전망 $23.8~24.0B로 상향, 조정 EPS $2.85~2.90 — 그날 주가 −1.3%', 'q3', 'Carrier 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 28일 장 전 — Q2 2026 실적', '2026-07-28',
     '매출 $6.4B(+4%) · 계속사업 희석 EPS $0.60(1년 전 $0.70) · 조정 EPS $0.86(−7%) · 회사 예상보다 좋았다고 발표 · 연간 전망 상향(매출 약 $23B, 조정 EPS 약 $2.90) — 그날 주가 −8.9%', 'q2', 'Carrier 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 4월 15일 — 주가 급락(회사 공시 없음)', '2026-04-15',
     '그날 주가 −9.4% — 이 시기 회사 8-K는 주총 표결 결과뿐이다(3월 26일에도 공시 없이 −7.7%)', 'q1', 'Carrier 공시 목록 (SEC)'),
    ('green', '2026년 4월 30일 장 전 — Q1 2026 실적', '2026-04-30',
     '매출 $5.3B(+2%) · 계속사업 희석 EPS $0.28(1년 전 $0.47) · 조정 EPS $0.57(−12%) · 상업용 냉난방 주문 +35%(데이터센터 +500% 이상) — 그날 주가 +8.8%', 'q1', 'Carrier 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 5일 장 전 — Q4 2025 실적', '2026-02-05',
     '매출 $4.8B(−6%, 유기 −9%) · 계속사업 희석 EPS $0.03(1년 전 −$0.05) · 조정 EPS $0.34(−37%) · 4분기 상업용 냉난방 주문 약 +50% — 그날 주가 −0.7%', 'q4', 'Carrier 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 26, 'nt': 14, 'mean': 71, 'median': 70, 'low': 60, 'high': 90, 'sb': 11, 'b': 2, 'h': 13, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-07'

# 미완성 카드 표시(2026-11-07 — 일회성 30% 이상 기준).
INCOMPLETE_SHORT = '유럽 사업 영업권 손상으로 GAAP 적자'
INCOMPLETE_WHY = '2026년 3분기에 유럽 냉난방 사업부 영업권 $3.1B를 손상 처리해 최근 4분기 GAAP 이익이 적자다 — 배수 판정이 왜곡돼 보류한다. 손상 분기가 빠지는 2027년 3분기 10-Q 뒤 다시 본다'
POST = [r"""
import re as _re0
_w = '2026년 3분기에 유럽 냉난방 사업부 영업권 $3.1B를 손상 처리해 최근 4분기 GAAP 이익이 적자다 — 배수 판정이 왜곡돼 보류한다. 손상 분기가 빠지는 2027년 3분기 10-Q 뒤 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 유럽 사업 영업권 손상으로 GAAP 적자</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 유럽 사업 영업권 손상으로 GAAP 적자. 최근 4분기 이익이 일회성 손상으로 적자라 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="carrFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">유럽 사업 영업권 손상으로 GAAP 적자</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]


# ── 자동 카드 — 부문 지도(seg_map_propose 전부 맞음). 원문 대조: Q3 2026 10-Q 3,354/1,335/848/726 = 6,263(2026-11-07) ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"carr:ClimateSolutionsAmericasSegmentMember": ["냉난방 미주", "#0033a0"], "carr:ClimateSolutionsEuropeSegmentMember": ["냉난방 유럽", "#00a0df"],
             "carr:ClimateSolutionsCSAMESegmentMember": ["냉난방 아태·중동·아프리카", "#7fb9e6"], "carr:ClimateSolutionsTransportationSegmentMember": ["운송 냉장", "#c9c9c9"]},
 "ignore": []
}
