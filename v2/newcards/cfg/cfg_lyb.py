CIK = '0001489393'
BUILD = {'no_dcf': '미완성 — 유럽 사업 매각 손실 등 일회성이 최근 4분기 GAAP 이익의 약 79%'}   # 2026-11-07·08 사용자 규칙(일회성 30% 이상이면 미완성, 회사 분류를 따른다) — RVTY·ROP·FANG와 같은 처리
# LYB(라이온델바젤) v2 카드 설정 — 자동 카드(AUTO), 미완성(판정 보류). 회계연도 12월 말. 올레핀·폴리올레핀(미주, 유럽·아시아·기타), 중간재·파생품(프로필렌옥사이드·옥시연료), 고급 폴리머, 기술 라이선스.
# 출처: SEC XBRL, Q3 2026 10-Q(2026-10-30 접수, 카드 기준일 11-12 종가), 실적 보도자료(8-K 2.02항 — 모두 장 전 06:3x 동부 → 그날),
#        Houston 정유소 매각 계약(Q3 실적 8-K 8.01항, 장 전 → 그날), 자사주 매입 승인(2026-05-22 주총 8-K, 16:05 동부 → 다음 거래일 5/26).
# 분기 이력: RESTATED_LATEST는 쓰지 않는다 — 2023년 분기는 재작성 값이 없어 재작성 연간 − 원공시 9개월로 Q4 2023 매출이 $2.2B로 깨졌다(Codex r2). 처음 공시값 한 기준으로 두고 MODEL_NOTE에 밝힌다.
# 일회성(E54): 최근 4분기 GAAP 희석 EPS 3.96(−0.45 + 0.38 + 1.71 + 2.32 — 보도자료) 대 회사 '확인 항목 제외' EPS 7.07(−0.26 + 0.49 + 4.30 + 2.54) → 차이 3.11(GAAP의 약 79%, 회사 주당 표 = 세후).
#   항목(주당): Q2 2026 유럽 4개 사이트 매각 손실 2.27(세전 $734M — 영업외), 자산 감액 0.04·0.03·0.18·0, 현금 개선 계획 비용 0.02·0·0.07·0.01, 사이트 폐쇄 0.08·0.01·0.06·0.17,
#   유럽 거래 비용(이전 서비스 수입 차감) 0.03·0.03·−0.03·−0.02, 중단사업(Houston 정유소) 손실 0.02·0.04·0.04·0.06. 비용만 약 3.16(80%) — 미완성.
CUR, YO, QO = '2026-09-30', '2025-09-30', '2026-06-30'
QLABEL, YL, QQL = 'Q3 2026', 'Q3 2025', 'Q2 2026'
L8 = ['Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025', 'Q1 2026', 'Q2 2026', 'Q3 2026']
FY_ENDS, FY_LABEL = ('2025-12-31', '2024-12-31'), 'FY2025'
VOTES, VERDICT = (0, 1, 0), '판정 보류'
CO = 'LyondellBasell'
NI_TAGS = ['ProfitLoss']   # 분기 순이익: NetIncomeLoss 태그가 2019년에 멈춤 — ProfitLoss(비지배 포함, 보도자료 순이익과 같음: Q3 2026 758, Q2 559)
S_ = 'https://www.sec.gov/Archives/edgar/data/1489393/'
SEC = S_
TENQ = S_ + '000148939326000070/lyb-20260930.htm'; TENQ_NAME = 'Q3 2026 10-Q'
PR = {'q3': S_ + '000148939326000067/a2026q3ex991_pressrelease.htm', 'q2': S_ + '000148939326000057/a2026q2ex991_pressrelease.htm',
      'q1': S_ + '000148939326000025/a2026q1ex991_pressrelease.htm', 'q4': S_ + '000148939326000003/a2025q4exhibit991.htm',
      'q3p': S_ + '000148939325000054/a2025q3ex991_pressrelease.htm', 'hou': S_ + '000148939326000067/lyb-20261029.htm', 'agm': S_ + '000148939326000034/lyb-20260522.htm'}
LINKS = {}
FAIRBAND_TITLE = 'id="lybFairBand" title="미완성 카드라 PER 구간으로 낸 적정주가를 표시하지 않는다(유럽 사업 매각 손실 등 일회성이 최근 4분기 GAAP 이익을 크게 깎는다)."'
HEADER_REQ_LABEL = '<span class="meta-label">현재가 요구 성장 (미완성 — 현금흐름 보류)</span>'
Y2 = (-30, 30)
ACT_REASON = ''
NONOP_WHAT = '투자'
MODEL_NOTE = ('미완성 카드다. 이 카드는 최근 4분기 GAAP 이익 대비 일회성이 순액이나 비용만으로 30% 이상이거나 GAAP가 적자면 판정을 보류하는데, LYB는 최근 4분기 GAAP 희석 EPS 합계가 $3.96으로 회사가 \'확인 항목\'을 뺀 EPS $7.07보다 $3.11(GAAP의 약 79%, 비용만 $3.16·약 80%) 작다. '
              '대부분 2026년 2분기 유럽 4개 사이트 매각 손실(세전 $734M, 주당 $2.27)이다 — 영업이익 아래 영업외 손실이라 PER은 크게 흔들리지만, 카드의 영업이익과 영업이익 + 감가상각으로 만든 EBITDA는 덜 흔들린다(회사가 발표하는 EBITDA에는 이 손실이 들어 있다). 나머지는 사이트 폐쇄(네덜란드 프로필렌옥사이드 합작 설비, 이탈리아 Brindisi 폴리프로필렌 설비, 고급 폴리머 사이트 등)·현금 개선 계획 비용·자산 감액, 그리고 2025년 2월 문을 닫은 Houston 정유소의 중단사업 손실이다. '
              '분기마다 다시 센다. 매각 손실이 든 2분기가 빠지는 2027년 2분기 실적(2027년 7월 말 예상)이 가장 이른 주요 확인 시점이다. 다만 4분기에 Houston 정유소 매각(장부상 자산 $15M·부채 $315M, 매각가 $321M)이 끝나면 중단사업 쪽에 일회성 이익이 잡힐 수 있고, 그러면 그 이익은 2027년 3분기 실적까지 최근 4분기에 남고 2027년 4분기 실적(2028년 1월 말 예상) 때 빠진다. 2분기가 빠진 뒤에도 남는 분기의 차이는 이어진다(3분기 주당 $0.22 — 사이트 폐쇄 0.17, 중단사업 0.06, 현금 개선 계획 0.01, 유럽 이전 서비스 수입 −0.02). 참고로 둔 자기 이력·동종업 PER은 중단사업 손실을 뺀 계속사업 EPS(최근 4분기 $4.12) 기준이라 총 GAAP EPS $3.96으로 낸 값보다 조금 낮고, 순이익 칸은 비지배 몫을 포함한 회사 연결 순이익이다. 2024년까지의 분기 값은 처음 공시한 값이라 정유 사업 매출·이익이 들어 있다(2024년 4분기 매출 $9.50B — 정유를 뺀 재작성 값은 $7.81B). 회사가 2023년 이전 분기를 다시 쓰지 않아 한 기준으로 맞출 수 없어서, 자기 이력 배수와 과거 성장률은 이 끊김을 안고 있다. '
              '이익은 업황에 크게 기대 있다 — 2025년에는 감액(영업권 손상 $972M 포함)으로 연간 GAAP 주당 손실 $2.34였다가, 2026년 중동 분쟁으로 세계 석유화학 원가 곡선이 가팔라지며 원가가 싼 미주 설비의 마진이 커졌다(회사 \'확인 항목 제외\' EPS 2분기 $4.30, 3분기 $2.54). 회사는 분쟁 전 상태로 돌아가는 데 예상보다 오래 걸릴 수 있다고 본다. '
              '배당은 2026년부터 분기 주당 $1.37에서 $0.69로 줄였고(9개월 지급 $672M, 1년 전 $1,321M), 5월 주총에서 발행 주식 10%(약 3,404만 주) 자사주 매입을 승인받았지만(2027년 11월까지), 2025년 9월 바꾼 신용 약정이 희석 상쇄분 말고는 매입을 막고 있어 9개월 실제 매입은 없다. 9월에 €500M 채권을 예정대로 갚았다. '
              '10월 29일 Houston 정유소 부지·자산을 Valero 자회사에 $320.5M에 팔기로 했다(4분기 종결 예상). 주가는 1월 30일 종가 $49.00에서 5월 1일 $74.99까지 올랐다.')
PH = ['DOW', 'DD', 'LIN', 'APD', 'PPG', 'ECL']
PEER_FILE = 'peer_universe/materials.json'
CHART_CAP, SELF_CAP, CHART_NOTE = {}, {}, {}
CHART_TITLES = {'per': '화학 6곳 PER 비교 (점수는 S&P500 소재 기준)', 'pbr': '화학 PBR 비교', 'psr': '화학 PSR 비교',
                'pcr': '화학 PCR(FCF) 비교', 'evebitda': '화학 EV/EBITDA 비교'}
PEER_NAME_TITLE = 'S&P500 소재 종목들보다 배수가 얼마나 낮은가. 높을수록 싸다.'
PEER_COMMENT = 'S&P500 소재 대비 배수 순위 (v2/peer_universe/materials.json)'
PEER_TIP = ('S&P500 소재(LYB 제외)와 배수 순위를 매긴 값이다.',
            '화학·산업용 가스·금속·건자재·포장재가 섞여 있다. 차트에는 화학 회사 6곳만 보인다.')
# 매출(Q3 2026 10-Q 부문 주석, 부문 간 매출 포함): O&P 미주 3,180 + O&P 유럽·아시아·기타 2,176 + 중간재·파생품 2,983 + 고급 폴리머 935 + 기술 114 = 9,388, 부문 간 −889 → 8,499.
SEG = [('올레핀·폴리올레핀 — 미주', 3180, '#00247d'), ('올레핀·폴리올레핀 — 유럽·아시아·기타', 2176, '#4a6fb5'), ('중간재·파생품(PO·옥시연료)', 2983, '#e4002b'), ('고급 폴리머', 935, '#f08a8a'), ('기술(라이선스·촉매)', 114, '#9fb3d9')]
SEG_ADJ = -889
SEG_TITLE = '매출 구성 — 사업 부문별'
# 손 뉴스: 최신 실적 8-K에 정유소 매각 계약(8.01항)이 함께 실려 최신 실적도 손으로 쓴다(안건 E32) — 계약은 8-K 본문 링크로 따로(Codex r1). 반응일: 실적은 모두 장 전 → 그날.
NEWS_RANGE = '2025.10 ~ 2026.11'
NEWS = [
    ('neutral', '2026년 10월 30일 장 전 — Houston 정유소 매각 계약(10월 29일 체결)', '2026-10-30',
     '2025년 2월 문을 닫은 Houston 정유소 부지·자산(Houston Refining, L.P.)을 Valero 자회사에 $320.5M에 팔기로 — 4분기 종결 예상, 실적과 같은 8-K', 'hou', 'LyondellBasell 8-K'),
    ('neutral', '2026년 10월 30일 장 전 — Q3 2026 실적', '2026-10-30',
     'GAAP 희석 EPS $2.32 · 확인 항목 제외 EPS $2.54 · €500M 채권 상환 — 그날 주가 +5.0%', 'q3', 'LyondellBasell 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 7월 31일 장 전 — Q2 2026 실적', '2026-07-31',
     'GAAP 희석 EPS $1.71(유럽 사업 매각 손실 $734M) · 확인 항목 제외 EPS $4.30 · 유럽 사이트 매각 완료 — 그날 주가 +2.7%', 'q2', 'LyondellBasell 보도자료 (SEC 8-K)'),
    ('neutral', '2026년 5월 22일 주총 — 자사주 매입 승인(발행 주식 10%)', '2026-05-26',
     '2027년 11월 22일까지 최대 3,404만 주 매입 승인 — 8-K 접수(장 마감 뒤) 다음 거래일 주가 −1.0%', 'agm', 'LyondellBasell 8-K'),
    ('green', '2026년 5월 1일 장 전 — Q1 2026 실적', '2026-05-01',
     'GAAP 희석 EPS $0.38 · 확인 항목 제외 EPS $0.49 · 중동 분쟁으로 세계 원가 곡선이 가팔라져 원가가 싼 설비 가동을 늘림 — 그날 주가 +0.5%', 'q1', 'LyondellBasell 보도자료 (SEC 8-K)'),
    ('red', '2026년 1월 30일 장 전 — 2025년 연간 실적', '2026-01-30',
     '4분기 GAAP 희석 주당 손실 $0.45 · 연간 주당 손실 $2.34(감액 $1.25B) · 확인 항목 제외 연간 EPS $1.70 · 현금 개선 목표 2026년 말 누적 $1.3B로 확대 — 그날 주가 −1.9%', 'q4', 'LyondellBasell 보도자료 (SEC 8-K)'),
    ('red', '2025년 10월 31일 장 전 — Q3 2025 실적', '2025-10-31',
     'GAAP 희석 주당 손실 $2.77(비현금 자산 감액 $1.2B) · 확인 항목 제외 EPS $1.01 — 그날 주가 +2.7%', 'q3p', 'LyondellBasell 보도자료 (SEC 8-K)'),
]
ANALYST = {'rating': 'Hold', 'n': 20, 'nt': 12, 'mean': 72.67, 'median': 72, 'low': 66, 'high': 83, 'sb': 2, 'b': 4, 'h': 11, 's': 1, 'ss': 2}
ANALYST_ASOF = '2026-11-21'

# 재검토 기록용(자동 재판정 코드는 아직 없음) — 일회성이 든 분기(결산일: GAAP와 확인 항목 제외 EPS 차이, 주당 $, +는 비용·−는 이익).
ONEOFF_QUARTERS = {'2025-12-31': '차이 0.19 — 사이트 폐쇄 0.08 · 감액 0.04 · 유럽 거래 비용 0.03 · 현금 개선 계획 0.02 · 중단사업 0.02',
                   '2026-03-31': '차이 0.11 — 감액 0.03 · 유럽 거래 비용 0.03 · 중단사업 0.04 · 사이트 폐쇄 0.01',
                   '2026-06-30': '차이 2.59 — 유럽 사업 매각 손실 2.27(세전 $734M) · 감액 0.18 · 현금 개선 계획 0.07 · 사이트 폐쇄 0.06 · 중단사업 0.04 · 이전 서비스 수입 −0.03',
                   '2026-09-30': '차이 0.22 — 사이트 폐쇄 0.17 · 중단사업 0.06 · 현금 개선 계획 0.01 · 이전 서비스 수입 −0.02'}

# 미완성 카드 표시(2026-11-08 사용자 규칙, AXON·RVTY·ROP·FANG 방식).
INCOMPLETE_SHORT = '유럽 사업 매각 손실이 큼'
INCOMPLETE_WHY = '최근 4분기 GAAP EPS($3.96)가 회사 확인 항목 제외 EPS($7.07)보다 $3.11 작다 — 대부분 2026년 2분기 유럽 4개 사이트 매각 손실(주당 $2.27)이라 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 가장 이른 주요 확인은 2027년 7월(2분기가 빠질 때)'
POST = [r"""
import re as _re0
_w = '최근 4분기 GAAP EPS($3.96)가 회사 확인 항목 제외 EPS($7.07)보다 $3.11 작다 — 대부분 2026년 2분기 유럽 4개 사이트 매각 손실(주당 $2.27)이라 배수 판정이 왜곡돼 보류한다. 분기마다 다시 세고, 가장 이른 주요 확인은 2027년 7월(2분기가 빠질 때)'
_hv = '<span class="meta-value" data-verdict style="font-size:22px;color:var(--gold);">판정 보류</span>'
if _hv in h and 'data-incomplete' not in h:
    h = h.replace(_hv, _hv + '<span data-incomplete style="display:block;font-size:12px;line-height:1.35;color:var(--text3);margin-top:2px;">미완성 — 유럽 사업 매각 손실이 큼 · 매 분기 재검토, 주요 확인 2027년 7월</span>', 1)
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다(보험사 등 — 영업이익·설비투자 구조가 맞지 않는다).', '미완성 카드다 — ' + _w + '. 그래서 현금흐름 내재가치 칸을 비우고 종합 판정을 보류한다(자기 이력·동종업 점수는 참고로 둔다).')
h = h.replace('이 종목은 현금흐름 내재가치를 계산하지 않는다.', '미완성 — 유럽 사업 매각 손실이 큼. 미완성 카드 규칙에 따라 종합 판정과 함께 현금흐름 내재가치도 보류했다.')
h = _re0.sub(r'(id="lybFairBand"[^>]*style=")[^"]*(">)[^<]*(<)', r'\1font-size:22px;color:var(--text3);\2해당 없음\3', h, count=1)
h = _re0.sub(r'<div class="note">미완성 카드다 — .*?</div>', '', h, count=1, flags=_re0.S)
h = h.replace("if (r) r.textContent = '내재가치를 계산하지 못했다 — ' + (D.unavailable || '입력 부족');", "if (r) r.textContent = '';")
h = h.replace('현금흐름 미적용', '현금흐름 보류(미완성)')
h = h.replace('내재가치를 계산하지 못했다 — 판정 보류 — ', '미완성 카드 — ')
h = h.replace('계산 불가 — 판정 보류 — ', '미완성 — ')
h = h.replace('계산 불가 — 미완성 — ', '미완성 — ')
h = h.replace("c.title = '계산 불가 — ' + why;", "c.title = why;")
h = _re0.sub(r'(<div class="verdict-summary-head">[^<]*)<span class="tag">[^<]*</span>', r'\1<span class="tag">유럽 사업 매각 손실이 큼</span>', h, count=1)
h = _re0.sub(r'<div class="bb-row bear"><span class="bb-icon">▼</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
h = _re0.sub(r'<div class="bb-row bull"><span class="bb-icon">▲</span><span class="bb-head">밸류</span>.*?</div>\n?', '', h, count=1, flags=_re0.S)
# Fable r1: 성장률·마진·부문 문장에 범위 변화·분쟁 마진을 붙이고, 체크포인트 ②를 쓸모 있는 기준으로
_scope = ' — 비교 기초인 2024년까지 매출에는 2025년 2월 문 닫은 정유 사업이, 2026년 5월 전 매출에는 판 유럽 사이트가 들어 있어 감소가 커 보인다'
h = _re0.sub(r'(<span class="bb-head">매출</span><span class="bb-text">[^<]*?3년 연평균[^<]*?\))\.?(</span>)', lambda m: m.group(1) + _scope + '.' + m.group(2), h, count=1)
h = _re0.sub(r'(<span class="bb-head">성장</span><span class="bb-text">[^<]*?)\.?(</span>)', lambda m: m.group(1) + _scope + '.' + m.group(2), h, count=1)
h = _re0.sub(r'(<span class="bb-head">마진</span><span class="bb-text">최근 4분기[^<]*?)\.?(</span>)', lambda m: m.group(1) + ' — 2·3분기 중동 분쟁으로 마진이 뛴 값이 크게 들어 있다.' + m.group(2), h, count=1)
h = _re0.sub(r'(<span class="bb-head">부문</span><span class="bb-text">올레핀·폴리올레핀 — 유럽·아시아·기타[^<]*?)\.?(</span>)', lambda m: m.group(1) + ' — 5월 유럽 사이트 매각 영향.' + m.group(2), h, count=1)
_c2 = h[h.index('<strong style="color:var(--accent2);">②</strong>'):]; _c2 = _c2[:_c2.index('</div>')]
if 'Q4 2025 −1.2%' in _c2:
    h = h.replace(_c2, '<strong style="color:var(--accent2);">②</strong> Q4 2026 GAAP 영업이익률이 직전 Q3 2026 12.6%에서 얼마나 내려오는지 — 1년 전 Q4 2025(−1.2%)는 업황 바닥이라 비교 기준으로 약하다. 정유소 매각 종결로 중단사업 일회성 이익이 생기는지도 본다', 1)
"""]

AUTO = True
SEG_MAP = {
 "concepts": ["us-gaap:Revenues"],
 "axis": "us-gaap:StatementBusinessSegmentsAxis",
 "extra": {"srt:ConsolidationItemsAxis": "us-gaap:OperatingSegmentsMember"},
 "members": {"lyb:OlefinsAndPolyolefinsAmericasMember": ["올레핀·폴리올레핀 — 미주", "#00247d"], "lyb:OlefinsAndPolyolefinsEuropeAsiaInternationalMember": ["올레핀·폴리올레핀 — 유럽·아시아·기타", "#4a6fb5"], "lyb:IntermediatesAndDerivativesMember": ["중간재·파생품(PO·옥시연료)", "#e4002b"], "lyb:AdvancedPolymerSolutionsMember": ["고급 폴리머", "#f08a8a"], "lyb:TechnologyMember": ["기술(라이선스·촉매)", "#9fb3d9"]},
 "ignore": ["lyb:CorporateNonSegmentAndEliminationsMember"]
}
