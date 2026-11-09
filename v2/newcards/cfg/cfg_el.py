CIK = '0001001250'
BUILD = {'no_dcf': '미완성 — 구조조정·소송 합의 등 일회성이 최근 4분기 GAAP 이익보다 크다(약 190%)'}   # 2026-11-08 사용자 규칙(일회성 30% 이상이면 미완성) — ZBH·GIS와 같은 처리
# EL(에스티 로더) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 6월 말(FY27 = 2026-07~2027-06). 스킨케어(La Mer·The Ordinary·Clinique)·메이크업(M·A·C)·향수(TOM FORD·Le Labo·Jo Malone)·헤어.
# 출처: SEC XBRL, Q1 FY27 10-Q(2026-11-02 12:06 동부 → 그날, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 07:0x~08:0x 동부 → 그날),
#        Puig 합병 협의 확인(2026-03-23 18:24 동부 장 마감 뒤 → 3-24), 투자자 행사 Capital Markets Experience(2026-11-04 06:23 동부 → 그날).
# 일회성(E54): 최근 4분기 GAAP 희석 EPS 1.00(0.44 + 0.24 − 0.32 + 0.64) 대 회사 조정 EPS 2.91(0.89 + 0.91 + 0.39 + 0.72).
#   차이 1.91(세후 주당, 회사 조정표): Q2 FY26 0.45(구조조정 반품·비용 $207M), Q3 FY26 0.67(구조조정 $224M + 증권 집단소송 합의 $84M — 연간 0.18),
#   Q4 FY26 0.71(구조조정 $306M), Q1 FY27 0.08(구조조정 $41M) → GAAP의 약 190% → 미완성(2026-11-09). 상각은 반복으로 둔다(조정표에 상각 항목 없음).
#   4분기 EPS FY25·FY26은 보도자료(Q4_EPS_OVERRIDE — −1.51·−0.32, 역산 −1.52·−0.31).
# 주식 수: 표지가 A·B주 종류별이라 분기 가중평균(기본 363.3M)으로 대신한다(SHARES_WA_FALLBACK) — 9/30 실제 발행 362.3M과 약 0.3% 차이(Codex r1).
# 엔진 입력(2026-11-09): 차입금 $7,251M(1년 안 503 + 장기 6,748 — DEBT_TOTAL_TAG), 현금 $3,198M(제한 현금 포함 합계 태그 — EV_TAGS_BY_CIK), 자본 StockholdersEquity $4,038M.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q1 FY27', 'Q1 FY26', 'Q4 FY26'
L8 = ['Q2 FY25', 'Q3 FY25', 'Q4 FY25', 'Q1 FY26', 'Q2 FY26', 'Q3 FY26', 'Q4 FY26', 'Q1 FY27']
FY_NAME_OFFSET = 0   # 6월 결산 이름(끝난 해) — 2026-09-30 분기 10-Q 표지도 2027 회계연도 1분기로 적는다
FY_ENDS, FY_LABEL = ('2026-06-30', '2025-06-30'), 'FY2026'
VOTES, VERDICT = (0, -1, 0), '판정 보류'
CO = 'Estée Lauder'
S_ = 'https://www.sec.gov/Archives/edgar/data/1001250/'
SEC = S_
TENQ = S_ + '000100125026000060/el-20260930.htm'; TENQ_NAME = 'Q1 FY27 10-Q'
PR = {'q1': S_ + '000100125026000057/fy2027q1exhibit991.htm', 'q4': S_ + '000100125026000038/elq4fy2026exhibit991.htm',
      'q3': S_ + '000100125026000017/fy2026q3exhibit991.htm', 'q2': S_ + '000100125026000004/fy2026q2exhibit991.htm',
      'puig': S_ + '000100125026000010/exhibit991_march2026.htm', 'cmd': S_ + '000100125026000066/a992beautyreimagined_tur.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="elFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(구조조정·소송 합의 등 일회성이 최근 4분기 GAAP 이익보다 크다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-40, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 일회성 항목이 최근 4분기 GAAP 이익의 30% 이상이면 판정을 보류하는데, EL은 최근 4분기 GAAP 희석 EPS가 $1.00, 회사 조정 EPS가 $2.91이다. '
              '차이 세후 주당 약 $1.91(GAAP의 약 190%)은 대부분 2024년 2월 시작한 구조조정(총 세전 약 $1.7B, 약 1만 명 감축, 2027 회계연도 말 마무리 예정)의 비용·반품이고, FY26 3분기(2026년 1~3월) 증권 집단소송 합의 손실 $84M(보험 회수 예상분 차감)이 더해졌다. '
              '구조조정 비용이 큰 FY26 분기들이 최근 4분기에서 모두 빠지는 2027 회계연도 4분기 실적(2027년 8월 예상) 때 다시 판정할 예정이고, 그 전에도 분기마다 비중을 다시 센다 — 회사 FY27 전망의 일회성은 구조조정(주당 약 $0.44~0.50)·Forest Essentials 일회성 지급(약 $0.10)과 평가 이익(약 −$0.25~0.27)이라, 비용만 더해도 GAAP 전망($2.85~3.18)의 30% 아래다. '
              '1분기 기준으로는 본업이 돌아서는 모습이다(FY26 연간 유기 +3%) — 1분기(2026년 9월) 매출 $3.7B(+7%, 유기 +6%), 향수 +19%·스킨케어 +5%, 조정 영업이익률 12.1%(1년 전 7.3%). 지역으로는 중국 본토(+15%, 유기 +9%)와 면세를 포함한 아시아·태평양(유기 +10%)이 끌었는데, 베이징·상하이 공항 면세 사업자 교체로 1년 전이 부진했던 기저 효과가 섞여 있다. 회사는 FY27 유기 매출 성장 전망을 +4.0~5.5%, 조정 EPS를 $3.20~3.45로 올리면서 상반기 성장이 하반기보다 높다고 예고했다. 관세는 FY27 수익성·현금흐름에 부정적이며 세율에 따라 영향이 클 수 있다고 적었다(10-Q). 신용등급은 S&P A−(안정), Moody\'s A3(부정적 전망)이다. '
              '11월 4일 투자자 행사에서는 전략 Beauty Reimagined 아래 FY30까지 해마다 유기 매출 중간 한 자릿수 성장, FY30 조정 영업이익률 16.5~18.5%를 목표로 냈다. CEO는 Stéphane de La Faverie, CFO는 Akhil Shrivastava다. 11월 17일 주총에서 Rolex CEO Jean-Frédéric Dufour 등 새 이사 2명을 뽑는다. '
              '10월 인도 브랜드 Forest Essentials의 나머지 지분 51%를 $160M에 사, FY27 2분기에 약 $94M의 평가 이익과 $37M의 일회성 지급 비용이 함께 잡힌다. 2026년 3월 스페인 화장품 회사 Puig와 합병을 협의 중이라고 확인했으나, 검토한 공시 범위에서는 후속 합의가 확인되지 않는다. '
              '공개 자사주 매입 프로그램은 2022년 12월부터 멈춰 있고(분기 소액 취득은 주식보상 세금 원천징수분) 분기 배당 $0.35를 낸다. 창업 가문이 1주 10표인 B주 1.15억 주로 의결권 대부분을 쥔다(2025년 11월 Leonard Lauder 후손 신탁이 B주 약 1,100만 주를 A주로 바꿔 매각). 탈크(석면) 소송은 2024년 합의 틀로 FY25에 $159M을 반영했고, 회사는 추가 손실이 크지 않을 것으로 본다.')
PH = ['PG', 'CL', 'KVUE', 'CHD', 'KMB']
PEER_FILE = 'peer_universe/consumer_staples.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '생활·개인용품 5곳 PER 비교 (점수는 S&P500 필수소비재 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 필수소비재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 필수소비재 대비 배수 순위 (v2/peer_universe/consumer_staples.json)'
PEER_TIP = ('S&P500 필수소비재(EL 제외)와 배수 순위를 매긴 값이다.',
            '식품·음료·생활용품·유통이 섞여 있다. 차트에는 생활·개인용품 회사만 보인다.')
# 매출(Q1 FY27 보도자료 상품군): 스킨케어 1,651 + 메이크업 1,048 + 향수 861 + 헤어 128 + 기타 28 = 3,716, 구조조정 반품 −1 → 3,715.
SEG = [('스킨케어', 1651.0, '#040a2b'), ('메이크업', 1048.0, '#c9a96e'), ('향수', 861.0, '#7d6b91'), ('헤어케어', 128.0, '#a3b8c9')]
SEG_ADJ = 27.0   # 기타 상품 28(XBRL 부문 사실 없음) + 구조조정 반품 −1
SEG_ADJ_LABEL = '기타·구조조정 반품'
SEG_TITLE = '매출 구성 — 상품군별'
# 손 뉴스: 실적 4건 + Puig 협의 확인 + 투자자 행사. 반응일: 실적은 장 전 → 그날, Puig는 장 마감 뒤 → 다음 날. 색은 사건 성격, 수치는 그날 주가.
NEWS_RANGE = '2026.02 ~ 2026.11'
NEWS = [
    ('green', '2026년 11월 4일 장 전 — 투자자 행사(Capital Markets Experience)', '2026-11-04',
     'FY30까지 해마다 유기 매출 중간 한 자릿수 성장 · FY30 조정 영업이익률 16.5~18.5% 목표 — 그날 주가 +6.3%', 'cmd', 'Estée Lauder 발표 자료 (SEC 8-K)'),
    ('green', '2026년 11월 2일 장 전 — Q1 FY27 실적', '2026-11-02',
     '매출 $3.7B(+7%, 유기 +6%) · GAAP 희석 EPS $0.64 · 조정 EPS $0.72(1년 전 $0.32) · FY27 조정 EPS 전망 $3.20~3.45로 상향 — 그날 주가 −4.1%', 'q1', 'Estée Lauder 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 8월 19일 장 전 — FY26 4분기·연간 실적', '2026-08-19',
     'FY26 매출 $15.0B(+5%, 유기 +3%) · 연간 GAAP 희석 EPS $0.50 · 조정 EPS $2.51(+66%) · 4분기 GAAP $(0.32)(구조조정 $306M) — 그날 주가 +16.3%', 'q4', 'Estée Lauder 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 1일 장 전 — Q3 FY26 실적', '2026-05-01',
     '매출 $3.7B(+5%, 유기 +2%) · GAAP 희석 EPS $0.24(구조조정·증권 집단소송 합의 $84M) · 조정 EPS $0.91(+40%) — 그날 주가 +3.4%', 'q3', 'Estée Lauder 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 3월 23일 장 마감 뒤 — Puig와 합병 협의 확인', '2026-03-24',
     '스페인 화장품 회사 Puig와 사업 합병을 협의 중이라고 확인 · 결정·합의 없음 — 다음 날 주가 −9.8%(발표 당일에도 −7.7%)', 'puig', 'Estée Lauder 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 5일 장 전 — Q2 FY26 실적', '2026-02-05',
     '매출 $4.2B(+6%, 유기 +4%) · GAAP 희석 EPS $0.44 · 조정 EPS $0.89(+43%) · 연간 조정 EPS 전망 상향 — 그날 주가 −19.2%(보도자료의 3분기 마진 축소·면세 사업자 교체 역풍·관세 전망이 단서지만 원인은 단정 못 함)', 'q2', 'Estée Lauder 실적 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 30, 'nt': 21, 'mean': 117.14, 'median': 120, 'low': 92, 'high': 129, 'sb': 9, 'b': 6, 'h': 14, 's': 0, 'ss': 1}
ANALYST_ASOF = '2026-11-09'

# 파이프라인 자동 재판정용 — 일회성이 든 분기(결산일: 항목, 세후 주당).
ONEOFF_QUARTERS = {'2025-12-31': '구조조정 반품·비용 0.45($207M)',
                   '2026-03-31': '구조조정 0.49($224M) · 증권 집단소송 합의 0.18($84M)',
                   '2026-06-30': '구조조정 0.71($306M)',
                   '2026-09-30': '구조조정 0.08($41M)'}

# 미완성 카드 표시(2026-11-08 사용자 규칙, D·SRE 방식).
INCOMPLETE_SHORT = '일회성 비용이 이익보다 큼'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익보다 큰 구조조정·소송 합의 비용(세후 주당 약 $1.91, GAAP의 약 190%)이 들어 있다 — 배수 판정이 왜곡돼 보류한다. 재검토는 이르면 2027년 8월(FY27 4분기 실적) — 구조조정 비용이 큰 FY26 분기가 빠질 때'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익보다 큰 구조조정·소송 합의 비용(세후 주당 약 $1.91, GAAP의 약 190%)이 들어 있다 — 배수 판정이 왜곡돼 보류한다. 재검토는 이르면 2027년 8월(FY27 4분기 실적) — 구조조정 비용이 큰 FY26 분기가 빠질 때'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 일회성 비용이 이익보다 큼 · 재검토 이르면 2027년 8월</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 일회성 비용이 이익보다 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="elFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">일회성 비용이 이익보다 큼</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
# 구조조정 비용이 섞인 GAAP 마진·영업이익을 체크포인트·Bear 근거로 쓰지 않는다(ZBH·IP와 같은 처리)
_c2 = h[h.index('<strong style="color:var(--accent2);">②</strong>'):]; _c2 = _c2[:_c2.index('</div>')]
h = h.replace(_c2, '<strong style="color:var(--accent2);">②</strong> Q2 FY27 회사 조정 영업이익률이 1년 전(Q2 FY26 14.4%)보다 높은지 — 2분기는 연말 성수기라 연간 전망(12.9~13.7%)보다 높게 나오는 분기다. GAAP 마진엔 구조조정 비용이 섞여 비교 기준으로 쓰지 않는다', 1)
h = h.replace('<span class="zone-val">$1M</span>', '<span class="zone-val" title="주식보상 세금 원천징수용 6,591주 — 공개 매입 프로그램은 2022년 12월부터 0">$1M(원천징수분)</span>', 1)
h = _re0.sub(r'(<span class="bb-text">순차입금\(리스 포함\) \$[0-9.]+B, 최근 4분기 영업이익의 [0-9.]+배)\.', r'\1 — 구조조정 비용이 섞인 GAAP 기준이고 회사 조정 영업이익 기준으로는 약 3배다. 무디스는 A3에 부정적 전망을 붙여 두었다.', h, count=1)
h = _re0.sub(r'<span class="bb-head">투자</span><span class="bb-text">Q1 FY27 FCF[^<]*</span>', '<span class="bb-head">관세</span><span class="bb-text">회사는 관세가 FY27 수익성·현금흐름에 부정적이고 세율에 따라 영향이 클 수 있다고 적었다(10-Q). FY27 영업현금흐름 전망($1.4~1.5B)도 구조조정 현금 지급 탓에 FY26보다 낮다. 1분기 FCF −$235M은 성수기 재고를 쌓는 계절 요인이 크다.</span>', h, count=1)
h = _re0.sub(r'(지배적 내러티브 · [^<]*?)영업이익률 [0-9.]+%\(1년 전 [0-9.]+%\)', r'\1조정 영업이익률 12.1%(1년 전 7.3%)', h, count=1)
_c1 = h[h.index('<strong style="color:var(--accent2);">①</strong>'):]; _c1 = _c1[:_c1.index('</div>')]
h = h.replace(_c1, '<strong style="color:var(--accent2);">①</strong> Q2 FY27 유기 매출 성장이 FY27 전망(+4.0~5.5%)의 위쪽에 있는지 — 회사가 상반기가 하반기보다 높다고 예고했으므로 1분기(+6%)보다 낮다는 것만으로 경고로 읽지 않는다', 1)
"""]

AUTO = True
SEG_MAP = {
 "concepts": ["el:RevenueFromContractWithCustomerExcludingAssessedTaxAdjusted"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {},
 "members": {"el:SkinCareMember": ["스킨케어", "#040a2b"], "el:MakeupMember": ["메이크업", "#c9a96e"], "el:FragranceMember": ["향수", "#7d6b91"], "el:HairCareMember": ["헤어케어", "#a3b8c9"]}
}
