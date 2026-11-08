CIK = '0000063754'
BUILD = {'no_dcf': '미완성 — 멕시코 합작사 재측정 이익이 최근 4분기 GAAP 이익을 크게 부풀린다', 'cover_shares': True}   # 2026-11-08 사용자 규칙(D군 — 일회성 30% 이상이면 미완성). 주식 수는 의결권·무의결권 두 종류라 표지 값 합산
# MKC(맥코믹) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 11월 30일. 소비자용 향신료·조미료(Consumer), 식품회사용 향미료(Flavor Solutions).
# 출처: SEC XBRL, Q3 FY26 10-Q(2026-10-01 16:36 동부 장 마감 뒤 → 첫 세션 10-02, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 06:3x~07:3x 동부 → 그날),
#        McCormick de Mexico 지배 지분 인수 완료(2026-01-02), Unilever Foods 결합 계약(2026-03-31 — 1분기 실적과 같은 날), 감사인 교체(2026-09-28).
# 엔진 입력(2026-11-08): 차입금 $5,018M(단기 1,340.2 + 1년 안 만기 771.9 + 장기 2,906.1), 현금 $331M, 비지배지분 $584M(McCormick de Mexico 25% — Grupo Herdez).
#   주식 수는 표지의 의결권·무의결권 합(cover_shares). 4분기 EPS FY20·FY24는 보도자료(Q4_EPS_OVERRIDE). 금융리스 $73.1M은 차입금 안에 있다(FL_IN_DEBT), 재고는 InventoryGross(Codex r1).
# 일회성(E54): 최근 4분기 GAAP 희석 EPS 5.53(0.84 + 3.77 + 0.56 + 0.36) 대 회사 조정 EPS 3.18(0.86 + 0.66 + 0.80 + 0.86).
#   Q1 FY26 McCormick de Mexico 기존 지분 재측정 이익 주당 3.22(비현금)에서 특별 비용(거래·통합 비용, 인수 재고 평가 상승분 등 — Q1 0.11·Q2 0.24·Q3 0.50·Q4 FY25 0.02)을 빼면
#   순 일회성 이익 주당 약 2.35 = GAAP의 약 42% → 미완성(일회성이 GAAP 이익을 부풀리는 쪽).
CUR, YO, QO = '2026-08-31', '2025-08-31', '2026-05-31'
QLABEL, YL, QQL = 'Q3 FY26', 'Q3 FY25', 'Q2 FY26'
L8 = ['Q4 FY24', 'Q1 FY25', 'Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26']
FY_ENDS, FY_LABEL = ('2025-11-30', '2024-11-30'), 'FY2025'
VOTES, VERDICT = (1, 1, 0), '판정 보류'
CO = 'McCormick'
S_ = 'https://www.sec.gov/Archives/edgar/data/63754/'
SEC = S_
TENQ = S_ + '000006375426000329/mkc-20260831.htm'; TENQ_NAME = 'Q3 FY26 10-Q'
PR = {'q3': S_ + '000006375426000326/mkcreportssolidthirdquar.htm', 'q2': S_ + '000006375426000270/mkcreportsstrongsecondqu.htm',
      'q1': S_ + '000006375426000189/mccormickreportsstrongfi.htm', 'q4': S_ + '000006375426000035/mccormickreportsstrong20.htm',
      'mexico': S_ + '000006375426000003/mcmexcompletesacquisitio.htm', 'ulv': S_ + '000199937126007382/mkcv_8k-033126.htm',
      'auditor': S_ + '000006375426000322/mkc-20260924.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="mkcFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(멕시코 합작사 재측정 이익이 최근 4분기 GAAP 이익을 크게 부풀린다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (0, 25)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 일회성 항목이 최근 4분기 GAAP 이익의 30% 이상이면 판정을 보류하고, 일회성 이익이 GAAP를 부풀리는 경우에도 같은 규칙을 적용한다. '
              '2026년 1월 멕시코 합작사(McCormick de Mexico) 지분을 50%에서 75%로 늘려(대금 $750M) 연결 자회사로 바꾸면서, 기존 50% 지분을 시가로 다시 평가한 비현금 이익이 1분기에 주당 약 $3.22 잡혔다. '
              '거래·통합 비용과 자산 손상 같은 특별 비용을 빼도 순 일회성 이익이 주당 약 $2.35로 최근 4분기 GAAP EPS($5.53)의 약 42%다 — 그래서 GAAP PER이 실제보다 훨씬 싸 보이고, 회사 조정 EPS($3.18)로 보면 PER은 두 배 가까이 높다. '
              '가장 큰 변화는 Unilever 식품 사업 결합이다. 2026년 3월 계약으로 Unilever가 식품 사업(인도·포르투갈 등 일부 제외)을 떼어 맥코믹과 합치고, 맥코믹은 Unilever에 약 $15.7B를 한 번에 지급한다. '
              '끝나면 기존 맥코믹 주주는 약 35%, Unilever 주주가 약 55%, Unilever가 약 10%를 갖는다(Unilever가 지분을 모두 나눠 주기로 하면 Unilever 주주 약 65%) — 주식 수가 약 3배로 늘어 사실상 회사가 바뀌는 거래다. 이사회는 맥코믹 8명·Unilever 지명 4명이 되고 유럽 증시 2차 상장도 추진한다. '
              '종결에는 맥코믹 주주 총회 승인(신주 발행·정관 변경)과 규제 승인이 필요하고, 이사회가 권고를 철회하면 $420M 해지 수수료, 주주가 부결하면 Unilever 비용 최대 $75M을 물어야 한다. 회사는 2027년 중반 종결을 목표로 한다. '
              '지급 대금은 최대 $15.7B 브리지론(그중 $2.0B는 3년 텀론으로 대체)과 앞으로 낼 채권으로 마련할 계획이라, 종결 뒤 차입금은 지금($5.0B)보다 크게 늘어난다 — 아래 약세 요인·체크포인트의 차입금은 종결 전 숫자다. '
              '회사는 결합 뒤 주당 이익이 늘어날 것(첫 12개월 한 자릿수 중후반, 3년째 10%대 중후반)과 연 약 $600M 비용 절감을 주장한다. 합병 뒤 독립성 문제로 감사인을 EY에서 KPMG로 바꾸고, 통합 책임자를 따로 임명했다. '
              '3분기에는 거래·통합 비용과 말레이시아 후추 조달 사업 중단에 따른 비현금 손상 등 특별 비용(주당 $0.50) 때문에 GAAP EPS가 $0.36에 그쳤다. 본업은 멕시코 합작사 연결 효과로 매출이 17% 늘었지만 유기적 성장은 2% 안팎이고, 2분기 이익에는 IEEPA 관세 환급($27.6M)도 들어 있다. '
              '지금까지 늘어난 차입금($4.0B → $5.0B)은 멕시코 합작사 대금과 운전자본을 기업어음으로 조달한 것이고 결합 자금은 아직 빌리지 않았다. 비지배지분($584M — 멕시코 합작사의 남은 25% 등을 포함한 연결 비지배지분)을 EV에 더한다. 주식은 의결권·무의결권 두 종류를 합해 센다. '
              '재측정 이익은 2027 회계연도 1분기 실적(2027년 3월 말) 뒤 최근 4분기에서 빠지지만, 그 무렵 Unilever 식품 사업 결합으로 회사 규모와 주식 수가 크게 바뀌므로 그때 처음부터 다시 본다.')
PH = ['GIS', 'HRL', 'SJM', 'KHC', 'MDLZ', 'HSY']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '포장식품 6곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(MKC 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·생활용품·유통이 섞여 있다. 차트에는 포장식품 6곳만 보인다.')
# 매출(Q3 FY26 보도자료): 소비자 1,215 + 향미료 솔루션 809 = 2,024.
SEG = [('소비자(향신료·조미료)', 1215.0, '#d52b1e'), ('향미료 솔루션(식품회사용)', 809.0, '#1f1f1f')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건(Q1은 Unilever 계약과 같은 날) + 멕시코 인수 완료 + 감사인 교체. 반응일: 실적 8-K 장 전 → 그날.
NEWS_RANGE = '2026.01 ~ 2026.10'
NEWS = [
    ('red', '2026년 10월 1일 장 전 — Q3 FY26 실적', '2026-10-01',
     '매출 +17.4%(유기 +1.9%, 멕시코 합작사 연결) · 희석 EPS $0.36(1년 전 $0.84 — 거래·통합 비용·손상) · 조정 EPS $0.86 · 연간 전망 유지 · Unilever 식품 결합 2027년 중반 종결 목표 — 그날 주가 −4.9%', 'q3', 'McCormick 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 9월 28일 장 마감 뒤 — 감사인 교체 결정(9월 24일 결정)', '2026-09-29',
     'Unilever 식품 결합 뒤 EY가 독립성 요건을 못 맞출 것으로 보여 FY26 10-K 제출 뒤 KPMG로 교체 — 회계 이견 없음(EY 확인) — 다음 날 주가 −0.1%', 'auditor', 'McCormick 공시 (SEC 8-K)'),
    ('green', '2026년 6월 25일 장 전 — Q2 FY26 실적', '2026-06-25',
     '매출 +16.7%(유기 +1.7%) · 희석 EPS $0.56 · 조정 EPS $0.80(+16%, IEEPA 관세 환급 $27.6M 포함) · 연간 전망 유지 — 그날 주가 +1.6%', 'q2', 'McCormick 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 3월 31일 장 전 — Q1 FY26 실적·Unilever 식품 사업 결합 계약', '2026-03-31',
     '희석 EPS $3.77(멕시코 합작사 재측정 이익 주당 $3.22 포함) · 조정 EPS $0.66 · 같은 날 오전 Unilever 식품 사업과 결합 발표(계약 8-K는 장 마감 뒤 접수) — 끝나면 기존 주주 약 35% 보유 — 그날 주가 −6.1%, 다음 날 −4.1%', 'ulv', 'McCormick·Unilever 공시 (SEC 8-K)'),
    ('red', '2026년 1월 22일 장 전 — 2025 회계연도 실적', '2026-01-22',
     '4분기 매출 +3% · 희석 EPS $0.84 · 조정 EPS $0.86 · 2025년 조정 EPS $3.00 · 2026년 전망 첫 제시(멕시코 연결을 합쳐도 조정 EPS 증가는 한 자릿수) — 그날 주가 −8.1%', 'q4', 'McCormick 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 2일 장 마감 뒤 — McCormick de Mexico 지분 75%로 확대', '2026-01-05',
     'Grupo Herdez에서 25% 추가 인수(대금 $750M, 보유 현금·기업어음) — 연결 자회사로 — 다음 거래일 주가 −2.4%', 'mexico', 'McCormick 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 15, 'nt': 9, 'mean': 52.89, 'median': 55, 'low': 47, 'high': 59, 'sb': 4, 'b': 3, 'h': 8, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'

# 파이프라인 자동 재판정용 — 일회성이 든 분기(결산일: 항목). Unilever 식품 결합 종결 뒤에는 처음부터 다시 본다(2026-11-08).
ONEOFF_QUARTERS = {'2025-11-30': '특별 비용 주당 0.02',
                   '2026-02-28': 'McCormick de Mexico 재측정 이익 주당 3.22 − 특별 비용 0.11',
                   '2026-05-31': '거래·통합 등 특별 비용 주당 0.24',
                   '2026-08-31': '거래·통합 등 특별 비용 주당 0.50'}

# 미완성 카드 표시(2026-11-08 사용자 규칙, D·SRE 방식).
INCOMPLETE_SHORT = '일회성 이익으로 이익 부풀림'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익에 멕시코 합작사 재측정 이익(비현금)이 커서 GAAP PER이 실제보다 싸 보인다 — 배수 판정이 왜곡돼 보류한다. 이 이익이 최근 4분기에서 빠지고 Unilever 식품 결합이 정리되면 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익에 멕시코 합작사 재측정 이익(비현금)이 커서 GAAP PER이 실제보다 싸 보인다 — 배수 판정이 왜곡돼 보류한다. 이 이익이 최근 4분기에서 빠지고 Unilever 식품 결합이 정리되면 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 일회성 이익으로 이익 부풀림</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 일회성 이익으로 이익 부풀림. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="mkcFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">일회성 이익으로 이익 부풀림</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]


# ── 자동 카드 — 부문 지도(seg_map_propose 뒤 원문 대조). 원문: Q3 FY26 보도자료 1,215 + 809 = 2,024 ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"mkc:ConsumerMember": ["소비자(향신료·조미료)", "#d52b1e"],
             "mkc:FlavorSolutionsMember": ["향미료 솔루션(식품회사용)", "#1f1f1f"]}
}
