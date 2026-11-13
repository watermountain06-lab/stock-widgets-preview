CIK = '0000040704'
BUILD = {'no_dcf': '미완성 — FY26 4분기 영업권·상표 손상과 브라질 사업 평가손실로 최근 4분기 GAAP가 적자'}   # 2026-11-08 사용자 규칙(일회성이 GAAP를 적자로 만들면 미완성)
# GIS(제너럴 밀스) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 5월 마지막 일요일(FY26 = 2026-05-31, 53주). 시리얼·스낵·반려동물 사료(Blue Buffalo)·외식.
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-09-23 15:44 동부 장중 → 그날, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 07:0x~07:0x 동부 → 그날),
#        COO 선임(2026-05-06 17:17 동부 → 05-07), CEO 승계(2026-09-30 07:33 동부 → 그날).
# 엔진 입력(2026-11-08): 차입금 $13,615.6M(단기 201.6 + 1년 안 1,046.8 + 장기 12,367.2 — DEBT_TOTAL_TAG, 기본은 1년 안 몫이 빠졌다), 현금 $433.1M.
#   4분기 EPS FY26은 보도자료(Q4_EPS_OVERRIDE — 역산 −3.72, 보도자료 −3.74). 이자비용은 순이자(fetch_financials), 장기차입 태그 LongTermDebtAndCapitalLeaseObligations.
# 일회성(E54): 최근 4분기 GAAP 희석 EPS −1.66(0.78 + 0.56 − 3.74 + 0.74) 대 회사 조정 EPS 3.44(1.10 + 0.64 + 0.95 + 0.75).
#   Q4 FY26(2026-05-31) 영업권 손상 $1.5B + 브랜드 무형자산 손상 약 $0.3B + 브라질 사업 매각 예정 평가손실 $1.0B(모두 비현금, 세전) → GAAP를 적자로 만든다.
CUR, YO, QO = '2026-08-30', '2025-08-24', '2026-05-31'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-05-31', '2025-05-25'), 'FY2026'
VOTES, VERDICT = (1, 0, 0), '판정 보류'
CO = 'General Mills'
S_ = 'https://www.sec.gov/Archives/edgar/data/40704/'
SEC = S_
TENQ = S_ + '000162828026063201/gis-20260830.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000162828026063141/a20260923ex99.htm', 'q4': S_ + '000162828026046337/a20260701ex99.htm',
      'q3': S_ + '000162828026019020/a20260318ex99.htm', 'q2': S_ + '000162828025057486/gis-20251217xex99.htm',
      'ceo': S_ + '000162828026063892/ex99.htm', 'coo': S_ + '000162828026031456/a20260506ex99.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="gisFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 GAAP가 손상·평가손실로 적자)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-60, 40)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 일회성이 최근 4분기 GAAP 이익을 적자로 만들면 판정을 보류하는데, GIS는 FY26 4분기(2026년 3~5월)에 영업권 $1.5B·상표 $250M(Nudges·True Chews) 손상(할인율 상승 탓)과 브라질 사업 매각 예정 평가손실 $1.0B를 잡아(모두 비현금) 최근 4분기 GAAP 희석 EPS가 −$1.66이다(회사 조정 EPS는 $3.44). '
              '손상 분기는 FY27 4분기 실적(2027년 6월 말~7월 초 예상) 때 최근 4분기에서 빠지며, 그때 GAAP 흑자 여부와 남은 일회성(2분기 상표 손상 $53M·브라질 추가 손실 $24M 등)을 다시 확인한다. '
              '본업 이익은 줄고 있다 — 회사는 FY26에 가격 투자와 투입원가 상승으로 조정 영업이익이 −16%였고, FY27도 유기 매출 −1.5%~+0.5%, 조정 영업이익 −8~−13%, 조정 EPS $3.00~3.20을 예상한다(53주 기저·인센티브 정상화·사업 매각 영향 포함). '
              'Q1 FY27 매출은 $4.39B(−3%, 미국 요구르트 매각 영향, 유기 기준 보합), 조정 EPS $0.75(−13%)였다. '
              '비용 절감으로 FY2030까지 누적 $3B(FY27 $750M 이상, 2025년 9월 공장 3곳 폐쇄 포함)를 목표로 한다. FY26 4분기에 €1.7B 후순위 하이브리드채(4.75~5.25%)로 만기 채권을 갈아탔다. 참고 점수의 EV/EBITDA가 매우 높게 나오는 것은 최근 4분기 EBITDA에 비현금 손상·평가손실 $2.8B가 들어가 부풀려진 값이고, 부채비율 306%도 손상으로 자본이 줄어 커진 값이다. 브라질 사업 매각은 2026년 9월 2일 끝났다. '
              'COO Dana McNabb가 2027년 1월 1일 CEO가 되고 Jeff Harmening은 이사회 의장(집행)으로 물러난다(9월 30일 발표). Q1 FY27에는 자사주를 사지 않았다(1년 전 $500M). '
              '이사회에는 1월 Joan Bottarini(Hyatt CFO)가 합류했고 Steve Odland가 9월 주총에서 물러났다. 주가는 2월 고점 약 $49에서 10월 초 약 $32까지 내렸다. 최근 4분기 GAAP가 적자라 PER 숫자는 나오지 않으며, 평가와 평균에서 뺀다.')
PH = ['SJM', 'KHC', 'HSY', 'MKC', 'HRL']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '포장 식품 5곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(GIS 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·생활용품·유통이 섞여 있다. 차트에는 포장 식품 5곳만 보인다.')
# 매출(Q1 FY27 보도자료 부문): 북미 소매 2,451.8 + 해외 794.3 + 북미 반려동물 612.8 + 북미 외식 523.1 = 4,382.0, 본사·기타 7.5 → 4,389.5.
SEG = [('북미 소매(시리얼·스낵·냉장)', 2451.8, '#0b3d91'), ('해외', 794.3, '#f5b335'), ('북미 반려동물(Blue Buffalo)', 612.8, '#6d8fc7'), ('북미 외식', 523.1, '#d7dfee')]
SEG_ADJ = 7.5
SEG_TITLE = '매출 구성 — 부문별(본사·기타 $7.5M 제외)'
# 손 뉴스: 실적 4건 + COO·CEO 승계. 반응일: 장 전 → 그날, 장 마감 뒤 → 다음 날. 색은 사건 성격, 수치는 그날 주가.
NEWS_RANGE = '2025.12 ~ 2026.09'
NEWS = [
    ('neutral', '2026년 9월 30일 장 전 — CEO 승계 발표', '2026-09-30',
     'COO Dana McNabb가 2027년 1월 1일 CEO로, Jeff Harmening은 집행 의장으로 — 그날 주가 −4.9%', 'ceo', 'General Mills 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 9월 23일 장 전 — Q1 FY27 실적', '2026-09-23',
     '매출 $4.39B(−3%, 유기 보합) · GAAP 희석 EPS $0.74 · 조정 EPS $0.75(−13%) · FY27 전망 유지(조정 EPS $3.00~3.20) — 그날 주가 +1.0%', 'q1', 'General Mills 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 7월 1일 장 전 — FY26 4분기 실적 · FY27 전망', '2026-07-01',
     '4분기 GAAP 희석 EPS −$3.74(영업권·상표 손상 $1.8B, 브라질 평가손실 $1.0B) · 조정 EPS $0.95(+27%) · FY27 조정 EPS $3.00~3.20 · FY2030까지 비용 절감 $3B — 그날 주가 +8.5%', 'q4', 'General Mills 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 6일 장 마감 뒤 — COO 선임', '2026-05-07',
     '북미 소매·반려동물 사장 Dana McNabb를 6월 1일부터 COO로, 이사회에도 합류 — 다음 날 주가 +1.8%', 'coo', 'General Mills 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 18일 장 전 — Q3 FY26 실적', '2026-03-18',
     '매출 $4.4B(−8%, 유기 −3%) · GAAP 희석 EPS $0.56(−50%) · 조정 EPS $0.64(−37%) · 연간 전망 유지 — 그날 주가 −3.0%', 'q3', 'General Mills 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 17일 장 전 — Q2 FY26 실적', '2025-12-17',
     '매출 $4.9B(−7%, 유기 −1%) · GAAP 희석 EPS $0.78(−45%) · 조정 EPS $1.10(−21%) · 연간 전망 유지 — 그날 주가 +3.4%', 'q2', 'General Mills 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 19, 'nt': 16, 'mean': 36.13, 'median': 35, 'low': 30, 'high': 45, 'sb': 1, 'b': 3, 'h': 11, 's': 2, 'ss': 2}
ANALYST_ASOF = '2026-11-08'

# 파이프라인 자동 재판정용 — 일회성이 든 분기(결산일: 항목).
ONEOFF_QUARTERS = {'2025-11-23': 'Uncle Toby’s 상표 손상 $53M(세전)',
                   '2026-05-31': '영업권 손상 $1.5B + 상표 손상 $250M(Nudges·True Chews) + 브라질 매각 예정 평가손실 $1.03B(세전)',
                   '2026-08-30': '브라질 추가 평가손실 $23.7M(세전)'}

# 미완성 카드 표시(2026-11-08 사용자 규칙, D·SRE 방식).
INCOMPLETE_SHORT = '손상·평가손실로 GAAP 적자'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익이 FY26 4분기 영업권·상표 손상($1.8B)과 브라질 평가손실($1.0B)로 적자다 — 배수 판정이 왜곡돼 보류한다. 판정 재개는 이르면 2027년 7월(FY27 4분기 실적) 뒤'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익이 FY26 4분기 영업권·상표 손상($1.8B)과 브라질 평가손실($1.0B)로 적자다 — 배수 판정이 왜곡돼 보류한다. 판정 재개는 이르면 2027년 7월(FY27 4분기 실적) 뒤'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 손상·평가손실로 GAAP 적자 · 판정 재개 이르면 2027년 7월</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 손상·평가손실로 GAAP 적자. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="gisFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">손상·평가손실로 GAAP 적자</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
# 손상·매각 이익이 섞인 GAAP 마진을 Bear·내러티브 근거로 쓰지 않는다(IP·SJM과 같은 처리)
_c2 = h[h.index('<strong style="color:var(--accent2);">②</strong>'):]; _c2 = _c2[:_c2.index('</div>')]
h = h.replace(_c2, '<strong style="color:var(--accent2);">②</strong> Q2 FY27 조정 영업이익률이 1년 전 17.4%보다 높은지(GAAP 15.0%는 상표 손상·구조조정 약 $0.1B 포함, Q2 FY27에는 브라질 매각 사후 정산이 들어온다)', 1)
_c1 = h[h.index('<strong style="color:var(--accent2);">①</strong>'):]; _c1 = _c1[:_c1.index('</div>')]
h = h.replace(_c1, '<strong style="color:var(--accent2);">①</strong> 유기 매출 증가율이 회사 FY27 전망(−1.5%~+0.5%) 안에 있는지 — 보고 매출은 53주 기저와 브라질 매각으로 약 4%p 더 낮게 나온다', 1)
h = h.replace('<span class="bb-text">북미 소매(시리얼·스낵·냉장) 매출 −6.6%(1년 전 같은 분기 대비).', '<span class="bb-text">북미 소매 유기 매출 −3%(보고 −6.6%는 요구르트 매각 4%p 포함).', 1)
h = h.replace('<span class="bb-text">부채비율(총부채 ÷ 자본) 306%, 자본 $7.5B.', '<span class="bb-text">차입금 $13.6B(현금 $0.4B), 이자보상배율 약 4.5배 — 부채비율 306%는 손상으로 자본이 줄어 커진 값이다.', 1)
h = h.replace('<div class="stat-sub">GAAP · 1년 전 $2.22 (−67%)</div>', '<div class="stat-sub">GAAP · 1년 전 $2.22(요구르트 매각 이익 포함) · 조정 $0.75(−13%)</div>', 1)
_bu = h[h.index('<div class="bb-title bb-bull">'):]; _bu = _bu[:_bu.index('</div>')+6]
h = h.replace(_bu, _bu + '\n      <div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">매출</span><span class="bb-text">Q1 FY27 유기 매출 보합(1년 전 −3%), FY27 비용 절감 $750M 이상 예상.</span></div>\n      <div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">배당</span><span class="bb-text">최근 4분기 FCF 약 $1.5B가 배당 약 $1.3B를 덮는다(127년 연속 지급).</span></div>', 1)
_b1 = '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">마진</span><span class="bb-text">최근 4분기 영업이익률 −1.1%(영업적자).</span></div>'
assert _b1 in h
h = h.replace(_b1, '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">이익</span><span class="bb-text">회사는 FY27 조정 영업이익 −8~−13%, 조정 EPS $3.00~3.20을 예상한다(FY26 $3.55).</span></div>', 1)
h = h.replace('영업이익률 14.4%(1년 전 38.2%).', '영업이익률 14.4%(1년 전 38.2%는 미국 요구르트 매각 이익 $1.05B 포함).', 1)
h = h.replace('Q2 FY27 실적 공시.', 'Q2 FY27 실적 공시 — 손상 분기(FY26 4분기)가 남아 판정은 계속 보류된다.', 1)
"""]

# ── 자동 카드 — 부문 지도(seg_map_propose 뒤 원문 대조). 원문: Q1 FY27 보도자료 2,451.8 + 794.3 + 612.8 + 523.1 = 4,382.0 ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"gis:NorthAmericaRetailSegmentMember": ["북미 소매(시리얼·스낵·냉장)", "#0b3d91"],
             "gis:InternationalSegmentMember": ["해외", "#f5b335"],
             "gis:NorthAmericaPetSegmentMember": ["북미 반려동물(Blue Buffalo)", "#6d8fc7"],
             "gis:NorthAmericaFoodserviceMember": ["북미 외식", "#d7dfee"]}
}
