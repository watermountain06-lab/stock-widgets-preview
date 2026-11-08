CIK = '0000915913'
BUILD = {'no_dcf': '미완성 — 자산 손상·세금 항목 등 큰 일회성이 최근 4분기 GAAP 이익을 크게 낮춘다'}   # 2026-11-08 사용자 규칙(D군 — 일회성 30% 이상이면 미완성 카드)
# ALB(앨버말) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 31일. 리튬(Energy Storage — 호주 Talison·칠레 등), 브로민·특수화학(Specialties), Ketjen 지분(2026-03 매각 뒤 소수 지분).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-04 16:26 동부 장 마감 뒤 → 첫 세션 11-05, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 마감 뒤 16:1x~16:2x 동부 → 다음 날),
#        Ketjen 지분 51% 매각 완료(2026-03-02), CEO 승계(2026-09-03 17:00 동부 → 09-04), 새 신용한도(10-29).
# 엔진 입력(2026-11-08): 차입금 $1,881M(금융리스 $104M 포함 — 장기차입 합계), 현금 $1,846M, 비지배지분 $278M, 우선주(의무 전환) $2,235M(2027-03-01 보통주로 자동 전환 예정).
#   4분기 EPS 2021·2022·2023·2025는 보도자료 GAAP 희석 EPS(Q4_EPS_OVERRIDE — Codex r1). 금융리스는 차입금 안에 있어 따로 더하지 않는다(FL_IN_DEBT). 희석 EPS는 우선주 배당을 뺀 보통주 귀속 기준.
# 일회성(E54): 최근 4분기 GAAP 희석 EPS 4.14(−3.87 + 2.34 + 3.52 + 2.15) 대 회사 조정 EPS 8.75(−0.53 + 2.95 + 3.75 + 2.58).
#   회사가 뺀 세후 항목: Q4 2025 $393.7M(Ketjen 관련 장기자산 손상 주당 2.09·세금 항목 0.73 — 미국 이연법인세 전액 평가충당금·기타 0.28 등, 합계 주당 3.19),
#   2026년 9개월 $170.4M(사업 매각 손실 0.39·구조조정 0.30·전략적 비용 절감 0.22·세금 0.19·채무 조기 상환 이익 −0.09 등) → 합 약 $564M = GAAP 순이익(Albemarle 귀속) $682M의 약 83%.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (1, 0, 0), '판정 보류'
CO = 'Albemarle'
S_ = 'https://www.sec.gov/Archives/edgar/data/915913/'
SEC = S_
TENQ = S_ + '000091591326000129/alb-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000091591326000128/a3q26earningsreleaseex991.htm', 'q2': S_ + '000091591326000101/a2q26earningsreleaseex991.htm',
      'q1': S_ + '000091591326000070/a1q26earningsreleaseex991.htm', 'q4': S_ + '000091591326000016/a4q25earningsreleaseex991.htm',
      'ketjen': S_ + '000091591326000032/a03-06x20268xkexhibit991.htm', 'ceo': S_ + '000114036126035623/ef20081522_8k.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="albFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(자산 손상·세금 항목 등 큰 일회성이 최근 4분기 GAAP 이익을 크게 낮춘다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-40, 60)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 일회성 항목이 최근 4분기 GAAP 이익의 30% 이상이면 판정을 보류하는데, ALB는 회사가 조정 이익에서 뺀 세후 항목이 약 $564M으로 최근 4분기 GAAP 순이익(약 $682M)의 80%를 넘는다. '
              '대부분 2025년 4분기에 몰려 있다 — Ketjen(정유 촉매) 사업 매각가에 맞춰 자산을 깎은 손상($245.6M, 주당 약 $2.09)과 Ketjen 관련 미국 세무상 장부가 차이 세금($86.2M, 주당 약 $0.73)이 커서 그 분기 희석 EPS가 −$3.87이었다. '
              '같은 분기에 미국 이연법인세 자산 전액에 평가충당금(앞으로 세금을 덜 낼 권리를 장부에서 0으로 본 것)도 쌓았는데, 이것은 회사도 조정 이익에서 빼지 않아 조정 EPS(−$0.53)에도 남아 있고, 앞으로도 미국·호주·중국 쪽 손익에 세금 효과가 붙지 않아 세율이 들쭉날쭉할 수 있다. '
              '2026년에는 Ketjen 지분 51%와 Eurecat 합작 지분 매각 손실($52.7M, 1분기), 호주 Kemerton 1호 라인 가동 중단 등 구조조정, 전략적 비용 절감 비용이 이어졌고, Kemerton 정리 비용은 2027년까지 $60~80M 더 들 것으로 회사가 예상한다. '
              '본업은 리튬 가격 반등으로 크게 좋아졌다 — 3분기 회사 전체 매출이 19% 늘고 조정 EBITDA가 약 2.9배가 됐는데, 그 중심인 에너지 저장 부문은 실현가격이 1년 전의 약 두 배가 돼 판매량이 19% 줄었는데도(1년 전 분기가 재고 조정으로 이례적으로 많았음) 매출이 58% 늘고 조정 EBITDA가 약 4.5배가 됐다. '
              '다만 회사는 4분기에 리튬 시장 가격이 내려 매출·조정 EBITDA가 3분기보다 줄고, 비싸게 산 원료 재고 때문에 마진도 줄 것으로 예고했다. 특수화학 부문은 연간 조정 EBITDA 전망을 $350~375M으로 올렸지만 중동 분쟁으로 물류·원료 비용이 올랐다. 연간 설비투자 전망은 $300~350M으로 낮췄다. '
              'Ketjen 매각 대금과 보유 현금으로 채권을 갚아 장기차입금이 2025년 말 $3.2B에서 9월 말 $1.9B로 줄었고, 10월에 $1.5B 신용한도(2031년 만기)를 새로 맺었다. '
              '희석 EPS는 분기마다 우선주($2.2B 규모 의무 전환 우선주, 배당 연 $167M)의 배당을 빼거나 보통주 전환을 가정하는 것 중 더 희석되는 쪽으로 계산한다(3분기는 배당 차감, 2분기는 전환 가정). 이 우선주는 2027년 3월 1일 보통주로 자동 전환될 예정이라 보통주가 약 15~18% 늘어난다. '
              '경영진도 바뀐다 — 2026년 9월 이사회가 Ragnar Udd를 2027년 2월 1일부터 CEO로 정했고 Kent Masters는 집행 의장으로 남는다. 주가는 리튬 가격에 크게 흔들려 4~5월 고점에서 절반 넘게 내렸다. '
              '2025년 4분기 손상·세금 항목은 2026년 4분기 실적(2027년 2월) 뒤 최근 4분기에서 빠지므로 그때 다시 본다 — 그 직후 3월 우선주 전환으로 주식 수와 EPS 기준이 바뀐다는 점도 함께 본다.')
PH = ['LYB', 'DOW', 'CF', 'MOS', 'FCX', 'NUE']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '소재 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(ALB 제외)와 배수 순위를 매긴 값이다.',
            '화학·금속·포장·건자재가 섞여 있다. 차트에는 화학·비료·금속 6곳만 보인다.')
# 매출(Q3 2026 보도자료 부문 표): 에너지 저장 1,118.8 + 특수화학 388.6 + 본사·기타 45.7 = 1,553.1.
SEG = [('에너지 저장(리튬)', 1118.8, '#00205b'), ('특수화학(브로민 등)', 388.6, '#a6c63a')]
SEG_ADJ = 45.7
SEG_ADJ_LABEL = '본사·기타(부문 밖 매출)'
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건 + Ketjen 매각 완료 + CEO 승계. 반응일: 실적 8-K 장 마감 뒤 → 다음 날.
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('green', '2026년 11월 4일 장 마감 뒤 — Q3 2026 실적', '2026-11-05',
     '매출 $1.55B(+19%, 리튬 가격 +68%) · 희석 EPS $2.15(1년 전 −$1.72) · 조정 EPS $2.58 · 조정 EBITDA $646M(+186%) · 특수화학 전망 상향·설비투자 전망 축소 — 다음 날 주가 +3.6%', 'q3', 'Albemarle 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 9월 3일 — CEO 승계', '2026-09-03',
     'Ragnar Udd를 2027년 2월 1일부터 CEO로, Kent Masters는 집행 의장으로 · 8-K는 장 마감 뒤 접수, 보도자료 시각은 공시에 없음 — 그날 주가 −4.1%, 다음 날 −4.4%', 'ceo', 'Albemarle 공시 (SEC 8-K)'),
    ('green', '2026년 8월 5일 장 마감 뒤 — Q2 2026 실적', '2026-08-06',
     '매출 $1.7B(+31%) · 희석 EPS $3.52(1년 전 −$0.16) · 조정 EPS $3.75 · 조정 EBITDA $858M(+155%) — 다음 날 주가 +5.5%', 'q2', 'Albemarle 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 6일 장 마감 뒤 — Q1 2026 실적', '2026-05-07',
     '매출 $1.4B(+33%) · 희석 EPS $2.34 · 조정 EPS $2.95(Ketjen 매각 손실 등 제외) · 조정 EBITDA $664M(+148%) — 다음 날 주가 +3.0%', 'q1', 'Albemarle 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 2일 장 마감 뒤 — Ketjen 지분 51% 매각 완료', '2026-03-03',
     'KPS Capital Partners에 정유 촉매 사업 지배 지분 매각(소수 지분은 보유, 성능 촉매 사업은 남김, 1월 Eurecat 합작 지분 매각과 합쳐 현금 약 $670M) — 매각 대금으로 채권 공개매수·상환 — 다음 날 주가 −7.5%', 'ketjen', 'Albemarle 보도자료 (SEC 8-K)'),
    ('red', '2026년 2월 11일 장 마감 뒤 — 2025년 연간 실적', '2026-02-12',
     '4분기 매출 $1.4B(+16%) · 희석 EPS −$3.87(Ketjen 자산 손상·Ketjen 관련 세금 등, 미국 이연법인세 평가충당금은 조정 EPS에도 남음) · 조정 EPS −$0.53 — 다음 날 주가 −9.4%', 'q4', 'Albemarle 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 23, 'nt': 19, 'mean': 164.89, 'median': 161, 'low': 95, 'high': 250, 'sb': 11, 'b': 3, 'h': 9, 's': 0, 'ss': 0}
ANALYST_ASOF = '2026-11-08'

# 파이프라인 자동 재판정용 — 일회성이 든 분기(결산일: 항목). 이 분기들이 최근 4분기에서 빠지면 다시 본다(2026-11-08 사용자 결정).
ONEOFF_QUARTERS = {'2025-12-31': 'Ketjen 관련 장기자산 손상·세금 항목 등(세후 $393.7M, 비경상 375.6 + 연금 18.2)',
                   '2026-03-31': 'Ketjen 지분 매각 손실·구조조정(세후 $82.4M)',
                   '2026-06-30': '구조조정·기타(세후 $31.2M)',
                   '2026-09-30': '구조조정·전략적 비용 절감·세금(세후 $56.9M)'}   # 분기 금액은 비경상 + 비영업 연금/OPEB(합 $564.1M, Codex r1)

# 미완성 카드 표시(2026-11-08 사용자 규칙, D·SRE 방식).
INCOMPLETE_SHORT = '큰 일회성으로 이익 왜곡'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익에 Ketjen 관련 자산 손상·세금 항목 같은 큰 일회성 비용이 GAAP 순이익의 80% 넘게 들어 있다 — 배수 판정이 왜곡돼 보류한다. 이 항목들이 최근 4분기에서 빠지면 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익에 Ketjen 관련 자산 손상·세금 항목 같은 큰 일회성 비용이 GAAP 순이익의 80% 넘게 들어 있다 — 배수 판정이 왜곡돼 보류한다. 이 항목들이 최근 4분기에서 빠지면 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 큰 일회성으로 이익 왜곡</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 큰 일회성으로 이익 왜곡. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="albFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">큰 일회성으로 이익 왜곡</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
"""]


# ── 자동 카드 — 부문 지도(seg_map_propose 뒤 원문 대조). 원문: Q3 2026 보도자료 1,118.8 + 388.6 + 45.7 = 1,553.1 ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"alb:EnergyStorageMember": ["에너지 저장(리튬)", "#00205b"],
             "alb:SpecialtiesMember": ["특수화학(브로민 등)", "#a6c63a"]}
}
