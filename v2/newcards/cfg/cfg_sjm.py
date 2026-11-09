CIK = '0000091419'
BUILD = {'no_dcf': '미완성 — 3분기(2026년 1월) Sweet Baked Snacks 영업권·Hostess 상표 손상이 최근 4분기 GAAP 이익보다 크다'}   # 2026-11-08 사용자 규칙(일회성 30% 이상이면 미완성)
# SJM(J.M. 스머커) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 4월 말(FY27 = 2026-05~2027-04). 커피·냉동 샌드위치(Uncrustables)·땅콩버터·반려동물 간식·Hostess.
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-08-26 16:16 동부 장 마감 뒤 → 08-27, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 07:0x~08:2x 동부 → 그날),
#        경영진 개편(2026-02-10 08:59 동부 → 그날), Elliott 협의·이사 선임(2026-02-26 16:17 동부 → 02-27).
# 엔진 입력(2026-11-08): 차입금 $6,737.8M(단기 193.5 + 1년 안 150.0 + 장기 6,394.3), 현금 $43.2M, 이자비용은 순이자(InterestIncomeExpenseNonoperatingNet — fetch_financials).
#   4분기 EPS FY25는 보도자료(Q4_EPS_OVERRIDE — 역산 −6.86, 보도자료 −6.85).
# 일회성(E54): 최근 4분기 GAAP 희석 EPS 2.14(2.26 − 6.79 + 3.64 + 3.03) 대 회사 조정 EPS 10.49(2.10 + 2.38 + 2.77 + 3.24).
#   Q3 FY26(2026-01-31) Sweet Baked Snacks 영업권 손상 $507.5M + Hostess 상표 손상 $454.2M = $961.7M(세전) — 그것만으로 최근 4분기 GAAP 순이익(약 $229M)보다 크다 → 미완성.
#   GAAP가 조정보다 높은 분기(Q2·Q4 FY26)는 미실현 파생상품 이익이 GAAP에 들어간 탓, Q1 FY27 조정 EPS에는 관세 환급 $0.84가 들어 있다.
CUR, YO, QO = '2026-07-31', '2025-07-31', '2026-04-30'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_ENDS, FY_LABEL = ('2026-04-30', '2025-04-30'), 'FY2026'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'J.M. Smucker'
S_ = 'https://www.sec.gov/Archives/edgar/data/91419/'
SEC = S_
TENQ = S_ + '000009141926000080/sjm-20260731.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000009141926000079/sjm20260826exhibit991.htm', 'q4': S_ + '000009141926000047/sjm06092026exhibit991.htm',
      'q3': S_ + '000009141926000013/sjm20260226exhibit991.htm', 'q2': S_ + '000009141925000104/sjm20251125exhibit991.htm',
      'lead': S_ + '000009141926000007/sjm20260209exhibit991.htm', 'elliott': S_ + '000009141926000017/sjm20260224-exhibit991.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="sjmFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(3분기 영업권·상표 손상이 최근 4분기 GAAP 이익을 흔든다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-40, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 일회성이 최근 4분기 GAAP 이익의 30% 이상이면 판정을 보류하는데, SJM은 2026년 1월 분기(Q3 FY26)에 Sweet Baked Snacks(Hostess) 영업권 $508M과 Hostess 상표 $454M을 손상 처리해(비현금, 합계 $962M) 그 분기 희석 EPS가 −$6.79였다. '
              '그 결과 최근 4분기 GAAP 희석 EPS는 $2.14로, 회사 조정 EPS $10.49와 크게 다르다. Hostess 관련 손상은 이번이 세 번째다 — Q3 FY25 약 $1.0B, Q4 FY25 약 $0.98B, Q3 FY26 $0.96B, 합계 약 $2.9B. '
              '반대로 GAAP가 조정보다 높은 분기도 있다 — 2025년 10월 분기는 커피 원두 등 파생상품의 아직 배분하지 않은 누적 손익 변동(평가이익 $103M, 회사가 조정에서 빼는 항목) 때문이고, 2026년 4월 분기는 3분기 손상이 연간 세율을 뒤흔들어 세금 환입($60.5M, 세율 −18.5%)이 생긴 탓이다 — 둘 다 본업 개선이 아니다. 2026년 7월 분기에는 관세 환급(원가 약 $115M, 주당 $0.84)도 들어 있다 — 회사는 조정 EPS에 포함하지만 카드는 일회성으로 본다(세후 약 $90M, 최근 4분기 GAAP 이익의 약 39%). 손상 분기는 Q3 FY27 실적(2027년 2월 말 예상) 때 최근 4분기에서 빠지며, 그 분기에 새 손상이 없고 관세 환급 등 남은 일회성이 GAAP 이익의 30% 아래일 때 판정을 재개한다. '
              '본업은 커피 가격 인상이 이끈다 — Q1 FY27 매출 $2.22B(+5%), 조정 EPS $3.24(+71%, 관세 환급 $0.84 포함). 회사는 FY27 전망을 매출 −1~−2%, 조정 EPS $10.50~11.00, 잉여현금흐름 약 $1.1B로 올렸다(6월 첫 전망은 −3~−4%, $9.75~10.25) — 다만 상향 폭 $0.75 중 약 $0.60는 1분기 관세 환급의 순효과이고 환급은 거의 다 받아 되풀이되지 않는다(환급을 빼면 Q1 조정 EPS는 약 $2.40, +26%). 회사는 FY27 매출 감소 이유를 ‘가격 실현 하락’으로만 설명한다. '
              '2월 사장 겸 COO John Brase가 회사를 떠나고 COO 자리를 없앴으며, CFO Tucker Marshall이 냉동 샌드위치·스프레드·Sweet Baked Snacks·해외 사업까지 맡게 됐다. 같은 달 행동주의 펀드 Elliott와 협의해 새 이사 2명(NRG CFO Bruce Chung, David Singer)을 4월에 선임했다. '
              '현금은 $43M뿐이고 차입금이 $6.7B라 순차입이 크지만 미사용 리볼버 $2.0B(2030년 만기)가 있다. 2월에는 캔자스 Emporia 공장 화재로 FY26 매출 전망 중간값을 조금 낮췄다. 주가는 4월 저점 약 $90에서 11월 $130대로 올랐다. 다음 실적(Q2 FY27)은 11월 말 예정이다.')
PH = ['GIS', 'KHC', 'HSY', 'MKC', 'HRL']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '포장 식품 5곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(SJM 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·생활용품·유통이 섞여 있다. 차트에는 포장 식품 5곳만 보인다.')
# 매출(Q1 FY27 보도자료 부문): 커피 807.8 + 냉동 샌드위치·스프레드 499.3 + 반려동물 371.7 + Sweet Baked Snacks 236.5 + 외식 203.7 + 기타(해외 등) 100.3 = 2,219.3.
SEG = [('미국 커피(Folgers·Dunkin’·Café Bustelo)', 807.8, '#c8102e'), ('냉동 샌드위치·스프레드(Uncrustables·Jif)', 499.3, '#f2a900'),
       ('반려동물 간식·사료(Milk-Bone·Meow Mix)', 371.7, '#7a1f2b'), ('Sweet Baked Snacks(Hostess)', 236.5, '#e57f84'),
       ('외식(Away From Home)', 203.7, '#c9b38a'), ('기타(해외 등)', 100.3, '#e9d8da')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건 + 경영진 개편 + Elliott 협의. 반응일: 장 전 → 그날, 장 마감 뒤 → 다음 날. 색은 사건 성격, 수치는 그날 주가.
NEWS_RANGE = '2025.11 ~ 2026.08'
NEWS = [
    ('green', '2026년 8월 26일 장 전 — Q1 FY27 실적', '2026-08-26',
     '매출 $2.22B(+5%) · GAAP 희석 EPS $3.03 · 조정 EPS $3.24(+71% — 관세 환급 $0.84 제외 시 약 $2.40, +26%) · FY27 전망 상향(조정 EPS $10.50~11.00) — 그날 주가 +4.3%', 'q1', 'Smucker 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 6월 9일 장 전 — FY26 4분기 실적 · FY27 전망', '2026-06-09',
     '4분기 매출 $2.27B(+6%) · GAAP 희석 EPS $3.64 · 조정 EPS $2.77(+20%) · FY27 전망 매출 −3~−4%, 조정 EPS $9.75~10.25 — 그날 주가 +10.4%', 'q4', 'Smucker 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 26일 장 마감 뒤 — Elliott 협의, 새 이사 2명', '2026-02-27',
     '행동주의 펀드 Elliott와 협의해 NRG Energy CFO Bruce Chung·David Singer를 4월 15일 이사로 선임하기로 · 정보 공유 협약 — 다음 날 주가 0.0%', 'elliott', 'Smucker 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 26일 장 전 — Q3 FY26 실적', '2026-02-26',
     '매출 $2.3B(+7%) · GAAP 희석 EPS −$6.79(Sweet Baked Snacks 영업권·Hostess 상표 손상 $962M) · 조정 EPS $2.38(−9%) · 2월 Emporia 공장 화재로 매출 전망 중간값 소폭 하향 — 그날 주가 +8.8%', 'q3', 'Smucker 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 10일 장 전 — 경영진 개편', '2026-02-10',
     '사장 겸 COO John Brase 퇴임·COO 자리 폐지 · CFO Tucker Marshall이 냉동 샌드위치·스프레드·Sweet Baked Snacks·해외 사업과 영업까지 맡음 — 그날 주가 +1.8%', 'lead', 'Smucker 보도자료 (SEC 8-K)'),
    ('red', '2025년 11월 25일 장 전 — Q2 FY26 실적', '2025-11-25',
     '매출 $2.3B(+3%) · GAAP 희석 EPS $2.26 · 조정 EPS $2.10(−24%) · 연간 전망 범위 좁힘(중간값 유지) — 그날 주가 −3.7%', 'q2', 'Smucker 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 19, 'nt': 14, 'mean': 142.07, 'median': 149, 'low': 110, 'high': 160, 'sb': 7, 'b': 3, 'h': 9, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'

# 파이프라인 자동 재판정용 — 일회성이 든 분기(결산일: 항목).
ONEOFF_QUARTERS = {'2026-01-31': 'Sweet Baked Snacks 영업권 손상 $507.5M + Hostess 상표 손상 $454.2M = $961.7M(세전)',
                   '2026-07-31': '관세 환급 원가 효과 약 $115M + 이자수익 $4M(주당 0.84, 세후 약 $90M)'}

# 미완성 카드 표시(2026-11-08 사용자 규칙, D·SRE 방식).
INCOMPLETE_SHORT = '영업권·상표 손상으로 이익 왜곡'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익에 2026년 1월 분기 Hostess 관련 영업권·상표 손상($962M)이 들어 있어 회사 조정 이익과 크게 다르다 — 배수 판정이 왜곡돼 보류한다. 재검토는 이르면 2027년 2월 말(Q3 FY27 실적) — 그 분기에 새 손상이 없고 관세 환급 등 남은 일회성이 30% 아래일 때'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익에 2026년 1월 분기 Hostess 관련 영업권·상표 손상($962M)이 들어 있어 회사 조정 이익과 크게 다르다 — 배수 판정이 왜곡돼 보류한다. 재검토는 이르면 2027년 2월 말(Q3 FY27 실적) — 그 분기에 새 손상이 없고 관세 환급 등 남은 일회성이 30% 아래일 때'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 영업권·상표 손상으로 이익 왜곡 · 재검토 이르면 2027년 2월 말</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 영업권·상표 손상으로 이익 왜곡. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="sjmFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">영업권·상표 손상으로 이익 왜곡</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
# 파생상품 손익·손상이 섞인 GAAP 마진·영업이익을 Bear·체크포인트 근거로 쓰지 않는다(IP·VTRS와 같은 처리)
_c2 = h[h.index('<strong style="color:var(--accent2);">②</strong>'):]; _c2 = _c2[:_c2.index('</div>')]
assert 'GAAP 영업이익률' in _c2
h = h.replace(_c2, '<strong style="color:var(--accent2);">②</strong> Q2 FY27 회사 조정 EPS가 1년 전 같은 분기($2.10)보다 높은지 — GAAP 영업이익률은 커피 파생상품 손익과 손상이 섞여 분기마다 크게 흔들려 비교에 쓰지 않는다', 1)
h = _re0.sub(r'(<span class="bb-text">순차입금\(리스 포함\) \$[0-9.]+B), 최근 4분기 영업이익의 [0-9.]+배\.', r'\1 — Hostess 인수 자금이 남아 있고 현금은 $43M뿐이다(최근 4분기 영업이익은 손상이 섞여 배수로 쓰지 않는다).', h, count=1)
h = _re0.sub(r'(영업이익률 [0-9.−-]+%\(1년 전 [0-9.−-]+%)\)', r'\1, GAAP — 커피 파생상품 손익·관세 환급이 섞임)', h, count=1)
h = h.replace('Q2 FY27 실적 공시.', 'Q2 FY27 실적 공시 — 손상 분기(Q3 FY26)가 남아 판정은 계속 보류된다.', 1)
_c1 = h[h.index('<strong style="color:var(--accent2);">①</strong>'):]; _c1 = _c1[:_c1.index('</div>')]
assert '매출 증가율' in _c1
h = h.replace(_c1, '<strong style="color:var(--accent2);">①</strong> Q2 FY27 매출이 1년 전($2.33B)보다 얼마나 줄었는지 — 회사는 FY27 매출 −1~−2%(가격 실현 하락)를 안내해 Q1 +5% 뒤 남은 세 분기는 평균 약 −3.5%가 예정돼 있다. 감소 폭이 이 안에 머무는지 본다', 1)
h = _re0.sub(r'(<span class="bb-text">최근 4분기 FCF \$[0-9.]+B, 매출의 [0-9.]+%)\.', r'\1 — 다만 관세 환급 현금 약 $0.12B이 들어 있고 회사 FY27 전망은 $1.1B이다.', h, count=1)
h = _re0.sub(r'(<span class="bb-text">Sweet Baked Snacks\(Hostess\) 매출 −[0-9.]+%\(1년 전 같은 분기 대비\))\.', r'\1 — Hostess 관련 손상이 다섯 분기 동안 세 번(합계 약 $2.9B) 나왔다.', h, count=1)
_bb = h[h.index('<span class="zone-label">자사주 매입'):]; _bb = _bb[:_bb.index('</div>', _bb.index('zone-val'))]
_v = _bb[_bb.index('<span class="zone-val">'):]; _v = _v[:_v.index('</span>')+7]
h = h.replace(_bb, _bb.replace(_v, '<span class="zone-val" style="font-size:13px;">공개 매입 없음 · 주식보상 회수 $6M</span>'), 1)
"""]

# ── 자동 카드 — 부문 지도(seg_map_propose 뒤 원문 대조). 원문: Q1 FY27 보도자료 807.8 + 499.3 + 371.7 + 236.5 + 203.7 + 100.3 = 2,219.3 ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"sjm:U.S.RetailCoffeeMember": ["미국 커피(Folgers·Dunkin’·Café Bustelo)", "#c8102e"],
             "sjm:U.S.RetailFrozenHandheldAndSpreadsMember": ["냉동 샌드위치·스프레드(Uncrustables·Jif)", "#f2a900"],
             "sjm:U.S.RetailPetFoodsMember": ["반려동물 간식·사료(Milk-Bone·Meow Mix)", "#7a1f2b"],
             "sjm:SweetBakedSnacksMember": ["Sweet Baked Snacks(Hostess)", "#e57f84"],
             "sjm:AwayFromHomeMember": ["외식(Away From Home)", "#c9b38a"],
             "us-gaap:AllOtherSegmentsMember": ["기타(해외 등)", "#e9d8da"]}
}
