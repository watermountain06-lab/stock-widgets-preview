CIK = '0001792044'
BUILD = {'no_dcf': '미완성 — 회사가 매 분기 내는 특별 항목(구조조정·인수 비용 등)이 최근 4분기 GAAP를 적자로 만든다'}   # 2026-11-08 사용자 결정(일회성이 GAAP를 적자로 만들면 미완성 — 매 분기 반복돼도 회사 분류대로)
# VTRS(비아트리스) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 말. 복제약·바이오시밀러·브랜드 의약품(2020 Mylan + Upjohn 합병).
# 출처: SEC XBRL, Q3 2026 10-Q(2026-11-05 09:23 동부 장중 → 그날, 카드 기준일 11-06 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 06:4x~08:5x 동부 → 그날),
#        Biocon Biologics 지분 매각(2025-12-08 07:00 동부 → 그날), CFO 교체(2026-05-04 16:39 동부 → 05-05), Pacira 인수 합의(2026-10-08 08:38 동부 → 그날).
# 엔진 입력(2026-11-08): 차입금 $13,315M(1년 안 1,727.5 + 장기 11,587.5), 현금 $1,789M, 단기투자는 연간 값만이라 EV에서 뺐다(EV_TAGS_BY_CIK).
#   4분기 EPS 2025는 보도자료(Q4_EPS_OVERRIDE — 역산 −0.34, 보도자료 −0.30). 순이익 태그 NetIncomeLossAvailableToCommonStockholdersBasic(fetch_financials).
# 일회성(E54): 최근 4분기 GAAP 희석 EPS −0.53(−0.30 + 0.15 − 0.10 − 0.28) 대 회사 조정 EPS 2.56(0.57 + 0.59 + 0.69 + 0.71).
#   인수 상각(세전 683 + 592 + 586 + 614 = $2,475M)·주식 보상(세전 $176M)은 반복 비용으로 둔다. 특별 항목(세전, 소송·사업 매각 손실·인수 비용·구조조정·원가·판관비·기타 특별항목):
#   Q4 2025 $419M · Q1 2026 $464M · Q2 2026 $435M · Q3 2026 $231M = $1,549M → 이것만 빼도 GAAP가 흑자로 바뀐다 → 미완성(2026-11-08 사용자 결정 — 매 분기 반복되지만 회사 분류대로).
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (-1, 1, 0), '판정 보류'
CO = 'Viatris'
S_ = 'https://www.sec.gov/Archives/edgar/data/1792044/'
SEC = S_
TENQ = S_ + '000179204426000057/vtrs-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000179204426000053/exhibit991-3q26earningsrel.htm', 'q2': S_ + '000179204426000037/exhibit991-2q26earningsrel.htm',
      'q1': S_ + '000179204426000025/exhibit991-1q26earningsrel.htm', 'q4': S_ + '000179204426000010/exhibit991-4q25earningsrel.htm',
      'pacira': S_ + '000114036126039024/ef20083514_ex99-1.htm', 'cfo': S_ + '000114036126018887/ef20072373_ex99-1.htm',
      'biocon': S_ + '000114036125044706/ef20060770_ex99-1.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="vtrsFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(최근 4분기 GAAP가 특별 항목으로 적자)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (5년 · 실제 5년 연 {pct(HIST[\'growth_5y\'])})</span>'
Y2 = (-100, 20)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 일회성이 최근 4분기 GAAP 이익을 적자로 만들면 판정을 보류하는데, VTRS는 최근 4분기 GAAP 희석 EPS가 −$0.53이고 회사 조정 EPS는 $2.56이다. '
              '차이 가운데 가장 큰 것은 회사가 인수 회계 상각으로 묶어 빼는 세전 약 $2.5B다 — 대부분 2020년 합병으로 생긴 무형자산 상각이라 카드는 반복 비용으로 보지만, 그 안에는 연구개발 자산 손상(2025년 4분기 $72M 등)도 일부 섞여 있다. '
              '나머지는 회사가 특별 항목으로 빼는 구조조정·인수 관련 비용·소송·원가 특별항목 등 세전 약 $1.55B로, 최근 4분기 순손실 $608M보다 커서 이것만 빼도(세금 효과 전 기준) GAAP가 흑자로 바뀌어 판정을 보류한다. '
              '이 항목들은 분기마다 $2~5억씩 이어져 왔다 — 2026년 2월 끝낸 전사 전략 검토에 따라 앞으로 3년간 인력 최대 약 10%를 줄이는 구조조정(세전 비용 $7~8.5억)을 진행 중이라 당분간 계속 나올 수 있다. '
              '그래서 특정 분기가 빠지길 기다리는 대신 두 조건이 함께 맞을 때 다시 본다 — 최근 4분기 합산 GAAP 순이익이 흑자이고, 특별 항목(세전)이 그 4분기 이익의 30% 아래일 때다. 2026년 1~3분기 EPS 합이 −$0.23이라 4분기 한 분기 흑자만으로는 풀리지 않고, 구조조정이 2028년까지 이어지며 Pacira 인수로 인수 비용과 새 상각이 더해져 2027년 2월에 풀릴 가능성은 낮다. 3분기만 보면 특별 항목을 다 포함해도 세전 GAAP 이익은 +$128M이었고, 적자(−$325M)는 불확실한 세무 포지션 변경 등으로 잡힌 법인세 $453M 때문이었다(회사 조정표는 이 중 $273M을 되돌린다). '
              '본업은 중국 성장과 비용 절감이 공급 차질을 메우는 구조다 — 3분기 매출 $3.75B(1년 전과 비슷)에서 중국은 +14%였지만 선진국 −2%·신흥국 −7%·일본 등 −6%였고, 회사 조정 EBITDA는 +4%였다. 회사는 2026년 조정 EPS 전망을 $2.56~2.63로 올렸다. 공급 차질의 중심은 인도 공장이다 — Nashik 공장은 2월 화재, 5월 FDA 지적(483), 9월 공식 조치 필요(OAI) 판정 뒤 10월 자발적으로 생산을 멈췄고 2027년 1분기 재가동을 예상한다(매출 영향 3분기 약 $1억, 4분기 약 $1억 추정). 2024년 경고장·수입 금지를 받은 Indore 공장은 아직 FDA 재검사를 기다리고 있고, 이를 둘러싼 증권 집단소송과 주주대표소송이 진행 중이다. 전략 검토로 3년간 총 $650M 비용 절감(최대 $250M 재투자)을 목표로 한다. '
              '10월 Pacira BioSciences를 주당 $36.50, 총 $1.65B(현금)에 사기로 했다(EXPAREL·ZILRETTA — 발표 때는 연내, 11월 5일에 11월 말 마무리 예상). 12월 27일에는 비마약성 진통제 fast-acting meloxicam의 FDA 결정이 예정돼 있다. 2025년 12월 6일 Biocon Biologics 지분을 팔기로 해 받은 현금과 Biocon 주식(7월 처분)으로 모두 약 $780M을 회수했다. 8월에는 Tyrvaya 판권을 Harrow에 팔면서 2분기에 손상 $178M을 잡았다. '
              '5월 CFO Doretta Mistras가 떠나 Paul Campbell이 임시 CFO를 맡고 있고, 2월 법무 책임자도 바뀌었다. 9월 말까지 자사주 약 $300M과 배당 지급 약 $417M으로 약 $717M을 주주에게 돌려줬고 남은 매입 한도는 약 $700M이다. '
              '주가는 1년 새 거의 두 배가 됐다 — 자기 이력 점수가 매우 낮은 것은 지난 5년(주가 $10 안팎, 영업권 손상으로 장부가 축소)보다 지금 배수가 높다는 뜻이고, 동종업 대비로는 싸다. 최근 4분기 GAAP가 적자라 PER 숫자는 나오지 않으며, 평가와 평균에서 뺀다.')
PH = ['PFE', 'BMY', 'MRK', 'GILD', 'AMGN', 'JNJ']
PEER_FILE = 'peer_universe/health_care.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '제약 6곳 PER 비교 (점수는 S&P500 헬스케어 기준)', 'pbr': 'PBR 비교', 'psr': 'PSR 비교',
                'pcr': 'PCR(FCF) 비교', 'evebitda': 'EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 헬스케어 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 헬스케어 대비 배수 순위 (v2/peer_universe/health_care.json)'
PEER_TIP = ('S&P500 헬스케어(VTRS 제외)와 배수 순위를 매긴 값이다.',
            '제약·의료기기·보험이 섞여 있다. 차트에는 대형 제약 6곳만 보인다(복제약 중심 회사는 S&P500에 없다).')
# 매출(Q3 2026 보도자료 지역별 순매출): 선진국 2,215.9 + 중국 702.6 + 신흥국 529.1 + JANZ 287.1 = 3,734.7.
SEG = [('선진국(북미·유럽)', 2215.9, '#0f2d69'), ('중국(Greater China)', 702.6, '#8dc63f'), ('신흥국', 529.1, '#4f7fc4'), ('일본·호주·뉴질랜드(JANZ)', 287.1, '#c9d3e6')]
SEG_ADJ = 0
SEG_TITLE = '지역별 순매출 구성(기타매출 제외)'
# 손 뉴스: 실적 4건 + Pacira 인수 + CFO 교체 + Biocon 지분 매각. 반응일: 장 전 → 그날, 장 마감 뒤 → 다음 날. 색은 사건 성격, 수치는 그날 주가.
NEWS_RANGE = '2025.11 ~ 2026.11'
NEWS = [
    ('green', '2026년 11월 5일 장 전 — Q3 2026 실적', '2026-11-05',
     '매출 $3.75B(1년 전과 비슷) · GAAP 희석 EPS −$0.28(법인세 $453M) · 조정 EPS $0.71(+6%) · 중국 +14% · Nashik 공장 생산 중단(매출 영향 약 $1억) · 2026 전망 중간값 모두 상향(조정 EPS $2.56~2.63) — 그날 주가 −1.3%', 'q3', 'Viatris 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 10월 8일 장 전 — Pacira BioSciences 인수 합의', '2026-10-08',
     '주당 $36.50 현금, 총 $1.65B · EXPAREL·ZILRETTA 확보 · 연내 마무리 예상 · 회사는 조정 지표에 바로 보탬이 된다고 설명 — 그날 주가 −0.3%', 'pacira', 'Viatris 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 8월 6일 장 전 — Q2 2026 실적', '2026-08-06',
     '매출 $3.8B(+5%) · GAAP 희석 EPS −$0.10(Tyrvaya 매각 손상 $178M) · 조정 EPS $0.69(+11%) · 차입 배수 2.9배 · 하반기 공급 차질 경고 — 그날 주가 −7.7%', 'q2', 'Viatris 실적 보도자료 (SEC 8-K)'),
    ('green', '2026년 5월 7일 장 전 — Q1 2026 실적', '2026-05-07',
     '매출 $3.5B(+8%) · GAAP 희석 EPS $0.15 · 조정 EPS $0.59(+18%) · 연간 전망 유지 — 그날 주가 +9.0%', 'q1', 'Viatris 실적 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 4일 장 마감 뒤 — CFO 교체', '2026-05-05',
     'CFO Doretta Mistras가 다른 회사로 떠나고 회계 책임자 Paul Campbell이 임시 CFO(5월 8일부터) — 다음 날 주가 +2.1%', 'cfo', 'Viatris 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 2월 26일 장 전 — 2025년 연간 실적 · 전략 검토 결과', '2026-02-26',
     '4분기 GAAP 희석 EPS −$0.30 · 조정 EPS $0.57 · 3년간 비용 절감 $650M(최대 $250M 재투자) · 인력 최대 약 10% 감축 구조조정(세전 $7~8.5억) — 그날 주가 −5.2%', 'q4', 'Viatris 실적 보도자료 (SEC 8-K)'),
    ('green', '2025년 12월 6일(토) — Biocon Biologics 지분 매각 발표', '2025-12-08',
     'Biocon Biologics 우선주 지분을 $815M(현금 $400M + Biocon 주식 $415M)에 Biocon에 팔기로 · 바이오시밀러 경업 금지 조기 종료 — 다음 거래일(12/8) 주가 +1.5%', 'biocon', 'Viatris 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Buy', 'n': 12, 'nt': 9, 'mean': 20.67, 'median': 20, 'low': 14, 'high': 28, 'sb': 6, 'b': 1, 'h': 4, 's': 1, 'ss': 0}
ANALYST_ASOF = '2026-11-08'

# 파이프라인 자동 재판정용 — 일회성이 든 분기(결산일: 항목). VTRS는 특별 항목이 매 분기 이어져 분기가 빠져도 바로 풀리지 않는다.
ONEOFF_QUARTERS = {'2025-12-31': '특별 항목 세전 $419M(원가 특별항목 $193M·인수 비용 $74M 등)',
                   '2026-03-31': '특별 항목 세전 $464M(원가 특별항목 $142M·구조조정 $93M 등)',
                   '2026-06-30': '특별 항목 세전 $435M(판관비 특별항목 $241M·소송 $73M 등)',
                   '2026-09-30': '특별 항목 세전 $231M(구조조정 $66M·원가 특별항목 $66M 등) · 법인세 관련 항목 +$273M'}

# 미완성 카드 표시(2026-11-08 사용자 규칙, D·SRE 방식).
INCOMPLETE_SHORT = '특별 항목으로 GAAP 적자'
INCOMPLETE_WHY = '최근 4분기 GAAP 이익이 회사가 매 분기 내는 특별 항목(구조조정·인수 비용 등 세전 약 $1.55B)으로 적자다 — 배수 판정이 왜곡돼 보류한다. GAAP가 흑자로 돌아서고 특별 항목이 30% 아래로 줄면 다시 본다'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP 이익이 회사가 매 분기 내는 특별 항목(구조조정·인수 비용 등 세전 약 $1.55B)으로 적자다 — 배수 판정이 왜곡돼 보류한다. GAAP가 흑자로 돌아서고 특별 항목이 30% 아래로 줄면 다시 본다'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 특별 항목으로 GAAP 적자 · 최근 4분기 GAAP 흑자 + 특별 항목 30% 미만일 때 다시 본다</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 특별 항목으로 GAAP 적자. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="vtrsFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">특별 항목으로 GAAP 적자</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
# 특별 항목이 섞인 GAAP 마진을 Bear·체크포인트 근거로 쓰지 않는다(IP·CRL과 같은 처리), 배당 칸은 자본 변동표 선언액으로
_b1 = '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">마진</span><span class="bb-text">최근 4분기 영업이익률 −0.0%(영업적자).</span></div>'
assert _b1 in h
h = h.replace(_b1, '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">특별 항목</span><span class="bb-text">회사가 매 분기 특별 항목(세전 분기 $2~5억)을 내 GAAP가 적자다 — 3년 구조조정(세전 $7~8.5억)이 이어진다.</span></div>', 1)
_c2 = h[h.index('<strong style="color:var(--accent2);">②</strong>'):]; _c2 = _c2[:_c2.index('</div>')]
assert 'GAAP 영업이익률' in _c2
h = h.replace(_c2, '<strong style="color:var(--accent2);">②</strong> Q4 2026 GAAP 순이익과 특별 항목(최근 4분기 세전 약 $1.55B) 흐름 — 미완성은 최근 4분기 GAAP 이익이 흑자이고 특별 항목이 그 30% 아래일 때 푼다', 1)
h = h.replace('다음 확인 포인트 · 2027년 2월 25일 무렵 (예상) Q4 2026 실적 공시.', '다음 확인 포인트 · 2027년 2월 25일 무렵 (예상) Q4 2026 실적 공시 — 볼 것은 특별 항목이 분기 $1억대로 내려오는지(이때 미완성이 풀릴 가능성은 낮다). 그 전 12월 27일 fast-acting meloxicam FDA 결정.', 1)
h = _re0.sub(r'(영업이익률 [0-9.−-]+%\(1년 전 [0-9.−-]+%)\)', r'\1, GAAP — 인수 상각·특별 항목 포함)', h, count=1)
_bs = '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">특별 항목</span>'
assert _bs in h
h = h.replace(_bs, '<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">공급</span><span class="bb-text">인도 Nashik 공장 생산 중단(2027년 1분기 재가동 예정)과 Indore 수입 금지로 유럽·신흥국 공급이 막혔다 — 분기 매출 영향 약 $1억.</span></div>\n      ' + _bs, 1)
_dv = '<span class="zone-label">보통주 배당 지급</span>\n          <span class="zone-val">공시 없음</span>'
assert _dv in h
h = h.replace(_dv, '<span class="zone-label">보통주 배당 (연초~9/30 선언 기준)</span>\n          <span class="zone-val">$429M</span>', 1)
"""]

# ── 자동 카드 — 부문 지도(seg_map_propose 뒤 원문 대조). 원문: Q3 2026 보도자료 2,215.9 + 702.6 + 529.1 + 287.1 = 3,734.7 ──
AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"vtrs:DevelopedMarketsSegmentMember": ["선진국(북미·유럽)", "#0f2d69"],
             "vtrs:GreaterChinaSegmentMember": ["중국(Greater China)", "#8dc63f"],
             "vtrs:EmergingMarketsSegmentMember": ["신흥국", "#4f7fc4"],
             "vtrs:JapanAustraliaAndNewZealandSegmentMember": ["일본·호주·뉴질랜드(JANZ)", "#c9d3e6"]}
}
