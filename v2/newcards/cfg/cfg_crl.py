CIK = '0001100682'
BUILD = {'no_dcf': '미완성 — 손상 손실과 세금 충당금 환입 등 큰 일회성이 최근 4분기 GAAP 이익을 흔든다'}   # 2026-11-08 사용자 규칙(D군 — 일회성 30% 이상이면 미완성)
# CRL(찰스 리버 연구소) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 마지막 토요일. 연구용 동물 모델(RMS), 비임상 시험·신약 탐색(DSA), 제조 지원(Manufacturing).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-04 10:03 동부 장중 → 그날, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 07:1x~08:1x 동부 → 그날),
#        CEO 승계(2026-01-08 발표, 01-09 16:18 동부 8-K), SEC 조사 종료(2025-11-17 08:06 동부), CDMO·Cell Solutions 매각(2026-05-06), 유럽 Discovery 매각(05-22).
# 엔진 입력(2026-11-08): 차입금 $2,446M(금융리스 $9.7M 포함 — FL_IN_DEBT), 현금 $200M, 4분기 EPS 2025는 보도자료 −$5.62(Q4_EPS_OVERRIDE, 역산 −5.57).
#   최근 4분기 순이익률이 낮아 PER은 '해당 없음'(A3).
# 일회성(E54): 최근 4분기 GAAP 희석 EPS 0.91(−5.62 − 0.30 − 0.03 + 6.86) 대 회사 조정 EPS 10.56(2.39 + 2.06 + 3.02 + 3.09).
#   Q4 2025 Biologics Solutions·Cell Solutions 무형자산 손상 $211.0M(주당 3.22) + 영업권 손상 $165.0M(3.35), Q3 2026 해외 인수 세금 충당금 환입 $245.6M(주당 5.06, 비현금 이익),
#   2026년 상반기 CDMO·Cell Solutions 매각 손실 Q1 $118.0M·Q2 $63.7M(Q1 부동산 매각 이익 $38.5M) 등 → 일회성이 GAAP 이익보다 훨씬 크다.
CUR, YO, QO = '2026-09-26', '2025-09-27', '2026-06-27'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-27', '2024-12-28'), 'FY2025'
VOTES, VERDICT = (-1, -1, 0), '판정 보류'
CO = 'Charles River Laboratories'
S_ = 'https://www.sec.gov/Archives/edgar/data/1100682/'
SEC = S_
TENQ = S_ + '000110068226000157/crl-20260926.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000110068226000156/crl3q26earningsrelease.htm', 'q2': S_ + '000110068226000115/crl2q26earningsrelease.htm',
      'q1': S_ + '000110068226000036/crl1q26earningsrelease.htm', 'q4': S_ + '000110068226000020/crl4q25earningsrelease.htm',
      'ceo': S_ + '000162828026001603/crl-20260108.htm', 'sec': S_ + '000162828025052484/crl-20251114.htm',
      'inv': S_ + '000110068226000142/crlinvestorday2026pressr.htm', 'div': S_ + '000162828026011395/crl-20260225.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="crlFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(손상 손실과 세금 충당금 환입 등 큰 일회성이 최근 4분기 GAAP 이익을 흔든다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-30, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 일회성 항목이 최근 4분기 GAAP 이익의 30% 이상이면 판정을 보류하는데, CRL은 반대 방향의 큰 일회성이 겹쳐 최근 4분기 GAAP 희석 EPS가 $0.91뿐이다(회사 조정 EPS는 $10.56). '
              '2025년 4분기에 CDMO(생물의약품 위탁생산)·Cell Solutions 사업의 무형자산·영업권 손상 $376M(비현금, 주당 약 $6.57)이 잡혀 그 분기 희석 EPS가 −$5.62였고, '
              '2026년 3분기에는 1월 인수한 캄보디아 NHP 공급업체에 딸려 온 세금 충당금을 현지 세법 제정으로 되돌린 이익 $245.6M(비현금, 주당 약 $5.06, 영업이익에 잡힌 $44.6M 포함)이 들어와 희석 EPS가 $6.86이 됐다. 그 사이 상반기에는 CDMO·Cell Solutions 매각 관련 손실이 1분기 $118.0M(주당 1.53), 2분기 $63.7M(주당 1.40) 잡혔고(1분기에는 부동산 매각 이익 $38.5M도 있었다), 구조조정 비용이 이어졌다. '
              '포트폴리오도 크게 바꿨다 — 2026년 5월 손상이 났던 CDMO·Cell Solutions 사업을 오히려 순현금 $12.4M을 얹어 GI Partners에 넘겼고(4년간 손실 보전 최대 $45M 부담, 성과에 따라 최대 $50M 회수 가능), 유럽 Discovery 사업 일부를 IQVIA에 $126M에 팔았으며, '
              '1월에는 비인간 영장류(NHP) 공급 안정을 위해 캄보디아 공급업체 자산을 약 $507M(일부 후불)에 사고, 4월에는 차세대 염기서열 분석 회사 PathoQuest를 100% 자회사로 만들었다. '
              '본업은 회복 중이다 — 신약 개발 고객의 비임상 시험 수요가 살아나 3분기 유기적 매출이 4.7% 늘었고(비임상 시험 부문 5.9%), 회사는 2026년 매출·조정 EPS 전망을 두 번 올렸다(조정 EPS $11.35–11.55). 9월 투자자 데이에서는 2027–2030년 유기적 매출 연 5–7% 성장, 조정 영업이익률 약 24%, 구조조정 프로그램 Create the Future로 4년 누적 $300M 넘는 비용 절감을 목표로 냈다. '
              '오래 이어진 NHP 조달 관련 SEC 조사는 2025년 11월 제재 권고 없이 끝났지만, 같은 사안의 증권 집단소송은 2026년 9월 2차 수정소장이 나와 계속된다. 2026년 5월 오래 CEO를 맡았던 James Foster가 물러나고 Birgit Girshick가 CEO가 됐다. 9개월 동안 승인 프로그램으로 자사주 $300M을 샀다(현금흐름표상 자기주식 취득은 임직원 세금 원천징수분을 더해 $324M). '
              '주가는 5월 저점 약 $150에서 11월 $330대로 두 배 넘게 올랐다. 최근 4분기 GAAP 이익이 매우 작아 PER 숫자는 수백 배로 나오며, 평가와 평균에서는 뺀다. '
              '판정 재개는 이르면 2027년 11월(2027년 3분기 실적) 뒤다. 2027년 2월에는 손상만 최근 4분기에서 빠지고 세금 환입(주당 $5.06)은 남으며, 상반기 매각 손실도 2027년 8월까지 남는다 — 그때마다 30% 규칙을 다시 적용한다.')
PH = ['IQV', 'TMO', 'DHR', 'A', 'MTD', 'WAT']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '생명과학 도구·서비스 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(CRL 제외)와 배수 순위를 매긴 값이다.',
            '제약·의료기기·보험이 섞여 있다. 차트에는 생명과학 도구·서비스 6곳만 보인다.')
# 매출(Q3 2026 보도자료 부문): 비임상 시험·탐색(DSA) 596.3 + 연구 모델(RMS) 207.5 + 제조 지원 178.9 = 982.7.
SEG = [('비임상 시험·신약 탐색(DSA)', 596.3, '#00558c'), ('연구용 동물 모델(RMS)', 207.5, '#78be20'), ('제조 지원(미생물·생물의약품 시험)', 178.9, '#cfdde9')]
SEG_ADJ = 0
SEG_TITLE = '매출 구성 — 부문별'
# 손 뉴스: 실적 4건 + 투자자 데이 + 매각 발표 + CEO 승계 + SEC 조사 종료. 색은 사건 성격, 수치는 그날 주가. 반응일: 실적 8-K 장 전 → 그날.
NEWS_RANGE = '2025.11 ~ 2026.11'
NEWS = [
    ('green', '2026년 11월 4일 장 전 — Q3 2026 실적', '2026-11-04',
     '매출 $983M(유기 +4.7%) · 희석 EPS $6.86(세금 충당금 환입 주당 $5.06 포함) · 조정 EPS $3.09(+27%) · 연간 전망 상향 — 그날 주가 −7.3%', 'q3', 'Charles River 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 9월 24일 — 투자자 데이 · 2030 목표', '2026-09-24',
     '2027–2030년 유기 매출 연 5–7% · 조정 영업이익률 약 24% · 조정 EPS 연 10%대 초반 성장 목표, 구조조정 Create the Future로 누적 $300M+ 절감, 2026 전망 상단 재확인 — 그날 주가 +6.2%', 'inv', 'Charles River 투자자 데이 보도자료 (SEC 8-K)'),
    ('green', '2026년 8월 5일 장 전 — Q2 2026 실적', '2026-08-05',
     '매출 $1.00B(유기 +0.1% — 유기 성장률이 2023년 3분기 뒤 가장 높음) · 희석 EPS −$0.03 · 조정 EPS $3.02 · 연간 전망 상향 · 5월 CDMO·Cell Solutions 등 매각 완료 — 그날 주가 +11.4%', 'q2', 'Charles River 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 7일 장 전 — Q1 2026 실적', '2026-05-07',
     '매출 $996M(유기 −1.5%) · 희석 EPS −$0.30 · 조정 EPS $2.06 · 연간 전망 유지 · 자사주 $200M — 그날 주가 0.0%', 'q1', 'Charles River 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 25일 — CDMO·Cell Solutions 매각 발표', '2026-02-25',
     'CDMO·Cell Solutions를 GI Partners에, 유럽 Discovery 일부를 IQVIA에 매각하기로 — 2026년 조정 영업이익률 1%p 이상 개선, 조정 EPS 전망 +$0.10(5월 완료 때 CRL이 순현금 $12.4M을 지급) — 그날 주가 +0.9%(다음 날 +4.7%)', 'div', 'Charles River 공시 (SEC 8-K)'),
    ('neutral', '2026년 2월 18일 장 전 — 2025년 연간 실적', '2026-02-18',
     '4분기 매출 $994M(유기 −2.6%) · 희석 EPS −$5.62(무형자산·영업권 손상 $376M) · 조정 EPS $2.39 · 2026년 전망 첫 제시 — 그날 주가 −0.3%', 'q4', 'Charles River 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 1월 8일 — CEO 승계 발표', '2026-01-08',
     'James Foster 회장 겸 CEO가 5월 5일 물러나고 Birgit Girshick COO가 CEO로 — 발표는 1월 8일 장 전, 8-K는 1월 9일 접수 — 1월 8일 주가 −0.6%', 'ceo', 'Charles River 공시 (SEC 8-K)'),
    ('green', '2025년 11월 17일 장 전 — SEC 조사 종료', '2025-11-17',
     'NHP 조달·공시 관련 SEC 집행국 조사가 제재 권고 없이 끝남 · 회사 자체 독립 조사도 중대한 문제 없이 종료 — 그날 주가 −3.0%', 'sec', 'Charles River 공시 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 17, 'nt': 15, 'mean': 335.8, 'median': 340, 'low': 219, 'high': 400, 'sb': 11, 'b': 3, 'h': 2, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-08'

# 파이프라인 자동 재판정용 — 일회성이 든 분기(결산일: 항목).
ONEOFF_QUARTERS = {'2025-12-27': '무형자산·영업권 손상 $376M(주당 6.57)',
                   '2026-03-28': 'CDMO·Cell Solutions 매각 예정 자산 손실 $118.0M(주당 1.53), 부동산 매각 이익 $38.5M',
                   '2026-06-27': 'CDMO·Cell Solutions 매각 손실 $63.7M(주당 1.40)',
                   '2026-09-26': '해외 세금 충당금 환입 이익 $245.6M(주당 5.06)'}

# 미완성 카드 표시(2026-11-08 사용자 규칙, D·SRE 방식).
INCOMPLETE_SHORT = '큰 일회성으로 이익 왜곡'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익에 큰 손상 손실과 큰 세금 충당금 환입 이익이 함께 들어 있어 회사 조정 이익과 크게 다르다 — 배수 판정이 왜곡돼 보류한다. 판정 재개는 이르면 2027년 11월(2027년 3분기 실적) 뒤 — 2027년 2월에는 손상만 빠지고 세금 환입은 남는다'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익에 큰 손상 손실과 큰 세금 충당금 환입 이익이 함께 들어 있어 회사 조정 이익과 크게 다르다 — 배수 판정이 왜곡돼 보류한다. 판정 재개는 이르면 2027년 11월(2027년 3분기 실적) 뒤 — 2027년 2월에는 손상만 빠지고 세금 환입은 남는다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 큰 일회성으로 이익 왜곡</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 큰 일회성으로 이익 왜곡. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="crlFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
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
# Fable r1: 일회성에 왜곡된 GAAP 마진·매각 효과를 Bear·체크포인트에서 걷어낸다
_b1 = '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">마진</span><span class="bb-text">최근 4분기 영업이익률 4.0%(5년 중앙값 14.0%).</span></div>'
assert _b1 in h
h = h.replace(_b1, '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">소송</span><span class="bb-text">NHP 조달 관련 증권 집단소송이 계속된다 — 2026년 9월 2차 수정소장(회사·전 CEO 피고), 회사는 10월 기각 신청.</span></div>', 1)
h = _re0.sub(r'\s*<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">부문</span>.*?</div>', '\n      <div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">비용</span><span class="bb-text">9월 시작한 다년 구조조정(Create the Future) 비용이 이어진다 — 2026년 조정 EPS에서 뺀 구조조정·효율화 비용 전망 주당 약 $1.50.</span></div>', h, count=1, flags=_re0.S)
_c1 = '<strong style="color:var(--accent2);">①</strong> 매출 증가율(1년 전 대비)이 최근 흐름(+1.2% → −2.7% → −2.2%)보다 낮아지지 않는지'
assert _c1 in h
h = h.replace(_c1, '<strong style="color:var(--accent2);">①</strong> 유기 매출 증가율이 Q3 2026 +4.7% 흐름을 지키는지(보고 기준 +1.2% → −2.7% → −2.2%는 매각 영향으로 2027년 5월까지 약 4.5%p 낮게 나온다)', 1)
_c2 = h[h.index('<strong style="color:var(--accent2);">②</strong>'):]; _c2 = _c2[:_c2.index('</div>')]
h = h.replace(_c2, '<strong style="color:var(--accent2);">②</strong> Q4 2026 회사 조정 영업이익률이 1년 전 같은 분기(Q4 2025 18.1%)보다 높은지(직전 Q3 2026 23.0%) — GAAP 마진은 손상·환입이 섞여 비교에 쓰지 않는다', 1)
h = h.replace('영업이익률 20.6%(1년 전 13.3%).', '영업이익률 20.6%(1년 전 13.3%, 세금 충당금 환입 $44.6M 포함).', 1)
h = h.replace('🔍 다음 확인 포인트 · 2027년 2월 17일 무렵 (예상) Q4 2026 실적 공시.', '🔍 다음 확인 포인트 · 2027년 2월 17일 무렵 (예상) Q4 2026 실적 공시. 판정 재개는 이르면 2027년 11월(Q3 2027 실적) 뒤.', 1)
h = h.replace('제조 지원(미생물·생물의약품 시험) −6.2% · 출처', '제조 지원(미생물·생물의약품 시험) −6.2% — 보고 기준이며 매각 영향을 뺀 유기 성장은 DSA +5.9%, RMS −0.6%, 제조 지원 +7.4% · 출처', 1)
"""]


# ── 자동 카드 — 부문 지도(seg_map_propose 뒤 원문 대조). 원문: Q3 2026 보도자료 596.3 + 207.5 + 178.9 = 982.7 ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"crl:DiscoveryAndSafetyAssessmentSegmentMember": ["비임상 시험·신약 탐색(DSA)", "#00558c"],
             "crl:ResearchModelsAndServicesSegmentMember": ["연구용 동물 모델(RMS)", "#78be20"],
             "crl:ManufacturingSupportSegmentMember": ["제조 지원(미생물·생물의약품 시험)", "#cfdde9"]}
}
