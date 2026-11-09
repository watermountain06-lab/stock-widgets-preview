CIK = '0001637459'
BUILD = {'no_dcf': '미완성 — 2분기 영업권·상표 손상($7.4B)으로 최근 4분기 GAAP가 적자'}   # 2026-11-08 사용자 규칙(일회성이 GAAP를 적자로 만들면 미완성)
# KHC(크래프트 하인즈) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 마지막 토요일. 케첩·소스·치즈·가공육·도시락(Heinz·Kraft·Oscar Mayer·Lunchables).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-04 16:33 동부 장 마감 뒤 → 11-05, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 06:0x~07:0x 동부 → 그날),
#        새 CEO 선임(2025-12-16 07:01 동부 → 그날), NYSE 이전(2026-08-26 발표, 09-14 상장), 부문 재편 재작성(2026-10-07).
# 엔진 입력(2026-11-08): 차입금 $18,003M(1년 안 918 + 장기 17,085, 금융리스 포함 — DEBT_TOTAL_TAG, 기본은 1년 안 몫이 빠졌다), 현금 $1,888M,
#   비지배지분 $102M + 상환 가능 $13M(EV_TAGS_BY_CIK). 4분기 EPS 2025는 보도자료(Q4_EPS_OVERRIDE — 역산 0.56, 보도자료 0.55).
# 일회성(E54): 최근 4분기 GAAP 희석 EPS −2.92(0.55 + 0.67 − 4.60 + 0.46) 대 회사 조정 EPS 2.34(0.67 + 0.58 + 0.56 + 0.53).
#   Q2 2026 영업권 손상 $2,441M + 상표 손상 $4,902M(Kraft $3.4B·Oscar Mayer $660M·Lunchables $445M 등) = 약 $7.4B, Q3 2026 영업권 손상 $69M(인도네시아) → GAAP를 적자로 만든다.
#   Q1 2026에는 원자재 헤지 미실현 이익 $178M, Q2 2026에는 회사채 조기 매입 이익 $265M이 GAAP에 들어 있다.
CUR, YO, QO = '2026-09-26', '2025-09-27', '2026-06-27'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-27', '2024-12-28'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Kraft Heinz'
S_ = 'https://www.sec.gov/Archives/edgar/data/1637459/'
SEC = S_
TENQ = S_ + '000163745926000081/khc-20260926.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000163745926000078/ex991-erq32026.htm', 'q2': S_ + '000163745926000052/ex991-erq22026.htm',
      'q1': S_ + '000163745926000020/ex991-erq12026.htm', 'q4': S_ + '000163745926000006/ex991-erq42025.htm',
      'ceo': S_ + '000119312525319938/d95367d8k.htm', 'nyse': S_ + '000163745926000057/ex991-nysepressrelease82526.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="khcFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 GAAP가 손상으로 적자)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-140, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 일회성이 최근 4분기 GAAP 이익을 적자로 만들면 판정을 보류하는데, KHC는 2026년 2분기에 영업권 $2.44B와 상표 $4.90B(Kraft $3.4B·Oscar Mayer $660M·Lunchables $445M 등)를 손상 처리해(비현금, 합계 약 $7.4B) 최근 4분기 GAAP 희석 EPS가 −$2.92다(회사 조정 EPS는 $2.34). '
              '2025년에도 손상이 $9.3B 있었고, 3분기에는 인도네시아 사업 영업권 $69M을 또 손상 처리했다. 손상 분기는 2027년 2분기 실적(8월 예상) 때 최근 4분기에서 빠지며, 그때 새 손상이 없는지와 남은 일회성(3분기 $69M 등)을 포함한 최근 4분기 GAAP가 흑자인지 확인해 다시 판정한다. '
              '반대 방향 일회성도 있다 — 원자재 헤지 미실현 손익이 1분기 +$178M, 2분기 −$101M, 3분기 +$39M(9개월 순 +$116M)이고, 2분기에는 2046년 만기 채권 액면 $1.4B를 약 $1.1B에 공개 매수해 생긴 이익 $265M(관련 헤지 손실을 빼면 세전 $228M)이 들어 있다. '
              '본업은 줄고 있다 — 3분기 매출 $6.1B(−2.0%, 유기 −1.1%), 조정 영업이익 −15%. 북미는 −3.4%, 신흥국은 +13.8%다. 회사는 2026년 유기 매출 −0.5~−1.25%, 조정 영업이익 −16~−18%(고정환율), 조정 EPS $2.07~2.13을 예상한다. '
              '2026년 1월 Kellanova 출신 Steve Cahillane이 CEO가 됐고, 2월에는 2025년에 발표한 두 회사 분리 작업을 보류하고(철회는 아니며 3분기에도 관련 비용 $24M) 마케팅·영업·연구개발과 가격에 $600M을 더 쓰기로 했다. 1월에는 최대주주 Berkshire Hathaway가 보유 3.25억 주(약 27%)를 팔 수 있도록 재매각 등록을 했다(매각 여부·시점은 미정). 3분기에 부문을 북미·유럽·태평양 선진국·신흥국 셋으로 바꾸고 10월 7일 과거 수치를 새 부문으로 재작성해 공시했다. '
              '1년 사이 북미 사장, 판매 책임자, 법무 책임자가 물러났고 11월 새 이사 2명을 선임했다. 6~7월 만기 채권과 2027년물도 갚아 차입금은 연초 약 $21B에서 $18.0B로 줄었고, 9월 14일 상장을 나스닥에서 NYSE로 옮겼다. 참고 점수의 EV/EBITDA는 손상으로 최근 4분기 EBITDA가 적자라 0점으로 들어가 자기 이력·동종업 점수를 끌어내린다. '
              '최근 4분기 GAAP가 적자라 PER 숫자는 나오지 않으며, 평가와 평균에서 뺀다.')
PH = ['GIS', 'SJM', 'HSY', 'MKC', 'HRL']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '포장 식품 5곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(KHC 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·생활용품·유통이 섞여 있다. 차트에는 포장 식품 5곳만 보인다.')
# 매출(Q3 2026 보도자료 부문, 10월 재편 뒤): 북미 4,485 + 유럽·태평양 선진국 910 + 신흥국 720 = 6,115.
SEG = [('북미', 4485.0, '#ce1126'), ('유럽·태평양 선진국', 910.0, '#0a2a66'), ('신흥국', 720.0, '#e7a1a8')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건 + 새 CEO + NYSE 이전. 반응일: 장 전 → 그날. 색은 사건 성격, 수치는 그날 주가.
NEWS_RANGE = '2025.12 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 11월 4일 장 전 — Q3 2026 실적', '2026-11-04',
     '매출 $6.1B(−2.0%, 유기 −1.1%) · GAAP 희석 EPS $0.46 · 조정 EPS $0.53(−13%) · 유기 매출 전망 하단 상향, 조정 EPS 전망 $2.07~2.13 · 새 이사 2명 — 그날 주가 +3.8%', 'q3', 'Kraft Heinz 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 26일 장 전 — NYSE 이전 발표', '2026-08-26',
     '상장을 나스닥에서 NYSE로 옮겨 9월 14일부터 같은 티커 KHC로 거래', 'nyse', 'Kraft Heinz 보도자료 (SEC 8-K)'),
    ('red', '2026년 8월 5일 장 전 — Q2 2026 실적', '2026-08-05',
     '매출 −1.4%(유기 −1.3%) · GAAP 희석 EPS −$4.60(영업권·상표 손상 약 $7.4B) · 조정 EPS $0.56(−19%) — 그날 주가 −3.4%', 'q2', 'Kraft Heinz 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 6일 장 전 — Q1 2026 실적', '2026-05-06',
     '매출 $6.0B(+0.8%, 유기 −0.4%) · GAAP 희석 EPS $0.67 · 조정 EPS $0.58(−6.5%) · 연간 전망 유지 — 그날 주가 +2.4%', 'q1', 'Kraft Heinz 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 11일 장 전 — 2025년 연간 실적 · 분리 작업 보류', '2026-02-11',
     '2025년 손상 $9.3B · 4분기 GAAP 희석 EPS $0.55 · 조정 EPS $0.67(−20%) · 두 회사 분리 작업 보류 · 성장 회복에 $600M 추가 투자 — 그날 주가 +0.4%', 'q4', 'Kraft Heinz 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2025년 12월 16일 장 전 — 새 CEO 선임', '2025-12-16',
     'Kellanova CEO 출신 Steve Cahillane을 2026년 1월 1일부터 CEO로 — 그날 주가 +0.7%', 'ceo', 'Kraft Heinz 공시 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 19, 'nt': 14, 'mean': 24.64, 'median': 25, 'low': 21, 'high': 32, 'sb': 1, 'b': 1, 'h': 13, 's': 4, 'ss': 0}
ANALYST_ASOF = '2026-11-09'

# 파이프라인 자동 재판정용 — 일회성이 든 분기(결산일: 항목).
ONEOFF_QUARTERS = {'2026-03-28': '원자재 헤지 미실현 이익 $178M(세전)',
                   '2026-06-27': '영업권 손상 $2,441M + 상표 손상 $4,902M = 약 $7.4B(세전) · 회사채 조기 매입 이익 $265M',
                   '2026-09-26': '인도네시아 영업권 손상 $69M(세전)'}

# 미완성 카드 표시(2026-11-08 사용자 규칙, D·SRE 방식).
INCOMPLETE_SHORT = '영업권·상표 손상으로 GAAP 적자'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익이 2026년 2분기 영업권·상표 손상(약 $7.4B)으로 적자다 — 배수 판정이 왜곡돼 보류한다. 판정 재개는 이르면 2027년 8월(2027년 2분기 실적) 뒤, 새 손상이 없을 때'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익이 2026년 2분기 영업권·상표 손상(약 $7.4B)으로 적자다 — 배수 판정이 왜곡돼 보류한다. 판정 재개는 이르면 2027년 8월(2027년 2분기 실적) 뒤, 새 손상이 없을 때'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 영업권·상표 손상으로 GAAP 적자 · 판정 재개 이르면 2027년 8월</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 영업권·상표 손상으로 GAAP 적자. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="khcFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">영업권·상표 손상으로 GAAP 적자</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
# 손상이 섞인 GAAP 마진을 Bear 근거로 쓰지 않는다(IP·GIS와 같은 처리)
_b1 = '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">마진</span><span class="bb-text">최근 4분기 영업이익률 −13.4%(영업적자).</span></div>'
assert _b1 in h
h = h.replace(_b1, '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">이익</span><span class="bb-text">회사 조정 영업이익이 3분기 −15%, 2026년 전망 −16~−18%(고정환율) — 손상을 빼도 이익이 줄고 있다.</span></div>', 1)
_c2 = h[h.index('<strong style="color:var(--accent2);">②</strong>'):]; _c2 = _c2[:_c2.index('</div>')]
assert 'GAAP 영업이익률' in _c2
h = h.replace(_c2, '<strong style="color:var(--accent2);">②</strong> Q4 2026 조정 영업이익 감소율이 회사 연간 전망(−16~−18%, 고정환율) 안에 머무는지(Q3 2026 −15.2%) — GAAP 영업이익률은 손상·헤지 평가손익이 섞여 비교에 쓰지 않는다', 1)
_bb = '<span class="zone-label">자사주 매입 (회계연도 누계 2025.12.28~2026.9.26, 39주)</span>\n          <div style="display:flex;align-items:center;gap:8px;">\n            <span class="zone-val">$79M</span>'
assert _bb in h
h = h.replace(_bb, _bb.replace('<span class="zone-val">$79M</span>', '<span class="zone-val" style="font-size:13px;">공개 매입 없음 · 주식보상 세금분 $79M</span>'), 1)
h = h.replace('Q4 2026 실적 공시.', 'Q4 2026 실적 공시 — 손상 분기(2026년 2분기)가 남아 판정은 계속 보류된다.', 1)
"""]

# ── 자동 카드 — 부문 지도(seg_map_propose 뒤 원문 대조). 원문: Q3 2026 보도자료 4,485 + 910 + 720 = 6,115 ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"khc:NorthAmericaSegmentMember": ["북미", "#ce1126"],
             "khc:EuropeAndPacificDevelopedMarketsSegmentMember": ["유럽·태평양 선진국", "#0a2a66"],
             "khc:EmergingMarketsSegmentMember": ["신흥국", "#e7a1a8"]}
}
