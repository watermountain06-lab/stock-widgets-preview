CIK = '0001071739'
BUILD = {'no_dcf': '미완성 — Magellan 손상·구조조정 퇴직금 등 일회성이 최근 4분기 GAAP 이익의 약 46%'}   # 2026-11-08 사용자 규칙(일회성 30% 이상이면 미완성) — ZBH·EL과 같은 처리
# CNC(센틴) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 말. 미국 최대 메디케이드 관리형 의료·ACA 마켓플레이스·메디케어(어드밴티지·처방약 PDP) 보험사.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-26 19:03 동부 장 마감 뒤 → 10-27, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — SEC 접수는 전날 저녁이지만 회사 발표는 그날 오전 6시 동부 장 전 → 그날, Codex r1),
#        CFO 교체(2026-08-17 06:05 동부 장 전 → 그날).
# 일회성(E54): 최근 4분기 GAAP 희석 EPS 2.92(−2.24 + 3.11 + 2.19 − 0.14) 대 회사 조정 EPS 5.27(−1.19 + 3.37 + 2.51 + 0.58).
#   차이 가운데 인수 무형자산 상각(세후 주당 약 0.25 × 4)은 반복 비용. 일회성(세후 주당, 회사 조정표 "Other adjustments"):
#   Q4 2025 0.79(Magellan 매각 예정 손상 $513M·세후 $389M; 계약 정리 비용 0.02와 Magellan Rx 매각 이익 조정 −0.02 상쇄), Q1 2026 약 0.01, Q2 2026 0.07(효율화 비용·퇴직금),
#   Q3 2026 0.48(퇴직금 0.42·효율화 0.06·과거 매각 추가 손실 0.03·부동산 이익 −0.03) → 합계 약 1.35(GAAP의 약 46%) → 미완성(2026-11-09).
# 현금 $20.7B은 대부분 규제 자회사 몫 — 비규제 현금·투자는 $1.4B(그중 일반 용도 현금 $175M, Q3 10-Q).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, 0), '판정 보류'
CO = 'Centene'
S_ = 'https://www.sec.gov/Archives/edgar/data/1071739/'
SEC = S_
TENQ = S_ + '000107173926000192/cnc-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000107173926000194/a20261027ex991pressrelease.htm', 'q2': S_ + '000107173926000154/a20260728ex991pressrelease.htm',
      'q1': S_ + '000107173926000099/a20260428ex991pressrelease.htm', 'q4': S_ + '000107173926000031/a20260206ex991pressrelease.htm',
      'q3p': S_ + '000107173925000185/a20251029ex991pressrelease.htm', 'cfo': S_ + '000107173926000165/a20260817formex991pressrel.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="cncFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(Magellan 손상·구조조정 퇴직금 등 일회성이 최근 4분기 GAAP 이익을 흔든다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-30, 10)
ACT_REASON = '보험사라 재고가 없고 받을 보험료·내줄 의료비가 대부분이라 재고·매출채권 회전으로 보는 활동성이 잘 맞지 않는다'
NONOP_WHAT = '장기투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 일회성 항목이 최근 4분기 GAAP 이익의 30% 이상이면 판정을 보류하는데, CNC는 최근 4분기 GAAP 희석 EPS가 $2.92, 회사 조정 EPS가 $5.27이다. '
              '차이 가운데 인수 무형자산 상각(세후 주당 약 $1.0)은 매 분기 반복되는 비용이라 카드는 일회성으로 보지 않는다. 나머지 일회성은 세후 주당 약 $1.35(GAAP의 약 46%)다 — '
              '2025년 12월 남은 Magellan Health 사업을 팔기로 하면서 4분기에 $513M(세후 $389M)을 손상 처리했고, 2026년 3분기에는 조직 효율화 퇴직금(세후 주당 $0.42)이 잡혔다. '
              '2분기에는 메디케어·커머셜의 비반복 이익(주당 약 $0.50, 회사 조정 EPS에도 포함)도 있어 비용과 순액으로 보면 약 29%지만, 비용만으로 30%를 넘으면 미완성으로 두는 카드 규칙(GNRC와 같은 처리)에 따라 보류한다. 가장 큰 Magellan 손상은 2026년 4분기 실적(2027년 2월 예상) 때 최근 4분기에서 빠지고, 회사 2026년 전망의 일회성(세후 주당 약 $0.75)은 GAAP 전망(>$3.46)의 약 22%라 그때 실제 숫자로 다시 판정한다. '
              '2025년은 위기였다 — 7월 마켓플레이스(ACA) 위험 조정 수입이 예상보다 크게 줄어 전망을 거둬들였고, 3분기 영업권 $6.7B 손상으로 연간 GAAP 주당 손실 $(13.53)을 냈다. '
              '2026년엔 빠르게 회복 중이다 — 회사는 2월 처음 제시한 조정 EPS 전망(>$3.00)을 4월 >$3.40, 7월 >$4.80(메디케어·커머셜 비반복 이익 약 $0.50 포함), 10월 >$5.20으로 세 차례 올렸다. '
              '다만 강화된 ACA 보험료 보조금이 2025년 말 끝나 마켓플레이스 가입자가 1년 새 583만 명에서 340만 명으로 줄었고, 메디케이드 가입자도 1,271만 명에서 1,190만 명으로 줄었다. 3분기 의료비율(HBR)은 92.7%였다. 메디케이드 감소 일부는 이중 수급자가 메디케어로 재분류된 몫이고, 메디케어 가입자 증가는 처방약(PDP) 가입자(797만 → 895만)가 이끌었다. 앞으로의 부담도 있다 — 10월 발표된 2027년 메디케어 어드밴티지 별점에서 3.5성 이상 플랜 가입자 비율이 60%에서 42%로 떨어져 2028년 메디케어 수입에 불리하고, 2027년부터 메디케이드 근로 요건(OBBBA)이 가입자를 더 줄일 수 있으며, 조지아·텍사스 메디케이드 재입찰 결과에 이의를 제기하고 있다. 2025년 7월 전망 철회와 관련한 증권 집단소송도 진행 중이다. '
              '현금 $20.7B은 대부분 주 정부 규제를 받는 보험 자회사 몫이라 회사가 마음대로 쓸 수 있는 돈은 일부(비규제 현금·투자 $1.4B)다. 3분기 말 총차입은 $15.5B이고, 10월 2027년 만기 채권 남은 $569M까지 갚아 6월 말 이후 $1.1B를 줄였다. 카드의 EV/EBITDA 등 배수는 규제 현금까지 현금으로 빼서 계산해 실제보다 싸 보일 수 있다. '
              'CFO Drew Asher가 2026년 12월 물러나고 2027년 1월 Chris Neczypor가 맡는다. 주가는 2026년 3월 약 $32에서 11월 4일 $76까지 올랐다가 이틀 새 약 8% 내렸다.')
PH = ['UNH', 'ELV', 'CI', 'HUM', 'CVS']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '건강보험 5곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(CNC 제외)와 배수 순위를 매긴 값이다.',
            '제약·의료기기·보험이 섞여 있다. 차트에는 건강보험 5곳만 보인다.')
# 매출(Q3 2026 10-Q 부문, 총매출 기준 — 주 정부 보험료세 포함): 메디케이드 29,581 + 메디케어 11,263 + 커머셜 8,700 + 기타 1,103 = 50,647.
SEG = [('메디케이드', 29581.0, '#1f3a68'), ('메디케어(어드밴티지·처방약)', 11263.0, '#6cc04a'), ('커머셜(ACA 마켓플레이스 등)', 8700.0, '#4f8fc0'), ('기타', 1103.0, '#b8c2cc')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 5건 + CFO 교체. 반응일: 모두 장 전 발표 → 그날(실적은 회사 발표 시각 기준). 색은 사건 성격, 수치는 그날 주가.
NEWS_RANGE = '2025.10 ~ 2026.10'
NEWS = [
    ('green', '2026년 10월 27일 장 전 — Q3 2026 실적', '2026-10-27',
     '총매출 $50.6B · GAAP 희석 EPS $(0.14)(퇴직금 등) · 조정 EPS $0.58 · 연간 조정 EPS 전망 >$5.20으로 상향 · 6월 말 이후 차입금 $1.1B 감축 — 그날 주가 +1.0%', 'q3', 'Centene 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 17일 장 전 — CFO 교체 발표', '2026-08-17',
     'CFO Drew Asher 12월 퇴임(2027년 말 은퇴) · Chris Neczypor가 2027년 1월 CFO — 그날 주가 −4.5%(원인은 공시로 확인 못 함)', 'cfo', 'Centene 보도자료 (SEC 8-K)'),
    ('green', '2026년 7월 28일 장 전 — Q2 2026 실적', '2026-07-28',
     'GAAP 희석 EPS $2.19 · 조정 EPS $2.51 · 커머셜 의료비율 79.2% · 연간 조정 EPS 전망 >$4.80으로 상향(일회성 이익 약 $0.50 포함) — 그날 주가 −0.3%', 'q2', 'Centene 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 4월 28일 장 전 — Q1 2026 실적', '2026-04-28',
     'GAAP 희석 EPS $3.11 · 조정 EPS $3.37(예상보다 약 $0.50 높음) · 연간 조정 EPS 전망 >$3.40으로 상향 · 차입금 $1.0B 감축(Part D 정산 채권 $1.0B 매각 대금으로) — 그날 주가 +14.0%', 'q1', 'Centene 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 6일 장 전 — 2025년 연간 실적 · 2026년 전망', '2026-02-06',
     '4분기 GAAP 희석 EPS $(2.24)(Magellan 손상 $513M) · 조정 EPS $(1.19) · 연간 GAAP $(13.53)·조정 $2.08 · 2026년 조정 EPS >$3.00 제시 — 그날 주가 −3.7%', 'q4', 'Centene 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 10월 29일 장 전 — Q3 2025 실적', '2025-10-29',
     'GAAP 희석 EPS $(13.50)(영업권 손상 $6.7B) · 조정 EPS $0.50 · 연간 조정 EPS 전망 $0.25 올려 최소 $2.00 — 그날 주가 +12.5%', 'q3p', 'Centene 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 21, 'nt': 14, 'mean': 75.86, 'median': 78, 'low': 65, 'high': 82, 'sb': 7, 'b': 1, 'h': 12, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-09'

# 파이프라인 자동 재판정용 — 일회성이 든 분기(결산일: 항목, 세후 주당). 상각은 반복으로 빼지 않는다.
ONEOFF_QUARTERS = {'2025-12-31': 'Magellan 매각 예정 손상 0.79 · 계약 정리 비용 0.02 · Magellan Rx 매각 이익 조정 −0.02',
                   '2026-03-31': '효율화 비용 0.02 · 채무 조기 상환 손실 0.01 · 네트워크·부동산 매각 이익 −0.02',
                   '2026-06-30': '효율화 비용 0.06 · 퇴직금 0.02 · 채무 상환 이익 −0.01',
                   '2026-09-30': '퇴직금 0.42 · 효율화 0.06 · 과거 매각 추가 손실 0.03 · 부동산 이익 −0.03'}

# 미완성 카드 표시(2026-11-08 사용자 규칙, D·SRE 방식).
INCOMPLETE_SHORT = '일회성 비용이 이익의 절반 가까이'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익에 Magellan 손상·구조조정 퇴직금 등 일회성(세후 주당 약 $1.35, GAAP의 약 46%)이 들어 있다 — 배수 판정이 왜곡돼 보류한다. 재검토는 이르면 2027년 2월(2026년 4분기 실적) — Magellan 손상이 빠질 때'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익에 Magellan 손상·구조조정 퇴직금 등 일회성(세후 주당 약 $1.35, GAAP의 약 46%)이 들어 있다 — 배수 판정이 왜곡돼 보류한다. 재검토는 이르면 2027년 2월(2026년 4분기 실적) — Magellan 손상이 빠질 때'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 일회성 비용이 이익의 절반 가까이 · 재검토 이르면 2027년 2월</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 일회성 비용이 이익의 절반 가까이. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="cncFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">일회성 비용이 이익의 절반 가까이</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
# 손상이 섞인 GAAP 마진, 규제 자회사 현금, 지급 시기로 출렁이는 분기 FCF를 판단 근거로 쓰지 않는다(ZBH·EL과 같은 처리)
_c2 = h[h.index('<strong style="color:var(--accent2);">②</strong>'):]; _c2 = _c2[:_c2.index('</div>')]
h = h.replace(_c2, '<strong style="color:var(--accent2);">②</strong> 2026년 연간 의료비율(HBR)이 회사 전망(90.4~91.1%) 안에서 끝나는지, 2027년 전망에서 마켓플레이스 가입자 감소를 얼마로 보는지 — Q4 2025 GAAP 영업이익률엔 Magellan 손상이 섞여 비교 기준으로 쓰지 않는다', 1)
h = _re0.sub(r'<span class="bb-head">부채</span><span class="bb-text">현금·단기투자가 차입금·리스보다 \$[0-9.]+B 많다\(순현금\)\.</span>', '<span class="bb-head">부채</span><span class="bb-text">6월 말 이후 차입금을 $1.1B 줄여 2027년 만기 채권을 모두 갚았고, $4.0B 회전 신용은 쓰지 않고 있다(3분기 말 총차입 $15.5B). 장부상 현금의 대부분은 규제 자회사 몫이다(비규제 현금·투자 $1.4B).</span>', h, count=1)
h = _re0.sub(r'<span class="bb-head">투자</span><span class="bb-text">Q3 2026 FCF[^<]*</span>', '<span class="bb-head">메디케어</span><span class="bb-text">2027년 별점에서 3.5성 이상 플랜 가입자 비율이 60%에서 42%로 떨어져 2028년 메디케어 수입에 불리하다. 3분기 FCF −$3.9B는 주 정부 지급금 전달 시기 탓(회사 예상)이라 근거로 쓰지 않는다.</span>', h, count=1)
h = h.replace('GAAP · 1년 전 −$13.50 (적자 지속)', 'GAAP · 1년 전 −$13.50 · 둘 다 일회성 포함(영업권 손상·퇴직금) — 조정 EPS $0.58(1년 전 $0.50)', 1)
h = _re0.sub(r'(지배적 내러티브 · [^<]*?영업이익률 −?[0-9.]+%\(1년 전 −?[0-9.]+%)\)', r'\1 · 둘 다 일회성 포함: 2025 영업권 손상 $6.7B, 2026 퇴직금)', h, count=1)
h = h.replace("$('fundNetCashNote').textContent = `순현금 ${B(N.net)}`", "$('fundNetCashNote').textContent = `순현금(대부분 규제 자회사 현금 — 비규제 현금·투자 $1.4B) ${B(N.net)}`", 1)
h = h.replace('<span class="diag-note" id="fundNetCashNote">순현금 ', '<span class="diag-note" id="fundNetCashNote">순현금(대부분 규제 자회사 현금 — 비규제 현금·투자 $1.4B) ', 1)
_c1 = h[h.index('<strong style="color:var(--accent2);">①</strong>'):]; _c1 = _c1[:_c1.index('</div>')]
h = h.replace(_c1, '<strong style="color:var(--accent2);">①</strong> 4분기는 해마다 적자가 나는 분기(마켓플레이스·처방약 계절성)라, 분기 숫자보다 2026년 연간 조정 EPS가 전망(>$5.20)을 지키는지 본다 — 총매출은 주 보험료세 전달분이 섞여 보험료·서비스 매출(3분기 +0.5%)로 성장을 본다', 1)
"""]

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"cnc:MedicaidSegmentMember": ["메디케이드", "#1f3a68"], "cnc:MedicareSegmentMember": ["메디케어(어드밴티지·처방약)", "#6cc04a"], "cnc:CommercialSegmentMember": ["커머셜(ACA 마켓플레이스 등)", "#4f8fc0"], "us-gaap:AllOtherSegmentsMember": ["기타", "#b8c2cc"]}
}
