CIK = '0001285785'
BUILD = {'no_dcf': '미완성 — 일회성 손실로 최근 4분기 GAAP 이익 적자'}   # 2026-11-07 사용자 규칙(D군 — 일회성이 GAAP 이익을 음수로 만들면 미완성 카드)
# MOS(모자이크) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 인산 비료(미국 플로리다·루이지애나), 칼륨(캐나다 서스캐처원), 브라질 유통·생산(Mosaic Fertilizantes).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-04 14:31 동부 장중 → 그날, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — Q4·Q2·Q3 장 마감 뒤 16:2x~16:3x 동부 → 다음 날, Q1 10:44 동부 장중 → 그날),
#        Araxá·Patrocínio 가동 중단(8-K 2.06, 2026-04-08 11:05 동부 → 그날), 채권 공개매수·신규 채권(08-10 08:50 동부, 08-17 16:18 동부 → 08-18).
# 엔진 입력(2026-11-07): 차입금 $5,913.1M = 단기 511.6 + 1년 안 만기 68.7 + 장기 5,332.8(DEBT_TOTAL_TAG), 현금 $272.6M.
#   4분기 EPS는 보도자료 GAAP 희석 EPS(Q4_EPS_OVERRIDE 2019~2023·2025 — 발표 당시 값, Codex r1).
# 일회성(E54 규칙): 최근 4분기 GAAP 희석 EPS −3.54(Q4 2025 −1.64, Q1 −0.81, Q2 −0.86, Q3 −0.23) 대 회사 조정 EPS 0.21(0.22 + 0.05 + 0.13 − 0.19).
#   특별항목(notable items) 주당 −3.75: Q4 −1.86(브라질 이연법인세 평가충당금 −0.82, Carlsbad 칼륨 광산 매각 예정 손실 −0.38, 브라질 영업권 손상 −0.28, Ma'aden 평가손 −0.25 등 — Fable r1),
#   Q1 −0.86(Araxá·Patrocínio 가동 중단 비용 $442M 세전), Q2 −0.99(Ma'aden 평가손 $162M·프로젝트 상각 $69M·환손실 $49M 세전), Q3 −0.04. 일회성이 GAAP를 음수로 만들어 미완성.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 0, 0), '판정 보류'
CO = 'Mosaic'
S_ = 'https://www.sec.gov/Archives/edgar/data/1285785/'
SEC = S_
TENQ = S_ + '000128578526000147/mos-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000128578526000139/pressreleaseq32026-ex991.htm', 'q2': S_ + '000128578526000109/pressreleaseq22026-ex991.htm',
      'q1': S_ + '000128578526000063/pressreleaseq12026-ex991.htm', 'q4': S_ + '000128578526000013/pressreleaseq42025-ex991.htm',
      'prelim': S_ + '000128578526000007/q425marketupdateandpre-rel.htm', 'araxa': S_ + '000128578526000058/pressrelease-exhibit991.htm',
      'tender': S_ + '000119312526341391/d319503dex991.htm', 'notes': S_ + '000119312526354095/d168739d8k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="mosFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(일회성 손실로 최근 4분기 GAAP 이익이 적자다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-20, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 최근 4분기 GAAP 희석 EPS 합계가 약 −$3.54로 적자인데, 회사가 특별항목으로 빼는 손실이 주당 약 $3.75라 이를 빼면 조정 EPS는 약 $0.21로 겨우 흑자다. '
              '2025년 4분기에 브라질 법인의 이연법인세 자산 평가충당금(주당 약 $0.82)과 브라질 영업권 손상(약 $0.28), 매각한 뉴멕시코 Carlsbad 칼륨 광산의 매각 예정 자산 손실(약 $0.38)이 한꺼번에 잡혔다. '
              '2026년 1분기에는 브라질 Araxá·Patrocínio 인산 공장 가동 중단 비용($442M, 세전 — 다른 항목과 상계한 특별항목 순액은 $323M), 2분기에는 사우디 Ma’aden 주식 평가손($162M)과 프로젝트 상각이 컸다. '
              'Ma’aden 주식은 9월 말 장부가가 약 $1.8B로 커서, 사우디 증시 주가에 따라 분기마다 많게는 수억 달러의 평가손익이 GAAP 이익을 흔든다. '
              '본업도 약해졌다 — 이란 긴장·호르무즈 해협 차질로 황 가격이 크게 올라(3분기 평균 롱톤당 $715) 인산 비료 생산을 줄였고, 브라질은 원료 부족과 고객 신용 위축으로 판매가 줄었다. 3분기 조정 EBITDA는 $324M으로 1년 전($806M)의 절반에 못 미치고, 3분기는 특별항목을 빼도 조정 EPS가 −$0.19로 적자다. '
              '이익을 내는 칼륨 부문도 캐나다 Esterhazy 광산의 광석 품위가 낮아져 2026년 생산 전망을 860만 톤으로 낮췄다. 회사는 4분기 황 계약을 롱톤당 $615로 낮췄지만 비싸게 산 원료가 원가에 반영되고 추가 감산을 해 4분기 마진은 더 줄 것으로 봤다. '
              '설비투자는 2026년 $1.2B, 2027년 $1B 아래를 목표로 하고, 자산 포트폴리오 전략적 검토로 Araxá 매각과 토지 매각을 진행한다. '
              '6월에 $1.0B 텀론 약정을 맺고, 8월에 채권 $2.0B를 새로 발행해 공개매수와 조기 상환으로 2027~2029년 만기 채권 약 $1.4B를 갚으면서 2028년까지 장기 만기를 없앴다 — 2029년에는 남은 채권 $339M과 텀론 $500M이 돌아온다. 분기 배당은 주당 $0.22다. '
              '2025년 4분기 특별항목은 2026년 4분기 실적(2027년 2월) 뒤, 2026년 1·2분기 항목은 2027년 5·8월 뒤 최근 4분기에서 빠진다. '
              '그때 GAAP 이익이 흑자면 정식 판정으로 다시 보고, 조정 이익까지 적자로 남으면 일회성 문제가 아니라 본업 적자 종목으로 다시 분류한다.')
PH = ['CF', 'LYB', 'DOW', 'NUE', 'FCX', 'ALB']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소재 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(MOS 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·포장·건자재가 섞여 있다. 차트에는 비료·화학·금속 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 주석): 인산 1,294.9 + 칼륨 643.4 + Mosaic Fertilizantes 1,254.0 − 본사·기타·상계 91.7 = 연결 3,100.6(Codex r1 — 보도자료 정수값 대신).
SEG = [('인산 비료(미국)', 1294.9, '#006a4e'), ('칼륨(캐나다)', 643.4, '#f2a900'), ('Mosaic Fertilizantes(브라질)', 1254.0, '#cfe5dc')]
SEG_ADJ = -91.7
SEG_ADJ_LABEL = '본사·기타·부문 간 상계'
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건 + 4분기 예비 실적 + Araxá 가동 중단 + 채권 차환 2건. 반응일은 8-K 접수 시각 기준.
NEWS_RANGE = '2026.01 ~ 2026.11'
NEWS = [
    ('green', '2026년 11월 3일 장 마감 뒤 — Q3 2026 실적', '2026-11-04',
     '매출 $3.10B(−10%) · 순손실 $72M · 희석 EPS −$0.23(1년 전 $1.29) · 조정 EPS −$0.19 · 4분기 황 계약 롱톤당 $615(3분기 평균 $715) · 2027년 설비투자 $1B 아래 목표 — 다음 날 주가 +17.4%', 'q3', 'Mosaic 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 17일 장 마감 뒤 — 신규 채권 $2.0B 발행 완료', '2026-08-18',
     '2031년 5.35% $1.0B · 2034년 5.65% $0.5B · 2036년 5.90% $0.5B — 2027~2029년 만기 채권 공개매수 자금, 8월 28일에는 2027·2028년 채권 잔량 전액 조기 상환을 통지(9월 상환) — 다음 날 주가 −0.4%', 'notes', 'Mosaic 공시 (SEC 8-K)'),
    ('neutral', '2026년 8월 10일 장 전 — 채권 공개매수 시작', '2026-08-10',
     '2027·2028·2029년 만기 채권을 최대 $1.4B까지 현금 매입 — 그날 주가 +1.8%', 'tender', 'Mosaic 보도자료 (SEC 8-K)'),
    ('green', '2026년 8월 4일 장 마감 뒤 — Q2 2026 실적', '2026-08-05',
     '매출 $2.8B · 순손실 $273M · 희석 EPS −$0.86 · 조정 EPS $0.13 — Ma’aden 주식 평가손 $162M 등 특별항목 $351M(세전) · 2026년 설비투자 전망 $1.2B로 축소 — 다음 날 주가 +3.1%', 'q2', 'Mosaic 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 5월 11일 장중 — Q1 2026 실적', '2026-05-11',
     '매출 $3.0B · 순손실 $258M · 희석 EPS −$0.81 · 조정 EPS $0.05 — Araxá·Patrocínio 가동 중단 비용 $442M(세전) · 원료 부족으로 5월부터 인산 생산 일부 감축 — 그날 주가 −1.8%', 'q1', 'Mosaic 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 4월 8일 장중 — 브라질 Araxá·Patrocínio 가동 중단', '2026-04-08',
     'Araxá 공장 가동 중단·매각 추진, Patrocínio 채굴 중단(나이오븀 사업 검토는 계속) — 연 인산 생산 약 100만 톤 감소 · 일회성 비용 $350~400M 예상 · 같은 달 뉴멕시코 Carlsbad 칼륨 광산 매각 완료 — 그날 주가 +0.9%', 'araxa', 'Mosaic 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 24일 장 마감 뒤 — 2025년 연간 실적', '2026-02-25',
     '4분기 순손실 $519M · 희석 EPS −$1.64(브라질 이연법인세 평가충당금·브라질 영업권 손상·Carlsbad 칼륨 광산 매각 손실 등) · 조정 EPS $0.22 · 2025년 순이익 $541M · 희석 EPS $1.70 — 다음 날 주가 −5.3%', 'q4', 'Mosaic 실적 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 16일 장 전 — 4분기 예비 판매 실적', '2026-01-16',
     '북미 비료 수요가 계절 둔화보다 크게 줄어 4분기 인산 판매 약 130만 톤 · 칼륨 약 220만 톤 — 그날 주가 −4.5%', 'prelim', 'Mosaic 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 20, 'nt': 15, 'mean': 24.07, 'median': 23, 'low': 17, 'high': 30, 'sb': 5, 'b': 3, 'h': 11, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-08'

# 미완성 카드 표시(2026-11-07 사용자 규칙, D·SRE 방식).
INCOMPLETE_SHORT = '일회성 손실로 GAAP 적자'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익이 브라질 이연법인세 평가충당금·공장 가동 중단 비용·Ma’aden 주식 평가손 같은 일회성 손실 때문에 적자다(회사 조정 이익은 흑자) — 배수 판정이 왜곡돼 보류한다. 이 손실이 최근 4분기에서 빠지는 2027년에 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익이 브라질 이연법인세 평가충당금·공장 가동 중단 비용·Ma’aden 주식 평가손 같은 일회성 손실 때문에 적자다(회사 조정 이익은 흑자) — 배수 판정이 왜곡돼 보류한다. 이 손실이 최근 4분기에서 빠지는 2027년에 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 일회성 손실로 GAAP 적자</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 일회성 손실로 GAAP 적자. 최근 4분기 이익이 일회성 손실로 적자라 현금흐름 내재가치를 계산하지 않았다.')
h = _re0.sub(r'(id="mosFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">일회성 손실로 GAAP 적자</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]


# ── 자동 카드 — 부문 지도(seg_map_propose 뒤 원문 대조). 원문: Q3 2026 10-Q 인산 1,294.9 + 칼륨 643.4 + 브라질 1,254.0 − 상계 91.7 = 3,100.6 ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"mos:PhosphatesSegmentMember": ["인산 비료(미국)", "#006a4e"],
             "mos:PotashSegmentMember": ["칼륨(캐나다)", "#f2a900"],
             "mos:MosaicFertilizantesMember": ["Mosaic Fertilizantes(브라질)", "#cfe5dc"]},
 "ignore": ["mos:CorporateEliminationsAndOtherSegmentMember"]
}
